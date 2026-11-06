## Summary: Bollinger %B signals
(:small[[TOC](#toc-bollingers)] | :small[See Also: [Bollinger 101](#bollinger-101)])

The TA Rule Engine uses Bollinger [%B](#b-where-is-price-relative-to-the-bands) as a **current-location contrarian / exhaustion measure**.

In simple terms:

- Low :blue-background[%B] readings mean price is near or below the lower Bollinger Band.
- High :blue-background[%B] readings mean price is near or above the upper Bollinger Band.
- The farther price stretches beyond a band, the stronger the project's exhaustion signal becomes.
- A Buy or Sell label describes **how stretched price currently is**. It does **not** mean that a reversal has already occurred or is guaranteed to occur.

The table below uses the balanced [BB(20,2.0)](#bb2020-b-rules-interpretation) medium-term setting as the main example.

| Signal | Literal trigger | Layman’s Translation | Rule Logic | Signal takeaway |
| --- | --- | --- | --- | --- |
| [strong_buy](#strong-buy-b) | :gray-background[%B < -10] | Price is materially below the lower Bollinger Band. | The current price has stretched far enough below the lower band to qualify as an unusually deep downside extension. | Price is exceptionally stretched below its Bollinger envelope. |
| [buy](#buy-b) | :gray-background[-10 <= %B < 10] | Price is near the lower band or modestly below it. | Price is in the project's lower-band exhaustion zone, but the stretch is not deep enough to qualify as Strong Buy. | Price is trading near the low side of its Bollinger envelope. |
| [neutral](#neutral-b) | :gray-background[10 <= %B <= 90] | Price is comfortably inside the bands and away from either exhaustion zone. | :blue-background[%B] is inside the project's middle / Neutral zone. | Price is not currently stretched toward either Bollinger extreme. |
| [sell](#sell-b) | :gray-background[90 < %B <= 110] | Price is near the upper band or modestly above it. | Price is in the project's upper-band exhaustion zone, but the stretch is not large enough to qualify as Strong Sell. | Price is trading near the high side of its Bollinger envelope. |
| [strong_sell](#strong-sell-b) | :gray-background[%B > 110] | Price is materially above the upper Bollinger Band. | The current price has stretched far enough above the upper band to qualify as an unusually large upside extension. | Price is exceptionally stretched above its Bollinger envelope. |

> **Important:** These are the medium-term :blue-background[BB(20,2.0)] thresholds. The short- and long-term Bollinger settings use the same :gray-background[10–90] Neutral zone but different Strong thresholds because their band configurations behave differently.

The three configured **[%B](#b-where-is-price-relative-to-the-bands)** views are:

| Horizon | Bollinger setting | Strong Buy | Buy | Neutral | Sell | Strong Sell |
| --- | --- | --- | --- | --- | --- | --- |
| Short term | [BB(10,1.5)](#bb1015-b-rules-interpretation) | :gray-background[%B < -20] | :gray-background[-20 <= %B < 10] | :gray-background[10 <= %B <= 90] | :gray-background[90 < %B <= 120] | :gray-background[%B > 120] |
| Medium term | [BB(20,2.0)](#bb2020-b-rules-interpretation) | :gray-background[%B < -10] | :gray-background[-10 <= %B < 10] | :gray-background[10 <= %B <= 90] | :gray-background[90 < %B <= 110] | :gray-background[%B > 110] |
| Long term | [BB(50,2.5)](#bb5025-b-rules-interpretation) | :gray-background[%B < 0] | :gray-background[0 <= %B < 10] | :gray-background[10 <= %B <= 90] | :gray-background[90 < %B <= 100] | :gray-background[%B > 100] |

These thresholds are **project-specific calibrations**, not universal Bollinger rules. The table's final column summarizes the **Signal alone**, whereas the enhanced hover's :blue-background[Bottom-line] combines price location with verified Bandwidth and breach evidence. They answer different questions.

The most useful next step is to consult [The Bollinger patterns you should not overlook](#the-bollinger-patterns-you-should-not-overlook). For a specific combination, use the [complete pattern reference](#bollinger-pattern-reference-complete-interpretations).

---
$\Large{\textsf{Bolllinger Metrics}}$
(:small[Section: [The Bollinger measurements at a glance](#the-bollinger-measurements-at-a-glance)])

| | [%B](#b--where-is-price-relative-to-the-bands) / [Signal](#summary-bollinger-b-signals) | [Bandwidth State](#bandwidth-state) | [Bandwidth Change (1D)](#bandwidth-change-1d) | [Bandwidth Development](#bandwidth-development-multi-session-context) | [Breach Status](#breach-status-and-compression-exit) | [Bottom-line](#how-the-bottom-line-chooses-what-to-explain) |
| --- | --- | --- | --- | --- | --- | --- |
| **Question answered** | <li>Where is price relative to the bands? <li> Where are we?| <li>How wide are bands compared with their recent history? <li>Is a big move about to happen? | <li>Did width expand/contract materially since yesterday? <li>What just happened?| <li>Has width changed materially across several sessions? <li>Is bandwidth emerging from compression, expanding persistently, leveling off, or contracting? | Has price just left, stayed beyond, or re-entered a band? | What is the dominant combination telling us? |
| **What it measures** | Normalized current price position and project contrarian score | Historical relative level of Bandwidth | One-session relative Bandwidth movement | Five-session absolute and relative change; qualifying 1D streak; Compression Exit | Current outside/inside state compared with preceding observations | Conditional synthesis, not a new score |
| **Comparison** | Price vs current lower/upper band | Current Bandwidth vs historical 60/120 observations | Current vs previous Bandwidth | Current vs five sessions ago; consecutive 1D classifications | Current and earlier band positions | Validated evidence across the preceding columns |
| **Outputs** | :gray-background[Strong Buy / Buy / Neutral / Sell / Strong Sell] | :gray-background[Very Narrow / Narrow / Typical / Wide / Very Wide] | :gray-background[Expanding / Contracting / Stable] | Five-session points and percentage, directional streak and event | Fresh/Continuing Breach, Re-entry, No Active Breach, or unavailable/onset unknown | A concise condition-specific interpretation, or no statement |


---
$\large{\textsf{Field Definitions:}}$
(:small[For more details, see: [Understanding the enhanced Bollinger %B hover](#enhanced-b-hover-field-map)])

- **Value**: Current band width as a percentage of the middle band; higher means wider bands.
- **Bandwidth State**: How unusual today's width is versus the stock's own recent history (ST: 60 observations; MT/LT: 120).
- **Bandwidth Change (1D)**: Whether the bands are Expanding, Contracting, or Stable under the horizon-specific tolerance.
- **Bandwidth Development**: Five-session change and consecutive movement, where available.
- **Breach Status**: Whether price is outside, returning inside, or remaining within the Bollinger envelope.

> **Important**: Absolute Bandwidth values are not universal Narrow/Wide thresholds. Bandwidth measures volatility, not price direction.

---
## The Bollinger patterns you should not overlook
(:small[[Back to top](#summary-bollinger-b-signals)] | :small[[Detailed pattern reference](#bollinger-pattern-reference-complete-interpretations)])

These patterns are ranked by **information value for interpretation**, **not** backtested profit potential. Historical compression has particular priority because the ordinary :blue-background[%B] Signal cannot tell you whether the surrounding band envelope is exceptionally narrow.

| Priority | Pattern to recognize | Key evidence | Why it matters | Detailed reference |
| --- | --- | --- | --- | --- |
| **Tier 1 — Compression** | Historically exceptional narrowing or sustained squeeze | :blue-background[Bandwidth State] = :gray-background[Very Narrow] or :gray-background[Narrow]; assess 1D and five-session development | Reveals an unusually quiet envelope, even when :blue-background[Signal] is Neutral | [Compression and setup](#compression-and-setup-patterns) |
| **Tier 2 — Emerging release / Compression Exit** | Price tests or breaches an outer band as compressed Bandwidth widens, or the envelope actually exits compression | Price location + :blue-background[Breach Status] + :blue-background[Bandwidth Development] + :blue-background[Bandwidth State] | Distinguishes an early directional attempt from a qualifying volatility-state transition | [Bullish](#bullish-price-action-patterns) / [Bearish](#bearish-price-action-patterns) |
| **Tier 3 — Sustained extension** | Repeated closes beyond the upper or lower band with established Bandwidth expansion | :gray-background[Continuing Upper/Lower Breach] + material, persistent widening | Identifies directional price pressure continuing during expanding volatility | [Bullish](#bullish-price-action-patterns) / [Bearish](#bearish-price-action-patterns) |
| **Tier 4 — Re-entry** | Price returns inside after an outside-band extension | :gray-background[Upper/Lower-Band Re-entry] + current Bandwidth trajectory | Shows an interruption of the prior extension, with or without volatility cooling | [Bullish](#bullish-price-action-patterns) / [Bearish](#bearish-price-action-patterns) |
| **Tier 5 — Elevated volatility / cooling** | Exceptionally wide envelope after material recent expansion, or an elevated envelope beginning to narrow | :gray-background[Very Wide] + five-session development + :blue-background[Bandwidth Change (1D)] | Distinguishes a high-volatility pause from actual cooling or normalization | [Volatility development](#volatility-development-patterns) |

**Reading priority:** First identify the historical volatility environment; next determine whether a boundary event occurred; finally evaluate whether widening or contraction is persistent. The same contrarian :blue-background[Sell] can coexist with an upside extension, just as :blue-background[Strong Buy] can coexist with persistent downside pressure.

For the three-step reading workflow, see [Setup → Transition → Development](#setup-transition-and-development). For threshold definitions, see [Measurement comparison](#the-bollinger-measurements-at-a-glance).

---

## How to read the Bollinger heatmap
(:small[[Back to top](#summary-bollinger-b-signals)] | :small[[Priority patterns](#the-bollinger-patterns-you-should-not-overlook)] | :small[[Understanding the enhanced Bollinger %B hover](#understanding-the-enhanced-bollinger-b-hover)])

Each configured horizon has a :blue-background[%B] row and a standalone :blue-background[BB Bandwidth] row. The enhanced :blue-background[%B] hover now brings the relevant Bandwidth context into the same observation; the standalone Bandwidth rows continue to describe nondirectional volatility rather than Buy/Sell price pressure.

| Horizon | Price-position row | Standalone volatility row | Bands used |
| --- | --- | --- | --- |
| Short term | :blue-background[BB %B(ST)] | :blue-background[BB Bandwidth(ST)] | :gray-background[BB(10,1.5)] |
| Medium term | :blue-background[BB %B] | :blue-background[BB Bandwidth] | :gray-background[BB(20,2.0)] |
| Long term | :blue-background[BB %B(LT)] | :blue-background[BB Bandwidth(LT)] | :gray-background[BB(50,2.5)] |

### Reading a %B cell
(:small[[Physical %B landmarks](#b-where-is-price-relative-to-the-bands)] | :small[[Five-state boundaries](#project-b-rules-consolidated-reference)])

The printed number is :blue-background[%B] in displayed units, not the classifier's score. For example, :gray-background[%B = 93.4] falls in the MT :gray-background[90 < %B <= 110] interval, so the Signal is :gray-background[Sell]. The number says **price is near the upper band**. The Signal reflects the project's **contrarian exhaustion convention**, not a confirmed reversal.

**Cell background:** determined by the authoritative five-state :blue-background[Signal] score. :blue-background[Bandwidth State] and :blue-background[Breach Status] do not alter the score or background.

### Reading the new display-value customizations
(:small[[Bandwidth State cutoffs](#bandwidth-state-calibration-by-horizon)] | :small[[Compression Exit definition](#compression-exit-a-bandwidth-state-event)])

| Display | Exact qualification | What it means | What it does not mean |
| --- | --- | --- | --- |
| **${\textcolor{Purple}{\textsf{\%B number}}}$** (lighter lavender on dark cells) | Matching historical :blue-background[Bandwidth State] is :gray-background[Very Narrow]: ST below the 10th percentile; MT/LT below the 5th | The Bollinger envelope is exceptionally compressed relative to the ticker's own historical Bandwidth | It does not indicate bullish or bearish direction; normal :gray-background[Narrow] is **not** colored purple |
| **$\large{◆}$ after the %B number** | :blue-background[Compression Exit] occurred **on this session** | Bandwidth has transitioned from :gray-background[Very Narrow/Narrow] to :gray-background[Typical/Wide/Very Wide] while today's 1D change qualifies as :gray-background[Expanding] | It does not, by itself, identify an upside or downside breakout or a support/resistance break |
| **No extra mark** | Neither visual condition qualifies, or supporting evidence is unavailable | The standard numeric value and score still apply | It does not establish that the observation is unimportant |

**Concrete GOOGL examples (MT):** On October 8, 2026, :gray-background[%B = 66.7] is purple because historical Bandwidth was at the :gray-background[2.1st percentile] (Very Narrow). On October 22, :gray-background[%B = −24.9 ◆] identifies that day's Compression Exit. The diamond is a separate visual event, not part of the number or score.

The diamond is black and displayed without a white box, approximately one character space after the value. Both treatments apply to the three heatmap views; the separate Single Indicator Trend Chart is not part of this enhancement.

### Setup, transition and development
(:small[[Full patterns](#bollinger-pattern-reference-complete-interpretations)] | :small[[Breach status](#breach-status-price-versus-the-bands)])

The practical reading sequence is:

| Stage | Question | Primary evidence | Practical interpretation |
| --- | --- | --- | --- |
| **Setup** | Is volatility unusually compressed? | :blue-background[Bandwidth State] and percentile; five-session narrowing | The envelope is unusually narrow; watch whether a boundary test develops |
| **Transition** | Is price testing/leaving a band as Bandwidth begins widening? | :blue-background[%B], :blue-background[Breach Status], :blue-background[Bandwidth Change (1D)], :blue-background[Compression Exit] | Distinguish an early release attempt from an actual exit out of historical compression |
| **Development** | Is the extension persisting, interrupting or cooling? | Consecutive breach closes, five-session Bandwidth change, direction streak, re-entry | Describe continuation, interruption, or contraction using contemporaneous evidence |

The sequence is a **reading framework**, not a required or inevitably successful trading sequence. A release attempt can stall; a re-entry can occur while Bandwidth remains elevated. See [the bullish/bearish comparison](#bullish-bearish-and-potential-failed-release-comparison).

### Reading a standalone Bandwidth cell
(:small[[Bandwidth State](#bandwidth-state)] | :small[[1D Change](#bandwidth-change-1d)] | :small[[Combined examples](#reading-bandwidth-state-bandwidth-change-1-d-together)])

The standalone :blue-background[BB Bandwidth] number is the total band-to-band width as a percentage of the middle band. A displayed :gray-background[4.22] means the upper-to-lower distance is about :gray-background[4.22%] of the middle band's level.

A valid standalone Bandwidth row retains :gray-background[Signal: Neutral] and :gray-background[Score: 0]. **Both standalone Bandwidth and enhanced %B hovers now use the same labels**: :blue-background[Bandwidth State] (:gray-background[Very Narrow / Narrow / Typical / Wide / Very Wide]) and :blue-background[Bandwidth Change (1D)] (:gray-background[Expanding / Contracting / Stable]). Read **Value + State + 1D Change** together; neither changes the Signal. The [comparison table](#the-bollinger-measurements-at-a-glance) and [combined-reading examples](#reading-bandwidth-state-bandwidth-change-1-d-together) show how the fields complement one another.

For field-by-field interpretation, see [Understanding the enhanced Bollinger %B hover](#understanding-the-enhanced-bollinger-b-hover).

---

## Bollinger Bands / %B / Bandwidth — brief overview
(:small[[Back to top](#summary-bollinger-b-signals)])

Bollinger Bands create a moving price envelope around a middle reference line.

Each Bollinger setting has three bands:

```text
Upper Band
Middle Band
Lower Band
```

Conceptually:

```text
Middle Band = moving average of price

Upper Band = Middle Band + configured standard-deviation distance

Lower Band = Middle Band - configured standard-deviation distance
```

The distance between the upper and lower bands changes as price volatility changes:

- quieter price movement generally produces narrower bands;
- larger price swings generally produce wider bands.

The project currently uses three Bollinger settings:

```text
BB(10,1.5)  → short-term view
BB(20,2.0)  → medium-term / balanced view
BB(50,2.5)  → long-term view
```

For example:

```text
BB(20,2.0)

20  = middle-band lookback
2.0 = standard-deviation multiplier used to position
      the upper and lower bands around the middle band
```

The Bollinger family produces two separate heatmap outputs:

```text
%B
BB Bandwidth
```

They come from the same Bollinger Bands, but they answer **different questions**.

### '%B' — Where is price relative to the bands?
(:small[[Parent](#bollinger-bands-b-bandwidth-brief-overview)] |  :small[See: [101: %B (The Position/Overbought-Oversold Gauge)](#b-the-positionoverbought-oversold-gauge)]| :small[[The Bollinger measurements at a glance](#the-bollinger-measurements-at-a-glance)] | :small[Related:] :small[[Reading %B and Bandwidth together](#reading-b-and-bandwidth-together) | [Project %B rules: consolidated reference](#project-b-rules--consolidated-reference)])


Bollinger :blue-background[%B] converts the current price's location relative to the bands into a standardized position measure.

Conceptually:

```text
%B = (Price - Lower Band)
     --------------------
     (Upper Band - Lower Band)
```

The calculation is stored internally as a fraction, but the heatmaps multiply it by :gray-background[100] for readability.

So:

```text
Raw %B      Displayed %B

0.00   →       0
0.50   →      50
1.00   →     100
1.10   →     110
-0.10  →     -10
```

The displayed scale has several useful landmarks:

| Displayed %B | Physical meaning |
| --- | --- |
| :gray-background[< 0] | Price is below the lower band |
| :gray-background[0] | Price is at the lower band |
| :gray-background[50] | Price is at the middle band |
| :gray-background[100] | Price is at the upper band |
| :gray-background[> 100] | Price is above the upper band |

Unlike an oscillator that is permanently bounded between :gray-background[0] and :gray-background[100], :blue-background[%B] can legitimately move below :gray-background[0] or above :gray-background[100].

That is not an error. It means price has moved outside the Bollinger envelope.

### Bandwidth — how wide are the bands?
(:small[[Parent](#bollinger-bands-b-bandwidth-brief-overview) | See Also: [101: Bollinger Bandwidth (The Volatility Gauge)](#bollinger-bandwidth-the-volatility-gauge)])

**[Bollinger Bandwidth](#understanding-bollinger-bandwidth)** measures the total distance between the upper and lower bands relative to the middle band.

Conceptually:

```text
Bandwidth = (Upper Band - Lower Band)
            -------------------------
                  Middle Band
```

Like :blue-background[%B], the project stores Bandwidth internally as a fraction and multiplies it by :gray-background[100] for display.

For example:

```text
Raw Bandwidth     Displayed Bandwidth

0.0422       →          4.22
0.1800       →         18.00
```

- A larger Bandwidth means the Bollinger envelope is wider.
- A smaller Bandwidth means the envelope is narrower.

But **Bandwidth alone says nothing about whether price is bullish or bearish**.

That distinction is fundamental to how this project treats the Bollinger family.

### Value-added use

Price alone tells you:

> **“What is the stock trading at?”**

Bollinger-derived measures add two kinds of relative context.

:blue-background[%B] asks:

> **“Where is that price relative to its current Bollinger envelope (the 'extremes')?”**

Bandwidth asks:

> **“How wide is that envelope?”**

Both the standalone :blue-background[BB Bandwidth] hover and the enhanced :blue-background[%B] hover use the **same two named measurements**, while the %B hover additionally shows [multi-session development](#bandwidth-development-multi-session-context) and [band-breach history](#breach-status-and-compression-exit):
- **[Bandwidth State](#bandwidth-state)** — how unusual the current width is compared with the stock's own recent history.
- **[Bandwidth Change (1D)](#bandwidth-change-1d)** — whether the width is materially expanding, contracting, or stable relative to the preceding session.

See the [measurement comparison table](#the-bollinger-measurements-at-a-glance) for a single-page summary of all the fields.

This matters because the same :blue-background[%B] reading can occur under very different volatility conditions.

For example:

```text
%B = 95
```

means price is near the upper band.

But that alone does not tell you whether the bands are:

```text
very narrow and stable,
narrow but beginning to expand,
already very wide and expanding further,
or very wide but beginning to contract.
```

Bandwidth context adds that missing volatility information.

It does **not** change the :blue-background[%B] score.

### Use with
(:small[[Parent](#bollinger-bands-b-bandwidth-brief-overview)])

Bollinger :blue-background[%B] and Bandwidth are most useful when treated as pieces of a larger technical picture rather than as standalone forecasts.

- **SMA / EMA** — provide trend direction and help distinguish a Bollinger extreme occurring with or against the broader price trend.
- **ADX** — helps show whether a strong trend is present. This is useful because price can remain near an outer Bollinger Band during a persistent trend.
- **RSI / Stochastic / Williams %R / MFI** — provide independent evidence about momentum or range-position extremes.
- **ROC / MACD** — help show whether momentum is strengthening or weakening while price is near a Bollinger extreme.
- **CMF / OBV / volume measures** — add participation or buying/selling-pressure context.

None of these companion indicators is required by the Bollinger scoring rules.

They provide context; they do not silently become additional :blue-background[%B] rule conditions.

> **Tip:** Use independent trend, price-structure or volume evidence when assessing a possible breakout. Bandwidth does not measure traded volume, so neither a band breach nor a Bandwidth increase alone proves institutional participation or establishes a false breakout.
  

### Important distinction
(:small[[Parent](#bollinger-bands-b-bandwidth-brief-overview)])

The project deliberately separates **price-location semantics** from **volatility semantics**.

```text
%B
→ directional / exhaustion interpretation
→ Strong Buy / Buy / Neutral / Sell / Strong Sell
→ drives the heatmap score and color

BB Bandwidth
→ nondirectional volatility interpretation
→ canonical directional score remains Neutral / 0
→ volatility meaning is carried separately through Bandwidth State and Bandwidth Change (1D)
```

This prevents several common misreadings.

```text
High Bandwidth
≠ bearish

Low Bandwidth
≠ bullish

Expanding Bandwidth
≠ price rising

Contracting Bandwidth
≠ price falling
```

Likewise:

```text
High %B
≠ guaranteed immediate decline

Low %B
≠ guaranteed immediate rebound
```

The :blue-background[%B] score describes the **current degree of price stretch** under the project's contrarian model.

Bandwidth describes the **current volatility environment**.

---

## The Bollinger measurements at a glance
(:small[[Back to top](#summary-bollinger-b-signals)] | :small[[State definitions](#bandwidth-state)] | :small[[1D Change](#bandwidth-change-1d)] | :small[[Enhanced hover field map](#enhanced-b-hover-field-map)])

The original three questions still hold: **where is price; how unusual is band width; what is band width doing today?** The IVE enhancement adds recent development, band-breach history and a conditional interpretation of their combination.

| | [%B](#b--where-is-price-relative-to-the-bands) / [Signal](#summary-bollinger-b-signals) | [Bandwidth State](#bandwidth-state) | [Bandwidth Change (1D)](#bandwidth-change-1d) | [Bandwidth Development](#bandwidth-development-multi-session-context) | [Breach Status](#breach-status-and-compression-exit) | [Bottom-line](#how-the-bottom-line-chooses-what-to-explain) |
| --- | --- | --- | --- | --- | --- | --- |
| **Question answered** | <li>Where is price relative to the bands? <li> Where are we?| <li>How wide are bands compared with their recent history? <li>Is a big move about to happen? | <li>Did width expand/contract materially since yesterday? <li>What just happened?| <li>Has width changed materially across several sessions? <li>Is bandwidth emerging from compression, expanding persistently, leveling off, or contracting? | Has price just left, stayed beyond, or re-entered a band? | What is the dominant combination telling us? |
| **What it measures** | Normalized current price position and project contrarian score | Historical relative level of Bandwidth | One-session relative Bandwidth movement | Five-session absolute and relative change; qualifying 1D streak; Compression Exit | Current outside/inside state compared with preceding observations | Conditional synthesis, not a new score |
| **Comparison** | Price vs current lower/upper band | Current Bandwidth vs historical 60/120 observations | Current vs previous Bandwidth | Current vs five sessions ago; consecutive 1D classifications | Current and earlier band positions | Validated evidence across the preceding columns |
| **Outputs** | :gray-background[Strong Buy / Buy / Neutral / Sell / Strong Sell] | :gray-background[Very Narrow / Narrow / Typical / Wide / Very Wide] | :gray-background[Expanding / Contracting / Stable] | Five-session points and percentage, directional streak and event | Fresh/Continuing Breach, Re-entry, No Active Breach, or unavailable/onset unknown | A concise condition-specific interpretation, or no statement |

**Two independent dimensions:** :blue-background[Bandwidth State] is a historical level, while :blue-background[Bandwidth Change (1D)] is the latest movement. The envelope can be :gray-background[Very Narrow + Expanding] or :gray-background[Very Wide + Contracting] without contradiction.

**Historical reference window is not the Bollinger calculation window.** For example, the MT bands use :gray-background[20 price observations], but the Bandwidth percentile compares its resulting widths with :gray-background[120 historical Bandwidth observations] (about six trading months). See the [reference-window table](#historical-reference-window-by-horizon).

---

## BB %B Rule Translation
(:small[[Back to top](#summary-bollinger-b-signals)])

The project uses :blue-background[%B] as a **current-location contrarian / exhaustion measure**. The signal depends on where price is now relative to the Bollinger envelope; reversal, crossback, persistence, Bandwidth confirmation, and other indicators are not required by the score. The balanced :gray-background[BB(20,2.0)] setting is used below as the detailed example.

### Strong Buy (%B)

**Rule:** :blue-background[%B < -10] (:gray-background[pct_b < -0.10] internally)

Price is materially below the lower :gray-background[BB(20,2.0)] band. The project treats this as unusually severe downside stretch and assigns **Strong Buy (+2)**. It describes current exhaustion; it does not mean a rebound has already begun.

**Bottom-line:** Exceptional downside extension relative to the MT Bollinger envelope.

### Buy (%B)

**Rule:** :blue-background[-10 <= %B < 10]

Price is near the lower band or modestly below it. This is the project's lower-edge exhaustion zone and receives **Buy (+1)**. An actual band breach is not required.

**Bottom-line:** Price is stretched toward the low side of the MT envelope, but not enough for Strong Buy.

### Neutral (%B)

**Rule:** :blue-background[10 <= %B <= 90]

Price is comfortably away from either exhaustion edge and receives **Neutral (0)**. Neutral does not mean price is exactly at the middle band; :gray-background[%B = 30] and :gray-background[%B = 75] are both Neutral because neither is close enough to an outer edge.

**Bottom-line:** No meaningful Bollinger-edge exhaustion signal.

### Sell (%B)

**Rule:** :blue-background[90 < %B <= 110]

Price is near the upper band or modestly above it. This is the project's upper-edge exhaustion zone and receives **Sell (-1)**. Price can remain near an upper band during a strong trend, so this is not a confirmed reversal call.

**Bottom-line:** Price is stretched toward the high side of the MT envelope, but not enough for Strong Sell.

### Strong Sell (%B)

**Rule:** :blue-background[%B > 110] (:gray-background[pct_b > 1.10] internally)

Price is materially above the upper :gray-background[BB(20,2.0)] band. The project treats this as unusually severe upside stretch and assigns **Strong Sell (-2)**. It identifies exceptional extension, not a guaranteed immediate decline.

**Bottom-line:** Exceptional upside extension relative to the MT Bollinger envelope.

## Industry-standard baseline

Classic Bollinger interpretation treats the bands as relative definitions of high and low, [%B](#b-where-is-price-relative-to-the-bands) as price location relative to the bands, and Bandwidth as normalized band width. A common reference construction is a 20-period middle band with upper/lower bands two standard deviations away.

The physical :blue-background[%B] landmarks are :gray-background[0] = lower band, :gray-background[50] = middle band, and :gray-background[100] = upper band; values outside :gray-background[0–100] mean price is outside the envelope. These measurements do **not** inherently prescribe a contrarian trading rule: high :blue-background[%B] can represent strength, continuation, overextension, or reversal context depending on the method.

Bandwidth likewise describes volatility magnitude: narrow bands indicate more compressed volatility and wide bands more expanded volatility. It does not inherently say Buy, Sell, bullish, or bearish. A band touch or breach is therefore not automatically a standalone trading signal.

## How the TA Rule Engine extends the classic baseline

The project keeps the classic physical meaning of :blue-background[%B] and Bandwidth but adds explicit application semantics:

- **[%B](#b-where-is-price-relative-to-the-bands):** current-location contrarian / exhaustion scoring. Lower-edge stretch maps to Buy-side exhaustion; upper-edge stretch maps to Sell-side exhaustion. This is a project choice, not a universal Bollinger rule.
- **[BB Bandwidth](#understanding-bollinger-bandwidth):** retains its directional-neutral score (:gray-background[Neutral / 0]) and reports **[Bandwidth State](#bandwidth-state)** and **[Bandwidth Change (1D)](#bandwidth-change-1d)** with the same user-facing labels as the %B hover. Their [percentile cutoffs](#bandwidth-state-calibration-by-horizon), [reference windows](#historical-reference-window-by-horizon) and [Stable tolerances](#bandwidth-change-1d-thresholds-by-horizon) are project-specific calibrations.

## Why Strong thresholds differ by horizon

A band touch or breach is not equally unusual across all three Bollinger settings. [BB(10,1.5)](#bb1015-b-rules-interpretation) is faster and tighter, so price crosses its bands more often; [BB(50,2.5)](#bb5025-b-rules-interpretation) is slower and wider, so an actual band breach is already comparatively unusual.

The project therefore keeps the ordinary exhaustion boundaries common at :gray-background[%B < 10] and :gray-background[%B > 90], while calibrating Strong thresholds by horizon:

```text
ST  BB(10,1.5):  Strong Buy < -20 | Strong Sell > 120
MT  BB(20,2.0):  Strong Buy < -10 | Strong Sell > 110
LT  BB(50,2.5):  Strong Buy <   0 | Strong Sell > 100
```

These are project-specific calibrations, not universal Bollinger rules.

## Comparison of the three Bollinger settings
(:small[[Back to top](#summary-bollinger-b-signals)])

The project uses three Bollinger configurations to capture different horizons.

| Setting | Horizon | Responsiveness | Band characteristics | Ordinary exhaustion zone | Strong Buy / Sell | Main trade-off |
| --- | --- | --- | --- | --- | --- | --- |
| [BB(10,1.5)](#bb1015-b-rules-interpretation) | Short term | Fastest | Short lookback and tightest band multiplier; reacts quickly and is breached more often. | :gray-background[<10] / :gray-background[>90] | :gray-background[<-20] / :gray-background[>120] | Most responsive, but ordinary band breaches are less exceptional. |
| [BB(20,2.0)](#bb2020-b-rules-interpretation) | Medium term | Balanced | Classic-style balanced configuration. | :gray-background[<10] / :gray-background[>90] | :gray-background[<-10] / :gray-background[>110] | Good balance between responsiveness and selectivity. |
| [BB(50,2.5)](#bb5025-b-rules-interpretation) | Long term | Slowest | Longer lookback and widest multiplier; responds more slowly and is harder to breach. | :gray-background[<10] / :gray-background[>90] | :gray-background[<0] / :gray-background[>100] | Most selective; actual band breaches are already unusual. |

### Practical selection guide

- **BB(10,1.5) — ST:** fastest and most sensitive; useful for short-term stretch.
- **BB(20,2.0) — MT:** balanced/default view; closest to the classic 20/2 reference.
- **BB(50,2.5) — LT:** slowest and most selective; useful for structural stretch.

Treat the three settings as **different horizon lenses, not three votes**. A stock can be Neutral on ST while Sell or Strong Sell on LT because each envelope measures relative location over a different horizon.

## BB(10,1.5) %B Rules interpretation

| Source | Signal | Rule logic | What’s happening | Answers the question | Bottom-line |
| --- | --- | --- | --- | --- | --- |
| BB %B(ST) | Strong Buy | :gray-background[%B < -20] | Price is deeply below the tight short-term lower band. | Is the current downside stretch exceptional even for the highly responsive ST envelope? | Exceptional ST downside exhaustion. |
| BB %B(ST) | Buy | :gray-background[-20 <= %B < 10] | Price is close to or moderately below the lower ST band. | Is price stretched toward the lower short-term edge? | ST lower-edge exhaustion. |
| BB %B(ST) | Neutral | :gray-background[10 <= %B <= 90] | Price is away from both short-term exhaustion zones. | Is price sufficiently inside the ST envelope to avoid an edge signal? | No ST exhaustion signal. |
| BB %B(ST) | Sell | :gray-background[90 < %B <= 120] | Price is close to or moderately above the upper ST band. | Is price stretched toward the upper short-term edge? | ST upper-edge exhaustion. |
| BB %B(ST) | Strong Sell | :gray-background[%B > 120] | Price is deeply above the tight short-term upper band. | Is the current upside stretch exceptional even for the responsive ST envelope? | Exceptional ST upside exhaustion. |

Because :gray-background[BB(10,1.5)] is the fastest and tightest configuration, excursions outside its bands are relatively common. Therefore :gray-background[%B > 100] alone is **not** Strong Sell, and :gray-background[%B < 0] alone is **not** Strong Buy. The stronger :gray-background[-20 / 120] boundaries keep Strong states selective.

---

## BB(20,2.0) %B Rules interpretation

| Source | Signal | Rule logic | What’s happening | Answers the question | Bottom-line |
| --- | --- | --- | --- | --- | --- |
| BB %B | [Strong Buy](#strong-buy-b) | :gray-background[%B < -10] | Price is materially below the medium-term lower band. | Is downside stretch unusually severe for the balanced envelope? | Exceptional MT downside exhaustion. |
| BB %B | [Buy](#buy-b) | :gray-background[-10 <= %B < 10] | Price is near or modestly below the lower band. | Is price stretched toward the medium-term lower edge? | MT lower-edge exhaustion. |
| BB %B | [Neutral](#neutral-b) | :gray-background[10 <= %B <= 90] | Price is comfortably away from either MT edge. | Is price inside the non-exhaustion portion of the envelope? | No MT exhaustion signal. |
| BB %B | [Sell](#sell-b) | :gray-background[90 < %B <= 110] | Price is near or modestly above the upper band. | Is price stretched toward the medium-term upper edge? | MT upper-edge exhaustion. |
| BB %B | [Strong Sell](#strong-sell-b) | :gray-background[%B > 110] | Price is materially above the medium-term upper band. | Is upside stretch unusually severe for the balanced envelope? | Exceptional MT upside exhaustion. |

:gray-background[BB(20,2.0)] is the project's balanced Bollinger configuration. Its Strong thresholds sit between the ST and LT calibrations:

```text
ST  → -20 / 120
MT  → -10 / 110
LT  →   0 / 100
```

---

## BB(50,2.5) %B Rules interpretation

| Source | Signal | Rule logic | What’s happening | Answers the question | Bottom-line |
| --- | --- | --- | --- | --- | --- |
| BB %B(LT) | Strong Buy | :gray-background[%B < 0] | Price is below the wide long-term lower band. | Has price actually breached an already-selective LT lower envelope? | Exceptional LT downside exhaustion. |
| BB %B(LT) | Buy | :gray-background[0 <= %B < 10] | Price is inside the envelope but very near the lower band. | Is price stretched toward the LT lower edge without an actual breach? | LT lower-edge exhaustion. |
| BB %B(LT) | Neutral | :gray-background[10 <= %B <= 90] | Price is away from both LT extremes. | Is price inside the central long-term envelope? | No LT exhaustion signal. |
| BB %B(LT) | Sell | :gray-background[90 < %B <= 100] | Price is inside the envelope but very near the upper band. | Is price stretched toward the LT upper edge without an actual breach? | LT upper-edge exhaustion. |
| BB %B(LT) | Strong Sell | :gray-background[%B > 100] | Price is above the wide long-term upper band. | Has price actually breached an already-selective LT upper envelope? | Exceptional LT upside exhaustion. |

:gray-background[BB(50,2.5)] is both slower and wider. An actual band breach is sufficiently uncommon that the breach itself marks the Strong boundary.

---

## Project %B rules — consolidated reference
(:small[[Back to top](#summary-bollinger-b-signals)])

| Horizon | Strong Buy | Buy | Neutral | Sell | Strong Sell |
| --- | --- | --- | --- | --- | --- |
| [ST BB(10,1.5)](#bb1015-b-rules-interpretation) | :gray-background[< -20] | :gray-background[-20 to <10] | :gray-background[10 to 90] | :gray-background[>90 to 120] | :gray-background[>120] |
| [MT BB(20,2.0)](#bb2020-b-rules-interpretation) | :gray-background[< -10] | :gray-background[-10 to <10] | :gray-background[10 to 90] | :gray-background[>90 to 110] | :gray-background[>110] |
| [LT BB(50,2.5)](#bb5025-b-rules-interpretation) | :gray-background[<0] | :gray-background[0 to <10] | :gray-background[10 to 90] | :gray-background[>90 to 100] | :gray-background[>100] |

### Scoring

```text
Strong Buy  → +2
Buy         → +1
Neutral     →  0
Sell        → -1
Strong Sell → -2
```

### Boundary handling

The exact edge behavior is intentional.

```text
ST %B = -20
→ Buy
not Strong Buy

ST %B = 120
→ Sell
not Strong Sell
```

```text
MT %B = -10
→ Buy

MT %B = 110
→ Sell
```

```text
LT %B = 0
→ Buy

LT %B = 100
→ Sell
```

And across all three settings:

```text
%B = 10
→ Neutral

%B = 90
→ Neutral
```

This keeps the five states mutually exclusive.

### Missing / warmup behavior

If :blue-background[%B] is not yet numerically initialized:

```text
%B = missing
```

then:

```text
Signal = missing
Score  = missing
```

The project does **not** convert unavailable Bollinger observations into synthetic Neutral readings.

### What the '%B' score uses

The score uses **current :blue-background[%B] location only**.
Bandwidth value, Bandwidth State, Bandwidth Change (1D), reversal/crossback confirmation, persistence, and other indicators remain context rather than hidden scoring conditions.

## Understanding Bollinger Bandwidth
(:small[[Back to top](#summary-bollinger-b-signals) | See: [101: Bollinger Bandwidth (The Volatility Gauge)](#bollinger-bandwidth-the-volatility-gauge) & [Bandwidth: How wide are the bands?](#bandwidth-how-wide-are-the-bands)]| :small[[Bandwidth State](#bandwidth-state)] | :small[[1D Change](#bandwidth-change-1d)] | :small[[Combined examples](#reading-bandwidth-state-bandwidth-change-1-d-together)])

One important consequence of :blue-background[%B] being a location measure is that the same :blue-background[%B] can occur in very different volatility environments. :gray-background[%B = 95] always means price is near the upper band, but the bands themselves may be exceptionally narrow, ordinary, or exceptionally wide.
- Bandwidth provides that missing '**volatility context**'.

Bollinger Bandwidth answers a different question:
- ***How wide is the Bollinger envelope?***

Its conceptual formula is:

```text
Bandwidth = (Upper Band - Lower Band)
            -------------------------
                  Middle Band
```

The project stores Bandwidth as a fraction and displays it as :gray-background[×100].

For example:

```text
Raw BB_BW = 0.0472
Displayed = 4.72
```

means:

> The total distance from the lower band to the upper band is approximately 4.72% of the middle-band level.

### Why the Bandwidth number alone is not enough

A Bandwidth of :gray-background[5.00] might be unusually narrow for one stock and completely ordinary for another.

Likewise, :gray-background[15.00] might be extremely wide for one security but routine for a more volatile security.

Therefore the project does **not** use universal absolute Bandwidth cutoffs. Instead, it asks:

> **Where does the current Bandwidth rank relative to this instrument's own recent Bandwidth history?**

That produces the project's [Bandwidth State](#bandwidth-state).

This is why Bandwidth is treated as a **relative-to-own-history volatility measure** rather than a universal cross-security volatility scale.

### Why BB_BW remains Neutral / 0

Bandwidth measures **volatility magnitude**.

It does not tell us whether price is moving up or down.

Therefore:

```text
Wide bands
≠ bearish

Narrow bands
≠ bullish

Bands expanding
≠ price rising

Bands contracting
≠ price falling
```

A valid BB_BW observation therefore retains:

```text
Signal: Neutral
Score: 0
```

Its useful semantic outputs are carried separately as:

```text
Bandwidth State
Bandwidth Change (1D)
```

---

## Bandwidth State
(:small[[Back to top](#summary-bollinger-b-signals)] | :small[[Reference windows](#historical-reference-window-by-horizon)] | :small[[1D Change](#bandwidth-change-1d)] | :small[[Combined reading](#reading-bandwidth-state-bandwidth-change-1-d-together)])

**Bandwidth State** describes:
- ***How unusual is the current [Bandwidth](#understanding-bollinger-bandwidth) compared with this stock's own recent Bandwidth history?***

The project uses five states:

```text
Very Narrow
Narrow
Typical
Wide
Very Wide
```

### Beginner interpretation (Bandwidth State)

| State | Beginner meaning |
| --- | --- |
| **Very Narrow** | Bands are exceptionally narrow compared with this stock’s recent history. |
| **Narrow** | Bands are narrower than usual. |
| **Typical** | Band width is around its typical historical range. |
| **Wide** | Bands are wider than usual. |
| **Very Wide** | Bands are exceptionally wide compared with recent history. |

The key phrase is **compared with this stock's recent history**.

:gray-background[Very Wide] does not mean “this stock has wider bands than every other stock.” It means “this stock's current bands are exceptionally wide relative to the Bandwidth levels it has recently experienced.”

### Consistent Bandwidth State labels across the heatmaps
(:small[[Parent](#bandwidth-state)] | :small[[Hover field map](#enhanced-b-hover-field-map)] | :small[[Visual legend](#reading-the-new-display-value-customizations)])

**Standalone Bandwidth and enhanced %B use exactly the same five visible States:** :gray-background[Very Narrow], :gray-background[Narrow], :gray-background[Typical], :gray-background[Wide] and :gray-background[Very Wide]. Both report :blue-background[Bandwidth Change (1D)] as :gray-background[Expanding], :gray-background[Contracting] or :gray-background[Stable]. The numeric classifications, reference windows and thresholds remain unchanged; only the standalone hover's legacy presentation labels have been standardized.

**Visual exception:** Only :gray-background[Very Narrow] makes the **%B cell number purple**; the slightly less exceptional :gray-background[Narrow] does not. The separate black ◆ denotes a [Compression Exit](#compression-exit-a-bandwidth-state-event), not a buy/sell signal. These overlays apply to %B heatmap cells, not standalone Bandwidth cells. For exact cutoffs, consult the [State calibration table](#bandwidth-state-calibration-by-horizon).

### How the percentile classification works

The project calculates the current Bandwidth's historical percentile within the configured reference window.

Conceptually:

```text
Current Bandwidth
        ↓
Compare with the instrument's own recent Bandwidth observations
        ↓
Determine current historical percentile
        ↓
Map percentile into one of five Bandwidth States
```

For example, a current percentile at the :gray-background[97th percentile] means current Bandwidth is wider than approximately 97% of the Bandwidth observations in the relevant reference history. That qualifies as :gray-background[Very Wide] under the MT/LT calibration.

### Historical reference window by horizon
(:small[[Parent](#bandwidth-state)])

| Horizon | Bollinger configuration | Historical reference | Approximate duration |
| --- | --- | --- | --- |
| Short term | :gray-background[BB(10,1.5)] | :gray-background[60 trading Bandwidth observations] | About 3 trading months |
| Medium term | :gray-background[BB(20,2.0)] | :gray-background[120 trading Bandwidth observations] | About 6 trading months |
| Long term | :gray-background[BB(50,2.5)] | :gray-background[120 trading Bandwidth observations] | About 6 trading months |

The historical window is used to rank **the current Bandwidth**, not to calculate the base Bollinger bands themselves. On daily data these are trading-session counts, not calendar-day counts. A percentile rank of :gray-background[2.1st] means current Bandwidth falls within roughly the lowest :gray-background[2–3 observations per 100] in the historical reference; in a 120-observation sample, this is approximately :gray-background[2–3 observations] (subject to the calculation's ranking convention).

### Bandwidth State calibration by horizon

| Horizon | Setting | Reference history | Very Narrow | Narrow | Typical | Wide | Very Wide |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| ST | BB(10,1.5) | 60 observations | <10th | 10th–<25th | 25th–75th | >75th–90th | >90th |
| MT | BB(20,2.0) | 120 observations | <5th | 5th–<15th | 15th–85th | >85th–95th | >95th |
| LT | BB(50,2.5) | 120 observations | <5th | 5th–<15th | 15th–85th | >85th–95th | >95th |

ST uses a shorter, more responsive reference history; MT/LT use a longer, more stable one. The outer percentile boundaries are also more selective for MT/LT. These are project-specific production calibrations, not textbook Bollinger settings.

### Warmup behavior

Bandwidth State requires enough initialized Bandwidth history to fill its historical reference window.

Conceptually:

```text
Bollinger Bands initialize
        ↓
Bandwidth initializes
        ↓
Enough Bandwidth history accumulates
        ↓
Historical percentile becomes available
        ↓
Bandwidth State becomes available
```

Before that reference history is available:

```text
Bandwidth State = missing
```

The project does not manufacture a :gray-background[Typical] state for an observation that lacks enough historical context.

---

## Bandwidth Change (1D)
(:small[[Back to top](#summary-bollinger-b-signals)] | :small[[State](#bandwidth-state)] | :small[[Change thresholds](#bandwidth-change-1d-thresholds-by-horizon)] | :small[[Development](#bandwidth-development-multi-session-context)])

**Bandwidth Change (1D)** answers:
- ***Is the Bollinger envelope getting wider, getting narrower, or changing too little to count as material?***

The possible outputs are:

```text
Expanding
Contracting
Stable
```

### Beginner interpretation (Bandwidth Change 1D)

| Direction | Beginner meaning |
| --- | --- |
| **Expanding** | Bands are getting wider. |
| **Contracting** | Bands are getting narrower. |
| **Stable** | Band width has not changed enough to count as meaningfully wider or narrower. |

This is separate from [Bandwidth State](#bandwidth-state).

A stock can have :gray-background[Very Narrow + Expanding] because its bands can still be exceptionally narrow **while beginning to widen**.

Likewise, :gray-background[Very Wide + Contracting] means bands can still be exceptionally wide **while beginning to narrow**.

### How Bandwidth Change (1D) is calculated

The project compares current Bandwidth with the prior observation:

```text
Relative Bandwidth change
=
Current Bandwidth / Prior Bandwidth - 1
```

The classification then applies a horizon-specific tolerance:

```text
Change > +tolerance
→ Expanding

Change < -tolerance
→ Contracting

Otherwise
→ Stable
```

Equality at either tolerance boundary is intentionally classified as :gray-background[Stable].

### Bandwidth Change (1D) thresholds by horizon

| Horizon | Expanding | Stable (inclusive) | Contracting |
| --- | --- | --- | --- |
| Short term :gray-background[BB(10,1.5)] | Above :gray-background[+3.0%] | :gray-background[−3.0% through +3.0%] | Below :gray-background[−3.0%] |
| Medium term :gray-background[BB(20,2.0)] | Above :gray-background[+2.0%] | :gray-background[−2.0% through +2.0%] | Below :gray-background[−2.0%] |
| Long term :gray-background[BB(50,2.5)] | Above :gray-background[+0.5%] | :gray-background[−0.5% through +0.5%] | Below :gray-background[−0.5%] |

Daily Bandwidth movement naturally becomes smaller as the Bollinger horizon slows, so each horizon uses a different tolerance. A change outside the tolerance is Expanding or Contracting; a change inside it—or exactly on either boundary—is Stable.

Example for ST: :gray-background[+4.2%] → [Expanding](#beginner-interpretation-bandwidth-change-1d), :gray-background[-4.0%] → Contracting, :gray-background[+1.8%] or exactly :gray-background[±3.0%] → Stable.

### One-session change warmup

Bandwidth Change (1D) requires:

```text
current Bandwidth
+
prior Bandwidth
```

If either observation is unavailable:

```text
Bandwidth Change (1D) = missing
```

The system does not label the first initialized observation as [Stable](#beginner-interpretation-bandwidth-change-1d) merely because no comparison exists.

---

## Bandwidth Development: multi-session context
(:small[[Back to top](#summary-bollinger-b-signals)] | :small[[1D Change](#bandwidth-change-1d)] | :small[[Breach events](#breach-status-and-compression-exit)] | :small[[Pattern reference](#bollinger-pattern-reference-complete-interpretations)])

The enhanced :blue-background[%B] hover reports three kinds of Bandwidth history together: the **five-session change**, the **consecutive qualified 1D direction streak**, and (when it occurs) a **Compression Exit** event. These are descriptive measurements, not new Buy/Sell scoring clauses.

### Five-session Bandwidth change

| Component | Calculation | Example |
| --- | --- | --- |
| :blue-background[Absolute change] | Current displayed Bandwidth − displayed Bandwidth five trading sessions earlier | :gray-background[13.82 − 5.69 = +8.13 points] |
| :blue-background[Relative change] | (Current Bandwidth ÷ five-session-prior Bandwidth − 1) × 100 | :gray-background[+143.0%] |
| :blue-background[Streak] | Count consecutive days ending today that qualify as Expanding or Contracting under the horizon's 1D tolerance | :gray-background[6 consecutive Expanding sessions] |

These are **five trading-session comparisons**, not five calendar days. The history may include observations before the earliest visible heatmap date. An isolated stable day interrupts an Expanding/Contracting streak, even when the five-session net change remains large. A displayed magnitude such as :gray-background[+143.0%] is a change in *Bandwidth*, not a :gray-background[143%] price move.

For clarity, a rise from Bandwidth :gray-background[5.69] to :gray-background[13.82] adds about :gray-background[8.13 Bandwidth points]. Relative to the starting width, that is about :gray-background[143%] additional width; the envelope is now approximately :gray-background[2.43×] as wide.

### Interpretation filters versus measurement definitions

| Context qualification | Requirement | Role |
| --- | --- | --- |
| Material recent widening | Five-session relative change :gray-background[≥ +20%] **plus** qualifying current :gray-background[Expanding] and at least :gray-background[2] consecutive Expanding sessions | Helps identify sustained expansion **in some** Bottom-line branches |
| Material recent narrowing | Five-session relative change :gray-background[≤ −20%] **plus** qualifying current :gray-background[Contracting] and at least :gray-background[2] consecutive Contracting sessions | Helps identify sustained cooling **in some** Bottom-line branches |
| Historically very wide after growth | :gray-background[Very Wide] State; five-session change :gray-background[≥ +20%]; today :gray-background[Stable]; :gray-background[No Active Breach] | A lower-priority eligible Bottom-line even when today's widening pauses |
| Compression Exit | Previous State historically compressed; current State no longer compressed; current day :gray-background[Expanding] | A separately identified transition; **does not require** the ±20% filter |

**Important:** The :gray-background[±20%] thresholds are approved **context materiality filters**, not universal Bollinger trading constants and not standalone proof of a price breakout. For example, a five-session :gray-background[+40.9%] increase can occur while the current State remains :gray-background[Narrow], as GOOGL demonstrated on September 15. Historical State takes precedence over interpreting percentage change in isolation.

### Streak exactness and missing history

A streak is meaningful only when the underlying preceding 1D classifications are available. If history is insufficient or the streak's starting point is not established, the hover must not manufacture an exact count. The same principle applies to unavailable five-session comparators. Missing evidence is :gray-background[Unavailable], **not** :gray-background[Stable], :gray-background[0%] or a presumed completed streak.

---

## Breach Status and Compression Exit
(:small[[Back to top](#summary-bollinger-b-signals)] | :small[[1D Change](#bandwidth-change-1d)] | :small[[Pattern reference](#bollinger-pattern-reference-complete-interpretations)] | :small[[GOOGL sequence](#verified-bollinger-examples)])

### Breach Status: price versus the bands

A **band breach** is defined by physical position, not by the project's Strong Buy/Sell cutoff. Displayed :gray-background[%B < 0] means the closing price is **below** the lower band; :gray-background[%B > 100] means **above** the upper band. An ordinary Buy/Sell can exist without any actual breach.

| Hover status | Exact type of event | Plain-language reading |
| --- | --- | --- |
| :gray-background[Fresh Upper Breach] | Current price is above the upper band and the immediately preceding observation was not above | Price newly closed beyond the upper band |
| :gray-background[Fresh Lower Breach] | Current price is below the lower band and the immediately preceding observation was not below | Price newly closed beyond the lower band |
| :gray-background[Continuing Upper Breach] | Two or more consecutive closing observations above the upper band, with available predecessor history | Price is maintaining an upper-band extension |
| :gray-background[Continuing Lower Breach] | Two or more consecutive closing observations below the lower band, with available predecessor history | Price is maintaining a lower-band extension |
| :gray-background[Upper-Band Re-entry] | Price was above the upper band and has now returned inside | The previous upper-side extension was interrupted |
| :gray-background[Lower-Band Re-entry] | Price was below the lower band and has now returned inside | The previous lower-side extension was interrupted |
| :gray-background[No Active Breach] | Current price is inside/on the envelope with sufficient history and no current re-entry event | No currently qualifying outside-band extension |
| :gray-background[Outside Lower Band (Onset Unknown)] or :gray-background[Outside Upper Band (Onset Unknown)] | Price is currently outside a band, but the beginning of the sequence is not known reliably | The side is known; the event cannot safely be called Fresh or Continuing |
| :gray-background[Transition Unavailable] / :gray-background[Unavailable] | A required preceding observation or status is missing | Do not infer a re-entry or No Active Breach from missing context |

A :gray-background[Continuing] label may include the exact count of consecutive closes when the full sequence is known. An exit from one side directly to the opposite side is evaluated from the actual sequence; it is not automatically called an inside-band re-entry. Event timing uses the **current closing observation** and available full-history predecessors, not only the first visible date.

### Compression Exit: a Bandwidth-state event

The event requires **all three** conditions on the current session:

1. The immediately preceding historical Bandwidth State was :gray-background[Very Narrow] or :gray-background[Narrow] (enhanced display: :gray-background[Very Narrow] or :gray-background[Narrow]).
2. The current historical State is :gray-background[Typical], :gray-background[Wide] or :gray-background[Very Wide] (display: :gray-background[Typical], :gray-background[Wide] or :gray-background[Very Wide]).
3. Today's :blue-background[Bandwidth Change (1D)] is :gray-background[Expanding] under the horizon-specific tolerance.

The **black ◆** appears on this event date only. An earlier :gray-background[Fresh Upper/Lower Breach] can happen while Bandwidth is still compressed; that is an **emerging release attempt**, *not* yet a qualifying Compression Exit. Conversely, a Compression Exit can occur while price remains inside the bands. The event by itself says nothing about the direction of price or a break of separately measured consolidation support/resistance.

**GOOGL example:** On October 21 (MT), price newly closed below the lower band while State remained :gray-background[Narrow]; October 22 was the actual Compression Exit to :gray-background[Typical] while a lower-band breach continued. See [the verified sequence](#verified-bollinger-examples).

---

## Reading Bandwidth State + Bandwidth Change (1D) together
(:small[[Back to top](#summary-bollinger-b-signals)] | :small[[State table](#bandwidth-state-calibration-by-horizon)] | :small[[1D thresholds](#bandwidth-change-1d-thresholds-by-horizon)] | :small[[Detailed patterns](#bollinger-pattern-reference-complete-interpretations)] | :small[[Reading %B and Bandwidth together](#reading-b-and-bandwidth-together)])

This is where the two Bandwidth descriptors become substantially more useful.

A simple way to remember the distinction is:

```text
Bandwidth State
= Where is Bandwidth relative to its recent history?

Bandwidth Change (1D)
= What is Bandwidth doing right now?
```

Or, even more simply:

```text
Bandwidth State       = historical width regime
Bandwidth Change (1D) = current session movement
```

Neither replaces the other.

### Example 1 — Very Narrow + Stable

```text
Bandwidth State: Very Narrow
Bandwidth Change (1D): Stable
```

> **Bands are extremely narrow and staying that way.**

Interpretation:

- current volatility is unusually compressed;
- there is not yet enough widening or narrowing to classify the envelope as moving materially.

This identifies a very quiet volatility regime. It does **not** predict whether the eventual price move will be upward or downward.

### Example 2 — Narrow + Expanding

```text
Bandwidth State: Narrow
Bandwidth Change (1D): Expanding
```

> **Bands are still narrow, but volatility is beginning to increase.**

Interpretation:

- Bandwidth remains below its normal historical range;
- the envelope is now widening enough to register an increase.

### Example 3 — Typical + Contracting

```text
Bandwidth State: Typical
Bandwidth Change (1D): Contracting
```

> **Bandwidth is still around normal, but it is narrowing.**

Interpretation:

- current Bandwidth has not yet moved into the project's Narrow zone;
- nevertheless, recent movement is toward narrower bands.

If contraction continues, a later observation may eventually transition from :gray-background[Typical] → :gray-background[Narrow] → :gray-background[Very Narrow], but that transition is not assumed in advance.

### Example 4 — Wide + Expanding

```text
Bandwidth State: Wide
Bandwidth Change (1D): Expanding
```

> **Bands are already wider than usual and are getting wider still.**

Interpretation:

- volatility is already elevated relative to recent history;
- the envelope is widening further.

:gray-background[Expanding] does not tell us whether price itself is moving higher or lower. It tells us that the **magnitude of the Bollinger envelope is increasing**.

### Example 5 — Very Wide + Contracting

```text
Bandwidth State: Very Wide
Bandwidth Change (1D): Contracting
```

> **Bands remain extremely wide, but volatility is beginning to cool.**

Interpretation:

- Bandwidth remains at an exceptional historical level;
- the latest movement is toward a narrower envelope.

A useful distinction is:

```text
Contracting
≠ Narrow
```

The bands can be contracting while still being extremely wide.

### Additional State + Change combinations

| State | Direction | Beginner interpretation |
| --- | --- | --- |
| Very Narrow | Expanding | Bands are exceptionally narrow, but beginning to widen. |
| Very Narrow | Contracting | Bands are already exceptionally narrow and are narrowing further. |
| Narrow | Stable | Bands are narrower than usual and little changed. |
| Narrow | Contracting | Bands are narrower than usual and becoming narrower still. |
| Typical | Expanding | Band width is around normal but is beginning to widen. |
| Typical | Stable | Band width is around its normal historical range and little changed. |
| Wide | Stable | Bands are wider than usual but are not changing materially. |
| Wide | Contracting | Bands are wider than usual but beginning to narrow. |
| Very Wide | Expanding | Bands are exceptionally wide and widening further. |
| Very Wide | Stable | Bands are exceptionally wide and remaining that way. |

These combinations describe **volatility behavior only**. They do not create additional Buy/Sell scores.

### Why State and Change can appear to disagree

A common beginner question is:

> “How can Bandwidth be :gray-background[Very Wide] and :gray-background[Contracting] at the same time?”

There is no contradiction.

Consider Bandwidth moving like this:

```text
18.0
17.2
16.3
```

Suppose recent historical Bandwidth is normally much lower.

Even after falling from :gray-background[18.0 → 16.3], the current :gray-background[16.3] may still rank above the 95th percentile of recent history.

Therefore:

```text
Bandwidth State: Very Wide
```

because the **level is still extremely high**.

At the same time:

```text
Bandwidth Change (1D): Contracting
```

because the **latest movement is downward**.

The two fields use different frames of reference:

```text
Bandwidth State
→ level relative to history

Bandwidth Change (1D)
→ current change relative to prior observation
```

This distinction is central to reading the Bandwidth model correctly.

---

## Understanding the enhanced Bollinger %B hover
(:small[[Back to top](#summary-bollinger-b-signals)] | :small[[Reference metrics](#the-bollinger-measurements-at-a-glance)] | :small[[Examples](#verified-bollinger-examples)])

The three heatmaps share the same classification and contextual evidence. **Rolling** leads with the indicator value; **Single Indicator** can combine price/volume context in its opening lines; **Multiple Indicators** retains its own layout. The field ordering below is the authoritative *Bollinger %B-specific sequence*; optional display geometry and view-specific opening context do not change any numeric calculations.

### Enhanced %B hover field map
(:small[[Measurement table](#the-bollinger-measurements-at-a-glance)] | :small[[Standalone Bandwidth reader](#reading-a-standalone-bandwidth-cell)] | :small[[Bottom-line priorities](#how-the-bottom-line-chooses-what-to-explain)])

| Field | What it tells you | How to interpret it |
| --- | --- | --- |
| :blue-background[Value] | Current displayed :blue-background[%B], scaled :gray-background[×100] from the raw fraction | Position of price relative to the three bands; may be outside :gray-background[0–100] |
| :blue-background[Δ vs prior day] | Absolute displayed %B-point change and, where valid, relative percentage change | One-session indicator change; **not** stock-price performance |
| :blue-background[Trend] | Whether %B itself rose, fell or was flat since the prior session | Can include separate price/volume direction in Single Indicator |
| :blue-background[Signal] | Verified Strong Buy / Buy / Neutral / Sell / Strong Sell | Determines the cell background; independent of Bandwidth context |
| :blue-background[Rule] | Dynamic, horizon-specific explanation of the actual five-state result | Uses verified rulebook thresholds and unrounded raw value; explains the exact classification |
| :blue-background[Bandwidth] | Current displayed width; prior-day absolute point change, relative percentage and mathematical Rising/Falling/Flat | Width of envelope and one-day numeric movement |
| :blue-background[Bandwidth State] | Very Narrow, Narrow, Typical, Wide, Very Wide, with historical percentile | Level **relative to the same security's** 60/120 historical Bandwidth observations |
| :blue-background[Bandwidth Change (1D)] | Expanding, Contracting, Stable | Relative one-day change compared against ST/MT/LT tolerance; may be Stable despite mathematical movement |
| :blue-background[Bandwidth Development] | Five-session absolute/relative change, qualifying direction streak and optional Compression Exit | Distinguishes a short-term pause from persistent expansion or contraction |
| :blue-background[Breach Status] | Fresh/Continuing outer-band breach, re-entry, No Active Breach or unavailable status | What current price is doing **relative to the physical bands** |
| :blue-background[Bottom-line] | Concise synthesis of qualifying historical State, development and price-position evidence | **Conditional:** it may be omitted if no meaningful, verified combination qualifies |
| :blue-background[Notes] | Existing educational and rulebook context | Additional definition; does not affect the Signal |
| :blue-background[Definition] / :blue-background[How to Read] | Static background explanation | How to interpret %B and its contrarian scoring model |
| :blue-background[Mid / Upper / Lower] | Current band geometry and any existing price-relative context | Where the actual Bollinger envelope sits around price |

**Two kinds of movement:** :blue-background[Bandwidth] may display a mathematical :gray-background[Rising] change while :blue-background[Bandwidth Change (1D)] says :gray-background[Stable], because the latter applies a materiality tolerance. Neither indicates stock-price direction by itself.

### How the Bottom-line chooses what to explain

The dynamic :blue-background[Bottom-line] does **not** repeat the five-state score. It looks for the most meaningful verified combination in this broad priority order:

1. **Re-entry:** interruption of a previous upper/lower outside-band extension.
2. **Compression Exit:** an actual Bandwidth-state transition out of historical compression, interpreted with any price/breach evidence.
3. **Still-compressed environment:** persistent or intensifying :gray-background[Very Narrow/Narrow] context, including Stable or Contracting days.
4. **Established expansion:** multi-session widening and its relation to inside-band position or persistent outside-band closes.
5. **Cooling:** meaningful narrowing from a previously elevated envelope.
6. **Other qualified price/volatility events:** fresh breaches or newly widening behavior; a final lower-priority case for :gray-background[Very Wide] Bandwidth after :gray-background[≥ +20%] five-session growth when the current day is Stable and there is No Active Breach.

These are **interpretation priorities**, not six new scoring states. The helper verifies the indicator value, rulebook, score, historical State/percentile consistency and event evidence. It may deliberately omit a Bottom-line where only routine unqualified observations are present. An absent Bottom-line does not equal Neutral and does not erase the measurements already shown in the hover.

### Reading the numbers together: three verified examples

| Date / ticker | Key fields | Bottom-line interpretation |
| --- | --- | --- |
| GOOGL :gray-background[2026-10-08] · MT | :gray-background[%B 66.7]; :gray-background[Very Narrow / 2.1st percentile]; five-session Bandwidth :gray-background[−23.8%]; Contracting | Exceptionally compressed envelope is narrowing further while price is inside the bands |
| GOOGL :gray-background[2026-10-22] · MT | :gray-background[%B −24.9]; State :gray-background[Typical] following compression; :gray-background[Compression Exit]; Continuing Lower Breach; five-session :gray-background[+38.4%] | Price remains beyond the lower band as the envelope exits compression and widens materially |
| ARKK :gray-background[2026-09-24] · ST | :gray-background[%B 93.6]; :gray-background[Very Wide / 92.5th percentile]; five-session :gray-background[+113.7%]; current day Stable | Exceptionally wide envelope after rapid recent expansion; price near upper band, with material daily widening paused |

The percentages above describe **Bandwidth**, not daily stock-price returns. See the [complete pattern reference](#bollinger-pattern-reference-complete-interpretations) for what these contexts suggest and what to monitor.

---

## Reading %B and Bandwidth together
(:small[[Back to top](#summary-bollinger-b-signals) | See: [101: How Are They Used Together?](#how-are-they-used-together)] | :small[Related: [Priority patterns](#the-bollinger-patterns-you-should-not-overlook)] | :small[[Reading Bandwidth State + Bandwidth Change together](#reading-bandwidth-state--bandwidth-change-1d-together)])

The enhanced :blue-background[%B] hover combines **price position**, **historical Bandwidth level**, **recent development**, and **Breach Status**. A contrarian Buy or Sell is still determined from :blue-background[%B] alone. Interpret the market condition separately from the project's directional *exhaustion* label.

### Bullish, bearish and potential failed-release comparison

Here, **bullish/bearish describes observed price extension**, not the project's Buy/Sell score. A confirmed break of independent price support/resistance, volume participation, or actual subsequent return is **not** supplied by Bandwidth alone.

| Evidence | Emerging upside release | Emerging downside release | Possible failed release / interrupted extension |
| --- | --- | --- | --- |
| **Price action** | Price tests or exceeds the upper Bollinger band; confirm any separately defined resistance break with price-structure data | Price tests or falls below the lower Bollinger band; confirm any separately defined support break externally | Price returns inside after an outer-band extension, or fails to sustain an attempted move |
| :blue-background[%B] | Moves toward :gray-background[100] or above; above :gray-background[100] is a physical upper-band breach | Moves toward :gray-background[0] or below; below :gray-background[0] is a physical lower-band breach | Moves back within :gray-background[0–100] after an outside-band close |
| :blue-background[Bandwidth State] | Historically :gray-background[Very Narrow/Narrow] sets up the release | Same compressed environment can precede a downside attempt | May remain compressed or shift back toward compression; not decisive alone |
| :blue-background[Bandwidth Change (1D)] | Expanding supports increased envelope width | Expanding supports increased envelope width | Stable/Contracting can accompany a stalled expansion; a single Stable day is not proof of failure |
| :blue-background[Bandwidth Development] | Repeated widening, material five-session growth or actual Compression Exit increases the evidence of development | Same widening criteria with lower-band price pressure | Widening stalls, contracts, or price re-enters while width is still elevated |
| :blue-background[Breach Status] | Fresh then potentially Continuing Upper Breach | Fresh then potentially Continuing Lower Breach | Upper/Lower-Band Re-entry is directly observed when price returns inside |
| **What to monitor** | Does price sustain upper-band positioning as volatility develops? | Does price sustain lower-band positioning as volatility develops? | Does price hold inside the bands, re-breach, or accompany a cooling envelope? |

A **re-entry is observable**. A market-wide or price-structure **fakeout** is a broader trading conclusion requiring subsequent behavior and often price/volume confirmation. A Bollinger breach also does not, by itself, prove that institutional buyers or sellers are participating.

---

## Bollinger Pattern Reference — Complete Interpretations
(:small[[Back to top](#summary-bollinger-b-signals)] | :small[[Top patterns](#the-bollinger-patterns-you-should-not-overlook)] | :small[[Rule windows](#historical-reference-window-by-horizon)])

Use this lookup when a particular combination appears in a cell. **Priority** identifies how informative the combination is for *describing the observed condition*; it is not a statistically calibrated trading-success ranking. For the five-state Signal thresholds, see [Project %B rules — consolidated reference](#project-b-rules-consolidated-reference).

### Compression and setup patterns

| Priority | Evidence / pattern | Interpretation | What to monitor |
| --- | --- | --- | --- |
| **1** | :gray-background[Very Narrow + Contracting]; possibly five-session :gray-background[≤ −20%] | Exceptionally narrow envelope is narrowing further: **deepening compression** | A new outer-band test and eventual change in Bandwidth Change (1D) |
| **2** | :gray-background[Very Narrow + Stable] | Exceptionally compressed environment is persisting, even with an ordinary/Neutral %B score | Whether Bandwidth begins materially widening or price starts pressing toward a band |
| **3** | :gray-background[Narrow + Expanding], possibly multiple sessions | Bandwidth is widening from a still-compressed baseline: an early development, **not yet necessarily a Compression Exit** | Whether State actually leaves compression; where price sits relative to bands |
| **4** | :gray-background[Narrow/Very Narrow] + Fresh outside-band breach | An **initial directional extension** from compressed conditions; the breach and volatility regime must be read together | Further closes beyond the same band, repeated widening, actual Compression Exit |
| **5** | :gray-background[Narrow + Stable/Contracting] | Narrow environment persists or is becoming narrower | Whether an apparent price move gains widening confirmation |

**Example:** GOOGL on September 15 widened about :gray-background[+40.9%] across five sessions but remained historically :gray-background[Narrow] and had a Stable 1D change. That is **still compression**, not an established release simply because the net percentage is large.

### Bullish price-action patterns

These are **upper-band price-pressure** patterns; the rule-engine may classify their high :blue-background[%B] values as :gray-background[Sell/Strong Sell].

| Priority | Evidence / pattern | Interpretation | What to monitor |
| --- | --- | --- | --- |
| **1** | :gray-background[Compression Exit + Upper Breach] | Volatility-state release accompanies observable upside price extension | Whether upper-side pressure persists as Bandwidth continues widening |
| **2** | :gray-background[Narrow/Very Narrow + Fresh Upper Breach + Expanding] | Initial upside release attempt from compression | Consecutive upper-band closes and whether Bandwidth exits compression |
| **3** | :gray-background[Continuing Upper Breach + sustained widening] | Repeated upside extension during an expanding envelope | Whether closes keep riding above the band or return inside |
| **4** | :gray-background[Upper-Band Re-entry] | Upper-side extension has been interrupted; volatility can still be expanding | Whether price stays inside and whether Bandwidth begins cooling |
| **5** | :gray-background[Very Wide + ≥ +20% over five sessions + Stable + No Active Breach], upper-side :blue-background[%B] | Volatility remains exceptionally elevated after substantial growth; price near the upper band shows upper-side positioning while the latest widening pauses | Whether price presses beyond the upper band or Bandwidth contracts |
| **6** | :gray-background[Sell/Strong Sell] Signal alone | Price is near/above the upper band under a contrarian exhaustion rule | Use State/Development/Breach to distinguish trending extension from isolated stretch |

**GOOGL September 21:** Upper-band :gray-background[Fresh Breach], :gray-background[Narrow] State, about :gray-background[+22.3%] over five sessions and three Expanding sessions indicate an emerging upside attempt **while still compressed**, not a completed Compression Exit.

### Bearish price-action patterns

These are **lower-band price-pressure** patterns; the rule-engine may classify low :blue-background[%B] values as :gray-background[Buy/Strong Buy].

| Priority | Evidence / pattern | Interpretation | What to monitor |
| --- | --- | --- | --- |
| **1** | :gray-background[Compression Exit + Lower Breach] | Volatility-state release is occurring alongside downside price pressure | Whether the downside extension continues as the envelope expands |
| **2** | :gray-background[Narrow/Very Narrow + Fresh Lower Breach + Expanding] | Initial downside extension from compressed conditions | Persistence below the band and whether Bandwidth exits compression |
| **3** | :gray-background[Continuing Lower Breach + sustained widening] | Persistent downside extension within an actively expanding envelope | Additional outside closes, re-entry, or slowing Bandwidth expansion |
| **4** | :gray-background[Lower-Band Re-entry] | The lower-side extension has been interrupted; the volatility environment may still be active | Whether price holds within the bands as Bandwidth evolves |
| **5** | :gray-background[Very Wide + ≥ +20% over five sessions + Stable + No Active Breach], lower-side :blue-background[%B] | Exceptionally elevated volatility after strong recent widening; price sits near the lower band even though daily widening pauses | Renewed band breach or movement toward the midpoint |
| **6** | :gray-background[Buy/Strong Buy] Signal alone | Price is near/below the lower band under the contrarian exhaustion model | Check whether a lower-band extension is fresh, continuing or interrupted |

**GOOGL October 22 and 30:** October 22 records an actual Compression Exit with a continuing lower-band breach. By October 30, :gray-background[Very Wide] Bandwidth, a five-session :gray-background[+153.0%] increase and a continuing lower breach describe **persistent downside pressure**, despite the contrarian :gray-background[Strong Buy] label.

### Volatility development patterns

These can matter in either price direction; use current :blue-background[%B] and :blue-background[Breach Status] to determine which side, if any, is under pressure.

| Priority | Evidence / pattern | Interpretation | What to monitor |
| --- | --- | --- | --- |
| **1** | :gray-background[Compression Exit] | The envelope has transitioned out of historical compression on a qualifying Expanding day | Whether an upper/lower band breach accompanies or follows it |
| **2** | :gray-background[Very Wide + substantial five-session growth] with current 1D Stable | Extremely wide envelope remains elevated after rapid recent widening, even though daily material growth pauses; lower-priority Bottom-line requires No Active Breach | Current price location and whether widening resumes or contraction begins |
| **3** | :gray-background[Wide/Very Wide + Contracting] | Envelope remains historically elevated but has begun narrowing: **early cooling** | Whether several Contracting sessions accumulate and State normalizes |
| **4** | :gray-background[Wide/Very Wide + ≤ −20% over five sessions + ≥2 Contracting days] | Sustained cooling after an expanded-volatility environment | Whether State declines from Very Wide toward Wide/Typical |
| **5** | :gray-background[Typical + sustained Expanding + price inside bands] | Broadening envelope remains active without a current outside-band breach | Whether price relocates toward or beyond either edge |
| **6** | :gray-background[Very Wide + Stable] without recent development | Historically elevated band width remains high, but today's movement alone is inconclusive | Price position and any subsequent contraction; a Bottom-line is not automatic |

### Ordinary and lower-priority combinations

| Priority | Evidence / pattern | Meaning | Why it is lower priority |
| --- | --- | --- | --- |
| **1** | :gray-background[Typical + Stable + No Active Breach] | Ordinary relative Bandwidth with no qualifying price event | Individual fields usually communicate enough; an extra Bottom-line may be omitted |
| **2** | :gray-background[Typical + single Expanding day] | One-session widening | Without material multi-session development or a price event, it is not necessarily a volatility release |
| **3** | :gray-background[Signal: Neutral] alone | Current %B is in its middle scoring zone | Neutral does **not** imply absent compression; always check historical State |
| **4** | :gray-background[Continuing Breach] without qualifying development | Price is repeatedly outside a band, but the volatility-development evidence is incomplete or mixed | Breach Status itself is still informative; a Bottom-line is selective rather than guaranteed |

### Verified Bollinger examples

These readings come from the bounded GOOGL diagnostic and the cross-stock peer verification used for Stage 6. The interpretations are descriptive of the **stated date**, not outcomes observed afterward.

| Date / ticker | Observation | Material insight |
| --- | --- | --- |
| **GOOGL Sep 15 · MT** | :gray-background[Narrow]; BW five-session :gray-background[+40.9%]; 1D Stable; No Active Breach | Bands have widened considerably but remain historically narrow; compression is not automatically over |
| **GOOGL Sep 21 · MT** | :gray-background[Fresh Upper Breach]; :gray-background[Narrow]; :gray-background[+22.3%] over five sessions; three Expanding sessions | Emerging upside release attempt from compressed conditions—not yet a Compression Exit |
| **GOOGL Oct 8 · MT** | :gray-background[%B 66.7]; :gray-background[Very Narrow / 2.1st percentile]; five-session :gray-background[−23.8%]; Contracting | Deepening compression with price inside the bands |
| **GOOGL Oct 20 · MT** | :gray-background[Very Narrow]; Stable; five-session :gray-background[−5.7%]; price in lower portion | Historical compression persists even without a qualifying daily contraction |
| **GOOGL Oct 21 · MT** | :gray-background[Fresh Lower Breach]; State still :gray-background[Narrow]; Expanding | Initial downside extension while the envelope remains compressed |
| **GOOGL Oct 22 · MT** | :gray-background[%B −24.9]; :gray-background[Compression Exit]; :gray-background[Continuing Lower Breach]; five-session :gray-background[+38.4%] | Developing downside pressure accompanies a genuine transition out of compression |
| **GOOGL Oct 27 · MT** | :gray-background[Lower-Band Re-entry]; five-session :gray-background[+146.9%]; Expanding | Downside extension interrupted even as Bandwidth continues expanding |
| **GOOGL Oct 28 · MT** | :gray-background[%B 18.2]; :gray-background[Typical]; :gray-background[+143.0%] over five sessions; six Expanding sessions; No Active Breach | Inside-band price position coexists with substantial ongoing volatility expansion |
| **GOOGL Oct 30 · MT** | :gray-background[%B −14.5]; :gray-background[Very Wide / 95.4th percentile]; :gray-background[+153.0%] over five sessions; eight Expanding sessions; Continuing Lower Breach | Persistent downside extension during a historically wide, actively expanding envelope |
| **ARKK Sep 24 · ST** | :gray-background[%B 93.6]; :gray-background[Very Wide / 92.5th percentile]; five-session :gray-background[+113.7%]; 1D Stable; No Active Breach | Exceptionally wide envelope after substantial expansion; upper-side price positioning while today's material widening pauses |

**How to read a representative row:** For GOOGL on October 30, the Bandwidth five-session increase of :gray-background[+153%] means the bands were about :gray-background[2.53×] as wide as five sessions earlier. In the same observation, two consecutive lower-band closes indicate that price remained outside the envelope on the downside. The :gray-background[Strong Buy] classification is *exhaustion semantics*, not an assertion that the downside extension has ended.

For the condensed priority order, return to [The Bollinger patterns you should not overlook](#the-bollinger-patterns-you-should-not-overlook). For exact qualifying rules, refer to [Bandwidth Development](#bandwidth-development-multi-session-context), [Breach Status](#breach-status-and-compression-exit), and the [enhanced hover field map](#enhanced-b-hover-field-map).

---

## Strengths & Weaknesses (BB)
(:small[[Back to top](#summary-bollinger-b-signals)])

### Strengths of the Bollinger implementation

- **Normalized location:** :blue-background[%B] expresses price position relative to the envelope rather than in raw dollars.
- **Volatility separated from direction:** BB_BW remains nondirectional while :blue-background[%B] carries the exhaustion score.
- **Instrument-relative State:** Bandwidth State compares Bandwidth with the same security's own recent history instead of using one absolute cutoff for every ticker.
- **Level separated from movement:** State says how unusual current width is; 1D Change and Development show daily and multi-session behavior.
- **Breach timing:** Fresh, Continuing, and Re-entry statuses distinguish outside-band events from a simple high/low %B reading.
- **Prioritized synthesis and visual discovery:** Conditional Bottom-lines, purple Very Narrow values and black Compression Exit ◆ expose important context without changing scores.
- **Multiple horizons:** ST, MT, and LT provide fast, balanced, and structural views of the same Bollinger framework.

### Limitations and interpretation risks

- **Extremes can persist:** Buy/Sell exhaustion labels do not guarantee an immediate reversal, especially during strong trends.
- **:blue-background[%B] is a location measure first:** the contrarian interpretation is a project choice; other legitimate systems may use :blue-background[%B] differently.
- **Bandwidth does not predict breakout direction:** compression or expansion describes volatility, not whether price will move up or down.
- **Bandwidth State is history-dependent:** :gray-background[Typical] means normal relative to the configured recent history, not an absolute universal volatility level.
- **ST / MT / LT are not votes:** they are different horizon lenses.
- **Thresholds are empirical project calibrations:** :blue-background[%B] boundaries, Bandwidth percentile cutoffs, lookbacks, and Direction tolerances are not universal Bollinger constants.

## Notes: Bollinger Bands
(:small[[Back to top](#summary-bollinger-b-signals)])

**Purpose:** :blue-background[%B] measures price location/stretch; standalone :blue-background[BB Bandwidth] measures envelope width. The enhanced %B hover combines :blue-background[Bandwidth State], :blue-background[Bandwidth Change (1D)], :blue-background[Bandwidth Development] and :blue-background[Breach Status] into a conditional :blue-background[Bottom-line].

**Configured variants:** [BB(10,1.5) ST](#bb1015-b-rules-interpretation), [BB(20,2.0) MT](#bb2020-b-rules-interpretation), [BB(50,2.5) LT](#bb5025-b-rules-interpretation).

**Quick :blue-background[%B] landmarks:** :gray-background[0] = lower band, :gray-background[50] = middle band, :gray-background[100] = upper band; values can move below :gray-background[0] or above :gray-background[100].

**BB_BW score:** valid Bandwidth remains :gray-background[Neutral / 0] because it measures volatility rather than bullish/bearish direction.

**Key distinction:** :blue-background[%B] exhaustion signals and observed price-extension direction are different concepts; narrow/wide/expanding/contracting Bandwidth remains nondirectional. **Visual legend:** purple = Very Narrow, black ◆ = Compression Exit event.

### 101
(:small[[Detailed Bandwidth State rules](#bandwidth-state)] | :small[[Change tolerances](#bandwidth-change-1d-thresholds-by-horizon)] | :small[[Hover field map](#enhanced-b-hover-field-map)])

#### Purpose

Bollinger Bands provide a volatility-adjusted envelope around price. The project uses that envelope to answer three questions:

```text
%B                  = Where is price?
Bandwidth State    = How unusual is current Bandwidth?
Bandwidth Change (1D) = Is Bandwidth widening, narrowing, or stable?
```

#### Key components

- **Middle Band:** moving-average center.
- **Upper / Lower Bands:** volatility-adjusted boundaries.
- **%B:** price position within or beyond the bands.
- **Bandwidth:** total envelope width relative to the middle band.

#### Quick guides

```text
%B: 0 = lower band | 50 = middle | 100 = upper band

Bandwidth State:
Very Narrow → exceptionally narrow vs recent history
Narrow      → narrower than usual
Typical          → around the typical recent range
Wide        → wider than usual
Very Wide   → exceptionally wide vs recent history

Bandwidth Change (1D):
Expanding   → getting wider
Contracting → getting narrower
Stable      → change is too small to count as meaningfully wider/narrower
```

#### Companion indicators

Useful companions include SMA/EMA for trend, ADX for trend strength, RSI/Stochastic/Williams %R/MFI for independent stretch or momentum context, ROC/MACD for momentum change, and volume/CMF/OBV for participation. None is required by the Bollinger score.

#### Primary limitation

Bollinger measurements describe **current relative conditions**. Read :blue-background[%B] as price location/stretch and Bandwidth as volatility context; neither guarantees the next price move.


---

---

## Old Notes
(:small[[Back to top](#summary-bollinger-b-signals)])

Bollinger Bands are often misunderstood as simple "overbought/oversold" indicators. 
- In reality, they are a map of **volatility-adjusted price action**. If you are building a dashboard, you want metrics that normalize data so you can compare a tech stock to a currency pair without the raw price scale getting in the way.

---
Here is the breakdown of the three primary metrics, and one value-added derivation.


##### 1. %B (Percent B)
**The Formula:** $$\%B = \frac{\text{Price} - \text{Lower Band}}{\text{Upper Band} - \text{Lower Band}}$$

* **The Insight:** It quantifies where the price is relative to the bands. 
    * **1.0:** Price is at the Upper Band.
    * **0.5:** Price is at the Midpoint (SMA).
    * **> 1.0:** Price is "walking the bands" (strong trend).
* **Value-Add:** It is essential for **signal confirmation**. If price makes a new high but %B makes a lower high (divergence), you have a classic "W-Bottom" or "M-Top" setup in the making.

##### 2. Bandwidth
**The Formula:** $$\text{Bandwidth} = \frac{\text{Upper Band} - \text{Lower Band}}{\text{Middle Band}}$$

* **The Insight:** This measures the "squeeze." It normalizes the width of the bands by dividing by the SMA.
* **Value-Add:** It is your **Volatility Regime** indicator. Narrow bandwidth tells you the market is coiled like a spring. A massive spike in bandwidth tells you the trend is likely climaxing.
* **Dashboard Utility:** It allows you to set "Squeeze Alerts" when bandwidth hits a 6-month or 1-year low.

##### 3. BB Trend (The Directional Component)
* **The Insight:** Simply tracking the slope of the Middle Band (the 20-period SMA).
* **Value-Add:** It provides the **Context**. Bollinger Bands are mean-reverting in sideways markets but trend-following in breakouts. Without knowing the slope of the mid-line, you won't know whether to fade the bands or ride them.

---

##### "BB Squeeze Score"

A **derived metric** that combines Bandwidth and %B to identify **Vol-Expansion Breakouts.**

**Why this metric?**
Raw price data is noisy. A dashboard's job is to filter noise into "Opportunity Zones." By tracking the **Rate of Change (ROC) of Bandwidth** alongside **%B**, you can identify the exact moment a market transitions from "Quiet/Accumulation" to "Active/Expansion."

**How to implement it on your dashboard:**
1.  **Metric:** **Bandwidth Percentile.** (Where is current Bandwidth relative to its last 125 periods?)
2.  **Trigger:** When Bandwidth Percentile is < 10% (The Squeeze).
3.  **Direction:** Use %B to determine the breakout. If %B crosses 0.8 while Bandwidth is expanding from a low percentile, you have a high-probability "Head-Fake" or "Squeeze Play" starting.

> **Tip:** > Never use Bollinger Bands in isolation for a dashboard. Pair them with a non-correlated volume indicator (like MFI or On-Balance Volume). 
> - If price hits the Upper Band (%B > 1.0) but volume is drying up, that "breakout" is likely a trap.


---

### Parameter Settings


**BB (10, 1.5)**:
- The "Front-Run" Band. 
- This is very tight. Price will hug or pierce these bands constantly. 
- This acts as an ***"early warning system"***. 
    - It tells you when a micro-trend is accelerating before the standard bands even react.

**BB (20, 2.0)**:
- The "Standard" Band. 
- This is the ***'baseline'***. 
- Represents the "normal" distribution of price for a swing trader.

**BB (50, 2.5)**:
- The "Institutional" Band. 
- By moving to 2.5 standard deviations and 50 periods, you're looking for tail-risk events. 
- When price touches the 50/2.5 band, it’s a "3-sigma" style event—meaning the move is statistically significant and likely driven by high-conviction institutional flow.

---
## Bollinger 101
(:small[[Back to top](#summary-bollinger-b-signals)])

### What Are Bollinger Bandwidth and %B?
(:small[[Parent](#bollinger-101)])

Bollinger Bands consist of three lines on a price chart: a middle simple moving average (typically 20 periods) and upper/lower bands placed two standard deviations away.

**Bollinger Bandwidth** and **%B** are two mathematical indicators derived from those bands that turn visual lines into concrete numbers:
- **Bollinger Bandwidth:** Measures the **distance or spread** between the upper and lower bands relative to the middle band.
    - _Formula:_ :blue-background[(Upper Band - Lower Band) / Middle Band]

- **%B (Percent B):** Quantifies where the **closing price** sits relative to the upper and lower bands.
    - _Formula:_ :blue-background[(Closing Price - Lower Band) / (Upper Band - Lower Band)]

---
### What Insight Does Each Provide?
(:small[[Parent](#bollinger-101)])

#### %B (The Position/Overbought-Oversold Gauge)
(:small[Parent: [What Are Bollinger Bandwidth and %B?](#what-are-bollinger-bandwidth-and-b) | Related: [%B: Where Price is relative to the Bands](#b--where-is-price-relative-to-the-bands)])

- **What it tells you:** The exact location of the price between the two outer bands.

- **Reading Scale:**
    - :gray-background[%B = 1.0]: Price is sitting right on the **upper band**.
    - :gray-background[%B = 0.5]: Price is sitting right on the **middle band** (moving average).
    - :gray-background[%B = 0.0]: Price is sitting right on the **lower band**.
    - :gray-background[%B > 1.0] or :gray-background[%B < 0.0]: Price has broken **outside** the upper or lower bands.
- **Key Insight**: It shows whether price is pressing against resistance (near 1.0) or support (near 0.0), helping spot overbought/oversold conditions or confirm chart patterns like W-bottoms and M-tops.

#### Bollinger Bandwidth (The Volatility Gauge)
(:small[[Parent](#bollinger-101) | Related: [Bandwidth: How wide are the bands?](#bandwidth-how-wide-are-the-bands) & [Understanding Bollinger Bandwidth](#understanding-bollinger-bandwidth)])

- **What it tells you:** How "wide" or "tight" the market is right now.
- **Low Bandwidth (Squeeze):** When the bands contract tightly together, Bandwidth drops to multi-month or extreme lows. This signals a :red[quiet, low-volatility consolidation phase].
- **High Bandwidth (Expansion):** When the bands stretch far apart, Bandwidth spikes. This signals :red[high volatility, strong directional trends, or market panic].
- **Key Insight**: Bandwidth does **not** tell you _which_ direction the price will break; it only tells you that volatility is contracting (often preceding a sharp move) or expanding.

### How Are They Used?
(:small[[Parent](#bollinger-101) | See: [%B- Where Price is relative to the Bands](#b--where-is-price-relative-to-the-bands)])

- **Using Bandwidth:** Traders track Bandwidth for **breakout setups**.
	- When Bandwidth hits an extreme low ("squeeze"), they wait for price to break out of the consolidation range, expecting a large directional move.

- **Using %B:** Traders use %B for **timing entries and exits**.
	- For example, if %B drops below 0.0 or bounces up from near 0.0 during a W-bottom pattern, it can signal a buying opportunity.
	- It also helps compare price extremes across different volatility environment

### How Are They Used Together?
(:small[[Parent](#bollinger-101) | Related: [Reading %B and Bandwidth together](#reading-b-and-bandwidth-together)])

**%B and Bandwidth complement and inform each other significantly.** They answer two completely different questions:
- _“Is a big move about to happen?”_ (Bandwidth) and
- _“Where is the price right now relative to the extremes?”_ (%B).

**The Squeeze + Position Synergy:**
- Bandwidth tells you when volatility has dried up to a extreme low (a squeeze).
- Once you see Bandwidth signaling a squeeze, you turn to **%B** to see _which way_ the price is leaning inside that tight range. If %B is creeping toward 1.0 (the upper band) during a tight squeeze, it suggests underlying strength and a readiness to break upward. If %B is hugging 0.0, it leans toward a breakdown.

**False Breakout Filter:**
- If price spikes past an outer band (pushing %B above 1.0 or below 0.0), you check Bandwidth.
	- If Bandwidth is already maxed out and expanding rapidly, the trend may have legs. If Bandwidth is low or flat, a move pushing %B past 1.0 might be a fakeout rather than a true breakout


### Terminology
(:small[[Parent](#bollinger-101)])

When a technical indicator is described as **"maxed out and expanding rapidly,"** it means that the indicator has reached a critical extreme and is moving very fast, signaling high momentum. Because Bollinger Bandwidth doesn’t have a fixed ceiling like an RSI or Stochastic oscillator (it isn't bound between 0 and 100), "maxed out" doesn't mean it hit a mathematical limit. Instead, it refers to hitting a **historical relative extreme**.

Here is exactly what that phrase means visually and mechanically on a chart:

#### "Maxed Out" (Historical Extremes)

Because Bandwidth can technically grow as wide as price volatility allows, you determine if it is "maxed out" by looking backward at the chart's history (usually the last 6 to 12 months).

- **The Visual:** The Bandwidth line has climbed to a peak that matches or exceeds previous major volatility spikes.
- **The Meaning:** The market is currently experiencing an unusually high amount of price expansion compared to its recent past. It is a warning sign that the current speed of the move is unsustainable over the long term.

#### "Expanding Rapidly" (The Slope of Volatility)
This refers to the **velocity** of the indicator's movement.
- **The Visual:** The Bandwidth line changes from a flat or gently sloping line into a nearly vertical, steep upward cliff.
- **The Meaning:** Volatility isn't just increasing—it is accelerating. Price is moving away from the 20-period average so fast that the standard deviations (the upper and lower bands) are being forced to rip wide open to accommodate the massive price bars.

---

#### How This Applies to a Trend Having "Legs"
(:small[[Parent](#bollinger-101)])

When you combine a price breakout (where :gray-background[%B] jumps above **1.0**) with a Bandwidth indicator that is **expanding rapidly toward a maxed-out peak**, it tells you a specific story about market psychology:

```
     [ Price Rips Higher ]
---> [ %B Shoots > 1.0 ]
---> [ Bandwidth Slopes Sharply Up ]
                                                            (Signals strong institutional volume and a trend with "legs")
```

- **A Trend with "Legs" (The Real Deal):** If a stock breaks out and Bandwidth shoots up like a rocket, it proves that the price movement is backed by massive volume and institutional momentum. Even though the price is "expensive" relative to the bands (:gray-background[%B > 1.0]), the rapid expansion of Bandwidth suggests this is the _beginning_ of a powerful trend, not a temporary spike. Traders will often buy into this momentum.
- **The Alternative (The "Fakeout"):** If price pushes past the upper band (:gray-background[%B > 1.0]), but the Bandwidth line barely nudges upward or stays flat, it means there is no real volatility or volume behind the move. The trend lacks "legs," and the price is highly likely to snap back inside the bands immediately.

---
#### Bollinger Bands Volatility Cycles
(:small[[Parent](#bollinger-101)])

> *Transitioning from low-volatility Squeeze compression to high-momentum Trend Expansion*


$\Large{\textsf{Anatomy of the Three Key Stages}}$
##### 1. The Squeeze Phase (Days 0 to 40)
- **The Price Action:** The stock is trading in a dull, tight sideways channel.
- **How the Bands React:** Because standard deviation relies on recent price changes, a flat market forces the upper and lower bands to pinch tightly together.
- **The Indicator Readings:**
       - **Bandwidth** drops to its lowest historical floor on the chart. This is the visual definition of "volatility compression."
    - **%B** constantly fluctuates quickly between **0.20** and **0.80**, bouncing like a pinball inside the tight bands because the distance from top to bottom is incredibly small.

##### 2. The Rapid Expansion (Days 41 to 70)
- **The Price Action:** A catalyst hits, major institutional buyers step in, and the price sharply bursts through the ceiling of the old consolidation zone.
- **How the Bands React:** The bands violently split apart like an opening alligator jaw. The upper band curves sharply upward with the price, while the lower band actually bends _downward_ momentarily due to the mathematical explosion in standard deviation.
- **The Indicator Readings:**
       - **%B shoots above 1.0:** This tells you the price isn't just going up—it is actively riding or piercing outside the upper band.
    - **Bandwidth slopes vertically upward:** The slope changes from flat to a steep cliff. This is the definition of **"expanding rapidly."** Because it is accelerating up while :gray-background[%B] is pinned above 1.0, it confirms that this move has real volume and "legs." It tells you _not_ to short the stock just because it looks expensive.

##### 3. Maxed-Out Volatility (Days 71 to 100)
- **The Price Action:** The initial aggressive buying frenzy slows down, and the price begins to move sideways again at its new, higher plateau.
- **How the Bands React:** The bands stop expanding and begin to flatten out or constrict slightly to catch up to the new trading range.
- **The Indicator Readings:**
    - **Bandwidth hits a peak and levels off:** It has reached a historical ceiling relative to the last several months of data. Volatility is now **"maxed out."**
    - **%B drops back toward 0.50:** Even though the stock price remains high, it pulls away from the upper band back toward the middle moving average. The trend's rapid momentum phase is over, and it has moved into a cooling-off period.

#### Executing the Trade: Trigger vs. Fakeout
(:small[[Parent](#bollinger-101)])

Once a stock checks all [[#The 4-Step Squeeze Checklist|four boxes,]] you put it on your watchlist and wait for the **Trigger**.
Do not guess the direction ahead of time; let :gray-background[%B] tell you when the door has opened.

|Metric|Bullish Breakout (Go Long)|Bearish Breakdown (Short/Exit)|The Fakeout (Avoid)|
|---|---|---|---|
|**Price Action**|Closes above upper consolidation resistance.|Closes below lower consolidation support.|Peeks above/below resistance, then reverses immediately.|
|**%B Reading**|**Crosses cleanly above 0.80 toward 1.0+**|**Crosses cleanly below 0.20 toward 0.0-**|Touches 1.0 or 0.0 briefly but snaps right back to 0.50.|
|**Bandwidth**|**Turns sharply upward** from its floor.|**Turns sharply upward** from its floor.|**Stays flat or crawls sideways** despite the price wiggle.|

_**Crucial Rule:**_ Remember that ${\textcolor{Red}{\textsf{Bandwidth always turns upward}}}$ regardless of whether the stock goes up or down.
- ==A sharp uptick in Bandwidth simply confirms that the market has **chosen a direction** and **fuel is entering the tank**==.


---
## TOC: Bollingers
(:small[[Back to top](#summary-bollinger-b-signals)])

- [Summary: Bollinger %B signals](#summary-bollinger-b-signals)
- [The Bollinger patterns you should not overlook](#the-bollinger-patterns-you-should-not-overlook)
- [How to read the Bollinger heatmap](#how-to-read-the-bollinger-heatmap)
  - [Reading a %B cell](#reading-a-b-cell)
  - [Reading the new display-value customizations](#reading-the-new-display-value-customizations)
  - [Setup, transition and development](#setup-transition-and-development)
  - [Reading a standalone Bandwidth cell](#reading-a-standalone-bandwidth-cell)
- [Bollinger Bands / %B / Bandwidth — brief overview](#bollinger-bands-b-bandwidth-brief-overview)
  - ['%B' — Where is price relative to the bands?](#b-where-is-price-relative-to-the-bands)
  - [Bandwidth — how wide are the bands?](#bandwidth-how-wide-are-the-bands)
  - [Value-added use](#value-added-use)
  - [Use with](#use-with)

- [The Bollinger measurements at a glance](#the-bollinger-measurements-at-a-glance)
- [BB %B Rule Translation](#bb-b-rule-translation)
  - [Strong Buy (%B)](#strong-buy-b)
  - [Buy (%B)](#buy-b)
  - [Neutral (%B)](#neutral-b)
  - [Sell (%B)](#sell-b)
  - [Strong Sell (%B)](#strong-sell-b)
- [Industry-standard baseline](#industry-standard-baseline)
- [How the TA Rule Engine extends the classic baseline](#how-the-ta-rule-engine-extends-the-classic-baseline)
- [Why Strong thresholds differ by horizon](#why-strong-thresholds-differ-by-horizon)
- [Comparison of the three Bollinger settings](#comparison-of-the-three-bollinger-settings)
  - [Practical selection guide](#practical-selection-guide)
- [BB(10,1.5) %B Rules interpretation](#bb1015-b-rules-interpretation)
- [BB(20,2.0) %B Rules interpretation](#bb2020-b-rules-interpretation)
- [BB(50,2.5) %B Rules interpretation](#bb5025-b-rules-interpretation)
- [Project %B rules — consolidated reference](#project-b-rules-consolidated-reference)
  - [Scoring](#scoring)
  - [Boundary handling](#boundary-handling)
  - [Missing / warmup behavior](#missing-warmup-behavior)
  - [What the '%B' score uses](#what-the-b-score-uses)
- [Understanding Bollinger Bandwidth](#understanding-bollinger-bandwidth)
  - [Why the Bandwidth number alone is not enough](#why-the-bandwidth-number-alone-is-not-enough)
  - [Why BB_BW remains Neutral / 0](#why-bbbw-remains-neutral-0)
- [Bandwidth State](#bandwidth-state)
  - [Beginner interpretation (Bandwidth State)](#beginner-interpretation-bandwidth-state)
  - [Consistent Bandwidth State labels across the heatmaps](#consistent-bandwidth-state-labels-across-the-heatmaps)
  - [How the percentile classification works](#how-the-percentile-classification-works)
  - [Historical reference window by horizon](#historical-reference-window-by-horizon)
  - [Bandwidth State calibration by horizon](#bandwidth-state-calibration-by-horizon)
  - [Warmup behavior](#warmup-behavior)
- [Bandwidth Change (1D)](#bandwidth-change-1d)
  - [Beginner interpretation (Bandwidth Change 1D)](#beginner-interpretation-bandwidth-change-1d)
  - [How Bandwidth Change (1D) is calculated](#how-bandwidth-change-1d-is-calculated)
  - [Bandwidth Change (1D) thresholds by horizon](#bandwidth-change-1d-thresholds-by-horizon)
  - [One-session change warmup](#one-session-change-warmup)
- [Bandwidth Development: multi-session context](#bandwidth-development-multi-session-context)
  - [Five-session Bandwidth change](#five-session-bandwidth-change)
  - [Interpretation filters versus measurement definitions](#interpretation-filters-versus-measurement-definitions)
  - [Streak exactness and missing history](#streak-exactness-and-missing-history)
- [Breach Status and Compression Exit](#breach-status-and-compression-exit)
  - [Breach Status: price versus the bands](#breach-status-price-versus-the-bands)
  - [Compression Exit: a Bandwidth-state event](#compression-exit-a-bandwidth-state-event)
- [Reading Bandwidth State + Bandwidth Change (1D) together](#reading-bandwidth-state-bandwidth-change-1-d-together)
  - [Example 1 — Very Narrow + Stable](#example-1-very-narrow-stable)
  - [Example 2 — Narrow + Expanding](#example-2-narrow-expanding)
  - [Example 3 — Typical + Contracting](#example-3-typical-contracting)
  - [Example 4 — Wide + Expanding](#example-4-wide-expanding)
  - [Example 5 — Very Wide + Contracting](#example-5-very-wide-contracting)
  - [Additional State + Change combinations](#additional-state-change-combinations)
  - [Why State and Change can appear to disagree](#why-state-and-change-can-appear-to-disagree)
- [Understanding the enhanced Bollinger %B hover](#understanding-the-enhanced-bollinger-b-hover)
  - [Enhanced %B hover field map](#enhanced-b-hover-field-map)
  - [How the Bottom-line chooses what to explain](#how-the-bottom-line-chooses-what-to-explain)
  - [Reading the numbers together: three verified examples](#reading-the-numbers-together-three-verified-examples)
- [Reading %B and Bandwidth together](#reading-b-and-bandwidth-together)
  - [Bullish, bearish and potential failed-release comparison](#bullish-bearish-and-potential-failed-release-comparison)
- [Bollinger Pattern Reference — Complete Interpretations](#bollinger-pattern-reference-complete-interpretations)
  - [Compression and setup patterns](#compression-and-setup-patterns)
  - [Bullish price-action patterns](#bullish-price-action-patterns)
  - [Bearish price-action patterns](#bearish-price-action-patterns)
  - [Volatility development patterns](#volatility-development-patterns)
  - [Ordinary and lower-priority combinations](#ordinary-and-lower-priority-combinations)
  - [Verified Bollinger examples](#verified-bollinger-examples)
- [Strengths & Weaknesses (BB)](#strengths-weaknesses-bb)
- [Notes: Bollinger Bands](#notes-bollinger-bands)
  - [101](#101)
  - [Parameter Settings](#parameter-settings)
- [Bollinger 101](#bollinger-101)
  - [%B (The Position/Overbought-Oversold Gauge)](#b-the-positionoverbought-oversold-gauge)
  - [Bollinger Bandwidth (The Volatility Gauge)](#bollinger-bandwidth-the-volatility-gauge)
  - [How Are They Used Together?](#how-are-they-used-together)
  - [Executing the Trade: Trigger vs. Fakeout](#executing-the-trade-trigger-vs-fakeout)