# Stamp: Thu, July 9, 2026 2:25 PM
# src/ui/rolling_heatmap_adapter.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import textwrap

import numpy as np
import pandas as pd
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
# Hover formatting helpers
# ----------------------------
def _wrap_hover_text(value: Any, *, width: int = 72) -> str:
    """
    Return text with explicit Plotly hover line breaks.

    Plotly hover labels do not reliably auto-wrap long strings. This helper
    keeps source content clean while rendering Notes / Definition / How to Read
    in narrower, readable hover blocks.
    """
    if value is None:
        return ""

    text = str(value).strip()
    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    wrapped_lines: List[str] = []

    for raw_line in text.split("\n"):
        line = raw_line.strip()

        if not line:
            wrapped_lines.append("")
            continue

        # Preserve caller-supplied Plotly/HTML line breaks where they already
        # exist, while still wrapping each segment.
        segments = line.split("<br>")
        wrapped_segments: List[str] = []

        for segment in segments:
            segment = segment.strip()
            if not segment:
                wrapped_segments.append("")
                continue

            wrapped = textwrap.wrap(
                segment,
                width=width,
                break_long_words=False,
                break_on_hyphens=False,
            )
            wrapped_segments.extend(wrapped or [segment])

        wrapped_lines.extend(wrapped_segments)

    return "<br>".join(wrapped_lines)


