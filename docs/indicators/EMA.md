# Summary: EMA(20) 'Signals'
Status: A

| Signal        | Layman’s translation                                                              | Literal trigger                                                       | Rule logic                                                                                                                |
| ------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `strong_buy`  | Price is above a 20-period EMA that is clearly and recently rising.               | `Close > EMA_20`, `EMA_20_slope > 0.002`, and `rising_2bar(EMA_20)`   | Price is above EMA(20), the EMA(20) slope is meaningfully positive, and EMA(20) is rising across the recent 2-bar check.  |
| `buy`         | Price is above the 20-period EMA, and the 20-period EMA is rising.                | `Close > EMA_20` and `EMA_20_slope > 0`                               | Price is above EMA(20), and EMA(20)’s slope is positive.                                                                  |
| `neutral`     | Price is close enough to the 20-period EMA that the rule treats the gap as noise. | Percent distance from EMA(20) is within `0.50 × ATRP_20`              | Price is within one-half of the stock’s typical 20-period price movement range.                                           |
| `sell`        | Price is below the 20-period EMA, and the 20-period EMA is falling.               | `Close < EMA_20` and `EMA_20_slope < 0`                               | Price is below EMA(20), and EMA(20)’s slope is negative.                                                                  |
| `strong_sell` | Price is below a 20-period EMA that is clearly and recently falling.              | `Close < EMA_20`, `EMA_20_slope < -0.002`, and `falling_2bar(EMA_20)` | Price is below EMA(20), the EMA(20) slope is meaningfully negative, and EMA(20) is falling across the recent 2-bar check. |

---
# EMA(20) — brief overview

For `EMA(20)`:

```text
EMA_20 = a 20-period moving average that gives more weight to recent prices
```

Compared with a simple moving average, an EMA reacts faster to new price changes because it places more emphasis on recent prices. That makes EMA(20) useful as a short-to-intermediate trend reference rather than a long-term regime filter.

Simple interpretation:
* If price is above EMA(20), price is above its recent/intermediate trend baseline.
* If price is below EMA(20), price is below its recent/intermediate trend baseline.
* If EMA(20) is rising, recent trend direction is improving.
* If EMA(20) is falling, recent trend direction is weakening.
* Because EMA(20) is more responsive than SMA(20), it can react earlier but may also be more sensitive to noise.

Value-added use:

> Use EMA(20) when you want a responsive short-to-intermediate trend filter that can identify whether price is trading above, near, or below its recent trend baseline.

Use with:
EMA is often paired with trend-strength or momentum tools such as ADX or RSI for confirmation.
* **ADX** — to check whether the EMA(20) trend has actual trend strength. ADX is commonly used for trend-strength confirmation.
* **MACD or ROC** — to confirm whether the EMA(20) direction is supported by momentum. MACD combines moving averages and momentum, and ROC gives a direct momentum read.
* **RSI** — to check whether an EMA(20) move is supported by momentum or becoming stretched.
* **OBV / CMF / volume confirmation** — to check whether the move above or below EMA(20) is supported by participation. Trend-trading references commonly pair moving averages with momentum and volume indicators such as MACD, RSI, and OBV. ([Investopedia][2])
* **SMA(50) or EMA(50)** — to compare the short/intermediate EMA(20) posture against a slower medium-term trend baseline.

---
# EMA(20) Rule Translation

## Strong buy

```json
"strong_buy": "Close > EMA_20 and EMA_20_slope > 0.002 and rising_2bar(EMA_20)"
```

### Literal component breakdown

`Close > EMA_20`

* The current closing price is above the 20-period exponential moving average.
* Layman’s translation: **price is trading above its recent/intermediate trend baseline.**

`EMA_20_slope > 0.002`

* The EMA(20) line has a positive slope greater than `0.002`.
* This means the EMA(20) line itself is rising by more than the project’s “meaningfully rising” threshold.
* Layman’s translation: **the 20-period EMA itself is rising meaningfully.**

`rising_2bar(EMA_20)`

* EMA(20) is rising across the recent 2-bar check.
* In daily data, this means EMA(20) has moved upward over the recent 2-trading-day comparison.
* Layman’s translation: **the 20-period EMA has also been rising recently.**

### Literal summary

Price is above EMA(20), EMA(20)’s slope is meaningfully positive, and EMA(20) is rising across the recent 2-bar check.

### Plain-English version

That means price must be above the 20-period EMA, the 20-period EMA must be rising meaningfully, and the 20-period EMA must also be rising recently.

