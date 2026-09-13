## Summary: Bull Bear Power (BBP) signals
**<u>Class</u>**: Momentum Indicators
**<u>aka</u>**: 'Elder-Ray Index', 'Bull/Bear Power'

Bull Bear Power (BBP) is a **trend-and-pressure indicator**.

At the simplest level, it asks two questions:
1. **Is the underlying EMA trend meaningfully rising or falling?**
2. **Does buying or selling pressure agree with that trend?**

The app uses five directional BBP states:

| Signal                        | Literal trigger                                                                                             | Layman’s translation                                                                                                  | Rule logic                                                      | Bottom-line                                                                    |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Bullish Confirmation (+2)** | Qualified rising EMA trend; BBP was at or below zero two bars ago; BBP is now above zero and still rising   | Buying pressure recently moved from the bearish side to the bullish side while the broader trend was already rising   | Rising trend + recent BBP zero-cross + continued improvement    | **A fresh bullish pressure shift is confirming an established rising trend.**  |
| **Bullish (+1)**              | Qualified rising EMA trend and BBP is above zero, without the fresh-confirmation pattern                    | Buyers have the pressure advantage and that agrees with the broader trend                                             | Rising trend + positive BBP                                     | **Bullish pressure is aligned with an established rising trend.**              |
| **Neutral (0)**               | Neither bullish nor bearish rule is satisfied                                                               | Trend and pressure are not sufficiently aligned for a directional BBP state                                           | Fallback when the required trend/pressure combination is absent | **BBP does not currently provide a qualified directional read.**               |
| **Bearish (-1)**              | Qualified falling EMA trend and BBP is below zero, without the fresh-confirmation pattern                   | Sellers have the pressure advantage and that agrees with the broader trend                                            | Falling trend + negative BBP                                    | **Bearish pressure is aligned with an established falling trend.**             |
| **Bearish Confirmation (-2)** | Qualified falling EMA trend; BBP was at or above zero two bars ago; BBP is now below zero and still falling | Selling pressure recently moved from the bullish side to the bearish side while the broader trend was already falling | Falling trend + recent BBP zero-cross + continued deterioration | **A fresh bearish pressure shift is confirming an established falling trend.** |

> **Important:** In this project, **'Confirmation' does not simply mean “stronger.”**
> - A very large positive or negative BBP value does not automatically receive a 'Confirmation' state.
> - 'Confirmation' means BBP has **recently crossed the zero line into the direction of an already-qualified EMA trend and is still moving that way**.

---
### Interpreting 'Signal', 'Setup', and 'Divergence' together

| Signal                                              | Elder-Ray Setup                                                                 | Divergence                             | Beginner interpretation                                                                                                                                                                          |
| --------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ${\textcolor{blue}{\textsf{Bullish Confirmation}}}$ | ${\textcolor{blue}{\textsf{Bullish}}}$                                          | ${\textsf{None}}$                      | A fresh bullish pressure shift agrees with a rising trend, while bearish pressure is also fading. **Several pieces point in the same bullish direction.**                                        |
| ${\textcolor{blue}{\textsf{Bullish}}}$              | ${\textcolor{blue}{\textsf{Bullish}}}$                                          | ${\textcolor{blue}{\textsf{Bullish}}}$ | The primary regime is bullish, sellers are weakening inside the uptrend, and a prior price low also showed improving selling pressure.                                                           |
| ${\textcolor{blue}{\textsf{Bullish}}}$              | ${\textsf{None}}$                                                               | ${\textcolor{Red}{\textsf{Bearish}}}$  | The current qualified regime remains bullish, but the latest confirmed price high was reached with weaker Bull Power. **The trend is bullish, but the pressure underneath it deserves caution.** |
| ${\textcolor{Red}{\textsf{Bearish Confirmation}}}$  | ${\textcolor{Red}{\textsf{Bearish}}}$                                           | ${\textsf{None}}$                      | A fresh bearish pressure shift agrees with a falling trend, while the remaining bullish pressure is weakening.                                                                                   |
| ${\textcolor{Red}{\textsf{Bearish}}}$               | ${\textcolor{Red}{\textsf{Bearish}}}$                                           | ${\textcolor{Red}{\textsf{Bearish}}}$  | The primary regime is bearish, buyers are losing strength inside the downtrend, and price also showed weaker Bull Power at a higher swing high.                                                  |
| ${\textcolor{Red}{\textsf{Bearish}}}$               | ${\textsf{None}}$                                                               | ${\textcolor{blue}{\textsf{Bullish}}}$ | The primary regime remains bearish, but the most recent lower price low came with improving Bear Power. **The trend is bearish, but selling pressure may be losing force.**                      |
| **Neutral**                                         | ${\textcolor{blue}{\textsf{Bullish}}}$ or ${\textcolor{Red}{\textsf{Bearish}}}$ | Any                                    | The primary trend/pressure test is unresolved, but the secondary Elder-Ray context can still be worth watching.                                                                                  |

---

## A brief overview

### What BBP measures

Bull Bear Power comes from the Elder-Ray framework, which compares the day's buying and selling extremes with an exponential moving average, or EMA.

The two underlying components are:

```text
Bull Power = High - EMA
Bear Power = Low - EMA
```

The app also calculates a combined value:

```text
BBP = Bull Power + Bear Power
```

or, written another way:

```text
BBP = (High - EMA) + (Low - EMA)
```

The easiest way to understand those three values is:

