

|Bucket|What it answers|Indicators|
|---|---|---|
|**Momentum / oscillators**|Overbought/oversold, turning points|RSI, Stochastic, MACD, ROC, **Williams %R**, CCI, UO, DPO|
|**Trend direction**|Which way, and is there even a trend?|SMA, EMA, HMA|
|**Trend strength**|Is the trend strong enough to trust?|ADX|
|**Volatility**|How big are the swings, right now?|Bollinger Bands, ATR|
|**Volume / money flow**|Is real participation behind the move?|CMF, MFI, VWMA|
|**Sentiment / power balance**|Who's winning, bulls or bears?|Bull Bear Power|

> Williams %R is normally interpreted as a bounded oscillator from `0` to `-100`. It reflects where the close sits relative to the highest high / lowest low over the lookback period. 


## Summary: WILLR(14) 'Signals'

| Signal        | Literal trigger                                                                                                                                       | Layman’s Translation                                                                                                                                                              | Rule Logic                                                                                                                                                                                                                 | Bottom-line                                                                                                   |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `strong_buy`  | `WILLR < -90` now, and WILLR was below `-90` in at least 3 of the last 4 observations                                                                 | Price is closing extremely close to the bottom of its recent 14-period range, and this has been happening repeatedly rather than for just one period.                             | The current reading must still be below `-90`, and at least 3 of the last 4 readings must have been below `-90`.                                                                                                           | **Price has been repeatedly closing near the bottom of its recent range.**                                    |
| `buy`         | `WILLR < -97` **or** WILLR was below `-90` for both of the last 2 observations, provided the 3-of-4 Strong Buy condition has not already been reached | Price is extremely close to the bottom of its recent range. Either today's reading is exceptionally low, or price has stayed very low for two observations in a row.              | Buy has two paths: one exceptionally deep reading below `-97`, or two consecutive readings below `-90`. If 3 of the last 4 readings are already below `-90`, the signal advances to Strong Buy.                            | **Price is extremely low in its recent range, but the stronger persistence condition has not yet matured.**   |
| `neutral`     | `-90 <= WILLR < -7`, **or** `-97 <= WILLR < -90` without enough persistence for Buy or Strong Buy                                                     | Price is either between the two active extreme zones, or it has only recently entered the very-low zone and has not yet become extreme or persistent enough to earn a Buy signal. | Ordinary middle-range readings are Neutral. A reading between `-97` and `-90` also remains Neutral if it has not been below `-90` for 2 consecutive observations and has not been below `-90` in at least 3 of the last 4. | **Price is either in the middle of its recent range or only beginning to look unusually low.**                |
| `sell`        | `WILLR >= -7`                                                                                                                                         | Price is closing extremely close to the top of its recent 14-period range.                                                                                                        | A current reading at `-7` or closer to `0` activates Sell.                                                                                                                                                                 | **Price is trading very near the top of its recent range.**                                                   |
| `strong_sell` | `WILLR >= -5` and WILLR fell from the prior observation                                                                                               | Price is extremely close to the top of its recent range, but the indicator has just started moving lower.                                                                         | The reading must first be at least `-5`, then the current WILLR value must be lower than the immediately preceding value.                                                                                                  | **Price is extremely high in its recent range and is showing an initial sign of moving away from that high.** |

---

## WILLR(14) — brief overview

Williams %R measures **where the current closing price sits within the recent high-low price range**.

For `WILLR(14)`:

```text
14 = the most recent 14 periods used to define the high-low range
```

In this project, the indicator uses daily market data, so a 14-period WILLR normally means the most recent **14 trading observations**, not 14 calendar days.

Williams %R normally runs from:

```text
0      = close is at or extremely near the highest point of the recent range

-50    = close is around the middle of the recent range

-100   = close is at or extremely near the lowest point of the recent range
```

The negative scale can feel backward at first.

The simplest way to remember it is:

```text
Closer to 0
= closer to the recent HIGH

Closer to -100
= closer to the recent LOW
```

So:

```text
WILLR = -5
```

means:

> **Price is closing extremely close to the top of its recent range.**

while:

```text
WILLR = -95
```

means:

> **Price is closing extremely close to the bottom of its recent range.**

A simplified conceptual formula is:

```text
Williams %R
=
-100 × (highest high − current close)
       ÷ (highest high − lowest low)
```

where the highest high and lowest low are taken from the selected lookback period.

You do not need to calculate the formula to interpret the indicator.

The main question is simply:

> **Where is today's closing price between the recent high and recent low?**

### Reading the negative scale

One useful way to make the scale more intuitive is to think about how far the close is from each end of the range.

For example:

|  WILLR | Simple range-position interpretation |
| -----: | ------------------------------------ |
|    `0` | At the recent high                   |
|   `-5` | Extremely close to the recent high   |
|  `-20` | Near the upper end of the range      |
|  `-50` | Around the middle                    |
|  `-80` | Near the lower end of the range      |
|  `-95` | Extremely close to the recent low    |
| `-100` | At the recent low                    |

Another way to think about a reading such as `-95`:

> The close is only about **5% of the high-low range above the recent low**.

Likewise, a reading of `-5` means:

> The close is only about **5% of the high-low range below the recent high**.

This is why a more-negative number such as `-95` means **lower in the range**, while a less-negative number such as `-5` means **higher in the range**.

### Value-added use

> Use WILLR(14) when you want to know whether price is currently sitting unusually close to the top or bottom of its recent trading range — and, particularly on the Buy side, whether that extremely low position has persisted.

Price alone tells you:

> **What does the stock cost?**

Williams %R adds a different question:

> **Where is that closing price compared with the stock's own recent high and low?**

