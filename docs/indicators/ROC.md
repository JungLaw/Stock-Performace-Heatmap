## Summary: ROC Signals
(:small[[ToC](#to-c-roc)])

:blue-background[Rate of Change (ROC)] measures the pure percentage change in price over a specified period to identify ***momentum*** 'acceleration' or 'deceleration'.
- measures the momentum of price changes
- shows whether an asset is gaining or losing momentum by comparing current prices to historical ones.


The displayed ROC percentage determines the primary :blue-background[Signal].
- Secondary metrics like ['zero-line crossovers'](#confirmed-zero-line-crossovers), '[Price/ROC Divergence](#confirmed-bullish-and-bearish-divergence)', '[Relative Volume](#relative-volume-20-prior-sessions)', and '[Historical ROC Standing](#historical-roc-standing-120-observations)' provide  **separate context** (no influence on five-state score) (:small[For more info, see '[Value-added use and complementary indicators](#value-added-use-and-complementary-indicators)']).

> The app interprets ROC as a **zero-centered momentum-continuation indicator**: positive values describe an advance over the lookback; negative values describe a decline.

---
### Primary Signal Summary: ROC(14)
(:small[[Parent](#summary-roc-signals)])

The main teaching example is :blue-background[ROC(14)]. ROC(12) and ROC(20) use the **same thresholds**, but measure returns over different lookbacks. See [ROC Signal Rules — The five-state model](#roc-signal-rules-the-five-state-model) for worked explanations, and [Other parameter settings](#other-parameter-settings) for ROC(9) and ROC(50).

| Signal | Literal trigger, on the raw fractional ROC(14) | Layman's translation | Rule logic | Bottom-line |
|---|---|---|---|---|
| [Strong Buy](#strong-buy-roc-14) | :blue-background[ROC_14 > 0.07] | Price is more than :gray-background[7%] above its level 14 sessions ago. | Positive return **exceeds** the Strong threshold. | **Large positive 14-session momentum.** |
| [Buy](#buy-roc-14) | :blue-background[ROC_14 > 0.03 and ROC_14 <= 0.07] | Price gained more than :gray-background[3%], but not more than :gray-background[7%]. | Meaningful positive momentum without Strong magnitude. | **Qualified upward momentum.** |
| [Neutral](#neutral-roc-14) | :blue-background[-0.03 <= ROC_14 <= 0.03] | The 14-session price change falls within the project’s middle band. | Both :gray-background[−3%] and :gray-background[+3%] boundaries belong to Neutral. | **No qualified directional ROC magnitude.** |
| [Sell](#sell-roc-14) | :blue-background[ROC_14 >= -0.07 and ROC_14 < -0.03] | Price declined more than :gray-background[3%], but not more than :gray-background[7%]. | Meaningful negative momentum without Strong magnitude. | **Qualified downward momentum.** |
| [Strong Sell](#strong-sell-roc-14) | :blue-background[ROC_14 < -0.07] | Price is more than :gray-background[7%] below its level 14 sessions ago. | Negative return exceeds the Strong threshold in magnitude. | **Large negative 14-session momentum.** |

These rules use the **unrounded ROC value**. A displayed value exactly at a threshold may conceal a small difference; the authoritative Signal and dynamic Rule explanation use full precision.

---
### Summary: Important ROC Patterns
(:small[Source: [Most Important ROC Patterns (6)](#most-important-roc-patterns-6)|See Also: [The ROC patterns you should recognize immediately](#the-roc-patterns-you-should-recognize-immediately)| [Back to top](#summary-roc-signals)])

| Rank                                                  | Pattern                                                                                                                                                                                                                                                                  | Scope                                                         | Relative attention | Why it deserves attention                                                                                                                                                                                                       | What to examine next                                                                                           |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **1:  Structural warning against qualified momentum** | <ol><li>:blue-background[Buy/Strong Buy] + ${\textcolor{Red}{\textsf{Bearish divergence}}}$ <li>:blue-background[Sell/Strong Sell] + ${\textcolor{DodgerBlue}{\textsf{Bullish divergence}}}$</ol>                                                                       | [Conflicting](#four-categories-for-interpreting-combinations) | **High — caution** | A meaningful lookback move remains qualified, but the latest confirmed price extreme was not supported by equivalent ROC momentum. <li>This reveals an important tension not evident from the Signal background. | Whether price loses support, fails to extend its high, stabilizes near its low or resumes the prevailing trend |
| **2:  Opposing Confirmed Events**                     | <ol><li>${\textcolor{DodgerBlue}{\textsf{Bullish divergence}}}$ + ▼<li>${\textcolor{Red}{\textsf{Bearish divergence}}}$ + ▲</ol>                                                                                                                                         | Conflicting                                                   | **High — mixed**   | Structural price/ROC evidence and the newly confirmed momentum-sign transition point in opposite directions. <li>A 'bullish' or 'bearish' conclusion based on only one annotation would be incomplete.           | Which development gains support from subsequent ROC and price behavior                                         |
| **3: Two confirmed 'Events' reinforce each other**    | <ol><li>${\textcolor{DodgerBlue}{\textsf{Bullish divergence}}}$ + ▲ <li>${\textcolor{Red}{\textsf{Bearish divergence}}}$ + ▼</ol>                                                                                                                                        | [Reinforcing](#four-categories-for-interpreting-combinations) | **High**           | The confirmed price-pivot disagreement and the confirmed ROC sign transition point toward a similar directional development. They add compatible evidence beyond the primary Signal.                                            | Whether price breaks a relevant level or sustains the newly established momentum direction                     |
| **4:  Neutral with a new Divergence Event**           | :blue-background[Neutral] + $\small{\textcolor{DodgerBlue}{\textsf{Bullish}}}$ or $\small{\textcolor{red}{\textsf{Bearish}}}$ (no crossover)                                                                                                                      | [Early Watch](#four-categories-for-interpreting-combinations) | **Medium–High**    | The Signal has not qualified as directional, yet a meaningful price-pivot nonconfirmation has just been confirmed. <li>The 'neutral' background alone would not communicate this development.                                   | Pivot dates, ROC differences, price structure and subsequent momentum                                          |
| **5:  Neutral with a new Zero-line Crossover**        | :blue-background[Neutral] **+** **▲ or ▼** (without divergence)                                                                                                                                                                                                          | Early Watch                                                   | **Medium**         | ROC has completed a 3-session 'sign' transition, but its magnitude remains within the period-specific 'Neutral' range. <li>Direction changed before a Buy/Sell threshold qualified.                                             | Whether ROC continues beyond the Neutral boundary or reverses toward zero                                      |
| **6 — Qualified momentum with aligned new evidence**  | 'Strong' with one qualifying event: <ol><li>:blue-background[Buy/Strong Buy] **+** ${\textcolor{DodgerBlue}{\textsf{Bullish divergence}}}$ or $\large{▲}$ <li>:blue-background[Sell/Strong Sell] + ${\textcolor{Red}{\textsf{Bearish divergence}}}$ or $\large{▼}$ </ol> | Reinforcing                                                   | **Medium**         | Existing directional momentum is accompanied by a compatible new observation, without an additional conflicting event. <li>Does not strengthen the assigned Signal score.                                                       | Persistence of momentum, price confirmation and whether the event is followed by continuation                  |

**How to use this table:** Start with the highest-ranked applicable observation. Multiple rows can apply to one cell; the ranking guides investigation rather than selecting one exclusive label.


---
### What the cell annotations mean
(:small[[Parent](#summary-roc-signals) | See Also: [How to read a ROC heatmap cell](#how-to-read-a-roc-heatmap-cell)])

| What you see | What it reports | What it does **not** mean |
|---|---|---|
| :blue-background[Cell background] | The [five-state Signal](#roc-signal-rules-the-five-state-model), scored :gray-background[+2, +1, 0, −1, −2] | A forecast of the next day's price |
| :blue-background[Printed ROC number] | Lookback percentage return, shown to :gray-background[2 decimal places] | The classification score or today's one-day price change |
| :blue-background[Black ▲] | A **positive** [zero-line crossover](#confirmed-zero-line-crossovers) confirmed today | An automatic Strong Buy |
| :blue-background[Black ▼] | A **negative** [zero-line crossover](#the-zero-line-is-not-the-signal-threshold) confirmed today | An automatic Strong Sell |
| :blue[Blue number] | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$  confirmed price/ROC [divergence](#what-divergence-means-and-what-it-does-not) event today | A proven reversal or automatically bullish Signal |
| :red[Red number] | ${\textcolor{red}{\textsf{Bearish}}}$ confirmed price/ROC [divergence](#confirmed-bullish-and-bearish-divergence) event today | A proven reversal or automatically bearish Signal |
| :gray-background[No event symbol or colored number] | No corresponding confirmed event displayed on that cell | Proof that all historical event-evaluation prerequisites were available |

The black triangle and the colored numeric text are independent. A cell can display **both**, and neither changes its background classification.

### Guide map
(:small[[Parent](#summary-roc-signals)])

| If you want to… | Go to… |
|---|---|
| Spot the important combinations immediately | [The ROC patterns you should recognize immediately](#the-roc-patterns-you-should-recognize-immediately) |
| Understand the number and formula | [ROC — brief overview](#roc-brief-overview) |
| Interpret the cell's score, value and annotations | [How to read a ROC heatmap cell](#how-to-read-a-roc-heatmap-cell) |
| Reconstruct each of the five Signal states | [ROC Signal Rules — The five-state model](#roc-signal-rules-the-five-state-model) |
| Understand Alignment, crossover, divergence, RVOL or Standing | [Understanding ROC secondary metrics and events](#understanding-roc-secondary-metrics-and-events) |
| Decide what mixed evidence means | [How to interpret ROC patterns and combinations](#how-to-interpret-roc-patterns-and-combinations) |
| Interpret every field in the actual hover | [Understanding the ROC hover](#understanding-the-roc-hover) |
| Compare ROC(9), ROC(12), ROC(20), ROC(50) | [Other parameter settings](#other-parameter-settings) |
| Combine ROC with other indicators | [Value-added use and complementary indicators](#value-added-use-and-complementary-indicators) |
| Check assumptions and edge cases | [Assumptions limitations and safeguards](#assumptions-limitations-and-safeguards) |
| Put everything together in examples | [Practical ROC reading workflow](#practical-roc-reading-workflow) <li><small>'Positive Signal + Bearish Divergence'; 'Neutral + confirmed Positive Crossover'; 'Positive momentum (with no new event)'; 'Downside Momentum easing'</small>|

---

### 6-Step ROC Reading Workflow
(:small[[Parent](#summary-roc-signals) | Section: [Practical ROC reading workflow](#a-six-step-reading-sequence)])

| Step | Action | The question you're answering |
|---|---|---|
| **1. Establish the horizon** | Confirm ROC(9), (12), (14), (20) or (50) | Over how many sessions is the percentage change measured? |
| **2. Read the number and background** | Value + Signal + period-specific cutoff | How large is current positive or negative momentum? |
| **3. Inspect 'New Events'** | ${▲/▼}$ and ${\textcolor{DodgerBlue}{\textsf{blue}}}$/${\textcolor{Red}{\textsf{red}}}$ numeric overlay | Did a confirmed sign transition or price-pivot disagreement occur **today**? |
| **4. Reconcile the evidence** | Compare event directions and [one-bar Alignment](#roc-direction-and-one-session-alignment) | Do the observations reinforce one another or create caution? |
| **5. Add supporting context** | [RVOL](#relative-volume-20-prior-sessions), [Standing](#historical-roc-standing-120-observations), trend, volume and price structure | Is the reading unusual or supported by other information? |
| **6. Verify the reason** | 'Dynamic Rule', 'Context Interpretation', '[Bottom-line](#how-to-read-the-dynamic-rule-and-context-interpretation)' | Can you explain the current state and any qualifications in plain language? |


---

## The ROC patterns you should recognize immediately
(:small[[Back to top](#summary-roc-signals) | Related: [Summary: Important ROC Patterns](#summary-important-roc-patterns)])

A ROC cell contains **two layers of information**: the background Signal tells you the magnitude of the lookback return; optional visual annotations identify **newly confirmed events**. Start by looking for information the color alone could not convey.

> See [How to interpret ROC patterns and combinations](#how-to-interpret-roc-patterns-and-combinations) for the complete interpretive reference.
For mechanics, see [Alignment](#roc-direction-and-one-session-alignment), [zero-line crossovers](#confirmed-zero-line-crossovers) and [confirmed divergence](#confirmed-bullish-and-bearish-divergence).

### Priority summary: what deserves attention first
(:small[[Parent](#the-roc-patterns-you-should-recognize-immediately)])

| Priority | Pattern family | First question to ask | Why it matters |
|---|---|---|---|
| **Tier 1 — New conflicting evidence** | <li>Positive :blue-background[Buy/Strong Buy] + ${\textcolor{Red}{\textsf{bearish divergence}}}$<li> Negative :blue-background[Sell/Strong Sell] + ${\textcolor{DodgerBlue}{\textsf{bullish divergence}}}$ | Is an established directional move losing confirmation at its new price extreme? | The background still signals strong or qualified momentum, while the newly confirmed price structure warns that momentum at the later extreme was weaker. |
| **Tier 2 — New reinforcing evidence** | <li>Positive crossover $\large{▲}$ with  ${\textcolor{DodgerBlue}{\textsf{bullish divergence}}}$; <li>Negative crossover $\large{▼}$ with ${\textcolor{Red}{\textsf{bearish divergence}}}$ | Do two distinct events support a similar directional interpretation? | A confirmed sign transition and a confirmed pivot comparison can agree, without turning into an extra scored vote. |
| **Tier 3 — Important Neutral developments** | <li>:blue-background[Neutral] + $\large{▲}$ or $\large{▼}$; <li>[Neutral](#neutral-roc14) + ${\textcolor{DodgerBlue}{\textsf{blue}}}$/${\textcolor{Red}{\textsf{red}}}$ divergence | Has something changed even though the primary magnitude is below the Buy/Sell cutoff? | Event context may be meaningful before the absolute ROC magnitude leaves the Neutral range. |
| **Tier 4 — Persistent directional magnitude** | [Strong Buy](#strong-buy-roc14)/[Strong Sell](#strong-sell-roc14) with no new event | Is substantial momentum continuing, and for how long? | A 'Strong' state identifies a large lookback displacement; it is not necessarily a new event today. |
| **Tier 5 — Supporting or contradicting context** | [One-bar price](#one-bar-disagreement-versus-pivot-divergence)/ROC disagreement; unusual [RVOL](#relative-volume-20-prior-sessions); extreme [historical standing](#historical-roc-standing-120-observations) | Does today's movement reinforce the lookback state? | These observations improve interpretation but do not independently qualify a Signal or formal divergence. |

- **'Priority'** means interpretive information value, not measured predictive accuracy or expected profitability.
- **Tier 1** deserves attention because it reveals a potentially important tension, not because it predicts a reversal.

### At-a-glance combination examples
(:small[[Parent](#the-roc-patterns-you-should-recognize-immediately)])

| Signal and other evidence | Accurate first reading | Examine next |
|---|---|---|
| :blue-background[Strong Buy] + ${\textcolor{red}{\textsf{bearish-divergence number}}}$ | The lookback advance is large, but the newer confirmed price high carried lower ROC than the previous high. | [Pivot evidence and timing](#confirmed-bullish-and-bearish-divergence); whether price holds near the new high |
| :blue-background[Strong Sell] + ${\textcolor{DodgerBlue}{\textsf{bullish-divergence number}}}$ | The lookback decline is large, but the newer confirmed price low had higher ROC than the earlier low. | Whether downside movement continues to ease; do **not** assume price has bottomed |
| :blue-background[Neutral] + :gray-background[▲] | ROC has spent three sessions above zero after an opposite-sign reading, but the gain is still below the Buy cutoff. | [Confirmed crossover mechanics](#confirmed-zero-line-crossovers); follow-through |
| :blue-background[Neutral] + ${\textcolor{DodgerBlue}{\textsf{bullish divergence}}}$ | A confirmed bullish divergence is present even though today's ROC magnitude remains Neutral. | Pivot dates and [separate event versus Signal](#how-to-read-a-roc-heatmap-cell) |
| :blue-background[Buy] + :gray-background[RVOL 0.60×] | Qualified positive lookback return, while today's volume is only 60% of its prior-20-session average. | [What RVOL can and cannot tell you](#relative-volume-20-prior-sessions) |
| :blue-background[Strong Buy] + :gray-background[Historical Standing 90th percentile] | A large positive lookback return is also high relative to the security's recent ROC readings. | Whether the observation is newly strengthening or simply staying elevated |

The descriptions are **illustrative combinations**. They do not assert these particular events occurred for a named ticker or that simultaneous events are common.

---

## ROC: Brief Overview
(:small[[Back to top](#summary-roc-signals) | Related: ['Notes'](#old-notes-roc)])

Rate of Change is a pure momentum oscillator. It compares the current price with the price :gray-background[n] periods earlier and expresses the difference as a percentage.

A conventional percentage formula is:

```text
ROC% = 100 × (Current Price − Price n periods ago)
             ÷ Price n periods ago
```

An equivalent form is:

```text
ROC% = 100 × ((Current Price ÷ Price n periods ago) − 1)
```


### Simplest mental model
(:small[[Parent](#roc-brief-overview)])

| Price compared with :gray-background[n] sessions ago | ROC sign | Core meaning |
|---|---|---|
| Higher | Positive | **Upward** lookback momentum |
| Unchanged | Zero | **Flat** lookback return |
| Lower | Negative | **Downward** lookback momentum |

ROC asks: **"How much has price changed from exactly :gray-background[n] sessions ago?"** It does not directly ask whether price increased today. For example, price can rise today while ROC falls if the comparison price from 14 sessions ago also rose enough to reduce the measured 14-session gain.

:blue-background[ROC(14)] compares the current session with the session **14 observations earlier**; :blue-background[ROC(50)] compares with **50 observations earlier**. These are trading observations, not calendar-day intervals.

### Formula and concrete calculations
(:small[[Parent](#roc-brief-overview)])

$$\operatorname{ROC}_n(\%)=100\left(\frac{P_t}{P_{t-n}}-1\right)$$

The application computes ROC in **fractional** units for its rule engine and multiplies by :gray-background[100] for the heatmap, hover and ROC percentage chart.

| Example, using the same price series at both dates | Calculation | Heatmap cell number | Meaning |
|---|---|---|---|
| :gray-background[$100] → :gray-background[$108] | :gray-background[(108 / 100 − 1) × 100] | :gray-background[8.00] | An :gray-background[8%] advance in 14 sessions — Strong Buy for ROC(14) |
| :gray-background[$100] → :gray-background[$94] | :gray-background[(94 / 100 − 1) × 100] | :gray-background[−6.00] | A :gray-background[6%] decline — Sell for ROC(14) |
| :gray-background[$100] → :gray-background[$100] | :gray-background[0] | :gray-background[0.00] | No lookback change — Neutral |

The cell typically shows a positive number **without a leading plus sign**, such as :gray-background[8.00]; a negative number shows its minus sign, such as :gray-background[−6.00]. The hover explicitly uses signed percentages, such as :gray-background[+8.00%]. The **Signal background** conveys classification; the number is not the score.

### What the price source means
(:small[[Parent](#roc-brief-overview)])

For ROC's Option C calculation, the canonical price series prioritizes the stored :blue-background[Adjusted Close] when available and falls back to :blue-background[Close] where necessary. The **same ROC price series** is used for the ROC percentage, one-session price comparisons, divergence price pivots and ROC hover Price values. Therefore these components have a consistent internal mathematical basis.

The general heatmap **Price** row and other indicator families do not necessarily use this exact series on database-backed observations. **Do not automatically assume the ROC hover Price equals the general Price-row value** on a given date. Historical adjustment coverage and acquisition conventions are a separate data-integrity concern; see [Price-source and history safeguards](#price-source-and-history-safeguards).


### Threshold comparison: all five settings
(:small[[Parent](#roc-brief-overview)])

| Setting | Neutral, inclusive | Buy / Sell begins beyond | Strong Buy / Strong Sell begins beyond | Interpretation |
|---|---|---|---|---|
| :blue-background[ROC(9)] | :gray-background[±2%] | :gray-background[±2%] | :gray-background[±5%] | Fastest short-term thrust |
| :blue-background[ROC(12)] | :gray-background[±3%] | :gray-background[±3%] | :gray-background[±7%] | Short-term thrust |
| :blue-background[ROC(14)] | :gray-background[±3%] | :gray-background[±3%] | :gray-background[±7%] | Main medium-term reference |
| :blue-background[ROC(20)] | :gray-background[±3%] | :gray-background[±3%] | :gray-background[±7%] | Longer medium-term view |
| :blue-background[ROC(50)] | :gray-background[±5%] | :gray-background[±5%] | :gray-background[±10%] | Longer-horizon momentum backdrop |

**Beyond** means strictly greater than the positive cutoff or strictly less than the negative cutoff. Thus :gray-background[+7.00%] is Buy and :gray-background[−7.00%] is Sell for ROC(14); Strong requires going **past** those values. The ROC(50) Strong calibration is retained but flagged for [future review](#project-calibration-and-market-conventions).


### The zero line is not the Signal threshold
(:small[[Parent](#roc-brief-overview)])

A positive ROC reading can remain :blue-background[Neutral]. For ROC(14), :gray-background[+1.50%] is positive but inside :gray-background[−3% to +3%]. Likewise :gray-background[−2.00%] is negative but Neutral. The **zero line** marks the sign of the lookback return; the **project's magnitude thresholds** determine Buy, Neutral, Sell and Strong classifications.

A [confirmed zero-line crossover](#confirmed-zero-line-crossovers) is a **separate event**, not an instant switch to Buy/Sell or Strong.

---

## How to read a ROC heatmap cell
(:small[[Back to top](#summary-roc-signals)])

### Read the number, background and event marks separately
(:small[[Parent](#how-to-read-a-roc-heatmap-cell)])

| Layer | Where it appears | How to read it |
|---|---|---|
| **Numeric value** | Printed within the cell | Lookback percent return, displayed with two decimals; positive values normally omit the :gray-background[+] prefix, while negative values have a minus sign |
| **Background** | Cell fill | Primary Signal: Strong Buy :gray-background[+2], Buy :gray-background[+1], Neutral :gray-background[0], Sell :gray-background[−1], Strong Sell :gray-background[−2] |
| ${▲/▼}$ (black) | Crossover event cell | A confirmed positive / negative zero-line transition **on this date** |
| ${\textcolor{DodgerBlue}{\textsf{blue}}}$/${\textcolor{Red}{\textsf{red}}}$ numeric value | Divergence event cell | A confirmed bullish / bearish price-pivot disagreement **on this date** |
| **Hover** | Move over the cell | Full precision-based Rule explanation and event evidence; see [Understanding the ROC hover](#understanding-the-roc-hover) |

The divergence overlay changes **only the numeric font color** on an event cell. The crossover overlay adds a **black triangle**. They do not modify the number itself, score or background color. When both qualify on the same date, both can be shown.

### Examples that prevent common misreadings
(:small[[Parent](#how-to-read-a-roc-heatmap-cell)])

| Cell reading | Correct interpretation | Common mistake to avoid |
|---|---|---|
| :gray-background[4.50], Buy | Price is :gray-background[4.5%] above its 14-session comparison price; qualified positive momentum. | Thinking the number is a one-day gain or a +1 score |
| :gray-background[8.20], Strong Buy, red text | Large positive lookback momentum **and** a newly confirmed bearish divergence. | Replacing Strong Buy with Sell because the number is red |
| :gray-background[1.20], Neutral, ▲ | Return is positive, still inside the Neutral band; positive zero-line transition just confirmed. | Assuming a triangle automatically changes the Signal |
| :gray-background[−5.40], Sell, blue text | Qualified downside lookback momentum with a newly confirmed bullish divergence. | Treating bullish divergence as proof of a completed upward reversal |
| Blank or unavailable numeric observation | Indicator not computable on that date. | Treating missing as a valid ROC of zero or as Neutral |

**Important:** Signal classification uses unrounded fractional values. ROC(14) at exactly :gray-background[+3.0000%] is Neutral; a value slightly above that may still display as :gray-background[+3.00] while correctly receiving Buy.

---

## ROC Signal Rules: The five-state model
(:small[[Back to top](#summary-roc-signals)])

The classification is a **magnitude-based continuation model**. Every finite, initialized ROC(14) reading is assigned to exactly one of five mutually exclusive ranges. It is not classified from a crossover, divergence, ROC slope, volume, or a three-day confirmation sequence.

### Rule summary: ROC(12), ROC(14), ROC(20)
(:small[[Parent](#roc-signal-rules-the-five-state-model)])

| State | Executable fractional rule (substitute 12, 14 or 20 for n) | Displayed percentage range |
|---|---|---|
| Strong Buy | :blue-background[ROC_n > 0.07] | :gray-background[greater than +7%] |
| Buy | :blue-background[ROC_n > 0.03 and ROC_n <= 0.07] | :gray-background[greater than +3% through +7%, inclusive at +7%] |
| Neutral | :blue-background[-0.03 <= ROC_n <= 0.03] | :gray-background[−3% through +3%, both inclusive] |
| Sell | :blue-background[ROC_n >= -0.07 and ROC_n < -0.03] | :gray-background[−7%, inclusive, through less than −3%] |
| Strong Sell | :blue-background[ROC_n < -0.07] | :gray-background[less than −7%] |

For ROC(14), the raw rulebook variable is :blue-background[ROC_14]. Internal :gray-background[0.07] means :gray-background[7%] on the display. These three periods differ **only in measurement lookback**, not in the five thresholds. See the full [period comparison](#other-parameter-settings).

### Strong Buy: ROC(14)
(:small[[Parent](#roc-signal-rules-the-five-state-model)])

**Rule:** :blue-background[ROC_14 > 0.07].

**Literal meaning:** Price is **more than** :gray-background[7%] above the comparison price 14 sessions earlier. For example, :gray-background[$100 → $108.20] gives :gray-background[+8.20%] and qualifies.

**Plain-English version:** A substantial upward price move has already occurred over the 14-session lookback. The classification says that momentum is large **now**; it does not establish that the move is accelerating today or will continue tomorrow.

**Boundary:** Exactly :gray-background[+7.00%] is **Buy**, not Strong Buy. Strong requires :gray-background[more than +7%].

**Bottom-line:** **Large, established positive lookback momentum.** A fresh crossover or bullish divergence is not required.

### Buy: ROC(14)
(:small[[Parent](#roc-signal-rules-the-five-state-model)])

**Rule:** :blue-background[ROC_14 > 0.03 and ROC_14 <= 0.07].

**Literal meaning:** The price has gained **more than** :gray-background[3%] but **no more than** :gray-background[7%] over 14 sessions. Examples: :gray-background[+3.40%] and :gray-background[+7.00%].

**Plain-English version:** Meaningful positive price thrust exists, but its magnitude does not exceed the higher Strong cutoff. Unlike CMF's Strong state, ROC's Strong qualification does **not** require a rising sequence of recent indicator values.

**Bottom-line:** **Qualified positive momentum without Strong magnitude.**

### Neutral: ROC(14)
(:small[[Parent](#roc-signal-rules-the-five-state-model)])

**Rule:** :blue-background[-0.03 <= ROC_14 <= 0.03].

**Literal meaning:** The current 14-session return falls within :gray-background[−3% to +3%], including the endpoints. Examples: :gray-background[−2.70%], :gray-background[0.00%] and :gray-background[+3.00%].

**Plain-English version:** The lookback return does not exceed the project’s magnitude cutoff for directional classification. ROC can still be **positive**, **negative**, rising or falling; Neutral does not necessarily mean price is flat or nothing interesting occurred.

A confirmed [crossover](#confirmed-zero-line-crossovers) or [divergence](#confirmed-bullish-and-bearish-divergence) can be displayed on a Neutral cell because those are separately dated observations.

**Bottom-line:** **No qualified directional magnitude under the ROC(14) rule.** Missing ROC is not Neutral.

### Sell: ROC(14)
(:small[[Parent](#roc-signal-rules-the-five-state-model)])

**Rule:** :blue-background[ROC_14 >= -0.07 and ROC_14 < -0.03].

**Literal meaning:** The price has declined **more than** :gray-background[3%] but **no more than** :gray-background[7%] over 14 sessions. Examples: :gray-background[−4.50%] and :gray-background[−7.00%].

**Plain-English version:** Meaningful negative lookback momentum exists, but the loss has not exceeded the Strong Sell threshold in magnitude.

**Bottom-line:** **Qualified negative momentum without Strong magnitude.**

### Strong Sell: ROC(14)
(:small[[Parent](#roc-signal-rules-the-five-state-model)])

**Rule:** :blue-background[ROC_14 < -0.07].

**Literal meaning:** Price is **more than** :gray-background[7%] below the comparison price 14 sessions earlier. For example, :gray-background[$100 → $91.50] yields :gray-background[−8.50%].

**Plain-English version:** A substantial decline has occurred over the lookback. That is a strong negative momentum **state**, not an oversold-reversal prediction.

**Boundary:** Exactly :gray-background[−7.00%] is **Sell**, not Strong Sell.

**Bottom-line:** **Large, established negative lookback momentum.**

### Why boundary exclusivity and rounding matter
(:small[[Parent](#roc-signal-rules-the-five-state-model)])

| Exact ROC(14) percentage | Assigned state | Reason |
|---:|---|---|
| :gray-background[+7.00%] | Buy | Positive Strong requires strictly **above** +7% |
| :gray-background[+3.00%] | Neutral | Buy requires strictly **above** +3% |
| :gray-background[0.00%] | Neutral | Inside the inclusive middle band |
| :gray-background[−3.00%] | Neutral | Sell requires strictly **below** −3% |
| :gray-background[−7.00%] | Sell | Negative Strong requires strictly **below** −7% |

The bounded Buy and Sell ranges prevent overlap with Strong states. Every finite ROC reading belongs to **one** state. When its numeric inputs are missing, it should remain **unavailable**, not be assigned Neutral. The hover's [dynamic Rule](#understanding-the-roc-hover) explains the active classification using source-checked rulebook semantics and the unrounded value.

---

## Understanding ROC Secondary Metrics and Events
(:small[[Back to top](#summary-roc-signals)])

These fields answer questions the Signal alone cannot answer. Some are **one-session context**, some require **20 or 120-session history**, and some are **event-only**. Their calculations use full available chronological history, not just the visible cells in the heatmap window.

### ROC direction and one-session Alignment
(:small[[Parent](#understanding-roc-secondary-metrics-and-events)])

**ROC sign** and **ROC change** are different quantities:

| Observation | Example | Meaning |
|---|---|---|
| ROC sign is positive | :gray-background[ROC +5.0%] | Current price exceeds its :gray-background[n]-session-ago price |
| ROC is rising | :gray-background[+4.0% → +5.0%] | Lookback return improved by :gray-background[+1.0 pps] since yesterday |
| ROC is falling but still positive | :gray-background[+7.0% → +5.0%] | Positive lookback momentum persists but **weakened** |
| ROC is rising but still negative | :gray-background[−7.0% → −5.0%] | Negative lookback momentum persists but downside momentum **eased** |

:blue-background[Alignment] compares the **latest price move** with the **latest ROC move**, while also considering the **current ROC sign**. In the hover, :gray-background[P(+)] means today's ROC-canonical price rose; :gray-background[P(−)] fell; :gray-background[P(0)] was flat. The corresponding :gray-background[ROC(+/−/0)] codes describe the one-session change in the ROC reading, **not** whether ROC itself is positive or negative.

| Price change | ROC change | Current ROC sign | Hover's interpretation |
|---|---|---|---|
| :gray-background[P(+)] | :gray-background[ROC(+)] | Positive | **Confirming upside momentum** |
| :gray-background[P(−)] | :gray-background[ROC(−)] | Negative | **Confirming downside momentum** |
| :gray-background[P(+)] | :gray-background[ROC(−)] | Positive | **Upside momentum weakening** |
| :gray-background[P(−)] | :gray-background[ROC(+)] | Negative | **Downside momentum easing** |
| :gray-background[P(+)] | :gray-background[ROC(+)] | Negative | **Downside momentum easing** |
| :gray-background[P(−)] | :gray-background[ROC(−)] | Positive | **Upside momentum weakening** |
| :gray-background[P(+)] | :gray-background[ROC(−)] | Negative | **Downside momentum intensifying despite rising price** |
| :gray-background[P(−)] | :gray-background[ROC(+)] | Positive | **Upside momentum strengthening despite falling price** |
| Flat price / ROC, or ROC exactly zero | Where sufficient current and prior observations exist | Any | Hover uses a qualified flat-component or zero description rather than inventing directional confirmation |

For example, if price rose today while ROC(14) moved from :gray-background[+6.20%] to :gray-background[+5.60%], the latest price direction is up but the 14-session return is smaller. **That is one-session disagreement**, not formal bearish divergence. Formal divergence requires two confirmed [price pivots](#confirmed-bullish-and-bearish-divergence).

If either prior price or prior ROC is missing, the Alignment line is omitted rather than inferred.

### Confirmed zero-line crossovers
(:small[[Parent](#understanding-roc-secondary-metrics-and-events)])

A :blue-background[zero-line crossover] is a change in the **sign** of the lookback return, confirmed by **three successive ROC observations on the new side of zero**, following a transition from the opposite side.

It is an event marker, not a five-state classification rule.

| Event | Required transition | Heatmap mark | Hover wording |
|---|---|---|---|
| Positive crossover | Prior negative ROC followed by three successive **positive** readings | **Black ▲** on the **third** positive session | :gray-background[Positive confirmed today (3rd consecutive session above 0)] |
| Negative crossover | Prior positive ROC followed by three successive **negative** readings | **Black ▼** on the **third** negative session | :gray-background[Negative confirmed today (3rd consecutive session below 0)] |

> **Failed transition**: ROC returns to zero or the previous side before confirmation, or only one or two qualifying sessions.

**Timing example:** Suppose the sequence is :gray-background[−0.8%, +0.4%, +0.9%, +1.1%]. Day 1 of the positive run is the first :gray-background[+0.4%]; the **▲ appears only at +1.1%**, the third consecutive positive observation. The event is not backdated to the initial sign change.


| Date  | ROC(14) | Status                                  |
| ----- | ------- | --------------------------------------- |
| Day 0 | −0.8%   | Negative                                |
| Day 1 | +0.4%   | Positive, session 1                     |
| Day 2 | +0.9%   | Positive, session 2                     |
| Day 3 | +1.1%   | **Positive crossover confirmed**        |
| Day 4 | +1.5%   | Positive regime continues; no new event |

The event belongs to Day 3. It is not backdated to Day 1 or repeated on Day 4.

**Boundaries and interruptions:**
- Exactly zero **does not count** as positive or negative and interrupts the three-session qualifying run.
- A missing ROC observation resets the sign history and prevents a crossover event from bridging the gap.
- A sign transition must be established; three positive observations at the beginning of available history do not automatically constitute a positive crossover.
  - IOW, to avoid false repeat crossovers when ROC merely touches zero, the last valid nonzero sign must have been the opposite sign.

**Relationship to Signal:** The third positive ROC can still be Neutral (for example, ROC(14) at :gray-background[+1.10%]); it does not need to exceed the :gray-background[+3%] Buy threshold. Likewise, a negative crossover can occur without :blue-background[Sell] qualification. See [important pattern combinations](#how-to-interpret-roc-patterns-and-combinations).

### Confirmed bullish and bearish divergence
(:small[[Parent](#understanding-roc-secondary-metrics-and-events)])

The application now implements **confirmed price/ROC divergence**. Unlike one-bar Alignment, this is a comparison of **two consecutive confirmed price swing points of the same kind**. The price series selects the pivot dates; ROC is sampled on exactly those dates.

#### Pivot-date terminology
(:small[[Section](#confirmed-bullish-and-bearish-divergence)])

| Term | Plain-language definition | Why it matters |
|---|---|---|
| :blue-background[Prior pivot] | The earlier confirmed swing low or swing high | Starting point of the comparison |
| :blue-background[Current/new pivot] | The later confirmed swing of the **same kind** | Its price and ROC readings are compared with the prior pivot |
| :blue-background[Pivot date] | The trading session on which the price actually reached that swing extreme | The price extreme occurred **before** confirmation |
| :blue-background[Confirmation date] | The fifth subsequent observed trading session after the new pivot | By then the detector can verify five sessions on the right of the price extreme |
| :blue-background[Divergence event date] | The date the validated event is emitted; in this implementation, the new pivot's confirmation date | The visual mark and hover event appear **on confirmation**, never on the old pivot date |
| :blue-background[ROC at pivot] | The ROC reading on the respective **price-pivot** date | The detector does **not** independently choose ROC pivot dates |

#### How the 11-session price pivot is confirmed
> The detector uses an **11-observation window: 5 sessions before the candidate pivot, the pivot itself, and 5 sessions afterward**.

A candidate pivot is tested against the **5 preceding and 5 following observed price sessions**, making an 11-session window including the candidate itself.
- A :orange-background[qualifying 'price high'] must be **strictly higher than each of the ten neighbors**;
- a :orange-background[qualifying 'price low'] must be **strictly lower than each of the ten neighbors**
- Ties or missing neighboring prices prevent that candidate from becoming a qualified pivot.

The first five available sessions cannot establish a confirmed pivot, and a candidate from the last five available sessions cannot yet be confirmed. The detector uses the full available history, including sessions outside the displayed heatmap window.

---
#### Exact Divergence Requirements
(:small[[Section](#confirmed-bullish-and-bearish-divergence)])

| Type | Price-pivot requirement | ROC on those same pivot dates | Minimum differences | Visual |
|---|---|---|---|---|
| :blue-background[Bullish divergence] | **New lower price low** | **New higher ROC reading** at the new low | Price falls at least :gray-background[0.5%] from prior low **and** ROC rises at least :gray-background[0.5 pps] | **Blue numeric text** on event date |
| :blue-background[Bearish divergence] | **New higher price high** | **New lower ROC reading** at the new high | Price rises at least :gray-background[0.5%] from prior high **and** ROC falls at least :gray-background[0.5 pps] | **Red numeric text** on event date |

These use **consecutive qualifying price pivots of the same kind**. The price move is calculated as :gray-background[(new price / prior price − 1) × 100%]; the ROC difference is :gray-background[new ROC percentage − prior ROC percentage], measured in :blue-background[percentage points (pps)]. No standalone zero-line reset, volatility scaling, trend filter or crossover is required for divergence qualification.

---

**Compare consecutive confirmed price pivots of the same type:**

| Condition                   | Bearish divergence              | Bullish divergence              |
| --------------------------- | ------------------------------- | ------------------------------- |
| Price                       | Newer swing high is higher      | Newer swing low is lower        |
| ROC at corresponding pivots | Newer ROC is lower              | Newer ROC is higher             |
| Minimum price difference    | +0.50%                          | −0.50%                          |
| Minimum ROC difference      | −0.50 pps                       | +0.50 pps                       |
| Event date                  | Newer pivot +5 trading sessions | Newer pivot +5 trading sessions |


**The crucial timing rule:** The five later observations confirm the *price pivot*. They are not used to recalculate the ROC reading at that pivot.
The "***event date***" is reported on the confirmation date, while the comparative evidence remains attached to the two earlier pivot dates.

---
#### Worked bullish example and dates
(:small[[Section](#confirmed-bullish-and-bearish-divergence)|FYI: [Example: Positive 'Signal' with Bearish Divergence](#worked-example-b-positive-signal-with-bearish-divergence)])

Suppose the earlier confirmed price-pivot low is :gray-background[$100.00] with ROC :gray-background[−8.00%]. The newer price-pivot low is :gray-background[$98.50] with ROC :gray-background[−6.80%]:

| Observation | Earlier pivot | Newer pivot | Change |
|---|---:|---:|---:|
| Price low | :gray-background[$100.00] | :gray-background[$98.50] | :gray-background[−1.50%] |
| ROC at those price lows | :gray-background[−8.00%] | :gray-background[−6.80%] | :gray-background[+1.20 pps] |

Both minimum differences qualify. Yet the **blue number appears only when the newer pivot is confirmed**, five subsequent sessions after its date. If the new pivot were :gray-background[11/5] and confirmed :gray-background[11/12], the hover would identify **11/5 pivot, confirmed 11/12**. This distinguishes when the extreme happened from when the pattern could be known.

For :red[bearish divergence], reverse the geometry: a later higher price high combined with a lower ROC at that high, with both minimum differences met.

#### What Divergence means: and what it does not
(:small[[Section](#confirmed-bullish-and-bearish-divergence)])

Bullish divergence means the newest lower price low was accompanied by a **less negative or otherwise higher ROC** than the prior low. It can signal diminishing downside momentum at the price extreme. Bearish divergence means the higher price peak was accompanied by a **lower ROC** than the prior peak; upward thrust did not confirm the new high. Neither constitutes proof of a top, bottom or imminent reversal.

The divergence may coexist with **any** primary five-state Signal consistent with the current ROC value. When both a crossover and divergence qualify on the same date, the independent observations may **reinforce** one another or provide **mixed evidence**. The [Bottom-line](#how-to-read-the-dynamic-rule-and-context-interpretation) describes that relationship without changing the Signal.

### Relative Volume: 20 prior sessions
(:small[[Parent](#understanding-roc-secondary-metrics-and-events)])

:blue-background[Relative Volume (RVOL)] compares **today's traded volume** with the mean volume of the **20 preceding sessions**, excluding today from the denominator.

$$RVOL_{20}=\frac{V_t}{\operatorname{mean}(V_{t-1},\ldots,V_{t-20})}$$

| Hover reading | Concrete arithmetic | Meaning |
|---|---|---|
| :gray-background[1.50× (50% above average)] | :gray-background[15M] shares today / :gray-background[10M] prior-session mean | Today's activity is 50% higher than the reference average |
| :gray-background[0.60× (40% below average)] | :gray-background[6M] / :gray-background[10M] | Today's activity is 40% lower |
| :gray-background[1.00× (at average)] | :gray-background[10M] / :gray-background[10M] | Today's activity equals the reference average |

RVOL says **how much** traded relative to recent activity, not whether trades were mostly purchases or sales. Thus a Strong Buy with low RVOL remains Strong Buy, and heavy volume does not establish bullish participation. For directional participation, examine [CMF, MFI, OBV or the price/volume relationship](#value-added-use-and-complementary-indicators).

The reference requires **20 valid prior volume observations** and a **positive** prior average. Otherwise the RVOL hover line is omitted; unavailable RVOL is not :gray-background[0.00×].

### Historical ROC Standing: 120 observations
(:small[[Parent](#understanding-roc-secondary-metrics-and-events)])

:blue-background[Historical ROC Standing] describes how the current :blue-background[ROC(n)] reading ranks **within its own latest 120 consecutive valid ROC(n) readings**, **including today**. It is not a stock-price percentile or a percentile of all companies.

**Method:** The project counts readings strictly below today's ROC, counts tied readings, then uses **midrank** for ties:

$$Standing=100\times\frac{\text{count below}+0.5\times\text{count tied}}{120}$$

The hover rounds this to an integer percentile and separately reports the **number of those 120 readings strictly higher than today's reading**.

| Example | Meaning |
|---|---|
| :gray-background[90th percentile (~12/120 observations were higher)] | Today's ROC is high relative to the recent history; approximately 12 sessions had a **higher** ROC, while about 107 were **lower**, with today's reading accounting for the remaining observation in this no-ties-beyond-self illustration. |
| :gray-background[10th percentile (~108/120 were higher)] | Today's ROC is low relative to the recent history; roughly 108 observations had a **higher** ROC. |
| :gray-background[50th percentile] | Today's ROC is near the middle of its own 120-reading comparison distribution. |

For a concrete 90th-percentile illustration with no other tied readings, suppose :gray-background[107] readings are below today, :gray-background[1] reading is today's value itself, and :gray-background[12] readings are above. Midrank is :gray-background[(107 + 0.5) / 120 × 100 ≈ 89.6%], displayed as **90th percentile**. Out of approximately 120 sessions, 107 had a lower ROC and 12 a higher ROC; one is today's observation. Ties among other observations can change these exact counts.

**Critical interpretation:** A high positive ROC reading and a high Historical ROC Standing reading are related, but distinct. Standing describes *relative unusualness for that ticker and ROC lookback*, not a universal overbought reversal threshold. A historically high negative ROC might also be ranked differently depending on the comparison distribution; consult the **signed ROC value** first.

Standing is unavailable until **120 consecutive finite ROC readings** exist. A missing value interrupts the sequence. The hover omits standing when the window is not ready; it does not manufacture a neutral percentile. The 120-reading history is calculated **independently for each ROC period**.

### Missing, warmup and no-event behavior
(:small[[Parent](#understanding-roc-secondary-metrics-and-events)])

| Situation | What is established | How to interpret the display |
|---|---|---|
| Current ROC missing during warmup | The :gray-background[n]-session return cannot yet be calculated | No valid five-state classification; **Missing is not Neutral** |
| ROC valid but fewer than 120 consecutive ROC readings | Current Signal can be classified, but Standing is not ready | Standing field omitted; do not infer median or zero standing |
| Fewer than 20 valid preceding volume readings | RVOL reference is incomplete | RVOL field omitted; do not infer zero volume |
| No confirmed divergence displayed | No validated divergence event is supplied on this date | **May mean no qualifying event or insufficient historical prerequisites**; does not prove every pivot comparison was evaluable |
| No ▲ / ▼ displayed | No validated three-session sign-transition event on this date | A positive or negative ROC value may still persist without a fresh crossover |
| Missing preceding price or ROC | One-bar context is incomplete | Alignment and unsupported changes are omitted rather than invented |

A divergence readiness flag exists upstream, but it is not displayed as a complete guarantee of evaluability. Thus a blank Divergence field is **not** a definitive “no divergence possible” conclusion. See [Assumptions, limitations and safeguards](#assumptions-limitations-and-safeguards).

---

## How to interpret ROC patterns and combinations
(:small[[Back to top](#summary-roc-signals) | See Also: '[Practical ROC reading workflow](#practical-roc-reading-workflow)'; '[Understanding ROC Secondary Metrics and Events](#understanding-roc-secondary-metrics-and-events)'])

The same number can carry different information when paired with a fresh event.
- Read **Signal + ROC value + event evidence (crossovers/divergence)) + recent development (alignment/RVOL)** rather than treating one visual mark as an override (:small[See: '[6-Step ROC Reading Workflow](#6-step-roc-reading-workflow)']).

$$----------$$
A ROC heatmap cell can communicate three different types of information:

1. **Signal:** The five-state classification based on the magnitude of the current ROC reading.
2. **Divergence:** A confirmed comparison between two price pivots showing that ROC failed to confirm the latest price extreme.
3. **Zero-line Crossover:** A confirmed transition from negative to positive ROC, or positive to negative ROC, following three consecutive readings on the new side of zero.

These observations do not override one another. A :blue-background[Strong Buy] remains Strong Buy even when the numeric value turns red because bearish divergence was confirmed.

> See [Confirmed bullish and bearish divergence](#confirmed-bullish-and-bearish-divergence), [Confirmed zero-line crossovers](#confirmed-zero-line-crossovers), and [ROC Signal Rules](#roc-signal-rules-the-five-state-model) for the underlying rules.

### Four Categories for Interpreting Combinations
(:small[[Parent](#how-to-interpret-roc-patterns-and-combinations)])

| Scope | Meaning | Interpretation priority |
|---|---|---|
| **Reinforcing** | The current Signal and/or newly confirmed events point toward compatible directional developments. | Examine whether price behavior provides further support. |
| **Conflicting** | The Signal, divergence or crossover suggest different directional developments. | Investigate the tension before forming a directional conclusion. |
| **Early Watch** | A meaningful event is present, but the primary Signal remains Neutral or corroborating evidence is limited. | Monitor what develops next; do not promote the event to a stronger Signal. |
| **Routine** | No new confirmed event is highlighted. The existing ROC state remains informative. | Interpret the ongoing momentum state and recent ROC change. |

**Scope** describes how the evidence relates. **Relative attention** describes how important it may be to examine the observation.

A high-attention conflict can deserve closer investigation than a reinforcing pattern. Neither designation represents a measured probability of future price movement.

---
### Reference table: Signal with Confirmed Events
(:small[[Parent](#how-to-interpret-roc-patterns-and-combinations)])

| Current Signal | Confirmed event/context | Primary interpretation | What to watch |
|---|---|---|---|
| :blue-background[Strong Buy or Buy] | **[Bearish divergence](#confirmed-bullish-and-bearish-divergence) (${\textcolor{Red}{\textsf{red number}}}$)** | Upward lookback momentum remains qualified; latest higher price high was achieved with lower ROC at the new pivot. | Whether weakening thrust extends beyond the pivot comparison |
| :blue-background[Strong Sell or Sell] | **Bullish divergence (${\textcolor{DodgerBlue}{\textsf{blue number}}}$)** | Downward lookback momentum remains qualified; latest lower price low had higher ROC at the new pivot. | Whether subsequent downside price action stabilizes |
| :blue-background[Buy or Strong Buy] | **[Positive crossover ▲](#confirmed-zero-line-crossovers)** | Recently confirmed positive ROC sign, with the primary magnitude evaluated separately. | Whether positive ROC remains sustained; event does not make Signal stronger |
| :blue-background[Sell or Strong Sell] | **Negative crossover ▼** | Recently confirmed negative ROC sign, with independently qualified downside magnitude. | Whether downside thrust persists |
| :blue-background[Neutral] | **Positive crossover ▲** | Positive sign-transition event without sufficient positive magnitude to qualify Buy. | Whether ROC later moves beyond the period's positive cutoff |
| :blue-background[Neutral] | **Negative crossover ▼** | Negative sign-transition event without sufficient negative magnitude to qualify Sell. | Whether ROC later moves beyond the negative cutoff |
| :blue-background[Neutral] | **Bullish or bearish divergence** | Price-pivot disagreement exists even though today's ROC is within the Neutral band. | Price response after confirmation; do not infer automatic Buy/Sell |
| **Any valid Signal** | **Bullish divergence + positive crossover**, same date | Two independently confirmed observations point in a similar bullish direction. | Whether price and ROC subsequently support that interpretation |
| **Any valid Signal** | **Bearish divergence + negative crossover**, same date | Two independently confirmed observations point in a similar bearish direction. | Whether weakening momentum persists |
| **Any valid Signal** | **Bullish divergence + negative crossover** or **bearish divergence + positive crossover**, same date | Structural price/ROC disagreement and newly confirmed ROC sign transition point in **different** directions. | Treat evidence as mixed, not as a single directional verdict |
| **Any valid Signal** | No event; price/ROC Alignment disagrees | One-session price and momentum movements differ, but no formal pivot event is identified here. | Examine the longer history rather than promoting Alignment to divergence |

Some combinations are constrained by chronology and may be uncommon. The table explains **how to interpret them if displayed**, not how frequently they occur.

### How to prioritize the patterns
(:small[[Parent](#how-to-interpret-roc-patterns-and-combinations)])

| Sequence | Read this first | Why |
|---|---|---|
| **1 — Anchor** | Current ROC value and [five-state Signal](#roc-signal-rules-the-five-state-model) | Establishes actual lookback momentum magnitude |
| **2 — Fresh events** | $\large{▲/▼}$ and/or ${\textcolor{DodgerBlue}{\textsf{blue}}}$/${\textcolor{Red}{\textsf{red}}}$ ROC number | Reveals information the existing cell background cannot provide |
| **3 — Reconciliation** | Do [crossover](#interpretating-crossovers--divergence-together) and [divergence](#what-divergence-means-and-what-it-does-not) agree, or conflict? | Prevents overconfident interpretations from mixed evidence |
| **4 — One-bar movement** | Trend, Price direction, [Alignment](#roc-direction-and-one-session-alignment), absolute Δ in pps | Shows whether lookback momentum is improving or deteriorating today |
| **5 — Supporting context** | [RVOL](#relative-volume-20-prior-sessions) and [Historical ROC Standing](#historical-roc-standing-120-observations) | Adds participation magnitude and historical unusualness, without changing the score |
| **6 — Decision framing** | ['Dynamic Rule'](#how-to-read-the-dynamic-rule-and-context-interpretation), 'Context Interpretation' and 'Bottom-line' | Grounds the conclusion in the actual available evidence |

An additional caution: :gray-background[“positive ROC”] and :gray-background[“ROC increased today”] are not interchangeable. Nor is :gray-background[“bearish divergence”] the same as :gray-background[“Sell”].

---
### Key Patterns (ROC)
(:small[[Section](#how-to-interpret-roc-patterns-and-combinations) | Related: [The ROC patterns you should recognize immediately](#the-roc-patterns-you-should-recognize-immediately)])

#### Most Important ROC Patterns (6)
(:small[[Parent](#key-patterns-roc)])

- The following ranks reflect **interpretive information value and the need to investigate a development**, not backtested profitability or predictive reliability.
- Bullish and bearish mirror cases share the same rank.

| Rank                                                  | Pattern                                                                                                                                                                                                                                                                  | Scope                                                         | Relative attention | Why it deserves attention                                                                                                                                                                                                       | What to examine next                                                                                           |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **1:  Structural warning against qualified momentum** | <ol><li>:blue-background[Buy/Strong Buy] + ${\textcolor{Red}{\textsf{Bearish divergence}}}$ <li>:blue-background[Sell/Strong Sell] + ${\textcolor{DodgerBlue}{\textsf{Bullish divergence}}}$</ol>                                                                       | [Conflicting](#four-categories-for-interpreting-combinations) | **High — caution** | A meaningful lookback move remains qualified, but the latest confirmed price extreme was not supported by equivalent ROC momentum. <li>This reveals an important tension not evident from the Signal background. | Whether price loses support, fails to extend its high, stabilizes near its low or resumes the prevailing trend |
| **2:  Opposing Confirmed Events**                     | <ol><li>${\textcolor{DodgerBlue}{\textsf{Bullish divergence}}}$ + ▼<li>${\textcolor{Red}{\textsf{Bearish divergence}}}$ + ▲</ol>                                                                                                                                         | Conflicting                                                   | **High — mixed**   | Structural price/ROC evidence and the newly confirmed momentum-sign transition point in opposite directions. <li>A 'bullish' or 'bearish' conclusion based on only one annotation would be incomplete.           | Which development gains support from subsequent ROC and price behavior                                         |
| **3: Two confirmed 'Events' reinforce each other**    | <ol><li>${\textcolor{DodgerBlue}{\textsf{Bullish divergence}}}$ + ▲ <li>${\textcolor{Red}{\textsf{Bearish divergence}}}$ + ▼</ol>                                                                                                                                        | [Reinforcing](#four-categories-for-interpreting-combinations) | **High**           | The confirmed price-pivot disagreement and the confirmed ROC sign transition point toward a similar directional development. They add compatible evidence beyond the primary Signal.                                            | Whether price breaks a relevant level or sustains the newly established momentum direction                     |
| **4:  Neutral with a new Divergence Event**           | :blue-background[Neutral] + $\small{\textcolor{DodgerBlue}{\textsf{Bullish}}}$ or $\small{\textcolor{red}{\textsf{Bearish}}}$ (no crossover)                                                                                                                      | [Early Watch](#four-categories-for-interpreting-combinations) | **Medium–High**    | The Signal has not qualified as directional, yet a meaningful price-pivot nonconfirmation has just been confirmed. <li>The 'neutral' background alone would not communicate this development.                                   | Pivot dates, ROC differences, price structure and subsequent momentum                                          |
| **5:  Neutral with a new Zero-line Crossover**        | :blue-background[Neutral] **+** **▲ or ▼** (without divergence)                                                                                                                                                                                                          | Early Watch                                                   | **Medium**         | ROC has completed a 3-session 'sign' transition, but its magnitude remains within the period-specific 'Neutral' range. <li>Direction changed before a Buy/Sell threshold qualified.                                             | Whether ROC continues beyond the Neutral boundary or reverses toward zero                                      |
| **6 — Qualified momentum with aligned new evidence**  | 'Strong' with one qualifying event: <ol><li>:blue-background[Buy/Strong Buy] **+** ${\textcolor{DodgerBlue}{\textsf{Bullish divergence}}}$ or $\large{▲}$ <li>:blue-background[Sell/Strong Sell] + ${\textcolor{Red}{\textsf{Bearish divergence}}}$ or $\large{▼}$ </ol> | Reinforcing                                                   | **Medium**         | Existing directional momentum is accompanied by a compatible new observation, without an additional conflicting event. <li>Does not strengthen the assigned Signal score.                                                       | Persistence of momentum, price confirmation and whether the event is followed by continuation                  |

**How to use this table:** Start with the highest-ranked applicable observation. Multiple rows can apply to one cell; the ranking guides investigation rather than selecting one exclusive label.
- For example, if a :blue-background[Strong Buy] cell has :red[red numeric text] and ▲, the ongoing positive momentum and bullish crossover agree, but the bearish divergence is contrary evidence.

**Rank 1 takes interpretive priority because that conflict is the information the background and triangle do not reveal on their own.**

The [next three tables](#buy-and-strong-buy-signal--divergence--crossover) provide the fuller cross-reference.


#### BUY and STRONG BUY: Signal + Divergence + Crossover
(:small[[Parent](#key-patterns-roc)])

Both :blue-background[Buy] and :blue-background[Strong Buy] require a **positive ROC** beyond the relevant period threshold.

For ROC(14):
- :blue-background[Buy] means a gain greater than :gray-background[+3%] through :gray-background[+7%].
- :blue-background[Strong Buy] means a gain greater than :gray-background[+7%].

Therefore, a current negative crossover ▼ is **not compatible** with either Signal. The available confirmed crossover is ▲, or no crossover.

| Signal           | Divergence                                   |  Crossover  | Interpretation                                                                                                                                                                                                                                                       | Relative attention | Scope                                                         |
| ---------------- | -------------------------------------------- | :---------: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------------------------------- |
| Buy / Strong Buy | ${\textcolor{Red}{\textsf{Bearish}}}$        | $\large{▲}$ | Positive lookback momentum is qualified and a positive sign transition has just confirmed, but the latest higher price high had weaker ROC than the prior high. The new pivot evidence cautions against assuming the positive transition will continue unchallenged. | **High — caution** | [Conflicting](#four-categories-for-interpreting-combinations) |
| Buy / Strong Buy | ${\textcolor{Red}{\textsf{Bearish}}}$        |    None     | Meaningful positive lookback momentum persists, but the newest confirmed higher high lacks corresponding ROC strength. This is a warning about the quality of the advance, not proof of an imminent decline.                                                         | **High — caution** | Conflicting                                                   |
| Buy / Strong Buy | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$ | $\large{▲}$ | A confirmed lower price low with higher ROC is accompanied by a confirmed positive momentum-sign transition and qualified positive ROC magnitude. The observations support an improving momentum interpretation.                                                     | **High**           | [Reinforcing](#four-categories-for-interpreting-combinations) |
| Buy / Strong Buy | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$ |    None     | The current lookback return is positive and qualified, while the recent confirmed price-pivot comparison also showed improving ROC at a lower low. There is compatible evidence without a fresh crossover today.                                                     | **Medium–High**    | Reinforcing                                                   |
| Buy / Strong Buy | None                                         | $\large{▲}$ | ROC has confirmed positive sign for three sessions and already exceeds the Buy or Strong Buy magnitude threshold. This identifies a relatively pronounced positive transition, without a newly confirmed divergence.                                                 | **Medium**         | Reinforcing                                                   |
| Buy / Strong Buy | None                                         |    None     | Positive lookback momentum remains qualified. The magnitude determines Buy versus Strong Buy; no new event is highlighted today.                                                                                                                                     | Routine            | [Routine](#four-categories-for-interpreting-combinations)     |

**Example — :blue-background[Strong Buy] with red divergence**

Suppose a ROC(14) cell displays :gray-background[8.20] on a Strong Buy background, but the number is red.

The :gray-background[+8.20%] return exceeds the :blue-background[+7%] Strong Buy threshold. At the same time, a confirmed price high was higher than its preceding pivot high while ROC at that newer high was lower.

**Bottom-line:** Price has gained substantially over 14 sessions, but the most recent confirmed price-high comparison raises a warning about weakening upside momentum. Strong Buy remains the correct Signal; a reversal has not been established.

---

#### SELL and STRONG SELL: Signal + Divergence + Crossover
(:small[[Parent](#how-to-interpret-roc-patterns-and-combinations)])

Both :blue-background[Sell] and :blue-background[Strong Sell] require a **negative ROC** beyond the relevant threshold.

For ROC(14):

- :blue-background[Sell] means a decline greater than :gray-background[3%] through :gray-background[7%].
- :blue-background[Strong Sell] means a decline greater than :gray-background[7%].

A current positive crossover ▲ is **not compatible** with either Signal. The available confirmed crossover is ▼, or no crossover.

| Signal             | Divergence                                   | Crossover | Interpretation                                                                                                                                                                                                                                              | Relative attention | Scope                                                         |
| ------------------ | -------------------------------------------- | :-------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------------------------------- |
| Sell / Strong Sell | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$ |     ▼     | Downside momentum is qualified and a negative sign transition has confirmed, but the newer confirmed lower price low had a higher ROC than the previous low. Structural evidence suggests some easing at the price extreme despite the negative transition. | **High — caution** | [Conflicting](#four-categories-for-interpreting-combinations) |
| Sell / Strong Sell | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$ |   None    | The stock remains materially below its lookback comparison price, but the newer lower price low was accompanied by less-negative or otherwise higher ROC. Downside momentum at that extreme failed to confirm the new low.                                  | **High — caution** | Conflicting                                                   |
| Sell / Strong Sell | ${\textcolor{Red}{\textsf{Bearish}}}$        |     ▼     | A confirmed higher price high with lower ROC is accompanied by a confirmed negative momentum-sign transition and qualified downside magnitude. The observations support a deteriorating momentum interpretation.                                            | **High**           | [Reinforcing](#four-categories-for-interpreting-combinations) |
| Sell / Strong Sell | ${\textcolor{Red}{\textsf{Bearish}}}$        |   None    | Downside lookback momentum is qualified, and the latest confirmed higher price high exhibited weaker ROC. This adds structural support to the bearish interpretation without a new crossover today.                                                         | **Medium–High**    | Reinforcing                                                   |
| Sell / Strong Sell | None                                         |     ▼     | ROC has confirmed negative sign for three sessions and its magnitude already exceeds the Sell or Strong Sell threshold. A negative transition is established without newly confirmed divergence.                                                            | **Medium**         | Reinforcing                                                   |
| Sell / Strong Sell | None                                         |   None    | Negative lookback momentum remains qualified. The magnitude determines Sell versus Strong Sell; no new event is highlighted today.                                                                                                                          | Routine            | [Routine](#four-categories-for-interpreting-combinations)     |

**Example — :blue-background[Strong Sell] with blue divergence**

Suppose ROC(14) displays :gray-background[−8.50] with a Strong Sell background and blue numeric text.

The :gray-background[−8.50%] lookback return exceeds the :blue-background[−7%] Strong Sell threshold in downside magnitude. However, the newer confirmed price low is lower than the preceding price-pivot low while ROC at that newer low is higher.

**Bottom-line:** The 14-session decline remains substantial, but its newest confirmed lower-low comparison shows a potential easing of downside momentum at the price extreme. That is a warning to investigate, not evidence that price has already bottomed.

---

#### NEUTRAL: Signal + Divergence + Crossover
(:small[[Parent](#how-to-interpret-roc-patterns-and-combinations)])

A **[Neutral](#neutral-roc14)** ROC(14) reading falls within :gray-background[−3% to +3%], including both boundaries.

Neutral describes the **magnitude of the lookback return**, not the absence of momentum movement or secondary events.

Because :blue-background[Neutral] can contain positive and negative readings, either crossover direction is possible.

| Signal  | Divergence                                   |  Crossover  | Interpretation                                                                                                                                                                                                                                 | Relative attention | Scope                                                         |
| ------- | -------------------------------------------- | :---------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------------------------------- |
| Neutral | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$ | $\large{▼}$ | A lower confirmed price low had higher ROC, and the lookback return has now remained positive for three sessions following a negative reading. Two observations point toward improving momentum, despite insufficient magnitude for Buy.       | **High**           | [Reinforcing](#four-categories-for-interpreting-combinations) |
| Neutral | ${\textcolor{Red}{\textsf{Bearish}}}$        | $\large{▼}$ | A higher confirmed price high had lower ROC, and the lookback return has now remained negative for three sessions following a positive reading. Two observations point toward deteriorating momentum, despite insufficient magnitude for Sell. | **High**           | Reinforcing                                                   |
| Neutral | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$ | $\large{▼}$ | The latest confirmed lower price low shows improved ROC relative to the preceding low, but the current ROC has just confirmed negative sign. Structural evidence and current momentum direction disagree.                                      | **High — mixed**   | [Conflicting](#four-categories-for-interpreting-combinations) |
| Neutral | ${\textcolor{Red}{\textsf{Bearish}}}$        | $\large{▼}$ | The latest confirmed higher price high shows weaker ROC, but the current ROC has just confirmed positive sign. The observations point in different directions.                                                                                 | **High — mixed**   | Conflicting                                                   |
| Neutral | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$ |    None     | A newly confirmed lower price low had higher ROC than the prior low. That may indicate an early improvement in downside momentum at the pivot, but the current Signal remains Neutral.                                                         | **Medium–High**    | [Early Watch](#four-categories-for-interpreting-combinations) |
| Neutral | ${\textcolor{Red}{\textsf{Bearish}}}$        |    None     | A newly confirmed higher price high had lower ROC than the prior high. That may indicate weakening upside momentum at the pivot, but the current Signal remains Neutral.                                                                       | **Medium–High**    | Early Watch                                                   |
| Neutral | None                                         | $\large{▲}$ | ROC has completed a confirmed positive zero-line transition, but its gain is still too small to qualify Buy.                                                                                                                                   | **Medium**         | Early Watch                                                   |
| Neutral | None                                         | $\large{▼}$ | ROC has completed a confirmed negative zero-line transition, but its decline is still too small to qualify Sell.                                                                                                                               | **Medium**         | Early Watch                                                   |
| Neutral | None                                         |    None     | ROC remains inside the Neutral magnitude zone without a newly confirmed event. Its signed value and latest one-session movement can still provide context.                                                                                     | Routine            | [Routine](#four-categories-for-interpreting-combinations)     |

**Example — :blue-background[Neutral] with a confirmed ▲**

Suppose ROC(14) displays :gray-background[1.20] on a :blue-background[Neutral] background with a $\large{▲}$.

That means:

- The stock's 14-session lookback return is :gray-background[+1.20%].
- Three consecutive ROC observations have remained positive following a negative ROC observation.
- The crossover is confirmed on this third positive session.
- The :blue-background[+3%] Buy threshold has not been exceeded, so the Signal remains Neutral.

**Bottom-line:** Momentum has transitioned to positive territory, but the magnitude of the gain has not yet qualified as Buy. This is an early directional development, not a Strong Buy or a confirmed price reversal.


---
### Interpretating 'Crossovers' & 'Divergence' together
(:small[[Parent](#how-to-interpret-roc-patterns-and-combinations)])


| Important distinction                                                                                                              | Correct reading                                                                                                                                               |
| ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[Positive ROC](#roc-direction-and-one-session-alignment)** + ${\textcolor{Red}{\textsf{Bearish divergence}}}$                                                                    | Momentum may still be positive despite weakening thrust at the latest confirmed higher price high.                                                            |
| **[Negative ROC](#roc-direction-and-one-session-alignment)** + ${\textcolor{DodgerBlue}{\textsf{Bullish divergence}}}$                                                             | Momentum may still be negative despite improving ROC at the latest confirmed lower price low.                                                                 |
| ${\textcolor{DodgerBlue}{\textsf{Bullish divergence}}}$ + $\large{▲}$                                                              | The structural 'price-pivot' evidence and confirmed positive sign transition are compatible. They do not necessarily occur at the same underlying pivot date. |
| ${\textcolor{Red}{\textsf{Bearish divergence}}}$ + $\large{▼}$                                                                     | The structural price-pivot evidence and confirmed negative sign transition are compatible.                                                                    |
| ${\textcolor{DodgerBlue}{\textsf{Bullish divergence}}}$ + $\large{▼}$                                                              | A bullish pivot comparison conflicts with a newly confirmed negative momentum transition.                                                                     |
| ${\textcolor{Red}{\textsf{Bearish divergence}}}$ + $\large{▲}$                                                                     | A bearish pivot comparison conflicts with a newly confirmed positive momentum transition.                                                                     |
| Buy / Strong Buy + $\large{▼}$                                                                                                     | **Not a valid same-date ROC combination** under the current model.                                                                                            |
| Sell / Strong Sell + $\large{▲}$                                                                                                   | **Not a valid same-date ROC combination** under the current model.                                                                                            |
| No '**[divergence](#what-divergence-means-and-what-it-does-not)**' or '**[crossover](#confirmed-zero-line-crossovers)**' displayed | No validated event is shown on that date. This does not necessarily prove that every historical event-evaluation prerequisite was available.                  |

**Timing matters:** The divergence is displayed when the newer price pivot is confirmed, five trading sessions after the pivot itself. Its ROC comparisons use the two price-pivot dates, not necessarily the current day's ROC values. A crossover is displayed on its own third-session confirmation date.

Therefore, when divergence and crossover appear together, they are **separately defined observations, not two independent forecasts**.

The background 'Signal' remains controlled by the current ROC value alone.

See [Pivot-date terminology](#pivot-date-terminology), [Historical ROC Standing](#historical-roc-standing-120-observations) and [Understanding the ROC hover](#understanding-the-roc-hover) for supporting context.


### One-bar disagreement versus pivot divergence
(:small[[Parent](#how-to-interpret-roc-patterns-and-combinations)])

A disagreement between today's price movement and today's ROC change is **not the same as formal price/ROC divergence**. (:small[See: [ROC Direction and 1-session Alignment](#roc-direction-and-one-session-alignment)])

| Observation                            | Evidence required                                                          | What it establishes                                                       |
| -------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Price rose today and ROC fell          | Current and prior price/ROC observations                                   | Today's lookback momentum deteriorated even though price rose.            |
| Price fell today and ROC rose          | Current and prior price/ROC observations                                   | Today's lookback momentum improved even though price fell.                |
| Bullish divergence                     | Two consecutive confirmed price-pivot lows and qualifying ROC differences  | The newer lower price low was accompanied by a higher ROC at that pivot.  |
| Bearish divergence                     | Two consecutive confirmed price-pivot highs and qualifying ROC differences | The newer higher price high was accompanied by a lower ROC at that pivot. |

Use the [one-session Alignment](#roc-direction-and-one-session-alignment) field to understand the latest price-versus-ROC development. Use the confirmed Divergence field for the historical price-pivot comparison.

**Final reading principle:** First establish the current ROC Signal. Then inspect any new divergence and crossover evidence, reconcile whether those observations agree or conflict, and finally use price behavior, RVOL, Historical Standing and the dynamic hover interpretation to decide what deserves further investigation.

---

**Alternate Version**:
- The first two observations describe recent changes; the latter two describe **confirmed structural nonconfirmation**.
- Neither kind predicts a future outcome by itself.

| Observation | Required comparison | Valid conclusion |
|---|---|---|
| Price rose today and ROC(14) fell | Two adjacent price and ROC readings | Upside lookback momentum may be weakening on a **one-session** basis if ROC remains positive |
| Price fell today and negative ROC(14) rose | Two adjacent readings | Downside lookback momentum may be easing **today** |
| Higher confirmed price high + lower ROC at that later price high | Two **confirmed** price-pivot highs with required minimum differences | **Bearish divergence** event, dated at pivot confirmation |
| Lower confirmed price low + higher ROC at that later price low | Two **confirmed** price-pivot lows with required minimum differences | **Bullish divergence** event, dated at pivot confirmation |

---

## Understanding the ROC hover
(:small[[Back to top](#summary-roc-signals)])

The hover is the **evidence trail** behind the cell, not a second classifier. The current implementation uses source-verified explanations: if the active five-state rules, score or value fail validation against the approved ROC specification, it does not fabricate a dynamic ROC interpretation.

### Hover field map: what each line tells you
(:small[[Parent](#understanding-the-roc-hover)])

| Field | What it contains | How to interpret it |
|---|---|---|
| **Value** | Signed :gray-background[ROC(n)%] to two decimals; alongside ROC-canonical Price and daily Volume when available | Current :gray-background[n]-session return, **not** the score |
| **Δ vs prior day** | Change in ROC in **pps**; relative ROC change when meaningful; price and volume changes when available | Separates one-day changes from the multi-session ROC measurement |
| **Trend** | Rising/Falling/Flat ROC, optionally Price and Volume directions | Describes the **latest movement** of each series, not the ROC sign |
| **Alignment** | :gray-background[P(+/−/0)] and :gray-background[ROC(+/−/0)] with contextual words | One-session relationship, considering current ROC sign; **not** formal divergence |
| **Relative Volume (20 prior sessions)** | RVOL ratio and amount above/below average | Participation **amount**, not buy/sell pressure direction |
| **Signal** | Strong Buy, Buy, Neutral, Sell, Strong Sell | Rulebook classification; controls the background color |
| **Zero-line Crossover** | Positive/Negative, confirmed today on third new-side session | **Event-only** transition; absent when not confirmed today |
| **Divergence** | Bullish/Bearish, newer pivot date and confirmation date | **Event-only** structural price/ROC nonconfirmation |
| **Pivot highs/lows** | Prior and newer pivot dates/prices and price percentage difference | Reconstructs the price-side test for divergence |
| **ROC at those highs/lows** | ROC at both price-pivot dates and ROC difference in pps | Reconstructs the momentum-side test for divergence |
| **Rule** | Dynamic, verified explanation of the exact five-state qualification | Explains why the actual ROC value belongs to the current Signal |
| **Historical ROC Standing** | Percentile and count of 120 observations with higher ROC | Historical context for **this ticker and ROC lookback** |
| **Context Interpretation** | Available one-session change, confirmed events and RVOL context | Interprets the evidence; does not re-score |
| **Bottom-line** | Concise reconciliation, prioritizing event agreement or conflict when present | Qualified conclusion, not a forecast or trade recommendation |
| **Notes** | Period-specific rulebook guidance | Read-only interpretation tips; events remain context, not Signal |
| **Definition / How to Read** | Static indicator description and triangle/divergence legend | Shared indicator metadata, not calculated events |

Event and standing lines are **conditional**. A blank line for one of these metrics does not mean the numeric metric is zero or an event was conclusively impossible.

### Value, delta and Trend: read the units carefully
(:small[[Parent](#understanding-the-roc-hover)])

Suppose yesterday's ROC(14) was :gray-background[−7.65%] and today's was :gray-background[−8.45%]. The **absolute change** is:

$$-8.45\%-(-7.65\%)=-0.80\text{ percentage points}$$

The hover would show approximately :gray-background[−0.80 pps (−10.5%)], subject to display rounding. The :gray-background[−10.5%] is the relative change in the **ROC reading**, calculated against the absolute previous ROC magnitude; it is **not** the stock's one-day return.

| Reading | What it means |
|---|---|
| :gray-background[ROC −7.65% → −8.45%] | ROC fell :gray-background[0.80 pps]; negative momentum intensified |
| :gray-background[ROC −8.45% → −7.65%] | ROC rose :gray-background[0.80 pps]; negative momentum eased |
| :gray-background[ROC +0.20% → +1.20%] | :gray-background[+1.00 pps] absolute change, but :gray-background[+500%] relative change — a denominator effect |
| :gray-background[ROC −0.20% → +0.20%] | :gray-background[+0.40 pps] change across zero; **relative ROC percentage omitted** because the signs differ |
| Prior ROC missing or zero | Relative change may be omitted; insufficient prior evidence must not be invented |

In the completed ROC opening, relative ROC percentage is displayed only when both successive readings are nonzero and on the **same side of zero**. Price and volume deltas, when available, are separate quantities.

### How to read the dynamic Rule and Context Interpretation
(:small[[Parent](#understanding-the-roc-hover)])

**:blue-background[Rule]** answers: ***Which exact, active five-state conditions explain today's Signal?***
- For example, a ROC(14) reading of :gray-background[+5.60%] is Buy because it exceeds :gray-background[+3%] but not :gray-background[+7%].
- A :gray-background[Strong Buy] at :gray-background[+8.20%] is explained by its lookback gain exceeding the 'Strong' threshold—not by a fresh crossover or confirming volume.

**:blue-background[Context Interpretation]** answers: ***What else is happening that the Signal alone omits?***
- Depending on available evidence, it may describe price rising while ROC declines, a three-session crossover, newly confirmed pivot divergence, or volume above/below the prior-20-session average.

**'[Bottom-line](#how-to-read-the-dynamic-rule-and-context-interpretation)'** reconciles those facts.
- For example, a positive ROC with a bearish divergence retains its qualified positive Signal but warns that the latest higher price peak was reached with weaker ROC.
- If a crossover and divergence occur together, 'Bottom-line' highlights whether they **agree** or supply **mixed evidence**.
- Missing inputs result in narrower wording, not a fabricated conclusion.

### Worked hover interpretations
(:small[[Parent](#understanding-the-roc-hover)])

| Illustrative hover evidence | Appropriate interpretation |
|---|---|
| **ROC(14) +8.20%, Strong Buy; no confirmed event** | The lookback advance exceeds +7%. It does **not** establish a new crossover or divergence today. |
| **ROC(14) +5.60%, Buy; Price rose, ROC fell; bearish divergence confirmed** | Positive 14-session momentum persists, but the recent ROC reading weakened and the newer confirmed price high had lower ROC. The divergence is a structural caution, not an automatic Sell. |
| **ROC(14) +1.10%, Neutral; Positive crossover confirmed** | The lookback return crossed to the positive side and stayed there for three observations, but +1.10% has not exceeded the +3% Buy threshold. |
| **ROC(14) −5.40%, Sell; bullish divergence confirmed; RVOL 1.40×** | Negative lookback momentum remains qualified, while the latest lower price low had higher ROC. Today's volume is 40% above average, but RVOL alone does not identify directional participation. |
| **ROC(50) Strong Buy; Historical Standing unavailable** | The current 50-session return can be classified even though 120 consecutive ROC(50) observations are not yet available for a percentile. |

These are **teaching illustrations**, not reproduced live hover captures or claims about a named security.

### The three heatmaps and the Single Indicator chart
(:small[[Parent](#understanding-the-roc-hover)])

The **Rolling Signals Heatmap**, **SCD Single Indicator heatmap**, and **SCD Multiple Indicators heatmap** reuse the same underlying ROC rules, dated event evidence and adapter-owned hover interpretation. Layout and supplementary lines may differ, but their **ROC classification and event meaning must not**.

In **SCD Single Indicator**, the ROC trend chart's *Indicator value* mode displays ROC as a **percentage**. Its *change* mode expresses changes in **percentage points (pps)**. This is a display transform: the rule engine continues to use raw fractional ROC. The price chart is a separate price presentation and should not be mistaken for the ROC calculation basis without inspecting its source.

The shared authoritative static :blue-background[Definition] and :blue-background[How to Read] text comes from indicator metadata; period-specific :blue-background[Notes] comes from the active rulebook. These footer explanations do not override numeric results, classifier state, or event detection.

---

## Other parameter settings
(:small[[Back to top](#summary-roc-signals)])

Use the main [ROC(14) five-state explanation](#roc-signal-rules-the-five-state-model) as the teaching reference. The other settings use the **same formula, event families, RVOL method and historical-standing method**, evaluated against their own ROC observations. What changes is the **lookback** and, for ROC(9) and ROC(50), the **Signal thresholds**.

### Period comparison and practical selection
(:small[[Parent](#other-parameter-settings)])

| Period | Project category / role | Neutral | Strong cutoff | Practical use | Main trade-off |
|---|---|---|---|---|---|
| :blue-background[ROC(9)] | Short-term thrust detection | :gray-background[±2%] | :gray-background[beyond ±5%] | Spot faster price momentum shifts | More sensitive to short-lived moves |
| :blue-background[ROC(12)] | Short-term thrust detection | :gray-background[±3%] | :gray-background[beyond ±7%] | Broader short-term confirmation | Slightly less responsive than ROC(9) |
| :blue-background[ROC(14)] | Medium-term thrust detection | :gray-background[±3%] | :gray-background[beyond ±7%] | Main medium-term reference | Does not by itself distinguish trend quality |
| :blue-background[ROC(20)] | Medium-term thrust detection | :gray-background[±3%] | :gray-background[beyond ±7%] | Evaluate a more persistent move | Later reaction to fresh changes |
| :blue-background[ROC(50)] | Long-term thrust detection | :gray-background[±5%] | :gray-background[beyond ±10%] | Broad momentum backdrop | Larger accumulated moves can repeatedly qualify as Strong |

Periods are **different lenses on the same price history**, not five independent votes. ROC(9) might become negative during a pullback while ROC(50) remains positive; both observations can be valid.

### ROC(9): complete five-state signal table
(:small[[Parent](#other-parameter-settings)])

| Signal | Raw executable rule | Display range | Layman's translation |
|---|---|---|---|
| :blue-background[Strong Buy] | :blue-background[ROC_9 > 0.05] | :gray-background[above +5%] | Price rose more than 5% over nine sessions. |
| :blue-background[Buy] | :blue-background[ROC_9 > 0.02 and ROC_9 <= 0.05] | :gray-background[above +2%, through +5%] | Positive short-term thrust is meaningful but not Strong. |
| :blue-background[Neutral] | :blue-background[-0.02 <= ROC_9 <= 0.02] | :gray-background[−2% through +2%, inclusive] | The nine-session return is inside the middle band. |
| :blue-background[Sell] | :blue-background[ROC_9 >= -0.05 and ROC_9 < -0.02] | :gray-background[−5%, inclusive, to below −2%] | Negative short-term thrust is meaningful but not Strong. |
| :blue-background[Strong Sell] | :blue-background[ROC_9 < -0.05] | :gray-background[below −5%] | Price fell more than 5% over nine sessions. |

**Exact boundaries:** :gray-background[+2%] and :gray-background[−2%] remain Neutral; :gray-background[+5%] is Buy; :gray-background[−5%] is Sell. The narrower bands make this setting more responsive and potentially noisier. Strong states still require **only magnitude**, not a three-session crossover or ROC acceleration.

### ROC(12) and ROC(20): same calibration as ROC(14)
(:small[[Parent](#other-parameter-settings)])

| Setting | Strong Buy | Buy | Neutral | Sell | Strong Sell |
|---|---|---|---|---|---|
| :blue-background[ROC(12)] | :gray-background[>+7%] | :gray-background[>+3% to +7%] | :gray-background[−3% to +3%] | :gray-background[−7% to <−3%] | :gray-background[<−7%] |
| :blue-background[ROC(14)] | :gray-background[>+7%] | :gray-background[>+3% to +7%] | :gray-background[−3% to +3%] | :gray-background[−7% to <−3%] | :gray-background[<−7%] |
| :blue-background[ROC(20)] | :gray-background[>+7%] | :gray-background[>+3% to +7%] | :gray-background[−3% to +3%] | :gray-background[−7% to <−3%] | :gray-background[<−7%] |

Here :gray-background[>+3% to +7%] means **strictly greater than** :gray-background[+3%] and **at most** :gray-background[+7%]; the negative side mirrors that boundary rule. See [ROC(14) Rule summary](#rule-summary-roc12-roc14-roc20) for the complete literal expressions, applicable to each period after substituting its period number.

### ROC(50): complete five-state signal table
(:small[[Parent](#other-parameter-settings)])

| Signal | Raw executable rule | Display range | Layman's translation |
|---|---|---|---|
| :blue-background[Strong Buy] | :blue-background[ROC_50 > 0.10] | :gray-background[above +10%] | Price gained more than 10% over 50 sessions. |
| :blue-background[Buy] | :blue-background[ROC_50 > 0.05 and ROC_50 <= 0.10] | :gray-background[above +5%, through +10%] | Sustained positive return without exceeding Strong magnitude. |
| :blue-background[Neutral] | :blue-background[-0.05 <= ROC_50 <= 0.05] | :gray-background[−5% through +5%, inclusive] | Longer-horizon return remains inside the middle band. |
| :blue-background[Sell] | :blue-background[ROC_50 >= -0.10 and ROC_50 < -0.05] | :gray-background[−10%, inclusive, to below −5%] | Sustained negative return without exceeding Strong magnitude. |
| :blue-background[Strong Sell] | :blue-background[ROC_50 < -0.10] | :gray-background[below −10%] | Price fell more than 10% over 50 sessions. |

**Exact boundaries:** :gray-background[±5%] are Neutral; :gray-background[+10%] is Buy; :gray-background[−10%] is Sell. The :blue-background[±10% Strong threshold] is the currently approved rulebook calibration, **not a universal market standard**. Production diagnostics identified potential over-frequency of Strong Buy on some volatile growth stocks; recalibrating ROC(50), especially a higher Strong cutoff, remains a **deferred, separately validated task**, not a change made in this documentation revision.

### Interpreting disagreements across periods
(:small[[Parent](#other-parameter-settings)])

| Example | Meaning | Avoid concluding |
|---|---|---|
| :gray-background[ROC(9) −3%] and :gray-background[ROC(50) +12%] | Short-term pullback within a still-positive 50-session comparison | That the two indicators contradict mathematically |
| :gray-background[ROC(9) +6%] and :gray-background[ROC(50) −7%] | Recent bounce while longer-horizon return remains negative | That the longer downturn has already reversed |
| :gray-background[ROC(14) +2%] and :gray-background[ROC(50) +8%] | Positive returns at both horizons, but short/mid-term ROC is Neutral by its thresholds | That all positive ROC values receive Buy |

Use long-term ROC for **backdrop** and shorter ROC for **more recent change**, with trend and participation evidence for confirmation. Cross-period disagreement is not itself a formally scored divergence event.

---

## Value-added use and complementary indicators
(:small[[Back to top](#summary-roc-signals)])

ROC is useful when you want to quantify **direction and magnitude of a price move over a fixed lookback**, rather than relying on today's candle alone. It helps compare how far securities have moved, recognize fading or improving momentum and investigate whether a move is consistent across time horizons.

### What to combine with ROC
(:small[[Parent](#value-added-use-and-complementary-indicators)])

| Complementary tool | Question it answers that ROC alone does not | Example interpretation |
|---|---|---|
| :blue-background[EMA, SMA, HMA, VWMA] | Does ROC agree with the prevailing price-trend structure? | Positive ROC above a rising average strengthens the *trend-consistency* case; it does not validate a forecast. |
| :blue-background[ADX] | Is the trend strong or weak, independent of direction? | Large ROC during weak ADX deserves different context from large ROC during an established strong trend. |
| :blue-background[MACD] | How do faster and slower moving-average momentum relationships compare? | Positive ROC with deteriorating MACD may warrant checking weakening thrust. |
| :blue-background[RSI, STOCH, Williams %R] | Where does price or oscillator momentum sit relative to customary stretch/range benchmarks? | Strong Buy ROC does not itself mean overbought; these indicators supply different context. |
| :blue-background[CMF, MFI, OBV] | Is volume-backed participation consistent with the move? | Positive ROC + positive CMF may provide accumulation-side support; low RVOL alone cannot answer this. |
| :blue-background[Volume and RVOL] | How much participation is occurring relative to usual activity? | Strong positive ROC + :gray-background[0.60× RVOL] means the advance persists despite today's below-average volume. |
| :blue-background[ATR or ATRP] | Is the return large relative to the security's typical movement? | :gray-background[+7%] ROC may be routine for one ticker and unusual for another. |
| :blue-background[Price structure, support, resistance] | Where is the ROC change occurring on the actual chart? | Bearish divergence near an important price high may deserve attention; the pivot event still does not prove reversal. |

### Suggested order of corroboration
(:small[[Parent](#value-added-use-and-complementary-indicators)])

First establish the ROC Signal and timeframe. Then check **trend** (moving averages/ADX), **participation** (CMF/MFI/volume), **risk and stretch** (ATR/ATRP/RSI/STOCH), and finally **price structure**. These are separate observations; do not count closely related indicators as independent proof.

---

## Assumptions limitations and safeguards
(:small[[Back to top](#summary-roc-signals)])

### Project calibration and market conventions
(:small[[Parent](#assumptions-limitations-and-safeguards)])

| Conventional ROC property | Project-specific implementation choice |
|---|---|
| ROC compares current price with the price :gray-background[n] periods earlier | Five active periods: :gray-background[9, 12, 14, 20, 50] |
| ROC above/below zero means positive/negative lookback return | Period-specific Neutral bands and Strong thresholds |
| ROC is a price-momentum measure; it has no universal RSI-style overbought/oversold thresholds | Fixed five-state scores :gray-background[+2, +1, 0, −1, −2] |
| Momentum can remain positive while weakening, or negative while improving | Dynamic one-session Alignment, three-session crossover, and confirmed price-pivot divergence |
| Price adjustments can influence historical comparisons | ROC-specific adjusted-price preference and read-only hover evidence |
| A percentile describes location within a distribution | 120 consecutive-valid-reading **midrank**, reported per ROC period |

The current thresholds are **approved application rules**, not universally validated empirical optima. The ROC(50) Strong cutoff is explicitly subject to future production-path calibration. Do not interpret a Strong Buy as “overbought and due to decline,” or Strong Sell as “oversold and due to rebound.”

### Price-source and history safeguards
(:small[[Parent](#assumptions-limitations-and-safeguards)])

The ROC-specific calculation prioritizes Adjusted Close, falling back to Close, and uses that same series for divergence and ROC hover price evidence. This helps avoid treating corporate-action adjustments as ordinary price momentum, provided the historical price series is **consistently adjusted**.

A separate read-only database examination found actual Close-versus-Adjusted-Close differences for certain historical observations; choosing one series over the other changed some threshold classifications. The remaining question of consistent historical adjustment and refresh policy is **not resolved by the ROC semantic audit** and is tracked separately as a data-integrity matter. Accordingly, the document describes the **intended calculation contract**, not an independently certified history of every database record.

### Warmup, lookback and event lag
(:small[[Parent](#assumptions-limitations-and-safeguards)])

- :blue-background[ROC(n)] requires a valid current price and valid price :gray-background[n] observations earlier; early history is missing, not Neutral.
- :blue-background[Zero-line crossover] requires a genuine opposite-sign history followed by **three consecutive new-side ROC observations**; the event is dated at confirmation.
- :blue-background[Divergence] requires strict eleven-session price pivots and comparisons between consecutive same-type confirmed pivots; the new pivot becomes confirmable **five sessions later**.
- :blue-background[Historical ROC Standing] requires **120 consecutive valid ROC readings**, including today; a missing reading breaks readiness.
- :blue-background[RVOL] requires **20 valid earlier volume observations** and a positive historical mean.
- **No event displayed** is not proof that the entire detector was evaluable from all desired prior history. [Missing versus no event](#missing-warmup-and-no-event-behavior) explains the distinction.

### What ROC does not establish
(:small[[Parent](#assumptions-limitations-and-safeguards)])

| ROC can establish… | ROC cannot establish on its own… |
|---|---|
| Percent return across a chosen lookback | Fair value, expected return, or a guaranteed next-day direction |
| A project-defined magnitude classification | That a security must be bought or sold |
| Recent improvement or deterioration in ROC | That today's price moved in the same direction |
| A confirmed ROC sign-transition event | That a new trend is durable or that Strong magnitude qualified |
| A confirmed price-pivot ROC nonconfirmation | That a top, bottom or reversal is complete |
| Today's relative volume amount | Whether volume represented net accumulation or distribution |
| Recent ROC percentile standing | That a high-percentile observation must soon reverse |

ROC is unbounded on the positive side and approaches :gray-background[−100%] as a positive-priced asset falls toward zero. Its distribution differs across securities and lookbacks, so a fixed threshold does not represent the same statistical rarity everywhere. **Base effect:** an older large move exiting the rolling comparison window can alter ROC markedly, even if the latest day's move is small. A very small prior ROC can also generate a large *relative* ROC-change percentage; prefer the **absolute change in pps** near zero.

---

## Practical ROC reading workflow
(:small[[Back to top](#summary-roc-signals) | Related: [How to prioritize the patterns](#how-to-prioritize-the-patterns)])

This is the practical synthesis: use the background for the **state**, event marks for **new information**, and the hover to **reconstruct the evidence**. Complete the interpretation before drawing a market conclusion.

### A six-step reading sequence
(:small[[Parent](#practical-roc-reading-workflow)])

| Step | Action | The question you're answering |
|---|---|---|
| **1. Establish the horizon** | Confirm ROC(9), (12), (14), (20) or (50) | Over how many sessions is the percentage change measured? |
| **2. Read the number and background** | Value + Signal + period-specific cutoff | How large is current positive or negative momentum? |
| **3. Inspect new events** | $\large{▲/▼}$ and ${\textcolor{DodgerBlue}{\textsf{blue}}}$/${\textcolor{Red}{\textsf{red}}}$ numeric overlay | Did a confirmed sign transition or price-pivot disagreement occur **today**? |
| **4. Reconcile the evidence** | Compare event directions and one-bar Alignment | Do the observations reinforce one another or create caution? |
| **5. Add supporting context** | RVOL, Standing, trend, volume and price structure | Is the reading unusual or supported by other information? |
| **6. Verify the reason** | Dynamic Rule, Context Interpretation, Bottom-line | Can you explain the current state and any qualifications in plain language? |

### Worked example A: Positive momentum with no new event
(:small[[Parent](#practical-roc-reading-workflow)])

Suppose ROC(14) is :gray-background[+8.20%] with :blue-background[Strong Buy], and no crossover or divergence is displayed. The 14-session advance exceeds the :gray-background[+7%] Strong threshold. If today's ROC also rose, that is additional one-session improvement; the Strong classification, however, rests **only on magnitude**.

**Bottom-line:** Strong positive lookback momentum is established. No new event is identified for that date, which is different from saying momentum will continue or that every event test had full history.

### Worked example B: Positive Signal with bearish divergence
(:small[[Parent](#practical-roc-reading-workflow)])

Suppose ROC(14) reads :gray-background[+5.60%] and the number is **red**. The current Signal is :blue-background[Buy] because the gain is above :gray-background[+3%] but not above :gray-background[+7%]. The red number means a confirmed **higher price high / lower ROC at that price high** occurred on this date. The hover supplies both price-pivot dates, pivot values, the price percentage increase, the ROC decline in pps, and the date of confirmation.

**Bottom-line:** Qualified positive 14-session momentum persists, but the newer confirmed price peak has weaker momentum support. Treat the divergence as caution, not as a replacement Sell Signal.

### Worked example C: Downside momentum easing without reversal proof
(:small[[Parent](#practical-roc-reading-workflow)])

Suppose ROC(14) moved from :gray-background[−6.20%] to :gray-background[−5.40%] while price fell again today. The Signal remains :blue-background[Sell], because the 14-session return is below :gray-background[−3%] but not below :gray-background[−7%]. ROC **rose by +0.80 pps**, so negative momentum became less severe even though price declined. If a blue bullish divergence is also present, a separately confirmed later lower price low had a higher ROC than the earlier low.

**Bottom-line:** Downside momentum may be easing. Neither the rising negative ROC nor bullish divergence proves a completed price reversal.

### Worked example D: Neutral with a newly confirmed positive crossover
(:small[[Parent](#practical-roc-reading-workflow)])

Suppose ROC(14) followed :gray-background[−0.70% → +0.20% → +0.60% → +1.10%]. On the latest session the heatmap shows :blue-background[Neutral] and a black **▲**. The new positive run has now lasted three consecutive sessions, so the **positive zero-line crossover** is confirmed today. Yet :gray-background[+1.10%] remains below the :gray-background[+3%] Buy cutoff.

**Bottom-line:** A fresh positive momentum-direction transition is confirmed, but the 14-session return has not yet reached qualified Buy magnitude. The event adds information; it does not change the Neutral score.

### Final reading principle
(:small[[Parent](#practical-roc-reading-workflow)])

**A five-state rule is not finished if a human cannot reconstruct why an observation landed in each state.**
- For ROC, that means explaining the **exact lookback return and threshold first**, then distinguishing dated events and optional historical context from the authoritative Signal. A useful ROC conclusion should say what the evidence establishes, what remains uncertain, and what additional context would matter—without converting any single reading into a guaranteed trading prediction.

---
## Old Notes: ROC
(:small[[Back to top](#summary-roc-signals)])

**Purpose:** Measure the pure percentage change in price over a specified period to identify momentum acceleration or deceleration.
- Shows whether an asset is gaining or losing momentum by comparing current prices to historical ones.


- Measures the momentum of price changes. It compares the current price to a price ':gray-background[n]' periods ago.

---
**Basic Interpretation**:
- **+ROC**: indicates rising prices and potentially strong buying pressure (uptrend)
- **-ROC**: indicates falling prices and potentially strong selling pressure (downtrend)
- A value around zero suggests balanced momentum.

---
> The ROC oscillates above and below a zero line, which serves as a critical threshold for interpreting momentum:

- **Positive ROC (Above Zero Line):** Indicates upward price momentum  and potentially strong buying pressure (uptrend). The higher the ROC, the stronger the bullish trend.
- **Negative ROC (Below Zero Line):** Reflects downward price momentum (and potentially strong selling pressure (downtrend)), with increasingly negative values pointing to a stronger bearish trend.
- **ROC at Zero:** Suggests no price change over the given period, often seen in consolidating or sideways markets.

---
**Use when:** You want to measure raw momentum without smoothing, or identify when momentum is accelerating or slowing down.

**Key Concept:** Simple but powerful momentum measure that shows the percentage change from N periods ago. Positive values show upward momentum; negative values show downward momentum.

**Calculation:** :blue-background[ROC = [(Current Price - Price N periods ago) ÷ Price N periods ago] × 100], typically using 12 or 14 periods.

**Signals & Interpretation:**
- Positive ROC = upward momentum
- Negative ROC = downward momentum
- ROC above zero line = bullish bias
- ROC below zero line = bearish bias
- Extreme readings suggest momentum exhaustion
- Divergences with price indicate potential trend changes

**Application/Strategies**:

- **Overbought/sold**: Consider selling when ROC is high (overbought) and vice versa
- **Breakouts**: Look for price breakout accompanied by a riding ROC for confirmation.
- **Trend Reversals**: Look for price movement contradicting ROC for possible trend reversal.
- **Zero-line Crossovers**: A possible trend change might be signaled by ROC crossing above/below 0.


**Optimal Conditions:** Most effective in trending markets for confirming momentum direction. Works well on daily and weekly timeframes for trend analysis.

**Limitations:** Can be volatile and noisy without smoothing. Doesn't provide specific overbought/oversold levels like bounded oscillators.

**Complexity Level:** Beginner-friendly

---
**Strengths**:
- Highly responsive to price changes, giving traders quick insights into market dynamics.
- ROC is nearly identical to Momentum (MoM), with MOM expressing the change as a value.

**Best for**:
- **Confirming trend strength and direction** in trending markets.

**Limitations**:
- Can generate many false signals in volatile or choppy markets. Unlike RSI, it is not range-bound, so overbought and oversold levels must be determined visually.

---

> **Short-term trading**

For short-term strategies like day trading, a shorter period setting is used on a daily chart to capture rapid momentum shifts.

- **Recommended settings:** 7–14 periods.
- **Best for:** Identifying fast momentum changes, price breakouts, and potential short-term reversals.
- **Considerations:** A more sensitive setting increases false signals (whipsaws). It is critical to use additional confirmation tools, like moving averages, to filter out noise.

> **Medium-term trading (swing trading)**

Swing traders aim to capture price movements over several days to a few weeks. The best ROC setting is balanced, providing a mix of sensitivity and reliability.

- **Recommended settings:** 14–36 periods.
- **Best for:** Signaling potential entry points during pullbacks within an established trend.
- **Considerations:** You should combine the ROC with a trend filter, such as a 50-period moving average, to confirm the direction of the overall trend before acting on signals.

> **Long-term trading**

For long-term trend analysis, a longer ROC period smooths out short-term fluctuations to reveal the broader trend with greater reliability.

- **Recommended settings:** 36–200 periods.
- **Best for:**
    - Identifying the overall market trend and its strength.
    - Helping with long-term portfolio management by highlighting significant shifts in momentum.
- **Considerations:** A long look-back period is slower to react to changes, which means opportunities take longer to manifest.

---

## ToC: ROC
(:small[[Back to top](#summary-roc-signals)])

- **[Summary: ROC signals](#summary-roc-signals)**
  - [Primary signal summary: ROC(14)](#primary-signal-summary-roc14)
  - [Summary: Important ROC Patterns](#summary-important-roc-patterns)
  - [What the cell annotations mean](#what-the-cell-annotations-mean)
  - [Guide map](#guide-map)
- [The ROC patterns you should recognize immediately](#the-roc-patterns-you-should-recognize-immediately)
  - [Priority summary: what deserves attention first](#priority-summary-what-deserves-attention-first)
  - [At-a-glance combination examples](#at-a-glance-combination-examples)
- [ROC: brief overview](#roc-brief-overview)
  - [Simplest mental model](#simplest-mental-model)
  - [Formula and concrete calculations](#formula-and-concrete-calculations)
  - [What the price source means](#what-the-price-source-means)
  - [Threshold comparison: all five settings](#threshold-comparison-all-five-settings)
  - [The zero line is not the Signal threshold](#the-zero-line-is-not-the-signal-threshold)
- [How to read a ROC heatmap cell](#how-to-read-a-roc-heatmap-cell)
  - [Read the number, background and event marks separately](#read-the-number-background-and-event-marks-separately)
  - [Examples that prevent common misreadings](#examples-that-prevent-common-misreadings)
- [ROC Signal Rules: The five-state model](#roc-signal-rules-the-five-state-model)
  - [Rule summary: ROC(12), ROC(14), ROC(20)](#rule-summary-roc12-roc14-roc20)
  - [Strong Buy: ROC(14)](#strong-buy-roc14)
  - [Buy: ROC(14)](#buy-roc14)
  - [Neutral: ROC(14)](#neutral-roc14)
  - [Sell: ROC(14)](#sell-roc14)
  - [Strong Sell: ROC(14)](#strong-sell-roc14)
  - [Why boundary exclusivity and rounding matter](#why-boundary-exclusivity-and-rounding-matter)
- **[Understanding ROC secondary metrics and events](#understanding-roc-secondary-metrics-and-events)**
  - [ROC direction and one-session Alignment](#roc-direction-and-one-session-alignment)
  - [Confirmed zero-line crossovers](#confirmed-zero-line-crossovers)
  - [Confirmed bullish and bearish divergence](#confirmed-bullish-and-bearish-divergence)
    - [Pivot-date terminology](#pivot-date-terminology)
    - [How the 11-session price pivot is confirmed](#how-the-11-session-price-pivot-is-confirmed)
    - [Exact Divergence Requirements](#exact-divergence-requirements)
    - [Worked bullish example and dates](#worked-bullish-example-and-dates)
    - [What divergence means: and what it does not](#what-divergence-means-and-what-it-does-not)
  - [Relative Volume: 20 prior sessions](#relative-volume-20-prior-sessions)
  - [Historical ROC Standing: 120 observations](#historical-roc-standing-120-observations)
  - [Missing, warmup and no-event behavior](#missing-warmup-and-no-event-behavior)
- **[How to interpret ROC patterns and combinations](#how-to-interpret-roc-patterns-and-combinations)**
  - [Four Categories for Interpreting Combinations](#four-categories-for-interpreting-combinations)
  - [Reference table: Signal with confirmed events](#reference-table-signal-with-confirmed-events)
  - [How to prioritize the patterns](#how-to-prioritize-the-patterns)
  - [Key Patterns (ROC)](#key-patterns-roc)
    - [Most Important ROC Patterns (6)](#most-important-roc-patterns-6)
    - [BUY and STRONG BUY: Signal + Divergence + Crossover](#buy-and-strong-buy-signal--divergence--crossover)
    - [SELL and STRONG SELL: Signal + Divergence + Crossover](#sell-and-strong-sell-signal--divergence--crossover)
    - [NEUTRAL: Signal + Divergence + Crossover](#neutral-signal--divergence--crossover)
  - [Interpretating Crossovers & Divergence together](#interpretating-crossovers--divergence-together)
  - [One-bar disagreement versus pivot divergence](#one-bar-disagreement-versus-pivot-divergence)
- **[Understanding the ROC hover](#understanding-the-roc-hover)**
  - [Hover field map: what each line tells you](#hover-field-map-what-each-line-tells-you)
  - [Value, delta and Trend: read the units carefully](#value-delta-and-trend-read-the-units-carefully)
  - [How to read the dynamic Rule and Context Interpretation](#how-to-read-the-dynamic-rule-and-context-interpretation)
  - [Worked hover interpretations](#worked-hover-interpretations)
  - [The three heatmaps and the Single Indicator chart](#the-three-heatmaps-and-the-single-indicator-chart)
- [Other parameter settings](#other-parameter-settings)
  - [Period comparison and practical selection](#period-comparison-and-practical-selection)
  - [ROC(9): complete five-state signal table](#roc9-complete-five-state-signal-table)
  - [ROC(12) and ROC(20): same calibration as ROC(14)](#roc12-and-roc20-same-calibration-as-roc14)
  - [ROC(50): complete five-state signal table](#roc50-complete-five-state-signal-table)
  - [Interpreting disagreements across periods](#interpreting-disagreements-across-periods)
- [Value-added use and complementary indicators](#value-added-use-and-complementary-indicators)
  - [What to combine with ROC](#what-to-combine-with-roc)
  - [Suggested order of corroboration](#suggested-order-of-corroboration)
- [Assumptions limitations and safeguards](#assumptions-limitations-and-safeguards)
  - [Project calibration and market conventions](#project-calibration-and-market-conventions)
  - [Price-source and history safeguards](#price-source-and-history-safeguards)
  - [Warmup, lookback and event lag](#warmup-lookback-and-event-lag)
  - [What ROC does not establish](#what-roc-does-not-establish)
- [Practical ROC reading workflow](#practical-roc-reading-workflow)
  - [A six-step reading sequence](#a-six-step-reading-sequence)
  - [Worked example A: Positive momentum with no new event](#worked-example-a-positive-momentum-with-no-new-event)
  - [Worked example B: Positive Signal with bearish divergence](#worked-example-b-positive-signal-with-bearish-divergence)
  - [Worked example C: Downside momentum easing without reversal proof](#worked-example-c-downside-momentum-easing-without-reversal-proof)
  - [Worked example D: Neutral with a newly confirmed positive crossover](#worked-example-d-neutral-with-a-newly-confirmed-positive-crossover)
  - [Final reading principle](#final-reading-principle)
  - [Old Notes](#old-notes-roc)