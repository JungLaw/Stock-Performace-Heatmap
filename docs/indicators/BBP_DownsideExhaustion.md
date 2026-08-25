## Summary: BBP Downside Exhaustion signals

**Class:** Momentum Indicators
**Scope:** Exhaustion Signals
**Family:** BullBearPower

BBP Downside Exhaustion is a **rebound-risk / selling-pressure exhaustion indicator**.

It does **not** ask:

> “Is the stock bullish?”

It asks:

> **“Inside an already-established decline, has selling pressure become unusually persistent and severe?”**

The app uses only two states:

| Signal                       | Literal trigger                                                                                                                          | Layman’s translation                                                                            | Rule logic                                                                          | Bottom-line                                                                        |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Downside Exhaustion (+2)** | Qualified falling EMA trend + BBP below zero + BBP falling for 3 consecutive intervals + 3-bar BBP decline greater than `0.50 × ATR(14)` | The stock is already in a meaningful decline, and selling pressure has become unusually intense | Bearish trend gate + negative pressure + persistence + volatility-adjusted severity | **The selloff may be stretched enough that rebound risk deserves more attention.** |
| **None (0)**                 | The full Downside Exhaustion rule is not satisfied                                                                                       | One or more required pieces are missing                                                         | Valid observation without the complete exhaustion pattern                           | **No Downside Exhaustion condition is active.**                                    |

> **Important:** `Downside Exhaustion` is **not a Buy signal, not a reversal confirmation, and not a prediction that price must bounce next.**
>
> It means the decline has become sufficiently persistent and severe that the **risk of a rebound is elevated relative to an ordinary bearish move**.

---
### The shortest useful explanation

The indicator is looking for **two things at the same time**:
1. **The stock is genuinely in a bearish trend.**
2. **Selling pressure inside that trend has become unusually severe.**


The following table explains what the **BBP pair and EMA pair mean when read together**.

| BBP pressure over 3 bars | EMA trend over 5 bars  | Interpretation                                                                                       |
| ------------------------ | ---------------------- | ---------------------------------------------------------------------------------------------------- |
| **BBP ↓ sharply**        | **EMA ↓ meaningfully** | **Downside Exhaustion candidate.** Selling pressure has become severe inside an established decline. |
| **BBP ↓ sharply**        | EMA flat or ↑          | Selling pressure worsened sharply, but the required bearish-trend backdrop is missing.               |
| Mild BBP ↓               | **EMA ↓ meaningfully** | Trend is bearish, but selling pressure has not become severe enough to qualify as exhausted.         |
| **BBP ↑ improving**      | **EMA ↓ meaningfully** | The broader trend remains bearish, but selling pressure is easing rather than intensifying.          |
| **BBP ↑ improving**      | EMA flat or ↑          | Neither half of the Downside Exhaustion thesis is present.                                           |

The easiest mental model is:
- **EMA** tells you whether the stock is genuinely in a decline.
- **BBP** tells you whether the selling pressure inside that decline has become unusually intense.
- **Downside Exhaustion** requires both.


---

## A brief overview

### Why this indicator exists

The primary Bull Bear Power indicator answers a directional question:

> **Who currently has control, and does that pressure agree with a meaningful EMA trend?**

BBP Downside Exhaustion answers a different question:

> **Has bearish pressure become so persistent and severe that continuing to chase the decline may carry greater rebound risk?**

That distinction matters.

A stock can be:

```text
Primary BBP: Bearish Confirmation
BBP Downside Exhaustion: Downside Exhaustion
```

without contradiction.

The first says:

> **Sellers currently have strong directional control.**

The second says:

> **That selling pressure has also become unusually stretched.**

Both can be true at the same time.

---

### What the indicator uses

For each configured period `p`, the rule uses:

```text
EMA(p)
BBP(p)
ATR(14)
```

The active periods are:

```text
10
13
21
```

The core rule structure is the same for all three.

Conceptually:

```text
EMA has fallen enough to prove a bearish trend
AND
BBP is below zero
AND
BBP has fallen for three consecutive intervals
AND
the 3-bar BBP decline is greater than 0.50 × ATR(14)
```

The rulebook stores this as a standalone semantic family rather than overwriting the primary BullBearPower score stream. That separation was intentional because exhaustion and directional control are different concepts.

---

### Why EMA matters

The EMA is the **trend filter**.