For example, a `$100` stock price by itself does not tell you whether the stock is currently near the top or bottom of its recent range.

Williams %R does.

`WILLR(14)` is the project's balanced / primary Williams %R setting. It is less reactive than `WILLR(5)` and faster than `WILLR(20)`.

### Use with

Williams %R is most useful when interpreted with trend, momentum, participation, and important price levels.

* **EMA or SMA** — to determine whether a very-low or very-high WILLR reading is occurring with or against the prevailing trend.
* **ADX** — to identify whether a strong trend may allow WILLR to remain near an extreme for an extended period.
* **MACD or ROC** — to check whether broader price momentum agrees with or contradicts the Williams %R extreme.
* **RSI or STOCH** — to see whether another bounded oscillator also considers price stretched.
* **MFI, CMF, OBV, or Volume** — to add participation / money-flow context.
* **Support and resistance** — an extreme WILLR reading near an important price level can be more informative than the same reading in isolation.

### Important distinction

The project's WILLR(14) rule set uses a **contrarian extreme-plus-persistence model**.

A low WILLR reading does not automatically mean:

```text
Buy
```

and an extremely low reading does not mean:

```text
The bottom is definitely in.
```

Instead, the Buy-side rules ask two questions:

```text
1. How extreme is the current reading?

2. Has price repeatedly remained this close
   to the bottom of its recent range?
```

The progression is:

```text
A first reading between -97 and -90
→ Neutral

One exceptionally deep reading below -97
→ Buy immediately

Two consecutive readings below -90
→ Buy

At least 3 of the last 4 readings below -90,
while the current reading is also below -90
→ Strong Buy
```

So the rule set distinguishes between:

```text
Severity
= how close price is to the absolute bottom of the recent range

Persistence
= how repeatedly price has remained near that bottom
```

The Sell side works differently:

```text
WILLR >= -7
→ Sell

WILLR >= -5
+ WILLR has moved lower from the prior observation
→ Strong Sell
```

Here, Strong Sell is not based on a multi-period persistence count.

Instead, it requires:

1. an exceptionally high position in the recent range; and
2. an initial move away from that high.

---

## WILLR(14) Rule Translation

### Strong buy

```json
"strong_buy": "WILLR_14 < -90 and count_below(WILLR_14, -90, 4) >= 3"
```

#### Literal component breakdown

`WILLR_14 < -90`

* The current Williams %R reading is below `-90`.
* Price is closing within the lowest portion of its recent 14-period high-low range.
* Layman’s translation: **price is closing extremely close to the bottom of its recent range.**

`count_below(WILLR_14, -90, 4) >= 3`

* Look at the most recent 4 WILLR observations.
* At least 3 of those 4 readings must be below `-90`.
* Layman’s translation: **price has been closing extremely close to the bottom of its recent range repeatedly — not just for one isolated observation.**

`... < -90 and count_below(...) >= 3`

* Both conditions must be true.
* The current reading must still be below `-90`.
* The recent 4-observation history must contain at least 3 readings below `-90`.
* Layman’s translation: **price is still extremely low in its recent range, and that extreme-low condition has persisted.**

#### Literal summary

The current WILLR reading is below `-90`, and at least 3 of the last 4 WILLR readings were below `-90`.

#### Plain-English version

Price is closing extremely close to the bottom of its 14-period range, and it has spent most of the last four observations near that bottom.

#### Interpretation

This is a **persistent extreme-low contrarian condition**.

The signal requires two layers:

1. price is still extremely close to the bottom of its recent range **now**;
2. that very-low condition has occurred in at least 3 of the last 4 observations.

For example:

```text
-92 → -94 → -88 → -93
```

Three of those four readings are below `-90`, and the latest reading is also below `-90`.

→ **Strong Buy**

The important idea is **persistence**:

> A single very-low reading normally does not produce Strong Buy. Price must repeatedly close near the bottom of its recent range.

#### Notes / confidence

* `< -90` means price is extremely close to the bottom of the 14-period range.
* `3 of the last 4` allows one temporary interruption without losing the persistence signal.
* Strong Buy does **not** mean price has definitely reached its bottom.
* Price can remain near the bottom of its recent range during a prolonged decline.
* The rule should therefore be read as **“persistent extreme-low condition”**, not “guaranteed rebound.”

---

### Buy

```json
"buy": "(WILLR_14 < -97 or count_below(WILLR_14, -90, 2) >= 2) and count_below(WILLR_14, -90, 4) < 3"
```

#### Literal component breakdown

`WILLR_14 < -97`

* The current Williams %R reading is below `-97`.
* Price is closing almost at the absolute bottom of its recent 14-period range.
* This condition can trigger Buy immediately.
* Layman’s translation: **today's closing price is exceptionally close to the lowest point of its recent range.**

`count_below(WILLR_14, -90, 2) >= 2`

* Look at the most recent 2 WILLR observations.
* Both must be below `-90`.
* Layman’s translation: **price has closed extremely close to the bottom of its recent range for two observations in a row.**

`WILLR_14 < -97 or count_below(WILLR_14, -90, 2) >= 2`

* Only one of these two paths needs to be true.
* Buy can therefore happen through **severity** or **persistence**.
* Layman’s translation: **either today's reading is exceptionally low, or price has stayed very low for two observations in a row.**

`count_below(WILLR_14, -90, 4) < 3`

* Fewer than 3 of the last 4 observations are below `-90`.
* This prevents a mature Strong Buy setup from remaining classified as ordinary Buy.
* Layman’s translation: **the extreme-low condition has not yet lasted long enough to become Strong Buy.**

#### Two ways to reach Buy

