# Stamp: Thu, May 14, 2026 6:22PM
# src/ui/rolling_heatmap_presets.py
"""
Rolling Heatmap curated preset and Custom membership catalog.
Version: 1.2

Purpose:
    Own curated row-key memberships for the Phase III Rolling Heatmap
    Selection & Catalog architecture.

Scope:
    This module is authoritative for curated membership metadata only:
      - default Custom row set
      - explicit Overview preset memberships
      - preset ordering / labels

    It does not own:
      - row classification metadata
      - Category / Scope / Window / Family filtering
      - thematic preset generation
      - numeric computation
      - rulebook semantics
      - signal scoring
      - rolling payload generation
      - display names
      - definitions / educational text
      - UI control rendering

Authority:
    All memberships are expressed as canonical rolling heatmap row_key values.
    These row keys must exist in rolling_heatmap_classification.ROW_CLASSIFICATION.

Important ownership boundary:
    Overview presets are explicit curated memberships.
    Thematic presets such as ST Trend, MT Trend, LT Trend, ST Momentum,
    MT Momentum, and LT Momentum are generated in rolling_heatmap_selection.py.
"""

from __future__ import annotations

from typing import Dict, List, Mapping, Tuple

try:
    from .rolling_heatmap_classification import ROW_CLASSIFICATION
except ImportError:  # pragma: no cover
    # Allows direct ad-hoc execution from repo root during manual verification.
    from src.ui.rolling_heatmap_classification import ROW_CLASSIFICATION


# ---------------------------------------------------------------------
# Custom default membership
# ---------------------------------------------------------------------
# Authoritative default row-key set for Custom mode.
#
# Custom is a saved/editable selection set at runtime, but restore-default
# behavior must resolve back to this catalog-owned definition.
CUSTOM_DEFAULT: List[str] = [
    "RSI_14",            # Momentum

    # Trend / directional bias
    "EMA_20",     # "EMA_20",
    "EMA_50",
    "SMA_50",
    "SMA_100",
    "SMA_200",
    "VWMA_20",
    "HMA_55",

    # Trend / conviction
    "ADX_14",
    "BullBearPower_13",

    # Momentum / exhaustion
    "STOCH_14_3_3",
    "WILLR_14",
    "CCI_20",
    "UO_7_14_28",
    "DPO_21",

    # Momentum / thrust
    "MACD_12_26_9",
    "ROC_12",

    # Volatility
    "BB_PCT_B",
    "BB_BW",
    "ATR_14",

    # Volume / accumulation-distribution
    "MFI_14",
    "CMF_21",
    "OBV",
]


# ---------------------------------------------------------------------
# Explicit Overview preset memberships
# ---------------------------------------------------------------------
# Overview presets are intentionally curated row sets.
# They are not generated from Category filters.
#
# Thematic presets are generated later in rolling_heatmap_selection.py.
OVERVIEW_PRESETS: Mapping[str, List[str]] = {
    "ST Overview": [
        # Short-term trend / directional bias
        "SMA_10",
        "SMA_20",
        "EMA_10",
        "EMA_20",
        "VWMA_10",
        "HMA_9",

        # Short-term trend / conviction
        "ADX_9",
        "BullBearPower_10",

        # Short-term momentum / exhaustion
        "RSI_10",
        "STOCH_5_3_3",
        "WILLR_5",
        "CCI_10",
        "UO_5_10_15",
        "DPO_11",

        # Short-term momentum / thrust
        "MACD_8_17_5",
        "ROC_9",

        # Short-term volatility
        "BB_PCT_B_ST",
        "BB_BW_ST",
        "ATR_10", # "ATR_5", "ATR_9", "ATR_10", "ATR_13", "ATR_12"  

        # Short-term volume / accumulation-distribution
        "MFI_10",
        "CMF_10",
    ],

    "MT Overview": [
        # Medium-term trend / directional bias
        "SMA_50",
        "EMA_50",
        "VWMA_20",
        "HMA_21",

        # Medium-term trend / conviction
        "ADX_14",
        "BullBearPower_13",

        # Medium-term momentum / exhaustion
        "RSI_14",
        "STOCH_14_3_3",
        "WILLR_14",
        "CCI_14",
        "UO_7_14_28",
        "DPO_21",

        # Medium-term momentum / thrust
        "MACD_12_26_9",
        "ROC_14",

        # Medium-term volatility
        "BB_PCT_B",
        "BB_BW",
        "ATR_14", # "ATR_20", "ATR_21"

        # Medium-term volume / accumulation-distribution
        "MFI_14",
        "CMF_21",
    ],

    "LT Overview": [
        # Long-term trend / directional bias
        "SMA_100",
        "SMA_200",
        "SMA_250",
        "EMA_100",
        "EMA_200",
        "VWMA_50",
        "HMA_55",

        # Long-term trend / conviction
        "ADX_20",
        "BullBearPower_21",

        # Long-term momentum / exhaustion
        "RSI_21",
        "STOCH_21_5_5",
        "WILLR_20",
        "CCI_20",
        "UO_10_20_40",
        "DPO_40",

        # Long-term momentum / thrust
        "MACD_20_50_10",
        "ROC_50",

        # Long-term volatility
        "BB_PCT_B_LT",
        "BB_BW_LT",
        "ATR_50",

        # Long-term volume / accumulation-distribution
        "MFI_30",
        "CMF_50",
    ],
}


# ---------------------------------------------------------------------
# Locked v1 preset dropdown order
# ---------------------------------------------------------------------
# Overview presets are explicit curated memberships above.
# Thematic presets in this order are generated by the selection layer.
PRESET_ORDER: Tuple[str, ...] = (
    "ST Overview",
    "MT Overview",
    "LT Overview",
    "ST Trend",
    "MT Trend",
    "LT Trend",
    "ST Momentum",
    "MT Momentum",
    "LT Momentum",
)


# ---------------------------------------------------------------------
# Lightweight validation helpers
# ---------------------------------------------------------------------
# These helpers validate curated membership metadata only. They do not
# resolve modes, apply filters, or generate thematic presets.
def get_explicit_preset_names() -> List[str]:
    """Return explicit curated preset names in locked dropdown order."""
    return [name for name in PRESET_ORDER if name in OVERVIEW_PRESETS]


def get_unknown_membership_keys() -> Dict[str, List[str]]:
    """
    Return unknown row keys referenced by curated memberships.

    Empty lists indicate that curated memberships are aligned with
    ROW_CLASSIFICATION.
    """
    known = set(ROW_CLASSIFICATION.keys())

    unknown: Dict[str, List[str]] = {
        "CUSTOM_DEFAULT": [row_key for row_key in CUSTOM_DEFAULT if row_key not in known]
    }

    for preset_name, row_keys in OVERVIEW_PRESETS.items():
        unknown[preset_name] = [row_key for row_key in row_keys if row_key not in known]

    return unknown


def validate_curated_memberships() -> None:
    """
    Raise ValueError if any curated membership references an unknown row_key.

    This is intended for manual verification and later unit-test coverage.
    """
    unknown = get_unknown_membership_keys()
    failures = {name: keys for name, keys in unknown.items() if keys}

    if failures:
        raise ValueError(f"Unknown row_key(s) in curated memberships: {failures}")