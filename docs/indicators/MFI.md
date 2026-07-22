## Summary: MFI Signals

The Money Flow Index, or MFI, is a volume-weighted momentum oscillator that measures the balance between positive and negative money flow over a selected lookback period.

The project computes and scores three MFI variants:
- `MFI_10` — short-term and most responsive
- `MFI_14` — standard reference period
- `MFI_30` — longer-term and more smoothed

All three variants use the same persistent five-state scoring model:

| MFI state | Signal | Score |
|---|---|---:|
| `MFI <= 15` | Strong Buy | `+2` |
| `MFI > 15 and MFI <= 25` | Buy | `+1` |
| `MFI > 25 and MFI < 75` | Neutral | `0` |
| `MFI >= 75 and MFI < 85` | Sell | `-1` |
| `MFI >= 85` | Strong Sell | `-2` |

These signals describe the current MFI state. They do not require a threshold crossing, reversal confirmation, prior-bar confirmation, price-direction filter, or divergence signal.


## Key Points
> Positive Money Flow: ***Price goes up + Volume is heavy = Cash is flowing in***.
> Negative Money Flow: ***Price goes down + Volume is heavy = Cash is flowing out***

- If the "Inflow Days" (+MF) have drastically higher volume than the "Outflow Days" (-MF), the MFI score pushes toward 100. 
- If the "Outflow Days" (-MF) dominate, the score drops toward 0.


---

## Indicator overview

MFI combines price and trading volume into an oscillator bounded between `0` and `100`.

Its purpose is to estimate whether recent trading activity reflects stronger buying pressure or stronger selling pressure.

The calculation begins with typical price:

```text
Typical Price = (High + Low + Close) / 3
```

Raw money flow is then calculated as:

```text
Raw Money Flow = Typical Price × Volume
```

Each period is classified as positive or negative money flow depending on whether typical price increased or decreased relative to the prior period.

Over the selected lookback:

```text
Money Flow Ratio =
Sum of Positive Money Flow
/
Sum of Negative Money Flow
```

MFI is then calculated as:

```text
MFI = 100 - (100 / (1 + Money Flow Ratio))
```

Because volume is included, MFI differs from a price-only oscillator such as RSI. A price move accompanied by greater volume generally has more influence on MFI than a similar price move accompanied by lower volume.

The output scale is:

* near `0` — unusually strong negative money-flow pressure
* near `50` — relatively balanced money flow
* near `100` — unusually strong positive money-flow pressure

MFI does not directly measure future returns. It describes the current balance of price-and-volume pressure over its configured lookback.

---

## Value-added use

MFI adds value by incorporating participation into momentum analysis.

A price-only oscillator can show that price has moved strongly, but it does not directly account for how much trading volume supported that move. MFI gives greater weight to periods with larger raw money flow.

Potential uses include:

* identifying unusually weak or strong money-flow conditions;
* comparing short-, medium-, and longer-lookback pressure;
* confirming whether price momentum has meaningful volume participation;
* identifying possible oversold opportunity zones;
* identifying possible overbought risk zones;
* comparing money-flow conditions across securities in the heatmap and SCD matrices.

MFI is most useful as a contextual state measure rather than as a guaranteed reversal predictor.

A low reading can identify an oversold condition without proving that price has reached a durable bottom. A high reading can identify an overbought condition without proving that price will immediately decline.

---

## Use with

MFI can be paired with:

* **Price trend or moving averages** — to determine whether an extreme MFI state is occurring with or against the prevailing trend.
* **RSI or Stochastic** — to compare price-only momentum with volume-weighted momentum.
* **CMF or OBV** — to compare bounded money-flow pressure with broader accumulation/distribution behavior.
* **Support and resistance** — to judge whether an MFI extreme is occurring near an important price level.
* **ADX** — to distinguish strong-trend conditions from weaker or range-bound conditions.
* **Price structure** — to evaluate whether an extreme MFI reading is accompanied by stabilization, continuation, or breakdown.

The project’s MFI score itself does not require these confirmations. They are supplementary analytical context.

---

## MFI Rule Translation

The same rule structure applies independently to:

* `MFI_10`
* `MFI_14`
* `MFI_30`

