---

## Stochastic Oscillator

The **Stochastic Oscillator** compares where the latest closing price sits relative to the recent high-low range.

For `Stoch(14,3,3)`:
* `14` = lookback window for the recent high-low range.
* First `3` = smoothing applied to `%K`.
* Second `3` = smoothing used to create `%D`.

In this project:

```text
STOCHK_14_3_3 = %K line
STOCHD_14_3_3 = %D line
```

**Simple interpretation (`%K` and `%D`):**
* `%K` above `%D` = short-term momentum is leaning bullish. 
* `%K` below `%D` = short-term momentum is leaning bearish.
* `%K` near the middle zone, around 50, suggests balanced / unclear momentum.
* `%K` rising or falling adds directional confirmation.


**Interpretation (Index values)**:
Compares closing price to its range over a period, scaled 0-100.
- Above 80 = overbought conditions
- Below 20 = oversold conditions
- **Buy**: %K line > 50 = bullish signal
	- %K crossing above %D = bullish signal
- **Sell**: %K line < 50 = bearish signal
	- %K crossing below %D = bearish signal
- **Neutral**: Around 50 or no clear crossover.

(See 'More about `%K` & `%D`' below for more information)

---
## Rule translation: Stoch(14,3,3) 

**SUMMARY:**

| Signal        | Literal trigger                                                 | Plain-English meaning                                  |
| ------------- | --------------------------------------------------------------- | ------------------------------------------------------ |
| `strong_buy`  | `%K > %D`, `%K` rising, `%K > 60`                               | Bullish Stochastic momentum is strengthening.          |
| `buy`         | `%K > %D`                                                       | Basic bullish Stochastic alignment.                    |
| `neutral`     | `%K` and `%D` are within 5 points, or `%K` is between 45 and 55 | Momentum is too close / balanced to classify strongly. |
| `sell`        | `%K < %D`                                                       | Basic bearish Stochastic alignment.                    |
| `strong_sell` | `%K < %D`, `%K` falling, `%K < 40`                              | Bearish Stochastic momentum is strengthening.          |


### Strong buy

```json
"strong_buy": "STOCHK_14_3_3 > STOCHD_14_3_3 and rising_2bar(STOCHK_14_3_3) and STOCHK_14_3_3 > 60"
```

Literal component breakdown:

* `STOCHK_14_3_3 > STOCHD_14_3_3`

  * The Stochastic %K line is above the Stochastic %D line.

* `rising_2bar(STOCHK_14_3_3)`

  * The Stochastic %K line is rising across the recent 2-trading-day check.

* `STOCHK_14_3_3 > 60`

  * The Stochastic %K value is above 60.

Literal summary:

> Stochastic %K is above %D, %K is rising across the recent 2-trading-day check, and %K is above 60.

Plain-English version:

> The intermediate Stochastic setup is bullish, and upward momentum is strengthening while already above the middle range.

Notes / confidence:

* High confidence on literal meaning.
* The `> 60` condition means this is **not** an oversold-bounce rule. It is more of a **bullish continuation / momentum confirmation** rule.
* This rule requires both **position** (`%K > %D`) and **improvement** (`%K rising`).

---

### Buy

```json
"buy": "STOCHK_14_3_3 > STOCHD_14_3_3"
```

Literal component breakdown:

* `STOCHK_14_3_3 > STOCHD_14_3_3`

  * The Stochastic %K line is above the Stochastic %D line.

Literal summary:

> Stochastic %K is above Stochastic %D.

Plain-English version:

> The intermediate Stochastic setup is bullish.

Notes / confidence:
* High confidence.
* This is the basic bullish Stochastic crossover/alignment condition.
* Unlike `strong_buy`, this does **not** require %K to be rising or above 60.


---

### Neutral
- Note: **neutral can overlap with buy or sell** because the neutral rule uses `or`. That may be intentional, because it prevents tiny %K/%D crossovers near the middle of the oscillator from being treated as meaningful.

```json
"neutral": "abs(STOCHK_14_3_3 - STOCHD_14_3_3) <= 5 or (45 <= STOCHK_14_3_3 <= 55)"
```

