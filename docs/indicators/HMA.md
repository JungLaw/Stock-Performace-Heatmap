## Summary: How to Interpret HMA
**Class**: Trend / Moving Average
**aka**: Hull Moving Average

The Hull Moving Average (HMA) is designed to follow price more responsively than many conventional moving averages while still providing a smoothed trend reference.
- Fidelity describes HMA as "*an extremely fast and smooth moving average that nearly eliminates lag*".

Because HMA is deliberately responsive, it can whipsaw more in sideways/choppy environments
- Practitioners recommend using HMA **direction** (*'turns'*) in a **trend** context rather than treating every turn as equally meaningful.
	- use a longer HMA to identify prevailing trend from its direction;
	- use a shorter HMA turning upward/downward for entries in the direction of that longer trend


In this app, HMA provides **two different kinds of information**:
1. **[Signal](#understanding-the-hma-signal)** — the current qualified HMA trend state.
2. **[Turning Context](#understanding-turning-context)** — whether the HMA just changed direction and, if so, whether that turn agrees with or opposes the broader trend.


The simplest mental model is:

```text
ATR Distance + 14-bar HMA Slope
→ Signal
→ current trend state

HMA Direction + Trend Context
→ Turn Context
→ fresh timing / transition information
```

These layers answer different questions and should not be treated as competing votes.

---

### Primary HMA Signal — quick reference
See: ['Signal Rules Translation'](#signal-rules-translation)

The primary HMA Signal answers:

> **Is price meaningfully above or below HMA, and does HMA's established trajectory support that direction strongly enough?**

| Signal               | Layman's translation                                                                                                       | Rule logic                                                        | Bottom-line                                                        |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Strong Buy (+2)**  | Price is meaningfully above HMA and HMA itself has a very strong upward established trajectory.                            | Qualified positive price separation + Strong positive HMA slope   | **A strongly qualified bullish HMA trend state is present.**       |
| **Buy (+1)**         | Price is meaningfully above HMA and HMA has a qualified upward trajectory, but that trajectory is not in the Strong range. | Qualified positive price separation + moderate positive HMA slope | **The HMA trend state is bullish.**                                |
| **Neutral (0)**      | Price position and HMA trajectory do not jointly satisfy a qualified bullish or bearish state.                             | Valid observation that fails the four directional combinations    | **HMA does not currently provide a qualified directional Signal.** |
| **Sell (-1)**        | Price is meaningfully below HMA and HMA has a qualified downward trajectory, but not in the Strong range.                  | Qualified negative price separation + moderate negative HMA slope | **The HMA trend state is bearish.**                                |
| **Strong Sell (-2)** | Price is meaningfully below HMA and HMA itself has a very strong downward established trajectory.                          | Qualified negative price separation + Strong negative HMA slope   | **A strongly qualified bearish HMA trend state is present.**       |

> **Important:** :gray-background[Strong] describes the strength of the qualified HMA trend state under the project's rule thresholds.
> It does **not** mean that continuation is guaranteed, and it does not mean a new turn occurred today.

The two inputs that determine the "*Signal*" are 'ATR Distance' and '14-bar HMA Slope':

```text
ATR Distance
→ How far is price from HMA after accounting for normal volatility?

14-bar HMA Slope
→ How strongly and in what direction has HMA been trending over its recent trajectory?
```

| Field                | Essential meaning                                                          | Analytical purpose                                                                   | Critical interpretation                                                                                                  |
| -------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| **ATR Distance**     | Price's distance from the selected HMA measured in ATR units.              | Makes price/HMA separation comparable across stocks and volatility regimes.          | One of the gates used by the HMA Signal. <li>Positive = price above HMA; <li>Negative = below.                              |
| **14-bar HMA Slope** | The HMA's 14-bar regression slope normalized as % per bar.                 | Measures the direction and strength of HMA's established trajectory.                 |The other major HMA Signal input. <li>Positive supports Buy; <li>Negative supports Sell. <li>Larger magnitude = steeper trend. |

---

### Secondary HMA Context — quick reference

The hover also contains information that does **not** change the primary Signal.

| Field             | What is it?                                                                            | Question it answers                                        | Analytical purpose                                                                   | How to interpret it                                                                                                                                                     |
| ----------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **HMA Direction** | A fresh HMA turning event. <li>Whether the designated HMA **changed direction today**. | **Did this HMA actually change direction today?**          | Flags a fresh turning event rather than an ongoing trend.                            | :gray-background[Turned Up ▲] / :gray-background[Turned Down ▼] appear on the reversal day. <br>:gray-background[None] means there was no new turn today.                                                                   |
| **Trend Context** | The broader/reference trend used to judge the new turn                                 | **What direction is the broader trend moving?**            | Distinguishes a turn occurring with the broader trend from one occurring against it. | :gray-background[Rising], :gray-background[Falling], :gray-background[Flat], or :gray-background[—]. <li> :gray-badge[Rising]/:gray-badge[Falling] provide the directional context used for named 'Turn Context' labels. <li> Does not alter the Signal score. |
| **Turn Context**  | The relationship between HMA Direction and Trend Context                               | **Is today's new turn with or against the broader trend?** | Summarizes whether the fresh turn is trend-aligned or counter-trend.                 | <li>:gray-background[Trend-Aligned] means they agree <li>:gray-background[Counter-Trend] means they oppose one another. <li>This is descriptive, no impact on score.                                    |

For designated turning-context HMAs:

| HMA Direction     | Trend Context                                                                 | Turn Context              | Beginner interpretation                                                                   |
| ----------------- | ----------------------------------------------------------------------------- | ------------------------- | ----------------------------------------------------------------------------------------- |
| **Turned Up ▲**   | ${\textcolor{blue}{\textsf{Rising}}}$                                   | **Bullish Trend-Aligned** | HMA just turned upward and the broader trend already supports the move.                   |
| **Turned Up ▲**   | ${\textcolor{Red}{\textsf{Falling}}}$                                   | **Bullish Counter-Trend** | HMA just turned upward while the broader trend is still falling.                          |
| **Turned Down ▼** | ${\textcolor{Red}{\textsf{Falling}}}$                                   | **Bearish Trend-Aligned** | HMA just turned downward and the broader trend already supports the move.                 |
| **Turned Down ▼** | ${\textcolor{blue}{\textsf{Rising}}}$                                   | **Bearish Counter-Trend** | HMA just turned downward while the broader trend is still rising.                         |
| **None**          | ${\textcolor{blue}{\textsf{Rising}}}$ / ${\textcolor{Red}{\textsf{Falling}}}$ | **—**                     | The broader trend still has a direction, but there was no new HMA turn to classify today. |

The shortest useful translation is:

```text
Signal
= What qualified trend state am I in?

HMA Direction
= Did something change today?

Trend Context
= What is the broader trend doing?

Turn Context
= Does today's change agree with that broader trend?
```

$\large{\rightarrow}$ See "[What the heatmap display is telling you](#what-the-heatmap-display-is-telling-you)" below for more details.

---

### The HMA patterns you should not overlook
See: '*[Reference: Complete Signal + Turning Context](#reference-complete-signal-turning-context)*' for description of all 30 patterns

An HMA cell can combine the primary Signal with a fresh turn and broader-trend context in several ways.

Not every combination deserves the same amount of attention.

More importantly, there are **two different kinds of importance**:

```text
Trend-state strength ('Signal')
→ How strong is the established HMA condition?

Timing significance  ('Turning Context')
→ Did something important just change today?
```

- A ':gray-background[Strong Buy]' with no new turn can therefore contain **more established trend evidence** than a ':gray-badge[Neutral]' cell, while
- a ':gray-background[Neutral]' cell with a fresh aligned upward turn can contain **more new timing information**.


The following are the patterns a user should recognize immediately:

| Pattern                                                                 | Turn Context              |       Trend-state information |          Timing information | Why it matters                                                                                                                                         |
| ----------------------------------------------------------------------- | ------------------------- | ----------------------------: | --------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Strong Buy + Turned Up ▲ + ${\textcolor{blue}{\textsf{Rising}}}$**    | **Bullish Trend-Aligned** |           **Maximum bullish** |   **Maximum fresh bullish** | Strong established bullish state **and** a new upward turn supported by the broader trend. **Do not overlook.**                                        |
| **Strong Sell + Turned Down ▼ + ${\textcolor{Red}{\textsf{Falling}}}$** | **Bearish Trend-Aligned** |           **Maximum bearish** |   **Maximum fresh bearish** | Strong established bearish state plus a new aligned downside turn. **Do not overlook.**                                                                |
| **Buy + Turned Up ▲ + ${\textcolor{blue}{\textsf{Rising}}}$**           | **Bullish Trend-Aligned** |                Strong bullish |   **Maximum fresh bullish** | Qualified bullish state gains a fresh trend-aligned timing event.                                                                                      |
| **Sell + Turned Down ▼ + ${\textcolor{Red}{\textsf{Falling}}}$**        | **Bearish Trend-Aligned** |                Strong bearish |   **Maximum fresh bearish** | Qualified bearish state gains a fresh trend-aligned timing event.                                                                                      |
| **Strong Buy / Strong Sell + no new turn**                              | **—**                     | **Maximum established state** |                         Low | A Strong state remains highly significant even though nothing new happened today. **No arrow does not make the Signal unimportant.**                   |
| **Neutral + Turned Up ▲ + ${\textcolor{blue}{\textsf{Rising}}}$**       | **Bullish Trend-Aligned** |                   Unqualified | **High bullish transition** | The formal Buy rule has not qualified yet, but a fresh upward turn agrees with the broader trend. **Do not dismiss merely because Signal is Neutral.** |
| **Neutral + Turned Down ▼ + ${\textcolor{Red}{\textsf{Falling}}}$**     | **Bearish Trend-Aligned** |                   Unqualified | **High bearish transition** | The formal Sell rule has not qualified yet, but a fresh downward turn agrees with the broader trend.                                                   |
| **Neutral + Turned Up ▲ + ${\textcolor{Red}{\textsf{Falling}}}$**       | **Bullish Counter-Trend** |                   Unqualified |     High, but counter-trend | Potential early bullish reversal attempt against a still-falling broader trend.                                                                        |
| **Neutral + Turned Down ▼ + ${\textcolor{blue}{\textsf{Rising}}}$**     | **Bearish Counter-Trend** |                   Unqualified |     High, but counter-trend | Potential early bearish reversal/pullback against a still-rising broader trend.                                                                        |
| **Neutral + no turn**                                                   | **—**                     |                           Low |                         Low | No qualified directional Signal and no fresh transition event.                                                                                         |


#### How to prioritize the important patterns

The table above identifies HMA combinations that deserve attention, but they are not all important for the same reason.

Some patterns tell you:

> **A directional HMA trend is already firmly established.**

Others tell you:

> **Something important may be changing right now.**

The most useful way to prioritize them is therefore not to force every combination onto one simple strongest-to-weakest scale.

Instead, ask:

```text
How strong is the established HMA state?
+
Did something important just change locally?
+
Does the broader trend support that new change?
```

The ten patterns above fall into five practical tiers:

| Tier       | Pattern group                                     | Technical meaning                                                                                        | Layman's translation                                                                                                                           |
| ---------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tier 1** | Qualified directional Signal + fresh aligned turn | Established trend state and fresh timing event point in the same direction, with broader-trend agreement | **“The trend is already established, and it has just received a fresh same-direction restart or re-acceleration.”**                            |
| **Tier 2** | Strong Buy / Strong Sell + no new turn            | Maximum established HMA state, but no fresh local reversal occurred today                                | **“The trend is already very strong and is simply continuing; nothing newly turned today.”**                                                   |
| **Tier 3** | Neutral + fresh trend-aligned turn                | Formal directional Signal has not qualified yet, but the local turn agrees with the broader trend        | **“The bigger trend already points this way, and the local HMA has just started moving with it—but the formal Signal has not caught up yet.”** |
| **Tier 4** | Neutral + fresh counter-trend turn                | Formal directional Signal has not qualified, and the new local turn opposes the broader trend            | **“Something has started turning locally against the bigger trend. It may be an early reversal—or only a temporary counter-move.”**            |
| **Tier 5** | Neutral + no turn                                 | No qualified directional Signal and no fresh local transition event                                      | **“HMA is not giving you a qualified trend state or a new turning event right now.”**                                                          |

These tiers describe **what kind of information deserves attention**. They are not a backtested ranking of future returns.

---

##### Tier 1 — Qualified trend + fresh aligned re-acceleration
```text
Tier 1
→ "Did the established trend just restart or re-accelerate locally?"
```

This tier contains four of the important patterns:

```text
Strong Buy + Turned Up ▲ + Rising
Strong Sell + Turned Down ▼ + Falling
Buy + Turned Up ▲ + Rising
Sell + Turned Down ▼ + Falling
```

A bullish example is:

```text
Signal: Strong Buy
HMA Direction: Turned Up ▲
Trend Context: Rising
Turn Context: Bullish Trend-Aligned
```

The bearish mirror is:

```text
Signal: Strong Sell
HMA Direction: Turned Down ▼
Trend Context: Falling
Turn Context: Bearish Trend-Aligned
```

The same structure applies to ordinary :gray-background[Buy] and :gray-background[Sell]; those states are qualified directional Signals, but their established trend strength is lower than :gray-background[Strong Buy/Strong Sell].

Technically, Tier 1 means:

> **A directional HMA state is already formally qualified, the local HMA has just changed direction in that same direction, and the broader/reference trend agrees with the new turn.**

The important point is that the fresh turn is **not necessarily the beginning of the overall trend**.

For example:

```text
Strong Buy
+
Turned Up
+
Rising
```

can mean the bullish state was already established, HMA locally paused or moved down, and has now turned upward again while the broader trend remains bullish.

In layman's terms:

> **“The trend was already bullish, it paused or pulled back locally, and the HMA has just started moving upward again while the bigger trend is still rising.”**

The bearish version means:

> **“The trend was already bearish, there was a local pause or bounce, and the HMA has just rolled downward again while the bigger trend is still falling.”**

So Tier 1 asks:

> **“Has an already-qualified trend just received a fresh same-direction restart or re-acceleration?”**

This tier is especially useful when the user is interested in **fresh timing inside an already-established trend**.

For example, someone watching for:

```text
a pullback to finish
a temporary pause to resolve
or
an established trend to resume locally
```

may give Tier 1 particular attention.

Within Tier 1:

```text
Strong Buy / Strong Sell + aligned turn
→ maximum established trend-state strength + maximum fresh aligned timing

Buy / Sell + aligned turn
→ qualified established trend-state strength + maximum fresh aligned timing
```

So all four belong to the same general pattern family, but the :gray-background[Strong] combinations contain greater established-state strength.

---

##### Tier 2 — Strong established trend + no new turn
```text
'Tier 2':
→ "Is the established strong trend simply continuing?"

vs. 'Tier 1':
→ "Did the established trend just restart or re-accelerate locally?"
```


This tier accounts for the combined table pattern:

```text
Strong Buy / Strong Sell + no new turn
```

A bullish example is:

```text
Signal: Strong Buy
HMA Direction: None
Trend Context: Rising
Turn Context: —
```

The bearish mirror is:

```text
Signal: Strong Sell
HMA Direction: None
Trend Context: Falling
Turn Context: —
```

Technically, Tier 2 means:

> **The primary HMA state remains maximally qualified in one direction, but the HMA did not produce a fresh local reversal on this observation.**

In layman's terms:

> **“The trend is already very strong and is simply continuing. Nothing newly turned upward or downward today.”**

So Tier 2 asks:

> **“Is the strongly established trend still intact even though nothing new happened today?”**

This is where Tier 2 differs from Tier 1.

Tier 1 says:

> **“The established trend just received a fresh same-direction local turn.”**

Tier 2 says:

> **“The established trend remains strong, but today is simply another continuation observation.”**

A user may care more about Tier 2 when the objective is not to find a new timing event, but to answer questions such as:

> "Is my existing strong trend condition still intact?"
>
> "Does the HMA still strongly support the direction I am already monitoring?"
>
> "Has anything happened that invalidates the established HMA state?"


For example, someone already monitoring or holding an established trend may not need another Up or Down arrow every day.

For that user:

```text
Strong Buy + no turn
```

still provides highly relevant information:

> **“The strong bullish HMA condition remains in force.”**

By contrast, a user specifically looking for **something newly actionable or newly changed today** would generally find Tier 1 more informative because Tier 1 contains the fresh event.

So the practical distinction is:

```text
Tier 1
→ "Did the established trend just restart or re-accelerate locally?"

Tier 2
→ "Is the established strong trend simply continuing?"
```

Neither interpretation makes Tier 2 a failed Tier 1.
- Tier 2 has less **new timing information**, not less validity as an established trend state.

---
##### Tier 3 — Neutral + fresh turn agrees with broader trend
```
Tier 3
→ “Is the existing broader trend getting fresh local confirmation?”
→ Tier 3 is early relative to formal Signal qualification
```

**Tier 3**
- broader trend already exists
- local HMA just joins/confirms it
- formal Buy/Sell has not yet qualified
- question: **“Is the existing broader trend getting fresh local support before the formal Signal catches up?”**
- **Tier 3 = fresh local 'support' for the existing broader trend, before formal Signal qualification.**

**Tier 4**
- broader trend already exists
- local HMA just moves against it
- formal Buy/Sell still has not qualified
- question: **“Could this local move be an early sign that the broader trend is starting to change?”**
- **Tier 4 = fresh local 'opposition' to the existing broader trend, potentially an early reversal signal, but not yet broader-trend confirmation.**


---

This tier contains:

```text
Neutral + Turned Up ▲ + Rising
Neutral + Turned Down ▼ + Falling
```

Take:

```text
Signal: Neutral
HMA Direction: Turned Up ▲
Trend Context: Rising
Turn Context: Bullish Trend-Aligned
```

In layman's terms:
> **"The stock does not yet meet all of the project's requirements to call the HMA condition bullish, but**
> - **the '*local*' HMA just changed direction upward, and**
> - **the '*broader trend*' is already moving upward too."**

Or even shorter:

> **“The bigger trend is already up, and the local HMA has just started moving up with it—but the formal 'Buy' test hasn't caught up yet.”**

Why can Signal still be Neutral?
- Because the fresh turn itself does not guarantee that both primary Signal inputs have qualified.

For example:

```text
ATR Distance
→ may still be too small

or

14-bar HMA Slope
→ may still be too weak
```

So the local HMA can already have:

```text
Turned Up ▲
```

while the complete Buy rule remains:

```text
not yet qualified
```

The important sequence is:

```text
broader trend
→ already Rising

local HMA
→ just Turned Up

formal Signal
→ still Neutral
```

So Tier 3 is basically:

```text
directional evidence is developing
+
the broader trend already supports it
+
formal Signal qualification is still pending
```

The bearish mirror works the same way:

```text
Signal: Neutral
HMA Direction: Turned Down ▼
Trend Context: Falling
Turn Context: Bearish Trend-Aligned
```

In layman's terms:

> **“The bigger trend is already down, and the local HMA has just started moving down with it—but the formal Sell test hasn't caught up yet.”**

The important point is what is “early” about this pattern.

Tier 3 is **early relative to formal Buy/Sell qualification**.

The broader trend is not waiting to reverse; it already points in the same direction as the new local turn.

What has happened is:

```text
broader trend
→ already supportive

fresh local turn
→ now joins that direction

formal Buy / Sell Signal
→ has not qualified yet
```

So Tier 3 asks:

> **“Is the existing broader trend getting fresh local support ${\underline{\textsf{before the formal 'Signal' qualifies}}}$?”**

This pattern is especially relevant when the user wants to identify a developing move **in the direction of an already-established broader trend**, $\large{\underline{\textsf{without}}}$ waiting for the full 'Buy/Sell' rule to qualify.

In practical terms:

> **“The bigger trend is already on my side, and the local HMA has just joined it.**
> - **The formal Signal is still Neutral, but the pieces are beginning to line up.”**


---
##### Tier 4 — Neutral + fresh turn against broader trend

**Key Points:**
→ "*Could the existing broader trend be starting to change?*"
→ Tier 4 is early relative to a possible reversal of the existing broader trend
- broader trend already exists
- local HMA just moves against it
- formal Buy/Sell still has not qualified
- question: **“Could this local move be an early sign that the broader trend is starting to change?”**
- **Tier 4 = fresh local 'opposition' to the existing broader trend, potentially an early reversal signal, but not yet broader-trend confirmation.**


---

This tier contains:

```text
Neutral + Turned Up ▲ + Falling
Neutral + Turned Down ▼ + Rising
```

Take:

```text
Signal: Neutral
HMA Direction: Turned Up ▲
Trend Context: Falling
Turn Context: Bullish Counter-Trend
```

In layman's terms:

> **The stock has not qualified as bullish, but the local HMA has just turned upward even though the broader trend is still falling.**

Or even shorter:

> **“Something may be trying to reverse upward, but the bigger trend hasn't turned with it.”**

Why is this different from Tier 3?

Because the fresh local turn and the broader trend now point in **opposite directions**:

```text
broader trend
→ still Falling

local HMA
→ just Turned Up

formal Signal
→ still Neutral
```

So the local HMA has changed first, while the broader trend has not.

That creates two plausible interpretations:

```text
possible early reversal
```

or:

```text
temporary bounce inside the existing downtrend
```

At this stage, the HMA fields do not tell you which outcome will follow.

The bearish mirror works the same way:

```text
Signal: Neutral
HMA Direction: Turned Down ▼
Trend Context: Rising
Turn Context: Bearish Counter-Trend
```

In layman's terms:

> **“The local HMA has just rolled over, but the bigger trend is still rising.”**

That could become:

```text
the beginning of a bearish reversal
```

or merely:

```text
a temporary pullback inside the existing uptrend
```

So Tier 4 is basically:

```text
a fresh local change has occurred
+
that change opposes the existing broader trend
+
formal directional qualification is still absent
```

The important point is what is “early” about this pattern.

Tier 4 is **early relative to a possible future change in the broader trend**.

The broader trend has not changed yet.

Only the local HMA has moved the other way.

So Tier 4 asks:

> **“Could this fresh local move be the first sign that the existing broader trend is starting to change?”**

This pattern is especially relevant when the user wants to identify **possible reversals, inflection points, or deterioration in the existing broader trend** before that broader trend itself has turned.

In practical terms:

> **“The local HMA is moving against the bigger trend. That may be the beginning of a real reversal—but it may also fail and remain only a temporary counter-move.”**


That does not make Tier 4 stronger than Tier 3.
- It means the two patterns answer different questions:
```text
Tier 3
→ existing broader trend + fresh local move in the same direction
→ early relative to formal Signal qualification

Tier 4
→ existing broader trend + fresh local move in the opposite direction
→ early relative to a possible broader-trend reversal
````

---

##### Tier 5 — Neutral + no turn

This tier contains:

```text
Neutral + no turn
```

A representative configuration is:

```text
Signal: Neutral
HMA Direction: None
Turn Context: —
```

Trend Context may still be:

```text
Rising
```

or:

```text
Falling
```

on a designated HMA row, but there is no fresh HMA turn to classify.

Technically, Tier 5 means:

> **The primary HMA inputs do not jointly qualify for Buy, Sell, Strong Buy, or Strong Sell, and no new local HMA reversal occurred today.**

In layman's terms:

> **“The HMA does not currently have enough agreement to give you a qualified bullish or bearish Signal, and nothing newly changed direction today either.”**

So Tier 5 asks:

> **“Is HMA currently providing little new directional information?”**

This does **not** mean:

```text
nothing is happening in the stock
```

and it does not mean:

```text
the broader trend has no direction
```

It means only that the HMA framework itself currently provides neither:

```text
a qualified directional Signal
nor
a fresh local turning event
```

For a user scanning the heatmap for either strong established states or meaningful new transitions, Tier 5 will generally deserve the least immediate attention of the ten patterns listed above.

---

The tier framework can therefore be remembered as:

```text
Tier 1
Qualified trend + fresh aligned re-acceleration
→ “Has the established trend just restarted locally?”

Tier 2
Strong established trend + no fresh turn
→ “Is the strong trend simply continuing?”

Tier 3
Early trend-aligned development
→ “Is the existing broader trend getting fresh local confirmation before the formal Signal qualifies?”

Tier 4
Early counter-trend reversal attempt
→ “Could the existing broader trend be starting to change?”

Tier 5
Neutral + no fresh event
→ “Is HMA currently providing little new directional information?”
```

These tiers should not be interpreted as five increasingly weak versions of the same phenomenon.

They represent different situations:

```text
trend already established + something new happened
trend already established + nothing new happened
trend not yet qualified + new evidence agrees with broader trend
trend not yet qualified + new evidence opposes broader trend
neither qualified state nor new event
```

The complete combination reference—including less-common Signal/turn disagreements and actual ticker/date examples—is provided later under **Reading Signal and Turning Context Together**.


---

### What the heatmap display is telling you
$\small{\textsf{See: 'How to Read an HMA Heatmap Cell' below}}$

The cell uses several visual channels at once.

| What you see              | What it represents        | Question it answers                                   |
| ------------------------- | ------------------------- | ----------------------------------------------------- |
| **Displayed HMA number**  | Current HMA value         | **Where is the HMA itself?**                          |
| **Cell background color** | Primary five-state Signal | **What qualified HMA trend state is present?**        |
| **▲ / ▼**                 | Fresh HMA Direction event | **Did HMA turn today, and which way?**                |
| **${\textcolor{blue}{\textsf{blue}}}$ / ${\textcolor{red}{\textsf{red}}}$ turn text**  | Trend Context             | **Is the broader/reference trend Rising or Falling?** |

For a turning-context row:

${\textcolor{blue}{\textsf{▲ trend↑}}}$
→ Turned Up + Rising = Bullish Trend-Aligned

${\textcolor{Red}{\textsf{▲ trend ↓}}}$
→ Turned Up + Falling = Bullish Counter-Trend

${\textcolor{Red}{\textsf{▼ trend ↓}}}$
→ Turned Down + Falling = Bearish Trend-Aligned

${\textcolor{blue}{\textsf{▼ trend↑}}}$
→ Turned Down + Rising = Bearish Counter-Trend

The background and the arrow/text can legitimately tell different stories because they describe different dimensions.

For example:

```text
640.30 ▲
gray background
red text
```

means:

```text
Signal: Neutral
HMA Direction: Turned Up
Trend Context: Falling
Turn Context: Bullish Counter-Trend
```

In plain English:

> **The formal HMA scoring conditions are not bullish enough to produce 'Buy', but HMA has just turned upward while its broader trend is still falling.**
> - **This is early counter-trend bullish information, not an established bullish Signal.**

Likewise:

```text
Strong Buy background
no arrow
```

does **not** mean the bullish condition is weak or fading.

It means:

> "***The bullish trend state is strongly established, but today is not the day on which HMA changed direction.***"


---

## HMA — Brief Overview

### What HMA measures

The Hull Moving Average (HMA) is a moving average designed to reduce the lag normally associated with smoothing price while suppressing some of the noise present in raw price movement.

Like SMA and EMA, HMA produces a smoothed price series.

What makes HMA different is the way that smoothed series is constructed.

Conceptually:

```text
HMA(n)
=
WMA(
    2 × WMA(price, n/2)
    - WMA(price, n),
    sqrt(n)
)
```

The project uses its canonical price series:
```
Adjusted Close when available
otherwise Close
```


The calculation can be thought of in three stages:

```text
1. Calculate a faster weighted average using roughly half the HMA period.
	- Compare it with the full-period weighted average.
2. Give that faster average extra weight relative to the full-period average.
3. Smooth the resulting series again using a much shorter WMA.
```

The purpose is not to predict price.
- It is to create a moving average that can react more quickly to changes in price direction than a comparably long conventional moving average, while remaining smoother than raw price.

A useful beginner translation is:
> **HMA tries to preserve the smoothness of a moving average while reducing some of the delay that normally comes with smoothing.**

That responsiveness is particularly useful when the question is not only:
> **What direction is the trend moving?**

but also:
> **Has that direction just begun to change?**

That second question is why the app supplements the normal HMA Signal with the separate :gray-background[HMA Direction], :gray-background[Trend Context], and :gray-background[Turn Context] fields.


---
### The 6 HMA Variants
$\small{\textsf{See Appendix: "How the other HMA variants differ"}}$

The app currently defines six HMA variants:

| Variant      | Window          | Relative role                                                     | ATR-distance (Buy/Sell price  gate) | Base slope threshold | 'Strong' slope threshold |
| ------------ | --------------- | ----------------------------------------------------------------- | ----------------------------------: | -------------------: | -----------------------: |
| **HMA(9)**   | ST              | Fastest HMA; reacts most quickly to recent price movement         |                       ±0.25 ATR(14) |           ±0.20%/bar |               ±0.50%/bar |
| **HMA(16)**  | MT              | Responsive intermediate HMA; also receives formal Turning Context |                       ±0.50 ATR(14) |           ±0.20%/bar |               ±0.50%/bar |
| **HMA(21)**  | MT              | Balanced medium-term HMA; also receives formal Turning Context    |                       ±0.50 ATR(14) |           ±0.20%/bar |               ±0.50%/bar |
| **HMA(50)**  | LT              | Slower long-term directional reference                            |                       ±0.50 ATR(14) |           ±0.20%/bar |               ±0.50%/bar |
| **HMA(55)**  | LT              | Long-term HMA; also receives formal Turning Context               |                       ±0.50 ATR(14) |           ±0.20%/bar |               ±0.50%/bar |
| **HMA(200)** | LT / structural | Very-long-term structural HMA                                     |                       ±2.00 ATR(14) |           ±0.25%/bar |               ±0.50%/bar |

All six use the same basic Signal architecture:

```text
ATR-normalized price separation
+
that HMA's own normalized 14-bar regression slope
```


The thresholds differ in two important places:

First, **HMA(9)** uses a smaller price-distance requirement, meaning, it needs less price separation before a directional state can qualify:

```text
±0.25 ATR(14)
```

because it is the fastest HMA in the family.


Second, **HMA(200)** requires substantially more evidence for price separation:

```text
±2.00 ATR(14)
```

 and for the ordinary Buy/Sell slope threshold:

```text
±0.25%/bar
```

Its Strong threshold remains:

```text
±0.50%/bar
```

The production rulebook therefore treats HMA(200) differently from merely applying the medium-term rules to a much longer moving average.


> **SUMMARY:**
> - * **HMA(9)** needs less price separation before a directional state can qualify.
> - * **HMA(200)** requires much larger price separation and a slightly stronger ordinary slope before Buy/Sell can qualify.
> - * * **HMA(16/21/50/55)** share the same Signal thresholds.


> **Important:** The HMA period changes the speed and threshold calibration of the measurement. It does not change what :gray-background[Buy], :gray-background[Sell], :gray-background[Strong Buy], or :gray-background[Strong Sell] fundamentally mean.


---
## Understanding the HMA "Signal"

The "Signal" is based on 2 inputs:
1. ATR Distance
2. 14-day HMA Slope

The Signal combines two different questions, each of which the which the 2 inputs - ATR Distance and 14d HMA Slope - answer:

| Input                | Question                                                                                      |What it prevents                                                                                                 |
| -------------------- | --------------------------------------------------------------------------------------------- |---------------------------------------------------------------------------------------------------------------- |
| **ATR Distance**     | **Is price far enough from HMA to matter relative to how much this security normally moves?** |Treating tiny price/HMA separations as meaningful merely because price is technically above or below HMA         |
| **14-bar HMA Slope** | **Is HMA itself moving in that same direction strongly enough over its recent trajectory?**   |Treating price position as directional when HMA's own established trajectory is too weak or points the other way |


The relationship is:

```text
ATR Distance
+
14-bar HMA Slope
→
HMA Signal
```

- A bullish state requires both inputs to support the bullish interpretation.
- A bearish state requires both inputs to support the bearish interpretation.

This produces four qualified directional states:

```text
Strong Buy
Buy
Sell
Strong Sell
```

Everything else that is a valid HMA observation falls back to:

```text
Neutral
```

':gray-background[Neutral]' can arise for several different reasons.

For example:

```text
Price separation is too small
```

or:

```text
HMA slope is too weak
```

or:

```text
price and slope point in opposite directions
```

can all leave the Signal Neutral.

So, **':gray-background[Neutral]' does not necessarily mean price is sitting directly on HMA or that HMA is flat.**

It means:

> **The required price-distance and trajectory/trend conditions do not jointly qualify for Buy, Sell, Strong Buy, or Strong Sell.**


---

$\Large{\textsf{The Two Numbers That Drive the 'Signal'}}$:

### 1. ATR Distance
$\small{\textsf{NOTE: see 'MU Example' below for real example.}}$

`ATR Distance` measures:

> **How far price is above or below the selected HMA in units of ATR(14).**

The calculation is:

```text
ATR Distance
=
Close - HMA
-----------
 ATR(14)
```

A positive result means:

```text
Price is above HMA
```

A negative result means:

```text
Price is below HMA
```

The **magnitude** tells you how large that separation is relative to current volatility.

---
$\large{\textsf{Worked example: ATR Distance}}$

Suppose:
```text
Close   = $105
HMA(21) = $103
ATR(14) = $4
```

First calculate the price difference:

```text
$105 - $103 = +$2
```

Then express that difference in ATR units:

```text
+$2 / $4 = +0.50 ATR
```

So:

```text
ATR Distance: +0.50 ATR
```

means:

> **Price is one-half of one current ATR above HMA(21).**

Now consider:

```text
Close   = $96
HMA(21) = $100
ATR(14) = $5
```

Then:

```text
($96 - $100) / $5
= -$4 / $5
= -0.80 ATR
```

So:

```text
ATR Distance: -0.80 ATR
```

means:

> **Price is 0.80 ATR below HMA(21).**


---
### 2. 14-bar HMA Slope
$\small{\textsf{NOTE: see 'MU Example' below for real example.}}$

The second Signal input measures the HMA's established trajectory.

The app first calculates a linear-regression slope across the most recent 14 HMA observations.

That raw slope is then normalized by the current HMA level:
- $\small{\text{For more info, see Appendix: 'Why normalize the slope?'}}$

```text
Normalized 14-bar HMA Slope

     14-bar regression slope
=   -----------------------  × 100
          current HMA

```

The displayed unit is:

```text
% per bar
```

This answers:

> ***Over its recent 14-bar trajectory, how steeply has this HMA been rising or falling relative to its own level?***

----
$\large{\textsf{Worked example: 14-day HMA Slope}}$

Suppose:

```text
Current HMA = $200
14-bar regression slope = +$0.60 per bar
```

Normalize it:

```text
(0.60 / 200) × 100 = +0.30%/bar
```

So the hover would show approximately:

```text
14-bar HMA Slope: +0.30%/bar
```

That means:
> **The "best-fit" trajectory through the recent 14 HMA observations is rising at roughly 0.30% of the HMA's current value per bar/day.**

For HMA(21), that slope is:

```text
above +0.20%/bar
```

but:

```text
not above +0.50%/bar
```

So, assuming the ATR Distance requirement also qualifies, the slope supports :gray-background[Buy] rather than :gray-background[Strong Buy].


### 'MU' Example: 'ATR Distance' and 'Slope'

The easiest way to see their value is to start with what the displayed HMA number **doesn't** tell you.

From your production test, MU on 8/28/26 showed:

```text
HMA(200): 1087.76
Signal: Neutral
```

That tells you where the HMA line is, but by itself :gray[1087.76] tells you almost nothing about **why** the signal is Neutral.
To explain the score, we need two additional questions:
1. **How far is price from HMA(200), relative to MU's normal volatility?**
2. **How strongly is HMA(200) itself rising or falling?**

Those are exactly the two quantities used by the new rules.

---
#### (MU) ATR Distance

The calculation is:

```text
ATR Distance = (Close - HMA) / ATR(14)
```

Suppose, purely as an arithmetic example around your **actual MU HMA(200) value of 1087.76**, that the same observation had:

```text
Close     = 1,130.00
HMA(200)  = 1,087.76
ATR(14)   = 25.00
```

First calculate the raw price gap:

```text
1,130.00 - 1,087.76 = +42.24
```

Then scale it by MU's current volatility:

```text
42.24 / 25.00 = +1.69 ATR
```

So the hover would say approximately:

```text
Price vs. HMA: +$42.24 (+3.88%)
ATR Distance: +1.69 ATR
```

$\Large{\textsf{What does `+1.69 ATR` actually mean?}}$

It means:
> Price is above HMA(200) by an amount equal to about **1.69 times MU's recent average daily trading range**.

That is much more informative than simply saying price is :gray[$42.24] above the HMA.

Why?

Because :gray[$42] means very different things for:

* a quiet stock whose ATR is :gray[$5];
* versus a volatile stock whose ATR is :gray[$30].

With ATR normalization:

```text
+$42 with ATR=$5
→ +8.4 ATR
→ enormous separation

+$42 with ATR=$30
→ +1.4 ATR
→ much less exceptional
```

That is exactly why we used ATR normalization (see Appendix) for HMA scoring.

$\Large{\textsf{How does it affect HMA(200)?}}$

Your approved HMA(200) bullish gate is:

```text
ATR Distance > +2.00

"buy":
(Close - HMA_200) / ATR_14 > 2.00
and (HMA_200_slope__linreg_14 / HMA_200) * 100 > 0.25
and (HMA_200_slope__linreg_14 / HMA_200) * 100 <= 0.50"
```

Therefore our illustrative:

```text
+1.69 ATR
```

would **not qualify as Buy**, even though price is above HMA by almost 4%.

In plain English:

> "***Price is above the long-term trend line, but not far enough above it relative to this stock's volatility to call the separation structurally meaningful.***"

That is very useful hover information.

#### (MU) '14-bar HMA Slope'

This is not today's HMA minus yesterday's HMA.

We're taking a **linear-regression slope over the last 14 HMA observations**, then normalizing that slope by the HMA level:

```text
SlopePctPerBar:

       HMA slope over 14 bars
=    ------------------------- × 100
           current HMA
```

Suppose HMA(200) is:
```text
1,087.76
```

and the 14-bar regression line through HMA(200) is rising by:
```text
+$4.35 per trading bar
```

Then:
```text
4.35 / 1,087.76 × 100 ≈ +0.40% per bar
```

The hover would say:

```text
14-bar HMA Slope: +0.40%/bar
```

What does that mean?

It means:
> ***Across the recent 14-bar window, the HMA's fitted trend has been rising at a rate equivalent to roughly 0.40% of the current HMA value per trading bar.***

It gives you ${\fcolorbox{none}{lightyellow}{\textsf{direction + steepness}}}$.

Compare:
```text
+0.03%/bar
→ HMA is technically rising, but barely.
```

versus:
```text
+0.27%/bar
→ A meaningful rising HMA.
```

versus:
```text
+0.62%/bar
→ A strongly rising HMA.
```

And our rules encode exactly that distinction.

For HMA(200):

```text
> +0.25%/bar through +0.50%
→ 'Buy'-quality slope

> +0.50%/bar
→ 'Strong Buy'-quality slope
```

#### (MU) Put both together

Take this example:

```text
HMA(200):               $1,087.76
Close:                  $1,145.00
ATR(14):                $25.00
14-bar raw HMA slope:   +$6.20/bar
```

$\large{\textsf{Price-distance calculation:}}$
```text
(Close - HMA(200)):
$1,145.00 - $1,087.76
= $57.24

((Price-MA gap)/ATR(14)):
$57.24 / $25.00
= +2.29 ATR
```

So Price passes HMA(200)'s bullish price gate:
```text
ATR Distance:           +2.29 ATR
bullish price gate:   > +2.00 ATR
```


$\large{\textsf{Slope calculation:}}$

Normalize 'raw slope' by the 'current HMA' level:
```text
($6.20 / $1,087.76) × 100 ≈ +0.57%/bar
```

So:
```text
14-bar HMA Slope: +0.57%/bar
```

That exceeds the Strong threshold:
```text
> +0.50%/bar
```

Therefore:
```text
Price distance   +2.29 ATR   → passes Strong Buy price prerequisite
HMA slope        +0.57%/bar  → passes Strong Buy slope prerequisite

Signal: Strong Buy
```

Now a human looking at the hover can reconstruct the classification.

Without those two fields, they would just see:

```text
HMA(200): $1,087.76
Signal: Strong Buy
```

and have no idea **why**.

That's the main information value.

---
### HMA(21): Complete 'Signal' Rule Map

A compact way to reconstruct the entire HMA(21) Signal is:

| Signal          |    ATR Distance |               14-bar HMA Slope | Beginner translation                                                   |
| --------------- | --------------: | -----------------------------: | ---------------------------------------------------------------------- |
| **Strong Buy**  |   `> +0.50 ATR` |                 `> +0.50%/bar` | Price is meaningfully above HMA and HMA is rising very strongly        |
| **Buy**         |   `> +0.50 ATR` | `> +0.20%` and `<= +0.50%/bar` | Price is meaningfully above HMA and HMA is rising at a qualified rate  |
| **Neutral**     | Any valid value |                Any valid value | The two inputs do not combine into one of the four directional rules   |
| **Sell**        |   `< -0.50 ATR` | `< -0.20%` and `>= -0.50%/bar` | Price is meaningfully below HMA and HMA is falling at a qualified rate |
| **Strong Sell** |   `< -0.50 ATR` |                 `< -0.50%/bar` | Price is meaningfully below HMA and HMA is falling very strongly       |

The key idea is:

```text
ATR Distance
→ confirms that price position is material

14-bar HMA Slope
→ determines direction and trend-strength tier
```

So the five-state classification is not simply:

```text
How far is price above or below HMA?
```

and it is not simply:

```text
Is HMA rising or falling?
```

It requires both.

$\large{\rightarrow}$ $\small{\textsf{Appendix: "Understanding the 'ATR' and 'Slope' Threshold Boundaries"}}$

---
### Checklist: Questions to understand 'Signal'

When trying to reconstruct an HMA Signal from the hover, ask:

| Step  | Question                                                                                       |
| ----- | ---------------------------------------------------------------------------------------------- |
| **1** | Is the 14-bar HMA Slope positive or negative?                                                  |
| **2** | Is its magnitude large enough to pass the ordinary slope threshold?                            |
| **3** | If it passes, is it in the ordinary or Strong slope range?                                     |
| **4** | Is ATR Distance on the same side of HMA as that slope?                                         |
| **5** | Is ATR Distance large enough to clear the period-specific price gate?                          |
| **6** | If any required piece fails or disagrees, does the observation therefore fall back to Neutral? |

The shortest way to remember the architecture is:

```text
ATR Distance says:
"Has price moved far enough in that same direction to confirm it?"

Slope says:
"What is HMA's established direction and strength?"

Together:
"What Signal should the app assign?"
```

---
---

## Understanding "Turning Context"

The primary HMA Signal answers:

> **What qualified HMA trend state is present right now?**

Turning Context answers a different question:

> **Did HMA just change direction, and if so, did that change occur with or against the broader trend?**

These two layers are deliberately separate.

```text
Signal
→ current trend state

Turning Context
→ fresh directional change + broader-trend relationship
```

That distinction matters because a strong established trend does not need a fresh turn to remain important, and a fresh turn can occur before the primary Signal has qualified as Buy or Sell.

For example:

```text
Signal: Strong Buy
HMA Direction: None
Trend Context: Rising
Turn Context: —
```

means:

> **The bullish HMA state is strongly established, but today is not a new reversal day.**

By contrast:

```text
Signal: Neutral
HMA Direction: Turned Up ▲
Trend Context: Rising
Turn Context: Bullish Trend-Aligned
```

means:

> **The primary HMA rule has not yet qualified as Buy, but HMA has just turned upward in agreement with its broader trend context.**

Neither result is contradictory.

They are describing different dimensions of the same observation.

The current production rulebook explicitly states that HMA Direction and context fields are supplementary and do not change the Signal score.

---

### The 3 Turning Context fields

The Turning Context layer consists of:

| Field             | Question it answers                                                         |
| ----------------- | --------------------------------------------------------------------------- |
| **HMA Direction** | **Did this HMA actually change direction today?**                           |
| **Trend Context** | **What direction is the broader/reference trend moving?**                   |
| **Turn Context**  | **Does today's new HMA direction agree with or oppose that broader trend?** |

The relationship is:

```text
HMA Direction
+
Trend Context
→
Turn Context
```

So:

```text
Turned Up
+
Rising
→
Bullish Trend-Aligned
```

while:

```text
Turned Up
+
Falling
→
Bullish Counter-Trend
```

The same logic applies in reverse for downward turns. Production computes exactly these four Rising/Falling combinations.

---
Turn Context is determined from two independent pieces of information:

```text
HMA Direction
+
Trend Context
```

The first identifies the **new event**.

The second identifies the **reference direction against which that event should be interpreted**.


---

### 1. HMA Direction

`HMA Direction` answers:

> **Did the selected HMA reverse its immediate direction today?**
> - `HMA Direction` tells you **whether something changed today**, not whether HMA currently has an upward or downward trajectory.


It is an **event field**, not a persistent state.

Possible values are:

```text
Turned Up ▲
Turned Down ▼
None
—
```

- :gray-background[Turned Up] and :gray-background[Turned Down] appear only on the observation where the reversal occurs.
	- :gray-background[Turned Up] is a **local reversal event**. It means the HMA had been flat/falling immediately beforehand and has now switched back upward.
	- :gray-background[Turned Down] is a **local reversal event**. It means the HMA had been flat/rising immediately beforehand and has now turned downward.
- :gray-background[None] means sufficient data exists, but no new reversal occurred today.
- `—` means the required turn inputs are unavailable.

---

#### How an upward turn is detected

The production logic requires three HMA observations:

```text
today
yesterday
two bars ago
```

An upward turn occurs when:

```text
HMA[t] > HMA[t-1]
and
HMA[t-1] <= HMA[t-2]
```

In plain English:

> **HMA is rising today, and yesterday's HMA had still been flat or falling relative to the preceding observation.**

That combination marks the point where immediate direction changes upward. The production implementation uses exactly this comparison.

Example:

```text
Two bars ago:  209.90
Yesterday:     209.60
Today:         209.85
```

First:

```text
209.85 > 209.60
```

so HMA rose today.

Second:

```text
209.60 <= 209.90
```

so yesterday had not already been rising.

Therefore:

```text
HMA Direction: Turned Up ▲
```

**Bottom-line:** Answers the question **“Did HMA switch from falling/flat to rising today?”**

---

#### How a downward turn is detected

A downward turn is the mirror image:

```text
HMA[t] < HMA[t-1]
and
HMA[t-1] >= HMA[t-2]
```

In plain English:

> **HMA is falling today, and yesterday's HMA had still been flat or rising relative to the preceding observation.**

Example:

```text
Two bars ago:  210.10
Yesterday:     210.30
Today:         210.05
```

Then:

```text
210.05 < 210.30
```

and:

```text
210.30 >= 210.10
```

so:

```text
HMA Direction: Turned Down ▼
```

**Bottom-line:** Answers the question **“Did HMA switch from rising/flat to falling today?”**

---
### 2. Trend Context
$\small{\textsf{See 'Appendix' for more on HMA(16,21,55)}}$

Once the app determines whether a fresh HMA turn occurred, it asks:

> **What broader/reference trend should the recent action (the 'turn') be compared against?**

That answer is `Trend Context`.

Possible production values include:

```text
Rising
Falling
Flat
—
```

The reference is deliberately not identical for every turning HMA.

| Timing HMA  | Trend Context reference             | Question being answered                                                    |
| ----------- | ----------------------------------- | -------------------------------------------------------------------------- |
| **HMA(16)** | HMA16's own normalized 14-bar slope | **Did the fresh HMA16 turn agree with its established 14-bar trajectory?** |
| **HMA(21)** | HMA(55) one-day direction           | **Did HMA21 turn with or against the slower HMA55 direction?**             |
| **HMA(55)** | HMA(200) one-day direction          | **Did HMA55 turn with or against the structural HMA200 direction?**        |

For HMA16, Trend Context answers:
- **“Is today's new local turn moving with or against HMA16's own established 14-bar trajectory?”**

For HMA21, Trend Context answers:
- **“Is the medium-term HMA21 turn moving with or against the slower HMA55?”**

For HMA55, Trend Context answers:
- **“Is the longer-term HMA55 turn moving with or against the structural HMA200 direction?”**


---
### 3. From the 2 inputs to 'Turn Context'
Once both fields are known:

```text
HMA Direction
+
Trend Context
```

the resulting interpretation is straightforward.

| HMA Direction     | Trend Context | Turn Context              | Beginner translation                        |
| ----------------- | ------------- | ------------------------- | ------------------------------------------- |
| **Turned Up ▲**   | Rising        | **Bullish Trend-Aligned** | New Up turn agrees with the broader trend   |
| **Turned Up ▲**   | Falling       | **Bullish Counter-Trend** | New Up turn opposes the broader trend       |
| **Turned Down ▼** | Falling       | **Bearish Trend-Aligned** | New Down turn agrees with the broader trend |
| **Turned Down ▼** | Rising        | **Bearish Counter-Trend** | New Down turn opposes the broader trend     |

These four labels are assigned directly in the production context logic.

A useful shortcut is:

```text
same direction
→ Trend-Aligned

opposite direction
→ Counter-Trend
```

Then determine bullish versus bearish from the new HMA turn:

```text
Up turn
→ Bullish

Down turn
→ Bearish
```

So:

```text
Up + Rising
→ Bullish Trend-Aligned

Up + Falling
→ Bullish Counter-Trend

Down + Falling
→ Bearish Trend-Aligned

Down + Rising
→ Bearish Counter-Trend
```

---
## Reading "Signal" and "Turning Context" Together

This is where the two HMA layers become most useful.

The primary Signal tells you:

> **How strongly does the current HMA configuration qualify as bullish, bearish, or Neutral?**

Turning Context tells you:

> **Did something change today, and does the broader trend support that change?**

The most useful conceptual split is:

```text
Signal
→ established state information

HMA Direction + Trend Context + Turn Context
→ transition / timing information
```

Neither dimension should automatically override the other.

---
### Two different kinds of importance
Related: $\small{\textsf{"The HMA patterns you should not overlook"}}$ under $\small{\textsf{"Summary: How to Interpret HMA"}}$

A common mistake would be to place every HMA combination on one simple strongest-to-weakest scale.

That loses information.

Consider:

```text
Strong Buy + HMA Direction: None
```

versus:

```text
Neutral + Turned Up ▲ + Rising
```

The first has much stronger **established-state information**.

The second has much stronger **fresh timing information**.

| BULLISH Patterns              |  Trend-state strength |      Timing significance |
| ----------------------------- | --------------------: | -----------------------: |
| **Strong Buy + aligned ▲**    | **Maximum (bullish)** |              **Maximum** |
| **Buy + aligned ▲**           |      Strong (bullish) |              **Maximum** |
| **Strong Buy + no turn**      | **Maximum (bullish)** |                      Low |
| **Buy + no turn**             |      Strong (bullish) |                      Low |
| **Neutral + aligned ▲**       |           Unqualified |                 **High** |
| **Neutral + counter-trend ▲** |           Unqualified | **High / early-warning** |
| **Neutral + no turn**         |                   Low |                      Low |

| BEARISH Patterns              | Trend-state strength |      Timing significance |
| ----------------------------- | -------------------: | -----------------------: |
| **Strong Sell + aligned ▼**   |  **Maximum bearish** |              **Maximum** |
| **Sell + aligned ▼**          |       Strong bearish |              **Maximum** |
| **Strong Sell + no turn**     |  **Maximum bearish** |                      Low |
| **Sell + no turn**            |       Strong bearish |                      Low |
| **Neutral + aligned ▼**       |          Unqualified |                 **High** |
| **Neutral + counter-trend ▼** |          Unqualified | **High / early-warning** |
| **Neutral + no turn**         |                  Low |                      Low |
- '**aligned ▼**' means  '`Turned Down ▼ + Falling`'
- '**counter-trend ▼**' means  '`Turned Down ▼ + Rising`'

> **NOTE**:
> **The bearish side mirrors the same structure.**
> - The purpose of this table is not to rank historical forward returns; it is to separate **established trend-state strength** from **fresh timing significance**.
> - See Also: '***Complete Signal + Turning Context reference***' above


So the better question is not merely:

> **Which pattern is stronger?**

It is:

> **What kind of information is this pattern giving me?**

That distinction is central to reading HMA correctly.

---
### Established state + fresh aligned turn

The clearest directional configuration occurs when:

```text
Signal direction
=
fresh turn direction ('HMA Direction')
=
broader trend direction ('Trnd Context')
```

For example:

```text
Signal: Strong Buy
HMA Direction: Turned Up ▲
Trend Context: Rising
Turn Context: Bullish Trend-Aligned
```

This combines:

```text
strong established bullish state
+
fresh upward timing event
+
broader-trend agreement
```

The bearish mirror is:

```text
Strong Sell
+
Turned Down ▼
+
Falling
```

These patterns contain both:

```text
strong state information
and
strong fresh timing information
```

That is why they belong among the most important combinations in the opening quick-reference table.

### Established 'State' + No new 'Turn'

A directional Signal does not require a fresh arrow.

For example:

```text
Signal: Strong Buy
HMA Direction: None
Trend Context: Rising
Turn Context: —
```

means:

> **The bullish trend state is strongly established, but today's observation is continuation rather than a new reversal event.**

The absence of an arrow should not be interpreted as:

```text
weakening
```

or:

```text
loss of conviction
```

It says only:

> **No new turn occurred today.**

The same applies to Strong Sell.

This is one of the most important distinctions in the whole HMA framework:

```text
Strong state
≠
fresh event
```

---

### Neutral + Aligned Turn

One of the most useful combinations to recognize is:

```text
Signal: Neutral
HMA Direction: Turned Up ▲
Trend Context: Rising
Turn Context: Bullish Trend-Aligned
```

At first glance, the Neutral background may make the observation seem unimportant.

But the two layers are saying:

```text
Primary HMA score
→ bullish conditions have not fully qualified yet

Turning Context
→ a fresh bullish transition has occurred and broader context agrees
```

This can happen because the HMA turn occurs before ATR Distance and slope jointly clear the formal Buy thresholds.

So this pattern can provide:

> **potentially important early-transition information without being a hidden Buy Signal.**

The bearish equivalent is:

```text
Neutral
+
Turned Down ▼
+
Falling
→ Bearish Trend-Aligned
```

---
### Neutral + Counter-trend Turn

Now consider:

```text
Signal: Neutral
HMA Direction: Turned Up ▲
Trend Context: Falling
Turn Context: Bullish Counter-Trend
```

This means:

> **HMA has begun turning upward locally, but the broader trend remains bearish.**

That can represent an early reversal attempt.

But it can also fail and resume the prior downtrend.

The app deliberately does not promote this pattern to Buy merely because a new Up turn occurred.

Likewise:

```text
Neutral
+
Turned Down ▼
+
Rising
→ Bearish Counter-Trend
```

can be an early bearish reversal attempt or simply a pullback within a still-rising trend.

The important point is:

> **Counter-trend does not mean false or unimportant. It means the fresh turn does not yet have broader-trend agreement.**

---
### When 'Signal' and the fresh 'Turn' disagree
$\small{\textsf{Related: 'Appendix: Why contradictory-looking combinations are possible'}}$

Another important family occurs when the established Signal points one way while the timing HMA has just turned the other way.

For example:

```text
Signal: Buy
HMA Direction: Turned Down ▼
Trend Context: Rising
Turn Context: Bearish Counter-Trend
```

The correct interpretation is not:

> “The app contradicts itself.”

It is:

> **The established HMA scoring conditions remain bullish, but the timing HMA has just rolled downward against a still-rising broader trend.**

That is a short-term caution signal inside an otherwise bullish configuration.

A more consequential disagreement would be:

```text
Signal: Buy
HMA Direction: Turned Down ▼
Trend Context: Falling
Turn Context: Bearish Trend-Aligned
```

Here:

```text
primary state
→ still bullish

fresh turn
→ bearish

broader reference
→ also bearish
```

The newest timing evidence is therefore more strongly opposed to the established Signal.

The Signal still should not be overwritten—the primary rule has its own criteria—but the disagreement is worth substantially more attention than a simple counter-trend pullback.

The bullish mirror applies to Sell / Strong Sell states with fresh upward turns.

### Reference: Complete Signal + Turning Context
[Back to top](#summary-how-to-interpret-hma)

The compact table near the beginning of this document highlights the combinations that deserve the most immediate attention.

The table below serves a different purpose:

> **It is the exhaustive lookup reference for normal Rising/Falling Signal + HMA Direction + Trend Context combinations.**

It should be used whenever a displayed combination appears in the app and the user wants to reconstruct what the complete pattern means.

| Pattern                                   | Turn Context              | Trend State Information                                               | Timing Information                                                           | Why it matters                                                                                                    | Bottom-line                                                                                                                                   |
| ----------------------------------------- | ------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Strong Buy + Turned Up ▲ + Rising**     | **Bullish Trend-Aligned** | **Maximum bullish** — price/HMA separation and slope strongly qualify | **Maximum bullish confirmation** — fresh Up turn agrees with broader trend   | Established bullish state and newest timing evidence point the same way                                           | **Strong bullish state + fresh aligned bullish turn. One of the most important bullish patterns.**                                            |
| **Strong Buy + Turned Up ▲ + Falling**    | **Bullish Counter-Trend** | **Maximum bullish**                                                   | Fresh bullish turn, but broader context is bearish                           | The Signal is already strongly bullish, while the turn itself is occurring against its separate broader reference | **Strong bullish state, but the newest Up turn is counter-trend. Bullish, with less contextual confirmation.**                                |
| **Strong Buy + Turned Down ▼ + Rising**   | **Bearish Counter-Trend** | **Maximum bullish**                                                   | Fresh bearish turn against a rising broader trend                            | Strong established bullish conditions remain, but the timing HMA has just rolled over                             | **Strong bullish trend with a fresh short-term caution signal—not a bearish Signal reversal.**                                                |
| **Strong Buy + Turned Down ▼ + Falling**  | **Bearish Trend-Aligned** | **Maximum bullish**                                                   | Fresh bearish turn confirmed by falling broader context                      | This is a meaningful disagreement: strong bullish scoring state versus newly aligned bearish timing evidence      | **Strong bullish state, but the newest timing evidence has turned bearish and is broadly confirmed. Pay attention to the conflict.**          |
| **Strong Buy + None + Rising**            | **—**                     | **Maximum bullish**                                                   | No new timing event                                                          | Strong bullish state is already established; nothing newly reversed today                                         | **Strong ongoing bullish trend. No arrow does not weaken the Signal.**                                                                        |
| **Strong Buy + None + Falling**           | **—**                     | **Maximum bullish**                                                   | No fresh turn; broader context remains bearish                               | Primary bullish state and broader reference disagree even without a fresh turning event                           | **Strong bullish Signal operating against a falling broader context. Bullish state, but context argues for caution.**                         |
| **Buy + Turned Up ▲ + Rising**            | **Bullish Trend-Aligned** | **Qualified bullish**                                                 | **Maximum fresh bullish timing**                                             | A qualified bullish state receives fresh confirmation from an aligned Up turn                                     | **Bullish state + fresh aligned bullish turn. Strong corroboration.**                                                                         |
| **Buy + Turned Up ▲ + Falling**           | **Bullish Counter-Trend** | **Qualified bullish**                                                 | Fresh bullish turn against bearish broader context                           | Current Signal is bullish, but the new turn is not yet supported by its broader reference                         | **Bullish state with a bullish turn, but broader trend confirmation is absent.**                                                              |
| **Buy + Turned Down ▼ + Rising**          | **Bearish Counter-Trend** | **Qualified bullish**                                                 | Fresh bearish turn against rising broader context                            | The established bullish state remains intact while the timing HMA starts moving against it                        | **Bullish trend with a short-term bearish warning; broader context still supports the bullish side.**                                         |
| **Buy + Turned Down ▼ + Falling**         | **Bearish Trend-Aligned** | **Qualified bullish**                                                 | Fresh bearish turn with bearish broader confirmation                         | Both timing components now oppose the still-bullish Signal                                                        | **Bullish Signal, but fresh bearish timing is aligned with the broader trend. More important caution than a simple counter-trend Down turn.** |
| **Buy + None + Rising**                   | **—**                     | **Qualified bullish**                                                 | No fresh timing event                                                        | Ordinary bullish continuation                                                                                     | **Established bullish HMA state; no new reversal today.**                                                                                     |
| **Buy + None + Falling**                  | **—**                     | **Qualified bullish**                                                 | No fresh turn; broader context bearish                                       | Bullish primary state exists against a bearish broader reference                                                  | **Bullish Signal with unfavorable broader context. Treat as less corroborated than Buy + Rising.**                                            |
| **Neutral + Turned Up ▲ + Rising**        | **Bullish Trend-Aligned** | **Unqualified** — primary Buy gates have not all passed               | **High bullish transition significance**                                     | A bullish transition may appear before ATR Distance and slope jointly qualify for Buy                             | **Potential early bullish development. Do not dismiss simply because the Signal is Neutral.**                                                 |
| **Neutral + Turned Up ▲ + Falling**       | **Bullish Counter-Trend** | **Unqualified**                                                       | High bullish timing significance, but counter-trend                          | A local Up reversal has begun while broader trend evidence remains bearish                                        | **Early bullish reversal attempt, not yet a qualified bullish trend.**                                                                        |
| **Neutral + Turned Down ▼ + Rising**      | **Bearish Counter-Trend** | **Unqualified**                                                       | High bearish timing significance, but counter-trend                          | A local Down reversal has started while broader context remains bullish                                           | **Early bearish warning/pullback attempt, not yet a qualified bearish trend.**                                                                |
| **Neutral + Turned Down ▼ + Falling**     | **Bearish Trend-Aligned** | **Unqualified**                                                       | **High bearish transition significance**                                     | Fresh downside turn agrees with bearish broader context even though Sell gates have not fully qualified           | **Potential early bearish development. Do not dismiss simply because the Signal is Neutral.**                                                 |
| **Neutral + None + Rising**               | **—**                     | No qualified directional Signal                                       | No fresh turn; broader context constructive                                  | There is some positive contextual information, but neither a directional score nor fresh event exists             | **Broader trend is rising, but HMA provides neither a qualified bullish Signal nor a new turn today.**                                        |
| **Neutral + None + Falling**              | **—**                     | No qualified directional Signal                                       | No fresh turn; broader context bearish                                       | There is negative contextual information, but no qualified Sell and no new event                                  | **Broader trend is falling, but HMA provides neither a qualified bearish Signal nor a new turn today.**                                       |
| **Sell + Turned Down ▼ + Falling**        | **Bearish Trend-Aligned** | **Qualified bearish**                                                 | **Maximum fresh bearish timing**                                             | Qualified bearish state gains a fresh Down turn supported by the broader trend                                    | **Bearish state + fresh aligned bearish turn. Strong corroboration.**                                                                         |
| **Sell + Turned Down ▼ + Rising**         | **Bearish Counter-Trend** | **Qualified bearish**                                                 | Fresh bearish turn against bullish broader context                           | Primary state and local turn are bearish, but broader reference has not joined them                               | **Bearish state with fresh bearish timing, but broader trend confirmation is absent.**                                                        |
| **Sell + Turned Up ▲ + Falling**          | **Bullish Counter-Trend** | **Qualified bearish**                                                 | Fresh bullish turn against falling broader context                           | Bearish established state remains, while timing HMA has just bounced upward                                       | **Bearish trend with a short-term bullish caution/rebound attempt; broader trend still supports bearishness.**                                |
| **Sell + Turned Up ▲ + Rising**           | **Bullish Trend-Aligned** | **Qualified bearish**                                                 | Fresh bullish turn with bullish broader confirmation                         | Both timing components now oppose the still-bearish primary Signal                                                | **Bearish Signal, but fresh bullish timing is broadly aligned. More consequential warning than a counter-trend bounce.**                      |
| **Sell + None + Falling**                 | **—**                     | **Qualified bearish**                                                 | No fresh timing event                                                        | Ordinary bearish continuation                                                                                     | **Established bearish HMA state; no new reversal today.**                                                                                     |
| **Sell + None + Rising**                  | **—**                     | **Qualified bearish**                                                 | No fresh turn; broader context bullish                                       | Bearish primary state exists against a bullish broader reference                                                  | **Bearish Signal with unfavorable broader context. Less corroborated than Sell + Falling.**                                                   |
| **Strong Sell + Turned Down ▼ + Falling** | **Bearish Trend-Aligned** | **Maximum bearish**                                                   | **Maximum bearish confirmation** — fresh Down turn agrees with broader trend | Established bearish state and newest timing evidence point the same way                                           | **Strong bearish state + fresh aligned bearish turn. One of the most important bearish patterns.**                                            |
| **Strong Sell + Turned Down ▼ + Rising**  | **Bearish Counter-Trend** | **Maximum bearish**                                                   | Fresh bearish turn, but broader context bullish                              | Signal is strongly bearish, while the new Down turn itself is occurring against the separate broader reference    | **Strong bearish state, but the newest Down turn is counter-trend. Bearish, with less contextual confirmation.**                              |
| **Strong Sell + Turned Up ▲ + Falling**   | **Bullish Counter-Trend** | **Maximum bearish**                                                   | Fresh bullish turn against falling broader context                           | Strong bearish conditions remain, but the timing HMA has begun reversing upward                                   | **Strong bearish trend with a fresh short-term bullish caution signal—not a bullish Signal reversal.**                                        |
| **Strong Sell + Turned Up ▲ + Rising**    | **Bullish Trend-Aligned** | **Maximum bearish**                                                   | Fresh bullish turn confirmed by rising broader context                       | Strong bearish scoring state now conflicts with newly aligned bullish timing evidence                             | **Strong bearish Signal, but the newest timing evidence has turned bullish and is broadly confirmed. Pay attention to the conflict.**         |
| **Strong Sell + None + Falling**          | **—**                     | **Maximum bearish**                                                   | No new timing event                                                          | Strong bearish state is already established                                                                       | **Strong ongoing bearish trend. No arrow does not weaken the Signal.**                                                                        |
| **Strong Sell + None + Rising**           | **—**                     | **Maximum bearish**                                                   | No fresh turn; broader context bullish                                       | Primary bearish state and broader reference disagree                                                              | **Strong bearish Signal operating against a rising broader context. Bearish state, but context argues for caution.**                          |

#### How to use the complete reference table

Read the columns in this order:

```text
1. Pattern
→ What combination is present?

2. Turn Context
→ What label appears in the hover?

3. Trend State Information
→ What does the primary Signal say about the established state?

4. Timing Information
→ What new event/context information is present?

5. Why it matters
→ Why is this combination worth noticing?

6. Bottom-line
→ What should the user mentally translate the whole pattern as?
```

The reference should not be read as a backtested performance ranking.

Its purpose is interpretive:

> **Every normal combination should be understandable, even if some combinations contain substantially more information than others.**

A useful priority rule is:
```text
Do not overlook:
- Strong directional state + fresh aligned turn
- Neutral + fresh aligned turn
- established directional Signal + fresh opposing aligned turn
- Strong directional state even when there is no new turn
```

Those patterns answer different questions, but each carries information that can be easy to miss if the user looks only at the cell background or only at the arrow.

---


### Representative Production Examples

The combination tables above explain what the different HMA patterns mean conceptually.

The examples below show several of those patterns as they actually appeared in the earlier bounded production diagnostic.

They are included for **interpretation**, not as evidence that one pattern produces better subsequent returns than another.

The purpose is to connect:

```text
what appeared in the heatmap / hover
→
the underlying numeric inputs
→
the Signal
→
the Turning Context
→
the practical interpretation
```

---

#### Example 1 — Strong Buy + fresh bullish trend-aligned turn

```text
AAPL — 2026-07-27 — HMA(16)

HMA: 331.93
Signal: Strong Buy
ATR Distance: +0.611 ATR
14-bar HMA Slope: +0.579%/bar
HMA Direction: Turned Up
Trend Context: Rising
Turn Context: Bullish Trend-Aligned
```

This observation contains two different kinds of bullish information.

First, the primary Signal is already:

```text
Strong Buy
```

For HMA(16), the observation clears both Strong Buy requirements:

```text
ATR Distance:
+0.611 > +0.50 ATR

14-bar HMA Slope:
+0.579 > +0.50%/bar
```

So price is meaningfully above HMA(16), and HMA(16)'s established trajectory is steeply positive.

At the same time:

```text
HMA Direction: Turned Up
Trend Context: Rising
```

produces:

```text
Turn Context: Bullish Trend-Aligned
```

So the HMA also produced a **fresh upward turn on this observation**, and that turn agreed with its broader trend context.

> **Bottom-line:** This is an example of **strong established bullish state + fresh bullish timing + broader-trend agreement**. Both analytical layers are pointing bullish at the same time.

This combination was observed directly in the earlier production diagnostic.

---

#### Example 2 — Strong Buy without a fresh turn

```text
SPY — 2026-04-15 — HMA(16)

HMA: 692.41
Signal: Strong Buy
ATR Distance: +0.794 ATR
14-bar HMA Slope: +0.548%/bar
HMA Direction: None
```

The primary Signal remains very strong:

```text
ATR Distance:
+0.794 > +0.50 ATR

14-bar HMA Slope:
+0.548 > +0.50%/bar
```

so:

```text
Signal: Strong Buy
```

But:

```text
HMA Direction: None
```

means there was **no new HMA reversal on this date**.

This is exactly why HMA state strength and HMA turning information must remain separate.

> **Bottom-line:** The bullish condition is already strongly established. The absence of an arrow does **not** weaken the Strong Buy classification; it only says that this particular observation is not a fresh turning event.

The earlier diagnostic preserved this example specifically to illustrate that distinction.

---

#### Example 3 — Neutral Signal + fresh bullish trend-aligned turn

```text
SPY — 2026-04-30 — HMA(16)

HMA: 717.12
Signal: Neutral
ATR Distance: +0.196 ATR
14-bar HMA Slope: +0.393%/bar
HMA Direction: Turned Up
Trend Context: Rising
```

Start with the Signal inputs.

The slope is clearly positive:

```text
+0.393%/bar
```

and falls inside HMA(16)'s ordinary Buy slope range:

```text
> +0.20%/bar
and
<= +0.50%/bar
```

But ATR Distance is only:

```text
+0.196 ATR
```

which does not clear the required:

```text
> +0.50 ATR
```

price-distance gate.

Therefore:

```text
Signal: Neutral
```

At the same time, HMA(16) has:

```text
HMA Direction: Turned Up
Trend Context: Rising
Turn Context: Bullish Trend-Aligned
```

which is the bullish trend-aligned turning pattern.

The important lesson is that the fresh turn can appear **before** the formal Buy conditions have fully qualified.

> **Bottom-line:** The primary Signal is still Neutral because price has not separated far enough from HMA, but a fresh upward transition has occurred in agreement with the broader trend. This is meaningful **early-transition information**, not a hidden Buy Signal.

This example was observed directly in the earlier production diagnostic.

---

#### Example 4 — Neutral Signal + fresh bullish counter-trend turn

```text
SPY — 2026-04-01 — HMA(16)

HMA: 639.65
Signal: Neutral
ATR Distance: +1.504 ATR
14-bar HMA Slope: -0.388%/bar
HMA Direction: Turned Up
Trend Context: Falling
Turn Context: Bullish Counter-Trend
```

Here, price is actually well above HMA in volatility-adjusted terms:

```text
ATR Distance: +1.504 ATR
```

But HMA's established trajectory remains negative:

```text
14-bar HMA Slope: -0.388%/bar
```

The bullish Signal requirements therefore do not agree:

```text
price position
→ bullish

established HMA trajectory
→ bearish
```

so:

```text
Signal: Neutral
```

Yet HMA has just changed its immediate direction upward:

```text
HMA Direction: Turned Up
```

while its broader HMA16 trend context remains:

```text
Falling
```

therefore:

```text
Turn Context: Bullish Counter-Trend
```

> **Bottom-line:** HMA has begun turning upward locally, but its established trend evidence remains bearish. This can be useful as an early reversal attempt, but it is not yet a qualified bullish HMA state.

This example shows why `Counter-Trend` should not be translated as either “bad” or “confirmed reversal.”

---

#### Example 5 — Strong Sell + fresh bearish trend-aligned turn

```text
AAPL — 2026-06-25 — HMA(21)

HMA: 290.77
Signal: Strong Sell
ATR Distance: -1.981 ATR
14-bar HMA Slope: -0.633%/bar
HMA Direction: Turned Down
Trend Context: Falling
Turn Context: Bearish Trend-Aligned
```

The primary HMA(21) state is strongly bearish:

```text
ATR Distance:
-1.981 < -0.50 ATR

14-bar HMA Slope:
-0.633 < -0.50%/bar
```

so:

```text
Signal: Strong Sell
```

At the same time:

```text
HMA Direction: Turned Down
Trend Context: Falling
```

produces:

```text
Turn Context: Bearish Trend-Aligned
```

The fresh downside turn therefore agrees with the broader trend context.

> **Bottom-line:** This is the bearish mirror of Example 1: **strong established bearish state + fresh bearish timing + broader-trend agreement**.

The combination was observed directly in the earlier production diagnostic.

---

#### Example 6 — Strong Sell without a fresh turn

```text
AAPL — 2026-06-26 — HMA(21)

HMA: 288.54
Signal: Strong Sell
ATR Distance: -0.584 ATR
14-bar HMA Slope: -0.551%/bar
```

The primary Signal remains Strong Sell because both HMA(21) Strong Sell conditions qualify:

```text
ATR Distance:
-0.584 < -0.50 ATR

14-bar HMA Slope:
-0.551 < -0.50%/bar
```

The earlier diagnostic identified this as a **Strong Sell without a new HMA turn**.

> **Bottom-line:** The bearish trend state is already strongly established. This observation illustrates the same principle as the bullish no-turn example: **a Strong state does not require a new turning event on every bar**.


---
#### What these examples are meant to teach

Taken together, the examples illustrate four different situations a user should learn to distinguish:

| Situation                              | Representative example            | Main lesson                                                                                |
| -------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------ |
| **Strong state + fresh aligned turn**  | AAPL 2026-07-27 / AAPL 2026-06-25 | Established trend strength and fresh timing confirmation are present together              |
| **Strong state + no fresh turn**       | SPY 2026-04-15 / AAPL 2026-06-26  | No arrow does not weaken an already-qualified Strong Signal                                |
| **Neutral + fresh aligned turn**       | SPY 2026-04-30                    | A meaningful transition can occur before the primary Signal qualifies                      |
| **Neutral + fresh counter-trend turn** | SPY 2026-04-01                    | A fresh reversal attempt can occur while broader trend evidence still points the other way |

The key distinction is:

```text
Signal
→ What is already qualified?

Turning Context
→ What just changed?
```

A production observation can contain strong information in either dimension—or in both.

---
## Understanding the HMA Hover
The HMA hover contains several fields because it is trying to answer **different questions rather than repeat the same answer in different forms**.

A typical hover may show:

```
Value:
Δ vs prior day:
Trend:
Price vs. HMA:
ATR Distance:
14-bar HMA Slope:
Signal:
HMA Direction:
Trend Context:
Turn Context:

Rule:
Notes:
Definition:
How to Read:
```

The easiest way to understand the fields is:

| Hover field          | Question it answers                                                                                                                |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Value**            | What is the HMA level right now?                                                                                                   |
| **Δ vs prior day**   | How much did the HMA value change since the prior observation?                                                                     |
| **Trend**            | Did the HMA itself rise or fall versus the prior observation?                                                                      |
| **Price vs. HMA**    | How far stock price is above or below HMA? (How many dollars / percent is price above or below HMA?)                               |
| **ATR Distance**     | Is that price/HMA separation large or small relative to normal volatility? (Volatility-normalized significance of that separation) |
| **14-bar HMA Slope** | What is HMA's established recent trajectory?                                                                                       |
| **Signal**           | Do ATR Distance and slope together qualify for one of the five HMA states?                                                         |
| **HMA Direction**    | Did HMA actually change direction today?                                                                                           |
| **Trend Context**    | What is the broader/reference trend doing?                                                                                         |
| **Turn Context**     | Does today's new HMA direction agree with or oppose that trend?                                                                    |

---
### What the five key Signal and Timing fields contribute

These five fields fall into two groups.
- :gray-background[ATR Distance] and :gray-background[14-bar HMA Slope] help determine the **Signal**.
- :gray-background[HMA Direction] and :gray-background[Trend Context] describe the **timing/context layer**, which combines into :gray-background[Turn Context].

This separation is why a strong Signal can exist without a new turn, and why a meaningful new turn can appear while the Signal is still Neutral.

| Field                | Essential meaning                                                          | Analytical purpose                                                                   | Critical interpretation                                                                                                                                                 |
| -------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ATR Distance**     | Price's distance from the selected HMA measured in ATR units.              | Makes price/HMA separation comparable across stocks and volatility regimes.          | Positive = price above HMA; negative = below. It is one of the gates used by the HMA Signal.                                                                            |
| **14-bar HMA Slope** | The HMA's 14-bar regression slope normalized as % per bar.                 | Measures the direction and strength of HMA's established trajectory.                 | Positive supports Buy; negative supports Sell. Larger magnitude = steeper trend. It is the other major HMA Signal input.                                                |
| **HMA Direction**    | Whether the designated HMA **changed direction today**.                    | Flags a fresh turning event rather than an ongoing trend.                            | :gray-background[Turned Up/Down] appears only on the reversal day; :gray-background[None] means no new turn occurred today.                                                                             |
| **Trend Context**    | The broader/reference trend against which the new HMA direction is judged. | Distinguishes a turn occurring with the broader trend from one occurring against it. | :gray-background[Rising], :gray-background[Falling], :gray-background[Flat], or :gray-background[—]. <li>:gray-background[Rising/Falling] provide the directional context used for named 'Turn Context' labels. <li> Does not alter the Signal score. |
| **Turn Context**     | The relationship between HMA Direction and Trend Context.                  | Summarizes whether the fresh turn is trend-aligned or counter-trend.                 | Aligned = turn and broader trend agree; Counter-Trend = they oppose. This is descriptive, not an extra score.                                                           |


---

The shortest useful shorthand is:

```
ATR Distance
→ Where is price relative to HMA?

14-bar HMA Slope
→ What is the established HMA trajectory?

HMA Direction
→ Did HMA change direction today?

Trend Context
→ What is the broader trend doing?

Turn Context
→ Does today's new direction agree with it?
```

---

### 'Trend' is not the same thing as 'HMA Direction'


This distinction is important.

The standard hover field:

```
Trend: Rising
```

simply means:

```
today's HMA > yesterday's HMA
```

For example:

```
Yesterday HMA = 210.00
Today HMA     = 210.25

Trend: Rising
```

That tells you the HMA increased today.

:gray-background[HMA Direction], however, asks:

> **Did the direction itself change today?**

The possible values are:

```
Turned Up ▲
Turned Down ▼
None
```

:gray-background[None] does **not** mean HMA has no direction.

It means:

> **There was no new turn today.**

A HMA can therefore show:

```
Trend: Rising
HMA Direction: None
```

for many consecutive sessions.

That simply means:
> **HMA continues to rise, but the upward turn happened earlier.**

NOTE:
The exact :gray-background[Turned Up/Turned Down] production logic is explained earlier under '***The Two Inputs That Drive Turn Context → HMA Direction***'.

---

#### Multi-day example: Trend vs. HMA Direction


Suppose HMA behaves like this:

|Day|HMA|Trend|HMA Direction|
|---|---|---|---|
|Day 1|210.40|—|—|
|Day 2|209.90|Falling|None|
|Day 3|209.60|Falling|None|
|Day 4|209.85|Rising|**Turned Up ▲**|
|Day 5|210.10|Rising|None|
|Day 6|210.30|Rising|None|
|Day 7|210.05|Falling|**Turned Down ▼**|

On Day 4:

```
209.85 > 209.60
```

and:

```
209.60 <= 209.90
```

so the rule detects a new upward turn.

On Day 5:

```
210.10 > 209.85
```

but the previous move was already upward.

Therefore:

```
HMA Direction: None
```

not another :gray[Turned Up].

The key is:

> - **'Trend' describes movement every day.**
> - **'HMA Direction' marks only the day that movement changes direction.**

---
## How to Read an HMA Heatmap Cell

The HMA cell combines several visual and hover elements.

They should be read as separate pieces of information rather than as one undifferentiated signal.

| Display element             | What it represents                         | Question answered                                         |
| --------------------------- | ------------------------------------------ | --------------------------------------------------------- |
| **Displayed HMA value**     | Current HMA level                          | **Where is the HMA itself?**                              |
| **Cell background**         | Primary five-state Signal                  | **What qualified HMA trend state exists?**                |
| **▲ / ▼**                   | HMA Direction                              | **Did a new turn occur today, and which way?**            |
| **Blue / red turn text**    | Rising/Falling Trend Context               | **What direction is the broader/reference trend moving?** |
| **Hover: ATR Distance**     | Volatility-normalized price/HMA separation | **Is price far enough from HMA to matter?**               |
| **Hover: 14-bar HMA Slope** | Established normalized HMA trajectory      | **How strongly is HMA trending?**                         |
| **Hover: Turn Context**     | Turn/reference relationship                | **Is the fresh turn aligned or counter-trend?**           |

The adapter displays ATR Distance and 14-bar HMA Slope before the Signal/context block and exposes the three formal turning fields on HMA16/21/55.

---
### Read the background first

The cell background represents:

```text
Strong Buy
Buy
Neutral
Sell
Strong Sell
```

This is the primary HMA Signal.

It tells you the current qualified trend state.

Do **not** infer the Signal from the arrow or font color.

Those belong to Turning Context.

---

### Then read the arrow

On HMA16, HMA21, and HMA55:

```text
▲
→ HMA turned upward today

▼
→ HMA turned downward today

no arrow
→ no new turn today
```

The arrow is therefore a timing event.

It does not mean:

```text
▲ = Buy
▼ = Sell
```

A gray Neutral cell can legitimately contain either arrow.

A Strong Buy cell can legitimately contain no arrow.

---

### Then read the font color

On turn dates, font color communicates the broader/reference Trend Context:

```text
Blue
→ Rising

Red
→ Falling
```

Therefore:

```text
blue ▲
→ Bullish Trend-Aligned
```

```text
red ▲
→ Bullish Counter-Trend
```

```text
red ▼
→ Bearish Trend-Aligned
```

```text
blue ▼
→ Bearish Counter-Trend
```

The current adapter describes this exact display grammar.

---

### A practical reading sequence

When you encounter an HMA cell, work through it in this order:

| Step  | Question                                                           |
| ----- | ------------------------------------------------------------------ |
| **1** | What is the primary Signal from the cell background?               |
| **2** | What is the displayed HMA value?                                   |
| **3** | What does :gray-badge[ATR Distance] say about price separation?               |
| **4** | What does :gray-badge[14-bar HMA Slope] say about the established trajectory? |
| **5** | Can I reconstruct why the primary Signal received that state?      |
| **6** | On HMA16/21/55, is there a fresh :gray-badge[HMA Direction] event?            |
| **7** | What does :gray-badge[Trend Context] say?                                     |
| **8** | What :gray-badge[Turn Context] does that combination produce?                 |
| **9** | Am I looking at an established trend, a fresh transition, or both? |

The most important conceptual shortcut is:

```text
Background
→ state

Arrow
→ new event

Font color
→ broader direction

Turn Context
→ relationship between event and broader direction
```

---

### Worked display example

Suppose an HMA21 cell shows:

```text
640.30 ▲
```

with:

```text
gray background
red font
```

The display translates as:

```text
gray background
→ Signal: Neutral

▲
→ HMA Direction: Turned Up

red font
→ Trend Context: HMA(55) Falling

therefore
→ Turn Context: Bullish Counter-Trend
```

The correct interpretation is:

> **HMA21 has just turned upward, but its slower HMA55 reference is still falling. The primary HMA21 scoring conditions have not yet jointly qualified as Buy.**

That is an:

```text
early bullish counter-trend transition
```

not:

```text
confirmed bullish HMA trend
```

---

$\large{\rightarrow}$ Next: $\large{\textsf{"Interpretation Boundaries and Limitations"}}$ (see Appendix)


---
## Signal Rules Translation
[top](#summary-how-to-interpret-hma)

HMA(9), HMA(16), HMA(21), HMA(50), HMA(55), and HMA(200) all use the same basic Signal architecture:

```text
qualified price separation from HMA
+
qualified 14-bar HMA trajectory
=
directional HMA Signal
```

The examples below use **HMA(21)** because its thresholds are representative of HMA(16), HMA(21), HMA(50), and HMA(55).

For HMA(21), the current production thresholds are:

```text
Price-distance gate:  ±0.50 ATR(14)
Buy/Sell slope gate:  ±0.20% per bar
Strong slope gate:    ±0.50% per bar
```

The current rulebook defines HMA(21) as follows:

```text
Strong Buy
(Close - HMA_21) / ATR_14 > 0.50
and
(HMA_21_slope__linreg_14 / HMA_21) * 100 > 0.50

Buy
(Close - HMA_21) / ATR_14 > 0.50
and
(HMA_21_slope__linreg_14 / HMA_21) * 100 > 0.20
and
(HMA_21_slope__linreg_14 / HMA_21) * 100 <= 0.50

Neutral
fallback when no directional rule qualifies

Sell
(Close - HMA_21) / ATR_14 < -0.50
and
(HMA_21_slope__linreg_14 / HMA_21) * 100 < -0.20
and
(HMA_21_slope__linreg_14 / HMA_21) * 100 >= -0.50

Strong Sell
(Close - HMA_21) / ATR_14 < -0.50
and
(HMA_21_slope__linreg_14 / HMA_21) * 100 < -0.50
```

One syntax rule matters throughout this section:

```text
AND
```

means:

> **Every condition connected by `and` must be true at the same time.**

The user should therefore evaluate the rule conceptually in this order:

```text
1. What direction is HMA's established trajectory?
2. Is that trajectory strong enough to qualify?
3. Is price far enough from HMA in the same direction to make that trend state meaningful?
4. If it qualifies, is the trajectory ordinary or Strong?
```

That order is more intuitive than reading the formula mechanically from left to right.

---

### Strong Buy (+2)

The HMA(21) Strong Buy rule is:

```text
(Close - HMA_21) / ATR_14 > 0.50
and
(HMA_21_slope__linreg_14 / HMA_21) * 100 > 0.50
```

A Strong Buy requires **two things**:

```text
1. HMA(21) must have a very steep established upward trajectory.
2. Price must also be meaningfully above HMA(21).
```

#### 1. Is HMA(21) rising strongly enough to count as a Strong bullish trend?

This part of the rule is:

```text
(HMA_21_slope__linreg_14 / HMA_21) * 100 > 0.50
```

This is the **14-bar HMA Slope** shown in the hover.

It asks:

> **Over the recent 14-bar window, is HMA(21)'s established trajectory rising at more than +0.50% of its current level per bar?**

Suppose the hover shows:

```text
14-bar HMA Slope: +0.68%/bar
```

Then:

```text
+0.68 > +0.50
```

so the Strong bullish slope condition passes.

If instead:

```text
14-bar HMA Slope: +0.35%/bar
```

HMA is still rising, but not steeply enough for Strong Buy.

**Bottom-line:** Answers the question **“Is HMA itself rising strongly enough to qualify as a Strong bullish trajectory?”**

---

#### 2. Is price meaningfully above that rising HMA?

This part is:

```text
(Close - HMA_21) / ATR_14 > 0.50
```

The result is the hover's **ATR Distance**.

It asks:

> **Is price more than one-half of an ATR(14) above HMA(21)?**

Suppose:

```text
Close   = $104
HMA(21) = $101
ATR(14) = $4
```

Then:

```text
Close - HMA(21)
=
$104 - $101
=
+$3
```

and:

```text
+$3 / $4
=
+0.75 ATR
```

Because:

```text
+0.75 > +0.50
```

the price-distance condition passes.

The point of the ATR adjustment is that it does not merely ask whether price is above HMA by a few cents. It asks whether the separation is meaningful relative to how much the security has recently been moving.

**Bottom-line:** Answers the question **“Is price far enough above HMA for the separation to matter relative to recent volatility?”**

---

#### Putting the Strong Buy rule together

Suppose the hover shows:

```text
ATR Distance:      +0.75 ATR
14-bar HMA Slope:  +0.68%/bar
```

Then:

```text
Price-distance test:
+0.75 > +0.50
PASS

Strong slope test:
+0.68 > +0.50
PASS
```

Therefore:

```text
Signal: Strong Buy
```

A beginner should be able to translate that as:

> **Price is meaningfully above HMA(21), and HMA(21) itself has a very steep established upward trajectory. Both parts agree strongly enough for the app to classify the current HMA trend state as Strong Buy.**

**Bottom-line:** `Strong Buy` means **meaningfully elevated price position + very strong upward HMA trajectory**.

It does **not** mean HMA just turned upward today; that is a separate `HMA Direction` question.

---

### Buy (+1)

The HMA(21) Buy rule is:

```text
(Close - HMA_21) / ATR_14 > 0.50
and
(HMA_21_slope__linreg_14 / HMA_21) * 100 > 0.20
and
(HMA_21_slope__linreg_14 / HMA_21) * 100 <= 0.50
```

This looks like three conditions, but conceptually it is easier to understand as **two tests**:

```text
A. Is HMA(21) rising at a qualified—but not Strong—rate?
B. Is price meaningfully above HMA(21)?
```

The first test happens to require both a lower and an upper boundary.

---

#### 1. Is HMA(21) rising strongly enough to qualify as bullish?

The lower slope boundary is:

```text
(HMA_21_slope__linreg_14 / HMA_21) * 100 > 0.20
```

This means:

> **The normalized 14-bar HMA slope must be greater than +0.20% per bar.**

Suppose:

```text
14-bar HMA Slope: +0.32%/bar
```

Then:

```text
+0.32 > +0.20
```

so HMA's established trajectory is sufficiently positive for a bullish state.

If the slope were only:

```text
+0.12%/bar
```

HMA would technically be rising, but the project does not consider that rise strong enough to qualify as ':gray-background[Buy]'.

This threshold prevents a very shallow or nearly flat HMA from being called bullish merely because the slope happens to be slightly above zero.

**Bottom-line:** Answers the question **“Is HMA's established upward trajectory strong enough to count as a qualified bullish trend rather than a weak rise?”**

---

#### 2. Is the upward trajectory still in the ordinary Buy range rather than the Strong Buy range?

The upper slope boundary is:

```text
(HMA_21_slope__linreg_14 / HMA_21) * 100 <= 0.50
```

This means:

> **The slope must be no greater than +0.50% per bar.**

Why is that condition needed?

Because anything above:

```text
+0.50%/bar
```

belongs to:

```text
Strong Buy
```

So `Buy` occupies the slope interval:

```text
greater than +0.20%/bar
through
+0.50%/bar
```

or more compactly:

```text
+0.20 < slope <= +0.50
```

Examples:

| 14-bar HMA Slope | Interpretation                                           |
| ---------------: | -------------------------------------------------------- |
|     `+0.15%/bar` | Too weak for Buy                                         |
|     `+0.20%/bar` | Still too weak; the rule requires **greater than** +0.20 |
|     `+0.21%/bar` | Buy-range slope                                          |
|     `+0.35%/bar` | Buy-range slope                                          |
|     `+0.50%/bar` | Still Buy-range                                          |
|     `+0.51%/bar` | Strong Buy-range                                         |

This condition is not asking a new market question. It is establishing **which bullish severity bucket** the already-qualified slope belongs to.

**Bottom-line:** Answers the question **“Is the bullish HMA trajectory moderate enough to remain Buy, rather than strong enough to become Strong Buy?”**

---

#### 3. Is price meaningfully above HMA(21)?

Now evaluate:

```text
(Close - HMA_21) / ATR_14 > 0.50
```

This requires:

```text
ATR Distance > +0.50 ATR
```

Suppose:

```text
ATR Distance: +0.72 ATR
```

That means price is 0.72 ATR above HMA(21), so:

```text
+0.72 > +0.50
```

and the condition passes.

But:

```text
ATR Distance: +0.31 ATR
```

would fail even if the HMA slope were a perfectly qualified:

```text
+0.35%/bar
```

Why?

Because the app requires the **price position and HMA trajectory to agree**. A rising HMA alone is not enough.

**Bottom-line:** Answers the question **“Has price moved far enough above HMA to make the bullish separation material relative to recent volatility?”**

---

#### Putting the Buy rule together

Suppose:

```text
ATR Distance:      +0.78 ATR
14-bar HMA Slope:  +0.34%/bar
```

Evaluate the trajectory first:

```text
+0.34 > +0.20
PASS

+0.34 <= +0.50
PASS
```

Therefore:

```text
HMA trajectory = qualified bullish, but not Strong
```

Then evaluate price separation:

```text
+0.78 > +0.50
PASS
```

Everything agrees:

```text
qualified bullish trajectory
+
meaningfully above HMA
=
Buy
```

A beginner should be able to explain the result as:

> **HMA(21) has a clearly rising established trajectory, but it is not steep enough to be Strong. Price is also more than half an ATR above HMA, so price position confirms that bullish trajectory. The app therefore classifies the current state as Buy.**

**Bottom-line:** `Buy` means **price is materially above HMA and HMA is rising at a qualified, but not Strong, rate.**

---

### Why `Buy` requires both slope boundaries

This deserves a short explicit note because the production rule can otherwise look unnecessarily complicated.

The two slope clauses:

```text
slope > +0.20
and
slope <= +0.50
```

are simply defining one interval:

```text
+0.20 < slope <= +0.50
```

Think of the bullish slope scale as:

```text
                Buy                     Strong Buy
                 │                          │
---------|-------|--------------------------|------------>
       +0.20                              +0.50

       not Buy       > +0.20 through +0.50      > +0.50
```

So the Buy rule is not applying two different kinds of bullish tests.

It is saying:

> **The HMA trajectory must be strong enough to qualify, but if it is stronger than +0.50%/bar it belongs in Strong Buy instead.**

---

### Neutral (0)

The HMA(21) rulebook contains:

```text
"neutral": ""
```

That is intentional.

Unlike an oscillator whose Neutral state may have an explicit range such as:

```text
-150 < CCI <= +150
```

HMA Neutral is the **fallback state**.

In plain English:

> **If a valid HMA observation does not satisfy Strong Buy, Buy, Sell, or Strong Sell, it remains Neutral.**

This is important because there is no single numeric condition that means:

```text
Neutral
```

Several different situations can produce it.

---

#### Neutral case 1 — HMA is rising, but too weakly

Suppose:

```text
ATR Distance:      +0.85 ATR
14-bar HMA Slope:  +0.12%/bar
```

Price is clearly above HMA:

```text
+0.85 > +0.50
PASS
```

but:

```text
+0.12 > +0.20
FAIL
```

So:

```text
Signal: Neutral
```

The price position is bullish-looking, but HMA's established trajectory is not strong enough to confirm it.

**Bottom-line:** Answers **“Do price position and HMA trajectory jointly qualify?”** Here the answer is **no because slope is too weak**.

---

#### Neutral case 2 — HMA is rising strongly enough, but price is too close to HMA

Suppose:

```text
ATR Distance:      +0.18 ATR
14-bar HMA Slope:  +0.37%/bar
```

The slope passes the Buy-range test:

```text
+0.37 > +0.20
PASS

+0.37 <= +0.50
PASS
```

but price does not pass:

```text
+0.18 > +0.50
FAIL
```

Therefore:

```text
Signal: Neutral
```

The HMA trend is bullish, but price has not separated enough from HMA to qualify under the rule.

**Bottom-line:** Answers **“Is the price/HMA separation large enough to confirm the otherwise bullish trajectory?”** Here the answer is **no**.

---

#### Neutral case 3 — price and HMA trajectory disagree

Suppose:

```text
ATR Distance:      +0.90 ATR
14-bar HMA Slope:  -0.33%/bar
```

Price is materially above HMA:

```text
bullish price position
```

but HMA's established trajectory is:

```text
bearish
```

No bullish rule can qualify because the slope is negative.

No bearish rule can qualify because price is above HMA rather than more than 0.50 ATR below it.

Therefore:

```text
Signal: Neutral
```

**Bottom-line:** Answers **“Are price position and HMA trajectory pointing in the same qualified direction?”** Here the answer is **no—they disagree**.

---

#### The key meaning of Neutral

A beginner should **not** translate Neutral as:

> “Nothing is happening.”

Nor should they automatically translate it as:

> “HMA is flat.”

The correct translation is:

> **The price-position and HMA-trajectory requirements do not currently combine into one of the four qualified directional Signal states.**

And, as discussed elsewhere in this document, a Neutral Signal can still coexist with important turning information such as:

```text
HMA Direction: Turned Up ▲
Trend Context: Rising
Turn Context: Bullish Trend-Aligned
```

because Turning Context does not determine the Signal.

**Bottom-line:** :gray-background[Neutral] answers **“Do the two primary scoring inputs currently agree strongly enough to produce a qualified bullish or bearish state?”** If not, the Signal remains Neutral.

---

### Sell (-1)

The HMA(21) Sell rule is:

```text
(Close - HMA_21) / ATR_14 < -0.50
and
(HMA_21_slope__linreg_14 / HMA_21) * 100 < -0.20
and
(HMA_21_slope__linreg_14 / HMA_21) * 100 >= -0.50
```

Sell is the bearish mirror of Buy.

Conceptually, ask:

```text
A. Is HMA(21) falling at a qualified—but not Strong—rate?
B. Is price meaningfully below HMA(21)?
```

---

#### 1. Is HMA(21) falling strongly enough to qualify as bearish?

The first slope boundary is:

```text
(HMA_21_slope__linreg_14 / HMA_21) * 100 < -0.20
```

This means:

> **HMA's normalized 14-bar trajectory must be more negative than -0.20% per bar.**

For example:

```text
14-bar HMA Slope: -0.31%/bar
```

passes because:

```text
-0.31 < -0.20
```

But:

```text
-0.12%/bar
```

does not.

HMA may technically be falling, but not strongly enough to count as a qualified bearish trend under the project rule.

**Bottom-line:** Answers the question **“Is HMA's established downward trajectory strong enough to qualify as bearish rather than merely drifting lower?”**

---

#### 2. Is the bearish trajectory still in Sell rather than Strong Sell territory?

The next condition is:

```text
(HMA_21_slope__linreg_14 / HMA_21) * 100 >= -0.50
```

This keeps Sell inside the interval:

```text
-0.50 <= slope < -0.20
```

For example:

| 14-bar HMA Slope | Interpretation                              |
| ---------------: | ------------------------------------------- |
|     `-0.15%/bar` | Too weak for Sell                           |
|     `-0.20%/bar` | Too weak; Sell requires **less than** -0.20 |
|     `-0.21%/bar` | Sell-range                                  |
|     `-0.35%/bar` | Sell-range                                  |
|     `-0.50%/bar` | Still Sell-range                            |
|     `-0.51%/bar` | Strong Sell-range                           |

**Bottom-line:** Answers the question **“Is the bearish trajectory qualified but still moderate enough to remain Sell rather than Strong Sell?”**

---

#### 3. Is price meaningfully below HMA(21)?

The **'price-distance' condition** is:

```text
(Close - HMA_21) / ATR_14 < -0.50
```

This means:

> **Price must be more than one-half of an ATR below HMA(21).**

Suppose:

```text
ATR Distance: -0.74 ATR
```

Then:

```text
-0.74 < -0.50
```

so the condition passes.

**Bottom-line:** Answers the question **“Has price moved far enough below HMA for the bearish separation to matter relative to recent volatility?”**

---

#### Putting the Sell rule together

Suppose:

```text
ATR Distance:      -0.82 ATR
14-bar HMA Slope:  -0.36%/bar
```

Then:

```text
-0.36 < -0.20
PASS

-0.36 >= -0.50
PASS
```

so the trajectory is qualified bearish but not Strong.

And:

```text
-0.82 < -0.50
PASS
```

so price is meaningfully below HMA.

Therefore:

```text
Signal: Sell
```

A beginner translation is:

> **HMA(21) is falling clearly enough to qualify as bearish, but not steeply enough for Strong Sell. Price is also materially below HMA, so the price position confirms the bearish trajectory.**

**Bottom-line:** `Sell` means **price is materially below HMA and HMA is falling at a qualified, but not Strong, rate.**

---

### Strong Sell (-2)

The HMA(21) Strong Sell rule is:

```text
(Close - HMA_21) / ATR_14 < -0.50
and
(HMA_21_slope__linreg_14 / HMA_21) * 100 < -0.50
```

A Strong Sell therefore requires:

```text
1. A very steep established downward HMA trajectory.
2. Price meaningfully below that HMA.
```

---

#### 1. Is HMA(21) falling strongly enough to count as a Strong bearish trajectory?

The slope condition, or '`(HMA_21_slope__linreg_14 / HMA_21) * 100 < -0.50`', is:

```text
normalized 14-bar HMA slope < -0.50%/bar
```

Suppose:

```text
14-bar HMA Slope: -0.67%/bar
```

Then:

```text
-0.67 < -0.50
```

so the Strong bearish slope condition passes.

**Bottom-line:** Answers the question **“Is HMA itself falling steeply enough to qualify as a Strong bearish trajectory?”**

---

#### 2. Is price meaningfully below that falling HMA?

The price condition remains:

```text
ATR Distance < -0.50 ATR
```

For example:

```text
ATR Distance: -0.91 ATR
```

passes.

Notice that the price-distance threshold is **not made more extreme** for Strong Sell.

The distinction between:

```text
Sell
```

and:

```text
Strong Sell
```

comes from the HMA slope severity.

Both still require price to clear the same `-0.50 ATR` gate.

**Bottom-line:** Answers the question **“Is price positioned far enough below HMA to confirm that strong downward trajectory?”**

---

#### Putting the Strong Sell rule together

Suppose:

```text
ATR Distance:      -0.91 ATR
14-bar HMA Slope:  -0.67%/bar
```

Both conditions pass.

Therefore:

```text
Signal: Strong Sell
```

Beginner translation:

> **Price is meaningfully below HMA(21), and HMA itself has a very steep established downward trajectory. Both conditions agree strongly enough for Strong Sell.**

**Bottom-line:** `Strong Sell` means **meaningfully depressed price position + very strong downward HMA trajectory**.


---

### Documentation references

This document follows the project's established beginner-first documentation approach used in the CCI and Bull Bear Power references:

```text
primary Signal first
→ secondary context
→ combined interpretation
→ deeper calculation/rule explanation
```

The HMA-specific structure expands that pattern because HMA has two especially distinct analytical layers:

```text
Signal
→ established trend state

Turning Context
→ fresh directional transition
```


---
## My Notes
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