def _format_hover_block(label: str, value: Any, *, width: int = 72) -> str:
    """Return a labeled hover block with wrapped content."""
    wrapped = _wrap_hover_text(value, width=width)
    if not wrapped:
        return ""
    return f"<br>{label}:<br>{wrapped}<br>"


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
        "definition": "EMA over a very long window.",
        "how_to_read": "Very long-term trend reference; often used as a regime filter.",
    },
    "SMA_10": {
        "display_name": "SMA(10)",
        "definition": "SMA averages closing prices equally over the last 10 periods.",
        "how_to_read": "Short-term trend reference. Smoother than very short EMA variants, but slower to react.",
    },
    "SMA_20": {
        "display_name": "SMA(20)",
        "definition": "SMA averages closing prices equally over the last 20 periods.",
        "how_to_read": "Common short-to-medium trend reference.<br>" 
        "Often used as a baseline trend and pullback level.",
    },
    "SMA_50": {
        "display_name": "SMA(50)",
        "definition": "SMA averages closing prices equally over the last 50 periods.",
        "how_to_read": "Medium-term trend reference.<br>" 
        "Smoother than SMA(20), with fewer short-term swings.",
    },
    "SMA_100": {
        "display_name": "SMA(100)",
        "definition": "SMA averages closing prices equally over the last 100 periods.",
        "how_to_read": "Longer-term trend reference.<br>" 
        "Useful for broader trend direction and structural support/resistance zones.",
    },
    "SMA_200": {
        "display_name": "SMA(200)",
        "definition": "SMA averages closing prices equally over the last 200 periods.",
        "how_to_read": "Very long-term trend reference.<br>" 
        "Commonly used as a regime-level trend filter.",
    },
    "SMA_250": {
        "display_name": "SMA(250)",
        "definition": "Rough proxy for one trading year.",
        "how_to_read": "Gives a slightly smoother 'annual trend' view than 200 days.",
    },
    # Event-only moving-average crossover rows.
    # Display metadata only: event truth is computed upstream and score truth
    # comes from the rulebook / signal-classifier path.
    "EMA_9_X_EMA_21": {
        "display_name": "EMA 9/21 Cross",
        "definition": (
            "Event-only row for EMA(9) crossing EMA(21).<br>"
            "It marks the crossover event date only."
        ),
        "how_to_read": (
            "+2 = EMA(9) crossed above EMA(21) on this date<br>"
            "-2 = EMA(9) crossed below EMA(21) on this date<br>"
            "0 = no crossover event | Blank = insufficient data"
        ),
    },
    "SMA_20_X_SMA_50": {
        "display_name": "SMA 20/50 Cross",
        "definition": (
            "Event-only row for SMA(20) crossing SMA(50).<br>"
            "It marks the crossover event date only."
        ),
        "how_to_read": (
            "+2 = SMA(20) crossed above SMA(50) on this date<br>"
            "-2 = SMA(20) crossed below SMA(50) on this date<br>"
            "0 = no crossover event | Blank = insufficient data"            
        ),
    },
    "SMA_50_X_SMA_200": {
        "display_name": "SMA 50/200 Cross",
        "definition": (
            "Event-only row for SMA(50) crossing SMA(200).<br>"
            "It marks the crossover event date only."
        ),
        "how_to_read": (
            "+2 = SMA(50) crossed above SMA(200) on this date<br>"
            "-2 = SMA(50) crossed below SMA(200) on this date<br>"
            "0 = no crossover event | Blank = insufficient data"            
        ),
    },
    "HMA_9": {
        "display_name": "HMA (9)",
        "definition": "Hull Moving Average reduces lag while staying smooth.",
        "how_to_read": "Short-term trend/timing; turns quickly relative to EMA/SMA.",
    },
    "HMA_16": {
        "display_name": "HMA(16)",
        "definition": "HMA(16) is a fast, smooth indicator designed to eliminate lag. It uses weighted moving averages to track price action closely while filtering out market noise. Turns quickly relative to EMA/SMA.",
        "how_to_read": (
            "Slope Indicator: An upward slope indicates a bullish trend.<br>"
            "Downward Slope: A downward slope indicates a bearish trend.<br>"
            "Direction Changes: A turning point suggests a potential trend reversal.<br>"
            "Price Crossovers: Price crossing above the line signals a buying opportunity.<br>"
            "Below the Line: Price dropping below the line signals a selling opportunity."
        ),
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
    "HMA_55": {
        "display_name": "HMA(55)",
        "definition": "Behaves like a 'living' trend line — it turns faster than a SMA(50) but w/o the whipsaw of a short EMA.",
        "how_to_read": "Smoother trend reference with reduced lag relative to longer SMAs/EMAs.",
    },
    "VWMA_10": {
        "display_name": "VWMA (10)",
        "definition": "Volume Weighted Moving Average weights price by volume over the last 10 periods.",
        "how_to_read": "Short-term trend reference. Because it is volume-weighted, heavier-volume sessions influence the average more than low-volume sessions.",
    },
    "VWMA_20": {
        "display_name": "VWMA (20)",
        "definition": "Volume Weighted Moving Average weights price by volume over the last 20 periods.",
        "how_to_read": "Medium-term trend reference. In Wave 1, shading should reflect engine-native VWMA rule scores while the displayed value remains the raw VWMA numeric value.",
    },
    "VWMA_50": {
        "display_name": "VWMA (50)",
        "definition": "Volume Weighted Moving Average weights price by volume over the last 50 periods.",
        "how_to_read": "Longer-term trend reference. Smoother than VWMA(10) and VWMA(20), with more emphasis on persistent, volume-backed trend direction.",
    },    
    # Momentum / oscillators
    "RSI_10": {
        "display_name": "RSI(10)",
        "definition": "Compares recent gains vs losses on a 0–100 scale. 80+ = strong sell | 70+ = sell | <30 = buy | <20 = strong buy",
        "how_to_read": "When RSI is rising above 50 and MACD crosses above its signal line,<br>" 
        "it reinforces the likelihood of an uptrend continuation.<br>" 
        "If RSI makes lower highs while MACD makes higher highs (or vice versa),<br>" 
        "it may indicate weakening momentum and a potential trend shift.",
    },
    "RSI_14": {
        "display_name": "RSI (14)",
        "definition": "Relative Strength Index compares recent gains vs losses on a 0–100 scale.",
        "how_to_read": "Higher = stronger recent gains; lower = stronger recent losses.",
    },
    "RSI_21": {
        "display_name": "RSI(21)",
        "definition": "Relative Strength Index compares recent gains vs losses on a 0–100 scale.",
        "how_to_read": "↑RSI above 50 + ↑volume ~ strong buying interest (reinforcing continuation of an uptrend). If RSI signals divergence (e.g., RSI (lower highs) + price (higher highs) +  high volume ~ possible trend reversal.",
    },
    "WILLR_5": {
        "display_name": "Williams %R(5)",
        "definition": "Shows where the close sits within the recent high-low range (typically -100 to 0).",
        "how_to_read": "Closer to 0 = near recent highs; closer to -100 = near recent lows.",
    },
    "WILLR_14": {
        "display_name": "Williams %R (14)",
        "definition": "Shows where the close sits within the recent high-low range (typically -100 to 0).",
        "how_to_read": "Closer to 0 = near recent highs; closer to -100 = near recent lows.",
    },
    "WILLR_20": {
        "display_name": "Williams %R(20)",
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
    "ROC_9": {
        "display_name": "ROC(9)",
        "definition": "More sensitive; faster signals; for ST trading; Caution: more frequent false signals",
        "how_to_read": "Confirming trend strength and direction in trending markets.",
    },    
    "ROC_12": {
        "display_name": "ROC (12)",
        "definition": "Measures the momentum of price changes. ROC measures %Δ versus N periods ago.",
        "how_to_read": "Positive = up vs N periods ago; negative = down vs N periods ago.",
    },
    "ROC_14": {
        "display_name": "ROC(14)",
        "definition": "Measures the momentum of price changes. ROC measures %Δ versus 14 periods ago.",
        "how_to_read": "+ROC: rising prices and potentially strong buying pressure (uptrend); -ROC: falling prices and potentially strong selling pressure (downtrend); 0: suggests balanced momentum",
    },
    "ROC_20": {
        "display_name": "ROC (20)",
        "definition": "14-36 days offers a balance of sensitivity & reliability for swing trading.",
        "how_to_read": "Smoother momentum read than ROC(12).",
    },
    "ROC_50": {
        "display_name": "ROC(50)",
        "definition": "Use longer periods, such as 36 or 200 days, for a smoother indicator that identifies long-term trend.",
        "how_to_read": "Strength: Highly responsive to price changes, giving traders quick insights into market dynamics.",
    },    
    # Detrended Price Oscillator
    "DPO_11": {
        "display_name": "DPO (11)",
        "definition": "Detrended Price Oscillator removes the longer trend component to highlight shorter-term cyclical price movement.",
        "how_to_read": "Displayed as DPO / price × 100. Negative values suggest price is below its detrended cycle baseline; '+' values suggest price is above it.",
    },
    "DPO_21": {
        "display_name": "DPO (21)",
        "definition": "Detrended Price Oscillator removes the longer trend component to highlight intermediate cyclical price movement.",
        "how_to_read": "Displayed as DPO / price × 100. '-' values suggest price is below its detrended cycle baseline; '+' values suggest price is above it.",
    },
    "DPO_40": {
        "display_name": "DPO (40)",
        "definition": "Detrended Price Oscillator removes the longer trend component to highlight longer cyclical price movement.",
        "how_to_read": "Displayed as DPO / price × 100. Negative values suggest price is below its detrended cycle baseline; '+'  values suggest price is above it.",
    },
    "BB_PCT_B_ST": {
        "display_name": "BB %B(ST)",
        "definition": "Bollinger %B using Bollinger(10,1.5). Shows where price sits within the ST band range.",
        "how_to_read": "Short-term Bollinger location measure. Lower values sit closer to the lower band; higher values sit closer to the upper band.",
    },
    "BB_BW_ST": {
        "display_name": "BB Bandwidth(ST)",
        "definition": "Bollinger Bandwidth using Bollinger(10,1.5). Measures short-term band width relative to the middle band.",
        "how_to_read": "Short-term Bollinger width measure. Higher values mean wider short-term bands; lower values mean tighter short-term bands.",
    },
    "BB_PCT_B": {
        "display_name": "BB %B",
        "definition": "Bollinger %B shows where price sits within the Bollinger band range.  A 'location indicactor'. Used for measuring relative price location within the bands (oscillator value).",
        "how_to_read": "Canonical medium-term Bollinger %B using Bollinger(20,2.0). Lower values sit closer to the lower band; higher values sit closer to the upper band.",
    },
    "BB_BW": {
        "display_name": "BB Bandwidth",
        "definition": "Bollinger Bandwidth measures the width of the Bollinger Bands relative to the middle band.",
        "how_to_read": "Canonical medium-term Bollinger bandwidth using Bollinger(20,2.0). Higher values mean wider bands; lower values mean tighter bands.",
    },
    "BB_PCT_B_LT": {
        "display_name": "BB %B(LT)",
        "definition": "Bollinger %B using Bollinger(50,2.5). Shows where price sits within the long-term band range.",
        "how_to_read": "Long-term Bollinger location measure. Lower values sit closer to the lower band; higher values sit closer to the upper band.",
    },
    "BB_BW_LT": {
        "display_name": "BB Bandwidth(LT)",
        "definition": "Bollinger Bandwidth using Bollinger(50,2.5). Measures LT band width relative to the middle band.",
        "how_to_read": "Long-term Bollinger width measure. Higher values mean wider long-term bands; lower values mean tighter long-term bands.",
    },    
    # Volatility / risk calibration
    "ATR_5": {
        "display_name": "ATR (5)",
        "definition": "Average True Range measures recent absolute price range / volatility over 5 periods.",
        "how_to_read": "Higher ATR means larger recent price ranges. ATR is directional-neutral: it measures volatility, not bullish or bearish direction.",
    },
    "ATR_9": {
        "display_name": "ATR (9)",
        "definition": "Average True Range measures recent absolute price range / volatility over 9 periods.",
        "how_to_read": "ST volatility reference. Higher ATR means larger recent price ranges; lower ATR means quieter price movement.",
    },
    "ATR_10": {
        "display_name": "ATR(10)",
        "definition": "Average True Range measures recent absolute price range / volatility over 10 periods.",
        "how_to_read": "ST volatility reference. Higher ATR means larger recent price ranges. ATR is directional-neutral: it measures volatility, not bullish or bearish direction.",
    },
    "ATR_13": {
        "display_name": "ATR (13)",
        "definition": "Average True Range measures recent absolute price range / volatility over 13 periods.",
        "how_to_read": "ST volatility reference. Higher ATR means larger recent price ranges. ATR is directional-neutral: it measures volatility, not bullish or bearish direction.",
    },
    "ATR_14": {
        "display_name": "ATR(14)",
        "definition": "Average True Range measures recent absolute price range / volatility over 14 periods.",
        "how_to_read": "Intermediate volatility reference. Higher ATR means larger recent price ranges; lower ATR means quieter price movement.",
    },
    "ATR_20": {
        "display_name": "ATR (20)",
        "definition": "Average True Range measures recent absolute price range / volatility over 20 periods.",
        "how_to_read": "Intermediate volatility reference. Higher ATR means larger recent price ranges; lower ATR means quieter price movement.",
    },
    "ATR_21": {
        "display_name": "ATR (21)",
        "definition": "Average True Range measures recent absolute price range / volatility over 21 periods.",
        "how_to_read": "Intermediate volatility reference. Higher ATR means larger recent price ranges. ATR is directional-neutral: it measures volatility, not bullish or bearish direction.",
    },
    "ATR_50": {
        "display_name": "ATR(50)",
        "definition": "Average True Range measures longer-term absolute price range / volatility over 50 periods.",
        "how_to_read": "LT volatility reference. Higher ATR means larger sustained price ranges; lower ATR means quieter longer-term movement.",
    },
    "ATR_100": {
        "display_name": "ATR (100)",
        "definition": "Average True Range measures recent absolute price range / volatility over 100 periods.",
        "how_to_read": "LT volatility reference. Higher ATR means larger recent price ranges; lower ATR means quieter price movement.",
    },
    "ATR_200": {
        "display_name": "ATR (200)",
        "definition": "Average True Range measures recent absolute price range / volatility over 200 periods.",
        "how_to_read": "LT volatility reference. Higher ATR means larger recent price ranges. ATR is directional-neutral: it measures volatility, not bullish or bearish direction.",
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
    "MACD_12_26_9": {
        "display_name": "MACD(12,26,9)",
        "definition": "Moving Average Convergence Divergence histogram using parameters 12 (fast), 26 (slow), and 9 (EMA(9) of the 'signal line').",
        "how_to_read": "Histogram value is calculated as the 'MACD Line' minus the 'Signal Line'.<br>" 
        "A positive histogram value (above zero) signifies that the MACD Line has recently crossed above the Signal Line.<br>"
        "The MACD line is the spread of the 2 EMAs.<br>"
        " - When the MACD line crosses above the 9-period signal line, it often generates a bullish (buy) signal.<br>"
        " - When it crosses below, it signals a bearish (sell) movement",
    },
    "MACD_5_34_1": {
        "display_name": "MACD(5,34,1)",
        "definition": "Moving Average Convergence Divergence histogram using parameters 5, 34, and 1.",
        "how_to_read": "Displayed value is the MACD histogram. Hover also shows the MACD line, signal line, and day-over-day histogram change.",
    },
    "MACD_8_17_5": {
        "display_name": "MACD(8,17,5)",
        "definition": "Moving Average Convergence Divergence histogram using parameters 8, 17, and 5.",
        "how_to_read": "Displayed value is the MACD histogram. Hover also shows the MACD line, signal line, and day-over-day histogram change.",
    },
    "MACD_20_50_10": {
        "display_name": "MACD(20,50,10)",
        "definition": "Moving Average Convergence Divergence histogram using parameters 20, 50, and 10.",
        "how_to_read": "Displayed value is the MACD histogram. Hover also shows the MACD line, signal line, and day-over-day histogram change.",
    },

    "STOCH_14_3_3": {
        "display_name": "Stoch(14,3,3)",
        "definition": "Stochastic Oscillator %K using parameters 14, 3, and 3.",
        "how_to_read": "Displayed value is %K. Higher values indicate price closing near the recent high; lower values indicate price closing near the recent low.",
    },
    "STOCH_5_3_3": {
        "display_name": "Stoch(5,3,3)",
        "definition": "Stochastic Oscillator %K using parameters 5, 3, and 3.",
        "how_to_read": "Shorter lookback makes this more reactive than Stoch(14,3,3). Displayed value is %K.",
    },
    "STOCH_21_5_5": {
        "display_name": "Stoch(21,5,5)",
        "definition": "Stochastic Oscillator %K using parameters 21, 5, and 5.",
        "how_to_read": "Longer lookback makes this smoother and slower. Displayed value is %K.",
    },
    "BullBearPower_10": {
        "display_name": "BullBear(10)",
        "definition": "Bull/Bear Power measures buying vs selling pressure around EMA(10).",
        "how_to_read": "Displayed value is the combined BullBearPower series. Positive values suggest bullish pressure; negative values suggest bearish pressure.",
    },
    "BullBearPower_13": {
        "display_name": "BullBear(13)",
        "definition": "Bull/Bear Power measures buying vs selling pressure around EMA(13).",
        "how_to_read": "Displayed value is the combined BullBearPower series. Positive values suggest bullish pressure; negative values suggest bearish pressure.",
    },
    "BullBearPower_21": {
        "display_name": "BullBear(21)",
        "definition": "Bull/Bear Power measures buying vs selling pressure around EMA(21).",
        "how_to_read": "Displayed value is the combined BullBearPower series. Positive values suggest bullish pressure; negative values suggest bearish pressure.",
    },
    # Volume-based
    "MFI_10": {
        "display_name": "MFI(10)",
        "definition": (
            "MFI combines typical price and volume into a 0–100 "
            "oscillator. MFI(10) is the fastest configured variant."
        ),
        "how_to_read": (
            "Low readings indicate oversold opportunity bias; high readings "
            "indicate overbought risk.<br>"
            "≤15: Strong Buy | 15–25: Buy | 25–75: Neutral | "
            "75–85: Sell | ≥85: Strong Sell.<br>"
            "The score describes the current MFI state, not a confirmed reversal."
        ),
    },
    "MFI_14": {
        "display_name": "MFI(14)",
        "definition": (
            "MFI combines typical price and volume into a 0–100 "
            "oscillator. MFI(14) is the standard reference variant."
        ),
        "how_to_read": (
            "Low readings indicate oversold opportunity bias; high readings "
            "indicate overbought risk.<br>"
            "≤15: Strong Buy | 15–25: Buy | 25–75: Neutral | "
            "75–85: Sell | ≥85: Strong Sell.<br>"
            "The score describes the current MFI state, not a confirmed reversal."
        ),
    },
    "MFI_30": {
        "display_name": "MFI(30)",
        "definition": (
            "MFI combines typical price and volume into a 0–100 "
            "oscillator. MFI(30) is the slowest configured variant."
        ),
        "how_to_read": (
            "Low readings indicate oversold opportunity bias; high readings "
            "indicate overbought risk.<br>"
            "≤15: Strong Buy | 15–25: Buy | 25–75: Neutral | "
            "75–85: Sell | ≥85: Strong Sell.<br>"
            "The score describes the current MFI state, not a confirmed reversal."
        ),
    },
    "CMF_10": {
        "display_name": "CMF(10)",
        "definition": "CMF estimates buying/selling pressure using price and volume.",
        "how_to_read": "Above 0 suggests accumulation; below 0 suggests distribution.",
    },
    "CMF_21": {
        "display_name": "CMF (21)",
        "definition": "Chaikin Money Flow estimates buying/selling pressure using price and volume.",
        "how_to_read": ">0: accumulation bias (buying pressure) | Above +0.25 = strong accumulation; <0 = distribution bias (selling pressure) | Below -0.25 = strong distribution",
    },
    "CMF_50": {
        "display_name": "CMF(50)",
        "definition": "CMF estimates buying/selling pressure using price and volume.",
        "how_to_read": "Effective in both trending and ranging markets. Works well on daily and weekly charts for swing trading analysis.",
    },
    "CMF_30": {
        "display_name": "CMF(30)",
        "definition": "CMF estimates buying/selling pressure using price and volume.",
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
    if indicator_key.startswith("ROC"):
#        return f"{fv:.3f}"             # fractional units
        return f"{fv * 100.0:.2f}"      # percent-point units
    if indicator_key.startswith("BB_PCT_B"):
        return f"{fv * 100.0:.1f}"
    if indicator_key.startswith("BB_BW"):
        return f"{fv * 100.0:.2f}"
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
    if indicator_key.startswith("ROC"):
#        return f"{fv:.3f}"          # fractional units
        return f"{fv * 100.0:.2f}"   # percent-point units   
    if indicator_key.startswith("BB_PCT_B"):
        return f"{fv * 100.0:.1f}"
    if indicator_key.startswith("BB_BW"):
        return f"{fv * 100.0:.2f}"
    if indicator_key.startswith("CMF"):
        return f"{fv:.3f}"
    if indicator_key.startswith("DPO_"):
        return f"{fv:+.2f}%"             # percent-point units   
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
    Convert raw indicator tokens into a cleaner display form.

    Examples:
      EMA_20           -> EMA(20)
      RSI_14           -> RSI(14)
      UO_7_14_28       -> UO(7,14,28)
      EMA_13_13        -> EMA(13)      # repeated-parameter alias
      EMA_21_21        -> EMA(21)      # repeated-parameter alias
      MACD_12_26_9     -> MACD(12,26,9)

    Important:
    - This is presentation-only.
    - It should not change rule semantics.
    - It focuses on root indicator tokens, not extended derivation suffixes
      such as _slope / _signal / _hist in this phase.
    """
    if not token or "_" not in token:
        return token

    # Already humanized / display-like token; leave it alone.
    if "(" in token and ")" in token:
        return token

    parts = token.split("_")
    head, tail = parts[0], parts[1:]

    # Root repeated-parameter alias collapse:
    # EMA_13_13 -> EMA(13), EMA_21_21 -> EMA(21), etc.
    # Restrict this to known moving-average alias families where the repeated
    # form is known to be a presentation alias rather than a true multi-param series.
    if head in {"EMA", "SMA", "VWMA", "HMA"} and len(tail) == 2 and tail[0] == tail[1]:
        if tail[0].replace(".", "", 1).isdigit():
            return f"{head}({tail[0]})"

    # Standard numeric-parameter families:
    # RSI_10 -> RSI(10), SMA_100 -> SMA(100), MACD_12_26_9 -> MACD(12,26,9), etc.
    if all(p.replace(".", "", 1).isdigit() for p in tail):
        return f"{head}({','.join(tail)})"

    return token


# Hover text clean-up: 
def should_fallback_to_raw_rule(expr: str) -> bool:
    """
    Return True when a rule expression is complex enough that the
    presentation-only translator is more likely to degrade readability
    than improve it.

    Hybrid strategy:
    - simple rules -> translated English-ish text
    - complex rules -> raw rule expression
    """
    if not expr:
        return False

    expr = str(expr)

    complex_markers = [
        "abs(",
        "* ATRP_",
        "*ATRP_",
        "/SMA_",
        "/EMA_",
        "/VWMA_",
        "/HMA_",
    ]

    return any(marker in expr for marker in complex_markers)


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

        # NOTE:
        # Do NOT translate '>= 0' / '<= 0' generically here.
        # Those replacements corrupt chained comparisons such as:
        #   -0.10 <= CMF_21 <= 0.10
        # by partially matching the second comparator.
        #
        # Keep slope thresholds raw for now as well; prettifying derived
        # suffix expressions belongs to a later pass.
        #
        # "_slope > 0": " is rising",
        # "_slope < 0": " is falling",

        "abs(Close/": "Price is close to ",
        "abs(close/": "Price is close to ",
    }

    for old, new in simple_replacements.items():
        text = text.replace(old, new)

    # Humanize root indicator tokens directly from the rule text, not only from
    # INDICATOR_DEFS keys. This catches cases like:
    #   RSI_10        -> RSI(10)
    #   SMA_100       -> SMA(100)
    #   EMA_13_13     -> EMA(13)
    #   MACD_12_26_9  -> MACD(12,26,9)
    import re

    token_pattern = re.compile(r"\b[A-Za-z][A-Za-z0-9]*_(?:\d+(?:\.\d+)?)(?:_(?:\d+(?:\.\d+)?))*\b")

    def _token_repl(match: re.Match) -> str:
        raw = match.group(0)
        return _humanize_indicator_token(raw)

    text = token_pattern.sub(_token_repl, text)

    # Helper-call cleanup:
    # Convert:
    #   rising_2bar(SMA_100)
    # to:
    #   has risen for 2 bars: SMA(100)
    #
    # and similarly for falling_2bar(...), without leaving a stray trailing ')'.
    text = re.sub(
        r"rising_2bar\(([^)]+)\)",
        r"has risen for 2 bars: \1",
        text,
    )
    text = re.sub(
        r"falling_2bar\(([^)]+)\)",
        r"has fallen for 2 bars: \1",
        text,
    )

    # Keep ATRP display readable as a first-pass presentation alias.
    text = re.sub(r"\bATRP_(\d+(?:\.\d+)?)\b", r"ATR%(\1)", text)

    return text


# ----------------------------
# Indicator family / doc helpers (Phase III education UX)
# ----------------------------
def get_indicator_family(row_key: str) -> str:
    """
    Resolve a row key like EMA_20 or MACD_12_26_9 to an indicator family name.

    This is intentionally adapter-owned because row-key interpretation belongs
    with the adapter metadata layer, not the Streamlit layout layer.
    """
    if not row_key:
        return ""

    # Crossover rows must be resolved before generic EMA_/SMA_ prefix checks.
    # Otherwise EMA_9_X_EMA_21 would be treated as EMA and SMA crossover rows
    # would be treated as SMA.
    if row_key in {
        "EMA_9_X_EMA_21",
        "SMA_20_X_SMA_50",
        "SMA_50_X_SMA_200",
    }:
        return "Crossover"

    if row_key.startswith("EMA_"):
        return "EMA"
    if row_key.startswith("SMA_"):
        return "SMA"
    if row_key.startswith("VWMA_"):
        return "VWMA"
    if row_key.startswith("HMA_"):
        return "HMA"
    if row_key.startswith("RSI_"):
        return "RSI"
    if row_key.startswith("MACD_"):
        return "MACD"
    if row_key.startswith("STOCH_"):
        return "STOCH"
    if row_key.startswith("ROC_"):
        return "ROC"
    if row_key.startswith("WILLR_"):
        return "WILLR"
    if row_key.startswith("ADX_"):
        return "ADX"
    if row_key.startswith("ATR_"):
        return "ATR"
    if row_key.startswith("ATRP_"):
        return "ATR"
    if row_key.startswith("MFI_"):
        return "MFI"
    if row_key.startswith("CMF_"):
        return "CMF"
    if row_key.startswith("CCI_"):
        return "CCI"
    if row_key.startswith("UO_"):
        return "UO"
    if row_key.startswith("DPO_"):
        return "DPO"
    if row_key == "OBV" or row_key.startswith("OBV_"):
        return "OBV"
    if row_key.startswith("BullBearPower_"):
        return "BullBearPower"

    # Future-proofed even if currently deferred / out of scope
    if row_key.startswith("BB_") or row_key.startswith("BOLL_") or row_key.startswith("Bollinger"):
        return "Bollinger"

# In `get_indicator_family()` but not here (a/o 4/22/26)
#    if row_key.startswith("SMA_"):
#        return "SMA"
#    if row_key.startswith("ATR_"):
#        return "ATR"
#    if row_key.startswith("ATRP_"):
#        return "ATR"

#    # Future-proofed even if currently deferred / out of scope
#    if row_key.startswith("BB_") or row_key.startswith("BOLL_") or row_key.startswith("Bollinger"):
#        return "Bollinger"

    return row_key


def get_indicator_doc_slug(row_key: str) -> str:
    """
    Resolve the markdown documentation slug for a row key.

    Initially this matches the indicator family, but it is intentionally
    separated so documentation structure can diverge later without changing
    UI call sites.
    """
    return get_indicator_family(row_key)

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

    # Date -> current price map for indicator-specific hover context
    price_values = list(price_block.get("values", [])) if isinstance(price_block, dict) else []
    if len(price_values) < len(raw_dates):
        price_values = price_values + [None] * (len(raw_dates) - len(price_values))
    price_by_date = dict(zip(raw_dates, price_values))

    def _normalize_hover_date_key(value: Any) -> str:
        """Return YYYY-MM-DD where possible for adapter-local date lookups."""
        try:
            return pd.Timestamp(value).strftime("%Y-%m-%d")
        except Exception:
            return str(value)[:10]

    def _lookup_hover_mapping(mapping: Dict[str, Any], date_value: Any, default: Any = None) -> Any:
        """Lookup adapter-local date maps using normalized and raw date keys."""
        normalized_key = _normalize_hover_date_key(date_value)
        if normalized_key in mapping:
            return mapping.get(normalized_key)

        raw_key = str(date_value)
        if raw_key in mapping:
            return mapping.get(raw_key)

        return default

    # Date -> OHLCV / computed-indicator row map for hover-only context.
    # This consumes already-computed indicator columns from ohlcv_df.
    # It does not create new score, signal, rule, or numeric-layer truth.
    ohlcv_by_date: Dict[str, Dict[str, Any]] = {}
    close_history_by_date: Dict[str, List[float]] = {}

    if ohlcv_df is not None:
        try:
            hover_df = ohlcv_df.copy().sort_index()

            # Hover-only support for next-bar SMA crossover projection.
            # These helper columns are not score truth, rule truth, or numeric-layer
            # outputs. They are adapter-local context derived from existing OHLCV.
            close_col = "Adj Close" if "Adj Close" in hover_df.columns else "Close"
            if close_col in hover_df.columns:
                close_series = pd.to_numeric(hover_df[close_col], errors="coerce")

                # Keep enough trailing close history to simulate SMA crossover
                # behavior under a constant-close future-price assumption.
                max_crossover_sma_len = 200
                raw_date_keys = [str(idx_val) for idx_val in hover_df.index]
                normalized_date_keys = [
                    _normalize_hover_date_key(idx_val)
                    for idx_val in hover_df.index
                ]
                close_values = close_series.tolist()

                for pos, normalized_date_key in enumerate(normalized_date_keys):
                    start_pos = max(0, pos - max_crossover_sma_len + 1)
                    trailing_values = close_values[start_pos : pos + 1]
                    trailing_history = [
                        float(value)
                        for value in trailing_values
                        if not _is_missing(value)
                    ]

                    close_history_by_date[normalized_date_key] = trailing_history

                    raw_date_key = raw_date_keys[pos]
                    if raw_date_key != normalized_date_key:
                        close_history_by_date[raw_date_key] = trailing_history

                for sma_len in (20, 50, 200):
                    hover_df[f"__SMA_SUM_{sma_len}"] = (
                        close_series.rolling(sma_len, min_periods=sma_len).sum()
                    )
                    hover_df[f"__SMA_OLDEST_{sma_len}"] = close_series.shift(sma_len - 1)

            hover_df.index = hover_df.index.astype(str)
            hover_records = hover_df.to_dict(orient="index")
            ohlcv_by_date = {}

            for raw_date_key, row_dict in hover_records.items():
                normalized_date_key = _normalize_hover_date_key(raw_date_key)

                ohlcv_by_date[raw_date_key] = row_dict
                ohlcv_by_date[normalized_date_key] = row_dict

        except Exception:
            ohlcv_by_date = {}
            close_history_by_date = {}

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

    crossover_specs = {
        "EMA_9_X_EMA_21": {
            "ma_type": "EMA",
            "fast_col": "EMA_9",
            "slow_col": "EMA_21",
            "fast_label": "EMA(9)",
            "slow_label": "EMA(21)",
            "fast_len": 9,
            "slow_len": 21,
        },
        "SMA_20_X_SMA_50": {
            "ma_type": "SMA",
            "fast_col": "SMA_20",
            "slow_col": "SMA_50",
            "fast_label": "SMA(20)",
            "slow_label": "SMA(50)",
            "fast_len": 20,
            "slow_len": 50,
        },
        "SMA_50_X_SMA_200": {
            "ma_type": "SMA",
            "fast_col": "SMA_50",
            "slow_col": "SMA_200",
            "fast_label": "SMA(50)",
            "slow_label": "SMA(200)",
            "fast_len": 50,
            "slow_len": 200,
        },
    }

    CROSSOVER_MAX_REQUIRED_MOVE_PCT = 20.0
    CROSSOVER_MAX_ESTIMATED_DAYS = 60
    CROSSOVER_MAX_SIMULATION_BARS = 60

    def _is_crossover_key(indicator_key: str) -> bool:
        return indicator_key in crossover_specs

    def _to_float_or_none(value: Any) -> Optional[float]:
        if _is_missing(value):
            return None
        try:
            return float(value)
        except Exception:
            return None

    def _format_value_with_delta(
        *,
        label: str,
        curr_value: Any,
        prev_value: Any,
        decimals: int = 2,
        prefix: str = "",
    ) -> str:
        curr_float = _to_float_or_none(curr_value)
        if curr_float is None:
            return ""

        prev_float = _to_float_or_none(prev_value)
        delta_abs = None
        if prev_float is not None:
            delta_abs = curr_float - prev_float

        delta_pct = safe_pct_delta(curr_float, prev_float)

        suffix = ""
        if delta_abs is not None or delta_pct is not None:
            suffix = (
                f" ({format_signed_number(delta_abs, decimals=decimals)}"
                f"{f', {format_signed_percent(delta_pct, decimals=1)}' if delta_pct is not None else ''})"
            )

        return f"{label}: {prefix}{curr_float:,.{decimals}f}{suffix}"

    def _format_price_value(value: Any) -> str:
        value_float = _to_float_or_none(value)
        if value_float is None:
            return ""
        return f"${value_float:,.2f}"

    def _format_spread_pct_of_price_line(
        *,
        spread_value: Any,
        price_value: Any,
        prev_spread_value: Any,
        prev_price_value: Any,
    ) -> str:
        spread_float = _to_float_or_none(spread_value)
        price_float = _to_float_or_none(price_value)

        if spread_float is None or price_float is None or price_float <= 0:
            return ""

        spread_pct = (spread_float / price_float) * 100.0

        prev_spread_float = _to_float_or_none(prev_spread_value)
        prev_price_float = _to_float_or_none(prev_price_value)

        suffix = ""
        if (
            prev_spread_float is not None
            and prev_price_float is not None
            and prev_price_float > 0
        ):
            prev_spread_pct = (prev_spread_float / prev_price_float) * 100.0
            bps_delta = (spread_pct - prev_spread_pct) * 100.0
            suffix = f" ({bps_delta:+.0f} bps vs. prior day)"

        return f"Spread % of Price: {format_signed_percent(spread_pct, decimals=2)}{suffix}"

    def _format_ma_vs_price_line(
        *,
        label: str,
        ma_value: Any,
        price_value: Any,
    ) -> str:
        ma_float = _to_float_or_none(ma_value)
        price_float = _to_float_or_none(price_value)

        if ma_float is None:
            return ""

        suffix = ""
        if price_float is not None and price_float > 0:
            pct_vs_price = ((ma_float / price_float) - 1.0) * 100.0
            suffix = f" ({format_signed_percent(pct_vs_price, decimals=1)} vs. price)"

        return f"{label}: ${ma_float:,.2f}{suffix}"

    def _has_crossover_between(prev_spread: float, current_spread: float) -> bool:
        if prev_spread > 0 and current_spread <= 0:
            return True
        if prev_spread < 0 and current_spread >= 0:
            return True
        return False

    def _simulate_sma_constant_close_projection(
        *,
        spec: Dict[str, Any],
        close_history: List[float],
        current_price: Any,
        spread_value: Any,
    ) -> Tuple[Optional[int], Optional[float], Optional[str]]:
        """
        Simulate future SMA crossover timing under a constant-close assumption.

        Returns:
            projected bars to cross,
            projected MA cross level,
            reason when unavailable.

        This is hover-only projection metadata.
        """
        current_price_float = _to_float_or_none(current_price)
        spread_float = _to_float_or_none(spread_value)

        if current_price_float is None or current_price_float <= 0:
            return None, None, "current price unavailable"

        if spread_float is None:
            return None, None, "insufficient spread history"

        try:
            fast_len = int(spec.get("fast_len"))
            slow_len = int(spec.get("slow_len"))
        except Exception:
            return None, None, "invalid crossover parameters"

        if fast_len <= 0 or slow_len <= 0 or fast_len == slow_len:
            return None, None, "invalid crossover parameters"

        required_len = max(fast_len, slow_len)
        history = [
            float(value)
            for value in close_history
            if not _is_missing(value)
        ]

        if len(history) < required_len:
            return None, None, "insufficient close history"

        simulated_closes = list(history[-required_len:])
        prev_spread_float = spread_float

        if abs(prev_spread_float) <= 1e-12:
            current_level = sum(simulated_closes[-fast_len:]) / fast_len
            return 0, current_level, None

        for bars_ahead in range(1, CROSSOVER_MAX_SIMULATION_BARS + 1):
            simulated_closes.append(current_price_float)

            fast_ma = sum(simulated_closes[-fast_len:]) / fast_len
            slow_ma = sum(simulated_closes[-slow_len:]) / slow_len
            current_spread_float = fast_ma - slow_ma

            if _has_crossover_between(prev_spread_float, current_spread_float):
                projected_level = (fast_ma + slow_ma) / 2.0
                return bars_ahead, projected_level, None

            prev_spread_float = current_spread_float

        return (
            None,
            None,
            f"no cross within {CROSSOVER_MAX_SIMULATION_BARS} bars at current close",
        )

    def _simulate_ema_constant_close_projection(
        *,
        spec: Dict[str, Any],
        fast_value: Any,
        slow_value: Any,
        current_price: Any,
        spread_value: Any,
    ) -> Tuple[Optional[int], Optional[float], Optional[str]]:
        """
        Simulate future EMA crossover timing under a constant-close assumption.

        Returns:
            projected bars to cross,
            projected MA cross level,
            reason when unavailable.

        This is hover-only projection metadata.
        """
        fast_float = _to_float_or_none(fast_value)
        slow_float = _to_float_or_none(slow_value)
        current_price_float = _to_float_or_none(current_price)
        spread_float = _to_float_or_none(spread_value)

        if fast_float is None or slow_float is None:
            return None, None, "insufficient MA history"

        if current_price_float is None or current_price_float <= 0:
            return None, None, "current price unavailable"

        if spread_float is None:
            return None, None, "insufficient spread history"

        try:
            fast_len = int(spec.get("fast_len"))
            slow_len = int(spec.get("slow_len"))
        except Exception:
            return None, None, "invalid crossover parameters"

        if fast_len <= 0 or slow_len <= 0 or fast_len == slow_len:
            return None, None, "invalid crossover parameters"

        alpha_fast = 2.0 / (fast_len + 1.0)
        alpha_slow = 2.0 / (slow_len + 1.0)

        prev_spread_float = spread_float

        if abs(prev_spread_float) <= 1e-12:
            return 0, (fast_float + slow_float) / 2.0, None

        simulated_fast = fast_float
        simulated_slow = slow_float

        for bars_ahead in range(1, CROSSOVER_MAX_SIMULATION_BARS + 1):
            simulated_fast = (
                alpha_fast * current_price_float
                + (1.0 - alpha_fast) * simulated_fast
            )
            simulated_slow = (
                alpha_slow * current_price_float
                + (1.0 - alpha_slow) * simulated_slow
            )
            current_spread_float = simulated_fast - simulated_slow

            if _has_crossover_between(prev_spread_float, current_spread_float):
                projected_level = (simulated_fast + simulated_slow) / 2.0
                return bars_ahead, projected_level, None

            prev_spread_float = current_spread_float

        return (
            None,
            None,
            f"no cross within {CROSSOVER_MAX_SIMULATION_BARS} bars at current close",
        )

    def _build_constant_close_projection_lines(
        *,
        spec: Dict[str, Any],
        close_history: List[float],
        fast_value: Any,
        slow_value: Any,
        current_price: Any,
        spread_value: Any,
        event_value: Any,
    ) -> Tuple[str, str]:
        """
        Build hover lines for constant-close crossover simulation.

        This answers:
            If future closes stay at the current close, how many bars until
            the fast and slow moving averages cross?
        """
        current_price_float = _to_float_or_none(current_price)

        event_float = _to_float_or_none(event_value)
        if event_float is not None and abs(event_float) > 0.5:
            level_float = None
            fast_float = _to_float_or_none(fast_value)
            slow_float = _to_float_or_none(slow_value)
            if fast_float is not None and slow_float is not None:
                level_float = (fast_float + slow_float) / 2.0

            level_line = "Projected Cross Level: N/A - crossover event on this date"
            if level_float is not None:
                level_line = f"Projected Cross Level: ~${level_float:,.2f} - crossover event on this date"

            return (
                "Projected Bars to Cross: 0 trading days - crossover event on this date",
                level_line,
            )

        ma_type = str(spec.get("ma_type", "")).upper()

        if ma_type == "SMA":
            bars_to_cross, projected_level, reason = _simulate_sma_constant_close_projection(
                spec=spec,
                close_history=close_history,
                current_price=current_price,
                spread_value=spread_value,
            )
        elif ma_type == "EMA":
            bars_to_cross, projected_level, reason = _simulate_ema_constant_close_projection(
                spec=spec,
                fast_value=fast_value,
                slow_value=slow_value,
                current_price=current_price,
                spread_value=spread_value,
            )
        else:
            bars_to_cross, projected_level, reason = None, None, "unsupported crossover type"

        if bars_to_cross is None:
            return (
                f"Projected Bars to Cross: N/A - {reason}",
                "Projected Cross Level: N/A - no projected cross level",
            )

        day_word = "day" if bars_to_cross == 1 else "days"
        bars_line = (
            f"Projected Bars to Cross: {bars_to_cross} trading {day_word} "
            "- constant-close simulation"
        )

        if projected_level is None:
            level_line = "Projected Cross Level: N/A - no projected cross level"
        elif current_price_float is not None and current_price_float > 0:
            level_line = (
                f"Projected Cross Level: ~${projected_level:,.2f} "
                f"- assumes future closes stay near ${current_price_float:,.2f}"
            )
        else:
            level_line = f"Projected Cross Level: ~${projected_level:,.2f}"

        return bars_line, level_line
        
    def _days_between(date_a: Any, date_b: Any) -> Optional[int]:
        try:
            d0 = datetime.fromisoformat(str(date_a)[:10])
            d1 = datetime.fromisoformat(str(date_b)[:10])
            return abs((d0 - d1).days)
        except Exception:
            return None

    def _event_direction(value: Any) -> str:
        event_value = _to_float_or_none(value)
        if event_value is None:
            return "Insufficient data"
        if event_value > 0.5:
            return "Bullish crossover"
        if event_value < -0.5:
            return "Bearish crossover"
        return "No crossover event"

    def _days_since_last_crossover(values: List[Any], dates: List[Any], idx: int) -> Optional[int]:
        if idx < 0 or idx >= len(values) or idx >= len(dates):
            return None

        current_date = dates[idx]
        for prior_idx in range(idx, -1, -1):
            prior_value = _to_float_or_none(values[prior_idx])
            if prior_value is None:
                continue
            if abs(prior_value) > 0.5:
                return _days_between(current_date, dates[prior_idx])

        return None

    def _resolve_crossover_cross_type(
        *,
        event_value: Any,
        spread_value: Any,
    ) -> str:
        """
        Return the active/next crossover direction for hover display only.

        Event days use the event value directly. Non-event days infer the next
        possible cross direction from current spread:
          spread < 0 -> fast MA is below slow MA -> next cross is Bullish
          spread > 0 -> fast MA is above slow MA -> next cross is Bearish
        """
        event_float = _to_float_or_none(event_value)
        if event_float is not None:
            if event_float > 0.5:
                return "Bullish"
            if event_float < -0.5:
                return "Bearish"

        spread_float = _to_float_or_none(spread_value)
        if spread_float is None:
            return "N/A"
        if spread_float < 0:
            return "Bullish"
        if spread_float > 0:
            return "Bearish"
        return "At crossover boundary"

    def _calculate_sma_next_cross_required_price(
        *,
        current_row: Dict[str, Any],
        fast_len: Any,
        slow_len: Any,
    ) -> Tuple[Optional[float], Optional[str]]:
        """
        Return the next close required for next-bar SMA fast == SMA slow.

        Formula:
            SMA_fast_next = (fast_sum_current - fast_oldest + X) / fast_len
            SMA_slow_next = (slow_sum_current - slow_oldest + X) / slow_len

        Solving fast == slow:
            X = (fast_len * slow_sum_after_drop - slow_len * fast_sum_after_drop)
                / (slow_len - fast_len)

        This is hover-only projection metadata.
        """
        try:
            fast_len = int(fast_len)
            slow_len = int(slow_len)
        except Exception:
            return None, "invalid crossover parameters"

        if fast_len <= 0 or slow_len <= 0 or fast_len == slow_len:
            return None, "invalid crossover parameters"

        fast_sum = _to_float_or_none(current_row.get(f"__SMA_SUM_{fast_len}"))
        slow_sum = _to_float_or_none(current_row.get(f"__SMA_SUM_{slow_len}"))
        fast_oldest = _to_float_or_none(current_row.get(f"__SMA_OLDEST_{fast_len}"))
        slow_oldest = _to_float_or_none(current_row.get(f"__SMA_OLDEST_{slow_len}"))

        if (
            fast_sum is None
            or slow_sum is None
            or fast_oldest is None
            or slow_oldest is None
        ):
            return None, "insufficient MA history"

        fast_sum_after_drop = fast_sum - fast_oldest
        slow_sum_after_drop = slow_sum - slow_oldest

        denominator = slow_len - fast_len
        if denominator == 0:
            return None, "invalid crossover parameters"

        required_price = (
            (fast_len * slow_sum_after_drop)
            - (slow_len * fast_sum_after_drop)
        ) / denominator

        return required_price, None

    def _calculate_ema_next_cross_required_price(
        *,
        fast_value: Any,
        slow_value: Any,
        fast_len: Any,
        slow_len: Any,
    ) -> Tuple[Optional[float], Optional[str]]:
        """
        Return the next close required for next-bar EMA fast == EMA slow.

        Formula:
            EMA_fast_next = alpha_fast * X + (1 - alpha_fast) * EMA_fast_current
            EMA_slow_next = alpha_slow * X + (1 - alpha_slow) * EMA_slow_current

        Solving fast == slow:
            X = ((1 - alpha_slow) * slow_current
                 - (1 - alpha_fast) * fast_current)
                / (alpha_fast - alpha_slow)

        This is hover-only projection metadata.
        """
        fast_float = _to_float_or_none(fast_value)
        slow_float = _to_float_or_none(slow_value)

        if fast_float is None or slow_float is None:
            return None, "insufficient MA history"

        try:
            fast_len = int(fast_len)
            slow_len = int(slow_len)
        except Exception:
            return None, "invalid crossover parameters"

        if fast_len <= 0 or slow_len <= 0 or fast_len == slow_len:
            return None, "invalid crossover parameters"

        alpha_fast = 2.0 / (fast_len + 1.0)
        alpha_slow = 2.0 / (slow_len + 1.0)
        denominator = alpha_fast - alpha_slow

        if abs(denominator) <= 1e-12:
            return None, "invalid crossover parameters"

        required_price = (
            ((1.0 - alpha_slow) * slow_float)
            - ((1.0 - alpha_fast) * fast_float)
        ) / denominator

        return required_price, None

    def _calculate_next_cross_required_price(
        *,
        spec: Dict[str, Any],
        current_row: Dict[str, Any],
        fast_value: Any,
        slow_value: Any,
    ) -> Tuple[Optional[float], Optional[str]]:
        """Route required-price calculation by crossover MA type."""
        ma_type = str(spec.get("ma_type", "")).upper()
        fast_len = spec.get("fast_len")
        slow_len = spec.get("slow_len")

        if ma_type == "SMA":
            return _calculate_sma_next_cross_required_price(
                current_row=current_row,
                fast_len=fast_len,
                slow_len=slow_len,
            )

        if ma_type == "EMA":
            return _calculate_ema_next_cross_required_price(
                fast_value=fast_value,
                slow_value=slow_value,
                fast_len=fast_len,
                slow_len=slow_len,
            )

        return None, "unsupported crossover type"

    def _estimate_days_to_cross_line(
        *,
        spread_value: Any,
        prev_spread_value: Any,
    ) -> str:
        """
        Estimate days to cross using one-day spread velocity.

        This is intentionally labeled as a naive spread-velocity estimate.
        It is not a model, not a score, and not a trading forecast.
        """
        spread_float = _to_float_or_none(spread_value)
        prev_spread_float = _to_float_or_none(prev_spread_value)

        if spread_float is None or prev_spread_float is None:
            return "Estimated Days to Cross: N/A - insufficient spread history"

        if abs(spread_float) <= 1e-12:
            return "Estimated Days to Cross: 0 trading days - at crossover boundary"

        spread_delta = spread_float - prev_spread_float

        if abs(spread_delta) <= 1e-12:
            return "Estimated Days to Cross: N/A - spread is flat"

        # To move toward a bullish cross, negative spread must rise toward 0.
        if spread_float < 0 and spread_delta <= 0:
            return "Estimated Days to Cross: N/A - spread is widening"

        # To move toward a bearish cross, positive spread must fall toward 0.
        if spread_float > 0 and spread_delta >= 0:
            return "Estimated Days to Cross: N/A - spread is widening"

        estimated_days = int(np.ceil(abs(spread_float) / abs(spread_delta)))

        if estimated_days > CROSSOVER_MAX_ESTIMATED_DAYS:
            return (
                "Estimated Days to Cross: N/A - estimate exceeds "
                f"{CROSSOVER_MAX_ESTIMATED_DAYS} trading days"
            )

        day_word = "day" if estimated_days == 1 else "days"
        return (
            f"Estimated Days to Cross: {estimated_days} trading {day_word} "
            "- naive spread-velocity estimate"
        )

    def _build_crossover_projection_lines(
        *,
        spec: Dict[str, Any],
        current_row: Dict[str, Any],
        fast_value: Any,
        slow_value: Any,
        current_price: Any,
        event_value: Any,
        spread_value: Any,
        prev_spread_value: Any,
    ) -> Tuple[str, str, str]:
        """
        Build guarded projection lines for crossover hover display.

        Fields:
            Required Price for Cross
            Required Move
            Estimated Days to Cross

        All outputs are display-only hover metadata.
        """
        event_float = _to_float_or_none(event_value)
        if event_float is not None and abs(event_float) > 0.5:
            return (
                "Price Needed to Force Cross: Already crossed on this date",
                "Required Move: N/A - crossover event already occurred",
                "Estimated Days to Cross: 0 trading days - crossover event on this date",
            )

        required_price, reason = _calculate_next_cross_required_price(
            spec=spec,
            current_row=current_row,
            fast_value=fast_value,
            slow_value=slow_value,
        )

        estimated_days_line = _estimate_days_to_cross_line(
            spread_value=spread_value,
            prev_spread_value=prev_spread_value,
        )

        if reason:
            return (
                f"Price Needed to Force Cross: N/A - {reason}",
                f"Required Move: N/A - {reason}",
                estimated_days_line,
            )

        required_price_float = _to_float_or_none(required_price)
        if required_price_float is None:
            return (
                "Price Needed to Force Cross: N/A - insufficient MA history",
                "Required Move: N/A - insufficient MA history",
                estimated_days_line,
            )

        if required_price_float <= 0:
            return (
                "Price Needed to Force Cross: N/A - required price is not positive",
                "Required Move: N/A - required price is not positive",
                estimated_days_line,
            )

        current_price_float = _to_float_or_none(current_price)
        required_price_line = f"Price Needed to Force Cross: ${required_price_float:,.2f}"

        if current_price_float is None or current_price_float <= 0:
            return (
                required_price_line,
                "Required Move: N/A - current price unavailable",
                estimated_days_line,
            )

        required_move_abs = required_price_float - current_price_float
        required_move_pct = ((required_price_float / current_price_float) - 1.0) * 100.0

        guard_suffix = ""
        if abs(required_move_pct) > CROSSOVER_MAX_REQUIRED_MOVE_PCT:
            guard_suffix = " - impractical one-day trigger"

        required_move_line = (
            "Required Move: "
            f"{format_signed_number(required_move_abs, decimals=2)} "
            f"({format_signed_percent(required_move_pct, decimals=1)})"
            f"{guard_suffix}"
        )

        if guard_suffix:
            required_price_line = f"{required_price_line}{guard_suffix}"

        return required_price_line, required_move_line, estimated_days_line

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
        if _is_crossover_key(indicator_key):
            return "Crossover"
        if indicator_key.startswith("EMA_"):
            return "EMA"
        if indicator_key.startswith("SMA_"):
            return "SMA"
        if indicator_key.startswith("HMA_"):
            return "HMA"
        if indicator_key.startswith("CCI_"):
            return "CCI"
        if indicator_key.startswith("UO_"):
            return "Ultimate_Oscillator"
        if indicator_key.startswith("BullBearPower_"):
            return "BullBearPower"
        if indicator_key.startswith("VWMA_"):
            return "VWMA"
        if indicator_key.startswith("ATR_"):
            return "ATR"
        if indicator_key.startswith("BB_PCT_B") or indicator_key.startswith("BB_BW"):
            return "Bollinger"
        if indicator_key.startswith("DPO_"):
            return "DPO"
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
        if _is_crossover_key(indicator_key):
            return indicator_key
        # Explicit Bollinger display-row mappings
        if indicator_key == "BB_PCT_B_ST" or indicator_key == "BB_BW_ST":
            return "10_1.5"
        if indicator_key == "BB_PCT_B" or indicator_key == "BB_BW":
            return "20_2.0"
        if indicator_key == "BB_PCT_B_LT" or indicator_key == "BB_BW_LT":
            return "50_2.5"
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

            if rule_expr:
                if should_fallback_to_raw_rule(rule_expr):
                    # Keep complex expressions raw to preserve readability and accuracy.
                    # Token normalization / helper cleanup will still be handled in the
                    # translator path for simpler rules only.
                    rule_text = rule_expr
                else:
                    rule_text = translate_rule_text(rule_expr)
            else:
                rule_text = ""

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
            volume_10d_avg = {}
            volume_3m_avg = {}

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
                        volume_10d_avg = (
                            df["Volume"]
                            .rolling(10)
                            .mean()
                            .to_dict()
                        )
                        volume_3m_avg = (
                            df["Volume"]
                            .rolling(63)
                            .mean()
                            .to_dict()
                        )
                except Exception:
                    volume_series = {}
                    volume_5d_avg = {}
                    volume_10d_avg = {}
                    volume_3m_avg = {}

            def _format_volume_vs_avg_line(label: str, vol_value: Any, avg_value: Any) -> str:
                """Return a preformatted Price-row volume-vs-average hover line."""
                if _is_missing(vol_value) or _is_missing(avg_value):
                    return ""

                try:
                    avg_float = float(avg_value)
                    if avg_float == 0:
                        return ""

                    rel_pct = ((float(vol_value) - avg_float) / avg_float) * 100.0
                    return (
                        f"Volume vs {label}: {format_signed_percent(rel_pct, decimals=1)} "
                        f"({_abbr(avg_float)})<br>"
                    )
                except Exception:
                    return ""

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
                vol_5d_avg = volume_5d_avg.get(d_raw)
                vol_10d_avg = volume_10d_avg.get(d_raw)
                vol_3m_avg = volume_3m_avg.get(d_raw)

                vol_5d_rel = None
                if vol is not None and vol_5d_avg not in (None, 0):
                    try:
                        vol_5d_rel = ((float(vol) - float(vol_5d_avg)) / float(vol_5d_avg)) * 100.0
                    except Exception:
                        vol_5d_rel = None

                vol_10d_rel = None
                if vol is not None and vol_10d_avg not in (None, 0):
                    try:
                        vol_10d_rel = ((float(vol) - float(vol_10d_avg)) / float(vol_10d_avg)) * 100.0
                    except Exception:
                        vol_10d_rel = None

                vol_3m_rel = None
                if vol is not None and vol_3m_avg not in (None, 0):
                    try:
                        vol_3m_rel = ((float(vol) - float(vol_3m_avg)) / float(vol_3m_avg)) * 100.0
                    except Exception:
                        vol_3m_rel = None

                # ----------------------------
                # Preformatted hover fragments (Price-row)
                # ----------------------------
                delta_abs_fmt = format_signed_number(delta_abs, decimals=2)
                delta_pct_suffix = f" ({format_signed_percent(delta_pct, decimals=2)})" if delta_pct is not None else ""

                volume_block = ""
                if not _is_missing(vol):
                    volume_block = f"Volume: {_abbr(float(vol))}<br>"

                volume_vs_avg_block = (
                    _format_volume_vs_avg_line("5D", vol, vol_5d_avg)
                    + _format_volume_vs_avg_line("10D", vol, vol_10d_avg)
                    + _format_volume_vs_avg_line("3M", vol, vol_3m_avg)
                )

                # price row stays display-only / non-semantic
                trend_line = ""
                signal_line = ""
                rule_block = ""
                notes_block = ""
                definition_block = ""
                how_to_read_block = ""

                # ----------------------------
                # Customdata enrichment ('Price'-row)
                # ----------------------------
                cd_row.append(
                    {
                        "indicator_key": "__PRICE__",
                        "display_name": "Price",   # To get rid of "Price" "display_name": "",
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
                        "volume_5d_avg": vol_5d_avg,
                        "volume_10d_avg": vol_10d_avg,
                        "volume_3m_avg": vol_3m_avg,
                        "volume_vs_5d_avg_pct": vol_5d_rel,
                        "volume_vs_10d_avg_pct": vol_10d_rel,
                        "volume_vs_3m_avg_pct": vol_3m_rel,

                        # Custom indicator-specific content
                        "macd_context_block": "",
                        "adx_context_block": "",
                        "stoch_context_block": "",
                        "bullbear_context_block": "",
                        "dpo_context_block": "",
                        "band_context_block": "",
                        "ma_context_block": "",
                        "crossover_context_block": "",
                        "crossover_summary_block": "",

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
                        "delta_line": f"Δ vs prior day: {delta_abs_fmt}{delta_pct_suffix}<br>",
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
        row_extras = list(row.get("extras", []))

        # Normalize lengths (defensive)
        if len(values) < len(x):
            values = values + [None] * (len(x) - len(values))
        if len(scores) < len(x):
            scores = scores + [None] * (len(x) - len(scores))
        if len(row_extras) < len(x):
            row_extras = row_extras + [{}] * (len(x) - len(row_extras))

        row_keys.append(key)
        y.append(display_name)

        z_row: List[float] = []
        text_row: List[str] = []
        cd_row: List[dict] = []

        for idx, (d_raw, v, s, extra_map) in enumerate(zip(raw_dates, values, scores, row_extras)):        
            prev_v = values[idx - 1] if idx > 0 else None
            prev_extra_map = row_extras[idx - 1] if idx > 0 else {}

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

            macd_context_block = ""
            stoch_context_block = ""
            bullbear_context_block = ""
            dpo_context_block = ""
            band_context_block = ""
            ma_context_block = ""
            adx_context_block = ""
            crossover_context_block = ""
            crossover_summary_block = ""
            crossover_cell_text = ""
            crossover_spread = None

            # MACD: Custom hover content (deltas) 
            if key.startswith("MACD_") and isinstance(extra_map, dict) and extra_map:
                parts = []

                prev_extra_map = row_extras[idx - 1] if idx > 0 else {}

                macd_line = extra_map.get("macd_line")
                prev_macd_line = prev_extra_map.get("macd_line") if isinstance(prev_extra_map, dict) else None

                macd_line_delta_abs = None
                if not _is_missing(macd_line) and not _is_missing(prev_macd_line):
                    try:
                        macd_line_delta_abs = float(macd_line) - float(prev_macd_line)
                    except Exception:
                        macd_line_delta_abs = None

                macd_line_delta_pct = safe_pct_delta(macd_line, prev_macd_line)

                if not _is_missing(macd_line):
                    macd_line_suffix = ""
                    if macd_line_delta_abs is not None or macd_line_delta_pct is not None:
                        macd_line_suffix = (
                            f" ({format_signed_number(macd_line_delta_abs, decimals=2)}"
                            f"{f', {format_signed_percent(macd_line_delta_pct, decimals=1)}' if macd_line_delta_pct is not None else ''})"
                        )
                    parts.append(f"MACD Line: {format_signed_number(macd_line, decimals=2)}{macd_line_suffix}")

                macd_signal = extra_map.get("macd_signal")
                prev_macd_signal = prev_extra_map.get("macd_signal") if isinstance(prev_extra_map, dict) else None

                macd_signal_delta_abs = None
                if not _is_missing(macd_signal) and not _is_missing(prev_macd_signal):
                    try:
                        macd_signal_delta_abs = float(macd_signal) - float(prev_macd_signal)
                    except Exception:
                        macd_signal_delta_abs = None

                macd_signal_delta_pct = safe_pct_delta(macd_signal, prev_macd_signal)

                if not _is_missing(macd_signal):
                    macd_signal_suffix = ""
                    if macd_signal_delta_abs is not None or macd_signal_delta_pct is not None:
                        macd_signal_suffix = (
                            f" ({format_signed_number(macd_signal_delta_abs, decimals=2)}"
                            f"{f', {format_signed_percent(macd_signal_delta_pct, decimals=1)}' if macd_signal_delta_pct is not None else ''})"
                        )
                    parts.append(f"Signal Line: {format_signed_number(macd_signal, decimals=2)}{macd_signal_suffix}")

                if parts:
                    macd_context_block = "<br>" + "<br>".join(parts) + "<br>"

            # STOCH: Custom hover content (deltas)
            if key.startswith("STOCH_") and isinstance(extra_map, dict) and extra_map:
                parts = []

                stoch_d = extra_map.get("stoch_d")
                prev_stoch_d = prev_extra_map.get("stoch_d") if isinstance(prev_extra_map, dict) else None

                stoch_d_delta_abs = None
                if not _is_missing(stoch_d) and not _is_missing(prev_stoch_d):
                    try:
                        stoch_d_delta_abs = float(stoch_d) - float(prev_stoch_d)
                    except Exception:
                        stoch_d_delta_abs = None

                stoch_d_delta_pct = safe_pct_delta(stoch_d, prev_stoch_d)

                if not _is_missing(stoch_d):
                    parts.append(
                        f"%D: {format_signed_number(stoch_d, decimals=2)} "
                        f"({format_signed_number(stoch_d_delta_abs, decimals=2)}"
                        f"{f', {format_signed_percent(stoch_d_delta_pct, decimals=1)}' if stoch_d_delta_pct is not None else ''})"
                    )

                if parts:
                    stoch_context_block = "<br>" + "<br>".join(parts) + "<br>"

            # DPO: Custom hover content (raw value + deltas)
            if key.startswith("DPO_") and isinstance(extra_map, dict) and extra_map:
                parts = []

                raw_dpo = extra_map.get("raw_dpo")
                dpo_delta = extra_map.get("dpo_delta")
                dpo_delta_pct = extra_map.get("dpo_delta_pct")

                if not _is_missing(v):
                    parts.append(f"DPO % of price: {format_signed_number(v, decimals=2)}%")

                if not _is_missing(raw_dpo):
                    parts.append(f"Raw DPO: {format_signed_number(raw_dpo, decimals=2)}")

                if not _is_missing(dpo_delta):
                    parts.append(
                        f"Raw DPO Δ vs prior day: {format_signed_number(dpo_delta, decimals=2)}"
                    )

                if not _is_missing(dpo_delta_pct):
                    parts.append(
                        f"DPO % Δ vs prior day: {format_signed_number(dpo_delta_pct, decimals=2)} pct pts"
                    )

                if parts:
                    dpo_context_block = "<br>" + "<br>".join(parts) + "<br>"

            # BULL BEAR: Custom hover content (deltas)
            if key.startswith("BullBearPower_") and isinstance(extra_map, dict) and extra_map:
                parts = []

                bull_val = extra_map.get("BullPower")
                prev_bull_val = prev_extra_map.get("BullPower") if isinstance(prev_extra_map, dict) else None
                bear_val = extra_map.get("BearPower")
                prev_bear_val = prev_extra_map.get("BearPower") if isinstance(prev_extra_map, dict) else None

                bull_delta_abs = None
                if not _is_missing(bull_val) and not _is_missing(prev_bull_val):
                    try:
                        bull_delta_abs = float(bull_val) - float(prev_bull_val)
                    except Exception:
                        bull_delta_abs = None
                bull_delta_pct = safe_pct_delta(bull_val, prev_bull_val)

                bear_delta_abs = None
                if not _is_missing(bear_val) and not _is_missing(prev_bear_val):
                    try:
                        bear_delta_abs = float(bear_val) - float(prev_bear_val)
                    except Exception:
                        bear_delta_abs = None
                bear_delta_pct = safe_pct_delta(bear_val, prev_bear_val)

                if not _is_missing(bull_val):
                    bull_suffix = ""
                    if bull_delta_abs is not None or bull_delta_pct is not None:
                        bull_suffix = (
                            f" ({format_signed_number(bull_delta_abs, decimals=2)}"
                            f"{f', {format_signed_percent(bull_delta_pct, decimals=1)}' if bull_delta_pct is not None else ''})"
                        )
                    parts.append(f"Bull: {format_signed_number(bull_val, decimals=2)}{bull_suffix}")

                if not _is_missing(bear_val):
                    bear_suffix = ""
                    if bear_delta_abs is not None or bear_delta_pct is not None:
                        bear_suffix = (
                            f" ({format_signed_number(bear_delta_abs, decimals=2)}"
                            f"{f', {format_signed_percent(bear_delta_pct, decimals=1)}' if bear_delta_pct is not None else ''})"
                        )
                    parts.append(f"Bear: {format_signed_number(bear_val, decimals=2)}{bear_suffix}")

                if parts:
                    bullbear_context_block = "<br>" + "<br>".join(parts) + "<br>"

            # ADX: Custom hover content (+DI / -DI / spread with deltas)
            if key.startswith("ADX_"):
                parts = []

                length_part = key.split("_", 1)[1] if "_" in key else ""
                dip_col = f"DIp_{length_part}"
                din_col = f"DIn_{length_part}"

                current_row = ohlcv_by_date.get(str(d_raw), {})
                prev_date = raw_dates[idx - 1] if idx > 0 else None
                prev_row = ohlcv_by_date.get(str(prev_date), {}) if prev_date is not None else {}

                dip_val = current_row.get(dip_col) if isinstance(current_row, dict) else None
                din_val = current_row.get(din_col) if isinstance(current_row, dict) else None
                prev_dip_val = prev_row.get(dip_col) if isinstance(prev_row, dict) else None
                prev_din_val = prev_row.get(din_col) if isinstance(prev_row, dict) else None

                def _format_adx_component_line(label: str, curr_value: Any, prev_value: Any) -> str:
                    """Return an ADX component line with value, absolute delta, and relative delta."""
                    if _is_missing(curr_value):
                        return ""

                    delta_abs = None
                    if not _is_missing(prev_value):
                        try:
                            delta_abs = float(curr_value) - float(prev_value)
                        except Exception:
                            delta_abs = None

                    delta_pct = safe_pct_delta(curr_value, prev_value)

                    suffix = ""
                    if delta_abs is not None or delta_pct is not None:
                        suffix = (
                            f" ({format_signed_number(delta_abs, decimals=2)}"
                            f"{f', {format_signed_percent(delta_pct, decimals=1)}' if delta_pct is not None else ''})"
                        )

                    return f"{label}: {float(curr_value):.2f}{suffix}"

                dip_line = _format_adx_component_line("+DI", dip_val, prev_dip_val)
                if dip_line:
                    parts.append(dip_line)

                din_line = _format_adx_component_line("-DI", din_val, prev_din_val)
                if din_line:
                    parts.append(din_line)

                spread_val = None
                prev_spread_val = None

                if not _is_missing(dip_val) and not _is_missing(din_val):
                    try:
                        spread_val = float(dip_val) - float(din_val)
                    except Exception:
                        spread_val = None

                if not _is_missing(prev_dip_val) and not _is_missing(prev_din_val):
                    try:
                        prev_spread_val = float(prev_dip_val) - float(prev_din_val)
                    except Exception:
                        prev_spread_val = None

                if spread_val is not None:
                    spread_delta_abs = None
                    if prev_spread_val is not None:
                        try:
                            spread_delta_abs = float(spread_val) - float(prev_spread_val)
                        except Exception:
                            spread_delta_abs = None

                    spread_delta_pct = safe_pct_delta(spread_val, prev_spread_val)

                    spread_suffix = ""
                    if spread_delta_abs is not None or spread_delta_pct is not None:
                        spread_suffix = (
                            f" ({format_signed_number(spread_delta_abs, decimals=2)}"
                            f"{f', {format_signed_percent(spread_delta_pct, decimals=1)}' if spread_delta_pct is not None else ''})"
                        )

                    parts.append(
                        f"Spread: {format_signed_number(spread_val, decimals=2)}{spread_suffix}"
                    )

                if parts:
                    adx_context_block = "<br>" + "<br>".join(parts) + "<br>"

            # ----------------------------
            # Preformatted hover fragments ('Indicator'-row)
            # ----------------------------
            delta_abs_fmt = format_signed_number(delta_abs, decimals=2)
            delta_pct_suffix = f" ({format_signed_percent(delta_pct, decimals=2)})" if delta_pct is not None else ""
            delta_line = "" if _is_crossover_key(key) else (
                f"Δ vs prior day: {delta_abs_fmt}{delta_pct_suffix}<br>"
            )
            trend_line = "" if _is_crossover_key(key) else (f"Trend: {trend}<br>" if trend else "")
            signal_line = f"<br>Signal: {score_label}<br>" if score_label else ""
            rule_block = _format_hover_block("Rule", rule_text, width=80)
            notes_block = _format_hover_block("Notes", rule_notes, width=72)
            definition_block = _format_hover_block("Definition", definition, width=72)
            how_to_read_block = _format_hover_block("How to Read", how_to_read, width=72)

            # indicator rows do not use volume hover fields
            volume_block = ""
            volume_vs_avg_block = ""

            # CROSSOVER: Custom hover content using already-computed MA context.
            # This avoids treating the event value itself as an EMA/SMA value.
            if _is_crossover_key(key):
                spec = crossover_specs.get(key, {})
                current_row = _lookup_hover_mapping(ohlcv_by_date, d_raw, {})
                prev_date = raw_dates[idx - 1] if idx > 0 else None
                prev_row = (
                    _lookup_hover_mapping(ohlcv_by_date, prev_date, {})
                    if prev_date is not None
                    else {}
                )

                fast_col = spec.get("fast_col")
                slow_col = spec.get("slow_col")
                fast_label = spec.get("fast_label", "Fast MA")
                slow_label = spec.get("slow_label", "Slow MA")

                fast_val = current_row.get(fast_col) if isinstance(current_row, dict) else None
                slow_val = current_row.get(slow_col) if isinstance(current_row, dict) else None
                prev_fast_val = prev_row.get(fast_col) if isinstance(prev_row, dict) else None
                prev_slow_val = prev_row.get(slow_col) if isinstance(prev_row, dict) else None

                price_val = price_by_date.get(d_raw)
                prev_price_val = price_by_date.get(prev_date) if prev_date is not None else None

                spread_val = None
                prev_spread_val = None

                fast_float = _to_float_or_none(fast_val)
                slow_float = _to_float_or_none(slow_val)
                prev_fast_float = _to_float_or_none(prev_fast_val)
                prev_slow_float = _to_float_or_none(prev_slow_val)

                if fast_float is not None and slow_float is not None:
                    spread_val = fast_float - slow_float

                if prev_fast_float is not None and prev_slow_float is not None:
                    prev_spread_val = prev_fast_float - prev_slow_float

                event_direction = _event_direction(v)
                event_value = _to_float_or_none(v)
                days_since = _days_since_last_crossover(values, raw_dates, idx)

                cross_type = _resolve_crossover_cross_type(
                    event_value=v,
                    spread_value=spread_val,
                )

                spread_line = _format_value_with_delta(
                    label="Spread",
                    curr_value=spread_val,
                    prev_value=prev_spread_val,
                    decimals=2,
                )

                price_line = _format_value_with_delta(
                    label="Price",
                    curr_value=price_val,
                    prev_value=prev_price_val,
                    decimals=2,
                    prefix="$",
                )

                if spread_line and price_line:
                    crossover_summary_line = f"{spread_line} | {price_line}"
                elif spread_line:
                    crossover_summary_line = spread_line
                elif price_line:
                    crossover_summary_line = price_line
                else:
                    crossover_summary_line = ""

                crossover_summary_block = (
                    f"{crossover_summary_line}<br>"
                    if crossover_summary_line
                    else ""
                )

                parts = []

                spread_pct_line = _format_spread_pct_of_price_line(
                    spread_value=spread_val,
                    price_value=price_val,
                    prev_spread_value=prev_spread_val,
                    prev_price_value=prev_price_val,
                )
                if spread_pct_line:
                    parts.append(spread_pct_line)
                    parts.append("")

                fast_line = _format_ma_vs_price_line(
                    label="Fast MA",
                    ma_value=fast_val,
                    price_value=price_val,
                )
                if fast_line:
                    parts.append(fast_line)

                slow_line = _format_ma_vs_price_line(
                    label="Slow MA",
                    ma_value=slow_val,
                    price_value=price_val,
                )
                if slow_line:
                    parts.append(slow_line)

                parts.append("")

                parts.append(f"Cross type: {cross_type}")

                close_history = _lookup_hover_mapping(close_history_by_date, d_raw, [])
                projected_bars_line, projected_level_line = (
                    _build_constant_close_projection_lines(
                        spec=spec,
                        close_history=close_history,
                        fast_value=fast_val,
                        slow_value=slow_val,
                        current_price=price_val,
                        spread_value=spread_val,
                        event_value=v,
                    )
                )

                required_price_line, required_move_line, estimated_days_line = (
                    _build_crossover_projection_lines(
                        spec=spec,
                        current_row=current_row,
                        fast_value=fast_val,
                        slow_value=slow_val,
                        current_price=price_val,
                        event_value=v,
                        spread_value=spread_val,
                        prev_spread_value=prev_spread_val,
                    )
                )

                parts.append(projected_bars_line)
                parts.append(projected_level_line)
                parts.append("")
                parts.append(required_price_line)
                parts.append(required_move_line)
                parts.append(estimated_days_line)
                parts.append("")

                parts.append(f"Event: {event_direction}")

                if event_value is not None:
                    parts.append(f"Event value: {event_value:.0f}")

                if days_since is not None:
                    parts.append(f"Days since last crossover: {days_since}")
                else:
                    parts.append("Days since last crossover: N/A - no prior event in window")

                parts.append("Condition:")
                parts.append("Bullish = prior spread <= 0 and current spread > 0")
                parts.append("Bearish = prior spread >= 0 and current spread < 0")

                crossover_context_block = "<br>".join(parts) + "<br>"

                if spread_val is not None:
                    crossover_spread = spread_val
                    crossover_cell_text = format_signed_number(spread_val, decimals=2)

            # BOLLINGERS: Custom hover content (deltas)
            #if key in {"BB_PCT_B", "BB_BW"} and isinstance(extra_map, dict) and extra_map:
            if key in {"BB_PCT_B_ST", "BB_BW_ST", "BB_PCT_B", "BB_BW", "BB_PCT_B_LT", "BB_BW_LT"} and isinstance(extra_map, dict) and extra_map:
                parts = []
                current_price = price_by_date.get(d_raw)

                try:
                    current_price = float(current_price) if not _is_missing(current_price) else None
                except Exception:
                    current_price = None

                for band_key, label_txt in (("mid", "Mid"), ("upper", "Upper"), ("lower", "Lower")):
                    band_val = extra_map.get(band_key)
                    if _is_missing(band_val):
                        continue

                    pct_vs_price = None
                    if current_price not in (None, 0):
                        try:
                            pct_vs_price = ((float(band_val) / float(current_price)) - 1.0) * 100.0
                        except Exception:
                            pct_vs_price = None

                    if pct_vs_price is None:
                        parts.append(f"{label_txt}: {float(band_val):.2f}")
                    else:
                        parts.append(f"{label_txt}: {float(band_val):.2f} ({pct_vs_price:+.1f}% vs. Price)")

                if parts:
                    band_context_block = "<br>" + "<br>".join(parts) + "<br>"

            # MVA: Custom hover content (deltas)
            if (
                not _is_crossover_key(key)
                and (
                    key.startswith("SMA_")
                    or key.startswith("EMA_")
                    or key.startswith("VWMA_")
                    or key.startswith("HMA_")
                )
            ):
                current_price = price_by_date.get(d_raw)

                try:
                    current_price = float(current_price) if not _is_missing(current_price) else None
                except Exception:
                    current_price = None

                try:
                    ma_value = float(v) if not _is_missing(v) else None
                except Exception:
                    ma_value = None

                diff_abs = None
                diff_pct = None

                if current_price is not None and ma_value not in (None, 0):
                    try:
                        diff_abs = current_price - ma_value
                    except Exception:
                        diff_abs = None

                    try:
                        diff_pct = ((current_price / ma_value) - 1.0) * 100.0
                    except Exception:
                        diff_pct = None

                if diff_abs is not None:
                    pct_suffix = f" ({diff_pct:+.1f}%)" if diff_pct is not None else ""
                    ma_context_block = (
                        f"<br>Price vs. MA: {diff_abs:+.2f}{pct_suffix}<br>"
                    )

            # z must be numeric; use NaN for missing.
            # For crossover event rows, keep z score-driven but show spread
            # as the cell text because the event code is lower information-value
            # and remains available in hover as Event value.
            z_row.append(float(s) if s is not None else float("nan"))
            text_row.append(
                crossover_cell_text
                if _is_crossover_key(key) and crossover_cell_text
                else format_cell_value(key, v)
            )
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
                    "delta_line": delta_line,
                    "trend_line": trend_line,
                    "signal_line": signal_line,
                    "rule_block": rule_block,
                    "notes_block": notes_block,
                    "definition_block": definition_block,
                    "how_to_read_block": how_to_read_block,
                    "volume_block": volume_block,
                    "volume_vs_avg_block": volume_vs_avg_block,
                    "band_context_block": band_context_block,
                    "ma_context_block": ma_context_block,
                    "crossover_context_block": crossover_context_block,
                    "crossover_summary_block": crossover_summary_block,
                    "crossover_spread": crossover_spread,
					"macd_context_block": macd_context_block,
                    "adx_context_block": adx_context_block,
                    "stoch_context_block": stoch_context_block, 
                    "dpo_context_block": dpo_context_block,
                    "bullbear_context_block": bullbear_context_block,
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
        "%{customdata.ma_context_block}"
        "%{customdata.crossover_summary_block}"
        "%{customdata.crossover_context_block}"
        "%{customdata.delta_line}"
        "%{customdata.trend_line}"
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

    # Display all row labels on ''rolling signals heatmap'
    row_count = max(len(hm.y), 1)
    dynamic_height = max(450, 28 * row_count + 140)

    fig.update_layout(
        title=title,
        margin=dict(l=150, r=20, t=80, b=20),   # larger left margin for row labels
        height=dynamic_height,
        hoverlabel=dict(align="left"),
    )

    fig.update_xaxes(side="top", type="category")    # Move date to top of heatmap
    fig.update_yaxes(
        autorange="reversed",
        automargin=True,
        tickfont=dict(size=11),
    )

    return fig