Without it, the indicator could mistake a short burst of selling pressure for exhaustion even when the broader trend is flat or rising.

The rule therefore asks:

> **Has the EMA itself fallen enough over five bars to prove that this is a meaningful bearish trend?**

The required condition is:

```text
EMA five bars ago - EMA now > 0.25 × ATR(14)
```

In plain English:

> **The EMA must have declined by more than one quarter of the stock’s recent typical trading range over five bars.**

#### Why do we want the EMA lower?

Because the purpose of this indicator is **not** to detect every sudden BBP drop.

It is specifically looking for:

> **severe selling pressure inside an established decline**

rather than:

> a temporary bad day inside a flat or rising market.

The EMA therefore answers:

> **“Is there actually a bearish trend here?”**

---

### Why BBP matters

BBP supplies the **pressure component**.

Recall:

```text
Bull Power = High - EMA
Bear Power = Low - EMA
BBP = Bull Power + Bear Power
```

A negative BBP means the combined buying-versus-selling pressure is on the bearish side of zero.

But Downside Exhaustion requires more than simply:

```text
BBP < 0
```

It also asks:

1. Has BBP kept deteriorating?
2. Has that deterioration become unusually large?

So the BBP portion answers:

> **“Is selling pressure merely bearish, or has it become unusually severe?”**

---

### Why ATR(14) matters

A raw move such as:

```text
BBP fell by 10 points
```

does not mean the same thing for every stock.

For a quiet stock, 10 points could be enormous.

For a volatile stock, 10 points might be ordinary.

ATR(14) provides a volatility reference.

So instead of asking only:

> “How much did BBP fall?”

the rule also asks:

> **“How large was that decline compared with how much this stock normally moves?”**

That is why the hover shows both:

```text
raw move
AND
move relative to ATR(14)
```

They are **two views of the same movement**, not two separate events.

---
## BBP Downside Exhaustion Rule Translation

The three variants use the same structure. The examples below use **BBP Exh (13)**.

### Downside Exhaustion (+2)

The rule is:

```text
lag(EMA_13, 5) - EMA_13 > 0.25 * ATR_14
and BBP_13 < 0
and falling_2bar(BBP_13, 3)
and lag(BBP_13, 3) - BBP_13 > 0.50 * ATR_14
```

Every condition is connected with `and`.

That means **all four conditions must be true at the same time**.

---

### Clause 1 — establish a meaningful bearish EMA trend

```text
lag(EMA_13, 5) - EMA_13 > 0.25 * ATR_14
```

#### Literal meaning

Compare EMA(13) five bars ago with EMA(13) now.

If:

```text
EMA five bars ago > EMA now
```

then the EMA has declined.

The decline must be greater than:

```text
0.25 × ATR(14)
```

#### Why this clause exists

This is the **trend gate**.

It prevents a sudden BBP deterioration from being classified as Downside Exhaustion when the broader EMA trend is not meaningfully bearish.

#### Plain-English version

> **The underlying trend must already be falling enough to matter.**

---

### Clause 2 — require current bearish pressure

```text
BBP_13 < 0
```

#### Literal meaning

Combined BBP must be below zero.

#### Why this clause exists

A Downside Exhaustion condition should represent **bearish pressure**, not merely a large historical change that happens to end above zero.

#### Plain-English version

> **Selling pressure must currently have the advantage.**

---

### Clause 3 — require persistent deterioration

```text
falling_2bar(BBP_13, 3)
```

For this rule, that means:

```text
BBP[t] < BBP[t-1] < BBP[t-2] < BBP[t-3]
```

BBP has fallen on three consecutive intervals.

#### Why this clause exists

A single large BBP decline could be a one-bar shock.

The rule is looking for **persistent pressure deterioration**, not merely one sudden move.

#### Plain-English version

> **Selling pressure must have been getting worse repeatedly, not just once.**

---

### Clause 4 — require unusual severity

```text
lag(BBP_13, 3) - BBP_13 > 0.50 * ATR_14
```

#### Literal meaning

Calculate the total BBP decline from three bars ago to now:

```text
BBP three bars ago - BBP now
```

Then require that decline to exceed:

```text
0.50 × ATR(14)
```

#### Why this clause exists

Persistence alone does not prove that the deterioration is unusually large.

BBP could fall slightly for three intervals:

```text
-2.0
-2.2
-2.4
-2.6
```

