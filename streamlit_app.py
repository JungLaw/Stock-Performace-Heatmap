# Stamp: Sat, June 20, 2026 4:18 PM
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
from datetime import datetime, timedelta
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
    get_window_names,
    resolve_row_selection,
)
from ui.rolling_heatmap_adapter import (
    INDICATOR_DEFS,
    build_plotly_heatmap_inputs,
)

# Developer-only diagnostic controls.
# Keep False for normal app use. Set True temporarily when running D3-C
# tail-buffer equivalence checks.
SCD_SHOW_TAIL_BUFFER_DIAGNOSTIC = False

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

def initialize_session_state():
    """Initialize session state variables"""
    if 'performance_data' not in st.session_state:
        st.session_state.performance_data = None
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None
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
        st.session_state.scd_custom_rows = list(RH_CUSTOM_DEFAULT)

    if 'scd_selected_category' not in st.session_state:
        st.session_state.scd_selected_category = None

    if 'scd_selected_scope' not in st.session_state:
        st.session_state.scd_selected_scope = 'All'

    if 'scd_selected_window' not in st.session_state:
        st.session_state.scd_selected_window = 'All'

    if 'scd_selected_family' not in st.session_state:
        st.session_state.scd_selected_family = 'All'

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

    Main Indicators are derived from the existing Rolling Heatmap Custom
    default membership so they stay aligned with curated Custom changes.
    """
    return [
        row_key
        for row_key in RH_CUSTOM_DEFAULT
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
        mode_options = ["Custom", "Category", "Preset"]

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
                "resets to the catalog-owned Rolling Heatmap Custom default."
            )
        with cc2:
            if st.button(
                "Restore Default Custom",
                key="scd_restore_default_custom_rows",
                use_container_width=True,
            ):
                st.session_state.scd_custom_rows = list(RH_CUSTOM_DEFAULT)
                st.session_state.pop("scd_custom_selected_row_keys", None)
                st.rerun()

        resolved_row_keys = resolve_row_selection(
            selection_mode="Custom",
            custom_rows=st.session_state.get(
                "scd_custom_rows",
                list(RH_CUSTOM_DEFAULT),
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

    if result_cell_writes:
        summary_parts.append(f"result-cell writes={result_cell_writes}")

    if result_cell_hits:
        summary_parts.append(f"result-cell reuse={result_cell_hits}")

    if result_cell_misses:
        summary_parts.append(f"result-cell misses={result_cell_misses}")

    if ticker_calculations_skipped:
        summary_parts.append(
            f"ticker calculations skipped={ticker_calculations_skipped}"
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
        f"{cache_stats.get('today_cell_tickers_refreshed', 0)}."
    )


def _clear_scd_session_cache() -> None:
    """
    Clear SCD session-only transport caches.

    This does not clear the currently rendered matrix. The next build will
    repopulate caches through the existing SCD fetch path.
    """
    st.session_state.scd_payload_cache = {}
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

    if 'scd_hover_ohlcv_cache' not in st.session_state:
        st.session_state.scd_hover_ohlcv_cache = {}

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

        return {
            "rolling_payload": rolling_payload,
            "indicator_context_df": cached_df.copy() if isinstance(cached_df, pd.DataFrame) else cached_df,
            "source": "cache",
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
        }

    if rolling_hit:
        # Rare partial-cache case: keep the cached rolling payload and only
        # fill the missing hover/context dataframe through the legacy fallback.
        stats["rolling_hits"] += 1
        rolling_payload = st.session_state.scd_payload_cache[rolling_cache_key]
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

    if isinstance(rolling_payload, dict) and rolling_payload:
        st.session_state.scd_payload_cache[rolling_cache_key] = rolling_payload

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
        source="bundled",
    )

    return {
        "rolling_payload": rolling_payload,
        "indicator_context_df": indicator_context_df,
        "source": "bundled",
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


def _build_scd_selected_row_compute_config(row_key: str) -> Dict[str, Any]:
    """
    Build a minimal diagnostic compute config for one selected SCD row.

    D3-D2 starts with RSI and SMA only:
    - RSI_<len>: compute only RSI_<len>
    - SMA_<len>: compute SMA_<len>, ATR/ATRP_<len>, and SMA slope aliases

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

    if engine_indicator == "SMA":
        length = _parse_scd_single_int_param_key(param_key)
        return {
            "SMA": [length],
            "ATR": [length],
            "ATRP": [length],
            "SLOPE": {
                "window": 14,
                "method": "linreg",
                "emit_aliases": True,
                "vwma_anchor": 20,
                "hma_anchor": 21,
                "families": ["SMA"],
                "canonical_pattern": "{base_col}_slope__{method}_{window}",
                "compatibility_aliases": [
                    "SMA_<len>_slope",
                    "EMA_<len>_slope",
                    "VWMA_slope",
                    "HMA_slope",
                ],
            },
        }

    raise ValueError(
        "D3-D2 selected-row numeric config diagnostic currently supports "
        f"RSI and SMA rows only. Got row_key={row_key!r}, "
        f"engine_indicator={engine_indicator!r}."
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
) -> Dict[str, Any]:
    """
    Refresh only today's visible Single Indicator cells in an existing matrix.

    This does not compute one-row indicators. It force-refreshes the existing
    lookback-aware SCD bundled payload path for each matrix ticker, then splices
    only today's rebuilt date/ticker cell back into the current matrix.

    Preserved:
    - historical matrix cells
    - selected row identity
    - selected ticker identity
    - chart/detail/export consumers of the matrix
    - existing acquisition/scoring/persistence boundaries
    """
    started_at = time.perf_counter()

    if not isinstance(matrix, dict) or matrix.get("view") != "single_indicator_time_series":
        return matrix

    live_date_key = _get_scd_current_live_date_key()
    if not live_date_key:
        refreshed_matrix = dict(matrix)
        refreshed_matrix["last_live_refresh"] = {
            "status": "skipped",
            "message": "Today is not a US trading day.",
            "date": None,
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
        "tickers_refreshed": [],
        "errors": [],
        "total_seconds": None,
    }

    if live_date_key not in refreshed_matrix["cells"]:
        refreshed_matrix["cells"][live_date_key] = {}

    for ticker in tickers:
        ticker_started_at = time.perf_counter()

        try:
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

            existing_status = dict(refreshed_matrix["ticker_status"].get(ticker, {}))
            existing_status.update(
                {
                    "live_refresh_status": refreshed_cell.get("status", "unknown"),
                    "live_refresh_date": live_date_key,
                    "live_refresh_bundle_source": bundle_source,
                    "live_refresh_seconds": round(
                        time.perf_counter() - ticker_started_at,
                        3,
                    ),
                }
            )
            refreshed_matrix["ticker_status"][ticker] = existing_status
            refresh_report["tickers_refreshed"].append(ticker)

        except Exception as e:
            message = f"{ticker}: {e}"
            refresh_report["errors"].append(message)

            existing_status = dict(refreshed_matrix["ticker_status"].get(ticker, {}))
            existing_status.update(
                {
                    "live_refresh_status": "error",
                    "live_refresh_date": live_date_key,
                    "live_refresh_error": message,
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
        _mark_scd_live_cells_as_of(
            matrix=matrix,
            date_key=live_date_key,
            as_of=datetime.now(),
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
        _mark_scd_live_cells_as_of(
            matrix=matrix,
            date_key=live_date_key,
            as_of=datetime.now(),
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

    for key in [
        "ma_context_block",
        "delta_abs_fmt",
        "delta_pct_suffix",
        "trend_line",
        "adx_context_block",
        "signal_line",
        "macd_context_block",
        "stoch_context_block",
        "dpo_context_block",
        "bullbear_context_block",
        "rule_block",
        "notes_block",
        "definition_block",
        "how_to_read_block",
        "band_context_block",
        "volume_block",
        "volume_vs_avg_block",
    ]:
        custom.setdefault(key, "")

    custom["ticker"] = ticker
    custom["row_key"] = row_key
    custom["status"] = cell.get("status")

    payload_hover = cell.get("hover")
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

            text_row.append(_format_scd_heatmap_text(row_key, cell))
            custom_row.append(
                _build_scd_hover_customdata(
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

    hovertemplate = (
        "<b>%{customdata.display_name}</b><br>"
        "Ticker: %{customdata.ticker}<br>"
        "Date: %{customdata.date}<br>"
        "<br>"
        "Value: %{customdata.formatted_value}<br>"
        "Δ vs prior day: %{customdata.delta_abs_fmt}"
        "%{customdata.delta_pct_suffix}<br>"
        "%{customdata.trend_line}"
        "%{customdata.ma_context_block}"
        "%{customdata.adx_context_block}"
        "%{customdata.signal_line}"
        "%{customdata.macd_context_block}"
        "%{customdata.stoch_context_block}"
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

    row_count = max(len(y_labels), 1)
    dynamic_height = max(450, 30 * row_count + 160)

    fig.update_layout(
        title="",
        margin=dict(l=170, r=20, t=30, b=40),
        height=dynamic_height,
    )

    fig.update_xaxes(side="top", type="category")
    fig.update_yaxes(
        autorange="reversed",
        automargin=True,
        tickfont=dict(size=11),
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
            delta_abs_txt = str(price_customdata.get("delta_abs_fmt", "") or "").strip()

        delta_pct_txt = ""
        try:
            delta_pct_txt = f" ({float(delta_pct):+.2f}%)"
        except (TypeError, ValueError):
            delta_pct_txt = str(price_customdata.get("delta_pct_suffix", "") or "").strip()

        combined = f"{delta_abs_txt}{delta_pct_txt}".strip()
        return "" if combined == "-" else combined

    price_formatted = _format_price_value_for_single_hover()
    price_delta = _format_price_delta_for_single_hover()
    price_trend = _derive_scd_price_trend_label(price_customdata)

    custom["single_price_value_suffix"] = (
        f" | Price: {price_formatted}" if price_formatted else ""
    )
    custom["single_price_delta_suffix"] = (
        f" | Price: {price_delta}" if price_delta else ""
    )

    indicator_trend = custom.get("trend") or ""
    if indicator_trend or price_trend:
        custom["single_combined_trend_line"] = (
            f"Trend: {indicator_trend or 'N/A'}"
            f"{f' | Price: {price_trend}' if price_trend else ''}<br>"
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

            try:
                z_row.append(float(score) if score is not None else None)
            except (TypeError, ValueError):
                z_row.append(None)

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

    hovertemplate = (
        "<b>%{customdata.display_name}</b><br>"
        "Ticker: %{customdata.ticker}<br>"
        "Date: %{customdata.date}<br>"
        "<br>"
        "Value: %{customdata.formatted_value}"
        "%{customdata.single_price_value_suffix}<br>"
        "Δ vs prior day: %{customdata.delta_abs_fmt}"
        "%{customdata.delta_pct_suffix}"
        "%{customdata.single_price_delta_suffix}<br>"
        "%{customdata.single_combined_trend_line}"
        "%{customdata.ma_context_block}"
        "%{customdata.adx_context_block}"
        "%{customdata.signal_line}"
        "%{customdata.macd_context_block}"
        "%{customdata.stoch_context_block}"
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

    dynamic_height = max(450, 24 * max(len(dates), 1) + 180)

    fig.update_layout(
        title=f"{row_label}",
        margin=dict(l=110, r=20, t=80, b=80),
        height=dynamic_height,
    )

    fig.update_xaxes(side="top", type="category")
    fig.update_yaxes(
        autorange="reversed",
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
    dates = list(matrix.get("dates", []))
    cells = matrix.get("cells", {})

    raw_series: dict[str, list[Optional[float]]] = {}

    for ticker in visible_tickers:
        values: list[Optional[float]] = []

        for date_key in dates:
            cell = cells.get(date_key, {}).get(ticker, {})
            if value_mode == "Score":
                values.append(_coerce_scd_chart_numeric_value(cell.get("score")))
            else:
                values.append(_coerce_scd_chart_numeric_value(cell.get("value")))

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


def _get_scd_single_chart_hover_fields(
    *,
    matrix: Dict[str, Any],
    ticker: str,
    date_key: str,
    chart_value: Optional[float],
    value_mode: str,
) -> list[Any]:
    """Return compact hover customdata for one Single Indicator chart point."""
    row_key = str(matrix.get("row_key", ""))
    cells = matrix.get("cells", {})
    cell = cells.get(date_key, {}).get(ticker, {})

    price_cell = cell.get("price_cell") if isinstance(cell, dict) else None
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

    return [
        str(date_key),
        _format_scd_heatmap_text(row_key, cell),
        cell.get("signal") if isinstance(cell, dict) else None,
        chart_value,
        price_value,
        price_delta,
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

    # STEP 3 & 4: Filter and Add Tickers for Selected Bucket
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"🔧 Modify/Filter {bucket_names[st.session_state.selected_bucket]}")
    
    # Import needed functions
    from config.assets import COUNTRY_ETFS, SECTOR_ETFS, get_tickers_only
    
    # Initialize bucket_save_to_db variable
    bucket_save_to_db = True  # Default value
    
    if st.session_state.selected_bucket == 'country':
        # Initialize visible tickers if empty
        all_country_tickers = get_tickers_only(COUNTRY_ETFS)
        if not st.session_state.country_visible_tickers:
            st.session_state.country_visible_tickers = all_country_tickers.copy()
        
        # Country ETF filtering
        with st.sidebar.expander("📋 Show/Hide Country ETFs", expanded=False):
            for ticker, display_name in COUNTRY_ETFS:
                is_visible = ticker in st.session_state.country_visible_tickers
                if st.checkbox(
                    f"{display_name} ({ticker})",
                    value=is_visible,
                    key=f"filter_country_{ticker}"
                ):
                    if ticker not in st.session_state.country_visible_tickers:
                        st.session_state.country_visible_tickers.append(ticker)
                else:
                    if ticker in st.session_state.country_visible_tickers:
                        st.session_state.country_visible_tickers.remove(ticker)
            
            st.caption(f"Showing: {len(st.session_state.country_visible_tickers)}/{len(all_country_tickers)} country ETFs")
        
        # Add new Country ETF
        with st.sidebar.expander("➕ Add New Country ETF", expanded=False):
            new_country_ticker = st.text_input(
                "Country ETF Ticker:",
                key="new_country_ticker_step4",
                placeholder="e.g., EWK"
            ).upper().strip()
            
            new_country_name = st.text_input(
                "Display Name:",
                key="new_country_name_step4", 
                placeholder="e.g., Belgium"
            ).strip()
            
            # FIXED: Capture the bucket-specific toggle value
            bucket_save_to_db = st.checkbox(
                "💾 Save to database",
                value=True,
                key="save_country_to_db",
                help="Save historical data for faster future access"
            )
            
            if st.button("Add Country ETF", key="add_country_step4"):
                if new_country_ticker and new_country_name:
                    if new_country_ticker not in st.session_state.country_visible_tickers:
                        st.session_state.country_visible_tickers.append(new_country_ticker)
                        st.success(f"✅ Added {new_country_name} ({new_country_ticker}) to country ETFs")
                    else:
                        st.warning(f"⚠️ {new_country_ticker} already in your list")
                else:
                    st.error("❌ Please enter both ticker and display name")
    
    elif st.session_state.selected_bucket == 'sector':
        # Initialize visible tickers if empty
        all_sector_tickers = get_tickers_only(SECTOR_ETFS)
        if not st.session_state.sector_visible_tickers:
            st.session_state.sector_visible_tickers = all_sector_tickers.copy()
        
        # Sector ETF filtering
        with st.sidebar.expander("📋 Show/Hide Sector ETFs", expanded=False):
            for ticker, display_name in SECTOR_ETFS:
                is_visible = ticker in st.session_state.sector_visible_tickers
                if st.checkbox(
                    f"{display_name} ({ticker})",
                    value=is_visible,
                    key=f"filter_sector_{ticker}"
                ):
                    if ticker not in st.session_state.sector_visible_tickers:
                        st.session_state.sector_visible_tickers.append(ticker)
                else:
                    if ticker in st.session_state.sector_visible_tickers:
                        st.session_state.sector_visible_tickers.remove(ticker)
            
            st.caption(f"Showing: {len(st.session_state.sector_visible_tickers)}/{len(all_sector_tickers)} sector ETFs")
        
        # Add new Sector ETF
        with st.sidebar.expander("➕ Add New Sector ETF", expanded=False):
            new_sector_ticker = st.text_input(
                "Sector ETF Ticker:",
                key="new_sector_ticker_step4",
                placeholder="e.g., JETS"
            ).upper().strip()
            
            new_sector_name = st.text_input(
                "Display Name:",
                key="new_sector_name_step4",
                placeholder="e.g., Airlines"
            ).strip()
            
            # FIXED: Capture the bucket-specific toggle value
            bucket_save_to_db = st.checkbox(
                "💾 Save to database",
                value=True,
                key="save_sector_to_db",
                help="Save historical data for faster future access"
            )
            
            if st.button("Add Sector ETF", key="add_sector_step4"):
                if new_sector_ticker and new_sector_name:
                    if new_sector_ticker not in st.session_state.sector_visible_tickers:
                        st.session_state.sector_visible_tickers.append(new_sector_ticker)
                        st.success(f"✅ Added {new_sector_name} ({new_sector_ticker}) to sector ETFs")
                    else:
                        st.warning(f"⚠️ {new_sector_ticker} already in your list")
                else:
                    st.error("❌ Please enter both ticker and display name")
    
    else:  # custom bucket
        # Initialize visible tickers if empty.
        # CUSTOM_DEFAULT may contain either plain ticker strings or
        # (ticker, display_name) tuples; session state must store ticker strings only.
        custom_default_tickers = get_tickers_only(CUSTOM_DEFAULT)

        if not st.session_state.custom_visible_tickers:
            st.session_state.custom_visible_tickers = custom_default_tickers.copy()
        
        # Custom stock filtering
        with st.sidebar.expander("📋 Show/Hide Custom Stocks", expanded=True):
            for item in CUSTOM_DEFAULT:
                if isinstance(item, tuple):
                    ticker, display_name = item
                else:
                    ticker, display_name = item, item

                is_visible = ticker in st.session_state.custom_visible_tickers
                if st.checkbox(
                    f"{display_name} ({ticker})",
                    value=is_visible,
                    key=f"filter_custom_{ticker}"
                ):
                    if ticker not in st.session_state.custom_visible_tickers:
                        st.session_state.custom_visible_tickers.append(ticker)
                else:
                    if ticker in st.session_state.custom_visible_tickers:
                        st.session_state.custom_visible_tickers.remove(ticker)
            
            st.caption(
                f"Showing: {len(st.session_state.custom_visible_tickers)}/"
                f"{len(custom_default_tickers)} custom stocks"
            )
        
        # Add new Custom Stocks
        with st.sidebar.expander("➕ Add Custom Stocks", expanded=False):
            ticker_input = st.text_area(
                "Add Ticker(s):",
                key="custom_ticker_input_step4",
                placeholder="Single: TSLA\nMultiple: AAPL, MSFT, GOOGL\n(comma or line separated)",
                height=80
            )
            
            # FIXED: Capture the bucket-specific toggle value
            bucket_save_to_db = st.checkbox(
                "💾 Save to database",
                value=st.session_state.save_custom_to_database,
                key="save_custom_to_db_step4",
                help="Save historical data for faster future access"
            )
            
            if st.button("Add Ticker(s)", key="add_custom_step4"):
                if ticker_input.strip():
                    # Parse input
                    parsed_tickers = []
                    for line in ticker_input.replace(',', '\n').split('\n'):
                        ticker = line.strip().upper()
                        if ticker and ticker not in parsed_tickers:
                            parsed_tickers.append(ticker)
                    
                    # Add tickers
                    added_count = 0
                    for ticker in parsed_tickers:
                        if ticker not in st.session_state.custom_visible_tickers:
                            st.session_state.custom_visible_tickers.append(ticker)
                            added_count += 1
                    
                    if added_count > 0:
                        st.success(f"✅ Added {added_count} ticker{'s' if added_count != 1 else ''}")
                    if added_count < len(parsed_tickers):
                        skipped = len(parsed_tickers) - added_count
                        st.info(f"ℹ️ {skipped} ticker{'s' if skipped != 1 else ''} already in list")
                else:
                    st.error("❌ Enter at least one ticker symbol")

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
    
    # Refresh button
    st.sidebar.subheader("🔄 Data Refresh")
    refresh_button = st.sidebar.button(
        "🔄 Refresh Data",
        help="Fetch latest market data",
        use_container_width=True
    )
    
    # FIXED: Return the actual bucket-specific database toggle value
    return {
        'group': asset_group,
        'group_name': group_name,
        'tickers': final_tickers,
        'period': selected_period,
        'period_name': selected_period_name,
        'refresh': refresh_button,
        'database_save': bucket_save_to_db,  # ← NOW USES BUCKET-SPECIFIC TOGGLE
        'analysis_mode': st.session_state.selected_analysis_mode
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
            performance_data = calculator.calculate_performance_for_group(tickers, period, save_to_db=save_to_db)
            
            # Show database usage statistics
            summary = calculator.get_performance_summary(performance_data)
            
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

def fetch_volume_data(tickers, period, save_to_db: bool = True):
    """Fetch volume data with progress tracking and database usage reporting"""
    with st.spinner(f"Fetching volume data for {len(tickers)} tickers..."):
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        volume_calculator = st.session_state.volume_calculator
        
        # Use the group calculation method for better efficiency
        status_text.text(f"Processing {len(tickers)} tickers using database-first approach...")
        
        try:
            volume_data = volume_calculator.calculate_volume_performance_for_group(tickers, period)
            
            # Show database usage statistics
            valid_count = len([v for v in volume_data if not v.get('error', False)])
            error_count = len([v for v in volume_data if v.get('error', False)])
            database_usage = len([v for v in volume_data if v.get('data_source') == 'database'])
            
            progress_bar.progress(1.0)
            status_text.empty()
            
            # Display efficiency information
            if database_usage > 0:
                cache_rate = database_usage / valid_count * 100 if valid_count > 0 else 0
                st.success(
                    f"✅ Volume data fetched successfully! "
                    f"Database cache used for {database_usage}/{valid_count} tickers "
                    f"({cache_rate:.0f}% cache hit rate)"
                )
            else:
                st.info("ℹ️ Volume data fetched from yfinance (no database cache available)")
            
        except Exception as e:
            st.error(f"Error fetching volume data: {str(e)}")
            volume_data = []
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        return volume_data

def display_summary_stats(performance_data):
    """Display summary statistics"""
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
    if stats['best_performer'] and stats['worst_performer']:
        col1, col2 = st.columns(2)
        
        with col1:
            best = stats['best_performer']
            # Handle both price and volume data structures
            if 'percentage_change' in best:
                performance_value = best['percentage_change']
            elif 'volume_change' in best:
                performance_value = best['volume_change']
            else:
                performance_value = 0.0
            
            st.success(
                f"🏆 Best: **{best['ticker']}** "
                f"({performance_value:+.2f}%)"
            )
        
        with col2:
            worst = stats['worst_performer']
            # Handle both price and volume data structures
            if 'percentage_change' in worst:
                performance_value = worst['percentage_change']
            elif 'volume_change' in worst:
                performance_value = worst['volume_change']
            else:
                performance_value = 0.0
            
            st.error(
                f"📉 Worst: **{worst['ticker']}** "
                f"({performance_value:+.2f}%)"
            )

def display_heatmap(performance_data, title, asset_group=None):
    """Display the main heatmap visualization"""
    generator = st.session_state.heatmap_generator
    
    # Create heatmap with asset group information
    fig = generator.create_treemap(
        performance_data=performance_data,
        title=title,
        width=1200,
        height=700,
        asset_group=asset_group
    )
    
    # Display with full width
    st.plotly_chart(fig, use_container_width=True)

def generate_ma_comment(ticker, period, ma_type, current_price, ma_value, price_vs_ma):
    """Generate contextual comment for moving average"""
    # Determine if price is above or below MA
    if price_vs_ma > 0:
        direction = "above"
        fall_pct = abs((ma_value - current_price) / current_price * 100)
        comment = f"{ticker} is {price_vs_ma:+.1f}% above its {period}D {ma_type}. It has to fall {fall_pct:.1f}% to reach it."
    else:
        direction = "below"
        rise_pct = abs((ma_value - current_price) / current_price * 100)
        comment = f"{ticker} is {price_vs_ma:.1f}% below its {period}D {ma_type}. It has to rise {rise_pct:.1f}% to reach it."
    
    return comment

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
    """Display professional moving averages table with color coding and comments"""
    if not ma_data or ma_data.get('error'):
        st.error(f"Error loading moving averages: {ma_data.get('message', 'Unknown error')}")
        return
    
    # Extract data
    ticker = ma_data['ticker']
    current_price = ma_data['current_price']
    calc_date = ma_data['calculation_date']
    periods_data = ma_data['periods']
    
    # Display current price header
    st.caption(f"Current Price: ${current_price:.2f} ({calc_date})")
    
    # Prepare table data
    table_rows = []
    periods = [5, 9, 10, 20, 21, 50, 100, 200]
    
    for period in periods:
        period_key = f'MA{period}'
        if period_key not in periods_data:
            continue
        
        sma_data = periods_data[period_key]['sma']
        ema_data = periods_data[period_key]['ema']
        
        # Generate comments for both SMA and EMA
        sma_comment = generate_ma_comment(ticker, period, 'SMA', current_price, 
                                         sma_data['value'], sma_data['price_vs_ma'])
        ema_comment = generate_ma_comment(ticker, period, 'EMA', current_price,
                                         ema_data['value'], ema_data['price_vs_ma'])
        
        # Column order: Period | SMA | P0/SMA | SMA/P0 | Signal | Comments | EMA | P0/EMA | EMA/P0 | Signal | Comments
        row = {
            'Period': f'MA{period}',
            'SMA': f"${sma_data['value']:.2f}",
            'P0/SMA': f"{sma_data['price_vs_ma']:+.1f}%",
            'SMA/P0': f"{sma_data['ma_vs_price']:+.1f}%",
            'SMA_Signal': sma_data['signal'],
            'SMA_Comments': sma_comment,
            'EMA': f"${ema_data['value']:.2f}",
            'P0/EMA': f"{ema_data['price_vs_ma']:+.1f}%",
            'EMA/P0': f"{ema_data['ma_vs_price']:+.1f}%",
            'EMA_Signal': ema_data['signal'],
            'EMA_Comments': ema_comment
        }
        table_rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(table_rows)
    
    # Apply styling with proper function for row-wise styling
    def style_row(row):
        """Apply color to signal cells"""
        styles = [''] * len(row)
        
        # Find signal column indices
        cols = list(row.index)
        if 'SMA_Signal' in cols:
            sma_signal_idx = cols.index('SMA_Signal')
            if row['SMA_Signal'] == 'Buy':
                styles[sma_signal_idx] = 'background-color: #d4edda; color: #155724; font-weight: bold'
            elif row['SMA_Signal'] == 'Sell':
                styles[sma_signal_idx] = 'background-color: #f8d7da; color: #721c24; font-weight: bold'
            else:  # Neutral
                styles[sma_signal_idx] = 'background-color: #f8f9fa; color: #6c757d; font-weight: bold'
        
        if 'EMA_Signal' in cols:
            ema_signal_idx = cols.index('EMA_Signal')
            if row['EMA_Signal'] == 'Buy':
                styles[ema_signal_idx] = 'background-color: #d4edda; color: #155724; font-weight: bold'
            elif row['EMA_Signal'] == 'Sell':
                styles[ema_signal_idx] = 'background-color: #f8d7da; color: #721c24; font-weight: bold'
            else:  # Neutral
                styles[ema_signal_idx] = 'background-color: #f8f9fa; color: #6c757d; font-weight: bold'
        
        return styles
    
    # Apply styling
    styled_df = df.style.apply(style_row, axis=1).set_properties(**{
        'text-align': 'left',
        'font-size': '14px',
        'padding': '8px'
    }).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#f8f9fa'), 
                                      ('font-weight', 'bold'),
                                      ('text-align', 'left'),
                                      ('padding', '10px')]}
    ])
    
    # Display table
    st.dataframe(
        styled_df,
        column_config={
            'Period': st.column_config.TextColumn('Period', width='small'),
            'SMA': st.column_config.TextColumn('SMA', width='small'),
            'P0/SMA': st.column_config.TextColumn('P0/SMA', width='small'),
            'SMA/P0': st.column_config.TextColumn('SMA/P0', width='small'),
            'SMA_Signal': st.column_config.TextColumn('Signal', width='small'),
            'SMA_Comments': st.column_config.TextColumn('Comments', width='large'),
            'EMA': st.column_config.TextColumn('EMA', width='small'),
            'P0/EMA': st.column_config.TextColumn('P0/EMA', width='small'),
            'EMA/P0': st.column_config.TextColumn('EMA/P0', width='small'),
            'EMA_Signal': st.column_config.TextColumn('Signal', width='small'),
            'EMA_Comments': st.column_config.TextColumn('Comments', width='large')
        },
        hide_index=True,
        use_container_width=True
    )

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
    valid_data = [p for p in performance_data if not p.get('error', False)]
    
    if not valid_data:
        st.warning("No valid data to display in table")
        return
    
    # Detect data type and create appropriate DataFrame
    if valid_data and 'percentage_change' in valid_data[0]:
        # Price performance data
        df_display = pd.DataFrame([
            {
                'Ticker': p['ticker'],
                'Current Price': f"${p['current_price']:.2f}" if p['current_price'] else "N/A",
                'Historical Price': f"${p['historical_price']:.2f}" if p['historical_price'] else "N/A",
                'Absolute Change': f"${p['absolute_change']:+.2f}" if p['absolute_change'] else "N/A",
                'Percentage Change': f"{p['percentage_change']:+.2f}%" if p['percentage_change'] is not None else "N/A",
                'Period': p.get('period_label', p.get('period', 'N/A'))
            }
            for p in valid_data
        ])
        # Sort by percentage change (descending)
        df_display = df_display.sort_values('Percentage Change', key=lambda x: 
            pd.to_numeric(x.str.rstrip('%'), errors='coerce'), ascending=False)
            
    elif valid_data and 'volume_change' in valid_data[0]:
        # Volume performance data
        df_display = pd.DataFrame([
            {
                'Ticker': p['ticker'],
                'Current Volume': f"{p['current_volume']:,}" if p['current_volume'] else "N/A",
                'Benchmark Average': f"{p['benchmark_average']:,.0f}" if p['benchmark_average'] else "N/A",
                'Volume Change': f"{p['volume_change']:+.2f}%" if p['volume_change'] is not None else "N/A",
                'Benchmark Period': p.get('benchmark_label', p.get('benchmark_period', 'N/A'))
            }
            for p in valid_data
        ])
        # Sort by volume change (descending)
        df_display = df_display.sort_values('Volume Change', key=lambda x: 
            pd.to_numeric(x.str.rstrip('%'), errors='coerce'), ascending=False)
    else:
        # Unknown data structure
        st.warning("Unknown data format - cannot display table")
        return
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
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
            
            # Get current price for display
            current_price = data.get('current_price', 0)
            timestamp_str = datetime.now().strftime('%m/%d/%Y, %I:%M %p')
            
            # Display current price
            st.markdown(f"**Current Price:** ${current_price:.2f} ({timestamp_str})")
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
                    mode_options = ["Custom", "Category", "Preset"]

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
                            st.write(f"Definition: {definition}")
                        if how_to_read:
                            st.write(f"How to Read: {how_to_read}")

                        # Optional family-level long-form overview
                        doc_slug = get_indicator_doc_slug(key)
                        markdown_text = load_indicator_markdown(doc_slug)

                        if markdown_text:
                            with st.expander(f"Learn more about {doc_slug}", expanded=False):
                                st.markdown(markdown_text)

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
        
    # Check if we need to fetch new data - handle both price and volume modes
    if controls['analysis_mode'] == 'price':
        current_data = st.session_state.performance_data
        last_update = st.session_state.last_update
    else:  # volume mode
        current_data = st.session_state.volume_data
        last_update = st.session_state.volume_last_update
    
    ticker_count_changed = (
        current_data is not None and 
        len(controls['tickers']) != len([p for p in current_data if not p.get('error', False)])
    )

    should_fetch = (
        controls['refresh'] or 
        current_data is None or
        last_update is None or
        ticker_count_changed  # NEW: Refresh when ticker count changes
    )
    
    if should_fetch:
        if controls['analysis_mode'] == 'price':
            # Fetch price performance data
            performance_data = fetch_performance_data(
                controls['tickers'], 
                controls['period'],
                save_to_db=controls['database_save']
            )
            
            # Store in session state
            st.session_state.performance_data = performance_data
            st.session_state.last_update = datetime.now()
            current_data = performance_data
            
        else:  # volume mode
            # Fetch volume performance data
            volume_data = fetch_volume_data(
                controls['tickers'], 
                controls['period'],
                save_to_db=controls['database_save']
            )
            
            # Store in session state
            st.session_state.volume_data = volume_data
            st.session_state.volume_last_update = datetime.now()
            current_data = volume_data
        
        st.success(f"✅ Data updated successfully at {datetime.now().strftime('%H:%M:%S')}")
    else:
        # Use cached data based on analysis mode
        if controls['analysis_mode'] == 'price':
            current_data = st.session_state.performance_data
        else:
            current_data = st.session_state.volume_data
    
    if current_data:
        # Create heatmap title based on analysis mode
        if controls['analysis_mode'] == 'price':
            title = f"{controls['group_name']} - {controls['period_name']} Performance"
        else:  # volume mode
            title = f"{controls['group_name']} - Current Volume vs. {controls['period_name']} Avg."
        
        # Display summary statistics
        st.subheader("📊 Summary Statistics")
        display_summary_stats(current_data)
        
        st.markdown("---")
        
        # Display heatmap
        st.subheader("🗺️ Performance Heatmap")
        
        # Add baseline date info (only for price mode)
        if controls['analysis_mode'] == 'price':
            baseline_date = None
            if current_data:
                for item in current_data:
                    if not item.get('error', False):
                        period = item.get('period', '1d')
                        
                        # FIXED: Use proper trading day calculation for baseline date
                        from src.calculations.performance import get_baseline_date_for_display
                        baseline_date_str = get_baseline_date_for_display(period)
                        baseline_date = datetime.strptime(baseline_date_str, '%Y-%m-%d').strftime('%m/%d/%y')
                        break
            
            if baseline_date:
                st.caption(f"Baseline Date: {baseline_date}")
        
        display_heatmap(current_data, title, controls['group'])
        
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

            refresh_today_clicked = st.button(
                "Refresh today's cells",
                key="scd_single_refresh_today_cells",
                disabled=not live_date_in_matrix,
                help=(
                    "Refresh today's visible date/ticker cells in the current "
                    "Single Indicator matrix. The app recalculates enough data to "
                    "produce today's values, replaces only today's visible cells, "
                    "and leaves historical cells unchanged."
                ),
            )

            if refresh_today_clicked:
                with st.spinner("Refreshing today's Single Indicator cells."):
                    st.session_state.scd_single_indicator_matrix = (
                        _refresh_scd_single_indicator_live_date_cells(
                            matrix=single_matrix,
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

                if refresh_report.get("status") == "ok":
                    st.success(
                        "Today's cells refreshed for "
                        f"{len(refresh_report.get('tickers_refreshed', []))} ticker(s) "
                        f"in {refresh_report.get('total_seconds')}s."
                    )
                elif refresh_report.get("status") == "partial":
                    st.warning(
                        "Today's cells partially refreshed. "
                        f"Refreshed {len(refresh_report.get('tickers_refreshed', []))} ticker(s); "
                        f"errors: {len(refresh_report.get('errors', []))}."
                    )
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
                        "scoring with a minimal selected-row compute config. D3-D2 "
                        "currently supports RSI and SMA rows."
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

    can_build_matrix = bool(selected_tickers) and bool(selected_row_keys)
    if not can_build_matrix:
        st.info("Select at least one ticker and one indicator row to build the SCD matrix.")

    col_build, col_clear_matrix = st.columns([0.45, 0.55])

    with col_build:
        build_clicked = st.button(
            "Rebuild Comparison Matrix",
            key="scd_build_matrix",
            type="primary",
            disabled=not can_build_matrix,
            use_container_width=True,
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

    if build_clicked:
        # Read from Session State at build time so the recalculation value used
        # by the matrix builder matches the active widget state for this run.
        force_refresh_for_build = bool(
            st.session_state.get("scd_force_refresh_cache", False)
        )

        if force_refresh_for_build:
            _get_scd_cache_stats()["force_refreshes"] += 1

        with st.spinner("Building comparison matrix from existing rolling signal data..."):
            st.session_state.scd_signal_matrix = _build_scd_cross_sectional_matrix(
                selected_tickers=selected_tickers,
                selected_row_keys=selected_row_keys,
                window_days=10,
                force_refresh=force_refresh_for_build,
                anchor_date=effective_anchor_date,
            )
            st.session_state.scd_matrix_last_run = datetime.now().isoformat(timespec="seconds")
     
    if st.session_state.scd_matrix_last_run:
        st.caption(f"Last SCD matrix build: {st.session_state.scd_matrix_last_run}")

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
                    # Backfill 22-day history for rolling heatmap
                    st.session_state.tech_calculator.backfill_technical_indicators(
                        ticker=ticker,
                        days=22
                    )
                    # Calculate 52-week price extremes
                    st.session_state.tech_calculator.calculate_52_week_analysis(ticker)
                except Exception as e:
                    # Silent failure - don't break app load for individual ticker failures
                    pass
        st.session_state.technical_background_updated = True
    
    # Page navigation in sidebar
    st.sidebar.title("📊 Navigation")
    st.session_state.selected_page = st.sidebar.selectbox(
        "Choose Dashboard:",
        options=['performance_heatmaps', 'technical_analysis', 'stock_comparison'],
        format_func=lambda x: {
            'performance_heatmaps': '📈 Performance Heatmaps',
            'technical_analysis': '🎯 Technical Analysis',  
            'stock_comparison': '📋 Stock Comparison'
        }[x],
        index=['performance_heatmaps', 'technical_analysis', 'stock_comparison'].index(
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

if __name__ == "__main__":
    main()
