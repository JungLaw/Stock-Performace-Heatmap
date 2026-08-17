## Summary: Bollinger %B signals

The TA Rule Engine uses Bollinger `%B` as a **current-location contrarian / exhaustion measure**.

In simple terms:

- Low `%B` readings mean price is near or below the lower Bollinger Band.
- High `%B` readings mean price is near or above the upper Bollinger Band.
- The farther price stretches beyond a band, the stronger the project's exhaustion signal becomes.
- A Buy or Sell label describes **how stretched price currently is**. It does **not** mean that a reversal has already occurred or is guaranteed to occur.

The table below uses the balanced `BB(20,2.0)` medium-term setting as the main example.

| Signal | Literal trigger | Layman’s Translation | Rule Logic | Bottom-line |
| --- | --- | --- | --- | --- |
| `strong_buy` | `%B < -10` | Price is materially below the lower Bollinger Band. | The current price has stretched far enough below the lower band to qualify as an unusually deep downside extension. | Price is exceptionally stretched below its Bollinger envelope. |
| `buy` | `-10 <= %B < 10` | Price is near the lower band or modestly below it. | Price is in the project's lower-band exhaustion zone, but the stretch is not deep enough to qualify as Strong Buy. | Price is trading near the low side of its Bollinger envelope. |
| `neutral` | `10 <= %B <= 90` | Price is comfortably inside the bands and away from either exhaustion zone. | `%B` is inside the project's middle / Neutral zone. | Price is not currently stretched toward either Bollinger extreme. |
| `sell` | `90 < %B <= 110` | Price is near the upper band or modestly above it. | Price is in the project's upper-band exhaustion zone, but the stretch is not large enough to qualify as Strong Sell. | Price is trading near the high side of its Bollinger envelope. |
| `strong_sell` | `%B > 110` | Price is materially above the upper Bollinger Band. | The current price has stretched far enough above the upper band to qualify as an unusually large upside extension. | Price is exceptionally stretched above its Bollinger envelope. |

> **Important:** These are the medium-term `BB(20,2.0)` thresholds. The short- and long-term Bollinger settings use the same `10–90` Neutral zone but different Strong thresholds because their band configurations behave differently.

The three configured `%B` views are:

| Horizon | Bollinger setting | Strong Buy | Buy | Neutral | Sell | Strong Sell |
| --- | --- | --- | --- | --- | --- | --- |
| Short term | `BB(10,1.5)` | `%B < -20` | `-20 <= %B < 10` | `10 <= %B <= 90` | `90 < %B <= 120` | `%B > 120` |
| Medium term | `BB(20,2.0)` | `%B < -10` | `-10 <= %B < 10` | `10 <= %B <= 90` | `90 < %B <= 110` | `%B > 110` |
| Long term | `BB(50,2.5)` | `%B < 0` | `0 <= %B < 10` | `10 <= %B <= 90` | `90 < %B <= 100` | `%B > 100` |

These thresholds are **project-specific calibrations**, not universal Bollinger rules.

---

## How to read the Bollinger heatmap

The Bollinger family appears in the heatmaps as paired `%B` and Bandwidth rows for the short-, medium-, and long-term settings.

Conceptually:

```text
BB %B(ST)          → Where is price in BB(10,1.5)?
BB Bandwidth(ST)   → How wide is BB(10,1.5)?

BB %B              → Where is price in BB(20,2.0)?
BB Bandwidth       → How wide is BB(20,2.0)?

BB %B(LT)          → Where is price in BB(50,2.5)?
BB Bandwidth(LT)   → How wide is BB(50,2.5)?
```

### Reading a `%B` cell

For a `%B` row, the **number printed in the cell is the displayed `%B` value**.

For example:

```text
93.4
```

means:

> Price is located near the upper Bollinger Band.

For the medium-term `BB(20,2.0)` setting:

```text
90 < %B <= 110
```

is classified as:

```text
Sell
```

So:

```text
%B = 93.4
Signal = Sell
```

means:

> Price is currently stretched toward the upper side of its medium-term Bollinger envelope, but not far enough beyond it to qualify as Strong Sell.

The **cell color comes from the `%B` score**, not from Bandwidth.

The `%B` hover also provides the matching Bollinger volatility context:

```text
Bandwidth
Volatility State
Bandwidth Direction
```

Those fields help explain the environment surrounding the `%B` reading, but they do not alter the `%B` signal.

For example:

```text
%B: 93.4
Bandwidth: 5.32
Volatility State: Expanded
Bandwidth Direction: Expanding
Signal: Sell
```

can be read as:

> Price is near the upper side of the Bollinger envelope and therefore receives a Sell exhaustion label. At the same time, the bands are wider than usual and are widening further.