### Interpretation

This is a **strong bullish short-to-intermediate trend confirmation** signal.

It requires three layers of confirmation:

1. price is above the EMA(20) baseline;
2. the EMA(20) line is meaningfully rising;
3. the EMA(20) line has also been rising recently.

### Notes / confidence
* High confidence on the literal interpretation.
* `0.002` is a project-calibrated raw slope threshold, not a universal EMA standard.
* EMA(20) is more responsive than SMA(20), so strong signals may appear earlier than an SMA-based signal, but may also be more sensitive to short-term noise.

---

## Buy

```json
"buy": "Close > EMA_20 and EMA_20_slope > 0"
```

### Literal component breakdown

`Close > EMA_20`

* The current closing price is above the 20-period exponential moving average.
* Layman’s translation: **price is above its recent/intermediate trend baseline.**

`EMA_20_slope > 0`

* The slope of the EMA(20) line is positive.
* This means EMA(20) is rising, even if it is not rising strongly enough to qualify as `strong_buy`.
* Layman’s translation: **the 20-period EMA must be rising.**

### Literal summary

Price is above EMA(20), and EMA(20)’s slope is positive.

### Plain-English version

That means price must be above the 20-period EMA **and** the 20-period EMA must be rising.

### Interpretation

This is a **bullish short-to-intermediate trend confirmation** signal.

It is stricter than simply saying “price is above EMA(20).” It also requires the EMA(20) line itself to be moving upward.

### Notes / confidence
* This avoids labeling price as bullish if price is above a flat or falling EMA(20).
* That matters because a price sitting above a falling EMA can be a temporary bounce rather than a confirmed improving trend.

---

## Neutral

```json
"neutral": "abs(Close/EMA_20 - 1) * 100 <= (0.50 * ATRP_20)"
```

### Literal component breakdown

`Close/EMA_20`

* This compares the current closing price to EMA(20).
* If the result is above `1`, price is above EMA(20).
* If the result is below `1`, price is below EMA(20).
* Layman’s translation: **compare price to the 20-period EMA.**

`Close/EMA_20 - 1`

* This converts the price/EMA comparison into a distance from EMA(20).
* Example: `1.02 - 1 = 0.02`, meaning price is 2% above EMA(20).
* Example: `0.98 - 1 = -0.02`, meaning price is 2% below EMA(20).
* Layman’s translation: **measure how far price is from the 20-period EMA.**

`abs(Close/EMA_20 - 1)`

* `abs()` ignores whether price is above or below EMA(20).
* It only measures the size of the gap.
* Layman’s translation: **measure the gap from EMA(20), regardless of direction.**

`abs(Close/EMA_20 - 1) * 100`

* This converts the price/EMA gap into percentage units.
* Example: `0.02 * 100 = 2.0`, meaning 2%.
* Layman’s translation: **express the price-vs-EMA(20) gap as a normal percent.**

`ATRP_20`

* ATRP(20) estimates the stock’s typical price movement range over the last 20 periods, expressed as a percent of price.
* Layman’s translation: **the stock’s typical 20-period price movement range, expressed as a percentage of price.**

`0.50 * ATRP_20`

* This uses half of the 20-period ATRP value as the neutral threshold.
* Layman’s translation: **one-half of the stock’s typical 20-period price movement range.**
    - Or, "one-half of an ATRP(20)-sized percentage distance from EMA(20)".

`abs(Close/EMA_20 - 1) * 100 <= (0.50 * ATRP_20)`

* Price is neutral if its percent distance from EMA(20) is no more than half of ATRP(20).
* Layman’s translation: **if price is no farther from EMA(20) than half of the stock’s typical 20-period price movement range, treat it as close enough to EMA(20) that the signal is neutral.**

### Literal summary

Price is within one-half of an ATRP(20)-sized percentage distance from EMA(20).

### Plain-English version

That means price is close enough to the 20-period EMA that the rule treats the difference as noise rather than a clear bullish or bearish signal.

### Interpretation

This is a **short-to-intermediate trend transition / noise-band rule**.

It does not say the stock has no trend in every sense. It says that, for this EMA(20) signal, price is close enough to EMA(20) that the rule avoids calling the move clearly bullish or clearly bearish.