| Component        | What it measures                                 | Beginner's question                                                                       |
| ---------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| **Bull Power**   | How far the day's high is above or below the EMA | **How far could buyers push price relative to its recent baseline?**                      |
| **Bear Power**   | How far the day's low is above or below the EMA  | **How far could sellers push price relative to its recent baseline?**                     |
| **Combined BBP** | Bull Power + Bear Power                          | **Taken together, which side currently has the pressure advantage around that baseline?** |

- A **positive BBP** means the combined balance is on the bullish-pressure side of zero.
- A **negative BBP** means the combined balance is on the bearish-pressure side.

The standard formulas and the conventional 13-period EMA reference are consistent with published Bull Bear Power/Elder-Ray descriptions. ([TradingView][1])

---
#### BBP has no fixed overbought or oversold scale

BBP is very different from RSI or Stochastic.

There is no universal rule such as:

```text
BBP > 70 = overbought
BBP < 30 = oversold
```

The indicator is unbounded, and its raw magnitude is tied to the instrument's price and volatility.

Consequently:
* :gray-background[+10] is not automatically extremely bullish;
* :gray-background[-10] is not automatically extremely bearish;
* :gray-background[+10] on one stock is not directly equivalent to :gray-badge[+10] on another stock;
* raw BBP magnitude should not be treated as a universal overbought/oversold scale.

That is one reason the primary project model uses **BBP's relationship to zero together with a volatility-qualified EMA trend**, rather than fixed high/low BBP thresholds.

---

### Why the EMA matters

The EMA is important because BBP does not merely ask whether today's high or low was high or low in absolute terms.

It asks:

> **How far could buyers and sellers push price away from its recent moving baseline?**

That baseline gives the pressure readings context.

Imagine a stock trading around $100.

The same $100 price can mean very different things if:
* its EMA is $94 and rising;
* its EMA is $100 and flat; or
* its EMA is $106 and falling.

BBP measures the day's buying and selling reach relative to that moving reference point.

The primary BBP Signal in this app goes one step further. It does not accept a tiny EMA rise or fall as sufficient evidence of a trend.

Over five trading bars, the matching EMA must move by more than:

```text
0.25 × ATR(14)
```

ATR(14) measures the stock's recent typical trading range in price units.

For example:

```text
ATR(14) = $4.00

-> 0.25 × $4.00 = $1.00
```

A bullish trend qualification therefore requires the EMA to rise by **more than $1.00 over 5 bars**.

A bearish qualification requires it to fall by **more than $1.00**.

In plain English:

> **The app requires enough EMA movement to matter relative to how much the stock normally moves.**

This keeps a nearly flat EMA from being treated as a meaningful trend merely because it happened to move a few cents.


---
### Why BBP adds information beyond price alone

A price chart tells you:

> **Where did the stock go?**

BBP asks an additional question:

> "***What did the day's buying and selling pressure look like relative to the stock's EMA?***"

Two stocks can both finish higher on the day while showing very different underlying pressure.

For one:
* buyers may push the high well above its EMA;
* sellers may have little ability to push the low beneath the EMA;
* combined BBP may be strongly positive;
* and the EMA may be meaningfully rising.

For another:
* price may close slightly higher;
* sellers may still push the low materially below the EMA;
* combined BBP may be weak or negative;
* and the EMA may be essentially flat.

A simple price change can make both stocks look “up.”

BBP helps distinguish the pressure structure underneath those moves.

> **Price tells you what happened to the stock. BBP asks whether buying or selling pressure around the EMA supports that move.**


---
### The 3 BBP variants

The app provides three parameter lengths:

| Variant     | Period | Horizon     | Character                                                                                |
| ----------- | -----: | ----------- | ---------------------------------------------------------------------------------------- |
| **BBP(10)** |     10 | Short term  | Fastest and most responsive<li>$\small{\textsf{Reacts sooner but changes more readily}}$ |
| **BBP(13)** |     13 | Medium term | Balances responsiveness with smoothing <li>Classic/reference Elder-Ray length            |
| **BBP(21)** |     21 | Long term   | Smoother and slower to recognize change.                                                 |

All three use the same basic model/signal philosophy:

```text
combined BBP sign
+
matching 5-bar EMA trend
+
0.25 × ATR(14) trend qualification
+
recent zero-cross logic for Confirmation
```

- The period changes **responsiveness**, not the meaning of Bullish, Bearish, or Confirmation.
	- The period changes how quickly the EMA and corresponding Bull/Bear Power measurements respond.


---

## BBP Rule Translation

The BBP(10), BBP(13), and BBP(21) rules use the same structure.

The examples below use **BBP(13)** because 13 is the classic/reference Elder-Ray parameter.

### Prerequisite: The 'EMA trend 'gate
Before the app can classify BBP as Bullish or Bearish, it first checks whether the corresponding EMA trend is strong enough to count.
- This is a shared prerequisite used by both bullish states and both bearish states; it is **not a separate BBP signal**.

#### Shared bullish EMA trend qualification

```text
EMA_13 - lag(EMA_13, 5) > 0.25 * ATR_14
```

##### Literal component breakdown

`EMA_13`
* Current EMA(13).

`lag(EMA_13, 5)`
* EMA(13) five trading observations ago.

`EMA_13 - lag(EMA_13, 5)`
* How much EMA(13) has risen over those five bars.

`0.25 * ATR_14`
* One quarter of current ATR(14).
* This provides a volatility-aware minimum movement requirement.

`>`
* The EMA rise must exceed that minimum.

##### Plain-English version

> **EMA(13) must have risen by more than one quarter of the stock's current ATR(14) over five bars.**

---

#### Shared bearish EMA trend qualification

```text
lag(EMA_13, 5) - EMA_13 > 0.25 * ATR_14
```