The Sell label comes from `%B = 93.4`.

The Bandwidth information is additional volatility context.

### Reading a Bandwidth cell

For a `BB Bandwidth` row, the printed number tells you **how wide the current Bollinger envelope is relative to its middle band**.

For example:

```text
Bandwidth = 4.22
```

means the total upper-to-lower band width is approximately `4.22%` of the middle-band level.

The important difference is that Bandwidth is **not given a bullish or bearish trading direction**.

A valid Bandwidth row therefore retains:

```text
Signal: Neutral
Score: 0
```

Its useful interpretation comes from the additional hover fields:

```text
Volatility State
Bandwidth Direction
```

So a Bandwidth cell should be read as:

```text
Value
+ State
+ Direction
```

rather than:

```text
Value
+ Buy/Sell direction
```

### A simple example

Suppose a hover shows:

```text
%B: 93.4
Bandwidth: 5.32
Volatility State: Expanded
Bandwidth Direction: Expanding
Signal: Sell
```

Read it as three independent questions: `%B = 93.4` means price is near the upper band; `Expanded` means the bands are wider than usual; `Expanding` means they are widening further. The Sell label comes from `%B`. The Bandwidth fields describe the volatility environment and do not guarantee the next price move.

## Bollinger Bands / %B / Bandwidth — brief overview

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

### `%B` — where is price relative to the bands?

Bollinger `%B` converts the current price's location relative to the bands into a standardized position measure.

Conceptually:

```text
%B = (Price - Lower Band)
     --------------------
     (Upper Band - Lower Band)
```

The calculation is stored internally as a fraction, but the heatmaps multiply it by `100` for readability.

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

| Displayed `%B` | Physical meaning |
| --- | --- |
| `< 0` | Price is below the lower band |
| `0` | Price is at the lower band |
| `50` | Price is at the middle band |
| `100` | Price is at the upper band |
| `> 100` | Price is above the upper band |

Unlike an oscillator that is permanently bounded between `0` and `100`, `%B` can legitimately move below `0` or above `100`.

That is not an error. It means price has moved outside the Bollinger envelope.

### Bandwidth — how wide are the bands?

Bollinger Bandwidth measures the total distance between the upper and lower bands relative to the middle band.

Conceptually:

```text
Bandwidth = (Upper Band - Lower Band)
            -------------------------
                  Middle Band
```

Like `%B`, the project stores Bandwidth internally as a fraction and multiplies it by `100` for display.

For example:

```text
Raw Bandwidth     Displayed Bandwidth

0.0422       →          4.22
0.1800       →         18.00
```

A larger Bandwidth means the Bollinger envelope is wider.

A smaller Bandwidth means the envelope is narrower.

But **Bandwidth alone says nothing about whether price is bullish or bearish**.

That distinction is fundamental to how this project treats the Bollinger family.

### Value-added use

Price alone tells you:

> **“What is the stock trading at?”**

Bollinger-derived measures add two kinds of relative context.

`%B` asks:

> **“Where is that price relative to its current Bollinger envelope?”**

Bandwidth asks:

> **“How wide is that envelope?”**

The project then adds two more Bandwidth descriptors:

- **Volatility State** — how unusual the current width is compared with the stock's own recent history.
- **Bandwidth Direction** — whether that width is currently expanding, contracting, or remaining roughly stable.

This matters because the same `%B` reading can occur under very different volatility conditions.

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

It does **not** change the `%B` score.

### Use with

Bollinger `%B` and Bandwidth are most useful when treated as pieces of a larger technical picture rather than as standalone forecasts.

- **SMA / EMA** — provide trend direction and help distinguish a Bollinger extreme occurring with or against the broader price trend.
- **ADX** — helps show whether a strong trend is present. This is useful because price can remain near an outer Bollinger Band during a persistent trend.
- **RSI / Stochastic / Williams %R / MFI** — provide independent evidence about momentum or range-position extremes.
- **ROC / MACD** — help show whether momentum is strengthening or weakening while price is near a Bollinger extreme.
- **CMF / OBV / volume measures** — add participation or buying/selling-pressure context.

None of these companion indicators is required by the Bollinger scoring rules.

They provide context; they do not silently become additional `%B` rule conditions.

> **Tip:** > Never use Bollinger Bands in isolation for a dashboard. Pair them with a non-correlated volume indicator (like MFI or On-Balance Volume).
> - If price hits the Upper Band (%B > 1.0) but volume is drying up, that "breakout" is likely a trap.
  

### Important distinction

The project deliberately separates **price-location semantics** from **volatility semantics**.