### Notes / confidence
* The `0.50 × ATRP_20` setting fits the daily-swing / short-to-intermediate EMA use case: wide enough to avoid tiny whipsaws, but not so wide that it suppresses valid buy/sell signals.
* The industry-consistent analogy is a moving-average envelope: a moving average is used as the baseline, and bands around it help avoid treating tiny crosses as meaningful signals. Moving-average envelopes are commonly placed above and below moving averages; similar channel indicators vary band width using volatility.

---

## Sell

```json
"sell": "Close < EMA_20 and EMA_20_slope < 0"
```

### Literal component breakdown

`Close < EMA_20`

* The current closing price is below the 20-period exponential moving average.
* Layman’s translation: **price is below its recent/intermediate trend baseline.**

`EMA_20_slope < 0`

* The slope of the EMA(20) line is negative.
* This means EMA(20) is falling.
* Layman’s translation: **the 20-period EMA must be falling.**

### Literal summary

Price is below EMA(20), and EMA(20)’s slope is negative.

### Plain-English version

That means price must be below the 20-period EMA **and** the 20-period EMA must be falling.

### Interpretation

This is a **bearish short-to-intermediate trend confirmation** signal.

It is stricter than simply saying “price is below EMA(20).” It also requires the EMA(20) line itself to be weakening.

### Notes / confidence
* This avoids labeling price as bearish if price is below a still-rising EMA(20), which could be a short-term pullback rather than a confirmed trend deterioration.

---

## Strong sell

```json
"strong_sell": "Close < EMA_20 and EMA_20_slope < -0.002 and falling_2bar(EMA_20)"
```

### Literal component breakdown

`Close < EMA_20`

* The current closing price is below the 20-period exponential moving average.
* Layman’s translation: **price is trading below its recent/intermediate trend baseline.**

`EMA_20_slope < -0.002`

* The EMA(20) line has a negative slope below `-0.002`.
* This means the EMA(20) line itself is falling by more than the project’s “meaningfully falling” threshold.
* Layman’s translation: **the 20-period EMA itself is falling meaningfully.**

`falling_2bar(EMA_20)`

* EMA(20) is falling across the recent 2-bar check.
* In daily data, this means EMA(20) has moved downward over the recent 2-trading-day comparison.
* Layman’s translation: **the 20-period EMA has also been falling recently.**

### Literal summary

Price is below EMA(20), EMA(20)’s slope is meaningfully negative, and EMA(20) is falling across the recent 2-bar check.

### Plain-English version

That means price must be below the 20-period EMA, the 20-period EMA must be falling meaningfully, and the 20-period EMA must also be falling recently.

### Interpretation

This is a **strong bearish short-to-intermediate trend confirmation** signal.

It requires three layers of bearish confirmation:
1. price is below the EMA(20) baseline;
2. the EMA(20) line is meaningfully falling;
3. the EMA(20) line has also been falling recently.

### Notes / confidence
* `-0.002` is project-calibrated.
* EMA(20) is more responsive than SMA(20), so strong sell signals may appear earlier than an SMA-based signal, but may also be more sensitive to short-term noise.


---
# Industry-standard Baseline

Industry usage usually does **not** define a formal five-level EMA(20) scale.
The simpler industry pattern is:
- price above EMA = bullish bias,
- price near EMA = transition/support-resistance test,
- price below EMA = bearish bias


| Signal        | Basic industry-style rule                 | Basic translation                                      |
| ------------- | ----------------------------------------- | ------------------------------------------------------ |
| `strong_buy`  | Price is clearly above a rising EMA(20).  | Strong short-to-intermediate bullish trend.            |
| `buy`         | Price is above EMA(20).                   | Bullish short-to-intermediate bias.                    |
| `neutral`     | Price is near EMA(20).                    | Transition zone; price is close to the trend baseline. |
| `sell`        | Price is below EMA(20).                   | Bearish short-to-intermediate bias.                    |
| `strong_sell` | Price is clearly below a falling EMA(20). | Strong short-to-intermediate bearish trend.            |


---


**What it is**
EMA is a moving average that gives more weight to recent prices than older prices.

**Why traders use it**
Because it reacts faster than a simple moving average, EMA is often used to track short- and medium-term trend direction.

**Common interpretations**
Shorter EMAs react faster but can be noisier.
Longer EMAs react more slowly but can be more stable as trend references.

**Limitations**
EMA can generate whipsaws in choppy markets and can lag major turning points despite being more responsive than SMA.

**Use with**
EMA is often paired with trend-strength or momentum tools such as ADX or RSI for confirmation.

**Common mistakes**
Treating every EMA cross or touch as equally meaningful without considering broader market context.