This reverses the subtraction.

##### Plain-English version

> **EMA(13) must have fallen by more than one quarter of ATR(14) over five bars.**

---

### Bullish Confirmation (+2)

The engine internally stores this state under `strong_buy`, but the user-facing BBP label is:

```text
Bullish Confirmation
```

The rule is:
```text
EMA_13 - lag(EMA_13, 5) > 0.25 * ATR_14
and lag(BBP_13, 2) <= 0
and BBP_13 > 0
and rising_2bar(BBP_13, 1)
```

#### Literal component breakdown

`EMA_13 - lag(EMA_13, 5) > 0.25 * ATR_14`

* The EMA is meaningfully rising.
* Layman's translation: **The broader trend is genuinely rising, not merely drifting upward.**

`lag(BBP_13, 2) <= 0`

* BBP was at or below zero two bars ago.
* Layman's translation: **Pressure was recently still on the bearish/non-bullish side of zero.**

`BBP_13 > 0`

* BBP is now positive.
* Layman's translation: **Buying pressure now has the advantage.**

`rising_2bar(BBP_13, 1)`

* BBP is above its immediately prior value.
* Layman's translation: **That newly positive pressure is still improving.**

Because the clauses use `and`, **every condition must be true**.

#### Literal summary

Meaningful rising trend + recent non-positive BBP + positive BBP now + continued BBP improvement.

#### Plain-English version

> **The EMA is meaningfully rising, BBP recently came from the non-positive side of zero, BBP is now positive, and it is still rising.**

#### Interpretation

This is a **fresh bullish pressure transition inside an already-established rising trend**.

A very large positive BBP can still be ordinary Bullish rather than Bullish Confirmation if it did not recently cross zero in this way.

---

### Bullish (+1)

```text
EMA_13 - lag(EMA_13, 5) > 0.25 * ATR_14
and BBP_13 > 0
and (lag(BBP_13, 2) > 0 or not_rising_2bar(BBP_13, 1))
```

The first two conditions say:

```text
qualified rising EMA
AND
positive BBP
```

The final parenthetical expression prevents the observation from also belonging to the fresh Bullish Confirmation state.

It permits ordinary Bullish when either:

```text
BBP was already positive two bars ago
```

or the current BBP movement does not satisfy the one-step rising condition required by Confirmation.

#### Plain-English version

> **The broader trend is meaningfully rising and BBP is positive, but this is not the specific recent-zero-cross-and-follow-through pattern required for Bullish Confirmation.**

#### Interpretation

> **Bullish is the ongoing aligned regime. Bullish Confirmation is the fresh transition event inside that regime.**

---

### Neutral (0)

The BBP rulebook does not define Neutral as a fixed numerical zone.

The explicit :gray-background[neutral] expression is blank, so Neutral serves as the fallback when none of the four directional expressions applies. The active rules reflect that structure.

Neutral can therefore occur because:

* the EMA has not moved enough to qualify as meaningfully rising or falling;
* BBP's sign does not agree with the qualified EMA direction;
* or the required directional combination is otherwise absent.

#### Plain-English version

> **The app does not currently have enough qualified alignment between EMA trend and BBP pressure to call the regime bullish or bearish.**

This distinction matters:

> **Neutral does not mean “BBP is in the middle of a numerical range.” It means the directional trend-and-pressure requirements are not currently satisfied.**

---

### Bearish (-1)

```text
lag(EMA_13, 5) - EMA_13 > 0.25 * ATR_14
and BBP_13 < 0
and (lag(BBP_13, 2) < 0 or not_falling_2bar(BBP_13, 1))
```

This is the bearish mirror of Bullish.

It requires:

* a qualified falling EMA;
* negative BBP;
* and absence of the specific recent bearish-confirmation pattern.

#### Plain-English version

> **The EMA is meaningfully falling and selling pressure is on the negative side of zero, but this is not the specific fresh-cross-and-follow-through event required for Bearish Confirmation.**

#### Interpretation

> **Selling pressure is aligned with an established falling trend.**

---

### Bearish Confirmation (-2)

Internally stored as `strong_sell`, the user-facing state is:

```text
Bearish Confirmation
```

The rule is:

```text
lag(EMA_13, 5) - EMA_13 > 0.25 * ATR_14
and lag(BBP_13, 2) >= 0
and BBP_13 < 0
and falling_2bar(BBP_13, 1)
```

#### Literal component breakdown

`lag(EMA_13, 5) - EMA_13 > 0.25 * ATR_14`

* EMA is meaningfully falling.
* Layman's translation: **The broader trend is genuinely falling.**

`lag(BBP_13, 2) >= 0`

* BBP was at or above zero two bars ago.
* Layman's translation: **Pressure was recently still on the bullish/non-bearish side.**

`BBP_13 < 0`

* BBP is negative now.
* Layman's translation: **Selling pressure now has the advantage.**

`falling_2bar(BBP_13, 1)`

* Current BBP is below its immediately prior value.
* Layman's translation: **That newly negative pressure is still deteriorating.**

#### Plain-English version

> **The EMA is meaningfully falling, BBP recently came from the non-negative side of zero, BBP is now negative, and it is still falling.**

#### Interpretation

This is a **fresh bearish pressure transition inside an established falling trend**.

Again:

> **Confirmation describes the recency and structure of the shift—not simply a larger negative BBP value.**


---

## (HTR) Understanding the BBP Hover
The BBP hover contains several related pieces of information.

They should **not** be treated as multiple versions of the same signal.

The most useful mental model is:
- **Signal** = current state
- **Setup** = favorable configuration
- **Divergence** = warning that price and pressure are separating.

