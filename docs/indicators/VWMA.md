## Summary: VWMA Signals
**<u>Class</u>**: Trend / Moving Average
**<u>aka</u>**: Volume-Weighted Moving Average

VWMA is a moving average that gives **more influence to prices traded on heavier-volume sessions** and less influence to prices traded on lighter-volume sessions.

At the simplest level, this app asks three questions:
1. **Is price meaningfully above or below VWMA relative to the stock's recent volatility?**
2. **Is VWMA itself rising or falling fast enough to support that direction?**
3. **For a Strong state, is the volume-weighted average also meaningfully above or below the matching SMA, and is that VWMA-vs-SMA relationship moving farther in the confirming direction?**

The project uses VWMA as a **directional trend-confirmation indicator**, not as an overbought/oversold or mean-reversion indicator.

> **Interpreting VWMA:**
>
> ```text
> VWMA(20) > SMA(20)
> ```
> - suggests higher-volume observations have tended to occur at relatively higher prices than the equally weighted average would imply.


### Summary Rules Translation

The three VWMA periods use the same rule structure. In the table below, `k` is the period-specific Price-vs-VWMA threshold: `0.25 ATR` for VWMA(10), `0.50 ATR` for VWMA(20), and `1.00 ATR` for VWMA(50).

| Signal | Literal trigger | Layman's translation | Rule logic | Bottom-line |
| --- | --- | --- | --- | --- |
| **Strong Buy (+2)** | Price is more than `+k ATR` above VWMA; normalized 14-bar VWMA slope is `> +0.05%/bar`; VWMA is at least `+0.15 ATR` above SMA; current VWMA/SMA % spread is greater than its prior value | Price is meaningfully above a clearly rising VWMA, and volume weighting is providing additional bullish confirmation relative to SMA | Bullish price-distance gate **AND** bullish slope gate **AND** positive VWMA/SMA spread threshold **AND** spread rising | **Qualified bullish VWMA trend + strong volume-weighted confirmation.** |
| **Buy (+1)** | Price is more than `+k ATR` above VWMA; slope is `> +0.05%/bar`; and **either** VWMA is less than `+0.15 ATR` above SMA **or** the VWMA/SMA % spread is not rising | The primary bullish trend conditions pass, but at least one Strong-Buy confirmation condition does not | Bullish price-distance gate **AND** bullish slope gate **AND** failure of at least one Strong-Buy confirmation clause | **Bullish VWMA trend, but not enough additional VWMA-vs-SMA confirmation for Strong Buy.** |
| **Neutral (0)** | Explicit rule is blank; Neutral is the mature fallback when none of the four directional rules matches | Price position and VWMA direction do not jointly satisfy a qualified bullish or bearish state | Fallback when Strong Buy / Buy / Sell / Strong Sell are all false | **VWMA does not currently provide a sufficiently qualified directional signal.** |
| **Sell (-1)** | Price is more than `-k ATR` below VWMA; slope is `< -0.05%/bar`; and **either** VWMA is less than `0.15 ATR` below SMA **or** the VWMA/SMA % spread is not falling | The primary bearish trend conditions pass, but at least one Strong-Sell confirmation condition does not | Bearish price-distance gate **AND** bearish slope gate **AND** failure of at least one Strong-Sell confirmation clause | **Bearish VWMA trend, but not enough additional VWMA-vs-SMA confirmation for Strong Sell.** |
| **Strong Sell (-2)** | Price is more than `-k ATR` below VWMA; slope is `< -0.05%/bar`; VWMA is at least `-0.15 ATR` below SMA; current VWMA/SMA % spread is less than its prior value | Price is meaningfully below a clearly falling VWMA, and volume weighting is providing additional bearish confirmation relative to SMA | Bearish price-distance gate **AND** bearish slope gate **AND** negative VWMA/SMA spread threshold **AND** spread falling | **Qualified bearish VWMA trend + strong volume-weighted confirmation.** |

> **Important:** `Strong Buy` and `Strong Sell` do **not** simply mean that price is farther from VWMA. A Strong state means the ordinary directional conditions already pass **and** the matching VWMA-vs-SMA relationship provides the project's additional confirmation.

### Signal interpretation — quick reference

| Signal | What it means | What it does **not** necessarily mean | Useful follow-up question |
| --- | --- | --- | --- |
| **Strong Buy (+2)** | Price is materially above a rising VWMA and VWMA is sufficiently above SMA with the signed VWMA/SMA spread still rising | That price must rise next, or that today's individual session was bullish | Is today's volume/price context reinforcing or disagreeing with the broader bullish state? |
| **Buy (+1)** | Price and VWMA slope jointly qualify as bullish | That VWMA is already above SMA, or that Strong-Buy confirmation is close | Which Strong-Buy confirmation clause is missing: spread size, spread direction, or both? |
| **Neutral (0)** | The current observation does not satisfy either complete directional gate | That price equals VWMA or VWMA is perfectly flat | Is price distance too small, slope too weak, or price/slope direction mixed? |
| **Sell (-1)** | Price and VWMA slope jointly qualify as bearish | That VWMA is already below SMA, or that Strong-Sell confirmation is close | Which Strong-Sell confirmation clause is missing: spread size, spread direction, or both? |
| **Strong Sell (-2)** | Price is materially below a falling VWMA and VWMA is sufficiently below SMA with the signed VWMA/SMA spread still falling | That price must fall next, or that today's individual session was bearish | Is today's volume/price context reinforcing or disagreeing with the broader bearish state? |

The Signal is a **current-state classification**. It is not limited to the first day a threshold is crossed. Buy/Sell states can persist while their conditions remain true. Strong states can also persist across consecutive observations when their base directional conditions remain true and the VWMA/SMA spread continues moving in the confirming direction.

---

### Interpreting the full VWMA readout together
> For more details, see the "Context and Hover Fields" section
> For examples, see the "Worked Examples" section below.

---
The VWMA display is easiest to understand as three layers:

| Layer | What it tells you | Shortest translation |
| --- | --- | --- |
| **Primary Signal** | Whether Price-vs-VWMA distance and normalized VWMA slope qualify as bullish/bearish, with VWMA/SMA reinforcement for Strong states | **What is the qualified VWMA trend state?** |
| **VWMA-vs-SMA / 1D MA context** | Whether volume weighting is strengthening or weakening the average relative to SMA, plus the latest one-day movement of each average | **How is the volume-weighted trend reference behaving relative to the ordinary average?** |
| **Current-session volume context** | How heavy/light today's volume is, whether it is extreme, and whether today's price rose or fell | **How much participation accompanied today's move?** |

These layers are related but should not be treated as three votes that must always agree.

#### Common combinations

