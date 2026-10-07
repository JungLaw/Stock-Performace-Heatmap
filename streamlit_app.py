"""
Stock Performance Heatmap Dashboard - Main Application

An interactive heatmap for visualizing stock and ETF performance
across different time periods and asset groups.

Run with: streamlit run streamlit_app.py
"""
import streamlit as st
import sys
import time
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
from typing import Dict, Any, Optional

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import our modules
from calculations.performance import (
    DatabaseIntegratedPerformanceCalculator,
    get_last_completed_trading_day,
    get_last_n_trading_days,
    is_us_trading_day,
)
from calculations.volume import DatabaseIntegratedVolumeCalculator
from calculations.technical import DatabaseIntegratedTechnicalCalculator
from data.data_acquisition import (
    DataAcquisitionManager,
    DataAcquisitionResult,
)
from data.data_mutation import DataMutationManager, MutationPlan
from data.database_manager import DatabaseManager
from data.universe_manager import UniverseManager
from visualization.heatmap import FinvizHeatmapGenerator, get_color_legend
from config.assets import (
    ASSET_GROUPS,
    CUSTOM_DEFAULT,
    get_tickers_only,
    SCD_DEFAULT_COUNTRY_TICKERS,
    SCD_DEFAULT_SECTOR_TICKERS,
    SCD_DEFAULT_CUSTOM_TICKERS,
)

# Rolling Heatmap Selection & Catalog architecture
# Grouping/selection truth lives in src/ui modules; streamlit_app.py only
# renders controls, stores session state, and passes resolved row_key sets
# into the existing downstream manual-control/render path.
from ui.rolling_heatmap_presets import CUSTOM_DEFAULT as RH_CUSTOM_DEFAULT
from ui.rolling_heatmap_classification import ROW_CLASSIFICATION
from ui.rolling_heatmap_selection import (
    describe_empty_selection,
    get_category_names,
    get_family_names,
    get_preset_names,
    get_scope_names,
    get_selection_modes,
    get_tag_names,
    get_window_names,
    resolve_row_selection,
)
from ui.rolling_heatmap_adapter import (
    INDICATOR_DEFS,
    apply_bbp_divergence_text_overlay,
    apply_cci_divergence_text_overlay,
    apply_uo_divergence_symbol_overlay,
    apply_hma_turn_text_overlay,
    apply_vwma_volume_extreme_text_overlay,
    build_plotly_heatmap_inputs,
    build_vwma_hover_opening,
)

# Developer-only diagnostic controls.
# Keep False for normal app use. Set True temporarily when running D3-C
# tail-buffer equivalence checks.
SCD_SHOW_TAIL_BUFFER_DIAGNOSTIC = False

# Stock Comparison Dashboard — Crossover Event Signal Rows v1 exposure.
#
# These are SCD-specific consumer defaults only. They do not mutate the global
# Rolling Heatmap Custom default, do not add computation, and do not alter
# rule-engine semantics.
SCD_CROSSOVER_EVENT_ROWS = [
    "EMA_9_X_EMA_21",
    "SMA_20_X_SMA_50",
    "SMA_50_X_SMA_200",
]

SCD_SINGLE_INDICATOR_MAIN_EXTRA_ROWS = [
    "SMA_20_X_SMA_50",
]

SCD_MULTIPLE_INDICATOR_CUSTOM_DEFAULT = [
    *RH_CUSTOM_DEFAULT,
    *[
        row_key
        for row_key in SCD_CROSSOVER_EVENT_ROWS
        if row_key not in RH_CUSTOM_DEFAULT
    ],
]


def _is_scd_crossover_event_row(row_key: str) -> bool:
    """Return True for first-wave SCD crossover event rows."""
    return str(row_key).strip() in SCD_CROSSOVER_EVENT_ROWS


def load_indicator_markdown(doc_slug: str) -> Optional[str]:
    """
    Load family-level educational markdown for an indicator, if available.

    Expected repo location:
        docs/indicators/<doc_slug>.md

    Returns:
        markdown text when the file exists and can be read,
        otherwise None.
    """
    if not doc_slug:
        return None

    doc_path = Path(__file__).parent / "docs" / "indicators" / f"{doc_slug}.md"

    try:
        if not doc_path.exists() or not doc_path.is_file():
            return None
        return doc_path.read_text(encoding="utf-8")
    except Exception:
        return None


def _strip_indicator_definition_markup(value: Any) -> str:
    """
    Return indicator definition text suitable for Streamlit text display.

    Some short definition strings use Plotly hover line-break markup so dense
    hover labels stay readable. The educational expander should show clean
    prose rather than literal hover markup.
    """
    if value is None:
        return ""

    text = str(value).strip()
    if not text:
        return ""

    for marker in ("<br />", "<br/>", "<br>"):
        text = text.replace(marker, " ")

    return " ".join(text.split())


def initialize_session_state():
    """Initialize session state variables"""
    if 'performance_data' not in st.session_state:
        st.session_state.performance_data = None
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None
    if 'performance_request_signature' not in st.session_state:
        st.session_state.performance_request_signature = None
    if 'calculator' not in st.session_state:
        st.session_state.calculator = DatabaseIntegratedPerformanceCalculator()
    if 'volume_calculator' not in st.session_state:
        st.session_state.volume_calculator = DatabaseIntegratedVolumeCalculator()
    if 'technical_calculator' not in st.session_state:
        st.session_state.technical_calculator = DatabaseIntegratedTechnicalCalculator()
    if 'heatmap_generator' not in st.session_state:
        st.session_state.heatmap_generator = FinvizHeatmapGenerator()
    
    # Three-level ticker management session state variables
    if 'selected_country_etfs' not in st.session_state:
        st.session_state.selected_country_etfs = []
    if 'selected_sector_etfs' not in st.session_state:
        st.session_state.selected_sector_etfs = []
    if 'session_custom_tickers' not in st.session_state:
        st.session_state.session_custom_tickers = []
    if 'permanent_country_additions' not in st.session_state:
        st.session_state.permanent_country_additions = []
    if 'permanent_sector_additions' not in st.session_state:
        st.session_state.permanent_sector_additions = []
    
    # Database and performance settings
    if 'save_custom_to_database' not in st.session_state:
        st.session_state.save_custom_to_database = True
    if 'custom_ticker_limit' not in st.session_state:
        st.session_state.custom_ticker_limit = 10

    if 'selected_bucket' not in st.session_state:
        st.session_state.selected_bucket = 'custom'  # Default to custom bucket
    
    # Page selection for navigation
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = 'performance_heatmaps'  # Default to existing heatmaps
    
    # Analysis mode selection
    if 'selected_analysis_mode' not in st.session_state:
        st.session_state.selected_analysis_mode = 'price'  # Default to price performance
    
    # Volume analysis data storage (separate from price performance)
    if 'volume_data' not in st.session_state:
        st.session_state.volume_data = None
    if 'volume_last_update' not in st.session_state:
        st.session_state.volume_last_update = None
    if 'volume_request_signature' not in st.session_state:
        st.session_state.volume_request_signature = None

    # Filtering state (Step 3: Future-ready for additions)
    if 'country_visible_tickers' not in st.session_state:
        st.session_state.country_visible_tickers = []  # Will be populated on first run
    if 'sector_visible_tickers' not in st.session_state:
        st.session_state.sector_visible_tickers = []   # Will be populated on first run
    if 'custom_visible_tickers' not in st.session_state:
        st.session_state.custom_visible_tickers = []   # Will be populated on first run

    # Stock Comparison Dashboard v1 ticker-selection session state.
    # These keys are SCD-specific and must not collide with Performance /
    # Volume ticker controls or Rolling Heatmap row-selection state.
    if 'scd_ticker_source' not in st.session_state:
        st.session_state.scd_ticker_source = 'custom'

    if 'scd_selected_country_tickers' not in st.session_state:
        st.session_state.scd_selected_country_tickers = list(SCD_DEFAULT_COUNTRY_TICKERS)

    if 'scd_selected_sector_tickers' not in st.session_state:
        st.session_state.scd_selected_sector_tickers = list(SCD_DEFAULT_SECTOR_TICKERS)

    if 'scd_selected_custom_tickers' not in st.session_state:
        st.session_state.scd_selected_custom_tickers = list(SCD_DEFAULT_CUSTOM_TICKERS)

    if 'scd_temp_tickers' not in st.session_state:
        st.session_state.scd_temp_tickers = []

    if 'scd_ticker_limit' not in st.session_state:
        st.session_state.scd_ticker_limit = 10

    # Stock Comparison Dashboard analysis-mode routing.
    # Multiple Indicators preserves the existing SCD cross-sectional matrix.
    # Single Indicator is the planned time-series view route.
    if 'scd_analysis_mode' not in st.session_state:
        st.session_state.scd_analysis_mode = 'Single Indicator'

    # Stock Comparison Dashboard Single Indicator selector state.
    # These controls select one canonical Rolling Heatmap row_key for the
    # planned dates × tickers time-series view. They do not build data yet.
    if 'scd_single_indicator_source' not in st.session_state:
        st.session_state.scd_single_indicator_source = 'Main Indicators'

    if 'scd_single_indicator_family' not in st.session_state:
        st.session_state.scd_single_indicator_family = 'RSI'

    if 'scd_single_indicator_row_key' not in st.session_state:
        st.session_state.scd_single_indicator_row_key = 'RSI_14'

    # Stock Comparison Dashboard Single Indicator selector state.
    # These controls select one canonical Rolling Heatmap row_key for the
    # planned dates × tickers time-series view. They do not build data yet.
    if 'scd_single_indicator_source' not in st.session_state:
        st.session_state.scd_single_indicator_source = 'Main Indicators'

    if 'scd_single_indicator_family' not in st.session_state:
        st.session_state.scd_single_indicator_family = 'RSI'

    if 'scd_single_indicator_row_key' not in st.session_state:
        st.session_state.scd_single_indicator_row_key = 'RSI_14'

    # Stock Comparison Dashboard Single Indicator date-window state.
    # These controls resolve a visible trading-day window only. They do not
    # fetch data, build matrices, or change cache/acquisition behavior yet.
    if 'scd_single_trading_days' not in st.session_state:
        st.session_state.scd_single_trading_days = 20

    if 'scd_single_anchor_mode' not in st.session_state:
        st.session_state.scd_single_anchor_mode = 'End date'

    if 'scd_single_use_anchor_date' not in st.session_state:
        st.session_state.scd_single_use_anchor_date = True
        #st.session_state.scd_single_use_anchor_date = False

    if 'scd_single_anchor_date' not in st.session_state:
        st.session_state.scd_single_anchor_date = datetime.now().date()        

    # Stock Comparison Dashboard v1 indicator-selection session state.
    # These keys are SCD-specific but resolve through the existing Rolling
    # Heatmap row-selection resolver and catalog.
    if 'scd_selection_mode' not in st.session_state:
        st.session_state.scd_selection_mode = 'Custom'

    if 'scd_custom_rows' not in st.session_state:
        st.session_state.scd_custom_rows = list(SCD_MULTIPLE_INDICATOR_CUSTOM_DEFAULT)

    if 'scd_selected_category' not in st.session_state:
        st.session_state.scd_selected_category = None

    if 'scd_selected_scope' not in st.session_state:
        st.session_state.scd_selected_scope = 'All'

    if 'scd_selected_window' not in st.session_state:
        st.session_state.scd_selected_window = 'All'

    if 'scd_selected_family' not in st.session_state:
        st.session_state.scd_selected_family = 'All'

    if 'scd_selected_tag' not in st.session_state:
        tag_names = get_tag_names()
        st.session_state.scd_selected_tag = tag_names[0] if tag_names else None

    if 'scd_selected_preset' not in st.session_state:
        preset_names = get_preset_names()
        st.session_state.scd_selected_preset = preset_names[0] if preset_names else None

    if 'scd_last_resolved_row_keys' not in st.session_state:
        st.session_state.scd_last_resolved_row_keys = []

    # Stock Comparison Dashboard v1 matrix transport state.
    # This stores reshaped existing Rolling Heatmap cells only.
    # It must not store new scores, rankings, aggregates, or semantic labels.
    if 'scd_signal_matrix' not in st.session_state:
        st.session_state.scd_signal_matrix = None

    if 'scd_matrix_last_run' not in st.session_state:
        st.session_state.scd_matrix_last_run = None

    # Stock Comparison Dashboard Single Indicator matrix transport state.
    # This stores reshaped existing Rolling Heatmap cells only, but oriented
    # as dates × tickers for one selected indicator.
    if 'scd_single_indicator_matrix_last_run' not in st.session_state:
        st.session_state.scd_single_indicator_matrix_last_run = None

    # Stock Comparison Dashboard Single Indicator chart display state.
    # These controls affect only the chart layer. They must not remove data
    # from the matrix, heatmap, detail table, export, cache, or payload.
    if 'scd_single_chart_value_mode' not in st.session_state:
        st.session_state.scd_single_chart_value_mode = 'Auto'

    if 'scd_single_chart_visible_tickers' not in st.session_state:
        st.session_state.scd_single_chart_visible_tickers = []

    # Stock Comparison Dashboard Single Indicator Price Trend Chart state.
    # This is an independent display transform over matrix-owned Price cells.
    # It must not trigger acquisition, adapter, cache, or calculation work.
    if 'scd_single_price_chart_value_mode' not in st.session_state:
        st.session_state.scd_single_price_chart_value_mode = 'Indexed to 100'

    # Stock Comparison Dashboard v1: Date-anchor controls
    # These are display/request controls only. They do not create a new
    # acquisition path, scoring path, or persistence behavior.
    if 'scd_use_anchor_date' not in st.session_state:
        st.session_state.scd_use_anchor_date = False

    if 'scd_anchor_date' not in st.session_state:
        st.session_state.scd_anchor_date = datetime.now().date()

    # Stock Comparison Dashboard v1: Session Cache.
    # Session-only transport cache for expensive per-ticker SCD payloads.
    # This must not introduce DB persistence, new acquisition behavior, ranking,
    # aggregation, or semantic reinterpretation.
    if 'scd_payload_cache' not in st.session_state:
        st.session_state.scd_payload_cache = {}

    # Session-only freshness metadata for scd_payload_cache entries.
    # This is display metadata only, used to distinguish live data freshness
    # from the time a cached matrix was re-rendered.
    if 'scd_payload_cache_meta' not in st.session_state:
        st.session_state.scd_payload_cache_meta = {}

    if 'scd_hover_ohlcv_cache' not in st.session_state:
        st.session_state.scd_hover_ohlcv_cache = {}

    # WS11-G: coverage-aware bundle metadata cache.
    # Write-only in WS11-G-A/B. Later WS11-G steps may read this to reuse
    # completed historical coverage across overlapping SCD requests.
    if 'scd_bundle_coverage_cache' not in st.session_state:
        st.session_state.scd_bundle_coverage_cache = {}

    # D3-A: completed historical result-cell cache.
    # Session-only store of final SCD matrix cells keyed by
    # (ticker, row_key, date). Commit 1 writes completed cells only; later
    # D3-A steps may read this to avoid recalculating completed historical cells.
    if 'scd_result_cell_cache' not in st.session_state:
        st.session_state.scd_result_cell_cache = {}

    if 'scd_cache_stats' not in st.session_state:
        st.session_state.scd_cache_stats = {
            "rolling_hits": 0,
            "rolling_misses": 0,
            "hover_hits": 0,
            "hover_misses": 0,
            "force_refreshes": 0,
            "clears": 0,
            "coverage_writes": 0,
            "coverage_hits": 0,
            "today_cell_refreshes": 0,
            "today_cell_tickers_refreshed": 0,
            "result_cell_writes": 0,
            "result_cell_hits": 0,
            "result_cell_misses": 0,
            "ticker_calculations_skipped": 0,
            "selected_row_refreshes": 0,
            "selected_row_refresh_tickers": 0,
            "selected_row_refresh_fallbacks": 0,
            "selected_row_refresh_errors": 0,
        }

    # Rolling Heatmap Selection & Catalog session state.
    # These keys support the Phase III row-selection architecture only.
    # They do not define numeric truth, semantic truth, display metadata,
    # or rolling payload contents.
    if 'rh_selection_mode' not in st.session_state:
        st.session_state.rh_selection_mode = 'Custom'

    if 'rh_custom_rows' not in st.session_state:
        st.session_state.rh_custom_rows = list(RH_CUSTOM_DEFAULT)

    if 'rh_selected_category' not in st.session_state:
        st.session_state.rh_selected_category = None

    if 'rh_selected_scope' not in st.session_state:
        st.session_state.rh_selected_scope = 'All'

    if 'rh_selected_window' not in st.session_state:
        st.session_state.rh_selected_window = 'All'

    if 'rh_selected_family' not in st.session_state:
        st.session_state.rh_selected_family = 'All'

    if 'rh_selected_tag' not in st.session_state:
        tag_names = get_tag_names()
        st.session_state.rh_selected_tag = tag_names[0] if tag_names else None

    if 'rh_selected_preset' not in st.session_state:
        preset_names = get_preset_names()
        st.session_state.rh_selected_preset = preset_names[0] if preset_names else None

    if 'rh_last_resolved_base_keys' not in st.session_state:
        st.session_state.rh_last_resolved_base_keys = []

def is_bucket_ticker(ticker: str) -> bool:
    """
    Check if ticker exists in any of the three buckets (COUNTRY/SECTOR/CUSTOM)
    
    Args:
        ticker: Stock ticker symbol (uppercase)
        
    Returns:
        True if ticker is in any bucket, False otherwise
    """
    # Get all bucket tickers
    all_bucket_tickers = []
    
    # COUNTRY_ETFS
    for item in ASSET_GROUPS.get('country', []):
        if isinstance(item, tuple):
            all_bucket_tickers.append(item[0])  # (ticker, display_name)
        else:
            all_bucket_tickers.append(item)     # Just ticker
    
    # SECTOR_ETFS
    for item in ASSET_GROUPS.get('sector', []):
        if isinstance(item, tuple):
            all_bucket_tickers.append(item[0])
        else:
            all_bucket_tickers.append(item)
    
    # CUSTOM_DEFAULT
    for item in CUSTOM_DEFAULT:
        if isinstance(item, tuple):
            all_bucket_tickers.append(item[0])
        else:
            all_bucket_tickers.append(item)
    
    return ticker.upper() in [t.upper() for t in all_bucket_tickers]


def _format_scd_ticker_label(ticker: str, ticker_names: Dict[str, str]) -> str:
    """Return a display label while preserving ticker as the canonical identity."""
    display_name = ticker_names.get(ticker, ticker)
    if display_name and display_name != ticker:
        return f"{display_name} ({ticker})"
    return ticker


def _get_scd_source_config(source: str) -> Dict[str, Any]:
    """
    Return existing asset-universe metadata for an SCD ticker source.

    SCD consumes the existing ASSET_GROUPS universes. It does not create a new
    asset universe or reorder canonical ticker lists.
    """
    source_key = source if source in {"country", "sector", "custom"} else "custom"
    group = ASSET_GROUPS.get(source_key, {})

    return {
        "source": source_key,
        "name": group.get("name", source_key.title()),
        "tickers": list(group.get("tickers", [])),
        "ticker_names": dict(group.get("ticker_names", {})),
    }


def _get_scd_selected_ticker_state_key(source: str) -> str:
    """Return the SCD session-state key for the selected source."""
    if source == "country":
        return "scd_selected_country_tickers"
    if source == "sector":
        return "scd_selected_sector_tickers"
    return "scd_selected_custom_tickers"


def _dedupe_preserve_order_str(values) -> list[str]:
    """Return uppercase non-empty strings with duplicates removed."""
    seen = set()
    out = []

    for value in values:
        ticker = str(value).strip().upper()
        if not ticker or ticker in seen:
            continue
        seen.add(ticker)
        out.append(ticker)

    return out


def _get_scd_selected_tickers() -> list[str]:
    """
    Return the current SCD selected ticker set.

    This is ticker-symbol identity only. Display names remain presentation
    metadata and must not replace ticker symbols.
    """
    source = st.session_state.get("scd_ticker_source", "custom")
    selected_key = _get_scd_selected_ticker_state_key(source)

    selected = list(st.session_state.get(selected_key, []))
    temp_tickers = list(st.session_state.get("scd_temp_tickers", []))

    selected_tickers = _dedupe_preserve_order_str(selected + temp_tickers)
    ticker_limit = int(st.session_state.get("scd_ticker_limit", 10))

    return selected_tickers[:ticker_limit]


def _format_scd_indicator_display_label(row_key: str) -> str:
    """
    Return a user-facing indicator label while preserving row_key identity.

    Examples:
        RSI_14 -> RSI(14)
        MACD_12_26_9 -> MACD(12,26,9)
        SMA_50 -> SMA(50)
    """
    row_key = str(row_key).strip()

    display_name = INDICATOR_DEFS.get(row_key, {}).get("display_name")
    if display_name:
        # Normalize existing labels such as "RSI (14)" to "RSI(14)".
        return display_name.replace(" (", "(").strip()

    parts = row_key.split("_")
    if len(parts) <= 1:
        return row_key

    family = parts[0]
    params = ",".join(parts[1:])

    family_display = {
        "STOCH": "Stoch",
        "WILLR": "Williams %R",
        "UO": "UO",
        "BB": "BB",
    }.get(family, family)

    return f"{family_display}({params})"


def _get_scd_single_indicator_main_rows() -> list[str]:
    """
    Return quick-access Single Indicator candidates.

    Main Indicators start from the existing Rolling Heatmap Custom default
    membership, then add SCD-specific Single Indicator extras. This keeps the
    global Rolling Heatmap Custom default unchanged while exposing the selected
    first-wave crossover row in SCD Single Indicator.
    """
    rows = [
        *RH_CUSTOM_DEFAULT,
        *[
            row_key
            for row_key in SCD_SINGLE_INDICATOR_MAIN_EXTRA_ROWS
            if row_key not in RH_CUSTOM_DEFAULT
        ],
    ]

    return [
        row_key
        for row_key in rows
        if row_key in ROW_CLASSIFICATION
    ]


def _get_scd_single_indicator_available_rows() -> list[str]:
    """
    Return catalog-backed Single Indicator candidates.

    v1 intentionally uses known Rolling Heatmap row keys and excludes Price.
    """
    return [
        row_key
        for row_key in ROW_CLASSIFICATION.keys()
        if row_key in INDICATOR_DEFS
    ]


def _get_scd_single_indicator_family_options(row_keys: list[str]) -> list[str]:
    """Return sorted family names available for the provided row keys."""
    families = sorted(
        {
            ROW_CLASSIFICATION[row_key].get("family", "")
            for row_key in row_keys
            if row_key in ROW_CLASSIFICATION
        }
    )
    return [family for family in families if family]


def _render_scd_single_indicator_controls() -> str | None:
    """
    Render selector controls for the planned SCD Single Indicator time-series view.

    This returns one canonical row_key. It does not build time-series data.
    """
    st.subheader("Single Indicator")

    source_options = ["Main Indicators", "Available Indicators"]
    current_source = st.session_state.get(
        "scd_single_indicator_source",
        "Main Indicators",
    )
    if current_source not in source_options:
        current_source = "Main Indicators"

    selected_source = st.selectbox(
        "Indicator Source",
        options=source_options,
        index=source_options.index(current_source),
        key="scd_single_indicator_source_widget",
        help=(
            "Main Indicators are derived from the current Custom default row set. "
            "Available Indicators are drawn from the Rolling Heatmap row catalog."
        ),
    )
    st.session_state.scd_single_indicator_source = selected_source

    if selected_source == "Main Indicators":
        candidate_rows = _get_scd_single_indicator_main_rows()
    else:
        candidate_rows = _get_scd_single_indicator_available_rows()

    if not candidate_rows:
        st.warning("No Single Indicator candidates are available.")
        st.session_state.scd_single_indicator_row_key = None
        return None

    family_options = _get_scd_single_indicator_family_options(candidate_rows)

    current_family = st.session_state.get(
        "scd_single_indicator_family",
        "RSI",
    )
    if current_family not in family_options:
        current_family = family_options[0] if family_options else None

    if selected_source == "Available Indicators" and family_options:
        selected_family = st.selectbox(
            "Indicator Family",
            options=family_options,
            index=family_options.index(current_family),
            key="scd_single_indicator_family_widget",
            help="Choose an indicator family, then select one parameter setting.",
        )
        st.session_state.scd_single_indicator_family = selected_family

        candidate_rows = [
            row_key
            for row_key in candidate_rows
            if ROW_CLASSIFICATION.get(row_key, {}).get("family") == selected_family
        ]
    else:
        selected_family = ROW_CLASSIFICATION.get(
            st.session_state.get("scd_single_indicator_row_key", "RSI_14"),
            {},
        ).get("family", "RSI")
        st.session_state.scd_single_indicator_family = selected_family

    current_row_key = st.session_state.get(
        "scd_single_indicator_row_key",
        "RSI_14",
    )
    if current_row_key not in candidate_rows:
        if "RSI_14" in candidate_rows:
            current_row_key = "RSI_14"
        else:
            current_row_key = candidate_rows[0]

    selected_row_key = st.selectbox(
        "Indicator",
        options=candidate_rows,
        index=candidate_rows.index(current_row_key),
        key="scd_single_indicator_row_key_widget",
        format_func=_format_scd_indicator_display_label,
        help="Select one indicator row for the planned dates × tickers view.",
    )

    st.session_state.scd_single_indicator_row_key = selected_row_key

    selected_label = _format_scd_indicator_display_label(selected_row_key)
    selected_family = ROW_CLASSIFICATION.get(selected_row_key, {}).get("family", "Unknown")

    st.success(f"Selected indicator: {selected_label}")
    st.caption(f"Canonical row key: {selected_row_key} | Family: {selected_family}")

    return selected_row_key


def _coerce_scd_date_to_datetime(value: Any) -> datetime:
    """Return a normalized naive datetime for an SCD date-control value."""
    try:
        ts = pd.Timestamp(value)
        if ts.tzinfo is not None:
            ts = ts.tz_localize(None)
        return ts.normalize().to_pydatetime()
    except Exception:
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def _get_next_n_trading_days_for_scd(start_date: datetime, n: int) -> list[datetime]:
    """Return n trading days starting at or after start_date."""
    trading_days: list[datetime] = []
    cursor = _coerce_scd_date_to_datetime(start_date)

    while len(trading_days) < int(n):
        if is_us_trading_day(cursor):
            trading_days.append(cursor)
        cursor += timedelta(days=1)

    return trading_days


def _resolve_scd_single_indicator_date_window(
    *,
    trading_days: int,
    anchor_mode: str,
    use_anchor_date: bool,
    anchor_date: Any,
) -> Dict[str, Any]:
    """
    Resolve the Single Indicator visible trading-day window.

    This is a UI/request helper only. It does not fetch data, build a matrix,
    change cache identity, or alter acquisition behavior.
    """
    trading_days = int(trading_days)

    if use_anchor_date and anchor_date is not None:
        effective_anchor = _coerce_scd_date_to_datetime(anchor_date)
    else:
        effective_anchor = _coerce_scd_date_to_datetime(get_last_completed_trading_day())

    if anchor_mode == "Start date":
        window_dates = _get_next_n_trading_days_for_scd(effective_anchor, trading_days)
        scenario_b_anchor_mode = "start"
    else:
        # Default behavior: visible window ends on the anchor date.
        window_dates = get_last_n_trading_days(effective_anchor, trading_days)
        scenario_b_anchor_mode = "asof"

    date_strings = [
        pd.Timestamp(day).strftime("%Y-%m-%d")
        for day in window_dates
    ]

    window_start = date_strings[0] if date_strings else None
    window_end = date_strings[-1] if date_strings else None

    return {
        "trading_days": trading_days,
        "anchor_mode": anchor_mode,
        "scenario_b_anchor_mode": scenario_b_anchor_mode,
        "use_anchor_date": bool(use_anchor_date),
        "anchor_date": pd.Timestamp(effective_anchor).date(),
        "window_start_date": window_start,
        "window_end_date": window_end,
        "date_strings": date_strings,
    }


def _render_scd_single_indicator_date_controls() -> Dict[str, Any]:
    """
    Render date-window controls for the planned Single Indicator time-series view.

    Returns resolved request metadata only. It does not build the matrix yet.
    """
    st.subheader("Date Window")

    trading_day_options = [10, 20, 30, 40]
    current_trading_days = int(
        st.session_state.get("scd_single_trading_days", 20)
    )
    if current_trading_days not in trading_day_options:
        current_trading_days = 20

    d1, d2 = st.columns(2)

    with d1:
        selected_trading_days = st.selectbox(
            "# of Trading days",
            options=trading_day_options,
            index=trading_day_options.index(current_trading_days),
            key="scd_single_trading_days_widget",
            help="Number of visible trading days for the Single Indicator view.",
        )
        st.session_state.scd_single_trading_days = int(selected_trading_days)

    anchor_mode_options = ["End date", "Start date"]
    current_anchor_mode = st.session_state.get(
        "scd_single_anchor_mode",
        "End date",
    )
    if current_anchor_mode not in anchor_mode_options:
        current_anchor_mode = "End date"

    with d2:
        selected_anchor_mode = st.selectbox(
            "Anchor mode",
            options=anchor_mode_options,
            index=anchor_mode_options.index(current_anchor_mode),
            key="scd_single_anchor_mode_widget",
            help=(
                "End date shows the selected number of trading days ending on the anchor. "
                "Start date shows the selected number of trading days starting from the anchor."
            ),
        )
        st.session_state.scd_single_anchor_mode = selected_anchor_mode

    use_anchor_date = st.checkbox(
        "Use anchor date",
        value=bool(st.session_state.get("scd_single_use_anchor_date", False)),
        key="scd_single_use_anchor_date_widget",
        help="When unchecked, the view uses the latest completed trading day.",
    )
    st.session_state.scd_single_use_anchor_date = bool(use_anchor_date)

    if use_anchor_date:
        selected_anchor_date = st.date_input(
            "Anchor date",
            value=st.session_state.get(
                "scd_single_anchor_date",
                datetime.now().date(),
            ),
            key="scd_single_anchor_date_widget",
            help="Weekend/holiday dates resolve to the nearest valid trading-day window.",
        )
        st.session_state.scd_single_anchor_date = selected_anchor_date
    else:
        selected_anchor_date = None

    date_request = _resolve_scd_single_indicator_date_window(
        trading_days=int(selected_trading_days),
        anchor_mode=selected_anchor_mode,
        use_anchor_date=bool(use_anchor_date),
        anchor_date=selected_anchor_date,
    )

    st.caption(
        "Resolved window: "
        f"{date_request['window_start_date']} → {date_request['window_end_date']} "
        f"({date_request['trading_days']} trading days)"
    )

    st.caption(
        "Request mode: "
        f"{date_request['scenario_b_anchor_mode']} | "
        f"Anchor date: {date_request['anchor_date']}"
    )

    return date_request


def _render_scd_ticker_controls() -> list[str]:
    """
    Render SCD-specific ticker controls in the sidebar.

    These controls intentionally mirror the Performance / Volume checkbox
    interaction pattern while using SCD-only session-state keys.
    """
    source_options = ["country", "sector", "custom"]
    source_labels = {
        "country": "🌍 Country ETFs",
        "sector": "🏭 Sector ETFs",
        "custom": "🎯 Custom Stocks",
    }

    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Stock Comparison Tickers")

    current_source = st.session_state.get("scd_ticker_source", "custom")
    if current_source not in source_options:
        current_source = "custom"

    selected_source = st.sidebar.radio(
        "Ticker Source",
        options=source_options,
        format_func=lambda source: source_labels[source],
        index=source_options.index(current_source),
        key="scd_ticker_source_widget",
    )

    # Keep canonical SCD source state separate from widget state.
    # This avoids stale source behavior when switching Country / Sector / Custom.
    st.session_state.scd_ticker_source = selected_source

    source_config = _get_scd_source_config(selected_source)
    available_tickers = source_config["tickers"]
    ticker_names = source_config["ticker_names"]
    selected_key = _get_scd_selected_ticker_state_key(selected_source)

    current_selected = [
        ticker for ticker in st.session_state.get(selected_key, [])
        if ticker in available_tickers
    ]
    st.session_state[selected_key] = current_selected

    ticker_limit = st.sidebar.number_input(
        "Selected ticker cap (max 10)",
        min_value=1,
        max_value=50,
        value=int(st.session_state.get("scd_ticker_limit", 10)),
        step=1,
        key="scd_ticker_limit",
        help="SCD v1 defaults to 10 selected tickers. Higher values may slow later payload execution.",
    )

    with st.sidebar.expander(f"📋 Show/Hide {source_config['name']}", expanded=True):
        col_select, col_clear = st.columns(2)

        with col_select:
            if st.button("Select Defaults", key=f"scd_select_defaults_{selected_source}"):
                if selected_source == "country":
                    st.session_state[selected_key] = [
                        ticker for ticker in SCD_DEFAULT_COUNTRY_TICKERS
                        if ticker in available_tickers
                    ]
                elif selected_source == "sector":
                    st.session_state[selected_key] = [
                        ticker for ticker in SCD_DEFAULT_SECTOR_TICKERS
                        if ticker in available_tickers
                    ]
                else:
                    st.session_state[selected_key] = [
                        ticker for ticker in SCD_DEFAULT_CUSTOM_TICKERS
                        if ticker in available_tickers
                    ]
                st.rerun()

        with col_clear:
            if st.button("Clear", key=f"scd_clear_source_{selected_source}"):
                st.session_state[selected_key] = []
                st.rerun()

        for ticker in available_tickers:
            is_selected = ticker in st.session_state[selected_key]
            label = _format_scd_ticker_label(ticker, ticker_names)

            if st.checkbox(
                label,
                value=is_selected,
                key=f"scd_filter_{selected_source}_{ticker}",
            ):
                if ticker not in st.session_state[selected_key]:
                    st.session_state[selected_key].append(ticker)
            else:
                if ticker in st.session_state[selected_key]:
                    st.session_state[selected_key].remove(ticker)

        st.caption(
            f"Selected from source: {len(st.session_state[selected_key])}/"
            f"{len(available_tickers)}"
        )

    with st.sidebar.expander("➕ Add Temporary SCD Tickers", expanded=False):
        temp_input = st.text_area(
            "Add temporary ticker(s):",
            key="scd_temp_ticker_input",
            placeholder="Single: TSLA\nMultiple: AAPL, MSFT, GOOGL\n(comma or line separated)",
            height=80,
            help="Temporary SCD tickers apply only to this dashboard view.",
        )

        if st.button("Add Temporary Ticker(s)", key="scd_add_temp_tickers"):
            parsed_tickers = _dedupe_preserve_order_str(
                temp_input.replace(",", "\n").split("\n")
            )
            existing = _dedupe_preserve_order_str(st.session_state.scd_temp_tickers)
            st.session_state.scd_temp_tickers = _dedupe_preserve_order_str(
                existing + parsed_tickers
            )

            if parsed_tickers:
                st.success(f"Added {len(parsed_tickers)} temporary ticker(s).")
            else:
                st.warning("Enter at least one ticker symbol.")

        if st.session_state.scd_temp_tickers:
            st.caption(
                "Temporary tickers: "
                + ", ".join(_dedupe_preserve_order_str(st.session_state.scd_temp_tickers))
            )

            tickers_to_remove = []
            for ticker in _dedupe_preserve_order_str(st.session_state.scd_temp_tickers):
                remove_col, label_col = st.columns([1, 4])
                with remove_col:
                    if st.button("❌", key=f"scd_remove_temp_{ticker}", help=f"Remove {ticker}"):
                        tickers_to_remove.append(ticker)
                with label_col:
                    st.write(ticker)

            for ticker in tickers_to_remove:
                st.session_state.scd_temp_tickers = [
                    existing
                    for existing in st.session_state.scd_temp_tickers
                    if existing != ticker
                ]
                st.rerun()

            if st.button("Clear Temporary Tickers", key="scd_clear_temp_tickers"):
                st.session_state.scd_temp_tickers = []
                st.rerun()

    selected_tickers = _get_scd_selected_tickers()

    if len(st.session_state[selected_key]) + len(st.session_state.scd_temp_tickers) > ticker_limit:
        st.sidebar.warning(
            f"Ticker cap is {ticker_limit}. Only the first {ticker_limit} selected "
            f"ticker(s), including temporary tickers, will be used."
        )

    st.sidebar.success(f"Selected for SCD: {len(selected_tickers)} ticker(s)")
    st.sidebar.caption(
        ", ".join(selected_tickers) if selected_tickers else "No tickers selected."
    )

    return selected_tickers

def _render_scd_indicator_selection_controls() -> list[str]:
    """
    Render SCD-specific indicator row-selection controls.

    SCD does not own indicator grouping metadata. This function only renders
    SCD-specific controls and delegates row-key resolution to the existing
    Rolling Heatmap selection resolver.
    """
    st.subheader("Indicator Selection")

    mode_options = get_selection_modes()
    if not mode_options:
        mode_options = ["Custom", "Category", "Preset", "Tag"]

    current_mode = st.session_state.get("scd_selection_mode", "Custom")
    if current_mode not in mode_options:
        current_mode = "Custom"

    selection_mode = st.selectbox(
        "Selection Mode",
        options=mode_options,
        index=mode_options.index(current_mode),
        key="scd_selection_mode",
        help="Choose the base indicator row set for the Stock Comparison Dashboard.",
    )

    resolved_row_keys: list[str] = []

    if selection_mode == "Custom":
        cc1, cc2 = st.columns([0.75, 0.25])
        with cc1:
            st.caption(
                "Custom mode uses the SCD session row set. Restore-default "
                "resets to the SCD Multiple Indicators Custom default."
            )
        with cc2:
            if st.button(
                "Restore Default Custom",
                key="scd_restore_default_custom_rows",
                use_container_width=True,
            ):
                st.session_state.scd_custom_rows = list(SCD_MULTIPLE_INDICATOR_CUSTOM_DEFAULT)
                st.session_state.pop("scd_custom_selected_row_keys", None)
                st.rerun()

        resolved_row_keys = resolve_row_selection(
            selection_mode="Custom",
            custom_rows=st.session_state.get(
                "scd_custom_rows",
                list(SCD_MULTIPLE_INDICATOR_CUSTOM_DEFAULT),
            ),
        )

        multiselect_key = "scd_custom_selected_row_keys"

    elif selection_mode == "Preset":
        preset_options = get_preset_names()

        if not preset_options:
            st.warning("No Rolling Heatmap presets are available.")
            selected_preset = None
            resolved_row_keys = []
            multiselect_key = "scd_preset_selected_row_keys__none"
        else:
            stored_preset = st.session_state.get("scd_selected_preset")
            if stored_preset not in preset_options:
                st.session_state.scd_selected_preset = preset_options[0]
                stored_preset = preset_options[0]

            selected_preset = st.selectbox(
                "Choose a preset",
                options=preset_options,
                index=preset_options.index(stored_preset),
                key="scd_selected_preset",
                help="Presets are resolved by the existing Rolling Heatmap selection catalog.",
            )

            resolved_row_keys = resolve_row_selection(
                selection_mode="Preset",
                preset_name=selected_preset,
            )

            preset_key_part = str(selected_preset).replace(" ", "_").replace("/", "_")
            multiselect_key = f"scd_preset_selected_row_keys__{preset_key_part}"

    elif selection_mode == "Category":
        category_options = get_category_names()

        if not category_options:
            st.warning("No row categories are available.")
            selected_category = None
            selected_scope = "All"
            selected_window = "All"
            selected_family = "All"
            resolved_row_keys = []
            multiselect_key = "scd_category_selected_row_keys__none"
        else:
            stored_category = st.session_state.get("scd_selected_category")
            if stored_category not in category_options:
                st.session_state.scd_selected_category = category_options[0]
                stored_category = category_options[0]

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                selected_category = st.selectbox(
                    "Category",
                    options=category_options,
                    index=category_options.index(stored_category),
                    key="scd_selected_category",
                )

            # Defensive local normalization for Streamlit rerun edges:
            # when switching categories, the widget/session-state handoff
            # can briefly yield a non-resolvable category value. The resolver
            # requires a concrete category, so fall back locally without
            # mutating the widget key after instantiation.
            if selected_category not in category_options:
                selected_category = stored_category

            if selected_category not in category_options:
                selected_category = category_options[0]

            scope_options = ["All"] + get_scope_names(category=selected_category)
            stored_scope = st.session_state.get("scd_selected_scope", "All")
            if stored_scope not in scope_options:
                stored_scope = "All"

            with c2:
                selected_scope = st.selectbox(
                    "Scope",
                    options=scope_options,
                    index=scope_options.index(stored_scope),
                    key="scd_selected_scope",
                )

            window_options = ["All"] + get_window_names(category=selected_category)
            stored_window = st.session_state.get("scd_selected_window", "All")
            if stored_window not in window_options:
                stored_window = "All"

            with c3:
                selected_window = st.selectbox(
                    "Window",
                    options=window_options,
                    index=window_options.index(stored_window),
                    key="scd_selected_window",
                )

            family_options = ["All"] + get_family_names(category=selected_category)
            stored_family = st.session_state.get("scd_selected_family", "All")
            if stored_family not in family_options:
                stored_family = "All"

            with c4:
                selected_family = st.selectbox(
                    "Family",
                    options=family_options,
                    index=family_options.index(stored_family),
                    key="scd_selected_family",
                )

            resolved_row_keys = resolve_row_selection(
                selection_mode="Category",
                category=selected_category,
                scope=selected_scope,
                window=selected_window,
                family=selected_family,
            )

            category_key_part = str(selected_category).replace(" ", "_").replace("/", "_")
            scope_key_part = str(selected_scope).replace(" ", "_").replace("/", "_")
            window_key_part = str(selected_window).replace(" ", "_").replace("/", "_")
            family_key_part = str(selected_family).replace(" ", "_").replace("/", "_")
            multiselect_key = (
                "scd_category_selected_row_keys__"
                f"{category_key_part}__{scope_key_part}__"
                f"{window_key_part}__{family_key_part}"
            )

    elif selection_mode == "Tag":
        tag_options = get_tag_names()

        if not tag_options:
            st.warning("No Rolling Heatmap tags are available.")
            selected_tag = None
            resolved_row_keys = []
            multiselect_key = "scd_tag_selected_row_keys__none"
        else:
            stored_tag = st.session_state.get("scd_selected_tag")
            if stored_tag not in tag_options:
                st.session_state.scd_selected_tag = tag_options[0]
                stored_tag = tag_options[0]

            selected_tag = st.selectbox(
                "Tag",
                options=tag_options,
                index=tag_options.index(stored_tag),
                key="scd_selected_tag",
                help=(
                    "Tags are cross-category secondary descriptors from the "
                    "Rolling Heatmap classification catalog."
                ),
            )

            resolved_row_keys = resolve_row_selection(
                selection_mode="Tag",
                tag=selected_tag,
            )

            tag_key_part = (
                str(selected_tag)
                .replace(" ", "_")
                .replace("/", "_")
                .replace(":", "_")
            )
            multiselect_key = (
                f"scd_tag_selected_row_keys__{tag_key_part}"
            )

    else:
        st.warning(f"Unsupported SCD selection mode: {selection_mode!r}")
        resolved_row_keys = []
        multiselect_key = "scd_selected_row_keys__unsupported"

    resolved_row_keys = list(resolved_row_keys)

    if not resolved_row_keys:
        empty_message = describe_empty_selection(
            selection_mode=selection_mode,
            category=st.session_state.get("scd_selected_category"),
            scope=st.session_state.get("scd_selected_scope"),
            window=st.session_state.get("scd_selected_window"),
            family=st.session_state.get("scd_selected_family"),
            tag=st.session_state.get("scd_selected_tag"),
            preset_name=st.session_state.get("scd_selected_preset"),
        )
        st.info(empty_message)
        st.session_state.scd_last_resolved_row_keys = []
        return []

    # Build a local default without mutating the widget's Session State key
    # before instantiating the widget. Mutating st.session_state[multiselect_key]
    # here while also passing default=... causes Streamlit's default/session-state warning.
    widget_default = [
        row_key
        for row_key in st.session_state.get(multiselect_key, resolved_row_keys)
        if row_key in resolved_row_keys
    ]

    selected_row_keys = st.multiselect(
        "Indicator rows",
        options=resolved_row_keys,
        default=widget_default,
        key=multiselect_key,
        help=(
            "These are canonical Rolling Heatmap row_key values. "
            "The final SCD matrix will use these row keys as indicator rows."
        ),
    )

    selected_row_keys = list(selected_row_keys)

    if selection_mode == "Custom":
        st.session_state.scd_custom_rows = list(selected_row_keys)

    st.session_state.scd_last_resolved_row_keys = list(selected_row_keys)

    st.success(f"Selected for SCD: {len(selected_row_keys)} indicator row(s)")
    st.caption(", ".join(selected_row_keys) if selected_row_keys else "No indicator rows selected.")

    return selected_row_keys

def _resolve_scd_effective_anchor_date(
    *,
    use_anchor_date: bool,
    selected_anchor_date: Optional[Any],
) -> Any:
    """
    Resolve the comparison dashboard snapshot date used for request/cache identity.

    Explicit date mode preserves the user-selected date.

    Latest/default mode resolves to the existing app-wide last completed trading
    day. This prevents the default latest snapshot from being cached under
    anchor_date=None while the same date selected explicitly is cached under a
    concrete date object.
    """
    if use_anchor_date and selected_anchor_date is not None:
        return selected_anchor_date

    latest_completed = get_last_completed_trading_day()

    if isinstance(latest_completed, datetime):
        return latest_completed.date()

    try:
        return pd.Timestamp(latest_completed).date()
    except Exception:
        return latest_completed


def _resolve_scd_cross_sectional_target_date_key(
    anchor_date: Optional[Any],
) -> Optional[str]:
    """
    Resolve the target extraction date for the SCD Multiple Indicators matrix.

    Scenario B treats weekend/holiday anchor dates as as-of requests and moves
    backward to the nearest valid trading day. This helper mirrors that behavior
    for the matrix extraction layer.

    This is extraction-target metadata only. It does not fetch data, mutate
    cache state, compute indicators, score signals, persist data, or alter
    rule semantics.
    """
    if anchor_date is None:
        return None

    try:
        target_date = _coerce_scd_date_to_datetime(anchor_date)
    except Exception:
        return None

    while not is_us_trading_day(target_date):
        target_date -= timedelta(days=1)

    return pd.Timestamp(target_date).strftime("%Y-%m-%d")


def _get_scd_ohlcv_request(
    window_days: int = 10,
    anchor_date: Optional[Any] = None,
    anchor_mode: str = "asof",
    historical_buffer_days: int = 435,
) -> Dict[str, Any]:
    """
    Return the Scenario B-style OHLCV request used by the comparison dashboard.

    Multiple Indicators uses the default as-of semantics. Single Indicator may
    request start-date semantics through the same existing Scenario B path.

    D3-C diagnostics may pass a smaller historical_buffer_days value only for
    equivalence testing against the 435-day reference. Production callers keep
    the default 435-day Scenario B buffer.
    """
    resolved_anchor_mode = str(anchor_mode).strip().lower()
    if resolved_anchor_mode not in {"asof", "start"}:
        resolved_anchor_mode = "asof"

    return {
        "mode": "rolling_heatmap_scenario_b",
        "window_days": int(window_days),
        "anchor_mode": resolved_anchor_mode,
        "anchor_date": anchor_date,
        "historical_buffer_days": int(historical_buffer_days),
    }

def _get_scd_cache_key(
    *,
    ticker: str,
    window_days: int,
    payload_kind: str,
    anchor_date: Optional[Any] = None,
    anchor_mode: str = "asof",
    historical_buffer_days: int = 435,
) -> tuple:
    """
    Return a deterministic comparison dashboard session-cache key.

    Cache identity is based on:
    - payload kind
    - ticker
    - the Scenario B-style OHLCV request signature

    Including anchor_date and anchor_mode in the request signature prevents
    cached data for one window shape from being reused for another.
    """
    request = _get_scd_ohlcv_request(
        window_days=window_days,
        anchor_date=anchor_date,
        anchor_mode=anchor_mode,
        historical_buffer_days=historical_buffer_days,
    )
    request_signature = tuple(
        sorted((str(key), repr(value)) for key, value in request.items())
    )

    return (
        str(payload_kind).strip(),
        str(ticker).strip().upper(),
        request_signature,
    )


def _get_scd_cache_stats() -> Dict[str, int]:
    """Return initialized SCD cache stats."""
    defaults = {
        "rolling_hits": 0,
        "rolling_misses": 0,
        "hover_hits": 0,
        "hover_misses": 0,
        "force_refreshes": 0,
        "clears": 0,
        "coverage_writes": 0,
        "coverage_hits": 0,
        "today_cell_refreshes": 0,
        "today_cell_tickers_refreshed": 0,
        "result_cell_writes": 0,
        "result_cell_hits": 0,
        "result_cell_misses": 0,
        "ticker_calculations_skipped": 0,
        "selected_row_refreshes": 0,
        "selected_row_refresh_tickers": 0,
        "selected_row_refresh_fallbacks": 0,
        "selected_row_refresh_errors": 0,
    }

    if 'scd_cache_stats' not in st.session_state:
        st.session_state.scd_cache_stats = dict(defaults)
    else:
        for key, value in defaults.items():
            st.session_state.scd_cache_stats.setdefault(key, value)

    return st.session_state.scd_cache_stats


def _get_scd_cache_diagnostics_snapshot() -> Dict[str, Any]:
    """
    Return a UI-ready snapshot of SCD session cache diagnostics.

    Diagnostic only. This does not mutate cache state, fetch data, calculate
    indicators, score signals, persist data, or change build behavior.
    """
    cache_stats = dict(_get_scd_cache_stats())
    coverage_cache = st.session_state.get("scd_bundle_coverage_cache", {})

    coverage_entry_count = sum(
        len(entries)
        for entries in coverage_cache.values()
        if isinstance(entries, list)
    )

    return {
        "payload_count": len(st.session_state.get("scd_payload_cache", {})),
        "hover_context_count": len(st.session_state.get("scd_hover_ohlcv_cache", {})),
        "coverage_entry_count": coverage_entry_count,
        "result_cell_count": len(st.session_state.get("scd_result_cell_cache", {})),
        "stats": cache_stats,
    }


def _format_scd_cache_activity_summary(snapshot: Dict[str, Any]) -> str:
    """
    Return a plain-English cache activity summary for the current session.

    Counters are cumulative session diagnostics, not a guaranteed latest-build
    accounting record. This helper intentionally summarizes activity without
    changing the underlying counters.
    """
    stats = snapshot.get("stats", {}) if isinstance(snapshot, dict) else {}

    rolling_hits = int(stats.get("rolling_hits", 0) or 0)
    hover_hits = int(stats.get("hover_hits", 0) or 0)
    coverage_hits = int(stats.get("coverage_hits", 0) or 0)
    rolling_misses = int(stats.get("rolling_misses", 0) or 0)
    hover_misses = int(stats.get("hover_misses", 0) or 0)
    force_refreshes = int(stats.get("force_refreshes", 0) or 0)
    today_cell_refreshes = int(stats.get("today_cell_refreshes", 0) or 0)
    today_cell_tickers_refreshed = int(
        stats.get("today_cell_tickers_refreshed", 0) or 0
    )
    result_cell_writes = int(stats.get("result_cell_writes", 0) or 0)
    result_cell_hits = int(stats.get("result_cell_hits", 0) or 0)
    result_cell_misses = int(stats.get("result_cell_misses", 0) or 0)
    ticker_calculations_skipped = int(
        stats.get("ticker_calculations_skipped", 0) or 0
    )
    selected_row_refreshes = int(stats.get("selected_row_refreshes", 0) or 0)
    selected_row_refresh_tickers = int(
        stats.get("selected_row_refresh_tickers", 0) or 0
    )
    selected_row_refresh_fallbacks = int(
        stats.get("selected_row_refresh_fallbacks", 0) or 0
    )
    selected_row_refresh_errors = int(
        stats.get("selected_row_refresh_errors", 0) or 0
    )

    summary_parts: list[str] = []

    if coverage_hits:
        summary_parts.append(f"coverage reuse={coverage_hits}")

    if rolling_hits or hover_hits:
        summary_parts.append(
            f"exact cache reuse: rolling={rolling_hits}, hover={hover_hits}"
        )

    if rolling_misses or hover_misses:
        summary_parts.append(
            f"fresh calculations: rolling={rolling_misses}, hover={hover_misses}"
        )

    if force_refreshes:
        summary_parts.append(f"force-refresh builds={force_refreshes}")

    if today_cell_refreshes:
        summary_parts.append(
            "today-cell refreshes="
            f"{today_cell_refreshes} "
            f"({today_cell_tickers_refreshed} ticker cell(s))"
        )

    if result_cell_misses:
        summary_parts.append(f"result-cell misses={result_cell_misses}")

    if ticker_calculations_skipped:
        summary_parts.append(
            f"ticker calculations skipped={ticker_calculations_skipped}"
        )

    if selected_row_refreshes:
        summary_parts.append(
            "selected-row refreshes="
            f"{selected_row_refreshes} "
            f"({selected_row_refresh_tickers} ticker cell(s); "
            f"fallbacks={selected_row_refresh_fallbacks}; "
            f"errors={selected_row_refresh_errors})"
        )

    if not summary_parts:
        return "Cache activity summary: no SCD cache activity recorded yet."

    return "Cache activity summary: " + "; ".join(summary_parts) + "."


def _render_scd_cache_diagnostics() -> None:
    """
    Render the shared SCD cache diagnostics UI.

    This centralizes the repeated Single Indicator / Multiple Indicators cache
    counter display. It is presentation-only and must not alter cache state.
    """
    snapshot = _get_scd_cache_diagnostics_snapshot()
    cache_stats = snapshot["stats"]

    st.caption(_format_scd_cache_activity_summary(snapshot))

    st.caption(
        "Counters are session totals and may include automatic builds, "
        "manual rebuilds, and Streamlit reruns."
    )

    st.caption(
        "Current session cache details: "
        f"{snapshot['payload_count']} ticker result(s), "
        f"{snapshot['hover_context_count']} hover-context result(s), "
        f"{snapshot['coverage_entry_count']} coverage-aware bundle entry/entries, "
        f"{snapshot['result_cell_count']} completed result-cell entrie(s). "
        f"Reused: rolling={cache_stats.get('rolling_hits', 0)}, "
        f"hover={cache_stats.get('hover_hits', 0)}, "
        f"coverage={cache_stats.get('coverage_hits', 0)}. "
        f"Calculated: rolling={cache_stats.get('rolling_misses', 0)}, "
        f"hover={cache_stats.get('hover_misses', 0)}. "
        f"Coverage writes={cache_stats.get('coverage_writes', 0)}. "
        f"Result-cell writes={cache_stats.get('result_cell_writes', 0)}. "
        f"Result-cell reuse={cache_stats.get('result_cell_hits', 0)}. "
        f"Result-cell misses={cache_stats.get('result_cell_misses', 0)}. "
        f"Ticker calculations skipped="
        f"{cache_stats.get('ticker_calculations_skipped', 0)}. "
        f"Force-refresh builds={cache_stats.get('force_refreshes', 0)}. "
        f"Today-cell refreshes={cache_stats.get('today_cell_refreshes', 0)}. "
        f"Today refreshed ticker cells="
        f"{cache_stats.get('today_cell_tickers_refreshed', 0)}. "
        f"Selected-row refreshes={cache_stats.get('selected_row_refreshes', 0)}. "
        f"Selected-row refreshed ticker cells="
        f"{cache_stats.get('selected_row_refresh_tickers', 0)}. "
        f"Selected-row fallbacks="
        f"{cache_stats.get('selected_row_refresh_fallbacks', 0)}. "
        f"Selected-row errors="
        f"{cache_stats.get('selected_row_refresh_errors', 0)}."
    )


def _clear_scd_session_cache() -> None:
    """
    Clear SCD session-only transport caches.

    This does not clear the currently rendered matrix. The next build will
    repopulate caches through the existing SCD fetch path.
    """
    st.session_state.scd_payload_cache = {}
    st.session_state.scd_payload_cache_meta = {}
    st.session_state.scd_hover_ohlcv_cache = {}
    st.session_state.scd_bundle_coverage_cache = {}
    st.session_state.scd_result_cell_cache = {}
    st.session_state.scd_cache_stats = {
        "rolling_hits": 0,
        "rolling_misses": 0,
        "hover_hits": 0,
        "hover_misses": 0,
        "force_refreshes": 0,
        "clears": st.session_state.get("scd_cache_stats", {}).get("clears", 0) + 1,
        "coverage_writes": 0,
        "coverage_hits": 0,
        "today_cell_refreshes": 0,
        "today_cell_tickers_refreshed": 0,
        "result_cell_writes": 0,
        "result_cell_hits": 0,
        "result_cell_misses": 0,
        "ticker_calculations_skipped": 0,
        "selected_row_refreshes": 0,
        "selected_row_refresh_tickers": 0,
        "selected_row_refresh_fallbacks": 0,
        "selected_row_refresh_errors": 0,
    }


def _normalize_scd_cache_date_value(value: Any) -> Optional[str]:
    """Normalize a date-like value to YYYY-MM-DD for SCD cache metadata."""
    try:
        ts = pd.Timestamp(value)
        if pd.isna(ts):
            return None
        if ts.tzinfo is not None:
            ts = ts.tz_localize(None)
        return ts.strftime("%Y-%m-%d")
    except Exception:
        return None


def _extract_scd_dates_from_rolling_payload(
    rolling_payload: Optional[Dict[str, Any]],
) -> set[str]:
    """Extract available YYYY-MM-DD dates from an SCD rolling payload."""
    if not isinstance(rolling_payload, dict):
        return set()

    dates = rolling_payload.get("dates", [])
    if not isinstance(dates, list):
        return set()

    return {
        normalized
        for normalized in (
            _normalize_scd_cache_date_value(value)
            for value in dates
        )
        if normalized
    }


def _extract_scd_dates_from_context_df(
    context_df: Optional[pd.DataFrame],
) -> set[str]:
    """Extract available YYYY-MM-DD dates from an SCD indicator/context dataframe."""
    if not isinstance(context_df, pd.DataFrame) or context_df.empty:
        return set()

    try:
        idx = pd.DatetimeIndex(context_df.index)
        if idx.tz is not None:
            idx = idx.tz_localize(None)
        return {
            normalized
            for normalized in (
                _normalize_scd_cache_date_value(value)
                for value in idx
            )
            if normalized
        }
    except Exception:
        return set()


def _classify_scd_cache_dates(date_strings: set[str]) -> Dict[str, set[str]]:
    """
    Classify cache dates into completed historical dates and live dates.

    WS11-G conservative policy:
    - today's date is live only if today is a US trading day
    - all other available dates are treated as completed for session-cache reuse
    """
    normalized_dates = {
        normalized
        for normalized in (
            _normalize_scd_cache_date_value(value)
            for value in date_strings
        )
        if normalized
    }

    today = datetime.now().date()
    today_str = today.strftime("%Y-%m-%d")
    today_dt = datetime.combine(today, datetime.min.time())

    live_dates: set[str] = set()
    if today_str in normalized_dates and is_us_trading_day(today_dt):
        live_dates.add(today_str)

    completed_dates = set(normalized_dates) - live_dates

    return {
        "available_dates": normalized_dates,
        "completed_dates": completed_dates,
        "live_dates": live_dates,
    }


def _get_scd_result_cell_cache() -> Dict[tuple[str, str, str], Dict[str, Any]]:
    """
    Return initialized SCD result-cell cache.

    D3-A Commit 1 writes completed historical cells only. Later D3-A steps may
    read this cache to avoid recalculating completed historical cells.
    """
    if 'scd_result_cell_cache' not in st.session_state:
        st.session_state.scd_result_cell_cache = {}
    return st.session_state.scd_result_cell_cache


def _get_scd_completed_result_cell(
    *,
    ticker: str,
    row_key: str,
    date_key: Any,
) -> Optional[Dict[str, Any]]:
    """
    Return one cached completed historical SCD cell, if available.

    This helper reads final cells produced by the existing SCD build path. It
    does not fetch data, calculate indicators, score signals, persist data,
    rank tickers, aggregate values, or reinterpret semantics.
    """
    normalized_ticker = str(ticker).strip().upper()
    normalized_row_key = str(row_key).strip()
    normalized_date = _normalize_scd_cache_date_value(date_key)

    if not normalized_ticker or not normalized_row_key or not normalized_date:
        return None

    if not _is_scd_completed_cache_date(normalized_date):
        return None

    cache = _get_scd_result_cell_cache()
    entry = cache.get((normalized_ticker, normalized_row_key, normalized_date))
    if not isinstance(entry, dict):
        return None

    cell = entry.get("cell")
    if not isinstance(cell, dict):
        return None

    if cell.get("status") != "ok":
        return None

    return dict(cell)


def _load_completed_result_cells_for_ticker(
    *,
    ticker: str,
    row_keys: list[str],
    date_keys: list[str],
) -> tuple[Dict[tuple[str, str], Dict[str, Any]], list[tuple[str, str]]]:
    """
    Load cached completed historical cells for one ticker.

    Returns:
      - cached cells keyed by (row_key, date_key)
      - missing (row_key, date_key) pairs

    Callers decide whether the cache coverage is sufficient to skip the
    expensive technical path. This helper only reads cache state.
    """
    cached_cells: Dict[tuple[str, str], Dict[str, Any]] = {}
    missing_cells: list[tuple[str, str]] = []

    for row_key in row_keys:
        normalized_row_key = str(row_key).strip()
        if not normalized_row_key:
            continue

        for date_key in date_keys:
            normalized_date = _normalize_scd_cache_date_value(date_key)
            if not normalized_date or not _is_scd_completed_cache_date(normalized_date):
                missing_cells.append((normalized_row_key, str(date_key)))
                continue

            cached_cell = _get_scd_completed_result_cell(
                ticker=ticker,
                row_key=normalized_row_key,
                date_key=normalized_date,
            )
            if cached_cell is None:
                missing_cells.append((normalized_row_key, normalized_date))
                continue

            cached_cells[(normalized_row_key, normalized_date)] = cached_cell

    return cached_cells, missing_cells


def _is_scd_completed_cache_date(date_key: Any) -> bool:
    """
    Return True when date_key is a completed historical cache date.

    This reuses the existing SCD completed/live date policy. Today's date is
    treated as live only when today is a US trading day.
    """
    normalized = _normalize_scd_cache_date_value(date_key)
    if not normalized:
        return False

    classified = _classify_scd_cache_dates({normalized})
    return normalized in classified.get("completed_dates", set())


def _store_scd_result_cell_cache_entry(
    *,
    ticker: str,
    row_key: str,
    date_key: Any,
    cell: Dict[str, Any],
    source: str,
) -> bool:
    """
    Store one completed historical SCD result cell.

    This helper does not fetch data, calculate indicators, score signals,
    persist data, rank tickers, aggregate values, or change matrix contents.
    It only stores already-built final SCD cells for future reuse.
    """
    if not isinstance(cell, dict):
        return False

    if cell.get("status") != "ok":
        return False

    normalized_ticker = str(ticker).strip().upper()
    normalized_row_key = str(row_key).strip()
    normalized_date = _normalize_scd_cache_date_value(date_key or cell.get("date"))

    if not normalized_ticker or not normalized_row_key or not normalized_date:
        return False

    if not _is_scd_completed_cache_date(normalized_date):
        return False

    cache = _get_scd_result_cell_cache()
    cache_key = (normalized_ticker, normalized_row_key, normalized_date)
    new_cell = dict(cell)

    existing_entry = cache.get(cache_key)
    if isinstance(existing_entry, dict) and existing_entry.get("cell") == new_cell:
        return False

    cache[cache_key] = {
        "ticker": normalized_ticker,
        "row_key": normalized_row_key,
        "date": normalized_date,
        "date_status": "completed",
        "cell": new_cell,
        "source": str(source),
        "created_at": datetime.now(),
    }

    _get_scd_cache_stats()["result_cell_writes"] += 1
    return True


def _store_scd_result_cells_from_matrix(
    *,
    matrix: Dict[str, Any],
    source: str,
) -> int:
    """
    Store completed historical cells from an existing SCD matrix.

    Supports both current SCD matrix shapes:
      - Single Indicator: matrix["cells"][date_key][ticker]
      - Multiple Indicators: matrix["cells"][row_key][ticker]
    """
    if not isinstance(matrix, dict):
        return 0

    view = str(matrix.get("view", "")).strip()
    stored_count = 0

    if view == "single_indicator_time_series":
        row_key = str(matrix.get("row_key", "")).strip()
        for date_key, cells_by_ticker in dict(matrix.get("cells", {})).items():
            if not isinstance(cells_by_ticker, dict):
                continue
            for ticker, cell in cells_by_ticker.items():
                if _store_scd_result_cell_cache_entry(
                    ticker=str(ticker),
                    row_key=row_key,
                    date_key=date_key,
                    cell=cell,
                    source=source,
                ):
                    stored_count += 1

        return stored_count

    row_keys = list(matrix.get("row_keys", []))
    for row_key in row_keys:
        cells_by_ticker = dict(matrix.get("cells", {}).get(row_key, {}))
        for ticker, cell in cells_by_ticker.items():
            if _store_scd_result_cell_cache_entry(
                ticker=str(ticker),
                row_key=str(row_key),
                date_key=cell.get("date") if isinstance(cell, dict) else None,
                cell=cell,
                source=source,
            ):
                stored_count += 1

    return stored_count


def _store_scd_coverage_cache_entry(
    *,
    ticker: str,
    anchor_mode: str,
    window_days: int,
    anchor_date: Optional[Any],
    rolling_payload: Optional[Dict[str, Any]],
    indicator_context_df: Optional[pd.DataFrame],
    source: str,
) -> None:
    """
    Store coverage metadata for a successful SCD bundle build.

    WS11-G-A/B writes metadata only. Later WS11-G steps may read these entries
    to reuse completed historical coverage across overlapping SCD requests.

    This helper does not fetch data, compute indicators, score signals, rank
    tickers, aggregate values, persist data, or mutate the returned bundle.
    """
    ticker = str(ticker).strip().upper()
    resolved_anchor_mode = str(anchor_mode).strip().lower()
    if resolved_anchor_mode not in {"asof", "start"}:
        resolved_anchor_mode = "asof"

    if 'scd_bundle_coverage_cache' not in st.session_state:
        st.session_state.scd_bundle_coverage_cache = {}

    rolling_dates = _extract_scd_dates_from_rolling_payload(rolling_payload)
    context_dates = _extract_scd_dates_from_context_df(indicator_context_df)

    coverage_dates = rolling_dates | context_dates
    classified = _classify_scd_cache_dates(coverage_dates)

    if not classified["available_dates"]:
        return

    anchor_date_key = _normalize_scd_cache_date_value(anchor_date)
    source_signature = (
        int(window_days),
        resolved_anchor_mode,
        anchor_date_key,
    )

    entry = {
        "ticker": ticker,
        "anchor_mode": resolved_anchor_mode,
        "created_at": datetime.now(),
        "source": str(source),
        "source_signature": source_signature,
        "source_request": {
            "window_days": int(window_days),
            "anchor_mode": resolved_anchor_mode,
            "anchor_date": anchor_date_key,
        },
        "available_dates": sorted(classified["available_dates"]),
        "completed_dates": sorted(classified["completed_dates"]),
        "live_dates": sorted(classified["live_dates"]),
        "contains_live_date": bool(classified["live_dates"]),
        "rolling_payload": rolling_payload,
        "indicator_context_df": (
            indicator_context_df.copy()
            if isinstance(indicator_context_df, pd.DataFrame)
            else indicator_context_df
        ),
    }

    cache_key = (ticker, resolved_anchor_mode)
    existing_entries = list(
        st.session_state.scd_bundle_coverage_cache.get(cache_key, [])
    )

    # Replace same request signature instead of growing duplicate entries.
    existing_entries = [
        existing
        for existing in existing_entries
        if existing.get("source_signature") != source_signature
    ]

    existing_entries.append(entry)

    # Keep the cache bounded while preserving the most recent coverage entries.
    st.session_state.scd_bundle_coverage_cache[cache_key] = existing_entries[-5:]

    stats = _get_scd_cache_stats()
    stats["coverage_writes"] += 1


def _normalize_scd_requested_cache_dates(
    requested_date_strings: Optional[list[str] | set[str] | tuple[str, ...]],
) -> set[str]:
    """Normalize requested visible date strings for coverage-cache lookup."""
    if not requested_date_strings:
        return set()

    return {
        normalized
        for normalized in (
            _normalize_scd_cache_date_value(value)
            for value in requested_date_strings
        )
        if normalized
    }


def _can_reuse_scd_coverage_entry(
    *,
    entry: Dict[str, Any],
    requested_dates: set[str],
) -> bool:
    """
    Return True when a coverage cache entry can satisfy requested dates.

    WS11-G-C1 policy:
    - reuse completed historical dates only
    - do not reuse live/current-day data in this step
    """
    if not isinstance(entry, dict) or not requested_dates:
        return False

    rolling_payload = entry.get("rolling_payload")
    indicator_context_df = entry.get("indicator_context_df")

    if not isinstance(rolling_payload, dict) or not rolling_payload:
        return False

    if not isinstance(indicator_context_df, pd.DataFrame) or indicator_context_df.empty:
        return False

    available_dates = set(entry.get("available_dates", []) or [])
    completed_dates = set(entry.get("completed_dates", []) or [])
    live_dates = set(entry.get("live_dates", []) or [])
    rolling_dates = _extract_scd_dates_from_rolling_payload(rolling_payload)

    if not requested_dates.issubset(available_dates):
        return False

    # The context dataframe can cover more dates than the rolling signal payload.
    # Reuse is valid only when the rolling payload itself contains every
    # requested visible date.
    if not requested_dates.issubset(rolling_dates):
        return False

    if requested_dates & live_dates:
        return False

    if not requested_dates.issubset(completed_dates):
        return False

    return True


def _find_scd_coverage_cache_entry(
    *,
    ticker: str,
    anchor_mode: str,
    requested_date_strings: Optional[list[str] | set[str] | tuple[str, ...]],
) -> Optional[Dict[str, Any]]:
    """
    Find a coverage-compatible SCD bundle entry for completed-date reuse.

    This is intentionally conservative and only returns entries that fully
    cover the requested visible Single Indicator date window.
    """
    ticker = str(ticker).strip().upper()
    resolved_anchor_mode = str(anchor_mode).strip().lower()
    if resolved_anchor_mode not in {"asof", "start"}:
        resolved_anchor_mode = "asof"

    requested_dates = _normalize_scd_requested_cache_dates(requested_date_strings)
    if not requested_dates:
        return None

    coverage_cache = st.session_state.get("scd_bundle_coverage_cache", {})
    entries = list(coverage_cache.get((ticker, resolved_anchor_mode), []) or [])

    reusable_entries = [
        entry
        for entry in entries
        if _can_reuse_scd_coverage_entry(
            entry=entry,
            requested_dates=requested_dates,
        )
    ]

    if not reusable_entries:
        return None

    reusable_entries.sort(
        key=lambda entry: (
            len(entry.get("completed_dates", []) or []),
            entry.get("created_at", datetime.min),
        ),
        reverse=True,
    )

    return reusable_entries[0]


def _fetch_scd_rolling_payload_for_ticker(
    *,
    ticker: str,
    window_days: int = 10,
    force_refresh: bool = False,
    anchor_date: Optional[Any] = None,
    anchor_mode: str = "asof",
) -> Dict[str, Any]:
    """
    Fetch the existing Rolling Heatmap / Option-C rolling payload for one ticker.

    SCD must not call yfinance directly and must not create a new acquisition
    path. This function delegates to the existing technical calculator path.

    WS6 adds session-only caching around that existing path.
    """
    ticker = str(ticker).strip().upper()

    if 'scd_payload_cache' not in st.session_state:
        st.session_state.scd_payload_cache = {}

    stats = _get_scd_cache_stats()
    cache_key = _get_scd_cache_key(
        ticker=ticker,
        window_days=window_days,
        payload_kind="rolling_payload",
        anchor_date=anchor_date,
        anchor_mode=anchor_mode,
    )

    if not force_refresh and cache_key in st.session_state.scd_payload_cache:
        stats["rolling_hits"] += 1
        return st.session_state.scd_payload_cache[cache_key]

    stats["rolling_misses"] += 1

    payload = st.session_state.technical_calculator.calculate_rule_engine_signals_optionc(
        ticker=ticker,
        feature_scope="heatmap",
        save_to_db=False,
        use_meta_coverage=True,
        return_type="rolling",
        ohlcv_request=_get_scd_ohlcv_request(
            window_days=window_days,
            anchor_date=anchor_date,
            anchor_mode=anchor_mode,
        ),
    )

    if isinstance(payload, dict) and payload:
        st.session_state.scd_payload_cache[cache_key] = payload

    return payload


def _fetch_scd_hover_ohlcv_df_for_ticker(
    *,
    ticker: str,
    window_days: int = 10,
    force_refresh: bool = False,
    anchor_date: Optional[Any] = None,
    anchor_mode: str = "asof",
) -> Optional[pd.DataFrame]:
    """
    Fetch hover-only OHLCV / indicator context for adapter hover enrichment.

    This mirrors the existing Rolling Signal Heatmap hover-context call.
    It is display context only and does not create SCD-local scores,
    rankings, aggregates, semantic labels, or persistence behavior.

    WS6 adds session-only caching around that existing path.
    """
    ticker = str(ticker).strip().upper()

    if 'scd_hover_ohlcv_cache' not in st.session_state:
        st.session_state.scd_hover_ohlcv_cache = {}

    stats = _get_scd_cache_stats()
    cache_key = _get_scd_cache_key(
        ticker=ticker,
        window_days=window_days,
        payload_kind="hover_ohlcv",
        anchor_date=anchor_date,
        anchor_mode=anchor_mode,
    )

    if not force_refresh and cache_key in st.session_state.scd_hover_ohlcv_cache:
        stats["hover_hits"] += 1
        cached_df = st.session_state.scd_hover_ohlcv_cache[cache_key]
        return cached_df.copy() if isinstance(cached_df, pd.DataFrame) else cached_df

    stats["hover_misses"] += 1

    try:
        hover_df = st.session_state.technical_calculator.calculate_optionc_indicators(
            ticker=ticker,
            save_to_db=False,
            ohlcv_request=_get_scd_ohlcv_request(
                window_days=window_days,
                anchor_date=anchor_date,
                anchor_mode=anchor_mode,
            ),
        )

        if isinstance(hover_df, pd.DataFrame) and not hover_df.empty:
            st.session_state.scd_hover_ohlcv_cache[cache_key] = hover_df.copy()

        return hover_df

    except Exception:
        return None


def _fetch_scd_rolling_bundle_for_ticker(
    *,
    ticker: str,
    window_days: int = 10,
    force_refresh: bool = False,
    anchor_date: Optional[Any] = None,
    anchor_mode: str = "asof",
    requested_date_strings: Optional[list[str] | set[str] | tuple[str, ...]] = None,
    historical_buffer_days: int = 435,
) -> Dict[str, Any]:
    """
    Fetch rolling payload and hover/context dataframe through one technical pass.

    This is a transport optimization for SCD only:
    - rolling_payload remains the existing Rolling Heatmap / Option-C payload
    - indicator_context_df is the already-computed df_ind from that same path
    - both are stored in the existing session-only SCD caches
    - no SCD-local scoring, ranking, aggregation, semantics, acquisition, or
      persistence behavior is introduced
    """
    ticker = str(ticker).strip().upper()

    if 'scd_payload_cache' not in st.session_state:
        st.session_state.scd_payload_cache = {}

    if 'scd_payload_cache_meta' not in st.session_state:
        st.session_state.scd_payload_cache_meta = {}

    if 'scd_hover_ohlcv_cache' not in st.session_state:
        st.session_state.scd_hover_ohlcv_cache = {}

    stats = _get_scd_cache_stats()

    stats = _get_scd_cache_stats()

    rolling_cache_key = _get_scd_cache_key(
        ticker=ticker,
        window_days=window_days,
        payload_kind="rolling_payload",
        anchor_date=anchor_date,
        anchor_mode=anchor_mode,
        historical_buffer_days=historical_buffer_days,
    )
    hover_cache_key = _get_scd_cache_key(
        ticker=ticker,
        window_days=window_days,
        payload_kind="hover_ohlcv",
        anchor_date=anchor_date,
        anchor_mode=anchor_mode,
        historical_buffer_days=historical_buffer_days,
    )

    rolling_hit = (
        not force_refresh
        and rolling_cache_key in st.session_state.scd_payload_cache
    )
    hover_hit = (
        not force_refresh
        and hover_cache_key in st.session_state.scd_hover_ohlcv_cache
    )

    if rolling_hit and hover_hit:
        stats["rolling_hits"] += 1
        stats["hover_hits"] += 1

        rolling_payload = st.session_state.scd_payload_cache[rolling_cache_key]
        cached_df = st.session_state.scd_hover_ohlcv_cache[hover_cache_key]
        cache_meta = st.session_state.scd_payload_cache_meta.get(
            rolling_cache_key,
            {},
        )

        return {
            "rolling_payload": rolling_payload,
            "indicator_context_df": cached_df.copy() if isinstance(cached_df, pd.DataFrame) else cached_df,
            "source": "cache",
            "cache_as_of": cache_meta.get("as_of"),
            "cache_as_of_source": cache_meta.get("source"),
        }

    coverage_entry = None
    if not force_refresh:
        coverage_entry = _find_scd_coverage_cache_entry(
            ticker=ticker,
            anchor_mode=anchor_mode,
            requested_date_strings=requested_date_strings,
        )

    if coverage_entry is not None:
        stats["coverage_hits"] += 1
        indicator_context_df = coverage_entry.get("indicator_context_df")

        return {
            "rolling_payload": coverage_entry.get("rolling_payload"),
            "indicator_context_df": (
                indicator_context_df.copy()
                if isinstance(indicator_context_df, pd.DataFrame)
                else indicator_context_df
            ),
            "source": "coverage_cache",
            "cache_as_of": coverage_entry.get("created_at"),
            "cache_as_of_source": coverage_entry.get("source"),
        }

    if rolling_hit:
        # Rare partial-cache case: keep the cached rolling payload and only
        # fill the missing hover/context dataframe through the legacy fallback.
        stats["rolling_hits"] += 1
        rolling_payload = st.session_state.scd_payload_cache[rolling_cache_key]
        cache_meta = st.session_state.scd_payload_cache_meta.get(
            rolling_cache_key,
            {},
        )
        hover_df = _fetch_scd_hover_ohlcv_df_for_ticker(
            ticker=ticker,
            window_days=window_days,
            force_refresh=False,
            anchor_date=anchor_date,
            anchor_mode=anchor_mode,
        )

        return {
            "rolling_payload": rolling_payload,
            "indicator_context_df": hover_df,
            "source": "partial_cache_hover_fallback",
            "cache_as_of": cache_meta.get("as_of"),
            "cache_as_of_source": cache_meta.get("source"),
        }

    stats["rolling_misses"] += 1
    if hover_hit:
        stats["hover_hits"] += 1
    else:
        stats["hover_misses"] += 1

    bundle = st.session_state.technical_calculator.calculate_rule_engine_signals_optionc(
        ticker=ticker,
        feature_scope="heatmap",
        save_to_db=False,
        use_meta_coverage=True,
        return_type="rolling_with_context",
        ohlcv_request=_get_scd_ohlcv_request(
            window_days=window_days,
            anchor_date=anchor_date,
            anchor_mode=anchor_mode,
            historical_buffer_days=historical_buffer_days,
        ),
    )

    if not isinstance(bundle, dict):
        return {
            "rolling_payload": {},
            "indicator_context_df": None,
            "source": "invalid_bundle",
        }

    rolling_payload = bundle.get("rolling_payload")
    indicator_context_df = bundle.get("indicator_context_df")
    bundled_as_of = datetime.now().isoformat(timespec="seconds")
    bundled_source = "force_refresh" if force_refresh else "bundled"

    if isinstance(rolling_payload, dict) and rolling_payload:
        st.session_state.scd_payload_cache[rolling_cache_key] = rolling_payload
        st.session_state.scd_payload_cache_meta[rolling_cache_key] = {
            "as_of": bundled_as_of,
            "source": bundled_source,
        }

    if isinstance(indicator_context_df, pd.DataFrame) and not indicator_context_df.empty:
        st.session_state.scd_hover_ohlcv_cache[hover_cache_key] = indicator_context_df.copy()
    elif hover_hit:
        cached_df = st.session_state.scd_hover_ohlcv_cache[hover_cache_key]
        indicator_context_df = cached_df.copy() if isinstance(cached_df, pd.DataFrame) else cached_df

    _store_scd_coverage_cache_entry(
        ticker=ticker,
        anchor_mode=anchor_mode,
        window_days=window_days,
        anchor_date=anchor_date,
        rolling_payload=rolling_payload,
        indicator_context_df=indicator_context_df,
        source=bundled_source,
    )

    return {
        "rolling_payload": rolling_payload,
        "indicator_context_df": indicator_context_df,
        "source": "bundled",
        "cache_as_of": bundled_as_of,
        "cache_as_of_source": bundled_source,
    }


def _normalize_scd_rolling_payload_for_adapter(
    rolling_payload: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize the raw SCD rolling payload into the adapter contract.

    The existing Rolling Signal Heatmap does this before calling
    build_plotly_heatmap_inputs(...). SCD must do the same because the adapter
    expects dates + rows[row_key].values/scores/hover/extras, not the raw
    short_term.data[date][row_key] structure.
    """
    return _extract_rolling_signals_from_data({"rolling_signals": rolling_payload})


def _build_scd_adapter_lookup(
    *,
    rolling_payload: Dict[str, Any],
    row_keys: list[str],
    ohlcv_df: Optional[pd.DataFrame] = None,
) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Build adapter-owned display metadata by row_key and raw date.

    Shape:
        lookup[row_key][raw_date] = {
            "customdata": adapter customdata dict,
            "text": adapter in-cell text,
            "z": adapter score/color value,
        }

    This is the only SCD bridge into the Rolling Heatmap adapter display
    contract. It normalizes the raw payload before adapter use.
    """
    lookup: Dict[str, Dict[str, Dict[str, Any]]] = {}

    adapter_payload = _normalize_scd_rolling_payload_for_adapter(rolling_payload)

    try:
        hm = build_plotly_heatmap_inputs(
            rolling_payload=adapter_payload,
            indicator_keys=row_keys,
            indicator_defs=INDICATOR_DEFS,
            ohlcv_df=ohlcv_df,
        )
    except Exception:
        return lookup

    for row_idx, row_key in enumerate(hm.row_keys):
        lookup.setdefault(row_key, {})

        customdata_row = hm.customdata[row_idx] if row_idx < len(hm.customdata) else []
        text_row = hm.text[row_idx] if row_idx < len(hm.text) else []
        z_row = hm.z[row_idx] if row_idx < len(hm.z) else []

        for col_idx, adapter_cd in enumerate(customdata_row):
            if not isinstance(adapter_cd, dict):
                continue

            raw_date = adapter_cd.get("date")
            if raw_date is None:
                continue

            lookup[row_key][str(raw_date)] = {
                "customdata": dict(adapter_cd),
                "text": text_row[col_idx] if col_idx < len(text_row) else "",
                "z": z_row[col_idx] if col_idx < len(z_row) else None,
            }

    return lookup


def _extract_latest_scd_cell(
    *,
    ticker: str,
    row_key: str,
    rolling_payload: Dict[str, Any],
    adapter_lookup: Optional[Dict[str, Dict[str, Dict[str, Any]]]] = None,
) -> Dict[str, Any]:
    """
    Extract the latest available SCD matrix cell for row_key.

    Indicator rows preserve existing value / signal / score / hover / extras
    from the raw rolling payload. Display text and rich hover metadata are
    consumed from the normalized adapter path when available.
    """
    ticker = str(ticker).strip().upper()
    row_key = str(row_key).strip()
    dates = list(rolling_payload.get("dates", []))
    adapter_lookup = adapter_lookup or {}

    if row_key == "__PRICE__":
        for date_key in reversed(dates):
            adapter_entry = adapter_lookup.get("__PRICE__", {}).get(str(date_key), {})
            adapter_cd = adapter_entry.get("customdata")

            if not isinstance(adapter_cd, dict) or not adapter_cd:
                continue

            return {
                "ticker": ticker,
                "row_key": "__PRICE__",
                "date": date_key,
                "value": adapter_cd.get("raw_value"),
                "signal": "",
                "score": adapter_entry.get("z"),
                "hover": None,
                "status": "ok",
                "display_text": adapter_entry.get("text", ""),
                "adapter_customdata": dict(adapter_cd),
            }

        return {
            "ticker": ticker,
            "row_key": "__PRICE__",
            "date": dates[-1] if dates else None,
            "value": None,
            "signal": "",
            "score": None,
            "hover": f"No Price row available for {ticker}.",
            "status": "missing_cell",
            "display_text": "missing_cell",
        }

    short_term = rolling_payload.get("short_term")
    data = short_term.get("data", {}) if isinstance(short_term, dict) else {}

    for date_key in reversed(dates):
        date_cells = data.get(date_key, {})
        if not isinstance(date_cells, dict):
            continue

        source_cell = date_cells.get(row_key)
        if not isinstance(source_cell, dict):
            continue

        adapter_entry = adapter_lookup.get(row_key, {}).get(str(date_key), {})
        adapter_cd = adapter_entry.get("customdata")

        cell = {
            "ticker": ticker,
            "row_key": row_key,
            "date": date_key,
            "value": source_cell.get("value"),
            "signal": source_cell.get("signal"),
            "score": source_cell.get("score"),
            "hover": source_cell.get("hover"),
            "status": "ok",
            "display_text": adapter_entry.get("text", ""),
        }

        if "extras" in source_cell:
            cell["extras"] = source_cell.get("extras")

        if isinstance(adapter_cd, dict) and adapter_cd:
            cell["adapter_customdata"] = dict(adapter_cd)

        return cell

    return {
        "ticker": ticker,
        "row_key": row_key,
        "date": None,
        "value": None,
        "signal": None,
        "score": None,
        "hover": f"No latest cell available for {row_key} on {ticker}.",
        "status": "missing_cell",
        "display_text": "missing_cell",
    }


def _extract_scd_cell_for_date(
    *,
    ticker: str,
    row_key: str,
    date_key: str,
    rolling_payload: Dict[str, Any],
    adapter_lookup: Optional[Dict[str, Dict[str, Dict[str, Any]]]] = None,
) -> Dict[str, Any]:
    """
    Extract one existing Rolling Heatmap cell for a specific row_key/date.

    This is used by the SCD Single Indicator time-series matrix. It preserves
    source value / signal / score / hover / extras and adapter customdata.
    """
    ticker = str(ticker).strip().upper()
    row_key = str(row_key).strip()
    date_key = str(date_key).strip()
    adapter_lookup = adapter_lookup or {}

    short_term = rolling_payload.get("short_term")
    data = short_term.get("data", {}) if isinstance(short_term, dict) else {}

    if row_key == "__PRICE__":
        adapter_entry = adapter_lookup.get("__PRICE__", {}).get(date_key, {})
        adapter_cd = adapter_entry.get("customdata")

        if isinstance(adapter_cd, dict) and adapter_cd:
            return {
                "ticker": ticker,
                "row_key": "__PRICE__",
                "date": date_key,
                "value": adapter_cd.get("raw_value"),
                "signal": "",
                "score": adapter_entry.get("z"),
                "hover": None,
                "status": "ok",
                "display_text": adapter_entry.get("text", ""),
                "adapter_customdata": dict(adapter_cd),
            }

        return {
            "ticker": ticker,
            "row_key": "__PRICE__",
            "date": date_key,
            "value": None,
            "signal": "",
            "score": None,
            "hover": f"No Price row available for {ticker} at {date_key}.",
            "status": "missing_cell",
            "display_text": "missing_cell",
        }

    date_cells = data.get(date_key, {})
    if not isinstance(date_cells, dict):
        date_cells = {}

    source_cell = date_cells.get(row_key)
    if not isinstance(source_cell, dict):
        return {
            "ticker": ticker,
            "row_key": row_key,
            "date": date_key,
            "value": None,
            "signal": None,
            "score": None,
            "hover": f"No cell available for {row_key} on {ticker} at {date_key}.",
            "status": "missing_cell",
            "display_text": "missing_cell",
        }

    adapter_entry = adapter_lookup.get(row_key, {}).get(date_key, {})
    adapter_cd = adapter_entry.get("customdata")

    cell = {
        "ticker": ticker,
        "row_key": row_key,
        "date": date_key,
        "value": source_cell.get("value"),
        "signal": source_cell.get("signal"),
        "score": source_cell.get("score"),
        "hover": source_cell.get("hover"),
        "status": "ok",
        "display_text": adapter_entry.get("text", ""),
    }

    if "extras" in source_cell:
        cell["extras"] = source_cell.get("extras")

    if isinstance(adapter_cd, dict) and adapter_cd:
        cell["adapter_customdata"] = dict(adapter_cd)

    return cell


def _build_scd_price_cell_from_context_df(
    *,
    ticker: str,
    date_key: str,
    context_df: Optional[pd.DataFrame],
) -> Dict[str, Any]:
    """
    Build a display-only Price cell for the SCD Single Indicator hover.

    This uses the already-bundled indicator/OHLCV context dataframe returned
    with the SCD rolling bundle. It does not fetch data, score data, persist
    data, or introduce new technical semantics.
    """
    ticker = str(ticker).strip().upper()
    date_key = str(date_key).strip()

    if not isinstance(context_df, pd.DataFrame) or context_df.empty:
        return {
            "ticker": ticker,
            "row_key": "__PRICE__",
            "date": date_key,
            "value": None,
            "signal": "",
            "score": None,
            "hover": f"No context dataframe available for {ticker} at {date_key}.",
            "status": "missing_context_df",
            "display_text": "missing_context_df",
        }

    price_col = "Adj Close" if "Adj Close" in context_df.columns else "Close"
    if price_col not in context_df.columns:
        return {
            "ticker": ticker,
            "row_key": "__PRICE__",
            "date": date_key,
            "value": None,
            "signal": "",
            "score": None,
            "hover": f"No price column available for {ticker} at {date_key}.",
            "status": "missing_price_column",
            "display_text": "missing_price_column",
        }

    try:
        df = context_df.copy()
        df.index = pd.to_datetime(df.index)
        df.index = df.index.tz_localize(None) if df.index.tz is not None else df.index
        df.index = df.index.normalize()
        df = df.sort_index()

        target_date = pd.Timestamp(date_key).normalize()

        matching_rows = df.loc[df.index == target_date]
        if matching_rows.empty:
            return {
                "ticker": ticker,
                "row_key": "__PRICE__",
                "date": date_key,
                "value": None,
                "signal": "",
                "score": None,
                "hover": f"No price row available for {ticker} at {date_key}.",
                "status": "missing_price_date",
                "display_text": "missing_price_date",
            }

        current_price = pd.to_numeric(
            matching_rows[price_col],
            errors="coerce",
        ).dropna()

        if current_price.empty:
            return {
                "ticker": ticker,
                "row_key": "__PRICE__",
                "date": date_key,
                "value": None,
                "signal": "",
                "score": None,
                "hover": f"Price value is missing for {ticker} at {date_key}.",
                "status": "missing_price_value",
                "display_text": "missing_price_value",
            }

        price_value = float(current_price.iloc[-1])

        prior_rows = df.loc[df.index < target_date]
        prior_price = None
        if not prior_rows.empty:
            prior_series = pd.to_numeric(
                prior_rows[price_col],
                errors="coerce",
            ).dropna()
            if not prior_series.empty:
                prior_price = float(prior_series.iloc[-1])

        delta_abs = None
        delta_pct = None
        if prior_price is not None:
            delta_abs = price_value - prior_price
            if prior_price != 0:
                delta_pct = (delta_abs / prior_price) * 100.0

        if delta_abs is None:
            trend = ""
            trend_line = ""
            delta_abs_fmt = "—"
            delta_pct_suffix = ""
        else:
            if delta_abs > 0:
                trend = "Rising"
            elif delta_abs < 0:
                trend = "Falling"
            else:
                trend = "Flat"

            trend_line = f"Trend: {trend}<br>"
            delta_abs_fmt = f"{delta_abs:+.2f}"
            delta_pct_suffix = (
                f" ({delta_pct:+.1f}%)"
                if delta_pct is not None
                else ""
            )

        formatted_value = f"{price_value:.2f}"

        adapter_customdata = {
            "indicator_key": "__PRICE__",
            "display_name": "Price",
            "date": date_key,
            "raw_value": price_value,
            "formatted_value": formatted_value,
            "score": None,
            "score_label": "",
            "delta_abs": delta_abs,
            "delta_pct": delta_pct,
            "trend": trend,
            "rule_expr": "",
            "rule_notes": "",
            "rule_text": "",
            "definition": "",
            "how_to_read": "",
            "delta_abs_fmt": delta_abs_fmt,
            "delta_pct_suffix": delta_pct_suffix,
            "trend_line": trend_line,
            "signal_line": "",
            "rule_block": "",
            "notes_block": "",
            "definition_block": "",
            "how_to_read_block": "",
            "volume_block": "",
            "volume_vs_avg_block": "",
            "band_context_block": "",
            "ma_context_block": "",
            "macd_context_block": "",
            "adx_context_block": "",
            "stoch_context_block": "",
            "dpo_context_block": "",
            "bullbear_context_block": "",
            "meta": {},
        }

        return {
            "ticker": ticker,
            "row_key": "__PRICE__",
            "date": date_key,
            "value": price_value,
            "signal": "",
            "score": None,
            "hover": None,
            "status": "ok",
            "display_text": formatted_value,
            "adapter_customdata": adapter_customdata,
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "row_key": "__PRICE__",
            "date": date_key,
            "value": None,
            "signal": "",
            "score": None,
            "hover": f"Price context error for {ticker} at {date_key}: {e}",
            "status": "price_context_error",
            "display_text": "price_context_error",
        }


# SCD-scaffolding for 'refresh "today"'
def _build_scd_single_indicator_cell_from_bundle(
    *,
    ticker: str,
    row_key: str,
    date_key: str,
    rolling_payload: Dict[str, Any],
    adapter_lookup: Dict[tuple[str, str], Dict[str, Any]],
    context_df: Optional[pd.DataFrame],
) -> Dict[str, Any]:
    """
    Build one SCD Single Indicator date/ticker cell from an existing bundle.

    This helper centralizes the same cell construction used by the normal
    Single Indicator matrix build:
    - extract the indicator cell from the rolling payload / adapter lookup
    - build the attached Price cell from the context dataframe
    - attach Price context only when available

    It does not fetch data, compute indicators, score signals, rank tickers,
    aggregate values, persist data, or reinterpret semantics.
    """
    cell = _extract_scd_cell_for_date(
        ticker=ticker,
        row_key=row_key,
        date_key=date_key,
        rolling_payload=rolling_payload,
        adapter_lookup=adapter_lookup,
    )

    # The shared Rolling Heatmap adapter emits its display-only __PRICE__
    # row alongside requested indicator rows. Reuse that already-built
    # Price cell instead of repeatedly copying, normalizing, sorting, and
    # scanning the context dataframe for every displayed date.
    adapter_price_entry = (
        adapter_lookup
        .get("__PRICE__", {})
        .get(str(date_key), {})
    )
    adapter_price_customdata = adapter_price_entry.get("customdata")

    if (
        isinstance(adapter_price_customdata, dict)
        and adapter_price_customdata
    ):
        price_cell = {
            "ticker": str(ticker).strip().upper(),
            "row_key": "__PRICE__",
            "date": str(date_key).strip(),
            "value": adapter_price_customdata.get("raw_value"),
            "signal": "",
            "score": adapter_price_entry.get("z"),
            "hover": None,
            "status": "ok",
            "display_text": adapter_price_entry.get("text", ""),
            "adapter_customdata": dict(adapter_price_customdata),
        }
    else:
        # Defensive compatibility fallback for malformed, partial, or older
        # payloads that do not contain an adapter-owned Price entry.
        price_cell = _build_scd_price_cell_from_context_df(
            ticker=ticker,
            date_key=date_key,
            context_df=context_df,
        )

    if price_cell.get("status") == "ok":
        cell["price_cell"] = price_cell

    return cell


def _get_scd_current_live_date_key() -> Optional[str]:
    """
    Return today's date key only when today is a US trading day.

    This helper is intentionally narrow:
    - weekend / holiday returns None
    - no market-hours inference is attempted
    - no acquisition, scoring, persistence, or semantic behavior changes
    """
    today = datetime.now().date()
    today_dt = datetime.combine(today, datetime.min.time())

    if not is_us_trading_day(today_dt):
        return None

    return today.strftime("%Y-%m-%d")


def _format_scd_live_as_of_label(as_of: Any) -> Optional[str]:
    """
    Return a compact UI label for live/current-day SCD timestamps.

    Example:
        (a/o: 6/18 @ 12:15 PM)

    This is display metadata only. It does not imply market-data exchange
    timestamp precision.
    """
    if as_of is None:
        return None

    try:
        ts = pd.Timestamp(as_of)
        if pd.isna(ts):
            return None
        if ts.tzinfo is not None:
            ts = ts.tz_localize(None)

        dt = ts.to_pydatetime()
        time_label = dt.strftime("%I:%M %p").lstrip("0")
        return f"(a/o: {dt.month}/{dt.day} @ {time_label})"
    except Exception:
        return None


def _get_scd_live_as_of_meta(
    *,
    matrix: Dict[str, Any],
    date_key: Any,
) -> Optional[Dict[str, Any]]:
    """
    Return stored live/current-day as-of metadata for a matrix/date.

    This reads matrix/session display metadata only. It does not fetch data,
    compute indicators, score signals, persist data, or reinterpret semantics.
    """
    if not isinstance(matrix, dict):
        return None

    normalized_date = _normalize_scd_cache_date_value(date_key)
    if not normalized_date:
        return None

    live_as_of = matrix.get("live_as_of", {})
    if not isinstance(live_as_of, dict):
        return None

    meta = live_as_of.get(normalized_date)
    if not isinstance(meta, dict):
        return None

    return dict(meta)


def _get_scd_live_as_of_caption(
    *,
    matrix: Dict[str, Any],
    date_key: Any,
) -> Optional[str]:
    """
    Return a compact caption for live/current-day SCD matrix data.
    """
    meta = _get_scd_live_as_of_meta(matrix=matrix, date_key=date_key)
    if not meta:
        return None

    label = meta.get("label") or _format_scd_live_as_of_label(meta.get("as_of"))
    if not label:
        return None

    return f"{label}"


def _mark_scd_live_cells_as_of(
    *,
    matrix: Dict[str, Any],
    date_key: Any,
    as_of: Any,
    source: str,
) -> None:
    """
    Mark live/current-day cells in an existing SCD matrix with as-of metadata.

    This mutates only display/session metadata on already-built matrix cells.
    It does not fetch data, compute indicators, score signals, persist data,
    rank tickers, aggregate values, or reinterpret semantics.
    """
    if not isinstance(matrix, dict):
        return

    normalized_date = _normalize_scd_cache_date_value(date_key)
    live_date_key = _get_scd_current_live_date_key()

    if not normalized_date or normalized_date != live_date_key:
        return

    as_of_ts = pd.Timestamp(as_of)
    if as_of_ts.tzinfo is not None:
        as_of_ts = as_of_ts.tz_localize(None)

    as_of_iso = as_of_ts.isoformat(timespec="seconds")
    label = _format_scd_live_as_of_label(as_of_ts)

    meta = {
        "date": normalized_date,
        "as_of": as_of_iso,
        "label": label,
        "source": str(source),
    }

    matrix.setdefault("live_as_of", {})
    matrix["live_as_of"][normalized_date] = dict(meta)

    matrix.setdefault("profile", {})
    matrix["profile"].setdefault("live_as_of", {})
    matrix["profile"]["live_as_of"][normalized_date] = dict(meta)

    view = str(matrix.get("view", "")).strip()

    if view == "single_indicator_time_series":
        cells_by_ticker = matrix.get("cells", {}).get(normalized_date, {})
        if not isinstance(cells_by_ticker, dict):
            return

        for cell in cells_by_ticker.values():
            if not isinstance(cell, dict):
                continue
            if _normalize_scd_cache_date_value(cell.get("date")) != normalized_date:
                continue

            cell["date_status"] = "live"
            cell["live_as_of"] = as_of_iso
            cell["live_as_of_label"] = label

            price_cell = cell.get("price_cell")
            if isinstance(price_cell, dict):
                price_cell["date_status"] = "live"
                price_cell["live_as_of"] = as_of_iso
                price_cell["live_as_of_label"] = label

        return

    for cells_by_ticker in matrix.get("cells", {}).values():
        if not isinstance(cells_by_ticker, dict):
            continue

        for cell in cells_by_ticker.values():
            if not isinstance(cell, dict):
                continue
            if _normalize_scd_cache_date_value(cell.get("date")) != normalized_date:
                continue

            cell["date_status"] = "live"
            cell["live_as_of"] = as_of_iso
            cell["live_as_of_label"] = label


def _normalize_scd_compare_value(value: Any) -> Any:
    """
    Normalize a cell field for D3-C tail-buffer comparison.

    This is diagnostic-only. It does not change cells, scoring, rendering, or
    persistence behavior.
    """
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    if isinstance(value, (int, float)):
        return round(float(value), 8)

    return value


def _compare_scd_tail_cells(
    *,
    reference_cell: Dict[str, Any],
    candidate_cell: Dict[str, Any],
    value_tolerance: float = 1e-6,
) -> Dict[str, Any]:
    """
    Compare one candidate reduced-tail cell against the 435-day reference cell.

    Equivalence is intentionally strict for production gating:
    - score must match
    - signal must match
    - status must match
    - display_text must match
    - numeric value must match within tolerance
    """
    reference_value = _normalize_scd_compare_value(reference_cell.get("value"))
    candidate_value = _normalize_scd_compare_value(candidate_cell.get("value"))

    if isinstance(reference_value, float) and isinstance(candidate_value, float):
        value_delta = abs(reference_value - candidate_value)
        value_match = value_delta <= float(value_tolerance)
    else:
        value_delta = None
        value_match = reference_value == candidate_value

    checks = {
        "status_match": reference_cell.get("status") == candidate_cell.get("status"),
        "score_match": reference_cell.get("score") == candidate_cell.get("score"),
        "signal_match": reference_cell.get("signal") == candidate_cell.get("signal"),
        "display_text_match": reference_cell.get("display_text") == candidate_cell.get("display_text"),
        "value_match": value_match,
    }

    return {
        "safe_for_candidate": all(checks.values()),
        "reference_value": reference_value,
        "candidate_value": candidate_value,
        "value_delta": value_delta,
        "reference_score": reference_cell.get("score"),
        "candidate_score": candidate_cell.get("score"),
        "reference_signal": reference_cell.get("signal"),
        "candidate_signal": candidate_cell.get("signal"),
        "reference_status": reference_cell.get("status"),
        "candidate_status": candidate_cell.get("status"),
        **checks,
    }


def _build_scd_tail_diagnostic_cell(
    *,
    ticker: str,
    row_key: str,
    date_key: str,
    window_days: int,
    anchor_date: Any,
    anchor_mode: str,
    historical_buffer_days: int,
    scoring_indicators: Optional[list[str]] = None,
    compute_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build one SCD cell through the existing technical/rule-engine path using
    a specified Scenario B historical buffer.

    Diagnostic-only:
    - no session cache writes
    - no result-cell writes
    - no scoring changes
    - no formula changes
    - no direct yfinance calls from SCD
    - no persistence behavior
    """
    started_at = time.perf_counter()

    bundle = st.session_state.technical_calculator.calculate_rule_engine_signals_optionc(
        ticker=ticker,
        feature_scope="heatmap",
        save_to_db=False,
        config=compute_config,
        indicators=scoring_indicators,
        use_meta_coverage=True,
        return_type="rolling_with_context",
        ohlcv_request=_get_scd_ohlcv_request(
            window_days=window_days,
            anchor_date=anchor_date,
            anchor_mode=anchor_mode,
            historical_buffer_days=historical_buffer_days,
        ),
    )

    rolling_payload = bundle.get("rolling_payload") if isinstance(bundle, dict) else {}
    context_df = bundle.get("indicator_context_df") if isinstance(bundle, dict) else None

    if not isinstance(rolling_payload, dict) or not rolling_payload:
        raise ValueError(
            f"No rolling payload returned for {ticker} using "
            f"historical_buffer_days={historical_buffer_days}."
        )

    adapter_lookup = _build_scd_adapter_lookup(
        rolling_payload=rolling_payload,
        row_keys=[row_key],
        ohlcv_df=context_df,
    )

    cell = _build_scd_single_indicator_cell_from_bundle(
        ticker=ticker,
        row_key=row_key,
        date_key=date_key,
        rolling_payload=rolling_payload,
        adapter_lookup=adapter_lookup,
        context_df=context_df,
    )

    return {
        "cell": cell,
        "seconds": round(time.perf_counter() - started_at, 3),
        "scoring_indicators": list(scoring_indicators) if scoring_indicators else None,
        "compute_config_keys": (
            sorted(compute_config.keys())
            if isinstance(compute_config, dict)
            else None
        ),
        "context_rows": len(context_df) if isinstance(context_df, pd.DataFrame) else None,
        "context_first_date": (
            pd.Timestamp(context_df.index.min()).strftime("%Y-%m-%d")
            if isinstance(context_df, pd.DataFrame) and not context_df.empty
            else None
        ),
        "context_last_date": (
            pd.Timestamp(context_df.index.max()).strftime("%Y-%m-%d")
            if isinstance(context_df, pd.DataFrame) and not context_df.empty
            else None
        ),
    }


def _run_scd_tail_buffer_equivalence_diagnostic(
    *,
    matrix: Dict[str, Any],
    ticker: str,
    diagnostic_date_key: Any,
    candidate_buffers: list[int],
) -> Dict[str, Any]:
    """
    Compare reduced Scenario B buffers against the 435-day reference for one
    visible Single Indicator matrix date.

    This produces evidence only. It does not enable reduced-tail production
    refresh.
    """
    started_at = time.perf_counter()

    if not isinstance(matrix, dict) or matrix.get("view") != "single_indicator_time_series":
        raise ValueError("Tail-buffer diagnostic requires a Single Indicator matrix.")

    selected_date_key = _normalize_scd_cache_date_value(diagnostic_date_key)
    if not selected_date_key:
        raise ValueError("Select a valid diagnostic date from the current matrix.")

    matrix_dates = [
        _normalize_scd_cache_date_value(date_key)
        for date_key in matrix.get("dates", [])
    ]
    matrix_dates = [date_key for date_key in matrix_dates if date_key]

    if selected_date_key not in matrix_dates:
        raise ValueError(
            f"Tail-buffer diagnostic date ({selected_date_key}) is not present "
            "in the current Single Indicator matrix."
        )

    tickers = _dedupe_preserve_order_str(matrix.get("tickers", []))
    normalized_ticker = str(ticker).strip().upper()
    if normalized_ticker not in tickers:
        raise ValueError(f"{normalized_ticker} is not in the current Single Indicator matrix.")

    row_key = str(matrix.get("row_key", "")).strip()
    window_days = int(matrix.get("window_days", len(matrix_dates) or 10))
    anchor_date = matrix.get("anchor_date")
    anchor_mode = str(matrix.get("anchor_mode", "asof"))

    candidate_buffers = [
        int(buffer)
        for buffer in candidate_buffers
        if int(buffer) > 0 and int(buffer) != 435
    ]

    if not candidate_buffers:
        raise ValueError("Select at least one candidate buffer other than 435.")

    reference = _build_scd_tail_diagnostic_cell(
        ticker=normalized_ticker,
        row_key=row_key,
        date_key=selected_date_key,
        window_days=window_days,
        anchor_date=anchor_date,
        anchor_mode=anchor_mode,
        historical_buffer_days=435,
    )

    reference_cell = reference["cell"]
    candidates = []

    for buffer_days in candidate_buffers:
        candidate_record = {
            "ticker": normalized_ticker,
            "row_key": row_key,
            "date": selected_date_key,
            "reference_buffer_days": 435,
            "candidate_buffer_days": int(buffer_days),
            "candidate_seconds": None,
            "candidate_context_rows": None,
            "candidate_context_first_date": None,
            "candidate_context_last_date": None,
            "safe_for_candidate": False,
            "error": None,
        }

        try:
            candidate = _build_scd_tail_diagnostic_cell(
                ticker=normalized_ticker,
                row_key=row_key,
                date_key=selected_date_key,
                window_days=window_days,
                anchor_date=anchor_date,
                anchor_mode=anchor_mode,
                historical_buffer_days=int(buffer_days),
            )

            comparison = _compare_scd_tail_cells(
                reference_cell=reference_cell,
                candidate_cell=candidate["cell"],
            )

            candidate_record.update(comparison)
            candidate_record.update(
                {
                    "candidate_seconds": candidate["seconds"],
                    "candidate_context_rows": candidate["context_rows"],
                    "candidate_context_first_date": candidate["context_first_date"],
                    "candidate_context_last_date": candidate["context_last_date"],
                }
            )

        except Exception as e:
            candidate_record["error"] = str(e)

        candidates.append(candidate_record)

    report = {
        "status": "ok",
        "ticker": normalized_ticker,
        "row_key": row_key,
        "date": selected_date_key,
        "reference_buffer_days": 435,
        "reference_seconds": reference["seconds"],
        "reference_context_rows": reference["context_rows"],
        "reference_context_first_date": reference["context_first_date"],
        "reference_context_last_date": reference["context_last_date"],
        "candidate_buffers": candidate_buffers,
        "candidates": candidates,
        "total_seconds": round(time.perf_counter() - started_at, 3),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    return report


def _get_scd_engine_indicator_for_row_key(row_key: str) -> Optional[str]:
    """
    Resolve a canonical SCD / Rolling Heatmap row_key to its rule-engine family.

    Diagnostic-only. This reads the existing technical calculator metadata and
    falls back to ROW_CLASSIFICATION for display/catalog-backed family labels.
    """
    normalized_row_key = str(row_key).strip()
    if not normalized_row_key:
        return None

    try:
        optionc_meta = st.session_state.technical_calculator._get_optionc_meta()
        for meta in optionc_meta:
            if str(meta.get("display_key", "")).strip() == normalized_row_key:
                engine_indicator = str(meta.get("engine_indicator", "")).strip()
                return engine_indicator or None
    except Exception:
        pass

    fallback_family = ROW_CLASSIFICATION.get(normalized_row_key, {}).get("family")
    return str(fallback_family).strip() if fallback_family else None


def _run_scd_selected_family_scoring_diagnostic(
    *,
    matrix: Dict[str, Any],
    ticker: str,
    diagnostic_date_key: Any,
) -> Dict[str, Any]:
    """
    Compare the full current scoring path against selected-family scoring for
    one visible Single Indicator matrix cell.

    This diagnostic isolates scoring breadth only:
    - same 435-day Scenario B buffer
    - same numeric computation path
    - same existing rule-engine / rolling payload path
    - candidate passes indicators=[selected_engine_indicator]
    - no production refresh behavior changes
    """
    started_at = time.perf_counter()

    if not isinstance(matrix, dict) or matrix.get("view") != "single_indicator_time_series":
        raise ValueError("Selected-family scoring diagnostic requires a Single Indicator matrix.")

    selected_date_key = _normalize_scd_cache_date_value(diagnostic_date_key)
    if not selected_date_key:
        raise ValueError("Select a valid diagnostic date from the current matrix.")

    matrix_dates = [
        _normalize_scd_cache_date_value(date_key)
        for date_key in matrix.get("dates", [])
    ]
    matrix_dates = [date_key for date_key in matrix_dates if date_key]

    if selected_date_key not in matrix_dates:
        raise ValueError(
            f"Diagnostic date ({selected_date_key}) is not present "
            "in the current Single Indicator matrix."
        )

    tickers = _dedupe_preserve_order_str(matrix.get("tickers", []))
    normalized_ticker = str(ticker).strip().upper()
    if normalized_ticker not in tickers:
        raise ValueError(f"{normalized_ticker} is not in the current Single Indicator matrix.")

    row_key = str(matrix.get("row_key", "")).strip()
    engine_indicator = _get_scd_engine_indicator_for_row_key(row_key)
    if not engine_indicator:
        raise ValueError(f"Could not resolve engine indicator for row_key={row_key!r}.")

    window_days = int(matrix.get("window_days", len(matrix_dates) or 10))
    anchor_date = matrix.get("anchor_date")
    anchor_mode = str(matrix.get("anchor_mode", "asof"))

    reference = _build_scd_tail_diagnostic_cell(
        ticker=normalized_ticker,
        row_key=row_key,
        date_key=selected_date_key,
        window_days=window_days,
        anchor_date=anchor_date,
        anchor_mode=anchor_mode,
        historical_buffer_days=435,
        scoring_indicators=None,
    )

    candidate = _build_scd_tail_diagnostic_cell(
        ticker=normalized_ticker,
        row_key=row_key,
        date_key=selected_date_key,
        window_days=window_days,
        anchor_date=anchor_date,
        anchor_mode=anchor_mode,
        historical_buffer_days=435,
        scoring_indicators=[engine_indicator],
    )

    comparison = _compare_scd_tail_cells(
        reference_cell=reference["cell"],
        candidate_cell=candidate["cell"],
    )

    return {
        "status": "ok",
        "ticker": normalized_ticker,
        "row_key": row_key,
        "engine_indicator": engine_indicator,
        "date": selected_date_key,
        "reference_mode": "full_current_scoring",
        "candidate_mode": "selected_family_scoring",
        "reference_buffer_days": 435,
        "candidate_buffer_days": 435,
        "reference_seconds": reference["seconds"],
        "candidate_seconds": candidate["seconds"],
        "seconds_delta": round(reference["seconds"] - candidate["seconds"], 3),
        "reference_context_rows": reference["context_rows"],
        "candidate_context_rows": candidate["context_rows"],
        "reference_scoring_indicators": reference["scoring_indicators"],
        "candidate_scoring_indicators": candidate["scoring_indicators"],
        **comparison,
        "total_seconds": round(time.perf_counter() - started_at, 3),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }


def _get_scd_optionc_meta_for_row_key(row_key: str) -> Optional[Dict[str, Any]]:
    """
    Return the technical-calculator optionc_meta record for a canonical row_key.

    Diagnostic-only. This keeps selected-row diagnostics anchored to the same
    metadata source used by the existing rolling payload path.
    """
    normalized_row_key = str(row_key).strip()
    if not normalized_row_key:
        return None

    try:
        optionc_meta = st.session_state.technical_calculator._get_optionc_meta()
        for meta in optionc_meta:
            if str(meta.get("display_key", "")).strip() == normalized_row_key:
                return dict(meta)
    except Exception:
        return None

    return None


def _parse_scd_single_int_param_key(param_key: Any) -> int:
    """Parse a one-part numeric param_key such as '14' or 14."""
    raw = str(param_key).strip()
    if "_" in raw:
        raise ValueError(f"Expected a single integer param_key, got {raw!r}.")
    return int(raw)


def _build_scd_moving_average_compute_config(
    *,
    engine_indicator: str,
    length: int,
) -> Dict[str, Any]:
    """
    Build a diagnostic selected-row compute config for moving-average families.

    D3-D5 target families:
    - SMA: parameterized slope aliases, e.g. SMA_100_slope
    - EMA: parameterized slope aliases, e.g. EMA_20_slope
    - HMA: matching parameter-specific canonical slope plus ATR(14)
    - VWMA: matching parameter-specific canonical slope, SMA, and ATR(14)

    This helper intentionally preserves the existing preprocessor slope shape.
    It does not introduce formulas, scoring, persistence, or production behavior.
    """
    family = str(engine_indicator).strip().upper()
    length = int(length)

    if family not in {"SMA", "EMA", "HMA", "VWMA"}:
        raise ValueError(f"Unsupported moving-average family: {engine_indicator!r}.")

    base_lengths = [length]
    atrp_lengths = [] if family == "HMA" else [length]

    # VWMA rules use the matching parameter-specific canonical slope and
    # compare VWMA(n) with SMA(n). The selected-row refresh therefore needs
    # the requested VWMA plus the matching SMA period; it no longer depends
    # on the compatibility VWMA_slope alias anchored to VWMA(20).
    matching_sma_lengths: list[int] = []

    if family == "VWMA":
        matching_sma_lengths.append(length)

    base_lengths = sorted(set(base_lengths))
    atrp_lengths = sorted(set(atrp_lengths))

    config: Dict[str, Any] = {
        family: base_lengths,
        "ATR": sorted(set([*atrp_lengths, 14])),
        "ATRP": atrp_lengths,
        "SLOPE": {
            "window": 14,
            "method": "linreg",
            "emit_aliases": True,
            "vwma_anchor": 20,
            "hma_anchor": 21,
            "families": [family],
            "canonical_pattern": "{base_col}_slope__{method}_{window}",
            "compatibility_aliases": [
                "SMA_<len>_slope",
                "EMA_<len>_slope",
                "VWMA_slope",
                "HMA_slope",
            ],
        },
    }

    if matching_sma_lengths:
        config["SMA"] = sorted(set(matching_sma_lengths))

    return config


def _build_scd_selected_row_compute_config(row_key: str) -> Dict[str, Any]:
    """
    Build a minimal diagnostic compute config for one selected SCD row.

    D3-D2 started with RSI and SMA:
    - RSI_<len>: compute only RSI_<len>
    - SMA_<len>: compute SMA_<len>, ATR/ATRP_<len>, and SMA slope aliases

    D3-D4 expanded Tier 1 direct-family rows:
    - ROC_<len>
    - WILLR_<len> / Williams_R
    - CCI_<len>
    - MFI_<len>
    - CMF_<len>

    D3-D5 expands moving-average rows:
    - SMA_<len>
    - EMA_<len>
    - HMA_<len>
    - VWMA_<len>

    This is diagnostic-only. It does not alter production refresh behavior.
    """
    meta = _get_scd_optionc_meta_for_row_key(row_key)
    if not meta:
        raise ValueError(f"No optionc_meta record found for row_key={row_key!r}.")

    engine_indicator = str(meta.get("engine_indicator", "")).strip()
    param_key = str(meta.get("param_key", "")).strip()

    if engine_indicator == "RSI":
        length = _parse_scd_single_int_param_key(param_key)
        return {
            "RSI": [length],
        }

    if engine_indicator in {"SMA", "EMA", "HMA", "VWMA"}:
        length = _parse_scd_single_int_param_key(param_key)
        return _build_scd_moving_average_compute_config(
            engine_indicator=engine_indicator,
            length=length,
        )

    direct_single_length_config_keys = {
        "ROC": "ROC",
        "Williams_R": "WILLR",
        "CCI": "CCI",
        "MFI": "MFI",
        "CMF": "CMF",
    }

    if engine_indicator in direct_single_length_config_keys:
        length = _parse_scd_single_int_param_key(param_key)
        config_key = direct_single_length_config_keys[engine_indicator]
        return {
            config_key: [length],
        }

    raise ValueError(
        "D3-D5 selected-row numeric config diagnostic currently supports "
        "RSI, SMA, EMA, HMA, VWMA, ROC, Williams_R, CCI, MFI, and CMF rows only. "
        f"Got row_key={row_key!r}, engine_indicator={engine_indicator!r}."
    )


def _summarize_scd_compute_config(config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Return a compact diagnostic summary for a compute_config dict."""
    if not isinstance(config, dict):
        return {}

    summary: Dict[str, Any] = {}
    for key, value in config.items():
        if key == "SLOPE" and isinstance(value, dict):
            summary[key] = {
                "window": value.get("window"),
                "method": value.get("method"),
                "emit_aliases": value.get("emit_aliases"),
                "families": value.get("families"),
            }
        else:
            summary[key] = value

    return summary


def _fetch_scd_selected_row_refresh_bundle_for_ticker(
    *,
    ticker: str,
    row_key: str,
    window_days: int,
    anchor_date: Any,
    anchor_mode: str,
    requested_date_strings: list[str],
) -> Dict[str, Any]:
    """
    Fetch a selected-row SCD bundle for Single Indicator live-date refresh.

    Production use is intentionally narrow:
    - Single Indicator → Refresh today's cells only
    - supported selected-row families only
    - existing technical calculator / rule-engine path only
    - no formula, scoring, persistence, chart, heatmap, export, or DB changes

    Unsupported families raise and are handled by the caller's fallback path.
    """
    normalized_ticker = str(ticker).strip().upper()
    normalized_row_key = str(row_key).strip()

    if not normalized_ticker:
        raise ValueError("Ticker is required for selected-row refresh.")

    if not normalized_row_key:
        raise ValueError("row_key is required for selected-row refresh.")

    engine_indicator = _get_scd_engine_indicator_for_row_key(normalized_row_key)
    if not engine_indicator:
        raise ValueError(
            f"Could not resolve engine indicator for row_key={normalized_row_key!r}."
        )

    compute_config = _build_scd_selected_row_compute_config(normalized_row_key)

    bundle = st.session_state.technical_calculator.calculate_rule_engine_signals_optionc(
        ticker=normalized_ticker,
        feature_scope="heatmap",
        save_to_db=False,
        config=compute_config,
        indicators=[engine_indicator],
        use_meta_coverage=True,
        return_type="rolling_with_context",
        ohlcv_request=_get_scd_ohlcv_request(
            window_days=window_days,
            anchor_date=anchor_date,
            anchor_mode=anchor_mode,
            historical_buffer_days=435,
        ),
    )

    if not isinstance(bundle, dict):
        raise ValueError("Selected-row refresh did not return a valid bundle.")

    rolling_payload = bundle.get("rolling_payload")
    if not isinstance(rolling_payload, dict) or not rolling_payload:
        raise ValueError("Selected-row refresh returned no rolling payload.")

    available_dates = _extract_scd_dates_from_rolling_payload(rolling_payload)
    requested_dates = {
        normalized
        for normalized in (
            _normalize_scd_cache_date_value(value)
            for value in requested_date_strings
        )
        if normalized
    }

    missing_dates = sorted(requested_dates - available_dates)
    if missing_dates:
        raise ValueError(
            "Selected-row refresh payload is missing requested date(s): "
            + ", ".join(missing_dates)
        )

    selected_bundle = dict(bundle)
    selected_bundle["source"] = "selected_row_live_refresh"
    selected_bundle["selected_row_engine_indicator"] = engine_indicator
    selected_bundle["selected_row_compute_config"] = _summarize_scd_compute_config(
        compute_config
    )
    selected_bundle["selected_row_compute_config_keys"] = sorted(compute_config.keys())

    return selected_bundle


def _run_scd_selected_row_numeric_config_diagnostic(
    *,
    matrix: Dict[str, Any],
    ticker: str,
    diagnostic_date_key: Any,
) -> Dict[str, Any]:
    """
    Compare selected-family scoring with broad numeric computation against
    selected-family scoring with selected-row numeric computation.

    This isolates D3-D2's numeric-config question:
    - same 435-day Scenario B buffer
    - same selected-family scoring
    - reference uses current broad numeric config path
    - candidate uses minimal selected-row compute_config
    """
    started_at = time.perf_counter()

    if not isinstance(matrix, dict) or matrix.get("view") != "single_indicator_time_series":
        raise ValueError("Selected-row numeric config diagnostic requires a Single Indicator matrix.")

    selected_date_key = _normalize_scd_cache_date_value(diagnostic_date_key)
    if not selected_date_key:
        raise ValueError("Select a valid diagnostic date from the current matrix.")

    matrix_dates = [
        _normalize_scd_cache_date_value(date_key)
        for date_key in matrix.get("dates", [])
    ]
    matrix_dates = [date_key for date_key in matrix_dates if date_key]

    if selected_date_key not in matrix_dates:
        raise ValueError(
            f"Diagnostic date ({selected_date_key}) is not present "
            "in the current Single Indicator matrix."
        )

    tickers = _dedupe_preserve_order_str(matrix.get("tickers", []))
    normalized_ticker = str(ticker).strip().upper()
    if normalized_ticker not in tickers:
        raise ValueError(f"{normalized_ticker} is not in the current Single Indicator matrix.")

    row_key = str(matrix.get("row_key", "")).strip()
    engine_indicator = _get_scd_engine_indicator_for_row_key(row_key)
    if not engine_indicator:
        raise ValueError(f"Could not resolve engine indicator for row_key={row_key!r}.")

    selected_compute_config = _build_scd_selected_row_compute_config(row_key)

    window_days = int(matrix.get("window_days", len(matrix_dates) or 10))
    anchor_date = matrix.get("anchor_date")
    anchor_mode = str(matrix.get("anchor_mode", "asof"))

    reference = _build_scd_tail_diagnostic_cell(
        ticker=normalized_ticker,
        row_key=row_key,
        date_key=selected_date_key,
        window_days=window_days,
        anchor_date=anchor_date,
        anchor_mode=anchor_mode,
        historical_buffer_days=435,
        scoring_indicators=[engine_indicator],
        compute_config=None,
    )

    candidate = _build_scd_tail_diagnostic_cell(
        ticker=normalized_ticker,
        row_key=row_key,
        date_key=selected_date_key,
        window_days=window_days,
        anchor_date=anchor_date,
        anchor_mode=anchor_mode,
        historical_buffer_days=435,
        scoring_indicators=[engine_indicator],
        compute_config=selected_compute_config,
    )

    comparison = _compare_scd_tail_cells(
        reference_cell=reference["cell"],
        candidate_cell=candidate["cell"],
    )

    return {
        "status": "ok",
        "ticker": normalized_ticker,
        "row_key": row_key,
        "engine_indicator": engine_indicator,
        "date": selected_date_key,
        "reference_mode": "selected_family_scoring_broad_numeric",
        "candidate_mode": "selected_row_numeric_config",
        "reference_buffer_days": 435,
        "candidate_buffer_days": 435,
        "reference_seconds": reference["seconds"],
        "candidate_seconds": candidate["seconds"],
        "seconds_delta": round(reference["seconds"] - candidate["seconds"], 3),
        "reference_context_rows": reference["context_rows"],
        "candidate_context_rows": candidate["context_rows"],
        "reference_compute_config_keys": reference["compute_config_keys"],
        "candidate_compute_config_keys": candidate["compute_config_keys"],
        "candidate_compute_config": _summarize_scd_compute_config(selected_compute_config),
        "reference_scoring_indicators": reference["scoring_indicators"],
        "candidate_scoring_indicators": candidate["scoring_indicators"],
        **comparison,
        "total_seconds": round(time.perf_counter() - started_at, 3),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }


def _refresh_scd_single_indicator_live_date_cells(
    *,
    matrix: Dict[str, Any],
    refresh_scope: str = "selected_indicator",
) -> Dict[str, Any]:
    """
    Refresh today's visible Single Indicator cells in an existing matrix.

    Supported scopes:
    - selected_indicator:
        use selected-row computation for allowlisted/proven-safe families and
        fall back to the existing full bundle path for unsupported/error cases.
    - all_indicators:
        bypass selected-row computation and force the existing full bundle path
        so the shared today payload is refreshed for the selected ticker set.

    Preserved behavior:
    - splice only today's rebuilt date/ticker cell back into the current matrix

    Preserved:
    - historical matrix cells
    - selected row identity
    - selected ticker identity
    - chart/detail/export consumers of the matrix
    - existing rule-engine scoring semantics
    - existing non-persistence boundary
    """
    started_at = time.perf_counter()
    refresh_scope = str(refresh_scope or "selected_indicator").strip()
    if refresh_scope not in {"selected_indicator", "all_indicators"}:
        refresh_scope = "selected_indicator"

    if not isinstance(matrix, dict) or matrix.get("view") != "single_indicator_time_series":
        return matrix

    live_date_key = _get_scd_current_live_date_key()
    if not live_date_key:
        refreshed_matrix = dict(matrix)
        refreshed_matrix["last_live_refresh"] = {
            "status": "skipped",
            "message": "Today is not a US trading day.",
            "date": None,
            "refresh_scope": refresh_scope,
            "tickers_refreshed": [],
            "errors": [],
            "total_seconds": round(time.perf_counter() - started_at, 3),
        }
        return refreshed_matrix

    date_strings = [
        str(date_key)
        for date_key in matrix.get("dates", [])
        if str(date_key).strip()
    ]
    if live_date_key not in date_strings:
        refreshed_matrix = dict(matrix)
        refreshed_matrix["last_live_refresh"] = {
            "status": "skipped",
            "message": f"{live_date_key} is not in the current Single Indicator matrix.",
            "date": live_date_key,
            "refresh_scope": refresh_scope,
            "tickers_refreshed": [],
            "errors": [],
            "total_seconds": round(time.perf_counter() - started_at, 3),
        }
        return refreshed_matrix

    tickers = _dedupe_preserve_order_str(matrix.get("tickers", []))
    row_key = str(matrix.get("row_key", "")).strip()
    window_days = int(matrix.get("window_days", len(date_strings) or 10))
    anchor_date = matrix.get("anchor_date")
    anchor_mode = str(matrix.get("anchor_mode", "asof"))

    refreshed_matrix = dict(matrix)
    refreshed_matrix["cells"] = {
        str(date_key): dict(cells_by_ticker)
        for date_key, cells_by_ticker in dict(matrix.get("cells", {})).items()
    }
    refreshed_matrix["ticker_status"] = dict(matrix.get("ticker_status", {}))
    refreshed_matrix["profile"] = dict(matrix.get("profile", {}))
    refreshed_matrix["profile"]["tickers"] = dict(
        refreshed_matrix["profile"].get("tickers", {})
    )

    refresh_report = {
        "status": "ok",
        "date": live_date_key,
        "refresh_scope": refresh_scope,
        "tickers_refreshed": [],
        "selected_row_tickers": [],
        "fallback_tickers": [],
        "broad_refresh_tickers": [],
        "fallback_reasons": {},
        "errors": [],
        "total_seconds": None,
    }

    cache_stats = _get_scd_cache_stats()
    if refresh_scope == "selected_indicator":
        cache_stats["selected_row_refreshes"] += 1

    if live_date_key not in refreshed_matrix["cells"]:
        refreshed_matrix["cells"][live_date_key] = {}

    for ticker in tickers:
        ticker_started_at = time.perf_counter()

        try:
            fallback_reason = None

            if refresh_scope == "all_indicators":
                refresh_path = "full_refresh"
                refresh_report["broad_refresh_tickers"].append(ticker)

                bundle = _fetch_scd_rolling_bundle_for_ticker(
                    ticker=ticker,
                    window_days=window_days,
                    force_refresh=True,
                    anchor_date=anchor_date,
                    anchor_mode=anchor_mode,
                    requested_date_strings=[live_date_key],
                )
            else:
                refresh_path = "selected_row"

                try:
                    bundle = _fetch_scd_selected_row_refresh_bundle_for_ticker(
                        ticker=ticker,
                        row_key=row_key,
                        window_days=window_days,
                        anchor_date=anchor_date,
                        anchor_mode=anchor_mode,
                        requested_date_strings=[live_date_key],
                    )
                except Exception as selected_row_error:
                    refresh_path = "full_fallback"
                    fallback_reason = str(selected_row_error)

                    cache_stats["selected_row_refresh_fallbacks"] += 1
                    refresh_report["fallback_tickers"].append(ticker)
                    refresh_report["fallback_reasons"][ticker] = fallback_reason

                    bundle = _fetch_scd_rolling_bundle_for_ticker(
                        ticker=ticker,
                        window_days=window_days,
                        force_refresh=True,
                        anchor_date=anchor_date,
                        anchor_mode=anchor_mode,
                        requested_date_strings=[live_date_key],
                    )

            rolling_payload = bundle.get("rolling_payload") if isinstance(bundle, dict) else {}
            context_df = bundle.get("indicator_context_df") if isinstance(bundle, dict) else None
            bundle_source = bundle.get("source") if isinstance(bundle, dict) else "invalid_bundle"

            if not isinstance(rolling_payload, dict) or not rolling_payload:
                raise ValueError("No rolling payload returned during live-date refresh.")

            adapter_lookup = _build_scd_adapter_lookup(
                rolling_payload=rolling_payload,
                row_keys=[row_key],
                ohlcv_df=context_df,
            )

            refreshed_cell = _build_scd_single_indicator_cell_from_bundle(
                ticker=ticker,
                row_key=row_key,
                date_key=live_date_key,
                rolling_payload=rolling_payload,
                adapter_lookup=adapter_lookup,
                context_df=context_df,
            )

            refreshed_matrix["cells"][live_date_key][ticker] = refreshed_cell

            if refresh_path == "selected_row":
                cache_stats["selected_row_refresh_tickers"] += 1
                refresh_report["selected_row_tickers"].append(ticker)

            existing_status = dict(refreshed_matrix["ticker_status"].get(ticker, {}))
            existing_status.update(
                {
                    "live_refresh_status": refreshed_cell.get("status", "unknown"),
                    "live_refresh_date": live_date_key,
                    "live_refresh_bundle_source": bundle_source,
                    "live_refresh_path": refresh_path,
                    "live_refresh_seconds": round(
                        time.perf_counter() - ticker_started_at,
                        3,
                    ),
                }
            )

            if fallback_reason:
                existing_status["live_refresh_fallback_reason"] = fallback_reason
            else:
                existing_status.pop("live_refresh_fallback_reason", None)

            refreshed_matrix["ticker_status"][ticker] = existing_status
            refresh_report["tickers_refreshed"].append(ticker)

        except Exception as e:
            message = f"{ticker}: {e}"
            refresh_report["errors"].append(message)
            cache_stats["selected_row_refresh_errors"] += 1

            existing_status = dict(refreshed_matrix["ticker_status"].get(ticker, {}))
            existing_status.update(
                {
                    "live_refresh_status": "error",
                    "live_refresh_date": live_date_key,
                    "live_refresh_error": message,
                    "live_refresh_path": "error",
                    "live_refresh_seconds": round(
                        time.perf_counter() - ticker_started_at,
                        3,
                    ),
                }
            )
            refreshed_matrix["ticker_status"][ticker] = existing_status

    if refresh_report["errors"]:
        refresh_report["status"] = (
            "partial"
            if refresh_report["tickers_refreshed"]
            else "error"
        )

    as_of_dt = datetime.now()
    refresh_report["total_seconds"] = round(time.perf_counter() - started_at, 3)
    refresh_report["as_of"] = as_of_dt.isoformat(timespec="seconds")
    refresh_report["as_of_label"] = _format_scd_live_as_of_label(as_of_dt)

    _mark_scd_live_cells_as_of(
        matrix=refreshed_matrix,
        date_key=live_date_key,
        as_of=as_of_dt,
        source="single_indicator_today_refresh",
    )

    refreshed_matrix["last_live_refresh"] = refresh_report
    refreshed_matrix["profile"]["last_live_refresh"] = refresh_report

    return refreshed_matrix


def _build_scd_single_indicator_time_series_matrix(
    *,
    selected_tickers: list[str],
    selected_row_key: str,
    date_request: Dict[str, Any],
    force_refresh: bool = False,
) -> Dict[str, Any]:
    """
    Build the SCD Single Indicator time-series matrix.

    Shape:
        matrix["cells"][date_key][ticker] = existing Rolling Heatmap cell

    This function reshapes existing rolling payload cells only. It does not
    compute new scores, rank tickers, aggregate signals, or reinterpret meaning.
    """
    tickers = _dedupe_preserve_order_str(selected_tickers)
    row_key = str(selected_row_key).strip()

    date_strings = [
        str(date_key)
        for date_key in date_request.get("date_strings", [])
        if str(date_key).strip()
    ]

    window_days = int(date_request.get("trading_days", len(date_strings) or 10))
    anchor_date = date_request.get("anchor_date")
    anchor_mode = str(date_request.get("scenario_b_anchor_mode", "asof"))

    profile_started_at = time.perf_counter()
    live_as_of_candidates: list[Any] = []

    matrix = {
        "status": "ok",
        "view": "single_indicator_time_series",
        "window_days": window_days,
        "anchor_mode": anchor_mode,
        "anchor_date": anchor_date,
        "window_start_date": date_request.get("window_start_date"),
        "window_end_date": date_request.get("window_end_date"),
        "tickers": tickers,
        "row_key": row_key,
        "row_label": _format_scd_indicator_display_label(row_key),
        "dates": date_strings,
        "cells": {date_key: {} for date_key in date_strings},
        "ticker_status": {},
        "errors": [],
        "profile": {
            "ticker_count": len(tickers),
            "date_count": len(date_strings),
            "row_key": row_key,
            "anchor_date": str(anchor_date),
            "anchor_mode": anchor_mode,
            "total_seconds": None,
            "tickers": {},
        },
    }

    if not tickers:
        matrix["status"] = "empty"
        matrix["errors"].append("No SCD tickers selected.")
        matrix["profile"]["total_seconds"] = round(time.perf_counter() - profile_started_at, 3)
        return matrix

    if not row_key:
        matrix["status"] = "empty"
        matrix["errors"].append("No Single Indicator row key selected.")
        matrix["profile"]["total_seconds"] = round(time.perf_counter() - profile_started_at, 3)
        return matrix

    if not date_strings:
        matrix["status"] = "empty"
        matrix["errors"].append("No Single Indicator dates resolved.")
        matrix["profile"]["total_seconds"] = round(time.perf_counter() - profile_started_at, 3)
        return matrix

    for ticker in tickers:
        ticker_started_at = time.perf_counter()
        ticker_profile = {
            "rolling_payload_seconds": None,
            "hover_context_seconds": None,
            "adapter_lookup_seconds": None,
            "cell_extraction_seconds": None,
            "total_seconds": None,
            "status": "started",
        }
        matrix["profile"]["tickers"][ticker] = ticker_profile

        completed_date_strings = [
            date_key
            for date_key in date_strings
            if _is_scd_completed_cache_date(date_key)
        ]

        cached_cells: Dict[tuple[str, str], Dict[str, Any]] = {}
        missing_cells: list[tuple[str, str]] = []
        fetch_requested_date_strings = list(date_strings)

        if not force_refresh and completed_date_strings:
            cached_cells, missing_cells = _load_completed_result_cells_for_ticker(
                ticker=ticker,
                row_keys=[row_key],
                date_keys=completed_date_strings,
            )

            if cached_cells:
                for (cached_row_key, cached_date_key), cached_cell in cached_cells.items():
                    if cached_row_key != row_key:
                        continue
                    matrix["cells"][cached_date_key][ticker] = cached_cell

                _get_scd_cache_stats()["result_cell_hits"] += len(cached_cells)

            if missing_cells:
                _get_scd_cache_stats()["result_cell_misses"] += len(missing_cells)

            if not missing_cells and len(completed_date_strings) == len(date_strings):
                stats = _get_scd_cache_stats()
                stats["ticker_calculations_skipped"] += 1

                matrix["ticker_status"][ticker] = {
                    "status": "result_cell_cache",
                    "message": "All requested completed historical cells reused.",
                    "bundle_source": "result_cell_cache",
                    "missing_cells": 0,
                }

                ticker_profile["rolling_payload_seconds"] = 0.0
                ticker_profile["hover_context_seconds"] = 0.0
                ticker_profile["adapter_lookup_seconds"] = 0.0
                ticker_profile["cell_extraction_seconds"] = 0.0
                ticker_profile["bundle_source"] = "result_cell_cache"
                ticker_profile["status"] = "result_cell_cache"
                ticker_profile["total_seconds"] = round(
                    time.perf_counter() - ticker_started_at,
                    3,
                )
                continue

            cached_date_strings = {
                cached_date_key
                for (_, cached_date_key) in cached_cells.keys()
            }
            fetch_requested_date_strings = [
                date_key
                for date_key in date_strings
                if _normalize_scd_cache_date_value(date_key) not in cached_date_strings
            ]

        try:
            stage_started_at = time.perf_counter()
            bundle = _fetch_scd_rolling_bundle_for_ticker(
                ticker=ticker,
                window_days=window_days,
                force_refresh=force_refresh,
                anchor_date=anchor_date,
                anchor_mode=anchor_mode,
                requested_date_strings=fetch_requested_date_strings,
            )
            ticker_profile["rolling_payload_seconds"] = round(
                time.perf_counter() - stage_started_at,
                3,
            )

            rolling_payload = bundle.get("rolling_payload") if isinstance(bundle, dict) else {}
            hover_ohlcv_df = bundle.get("indicator_context_df") if isinstance(bundle, dict) else None
            bundle_source = bundle.get("source") if isinstance(bundle, dict) else "invalid_bundle"
            bundle_as_of = bundle.get("cache_as_of") if isinstance(bundle, dict) else None

            if bundle_as_of is not None:
                live_as_of_candidates.append(bundle_as_of)
                ticker_profile["bundle_as_of"] = str(bundle_as_of)

            ticker_profile["hover_context_seconds"] = 0.0
            ticker_profile["bundle_source"] = bundle_source

            if not isinstance(rolling_payload, dict) or not rolling_payload:
                matrix["ticker_status"][ticker] = {
                    "status": "empty",
                    "message": "No rolling payload returned.",
                    "bundle_source": bundle_source,
                }
                for date_key in date_strings:
                    normalized_date = _normalize_scd_cache_date_value(date_key)
                    if (row_key, normalized_date) in cached_cells:
                        matrix["cells"][date_key][ticker] = cached_cells[
                            (row_key, normalized_date)
                        ]
                        continue

                    matrix["cells"][date_key][ticker] = {
                        "ticker": ticker,
                        "row_key": row_key,
                        "date": date_key,
                        "value": None,
                        "signal": None,
                        "score": None,
                        "hover": f"No rolling payload returned for {ticker}.",
                        "status": "missing_payload",
                        "display_text": "missing_payload",
                    }
                ticker_profile["status"] = "missing_payload"
                continue

            stage_started_at = time.perf_counter()
            adapter_lookup = _build_scd_adapter_lookup(
                rolling_payload=rolling_payload,
                row_keys=[row_key],
                ohlcv_df=hover_ohlcv_df,
            )
            ticker_profile["adapter_lookup_seconds"] = round(
                time.perf_counter() - stage_started_at,
                3,
            )

            stage_started_at = time.perf_counter()
            missing_count = 0

            for date_key in date_strings:
                normalized_date = _normalize_scd_cache_date_value(date_key)
                if (row_key, normalized_date) in cached_cells:
                    cell = cached_cells[(row_key, normalized_date)]
                else:
                    cell = _build_scd_single_indicator_cell_from_bundle(
                        ticker=ticker,
                        row_key=row_key,
                        date_key=date_key,
                        rolling_payload=rolling_payload,
                        adapter_lookup=adapter_lookup,
                        context_df=hover_ohlcv_df,
                    )

                if cell.get("status") != "ok":
                    missing_count += 1
                matrix["cells"][date_key][ticker] = cell

            ticker_profile["cell_extraction_seconds"] = round(
                time.perf_counter() - stage_started_at,
                3,
            )

            matrix["ticker_status"][ticker] = {
                "status": "ok" if missing_count == 0 else "partial",
                "message": (
                    "All requested dates available."
                    if missing_count == 0
                    else f"{missing_count} requested date(s) missing."
                ),
                "bundle_source": bundle_source,
                "missing_cells": missing_count,
            }
            ticker_profile["status"] = matrix["ticker_status"][ticker]["status"]

        except Exception as e:
            message = f"{ticker}: {e}"
            matrix["errors"].append(message)
            matrix["ticker_status"][ticker] = {
                "status": "error",
                "message": message,
            }
            for date_key in date_strings:
                matrix["cells"][date_key][ticker] = {
                    "ticker": ticker,
                    "row_key": row_key,
                    "date": date_key,
                    "value": None,
                    "signal": None,
                    "score": None,
                    "hover": message,
                    "status": "error",
                    "display_text": "error",
                }
            ticker_profile["status"] = "error"

        finally:
            ticker_profile["total_seconds"] = round(
                time.perf_counter() - ticker_started_at,
                3,
            )

    matrix["profile"]["total_seconds"] = round(
        time.perf_counter() - profile_started_at,
        3,
    )

    live_date_key = _get_scd_current_live_date_key()
    if live_date_key and live_date_key in date_strings:
        live_as_of_values = []
        for candidate in live_as_of_candidates:
            try:
                ts = pd.Timestamp(candidate)
                if pd.isna(ts):
                    continue
                if ts.tzinfo is not None:
                    ts = ts.tz_localize(None)
                live_as_of_values.append(ts)
            except Exception:
                continue

        live_as_of = min(live_as_of_values) if live_as_of_values else datetime.now()

        _mark_scd_live_cells_as_of(
            matrix=matrix,
            date_key=live_date_key,
            as_of=live_as_of,
            source="single_indicator_build",
        )

    result_cell_writes = _store_scd_result_cells_from_matrix(
        matrix=matrix,
        source="single_indicator_build",
    )
    matrix["profile"]["result_cell_writes"] = result_cell_writes

    if matrix["errors"]:
        matrix["status"] = "partial"

    return matrix


def _build_scd_cross_sectional_matrix(
    *,
    selected_tickers: list[str],
    selected_row_keys: list[str],
    window_days: int = 10,
    force_refresh: bool = False,
    anchor_date: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Build the SCD latest-cell cross-sectional matrix.

    Shape:
        matrix["cells"][row_key][ticker] = latest existing Rolling Heatmap cell

    This function reshapes existing rolling payload cells only. It does not
    compute new scores, rank tickers, aggregate signals, or reinterpret meaning.
    """
    tickers = _dedupe_preserve_order_str(selected_tickers)
    selected_row_keys_clean = [
        str(row_key).strip()
        for row_key in selected_row_keys
        if str(row_key).strip()
    ]

    row_keys = ["__PRICE__"] + [
        row_key for row_key in selected_row_keys_clean
        if row_key != "__PRICE__"
    ]

    target_date_key = _resolve_scd_cross_sectional_target_date_key(anchor_date)

    profile_started_at = time.perf_counter()
    live_as_of_candidates: list[Any] = []

    matrix = {
        "status": "ok",
        "window_days": int(window_days),
        "anchor_mode": "asof",
        "anchor_date": anchor_date,
        "target_date": target_date_key,
        "tickers": tickers,
        "row_keys": row_keys,
        "cells": {row_key: {} for row_key in row_keys},
        "ticker_status": {},
        "errors": [],
        "profile": {
            "ticker_count": len(tickers),
            "row_count": len(row_keys),
            "anchor_date": str(anchor_date),
            "target_date": target_date_key,
            "total_seconds": None,
            "tickers": {},
        },
    }

    if not tickers:
        matrix["status"] = "empty"
        matrix["errors"].append("No SCD tickers selected.")
        matrix["profile"]["total_seconds"] = round(time.perf_counter() - profile_started_at, 3)
        return matrix

    if not selected_row_keys_clean:
        matrix["status"] = "empty"
        matrix["errors"].append("No SCD indicator row keys selected.")
        matrix["profile"]["total_seconds"] = round(time.perf_counter() - profile_started_at, 3)
        return matrix

    for ticker in tickers:
        ticker_started_at = time.perf_counter()
        ticker_profile = {
            "rolling_payload_seconds": None,
            "hover_context_seconds": None,
            "adapter_lookup_seconds": None,
            "latest_cell_extraction_seconds": None,
            "total_seconds": None,
            "status": "started",
        }
        matrix["profile"]["tickers"][ticker] = ticker_profile

        target_date_completed = (
            bool(target_date_key)
            and _is_scd_completed_cache_date(target_date_key)
        )

        cached_cells: Dict[tuple[str, str], Dict[str, Any]] = {}
        missing_cells: list[tuple[str, str]] = []

        if not force_refresh and target_date_completed:
            cached_cells, missing_cells = _load_completed_result_cells_for_ticker(
                ticker=ticker,
                row_keys=row_keys,
                date_keys=[target_date_key],
            )

            if cached_cells:
                normalized_target_date = _normalize_scd_cache_date_value(target_date_key)
                for row_key in row_keys:
                    cached_cell = cached_cells.get((row_key, normalized_target_date))
                    if cached_cell is None:
                        continue
                    matrix["cells"][row_key][ticker] = cached_cell

                _get_scd_cache_stats()["result_cell_hits"] += len(cached_cells)

            if missing_cells:
                _get_scd_cache_stats()["result_cell_misses"] += len(missing_cells)

            if not missing_cells:
                stats = _get_scd_cache_stats()
                stats["ticker_calculations_skipped"] += 1

                matrix["ticker_status"][ticker] = {
                    "status": "result_cell_cache",
                    "message": "All requested completed historical cells reused.",
                    "target_date": target_date_key,
                    "bundle_source": "result_cell_cache",
                }

                ticker_profile["rolling_payload_seconds"] = 0.0
                ticker_profile["hover_context_seconds"] = 0.0
                ticker_profile["adapter_lookup_seconds"] = 0.0
                ticker_profile["latest_cell_extraction_seconds"] = 0.0
                ticker_profile["bundle_source"] = "result_cell_cache"
                ticker_profile["status"] = "result_cell_cache"
                ticker_profile["total_seconds"] = round(
                    time.perf_counter() - ticker_started_at,
                    3,
                )
                continue

        try:
            stage_started_at = time.perf_counter()

            requested_date_strings = [target_date_key] if target_date_key else []

            bundle = _fetch_scd_rolling_bundle_for_ticker(
                ticker=ticker,
                window_days=window_days,
                force_refresh=force_refresh,
                anchor_date=anchor_date,
                requested_date_strings=requested_date_strings,
            )
            ticker_profile["rolling_payload_seconds"] = round(
                time.perf_counter() - stage_started_at,
                3,
            )

            rolling_payload = bundle.get("rolling_payload") if isinstance(bundle, dict) else {}
            hover_ohlcv_df = bundle.get("indicator_context_df") if isinstance(bundle, dict) else None
            bundle_source = bundle.get("source") if isinstance(bundle, dict) else "invalid_bundle"
            bundle_as_of = bundle.get("cache_as_of") if isinstance(bundle, dict) else None

            if bundle_as_of is not None:
                live_as_of_candidates.append(bundle_as_of)
                ticker_profile["bundle_as_of"] = str(bundle_as_of)

            # Hover/context is now supplied by the same technical-layer pass as
            # the rolling payload. There is no separate hover fetch in the
            # normal bundled cold path.
            ticker_profile["hover_context_seconds"] = 0.0
            ticker_profile["bundle_source"] = bundle_source

            if not isinstance(rolling_payload, dict) or not rolling_payload:
                matrix["ticker_status"][ticker] = {
                    "status": "empty",
                    "message": "No rolling payload returned.",
                    "bundle_source": bundle_source,
                }
                normalized_target_date = _normalize_scd_cache_date_value(target_date_key)
                for row_key in row_keys:
                    if (row_key, normalized_target_date) in cached_cells:
                        matrix["cells"][row_key][ticker] = cached_cells[
                            (row_key, normalized_target_date)
                        ]
                        continue

                    matrix["cells"][row_key][ticker] = {
                        "ticker": ticker,
                        "row_key": row_key,
                        "date": None,
                        "value": None,
                        "signal": None,
                        "score": None,
                        "hover": f"No rolling payload returned for {ticker}.",
                        "status": "missing_payload",
                        "display_text": "missing_payload",
                    }
                ticker_profile["status"] = "missing_payload"
                ticker_profile["total_seconds"] = round(
                    time.perf_counter() - ticker_started_at,
                    3,
                )
                continue

            payload_status = rolling_payload.get("status", "unknown")
            payload_dates = list(rolling_payload.get("dates", []))

            matrix["ticker_status"][ticker] = {
                "status": payload_status,
                "dates": payload_dates,
                "latest_date": payload_dates[-1] if payload_dates else None,
                "target_date": target_date_key,
                "bundle_source": bundle_source,
                "has_indicator_context": (
                    isinstance(hover_ohlcv_df, pd.DataFrame)
                    and not hover_ohlcv_df.empty
                ),
            }

            stage_started_at = time.perf_counter()
            adapter_lookup = _build_scd_adapter_lookup(
                rolling_payload=rolling_payload,
                row_keys=selected_row_keys_clean,
                ohlcv_df=hover_ohlcv_df,
            )
            ticker_profile["adapter_lookup_seconds"] = round(
                time.perf_counter() - stage_started_at,
                3,
            )

            stage_started_at = time.perf_counter()
            normalized_target_date = _normalize_scd_cache_date_value(target_date_key)

            for row_key in row_keys:
                if target_date_key and (row_key, normalized_target_date) in cached_cells:
                    matrix["cells"][row_key][ticker] = cached_cells[
                        (row_key, normalized_target_date)
                    ]
                elif target_date_key:
                    matrix["cells"][row_key][ticker] = _extract_scd_cell_for_date(
                        ticker=ticker,
                        row_key=row_key,
                        date_key=target_date_key,
                        rolling_payload=rolling_payload,
                        adapter_lookup=adapter_lookup,
                    )
                else:
                    matrix["cells"][row_key][ticker] = _extract_latest_scd_cell(
                        ticker=ticker,
                        row_key=row_key,
                        rolling_payload=rolling_payload,
                        adapter_lookup=adapter_lookup,
                    )
            ticker_profile["latest_cell_extraction_seconds"] = round(
                time.perf_counter() - stage_started_at,
                3,
            )
            ticker_profile["status"] = "ok"
            ticker_profile["total_seconds"] = round(
                time.perf_counter() - ticker_started_at,
                3,
            )

        except Exception as e:
            message = f"{ticker}: {e}"
            matrix["errors"].append(message)
            matrix["ticker_status"][ticker] = {
                "status": "error",
                "message": str(e),
            }

            for row_key in row_keys:
                matrix["cells"][row_key][ticker] = {
                    "ticker": ticker,
                    "row_key": row_key,
                    "date": None,
                    "value": None,
                    "signal": None,
                    "score": None,
                    "hover": message,
                    "status": "error",
                    "display_text": "error",
                }

            ticker_profile["status"] = "error"
            ticker_profile["total_seconds"] = round(
                time.perf_counter() - ticker_started_at,
                3,
            )

    matrix["profile"]["total_seconds"] = round(
        time.perf_counter() - profile_started_at,
        3,
    )

    live_date_key = _get_scd_current_live_date_key()
    if (
        target_date_key
        and live_date_key
        and _normalize_scd_cache_date_value(target_date_key) == live_date_key
    ):
        live_as_of_values = []
        for candidate in live_as_of_candidates:
            try:
                ts = pd.Timestamp(candidate)
                if pd.isna(ts):
                    continue
                if ts.tzinfo is not None:
                    ts = ts.tz_localize(None)
                live_as_of_values.append(ts)
            except Exception:
                continue

        live_as_of = min(live_as_of_values) if live_as_of_values else datetime.now()

        _mark_scd_live_cells_as_of(
            matrix=matrix,
            date_key=live_date_key,
            as_of=live_as_of,
            source="multiple_indicators_build",
        )

    result_cell_writes = _store_scd_result_cells_from_matrix(
        matrix=matrix,
        source="multiple_indicators_build",
    )
    matrix["profile"]["result_cell_writes"] = result_cell_writes

    return matrix


def _get_scd_row_display_name(row_key: str):
    """
    Return the adapter-owned display label for a canonical SCD row_key.
    """
    if row_key == "__PRICE__":
        return "Price"

    row_def = INDICATOR_DEFS.get(row_key, {})
    return row_def.get("display_name", row_key)


def _format_scd_heatmap_text(row_key: str, cell: Dict[str, Any]) -> str:
    """
    Return adapter-produced in-cell text.

    SCD does not append signal labels below values. The Rolling Heatmap adapter
    owns cell display formatting.
    """
    if cell.get("status") != "ok":
        return str(cell.get("status", ""))

    display_text = cell.get("display_text")
    if display_text:
        return str(display_text)

    value = cell.get("value")
    if value is None:
        return ""

    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return str(value)


def _build_scd_hover_customdata(
    *,
    ticker: str,
    row_key: str,
    cell: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build SCD heatmap customdata from adapter-owned hover fields.

    The adapter supplies the Rolling Signal Heatmap hover contract. SCD adds
    only cross-sectional identity and the original raw payload hover line.
    """
    adapter_cd = cell.get("adapter_customdata")
    custom = dict(adapter_cd) if isinstance(adapter_cd, dict) else {}

    custom.setdefault("indicator_key", row_key)
    custom.setdefault("display_name", _get_scd_row_display_name(row_key))
    custom.setdefault("date", cell.get("date"))
    custom.setdefault("raw_value", cell.get("value"))
    custom.setdefault("formatted_value", cell.get("display_text") or "")
    custom.setdefault("score", cell.get("score"))
    custom.setdefault("score_label", cell.get("signal"))
    custom.setdefault("value_label", "Value")

    for key in [
        "ma_context_block",
        "vwma_post_signal_block",
        "crossover_context_block",
        "crossover_summary_block",
        "delta_abs_fmt",
        "delta_pct_suffix",
        "delta_line",
        "trend_line",
        "bb_bw_context_block",
        "alignment_line",
        "adx_context_block",
        "signal_line",
        "bbp_exhaustion_context_block",
        "macd_context_block",
        "stoch_context_block",
        "dpo_context_block",
        "bullbear_context_block",
        "cci_context_block",
        "uo_context_block",
        "rule_block",
        "notes_block",
        "definition_block",
        "how_to_read_block",
        "band_context_block",
        "volume_block",
        "volume_vs_avg_block",
    ]:
        custom.setdefault(key, "")

    if not custom.get("delta_line") and not _is_scd_crossover_event_row(row_key):
        custom["delta_line"] = (
            f"Δ vs prior day: {custom.get('delta_abs_fmt', '')}"
            f"{custom.get('delta_pct_suffix', '')}<br>"
        )

    if _is_scd_crossover_event_row(row_key) and custom.get("crossover_summary_block"):
        custom["scd_value_line"] = ""
    else:
        custom["scd_value_line"] = (
            f"{custom.get('value_label', 'Value')}: "
            f"{custom.get('formatted_value', '')}<br>"
        )

    custom.setdefault("scd_single_value_line", custom["scd_value_line"])
    custom["ticker"] = ticker
    custom["row_key"] = row_key
    custom["status"] = cell.get("status")

    payload_hover = cell.get("hover")

    payload_hover = cell.get("hover")

    # Bollinger, Bull/Bear Power, VWMA, HMA, and UO rows already expose
    # their user-facing information through structured adapter hover fields.
    # Suppress the redundant raw payload summary in SCD so diagnostic-style
    # payload text does not duplicate structured context or dominate hover
    # geometry.
    if (
        row_key in {
            "BB_PCT_B_ST",
            "BB_PCT_B",
            "BB_PCT_B_LT",
            "BB_BW_ST",
            "BB_BW",
            "BB_BW_LT",
        }
        or row_key.startswith("BullBearPower_")
        or row_key.startswith("BBP_DOWNSIDE_EXHAUSTION_")
        or row_key.startswith("VWMA_")
        or row_key.startswith("HMA_")
        or row_key.startswith("UO_")
    ):
        custom["scd_payload_hover_block"] = ""
    else:
        custom["scd_payload_hover_block"] = (
            f"<br>{payload_hover}" if payload_hover else ""
        )

    return custom

def _build_scd_heatmap_figure(matrix: Dict[str, Any]) -> go.Figure:
    """
    Build the SCD Plotly Heatmap View from the already-built SCD matrix.
    """
    tickers = list(matrix.get("tickers", []))
    row_keys = list(matrix.get("row_keys", []))
    cells = matrix.get("cells", {})

    y_labels = [_get_scd_row_display_name(row_key) for row_key in row_keys]
    z = []
    text = []
    customdata = []

    for row_key in row_keys:
        z_row = []
        text_row = []
        custom_row = []

        for ticker in tickers:
            cell = cells.get(row_key, {}).get(ticker, {})
            score = cell.get("score")

            try:
                z_row.append(float(score) if score is not None else None)
            except (TypeError, ValueError):
                z_row.append(None)

            text_row.append(
                _format_scd_heatmap_text(
                    row_key,
                    cell,
                )
            )

            custom = (
                _build_scd_hover_customdata(
                    ticker=ticker,
                    row_key=row_key,
                    cell=cell,
                )
            )

            if str(row_key).startswith(
                "VWMA_"
            ):
                price_cell = (
                    cells
                    .get("__PRICE__", {})
                    .get(ticker, {})
                )

                price_customdata = {}

                if isinstance(
                    price_cell,
                    dict,
                ):
                    maybe_price_customdata = (
                        price_cell.get(
                            "adapter_customdata"
                        )
                    )

                    same_date = (
                        str(
                            price_cell.get(
                                "date",
                                "",
                            )
                        )
                        == str(
                            cell.get(
                                "date",
                                "",
                            )
                        )
                    )

                    if (
                        same_date
                        and isinstance(
                            maybe_price_customdata,
                            dict,
                        )
                    ):
                        price_customdata = (
                            maybe_price_customdata
                        )

                vwma_opening = (
                    build_vwma_hover_opening(
                        custom,
                        price_customdata,
                    )
                )

                custom[
                    "formatted_value"
                ] = vwma_opening[
                    "formatted_value"
                ]

                custom[
                    "scd_value_line"
                ] = (
                    "Value: "
                    f"{vwma_opening['formatted_value']}"
                    "<br>"
                )

                custom[
                    "delta_line"
                ] = vwma_opening[
                    "delta_line"
                ]

                custom[
                    "trend_line"
                ] = vwma_opening[
                    "trend_line"
                ]

            custom_row.append(custom)

        z.append(z_row)
        text.append(text_row)
        customdata.append(custom_row)

    colorscale = [
        [0.0, "#8B0000"],   # strong sell
        [0.25, "#CD5C5C"],  # sell
        [0.5, "#D3D3D3"],   # neutral
        [0.75, "#90EE90"],  # buy
        [1.0, "#006400"],   # strong buy
    ]

    hovertemplate = (
        "<b>%{customdata.display_name}</b><br>"
        "Ticker: %{customdata.ticker}<br>"
        "Date: %{customdata.date}<br>"
        "<br>"
        "%{customdata.scd_value_line}"
        "%{customdata.crossover_summary_block}"
        "%{customdata.crossover_context_block}"
        "%{customdata.delta_line}"
        "%{customdata.trend_line}"
        "%{customdata.bb_bw_context_block}"
        "%{customdata.alignment_line}"
        "%{customdata.ma_context_block}"
        "%{customdata.adx_context_block}"
        "%{customdata.uo_context_block}"
        "%{customdata.signal_line}"
        "%{customdata.hma_post_signal_block}"
        "%{customdata.vwma_post_signal_block}"
        "%{customdata.cci_context_block}"
        "%{customdata.bbp_exhaustion_context_block}"
        "%{customdata.macd_context_block}"
        "%{customdata.stoch_context_block}"
        "%{customdata.cmf_context_block}"
        "%{customdata.dpo_context_block}"
        "%{customdata.bullbear_context_block}"
        "%{customdata.rule_block}"
        "%{customdata.notes_block}"
        "%{customdata.definition_block}"
        "%{customdata.how_to_read_block}"
        "%{customdata.band_context_block}"
        "%{customdata.volume_block}"
        "%{customdata.volume_vs_avg_block}"
        "%{customdata.scd_payload_hover_block}"
        "<extra></extra>"
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=tickers,
            y=y_labels,
            text=text,
            texttemplate="%{text}",
            customdata=customdata,
            colorscale=colorscale,
            zmin=-2,
            zmax=2,
            hovertemplate=hovertemplate,
            colorbar=dict(title="Score"),
        )
    )

    apply_bbp_divergence_text_overlay(
        fig,
        text=text,
        customdata=customdata,
        x=tickers,
        y=y_labels,
    )

    apply_cci_divergence_text_overlay(
        fig,
        text=text,
        customdata=customdata,
        x=tickers,
        y=y_labels,
    )

    apply_uo_divergence_symbol_overlay(
        fig,
        customdata=customdata,
        x=tickers,
        y=y_labels,
    )

    apply_hma_turn_text_overlay(
        fig,
        text=text,
        customdata=customdata,
        x=tickers,
        y=y_labels,
    )

    apply_vwma_volume_extreme_text_overlay(
        fig,
        text=text,
        customdata=customdata,
        x=tickers,
        y=y_labels,
    )

    row_count = max(len(y_labels), 1)
    base_height = 30 * row_count + 160

    # Preserve the compact 450px layout for very small matrices, then add
    # vertical hover clearance as row density increases. The supplemental
    # allowance is capped at the ten-row level; normal row-based scaling
    # takes over once it becomes larger.
    hover_clearance_height = (
        450
        + 15 * max(min(row_count, 10) - 3, 0)
    )
    dynamic_height = max(
        450,
        base_height,
        hover_clearance_height,
    )

    # Price plus exactly three indicator rows is a narrow Plotly placement
    # boundary for detailed first-row hover labels. Add a modest allowance
    # only for that layout; one-, two-, and larger-indicator matrices retain
    # their already validated dimensions.
    if row_count == 4:
        dynamic_height = max(dynamic_height, 500)

    # Very short matrices place the first indicator row close to the upper
    # figure boundary. Reserve top placement space for detailed hover labels.
    top_margin = 120 if row_count <= 4 else 30

    fig.update_layout(
        title="",
        margin=dict(l=170, r=20, t=top_margin, b=40),
        height=dynamic_height,
        hoverlabel=dict(align="left"),
    )

    fig.update_xaxes(side="top", type="category")
    fig.update_yaxes(
        autorange="reversed",
        automargin=True,
        tickfont=dict(size=11),
        showgrid=False,
    )

    return fig

def _derive_scd_price_trend_label(price_customdata: Dict[str, Any]) -> str:
    """
    Derive a simple price trend label from adapter-owned Price-row delta data.
    """
    delta_abs = price_customdata.get("delta_abs")

    try:
        delta_abs_f = float(delta_abs)
    except (TypeError, ValueError):
        return ""

    if delta_abs_f > 0:
        return "Rising"
    if delta_abs_f < 0:
        return "Falling"
    return "Flat"


def _build_scd_single_indicator_hover_customdata(
    *,
    ticker: str,
    row_key: str,
    cell: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build customdata for the Single Indicator time-series heatmap.

    This reuses the existing SCD/adapter hover contract and adds Price context
    from the attached Price-row cell when available.
    """
    custom = _build_scd_hover_customdata(
        ticker=ticker,
        row_key=row_key,
        cell=cell,
    )

    price_cell = cell.get("price_cell")
    price_customdata: Dict[str, Any] = {}

    if isinstance(price_cell, dict):
        maybe_cd = price_cell.get("adapter_customdata")
        if isinstance(maybe_cd, dict):
            price_customdata = maybe_cd

    if str(row_key).startswith("VWMA_"):
        vwma_price_customdata = (
            price_customdata
        )

        if (
            isinstance(price_cell, dict)
            and str(
                price_cell.get("date", "")
            )
            != str(
                cell.get("date", "")
            )
        ):
            vwma_price_customdata = {}

        vwma_opening = (
            build_vwma_hover_opening(
                custom,
                vwma_price_customdata,
            )
        )

        custom[
            "formatted_value"
        ] = vwma_opening[
            "formatted_value"
        ]

        custom[
            "scd_single_value_line"
        ] = (
            f"{custom.get('value_label', 'Value')}: "
            f"{vwma_opening['formatted_value']}"
            "<br>"
        )

        custom[
            "single_combined_delta_line"
        ] = vwma_opening[
            "delta_line"
        ]

        custom[
            "single_combined_trend_line"
        ] = vwma_opening[
            "trend_line"
        ]

        return custom

    def _format_price_value_for_single_hover() -> str:
        raw_value = price_customdata.get("raw_value")
        if raw_value is None and isinstance(price_cell, dict):
            raw_value = price_cell.get("value")

        try:
            return f"{float(raw_value):.2f}"
        except (TypeError, ValueError):
            formatted = (
                price_customdata.get("formatted_value")
                or (price_cell or {}).get("display_text")
                or ""
            )
            formatted = str(formatted).strip()
            if formatted.startswith("$"):
                formatted = formatted[1:]
            return "" if formatted == "-" else formatted

    def _format_price_delta_for_single_hover() -> str:
        delta_abs = price_customdata.get("delta_abs")
        delta_pct = price_customdata.get("delta_pct")

        delta_abs_txt = ""
        try:
            delta_abs_txt = f"{float(delta_abs):+.2f}"
        except (TypeError, ValueError):
            delta_abs_txt = str(
                price_customdata.get(
                    "delta_abs_fmt",
                    "",
                )
                or ""
            ).strip()

        delta_pct_txt = ""
        try:
            delta_pct_txt = (
                f" ({float(delta_pct):+.1f}%)"
            )
        except (TypeError, ValueError):
            delta_pct_txt = str(
                price_customdata.get(
                    "delta_pct_suffix",
                    "",
                )
                or ""
            ).strip()

        combined = (
            f"{delta_abs_txt}"
            f"{delta_pct_txt}"
        ).strip()

        return "" if combined == "-" else combined

    def _format_compact_volume(
        value: Any,
        *,
        signed: bool = False,
    ) -> str:
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return ""

        if pd.isna(numeric):
            return ""

        sign = (
            "+"
            if signed and numeric > 0
            else ""
        )

        magnitude = abs(numeric)

        if magnitude >= 1_000_000_000:
            return (
                f"{sign}"
                f"{numeric / 1_000_000_000:.1f}B"
            )

        if magnitude >= 1_000_000:
            return (
                f"{sign}"
                f"{numeric / 1_000_000:.1f}M"
            )

        if magnitude >= 1_000:
            return (
                f"{sign}"
                f"{numeric / 1_000:.0f}K"
            )

        return (
            f"{sign}"
            f"{numeric:,.0f}"
        )

    price_formatted = (
        _format_price_value_for_single_hover()
    )

    price_delta = (
        _format_price_delta_for_single_hover()
    )

    price_trend = (
        _derive_scd_price_trend_label(
            price_customdata
        )
    )

    is_crossover = _is_scd_crossover_event_row(
        row_key
    )

    volume_formatted = ""
    volume_delta_formatted = ""

    if not is_crossover:
        volume_formatted = _format_compact_volume(
            custom.get("volume_value")
        )

        volume_delta_abs = custom.get(
            "volume_delta"
        )

        volume_delta_pct = custom.get(
            "volume_delta_pct"
        )

        compact_volume_delta = (
            _format_compact_volume(
                volume_delta_abs,
                signed=True,
            )
        )

        if compact_volume_delta:
            volume_delta_formatted = (
                compact_volume_delta
            )

            try:
                volume_delta_formatted += (
                    " "
                    f"({float(volume_delta_pct):+.1f}%)"
                )
            except (TypeError, ValueError):
                pass

    custom["single_price_value_suffix"] = (
        f" | Price: {price_formatted}"
        if price_formatted
        and not is_crossover
        else ""
    )

    custom["single_volume_value_suffix"] = (
        f" | Vol: {volume_formatted}"
        if volume_formatted
        and not is_crossover
        else ""
    )

    custom["single_price_delta_suffix"] = (
        f" | $: {price_delta}"
        if price_delta
        and not is_crossover
        else ""
    )

    custom["single_volume_delta_suffix"] = (
        f" | Vol: {volume_delta_formatted}"
        if volume_delta_formatted
        and not is_crossover
        else ""
    )

    # Preserve the adapter-owned indicator delta formatting.
    # This retains family-specific semantics such as ROC "pps",
    # CMF zero-line handling, and BB Bandwidth display scaling.
    indicator_delta_line = (
        custom.get("delta_line", "")
        .removesuffix("<br>")
    )

    custom["single_combined_delta_line"] = (
        f"{indicator_delta_line}"
        f"{custom.get('single_price_delta_suffix', '')}"
        f"{custom.get('single_volume_delta_suffix', '')}"
        "<br>"
        if indicator_delta_line
        and not is_crossover
        else ""
    )

    if (
        is_crossover
        and custom.get(
            "crossover_summary_block"
        )
    ):
        custom["single_price_value_suffix"] = ""
        custom["single_volume_value_suffix"] = ""
        custom["single_price_delta_suffix"] = ""
        custom["single_volume_delta_suffix"] = ""
        custom["single_combined_delta_line"] = ""
        custom["scd_single_value_line"] = ""
    else:
        custom["scd_single_value_line"] = (
            f"{custom.get('value_label', 'Value')}: "
            f"{custom.get('formatted_value', '')}"
            f"{custom.get('single_price_value_suffix', '')}"
            f"{custom.get('single_volume_value_suffix', '')}<br>"
        )

    indicator_trend = custom.get("trend") or ""

    volume_trend = ""
    volume_value = custom.get(
        "volume_value"
    )
    volume_delta = custom.get(
        "volume_delta"
    )

    if volume_value is not None:
        try:
            volume_delta_value = float(
                volume_delta
            )

            if volume_delta_value > 0.0:
                volume_trend = "Rising"
            elif volume_delta_value < 0.0:
                volume_trend = "Falling"
            else:
                volume_trend = "Flat"
        except (TypeError, ValueError):
            volume_trend = ""

    if _is_scd_crossover_event_row(row_key):
        custom["single_combined_trend_line"] = ""
    elif (
        indicator_trend
        or price_trend
        or volume_trend
    ):
        custom["single_combined_trend_line"] = (
            f"Trend: {indicator_trend or 'N/A'}"
            f"{f' | Price: {price_trend}' if price_trend else ''}"
            f"{f' | Vol: {volume_trend}' if volume_trend else ''}<br>"
        )
    else:
        custom["single_combined_trend_line"] = ""

    return custom


def _format_scd_compact_date_label(date_key: Any) -> str:
    """Return compact M/D display text for Single Indicator heatmap row labels."""
    try:
        ts = pd.Timestamp(date_key)
        return f"{ts.month}/{ts.day}"
    except Exception:
        return str(date_key)


def _build_scd_single_indicator_heatmap_figure(matrix: Dict[str, Any]) -> go.Figure:
    """
    Build the Single Indicator time-series heatmap.

    Shape:
        y-axis = dates
        x-axis = tickers
        z/text/customdata = one selected indicator cell per date/ticker
    """
    tickers = list(matrix.get("tickers", []))
    dates = list(matrix.get("dates", []))
    date_labels = [_format_scd_compact_date_label(date_key) for date_key in dates]
    row_key = str(matrix.get("row_key", ""))
    row_label = str(matrix.get("row_label", row_key))
    cells = matrix.get("cells", {})

    z = []
    text = []
    customdata = []

    for date_key in dates:
        z_row = []
        text_row = []
        custom_row = []

        for ticker in tickers:
            cell = cells.get(date_key, {}).get(ticker, {})
            score = cell.get("score")

            z_value = None
            try:
                z_value = float(score) if score is not None else None
            except (TypeError, ValueError):
                z_value = None

            if z_value is None and _is_scd_crossover_event_row(row_key):
                adapter_cd = cell.get("adapter_customdata")
                has_crossover_hover = (
                    isinstance(adapter_cd, dict)
                    and (
                        adapter_cd.get("crossover_summary_block")
                        or adapter_cd.get("crossover_context_block")
                        or adapter_cd.get("crossover_spread") is not None
                    )
                )

                # Plotly heatmap cells with missing z may not expose hover.
                # For crossover rows only, use a neutral carrier when adapter
                # customdata exists so valid hover text remains reachable.
                if has_crossover_hover:
                    z_value = 0.0

            z_row.append(z_value)

            text_row.append(_format_scd_heatmap_text(row_key, cell))
            custom_row.append(
                _build_scd_single_indicator_hover_customdata(
                    ticker=ticker,
                    row_key=row_key,
                    cell=cell,
                )
            )

        z.append(z_row)
        text.append(text_row)
        customdata.append(custom_row)

    colorscale = [
        [0.0, "#8B0000"],   # strong sell
        [0.25, "#CD5C5C"],  # sell
        [0.5, "#D3D3D3"],   # neutral
        [0.75, "#90EE90"],  # buy
        [1.0, "#006400"],   # strong buy
    ]

    if _is_scd_crossover_event_row(row_key):
        # Crossover rows have intentionally dense projection/context hover.
        # Keep SCD Single Indicator crossover hover compact so Plotly can place
        # the hover label reliably across all date rows.
        #
        # Educational/reference text remains available in Indicator Definitions
        # and the family markdown path; it is omitted here only for hover
        # geometry reliability.
        hovertemplate = (
            "<b>%{customdata.display_name}</b><br>"
            "Ticker: %{customdata.ticker}<br>"
            "Date: %{customdata.date}<br>"
            "<br>"
            "%{customdata.crossover_summary_block}"
            "%{customdata.crossover_context_block}"
            "%{customdata.signal_line}"
            "%{customdata.scd_payload_hover_block}"
            "<extra></extra>"
        )
    elif row_key.startswith("VWMA_"):
        hovertemplate = (
            "<b>%{customdata.display_name}</b><br>"
            "Ticker: %{customdata.ticker}<br>"
            "Date: %{customdata.date}<br>"
            "<br>"
            "%{customdata.scd_single_value_line}"
            "%{customdata.single_combined_delta_line}"
            "%{customdata.single_combined_trend_line}"
            "%{customdata.ma_context_block}"
            "%{customdata.signal_line}"
            "%{customdata.vwma_post_signal_block}"
            "%{customdata.notes_block}"
            "%{customdata.definition_block}"
            "%{customdata.how_to_read_block}"
            "<extra></extra>"
        )

    elif row_key.startswith("HMA_"):
        hovertemplate = (
            "<b>%{customdata.display_name}</b><br>"
            "Ticker: %{customdata.ticker}<br>"
            "Date: %{customdata.date}<br>"
            "<br>"
            "%{customdata.scd_single_value_line}"
            "%{customdata.single_combined_delta_line}"
            "%{customdata.single_combined_trend_line}"
            "%{customdata.ma_context_block}"
            "%{customdata.signal_line}"
            "%{customdata.hma_post_signal_block}"
            "%{customdata.rule_block}"
            "%{customdata.notes_block}"
            "%{customdata.definition_block}"
            "%{customdata.how_to_read_block}"
            "<extra></extra>"
        )

    else:
        hovertemplate = (
            "<b>%{customdata.display_name}</b><br>"
            "Ticker: %{customdata.ticker}<br>"
            "Date: %{customdata.date}<br>"
            "<br>"
            "%{customdata.scd_single_value_line}"
            "%{customdata.crossover_summary_block}"
            "%{customdata.crossover_context_block}"
            "%{customdata.single_combined_delta_line}"
            "%{customdata.single_combined_trend_line}"
            "%{customdata.bb_bw_context_block}"
            "%{customdata.alignment_line}"
            "%{customdata.ma_context_block}"
            "%{customdata.adx_context_block}"
            "%{customdata.uo_context_block}"
            "%{customdata.signal_line}"
            "%{customdata.cci_context_block}"
            "%{customdata.bbp_exhaustion_context_block}"
            "%{customdata.macd_context_block}"
            "%{customdata.stoch_context_block}"
            "%{customdata.cmf_context_block}"
            "%{customdata.dpo_context_block}"
            "%{customdata.bullbear_context_block}"
            "%{customdata.rule_block}"
            "%{customdata.notes_block}"
            "%{customdata.definition_block}"
            "%{customdata.how_to_read_block}"
            "%{customdata.band_context_block}"
            "%{customdata.volume_block}"
            "%{customdata.volume_vs_avg_block}"
            "%{customdata.scd_payload_hover_block}"
            "<extra></extra>"
        )

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=tickers,
            y=date_labels,
            text=text,
            texttemplate="%{text}",
            customdata=customdata,
            colorscale=colorscale,
            zmin=-2,
            zmax=2,
            hovertemplate=hovertemplate,
            colorbar=dict(title="Score"),
        )
    )

    apply_bbp_divergence_text_overlay(
        fig,
        text=text,
        customdata=customdata,
        x=tickers,
        y=date_labels,
    )

    apply_cci_divergence_text_overlay(
        fig,
        text=text,
        customdata=customdata,
        x=tickers,
        y=date_labels,
    )

    apply_uo_divergence_symbol_overlay(
        fig,
        customdata=customdata,
        x=tickers,
        y=date_labels,
    )

    apply_hma_turn_text_overlay(
        fig,
        text=text,
        customdata=customdata,
        x=tickers,
        y=date_labels,
    )

    apply_vwma_volume_extreme_text_overlay(
        fig,
        text=text,
        customdata=customdata,
        x=tickers,
        y=date_labels,
    )

    dynamic_height = max(450, 24 * max(len(dates), 1) + 180)    # dynamic_height = max(900, 42 * max(len(dates), 1) + 360)

    fig.update_layout(
        title=f"{row_label}",
        margin=dict(l=110, r=20, t=80, b=80),
        height=dynamic_height,
        hoverlabel=dict(align="left"),
    )

    fig.update_xaxes(
        side="top",
        type="category",
    )

    fig.update_yaxes(
        range=[
            len(date_labels) - 0.5,
            -0.5,
        ],
        automargin=True,
        tickmode="array",
        tickvals=date_labels,
        ticktext=date_labels,
        tickfont=dict(size=11),
    )

    return fig


def _build_scd_single_indicator_detail_table(matrix: Dict[str, Any]) -> pd.DataFrame:
    """
    Build a dates × tickers detail table for the Single Indicator matrix.

    The table uses the same display text shown in the heatmap cells.
    """
    tickers = list(matrix.get("tickers", []))
    dates = list(matrix.get("dates", []))
    row_key = str(matrix.get("row_key", ""))
    cells = matrix.get("cells", {})

    records = []
    for date_key in dates:
        row = {"Date": date_key}
        for ticker in tickers:
            cell = cells.get(date_key, {}).get(ticker, {})
            row[ticker] = _format_scd_heatmap_text(row_key, cell)
        records.append(row)

    return pd.DataFrame(records)


def _get_scd_single_chart_value_modes() -> list[str]:
    """Return supported Single Indicator chart value modes."""
    return [
        "Auto",
        "Indicator value",
        "Indexed to 100",
        "Change from first date",
        "% change from first date",
        "Score",
    ]


def _get_scd_single_chart_auto_mode(row_key: str) -> str:
    """
    Resolve Auto chart mode for one Single Indicator row_key.

    Auto intentionally avoids Score mode. It chooses a display transform only.
    """
    row_key = str(row_key).strip()
    family = ROW_CLASSIFICATION.get(row_key, {}).get("family", "")

    if _is_scd_crossover_event_row(row_key):
        return "Indicator value"

    if row_key.startswith("BBP_DOWNSIDE_EXHAUSTION_"):
        return "Indicator value"

    if row_key == "OBV":
        return "Change from first date"

    if family in {
        "RSI",
        "Stochastic",
        "Williams_R",
        "MFI",
        "Ultimate_Oscillator",
        "ADX",
        "CMF",
        "CCI",
        "ROC",
        "DPO",
    }:
        return "Indicator value"

    if row_key.startswith("BB_PCT_B") or row_key.startswith("BB_BW"):
        return "Indicator value"

    if family in {"SMA", "EMA", "HMA", "VWMA", "ATR"}:
        return "Indexed to 100"

    if family in {"MACD", "BullBearPower"}:
        return "Change from first date"

    return "Indicator value"


def _resolve_scd_single_chart_value_mode(
    *,
    row_key: str,
    selected_mode: str,
) -> str:
    """Resolve chart mode, expanding Auto to the indicator-specific default."""
    mode = str(selected_mode).strip()
    if mode == "Auto":
        return _get_scd_single_chart_auto_mode(row_key)
    if mode in _get_scd_single_chart_value_modes():
        return mode
    return _get_scd_single_chart_auto_mode(row_key)


def _coerce_scd_chart_numeric_value(value: Any) -> Optional[float]:
    """Coerce chart values to float while preserving missing values as None."""
    try:
        value_f = float(value)
    except (TypeError, ValueError):
        return None

    if pd.isna(value_f):
        return None

    return value_f


def _get_scd_single_chart_source_value(
    *,
    row_key: str,
    cell: Dict[str, Any],
    value_mode: str,
) -> Optional[float]:
    """
    Return the numeric source value for the SCD Single Indicator chart.

    Crossover event rows are score-colored in the heatmap, but their chart
    visualizes MA spread rather than event score/value, regardless of the
    currently selected chart transform.
    """
    if _is_scd_crossover_event_row(row_key):
        adapter_cd = cell.get("adapter_customdata")
        if isinstance(adapter_cd, dict):
            return _coerce_scd_chart_numeric_value(
                adapter_cd.get("crossover_spread")
            )
        return None

    if value_mode == "Score":
        return _coerce_scd_chart_numeric_value(cell.get("score"))

    return _coerce_scd_chart_numeric_value(cell.get("value"))


def _get_scd_chart_yaxis_title(mode: str, row_label: str) -> str:
    """Return a compact y-axis title for the selected chart transform."""
    if mode == "Indexed to 100":
        return "Indexed value"
    if mode == "Change from first date":
        return "Change from first date"
    if mode == "% change from first date":
        return "% change from first date"
    if mode == "Score":
        return "Score"
    return row_label


def _build_scd_single_indicator_chart_series(
    *,
    matrix: Dict[str, Any],
    visible_tickers: list[str],
    value_mode: str,
) -> tuple[dict[str, list[Optional[float]]], list[str]]:
    """
    Build chart series from the already-built Single Indicator matrix.

    This is display-only. It does not alter matrix cells, scores, rules,
    cache entries, acquisition, or persistence.
    """
    row_key = str(matrix.get("row_key", "")).strip()
    dates = list(matrix.get("dates", []))
    cells = matrix.get("cells", {})

    raw_series: dict[str, list[Optional[float]]] = {}

    for ticker in visible_tickers:
        values: list[Optional[float]] = []

        for date_key in dates:
            cell = cells.get(date_key, {}).get(ticker, {})
            values.append(
                _get_scd_single_chart_source_value(
                    row_key=row_key,
                    cell=cell,
                    value_mode=value_mode,
                )
            )

        raw_series[ticker] = values

    warnings: list[str] = []

    if value_mode in {"Indicator value", "Score"}:
        return raw_series, warnings

    transformed: dict[str, list[Optional[float]]] = {}

    for ticker, values in raw_series.items():
        first_valid = next((v for v in values if v is not None), None)

        if first_valid is None:
            transformed[ticker] = [None for _ in values]
            warnings.append(f"{ticker}: no valid starting value.")
            continue

        if value_mode == "Change from first date":
            transformed[ticker] = [
                (v - first_valid) if v is not None else None
                for v in values
            ]
            continue

        if value_mode == "% change from first date":
            if abs(first_valid) <= 1e-9:
                transformed[ticker] = [None for _ in values]
                warnings.append(
                    f"{ticker}: % change unavailable because first value is near zero."
                )
                continue

            transformed[ticker] = [
                ((v - first_valid) / abs(first_valid) * 100.0)
                if v is not None
                else None
                for v in values
            ]
            continue

        if value_mode == "Indexed to 100":
            if first_valid <= 0 or abs(first_valid) <= 1e-9:
                transformed[ticker] = [None for _ in values]
                warnings.append(
                    f"{ticker}: Indexed to 100 unavailable because first value "
                    "is not positive or is near zero."
                )
                continue

            transformed[ticker] = [
                (v / first_valid * 100.0) if v is not None else None
                for v in values
            ]
            continue

        transformed[ticker] = values

    return transformed, warnings


def _get_scd_chart_signal_text(
    *,
    row_key: str,
    cell: Any,
) -> str:
    """
    Return the user-facing Signal label for SCD chart hovers.

    UO reuses the adapter-owned semantic Signal line so chart hovers match
    the heatmap's seven-state presentation vocabulary. Other indicators
    retain their existing payload signal labels.
    """
    if not isinstance(cell, dict):
        return "N/A"

    if row_key.startswith("UO_"):
        adapter_cd = cell.get("adapter_customdata")

        if isinstance(adapter_cd, dict):
            signal_line = adapter_cd.get("signal_line")

            if signal_line not in {
                None,
                "",
            }:
                signal_text = (
                    str(signal_line)
                    .removeprefix("<br>")
                    .removeprefix("Signal: ")
                    .removesuffix("<br>")
                    .strip()
                )

                if signal_text:
                    return signal_text

    signal = cell.get("signal")

    return (
        str(signal)
        if signal not in {
            None,
            "",
        }
        else "N/A"
    )


def _get_scd_single_chart_hover_fields(
    *,
    matrix: Dict[str, Any],
    ticker: str,
    date_key: str,
    chart_value: Optional[float],
    value_mode: str,
) -> list[Any]:
    """
    Return compact hover customdata for one Single Indicator chart point.

    Indicator delta is calculated from the underlying indicator series rather
    than from the selected chart transform. This keeps the hover value stable
    across Indicator value, Indexed to 100, change, percentage-change, and
    Score display modes.
    """
    row_key = str(matrix.get("row_key", ""))
    dates = list(matrix.get("dates", []))
    cells = matrix.get("cells", {})
    cell = cells.get(date_key, {}).get(ticker, {})

    indicator_value = _get_scd_single_chart_source_value(
        row_key=row_key,
        cell=cell,
        value_mode="Indicator value",
    )

    indicator_delta_line = "N/A"

    # Ordinary indicator cells already carry adapter-formatted delta metadata.
    # Reuse it so the chart hover follows the same display units as the heatmap.
    #
    # Example:
    #   canonical CMF delta: -0.043
    #   displayed CMF delta: -4.3
    #
    # Crossover charts visualize MA spread rather than the event-row value, so
    # they retain the chart-local spread calculation below.
    indicator_cd = (
        cell.get("adapter_customdata")
        if isinstance(cell, dict)
        else None
    )

    if (
        not _is_scd_crossover_event_row(row_key)
        and isinstance(indicator_cd, dict)
        and indicator_cd.get("delta_line")
    ):
        indicator_delta_line = (
            str(indicator_cd.get("delta_line", ""))
            .removeprefix("Δ vs prior day: ")
            .removesuffix("<br>")
        )
    else:
        try:
            date_position = dates.index(date_key)
        except ValueError:
            date_position = -1

        if date_position > 0 and indicator_value is not None:
            prior_date_key = dates[date_position - 1]
            prior_cell = cells.get(
                prior_date_key,
                {},
            ).get(
                ticker,
                {},
            )
            prior_indicator_value = _get_scd_single_chart_source_value(
                row_key=row_key,
                cell=prior_cell,
                value_mode="Indicator value",
            )

            if prior_indicator_value is not None:
                indicator_delta_abs = (
                    indicator_value
                    - prior_indicator_value
                )

                if abs(prior_indicator_value) > 1e-9:
                    indicator_delta_pct = (
                        indicator_delta_abs
                        / abs(prior_indicator_value)
                        * 100.0
                    )
                    indicator_delta_line = (
                        f"{indicator_delta_abs:+.1f} "
                        f"({indicator_delta_pct:+.1f}%)"
                    )
                else:
                    indicator_delta_line = (
                        f"{indicator_delta_abs:+.1f} "
                        "(relative change unavailable)"
                    )

    price_cell = (
        cell.get("price_cell")
        if isinstance(cell, dict)
        else None
    )
    price_cd = {}

    if isinstance(price_cell, dict):
        maybe_cd = price_cell.get("adapter_customdata")
        if isinstance(maybe_cd, dict):
            price_cd = maybe_cd

    price_value = price_cd.get("formatted_value", "")
    price_delta = ""

    if price_cd.get("delta_abs_fmt"):
        price_delta = (
            f"{price_cd.get('delta_abs_fmt', '')}"
            f"{price_cd.get('delta_pct_suffix', '')}"
        )

    alignment_line = ""

    if isinstance(indicator_cd, dict):
        alignment_line = str(
            indicator_cd.get("alignment_line", "")
        )

    return [
        str(date_key),
        _format_scd_heatmap_text(row_key, cell),
        _get_scd_chart_signal_text(
            row_key=row_key,
            cell=cell,
        ),
        chart_value,
        price_value,
        price_delta,
        indicator_delta_line,
        alignment_line,
    ]

def _add_scd_single_chart_reference_lines(
    *,
    fig: go.Figure,
    row_key: str,
    value_mode: str,
) -> None:
    """Add native indicator reference lines where they are meaningful."""
    if value_mode == "Score":
        for level in [-2, -1, 0, 1, 2]:
            fig.add_hline(y=level, line_dash="dot", opacity=0.35)
        fig.update_yaxes(range=[-2.25, 2.25])
        return

    if value_mode != "Indicator value":
        return

    family = ROW_CLASSIFICATION.get(row_key, {}).get("family", "")

    if family == "CCI":
        for level in [100, 0, -100]:
            fig.add_hline(y=level, line_dash="dot", opacity=0.45)

    elif family == "RSI":
        for level in [70, 50, 30]:
            fig.add_hline(y=level, line_dash="dot", opacity=0.45)

    elif family in {"MFI", "Ultimate_Oscillator", "Stochastic"}:
        for level in [80, 50, 20]:
            fig.add_hline(y=level, line_dash="dot", opacity=0.45)

    elif family == "Williams_R":
        for level in [-20, -50, -80]:
            fig.add_hline(y=level, line_dash="dot", opacity=0.45)


def _build_scd_single_indicator_chart_figure(
    *,
    matrix: Dict[str, Any],
    visible_tickers: list[str],
    selected_value_mode: str,
) -> tuple[go.Figure, str, list[str]]:
    """
    Build the Single Indicator line chart.

    The chart is derived only from existing Single Indicator matrix cells.
    """
    row_key = str(matrix.get("row_key", ""))
    row_label = str(matrix.get("row_label", row_key))
    dates = list(matrix.get("dates", []))
    date_labels = [_format_scd_compact_date_label(date_key) for date_key in dates]

    resolved_mode = _resolve_scd_single_chart_value_mode(
        row_key=row_key,
        selected_mode=selected_value_mode,
    )

    series_by_ticker, warnings = _build_scd_single_indicator_chart_series(
        matrix=matrix,
        visible_tickers=visible_tickers,
        value_mode=resolved_mode,
    )

    fig = go.Figure()

    for ticker in visible_tickers:
        y_values = series_by_ticker.get(ticker, [])
        customdata = [
            _get_scd_single_chart_hover_fields(
                matrix=matrix,
                ticker=ticker,
                date_key=date_key,
                chart_value=y_values[i] if i < len(y_values) else None,
                value_mode=resolved_mode,
            )
            for i, date_key in enumerate(dates)
        ]

        fig.add_trace(
            go.Scatter(
                x=date_labels,
                y=y_values,
                mode="lines+markers",
                name=ticker,
                customdata=customdata,
                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "Date: %{customdata[0]}<br>"
                    f"{row_label}: %{{customdata[1]}}<br>"
                    "Δ vs prior day: %{customdata[6]}<br>"
                    "%{customdata[7]}"
                    f"Chart value ({resolved_mode}): %{{customdata[3]:.2f}}<br>"
                    "Signal: %{customdata[2]}<br>"
                    "Price: %{customdata[4]}<br>"
                    "Price Δ vs prior day: %{customdata[5]}"
                    "<extra></extra>"
                ),
            )
        )

    _add_scd_single_chart_reference_lines(
        fig=fig,
        row_key=row_key,
        value_mode=resolved_mode,
    )

    y_axis_title = _get_scd_chart_yaxis_title(resolved_mode, row_label)
    dynamic_height = max(420, 35 * max(len(visible_tickers), 1) + 260)

    fig.update_layout(
        title=dict(
            text=f"{row_label}",
            y=0.98,
            yanchor="top",
        ),
        height=dynamic_height,
        margin=dict(l=70, r=30, t=150, b=70),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="left",
            x=0,
        ),
        hoverlabel=dict(align="left"),
    )

    fig.update_xaxes(
        title="Date",
        type="category",
        tickmode="array",
        tickvals=date_labels,
        ticktext=date_labels,
    )
    fig.update_yaxes(title=y_axis_title)

    return fig, resolved_mode, warnings


def _get_scd_single_price_chart_value_modes() -> list[str]:
    """Return supported display modes for the SCD Price Trend Chart."""
    return [
        "Indexed to 100",
        "Stock price",
    ]


def _get_scd_single_price_value(
    cell: Dict[str, Any],
) -> Optional[float]:
    """
    Return the matrix-owned numeric Price value for one SCD cell.

    The optimized Single Indicator matrix normally stores the adapter-owned
    __PRICE__ raw value in price_cell["value"]. The customdata fallback keeps
    this display helper compatible with older or partial matrix payloads.
    """
    if not isinstance(cell, dict):
        return None

    price_cell = cell.get("price_cell")
    if not isinstance(price_cell, dict):
        return None

    price_value = _coerce_scd_chart_numeric_value(
        price_cell.get("value")
    )
    if price_value is not None:
        return price_value

    adapter_cd = price_cell.get("adapter_customdata")
    if isinstance(adapter_cd, dict):
        return _coerce_scd_chart_numeric_value(
            adapter_cd.get("raw_value")
        )

    return None


def _build_scd_single_price_chart_series(
    *,
    matrix: Dict[str, Any],
    visible_tickers: list[str],
    value_mode: str,
) -> tuple[
    dict[str, list[Optional[float]]],
    dict[str, list[Optional[float]]],
    list[str],
]:
    """
    Build actual-price and display-price series from matrix-owned Price cells.

    Returns:
        display_series:
            Stock price or Indexed-to-100 values used on the y-axis.

        actual_price_series:
            Untransformed Price values retained for hover display.

        warnings:
            Per-ticker transform limitations.

    This helper is display-only. It does not alter matrix cells, acquisition,
    rolling payloads, adapters, caches, persistence, or indicator computation.
    """
    dates = list(matrix.get("dates", []))
    cells = matrix.get("cells", {})

    actual_price_series: dict[
        str,
        list[Optional[float]],
    ] = {}

    for ticker in visible_tickers:
        values: list[Optional[float]] = []

        for date_key in dates:
            cell = cells.get(date_key, {}).get(ticker, {})
            values.append(
                _get_scd_single_price_value(cell)
            )

        actual_price_series[ticker] = values

    warnings: list[str] = []

    if value_mode == "Stock price":
        return (
            dict(actual_price_series),
            actual_price_series,
            warnings,
        )

    display_series: dict[
        str,
        list[Optional[float]],
    ] = {}

    for ticker, values in actual_price_series.items():
        first_valid = next(
            (
                value
                for value in values
                if value is not None
            ),
            None,
        )

        if (
            first_valid is None
            or first_valid <= 0
            or abs(first_valid) <= 1e-9
        ):
            display_series[ticker] = [
                None
                for _ in values
            ]
            warnings.append(
                f"{ticker}: Indexed to 100 unavailable because "
                "no positive starting Price value is available."
            )
            continue

        display_series[ticker] = [
            (
                value / first_valid * 100.0
                if value is not None
                else None
            )
            for value in values
        ]

    return (
        display_series,
        actual_price_series,
        warnings,
    )


def _build_scd_single_price_chart_figure(
    *,
    matrix: Dict[str, Any],
    visible_tickers: list[str],
    selected_value_mode: str,
) -> tuple[go.Figure, list[str]]:
    """
    Build the SCD Price Trend Chart from existing matrix-owned Price cells.
    """
    row_key = str(matrix.get("row_key", ""))
    dates = list(matrix.get("dates", []))
    date_labels = [
        _format_scd_compact_date_label(date_key)
        for date_key in dates
    ]

    value_modes = _get_scd_single_price_chart_value_modes()
    resolved_mode = (
        selected_value_mode
        if selected_value_mode in value_modes
        else "Indexed to 100"
    )

    (
        display_series,
        actual_price_series,
        warnings,
    ) = _build_scd_single_price_chart_series(
        matrix=matrix,
        visible_tickers=visible_tickers,
        value_mode=resolved_mode,
    )

    fig = go.Figure()

    for ticker in visible_tickers:
        y_values = display_series.get(ticker, [])
        actual_prices = actual_price_series.get(ticker, [])
        matrix_cells = matrix.get("cells", {})

        customdata = []

        for index, date_key in enumerate(dates):
            cell = (
                matrix_cells
                .get(date_key, {})
                .get(ticker, {})
            )

            adapter_cd = (
                cell.get("adapter_customdata")
                if isinstance(cell, dict)
                else None
            )

            indicator_value = ""

            if isinstance(adapter_cd, dict):
                formatted_value = adapter_cd.get(
                    "formatted_value"
                )
                if formatted_value not in {
                    None,
                    "",
                }:
                    indicator_value = str(formatted_value)

            if not indicator_value:
                raw_indicator_value = (
                    _coerce_scd_chart_numeric_value(
                        cell.get("value")
                    )
                    if isinstance(cell, dict)
                    else None
                )

                indicator_value = (
                    f"{raw_indicator_value:,.2f}"
                    if raw_indicator_value is not None
                    else "N/A"
                )

            signal_text = (
                _get_scd_chart_signal_text(
                    row_key=row_key,
                    cell=cell,
                )
            )

            customdata.append(
                [
                    str(date_key),
                    (
                        actual_prices[index]
                        if index < len(actual_prices)
                        else None
                    ),
                    indicator_value,
                    signal_text,
                ]
            )

        if resolved_mode == "Stock price":
            chart_value_line = (
                "Stock price: $%{y:,.2f}<br>"
            )
        else:
            chart_value_line = (
                "Indexed value: %{y:,.2f}<br>"
                "Stock price: $%{customdata[1]:,.2f}<br>"
            )

        fig.add_trace(
            go.Scatter(
                x=date_labels,
                y=y_values,
                mode="lines+markers",
                name=ticker,
                customdata=customdata,
                connectgaps=False,
                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "Date: %{customdata[0]}<br>"
                    f"{chart_value_line}"
                    "Indicator value: %{customdata[2]}<br>"
                    "Signal: %{customdata[3]}<br>"
                    "<extra></extra>"
                ),
            )
        )

    original_height = max(
        420,
        35 * max(len(visible_tickers), 1) + 260,
    )
    dynamic_height = max(
        330,
        int(round(original_height * 0.75)), # change height of 'Price trend' chart
    )

    fig.update_layout(
        title=dict(
            text="Price Trend Chart",
            x=0.0,
            xanchor="left",
            y=0.98,
            yanchor="top",
        ),
        height=dynamic_height,
        margin=dict(
            l=70,
            r=30,
            t=105,
            b=70,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="left",
            x=0,
        ),
        hoverlabel=dict(align="left"),
    )

    fig.update_xaxes(
        title="Date",
        type="category",
        tickmode="array",
        tickvals=date_labels,
        ticktext=date_labels,
    )

    if resolved_mode == "Stock price":
        fig.update_yaxes(
            title="Stock price ($)",
            tickprefix="$",
            tickformat=",.2f",
        )
    else:
        fig.update_yaxes(
            title="Indexed price",
            tickformat=",.2f",
        )
        fig.add_hline(
            y=100,
            line_dash="dot",
            opacity=0.45,
        )

    return fig, warnings


def _render_scd_single_price_chart_view(
    matrix: Dict[str, Any],
) -> None:
    """
    Render the independent SCD Price Trend Chart below the indicator chart.

    Ticker visibility is handled by this chart's native Plotly legend and is
    intentionally independent from the indicator chart legend.
    """
    if not isinstance(matrix, dict) or not matrix:
        return

    tickers = list(matrix.get("tickers", []))
    if not tickers:
        st.info("No tickers available for the Price Trend Chart.")
        return

    value_modes = _get_scd_single_price_chart_value_modes()
    current_mode = st.session_state.get(
        "scd_single_price_chart_value_mode",
        "Indexed to 100",
    )

    if current_mode not in value_modes:
        current_mode = "Indexed to 100"
        st.session_state.scd_single_price_chart_value_mode = (
            current_mode
        )

    fig, warnings = _build_scd_single_price_chart_figure(
        matrix=matrix,
        visible_tickers=tickers,
        selected_value_mode=current_mode,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="scd_single_price_trend_chart",
        config={
            "doubleClickDelay": 800,
            "responsive": True,
        },
    )

    st.selectbox(
        "Price chart value",
        options=value_modes,
        index=value_modes.index(current_mode),
        key="scd_single_price_chart_value_mode",
        help=(
            "Indexed to 100 rebases each ticker's first valid Price "
            "in the displayed date range to 100. Stock price shows "
            "the underlying dollar values."
        ),
    )

    st.markdown(
        "<small style='color: #6c757d;'>"
        "Tip: This chart has an independent legend. "
        "Click a ticker to hide/show it; double-click to isolate it."
        "</small>",
        unsafe_allow_html=True,
    )

    if warnings:
        with st.expander(
            "Price chart transform notes",
            expanded=False,
        ):
            for warning in warnings:
                st.markdown(
                    f"<small style='color: #6c757d;'>"
                    f"- {warning}"
                    f"</small>",
                    unsafe_allow_html=True,
                )


def _render_scd_single_indicator_chart_view(matrix: Dict[str, Any]) -> None:
    """
    Render chart-only controls and line chart for the Single Indicator matrix.

    Ticker visibility is handled by the native Plotly legend. This affects only
    chart display and must not mutate the matrix, heatmap, table, export, cache,
    or payload.
    """
    if not isinstance(matrix, dict) or not matrix:
        return

    tickers = list(matrix.get("tickers", []))
    if not tickers:
        st.info("No tickers available for the Single Indicator chart.")
        return

    st.subheader("Single Indicator Trend Chart")

    value_modes = _get_scd_single_chart_value_modes()
    current_mode = st.session_state.get("scd_single_chart_value_mode", "Auto")
    if current_mode not in value_modes:
        current_mode = "Auto"
        st.session_state.scd_single_chart_value_mode = current_mode

    selected_mode = st.selectbox(
        "Chart value",
        options=value_modes,
        index=value_modes.index(current_mode),
        key="scd_single_chart_value_mode",
        help=(
            "Auto chooses a display transform based on the selected indicator. "
            "Score plots the existing heatmap score from -2 to +2."
        ),
    )

    fig, resolved_mode, warnings = _build_scd_single_indicator_chart_figure(
        matrix=matrix,
        visible_tickers=tickers,
        selected_value_mode=selected_mode,
    )

    if selected_mode == "Auto":
        st.markdown(
            f"<small style='color: #6c757d;'>"
            f"Auto chart mode resolved to: {resolved_mode}"
            f"</small>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<small style='color: #6c757d;'>"
        "Tip: Click a ticker in the legend to hide/show it. "
        "Double-click to isolate one ticker."
        "</small>",
        unsafe_allow_html=True,
    )

    if warnings:
        with st.expander("Chart transform notes", expanded=False):
            for warning in warnings:
                st.markdown(
                    f"<small style='color: #6c757d;'>- {warning}</small>",
                    unsafe_allow_html=True,
                )

    #st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(
        fig,
        use_container_width=True,
        key="scd_single_indicator_trend_chart",
        config={
            "doubleClickDelay": 800,
            "responsive": True,
        },
    )    


def _render_scd_single_indicator_matrix_view(matrix: Dict[str, Any]) -> None:
    """
    Render the Single Indicator time-series matrix.

    This renders display-only views of already-built cells:
    - heatmap
    - detail/export table
    - existing ticker-status diagnostics
    """
    if not isinstance(matrix, dict) or not matrix:
        st.info("Build the Single Indicator time-series matrix first.")
        return

    if matrix.get("status") == "empty":
        st.warning("Single Indicator matrix is empty.")
        if matrix.get("errors"):
            st.write(matrix.get("errors"))
        return

    st.subheader("Single Indicator Time-Series Heatmap")

    fig = _build_scd_single_indicator_heatmap_figure(matrix)
    st.plotly_chart(fig, use_container_width=True)

    _render_scd_single_indicator_chart_view(matrix)
    _render_scd_single_price_chart_view(matrix)

    detail_df = _build_scd_single_indicator_detail_table(matrix)

    with st.expander("Show Details / Export", expanded=False):
        st.dataframe(detail_df, use_container_width=True, hide_index=True)

        csv_bytes = detail_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Single Indicator CSV",
            data=csv_bytes,
            file_name=(
                "scd_single_indicator_"
                f"{matrix.get('row_key', 'indicator')}_"
                f"{matrix.get('window_start_date', 'start')}_"
                f"{matrix.get('window_end_date', 'end')}.csv"
            ),
            mime="text/csv",
            key="scd_single_indicator_download_csv",
        )


def _build_scd_detail_table(matrix: Dict[str, Any]) -> pd.DataFrame:
    """
    Build the SCD Detail Table View from the same matrix cells as the heatmap.
    """
    rows = []
    cells = matrix.get("cells", {})

    for row_key in matrix.get("row_keys", []):
        display_name = _get_scd_row_display_name(row_key)

        for ticker in matrix.get("tickers", []):
            cell = cells.get(row_key, {}).get(ticker, {})
            adapter_cd = cell.get("adapter_customdata")
            formatted_value = ""
            if isinstance(adapter_cd, dict):
                formatted_value = adapter_cd.get("formatted_value", "")

            rows.append(
                {
                    "ticker": ticker,
                    "row_key": row_key,
                    "display_name": display_name,
                    "date": cell.get("date"),
                    "value": cell.get("value"),
                    "formatted_value": formatted_value or cell.get("display_text"),
                    "signal": cell.get("signal"),
                    "score": cell.get("score"),
                    "status": cell.get("status"),
                    "hover": cell.get("hover"),
                }
            )

    return pd.DataFrame(rows)


def _render_scd_matrix_view(matrix: Optional[Dict[str, Any]]) -> None:
    """
    Render the Stock Comparison heatmap, detail table, and diagnostics.

    This consumes the existing matrix. It does not trigger payload execution
    and does not compute new numeric or semantic truth.
    """
    if not matrix:
        st.info("No comparison matrix has been built yet.")
        return

    if matrix.get("errors"):
        st.warning("Some ticker payloads produced errors.")
        with st.expander("View ticker errors", expanded=False):
            st.write(matrix.get("errors"))

        with st.expander("Ticker payload status", expanded=False):
            st.json(matrix.get("ticker_status", {}))

    fig = _build_scd_heatmap_figure(matrix)
    st.plotly_chart(fig, use_container_width=True)

    snapshot_date = matrix.get("anchor_date") or "Latest available completed snapshot"
    ticker_count = len(matrix.get("tickers", []))
    row_count = len(matrix.get("row_keys", []))
    st.caption(
        f"Snapshot date: {snapshot_date} | "
        f"Tickers: {ticker_count} | "
        f"Indicator rows: {row_count}"
    )

    profile = matrix.get("profile", {})
    if isinstance(profile, dict) and profile:
        show_performance_profile = st.checkbox(
            "Show Performance Profile",
            value=False,
            key="scd_show_performance_profile",
            help=(
                "Show timing diagnostics for the latest matrix build. "
                "This is for performance investigation only."
            ),
        )

        if show_performance_profile:
            st.caption(
                f"Total build time: {profile.get('total_seconds')}s | "
                f"Tickers: {profile.get('ticker_count')} | "
                f"Rows: {profile.get('row_count')}"
            )

            ticker_profile = profile.get("tickers", {})
            if isinstance(ticker_profile, dict) and ticker_profile:
                profile_rows = []
                for ticker, stats in ticker_profile.items():
                    if not isinstance(stats, dict):
                        continue
                    profile_rows.append({
                        "ticker": ticker,
                        "status": stats.get("status"),
                        "bundle_source": stats.get("bundle_source"),
                        "rolling_payload_seconds": stats.get("rolling_payload_seconds"),
                        "hover_context_seconds": stats.get("hover_context_seconds"),
                        "adapter_lookup_seconds": stats.get("adapter_lookup_seconds"),
                        "latest_cell_extraction_seconds": stats.get("latest_cell_extraction_seconds"),
                        "total_seconds": stats.get("total_seconds"),
                    })

                if profile_rows:
                    st.dataframe(
                        pd.DataFrame(profile_rows),
                        use_container_width=True,
                        hide_index=True,
                    )

    show_detail_export = st.checkbox(
        "Show Details / Export",
        value=False,
        key="scd_show_detail_export",
        help=(
            "Build and display the detail table only when needed for audit, "
            "copy/export, or validation."
        ),
    )

    if show_detail_export:
        with st.expander("Details / Export", expanded=True):
            detail_df = _build_scd_detail_table(matrix)

            if detail_df.empty:
                st.info("No detail rows available.")
            else:
                st.dataframe(detail_df, use_container_width=True, hide_index=True)

                csv = detail_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download Detail Table CSV",
                    data=csv,
                    file_name="stock_comparison_detail_table.csv",
                    mime="text/csv",
                    key="scd_detail_table_csv_download",
                )

        
def is_final_data_available_for_date(target_date: datetime) -> bool:
    """
    Check if final data is available for a given date
    Only save to database if data is from last completed trading day or earlier
    
    Args:
        target_date: The date to check
        
    Returns:
        True if final data is available (target_date <= last completed trading day)
    """
    from calculations.performance import get_last_completed_trading_day
    
    last_complete_day = get_last_completed_trading_day()
    
    # Convert both to date objects for comparison
    if isinstance(last_complete_day, datetime):
        last_complete_day = last_complete_day.date()
    
    if isinstance(target_date, datetime):
        target_date_only = target_date.date()
    else:
        target_date_only = target_date
    
    # Final data is available if target date is on or before last completed trading day
    return target_date_only <= last_complete_day

def create_level1_predefined_selection():
    """Level 1: Predefined ticker selection with checkboxes"""
    from config.assets import COUNTRY_ETFS, SECTOR_ETFS, get_tickers_only
    
    st.sidebar.subheader("📋 Level 1: Predefined Assets")
    
    # Country ETFs Section
    with st.sidebar.expander("🌍 Country ETFs (52 available)", expanded=False):
        # Select All/Deselect All for Country ETFs
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Select All Countries", key="select_all_countries"):
                st.session_state.selected_country_etfs = get_tickers_only(COUNTRY_ETFS)
        with col2:
            if st.button("Deselect All Countries", key="deselect_all_countries"):
                st.session_state.selected_country_etfs = []
        
        # Search filter for countries
        country_search = st.text_input(
            "Search countries:",
            key="country_search",
            placeholder="Type to filter..."
        )
        
        # Filter country ETFs based on search
        filtered_countries = COUNTRY_ETFS
        if country_search:
            filtered_countries = [
                (ticker, name) for ticker, name in COUNTRY_ETFS
                if country_search.lower() in name.lower() or country_search.lower() in ticker.lower()
            ]
        
        # Create checkboxes for country ETFs
        for ticker, display_name in filtered_countries:
            is_selected = ticker in st.session_state.selected_country_etfs
            if st.checkbox(
                f"{display_name} ({ticker})",
                value=is_selected,
                key=f"country_{ticker}"
            ):
                if ticker not in st.session_state.selected_country_etfs:
                    st.session_state.selected_country_etfs.append(ticker)
            else:
                if ticker in st.session_state.selected_country_etfs:
                    st.session_state.selected_country_etfs.remove(ticker)
        
        # Show selection count
        st.caption(f"Selected: {len(st.session_state.selected_country_etfs)} countries")
    
    # Sector ETFs Section
    with st.sidebar.expander("🏭 Sector ETFs (30 available)", expanded=False):
        # Select All/Deselect All for Sector ETFs
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Select All Sectors", key="select_all_sectors"):
                st.session_state.selected_sector_etfs = get_tickers_only(SECTOR_ETFS)
        with col2:
            if st.button("Deselect All Sectors", key="deselect_all_sectors"):
                st.session_state.selected_sector_etfs = []
        
        # Search filter for sectors
        sector_search = st.text_input(
            "Search sectors:",
            key="sector_search",
            placeholder="Type to filter..."
        )
        
        # Filter sector ETFs based on search
        filtered_sectors = SECTOR_ETFS
        if sector_search:
            filtered_sectors = [
                (ticker, name) for ticker, name in SECTOR_ETFS
                if sector_search.lower() in name.lower() or sector_search.lower() in ticker.lower()
            ]
        
        # Create checkboxes for sector ETFs
        for ticker, display_name in filtered_sectors:
            is_selected = ticker in st.session_state.selected_sector_etfs
            if st.checkbox(
                f"{display_name} ({ticker})",
                value=is_selected,
                key=f"sector_{ticker}"
            ):
                if ticker not in st.session_state.selected_sector_etfs:
                    st.session_state.selected_sector_etfs.append(ticker)
            else:
                if ticker in st.session_state.selected_sector_etfs:
                    st.session_state.selected_sector_etfs.remove(ticker)
        
        # Show selection count
        st.caption(f"Selected: {len(st.session_state.selected_sector_etfs)} sectors")

def create_level2_permanent_expansion():
    """Level 2: Add new tickers to permanent predefined lists"""
    st.sidebar.subheader("➕ Level 2: Expand Permanent Lists")
    
    # Add to Country ETFs
    with st.sidebar.expander("🌍 Add New Country ETF", expanded=False):
        new_country_ticker = st.text_input(
            "Country ETF Ticker:",
            key="new_country_ticker",
            placeholder="e.g., EWK"
        ).upper().strip()
        
        new_country_name = st.text_input(
            "Display Name:",
            key="new_country_name",
            placeholder="e.g., Belgium"
        ).strip()
        
        if st.button("Add Country ETF", key="add_country_etf"):
            if new_country_ticker and new_country_name:
                # Check if already exists
                existing_tickers = [item[0] for item in st.session_state.permanent_country_additions]
                if new_country_ticker not in existing_tickers:
                    st.session_state.permanent_country_additions.append((new_country_ticker, new_country_name))
                    # Auto-select the newly added ticker
                    if new_country_ticker not in st.session_state.selected_country_etfs:
                        st.session_state.selected_country_etfs.append(new_country_ticker)
                    st.success(f"✅ Added {new_country_name} ({new_country_ticker}) to country ETFs")
                else:
                    st.warning(f"⚠️ {new_country_ticker} already exists in your additions")
            else:
                st.error("❌ Please enter both ticker and display name")
        
        # Show current permanent additions
        if st.session_state.permanent_country_additions:
            st.caption("Your additions:")
            for ticker, name in st.session_state.permanent_country_additions:
                st.caption(f"• {name} ({ticker})")
    
    # Add to Sector ETFs
    with st.sidebar.expander("🏭 Add New Sector ETF", expanded=False):
        new_sector_ticker = st.text_input(
            "Sector ETF Ticker:",
            key="new_sector_ticker",
            placeholder="e.g., JETS"
        ).upper().strip()
        
        new_sector_name = st.text_input(
            "Display Name:",
            key="new_sector_name",
            placeholder="e.g., Airlines"
        ).strip()
        
        if st.button("Add Sector ETF", key="add_sector_etf"):
            if new_sector_ticker and new_sector_name:
                # Check if already exists
                existing_tickers = [item[0] for item in st.session_state.permanent_sector_additions]
                if new_sector_ticker not in existing_tickers:
                    st.session_state.permanent_sector_additions.append((new_sector_ticker, new_sector_name))
                    # Auto-select the newly added ticker
                    if new_sector_ticker not in st.session_state.selected_sector_etfs:
                        st.session_state.selected_sector_etfs.append(new_sector_ticker)
                    st.success(f"✅ Added {new_sector_name} ({new_sector_ticker}) to sector ETFs")
                else:
                    st.warning(f"⚠️ {new_sector_ticker} already exists in your additions")
            else:
                st.error("❌ Please enter both ticker and display name")
        
        # Show current permanent additions
        if st.session_state.permanent_sector_additions:
            st.caption("Your additions:")
            for ticker, name in st.session_state.permanent_sector_additions:
                st.caption(f"• {name} ({ticker})")

def create_level3_session_custom():
    """Level 3: Session-only custom tickers with configurable limit"""
    st.sidebar.subheader("🎯 Level 3: Session Custom Tickers")
    
    # Configurable ticker limit
    st.session_state.custom_ticker_limit = st.sidebar.slider(
        "Max custom tickers:",
        min_value=5,
        max_value=50,
        value=st.session_state.custom_ticker_limit,
        help="Higher limits may slow analysis"
    )
    
    # Performance warning
    if st.session_state.custom_ticker_limit > 20:
        st.sidebar.warning("⚠️ Large ticker counts may slow analysis")
    
    # Add ticker(s) - unified input for single or multiple
    ticker_input = st.sidebar.text_area(
        "Add Ticker(s):",
        key="custom_ticker_input",
        placeholder="Single: TSLA\nMultiple: AAPL, MSFT, GOOGL\n(comma or line separated)",
        height=80
    )
    
    if st.sidebar.button("Add Ticker(s)", key="add_custom_tickers"):
        if ticker_input.strip():
            # Parse input (reuse bulk parsing logic)
            parsed_tickers = []
            for line in ticker_input.replace(',', '\n').split('\n'):
                ticker = line.strip().upper()
                if ticker and ticker not in parsed_tickers:
                    parsed_tickers.append(ticker)
            
            # Add tickers respecting limit
            added_count = 0
            current_count = len(st.session_state.session_custom_tickers)
            
            for ticker in parsed_tickers:
                if current_count + added_count < st.session_state.custom_ticker_limit:
                    if ticker not in st.session_state.session_custom_tickers:
                        st.session_state.session_custom_tickers.append(ticker)
                        added_count += 1
                else:
                    break
            
            if added_count > 0:
                st.success(f"✅ Added {added_count} ticker{'s' if added_count != 1 else ''}")
            if added_count < len(parsed_tickers):
                remaining = len(parsed_tickers) - added_count
                st.warning(f"⚠️ {remaining} ticker{'s' if remaining != 1 else ''} skipped (limit reached)")
        else:
            st.error("❌ Enter at least one ticker symbol")
    
    # Display current custom tickers with remove functionality
    if st.session_state.session_custom_tickers:
        st.sidebar.write("**Current custom tickers:**")
        
        # Show count
        count = len(st.session_state.session_custom_tickers)
        limit = st.session_state.custom_ticker_limit
        st.sidebar.caption(f"Selected: {count}/{limit} tickers")
        
        # Tag-style display with remove buttons
        tickers_to_remove = []
        for i, ticker in enumerate(st.session_state.session_custom_tickers):
            col1, col2 = st.sidebar.columns([3, 1])
            with col1:
                st.write(f"🏷️ {ticker}")
            with col2:
                if st.button("❌", key=f"remove_custom_{i}", help=f"Remove {ticker}"):
                    tickers_to_remove.append(ticker)
        
        # Remove tickers (done after iteration to avoid modification during iteration)
        for ticker in tickers_to_remove:
            st.session_state.session_custom_tickers.remove(ticker)
            st.success(f"✅ Removed {ticker}")
            st.rerun()
        
        # Clear all button
        if st.sidebar.button("🗑️ Clear All Custom", key="clear_all_custom"):
            st.session_state.session_custom_tickers = []
            st.success("✅ Cleared all custom tickers")
            st.rerun()
    
    # Database save toggle
    st.sidebar.markdown("---")
    st.session_state.save_custom_to_database = st.sidebar.checkbox(
        "💾 Save custom tickers to database",
        value=st.session_state.save_custom_to_database,
        help="When checked, custom ticker data will be permanently cached for faster future access"
    )


def create_sidebar_controls():
    """Create sidebar controls for bucket-based ticker management"""
    st.sidebar.title("⚙️ Dashboard Controls")

    # STEP 0: Analysis Mode Selection
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Analysis Mode")
    
    st.session_state.selected_analysis_mode = st.sidebar.radio(
        "Choose analysis type:",
        options=['price', 'volume'],
        format_func=lambda x: {
            'price': '💰 Price Performance',
            'volume': '📊 Volume Performance'
        }[x],
        index=['price', 'volume'].index(st.session_state.selected_analysis_mode),
        key='analysis_mode_selection'
    )

    # STEP 1: Bucket Selection
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Select Analysis Bucket")

    st.session_state.selected_bucket = st.sidebar.radio(
        "Choose your analysis focus:",
        options=['country', 'sector', 'custom'],
        format_func=lambda x: {
            'country': '🌍 Country ETFs',
            'sector': '🏭 Sector ETFs', 
            'custom': '🎯 Custom Stocks'
        }[x],
        index=['country', 'sector', 'custom'].index(st.session_state.selected_bucket),
        key='bucket_selection'
    )

    # Show current selection
    bucket_names = {
        'country': 'Country ETFs',
        'sector': 'Sector ETFs',
        'custom': 'Custom Stocks'
    }
    st.sidebar.info(f"Currently analyzing: **{bucket_names[st.session_state.selected_bucket]}**")

    # STEP 3 & 4: Filter and temporarily augment the selected bucket.
    #
    # Persistent bucket membership/order/display names come from UniverseManager.
    # Checkbox visibility and ad hoc ticker additions remain session-only.
    st.sidebar.markdown("---")
    st.sidebar.subheader(
        f"🔧 Modify/Filter "
        f"{bucket_names[st.session_state.selected_bucket]}"
    )

    universe_manager = UniverseManager()

    selected_bucket_name = {
        "country": "Country",
        "sector": "Sector",
        "custom": "Custom",
    }[st.session_state.selected_bucket]

    bucket_records = universe_manager.get_bucket_records(
        selected_bucket_name
    )

    persistent_bucket_tickers = [
        record.ticker
        for record in bucket_records
    ]

    persistent_ticker_names = {
        record.ticker: record.display_name
        for record in bucket_records
    }

    if st.session_state.selected_bucket == 'country':
        if not st.session_state.country_visible_tickers:
            st.session_state.country_visible_tickers = (
                persistent_bucket_tickers.copy()
            )

        with st.sidebar.expander(
            "📋 Show/Hide Country ETFs",
            expanded=False,
        ):
            for record in bucket_records:
                ticker = record.ticker
                display_name = record.display_name

                is_visible = (
                    ticker
                    in st.session_state.country_visible_tickers
                )

                if st.checkbox(
                    f"{display_name} ({ticker})",
                    value=is_visible,
                    key=f"filter_country_{ticker}",
                ):
                    if (
                        ticker
                        not in st.session_state.country_visible_tickers
                    ):
                        st.session_state.country_visible_tickers.append(
                            ticker
                        )
                else:
                    if ticker in st.session_state.country_visible_tickers:
                        st.session_state.country_visible_tickers.remove(
                            ticker
                        )

            st.caption(
                f"Showing: "
                f"{len(st.session_state.country_visible_tickers)}/"
                f"{len(persistent_bucket_tickers)} country ETFs"
            )

        with st.sidebar.expander(
            "➕ Add Temporary Country Ticker",
            expanded=False,
        ):
            new_country_ticker = st.text_input(
                "Ticker:",
                key="new_country_ticker_step4",
                placeholder="e.g., EWK",
                help=(
                    "Add a ticker to this dashboard session only. "
                    "This does not add universe membership or store OHLCV."
                ),
            ).upper().strip()

            if st.button(
                "Add Temporary Ticker",
                key="add_country_step4",
            ):
                if new_country_ticker:
                    if (
                        new_country_ticker
                        not in st.session_state.country_visible_tickers
                    ):
                        st.session_state.country_visible_tickers.append(
                            new_country_ticker
                        )
                        st.success(
                            f"✅ Added {new_country_ticker} "
                            "to this Country view"
                        )
                    else:
                        st.warning(
                            f"⚠️ {new_country_ticker} "
                            "already in this view"
                        )
                else:
                    st.error("❌ Enter a ticker symbol")

    elif st.session_state.selected_bucket == 'sector':
        if not st.session_state.sector_visible_tickers:
            st.session_state.sector_visible_tickers = (
                persistent_bucket_tickers.copy()
            )

        with st.sidebar.expander(
            "📋 Show/Hide Sector ETFs",
            expanded=False,
        ):
            for record in bucket_records:
                ticker = record.ticker
                display_name = record.display_name

                is_visible = (
                    ticker
                    in st.session_state.sector_visible_tickers
                )

                if st.checkbox(
                    f"{display_name} ({ticker})",
                    value=is_visible,
                    key=f"filter_sector_{ticker}",
                ):
                    if (
                        ticker
                        not in st.session_state.sector_visible_tickers
                    ):
                        st.session_state.sector_visible_tickers.append(
                            ticker
                        )
                else:
                    if ticker in st.session_state.sector_visible_tickers:
                        st.session_state.sector_visible_tickers.remove(
                            ticker
                        )

            st.caption(
                f"Showing: "
                f"{len(st.session_state.sector_visible_tickers)}/"
                f"{len(persistent_bucket_tickers)} sector ETFs"
            )

        with st.sidebar.expander(
            "➕ Add Temporary Sector Ticker",
            expanded=False,
        ):
            new_sector_ticker = st.text_input(
                "Ticker:",
                key="new_sector_ticker_step4",
                placeholder="e.g., JETS",
                help=(
                    "Add a ticker to this dashboard session only. "
                    "This does not add universe membership or store OHLCV."
                ),
            ).upper().strip()

            if st.button(
                "Add Temporary Ticker",
                key="add_sector_step4",
            ):
                if new_sector_ticker:
                    if (
                        new_sector_ticker
                        not in st.session_state.sector_visible_tickers
                    ):
                        st.session_state.sector_visible_tickers.append(
                            new_sector_ticker
                        )
                        st.success(
                            f"✅ Added {new_sector_ticker} "
                            "to this Sector view"
                        )
                    else:
                        st.warning(
                            f"⚠️ {new_sector_ticker} "
                            "already in this view"
                        )
                else:
                    st.error("❌ Enter a ticker symbol")

    else:  # custom bucket
        if not st.session_state.custom_visible_tickers:
            st.session_state.custom_visible_tickers = (
                persistent_bucket_tickers.copy()
            )

        with st.sidebar.expander(
            "📋 Show/Hide Custom Stocks",
            expanded=True,
        ):
            for record in bucket_records:
                ticker = record.ticker
                display_name = record.display_name

                is_visible = (
                    ticker
                    in st.session_state.custom_visible_tickers
                )

                if st.checkbox(
                    f"{display_name} ({ticker})",
                    value=is_visible,
                    key=f"filter_custom_{ticker}",
                ):
                    if (
                        ticker
                        not in st.session_state.custom_visible_tickers
                    ):
                        st.session_state.custom_visible_tickers.append(
                            ticker
                        )
                else:
                    if ticker in st.session_state.custom_visible_tickers:
                        st.session_state.custom_visible_tickers.remove(
                            ticker
                        )

            st.caption(
                f"Showing: "
                f"{len(st.session_state.custom_visible_tickers)}/"
                f"{len(persistent_bucket_tickers)} custom stocks"
            )

        with st.sidebar.expander(
            "➕ Add Temporary Custom Ticker(s)",
            expanded=False,
        ):
            ticker_input = st.text_area(
                "Add Ticker(s):",
                key="custom_ticker_input_step4",
                placeholder=(
                    "Single: TSLA\n"
                    "Multiple: AAPL, MSFT, GOOGL\n"
                    "(comma or line separated)"
                ),
                height=80,
                help=(
                    "Add ticker(s) to this dashboard session only. "
                    "This does not add universe membership or store OHLCV."
                ),
            )

            if st.button(
                "Add Temporary Ticker(s)",
                key="add_custom_step4",
            ):
                if ticker_input.strip():
                    parsed_tickers = []

                    for line in (
                        ticker_input
                        .replace(',', '\n')
                        .split('\n')
                    ):
                        ticker = line.strip().upper()

                        if (
                            ticker
                            and ticker not in parsed_tickers
                        ):
                            parsed_tickers.append(
                                ticker
                            )

                    added_count = 0

                    for ticker in parsed_tickers:
                        if (
                            ticker
                            not in st.session_state.custom_visible_tickers
                        ):
                            st.session_state.custom_visible_tickers.append(
                                ticker
                            )
                            added_count += 1

                    if added_count > 0:
                        st.success(
                            f"✅ Added {added_count} "
                            f"temporary ticker"
                            f"{'s' if added_count != 1 else ''}"
                        )

                    if added_count < len(parsed_tickers):
                        skipped = (
                            len(parsed_tickers)
                            - added_count
                        )
                        st.info(
                            f"ℹ️ {skipped} ticker"
                            f"{'s' if skipped != 1 else ''} "
                            "already in this view"
                        )
                else:
                    st.error(
                        "❌ Enter at least one ticker symbol"
                    )

    # Ticker Aggregation Based on Selected Bucket
    st.sidebar.markdown("---")
    
    # Get final tickers based on bucket selection
    if st.session_state.selected_bucket == 'country':
        final_tickers = st.session_state.country_visible_tickers.copy()
    elif st.session_state.selected_bucket == 'sector':
        final_tickers = st.session_state.sector_visible_tickers.copy()
    else:  # custom bucket
        final_tickers = st.session_state.custom_visible_tickers.copy()
    
    # Remove duplicates while preserving order
    seen = set()
    deduplicated_tickers = []
    for ticker in final_tickers:
        if ticker not in seen:
            seen.add(ticker)
            deduplicated_tickers.append(ticker)
    
    final_tickers = deduplicated_tickers
    
    # Display current selection summary
    st.sidebar.success(f"✅ Total selected: {len(final_tickers)} tickers")
    st.sidebar.caption(f"Bucket: {bucket_names[st.session_state.selected_bucket]}")
    
    # Show preview
    preview_tickers = final_tickers[:5]
    preview_text = ", ".join(preview_tickers)
    if len(final_tickers) > 5:
        preview_text += f" +{len(final_tickers) - 5} more"
    st.sidebar.caption(f"Preview: {preview_text}")
    
    # Use bucket selection for asset group and title
    asset_group = st.session_state.selected_bucket
    
    bucket_titles = {
        'country': f"Country ETFs ({len(final_tickers)} tickers)",
        'sector': f"Sector ETFs ({len(final_tickers)} tickers)", 
        'custom': f"Custom Stocks ({len(final_tickers)} tickers)"
    }
    group_name = bucket_titles[st.session_state.selected_bucket]
    
    # Time Period Selection - conditional based on analysis mode
    st.sidebar.subheader("⏰ Time Period")
    
    if st.session_state.selected_analysis_mode == 'price':
        period_options = {
            "1 Day": "1d",
            "1 Week": "1w", 
            "1 Month": "1m",
            "3 Months": "3m",
            "6 Months": "6m",
            "Year to Date": "ytd",
            "1 Year": "1y"
        }
        period_label = "Compare against:"
    else:  # volume mode
        period_options = {
            "10 Days": "10d",
            "1 Week": "1w",
            "1 Month": "1m", 
            "60 Days": "60d"
        }
        period_label = "Volume benchmark period:"
    
    selected_period_name = st.sidebar.selectbox(
        period_label,
        options=list(period_options.keys()),
        index=0
    )
    selected_period = period_options[selected_period_name]

    if st.session_state.selected_analysis_mode == 'volume':
        view_last_complete_day = st.sidebar.toggle(
            "View last complete day",
            value=False,
            help=(
                "Off: use the latest available Volume observation. "
                "During market hours this is cumulative intraday volume. "
                "On: use the latest fully completed trading session."
            ),
            key='performance_volume_last_complete_day',
        )

        volume_view_mode = (
            'completed'
            if view_last_complete_day
            else 'live'
        )
    else:
        volume_view_mode = None
    
    # Refresh button
    st.sidebar.subheader("🔄 Data Refresh")
    refresh_button = st.sidebar.button(
        "🔄 Refresh Data",
        help="Fetch latest market data",
        use_container_width=True
    )
    
    return {
        'group': asset_group,
        'group_name': group_name,
        'tickers': final_tickers,
        'ticker_names': persistent_ticker_names,
        'period': selected_period,
        'period_name': selected_period_name,
        'refresh': refresh_button,
        'analysis_mode': st.session_state.selected_analysis_mode,
        'volume_view_mode': volume_view_mode,
    }


def create_header():
    """Create the main header section"""
    st.title("📈 Stock Performance Heatmap Dashboard")
    
    # Description
    st.markdown("""
    Interactive financial heatmap inspired by Finviz, showing price performance 
    across different time periods. Select asset groups and time periods from the sidebar.
    """)
    
    # Color legend
    with st.expander("🎨 Color Legend", expanded=False):
        legend_data = get_color_legend()
        
        cols = st.columns(len(legend_data))
        for i, (description, color) in enumerate(legend_data.items()):
            with cols[i]:
                st.markdown(
                    f'<div style="background-color: {color}; padding: 10px; '
                    f'border-radius: 5px; text-align: center; color: white; '
                    f'font-weight: bold; margin: 2px;">{description}</div>',
                    unsafe_allow_html=True
                )

def fetch_performance_data(tickers, period, save_to_db: bool = True):
    """Fetch performance data with progress tracking and database usage reporting"""
    with st.spinner(f"Fetching data for {len(tickers)} tickers..."):
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        calculator = st.session_state.calculator
        
        # Use the group calculation method for better efficiency
        status_text.text(f"Processing {len(tickers)} tickers using database-first approach...")
        
        try:
            performance_data = (
                calculator.calculate_performance_for_group(
                    tickers,
                    period,
                    save_to_db=save_to_db,
                )
            )

            volume_calculator = (
                st.session_state.volume_calculator
            )

            for item in performance_data:
                if item.get('error', False):
                    continue

                price_metadata = (
                    item.get('current_price_metadata')
                    or {}
                )
                current_volume = price_metadata.get(
                    'current_volume'
                )

                if current_volume is None:
                    item['live_volume_context'] = None
                    continue

                item['live_volume_context'] = (
                    volume_calculator.get_live_volume_context(
                        item['ticker'],
                        current_volume=current_volume,
                        save_to_db=save_to_db,
                    )
                )
            
            # Show database usage statistics
            summary = calculator.get_performance_summary(
                performance_data
            )
            
            progress_bar.progress(1.0)
            status_text.empty()
            
            # Display efficiency information
            if summary['database_usage'] > 0:
                st.success(
                    f"✅ Data fetched successfully! "
                    f"Database cache used for {summary['database_usage']}/{summary['valid_count']} tickers "
                    f"({summary['database_usage']/summary['valid_count']*100:.0f}% cache hit rate)"
                )
            else:
                st.info("ℹ️ Data fetched from yfinance (no database cache available)")
            
        except Exception as e:
            st.error(f"Error fetching performance data: {str(e)}")
            performance_data = []
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        return performance_data


def fetch_volume_data(
    tickers,
    period,
    observation_mode='live',
    save_to_db: bool = True,
):
    """Fetch volume data with progress tracking and database usage reporting"""
    with st.spinner(f"Fetching volume data for {len(tickers)} tickers..."):
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        volume_calculator = st.session_state.volume_calculator
        
        # Use the group calculation method for better efficiency
        status_text.text(f"Processing {len(tickers)} tickers using database-first approach...")
        
        try:
            if observation_mode == 'completed':
                volume_data = (
                    volume_calculator
                    .calculate_latest_completed_volume_performance_for_group(
                        tickers,
                        period,
                        save_to_db=save_to_db,
                    )
                )
            else:
                volume_data = (
                    volume_calculator
                    .calculate_live_volume_performance_for_group(
                        tickers,
                        period,
                        save_to_db=save_to_db,
                    )
                )
            
            # Show database usage statistics
            valid_count = len([v for v in volume_data if not v.get('error', False)])
            error_count = len([v for v in volume_data if v.get('error', False)])
            database_usage = len([v for v in volume_data if v.get('data_source') == 'database'])
            
            progress_bar.progress(1.0)
            status_text.empty()
            
            # Display efficiency information
            if observation_mode == 'live':
                st.success(
                    f"✅ Live Volume data updated for "
                    f"{valid_count} tickers"
                )
            elif database_usage > 0:
                cache_rate = (
                    database_usage / valid_count * 100
                    if valid_count > 0
                    else 0
                )
                st.success(
                    f"✅ Volume data fetched successfully! "
                    f"Database cache used for "
                    f"{database_usage}/{valid_count} tickers "
                    f"({cache_rate:.0f}% cache hit rate)"
                )
            else:
                st.info(
                    "ℹ️ Completed Volume data fetched from "
                    "yfinance (no database cache available)"
                )

        except Exception as e:
            st.error(f"Error fetching volume data: {str(e)}")
            volume_data = []
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        return volume_data

def display_summary_stats(
    performance_data,
    ticker_names=None,
):
    """Display summary statistics"""
    ticker_names = dict(
        ticker_names or {}
    )
    generator = st.session_state.heatmap_generator
    stats = generator.create_summary_stats(performance_data)
    
    # Main metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Tickers", 
            stats['total_tickers'],
            help="Number of tickers analyzed"
        )
    
    with col2:
        st.metric(
            "Valid Data", 
            stats['valid_data'],
            help="Tickers with successful data fetch"
        )
    
    with col3:
        avg_perf = stats['avg_performance']
        st.metric(
            "Average Performance",
            f"{avg_perf:+.2f}%",
            help="Average percentage change across all tickers"
        )
    
    with col4:
        pos_count = stats['positive_count']
        neg_count = stats['negative_count']
        if pos_count + neg_count > 0:
            pos_ratio = pos_count / (pos_count + neg_count) * 100
            st.metric(
                "Positive %",
                f"{pos_ratio:.1f}%",
                help="Percentage of tickers with positive performance"
            )
        else:
            st.metric("Positive %", "N/A")
    
    # Best/Worst performers
    valid_data = [
        item
        for item in performance_data
        if not item.get('error', False)
    ]

    performance_key = None

    if valid_data:
        if 'percentage_change' in valid_data[0]:
            performance_key = 'percentage_change'
        elif 'volume_change' in valid_data[0]:
            performance_key = 'volume_change'

    if performance_key:
        best_performers = sorted(
            valid_data,
            key=lambda item: item[performance_key],
            reverse=True,
        )[:5]

        worst_performers = sorted(
            valid_data,
            key=lambda item: item[performance_key],
        )[:5]

        col1, col2 = st.columns(2)

        with col1:
            best_lines = [
                (
                    f"{rank}. **{item['ticker']}** "
                    f"({item[performance_key]:+.1f}%)"
                    + (
                        f" - {ticker_names[item['ticker']]}"
                        if ticker_names.get(item['ticker'])
                        and ticker_names[item['ticker']]
                        != item['ticker']
                        else ""
                    )
                )
                for rank, item in enumerate(
                    best_performers,
                    start=1,
                )
            ]

            st.success(
                "🏆 **Best**\n\n"
                + "\n\n".join(best_lines)
            )

        with col2:
            worst_lines = [
                (
                    f"{rank}. **{item['ticker']}** "
                    f"({item[performance_key]:+.1f}%)"
                    + (
                        f" - {ticker_names[item['ticker']]}"
                        if ticker_names.get(item['ticker'])
                        and ticker_names[item['ticker']]
                        != item['ticker']
                        else ""
                    )
                )
                for rank, item in enumerate(
                    worst_performers,
                    start=1,
                )
            ]

            st.error(
                "📉 **Worst**\n\n"
                + "\n\n".join(worst_lines)
            )

def display_heatmap(
    performance_data,
    title,
    asset_group=None,
    tile_order='original',
    ticker_names=None,
):
    """Display the main heatmap visualization"""
    generator = st.session_state.heatmap_generator

    fig = generator.create_treemap(
        performance_data=performance_data,
        title=title,
        width=1200,
        height=700,
        asset_group=asset_group,
        tile_order=tile_order,
        ticker_names=ticker_names,
    )
    
    # Display with full width
    st.plotly_chart(fig, use_container_width=True)

def generate_ma_comment(
    ticker,
    period,
    ma_type,
    current_price,
    ma_value,
    price_vs_ma,
):
    """Generate a compact user-facing moving-average distance comment."""
    rounded_diff = round(float(price_vs_ma), 1)

    if rounded_diff > 0:
        reach_pct = abs(
            (ma_value - current_price)
            / current_price
            * 100
        )

        return (
            f"{ticker} is {abs(rounded_diff):.1f}% above its "
            f"{period}D {ma_type}. "
            f"It has to fall {reach_pct:.1f}% to reach it."
        )

    if rounded_diff < 0:
        reach_pct = abs(
            (ma_value - current_price)
            / current_price
            * 100
        )

        return (
            f"{ticker} is {abs(rounded_diff):.1f}% below its "
            f"{period}D {ma_type}. "
            f"It has to rise {reach_pct:.1f}% to reach it."
        )

    return f"{ticker} is at its {period}D {ma_type}."

def display_technical_indicators_cards(indicators_data):
    """Display technical indicators in card-based layout similar to Investing.com"""
    if not indicators_data:
        st.warning("No technical indicators data available")
        return
    
    # Define indicator display order and formatting
    indicator_configs = {
        'rsi_14': {
            'name': 'RSI (14)',
            'format': '{:.2f}',
            'description': 'Relative Strength Index'
        },
        'macd': {
            'name': 'MACD (12,26)',
            'format': '{:.3f}',
            'description': 'Moving Average Convergence Divergence'
        },
        'stochastic': {
            'name': 'STOCH (9,6)',
            'format': '{:.2f}',
            'description': 'Stochastic Oscillator'
        },
        'adx': {
            'name': 'ADX (14)',
            'format': '{:.2f}',
            'description': 'Average Directional Index'
        },
        'elder_ray': {
            'name': 'Bull/Bear Power',
            'format': '{:.3f}',
            'description': 'Elder-ray System'
        },
        'atr_14': {
            'name': 'ATR (14)',
            'format': '{:.2f}',
            'description': 'Average True Range'
        },
        'williams_r': {
            'name': 'Williams %R',
            'format': '{:.2f}',
            'description': 'Williams Percent Range'
        },
        'cci_14': {
            'name': 'CCI (14)',
            'format': '{:.2f}',
            'description': 'Commodity Channel Index'
        },
        'ultimate_osc': {
            'name': 'Ultimate Osc',
            'format': '{:.2f}',
            'description': 'Ultimate Oscillator'
        },
        'roc_12': {
            'name': 'ROC (12)',
            'format': '{:.2f}',
            'description': 'Rate of Change'
        }
    }
    
    # Create responsive grid layout - 3 columns for 10 indicators
    cols = st.columns(3)
    
    col_index = 0
    for indicator_key, config in indicator_configs.items():
        if indicator_key in indicators_data:
            indicator = indicators_data[indicator_key]
            
            with cols[col_index % 3]:
                _display_indicator_card(
                    indicator_key,
                    config,
                    indicator
                )
            
            col_index += 1

def _display_indicator_card(indicator_key, config, indicator_data):
    """Display individual technical indicator card"""
    
    # Extract signal information
    signal_info = indicator_data.get('signal', {})
    signal = signal_info.get('signal', 'N/A')
    description = signal_info.get('description', '')
    
    # Get indicator value(s)
    if indicator_key == 'macd':
        value = indicator_data.get('value', 0)
        signal_line = indicator_data.get('signal_line', 0)
        display_value = f"{value:.3f} / {signal_line:.3f}"
    elif indicator_key == 'stochastic':
        k_value = indicator_data.get('k', 0)
        d_value = indicator_data.get('d', 0)
        display_value = f"%K: {k_value:.2f}, %D: {d_value:.2f}"
    elif indicator_key == 'adx':
        adx_value = indicator_data.get('value', 0)
        plus_di = indicator_data.get('plus_di', 0)
        minus_di = indicator_data.get('minus_di', 0)
        display_value = f"{adx_value:.2f} (+DI: {plus_di:.2f}, -DI: {minus_di:.2f})"
    elif indicator_key == 'elder_ray':
        bull_power = indicator_data.get('bull_power', 0)
        bear_power = indicator_data.get('bear_power', 0)
        # UPDATE 12/29
        #bull_power = indicator_data.get('bull_power')
        #bear_power = indicator_data.get('bear_power')
        #bull_power = 0.0 if bull_power is None else float(bull_power)
        #bear_power = 0.0 if bear_power is None else float(bear_power)
        display_value = f"Bull: {bull_power:.3f}, Bear: {bear_power:.3f}"
    else:
        value = indicator_data.get('value', 0)
        # Handle None values gracefully
        if value is None:
            display_value = "N/A"
        else:
            display_value = config['format'].format(value)
    
    # Determine signal color
    signal_colors = {
        'Buy': '🟢',
        'Strong Buy': '🟢',
        'Sell': '🔴', 
        'Strong Sell': '🔴',
        'Neutral': '⚪',
        'N/A': '⚫'
    }
    
    signal_color = signal_colors.get(signal, '⚪')
    
    # Generate contextual comment
    comment = _generate_indicator_comment(indicator_key, indicator_data, signal_info)
    
    # Create card using container
    with st.container():
        st.markdown(f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            background-color: #fafafa;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h4 style="margin: 0; color: #333;">{config['name']}</h4>
                <span style="font-size: 18px;">{signal_color}</span>
            </div>
            <div style="margin-bottom: 8px;">
                <strong style="font-size: 18px; color: #333;">{display_value}</strong>
            </div>
            <div style="margin-bottom: 8px;">
                <span style="
                    background-color: {'#d4edda' if 'Buy' in signal else '#f8d7da' if 'Sell' in signal else '#e2e3e5'};
                    color: {'#155724' if 'Buy' in signal else '#721c24' if 'Sell' in signal else '#383d41'};
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: bold;
                ">{signal}</span>
            </div>
            <div style="font-size: 14px; color: #666; line-height: 1.4;">
                {comment}
            </div>
        </div>
        """, unsafe_allow_html=True)

def _generate_indicator_comment(indicator_key, indicator_data, signal_info):
    """Generate contextual comments for technical indicators using signal_info to avoid duplication"""
    
    signal = signal_info.get('signal', 'N/A')
    description = signal_info.get('description', '')
    
    if indicator_key == 'rsi_14':
        value = indicator_data.get('value', 0)
        # Use signal_info description and add contextual value information
        base_comment = description or f"RSI signal: {signal}"
        return f"RSI at {value:.1f}. {base_comment}"
    
    elif indicator_key == 'macd':
        value = indicator_data.get('value', 0)
        signal_line = indicator_data.get('signal_line', 0)
        base_comment = description or f"MACD signal: {signal}"
        return f"MACD at {value:.3f} (Signal: {signal_line:.3f}). {base_comment}"
    
    elif indicator_key == 'stochastic':
        k_value = indicator_data.get('k', 0)
        d_value = indicator_data.get('d', 0)
        base_comment = description or f"Stochastic signal: {signal}"
        return f"Stochastic %K: {k_value:.1f}, %D: {d_value:.1f}. {base_comment}"
    
    elif indicator_key == 'adx':
        adx_value = indicator_data.get('value', 0)
        plus_di = indicator_data.get('plus_di', 0)
        minus_di = indicator_data.get('minus_di', 0)
        base_comment = description or f"ADX signal: {signal}"
        return f"ADX: {adx_value:.1f} (+DI: {plus_di:.1f}, -DI: {minus_di:.1f}). {base_comment}"
    
    elif indicator_key == 'elder_ray':
        bull_power = indicator_data.get('bull_power', 0)
        bear_power = indicator_data.get('bear_power', 0)
        # UPDATE 12/29
        #bull_power = indicator_data.get('bull_power')
        #bear_power = indicator_data.get('bear_power')
        #bull_power = 0.0 if bull_power is None else float(bull_power)
        #bear_power = 0.0 if bear_power is None else float(bear_power)
        base_comment = description or f"Elder Ray signal: {signal}"
        return f"Bull Power: {bull_power:.3f}, Bear Power: {bear_power:.3f}. {base_comment}"
    
    elif indicator_key == 'atr_14':
        value = indicator_data.get('value', 0)
        return f"ATR at {value:.2f} measures current volatility. Higher values indicate increased price movement potential."
    
    elif indicator_key == 'williams_r':
        value = indicator_data.get('value', 0)
        base_comment = description or f"Williams %R signal: {signal}"
        return f"Williams %R at {value:.1f}. {base_comment}"
    
    elif indicator_key == 'cci_14':
        value = indicator_data.get('value', 0)
        base_comment = description or f"CCI signal: {signal}"
        return f"CCI at {value:.1f}. {base_comment}"
    
    elif indicator_key == 'ultimate_osc':
        value = indicator_data.get('value', 0)
        base_comment = description or f"Ultimate Oscillator signal: {signal}"
        return f"Ultimate Oscillator at {value:.1f}. {base_comment}"
    
    elif indicator_key == 'roc_12':
        value = indicator_data.get('value', 0)
        base_comment = description or f"ROC signal: {signal}"
        return f"ROC at {value:.2f}%. {base_comment}"
    
    # Fallback to signal description
    return description or f"{signal} signal detected."

def display_moving_averages_table(ma_data):
    """Display compact tabbed SMA and EMA analysis tables."""
    if not ma_data or ma_data.get('error'):
        message = (
            ma_data.get('message', 'Unknown error')
            if ma_data
            else 'Unknown error'
        )
        st.error(f"Error loading moving averages: {message}")
        return

    ticker = ma_data['ticker']
    current_price = float(ma_data['current_price'])
    periods_data = ma_data['periods']

    effective_date_raw = (
        ma_data.get('price_effective_date')
        or ma_data.get('calculation_date')
    )
    effective_timestamp_raw = ma_data.get(
        'price_effective_timestamp'
    )

    effective_date = pd.to_datetime(
        effective_date_raw,
        errors='coerce',
    )
    effective_timestamp = pd.to_datetime(
        effective_timestamp_raw,
        errors='coerce',
    )

    if pd.notna(effective_timestamp):
        if effective_timestamp.tzinfo is None:
            effective_timestamp = (
                effective_timestamp.tz_localize(
                    'America/New_York'
                )
            )
        else:
            effective_timestamp = (
                effective_timestamp.tz_convert(
                    'America/New_York'
                )
            )

    today = pd.Timestamp.now(
        tz='America/New_York'
    ).date()

    if pd.notna(effective_date):
        date_text = (
            f"{effective_date.month}/"
            f"{effective_date.day}/"
            f"{effective_date.strftime('%y')}"
        )
    else:
        date_text = 'date unavailable'

    if (
        pd.notna(effective_timestamp)
        and effective_timestamp.date() == today
    ):
        hour_12 = effective_timestamp.hour % 12 or 12
        meridiem = (
            'A'
            if effective_timestamp.hour < 12
            else 'P'
        )
        time_text = (
            f"{hour_12}:"
            f"{effective_timestamp.minute:02d}"
            f"{meridiem}"
        )

        price_label = (
            f"Latest Price: ${current_price:.2f} "
            f"({date_text} @ {time_text})"
        )
    else:
        price_label = (
            f"Latest Price: ${current_price:.2f} "
            f"({date_text})"
        )

    st.caption(price_label)

    periods_by_type = {
        'SMA': [
            5,
            9,
            10,
            20,
            21,
            50,
            100,
            200,
            250,
        ],
        'EMA': [
            5,
            9,
            10,
            20,
            21,
            50,
            100,
            200,
        ],
    }

    def build_table(ma_type):
        rows = []
        key = ma_type.lower()

        for period in periods_by_type[ma_type]:
            period_data = (
                periods_data
                .get(f'MA{period}', {})
                .get(key)
            )

            if not period_data:
                continue

            ma_value = float(period_data['value'])
            price_vs_ma = float(
                period_data['price_vs_ma']
            )
            signal_payload = (
                period_data.get('signal')
                or {}
            )

            if price_vs_ma > 0:
                price_vs_text = (
                    f"+{abs(price_vs_ma):.1f}% above"
                )
            elif price_vs_ma < 0:
                price_vs_text = (
                    f"-{abs(price_vs_ma):.1f}% below"
                )
            else:
                price_vs_text = "0.0% at MA"

            rows.append({
                'Period': f'{ma_type}({period})',
                'MA Value': f'${ma_value:.2f}',
                'Price vs MA': price_vs_text,
                'Signal': signal_payload.get(
                    'signal',
                    'N/A',
                ),
                'Strength': signal_payload.get(
                    'strength',
                    'N/A',
                ),
                'Comment': generate_ma_comment(
                    ticker,
                    period,
                    ma_type,
                    current_price,
                    ma_value,
                    price_vs_ma,
                ),
                '_price_vs_ma_numeric': price_vs_ma,
            })

        return pd.DataFrame(rows)

    def render_table(ma_type):
        table_df = build_table(ma_type)

        if table_df.empty:
            st.info(f"No {ma_type} data available.")
            return

        display_df = table_df.drop(
            columns=['_price_vs_ma_numeric']
        )

        st.dataframe(
            display_df,
            column_config={
                'Period': (
                    st.column_config.TextColumn(
                        'Period',
                        width='small',
                    )
                ),
                'MA Value': (
                    st.column_config.TextColumn(
                        'MA Value',
                        width='small',
                    )
                ),
                'Price vs MA': (
                    st.column_config.TextColumn(
                        'Price vs MA',
                        width='small',
                    )
                ),
                'Signal': (
                    st.column_config.TextColumn(
                        'Signal',
                        width='small',
                    )
                ),
                'Strength': (
                    st.column_config.TextColumn(
                        'Strength',
                        width='small',
                    )
                ),
                'Comment': (
                    st.column_config.TextColumn(
                        'Comment',
                        width='large',
                    )
                ),
            },
            hide_index=True,
            use_container_width=True,
        )

    sma_tab, ema_tab = st.tabs(['SMA', 'EMA'])

    with sma_tab:
        render_table('SMA')

    with ema_tab:
        render_table('EMA')

def display_pivot_points(ticker: str, pivot_data: Dict, current_price: float) -> None:
    """
    Display pivot points analysis - All 4 pivot types side-by-side
    
    Args:
        ticker: Stock ticker symbol
        pivot_data: Dictionary with pivot calculations (classic, fibonacci, camarilla, woodys)
        current_price: Current stock price
    """
    if pivot_data.get('error'):
        st.error(f"Error calculating pivot points: {pivot_data.get('message', 'Unknown error')}")
        return
    
    # Display calculation metadata
    st.caption(f"Calculated using {pivot_data.get('ohlc_date', 'N/A')} OHLC data (previous trading day)")
    
    # Extract all pivot types
    classic = pivot_data.get('classic')
    fibonacci = pivot_data.get('fibonacci')
    camarilla = pivot_data.get('camarilla')
    woodys = pivot_data.get('woodys')
    
    # Check if we have at least one pivot type
    if not any([classic, fibonacci, camarilla, woodys]):
        st.warning("No pivot data available")
        return
    
    # Build DataFrame for side-by-side display
    pivot_levels = ['R3', 'R2', 'R1', 'Pivot', 'S1', 'S2', 'S3']
    pivot_keys = ['r3', 'r2', 'r1', 'pivot', 's1', 's2', 's3']
    
    table_data = []
    for level_name, level_key in zip(pivot_levels, pivot_keys):
        row = {'Level': level_name}
        
        # Add Classic
        if classic and level_key in classic:
            row['Classic'] = f"${classic[level_key]:.2f}"
        else:
            row['Classic'] = "N/A"
        
        # Add Fibonacci
        if fibonacci and level_key in fibonacci:
            row['Fibonacci'] = f"${fibonacci[level_key]:.2f}"
        else:
            row['Fibonacci'] = "N/A"
        
        # Add Camarilla
        if camarilla and level_key in camarilla:
            row['Camarilla'] = f"${camarilla[level_key]:.2f}"
        else:
            row['Camarilla'] = "N/A"
        
        # Add Woody's
        if woodys and level_key in woodys:
            row["Woody's"] = f"${woodys[level_key]:.2f}"
        else:
            row["Woody's"] = "N/A"
        
        table_data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(table_data)
    
    # Display as styled table
    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Level": st.column_config.TextColumn("Level", width="small"),
            "Classic": st.column_config.TextColumn("Classic", width="medium"),
            "Fibonacci": st.column_config.TextColumn("Fibonacci", width="medium"),
            "Camarilla": st.column_config.TextColumn("Camarilla", width="medium"),
            "Woody's": st.column_config.TextColumn("Woody's", width="medium")
        }
    )
    
    st.caption(f"Current Price: ${current_price:.2f}")

def display_data_table(performance_data):
    """Display detailed data table for both price and volume data"""
    if not performance_data:
        return
    
    # Filter valid data and create DataFrame
    valid_data = [
        p
        for p in performance_data
        if not p.get('error', False)
    ]
    
    if not valid_data:
        st.warning("No valid data to display in table")
        return
    
    # Detect data type and create appropriate DataFrame
    if 'percentage_change' in valid_data[0]:
        # Price performance data.
        #
        # Keep numeric values numeric so Streamlit header sorting remains
        # numeric rather than lexicographic. Display formatting is handled
        # separately through column_config.
        df_display = pd.DataFrame([
            {
                'Ticker': p['ticker'],
                'Current Price': (
                    p['current_price']
                    if p.get('current_price') is not None
                    else None
                ),
                'Historical Price': (
                    p['historical_price']
                    if p.get('historical_price') is not None
                    else None
                ),
                'Absolute Change': (
                    p['absolute_change']
                    if p.get('absolute_change') is not None
                    else None
                ),
                'Percentage Change': (
                    p['percentage_change']
                    if p.get('percentage_change') is not None
                    else None
                ),
                'Period': p.get(
                    'period_label',
                    p.get('period', 'N/A')
                ),
            }
            for p in valid_data
        ])

        # Initial display order: highest percentage change first.
        df_display = df_display.sort_values(
            'Percentage Change',
            ascending=False,
            na_position='last',
        )

        column_config = {
            'Current Price': st.column_config.NumberColumn(
                'Current Price',
                format='$%.2f',
            ),
            'Historical Price': st.column_config.NumberColumn(
                'Historical Price',
                format='$%.2f',
            ),
            'Absolute Change': st.column_config.NumberColumn(
                'Absolute Change',
                format='$%+.2f',
            ),
            'Percentage Change': st.column_config.NumberColumn(
                'Percentage Change',
                format='%+.2f%%',
            ),
        }
            
    elif 'volume_change' in valid_data[0]:
        # Volume performance data.
        #
        # Preserve numeric values and let Streamlit handle presentation.
        # This keeps interactive header sorting numeric.
        df_display = pd.DataFrame([
            {
                'Ticker': p['ticker'],
                'Current Volume': (
                    int(round(p['current_volume']))
                    if p.get('current_volume') is not None
                    else None
                ),
                'Benchmark Average': (
                    int(round(p['benchmark_average']))
                    if p.get('benchmark_average') is not None
                    else None
                ),
                'Volume Change': (
                    p['volume_change']
                    if p.get('volume_change') is not None
                    else None
                ),
                'Benchmark Period': p.get(
                    'benchmark_label',
                    p.get('benchmark_period', 'N/A')
                ),
            }
            for p in valid_data
        ])

        # Initial display order: highest volume change first.
        df_display = df_display.sort_values(
            'Volume Change',
            ascending=False,
            na_position='last',
        )

        column_config = {
            'Current Volume': st.column_config.NumberColumn(
                'Current Volume',
                format='localized',
            ),
            'Benchmark Average': st.column_config.NumberColumn(
                'Benchmark Average',
                format='localized',
            ),
            'Volume Change': st.column_config.NumberColumn(
                'Volume Change',
                format='%+.2f%%',
            ),
        }
    else:
        # Unknown data structure
        st.warning("Unknown data format - cannot display table")
        return
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
    )


def _extract_rolling_signals_from_data(data: dict) -> dict:
    rs = data.get("rolling_signals") or {}
    meta = {k: rs.get(k) for k in ("engine", "status", "ticker") if k in rs}

    # A) Already close to contract: rs has 'dates' and 'rows'
    if isinstance(rs.get("dates"), list) and isinstance(rs.get("rows"), dict):
        extras = rs.get("extras") if isinstance(rs.get("extras"), dict) else {}
        return {"meta": meta, "dates": rs["dates"], "rows": rs["rows"], "extras": extras}

    # B) Term-block style: rs has {short_term: {...}, intermediate_term: {...}, long_term: {...}}
    for term_key in ("short_term", "intermediate_term", "long_term"):
        block = rs.get(term_key)
        if isinstance(block, dict):
            dates = block.get("dates")
            rows = block.get("rows")
            if isinstance(dates, list) and isinstance(rows, dict):
                extras = block.get("extras") if isinstance(block.get("extras"), dict) else {}
                return {"meta": meta, "dates": dates, "rows": rows, "extras": extras}

    # C) Current engine shape: top-level dates + term-block data dict
    # short_term: { indicators: [...], data: {date: {indicator_key: {value, score, hover}}}}
    if isinstance(rs.get("dates"), list):
        rs_dates = rs["dates"]

        for term_key in ("short_term", "intermediate_term", "long_term"):
            block = rs.get(term_key)
            if not isinstance(block, dict):
                continue

            data_by_date = block.get("data")
            if not isinstance(data_by_date, dict):
                continue

            indicators = block.get("indicators")
            if not isinstance(indicators, list):
                first_day = next(iter(data_by_date.values()), {})
                indicators = list(first_day.keys()) if isinstance(first_day, dict) else []

            rows: dict = {}
            for ind_key in indicators:
                vals, scores, hovers, extras_list = [], [], [], []

                for d in rs_dates:
                    cell = (data_by_date.get(d, {}) or {}).get(ind_key, {}) or {}
                    vals.append(cell.get("value"))
                    scores.append(cell.get("score"))
                    hovers.append(cell.get("hover"))
                    extras_list.append(cell.get("extras") if isinstance(cell.get("extras"), dict) else {})

                # Skip rows that contain nothing (prevents blank/ghost rows)
                has_any = any(v is not None for v in vals) or any(s is not None for s in scores)
                if not has_any:
                    continue

                rows[ind_key] = {
                    "display_name": ind_key,
                    "values": vals,
                    "scores": scores,
                    "hover": hovers,
                    "extras": extras_list,
                }

            extras = rs.get("extras") if isinstance(rs.get("extras"), dict) else {}
            return {"meta": meta, "dates": rs_dates, "rows": rows, "extras": extras}

    # Fallback: empty
    return {"meta": meta, "dates": [], "rows": {}, "extras": {}}

def show_technical_analysis_dashboard():
    """Dashboard 1: Single Stock Technical Analysis"""
    st.title("🎯 Technical Analysis Dashboard")
    
    # Description
    st.markdown("""
    Comprehensive technical analysis for individual stocks with moving averages,
    technical indicators, and signal analysis.
    """)
    
    # Ticker input section
    st.subheader("📊 Stock Selection")
    
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Symbol:",
            value="NVDA",
            placeholder="e.g., AAPL, MSFT, GOOGL",
            help="Enter any valid stock ticker symbol"
        ).upper().strip()

    # Ensure rolling days selector state exists before any compute gating reads it.
    if "rh_days_selector" not in st.session_state:
        st.session_state.rh_days_selector = int(st.session_state.get("technical_analysis_rolling_days", 10))
    
    with col2:
        # Save to database checkbox (only for non-bucket tickers)
        save_to_db_checkbox = st.checkbox(
            "Save to database (Tracker)",
            value=False,
            help="Check to permanently track this ticker with daily updates. Bucket tickers (Country/Sector/Custom) are always saved.",
            key="ta_save_to_db_checkbox"
        )
    
    with col3:
        analyze_button = st.button(
            "🔍 Analyze",
            type="primary",
            use_container_width=True
        )

    # --- Phase III (UI-only): Rolling window selector drives rolling heatmap length ---
    # Selector must render whenever ticker is present (not only during Analyze).
    if ticker:
        # Persistence policy (UI-level resolution for the overall dashboard run)
        is_bucket = is_bucket_ticker(ticker)
        resolved_save_to_db = is_bucket or save_to_db_checkbox

        # Decide whether we need to compute now (single compute gate)
        last_ticker = st.session_state.get("technical_analysis_ticker")
        last_days = int(st.session_state.get("technical_analysis_rolling_days", 10))

        need_compute = False

        # Auto-compute on first load or ticker change (matches your current behavior)
        if last_ticker is None or last_ticker != ticker:
            need_compute = True

        # Analyze click always recomputes
        if analyze_button:
            need_compute = True

        # If rolling_days changed for this ticker, recompute
        selected_days = int(st.session_state.get("rh_days_selector", last_days))
        if last_ticker == ticker and selected_days != last_days:
            need_compute = True
#        if last_ticker == ticker and int(rolling_days) != last_days:
#            need_compute = True

        if need_compute:
            # Keep current_ticker if other dashboards reference it
            st.session_state.current_ticker = ticker

            # Info message (unchanged)
            if is_bucket:
                st.info(f"ℹ️ {ticker} is a bucket ticker and will be automatically tracked with daily updates.")
            elif save_to_db_checkbox:
                st.info(f"ℹ️ {ticker} will be added to tracking list with daily updates.")
            else:
                st.info(f"ℹ️ {ticker} analysis is session-only. Check 'Save to database' to track permanently.")

            with st.spinner(f"Analyzing {ticker}..."):
                try:
                    technical_calculator = st.session_state.technical_calculator

                    analysis_data = technical_calculator.calculate_comprehensive_analysis(
                        ticker,
                        save_to_db=resolved_save_to_db,

                        rolling_days=int(selected_days),  #int(rolling_days),
                    )

                    if not analysis_data.get("error"):
                        st.session_state.technical_analysis_data = analysis_data
                        st.session_state.technical_analysis_ticker = ticker
                        st.session_state.technical_analysis_timestamp = datetime.now()
                        # Remember the days used to compute rolling_signals
                        st.session_state.technical_analysis_rolling_days = int(selected_days)    #st.session_state.technical_analysis_rolling_days = int(rolling_days)

                        st.session_state.technical_analysis_save_to_db = bool(resolved_save_to_db)

                        extremes_result = technical_calculator.calculate_52_week_analysis(ticker, save_to_db=resolved_save_to_db,)
                        if extremes_result.get("success"):
                            st.session_state.price_extremes_data = extremes_result["periods"]

                        st.success(f"✅ Analysis complete for {ticker}")
                    else:
                        st.error(f"❌ Error analyzing {ticker}: {analysis_data.get('message', 'Unknown error')}")
                        return

                except Exception as e:
                    st.error(f"❌ Error analyzing {ticker}: {str(e)}")
                    return
    
    # Display analysis if available
    if ('technical_analysis_data' in st.session_state and 
        'technical_analysis_ticker' in st.session_state and
        st.session_state.technical_analysis_ticker == ticker):
        
        data = st.session_state.technical_analysis_data
                    
        # Show timestamp
        if 'technical_analysis_timestamp' in st.session_state:
            timestamp = st.session_state.technical_analysis_timestamp
            st.caption(f"Analysis generated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.markdown("---")

        # ------------------------------------------------------------
        # Technical Analysis Dashboard section layout
        # ------------------------------------------------------------
        # Containers are declared in the desired visual order. Existing
        # section logic can execute later while rendering into these
        # containers, preserving dependencies such as current_price for
        # Pivot Points.
        technical_indicators_container = st.container()
        rolling_heatmap_container = st.container()
        week52_container = st.container()
        moving_averages_container = st.container()
        pivot_points_container = st.container()
        
        # PLACEHOLDER: Display technical analysis components
        # These will be implemented in subsequent steps
        
        # Moving Averages Table
        with moving_averages_container:
            st.markdown("---")
            st.subheader("📈 Moving Averages Analysis")
            if 'moving_averages' in data:
                display_moving_averages_table(data['moving_averages'])
        
        # Technical Indicators Table
        with technical_indicators_container:
            st.subheader("📊 Technical Indicators")
            if 'technical_indicators' in data:
                display_technical_indicators_cards(data['technical_indicators'])
            else:
                st.warning("Technical indicators data not available")
        
        # 52-Week High Analysis
        with week52_container:
            st.subheader("📊 52-Week High Analysis")
            
            # Reuse the Moving Average price bundle so the displayed price,
            # effective date/time, and 52-week comparison calculations share
            # the same provenance.
            moving_average_data = data.get(
                'moving_averages'
            ) or {}

            if (
                not moving_average_data.get('error')
                and moving_average_data.get('current_price')
                is not None
            ):
                current_price = float(
                    moving_average_data['current_price']
                )
                effective_date_raw = (
                    moving_average_data.get(
                        'price_effective_date'
                    )
                    or moving_average_data.get(
                        'calculation_date'
                    )
                )
                effective_timestamp_raw = (
                    moving_average_data.get(
                        'price_effective_timestamp'
                    )
                )
            else:
                # Compatibility fallback: retain the existing top-level
                # price, but use its calculation date only. Never label
                # this fallback with the current application time.
                current_price = float(
                    data.get('current_price') or 0
                )
                effective_date_raw = data.get(
                    'calculation_date'
                )
                effective_timestamp_raw = None

            effective_date = pd.to_datetime(
                effective_date_raw,
                errors='coerce',
            )
            effective_timestamp = pd.to_datetime(
                effective_timestamp_raw,
                errors='coerce',
            )

            if pd.notna(effective_timestamp):
                if effective_timestamp.tzinfo is None:
                    effective_timestamp = (
                        effective_timestamp.tz_localize(
                            'America/New_York'
                        )
                    )
                else:
                    effective_timestamp = (
                        effective_timestamp.tz_convert(
                            'America/New_York'
                        )
                    )

            today = pd.Timestamp.now(
                tz='America/New_York'
            ).date()

            if pd.notna(effective_date):
                date_text = (
                    f"{effective_date.month}/"
                    f"{effective_date.day}/"
                    f"{effective_date.strftime('%y')}"
                )
            else:
                date_text = 'date unavailable'

            if (
                pd.notna(effective_timestamp)
                and effective_timestamp.date() == today
            ):
                hour_12 = (
                    effective_timestamp.hour % 12
                    or 12
                )
                meridiem = (
                    'A'
                    if effective_timestamp.hour < 12
                    else 'P'
                )
                time_text = (
                    f"{hour_12}:"
                    f"{effective_timestamp.minute:02d}"
                    f"{meridiem}"
                )

                price_label = (
                    f"Latest Price: ${current_price:.2f} "
                    f"({date_text} @ {time_text})"
                )
            else:
                price_label = (
                    f"Latest Price: ${current_price:.2f} "
                    f"({date_text})"
                )

            st.markdown(f"**{price_label}**")
            st.markdown("---")
            
            # Display 52-week analysis table if data available
            if 'price_extremes_data' in st.session_state and st.session_state.price_extremes_data:
                periods_data = st.session_state.price_extremes_data
                
                # Create display table with restructured columns
                table_rows = []
                period_order = ['52w', '52w_close', '6m', '3m', '1m', 'ytd']
                period_labels = {
                    '52w': '52W',
                    '52w_close': '52W (Close)',
                    '6m': '6M',
                    '3m': '3M',
                    '1m': '1M',
                    'ytd': 'YTD'
                }
                
                for period in period_order:
                    if period in periods_data:
                        p_data = periods_data[period]
                        
                        # Calculate current vs levels
                        vs_high = ((current_price - p_data['high_price']) / p_data['high_price']) * 100
                        vs_5pct = ((current_price - p_data['level_minus_5pct']) / p_data['level_minus_5pct']) * 100
                        vs_10pct = ((current_price - p_data['level_minus_10pct']) / p_data['level_minus_10pct']) * 100
                        vs_15pct = ((current_price - p_data['level_minus_15pct']) / p_data['level_minus_15pct']) * 100
                        vs_20pct = ((current_price - p_data['level_minus_20pct']) / p_data['level_minus_20pct']) * 100
                        vs_33pct = ((current_price - p_data['level_minus_33pct']) / p_data['level_minus_33pct']) * 100
                        vs_low = ((current_price - p_data['low_price']) / p_data['low_price']) * 100
                        
                        row = {
                            'Period': period_labels[period],
                            'High': f"${p_data['high_price']:.2f}",
                            '% Chg (High)': f"{vs_high:+.1f}%",
                            '-5%': f"${p_data['level_minus_5pct']:.2f}",
                            '% Chg (-5%)': f"{vs_5pct:+.1f}%",
                            '-10%': f"${p_data['level_minus_10pct']:.2f}",
                            '% Chg (-10%)': f"{vs_10pct:+.1f}%",
                            '-15%': f"${p_data['level_minus_15pct']:.2f}",
                            '% Chg (-15%)': f"{vs_15pct:+.1f}%",
                            '-20%': f"${p_data['level_minus_20pct']:.2f}",
                            '% Chg (-20%)': f"{vs_20pct:+.1f}%",
                            '-33%': f"${p_data['level_minus_33pct']:.2f}",
                            '% Chg (-33%)': f"{vs_33pct:+.1f}%",
                            'Low': f"${p_data['low_price']:.2f}",
                            '% Chg (Low)': f"{vs_low:+.1f}%"
                        }
                        table_rows.append(row)
                
                if table_rows:
                    df = pd.DataFrame(table_rows)
                    # TODO: Add styling for negative percentages (red color)
                    st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Custom input section BELOW table
            st.markdown("---")
            st.markdown("**Update 52W High** (optional)")
            
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                custom_52w_high = st.number_input(
                    "Custom 52W high:",
                    min_value=0.01,
                    value=None,
                    step=None,  # Removes +/- buttons
                    format="%.2f",
                    placeholder="e.g., 195.30",
                    help="Enter intraday high exceeding 52W closing high",
                    key="custom_52w_high_input"
                )
            
            with col2:
                custom_date = st.date_input(
                    "Date of high:",
                    value=None,
                    help="Date when the custom high occurred",
                    key="custom_52w_date_input"
                )
            
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)  # Spacer for alignment
                if st.button("🔄 Update", key="update_52w", use_container_width=True):
                    if custom_52w_high:
                        with st.spinner("Updating 52-week analysis..."):
                            extremes_result = st.session_state.technical_calculator.calculate_52_week_analysis(
                                ticker,
                                user_52w_high=custom_52w_high,
                                save_to_db=resolved_save_to_db,
                            )
                            
                            if extremes_result.get('error'):
                                st.error(f"❌ {extremes_result['message']}")
                            elif extremes_result.get('success'):
                                st.session_state.price_extremes_data = extremes_result['periods']
                                st.success("✅ 52-week analysis updated")
                                st.rerun()
                    else:
                        st.warning("⚠️ Enter a custom high value first")
        
        # Pivot Points Analysis
        with pivot_points_container:
            st.markdown("---")
            st.subheader("📍 Pivot Points Analysis")
            
            # Determine save_to_db setting (same logic as main analysis)
            is_bucket = is_bucket_ticker(ticker)
            should_save_to_db = is_bucket or st.session_state.get('ta_save_to_db_checkbox', False)
            
            # Calculate pivot points if not already cached in session
            if 'pivot_points_data' not in st.session_state or st.session_state.get('pivot_points_ticker') != ticker:
                with st.spinner("Calculating pivot points..."):
                    try:
                        pivot_data = st.session_state.technical_calculator.calculate_pivot_points(
                            ticker=ticker,
                            target_date=None,  # Auto-detect previous trading day
                            save_to_db=resolved_save_to_db   #should_save_to_db
                        )
                        st.session_state.pivot_points_data = pivot_data
                        st.session_state.pivot_points_ticker = ticker
                    except Exception as e:
                        st.error(f"Error calculating pivot points: {str(e)}")
                        st.session_state.pivot_points_data = {'error': True, 'message': str(e)}
            
            # Display pivot points
            if 'pivot_points_data' in st.session_state:
                display_pivot_points(
                    ticker=ticker,
                    pivot_data=st.session_state.pivot_points_data,
                    current_price=current_price
                )
            else:
                st.info("Pivot points data not available")

        # Rolling Heatmap
        with rolling_heatmap_container:
            st.subheader("🔥 Rolling Signal Heatmap")
            if "rolling_signals" in data:
                from src.ui.rolling_heatmap_adapter import (
                    INDICATOR_DEFS,
                    build_plotly_heatmap_inputs,
                    make_rolling_heatmap_figure,
                    get_indicator_doc_slug,
                )

                technical_calculator = st.session_state.technical_calculator

                # --- Phase III (UI-only): Rolling heatmap controls (local to heatmap section) ---
                # D1: Only recompute rolling_signals when rolling params change (not on every rerun).
                cA, cB, cC, cD = st.columns([1.2, 1.2, 1.0, 1.4])

                with cA:
                    rolling_days = st.selectbox(
                        "Rolling window (trading days)",
                        options=[10, 20, 30, 60],
                        index=0,
                        key="rh_days_selector",
                        help="Controls how many trading days the rolling heatmap displays.",
                    )

                with cB:
                    anchor_mode = st.radio(
                        "Anchor mode",
                        options=["asof", "start"],
                        index=0,
                        horizontal=True,
                        key="rh_anchor_mode",
                        help="As-of: window ends on anchor date. Start: window begins on anchor date.",
                    )

                with cC:
                    cache_enabled = st.toggle(
                        "Save in-session",
                        value=False,
                        key="rh_cache_enabled",
                        help="Caches rolling inputs per ticker for faster browsing within this session only. "
                            "'On': deep-dive into multiple dates/windows. 'Off': sampling many tickers once each.",
                    )

                with cD:
                    use_anchor_date = st.checkbox(
                        "Use anchor date",
                        value=False,
                        key="rh_use_anchor_date",
                        help="If unchecked, the builder uses the latest available trading day (as-of) "
                            "or the earliest available trading day (start), depending on Anchor mode.",
                    )

                anchor_date = None
                if use_anchor_date:
                    anchor_label = "As-of date" if anchor_mode == "asof" else "Start date"
                    anchor_date = st.date_input(
                        anchor_label,
                        key="rh_anchor_date",
                        help="Pick the anchor date used to resolve the rolling window.",
                    )

                # Compute-gating: only rebuild rolling_signals when parameters change.
                # This prevents unnecessary recompute on row-order clicks, expanders, etc.
                rolling_params = (
                    str(ticker).upper().strip(),
                    int(rolling_days),
                    str(anchor_mode),
                    anchor_date,               # datetime.date or None
                    bool(cache_enabled),
                )

                if "rh_last_params" not in st.session_state:
                    st.session_state.rh_last_params = None
                if "rh_last_signals" not in st.session_state:
                    st.session_state.rh_last_signals = None

                need_rebuild = (st.session_state.rh_last_params != rolling_params) or (st.session_state.rh_last_signals is None)

                if need_rebuild:
                    with st.spinner("Building rolling heatmap…"):
                        rolling_signals = technical_calculator.build_rolling_heatmap_signals(
                            ticker=ticker,
                            window_days=int(rolling_days),
                            anchor_mode=str(anchor_mode),
                            anchor_date=anchor_date,          # date | None
                            cache_enabled=bool(cache_enabled),
                            base_buffer_days=None,            # defer tuning; safe default inside builder
                        )
                    st.session_state.rh_last_params = rolling_params
                    st.session_state.rh_last_signals = rolling_signals
                else:
                    rolling_signals = st.session_state.rh_last_signals

                # Inject/override only the rolling_signals used by the heatmap renderer
                data = dict(data)  # shallow copy so we don't mutate session_state object unexpectedly
                data["rolling_signals"] = rolling_signals

                available_keys = list(INDICATOR_DEFS.keys())

                # v1 defaults (edit this list freely; any missing keys are ignored safely)
                DEFAULT_KEYS = [
                    "RSI_14",
    #                "RSI_10",
                    "RSI_21", "RSI_30",
                    "SMA_50",   #"SMA_10",  "SMA_20",
                    "SMA_100",
                    "SMA_200",
                    #"EMA_5",
                    #"EMA_10",
                    "EMA_13",
                    "EMA_20", 
                    "EMA_50",
                    #"EMA_100",
                    #"EMA_200",
                    #"HMA_9",
    #                "HMA_21",
                    #"HMA_50",
                    "WILLR_5",
                    "WILLR_14",
                    "WILLR_20",
                    "CMF_10",  
                    "CMF_21",
                    "CMF_50",  
                    "CMF_30", 
                    #"UO_5_10_15",
                    "UO_7_14_28",
                    #"UO_10_20_40",
                    #"CCI_10"
                    "CCI_14",
                    #"CCI_20"
                    "MFI_10",
                    "MFI_14",
                    "MFI_30",
                    #"ROC_9",
                    "ROC_12",
                    "ROC_14",
                    "ROC_20",
                    "ROC_50",
                    "BB_PCT_B_ST",
                    "BB_PCT_B",
                    "BB_PCT_B_LT",
                    "BB_BW_ST",
                    "BB_BW",
                    "BB_BW_LT",
                    #"ADX_9",
                    "ADX_14",
                    #"ADX_20",
                    #"OBV",
                    "HMA_9",
                    "HMA_16",
                    "HMA_21",  
                    "HMA_50",
                    "HMA_55",
                    "VWMA_10", "VWMA_20", "VWMA_50",  
                    "MACD_12_26_9", "MACD_8_17_5", "MACD_20_50_10", 
                    "STOCH_14_3_3", "STOCH_5_3_3", "STOCH_21_5_5",
                    "BullBearPower_10", "BullBearPower_13", "BullBearPower_21",
                    # "MACD_5_34_1"
                    # If you want to include the UI-mock expansion, uncomment these:
                    # "EMA_20", "EMA_50", "HMA_21", "UO_7_14_28", "CCI_14", "OBV",
                ]
                default_keys = [k for k in DEFAULT_KEYS if k in available_keys]

                # -------------------------------
                # Phase III Rolling Heatmap: Selection Mode integration
                # -------------------------------
                # Contract path:
                # Selection Mode -> mode-specific controls -> resolved base row-key set
                # -> manual display/remove override -> row-order override -> heatmap render.
                #
                # Important Streamlit rule:
                # Do not assign to st.session_state[widget_key] after a widget with that key
                # has been instantiated. Initialize/validate state before rendering widgets,
                # then read widget return values.

                mode_options = get_selection_modes()
                if not mode_options:
                    mode_options = ["Custom", "Category", "Preset", "Tag"]

                current_mode = st.session_state.get("rh_selection_mode", "Custom")
                if current_mode not in mode_options:
                    current_mode = "Custom"

                selection_mode = st.selectbox(
                    "Selection Mode",
                    options=mode_options,
                    index=mode_options.index(current_mode),
                    key="rh_selection_mode",
                    help="Choose the base row set. Manual display/remove and row-order still apply afterward.",
                )

                resolved_base_keys = []

                if selection_mode == "Custom":
                    # Custom is an editable saved/session row set. Restore-default must
                    # resolve from the catalog-owned RH_CUSTOM_DEFAULT.
                    cc1, cc2 = st.columns([0.75, 0.25])
                    with cc1:
                        st.caption(
                            "Custom mode uses your saved/default row set. "
                            "Manual add/remove below updates the session Custom set."
                        )
                    with cc2:
                        if st.button(
                            "Restore Default Custom",
                            key="rh_restore_default_custom",
                            use_container_width=True,
                        ):
                            st.session_state.rh_custom_rows = list(RH_CUSTOM_DEFAULT)
                            st.session_state.pop("rh_custom_selected_keys", None)
                            st.session_state.pop("rh_row_order", None)
                            st.rerun()

                    resolved_base_keys = resolve_row_selection(
                        selection_mode="Custom",
                        custom_rows=st.session_state.get("rh_custom_rows", list(RH_CUSTOM_DEFAULT)),
                    )

                    current_multiselect_key = "rh_custom_selected_keys"

                elif selection_mode == "Preset":
                    preset_options = get_preset_names()

                    if not preset_options:
                        st.warning("No rolling heatmap presets are available.")
                        selected_preset = None
                        resolved_base_keys = []
                        current_multiselect_key = "rh_preset_selected_keys__none"
                    else:
                        stored_preset = st.session_state.get("rh_selected_preset")
                        if stored_preset not in preset_options:
                            # Safe: this occurs before the widget is instantiated.
                            st.session_state.rh_selected_preset = preset_options[0]
                            stored_preset = preset_options[0]

                        selected_preset = st.selectbox(
                            "Choose a preset",
                            options=preset_options,
                            index=preset_options.index(stored_preset),
                            key="rh_selected_preset",
                            help="Overview presets are curated; thematic presets are generated from the selection catalog.",
                        )

                        resolved_base_keys = resolve_row_selection(
                            selection_mode="Preset",
                            preset_name=selected_preset,
                        )

                        preset_key_part = str(selected_preset).replace(" ", "_").replace("/", "_")
                        current_multiselect_key = f"rh_preset_selected_keys__{preset_key_part}"

                elif selection_mode == "Category":
                    category_options = get_category_names()

                    if not category_options:
                        st.warning("No row categories are available.")
                        selected_category = None
                        selected_scope = "All"
                        selected_window = "All"
                        selected_family = "All"
                        resolved_base_keys = []
                        current_multiselect_key = "rh_category_selected_keys__none"
                    else:
                        stored_category = st.session_state.get("rh_selected_category")
                        if stored_category not in category_options:
                            # Safe: this occurs before the widget is instantiated.
                            st.session_state.rh_selected_category = category_options[0]
                            stored_category = category_options[0]

                        c1, c2, c3, c4 = st.columns(4)

                        with c1:
                            selected_category = st.selectbox(
                                "Category",
                                options=category_options,
                                index=category_options.index(stored_category),
                                key="rh_selected_category",
                            )

                        # Defensive local normalization for Streamlit rerun edges:
                        # when switching categories, the widget/session-state
                        # handoff can briefly yield a non-resolvable category
                        # value. The resolver requires a concrete category, so
                        # fall back locally without mutating the widget key after
                        # instantiation.
                        if selected_category not in category_options:
                            selected_category = stored_category

                        if selected_category not in category_options:
                            selected_category = category_options[0]

                        scope_values = get_scope_names(selected_category)
                        scope_options = ["All"] + [s for s in scope_values if s != "All"]
                        stored_scope = st.session_state.get("rh_selected_scope", "All")
                        if stored_scope not in scope_options:
                            st.session_state.rh_selected_scope = "All"
                            stored_scope = "All"

                        with c2:
                            selected_scope = st.selectbox(
                                "Scope",
                                options=scope_options,
                                index=scope_options.index(stored_scope),
                                key="rh_selected_scope",
                                help="Optional narrowing filter.",
                            )

                        window_values = get_window_names(selected_category)
                        window_options = ["All"] + [w for w in window_values if w != "All"]
                        stored_window = st.session_state.get("rh_selected_window", "All")
                        if stored_window not in window_options:
                            st.session_state.rh_selected_window = "All"
                            stored_window = "All"

                        with c3:
                            selected_window = st.selectbox(
                                "Window",
                                options=window_options,
                                index=window_options.index(stored_window),
                                key="rh_selected_window",
                                help="Optional ST / MT / LT filter. 'All' means no Window filter.",
                            )

                        family_values = get_family_names(selected_category)
                        family_options = ["All"] + [f for f in family_values if f != "All"]
                        stored_family = st.session_state.get("rh_selected_family", "All")
                        if stored_family not in family_options:
                            st.session_state.rh_selected_family = "All"
                            stored_family = "All"

                        with c4:
                            selected_family = st.selectbox(
                                "Family",
                                options=family_options,
                                index=family_options.index(stored_family),
                                key="rh_selected_family",
                                help="Optional family filter, including grouped families such as MVA and Oscillators.",
                            )

                        resolved_base_keys = resolve_row_selection(
                            selection_mode="Category",
                            category=selected_category,
                            scope=selected_scope,
                            window=selected_window,
                            family=selected_family,
                        )

                        category_key_part = str(selected_category).replace(" ", "_").replace("/", "_")
                        scope_key_part = str(selected_scope).replace(" ", "_").replace("/", "_")
                        window_key_part = str(selected_window).replace(" ", "_").replace("/", "_")
                        family_key_part = str(selected_family).replace(" ", "_").replace("/", "_")
                        current_multiselect_key = (
                            "rh_category_selected_keys__"
                            f"{category_key_part}__{scope_key_part}__{window_key_part}__{family_key_part}"
                        )

                elif selection_mode == "Tag":
                    tag_options = get_tag_names()

                    if not tag_options:
                        st.warning("No rolling heatmap tags are available.")
                        selected_tag = None
                        resolved_base_keys = []
                        current_multiselect_key = "rh_tag_selected_keys__none"
                    else:
                        stored_tag = st.session_state.get("rh_selected_tag")
                        if stored_tag not in tag_options:
                            st.session_state.rh_selected_tag = tag_options[0]
                            stored_tag = tag_options[0]

                        selected_tag = st.selectbox(
                            "Tag",
                            options=tag_options,
                            index=tag_options.index(stored_tag),
                            key="rh_selected_tag",
                            help=(
                                "Tags are cross-category secondary descriptors. "
                                "Selecting a tag returns all catalog rows carrying it."
                            ),
                        )

                        resolved_base_keys = resolve_row_selection(
                            selection_mode="Tag",
                            tag=selected_tag,
                        )

                        tag_key_part = (
                            str(selected_tag)
                            .replace(" ", "_")
                            .replace("/", "_")
                            .replace(":", "_")
                        )
                        current_multiselect_key = (
                            f"rh_tag_selected_keys__{tag_key_part}"
                        )

                else:
                    st.warning(f"Unknown Selection Mode: {selection_mode}")
                    resolved_base_keys = []
                    current_multiselect_key = "rh_unknown_selected_keys"

                # Compatibility filtering only: grouping truth remains in the catalog /
                # selection modules; INDICATOR_DEFS is used here only as the current
                # display/render-compatible row universe.
                resolved_base_keys = [k for k in resolved_base_keys if k in available_keys]
                st.session_state.rh_last_resolved_base_keys = list(resolved_base_keys)

                # Initialize the active multiselect state before creating the widget.
                # Because current_multiselect_key changes by mode/preset/category filters,
                # Streamlit treats each resolved context as a distinct widget and loads
                # the correct base row set.
                if current_multiselect_key not in st.session_state:
                    st.session_state[current_multiselect_key] = list(resolved_base_keys)
                else:
                    st.session_state[current_multiselect_key] = [
                        k for k in st.session_state[current_multiselect_key] if k in available_keys
                    ]

                if not resolved_base_keys:
                    st.warning(
                        describe_empty_selection(
                            selection_mode=selection_mode,
                            category=st.session_state.get("rh_selected_category"),
                            scope=st.session_state.get("rh_selected_scope"),
                            window=st.session_state.get("rh_selected_window"),
                            family=st.session_state.get("rh_selected_family"),
                            tag=st.session_state.get("rh_selected_tag"),
                            preset_name=st.session_state.get("rh_selected_preset"),
                        )
                    )

                # ------------------------------------------------------------
                # Visual layout placeholders
                # ------------------------------------------------------------
                # The manual controls must execute before heatmap rendering so
                # ordered_selected_keys is current. These containers let the heatmap
                # appear above the manual controls while preserving the execution order.
                heatmap_container = st.empty()
                manual_controls_container = st.container()

                with manual_controls_container:
                    selected_keys = st.multiselect(
                        "Indicators to display/remove",
                        options=available_keys,
                        key=current_multiselect_key,
                        help="Manual downstream override. Starts from the selected row set, then you can add/remove visible rows.",
                    )

                    if selection_mode == "Custom":
                        st.session_state.rh_custom_rows = list(selected_keys)

                    # ---- Phase III (UI-only): Session-only row order persistence (Option 2) ----
                    # Goal: order persists across ticker changes/reruns in the same session, but resets on new session.

                    # Initialize row order once per session from the current post-manual
                    # display/remove selection.
                    if "rh_row_order" not in st.session_state:
                        st.session_state.rh_row_order = list(selected_keys)

                    # Reconcile row order with current selection:
                    #  - remove deselected keys
                    #  - append newly selected keys at the end
                    current_order = [k for k in st.session_state.rh_row_order if k in selected_keys]
                    newly_selected = [k for k in selected_keys if k not in current_order]
                    st.session_state.rh_row_order = current_order + newly_selected
                    st.session_state.rh_row_order = list(dict.fromkeys(st.session_state.rh_row_order))

                    # Row reordering UI (mouse clicks; no external components)
                    with st.expander("Change Indicator Order", expanded=False):
                        st.caption("Use ↑ / ↓ to reorder rows for this session. Order resets on a new session.")

                        # Use INDICATOR_DEFS for friendly labels in the reorder panel
                        defs = INDICATOR_DEFS

                        # Sync the row order between heatmap & ordering drop-down
                        order_view = list(st.session_state.rh_row_order)
                        for idx, key in enumerate(order_view):
                            label = defs.get(key, {}).get("display_name", key)

                            c1, c2, c3 = st.columns([0.08, 0.08, 0.84])

                            up_disabled = idx == 0
                            down_disabled = idx == (len(st.session_state.rh_row_order) - 1)

                            if c1.button("↑", key=f"rh_up_{idx}_{key}", disabled=up_disabled):
                                order = list(st.session_state.rh_row_order)
                                order[idx - 1], order[idx] = order[idx], order[idx - 1]
                                st.session_state.rh_row_order = order
                                st.rerun()

                            if c2.button("↓", key=f"rh_down_{idx}_{key}", disabled=down_disabled):
                                order = list(st.session_state.rh_row_order)
                                order[idx], order[idx + 1] = order[idx + 1], order[idx]
                                st.session_state.rh_row_order = order
                                st.rerun()

                            c3.write(label)

                    with st.expander("Selection Debug", expanded=False):
                        st.write(f"Selection Mode: {selection_mode}")
                        st.write(f"Resolved base keys count: {len(resolved_base_keys)}")
                        st.write(f"Multiselect session key: {current_multiselect_key}")
                        st.write(f"Selected keys count: {len(selected_keys)}")
                        st.write(f"Resolved base keys: {resolved_base_keys}")

                # Ordered keys for rendering
                ordered_selected_keys = st.session_state.rh_row_order

                rolling_payload = _extract_rolling_signals_from_data(data)

                # ----------------------------------------
                # Hover-only OHLCV / indicator context
                # ----------------------------------------
                hover_ohlcv_df = None
                try:
                    hover_ohlcv_df = technical_calculator.calculate_optionc_indicators(
                        ticker=ticker,
                        save_to_db=False,
                        ohlcv_request={
                            "mode": "rolling_heatmap_scenario_b",
                            "window_days": int(rolling_days),
                            "anchor_mode": str(anchor_mode),
                            "anchor_date": anchor_date,
                            "historical_buffer_days": 435,
                        },
                    )
                except Exception:
                    hover_ohlcv_df = None

                hm = build_plotly_heatmap_inputs(
                    rolling_payload=rolling_payload,
                    indicator_keys=ordered_selected_keys,
                    ohlcv_df=hover_ohlcv_df,
                )
                # populate rolling heatmap & add title, if desired
                fig = make_rolling_heatmap_figure(hm, title="")
                
                with heatmap_container.container():
                    st.plotly_chart(fig, use_container_width=True)

                # ----------------------------------------
                # Educational expander (row-stable only)
                # ----------------------------------------
                with st.expander("📘 Indicator Definitions", expanded=False):
                    for key in ordered_selected_keys:
                        info = INDICATOR_DEFS.get(key, {})
                        display_name = info.get("display_name", key)
                        definition = info.get("definition", "")
                        how_to_read = info.get("how_to_read", "")

                        st.markdown(f"**{display_name}**")
                        if definition:
                            st.write(
                                "Definition: "
                                f"{_strip_indicator_definition_markup(definition)}"
                            )
                        if how_to_read:
                            st.write(
                                "How to Read: "
                                f"{_strip_indicator_definition_markup(how_to_read)}"
                            )

                        # Optional family-level long-form overview
                        doc_slug = get_indicator_doc_slug(key)
                        markdown_text = load_indicator_markdown(doc_slug)

                        if markdown_text:
                            with st.expander(f"Learn more about {doc_slug}", expanded=False):
                                st.markdown(
                                    markdown_text,
                                    unsafe_allow_html=True,
                                )

                        st.markdown("---")

                # Optional debug view (safe to keep, collapsed)
                with st.expander("Raw Rolling Signals Data (debug)", expanded=False):
                    st.json(data.get("rolling_signals", {}))                
            else:
                st.info("No rolling signals available yet for this ticker.")

    elif ticker:
        st.info(f"👆 Click 'Analyze Stock' to get technical analysis for {ticker}")
    else:
        st.info("👆 Enter a stock ticker symbol above to get started")             

def show_performance_heatmaps():
    """Original Performance Heatmaps Dashboard (Existing Functionality)"""
    # Create header
    create_header()
    
    # Create sidebar controls
    controls = create_sidebar_controls()
        
    # Check if we need to fetch new data - handle both price and volume modes.
    #
    # Cache identity is based on the exact data request rather than the number
    # of successful rows returned. Individual ticker errors therefore remain a
    # valid cached result for the request that produced them.
    if controls['analysis_mode'] == 'volume':
        current_request_signature = (
            controls['analysis_mode'],
            controls['period'],
            controls['volume_view_mode'],
            tuple(controls['tickers']),
        )
    else:
        current_request_signature = (
            controls['analysis_mode'],
            controls['period'],
            tuple(controls['tickers']),
        )

    if controls['analysis_mode'] == 'price':
        current_data = st.session_state.performance_data
        last_update = st.session_state.last_update
        cached_request_signature = (
            st.session_state.performance_request_signature
        )
    else:  # volume mode
        current_data = st.session_state.volume_data
        last_update = st.session_state.volume_last_update
        cached_request_signature = (
            st.session_state.volume_request_signature
        )

    request_changed = (
        cached_request_signature
        != current_request_signature
    )

    should_fetch = (
        controls['refresh']
        or current_data is None
        or current_data == []
        or last_update is None
        or request_changed
    )

    if should_fetch:
        if controls['analysis_mode'] == 'price':
            # Fetch price performance data
            performance_data = fetch_performance_data(
                controls['tickers'],
                controls['period'],
                save_to_db=False,
            )

            # Store in session state.
            #
            # Record request identity whenever the fetch path returned a
            # non-empty result set. Individual ticker error rows remain part of
            # that completed request and must not force another fetch on the next
            # unrelated Streamlit rerun.
            st.session_state.performance_data = performance_data
            st.session_state.last_update = datetime.now()

            if performance_data:
                st.session_state.performance_request_signature = (
                    current_request_signature
                )
            else:
                st.session_state.performance_request_signature = None

            current_data = performance_data

        else:  # volume mode
            # Fetch volume performance data
            volume_data = fetch_volume_data(
                controls['tickers'],
                controls['period'],
                observation_mode=controls[
                    'volume_view_mode'
                ],
                save_to_db=False,
            )

            # Store in session state using the same request-identity contract as
            # Price performance.
            st.session_state.volume_data = volume_data
            st.session_state.volume_last_update = datetime.now()

            if volume_data:
                st.session_state.volume_request_signature = (
                    current_request_signature
                )
            else:
                st.session_state.volume_request_signature = None

            current_data = volume_data

        valid_update_items = [
            item
            for item in (current_data or [])
            if not item.get('error', False)
        ]

        if valid_update_items:
            st.success(
                f"✅ Data updated successfully at "
                f"{datetime.now().strftime('%H:%M:%S')}"
            )
    else:
        # Use cached data only when it belongs to the exact active request.
        if controls['analysis_mode'] == 'price':
            current_data = st.session_state.performance_data
        else:
            current_data = st.session_state.volume_data
    
    if current_data:
        # Create heatmap title based on analysis mode
        if controls['analysis_mode'] == 'price':
            title = f"{controls['group_name']} - {controls['period_name']} Performance"
        else:  # volume mode
            if controls['volume_view_mode'] == 'completed':
                volume_title_prefix = "Last Complete Volume"
            else:
                volume_title_prefix = "Current Volume"

            title = (
                f"{controls['group_name']} - "
                f"{volume_title_prefix} vs. "
                f"{controls['period_name']} Avg."
            )
        
        # Display summary statistics
        st.subheader("📊 Summary Statistics")
        display_summary_stats(
            current_data,
            ticker_names=controls[
                'ticker_names'
            ],
        )
        
        st.markdown("---")
        
        # Display heatmap
        st.subheader("🗺️ Performance Heatmap")

        tile_order_labels = {
            'original': 'Original',
            'performance_desc': 'Highest → Lowest',
        }

        selected_tile_order = st.radio(
            "Tile Order",
            options=list(tile_order_labels.keys()),
            format_func=lambda key: tile_order_labels[key],
            horizontal=True,
            key='performance_heatmap_tile_order',
        )

        # Add timestamp and baseline date info (only for price mode)
        if controls['analysis_mode'] == 'price':
            valid_items = [
                item
                for item in current_data
                if not item.get('error', False)
            ]

            reliable_timestamps = []
            reliable_dates = []

            for item in valid_items:
                metadata = (
                    item.get('current_price_metadata')
                    or {}
                )
                effective_timestamp = metadata.get(
                    'effective_timestamp'
                )
                effective_date = metadata.get(
                    'effective_date'
                )

                if effective_timestamp:
                    try:
                        reliable_timestamps.append(
                            pd.Timestamp(
                                effective_timestamp
                            )
                        )
                    except Exception:
                        pass

                if effective_date:
                    try:
                        reliable_dates.append(
                            pd.Timestamp(effective_date)
                        )
                    except Exception:
                        pass

            timestamp_caption = None

            if reliable_timestamps:
                oldest_timestamp = min(
                    reliable_timestamps
                )
                now_local = datetime.now()

                if (
                    is_us_trading_day(now_local)
                    and oldest_timestamp.date()
                    == now_local.date()
                ):
                    hour = (
                        oldest_timestamp
                        .strftime('%I')
                        .lstrip('0')
                        or '0'
                    )
                    timestamp_caption = (
                        f"{oldest_timestamp.month}/"
                        f"{oldest_timestamp.day}/"
                        f"{str(oldest_timestamp.year)[-2:]}"
                        f" @ {hour}:"
                        f"{oldest_timestamp.strftime('%M')}"
                        f"{oldest_timestamp.strftime('%p')[0]}"
                    )
                else:
                    timestamp_caption = (
                        f"{oldest_timestamp.month}/"
                        f"{oldest_timestamp.day}/"
                        f"{str(oldest_timestamp.year)[-2:]}"
                    )

            elif reliable_dates:
                oldest_date = min(reliable_dates)
                timestamp_caption = (
                    f"{oldest_date.month}/"
                    f"{oldest_date.day}/"
                    f"{str(oldest_date.year)[-2:]}"
                )

            if timestamp_caption:
                st.caption(
                    f"Timestamp: {timestamp_caption}"
                )

            baseline_date = None

            if valid_items:
                period = valid_items[0].get(
                    'period',
                    '1d',
                )

                from src.calculations.performance import (
                    get_baseline_date_for_display,
                )

                baseline_date_str = (
                    get_baseline_date_for_display(
                        period
                    )
                )
                baseline_date = datetime.strptime(
                    baseline_date_str,
                    '%Y-%m-%d',
                ).strftime('%m/%d/%y')

            if baseline_date:
                st.caption(
                    f"Baseline Date: {baseline_date}"
                )

        else:
            valid_volume_items = [
                item
                for item in current_data
                if not item.get('error', False)
            ]

            volume_timestamps = []
            volume_dates = []

            for item in valid_volume_items:
                volume_context = (
                    item.get('volume_context')
                    or {}
                )

                effective_timestamp = (
                    volume_context.get(
                        'effective_timestamp'
                    )
                )
                effective_date = volume_context.get(
                    'effective_date'
                )

                if effective_timestamp:
                    try:
                        volume_timestamps.append(
                            pd.Timestamp(
                                effective_timestamp
                            )
                        )
                    except Exception:
                        pass

                if effective_date:
                    try:
                        volume_dates.append(
                            pd.Timestamp(effective_date)
                        )
                    except Exception:
                        pass

            volume_caption = None

            if volume_timestamps:
                oldest_timestamp = min(
                    volume_timestamps
                )

                hour = (
                    oldest_timestamp
                    .strftime('%I')
                    .lstrip('0')
                    or '0'
                )

                volume_caption = (
                    f"{oldest_timestamp.month}/"
                    f"{oldest_timestamp.day}/"
                    f"{str(oldest_timestamp.year)[-2:]}"
                    f" @ {hour}:"
                    f"{oldest_timestamp.strftime('%M')}"
                    f"{oldest_timestamp.strftime('%p')[0]}"
                )

            elif volume_dates:
                oldest_date = min(volume_dates)

                volume_caption = (
                    f"{oldest_date.month}/"
                    f"{oldest_date.day}/"
                    f"{str(oldest_date.year)[-2:]}"
                )

            if volume_caption:
                label = (
                    "As of"
                    if controls['volume_view_mode']
                    == 'completed'
                    else "Timestamp"
                )

                st.caption(
                    f"{label}: {volume_caption}"
                )
        
        display_heatmap(
            current_data,
            title,
            controls['group'],
            tile_order=selected_tile_order,
            ticker_names=controls[
                'ticker_names'
            ],
        )

        # Display data table
        with st.expander("📋 Detailed Data Table", expanded=False):
            display_data_table(current_data)
        
        # Show last update time based on analysis mode
        if controls['analysis_mode'] == 'price' and st.session_state.last_update:
            st.caption(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        elif controls['analysis_mode'] == 'volume' and st.session_state.volume_last_update:
            st.caption(f"Last updated: {st.session_state.volume_last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    
    else:
        st.info("👆 Select your preferences in the sidebar and click 'Refresh Data' to get started!")

    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit and Plotly | "
        "Data provided by Yahoo Finance via yfinance"
    )

def show_stock_comparison_dashboard():
    """
    Render the Stock Comparison Dashboard v1 route shell.

    WS2 scope: SCD-specific ticker controls only.
    Indicator selection, rolling payload execution, matrix assembly, heatmap,
    and detail table rendering are added in later workstreams.
    """
    st.title("📋 Stock Comparison Dashboard")
    st.caption("Phase III Extension — Stock Comparison Dashboard v1")

    st.markdown(
        """
        This dashboard compares selected technical indicator rows across
        selected tickers using the existing Rolling Heatmap value / signal / score path.
        """
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Analysis Mode")

    analysis_mode_options = ["Single Indicator", "Multiple Indicators"]
    current_analysis_mode = st.session_state.get(
        "scd_analysis_mode",
        "Single Indicator",
    )
    if current_analysis_mode not in analysis_mode_options:
        current_analysis_mode = "Single Indicator"

    analysis_mode = st.sidebar.radio(
        "Analysis Mode",
        options=analysis_mode_options,
        index=analysis_mode_options.index(current_analysis_mode),
        key="scd_analysis_mode_widget",
        help=(            
            "Single Indicator will show one selected indicator across tickers and dates."
            "Multiple Indicators shows the current cross-sectional comparison matrix. "
        ),
    )

    # Keep canonical SCD analysis-mode state separate from widget state.
    # This mirrors the existing SCD ticker-source pattern and prevents stale
    # routing behavior when switching between analysis modes.
    st.session_state.scd_analysis_mode = analysis_mode

    if st.session_state.get(
        _DATA_MANAGEMENT_SCD_STALE_KEY,
        False,
    ):
        rebuild_action = (
            "Rebuild Time-Series Matrix"
            if analysis_mode == "Single Indicator"
            else "Rebuild Comparison Matrix"
        )

        st.warning(
            "The underlying authoritative OHLCV data has changed since "
            "the previous Stock Comparison results were built. "
            f"Click **{rebuild_action}** to rebuild this view from the "
            "updated data."
        )

    selected_tickers = _render_scd_ticker_controls()

    if selected_tickers:
        st.caption(
            f"Selected tickers: {len(selected_tickers)} — "
            + ", ".join(selected_tickers)
        )
    else:
        st.info("Choose at least one ticker in the sidebar.")

    if analysis_mode == "Single Indicator":
        selected_single_indicator = _render_scd_single_indicator_controls()
        single_indicator_date_request = _render_scd_single_indicator_date_controls()

        st.subheader("Time-Series Matrix")
        st.caption(
            "The default Single Indicator matrix builds automatically on first load. "
            "Use Rebuild Time-Series Matrix when you want to rebuild the current "
            "date × ticker view."
        )

        force_refresh_single = st.checkbox(
            "Recalculate selected tickers for this build",
            value=False,
            key="scd_single_force_refresh",
            help=(
                "Bypass the SCD session cache once for this Single Indicator build. "
                "This does not change DB persistence behavior."
            ),
        )

        build_single_clicked = st.button(
            "Rebuild Time-Series Matrix",
            key="scd_single_build_matrix",
            type="primary",
            disabled=not selected_tickers or not selected_single_indicator,
        )

        should_auto_build_single = (
            selected_tickers
            and selected_single_indicator
            and st.session_state.get("scd_single_indicator_matrix") is None
            and not st.session_state.get(
                _DATA_MANAGEMENT_SCD_STALE_KEY,
                False,
            )
        )

        if build_single_clicked or should_auto_build_single:
            spinner_text = (
                "Building Single Indicator time-series matrix."
                if build_single_clicked
                else "Building default Single Indicator time-series matrix."
            )

            if build_single_clicked and force_refresh_single:
                _get_scd_cache_stats()["force_refreshes"] += 1

            with st.spinner(spinner_text):
                st.session_state.scd_single_indicator_matrix = (
                    _build_scd_single_indicator_time_series_matrix(
                        selected_tickers=selected_tickers,
                        selected_row_key=selected_single_indicator,
                        date_request=single_indicator_date_request,
                        force_refresh=force_refresh_single if build_single_clicked else False,
                    )
                )
                st.session_state.scd_single_indicator_matrix_last_run = datetime.now()

            if build_single_clicked:
                stale_rebuild_completed = bool(
                    st.session_state.get(
                        _DATA_MANAGEMENT_SCD_STALE_KEY,
                        False,
                    )
                )

                st.session_state.pop(
                    _DATA_MANAGEMENT_SCD_STALE_KEY,
                    None,
                )

                if stale_rebuild_completed:
                    st.rerun()

        single_matrix = st.session_state.get("scd_single_indicator_matrix")

        if single_matrix:
            st.success("Time-Series Matrix ready.")
            st.caption(
                f"Indicator: {single_matrix.get('row_key')} · "
                f"Window: {single_matrix.get('window_start_date')} → "
                f"{single_matrix.get('window_end_date')} · "
                f"Dates: {len(single_matrix.get('dates', []))} · "
                f"Tickers: {len(single_matrix.get('tickers', []))}"
            )

            live_date_key = _get_scd_current_live_date_key()
            live_date_in_matrix = (
                bool(live_date_key)
                and live_date_key in [str(date_key) for date_key in single_matrix.get("dates", [])]
            )

            col_refresh_selected, col_refresh_all = st.columns([0.5, 0.5])

            with col_refresh_selected:
                refresh_selected_today_clicked = st.button(
                    "Refresh this indicator only",
                    key="scd_single_refresh_selected_today_cells",
                    disabled=not live_date_in_matrix,
                    use_container_width=True,
                    help=(
                        "Refresh today's visible cells for the currently selected "
                        "Single Indicator row only. Supported rows use the faster "
                        "selected-row path; unsupported rows fall back to the full path. "
                        "This updates the currently displayed matrix cells, but it does "
                        "not replace the broader reusable payload used by later "
                        "'Rebuild Time-Series Matrix' actions. Use 'Refresh all indicators "
                        "for today' when you want refreshed today data to persist across "
                        "later rebuilds or indicator switching."
                    ),
                )

            with col_refresh_all:
                refresh_all_today_clicked = st.button(
                    "Refresh all indicators for today",
                    key="scd_single_refresh_all_today_values",
                    disabled=not live_date_in_matrix,
                    use_container_width=True,
                    help=(
                        "Refresh today's broader reusable payload for the selected "
                        "ticker set. This is slower than refreshing one indicator, "
                        "but later 'Rebuild Time-Series Matrix' actions and other "
                        "Single Indicator rows can reuse the refreshed today data "
                        "and freshness timestamp."
                    ),
                )

            refresh_today_clicked = (
                refresh_selected_today_clicked or refresh_all_today_clicked
            )
            refresh_scope = (
                "all_indicators"
                if refresh_all_today_clicked
                else "selected_indicator"
            )

            if refresh_today_clicked:
                spinner_text = (
                    "Refreshing all Single Indicator today values."
                    if refresh_scope == "all_indicators"
                    else "Refreshing this Single Indicator row."
                )

                if refresh_scope == "all_indicators":
                    _get_scd_cache_stats()["force_refreshes"] += 1

                with st.spinner(spinner_text):
                    st.session_state.scd_single_indicator_matrix = (
                        _refresh_scd_single_indicator_live_date_cells(
                            matrix=single_matrix,
                            refresh_scope=refresh_scope,
                        )
                    )
                    st.session_state.scd_single_indicator_matrix_last_run = datetime.now()
                    single_matrix = st.session_state.get("scd_single_indicator_matrix")

                refresh_report = (
                    single_matrix.get("last_live_refresh", {})
                    if isinstance(single_matrix, dict)
                    else {}
                )

                if refresh_report.get("status") in {"ok", "partial"}:
                    cache_stats = _get_scd_cache_stats()
                    cache_stats["today_cell_refreshes"] += 1
                    cache_stats["today_cell_tickers_refreshed"] += len(
                        refresh_report.get("tickers_refreshed", [])
                    )

                    cache_stats["selected_row_refreshes"] += int(
                        refresh_report.get("selected_row_refreshes", 0) or 0
                    )
                    cache_stats["selected_row_refresh_tickers"] += int(
                        refresh_report.get("selected_row_refresh_tickers", 0) or 0
                    )
                    cache_stats["selected_row_refresh_fallbacks"] += int(
                        refresh_report.get("selected_row_refresh_fallbacks", 0) or 0
                    )
                    cache_stats["selected_row_refresh_errors"] += int(
                        refresh_report.get("selected_row_refresh_errors", 0) or 0
                    )

                selected_row_tickers = int(
                    refresh_report.get("selected_row_refresh_tickers", 0) or 0
                )
                fallback_tickers = int(
                    refresh_report.get("selected_row_refresh_fallbacks", 0) or 0
                )
                broad_refresh_tickers = len(
                    refresh_report.get("broad_refresh_tickers", []) or []
                )

                refresh_path_caption = None
                if broad_refresh_tickers:
                    refresh_path_caption = (
                        "Refresh path: full today refresh used for "
                        f"{broad_refresh_tickers} ticker cell(s). Other Single "
                        "Indicator rows can reuse the refreshed today payload when rebuilt."
                    )
                elif selected_row_tickers and fallback_tickers:
                    refresh_path_caption = (
                        "Refresh path: selected-row calculation used for "
                        f"{selected_row_tickers} ticker cell(s); full calculation "
                        f"full fallback used for {fallback_tickers} ticker cell(s)."
                    )
                elif selected_row_tickers:
                    refresh_path_caption = (
                        "Refresh path: selected-row calculation used for "
                        f"{selected_row_tickers} ticker cell(s)."
                    )
                elif fallback_tickers:
                    refresh_path_caption = (
                        "Refresh path: full calculation fallback used for "
                        f"{fallback_tickers} ticker cell(s)."
                    )

                if refresh_report.get("status") == "ok":
                    if refresh_report.get("refresh_scope") == "all_indicators":
                        st.success(
                            "Today's indicator payload refreshed for "
                            f"{len(refresh_report.get('tickers_refreshed', []))} ticker(s) "
                            f"in {refresh_report.get('total_seconds')}s."
                        )
                    else:
                        st.success(
                            "This indicator's today cells refreshed for "
                            f"{len(refresh_report.get('tickers_refreshed', []))} ticker(s) "
                            f"in {refresh_report.get('total_seconds')}s."
                        )

                    if refresh_path_caption:
                        st.caption(refresh_path_caption)
                elif refresh_report.get("status") == "partial":
                    st.warning(
                        "Today's cells partially refreshed. "
                        f"Refreshed {len(refresh_report.get('tickers_refreshed', []))} ticker(s); "
                        f"errors: {len(refresh_report.get('errors', []))}."
                    )
                    if refresh_path_caption:
                        st.caption(refresh_path_caption)
                else:
                    st.warning(
                        refresh_report.get(
                            "message",
                            "Today-refresh did not complete.",
                        )
                    )

            if live_date_in_matrix:
                live_caption = _get_scd_live_as_of_caption(
                    matrix=single_matrix,
                    date_key=live_date_key,
                )
                st.caption(
                    live_caption
                    if live_caption
                    else "Today's data: no current-session timestamp available yet."
                )

            if st.session_state.scd_single_indicator_matrix_last_run:
                st.caption(
                    "Last Single Indicator matrix render/build: "
                    f"{st.session_state.scd_single_indicator_matrix_last_run.isoformat(timespec='seconds')}"
                )

            if SCD_SHOW_TAIL_BUFFER_DIAGNOSTIC:
                with st.expander("Tail-buffer equivalence diagnostic", expanded=False):
                    st.caption(
                        "Diagnostic only. Compares reduced Scenario B buffers against "
                        "the 435-day reference for one ticker, one visible matrix date, "
                        "and the selected Single Indicator row. This does not change "
                        "refresh behavior."
                    )

                    diagnostic_tickers = _dedupe_preserve_order_str(
                        single_matrix.get("tickers", [])
                    )
                    diagnostic_dates = [
                        _normalize_scd_cache_date_value(date_key)
                        for date_key in single_matrix.get("dates", [])
                    ]
                    diagnostic_dates = [
                        date_key for date_key in diagnostic_dates if date_key
                    ]

                    if not diagnostic_tickers or not diagnostic_dates:
                        st.info(
                            "Build a populated Single Indicator matrix before running "
                            "the tail-buffer diagnostic."
                        )
                    else:
                        selected_diag_ticker = st.selectbox(
                            "Diagnostic ticker",
                            options=diagnostic_tickers,
                            index=0,
                            key="scd_tail_diag_ticker",
                        )

                        selected_diag_date = st.selectbox(
                            "Diagnostic date",
                            options=diagnostic_dates,
                            index=len(diagnostic_dates) - 1,
                            key="scd_tail_diag_date",
                            help=(
                                "The diagnostic can run on any visible matrix date. "
                                "This is separate from production today-refresh."
                            ),
                        )

                        selected_candidate_buffers = st.multiselect(
                            "Candidate buffer(s)",
                            options=[80, 120, 180, 250, 320, 365, 400],
                            default=[365],
                            key="scd_tail_diag_buffers",
                            help=(
                                "Each candidate is compared against the 435-day Scenario B "
                                "reference. Start with one buffer to keep runtime manageable. "
                                "Larger buffers are slower but may be necessary for the full "
                                "rule-engine path to produce comparable results."
                            ),
                        )
                        if st.button(
                            "Run tail-buffer diagnostic",
                            key="scd_run_tail_buffer_diagnostic",
                        ):
                            with st.spinner("Running tail-buffer equivalence diagnostic."):
                                try:
                                    diagnostic_report = (
                                        _run_scd_tail_buffer_equivalence_diagnostic(
                                            matrix=single_matrix,
                                            ticker=selected_diag_ticker,
                                            diagnostic_date_key=selected_diag_date,
                                            candidate_buffers=list(selected_candidate_buffers),
                                        )
                                    )
                                    st.session_state.scd_tail_buffer_diagnostic_last = (
                                        diagnostic_report
                                    )
                                except Exception as e:
                                    st.session_state.scd_tail_buffer_diagnostic_last = {
                                        "status": "error",
                                        "error": str(e),
                                        "created_at": datetime.now().isoformat(
                                            timespec="seconds"
                                        ),
                                    }

                    st.markdown("---")
                    st.caption(
                        "Selected-family scoring diagnostic. Compares the full current "
                        "scoring path against scoring only the selected row's rule-engine "
                        "family, using the same 435-day buffer and same numeric path."
                    )

                    if st.button(
                        "Run selected-family scoring diagnostic",
                        key="scd_run_selected_family_scoring_diagnostic",
                    ):
                        with st.spinner("Running selected-family scoring diagnostic."):
                            try:
                                scoring_report = (
                                    _run_scd_selected_family_scoring_diagnostic(
                                        matrix=single_matrix,
                                        ticker=selected_diag_ticker,
                                        diagnostic_date_key=selected_diag_date,
                                    )
                                )
                                st.session_state.scd_selected_family_scoring_diagnostic_last = (
                                    scoring_report
                                )
                            except Exception as e:
                                st.session_state.scd_selected_family_scoring_diagnostic_last = {
                                    "status": "error",
                                    "error": str(e),
                                    "created_at": datetime.now().isoformat(
                                        timespec="seconds"
                                    ),
                                }

                    scoring_report = st.session_state.get(
                        "scd_selected_family_scoring_diagnostic_last"
                    )
                    if isinstance(scoring_report, dict):
                        if scoring_report.get("status") == "ok":
                            st.caption(
                                "Selected-family scoring run: "
                                f"reference={scoring_report.get('reference_seconds')}s · "
                                f"candidate={scoring_report.get('candidate_seconds')}s · "
                                f"delta={scoring_report.get('seconds_delta')}s · "
                                f"family={scoring_report.get('engine_indicator')}"
                            )

                            scoring_df = pd.DataFrame([scoring_report])
                            display_cols = [
                                col
                                for col in [
                                    "engine_indicator",
                                    "safe_for_candidate",
                                    "reference_seconds",
                                    "candidate_seconds",
                                    "seconds_delta",
                                    "value_match",
                                    "score_match",
                                    "signal_match",
                                    "display_text_match",
                                    "status_match",
                                    "value_delta",
                                    "reference_score",
                                    "candidate_score",
                                    "reference_signal",
                                    "candidate_signal",
                                ]
                                if col in scoring_df.columns
                            ]
                            st.dataframe(
                                scoring_df[display_cols],
                                use_container_width=True,
                                hide_index=True,
                            )

                            with st.expander(
                                "Raw selected-family scoring diagnostic report",
                                expanded=False,
                            ):
                                st.json(scoring_report)
                        else:
                            st.warning(
                                scoring_report.get(
                                    "error",
                                    "Selected-family scoring diagnostic did not complete.",
                                )
                            )

                    st.markdown("---")
                    st.caption(
                        "Selected-row numeric config diagnostic. Compares selected-family "
                        "scoring with the broad numeric path against selected-family "
                        "scoring with a minimal selected-row compute config. D3-D5 "
                        "currently supports RSI, SMA, EMA, HMA, VWMA, ROC, "
                        "Williams %R, CCI, MFI, and CMF rows."
                    )

                    if st.button(
                        "Run selected-row numeric config diagnostic",
                        key="scd_run_selected_row_numeric_config_diagnostic",
                    ):
                        with st.spinner("Running selected-row numeric config diagnostic."):
                            try:
                                numeric_config_report = (
                                    _run_scd_selected_row_numeric_config_diagnostic(
                                        matrix=single_matrix,
                                        ticker=selected_diag_ticker,
                                        diagnostic_date_key=selected_diag_date,
                                    )
                                )
                                st.session_state.scd_selected_row_numeric_config_diagnostic_last = (
                                    numeric_config_report
                                )
                            except Exception as e:
                                st.session_state.scd_selected_row_numeric_config_diagnostic_last = {
                                    "status": "error",
                                    "error": str(e),
                                    "created_at": datetime.now().isoformat(
                                        timespec="seconds"
                                    ),
                                }

                    numeric_config_report = st.session_state.get(
                        "scd_selected_row_numeric_config_diagnostic_last"
                    )
                    if isinstance(numeric_config_report, dict):
                        if numeric_config_report.get("status") == "ok":
                            st.caption(
                                "Selected-row numeric config run: "
                                f"reference={numeric_config_report.get('reference_seconds')}s · "
                                f"candidate={numeric_config_report.get('candidate_seconds')}s · "
                                f"delta={numeric_config_report.get('seconds_delta')}s · "
                                f"family={numeric_config_report.get('engine_indicator')}"
                            )

                            numeric_config_df = pd.DataFrame([numeric_config_report])
                            display_cols = [
                                col
                                for col in [
                                    "engine_indicator",
                                    "safe_for_candidate",
                                    "reference_seconds",
                                    "candidate_seconds",
                                    "seconds_delta",
                                    "value_match",
                                    "score_match",
                                    "signal_match",
                                    "display_text_match",
                                    "status_match",
                                    "value_delta",
                                    "reference_compute_config_keys",
                                    "candidate_compute_config_keys",
                                    "reference_score",
                                    "candidate_score",
                                    "reference_signal",
                                    "candidate_signal",
                                ]
                                if col in numeric_config_df.columns
                            ]
                            st.dataframe(
                                numeric_config_df[display_cols],
                                use_container_width=True,
                                hide_index=True,
                            )

                            with st.expander(
                                "Raw selected-row numeric config diagnostic report",
                                expanded=False,
                            ):
                                st.json(numeric_config_report)
                        else:
                            st.warning(
                                numeric_config_report.get(
                                    "error",
                                    "Selected-row numeric config diagnostic did not complete.",
                                )
                            )

                    diagnostic_report = st.session_state.get(
                        "scd_tail_buffer_diagnostic_last"
                    )
                    if isinstance(diagnostic_report, dict):
                        if diagnostic_report.get("status") == "ok":
                            st.caption(
                                "Reference run: "
                                f"{diagnostic_report.get('reference_seconds')}s · "
                                f"Rows: {diagnostic_report.get('reference_context_rows')} · "
                                f"Window: {diagnostic_report.get('reference_context_first_date')} → "
                                f"{diagnostic_report.get('reference_context_last_date')}"
                            )

                            candidates_df = pd.DataFrame(
                                diagnostic_report.get("candidates", [])
                            )
                            if not candidates_df.empty:
                                display_cols = [
                                    col
                                    for col in [
                                        "candidate_buffer_days",
                                        "safe_for_candidate",
                                        "candidate_seconds",
                                        "candidate_context_rows",
                                        "value_match",
                                        "score_match",
                                        "signal_match",
                                        "display_text_match",
                                        "status_match",
                                        "value_delta",
                                        "error",
                                    ]
                                    if col in candidates_df.columns
                                ]
                                st.dataframe(
                                    candidates_df[display_cols],
                                    use_container_width=True,
                                    hide_index=True,
                                )

                            with st.expander("Raw tail-buffer diagnostic report", expanded=False):
                                st.json(diagnostic_report)
                        else:
                            st.warning(
                                diagnostic_report.get(
                                    "error",
                                    "Tail-buffer diagnostic did not complete.",
                                )
                            )

            _render_scd_single_indicator_matrix_view(single_matrix)

            if single_matrix.get("errors"):
                st.warning("Some ticker payloads produced errors.")
                with st.expander("View Single Indicator ticker errors", expanded=False):
                    st.write(single_matrix.get("errors"))

            with st.expander("Ticker build diagnostics", expanded=False):
                st.json(single_matrix.get("ticker_status", {}))

            profile = single_matrix.get("profile", {})
            if isinstance(profile, dict) and profile:
                st.caption(
                    f"Built in {profile.get('total_seconds')}s · "
                    f"Request mode: {single_matrix.get('anchor_mode')} · "
                    f"Anchor: {single_matrix.get('anchor_date')}"
                )

            with st.expander("Cache diagnostics", expanded=False):
                _render_scd_cache_diagnostics()
        else:
            st.info(
                "Build the Single Indicator time-series matrix to prepare the "
                "dates × tickers payload for the next rendering step."
            )

        return

    selected_row_keys = _render_scd_indicator_selection_controls()

    st.subheader("Build Comparison Matrix")

    st.checkbox(
        "Use specific as-of date",
        key="scd_use_anchor_date",
        help=(
            "Use this to build the comparison as of a selected date instead of "
            "the latest available completed snapshot. If the selected date is not "
            "a trading day, the existing data path resolves to the nearest valid "
            "trading day according to the current date-handling rules."
        ),
    )

    use_anchor_date = bool(st.session_state.get("scd_use_anchor_date", False))

    selected_anchor_date = None
    if use_anchor_date:
        st.date_input(
            "As-of date",
            key="scd_anchor_date",
            help=(
                "Choose the date for the comparison snapshot. Selecting today is "
                "allowed, but values may depend on what data is available for the "
                "current session."
            ),
        )
        selected_anchor_date = st.session_state.get("scd_anchor_date")

    effective_anchor_date = _resolve_scd_effective_anchor_date(
        use_anchor_date=use_anchor_date,
        selected_anchor_date=selected_anchor_date,
    )

    if use_anchor_date:
        st.caption(f"Snapshot date: {effective_anchor_date}")
    else:
        st.caption(f"Snapshot date: Latest available completed snapshot ({effective_anchor_date})")

    target_date_key_for_build = _resolve_scd_cross_sectional_target_date_key(
        effective_anchor_date
    )
    live_date_key_for_build = _get_scd_current_live_date_key()
    is_live_snapshot = (
        bool(target_date_key_for_build)
        and bool(live_date_key_for_build)
        and _normalize_scd_cache_date_value(target_date_key_for_build)
        == live_date_key_for_build
    )

    if is_live_snapshot:
        st.caption(
            "Today/live snapshot: Build uses available session cache by default "
            "for speed. Use Refresh today's values when you want current values."
        )

    can_build_matrix = bool(selected_tickers) and bool(selected_row_keys)
    if not can_build_matrix:
        st.info("Select at least one ticker and one indicator row to build the SCD matrix.")

    col_build, col_refresh_live, col_clear_matrix = st.columns([0.34, 0.33, 0.33])

    with col_build:
        build_clicked = st.button(
            "Rebuild Comparison Matrix",
            key="scd_build_matrix",
            type="primary",
            disabled=not can_build_matrix,
            use_container_width=True,
            help=(
                "Builds the comparison matrix using available session cache when possible. "
                "This is the speed-first default."
            ),
        )

    with col_refresh_live:
        refresh_live_clicked = st.button(
            "Refresh today's values",
            key="scd_refresh_live_matrix",
            disabled=not can_build_matrix or not is_live_snapshot,
            use_container_width=True,
            help=(
                "Available only when the Multiple Indicators as-of date resolves to "
                "today's live trading date. Bypasses the SCD session cache for the "
                "currently selected tickers and rebuilds the matrix with current values."
            ),
        )

    with col_clear_matrix:
        if st.button(
            "Clear Results",
            key="scd_clear_matrix",
            disabled=st.session_state.scd_signal_matrix is None,
            use_container_width=True,
            help=(
                "Removes the currently displayed heatmap and detail table from the page. "
                "This does not clear saved ticker data, so rebuilding can still be fast."
            ),
        ):
            st.session_state.scd_signal_matrix = None
            st.session_state.scd_matrix_last_run = None
            st.rerun()

    if build_clicked or refresh_live_clicked:
        # Build remains cache-first by default. The explicit live-refresh action
        # bypasses the session cache for today's Multiple Indicators values only.
        force_refresh_for_build = bool(
            st.session_state.get("scd_force_refresh_cache", False)
        )
        if refresh_live_clicked:
            force_refresh_for_build = True

        if force_refresh_for_build:
            _get_scd_cache_stats()["force_refreshes"] += 1

        spinner_text = (
            "Refreshing today's Multiple Indicators values..."
            if refresh_live_clicked
            else "Building comparison matrix from existing rolling signal data..."
        )

        with st.spinner(spinner_text):
            st.session_state.scd_signal_matrix = _build_scd_cross_sectional_matrix(
                selected_tickers=selected_tickers,
                selected_row_keys=selected_row_keys,
                window_days=10,
                force_refresh=force_refresh_for_build,
                anchor_date=effective_anchor_date,
            )
            st.session_state.scd_matrix_last_run = datetime.now().isoformat(timespec="seconds")

        stale_rebuild_completed = bool(
            st.session_state.get(
                _DATA_MANAGEMENT_SCD_STALE_KEY,
                False,
            )
        )

        st.session_state.pop(
            _DATA_MANAGEMENT_SCD_STALE_KEY,
            None,
        )

        if stale_rebuild_completed:
            st.rerun()

        refreshed_matrix = st.session_state.get("scd_signal_matrix")
        refreshed_profile = (
            refreshed_matrix.get("profile", {})
            if isinstance(refreshed_matrix, dict)
            else {}
        )

        if refresh_live_clicked:
            st.success(
                "Today's Multiple Indicators values refreshed for "
                f"{len(selected_tickers)} ticker(s)"
                + (
                    f" in {refreshed_profile.get('total_seconds')}s."
                    if isinstance(refreshed_profile, dict)
                    and refreshed_profile.get("total_seconds") is not None
                    else "."
                )
            )
     
    if st.session_state.scd_matrix_last_run:
        st.caption(f"Last SCD matrix render/build: {st.session_state.scd_matrix_last_run}")

    live_date_key = _get_scd_current_live_date_key()
    current_matrix = st.session_state.get("scd_signal_matrix")
    if (
        isinstance(current_matrix, dict)
        and live_date_key
        and _normalize_scd_cache_date_value(current_matrix.get("target_date")) == live_date_key
    ):
        live_caption = _get_scd_live_as_of_caption(
            matrix=current_matrix,
            date_key=live_date_key,
        )
        st.caption(
            live_caption
            if live_caption
            else "Today's data: no current-session timestamp available yet."
        )

    _render_scd_matrix_view(st.session_state.scd_signal_matrix)

    with st.expander("Advanced options", expanded=False):
        st.checkbox(
            "Recalculate selected tickers on next build",
            key="scd_force_refresh_cache",
            help=(
                "Use this when you want the currently selected tickers recalculated "
                "instead of reused from this session's saved results. This only refreshes "
                "the tickers currently selected. Other cached tickers are kept. For a full "
                "reset of all saved ticker data, use Clear Cache."
            ),
        )

        cache_is_empty = (
            not st.session_state.get("scd_payload_cache")
            and not st.session_state.get("scd_hover_ohlcv_cache")
        )

        if st.button(
            "Clear Cache",
            key="scd_clear_cache",
            disabled=cache_is_empty,
            use_container_width=True,
            help=(
                "Clears all saved ticker data from this app session. The next build "
                "will calculate the selected tickers from scratch. Use this when "
                "you want a full reset, not just a refresh of the currently selected tickers."
            ),
        ):
            _clear_scd_session_cache()
            st.rerun()

    with st.expander("Cache diagnostics", expanded=False):
        _render_scd_cache_diagnostics()


# ---------------------------------------------------------------------
# Data Management acquisition + mutation UI helpers
# ---------------------------------------------------------------------

_DATA_MANAGEMENT_ACQUISITION_CONTEXT_KEY = (
    "data_management_acquisition_context"
)

_DATA_MANAGEMENT_MANUAL_ENTRY_CONTEXT_KEY = (
    "data_management_manual_entry_context"
)

_DATA_MANAGEMENT_MUTATION_PLAN_KEY = (
    "data_management_mutation_plan"
)
_DATA_MANAGEMENT_MUTATION_CONFIRMED_FINGERPRINT_KEY = (
    "data_management_mutation_confirmed_fingerprint"
)
_DATA_MANAGEMENT_MUTATION_RESULT_KEY = (
    "data_management_mutation_result"
)
_DATA_MANAGEMENT_MUTATION_ERROR_KEY = (
    "data_management_mutation_error"
)
_DATA_MANAGEMENT_SCD_STALE_KEY = (
    "data_management_scd_stale"
)

_DATA_MANAGEMENT_MAINTENANCE_REQUEST_KEY = (
    "data_management_maintenance_request"
)


def _prepare_data_management_maintenance_request(
    request: Dict[str, Any],
) -> None:
    """
    Prepare one session-only Ticker Diagnostics maintenance handoff.

    This helper may preselect the existing acquisition operation and stored
    ticker controls. It does not acquire source data, build a MutationPlan,
    approve changes, commit changes, or write to SQLite.
    """
    if not isinstance(
        request,
        dict,
    ):
        return

    operation = str(
        request.get(
            "operation",
            "",
        )
    ).strip()

    if operation not in {
        "Update to Current",
        "Repair Missing",
        "Repair Duplicate Stored Keys",
    }:
        return

    ticker = str(
        request.get(
            "ticker",
            "",
        )
    ).strip().upper()

    if not ticker:
        return

    if st.session_state.get(
        _DATA_MANAGEMENT_MUTATION_PLAN_KEY
    ) is not None:
        return

    normalized_request = dict(
        request
    )

    normalized_request[
        "operation"
    ] = operation
    normalized_request[
        "ticker"
    ] = ticker
    normalized_request[
        "origin"
    ] = str(
        normalized_request.get(
            "origin",
            "Ticker Diagnostics",
        )
    ).strip() or "Ticker Diagnostics"

    st.session_state[
        _DATA_MANAGEMENT_MAINTENANCE_REQUEST_KEY
    ] = normalized_request

    st.session_state[
        "data_management_acquisition_operation"
    ] = operation

    st.session_state[
        "data_management_acquisition_maintenance_ticker"
    ] = ticker

    st.session_state.pop(
        _DATA_MANAGEMENT_ACQUISITION_CONTEXT_KEY,
        None,
    )


def _build_data_management_acquisition_context(
    result: DataAcquisitionResult,
) -> Dict[str, Any]:
    """
    Build UI-only acquisition context for the active mutation Preview.

    This context preserves the distinction between the administrator's
    original requested interval and the effective persistence scope passed
    to DataMutationManager. It is display state only; MutationPlan remains
    authoritative for Preview / Confirm / Commit.
    """
    if not isinstance(
        result,
        DataAcquisitionResult,
    ):
        raise TypeError(
            "result must be a DataAcquisitionResult."
        )

    return {
        "source": result.source,
        "requested_tickers": list(
            result.requested_tickers
        ),
        "requested_start_date": (
            result.requested_start_date.isoformat()
        ),
        "requested_end_date": (
            result.requested_end_date.isoformat()
        ),
        "effective_start_date": (
            result.effective_start_date.isoformat()
            if result.effective_start_date is not None
            else None
        ),
        "effective_end_date": (
            result.effective_end_date.isoformat()
            if result.effective_end_date is not None
            else None
        ),
        "latest_expected_stored_session": (
            result.latest_expected_stored_session.isoformat()
        ),
        "yfinance_end_exclusive": (
            result.yfinance_end_exclusive.isoformat()
            if result.yfinance_end_exclusive is not None
            else None
        ),
        "candidate_count": len(
            result.candidates
        ),
        "issues": [
            {
                "level": issue.level,
                "code": issue.code,
                "message": issue.message,
                "ticker": issue.ticker,
            }
            for issue in result.issues
        ],
    }


def _render_data_management_acquisition_context(
    context: Dict[str, Any],
) -> None:
    """Render the source request and effective persistence scope."""
    if not isinstance(
        context,
        dict,
    ):
        return

    st.caption(
        "Canonical source: "
        f"{context.get('source') or '—'}"
    )

    scope_columns = st.columns(4)

    scope_columns[0].metric(
        "Requested Start",
        context.get(
            "requested_start_date"
        ) or "—",
    )
    scope_columns[1].metric(
        "Requested End",
        context.get(
            "requested_end_date"
        ) or "—",
    )
    scope_columns[2].metric(
        "Effective Start",
        context.get(
            "effective_start_date"
        ) or "—",
    )
    scope_columns[3].metric(
        "Effective End",
        context.get(
            "effective_end_date"
        ) or "—",
    )

    persistence_columns = st.columns(3)

    persistence_columns[0].metric(
        "Latest Expected Stored Session",
        context.get(
            "latest_expected_stored_session"
        ) or "—",
    )
    persistence_columns[1].metric(
        "Source Candidates",
        f"{context.get('candidate_count', 0):,}",
    )
    persistence_columns[2].metric(
        "yFinance Exclusive End",
        context.get(
            "yfinance_end_exclusive"
        ) or "—",
    )

    acquisition_issues = context.get(
        "issues",
        [],
    )

    for issue in acquisition_issues:
        ticker = issue.get(
            "ticker"
        )

        prefix = (
            f"{ticker}: "
            if ticker
            else ""
        )

        message = (
            prefix
            + str(
                issue.get(
                    "message",
                    "",
                )
            )
        )

        if issue.get(
            "level"
        ) == "error":
            st.error(message)
        else:
            st.warning(message)


def _render_data_management_acquisition_controls(
    *,
    inventory: list[Dict[str, Any]],
    database_manager: DatabaseManager,
    latest_expected_stored_session: Any,
) -> None:
    """
    Render canonical Data Management acquisition and maintenance workflows.

    Supported operations:
    - Add Market Data
    - Update to Current
    - Repair Missing
    - Repair Duplicate Stored Keys
    - Backfill Earlier

    Acquisition remains read-only. Build Preview passes the exact effective
    source result into DataMutationManager.build_plan(); the existing mutation
    workflow continues to own Preview / Approve / Apply.
    """
    active_plan = st.session_state.get(
        _DATA_MANAGEMENT_MUTATION_PLAN_KEY
    )

    if (
        isinstance(
            active_plan,
            MutationPlan,
        )
        and active_plan.operation
        in {
            "Manual Add",
            "Manual Replace",
        }
    ):
        return

    st.markdown("---")
    st.subheader("Acquire Market Data")

    st.caption(
        "Acquire canonical daily OHLCV from yFinance and preview the exact "
        "database actions before anything is saved. Review the preview, "
        "approve it, then apply the approved changes."
    )

    acquisition_context = st.session_state.get(
        _DATA_MANAGEMENT_ACQUISITION_CONTEXT_KEY
    )

    maintenance_request = st.session_state.get(
        _DATA_MANAGEMENT_MAINTENANCE_REQUEST_KEY
    )

    if active_plan is not None:
        context_workflow = (
            acquisition_context.get(
                "workflow"
            )
            if isinstance(
                acquisition_context,
                dict,
            )
            else None
        )

        if context_workflow != "Historical Data Reconciliation":
            st.info(
                "A Database Change Preview is active. Approve and apply it, "
                "or Cancel Preview, before changing the acquisition request."
            )

            if isinstance(
                acquisition_context,
                dict,
            ):
                _render_data_management_acquisition_context(
                    acquisition_context
                )

        return

    try:
        default_end_date = pd.Timestamp(
            latest_expected_stored_session
        ).date()
    except Exception:
        default_end_date = date.today()

    operation_labels = [
        "Add Market Data",
        "Update to Current",
        "Repair Missing",
        "Repair Duplicate Stored Keys",
        "Backfill Earlier",
    ]

    selected_operation = st.radio(
        "Acquisition Operation",
        options=operation_labels,
        horizontal=True,
        key="data_management_acquisition_operation",
        help=(
            "Add Market Data uses an explicit ticker/date request. "
            "Update to Current fills the stale tail after a stored ticker's "
            "Last Date. Repair Missing reacquires the envelope containing "
            "known Internal Gaps while preserving existing rows. Repair "
            "Duplicate Stored Keys reacquires canonical source observations "
            "for exact duplicate ticker/date keys and replaces every stored "
            "physical copy with one canonical row. Backfill Earlier extends "
            "stored history before the current First Date."
        ),
    )

    inventory_by_ticker = {
        str(
            row.get(
                "ticker",
                "",
            )
        ).strip().upper(): row
        for row in inventory
        if str(
            row.get(
                "ticker",
                "",
            )
        ).strip()
    }

    stored_tickers = sorted(
        inventory_by_ticker
    )

    requested_tickers: list[str] = []
    requested_start_date: Optional[date] = None
    requested_end_date: Optional[date] = None
    backend_operation: Optional[str] = None
    build_preview_clicked = False

    if selected_operation == "Add Market Data":
        backend_operation = "Add"

        with st.form(
            "data_management_acquisition_form"
        ):
            ticker_input = st.text_input(
                "Ticker(s)",
                value="",
                help=(
                    "Enter one or more ticker symbols separated by commas "
                    "or spaces."
                ),
            )

            date_columns = st.columns(2)

            with date_columns[0]:
                requested_start_date = st.date_input(
                    "Start Date",
                    value=default_end_date,
                )

            with date_columns[1]:
                requested_end_date = st.date_input(
                    "End Date",
                    value=default_end_date,
                )

            build_preview_clicked = (
                st.form_submit_button(
                    "Preview Database Changes",
                    type="primary",
                    use_container_width=True,
                    help=(
                        "Fetch the requested yFinance data and compare it with "
                        "the authoritative database. This does not save or "
                        "replace any records."
                    ),
                )
            )

        if build_preview_clicked:
            requested_tickers = [
                ticker
                for ticker in (
                    str(ticker_input)
                    .replace(",", " ")
                    .split()
                )
                if ticker
            ]

    else:
        if not stored_tickers:
            st.warning(
                "No stored tickers are available for this maintenance "
                "operation."
            )
            return

        selected_ticker = st.selectbox(
            "Stored Ticker",
            options=stored_tickers,
            key="data_management_acquisition_maintenance_ticker",
            help=(
                "Choose one ticker currently stored in daily_prices."
            ),
        )

        selected_inventory = (
            inventory_by_ticker[
                selected_ticker
            ]
        )

        if isinstance(
            maintenance_request,
            dict,
        ):
            prepared_operation = str(
                maintenance_request.get(
                    "operation",
                    "",
                )
            ).strip()
            prepared_ticker = str(
                maintenance_request.get(
                    "ticker",
                    "",
                )
            ).strip().upper()

            if (
                prepared_operation
                == selected_operation
                and prepared_ticker
                == selected_ticker
            ):
                reason = str(
                    maintenance_request.get(
                        "reason",
                        "",
                    )
                ).strip()

                suggested_start = (
                    maintenance_request.get(
                        "suggested_start_date"
                    )
                )
                suggested_end = (
                    maintenance_request.get(
                        "suggested_end_date"
                    )
                )

                prepared_message = (
                    "Prepared from Ticker Diagnostics"
                )

                if reason:
                    prepared_message += (
                        f": {reason}"
                    )

                st.info(
                    prepared_message
                )

                if (
                    suggested_start
                    and suggested_end
                ):
                    st.caption(
                        "Diagnostic-derived request scope: "
                        f"{suggested_start} → "
                        f"{suggested_end}. "
                        "Review the authoritative scope below, then explicitly "
                        "build the Preview when ready."
                    )

                evidence = (
                    maintenance_request.get(
                        "evidence",
                        {},
                    )
                )

                if isinstance(
                    evidence,
                    dict,
                ):
                    if (
                        selected_operation
                        == "Repair Missing"
                    ):
                        gap_count = int(
                            evidence.get(
                                "internal_gap_count",
                                0,
                            )
                            or 0
                        )
                        gap_range_count = len(
                            evidence.get(
                                "internal_gap_ranges",
                                [],
                            )
                            or []
                        )

                        st.caption(
                            "Diagnostic evidence carried forward: "
                            f"{gap_count:,} missing expected session(s) "
                            f"across {gap_range_count:,} Internal Gap "
                            "range(s)."
                        )

                    elif (
                        selected_operation
                        == "Update to Current"
                    ):
                        tail_count = int(
                            evidence.get(
                                "missing_tail_count",
                                0,
                            )
                            or 0
                        )
                        tail_range_count = len(
                            evidence.get(
                                "missing_tail_ranges",
                                [],
                            )
                            or []
                        )

                        st.caption(
                            "Diagnostic evidence carried forward: "
                            f"{tail_count:,} missing expected tail session(s) "
                            f"across {tail_range_count:,} tail range(s)."
                        )

                    elif (
                        selected_operation
                        == "Repair Duplicate Stored Keys"
                    ):
                        duplicate_key_count = int(
                            evidence.get(
                                "duplicate_stored_key_count",
                                0,
                            )
                            or 0
                        )
                        excess_row_count = int(
                            evidence.get(
                                "duplicate_stored_excess_rows",
                                0,
                            )
                            or 0
                        )

                        st.caption(
                            "Diagnostic evidence carried forward: "
                            f"{duplicate_key_count:,} duplicate stored "
                            "(Ticker, Date) key(s), representing "
                            f"{excess_row_count:,} excess physical row(s)."
                        )
            else:
                st.session_state.pop(
                    _DATA_MANAGEMENT_MAINTENANCE_REQUEST_KEY,
                    None,
                )
                maintenance_request = None

        stored_columns = st.columns(4)

        stored_columns[0].metric(
            "Stored Records",
            f"{int(selected_inventory.get('records', 0) or 0):,}",
        )
        stored_columns[1].metric(
            "First Stored Date",
            selected_inventory.get(
                "first_date"
            ) or "—",
        )
        stored_columns[2].metric(
            "Last Stored Date",
            selected_inventory.get(
                "last_date"
            ) or "—",
        )
        stored_columns[3].metric(
            "Status",
            selected_inventory.get(
                "status"
            ) or "—",
        )

        requested_tickers = [
            selected_ticker
        ]

        maintenance_request_ready = True

        if selected_operation == "Update to Current":
            backend_operation = "Update to Current"

            try:
                last_stored_date = date.fromisoformat(
                    str(
                        selected_inventory[
                            "last_date"
                        ]
                    )
                )
                requested_start_date = (
                    last_stored_date
                    + timedelta(days=1)
                )
                requested_end_date = (
                    default_end_date
                )
            except Exception as exc:
                st.error(
                    "Unable to resolve the stored Last Date for "
                    f"{selected_ticker}: {exc}"
                )
                return

            scope_columns = st.columns(2)

            scope_columns[0].metric(
                "Update From",
                requested_start_date.isoformat(),
            )
            scope_columns[1].metric(
                "Update Through",
                requested_end_date.isoformat(),
            )

            if (
                requested_start_date
                > requested_end_date
            ):
                maintenance_request_ready = False
                st.info(
                    f"{selected_ticker} already reaches the Latest Expected "
                    "Stored Session. There is no stale tail to update."
                )
            else:
                st.caption(
                    "Update to Current acquires the calendar interval after "
                    "the current Last Date through the Latest Expected Stored "
                    "Session. Existing stored observations are preserved."
                )

        elif selected_operation == "Repair Missing":
            backend_operation = "Repair Missing"

            try:
                diagnostics = (
                    database_manager.get_ticker_diagnostics(
                        selected_ticker
                    )
                )
            except Exception as exc:
                st.error(
                    "Unable to read Internal Gap diagnostics for "
                    f"{selected_ticker}: {exc}"
                )
                return

            internal_gap_dates = (
                list(
                    diagnostics.get(
                        "internal_gap_dates",
                        [],
                    )
                )
                if isinstance(
                    diagnostics,
                    dict,
                )
                else []
            )

            if not internal_gap_dates:
                maintenance_request_ready = False
                st.info(
                    f"{selected_ticker} has no known Internal Gaps to repair."
                )
            else:
                try:
                    requested_start_date = (
                        date.fromisoformat(
                            str(
                                internal_gap_dates[
                                    0
                                ]
                            )
                        )
                    )
                    requested_end_date = (
                        date.fromisoformat(
                            str(
                                internal_gap_dates[
                                    -1
                                ]
                            )
                        )
                    )
                except Exception as exc:
                    st.error(
                        "Unable to resolve the Internal Gap repair scope for "
                        f"{selected_ticker}: {exc}"
                    )
                    return

                gap_columns = st.columns(3)

                gap_columns[0].metric(
                    "Missing Sessions",
                    f"{len(internal_gap_dates):,}",
                )
                gap_columns[1].metric(
                    "Repair From",
                    requested_start_date.isoformat(),
                )
                gap_columns[2].metric(
                    "Repair Through",
                    requested_end_date.isoformat(),
                )

                st.caption(
                    "Repair Missing reacquires the continuous envelope from "
                    "the first known Internal Gap through the last known "
                    "Internal Gap. Existing stored rows inside that envelope "
                    "are preserved; only eligible missing observations can "
                    "be added."
                )

        elif (
            selected_operation
            == "Repair Duplicate Stored Keys"
        ):
            backend_operation = (
                "Repair Duplicate Stored Keys"
            )

            try:
                diagnostics = (
                    database_manager.get_ticker_diagnostics(
                        selected_ticker
                    )
                )
            except Exception as exc:
                st.error(
                    "Unable to read Duplicate Stored Key diagnostics for "
                    f"{selected_ticker}: {exc}"
                )
                return

            duplicate_stored_keys = (
                list(
                    diagnostics.get(
                        "duplicate_stored_keys",
                        [],
                    )
                )
                if isinstance(
                    diagnostics,
                    dict,
                )
                else []
            )

            duplicate_dates = [
                str(
                    duplicate_key.get(
                        "date",
                        "",
                    )
                ).strip()
                for duplicate_key
                in duplicate_stored_keys
                if str(
                    duplicate_key.get(
                        "date",
                        "",
                    )
                ).strip()
            ]

            if not duplicate_dates:
                maintenance_request_ready = False
                st.info(
                    f"{selected_ticker} has no Duplicate Stored Keys "
                    "to repair."
                )
            else:
                try:
                    requested_start_date = (
                        date.fromisoformat(
                            duplicate_dates[
                                0
                            ]
                        )
                    )
                    requested_end_date = (
                        date.fromisoformat(
                            duplicate_dates[
                                -1
                            ]
                        )
                    )
                except Exception as exc:
                    st.error(
                        "Unable to resolve the Duplicate Stored Key "
                        f"repair scope for {selected_ticker}: {exc}"
                    )
                    return

                duplicate_physical_rows = sum(
                    int(
                        duplicate_key.get(
                            "physical_rows",
                            0,
                        )
                        or 0
                    )
                    for duplicate_key
                    in duplicate_stored_keys
                )

                duplicate_excess_rows = sum(
                    int(
                        duplicate_key.get(
                            "excess_rows",
                            0,
                        )
                        or 0
                    )
                    for duplicate_key
                    in duplicate_stored_keys
                )

                duplicate_columns = st.columns(
                    5
                )

                duplicate_columns[0].metric(
                    "Duplicate Keys",
                    f"{len(duplicate_dates):,}",
                )
                duplicate_columns[1].metric(
                    "Physical Rows",
                    f"{duplicate_physical_rows:,}",
                )
                duplicate_columns[2].metric(
                    "Excess Rows",
                    f"{duplicate_excess_rows:,}",
                )
                duplicate_columns[3].metric(
                    "Acquire From",
                    requested_start_date.isoformat(),
                )
                duplicate_columns[4].metric(
                    "Acquire Through",
                    requested_end_date.isoformat(),
                )

                st.dataframe(
                    pd.DataFrame(
                        [
                            {
                                "Duplicate Date": (
                                    duplicate_key[
                                        "date"
                                    ]
                                ),
                                "Physical Rows": (
                                    duplicate_key[
                                        "physical_rows"
                                    ]
                                ),
                                "Excess Rows": (
                                    duplicate_key[
                                        "excess_rows"
                                    ]
                                ),
                            }
                            for duplicate_key
                            in duplicate_stored_keys
                        ]
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

                st.caption(
                    "Canonical yFinance data is acquired over the continuous "
                    "calendar envelope from the first duplicate date through "
                    "the last duplicate date. Only the exact Duplicate Dates "
                    "shown above are repair targets; intervening non-duplicate "
                    "stored dates are not eligible for mutation."
                )

        else:
            backend_operation = "Backfill Earlier"

            try:
                first_stored_date = date.fromisoformat(
                    str(
                        selected_inventory[
                            "first_date"
                        ]
                    )
                )
            except Exception as exc:
                st.error(
                    "Unable to resolve the stored First Date for "
                    f"{selected_ticker}: {exc}"
                )
                return

            requested_end_date = (
                first_stored_date
                - timedelta(days=1)
            )

            requested_start_date = st.date_input(
                "Backfill Start Date",
                value=requested_end_date,
                max_value=requested_end_date,
                key="data_management_backfill_start_date",
                help=(
                    "Choose how far back to extend stored history. "
                    "The backfill ends on the calendar day immediately before "
                    "the ticker's current First Stored Date."
                ),
            )

            backfill_columns = st.columns(2)

            backfill_columns[0].metric(
                "Backfill From",
                requested_start_date.isoformat(),
            )
            backfill_columns[1].metric(
                "Backfill Through",
                requested_end_date.isoformat(),
            )

            st.caption(
                "Backfill Earlier preserves every existing stored observation "
                "and only adds eligible observations before the current "
                "First Stored Date."
            )

        build_preview_clicked = st.button(
            "Preview Database Changes",
            key="data_management_acquisition_maintenance_preview",
            type="primary",
            use_container_width=True,
            disabled=not maintenance_request_ready,
            help=(
                "Fetch canonical yFinance data for this maintenance scope and "
                "compare it with the authoritative database. Nothing is "
                "changed until the resulting Preview is approved and applied."
            ),
        )

    if not build_preview_clicked:
        if isinstance(
            acquisition_context,
            dict,
        ):
            _render_data_management_acquisition_context(
                acquisition_context
            )

        return

    if not requested_tickers:
        st.error(
            "Enter at least one ticker before previewing database changes."
        )
        return

    if (
        requested_start_date is None
        or requested_end_date is None
    ):
        st.error(
            "A valid Start Date and End Date are required before "
            "previewing database changes."
        )
        return

    if requested_start_date > requested_end_date:
        st.error(
            "Requested Start Date cannot be later than End Date."
        )
        return

    if backend_operation is None:
        st.error(
            "Unable to resolve the selected acquisition operation."
        )
        return

    acquisition_manager = (
        DataAcquisitionManager()
    )

    try:
        acquisition_result = (
            acquisition_manager.acquire_daily_ohlcv(
                tickers=requested_tickers,
                requested_start_date=(
                    requested_start_date
                ),
                requested_end_date=(
                    requested_end_date
                ),
            )
        )
    except Exception as exc:
        st.error(
            "Unable to acquire canonical market data: "
            f"{exc}"
        )
        return

    acquisition_context = (
        _build_data_management_acquisition_context(
            acquisition_result
        )
    )

    acquisition_context[
        "workflow"
    ] = "Acquire Market Data"

    acquisition_context[
        "ui_operation"
    ] = selected_operation

    st.session_state[
        _DATA_MANAGEMENT_ACQUISITION_CONTEXT_KEY
    ] = acquisition_context

    if not acquisition_result.has_effective_scope:
        _render_data_management_acquisition_context(
            acquisition_context
        )
        return

    mutation_manager = DataMutationManager()

    try:
        if (
            backend_operation
            == "Repair Duplicate Stored Keys"
        ):
            duplicate_repair_dates = [
                str(
                    duplicate_key.get(
                        "date",
                        "",
                    )
                ).strip()
                for duplicate_key
                in duplicate_stored_keys
                if str(
                    duplicate_key.get(
                        "date",
                        "",
                    )
                ).strip()
            ]

            plan = (
                mutation_manager.build_duplicate_repair_plan(
                    operation=backend_operation,
                    source=acquisition_result.source,
                    ticker=requested_tickers[0],
                    duplicate_dates=(
                        duplicate_repair_dates
                    ),
                    candidates=(
                        acquisition_result.candidates
                    ),
                )
            )
        else:
            plan = mutation_manager.build_plan(
                operation=backend_operation,
                source=acquisition_result.source,
                candidates=(
                    acquisition_result.candidates
                ),
                requested_tickers=(
                    acquisition_result.requested_tickers
                ),
                requested_start_date=(
                    acquisition_result.effective_start_date
                ),
                requested_end_date=(
                    acquisition_result.effective_end_date
                ),
            )
    except Exception as exc:
        st.error(
            "Unable to build Database Change Preview: "
            f"{exc}"
        )
        return

    _set_data_management_mutation_plan(
        plan
    )

    st.session_state.pop(
        _DATA_MANAGEMENT_MAINTENANCE_REQUEST_KEY,
        None,
    )

    st.rerun()


def _sync_data_management_replace_range_end_date() -> None:
    """
    Reset Replace-a-Date-Range End Date to the newly selected Start Date.

    This is UI session state only. The user may subsequently extend End Date
    before building the reconciliation Preview.
    """
    start_key = (
        "data_management_replace_"
        "range_start_date"
    )
    end_key = (
        "data_management_replace_"
        "range_end_date"
    )

    selected_start_date = (
        st.session_state.get(
            start_key
        )
    )

    if selected_start_date is not None:
        st.session_state[
            end_key
        ] = selected_start_date


def _render_data_management_reconciliation_controls(
    *,
    inventory: list[Dict[str, Any]],
    latest_expected_stored_session: Any,
) -> None:
    """
    Render explicit historical yFinance reconciliation workflows.

    User-facing operations:
    - Replace a Date Range
        One or more tickers share one explicit requested date range.
        Backend MutationPlan operation: Replace Range.

    - Refresh Existing Coverage
        One stored ticker uses its existing First Date through Last Date.
        Backend MutationPlan operation: Refresh Existing Coverage.

    Acquisition remains read-only. This helper builds and stores one exact
    MutationPlan; existing Preview / Approve / Apply controls own mutation.
    """
    active_plan = st.session_state.get(
        _DATA_MANAGEMENT_MUTATION_PLAN_KEY
    )

    acquisition_context = st.session_state.get(
        _DATA_MANAGEMENT_ACQUISITION_CONTEXT_KEY
    )

    if active_plan is not None:
        context_workflow = (
            acquisition_context.get(
                "workflow"
            )
            if isinstance(
                acquisition_context,
                dict,
            )
            else None
        )

        if context_workflow == "Historical Data Reconciliation":
            st.markdown("---")
            st.subheader(
                "Historical Data Reconciliation"
            )
            st.info(
                "A reconciliation Preview is active. Review and approve it, "
                "apply the approved changes, or Cancel Preview before "
                "starting another reconciliation request."
            )

            _render_data_management_acquisition_context(
                acquisition_context
            )

        return

    st.markdown("---")
    st.subheader(
        "Historical Data Reconciliation"
    )

    st.caption(
        "Compare fresh canonical yFinance history with authoritative stored "
        "OHLCV before replacing anything. Nothing is changed until the exact "
        "preview is approved and applied."
    )

    operation_labels = [
        "Refresh Existing Coverage",
        "Replace a Date Range",
    ]

    selected_operation = st.radio(
        "Reconciliation Operation",
        options=operation_labels,
        horizontal=True,
        key="data_management_reconciliation_operation",
        help=(
            "Refresh Existing Coverage checks one stored ticker across its "
            "entire current First Date through Last Date. Replace a Date "
            "Range uses one explicit shared date range for one or more "
            "tickers."
        ),
    )

    try:
        default_end_date = pd.Timestamp(
            latest_expected_stored_session
        ).date()
    except Exception:
        default_end_date = date.today()

    requested_tickers: list[str] = []
    requested_start_date: Optional[date] = None
    requested_end_date: Optional[date] = None
    backend_operation: Optional[str] = None
    preview_clicked = False

    if selected_operation == "Replace a Date Range":
        backend_operation = "Replace Range"

        start_date_key = (
            "data_management_replace_"
            "range_start_date"
        )
        end_date_key = (
            "data_management_replace_"
            "range_end_date"
        )

        if start_date_key not in st.session_state:
            st.session_state[
                start_date_key
            ] = default_end_date

        if end_date_key not in st.session_state:
            st.session_state[
                end_date_key
            ] = st.session_state[
                start_date_key
            ]

        ticker_input = st.text_input(
            "Ticker(s)",
            value="",
            key=(
                "data_management_replace_"
                "range_tickers"
            ),
            help=(
                "Enter one or more ticker symbols separated by commas "
                "or spaces. Every ticker in this request uses the same "
                "Start Date and End Date."
            ),
        )

        date_columns = st.columns(2)

        with date_columns[0]:
            range_start_date = st.date_input(
                "Start Date",
                key=start_date_key,
                on_change=(
                    _sync_data_management_replace_range_end_date
                ),
            )

        with date_columns[1]:
            range_end_date = st.date_input(
                "End Date",
                key=end_date_key,
            )

        preview_clicked = st.button(
            "Preview Changes",
            key=(
                "data_management_replace_"
                "range_preview"
            ),
            type="primary",
            use_container_width=True,
            help=(
                "Fetch fresh canonical yFinance history for this "
                "shared ticker/date scope and compare it with stored "
                "OHLCV. Nothing is replaced by this preview."
            ),
        )

        if preview_clicked:
            requested_tickers = [
                ticker
                for ticker in (
                    str(ticker_input)
                    .replace(",", " ")
                    .split()
                )
                if ticker
            ]
            requested_start_date = (
                range_start_date
            )
            requested_end_date = (
                range_end_date
            )

    else:
        backend_operation = (
            "Refresh Existing Coverage"
        )

        inventory_by_ticker = {
            str(
                row.get(
                    "ticker",
                    "",
                )
            ).strip().upper(): row
            for row in inventory
            if str(
                row.get(
                    "ticker",
                    "",
                )
            ).strip()
        }

        stored_tickers = sorted(
            inventory_by_ticker
        )

        if not stored_tickers:
            st.warning(
                "No stored tickers are available for historical "
                "reconciliation."
            )
            return

        selected_ticker = st.selectbox(
            "Stored Ticker",
            options=stored_tickers,
            key=(
                "data_management_reconcile_"
                "stored_ticker"
            ),
            help=(
                "Choose one ticker already stored in daily_prices. "
                "Its complete current First Date through Last Date "
                "will be reconciled."
            ),
        )

        selected_inventory = (
            inventory_by_ticker[
                selected_ticker
            ]
        )

        coverage_columns = st.columns(3)

        coverage_columns[0].metric(
            "Stored Records",
            f"{int(selected_inventory.get('records', 0) or 0):,}",
        )
        coverage_columns[1].metric(
            "First Stored Date",
            selected_inventory.get(
                "first_date"
            ) or "—",
        )
        coverage_columns[2].metric(
            "Last Stored Date",
            selected_inventory.get(
                "last_date"
            ) or "—",
        )

        st.caption(
            "This operation automatically compares fresh canonical "
            "yFinance history across the ticker's entire currently stored "
            "date range. The date boundaries are not manually editable."
        )

        preview_clicked = st.button(
            "Preview Changes",
            key=(
                "data_management_reconcile_"
                "stored_history_preview"
            ),
            type="primary",
            use_container_width=True,
            help=(
                "Fetch fresh canonical yFinance history from the ticker's "
                "First Stored Date through Last Stored Date and compare it "
                "with the authoritative database. Nothing is replaced by "
                "this preview."
            ),
        )

        if preview_clicked:
            requested_tickers = [
                selected_ticker
            ]

            try:
                requested_start_date = (
                    date.fromisoformat(
                        str(
                            selected_inventory[
                                "first_date"
                            ]
                        )
                    )
                )
                requested_end_date = (
                    date.fromisoformat(
                        str(
                            selected_inventory[
                                "last_date"
                            ]
                        )
                    )
                )
            except Exception as exc:
                st.error(
                    "Unable to resolve the stored coverage range for "
                    f"{selected_ticker}: {exc}"
                )
                return

    if not preview_clicked:
        return

    if not requested_tickers:
        st.error(
            "Enter at least one ticker before previewing changes."
        )
        return

    if (
        requested_start_date is None
        or requested_end_date is None
    ):
        st.error(
            "A valid Start Date and End Date are required before "
            "previewing changes."
        )
        return

    acquisition_manager = (
        DataAcquisitionManager()
    )

    try:
        acquisition_result = (
            acquisition_manager.acquire_daily_ohlcv(
                tickers=requested_tickers,
                requested_start_date=(
                    requested_start_date
                ),
                requested_end_date=(
                    requested_end_date
                ),
            )
        )
    except Exception as exc:
        st.error(
            "Unable to acquire canonical market data for reconciliation: "
            f"{exc}"
        )
        return

    acquisition_context = (
        _build_data_management_acquisition_context(
            acquisition_result
        )
    )

    acquisition_context[
        "workflow"
    ] = "Historical Data Reconciliation"

    acquisition_context[
        "ui_operation"
    ] = selected_operation

    st.session_state[
        _DATA_MANAGEMENT_ACQUISITION_CONTEXT_KEY
    ] = acquisition_context

    if not acquisition_result.has_effective_scope:
        _render_data_management_acquisition_context(
            acquisition_context
        )
        return

    mutation_manager = (
        DataMutationManager()
    )

    try:
        plan = mutation_manager.build_plan(
            operation=backend_operation,
            source=acquisition_result.source,
            candidates=(
                acquisition_result.candidates
            ),
            requested_tickers=(
                acquisition_result.requested_tickers
            ),
            requested_start_date=(
                acquisition_result.effective_start_date
            ),
            requested_end_date=(
                acquisition_result.effective_end_date
            ),
        )
    except Exception as exc:
        st.error(
            "Unable to build reconciliation Preview: "
            f"{exc}"
        )
        return

    _set_data_management_mutation_plan(
        plan
    )

    st.rerun()


def _render_data_management_manual_entry_controls(
    *,
    latest_expected_stored_session: Any,
) -> None:
    """
    Render one-record Manual Entry controls.

    Manual Entry supplies one candidate observation directly to the existing
    DataMutationManager planning boundary. It does not acquire yFinance data,
    write SQLite directly, or bypass Preview / Approve / Apply.

    A session-only draft context preserves the administrator's entered values
    so an active Manual Entry Preview can be discarded for editing without
    requiring the complete observation to be re-entered.
    """
    active_plan = st.session_state.get(
        _DATA_MANAGEMENT_MUTATION_PLAN_KEY
    )

    manual_context = st.session_state.get(
        _DATA_MANAGEMENT_MANUAL_ENTRY_CONTEXT_KEY
    )

    if not isinstance(
        manual_context,
        dict,
    ):
        manual_context = {}

    if active_plan is not None:
        if (
            isinstance(
                active_plan,
                MutationPlan,
            )
            and active_plan.operation
            in {
                "Manual Add",
                "Manual Replace",
            }
        ):
            st.markdown("---")
            st.subheader("Manual Entry")
            st.info(
                "A Manual Entry Preview is active. Review the exact values "
                "and database action below, then use the Preview controls to "
                "approve, apply, edit, or cancel this manual observation."
            )

        return

    st.markdown("---")
    st.subheader("Manual Entry")

    st.caption(
        "Enter one complete daily OHLCV observation and preview the exact "
        "database action before anything is saved. Manual Add preserves an "
        "existing ticker/date; Manual Replace explicitly permits replacement "
        "when stored values differ."
    )

    try:
        default_manual_date = pd.Timestamp(
            latest_expected_stored_session
        ).date()
    except Exception:
        default_manual_date = date.today()

    stored_operation = str(
        manual_context.get(
            "ui_operation",
            "Add a Record",
        )
    )

    operation_labels = [
        "Add a Record",
        "Replace a Record",
    ]

    if stored_operation not in operation_labels:
        stored_operation = "Add a Record"

    try:
        stored_manual_date = pd.Timestamp(
            manual_context.get(
                "date",
                default_manual_date,
            )
        ).date()
    except Exception:
        stored_manual_date = default_manual_date

    with st.form(
        "data_management_manual_entry_form"
    ):
        selected_operation = st.radio(
            "Manual Entry Operation",
            options=operation_labels,
            index=operation_labels.index(
                stored_operation
            ),
            horizontal=True,
            help=(
                "Add a Record preserves an existing ticker/date if one is "
                "already stored. Replace a Record explicitly permits replacing "
                "an existing ticker/date when the entered OHLCV values differ."
            ),
        )

        identity_columns = st.columns(2)

        with identity_columns[0]:
            ticker_input = st.text_input(
                "Ticker",
                value=str(
                    manual_context.get(
                        "ticker",
                        "",
                    )
                ),
                help=(
                    "Enter one ticker symbol. Canonical ticker normalization "
                    "is performed by the Data Management mutation layer."
                ),
            )

        with identity_columns[1]:
            manual_date = st.date_input(
                "Date",
                value=stored_manual_date,
                help=(
                    "The observation date. Dates later than the Latest "
                    "Expected Stored Session are rejected by canonical "
                    "Data Management validation."
                ),
            )

        price_columns_1 = st.columns(3)

        with price_columns_1[0]:
            manual_open = st.number_input(
                "Open",
                value=float(
                    manual_context.get(
                        "open",
                        0.0,
                    )
                ),
                step=0.001,
                format="%.3f",
            )

        with price_columns_1[1]:
            manual_high = st.number_input(
                "High",
                value=float(
                    manual_context.get(
                        "high",
                        0.0,
                    )
                ),
                step=0.001,
                format="%.3f",
            )

        with price_columns_1[2]:
            manual_low = st.number_input(
                "Low",
                value=float(
                    manual_context.get(
                        "low",
                        0.0,
                    )
                ),
                step=0.001,
                format="%.3f",
            )

        price_columns_2 = st.columns(3)

        with price_columns_2[0]:
            manual_close = st.number_input(
                "Close",
                value=float(
                    manual_context.get(
                        "close",
                        0.0,
                    )
                ),
                step=0.001,
                format="%.3f",
            )

        with price_columns_2[1]:
            manual_adj_close = st.number_input(
                "Adj Close",
                value=float(
                    manual_context.get(
                        "adj_close",
                        0.0,
                    )
                ),
                step=0.001,
                format="%.3f",
                help=(
                    "Adjusted Close is required. Manual Entry does not "
                    "silently substitute Close for Adj Close."
                ),
            )

        with price_columns_2[2]:
            manual_volume = st.number_input(
                "Volume",
                value=int(
                    manual_context.get(
                        "volume",
                        0,
                    )
                ),
                step=1,
                help=(
                    "Enter whole-share daily volume. Canonical validation "
                    "owns final eligibility."
                ),
            )

        preview_clicked = st.form_submit_button(
            "Preview Changes",
            type="primary",
            use_container_width=True,
            help=(
                "Compare this manually entered observation with the "
                "authoritative database. Nothing is saved by this preview."
            ),
        )

    if not preview_clicked:
        return

    if not str(
        ticker_input
    ).strip():
        st.error(
            "Enter a ticker before previewing the manual observation."
        )
        return

    operation_map = {
        "Add a Record": "Manual Add",
        "Replace a Record": "Manual Replace",
    }

    backend_operation = operation_map[
        selected_operation
    ]

    manual_context = {
        "ui_operation": selected_operation,
        "backend_operation": backend_operation,
        "ticker": ticker_input,
        "date": manual_date,
        "open": manual_open,
        "high": manual_high,
        "low": manual_low,
        "close": manual_close,
        "adj_close": manual_adj_close,
        "volume": manual_volume,
    }

    st.session_state[
        _DATA_MANAGEMENT_MANUAL_ENTRY_CONTEXT_KEY
    ] = manual_context

    candidate = {
        "Ticker": ticker_input,
        "Date": manual_date,
        "Open": manual_open,
        "High": manual_high,
        "Low": manual_low,
        "Close": manual_close,
        "Adj Close": manual_adj_close,
        "Volume": manual_volume,
    }

    mutation_manager = DataMutationManager()

    try:
        plan = mutation_manager.build_plan(
            operation=backend_operation,
            source="Manual Entry",
            candidates=[
                candidate
            ],
        )
    except Exception as exc:
        st.error(
            "Unable to build Manual Entry Preview: "
            f"{exc}"
        )
        return

    _set_data_management_mutation_plan(
        plan
    )

    st.rerun()


def _render_data_management_deletion_controls(
    *,
    inventory: list[Dict[str, Any]],
) -> None:
    """
    Render explicit Delete Range / Delete Ticker controls.

    Deletion operates only on stored daily_prices rows and always enters the
    existing Preview / Approve / Apply mutation lifecycle. It does not alter
    configured universe or bucket membership.
    """
    active_plan = st.session_state.get(
        _DATA_MANAGEMENT_MUTATION_PLAN_KEY
    )

    if active_plan is not None:
        if (
            isinstance(
                active_plan,
                MutationPlan,
            )
            and active_plan.operation
            in {
                "Delete Range",
                "Delete Ticker",
            }
        ):
            st.markdown("---")
            st.subheader("Data Deletion")
            st.info(
                "A deletion Preview is active. Review the exact deletion "
                "scope below, then approve and apply it, or Cancel Preview "
                "before starting another deletion request."
            )

        return

    st.markdown("---")
    st.subheader("Data Deletion")

    st.caption(
        "Explicitly remove stored OHLCV from daily_prices. Deletion never "
        "occurs because a source omitted a row, and deleting a ticker does "
        "not remove it from configured Custom, Sector, or Country membership."
    )

    if not inventory:
        st.info(
            "No stored tickers are available for deletion."
        )
        return

    inventory_by_ticker = {
        str(row["ticker"]).strip().upper(): row
        for row in inventory
    }

    stored_tickers = sorted(
        inventory_by_ticker
    )

    selected_operation = st.radio(
        "Deletion Operation",
        options=[
            "Delete a Date Range",
            "Delete a Ticker",
        ],
        horizontal=True,
        key="data_management_deletion_operation",
        help=(
            "Delete a Date Range removes stored rows for one ticker inside "
            "an inclusive date interval. Delete a Ticker removes every "
            "stored daily_prices row for one ticker."
        ),
    )

    selected_ticker = st.selectbox(
        "Stored Ticker",
        options=stored_tickers,
        key="data_management_deletion_ticker",
        help=(
            "Only tickers currently stored in daily_prices are available."
        ),
    )

    selected_inventory = inventory_by_ticker[
        selected_ticker
    ]

    record_count = int(
        selected_inventory.get(
            "records",
            0,
        ) or 0
    )

    first_date_text = str(
        selected_inventory.get(
            "first_date",
            "",
        )
    )
    last_date_text = str(
        selected_inventory.get(
            "last_date",
            "",
        )
    )

    stored_columns = st.columns(3)

    stored_columns[0].metric(
        "Stored Records",
        f"{record_count:,}",
    )
    stored_columns[1].metric(
        "First Stored Date",
        first_date_text or "—",
    )
    stored_columns[2].metric(
        "Last Stored Date",
        last_date_text or "—",
    )

    buckets = selected_inventory.get(
        "buckets",
        [],
    )

    bucket_text = (
        ", ".join(
            str(bucket)
            for bucket in buckets
        )
        if buckets
        else "Unassigned"
    )

    st.caption(
        f"Configured universe membership: {bucket_text}. "
        "Deletion affects daily_prices only; this membership is not changed."
    )

    backend_operation: str
    requested_start_date: Optional[date]
    requested_end_date: Optional[date]

    if selected_operation == "Delete a Date Range":
        backend_operation = "Delete Range"

        try:
            default_start_date = pd.Timestamp(
                first_date_text
            ).date()
            default_end_date = pd.Timestamp(
                last_date_text
            ).date()
        except Exception:
            st.error(
                "Stored ticker inventory does not contain a usable "
                "First Date / Last Date range."
            )
            return

        date_columns = st.columns(2)

        with date_columns[0]:
            requested_start_date = st.date_input(
                "Start Date",
                value=default_start_date,
                key=(
                    "data_management_delete_"
                    "range_start_date"
                ),
                help=(
                    "Inclusive first calendar date of the deletion scope."
                ),
            )

        with date_columns[1]:
            requested_end_date = st.date_input(
                "End Date",
                value=default_end_date,
                key=(
                    "data_management_delete_"
                    "range_end_date"
                ),
                help=(
                    "Inclusive last calendar date of the deletion scope."
                ),
            )

        st.warning(
            "This operation will permanently delete every stored "
            f"{selected_ticker} OHLCV row inside the selected inclusive "
            "date range after Preview approval and Apply."
        )
    else:
        backend_operation = "Delete Ticker"
        requested_start_date = None
        requested_end_date = None

        st.warning(
            f"This operation will permanently delete all {record_count:,} "
            f"stored {selected_ticker} OHLCV record(s) from daily_prices "
            "after Preview approval and Apply. Configured universe "
            "membership will remain unchanged."
        )

    preview_clicked = st.button(
        "Preview Deletion",
        key="data_management_deletion_preview",
        type="primary",
        use_container_width=True,
        help=(
            "Build an exact read-only deletion Preview. This button does "
            "not delete anything."
        ),
    )

    if not preview_clicked:
        return

    mutation_manager = DataMutationManager()

    try:
        plan = mutation_manager.build_deletion_plan(
            operation=backend_operation,
            source="Data Management Deletion",
            ticker=selected_ticker,
            requested_start_date=requested_start_date,
            requested_end_date=requested_end_date,
        )
    except Exception as exc:
        st.error(
            "Unable to build deletion Preview: "
            f"{exc}"
        )
        return

    _set_data_management_mutation_plan(
        plan
    )

    st.rerun()


def _set_data_management_mutation_plan(
    plan: MutationPlan,
) -> None:
    """
    Store one exact materialized MutationPlan as the active Preview.

    A new Preview invalidates any confirmation, prior Commit result, or
    prior Commit error belonging to an older Preview.
    """
    if not isinstance(plan, MutationPlan):
        raise TypeError(
            "plan must be a MutationPlan produced by "
            "DataMutationManager.build_plan()."
        )

    st.session_state[
        _DATA_MANAGEMENT_MUTATION_PLAN_KEY
    ] = plan

    st.session_state.pop(
        _DATA_MANAGEMENT_MUTATION_CONFIRMED_FINGERPRINT_KEY,
        None,
    )
    st.session_state.pop(
        _DATA_MANAGEMENT_MUTATION_RESULT_KEY,
        None,
    )
    st.session_state.pop(
        _DATA_MANAGEMENT_MUTATION_ERROR_KEY,
        None,
    )


def _discard_data_management_mutation_plan(
    *,
    preserve_manual_entry_context: bool = False,
) -> None:
    """
    Discard the active mutation Preview and its confirmation state.

    Manual Entry may explicitly preserve its session-only draft while editing
    the values that produced a Preview. Ordinary Cancel discards that draft.
    """
    st.session_state.pop(
        _DATA_MANAGEMENT_MUTATION_PLAN_KEY,
        None,
    )
    st.session_state.pop(
        _DATA_MANAGEMENT_MUTATION_CONFIRMED_FINGERPRINT_KEY,
        None,
    )
    st.session_state.pop(
        _DATA_MANAGEMENT_MUTATION_ERROR_KEY,
        None,
    )
    st.session_state.pop(
        _DATA_MANAGEMENT_ACQUISITION_CONTEXT_KEY,
        None,
    )
    st.session_state.pop(
        _DATA_MANAGEMENT_MAINTENANCE_REQUEST_KEY,
        None,
    )

    if not preserve_manual_entry_context:
        st.session_state.pop(
            _DATA_MANAGEMENT_MANUAL_ENTRY_CONTEXT_KEY,
            None,
        )


def _render_data_management_source_data_preview(
    plan: MutationPlan,
) -> None:
    """
    Render bounded source-data evidence from the exact materialized Preview.

    The displayed/exported rows come only from MutationPlan observations.
    This helper does not refetch source data, read SQLite, or reinterpret
    mutation actions.
    """
    if not isinstance(
        plan,
        MutationPlan,
    ):
        raise TypeError(
            "plan must be a MutationPlan produced by "
            "DataMutationManager.build_plan()."
        )

    source_rows = [
        observation.candidate.to_dict()
        for observation in plan.observations
    ]

    if not source_rows:
        return

    source_rows.sort(
        key=lambda row: (
            str(row.get("Ticker", "")),
            str(row.get("Date", "")),
        )
    )

    source_columns = [
        "Ticker",
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
    ]

    source_df = pd.DataFrame(
        source_rows,
        columns=source_columns,
    )

    with st.expander(
        "Incoming Source Data",
        expanded=False,
    ):
        st.caption(
            "Inspect the canonical source records contained in this exact "
            "Database Change Preview. These are the eligible source rows "
            "being evaluated for the actions shown below. Rows Not Eligible "
            "are listed separately and are not included here."
        )

        source_tickers = list(
            dict.fromkeys(
                source_df["Ticker"].tolist()
            )
        )

        for ticker in source_tickers:
            ticker_df = (
                source_df.loc[
                    source_df["Ticker"] == ticker,
                    source_columns,
                ]
                .sort_values("Date")
                .reset_index(drop=True)
            )

            ticker_count = len(
                ticker_df
            )

            st.markdown(
                f"**{ticker} — "
                f"{ticker_count:,} eligible source record(s)**"
            )

            if ticker_count <= 6:
                display_df = ticker_df
                st.caption(
                    "Showing all eligible source records "
                    "for this ticker."
                )
            else:
                display_df = pd.concat(
                    [
                        ticker_df.head(3),
                        ticker_df.tail(3),
                    ],
                    ignore_index=True,
                )
                st.caption(
                    "Showing the first 3 and last 3 eligible source "
                    "records for this ticker. Download the CSV below "
                    "to inspect the complete source dataset."
                )

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )

        requested_start = (
            plan.requested_start_date.isoformat()
            if plan.requested_start_date is not None
            else "start"
        )
        requested_end = (
            plan.requested_end_date.isoformat()
            if plan.requested_end_date is not None
            else "end"
        )

        csv_bytes = source_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download All Source Records CSV",
            data=csv_bytes,
            file_name=(
                "data_management_source_"
                f"{requested_start}_to_{requested_end}.csv"
            ),
            mime="text/csv",
            key=(
                "data_management_source_preview_csv_"
                f"{plan.plan_fingerprint[:12]}"
            ),
            help=(
                "Download every eligible canonical source record contained "
                "in this exact Database Change Preview, not just the rows "
                "shown in the first/last sample."
            ),
        )


def _render_data_management_stored_vs_proposed_preview(
    plan: MutationPlan,
) -> None:
    """
    Render exact stored-versus-proposed values for replacement candidates.

    Every displayed/exported value comes from the already-materialized
    MutationPlan. This helper does not refetch source data, reread SQLite,
    rebuild the plan, or reinterpret mutation actions.
    """
    if not isinstance(
        plan,
        MutationPlan,
    ):
        raise TypeError(
            "plan must be a MutationPlan produced by "
            "DataMutationManager.build_plan()."
        )

    replacement_observations = [
        observation
        for observation in plan.observations
        if (
            str(
                observation.planned_action
            ).strip().lower()
            == "replacement_candidate"
            and observation.existing is not None
        )
    ]

    if not replacement_observations:
        return

    comparison_rows = []

    for observation in replacement_observations:
        stored = observation.existing.to_dict()
        proposed = observation.candidate.to_dict()

        comparison_rows.append(
            {
                "Ticker": observation.candidate.ticker,
                "Date": observation.candidate.date.isoformat(),
                "Stored Open": stored["Open"],
                "Proposed Open": proposed["Open"],
                "Stored High": stored["High"],
                "Proposed High": proposed["High"],
                "Stored Low": stored["Low"],
                "Proposed Low": proposed["Low"],
                "Stored Close": stored["Close"],
                "Proposed Close": proposed["Close"],
                "Stored Adj Close": stored["Adj Close"],
                "Proposed Adj Close": proposed["Adj Close"],
                "Stored Volume": stored["Volume"],
                "Proposed Volume": proposed["Volume"],
                "Fields That Differ": (
                    ", ".join(
                        observation.differing_fields
                    )
                    if observation.differing_fields
                    else "—"
                ),
            }
        )

    comparison_rows.sort(
        key=lambda row: (
            str(row.get("Ticker", "")),
            str(row.get("Date", "")),
        )
    )

    comparison_columns = [
        "Ticker",
        "Date",
        "Stored Open",
        "Proposed Open",
        "Stored High",
        "Proposed High",
        "Stored Low",
        "Proposed Low",
        "Stored Close",
        "Proposed Close",
        "Stored Adj Close",
        "Proposed Adj Close",
        "Stored Volume",
        "Proposed Volume",
        "Fields That Differ",
    ]

    comparison_df = pd.DataFrame(
        comparison_rows,
        columns=comparison_columns,
    )

    st.markdown(
        "#### Preview Changes — Stored vs Proposed"
    )
    st.caption(
        "These are the existing database records that this exact Preview "
        "would replace. Stored values are what is currently authoritative; "
        "Proposed values are the canonical source values that would replace "
        "them only if this Preview is approved and applied."
    )

    comparison_tickers = list(
        dict.fromkeys(
            comparison_df["Ticker"].tolist()
        )
    )

    for ticker in comparison_tickers:
        ticker_df = (
            comparison_df.loc[
                comparison_df["Ticker"] == ticker,
                comparison_columns,
            ]
            .sort_values("Date")
            .reset_index(drop=True)
        )

        ticker_count = len(
            ticker_df
        )

        st.markdown(
            f"**{ticker} — "
            f"{ticker_count:,} stored record(s) would be replaced**"
        )

        if ticker_count <= 6:
            display_df = ticker_df

            st.caption(
                "Showing all proposed replacements for this ticker."
            )
        else:
            display_df = pd.concat(
                [
                    ticker_df.head(3),
                    ticker_df.tail(3),
                ],
                ignore_index=True,
            )

            st.caption(
                "Showing the first 3 and last 3 proposed replacements "
                "for this ticker. Download the full comparison CSV below "
                "to inspect every proposed replacement."
            )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

    requested_start = (
        plan.requested_start_date.isoformat()
        if plan.requested_start_date is not None
        else "start"
    )

    requested_end = (
        plan.requested_end_date.isoformat()
        if plan.requested_end_date is not None
        else "end"
    )

    comparison_csv_bytes = (
        comparison_df.to_csv(
            index=False
        ).encode("utf-8")
    )

    st.download_button(
        "Download Full Comparison CSV",
        data=comparison_csv_bytes,
        file_name=(
            "data_management_stored_vs_proposed_"
            f"{requested_start}_to_{requested_end}.csv"
        ),
        mime="text/csv",
        key=(
            "data_management_stored_vs_proposed_csv_"
            f"{plan.plan_fingerprint[:12]}"
        ),
        help=(
            "Download every stored-versus-proposed replacement contained "
            "in this exact Preview, including records not shown in the "
            "first/last sample."
        ),
    )


def _render_data_management_deletion_preview(
    plan: MutationPlan,
) -> None:
    """
    Render bounded evidence for one exact materialized deletion Preview.

    The complete deletion set remains stored in MutationPlan and participates
    in the exact plan fingerprint. The table is intentionally bounded for
    large deletion scopes, while the CSV exposes every affected row.
    """
    if plan.operation not in {
        "Delete Range",
        "Delete Ticker",
    }:
        raise ValueError(
            "Deletion Preview requires a deletion MutationPlan."
        )

    deletion_rows = [
        deletion.record.to_dict()
        for deletion in plan.deletions
    ]

    deletion_rows.sort(
        key=lambda row: (
            str(row.get("Ticker", "")),
            str(row.get("Date", "")),
        )
    )

    deletion_count = len(
        deletion_rows
    )

    st.markdown("---")
    st.subheader("Database Deletion Preview")

    st.caption(
        "Review the exact stored OHLCV scope that will be permanently "
        "removed if this Preview is approved and applied. Nothing has been "
        "deleted yet."
    )

    request_columns = st.columns(4)

    request_columns[0].metric(
        "Operation",
        plan.operation,
    )
    request_columns[1].metric(
        "Ticker",
        (
            plan.requested_tickers[0]
            if plan.requested_tickers
            else "—"
        ),
    )
    request_columns[2].metric(
        "Rows to Delete",
        f"{deletion_count:,}",
    )
    request_columns[3].metric(
        "Source",
        plan.source,
    )

    if deletion_rows:
        first_affected_date = str(
            deletion_rows[0]["Date"]
        )
        last_affected_date = str(
            deletion_rows[-1]["Date"]
        )
    else:
        first_affected_date = "—"
        last_affected_date = "—"

    scope_columns = st.columns(4)

    scope_columns[0].metric(
        "Requested Start Date",
        (
            plan.requested_start_date.isoformat()
            if plan.requested_start_date is not None
            else "All Stored Dates"
        ),
    )
    scope_columns[1].metric(
        "Requested End Date",
        (
            plan.requested_end_date.isoformat()
            if plan.requested_end_date is not None
            else "All Stored Dates"
        ),
    )
    scope_columns[2].metric(
        "First Affected Date",
        first_affected_date,
    )
    scope_columns[3].metric(
        "Last Affected Date",
        last_affected_date,
    )

    st.warning(
        "Applying this approved Preview permanently removes these rows from "
        "daily_prices. It does not remove the ticker from Custom, Sector, "
        "Country, or other configured universe membership, and it does not "
        "delete prior audit history."
    )

    if not deletion_rows:
        st.info(
            "No stored OHLCV rows match this deletion scope. There is "
            "nothing to delete, so this Preview cannot be applied."
        )
        return

    deletion_columns = [
        "Ticker",
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
    ]

    deletion_df = pd.DataFrame(
        deletion_rows,
        columns=deletion_columns,
    )

    st.markdown("#### Affected Stored Records")

    if deletion_count <= 20:
        st.caption(
            "This deletion affects 20 or fewer records, so every affected "
            "stored row is shown."
        )

        display_df = deletion_df
    else:
        st.caption(
            "This deletion affects more than 20 records. The table shows "
            "the first 3 and last 3 affected rows; the complete deletion "
            "set is available in the CSV below."
        )

        first_rows = deletion_df.head(
            3
        ).copy()
        last_rows = deletion_df.tail(
            3
        ).copy()

        first_rows.insert(
            0,
            "Preview Position",
            "First 3",
        )
        last_rows.insert(
            0,
            "Preview Position",
            "Last 3",
        )

        display_df = pd.concat(
            [
                first_rows,
                last_rows,
            ],
            ignore_index=True,
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    full_csv = deletion_df.to_csv(
        index=False
    ).encode(
        "utf-8"
    )

    st.download_button(
        "Download Full Deletion Preview CSV",
        data=full_csv,
        file_name=(
            "data_management_deletion_preview_"
            f"{plan.plan_fingerprint[:12]}.csv"
        ),
        mime="text/csv",
        key=(
            "data_management_deletion_preview_csv_"
            f"{plan.plan_fingerprint[:12]}"
        ),
        help=(
            "Download every stored OHLCV row contained in this exact "
            "deletion Preview, including rows not shown in the bounded table."
        ),
    )

    st.caption(
        "Approval is bound to the complete materialized deletion set and "
        "plan fingerprint, not only to the rows displayed in this table."
    )

def _render_data_management_duplicate_repair_preview(
    plan: MutationPlan,
) -> None:
    """
    Render one exact materialized Duplicate Stored Key repair Preview.

    All stored and proposed values come from MutationPlan.duplicate_repairs.
    This helper does not refetch source data or reread SQLite.
    """
    if not isinstance(
        plan,
        MutationPlan,
    ):
        raise TypeError(
            "plan must be a MutationPlan produced by "
            "DataMutationManager.build_duplicate_repair_plan()."
        )

    repair_count = len(
        plan.duplicate_repairs
    )
    physical_rows_to_remove = sum(
        repair.physical_row_count
        for repair
        in plan.duplicate_repairs
    )
    canonical_rows_to_insert = (
        repair_count
    )
    net_rows_removed = (
        physical_rows_to_remove
        - canonical_rows_to_insert
    )

    st.markdown("---")
    st.subheader(
        "Database Change Preview"
    )

    st.caption(
        "Review the exact Duplicate Stored Key repair. Nothing is changed by "
        "this Preview. Approval is bound to every physical stored duplicate "
        "row plus the exact canonical replacement observation."
    )

    request_columns = st.columns(
        4
    )

    request_columns[0].metric(
        "Operation",
        plan.operation,
    )
    request_columns[1].metric(
        "Source",
        plan.source,
    )
    request_columns[2].metric(
        "Duplicate Keys to Repair",
        f"{repair_count:,}",
    )
    request_columns[3].metric(
        "Latest Expected Session",
        plan.latest_expected_stored_session.isoformat(),
    )

    requested_start = (
        plan.requested_start_date.isoformat()
        if plan.requested_start_date
        is not None
        else "—"
    )
    requested_end = (
        plan.requested_end_date.isoformat()
        if plan.requested_end_date
        is not None
        else "—"
    )

    st.caption(
        "Acquisition envelope represented by this Preview: "
        f"{requested_start} through {requested_end}. "
        "Only the exact duplicate keys materialized below can be changed."
    )

    summary_columns = st.columns(
        4
    )

    summary_columns[0].metric(
        "Duplicate Keys",
        f"{repair_count:,}",
    )
    summary_columns[1].metric(
        "Stored Physical Rows",
        f"{physical_rows_to_remove:,}",
        help=(
            "Every physical stored row captured for the duplicate keys "
            "in this exact Preview."
        ),
    )
    summary_columns[2].metric(
        "Canonical Rows to Insert",
        f"{canonical_rows_to_insert:,}",
        help=(
            "Exactly one validated canonical source observation will remain "
            "for each successfully repaired logical key."
        ),
    )
    summary_columns[3].metric(
        "Net Excess Rows Removed",
        f"{net_rows_removed:,}",
        help=(
            "Stored physical rows removed minus canonical rows inserted."
        ),
    )

    if plan.duplicate_repairs:
        st.info(
            "**What this preview will do:** "
            f"{repair_count:,} duplicate logical key(s) contain "
            f"{physical_rows_to_remove:,} stored physical row(s). "
            "If approved and applied, Data Management will atomically remove "
            "all stored physical copies for each exact key and insert exactly "
            f"{canonical_rows_to_insert:,} validated canonical source row(s), "
            f"removing {net_rows_removed:,} net excess row(s)."
        )

        st.markdown(
            "#### Duplicate Repair Actions"
        )

        action_rows = []

        for repair in plan.duplicate_repairs:
            action_rows.append(
                {
                    "Ticker": (
                        repair.candidate.ticker
                    ),
                    "Date": (
                        repair.candidate.date.isoformat()
                    ),
                    "Stored Physical Rows": (
                        repair.physical_row_count
                    ),
                    "Canonical Rows After Repair": 1,
                    "What Will Happen": (
                        f"Replace {repair.physical_row_count} stored "
                        "physical rows with 1 canonical row"
                    ),
                }
            )

        st.dataframe(
            pd.DataFrame(
                action_rows
            ),
            use_container_width=True,
            hide_index=True,
        )

        for repair in plan.duplicate_repairs:
            st.markdown(
                f"##### {repair.candidate.ticker} — "
                f"{repair.candidate.date.isoformat()}"
            )

            stored_rows = []

            for row_number, stored_record in enumerate(
                repair.stored_records,
                start=1,
            ):
                stored_values = (
                    stored_record.to_dict()
                )

                stored_rows.append(
                    {
                        "Stored Copy": row_number,
                        "Open": stored_values[
                            "Open"
                        ],
                        "High": stored_values[
                            "High"
                        ],
                        "Low": stored_values[
                            "Low"
                        ],
                        "Close": stored_values[
                            "Close"
                        ],
                        "Adj Close": stored_values[
                            "Adj Close"
                        ],
                        "Volume": stored_values[
                            "Volume"
                        ],
                    }
                )

            st.caption(
                "Physical stored copies captured by this exact Preview:"
            )

            st.dataframe(
                pd.DataFrame(
                    stored_rows
                ),
                use_container_width=True,
                hide_index=True,
            )

            candidate_values = (
                repair.candidate.to_dict()
            )

            st.caption(
                "Canonical source observation that will replace all stored "
                "copies for this logical key:"
            )

            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Open": candidate_values[
                                "Open"
                            ],
                            "High": candidate_values[
                                "High"
                            ],
                            "Low": candidate_values[
                                "Low"
                            ],
                            "Close": candidate_values[
                                "Close"
                            ],
                            "Adj Close": candidate_values[
                                "Adj Close"
                            ],
                            "Volume": candidate_values[
                                "Volume"
                            ],
                        }
                    ]
                ),
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.warning(
            "No valid duplicate repair actions were materialized."
        )

    if plan.validation_warnings:
        st.markdown(
            "#### Warnings"
        )

        warning_rows = [
            {
                "Ticker": warning.ticker
                or "—",
                "Date": warning.date
                or "—",
                "Code": warning.code,
                "Message": warning.message,
            }
            for warning
            in plan.validation_warnings
        ]

        st.dataframe(
            pd.DataFrame(
                warning_rows
            ),
            use_container_width=True,
            hide_index=True,
        )

    if plan.excluded_observations:
        st.markdown(
            "#### Rows Not Eligible"
        )

        excluded_rows = []

        for observation in plan.excluded_observations:
            for issue in observation.issues:
                excluded_rows.append(
                    {
                        "Ticker": (
                            observation.ticker
                            or "—"
                        ),
                        "Date": (
                            observation.date
                            or "—"
                        ),
                        "Code": issue.code,
                        "Reason": (
                            issue.message
                        ),
                    }
                )

        st.dataframe(
            pd.DataFrame(
                excluded_rows
            ),
            use_container_width=True,
            hide_index=True,
        )

    if plan.validation_issues:
        st.markdown(
            "#### Blocking Issues"
        )

        st.caption(
            "These issues prevent this duplicate-repair Preview from being "
            "applied. Build a fresh valid Preview before making database "
            "changes."
        )

        issue_rows = [
            {
                "Ticker": issue.ticker
                or "—",
                "Date": issue.date
                or "—",
                "Code": issue.code,
                "Message": issue.message,
            }
            for issue
            in plan.validation_issues
        ]

        st.dataframe(
            pd.DataFrame(
                issue_rows
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "Preview ID: "
        f"{plan.plan_fingerprint} "
        "— used internally to bind approval to this exact duplicate repair."
    )


def _render_data_management_mutation_preview(
    plan: MutationPlan,
) -> None:
    """Render the exact materialized MutationPlan for administrator review."""
    if not isinstance(plan, MutationPlan):
        raise TypeError(
            "plan must be a MutationPlan produced by "
            "DataMutationManager.build_plan()."
        )

    if plan.operation in {
        "Delete Range",
        "Delete Ticker",
    }:
        _render_data_management_deletion_preview(
            plan
        )
        return

    if (
        plan.operation
        == "Repair Duplicate Stored Keys"
    ):
        _render_data_management_duplicate_repair_preview(
            plan
        )
        return

    summary = plan.summary()

    new_count = int(
        summary.get("new", 0) or 0
    )
    same_count = int(
        summary.get("unchanged", 0) or 0
    )
    different_count = int(
        summary.get("changed", 0) or 0
    )
    insert_count = int(
        summary.get("insert", 0) or 0
    )
    replacement_count = int(
        summary.get(
            "replacement_candidate",
            0,
        ) or 0
    )
    preserve_count = int(
        summary.get(
            "preserve_existing",
            0,
        ) or 0
    )
    no_change_count = int(
        summary.get(
            "no_change",
            0,
        ) or 0
    )
    warning_count = int(
        summary.get(
            "validation_warnings",
            0,
        ) or 0
    )
    excluded_count = int(
        summary.get(
            "excluded_observations",
            0,
        ) or 0
    )
    source_missing_count = int(
        summary.get(
            "source_missing",
            0,
        ) or 0
    )

    source_missing_preserved_count = sum(
        1
        for observation in plan.source_missing
        if (
            str(
                observation.planned_action
            ).strip().lower()
            == "preserve_existing"
            and observation.existing is not None
        )
    )

    source_missing_unresolved_count = sum(
        1
        for observation in plan.source_missing
        if (
            str(
                observation.planned_action
            ).strip().lower()
            == "unresolved"
            and observation.existing is None
        )
    )

    blocking_count = int(
        summary.get(
            "validation_issues",
            0,
        ) or 0
    )
    duplicate_count = int(
        summary.get(
            "duplicate_keys",
            0,
        ) or 0
    )

    compared_count = (
        new_count
        + same_count
        + different_count
    )

    st.markdown("---")
    st.subheader("Database Change Preview")
    st.caption(
        "Review exactly what Data Management would do to the authoritative "
        "OHLCV database. Nothing is saved by this preview. First approve "
        "these exact changes; then use Apply Approved Changes to execute "
        "only the actions shown below. For an Add operation, existing "
        "records are never overwritten; use a replacement operation when "
        "you intend to replace stored values."
    )

    is_manual_entry = (
        str(
            plan.source
        ).strip()
        == "Manual Entry"
    )

    if is_manual_entry:
        request_columns = st.columns(3)

        request_columns[0].metric(
            "Operation",
            plan.operation,
        )
        request_columns[1].metric(
            "Source",
            plan.source,
        )
        request_columns[2].metric(
            "Latest Expected Session",
            plan.latest_expected_stored_session.isoformat(),
        )

        st.caption(
            "Manual Entry evaluates only the explicitly entered observation. "
            "Source Missing inference is not used for this Preview."
        )

    else:
        request_columns = st.columns(4)

        request_columns[0].metric(
            "Operation",
            plan.operation,
        )
        request_columns[1].metric(
            "Source",
            plan.source,
        )
        request_columns[2].metric(
            "Requested Tickers",
            f"{len(plan.requested_tickers):,}",
        )
        request_columns[3].metric(
            "Latest Expected Session",
            plan.latest_expected_stored_session.isoformat(),
        )

        requested_start = (
            plan.requested_start_date.isoformat()
            if plan.requested_start_date is not None
            else "—"
        )
        requested_end = (
            plan.requested_end_date.isoformat()
            if plan.requested_end_date is not None
            else "—"
        )

        st.caption(
            f"Effective database range: {requested_start} through "
            f"{requested_end}"
        )

    if plan.requested_tickers:
        with st.expander(
            "Requested ticker scope",
            expanded=False,
        ):
            st.write(", ".join(plan.requested_tickers))

    consequence_text = (
        f"{compared_count:,} eligible source observations were compared "
        f"with stored data: {new_count:,} new, {same_count:,} the same, "
        f"and {different_count:,} different. "
        f"If applied, {insert_count:,} records will be added, "
        f"{replacement_count:,} existing records will be replaced, "
        f"{preserve_count:,} differing existing records will be kept "
        f"unchanged, and {no_change_count:,} matching records require "
        "no change."
    )

    if excluded_count:
        consequence_text += (
            f" {excluded_count:,} returned source rows are not eligible "
            "and will not be applied."
        )

    if source_missing_count:
        consequence_text += (
            f" {source_missing_count:,} expected sessions were missing "
            "from the current yFinance response. Of those, "
            f"{source_missing_preserved_count:,} stored records will be "
            "kept unchanged despite the yFinance omission and "
            f"{source_missing_unresolved_count:,} sessions remain missing "
            "because neither the current yFinance response nor the database "
            "contains a record. Data Management will not fabricate or "
            "delete observations because yFinance omitted them from this "
            "request."
        )

    if blocking_count or duplicate_count:
        consequence_text += (
            " This preview contains blocking issues and cannot be applied "
            "until a new valid preview is built."
        )

    st.info(
        "**What this preview will do:** "
        + consequence_text
    )

    st.markdown("#### Change Summary")

    summary_columns_1 = st.columns(5)

    summary_columns_1[0].metric(
        "New Records",
        f"{new_count:,}",
        help=(
            "No stored record currently exists for this ticker and date."
        ),
    )
    summary_columns_1[1].metric(
        "Same as Stored",
        f"{same_count:,}",
        help=(
            "The source OHLCV values exactly match the record already "
            "stored for the same ticker and date."
        ),
    )
    summary_columns_1[2].metric(
        "Different from Stored",
        f"{different_count:,}",
        help=(
            "The ticker and date already exist, but one or more stored "
            "OHLCV values differ from the newly acquired source values. "
            "This does not mean the database has already been changed."
        ),
    )
    summary_columns_1[3].metric(
        "Records to Add",
        f"{insert_count:,}",
        help=(
            "New records that will be inserted if this preview is "
            "approved and applied."
        ),
    )
    summary_columns_1[4].metric(
        "Records to Replace",
        f"{replacement_count:,}",
        help=(
            "Existing records explicitly proposed for replacement if "
            "this preview is approved and applied."
        ),
    )

    summary_columns_2 = st.columns(4)

    summary_columns_2[0].metric(
        "Warnings",
        f"{warning_count:,}",
        help=(
            "Items that deserve review but do not, by themselves, block "
            "the database operation."
        ),
    )
    summary_columns_2[1].metric(
        "Rows Not Eligible",
        f"{excluded_count:,}",
        help=(
            "Source rows that were returned but failed required validation. "
            "They are excluded and will not be saved."
        ),
    )
    summary_columns_2[2].metric(
        "Blocking Issues",
        f"{blocking_count:,}",
        help=(
            "Problems that prevent the entire preview from being applied. "
            "A new valid preview must be built before database changes can "
            "be made."
        ),
    )
    summary_columns_2[3].metric(
        "Duplicate Incoming Records",
        f"{duplicate_count:,}",
        help=(
            "The same ticker/date appears more than once in the incoming "
            "source set. Duplicate incoming identities block the preview "
            "because Data Management cannot safely choose between them."
        ),
    )

    if not is_manual_entry:
        summary_columns_3 = st.columns(3)

        summary_columns_3[0].metric(
            "Missing From Current yFinance Response",
            f"{source_missing_count:,}",
            help=(
                "Expected NYSE trading sessions for which the current "
                "yFinance request returned no ticker-date row. This does not "
                "mean yFinance never had the record; it means the row was "
                "absent from the response used to build this Preview."
            ),
        )
        summary_columns_3[1].metric(
            "Stored Records Kept Despite yFinance Omission",
            f"{source_missing_preserved_count:,}",
            help=(
                "yFinance returned no row for these expected ticker-date "
                "sessions, but the database already contains one. The stored "
                "record will be kept unchanged; a missing row in the current "
                "yFinance response does not authorize deletion."
            ),
        )
        summary_columns_3[2].metric(
            "Still Missing After yFinance Check",
            f"{source_missing_unresolved_count:,}",
            help=(
                "Neither the current yFinance response nor the database "
                "contains a record for these expected trading sessions. "
                "Data Management will not fabricate OHLCV values, so these "
                "sessions remain missing."
            ),
        )

    _render_data_management_source_data_preview(
        plan
    )

    _render_data_management_stored_vs_proposed_preview(
        plan
    )

    if plan.observations:
        st.markdown("#### Record Comparison & Actions")
        st.caption(
            "Each row shows how the acquired source observation compares "
            "with the authoritative stored record and what Data Management "
            "would actually do if the preview is applied."
        )

        classification_labels = {
            "new": "New",
            "unchanged": "Same",
            "changed": "Different",
        }

        action_labels = {
            "insert": "Add Record",
            "no_change": "No Change",
            "preserve_existing": "Keep Stored Record",
            "replacement_candidate": "Replace Stored Record",
        }

        observation_rows = []

        for observation in plan.observations:
            classification_key = str(
                observation.classification
            ).strip().lower()

            action_key = str(
                observation.planned_action
            ).strip().lower()

            observation_rows.append(
                {
                    "Ticker": observation.candidate.ticker,
                    "Date": (
                        observation.candidate.date.isoformat()
                    ),
                    "Compared with Stored Data": (
                        classification_labels.get(
                            classification_key,
                            observation.classification,
                        )
                    ),
                    "What Will Happen": (
                        action_labels.get(
                            action_key,
                            observation.planned_action,
                        )
                    ),
                    "Existing Record": (
                        "Yes"
                        if observation.collision
                        else "No"
                    ),
                    "Fields That Differ": (
                        ", ".join(
                            observation.differing_fields
                        )
                        if observation.differing_fields
                        else "—"
                    ),
                }
            )

        comparison_df = pd.DataFrame(
            observation_rows
        )

        filter_row_one = st.columns(
            [1.2, 1.4, 1.0]
        )

        with filter_row_one[0]:
            comparison_filter = st.selectbox(
                "Compared with Stored Data",
                options=[
                    "All",
                    "New",
                    "Same",
                    "Different",
                ],
                index=0,
                key=(
                    "data_management_record_comparison_"
                    "classification_filter"
                ),
            )

        with filter_row_one[1]:
            action_filter = st.selectbox(
                "What Will Happen",
                options=[
                    "All",
                    "Add Record",
                    "No Change",
                    "Keep Stored Record",
                    "Replace Stored Record",
                ],
                index=0,
                key=(
                    "data_management_record_comparison_"
                    "action_filter"
                ),
            )

        with filter_row_one[2]:
            existing_record_filter = st.selectbox(
                "Existing Record",
                options=[
                    "All",
                    "Yes",
                    "No",
                ],
                index=0,
                key=(
                    "data_management_record_comparison_"
                    "existing_record_filter"
                ),
            )

        filter_row_two = st.columns(
            [1.2, 1.8]
        )

        with filter_row_two[0]:
            differing_field_filter = st.selectbox(
                "Fields That Differ",
                options=[
                    "All",
                    "Any Difference",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Adj Close",
                    "Volume",
                ],
                index=0,
                key=(
                    "data_management_record_comparison_"
                    "differing_field_filter"
                ),
            )

        with filter_row_two[1]:
            date_search = st.text_input(
                "Search Date",
                value="",
                key=(
                    "data_management_record_comparison_"
                    "date_search"
                ),
                placeholder="Examples: 2024, 2024-12, 2024-12-18",
                help=(
                    "Filters the ISO Date column using partial text matching. "
                    "For example, 2024-12 shows all December 2024 records."
                ),
            ).strip()

        filtered_comparison_df = (
            comparison_df.copy()
        )

        if comparison_filter != "All":
            filtered_comparison_df = (
                filtered_comparison_df[
                    filtered_comparison_df[
                        "Compared with Stored Data"
                    ]
                    == comparison_filter
                ]
            )

        if action_filter != "All":
            filtered_comparison_df = (
                filtered_comparison_df[
                    filtered_comparison_df[
                        "What Will Happen"
                    ]
                    == action_filter
                ]
            )

        if existing_record_filter != "All":
            filtered_comparison_df = (
                filtered_comparison_df[
                    filtered_comparison_df[
                        "Existing Record"
                    ]
                    == existing_record_filter
                ]
            )

        if differing_field_filter == "Any Difference":
            filtered_comparison_df = (
                filtered_comparison_df[
                    filtered_comparison_df[
                        "Fields That Differ"
                    ]
                    != "—"
                ]
            )
        elif differing_field_filter != "All":
            filtered_comparison_df = (
                filtered_comparison_df[
                    filtered_comparison_df[
                        "Fields That Differ"
                    ].apply(
                        lambda value: (
                            differing_field_filter
                            in {
                                field.strip()
                                for field in str(
                                    value
                                ).split(",")
                                if field.strip()
                                and field.strip()
                                != "—"
                            }
                        )
                    )
                ]
            )

        if date_search:
            filtered_comparison_df = (
                filtered_comparison_df[
                    filtered_comparison_df[
                        "Date"
                    ]
                    .astype(str)
                    .str.contains(
                        date_search,
                        case=False,
                        regex=False,
                        na=False,
                    )
                ]
            )

        st.caption(
            f"Showing {len(filtered_comparison_df):,} of "
            f"{len(comparison_df):,} comparison row(s). "
            "Filters affect display only; approval and Apply remain bound "
            "to the complete unfiltered Database Change Preview."
        )

        if filtered_comparison_df.empty:
            st.info(
                "No comparison rows match the selected filters."
            )
        else:
            st.dataframe(
                filtered_comparison_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Compared with Stored Data": (
                        st.column_config.TextColumn(
                            "Compared with Stored Data",
                            help=(
                                "New: no stored ticker/date exists. "
                                "Same: source and stored OHLCV values match. "
                                "Different: the ticker/date exists but one or "
                                "more OHLCV values differ."
                            ),
                        )
                    ),
                    "What Will Happen": (
                        st.column_config.TextColumn(
                            "What Will Happen",
                            help=(
                                "The exact database action authorized by this "
                                "preview: Add Record, No Change, Keep Stored "
                                "Record, or Replace Stored Record."
                            ),
                        )
                    ),
                    "Existing Record": (
                        st.column_config.TextColumn(
                            "Existing Record",
                            help=(
                                "Yes means the authoritative database already "
                                "contains this ticker/date. This is not an "
                                "error."
                            ),
                        )
                    ),
                    "Fields That Differ": (
                        st.column_config.TextColumn(
                            "Fields That Differ",
                            help=(
                                "The stored OHLCV fields whose values differ "
                                "from the newly acquired source observation."
                            ),
                        )
                    ),
                },
            )

        if is_manual_entry:
            manual_value_rows = []

            for observation in plan.observations:
                candidate_values = (
                    observation.candidate.to_dict()
                )

                manual_value_rows.append(
                    {
                        "Open": candidate_values["Open"],
                        "High": candidate_values["High"],
                        "Low": candidate_values["Low"],
                        "Close": candidate_values["Close"],
                        "Adj Close": candidate_values["Adj Close"],
                        "Volume": candidate_values["Volume"],
                    }
                )

            if manual_value_rows:
                st.caption(
                    "Manual Entry values bound to this exact Preview:"
                )

                st.dataframe(
                    pd.DataFrame(
                        manual_value_rows,
                        columns=[
                            "Open",
                            "High",
                            "Low",
                            "Close",
                            "Adj Close",
                            "Volume",
                        ],
                    ),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Open": st.column_config.NumberColumn(
                            "Open",
                            format="%.3f",
                        ),
                        "High": st.column_config.NumberColumn(
                            "High",
                            format="%.3f",
                        ),
                        "Low": st.column_config.NumberColumn(
                            "Low",
                            format="%.3f",
                        ),
                        "Close": st.column_config.NumberColumn(
                            "Close",
                            format="%.3f",
                        ),
                        "Adj Close": st.column_config.NumberColumn(
                            "Adj Close",
                            format="%.3f",
                        ),
                        "Volume": st.column_config.NumberColumn(
                            "Volume",
                            format="%d",
                        ),
                    },
                )

    if plan.validation_warnings:
        st.markdown("#### Warnings")

        warning_rows = [
            {
                "Ticker": warning.ticker or "—",
                "Date": warning.date or "—",
                "Code": warning.code,
                "Message": warning.message,
            }
            for warning in plan.validation_warnings
        ]

        st.dataframe(
            pd.DataFrame(warning_rows),
            use_container_width=True,
            hide_index=True,
        )

    if plan.excluded_observations:
        st.markdown("#### Rows Not Eligible")
        st.caption(
            "These source rows were returned, but failed required "
            "row-level validation. They are excluded from the database "
            "actions and will not be saved."
        )

        excluded_rows = []

        for observation in plan.excluded_observations:
            for issue in observation.issues:
                excluded_rows.append(
                    {
                        "Candidate Index": (
                            observation.candidate_index
                        ),
                        "Ticker": (
                            observation.ticker or "—"
                        ),
                        "Date": (
                            observation.date or "—"
                        ),
                        "Code": issue.code,
                        "Reason": issue.message,
                    }
                )

        st.dataframe(
            pd.DataFrame(excluded_rows),
            use_container_width=True,
            hide_index=True,
        )

    if plan.source_missing:
        st.markdown(
            "#### Missing From Current yFinance Response"
        )
        st.caption(
            "These expected NYSE trading sessions were not returned in the "
            "current yFinance response used for this Preview. If the "
            "database already contains that ticker-date record, Data "
            "Management keeps it unchanged. If neither yFinance nor the "
            "database has the record, the session remains missing."
        )

        source_missing_action_labels = {
            "preserve_existing": "Keep Stored Record",
            "unresolved": "No Record Available",
        }

        source_missing_rows = []

        for observation in plan.source_missing:
            action_key = str(
                observation.planned_action
            ).strip().lower()

            source_missing_rows.append(
                {
                    "Ticker": observation.ticker,
                    "Date": observation.date.isoformat(),
                    "Stored Record Exists": (
                        "Yes"
                        if observation.existing is not None
                        else "No"
                    ),
                    "What Will Happen": (
                        source_missing_action_labels.get(
                            action_key,
                            observation.planned_action,
                        )
                    ),
                }
            )

        st.dataframe(
            pd.DataFrame(source_missing_rows),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Stored Record Exists": (
                    st.column_config.TextColumn(
                        "Stored Record Exists",
                        help=(
                            "Yes means the authoritative database already "
                            "contains this ticker/date even though the source "
                            "did not return it."
                        ),
                    )
                ),
                "What Will Happen": (
                    st.column_config.TextColumn(
                        "What Will Happen",
                        help=(
                            "Keep Stored Record: retain the existing database "
                            "observation unchanged. No Record Available: "
                            "neither source nor database contains an "
                            "observation, so nothing can be added."
                        ),
                    )
                ),
            },
        )

    if plan.validation_issues:
        st.markdown("#### Blocking Issues")
        st.caption(
            "These problems prevent the entire preview from being applied. "
            "Correct the request and build a new valid preview before "
            "making database changes."
        )

        issue_rows = [
            {
                "Ticker": issue.ticker or "—",
                "Date": issue.date or "—",
                "Code": issue.code,
                "Message": issue.message,
            }
            for issue in plan.validation_issues
        ]

        st.dataframe(
            pd.DataFrame(issue_rows),
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "Preview ID: "
        f"{plan.plan_fingerprint} "
        "— used internally to bind approval to this exact preview."
    )


def _invalidate_data_derived_session_state_after_mutation(
    *,
    rows_affected: int,
) -> bool:
    """
    Invalidate session-derived dashboard state after authoritative OHLCV changes.

    This runs only after DataMutationManager.commit_plan() has succeeded.
    It does not touch database state, source acquisition, indicator formulas,
    scoring semantics, ticker universes, or user selections.

    Returns True when downstream state was invalidated.
    """
    affected = int(
        rows_affected or 0
    )

    if affected <= 0:
        return False

    # Performance Heatmaps / Volume:
    # Clearing the completed request state causes the existing dashboard
    # path to fetch/rebuild from current authoritative data on next use.
    st.session_state.performance_data = None
    st.session_state.last_update = None
    st.session_state.performance_request_signature = None

    st.session_state.volume_data = None
    st.session_state.volume_last_update = None
    st.session_state.volume_request_signature = None

    # Technical Analysis:
    # Retain user controls, but retire analysis/results derived from the
    # superseded OHLCV. Existing compute gating will rebuild on next use.
    for key in (
        "technical_analysis_data",
        "technical_analysis_ticker",
        "technical_analysis_timestamp",
        "technical_analysis_rolling_days",
        "technical_analysis_save_to_db",
        "price_extremes_data",
        "rh_last_params",
        "rh_last_signals",
    ):
        st.session_state.pop(
            key,
            None,
        )

    # Stock Comparison:
    # Clear all session-only data-derived caches plus rendered matrices.
    # The stale flag intentionally suppresses Single Indicator's normal
    # first-load auto-build so the administrator explicitly rebuilds.
    _clear_scd_session_cache()

    st.session_state.scd_signal_matrix = None
    st.session_state.scd_matrix_last_run = None
    st.session_state.scd_single_indicator_matrix = None
    st.session_state.scd_single_indicator_matrix_last_run = None

    st.session_state[
        _DATA_MANAGEMENT_SCD_STALE_KEY
    ] = True

    return True


def _render_data_management_mutation_controls(
    plan: MutationPlan,
) -> None:
    """Render explicit confirmation and exact-plan Commit controls."""
    confirmed_fingerprint = st.session_state.get(
        _DATA_MANAGEMENT_MUTATION_CONFIRMED_FINGERPRINT_KEY
    )

    is_confirmed = (
        confirmed_fingerprint == plan.plan_fingerprint
    )

    is_deletion = (
        plan.operation
        in {
            "Delete Range",
            "Delete Ticker",
        }
    )

    if not plan.can_commit:
        st.error(
            "This preview contains blocking issues. Changes cannot be "
            "applied until a new valid preview is built."
        )
    elif is_confirmed:
        st.success(
            "These exact changes are approved and ready to apply."
        )
    else:
        st.info(
            "Review the database changes above, then approve them before "
            "applying anything to the authoritative database."
        )

    is_manual_entry = (
        str(
            plan.source
        ).strip()
        == "Manual Entry"
        and plan.operation
        in {
            "Manual Add",
            "Manual Replace",
        }
    )

    if is_manual_entry:
        (
            confirm_column,
            commit_column,
            edit_column,
            discard_column,
        ) = st.columns(4)
    else:
        (
            confirm_column,
            commit_column,
            discard_column,
        ) = st.columns(3)

        edit_column = None

    with confirm_column:
        confirm_clicked = st.button(
            "Approve These Changes",
            key="data_management_mutation_confirm",
            type="primary",
            disabled=not plan.can_commit,
            use_container_width=True,
            help=(
                "Approve this exact Database Change Preview. Approval does "
                "not change the database. If a new preview is built, this "
                "approval no longer applies."
            ),
        )

    if confirm_clicked:
        st.session_state[
            _DATA_MANAGEMENT_MUTATION_CONFIRMED_FINGERPRINT_KEY
        ] = plan.plan_fingerprint
        st.session_state.pop(
            _DATA_MANAGEMENT_MUTATION_ERROR_KEY,
            None,
        )
        st.rerun()

    with commit_column:
        commit_clicked = st.button(
            "Apply Approved Changes",
            key="data_management_mutation_commit",
            disabled=(
                not plan.can_commit
                or not is_confirmed
            ),
            use_container_width=True,
            help=(
                (
                    "Apply only the approved deletion shown in this preview "
                    "to the authoritative OHLCV database. This is the step "
                    "that permanently deletes the approved stored records."
                )
                if is_deletion
                else (
                    "Apply only the approved actions shown in this preview "
                    "to the authoritative OHLCV database. This is the step "
                    "that actually inserts or replaces records when the "
                    "approved plan calls for those actions."
                )
            ),
        )

    if commit_clicked:
        mutation_manager = DataMutationManager()

        try:
            result = mutation_manager.commit_plan(
                plan,
                confirmed_plan_fingerprint=(
                    confirmed_fingerprint
                ),
            )
        except Exception as exc:
            st.session_state[
                _DATA_MANAGEMENT_MUTATION_ERROR_KEY
            ] = str(exc)

            st.session_state.pop(
                _DATA_MANAGEMENT_MUTATION_CONFIRMED_FINGERPRINT_KEY,
                None,
            )

            st.rerun()

        derived_state_invalidated = (
            _invalidate_data_derived_session_state_after_mutation(
                rows_affected=result.rows_affected,
            )
        )

        st.session_state[
            _DATA_MANAGEMENT_MUTATION_RESULT_KEY
        ] = {
            "operation": plan.operation,
            "plan_fingerprint": (
                plan.plan_fingerprint
            ),
            "rows_affected": result.rows_affected,
            "audit_id": result.audit_id,
            "derived_state_invalidated": (
                derived_state_invalidated
            ),
        }

        st.session_state.pop(
            _DATA_MANAGEMENT_MUTATION_PLAN_KEY,
            None,
        )
        st.session_state.pop(
            _DATA_MANAGEMENT_MUTATION_CONFIRMED_FINGERPRINT_KEY,
            None,
        )
        st.session_state.pop(
            _DATA_MANAGEMENT_MUTATION_ERROR_KEY,
            None,
        )
        st.session_state.pop(
            _DATA_MANAGEMENT_ACQUISITION_CONTEXT_KEY,
            None,
        )
        st.session_state.pop(
            _DATA_MANAGEMENT_MAINTENANCE_REQUEST_KEY,
            None,
        )
        st.session_state.pop(
            _DATA_MANAGEMENT_MANUAL_ENTRY_CONTEXT_KEY,
            None,
        )

        st.rerun()

    edit_clicked = False

    if edit_column is not None:
        with edit_column:
            edit_clicked = st.button(
                "Edit Manual Inputs",
                key=(
                    "data_management_manual_entry_"
                    "edit_inputs"
                ),
                use_container_width=True,
                help=(
                    "Discard this Preview and its approval while preserving "
                    "the Manual Entry values so they can be corrected and "
                    "previewed again. No database changes are made."
                ),
            )

    if edit_clicked:
        _discard_data_management_mutation_plan(
            preserve_manual_entry_context=True,
        )
        st.session_state.pop(
            _DATA_MANAGEMENT_MUTATION_RESULT_KEY,
            None,
        )
        st.rerun()

    with discard_column:
        discard_clicked = st.button(
            "Cancel Preview",
            key="data_management_mutation_discard",
            use_container_width=True,
            help=(
                "Discard this preview and its approval so you can change "
                "the Data Management request. No database changes are made."
            ),
        )

    if discard_clicked:
        _discard_data_management_mutation_plan()
        st.session_state.pop(
            _DATA_MANAGEMENT_MUTATION_RESULT_KEY,
            None,
        )
        st.rerun()


def _render_data_management_audit_history(
    *,
    mutation_manager: DataMutationManager,
) -> None:
    """
    Render bounded, read-only Data Management Audit History.

    This surface inspects successfully committed Data Management operations
    only. It does not create, update, delete, replay, or otherwise mutate
    audit events or daily_prices.
    """
    st.markdown("---")
    st.subheader("Audit History")

    st.caption(
        "Review successfully committed Data Management operations. "
        "A successful committed operation may have zero Rows Affected when "
        "the approved operation required no physical database changes."
    )

    try:
        audit_actions = (
            mutation_manager.get_audit_actions()
        )
    except Exception as exc:
        st.error(
            "Unable to read Audit History actions: "
            f"{exc}"
        )
        return

    filter_columns = st.columns(
        [1.2, 1.2, 1, 1]
    )

    with filter_columns[0]:
        ticker_filter = st.text_input(
            "Ticker",
            value="",
            key="data_management_audit_ticker_filter",
            help=(
                "Show committed audit events involving this ticker. "
                "The filter includes ticker evidence stored in requested "
                "scope, committed mutations, Source Missing evidence, "
                "deletions, and duplicate repairs."
            ),
        )

    with filter_columns[1]:
        action_filter = st.selectbox(
            "Action",
            options=[
                "All",
                *audit_actions,
            ],
            index=0,
            key="data_management_audit_action_filter",
            help=(
                "Filter by the committed Data Management action stored "
                "in Audit History."
            ),
        )

    with filter_columns[2]:
        commit_date_from = st.date_input(
            "Commit Date From",
            value=None,
            key="data_management_audit_commit_date_from",
            help=(
                "Filter by when the operation committed. "
                "This is not the requested OHLCV Start Date."
            ),
        )

    with filter_columns[3]:
        commit_date_to = st.date_input(
            "Commit Date To",
            value=None,
            key="data_management_audit_commit_date_to",
            help=(
                "Filter by when the operation committed. "
                "This is not the requested OHLCV End Date."
            ),
        )

    if (
        commit_date_from is not None
        and commit_date_to is not None
        and commit_date_from > commit_date_to
    ):
        st.error(
            "Commit Date From cannot be later than Commit Date To."
        )
        return

    selected_action = (
        None
        if action_filter == "All"
        else action_filter
    )

    try:
        audit_history = (
            mutation_manager.get_audit_history(
                ticker=(
                    ticker_filter
                    if str(
                        ticker_filter
                    ).strip()
                    else None
                ),
                action=selected_action,
                start_commit_date=commit_date_from,
                end_commit_date=commit_date_to,
                limit=100,
            )
        )
    except Exception as exc:
        st.error(
            "Unable to read Audit History: "
            f"{exc}"
        )
        return

    st.caption(
        "Showing up to the 100 newest matching committed operations."
    )

    if not audit_history:
        st.info(
            "No Audit History events match the current filters."
        )
        return

    history_rows = []

    for record in audit_history:
        history_rows.append(
            {
                "Audit ID": record.audit_id,
                "Timestamp": record.timestamp,
                "Action": record.action,
                "Ticker": record.display_ticker,
                "Start Date": (
                    record.start_date
                    or "\u2014"
                ),
                "End Date": (
                    record.end_date
                    or "\u2014"
                ),
                "Source": record.source,
                "Rows Affected": (
                    record.rows_affected
                ),
            }
        )

    history_frame = pd.DataFrame(
        history_rows
    )

    st.dataframe(
        history_frame,
        hide_index=True,
        use_container_width=True,
    )

    records_by_id = {
        record.audit_id: record
        for record in audit_history
    }

    audit_id_options = [
        record.audit_id
        for record in audit_history
    ]

    selected_audit_id = st.selectbox(
        "View Audit Event",
        options=audit_id_options,
        index=0,
        format_func=lambda audit_id: (
            f"#{audit_id} — "
            f"{records_by_id[audit_id].timestamp} — "
            f"{records_by_id[audit_id].action} — "
            f"{records_by_id[audit_id].display_ticker}"
        ),
        key="data_management_audit_selected_event",
        help=(
            "Select one committed operation to inspect its stored "
            "request scope, affected scope, summary, and audit evidence."
        ),
    )

    record = records_by_id[
        selected_audit_id
    ]

    details = record.details

    st.markdown("#### Audit Event")

    event_columns = st.columns(4)

    event_columns[0].metric(
        "Audit ID",
        record.audit_id,
    )
    event_columns[1].metric(
        "Action",
        record.action,
    )
    event_columns[2].metric(
        "Source",
        record.source,
    )
    event_columns[3].metric(
        "Rows Affected",
        record.rows_affected,
        help=(
            "Physical database mutation effects performed by the "
            "committed operation. Zero is a valid successful result."
        ),
    )

    st.caption(
        "Committed: "
        f"{record.timestamp}"
    )

    if record.details_parse_error:
        st.warning(
            "Structured Audit Details could not be parsed. "
            "The authoritative summary row remains available, and the "
            "exact stored details value is preserved in the advanced "
            "raw-details section below. "
            f"Parser message: {record.details_parse_error}"
        )

    st.markdown("#### Requested Scope")

    requested_ticker_label = (
        ", ".join(
            record.requested_tickers
        )
        if record.requested_tickers
        else (
            record.ticker
            or "\u2014"
        )
    )

    requested_scope_columns = (
        st.columns(3)
    )

    requested_scope_columns[0].metric(
        "Requested Ticker(s)",
        requested_ticker_label,
    )
    requested_scope_columns[1].metric(
        "Requested Start Date",
        record.start_date
        or "\u2014",
    )
    requested_scope_columns[2].metric(
        "Requested End Date",
        record.end_date
        or "\u2014",
    )

    st.caption(
        "Requested Scope reflects the scope persisted with the "
        "committed operation. Manual Entry may legitimately have no "
        "stored requested ticker/date scope because its affected record "
        "identity is carried in committed mutation evidence."
    )

    st.markdown("#### Affected Scope")

    affected_ticker_label = (
        ", ".join(
            record.affected_tickers
        )
        if record.affected_tickers
        else "\u2014"
    )

    affected_scope_columns = (
        st.columns(3)
    )

    affected_scope_columns[0].metric(
        "Affected Ticker(s)",
        affected_ticker_label,
    )
    affected_scope_columns[1].metric(
        "First Affected Date",
        record.affected_start_date
        or "\u2014",
    )
    affected_scope_columns[2].metric(
        "Last Affected Date",
        record.affected_end_date
        or "\u2014",
    )

    if record.rows_affected == 0:
        st.caption(
            "No physical database rows were changed by this committed "
            "operation."
        )

    summary = details.get(
        "summary",
        {},
    )

    if isinstance(
        summary,
        dict,
    ):
        summary_labels = {
            "new": "New Observations",
            "changed": "Changed Observations",
            "unchanged": "Unchanged Observations",
            "insert": "Rows Inserted",
            "replacement_candidate": (
                "Replacement Candidates"
            ),
            "preserve_existing": (
                "Existing Records Preserved"
            ),
            "no_change": "No Change",
            "delete": "Rows Deleted",
            "source_missing": "Source Missing",
            "source_missing_preserved": (
                "Source Missing Preserved"
            ),
            "source_missing_unresolved": (
                "Source Missing Unresolved"
            ),
            "duplicate_keys": "Duplicate Keys",
            "validation_issues": (
                "Validation Issues"
            ),
            "validation_warnings": (
                "Validation Warnings"
            ),
            "excluded_observations": (
                "Excluded Observations"
            ),
            "excluded_validation_issues": (
                "Excluded Validation Issues"
            ),
        }

        summary_rows = []

        for key, label in summary_labels.items():
            if key not in summary:
                continue

            value = summary.get(
                key
            )

            show_zero = (
                record.rows_affected == 0
                and key
                in {
                    "insert",
                    "replacement_candidate",
                    "delete",
                }
            )

            if (
                value
                or show_zero
            ):
                summary_rows.append(
                    {
                        "Metric": label,
                        "Count": value,
                    }
                )

        if summary_rows:
            st.markdown(
                "#### Operation Summary"
            )

            st.dataframe(
                pd.DataFrame(
                    summary_rows
                ),
                hide_index=True,
                use_container_width=True,
            )

    validation_warnings = details.get(
        "validation_warnings",
        [],
    )

    if (
        isinstance(
            validation_warnings,
            list,
        )
        and validation_warnings
    ):
        st.markdown(
            "#### Validation Warnings"
        )

        st.dataframe(
            pd.DataFrame(
                validation_warnings
            ),
            hide_index=True,
            use_container_width=True,
        )

    excluded_observations = details.get(
        "excluded_observations",
        [],
    )

    if (
        isinstance(
            excluded_observations,
            list,
        )
        and excluded_observations
    ):
        st.markdown(
            "#### Excluded Observations"
        )

        excluded_rows = []

        for observation in excluded_observations:
            if not isinstance(
                observation,
                dict,
            ):
                continue

            issues = observation.get(
                "issues",
                [],
            )

            issue_messages = []

            if isinstance(
                issues,
                list,
            ):
                for issue in issues:
                    if not isinstance(
                        issue,
                        dict,
                    ):
                        continue

                    message = str(
                        issue.get(
                            "message",
                            "",
                        )
                        or ""
                    ).strip()

                    code = str(
                        issue.get(
                            "code",
                            "",
                        )
                        or ""
                    ).strip()

                    if code and message:
                        issue_messages.append(
                            f"{code}: {message}"
                        )
                    elif message:
                        issue_messages.append(
                            message
                        )
                    elif code:
                        issue_messages.append(
                            code
                        )

            excluded_rows.append(
                {
                    "Candidate Index": (
                        observation.get(
                            "candidate_index"
                        )
                    ),
                    "Ticker": (
                        observation.get(
                            "ticker"
                        )
                    ),
                    "Date": (
                        observation.get(
                            "date"
                        )
                    ),
                    "Issues": (
                        " | ".join(
                            issue_messages
                        )
                        if issue_messages
                        else "\u2014"
                    ),
                }
            )

        if excluded_rows:
            st.dataframe(
                pd.DataFrame(
                    excluded_rows
                ),
                hide_index=True,
                use_container_width=True,
            )

    mutations = details.get(
        "mutations",
        [],
    )

    if (
        isinstance(
            mutations,
            list,
        )
        and mutations
    ):
        st.markdown(
            "#### Committed Mutations"
        )

        mutation_rows = []

        for mutation in mutations:
            if not isinstance(
                mutation,
                dict,
            ):
                continue

            differing_fields = (
                mutation.get(
                    "differing_fields",
                    [],
                )
            )

            if isinstance(
                differing_fields,
                list,
            ):
                differing_fields_label = (
                    ", ".join(
                        str(
                            field
                        )
                        for field
                        in differing_fields
                    )
                    if differing_fields
                    else "\u2014"
                )
            else:
                differing_fields_label = (
                    str(
                        differing_fields
                    )
                )

            mutation_rows.append(
                {
                    "Ticker": (
                        mutation.get(
                            "Ticker"
                        )
                    ),
                    "Date": (
                        mutation.get(
                            "Date"
                        )
                    ),
                    "Classification": (
                        mutation.get(
                            "classification"
                        )
                    ),
                    "Planned Action": (
                        mutation.get(
                            "planned_action"
                        )
                    ),
                    "Differing Fields": (
                        differing_fields_label
                    ),
                }
            )

        if mutation_rows:
            st.dataframe(
                pd.DataFrame(
                    mutation_rows
                ),
                hide_index=True,
                use_container_width=True,
            )

    source_missing = details.get(
        "source_missing",
        [],
    )

    if (
        isinstance(
            source_missing,
            list,
        )
        and source_missing
    ):
        st.markdown(
            "#### Source Missing"
        )

        st.dataframe(
            pd.DataFrame(
                source_missing
            ),
            hide_index=True,
            use_container_width=True,
        )

    deletion = details.get(
        "deletion"
    )

    if isinstance(
        deletion,
        dict,
    ):
        st.markdown(
            "#### Deletion Details"
        )

        deletion_rows = [
            {
                "Planned Action": (
                    deletion.get(
                        "planned_action"
                    )
                ),
                "Materialized Rows": (
                    deletion.get(
                        "materialized_rows"
                    )
                ),
                "First Affected Date": (
                    deletion.get(
                        "first_affected_date"
                    )
                ),
                "Last Affected Date": (
                    deletion.get(
                        "last_affected_date"
                    )
                ),
            }
        ]

        st.dataframe(
            pd.DataFrame(
                deletion_rows
            ),
            hide_index=True,
            use_container_width=True,
        )

    duplicate_repairs = details.get(
        "duplicate_repairs",
        [],
    )

    if (
        isinstance(
            duplicate_repairs,
            list,
        )
        and duplicate_repairs
    ):
        st.markdown(
            "#### Duplicate Repair Details"
        )

        for repair_index, repair in enumerate(
            duplicate_repairs,
            start=1,
        ):
            if not isinstance(
                repair,
                dict,
            ):
                continue

            repair_ticker = str(
                repair.get(
                    "Ticker",
                    "",
                )
                or ""
            )

            repair_date = str(
                repair.get(
                    "Date",
                    "",
                )
                or ""
            )

            with st.expander(
                (
                    f"Repair {repair_index}: "
                    f"{repair_ticker or '\u2014'} "
                    f"{repair_date or '\u2014'}"
                ),
                expanded=False,
            ):
                repair_columns = (
                    st.columns(3)
                )

                repair_columns[0].metric(
                    "Planned Action",
                    repair.get(
                        "planned_action"
                    )
                    or "\u2014",
                )

                repair_columns[1].metric(
                    "Physical Rows Removed",
                    repair.get(
                        "physical_rows_removed",
                        0,
                    ),
                )

                stored_records = repair.get(
                    "stored_records",
                    [],
                )

                stored_record_count = (
                    len(
                        stored_records
                    )
                    if isinstance(
                        stored_records,
                        list,
                    )
                    else 0
                )

                repair_columns[2].metric(
                    "Stored Records",
                    stored_record_count,
                )

                canonical_candidate = (
                    repair.get(
                        "canonical_candidate"
                    )
                )

                if isinstance(
                    canonical_candidate,
                    dict,
                ):
                    st.caption(
                        "Canonical replacement"
                    )

                    st.dataframe(
                        pd.DataFrame(
                            [
                                canonical_candidate
                            ]
                        ),
                        hide_index=True,
                        use_container_width=True,
                    )

                if (
                    isinstance(
                        stored_records,
                        list,
                    )
                    and stored_records
                ):
                    st.caption(
                        "Stored physical records removed"
                    )

                    st.dataframe(
                        pd.DataFrame(
                            stored_records
                        ),
                        hide_index=True,
                        use_container_width=True,
                    )

    st.markdown(
        "#### Technical Identity"
    )

    technical_rows = [
        {
            "Field": "Plan Fingerprint",
            "Value": (
                record.plan_fingerprint
            ),
        },
        {
            "Field": "Baseline Fingerprint",
            "Value": (
                details.get(
                    "baseline_fingerprint"
                )
                or "\u2014"
            ),
        },
    ]

    st.dataframe(
        pd.DataFrame(
            technical_rows
        ),
        hide_index=True,
        use_container_width=True,
    )

    with st.expander(
        "Advanced — Raw Audit Details",
        expanded=False,
    ):
        if record.raw_details is None:
            st.caption(
                "No raw Audit Details value is stored for this event."
            )
        elif not record.raw_details:
            st.caption(
                "The stored Audit Details value is empty."
            )
        else:
            st.code(
                record.raw_details,
                language="json",
            )


def _render_data_management_mutation_workflow() -> None:
    """
    Render mutation result/error state and the active Preview when present.

    With no active mutation state this helper is intentionally a no-op.
    """
    mutation_result = st.session_state.get(
        _DATA_MANAGEMENT_MUTATION_RESULT_KEY
    )

    mutation_error = st.session_state.get(
        _DATA_MANAGEMENT_MUTATION_ERROR_KEY
    )

    active_plan = st.session_state.get(
        _DATA_MANAGEMENT_MUTATION_PLAN_KEY
    )

    if (
        mutation_result is None
        and mutation_error is None
        and active_plan is None
    ):
        return

    if mutation_result is not None:
        st.markdown("---")
        st.subheader("Database Change Result")
        st.success(
            "The approved database changes were applied successfully."
        )

        result_columns = st.columns(3)

        result_columns[0].metric(
            "Operation",
            mutation_result["operation"],
        )
        result_columns[1].metric(
            "Rows Affected",
            f"{mutation_result['rows_affected']:,}",
        )
        result_columns[2].metric(
            "Audit ID",
            str(mutation_result["audit_id"]),
        )

        if mutation_result.get(
            "derived_state_invalidated"
        ):
            st.info(
                "Authoritative OHLCV changed. Cached or previously rendered "
                "dashboard results derived from the older data were cleared. "
                "Performance and Technical Analysis will refresh through their "
                "existing workflows; Stock Comparison will ask you to rebuild "
                "its matrix."
            )
        elif int(
            mutation_result.get(
                "rows_affected",
                0,
            ) or 0
        ) == 0:
            st.caption(
                "No OHLCV rows changed, so downstream dashboard state "
                "did not need to be invalidated."
            )

        st.caption(
            "Committed Preview fingerprint: "
            f"{mutation_result['plan_fingerprint']}"
        )

    if mutation_error is not None:
        st.markdown("---")
        st.subheader("Database Change Error")
        st.error(mutation_error)
        st.caption(
            "Approval was cleared. Review the error and build a fresh "
            "Database Change Preview when required."
        )

    if active_plan is None:
        return

    if not isinstance(active_plan, MutationPlan):
        st.error(
            "Stored Data Management mutation state is invalid. "
            "Discard the Preview and build a fresh one."
        )
        return

    _render_data_management_mutation_preview(
        active_plan
    )
    _render_data_management_mutation_controls(
        active_plan
    )


def _render_data_management_universe_management(
    *,
    inventory: list[Dict[str, Any]],
) -> None:
    """
    Render persistent ticker-universe membership and metadata controls.

    Universe mutations are intentionally independent from authoritative
    OHLCV storage. These controls do not acquire, replace, or delete
    daily_prices observations.
    """
    universe_manager = UniverseManager()

    stored_ticker_set = {
        str(row["ticker"]).strip().upper()
        for row in inventory
        if row.get("ticker")
    }

    st.markdown("---")
    st.subheader("Ticker Universe Management")
    st.caption(
        "Manage persistent Custom, Sector, and Country membership. "
        "Universe membership is independent from stored market data: "
        "adding a ticker to a bucket does not acquire OHLCV, and removing "
        "a ticker from a bucket does not delete OHLCV."
    )

    try:
        schema_status = (
            universe_manager.get_schema_status()
        )
    except Exception as exc:
        st.error(
            "Unable to read persistent ticker-universe infrastructure: "
            f"{exc}"
        )
        return

    if not schema_status.compatible:
        st.error(
            "Persistent ticker-universe infrastructure is not compatible. "
            "Universe management is unavailable until the schema is "
            "corrected."
        )
        return

    result_message = st.session_state.pop(
        "data_management_universe_result",
        None,
    )
    error_message = st.session_state.pop(
        "data_management_universe_error",
        None,
    )

    if result_message:
        st.success(
            result_message
        )

    if error_message:
        st.error(
            error_message
        )

    try:
        custom_records = (
            universe_manager.get_bucket_records(
                "Custom"
            )
        )
        sector_records = (
            universe_manager.get_bucket_records(
                "Sector"
            )
        )
        country_records = (
            universe_manager.get_bucket_records(
                "Country"
            )
        )
    except Exception as exc:
        st.error(
            "Unable to read persistent universe membership: "
            f"{exc}"
        )
        return

    summary_columns = st.columns(3)

    summary_columns[0].metric(
        "Custom",
        len(custom_records),
    )
    summary_columns[1].metric(
        "Sector",
        len(sector_records),
    )
    summary_columns[2].metric(
        "Country",
        len(country_records),
    )

    (
        add_tab,
        remove_tab,
        rename_tab,
        reorder_tab,
    ) = st.tabs(
        [
            "Add to Bucket",
            "Remove from Bucket",
            "Edit Display Name",
            "Reorder in Bucket",
        ]
    )

    with add_tab:
        st.caption(
            "Add one persistent bucket membership. "
            "If the ticker has no metadata row yet, one is created. "
            "No market data is acquired. A stored ticker with no "
            "Custom, Sector, or Country membership is Unassigned; "
            "adding it here assigns it to the selected bucket."
        )

        add_columns = st.columns(
            [1, 1, 2]
        )

        with add_columns[0]:
            add_ticker = st.text_input(
                "Ticker",
                value="",
                key=(
                    "data_management_universe_"
                    "add_ticker"
                ),
            ).strip().upper()

        with add_columns[1]:
            add_bucket = st.selectbox(
                "Bucket",
                options=[
                    "Custom",
                    "Sector",
                    "Country",
                ],
                key=(
                    "data_management_universe_"
                    "add_bucket"
                ),
            )

        with add_columns[2]:
            add_display_name = st.text_input(
                "Display name for new ticker (optional)",
                value="",
                key=(
                    "data_management_universe_"
                    "add_display_name"
                ),
                help=(
                    "Used only when ticker metadata does not already "
                    "exist. Existing display names are not silently "
                    "overwritten."
                ),
            ).strip()

        if add_ticker:
            try:
                current_memberships = (
                    universe_manager.get_bucket_memberships(
                        add_ticker
                    )
                )

                current_display_name = (
                    universe_manager.get_display_name(
                        add_ticker
                    )
                )

                membership_labels = [
                    membership.bucket
                    for membership
                    in current_memberships
                ]

                if membership_labels:
                    membership_text = ", ".join(
                        membership_labels
                    )
                    state_text = (
                        "Current membership"
                        if len(membership_labels) == 1
                        else "Current memberships"
                    )

                    st.info(
                        f"{state_text}: {membership_text}"
                    )

                elif add_ticker in stored_ticker_set:
                    st.info(
                        "Current status: Unassigned — "
                        "stored OHLCV exists, but this ticker has "
                        "no persistent Custom, Sector, or Country "
                        "membership."
                    )

                else:
                    st.info(
                        "Current memberships: none — "
                        "this ticker is not currently stored in "
                        "daily_prices."
                    )

                st.caption(
                    "Current display name: "
                    f"{current_display_name}"
                )

            except Exception as exc:
                st.warning(
                    "Unable to inspect current ticker state: "
                    f"{exc}"
                )

        if st.button(
            "Add to Bucket",
            key=(
                "data_management_universe_"
                "add_button"
            ),
            type="primary",
        ):
            if not add_ticker:
                st.warning(
                    "Enter a ticker before adding membership."
                )
            else:
                try:
                    add_result = (
                        universe_manager.add_to_bucket(
                            ticker=add_ticker,
                            bucket=add_bucket,
                            display_name=(
                                add_display_name
                                if add_display_name
                                else None
                            ),
                        )
                    )

                    st.session_state[
                        "data_management_universe_result"
                    ] = (
                        f"Added {add_result.ticker} to "
                        f"{add_result.bucket} at position "
                        f"{add_result.sort_order}."
                    )

                    st.session_state.pop(
                        "data_management_universe_error",
                        None,
                    )

                    st.rerun()

                except Exception as exc:
                    st.session_state[
                        "data_management_universe_error"
                    ] = str(exc)

                    st.rerun()

    with remove_tab:
        st.caption(
            "Remove exactly one bucket membership. "
            "Other memberships, ticker metadata, and stored OHLCV "
            "are preserved. If this is the ticker's final bucket "
            "membership and stored OHLCV exists, the ticker will "
            "become Unassigned."
        )

        remove_bucket = st.selectbox(
            "Bucket",
            options=[
                "Custom",
                "Sector",
                "Country",
            ],
            key=(
                "data_management_universe_"
                "remove_bucket"
            ),
        )

        remove_record_map = {
            "Custom": custom_records,
            "Sector": sector_records,
            "Country": country_records,
        }

        remove_records = remove_record_map[
            remove_bucket
        ]

        if not remove_records:
            st.info(
                f"{remove_bucket} has no persistent members."
            )
        else:
            remove_name_map = {
                record.ticker: record.display_name
                for record in remove_records
            }

            remove_ticker = st.selectbox(
                "Ticker to remove",
                options=[
                    record.ticker
                    for record in remove_records
                ],
                format_func=lambda ticker: (
                    f"{remove_name_map[ticker]} "
                    f"({ticker})"
                    if (
                        remove_name_map[ticker]
                        and remove_name_map[ticker]
                        != ticker
                    )
                    else ticker
                ),
                key=(
                    "data_management_universe_"
                    "remove_ticker"
                ),
            )

            remove_confirmed = st.checkbox(
                (
                    "I understand this removes only the "
                    f"{remove_bucket} membership and does "
                    "not delete stored market data."
                ),
                key=(
                    "data_management_universe_"
                    "remove_confirmed"
                ),
            )

            if st.button(
                "Remove from Bucket",
                key=(
                    "data_management_universe_"
                    "remove_button"
                ),
            ):
                if not remove_confirmed:
                    st.warning(
                        "Confirm the membership-only removal "
                        "before continuing."
                    )
                else:
                    try:
                        remove_result = (
                            universe_manager.remove_from_bucket(
                                ticker=remove_ticker,
                                bucket=remove_bucket,
                            )
                        )

                        st.session_state[
                            "data_management_universe_result"
                        ] = (
                            f"Removed {remove_result.ticker} "
                            f"from {remove_result.bucket}. "
                            "Ticker metadata and stored market "
                            "data were preserved."
                        )

                        st.session_state.pop(
                            "data_management_universe_error",
                            None,
                        )

                        st.rerun()

                    except Exception as exc:
                        st.session_state[
                            "data_management_universe_error"
                        ] = str(exc)

                        st.rerun()

    with rename_tab:
        st.caption(
            "Edit the canonical ticker-level display name. "
            "This does not change bucket membership or stored OHLCV."
        )

        rename_columns = st.columns(
            [1, 2]
        )

        with rename_columns[0]:
            rename_ticker = st.text_input(
                "Ticker",
                value="",
                key=(
                    "data_management_universe_"
                    "rename_ticker"
                ),
            ).strip().upper()

        with rename_columns[1]:
            rename_display_name = st.text_input(
                "New display name",
                value="",
                key=(
                    "data_management_universe_"
                    "rename_display_name"
                ),
            ).strip()

        if rename_ticker:
            try:
                current_name = (
                    universe_manager.get_display_name(
                        rename_ticker
                    )
                )
                current_memberships = (
                    universe_manager.get_bucket_memberships(
                        rename_ticker
                    )
                )

                st.caption(
                    "Current persistent state — "
                    f"Display name: {current_name}; "
                    "Memberships: "
                    + (
                        ", ".join(
                            membership.bucket
                            for membership
                            in current_memberships
                        )
                        if current_memberships
                        else "none"
                    )
                )
            except Exception as exc:
                st.warning(
                    "Unable to inspect current ticker state: "
                    f"{exc}"
                )

        if st.button(
            "Update Display Name",
            key=(
                "data_management_universe_"
                "rename_button"
            ),
        ):
            if not rename_ticker:
                st.warning(
                    "Enter a ticker before updating its display name."
                )
            elif not rename_display_name:
                st.warning(
                    "Enter a new display name."
                )
            else:
                try:
                    rename_result = (
                        universe_manager.update_display_name(
                            ticker=rename_ticker,
                            display_name=rename_display_name,
                        )
                    )

                    st.session_state[
                        "data_management_universe_result"
                    ] = (
                        f"Updated {rename_result.ticker} display "
                        f"name from "
                        f"'{rename_result.previous_display_name}' "
                        f"to '{rename_result.display_name}'."
                    )

                    st.session_state.pop(
                        "data_management_universe_error",
                        None,
                    )

                    st.rerun()

                except Exception as exc:
                    st.session_state[
                        "data_management_universe_error"
                    ] = str(exc)

                    st.rerun()

    with reorder_tab:
        st.caption(
            "Move one ticker up or down within a single persistent "
            "bucket. Membership in all buckets remains unchanged."
        )

        reorder_bucket = st.selectbox(
            "Bucket",
            options=[
                "Custom",
                "Sector",
                "Country",
            ],
            key=(
                "data_management_universe_"
                "reorder_bucket"
            ),
        )

        reorder_record_map = {
            "Custom": custom_records,
            "Sector": sector_records,
            "Country": country_records,
        }

        reorder_records = list(
            reorder_record_map[
                reorder_bucket
            ]
        )

        if not reorder_records:
            st.info(
                f"{reorder_bucket} has no persistent members."
            )
        else:
            reorder_name_map = {
                record.ticker: record.display_name
                for record in reorder_records
            }

            reorder_tickers = [
                record.ticker
                for record in reorder_records
            ]

            reorder_ticker = st.selectbox(
                "Ticker to move",
                options=reorder_tickers,
                format_func=lambda ticker: (
                    f"{reorder_name_map[ticker]} "
                    f"({ticker})"
                    if (
                        reorder_name_map[ticker]
                        and reorder_name_map[ticker]
                        != ticker
                    )
                    else ticker
                ),
                key=(
                    "data_management_universe_"
                    "reorder_ticker"
                ),
            )

            current_index = reorder_tickers.index(
                reorder_ticker
            )

            st.caption(
                f"Current position: "
                f"{current_index + 1} of "
                f"{len(reorder_tickers)}"
            )

            up_column, down_column = st.columns(2)

            with up_column:
                move_up = st.button(
                    "Move Up",
                    key=(
                        "data_management_universe_"
                        "move_up"
                    ),
                    disabled=(
                        current_index == 0
                    ),
                )

            with down_column:
                move_down = st.button(
                    "Move Down",
                    key=(
                        "data_management_universe_"
                        "move_down"
                    ),
                    disabled=(
                        current_index
                        == len(reorder_tickers) - 1
                    ),
                )

            if move_up or move_down:
                proposed_order = list(
                    reorder_tickers
                )

                target_index = (
                    current_index - 1
                    if move_up
                    else current_index + 1
                )

                (
                    proposed_order[current_index],
                    proposed_order[target_index],
                ) = (
                    proposed_order[target_index],
                    proposed_order[current_index],
                )

                try:
                    reorder_result = (
                        universe_manager.reorder_bucket(
                            bucket=reorder_bucket,
                            ordered_tickers=proposed_order,
                        )
                    )

                    new_position = (
                        reorder_result.ordered_tickers.index(
                            reorder_ticker
                        )
                        + 1
                    )

                    st.session_state[
                        "data_management_universe_result"
                    ] = (
                        f"Moved {reorder_ticker} to position "
                        f"{new_position} in {reorder_bucket}."
                    )

                    st.session_state.pop(
                        "data_management_universe_error",
                        None,
                    )

                    st.rerun()

                except Exception as exc:
                    st.session_state[
                        "data_management_universe_error"
                    ] = str(exc)

                    st.rerun()


def show_data_management():
    """Render Data Management inspection and controlled mutation workflows."""
    st.title("Data Management")
    st.caption(
        "Inspect authoritative OHLCV coverage and use controlled "
        "Preview → Approve → Apply workflows to manage stored market data."
    )

    mutation_manager = DataMutationManager()

    try:
        audit_status = (
            mutation_manager.get_audit_schema_status()
        )

        if not audit_status.exists:
            audit_status = (
                mutation_manager.initialize_audit_schema()
            )

        if not audit_status.compatible:
            missing_columns = ", ".join(
                audit_status.missing_columns
            )

            st.error(
                "Data Management audit infrastructure is incompatible. "
                "Database changes are unavailable until the audit schema "
                "is corrected."
                + (
                    f" Missing required column(s): {missing_columns}."
                    if missing_columns
                    else ""
                )
            )
            return

    except Exception as exc:
        st.error(
            "Unable to initialize Data Management audit infrastructure: "
            f"{exc}"
        )
        return

    manager = DatabaseManager()

    try:
        inventory = manager.get_ticker_inventory()
        overview = manager.get_database_overview(
            inventory=inventory
        )
    except Exception as exc:
        st.error(f"Unable to read the market-data database: {exc}")
        return

    st.subheader("Database Overview")

    primary_metric_columns = st.columns(4)

    primary_metric_columns[0].metric(
        "Unique Tickers",
        f"{overview['unique_tickers']:,}",
    )
    primary_metric_columns[1].metric(
        "Total OHLCV Records",
        f"{overview['total_records']:,}",
    )
    primary_metric_columns[2].metric(
        "Earliest Stored Record",
        overview["earliest_date"] or "—",
    )
    primary_metric_columns[3].metric(
        "Latest Expected Stored Session",
        overview["latest_expected_stored_session"] or "—",
    )

    health_metric_columns = st.columns(4)

    health_metric_columns[0].metric(
        "Tickers Current",
        f"{overview['current_tickers']:,}",
    )
    health_metric_columns[1].metric(
        "Tickers Stale",
        f"{overview['stale_tickers']:,}",
    )
    health_metric_columns[2].metric(
        "Tickers with Internal Gaps",
        f"{overview['tickers_with_internal_gaps']:,}",
    )
    health_metric_columns[3].metric(
        "Tickers with Large Price Moves",
        f"{overview['tickers_with_large_price_moves']:,}",
    )

    st.markdown("---")
    st.subheader("Ticker Inventory")

    universe_column, health_column, search_column = st.columns([1, 1, 2])

    with universe_column:
        universe_filter = st.selectbox(
            "Universe",
            options=[
                "Custom",
                "Sector",
                "Country",
                "Unassigned",
                "All",
            ],
            index=0,
            key="data_management_universe_filter",
        )

    with health_column:
        health_filter = st.selectbox(
            "Health Filter",
            options=[
                "All",
                "Current",
                "Stale",
                "Internal Gaps",
                "Large Price Moves",
            ],
            index=0,
            key="data_management_health_filter",
        )

    with search_column:
        ticker_search = st.text_input(
            "Search ticker",
            value="",
            key="data_management_ticker_search",
        ).strip().upper()

    filtered_inventory = []

    for row in inventory:
        buckets = row["buckets"]

        if universe_filter == "All":
            include_row = True
        elif universe_filter == "Unassigned":
            include_row = not buckets
        else:
            include_row = universe_filter in buckets

        if health_filter == "Current":
            include_row = (
                include_row
                and row["is_current"]
            )
        elif health_filter == "Stale":
            include_row = (
                include_row
                and row["is_stale"]
            )
        elif health_filter == "Internal Gaps":
            include_row = (
                include_row
                and row["internal_gaps"] > 0
            )
        elif health_filter == "Large Price Moves":
            include_row = (
                include_row
                and bool(row["large_price_moves"])
            )

        if ticker_search:
            include_row = (
                include_row
                and ticker_search in row["ticker"]
            )

        if include_row:
            filtered_inventory.append(row)

    display_rows = [
        {
            "Ticker": row["ticker"],
            "Bucket(s)": (
                ", ".join(row["buckets"])
                if row["buckets"]
                else "Unassigned"
            ),
            "Records": row["records"],
            "First Date": row["first_date"],
            "Last Date": row["last_date"],
            "Coverage": (
                f"{row['coverage']:.1f}%"
                if row["coverage"] is not None
                else "—"
            ),
            "Internal Gaps": row["internal_gaps"],
            "Status": row["status"] or "—",
            "Large Price Moves": (
                ", ".join(
                    event["date"]
                    for event in row["large_price_moves"]
                )
                if row["large_price_moves"]
                else "—"
            ),
        }
        for row in filtered_inventory
    ]

    st.caption(
        f"Showing {len(display_rows):,} of "
        f"{len(inventory):,} stored tickers."
    )

    if display_rows:
        inventory_df = pd.DataFrame(display_rows)

        st.dataframe(
            inventory_df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info(
            "No stored tickers match the selected universe and search."
        )

    st.caption(
        "**Coverage** — Percentage of expected NYSE sessions present "
        "between First Date and Last Date. "
        "**Internal Gaps** — Expected NYSE sessions missing between "
        "First Date and Last Date. "
        "**Status** — Current when Last Date reaches the latest session "
        "expected to be stored under the next-day daily-data policy; "
        "Stale when Last Date is earlier. "
        "**Large Price Moves** — Dates where Close changed by at least 25% "
        "versus the immediately preceding expected NYSE session. If that "
        "prior session is missing from the database, no Large Price Move "
        "is evaluated."
    )

    _render_data_management_universe_management(
        inventory=inventory,
    )

    st.markdown("---")
    st.subheader("Data Explorer")
    st.caption(
        "Inspect raw stored OHLCV records. Select stored ticker(s), a Start Date, "
        "and an End Date, then run the query. Calendar endpoints do not need to "
        "be NYSE trading sessions."
    )

    stored_tickers = [row["ticker"] for row in inventory]
    stored_ticker_set = set(stored_tickers)

    def _parse_data_explorer_tickers(raw_value):
        seen = set()
        parsed = []

        for value in str(raw_value or "").split(","):
            ticker = value.strip().upper()
            if not ticker or ticker in seen:
                continue
            seen.add(ticker)
            parsed.append(ticker)

        return parsed

    def _sync_data_explorer_end_date():
        selected_start_date = st.session_state.get(
            "data_management_explorer_start_date"
        )
        if selected_start_date is not None:
            st.session_state[
                "data_management_explorer_end_date"
            ] = selected_start_date

    def _add_data_explorer_browse_tickers(candidate_tickers):
        current_tickers = _parse_data_explorer_tickers(
            st.session_state.get(
                "data_management_explorer_ticker_input",
                "",
            )
        )
        selected_browse_tickers = [
            ticker
            for ticker in candidate_tickers
            if st.session_state.get(
                f"data_management_explorer_browse_{ticker}",
                False,
            )
        ]

        merged_tickers = []
        seen = set()
        for ticker in current_tickers + selected_browse_tickers:
            if ticker in seen:
                continue
            seen.add(ticker)
            merged_tickers.append(ticker)

        st.session_state[
            "data_management_explorer_ticker_input"
        ] = ", ".join(merged_tickers)

    if "data_management_explorer_ticker_input" not in st.session_state:
        st.session_state["data_management_explorer_ticker_input"] = ""

    ticker_input = st.text_input(
        "Ticker(s)",
        key="data_management_explorer_ticker_input",
        placeholder="AAPL, MSFT, NVDA",
        help=(
            "Enter one or more stored ticker symbols separated by commas. "
            "Ticker matching is case-insensitive."
        ),
    )

    parsed_tickers = _parse_data_explorer_tickers(ticker_input)
    invalid_tickers = [
        ticker
        for ticker in parsed_tickers
        if ticker not in stored_ticker_set
    ]
    selected_tickers = [
        ticker
        for ticker in parsed_tickers
        if ticker in stored_ticker_set
    ]

    if invalid_tickers:
        st.warning(
            "Not stored in database: "
            + ", ".join(invalid_tickers)
        )
    elif selected_tickers:
        st.caption(
            "Selected: "
            + " · ".join(selected_tickers)
        )

    with st.expander("Browse / Select Tickers", expanded=False):
        browse_universe = st.selectbox(
            "Universe",
            options=[
                "Custom",
                "Sector",
                "Country",
                "Unassigned",
                "All",
            ],
            index=0,
            key="data_management_explorer_browse_universe",
        )

        browse_candidates = []
        for row in inventory:
            buckets = row["buckets"]

            if browse_universe == "All":
                include_ticker = True
            elif browse_universe == "Unassigned":
                include_ticker = not buckets
            else:
                include_ticker = browse_universe in buckets

            if include_ticker:
                browse_candidates.append(row["ticker"])

        if browse_candidates:
            browse_columns = st.columns(4)
            for index, ticker in enumerate(browse_candidates):
                with browse_columns[index % len(browse_columns)]:
                    st.checkbox(
                        ticker,
                        key=f"data_management_explorer_browse_{ticker}",
                    )

            st.button(
                "Add Selected",
                key="data_management_explorer_add_selected",
                on_click=_add_data_explorer_browse_tickers,
                args=(tuple(browse_candidates),),
            )
        else:
            st.info(
                "No stored tickers are available in the selected universe."
            )

    if "data_management_explorer_start_date" not in st.session_state:
        st.session_state["data_management_explorer_start_date"] = None
    if "data_management_explorer_end_date" not in st.session_state:
        st.session_state["data_management_explorer_end_date"] = None

    start_date_column, end_date_column = st.columns(2)

    with start_date_column:
        explorer_start_date = st.date_input(
            "Start Date",
            key="data_management_explorer_start_date",
            on_change=_sync_data_explorer_end_date,
        )

    with end_date_column:
        explorer_end_date = st.date_input(
            "End Date",
            key="data_management_explorer_end_date",
        )

    run_explorer_query = st.button(
        "Run Query",
        key="data_management_explorer_run_query",
        type="primary",
    )

    if run_explorer_query:
        if invalid_tickers:
            st.error(
                "Remove or correct tickers that are not stored in the database "
                "before running the query."
            )
        elif not selected_tickers:
            st.error("Enter at least one ticker stored in the database.")
        elif explorer_start_date is None or explorer_end_date is None:
            st.error("Start Date and End Date are required.")
        elif explorer_start_date > explorer_end_date:
            st.error("Start Date cannot be later than End Date.")
        else:
            try:
                explorer_records = manager.get_ohlcv_records(
                    tickers=selected_tickers,
                    start_date=explorer_start_date,
                    end_date=explorer_end_date,
                )
                st.session_state[
                    "data_management_explorer_result"
                ] = explorer_records
                st.session_state[
                    "data_management_explorer_query"
                ] = {
                    "tickers": list(selected_tickers),
                    "start_date": explorer_start_date.isoformat(),
                    "end_date": explorer_end_date.isoformat(),
                }
            except Exception as exc:
                st.error(f"Unable to read OHLCV records: {exc}")

    explorer_query = st.session_state.get(
        "data_management_explorer_query"
    )
    explorer_records = st.session_state.get(
        "data_management_explorer_result"
    )

    if explorer_query is not None and explorer_records is not None:
        query_tickers = explorer_query.get("tickers", [])
        query_start_date = explorer_query.get("start_date")
        query_end_date = explorer_query.get("end_date")

        st.caption(
            "Last query: "
            f"{', '.join(query_tickers)} | "
            f"{query_start_date} → {query_end_date} | "
            f"{len(explorer_records):,} record(s)"
        )

        if explorer_records:
            explorer_columns = [
                "Ticker",
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "Adj Close",
                "Volume",
            ]
            explorer_df = pd.DataFrame(
                explorer_records,
                columns=explorer_columns,
            )

            st.dataframe(
                explorer_df,
                use_container_width=True,
                hide_index=True,
            )

            csv_bytes = explorer_df.to_csv(
                index=False
            ).encode("utf-8")
            st.download_button(
                "Download CSV",
                data=csv_bytes,
                file_name=(
                    "OHLCV_"
                    f"{query_start_date}_to_{query_end_date}.csv"
                ),
                mime="text/csv",
                key="data_management_explorer_download_csv",
            )
        else:
            st.info(
                "No stored OHLCV records were found for the selected "
                "ticker(s) and date range."
            )

    st.markdown("---")
    st.subheader("Ticker Diagnostics")
    st.caption(
        "Inspect detailed database-health evidence for one stored ticker."
    )

    diagnostics_ticker_options = [""] + stored_tickers
    selected_diagnostics_ticker = st.selectbox(
        "Ticker",
        options=diagnostics_ticker_options,
        index=0,
        key="data_management_diagnostics_ticker",
        format_func=lambda ticker: (
            "Select a stored ticker"
            if ticker == ""
            else ticker
        ),
    )

    def _set_explorer_from_diagnostics(
        ticker,
        start_date_value=None,
        end_date_value=None,
    ):
        st.session_state[
            "data_management_explorer_ticker_input"
        ] = str(ticker).strip().upper()

        if start_date_value is not None:
            st.session_state[
                "data_management_explorer_start_date"
            ] = date.fromisoformat(str(start_date_value))

        if end_date_value is not None:
            st.session_state[
                "data_management_explorer_end_date"
            ] = date.fromisoformat(str(end_date_value))

        st.session_state.pop(
            "data_management_explorer_result",
            None,
        )
        st.session_state.pop(
            "data_management_explorer_query",
            None,
        )

    maintenance_handoff_disabled = (
        st.session_state.get(
            _DATA_MANAGEMENT_MUTATION_PLAN_KEY
        )
        is not None
    )

    if not selected_diagnostics_ticker:
        st.info(
            "Select a stored ticker to view detailed "
            "database-health diagnostics."
        )
    else:
        try:
            diagnostics = manager.get_ticker_diagnostics(
                selected_diagnostics_ticker
            )
        except Exception as exc:
            st.error(
                f"Unable to read ticker diagnostics: {exc}"
            )
            diagnostics = None

        if diagnostics is not None:
            st.markdown(
                f"### Ticker Diagnostics — {diagnostics['ticker']}"
            )

            bucket_label = (
                " · ".join(diagnostics["buckets"])
                if diagnostics["buckets"]
                else "Unassigned"
            )
            st.caption(f"Bucket(s): {bucket_label}")

            summary_row_one = st.columns(4)
            summary_row_one[0].metric(
                "Records",
                f"{diagnostics['records']:,}",
            )
            summary_row_one[1].metric(
                "First Date",
                diagnostics["first_date"],
            )
            summary_row_one[2].metric(
                "Last Date",
                diagnostics["last_date"],
            )
            summary_row_one[3].metric(
                "Coverage",
                (
                    f"{diagnostics['coverage']:.1f}%"
                    if diagnostics["coverage"] is not None
                    else "—"
                ),
            )

            summary_row_two = st.columns(4)
            summary_row_two[0].metric(
                "Status",
                diagnostics["status"] or "—",
            )
            summary_row_two[1].metric(
                "Expected Through",
                diagnostics["latest_expected_stored_session"],
            )
            summary_row_two[2].metric(
                "Internal Gaps",
                f"{diagnostics['internal_gaps']:,}",
            )
            summary_row_two[3].metric(
                "Large Price Moves",
                f"{len(diagnostics['large_price_moves']):,}",
            )

            st.caption(
                "**Expected Through** = Latest Expected Stored Session "
                "under the next-calendar-day daily-data policy."
            )

            st.button(
                "Inspect This Ticker in Data Explorer",
                key=(
                    "data_management_diagnostics_open_explorer_"
                    f"{diagnostics['ticker']}"
                ),
                on_click=_set_explorer_from_diagnostics,
                args=(diagnostics["ticker"],),
            )

            st.markdown(
                "#### Duplicate Stored Key Diagnostics"
            )

            duplicate_stored_keys = diagnostics[
                "duplicate_stored_keys"
            ]

            if duplicate_stored_keys:
                st.warning(
                    f"{len(duplicate_stored_keys):,} duplicate stored "
                    "(Ticker, Date) key(s) were found, representing "
                    f"{diagnostics['duplicate_stored_excess_rows']:,} "
                    "excess physical row(s)."
                )

                duplicate_key_rows = [
                    {
                        "Date": duplicate_key[
                            "date"
                        ],
                        "Physical Rows": (
                            duplicate_key[
                                "physical_rows"
                            ]
                        ),
                        "Excess Rows": (
                            duplicate_key[
                                "excess_rows"
                            ]
                        ),
                    }
                    for duplicate_key
                    in duplicate_stored_keys
                ]

                st.dataframe(
                    pd.DataFrame(
                        duplicate_key_rows
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

                duplicate_dates = [
                    str(
                        duplicate_key[
                            "date"
                        ]
                    )
                    for duplicate_key
                    in duplicate_stored_keys
                ]

                duplicate_repair_request = {
                    "operation": (
                        "Repair Duplicate Stored Keys"
                    ),
                    "ticker": diagnostics[
                        "ticker"
                    ],
                    "origin": (
                        "Ticker Diagnostics"
                    ),
                    "reason": (
                        f"{len(duplicate_stored_keys):,} duplicate stored "
                        "(Ticker, Date) key(s) were detected, representing "
                        f"{diagnostics['duplicate_stored_excess_rows']:,} "
                        "excess physical row(s)."
                    ),
                    "suggested_start_date": (
                        duplicate_dates[0]
                    ),
                    "suggested_end_date": (
                        duplicate_dates[-1]
                    ),
                    "evidence": {
                        "duplicate_stored_key_count": (
                            len(
                                duplicate_stored_keys
                            )
                        ),
                        "duplicate_stored_excess_rows": (
                            diagnostics[
                                "duplicate_stored_excess_rows"
                            ]
                        ),
                        "duplicate_dates": list(
                            duplicate_dates
                        ),
                        "duplicate_stored_keys": [
                            dict(
                                duplicate_key
                            )
                            for duplicate_key
                            in duplicate_stored_keys
                        ],
                    },
                }

                st.info(
                    "Recommended maintenance: Repair Duplicate Stored Keys. "
                    "The repair will reacquire canonical yFinance history "
                    "covering the affected dates, but only the exact duplicate "
                    "(Ticker, Date) keys shown above are eligible for repair. "
                    "Every physical copy for an approved duplicate key will "
                    "be replaced atomically with one validated canonical "
                    "source observation."
                )

                st.button(
                    "Prepare Duplicate Repair",
                    key=(
                        "data_management_diagnostics_prepare_"
                        "duplicate_repair_"
                        f"{diagnostics['ticker']}"
                    ),
                    on_click=(
                        _prepare_data_management_maintenance_request
                    ),
                    args=(
                        duplicate_repair_request,
                    ),
                    disabled=maintenance_handoff_disabled,
                    help=(
                        "Prepare the canonical duplicate-repair workflow "
                        "below. This does not fetch source data, build a "
                        "Preview, approve changes, or modify the database."
                    ),
                )

                st.caption(
                    "Continue below in Acquire Market Data to review the "
                    "exact duplicate-key repair scope, then explicitly build "
                    "the Preview."
                )
            else:
                st.info(
                    "No duplicate stored (Ticker, Date) keys found."
                )

            st.caption(
                "Duplicate Stored Keys are detected by logical identity "
                "only: the same ticker and date appearing in more than one "
                "physical database row. OHLCV and Adj Close values do not "
                "need to match for the rows to be duplicates."
            )

            st.markdown("#### Internal Gap Diagnostics")

            internal_gap_dates = diagnostics[
                "internal_gap_dates"
            ]
            internal_gap_ranges = diagnostics[
                "internal_gap_ranges"
            ]

            if internal_gap_dates:
                st.write(
                    f"{len(internal_gap_dates):,} expected NYSE "
                    "session(s) are missing between First Date "
                    "and Last Date."
                )

                internal_gap_range_rows = []
                for gap_range in internal_gap_ranges:
                    start_value = gap_range["start_date"]
                    end_value = gap_range["end_date"]
                    range_label = (
                        start_value
                        if start_value == end_value
                        else f"{start_value} → {end_value}"
                    )

                    internal_gap_range_rows.append(
                        {
                            "Missing Range": range_label,
                            "Missing Sessions": (
                                gap_range["missing_sessions"]
                            ),
                        }
                    )

                st.dataframe(
                    pd.DataFrame(internal_gap_range_rows),
                    use_container_width=True,
                    hide_index=True,
                )

                with st.expander(
                    "Show exact missing sessions",
                    expanded=False,
                ):
                    st.dataframe(
                        pd.DataFrame(
                            {
                                "Missing Session": (
                                    internal_gap_dates
                                )
                            }
                        ),
                        use_container_width=True,
                        hide_index=True,
                    )

                repair_request = {
                    "operation": "Repair Missing",
                    "ticker": diagnostics["ticker"],
                    "origin": "Ticker Diagnostics",
                    "reason": (
                        f"{len(internal_gap_dates):,} expected NYSE "
                        "session(s) are missing inside stored coverage."
                    ),
                    "suggested_start_date": (
                        internal_gap_dates[0]
                    ),
                    "suggested_end_date": (
                        internal_gap_dates[-1]
                    ),
                    "evidence": {
                        "internal_gap_count": (
                            len(
                                internal_gap_dates
                            )
                        ),
                        "internal_gap_dates": (
                            list(
                                internal_gap_dates
                            )
                        ),
                        "internal_gap_ranges": [
                            dict(
                                gap_range
                            )
                            for gap_range
                            in internal_gap_ranges
                        ],
                    },
                }

                st.info(
                    "Recommended maintenance: Repair Missing. "
                    "This operation reacquires the envelope containing the "
                    "known Internal Gaps while preserving existing stored rows."
                )

                st.button(
                    "Prepare Repair Missing",
                    key=(
                        "data_management_diagnostics_prepare_repair_"
                        f"{diagnostics['ticker']}"
                    ),
                    on_click=(
                        _prepare_data_management_maintenance_request
                    ),
                    args=(
                        repair_request,
                    ),
                    disabled=maintenance_handoff_disabled,
                    help=(
                        "Prepare the existing Repair Missing workflow below. "
                        "This does not fetch source data, build a Preview, "
                        "approve changes, or modify the database."
                    ),
                )

                st.caption(
                    "Continue below in Acquire Market Data to review the "
                    "prepared ticker and repair scope, then explicitly build "
                    "the Preview."
                )
            else:
                st.info(
                    "No missing expected NYSE sessions were found "
                    "between First Date and Last Date."
                )

            st.markdown("#### Staleness Diagnostics")

            missing_tail_dates = diagnostics[
                "missing_tail_dates"
            ]
            missing_tail_ranges = diagnostics[
                "missing_tail_ranges"
            ]

            staleness_rows = [
                {
                    "Field": "Last Stored Date",
                    "Value": diagnostics["last_date"],
                },
                {
                    "Field": "Latest Expected Stored Session",
                    "Value": diagnostics[
                        "latest_expected_stored_session"
                    ],
                },
                {
                    "Field": "Missing Tail Sessions",
                    "Value": len(missing_tail_dates),
                },
                {
                    "Field": "Status",
                    "Value": diagnostics["status"] or "—",
                },
            ]

            st.dataframe(
                pd.DataFrame(staleness_rows),
                use_container_width=True,
                hide_index=True,
            )

            if diagnostics["is_current"]:
                st.info(
                    "This ticker reaches the latest session currently "
                    "expected to be stored."
                )
            elif diagnostics["is_stale"]:
                if missing_tail_ranges:
                    missing_tail_range_rows = []

                    for tail_range in missing_tail_ranges:
                        start_value = tail_range["start_date"]
                        end_value = tail_range["end_date"]
                        range_label = (
                            start_value
                            if start_value == end_value
                            else f"{start_value} → {end_value}"
                        )

                        missing_tail_range_rows.append(
                            {
                                "Missing Tail Range": range_label,
                                "Missing Sessions": (
                                    tail_range[
                                        "missing_sessions"
                                    ]
                                ),
                            }
                        )

                    st.dataframe(
                        pd.DataFrame(
                            missing_tail_range_rows
                        ),
                        use_container_width=True,
                        hide_index=True,
                    )

                if missing_tail_dates:
                    try:
                        update_start_date = (
                            date.fromisoformat(
                                str(
                                    diagnostics[
                                        "last_date"
                                    ]
                                )
                            )
                            + timedelta(days=1)
                        ).isoformat()
                    except Exception:
                        update_start_date = None

                    if update_start_date is not None:
                        update_request = {
                            "operation": "Update to Current",
                            "ticker": diagnostics["ticker"],
                            "origin": "Ticker Diagnostics",
                            "reason": (
                                f"{len(missing_tail_dates):,} expected NYSE "
                                "session(s) are missing after Last Date."
                            ),
                            "suggested_start_date": (
                                update_start_date
                            ),
                            "suggested_end_date": (
                                diagnostics[
                                    "latest_expected_stored_session"
                                ]
                            ),
                            "evidence": {
                                "missing_tail_count": (
                                    len(
                                        missing_tail_dates
                                    )
                                ),
                                "missing_tail_dates": (
                                    list(
                                        missing_tail_dates
                                    )
                                ),
                                "missing_tail_ranges": [
                                    dict(
                                        tail_range
                                    )
                                    for tail_range
                                    in missing_tail_ranges
                                ],
                            },
                        }

                        st.info(
                            "Recommended maintenance: Update to Current. "
                            "This operation acquires the stale tail after the "
                            "current Last Date through the Latest Expected "
                            "Stored Session while preserving existing rows."
                        )

                        st.button(
                            "Prepare Update to Current",
                            key=(
                                "data_management_diagnostics_prepare_update_"
                                f"{diagnostics['ticker']}"
                            ),
                            on_click=(
                                _prepare_data_management_maintenance_request
                            ),
                            args=(
                                update_request,
                            ),
                            disabled=maintenance_handoff_disabled,
                            help=(
                                "Prepare the existing Update to Current "
                                "workflow below. This does not fetch source "
                                "data, build a Preview, approve changes, or "
                                "modify the database."
                            ),
                        )

                        st.caption(
                            "Continue below in Acquire Market Data to review "
                            "the prepared ticker and stale-tail scope, then "
                            "explicitly build the Preview."
                        )
            else:
                st.warning(
                    "The ticker's Last Date does not fit the normal "
                    "Current/Stale relationship to the Latest Expected "
                    "Stored Session. Review the stored dates."
                )

            st.caption(
                "Missing Tail Sessions occur after Last Date and are "
                "not counted as Internal Gaps."
            )

            st.markdown(
                "#### Large Price Move Diagnostics"
            )

            large_price_moves = diagnostics[
                "large_price_moves"
            ]

            if large_price_moves:
                st.write(
                    f"{len(large_price_moves):,} Large Price Move "
                    "event(s) require inspection."
                )

                large_move_rows = [
                    {
                        "Date": event["date"],
                        "Prior Expected Session": (
                            event["prior_date"]
                        ),
                        "Prior Close": (
                            f"{event['prior_close']:.2f}"
                        ),
                        "Close": f"{event['close']:.2f}",
                        "Change": (
                            f"{event['change_pct']:+.2f}%"
                        ),
                    }
                    for event in large_price_moves
                ]

                st.dataframe(
                    pd.DataFrame(large_move_rows),
                    use_container_width=True,
                    hide_index=True,
                )

                for event in large_price_moves:
                    event_date = date.fromisoformat(
                        str(
                            event[
                                "date"
                            ]
                        )
                    )

                    explorer_start_date = (
                        event_date
                        - timedelta(days=2)
                    ).isoformat()

                    explorer_end_date = (
                        event_date
                        + timedelta(days=2)
                    ).isoformat()

                    st.button(
                        (
                            f"Inspect {event['date']} "
                            "in Data Explorer"
                        ),
                        key=(
                            "data_management_diagnostics_lpm_"
                            f"{diagnostics['ticker']}_"
                            f"{event['date']}"
                        ),
                        on_click=_set_explorer_from_diagnostics,
                        args=(
                            diagnostics["ticker"],
                            explorer_start_date,
                            explorer_end_date,
                        ),
                        help=(
                            "Open Data Explorer for the Large Price Move "
                            "event date plus two calendar days before and "
                            "two calendar days after."
                        ),
                    )
            else:
                st.info("No Large Price Moves found.")

            st.caption(
                "Large Price Moves are dates where Close changed by "
                "at least 25% versus the immediately preceding expected "
                "NYSE session. They are inspection warnings, not "
                "automatic evidence of bad data or a corporate action."
            )

    _render_data_management_acquisition_controls(
        inventory=inventory,
        database_manager=manager,
        latest_expected_stored_session=(
            overview[
                "latest_expected_stored_session"
            ]
        ),
    )

    _render_data_management_reconciliation_controls(
        inventory=inventory,
        latest_expected_stored_session=(
            overview[
                "latest_expected_stored_session"
            ]
        ),
    )

    _render_data_management_manual_entry_controls(
        latest_expected_stored_session=(
            overview[
                "latest_expected_stored_session"
            ]
        ),
    )

    _render_data_management_deletion_controls(
        inventory=inventory,
    )

    _render_data_management_audit_history(
        mutation_manager=mutation_manager,
    )

    _render_data_management_mutation_workflow()


def main():
    """Main application function with page navigation"""
    # Page config
    st.set_page_config(
        page_title="Stock Performance Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Background update: Pre-load technical indicators for CUSTOM_DEFAULT tickers
    if 'technical_background_updated' not in st.session_state:
        custom_default_tickers = get_tickers_only(CUSTOM_DEFAULT)

        with st.spinner(f'Refreshing technical indicators for {len(custom_default_tickers)} tickers...'):
            for ticker in custom_default_tickers:
                try:
                    # Calculate latest indicators
                    st.session_state.tech_calculator.calculate_comprehensive_analysis(
                        ticker=ticker,
                        save_to_db=True
                    )
                    # Calculate 52-week price extremes
                    st.session_state.tech_calculator.calculate_52_week_analysis(ticker)
                except Exception as e:
                    # Silent failure - don't break app load for individual ticker failures
                    pass
        st.session_state.technical_background_updated = True
    
    # Page navigation in sidebar
    st.sidebar.title("📊 Navigation")

    page_options = [
        'performance_heatmaps',
        'technical_analysis',
        'stock_comparison',
        'data_management',
    ]

    st.session_state.selected_page = st.sidebar.selectbox(
        "Choose Dashboard:",
        options=page_options,
        format_func=lambda x: {
            'performance_heatmaps': '📈 Performance Heatmaps',
            'technical_analysis': '🎯 Technical Analysis',
            'stock_comparison': '📋 Stock Comparison',
            'data_management': '🗄️ Data Management',
        }[x],
        index=page_options.index(
            st.session_state.selected_page
        ),
        key='page_navigation'
    )
    
    # Route to appropriate dashboard
    if st.session_state.selected_page == 'performance_heatmaps':
        show_performance_heatmaps()
    elif st.session_state.selected_page == 'technical_analysis':
        show_technical_analysis_dashboard()
    elif st.session_state.selected_page == 'stock_comparison':
        show_stock_comparison_dashboard()
    elif st.session_state.selected_page == 'data_management':
        show_data_management()

if __name__ == "__main__":
    main()