Another useful distinction is:
> The '**Signal**' asks who currently has directional control;
>
> The '**Elder-Ray Setup**' asks whether the weaker side appears to be losing its remaining influence inside that trend.

The app deliberately carries Setup and Divergence separately from the primary score rather than collapsing all Elder-Ray information into one classification.

### The generic opening

The BBP hover begins with observation-level information such as:

```text
Value: XX.XX | Price: XXX.XX
Δ vs prior day: +X.XX (+X.X%) | Price: ...
Trend: Rising | Price: ...

Signal: Bullish
```

These fields answer:

| Hover field        | What it tells you                                                       |
| ------------------ | ----------------------------------------------------------------------- |
| **Value**          | Current combined BBP                                                    |
| **Δ vs prior day** | How much BBP changed from the previous observation                      |
| **Trend**          | Whether BBP rose, fell, or remained effectively flat on the latest move |
| **Signal**         | The primary qualified BBP state                                         |

One subtle but important distinction:

> **Hover 'Trend' is a one-bar description of the displayed BBP value. It is not the five-bar EMA trend test used by the primary Signal.**

---

### Bull and Bear Power in the Hover

The hover also exposes the individual Bull Power and Bear Power values, including their change from the prior observation. The adapter carries those two component values separately rather than showing only the combined BBP result.

This is valuable because two observations can have the same combined BBP while having very different internal structures.

Example 1:

```text
Bull Power = +8
Bear Power = -2

BBP = +6
```

Example 2:

```text
Bull Power = +14
Bear Power = -8

BBP = +6
```

Both produce:

```text
BBP = +6
```

But the second case contains much larger opposing forces.

The separate component lines therefore help answer:

* How strongly can buyers push above the EMA?
* How strongly can sellers push below it?
* Is Bull Power strengthening or weakening?
* Is negative Bear Power becoming more or less severe?

Those questions are especially relevant to interpreting **Elder-Ray Setup** and **Elder-Ray Divergence**.

---

### Signal, Setup, and Divergence — the 3 BBP layers

The three hover fields should be viewed as **different lenses**, not three votes that must always agree.

| Layer                    | Main question                                                             | Simplest translation                                               |
| ------------------------ | ------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Signal**               | Does current combined BBP pressure agree with a meaningful EMA trend?     | **What is happening right now?**                                   |
| **Elder-Ray Setup**      | Is the weaker side losing influence inside that trend?                    | **Is the market arranged in a way that may favor the trend side?** |
| **Elder-Ray Divergence** | Is price making a new swing extreme without matching underlying pressure? | **Is price telling one story while pressure tells another?**       |

### How to interpret 'Signal', 'Setup', and 'Divergence' together

| Signal                                              | Elder-Ray Setup                                                                 | Divergence                             | Beginner interpretation                                                                                                                                                                          |
| --------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ${\textcolor{blue}{\textsf{Bullish Confirmation}}}$ | ${\textcolor{blue}{\textsf{Bullish}}}$                                          | None                                   | A fresh bullish pressure shift agrees with a rising trend, while bearish pressure is also fading. **Several pieces point in the same bullish direction.**                                        |
| ${\textcolor{blue}{\textsf{Bullish}}}$              | ${\textcolor{blue}{\textsf{Bullish}}}$                                          | ${\textcolor{blue}{\textsf{Bullish}}}$ | The primary regime is bullish, sellers are weakening inside the uptrend, and a prior price low also showed improving selling pressure.                                                           |
| ${\textcolor{blue}{\textsf{Bullish}}}$              | None                                                                            | ${\textcolor{Red}{\textsf{Bearish}}}$  | The current qualified regime remains bullish, but the latest confirmed price high was reached with weaker Bull Power. **The trend is bullish, but the pressure underneath it deserves caution.** |
| ${\textcolor{Red}{\textsf{Bearish Confirmation}}}$  | ${\textcolor{Red}{\textsf{Bearish}}}$                                           | None                                   | A fresh bearish pressure shift agrees with a falling trend, while the remaining bullish pressure is weakening.                                                                                   |
| ${\textcolor{Red}{\textsf{Bearish}}}$               | ${\textcolor{Red}{\textsf{Bearish}}}$                                           | ${\textcolor{Red}{\textsf{Bearish}}}$  | The primary regime is bearish, buyers are losing strength inside the downtrend, and price also showed weaker Bull Power at a higher swing high.                                                  |
| ${\textcolor{Red}{\textsf{Bearish}}}$               | None                                                                            | ${\textcolor{blue}{\textsf{Bullish}}}$ | The primary regime remains bearish, but the most recent lower price low came with improving Bear Power. **The trend is bearish, but selling pressure may be losing force.**                      |
| **Neutral**                                         | ${\textcolor{blue}{\textsf{Bullish}}}$ or ${\textcolor{Red}{\textsf{Bearish}}}$ | Any                                    | The primary trend/pressure test is unresolved, but the secondary Elder-Ray context can still be worth watching.                                                                                  |

One sentence is especially useful here:

> **A warning does not cancel a trend, and a trend does not cancel a warning.**

For example:

```text
Signal: Bearish
Elder-Ray Divergence: Bullish
```

is not contradictory.

It can mean:

> **The current EMA/BBP regime still favors sellers, but the most recent price swing suggests those sellers may be losing some underlying force.**

They are answering different questions.

---

### Signal — who has directional control now?

The primary "Signal" can be:

```text
Bullish Confirmation
Bullish
Neutral
Bearish
Bearish Confirmation
```

It uses three types of information:

1. **EMA trend** — is the relevant EMA meaningfully rising or falling?
2. **BBP sign** — is combined pressure above or below zero?
3. **Recent BBP history** — for Confirmation, has BBP recently crossed zero and continued in that direction?

The simplest translation is:
> "***Signal tells you whether current pressure agrees with a meaningful trend—and whether that alignment has just been reinforced by a fresh zero-line shift.***"

#### What Signal does not mean

Signal does **not** tell you:

* that price must continue;
* that price must reverse;
* that a trade should automatically be opened;
* that a large positive BBP is “overbought”;
* that a large negative BBP is “oversold”;
* whether a classic Elder-Ray Setup exists;
* whether price and the underlying pressure components are diverging.

Those last two questions belong to the next two hover fields.

---

### Elder-Ray Setup: "*Is the weaker side losing influence inside the trend?*"

Elder-Ray Setup is a separate contextual field.

It can display:

```text
Bullish
Bearish
None
```

This layer uses the individual Bull Power or Bear Power component rather than relying only on their combined BBP value. That matches the classic Elder-Ray idea of reading Bear Power inside a rising EMA environment and Bull Power inside a falling EMA environment. ([Interactive Brokers][2])

#### Elder-Ray Setup logic

The Setup layer is intentionally separate from the primary BBP score.

| Setup       | Rule idea                                         | What is happening                                                              | Bottom-line                                   |
| ----------- | ------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------- |
| **Bullish** | EMA rising + Bear Power < 0 + Bear Power rising   | Sellers still push beneath the EMA, but their pressure is becoming less severe | **Trend is up; seller influence is fading.**  |
| **Bearish** | EMA falling + Bull Power > 0 + Bull Power falling | Buyers still push above the EMA, but their pressure is weakening               | **Trend is down; buyer influence is fading.** |
| **None**    | Neither condition                                 | Classic setup arrangement is absent                                            | **No active Elder-Ray Setup.**                |

The primary Signal asks about:

```text
combined BBP + qualified EMA trend
```

The Setup asks about:

```text
individual Bear/Bull Power + EMA direction
```

That difference is precisely why the fields can disagree.

---

#### Bullish Elder-Ray Setup

Conceptually:

```text
EMA rising
AND Bear Power < 0
AND Bear Power rising
```

Each part matters.

##### EMA rising

The general trend is upward.

That provides the directional backdrop.

##### Bear Power is negative

Sellers can still push the stock's low beneath the EMA.

In other words:

> **Selling pressure has not disappeared.**

##### Bear Power is rising

Suppose:

```text
Yesterday: Bear Power = -5.20
Today:     Bear Power = -2.80
```

Bear Power remains negative, but it became:

```text
+2.40
```

less negative.

That means sellers still have some ability to push below the EMA, but that ability has **weakened**.

The complete interpretation is therefore:

> ***The trend is rising. Sellers can still push price below the EMA, but they are doing so with less force than before.***

Or even more simply:

> "***The trend is up, and the remaining selling pressure is easing.***"

This is why a Bullish Elder-Ray Setup does **not** require Bear Power to become positive.

The interesting condition is precisely that sellers remain present but appear to be losing influence.

---

#### Bearish Elder-Ray Setup

The bearish case reverses the logic:

```text
EMA falling
AND Bull Power > 0
AND Bull Power falling
```

##### EMA falling

The broader trend is downward.

##### Bull Power is falling

Suppose:

```text
Yesterday: Bull Power = +6.10
Today:     Bull Power = +3.25
```

Bull Power is still positive, but it weakened by:

```text
-2.85
```

Buyers are still capable of producing an upside push, but that push has become weaker.

The combined interpretation is:

> **The trend is falling. Buyers can still rally price above the EMA, but that buying pressure is fading.**

Or:

> **The trend is down, and the remaining buying pressure is losing strength.**

---

##### Bull Power remains positive

Buyers can still push the high above the EMA.

So buyers have not disappeared.

#### What does 'Elder-Ray Setup: None' mean?

:gray-background[None] means neither the bullish nor bearish Elder-Ray Setup is currently active.

It does **not** mean:

```text
Signal = Neutral
```

It also does not mean:

* there is no trend;
* BBP contains no useful information;
* a divergence cannot exist.

It means only:

> **The specific Elder-Ray Setup conditions are not present on this observation.**

---

### Elder-Ray Divergence: "*Is price telling one story while pressure tells another?*"

**Elder-Ray Divergence** is another independent layer.

It can display:

```text
Bullish
Bearish
None
```

The easiest way to understand divergence is:

> **Price is reaching a more extreme level, but the buying or selling pressure underneath that move is failing to become equally extreme.**

Most importantly:

> **Divergence is a warning, not a prediction.**

The project's divergence implementation uses confirmed five-bar **price** swing points, then samples the corresponding Bear Power or Bull Power on those exact pivot dates.

#### Elder-Ray Divergence logic

The Divergence layer is also independent.

| Divergence  | Price condition                         | Pressure condition                     | Bottom-line                                        |
| ----------- | --------------------------------------- | -------------------------------------- | -------------------------------------------------- |
| **Bullish** | New confirmed swing low is lower        | Bear Power at that newer low is higher | **Price worsened, but selling pressure improved.** |
| **Bearish** | New confirmed swing high is higher      | Bull Power at that newer high is lower | **Price improved, but buying pressure weakened.**  |
| **None**    | No qualifying divergence once evaluable | —                                      | **No confirmed price/pressure divergence event.**  |

The relevant pressure component is sampled on the same price-pivot dates, and the event appears only after the five-bar pivot becomes confirmed.


---

#### Bullish Elder-Ray Divergence