That is persistent, but may not be severe.

This clause asks whether the total deterioration is **large relative to the stock’s normal volatility**.

#### Plain-English version

> **Selling pressure must not only keep worsening—it must worsen by enough to be unusual for this stock.**

---

### Literal summary

Downside Exhaustion requires:

```text
meaningful bearish EMA trend
+
negative BBP
+
three consecutive BBP declines
+
3-bar BBP decline > 0.50 × ATR(14)
```

### Plain-English version

> **The stock is already in a meaningful decline, selling pressure is bearish, that pressure has worsened repeatedly for three intervals, and the total deterioration is unusually large relative to normal volatility.**

### Interpretation

That combination is treated as:

```text
Downside Exhaustion
```

because the move may have become **stretched**.

It does **not** say:

```text
the downtrend has ended
```

or:

```text
price must reverse now
```

It says:

> **The decline has become severe enough that rebound risk deserves more attention than it would during an ordinary bearish move.**

---

### None (0)

`None` means the complete Downside Exhaustion structure is not active.

One or more of the following may be missing:

* EMA trend is not bearish enough;
* BBP is not below zero;
* BBP has not declined for three consecutive intervals;
* total BBP deterioration does not exceed `0.50 × ATR(14)`.

`None` does **not** mean:

* the stock is bullish;
* selling pressure is absent;
* the primary BBP Signal cannot be Bearish.

For example:

```text
Primary BBP: Bearish
BBP Downside Exhaustion: None
```

can simply mean:

> **The trend/pressure regime is bearish, but the selloff has not become severe enough to meet the exhaustion test.**


---
## The 3 BBP Downside Exhaustion variants

| Variant          | Period | Horizon     | Evidence status                                                    |
| ---------------- | -----: | ----------- | ------------------------------------------------------------------ |
| **BBP Exh (10)** |     10 | Short term  | **Provisional observational variant**                              |
| **BBP Exh (13)** |     13 | Medium term | **Empirically supported candidate from the production diagnostic** |
| **BBP Exh (21)** |     21 | Long term   | **Provisional observational variant**                              |

The 10- and 21-period versions use the same structural rule as the 13-period version, but they were added so their behavior can be observed rather than because their rebound behavior has already been independently validated.

The 13-period version is the one included in the default Custom set; the 10- and 21-period variants remain selectable through the BullBearPower family and the corresponding Momentum presets.

---

## (HTR) Understanding the BBP Downside Exhaustion Hover

This hover is especially important because the four exhaustion-specific fields tell you **why** the condition did or did not trigger.

A typical hover includes:

```text
Value: XX.XX | Price: XXX.XX
Δ vs prior day: ... | Price: ...
Trend: ... | Price: ...

Signal: Downside Exhaustion

3-bar BBP move: ↓ XX.XX
3-bar BBP decline / ATR14: X.XX×
5-bar EMA move: ↓ XX.XX
5-bar EMA decline / ATR14: X.XX×
```

The four specialized fields are easier to understand if you treat them as **two pairs**.

---

### The two questions behind the four hover fields

| Question                                          | Raw field        | Volatility-adjusted field   |
| ------------------------------------------------- | ---------------- | --------------------------- |
| **Has selling pressure become unusually severe?** | `3-bar BBP move` | `3-bar BBP decline / ATR14` |
| **Is the broader trend genuinely falling?**       | `5-bar EMA move` | `5-bar EMA decline / ATR14` |

This is the conceptual heart of the hover.

> **BBP tells you what selling pressure is doing. EMA tells you whether that selling pressure is happening inside a real bearish trend.**

---

## Part 1 — Has selling pressure become unusually severe?

### Why BBP is the focus here

BBP measures the balance of buying and selling pressure relative to the EMA.

For Downside Exhaustion, the question is not merely:

> “Is BBP negative?”

The more important question is:

> **“Has selling pressure become much worse over a short period?”**

That is what the first two specialized hover fields describe.

---

### `3-bar BBP move`

Example:

```text
3-bar BBP move: ↓ 30.11
```

The arrow gives the direction.

```text
↓ = BBP moved downward
↑ = BBP moved upward
→ = no net change
```

So:

```text
↓ 30.11
```

means:

> **BBP is 30.11 points lower than it was three bars ago.**

Because lower BBP represents deterioration in the combined pressure balance, the beginner translation is:

> **Selling pressure became substantially worse over the three-bar comparison.**

If the field instead shows:

```text
3-bar BBP move: ↑ 4.20
```

then BBP increased by 4.20 points.

That means:

> **Selling pressure eased rather than intensified over the comparison.**

The arrow convention is display-only. The underlying rule math remains based on:

```text
BBP[t-3] - BBP[t]
```

---

### `3-bar BBP decline / ATR14`

Example:

```text
3-bar BBP decline / ATR14: 3.91×
```

This takes the same three-bar BBP deterioration and divides it by ATR(14).

The question is:

> **Was that deterioration large compared with this stock’s normal price movement?**

A reading of:

```text
3.91×
```

means:

> **The BBP deterioration was equal to 3.91 times one ATR(14).**

You can also think of it as:

> **391% of one ATR.**

The rule requires:

```text
> 0.50×
```

So:

```text
3.91×
```

is far beyond the minimum exhaustion threshold.

If BBP rose instead of fell, the ratio can be negative:

```text
3-bar BBP move: ↑ 4.20
3-bar BBP decline / ATR14: -0.54×
```

Those two fields agree.

The first says:

> BBP increased.

The second says:

> Therefore there was no positive BBP decline magnitude to qualify toward the exhaustion threshold.

---

### Raw BBP move versus ATR-adjusted BBP decline

These are **not two different events**.

They are two ways of viewing the same BBP movement.

| Field                                | What it adds                                                         |
| ------------------------------------ | -------------------------------------------------------------------- |
| **3-bar BBP move: ↓ 30.11**          | Actual movement in BBP's own price-related units                     |
| **3-bar BBP decline / ATR14: 3.91×** | How unusual that same deterioration is relative to recent volatility |

The raw value gives the movement **color and scale**.

The ATR ratio gives the movement **context**.

---

## Part 2 — Is the broader trend genuinely falling?

### Why EMA is part of an exhaustion signal

A sudden pressure collapse is not enough by itself.

Imagine BBP falling sharply while the EMA is still:

```text
flat
```

or:

```text
rising
```

That could be a temporary shock inside a non-bearish environment.

Downside Exhaustion is intended to identify **extreme selling inside an existing decline**.

So the EMA pair asks:

> **“Is this pressure deterioration occurring inside a genuine bearish trend?”**

---

### `5-bar EMA move`

Example:

```text
5-bar EMA move: ↓ 10.64
```

This means:

> **The EMA is 10.64 price units lower than it was five bars ago.**

That is useful because it tells you the actual size of the trend movement.

Why do we want this value to point downward?

Because the rule is specifically asking for:

> **a bearish trend backdrop**

before interpreting severe BBP deterioration as Downside Exhaustion.

If the hover instead shows:

```text
5-bar EMA move: ↑ 1.85
```

the EMA rose over five bars.

That would work against the bearish-trend requirement.

---

### `5-bar EMA decline / ATR14`

Example:

```text
5-bar EMA decline / ATR14: 1.38×
```

This answers:

> **Is the EMA decline large enough to count as meaningful relative to normal volatility?**

The rule requires:

```text
> 0.25×
```

A reading of:

```text
1.38×
```

means the EMA declined by an amount equal to **1.38 times ATR(14)**.

That is comfortably beyond the trend threshold.

If the EMA rose:

```text
5-bar EMA move: ↑ 1.85
5-bar EMA decline / ATR14: -0.24×
```

the negative ratio confirms that there was no qualifying five-bar EMA decline.

---

### Raw EMA move versus ATR-adjusted EMA decline

Again, these are two views of the same movement.

| Field                                | What it adds                                                       |
| ------------------------------------ | ------------------------------------------------------------------ |
| **5-bar EMA move: ↓ 10.64**          | Actual amount the EMA moved lower                                  |
| **5-bar EMA decline / ATR14: 1.38×** | How significant that same decline is relative to recent volatility |

The raw field tells you:

> **How far did the trend baseline move?**

The ratio tells you:

> **Was that movement large enough to matter for this stock?**

---

## The four hover fields together

The first table explains each field individually.

The following table explains what the **BBP pair and EMA pair mean when read together**.

