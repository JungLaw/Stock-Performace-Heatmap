## Summary: MACD(12,26,9) Signals
Status: A

| Signal        | Literal trigger                                                                                | Layman’s translation                                                                                                   | Rule logic                                                                                                                             |
| ------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `strong_buy`  | `MACD_12_26_9_line < 0`, `MACD_12_26_9_hist > 0`, and `rising_2bar(MACD_12_26_9_hist, 2)`      | The broader MACD trend is still bearish, but bullish momentum has emerged and is strengthening consistently.           | The MACD line remains below zero, the histogram is positive, and the histogram has risen across the recent 2-bar check.                |
| `buy`         | `MACD_12_26_9_line < 0`, `MACD_12_26_9_hist > 0`, and `not_rising_2bar(MACD_12_26_9_hist, 2)`  | The broader MACD trend is still bearish, but shorter-term momentum has turned bullish without sustained strengthening. | The MACD line remains below zero and the histogram is positive, but the histogram does not satisfy the strict 2-bar rising condition.  |
| `neutral`     | MACD line and histogram are both nonnegative, or both nonpositive                              | The broader MACD trend and shorter-term momentum are aligned, so no contrarian reversal state is active.               | The MACD line and histogram have the same directional sign, including the zero-boundary cases.                                         |
| `sell`        | `MACD_12_26_9_line > 0`, `MACD_12_26_9_hist < 0`, and `not_falling_2bar(MACD_12_26_9_hist, 2)` | The broader MACD trend is still bullish, but shorter-term momentum has turned bearish without sustained weakening.     | The MACD line remains above zero and the histogram is negative, but the histogram does not satisfy the strict 2-bar falling condition. |
| `strong_sell` | `MACD_12_26_9_line > 0`, `MACD_12_26_9_hist < 0`, and `falling_2bar(MACD_12_26_9_hist, 2)`     | The broader MACD trend is still bullish, but bearish momentum has emerged and is weakening consistently.               | The MACD line remains above zero, the histogram is negative, and the histogram has fallen across the recent 2-bar check.               |

## Indicator overview

**MACD** stands for **Moving Average Convergence Divergence**. It is a trend-momentum indicator built from two exponential moving averages:

* **MACD line:** the 12-period EMA minus the 26-period EMA
* **Signal line:** the 9-period EMA of the MACD line
* **Histogram:** the MACD line minus the signal line

The histogram therefore shows the relationship between the MACD line and its signal line:

* A **positive histogram** means the MACD line is above the signal line.
* A **negative histogram** means the MACD line is below the signal line.
* A rising positive histogram indicates increasing bullish momentum.
* A falling negative histogram indicates increasing bearish momentum.

The zero line provides broader trend context:

* A MACD line **above zero** means the faster 12-period EMA is above the slower 26-period EMA.
* A MACD line **below zero** means the faster 12-period EMA is below the slower 26-period EMA.

The project’s MACD(12,26,9) rules use these two relationships together:

1. whether the MACD line is above or below zero; and
2. whether the histogram is positive or negative.

The rules are designed to identify **early reversal states**, rather than simply classify all positive MACD readings as bullish and all negative readings as bearish.

## Value-added use

MACD(12,26,9) adds value by showing whether momentum is beginning to move against the existing broader trend.

For example:

* A MACD line below zero indicates that the faster EMA remains below the slower EMA, which reflects an established bearish condition.
* If the histogram turns positive while the MACD line is still below zero, short-term momentum has turned upward before the broader MACD trend has fully recovered.
* This can identify an early bullish reversal or recovery attempt.

The inverse applies when the MACD line is above zero but the histogram becomes negative:

* the broader MACD trend remains positive;
* short-term momentum has turned downward;
* this may indicate an early bearish reversal or weakening phase.

The strong classifications add another confirmation layer by requiring the histogram to expand in the reversal direction for two consecutive comparisons.

This makes the rules more selective than a simple MACD-line/signal-line crossover test.

