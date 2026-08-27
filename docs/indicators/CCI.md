## Summary: CCI Signals
**<u>Class</u>**: Momentum / Oscillator
**<u>aka</u>**: Commodity Channel Index

CCI tells you whether the current price is unusually high or unusually low relative to its recent normal behavior.
- measures how far the market's current **typical price** has moved away from its recent statistical average.
- tells you how far price is from its recent average, adjusted by the typical amount of deviation.
- measures the deviation from average price, typically oscillating around 0.


$$----------$$
At the simplest level, this app asks:
1. **Has CCI moved far enough below its normal range to indicate meaningful downside stretch?**
2. **Has CCI moved far enough above its normal range to indicate meaningful upside stretch?**


The primary CCI Signal uses a **contrarian / mean-reversion interpretation**:

| Signal               | Literal trigger      | Layman’s translation                                                                           | Rule logic                           | Bottom-line                                                                                       |
| -------------------- | -------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------- |
| **Strong Buy (+2)**  | `CCI <= -200`        | CCI is severely depressed relative to its recent norm.                                         | Severe downside statistical stretch. | **Price/momentum conditions are unusually stretched to the downside, raising rebound potential.** |
| **Buy (+1)**         | `-200 < CCI <= -150` | CCI is materially depressed, but not at the most extreme project threshold.                    | Material downside stretch.           | **The market is meaningfully stretched to the downside.**                                         |
| **Neutral (0)**      | `-150 < CCI <= +150` | CCI is not far enough from its recent norm to trigger the project's contrarian extreme states. | Middle / non-extreme range.          | **CCI does not currently indicate a sufficiently large statistical stretch.**                     |
| **Sell (-1)**        | `+150 < CCI < +200`  | CCI is materially elevated relative to its recent norm.                                        | Material upside stretch.             | **The market is meaningfully stretched to the upside.**                                           |
| **Strong Sell (-2)** | `CCI >= +200`        | CCI is severely elevated relative to its recent norm.                                          | Severe upside statistical stretch.   | **Price/momentum conditions are unusually stretched to the upside, raising pullback risk.**       |

> **Important:** In this project, `Strong Buy` and `Strong Sell` describe **severity of the current CCI extreme**.
> - They do **not** mean that a reversal has already begun.

A CCI reading can remain below `-200` for more than one observation.
During that entire period, the primary Signal remains:

```text
Strong Buy
```

Likewise, CCI can remain above `+200` and continue to classify as:

```text
Strong Sell
```

The Signal is therefore a **persistent current-state classification**, not a one-day threshold-crossing event.

---

### Signal, Divergence, Zero-Line Crossover - the 3  layers

CCI now exposes three different pieces of information.

They should be viewed as **different lenses**, not three votes that must always agree.

| Layer                       | Main question                                                            | Simplest translation                                                        |
| --------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| **Signal**                  | How statistically stretched is CCI right now?                            | **Is the current reading normal, materially extreme, or severely extreme?** |
| **CCI Divergence**          | Is price making a new confirmed swing extreme without CCI confirming it? | **Is price telling one story while CCI tells another?**                     |
| **CCI Zero-Line Crossover** | Did CCI just cross through its zero midpoint?                            | **Has the oscillator's immediate momentum bias just changed sides?**        |

The shortest useful summary is:
- **Signal** = current stretch
- **Divergence** = price/momentum disagreement.
- **Zero-line crossover** = momentum-bias transition.

CCI Divergence and CCI Zero-Line Crossover are **independent context**.
They do not change the primary CCI score.

---
#### Interpreting 'Signal', 'Divergence', 'Zero-Line Crossover' together

| Signal          | CCI Divergence | Zero-Line Crossover  | Beginner interpretation                                                                                                                                                                                      |
| --------------- | -------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Strong Buy**  | **Bullish**    | None                 | CCI is severely downside-stretched, and a confirmed lower price low occurred with a higher CCI reading. **The extreme and divergence both point toward possible downside exhaustion.**                       |
| **Strong Buy**  | None           | **Uptrend Bias ▲**   | CCI remains severely stretched, but it has just crossed above zero. **The primary extreme and the newest momentum transition both favor a rebound interpretation.**                                          |
| **Strong Buy**  | **Bearish**    | **Downtrend Bias ▼** | CCI is severely downside-stretched, but the newest secondary context remains bearish. **The market is stretched enough to raise rebound potential, while recent momentum context still argues for caution.** |
| **Buy**         | **Bullish**    | None                 | CCI is materially depressed and price/CCI swing behavior also suggests downside momentum is weakening. **Two independent forms of evidence point toward rebound risk.**                                      |
| **Neutral**     | **Bullish**    | **Uptrend Bias ▲**   | CCI itself is no longer extreme, but a confirmed bullish divergence and fresh move through zero provide positive momentum context. **The score is Neutral even though secondary context is constructive.**   |
| **Neutral**     | **Bearish**    | **Downtrend Bias ▼** | CCI is not statistically extreme, but both secondary layers are warning about weakening momentum.                                                                                                            |
| **Sell**        | **Bearish**    | None                 | CCI is materially upside-stretched while the latest confirmed price high was reached with weaker CCI. **The extreme and divergence both raise pullback risk.**                                               |
| **Strong Sell** | **Bullish**    | **Uptrend Bias ▲**   | CCI is severely upside-stretched, but recent secondary context remains positive. **The primary contrarian warning and current momentum evidence disagree; neither should erase the other.**                  |