| BBP pressure over 3 bars | EMA trend over 5 bars  | Interpretation                                                                                       |
| ------------------------ | ---------------------- | ---------------------------------------------------------------------------------------------------- |
| **BBP ↓ sharply**        | **EMA ↓ meaningfully** | **Downside Exhaustion candidate.** Selling pressure has become severe inside an established decline. |
| **BBP ↓ sharply**        | EMA flat or ↑          | Selling pressure worsened sharply, but the required bearish-trend backdrop is missing.               |
| Mild BBP ↓               | **EMA ↓ meaningfully** | Trend is bearish, but selling pressure has not become severe enough to qualify as exhausted.         |
| **BBP ↑ improving**      | **EMA ↓ meaningfully** | The broader trend remains bearish, but selling pressure is easing rather than intensifying.          |
| **BBP ↑ improving**      | EMA flat or ↑          | Neither half of the Downside Exhaustion thesis is present.                                           |

This is the central coordination rule:
- **EMA** tells you whether the stock is genuinely in a decline.
- **BBP** tells you whether the selling pressure inside that decline has become unusually intense.
- **Downside Exhaustion** requires both.

---

## A concrete hover example

The following is a verified production example:

```text
Signal: Downside Exhaustion

3-bar BBP move: ↓ 30.11
3-bar BBP decline / ATR14: 3.91×
5-bar EMA move: ↓ 10.64
5-bar EMA decline / ATR14: 1.38×
```

### Step 1 — read the BBP move

```text
3-bar BBP move: ↓ 30.11
```

BBP moved downward by **30.11 points over three bars**.

That tells you:

> **The buying-versus-selling pressure balance deteriorated sharply.**

Selling pressure did not merely remain bearish; it became materially worse.

### Step 2 — put that BBP move in volatility context

```text
3-bar BBP decline / ATR14: 3.91×
```

That same deterioration was equal to **3.91 times ATR(14)**.

The rule requires only:

```text
0.50×
```

So the measured deterioration was nearly **eight times the minimum required severity threshold**:

```text
3.91 / 0.50 ≈ 7.82
```

In plain English:

> **The deterioration in selling pressure was not marginal—it was extremely large relative to the stock's normal recent movement.**

### Step 3 — read the EMA move

```text
5-bar EMA move: ↓ 10.64
```

The EMA itself fell by **10.64 price units over five bars**.

That matters because the indicator does not want to flag a brief selling shock inside a flat or rising trend.

The EMA is telling us:

> **The broader price baseline is genuinely moving lower.**

### Step 4 — put the EMA move in volatility context

```text
5-bar EMA decline / ATR14: 1.38×
```

The five-bar EMA decline measured **1.38 times ATR(14)**.

The rule requires:

```text
0.25×
```

So the bearish trend qualification was comfortably satisfied.

### Put everything together

The hover is telling you:

> **The stock is already in a meaningful decline. The EMA fell by 10.64 price units over five bars, equal to 1.38× ATR(14). At the same time, BBP deteriorated by 30.11 points over three bars, equal to 3.91× ATR(14).**

That is why the app displays:

```text
Signal: Downside Exhaustion
```

The appropriate interpretation is:

> **The trend remains bearish, but selling pressure has become unusually persistent and severe. The selloff may now be stretched enough that rebound risk deserves additional attention.**

It does **not** mean:

> “Buy now.”

It does **not** mean:

> “The bottom is in.”

It means:

> **Be more cautious about assuming that an already-severe decline can continue at the same pace without interruption.**

---

## What an improving hover can look like

Suppose instead the hover shows:

```text
Signal: None

3-bar BBP move: ↑ 4.20
3-bar BBP decline / ATR14: -0.54×
5-bar EMA move: ↓ 2.40
5-bar EMA decline / ATR14: 0.31×
```

The EMA still satisfies the bearish trend gate:

```text
0.31× > 0.25×
```

But BBP is moving upward rather than downward.

Translation:

> **The broader trend remains bearish, but selling pressure is currently easing rather than intensifying.**

That is a very different condition from Downside Exhaustion.

It demonstrates why the indicator needs both the EMA pair and BBP pair.

---

## What if both BBP and EMA are rising?

Example:

```text
Signal: None

3-bar BBP move: ↑ 5.80
3-bar BBP decline / ATR14: -0.72×

5-bar EMA move: ↑ 1.90
5-bar EMA decline / ATR14: -0.24×
```

Here:

* BBP is improving;
* EMA is rising;
* neither the severe-pressure condition nor the bearish-trend condition is present.

The Downside Exhaustion thesis is therefore absent.

---