## Use with

MACD is generally most useful when combined with indicators that provide information it does not independently supply.

### Price trend or moving averages

Use SMA, EMA, HMA, or VWMA to confirm whether the price trend supports or contradicts the MACD reversal state.

Examples:

* A MACD buy state accompanied by price reclaiming a moving average provides stronger bullish confirmation.
* A MACD sell state accompanied by price falling below an important moving average provides stronger bearish confirmation.

### ADX and directional movement

ADX can help determine whether the market is trending strongly enough for a momentum signal to carry greater weight.

The +DI and −DI lines can also confirm directional pressure:

* +DI above −DI supports a bullish interpretation.
* −DI above +DI supports a bearish interpretation.

### RSI or another momentum oscillator

RSI can help determine whether the MACD reversal signal is supported by broader momentum.

Examples:

* MACD bullish reversal plus a rising RSI may strengthen the bullish interpretation.
* MACD bearish reversal plus a falling RSI may strengthen the bearish interpretation.

### Volume indicators

MFI, CMF, OBV, or raw volume can help determine whether participation supports the reversal.

A MACD reversal state without supporting volume may be less reliable than one accompanied by clear accumulation or distribution.

## MACD(12,26,9) Rule Translation

### Strong buy

```json
"strong_buy": "MACD_12_26_9_line < 0 and MACD_12_26_9_hist > 0 and rising_2bar(MACD_12_26_9_hist, 2)"
```

#### Literal component breakdown

`MACD_12_26_9_line < 0`

* The MACD line is below zero.
* This means the 12-period EMA remains below the 26-period EMA.
* **Layman’s translation**: "*The broader MACD trend is still bearish.*"

`MACD_12_26_9_hist > 0`

* The histogram is positive.
* Because the histogram equals the MACD line minus the signal line, this means the MACD line is above its signal line.
* **Layman’s translation**: "*Shorter-term momentum has turned bullish.*"

`rising_2bar(MACD_12_26_9_hist, 2)`

* The histogram is rising across the recent 2-bar check.
* The current histogram value is above the prior value, and the prior value is above the value before it.
* **Layman’s translation**: "*Bullish momentum has also been strengthening recently.*"

#### Literal summary

The MACD line is below zero, the histogram is positive, and the histogram is rising across the recent 2-bar check.

#### Plain-English version

The broader MACD trend remains bearish, but shorter-term momentum has turned bullish and has been strengthening consistently.

#### Interpretation

This is a **strong bullish reversal-state** signal.

It requires three layers of bullish reversal confirmation:

1. the broader MACD trend remains below zero;
2. the histogram has turned positive;
3. the histogram has also been rising recently.

### Buy

```json
"buy": "MACD_12_26_9_line < 0 and MACD_12_26_9_hist > 0 and not_rising_2bar(MACD_12_26_9_hist, 2)"
```

#### Literal component breakdown

`MACD_12_26_9_line < 0`

* The MACD line is below zero.
* The 12-period EMA remains below the 26-period EMA.
* **Layman’s translation**: "*The broader MACD trend is still bearish.*"

`MACD_12_26_9_hist > 0`

* The histogram is positive.
* The MACD line is above its signal line.
* **Layman’s translation**: "*Shorter-term momentum has turned bullish.*"

`not_rising_2bar(MACD_12_26_9_hist, 2)`

* The histogram does not satisfy the strict recent 2-bar rising condition.
* Bullish momentum is present, but it has not strengthened consistently across the full recent sequence.
* **Layman’s translation**: "*Bullish momentum has appeared, but it is not strengthening consistently enough to qualify as strong.*"

#### Literal summary

The MACD line is below zero, the histogram is positive, and the histogram is not rising across the full recent 2-bar check.

#### Plain-English version

The broader MACD trend remains bearish, but shorter-term momentum has turned bullish without enough consistent strengthening to qualify as a strong buy.