```text
%B
→ directional / exhaustion interpretation
→ Strong Buy / Buy / Neutral / Sell / Strong Sell
→ drives the heatmap score and color

BB Bandwidth
→ nondirectional volatility interpretation
→ canonical directional score remains Neutral / 0
→ volatility meaning is carried separately through State and Direction
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

The `%B` score describes the **current degree of price stretch** under the project's contrarian model.

Bandwidth describes the **current volatility environment**.

---

## The three questions behind the Bollinger rows

The easiest way to understand the project's Bollinger implementation is to separate it into three independent questions.

| Question | Project output | What it means |
| --- | --- | --- |
| **Where is price relative to the bands?** | `%B` | Shows whether price is near the lower band, near the middle, near the upper band, or outside the envelope. |
| **How unusual is the current Bandwidth?** | `Volatility State` | Compares the current band width with this stock's own recent Bandwidth history. |
| **Is that Bandwidth changing?** | `Bandwidth Direction` | Shows whether the bands are currently widening, narrowing, or changing too little to count as meaningfully different. |

A useful shorthand is:

```text
%B
= Where is price?

Volatility State
= How unusual is the current width?

Bandwidth Direction
= What is that width doing now?
```

The second and third questions describe **volatility**, not price direction.

For example:

```text
Volatility State: Expanded
Bandwidth Direction: Expanding
```

does not mean:

```text
"Price is bullish."
```

It means:

```text
"The bands are already wider than usual,
and they are getting wider still."
```

---

## BB %B Rule Translation

The project uses `%B` as a **current-location contrarian / exhaustion measure**. The signal depends on where price is now relative to the Bollinger envelope; reversal, crossback, persistence, Bandwidth confirmation, and other indicators are not required by the score. The balanced `BB(20,2.0)` setting is used below as the detailed example.

### Strong Buy

**Rule:** `%B < -10` (`pct_b < -0.10` internally)

Price is materially below the lower `BB(20,2.0)` band. The project treats this as unusually severe downside stretch and assigns **Strong Buy (+2)**. It describes current exhaustion; it does not mean a rebound has already begun.

**Bottom-line:** Exceptional downside extension relative to the MT Bollinger envelope.

### Buy

**Rule:** `-10 <= %B < 10`

Price is near the lower band or modestly below it. This is the project's lower-edge exhaustion zone and receives **Buy (+1)**. An actual band breach is not required.

**Bottom-line:** Price is stretched toward the low side of the MT envelope, but not enough for Strong Buy.

### Neutral

**Rule:** `10 <= %B <= 90`

Price is comfortably away from either exhaustion edge and receives **Neutral (0)**. Neutral does not mean price is exactly at the middle band; `%B = 30` and `%B = 75` are both Neutral because neither is close enough to an outer edge.

**Bottom-line:** No meaningful Bollinger-edge exhaustion signal.

### Sell

**Rule:** `90 < %B <= 110`

Price is near the upper band or modestly above it. This is the project's upper-edge exhaustion zone and receives **Sell (-1)**. Price can remain near an upper band during a strong trend, so this is not a confirmed reversal call.

**Bottom-line:** Price is stretched toward the high side of the MT envelope, but not enough for Strong Sell.

### Strong Sell

**Rule:** `%B > 110` (`pct_b > 1.10` internally)

Price is materially above the upper `BB(20,2.0)` band. The project treats this as unusually severe upside stretch and assigns **Strong Sell (-2)**. It identifies exceptional extension, not a guaranteed immediate decline.

**Bottom-line:** Exceptional upside extension relative to the MT Bollinger envelope.

## Industry-standard baseline

Classic Bollinger interpretation treats the bands as relative definitions of high and low, `%B` as price location relative to the bands, and Bandwidth as normalized band width. A common reference construction is a 20-period middle band with upper/lower bands two standard deviations away.

The physical `%B` landmarks are `0` = lower band, `50` = middle band, and `100` = upper band; values outside `0–100` mean price is outside the envelope. These measurements do **not** inherently prescribe a contrarian trading rule: high `%B` can represent strength, continuation, overextension, or reversal context depending on the method.

Bandwidth likewise describes volatility magnitude: narrow bands indicate more compressed volatility and wide bands more expanded volatility. It does not inherently say Buy, Sell, bullish, or bearish. A band touch or breach is therefore not automatically a standalone trading signal.

## How the TA Rule Engine extends the classic baseline

The project keeps the classic physical meaning of `%B` and Bandwidth but adds explicit application semantics:

- **`%B`:** current-location contrarian / exhaustion scoring. Lower-edge stretch maps to Buy-side exhaustion; upper-edge stretch maps to Sell-side exhaustion. This is a project choice, not a universal Bollinger rule.
- **BB_BW:** remains directional-neutral (`Neutral / 0`) and is enriched with **Volatility State** and **Bandwidth Direction**. The percentile boundaries, lookbacks, and Stable tolerances are project-specific calibrations.

## Why Strong thresholds differ by horizon

A band touch or breach is not equally unusual across all three Bollinger settings. `BB(10,1.5)` is faster and tighter, so price crosses its bands more often; `BB(50,2.5)` is slower and wider, so an actual band breach is already comparatively unusual.

The project therefore keeps the ordinary exhaustion boundaries common at `%B < 10` and `%B > 90`, while calibrating Strong thresholds by horizon:

```text
ST  BB(10,1.5):  Strong Buy < -20 | Strong Sell > 120
MT  BB(20,2.0):  Strong Buy < -10 | Strong Sell > 110
LT  BB(50,2.5):  Strong Buy <   0 | Strong Sell > 100
```

These are project-specific calibrations, not universal Bollinger rules.

## Comparison of the three Bollinger settings

The project uses three Bollinger configurations to capture different horizons.

| Setting | Horizon | Responsiveness | Band characteristics | Ordinary exhaustion zone | Strong Buy / Sell | Main trade-off |
| --- | --- | --- | --- | --- | --- | --- |
| `BB(10,1.5)` | Short term | Fastest | Short lookback and tightest band multiplier; reacts quickly and is breached more often. | `<10` / `>90` | `<-20` / `>120` | Most responsive, but ordinary band breaches are less exceptional. |
| `BB(20,2.0)` | Medium term | Balanced | Classic-style balanced configuration. | `<10` / `>90` | `<-10` / `>110` | Good balance between responsiveness and selectivity. |
| `BB(50,2.5)` | Long term | Slowest | Longer lookback and widest multiplier; responds more slowly and is harder to breach. | `<10` / `>90` | `<0` / `>100` | Most selective; actual band breaches are already unusual. |

### Practical selection guide

- **`BB(10,1.5)` — ST:** fastest and most sensitive; useful for short-term stretch.
- **`BB(20,2.0)` — MT:** balanced/default view; closest to the classic 20/2 reference.
- **`BB(50,2.5)` — LT:** slowest and most selective; useful for structural stretch.

Treat the three settings as **different horizon lenses, not three votes**. A stock can be Neutral on ST while Sell or Strong Sell on LT because each envelope measures relative location over a different horizon.

## BB(10,1.5) %B Rules interpretation

| Source | Signal | Rule logic | What’s happening | Answers the question | Bottom-line |
| --- | --- | --- | --- | --- | --- |
| `BB %B(ST)` | Strong Buy | `%B < -20` | Price is deeply below the tight short-term lower band. | Is the current downside stretch exceptional even for the highly responsive ST envelope? | Exceptional ST downside exhaustion. |
| `BB %B(ST)` | Buy | `-20 <= %B < 10` | Price is close to or moderately below the lower ST band. | Is price stretched toward the lower short-term edge? | ST lower-edge exhaustion. |
| `BB %B(ST)` | Neutral | `10 <= %B <= 90` | Price is away from both short-term exhaustion zones. | Is price sufficiently inside the ST envelope to avoid an edge signal? | No ST exhaustion signal. |
| `BB %B(ST)` | Sell | `90 < %B <= 120` | Price is close to or moderately above the upper ST band. | Is price stretched toward the upper short-term edge? | ST upper-edge exhaustion. |
| `BB %B(ST)` | Strong Sell | `%B > 120` | Price is deeply above the tight short-term upper band. | Is the current upside stretch exceptional even for the responsive ST envelope? | Exceptional ST upside exhaustion. |

Because `BB(10,1.5)` is the fastest and tightest configuration, excursions outside its bands are relatively common. Therefore `%B > 100` alone is **not** Strong Sell, and `%B < 0` alone is **not** Strong Buy. The stronger `-20 / 120` boundaries keep Strong states selective.

---

## BB(20,2.0) %B Rules interpretation

| Source | Signal | Rule logic | What’s happening | Answers the question | Bottom-line |
| --- | --- | --- | --- | --- | --- |
| `BB %B` | Strong Buy | `%B < -10` | Price is materially below the medium-term lower band. | Is downside stretch unusually severe for the balanced envelope? | Exceptional MT downside exhaustion. |
| `BB %B` | Buy | `-10 <= %B < 10` | Price is near or modestly below the lower band. | Is price stretched toward the medium-term lower edge? | MT lower-edge exhaustion. |
| `BB %B` | Neutral | `10 <= %B <= 90` | Price is comfortably away from either MT edge. | Is price inside the non-exhaustion portion of the envelope? | No MT exhaustion signal. |
| `BB %B` | Sell | `90 < %B <= 110` | Price is near or modestly above the upper band. | Is price stretched toward the medium-term upper edge? | MT upper-edge exhaustion. |
| `BB %B` | Strong Sell | `%B > 110` | Price is materially above the medium-term upper band. | Is upside stretch unusually severe for the balanced envelope? | Exceptional MT upside exhaustion. |

`BB(20,2.0)` is the project's balanced Bollinger configuration. Its Strong thresholds sit between the ST and LT calibrations:

```text
ST  → -20 / 120
MT  → -10 / 110
LT  →   0 / 100
```

---

## BB(50,2.5) %B Rules interpretation

| Source | Signal | Rule logic | What’s happening | Answers the question | Bottom-line |
| --- | --- | --- | --- | --- | --- |
| `BB %B(LT)` | Strong Buy | `%B < 0` | Price is below the wide long-term lower band. | Has price actually breached an already-selective LT lower envelope? | Exceptional LT downside exhaustion. |
| `BB %B(LT)` | Buy | `0 <= %B < 10` | Price is inside the envelope but very near the lower band. | Is price stretched toward the LT lower edge without an actual breach? | LT lower-edge exhaustion. |
| `BB %B(LT)` | Neutral | `10 <= %B <= 90` | Price is away from both LT extremes. | Is price inside the central long-term envelope? | No LT exhaustion signal. |
| `BB %B(LT)` | Sell | `90 < %B <= 100` | Price is inside the envelope but very near the upper band. | Is price stretched toward the LT upper edge without an actual breach? | LT upper-edge exhaustion. |
| `BB %B(LT)` | Strong Sell | `%B > 100` | Price is above the wide long-term upper band. | Has price actually breached an already-selective LT upper envelope? | Exceptional LT upside exhaustion. |

`BB(50,2.5)` is both slower and wider. An actual band breach is sufficiently uncommon that the breach itself marks the Strong boundary.

---

## Project %B rules — consolidated reference

| Horizon | Strong Buy | Buy | Neutral | Sell | Strong Sell |
| --- | --- | --- | --- | --- | --- |
| ST `BB(10,1.5)` | `< -20` | `-20 to <10` | `10 to 90` | `>90 to 120` | `>120` |
| MT `BB(20,2.0)` | `< -10` | `-10 to <10` | `10 to 90` | `>90 to 110` | `>110` |
| LT `BB(50,2.5)` | `<0` | `0 to <10` | `10 to 90` | `>90 to 100` | `>100` |

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

If `%B` is not yet numerically initialized:

```text
%B = missing
```

then:

```text
Signal = missing
Score  = missing
```

The project does **not** convert unavailable Bollinger observations into synthetic Neutral readings.

### What the `%B` score uses

The score uses **current `%B` location only**. Bandwidth value, Volatility State, Bandwidth Direction, reversal/crossback confirmation, persistence, and other indicators remain context rather than hidden scoring conditions.

## Understanding Bollinger Bandwidth

One important consequence of `%B` being a location measure is that the same `%B` can occur in very different volatility environments. `%B = 95` always means price is near the upper band, but the bands themselves may be exceptionally narrow, ordinary, or exceptionally wide. Bandwidth provides that missing volatility context.

Bollinger Bandwidth answers a different question:

> **How wide is the Bollinger envelope?**

Its conceptual formula is:

```text
Bandwidth = (Upper Band - Lower Band)
            -------------------------
                  Middle Band