## How to read the BBP Downside Exhaustion heatmap

A useful sequence is:

1. **Read the cell value.**
2. **Read Signal.**
3. **Check the BBP pair.**
4. **Check the EMA pair.**
5. **Decide whether the two stories agree.**
6. **Compare with primary BBP for directional context.**

---

### What does the number in the heatmap cell mean?

The number printed in a BBP Downside Exhaustion cell is the **underlying BBP value** for that period.

It is **not** the binary score.

For:

```text
BBP Exh (13)
```

the displayed value is the underlying:

```text
BBP(13)
```

value.

So a cell might display:

```text
-18.42
```

while the color represents:

```text
+2 = Downside Exhaustion
```

The printed number and color answer different questions:

| Heatmap feature        | Meaning                                             |
| ---------------------- | --------------------------------------------------- |
| **Printed BBP value**  | Current underlying pressure value                   |
| **Cell color / score** | Whether the full Downside Exhaustion rule is active |

---

## Why a negative BBP is not enough

Suppose:

```text
BBP = -20
```

That tells you bearish pressure is currently substantial.

But that alone does not prove exhaustion.

The rule still needs to know:

* Is the EMA trend meaningfully bearish?
* Has BBP worsened persistently?
* Is the three-bar deterioration unusually large relative to ATR?

So:

> **Negative BBP tells you sellers have the pressure advantage. Downside Exhaustion tells you that bearish pressure has become unusually persistent and severe inside a qualified decline.**

Those are different levels of information.

---

## Relationship to primary BBP

Primary BBP and Downside Exhaustion should be read together when both are available.

| Primary BBP                        | Downside Exhaustion     | Interpretation                                                                                                                                                                                                     |
| ---------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Bearish Confirmation**           | **Downside Exhaustion** | Sellers have recently taken clear control, but pressure is also unusually stretched. **Bearish direction + elevated rebound risk.**                                                                                |
| **Bearish**                        | **Downside Exhaustion** | Bearish regime remains active while pressure severity has reached exhaustion criteria.                                                                                                                             |
| **Bearish**                        | **None**                | Trend/pressure regime is bearish, but severity has not reached exhaustion conditions.                                                                                                                              |
| **Neutral**                        | **Downside Exhaustion** | The standalone exhaustion structure is active even though the primary five-state directional regime is not currently classifying the observation as Bearish. Inspect the hover rather than assuming contradiction. |
| **Bullish / Bullish Confirmation** | **None**                | Normal case: downside-exhaustion conditions are absent.                                                                                                                                                            |

The most important case is:

```text
Primary BBP: Bearish
or
Primary BBP: Bearish Confirmation

AND

BBP Downside Exhaustion: Downside Exhaustion
```

Beginner translation:

> **Sellers still control the direction, but the selloff may have become stretched.**

That does **not** mean the primary bearish Signal is wrong.

It means:

> **Directional control and exhaustion risk are two different questions.**

---

## Industry concept versus project-specific model

The underlying Bull Power, Bear Power, EMA, and ATR concepts are conventional technical-analysis building blocks.

However:

```text
BBP Downside Exhaustion
```

as implemented here is a **project-specific derived semantic model**.

It is not presented as a standard Elder-Ray signal with universally accepted thresholds.

In particular, these thresholds are project rules:

```text
5-bar EMA decline > 0.25 × ATR(14)

3-bar BBP decline > 0.50 × ATR(14)
```

along with:

```text
BBP < 0
three consecutive BBP declines
```

The model was adopted because production-path diagnostics indicated that the severe downside condition behaved more like **downside exhaustion / rebound-risk context** than like an ordinary “Strong Sell” continuation state.

That empirical finding is why the condition was separated from the primary BBP directional regime rather than left as the strongest bearish score.

---

## Evidence status by period

The three variants should not be assumed to have equal empirical support.

### BBP Exh (13)

**Status:** Empirically supported candidate.

The medium-term 13-period version was the principal production-diagnostic case supporting the exhaustion interpretation.

This is the variant included in the default Custom set.

### BBP Exh (10)

**Status:** Provisional observational variant.

The same structural rule is applied to the faster 10-period BBP/EMA pair so its behavior can be observed.

It has **not** been independently validated as having the same rebound behavior as the 13-period model.

### BBP Exh (21)

**Status:** Provisional observational variant.