| Signal | VWMA/SMA context | Volume / price context | Beginner interpretation |
| --- | --- | --- | --- |
| **Strong Buy** | VWMA sufficiently above SMA; spread rising | **Blue ▲** | **Broad VWMA trend and today's high-volume price move both point bullish.** The latest session reinforces the already-qualified Strong Buy state. |
| **Strong Buy** | VWMA sufficiently above SMA; spread rising | **Red ▲** | **The broader VWMA state remains strongly bullish, but today's individual session fell on exceptionally high volume.** That short-term disagreement deserves attention; it does not retroactively erase the Strong Buy rule state. |
| **Buy** | VWMA below SMA but spread rising | Ordinary volume | **Price is above a rising VWMA, but VWMA has not yet achieved the required Strong-Buy separation above SMA.** The spread may be improving without being strong enough. |
| **Buy** | Strong confirmation incomplete | **Blue ▼** | **The broader VWMA trend is bullish, but today's up move occurred on exceptionally light participation.** That is weaker current-session confirmation, not an automatic downgrade of the score. |
| **Neutral** | Any non-Strong context | **Blue ▲** | **Today's price rose on exceptional volume, but Price-vs-VWMA and normalized slope do not currently satisfy the VWMA bullish rule.** Current-session enthusiasm is not enough by itself to create a Buy state. |
| **Sell** | VWMA above SMA but spread falling | Ordinary volume | **Price is below a falling VWMA, but VWMA has not yet achieved the required Strong-Sell separation below SMA.** The VWMA/SMA relationship may be deteriorating without being strong enough. |
| **Strong Sell** | VWMA sufficiently below SMA; spread falling | **Red ▲** | **Broad VWMA trend and today's high-volume down move both point bearish.** Current-session participation reinforces the already-qualified Strong Sell state. |
| **Strong Sell** | VWMA sufficiently below SMA; spread falling | **Blue ▼** | **The broader VWMA state remains strongly bearish, while today's counter-move higher occurred on exceptionally light volume.** The two layers describe different time horizons rather than contradicting one another. |

#### A practical reading order

When looking at a VWMA hover, use this order:

1. **Signal** — What qualified five-state VWMA condition exists?
2. **Price vs. MA** — How far is price from VWMA in raw terms?
3. **VWMA vs SMA** — Is volume weighting lifting or depressing the average relative to SMA, and is that signed relationship rising or falling?
4. **1D Direction** — What did VWMA and SMA do since yesterday?
5. **Volume Activity** — Was today's trading participation ordinary, heavy, light, or extreme?
6. **▲ / ▼ and color** — If volume is extreme, did price rise or fall on that session?

The shortest useful summary is:

> **Signal = qualified VWMA trend state.**
> **VWMA vs SMA = whether volume weighting is strengthening or weakening the trend reference relative to SMA.**
> **1D Direction = what the two averages did since yesterday.**
> **Volume Activity = how unusual today's participation is.**
> **Arrow/color = extreme volume plus today's price direction.**
---

## VWMA — brief overview

### What VWMA measures

VWMA is a moving average of price in which each observation is weighted by that session's trading volume.

Conceptually:

```text
VWMA(N) =
Σ(Close × Volume)
-----------------
Σ(Volume)
```

over the most recent `N` periods.

A Simple Moving Average gives each observation equal weight:

```text
SMA(N) =
Close1 + Close2 + ... + CloseN
------------------------------
              N
```

VWMA instead asks:

> **Where does the average price move when heavier-volume sessions are allowed to matter more than lighter-volume sessions?**

A high-volume session contributes more to VWMA than a low-volume session.

### Simple example

Suppose there are three sessions:

| Day | Close | Volume |
| --- | ---: | ---: |
| 1 | $100 | 1M |
| 2 | $101 | 1M |
| 3 | $106 | 5M |

The 3-day SMA is:

```text
(100 + 101 + 106) / 3
= 102.33
```

VWMA gives Day 3 much more influence because five times as many shares traded:

```text
VWMA =
(100 × 1M) + (101 × 1M) + (106 × 5M)
-------------------------------------
              1M + 1M + 5M

= 731M / 7M
≈ 104.43
```

So:

```text
SMA  = 102.33
VWMA = 104.43
```

In plain English:

> **The market did much more of its trading near the higher price, so the volume-weighted average is pulled upward relative to the equal-weighted SMA.**

### VWMA versus SMA and EMA

| Average | What receives more weight? | Main question |
| --- | --- | --- |
| **SMA** | Every session equally | **What is the simple average closing price over this period?** |
| **EMA** | More recent prices | **What is the price trend when newer observations receive more influence?** |
| **VWMA** | Higher-volume sessions | **How does the average price change when heavier trading activity receives more influence?** |

VWMA's differentiated value in this project is not simply that it is another moving-average line. It tells you whether **volume weighting materially changes the trend reference relative to an ordinary SMA**.

If VWMA is above SMA, heavier-volume observations have, on balance, pulled the weighted average upward relative to the equal-weighted average.

If VWMA is below SMA, heavier-volume observations have, on balance, pulled the weighted average downward relative to the equal-weighted average.

That is why the project uses the VWMA-vs-SMA relationship as **additional Strong-state confirmation** rather than using raw current-day volume directly in the primary score.


$$----------$$
> **Comparing VWMA to SMA:**
> Unlike SMA, every session does **not** contribute equally.
> A high-volume day pulls the moving average toward its price more strongly than a low-volume day.
> - **SMA**: Gives equal importance to every price point in its calculation.
> - **VWMA**: Gives greater importance to price points where a significant amount of trading occurred, providing a more meaningful average

$~~$

**VWMA should answer whether the price trend is being shaped disproportionately by higher-volume sessions.**
> Compare it with an SMA to reveal the impact of volume weighting.
> - If VWMA is above SMA, that can indicate heavier volume occurred on relatively higher-closing sessions;
> - VWMA below SMA can indicate relatively heavier volume on lower-closing sessions


---

## Value-added use

VWMA adds information that is not visible from price alone because the same closing-price path can produce a different moving-average reference depending on **where the heavier trading occurred**.

The project uses that information in three layers:

1. **Price vs VWMA** — Is price meaningfully displaced from the volume-weighted trend reference?
2. **VWMA slope** — Is that volume-weighted trend reference itself moving meaningfully in the same direction?
3. **VWMA vs SMA** — Is volume weighting changing the trend reference enough, and in a direction that strengthens the interpretation?

The current day's raw volume is then shown separately as **context**, so a user can distinguish the broader VWMA state from what happened in the latest individual session.

### Useful companion indicators in this dashboard

| Companion | Complementary role |
| --- | --- |
| **SMA / EMA / HMA** | Compare VWMA's volume-weighted trend with equal-weighted, recency-weighted, or lower-lag moving-average views |
| **ADX** | Adds a separate view of trend strength rather than trend direction alone |
| **ROC / RSI / CCI / Stochastic** | Adds momentum or stretch context that can agree with or challenge the moving-average trend state |
| **CMF / MFI / OBV** | Adds separate volume-flow or money-flow context rather than merely weighting the average price by volume |
| **ATR / ATRP / Bollinger Bandwidth** | Adds volatility context, which can help distinguish ordinary movement from unusually volatile conditions |

No companion indicator automatically overrides the VWMA Signal. They answer different questions.

---