```

The project stores Bandwidth as a fraction and displays it as `×100`.

For example:

```text
Raw BB_BW = 0.0472
Displayed = 4.72
```

means:

> The total distance from the lower band to the upper band is approximately 4.72% of the middle-band level.

### Why the Bandwidth number alone is not enough

A Bandwidth of `5.00` might be unusually narrow for one stock and completely ordinary for another.

Likewise, `15.00` might be extremely wide for one security but routine for a more volatile security.

Therefore the project does **not** use universal absolute Bandwidth cutoffs. Instead, it asks:

> **Where does the current Bandwidth rank relative to this instrument's own recent Bandwidth history?**

That produces the project's `Volatility State`.

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
Volatility State
Bandwidth Direction
```

---

## Volatility State

`Volatility State` describes:

> **How unusual is the current Bandwidth compared with this stock's own recent Bandwidth history?**

The project uses five states:

```text
Very Compressed
Compressed
Normal
Expanded
Very Expanded
```

### Beginner interpretation

| State | Beginner meaning |
| --- | --- |
| **Very Compressed** | Bands are exceptionally narrow compared with this stock’s recent history. |
| **Compressed** | Bands are narrower than usual. |
| **Normal** | Band width is around its typical historical range. |
| **Expanded** | Bands are wider than usual. |
| **Very Expanded** | Bands are exceptionally wide compared with recent history. |