This independence is intentional.

For example, the app can legitimately show:

```text
Signal: Strong Buy
CCI Divergence: Bearish
CCI Zero-Line Crossover: Downtrend Bias
```

That is not contradictory.

It means:

> **CCI is severely stretched to the downside, but the newest divergence and zero-line evidence do not yet support a bullish reversal interpretation.**

The primary Signal answers:

> **How extreme is the current CCI reading?**

The context fields answer different questions.

---

## CCI — brief overview
The Commodity Channel Index (CCI) measures how far the market's current **typical price** has moved away from its recent statistical average.

Despite its name, CCI is not limited to commodities. It is widely used with stocks, ETFs, futures, currencies, and other traded instruments.

At the simplest level, this app asks:
1. **Has CCI moved far enough below its normal range to indicate meaningful downside stretch?**
2. **Has CCI moved far enough above its normal range to indicate meaningful upside stretch?**


**Purpose:** Identify cyclical turns and measure how far price deviates from its statistical average to spot potential reversal points.
**Use when:** You want to identify when prices are extremely stretched from their normal range, particularly in cyclical markets.
### What CCI measures

CCI compares the market's current **Typical Price** with the average Typical Price over a specified lookback period.

Typical Price is:

```text
Typical Price = (High + Low + Close) / 3
```

CCI then asks how far that Typical Price is from its recent moving average relative to the average amount by which Typical Price normally varies around that average.

Conceptually:

```text
CCI =
    Typical Price - Average Typical Price
    --------------------------------------
       0.015 × Mean Deviation
```

More explicitly:

```text
TP = (High + Low + Close) / 3

CCI =
    TP - SMA(TP, n)
    -------------------------
    0.015 × MeanDeviation(TP, n)
```

The constant `0.015` is part of the conventional CCI construction.

The result is an oscillator centered around:

```text
0
```

but unlike RSI or Stochastic, CCI is **not bounded**.

It can move above:

```text
+100
+150
+200
```

or below:

```text
-100
-150
-200
```

and can continue farther in either direction.

$$----------$$
> **FYI:**
> CCI does **not** measure:
> ```
> where today's price sits within the last 20 days
> ```
>
> It measures:
> ```
> where current Typical Price sits
> relative to its own 20d moving average,
> scaled by recent mean deviation
> ```



---

### A simple way to understand CCI

CCI is essentially asking:

> **How unusual is the market's current price position compared with its own recent behavior?**

- A strongly positive CCI means Typical Price is unusually high relative to its recent norm.
- A strongly negative CCI means Typical Price is unusually low relative to its recent norm.

For example:

```text
CCI = +35
```

means price is above its recent statistical center, but not particularly extreme under this project's scoring model.

```text
CCI = +175
```

means price is materially stretched above that recent norm.

```text
CCI = -215
```

means price is severely stretched below it.

---
### The 3 CCI variants

The app provides three CCI lookback periods:

| Variant     | Period | Horizon     | Character                                                                                                |
| ----------- | -----: | ----------- | -------------------------------------------------------------------------------------------------------- |
| **CCI(10)** |     10 | Short term  | Fastest and most responsive; reacts sooner to recent price deviations but changes state more frequently. |
| **CCI(14)** |     14 | Medium term | Balanced intermediate view between responsiveness and smoothing.                                         |
| **CCI(20)** |     20 | Long term   | Slowest of the three; requires more persistent price behavior to move to the same degree.                |

All three use the same primary scoring thresholds:

```text
<= -200        Strong Buy
-200 to -150   Buy
-150 to +150   Neutral
+150 to +200   Sell
>= +200        Strong Sell
```

The period changes **responsiveness**, not the semantic meaning of the states.

A `CCI(10)` value can move into or out of an extreme more quickly because it is comparing price with a shorter history.

A `CCI(20)` reading is smoother and generally slower to change because more observations contribute to its statistical baseline.