Literal component breakdown:

* `abs(STOCHK_14_3_3 - STOCHD_14_3_3) <= 5`

  * The gap between %K and %D is 5 points or less, ignoring which one is higher.

* `or`

  * Either side of the rule can make the signal neutral.

* `(45 <= STOCHK_14_3_3 <= 55)`

  * The %K value is between 45 and 55.

Literal summary:

> Treat Stochastic as neutral if %K and %D are very close together, or if %K is near the middle of its range.

Plain-English version:

> Momentum is too balanced or too indecisive to call clearly bullish or bearish.

Notes / confidence:

* High confidence on literal meaning.
* The “within 5 points” part means the %K/%D crossover is too small to matter.
* The `45–55` part means %K is near the middle of the oscillator range, so price is not closing strongly near the recent high or low.
* This rule can overlap with `buy` or `sell`. Example: if `%K = 52` and `%D = 50`, then `%K > %D` is bullish, but `%K` is also between 45 and 55, so the neutral rule is also true. In practice, this appears designed to suppress weak bullish/bearish readings when the oscillator is near the middle.

---

### Sell

```json
"sell": "STOCHK_14_3_3 < STOCHD_14_3_3"
```

Literal component breakdown:

* `STOCHK_14_3_3 < STOCHD_14_3_3`

  * The Stochastic %K line is below the Stochastic %D line.

Literal summary:

> Stochastic %K is below Stochastic %D.

Plain-English version:

> The intermediate Stochastic setup is bearish.

Notes / confidence:

* High confidence.
* This is the basic bearish Stochastic crossover/alignment condition.
* Unlike `strong_sell`, this does **not** require %K to be falling or below 40.

---

### Strong sell

```json
"strong_sell": "STOCHK_14_3_3 < STOCHD_14_3_3 and falling_2bar(STOCHK_14_3_3) and STOCHK_14_3_3 < 40"
```

Literal component breakdown:

* `STOCHK_14_3_3 < STOCHD_14_3_3`

  * The Stochastic %K line is below the Stochastic %D line.

* `falling_2bar(STOCHK_14_3_3)`

  * The Stochastic %K line is declining across the recent 2-trading-day check.

* `STOCHK_14_3_3 < 40`

  * The Stochastic %K value is below 40.

Literal summary:

> Stochastic %K is below %D, %K is declining across the recent 2-trading-day check, and %K is below 40.

Plain-English version:

> The intermediate Stochastic setup is bearish, and downward momentum is strengthening while already below the middle range.

Notes / confidence:

* High confidence on literal meaning.
* The `< 40` condition means this is not simply “overbought rolling over.” It is more of a bearish momentum-confirmation rule.
* This mirrors the `strong_buy` structure: crossover/alignment + 2-day direction check + threshold away from the middle.





---
### 101
**Purpose:** Compare a security's closing price to its price range over a given period to identify momentum turning points (ie,  potential market reversals) and overbought/oversold levels.

**Use when:** You want to time entries and exits based on where current price sits relative to recent highs and lows.
- Use Stochastic when you want to see whether price is closing closer to the top or bottom of its recent range, and whether short-term momentum is turning up or down.

**Key Concept:** Measures where the current close is relative to the high-low range. A close near the high suggests buying pressure; a close near the low suggests selling pressure.

**Calculation:**
- **`%K = [(Current Close - Lowest Low) ÷ (Highest High - Lowest Low)] × 100`**
- **`%D = 3-period moving average of %K`**
- Typically uses 14-period lookback

**Signals & Interpretation:**
Compares closing price to its range over a period, scaled 0-100.
- Above 80 = overbought conditions
- Below 20 = oversold conditions
- **Buy**: %K line > 50 = bullish signal
	- %K crossing above %D = bullish signal
- **Sell**: %K line < 50 = bearish signal
	- %K crossing below %D = bearish signal
- **Neutral**: Around 50 or no clear crossover.

**Tips:**
- Divergences with price indicate potential reversals
- Look for signals when leaving extreme zones

**Optimal Conditions:** Most effective in ranging markets and during pullbacks in trends. Works well on shorter timeframes for day trading and swing trading.