The key phrase is **compared with this stock's recent history**.

`Very Expanded` does not mean “this stock has wider bands than every other stock.” It means “this stock's current bands are exceptionally wide relative to the Bandwidth levels it has recently experienced.”

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
Map percentile into one of five Volatility States
```

For example, a current percentile at the `97th percentile` means current Bandwidth is wider than approximately 97% of the Bandwidth observations in the relevant reference history. That qualifies as `Very Expanded` under the MT/LT calibration.

### Volatility State calibration by horizon

| Horizon | Setting | Reference history | Very Compressed | Compressed | Normal | Expanded | Very Expanded |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| ST | `BB(10,1.5)` | 60 observations | `<10th` | `10th–<25th` | `25th–75th` | `>75th–90th` | `>90th` |
| MT | `BB(20,2.0)` | 120 observations | `<5th` | `5th–<15th` | `15th–85th` | `>85th–95th` | `>95th` |
| LT | `BB(50,2.5)` | 120 observations | `<5th` | `5th–<15th` | `15th–85th` | `>85th–95th` | `>95th` |

ST uses a shorter, more responsive reference history; MT/LT use a longer, more stable one. The outer percentile boundaries are also more selective for MT/LT. These are project-specific production calibrations, not textbook Bollinger settings.

### Warmup behavior

Volatility State requires enough initialized Bandwidth history to fill its historical reference window.

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
Volatility State becomes available
```

