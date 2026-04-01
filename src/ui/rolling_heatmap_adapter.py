# Stamp: Sat, March 14, 2026 6:00PM
# src/ui/rolling_heatmap_adapter.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import plotly.graph_objects as go
from datetime import datetime


# ----------------------------
# Public “payload” structure
# ----------------------------
@dataclass(frozen=True)
class PlotlyHeatmapInputs:
    """
    UI-ready inputs for a Plotly Heatmap.

    z: numeric matrix used for color mapping (we use score levels, not raw indicator values)
    text: strings displayed in each cell (raw indicator values formatted for humans)
    customdata: per-cell metadata used for hover and click interactions
    x: column labels (dates)
    y: row labels (indicator display names)
    row_keys: stable IDs for rows (used by dropdown/definition panel)
    """
    z: List[List[float]]
    text: List[List[str]]
    customdata: List[List[dict]]
    x: List[str]
    y: List[str]
    row_keys: List[str]


# ----------------------------
# Row definitions (v1)
# ----------------------------
# indicator_key must match what your rolling payload contains.
# If a key is defined here but not present in rolling_payload, the UI will show blanks for that row (expected).
INDICATOR_DEFS: Dict[str, Dict[str, str]] = {
    # Moving averages
    "EMA_5": {
        "display_name": "EMA (5)",
        "definition": "Exponential Moving Average puts more weight on recent prices.",
        "how_to_read": "Very short-term trend reference; reacts quickly to price changes.",
    },
    "EMA_10": {
        "display_name": "EMA (10)",
        "definition": "Exponential Moving Average puts more weight on recent prices.",
        "how_to_read": "Short-term trend reference; faster than EMA(20).",
    },
    "EMA_13": {
        "display_name": "EMA (13)",
        "definition": "Exponential Moving Average puts more weight on recent prices.",
        "how_to_read": "Short-term trend reference; commonly paired with other MAs.",
    },
    "EMA_20": {
        "display_name": "EMA (20)",
        "definition": "Exponential Moving Average puts more weight on recent prices.",
        "how_to_read": "Often used to judge short-to-medium trend direction.",
    },
    "EMA_50": {
        "display_name": "EMA (50)",
        "definition": "Exponential Moving Average over a longer window than EMA(20).",
        "how_to_read": "Smoother than EMA(20); often used as a medium-term trend reference.",
    },
    "EMA_100": {
        "display_name": "EMA (100)",
        "definition": "Exponential Moving Average over a long window.",
        "how_to_read": "Longer-term trend reference; smoother and slower to change.",
    },
    "EMA_200": {
        "display_name": "EMA (200)",
        "definition": "Exponential Moving Average over a very long window.",
        "how_to_read": "Very long-term trend reference; often used as a regime filter.",
    },
    "HMA_9": {
        "display_name": "HMA (9)",
        "definition": "Hull Moving Average reduces lag while staying smooth.",
        "how_to_read": "Short-term trend/timing; turns quickly relative to EMA/SMA.",
    },
    "HMA_21": {
        "display_name": "HMA (21)",
        "definition": "Hull Moving Average is designed to reduce lag while staying smooth.",
        "how_to_read": "Can turn earlier than SMA/EMA; often used for trend and turns.",
    },
    "HMA_50": {
        "display_name": "HMA (50)",
        "definition": "Hull Moving Average over a longer window.",
        "how_to_read": "Smoother trend reference with reduced lag relative to longer SMAs/EMAs.",
    },
    # Momentum / oscillators
    "RSI_14": {
        "display_name": "RSI (14)",
        "definition": "Relative Strength Index compares recent gains vs losses on a 0–100 scale.",
        "how_to_read": "Higher = stronger recent gains; lower = stronger recent losses.",
    },
    "WILLR_14": {
        "display_name": "Williams %R (14)",
        "definition": "Shows where the close sits within the recent high-low range (typically -100 to 0).",
        "how_to_read": "Closer to 0 = near recent highs; closer to -100 = near recent lows.",
    },
    "UO_5_10_15": {
        "display_name": "UO(5,10,15)",
        "definition": "Ultimate Oscillator blends short/medium/long buying pressure into one momentum oscillator.",
        "how_to_read": "Higher = stronger momentum; 45–55 often treated as neutral depending on your rules.",
    },    
    "UO_7_14_28": {
        "display_name": "UO(7,14,28)",
        "definition": "Blends short/medium/long lookbacks into one momentum oscillator.",
        "how_to_read": "Higher suggests stronger buying pressure; lower suggests selling pressure.",
    },
    "UO_10_20_40": {
        "display_name": "Ultimate Oscillator (10,20,40)",
        "definition": "Ultimate Oscillator blends short/medium/long buying pressure into one momentum oscillator.",
        "how_to_read": "Longer windows smooth signals; use your rule thresholds for buy/sell regions.",
    },
    "CCI_10": {
        "display_name": "CCI (10)",
        "definition": "Commodity Channel Index measures how far price has deviated from its statistical mean.",
        "how_to_read": "Above +100 often indicates strength; below -100 often indicates weakness.",
    },
    "CCI_14": {
        "display_name": "CCI (14)",
        "definition": "Commodity Channel Index measures how far price is from its recent average.",
        "how_to_read": "Bigger positive = price unusually strong; bigger negative = unusually weak.",
    },
    "CCI_20": {
        "display_name": "CCI (20)",
        "definition": "Commodity Channel Index measures how far price has deviated from its statistical mean.",
        "how_to_read": "Longer length smooths swings; +100/-100 remain common reference levels.",
    },
    "ROC_12": {
        "display_name": "ROC (12)",
        "definition": "Rate of Change measures percent change versus N periods ago.",
        "how_to_read": "Positive = up vs N periods ago; negative = down vs N periods ago.",
    },
    "ROC_20": {
        "display_name": "ROC (20)",
        "definition": "Rate of Change over a longer window than ROC(12).",
        "how_to_read": "Smoother momentum read than ROC(12).",
    },

    # Trend strength
    "ADX_9": {
        "display_name": "ADX (9)",
        "definition": "Average Directional Index measures trend strength (not direction).",
        "how_to_read": "More responsive than ADX(14); can react faster to emerging trends.",
    },
    "ADX_14": {
        "display_name": "ADX (14)",
        "definition": "Average Directional Index measures trend strength (not direction).",
        "how_to_read": "Higher = stronger trend; lower = weaker or ranging market.",
    },
    "ADX_20": {
        "display_name": "ADX (20)",
        "definition": "Average Directional Index measures trend strength (not direction).",
        "how_to_read": "Smoother than ADX(14); better for longer trend-strength regimes.",
    },
    # Volume-based
    "MFI_14": {
        "display_name": "MFI (14)",
        "definition": "Money Flow Index combines price and volume to estimate buying vs selling pressure.",
        "how_to_read": "Higher suggests stronger buying pressure; lower suggests stronger selling pressure.",
    },
    "CMF_21": {
        "display_name": "CMF (21)",
        "definition": "Chaikin Money Flow estimates buying/selling pressure using price and volume.",
        "how_to_read": "Above 0 suggests accumulation; below 0 suggests distribution.",
    },
    "OBV": {
        "display_name": "OBV",
        "definition": "On-Balance Volume cumulatively adds/subtracts volume based on up/down closes.",
        "how_to_read": "Rising OBV can confirm an uptrend; falling OBV can confirm a downtrend.",
    },
    # Add more keys as you expand the milestone (MACD, BB, Stoch, etc.)
}