The app looks for:

```text
Price makes a lower swing low
AND
Bear Power makes a higher value
```

Example:

|                | Earlier low | Newer low |
| -------------- | ----------: | --------: |
| **Price**      |        $100 |       $96 |
| **Bear Power** |        -8.0 |      -4.5 |

Price became worse:

```text
$100 → $96
```

It made a lower low.

But Bear Power became **less negative**:

```text
-8.0 → -4.5
```

Selling pressure did not confirm the deterioration in price.

The beginner translation is:

> **Price looks worse, but selling pressure looks better. Sellers may be losing force even though price has reached a lower low.**

That is why it is called **bullish divergence**.

It does **not** mean price must immediately reverse higher.

---

#### Bearish Elder-Ray Divergence

The opposite condition is:

```text
Price makes a higher swing high
AND
Bull Power makes a lower value
```

Example:

|                | Earlier high | Newer high |
| -------------- | -----------: | ---------: |
| **Price**      |         $150 |       $156 |
| **Bull Power** |         +9.0 |       +5.5 |

Price became stronger:

```text
$150 → $156
```

But Bull Power weakened:

```text
+9.0 → +5.5
```

The newer price high was reached with **less underlying buying pressure**.

Beginner translation:

> **Price looks stronger, but buying pressure looks weaker. Buyers may be losing force even though price has reached a higher high.**

That is a bearish warning—not proof that a decline must begin.

---

#### Why divergence appears two bars after the swing

A price swing cannot be known with certainty at the instant the candidate high or low occurs.

The project uses a five-bar pivot structure. A candidate pivot at bar :gray-background[t] becomes confirmed only after the next two trading bars exist.

Therefore:

```text
candidate pivot = t
confirmed pivot = t + 2
```

A divergence event is emitted at `t+2`.

It is **not** painted backward onto `t`.

That delay is intentional.

> **The app waits until the swing was actually knowable rather than using future information to make the historical chart look smarter than it really was.**

#### 'None' versus no value

Once enough confirmed swing history exists for both divergence directions to be evaluated:

```text
Elder-Ray Divergence: None
```

means:

> **No divergence is confirmed on this observation.**

Before sufficient swing history exists, the field can remain unavailable rather than falsely claiming that no divergence occurred. The production implementation makes that distinction explicitly.

---

## How to Read the BBP heatmap

A useful reading sequence is:

1. **Read the number.** Is BBP positive or negative?
2. **Read the color / Signal.** Does that pressure agree with a qualified EMA trend?
3. **Look for Confirmation.** Has BBP recently crossed zero into that trend and continued moving in the same direction?
4. **Open the hover.** Use Elder-Ray Setup and Elder-Ray Divergence as separate context—not as duplicates of Signal.

The five primary states can be simplified to:

| Signal                   | Question to ask                                                         |
| ------------------------ | ----------------------------------------------------------------------- |
| **Bullish Confirmation** | **Did pressure recently turn bullish inside an already-rising trend?**  |
| **Bullish**              | **Are bullish pressure and a qualified rising trend aligned?**          |
| **Neutral**              | **Is that qualified directional alignment currently absent?**           |
| **Bearish**              | **Are bearish pressure and a qualified falling trend aligned?**         |
| **Bearish Confirmation** | **Did pressure recently turn bearish inside an already-falling trend?** |

---

### What does the number in the heatmap cell mean?

The number printed inside a BBP heatmap cell is the **combined BBP value**.

It is **not** the score.

For BBP(13):
- **Bull Power** = `High - EMA(13)`
- **Bear Power** = `Low - EMA(13)`
- **BBP(13)** = `Bull Power + Bear Power`


So if the cell displays:

```text
+6.40
```

combined buying-versus-selling pressure is **6.40 price units above zero**.

If it displays:

```text
-8.25
```

the combined pressure measure is **8.25 price units below zero**.

### The number and the color answer different questions

| Heatmap feature         | What it represents         | Question it answers                                                                        |
| ----------------------- | -------------------------- | ------------------------------------------------------------------------------------------ |
| **Printed BBP value**   | Raw combined BBP           | **Which side of zero is pressure on, and by how much?**                                    |
| **Cell color / Signal** | Project BBP classification | **Does that pressure agree with a meaningful EMA trend, and is it a recent confirmation?** |

This distinction is extremely important.

A **positive BBP does not automatically mean Bullish**.

Consider:

```text
BBP(13) = +5.00

EMA(13), five bars ago = $100.00
EMA(13), now            = $100.40

EMA rise = $0.40

ATR(14) = $4.00
Required rise = 0.25 × $4.00 = $1.00
```

BBP is positive, so buyers currently have the combined pressure advantage.

But the EMA rose only:

```text
$0.40
```

while the rule requires more than:

```text
$1.00
```

The Signal can therefore be:

```text
Neutral
```

The app is effectively saying:

> **Buyers currently have the pressure advantage, but the broader EMA trend is not strong enough for that pressure to count as a qualified Bullish BBP regime.**



---

## Industry-standard baseline versus this project

### Conventional Elder-Ray foundation

Published descriptions of Elder-Ray/Bull Bear Power use separate Bull Power and Bear Power measurements relative to an EMA:

```text
Bull Power = High - EMA
Bear Power = Low - EMA
```

A 13-period EMA is the conventional/default reference in widely used implementations. EMA direction, improving negative Bear Power, weakening positive Bull Power, and price/pressure divergence are also recognized Elder-Ray interpretation concepts. ([TradingView][1])

### Project-specific calibration

This dashboard extends that foundation by:

* displaying :gray-background[Bull Power + Bear Power] as combined BBP;
* supporting 10-, 13-, and 21-period versions;
* requiring a five-bar EMA move greater than :gray-badge[0.25 × ATR(14)] before assigning the primary Bullish/Bearish regime;
* distinguishing recent BBP zero-cross Confirmation from the ongoing directional regime;
* preserving Elder-Ray Setup as separate context;
* preserving confirmed Elder-Ray Divergence as separate context.

The project's five states:

```text
Bullish Confirmation
Bullish
Neutral
Bearish
Bearish Confirmation
```

are therefore **project-specific classifications**, not a claim that Elder-Ray has a standard industry five-state taxonomy.

> **The project does not force every useful Elder-Ray concept into a single score.**

---

## Strengths

BBP is particularly useful for:

* distinguishing price movement from underlying buying/selling pressure;
* requiring pressure to agree with a meaningful EMA trend;
* filtering tiny EMA movements through ATR(14);
* separating an ongoing trend/pressure regime from a fresh zero-line transition;
* examining the weaker side directly through Bull Power and Bear Power;
* identifying price/pressure disagreement through confirmed divergence.

---

## Limitations

### Raw BBP magnitude is not standardized

BBP is unbounded and expressed in price-related units.

A value of:

```text
+8
```

on one security is not necessarily equivalent to :gray-background[+8] on another.

### Positive BBP does not automatically mean Bullish

Positive BBP says buyers have the combined pressure advantage.

The project still requires a qualified rising EMA trend.

Negative BBP works the same way in reverse.

### Confirmation is not a prediction

A Confirmation state identifies a recent pressure transition into an existing trend.

It does not guarantee continuation.

### Elder-Ray Setup is context, not the primary score

Setup can disagree with Signal because the two use different information and answer different questions.

### Divergence is also context

A bearish divergence can occur while the primary regime remains Bullish.

A bullish divergence can occur while the primary regime remains Bearish.

> **Divergence warns that the pressure underneath price is changing; it does not by itself declare that the current trend has ended.**

### Confirmed divergence necessarily arrives later

Because the app waits for the swing pivot to become knowable, the divergence cannot appear on the original pivot date in real time.

That delay is a tradeoff for avoiding hindsight/back-painting.

---

## Relationship to BBP Downside Exhaustion

**BBP Downside Exhaustion** is a separate indicator.

Primary BBP asks:

> **Who currently has directional control, and does that pressure agree with a meaningful EMA trend?**

BBP Downside Exhaustion asks:

> **Inside a qualified decline, has negative BBP pressure become unusually persistent and severe enough to raise rebound risk?**

Those statements can coexist.

For example:

```text
Primary BBP: Bearish Confirmation

BBP Downside Exhaustion: Downside Exhaustion
```

is not contradictory.

It can mean:

> **Sellers have recently taken clear directional control, but selling pressure has also become unusually stretched.**

The first describes **directional control**.

The second describes **potential exhaustion/rebound risk**.

The separate 'BBP_DOWNSIDEEXHAUSTION.md' document covers that model in detail.

---

## Beginner's checklist

When reading a BBP cell, ask these questions in order:

| Step  | Question                                                                            |
| ----- | ----------------------------------------------------------------------------------- |
| **1** | Is the displayed BBP value positive or negative?                                    |
| **2** | What does the primary Signal say?                                                   |
| **3** | Is it a Confirmation state—meaning BBP recently crossed zero into the trend?        |
| **4** | What does Elder-Ray Setup say about the weaker side's remaining influence?          |
| **5** | What does Elder-Ray Divergence say about price versus underlying pressure?          |
| **6** | Do those layers agree, or is one warning about something the others do not measure? |

The shortest useful summary remains:

> **Signal = current state. Setup = favorable configuration. Divergence = warning that price and pressure are separating.**

---

## Initial audit note

**Semantic type:** Directional trend/pressure regime with separate Elder-Ray context layers.

**Primary philosophy:** Trend confirmation rather than fixed overbought/oversold classification.

**Numeric identity:**

```text
Bull Power = High - EMA(p)
Bear Power = Low - EMA(p)
BBP(p) = Bull Power + Bear Power
```

with configured periods:

```text
10 / 13 / 21
```

**Primary scoring vocabulary:**

```text
+2  Bullish Confirmation
+1  Bullish
 0  Neutral
-1  Bearish
-2  Bearish Confirmation
```

**Trend qualification:** Five-bar EMA movement must exceed :gray-badge[0.25 × ATR(14)] in the applicable direction.

**Confirmation meaning:** Recent BBP zero-line transition into the qualified EMA trend direction plus current BBP follow-through.

**Elder-Ray Setup:** Independent secondary context using EMA direction and the relevant Bull Power/Bear Power component.

**Elder-Ray Divergence:** Independent price-swing-versus-pressure context using confirmed five-bar price pivots; events are emitted after confirmation rather than back-painted.

**Display-versus-scoring distinction:** The heatmap displays raw combined BBP numerically while the heatmap color represents the five-state rule-engine classification.

**Verification status:** The adopted directional-regime implementation completed production-path verification, independent rule-contract checks, manual UI acceptance, and version-control checkpointing before this documentation pass.

---

## References

### External conceptual references

* **TradingView — Bull Bear Power:** formula, combined BBP interpretation, zero line, and 13-period default.
* **Interactive Brokers / IBKR Campus — Elder-Ray:** Bull/Bear Power interpretation, EMA trend context, improving negative Bear Power, weakening positive Bull Power, and divergence.

### Project references