Before that reference history is available:

```text
Volatility State = missing
```

The project does not manufacture a `Normal` state for an observation that lacks enough historical context.

---

## Bandwidth Direction

`Bandwidth Direction` answers:

> **Is the Bollinger envelope getting wider, getting narrower, or changing too little to count as materially different?**

The possible outputs are:

```text
Expanding
Contracting
Stable
```

### Beginner interpretation

| Direction | Beginner meaning |
| --- | --- |
| **Expanding** | Bands are getting wider. |
| **Contracting** | Bands are getting narrower. |
| **Stable** | Band width has not changed enough to count as meaningfully wider or narrower. |

This is separate from `Volatility State`.

A stock can have `Very Compressed + Expanding` because its bands can still be exceptionally narrow **while beginning to widen**.

Likewise, `Very Expanded + Contracting` means bands can still be exceptionally wide **while beginning to narrow**.

### How Bandwidth Direction is calculated

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

Equality at either tolerance boundary is intentionally classified as `Stable`.

### Bandwidth Direction tolerance by horizon

| Horizon | Setting | Stable tolerance |
| --- | --- | ---: |
| ST | `BB(10,1.5)` | `±3.0%` |
| MT | `BB(20,2.0)` | `±2.0%` |
| LT | `BB(50,2.5)` | `±0.5%` |

Daily Bandwidth movement naturally becomes smaller as the Bollinger horizon slows, so each horizon uses a different tolerance. A change outside the tolerance is Expanding or Contracting; a change inside it—or exactly on either boundary—is Stable.

Example for ST: `+4.2%` → Expanding, `-4.0%` → Contracting, `+1.8%` or exactly `±3.0%` → Stable.

### Direction warmup

Bandwidth Direction requires:

```text
current Bandwidth
+
prior Bandwidth
```

If either observation is unavailable:

```text
Bandwidth Direction = missing
```

The system does not label the first initialized observation as `Stable` merely because no comparison exists.

---

## Reading Volatility State + Bandwidth Direction together

This is where the two Bandwidth descriptors become substantially more useful.

A simple way to remember the distinction is:

```text
Volatility State
= Where is Bandwidth relative to its recent history?

Bandwidth Direction
= What is Bandwidth doing right now?
```

Or, even more simply:

```text
State     = current regime
Direction = current movement
```

Neither replaces the other.

### Example 1 — Very Compressed + Stable

```text
Volatility State: Very Compressed
Bandwidth Direction: Stable
```

> **Bands are extremely narrow and staying that way.**

Interpretation:

- current volatility is unusually compressed;
- there is not yet enough widening or narrowing to classify the envelope as moving materially.

This identifies a very quiet volatility regime. It does **not** predict whether the eventual price move will be upward or downward.

### Example 2 — Compressed + Expanding

```text
Volatility State: Compressed
Bandwidth Direction: Expanding
```

> **Bands are still narrow, but volatility is beginning to increase.**

Interpretation:

- Bandwidth remains below its normal historical range;
- the envelope is now widening enough to register an increase.

### Example 3 — Normal + Contracting

```text
Volatility State: Normal
Bandwidth Direction: Contracting
```

> **Band width is still around normal, but it is narrowing.**

Interpretation:

- current Bandwidth has not yet moved into the project's Compressed zone;
- nevertheless, recent movement is toward narrower bands.