# ----------------------------
# Formatting helpers (v1)
# ----------------------------
def format_date_label(date_key: str) -> str:
    """
    Convert 'YYYY-MM-DD' -> 'M/D' for x-axis display.
    Falls back to the raw string if parsing fails.
    """
    try:
        dt = datetime.strptime(date_key, "%Y-%m-%d")
        return f"{dt.month}/{dt.day}"
    except Exception:
        return date_key
    
def _abbr(n: float) -> str:
    """Human-friendly abbreviation for large magnitudes (e.g., 1532000 -> 1.53M)."""
    if n is None or (isinstance(n, float) and np.isnan(n)):
        return "—"
    a = abs(n)
    if a >= 1_000_000_000:
        return f"{n/1_000_000_000:.2f}B"
    if a >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    if a >= 1_000:
        return f"{n/1_000:.2f}K"
    return f"{n:.2f}"


def format_cell_value(indicator_key: str, v: Any) -> str:
    """
    Turn a raw indicator value into the string shown inside each heatmap cell.

    Rules:
    - RSI: 1 decimal (or 0 if you prefer later)
    - CMF: 3 decimals (small magnitudes matter)
    - OBV: abbreviated (K/M/B)
    - default: 2 decimals
    """
    if v is None:
        return "—"
    try:
        fv = float(v)
    except Exception:
        return "—"
    if np.isnan(fv):
        return "—"

    if indicator_key.startswith("RSI"):
        return f"{fv:.1f}"
    if indicator_key.startswith("CMF"):
        return f"{fv:.3f}"
    if indicator_key == "OBV" or indicator_key.startswith("OBV"):
        return _abbr(fv)
    return f"{fv:.2f}"