## VWMA parameter variants

The app uses:

```text
VWMA(10)
VWMA(20)
VWMA(50)
```

| Variant | Horizon | Character | `k` price-distance threshold |
| --- | --- | --- | ---: |
| **VWMA(10)** | Short term | Fastest of the three; reacts most quickly to recent price/volume behavior | `0.25 ATR(14)` |
| **VWMA(20)** | Medium term | Intermediate balance between responsiveness and smoothing | `0.50 ATR(14)` |
| **VWMA(50)** | Longer term | Smoothest; requires the largest Price-vs-VWMA displacement before a directional state qualifies | `1.00 ATR(14)` |

All three use:

```text
slope_deadband_pct_per_bar = 0.05
strong_spread_atr          = 0.15
```

The wider `k` requirement for longer horizons is deliberate: VWMA(50) must see a larger price displacement than VWMA(10) before the app treats the observation as directionally qualified.

---

## How to read the VWMA heatmap and hover

### What the cell shows

The number printed in a VWMA heatmap cell is the current raw VWMA value for that period.

The **background color** comes from the five-state rule-engine score:

```text
+2  Strong Buy
+1  Buy
 0  Neutral
-1  Sell
-2  Strong Sell
```

The displayed number and the background color therefore represent different things:

```text
printed value
→ current VWMA level

cell color
→ five-state VWMA Signal
```

### Compact value / price / volume lines

The hover begins with factual current-observation context such as:

```text
Value: 209.39 | Price: 211.34 | Vol: 34.7M
Δ vs prior day: +0.75 (+0.4%) | $: +5.30 (+2.6%) | Vol: +4.2M (+13.8%)
```

This means:
- `Value` = current VWMA value;
- `Price` = current closing price;
- `Vol` = current trading volume;
- first delta = VWMA change from the prior observation;
- `$` = price change from the prior observation;
- second `Vol` = raw volume change from the prior observation.

These are factual display fields. They do not independently alter the VWMA Signal.

### `Trend`

The hover's generic `Trend` field describes the displayed VWMA value's **one-observation direction**. When price trend is also shown, it describes the current price's one-observation direction as separate context.

This is not the same as the **normalized 14-bar linear-regression slope** used by the VWMA rulebook.

### `Price vs. MA`

Example:

```text
Price vs. MA: +1.95 (+0.9%)
```

This is the visible raw Price-minus-VWMA relationship:

```text
absolute difference = Close - VWMA
percentage difference = (Close / VWMA - 1) × 100
```

The Signal does **not** score directly from this displayed percentage. The rulebook uses the ATR-normalized form explained below.

---

## VWMA Rule Translation

The VWMA(10), VWMA(20), and VWMA(50) rules use the same structure. The examples below use **VWMA(20)** because it is the middle horizon. For VWMA(10) and VWMA(50), substitute the matching VWMA/SMA columns and the appropriate `k` value.

### Common rule components

Before interpreting the five states, it helps to separate the four measurements used by the rules.

#### 1. Price distance from VWMA, normalized by ATR

For VWMA(20):

```text
(Close - VWMA_20) / ATR_14
```

Component breakdown:

`Close - VWMA_20`

- Current closing price minus current VWMA(20).
- Positive means price is above VWMA; negative means price is below VWMA.

`/ ATR_14`

- Divides that price difference by current ATR(14).
- This converts the raw dollar gap into a volatility-relative distance.

Layman's translation:

> **How far is price above or below VWMA compared with how much this stock normally moves?**

For VWMA(20):

```text
> +0.50
```

means price must be **more than one-half ATR above VWMA** for the bullish base gate.

```text
< -0.50
```

means price must be **more than one-half ATR below VWMA** for the bearish base gate.

The inequalities are strict. Exactly `+0.50` or exactly `-0.50` does not satisfy the corresponding directional clause.

#### 2. Normalized 14-bar VWMA slope

For VWMA(20):

```text
(VWMA_20_slope__linreg_14 / VWMA_20) * 100
```

Component breakdown:

`VWMA_20_slope__linreg_14`

- The 14-bar linear-regression slope of VWMA(20).
- It measures the fitted rate of change of VWMA over that recent 14-bar window.

`/ VWMA_20`

- Divides the slope by the current VWMA level.
- This removes much of the raw price-level dependence.

`* 100`

- Expresses the normalized slope as percent of VWMA per bar.

Project thresholds:

```text
> +0.05% per bar
→ bullish slope gate passes

< -0.05% per bar
→ bearish slope gate passes
```

The interval from `-0.05%` through `+0.05%` is effectively the slope deadband for rule purposes. Exactly `+0.05%` and exactly `-0.05%` do not satisfy the directional clauses because the expressions use strict `>` and `<` comparisons.

Layman's translation:

> **VWMA itself must be rising or falling meaningfully enough; price being on one side of VWMA is not sufficient by itself.**

#### 3. VWMA-vs-SMA spread, normalized by ATR

For VWMA(20):

```text
(VWMA_20 - SMA_20) / ATR_14
```

Component breakdown:

`VWMA_20 - SMA_20`

- Positive means VWMA is above SMA.
- Negative means VWMA is below SMA.

`/ ATR_14`

- Measures that VWMA/SMA separation relative to current volatility.

Strong-state threshold:

```text
>= +0.15
→ sufficient bullish VWMA-vs-SMA separation

<= -0.15
→ sufficient bearish VWMA-vs-SMA separation
```

Layman's translation:

> **For a Strong state, volume weighting must move VWMA far enough away from the ordinary SMA to count as meaningful additional confirmation.**

Unlike the price-distance and slope clauses, the Strong spread boundary is inclusive: `+0.15` can satisfy the bullish spread-size clause and `-0.15` can satisfy the bearish spread-size clause.

#### 4. VWMA/SMA percentage-spread direction

For VWMA(20), the rule compares:

```text
VWMA_20 / SMA_20 - 1
```

with:

```text
lag(VWMA_20 / SMA_20 - 1, 1)
```

The first expression is the current signed VWMA/SMA percentage spread in fractional form. The `lag(..., 1)` expression is the same relationship one observation earlier.

Bullish comparison:

```text
current spread > prior spread
```

means the signed spread is **Rising**.

Bearish comparison:

```text
current spread < prior spread
```

means the signed spread is **Falling**.

Important: `Rising` does not automatically mean VWMA is above SMA, and `Falling` does not automatically mean VWMA is below SMA.

Examples:

```text
-0.45% → -0.30%
```

is **Spread Rising** because `-0.30 > -0.45`, even though VWMA remains below SMA.

```text
+0.40% → +0.25%
```

is **Spread Falling** because `+0.25 < +0.40`, even though VWMA remains above SMA.

This clause therefore asks whether the VWMA/SMA relationship is moving **farther in the confirming direction**, not merely which side of zero it is on.

---

### Strong Buy (+2)

VWMA(20) rule:

```json
"strong_buy": "(Close - VWMA_20) / ATR_14 > 0.50 and (VWMA_20_slope__linreg_14 / VWMA_20) * 100 > 0.05 and (VWMA_20 - SMA_20) / ATR_14 >= 0.15 and (VWMA_20 / SMA_20 - 1) > lag(VWMA_20 / SMA_20 - 1, 1)"
```

#### Literal component breakdown

`(Close - VWMA_20) / ATR_14 > 0.50`

- Price is more than `0.50 ATR(14)` above VWMA(20).
- Layman's translation: **Price is meaningfully above the volume-weighted trend reference.**

`(VWMA_20_slope__linreg_14 / VWMA_20) * 100 > 0.05`

- The normalized 14-bar VWMA slope is greater than `+0.05%` per bar.
- Layman's translation: **VWMA itself is meaningfully rising.**

`(VWMA_20 - SMA_20) / ATR_14 >= 0.15`

- VWMA(20) is at least `0.15 ATR(14)` above SMA(20).
- Layman's translation: **Volume weighting has lifted VWMA meaningfully above the ordinary SMA.**

`(VWMA_20 / SMA_20 - 1) > lag(VWMA_20 / SMA_20 - 1, 1)`

- The current signed percentage spread is greater than yesterday's spread.
- Layman's translation: **VWMA's relative position versus SMA is still moving in the bullish direction.**

Because all four clauses use `and`, **every clause must be true**.

#### Literal summary

Meaningful price-above-VWMA distance **AND** meaningfully rising VWMA **AND** VWMA sufficiently above SMA **AND** VWMA/SMA spread rising.

#### Plain-English version

> **Price is convincingly above a rising VWMA, and the volume-weighted average is both meaningfully above SMA and continuing to strengthen relative to SMA.**

#### Interpretation

Strong Buy is the ordinary bullish VWMA state **plus both Strong-confirmation clauses**. It does not mean the next price move is guaranteed to be higher.

---

### Buy (+1)

VWMA(20) rule:

```json
"buy": "(Close - VWMA_20) / ATR_14 > 0.50 and (VWMA_20_slope__linreg_14 / VWMA_20) * 100 > 0.05 and ((VWMA_20 - SMA_20) / ATR_14 < 0.15 or (VWMA_20 / SMA_20 - 1) <= lag(VWMA_20 / SMA_20 - 1, 1))"
```

#### Literal component breakdown

The first two clauses are the same bullish base gates as Strong Buy:

`(Close - VWMA_20) / ATR_14 > 0.50`

- Price is meaningfully above VWMA.

`(VWMA_20_slope__linreg_14 / VWMA_20) * 100 > 0.05`

- VWMA is meaningfully rising.

The final parenthetical expression is what keeps ordinary Buy separate from Strong Buy:

```text
(VWMA_20 - SMA_20) / ATR_14 < 0.15
or
(VWMA_20 / SMA_20 - 1) <= lag(VWMA_20 / SMA_20 - 1, 1)
```

First path:

`(VWMA_20 - SMA_20) / ATR_14 < 0.15`

- VWMA is **not** at least `+0.15 ATR` above SMA.
- This includes cases where VWMA is only slightly above SMA, equal to SMA, or below SMA.
- Layman's translation: **The VWMA-vs-SMA separation is not large enough for Strong Buy.**

Second path:

`(VWMA_20 / SMA_20 - 1) <= lag(VWMA_20 / SMA_20 - 1, 1)`

- The current signed percentage spread is not greater than the prior spread.
- The spread is flat or falling rather than rising.
- Layman's translation: **The VWMA-vs-SMA relationship is not strengthening in the bullish direction.**

Because these two confirmation-failure clauses use `or`, **either one is enough** to keep the observation at Buy rather than Strong Buy.

That captures three ordinary-Buy cases:

1. spread size is too small, even if the spread is rising;
2. spread size is large enough, but the spread is not rising;
3. both Strong-confirmation conditions fail.

#### Literal summary

Qualified bullish Price-vs-VWMA state **AND** qualified bullish VWMA slope **AND** at least one Strong-Buy confirmation requirement is absent.

#### Plain-English version

> **The VWMA trend is bullish, but the VWMA-vs-SMA relationship does not satisfy the full Strong-Buy confirmation test.**

#### Why the `or` clause exists

Without the final `or` block, ordinary Buy and Strong Buy could describe the same base bullish observations. The `or` block explicitly assigns ordinary Buy to bullish observations that **fail at least one** of the two Strong-Buy confirmation clauses.

This makes the two bullish states mechanically separate:

```text
Strong Buy
= bullish base + spread large enough + spread rising

Buy
= bullish base + not(full Strong confirmation)
```

---

### Neutral (0)

VWMA rulebook entry:

```json
"neutral": ""
```

Neutral is therefore not a separately coded fixed zone. It is the **mature fallback state** when none of the four directional expressions matches.

Neutral can occur for several reasons:

- price distance does not exceed the period's bullish or bearish `k` threshold;
- normalized slope remains inside the `±0.05%/bar` deadband;
- price and VWMA slope point in conflicting directions;
- price is exactly on a strict directional boundary such as `+0.50 ATR` for VWMA(20);
- slope is exactly `+0.05%/bar` or `-0.05%/bar`, which does not satisfy the strict directional comparison.

Examples for VWMA(20):

```text
Price distance = +0.80 ATR
Slope          = +0.02%/bar
→ Neutral
```

Price passes the bullish distance gate, but slope does not.

```text
Price distance = +0.20 ATR
Slope          = +0.09%/bar
→ Neutral
```

Slope passes, but price is not far enough above VWMA.

```text
Price distance = +0.70 ATR
Slope          = -0.08%/bar
→ Neutral
```

Price and VWMA direction disagree.

#### Plain-English version

> **The app does not currently have enough qualified agreement between Price-vs-VWMA position and VWMA direction to call the state bullish or bearish.**

Neutral does **not** mean that price equals VWMA or that VWMA is perfectly flat.

---

### Sell (-1)

VWMA(20) rule:

```json
"sell": "(Close - VWMA_20) / ATR_14 < -0.50 and (VWMA_20_slope__linreg_14 / VWMA_20) * 100 < -0.05 and ((VWMA_20 - SMA_20) / ATR_14 > -0.15 or (VWMA_20 / SMA_20 - 1) >= lag(VWMA_20 / SMA_20 - 1, 1))"
```

#### Literal component breakdown

`(Close - VWMA_20) / ATR_14 < -0.50`

- Price is more than `0.50 ATR(14)` below VWMA(20).
- Layman's translation: **Price is meaningfully below the volume-weighted trend reference.**

`(VWMA_20_slope__linreg_14 / VWMA_20) * 100 < -0.05`

- The normalized VWMA slope is less than `-0.05%` per bar.
- Layman's translation: **VWMA itself is meaningfully falling.**

The final parenthetical expression separates Sell from Strong Sell:

```text
(VWMA_20 - SMA_20) / ATR_14 > -0.15
or
(VWMA_20 / SMA_20 - 1) >= lag(VWMA_20 / SMA_20 - 1, 1)
```