If contraction continues, a later observation may eventually transition from `Normal → Compressed → Very Compressed`, but that transition is not assumed in advance.

### Example 4 — Expanded + Expanding

```text
Volatility State: Expanded
Bandwidth Direction: Expanding
```

> **Bands are already wider than usual and are getting wider still.**

Interpretation:

- volatility is already elevated relative to recent history;
- the envelope is widening further.

`Expanding` does not tell us whether price itself is moving higher or lower. It tells us that the **magnitude of the Bollinger envelope is increasing**.

### Example 5 — Very Expanded + Contracting

```text
Volatility State: Very Expanded
Bandwidth Direction: Contracting
```

> **Bands remain extremely wide, but volatility is beginning to cool.**

Interpretation:

- Bandwidth remains at an exceptional historical level;
- the latest movement is toward a narrower envelope.

A useful distinction is:

```text
Contracting
≠ Compressed
```

The bands can be contracting while still being extremely wide.

### Additional State + Direction combinations

| State | Direction | Beginner interpretation |
| --- | --- | --- |
| Very Compressed | Expanding | Bands are exceptionally narrow, but beginning to widen. |
| Very Compressed | Contracting | Bands are already exceptionally narrow and are narrowing further. |
| Compressed | Stable | Bands are narrower than usual and little changed. |
| Compressed | Contracting | Bands are narrower than usual and becoming narrower still. |
| Normal | Expanding | Band width is around normal but is beginning to widen. |
| Normal | Stable | Band width is around its normal historical range and little changed. |
| Expanded | Stable | Bands are wider than usual but are not changing materially. |
| Expanded | Contracting | Bands are wider than usual but beginning to narrow. |
| Very Expanded | Expanding | Bands are exceptionally wide and widening further. |
| Very Expanded | Stable | Bands are exceptionally wide and remaining that way. |

These combinations describe **volatility behavior only**. They do not create additional Buy/Sell scores.

### Why State and Direction can appear to disagree

A common beginner question is:

> “How can Bandwidth be `Very Expanded` and `Contracting` at the same time?”

There is no contradiction.

Consider Bandwidth moving like this:

```text
18.0
17.2
16.3
```

Suppose recent historical Bandwidth is normally much lower.

Even after falling from `18.0 → 16.3`, the current `16.3` may still rank above the 95th percentile of recent history.

Therefore:

```text
Volatility State: Very Expanded
```

because the **level is still extremely high**.

At the same time:

```text
Bandwidth Direction: Contracting
```

because the **latest movement is downward**.

The two fields use different frames of reference:

```text
State
→ level relative to history

Direction
→ current change relative to prior observation
```

This distinction is central to reading the Bandwidth model correctly.

---

## Reading %B and Bandwidth together

The `%B` hover intentionally brings the matching Bandwidth context into the same view.

That lets the user answer all three Bollinger questions without moving between rows:

```text
%B
→ Where is price?

Volatility State
→ How unusual is current Bandwidth?

Bandwidth Direction
→ Is Bandwidth widening, narrowing, or stable?
```

Bandwidth context is explanatory. It does **not** become an additional `%B` scoring clause.

### Joint-reading examples

```text
%B: 94 | State: Normal | Direction: Stable | Signal: Sell
```
Price is stretched toward the upper edge while volatility remains ordinary and little changed. The Sell signal comes from `%B`, not from the Bandwidth context.

```text
%B: 116 | State: Very Expanded | Direction: Contracting | Signal: Strong Sell
```
Price is exceptionally stretched above the MT envelope; volatility remains exceptionally elevated but is beginning to cool. Contraction did not cause the Strong Sell classification.

```text
%B: 4 | State: Compressed | Direction: Expanding | Signal: Buy
```
Price is near the lower edge while the envelope is still narrower than usual but beginning to widen. `Expanding` describes volatility, not bullish price direction.

### Compact joint-reading matrix

| `%B` condition | Bandwidth context | Combined interpretation |
| --- | --- | --- |
| Low `%B` | Very Compressed + Stable | Price is near the lower edge during an exceptionally quiet volatility regime. |
| Low `%B` | Compressed + Expanding | Price is near the lower edge while previously quiet volatility begins to increase. |
| Low `%B` | Very Expanded + Expanding | Price is deeply stretched low during an already extreme and worsening volatility expansion. |
| High `%B` | Normal + Stable | Price is near the upper edge in an otherwise ordinary volatility environment. |
| High `%B` | Expanded + Expanding | Price is stretched high while volatility is elevated and increasing. |
| High `%B` | Very Expanded + Contracting | Price remains highly stretched while unusually high volatility begins to cool. |
| Neutral `%B` | Very Compressed + Stable | Price is not near either edge, but the volatility envelope is exceptionally quiet. |
| Neutral `%B` | Expanded + Contracting | Price location is ordinary while elevated volatility begins to subside. |