* :gray[src/config/master_rules_normalized.json] — primary BBP directional-regime rules.
* :gray[src/calculations/technical.py] — BBP component transport and confirmed Elder-Ray divergence.
* :gray[src/calculations/signal_classifier.py] — rule classification and maturity handling.
* :gray[src/ui/rolling_heatmap_adapter.py] — displayed BBP value, Signal vocabulary, Elder-Ray Setup/Divergence, and Bull/Bear component hover presentation.



---
## Notes
The Elder Ray index is primarily a momentum indicator that combines components of trend-following and momentum to assess the strength of buying (bullish) and selling (bearish) pressures in the market. It identifies the strength of bulls by measuring how far prices move above a moving average and the strength of bears by measuring how far prices move below it, providing insight into market power dynamics.

The Elder Ray index is not solely a trend or volatility indicator but a combination of both to analyze momentum. 
- It helps traders understand the balance of power between buyers and sellers

Quantifies buying and selling pressure through its bull power and bear power components.
- This approach offers traders instant clarity into dynamic power shifts between buyers and sellers at each moment—an invaluable tool for spotting potential reversals or continuation patterns based on divergence or convergence with price action.



$$----------$$
The Elder Ray Index is a technical indicator that uses Bull Power and Bear Power to measure buying and selling pressure, helping traders identify potential market trends and reversals by analyzing the distance between a security's high/low and its exponential moving average (EMA).
- It consists of two oscillating histograms that show the strength of bulls and bears relative to the prevailing trend, which is determined by the EMA's slope.  


---
$\large{\textsf{Components}}$
The indicator consists of two main parts: Bull Power and Bear Power, which are calculated relative to a specified Exponential Moving Average (EMA).
- **Bull Power:** Calculated as the difference between the day's high price and the 13-period EMA.
- **Bear Power:** Calculated as the difference between the day's low price and the 13-period EMA.

---
**<u>Interpretation/Rules for Bull Bear Index</u>**:
1. If both Bull Power and Bear Power rise, it could signal a potential bullish trend.
2. If both Bull Power and Bear Power fall, it could indicate a potential bearish trend.
3. If Bull Power rises while Bear Power falls, it could suggest an upcoming trend reversal in favor of the bulls.
4. If Bear Power is rising while Bull Power is falling, it could suggest an upcoming trend reversal in favor of the bears.


| Date           |Bull Power|Bear Power|Interpretation|
|---|---|---|---|
| **2025-12-10** |90.77|14.79|**Extremely Bullish:** Both are positive; bears couldn't even push price below the average.|
| **2025-12-15** |15.47|-44.63|**Standard Market:** Bulls above average, bears below average.|
| **2025-12-18** |-16.30|-73.93|**Extremely Bearish:** Both are negative; bulls couldn't lift price above the average.|


---
$\large{\textsf{What it Indicates}}$
- **Momentum:** It measures the conviction of buyers (Bull Power) and sellers (Bear Power) by showing how far price is being pushed away from the average price (EMA). 
- **Trend Strength:** The direction and strength of Bull Power and Bear Power can indicate the strength of existing trends. For instance, rising Bull Power suggests strong buying momentum, while rising Bear Power signals strong selling momentum. 
- **Potential Reversals:** Divergences between Bull Power or Bear Power and the actual price can signal potential trend reversals

$$----------$$
The Elder Ray Index is a technical indicator that uses Bull Power and Bear Power to measure buying and selling pressure, helping traders identify potential market trends and reversals by analyzing the distance between a security's high/low and its exponential moving average (EMA). It consists of two oscillating histograms that show the strength of bulls and bears relative to the prevailing trend, which is determined by the EMA's slope.  


$\large{\textsf{How it Works}}$: 
- **Bull Power**: Measures the strength of buyers by calculating the difference between the current high and the EMA. A higher positive Bull Power indicates strong buying pressure, while a falling or negative value shows weakening bulls.
- **Bear Power**: Measures the strength of sellers by calculating the difference between the current low and the EMA. A lower negative Bear Power indicates strong selling pressure, and a positive value suggests bears are losing control.


$\large{\textsf{Key Uses}}$
- Particularly valuable for traders seeking to grasp <u>short-term market dynamics</u> and <u>reversals</u>


- **Trend Identification**: By comparing the Bull Power and Bear Power histograms to the EMA, traders can assess the strength of the trend and the forces driving it. 

- **Divergence Signals**: A divergence between Bull Power/Bear Power and the price action can signal a potential reversal. For example, rising Bear Power while the price is falling can indicate strong selling momentum. 

- **Confirmation**: The indicator can confirm trends by showing that bulls are pushing prices above the EMA or that bears are pressing prices below it. 


$\large{\textsf{How to Trade With It}}$:
- **In a Bullish Trend**: Look for an upward-sloping EMA, a negative Bear Power that is rising (weakening sellers), and a positive Bull Power that is strong and increasing to confirm buying pressure. 

- **In a Bearish Trend**: Look for a downward-sloping EMA, a positive Bull Power that is falling (weakening buyers), and a strong and falling Bear Power to confirm selling pressure. 

- **Divergence Trading**: If the price makes a new high but Bull Power makes a lower high, it signals diminishing buying strength, a potential reversal. 


$\large{\textsf{Important Considerations}}$:
 
- **Combine with Other Indicators**: The Elder Ray Index should not be used in isolation; it is most effective when combined with other technical indicators and price action analysis.

- **Market Conditions**: The indicator works best in trending markets and can generate false signals in sideways or range-bound markets.

- **EMA Period**: The accuracy of the indicator depends on the chosen period for the exponential moving average (EMA), requiring fine-tuning for optimal results.