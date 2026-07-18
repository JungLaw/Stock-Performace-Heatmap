The **Hull Moving Average** was Alan Hull's solution to a fundamental problem with all traditional MAs: *the longer the period, the smoother, but the more lag.* Hull attacked that tradeoff mathematically using **weighted moving averages (WMAs) and square root periods** to dramatically cut lag while preserving smoothness.

The formula essentially is:
> **HMA(n) = WMA(2 × WMA(n/2) − WMA(n)), smoothed over √n periods**


---
The HMA is a fast, smooth moving average designed to reduce lag while maintaining responsiveness. Experienced traders adjust the lookback period to align with their trading timeframe.


**Settings**:
- **Short-term (1-15 days):** HMA(9)
  - This is the most common setting for short-term trading, as it reacts quickly to price changes. It’s widely used for day trading or short-term swing trading.
- **Intermediate-term (15-50 days):** HMA(21)
  - A 21-period HMA balances responsiveness and stability, making it suitable for swing traders or those tracking trends over a few weeks. It smooths out noise while capturing mid-term price movements.
- **Long-term (50+ days):** HMA(50)
  - A 50-period HMA is used for long-term trend analysis, often in position trading or to identify major market trends. It’s less sensitive to short-term fluctuations, focusing on broader price direction.

---

**Why HMA(55) specifically:**

| Reason | Detail |
|---|---|
| **Fibonacci** | 55 is a core Fibonacci number — markets respect these periods because enough participants use them to become self-reinforcing |
| **Lag reduction math** | Because HMA's lag is dramatically less than a standard EMA or SMA, a 55-period HMA behaves more like a 30-35 period EMA in terms of responsiveness — you get intermediate-term smoothing with near-term reaction speed |
| **Avoids crowding** | Everyone watches EMA(50). HMA(55) gives you a slightly differentiated read on the same timeframe — less susceptible to stop-hunting around the round number |
| **√55 ≈ 7.4** | The smoothing period is ~7, which maps neatly to one trading week — there's an elegant internal structure to it |

In practice, HMA(55) on a daily chart behaves like a *living* trend line — it turns faster than a 50 SMA but without the whipsaw of a short EMA. It's particularly effective as a dynamic support/resistance level in trending markets.

---

# HMA(55) — Rule translation

## Brief overview
**HMA** stands for **Hull Moving Average**. It is a moving average designed to reduce lag while staying smoother than many faster moving averages.

For `HMA(55)`:

```text
HMA_55 = Hull Moving Average over 55 periods
HMA_55_slope = 14-period linear-regression slope of HMA(55)
```

Simple interpretation:

* If price is above HMA(55), price is above that longer-term Hull trend baseline.
* If price is below HMA(55), price is below that longer-term Hull trend baseline.
* If `HMA_55_slope` is positive, HMA(55)’s own trend line is rising.
* If `HMA_55_slope` is negative, HMA(55)’s own trend line is falling.
* Because HMA is designed to reduce lag, it can turn faster than a traditional long moving average.

Value-added use:

> Use HMA(55) when you want a smoother long-term trend reference that can still respond faster than a traditional long moving average, especially for dynamic support/resistance in trending markets.

---

# HMA(55) rule translation

## Strong buy

```json
"strong_buy": "Close > HMA_55 and HMA_55_slope > 0.001 and rising_2bar(HMA_55)"
```

Literal component breakdown:

* `Close > HMA_55`

  * The closing price is above HMA(55).

* `HMA_55_slope > 0.001`

  * HMA(55)’s own slope is greater than `0.001`.
  * In plain terms: HMA(55)’s trend line is meaningfully rising, based on the project’s slope scale.

* `rising_2bar(HMA_55)`

  * HMA(55) is rising across the recent 2-trading-day check.

Literal summary:

> Price is above HMA(55), HMA(55)’s own slope is meaningfully positive, and HMA(55) is rising across the recent 2-trading-day check.

Plain-English version:

> Price is above a rising long-term Hull trend line, and that trend line is improving enough to qualify as strong bullish trend confirmation.

Notes / confidence:

* High confidence on literal meaning.
* This is now HMA(55)-specific because it uses `HMA_55_slope`, not the generic `HMA_slope` alias.
* The slope threshold `0.001` is project-specific calibration.

---

## Buy

```json
"buy": "Close > HMA_55 and HMA_55_slope > 0"
```

Literal component breakdown:

* `Close > HMA_55`

  * The closing price is above HMA(55).

* `HMA_55_slope > 0`

  * HMA(55)’s own slope is positive.

Literal summary:

> Price is above HMA(55), and HMA(55)’s own slope is positive.

Plain-English version:

> Price is above the long-term Hull trend baseline, and that baseline is rising.

Notes / confidence:

* High confidence.
* This is the basic bullish HMA(55) trend-following condition.

---

## Neutral

```json
"neutral": "abs(Close/HMA_55 - 1) * 100 <= 1.0 * ATRP_50"
```

