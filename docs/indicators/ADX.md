## ADX Signal Summary
:small[[ToC](#index-adx)]

> "Identifying a trend’s strength"

|Bucket|What it answers|Indicators|
|---|---|---|
|**Trend strength**|Is the trend strong enough to trust?|ADX|
|**Momentum / oscillators**|Overbought/oversold, turning points|RSI, Stochastic, MACD, ROC, **Williams %R**, CCI, UO, DPO|
|**Trend direction**|Which way, and is there even a trend?|SMA, EMA, HMA|
|**Volatility**|How big are the swings, right now?|Bollinger Bands, ATR|
|**Volume / money flow**|Is real participation behind the move?|CMF, MFI, VWMA|
|**Sentiment / power balance**|Who's winning, bulls or bears?|Bull Bear Power|

---
> **Start here:** ADX tells you how strong the directional trend is. +DI and −DI tell you which side is in control. The heatmap Signal combines both. The number's font color and the symbols add **separate observations**; they never change the Signal.

This guide uses **ADX(14)** for its examples. The same five-state thresholds and display rules apply to ADX(9) and ADX(20); the periods respond at different speeds. [How to read the cell](#how-to-read-an-adx-heatmap-cell) · [Most important combinations](#key-combinations-what-deserves-attention) · [Secondary hover metrics](#secondary-hover-metrics) · [Complete rules](#adx-rule-translation).

### At a glance: what each part of the heatmap means

| What you see | What it tells you | Important distinction |
| --- | --- | --- |
| **Signal/background:** Strong Buy, Buy, Neutral, Sell, Strong Sell | Whether **ADX strength and DI control jointly qualify** under the rulebook | A crossover or divergence never changes the Signal. |
| **ADX number** (for example, 28.10) | Strength of the trend, **not** bullish or bearish direction | Its day-to-day rise/fall appears under Trend and Δ vs prior day. |
| [:blue-background[Blue ADX number]](#spread-color-blue-or-red-adx-value) | The same DI leader has been **gaining control** over two consecutive moves | Blue number is **not** automatically bullish: bears can be gaining control. |
| [**Red ADX number**](#spread-color-blue-or-red-adx-value) | The same DI leader has been **losing some control** over two consecutive moves | Red number is **not** automatically bearish: bulls can be losing control. |
| [**Black ▲ / ▼**](#di-crossover-black-arrows) | A new DI leader appeared **on this session**: ▲ buyers, ▼ sellers | A new leader may still leave Signal Neutral. |
| [**Blue ◆ / red ◆**](#price-adx-divergence) | Confirmed price/ADX nonconfirmation: **blue = bullish divergence** after a lower price low; **red = bearish divergence** after a higher price high | Diamond means a **swing-level warning**, not a reversal or an automatic score change. |
| Ordinary black number, no symbol | No qualifying *new* display customization in that cell | Does **not** mean the existing Buy/Sell trend has ended. |

### HTR: five-state Signals

| Signal | Literal trigger | Layman's translation | Read more |
| --- | --- | --- | --- |
| **Strong Buy** | :gray-background[ADX > 25] and :gray-background[+DI at least 10 points above −DI] | Bulls are firmly in control, and the trend is strong. | [Strong Buy](#strong-buy) |
| **Buy** | :gray-background[ADX > 20] and :gray-background[+DI at least 5 points above −DI], **but Strong Buy is not met** | Bulls are in control, with meaningful trend strength. | [Buy](#buy) |
| **Neutral** | :gray-background[ADX ≤ 20] **or** :gray-background[absolute DI gap < 5 points] | The trend is too weak **or** neither side leads by enough to qualify. | [Neutral](#neutral) |
| **Sell** | :gray-background[ADX > 20] and :gray-background[−DI at least 5 points above +DI], **but Strong Sell is not met** | Bears are in control, with meaningful trend strength. | [Sell](#sell) |
| **Strong Sell** | :gray-background[ADX > 25] and :gray-background[−DI at least 10 points above +DI] | Bears are firmly in control, and the trend is strong. | [Strong Sell](#strong-sell) |

**Boundary rules:** ADX exactly 20 is Neutral. ADX exactly 25 does not meet the Strong threshold. A DI gap of exactly 5 qualifies for an ordinary directional Signal when ADX is above 20; a gap of exactly 10 qualifies for Strong when ADX is above 25. **Missing/warmup data is not Neutral.** These thresholds describe the application's custom rulebook, not a universal ADX trading strategy.

---

### Key Combinations: What Deserves Attention

**How to prioritize:** Start with the Signal. Next, see whether ADX is rising or falling. Then interpret the number's font color, crossover arrow, and divergence diamond. A single observation can strengthen a trend reading **or** challenge it. The tiers below rank **interpretive importance**, not historical hit rate, expected returns, or trading instructions.

#### Tier 1 — Strongest aligned or cautionary combinations

| Pattern you see | Plain-English meaning | What to examine next |
| --- | --- | --- |
| **Strong Buy + [rising ADX](#rising-vs-falling-adx) + ${\textcolor{DodgerBlue}{\textsf{blue value}}}$** | **Bulls are firmly in control and gaining more control.** Both the smoothed trend-strength reading and recent DI separation are improving. | Is price also making progress higher? See [Spread Color](#spread-color-blue-or-red-adx-value). |
| **Strong Sell + rising ADX + ${\textcolor{DodgerBlue}{\textsf{widening}}}$** | **Bears are firmly in control and gaining more control.** Blue describes widening separation, **not** an upward price forecast. | Is price continuing lower? See [Spread Color](#spread-color-blue-or-red-adx-value). |
| **Buy/Strong Buy + [falling ADX](#rising-vs-falling-adx) + ${\textcolor{red}{\textsf{red value}}}$** | **Bulls still control direction, but their control is weakening.** Both ADX and DI separation have eased. The existing Buy Signal may persist. | Watch whether price support holds and DI lines keep converging. |
| **Sell/Strong Sell + falling ADX + ${\textcolor{red}{\textsf{narrowing}}}$** | **Bears still control direction, but their control is weakening.** This is a caution about trend strength, not proof of a bullish reversal. | Watch whether selling pressure continues easing and price stabilizes. |
| **Buy/Strong Buy + $\large{\textcolor{red}{\textsf{◆}}}$** | Price made a **higher swing high**, but nearby ADX trend strength was lower. **Bulls may be tiring**, even though today's classification remains bullish. | Read the pivot dates, ADX peaks, and current DI leader in [Price/ADX Divergence](#price-adx-divergence). |
| **Sell/Strong Sell + $\large{\textcolor{blue}{\textsf{◆}}}$** | Price made a **lower swing low**, but nearby ADX strength was lower. **Bears may be tiring**, even though today's classification remains bearish. | Read the pivot dates, ADX peaks, and current DI leader in [Price/ADX Divergence](#price-adx-divergence). |

#### Tier 2 — Early changes and conflicting evidence

| Pattern you see | Plain-English meaning | What to examine next |
| --- | --- | --- |
| **Buy/Strong Buy + $\large{\textcolor{black}{\textsf{▲}}}$** | Buyers **just took DI leadership**, and today’s strength/gap also qualifies the bullish Signal. A fresh event and a qualified condition reinforce each other. | Check whether ADX keeps rising and price holds the shift. |
| **Sell/Strong Sell + $\large{\textcolor{black}{\textsf{▼}}}$** | Sellers **just took DI leadership**, and today’s strength/gap also qualifies the bearish Signal. | Check whether ADX keeps rising and price confirms the decline. |
| **Neutral + $\large{\textcolor{black}{\textsf{▲}}}$** | Buyers have **just overtaken sellers**, but ADX strength or the DI gap is not sufficient for a Buy Signal. | Is ADX rising? Does the positive DI gap persist or widen? See [DI Crossover](#di-crossover-black-arrows). |
| **Neutral + $\large{\textcolor{black}{\textsf{▼}}}$** | Sellers have **just overtaken buyers**, but ADX strength or the DI gap is not sufficient for a Sell Signal. | Is ADX rising? Does the negative DI gap persist or widen? |
| **Neutral + $\large{\textcolor{blue}{\textsf{◆}}}$ or $\large{\textcolor{red}{\textsf{◆}}}$** | A confirmed price-swing nonconfirmation exists, **even though today’s ADX/DI state is Neutral**. The diamond is historical structure, not a qualified trend Signal. | Check whether ADX was already below 20 at the pivots and which DI now leads. |
| **Rising ADX + ${\textcolor{red}{\textsf{red value}}}$** | The smoothed trend-strength measure is rising, **but the current DI leader is losing ground**. These measures are not confirming each other. | Check which DI leads and whether the discrepancy persists. |
| **Falling ADX + ${\textcolor{DodgerBlue}{\textsf{blue value}}}$** | The current DI leader is gaining ground, **but smoothed trend strength is easing**. Do not call this confirmed acceleration. | Check actual DI values and subsequent ADX development. |
| **$\large{\textcolor{red}{\textsf{◆}}}$ with −DI now leading**, or **$\large{\textcolor{blue}{\textsf{◆}}}$ with +DI now leading** | The price/ADX divergence remains a valid swing observation, but **current DI leadership has changed or conflicts with the original price-swing direction**. | Give the current leadership and the older swing event separate weight; read the hover's DI context. |
| **Diamond ◆ + colored number or black arrow** | Multiple observations coexist on the same date: **a confirmed earlier price-swing comparison** and **a current DI development**. They need not agree. | Read each legend separately; do not add or subtract them as if they were scores. |

#### Tier 3 — Normal but still informative

| Pattern you see | Meaning | What to examine next |
| --- | --- | --- |
| **Buy/Sell or Strong state with an ordinary black number and no event** | The classification still stands. No additional two-move color or fresh event qualified today. | Check ADX Trend and the signed Spread in the hover. |
| **Neutral without an arrow (▲/▼) or diamond (◆)** | No directional Signal or fresh qualifying event is displayed. Neutral can still contain a DI leader or a developing gap. | Check whether Neutral arose from low ADX, a gap below 5, or both. |

**Two important rules for reading the tables:**
1) **Blue/red numeric font is about widening/narrowing**, whereas **blue/red diamonds are about the direction of a price/ADX divergence**.
2) A diamond is **not** a prediction: a lower low with lower ADX can be followed by further price declines, and a higher high with lower ADX can be followed by further advances. See [How to Read an ADX Heatmap Cell](#how-to-read-an-adx-heatmap-cell).

---

## ADX(14) — Brief Overview
:small[[Back to top](#adx-signal-summary) | See Also: [ADX 101](#adx-metrics-the-3-values)]

**ADX** means **Average Directional Index**. It gauges **trend strength**, regardless of whether price is moving higher or lower. The directional indicators give the missing direction.

- **ADX Number (Trend Strength):** This value measures **intensity**. It ignores direction entirely. A high number means a fierce trend is happening; a low number means the market is drifting sideways.
- **[+DI Number (Buyer Strength)](#1--interpreting-trend-direction-di-and--di):** Short for _Positive Directional Indicator_. This measures how strongly the bulls are pushing the price upward.
- **-DI Number (Seller Strength):** Short for _Minus Directional Indicator_. This measures how aggressively the bears are driving the price downward.

| Metric | Plain-English question | How to read it |
| --- | --- | --- |
| :blue-background[ADX_14] | Is there meaningful trend strength? | Above 20 qualifies the application's basic trend-strength gate; above 25 meets its Strong gate. |
| :blue-background[DIp_14] (shown as **+DI**) | How much positive directional movement is present? | Above −DI means **buyers lead**. |
| :blue-background[DIn_14] (shown as **−DI**) | How much negative directional movement is present? | Above +DI means **sellers lead**. |
| :blue-background[Spread = +DI minus −DI] | Who leads, and by how many DI points? | Positive = buyers lead; negative = sellers lead; zero = tied. |
| **Δ vs prior day / Trend** | Is ADX strengthening or easing today? | Rising ADX means increasing smoothed trend strength; falling ADX means easing trend strength, **not necessarily a price reversal**. |

**Example:** +DI = 39.23 and −DI = 20.80 produces a **Spread of +18.43 points**. Buyers lead substantially. If ADX = 38.11, the application qualifies **Strong Buy** because ADX is above 25 and the positive gap is at least 10. The Signal describes the current condition; it does **not** say price must rise next session.

**Important:** ADX is not a volatility gauge, an overbought/oversold measure, or a forecast. A tight DI gap does not, by itself, prove volatility is low. A widening raw DI gap does **not** mathematically require ADX to rise: ADX smooths the **normalized** difference between the DI lines over time.


---
**Simple interpretation:**

* :blue-background[ADX] tells you **how strong the trend is**.
* :blue-background[+DI] tells you how much positive/upward directional movement is dominating.
* :blue-background[-DI] tells you how much negative/downward directional movement is dominating.
* :blue-background[+DI > -DI] means upward directional pressure is stronger.
* :blue-background[-DI > +DI] means downward directional pressure is stronger.
* Higher ADX means the trend is stronger, regardless of whether it is bullish or bearish.
* If the ADX is falling, it means the **trend is weakening**, so trend-following signals should be taken with caution.

**Value-added use:**
> Use ADX when you want to distinguish “*there is a real trend here*” from “*price is just chopping around*” and when you want to confirm whether the directional pressure is more bullish or bearish.

### Understanding the Spread Numbers
(:small[[Parent](#adx-14-brief-overview) | See Also: [Spread Color:  Blue or Red ADX Value](#spread-color--blue-or-red-adx-value)])

When comparing a spread of, say, -5 to a spread of -20 (where -DI is higher than +DI):
- **Spread of -5 (Narrow):** This indicates a tight, compressed market. Sellers have a slight edge, but buyers are fighting back. The market is likely in a consolidation phase, a weak trend, or preparing for a potential reversal.
- **Spread of -20 (Wide):** This indicates massive downward momentum. Sellers are completely dominating buyers. The wide gap shows that price ranges are expanding aggressively downward, signaling a highly stable and strong bearish trend

#### Key Trading Insights from Spread Magnitude
(:small[[Parent](#adx-14-brief-overview)])

Tracking +DI and -DI as a time series over time is highly beneficial. While the standalone ADX line tells you how hard the market is driving, it is completely "blind" to the steering wheel.
- Monitoring the historical behavior of the underlying +DI and -DI time series provides granular insights into shifts in market equilibrium.

##### 1. Trend Acceleration vs. Deceleration (Gauging the Intensity Shift (The "Spread"))
(:small[[Parent](#adx-14-brief-overview)])

Tracking the distance between the two time series over multiple intervals quantifies who is completely dominating the trend:
- When the gap between the +DI and -DI expands, it indicates that one group (buyers or sellers) is accelerating while the opposing group's momentum is collapsing.
- This confirms a high-probability continuation of the current trend.

**Expanding Spread:** When the gap between +DI and -DI is actively widening, the trend is accelerating. Said differently, it indicates that one group (buyers or sellers) is accelerating while the opposing group's momentum is collapsing.
- This confirms a high-probability continuation of the current trend.
	You should stay with the trend and avoid fighting the move.

**Contracting Spread:** When the gap begins to narrow (converge toward each other), the trend is losing steam.
- This typically happens _before_ a full crossover occurs and serves as an early warning to tighten stop-losses or take profits.
- This provides an early warning signal of a potential "range-bound" period or an upcoming "trend reversal" long before the ADX line falls.

##### 2a. Predicting ADX Turning Points
(:small[[Parent](#adx-14-brief-overview)])

- The ADX line is mathematically derived from the smoothed differences between +DI and -DI.
- A **widening spread** will force the ADX line to rise, confirming a strong trend.
- A **narrowing spread** causes the ADX line to flatten out and fall, signaling the end of the trend.

##### 2b. Identifying Early Entry and Exit Signals
(:small[[Parent](#adx-14-brief-overview)])

Using the crossover of these two time series serves as a mechanical trend-following engine:
* **Bullish Shift (+DI > -DI)**: Indicates buying pressure has overtaken selling pressure.
* **Bearish Shift (-DI > +DI)**: Indicates selling pressure has conquered buying pressure.


##### 3. Volatility and Breakout Confirmation
(:small[[Parent](#adx-14-brief-overview)])

- **The Squeeze:** When the spread shrinks close to zero, volatility is dangerously low.
- **The Pop:** A sudden, explosive widening of the spread confirms a legitimate breakout or breakdown, helping you filter out sideways market noise.

---
### Choosing among ADX(9), ADX(14), and ADX(20)
(:small[[Parent](#adx-14-brief-overview)])

| Variant | General behavior | Practical use |
| --- | --- | --- |
| **ADX(9)** | Reacts sooner to changing directional movement; more sensitive to short-lived shifts. | Examine emerging short-term conditions with extra attention to noise. |
| **ADX(14)** | Middle setting; the principal example throughout this guide. | Balanced day-to-day interpretation. |
| **ADX(20)** | Smoother; changes tend to develop more gradually. | Assess whether a condition persists over a longer window. |

All three use the **same five-state thresholds**, with separate values, confirmation histories and display events. A blue ADX(9) number does not mean ADX(14) or ADX(20) must also be blue.

---

## How to Read an ADX Heatmap Cell

:small[[Back to top](#adx-signal-summary)]

Read the cell in this order:

1. **Background / Signal:** Is it Strong Buy, Buy, Neutral, Sell, or Strong Sell? That is the rulebook classification.
2. **Number / Trend:** How strong is ADX, and did it [rise or fall](#rising-vs-falling-adx) versus the prior session?
3. **Number font color:** If blue or red, is the current DI leader gaining or losing control over two consecutive DI-gap moves?
4. **Symbol:** ▲/▼ identifies a **same-session DI leadership crossover**; blue/red ◆ identifies a **confirmed price/ADX divergence** derived from price swings.
5. **Hover evidence:** Check +DI, −DI, signed '*Spread*', the exact event explanation, '*Rule*', '*Context Interpretation*' and '*Bottom-line*'. Price and volume, where shown, provide separate confirmation or conflict.

**There can be multiple observations in one cell.** For example, a red diamond ${\textcolor{red}{\textsf{◆}}}$ (bearish [price/ADX divergence](#price-adx-divergence)) can coexist with a blue number (the current DI leader gaining control). The diamond compares **two older price swings**; the number color evaluates **the last two DI-gap changes**. Treat neither as an automatic new Buy or Sell.

**No marker is a valid outcome.** The absence of a diamond, arrow, or colored value means that particular display condition did not qualify or lacked sufficient evidence. It does not invalidate the underlying ADX Signal.

### Reading signed Spread and its changes

**Spread = +DI − −DI**
- For example, +DI = 21.06 and −DI = 31.05 gives **−9.99 points**: sellers lead by 9.99 DI points.
- A change from +3.89 to −9.99 is a **−13.88-point change** and a change in leadership—not simply a normal narrowing of an existing positive gap.

The hover may also show a **relative percentage change** in 'Spread'. The application calculates this from the signed point change divided by the **absolute magnitude of the previous 'Spread'**. When the previous 'Spread' is close to zero or a crossover occurs, this percentage can be very large and misleading as a measure of trend strength. **Read the actual DI points and crossover first.** When the prior Sp'read is zero or missing, no valid percentage is shown.

---
## Secondary Hover Metrics
:small[[Back to top](#adx-signal-summary)]

These fields provide context **without modifying the primary Signal or score**. They answer different questions; none should be interpreted as an extra sixth or seventh ADX state.

| Hover field | What it answers | When it appears |
| --- | --- | --- |
| **[+DI / −DI](#1--interpreting-trend-direction-di-and--di)** | Who is applying more positive or negative directional movement, and how did each reading change? | When the values exist. |
| **[Spread](#understanding-the-spread-numbers)** | Which side leads, by how many points, and how much did the signed difference change? | When both DI values exist. |
| **[DI Crossover](#di-crossover--black-arrows)** | Did the DI leader switch **today**? | On a qualifying strict bullish or bearish crossover day. |
| **[Price/ADX Divergence](#price-adx-divergence)** | Did price reach a new confirmed swing extreme without comparable ADX strength near that swing? | On the newer pivot's confirmation date when the comparison qualifies. |
| **[Spread Color](#spread-color--blue-or-red-adx-value)** | Has the same DI leader been gaining or losing control for **two consecutive changes**, with ADX above 20? | Only when the blue/red numeric-font condition qualifies; not on crossover days. |
| **Rule** | Why did the actual five-state Signal qualify, including why a non-Strong state is not Strong? | For verified, initialized classified observations. |
| **Context Interpretation** | How are the DI leadership, gap and smoothed ADX strength changing? | When the required current and prior observations are available. |
| **Bottom-line** | What do the Signal and recent developments mean **together**, including price context when available? | With sufficient verified input history; absence is not an extra neutral signal. |

### DI Crossover — Black Arrows
(:small[[Parent](#secondary-hover-metrics)])

| Event | Exact event condition | What it means |
| --- | --- | --- |
| **$\large{\textcolor{black}{\textsf{▲}}}$: Bullish** | Yesterday's signed Spread was **negative** and today's is **positive**. | :blue-background[Buyers have just taken control] of directional movement. This does **not** automatically qualify Buy. |
| **$\large{\textcolor{black}{\textsf{▼}}}$: Bearish** | Yesterday's signed Spread was **positive** and today's is **negative**. | :blue-background[Sellers have just taken control] of directional movement. This does **not** automatically qualify Sell. |

The crossover is a **one-session event**, not a persistent state. It requires a strict change from negative to positive, or positive to negative. A tie at exactly zero on either observation does not qualify under the current implementation. The hover writes **DI Crossover: (Bullish)** or **DI Crossover: (Bearish)** and explains the signed Spread transition.

**Example:** SPY's November 4, 2026 bullish crossover occurred while ADX(14) was only 16.40 and the positive gap was 3.20 points. The Signal remained **Neutral**. The next session produced a bearish crossover and again remained Neutral. **Two opposite arrows in succession are evidence of unstable DI leadership, not two confirmed trend reversals.**

### Spread Color — Blue or Red ADX Value
(:small[[Parent](#secondary-hover-metrics) | See Also: [Understanding the Spread](#understanding-the-spread-numbers)])

The *number itself* changes color only when **the same DI leader remains in place across three successive observations**, the absolute DI gap changes in the **same direction twice in a row**, and **current ADX is above 20**.

| Numeric font | Exact qualifying pattern | Plain-English interpretation |
| --- | --- | --- |
| ${\textcolor{DodgerBlue}{\textsf{Blue ADX value}}}$ | Same DI leader for three readings; absolute gap **widened twice**; ADX > 20. | The current leader—**bulls or bears**—has been gaining control. |
| **${\textcolor{red}{\textsf{Red ADX value}}}$** | Same DI leader for three readings; absolute gap **narrowed twice**; ADX > 20. | The current leader—**bulls or bears**—has been losing some control. |
| **Ordinary value** | Either condition not met, including ADX ≤ 20, ties, insufficient history, mixed changes, or a crossover. | No qualifying two-move color state; examine the signed Spread normally. |

**Examples (illustrative, not historical):** If the bullish gap increases from +10 to +13 to +18, and ADX is above 20, **buyers are gaining control** and the numeric font is blue. If the bearish gap changes from −20 to −16 to −12, and ADX is above 20, **sellers are losing some control** and the numeric font is red. Both examples use the *magnitude* of the gap, not whether its signed value increased.

**Do not confuse color with direction:** A **blue number** may accompany Strong Sell if bears are gaining control. A **red number** may accompany Strong Buy if bulls are losing some control. **The color is suppressed on a DI crossover date in the same ADX row:** that day the black arrow identifies the new leader instead. Also, blue does **not** say ADX rose, and red does **not** say ADX fell. Confirm ADX's own direction separately from **Trend** or **Δ vs prior day**.

### Price ADX Divergence
(:small[[Parent](#secondary-hover-metrics)])

A **blue or red ◆** signals a **swing-level nonconfirmation**, not a one-day disagreement between price and ADX. The current display definition compares two consecutive **confirmed five-bar price swing highs**, or two consecutive **confirmed five-bar price swing lows**. Each price swing is compared with the **highest ADX reading from two sessions before through two sessions after that price pivot**.

| Diamond | Price pattern | ADX requirement | What it suggests |
| --- | --- | --- | --- |
| **$\large{\textcolor{DodgerBlue}{\textsf{◆}}}$: Bullish divergence** | A **lower confirmed price swing low** than the preceding confirmed swing low. | The nearby ADX peak is **lower** at the newer low. | Price fell to a new low without higher ADX strength. If **−DI still leads**, the downtrend may be tiring—not necessarily reversing. |
| **$\large{\textcolor{red}{\textsf{◆}}}$: Bearish divergence** | A **higher confirmed price swing high** than the preceding confirmed swing high. | The nearby ADX peak is **lower** at the newer high. | Price rose to a new high without higher ADX strength. If **+DI still leads**, the uptrend may be tiring—not necessarily reversing. |

**Timing matters.** A five-bar price pivot has two earlier and two later sessions. The newer price pivot is therefore **confirmed two trading sessions later**. The ◆ appears on **that confirmation date**, not on the older pivot date or retroactively on the new extreme's date. The price swing dates, prices and nearby ADX peaks are reported in the hover so the user can reconstruct the observation.

**Example from the diagnostic:** NVDA's ADX(14) event confirmed August 31, 2026 compared higher price swing highs of :gray-background[$227.92 → $230.47] with lower nearby ADX peaks of :gray-background[21.04 → 17.33]. It therefore qualifies as a **red ◆ (bearish divergence)**. It does not itself forecast a price decline.

**Qualification:** This definition does **not** impose an ADX-above-20 gate. If the compared ADX peaks are both below 20, treat the event as nonconfirmation under already-weak trend conditions—not as strong-trend exhaustion.


**DI leadership is checked on the confirmation date:**

- **Aligned:** +DI leads at a higher-high/$\large{\textcolor{red}{\textsf{◆}}}$ event, or −DI leads at a lower-low/$\large{\textcolor{DodgerBlue}{\textsf{◆}}}$ event. The original directional side still leads, but price's new extreme lacks comparable ADX strength.
- **Contrary:** −DI leads at a higher-high/$\large{\textcolor{red}{\textsf{◆}}}$ event, or +DI leads at a lower-low/$\large{\textcolor{DodgerBlue}{\textsf{◆}}}$ event. The swing-level event remains visible, but leadership has already shifted; do not describe the old side as still in control.
- **Tied:** +DI equals −DI. The swing-level observation remains; neither DI currently leads.

**Do not confuse the diamond's color with the number's color.** The diamond identifies the **kind of price swing** (lower low or higher high) that ADX failed to confirm; the number color identifies **recent DI-gap development**. A divergence can coexist with a bullish or bearish Signal, a colored number, or a crossover arrow. None is itself proof of a reversal or a command to trade.

---

## Reading the Rule, Context Interpretation and Bottom-line Together

:small[[Back to top](#adx-signal-summary)]

The three narrative fields have different jobs:

| Field | What to ask |
| --- | --- |
| **Rule** | **Why is this a Strong Buy, Buy, Neutral, Sell or Strong Sell today?** |
| **Context Interpretation** | **Are bulls or bears taking control, gaining ground, losing ground, or seeing smoothed trend strength change?** |
| **Bottom-line** | **What do those facts imply together—and does today's price move support or contradict that reading?** |

**Example — Strong Buy with some easing:** XLP on November 9, 2026 had ADX(14) **38.11**, +DI **39.23**, −DI **20.80**, and Spread **+18.43**. The values clearly qualify **Strong Buy**. But ADX eased from **38.68**, and the bullish Spread had increased only marginally from **18.25**. **Plain English:** Bulls remained firmly in control; the latest movement did not show uniform fresh strengthening. A Strong Buy Signal can persist while conditions begin to moderate.

**Example — Neutral with a fresh change:** A bullish ▲ while ADX is below 20 says buyers have just taken control of DI, **not** that a qualifying bullish trend has been established. A bearish ▼ the following day can reverse that leadership without either day qualifying for Sell.

---

## ADX Rule Translation

:small[[Back to top](#adx-signal-summary)]

The expressions below describe **ADX(14)**. For ADX(9) or ADX(20), replace the period in ADX, +DI and −DI consistently; the numeric thresholds remain the same. Classification is based on initialized actual values. Missing ADX or DI inputs remain **Missing**, not Neutral.

### Strong Buy (ADX)

**Literal trigger:** :gray-background[ADX_14 > 25] **and** :gray-background[DIp_14 − DIn_14 ≥ 10].

**Literal component breakdown:**
ADX is **strictly above 25**; +DI is **at least 10 points above** −DI. Both conditions must hold.

**Plain English:**
- **Bulls are firmly in control, and the trend is strong.**
This describes current directional conditions, not a guaranteed gain tomorrow.

### Buy (ADX)

**Literal trigger:** :gray-background[ADX_14 > 20] **and** :gray-background[DIp_14 − DIn_14 ≥ 5] **and** :gray-background[ADX_14 ≤ 25 or DIp_14 − DIn_14 < 10].

**Literal component breakdown:**
- ADX exceeds **20** and buyers lead by at least **5** DI points. But **ADX does not exceed 25** or the lead is **below 10**; therefore the Strong Buy conditions are not both met.

**Plain English:**
- **Bulls are in control, and there is meaningful trend strength, but the Strong Buy requirements are not both met.**
- For example, ADX = 30 with a +7-point DI gap is **Buy**, not Strong Buy.

### Neutral (ADX)

**Literal trigger:** :gray-background[ADX_14 ≤ 20] **or** :gray-background[absolute DIp_14 − DIn_14 gap < 5].

**Literal component breakdown:**
- Either the smoothed strength is **20 or lower**, or buyers and sellers are separated by **less than 5 DI points**.
- One condition is enough.

**Plain English:**
- **The trend is too weak or neither side controls directional movement by enough to qualify.** It does not mean +DI equals −DI.
- A recent ▲ or ▼ may still be visible with Neutral.
- Missing/warmup is a separate condition.

### Sell (ADX)

**Literal trigger:** :gray-background[ADX_14 > 20] **and** :gray-background[DIn_14 − DIp_14 ≥ 5] **and** :gray-background[ADX_14 ≤ 25 or DIn_14 − DIp_14 < 10].

**Literal component breakdown:**
- ADX exceeds **20** and sellers lead by at least **5** points. But **ADX does not exceed 25** or the lead is **below 10**; therefore the Strong Sell conditions are not both met.

**Plain English:**
- **Bears are in control, and there is meaningful trend strength, but the Strong Sell requirements are not both met.**
- For example, ADX = 30 with a −7-point signed Spread is **Sell**, not Strong Sell.

### Strong Sell (ADX)

**Literal trigger:** :gray-background[ADX_14 > 25] **and** :gray-background[DIn_14 − DIp_14 ≥ 10].

**Literal component breakdown:**
- ADX is **strictly above 25**; −DI is **at least 10 points above** +DI. Both conditions must hold.

**Plain English:**
- **Bears are firmly in control, and the trend is strong.**
- This describes current directional conditions, not a guaranteed decline tomorrow.

---

## Industry-Standard Baseline and Practical Limits

:small[[Back to top](#adx-signal-summary)]

The underlying ADX/DMI framework was developed by J. Welles Wilder Jr. Standard charting references commonly describe **ADX below 20** as weak or trendless, **20–25** as a transition zone, and **above 25** as stronger trending conditions. Many traders use ADX with price structure, moving averages, momentum and volume rather than in isolation. The application's **five-state Signal and 5-/10-point DI-gap tests are its own transparent rulebook choices**, not Wilder's universal buy/sell rules.

| Useful pairing | What it adds beyond ADX |
| --- | --- |
| **Price chart / moving averages** | Whether price structure agrees with the indicated direction. |
| **RSI, STOCH, ROC or MACD** | Momentum and potential exhaustion/reversal context. ADX alone is not an overbought/oversold measure. |
| **CMF, MFI or VWMA** | Participation and money-flow context. |
| **ATR / Bollinger Bands** | Price-range volatility, which cannot be inferred from the DI gap alone. |

**Limitations:** ADX is smoothed and lagging. A rising ADX can describe a strengthening **downtrend**. A falling ADX does not prove price will reverse. DI crosses can be frequent in choppy markets. A confirmed price/ADX divergence indicates nonconfirmation at past swings, **not** a statistically proven entry or exit. Strong ADX is not, by itself, an overbought/oversold warning.

**Reference material:** [StockCharts — Average Directional Index](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/average-directional-index-adx) · [Fidelity — Average Directional Index](https://www.fidelity.com/viewpoints/active-investor/average-directional-index-adx) · [Schwab — ADX and RSI together](https://www.schwab.com/learn/story/spot-and-stick-to-trends-with-adx-and-rsi).

### Notes on superseded interpretations

Older notes in this guide used different Buy/Sell thresholds and described Spread widening as necessarily making ADX rise or guaranteeing continuation. Those statements have **not** been retained as active interpretation rules because they contradict either the current rulebook or ADX's smoothed calculation. The five-state table and Rule Translation in this version are the authoritative descriptions of the application's active ADX(9/14/20) classification; the visual customization definitions describe the separately proposed ADX Visual Enhancements implementation.

### Scope and documentation discipline

This guide explains the **intended** ADX visual enhancements alongside the already-verified classification and hover behavior. The diamond and numeric-font additions should be treated as **pending production acceptance until their display is manually verified** in Rolling Heatmap, SCD Single Indicator and SCD Multiple Indicators. No documentation statement changes score or approves a trading strategy. Adjust the implementation-status note after live acceptance, without changing the analytical definitions.

## ADX 101
:small[[Back to top](#adx-signal-summary)]

The **Average Directional Index (ADX)** is a technical indicator that measures the **strength** of a market trend, regardless of whether the price is moving up or down.

### Core Components
:small[[Parent](#adx-101)]

- **ADX Line (Trend Strength):** A single line that oscillates between **0 and 100**. It does not tell you if the trend is bullish or bearish—only how strong the current move is.
- **+DI Line (Positive Directional Indicator):** Measures the strength of upward price movement (often colored green).
- **-DI Line (Minus Directional Indicator):** Measures the strength of downward price movement (often colored red).

### Cheat sheet
:small[[Parent](#adx-101)]

To understand the market conditions at any given moment, look at the relationship between these numbers:
##### Step 1: Check who is winning (Compare +DI and -DI)
- **If +DI is greater than -DI:** The **buyers are in control** (Bullish environment).
- **If -DI is greater than +DI:** The **sellers are in control** (Bearish environment). 
##### Step 2: Check if it's worth trading (Look at the ADX value)
- **ADX is below 20:** The market is **choppy or range-bound**. No matter which DI number is higher, the trend is weak. Breakout strategies will likely experience false signals here. 
- **ADX is above 25:** A **genuine trend** has broken out. Trend-following setups (like buying pullbacks or riding momentum) become much more reliable.
- **ADX is above 40 to 50:** An **extremely strong trend** is in play. The market is moving aggressively in one direction.

> See "[[#How to Read ADX Values]]" below for more details.

---

### ADX Metrics: the 3 values
:small[[Parent](#adx-101)]

When tracking the **ADX (Average Directional Index)**, the "three numbers" you see typically refer to the **live numerical readings** of the indicator's three component lines at the specific spot where your cursor is hovering. 

Here is exactly how to break down what those three numbers mean and how to interpret them in real-time.

$\Large{\textsf{The Core Meanings of the 3 Numbers}}$
In almost all charting software, the three numbers correspond to these specific metrics (usually color-coded to match the lines on your chart):
- **The ADX Number (Trend Strength):** This value measures **intensity**. It ignores direction entirely. A high number means a fierce trend is happening; a low number means the market is drifting sideways.
- **The +DI Number (Buyer Strength):** Short for _Positive Directional Indicator_. This measures how strongly the bulls are pushing the price upward.
- **The -DI Number (Seller Strength):** Short for _Minus Directional Indicator_. This measures how aggressively the bears are driving the price downward.

---
### How to Read ADX Values
:small[[Parent](#adx-101)]

> 1. **Use the +/- DI values first to pin down the direction.**
> 2. **Then look at the ADX to see if that direction actually has the muscle to back it up.**

#### 1- Interpreting Trend Direction (+DI and -DI)
:small[[Parent](#adx-101)]

While the ADX line tells you _how strong_ the trend is, the two DI lines tell you _who is in control_: 
- **Bullish Signal:** The **+DI** is above the **-DI**. If the ADX is rising above 25 at the same time, the upward trend is gaining solid momentum.
- **Bearish Signal:** The **-DI** is above the **+DI**. If the ADX is rising above 25 here, the downward trend is gathering strong momentum.
- **Crossovers:** When the +DI and -DI cross each other, it hints at a potential change in trend direction.

---
#### 2- Verify Trend Validity/Strength
:small[[Parent](#adx-101)]

- **Below 20:** Indicates a weak, absent, or sideways (range-bound) market. Trend-following strategies often struggle here.
- **20 to 25:** Represents a transition zone where a new trend may be starting.
- **Above 25:** Signals a strong trend is underway, making trend-following systems more reliable.
- **Above 40 to 50+:** Indicates a very strong or extreme trend momentum. 

##### Rising vs. Falling ADX
:small[[Parent](#adx-101)]

- **Rising ADX:** The current trend—whether up or down—is **strengthening**.
- **Falling ADX:** The current trend is **weakening** or losing steam (which can happen right before the market shifts into a range or reverses).

---

#### Real-World Examples
:small[[Parent](#adx-101)]

To see how this works in practice, consider these scenarios:

| If you see these numbers...                   | ...Here is what it means:                                                                                                                                                  |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ADX:** 35  <br>**+DI:** 28  <br>**-DI:** 12 | **Strong Uptrend:** The +DI is much higher than the -DI (bulls control the board), and the ADX is well above 25, meaning this upward move has powerful momentum behind it. |
| **ADX:** 42  <br>**+DI:** 10  <br>**-DI:** 36 | **Strong Downtrend:** The -DI dominates the +DI (bears are crushing it), and because the ADX is up at 42, it is a very aggressive, sustained sell-off.                     |
| **ADX:** 14  <br>**+DI:** 22  <br>**-DI:** 19 | **Sideways Market:** Even though +DI is technically higher, the ADX is down at 14. This tells you the asset is just bouncing around aimlessly in a tight box.              |

_(Note: In some settings, you might also see a standalone "14" listed next to the indicator name. That isn't a live reading; it simply denotes the default **14-period lookback window** used to calculate the data.)_


---
### The Behind-the-Scenes Math (The DX Formula)
:small[[Parent](#adx-101)]

**The three numbers do not have a simple mathematical relationship like a sum or a difference.** You cannot add or subtract them to equal the ADX.
Instead, the ADX is calculated through a multi-step mathematical process where the **relative difference** and **total sum** of the DI values are compressed and smoothed out over time.

To see why they don't cleanly add up, look at how the indicator builds the **Directional Movement Index (DX)**before smoothing it into the final ADX. On any given day, the formula uses the absolute difference and the sum of the DI lines like this:

$$\text{DX}=\left(\frac{|{}(+DI)-(-DI)|{}}{(+DI)+(-DI)}\right)\times 100$$

Because the formula divides the difference by the sum, it creates a ratio that always falls between 0 and 100:

- **If +DI and -DI are identical** (e.g., both are 20), the top of the fraction becomes 0, making the DX **0**.
- **If one DI completely dominates the other** (e.g., +DI is 40 and -DI is 0), the fraction becomes $(40 / 40)$, making the DX **100**.

---

### How DX Becomes ADX
:small[[Parent](#adx-101)]

The number you see on your screen isn't just the raw DX from today. The final **ADX** is a **moving average**(typically a 14-period smoothed Wilder's Moving Average) of those daily DX values.

Because it averages the last 14 periods of market behavior, the ADX line moves much more slowly and smoothly than the erratic, daily crisscrossing of the +DI and -DI lines. This lag is intentional—it prevents you from getting tricked by a sudden, single-day price spike.

---
## ADX (Notes)
(:small[[Back to top](#adx-14-signal-summary)])

**Overview**
The ADX, a component of J. Welles Wilder Jr.’s Directional Movement System, measures trend strength independent from trend direction.
- An ascending ADX signals an intensifying trend – regardless if it is bullish or bearish; conversely,
- a falling ADX implies either weakening trends or conditions within trading ranges.

Two directional indicators – the +DI and the -DI – supplement the ADX to ascertain trend directionality.

The ADX proves invaluable for ${\textcolor{Red}{\textsf{identifying a trend’s strength}}}$ over time. It serves traders in confirming whether they should continue holding their position for an extended trend or prepare against potential exhaustion of said trend. The ADX itself does not signal direction; however, this crucial information is provided by the interplay between +DI and -DI.

---
**Purpose:** Measure the strength of a trend without indicating its direction, helping traders determine whether to use trend-following or range-bound strategies.

**Use when:** You need to determine if the market is trending strongly enough to warrant trend-following strategies rather than range-bound approaches.
- **Note**: ADX is highly ineffective in sideways, "range-bound" markets.

**Key Concept:** Quantifies trend strength on a scale of 0-100. High ADX values indicate strong trends (regardless of direction), while low values suggest weak or non-trending markets.

**Calculation:** Complex calculation involving True Range and Directional Movement, smoothed with exponential moving averages to create a single oscillating line.

**Signals & Interpretation:**
Measures trend strength on a scale of 0-100 (ignores direction).
- ADX above 25 = strong trend (use 'trend-following' strategies)
- ADX below 20 = weak trend (use 'range-bound' strategies)
- Rising ADX = strengthening trend
- Falling ADX = weakening trend

$$----------$$
- **Trend Strength:**
	- **Above 25:** A genuine trend exists.
		- **Between 25 and 50:** A moderate-strength trend.
		- **Between 50 and 75:** A strong trend.
		- **Above 75:** An extremely strong, potentially unsustainable trend.
	- **Below 20:** Suggests a weak trend or no clear trend at all.
		- **<20 to 25:** No clear trend signals.

- **Trend Momentum:**
    - An up-sloping ADX indicates a strengthening trend. 
    - A down-sloping ADX indicates a weakening trend. 
    - A changing slope of the ADX line can serve as an early indicator of a developing trend. 

- **Trend Direction**:
	- **Uptrend:** When the '+DI' (positive Directional Indicator) is above the '-DI' (negative Directional Indicator), the trend is bullish. 
	- **Downtrend:** When the '-DI' is above the '+DI', the trend is bearish.


## Index: ADX
:small[[Back to top](#adx-signal-summary)]

**Quick Reference**
- [At a Glance: What Each Part of the Heatmap Means](#at-a-glance-what-each-part-of-the-heatmap-means)
- [HTR: Five-State Signals](#htr-five-state-signals)
- [Key Combinations: What Deserves Attention](#key-combinations-what-deserves-attention)
  - [Tier 1 — Strongest Aligned or Cautionary Combinations](#tier-1-strongest-aligned-or-cautionary-combinations)
  - [Tier 2 — Early Changes and Conflicting Evidence](#tier-2-early-changes-and-conflicting-evidence)
  - [Tier 3 — Normal but Still Informative](#tier-3-normal-but-still-informative)

**Understanding ADX and Its Displays**
- [ADX(14) — Brief Overview](#adx14-brief-overview)
  - [Understanding the Spread Numbers](#understanding-the-spread-numbers)
  - [Key Trading Insights from Spread Magnitude](#key-trading-insights-from-spread-magnitude)
	  - [1. Trend Acceleration vs. Deceleration (Gauging the Intensity Shift (The "Spread"))](#1-trend-acceleration-vs-deceleration-gauging-the-intensity-shift-the-spread)
	  - [2a. Predicting ADX Turning Points](#2a-predicting-adx-turning-points)
	  - [2b. Identifying Early Entry and Exit Signals](#2b-identifying-early-entry-and-exit-signals)
	  - [3. Volatility and Breakout Confirmation](#3-volatility-and-breakout-confirmation)

- [Choosing Among ADX(9), ADX(14), and ADX(20)](#choosing-among-adx9-adx14-and-adx20)
- [How to Read an ADX Heatmap Cell](#how-to-read-an-adx-heatmap-cell)
- [Reading Signed Spread and Its Changes](#reading-signed-spread-and-its-changes)

**Secondary Hover Metrics**
- [Secondary Hover Metrics — Overview](#secondary-hover-metrics)
- [DI Crossover — Black Arrows](#di-crossover-black-arrows)
- [Spread Color — Blue or Red ADX Value](#spread-color-blue-or-red-adx-value)
- [Price/ADX Divergence](#price-adx-divergence)
- [Reading the Rule, Context Interpretation and Bottom-line Together](#reading-the-rule-context-interpretation-and-bottom-line-together)

**Signal Rules and Reference**
- [ADX Rule Translation](#adx-rule-translation)
  - [Strong Buy](#strong-buy-adx)
  - [Buy](#buy-adx)
  - [Neutral](#neutral-adx)
  - [Sell](#sell-adx)
  - [Strong Sell](#strong-sell-adx)
- [Industry-Standard Baseline and Practical Limits](#industry-standard-baseline-and-practical-limits)
- [Notes on Superseded Interpretations](#notes-on-superseded-interpretations)
- [Scope and Documentation Discipline](#scope-and-documentation-discipline)

**Overview**
- [ADX 101](#adx-101)
- [ADX (Notes)](#adx-notes)