The three variants should therefore be interpreted as:

```text
CCI(10) = short-horizon stretch
CCI(14) = intermediate stretch
CCI(20) = longer-horizon stretch
```

not as three independent votes of equal meaning.

$$----------$$
> **TIP**
> To time local minima,
> - Use `CCI(20) <= -150` to identify
> 	- and confirm using `CCI(14) <= -200`


$$----------$$
> **WHEN TO USE**
> - **CCI(14):** <u>strongest</u> balanced contrarian timing candidate.
> - **CCI(20):** <u>strongest</u> local-extrema / slower exhaustion locator.
 > 	- the best *'location'/'exhaustion'* indicator
> - **CCI(10):** fast 'exhaustion'/'reversal' detector.

---

## CCI Rule Translation

CCI(10), CCI(14), and CCI(20) use the same rule structure.

The examples below use **CCI(14)**.

---
### Strong Buy (+2)

The rule is:

```text
CCI_14 <= -200
```

#### Literal component breakdown

`CCI_14`

* Current CCI value using a 14-period lookback.

`<= -200`

* The reading must be at or below negative 200.

#### Plain-English version

> **CCI(14) is severely depressed relative to its recent statistical norm.**

#### Interpretation
- This is a **severe downside-stretch state**.
- It raises the possibility that selling pressure or downside price displacement has become unusually extended.
- It does **not**:
	- require CCI to turn upward.
	- require bullish divergence.
	- require a zero-line crossover.
	- claim that the low has already occurred.

For example:

```text
CCI = -208
```

produces:

```text
Strong Buy
```

even if CCI fell further that day.

That is intentional.

> **Strong describes the severity of the stretch—not confirmation that a rebound has started.**

---

### Buy (+1)

The rule is:

```text
CCI_14 <= -150
and
CCI_14 > -200
```

or equivalently:

```text
-200 < CCI_14 <= -150
```

#### Plain-English version

> **CCI is materially depressed, but it has not reached the project's most severe downside threshold.**

Examples:

```text
CCI = -151
→ Buy

CCI = -175
→ Buy

CCI = -199.9
→ Buy
```

But:

```text
CCI = -200
→ Strong Buy
```

because `-200` belongs to the Strong Buy range.

---

### Neutral (0)

The primary Neutral range is:

```text
-150 < CCI_14 <= +150
```

Examples:

```text
CCI = -149
→ Neutral

CCI = 0
→ Neutral

CCI = +125
→ Neutral

CCI = +150
→ Neutral
```

The exact `+150` boundary remains Neutral.

That differs from the negative boundary:

```text
CCI = -150
→ Buy
```

This is the literal production boundary contract.

Neutral does **not** mean that CCI has no information.

It means:
> **The current CCI magnitude is not sufficiently extreme to receive one of the project's contrarian directional scores.**

A Neutral cell can still carry:

```text
CCI Divergence: Bullish
```

or:

```text
CCI Zero-Line Crossover: Uptrend Bias
```

because those are independent context layers.

---

### Sell (-1)

The rule is:

```text
CCI_14 > +150
and
CCI_14 < +200
```

or:

```text
+150 < CCI_14 < +200
```

#### Plain-English version

> **CCI is materially elevated relative to its recent norm, raising the risk that the move has become stretched.**

Examples:

```text
CCI = +151
→ Sell

CCI = +175
→ Sell

CCI = +199.9
→ Sell
```

But:

```text
CCI = +150
→ Neutral
```

and:

```text
CCI = +200
→ Strong Sell
```

---

### Strong Sell (-2)

The rule is:

```text
CCI_14 >= +200
```

#### Plain-English version

> **CCI is severely elevated relative to its recent statistical norm.**

- This is the upside counterpart of Strong Buy.

Again:
> **Severe overextension is not the same thing as confirmed reversal.**

- CCI can remain above `+200`.
- If it does, the primary state remains Strong Sell until it leaves that range.

---

### Why the Signal persists while CCI stays extreme

The primary CCI model is deliberately **state-based** rather than **entry-event based**.

Suppose CCI moves:

```text
Day 1: -165
Day 2: -184
Day 3: -214
Day 4: -226
Day 5: -207
Day 6: -188
```

The primary states are:

```text
Day 1: Buy
Day 2: Buy
Day 3: Strong Buy
Day 4: Strong Buy
Day 5: Strong Buy
Day 6: Buy
```

The app does not say:

```text
Strong Buy only on Day 3
```

simply because that was the first move through `-200`.

Why?

Because the primary Signal is answering:

> **How stretched is CCI now?**

not:

> **Did CCI cross an extreme threshold today?**

Event information belongs in separate context fields such as the zero-line crossover.

---

## CCI Divergence

