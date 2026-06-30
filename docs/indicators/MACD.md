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
    - When the histogram is below zero, it means the MACD line is trading below the signal line. 
    - This condition typically implies that bearish momentum is currently in control of the asset

- MACD crosses above signal line = bullish signal
- MACD crosses below signal line = bearish signal
- Histogram shows momentum acceleration/deceleration
- Divergences between MACD and price signal potential reversals

**Terms**:

Here’s the precise meaning of each component of MACD(12,26,9):

- **MACD Line** — the core indicator  
    - $\text{MACD line} = \text{EMA}_{12} - \text{EMA}_{26}$

- **Signal Line** — a smoothed version of the MACD line  
  It’s a 9‑period EMA of the MACD line.

- **MACD Histogram** — the *difference* between the two  
    - $\text{Histogram} = \text{MACD line} - \text{Signal line}$

So when someone says "MACD", they mean the **MACD line** unless they explicitly say "signal line" or "histogram".



| Component | What It Measures | What It Tells You |
| --- | --- | --- |
| **MACD Line** | Trend momentum (fast EMA vs slow EMA) | Direction + strength of the trend |
| **Signal Line** | Smoothed MACD | Helps generate crossover signals |
| **MACD Histogram** | Difference between MACD & signal line | Acceleration/deceleration of momentum |

| Term | What it refers to | What people mean when they say it |
| --- | --- | --- |
| **MACD** | The MACD line (12 EMA − 26 EMA) | **Default meaning** |
| **Signal Line** | 9‑EMA of MACD line | Only used when explicitly named |
| **MACD Histogram** | MACD line − Signal line | Only used when explicitly named |

The MACD line and the MACD histogram measure related but different aspects of momentum. The cleanest way to think about it is:

- The MACD line measures "trend momentum".
    - the overall momentum direction and strength
- The MACD histogram measures the "change in that momentum".
    - shows momentum acceleration or deceleration

**What the MACD Line Represents**
- It’s the difference between the fast and slow EMAs (12‑period minus 26‑period).

- When the fast EMA pulls away from the slow EMA, the MACD line moves farther from zero → momentum strengthening.

- When they converge, the MACD line moves toward zero → momentum weakening.

**What the MACD Histogram Represents**
- It’s the visual distance between the MACD line and the signal line (the 9‑EMA of the MACD).
- Bars grow when momentum is accelerating.
- Bars shrink when momentum is decelerating.
-   Shrinking bars often warn that a MACD–signal line crossover is approaching.

---
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


#### What it means when the histogram is falling
A falling MACD histogram means:

- Momentum is fading in the current trend direction.
(Bars shrink toward zero — convergence.) 

- If bars are above zero and falling → bullish momentum is weakening.
- If bars are below zero and falling → bearish momentum is weakening.

- A falling histogram often precedes a MACD–signal line crossover, because shrinking bars indicate the two lines are converging