#### Interpretation

This is an **early bullish reversal-state** signal.

It requires:

1. the broader MACD trend to remain below zero;
2. the histogram to be positive;
3. no strict requirement that bullish momentum be strengthening consistently.

### Neutral

```json
"neutral": "(MACD_12_26_9_line >= 0 and MACD_12_26_9_hist >= 0) or (MACD_12_26_9_line <= 0 and MACD_12_26_9_hist <= 0)"
```

#### Literal component breakdown

`MACD_12_26_9_line >= 0 and MACD_12_26_9_hist >= 0`

* The MACD line is at or above zero.
* The histogram is also at or above zero.
* The broader trend and shorter-term momentum are aligned in the bullish direction.
* **Layman’s translation**: "*The broader trend and current momentum are both bullish, so no new contrarian reversal is occurring.*"

`MACD_12_26_9_line <= 0 and MACD_12_26_9_hist <= 0`

* The MACD line is at or below zero.
* The histogram is also at or below zero.
* The broader trend and shorter-term momentum are aligned in the bearish direction.
* **Layman’s translation**: "*The broader trend and current momentum are both bearish, so no new contrarian reversal is occurring.*"

#### Literal summary

The MACD line and histogram have the same directional sign, including the zero-boundary cases.

#### Plain-English version

The broader MACD trend and shorter-term momentum are aligned, so the project does not treat the condition as an active bullish or bearish reversal state.

#### Interpretation

This is a **no-contrarian-reversal-state** classification.

It does not necessarily mean:

* momentum is weak;
* price is moving sideways;
* the market lacks a trend.

It means only that the MACD line and histogram are not pointing in opposite directional states.

### Sell

```json
"sell": "MACD_12_26_9_line > 0 and MACD_12_26_9_hist < 0 and not_falling_2bar(MACD_12_26_9_hist, 2)"
```

#### Literal component breakdown

`MACD_12_26_9_line > 0`

* The MACD line is above zero.
* This means the 12-period EMA remains above the 26-period EMA.
* **Layman’s translation**: "*The broader MACD trend is still bullish.*"

`MACD_12_26_9_hist < 0`

* The histogram is negative.
* The MACD line is below its signal line.
* **Layman’s translation**: "*Shorter-term momentum has turned bearish.*"

`not_falling_2bar(MACD_12_26_9_hist, 2)`

* The histogram does not satisfy the strict recent 2-bar falling condition.
* Bearish momentum is present, but it has not weakened consistently across the full recent sequence.
* **Layman’s translation**: "*Bearish momentum has appeared, but it is not strengthening consistently enough to qualify as strong.*"

#### Literal summary

The MACD line is above zero, the histogram is negative, and the histogram is not falling across the full recent 2-bar check.

#### Plain-English version

The broader MACD trend remains bullish, but shorter-term momentum has turned bearish without enough consistent weakening to qualify as a strong sell.

#### Interpretation

This is an **early bearish reversal-state** signal.

It requires:

1. the broader MACD trend to remain above zero;
2. the histogram to be negative;
3. no strict requirement that bearish momentum be strengthening consistently.

### Strong sell

```json
"strong_sell": "MACD_12_26_9_line > 0 and MACD_12_26_9_hist < 0 and falling_2bar(MACD_12_26_9_hist, 2)"
```

#### Literal component breakdown

`MACD_12_26_9_line > 0`

* The MACD line is above zero.
* This means the 12-period EMA remains above the 26-period EMA.
* **Layman’s translation**: "*The broader MACD trend is still bullish.*"

`MACD_12_26_9_hist < 0`

* The histogram is negative.
* The MACD line is below its signal line.
* **Layman’s translation**: "*Shorter-term momentum has turned bearish.*"

`falling_2bar(MACD_12_26_9_hist, 2)`

* The histogram is falling across the recent 2-bar check.
* The current histogram value is below the prior value, and the prior value is below the value before it.
* **Layman’s translation**: "*Bearish momentum has also been strengthening recently.*"