| Buy path                 | What must happen                              | Beginner translation                                                                                  |
| ------------------------ | --------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Extreme-reading path** | Current WILLR `< -97`                         | **Price is almost at the absolute bottom of its recent 14-period range.**                             |
| **Persistence path**     | Both of the last 2 WILLR readings are `< -90` | **Price has stayed extremely close to the bottom of its recent range for two observations in a row.** |

In either case:

```text
fewer than 3 of the last 4 readings may be below -90
```

because otherwise the setup has matured into Strong Buy.

#### Literal summary

WILLR is either below `-97` now **or** has been below `-90` for both of the last two observations, while fewer than 3 of the last 4 observations are below `-90`.

#### Plain-English version

Price is extremely close to the bottom of its recent range.

That is enough for Buy if either:

1. today's reading is exceptionally extreme; **or**
2. price has remained very close to the bottom for two observations in a row.

If that very-low condition lasts long enough to appear in 3 of the last 4 observations, the signal advances to Strong Buy.

#### Interpretation

This is an **extreme-low contrarian Buy condition that has not yet matured into the persistence-based Strong Buy state**.

The progression can look like this:

```text
First ordinary reading below -90
→ Neutral

Exceptionally deep reading below -97
→ Buy immediately

Two consecutive readings below -90
→ Buy

3 of the last 4 readings below -90,
with the current reading still below -90
→ Strong Buy
```

#### Notes / confidence

* Buy does **not** require price to have started rising.
* A reading below `-97` is sufficiently extreme to bypass the normal two-observation persistence requirement.
* The two-reading path recognizes repeated weakness even if neither observation reaches `-97`.
* `Buy` means **“extreme-low setup”**, not “confirmed bottom.”
* In a persistent decline, price may continue falling after the Buy condition first appears.

---

### Neutral

```json
"neutral": "(WILLR_14 >= -90 and WILLR_14 < -7) or (WILLR_14 >= -97 and WILLR_14 < -90 and count_below(WILLR_14, -90, 2) < 2 and count_below(WILLR_14, -90, 4) < 3)"
```

#### Literal component breakdown

The Neutral rule has **two separate paths**.

#### Neutral path 1 — ordinary middle range

`WILLR_14 >= -90`

* WILLR is `-90` or higher.
* Price is not inside the project's very-low Buy-side zone.
* Layman’s translation: **price is not extremely close to the bottom of its recent range.**

`WILLR_14 < -7`

* WILLR remains below the Sell threshold.
* Price is not yet close enough to the top of the range to trigger Sell.
* Layman’s translation: **price is not extremely close to the top of its recent range either.**

Together:

```text
WILLR_14 >= -90 and WILLR_14 < -7
```

means:

> **Price is somewhere between the project's extreme-low Buy zone and extreme-high Sell zone.**

This is the straightforward form of Neutral.

#### Neutral path 2 — very low, but not yet enough for Buy or Strong Buy

```text
WILLR_14 >= -97
and WILLR_14 < -90
and count_below(WILLR_14, -90, 2) < 2
and count_below(WILLR_14, -90, 4) < 3
```

This clause covers an important special case:

> **Price is already very close to the bottom of its recent range, but the reading is neither extreme enough nor persistent enough to qualify for Buy or Strong Buy yet.**

`WILLR_14 >= -97 and WILLR_14 < -90`

* WILLR is below `-90`, so price is very close to the bottom of its recent 14-period range.
* But WILLR is not below `-97`.
* Therefore the immediate “exceptionally deep reading” Buy path has not triggered.
* Layman’s translation: **price is very low, but today's reading alone is not extreme enough to earn Buy.**

`count_below(WILLR_14, -90, 2) < 2`

* Fewer than 2 of the last 2 readings were below `-90`.
* In practice, the stock has **not been below `-90` for two observations in a row**.
* Therefore the normal persistence-based Buy condition has not triggered.
* Layman’s translation: **price has not stayed this low for two consecutive observations.**

`count_below(WILLR_14, -90, 4) < 3`

* Fewer than 3 of the last 4 readings were below `-90`.
* Therefore the broader persistence-based Strong Buy condition has not triggered.
* Layman’s translation: **price also has not spent enough of the last four observations this close to the bottom to qualify as Strong Buy.**

So all four pieces together mean:

> **Price is very low in its recent range, but today's reading is not below `-97`, it has not been below `-90` for two consecutive observations, and it has not been below `-90` often enough over the last four observations to qualify as Strong Buy. Therefore it remains Neutral.**

#### Why are both persistence checks needed?

The two conditions:

```text
count_below(WILLR_14, -90, 2) < 2
```

and:

```text
count_below(WILLR_14, -90, 4) < 3
```

check for **two different kinds of persistence**.

| Check                     | What it asks                                                                                          | Signal it keeps separate from Neutral |
| ------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------- |
| `count_below(..., 2) < 2` | “Have the last **two observations in a row** both been below `-90`?”                                  | **Buy**                               |
| `count_below(..., 4) < 3` | “Have at least **3 of the last 4 observations** been below `-90`, even if they were not consecutive?” | **Strong Buy**                        |

The first looks for a **short consecutive streak**.

The second looks for **broader persistence across four observations**.

Those are not the same pattern.

##### Example 1 — first very-low reading: Neutral

```text
-65 → -94
```

Current WILLR is `-94`.

* It is below `-90`.
* It is not below `-97`.
* Only 1 of the last 2 readings is below `-90`.
* Fewer than 3 of the last 4 are below `-90`.

→ **Neutral**

Beginner translation:

> **Price has just entered the very-low zone, but one reading alone is not enough.**

##### Example 2 — two very-low readings in a row: Buy

```text
-65 → -94 → -93
```

Now the last two observations are both below `-90`.

So:

```text
count_below(WILLR_14, -90, 2) = 2
```

The Neutral condition fails.

→ **Buy**

Beginner translation:

> **Price has stayed very close to the bottom for two observations in a row, so the signal advances from Neutral to Buy.**

##### Example 3 — not two in a row, but 3 of the last 4: Strong Buy

```text
-92 → -91 → -50 → -94
```

The last two observations are:

```text
-50 → -94
```

so they are not both below `-90`.

But across all four observations:

```text
-92 ✓
-91 ✓
-50 ✗
-94 ✓
```

three are below `-90`.

So:

```text
count_below(WILLR_14, -90, 4) = 3
```

→ **Strong Buy**

Beginner translation:

> **The stock did not stay below `-90` for the last two observations in a row, but it has still spent most of the last four observations near the bottom of its range. That broader persistence is enough for Strong Buy.**

#### The simplest way to understand Neutral

For WILLR(14), Neutral means one of two things:

```text
1. Price is not in either active extreme zone.

OR

2. Price has entered the very-low zone,
   but it has not yet done enough to earn Buy or Strong Buy.
```

For the second case, ask:

```text
Is today's reading exceptionally deep below -97?
→ If yes: Buy.

Have the last two readings both been below -90?
→ If yes: Buy.

Have at least 3 of the last 4 readings been below -90?
→ If yes: Strong Buy.

If all three answers are no:
→ Neutral.
```

#### Literal summary

Neutral means either:

1. WILLR is between `-90` and `-7`; **or**
2. WILLR is between `-97` and `-90`, but it has qualified for neither the immediate extreme-reading Buy path, the two-consecutive-observation Buy path, nor the 3-of-4 Strong Buy path.

#### Plain-English version

Price is either in the broad middle of its recent range, **or it has only recently moved very close to the bottom and has not yet become extreme or persistent enough to earn a Buy signal.**

#### Interpretation

This is a **middle-range or not-yet-qualified extreme state**.

The second Neutral path is essentially a waiting state:

> **“Price is unusually low, but we do not yet have enough evidence to promote the signal.”**

A `-94` Neutral reading therefore means something different from a `-50` Neutral reading:

```text
-50 Neutral
= ordinary middle-range condition

-94 Neutral
= very-low condition that has not yet qualified for Buy
```

#### Notes / confidence

* `WILLR = -90` belongs to ordinary Neutral because the Buy-side tests require values strictly below `-90`.
* A first reading such as `-94` can remain Neutral.
* A first reading below `-97` becomes Buy immediately because severity alone is sufficient.
* Two consecutive readings below `-90` become Buy.
* Three of the last four readings below `-90`, with the current reading also below `-90`, become Strong Buy — even if the last two readings are not both below `-90`.
* Neutral therefore acts as both the ordinary middle state **and** the temporary holding state for a newly extreme reading that has not yet met a stronger rule.

---

### Sell

```json
"sell": "WILLR_14 >= -7"
```

#### Literal component breakdown

`WILLR_14 >= -7`

* The current Williams %R value is `-7` or closer to `0`.
* Price is closing extremely close to the top of its recent 14-period range.
* Layman’s translation: **price is trading very near the highest part of its recent range.**

Because Williams %R uses a negative scale:

```text
-5 is HIGHER than -20

-2 is closer to the recent high than -10
```

#### Literal summary

WILLR is `-7` or higher.

#### Plain-English version

Price is closing extremely close to the top of its recent 14-period range.

#### Interpretation

This is a **contrarian extreme-high condition**.

The Sell signal says:

> Price is stretched toward the very top of where it has traded recently.

It does **not** say that price has already begun falling.

For example:

```text
WILLR = -4
```

means price is extremely close to the recent high.

That is enough to satisfy Sell unless the Strong Sell condition also applies.

#### Notes / confidence

* The Williams %R scale is reversed-looking: values closer to `0` correspond to higher positions in the recent range.
* Sell is triggered by the current extreme reading alone.
* The rule does not require a downturn or reversal.
* A strong uptrend can keep WILLR near `0` for multiple observations.
* Sell should therefore be read as **“extreme-high / stretched condition”**, not “price must fall next.”

---

### Strong sell

```json
"strong_sell": "WILLR_14 >= -5 and falling_2bar(WILLR_14, 1)"
```

#### Literal component breakdown

`WILLR_14 >= -5`

* The current WILLR reading is `-5` or closer to `0`.
* Price is closing exceptionally close to the top of its recent 14-period range.
* This is more extreme than the ordinary Sell threshold of `-7`.
* Layman’s translation: **price is almost at the top of its recent range.**

`falling_2bar(WILLR_14, 1)`

* Despite the helper's legacy name, the explicit argument `1` makes this a current-versus-prior-observation comparison.
* The current WILLR value is lower than the immediately preceding WILLR value.
* Example:

```text
prior WILLR   = -2
current WILLR = -4
```

Since `-4` is lower than `-2`, WILLR has fallen.

* Layman’s translation: **the indicator has started moving away from the very top of the range.**

`WILLR_14 >= -5 and falling_2bar(WILLR_14, 1)`

* Both conditions must be true.
* Price must still be exceptionally close to the recent high.
* WILLR must also have moved lower from the prior observation.
* Layman’s translation: **price is still extremely high in its recent range, but the first sign of movement away from that high has appeared.**

#### Literal summary

WILLR is at least `-5`, and the current WILLR reading is lower than the previous reading.

#### Plain-English version

Price is extremely close to the top of its recent range, but Williams %R has just started moving lower.

#### Interpretation

This is an **extreme-high condition with an initial sign of retreat from the high**.

For example:

```text
-2 → -4
```

The current `-4` reading still places price extremely close to the top of its recent range.

