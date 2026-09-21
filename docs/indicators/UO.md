## Ultimate Oscillator - Table of Contents
1. [UO Heatmap Translation Cheat Sheets](#uo-heatmap-translation-cheat-sheets)
2. [Ultimate Oscillator — At a Glance](#ultimate-oscillator--at-a-glance)
3. [Reading the UO Heatmap](#reading-the-uo-heatmap)
4. [UO Hover Field Reference](#uo-hover-field-reference)
5. [The Staged Reversal Framework](#the-staged-reversal-framework)
6. [The Three UO Variants](#the-three-uo-variants)
7. [How UO Is Calculated](#how-uo-is-calculated)
8. [Worked Heatmap Examples](#worked-heatmap-examples)
9. [Practical Reading Guide](#practical-reading-guide)
10. [Limitations, Warmup, and Interpretation Boundaries](#limitations-warmup-and-interpretation-boundaries)
11. [Glossary and Quick Reference](#glossary-and-quick-reference)

[Complete Outline](#table-of-contents-complete-outline)

$$----------$$

**[Common UO Combinations](#common-uo-combinations)**
- [Watch + Strengthening Pressure Mix](#watch--strengthening-pressure-mix)
- [Watch + Weakening Pressure Mix](#watch--weakening-pressure-mix)
- [Divergence + Positive Pressure Bias](#divergence--positive-pressure-bias)
- [Divergence + Fresh 50-Line Crossover](#divergence--fresh-50-line-crossover)
- [Confirmed + Opposite Current Zone](#confirmed--opposite-current-zone)
- [No Active Setup + Meaningful Context](#no-active-setup--meaningful-context)

$$----------$$

**How to Use:**
[What to Focus on First](#what-to-focus-on-first)

[A Simple Reading Sequence](#a-simple-reading-sequence)
- [Step 1 — Start with Signal](#step-1--start-with-signal)
- [Step 2 — Check Divergence](#step-2--check-divergence)
- [Step 3 — Check Classic Confirmation](#step-3--check-classic-confirmation)
- [Step 4 — Read Zone](#step-4--read-zone)
- [Step 5 — Read Pressure Bias](#step-5--read-pressure-bias)
- [Step 6 — Read Pressure Mix](#step-6--read-pressure-mix)
- [Step 7 — Use Rule as the Audit Trail](#step-7--use-rule-as-the-audit-trail)

[One-Screen Mental Model](#one-screen-mental-model)

---
## UO Heatmap Translation Cheat Sheets

Use these tables to translate what appears in the UO heatmap cell and hover into the **effective rule or condition that produced it**, the role that datapoint plays, and its plain-English meaning.

> "***The Rule / Condition column below shows the effective UO semantic rule. For simple fields, that is a direct numeric expression. For Divergence, Confirmation, and Signal states, it is necessarily a composite or lifecycle rule rather than a single raw-value expression.***"

The normalized rulebook routes already-computed UO semantic states into the five heatmap scores. The tables below expose the underlying logic that makes those state aliases meaningful.

---

### Cheat Sheet 1 — Heatmap Cell: What Am I Looking At?

| Cell element | Rule / Condition | Description | In 1-line |
| --- | --- | --- | --- |
| [UO Value](#the-uo-value) | [4:2:1 weighted blend](#the-421-weighting) of the Fast, Medium, and Slow pressure ratios | Current Ultimate Oscillator reading, normally expressed on a 0–100 scale | **“What is the current blended buying-pressure reading?”** |
| [Heatmap Background](#the-heatmap-background) | [Semantic state](#the-seven-semantic-states) → [five-level heatmap score](#five-heatmap-scores-from-seven-uo-states) | Shows the score projection of the active UO state: +2, +1, 0, -1, or -2 | **“How strongly is the current UO setup scored?”** |
| [▲ / ▼ 50-Line Crossover](#50-line-crossover-symbols) | ▲: :blue-background[prior UO <= 50 AND current UO > 50] <br> ▼: :blue-background[prior UO >= 50 AND current UO < 50] | Fresh current-session midpoint crossover; appears to the **left** of the value | **“Did UO just change sides of 50?”** |
| [◆ Divergence Diamond](#divergence-symbols) | Blue ◆ = active bullish divergence <br> Red ◆ = active bearish divergence | Marks an active qualifying confirmed-pivot divergence; appears to the **right** of the value | **“Is a divergence setup currently active and unresolved?”** |

**Important:** the value, background, triangle, and diamond are separate pieces of information. They should not be treated as four votes that must agree directionally.

---

### Cheat Sheet 2 — Signal & Heatmap Score Translation

This is the primary **rule-to-Signal translation** table.

| Semantic state | [Signal](#signal) shown in hover | Effective rule / condition | Heatmap score | Description | In 1-line |
| --- | --- | --- | :---: | --- | --- |
| [Bullish Confirmed](#bullish-confirmed-signal) | [Bullish Confirmed](#bullish-confirmed-signal) | Qualifying bullish divergence **AND** :blue-background[current UO > bullish Confirmation Trigger] **AND** confirmation occurs within :blue-background[Event lag 0–10 inclusive] | +2 | Highest-priority bullish staged-reversal event; confirmation is event-day only | **“The bullish divergence completed its required confirmation step in time.”** |
| [Bullish Watch](#bullish-watch-signal) | [Bullish Setup (Watch)](#bullish-watch-signal) | Fast: :blue-background[UO < 30] <br> Medium/Slow: :blue-background[UO < 35] <br> **AND no higher-priority Divergence or Confirmed state is active** | +1 | Current UO is in its bullish extreme zone, but the setup has not progressed to a higher stage | **“UO is oversold enough to watch for a bullish reversal setup.”** |
| [Bullish Divergence](#bullish-divergence-signal) | [Bullish Setup (Divergence)](#bullish-divergence-signal) | :blue-background[current confirmed price pivot low < prior confirmed price pivot low] **AND** :blue-background[current UO pivot low > prior UO pivot low] **AND** qualifying oversold involvement **AND** setup remains unresolved | +1 | Qualifying bullish confirmed-pivot disagreement awaiting confirmation | **“Price made a lower low, but UO made a higher low; confirmation is still pending.”** |
| [No Active Setup](#no-active-setup-signal) | [No Active Setup](#no-active-setup-signal) | No Confirmed, Divergence, or Watch setup currently has precedence | 0 | Valid UO observation with no active staged-reversal setup | **“There is no active UO reversal setup right now.”** |
| [Bearish Watch](#bearish-watch-signal) | [Bearish Setup (Watch)](#bearish-watch-signal) | :blue-background[UO > 70] **AND no higher-priority Divergence or Confirmed state is active** | -1 | Current UO is in its bearish extreme zone, but the setup has not progressed to a higher stage | **“UO is overbought enough to watch for a bearish reversal setup.”** |
| [Bearish Divergence](#bearish-divergence-signal) | [Bearish Setup (Divergence)](#bearish-divergence-signal) | :blue-background[current confirmed price pivot high > prior confirmed price pivot high] **AND** :blue-background[current UO pivot high < prior UO pivot high] **AND** qualifying overbought involvement **AND** setup remains unresolved | -1 | Qualifying bearish confirmed-pivot disagreement awaiting confirmation | **“Price made a higher high, but UO made a lower high; confirmation is still pending.”** |
| [Bearish Confirmed](#bearish-confirmed-signal) | [Bearish Confirmed](#bearish-confirmed-signal) | Qualifying bearish divergence **AND** :blue-background[current UO < bearish Confirmation Trigger] **AND** confirmation occurs within :blue-background[Event lag 0–10 inclusive] | -2 | Highest-priority bearish staged-reversal event; confirmation is event-day only | **“The bearish divergence completed its required confirmation step in time.”** |

#### Rulebook Routing vs. Effective UO Rules

The normalized rulebook uses the following aliases to route the already-computed UO states into the standard five heatmap scores:

| Heatmap route | Rulebook alias | UO states represented |
| --- | --- | --- |
| Strong Buy / +2 | UO_BULLISH_CONFIRMED | [Bullish Confirmed](#bullish-confirmed-signal) |
| Buy / +1 | UO_BULLISH_SETUP | [Bullish Watch](#bullish-watch-signal) **or** [Bullish Divergence](#bullish-divergence-signal) |
| Neutral / 0 | UO_NO_ACTIVE_SETUP | [No Active Setup](#no-active-setup-signal) |
| Sell / -1 | UO_BEARISH_SETUP | [Bearish Watch](#bearish-watch-signal) **or** [Bearish Divergence](#bearish-divergence-signal) |
| Strong Sell / -2 | UO_BEARISH_CONFIRMED | [Bearish Confirmed](#bearish-confirmed-signal) |

These aliases are **score-routing inputs**, not complete human-readable definitions of how the state was created.

For example:
:blue-background[UO_BULLISH_CONFIRMED] is useful to the classifier, but the effective semantic rule is:

> **qualifying bullish divergence + strict break above its Classic Confirmation Trigger within the permitted confirmation window.**

Similarly:
:blue-background[UO_BULLISH_SETUP] does not by itself tell the reader whether the active +1 state is:

- [Bullish Watch](#bullish-watch-signal); or
- [Bullish Divergence](#bullish-divergence-signal).

That distinction is preserved in the [Signal](#signal) shown in the hover.

This is why the cheat sheets use the **effective semantic rule** rather than stopping at the rulebook alias.

---
### Cheat Sheet 3 — Zone, Pressure Bias & Pressure Mix: Current Context

These fields describe the **current oscillator context** (current-context fields). They do not override the staged-reversal Signal.

| Hover field | Outcome | Rule / Condition | Description | In 1-line |
| --- | --- | --- | --- | --- |
| [Zone](#zone) | [Oversold](#oversold) | Fast: :blue-background[UO < 30] <br> Medium/Slow: :blue-background[UO < 35] | Current UO is below the active variant's bullish Watch threshold | **“UO is currently in its downside extreme zone.”** |
| [Zone](#zone) | [Overbought](#overbought) | All variants: :blue-background[UO > 70] | Current UO is above the bearish Watch threshold | **“UO is currently in its upside extreme zone.”** |
| [Zone](#zone) | [Neither Extreme](#neither-extreme) | Fast: :blue-background[30 <= UO <= 70] <br> Medium/Slow: :blue-background[35 <= UO <= 70] | Current UO is outside both Watch zones | **“UO is not currently inside either extreme zone.”** |

| Hover field | Outcome | Rule / Condition | Description | In 1-line |
| --- | --- | --- | --- | --- |
| [Pressure Bias](#pressure-bias) | [Positive](#positive-pressure-bias) | :blue-background[UO > 50] | Current blended UO is above its midpoint | **“Current UO pressure is on the stronger side of 50.”** |
| [Pressure Bias](#pressure-bias) | [Negative](#negative-pressure-bias) | :blue-background[UO < 50] | Current blended UO is below its midpoint | **“Current UO pressure is on the weaker side of 50.”** |
| [Pressure Bias](#pressure-bias) | [Balanced](#balanced-pressure-bias) | :blue-background[UO = 50] | Current blended UO is exactly at its midpoint | **“UO is sitting exactly at 50.”** |

| Hover field                       | Outcome                                                         | Rule / Condition                                                                          | Description                                                                          | In 1-line                                                        |
| --------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| [Pressure Mix](#pressure-mix-101) | [recent pressure strengthening](#recent-pressure-strengthening) | :blue-background[Fast > Medium > Slow]                                                    | Shorter-horizon buying pressure is stronger than each broader horizon                | **“Recent pressure is leading the broader pressure structure.”** |
| [Pressure Mix](#pressure-mix-101) | [recent pressure weakening](#recent-pressure-weakening)         | :blue-background[Fast < Medium < Slow]                                                    | Shorter-horizon buying pressure is weaker than each broader horizon                  | **“Recent pressure is lagging the broader pressure structure.”** |
| [Pressure Mix](#pressure-mix-101) | [mixed / transitional](#mixed--transitional)                    | Neither :blue-background[Fast > Medium > Slow] nor :blue-background[Fast < Medium < Slow] | The three horizons do not form a clean monotonic strengthening or weakening sequence | **“Pressure is mixed across horizons or may be transitioning.”** |


**Pressure Mix reminder:** the classification uses the **current Fast / Medium / Slow ordering**. The day-to-day changes shown beside those components answer a different question.


### Cheat Sheet 4 — Divergence Outcome Translation

| [Divergence](#divergence-101) outcome | Effective rule / condition | Supporting display | Description | In 1-line |
| --- | --- | --- | --- | --- |
| [None](#none) | No active qualifying divergence is being displayed on this observation | No divergence diamond | May mean no qualifying divergence formed, a prior setup confirmed, a prior setup expired, or the observation is only at Watch / No Active Setup | **“There is no unresolved divergence being displayed right now.”** |
| [Active - Bullish](#active---bullish-bullish-divergence) | :blue-background[current confirmed price pivot low < prior confirmed price pivot low] **AND** :blue-background[current UO pivot low > prior UO pivot low] **AND** at least one of the two UO pivot lows satisfies the bullish qualifying-extreme threshold | Blue ◆ plus [Prior](#prior), [Current](#current), and [Event](#event) | Qualifying bullish confirmed-pivot disagreement; setup remains active until confirmation or expiry | **“Price made a lower low while UO made a higher low.”** |
| [Active - Bearish](#active---bearish-bearish-divergence) | :blue-background[current confirmed price pivot high > prior confirmed price pivot high] **AND** :blue-background[current UO pivot high < prior UO pivot high] **AND** at least one of the two UO pivot highs satisfies :blue-background[UO > 70] | Red ◆ plus [Prior](#prior), [Current](#current), and [Event](#event) | Qualifying bearish confirmed-pivot disagreement; setup remains active until confirmation or expiry | **“Price made a higher high while UO made a lower high.”** |

#### Qualifying-Extreme Requirement

For [bullish divergence](#active---bullish-bullish-divergence), at least one of the two UO pivot lows must satisfy:

- UO(5,10,15): :blue-background[UO < 30]
- UO(7,14,28): :blue-background[UO < 35]
- UO(10,20,40): :blue-background[UO < 35]

For [bearish divergence](#active---bearish-bearish-divergence), at least one of the two UO pivot highs must satisfy:

- all variants: :blue-background[UO > 70]

The **current** UO reading does not need to remain extreme after the divergence becomes active.

---

### Cheat Sheet 5 — Classic Confirmation Outcome Translation

| [Classic Confirmation](#classic-confirmation-101) outcome | Effective rule / condition | Supporting fields | Description | In 1-line |
| --- | --- | --- | --- | --- |
| [None](#none-1) | No applicable active confirmation status is being displayed on this observation | — | Typically no divergence is awaiting resolution and no confirmation / expiry event is being reported | **“There is no Classic Confirmation process to report on this row.”** |
| [Pending](#pending) | Qualifying divergence is active **AND** its trigger has not been strictly crossed **AND** the confirmation window is still open | [Trigger](#understanding-the-trigger), [Sessions Remaining](#understanding-sessions-remaining) | Divergence exists and is still waiting for its required UO trigger | **“The setup exists, but the required confirmation trigger has not fired yet.”** |
| [Bullish Confirmed](#bullish-confirmed) | :blue-background[current UO > bullish Confirmation Trigger] while the qualifying bullish divergence is still inside :blue-background[Event lag 0–10 inclusive] | [Trigger](#understanding-the-trigger), [Confirmation Event](#understanding-the-confirmation-event) | Bullish divergence completed Classic Confirmation; corresponding Signal is [Bullish Confirmed](#bullish-confirmed-signal) | **“The bullish divergence broke its required UO trigger in time.”** |
| [Bearish Confirmed](#bearish-confirmed) | :blue-background[current UO < bearish Confirmation Trigger] while the qualifying bearish divergence is still inside :blue-background[Event lag 0–10 inclusive] | [Trigger](#understanding-the-trigger), [Confirmation Event](#understanding-the-confirmation-event) | Bearish divergence completed Classic Confirmation; corresponding Signal is [Bearish Confirmed](#bearish-confirmed-signal) | **“The bearish divergence broke its required UO trigger in time.”** |
| [Expired](#expired) | No strict trigger break occurred through :blue-background[Event lag 10]; the old setup becomes inactive before lag 11 | 10-bar window elapsed | Valid divergence failed to complete confirmation within the permitted window; its old trigger becomes stale | **“The setup was valid, but confirmation did not happen soon enough.”** |

**Same-day confirmation:** Event lag 0 is eligible. A divergence can therefore become knowable and confirm on the same session; Confirmed then outranks Divergence in the displayed Signal.

---

### Cheat Sheet 6 — Lifecycle Metadata: Prior, Current, Event & Trigger

These terms explain **how the app reconstructs the divergence and confirmation lifecycle**.

| Displayed term / concept | Rule / Definition | Description | In 1-line |
| --- | --- | --- | --- |
| [Pivot](#confirmed-five-bar-pivots) | Candidate swing + two sessions before + two sessions after | Confirmed five-bar swing point; it cannot be known on the pivot date because two future sessions are required | **“A swing point that has survived two later sessions of confirmation.”** |
| [Prior](#prior) / [Prior Pivot](#prior-pivot) | Earlier confirmed price pivot used in the divergence pair | Supplies the earlier pivot date, price, and UO value | **“The first swing point in the divergence comparison.”** |
| [Current](#current) / [Current Pivot](#current-pivot) | Newer confirmed price pivot used in the divergence pair | Supplies the newer pivot date, price, and UO value | **“The second swing point being compared with Prior.”** |
| [Qualifying Extreme](#the-qualifying-extreme-requirement) | At least one of the two UO pivots must enter the applicable bullish or bearish extreme zone | Prevents ordinary pivot disagreement from automatically becoming a staged UO divergence | **“At least one pivot must involve a meaningful UO extreme.”** |
| [Divergence Event](#divergence-event) | Normally :blue-background[Current Pivot + 2 trading sessions] | Date the newer five-bar pivot becomes knowable and the divergence can legitimately be emitted without future information | **“When the app can first know the divergence is real.”** |
| [Confirmation Trigger](#confirmation-trigger) | Bullish: highest UO from Prior through Current, inclusive <br> Bearish: lowest UO from Prior through Current, inclusive | Divergence-specific UO level that must be strictly broken | **“The UO level the setup must cross to become Confirmed.”** |
| [Confirmation Event](#confirmation-event) | Bullish: first valid :blue-background[UO > Trigger] <br> Bearish: first valid :blue-background[UO < Trigger] within the window | Session on which the divergence actually completes Classic Confirmation | **“The day the confirmation trigger actually fires.”** |
| [Confirmation Window](#the-10-session-confirmation-window) | :blue-background[Event lag 0 through Event lag 10, inclusive] | Bounded interval during which the divergence is eligible to confirm | **“The setup gets the Event day plus the next 10 trading sessions to confirm.”** |
| [Sessions Remaining](#understanding-sessions-remaining) | Remaining eligible sessions while Classic Confirmation is Pending | Countdown showing how much of the confirmation window remains | **“How much time the active divergence still has to confirm.”** |

#### Divergence Event vs Confirmation Event

| Event | What happened? | In 1-line |
| --- | --- | --- |
| [Divergence Event](#divergence-event) | The newer five-bar pivot became knowable, so the qualifying divergence could be emitted | **“The setup became knowable.”** |
| [Confirmation Event](#confirmation-event) | UO actually crossed the divergence-specific Confirmation Trigger | **“The setup triggered.”** |

The two dates can differ. They can also be the same.

---

### Cheat Sheet 7 — Generic & Supporting Hover Fields

The UO hover also contains several fields that are not themselves staged-reversal outcomes.

| Hover field | How it is derived / populated | Description | In 1-line |
| --- | --- | --- | --- |
| [Value](#the-uo-value) | Current UO reading for the selected variant | Current weighted oscillator value | **“Where is UO right now?”** |
| Δ vs prior day | :blue-background[current UO - prior-session UO], with relative % change when available | Shows how much the displayed UO value changed from the previous session | **“How much did UO move since yesterday?”** |
| Trend | Current UO compared with prior-session UO: Rising, Falling, or Flat | Direction of the one-session UO change | **“Is UO rising, falling, or unchanged versus the prior session?”** |
| [Zone](#zone) | Variant-specific extreme thresholds | Current oscillator location | **“Is UO currently oversold, overbought, or neither?”** |
| [Pressure Bias](#pressure-bias) | Current UO relative to 50 | Current midpoint context; may also carry a fresh ▲ / ▼ crossover marker | **“Which side of 50 is UO on?”** |
| [Pressure Mix](#pressure-mix-101) | Current Fast / Medium / Slow pressure ratios and their ordering | Internal multi-horizon buying-pressure structure | **“Is recent pressure leading or lagging the broader horizons?”** |
| [Divergence](#divergence-101) | Confirmed-pivot price/UO structure + qualifying extreme + lifecycle status | Shows whether an unresolved qualifying divergence is active | **“Has price and UO formed a qualifying disagreement?”** |
| [Classic Confirmation](#classic-confirmation-101) | Divergence-specific trigger + bounded confirmation window | Shows whether the divergence is waiting, confirmed, expired, or not applicable | **“Has the divergence actually triggered?”** |
| [Signal](#signal) | Highest-priority active semantic state under :blue-background[Confirmed > Divergence > Watch > No Active Setup] | User-facing summary of the staged-reversal state | **“What is the strongest active UO setup?”** |
| [Rule](#rule) | Dynamic text derived from the active UO semantic state | Explains why the displayed Signal was assigned | **“Why did the app give me this Signal?”** |
| Notes | Rule / implementation notes associated with the UO row | Additional context behind the rule framework | **“What extra rule context should I know?”** |
| Definition | Static UO definition for the selected variant | Explains what the indicator measures | **“What is UO measuring?”** |
| How to Read | Static interpretation guidance for the UO row | Short usage guide for Watch, divergence, confirmation, and symbols | **“How should I interpret this row?”** |

---

### One-Screen Mental Model

If you need the shortest possible translation sequence:

| Read this | Ask this |
| --- | --- |
| [Signal](#signal) | **“What is the strongest active UO state?”** |
| [Rule](#rule) | **“Why did it receive that state?”** |
| [Divergence](#divergence-101) | **“What pivot structure produced the setup?”** |
| [Classic Confirmation](#classic-confirmation-101) | **“Is that setup waiting, confirmed, expired, or absent?”** |
| [Zone](#zone) | **“Where is UO relative to its extreme thresholds right now?”** |
| [Pressure Bias](#pressure-bias) | **“Which side of 50 is UO on?”** |
| [Pressure Mix](#pressure-mix-101) | **“Is recent buying pressure leading or lagging the broader horizons?”** |

> "***Signal tells you the state. Rule tells you why. Divergence and Classic Confirmation tell you the lifecycle. Zone, Pressure Bias, and Pressure Mix tell you the current context.***"

See Also:
- [A Simple Reading Sequence](#a-simple-reading-sequence)
- [What to Focus on First](#what-to-focus-on-first)

---
## Ultimate Oscillator — At a Glance

The Ultimate Oscillator, or UO, is a momentum oscillator designed to measure :blue[buying pressure across three different time horizons at the same time].

Instead of asking only:

> *'Is momentum strong or weak right now?'*

UO asks a more useful multi-horizon question:
> "***Is recent buying pressure strengthening or weakening relative to the market's medium- and longer-term pressure?***"

The indicator combines [three measurements](#fast-medium-and-slow-pressure) of [buying pressure](#buying-pressure):
- a :blue[Fast] component;
- a :blue[Medium] component;
- a :blue[Slow] component.

Those three components are blended into one UO value on a scale that normally runs from 0 to 100.

The Fast component receives the greatest weight, the Medium component receives less, and the Slow component receives the least:
- :blue-background[4 : 2 : 1]

This makes UO more responsive to recent changes while still retaining information from broader pressure conditions.

The app goes beyond displaying the raw UO value. It uses UO as a :blue-background[staged reversal framework] that asks three progressively stronger questions:
1. Has UO reached a meaningful extreme?
2. Is price making a new swing extreme while UO fails to confirm it?
3. Has UO subsequently broken its Classic Confirmation level?

In simplified form:
```text
  Extreme
     ↓
Divergence
     ↓
Confirmation
```

The app expresses those stages through seven UO [semantic states](#semantic-state).

### What UO Is Designed to Show

UO is primarily used in this app to identify :blue[potential reversal structures], not simply to classify whether momentum is currently above or below a midpoint.

It provides several distinct layers of information:

| UO layer | Main question |
| --- | --- |
| [Zone](#zone) | Is UO currently in an unusually weak or strong pressure zone? |
| [Pressure Bias](#pressure-bias) | Is the blended UO value currently above, below, or exactly at its 50 midpoint? |
| [Pressure Mix](#pressure-mix) | Is recent pressure stronger or weaker than the medium- and longer-horizon pressure underneath it? |
| [Divergence](#divergence) | Is price making a new confirmed swing extreme while UO is moving in the opposite direction? |
| [Classic Confirmation](#classic-confirmation) | Has UO broken the level required to confirm the divergence structure? |
| [Signal](#signal) | What is the strongest currently active UO reversal state? |
| [Rule](#rule) | Why did the app assign that Signal? |

These fields are related, but they do :red[not] all answer the same question.

For example:
- Zone describes the :blue[current UO location].
- Pressure Mix describes the :blue[relationship among the three pressure horizons].
- Divergence compares :blue[price structure with UO structure].
- Classic Confirmation asks whether the divergence has actually triggered.
- Signal summarizes the :blue[highest-priority active reversal state].

Because the fields describe different dimensions of the same setup, they do not need to agree directionally at every moment.

A stock can legitimately show, for example:
- **Zone**: [Overbought](#overbought)
- **Signal**: [Bullish Confirmed](#bullish-confirmed)

That does not automatically indicate an error.

The "*Zone*" describes where UO is **now**, while "*Bullish Confirmed*" describes a qualifying reversal structure that developed earlier and subsequently reached its confirmation trigger.

The relationship between these fields is explained in detail under [The Staged Reversal Framework](#the-staged-reversal-framework).

### The Seven UO Signal States

The app recognizes seven distinct UO semantic states.

These are the actual UO concepts underneath the five [heatmap score](#heatmap-score) levels.

| UO state | User-facing Signal | Heatmap score | Simplest interpretation |
| --- | --- | :---: | --- |
| :blue-background[Bullish Confirmed] | [Bullish Confirmed](#bullish-confirmed) | +2 | A qualifying bullish divergence has broken above its Classic Confirmation trigger within the allowed [confirmation window](#confirmation-window). |
| :blue-background[Bullish Divergence] | [Bullish Setup (Divergence)](#bullish-divergence-signal) | +1 | Price made a lower confirmed low while UO made a higher corresponding low, with the required oversold involvement. Confirmation is still pending. |
| :blue-background[Bullish Watch] | [Bullish Setup (Watch)](#bullish-watch-signal) | +1 | UO is currently inside the variant’s oversold Watch zone, but no higher-priority bullish setup is active. |
| No Active Setup | [No Active Setup](#no-active-setup) | 0 | No active Watch, Divergence, or Confirmed UO reversal setup is present. |
| :red-background[Bearish Watch] | [Bearish Setup (Watch)](#bearish-watch-signal) | -1 | UO is currently inside the overbought Watch zone, but no higher-priority bearish setup is active. |
| :red-background[Bearish Divergence] | [Bearish Setup (Divergence)](#bearish-divergence-signal) | -1 | Price made a higher confirmed high while UO made a lower corresponding high, with the required overbought involvement. Confirmation is still pending. |
| :red-background[Bearish Confirmed] | [Bearish Confirmed](#bearish-confirmed) | -2 | A qualifying bearish divergence has broken below its Classic Confirmation trigger within the allowed confirmation window. |

The distinction between '[Watch](#watch)' and '[Divergence](#divergence)' is important even though both map to the same $\small{\fcolorbox{none}{lightgreen}{\textsf{+1}}}$ or $\small{\fcolorbox{none}{pink}{\textsf{-1}}}$ [heatmap score](#heatmap-score).


'Watch' means:
- "***UO is currently [extreme](#qualifying-extreme) enough to deserve attention.***"
- It's saying: **An [extreme](#the-qualifying-extreme-requirement) exists.**

'Divergence' means:
- "***Price and UO have formed a [qualifying](#the-qualifying-extreme-requirement) [confirmed](#confirmed)-[pivot](#pivot) disagreement that is now awaiting confirmation***"
- It's saying: **An [extreme](#the-qualifying-extreme-requirement) participated in a confirmed-[pivot](#pivot) price/UO disagreement.**

'Confirmed' means:
- "***That qualifying divergence has subsequently crossed its [Classic Confirmation trigger](#confirmation-trigger)***".
- It's saying: **That [divergence](#divergence) also crossed its required [confirmation trigger](#confirmation-trigger) in time.**


The score becomes stronger only at the Confirmed stage.

More detail: [Signal and Rule](#signal-and-rule)

### Heatmap Symbols at a Glance

The UO heatmap can add symbols to the displayed UO value.

These symbols represent :blue[event/context information] and should be read separately from the background score.

| Symbol | Meaning |
| --- | --- |
| $\large{\textcolor{blue}{\textsf{▲}}}$ | UO crossed :blue[above 50] during the current session. |
| $\large{\textcolor{Red}{\textsf{▼}}}$ | UO crossed :red[below 50] during the current session. |
| $\large{\textcolor{blue}{\textsf{◆}}}$ | A :blue[bullish divergence] is currently active. |
| $\large{\textcolor{red}{\textsf{◆}}}$ | A :red[bearish divergence] is currently active. |

- The [crossover symbol](#50-line-crossover-symbols) appears to the :blue[left] of the UO value.
- The [divergence diamond](#divergence-symbols) appears to the :blue[right] of the value.

That allows both to appear together.

For example: $\large{\textcolor{blue}{\textsf{▲}}}$ 50.3 $\large{\textcolor{blue}{\textsf{◆}}}$

means:
- UO crossed above 50 during the current session; and
- a bullish divergence remains active.

Those are two separate pieces of information.
- The triangle describes a :red-background[current-session midpoint crossover].
- The diamond describes an :red-background[active confirmed-pivot divergence structure].

Neither symbol replaces the Signal or heatmap background.

More detail:

- [Pressure Bias and the 50-Line Crossover](#pressure-bias-and-the-50-line-crossover)
- [Divergence](#divergence)

### The Simplest Way to Think About UO

A useful way to read UO in this app is:

:blue-background[Zone]: *"Where is UO right now?"*

                    ↓

:blue-background[Pressure Bias]: *"Which side of the 50 midpoint currently has the advantage?"*

                    ↓

:blue-background[Pressure Mix]: *"Is recent pressure stronger or weaker than the broader pressure underneath it?"*

                    ↓

:blue-background[Divergence]: *"Is price making a new swing extreme that UO is failing to confirm?"*

                    ↓

:blue-background[Classic Confirmation]: *"Has that divergence actually triggered?"*

                    ↓

:blue-background[Signal]: *"What is the strongest active UO reversal state?"*

This is why UO should not be interpreted as a simple:
> Low number = Buy
> High number = Sell

framework.

The raw UO value matters, but the app deliberately asks a more structured question:

> ***Has pressure become extreme, has price/UO behavior begun to diverge, and has that divergence subsequently [confirmed](#confirmed)?***

That sequence is the foundation for the rest of the UO documentation.

See also:

- [Reading the UO Heatmap](#reading-the-uo-heatmap)
- [The Staged Reversal Framework](#the-staged-reversal-framework)


---
## Reading the UO Heatmap
[Top](#ultimate-oscillator-at-a-glance)

This section focuses only on the UO-specific information a user sees in the heatmap cell and hover.

The goal is to answer:
- "***What is the heatmap showing me right now, and which parts describe the current UO reading versus the active reversal setup?***"

### Understanding the Cell

A UO heatmap cell can contain several pieces of information at once:
- the [current UO value](#the-uo-value);
- the [heatmap background score](#the-heatmap-background);
- a [50-line crossover symbol](#50-line-crossover-symbols);
- a [divergence diamond](#divergence-symbols).

These are related, but they do **not** all describe the same thing.

A useful way to separate them is:

| Cell element | What it tells you |
| --- | --- |
| UO number | The current blended Ultimate Oscillator reading |
| Background color | The current five-level heatmap score |
| $\large{\textcolor{blue}{\textsf{▲}}}$ / $\large{\textcolor{Red}{\textsf{▼}}}$ | A fresh current-session cross of the 50 line |
| $\large{\textcolor{blue}{\textsf{◆}}}$ / $\large{\textcolor{red}{\textsf{◆}}}$ | An active confirmed-pivot divergence |

The key point is:
- "***The value, background, triangle, and diamond are separate pieces of information. They should not be interpreted as four independent votes that must all point in the same direction.***"

#### The UO Value

The number shown in the cell is the current UO reading.

UO normally ranges from 0 to 100.
- A lower value means the blended buying-pressure ratio is weaker.
- A higher value means the blended buying-pressure ratio is stronger.

The current value alone does **not** determine the entire UO Signal.

For example, a value may no longer be inside an oversold zone even though a previously established bullish divergence is still active.

See also:
- [How UO Is Calculated](#how-uo-is-calculated)
- [Common UO Combinations](#common-uo-combinations)
- [Zone and Watch](#zone-and-watch)
- [The Staged Reversal Framework](#the-staged-reversal-framework)


#### The Heatmap Background

The background color reflects the five-level [heatmap score](#heatmap-score):

| Score | UO meaning |
| :---: | --- |
| +2 | [Bullish Confirmed](#bullish-confirmed) |
| +1 | [Bullish Watch](#bullish-watch-signal) or [Bullish Divergence](#active---bullish-bullish-divergence) |
| 0 | [No Active Setup](#no-active-setup-signal) |
| -1 | [Bearish Watch](#bearish-watch-signal) or [Bearish Divergence](#bearish-divergence-signal) |
| -2 | [Bearish Confirmed](#bearish-confirmed-signal) |

The background therefore shows the **score projection**, not the full seven-state UO vocabulary.

This matters because two different [semantic states](#semantic-state) can share the same heatmap color.

For example:

[Bullish Setup (Watch)](#bullish-watch-signal) AND [Bullish Setup (Divergence)](#bullish-divergence-signal) both map to $\small{\fcolorbox{none}{lightgreen}{\textsf{+1}}}$.

The hover [Signal](#signal) field tells you which one is actually active.

See also:

- [Signal and Rule](#signal-and-rule)

#### 50-Line Crossover Symbols

A triangle marks a **current-session crossover of the UO 50 line**.

| Symbol | Meaning |
| --- | --- |
| $\large{\textcolor{blue}{\textsf{▲}}}$ | UO crossed above 50 during the current session |
| $\large{\textcolor{Red}{\textsf{▼}}}$ | UO crossed below 50 during the current session |

The crossover symbol appears to the **left** of the UO value.

Examples:

$\large{\textcolor{blue}{\textsf{▲}}}$ 52.8 means:
> :gray-background[UO was at or below 50 on the prior session and is now above 50.]

$\large{\textcolor{Red}{\textsf{▼}}}$ 47.6 means:
> :gray-background[UO was at or above 50 on the prior session and is now below 50.]

The symbol is event-specific.
- If UO remains above 50 on the next session without another crossover, the blue triangle does not repeat merely because Pressure Bias remains Positive.

See also:
- [Pressure Bias and the 50-Line Crossover](#pressure-bias-and-the-50-line-crossover)

#### Divergence Symbols

A diamond marks an **active UO divergence**.

| Symbol | Meaning |
| --- | --- |
| $\large{\textcolor{blue}{\textsf{◆}}}$ | Active bullish divergence |
| $\large{\textcolor{red}{\textsf{◆}}}$ | Active bearish divergence |

The divergence diamond appears to the **right** of the UO value.

Examples:

48.2 $\large{\textcolor{blue}{\textsf{◆}}}$ means:

> :gray-background[A qualifying bullish divergence is active and awaiting either confirmation or expiry.]

61.7 $\large{\textcolor{red}{\textsf{◆}}}$ means:
> :gray-background[A qualifying bearish divergence is active and awaiting either confirmation or expiry.]

The diamond identifies the divergence lifecycle state.

It does **not** mean that price must reverse.

See also:
- [Divergence](#divergence)
- [Classic Confirmation](#classic-confirmation)
- [Why Expiry Matters](#why-expiry-matters)

#### When More Than One Visual Cue Appears

A crossover symbol and divergence diamond can appear on the same cell.

For example:

$\large{\textcolor{blue}{\textsf{▲}}}$ 50.3 $\large{\textcolor{blue}{\textsf{◆}}}$

means two things happened to be true at the same time:

1. UO crossed above 50 during the current session.
2. A bullish divergence is still active.

Those two observations are related to UO, but they answer different questions.

The triangle asks:
> "***Did UO just cross its midpoint?***"

The diamond asks:
> "***Is a confirmed-pivot divergence currently active?***"

Neither one replaces the Signal.

The Signal still determines the active staged-reversal state.

---

### Understanding the Hover

The UO hover contains several UO-specific fields.

They appear in this order:

1. [Zone](#zone)
2. [Pressure Bias](#pressure-bias)
3. [Pressure Mix](#pressure-mix)
4. [Divergence](#divergence)
5. [Classic Confirmation](#classic-confirmation)
6. [Signal](#signal)
7. [Rule](#rule)

Each field answers a different question.

| Hover field | Main question |
| --- | --- |
| [Zone](#zone) | Is UO currently in a meaningful extreme zone? |
| [Pressure Bias](#pressure-bias) | Is blended UO currently above, below, or exactly at 50? |
| [Pressure Mix](#pressure-mix) | Is recent pressure stronger or weaker than the broader pressure underneath it? |
| [Divergence](#divergence) | Has price formed a qualifying swing extreme that UO did not confirm? |
| [Classic Confirmation](#classic-confirmation) | Has the divergence broken its confirmation trigger? |
| [Signal](#signal) | What is the strongest currently active UO reversal state? |
| [Rule](#rule) | Why did the app assign that Signal? |

The easiest way to read the hover is:

> "***Location → Bias → Pressure structure → Divergence → Confirmation → Signal → Why***"

That sequence mirrors the way the UO model is intended to be interpreted.

### What Each UO-Specific Field Answers

#### Zone
:violet-background[Zone] describes the current UO location relative to the active variant's extreme thresholds.

Zone answers:
> "***Where is UO relative to the variant's extreme thresholds right now?***"

Possible outcomes:
- [Oversold](#oversold)
- [Overbought](#overbought)
- [Neither Extreme](#neither-extreme)

Note: Zone does not by itself determine the active [Signal](#signal).

See [Zone and Watch](#zone-and-watch).

#### Pressure Bias

Pressure Bias answers:
> "***Is the blended UO value currently above, below, or exactly at the 50 midpoint?***"

Possible outcomes:
- [Positive](#positive-pressure-bias): :blue-background[UO > 50]
- [Negative](#negative-pressure-bias): :blue-background[UO < 50]
- [Balanced](#balanced-pressure-bias): :blue-background[UO = 50]

A fresh crossover may also append:

$\large{\textcolor{blue}{\textsf{▲}}}$ or $\large{\textcolor{Red}{\textsf{▼}}}$

**Note**: Pressure Bias is contextual and does not directly determine the UO score.

See [Pressure Bias and the 50-Line Crossover](#pressure-bias-and-the-50-line-crossover).

#### Pressure Mix
:violet-background[Pressure Mix] shows the current relationship among the Fast, Medium, and Slow buying-pressure ratios.

Pressure Mix answers:
> "***Which pressure horizon is leading, and is recent pressure stronger or weaker than the broader pressure structure?***"

Possible classification outcomes:
- [recent pressure strengthening](#recent-pressure-strengthening)
- [recent pressure weakening](#recent-pressure-weakening)
- [mixed / transitional](#mixed--transitional)

The classification is based on the **current cross-horizon ordering**, not on the day-to-day component changes.

See [Pressure Mix 101](#pressure-mix-101).

#### Divergence
Divergence answers:
> "***Has price made a [qualifying confirmed swing extreme](#qualifying-extreme) while UO moved in the opposite direction? IOW, that UO failed to confirm that move.***"

'Divergence' means:
- "**Price and UO have formed a [qualifying](#the-qualifying-extreme-requirement) confirmed-[pivot](#pivot) disagreement that is now awaiting confirmation**"
- It tells you whether price and UO have formed a qualifying **confirmed-pivot disagreement**.
- It's saying: **An [extreme](#the-qualifying-extreme-requirement) participated in a confirmed-[pivot](#pivot) price/UO disagreement.**

A divergence is a setup awaiting [confirmation](#confirmed), not a guaranteed reversal.

Possible outcomes:
- [None](#none)
- [Active - Bullish](#active---bullish-bullish-divergence)
    - :blue-background[current price pivot low < prior price pivot low] AND :blue-background[current UO pivot low > prior UO pivot low] with qualifying oversold involvement.
- [Active - Bearish](#active---bearish-bearish-divergence)
    - :blue-background[current price pivot high > prior price pivot high] AND :blue-background[current UO pivot high < prior UO pivot high] with qualifying overbought involvement.

When active, the hover also shows:
- [Prior](#prior)
- [Current](#current)
- [Event](#event)


See [Divergence 101](#divergence-101), [Divergence Event](#divergence-event).


#### Classic Confirmation
Classic Confirmation asks whether UO broke the divergence-specific [confirmation trigger](#confirmation-trigger) within the permitted [window](#the-10-session-confirmation-window).

Classic Confirmation answers:
> "***Has the active divergence actually crossed the UO [trigger](#confirmation-trigger) required for confirmation?***"

The third and strongest stage of the UO reversal framework.

**[Possible outcomes](#classic-confirmation-outcomes)**:
- [None](#none-1)
- [Pending](#pending)
- [Bullish Confirmed](#bullish-confirmed)
- [Bearish Confirmed](#bearish-confirmed)
- [Expired](#expired)

Depending on the outcome, the hover may also show:
- [Trigger](#understanding-the-trigger)
- [Event](#event)
- [sessions remaining](#understanding-sessions-remaining)

See [Classic Confirmation 101](#classic-confirmation-101).


#### Signal
:violet-background[Signal] is the user-facing label for the **highest-priority active UO [semantic state](#semantic-state)**.

Signal answers:
> "***What is the strongest currently active UO staged-reversal state?***"

Possible outcomes:
- [Bullish Setup (Watch)](#bullish-watch-signal)
- [Bullish Setup (Divergence)](#bullish-divergence-signal)
- [Bullish Confirmed](#bullish-confirmed-signal)
- [No Active Setup](#no-active-setup-signal)
- [Bearish Setup (Watch)](#bearish-watch-signal)
- [Bearish Setup (Divergence)](#bearish-divergence-signal)
- [Bearish Confirmed](#bearish-confirmed-signal)

See [Signal and Rule](#signal-and-rule).


##### Watch
This is the first stage of the UO reversal framework.

'Watch' is saying the **UO is currently extreme enough to deserve attention**, that an [extreme](#the-qualifying-extreme-requirement) exists.

A Watch means the **current UO value is inside the applicable extreme zone**, but no higher-priority Divergence or Confirmed state is active.

[Bullish Watch](#bullish-watch-signal) rules:
- UO(5,10,15): :blue-background[UO < 30]
- UO(7,14,28): :blue-background[UO < 35]
- UO(10,20,40): :blue-background[UO < 35]

Bearish Watch rule:
- all variants: :blue-background[UO > 70]



See also: [Zone and Watch](#zone-and-watch) and [Stage 1 — Watch](#stage-1--watch).



#### Rule

:violet-background[Rule] is the dynamic explanation of why the current Signal was assigned.

Rule answers:
> "***Why did the app assign this Signal?***"

IOW, **"*Signal* states the result. *Rule* states the reason."**


Unlike a generic static rule description, the UO Rule field changes with the active semantic state.

For example:
- 'Bullish Setup (Watch)' may display a [threshold-based](#watch-thresholds) Rule.
- 'Bullish Setup (Divergence)' explains the lower price low + higher UO pivot low structure and qualifying oversold involvement.
- 'Bullish Confirmed' explains that a qualifying bullish divergence subsequently broke above its Classic Confirmation trigger within the allowed window.


Other examples include:
- threshold logic for Watch;
- price/UO pivot structure for Divergence;
- trigger-break logic for Confirmed;
- no active staged setup for No Active Setup.

See [Signal and Rule](#signal-and-rule).

---

## UO Hover Field Reference
[Top](#ultimate-oscillator-at-a-glance)

### Zone and Watch

Zone describes the **current UO location relative to the active variant's extreme thresholds**.

Watch is the staged-reversal state that can arise from that current extreme.

The two concepts are closely related, but they are not identical:

> "***Zone describes where UO is now. Watch describes whether that current extreme is the highest-priority active UO setup.***"

#### Zone Outcomes

##### Oversold
$\small{\textsf{Scope: Zone Outcomes}}$

Oversold means the current UO value is below the bullish Watch threshold for that UO variant.

The thresholds are:

| UO variant | Oversold / Bullish Watch threshold |
| --- | ---: |
| UO(5,10,15) | UO < 30 |
| UO(7,14,28) | UO < 35 |
| UO(10,20,40) | UO < 35 |

Example:

:gray-background[UO(7,14,28) = 32.4] produces: :gray-background[Zone: Oversold]

If no higher-priority bullish Divergence or Confirmed state is active, this can produce: :gray-background[Signal: Bullish Setup (Watch)]

The correct interpretation is:

> "***UO is currently weak enough to enter the project's bullish reversal-watch zone, but a qualifying divergence has not yet become the active setup.***"

Oversold does **not** mean that price has already bottomed.
- It means the oscillator has reached a downside extreme that deserves monitoring for further reversal evidence.

##### Overbought
$\small{\textsf{Scope: Zone Outcomes}}$

Overbought means the current UO value is above the bearish Watch threshold.

For all three UO variants: :blue-background[UO > 70] produces: :gray-background[Zone: Overbought]

If no higher-priority bearish Divergence or Confirmed state is active, this can produce: :gray-background[Signal: Bearish Setup (Watch)]

The correct interpretation is:
> "***UO is currently strong enough to enter the project's bearish reversal-watch zone, but a qualifying bearish divergence has not yet become the active setup.***"

Overbought does **not** mean that price has already topped.

It means the oscillator has reached an upside extreme that deserves monitoring for further reversal evidence.

##### Neither Extreme
$\small{\textsf{Scope: Zone Outcomes}}$

Neither Extreme means the current UO value is outside both [Watch](#watch) zones.
- For UO(5,10,15): :blue-background[30 <= UO <= 70]
- For UO(7,14,28) and UO(10,20,40): :blue-background[35 <= UO <= 70]

This means only:
> "***The current UO value is not inside either Watch threshold.***"

It does **not** automatically mean:
- No Active Setup;
- no divergence;
- no confirmation;
- no useful UO information.

A previously established divergence can remain active after UO leaves the extreme zone.

A confirmation can also occur while Zone is Neither Extreme.

That distinction is central to the staged model.

#### How Zone Relates to Watch

Watch is the first stage of the UO reversal framework.
- Bullish Watch requires the current UO value to be inside the oversold zone.
- Bearish Watch requires the current UO value to be inside the overbought zone.

But Watch has lower precedence than Divergence and Confirmation.

So:
- :violet-background[Zone]: :green-background[Oversold]

does **not** guarantee:
- :violet-background[Signal]: :green-background[Bullish Setup (Watch)]

if a higher-priority state is already active.

Likewise:
- :violet-background[Zone]: :green-background[Overbought]

does **not** guarantee:
- :violet-background[Signal]: :green-background[Bearish Setup (Watch)]


if an active Divergence or Confirmed state takes precedence.

#### Why Zone and Signal Can Differ

This is one of the most important UO concepts.

- [Zone](#zone) is a **current-value field**.
- [Signal](#signal) is a **staged-state field**.

Those two timelines are not always the same.

For example:

- :violet-background[Zone]: :green-background[Overbought]
- :violet-background[Signal]: :green-background[Bullish Confirmed]

may look contradictory at first.

It is not.

The interpretation is:

> "***UO is currently in an overbought zone, but the strongest active staged-reversal event is still a bullish confirmation that developed from an earlier qualifying bullish divergence.***"

The current Zone does not erase the historical setup that produced the Confirmed event.

Likewise:

- :violet-background[Zone]: Neither Extreme
- :violet-background[Signal]: Bullish Setup (Divergence)

means:

> "***UO is no longer currently oversold, but a qualifying bullish divergence was already established and remains active while confirmation is pending.***"

That is why Zone should be read as **current location**, not as the complete UO Signal.

See also:

- [The Staged Reversal Framework](#the-staged-reversal-framework)
- [Divergence](#divergence)
- [Classic Confirmation](#classic-confirmation)

---
### Pressure Bias and the 50-Line Crossover

:violet-background[Pressure Bias] describes which side of the UO 50 midpoint the **current blended oscillator value** occupies.

It answers:

> "***Is the current UO reading on the stronger side of its range, the weaker side, or exactly balanced at the midpoint?***"

The 50 line is useful because it provides a simple directional reference for the blended UO value without replacing the staged-reversal model.

:violet-background[Pressure Bias] is **context only**. It does not, by itself, create or override a Watch, Divergence, Confirmed, or No Active Setup Signal.

A separate current-session crossover event may also be shown with a colored triangle.

---

#### Pressure Bias Outcomes

There are exactly three possible :violet-background[Pressure Bias] outcomes:

- :green-background[Positive]
- :green-background[Negative]
- :green-background[Balanced]

##### Positive Pressure Bias

:violet-background[Pressure Bias]: :green-background[Positive]

means:

:blue-background[UO > 50]

In plain English:

> "***The current blended UO reading is on the stronger side of its 0–100 range.***"

This says something about the **current level of UO**, not about whether a reversal setup is bullish or bearish.

For example:

- :violet-background[Pressure Bias]: :green-background[Positive]
- :violet-background[Signal]: :green-background[Bearish Setup (Divergence)]

is possible.

That combination means:

> "***UO is currently above 50, but a qualifying bearish price/UO divergence is the stronger staged-reversal state.***"

The two fields are answering different questions.

See also:

- [Divergence](#divergence)
- [Signal and Rule](#signal-and-rule)

##### Negative Pressure Bias

:violet-background[Pressure Bias]: :green-background[Negative]

means:

:blue-background[UO < 50]

In plain English:

> "***The current blended UO reading is on the weaker side of its 0–100 range.***"

Again, this is a current-level description rather than a reversal Signal.

For example:

- :violet-background[Pressure Bias]: :green-background[Negative]
- :violet-background[Signal]: :green-background[Bullish Setup (Divergence)]

is valid.

That means:

> "***UO is still below its midpoint, but a qualifying bullish divergence has already formed and remains the stronger staged-reversal state.***"

##### Balanced Pressure Bias

:violet-background[Pressure Bias]: :green-background[Balanced] means: :blue-background[UO = 50]

In plain English:

> "***The current UO reading sits exactly at its midpoint.***"

This is a narrow condition.
- It does not mean that buying and selling pressure are perfectly balanced in every underlying component.

It means only that the final blended UO value equals 50.

A :green-background[Balanced] reading does not create a special heatmap score and does not cancel an existing staged-reversal setup.

---

#### 50-Line Crossover Events

The :violet-background[Pressure Bias] field may also display a symbol when UO crosses the 50 line during the current session.

There are two possible crossover events:

- :green-background[Cross Above 50]
- :green-background[Cross Below 50]

The hover expresses these events through the Pressure Bias line, while the heatmap cell displays the corresponding symbol.

##### Cross Above 50

A :green-background[Cross Above 50] event occurs when:
- :blue-background[prior UO <= 50] AND :blue-background[current UO > 50]

The heatmap cell displays:
- $\large{\textcolor{blue}{\textsf{▲}}}$

and the hover shows the current state as:
- :violet-background[Pressure Bias]: :green-background[Positive] $\large{\textcolor{blue}{\textsf{▲}}}$

In plain English:

> "***UO was at or below its midpoint on the prior session and has now moved above it.***"

This is a **fresh transition event**.

It is different from merely having:

:violet-background[Pressure Bias]: :green-background[Positive]

A Positive reading can persist for many sessions.

The blue triangle appears only on the session when the crossover condition itself occurs.

##### Cross Below 50

A :green-background[Cross Below 50] event occurs when:
- :blue-background[prior UO >= 50] AND :blue-background[current UO < 50]

The heatmap cell displays: $\large{\textcolor{Red}{\textsf{▼}}}$

and the hover shows: :violet-background[Pressure Bias]: :green-background[Negative] $\large{\textcolor{Red}{\textsf{▼}}}$

In plain English:

> "***UO was at or above its midpoint on the prior session and has now moved below it.***"

Like the bullish crossover, this is a **current-session transition event**, not a persistent state.

If UO remains below 50 on the following session, :violet-background[Pressure Bias] can remain :green-background[Negative], but the red triangle will not repeat unless another qualifying crossover occurs.

---

#### What the Crossover Symbol Means (State vs Event: An Important Distinction)

The easiest way to understand :violet-background[Pressure Bias] and the crossover symbol is:

| Information | Type | What it tells you |
| --- | --- | --- |
| :green-background[Positive] | State | UO is currently above 50 |
| :green-background[Negative] | State | UO is currently below 50 |
| :green-background[Balanced] | State | UO is currently exactly 50 |
| $\large{\textcolor{blue}{\textsf{▲}}}$ | Event | UO crossed above 50 this session |
| $\large{\textcolor{Red}{\textsf{▼}}}$ | Event | UO crossed below 50 this session |

So:

> "***Pressure Bias tells you where UO is now. The triangle tells you whether UO just changed sides.***"

This distinction matters because a persistent state and a fresh event have different informational value.

---

#### How to Use Pressure Bias

:violet-background[Pressure Bias] is most useful as **secondary context around the staged-reversal Signal**.

It can help answer questions such as:

- Is UO still below 50 while a bullish divergence is developing?
- Has UO moved above 50 while bullish confirmation is approaching?
- Is UO still above 50 while a bearish divergence is active?
- Did a fresh midpoint crossover occur on the same session as another UO event?

For example:

- :violet-background[Signal]: :green-background[Bullish Setup (Divergence)]
- :violet-background[Pressure Bias]: :green-background[Negative]

means the bullish setup exists, but blended UO has not yet moved above its midpoint.

If the next session becomes:

- :violet-background[Signal]: :green-background[Bullish Setup (Divergence)]
- :violet-background[Pressure Bias]: :green-background[Positive] $\large{\textcolor{blue}{\textsf{▲}}}$

then the divergence is still the active staged-reversal Signal, while the fresh 50-line crossover provides additional positive momentum context.

The crossover does **not** promote the setup to :green-background[Bullish Confirmed].

Only the defined [Classic Confirmation](#classic-confirmation) trigger can do that.

---

#### What Pressure Bias Does Not Do

:violet-background[Pressure Bias] does **not** directly determine the UO [heatmap score](#heatmap-score).

Specifically:

- :green-background[Positive] does not automatically mean Bullish.
- :green-background[Negative] does not automatically mean Bearish.
- $\large{\textcolor{blue}{\textsf{▲}}}$ does not automatically create :green-background[Bullish Confirmed].
- $\large{\textcolor{Red}{\textsf{▼}}}$ does not automatically create :green-background[Bearish Confirmed].
- A [50-line crossover](#50-line-crossover) does not replace the Extreme → Divergence → Confirmation framework.
- Pressure Bias does not override a higher-priority active Divergence or Confirmed state.

The core distinction is:

> "***Pressure Bias describes the current midpoint context. Signal describes the strongest active staged-reversal state.***"

See also:
- [The Staged Reversal Framework](#the-staged-reversal-framework)
- [Classic Confirmation](#classic-confirmation)
- [Signal and Rule](#signal-and-rule)
- Section:[Pressure Bias and the 50-line Crossover](#pressure-bias-and-the-50-line-crossover)

---
### Pressure Mix 101
[Section](#uo-hover-field-reference)


[Pressure Mix](#pressure-mix) shows the three buying-pressure ratios that feed the Ultimate Oscillator:
- :violet-background[Fast]
- :violet-background[Medium]
- :violet-background[Slow]

It answers:

> "***Is recent buying pressure stronger or weaker than the medium- and longer-horizon pressure underneath it?***"

The three values are not three separate UO Signals.

They are the underlying pressure components used to build the final blended UO value.

A typical hover line may look like:

:violet-background[Pressure Mix]: Fast 0.57 (+0.03, +5.6%) | Medium 0.50 (+0.01, +2.0%) | Slow 0.42 (-0.00, -0.5%)
- :green-background[recent pressure strengthening]

The first line shows the three current [pressure ratios](#pressure-ratio) and their changes from the prior session.

The second line interprets the **current relationship among the three horizons**.

That distinction is important.

---

#### What Fast, Medium, and Slow Represent

Each Pressure Mix component measures:

> "***Buying Pressure over its own horizon ÷ True Range over that same horizon.***"

- :red[True Range] measures the session’s effective price range while accounting for overnight gaps by comparing today’s high/low with the previous close. See [below](#true-range) for the full definition and formula.

The result is a ratio between 0 and 1 under normal conditions.
- A **higher ratio** means buying pressure occupied a larger share of the available trading range over that horizon.
- A **lower ratio** means buying pressure occupied a smaller share.

For a given UO variant:
- :violet-background[Fast] uses the shortest lookback.
- :violet-background[Medium] uses the middle lookback.
- :violet-background[Slow] uses the longest lookback.

For example, UO(7,14,28) uses:
- Fast = 7-session [pressure ratio](#pressure-ratio)
- Medium = 14-session pressure ratio
- Slow = 28-session pressure ratio

The final UO does not weight them equally.

Fast receives the greatest weight, followed by Medium, then Slow.

See [How UO Is Calculated](#how-uo-is-calculated) for the full BP/TR and 4:2:1 calculation.

---

#### Reading the Three Pressure Values

Suppose the hover shows:

:violet-background[Pressure Mix]: Fast 0.57 | Medium 0.50 | Slow 0.42

Read each value independently first:

:gray-background[Fast 0.57] means:
> Over the shortest UO horizon, buying pressure represented about 57% of the corresponding True Range total.

:gray-background[Medium 0.50] means:
> Over the medium UO horizon, buying pressure represented about 50% of the corresponding True Range total.

:gray-background[Slow 0.42] means:
> Over the longest UO horizon, buying pressure represented about 42% of the corresponding True Range total.

The next question is not merely whether those values are high or low.

It is:
> "***How are the three horizons ordered relative to one another right now?***"

That ordering determines the [Pressure Mix classification](#pressure-mix-outcomes).

---

#### Reading the Day-to-Day Changes

Each component may also show a parenthetical change from the prior session.

For example, :gray-background[Fast 0.57 (+0.03, +5.6%)] means:
- current Fast [pressure ratio](#pressure-ratio) = 0.57
- absolute change from the prior session = +0.03
- relative change from the prior session = +5.6%

The same interpretation applies to Medium and Slow.

These changes answer:

> "***Did this individual pressure component rise or fall since the prior session?***"

They do **not** determine whether the Pressure Mix is classified as strengthening, weakening, or mixed.

That classification comes from the current Fast / Medium / Slow ordering.

---

#### Pressure Mix Outcomes

There are exactly three :violet-background[Pressure Mix] classification outcomes:
- :green-background[recent pressure strengthening]
- :green-background[recent pressure weakening]
- :green-background[mixed / transitional]

##### Recent Pressure Strengthening

:violet-background[Pressure Mix]: :green-background[recent pressure strengthening]

occurs when: :red-background[Fast > Medium > Slow]

For example:
- Fast 0.57
- Medium 0.50
- Slow 0.42

Because: :gray-background[0.57 > 0.50 > 0.42]
- the most recent pressure is stronger than the medium-horizon pressure, which is itself stronger than the long-horizon pressure.

In plain English:

> "***The shorter the horizon, the stronger the buying-pressure ratio currently looks. Recent pressure is leading the broader pressure structure.***"

This can be useful evidence that buying pressure has improved more recently than the longer-horizon averages yet reflect.

It does **not** automatically create a bullish Signal.

##### Recent Pressure Weakening

:violet-background[Pressure Mix]: :green-background[recent pressure weakening]

occurs when: :red-background[Fast < Medium < Slow]

For example:
- Fast 0.35
- Medium 0.40
- Slow 0.46

Because: :gray-background[0.35 < 0.40 < 0.46]
- the most recent pressure is weaker than the medium-horizon pressure, which is itself weaker than the long-horizon pressure.

In plain English:

> "***The shorter the horizon, the weaker the buying-pressure ratio currently looks. Recent pressure is lagging the broader pressure structure.***"

This can indicate that more recent buying pressure has deteriorated relative to what is still embedded in the longer-horizon averages.

It does **not** automatically create a bearish Signal.

##### Mixed / Transitional
FYI: '*Mixed*' means neither monotonic ordering applies.

:violet-background[Pressure Mix]: :green-background[mixed / transitional] appears whenever the three current [pressure ratios](#pressure-ratio) are **not** strictly ordered in either direction:
- neither :gray-background[Fast > Medium > Slow] nor :gray-background[Fast < Medium < Slow]

Examples include:
- Fast 0.52
- Medium 0.47
- Slow 0.50

or:

- Fast 0.41
- Medium 0.46
- Slow 0.43

or equalities such as:
- Fast 0.48
- Medium 0.48
- Slow 0.44

In plain English:

> "***The three horizons do not form a clean strengthening or weakening sequence. Pressure is mixed across time horizons or may be transitioning from one structure to another.***"

Mixed / transitional should not be interpreted as 'Neutral'.

It means only that the Fast, Medium, and Slow [pressure ratios](#pressure-ratio) do not currently form one of the two strict monotonic orderings.

---

#### Cross-Horizon Ordering vs Day-to-Day Change

This is the most important Pressure Mix distinction.

The classification:

- :green-background[recent pressure strengthening]
- :green-background[recent pressure weakening]
- :green-background[mixed / transitional]

is based on the **current ordering of Fast, Medium, and Slow**.

The parenthetical changes are based on **current value versus prior-session value**.

These are different comparisons.

For example:
- Fast 0.35 (+0.01, +2.9%)
- Medium 0.40 (+0.02, +5.3%)
- Slow 0.46 (-0.00, -0.4%)

The Fast and Medium components both rose from the prior session.

But the current ordering is still: :gray-background[0.35 < 0.40 < 0.46] so the hover correctly shows :green-background[recent pressure weakening]

There is no contradiction.

The day-to-day changes say:

> "***Fast and Medium improved compared with yesterday.***"

The cross-horizon ordering says:

> "***Even after that improvement, recent pressure is still weaker than medium pressure, and medium pressure is still weaker than slow pressure.***"

A useful distinction is:

| Displayed information | Comparison being made | Question answered |
| --- | --- | --- |
| +0.01, +2.9% | Fast today vs Fast yesterday | Did Fast improve or deteriorate since yesterday? |
| +0.02, +5.3% | Medium today vs Medium yesterday | Did Medium improve or deteriorate since yesterday? |
| Fast < Medium < Slow | Current Fast vs current Medium vs current Slow | Is recent pressure weaker or stronger than the broader pressure structure? |

Both views are useful.

They should not be substituted for one another.

---

#### How to Use Pressure Mix

:violet-background[Pressure Mix] is best used as **context around the staged-reversal Signal**.

It can help answer:
- Is recent pressure improving while a bullish Watch is active?
- Is recent pressure still weakening while a bullish divergence is waiting for confirmation?
- Is recent pressure deteriorating while a bearish Watch is active?
- Is the pressure structure becoming mixed as a prior directional pattern loses alignment?
- Is a developing Signal supported or opposed by the short-vs-long pressure structure?

For example:
- :violet-background[Signal]: :green-background[Bullish Setup (Watch)]
- :violet-background[Pressure Mix]: :green-background[recent pressure strengthening]

means:

> "***UO is currently in the bullish Watch zone, while the shortest-horizon buying-pressure ratio is stronger than the medium ratio, which is stronger than the long ratio. The current pressure structure is improving from short to long horizon.***"

By contrast:

- :violet-background[Signal]: :green-background[Bullish Setup (Watch)]
- :violet-background[Pressure Mix]: :green-background[recent pressure weakening]

means:

> "***The current UO value is low enough for a bullish Watch, but the short-horizon pressure structure is still weaker than the broader pressure underneath it.***"

The second combination does not cancel the Watch.

It provides additional context about what is happening inside the blended oscillator.

---

#### What Pressure Mix Does Not Do

:violet-background[Pressure Mix] does **not** directly determine the UO Signal or heatmap score.

Specifically:

- '[recent pressure strengthening](#recent-pressure-strengthening)' does not automatically mean Bullish.
- '[recent pressure weakening](#recent-pressure-weakening)' does not automatically mean [Bearish](#bearish-confirmed-signal).
- '[mixed / transitional](#mixed--transitional)' does not mean [No Active Setup](#no-active-setup-signal).
- Pressure Mix does not create a [Watch](#watch).
- Pressure Mix does not create a [Divergence](#divergence).
- Pressure Mix does not trigger [Classic Confirmation](#classic-confirmation).
- Pressure Mix does not override [state precedence](#state-precedence).

The core distinction is:

> "***Pressure Mix explains the internal multi-horizon pressure structure. Signal identifies the strongest active staged-reversal state.***"

That is why two observations with similar final UO values can still carry different Pressure Mix information.

See also:

- [How UO Is Calculated](#how-uo-is-calculated)
- [The Staged Reversal Framework](#the-staged-reversal-framework)
- [Signal and Rule](#signal-and-rule)

---

### Divergence 101
[Section](#uo-hover-field-reference)

:violet-background[Divergence] tells you whether price and UO have formed a qualifying **confirmed-pivot disagreement**.

It answers:
> "***Has price made a new confirmed swing extreme while UO failed to confirm that move?***"

A [divergence](#divergence) is more specific than simply seeing price and UO move in opposite directions for a day or two.

The UO model compares **confirmed five-bar price pivots** and samples UO on those same pivot dates.

For a divergence to qualify, the structure must also include the relevant UO extreme:
- [bullish divergence](#active---bullish-bullish-divergence) requires qualifying [oversold](#oversold) involvement;
- [bearish divergence](#active---bearish-bearish-divergence) requires qualifying [overbought](#overbought) involvement.

Once a qualifying divergence becomes knowable, it can remain active while the app waits for [Classic Confirmation 101](#classic-confirmation-101).

---

#### Divergence Outcomes

There are exactly three displayed :violet-background[Divergence] outcomes:

- :green-background[None]
- :green-background[Active - Bullish]
- :green-background[Active - Bearish]

##### None
$\small{\textsf{Scope: Divergence}}$

:violet-background[Divergence]: :green-background[None]

means there is **no currently active qualifying UO divergence**.

This can occur because:

- no qualifying confirmed-pivot divergence has formed;
- a prior divergence already confirmed;
- a prior divergence expired;
- or the current setup is only at the Watch stage.

It does **not** mean UO contains no useful information.

For example:

- :violet-background[Zone]: :green-background[Oversold]
- :violet-background[Divergence]: :green-background[None]
- :violet-background[Signal]: :green-background[Bullish Setup (Watch)]

means UO is currently extreme enough for a bullish Watch, but the confirmed-pivot divergence condition has not become the active setup.

Related: [None (Classic Confirmation)](#none-1)

##### Active - Bullish ('Bullish Divergence')
Here, we're referring to "$\large{\textcolor{crimson}{\textsf{Bullish Divergence}}}$"

:violet-background[Divergence]: :green-background[Active - Bullish] means the model has identified:
1. a **lower confirmed price swing low**;
2. a **higher corresponding UO pivot low**; and
3. qualifying [oversold](#oversold) involvement in the two-pivot structure.

> :blue-background[current price pivot low < prior price pivot low] AND :blue-background[current UO pivot low > prior UO pivot low] with qualifying oversold involvement.

In shorthand:
- Price: lower low
- UO: higher low

In plain English:
> "***Price pushed to a lower confirmed low, but UO did not become as weak as it was at the prior confirmed low. Downside price pressure and UO pressure are no longer confirming one another.***"

This is a **bullish reversal setup**, not a completed bullish reversal.

The setup remains at the Divergence stage until it either:
- reaches its bullish Classic Confirmation trigger; or
- expires without confirming.

While active, the heatmap cell displays $\large{\textcolor{blue}{\textsf{◆}}}$ to the right of the UO value.

See [Classic Confirmation 101](#classic-confirmation-101); [Confirmation Trigger](#confirmation-trigger)

##### Active - Bearish ('Bearish Divergence')
This is case of a "$\large{\textcolor{crimson}{\textsf{Bearish Divergence}}}$".

:violet-background[Divergence]: :green-background[Active - Bearish] means the model has identified:
1. a **higher confirmed price swing high**;
2. a **lower corresponding UO pivot high**; and
3. qualifying [overbought](#overbought) involvement in the two-pivot structure.

> :blue-background[current price pivot high > prior price pivot high] AND :blue-background[current UO pivot high < prior UO pivot high] with qualifying overbought involvement.

In shorthand:
- Price: higher high
- UO: lower high

In plain English:
- "***Price pushed to a higher confirmed high, but UO did not become as strong as it was at the prior confirmed high. Upside price movement and UO pressure are no longer confirming one another.***"

This is a **bearish reversal setup**, not a completed bearish reversal.

While active, the heatmap cell displays $\large{\textcolor{red}{\textsf{◆}}}$ to the right of the UO value.

The setup remains active until it confirms or expires.

---

#### The Qualifying Extreme Requirement

The model does not treat every pair of diverging pivots as a UO reversal setup.

A [qualifying extreme](#qualifying-extreme) must be present in the two-pivot structure.

For bullish divergence, at least one of the two UO pivot lows must be below the bullish extreme threshold for the active UO variant:

| UO variant | Qualifying bullish extreme |
| --- | ---: |
| UO(5,10,15) | UO < 30 |
| UO(7,14,28) | UO < 35 |
| UO(10,20,40) | UO < 35 |

For bearish divergence, at least one of the two UO [pivot](#pivot) highs must satisfy :blue-background[UO > 70] for all three variants.

This requirement links the divergence back to the '***Extreme → Divergence → Confirmation***' framework.

Importantly, the **current** UO value does not have to remain inside the extreme zone once the divergence becomes active.

See [Zone and Watch](#zone-and-watch).

---

#### Understanding Prior, Current, and Event

When :violet-background[Divergence] is active, the hover can show a line such as:

:violet-background[Divergence]: :green-background[Active - Bullish]
- ':gray[Prior: 9/6/22, $251.94, UO 27.88 | Current: 9/30/22, $232.73, UO 37.34 | Event: 10/4/22]'

The three labels have different meanings.

Section: [Divergence 101](#divergence-101)

##### Prior

:violet-background[Prior] identifies the earlier confirmed price [pivot](#pivot) used in the divergence comparison.

It includes:
- the [prior pivot](#prior-pivot) date;
- the price at that pivot;
- the UO value sampled on that same pivot date.

Example: :gray-background[Prior: 9/6/22, $251.94, UO 27.88] means:
> "On September 6, price formed the earlier qualifying pivot low at $251.94 and UO was 27.88 on that same date."

Terms: [prior pivot](#prior-pivot); [pivot](#pivot)
Section: [Divergence 101](#divergence-101)

##### Current

:violet-background[Current] identifies the newer confirmed price pivot.

It likewise includes:

- the [newer pivot](#current-pivot) date;
- the price at that pivot;
- the UO value sampled on that date.

Example: :gray-background[Current: 9/30/22, $232.73, UO 37.34] means:
> "*On September 30, price formed a lower pivot low at $232.73 while UO formed a higher corresponding pivot low at 37.34".

The bullish divergence is therefore visible in the comparison:
- :blue[Price: $251.94 → $232.73] = lower low
- :blue[UO: 27.88 → 37.34] = higher low


Terms: [Current Pivot](#current-pivot)
Section: [Divergence 101](#divergence-101)

##### Event

:violet-background[Event] is **not** the same date as the Current pivot.

It is the date the newer five-bar pivot becomes knowable.

In the example:
- [Current pivot](#current-pivot): 9/30/22
- [Event](#event): 10/4/22

The September 30 pivot requires two later trading sessions before the app can confirm that it really was a five-bar swing low.

Only then can the divergence be emitted without using future information.

Section: [Divergence 101](#divergence-101)

---

#### Confirmed Five-Bar Pivots

A five-bar pivot uses the candidate pivot session plus two trading sessions on either side.

For a pivot low, the center value must be lower than:
- each of the two preceding lows; and
- each of the two following lows.

For a pivot high, the center value must be higher than:
- each of the two preceding highs; and
- each of the two following highs.

Conceptually:

Day -2 | Day -1 | **Pivot** | Day +1 | Day +2

The two future sessions are why the pivot cannot be known on the pivot date itself.

This confirmed-pivot architecture prevents the app from pretending that a swing was known before the market supplied enough information to establish it.

---

#### Why the Event Date Comes After the Pivot Date

The distinction between :violet-background[Current] and :violet-background[Event] prevents **back-painting**.

Suppose Friday becomes the eventual pivot low.

On Friday itself, the app cannot know that Monday and Tuesday will both remain above Friday's low.

The pivot becomes confirmed only after those two later trading sessions exist.

Therefore:

> "***The pivot date tells you where the swing occurred. The Event date tells you when the app could legitimately know that the swing was confirmed.***"

The divergence state begins from the Event date, not retroactively on the pivot date.

See [No Back-Painting](#no-back-painting).

---

#### How Long Divergence Remains Active

Once a qualifying divergence is emitted, it becomes a persistent setup while Classic Confirmation is pending.

It does **not** require UO to remain in the original oversold or overbought zone every day.

The divergence remains active until one of two things happens:

1. UO crosses the applicable Classic [Confirmation trigger](#confirmation-trigger) within the allowed window; or
2. the [confirmation window](#confirmation-window) expires.

If confirmation occurs, the current session becomes a Confirmed event.

If the setup expires, the divergence is no longer active and cannot be revived later by crossing the old trigger.

See [Classic Confirmation 101](#classic-confirmation-101).

---

#### What the Divergence Diamond Means

The diamond is a visual marker for the **active divergence state**.

| Symbol | Meaning |
| --- | --- |
| $\large{\textcolor{blue}{\textsf{◆}}}$ | Active bullish divergence |
| $\large{\textcolor{red}{\textsf{◆}}}$ | Active bearish divergence |

The diamond appears while the [semantic state](#semantic-state) is Bullish Divergence or Bearish Divergence.

It does not appear merely because an old divergence once existed.

It also does not remain as the primary divergence marker on a Confirmed event, because the Confirmed heatmap state now communicates the higher-priority event.

The diamond means:

> "***A qualifying confirmed-pivot divergence is active and awaiting resolution.***"

It does **not** mean:

> Price must reverse.

---

#### How Divergence Affects the UO Signal

An active bullish divergence maps to:

- :violet-background[Signal]: :green-background[Bullish Setup (Divergence)]
- heatmap score: $\small{\fcolorbox{none}{lightgreen}{\textsf{+1}}}$

An active bearish divergence maps to:

- :violet-background[Signal]: :green-background[Bearish Setup (Divergence)]
- heatmap score: $\small{\fcolorbox{none}{pink}{\textsf{-1}}}$

Watch and Divergence share the same directional score, but they represent different levels of structural evidence.

Watch means:

> UO is currently in an extreme zone.

Divergence means:

> Price and UO have formed a qualifying confirmed-pivot disagreement.

That distinction is why the hover preserves the more specific Signal vocabulary even though both project to the same [heatmap score](#heatmap-score).

See also:

- [Classic Confirmation 101](#classic-confirmation-101)
- [Signal and Rule](#signal-and-rule)
- [The Staged Reversal Framework](#the-staged-reversal-framework)

---

### Classic Confirmation 101
[Section](#uo-hover-field-reference) | [Top](#ultimate-oscillator-at-a-glance)


:violet-background[Classic Confirmation] tells you whether an active qualifying divergence has crossed the UO level required to confirm the setup.

It answers:

> "***Has UO actually broken the trigger derived from the divergence structure, or is the setup still waiting?***"

Classic Confirmation is the third stage of the UO reversal framework:
```text
  Extreme
    ↓
Divergence
    ↓
Confirmation
```

A divergence creates the setup.

Classic Confirmation determines whether that setup reaches the [Confirmed](#confirmed) [state](#state-precedence).

---

#### Classic Confirmation Outcomes

There are exactly five displayed :violet-background[Classic Confirmation] outcomes:

- :green-background[None]
- :green-background[Pending]
- :green-background[Bullish Confirmed]
- :green-background[Bearish Confirmed]
- :green-background[Expired]

Section: [Classic Confirmation 101](#classic-confirmation-101)

##### None
$\small{\textsf{Scope: Classic Confirmation}}$

:violet-background[Classic Confirmation]: :green-background[None] means there is no current confirmation condition to display for the observation.

Typically, there is no active divergence awaiting resolution and no confirmation or expiry event being reported on that session.

Examples include:
- a simple Watch state;
- No Active Setup;
- ordinary observations with no active staged divergence.

:green-background[None] does not mean that UO itself is neutral.

It means only that there is no applicable Classic Confirmation status for the current observation.

Scope: [Classic Confirmation Outcomes](#classic-confirmation-outcomes)
Related: [None (Divergence)](#none)

##### Pending
$\small{\textsf{Scope: Classic Confirmation}}$

:violet-background[Classic Confirmation]: :green-background[Pending] means a qualifying divergence is active, its [confirmation window](#confirmation-window) remains open, and UO has **not yet strictly crossed** the applicable confirmation trigger.

The hover may show:
:violet-background[Classic Confirmation]: :green-background[Pending] :gray-background[(Trigger: 51.74 | 10 sessions remaining)]

The displayed information tells you:

- the exact UO level that must be broken; and
- how much of the confirmation window remains.

In plain English:

> "***The divergence exists, but the required UO breakout has not happened yet.***"

A Pending bullish setup remains: :violet-background[Signal]: :green-background[Bullish Setup (Divergence)]

A Pending bearish setup remains: :violet-background[Signal]: :green-background[Bearish Setup (Divergence)]

Scope: [Classic Confirmation Outcomes](#classic-confirmation-outcomes)

##### Bullish Confirmed
$\small{\textsf{Scope: Classic Confirmation}}$

:violet-background[Classic Confirmation]: :green-background[Bullish Confirmed] means UO has **strictly moved above** the bullish confirmation trigger before the setup expired.

The hover may show:

:violet-background[Classic Confirmation]: :green-background[Bullish Confirmed] (Trigger: 36.48 | Event: 1/21/25)

The corresponding Signal is: :violet-background[Signal]: :green-background[Bullish Confirmed]

with [heatmap score](#heatmap-score): $\small{\fcolorbox{none}{Green}{\textcolor{white}{\textsf{+2}}}}$

In plain English:

> "***The qualifying bullish divergence has now passed its defined UO confirmation test.***"

This is stronger evidence than Watch or Divergence alone, but it is not a guarantee that price will rise.

Related: [Bullish Confirmed Signal](#bullish-confirmed-signal)
Scope: [Classic Confirmation Outcomes](#classic-confirmation-outcomes)

##### Bearish Confirmed
$\small{\textsf{Scope: Classic Confirmation}}$

:violet-background[Classic Confirmation]: :green-background[Bearish Confirmed] means UO has **strictly moved below** the bearish confirmation trigger before the setup expired.
- * `Classic Confirmation: Bearish Confirmed` answers ***"Did the bearish divergence complete confirmation?"***

The corresponding Signal is: :violet-background[Signal]: :green-background[Bearish Confirmed]
with heatmap score: $\small{\fcolorbox{none}{Crimson}{\textsf{-2}}}$

In plain English:
> "***The qualifying bearish divergence has now passed its defined UO confirmation test.***"

Again, Confirmed describes completion of the UO setup logic, not certainty about the next price move.


Scope: [Classic Confirmation Outcomes](#classic-confirmation-outcomes)
Related: [Bearish Confirmed 'Signal'](#bearish-confirmed-signal)


##### Expired
$\small{\textsf{Scope: Classic Confirmation}}$

[Classic Confirmation](#classic-confirmation): :green-background[Expired] is a "Classic Confirmation outcome" meaning that a qualifying divergence did not cross its [confirmation trigger](#confirmation-trigger) within the permitted/allowed [confirmation window](#confirmation-window).

The hover displays: :violet-background[Classic Confirmation]: :green-background[Expired] (10-bar window elapsed)

Once expired, the old setup is finished.
- the divergence is no longer active;
- the old Trigger is stale;
- a later crossing of that old Trigger cannot revive the setup. IOW, it does **not** retroactively confirm or reactivate the expired divergence.

In plain English:

> "***The market did not supply the required UO confirmation soon enough, so the old divergence is no longer treated as an active reversal setup.***"

This prevents stale historical divergences from triggering Confirmed states long after the setup that created them has ceased to be timely.

Scope: [Classic Confirmation Outcomes](#classic-confirmation-outcomes)

---

#### Understanding the Trigger
[Section](#classic-confirmation-101)


The :violet-background[Trigger] is derived from the UO values inside the divergence span.

For a bullish divergence:
> Bullish Trigger = the **highest UO value from the Prior pivot through the Current pivot, inclusive**

- Confirmation requires: :red-background[current UO > Bullish Trigger]

For a bearish divergence:
> Bearish Trigger = the **lowest UO value from the Prior pivot through the Current pivot, inclusive**

- Confirmation requires: :red-background[current UO < Bearish Trigger]

The inequalities are strict.

Therefore:
- UO equal to a bullish Trigger is **not** Bullish Confirmed.
- UO equal to a bearish Trigger is **not** Bearish Confirmed.

The oscillator must actually break through the level.

---

#### Understanding 'Sessions Remaining'
***The number of eligible confirmation sessions still available while :violet-background[Classic Confirmation] is :green-background[Pending].***


When confirmation is :green-background[Pending], the hover can show the number of sessions remaining.

For example:
:green-background[10 sessions remaining] means the divergence has just become actionable and the setup still has its full post-event allowance available.

The Event session itself is also eligible for confirmation.

The timing convention is:
- Event date = lag 0 and may confirm immediately;
- confirmation remains eligible through the next 10 trading sessions;
- if no strict trigger break has occurred, the setup expires before the following session.

This is why a same-day [divergence](#divergence-event)-and-[confirmation event](#confirmation-event) is possible while the model still enforces the 10-session expiry discipline.


Section: [Classic Confirmation 101](#classic-confirmation-101)

---

#### Understanding the 'Confirmation Event'
The session on which UO actually crosses the applicable [Confirmation Trigger](#confirmation-trigger).

For a Confirmed observation, :violet-background[Event] identifies the session on which UO actually crossed the confirmation trigger.

For example:
:violet-background[Classic Confirmation]: :green-background[Bullish Confirmed] (Trigger: 36.48 | Event: 1/21/25) means:
- 36.48 was the bullish confirmation level;
- UO moved strictly above that level on January 21, 2025;
- January 21 is therefore the Bullish Confirmed event session.

Do not confuse this with the [Divergence Event](#divergence-event).

They answer different questions:

| Event | Meaning |
| --- | --- |
| Divergence Event | Date the newer five-bar pivot became knowable and the divergence could legitimately be emitted |
| [Confirmation Event](#confirmation-event) | Date UO actually crossed the Classic Confirmation trigger |

The two dates may differ.

They may also be the same.

---

#### Bullish Confirmation Logic

A bullish setup begins with a qualifying bullish divergence:

Price: lower confirmed low
UO: higher corresponding pivot low
Qualifying extreme: oversold involvement

The model then finds the highest UO reading from the Prior pivot through the Current pivot.

That becomes the bullish [Trigger](#confirmation-trigger).

The setup confirms only when: :red-background[UO > Trigger] within the allowed window.

This produces:
- :violet-background[Classic Confirmation]: :green-background[Bullish Confirmed]
- :violet-background[Signal]: :green-background[Bullish Confirmed]
- **[heatmap score](#heatmap-score)**: $\small{\fcolorbox{none}{Green}{\textcolor{white}{\textsf{+2}}}}$

---

#### Bearish Confirmation Logic

A bearish setup begins with a qualifying bearish divergence:
- Price: higher confirmed high
- UO: lower corresponding pivot high
- [Qualifying extreme](#qualifying-extreme): overbought involvement

The model then finds the lowest UO reading from the Prior pivot through the Current pivot.
- That becomes the bearish Trigger.

The setup confirms only when: :red-background[UO < Trigger] within the allowed window.

This produces:
- :violet-background[Classic Confirmation]: :green-background[Bearish Confirmed]
- :violet-background[Signal]: :green-background[Bearish Confirmed]
- heatmap score: $\small{\fcolorbox{none}{Crimson}{\textsf{-2}}}$

---

#### Same-Day Divergence and Confirmation

A qualifying divergence can confirm on the same session that the divergence first becomes knowable.

This is intentional.

The confirmation search begins on the [Divergence Event](#divergence-event) date itself.

For example:

- Current pivot occurs on January 17.
- Two later trading sessions confirm that pivot.
- Divergence Event is January 21.
- UO on January 21 is already above the bullish Trigger.

The January 21 observation can therefore be:

- :violet-background[Divergence]: :green-background[None]
- :violet-background[Classic Confirmation]: :green-background[Bullish Confirmed]
- :violet-background[Signal]: :green-background[Bullish Confirmed]

This may initially look surprising because there is no visible intermediate Divergence state on that same row.

The reason is state precedence:

> "***Confirmed outranks Divergence.***"

The divergence condition became knowable, but it also confirmed immediately, so the higher-priority state is displayed.

See [State Precedence](#state-precedence).

---

#### The 10-Session Confirmation Window

The [confirmation window](#confirmation-window) prevents a divergence from remaining actionable indefinitely.

The [Divergence Event](#divergence-event) session is eligible immediately.

After that, the setup remains eligible through the next 10 trading sessions.

If the strict trigger break has still not occurred by the end of that allowance, the setup expires before the following session.

The purpose is not to claim that every valid reversal must occur within an exact universal market law.

The purpose is to keep the rule engine from treating a very old divergence as though it were still the same active setup.

---

#### Why Confirmation Can Expire

Without expiry, a historical divergence could remain dormant for weeks or months and then appear to "confirm" merely because UO eventually crossed an old trigger.

That would make the signal difficult to interpret.

Expiry imposes a bounded relationship between:

- the divergence structure; and
- the [confirmation event](#confirmation-event) that is supposed to validate it.

Once the window closes:

> "***The old divergence is stale. A later trigger crossing must not revive it.***"

A new qualifying pivot structure is required for a new divergence setup.

---

#### What Confirmation Does and Does Not Mean

Classic Confirmation means:

> "***The qualifying UO divergence completed the project's defined confirmation step within the permitted time window.***"

It does **not** mean:

- price is guaranteed to reverse;
- the Confirmed direction must dominate every contextual UO field;
- the current Zone must still be oversold or overbought;
- Pressure Bias must already agree;
- Pressure Mix must already agree.

This is why a valid observation can show, for example:

- :violet-background[Zone]: :green-background[Overbought]
- :violet-background[Classic Confirmation]: :green-background[Bullish Confirmed]
- :violet-background[Signal]: :green-background[Bullish Confirmed]

The Zone describes the current oscillator location.

Classic Confirmation describes completion of the previously established divergence setup.

See also:

- [Divergence 101](#divergence-101)
- [Signal and Rule](#signal-and-rule)
- [The Staged Reversal Framework](#the-staged-reversal-framework)

---

### Signal and Rule

**'[Signal](#signal)'** tells you the **highest-priority active UO semantic state**.
***'[Rule](#rule)'*** tells you **why that Signal was assigned**.

Read together:
- "***Signal tells you what state the UO model is in. Rule tells you the condition that put it there.***"

This pairing is important because seven distinct UO states are projected onto only five [heatmap score](#heatmap-score) levels.

The Signal preserves the semantic detail that the background color alone cannot show.


---

#### The Seven Semantic States

The underlying UO model recognizes exactly seven states:

1. Bullish Confirmed
2. Bullish Watch
3. Bullish Divergence
4. No Active Setup
5. Bearish Watch
6. Bearish Divergence
7. Bearish Confirmed


The user-facing Signal labels are:

| Semantic state | :violet-background[Signal] shown in the hover |
| --- | --- |
| [Bullish Confirmed](#bullish-confirmed-signal) | :green-background[Bullish Confirmed] |
| [Bullish Watch](#bullish-watch-signal) | :green-background[Bullish Setup (Watch)] |
| [Bullish Divergence](#bullish-divergence-signal) | :green-background[Bullish Setup (Divergence)] |
| [No Active Setup](#no-active-setup-signal) | :green-background[No Active Setup] |
| [Bearish Watch](#bearish-watch-signal) | :green-background[Bearish Setup (Watch)] |
| [Bearish Divergence](#bearish-divergence-signal) | :green-background[Bearish Setup (Divergence)] |
| [Bearish Confirmed](#bearish-confirmed-signal) | :green-background[Bearish Confirmed] |

Every valid UO observation with available semantic context lands in one of these seven states.


---

#### User-Facing Signal Labels


##### Bullish Watch Signal
$\small{\textsf{Scope: Signal}}$

:violet-background[Signal]: :green-background[Bullish Setup (Watch)] means the current UO value is inside the bullish Watch zone and no higher-priority Bullish Divergence or Bullish Confirmed state is active.

The corresponding :violet-background[Rule] is variant-specific:
- For UO(5,10,15): :blue-background[UO < 30]
- For UO(7,14,28): :blue-background[UO < 35]
- For UO(10,20,40): :blue-background[UO < 35]

In plain English:

> "***UO is currently at a meaningful downside extreme, so the model is watching for stronger reversal evidence.***"

Heatmap score: $\small{\fcolorbox{none}{lightgreen}{\textsf{+1}}}$

See [Zone and Watch](#zone-and-watch).

##### Bullish Divergence Signal
$\small{\textsf{Scope: Signal}}$

:violet-background[Signal]: :green-background[Bullish Setup (Divergence)]

means a qualifying bullish confirmed-pivot divergence is active and awaiting confirmation.

The displayed :violet-background[Rule] is:

> Lower confirmed price low + higher UO pivot low, with a qualifying oversold reading; awaiting confirmation.

In plain English:

> "***Price made a lower confirmed low while UO made a higher corresponding low, and the structure included the required oversold condition. The setup is now waiting for Classic Confirmation.***"

Heatmap score: $\small{\fcolorbox{none}{lightgreen}{\textsf{+1}}}$

See [Divergence 101](#divergence-101); [bullish divergence](#active---bullish-bullish-divergence)

##### Bullish Confirmed Signal
$\small{\textsf{Scope: Signal}}$

:violet-background[Signal]: [Bullish Confirmed](#bullish-confirmed) means a qualifying bullish divergence subsequently broke above its Classic Confirmation trigger within the allowed window.

The displayed :violet-background[Rule] is:

> Qualifying bullish divergence + UO broke above its Classic Confirmation trigger within the 10-session window.

In plain English:

> "***The bullish divergence progressed through the project's confirmation step.***"

Heatmap score: $\small{\fcolorbox{none}{Green}{\textcolor{white}{\textsf{+2}}}}$

See [Classic Confirmation 101](#classic-confirmation-101)


##### 'No Active Setup' Signal
$\small{\textsf{Scope: Signal}}$

:violet-background[Signal]: :green-background[No Active Setup] is a valid UO [semantic state](#semantic-state) that means no 'Watch', 'Divergence', or 'Confirmed' setup currently has precedence.

It only means "***No staged reversal setup is currently active***".

The displayed :violet-background[Rule] is:
> No active Watch, Divergence, or Confirmed setup.

Heatmap score: $\small{\fcolorbox{none}{gainsboro}{\textsf{0}}}$

This does **not** mean:
- UO equals 50;
- Pressure Bias must be Balanced;
- Pressure Mix must be mixed;
- nothing useful can be learned from the UO context fields.


See: [No Active Setup](#no-active-setup); [No Active Setup: Meaningful Context](#no-active-setup--meaningful-context)


##### Bearish Watch Signal
$\small{\textsf{Scope: Signal}}$

:violet-background[Signal]: :green-background[Bearish Setup (Watch)]

means current UO is above the bearish Watch threshold and no higher-priority Bearish Divergence or Bearish Confirmed state is active.

The displayed :violet-background[Rule] is:

:blue-background[UO > 70]

In plain English:

> "***UO is currently at a meaningful upside extreme, so the model is watching for stronger bearish reversal evidence.***"

Heatmap score: $\small{\fcolorbox{none}{pink}{\textsf{-1}}}$


See [Zone and Watch](#zone-and-watch).

##### Bearish Divergence Signal
$\small{\textsf{Scope: Signal}}$

:violet-background[Signal]: :green-background[Bearish Setup (Divergence)]

means a qualifying bearish confirmed-pivot divergence is active and awaiting confirmation.

The displayed :violet-background[Rule] is:

> Higher confirmed price high + lower UO pivot high, with a qualifying overbought reading; awaiting confirmation.

In plain English:

> "***Price made a higher confirmed high while UO made a lower corresponding high, and the structure included the required overbought condition. The setup is now waiting for Classic Confirmation.***"

Heatmap score: $\small{\fcolorbox{none}{pink}{\textsf{-1}}}$

See [Divergence 101](#divergence-101); [bearish divergence](#active---bearish-bearish-divergence)

##### Bearish Confirmed Signal
$\small{\textsf{Scope: Signal Labels/Outcomes}}$

:violet-background[Signal]: '[Bearish Confirmed](#bearish-confirmed)' means a qualifying bearish divergence subsequently broke below its Classic Confirmation trigger within the allowed window.

The displayed :violet-background[Rule] is:

> "*Qualifying bearish divergence + UO broke below its Classic Confirmation trigger within the 10-session window.*"

In plain English:

> "***The bearish divergence progressed through the project's confirmation step.***"

Heatmap score: $\small{\fcolorbox{none}{Crimson}{\textsf{-2}}}$


Section: [Signal and Rules](#signal-and-rule)
See [Classic Confirmation 101](#classic-confirmation-101).


${\textsf{Difference: 'Bearish Confirmed' under "Signals" vs. "Classic Confirmation" }}$
Under **Signal**, `Bearish Confirmed` means:
> the highest-priority active UO semantic state for that observation is Bearish Confirmed.

Under **Classic Confirmation**, `Bearish Confirmed` means:
> the qualifying bearish divergence has successfully completed the confirmation step by breaking below its bearish confirmation trigger within the allowed window.

So the **underlying event/state is the same**. The difference is the field's role:
* `Classic Confirmation: Bearish Confirmed` answers *"Did the bearish divergence complete confirmation?"*
* `Signal: Bearish Confirmed` answers ***"What is the highest-priority active UO state?"***

---

#### Five Heatmap Scores from Seven UO States

The heatmap still uses the project's standard five-level score range.

The seven UO semantic states therefore project into five scores:

| UO semantic state | Heatmap score |
| --- | ---: |
| Bullish Confirmed | +2 |
| Bullish Watch | +1 |
| Bullish Divergence | +1 |
| No Active Setup | 0 |
| Bearish Watch | -1 |
| Bearish Divergence | -1 |
| Bearish Confirmed | -2 |

This preserves compatibility with the broader heatmap while keeping the richer UO meaning available in the hover.

---

#### Why Watch and Divergence Share the Same Score

Watch and Divergence represent different amounts of structural information, but neither has completed Classic Confirmation.

A Watch says:

> "***An extreme exists.***"

A Divergence says:

> "***An extreme participated in a confirmed-pivot price/UO disagreement.***"

A Confirmed state says:

> "***That divergence also crossed its required confirmation trigger in time.***"

The score therefore reserves ±2 for Confirmed events.

Watch and Divergence both remain at ±1, while the :violet-background[Signal] field tells you which setup is actually present.

This is why the Signal label matters even when two cells share the same background color.

---

#### Dynamic Rule Text

The UO :violet-background[Rule] is intentionally dynamic.

It changes with the active Signal rather than displaying one generic description for every UO observation.

That makes the Rule field a direct explanation of the current classification.

| :violet-background[Signal] | What :violet-background[Rule] explains |
| --- | --- |
| :green-background[Bullish Setup (Watch)] | The applicable UO < 30 or UO < 35 threshold |
| :green-background[Bullish Setup (Divergence)] | Lower confirmed price low + higher UO pivot low + qualifying oversold involvement |
| :green-background[Bullish Confirmed] | Qualifying bullish divergence + break above the confirmation trigger within the window |
| :green-background[No Active Setup] | No active Watch, Divergence, or Confirmed setup |
| :green-background[Bearish Setup (Watch)] | UO > 70 |
| :green-background[Bearish Setup (Divergence)] | Higher confirmed price high + lower UO pivot high + qualifying overbought involvement |
| :green-background[Bearish Confirmed] | Qualifying bearish divergence + break below the confirmation trigger within the window |

The intended standard is:

> "***A user should be able to reconstruct why the observation received its Signal without reverse-engineering the code.***"

---

#### Reading Signal and Rule Together

When reviewing a UO hover, read these two fields as a pair.

For example:

- :violet-background[Signal]: :green-background[Bullish Setup (Divergence)]
- :violet-background[Rule]: Lower confirmed price low + higher UO pivot low, with a qualifying oversold reading; awaiting confirmation.

The Signal tells you:

> Bullish divergence is the active state.

The Rule tells you:

> Exactly what structural condition produced that state and what remains unresolved.

Likewise:

- :violet-background[Signal]: :green-background[Bullish Confirmed]
- :violet-background[Rule]: Qualifying bullish divergence + UO broke above its Classic Confirmation trigger within the 10-session window.

The Signal tells you:

> The setup reached the highest bullish UO state.

The Rule tells you:

> It reached that state because the divergence completed the required confirmation step in time.

This is the core interpretability contract for UO:

> "***Signal states the result. Rule states the reason.***"

See also:

- [Zone and Watch](#zone-and-watch)
- [Pressure Bias and the 50-Line Crossover](#pressure-bias-and-the-50-line-crossover)
- [Pressure Mix 101](#pressure-mix-101)
- [Divergence 101](#divergence-101)
- [Classic Confirmation 101](#classic-confirmation-101)
- [The Staged Reversal Framework](#the-staged-reversal-framework)

---
## The Staged Reversal Framework
[Top](#ultimate-oscillator-at-a-glance)

The UO model is built around a three-stage reversal sequence: :gray-background[Extreme → Divergence → Confirmation]

The stages represent progressively stronger evidence.

They are **not** three independent signals that must appear on three consecutive sessions, and they do not all persist in the same way.

A useful way to think about the framework is:

1. **Watch** asks whether UO is currently extreme enough to deserve attention.
2. **Divergence** asks whether price and UO have formed a qualifying confirmed-pivot disagreement.
3. **Confirmation** asks whether UO subsequently broke the trigger required to validate that divergence.

The framework therefore moves from:

> "***Potential → Structure → Trigger***"

The app then applies state precedence so that the strongest currently active stage becomes the displayed :violet-background[Signal].

See also:

- [Zone and Watch](#zone-and-watch)
- [Divergence 101](#divergence-101)
- [Classic Confirmation 101](#classic-confirmation-101)
- [Signal and Rule](#signal-and-rule)

---

### The Staged Reversal Lifecycle

#### Stage 1 — Watch

Watch is the first stage.

It is based on the **current UO value** being inside the active variant's extreme zone.

For a bullish Watch:
- UO(5,10,15): :blue-background[UO < 30]
- UO(7,14,28): :blue-background[UO < 35]
- UO(10,20,40): :blue-background[UO < 35]

For a bearish Watch:

- all three variants: :blue-background[UO > 70]

A [Watch](#watch) means:

> "***UO is currently extreme enough to justify monitoring for a possible reversal setup.***"

It does **not** mean that a divergence already exists.

It also does not mean that price has already reversed.

Example:

:gray-background[UO(7,14,28) = 32.4] produces
- :violet-background[Zone]: :green-background[Oversold]

and, if no higher-priority bullish state is active:
- :violet-background[Signal]: :green-background[Bullish Setup (Watch)]

The important lifecycle point is that Watch is tied to the **current** oscillator extreme.

If UO leaves that extreme zone before a qualifying divergence becomes active, Watch itself does not persist merely because the stock was recently oversold or overbought.

See [Zone and Watch](#zone-and-watch).

---

#### Stage 2 — Divergence

Divergence is the second stage.

It requires more evidence than [Watch](#watch).

A bullish divergence requires:

- :blue-background[current confirmed price pivot low < prior confirmed price pivot low]
- :blue-background[current UO pivot low > prior UO pivot low]
- :blue-background[at least one of the two UO pivot lows is below the bullish extreme threshold]

A bearish divergence requires the mirror image:

- :blue-background[current confirmed price pivot high > prior confirmed price pivot high]
- :blue-background[current UO pivot high < prior UO pivot high]
- :blue-background[at least one of the two UO pivot highs is above 70]

In shorthand:

- Bullish: :gray-background[Price lower low + UO higher low]
- Bearish: :gray-background[Price higher high + UO lower high]

The divergence is based on **[confirmed five-bar pivots](#confirmed-five-bar-pivots)**.

That means the newer pivot cannot become known until two later trading sessions have occurred.

The divergence therefore begins on its '**Event date**', not retroactively on the 'pivot date'.

Once active, a divergence has its own lifecycle and can remain active even if the current UO value has already left the original extreme zone.

This is the key transition from Watch to Divergence:

> "***Watch depends on where UO is now. Divergence depends on a confirmed structure that has already formed.***"

A [bullish divergence](#active---bullish-bullish-divergence) maps to:
- :violet-background[Signal]: :green-background[Bullish Setup (Divergence)]

A [bearish divergence](#active---bearish-bearish-divergence) maps to:
- :violet-background[Signal]: :green-background[Bearish Setup (Divergence)]

Both remain at heatmap score ±1 because confirmation has not yet occurred.

See [Divergence 101](#divergence-101).

---

#### Stage 3 — Confirmation

Confirmation is the third and highest UO reversal stage.

It can occur only after a qualifying divergence exists.

For a bullish divergence, the confirmation trigger is:

> :blue-background[the highest UO value from the Prior pivot through the Current pivot, inclusive]

Bullish confirmation requires:

> :blue-background[current UO > bullish confirmation trigger]

For a bearish divergence, the confirmation trigger is:

> :blue-background[the lowest UO value from the Prior pivot through the Current pivot, inclusive]

Bearish confirmation requires:

> :blue-background[current UO < bearish confirmation trigger]

The break is strict.

Examples:

- If the bullish Trigger is 51.74, :gray-background[UO = 51.74] is **not** confirmed.
- :gray-background[UO = 51.75] satisfies the bullish trigger condition.
- If the bearish Trigger is 44.20, :gray-background[UO = 44.20] is **not** confirmed.
- :gray-background[UO = 44.19] satisfies the bearish trigger condition.

When confirmation occurs:

Bullish:

- :violet-background[Signal]: :green-background[Bullish Confirmed]
- [heatmap score](#heatmap-score): $\small{\fcolorbox{none}{Green}{\textcolor{white}{\textsf{+2}}}}$

Bearish:

- :violet-background[Signal]: :green-background[Bearish Confirmed]
- heatmap score: $\small{\fcolorbox{none}{Crimson}{\textsf{-2}}}$

Confirmation means:

> "***The qualifying divergence completed the project's defined UO trigger step within the permitted time window.***"

It does **not** mean the subsequent price reversal is guaranteed.

See [Classic Confirmation 101](#classic-confirmation-101).

---

### State Precedence

The rule that determines which staged state is displayed when multiple lower-level conditions are simultaneously true.
More than one lower-level condition can be true on the same observation.

The app therefore uses a fixed precedence hierarchy: :red-background[Confirmed > Divergence > Watch > No Active Setup]
- This determines which semantic state becomes the displayed :violet-background[Signal].

The precedence rule is directional in the sense of **setup strength**, not a bullish-versus-bearish voting system.

It prevents the hover from reporting a weaker stage when a stronger stage is already active.
IOW, this is why a [Confirmed event](#confirmation-event) is displayed instead of a [Divergence event](#divergence-event) on a same-day confirmation, and why Divergence outranks [Watch](#watch).


---

#### Confirmed Over Divergence

If a qualifying divergence reaches its confirmation trigger on the same session that the divergence becomes knowable, the displayed state is Confirmed.

For example:

- Current pivot occurs on January 17.
- Two later trading sessions make that pivot knowable on January 21.
- January 21 is therefore the Divergence Event.
- UO on January 21 is already above the bullish Trigger.

The same observation satisfies:

- a newly knowable bullish divergence; and
- bullish Classic Confirmation.

Because:

:blue-background[Confirmed > Divergence]

the displayed result is:

- :violet-background[Signal]: :green-background[Bullish Confirmed]

not:

- :violet-background[Signal]: :green-background[Bullish Setup (Divergence)]

This is why a valid same-day confirmation can occur without an intermediate Divergence state appearing on a separate row.

See [Same-Day Divergence and Confirmation](#same-day-divergence-and-confirmation).

---

#### Divergence Over Watch

A current extreme may still be present when a qualifying divergence becomes active.

For example:

- :violet-background[Zone]: :green-background[Oversold]
- qualifying bullish divergence becomes active

Both the Watch condition and the Divergence condition may be true.

Because:

:blue-background[Divergence > Watch]

the displayed Signal becomes:

- :violet-background[Signal]: :green-background[Bullish Setup (Divergence)]

rather than:

- :violet-background[Signal]: :green-background[Bullish Setup (Watch)]

The current Zone remains visible because it answers a different question.

This preserves both pieces of information:

> "***UO is still oversold, and the setup has progressed beyond Watch into a confirmed-pivot divergence.***"

---

#### Watch Over No Active Setup

If UO is currently inside an extreme Watch zone and no higher-priority Divergence or Confirmed state is active, Watch becomes the displayed state.

For example:

:gray-background[UO(5,10,15) = 27.8] satisfies: :blue-background[UO < 30]

so, absent a higher-priority state:
- :violet-background[Zone]: :green-background[Oversold]
- :violet-background[Signal]: :green-background[Bullish Setup (Watch)]

If UO then moves to: :gray-background[UO(5,10,15) = 34.2] and no qualifying divergence has become active, the Watch condition is gone.

The Signal may then return to:
- :violet-background[Signal]: :green-background[No Active Setup]

This illustrates why Watch is a current-condition state rather than a persistent historical flag.

---

### Persistence, Confirmation, and Expiry

The three stages do not persist in the same way.

That distinction is essential to understanding why the current :violet-background[Zone], :violet-background[Divergence], :violet-background[Classic Confirmation], and :violet-background[Signal] can appear to tell different stories.

A compact summary is:

| Stage | Persists? | Ends when |
| --- | --- | --- |
| Watch | Only while current UO remains inside the applicable extreme zone | UO leaves the zone or a higher-priority state takes over |
| Divergence | Yes | Confirmation occurs or the setup expires |
| Confirmed | No; event-day state | Re-evaluated on the next session |
| Expired setup | No | It is finished and cannot later revive from the old trigger |

---

#### Watch Persistence

Watch does not persist after the current UO value leaves the applicable extreme zone.

Bullish Watch requires:

- Fast variant: :blue-background[current UO < 30]
- Medium/Slow variants: :blue-background[current UO < 35]

Bearish Watch requires:

- :blue-background[current UO > 70]

If the current value no longer satisfies that rule, Watch eligibility ends.

The app does not keep a Watch alive merely because UO was extreme several sessions ago.

However, a divergence that was formed from an earlier extreme can remain active after UO leaves the zone.

That is a different state with different persistence rules.

---

#### Divergence Persistence

Once a qualifying divergence becomes active, it persists while Classic Confirmation remains unresolved.

It does not require the current UO value to stay oversold or overbought.

For example:

A bullish divergence may have been built from:

:gray-background[Prior UO = 27.88]

and:

:gray-background[Current UO = 37.34]

where the earlier pivot supplied the qualifying oversold reading.

By the time the divergence is active, the current UO value can be above the oversold threshold.

The divergence remains valid because its [qualifying extreme](#qualifying-extreme) belongs to the **two-pivot structure**, not to every later observation.

The active divergence ends when:

1. UO confirms within the permitted window; or
2. the [confirmation window](#confirmation-window) expires.

See [Divergence 101](#divergence-101).

---

#### Confirmation as an Event-Day State

Confirmed is an **event-day state**.

When UO crosses its confirmation Trigger within the permitted window, that session becomes:

- :green-background[Bullish Confirmed]; or
- :green-background[Bearish Confirmed]

The app does not then carry Confirmed forward indefinitely.

On the next session, UO is re-evaluated from the current conditions and active setup context.

In other words:

> "***Confirmed tells you that the [confirmation event](#confirmation-event) happened on this observation. It is not a permanent regime label.***"

This is different from an active Divergence, which persists while it waits for resolution.

---

#### Expiry and Stale-Setup Prevention

A divergence is not allowed to wait forever for confirmation.

The [Divergence Event](#divergence-event) session is eligible for immediate confirmation.

The setup remains eligible through the next 10 trading sessions.

The valid confirmation range is therefore:
- :blue-background[Event lag 0 through Event lag 10, inclusive]

If no strict trigger break has occurred, the setup expires before the following session.

Conceptually:
- :gray-background[Event = lag 0 → lag 1 → ... → lag 10 → expiry before lag 11]

Once expired:
- the divergence is no longer active;
- the old confirmation Trigger is stale;
- a later crossing of that old Trigger does not reactivate the setup.

This prevents a divergence from remaining dormant for an unlimited period and then appearing to confirm long after its original market structure has lost timeliness.

A new qualifying pivot structure is required for a new divergence setup.

See [Classic Confirmation 101](#classic-confirmation-101).

---

### Why the Current Zone Can Differ from the Active Signal

One of the most important consequences of the staged framework is that the current :violet-background[Zone] and active :violet-background[Signal] do not always point in the same intuitive direction.

That is not automatically a contradiction.

They operate on different information.

:violet-background[Zone] answers:

> "***Where is the UO value right now relative to its extreme thresholds?***"

:violet-background[Signal] answers:

> "***What is the highest-priority active staged-reversal state?***"

Consider:

- :violet-background[Zone]: :green-background[Overbought]
- :violet-background[Signal]: :green-background[Bullish Confirmed]

At first glance, this may appear inconsistent.
But the two fields describe different parts of the timeline.

The bullish divergence could have originated from an earlier downside extreme.

UO could then recover sharply enough to:
1. leave the oversold zone;
2. cross through the middle of its range;
3. exceed the bullish Classic Confirmation Trigger;
4. continue far enough that the **current** UO value is now overbought.

The observation can therefore legitimately show both:

:gray-background[current location = Overbought]

and:

:gray-background[active event = Bullish Confirmed]

The Zone describes **now**.

The Confirmed Signal describes **what the earlier qualifying divergence has just accomplished**.

Likewise:

- :violet-background[Zone]: :green-background[Neither Extreme]
- :violet-background[Signal]: :green-background[Bullish Setup (Divergence)]

means:

> "***UO is no longer currently oversold, but the qualifying bullish divergence formed from the earlier pivot structure remains active while confirmation is pending.***"

This is why the UO fields should not be treated as independent votes.

A useful reading hierarchy is:

1. Read :violet-background[Signal] to identify the active staged-reversal state.
2. Read :violet-background[Zone] to understand the current oscillator location.
3. Read :violet-background[Divergence] and :violet-background[Classic Confirmation] to reconstruct the setup lifecycle.
4. Use :violet-background[Pressure Bias] and :violet-background[Pressure Mix] as additional current context.

The fields can disagree superficially while remaining internally consistent.

See also:

- [Zone and Watch](#zone-and-watch)
- [Divergence 101](#divergence-101)
- [Classic Confirmation 101](#classic-confirmation-101)
- [Signal and Rule](#signal-and-rule)

---
## The Three UO Variants
[Top](#ultimate-oscillator-at-a-glance)

The app calculates three Ultimate Oscillator variants:

- :violet-background[UO(5,10,15)] — Fast
- :violet-background[UO(7,14,28)] — Classic / Medium
- :violet-background[UO(10,20,40)] — Slow

Each variant uses the same core UO construction and the same staged-reversal logic.

What changes is the **speed of the three pressure horizons** and, for the bullish Watch side, the extreme threshold used by the rule engine.

The practical trade-off is straightforward:

> "***Shorter windows react faster. Longer windows smooth more noise and require more persistent pressure to move materially.***"

The three variants should therefore be treated as **three views of the same pressure process at different speeds**, not as three equal votes that must agree.

---

### UO(5,10,15) — Fast

:violet-background[UO(5,10,15)] is the most responsive UO variant in the app.

Its pressure horizons are:

- Fast = 5 sessions
- Medium = 10 sessions
- Slow = 15 sessions

Its bullish Watch threshold is: :blue-background[UO < 30]
Its bearish Watch threshold is: :blue-background[UO > 70]

Because all three lookbacks are relatively short, this variant responds most quickly to recent changes in buying pressure.

That makes it useful for identifying:

- faster shifts in pressure;
- earlier entry into extreme zones;
- shorter-lived divergences;
- more frequent staged-reversal setups.

The trade-off is that faster sensitivity can also produce more fluctuation and more frequent state changes.

In plain English:

> "***Fast UO reacts first, but it is also the most sensitive to short-term noise.***"

Example:

:gray-background[Fast = 0.62 | Medium = 0.51 | Slow = 0.44]

shows a clear :green-background[recent pressure strengthening] pattern because:

:gray-background[0.62 > 0.51 > 0.44]

See [Pressure Mix 101](#pressure-mix-101).

---

### UO(7,14,28) — Classic / Medium

:violet-background[UO(7,14,28)] is the classic Larry Williams parameterization and serves as the app's middle-speed UO variant.

Its pressure horizons are:

- Fast = 7 sessions
- Medium = 14 sessions
- Slow = 28 sessions

Its bullish Watch threshold is: :blue-background[UO < 35]
Its bearish Watch threshold is: :blue-background[UO > 70]

Compared with UO(5,10,15), it smooths more short-term movement.
Compared with UO(10,20,40), it remains more responsive to recent pressure changes.

This makes it a useful middle ground between speed and stability.

In plain English:

> "***Classic / Medium UO reacts more slowly than Fast UO, but it usually provides a steadier view of the same pressure structure.***"

Example:

:gray-background[UO(7,14,28) = 32.4]

satisfies: :blue-background[UO < 35]

so the current Zone is:

- :violet-background[Zone]: :green-background[Oversold]

and, if no higher-priority setup is active:

- :violet-background[Signal]: :green-background[Bullish Setup (Watch)]

See [Zone and Watch](#zone-and-watch).

---

### UO(10,20,40) — Slow

:violet-background[UO(10,20,40)] is the slowest and smoothest UO variant in the app.

Its pressure horizons are:

- Fast = 10 sessions
- Medium = 20 sessions
- Slow = 40 sessions

Its bullish Watch threshold is: :blue-background[UO < 35]
Its bearish Watch threshold is: :blue-background[UO > 70]

Because the underlying windows are longer, this variant changes more gradually.

It is less sensitive to brief pressure spikes and more influenced by sustained buying-pressure behavior.

That makes it useful for identifying:

- broader multi-week pressure structure;
- more persistent extremes;
- slower-forming divergences;
- longer-duration changes in pressure balance.

The trade-off is delayed responsiveness.

In plain English:

> "***Slow UO filters more short-term noise, but it will usually react later than the Fast or Medium variants.***"

A short-lived pressure burst may noticeably move UO(5,10,15) while having only a modest effect on UO(10,20,40).

That difference is expected.

---

### Comparing the Three Variants

| Comparison | :violet-background[UO(5,10,15) — Fast] | :violet-background[UO(7,14,28) — Classic / Medium] | :violet-background[UO(10,20,40) — Slow] |
| --- | --- | --- | --- |
| **Responsiveness** | Most responsive; recent pressure changes affect it fastest | Intermediate responsiveness; balances sensitivity and smoothing | Smoothest / slowest; requires more persistent pressure to move materially |
| **Watch Thresholds** | Bullish: :blue-background[UO < 30] <br> Bearish: :blue-background[UO > 70] | Bullish: :blue-background[UO < 35] <br> Bearish: :blue-background[UO > 70] | Bullish: :blue-background[UO < 35] <br> Bearish: :blue-background[UO > 70] |
| **Signal Frequency** | Generally more frequent state changes and shorter-lived setups | Generally between Fast and Slow | Generally fewer state changes and more persistent setups |
| **When Most Useful** | Detecting shorter-term pressure shifts and earlier changes in reversal structure | General-purpose UO interpretation with the classic Williams balance | Evaluating broader, smoother, more persistent pressure structure |

---
The three variants use the same conceptual model (:gray-background[Extreme → Divergence → Confirmation]) but operate at different speeds.


#### Responsiveness

A useful hierarchy is:
- :gray-background[UO(5,10,15) → most responsive]
- :gray-background[UO(7,14,28) → intermediate]
- :gray-background[UO(10,20,40) → smoothest / slowest]

'Shorter' lookbacks allow recent pressure changes to affect the oscillator more quickly.
'Longer' lookbacks dilute a single recent move across a larger historical window.

This means the same stock can legitimately show different UO values and different staged states across the three variants on the same date.

---

#### Watch Thresholds

The bullish Watch thresholds are:

| UO variant | Bullish Watch rule |
| --- | --- |
| :violet-background[UO(5,10,15)] | :blue-background[UO < 30] |
| :violet-background[UO(7,14,28)] | :blue-background[UO < 35] |
| :violet-background[UO(10,20,40)] | :blue-background[UO < 35] |

The bearish Watch threshold is the same for all three: :blue-background[UO > 70]

The Fast variant uses the lower bullish threshold because its shorter construction is more reactive and reaches lower values more readily during short-term downside pressure.

The Medium and Slow variants use 35 to identify a meaningful downside extreme without requiring the same depth of short-term compression.

---

#### Signal Frequency

Because the variants respond at different speeds, they should not be expected to generate the same number of Watch, Divergence, or Confirmed observations.

In general:

- the Fast variant will tend to produce more frequent state changes;
- the Medium variant will tend to sit between Fast and Slow;
- the Slow variant will tend to produce fewer, more persistent setups.

This does not mean that the Slow variant is inherently "better" or that the Fast variant is inherently "noisier" in every market condition.

It means the variants are solving the same problem at different temporal resolutions.

A fast setup may appear and resolve before the Slow variant has moved enough to enter an extreme zone.

Conversely, a Slow setup may remain structurally relevant after a Fast setup has already cycled through several state changes.

---

#### When Each Variant Is Most Useful

A practical way to think about the three variants is:

| Variant | Most useful for |
| --- | --- |
| :violet-background[UO(5,10,15)] | Detecting shorter-term pressure shifts and earlier changes in reversal structure |
| :violet-background[UO(7,14,28)] | General-purpose UO interpretation with the classic Williams balance |
| :violet-background[UO(10,20,40)] | Evaluating broader, smoother, more persistent pressure structure |

This is not a ranking.

It is a **time-horizon distinction**.

The appropriate interpretation depends on whether you care more about recent sensitivity or broader persistence.

---

#### Why the Three Variants Are Not Three Equal Votes

It is tempting to read the three variants like this:

> Two bullish variants + one neutral variant = bullish consensus.

That is **not** how the UO framework is designed.

Each variant is a separate measurement of the same buying-pressure concept using different time windows.

Their disagreement is often useful information.

For example:

- :violet-background[UO(5,10,15)]: :green-background[Bullish Setup (Watch)]
- :violet-background[UO(7,14,28)]: :green-background[No Active Setup]
- :violet-background[UO(10,20,40)]: :green-background[No Active Setup]

can mean:

> "***Recent pressure has weakened enough to create a short-horizon extreme, but the broader pressure structure has not yet deteriorated enough to produce the same condition in the slower variants.***"

Likewise:

- Fast may already have confirmed;
- Medium may still be in Divergence;
- Slow may still show No Active Setup.

That does not automatically indicate inconsistency.

It indicates that the pressure transition is appearing at different speeds.

A useful reading rule is:

> "***Treat agreement across variants as corroborating context, and disagreement as information about where the pressure change is appearing first — not as a voting system.***"

See also:

- [Pressure Mix 101](#pressure-mix-101)
- [The Staged Reversal Framework](#the-staged-reversal-framework)
- [Signal and Rule](#signal-and-rule)

---
## How UO Is Calculated
[Top](#ultimate-oscillator-at-a-glance)

The final Ultimate Oscillator value is built from **Buying Pressure** and **True Range** measured across three different time horizons.

The calculation follows this sequence:

:gray-background[Price data → Buying Pressure and True Range → Fast / Medium / Slow [pressure ratios](#pressure-ratio) → 4:2:1 weighting → Final UO]

The important idea is:

> "***UO is not a single-period momentum reading. It is a weighted blend of three buying-pressure ratios measured over different horizons.***"

That is also why the hover's [Pressure Mix](#pressure-mix-101) can reveal information that the final UO number alone cannot show.

---

### Buying Pressure

Buying Pressure, or BP, measures how far the current Close sits above the session's effective lower reference point.

The rule is:
> :blue-background[Buying Pressure = Current Close - min(Current Low, Previous Close)]

The lower reference is whichever is lower:
- the current session's Low; or
- the previous session's Close.

Using the 'Previous Close' allows the calculation to account for gaps.

This allows the calculation to account for overnight gaps rather than looking only at the current day's High-Low range.


#### Example — No Downside Gap

Suppose:

- Previous Close = 100
- Current Low = 98
- Current Close = 102

The lower reference is: :gray-background[min(98, 100) = 98]

So: :gray-background[Buying Pressure = 102 - 98 = 4]

In plain English:

> "***The stock closed 4 points above the lowest relevant reference for the session.***"

#### Example — Gap Up

Suppose:

- Previous Close = 100
- Current Low = 104
- Current Close = 105

Using only the current Low would ignore the overnight move from 100 to 104.

Instead: :gray-background[min(104, 100) = 100]

So: :gray-background[Buying Pressure = 105 - 100 = 5]

The prior Close becomes the lower reference because it captures the gap.

This is one reason UO uses the previous Close in both Buying Pressure and True Range.

---

### True Range

True Range, or TR, measures the session's **effective total price range while accounting for overnight gaps**.

The rule is:

> :red-background[True Range = max(Current High, Previous Close) - min(Current Low, Previous Close)]

The upper reference is whichever is higher:
- the current High; or
- the previous Close.

The lower reference is whichever is lower:
- the current Low; or
- the previous Close.

This makes True Range broader than simply ':gray[Current High - Current Low]' when a gap has occurred.



#### Example — No Material Gap

Suppose:
- Previous Close = 100
- Current High = 105
- Current Low = 98

Then: :gray-background[max(105, 100) = 105]
And: :gray-background[min(98, 100) = 98]

So: :gray-background[True Range = 105 - 98 = 7]

In this case, True Range is the same as the ordinary High-Low range.

#### Example — Gap Up

Suppose:

- Previous Close = 100
- Current High = 108
- Current Low = 104

The ordinary intraday range is only: :gray-background[108 - 104 = 4]

But that would ignore the overnight gap from 100 to 104.

True Range instead uses :gray-background[max(108, 100) = 108] and :gray-background[min(104, 100) = 100].
- So: :gray-background[True Range = 108 - 100 = 8]

In plain English:

> "***True Range expands the measured range when the previous Close lies outside the current session's High-Low range.***"

That is what allows UO's pressure calculation to remain sensitive to gap behavior.

---

### Fast, Medium, and Slow Pressure

UO does not use Buying Pressure from a single session by itself.

For each horizon, it sums Buying Pressure and True Range over the applicable lookback and divides the two totals.

The rules are:
- :blue-background[Fast Pressure = Sum(BP over Fast window) / Sum(TR over Fast window)]
- :blue-background[Medium Pressure = Sum(BP over Medium window) / Sum(TR over Medium window)]
- :blue-background[Slow Pressure = Sum(BP over Slow window) / Sum(TR over Slow window)]

These are the three component values displayed in [Pressure Mix](#pressure-mix).

For UO(7,14,28), for example:

- Fast = 7-session BP/TR ratio
- Medium = 14-session BP/TR ratio
- Slow = 28-session BP/TR ratio

Suppose the current component values are:

- Fast = 0.57
- Medium = 0.50
- Slow = 0.42

The interpretation is approximately:

- over the Fast horizon, accumulated Buying Pressure equals 57% of accumulated True Range;
- over the Medium horizon, accumulated Buying Pressure equals 50% of accumulated True Range;
- over the Slow horizon, accumulated Buying Pressure equals 42% of accumulated True Range.

The ordering is: :gray-background[0.57 > 0.50 > 0.42]

so [Pressure Mix](#pressure-mix) classifies the current structure as: :green-background[recent pressure strengthening]

The ratios themselves feed the final UO calculation.

Their **ordering** feeds the Pressure Mix interpretation.

Those are related but separate uses of the same three component values.

---

### The 4:2:1 Weighting

The three pressure horizons do not contribute equally to the final oscillator.

UO gives the greatest weight to the shortest horizon:
- :blue-background[Fast × 4]
- :blue-background[Medium × 2]
- :blue-background[Slow × 1]

The total weight is: :gray-background[4 + 2 + 1 = 7]

The final formula is therefore: :blue-background[UO = 100 × ((4 × Fast) + (2 × Medium) + Slow) / 7]

This design makes the oscillator more responsive to recent pressure while still retaining information from the medium- and longer-term components.

Using the prior example:

- Fast = 0.57
- Medium = 0.50
- Slow = 0.42

the weighted pieces are:
- :gray-background[4 × 0.57 = 2.28]
- :gray-background[2 × 0.50 = 1.00]
- :gray-background[1 × 0.42 = 0.42]

Add them: :gray-background[2.28 + 1.00 + 0.42 = 3.70]

Divide by the total weight: :gray-background[3.70 / 7 = 0.5286]

Scale to the familiar 0–100 UO range: :gray-background[0.5286 × 100 ≈ 52.86]

So the final oscillator is approximately: :gray-background[UO = 52.86]

---

### From Pressure Components to the Final UO Value

The full calculation can be summarized as:

1. Calculate session-level Buying Pressure.
2. Calculate session-level True Range.
3. Sum BP and TR over each of the three horizons.
4. Divide each BP sum by its matching TR sum.
5. Weight Fast, Medium, and Slow by 4:2:1.
6. Divide the weighted total by 7.
7. Multiply by 100.

In formula form:

> :blue-background[BP = Close - min(Low, Previous Close)]

> :blue-background[TR = max(High, Previous Close) - min(Low, Previous Close)]

> :blue-background[Fast = Sum(BP, Fast) / Sum(TR, Fast)]

> :blue-background[Medium = Sum(BP, Medium) / Sum(TR, Medium)]

> :blue-background[Slow = Sum(BP, Slow) / Sum(TR, Slow)]

> :blue-background[UO = 100 × ((4 × Fast) + (2 × Medium) + Slow) / 7]

For the three app variants, the same calculation is used with different lookback windows:

| Variant | Fast | Medium | Slow |
| --- | ---: | ---: | ---: |
| :violet-background[UO(5,10,15)] | 5 | 10 | 15 |
| :violet-background[UO(7,14,28)] | 7 | 14 | 28 |
| :violet-background[UO(10,20,40)] | 10 | 20 | 40 |

See [The Three UO Variants](#the-three-uo-variants) for how those window lengths affect responsiveness and interpretation.

---

### Why Pressure Mix Adds Information Beyond the Final UO Number

The final UO value compresses three component ratios into **one weighted number**.

That is useful for scoring and threshold logic, but compression inevitably hides some of the internal structure.

Consider two hypothetical observations.

${\textbf{Observation A}}$:

- Fast = 0.57
- Medium = 0.50
- Slow = 0.42

The ordering is :red-background[Fast > Medium > Slow] so :violet-background[Pressure Mix] is: :green-background[recent pressure strengthening]

Its final UO is approximately: :gray-background[52.86]

${\textbf{Observation B}}$:

Suppose another observation produces a similar blended UO value, but its component ordering is mixed.

For example:

- Fast = 0.50
- Medium = 0.56
- Slow = 0.45

The three horizons no longer form :gray-background[Fast > Medium > Slow] or :gray-background[Fast < Medium < Slow].
- So :violet-background[Pressure Mix] is :green-background[mixed / transitional].

Even if the final UO values are fairly close, the internal pressure structures are different.

Observation A says:

> "***Recent pressure is leading the broader horizons in a clean strengthening sequence.***"

Observation B says:

> "***The three horizons are not aligned in a clean strengthening or weakening sequence.***"

That is the value of exposing Pressure Mix separately.

The final UO answers:

> "***What is the weighted three-horizon pressure reading?***"

[Pressure Mix](#pressure-mix) answers:

> "***How are those three pressure horizons arranged underneath that final number?***"

Neither replaces the other.

Together, they make the oscillator more interpretable.

See also:

- [Pressure Mix 101](#pressure-mix-101)
- [The Three UO Variants](#the-three-uo-variants)
- [The Staged Reversal Framework](#the-staged-reversal-framework)

---

## Worked Heatmap Examples
[Top](#ultimate-oscillator-at-a-glance)

The examples below show how the UO fields fit together on real observations from the production-path validation set.

The goal is not to repeat every field definition.

Instead, each example answers:

> "***What would I actually conclude from this combination of cell, hover, lifecycle state, and rule?***"

For field definitions, use the inline references throughout the examples.

---

### MSFT — Bullish Divergence Pending Confirmation

This example uses the 'Medium / Classic' variant: [UO(7,14,28)](#uo-7-14-28-classic-medium)

The qualifying [bullish divergence](#active---bullish-bullish-divergence) was built from:
- :violet-background[Prior]: 9/6/22, $251.94, UO 27.88
- :violet-background[Current]: 9/30/22, $232.73, UO 37.34
- :violet-background[Divergence Event]: 10/4/22

The bullish confirmation trigger was approximately :gray-background[51.74].

On 10/4/22, the divergence was active but had not yet confirmed.

---

#### Reading the Cell (Bullish Divergence Pending Confirmation)

The important cell-level information is:

- [heatmap score](#heatmap-score): $\small{\fcolorbox{none}{lightgreen}{\textsf{+1}}}$
- active bullish divergence diamond: $\large{\textcolor{blue}{\textsf{◆}}}$

That combination tells you:

> "***A bullish setup is active, but it has not yet reached the Confirmed state.***"

The diamond matters because $\small{\fcolorbox{none}{lightgreen}{\textsf{+1}}}$ can represent either:

- [Bullish Setup (Watch)](#bullish-watch-signal); or
- [Bullish Setup (Divergence)](#bullish-divergence-signal)

The diamond identifies the second case.

See [Divergence 101](#divergence-101).

---

#### Reading the Hover (Bullish Divergence Pending Confirmation)

The key hover fields are:

- :violet-background[Divergence]: :green-background[Active - Bullish]
- :violet-background[Classic Confirmation]: :green-background[Pending]
- :violet-background[Signal]: :green-background[Bullish Setup (Divergence)]

The divergence structure is: :gray-background[$251.94 → $232.73 = lower price low]
- while UO moved: :gray-background[27.88 → 37.34 = higher UO low]

- So price weakened to a new confirmed swing low while UO did not become as weak as it had at the prior swing low.

That is the bullish divergence.

The earlier UO pivot of :gray-background[27.88] also satisfies the Medium variant's qualifying bullish extreme rule: :blue-background[UO < 35].

The setup therefore contains both:
1. the required price/UO divergence structure; and
2. the required oversold involvement.

---

#### Why the Signal Is Bullish Setup (Divergence)

The Signal is not merely: :green-background[Bullish Setup (Watch)] because a higher-priority confirmed-pivot divergence is already active.

The precedence rule is: :red-background[Divergence > Watch]

So the app reports :violet-background[Signal]: :green-background[Bullish Setup (Divergence)] even if the current UO value is no longer below the Watch threshold.

The key distinction is:

> "***The Watch condition is about current extremity. The Divergence condition is about a qualifying structure that has already formed.***"

See: [State Precedence](#state-precedence)
**References**:
- [Bullish Setup (Watch)](#bullish-watch-signal); or
- [Bullish Setup (Divergence)](#bullish-divergence-signal)
- [Bullish Confirmed](#bullish-confirmed-signal)
- [No Active Setup](#no-active-setup-signal)
- [Bearish Setup (Watch)](#bearish-watch-signal)
- [Bearish Setup (Divergence)](#bearish-divergence-signal)
- [Bearish Confirmed](#bearish-confirmed-signal)

---

#### What Would Confirm the Setup (Bullish Divergence Pending Confirmation)

The [bullish Classic Confirmation](#bullish-confirmed) ['trigger'](#understanding-the-trigger) was approximately: :gray-background[51.74]

The confirmation rule was: :blue-background[current UO > 51.74]

Equality would not be enough.

The setup would remain Pending until UO moved strictly above the trigger within the allowed [confirmation window](#confirmation-window).

That happened on the following session, 10/5/22.

The state therefore progressed:
- from: :gray-background[10/4/22 → Bullish Setup (Divergence)]
- to: :gray-background[10/5/22 → Bullish Confirmed]

See [Classic Confirmation 101](#classic-confirmation-101).

---

### XLP — Bullish Confirmation

This example uses the Slow variant: [UO(10,20,40)](#uo-10-20-40-slow)

On 1/21/25:

- UO = 38.1607
- bullish confirmation trigger = 36.4752
- the divergence became knowable and confirmed on the same session

Because :gray-background[38.1607 > 36.4752] the strict bullish confirmation rule was satisfied immediately.

---

#### Reading the Cell (Bullish confirmation)

The cell should be read as a Confirmed event:

- heatmap score: $\small{\fcolorbox{none}{Green}{\textcolor{white}{\textsf{+2}}}}$
- :violet-background[Signal]: :green-background[Bullish Confirmed]

There is no need for the active divergence diamond to remain the primary visual cue because the setup has already advanced to the higher-precedence Confirmed state.

The relevant precedence rule is: :red-background[Confirmed > Divergence]

---

#### Reading the Hover (Bullish confirmation)

The key lifecycle information is:

- :violet-background[Classic Confirmation]: :green-background[Bullish Confirmed]
- Trigger: 36.48
- Event: 1/21/25
- :violet-background[Signal]: :green-background[Bullish Confirmed]

The important point is that the [Divergence Event](#divergence-event) and [Confirmation Event](#confirmation-event) occurred on the same session.

That is valid because the confirmation search begins on the Divergence [Event](#event) date itself.

The rule is: :red-background[Event lag 0 is eligible for confirmation]

So a setup does not need to spend at least one full day in the displayed Divergence state before reaching Confirmed.

See [Same-Day Divergence and Confirmation](#same-day-divergence-and-confirmation).

---

#### Why Confirmation Can Occur Outside the Extreme Zone

The current UO value was: :gray-background[38.1607]
For the Slow variant, bullish Watch requires: :blue-background[UO < 35]
- So the current value was no longer inside the [Bullish Watch](#bullish-watch-signal) zone.

That does not invalidate the bullish confirmation.

The qualifying oversold condition belonged to the earlier two-pivot divergence structure.

By the time confirmation occurs, UO is expected to have recovered from that earlier weakness.

In fact, a [bullish confirmation](#bullish-confirmed-signal) generally requires UO to rise enough to break above the divergence trigger.

So:

> "***The extreme helps create the setup. It does not need to remain present when the setup confirms.***"

See [Zone and Watch](#zone-and-watch).

---

### XLY — Bullish Confirmation While Zone Is Overbought

This example uses the Fast variant: [UO(5,10,15)](#uo-5-10-15-fast)

On 8/7/24:

- UO = 83.8674
- bullish confirmation trigger = 47.7916
- the divergence became knowable and confirmed on the same session
- the current Zone was Overbought

Because :gray-background[83.87 > 47.79], the bullish confirmation condition was satisfied.

At the same time: :gray-background[83.87 > 70]

so the current [Zone](#zone) was: :violet-background[Zone]: :green-background[Overbought]

The final Signal was still :violet-background[Signal]: :green-background[Bullish Confirmed] with [heatmap score](#heatmap-score): $\small{\fcolorbox{none}{Green}{\textcolor{white}{\textsf{+2}}}}$

---

#### Why This Is Not a Contradiction

At first glance:

- :violet-background[Zone]: :green-background[Overbought]
- :violet-background[Signal]: :green-background[Bullish Confirmed]

can look inconsistent.

It is not.

The two fields describe different time dimensions.

:violet-background[Zone] describes:

> "***Where is UO right now?***"

:violet-background[Signal] describes:

> "***What is the highest-priority active staged-reversal event?***"

The bullish divergence developed from an earlier downside structure.

By 8/7/24, UO had recovered so strongly that it not only crossed the bullish confirmation trigger, but had already moved above 70.

So the correct interpretation is:

> "***The earlier bullish reversal setup has just confirmed, while the current oscillator reading has already advanced into an overbought zone.***"

The current overbought condition does not retroactively erase the bullish setup that produced the Confirmed event.

See [Why the Current Zone Can Differ from the Active Signal](#why-the-current-zone-can-differ-from-the-active-signal).

---

#### How Precedence Explains the Result

On the confirmation session, more than one condition may be true.

For example:

- current UO may satisfy the bearish Watch threshold because :blue-background[UO > 70];
- the earlier bullish divergence may simultaneously satisfy its bullish confirmation trigger.

The app does not resolve this by treating the fields as votes.

It uses the staged-state precedence rule:

:blue-background[Confirmed > Divergence > Watch > No Active Setup]

Therefore, the displayed Signal is: [Bullish Confirmed](#bullish-confirmed-signal)
Not: [Bearish Setup (Watch)](#bearish-watch-signal)

The [Zone](#zone-outcomes) still displays [Overbought](#overbought) because it remains factually true about the current UO value.

This is a concrete example of why:

> "***Zone and Signal should be interpreted together, not forced to agree.***"

---

### MSFT — Expired Bullish Divergence

This example uses the 'Medium / Classic' variant [UO(7,14,28)](#uo-7-14-28-classic-medium).

For the relevant 2025 setup:

- bullish confirmation trigger = 60.0896
- the setup ultimately expired without confirming
- by 12/15/25, the divergence was no longer an active setup

The hover therefore reflected the expired lifecycle rather than preserving the old bullish divergence indefinitely.

---

#### What Expired Means

A divergence has a bounded [confirmation window](#confirmation-window).

The valid confirmation range is:

:blue-background[Event lag 0 through Event lag 10, inclusive]

If UO does not strictly cross the confirmation trigger during that period, the setup [expires](#expired) before the following session.

So:

:violet-background[Classic Confirmation]: :green-background[Expired]

means:

> "***The divergence was valid, but it did not complete the required confirmation step within the allowed time.***"

It does not mean the divergence was incorrectly detected.

It means the setup failed to progress in time.

See [Expiry and Stale-Setup Prevention](#expiry-and-stale-setup-prevention).

---

#### Why the Old Setup Does Not Reactivate Later

Once the setup expires, its old trigger (:gray-background[60.09]) becomes stale.

A later UO move above that value does not revive the old divergence.

The rule is: :red-background[an expired setup cannot later confirm from its old trigger]

This matters because UO may cross many historical levels months later for completely different reasons.

Allowing an old divergence to reactivate would make the event difficult to interpret and would disconnect the confirmation from the market structure that originally created it.

The correct lifecycle is: :gray-background[Divergence → Pending → Expired → finished]
Not: :gray-background[Divergence → Pending → Expired → months later Confirmed]

A new Confirmed state requires a new qualifying divergence structure.

That is why a later crossing of the old 60.0896 trigger does not resurrect the 2025 MSFT setup.

See also:

- [Divergence 101](#divergence-101)
- [Classic Confirmation 101](#classic-confirmation-101)
- [The Staged Reversal Framework](#the-staged-reversal-framework)

---
## Practical Reading Guide
[Top](#ultimate-oscillator-at-a-glance)

This section turns the UO framework into a repeatable reading process.

The goal is not to memorize every field.

It is to answer:

> "***What should I look at first, what should I look at next, and how do I avoid over-interpreting a single UO field?***"

The most useful habit is to separate:

- the **active staged-reversal state**;
- the **current oscillator location**;
- the **supporting pressure context**.

A practical hierarchy is:

:gray-background[Signal → Divergence / Confirmation → Zone → Pressure Bias → Pressure Mix]

That order keeps the strongest semantic state at the center of the interpretation while still using the contextual fields to explain what is happening underneath it.

---

### A Simple Reading Sequence

A useful UO reading sequence is:

1. Read :violet-background[Signal](#signal-and-rule).
2. Check :violet-background[Divergence](#divergence-101).
3. Check :violet-background[Classic Confirmation](#classic-confirmation).
4. Read :violet-background[Zone](#zone).
5. Read :violet-background[Pressure Bias](#pressure-bias).
6. Read :violet-background[Pressure Mix](#pressure-mix).
7. Use :violet-background[Rule] to verify why the Signal was assigned.

Each step answers a different question.

See Also:
- [What to Focus on First](#what-to-focus-on-first)
- [One-Screen Mental Model](#one-screen-mental-model)

#### Step 1 — Start with Signal

:violet-background[Signal] is the best first field because it identifies the highest-priority active UO state.

It tells you whether the current observation is:
- [Bullish Setup (Watch)](#bullish-watch-signal); or
- [Bullish Setup (Divergence)](#bullish-divergence-signal)
- [Bullish Confirmed](#bullish-confirmed-signal)
- [No Active Setup](#no-active-setup-signal)
- [Bearish Setup (Watch)](#bearish-watch-signal)
- [Bearish Setup (Divergence)](#bearish-divergence-signal)
- [Bearish Confirmed](#bearish-confirmed-signal)

Start here before trying to infer the setup from the raw UO value alone.

See [Signal and Rule](#signal-and-rule).

#### Step 2 — Check Divergence

If the Signal is a Divergence state, :violet-background[Divergence] shows the structure that created it.

Look for:

- :green-background[Active - Bullish]
- :green-background[Active - Bearish]
- or :green-background[None]

If active, use the Prior / Current / Event values to reconstruct the confirmed-pivot relationship.

See [Divergence 101](#divergence-101).

#### Step 3 — Check Classic Confirmation

:violet-background[Classic Confirmation] tells you whether the divergence is:

- still :green-background[Pending];
- already :green-background[Bullish Confirmed];
- already :green-background[Bearish Confirmed];
- :green-background[Expired];
- or not applicable, :green-background[None].

This is where you determine whether the setup is still waiting, has triggered, or has gone stale.

See [Classic Confirmation 101](#classic-confirmation-101).

#### Step 4 — Read Zone

:violet-background[Zone] tells you where the current UO value sits relative to the active variant's extreme thresholds.

Possible outcomes are:

- :green-background[Oversold]
- :green-background[Overbought]
- :green-background[Neither Extreme]

Do not use Zone as a replacement for Signal.

A valid divergence or Confirmed event can remain the active staged state even when current Zone is no longer extreme.

See [Zone and Watch](#zone-and-watch).

#### Step 5 — Read Pressure Bias

:violet-background[Pressure Bias] tells you whether the current blended UO reading is:

- :green-background[Positive]
- :green-background[Negative]
- :green-background[Balanced]

A fresh midpoint crossover may also display:

- $\large{\textcolor{blue}{\textsf{▲}}}$ for Cross Above 50
- $\large{\textcolor{Red}{\textsf{▼}}}$ for Cross Below 50

Use this as directional context around the staged setup.

See [Pressure Bias and the 50-Line Crossover](#pressure-bias-and-the-50-line-crossover).

#### Step 6 — Read Pressure Mix

:violet-background[Pressure Mix] tells you whether the current Fast / Medium / Slow [pressure ratios](#pressure-ratio) are:

- :green-background[recent pressure strengthening]
- :green-background[recent pressure weakening]
- :green-background[mixed / transitional]

This gives you a view inside the blended UO value.

Use it to understand whether recent pressure is leading or lagging the broader pressure structure.

See [Pressure Mix](#pressure-mix).

#### Step 7 — Use Rule as the Audit Trail

:violet-background[Rule] is the quickest way to verify why the current Signal exists.

For example:

- Watch → threshold rule
- Divergence → confirmed-pivot price/UO disagreement + [qualifying extreme](#qualifying-extreme)
- Confirmed → qualifying divergence + confirmation trigger break
- No Active Setup → no Watch, Divergence, or Confirmed state active

A useful habit is:

> "***If the Signal surprises you, read Rule before assuming the classification is inconsistent.***"

See [Signal and Rule](#signal-and-rule).

---

### Common UO Combinations

The UO fields are designed to be interpreted together.

The combinations below are useful because they show how apparently different field directions can still be internally consistent.

---
#### Watch + Strengthening Pressure Mix

Example:

- :violet-background[Signal]: [Bullish Setup (Watch)](#bullish-watch-signal)
- :violet-background[Pressure Mix]: [recent pressure strengthening](#recent-pressure-strengthening)

Interpretation:

> "***UO is currently in a bullish Watch zone, and recent buying pressure is stronger than the medium- and longer-horizon pressure underneath it.***"

This can be read as:

- an extreme condition exists; and
- the short-horizon pressure structure is already improving.

It does **not** mean a bullish divergence exists.

It also does not mean confirmation has occurred.

The setup is still at the Watch stage.

See [Pressure Mix](#pressure-mix).

---

#### Watch + Weakening Pressure Mix

Example:

- :violet-background[Signal]: [Bullish Setup (Watch)](#bullish-watch-signal)
- :violet-background[Pressure Mix]: [recent pressure weakening](#recent-pressure-weakening)

Interpretation:

> "***UO is low enough to create a bullish Watch, but recent buying pressure is still weaker than the broader pressure structure.***"

That combination can occur because Watch is based on the current UO extreme, while Pressure Mix describes the internal ordering of Fast, Medium, and Slow pressure.

The Pressure Mix does not cancel the Watch.

It simply adds context about the quality of the current pressure structure.

---

#### Divergence + Positive Pressure Bias

Example:

- :violet-background[Signal]: [Bullish Setup (Divergence)](#bullish-divergence-signal)
- :violet-background[Pressure Bias]: [Positive](#positive-pressure-bias)

Interpretation:

> "***A qualifying bullish divergence is active, and the blended UO value is already above 50.***"

That can happen if UO has recovered materially after the pivot structure formed but has not yet crossed the specific Classic Confirmation trigger.

Positive Pressure Bias is therefore supportive context, but it is not the confirmation rule.

The setup remains Divergence until: :red-background[current UO > bullish confirmation trigger]

See [Classic Confirmation 101](#classic-confirmation-101).

---

#### Divergence + Fresh 50-Line Crossover

Example:

- :violet-background[Signal]: [Bullish Setup (Divergence)](#bullish-divergence-signal)
- :violet-background[Pressure Bias]: :green-background[Positive] $\large{\textcolor{blue}{\textsf{▲}}}$

Interpretation:

> "***A bullish divergence is active, and UO crossed above 50 during the current session.***"

This adds fresh positive midpoint context.

But the 50-line crossover does not promote the setup to Bullish Confirmed.

The confirmation rule is still the divergence-specific trigger.

In other words, :gray-background[Cross Above 50 ≠ Classic Confirmation] unless the confirmation trigger itself happens to be crossed on the same session.

See [Pressure Bias and the 50-Line Crossover](#pressure-bias-and-the-50-line-crossover).

---

#### Confirmed + Opposite Current Zone

Example:

- :violet-background[Zone]: [Overbought](#overbought)
- :violet-background[Signal]: [Bullish Confirmed](#bullish-confirmed-signal)

Interpretation:

> "***The earlier bullish divergence has just completed its confirmation step, while the current UO reading has already advanced into the overbought zone.***"

This is not contradictory.

- 'Zone' describes the current oscillator location.
- 'Signal' describes the highest-priority staged-reversal event.

See [Why the Current Zone Can Differ from the Active Signal](#why-the-current-zone-can-differ-from-the-active-signal).

---

#### No Active Setup + Meaningful Context

Example:

- :violet-background[Signal]: [No Active Setup](#no-active-setup-signal)
- :violet-background[Pressure Bias]: [Positive](#positive-pressure-bias)
- :violet-background[Pressure Mix]: [recent pressure strengthening](#recent-pressure-strengthening)

Interpretation:

> "***There is no active UO reversal setup, but current pressure context is constructive.***"

This is an important distinction.

No Active Setup does **not** mean:

- UO has no directional information;
- Pressure Bias must be Balanced;
- Pressure Mix must be mixed;
- the oscillator is uninformative.

It means only that no Watch, Divergence, or Confirmed staged-reversal state currently has precedence.

---

### What to Focus on First

If you want the shortest possible UO reading workflow, focus on four things:

1. [Signal](#signal)
2. [Divergence](#divergence)
3. [Classic Confirmation](#classic-confirmation)
4. [Rule](#rule)

Those four fields tell you:

- what the active state is;
- whether a qualifying divergence exists;
- whether that divergence has confirmed or expired;
- why the state was assigned.

Then use:

- [Zone](#zone)
- [Pressure Bias](#pressure-bias)
- [Pressure Mix](#pressure-mix)

to add current context.

A compact mental model is:

> "***Signal tells you the state. Divergence and Confirmation tell you the lifecycle. Zone, Pressure Bias, and Pressure Mix tell you the context. Rule tells you why.***"

That ordering helps prevent two common interpretation errors:

1. treating every UO field as an equal vote;
2. treating the current raw UO value as though it fully determines the staged Signal.

See also:

- [Signal and Rule](#signal-and-rule)
- [The Staged Reversal Framework](#the-staged-reversal-framework)
- [Worked Heatmap Examples](#worked-heatmap-examples)
- [A Simple Reading Sequence](#a-simple-reading-sequence)
- [One-Screen Mental Model](#one-screen-mental-model)


---
## Limitations, Warmup, and Interpretation Boundaries
[Top](#ultimate-oscillator-at-a-glance)

The UO framework is designed to make reversal structure more explicit, but it still has important boundaries.

This section explains what the model does **not** know, what it intentionally delays, and which observations should not be over-interpreted.

A useful principle is:

> "***The UO framework organizes evidence. It does not remove uncertainty.***"

---

### Missing Is Not Neutral

A missing UO observation is **not** the same thing as:

- :violet-background[Signal]: :green-background[No Active Setup]
- :violet-background[Pressure Bias]: :green-background[Balanced]
- :violet-background[Pressure Mix]: :green-background[mixed / transitional]

Missing means the model does not yet have enough valid underlying data to calculate the relevant UO context.

That distinction matters most during warmup.

Each UO variant requires enough history to calculate its longest pressure horizon.

The Slow variant therefore requires more history than the Fast variant.

Conceptually:

:gray-background[Insufficient history ≠ No Active Setup]

The app should not treat an unavailable value as a valid neutral state.

This preserves the difference between:

> "***No signal is active***"

and:

> "***The signal cannot yet be evaluated.***"

---

### Pivot Confirmation Is Delayed by Design

UO divergence uses confirmed five-bar pivots.

A candidate pivot needs:

- two earlier trading sessions; and
- two later trading sessions.

The rule is conceptually:

:blue-background[two sessions before + pivot session + two sessions after]

This means a pivot cannot be known on the day it occurs.

For example: :gray-background[Friday = eventual pivot low] cannot be confirmed until two later trading sessions have occurred.

That delay is intentional.

It prevents the system from claiming knowledge that was not yet available in real time.

The consequence is:

> "***The pivot date marks where the swing occurred. The [Divergence Event](#divergence-event) date marks when the app could legitimately know it was a confirmed swing.***"

See [Divergence](#divergence)

---

### No Back-Painting

The app does not retroactively place a divergence signal on the original pivot date.

If a Current pivot occurs on one date and becomes confirmable two sessions later, the divergence begins on the later Event date.

The rule is: :orange-background[Divergence state begins on the Event date, not the Current pivot date]

This avoids back-painting.

Back-painting would make historical charts look cleaner than the information actually available at the time.

For example:
:gray-background[Current pivot = 9/30/22] AND :gray-background[Divergence Event = 10/4/22] means the divergence becomes actionable on 10/4/22.

It should not be displayed as though it had been known on 9/30/22.

See [Why the Event Date Comes After the Pivot Date](#why-the-event-date-comes-after-the-pivot-date).

---

### Extreme Does Not Mean Reversal

An extreme UO reading creates a Watch condition.

It does not establish that price has already bottomed or topped.

Bullish Watch rules are:

- Fast: :blue-background[UO < 30]
- Medium: :blue-background[UO < 35]
- Slow: :blue-background[UO < 35]

Bearish Watch rule:

- all variants: :blue-background[UO > 70]

Those rules mean only that UO has entered a reversal-monitoring zone.

They do **not** mean:

- price must reverse immediately;
- a divergence exists;
- confirmation has occurred.

A strong trend can keep UO extreme for multiple sessions.

So:

> "***Extreme means 'pay attention,' not 'the reversal is complete.'***"

See [Zone and Watch](#zone-and-watch).

---

### Divergence Does Not Mean Reversal

A qualifying divergence is stronger evidence than Watch, but it is still a setup.

Bullish divergence requires:

:blue-background[price lower confirmed low + UO higher pivot low + qualifying oversold involvement]

Bearish divergence requires:

:blue-background[price higher confirmed high + UO lower pivot high + qualifying overbought involvement]

That structure says price and UO are no longer confirming one another at the relevant swing points.

It does **not** guarantee that price will reverse.

The setup can remain Pending and later expire.

That is why the framework includes [Classic Confirmation 101](#classic-confirmation-101).

A useful interpretation is:

> "***Divergence identifies a structural disagreement. Confirmation tests whether UO actually follows through.***"

---

### Confirmation Does Not Guarantee Price Reversal

Bullish Confirmed and Bearish Confirmed are the strongest UO states in the model.

But they still describe **completion of the UO rule sequence**, not certainty about future price.

- Bullish confirmation means: :blue-background[current UO > bullish confirmation trigger within the allowed window]
- Bearish confirmation means: :blue-background[current UO < bearish confirmation trigger within the allowed window]

That is stronger than Watch or Divergence because the setup has progressed through the full framework.

It still does **not** mean:

- price must reverse immediately;
- price cannot retest the prior extreme;
- the move cannot fail;
- another indicator must agree.

The correct interpretation is:

> "***Confirmed means the UO reversal setup completed its defined trigger condition. It does not mean the subsequent price path is guaranteed.***"

See [Classic Confirmation 101](#classic-confirmation-101).

---

### Context Fields Do Not Override the Primary Signal

:violet-background[Pressure Bias] and :violet-background[Pressure Mix] are contextual fields.

They help explain what the oscillator is doing internally.

They do not override the staged-reversal state.

For example:

- :violet-background[Signal]: :green-background[Bullish Setup (Divergence)]
- :violet-background[Pressure Bias]: :green-background[Negative]
- :violet-background[Pressure Mix]: :green-background[recent pressure weakening]

is still a bullish divergence setup.

The context says:

> "***Current pressure is still weak.***"

The Signal says:

> "***A qualifying bullish divergence is the highest-priority active staged-reversal state.***"

Likewise:

- :violet-background[Signal]: :green-background[Bullish Confirmed]
- :violet-background[Zone]: :green-background[Overbought]

remains Bullish Confirmed because:

:blue-background[Confirmed > Divergence > Watch > No Active Setup]

The fields should be read together, not treated as competing votes.

See:

- [Pressure Bias and the 50-Line Crossover](#pressure-bias-and-the-50-line-crossover)
- [Pressure Mix 101](#pressure-mix-101)
- [State Precedence](#state-precedence)

---

### Why Expiry Matters

Expiry prevents an old divergence from remaining actionable forever.

The valid confirmation interval is: :orange-background[Event lag 0 through Event lag 10, inclusive]

If the trigger is not crossed within that period, the setup expires before the following session.

Once expired:

- the divergence is no longer active;
- the old Trigger is stale;
- a later crossing of that old Trigger cannot revive the setup.

Conceptually: :gray-background[Divergence → Pending → Expired → finished]

NOT: :gray-background[Divergence → Pending → Expired → later reactivated]

Without expiry, a divergence from weeks or months earlier could appear to "confirm" long after the market structure that created it had lost relevance.

Expiry therefore protects interpretability.

It keeps the [confirmation event](#confirmation-event) tied to the divergence that actually generated it.

See [Expiry and Stale-Setup Prevention](#expiry-and-stale-setup-prevention).

---

## Glossary and Quick Reference
[Top](#ultimate-oscillator-at-a-glance)

This glossary is designed for **fast lookup**, not to replace the detailed sections above.

Each term includes a short definition and an inline reference to the section where the concept is explained in more detail.

Where a glossary heading would otherwise duplicate an existing heading elsewhere in the document, **II** has been added to the glossary heading so the Markdown anchor remains unambiguous.

---
### Confirmed

'Confirmed' means:
- "***That qualifying divergence has subsequently crossed its [Classic Confirmation trigger](#confirmation-trigger)***".
- It's saying: **That [divergence](#divergence) also crossed its required [confirmation trigger](#confirmation-trigger) in time.**


> "Bullish confirmation" means: :blue-background[current UO > bullish confirmation trigger within the allowed window]
> "Bearish confirmation" means: :blue-background[current UO < bearish confirmation trigger within the allowed window]

See: [confirmation event](#confirmation-event); [confirmation window](#confirmation-window); [confirmation trigger](#confirmation-trigger)
Related: [What 'confirmation' does and does not mean](#what-confirmation-does-and-does-not-mean); [Confirmed over Divergence](#confirmed-over-divergence); [Confirmed 5-bar Pivots](#confirmed-five-bar-pivots)
[Confirmation Does Not Guarantee Price Reversal](#confirmation-does-not-guarantee-price-reversal)

---

### 50-Line Crossover

A current-session event showing that UO changed sides of its 50 midpoint.
- **Cross Above 50**: :blue-background[prior UO <= 50 and current UO > 50]
- **Cross Below 50**: :blue-background[prior UO >= 50 and current UO < 50]

The crossover is shown with $\large{\textcolor{blue}{\textsf{▲}}}$ or $\large{\textcolor{Red}{\textsf{▼}}}$ and is context only; it is not Classic Confirmation.

See [50-Line Crossover Events](#50-line-crossover-events); [Pressure Bias and the 50-Line Crossover](#pressure-bias-and-the-50-line-crossover)

---

### Pressure Ratio

A Pressure Ratio is the accumulated Buying Pressure divided by accumulated True Range over one UO horizon.

For example: :blue-background[Fast Pressure = Sum(BP over Fast window) / Sum(TR over Fast window)]

The same structure is used for Medium and Slow.

These three ratios are the values shown in [Pressure Mix](#pressure-mix) and are also the inputs to the final weighted UO calculation.

See [Fast, Medium, and Slow Pressure](#fast-medium-and-slow-pressure).

---

### Pivot

A confirmed five-bar swing point used in the UO divergence logic.

A pivot uses: :blue-background[two sessions before + pivot session + two sessions after]

A pivot low must be lower than the two preceding and two following lows; a pivot high must be higher than the two preceding and two following highs.

Because two future sessions are required, a pivot is not knowable on the pivot date itself.

See [Confirmed Five-Bar Pivots](#confirmed-five-bar-pivots).

---

### Prior Pivot

The **earlier confirmed price [pivot](#pivot)** used in a divergence comparison.

The hover's :violet-background[Prior] information includes:

- pivot date;
- price at the pivot;
- UO value on the same date.

The Prior Pivot is compared with the [Current Pivot](#current-pivot) to determine whether price and UO diverged.

See [Understanding Prior, Current, and Event](#understanding-prior-current-and-event).

---

### Current Pivot

The **newer confirmed price [pivot](#pivot)** used in the divergence comparison.

The hover's :violet-background[Current] information includes:
- pivot date;
- price at the pivot;
- UO value on the same date.

The Current Pivot occurs before the [Divergence Event](#divergence-event) because two later trading sessions are required to confirm it.

See [Understanding Prior, Current, and Event](#understanding-prior-current-and-event); [Prior Pivot](#prior-pivot)

---

### Qualifying Extreme

The extreme UO reading required for a price/UO divergence to qualify as a staged reversal setup.

Bullish divergence requires at least one of the two UO pivot lows to satisfy the active variant's bullish extreme threshold.

Bearish divergence requires at least one of the two UO pivot highs to satisfy:

:blue-background[UO > 70]

The current UO value does not have to remain extreme after the divergence becomes active.

See [The Qualifying Extreme Requirement](#the-qualifying-extreme-requirement).

---

### Divergence Event

The date on which the newer confirmed five-bar pivot becomes **knowable**, allowing the divergence to be emitted without future information.

It is generally two trading sessions after the Current Pivot date.

The Divergence Event starts the active divergence lifecycle and the confirmation window.

See [Understanding Prior, Current, and Event](#understanding-prior-current-and-event) and [Why the Event Date Comes After the Pivot Date](#why-the-event-date-comes-after-the-pivot-date).
Related: [Confirmation Event](#confirmation-event)

---
### Confirmation Trigger

The UO level that must be strictly broken for a qualifying divergence to become Confirmed.

For bullish divergence:
- :blue-background[Trigger = highest UO value from Prior pivot through Current pivot, inclusive]

- and confirmation requires: :blue-background[current UO > Trigger]

For bearish divergence:
- :blue-background[Trigger = lowest UO value from Prior pivot through Current pivot, inclusive]

- and confirmation requires: :blue-background[current UO < Trigger]

See [Understanding the Trigger](#understanding-the-trigger); [Confirmation Event](#confirmation-event)

---

### Confirmation Event

The session on which UO actually crosses the applicable [Confirmation Trigger](#confirmation-trigger).

This is different from the Divergence Event:
- Divergence Event = when the pivot-based divergence becomes knowable.
- Confirmation Event = when UO subsequently satisfies the confirmation rule.

The two events can occur on different sessions or on the same session.

See [Understanding the Confirmation Event](#understanding-the-confirmation-event); [Confirmation trigger](#confirmation-trigger)

Related: [Divergence Event](#divergence-event)

---

### Confirmation Window

The bounded period during which an active divergence is eligible for Classic Confirmation.

The valid interval is: :blue-background[Event lag 0 through Event lag 10, inclusive]

The Divergence Event itself can confirm immediately.

If the trigger is not broken during the allowed interval, the setup expires before the following session.

See [The 10-Session Confirmation Window](#the-10-session-confirmation-window).

---

### Sessions Remaining

The number of eligible confirmation sessions still available while :violet-background[Classic Confirmation] is :green-background[Pending].

For example:

:gray-background[10 sessions remaining] means the divergence has just become actionable and still has its full post-event allowance available.

See [Understanding Sessions Remaining](#understanding-sessions-remaining).

---

### Semantic State

One of the seven underlying UO lifecycle states before projection onto the five [heatmap scores](#heatmap-score).

The seven states are:
1. Bullish Confirmed
2. Bullish Watch
3. Bullish Divergence
4. No Active Setup
5. Bearish Watch
6. Bearish Divergence
7. Bearish Confirmed

See [The Seven Semantic States](#the-seven-semantic-states).

---

### No Active Setup

A valid UO semantic state meaning that no Watch, Divergence, or Confirmed setup currently has precedence.

It does **not** mean:

- UO = 50;
- Pressure Bias is Balanced;
- Pressure Mix is mixed;
- UO contains no useful context.

It means only that no staged reversal setup is active.

See [No Active Setup Signal](#no-active-setup-signal).

---

### Heatmap Score

The five-level numeric projection used to map the seven UO semantic states into the broader heatmap system.

| UO semantic state | Heatmap score |
| --- | ---: |
| [Bullish Confirmed](#bullish-confirmation-logic) | +2 |
| [Bullish Watch](#bullish-watch-signal) | +1 |
| [Bullish Divergence](#bullish-divergence-signal) | +1 |
| [No Active Setup](#no-active-setup-signal) | 0 |
| [Bearish Watch](#bearish-watch-signal) | -1 |
| [Bearish Divergence](#bearish-divergence-signal) | -1 |
| [Bearish Confirmed](#bearish-confirmed-signal) | -2 |

The hover's :violet-background[Signal] preserves the semantic distinction between [Watch](#watch) and [Divergence](#divergence) even though they share the same ±1 score.

See [Five Heatmap Scores from Seven UO States](#five-heatmap-scores-from-seven-uo-states).

---
## My Notes
[Top](#uo-heatmap-translation-cheat-sheets)

- **Purpose:** To measure momentum across different timeframes, aiming to reduce false signals. 
- **Calculation:** Incorporates data from three time periods (7, 14, and 28) to create a single, more stable momentum measurement. 
	- Default settings are 7, 14, and 28 periods for the short, medium,
- **Features:**
    - **Multi-Timeframe:** Addresses limitations of single-timeframe oscillators by combining data from different trends. 
    - **Divergence-Based Signals:** Relies on divergences between the indicator and price as a primary signal for buy and sell orders. 
    - **Volatility Reduction:** The multi-timeframe approach helps smooth out the signal, leading to fewer false signals

$$----------$$

UO uses three different periods to capture a broader view of momentum. 
- Uses three different time periods (7, 14, and 28) to measure momentum across short, medium, and long-term trends, aiming to provide more reliable buy and sell signals by reducing volatility

**Signals:** UO relies on "*divergences*" for signals, a strategy that helps confirm potential trend reversals.

**Volatility vs. Signal Generation:** UO is designed to <u>reduce volatility</u> and generate <u>fewer but more reliable signals</u>, whereas Awesome Oscillator can produce more frequent signals but with less reliability in certain market conditions.

---

> **Adjusting the settings**
 
- **For higher sensitivity:**
    If the default settings are too slow for a particular security, you can shorten the timeframes (e.g., to 4, 8, and 16 periods).

- **For lower sensitivity:**
    For highly volatile stocks, you can lengthen the timeframes to reduce noise and get fewer signal

---
## Table of Contents — Complete Outline
[Top](#uo-heatmap-translation-cheat-sheets)

1. [UO Heatmap Translation Cheat Sheets](#uo-heatmap-translation-cheat-sheets)
    - 1.1. [Cheat Sheet 1 — Heatmap Cell: What Am I Looking At?](#cheat-sheet-1--heatmap-cell-what-am-i-looking-at)
    - 1.2. [Cheat Sheet 2 — Signal & Heatmap Score Translation](#cheat-sheet-2--signal--heatmap-score-translation)
        - 1.2.1. [Rulebook Routing vs. Effective UO Rules](#rulebook-routing-vs-effective-uo-rules)
    - 1.3. [Cheat Sheet 3 — Zone, Pressure Bias & Pressure Mix: Current Context](#cheat-sheet-3--zone-pressure-bias--pressure-mix-current-context)
    - 1.4. [Cheat Sheet 4 — Divergence Outcome Translation](#cheat-sheet-4--divergence-outcome-translation)
        - 1.4.1. [Qualifying-Extreme Requirement](#qualifying-extreme-requirement)
    - 1.5. [Cheat Sheet 5 — Classic Confirmation Outcome Translation](#cheat-sheet-5--classic-confirmation-outcome-translation)
    - 1.6. [Cheat Sheet 6 — Lifecycle Metadata: Prior, Current, Event & Trigger](#cheat-sheet-6--lifecycle-metadata-prior-current-event--trigger)
        - 1.6.1. [Divergence Event vs Confirmation Event](#divergence-event-vs-confirmation-event)
    - 1.7. [Cheat Sheet 7 — Generic & Supporting Hover Fields](#cheat-sheet-7--generic--supporting-hover-fields)
    - 1.8. [One-Screen Mental Model](#one-screen-mental-model)
2. [Ultimate Oscillator — At a Glance](#ultimate-oscillator--at-a-glance)
    - 2.1. [What UO Is Designed to Show](#what-uo-is-designed-to-show)
    - 2.2. [The Seven UO Signal States](#the-seven-uo-signal-states)
    - 2.3. [Heatmap Symbols at a Glance](#heatmap-symbols-at-a-glance)
    - 2.4. [The Simplest Way to Think About UO](#the-simplest-way-to-think-about-uo)
3. [Reading the UO Heatmap](#reading-the-uo-heatmap)
    - 3.1. [Understanding the Cell](#understanding-the-cell)
        - 3.1.1. [The UO Value](#the-uo-value)
        - 3.1.2. [The Heatmap Background](#the-heatmap-background)
        - 3.1.3. [50-Line Crossover Symbols](#50-line-crossover-symbols)
        - 3.1.4. [Divergence Symbols](#divergence-symbols)
        - 3.1.5. [When More Than One Visual Cue Appears](#when-more-than-one-visual-cue-appears)
    - 3.2. [Understanding the Hover](#understanding-the-hover)
    - 3.3. [What Each UO-Specific Field Answers](#what-each-uo-specific-field-answers)
        - 3.3.1. [Zone](#zone)
        - 3.3.2. [Pressure Bias](#pressure-bias)
        - 3.3.3. [Pressure Mix](#pressure-mix)
        - 3.3.4. [Divergence](#divergence)
        - 3.3.5. [Classic Confirmation](#classic-confirmation)
        - 3.3.6. [Signal](#signal)
            - 3.3.6.1. [Watch](#watch)
        - 3.3.7. [Rule](#rule)
4. [UO Hover Field Reference](#uo-hover-field-reference)
    - 4.1. [Zone and Watch](#zone-and-watch)
        - 4.1.1. [Zone Outcomes](#zone-outcomes)
            - 4.1.1.1. [Oversold](#oversold)
            4.1.1.2. [Overbought](#overbought)
            4.1.1.3. [Neither Extreme](#neither-extreme)
        - 4.1.2. [How Zone Relates to Watch](#how-zone-relates-to-watch)
        - 4.1.3. [Why Zone and Signal Can Differ](#why-zone-and-signal-can-differ)
    - 4.2. [Pressure Bias and the 50-Line Crossover](#pressure-bias-and-the-50-line-crossover)
        - 4.2.1. [Pressure Bias Outcomes](#pressure-bias-outcomes)
            - 4.2.1.1. [Positive Pressure Bias](#positive-pressure-bias)
            4.2.1.2. [Negative Pressure Bias](#negative-pressure-bias)
            4.2.1.3. [Balanced Pressure Bias](#balanced-pressure-bias)
        - 4.2.2. [50-Line Crossover Events](#50-line-crossover-events)
            - 4.2.2.1. [Cross Above 50](#cross-above-50)
            4.2.2.2. [Cross Below 50](#cross-below-50)
        - 4.2.3. [What the Crossover Symbol Means (State vs Event: An Important Distinction)](#what-the-crossover-symbol-means-state-vs-event-an-important-distinction)
        - 4.2.4. [How to Use Pressure Bias](#how-to-use-pressure-bias)
        - 4.2.5. [What Pressure Bias Does Not Do](#what-pressure-bias-does-not-do)
    - 4.3. [Pressure Mix 101](#pressure-mix-101)
        - 4.3.1. [What Fast, Medium, and Slow Represent](#what-fast-medium-and-slow-represent)
        - 4.3.2. [Reading the Three Pressure Values](#reading-the-three-pressure-values)
        - 4.3.3. [Reading the Day-to-Day Changes](#reading-the-day-to-day-changes)
        - 4.3.4. [Pressure Mix Outcomes](#pressure-mix-outcomes)
            - 4.3.4.1. [Recent Pressure Strengthening](#recent-pressure-strengthening)
            4.3.4.2. [Recent Pressure Weakening](#recent-pressure-weakening)
            4.3.4.3. [Mixed / Transitional](#mixed--transitional)
        - 4.3.5. [Cross-Horizon Ordering vs Day-to-Day Change](#cross-horizon-ordering-vs-day-to-day-change)
        - 4.3.6. [How to Use Pressure Mix](#how-to-use-pressure-mix)
        - 4.3.7. [What Pressure Mix Does Not Do](#what-pressure-mix-does-not-do)
    - 4.4. [Divergence 101](#divergence-101)
        - 4.4.1. [Divergence Outcomes](#divergence-outcomes)
            - 4.4.1.1. [None](#none)
            4.4.1.2. [Active - Bullish ('Bullish Divergence')](#active---bullish-bullish-divergence)
            4.4.1.3. [Active - Bearish ('Bearish Divergence')](#active---bearish-bearish-divergence)
        - 4.4.2. [The Qualifying Extreme Requirement](#the-qualifying-extreme-requirement)
        - 4.4.3. [Understanding Prior, Current, and Event](#understanding-prior-current-and-event)
            - 4.4.3.1. [Prior](#prior)
            4.4.3.2. [Current](#current)
            4.4.3.3. [Event](#event)
        - 4.4.4. [Confirmed Five-Bar Pivots](#confirmed-five-bar-pivots)
        - 4.4.5. [Why the Event Date Comes After the Pivot Date](#why-the-event-date-comes-after-the-pivot-date)
        - 4.4.6. [How Long Divergence Remains Active](#how-long-divergence-remains-active)
        - 4.4.7. [What the Divergence Diamond Means](#what-the-divergence-diamond-means)
        - 4.4.8. [How Divergence Affects the UO Signal](#how-divergence-affects-the-uo-signal)
    - 4.5. [Classic Confirmation 101](#classic-confirmation-101)
        - 4.5.1. [Classic Confirmation Outcomes](#classic-confirmation-outcomes)
            - 4.5.1.1. [None](#none-1)
            4.5.1.2. [Pending](#pending)
            4.5.1.3. [Bullish Confirmed](#bullish-confirmed)
            4.5.1.4. [Bearish Confirmed](#bearish-confirmed)
            4.5.1.5. [Expired](#expired)
        - 4.5.2. [Understanding the Trigger](#understanding-the-trigger)
        - 4.5.3. [Understanding 'Sessions Remaining'](#understanding-sessions-remaining)
        - 4.5.4. [Understanding the 'Confirmation Event'](#understanding-the-confirmation-event)
        - 4.5.5. [Bullish Confirmation Logic](#bullish-confirmation-logic)
        - 4.5.6. [Bearish Confirmation Logic](#bearish-confirmation-logic)
        - 4.5.7. [Same-Day Divergence and Confirmation](#same-day-divergence-and-confirmation)
        - 4.5.8. [The 10-Session Confirmation Window](#the-10-session-confirmation-window)
        - 4.5.9. [Why Confirmation Can Expire](#why-confirmation-can-expire)
        - 4.5.10. [What Confirmation Does and Does Not Mean](#what-confirmation-does-and-does-not-mean)
    - 4.6. [Signal and Rule](#signal-and-rule)
        - 4.6.1. [The Seven Semantic States](#the-seven-semantic-states)
        - 4.6.2. [User-Facing Signal Labels](#user-facing-signal-labels)
            - 4.6.2.1. [Bullish Watch Signal](#bullish-watch-signal)
            4.6.2.2. [Bullish Divergence Signal](#bullish-divergence-signal)
            4.6.2.3. [Bullish Confirmed Signal](#bullish-confirmed-signal)
            4.6.2.4. ['No Active Setup' Signal](#no-active-setup-signal)
            4.6.2.5. [Bearish Watch Signal](#bearish-watch-signal)
            4.6.2.6. [Bearish Divergence Signal](#bearish-divergence-signal)
            4.6.2.7. [Bearish Confirmed Signal](#bearish-confirmed-signal)
        - 4.6.3. [Five Heatmap Scores from Seven UO States](#five-heatmap-scores-from-seven-uo-states)
        - 4.6.4. [Why Watch and Divergence Share the Same Score](#why-watch-and-divergence-share-the-same-score)
        - 4.6.5. [Dynamic Rule Text](#dynamic-rule-text)
        - 4.6.6. [Reading Signal and Rule Together](#reading-signal-and-rule-together)
5. [The Staged Reversal Framework](#the-staged-reversal-framework)
    - 5.1. [The Staged Reversal Lifecycle](#the-staged-reversal-lifecycle)
        - 5.1.1. [Stage 1 — Watch](#stage-1--watch)
        - 5.1.2. [Stage 2 — Divergence](#stage-2--divergence)
        - 5.1.3. [Stage 3 — Confirmation](#stage-3--confirmation)
    - 5.2. [State Precedence](#state-precedence)
        - 5.2.1. [Confirmed Over Divergence](#confirmed-over-divergence)
        - 5.2.2. [Divergence Over Watch](#divergence-over-watch)
        - 5.2.3. [Watch Over No Active Setup](#watch-over-no-active-setup)
    - 5.3. [Persistence, Confirmation, and Expiry](#persistence-confirmation-and-expiry)
        - 5.3.1. [Watch Persistence](#watch-persistence)
        - 5.3.2. [Divergence Persistence](#divergence-persistence)
        - 5.3.3. [Confirmation as an Event-Day State](#confirmation-as-an-event-day-state)
        - 5.3.4. [Expiry and Stale-Setup Prevention](#expiry-and-stale-setup-prevention)
    - 5.4. [Why the Current Zone Can Differ from the Active Signal](#why-the-current-zone-can-differ-from-the-active-signal)
6. [The Three UO Variants](#the-three-uo-variants)
    - 6.1. [UO(5,10,15) — Fast](#uo51015--fast)
    - 6.2. [UO(7,14,28) — Classic / Medium](#uo71428--classic--medium)
    - 6.3. [UO(10,20,40) — Slow](#uo102040--slow)
    - 6.4. [Comparing the Three Variants](#comparing-the-three-variants)
        - 6.4.1. [Responsiveness](#responsiveness)
        - 6.4.2. [Watch Thresholds](#watch-thresholds)
        - 6.4.3. [Signal Frequency](#signal-frequency)
        - 6.4.4. [When Each Variant Is Most Useful](#when-each-variant-is-most-useful)
        - 6.4.5. [Why the Three Variants Are Not Three Equal Votes](#why-the-three-variants-are-not-three-equal-votes)
7. [How UO Is Calculated](#how-uo-is-calculated)
    - 7.1. [Buying Pressure](#buying-pressure)
        - 7.1.1. [Example — No Downside Gap](#example--no-downside-gap)
        - 7.1.2. [Example — Gap Up](#example--gap-up)
    - 7.2. [True Range](#true-range)
        - 7.2.1. [Example — No Material Gap](#example--no-material-gap)
        - 7.2.2. [Example — Gap Up](#example--gap-up-1)
    - 7.3. [Fast, Medium, and Slow Pressure](#fast-medium-and-slow-pressure)
    - 7.4. [The 4:2:1 Weighting](#the-421-weighting)
    - 7.5. [From Pressure Components to the Final UO Value](#from-pressure-components-to-the-final-uo-value)
    - 7.6. [Why Pressure Mix Adds Information Beyond the Final UO Number](#why-pressure-mix-adds-information-beyond-the-final-uo-number)
8. [Worked Heatmap Examples](#worked-heatmap-examples)
    - 8.1. [MSFT — Bullish Divergence Pending Confirmation](#msft--bullish-divergence-pending-confirmation)
        - 8.1.1. [Reading the Cell (Bullish Divergence Pending Confirmation)](#reading-the-cell-bullish-divergence-pending-confirmation)
        - 8.1.2. [Reading the Hover (Bullish Divergence Pending Confirmation)](#reading-the-hover-bullish-divergence-pending-confirmation)
        - 8.1.3. [Why the Signal Is Bullish Setup (Divergence)](#why-the-signal-is-bullish-setup-divergence)
        - 8.1.4. [What Would Confirm the Setup  (Bullish Divergence Pending Confirmation)](#what-would-confirm-the-setup-bullish-divergence-pending-confirmation)
    - 8.2. [XLP — Bullish Confirmation](#xlp--bullish-confirmation)
        - 8.2.1. [Reading the Cell (Bullish confirmation)](#reading-the-cell-bullish-confirmation)
        - 8.2.2. [Reading the Hover (Bullish confirmation)](#reading-the-hover-bullish-confirmation)
        - 8.2.3. [Why Confirmation Can Occur Outside the Extreme Zone](#why-confirmation-can-occur-outside-the-extreme-zone)
    - 8.3. [XLY — Bullish Confirmation While Zone Is Overbought](#xly--bullish-confirmation-while-zone-is-overbought)
        - 8.3.1. [Why This Is Not a Contradiction](#why-this-is-not-a-contradiction)
        - 8.3.2. [How Precedence Explains the Result](#how-precedence-explains-the-result)
    - 8.4. [MSFT — Expired Bullish Divergence](#msft--expired-bullish-divergence)
        - 8.4.1. [What Expired Means](#what-expired-means)
        - 8.4.2. [Why the Old Setup Does Not Reactivate Later](#why-the-old-setup-does-not-reactivate-later)
9. [Practical Reading Guide](#practical-reading-guide)
    - 9.1. [A Simple Reading Sequence](#a-simple-reading-sequence)
        - 9.1.1. [Step 1 — Start with Signal](#step-1--start-with-signal)
        - 9.1.2. [Step 2 — Check Divergence](#step-2--check-divergence)
        - 9.1.3. [Step 3 — Check Classic Confirmation](#step-3--check-classic-confirmation)
        - 9.1.4. [Step 4 — Read Zone](#step-4--read-zone)
        - 9.1.5. [Step 5 — Read Pressure Bias](#step-5--read-pressure-bias)
        - 9.1.6. [Step 6 — Read Pressure Mix](#step-6--read-pressure-mix)
        - 9.1.7. [Step 7 — Use Rule as the Audit Trail](#step-7--use-rule-as-the-audit-trail)
    - 9.2. [Common UO Combinations](#common-uo-combinations)
        - 9.2.1. [Watch + Strengthening Pressure Mix](#watch--strengthening-pressure-mix)
        - 9.2.2. [Watch + Weakening Pressure Mix](#watch--weakening-pressure-mix)
        - 9.2.3. [Divergence + Positive Pressure Bias](#divergence--positive-pressure-bias)
        - 9.2.4. [Divergence + Fresh 50-Line Crossover](#divergence--fresh-50-line-crossover)
        - 9.2.5. [Confirmed + Opposite Current Zone](#confirmed--opposite-current-zone)
        - 9.2.6. [No Active Setup + Meaningful Context](#no-active-setup--meaningful-context)
    - 9.3. [What to Focus on First](#what-to-focus-on-first)
10. [Limitations, Warmup, and Interpretation Boundaries](#limitations-warmup-and-interpretation-boundaries)
    - 10.1. [Missing Is Not Neutral](#missing-is-not-neutral)
    - 10.2. [Pivot Confirmation Is Delayed by Design](#pivot-confirmation-is-delayed-by-design)
    - 10.3. [No Back-Painting](#no-back-painting)
    - 10.4. [Extreme Does Not Mean Reversal](#extreme-does-not-mean-reversal)
    - 10.5. [Divergence Does Not Mean Reversal](#divergence-does-not-mean-reversal)
    - 10.6. [Confirmation Does Not Guarantee Price Reversal](#confirmation-does-not-guarantee-price-reversal)
    - 10.7. [Context Fields Do Not Override the Primary Signal](#context-fields-do-not-override-the-primary-signal)
    - 10.8. [Why Expiry Matters](#why-expiry-matters)
11. [Glossary and Quick Reference](#glossary-and-quick-reference)
    - 11.1. [Confirmed](#confirmed)
    - 11.2. [50-Line Crossover](#50-line-crossover)
    - 11.3. [Pressure Ratio](#pressure-ratio)
    - 11.4. [Pivot](#pivot)
    - 11.5. [Prior Pivot](#prior-pivot)
    - 11.6. [Current Pivot](#current-pivot)
    - 11.7. [Qualifying Extreme](#qualifying-extreme)
    - 11.8. [Divergence Event](#divergence-event)
    - 11.9. [Confirmation Trigger](#confirmation-trigger)
    - 11.10. [Confirmation Event](#confirmation-event)
    - 11.11. [Confirmation Window](#confirmation-window)
    - 11.12. [Sessions Remaining](#sessions-remaining)
    - 11.13. [Semantic State](#semantic-state)
    - 11.14. [No Active Setup](#no-active-setup)
    - 11.15. [Heatmap Score](#heatmap-score)

---