First path:

`(VWMA_20 - SMA_20) / ATR_14 > -0.15`

- VWMA is **not** at least `0.15 ATR` below SMA.
- Layman's translation: **The VWMA-vs-SMA separation is not bearish enough for Strong Sell.**

Second path:

`(VWMA_20 / SMA_20 - 1) >= lag(VWMA_20 / SMA_20 - 1, 1)`

- The current signed percentage spread is not less than the prior spread.
- The spread is flat or rising rather than falling.
- Layman's translation: **The VWMA-vs-SMA relationship is not strengthening in the bearish direction.**

Because these two confirmation-failure clauses use `or`, **either one is enough** to keep the observation at Sell rather than Strong Sell.

#### Literal summary

Qualified bearish Price-vs-VWMA state **AND** qualified bearish VWMA slope **AND** at least one Strong-Sell confirmation requirement is absent.

#### Plain-English version

> **The VWMA trend is bearish, but the VWMA-vs-SMA relationship does not satisfy the full Strong-Sell confirmation test.**

#### Why the `or` clause exists

The structure is the bearish mirror of Buy:

```text
Strong Sell
= bearish base + spread large enough in the bearish direction + spread falling

Sell
= bearish base + not(full Strong confirmation)
```

---

### Strong Sell (-2)

VWMA(20) rule:

```json
"strong_sell": "(Close - VWMA_20) / ATR_14 < -0.50 and (VWMA_20_slope__linreg_14 / VWMA_20) * 100 < -0.05 and (VWMA_20 - SMA_20) / ATR_14 <= -0.15 and (VWMA_20 / SMA_20 - 1) < lag(VWMA_20 / SMA_20 - 1, 1)"
```

#### Literal component breakdown

`(Close - VWMA_20) / ATR_14 < -0.50`

- Price is meaningfully below VWMA.

`(VWMA_20_slope__linreg_14 / VWMA_20) * 100 < -0.05`

- VWMA is meaningfully falling.

`(VWMA_20 - SMA_20) / ATR_14 <= -0.15`

- VWMA is at least `0.15 ATR` below SMA.
- Layman's translation: **Volume weighting has pulled VWMA meaningfully below the ordinary SMA.**

`(VWMA_20 / SMA_20 - 1) < lag(VWMA_20 / SMA_20 - 1, 1)`

- The current signed percentage spread is less than the prior spread.
- Layman's translation: **VWMA's relative position versus SMA is still moving farther in the bearish direction.**

Because all four clauses use `and`, **every clause must be true**.

#### Literal summary

Meaningful price-below-VWMA distance **AND** meaningfully falling VWMA **AND** VWMA sufficiently below SMA **AND** VWMA/SMA spread falling.

#### Plain-English version

> **Price is convincingly below a falling VWMA, and the volume-weighted average is both meaningfully below SMA and continuing to weaken relative to SMA.**

---

### Parameter mapping across VWMA(10), VWMA(20), and VWMA(50)

The expression structure above is identical across periods. Substitute the matching columns and `k` value:

| Component | VWMA(10) | VWMA(20) | VWMA(50) |
| --- | --- | --- | --- |
| VWMA column | `VWMA_10` | `VWMA_20` | `VWMA_50` |
| SMA confirmation column | `SMA_10` | `SMA_20` | `SMA_50` |
| Price-distance `k` | `0.25` | `0.50` | `1.00` |
| Slope threshold | `±0.05%/bar` | `±0.05%/bar` | `±0.05%/bar` |
| Strong spread threshold | `±0.15 ATR` | `±0.15 ATR` | `±0.15 ATR` |
| Slope lookback | 14 bars | 14 bars | 14 bars |

### Boundary behavior and mutual exclusivity

A few boundaries are worth documenting explicitly:

- Price-distance clauses use strict `>` / `<` comparisons.
- Slope clauses use strict `>` / `<` comparisons.
- Strong spread-size clauses use inclusive `>= +0.15` / `<= -0.15` comparisons.
- Strong Buy requires current spread **strictly greater** than prior spread.
- Strong Sell requires current spread **strictly less** than prior spread.
- Buy accepts a spread that is flat or falling through `<=`.
- Sell accepts a spread that is flat or rising through `>=`.

The ordinary Buy/Sell `or` clauses are the complement of the full Strong confirmation. This is what keeps the final five-state model mutually exclusive while allowing the same bullish or bearish base gate to feed either the ordinary or Strong state.

---

## Context and Hover fields
> See Also: "Interpreting the full VWMA readout together"
> For examples, see the "Worked Examples" section below.

---
The primary Signal is only one layer of the VWMA readout.
The hover exposes several additional fields that help explain **why the Signal exists** and **what today's individual session looks like**.

| Field | Main question | Score impact |
| --- | --- | --- |
| **Signal** | What qualified VWMA state applies now? | **Yes** |
| **Price vs. MA** | How far is price above/below VWMA in raw price and % terms? | Display of a relationship used by the score in ATR-normalized form |
| **VWMA vs SMA** | How far is VWMA above/below SMA, and is that signed relationship rising or falling? | Spread size/direction participates in **Strong** states |
| **1D Direction** | Did VWMA and SMA individually rise or fall since the prior observation? | **No — context only** |
| **Volume Activity** | How heavy/light is today's volume versus the matching-period average and recent 120-session distribution? | **No — context only** |
| **▲ / ▼ + blue/red value** | Is today's volume exceptionally high/low, and did price rise/fall? | **No — context only** |

### `VWMA vs SMA`

Example:

```text
VWMA vs SMA: -0.75 (-0.30%) | Spread Rising
```

`-0.75`

- Absolute spread: `VWMA - SMA`.
- VWMA is `$0.75` below SMA.

`-0.30%`

- Percentage spread: `(VWMA / SMA - 1) × 100`.
- VWMA is approximately `0.30%` below SMA.

`Spread Rising`

- Current signed VWMA/SMA percentage spread is greater than its prior value.
- It does **not** necessarily mean VWMA is above SMA.

Examples:

```text
-0.45% → -0.30%
→ Spread Rising
```

VWMA is still below SMA, but the disadvantage is narrowing.

```text
+0.20% → +0.35%
→ Spread Rising
```

VWMA is above SMA and the advantage is widening.

Likewise:

```text
+0.40% → +0.25%
→ Spread Falling
```

VWMA remains above SMA, but its advantage is narrowing.

```text
-0.25% → -0.42%
→ Spread Falling
```

VWMA is below SMA and its disadvantage is widening. This is the direction needed for Strong Sell when the other Strong-Sell clauses also pass.

### `1D Direction`

Example:

```text
1D Direction: VWMA Rising | SMA Rising
```

This compares each average with its own immediately prior value.

```text
Current VWMA > Prior VWMA
→ VWMA Rising

Current VWMA < Prior VWMA
→ VWMA Falling
```

The same logic applies to SMA.

This field is **context only**. It is not the same thing as the normalized 14-bar linear-regression slope used by the primary Signal.

