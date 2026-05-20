# Stamp: Thu, May 14, 2026 6:22PM
# src/ui/rolling_heatmap_classification.py
"""
Rolling Heatmap row-classification catalog.

Purpose:
    Own canonical row grouping metadata for the Phase III Rolling Heatmap
    Selection & Catalog architecture.

Scope:
    This module is authoritative for classification metadata only:
      - family
      - category
      - scope
      - window
      - tags
      - family-group membership support

    It does not own:
      - numeric computation
      - rulebook semantics
      - signal scoring
      - rolling payload generation
      - display names
      - definitions / educational text
      - preset or Custom curated memberships

Authority:
    Row identity is keyed by canonical rolling heatmap row_key values.
    These row keys must match the row identities emitted by the existing
    rolling payload path and consumed by the adapter/UI.

Important ownership boundary:
    Display / education metadata remains in
    rolling_heatmap_adapter.py::INDICATOR_DEFS.
"""

from __future__ import annotations

from typing import Any, Dict, FrozenSet, List, Mapping


# ---------------------------------------------------------------------
# Family groups
# ---------------------------------------------------------------------
# Derived selection logic may use these groups as first-class filters.
# These are grouping aliases only; they do not define numeric or semantic
# meaning and must not be used as display/education metadata.
FAMILY_GROUPS: Mapping[str, FrozenSet[str]] = {
    "MVA": frozenset({"SMA", "EMA", "VWMA", "HMA"}),
    "Oscillators": frozenset(
        {
            "RSI",
            "Stochastic",
            "Williams_R",
            "CCI",
            "Ultimate_Oscillator",
            "MFI",
            "CMF",
        }
    ),
}