But WILLR has moved down from `-2` to `-4`.

→ **Strong Sell**

The key difference is:

```text
Sell
= extremely close to the recent high

Strong Sell
= even closer to the recent high
  + beginning to move away from that high
```

#### Notes / confidence

* `-5` is a more extreme threshold than the ordinary `-7` Sell cutoff.
* The falling test compares only the current observation with the immediately preceding observation.
* Strong Sell does not require a long decline.
* It identifies an **initial rollover while price is still near the top of its range**.
* It is not proof that a durable top has formed.

---

## Industry-standard baseline
Williams %R is normally interpreted as a bounded oscillator from `0` to `-100`. It reflects where the close sits relative to the highest high / lowest low over the lookback period. 

Standard Williams %R interpretation usually emphasizes:
* Williams %R normally ranges from **`-100` to `0`**.
* Values closer to `-100` mean the close is near the **bottom** of the recent high-low range.
* Values closer to `0` mean the close is near the **top** of the recent range.
* A conventional oversold area is commonly around **`-80` or lower**.
* A conventional overbought area is commonly around **`-20` or higher**.
* An oversold reading is not necessarily a Buy by itself.
* An overbought reading is not necessarily a Sell by itself.
* During a strong downtrend, Williams %R can remain near `-100`.
* During a strong uptrend, Williams %R can remain near `0`.

The common default interpretation is:

| Condition                                     | Basic translation                                                                                |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `WILLR <= -80`                                | Price is near the lower end of its recent range; conventionally considered oversold territory.   |
| `WILLR ≈ -50`                                 | Price is around the middle of its recent high-low range.                                         |
| `WILLR >= -20`                                | Price is near the upper end of its recent range; conventionally considered overbought territory. |
| WILLR starts rising from a very-low reading   | Price is moving away from the lower end of the range.                                            |
| WILLR starts falling from a very-high reading | Price is moving away from the upper end of the range.                                            |

The project's rules are intentionally **more selective than the conventional `-80/-20` shorthand**.

They use tighter thresholds and, for WILLR(14) and WILLR(20), persistence tests so that a routine oversold reading does not automatically become a Buy or Strong Buy.

The project therefore uses Williams %R primarily as a:

> **contrarian range-position / exhaustion indicator**

rather than a simple momentum-continuation score.

---

## Comparison of the three Williams %R settings

The three settings all answer the same basic question:

> **Where is the closing price inside its recent high-low range?**

But they use different lookback periods **and different project-specific signal rules**.

They should therefore not be treated as identical rules applied at three speeds.

| Setting     | Relative speed     | What it emphasizes                                                  | Project rule style                                                                                           | Main trade-off                                                                                 |
| ----------- | ------------------ | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `WILLR(5)`  | Fastest            | Very short-term range extremes                                      | Direct, highly selective level thresholds                                                                    | Responds quickly, but short lookback values can move sharply from one observation to the next  |
| `WILLR(14)` | Balanced / primary | Intermediate range position plus persistence near the lower extreme | Severity **or** persistence for Buy; broader persistence for Strong Buy; high-end rollover for Strong Sell   | More context than WILLR(5) while remaining reasonably responsive                               |
| `WILLR(20)` | Slowest            | Broader, slower range extremes and more persistent weakness         | Two-observation persistence for Buy; 3-of-4 persistence for Strong Buy; exceptional `< -99.9` floor override | Filters more short-term movement, but normally takes more evidence to produce Buy-side signals |

### Practical selection guide

```text
Use WILLR(5)
when very short-term range extremes matter most.

Use WILLR(14)
when you want the balanced primary setting
and want persistence to matter.

Use WILLR(20)
when you want a slower range-position view
and generally require more persistent weakness
before assigning Buy / Strong Buy.
```

### Important: the thresholds are not interchangeable

The three settings intentionally use different rule thresholds.

For example:

```text
WILLR(5)
Strong Buy = <= -97

WILLR(14)
Strong Buy = persistent readings below -90

WILLR(20)
Strong Buy = persistent readings below -90
             OR an exceptional reading below -99.9
```

So a value of `-96` can mean different things depending on the WILLR setting and its recent history.

The **number tells you range position**.

The **signal tells you how that setting's rulebook interprets that number and recent sequence**.

---

## Rule interpretation tables

### WILLR(14) Rules interpretation

| Source        | Signal      | Rule logic                                                                                                                                                | What's happening                                                                                                                                                    | Answers the question                                                                            | Bottom-line                                                                                                 |
| ------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **WILLR(14)** | Strong Buy  | `WILLR_14 < -90 and count_below(WILLR_14, -90, 4) >= 3`                                                                                                   | Price is extremely close to the bottom of its recent range and has been there repeatedly.                                                                           | *“Is price near the bottom of its recent range, and has that extreme-low condition persisted?”* | **Price has repeatedly been closing near the bottom of its recent range.**                                  |
| **WILLR(14)** | Buy         | `(WILLR_14 < -97 or count_below(WILLR_14, -90, 2) >= 2) and count_below(WILLR_14, -90, 4) < 3`                                                            | Price is either exceptionally close to the bottom now or has stayed very low for two observations, but the longer Strong Buy persistence condition has not matured. | *“Is price exceptionally low now, or has it stayed very low long enough to trigger Buy?”*       | **Price is extremely low in its recent range, but the stronger persistence condition has not yet matured.** |
| **WILLR(14)** | Neutral     | `(WILLR_14 >= -90 and WILLR_14 < -7) or (WILLR_14 >= -97 and WILLR_14 < -90 and count_below(WILLR_14, -90, 2) < 2 and count_below(WILLR_14, -90, 4) < 3)` | Price is either in the broad middle of its recent range or has only just entered the very-low zone without enough severity or persistence for Buy.                  | *“Is price outside the active extremes, or only beginning to enter the very-low zone?”*         | **Price is either in the middle of its recent range or only beginning to look unusually low.**              |
| **WILLR(14)** | Sell        | `WILLR_14 >= -7`                                                                                                                                          | Price is extremely close to the top of its recent range.                                                                                                            | *“Is price currently stretched near the top of its recent range?”*                              | **Price is trading very near the top of its recent range.**                                                 |
| **WILLR(14)** | Strong Sell | `WILLR_14 >= -5 and falling_2bar(WILLR_14, 1)`                                                                                                            | Price is exceptionally close to the top of its recent range, but WILLR has started moving lower.                                                                    | *“Is price extremely high in its recent range and beginning to move away from that high?”*      | **Price is extremely high in its recent range and is showing an initial sign of retreat.**                  |

