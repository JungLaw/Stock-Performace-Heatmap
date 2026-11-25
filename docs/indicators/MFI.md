## Summary MFI Signals
:small[[Table of contents](#table-of-contents-mfi) | [Full Signal rules](#mfi-signal-rules-the-five-state-model) | [Understanding the hover](#understanding-the-mfi-hover)]

Often called "volume-weighted RSI", **[MFI](#mfi-my-notes)** uses both **'price' movement and trading 'volume'** to measure buying/selling pressure, making it more comprehensive than price-only oscillators.
- **Purpose:** Estimates positive versus negative price-and-volume-weighted money-flow pressure, often highlighting overbought/oversold conditions. 
- **Calculation:** Typical price = (High + Low + Close) ÷ 3; volume weights raw money flow, not typical price itself. 
- **Range:** Oscillates between 0 and 100. 
- **Signals:** Conventional reference levels often use 20/80. The app uses **15/25/75/85** for five-state Signals and **20/80** for failure swings.

---
> **Positive Money Flow:** :green-background[Typical price rises] + :orange-background[Volume] = ***Positive classified raw money flow***.
> **Negative Money Flow:** :red-background[Typical price falls] + :orange-background[Volume] = ***Negative classified raw money flow***.

- When positive raw-money-flow totals outweigh negative totals, MFI approaches 100; greater volume increases a session’s weight.
- When negative totals dominate, MFI approaches 0. These are modeled weights, not verified cash inflows/outflows.

---
The application interprets an unusually **low** MFI as a *contrarian oversold opportunity* and an unusually **high** MFI as *overbought risk*—not as an instruction to buy or sell.

**Start here:** The **cell background** answers *“Which five-state condition qualifies now?”*
- A "${\textcolor{DodgerBlue}{\textsf{blue}}}$/${\textcolor{Red}{\textsf{red}}}$ [number"](#how-to-read-an-mfi-heatmap-cell) or black [▲/▼](#mfi-failure-swings) identifies a separately confirmed event **on that cell's date**.
- '[Historical Standing](#historical-mfi-standing-252-sessions)', '[Volume Activity](#volume-activity-and-unusual-participation)', and '[Context Interpretation](#reading-rule-context-interpretation-and-bottom-line-together)' explain what the background alone misses. **None changes the Signal or score.**

### Primary Signal Summary
:small[[Detailed five-state explanations](#mfi-signal-rules-the-five-state-model)]

| Signal and score | Literal trigger for MFI(n) | Layman's translation | Rule logic | Bottom-line |
|---|---|---|---|---|
| [**Strong Buy (+2)**](#strong-buy-mfi) | :blue-background[MFI_n ≤ 15] | Very little positive flow versus negative flow over the window; severely oversold. | At/below 15; includes 15 exactly. | **Deep contrarian opportunity condition**, not a recovery confirmation. |
| [**Buy (+1)**](#buy-mfi) | :blue-background[15 < MFI_n ≤ 25] | Negative money flow predominates; oversold but less extreme. | Above 15, through 25 inclusive. | **Oversold opportunity condition.** |
| [**Neutral (0)**](#neutral-mfi) | :blue-background[25 < MFI_n < 75] | Neither project-defined extreme qualifies; flow need not be balanced. | Both 25 and 75 excluded. | **Non-extreme band—not necessarily unimportant.** |
| [**Sell (−1)**](#sell-mfi) | :blue-background[75 ≤ MFI_n < 85] | Positive money flow predominates; overbought. | From 75 inclusive, below 85. | **Contrarian overextension risk.** |
| [**Strong Sell (−2)**](#strong-sell-mfi) | :blue-background[MFI_n ≥ 85] | Exceptionally dominant positive flow; severely overbought. | At/above 85; includes 85 exactly. | **Deep overextension condition**, not a bearish turn confirmation. |

**All three settings—MFI(10), MFI(14), MFI(30)—use these exact bands.** Their rulebook column names are :blue-background[MFI_10], :blue-background[MFI_14] and :blue-background[MFI_30]. They classify the **current unrounded MFI value**, not yesterday's crossing, price direction, volume percentile, divergence or failure swing. A value that cannot be calculated is **Missing, not Neutral**. See [why boundaries and rounding matter](#exact-boundaries-persistence-and-missing-values).

### Summary Important MFI Patterns
(:small[[Patterns You Should Recognize Immediately](#the-mfi-patterns-you-should-recognize-immediately) | [Full combination reference](#complete-signal-and-event-combination-reference)])

| Priority | What you see | Why it matters | Inspect next |
|---|---|---|---|
| **1 — Structural conflict** | <li>:blue-background[Buy/Strong Buy] + [bearish divergence](#mfi-divergence) or ▼; <li> :blue-background[Sell/Strong Sell] + [bullish divergence](#bullish-divergence-worked-spy-example) or ▲ | Contrarian extreme and latest completed oscillator/price structure suggest different directions. | Dates, A/B/C/D or pivot evidence; [mixed-evidence reference](#complete-signal-and-event-combination-reference) |
| **2 — Compatible completed events** |<li> ${\textcolor{DodgerBlue}{\textsf{Blue value}}}$ + ▲, <li> ${\textcolor{Red}{\textsf{Red value}}}$ + ▼ | Two separately defined structural observations point the same way. | Whether their confirmation dates truly coincide; price/volume context |
| **3 — Neutral + confirmed event** | :blue-background[Neutral] with: <li>${\textcolor{DodgerBlue}{\textsf{Blue}}}$/${\textcolor{Red}{\textsf{Red}}}$ number or <li>▲/▼ | Something meaningful occurred without changing the middle-band classification. | Event mechanics and the [Bottom-line](#reading-rule-context-interpretation-and-bottom-line-together) |
| **4 — Severe extreme still worsening** | <li> :blue-background[Strong Buy] while MFI falls; <li>:blue-background[Strong Sell] while MFI rises | The contrarian extreme may be **intensifying**, not resolving. | Current versus prior MFI, price and [flow direction](#positive-and-negative-money-flow-balance). |
| **5 — Unusual Historical Standing** | :blue-background[Neutral] with MFI near its '252-session low/high' | Ticker-specific rarity and fixed Signal thresholds tell different stories. | [252-session rank/count](#historical-mfi-standing-252-sessions) |
| **6 — Entry, exit, persistence** | 'Entered Oversold' versus 'Oversold 4 sessions' | A fresh transition differs from sustained pressure. | [Zone history](#extreme-zone-entry-exit-and-duration); [Overbought/Oversold Levels](#understanding-divergence-failure-swings-and-overboughtoversold-levels) |
| **7 — Exceptional participation** | '120-session volume rank' :red-background[≤2.5th] or :red-background[≥97.5th] pct | Unusually light/heavy participation may qualify today's pressure or event. | [Volume Activity](#volume-activity-and-unusual-participation); direction of *typical price*. |
| **8 — No symbol or incomplete history** | Ordinary number, or Standing unavailable | No validated new event is displayed, or an evidence window is not ready. | [Missing versus no event](#missing-history-and-no-event-behavior) |

**Priority reflects interpretive information value, not backtested profitability or predicted returns.** Multiple patterns can apply to one observation.

### What the Cell Annotations Mean
:small[[Complete cell guide](#how-to-read-an-mfi-heatmap-cell)]

| What appears | Meaning | What it does **not** mean |
|---|---|---|
| **Background** (five-state color) | Current [MFI Signal](#mfi-signal-rules-the-five-state-model), scored +2/+1/0/−1/−2 | Prediction of tomorrow's price |
| **Printed number**, such as :gray-background[29.82] | Current MFI index value on a 0–100 scale | A percentage return, a score or a one-day change |
| ${\textcolor{DodgerBlue}{\textsf{Blue number}}}$ | Confirmed **bullish [price–MFI divergence](#bullish-divergence-worked-spy-example)** on this date | Automatically Buy or a confirmed price reversal |
| ${\textcolor{Red}{\textsf{Red number}}}$ | Confirmed **bearish** [price–MFI divergence](#mfi-divergence) on this date | Automatically Sell |
| $\large{\textcolor{black}{\textsf{▲}}}$ | Completed **[bullish failure swing](#bullish-failure-swing)** on this date | Price breakout or a change to the Signal |
| $\large{\textcolor{black}{\textsf{▼}}}$ | Completed **[bearish failure swing](#bearish-failure-swing)** on this date | Price breakdown or a change to the Signal |
| ${\textcolor{DodgerBlue}{\textsf{Blue}}}$/${\textcolor{Red}{\textsf{Red}}}$ + $\large{\textcolor{black}{\textsf{▲}}}$/$\large{\textcolor{black}{\textsf{▼}}}$ | Two independent event channels qualify on the same date | Two extra votes added to the score |
| **Ordinary number, no symbol** | No such *confirmed event shown today* | Proof that every historical test had enough data |

Colored numeric text and black arrows are independent of the background. When same-channel event directions would make a single color/arrow ambiguous, styling is suppressed rather than presenting a false unambiguous mark; validated event evidence remains the authoritative detail.

### Secondary Evidence at a Glance
:small[[Full calculations and examples](#understanding-mfi-secondary-metrics-and-events)]

| Evidence | Question it answers | Most useful clue | Read more |
|---|---|---|---|
| **[Price–MFI Divergence](#mfi-divergence)** | Did the newest confirmed price extreme have *less* supporting money-flow pressure? | Price lower low + nearby MFI higher low (bullish), or the reverse at highs. | [Mechanics and pivot dates](#confirmed-price-mfi-divergence) |
| **[Failure Swing](#mfi-failure-swings)** | Did MFI complete a recovery–retest–break pattern? | A/B/C/D and a crossing beyond B, independent of Signal. | [20/80 event sequence](#mfi-failure-swings) |
| **Historical MFI Standing** | How unusual is this MFI for the ticker and setting? | 0.6th pct can occur while Signal remains Neutral. | [252-session midrank](#historical-mfi-standing-252-sessions) |
| **Volume Activity** | Was today's participation unusual? | 1.33× 14D average and 94th pct answer different questions. | [Volume ratio and 120-session rank](#volume-activity-and-unusual-participation) |
| **[Zone entry / persistence](#understanding-divergence-failure-swings-and-overboughtoversold-levels)** | Is an extreme new, continuing or ending? | “Entered Oversold” vs “Oversold 4 sessions.” | [25/75 duration](#extreme-zone-entry-exit-and-duration) |
| **Flow balance / current raw flow** | Which pressure dominates the window, and what did *today* add? | MFI 25.56 implies ~74% negative classified flow. | [Rolling versus daily flow](#positive-and-negative-money-flow-balance) |
| **Daily MFI change and price** | Is the rolling pressure improving, deteriorating or disagreeing with price? | MFI may rise while today's raw flow is negative. | [Points, percent and Trend](#mfi-change-trend-and-one-session-price-relationship) |

### Six Step MFI Reading Workflow
:small[[Expanded examples](#practical-mfi-reading-workflow-and-worked-examples)]

| Step | Read | Question |
|---|---|---|
| **1** | Period and current value | Which 10-, 14-, or 30-session flow balance am I examining? |
| **2** | Signal/background and Rule | Exactly why did the five-state classification qualify? |
| **3** | ${\textcolor{DodgerBlue}{\textsf{Blue}}}$/${\textcolor{Red}{\textsf{Red}}}$ (['Divergence'](#mfi-divergence)) and $\large{\textcolor{black}{\textsf{▲}}}$/$\large{\textcolor{black}{\textsf{▼}}}$ ['Failure Swings'](#mfi-failure-swings) | Did a new confirmed structural event occur **today**? |
| **4** | Event dates, price lows/highs, nearby MFI or A/B/C/D | Can I reconstruct what qualified, and when it became knowable? |
| **5** | Standing, Volume Activity, MFI trend, extreme duration | Is pressure rare, newly changing, persisting or accompanied by unusual participation? |
| **6** | Context Interpretation + Bottom-line | How do the observations fit **together**, including conflicts? |

### Guide Map
:small[[Complete ToC](#table-of-contents-mfi)]

| I want to… | Go to… |
|---|---|
| Recognize the most important combinations | [Patterns to recognize immediately](#the-mfi-patterns-you-should-recognize-immediately) |
| Decode blue/red numbers, arrows and backgrounds | [How to read a cell](#how-to-read-an-mfi-heatmap-cell) |
| Understand an unfamiliar hover line | [Complete hover field map](#understanding-the-mfi-hover) |
| Understand MFI's arithmetic and what its number represents | [Overview and formula](#mfi-brief-overview-and-calculation) |
| Reconstruct a Signal's exact threshold | [Five-state rules](#mfi-signal-rules-the-five-state-model) |
| Learn A/B/C/D, Breakout, Nearby MFI Lows | [Secondary metrics and events](#understanding-mfi-secondary-metrics-and-events) |
| Reconcile events that agree or conflict | [Combination reference](#how-to-interpret-mfi-patterns-and-combinations) |
| Walk through real NVDA/SPY/MSFT observations | [Worked examples](#practical-mfi-reading-workflow-and-worked-examples) |
| Check other periods, limitations or complementary tools | [Periods](#mfi10-mfi14-and-mfi30) · [Safeguards](#value-added-use-complementary-indicators-and-safeguards) |

---

## The MFI Patterns You Should Recognize Immediately
:small[[Back to top](#summary-mfi-signals) | [Full combination reference](#how-to-interpret-mfi-patterns-and-combinations)]

An MFI cell reports **a condition** (the five-state Signal) and may also report **an event** (a confirmed divergence or failure swing). Neither replaces the other. A new event often deserves more attention than another day spent in the same extreme band.

### Priority Summary What Deserves Attention First
(:small[[Parent](#the-mfi-patterns-you-should-recognize-immediately)])

| Tier | What to recognize | Plain-language reading | What to examine next |
|---|---|---|---|
| **1 — Structural tension** | 'Buy/Strong Buy' + ${\textcolor{Red}{\textsf{bearish}}}$ [divergence](#mfi-divergence) or ▼; 'Sell/Strong Sell' + ${\textcolor{DodgerBlue}{\textsf{bullish divergence}}}$ or ▲ | **Opportunity/risk by level, but fresh structure points against that contrarian interpretation.** | The event's actual dates and B/breakout or price/MFI pivot comparison. |
| **2 — Two compatible events** | <li>${\textcolor{DodgerBlue}{\textsf{Blue number}}}$ + $\large{\textcolor{black}{\textsf{▲}}}$ <li>${\textcolor{Red}{\textsf{Red number}}}$ + $\large{\textcolor{black}{\textsf{▼}}}$ | Independent price-pivot nonconfirmation and oscillator completion support a similar directional reading. | Whether both qualified on the same date; the underlying data, not the symbol count. |
| **3 — Neutral with confirmed event** | 'Neutral' + any ${\textcolor{DodgerBlue}{\textsf{Blue}}}$/${\textcolor{Red}{\textsf{Red}}}$ number or ▲/▼ | The current MFI value is non-extreme, but a meaningful structural change has been confirmed. | [Divergence](#mfi-divergence) or [failure-swing steps](#mfi-failure-swings). |
| **4 — Severe extreme without relief** | 'Strong Buy' + falling MFI; 'Strong Sell' + rising MFI | [Deeply oversold/overbought](#extreme-zone-entry-exit-and-duration) is not synonymous with a turn. | Today's raw flow, relative volume, persistence and price. |
| **5 — Rare compared with own history** | Bottom/top :red-background[2.5%] of [252-session Standing](#historical-mfi-standing-252-sessions), potentially Neutral | This ticker/period is at an unusual position **even if** its project band has not changed. | Exact higher-count and recent MFI movement. |
| **6 — Extreme starts or persists** | Entered/Exited [Oversold or Overbought](#understanding-divergence-failure-swings-and-overboughtoversold-levels), or N sessions in zone | Fresh boundary event versus sustained condition. | Is pressure intensifying or easing while the same Signal persists? |
| **7 — Participation makes context unusual** | [Volume rank](#volume-activity-and-unusual-participation) at/beyond the 2.5% tails | Very low/high activity may qualify how much weight to place on today's pressure development. | Volume ratio and typical-price movement. |
| **8 — Ordinary / insufficient evidence** | No new annotation or missing Standing | Current Signal can still be valid; lack of an event may reflect no qualification or incomplete history. | Missing-data conditions, not an invented neutral event. |

**Tier is a reading priority, not a probability.** An unusual but conflicting observation may be more important to *investigate* than an apparently aligned one.

### At a Glance Combinations
(:small[[Parent](#the-mfi-patterns-you-should-recognize-immediately)])

| Observation you encounter | Useful first interpretation | Important distinction |
|---|---|---|
| :blue-background[Buy] + ${\textcolor{black}{\textsf{▼}}}$ | Oversold contrarian condition, **but** confirmed bearish oscillator breakdown. | See the [MSFT failure swing conflict](#example-f-msft-buy-with-bearish-failure-swing); no score change. |
| :blue-background[Sell] + $\small{\textcolor{DodgerBlue}{\textsf{bullish divergence}}}$ | Overbought risk while earlier lower price low saw improved nearby money-flow pressure. | The two observations concern different aspects/dates; [AAPL example](#example-g-aapl-sell-with-bullish-divergence). |
| :blue-background[Neutral] + $\small{\textcolor{DodgerBlue}{\textsf{bullish divergence}}}$ | A bullish [divergence](#mfi-divergence) exists even though the current index is inside 25–75. | [SPY pivot evidence](#example-d-spy-neutral-with-bullish-divergence). |
| :blue-background[Neutral] + ${\textcolor{black}{\textsf{▲}}}$ | A [bullish failure swing](#bullish-failure-swing) completed after a low/rebound/higher-low sequence. | [NVDA A/B/C/D](#example-e-nvda-bullish-failure-swing). |
| :blue-background[Strong Buy] + falling MFI | Deep oversold condition is getting **more** extreme. | Not automatically a bullish turning event. |
| :blue-background[Strong Sell] + rising MFI | Deep overbought pressure continues to intensify. | Not automatically a bearish reversal. |
| :blue-background[Neutral] + very low Standing | No project extreme, but very rare weakness relative to this ticker's 252 readings. | [SPY rare Neutral](#example-a-spy-neutral-with-rare-weak-flow). |
| $\small{\textcolor{DodgerBlue}{\textsf{Bullish divergence}}}$ + ${\textcolor{black}{\textsf{▼}}}$ | Bullish pivot evidence and bearish failure-swing structure coexist. | **Mixed directions**; don't reduce them to one bullish/bearish vote. |

### Questions Worth Asking After a Pattern Appears
(:small[[Parent](#the-mfi-patterns-you-should-recognize-immediately)])

Check **which date** the event belongs to, whether the current MFI is recovering or deteriorating, whether today's [volume participation](#volume-activity-and-unusual-participation) was unusually light/heavy, and whether the broader price trend agrees. A colored value or black triangle does **not** establish a completed price reversal.

---

## How to Read an MFI Heatmap Cell
:small[[Back to top](#summary-mfi-signals) | [Event mechanics](#understanding-mfi-secondary-metrics-and-events) | [Hover reference](#understanding-the-mfi-hover)]

### Read the Background Number and Symbols Separately

| Layer | Where to look | Correct reading |
|---|---|---|
| **Background/Signal** | Cell fill, and hover Signal/Rule | Current 15/25/75/85 band only: +2, +1, 0, −1 or −2. |
| **MFI number** | Center of cell | Current bounded **index value**, ordinarily to 2 decimals. Not a percent return. |
| **Blue or red number** | Number's font color, on a dated event cell | New confirmed bullish or bearish [price–MFI divergence](#confirmed-price-mfi-divergence). |
| **Black ▲ or ▼** | Next to the number | Completed bullish or bearish [20/80 failure swing](#mfi-failure-swings) on that date. |
| **Hover** | Move over the cell | Current value, daily changes, verified event evidence, Rule, Standing, Volume Activity and interpretation. |

The event marks are **one-day annotations**. They are not repeated on later dates just because the underlying oversold or overbought condition persists. They do not alter the z-score/background. A divergence number and failure-swing arrow may coexist in a cell, including where their directions conflict.

### Examples That Prevent Common Misreadings

| Cell appearance | Meaning | Do **not** conclude |
|---|---|---|
| :gray-background[12.00], Strong Buy, ordinary number | Current MFI is at/below 15: severely oversold. | Buyers have already regained control. |
| :gray-background[40.64], Neutral, **blue** number | Current value is Neutral; confirmed bullish divergence appeared on that date. | Neutral automatically becomes Buy. |
| :gray-background[22.00], Buy, ▼ | Oversold condition with a newly completed bearish failure swing. | The arrow must change the score to Sell. |
| :gray-background[76.15], Sell, **blue** number | Overbought current value and bullish divergence from earlier lows. | Either observation invalidates the other. |
| Blank/unavailable cell | No initialized value for classification. | Missing is the same as Neutral. |

**Timing example:** A lower price pivot occurred on 11/5 and became confirmable on **11/9** (two observed sessions later). A blue divergence number belongs to **11/9**, even though the price low was on **11/5**. See the [worked SPY example](#example-d-spy-neutral-with-bullish-divergence).

---

## Understanding the MFI Hover
:small[[Back to top](#summary-mfi-signals) | See Also: [Secondary Metrics](#understanding-mfi-secondary-metrics-and-events)]

The hover is a **compact evidence trail**, not a second scoring engine. The important question is whether the **Rule, Context Interpretation and Bottom-line together** tell a coherent story about an actual observation, rather than merely repeat the Value, Price and Volume rows.

### Hover Field Map
(:small[[Parent](#understanding-the-mfi-hover)])

| Field as displayed | What you are seeing | Why it matters / learn more |
|---|---|---|
| **Value** | MFI(n) to 2 decimals; available Price and daily Vol | Current 0–100 index and separately displayed price/participation. |
| **Δ vs prior day** | MFI-point change and relative %; corresponding price/volume changes | Shows new movement, **not** the MFI lookback return. [Units](#daily-change-units-and-trend). |
| **Trend** | Rising/Falling/Flat MFI plus price/volume movements | Direction of latest change; not the Signal itself. |
| **Signal** | Strong Buy / Buy / Neutral / Sell / Strong Sell | Current five-state score. [Exact rules](#mfi-signal-rules-the-five-state-model). |
| **Price–MFI Divergence** *(conditional)* | Bullish/Bearish; confirmation M/D | A confirmed nonconfirmation at newer price extreme. [How it qualifies](#confirmed-price-mfi-divergence). |
| **Price lows / highs** *(conditional)* | Earlier/newer price-pivot dates, prices and % change | Reconstructs the **price** side of divergence. |
| **Nearby MFI lows / highs** *(conditional)* | MFI extreme dates, values and index-point / relative-% change | Reconstructs the **money-flow** side of divergence; dates may differ from price pivots. |
| **Failure Swing** *(conditional)* | Bullish/Bearish, confirmation date, 20/80 model | Completed independent MFI oscillator pattern. [Stages](#mfi-failure-swings). |
| **A/B/C/D** *(conditional)* | Four MFI readings with their actual M/D dates | Initial extreme → rebound/trough → retest → completion. |
| **Breakout** *(conditional)* | Points past B and B's value/date; “marginal” when <0.05 pt | Shows exactly what level completed the swing. [Read an example](#bullish-failure-swing-worked-nvda-example). |
| **Rule** | Verified statement of which fixed threshold qualifies | Explains the **background/score**, not the event. |
| **Historical MFI Standing** | 252-reading percentile and count strictly higher | Reveals unusualness for the ticker and MFI period. [Calculation](#historical-mfi-standing-252-sessions). |
| **Volume Activity** | Current / period average ratio and 120-session volume percentile | Distinguishes today's volume spike from typical participation. [Calculation](#volume-activity-and-unusual-participation). |
| **Context Interpretation** | Concise, prioritized relationships: flow balance, unusual participation, transitions, event evidence | Explains **what's happening beneath the reading**. |
| **Bottom-line** | Short synthesis of Signal and other evidence | Highlights compatible, opposing or limited developments; **no score change**. |
| **Notes** *(heatmaps only)* | Short cross-check suggestion (SMA(200), OBV, RSI, Bollinger Bands) | Ideas for independent context, not additional MFI rules. |
| **Definition** *(heatmaps only)* | One-line 0–100 oscillator definition | Static reminder. |
| **How to Read** *(heatmaps only)* | Blue/red/▲/▼ legend and guide reference | Quick decoding; this guide supplies the detailed explanation. |

**Visibility:** The same analytical MFI content is shared by Rolling Signals Heatmap, SCD Single Indicator and SCD Multiple Indicators. The **Single Indicator Value Trend Chart** reuses the analytical fields **without Notes, Definition or How to Read**. The separate **Price Trend Chart is unaffected**. A chart's Score/other plotted-value mode is not a different MFI reading or score calculation.

### Daily Change Units and Trend
(:small[[Parent](#understanding-the-mfi-hover)])

MFI is a **unitless 0–100 index**. Its daily difference is measured in **MFI index points**, not percentage points (pps). The hover also displays the relative percentage change in the *MFI reading* when yesterday's value is greater than zero.

| Suppose… | Arithmetic | Correct interpretation |
|---|---|---|
| Yesterday MFI 20.00; today 22.00 | :gray-background[+2.0] points; :gray-background[+10.0%] relative | MFI improved 2 points; this is **not** a 10% stock return. |
| Yesterday 50.03; today 42.00 | :gray-background[−8.0 (−16.1%)] | MFI fell ~8 points; its reading declined ~16.1% relative to yesterday. |
| Yesterday 0; today 10 | :gray-background[+10.0], no valid relative % | Division by zero is not presented as a percent. |
| Yesterday 25.52; today 25.56 | :gray-background[+0.04] | The small real change should not be rounded into a misleading zero. |

The **Price** change uses its own currency/percentage units; **Vol** uses shares/volume units and its own daily relative percentage. MFI Trend reports *rising/falling/flat compared with yesterday*. It is not proof that today's classified raw money flow was positive or negative; see [how rolling flow can disagree with the latest session](#positive-and-negative-money-flow-balance).

### Reading Rule Context Interpretation and Bottom-line Together
(:small[[Parent](#understanding-the-mfi-hover)])

| Field | Question it should answer | Example |
|---|---|---|
| **Rule** | *Why did today's primary Signal qualify?* | MFI 25.56 is above 25 and below 75 → Neutral. |
| **Context Interpretation** | *What meaningful condition/development is not obvious from the score?* | Negative flow ~74% of 14D balance; heavy volume added negative flow even though rolling MFI edged up. |
| **Bottom-line** | *What matters when those facts are combined?* | Neutral by threshold, but flow near the 252-session low; downside pressure elevated. |

Do **not** read the three fields as interchangeable. “Strong Buy” is the project's **contrarian** response to severe negative flow, not proof that raw money flow or price has turned positive. A completed bearish failure swing may conflict with a Buy state; the Bottom-line should identify that tension without hiding either observation.

**Real conflict example:** MSFT MFI(10) at 22.00 on 10/23/26 was **Buy**, yet a **bearish failure swing** completed that day. Rule explains the oversold band. Context explains the failed rebound/break below an earlier oscillator trough, with exceptionally light volume. Bottom-line reconciles the oversold opportunity and worsening MFI structure as mixed evidence. [Walkthrough](#example-f-msft-buy-with-bearish-failure-swing).

### Read Event Lines Before Interpreting Them
(:small[[Parent](#understanding-the-mfi-hover)])

A dated event block is **not an explanation of the entire current price trend**. Its price-pivot values may come from days earlier, and its MFI extrema may be on *nearby but different* days. For a failure swing, A/B/C/D are **MFI values**, not price points; the Breakout refers to **MFI crossing B**, not stock-price resistance. [Read the divergence mechanics](#confirmed-price-mfi-divergence) and [failure-swing mechanics](#mfi-failure-swings) before using these fields as evidence.

---

## MFI Brief Overview and Calculation
:small[[Back to top](#summary-mfi-signals) | [Rules](#mfi-signal-rules-the-five-state-model)]

### The Simplest Mental Model
(:small[[Parent](#mfi-brief-overview-and-calculation)])

MFI asks: **“Across the latest n trading sessions, has price-weighted trading activity been classified mainly as positive or negative money flow?”**

A positive-flow session has a **higher typical price** than the prior session; a negative-flow session has a **lower typical price**. More trading volume gives that session a larger weight. MFI compares the *rolling totals*, then expresses their balance from 0 to 100.

This is why MFI adds something to a price-only indicator such as [RSI](#useful-complementary-indicators): it incorporates volume in the measurement. But it **does not directly measure cash entering/exiting the market, count buyer versus seller shares, or identify institutional transactions**.

### Calculation With Real Units
(:small[[Parent](#mfi-brief-overview-and-calculation)])

| Step | Calculation | Meaning |
|---|---|---|
| **1. Typical Price (TP)** | :gray-background[(High + Low + Close) ÷ 3] | Represents each session by its observed H/L/Close average. |
| **2. Raw Money Flow (RMF)** | :gray-background[TP × Volume] | Price-weighted traded activity for that session. |
| **3. Assign sign** | If TP > prior TP → positive RMF; if TP < prior TP → negative RMF; if equal → neither | Classification uses **typical price**, **not** Close-to-Close direction. |
| **4. Add flows** | Sum positive and negative classified RMF over **n** sessions | Requires eligible price/volume comparisons. |
| **5. Compute MFI** | :gray-background[100 × Positive Sum ÷ (Positive Sum + Negative Sum)] | Positive share of the total classified raw flow, expressed on a 0–100 scale. |

Equivalent conventional form:

$$\mathrm{MFR}_n=\frac{\sum \text{Positive RMF}}{\sum \text{Negative RMF}},\qquad \mathrm{MFI}_n=100-\frac{100}{1+\mathrm{MFR}_n}.$$

The application's implementation uses explicit handling of zero denominators: **100** if only positive flow exists, **0** if only negative flow exists; if both sums are zero, MFI is **undefined/missing**, not Neutral (50). A session with missing inputs is not secretly treated as zero flow.

### Two Concrete Calculations
(:small[[Parent](#mfi-brief-overview-and-calculation)])

**Single session:** Suppose High = $102, Low = $98, Close = $101, Volume = 2M shares. TP = :gray-background[(102 + 98 + 101)/3 = $100.33]; RMF ≈ :gray-background[$200.67M price×share units]. If prior TP was $99.50, the session contributes to the **positive** sum. If prior TP was $101, it contributes to the **negative** sum. These are modeled activity weights, **not literal dollars of net inflows**.

**Full-window balance:** Suppose the 14-session positive RMF sum is :gray-background[26 weighted units] and negative sum is :gray-background[74]. Then MFI = :gray-background[100 × 26/(26+74) = 26.00]. In other words, **negative flow accounted for ~74% of the classified activity in the window**. This is an intuitive interpretation of a low MFI reading, not a statement that 74% of actual trades were sells.

| MFI reading | Positive / negative modeled balance | Broad reading |
|---|---|---|
| :gray-background[12] | ~12% / 88% | Severe negative-flow dominance; Strong Buy *contrarian* band |
| :gray-background[25.56] | ~25.6% / 74.4% | Substantial negative tilt, despite technically Neutral (>25) |
| :gray-background[50] | ~50% / 50% | Balanced modeled classified flow |
| :gray-background[78] | ~78% / 22% | Positive-flow dominance; overbought Sell band |
| :gray-background[90] | ~90% / 10% | Severe positive-flow dominance; Strong Sell *contrarian* band |

### Why a Negative Session Can Accompany Rising MFI
(:small[[Parent](#mfi-brief-overview-and-calculation)])

MFI measures a **rolling** total. When a new session enters, the oldest classified session drops out. Therefore today's typical price can fall and add **negative raw flow**, while the total window's balance still improves because an even larger old negative-flow session just left. Likewise, today's positive raw flow does not guarantee a rising MFI. This distinction is built into the hover's [Context Interpretation](#reading-rule-context-interpretation-and-bottom-line-together).

### Comparing MFI, RSI, and CMF
(:small[[Parent](#mfi-brief-overview-and-calculation) | Related: [Useful Complementaty Indicators](#useful-complementary-indicators)])

| Indicator | Primary question | Why it is not interchangeable with MFI |
|---|---|---|
| **MFI** | How is the rolling **price-and-volume** balance distributed between positive and negative typical-price sessions? | Bounded, volume-weighted contrarian oscillator. |
| **RSI** | How does the magnitude of recent price gains compare with losses? | Price momentum without MFI's volume weighting. |
| **CMF** | Where has price closed within its range, weighted by volume, over the window? | Different accumulation/distribution proxy; not the same TP-change sign assignment. |

### Price Basis and Complete-Window Requirements
(:small[[Parent](#mfi-brief-overview-and-calculation)])

MFI's raw flow uses **High, Low, Close and Volume**. The separate MFI hover **Price** comparison may use Adjusted Close when that series is available, otherwise Close; confirmed bullish divergence compares actual **Low** pivots, and bearish divergence compares actual **High** pivots. **These are distinct inputs by design**. The price basis printed for context should not be assumed to equal the price used inside MFI's typical-price calculation.

An MFI(n) requires **n valid classified flow sessions**, each with a current and preceding finite typical price and eligible volume; the earliest MFI(n) generally appears only after at least **n+1 complete OHLCV observations**. Missing inputs interrupt readiness. See [missing-history safeguards](#missing-history-and-no-event-behavior).


---
## Understanding MFI Secondary Metrics and Events
:small[[Back to top](#summary-mfi-signals) | [Secondary evidence at a glance](#secondary-evidence-at-a-glance) | [Worked examples](#practical-mfi-reading-workflow-and-worked-examples)]

These measurements answer questions the primary Signal cannot. They come from **full available chronological history**, not merely the 20/40 cells currently visible. Some are a **persistent condition**, some a **one-session development**, and divergence/failure swings are **one-date confirmed events**. None changes the +2/+1/0/−1/−2 score.

The most important are Divergence, Failure Swings and Overbought/Oversold Levels.

### Understanding 'Divergence', 'Failure Swings' and 'Overbought/Oversold Levels'
(:small[[Parent](#understanding-mfi-secondary-metrics-and-events)])

**Overbought and oversold levels** can be used to identify [overbought/oversold extremes](#extreme-zone-entry-exit-and-duration). Typically, MFI above 80 is considered overbought and MFI below 20 is considered oversold. The app uses **15/25/75/85** for five-state Signals and **20/80** for failure-swing setup levels.
Strong trends can present a problem for these classic overbought and oversold levels.
- MFI can become overbought (>80) and prices can simply continue higher when the uptrend is strong.
- Conversely, MFI can become oversold (<20) and prices can continue lower when the downtrend is strong.

Quong and Soudack also described more stringent 90/10 extremes; these are conventional references, not the app’s five-state thresholds.
- **Readings above 90 or below 10 reflect more extreme modeled flow imbalance, not proof that the price move is unsustainable.**

**Note:**
- Many stocks will trade for a long time without reaching the 90/10 extremes.
- Oversold levels alone are not reason enough to turn bullish.
  - Some sort of reversal or upturn is needed to confirm that prices have indeed turned a corner.
  - Example: [NKE (Chart School](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/money-flow-index-mfi#overbought_oversold)

---
Both **[Failure Swings](#mfi-failure-swings)** and **[Divergences](#mfi-divergence)** can be used to identify potential price reversals.

**BULLISH SIGNALS**
- A ${\textcolor{DodgerBlue}{\textsf{bullish divergence}}}$ forms when prices move to a lower low, but the indicator forms a higher low to show improving money flow or momentum.
- A [bullish failure swing](#bullish-failure-swing) occurs when MFI becomes oversold below 20, surges above 20, holds above 20 on a pullback, and then breaks above its prior reaction high.
- Both are bullish structural observations in a downtrend; they may warrant investigating a reversal but do not confirm one.

**BEARISH SIGNALS**
- Conversely, a ${\textcolor{Red}{\textsf{bearish divergence}}}$ forms when the stock forges a higher high and the indicator forms a lower high, which indicates deteriorating money flow or momentum.
- A [bearish failure swing](#bearish-failure-swing) occurs when MFI becomes overbought above 80, plunges below 80, fails to exceed 80 on a bounce and then breaks below the prior reaction low.
- Both are bearish structural observations in an uptrend; they may warrant investigating a reversal but do not confirm one.

When divergence and failure swing complete on the same date **and agree in direction**, they provide compatible structural evidence. Their predictive advantage has not been established, and neither changes the five-state score.
- Example: [NKE (Chart School](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/money-flow-index-mfi#divergences_and_failures)

---

### MFI 'Divergence'
(:small[[Parent](#understanding-mfi-secondary-metrics-and-events) | See: [Understanding 'Divergence', 'Failure Swings' and 'Overbought/Oversold Levels'](#understanding-divergence-failure-swings-and-overboughtoversold-levels)])

MFI divergence compares **two confirmed price swing highs or lows** with **nearby MFI highs or lows**. A newer price extreme without matching MFI pressure is structural nonconfirmation, not a one-day price/MFI disagreement or a proven reversal.

$\large{\textsf{Types of MFI Divergence}}$

|Type|Price Action|MFI Action|Signal|
|---|---|---|---|
|**Bullish Divergence**|Makes a **lower low**|Forms a **higher low**|Downward selling pressure is drying up; potential **upward reversal**.|
|**Bearish Divergence**|Makes a **higher high**|Forms a **lower high**|Upward buying volume is weakening; potential **downward reversal**.|

---

$\large{\textsf{How it works in practice}}$

1. **Identify a clear price swing:** Look for an established uptrend making new highs or a downtrend making new lows.
2. **Compare with MFI peaks/troughs:** Check whether the MFI confirms the price extreme or fails to match it. Because MFI incorporates volume, divergence can indicate weaker **modeled money-flow pressure** at the newer extreme; it does not measure actual cash inflows.
3. **Wait for confirmation:** A divergence alone can persist during strong trends. Traders typically wait for a break in market structure (such as a trendline break, moving average cross, or an MFI failure swing) before acting.

---

$\large{\textsf{Divergence vs. Failure Swing}}$

- **Divergence** compares **price highs/lows against MFI highs/lows**.
- **[Failure swing](#mfi-failure-swings)** looks **exclusively at MFI's own structure** around the 20 and 80 thresholds, ignoring whether price made a new extreme.
- **Combined evidence:** When both complete in the same direction, they reinforce the structural interpretation. An opposite-direction pairing is conflicting, not automatically stronger.

---
#### Confirmed Price MFI Divergence
:small[[Parent](#mfi-divergence) | [SPY example](#bullish-divergence-worked-spy-example)]

**Question:** *Did price set a new confirmed swing extreme while nearby MFI showed **less** pressure in that same direction?*

A :blue-background[bullish divergence] occurs when **price makes a lower confirmed low**, but the **nearby MFI low is higher** than at the prior confirmed price low. This suggests negative flow was *less severe* at the later price extreme. A :blue-background[bearish divergence] is the mirror: **price makes a higher confirmed high**, but the **nearby MFI high is lower**, suggesting buying pressure failed to match the higher peak.

##### Pivot Dates and Confirmation Terms
(:small[[Parent](#confirmed-price-mfi-divergence)])

| Term in the hover | Meaning in plain language | Why it matters |
|---|---|---|
| **Prior price pivot** | The earlier qualifying swing low (bullish) or swing high (bearish) | Starting price extreme for comparison. |
| **Newer/current price pivot** | The later qualifying swing of the **same type** | Its price must extend the prior extreme. |
| **Pivot date** | Session on which price actually reached that high or low | The extreme occurred **before** the engine could confirm it. |
| **Nearby MFI low/high** | Lowest/highest MFI within two sessions before/after the corresponding price pivot | The MFI extreme can occur on a **different date** from the price extreme. |
| **Confirmation date** | The session **two observed trading sessions after** the newer price pivot | The engine now has the right-hand observations to verify the pivot. |
| **Divergence event date** | The newer price pivot's confirmation date | **Blue/red value appears here**, never backpainted onto the pivot. |

The detector uses a **strict five-observation price pivot**: **two sessions before + the candidate + two sessions after**. A low must be **strictly below** all four neighbors; a high must be **strictly above** them. Ties or missing necessary data prevent a valid candidate. It compares **consecutive qualifying, confirmed price pivots of the same type**.

For each price pivot, the detector independently inspects the **five MFI observations centered on that price-pivot date**; for lows, it takes the minimum, and for highs, the maximum. All five MFI observations must be finite for the comparison. If a repeated equal MFI extreme occurs in the window, the selected date is the one nearest the price pivot (earlier date resolves an equal-distance tie).

##### Exact Divergence Qualification
(:small[[Parent](#confirmed-price-mfi-divergence)])

| Event | Price-side condition | MFI-side condition | What is displayed |
|---|---|---|---|
| **Bullish** | Newer confirmed **Low** strictly below prior confirmed Low | Nearby MFI minimum at newer pivot **strictly above** the previous pivot's nearby minimum | **Blue** current MFI number on the confirmation date |
| **Bearish** | Newer confirmed **High** strictly above prior confirmed High | Nearby MFI maximum at newer pivot **strictly below** the previous pivot's nearby maximum | **Red** current MFI number on the confirmation date |

There is **no separate minimum price-% change or MFI-point-difference gate** in the approved MFI divergence test. The strict inequalities, pivot geometry, complete local windows and two-session confirmation govern qualification. Do **not** copy ROC's 11-session price pivots or its 0.5%/0.5-pps magnitude tests into MFI.

##### Bullish Divergence Worked SPY Example
(:small[[Parent](#confirmed-price-mfi-divergence)]) | (:small[Other 'Bullish divergence' examples': ['Neutral'](#example-d-spy-neutral-with-bullish-divergence); ['Sell'](#example-g-aapl-sell-with-bullish-divergence)])

SPY MFI(14) produced a confirmed bullish divergence on **11/9/26**:

| Comparison | Earlier swing | Newer swing | Change |
|---|---:|---:|---:|
| **Price lows** | **10/30:** $750.36 | **11/5:** $732.71 | **−2.4%** |
| **Nearby MFI lows** | **10/30:** 33.30 | **11/6:** 39.43 | **+6.13 points / +18.4%** |

The price low fell by approximately :gray-background[($732.71 ÷ $750.36 − 1) × 100 = −2.4%]. Yet the nearby MFI minimum **rose**, from 33.30 to 39.43. Thus the new lower price low occurred with **less severe negative money-flow pressure**.

**Why are the dates different?** The 11/5 **price** pivot is compared with the lowest **MFI** reading in its 11/3–11/9 five-session neighborhood. In this example that MFI low was on **11/6**. Two subsequent trading observations confirmed the 11/5 price pivot by **11/9**; the blue number therefore appears **11/9**, not 11/5 or 11/6.

**What it adds:** The 11/9 MFI value was :gray-background[40.64], **Neutral** by the project's bands. The blue number adds information that the Neutral background cannot: at the later price low, modeled downside pressure was easing. **It does not prove that price has bottomed**.

For the bearish mirror, read **price highs** and **nearby MFI highs**: a later higher price high with a lower nearby MFI high is a red-number event. The logic and two-session confirmation timing are otherwise symmetric.

##### What Divergence Is Not
(:small[[Parent](#confirmed-price-mfi-divergence)])

A price rise today combined with a falling MFI today is a **one-session disagreement**, **not** a formal divergence. Formal divergence requires two confirmed price pivots and two nearby MFI-extreme comparisons. A divergence reflects *previous swing evidence* and can coexist with a current Neutral, Buy or Sell because the classifier does not depend on it.

### MFI 'Failure Swings'
(:small[[Parent](#understanding-mfi-secondary-metrics-and-events) | See: [Understanding 'Divergence', 'Failure Swings' and 'Overbought/Oversold Levels'](#understanding-divergence-failure-swings-and-overboughtoversold-levels)])

A failure swing on the Money Flow Index (MFI) is a [four-step reversal signal](#the-four-stages-abcd) formed solely by the indicator's own peaks and troughs after hitting extreme levels, without needing price divergence.

#### Bullish Failure Swing
(:small[[Parent](#mfi-failure-swings) | Ex: [NVDA](#bullish-failure-swing-worked-nvda-example)])

Signals potential upward reversal as selling pressure weakens:
1. MFI drops below 20 (oversold).
2. MFI bounces back above 20.
3. MFI pulls back but stays above 20 (or forms a higher low).
4. MFI breaks above its prior reaction high.

#### Bearish Failure Swing
(:small[[Parent](#mfi-failure-swings) | [Example](#bearish-failure-swing-example)])

Signals potential downward reversal as buying momentum fades:
1. MFI rises above 80 (overbought).
2. MFI drops below 80.
3. MFI rebounds slightly but fails to reclaim 80 (forming a lower high).
4. MFI breaks below its prior reaction low.

#### Failure Swing: Key Characteristics & Usage
(:small[[Parent](#mfi-failure-swings)])

• **Self-contained pattern**: Unlike divergence, it compares MFI swings against MFI itself rather than price swings.
• **Confirmation trigger**: Breaking the prior high (bullish) or prior low (bearish) acts as the confirmation step.
• **Related terms**: Traders also refer to this pattern as a swing failure or oscillator swing failure (adapted from J. Welles Wilder's RSI failure swing)

---
**Question:** *Has MFI completed a recognizable low–rebound–higher-low–breakout sequence, or its high-side mirror?*

Unlike divergence, a **failure swing is an MFI-only pattern**: it does not require price pivots. The engine uses **conventional MFI 20/80 reference levels**, independently of the project's **15/25/75/85 Signal bands**. The visual arrow appears **only when the final strict crossing completes**—not when A, B or C first forms.

#### The Four Stages A/B/C/D
(:small[[Parent](#mfi-failure-swings)])

| Stage | **Bullish failure swing** (black ▲) | **Bearish failure swing** (black ▼) |
|---|---|---|
| **A — Initial extreme** | MFI reaches **≤20** (oversold low). | MFI reaches **≥80** (overbought high). |
| **B — Initial recovery** | MFI rises above 20 to an interim **rebound high**. | MFI falls below 80 to an interim **recovery trough**. |
| **C — Retest** | MFI pulls back, holds a **higher low above A** and stays **above 20**. | MFI rebounds, holds a **lower high below A** and stays **below 80**. |
| **D — Completion** | MFI moves **strictly above B**, confirming a bullish event today. | MFI moves **strictly below B**, confirming a bearish event today. |

The final inequalities are **A ≤20 < C < B < D** for bullish and **A ≥80 > C > B > D** for bearish. The detector tracks the active episode chronologically; during development it may update interim extrema. Returning to the original extreme or an opposite extreme can reset/supersede an unfinished setup. A missing/invalid MFI observation resets its state. **A developing A/B/C is not a confirmed failure swing.**

The arrow is a **one-day completion marker**, not a persistent “uptrend” or “downtrend” symbol. The event may be complete while the primary Signal is still Neutral.

#### Bullish Failure Swing Worked NVDA Example
(:small[[Parent](#mfi-failure-swings) | ['Bullish Failure Swing'](#bullish-failure-swing)])

NVDA MFI(14), using the **refreshed November 23, 2026** accepted observation:

| Stage | Date | MFI displayed | What happened |
|---|---|---:|---|
| **A** | **11/10** | **19.29** | Initial oversold low at/below 20. |
| **B** | **11/11** | **29.77** | MFI rebounded; this becomes the level that must be broken. |
| **C** | **11/20** | **20.60** | Pullback held above A and above 20; a higher low. |
| **D** | **11/23** | **29.82** | MFI exceeded the earlier B level; **black ▲** appears. |

**Reading the hover:**

> **Failure Swing:** Bullish; confirmed 11/23 (20/80 model)
> **A/B/C/D:** 19.29 (11/10) → 29.77 (11/11) → 20.60 (11/20) → 29.82 (11/23)
> **Breakout:** +0.06 pt above prior MFI rebound high (29.77, 11/11).

**Why +0.06 instead of subtracting displayed 29.82 − 29.77 = 0.05?** Confirmation and Breakout use **unrounded source MFI values**; the four A/B/C/D readings are rounded for display. The underlying difference can therefore differ by ~0.01 from arithmetic on the two printed numbers.

**Why it matters:** MFI recovered from an extreme, held a higher low, then cleared its earlier rebound level. This is a completed **bullish oscillator structure** even though today's MFI :gray-background[29.82] remains **Neutral** under the project's five-state thresholds. Exceptionally heavy volume on the completion day adds **participation context**, not a second confirmation gate.

**A marginal crossing still qualifies.** For a separate *illustrative* case, if unrounded B = 29.770 and unrounded D = 29.780, the Breakout is :gray-background[+0.01 pt] and the hover may append **“marginal”** (absolute difference below 0.05 pt). There is **no minimum magnitude beyond a strict crossing**. Do not confuse that illustrative +0.01 with the refreshed NVDA +0.06.

#### Bearish Failure Swing Example
(:small[[Parent](#mfi-failure-swings)])

Consider a bearish A/B/C/D with **A 80.85 → B 65.64 → C 73.68 → D 57.73** (observed in the XLY MFI(14) event family). MFI initially reached overbought territory, fell to its recovery trough B, rebounded to a **lower high** C, then fell **below B**. The black ▼ belongs to D's completion session. The Breakout explains **how far below B**, and displays B's **date** when recorded.

**What it adds:** The bearish pattern records a **failed recovery and subsequent oscillator breakdown**. It can coexist with a Neutral current MFI value and does not prove that stock price has begun a sustained decline.

#### Timing Eligibility and Nonqualification
(:small[[Parent](#mfi-failure-swings)])

| Situation | What the application can honestly conclude |
|---|---|
| MFI touches ≤20 or ≥80 but no full A/B/C/D completes | **Developing or no event**, not a confirmed arrow. |
| Bullish D equals B exactly | **No strict breakout**; ▲ does not qualify on equality. |
| Bearish D equals B exactly | **No strict breakdown**; ▼ does not qualify on equality. |
| Completed D is 29.82 and primary Signal Neutral | **Valid**; the 20/80 event and 25/75 Signal are independent. |
| Prior MFI observation missing/invalid | Setup state is reset; do not connect unrelated observations across the gap. |
| Same-date divergence also qualifies | The number may be colored **and** have a black arrow. Read each event separately. |

### Historical MFI Standing 252 Sessions
:small[[Back to top](#summary-mfi-signals) | [SPY rare Neutral example](#example-a-spy-neutral-with-rare-weak-flow)]

**Question:** *How unusual is today's MFI(n) relative to this ticker's own MFI(n) history?* Standing is **not** a stock-price percentile, cross-ticker ranking, score or extra Buy/Sell threshold.

The comparison uses the **latest 252 consecutive valid MFI(n) observations, including today**. It counts observations below the current value and ties, then calculates a **midrank**:

$$\mathrm{Standing}_{252}=100\times\frac{\#(MFI < MFI_{today})+0.5\,\#(MFI=MFI_{today})}{252}.$$

The hover reports Standing to **one decimal**, plus the number of the 252 readings **strictly higher** than today. A missing MFI in the comparison window invalidates Standing until a complete 252-reading window becomes available again.

**Real SPY example:** MFI(14) = :gray-background[25.56] on **11/19/26** was approximately **0.6th percentile**, with **250/252 observations higher**. In this no-additional-ties example, **1** reading was lower, **1** was today's reading, and **250** were higher. Midrank = :gray-background[(1 + 0.5)/252 × 100 ≈ 0.6%].

**Interpretation:** Neutral by fixed threshold (>25), yet near the **very bottom** of SPY's own 252-session MFI range. That is meaningful downside-pressure context—*not* automatic Buy, proof of a bottom, or a forecast. A value near the 99th percentile is the corresponding high-side rarity.

**Why the denominator includes today's observation:** Standing ranks the current reading **among 252**, so the current value is itself one observation. The higher-count is strictly greater; with other tied readings, lower/equal/higher counts must be considered before translating a percentile into exact session counts.

### Volume Activity and Unusual Participation
:small[[Back to top](#summary-mfi-signals) | [Flow direction](#positive-and-negative-money-flow-balance)]

**Question:** *How much trading took place today relative to normal activity for this ticker?*

This is relevant because **volume enters the MFI calculation**, but volume magnitude and **positive/negative flow direction are separate**.

Two readings appear in the same field:

| Hover component | Computation | What it adds |
|---|---|---|
| **Relative-to-average volume** | Today's volume ÷ average of the **last n** valid volumes, **including today** (n = 10, 14 or 30) | Shows whether participation is larger/smaller than the selected MFI period's recent average. |
| **120-session volume percentile** | Rank of today's volume within the **latest 120 consecutive sessions with valid volume, including today**, scaled to 0–100; ties receive average rank | Shows whether this session's volume is unusual relative to longer recent history. |

**Example — SPY 11/19/26 MFI(14):** :gray-background[1.33× 14D avg | 94th pct (120 sessions)]. Volume was roughly **33% above** its 14-session average; at the 94.2nd-percentile unrounded rank. In the observed 120-session comparison, **112 sessions had lower volume, 1 was equal (today), and 7 were higher**. This is a statement about participation *amount*, not direction.

**Exceptional-volume commentary:** The engine explicitly calls out the **inclusive tails**—rank **≤2.5th percentile** (exceptionally light) or **≥97.5th percentile** (exceptionally heavy)—using the **unrounded** rank. For ordinary ranks, volume is mentioned selectively when it changes the interpretation. A value displayed as “2nd pct” or “98th pct” is rounded; the eligibility check is not.

| Illustration | Correct reading | Do not assume |
|---|---|---|
| :gray-background[0.70× 10D avg · 2nd pct] | About 30% below its 10-session average; exceptionally light relative to 120 sessions. | A bearish failure swing on that date is invalidated. |
| :gray-background[1.89× 14D avg · 100th pct] | Nearly 89% above its average; exceptionally heavy participation. | The trades were necessarily bullish. |
| :gray-background[1.00× 30D avg · 60th pct] | Near period average but moderately above the middle of 120-session ranks. | Both measures are equivalent. |

The ratio needs a complete **n-session volume window** and nonzero mean. The percentile needs a complete **120-session window**. Missing volume invalidates the affected comparison windows; unavailable must not be reported as zero. Also, unlike ROC's **20 preceding sessions** RVOL, MFI's period average **includes today**.

### Extreme Zone Entry Exit and Duration
:small[[Back to top](#summary-mfi-signals) | See: [Understanding 'Divergence', 'Failure Swings' and 'Overbought/Oversold Levels'](#understanding-divergence-failure-swings-and-overboughtoversold-levels) | [NVDA duration example](#example-h-nvda-zone-entry-and-persistence)]

**Question:** *Did MFI just enter/leave an extreme, or has the pressure persisted?* The additional context uses the project's **≤25 Oversold** and **≥75 Overbought** zones, separately from the failure swing's 20/80 setup.

| Hover wording | Literal condition | What it tells you |
|---|---|---|
| **Entered Oversold today** | Prior MFI >25; current MFI ≤25 | A **new zone entry**, not necessarily a Buy after an upward cross. |
| **Exited Oversold today** | Prior MFI ≤25; current >25 | Leaves oversold zone; may have merely moved to Neutral. |
| **Entered Overbought today** | Prior MFI <75; current ≥75 | Fresh overbought condition. |
| **Exited Overbought today** | Prior MFI ≥75; current <75 | Leaves overbought; not an automatic bearish event. |
| **Oversold 4 sessions** | Four consecutive valid MFI readings ≤25 | Persistent pressure; distinguish from entry day. |
| **Overbought ≥N sessions** | Available history shows at least N consecutive ≥75; earlier start unknown | **Lower bound**, not an exact onset date. |

Consecutive duration resets when a reading is outside the zone or missing. A zone transition requires **both current and preceding valid MFI**; with no predecessor, the engine does not fabricate an “Entered” label. A direct leap from ≤25 to ≥75 can register **both** exit and entry, because both boundaries were crossed.

**Real NVDA contrast:** On **11/17/26**, MFI(14) = **23.73**, with **“Entered Oversold today.”** On **11/20/26**, MFI(14) = **20.63**, with **“Oversold 4 sessions.”** Both days qualified Buy. The additional text explains *when the pressure started* and *how long it persisted*, information the unchanged Buy background could not convey.

### Positive and Negative Money Flow Balance
:small[[Back to top](#summary-mfi-signals) | [MFI formula](#calculation-with-real-units)]

**Question:** *What proportion of the rolling price-weighted activity is classified positive versus negative, and what did this session add?*

An MFI(n) of :gray-background[25.56] directly implies a modeled balance of **~25.6% positive versus ~74.4% negative** classified raw flow over the n-session window. That's why “Negative flow ~74% of 14D balance” can be a better interpretation than merely “MFI is low.” It does **not** mean 74% of shares traded were sells.

Today's raw-flow **direction** is determined by **typical price versus yesterday's typical price**, with eligible volume:

| Today's condition | Classified raw-flow contribution |
|---|---|
| Typical Price rises and volume >0 | Positive |
| Typical Price falls and volume >0 | Negative |
| Typical Price unchanged or volume =0 | None |
| Necessary historical data missing | Unavailable |

**Crucial distinction:** MFI may **rise on a negative-flow day**. The current day adds negative raw flow, but a larger negative-flow session may have left the rolling window. Thus “Price down, volume heavy, MFI slightly up” is not a contradiction—and the hover should not automatically call it new buying pressure. See the [SPY rare Neutral walkthrough](#example-a-spy-neutral-with-rare-weak-flow).

A closing-price increase is **not** sufficient to claim positive raw flow: if High/Low/Close **typical price** fell relative to its previous observation, that day belongs to the negative side, even with a higher Close. Flow direction is guarded against the underlying typical-price values.

### MFI Change Trend and One Session Price Relationship

**Question:** *Is the rolling money-flow balance strengthening or weakening today, and does recent price behavior tell the same story?*

| MFI movement | Price movement | Useful reading | Important caution |
|---|---|---|---|
| MFI rises | Price rises | Rolling money-flow balance and latest displayed price move improve together. | Not a guaranteed continuation. |
| MFI falls | Price falls | Price and rolling money-flow balance deteriorate together. | A contrarian Buy can still qualify if oversold. |
| MFI rises | Price falls | One-session **price/MFI mismatch**; pressure may be easing in the rolling window despite weaker displayed price. | Not formal bullish divergence without price pivots. |
| MFI falls | Price rises | One-session mismatch; advance isn't accompanied by improvement in rolling MFI. | Not formal bearish divergence without price pivots. |

MFI daily change is **index points**. Relative percent change is an arithmetic comparison with yesterday's MFI if the prior reading is positive. **Trend** is rising/falling/flat over one session, not a new classifier state. If the prior reading is missing, do not invent the change or direction.

### Missing History and No Event Behavior

| Situation | Correct handling |
|---|---|
| Current MFI not computable | Missing; **not** Neutral/0. |
| Valid MFI but fewer than **252 consecutive valid MFI readings** | Current Signal can qualify; **Standing unavailable**. |
| Fewer than **120 complete volume observations** | 120-session volume rank unavailable; period-average ratio may still be available. |
| Period average volume unavailable/zero | Ratio unavailable; do not manufacture 1.00×. |
| Missing local MFI or price inputs around divergence pivots | No validated divergence event; may reflect **insufficient prerequisites**, not proved absence of every setup. |
| Failure-swing A/B/C is developing but D not complete | No confirmed ▲/▼ today; a partial setup is not a completion event. |
| Missing MFI during failure-swing development | Active sequence resets; no bridging the gap. |
| No symbol or colored number on a valid cell | No such **confirmed event displayed on this date**; ordinary Signal still applies. |
| Historical window begins inside an existing extreme run | Display duration as **at least N** when the earlier onset cannot be verified. |

Do not infer a confirmed reversal, a zero observation, or a fresh zone entry from missing data. All event history is evaluated in **chronological order** so qualifying events appear only when knowable, not painted backward onto earlier dates.

---
## MFI Signal Rules The Five State Model
:small[[Back to top](#summary-mfi-signals) | [Primary Signal Summary](#primary-signal-summary)]

The engine assigns **exactly one** of five mutually exclusive states to a valid initialized MFI(n) reading. This is a **persistent current-value model**: if MFI stays in the same range for seven sessions, the Signal may remain the same for all seven. No threshold crossing, rising/falling requirement, price filter, volume-rank threshold, divergence, or failure swing is required to qualify it.

### Rule Summary for MFI 10 14 and 30

| Signal | Executable expression (replace n with 10, 14 or 30) | Boundary explanation |
|---|---|---|
| **Strong Buy (+2)** | :blue-background[MFI_n <= 15] | 15.00 qualifies Strong Buy. |
| **Buy (+1)** | :blue-background[MFI_n > 15 and MFI_n <= 25] | Above 15; 25.00 still Buy. |
| **Neutral (0)** | :blue-background[MFI_n > 25 and MFI_n < 75] | Both extreme-zone endpoints excluded. |
| **Sell (−1)** | :blue-background[MFI_n >= 75 and MFI_n < 85] | 75.00 qualifies Sell; 85.00 does not. |
| **Strong Sell (−2)** | :blue-background[MFI_n >= 85] | 85.00 qualifies Strong Sell. |

### Strong Buy MFI

**Rule:** :blue-background[MFI_n ≤ 15]. A value of :gray-background[11.74] or exactly :gray-background[15.00] receives **+2**. The window's negative-flow pressure is especially dominant; the project assigns its strongest *contrarian opportunity* state.

**Why not ordinary Buy?** Ordinary Buy begins only **above** 15. **Do not infer recovery:** MFI could be falling sharply, price could still be declining, and volume could be increasing. No upward turn, divergence or confirmation is required. [MSFT's worsening Strong Buy example](#example-b-msft-strong-buy-while-pressure-deepens) illustrates why that matters.

### Buy MFI

**Rule:** :blue-background[15 < MFI_n ≤ 25]. Readings :gray-background[20.63] and :gray-background[25.00] qualify **+1**; exactly 15 remains Strong Buy. This is an oversold contrarian opportunity band, not a claim that the latest money flow was positive.

**What to examine:** Is MFI recovering, getting worse, or completing a separately dated [failure swing](#mfi-failure-swings)? A Buy can coexist with a **bearish** event because level and structural development answer different questions.

### Neutral MFI

**Rule:** :blue-background[25 < MFI_n < 75]. Both endpoints are excluded: :gray-background[25.00] = Buy and :gray-background[75.00] = Sell. A reading of :gray-background[25.56] is **Neutral**, despite implying ~74% negative classified flow.

**Neutral is not necessarily balanced or uneventful.** A confirmed divergence or failure swing can appear on a Neutral cell; a 252-session Standing can be historically exceptional. Missing MFI is also **not** Neutral. See [SPY's rare Neutral example](#example-a-spy-neutral-with-rare-weak-flow).

### Sell MFI

**Rule:** :blue-background[75 ≤ MFI_n < 85]. Exactly :gray-background[75.00] qualifies **−1**, and :gray-background[85.00] belongs to Strong Sell. Positive price-weighted money flow predominates and the project treats this as **contrarian overextension risk**.

**Do not infer immediate weakness:** MFI can continue rising and price can keep advancing after the Sell classification. A new bullish divergence may also appear independently; see the [AAPL example](#example-g-aapl-sell-with-bullish-divergence).

### Strong Sell MFI

**Rule:** :blue-background[MFI_n ≥ 85]. A value :gray-background[86.97] or exactly :gray-background[85.00] receives **−2** because positive flow is exceptionally dominant. Strong Sell is the strongest **contrarian risk** classification; it does not guarantee an imminent price decline or require MFI to fall.

When MFI and price keep rising, the overbought condition can be **intensifying**, not reversing. [TSM example](#example-c-tsm-strong-sell-with-growing-upside-pressure).

### Exact Boundaries Persistence and Missing Values

| Actual MFI(n) | Signal | Why |
|---:|---|---|
| :gray-background[15.00] | Strong Buy | Strong includes the lower threshold. |
| :gray-background[15.01] | Buy | Strictly above 15, still ≤25. |
| :gray-background[25.00] | Buy | Buy includes 25. |
| :gray-background[25.01] | Neutral | Above 25, below 75. |
| :gray-background[74.99] | Neutral | Still below 75. |
| :gray-background[75.00] | Sell | Sell includes 75. |
| :gray-background[84.99] | Sell | Below 85. |
| :gray-background[85.00] | Strong Sell | Strong includes 85. |
| **Unavailable** | **Missing** | No valid five-state score should be manufactured. |

Classification uses the **unrounded** reading. A value slightly above a boundary might *display* the same two-decimal number as the boundary while correctly receiving a different Signal; read the dynamic **Rule** for the precise classification. Likewise, remaining in the same state does not mean nothing changed: daily MFI direction, [zone duration](#extreme-zone-entry-exit-and-duration) and event evidence can change independently.

---

## How to Interpret MFI Patterns and Combinations
:small[[Back to top](#summary-mfi-signals) | [Quick priority table](#priority-summary-what-deserves-attention-first)]

Read **state** (where the MFI value stands), **structure** (what a dated divergence or failure swing completed), then **participation and development** (how money flow, volume and price are changing). A structural event is supplementary evidence, **not** a sixth score or a command to trade.

### Four Categories for Interpreting Combinations
(:small[[Parent](#how-to-interpret-mfi-patterns-and-combinations)])

| Category | How to recognize it | Practical reading |
|---|---|---|
| **Reinforcing** | Buy/Strong Buy with a bullish event; Sell/Strong Sell with bearish event, or two events of the same direction | The event's structural message is compatible with the contrarian interpretation, but does not strengthen the score. |
| **Conflicting** | Buy/Strong Buy with bearish event; Sell/Strong Sell with bullish event; or simultaneous opposite events | Keep both observations visible. The current extreme and newer structure point in different directions. |
| **Early development / Neutral** | Neutral Signal with newly confirmed bullish or bearish event | A structural change can appear before a project extreme qualifies—or after MFI has left it. |
| **Routine or unavailable** | Persistent state, no new event, or missing evidence window | Read level, daily movement, duration, Standing and participation; absence of a symbol need not prove every detector was eligible. |

**“Reinforcing” and “conflicting” describe interpretive compatibility**, not statistical independence, trade certainty or realized future price performance.

### Complete Signal and Event Combination Reference
(:small[[Parent](#how-to-interpret-mfi-patterns-and-combinations)])

| Current Signal | [Confirmed](#confirmed-price-mfi-divergence) ['Divergence'](#mfi-divergence) | [Confirmed 'Failure Swing'](#mfi-failure-swings) | How to interpret together |
|---|---|---|---|
| **Buy / Strong Buy** | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$ | None | Oversold contrarian condition plus lower-price-low/higher-nearby-MFI-low evidence. Potential easing of downside pressure, while Signal stays fixed by today's level. |
| **Buy / Strong Buy** | ${\textcolor{Red}{\textsf{Bearish}}}$ | None | Oversold condition but a higher price high had weaker nearby MFI; evidence is **mixed**, possibly reflecting different dates/regimes. |
| **Buy (not Strong Buy)** | None | $\large{\textcolor{black}{\textsf{▲}}}$ (**Bullish**) | Oversold condition with completed improvement in oscillator structure. A bullish D must exceed 20, so a Strong Buy completion is impossible. |
| **Buy / Strong Buy** | None | $\large{\textcolor{black}{\textsf{▼}}}$ (**Bearish**) | Contrarian oversold condition alongside a failed rebound and completed oscillator breakdown. **Mixed**; see [MSFT](#example-f-msft-buy-with-bearish-failure-swing). |
| **Neutral** | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$ | None | Confirmed less-severe MFI at a lower price low, even though current level is between 25 and 75. |
| **Neutral** | ${\textcolor{Red}{\textsf{Bearish}}}$ | None | Confirmed weaker MFI at a higher price high, despite Neutral level. |
| **Neutral** | None | **Bullish ▲ / Bearish ▼** | Completed four-stage oscillator pattern, not a changed Neutral score. |
| **Sell / Strong Sell** | ${\textcolor{Red}{\textsf{Bearish}}}$ | None | Overbought contrarian risk and bearish nonconfirmation at a higher price high are compatible. |
| **Sell / Strong Sell** | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$ | None | Overbought current level alongside earlier improving downside structure: **mixed**; see [AAPL](#example-g-aapl-sell-with-bullish-divergence). |
| **Sell (not Strong Sell)** | None | $\large{\textcolor{black}{\textsf{▼}}}$ (**Bearish**) | Overbought condition and completed deterioration of oscillator structure. A bearish D is below 80, so Strong Sell completion is impossible. |
| **Sell / Strong Sell** | None | $\large{\textcolor{black}{\textsf{▲}}}$ (**Bullish**) | Overbought condition with a bullish four-stage completion; mixed with contrarian risk. |
| **Any valid compatible state** | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$ | $\large{\textcolor{black}{\textsf{▲}}}$ (**Bullish**), same date | Two separate observations give compatible bullish structural context; neither changes the score. |
| **Any valid compatible state** | ${\textcolor{Red}{\textsf{Bearish}}}$ | $\large{\textcolor{black}{\textsf{▼}}}$ (**Bearish**), same date | Two separate observations give compatible bearish structural context. |
| **Any valid compatible state** | ${\textcolor{DodgerBlue}{\textsf{Bullish}}}$ | $\large{\textcolor{black}{\textsf{▼}}}$ (**Bearish**), same date | Lower-price-low/higher-nearby-MFI-low evidence versus recent oscillator breakdown: genuinely competing information. |
| **Any valid compatible state** | ${\textcolor{Red}{\textsf{Bearish}}}$ | $\large{\textcolor{black}{\textsf{▲}}}$  (**Bullish**), same date | Higher-price-high/lower-nearby-MFI-high evidence versus completed oscillator improvement: competing information. |
| **Any valid state** | None | None | No confirmed new structural event shown today; interpret current pressure, historical standing and volume instead. |

**Important mathematical restrictions:**
- A confirmed **bullish** failure swing completes with D **above B**, where B is **above 20**, so it **cannot** occur on a **Strong Buy (MFI ≤15)** completion cell.
- Similarly, a confirmed **bearish** failure swing completes **below B**, where B is **below 80**, so it **cannot** occur on a **Strong Sell (MFI ≥85)** completion cell.

These are consequences of the [current A/B/C/D definition](#the-four-stages-abcd), not additional rulebook filters. Other combinations still depend on actual history and must not be invented as observed events.

### Event Agreement and Opposition
(:small[[Parent](#how-to-interpret-mfi-patterns-and-combinations)])

| Visual appearance | First reading | Follow-up question |
|---|---|---|
| ${\textcolor{DodgerBlue}{\textsf{Blue number}}}$ + $\large{\textcolor{black}{\textsf{▲}}}$ | '[Bullish Divergence](#bullish-divergence-worked-spy-example)' **and** '[Bullish Failure Swing](#bullish-failure-swing)' were confirmed on the same date. | Did improving MFI structure also coincide with meaningful participation? |
| ${\textcolor{Red}{\textsf{Red number}}}$ + $\large{\textcolor{black}{\textsf{▼}}}$ | '[Bearish Divergence](#confirmed-price-mfi-divergence)' **and** '[Bearish Failure Swing](#bearish-failure-swing)' were confirmed. | Is the current price/flow condition also weakening? |
| ${\textcolor{DodgerBlue}{\textsf{Blue number}}}$ + $\large{\textcolor{black}{\textsf{▼}}}$ | Bullish swing-level nonconfirmation **but** Bearish oscillator completion. | Which evidence concerns earlier price pivots, and which concerns the latest oscillator sequence? |
| ${\textcolor{Red}{\textsf{Red number}}}$ +$\large{\textcolor{black}{\textsf{▲}}}$ | Bearish pivot evidence **but** Bullish oscillator completion. | Are the event timeframes giving different signals? |

The text-color channel and arrow channel are independent. Both are dated to **their own** confirmation. A shared day does **not** imply their underlying pivots and A/B/C/D stages occurred on that same day.

### State and Context Combinations
(:small[[Parent](#how-to-interpret-mfi-patterns-and-combinations)])

| Condition + context | Information value | What not to infer |
|---|---|---|
| [Strong Buy](#strong-buy-mfi) + falling MFI + heavy **negative** raw flow | Severe oversold condition may be **deepening** rather than improving. | A bullish turn has begun. |
| [Strong Sell](#strong-sell-mfi) + rising MFI + heavy **positive** raw flow | Overbought pressure may be **intensifying**. | The price advance must end now. |
| [Neutral](#neutral-mfi) + 0.6th-percentile Standing | Historically unusual negative-flow balance despite no fixed project extreme. | The 252-session rank overrides the Neutral score. |
| Newly entered Oversold + a confirmed [bearish ▼](#bearish-failure-swing) | Oversold classification and bearish oscillator structure can arrive together. | The 'Buy' classification is an error. |
| Failure Swing + exceptionally **light** Volume | Confirmed oscillator geometry with unusually low event-day participation. | The swing is mathematically disqualified. |
| Failure Swing + exceptionally **heavy** Volume | Confirmed structure with unusually high participation that day. | The event proves stock-price reversal. |
| No fresh symbol + 4 sessions Oversold | Persistent condition can still be meaningful without a new event. | No information is available beyond the cell color. |

### A Useful Order of Interpretation
(:small[[Parent](#how-to-interpret-mfi-patterns-and-combinations)])

1. Establish the **Signal and Rule**,
2. read any **fresh dated events** and their actual values/dates,
3. assess whether their directions **agree or conflict**,
4. then add **Historical Standing**, **Volume Activity** and **zone duration**.
5. Finish with Context Interpretation and Bottom-line.

> **Do not treat an exceptionally low volume percentile as automatically bearish, or a high volume percentile as automatically bullish; raw-flow sign follows typical-price movement.**

---

## Practical MFI Reading Workflow and Worked Examples
:small[[Back to top](#summary-mfi-signals) | [Quick six-step workflow](#six-step-mfi-reading-workflow)]

The following observations illustrate how to move from *what the cell says* to *why it matters*. Historical examples are based on the accepted 2026 MFI evidence and screenshots; values are shown at the precision displayed in the app. **Descriptions are interpretations of the observations, not forecasts or measured hit rates.**

### Example A: SPY Neutral With Rare Weak Flow
(:small[[Parent](#practical-mfi-reading-workflow-and-worked-examples)])

**SPY · 11/19/26 · MFI(14) = 25.56 · Neutral.**

| Evidence | Observation |
|---|---|
| **Rule** | 25 <25.56<75: correctly **Neutral (0)**. |
| **Historical Standing** | **0.6th percentile**, with **250/252** MFI readings higher. |
| **Volume Activity** | **1.33×** its 14-session average; **94th percentile** of 120 sessions. |
| **Flow balance** | ~**74% negative** flow in 14-session balance. Today's typical-price flow was negative. |
| **Latest movement** | MFI edged up only ~0.1 point, despite a substantial down-price session and heavy participation. |

**Context Interpretation:** Negative flow ~74% of 14D balance. Heavy volume added negative flow, yet rolling MFI edged up 0.1 pt.

**Bottom-line:** Neutral by threshold, but flow near 252-session low; downside pressure elevated.

**What this teaches:** A fixed-threshold Neutral is not necessarily an ordinary or unimportant observation. A 252-session Standing near the bottom supplies **historical rarity**; today's raw-flow sign and volume tell a **different, current-session story**. Neither one changes the Signal.

### Example B: MSFT 'Strong Buy' While Pressure Deepens
(:small[[Parent](#practical-mfi-reading-workflow-and-worked-examples)])

**MSFT · 11/2/26 · MFI(14) = 11.74 · Strong Buy (+2)**, at approximately the **0.6th percentile** of 252 MFI readings. MFI fell by ~8.0 points and price declined ~2.8%.

**Rule:** At/below 15 qualifies Strong Buy regardless of whether MFI is currently recovering.

**Context Interpretation:** Negative flow accounts for ~88% of 14-session activity; the latest price/volume behavior and falling MFI show pressure remained severe.

**Bottom-line:** Severe oversold flow, but selling pressure is still deepening.

**What this teaches:** **Contrarian opportunity** and **upward recovery** are not synonymous. A stronger positive *score* can accompany a more severe **negative-flow state**.

### Example C: TSM 'Strong Sell' With Growing Upside Pressure
(:small[[Parent](#practical-mfi-reading-workflow-and-worked-examples)])

**TSM · 10/5/26 · MFI(14) = 86.97 · Strong Sell (−2)**, approximately the **99.8th percentile** of its 252 MFI readings. MFI rose ~6.8 points while price advanced ~2.8%.

**Rule:** At/above 85 qualifies Strong Sell; MFI need not have begun declining.

**Context Interpretation:** Positive flow dominates the window (~87%). Continued price/MFI gains mean the extreme **intensified** rather than faded.

**Bottom-line:** Severe overbought flow; buying pressure still intensifying.

**What this teaches:** Overbought risk is a **condition**. It does not, by itself, establish that sellers have taken control.

### Example D: SPY 'Neutral' With 'Bullish Divergence'
(:small[[Parent](#practical-mfi-reading-workflow-and-worked-examples) | Related: [Example: 'Bullish Divergence' (SPY)](#bullish-divergence-worked-spy-example)])

**SPY · 11/9/26 · MFI(14) = 40.64 · Neutral, blue numeric value.**

| Field | Exact displayed comparison |
|---|---|
| **Price lows** | 10/30 ($750.36) → 11/5 ($732.71), **−2.4%** |
| **Nearby MFI lows** | 10/30 (33.30) → 11/6 (39.43), **+6.13 / +18.4%** |
| **Confirmed event date** | **11/9**, after two right-hand price-pivot sessions. |

**Context Interpretation:** Price lower low, nearby MFI higher low: selling pressure eased at new low.

**Bottom-line:** [Bullish divergence](#confirmed-price-mfi-divergence) suggests easing downside pressure despite Neutral Signal.

**What this teaches:** The later lower price low occurred alongside a **higher nearby MFI low**; that new structural information is invisible in the Neutral background alone. The different price/MFI dates and 11/9 confirmation are essential. [Reconstruct the event](#bullish-divergence-worked-spy-example).

### Example E: NVDA Bullish 'Failure Swing'
(:small[[Parent](#practical-mfi-reading-workflow-and-worked-examples)])

**NVDA · 11/23/26 · MFI(14) ~29.82 · Neutral, black ▲.** The event completed the full **A/B/C/D** sequence, not a stock-price breakout:

| Stage | Date | Displayed MFI | Meaning |
|---|---|---:|---|
| A | 11/10 | 19.29 | Oversold low (≤20). |
| B | 11/11 | 29.77 | Rebound high to exceed. |
| C | 11/20 | 20.60 | Higher retest low above A and above 20. |
| D | 11/23 | 29.82 | **Strict move above B**, confirming ▲. |

**Breakout:** +0.06 pt above prior MFI rebound high (29.77, 11/11), from **unrounded** event readings. The 11/23 hover also reported exceptionally heavy volume (100th percentile of 120 sessions).

**Context Interpretation:** Exited Oversold today. Bullish failure swing: MFI recovered, held a higher low & broke prior rebound high. Exceptionally heavy volume on event day.

**Bottom-line:** Bullish failure swing suggests improving MFI structure despite Neutral Signal.

**What this teaches:** The **20/80 oscillator event** can qualify while the **25/75 five-state score is Neutral**. An ▲ signifies completed MFI structure, not a confirmed price reversal. [Complete mechanics](#bullish-failure-swing-worked-nvda-example).

### Example F: MSFT Buy With Bearish 'Failure Swing'
(:small[[Parent](#practical-mfi-reading-workflow-and-worked-examples) | Related: [Ex: 'Bearish Failure Swing'](#bearish-failure-swing-example)])

**MSFT · 10/23/26 · MFI(10) = 22.00 · Buy (+1), black ▼.** MFI entered the oversold zone and completed a bearish failure swing as its recovery failed and it broke below its earlier recovery trough. **Volume Activity** was ~**0.70×** its 10D average, at the exceptionally light **2nd percentile** of 120 sessions.

**Context Interpretation:** Entered Oversold today. Bearish failure swing: rebound failed; MFI broke its prior recovery trough. Exceptionally light volume (2nd pct) on event day.

**Bottom-line:** Buy reflects oversold flow, but bearish failure swing indicates worsening MFI structure; evidence mixed.

**What this teaches:** “Buy” describes **how low MFI is**, whereas ▼ describes **how the latest oscillator sequence completed**. Both can be true. The very low event-day volume qualifies participation, but does not invalidate the pattern.

### Example G: AAPL Sell With 'Bullish Divergence'
(:small[[Parent](#practical-mfi-reading-workflow-and-worked-examples)])

**AAPL · 10/5/26 · MFI(14) = 76.15 · Sell (−1), blue numeric value.**

Price pivot lows moved from **$334.30 (9/24) to $325.81 (10/1)**, a fall of ~2.5%. Nearby MFI lows moved **63.98 (9/24) → 70.27 (10/2)**, up ~6.29 points / ~9.8%. Divergence was confirmed **10/5**, the same session MFI entered the overbought Sell zone.

**Context Interpretation:** Entered Overbought today. Price lower low, nearby MFI higher low: selling pressure eased at new low.

**Bottom-line:** Sell reflects overbought flow, but bullish divergence indicates easing downside pressure; evidence mixed.

**What this teaches:** The Sell classification identifies **today's elevated MFI level**. The blue value reports an **earlier pivot comparison**. Their interpretive implications can conflict without either result being an error. Future price moves do not retroactively change the event or score.

### Example H: NVDA 'Zone Entry' and 'Persistence'
(:small[[Parent](#practical-mfi-reading-workflow-and-worked-examples)])

**NVDA · November 2026 · MFI(14).**
- On **11/17**, MFI was **23.73**, with **“Entered Oversold today.”**
- By **11/20**, MFI was around **20.6**, with **“Oversold 4 sessions.”**
- Both belonged to the project's Buy band.

**Why this matters:** The same green Buy state is not the same market story on both dates. The first identifies a **new threshold entry**; the latter identifies **persistent negative-flow pressure**, with exceptionally heavy volume contributing to the recent deterioration. The chronology helps distinguish an emerging condition from a sustained one.

### Worked Example Summary What Each Adds
(:small[[Parent](#practical-mfi-reading-workflow-and-worked-examples)])

| Observation | Unique information you should retain |
|---|---|
| SPY 11/19 | Historical rarity can be meaningful when the score is Neutral. |
| MSFT 11/2 | Strong oversold condition may continue deteriorating. |
| TSM 10/5 | Strong overbought condition may continue intensifying. |
| SPY 11/9 | Divergence compares price pivots **and nearby MFI extremes**, with separate dates. |
| NVDA 11/23 | A/B/C/D is an **oscillator event**, not a stock-price breakout. |
| MSFT 10/23 | A Buy score and bearish structural event can coexist; participation can qualify the reading. |
| AAPL 10/5 | Current elevated MFI and earlier bullish pivot evidence are distinct. |
| NVDA 11/17–20 | Zone **entry** versus **persistence** offers useful context even with identical Signal. |

---

## MFI(10), MFI(14) and MFI(30)
:small[[Back to top](#summary-mfi-signals) | [Same five-state rules](#rule-summary-for-mfi-10-14-and-30)]

All periods use **the same formula, score thresholds, five-state Rule, divergence logic, failure-swing 20/80 model, 252-session Standing methodology and 120-session volume-rank method**. Each is calculated from its **own** MFI(n) history, so values, event dates and relative-volume averages can differ.

### Period Comparison and Practical Selection

| Setting | Typical behavior | Useful lens | Trade-off |
|---|---|---|---|
| **MFI(10)** | Most responsive of the three | Recent money-flow changes and earlier extremes | More sensitive to short-lived participation swings. |
| **MFI(14)** | Intermediate/standard reference | Balanced reference for most examples in this guide | Still changes with short-term flow shocks. |
| **MFI(30)** | Longer, smoother pressure balance | Persistence and broader money-flow backdrop | New changes may be muted or appear later. |

A ticker might show MFI(10) = 22 (Buy) and MFI(30) = 48 (Neutral). This is **not a computational contradiction**: the latest 10-session flow is unusually negative while the 30-session balance is closer to the middle. Likewise, an MFI(10) divergence date need not match MFI(14)'s because their nearby MFI extrema and eligible evidence differ.

### Periods Are Not Three Independent Votes

Treat the variants as **time-horizon views on overlapping underlying price/volume data**, not separate buy/sell confirmations. Relative volume uses the corresponding 10D/14D/30D average (including today); all variants share the same **120-session volume-rank history** for that ticker/date when eligible. Historical MFI Standing always ranks **252 values of the selected MFI period**, not one common composite MFI.

---

## Value Added Use Complementary Indicators and Safeguards
:small[[Back to top](#summary-mfi-signals)]

### Useful Complementary Indicators
(:small[[Parent](#value-added-use-complementary-indicators-and-safeguards) | See Also: [Comparing MFI, RSI, CMF](#comparing-mfi-rsi-and-cmf)])

MFI answers a specific question about **classified volume-weighted pressure**. Complementary indicators are valuable when they answer **different** questions, rather than simply agreeing with MFI because they use overlapping inputs.

| Tool to cross-check | What it adds that MFI alone does not | Example of useful investigation |
|---|---|---|
| **SMA(200)** / price trend | Broad price-trend direction and location relative to a long average | Is a Strong Buy oversold condition developing within an established downtrend or a broader uptrend pullback? |
| **OBV** | Cumulative, volume-weighted direction of close-to-close changes | Does broader volume accumulation/distribution agree with MFI's current pressure balance? |
| **RSI** | Price-only momentum/overbought-oversold comparison | Is MFI weakness mainly a volume-weighted phenomenon or visible in price momentum too? |
| **Bollinger Bands** | Price position/stretch relative to recent volatility bands | Is the security also unusually extended in price, not just money flow? |
| **CMF** | Different volume-based accumulation/distribution method | Does closing location within price ranges corroborate or complicate MFI's typical-price sign model? |
| **ADX** | Directional trend strength with DI leadership | Is the oversold/overbought condition occurring during a strong directional trend? |
| **Support/resistance and price structure** | Actual market-price levels and swing behavior | Does price react at a relevant level after an MFI event? |

A compact hover **Notes** line suggests **SMA(200), OBV, RSI and Bollinger Bands**. The extended table above explains what each contributes; it does not create new Signal requirements.

---
Cross-check the regime with ADX or a longer moving-average slope: MFI extremes can persist during strong trends. Any claimed hit-rate advantage for range-bound conditions requires separate evidence; this project has not established one.

---
| Indicator | Primary question | Why it is not interchangeable with MFI |
|---|---|---|
| **MFI** | How is the rolling **price-and-volume** balance distributed between positive and negative typical-price sessions? | Bounded, volume-weighted contrarian oscillator. |
| **RSI** | How does the magnitude of recent price gains compare with losses? | Price momentum without MFI's volume weighting. |
| **CMF** | Where has price closed within its range, weighted by volume, over the window? | Different accumulation/distribution proxy; not the same TP-change sign assignment. |

---
### Project Thresholds Versus Conventional MFI

| Topic | Conventional interpretation | This application |
|---|---|---|
| **Main overbought/oversold reference** | Often around **20 / 80** | Five-state classifier uses **15 / 25 / 75 / 85**. |
| **[Failure swings](#mfi-failure-swings)** | Often described using a **20 / 80** extreme and A/B/C/D sequence | Implements that separate **20/80 pattern**; ▲/▼ only at D completion. |
| **[Divergence](#confirmed-price-mfi-divergence)** | Price makes a new extreme not confirmed by the indicator | Uses **strict five-observation price pivots**, nearby 5-observation MFI extrema and **two-session** price-pivot confirmation. |
| **[Volume participation](#volume-activity-and-unusual-participation)** | Context-sensitive, no universal percentile cutoff | Adds 120-session volume percentile; highlights **≤2.5 / ≥97.5** tails in Context. |
| **[Historical rarity](#historical-mfi-standing-252-sessions)** | Ranking can help put an oscillator reading in context | Uses **252 consecutive valid MFI(n) readings** and **midrank**. |
| **[Scoring](#mfi-signal-rules-the-five-state-model)** | No universal MFI five-state +2/+1/0/−1/−2 method | Project-specific **contrarian** classification, independent of events. |

### Sources Windows and Data Freshness

- **Raw MFI:** High/Low/Close typical price and Volume; first eligible calculation needs n valid classified flow observations plus prior typical-price history. Missing values interrupt readiness.
- **Price in the hover:** Canonical Adjusted Close when available, else Close; it is separate from the typical price used to classify raw MFI flow.
- **Price pivots for divergence:** Actual High/Low price extremes, not necessarily the displayed adjusted close. The entire comparison must remain chronologically available.
- **Historical Standing:** Requires 252 **consecutive** finite readings of the **selected** MFI(n), including today.
- **Volume percentile:** Requires 120 **consecutive** valid volume observations. The n-session average has its own readiness check and includes today's volume.
- **Live versus cached history:** Independently cached heatmaps may temporarily show different versions of the same day's volume if the source was revised. A fresh recalculation can reconcile them; this is a **data freshness issue**, not a different MFI formula.

### What MFI Can and Cannot Establish

| MFI evidence can establish… | It cannot alone establish… |
|---|---|
| Which fixed project money-flow band today's MFI belongs to | A guaranteed next-day direction, trading recommendation or valuation |
| A weighted balance of positive/negative classified typical-price activity | Actual dollars entering/leaving the market or trader identity |
| That pressure is rising/falling in the rolling window | That today's Close and today's classified raw flow moved the same way |
| A completed divergence pivot comparison | An accomplished price reversal or eventual profitable trade |
| A completed oscillator failure swing | A stock-price breakout, confirmed price trend or minimum future return |
| A rare 252-session oscillator rank | That rarity must shortly revert toward the mean |
| Exceptional relative volume | That exceptional participation is bullish or bearish without flow/price evidence |

**Final reading principle:** Read the five-state **Rule** first, then inspect new dated events, understand the **flow and volume context**, and use **Context Interpretation + Bottom-line** to reconcile those observations. **A five-state rule is not finished if a human cannot reconstruct why an observation landed in each state.** The same expectation applies to each event: a user must be able to reconstruct what qualified, using the displayed values, dates and source rules.

---
## MFI: My Notes
(:small[[Back to top](#summary-mfi-signals)])

> The volume-based equivalent to RSI. 
>  - Often used for **overbought/oversold analysis** 
>
> MFI is often used like an RSI but with volume, and traders look for divergence.    
> - MFI is RSI's volume-weighted cousin (uses typical price × volume flow instead of pure price change), so it tends to spike/exhaust faster on climactic volume — which matters for how you set your bands.

> Cross-check ADX or a longer moving-average slope to distinguish range-bound conditions from strong trends, where MFI extremes can persist. Any difference in mean-reversion hit rates remains unverified here.

---
**Purpose:** Combine price and volume data to create a volume-weighted momentum oscillator that identifies overbought/oversold conditions. 

**Use when**:  You want **overbought/oversold signals** but with volume confirmation, especially in ranging markets.
The "volume-based" equivalent to RSI:
- "*While volume-based, MFI behaves like RSI and is often used for **overbought/oversold analysis** similar to momentum indicators.*"

**Key Concept:** Often called "volume-weighted RSI". Uses both price change and volume to measure buying/selling pressure, making it more comprehensive than price-only oscillators.

**Calculation:** Uses typical price :blue-background[[(high + low + close) ÷ 3]] multiplied by volume to create money flow, then applies RSI-style calculation over 14 periods.

**Signals & Interpretation:**
- Above 80 = overbought (potential selling opportunity)
- Below 20 = oversold (potential buying opportunity)
- Divergences between MFI and price signal potential reversals
- Rising MFI = increasing buying pressure

$\large{\rightarrow}$ Divergence between the MFI and price can indicate a potential trend reversal
- **Optimal Conditions:** Works best in ranging or mildly trending markets. Most effective on daily and weekly timeframes for swing trading setups.
- **Limitations:** Can remain overbought/oversold for extended periods in strong trends. May produce false signals in low-volume conditions.

---
### Difference Btwn: Chaikin's Money Flow & MFI
(:small[[Parent](#mfi-my-notes) | Related: [Useful Complementary Indicators](#useful-complementary-indicators)])

The main difference is that the MFI is a momentum oscillator that uses price and volume to identify overbought/oversold conditions, ranging from 0-100, while CMF measures the strength of buying and selling pressure over a **longer period**, using a multiplier based on the price's closing position within its high-low range, resulting in a range between -1 and +1.

MFI gives a more direct overbought/oversold signal, whereas CMF is more focused on the overall trend strength and direction of money flow.

---

## Table of Contents MFI
:small[[Back to top](#summary-mfi-signals)]

### Quick Reference

- [Summary MFI Signals](#summary-mfi-signals)
  - [Primary Signal Summary](#primary-signal-summary)
  - [Summary Important MFI Patterns](#summary-important-mfi-patterns)
  - [What the Cell Annotations Mean](#what-the-cell-annotations-mean)
  - [Secondary Evidence at a Glance](#secondary-evidence-at-a-glance)
  - [Six Step MFI Reading Workflow](#six-step-mfi-reading-workflow)
  - [Guide Map](#guide-map)
- [The MFI Patterns You Should Recognize Immediately](#the-mfi-patterns-you-should-recognize-immediately)
  - [Priority Summary What Deserves Attention First](#priority-summary-what-deserves-attention-first)
  - [At a Glance Combinations](#at-a-glance-combinations)
- [How to Read an MFI Heatmap Cell](#how-to-read-an-mfi-heatmap-cell)
- [Understanding the MFI Hover](#understanding-the-mfi-hover)
  - [Hover Field Map](#hover-field-map)
  - [Daily Change Units and Trend](#daily-change-units-and-trend)
  - [Reading Rule Context Interpretation and Bottom-line Together](#reading-rule-context-interpretation-and-bottom-line-together)

### Indicator and Signal Mechanics

- [MFI Brief Overview and Calculation](#mfi-brief-overview-and-calculation)
  - [Calculation With Real Units](#calculation-with-real-units)
  - [Two Concrete Calculations](#two-concrete-calculations)
  - [Comparing MFI RSI and CMF](#comparing-mfi-rsi-and-cmf)
- [Understanding MFI Secondary Metrics and Events](#understanding-mfi-secondary-metrics-and-events)
  - [Understanding 'Divergence', 'Failure Swings' and 'Overbought/Oversold Levels'](#understanding-divergence-failure-swings-and-overboughtoversold-levels)
  - [MFI 'Divergence'](#mfi-divergence)
    - [Confirmed Price MFI Divergence](#confirmed-price-mfi-divergence)
      - [Pivot Dates and Confirmation Terms](#pivot-dates-and-confirmation-terms)
      - [Bullish Divergence Worked SPY Example](#bullish-divergence-worked-spy-example)
  - [MFI 'Failure Swings'](#mfi-failure-swings)
    - [Bullish Failure Swing](#bullish-failure-swing)
    - [Bearish Failure Swing](#bearish-failure-swing)
    - [Key Characteristics and Usage](#failure-swing-key-characteristics-usage)
    - [The Four Stages A/B/C/D](#the-four-stages-abcd)
    - [Bullish Failure Swing Worked NVDA Example](#bullish-failure-swing-worked-nvda-example)
  - [Historical MFI Standing 252 Sessions](#historical-mfi-standing-252-sessions)
  - [Volume Activity and Unusual Participation](#volume-activity-and-unusual-participation)
  - [Extreme Zone Entry Exit and Duration](#extreme-zone-entry-exit-and-duration)
  - [Positive and Negative Money Flow Balance](#positive-and-negative-money-flow-balance)
  - [MFI Change Trend and One Session Price Relationship](#mfi-change-trend-and-one-session-price-relationship)
  - [Missing History and No Event Behavior](#missing-history-and-no-event-behavior)

- [MFI Signal Rules The Five State Model](#mfi-signal-rules-the-five-state-model)
  - [Strong Buy](#strong-buy-mfi) · [Buy](#buy-mfi) · [Neutral](#neutral-mfi) · [Sell](#sell-mfi) · [Strong Sell](#strong-sell-mfi)
  - [Exact Boundaries Persistence and Missing Values](#exact-boundaries-persistence-and-missing-values)
### Interpretation and Reference

- [How to Interpret MFI Patterns and Combinations](#how-to-interpret-mfi-patterns-and-combinations)
  - [Four Categories for Interpreting Combinations](#four-categories-for-interpreting-combinations)
  - [Complete Signal and Event Combination Reference](#complete-signal-and-event-combination-reference)
  - [Event Agreement and Opposition](#event-agreement-and-opposition)
- [Practical MFI Reading Workflow and Worked Examples](#practical-mfi-reading-workflow-and-worked-examples)
  - [SPY Rare Neutral](#example-a-spy-neutral-with-rare-weak-flow)
  - [MSFT Strong Buy With Deepening Pressure](#example-b-msft-strong-buy-while-pressure-deepens)
  - [TSM Strong Sell With Intensifying Pressure](#example-c-tsm-strong-sell-with-growing-upside-pressure)
  - [SPY Bullish Divergence](#example-d-spy-neutral-with-bullish-divergence)
  - [NVDA Bullish Failure Swing](#example-e-nvda-bullish-failure-swing)
  - [MSFT Bearish Swing Conflict](#example-f-msft-buy-with-bearish-failure-swing)
  - [AAPL Bullish Divergence Conflict](#example-g-aapl-sell-with-bullish-divergence)
  - [NVDA Zone Entry and Persistence](#example-h-nvda-zone-entry-and-persistence)
- [MFI 10 MFI 14 and MFI 30](#mfi10-mfi14-and-mfi30)
- [Value Added Use Complementary Indicators and Safeguards](#value-added-use-complementary-indicators-and-safeguards)
  - [Useful Complementary Indicators](#useful-complementary-indicators)
  - [Project Thresholds Versus Conventional MFI](#project-thresholds-versus-conventional-mfi)
  - [Sources Windows and Data Freshness](#sources-windows-and-data-freshness)
  - [What MFI Can and Cannot Establish](#what-mfi-can-and-cannot-establish)