Therefore, this combination is possible:

```text
14-bar normalized VWMA slope = positive
1D Direction                 = VWMA Falling
```

One down day can occur inside a broader rising 14-bar VWMA trend.

### `Volume Activity`

Example:

```text
Volume Activity: 0.56× 20D avg | 2nd pct
```

The two values answer different questions.

`0.56× 20D avg`

- Current volume divided by the matching-period average volume.
- For VWMA(20), the denominator is the 20-day average volume.

If current volume is `8.73M` shares:

```text
8.73M / 0.56
≈ 15.59M
```

So `0.56× 20D avg` means today's volume is about **56% of the recent 20-day average**.

The comparison period follows the VWMA period:

```text
VWMA(10) → current volume vs 10D average
VWMA(20) → current volume vs 20D average
VWMA(50) → current volume vs 50D average
```

`2nd pct`

- Current absolute volume percentile within the trailing 120 sessions.
- It describes how unusual today's volume is relative to recent history.

With roughly 120 sessions:

```text
120 × 0.02 = 2.4
```

A practical translation is:

> **Out of roughly 120 trading sessions, only about 1–2 had volume this low or lower, while roughly 117–118 had greater volume.**

This is an intuitive approximation; ties and percentile ranking mechanics mean the exact count need not be identical in every case.

A high-volume example:

```text
Volume Activity: 2.39× 20D avg | 100th pct
```

means today's volume is about `239%` of the 20-day average and sits at the very top of the recent 120-session volume distribution.

### Extreme-volume marker: arrow = volume, color = price direction

The marker rule is deliberately simple:

```text
Volume percentile >= 95
→ ▲

Volume percentile <= 5
→ ▼
```

The **arrow describes volume extremity**.

The **font color describes price direction versus the prior Close**.

| Display | Meaning |
| --- | --- |
| **Blue ▲** | Exceptionally high volume + Price Up |
| **Red ▲** | Exceptionally high volume + Price Down |
| **Blue ▼** | Exceptionally low volume + Price Up |
| **Red ▼** | Exceptionally low volume + Price Down |

If price is unchanged, the app does not force the observation into an up/down directional event.

Examples:

```text
Blue ▲
```

> **Price rose on exceptionally high volume.**

```text
Red ▲
```

> **Price fell on exceptionally high volume.**

```text
Blue ▼
```

> **Price rose on exceptionally low volume.**

```text
Red ▼
```

> **Price fell on exceptionally low volume.**

The arrow/color context does **not** change the primary VWMA score.


---
## Worked examples
> See Also: "Interpreting the full VWMA readout together"
> For more details, see the "Context and Hover Fields" section

### Example 1 — VWMA(20) Buy, not Strong Buy

Suppose:

```text
Close                      = 211.34
VWMA(20)                   = 207.10
SMA(20)                    = 207.85
ATR(14)                    = 7.50
Normalized VWMA slope      = +0.09%/bar
Prior VWMA/SMA % spread    = -0.44%
Current VWMA/SMA % spread  = -0.36%
```

Price-distance test:

```text
(211.34 - 207.10) / 7.50
= +0.565 ATR
```

VWMA(20) requires `> +0.50 ATR`, so the bullish price-distance gate passes.

Slope test:

```text
+0.09% > +0.05%
```

PASS.

The observation therefore qualifies for at least **Buy**.

Strong spread-size test:

```text
(207.10 - 207.85) / 7.50
= -0.10 ATR
```

Strong Buy requires `>= +0.15 ATR`, so this fails.

The percentage spread did improve from `-0.44%` to `-0.36%`, so it is Rising, but the spread-size clause is still insufficient.

Result:

```text
Signal: Buy
VWMA vs SMA: -0.75 (-0.36%) | Spread Rising
```

Beginner translation:

> **Price is meaningfully above a rising VWMA, but VWMA is still below SMA and therefore lacks the required Strong-Buy reinforcement.**

### Example 2 — VWMA(20) Strong Buy

Suppose:

```text
Close                      = 211.08
VWMA(20)                   = 207.00
SMA(20)                    = 205.60
ATR(14)                    = 8.00
Normalized VWMA slope      = +0.11%/bar
Prior VWMA/SMA % spread    = +0.55%
Current VWMA/SMA % spread  = +0.68%
```

Price distance:

```text
(211.08 - 207.00) / 8.00
= +0.51 ATR
```

VWMA(20) requires `> +0.50 ATR`, so the bullish price-distance gate passes.

Slope:

```text
+0.11% > +0.05%
```

PASS.

Strong spread-size:

```text
(207.00 - 205.60) / 8.00
= +0.175 ATR
```

PASS because `+0.175 >= +0.15`.

Spread direction:

```text
+0.55% → +0.68%
```

PASS because the signed spread is Rising.

Result: **Strong Buy**.

### Example 3 — Neutral because only one base gate passes

Suppose VWMA(20) has:

```text
Price Distance = +0.80 ATR
VWMA slope     = +0.02%/bar
```

Price distance passes the bullish gate, but slope does not exceed `+0.05%/bar`.

Result: **Neutral**.

This illustrates one of the most important rules in the model:

> **Price being above VWMA by itself is not a Buy signal.**

### Example 4 — Strong Sell

Suppose VWMA(50) has:

```text
Close                      = 180
VWMA(50)                   = 190
SMA(50)                    = 192
ATR(14)                    = 8
Normalized VWMA slope      = -0.10%/bar
Prior VWMA/SMA % spread    = -0.72%
Current VWMA/SMA % spread  = -1.04%
```

Price distance:

```text
(180 - 190) / 8
= -1.25 ATR
```

VWMA(50) requires `< -1.00 ATR`, so PASS.

Slope:

```text
-0.10% < -0.05%
```

PASS.

Strong spread-size:

```text
(190 - 192) / 8
= -0.25 ATR
```

PASS because `-0.25 <= -0.15`.

Spread direction:

```text
-0.72% → -1.04%
```

PASS because the signed spread is Falling.

Result: **Strong Sell**.

### Example 5 — exceptionally low-volume up day

Suppose a VWMA(20) hover shows:

```text
Vol: 8.73M
Volume Activity: 0.56× 20D avg | 2nd pct | Low ▼ | Price Up
```

The implied 20-day average volume is approximately:

```text
8.73M / 0.56
≈ 15.59M
```

The `2nd pct` reading means volume is near the bottom of the trailing 120-session distribution. A useful approximation is that only about `1–2` sessions had volume this low or lower while roughly `117–118` had greater volume.

The **blue ▼** tells you that price rose, but on exceptionally light volume.

This context does not alter the primary VWMA Signal.

---

## Industry-standard foundation versus project calibration

### Conventional foundation

The underlying VWMA construction is conventional:

```text
VWMA = Σ(Price × Volume) / Σ(Volume)
```

Its basic purpose is to weight higher-volume observations more heavily than lower-volume observations.

### Project-specific calibration

The five-state signal framework is a project design rather than a universal VWMA taxonomy. Project-specific choices include:

- configured periods `10 / 20 / 50`;
- ATR-normalized Price-vs-VWMA distance;
- period-specific `k` values `0.25 / 0.50 / 1.00`;
- normalized 14-bar linear-regression VWMA slope;
- `±0.05%/bar` slope thresholds;
- matching-period VWMA-vs-SMA reinforcement;
- `±0.15 ATR` Strong spread-size threshold;
- one-observation VWMA/SMA spread direction as a Strong confirmation requirement;
- five-state `Strong Buy / Buy / Neutral / Sell / Strong Sell` classification;
- trailing 120-session volume percentile;
- `95th / 5th percentile` extreme-volume marker.

The design goal is to make the VWMA state human-auditable:

> **A user should be able to reconstruct whether the observation qualified because of Price-vs-VWMA distance, VWMA slope, VWMA-vs-SMA reinforcement, or the absence of one of those clauses.**

---

## Diagnostic and design decisions from the VWMA audit

Several choices were tested or explicitly rejected during the VWMA workstream.

### Adopted

- ATR-normalized Price-vs-VWMA distance rather than raw dollar distance;
- period-specific 14-bar normalized VWMA slope rather than the legacy shared/raw slope alias;
- matching-period VWMA-vs-SMA relationship as Strong-state confirmation;
- current-day volume anomaly as context only, not as a scoring gate;
- simple `95th / 5th` percentile extreme-volume marker with price-direction color.

### Rejected / not adopted

**VWMA/SMA crossover event:** rejected as a separate arrow/event feature after bounded diagnostics showed the crossover was selective but did not provide sufficiently consistent forward behavior versus baseline to justify another event layer.

**Additional low-volume materiality filters:** not adopted for the initial version. The extreme-volume marker deliberately remains simple: `>=95th` or `<=5th` percentile, with no minimum price-move threshold.

### Extreme-volume diagnostic context

In the bounded diagnostic sample, exceptionally high-volume observations were associated with much larger typical same-day price moves than exceptionally low-volume observations. The low-volume observations were much quieter on average. That supported treating high/low volume as useful context while keeping it outside the primary VWMA score.

The final decision was therefore:

> **Use extreme-volume markers to explain the character of the current session, not to rewrite the VWMA trend score.**

---

## Strengths & Weakness
### Strengths

VWMA is particularly useful in this project for:

- incorporating trading participation directly into a moving-average calculation;
- distinguishing a volume-weighted price trend from an equal-weighted SMA trend;
- requiring price and VWMA direction to agree before assigning Buy/Sell;
- normalizing price displacement through ATR so thresholds scale with volatility;
- normalizing slope so differently priced securities are more comparable;
- using the matching SMA as an intuitive benchmark for whether volume weighting is materially changing the trend reference;
- reserving Strong states for additional VWMA-vs-SMA confirmation rather than merely larger Price-vs-VWMA distance;
- exposing current-day volume context without forcing raw volume directly into the primary score;
- identifying exceptionally high- or low-volume sessions visually.

---

### Limitations

**VWMA is still a lagging moving average**
- VWMA is derived from historical price and volume. A qualified trend can weaken or reverse after the Signal is assigned.

**Volume weighting does not automatically make a trend correct**
- Heavy trading can accompany buying, selling, news shocks, capitulation, earnings reactions, or rebalancing. VWMA tells you **where heavier trading has pulled the average**; it does not independently explain why that trading occurred.

**Price above/below VWMA is not sufficient**
- The project intentionally requires normalized VWMA slope to agree.

```text
Price > VWMA
```

- does not automatically mean Buy, and:

```text
Price < VWMA
```

- does not automatically mean Sell.


**'`Spread Rising`' is not automatically bullish**
- A negative spread can rise while remaining negative, and a positive spread can fall while remaining positive. Always read the signed spread value and the direction label together.

**'`1D Direction`' can disagree with the primary slope**
- That is expected because `1D Direction` measures one observation while the Signal uses a 14-bar linear-regression slope.

**Volume percentile is contextual**
- A `100th pct` volume observation is not automatically bullish. A `2nd pct` observation is not automatically bearish. The arrow describes volume extremity; the color describes daily price direction.

**'Strong' does not mean certain**
- Strong Buy and Strong Sell mean **more qualifying VWMA confirmation under the project rules**, not certainty about the next price move.

---

## Beginner's checklist

When reading a VWMA cell, ask:

| Step | Question |
| --- | --- |
| **1** | What does the primary `Signal` say? |
| **2** | How far is Price above or below VWMA? |
| **3** | Is the normalized 14-bar VWMA slope sufficiently positive or negative? |
| **4** | What does `VWMA vs SMA` show — above or below, by how much, and Rising/Falling? |
| **5** | If the Signal is only Buy/Sell rather than Strong, which Strong-confirmation clause is missing? |
| **6** | What does `1D Direction` say about today's VWMA and SMA movement? |
| **7** | Is today's volume ordinary, unusually heavy, or unusually light? |
| **8** | If an ▲ or ▼ appears, what does its color say about today's price direction? |
| **9** | Do the broader VWMA state and the latest session's volume/price context reinforce one another or describe different things? |

The shortest useful summary is:

> **Signal = qualified VWMA trend state.**
> **VWMA vs SMA = Strong-state reinforcement and visible volume-weighting effect.**
> **1D Direction = latest one-day movement of VWMA and SMA.**
> **Volume Activity = current participation context.**
> **Arrow/color = extreme-volume + daily-price-direction context.**

---

## Initial audit note

**Semantic type:** Directional / trend-confirmation moving average with VWMA-vs-SMA reinforcement and separate current-volume context.

**Primary philosophy:** Require meaningful Price-vs-VWMA separation and directional VWMA slope before assigning Buy/Sell; reserve Strong states for additional matching-period VWMA-vs-SMA confirmation.

**Numeric identity:**

```text
VWMA(N) =
Σ(Close × Volume)
-----------------
Σ(Volume)
```

Configured periods:

```text
10 / 20 / 50
```

**Primary scoring vocabulary:**

```text
+2  Strong Buy
+1  Buy
 0  Neutral
-1  Sell
-2  Strong Sell
```

**Price-distance normalization:**

```text
DistanceATR =
Close - VWMA(N)
---------------
    ATR(14)
```

Thresholds:

```text
VWMA(10): > +0.25 / < -0.25
VWMA(20): > +0.50 / < -0.50
VWMA(50): > +1.00 / < -1.00
```

**Normalized slope:**

```text
SlopePctPerBar =
VWMA_N_slope__linreg_14
----------------------- × 100
        VWMA_N
```

Thresholds:

```text
> +0.05%/bar → bullish slope gate
< -0.05%/bar → bearish slope gate
```

**Strong-state VWMA/SMA reinforcement:**

```text
SpreadATR =
VWMA(N) - SMA(N)
----------------
     ATR(14)
```

```text
Strong Buy component:
SpreadATR >= +0.15
and current VWMA/SMA % spread > prior spread

Strong Sell component:
SpreadATR <= -0.15
and current VWMA/SMA % spread < prior spread
```