CCI Divergence compares **confirmed price swings** with the CCI values observed at those same price pivots.

It is separate from the primary CCI score.

The app recognizes:

```text
Bullish
Bearish
None
```

after enough swing history exists to evaluate divergence.

---

### Divergence logic

| Divergence  | Price behavior                                                                        | CCI behavior                                                     | Basic interpretation                                                                                        |
| ----------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Bullish** | Newer confirmed price swing low is **lower** than the previous confirmed swing low    | CCI at the newer low is **higher** than CCI at the previous low  | **Price made a worse low, but CCI did not become equally weak. Downside momentum may be losing force.**     |
| **Bearish** | Newer confirmed price swing high is **higher** than the previous confirmed swing high | CCI at the newer high is **lower** than CCI at the previous high | **Price made a stronger high, but CCI did not become equally strong. Upside momentum may be losing force.** |
| **None**    | No qualifying confirmed divergence event                                              | —                                                                | **No new confirmed price/CCI divergence is present on this observation.**                                   |

The logic is:

```text
Bullish CCI Divergence
=
new price swing low < prior price swing low
AND
CCI at new swing low > CCI at prior swing low
```

and:

```text
Bearish CCI Divergence
=
new price swing high > prior price swing high
AND
CCI at new swing high < CCI at prior swing high
```

---

### Bullish CCI Divergence

Suppose price forms:

```text
Earlier confirmed low:
Price = $180
CCI   = -190
```

and later forms:

```text
New confirmed low:
Price = $172
CCI   = -155
```

Price did this:

```text
$180 → $172
```

so price made a:

```text
lower low
```

But CCI did this:

```text
-190 → -155
```

so CCI made a:

```text
higher reading
```

That is bullish divergence.

Beginner translation:
> **Price made a worse low, but CCI was less negative than before.**  
> **Price weakened, while downside momentum failed to weaken by the same amount.**

That can indicate that selling pressure is losing force.

It is a **bullish warning / rebound context**, not proof that price must rise next.

---

### Bearish CCI Divergence

Suppose price forms:

```text
Earlier confirmed high:
Price = $190
CCI   = +180
```

and later:

```text
New confirmed high:
Price = $198
CCI   = +115
```

Price did this:

```text
$190 → $198
```

so price made a:

```text
higher high
```

But CCI did this:

```text
+180 → +115
```

so CCI made a lower reading.

That is bearish divergence.

Beginner translation:
> **Price made a stronger high, but CCI was weaker than at the earlier high.**<br>
> **Price looks stronger, while upside momentum looks weaker.**

That is a bearish warning—not proof that a decline must begin.

---

### Divergence does not require CCI to be beyond ±150

CCI Divergence and the primary CCI Signal answer different questions.

A divergence event can occur while CCI is:

```text
Neutral
```

because divergence is based on the **relationship between two confirmed price swings and their corresponding CCI readings**, not on whether the latest reading exceeds a scoring threshold.

For example:

```text
Price high #1 = $190
CCI #1        = +120

Price high #2 = $195
CCI #2        = +80
```

can still be bearish divergence:

```text
price: higher high
CCI:   lower reading
```

even though neither CCI reading is above the project's `+150` Sell threshold.

This is deliberate.

Requiring every divergence to occur inside an extreme zone would change the meaning of divergence from:

> **price and momentum are separating**

to:

> **price and momentum are separating only when CCI is already extreme**

Those are different concepts.

The project keeps them separate.

---

### Why divergence appears two bars after the swing

A swing high or swing low cannot be known with certainty at the instant the candidate pivot occurs.

The project uses a **confirmed five-bar price pivot**.

For a candidate swing low at bar `t`, the Low at `t` must be lower than the two preceding Lows and the two subsequent Lows.

For a candidate swing high at `t`, the High at `t` must be higher than the two preceding Highs and the two subsequent Highs.

That means the app requires:

```text
t - 2
t - 1
t
t + 1
t + 2
```

before it can confirm that `t` was actually the swing.

Therefore:

```text
candidate pivot = t
confirmed pivot = t + 2
```

A divergence event is emitted at:

```text
t + 2
```

It is **not** painted backward onto `t`.

This delay is intentional.

> **The app waits until the swing was actually knowable rather than using future observations to make the historical heatmap look more accurate than it could have been in real time.**

---

### An actual AAPL divergence example

One production example from the CCI diagnostic used:

```text
AAPL CCI(14)

Earlier price pivot:
2026-01-08

New price pivot:
2026-01-20

Divergence confirmation:
2026-01-22
```

The corresponding values were approximately:

```text
Earlier price low = $255.70
Earlier CCI       = -198.75

New price low     = $243.42
New CCI           = -165.27
```