For each configured period `n`, the rule engine evaluates the current initialized value in column:

```text
MFI_n
```

The rules form five mutually exclusive and collectively exhaustive bands for every initialized numeric MFI value.

Missing or uninitialized MFI values remain missing. They are not classified as Neutral.

---

### Strong Buy (`+2`)

**Executable rule**

```text
MFI_n <= 15
```

**Plain-English translation**

The current MFI reading is `15` or lower.

This represents the project’s most deeply oversold money-flow state and its strongest positive opportunity bias.

**Why it receives the strongest positive score**

A reading at or below `15` indicates that negative money flow has been unusually dominant over the selected lookback. The project interprets that degree of downside pressure as a stronger potential mean-reversion opportunity than the broader Buy band.

**Boundary behavior**

* `15.00` is Strong Buy.
* Values below `15.00` are Strong Buy.
* A value just above `15.00` is not Strong Buy.

**What the rule does not require**

The rule does not require:

* MFI to rise;
* MFI to cross above a threshold;
* a prior oversold reading;
* price to rise;
* bullish divergence;
* a reversal candle;
* future confirmation.

**Interpretive limitation**

Strong Buy means the current MFI state is deeply oversold under the project’s scoring model. It does not mean a reversal has already occurred or that price cannot continue falling.

---

### Buy (`+1`)

**Executable rule**

```text
MFI_n > 15 and MFI_n <= 25
```

**Plain-English translation**

The current MFI reading is above `15` and no higher than `25`.

This represents an oversold opportunity state, but one that is less extreme than Strong Buy.

**Why it receives a positive score**

The reading remains in a low money-flow zone where selling pressure has been substantial. The project assigns a positive mean-reversion bias, but the condition is not sufficiently extreme for the strongest score.

**Boundary behavior**

* `15.00` is not Buy; it is Strong Buy.
* Values greater than `15.00` and below `25.00` are Buy.
* `25.00` is Buy.
* A value just above `25.00` is Neutral.

**What the rule does not require**

The rule does not require:

* MFI to be rising;
* continuation across multiple bars;
* a threshold-cross event;
* price confirmation;
* divergence;
* a prior Strong Buy state.

**Interpretive limitation**

Buy identifies the current oversold band. It does not prove that money flow has turned upward.

---

### Neutral (`0`)

**Executable rule**

```text
MFI_n > 25 and MFI_n < 75
```

**Plain-English translation**

The current MFI reading is strictly above `25` and strictly below `75`.

This is the project’s non-extreme middle range.

**Why it receives a zero score**

The current money-flow reading is neither sufficiently low to receive a positive mean-reversion score nor sufficiently high to receive a negative overbought-risk score.

Neutral means the MFI state itself does not provide one of the project’s directional opportunity or risk classifications.

**Boundary behavior**

* `25.00` is not Neutral; it is Buy.
* Values above `25.00` and below `75.00` are Neutral.
* `75.00` is not Neutral; it is Sell.

**What Neutral does not mean**

Neutral does not necessarily mean:

* price is moving sideways;
* buying and selling volume are exactly equal;
* the security has no trend;
* the broader market setup is neutral;
* other indicators cannot be bullish or bearish.

It means only that the current MFI value lies inside the project’s middle state band.

**Missing-value behavior**

An uninitialized or missing MFI value is not Neutral. It remains missing and should not receive score `0`.

---

### Sell (`-1`)

**Executable rule**

```text
MFI_n >= 75 and MFI_n < 85
```

**Plain-English translation**

The current MFI reading is at least `75` but below `85`.

This represents an overbought-risk state, but one that is less extreme than Strong Sell.

**Why it receives a negative score**

Positive money flow has been unusually dominant over the selected lookback. The project interprets this as elevated overextension risk and assigns a negative mean-reversion bias.

**Boundary behavior**

* `75.00` is Sell.
* Values above `75.00` and below `85.00` are Sell.
* A value just below `75.00` is Neutral.
* `85.00` is not Sell; it is Strong Sell.

**What the rule does not require**

The rule does not require:

* MFI to be falling;
* MFI to cross below a threshold;
* price to decline;
* bearish divergence;
* a prior Strong Sell state;
* reversal confirmation.

**Interpretive limitation**

Sell identifies the current overbought-risk band. It does not prove that money flow has turned negative or that price must immediately fall.

---

### Strong Sell (`-2`)

**Executable rule**

```text
MFI_n >= 85
```

**Plain-English translation**

The current MFI reading is `85` or higher.

This represents the project’s most extreme overbought money-flow state and its strongest negative risk bias.

**Why it receives the strongest negative score**

A reading at or above `85` indicates unusually dominant positive money flow over the selected lookback. The project treats that degree of upside pressure as a stronger overextension risk than the broader Sell band.

**Boundary behavior**

* `85.00` is Strong Sell.
* Values above `85.00` are Strong Sell.
* A value just below `85.00` is Sell.

**What the rule does not require**

The rule does not require:

* MFI to fall;
* a threshold-cross event;
* a prior overbought reading;
* price weakness;
* bearish divergence;
* a confirmed reversal.

**Interpretive limitation**

Strong Sell means the current MFI state is deeply overbought under the project’s scoring model. It does not mean an immediate price decline is certain.

---

## Project-specific rule summary

| Signal      | Score | Exact condition              | Current-state interpretation     |
| ----------- | ----: | ---------------------------- | -------------------------------- |
| Strong Buy  |  `+2` | `MFI_n <= 15`                | Deeply oversold opportunity bias |
| Buy         |  `+1` | `MFI_n > 15 and MFI_n <= 25` | Oversold opportunity bias        |
| Neutral     |   `0` | `MFI_n > 25 and MFI_n < 75`  | Non-extreme middle range         |
| Sell        |  `-1` | `MFI_n >= 75 and MFI_n < 85` | Overbought risk                  |
| Strong Sell |  `-2` | `MFI_n >= 85`                | Deeply overbought risk           |


The rule bands are:
* mutually exclusive;
* ordered from lowest to highest MFI;
* exhaustive for every initialized numeric MFI value;
* identical across periods `10`, `14`, and `30`.

The model is a persistent state-band model. A signal remains active for as long as the current MFI value remains inside its corresponding band.

---

## Industry-standard Baseline

Conventional MFI interpretation commonly treats:

* readings near or below `20` as oversold;
* readings near or above `80` as overbought.

Some practitioners use more extreme thresholds, such as `10` and `90`, to identify rarer conditions.

There is no universal industry-standard five-state MFI scoring system equivalent to the project’s `+2`, `+1`, `0`, `-1`, and `-2` scale.

The project’s thresholds are therefore best understood as a custom calibration built around the conventional overbought/oversold concept:

* `15` and `85` identify the project’s strongest extreme states;
* `25` and `75` widen the actionable opportunity/risk zones;
* the middle range remains Neutral.

The semantic philosophy is primarily:

* volume-weighted overbought/oversold analysis;
* current-state classification;
* mean-reversion opportunity and risk bias.

It is not:

* a threshold-cross event model;
* confirmed reversal detection;
* divergence detection;
* momentum-continuation scoring;
* trend-regime scoring.

The thresholds are defensible as a project-specific heatmap calibration, but they should not be described as a universal market standard.

---

## How to Read

Read the displayed MFI value first, then interpret the signal as the project’s current-state classification.

### By value

* `MFI <= 15` — deeply oversold; Strong Buy opportunity bias
* `15 < MFI <= 25` — oversold; Buy opportunity bias
* `25 < MFI < 75` — middle range; Neutral
* `75 <= MFI < 85` — overbought; Sell risk bias
* `MFI >= 85` — deeply overbought; Strong Sell risk bias

### By configured period

**MFI(10)**

* reacts most quickly to recent price-and-volume changes;
* can enter and leave extreme states more frequently;
* is most suitable for short-term sensitivity.

**MFI(14)**

* is the standard reference variant;
* balances responsiveness and smoothing;
* is suitable for general-purpose interpretation.

**MFI(30)**

* changes more slowly;
* smooths shorter-term fluctuations;
* emphasizes more persistent money-flow conditions.