Literal component breakdown:

* `Close/HMA_55 - 1`

  * Measures how far the closing price is from HMA(55) as a ratio.

* `abs(Close/HMA_55 - 1)`

  * Ignores whether price is above or below HMA(55); only measures the size of the distance.

* `abs(Close/HMA_55 - 1) * 100`

  * Converts that distance into percentage units.
  * Example: if price is 2% above HMA(55), this value is `2.0`.

* `1.0 * ATRP_50`

  * Uses one full ATRP(50) value as the neutral-zone width.
  * ATRP(50) is the stock’s recent normal movement expressed as a percent of price.

* `abs(Close/HMA_55 - 1) * 100 <= 1.0 * ATRP_50`

  * Price is close enough to HMA(55), measured in percent terms, to be treated as neutral.

Literal summary:

> Price is within one ATRP(50)-sized percentage band of HMA(55).

Plain-English version:

> Price is close enough to the HMA(55) trend line that the rule treats the signal as too near the baseline to classify as clearly bullish or bearish.

Notes / confidence:

* High confidence on the corrected unit logic.
* This fixes the prior unit issue by comparing percent distance to ATRP in percent units.
* `ATRP_50` is used as the volatility reference for the HMA(55) neutral band.

---

## Sell

```json
"sell": "Close < HMA_55 and HMA_55_slope < 0"
```

Literal component breakdown:

* `Close < HMA_55`

  * The closing price is below HMA(55).

* `HMA_55_slope < 0`

  * HMA(55)’s own slope is negative.

Literal summary:

> Price is below HMA(55), and HMA(55)’s own slope is negative.

Plain-English version:

> Price is below the long-term Hull trend baseline, and that baseline is falling.

Notes / confidence:

* High confidence.
* This is the basic bearish HMA(55) trend-following condition.

---

## Strong sell

```json
"strong_sell": "Close < HMA_55 and HMA_55_slope < -0.001 and falling_2bar(HMA_55)"
```

Literal component breakdown:

* `Close < HMA_55`

  * The closing price is below HMA(55).

* `HMA_55_slope < -0.001`

  * HMA(55)’s own slope is less than `-0.001`.
  * In plain terms: HMA(55)’s trend line is meaningfully falling, based on the project’s slope scale.

* `falling_2bar(HMA_55)`

  * HMA(55) is falling across the recent 2-trading-day check.

Literal summary:

> Price is below HMA(55), HMA(55)’s own slope is meaningfully negative, and HMA(55) is falling across the recent 2-trading-day check.

Plain-English version:

> Price is below a falling long-term Hull trend line, and that trend line is weakening enough to qualify as strong bearish trend confirmation.

Notes / confidence:

* High confidence.
* `HMA_55_slope < -0.001` and `falling_2bar(HMA_55)` are related but not identical:

  * `HMA_55_slope < -0.001` checks the broader 14-period fitted slope.
  * `falling_2bar(HMA_55)` checks recent 2-trading-day direction.
* Together they require both broader downside slope and recent downside confirmation.

---

# HMA(55) summary

| Signal        | Literal trigger                                                | Plain-English meaning                                       |
| ------------- | -------------------------------------------------------------- | ----------------------------------------------------------- |
| `strong_buy`  | `Close > HMA_55`, `HMA_55_slope > 0.001`, and HMA(55) rising   | Price is above a meaningfully rising HMA(55) trend line.    |
| `buy`         | `Close > HMA_55` and `HMA_55_slope > 0`                        | Price is above a rising HMA(55) trend baseline.             |
| `neutral`     | Percent distance from HMA(55) is within `1.0 × ATRP_50`        | Price is close enough to HMA(55) that direction is unclear. |
| `sell`        | `Close < HMA_55` and `HMA_55_slope < 0`                        | Price is below a falling HMA(55) trend baseline.            |
| `strong_sell` | `Close < HMA_55`, `HMA_55_slope < -0.001`, and HMA(55) falling | Price is below a meaningfully falling HMA(55) trend line.   |

# Updated audit note

HMA(55) is a **momentum / trend-following confirmation** rule:

```text
price above rising HMA → bullish
price below falling HMA → bearish
price close to HMA → neutral
```

The prior version had two audit issues:

1. It used generic `HMA_slope`, which was anchored to HMA(21), not HMA(55).
2. Its neutral rule compared fractional distance to ATRP percent units.

The updated version resolves both issues:

1. HMA(55) now uses `HMA_55_slope`, so the slope condition is parameter-specific.
2. The neutral expression now multiplies the price/HMA distance by `100`, so both sides are in percent units.

Validation status:

* JSON syntax passed.
* Python compile checks passed.
* Rulebook load smoke test passed.
* App/manual dashboard checks passed, including hover text showing the new signal definitions.

Overall assessment:

> HMA(55) is now mechanically valid, semantically cleaner, and easier to explain.