### WILLR(5) Rules interpretation

| Source       | Signal      | Rule logic                                   | What's happening                                                                                                           | Answers the question                                                                  | Bottom-line                                                                                     |
| ------------ | ----------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **WILLR(5)** | Strong Buy  | `WILLR_5 <= -97`                             | Price is almost at the absolute bottom of its very short 5-period range.                                                   | *“Is price exceptionally close to the bottom of its short-term range?”*               | **Price is at an unusually deep short-term extreme.**                                           |
| **WILLR(5)** | Buy         | `WILLR_5 > -97 and WILLR_5 <= -95`           | Price is extremely close to the bottom of its 5-period range, but not inside the strongest `<= -97` zone.                  | *“Is price very close to its short-term low without reaching the most extreme zone?”* | **Price is very near the bottom of its short-term range.**                                      |
| **WILLR(5)** | Neutral     | `WILLR_5 > -95 and WILLR_5 < -5`             | Price is outside both of the project's very narrow short-term extreme zones.                                               | *“Is price outside the unusually low and unusually high short-term extremes?”*        | **Price is not at one of the project's selected short-term extremes.**                          |
| **WILLR(5)** | Sell        | `WILLR_5 >= -5`                              | Price is extremely close to the top of its 5-period range.                                                                 | *“Is price almost at the top of its short-term range?”*                               | **Price is at an unusually high short-term extreme.**                                           |
| **WILLR(5)** | Strong Sell | `WILLR_5 >= -5 and falling_2bar(WILLR_5, 1)` | Price remains extremely close to the top of its 5-period range, but WILLR has just moved lower from the prior observation. | *“Is price at an extreme short-term high and beginning to move away from it?”*        | **Price is extremely high in its short-term range and has begun to retreat from that extreme.** |

#### WILLR(5) — important context

WILLR(5) is intentionally simple.

It does **not** wait for multi-observation Buy-side persistence.

Instead:

```text
<= -97
→ Strong Buy

> -97 through -95
→ Buy

> -95 through < -5
→ Neutral

>= -5
→ Sell

>= -5 and falling from the prior observation
→ Strong Sell
```

This makes WILLR(5) a **fast, severity-driven range-extreme indicator**.

Because the lookback contains only 5 periods, the range can change quickly. A sharp new high or low can therefore cause WILLR(5) to move substantially from one observation to the next.

---

### WILLR(20) Rules interpretation

| Source        | Signal      | Rule logic                                                                                                                                                                        | What's happening                                                                                                                                  | Answers the question                                                                              | Bottom-line                                                                           |
| ------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **WILLR(20)** | Strong Buy  | `WILLR_20 < -99.9 or (WILLR_20 < -90 and count_below(WILLR_20, -90, 4) >= 3)`                                                                                                     | Price is either essentially at the absolute bottom of its 20-period range, or has repeatedly remained extremely close to that bottom.             | *“Is price essentially at the range floor, or has it persistently stayed near the bottom?”*       | **Price is at an exceptional or persistent long-window low extreme.**                 |
| **WILLR(20)** | Buy         | `WILLR_20 < -85 and count_below(WILLR_20, -85, 2) >= 2 and WILLR_20 >= -99.9 and (WILLR_20 >= -90 or count_below(WILLR_20, -90, 4) < 3)`                                          | Price has remained near the bottom of its 20-period range for two consecutive observations, but it has not qualified for either Strong Buy route. | *“Has price stayed unusually low for two observations without reaching Strong Buy?”*              | **Price has persistently remained near the bottom of its broader range.**             |
| **WILLR(20)** | Neutral     | `(WILLR_20 >= -85 and WILLR_20 < -10) or (WILLR_20 < -85 and WILLR_20 >= -99.9 and count_below(WILLR_20, -85, 2) < 2 and (WILLR_20 >= -90 or count_below(WILLR_20, -90, 4) < 3))` | Price is either in the broad non-extreme zone or has entered the low zone without enough persistence to qualify as Buy/Strong Buy.                | *“Is price outside the active extremes, or has the low condition not persisted long enough yet?”* | **Price is either in the broad middle or only beginning to establish a low extreme.** |
| **WILLR(20)** | Sell        | `WILLR_20 >= -10`                                                                                                                                                                 | Price is very close to the top of its broader 20-period range.                                                                                    | *“Is price stretched toward the top of its broader range?”*                                       | **Price is trading very near the top of its 20-period range.**                        |
| **WILLR(20)** | Strong Sell | `WILLR_20 >= -5 and falling_2bar(WILLR_20, 1)`                                                                                                                                    | Price is exceptionally close to the top of its 20-period range and WILLR has just begun moving lower.                                             | *“Is price extremely high in its broader range and starting to retreat?”*                         | **Price is extremely high in its broader range and showing an initial rollover.**     |