**Limitations:** Prone to false signals in strong trending markets. Can stay in extreme zones longer than expected during powerful moves.


#### More about `%K` & `%D`

When people refer to "stochastic" in general, they're speaking about **%K**.

More precisely:

```text
%K = where the latest close sits within the recent high-low range
```

So when people say:

> “The Stochastic Oscillator ranges from 0 to 100 and shows where the close sits relative to the recent high-low range,”

they are usually referring to **%K**, because %K is the direct range-position calculation.

## Difference between %K and %D

| Term | What it is                           | What it tells you                                                                                     |
| ---- | ------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| `%K` | The primary Stochastic line          | Where the close is within the recent high-low range, usually after smoothing depending on the version |
| `%D` | A moving average / smoothing of `%K` | The signal line used to judge whether %K is turning up or down                                        |

In the project’s naming:

```text
STOCHK_14_3_3 = %K
STOCHD_14_3_3 = %D
```

So for this rule:

```json
"buy": "STOCHK_14_3_3 > STOCHD_14_3_3"
```

Literal translation:

> The %K line is above the %D line.

Plain-English version:

> "*The current Stochastic reading is stronger than its smoothed signal line*".

## What `%K = 80` means

A `%K` value around `80` means:
> "*The close is near the upper end of its recent high-low range.*"

A `%K` value around `20` means:
> "*The close is near the lower end of its recent high-low range.*"

A `%K` value around `50` means:
> "*The close is near the middle of its recent range.*"

## What `%D` adds

`%D` does **not** directly tell you where the latest close sits in the range. It is a smoothed version of `%K`.

So `%D` is more like:

> The recent average / signal-line version of the Stochastic reading.

That is why the rulebook compares `%K` to `%D`:

```text
%K > %D  → current Stochastic is above its smoothed signal line
%K < %D  → current Stochastic is below its smoothed signal line
```

For clarity, I should phrase future translations like this:

> **%K** shows where the close sits within the recent high-low range. **%D** is the smoothed signal line used to confirm whether %K is turning up or down.


## Audit

- 6/28/26

| Rule element                 |                       Industry-consistent? | Comment                                                       |
| ---------------------------- | -----------------------------------------: | ------------------------------------------------------------- |
| `%K > %D` = bullish          |                                        Yes | %K/%D crossovers are a standard Stochastic concept.           |
| `%K < %D` = bearish          |                                        Yes | Same.                                                         |
| Rising %K confirms strength  |                                        Yes | Direction of %K is commonly used as momentum confirmation.    |
| Falling %K confirms weakness |                                        Yes | Same.                                                         |
| Middle-zone neutrality       |                                 Reasonable | Not the classic headline rule, but conceptually sensible.     |
| Avoiding tiny %K/%D gaps     |                                 Reasonable | Helps suppress noise.                                         |
| Strong buy above 60          |                                     Custom | This is not the classic oversold-reversal Stochastic setup.   |
| Strong sell below 40         |                                     Custom | This is not the classic overbought-reversal Stochastic setup. |
| No 80/20 logic               | Nonstandard relative to classic Stochastic | Classic use usually focuses on 80/20 zones.                   |


Opinion: **the Stoch(14,3,3) rules are adequate as a custom momentum-confirmation rule, but they are not “classic textbook Stochastic” rules.** They are closer to a **trend/momentum continuation interpretation** than a traditional **overbought/oversold reversal interpretation**.

### Industry-standard baseline

Standard Stochastic interpretation usually emphasizes:

* Stochastic ranges from **0 to 100** and shows where the close sits relative to the recent high-low range.
* The common overbought / oversold zones are **above 80** and **below 20**.
* A classic buy signal often involves Stochastic moving up from oversold, especially below/around 20.
* A classic sell signal often involves Stochastic moving down from overbought, especially above/around 80.
* %K / %D crossovers are often most meaningful when they occur in overbought or oversold zones, not necessarily in the middle of the range. ([Fidelity][1])

Your current `Stoch(14,3,3)` rules are:

```json
"strong_buy": "STOCHK_14_3_3 > STOCHD_14_3_3 and rising_2bar(STOCHK_14_3_3) and STOCHK_14_3_3 > 60",
"buy": "STOCHK_14_3_3 > STOCHD_14_3_3",
"neutral": "abs(STOCHK_14_3_3 - STOCHD_14_3_3) <= 5 or (45 <= STOCHK_14_3_3 <= 55)",
"sell": "STOCHK_14_3_3 < STOCHD_14_3_3",
"strong_sell": "STOCHK_14_3_3 < STOCHD_14_3_3 and falling_2bar(STOCHK_14_3_3) and STOCHK_14_3_3 < 40"
```

These rules **do not use the classic 80/20 overbought/oversold framework**. They use:

* `%K > %D` as bullish
* `%K < %D` as bearish
* `%K > 60` as strong bullish confirmation
* `%K < 40` as strong bearish confirmation
* `45–55` as a neutral middle zone
* `%K/%D gap <= 5` as a “too close to matter” neutral filter

### Are they consistent with industry standards?

**Partially.**

They are consistent with industry standards in these ways:

| Rule element                 |                       Industry-consistent? | Comment                                                       |
| ---------------------------- | -----------------------------------------: | ------------------------------------------------------------- |
| `%K > %D` = bullish          |                                        Yes | %K/%D crossovers are a standard Stochastic concept.           |
| `%K < %D` = bearish          |                                        Yes | Same.                                                         |
| Rising %K confirms strength  |                                        Yes | Direction of %K is commonly used as momentum confirmation.    |
| Falling %K confirms weakness |                                        Yes | Same.                                                         |
| Middle-zone neutrality       |                                 Reasonable | Not the classic headline rule, but conceptually sensible.     |
| Avoiding tiny %K/%D gaps     |                                 Reasonable | Helps suppress noise.                                         |
| Strong buy above 60          |                                     Custom | This is not the classic oversold-reversal Stochastic setup.   |
| Strong sell below 40         |                                     Custom | This is not the classic overbought-reversal Stochastic setup. |
| No 80/20 logic               | Nonstandard relative to classic Stochastic | Classic use usually focuses on 80/20 zones.                   |

So I would call these **industry-informed but custom**, not pure industry-standard.

## Are they overkill?

For a rule-engine heatmap, I do **not** think they are overkill.

The `strong_buy` and `strong_sell` rules require three things:

```text
directional alignment + recent direction + away from the neutral middle
```

That is a reasonable structure for a heatmap because you do not want every small crossover to immediately become strong buy or strong sell.

Where I do think the rules may be **over-simplified** is the plain `buy` and `sell` logic:

```text
buy  = %K > %D
sell = %K < %D
```

That is very sensitive. %K and %D can cross often, especially near the middle of the range. The neutral rule tries to suppress that, but because this depends on rule-evaluation ordering, it needs to be tested carefully.

## Are they inadequate?

Not inadequate, but they are **incomplete if the goal is classic Stochastic interpretation**.

Classic Stochastic would care more about:

```text
oversold bounce: %K crossing up from below 20
overbought rollover: %K crossing down from above 80
```

Your current rule does not really say:

> “Buy because the stock is oversold and turning up.”

Instead it says:

> “Buy because %K is above %D.”

And strong buy says:

> “Strong buy because %K is above %D, rising, and already above 60.”

That is more of a **momentum continuation** rule.

### Recommendation

I would keep these rules only if your intended Stochastic interpretation is:

> “Use Stochastic as a short/intermediate momentum confirmation tool.”

In that case, these rules are **adequate and explainable**.

I would **not** present them as classic Stochastic overbought/oversold rules. For that, they would need a different design using 80/20 zones.

My recommended label for the current rule family would be:

> **Stochastic momentum-confirmation rule, not oversold/overbought reversal rule.**

### My audit grade

> See the introductory markdown table summary.

Bottom-line opinion:
> **Adequate and usable, but only if we explicitly document that this is a momentum-confirmation version of Stochastic. If you want classic Stochastic behavior, these rules should be redesigned around 80/20 overbought/oversold zones and crossovers out of those zones.**