These are **interpretation combinations**, not new rule combinations.

There is no hidden logic such as:

```text
%B > 90
AND Bandwidth Expanding
→ Strong Sell
```

or:

```text
%B < 10
AND Very Compressed
→ Strong Buy
```

unless the scoring model is explicitly reopened in a later project stage.

---

## Strengths of the Bollinger implementation

- **Normalized location:** `%B` expresses price position relative to the envelope rather than in raw dollars.
- **Volatility separated from direction:** BB_BW remains nondirectional while `%B` carries the exhaustion score.
- **Instrument-relative State:** Volatility State compares Bandwidth with the same security's own recent history instead of using one absolute cutoff for every ticker.
- **Level separated from movement:** State says how unusual the current width is; Direction says whether that width is widening or narrowing now.
- **Multiple horizons:** ST, MT, and LT provide fast, balanced, and structural views of the same Bollinger framework.

## Limitations and interpretation risks

- **Extremes can persist:** Buy/Sell exhaustion labels do not guarantee an immediate reversal, especially during strong trends.
- **`%B` is a location measure first:** the contrarian interpretation is a project choice; other legitimate systems may use `%B` differently.
- **Bandwidth does not predict breakout direction:** compression or expansion describes volatility, not whether price will move up or down.
- **Volatility State is history-dependent:** `Normal` means normal relative to the configured recent history, not an absolute universal volatility level.
- **ST / MT / LT are not votes:** they are different horizon lenses.
- **Thresholds are empirical project calibrations:** `%B` boundaries, Bandwidth percentile cutoffs, lookbacks, and Direction tolerances are not universal Bollinger constants.

## Notes: Bollinger Bands

**Purpose:** `%B` measures price location/stretch; BB_BW measures envelope width. Volatility State says how unusual that width is relative to recent history, and Bandwidth Direction says whether it is widening, narrowing, or stable.

**Configured variants:** `BB(10,1.5)` ST, `BB(20,2.0)` MT, `BB(50,2.5)` LT.

**Quick `%B` landmarks:** `0` = lower band, `50` = middle band, `100` = upper band; values can move below `0` or above `100`.

**BB_BW score:** valid Bandwidth remains `Neutral / 0` because it measures volatility rather than bullish/bearish direction.

**Key caution:** `%B` extreme ≠ guaranteed reversal; compressed/expanded/expanding/contracting Bandwidth ≠ bullish/bearish direction.

### 101

#### Purpose

Bollinger Bands provide a volatility-adjusted envelope around price. The project uses that envelope to answer three questions:

```text
%B                  = Where is price?
Volatility State    = How unusual is current Bandwidth?
Bandwidth Direction = Is Bandwidth widening, narrowing, or stable?
```

#### Key components

- **Middle Band:** moving-average center.
- **Upper / Lower Bands:** volatility-adjusted boundaries.
- **`%B`:** price position within or beyond the bands.
- **Bandwidth:** total envelope width relative to the middle band.

#### Quick guides

```text
%B: 0 = lower band | 50 = middle | 100 = upper band

Volatility State:
Very Compressed → exceptionally narrow vs recent history
Compressed      → narrower than usual
Normal          → around the typical recent range
Expanded        → wider than usual
Very Expanded   → exceptionally wide vs recent history

Bandwidth Direction:
Expanding   → getting wider
Contracting → getting narrower
Stable      → change is too small to count as meaningfully wider/narrower
```

#### Use with

Useful companions include SMA/EMA for trend, ADX for trend strength, RSI/Stochastic/Williams %R/MFI for independent stretch or momentum context, ROC/MACD for momentum change, and volume/CMF/OBV for participation. None is required by the Bollinger score.

#### Primary limitation

Bollinger measurements describe **current relative conditions**. Read `%B` as price location/stretch and Bandwidth as volatility context; neither guarantees the next price move.


---

## Old Notes
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


**`BB (10, 1.5)`**: 
- The "Front-Run" Band. 
- This is very tight. Price will hug or pierce these bands constantly. 
- This acts as an ***"early warning system"***. 
    - It tells you when a micro-trend is accelerating before the standard bands even react.

**`BB (20, 2.0)`**: 
- The "Standard" Band. 
- This is the ***'baseline'***. 
- Represents the "normal" distribution of price for a swing trader.

**`BB (50, 2.5)`**: 
- The "Institutional" Band. 
- By moving to 2.5 standard deviations and 50 periods, you're looking for tail-risk events. 
- When price touches the 50/2.5 band, it’s a "3-sigma" style event—meaning the move is statistically significant and likely driven by high-conviction institutional flow.