#### WILLR(20) — why Strong Buy has two paths

WILLR(20) normally requires persistence for Strong Buy:

```text
Current WILLR < -90
+
at least 3 of the last 4 WILLR readings < -90
```

This means:

> **Price has repeatedly spent time extremely close to the bottom of its broader 20-period range.**

But WILLR(20) also has one exceptional override:

```text
WILLR_20 < -99.9
```

This means the closing price is effectively at the **absolute bottom of the 20-period range**.

That condition is sufficiently extreme that the rule does not wait for several observations of persistence.

So WILLR(20) Strong Buy can mean one of two things:

```text
Path 1 — exceptional floor

WILLR < -99.9
→ price is essentially at the absolute bottom
  of the 20-period range

OR

Path 2 — persistent extreme

WILLR < -90 now
+ at least 3 of the last 4 readings < -90
→ price has repeatedly remained extremely close
  to the bottom of the range
```

The floor override should **not** be interpreted as:

> “This is definitely the final market bottom.”

It means:

> **The current range position is so extreme that the project treats it as a Strong Buy condition immediately rather than waiting for persistence.**

Historical testing of this project rule showed that such floor events can still experience additional downside after the signal. The rule therefore identifies an **exceptional contrarian extreme**, not a guaranteed turning point.

---

## Understanding Williams %R

### What the number actually tells you

Williams %R has only one primary numeric output.

Unlike Stochastic, there is no `%K` and `%D` pair to compare.

The WILLR value itself answers:

> **Where did the stock close inside the recent high-low range?**

In project naming:

```text
WILLR_5
= closing-price position inside the most recent 5-period range

WILLR_14
= closing-price position inside the most recent 14-period range

WILLR_20
= closing-price position inside the most recent 20-period range
```

### What WILLR = -90 means

A reading around:

```text
-90
```

means:

> **The close is very near the bottom of the recent range.**

Conceptually, it is only about 10% of the high-low range above the recent low.

A reading around:

```text
-10
```

means:

> **The close is very near the top of the recent range.**

Conceptually, it is only about 10% of the high-low range below the recent high.

A reading around:

```text
-50
```

means:

> **The close is roughly halfway between the recent high and low.**

### Higher and lower can sound backward

With Williams %R:

```text
-5 is higher than -20

-95 is lower than -80
```

Therefore:

```text
WILLR rising
= moving toward 0
= close moving toward the upper part of the recent range

WILLR falling
= moving toward -100
= close moving toward the lower part of the recent range
```

This matters particularly for Strong Sell.

For example:

```text
-2 → -4
```

is a **fall** in WILLR.

Price is still very near the top of the range, but the indicator has begun moving away from that top.

That is the rollover behavior used by the Strong Sell rules.

---

## Reading WILLR in the app

The displayed WILLR number and the signal label answer **different questions**.

### The displayed value

The numeric value tells you:

> **Where is today's closing price within this setting's recent high-low range?**

Example:

```text
WILLR(14) = -94
```

means:

> **Price is closing extremely close to the bottom of its 14-period range.**

### The signal / color

The signal tells you:

> **How does the project's rulebook interpret that value and its recent history?**

For example, the same:

```text
WILLR(14) = -94
```

could be:

```text
Neutral
```

if this is only the first very-low observation,

or:

```text
Buy
```

if the previous observation was also below `-90`,

or:

```text
Strong Buy
```

if at least 3 of the last 4 observations were below `-90`.

So:

> **Do not try to infer the signal from the current number alone when the rule uses recent history.**

This is especially important for WILLR(14) and WILLR(20).

### Trend versus signal

If the app reports that WILLR is:

```text
Rising
```

that simply means the current WILLR value is higher than the prior value.

Example:

```text
-94 → -89
```

WILLR is rising.

If the app reports:

```text
Falling
```

the current value is lower than the prior value.

Example:

```text
-2 → -4
```

WILLR is falling.

This one-observation direction is **context**.

It should not be confused with the multi-observation persistence rules such as:

```text
2 consecutive readings below -90
```

or:

```text
3 of the last 4 readings below -90
```

Those are separate rulebook conditions.

### Warmup / unavailable values

Williams %R needs enough price history to define its selected high-low range.

Early observations before the required lookback is initialized may therefore be unavailable / blank.

A blank value should not be interpreted as Neutral.

It means:

> **There was not yet enough valid history to calculate and classify that WILLR observation.**

---

## Notes: Williams %R

The **Williams %R oscillator** compares the latest closing price with the recent highest high and lowest low.

For `WILLR(14)`:

* `14` = lookback window used to define the recent high-low range.
* Output normally runs from `-100` to `0`.
* Near `-100` = close near the recent low.
* Near `0` = close near the recent high.

**Simple interpretation:**

```text
Near -100
= close near bottom of recent range

Near -50
= close around middle of recent range

Near 0
= close near top of recent range
```

In the project, Williams %R is treated primarily as a **contrarian exhaustion / range-position indicator**.

The three variants differ deliberately:

```text
WILLR(5)
= fast, severity-focused extremes

WILLR(14)
= balanced severity + persistence model

WILLR(20)
= slower persistence model
  with exceptional floor override
```

### What Williams %R does well

**Range-position clarity**

Williams %R gives a very direct answer to whether price is currently near the top or bottom of its own recent range.

**Extreme-condition detection**

It is useful for identifying when price has become unusually stretched toward one end of that range.

**Persistence context**

The project's 14- and 20-period rules go beyond a single reading by distinguishing a newly extreme condition from one that has persisted.

**Different horizons**

The 5-, 14-, and 20-period variants allow short-, medium-, and longer-window range position to be viewed separately.

### Limitations

**An extreme is not a reversal**