The same structural rule is applied to the slower 21-period BBP/EMA pair.

It likewise has **not** been independently validated as having the same rebound behavior as the 13-period version.

That distinction is deliberate:

> **UI availability does not imply equal evidentiary support.**

---

## Strengths

BBP Downside Exhaustion is useful because it combines several ideas that are weak in isolation:

* a meaningful bearish trend;
* currently negative pressure;
* persistent deterioration;
* volatility-adjusted severity.

It can help distinguish:

```text
ordinary bearish pressure
```

from:

```text
bearish pressure that has become unusually stretched
```

It is particularly useful as:

* a rebound-risk warning;
* a “do not blindly chase” context signal;
* a companion to primary BBP;
* a way to identify unusually severe selling pressure relative to the security's own volatility.

---

## Limitations

### Exhaustion does not mean reversal

This is the most important limitation.

A severe decline can become even more severe.

`Downside Exhaustion` therefore means:

> **rebound risk has increased**

not:

> **a rebound is guaranteed**

---

### It is not an oversold scale

BBP is unbounded.

There is no universal BBP value that means:

```text
oversold
```

The model instead defines exhaustion through:

```text
trend
+
sign
+
persistence
+
ATR-adjusted severity
```

---

### The raw BBP move is not directly comparable across all stocks

A raw:

```text
↓ 20
```

can mean very different things for different securities.

That is why the hover also supplies:

```text
3-bar BBP decline / ATR14
```

The ratio is more useful for understanding whether the move is large relative to that instrument's own volatility.

---

### The raw EMA move is also price-scale dependent

A:

```text
↓ 5
```

five-bar EMA move can be enormous for one stock and trivial for another.

Again, the ATR-normalized ratio supplies context.

---

### The four hover fields are not four independent signals

They are two movements shown in two forms:

```text
BBP move
├─ raw move
└─ ATR-adjusted size

EMA move
├─ raw move
└─ ATR-adjusted size
```

Do not count them as four separate confirmations.

---

### ST and LT variants remain provisional

BBP Exh (10) and BBP Exh (21) exist for observation.

Their inclusion should not be interpreted as proof that they have the same rebound characteristics as BBP Exh (13).

---

## Beginner's checklist

When reading a BBP Downside Exhaustion cell:

| Step  | Question                                                                                   |
| ----- | ------------------------------------------------------------------------------------------ |
| **1** | What does `Signal` say—Downside Exhaustion or None?                                        |
| **2** | Is `3-bar BBP move` pointing down or up?                                                   |
| **3** | How large is the BBP move relative to ATR(14)?                                             |
| **4** | Is `5-bar EMA move` pointing down or up?                                                   |
| **5** | Is the EMA decline greater than `0.25× ATR(14)`?                                           |
| **6** | Are both stories present: genuine bearish trend **and** unusually severe selling pressure? |
| **7** | What does primary BBP say about current directional control?                               |

The shortest useful summary is:

> **EMA = Is the decline real?**
> **BBP = Has selling pressure become unusually severe?**
> **Downside Exhaustion = Both are true strongly enough to raise rebound risk.**

---

## Initial audit note

**Semantic type:** Binary downside-exhaustion / rebound-risk context signal.

**Primary philosophy:** Contrarian exhaustion context, not bearish continuation scoring.

**Underlying displayed value:** Existing combined BBP numeric series for the matching period.

**Configured periods:**

```text
10 / 13 / 21
```

**Binary display vocabulary:**

```text
+2  Downside Exhaustion
 0  None
```

The generic internal classifier still maps the active event through its normal `strong_buy → +2` score channel, but the user-facing label is deliberately:

```text
Downside Exhaustion
```

rather than:

```text
Strong Buy
```

because the condition represents **rebound-risk context**, not a literal trade instruction.

**Trend gate:**

```text
EMA five bars ago - EMA now > 0.25 × ATR(14)
```

**Pressure requirements:**

```text
BBP < 0

BBP[t] < BBP[t-1] < BBP[t-2] < BBP[t-3]

BBP[t-3] - BBP[t] > 0.50 × ATR(14)
```

**Hover context:**

```text
3-bar BBP move
3-bar BBP decline / ATR14
5-bar EMA move
5-bar EMA decline / ATR14
```

The raw move fields use intuitive arrows:

```text
↓ = underlying series declined
↑ = underlying series increased
→ = unchanged
```