Price made:

```text
$255.70 → $243.42
```

a lower low.

CCI moved:

```text
-198.75 → -165.27
```

a higher reading.

So the app confirms:

```text
CCI Divergence: Bullish
```

on:

```text
2026-01-22
```

rather than retroactively coloring `2026-01-20`.

---

### `None` versus no value

Once enough confirmed swing history exists for divergence to be evaluated:

```text
CCI Divergence: None
```

means:

> **No new CCI divergence was confirmed on this observation.**

Before enough confirmed swing history exists, divergence can remain unavailable.

Those are different states.

An unavailable field means:

> **The app does not yet have enough confirmed swing history to evaluate this context properly.**

`None` means:

> **The context is evaluable, and no divergence event occurred here.**

---

## CCI Zero-Line Crossover

The zero line is CCI's central reference:

```text
CCI = 0
```

Unlike the ±150 / ±200 thresholds, it is **not an extreme threshold**.

It represents the point at which CCI moves from one side of its statistical center to the other.

The app tracks two event-only states:

```text
Uptrend Bias
Downtrend Bias
```

---

### Uptrend Bias

The event occurs when:

```text
Prior CCI <= 0
and
Current CCI > 0
```

Example:

```text
Prior CCI   = -18
Current CCI = +24
```

The app reports:

```text
CCI Zero-Line Crossover: Uptrend Bias
```

and the heatmap value receives:

```text
▲
```

so a value might display as:

```text
24.00 ▲
```

Beginner translation:

> **CCI has just moved from the non-positive side of its midpoint to the positive side. Shorter-term momentum bias has shifted upward.**

---

### Downtrend Bias

The event occurs when:

```text
Prior CCI >= 0
and
Current CCI < 0
```

Example:

```text
Prior CCI   = +12
Current CCI = -27
```

The app reports:

```text
CCI Zero-Line Crossover: Downtrend Bias
```

and the heatmap cell receives:

```text
▼
```

For example:

```text
-27.00 ▼
```

Beginner translation:

> **CCI has just moved from the non-negative side of its midpoint to the negative side. Shorter-term momentum bias has shifted downward.**

---

### Why equality belongs to the prior side

The production definitions are:

```text
prior <= 0 and current > 0
```

and:

```text
prior >= 0 and current < 0
```

So:

```text
Prior = 0
Current = +10
```

is an Uptrend Bias event.

And:

```text
Prior = 0
Current = -10
```

is a Downtrend Bias event.

But simply arriving at exactly zero is not itself a crossing.

For example:

```text
Prior = -15
Current = 0
```

does not yet qualify as Uptrend Bias.

The current value must actually move above zero.

---

### Zero-Line Crossover is an event, not a persistent state

Suppose CCI behaves like this:

```text
Day 1: -20
Day 2: +15
Day 3: +35
Day 4: +47
```

The Uptrend Bias event occurs only on:

```text
Day 2
```

because that is the observation where CCI crosses from the non-positive side to the positive side.

Days 3 and 4 remain above zero, but they are not new crossover events.

So:

```text
Day 2 → ▲
Day 3 → no glyph
Day 4 → no glyph
```

This is deliberately different from the primary CCI score, which persists as long as the current value remains inside the applicable extreme zone.

---

### Why zero crossing does not alter the primary score

Zero-line crossover measures **directional momentum transition**.

The primary Signal measures **statistical stretch**.

Those concepts can disagree.

Consider:

```text
CCI yesterday = -20
CCI today     = +25
```

Today produces:

```text
Signal: Neutral
CCI Zero-Line Crossover: Uptrend Bias
```

because `+25` is nowhere near the project's `+150` extreme threshold.

The app is saying:

> **CCI is not statistically extreme, but its immediate momentum bias has just shifted from negative to positive.**

That is useful information without changing the primary score.

---

## How to Read the CCI heatmap

A useful reading sequence is:

1. **Read the number.** How positive or negative is CCI?
2. **Read the color / Signal.** Is the current CCI reading materially or severely stretched?
3. **Check the font color.** Is there a newly confirmed Bullish or Bearish divergence?
4. **Look for ▲ or ▼.** Did CCI just cross its zero line?
5. **Open the hover.** Read Signal, CCI Divergence, and CCI Zero-Line Crossover together.
6. **Ask whether those layers agree or disagree.**

---

### What does the number in the heatmap cell mean?

The printed number is the **raw CCI value**.

It is not the score.

For example:

```text
-208.21
```

means the current CCI reading is approximately negative 208.

The Signal corresponding to that number is separately classified as:

```text
Strong Buy
```

because:

```text
CCI <= -200
```

---

### The number, background, font color, and glyph answer different questions