#### Literal summary

The MACD line is above zero, the histogram is negative, and the histogram is falling across the recent 2-bar check.

#### Plain-English version

The broader MACD trend remains bullish, but shorter-term momentum has turned bearish and has been weakening consistently.

#### Interpretation

This is a **strong bearish reversal-state** signal.

It requires three layers of bearish reversal confirmation:

1. the broader MACD trend remains above zero;
2. the histogram has turned negative;
3. the histogram has also been falling recently.

## Rule summary table

| Signal          | Exact rule conditions                                                                                               | Plain-English translation                                                                                          | Practical interpretation                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| **Strong Buy**  | MACD line is below zero; histogram is positive; histogram has risen strictly across the required two-bar sequence.  | The broader MACD trend is still bearish, but bullish momentum has emerged and is expanding consistently.           | Confirmed bullish reversal state developing below the zero line.                                               |
| **Buy**         | MACD line is below zero; histogram is positive; histogram does not satisfy the strict two-bar rising condition.     | The broader MACD trend is still bearish, but shorter-term momentum has turned bullish without sustained expansion. | Early bullish reversal state, but with less momentum confirmation than strong buy.                             |
| **Neutral**     | MACD line and histogram are both nonnegative, or both nonpositive.                                                  | The broader MACD trend and shorter-term momentum have the same directional sign.                                   | No contrarian zero-line reversal state is active. Neutral does not necessarily mean weak or sideways momentum. |
| **Sell**        | MACD line is above zero; histogram is negative; histogram does not satisfy the strict two-bar falling condition.    | The broader MACD trend is still bullish, but shorter-term momentum has turned bearish without sustained expansion. | Early bearish reversal state, but with less momentum confirmation than strong sell.                            |
| **Strong Sell** | MACD line is above zero; histogram is negative; histogram has fallen strictly across the required two-bar sequence. | The broader MACD trend is still bullish, but bearish momentum has emerged and is expanding consistently.           | Confirmed bearish reversal state developing above the zero line.                                               |

## Industry-standard Baseline

| Signal        | Basic industry-style rule                                                                                          | Basic translation                                           |
| ------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| `strong_buy`  | MACD is below zero, but the MACD line has crossed clearly above the signal line and bullish momentum is expanding. | Strong early bullish reversal from a bearish trend context. |
| `buy`         | MACD line crosses above the signal line.                                                                           | Bullish momentum shift or possible early buy signal.        |
| `neutral`     | MACD and signal line are close, flat, or moving without a decisive crossover.                                      | Momentum is mixed or lacks a clear directional trigger.     |
| `sell`        | MACD line crosses below the signal line.                                                                           | Bearish momentum shift or possible early sell signal.       |
| `strong_sell` | MACD is above zero, but the MACD line has crossed clearly below the signal line and bearish momentum is expanding. | Strong early bearish reversal from a bullish trend context. |

The table above is a simplified industry-style baseline. MACD does not have one universal five-state industry standard, so the strong and neutral labels are practical approximations rather than universally fixed definitions.

## How to Read

For an output such as:

```text
MACD(12,26,9) = -1.83, -2.05, 0.22
```

the values normally correspond to:

1. MACD line;
2. signal line;
3. histogram.

### Component breakdown

**MACD line: `-1.83`**

* The MACD line is calculated as:

```text
EMA(12) − EMA(26)
```

* A value of `-1.83` means the faster 12-period EMA is below the slower 26-period EMA.
* This generally indicates a bearish or downward broader momentum context.

**Signal line: `-2.05`**

* The signal line is usually a 9-period EMA of the MACD line.
* It is a smoothed version of the MACD line and is commonly used as the crossover reference.
* Because `-1.83` is greater than `-2.05`, the MACD line is above the signal line.

**Histogram: `0.22`**

* The histogram is calculated as:

```text
MACD line − Signal line
```

