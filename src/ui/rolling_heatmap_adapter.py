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
# Contract adapter (pure)
# ----------------------------
def build_plotly_heatmap_inputs(
    *,
    rolling_payload: dict,
    indicator_keys: List[str],
    indicator_defs: Optional[Dict[str, Dict[str, str]]] = None,
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
    raw_dates = dates   #x = dates    
    x = [format_date_label(d) for d in raw_dates]
    
    # Inititalize variables
    row_keys: List[str] = []
    y: List[str] = []
    z: List[List[float]] = []
    text: List[List[str]] = []
    customdata: List[List[dict]] = []

    # ----------------------------
    # Phase III (UI-only): Display-Only Price row
    # ----------------------------
    if price_block and isinstance(price_block.get("values"), list):
        price_vals = price_block.get("values", [])
        # Ensure length alignment to raw_dates
        if len(price_vals) == len(raw_dates):
            row_keys.append("__PRICE__")
            y.append("Price")

            z_row = [float("nan")] * len(raw_dates)  # NaN => no score color semantics
            text_row = []
            cd_row = []

            for d_raw, v in zip(raw_dates, price_vals):
                if v is None:
                    text_row.append("")  # blank cell
                else:
                    try:
                        text_row.append(f"${float(v):,.2f}")
                    except (TypeError, ValueError):
                        text_row.append("")

                cd_row.append(
                    {
                        "indicator_key": "__PRICE__",
                        "display_name": "Price",
                        "date": d_raw,
                        "raw_value": v,
                        "score": None,
                        "meta": rolling_payload.get("meta", {}),
                    }
                )

            z.append(z_row)
            text.append(text_row)
            customdata.append(cd_row)

    for key in indicator_keys:
        row = rows.get(key) or {}
        
        # display reader-friendly TI names
        #display_name = row.get("display_name") or defs.get(key, {}).get("display_name") or key
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

        for d_raw, v, s in zip(raw_dates, values, scores):  #for d, v, s in zip(x, values, scores):
            # z must be numeric; use NaN for missing
            z_row.append(float(s) if s is not None else float("nan"))
            text_row.append(format_cell_value(key, v))
            cd_row.append(
                {
                    "indicator_key": key,
                    "display_name": display_name,
                    "date": d_raw,    #d,
                    "raw_value": v,
                    "score": s,
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
            hovertemplate=(
                "<b>%{customdata.display_name}</b><br>"
                "Date: %{customdata.date}<br>"
                "Value: %{customdata.raw_value}<br>"
                "Score: %{customdata.score}<br>"
                "<extra></extra>"
            ),
            colorbar=dict(title="Score"),
        )
    )

    fig.update_layout(
        title=title,
        margin=dict(l=20, r=20, t=50, b=20),
        height=450,
    )

    fig.update_xaxes(side="top", type="category")    # Move date to top of heatmap
    fig.update_yaxes(autorange="reversed")

    return fig