A stock can remain close to the bottom of its range while continuing to decline.

Likewise, it can remain close to the top while continuing to rise.

**Williams %R does not measure trend strength**

A reading of `-95` tells you that price is near the recent low.

It does not independently tell you whether the broader trend is weak, strong, bullish, or bearish.

**The range moves**

The recent highest high and lowest low change as observations enter and leave the lookback window.

Williams %R can therefore change because:

* the closing price moved;
* the recent high changed;
* the recent low changed;
* or some combination of the three.

**Shorter settings are more reactive**

WILLR(5) can change considerably because its recent range contains only five periods.

**Signals are project-specific**

Industry convention often describes broad `-80/-20` overbought/oversold zones.

The project's five-state signals use substantially tighter and more selective thresholds and should not be confused with generic textbook labels.

---

### 101

**Purpose:** Show where the latest closing price sits within the recent high-low range so that unusually high and unusually low range positions can be identified.

**Use when:** You want to know whether price is currently trading near the top or bottom of where it has traded recently.

**Key concept:** Williams %R is a range-position indicator.

```text
Closer to -100
= closer to the recent low

Closer to 0
= closer to the recent high
```

**Calculation:**

```text
Williams %R
=
-100 × (Highest High − Current Close)
       ÷ (Highest High − Lowest Low)
```

**Traditional interpretation:**

```text
At or below roughly -80
= conventionally oversold

At or above roughly -20
= conventionally overbought
```

**Project interpretation:**

The project uses tighter, parameter-specific rules rather than treating every conventional oversold/overbought observation as a Buy or Sell.

For the primary `WILLR(14)` setting:

```text
Persistent extreme near the low
→ Strong Buy

Exceptionally deep or consecutively very-low readings
→ Buy

Middle / not-yet-qualified low extreme
→ Neutral

Extremely close to recent high
→ Sell

Extremely close to recent high + initial rollover
→ Strong Sell
```

**Tips:**

* Always remember the negative scale: `-5` is near the high; `-95` is near the low.
* Treat extreme readings as **conditions**, not predictions.
* Use trend context before assuming that oversold must rebound or overbought must decline.
* For WILLR(14) and WILLR(20), check recent history because the current value alone may not determine the signal.
* Compare different WILLR periods as different horizons, not as three equal “votes.”

**Optimal conditions:** Particularly useful when range extremes matter—for example, swing setups, pullbacks, exhaustion monitoring, and range-bound markets. It can also provide useful context during trends, provided extreme readings are not automatically assumed to signal reversal.

**Limitations:** Can remain extreme during persistent trends; does not independently measure trend strength, volume participation, or the probability/timing of a reversal.

---

## Initial audit note

Williams %R was reviewed as a **bounded range-position / exhaustion oscillator** with a contrarian project philosophy.

Key conclusions:

* Numeric range: approximately `-100` to `0`.
* Lower / more negative values mean price is closer to the recent low.
* Higher / less negative values mean price is closer to the recent high.
* Active project variants are `WILLR(5)`, `WILLR(14)`, and `WILLR(20)`.
* The three variants intentionally use different semantic rules rather than one universal threshold model.
* `WILLR(14)` is the primary balanced setting and combines current-reading severity with recent persistence.
* `WILLR(5)` is a faster severity-driven model.
* `WILLR(20)` is a slower persistence model with an exceptional `< -99.9` immediate Strong Buy override.
* Buy / Strong Buy mean **contrarian extreme conditions**, not confirmed bottoms.
* Sell means an extreme-high condition; Strong Sell adds an initial one-observation rollover.
* Neutral on WILLR(14) and WILLR(20) can include a newly very-low reading that has not yet met the stronger persistence requirements.
* The project's thresholds are deliberately more selective than conventional `-80/-20` Williams %R shorthand.
* The current signal semantics were mechanically and manually validated before this documentation was prepared.
* Numeric display and semantic classification remain separate: the displayed WILLR value reports range position, while the rulebook determines the signal using that value and, where applicable, recent history.



---
# Williams R% (original notes)

**Purpose:** Identify overbought and oversold levels by measuring where the current close falls within the recent price range, similar to Stochastic but with inverted scale.

**Use when:** You want overbought/oversold signals with faster, more sensitive readings than traditional Stochastic.
- **Market conditions:** The indicator works best in sideways or ranging markets. In strong trends, it can stay overbought or oversold for a long time, so use it with caution and confirmation

**Key Concept:** Uses the same logic as Stochastic but inverted, ranging from 0 to -100.
- More sensitive to recent price action and often provides earlier signals.

**Calculation:** `%R = [(Highest High - Current Close) ÷ (Highest High - Lowest Low)] × -100`, typically over 14 periods.

**Signals & Interpretation:**
Momentum indicator scaled 0 to -100.

- **Overbought**:  '`> -20`'
	- Above -20 = overbought (near 0)
		-  price near highs, potential sell
- **Oversold**: '`< -80`'
	- Below -80 = oversold (near -100)
		- price near lows, potential buy
- **Potential 'Buy' signal**: Crossing above -80 from below
	- Often triggered when Williams %R crosses above -80 from below (indicating a shift from oversold to bullish momentum).
- **Potential 'Sell' signal**: Crossing below -20 from above
	- Often triggered when Williams %R crosses below -20 from above (indicating a shift from overbought to bearish momentum).
- Divergences with price suggest momentum shifts
- More sensitive than Stochastic to recent price changes

**Optimal Conditions:** Effective in volatile markets where quick momentum shifts occur. Works well on shorter timeframes and for active trading strategies.

**Limitations:** High sensitivity can lead to many false signals and whipsaws. Requires careful confirmation from other indicators.

