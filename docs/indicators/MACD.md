# MACD
Status: Incomplete

**Purpose:** Reveal changes in trend strength, direction, momentum, and duration by showing the relationship between two exponential moving averages.

**Use when:** You want to confirm trend changes, spot momentum shifts, or identify potential entry/exit points in trending markets.

**Key Concept:** Combines trend-following and momentum characteristics by measuring the difference between fast and slow EMAs, then smoothing that difference with a signal line.

**Calculation:**
- **MACD Line:** 12-period EMA minus 26-period EMA
- **Signal Line:** 9-period EMA of MACD Line
- **Histogram:** MACD Line minus Signal Line

**Signals & Interpretation:**
- MACD above zero = bullish momentum
- MACD below zero = bearish momentum
- MACD crosses above signal line = bullish signal
- MACD crosses below signal line = bearish signal
- Histogram shows momentum acceleration/deceleration
- Divergences between MACD and price signal potential reversals

**Optimal Conditions:** Most effective in trending markets on daily and weekly timeframes. Works well for swing trading and position trading.

**Limitations:** Can produce false signals in sideways markets. As a lagging indicator, may miss early trend changes in fast-moving markets.

**Complexity Level:** Intermediate

---

The single most valuable metric to track daily for the standard **MACD(12,26,9)** indicator is the **MACD Histogram** value, as it provides an early warning of momentum shifts and potential trend changes. 

#### Why the MACD Histogram?

Technical analysts and equity traders focus on the histogram because: 

- **Momentum Changes:** The histogram visually represents the distance between the MACD line and the signal line. As the difference widens, momentum accelerates; as it shrinks, momentum decelerates, signaling that a trend may be weakening.
- **Early Signals:** The histogram reacts faster to changes in price direction than the MACD line or signal line alone, offering earlier indications of potential reversals or crossovers.
- **Divergence Analysis:** A primary strategy involves looking for divergence between the price action (e.g., price makes a new high) and the histogram (e.g., histogram makes a lower high). This divergence is a strong signal that the current trend's momentum is exhausting itself and a reversal is likely. 

While tracking the absolute values of the MACD line and the signal line is necessary for context, the **rate of change and direction of the histogram** provides the most actionable and forward-looking information according to industry standard

---
#### The Hierarchy of MACD Information-Value

Instead of one metric, traders monitor three distinct **signal states** derived from your outputs:

- **State 1: The Histogram Trend (Momentum)**
    - **Metric:** Direction of change in the Histogram (e.g., is 0.22 higher or lower than yesterday?).
    - **Value:** This is considered a **leading indicator**. Even if the MACD is negative (bearish trend), a rising histogram tells traders that the selling pressure is "exhausting" and a reversal is likely before it actually happens.
- **State 2: Signal Line Crossovers (Trade Triggers)**
    - **Metric:** Whether the MACD Line is above or below the Signal Line.
    - **Value:** This provides the actual **buy/sell signal**. Since your MACD (-1.83) is above your Signal (-2.05), you have a "Bullish Crossover." Analysts use this to time the exact day to enter or exit a position.
- **State 3: The Zero-Line Position (Trend Context)**
    - **Metric:** Is the MACD Line positive or negative?
    - **Value:** This is the **lagging confirmation** of the broad trend. A MACD below zero (like your -1.83) means the long-term trend is still bearish. Professional traders often won't take a "buy" signal from a histogram reversal unless the MACD line eventually crosses above zero to confirm a new uptrend. 


Pro-Tip: The "Percentage Price Oscillator (PPO)"
- If you are looking for a single standardized metric used by Wall Street to compare different stocks, many institutional analysts prefer the **Percentage Price Oscillator (PPO)** over the standard MACD. 

- **The Problem:** MACD is based on absolute dollar values. A MACD of -1.83 for a $20 stock is massive, but for a $500 stock, it’s negligible.
- **The Standard:** The PPO converts the MACD into a percentage. This allows you to track and compare the "momentum strength" across your entire portfolio using one standardized scale. 