while the normalized decline ratios preserve their signed mathematical values.

**Evidence status:** BBP Exh (13) is the empirically supported candidate from the production diagnostic. BBP Exh (10) and BBP Exh (21) are provisional observational variants.

**Isolation from primary BBP:** Downside Exhaustion has an independent semantic score identity while reusing the existing period-specific BBP numeric series for display.

**Elder-Ray isolation:** The exhaustion rows do not inherit primary BBP's Elder-Ray Setup or Divergence hover context.

**Verification status:** The implementation passed independent production/oracle score equivalence, warmup checks, full-history context arithmetic, rolling-payload transport, adapter presentation checks, manual validation across Rolling Signals and both SCD views, and subsequent display-arrow verification before this documentation pass.

---

## References

### Historical forward-return reference

The condition that ultimately became **BBP Downside Exhaustion** was originally classified as `Strong Sell`. When we examined what prices actually did after those observations, the pattern looked surprisingly **rebound-oriented rather than continuation-oriented**.

Using the fixed **ATR(14)** model that ultimately matches the adopted exhaustion rule:

| Period      | Observations | Median +1d return | Positive after 1d | Median +3d return | Positive after 3d | Median +5d return | Positive after 5d |
| ----------- | -----------: | ----------------: | ----------------: | ----------------: | ----------------: | ----------------: | ----------------: |
| **BBP(10)** |          101 |        **+0.16%** |             51.5% |        **+1.12%** |         **63.4%** |        **+1.66%** |         **67.3%** |
| **BBP(13)** |           97 |        **+0.26%** |             53.6% |        **+1.20%** |         **68.0%** |        **+1.91%** |         **70.1%** |
| **BBP(21)** |           78 |        **+0.42%** |         **60.3%** |        **+1.22%** |         **70.5%** |        **+2.64%** |         **76.9%** |



A few useful takeaways:

* **The signal did not behave like a strong bearish-continuation signal.** Median returns after the old `Strong Sell` state were actually positive at **1, 3, and 5 trading days for all three BBP periods**.
* The rebound tendency became clearer with time. The percentage of observations showing a positive return after five trading days ranged from roughly **67% for BBP(10)** to **77% for BBP(21)**.
* **BBP(13)**—the variant we ultimately treated as the empirically supported reference—showed a median **+1.20%** return after three days and **+1.91%** after five days, with positive returns in about **68%** and **70%** of observations respectively.
* Some individual episodes were considerably stronger. For example, the TSM July 29 observation was followed by approximately **+7.64% after one day, +8.39% after three days, and +10.50% after five days**. The same diagnostic contains other strong rebound examples, including MU and GOOGL.
* That evidence was a major reason to stop interpreting the condition as **“Strong Sell”**. Empirically, it looked much more like **bearish pressure becoming stretched enough to create elevated rebound risk**.
* **Important sample limitation:** the 10-stock diagnostic universe was `TSM, MU, META, NVDA, GOOGL, AMZN, MSFT, GEV, MRVL, VRT`. That is heavily tilted toward semiconductors, technology, AI-related infrastructure, and other high-growth/high-volatility names. The observed rebound rates therefore should **not** be presented as universal expected probabilities for the broader equity market.
* The figures are best treated as **supporting calibration evidence**, not as a claim that “Downside Exhaustion has a 70% success rate.” The sample was bounded, overlapping signals can occur during the same decline, and the diagnostic was not designed as an independent trading-strategy backtest with transaction costs, entry rules, exits, or out-of-sample validation.

### Project references

* `src/config/master_rules_normalized.json` — BBP Downside Exhaustion rule semantics.
* `src/calculations/signal_classifier.py` — independent exhaustion maturity/warmup handling.
* `src/calculations/technical.py` — exhaustion row registration and full-history hover-context arithmetic.
* `src/ui/rolling_heatmap_adapter.py` — `Downside Exhaustion / None` display vocabulary, move arrows, and hover formatting.
* `src/ui/rolling_heatmap_classification.py` — BullBearPower family / Momentum / Exhaustion Signals classification.
* `src/ui/rolling_heatmap_presets.py` — default Custom exposure for BBP Exh (13).
* `streamlit_app.py` — SCD presentation and Single Indicator chart behavior.
* `docs/indicators/BullBearPower.md` — foundational BBP, Bull Power, Bear Power, EMA, Signal, Setup, and Divergence explanation.