# ---------------------------------------------------------------------
# Canonical row classification
# ---------------------------------------------------------------------
# Authoritative classification metadata keyed by canonical row_key.
#
# Fields:
#   family:
#       Indicator family / rule-engine family label.
#   category:
#       Primary Category entry point for browsing.
#   scope:
#       First-class classification field within Category.
#   window:
#       Canonical Window filter value: ST, MT, LT, or All.
#   tags:
#       Secondary descriptors. Tags are not canonical homes and must not
#       duplicate category/scope/window ownership.
#
# Special cases:
#   - VWMA canonical home is Trend -> Directional Bias.
#     It receives the secondary tag "Institutional Anchor".
#   - OBV uses Window = All and is not forced into fake ST/MT/LT buckets.
ROW_CLASSIFICATION: Dict[str, Dict[str, Any]] = {
    # -----------------------------------------------------------------
    # Trend / moving-average directional bias
    # -----------------------------------------------------------------
    "EMA_5": {
        "family": "EMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "ST",
        "tags": [],
    },
    "EMA_10": {
        "family": "EMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "ST",
        "tags": [],
    },
    "EMA_13": {
        "family": "EMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "ST",
        "tags": [],
    },
    "EMA_20": {
        "family": "EMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "ST",
        "tags": [],
    },
    "EMA_50": {
        "family": "EMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "MT",
        "tags": [],
    },
    "EMA_100": {
        "family": "EMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "LT",
        "tags": [],
    },
    "EMA_200": {
        "family": "EMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "LT",
        "tags": [],
    },

    "SMA_10": {
        "family": "SMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "ST",
        "tags": [],
    },
    "SMA_20": {
        "family": "SMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "ST",
        "tags": [],
    },
    "SMA_50": {
        "family": "SMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "MT",
        "tags": [],
    },
    "SMA_100": {
        "family": "SMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "LT",
        "tags": [],
    },
    "SMA_200": {
        "family": "SMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "LT",
        "tags": [],
    },
    "SMA_250": {
        "family": "SMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "LT",
        "tags": [],
    },
    "HMA_9": {
        "family": "HMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "ST",
        "tags": [],
    },
    "HMA_21": {
        "family": "HMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "MT",
        "tags": [],
    },
    "HMA_50": {
        "family": "HMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "LT",
        "tags": [],
    },
    "HMA_55": {
        "family": "HMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "LT",
        "tags": [],
    },

    "VWMA_10": {
        "family": "VWMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "ST",
        "tags": ["Institutional Anchor"],
    },
    "VWMA_20": {
        "family": "VWMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "MT",
        "tags": ["Institutional Anchor"],
    },
    "VWMA_50": {
        "family": "VWMA",
        "category": "Trend",
        "scope": "Directional Bias",
        "window": "LT",
        "tags": ["Institutional Anchor"],
    },

    # -----------------------------------------------------------------
    # Trend strength / trend-momentum support
    # -----------------------------------------------------------------
    "ADX_9": {
        "family": "ADX",
        "category": "Trend",
        "scope": "Conviction Filter",
        "window": "ST",
        "tags": [],
    },
    "ADX_14": {
        "family": "ADX",
        "category": "Trend",
        "scope": "Conviction Filter",
        "window": "MT",
        "tags": [],
    },
    "ADX_20": {
        "family": "ADX",
        "category": "Trend",
        "scope": "Conviction Filter",
        "window": "LT",
        "tags": [],
    },

    "MACD_12_26_9": {
        "family": "MACD",
        "category": "Momentum",
        "scope": "Thrust Detection",
        "window": "MT",
        "tags": [],
    },
    "MACD_5_34_1": {
        "family": "MACD",
        "category": "Momentum",
        "scope": "Thrust Detection",
        "window": "ST",
        "tags": [],
    },
    "MACD_8_17_5": {
        "family": "MACD",
        "category": "Momentum",
        "scope": "Thrust Detection",
        "window": "ST",
        "tags": [],
    },
    "MACD_20_50_10": {
        "family": "MACD",
        "category": "Momentum",
        "scope": "Thrust Detection",
        "window": "LT",
        "tags": [],
    },

    "BullBearPower_10": {
        "family": "BullBearPower",
        "category": "Trend",
        "scope": "Conviction Filter",
        "window": "ST",
        "tags": [],
    },
    "BullBearPower_13": {
        "family": "BullBearPower",
        "category": "Trend",
        "scope": "Conviction Filter",
        "window": "MT",
        "tags": [],
    },
    "BullBearPower_21": {
        "family": "BullBearPower",
        "category": "Trend",
        "scope": "Conviction Filter",
        "window": "LT",
        "tags": [],
    },

    # -----------------------------------------------------------------
    # Momentum / oscillators
    # -----------------------------------------------------------------
    "RSI_10": {
        "family": "RSI",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "ST",
        "tags": [],
    },
    "RSI_14": {
        "family": "RSI",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "MT",
        "tags": [],
    },
    "RSI_21": {
        "family": "RSI",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "MT",
        "tags": [],
    },
    "RSI_30": {
        "family": "RSI",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "LT",
        "tags": [],
    },

    "STOCH_5_3_3": {
        "family": "Stochastic",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "ST",
        "tags": [],
    },
    "STOCH_14_3_3": {
        "family": "Stochastic",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "MT",
        "tags": [],
    },
    "STOCH_21_5_5": {
        "family": "Stochastic",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "LT",
        "tags": [],
    },

    "WILLR_5": {
        "family": "Williams_R",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "ST",
        "tags": [],
    },
    "WILLR_14": {
        "family": "Williams_R",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "MT",
        "tags": [],
    },
    "WILLR_20": {
        "family": "Williams_R",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "LT",
        "tags": [],
    },

    "CCI_10": {
        "family": "CCI",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "ST",
        "tags": [],
    },
    "CCI_14": {
        "family": "CCI",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "MT",
        "tags": [],
    },
    "CCI_20": {
        "family": "CCI",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "LT",
        "tags": [],
    },

    "UO_5_10_15": {
        "family": "Ultimate_Oscillator",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "ST",
        "tags": [],
    },
    "UO_7_14_28": {
        "family": "Ultimate_Oscillator",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "MT",
        "tags": [],
    },
    "UO_10_20_40": {
        "family": "Ultimate_Oscillator",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "LT",
        "tags": [],
    },

    "ROC_9": {
        "family": "ROC",
        "category": "Momentum",
        "scope": "Thrust Detection",
        "window": "ST",
        "tags": [],
    },
    "ROC_12": {
        "family": "ROC",
        "category": "Momentum",
        "scope": "Thrust Detection",
        "window": "ST",
        "tags": [],
    },
    "ROC_14": {
        "family": "ROC",
        "category": "Momentum",
        "scope": "Thrust Detection",
        "window": "MT",
        "tags": [],
    },
    "ROC_20": {
        "family": "ROC",
        "category": "Momentum",
        "scope": "Thrust Detection",
        "window": "MT",
        "tags": [],
    },
    "ROC_50": {
        "family": "ROC",
        "category": "Momentum",
        "scope": "Thrust Detection",
        "window": "LT",
        "tags": [],
    },    
    # -----------------------------------------------------------------
    # Momentum / detrended cycle exhaustion
    # -----------------------------------------------------------------
    "DPO_11": {
        "family": "DPO",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "ST",
        "tags": [],
    },
    "DPO_21": {
        "family": "DPO",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "MT",
        "tags": [],
    },
    "DPO_40": {
        "family": "DPO",
        "category": "Momentum",
        "scope": "Exhaustion Signals",
        "window": "LT",
        "tags": [],
    },
    # -----------------------------------------------------------------
    # Volatility / risk calibration
    # -----------------------------------------------------------------
    "ATR_5": {
        "family": "ATR",
        "category": "Volatility",
        "scope": "Risk Calibration",
        "window": "ST",
        "tags": [],
    },
#    "ATR_9": {
#        "family": "ATR",
#        "category": "Volatility",
#        "scope": "Risk Calibration",
#        "window": "ST",
#        "tags": [],
#    },
    "ATR_10": {
        "family": "ATR",
        "category": "Volatility",
        "scope": "Risk Calibration",
        "window": "ST",
        "tags": [],
    },
#    "ATR_13": {
#        "family": "ATR",
#        "category": "Volatility",
#        "scope": "Risk Calibration",
#        "window": "ST",
#        "tags": [],
#    },
    "ATR_14": {
        "family": "ATR",
        "category": "Volatility",
        "scope": "Risk Calibration",
        "window": "MT",
        "tags": [],
    },    
    "ATR_20": {
        "family": "ATR",
        "category": "Volatility",
        "scope": "Risk Calibration",
        "window": "MT",
        "tags": [],
    },
#    "ATR_21": {
#        "family": "ATR",
#        "category": "Volatility",
#        "scope": "Risk Calibration",
#        "window": "MT",
#        "tags": [],
#    },
    "ATR_50": {
        "family": "ATR",
        "category": "Volatility",
        "scope": "Risk Calibration",
        "window": "LT",
        "tags": [],
    },
    "ATR_100": {
        "family": "ATR",
        "category": "Volatility",
        "scope": "Risk Calibration",
        "window": "LT",
        "tags": [],
    },
    "ATR_200": {
        "family": "ATR",
        "category": "Volatility",
        "scope": "Risk Calibration",
        "window": "LT",
        "tags": [],
    },
    # -----------------------------------------------------------------
    # Volatility / Bollinger-derived numeric rows
    # -----------------------------------------------------------------
    "BB_PCT_B_ST": {
        "family": "Bollinger",
        "category": "Volatility",
        "scope": "Band Position/Width",
        "window": "ST",
        "tags": [],
    },
    "BB_BW_ST": {
        "family": "Bollinger",
        "category": "Volatility",
        "scope": "Band Position/Width",
        "window": "ST",
        "tags": [],
    },
    "BB_PCT_B": {
        "family": "Bollinger",
        "category": "Volatility",
        "scope": "Band Position/Width",
        "window": "MT",
        "tags": [],
    },
    "BB_BW": {
        "family": "Bollinger",
        "category": "Volatility",
        "scope": "Band Position/Width",
        "window": "MT",
        "tags": [],
    },
    "BB_PCT_B_LT": {
        "family": "Bollinger",
        "category": "Volatility",
        "scope": "Band Position/Width",
        "window": "LT",
        "tags": [],
    },
    "BB_BW_LT": {
        "family": "Bollinger",
        "category": "Volatility",
        "scope": "Band Position/Width",
        "window": "LT",
        "tags": [],
    },

    # -----------------------------------------------------------------
    # Volume / money flow
    # -----------------------------------------------------------------
    "MFI_10": {
        "family": "MFI",
        "category": "Volume",
        "scope": "Accumulation/Distribution",
        "window": "ST",
        "tags": [],
    },
    "MFI_14": {
        "family": "MFI",
        "category": "Volume",
        "scope": "Accumulation/Distribution",
        "window": "MT",
        "tags": [],
    },
    "MFI_30": {
        "family": "MFI",
        "category": "Volume",
        "scope": "Accumulation/Distribution",
        "window": "LT",
        "tags": [],
    },

    "CMF_10": {
        "family": "CMF",
        "category": "Volume",
        "scope": "Accumulation/Distribution",
        "window": "ST",
        "tags": [],
    },
    "CMF_21": {
        "family": "CMF",
        "category": "Volume",
        "scope": "Accumulation/Distribution",
        "window": "MT",
        "tags": [],
    },
    "CMF_30": {
        "family": "CMF",
        "category": "Volume",
        "scope": "Accumulation/Distribution",
        "window": "MT",
        "tags": [],
    },
    "CMF_50": {
        "family": "CMF",
        "category": "Volume",
        "scope": "Accumulation/Distribution",
        "window": "LT",
        "tags": [],
    },

    "OBV": {
        "family": "OBV",
        "category": "Volume",
        "scope": "Accumulation/Distribution",
        "window": "All",
        "tags": [],
    },
}