| Heatmap feature              | What it represents                   | Question it answers                                                      |
| ---------------------------- | ------------------------------------ | ------------------------------------------------------------------------ |
| **Printed CCI value**        | Raw CCI reading                      | **How far is CCI from its statistical center?**                          |
| **Cell background / Signal** | Five-state contrarian classification | **Is that reading normal, materially stretched, or severely stretched?** |
| **Blue / red number**        | Confirmed CCI divergence             | **Did price make a new swing extreme without CCI confirming it?**        |
| **▲ / ▼ glyph**              | Zero-line crossover event            | **Did CCI just cross through zero, and in which direction?**             |

That distinction is fundamental.

A cell can therefore contain:

```text
-208.21 ▼
```

with:

```text
green Strong Buy background
red number
```

without contradiction.

Each visual channel is describing something different.

---

### Actual AAPL example — July 31, 2026

The validated AAPL CCI(14) cell was approximately:

```text
CCI(14): -208.21 ▼
```

with:

```text
Signal: Strong Buy
CCI Divergence: Bearish
CCI Zero-Line Crossover: Downtrend Bias
```

The layers mean:

#### Primary Signal

```text
CCI = -208.21
```

is below:

```text
-200
```

so the current statistical stretch is severe:

```text
Strong Buy
```

#### Divergence

The divergence event is:

```text
Bearish
```

so the printed value is red.

That warns that the most recently confirmed price/CCI swing relationship contains bearish momentum disagreement.

#### Zero-line event

CCI also registered:

```text
Downtrend Bias
```

so the cell receives:

```text
▼
```

#### Combined interpretation

> **CCI is severely downside-stretched, which raises contrarian rebound potential. But the newly confirmed divergence and zero-line transition are bearish, so the latest secondary context has not confirmed that rebound thesis.**

This is precisely why the project keeps Signal, Divergence, and Zero-Line Crossover separate.

---

### Actual AAPL example — April 1, 2026

The validated AAPL CCI(20) cell was approximately:

```text
28.10 ▲
```

with:

```text
Signal: Neutral
CCI Divergence: Bullish
CCI Zero-Line Crossover: Uptrend Bias
```

The primary CCI value:

```text
+28.10
```

is well inside the project's Neutral range:

```text
-150 < CCI <= +150
```

so the background remains Neutral.

But:

```text
CCI Divergence: Bullish
```

makes the number blue, while:

```text
CCI Zero-Line Crossover: Uptrend Bias
```

adds:

```text
▲
```

Combined interpretation:

> **CCI itself is not extreme enough for a contrarian score, but price/CCI swing behavior is showing bullish divergence and CCI has just moved above its zero midpoint. Secondary momentum context is constructive even though the primary score remains Neutral.**

---

## Industry-standard baseline versus this project

### Conventional CCI foundation

CCI is conventionally centered around zero and is unbounded.

Common reference levels include:

```text
+100
-100
```

Readings beyond those levels are commonly used to identify unusually strong deviations from the indicator's recent norm.

CCI can be interpreted in more than one way in practice.

One approach treats strong positive readings as evidence of positive momentum and strong negative readings as evidence of negative momentum.

Another uses sufficiently large positive or negative readings as evidence that price has become stretched and may eventually mean-revert.

Divergence between price and CCI is also commonly used as momentum-warning context.

---

### Project-specific calibration

This project deliberately adopts a **contrarian five-state heatmap model**.

It differs from the basic conventional ±100 reference by requiring more extreme readings before changing the primary Signal:

```text
<= -200        Strong Buy
-200 to -150   Buy
-150 to +150   Neutral
+150 to +200   Sell
>= +200        Strong Sell
```

It also adds two separate context layers:

```text
CCI Divergence
CCI Zero-Line Crossover
```

The project's design therefore distinguishes:

```text
magnitude/extreme
from
swing disagreement
from
momentum midpoint transition
```

instead of forcing all three concepts into one score.

The five-state taxonomy:

```text
Strong Buy
Buy
Neutral
Sell
Strong Sell
```

and the exact `±150 / ±200` thresholds are **project-specific calibration**, not a claim that CCI has a universal industry five-state scoring system.

> **The project intentionally uses conventional CCI concepts without pretending that every useful CCI observation belongs inside the primary score.**

---



### Why ±100 still matters even though the app scores at ±150 / ±200

The conventional CCI reference zones are commonly associated with:

```text
+100
-100
```

Those remain useful visual reference levels.

But this project deliberately does **not** assign a Buy or Sell merely because CCI crosses ±100.

The primary score waits for larger deviations:

```text
-150
+150
```

before assigning the first contrarian directional state.

And it waits for:

```text
-200
+200
```