# ----------------------------
# Formatting + hover helpers (Phase III UX)
# ----------------------------
_SCORE_LABELS = {
    -2: "Strong Sell",
    -1: "Sell",
     0: "Neutral",
     1: "Buy",
     2: "Strong Buy",
}

_SCORE_RULE_KEYS = {
    -2: "strong_sell",
    -1: "sell",
     0: "neutral",
     1: "buy",
     2: "strong_buy",
}


def score_to_label(score: Any) -> str:
    """Map numeric score to the user-facing signal label."""
    try:
        return _SCORE_LABELS.get(int(score), "")
    except Exception:
        return ""


def score_to_rule_key(score: Any) -> Optional[str]:
    """Map numeric score to the rulebook state key."""
    try:
        return _SCORE_RULE_KEYS.get(int(score))
    except Exception:
        return None


def _is_missing(v: Any) -> bool:
    """Safe missing-value check for None / NaN-like values."""
    if v is None:
        return True
    try:
        return bool(np.isnan(float(v)))
    except Exception:
        return False


def format_hover_value(indicator_key: str, v: Any) -> str:
    """
    Format values for hover/expander display.

    This is deliberately separate from format_cell_value() so we can keep
    in-cell text stable while using cleaner hover-specific formatting.
    """
    if _is_missing(v):
        return "—"

    try:
        fv = float(v)
    except Exception:
        return "—"

    if indicator_key == "__PRICE__":
        return f"${fv:,.2f}"
    if indicator_key.startswith("RSI"):
        return f"{fv:.1f}"
    if indicator_key.startswith("CMF"):
        return f"{fv:.3f}"
    if indicator_key == "OBV" or indicator_key.startswith("OBV"):
        return _abbr(fv)
    return f"{fv:.2f}"


def format_signed_number(v: Any, decimals: int = 2) -> str:
    """Format signed numeric deltas such as +4.81 / -1.22."""
    if _is_missing(v):
        return "—"
    try:
        fv = float(v)
    except Exception:
        return "—"
    return f"{fv:+,.{decimals}f}"


def format_signed_percent(v: Any, decimals: int = 2) -> str:
    """Format signed percentages such as +0.99% / -1.22%."""
    if _is_missing(v):
        return "—"
    try:
        fv = float(v)
    except Exception:
        return "—"
    return f"{fv:+.{decimals}f}%"


def safe_pct_delta(curr: Any, prev: Any) -> Optional[float]:
    """
    Compute percent change from prev -> curr as a display percentage.
    Returns None when calculation is not valid.
    """
    if _is_missing(curr) or _is_missing(prev):
        return None
    try:
        curr_f = float(curr)
        prev_f = float(prev)
    except Exception:
        return None
    if prev_f == 0:
        return None
    return ((curr_f - prev_f) / abs(prev_f)) * 100.0


def infer_trend(curr: Any, prev: Any, tolerance: float = 1e-12) -> str:
    """Return Rising / Falling / Flat for day-over-day movement."""
    if _is_missing(curr) or _is_missing(prev):
        return ""
    try:
        curr_f = float(curr)
        prev_f = float(prev)
    except Exception:
        return ""
    delta = curr_f - prev_f
    if abs(delta) <= tolerance:
        return "Flat"
    return "Rising" if delta > 0 else "Falling"


def _humanize_indicator_token(token: str) -> str:
    """
    Convert a raw rule token like EMA_20 into EMA(20), RSI_14 into RSI(14),
    UO_7_14_28 into UO(7,14,28), etc.
    """
    if not token or "_" not in token:
        return token

    parts = token.split("_")
    head, tail = parts[0], parts[1:]

    if all(p.replace(".", "", 1).isdigit() for p in tail):
        return f"{head}({','.join(tail)})"
    return token