### Practical interpretation
- A positive MFI score means the oscillator is in an oversold opportunity band.
- A negative MFI score means the oscillator is in an overbought-risk band.
- A zero score means the value is in the non-extreme middle range.
- The score does not indicate that a reversal has already begun.

For stronger decision support, compare MFI with:
* price trend;
* support or resistance;
* moving-average structure;
* price-volume confirmation;
* other momentum or money-flow indicators.

---

## Initial audit note

The prior MFI rule design relied on directional or transition-style conditions, including rising or falling behavior and threshold-state changes.

The approved implementation replaces that approach with a direct persistent state-band model.

The final model:

* uses only the current initialized MFI value;
* applies the same thresholds to `MFI_10`, `MFI_14`, and `MFI_30`;
* does not require `rising_2bar()` or `falling_2bar()`;
* does not require `crossed_above()` or `crossed_below()`;
* does not require prior-bar confirmation;
* does not require price direction;
* does not implement divergence;
* does not predict future price behavior;
* preserves missing MFI values as missing rather than Neutral.

The implementation was validated for:

* exact threshold boundaries;
* mutual exclusivity;
* full initialized-value coverage;
* signal-label and score mapping;
* warmup and missing-value handling;
* Rolling Heatmap display;
* SCD Multiple Indicators display;
* SCD Single Indicator display;
* Category, Custom, and Preset selection paths.


---
# MFI: My Notes
> The volume-based equivalent to RSI. 
>  - Often used for **overbought/oversold analysis** 
>
> MFI is often used like an RSI but with volume, and traders look for divergence.    
> - MFI is RSI's volume-weighted cousin (uses typical price × volume flow instead of pure price change), so it tends to spike/exhaust faster on climactic volume — which matters for how you set your bands.

> Pair with a regime filter (e.g., ADX or a longer moving average slope) — mean reversion signals on MFI have a much better hit rate in low-ADX, range-bound conditions and a materially worse one when the underlying is trending hard, regardless of which band logic you choose.

---
**Purpose:** Combine price and volume data to create a volume-weighted momentum oscillator that identifies overbought/oversold conditions. 

**Use when**:  You want **overbought/oversold signals** but with volume confirmation, especially in ranging markets.
The "volume-based" equivalent to RSI:
- "*While volume-based, MFI behaves like RSI and is often used for **overbought/oversold analysis** similar to momentum indicators.*"

**Key Concept:** Often called "volume-weighted RSI." Uses both price change and volume to measure buying/selling pressure, making it more comprehensive than price-only oscillators.

**Calculation:** Uses typical price `[(high + low + close) ÷ 3]` multiplied by volume to create money flow, then applies RSI-style calculation over 14 periods.

**Signals & Interpretation:**
- Above 80 = overbought (potential selling opportunity)
- Below 20 = oversold (potential buying opportunity)
- Divergences between MFI and price signal potential reversals
- Rising MFI = increasing buying pressure

$\large{\rightarrow}$ Divergence between the MFI and price can indicate a potential trend reversa

**Optimal Conditions:** Works best in ranging or mildly trending markets. Most effective on daily and weekly timeframes for swing trading setups.

**Limitations:** Can remain overbought/oversold for extended periods in strong trends. May produce false signals in low-volume conditions.

**Complexity Level:** Intermediate

---
**Money Flow Index (MFI)**
- **Purpose:** Measures the strength of money flow into and out of an asset, often indicating overbought or oversold conditions. 
- **Calculation:** It uses a technique similar to the RSI but incorporates volume in its calculation of "typical price" and "money flow". 
- **Range:** Oscillates between 0 and 100. 
- **Signals:** Readings above 80 suggest an overbought market, while readings below 20 suggest an oversold market. 

---
#### Difference Btwn: Chaikin's Money Flow & MFI
The main difference is that the MFI is a momentum oscillator that uses price and volume to identify overbought/oversold conditions, ranging from 0-100, while CMF measures the strength of buying and selling pressure over a <u>longer period</u>, using a multiplier based on the price's closing position within its high-low range, resulting in a range between -1 and +1. 

MFI gives a more direct overbought/oversold signal, whereas CMF is more focused on the overall trend strength and direction of money flow.