before assigning the Strong state.

The distinction is:

```text
±100
= conventional/reference level

±150
= project threshold for material extreme

±200
= project threshold for severe extreme
```

That means, for example:

```text
CCI = -125
```

can still be:

```text
Neutral
```

even though it is below the conventional `-100` reference line.

The project is effectively saying:

> **CCI is outside its commonly watched range, but not far enough outside it for this heatmap to assign a contrarian Buy state.**

This higher threshold is intentional.

It reduces the number of moderate ±100 excursions that the heatmap treats as actionable extremes.


## Strengths/Weaknesses
### Strengths

CCI is particularly useful in this implementation for:

* identifying unusually large positive and negative deviations from recent price behavior;
* distinguishing **material** stretch from **severe** stretch;
* filtering many ordinary ±100 excursions out of the primary directional score;
* preserving extreme states for as long as the extreme actually persists;
* identifying price/momentum disagreement through confirmed divergence;
* showing fresh zero-line momentum transitions without turning them into persistent score states;
* separating contrarian opportunity from momentum context;
* providing short-, medium-, and longer-horizon versions through CCI(10), CCI(14), and CCI(20).

---

### Limitations

##### CCI is unbounded

Unlike RSI or Stochastic, there is no hard maximum or minimum.

A value of:

```text
+250
```

does not mean CCI cannot rise to:

```text
+300
```

Likewise, a deeply negative CCI can become still more negative.

---

##### Extreme does not mean reversal

This is the most important limitation of the primary model.

```text
CCI <= -200
```

means:

> **severe downside stretch**

not:

> **price has bottomed**

Likewise:

```text
CCI >= +200
```

means:

> **severe upside stretch**

not:

> **price has topped**

Strong trends can remain statistically stretched.

---

##### A Strong state does not contain reversal confirmation

Unlike some reversal-confirmation oscillator models, CCI Strong Buy / Strong Sell in this project does not require:

```text
CCI rising
CCI falling
threshold crossback
divergence
zero-line crossover
```

Strong means:

> **more extreme**

not:

> **more confirmed**

---

##### Divergence is context, not the score

A Bearish divergence can appear while the primary Signal is:

```text
Strong Buy
```

A Bullish divergence can appear while the primary Signal is:

```text
Sell
```

That is possible because divergence and current CCI magnitude answer different questions.

> **Divergence warns that price and CCI are separating; it does not by itself declare that the primary CCI state is wrong.**

---

##### Confirmed divergence necessarily arrives later

The project waits for two subsequent observations before confirming a price pivot.

That means divergence appears at:

```text
pivot + 2 bars
```

rather than on the original swing date.

This introduces delay.

The tradeoff is that the app avoids back-painting a pivot using information that was not available at the time.

---

##### Zero-line crossover can be noisy

Crossing zero indicates a change in CCI's immediate directional bias.

But CCI can move back and forth across zero during choppy markets.

That is why zero crossing remains an event-only context field rather than automatically changing the primary score.

---

##### Different periods can legitimately disagree

CCI(10), CCI(14), and CCI(20) measure the same concept over different horizons.

For example:

```text
CCI(10) = Strong Buy
CCI(14) = Buy
CCI(20) = Neutral
```

is not necessarily inconsistent.

It can mean:

> **The very recent move is severely stretched, the intermediate move is materially stretched, and the longer-horizon deviation has not yet become extreme.**

---

## Beginner's checklist

When reading a CCI heatmap cell, ask these questions in order:

| Step  | Question                                                                                        |
| ----- | ----------------------------------------------------------------------------------------------- |
| **1** | What is the displayed CCI value?                                                                |
| **2** | Is it inside the Neutral range, materially extreme, or severely extreme?                        |
| **3** | What does the background / primary Signal say?                                                  |
| **4** | Is the number blue or red because a Bullish or Bearish divergence was just confirmed?           |
| **5** | Is there an `▲` or `▼`, indicating a zero-line crossover event?                                 |
| **6** | Do Signal, Divergence, and Zero-Line Crossover agree, or is one providing counter-context?      |
| **7** | Which CCI period am I looking at—10, 14, or 20—and therefore which horizon is being emphasized? |

The shortest useful summary is:

> **Signal = current stretch. Divergence = price/momentum disagreement. Zero-line crossover = momentum-bias transition.**

And one additional rule is worth remembering:

> **Strong means more extreme—not more certain.**

---

## Initial audit note

**Semantic type:** Contrarian / mean-reversion oscillator with independent divergence and zero-line context.

**Primary philosophy:** Identify meaningful and severe CCI extremes without treating ordinary ±100 excursions as automatic reversal signals.

**Numeric identity:**