def translate_rule_text(expr: str) -> str:
    """
    Lightweight adapter-side translation of common rule-expression patterns.

    This is presentation-only. It should improve readability without altering
    rule meaning. Unknown patterns fall back to the raw expression.
    """
    if not expr:
        return ""

    text = str(expr)

    simple_replacements = {
        "Close > ": "Price is above ",
        "Close < ": "Price is below ",
        "close > ": "Price is above ",
        "close < ": "Price is below ",
        " >= 0": " is non-negative",
        " <= 0": " is non-positive",
        "_slope > 0": " is rising",
        "_slope < 0": " is falling",
        "rising_2bar(": "has risen for 2 bars: ",
        "falling_2bar(": "has fallen for 2 bars: ",
        "abs(Close/": "Price is close to ",
        "abs(close/": "Price is close to ",
    }

    for old, new in simple_replacements.items():
        text = text.replace(old, new)

    for raw in sorted(INDICATOR_DEFS.keys(), key=len, reverse=True):
        text = text.replace(raw, _humanize_indicator_token(raw))

    text = text.replace("ATRP_", "ATR%(")
    text = text.replace(") ", ") ")
    return text

# ----------------------------
# Contract adapter (pure)
# ----------------------------
def build_plotly_heatmap_inputs(
    *,
    rolling_payload: dict,
    indicator_keys: List[str],
    indicator_defs: Optional[Dict[str, Dict[str, str]]] = None,
    ohlcv_df: Optional[Any] = None,   # (for hover-only)
) -> PlotlyHeatmapInputs:
    """
    Convert the rolling heatmap “contract payload” into Plotly-ready matrices.

    Expected rolling_payload shape (minimum needed for v1):
      {
        "meta": {"ticker": str, "asof": "YYYY-MM-DD", "window_days": int},
        "dates": ["YYYY-MM-DD", ...],                 # x-axis
        "rows": {
          "<indicator_key>": {
            "display_name": str,
            "values": [float|None, ...],              # raw indicator values (text)
            "scores": [int|None, ...],                # -2..+2 preferred; drives colors
          },
          ...
        }
      }

    z uses scores (color), text uses values (display), customdata carries everything else.
    """
    defs = indicator_defs or INDICATOR_DEFS

    dates: List[str] = list(rolling_payload.get("dates", []))
    rows: Dict[str, dict] = dict(rolling_payload.get("rows", {}))
    extras = rolling_payload.get("extras") if isinstance(rolling_payload.get("extras"), dict) else {}
    price_block = extras.get("price") if isinstance(extras.get("price"), dict) else None
    raw_dates = dates
    x = [format_date_label(d) for d in raw_dates]

    # Initialize variables
    row_keys: List[str] = []
    y: List[str] = []
    z: List[List[float]] = []
    text: List[List[str]] = []
    customdata: List[List[dict]] = []

    # -------------------------------------------------
    # Local rulebook lookup (presentation-only, adapter-owned)
    # -------------------------------------------------
    _rulebook_cache: Optional[dict] = None

    def _load_rulebook() -> dict:
        nonlocal _rulebook_cache
        if _rulebook_cache is not None:
            return _rulebook_cache

        try:
            import json
            from pathlib import Path

            candidate_paths = [
                Path("master_rules_normalized.json"),
                Path("src/config/master_rules_normalized.json"),
            ]
            for p in candidate_paths:
                if p.exists():
                    with p.open("r", encoding="utf-8") as f:
                        _rulebook_cache = json.load(f)
                    return _rulebook_cache
        except Exception:
            pass

        _rulebook_cache = {}
        return _rulebook_cache

    def _rulebook_indicator_name(indicator_key: str) -> Optional[str]:
        """
        Map a row key like RSI_14 / STOCH_14_3_3 to the rulebook indicator family.
        """
        if indicator_key.startswith("RSI_"):
            return "RSI"
        if indicator_key.startswith("MACD_"):
            return "MACD"
        if indicator_key.startswith("STOCH_"):
            return "Stochastic"
        if indicator_key.startswith("ROC_"):
            return "ROC"
        if indicator_key.startswith("WILLR_"):
            return "Williams_R"
        if indicator_key.startswith("ADX_"):
            return "ADX"
        if indicator_key.startswith("MFI_"):
            return "MFI"
        if indicator_key.startswith("CMF_"):
            return "CMF"
        if indicator_key == "OBV" or indicator_key.startswith("OBV"):
            return "OBV"
        if indicator_key.startswith("EMA_"):
            return "EMA"
        if indicator_key.startswith("HMA_"):
            return "HMA"
        if indicator_key.startswith("CCI_"):
            return "CCI"
        if indicator_key.startswith("UO_"):
            return "Ultimate_Oscillator"
        if indicator_key.startswith("BullBearPower_"):
            return "BullBearPower"
        return None

    def _rulebook_param_key(indicator_key: str) -> Optional[str]:
        """
        Extract the param portion from a row key.
        Examples:
          RSI_14 -> 14
          MACD_12_26_9 -> 12_26_9
          OBV -> 0
        """
        if indicator_key == "OBV":
            return "0"
        if "_" not in indicator_key:
            return None
        return indicator_key.split("_", 1)[1]

    def _find_rule_block(indicator_key: str, score: Any) -> tuple[str, str, str]:
        """
        Return (rule_expr, rule_notes, rule_text) for the current indicator row + score.
        Presentation-only. Falls back cleanly on misses.
        """
        rule_state = score_to_rule_key(score)
        if not rule_state:
            return "", "", ""

        ind_name = _rulebook_indicator_name(indicator_key)
        param_key = _rulebook_param_key(indicator_key)
        if not ind_name or not param_key:
            return "", "", ""

        rules = _load_rulebook()
        categories = rules.get("categories", {}) if isinstance(rules, dict) else {}

        for _cat_name, indicators in categories.items():
            if not isinstance(indicators, dict):
                continue
            ind_block = indicators.get(ind_name)
            if not isinstance(ind_block, dict):
                continue

            feature_scopes = ind_block.get("feature_scopes", {})
            heatmap_scope = feature_scopes.get("heatmap", {}) if isinstance(feature_scopes, dict) else {}
            rule_block = heatmap_scope.get(param_key)
            if not isinstance(rule_block, dict):
                continue

            rule_expr = str(rule_block.get(rule_state, "") or "")
            rule_notes = str(rule_block.get("notes", "") or "")
            rule_text = translate_rule_text(rule_expr) if rule_expr else ""
            return rule_expr, rule_notes, rule_text

        return "", "", ""

    # ----------------------------
    # Phase III (UI-only): Display-Only Price row
    # ----------------------------
    if price_block and isinstance(price_block.get("values"), list):
        price_vals = price_block.get("values", [])
        if len(price_vals) == len(raw_dates):
            row_keys.append("__PRICE__")
            y.append("Price")

            z_row = [float("nan")] * len(raw_dates)
            text_row = []
            cd_row = []

            # ----------------------------------------
            # Optional OHLCV context (hover-only)
            # ----------------------------------------
            volume_series = {}
            volume_5d_avg = {}

            if ohlcv_df is not None:
                try:
                    df = ohlcv_df.copy()
                    df = df.sort_index()

                    # Normalize index to string YYYY-MM-DD
                    df.index = df.index.astype(str)

                    if "Volume" in df.columns:
                        volume_series = df["Volume"].to_dict()
                        volume_5d_avg = (
                            df["Volume"]
                            .rolling(5)
                            .mean()
                            .to_dict()
                        )
                except Exception:
                    volume_series = {}
                    volume_5d_avg = {}

            for idx, (d_raw, v) in enumerate(zip(raw_dates, price_vals)):
                prev_v = price_vals[idx - 1] if idx > 0 else None

                # ----------------------------
                # Value + formatting
                # ----------------------------
                if v is None:
                    text_row.append("")
                else:
                    try:
                        text_row.append(f"${float(v):,.2f}")
                    except Exception:
                        text_row.append("")

                formatted_value = format_hover_value("__PRICE__", v)

                # ----------------------------
                # Delta calculations
                # ----------------------------
                delta_abs = None
                if not _is_missing(v) and not _is_missing(prev_v):
                    try:
                        delta_abs = float(v) - float(prev_v)
                    except Exception:
                        delta_abs = None

                delta_pct = safe_pct_delta(v, prev_v)

                # ----------------------------
                # Volume metrics
                # ----------------------------
                vol = volume_series.get(d_raw)
                vol_avg = volume_5d_avg.get(d_raw)

                vol_rel = None
                if vol is not None and vol_avg not in (None, 0):
                    try:
                        vol_rel = ((float(vol) - float(vol_avg)) / float(vol_avg)) * 100.0
                    except Exception:
                        vol_rel = None

                # ----------------------------
                # Preformatted hover fragments (Price-row)
                # ----------------------------
                delta_abs_fmt = format_signed_number(delta_abs, decimals=2)
                delta_pct_suffix = f" ({format_signed_percent(delta_pct, decimals=2)})" if delta_pct is not None else ""

                volume_block = ""
                if not _is_missing(vol):
                    volume_block = f"Volume: {_abbr(float(vol))}<br>"

                volume_vs_avg_block = ""
                if not _is_missing(vol_rel) and not _is_missing(vol_avg):
                    volume_vs_avg_block = (
                        f"Volume vs 5D Avg: {format_signed_percent(vol_rel, decimals=1)} "
                        f"({_abbr(float(vol_avg))})<br>"
                    )

                # price row stays display-only / non-semantic
                trend_line = ""
                signal_line = ""
                rule_block = ""
                notes_block = ""
                definition_block = ""
                how_to_read_block = ""

                # ----------------------------
                # Customdata enrichment
                # ----------------------------
                cd_row.append(
                    {
                        "indicator_key": "__PRICE__",
                        "display_name": "Price",
                        "date": d_raw,
                        "raw_value": v,
                        "formatted_value": formatted_value,
                        "score": None,
                        "score_label": "",
                        "delta_abs": delta_abs,
                        "delta_pct": delta_pct,
                        "trend": "",

                        # volume metrics
                        "volume": vol,
                        "volume_5d_avg": vol_avg,
                        "volume_vs_5d_avg_pct": vol_rel,

                        # no rule semantics
                        "rule_expr": "",
                        "rule_notes": "",
                        "rule_text": "",

                        # no educational text for price row
                        "definition": "",
                        "how_to_read": "",

                        # preformatted hover fields
                        "delta_abs_fmt": delta_abs_fmt,
                        "delta_pct_suffix": delta_pct_suffix,
                        "trend_line": trend_line,
                        "signal_line": signal_line,
                        "rule_block": rule_block,
                        "notes_block": notes_block,
                        "definition_block": definition_block,
                        "how_to_read_block": how_to_read_block,
                        "volume_block": volume_block,
                        "volume_vs_avg_block": volume_vs_avg_block,

                        "meta": rolling_payload.get("meta", {}),
                    }
                )

            z.append(z_row)
            text.append(text_row)
            customdata.append(cd_row)

    for key in indicator_keys:
        row = rows.get(key) or {}

        # display reader-friendly TI names
        row_display = row.get("display_name")
        defs_display = defs.get(key, {}).get("display_name")

        # Prefer payload label unless it looks like a raw indicator key (e.g., "RSI_14").
        if row_display and defs_display and row_display.strip() == key:
            display_name = defs_display
        else:
            display_name = row_display or defs_display or key

        values = list(row.get("values", []))
        scores = list(row.get("scores", []))

        # Normalize lengths (defensive)
        if len(values) < len(x):
            values = values + [None] * (len(x) - len(values))
        if len(scores) < len(x):
            scores = scores + [None] * (len(x) - len(scores))

        row_keys.append(key)
        y.append(display_name)

        z_row: List[float] = []
        text_row: List[str] = []
        cd_row: List[dict] = []

        for idx, (d_raw, v, s) in enumerate(zip(raw_dates, values, scores)):
            prev_v = values[idx - 1] if idx > 0 else None
            delta_abs = None
            if not _is_missing(v) and not _is_missing(prev_v):
                try:
                    delta_abs = float(v) - float(prev_v)
                except Exception:
                    delta_abs = None

            delta_pct = safe_pct_delta(v, prev_v)
            trend = infer_trend(v, prev_v)

            formatted_value = format_hover_value(key, v)
            score_label = score_to_label(s)

            rule_expr, rule_notes, rule_text = _find_rule_block(key, s)
            definition = defs.get(key, {}).get("definition", "")
            how_to_read = defs.get(key, {}).get("how_to_read", "")

            # ----------------------------
            # Preformatted hover fragments (Indicator-row)
            # ----------------------------
            delta_abs_fmt = format_signed_number(delta_abs, decimals=2)
            delta_pct_suffix = f" ({format_signed_percent(delta_pct, decimals=2)})" if delta_pct is not None else ""
            trend_line = f"Trend: {trend}<br>" if trend else ""
            signal_line = f"<br>Signal: {score_label}<br>" if score_label else ""
            rule_block = f"<br>Rule:<br>{rule_text}<br>" if rule_text else ""
            notes_block = f"<br>Notes:<br>{rule_notes}<br>" if rule_notes else ""
            definition_block = f"<br>Definition:<br>{definition}<br>" if definition else ""
            how_to_read_block = f"<br>How to Read:<br>{how_to_read}<br>" if how_to_read else ""

            # indicator rows do not use volume hover fields
            volume_block = ""
            volume_vs_avg_block = ""

            # z must be numeric; use NaN for missing
            z_row.append(float(s) if s is not None else float("nan"))
            text_row.append(format_cell_value(key, v))
            cd_row.append(
                {
                    "indicator_key": key,
                    "display_name": display_name,
                    "date": d_raw,
                    "raw_value": v,
                    "formatted_value": formatted_value,
                    "score": s,
                    "score_label": score_label,
                    "delta_abs": delta_abs,
                    "delta_pct": delta_pct,
                    "trend": trend,
                    "rule_expr": rule_expr,
                    "rule_notes": rule_notes,
                    "rule_text": rule_text,
                    "definition": definition,
                    "how_to_read": how_to_read,

                    # preformatted hover fields
                    "delta_abs_fmt": delta_abs_fmt,
                    "delta_pct_suffix": delta_pct_suffix,
                    "trend_line": trend_line,
                    "signal_line": signal_line,
                    "rule_block": rule_block,
                    "notes_block": notes_block,
                    "definition_block": definition_block,
                    "how_to_read_block": how_to_read_block,
                    "volume_block": volume_block,
                    "volume_vs_avg_block": volume_vs_avg_block,

                    "meta": rolling_payload.get("meta", {}),
                }
            )

        z.append(z_row)
        text.append(text_row)
        customdata.append(cd_row)

    return PlotlyHeatmapInputs(z=z, text=text, customdata=customdata, x=x, y=y, row_keys=row_keys)


