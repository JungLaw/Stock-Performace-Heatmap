## Summary: CMF(21) signals
**See**: [Table of Contents](#table-of-contents)

| Signal | Literal trigger | Layman’s translation | Rule logic | Bottom-line |
|---|---|---|---|---|
| :blue-background[strong_buy] | :gray-background[CMF_21 > 0.20] and CMF rose across both recent moves | CMF shows substantial accumulation pressure, and that pressure has strengthened twice in succession. | The raw CMF value is above the CMF(21) Strong threshold, and :gray-background[current > prior > two periods ago]. | **Buying pressure is high and still strengthening.** |
| :blue-background[buy] | :gray-background[CMF_21 > 0.10], without the complete Strong Buy combination | CMF shows meaningful accumulation pressure, but the reading is either not above the Strong threshold or has not risen across both recent moves. | The value has left Neutral on the positive side, but it is not both above :gray-background[+0.20] and strictly rising across two moves. | **Buying pressure exists**, but it is not both high and steadily strengthening. |
| :blue-background[neutral] | :gray-background[-0.10 <= CMF_21 <= 0.10] | CMF is inside the project’s middle zone, where neither accumulation nor distribution has a clear enough advantage. | The raw CMF value has not crossed either the :gray-background[+0.10] Buy cutoff or the :gray-background[-0.10] Sell cutoff. | **Neither side has a clear volume-backed pressure advantage.** |
| :blue-background[sell] | :gray-background[CMF_21 < -0.10], without the complete Strong Sell combination | CMF shows meaningful distribution pressure, but the reading is either not below the Strong Sell threshold or has not fallen across both recent moves. | The value has left Neutral on the negative side, but it is not both below :gray-background[-0.20] and strictly falling across two moves. | **Selling pressure exists**, but it is not both high and steadily strengthening. |
| :blue-background[strong_sell] | :gray-background[CMF_21 < -0.20] and CMF fell across both recent moves | CMF shows substantial distribution pressure, and that pressure has strengthened twice in succession. | The raw CMF value is below the CMF(21) Strong Sell threshold, and :gray-background[current < prior < two periods ago]. | **Selling pressure is high and still strengthening.** |

---
### How to Read: '↗|↘' Display-value Customizations
(:small[[Back to top](#summary-cmf-21-signals)])

- **↗ / ↘:** CMF increasing / decreasing — not stock price direction.
- **Sell ↗:** Distribution pressure easing; CMF rose for 2 consecutive moves.
- **Buy ↘:** Accumulation pressure easing; CMF fell for 2 consecutive moves.
- **Neutral ↗ / ↘:** CMF rose/fell for 4 consecutive moves; directional pressure may be building or easing, but the current Signal remains :blue-background[Neutral].
- **No arrow:** Conditions not met, insufficient history, or Strong Buy/Sell.

**NOTE**: :blue-background[Neutral ↗] doesn't necessarily mean accumulation is building, and :blue-background[Neutral ↘] doesn't necessarily mean distribution is building.
- The sign of the displayed CMF value determines whether the **movement represents '*strengthening*' or '*easing*' pressure**.


### Most Important Patterns
(:small[[Back to top](#summary-cmf-21-signals)])
**See:** [The CMF patterns you should not overlook](#the-cmf-patterns-you-should-not-overlook)

There are 2 ways to interpret importance here:
1. **Strongest evidence of an established pressure state**: :green-background[Strong Buy] and :red-background[Strong Sell] rank highest. Their underlying CMF magnitude and direction meet our strictest rule conditions.
2. **Most valuable new information beyond the existing heatmap colors**: :red-background[Sell ↗] and :green-background[Buy ↘] rank highest. The color already communicates Sell or Buy; the arrow reveals that qualified pressure has begun weakening.


| Priority                                 | Patterns                                   | Why they deserve attention                                                                                                                                           |
| ---------------------------------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tier 1 — **Qualified pressure weakening**    | **:red-background[Sell]** :red[−29.1]**↗** and **:green-background[Buy]** :blue[+18.4]**↘**             | Reveals changes that the existing Buy/Sell cell color cannot communicate. Potential early warning that established pressure is losing strength.                      |
| Tier 2 — **Strong directional confirmation** | **:green-background[Strong Buy]** :blue[+22.0] and **:red-background[Strong Sell]** :red[−23.0] | Strongest current pressure evidence under our rules: material CMF magnitude plus two-move confirmation. Especially useful when aligned with the broader price trend. |
| Tier 3 — **Price/CMF disagreement**          | **Price up + :red-background[Sell]** and **Price down + :green-background[Buy]**       | Raises questions about participation supporting price movement. More important when disagreement persists or occurs around support, resistance, or a breakout.       |
| Tier 4 — **Emerging directional bias**       | **:gray-background[Neutral]** :blue[+7.0]**↗** and **:gray-background[Neutral]** :red[−7.0]**↘**        | Four consecutive moves are developing pressure in one direction, but it hasn't reached the Buy/Sell threshold.                                                       |
| Tier 5 — **Fading unqualified pressure**     | **:gray-background[Neutral]** :red[−3.0]**↗** and **:gray-background[Neutral]** :blue[+3.0]**↘**        | Shows early improvement or deterioration within Neutral, but remains less decisive than the other patterns.                                                          |

---
### CMF period rule comparison
(:small[[Back to top](#summary-cmf-21-signals)])

| Setting   | Strong Buy                                 | Buy                                                | Neutral                 | Sell                                               | Strong Sell                                 |
| --------- | ------------------------------------------ | -------------------------------------------------- | ----------------------- | -------------------------------------------------- | ------------------------------------------- |
| :gray-background[CMF(10)] | Above :gray-background[+0.25] and rising across two moves  | Above :gray-background[+0.10] without complete Strong confirmation | :gray-background[-0.10] through :gray-background[+0.10] | Below :gray-background[-0.10] without complete Strong confirmation | Below :gray-background[-0.25] and falling across two moves  |
| :gray-background[CMF(21)] | Above :gray-background[+0.20] and rising across two moves  | Above :gray-background[+0.10] without complete Strong confirmation | :gray-background[-0.10] through :gray-background[+0.10] | Below :gray-background[-0.10] without complete Strong confirmation | Below :gray-background[-0.20] and falling across two moves  |
| :gray-background[CMF(30)] | Above :gray-background[+0.175] and rising across two moves | Above :gray-background[+0.10] without complete Strong confirmation | :gray-background[-0.10] through :gray-background[+0.10] | Below :gray-background[-0.10] without complete Strong confirmation | Below :gray-background[-0.175] and falling across two moves |
| :gray-background[CMF(50)] | Above :gray-background[+0.15] and rising across two moves  | Above :gray-background[+0.10] without complete Strong confirmation | :gray-background[-0.10] through :gray-background[+0.10] | Below :gray-background[-0.10] without complete Strong confirmation | Below :gray-background[-0.15] and falling across two moves  |


| Signal      | One-sentence interpretation                                                         | Bottom-line                                                           |
| ----------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Strong Buy  | Buying pressure is strong and has strengthened through both recent moves.           | **Strong buying pressure is getting stronger.**                       |
| Buy         | Buying pressure exists, but it is not both strong and steadily strengthening.       | **Buying pressure exists, but it is not fully confirmed as Strong.**  |
| Neutral     | Neither buying nor selling pressure has crossed the project’s directional boundary. | **Neither side has a clear volume-backed advantage.**                 |
| Sell        | Selling pressure exists, but it is not both strong and steadily strengthening.      | **Selling pressure exists, but it is not fully confirmed as Strong.** |
| Strong Sell | Selling pressure is strong and has strengthened through both recent moves.          | **Strong selling pressure is getting stronger.**                      |
|             |                                                                                     |                                                                       |

## CMF(21) — brief overview
(:small[[Back to top](#summary-cmf-21-signals)])

Chaikin Money Flow, or **CMF**, is a volume-based indicator that estimates whether a stock is experiencing more **accumulation pressure** or **distribution pressure** over a chosen period.
- In other words, it builds on the **Accumulation/Distribution** concept by weighting daily closing-location contributions by volume over the selected lookback (typically 21 sessions).

In ordinary language:
- **Accumulation pressure** means volume has been associated more with closes near the upper part of each day’s trading range.
- **Distribution pressure** means volume has been associated more with closes near the lower part of each day’s trading range.
- A value near zero means neither pattern has established a strong enough advantage.

For :blue-background[CMF(21)]:

```text
21 = the most recent 21 trading periods used in the calculation
```

On daily stock data, that is roughly one trading month.

CMF does not ask only whether the stock’s price rose or fell from the prior day. It asks:

> **Where did the stock close inside each day’s High–Low range, and how much volume accompanied that closing position?**

That distinction matters.
- A stock can rise from one day to the next but still close near the low of the current day’s range. That day can contribute negatively to CMF.
- A stock can also fall from the prior day but close near the high of the current day’s range. That day can contribute positively to CMF.

$$\Large{\bf{-----------}}$$

CMF answers a focused question:

> Is volume occurring more often with closes near the top or bottom of each
> period’s range?

The project translates that answer into five mutually exclusive states:

```text
Strong Buy
Buy
Neutral
Sell
Strong Sell
```

The simplest interpretation is:

```text
Positive CMF  = accumulation pressure
Near-zero CMF = no clear pressure advantage
Negative CMF  = distribution pressure
```

Strong states add one more requirement:

```text
The pressure must also be strengthening through two consecutive moves.
```

Therefore:

> **Buy or Sell means directional pressure exists. Strong Buy or Strong Sell
> means that pressure is both unusually large and still strengthening.**




### Simplest mental model

```text
Heavy volume + closes near daily highs
→ pushes CMF upward
→ accumulation pressure

Heavy volume + closes near daily lows
→ pushes CMF downward
→ distribution pressure

Mixed closes or closes near the middle
→ keeps CMF closer to zero
→ no clear pressure advantage
```

### What the displayed number means

The app multiplies the raw CMF value by :gray-background[100] for readability.

| App display | Raw CMF used by the rules |
| :----------: | ------------------------: |
|    :gray-background[+22.0] |     approximately :gray-background[+0.220] |
|    :gray-background[+10.0] |     approximately :gray-background[+0.100] |
|     :gray-background[+5.0] |     approximately :gray-background[+0.050] |
|      :gray-background[0.0] |      approximately :gray-background[0.000] |
|    :gray-background[-10.0] |     approximately :gray-background[-0.100] |
|    :gray-background[-23.0] |     approximately :gray-background[-0.230] |

The multiplication by :gray-background[100] is display-only. Heatmap cells show **one decimal place**; classification and arrow qualification use the **unrounded raw CMF**.

A cell displaying :gray-background[+22.0] does **not** mean “22% price performance.” It means the raw CMF reading is approximately :gray-background[+0.220].


### Why +0.22 is already meaningful

CMF has a theoretical range from :gray-background[-1.00] to :gray-background[+1.00], but its real-world readings normally occupy a much narrower area.

To reach :gray-background[+1.00], every period in the entire lookback would need to close at its exact high.

To reach :gray-background[-1.00], every period would need to close at its exact low.

Because real markets fluctuate inside each day’s range, those theoretical extremes are rarely approached. CMF typically operates within a substantially narrower practical range.

That means a raw CMF of :gray-background[+0.22] is not merely “22% of the way to the maximum.” It is already a materially positive reading within CMF’s normal operating range.


### Quick intuitive model

| Price behavior inside the period | Volume contribution | CMF interpretation |
|---|---:|---|
| Close is near the High | Positive | Accumulation pressure |
| Close is near the Low | Negative | Distribution pressure |
| Close is near the middle | Near zero | Little directional contribution |
| Heavy volume near the High | Large positive contribution | Stronger accumulation evidence |
| Heavy volume near the Low | Large negative contribution | Stronger distribution evidence |
| Light volume | Smaller contribution | Less influence on CMF |

$\Large{\textsf{Simplest translation}}$

> **Heavy volume near the top of the range pushes CMF up**.
> **Heavy volume near the bottom of the range pushes CMF down.**


---

### Value-added use

> Use CMF when you want to know whether recent price behavior is being supported by volume-backed accumulation or distribution rather than looking at price direction alone.

CMF adds a participation layer to the heatmap.

A price move can look bullish while CMF shows weak or negative participation. A price decline can look bearish while CMF shows improving accumulation pressure.

CMF is particularly useful for:

* confirming whether volume supports an uptrend or downtrend;
* identifying persistent accumulation or distribution pressure;
* comparing price direction with participation direction;
* detecting when volume-backed pressure is strengthening or weakening;
* distinguishing small near-zero fluctuations from meaningful pressure states.

### Use with

CMF is most useful when interpreted with price, trend, momentum, and volatility context.

* **Price trend, support, and resistance** — to determine whether CMF confirms a breakout, breakdown, or established trend.
* **EMA or SMA** — to compare volume-backed pressure with the prevailing price trend.
* **ADX** — to determine whether the trend that CMF appears to support has meaningful strength.
* **MACD or ROC** — to see whether price momentum agrees with the accumulation/distribution reading.
* **RSI, MFI, or Stochastic** — to compare CMF’s participation signal with momentum or exhaustion conditions.
* **OBV or raw volume** — to compare CMF’s closing-location method with another participation measure.
* **ATR or ATRP** — to understand whether changes are occurring in a high- or low-volatility environment.

### Important distinction

The project uses a **directional-pressure plus continuation-confirmation** model.

```text
Positive CMF
→ accumulation pressure

Negative CMF
→ distribution pressure

Near-zero CMF
→ no clear pressure advantage

Large positive or negative CMF
+ strengthening across two moves
→ Strong state
```

This is not primarily:
* an overbought/oversold reversal model;
* a price-valuation model;
* a crossover-event model;
* a formal divergence model;
* a standalone trading system.

The labels '***Buy***' and '***Sell***' are project signal names.

In CMF terms:

```text
Buy
= accumulation pressure

Sell
= distribution pressure
```

They are not automatic instructions to buy or sell the stock.

---

## How to read the CMF(21) heatmap
(:small[[Back to top](#summary-cmf-21-signals)])

Each CMF(21) cell answers two related questions:
1. **What is the current volume-backed pressure reading?**
2. **Which project signal does that reading satisfy?**

The color comes from the rule-engine score:

| Signal      | Score | General color meaning       |
| ----------- | ----: | --------------------------- |
| Strong Buy  | :gray-background[+2] | strongest bullish CMF state |
| Buy         | :gray-background[+1] | bullish CMF state           |
| Neutral     | :gray-background[0] | no directional CMF state    |
| Sell        | :gray-background[-1] | bearish CMF state           |
| Strong Sell | :gray-background[-2] | strongest bearish CMF state |

The number printed in the cell is the scaled CMF value, not the score.

For example:

```text
Cell value: +22
Cell color: dark green
```

means:

* the raw CMF value is approximately :gray-background[+0.22];
* the classifier assigned Strong Buy, with a score of :gray-background[+2];
* the value alone was not enough—the two-move confirmation also had to be satisfied.

### The three questions behind the CMF(21) rules

| Question                                               | CMF(21) test                                   | What it determines                                      |
| ------------------------------------------------------ | ---------------------------------------------- | ------------------------------------------------------- |
| Is there enough pressure to leave Neutral?             | Above :gray-background[+0.10] or below :gray-background[-0.10]                 | Whether a Buy or Sell side exists at all                |
| Is the pressure large enough to be a Strong candidate? | Above :gray-background[+0.20] or below :gray-background[-0.20]                 | Whether magnitude qualifies for possible Strong status  |
| Is that large pressure strengthening consistently?     | Rising or falling across two consecutive moves | Whether the candidate becomes Strong Buy or Strong Sell |

The logic is layered:

```text
±0.10:
Is meaningful directional pressure present?

±0.20:
Is that pressure large enough for a CMF(21) Strong candidate?

Two-move confirmation:
Has that large pressure strengthened through both recent moves?
```

### Practical reading scale

This table is a reading aid, not a universal five-state industry standard.

| App display area |       Raw CMF area | Practical reading                                                                             |
| ---------------: | -----------------: | --------------------------------------------------------------------------------------------- |
|      Above :gray-background[+25] |      Above :gray-background[+0.25] | Large positive accumulation-pressure reading; a Strong Buy **candidate**, depending on the period and two-move confirmation. |
| :gray-background[+10] to :gray-background[+25] | :gray-background[+0.10] to :gray-background[+0.25] | Qualified accumulation pressure above +10; Strong status depends on the period-specific cutoff and confirmation. |
| :gray-background[-10] to :gray-background[+10] | :gray-background[-0.10] to :gray-background[+0.10] | Neutral: neither directional pressure exceeds the project cutoff; CMF can still rise or fall. |
| :gray-background[-25] to :gray-background[-10] | :gray-background[-0.25] to :gray-background[-0.10] | Qualified distribution pressure below −10; Strong status depends on the period-specific cutoff and confirmation. |
|      Below :gray-background[-25] |      Below :gray-background[-0.25] | Large negative distribution-pressure reading; a Strong Sell **candidate**, depending on the period and two-move confirmation. |

This practical magnitude guide and the project signal rules are related but not identical:

```text
Practical magnitude guide:
How positive or negative is the CMF level?

Project signal:
What is the CMF level, and—for Strong states—
has it strengthened across two consecutive moves?
```

Therefore:

* :gray-background[+24] can be **Buy** if it lacks the required two-move rise.
* :gray-background[+22] can be **Strong Buy** if its raw value is above :gray-background[+0.20] and it has risen across both recent moves.
* :gray-background[-23] can be **Sell** if it lacks the required two-move decline.
* :gray-background[-21] can be **Strong Sell** if its raw value is below :gray-background[-0.20] and it has fallen across both recent moves.


**Important rounding note**:
Heatmap cells show **one decimal place** (raw CMF × 100), but classification and arrow comparisons use full-precision raw values.

For example, raw :gray-background[+0.0996] and :gray-background[+0.1004] both display approximately :gray-background[+10.0]. The first remains Neutral; the second qualifies for Buy.

At a displayed boundary, trust the **Signal** and its Rule explanation rather than reverse-engineering the classification from the rounded number. An arrow is a separate directional observation, never a change to that Signal.

---

### The CMF patterns you should not overlook
(:small[[Parent](#how-to-read-the-cmf-21-heatmap)] | **Related:** :small[[Most Important Patterns](#most-important-patterns)])

Read **cell value + arrow + Signal color** together. The examples are illustrative; the actual Signal is always determined from the raw rulebook conditions.

| Pattern | What it means | Why to notice it |
|---|---|---|
| **:red-background[Sell]** :red[−29.1]**↗** | CMF remains below −10 but has increased across 2 moves. | Qualified distribution pressure is **easing**, even if the Sell background has not changed. |
| **:green-background[Buy]** :blue[+18.4]**↘** | CMF remains above +10 but has decreased across 2 moves. | Qualified accumulation pressure is **easing**, despite the Buy background. |
| **:gray-background[Neutral]** :red[−7.0]**↘** | CMF has fallen for 4 moves; the latest reading is still within ±10. | Negative distribution bias is **building**, but Sell has **not** qualified. |
| **:gray-background[Neutral]** :red[−3.0]**↗** | CMF has risen for 4 moves while still negative. | Negative distribution bias is **fading**; an upward arrow does not establish Buy. |
| **:gray-background[Neutral]** :blue[+7.0]**↗** | CMF has risen for 4 moves while positive. | Positive accumulation bias is **building** without qualifying for Buy. |
| **:gray-background[Neutral]** :blue[+3.0]**↘** | CMF has fallen for 4 moves while positive. | Positive accumulation bias is **fading**; a downward arrow does not establish Sell. |
| **:green-background[Strong Buy]** :blue[+22.0] | CMF(21) is above +20 and rose across 2 moves. | Substantial accumulation pressure is still strengthening; **no easing arrow** is added. |
| **:red-background[Strong Sell]** :red[−23.0] | CMF(21) is below −20 and fell across 2 moves. | Substantial distribution pressure is still strengthening; **no easing arrow** is added. |
| **Price up + :red-background[Sell]** | Daily price gained, but CMF still qualifies as distribution. | Price direction and longer-window pressure are in **tension**; check the Bottom-line for today's comparison. |
| **Price down + :green-background[Buy]** | Daily price declined, but CMF still qualifies as accumulation. | Price direction and longer-window pressure are in **tension**; neither is a guaranteed forecast. |


**Priority:** \
- First inspect qualified Buy/Sell cells with easing arrows and Neutral cells showing persistent movement toward or across zero.
- Then use the hover's Rule and Bottom-line to understand the actual evidence.
- **An arrow alone is not a trade signal.**

**Neutral timing:** Four moves require **five** successive valid CMF readings. Only the *current* observation must be Neutral; prior readings may have been Buy or Sell. An arrow can therefore appear on the first visible day of a heatmap if sufficient earlier history exists. Missing or tied observations do not qualify. Strong Buy/Sell cells never receive arrows.

#### How to prioritize the CMF patterns

| Tier | Priority                        | Patterns                       |
| ---- | ------------------------------- | ------------------------------ |
| 1    | **Pressure weakening**          | Sell ↗ / Buy ↘                 |
| 2    | **Strong pressure confirmed**   | Strong Buy / Strong Sell       |
| 3    | **Price–CMF disagreement**      | Price ↑ + Sell / Price ↓ + Buy |
| 4    | **Directional bias developing** | Neutral +↗ / −↘                |
| 5    | **Unqualified pressure fading** | Neutral −↗ / +↘                |

**Reading priority:** Focus first on qualified pressure that is weakening or strengthening, then examine whether CMF confirms the prevailing price trend. Use Neutral arrows as early context, not formal Buy/Sell signals.

**Important:** These tiers rank practical interpretation value—not predictive accuracy or trading profitability.

---

### How to Read: 'Strong Buy'
(:small[[Parent](#how-to-read-the-cmf-21-heatmap)])
(:small[[See: 'Strong Buy'](#strong-buy-cmf)])

```json
"strong_buy": "CMF_21 > 0.20 and rising_2bar(CMF_21)"
```

A Strong Buy requires **both**:
1. CMF is above the CMF(21) Strong threshold of :gray-background[+0.20].
2. CMF has risen through both recent comparisons:

```text
current CMF > prior CMF > CMF two periods ago
```

Example:

```text
CMF sequence: +0.20 → +0.22 → +0.24
Displayed:       +20 →    +22 →    +24
```

At the latest observation:

* :gray-background[+0.24] is above the :gray-background[+0.20] Strong threshold;
* :gray-background[+0.24 > +0.22];
* :gray-background[+0.22 > +0.20].

The value is already high, and pressure has continued strengthening.

#### How one beginner could explain it to another

> Over the last 21 trading days, volume has been associated much more with strong closes than weak closes.
> - That buying-pressure reading is already high, and it has continued increasing for two straight moves.

#### Bottom-line

> **Buying pressure is high and still strengthening.**

#### What it does not mean

Strong Buy does not mean:

* the stock is inexpensive;
* price is guaranteed to rise next;
* a known institution definitely purchased shares;
* the user should automatically place a buy order.

It is a strong **CMF accumulation-pressure state**, not a valuation opinion or guaranteed forecast.

---

### How to Read: 'Buy'
(:small[[Parent](#how-to-read-the-cmf-21-heatmap)])
(:small[[See: 'Buy'](#buy-cmf)])

```json
"buy": "CMF_21 > 0.10 and (CMF_21 <= 0.20 or not_rising_2bar(CMF_21))"
```

Buy is easier to understand when separated into two steps.

#### Step 1 — Accumulation pressure exists

```text
CMF_21 > +0.10
```

The reading has crossed the positive Buy cutoff and left Neutral.

Beginner translation:

> Over the 21-day lookback, volume has favored stronger closes enough to indicate meaningful accumulation pressure.

#### Step 2 — The complete Strong Buy combination is absent

At least one of these is true:

```text
CMF_21 <= +0.20
```

or:

```text
CMF has not risen across both recent moves
```

That produces two possible Buy cases.

#### Buy case A — Positive, but not above the Strong threshold

```text
Current raw CMF: +0.15
Displayed value: +15
```

This is above the :gray-background[+0.10] Buy cutoff but not above the :gray-background[+0.20] Strong threshold.

Translation:

> Buying pressure exists, but its magnitude is not high enough to qualify for Strong Buy.

#### Buy case B — Above the Strong threshold, but not steadily rising

```text
CMF sequence: +0.20 → +0.18 → +0.22
Displayed:       +20 →    +18 →    +22
```

The latest value is above :gray-background[+0.20], but the sequence did not rise through both moves. It first fell and then rose.

Translation:

> Buying pressure is high, but it has not strengthened steadily for two straight moves.

#### How one beginner could explain it to another

> Volume currently favors buying pressure.
> - However, the pressure is either not high enough to be called Strong, or it is high but has not increased steadily for two straight moves.

#### Bottom-line

> **Buying pressure exists, but it is not both high and steadily strengthening.**

The shortest accurate distinction is:

```text
Buy:
buying pressure exists

Strong Buy:
buying pressure is high
and has strengthened twice in succession
```

---

### How to Read: 'Neutral'
(:small[[Parent](#how-to-read-the-cmf-21-heatmap)])
(:small[[See: 'Neutral'](#neutral-cmf)])

```json
"neutral": "-0.10 <= CMF_21 <= 0.10"
```

Neutral means the raw CMF value is inside the middle zone from :gray-background[-0.10] through :gray-background[+0.10].

The displayed equivalent is approximately:

```text
-10 through +10
```

This does not require CMF to equal exactly zero.

Examples of Neutral readings include:

```text
+8
+3
0
-4
-9
```

A positive Neutral value such as :gray-background[+8] means:

> Buying pressure has a slight advantage, but not enough to cross the project’s :gray-background[+10] Buy cutoff.

A negative Neutral value such as :gray-background[-7] means:

> Selling pressure has a slight advantage, but not enough to cross the project’s :gray-background[-10] Sell cutoff.

#### How one beginner could explain it to another

> Over the last 21 trading days, neither stronger closes nor weaker closes carried enough volume advantage to produce a clear directional signal.

#### Bottom-line

> **Neither buying nor selling pressure has a clear enough advantage.**

#### What Neutral does not mean

Neutral does not necessarily mean:

* price is flat;
* volume is low;
* CMF equals exactly zero;
* buyers and sellers traded equal numbers of shares;
* the stock has no trend;
* nothing important is occurring.

It means only that CMF remains inside the project’s middle pressure zone.

CMF can also be rising quickly while still Neutral:

```text
-0.08 → +0.01 → +0.09
```

The latest value remains below the :gray-background[+0.10] Buy cutoff, so the result is Neutral.

---

### How to Read: 'Sell'
(:small[[Parent](#how-to-read-the-cmf-21-heatmap)])
(:small[[See: 'Sell'](#sell-cmf)])

```json
"sell": "CMF_21 < -0.10 and (CMF_21 >= -0.20 or not_falling_2bar(CMF_21))"
```

Sell mirrors Buy.

#### Step 1 — Distribution pressure exists

```text
CMF_21 < -0.10
```

The reading has crossed the negative Sell cutoff and left Neutral.

Beginner translation:

> Over the 21-day lookback, volume has favored weaker closes enough to indicate meaningful distribution pressure.

#### Step 2 — The complete Strong Sell combination is absent

At least one of these is true:

```text
CMF_21 >= -0.20
```

or:

```text
CMF has not fallen across both recent moves
```

That produces two possible Sell cases.

#### Sell case A — Negative, but not below the Strong Sell threshold

```text
Current raw CMF: -0.15
Displayed value: -15
```

This is below the :gray-background[-0.10] Sell cutoff but not below the :gray-background[-0.20] Strong Sell threshold.

Translation:

> Selling pressure exists, but its magnitude is not high enough to qualify for Strong Sell.

#### Sell case B — Below the Strong Sell threshold, but not steadily falling

```text
CMF sequence: -0.19 → -0.18 → -0.23
Displayed:       -19 →    -18 →    -23
```

The latest value is below :gray-background[-0.20], but the sequence did not fall through both moves. It first became less negative and then became more negative.

Translation:

> Selling pressure is high, but it has not worsened steadily for two straight moves.

#### How one beginner could explain it to another

> Volume currently favors selling pressure. However, the pressure is either not high enough to be called Strong, or it is high but has not worsened steadily for two straight moves.

#### Bottom-line

> **Selling pressure exists, but it is not both high and steadily strengthening.**

On the negative side, “strengthening” means becoming progressively more negative.

---

### How to Read: 'Strong Sell'
(:small[[Parent](#how-to-read-the-cmf-21-heatmap)])
(:small[[See: 'Strong Sell'](#strong-sell-cmf)])

```json
"strong_sell": "CMF_21 < -0.20 and falling_2bar(CMF_21)"
```

A Strong Sell requires **both**:

1. CMF is below the CMF(21) Strong Sell threshold of :gray-background[-0.20].
2. CMF has fallen through both recent comparisons:

```text
current CMF < prior CMF < CMF two periods ago
```

Example:

```text
CMF sequence: -0.20 → -0.22 → -0.29
Displayed:       -20 →    -22 →    -29
```

At the latest observation:

* :gray-background[-0.29] is below the :gray-background[-0.20] Strong Sell threshold;
* :gray-background[-0.29 < -0.22];
* :gray-background[-0.22 < -0.20].

The distribution reading is already high in magnitude, and it has continued strengthening.

#### How one beginner could explain it to another

> Over the last 21 trading days, volume has been associated much more with weak closes than strong closes. That selling-pressure reading is already high, and it has continued worsening for two straight moves.

#### Bottom-line

> **Selling pressure is high and still strengthening.**

Strong Sell is not a guaranteed prediction that price will fall next. It is the strongest negative CMF state in the current rule model.

---

## CMF formula — what is being measured
(:small[[Back to top](#summary-cmf-21-signals)])

CMF is calculated in three conceptual steps.

### Step 1 — Money Flow Multiplier
(:small[[Parent: 'CMF formula — What's being measured'](#cmf-formula-what-is-being-measured)])

---
**Interpreting different multiplier values**

| Multiplier | Where price closed                   |
| ---------- | ------------------------------------ |
| +1.00      | Exactly at the day's high            |
| +0.80      | Very near the high                   |
| +0.40      | Upper half of the range              |
| 0.00       | Exactly halfway between high and low |
| −0.40      | Lower half of the range              |
| −0.60      | Near the low                         |
| −1.00      | Exactly at the day's low             |


---
**Calculating the CMF Multiplier**

```text
Money Flow Multiplier
= ((Close - Low) - (High - Close)) / (High - Low)
```

Equivalent form:

```text
Money Flow Multiplier
= (2 × Close - High - Low) / (High - Low)
```

This measures where the closing price sits inside that period’s High–Low range.

| Closing position   | Approximate multiplier | Meaning                        |
| ------------------ | ---------------------: | ------------------------------ |
| At the period High |               :gray-background[+1.0] | maximum positive contribution  |
| Above the midpoint |               positive | accumulation-side contribution |
| At the midpoint    |                :gray-background[0.0] | no directional contribution    |
| Below the midpoint |               negative | distribution-side contribution |
| At the period Low  |               :gray-background[-1.0] | maximum negative contribution  |

If :gray-background[High == Low], the period has no usable range width; the implementation avoids dividing by zero.



### Step 2 — Money Flow Volume
(:small[[Parent: 'CMF formula — What's being measured'](#cmf-formula-what-is-being-measured)])

```text
Money Flow Volume
= Money Flow Multiplier × Volume
```

Volume gives more weight to periods with heavier trading.

For example:

* a close near the High on heavy volume creates a large positive contribution;
* a close near the Low on heavy volume creates a large negative contribution;
* the same closing location on light volume has less influence.

### Step 3 — Chaikin Money Flow
(:small[[Parent: 'CMF formula — What's being measured'](#cmf-formula-what-is-being-measured)])

```text
CMF(n)
= Sum of Money Flow Volume over n periods
  / Sum of Volume over n periods
```

The final result is a volume-weighted average of closing-location pressure over the selected period.

### Important implication
(:small[[Parent: 'CMF formula — What's being measured'](#cmf-formula-what-is-being-measured)])

CMF does not directly count “buy orders” and “sell orders.”

“Accumulation” and “distribution” are interpretations inferred from:

* closing location within the period’s range;
* volume attached to that closing location;
* persistence of those contributions across the lookback.

CMF can serve as a proxy for volume-backed buying or selling behavior, but it does not identify the traders responsible.

---

## CMF(21) Rule Translation
(:small[[Back to top](#summary-cmf-21-signals)])

### Strong buy (CMF)
(:small[[Parent](#cmf-21-rule-translation)])
(:small[[See: 'How to read: Strong Buy'](#how-to-read-strong-buy)])

```json
"strong_buy": "CMF_21 > 0.20 and rising_2bar(CMF_21)"
```

#### Literal component breakdown

:blue-background[CMF_21 > 0.20]

* The current raw CMF(21) value is above :gray-background[+0.20].
* This is above the project’s CMF(21) positive Strong threshold.
* On the heatmap’s scaled display, this is approximately above :gray-background[+20].
* Layman’s translation: **the 21-period accumulation-pressure reading is already high.**

:blue-background[rising_2bar(CMF_21)]

* The helper evaluates three consecutive CMF observations.
* It requires:

```text
current CMF > prior CMF > CMF two periods ago
```

* There are two consecutive upward moves.
* Layman’s translation: **CMF has strengthened twice in succession.**

:blue-background[CMF_21 > 0.20 and rising_2bar(CMF_21)]

* Both conditions must be true.
* A high reading without the rising sequence is not Strong Buy.
* A rising reading below or at the Strong threshold is not Strong Buy.
* Layman’s translation: **buying pressure is both high and still getting stronger.**

#### Literal summary

CMF(21) is above :gray-background[+0.20], and the current value is greater than the prior value, which is greater than the value two periods earlier.

#### Plain-English version

The 21-period CMF reading shows substantial accumulation pressure, and that pressure has increased across both recent moves.

#### Interpretation

This is a **strong bullish accumulation-continuation state**.

It requires:
1. high positive CMF magnitude;
2. strict two-move strengthening.

#### Notes / confidence
* High confidence on the literal interpretation.
* Positive CMF as accumulation pressure is conventional.
* The exact five-state scoring system and two-move Strong confirmation are project-specific.
* :gray-background[+0.20] is the approved CMF(21) Strong threshold.
* Strong Buy does not guarantee that price will rise next.

---

### Buy (CMF)
(:small[[Parent](#cmf-21-rule-translation)] | :small[[See: 'How to read: Buy'](#how-to-read-buy)])

```json
"buy": "CMF_21 > 0.10 and (CMF_21 <= 0.20 or not_rising_2bar(CMF_21))"
```

#### Literal component breakdown

:blue-background[CMF_21 > 0.10]

* The current raw CMF(21) value is above :gray-background[+0.10].
* The reading crossed the project’s positive Buy cutoff.
* It is outside Neutral on the accumulation side.
* Layman’s translation: **meaningful buying pressure is present.**

:blue-background[CMF_21 <= 0.20]

* The current value is no higher than the CMF(21) Strong threshold.
* Example: :gray-background[+0.15] is Buy-side pressure but not a Strong candidate.
* Layman’s translation: **buying pressure exists, but the reading is not above the Strong threshold.**

:blue-background[not_rising_2bar(CMF_21)]

* The following strict sequence is not true:

```text
current CMF > prior CMF > CMF two periods ago
```

* The sequence may have risen then fallen, fallen then risen, stayed flat during either comparison, or fallen through both moves.
* Layman’s translation: **CMF has not strengthened steadily through both recent moves.**

:blue-background[CMF_21 <= 0.20 or not_rising_2bar(CMF_21)]

* Only one of the two conditions must be true.
* It captures:

  * readings above :gray-background[+0.10] but no higher than :gray-background[+0.20]; and
  * readings above :gray-background[+0.20] that lack the required two-move rise.
* Layman’s translation: **the reading does not have the complete “high and steadily strengthening” Strong Buy combination.**

#### Literal summary

CMF(21) is above :gray-background[+0.10], but it is either no higher than :gray-background[+0.20] or has not risen through both recent moves.

#### Plain-English version

CMF shows meaningful accumulation pressure, but the pressure is not both above the Strong threshold and steadily strengthening.

#### Interpretation

This is a **bullish accumulation-pressure state without complete Strong confirmation**.

#### Notes / confidence

* Buy is intentionally weaker than Strong Buy.
* A CMF value above :gray-background[+0.20] can still be Buy.
* Magnitude alone does not determine the Strong state.
* Buy means accumulation pressure—not a guaranteed entry signal.

---

### Neutral (CMF)
(:small[[Parent](#cmf-21-rule-translation)] | :small[[See: 'How to read: Neutral'](#how-to-read-neutral)])


```json
"neutral": "-0.10 <= CMF_21 <= 0.10"
```

#### Literal component breakdown

:blue-background[-0.10 <= CMF_21]

* CMF is not below the project’s negative Sell cutoff.
* Distribution pressure has not become large enough to activate Sell.
* Layman’s translation: **selling pressure is not large enough to create a negative CMF signal.**

:blue-background[CMF_21 <= 0.10]

* CMF is not above the project’s positive Buy cutoff.
* Accumulation pressure has not become large enough to activate Buy.
* Layman’s translation: **buying pressure is not large enough to create a positive CMF signal.**

:blue-background[-0.10 <= CMF_21 <= 0.10]

* Exact raw values of :gray-background[-0.10] and :gray-background[+0.10] are included.
* Layman’s translation: **CMF is inside the middle pressure zone.**

#### Literal summary

CMF(21) is between :gray-background[-0.10] and :gray-background[+0.10], inclusive.

#### Plain-English version

Neither accumulation nor distribution has enough of a volume-backed advantage to cross the project’s directional cutoff.

#### Interpretation

This is a **balanced / no-active-direction CMF state**.

#### Notes / confidence

* :gray-background[+0.10] is Neutral; Buy requires strictly greater than :gray-background[+0.10].
* :gray-background[-0.10] is Neutral; Sell requires strictly less than :gray-background[-0.10].
* Recent direction does not override the Neutral zone.
* Neutral does not mean price has no trend or that volume is low.

---

### Sell (CMF)
(:small[[Parent](#cmf-21-rule-translation)] | :small[[See: 'How to read: Sell'](#how-to-read-sell)])

```json
"sell": "CMF_21 < -0.10 and (CMF_21 >= -0.20 or not_falling_2bar(CMF_21))"
```

#### Literal component breakdown

:blue-background[CMF_21 < -0.10]

* The current raw value is below :gray-background[-0.10].
* It crossed the project’s negative Sell cutoff.
* It is outside Neutral on the distribution side.
* Layman’s translation: **meaningful selling pressure is present.**

:blue-background[CMF_21 >= -0.20]

* The current value is no lower than the CMF(21) Strong Sell threshold.
* Example: :gray-background[-0.15] is Sell-side pressure but not a Strong candidate.
* Layman’s translation: **selling pressure exists, but the reading is not below the Strong Sell threshold.**

:blue-background[not_falling_2bar(CMF_21)]

* The following strict sequence is not true:

```text
current CMF < prior CMF < CMF two periods ago
```

* The sequence may have fallen then risen, risen then fallen, stayed flat during either comparison, or risen through both moves.
* Layman’s translation: **CMF has not worsened steadily through both recent moves.**

:blue-background[CMF_21 >= -0.20 or not_falling_2bar(CMF_21)]

* Only one condition must be true.
* It captures:

  * readings below :gray-background[-0.10] but no lower than :gray-background[-0.20]; and
  * readings below :gray-background[-0.20] that lack the required two-move decline.
* Layman’s translation: **the reading does not have the complete “high and steadily strengthening” Strong Sell combination.**

#### Literal summary

CMF(21) is below :gray-background[-0.10], but it is either no lower than :gray-background[-0.20] or has not fallen through both recent moves.

#### Plain-English version

CMF shows meaningful distribution pressure, but the pressure is not both below the Strong Sell threshold and steadily strengthening.

#### Interpretation

This is a **bearish distribution-pressure state without complete Strong confirmation**.

#### Notes / confidence

* Sell is intentionally weaker than Strong Sell.
* A value below :gray-background[-0.20] can still be Sell.
* Magnitude alone does not determine the Strong state.
* Sell means distribution pressure—not a guaranteed exit signal.

---

### Strong sell (CMF)
(:small[[Parent](#cmf-21-rule-translation)])
(:small[[See: 'How to read: Strong Sell'](#how-to-read-strong-sell)])

```json
"strong_sell": "CMF_21 < -0.20 and falling_2bar(CMF_21)"
```

#### Literal component breakdown

:blue-background[CMF_21 < -0.20]

* The current raw value is below :gray-background[-0.20].
* This is below the CMF(21) Strong Sell threshold.
* On the scaled display, this is approximately below :gray-background[-20].
* Layman’s translation: **the 21-period distribution-pressure reading is already high.**

:blue-background[falling_2bar(CMF_21)]

* The helper evaluates three observations.
* It requires:

```text
current CMF < prior CMF < CMF two periods ago
```

* There are two consecutive downward moves.
* Layman’s translation: **CMF has become more negative twice in succession.**

:blue-background[CMF_21 < -0.20 and falling_2bar(CMF_21)]

* Both conditions must be true.
* A deeply negative reading without the falling sequence is not Strong Sell.
* A falling reading above or at the threshold is not Strong Sell.
* Layman’s translation: **selling pressure is both high and still getting stronger.**

#### Literal summary

CMF(21) is below :gray-background[-0.20], and the current value is less than the prior value, which is less than the value two periods earlier.

#### Plain-English version

The 21-period CMF reading shows substantial distribution pressure, and that pressure has increased across both recent moves.

#### Interpretation

This is a **strong bearish distribution-continuation state**.

#### Notes / confidence

* High confidence on the literal interpretation.
* Negative CMF as distribution pressure is conventional.
* The exact five-state system and two-move confirmation are project-specific.
* :gray-background[-0.20] is the approved CMF(21) Strong Sell threshold.
* Strong Sell does not guarantee that price will fall next.

---

## Industry-standard baseline and project calibration
(:small[[Back to top](#summary-cmf-21-signals)])

Industry practice generally agrees that:

* CMF is a volume-weighted accumulation/distribution indicator.
* Positive CMF indicates accumulation or buying pressure.
* Negative CMF indicates distribution or selling pressure.
* Zero is the natural centerline.
* CMF can confirm or question price trends and breakouts.
* Its theoretical :gray-background[-1] to :gray-background[+1] extremes are rarely reached.
* Its practical range is substantially narrower.

Industry practice does **not** define one universal:

```text
Strong Buy / Buy / Neutral / Sell / Strong Sell
```

classification system.


### Practical magnitude context

|            Raw CMF | Scaled display | Practical interpretation               |
| -----------------: | -------------: | -------------------------------------- |
|      Above :gray-background[+0.25] |    Above :gray-background[+25] | unusually strong accumulation pressure |
| :gray-background[+0.10] to :gray-background[+0.25] | :gray-background[+10] to :gray-background[+25] | meaningful accumulation pressure       |
| :gray-background[-0.10] to :gray-background[+0.10] | :gray-background[-10] to :gray-background[+10] | weak, mixed, or inconclusive pressure  |
| :gray-background[-0.25] to :gray-background[-0.10] | :gray-background[-25] to :gray-background[-10] | meaningful distribution pressure       |
|      Below :gray-background[-0.25] |    Below :gray-background[-25] | unusually strong distribution pressure |

This is a practical reading guide, not a universal formal rulebook.


### Conventional elements (Basic Interpretation)

| Condition                       | Basic translation                                |
| ------------------------------- | ------------------------------------------------ |
| CMF above zero                  | volume-backed pressure leans toward accumulation |
| CMF below zero                  | volume-backed pressure leans toward distribution |
| CMF near zero                   | neither side has a clear pressure advantage      |
| Positive CMF during an uptrend  | participation may **confirm** the uptrend        |
| Negative CMF during an uptrend  | participation may *question* the uptrend         |
| Negative CMF during a downtrend | participation may **confirm** the downtrend      |
| Positive CMF during a downtrend | participation may *question* the downtrend       |


* positive values represent accumulation pressure;
* negative values represent distribution pressure;
* a middle area around zero filters weak readings;
* larger absolute values represent stronger pressure;
* sustained direction can provide confirmation.

### Project-specific elements

* the five signal labels;
* scores from :gray-background[-2] through :gray-background[+2];
* the common :gray-background[±0.10] Neutral-zone cutoffs;
* period-specific Strong thresholds;
* strict two-move Strong confirmation;
* the :gray-background[×100] display;
* exact boundary behavior.

### Buy/Sell cutoffs versus Strong thresholds

| Threshold type                 |          CMF(21) value | Question answered                                                    |
| ------------------------------ | ---------------------: | -------------------------------------------------------------------- |
| Positive Buy cutoff            |             :gray-background[+0.10] | Is accumulation pressure large enough to leave Neutral?              |
| Negative Sell cutoff           |             :gray-background[-0.10] | Is distribution pressure large enough to leave Neutral?              |
| Positive Strong threshold      |             :gray-background[+0.20] | Is accumulation pressure large enough for Strong Buy consideration?  |
| Negative Strong Sell threshold |             :gray-background[-0.20] | Is distribution pressure large enough for Strong Sell consideration? |
| Two-move confirmation          | three CMF observations | Is that large pressure still strengthening consistently?             |

The :gray-background[±0.10] cutoffs create a buffer around zero so tiny fluctuations do not continually alternate between Buy and Sell.

The Strong thresholds test magnitude. The directional helper then tests continuation.



---

## Comparison of the four CMF settings
(:small[[Back to top](#summary-cmf-21-signals)])

All four settings use the same :gray-background[±0.10] Buy/Sell cutoffs and the same five-state model.

Their Strong thresholds differ because longer, smoother CMF series generally occupy narrower empirical ranges.

| Setting   | Relative speed      | Strong threshold | What it emphasizes                          | Main trade-off                                 |
| --------- | ------------------- | ---------------: | ------------------------------------------- | ---------------------------------------------- |
| CMF(10) | Fastest             |       :gray-background[±0.25]| short-term changes in pressure              | reacts quickly, but changes state more often   |
| CMF(21) | Standard / balanced |       :gray-background[±0.20]| approximately one trading month of pressure | balances responsiveness and persistence        |
| CMF(30) | Medium-slow         |      :gray-background[±0.175]| more sustained pressure                     | smoother, but slower to react                  |
| CMF(50) | Slowest             |       :gray-background[±0.15] | persistent longer-horizon pressure          | filters more noise, but confirms changes later |

### Practical selection guide

```text
Use CMF(10)
when short-term changes matter most.

Use CMF(21)
when you want the balanced standard view.

Use CMF(30)
when you want a smoother medium-slow view.

Use CMF(50)
when persistence matters more than early response.
```

These are different time-horizon views of the same concept. They should not be treated as four independent votes of equal meaning.

---

## Rule interpretation tables
(:small[[Back to top](#summary-cmf-21-signals)])

### CMF(21) rules interpretation

| Source      | Signal      | Rule logic                                                         | What’s happening                                                                           | Answers the question                                                                  | Bottom-line                                                                      |
| ----------- | ----------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **CMF(21)** | Strong Buy  | :gray-background[CMF_21 > 0.20 and rising_2bar(CMF_21)]                           | CMF is above the positive Strong threshold and has risen across both recent moves.         | *“Is accumulation pressure already high and still strengthening consistently?”*       | **Buying pressure is high and still strengthening.**                             |
| **CMF(21)** | Buy         | :gray-background[CMF_21 > 0.10 and (CMF_21 <= 0.20 or not_rising_2bar(CMF_21))]   | CMF is above the positive Buy cutoff, but the complete Strong Buy combination is absent.   | *“Is meaningful accumulation pressure present without complete Strong confirmation?”* | **Buying pressure exists, but it is not both high and steadily strengthening.**  |
| **CMF(21)** | Neutral     | :gray-background[-0.10 <= CMF_21 <= 0.10]                                         | CMF remains inside the middle pressure zone.                                               | *“Has neither side gained enough of a volume-backed advantage to leave Neutral?”*     | **Neither side has a clear volume-backed pressure advantage.**                   |
| **CMF(21)** | Sell        | :gray-background[CMF_21 < -0.10 and (CMF_21 >= -0.20 or not_falling_2bar(CMF_21))]| CMF is below the negative Sell cutoff, but the complete Strong Sell combination is absent. | *“Is meaningful distribution pressure present without complete Strong confirmation?”* | **Selling pressure exists, but it is not both high and steadily strengthening.** |
| **CMF(21)** | Strong Sell | :gray-background[CMF_21 < -0.20 and falling_2bar(CMF_21)]                         | CMF is below the negative Strong Sell threshold and has fallen across both recent moves.   | *“Is distribution pressure already high and still strengthening consistently?”*       | **Selling pressure is high and still strengthening.**                            |


---

## Understanding the CMF hover
(:small[[Back to top](#summary-cmf-21-signals)])

The three heatmaps share the same authoritative CMF classification, Rule explanation and Context Interpretation. The opening layout differs slightly: **Rolling** leads with the indicator Value; **SCD Single Indicator** also shows price/volume context where available; **SCD Multiple Indicators** retains its trailing raw-payload summary. These additions do **not** change CMF scoring.

### Hover field map
(:small[[Parent](#understanding-the-cmf-hover)])

| Field | What it tells you | Source / interpretation |
|---|---|---|
| **Value** | Current CMF × 100, to one decimal. | Numeric CMF level; the **cell-only** :red-background[↗] / :red-background[↘] suffix is not part of the hover's Value. |
| **Δ vs prior day** | Current minus prior CMF, shown in scaled CMF points; a relative change may also appear. | One-session change, **not** a four-move trend. |
| **Trend** | Rising, Falling or Flat relative to the previous CMF observation. | One CMF move only. |
| **Signal** | Strong Buy / Buy / Neutral / Sell / Strong Sell. | Authoritative rule-engine state; determines the background color. |
| **2-move confirmation** | Rising across 2 moves, Falling across 2 moves, Not met or Not available. | Uses three valid CMF readings; relevant to Strong qualification. It is **not** the Neutral arrow's four-move test. |
| **Rule** | The actual threshold and historical evidence explaining this Signal. | Dynamic five-state explanation; shows why Strong did or did not qualify. |
| **CMF Interpretation** | Interprets accumulation, distribution or Neutral from volume-weighted closing locations. | Describes the **CMF measurement window**, not a direct count of buyers or sellers. |
| **Bottom-line** | Relates the latest verified price direction to current CMF pressure and, where established, its recent development. | Price comparison uses aligned canonical **Adjusted Close**, falling back to **Close**; no prediction. |
| **Notes** | Additional rulebook guidance, including the :red-background[↗] / :red-background[↘] legend you've added. | Educational text; does not affect signals. |
| **Definition / How to Read** | Indicator definition and interpretation guidance. | Static explanation text. |

:red[Pressure] and :red[Strong threshold] are **not separate CMF hover fields** in the completed layout. The pressure qualification and period-specific Strong cutoff are conveyed by **Signal**, **Rule** and **CMF Interpretation**.

### Value and delta: concrete example
(:small[[Parent](#understanding-the-cmf-hover)])

```text
Current raw CMF: +0.122
Prior raw CMF:   +0.125
Hover Value:     +12.2
Displayed Δ:    −0.3 CMF points
```

The app multiplies the raw CMF by 100 **only for presentation**. The absolute delta is :gray-background[(current − prior) × 100]. If a relative percentage is shown, it is :gray-background[(current − prior) / abs(prior) × 100]. Very small prior CMF readings can produce large percentages; prefer the signed CMF level and **absolute** delta near zero.

### Trend, confirmation and arrow timing are different
(:small[[Parent](#understanding-the-cmf-hover)])

| Observation | Required history | Example | Meaning |
|---|---:|---|---|
| **Trend: Rising** | 2 CMF readings | :gray-background[−29.9 → −29.1] | The latest CMF move rose. |
| **2-move confirmation: Rising** | 3 CMF readings | :gray-background[−30.9 → −29.9 → −29.1] | Two consecutive increases. |
| **Sell :red-background[↗]** | 3 CMF readings | :gray-background[−30.9 → −29.9 → −29.1] | Distribution pressure easing; Sell remains qualified. |
| **Buy :red-background[↘]** | 3 CMF readings | :gray-background[+22.0 → +20.5 → +18.4] | Accumulation pressure easing; Buy remains qualified. |
| **Neutral :red-background[↗] or :red-background[↘]** | 5 CMF readings | :gray-background[−16 → −13 → −9 → −5 → −2] | Four consecutive moves; only the **latest** reading must be Neutral. |

The **2-move confirmation** field can say :gray-background[Rising across 2 moves] on a Neutral cell even when **no Neutral arrow** appears: the Neutral suffix requires four, not two, monotonic moves. Missing predecessor evidence cannot establish an arrow. A missing *current* CMF value must not be interpreted as a valid Neutral reading. All comparisons use the raw, unrounded observations, including days before the visible heatmap window.

### How to read the Dynamic Rule and Context Interpretation
(:small[[Parent](#understanding-the-cmf-hover)])

Use the NVDA CMF(21) example as a concrete reading:

```text
CMF sequence: −30.9 → −29.9 → −29.1
Signal: Sell
2-move confirmation: Rising across 2 moves
Cell: −29.1↗
```

**Rule:** The current reading is below the −10 distribution cutoff and is also more negative than the CMF(21) Strong Sell threshold of −20. However, CMF **rose**, rather than fell, across the two moves. Thus the Strong Sell magnitude test passes, but its required two-move decline fails; Sell is correct. The Rule identifies the actual failed condition instead of merely repeating the Signal.

**CMF Interpretation:** The weighted closing locations over the **21-session measurement window** favor distribution pressure. This describes the CMF calculation, **not** today's stock-price direction or the identity of market participants.

**Bottom-line:** In this example, price rose on September 15, 2026, while CMF became less negative across the two moves: distribution pressure was **easing**. Daily price movement and 21-session CMF are different observation windows; neither establishes what price must do next.

The Bottom-line is conditional on verified, same-date canonical price observations. If price history is unavailable or misaligned, the display reports that limitation rather than inventing agreement or disagreement. The Context Interpretation also fails closed if the active rulebook or score does not match the approved CMF semantics. **A five-state rule is not finished if a human cannot reconstruct why an observation landed in each state.**

---

## Why price and CMF can move in opposite directions
(:small[[Back to top](#summary-cmf-21-signals)] | :small[[Previous](#understanding-the-cmf-hover)])

CMF and price do not measure the same thing.

Price may rise while CMF falls when:
* the stock rises from the prior close;
* but closes lower within the current day’s range;
* weaker closing locations carry heavier volume;
* or recent positive money-flow contributions fade.

Price may fall while CMF rises when:
* the stock remains below the prior close;
* but closes higher within the current day’s range;
* or stronger closing locations carry heavier volume.

A hover can therefore show:

```text
Trend: Falling | Price: Rising
```

This means:

> Price rose over the comparison, while CMF became less positive or more negative.

That may question the participation behind the price move, but the current project does not convert it into a formal divergence score.

---

## Strengths and limitations
(:small[[Back to top](#summary-cmf-21-signals)])

### Strengths

CMF can help:

* incorporate volume into accumulation/distribution analysis;
* confirm or question participation behind price trends;
* distinguish positive from negative volume-backed pressure;
* show whether pressure is persistent or changing;
* add context unavailable from price-only indicators.

### Limitations

#### CMF infers pressure

CMF does not directly observe:

* who bought or sold;
* whether trades were institution-initiated;
* the direction of every transaction;
* changes in institutional ownership.

#### The current range matters more than the prior close

A stock can gap lower yet produce a positive CMF contribution if it closes near the top of its current High–Low range.

#### Shorter settings can be noisy

CMF(10) responds faster but may change state more often.

#### Longer settings can lag

CMF(30) and CMF(50) smooth more history and may react later.

#### Relative changes near zero can appear extreme

A small prior value can create a large relative percentage even when the absolute CMF change is modest.

#### CMF does not guarantee future price direction
- Positive CMF does not guarantee a price increase.
- Negative CMF does not guarantee a price decline.

- Use CMF with trend, momentum, support/resistance, and broader market context.


---

## Initial audit note
(:small[[Back to top](#summary-cmf-21-signals)])

The earlier CMF rules were not documented as authoritative without review.

The final approved work included:
* confirming canonical raw CMF units;
* correcting computation to use raw :gray-background[Close] consistently with raw :gray-background[High] and :gray-background[Low];
* validating CMF(10), CMF(21), CMF(30), and CMF(50) through the production numeric and classifier paths;
* selecting period-calibrated Strong thresholds;
* making the five states complete and mutually exclusive;
* preserving raw CMF for rules while applying :gray-background[×100] only for display;
* adding CMF-specific hover context;
* verifying behavior in:
  * Rolling Signals Heatmap;
  * SCD Multiple Indicators;
  * SCD Single Indicator.

The final semantic model is:

```text
directional accumulation/distribution pressure
+ period-calibrated magnitude
+ two-move continuation confirmation for Strong states
```

It is not an overbought/oversold reversal model.


---
## My Notes
(:small[[Back to top](#summary-cmf-21-signals)])

CMF is for assessing the prevailing buy or sell pressure over a sustained period. 
- CMF helps confirm trends and potential reversals.


---
**Class**: Volume Indicator

**Purpose:** Measure the amount of money flow volume over a specific period to gauge accumulation/distribution pressure.

**Use when**: You need to assess overall buying/selling pressure over a multi-day period.

**Key Concept:** Combines Accumulation/Distribution Line concept with momentum analysis by averaging the money flow multiplier over a set period (typically 21 days).

**Calculation:** Sum of money flow volume over N periods divided by sum of volume over same N periods. Oscillates between +1 and -1.

**Signals & Interpretation:**
- Above 0 = accumulation bias (buying pressure)
- Below 0 = distribution bias (selling pressure)
- Above +0.25 = strong accumulation
- Below -0.25 = strong distribution
- Zero-line crosses signal changes in money flow direction

**Optimal Conditions:** Effective in both trending and ranging markets. Works well on daily and weekly charts for swing trading analysis.

**Limitations:** Can lag during rapid price movements. May produce whipsaws around the zero line in choppy markets.

**Difference Between: Chaikin Money Flow vs. MFI**:
MFI gives a more direct overbought/oversold signal, whereas CMF is more focused on the overall trend strength and direction of money flow.

The main difference is that: 
- Money Flow Index (MFI) is a momentum oscillator that uses price and volume to identify overbought/oversold conditions, ranging from 0-100
- Chaikin Money Flow (CMF) measures the strength of buying and selling pressure over a longer period, using a multiplier based on the price's closing position within its high-low range, resulting in a range between -1 and +1. 

## Table of Contents
(:small[[Back to top](#summary-cmf-21-signals)])

- [Summary: CMF(21) signals](#summary-cmf-21-signals)
  - [Display-value Customizations: ↗ / ↘](#how-to-read-display-value-customizations)
  - [Most Important Patterns](#most-important-patterns)
  - [CMF period rule comparison](#cmf-period-rule-comparison)
- [CMF(21) — brief overview](#cmf-21-brief-overview)
  - [Simplest mental model](#simplest-mental-model)
  - [What the displayed number means](#what-the-displayed-number-means)
  - [Why +0.22 is already meaningful](#why-0-22-is-already-meaningful)
  - [Quick intuitive model](#quick-intuitive-model)
  - [Value-added use](#value-added-use)
  - [Use with](#use-with)
  - [Important distinction](#important-distinction)
- [How to read the CMF(21) heatmap](#how-to-read-the-cmf-21-heatmap)
  - [The three questions behind the CMF(21) rules](#the-three-questions-behind-the-cmf-21-rules)
  - [Practical reading scale](#practical-reading-scale)
  - [Important rounding note](#important-rounding-note)
  - [The CMF patterns you should not overlook](#the-cmf-patterns-you-should-not-overlook)
    - [How to prioritize the CMF patterns](#how-to-prioritize-the-cmf-patterns)
  - [How to Read: Strong Buy](#how-to-read-strong-buy)
  - [How to Read: Buy](#how-to-read-buy)
  - [How to Read: Neutral](#how-to-read-neutral)
  - [How to Read: Sell](#how-to-read-sell)
  - [How to Read: Strong Sell](#how-to-read-strong-sell)
- [CMF formula — what is being measured](#cmf-formula-what-is-being-measured)
  - [Step 1 — Money Flow Multiplier](#step-1-money-flow-multiplier)
  - [Step 2 — Money Flow Volume](#step-2-money-flow-volume)
  - [Step 3 — Chaikin Money Flow](#step-3-chaikin-money-flow)
  - [Important implication](#important-implication)
- [CMF(21) Rule Translation](#cmf-21-rule-translation)
  - [Strong Buy](#strong-buy-cmf)
  - [Buy](#buy-cmf)
  - [Neutral](#neutral-cmf)
  - [Sell](#sell-cmf)
  - [Strong Sell](#strong-sell-cmf)
- [Industry-standard baseline and project calibration](#industry-standard-baseline-and-project-calibration)
  - [Practical magnitude context](#practical-magnitude-context)
  - [Conventional elements (Basic Interpretation)](#conventional-elements-basic-interpretation)
  - [Project-specific elements](#project-specific-elements)
  - [Buy/Sell cutoffs versus Strong thresholds](#buy-sell-cutoffs-versus-strong-thresholds)
- [Comparison of the four CMF settings](#comparison-of-the-four-cmf-settings)
  - [Practical selection guide](#practical-selection-guide)
- [Rule interpretation tables](#rule-interpretation-tables)
  - [CMF(21) rules interpretation](#cmf-21-rules-interpretation)
- [Understanding the CMF hover](#understanding-the-cmf-hover)
  - [Hover field map](#hover-field-map)
  - [Value and delta: concrete example](#value-and-delta-concrete-example)
  - [Trend, confirmation and arrow timing are different](#trend-confirmation-and-arrow-timing-are-different)
  - [How to read the Dynamic Rule and Context Interpretation](#how-to-read-the-dynamic-rule-and-context-interpretation)
- [Why price and CMF can move in opposite directions](#why-price-and-cmf-can-move-in-opposite-directions)
- [Strengths and limitations](#strengths-and-limitations)
  - [Strengths](#strengths)
  - [Limitations](#limitations)
- [Initial audit note](#initial-audit-note)
- [My Notes](#my-notes)