```text
Typical Price = (High + Low + Close) / 3

CCI =
(Typical Price - average Typical Price)
/
(0.015 × Mean Deviation)
```

Configured project periods:

```text
10 / 14 / 20
```

**Primary scoring vocabulary:**

```text
+2  Strong Buy
+1  Buy
 0  Neutral
-1  Sell
-2  Strong Sell
```

**Primary thresholds:**

```text
CCI <= -200            Strong Buy
-200 < CCI <= -150     Buy
-150 < CCI <= +150     Neutral
+150 < CCI < +200      Sell
CCI >= +200            Strong Sell
```

**Primary state model:** Persistent current-level classification. No lag or threshold-entry requirement.

**Conventional reference levels:** `±100` remain useful chart/reference levels but do not independently trigger the project's Buy/Sell states.

**CCI Divergence:** Independent context using confirmed five-bar price pivots and the same CCI series sampled at corresponding pivot dates. Events are emitted on confirmation at `t+2`, not back-painted.

**Bullish divergence:**

```text
newer price low < prior price low
and
newer CCI > prior CCI
```

**Bearish divergence:**

```text
newer price high > prior price high
and
newer CCI < prior CCI
```

**CCI Zero-Line Crossover:** Independent event-only context.

```text
prior CCI <= 0 and current CCI > 0
→ Uptrend Bias ▲

prior CCI >= 0 and current CCI < 0
→ Downtrend Bias ▼
```

**Display-versus-scoring distinction:**

```text
raw number
→ current CCI value

background color
→ primary five-state Signal

blue/red number
→ Bullish/Bearish confirmed divergence

▲ / ▼
→ zero-line crossover event
```

**Verification status:** The adopted CCI implementation completed rule-contract verification, warmup verification, production-path context verification, adapter/UI structural verification, and manual acceptance across the Rolling Heatmap, SCD Multiple Indicators, and SCD Single Indicator views. Date-specific AAPL checks also confirmed combined Signal / Divergence / Zero-Line presentation.

---

## References

### External conceptual references

* **TradingView — Commodity Channel Index (CCI):** conventional CCI construction, centered-zero behavior, ±100 reference levels, and divergence interpretation.
* **StockCharts — Commodity Channel Index (CCI):** CCI momentum interpretation, zero-line behavior, extreme readings, and practical use of threshold filtering.

### Project references

* `src/config/master_rules_normalized.json` — primary CCI five-state scoring rules and project thresholds.
* `src/calculations/indicator_preprocessor.py` — CCI numeric computation.
* `src/calculations/signal_classifier.py` — five-state classification and CCI missing/warmup handling.
* `src/calculations/technical.py` — CCI rolling transport, confirmed divergence, and zero-line crossover context.
* `src/ui/rolling_heatmap_adapter.py` — CCI value formatting, divergence font overlay, zero-line glyphs, and hover presentation.
* `streamlit_app.py` — Rolling Heatmap / SCD consumer integration.

---

# My Notes: CCI

Measures deviation from average price, typically oscillating around 0.

**CCI** stands for **Commodity Channel Index**. Despite the name, it is used across stocks, ETFs, commodities, and other instruments.

CCI measures how far price is from its recent average, adjusted by the typical amount of deviation.
- In practical terms, it tells you whether price is unusually high or unusually low relative to its recent normal behavior.

---

**Purpose:** Identify cyclical turns and measure how far price deviates from its statistical average to spot potential reversal points.

**Use when:** You want to identify when prices are extremely stretched from their normal range, particularly in commodity or cyclical markets.

**Key Concept:** Measures how current price compares to average price over a period, scaled by standard deviation. Assumes prices oscillate around a central tendency and extreme deviations tend to revert.

**Calculation:** `CCI = (Typical Price - SMA of Typical Price) ÷ (0.015 × Mean Deviation)`, where `Typical Price = (High + Low + Close) ÷ 3`.

**Signals & Interpretation:**
Measures deviation from average price, typically oscillating around 0.

- Values between `-100` and `+100` are often treated as a normal/neutral range.
- Above +100 = overbought conditions
    - price is unusually strong relative to its recent average.
- Below -100 = oversold conditions
    - price is unusually weak relative to its recent average.
- Above +200 = extremely overbought
- Below -200 = extremely oversold
    - More extreme values suggest stronger deviation from normal.

- Zero line crossings indicate momentum shifts
- Divergences suggest potential trend reversals

**Optimal Conditions:** Originally designed for commodities but works well in any market. Most effective in ranging markets and for identifying extreme price moves.

**Limitations:** Unbounded oscillator can stay in extreme territory longer than expected. May produce false signals in strongly trending markets.

**Complexity Level:** Intermediate