# ----------------------------
# Plotly figure (pure)
# ----------------------------
def make_rolling_heatmap_figure(
    hm: PlotlyHeatmapInputs,
    *,
    title: str = "Rolling Signal Heatmap",
) -> go.Figure:
    """
    Build the Plotly figure using:
    - z = score-based color levels
    - text = raw indicator values shown in-cell
    - customdata = hover payload
    """
    # 5-level discrete mapping around scores -2..+2.
    # We keep this simple; you can swap colors later without changing schema.
    colorscale = [
        [0.0, "#8B0000"],   # strong sell
        [0.25, "#CD5C5C"],  # sell
        [0.5, "#D3D3D3"],   # neutral
        [0.75, "#90EE90"],  # buy
        [1.0, "#006400"],   # strong buy
    ]

    hovertemplate = (
        "<b>%{customdata.display_name}</b><br>"
        "Date: %{customdata.date}<br>"
        "<br>"
        "Value: %{customdata.formatted_value}<br>"
        "Δ vs prior day: %{customdata.delta_abs_fmt}"
        "%{customdata.delta_pct_suffix}<br>"
        "%{customdata.trend_line}"
        "%{customdata.signal_line}"
        "%{customdata.rule_block}"
        "%{customdata.notes_block}"
        "%{customdata.definition_block}"
        "%{customdata.how_to_read_block}"
        "%{customdata.volume_block}"
        "%{customdata.volume_vs_avg_block}"
        "<extra></extra>"
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=hm.z,
            x=hm.x,
            y=hm.y,
            text=hm.text,
            texttemplate="%{text}",
            customdata=hm.customdata,
            colorscale=colorscale,
            zmin=-2,
            zmax=2,
            hovertemplate=hovertemplate,
            colorbar=dict(title="Score"),
        )
    )

    fig.update_layout(
        title=title,
        margin=dict(l=20, r=20, t=80, b=20),   # 't': use to add padding btwn plotly icons & heatmap
        height=450,
    )

    fig.update_xaxes(side="top", type="category")    # Move date to top of heatmap
    fig.update_yaxes(autorange="reversed")

    return fig