**Primary state model:** Current-state classification. No VWMA/SMA crossover event is required for the five-state score.

**Volume Activity:** Context only.

```text
Current Volume / matching-period average Volume
+
Current Volume percentile within trailing 120 sessions
```

**Extreme-volume display:**

```text
>= 95th percentile → ▲
<= 5th percentile  → ▼

Blue → Price Up
Red  → Price Down
```

No score effect.

**Display-versus-scoring distinction:**

```text
raw VWMA number
→ current VWMA value

heatmap background color
→ primary five-state Signal

Price vs. MA
→ visible raw Price-vs-VWMA relationship
  (score uses ATR-normalized form)

VWMA vs SMA
→ visible matching-period VWMA/SMA relationship;
  spread size/direction participates in Strong states

1D Direction
→ one-day VWMA/SMA movement; context only

Volume Activity
→ current participation context only

blue/red ▲ / ▼
→ extreme-volume + daily-price-direction context only
```

**Verification status:** The adopted VWMA implementation completed five-state classification verification, maturity/warmup verification, production-path context verification, VWMA/SMA crossover diagnostic review, extreme-volume diagnostic review, adapter/UI structural verification, and manual acceptance across the Rolling Signal Heatmap, SCD Multiple Indicators, and SCD Single Indicator views.

---

## References

### Project references

- `src/config/master_rules_normalized.json` — VWMA five-state scoring expressions, thresholds, parameters, notes, definitions, and configured periods.
- `src/calculations/indicator_preprocessor.py` — VWMA numeric computation and supporting moving-average primitives.
- `src/calculations/signal_classifier.py` — five-state classification and VWMA maturity/missing handling.
- `src/calculations/technical.py` — normalized VWMA slope support, VWMA/SMA context, rolling transport, volume percentile, and extreme-volume event truth.
- `src/ui/rolling_heatmap_adapter.py` — VWMA hover construction, `VWMA vs SMA`, `1D Direction`, `Volume Activity`, extreme-volume text/color overlay, and Rolling Signal Heatmap hover presentation.
- `streamlit_app.py` — SCD Single / Multiple consumer presentation and shared Price/Volume hover context.


---
## My Notes
VWMA is a **trend-following moving average** that weights price by volume.


**Purpose:** Smooth price data while giving **more weight to periods with heavier volume**, helping reveal the “true” trend driven by meaningful participation.
- IOW, the 'line' reflects where the market actually traded with conviction


**Use when:** You want **trend confirmation with volume context**, especially to distinguish between weak moves (low volume) and strong, conviction-backed moves (high volume).

- Particularly useful on intraday and daily charts when you want to separate strong moves from weak ones (IOW, identifying institutional participation).

**Key Concept:**
VWMA assigns greater weight to prices that occur on higher volume. This helps filter out noise and emphasizes moves where institutional activity is more likely present.

**Calculation:**

$$\large{VWMA=\frac{\sum (Price \times Volume)}{\sum Volume}}$$

- Typically uses closing price, though some traders use typical price \((high + low + close)/3\)
- Calculated over a rolling lookback period (e.g., 20 bars)

---
**How to Read:**
- **Price above VWMA:** Bullish bias; volume is supporting higher prices.
- **Price below VWMA:** Bearish bias; selling pressure is more convincing.
- **VWMA rising:** Buyers are in control.
- **VWMA falling:** Sellers are in control.
- **Price crossing VWMA:** Often used as a trend shift or entry/exit trigger. [ninjatrader](https://ninjatrader.com/futures/blogs/what-is-a-volume-weighted-moving-average-vwma/)
- **VWMA as support/resistance:** In uptrends, price may pull back to VWMA and bounce; in downtrends, it may reject from VWMA.


---
**Signals & Interpretation:**

- **Trend Direction:**
  - Price above VWMA = bullish bias (volume supports higher prices)
  - Price below VWMA = bearish bias

- **Trend Strength:**
  - Steep upward slope = strong buying pressure
  - Flat VWMA = consolidation or lack of conviction
  - Steep downward slope = strong selling pressure

- **Crossovers (with price or other MAs):**
  - Price crossing above VWMA = potential bullish shift
  - Price crossing below VWMA = potential bearish shift
  - VWMA above SMA = volume confirms strength (bullish)
  - VWMA below SMA = weak participation (bearish)

- **Volume Confirmation:**
  - If VWMA rises faster than SMA → strong volume-backed move
  - If price rises but VWMA lags → weak rally (low volume)

- **Support/Resistance:**
  - VWMA often acts as dynamic support in uptrends
  - Acts as resistance in downtrends

**Optimal Conditions:**
- Works best in **trending markets** where volume expands in the direction of the trend.

VWMA tends to work best in **trending markets with meaningful volume expansion**, not in dead, choppy tape. It is useful on intraday and daily charts when you want to separate strong moves from weak ones.

**Limitations:**
- Less effective in **low-volume or choppy markets**
- Can lag like all moving averages
- Volume spikes (news events) can distort the line temporarily
- Not useful for overbought/oversold conditions (not an oscillator)

**Complexity Level:** Beginner–Intermediate

**Other indicators to use w/**:

- **RSI or MFI:** Add overbought/oversold context VWMA lacks
- **MACD:** Confirms momentum alongside VWMA trend
- **Volume Profile / OBV:** Deeper volume confirmation
- **Bollinger Bands:** Helps identify volatility around VWMA
- **ADX:** Confirms whether a trend is strong enough to trust VWMA signals

**Best for:**

- Identifying **volume-confirmed trends**
- Filtering out weak breakouts
- Spotting institutional accumulation/distribution
- Dynamic support/resistance in trending markets

**Strengths:**

- Incorporates volume, giving it an edge over SMA/EMA
- Helps validate whether price moves have conviction
- Simple to interpret visually
- Adapts well across timeframes

**Limitations:**

- Still a lagging indicator
- Can be misleading during irregular volume spikes
- Provides no direct momentum or exhaustion signals

---
**Parameter Settings:**

- **Short-term (1–15 days): VWMA(10)**
  - Fast and responsive; useful for day trading and short swings

- **Intermediate-term (15–50 days): VWMA(20)**
  - Balanced; commonly used for swing trading and trend tracking

- **Long-term (50+ days): VWMA(50)**
  - Smooth and stable; ideal for identifying primary trends

---
**Practical trading framework**

**1. Trend filter**
- Trade long when price holds above a rising VWMA.
- Trade short when price stays below a falling VWMA.

**2. Breakout confirmation**
- A breakout is more credible if it expands above VWMA on strong volume.
- If price breaks out but VWMA barely moves, the move may lack sponsorship.

**3. Pullback setup**
- In an uptrend, use VWMA as a pullback zone.
- In a downtrend, use VWMA as a rally-fade zone.

**4. Crossover logic**
- Faster VWMA crossing above a slower SMA can signal improving participation.
- A VWMA/SMA crossover system is often used for swing trading.