* In this example:

```text
-1.83 − (-2.05) = 0.22
```

* The positive histogram confirms that the MACD line is above the signal line.
* This indicates that shorter-term momentum has turned upward relative to its signal line.

### Market interpretation

The relationship between these values suggests a **bullish momentum shift within a still-bearish broader MACD context**.

* The MACD line remains below zero, so the faster EMA remains below the slower EMA.
* The histogram is positive, so the MACD line is above the signal line.
* This combination can indicate that bearish momentum is weakening and an early bullish reversal or relief rally may be developing.

Under the project’s rule system:

* if the positive histogram is not rising across the strict recent 2-bar check, the condition is classified as `buy`;
* if the positive histogram is rising across that check, the condition is classified as `strong_buy`.

### Interpreting the signs

| MACD line  | Histogram | Basic implication                                                            |
| ---------- | --------- | ---------------------------------------------------------------------------- |
| Above zero | Positive  | Broader bullish trend and bullish shorter-term momentum are aligned.         |
| Above zero | Negative  | Broader trend remains bullish, but shorter-term momentum has turned bearish. |
| Below zero | Negative  | Broader bearish trend and bearish shorter-term momentum are aligned.         |
| Below zero | Positive  | Broader trend remains bearish, but shorter-term momentum has turned bullish. |

The project specifically emphasizes the two mixed-sign cases:

* MACD line below zero with a positive histogram;
* MACD line above zero with a negative histogram.

These represent potential reversal states because shorter-term momentum has moved against the existing broader MACD trend.

### Histogram direction

The histogram’s sign shows the relationship between the MACD line and the signal line, while its movement shows whether that relationship is strengthening or weakening.

* A positive and rising histogram means bullish momentum is expanding.
* A positive but falling histogram means bullish momentum remains positive but is weakening.

* A negative and falling histogram means bearish momentum is expanding.
* A negative but rising histogram means bearish momentum remains negative but is weakening.

A histogram moving toward zero often means the current momentum advantage is fading.
A histogram moving farther away from zero generally means the momentum gap between the MACD line and signal line is expanding.

**Alternative Interpretation**:
> - A growing positive histogram indicates that MACD is moving farther above its signal line.
> - A growing negative histogram indicates that MACD is moving farther below its signal line.
> - Conversely, shrinking bars indicate convergence and possible momentum deceleration.


---
## Initial audit note
(a/o 7/17/26)

The current MACD(12,26,9) rules are a **custom, project-calibrated five-state interpretation**. They should not be described as a universal or standard industry MACD classification model.

The underlying components are industry-standard:
* MACD line;
* signal line;
* histogram;
* zero-line context;
* histogram expansion and contraction.

The specific classification design is custom:
* aligned MACD-line and histogram signs are assigned to neutral;
* bullish scores are reserved for positive histogram momentum while the MACD line remains below zero;
* bearish scores are reserved for negative histogram momentum while the MACD line remains above zero;
* strong classifications require a strict two-bar directional histogram sequence.

This design intentionally emphasizes **contrarian reversal-state detection**, rather than ordinary trend-following classification.

The rules were validated against the production expression and signal-classification path. For the tested AAPL sample of 765 fully initialized observations, the resulting distribution was:

| Signal      | Historical count |
| ----------- | ---------------: |
| Strong Buy  |               68 |
| Buy         |               46 |
| Neutral     |              470 |
| Sell        |               80 |
| Strong Sell |              101 |
| **Total**   |          **765** |

The five rules were confirmed to be:

* executable through the production expression engine;
* mutually exclusive;
* collectively exhaustive for initialized observations;
* free of the previous nonexistent unsuffixed MACD alias;
* independent of ATR and ATRP;
* consistent across the Rolling Signals Heatmap, SCD Multiple Indicators, and SCD Single Indicator views.

The structure now matches the requested indicator-overview pattern while preserving the original substantive content.

---
## MACD (old notes)

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