# ---------------------------------------------------------------------
# Lightweight catalog helpers
# ---------------------------------------------------------------------
# These helpers expose catalog metadata for later selection logic without
# making this module responsible for selection resolution.
def get_all_row_keys() -> List[str]:
    """Return all row_keys classified by the catalog, preserving catalog order."""
    return list(ROW_CLASSIFICATION.keys())


def get_categories() -> List[str]:
    """Return available Category values in deterministic first-seen order."""
    return list(dict.fromkeys(meta["category"] for meta in ROW_CLASSIFICATION.values()))


def get_scopes(category: str | None = None) -> List[str]:
    """Return available Scope values, optionally narrowed by Category."""
    scopes: List[str] = []
    for meta in ROW_CLASSIFICATION.values():
        if category is not None and meta["category"] != category:
            continue
        scopes.append(meta["scope"])
    return list(dict.fromkeys(scopes))


def get_windows(category: str | None = None) -> List[str]:
    """Return available Window values, optionally narrowed by Category."""
    windows: List[str] = []
    for meta in ROW_CLASSIFICATION.values():
        if category is not None and meta["category"] != category:
            continue
        windows.append(meta["window"])
    return list(dict.fromkeys(windows))


def get_families(category: str | None = None) -> List[str]:
    """Return available Family values, optionally narrowed by Category."""
    families: List[str] = []
    for meta in ROW_CLASSIFICATION.values():
        if category is not None and meta["category"] != category:
            continue
        families.append(meta["family"])

    # Include grouped-family names as first-class filter options.
    grouped = [group_name for group_name in FAMILY_GROUPS.keys()]
    return list(dict.fromkeys(grouped + families))


def has_row_key(row_key: str) -> bool:
    """Return True when row_key is classified by this catalog."""
    return row_key in ROW_CLASSIFICATION