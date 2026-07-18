# Summary table: SMA(200)
Status: A

| Signal        | Layman’s translation                                                                | Literal trigger                                                          | Rule logic                                                                                                                  |
| ------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| `strong_buy`  | Price is above a 200-day average that is clearly and recently rising.               | `Close > SMA_200`, `SMA_200_slope > 0.001`, and `rising_2bar(SMA_200)`   | Price is above SMA(200), the 200-day slope is meaningfully positive, and SMA(200) is rising across the recent 2-bar check.  |
| `buy`         | Price is above the 200-day average, and the 200-day average is rising.              | `Close > SMA_200` and `SMA_200_slope > 0`                                | Price is above SMA(200), and SMA(200)’s slope is positive.                                                                  |
| `neutral`     | Price is close enough to the 200-day average that the rule treats the gap as noise. | Percent distance from SMA(200) is within `0.25 × ATRP_200`               | Price is within one-quarter of an ATRP(200)-sized percentage distance from SMA(200).                                        |
| `sell`        | Price is below the 200-day average, and the 200-day average is falling.             | `Close < SMA_200` and `SMA_200_slope < 0`                                | Price is below SMA(200), and SMA(200)’s slope is negative.                                                                  |
| `strong_sell` | Price is below a 200-day average that is clearly and recently falling.              | `Close < SMA_200`, `SMA_200_slope < -0.001`, and `falling_2bar(SMA_200)` | Price is below SMA(200), the 200-day slope is meaningfully negative, and SMA(200) is falling across the recent 2-bar check. |


| Signal        | One-line meaning                                                         |
| ------------- | ------------------------------------------------------------------------ |
| `strong_buy`  | Price is above a clearly rising 200-day average.                         |
| `buy`         | Price is above a rising 200-day average.                                 |
| `neutral`     | Price is close enough to the 200-day average to treat the move as noise. |
| `sell`        | Price is below a falling 200-day average.                                |
| `strong_sell` | Price is below a clearly falling 200-day average.                        |

> Note: see below for 'basic' rules


---
# SMA(200) — brief overview

**SMA** stands for **Simple Moving Average**.

For `SMA(200)`:

```text
SMA_200 = the average closing price over the last 200 periods
```

In a daily-stock context, that usually means roughly the average close over the last **200 trading days**.

Simple interpretation:

* If price is above SMA(200), price is above its long-term average.
* If price is below SMA(200), price is below its long-term average.
* If SMA(200) is rising, the long-term average price is improving.
* If SMA(200) is falling, the long-term average price is weakening.
* Because SMA(200) changes slowly, it is best understood as a **long-term trend / regime filter**, not a short-term timing signal.

Value-added use:

> Use SMA(200) when you want a long-term trend reference that helps distinguish broadly bullish, neutral/transition, and bearish market posture.

Use with:

* **Volume / OBV / CMF** — to check whether a move above or below the 200-day average is supported by participation. IBD specifically treats breaks below the 200-day line as more serious when they occur on heavy volume. ([Investor's Business Daily][1])
* **ADX** — to check whether the trend has strength. ADX is widely used as a trend-strength indicator, and Investopedia notes that values above 25 are commonly treated as evidence of a strong trend while values below 20 suggest weak or rangebound conditions. ([Investopedia][2])
* **MACD or ROC** — to check whether long-term trend posture is supported by momentum. Moving averages are lagging by nature, so pairing them with momentum helps distinguish a slow regime read from actual thrust.
* **RSI** — to check whether the move is supported by momentum or becoming stretched/exhausted.
* **SMA 50/200 crossover row** — to check whether the medium-term average is crossing the long-term average. Your project already defines `SMA_50_X_SMA_200` as an event-only crossover row in the UI metadata.

# SMA(200) rule translation

## Strong buy

```json id="ijzknb"
"strong_buy": "Close > SMA_200 and (SMA_200_slope > 0.001) and rising_2bar(SMA_200)"
```

### Literal component breakdown

`Close > SMA_200`

* The current closing price is above the 200-day simple moving average.
* Layman’s translation: **price is trading above its long-term average.**

`SMA_200_slope > 0.001`

* The 200-day average has a positive slope greater than `0.001`.
* This does not merely mean price is above the average. It means the average line itself is rising by more than the project’s “meaningfully rising” threshold.
* Layman’s translation: **the 200-day average itself is rising meaningfully.**

`rising_2bar(SMA_200)`

* SMA(200) is rising across the recent 2-bar check.
* In daily data, this means the 200-day average has moved upward over the recent 2-trading-day comparison.
* Layman’s translation: **the 200-day average has also been rising recently.**

### Literal summary

Price is above SMA(200), SMA(200)’s slope is meaningfully positive, and SMA(200) is rising across the recent 2-bar check.

### Plain-English version

That means price must be above the 200-day average, the 200-day average must be rising meaningfully, and the 200-day average must also be rising recently.

### Interpretation

This is a **strong bullish long-term trend confirmation** signal.

It requires three layers of confirmation:

1. price is above the long-term average;
2. the long-term average is meaningfully rising;
3. the long-term average has also been rising recently.

### Notes / confidence

* High confidence on the literal interpretation.
* `0.001` is a project-calibrated slope threshold, not an industry-standard SMA threshold.
* Because SMA(200) moves slowly, strong signals should be expected to be less frequent and slower to change.

---

## Buy

```json
"buy": "Close > SMA_200 and (SMA_200_slope > 0)"
```

### Literal component breakdown

`Close > SMA_200`

* The current closing price is above the 200-day simple moving average.
* Layman’s translation: **price is above its long-term average.**

`SMA_200_slope > 0`

* The slope of the 200-day average is positive.
* This means the 200-day average is rising, even if it is not rising strongly enough to qualify as `strong_buy`.
* Layman’s translation: **the 200-day average must be rising.**

### Literal summary

Price is above SMA(200), and SMA(200)’s slope is positive.

### Plain-English version

That means price must be above the 200-day average **and** the 200-day average must be rising.

### Interpretation

This is a **bullish long-term trend confirmation** signal.

It is stricter than simply saying “price is above the 200-day average.” It also requires the 200-day average itself to be moving upward.

### Notes / confidence

* High confidence.
* This is the core bullish regime rule.
* It avoids labeling price as bullish if price is above a flat or falling 200-day average.

---

## Neutral

```json
"neutral": "abs(Close/SMA_200 - 1) * 100 <= (0.25 * ATRP_200)"
```

### Literal component breakdown

`Close/SMA_200`

* This compares the current closing price to the 200-day average.
* If the result is above `1`, price is above SMA(200).
* If the result is below `1`, price is below SMA(200).
* Layman’s translation: **compare price to the 200-day average.**

`Close/SMA_200 - 1`

* This turns the comparison into a distance from SMA(200).
* Example: `1.03 - 1 = 0.03`, meaning price is 3% above SMA(200).
* Example: `0.97 - 1 = -0.03`, meaning price is 3% below SMA(200).
* Layman’s translation: **measure how far price is from the 200-day average.**

`abs(Close/SMA_200 - 1)`

* `abs()` ignores whether price is above or below SMA(200).
* It only measures the size of the gap.
* Layman’s translation: **measure the gap from the 200-day average, regardless of direction.**

`abs(Close/SMA_200 - 1) * 100`

* This converts the gap into percentage units.
* Example: `0.03 * 100 = 3.0`, meaning 3%.
* Layman’s translation: **express the price/SMA gap as a normal percent.**

`ATRP_200`

* ATRP(200) estimates the stock’s typical price movement over the last 200 periods, expressed as a percent of price.
* Layman’s translation: **how much the stock normally moves, in percentage terms, over the long-term lookback (last 200 days).**

`0.25 * ATRP_200`
* This uses one-quarter of that typical movement as the neutral threshold.
* Layman’s translation: **one-quarter of the stock’s normal movement over the last 200 days.**

`abs(Close/SMA_200 - 1) * 100 <= (0.25 * ATRP_200)`

* Price is neutral if its percent distance from SMA(200) is no more than one-quarter of ATRP(200).
* Layman’s translation: **if price is only a small volatility-adjusted distance from the 200-day average, treat it as too close to call.**

### Literal summary

Price is within one-quarter of an ATRP(200)-sized percentage distance from SMA(200).

### Plain-English version

That means price is close enough to the 200-day average that the rule treats the difference as noise rather than a clear bullish or bearish signal.

### Interpretation

This is a **long-term transition / noise-band rule**.

It does not say the stock has no trend in every sense. It says that, for this SMA(200) signal, price is so close to the 200-day average that the rule should avoid calling the move clearly bullish or clearly bearish.

### Notes / confidence

* High confidence after the `0.25 × ATRP_200` correction.
* This now matches your intended “percentage-based ATR buffer” concept: price near the moving average is neutral if the distance is small relative to typical movement.
* The industry-consistent analogy is a moving-average envelope or channel: the moving average is the baseline, and a buffer around it helps avoid false signals from minor crosses. Moving-average envelopes are commonly defined as bands above and below a moving average, and related indicators like Keltner channels use volatility-based band width.
* The exact `0.25` multiplier is not an industry-standard constant; it is a project calibration chosen to fit a long-term trend filter without letting neutral overpower the buy/sell rules.

---

## Sell

```json
"sell": "Close < SMA_200 and (SMA_200_slope < 0)"
```

### Literal component breakdown

`Close < SMA_200`

* The current closing price is below the 200-day simple moving average.
* Layman’s translation: **price is below its long-term average.**

`SMA_200_slope < 0`

* The slope of the 200-day average is negative.
* This means the 200-day average is falling.
* Layman’s translation: **the 200-day average must be falling.**

### Literal summary

Price is below SMA(200), and SMA(200)’s slope is negative.

### Plain-English version

That means price must be below the 200-day average **and** the 200-day average must be falling.

### Interpretation

This is a **bearish long-term trend confirmation** signal.

It is stricter than simply saying “price is below the 200-day average.” It also requires the long-term average itself to be weakening.

### Notes / confidence

* High confidence.
* This is the bearish counterpart to the buy rule.
* It avoids labeling price as bearish if price is below a still-rising 200-day average, which could be a pullback rather than confirmed long-term deterioration.

---

## Strong sell

```json id="3mbjh2"
"strong_sell": "Close < SMA_200 and (SMA_200_slope < -0.001) and falling_2bar(SMA_200)"
```

### Literal component breakdown

`Close < SMA_200`

* The current closing price is below the 200-day simple moving average.
* Layman’s translation: **price is trading below its long-term average.**

`SMA_200_slope < -0.001`

* The 200-day average has a negative slope below `-0.001`.
* This means the average is falling by more than the project’s “meaningfully falling” threshold.
* Layman’s translation: **the 200-day average itself is falling meaningfully.**

`falling_2bar(SMA_200)`

* SMA(200) is falling across the recent 2-bar check.
* In daily data, this means the 200-day average has moved downward over the recent 2-trading-day comparison.
* Layman’s translation: **the 200-day average has also been falling recently.**

### Literal summary

Price is below SMA(200), SMA(200)’s slope is meaningfully negative, and SMA(200) is falling across the recent 2-bar check.

### Plain-English version

That means price must be below the 200-day average, the 200-day average must be falling meaningfully, and the 200-day average must also be falling recently.

### Interpretation

This is a **strong bearish long-term trend confirmation** signal.

It requires three layers of bearish confirmation:

1. price is below the long-term average;
2. the long-term average is meaningfully falling;
3. the long-term average has also been falling recently.

### Notes / confidence

* High confidence.
* `-0.001` is project-calibrated.
* Because SMA(200) changes slowly, strong sell signals may lag, but that is expected for a long-term regime indicator.

---
# Initial audit note

SMA(200) is a **long-term trend / regime-filter rule**.

The current rule philosophy is:

```text id="dkbmfz"
above rising SMA(200) → bullish
very close to SMA(200) → neutral / noise band
below falling SMA(200) → bearish
```

It is **not** a mean-reversion rule. It does not say “far above SMA(200) means sell” or “far below SMA(200) means buy.”

The revised neutral rule now fits the rest of the signal structure better:

```json id="fjz4dx"
"neutral": "abs(Close/SMA_200 - 1) * 100 <= (0.25 * ATRP_200)"
```

That means neutral only suppresses the buy/sell label when price is close enough to SMA(200) that the above/below distinction may be noise. This is more consistent with the rest of the SMA(200) rule block than the earlier `1.0 × ATRP_200` version.

---
# Industry-standard baseline
- basic signal rules

> The common industry convention is closer to a three-state model:

| State                | Common industry trigger           |
| -------------------- | --------------------------------- |
| Bullish              | Price above 200-day SMA           |
| Neutral / watch zone | Price near or testing 200-day SMA |
| Bearish              | Price below 200-day SMA           |



> 5-state 'Signal' model:

| Signal        | Industry-style meaning                                  |
| ------------- | ------------------------------------------------------- |
| `strong_buy`  | Strong long-term uptrend.                               |
| `buy`         | Long-term bullish / above trend.                        |
| `neutral`     | Near the long-term trend line; unclear or transitional. |
| `sell`        | Long-term bearish / below trend.                        |
| `strong_sell` | Strong long-term downtrend.                             |


> 5-state detail:

| Signal        | Basic rule                                                              | Basic translation                                                                                                                                    |
| ------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `strong_buy`  | Price is clearly above the 200-day SMA, and the 200-day SMA is rising.  | **Strong bullish long-term trend.** Price is above its long-term average, and that long-term average is moving upward.                               |
| `buy`         | Price is above the 200-day SMA.                                         | **Bullish long-term bias.** Price is trading above its long-term average.                                                                            |
| `neutral`     | Price is near the 200-day SMA.                                          | **Transition / decision zone.** Price is close enough to the 200-day average that the market may be testing support, resistance, or trend direction. |
| `sell`        | Price is below the 200-day SMA.                                         | **Bearish long-term bias.** Price is trading below its long-term average.                                                                            |
| `strong_sell` | Price is clearly below the 200-day SMA, and the 200-day SMA is falling. | **Strong bearish long-term trend.** Price is below its long-term average, and that long-term average is moving downward.                             |
