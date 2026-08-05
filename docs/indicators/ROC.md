
## Summary: ROC signals
Status: B

ROC measures the percentage change between the current adjusted closing price and the adjusted closing price a specified number of periods earlier.

The project uses ROC as a **zero-centered momentum-continuation indicator**:
- positive ROC means price is above its level `n` periods ago;
- negative ROC means price is below its level `n` periods ago;
- larger positive values indicate stronger upward price thrust;
- larger negative values indicate stronger downward price thrust;
- values near zero are treated as weak, mixed, or inconclusive momentum.

The project does **not** use ROC as a pure reversal indicator, crossover-event indicator, or formal divergence detector.


### 'Signal' Summary table

| Signal | Layman’s translation | Literal trigger | Rule logic |
|---|---|---|---|
| `strong_buy` | Price has advanced far enough over the lookback to qualify as unusually strong upward momentum. | ROC is above the period’s positive Strong threshold. | The current `n`-period percentage return exceeds the project’s higher bullish cutoff. |
| `buy` | Price is meaningfully higher than it was `n` periods ago, but not above the Strong threshold. | ROC is above the positive ordinary threshold and at or below the positive Strong threshold. | Positive momentum is meaningful but remains inside the ordinary bullish range. |
| `neutral` | Price is close enough to its level `n` periods ago that no meaningful directional momentum advantage is assigned. | ROC is inside the period’s symmetric Neutral band, including both exact boundaries. | Small positive and negative changes are treated as noise or weak momentum. |
| `sell` | Price is meaningfully lower than it was `n` periods ago, but not below the Strong threshold. | ROC is at or above the negative Strong threshold and below the negative ordinary threshold. | Negative momentum is meaningful but remains inside the ordinary bearish range. |
| `strong_sell` | Price has declined far enough over the lookback to qualify as unusually strong downward momentum. | ROC is below the period’s negative Strong threshold. | The current `n`-period percentage return exceeds the project’s higher bearish cutoff in magnitude. |

#### 'Threshold' Summary table

| Period | Neutral band | Strong threshold |
|---|---:|---:|
| ROC(9) | `±2%` | Beyond `±5%` |
| ROC(12) | `±3%` | Beyond `±7%` |
| ROC(14) | `±3%` | Beyond `±7%` |
| ROC(20) | `±3%` | Beyond `±7%` |
| ROC(50) | `±5%` | Beyond `±10%` |

---




## ROC — brief overview

Rate of Change is a pure momentum oscillator. It compares the current price with the price `n` periods earlier and expresses the difference as a percentage.

A conventional percentage formula is:

```text
ROC% = 100 × (Current Price − Price n periods ago)
             ÷ Price n periods ago
```

An equivalent form is:

```text
ROC% = 100 × ((Current Price ÷ Price n periods ago) − 1)
```

### Simple examples

If price was `$100` fourteen periods ago and is `$108` now:

```text
ROC(14) = 100 × (($108 − $100) ÷ $100)
        = +8.00%
```

If price was `$100` fourteen periods ago and is `$94` now:

```text
ROC(14) = 100 × (($94 − $100) ÷ $100)
        = -6.00%
```

If price is unchanged from fourteen periods ago:

```text
ROC(14) = 0.00%
```

### Simplest mental model

```text
Price is higher than n periods ago
→ ROC is positive
→ upward momentum

Price is lower than n periods ago
→ ROC is negative
→ downward momentum

Price is near its level n periods ago
→ ROC is near zero
→ weak or mixed momentum
```

### What ROC is actually measuring

ROC does not measure today’s one-day price change.

It measures the total percentage change across the selected lookback:

```text
ROC(9)
= current price compared with 9 periods ago

ROC(50)
= current price compared with 50 periods ago
```

A positive ROC can fall from one day to the next while price still rises. That means the current `n`-period gain is smaller than the prior day’s `n`-period gain; it does not necessarily mean price fell.

Likewise, a negative ROC can rise toward zero while price continues to decline. That means downside momentum is easing, not necessarily that price has reversed upward.

### Zero line

ROC is centered on zero:

| ROC area | Basic meaning |
|---:|---|
| Above `0` | Price is higher than it was `n` periods ago |
| At `0` | Price is unchanged from `n` periods ago |
| Below `0` | Price is lower than it was `n` periods ago |

The project does not score the zero line by itself. Each ROC period has a Neutral band around zero so small movements are not classified as directional signals.

---

## Current project periods

The Rolling Heatmap classification metadata assigns them as follows:

| Row | Category | Scope | Window |
|---|---|---|---|
| `ROC_9` | Momentum | Thrust Detection | Short term |
| `ROC_12` | Momentum | Thrust Detection | Short term |
| `ROC_14` | Momentum | Thrust Detection | Medium term |
| `ROC_20` | Momentum | Thrust Detection | Medium term |
| `ROC_50` | Momentum | Thrust Detection | Long term |


---
## Value-added use

> Use ROC when you want a direct, percentage-based measure of how far price has moved over a selected lookback and whether that move qualifies as weak, meaningful, or strong momentum under the project’s rules.

ROC is particularly useful for:
- identifying short-, medium-, and long-term thrust;
- confirming whether price direction has meaningful momentum behind it;
- comparing momentum strength across securities;
- recognizing when upward momentum is weakening despite a rising price;
- recognizing when downside momentum is easing despite a falling price;
- distinguishing small near-zero changes from meaningful directional movement.

**Also used to verify:**
- **Bullish divergence** forms when price makes lower lows while the ROC makes higher lows, suggesting that bearish momentum [is waning](https://www.investopedia.com/articles/trading/04/012804.asp) despite continued price declines.
- **Bearish divergence** appears when price makes higher highs while the ROC makes lower highs. This suggests that upward momentum is diminishing despite price advances.

---

## Use with

ROC is most useful when interpreted with trend, participation, volatility, and price structure.

> **EMA, SMA, HMA, or VWMA**

Use moving averages to determine whether ROC momentum agrees with the prevailing trend.

Examples:

```text
Price above rising EMA + positive ROC
→ trend and momentum agree

Price below falling SMA + negative ROC
→ downside trend and momentum agree
```

> **ADX**

ADX helps distinguish:

- strong trends, where elevated ROC may persist;
- weak trends, where ROC signals may reverse or whipsaw more frequently.

> **MACD**

MACD can confirm broader momentum direction and trend structure.

ROC gives a direct percentage return over a fixed lookback; MACD measures relationships between moving averages.

> **RSI, Stochastic, or Williams %R**

These indicators can add stretch or range-position context.

ROC is not bounded and does not use universal overbought/oversold levels.

> **MFI, CMF, OBV, and volume**

Participation indicators help determine whether volume supports the price thrust shown by ROC.

Examples:

```text
Strong positive ROC + positive CMF
→ upward momentum with accumulation support

Strong positive ROC + negative CMF
→ price thrust without supportive accumulation pressure
```

> **ATR or ATRP**

Volatility context helps assess whether a ROC reading is unusual for the security.

### Support, resistance, and price structure

ROC is more informative when interpreted near:
- breakouts;
- breakdowns;
- major support;
- major resistance;
- confirmed swing highs or lows.


---

# ROC(9) rule translation

## Signal table

| Signal | Raw rule | Display equivalent |
|---|---|---:|
| Strong Buy | `ROC_9 > 0.05` | Above `+5.00%` |
| Buy | `ROC_9 > 0.02 and ROC_9 <= 0.05` | Above `+2.00%` through `+5.00%` |
| Neutral | `-0.02 <= ROC_9 <= 0.02` | `-2.00%` through `+2.00%` |
| Sell | `ROC_9 >= -0.05 and ROC_9 < -0.02` | `-5.00%` through below `-2.00%` |
| Strong Sell | `ROC_9 < -0.05` | Below `-5.00%` |

## Strong Buy

```json
"strong_buy": "ROC_9 > 0.05"
```

### Literal meaning

The current adjusted closing price is more than `5%` above its adjusted closing price nine periods earlier.

### Plain-English version

> Price has advanced by more than 5% over nine periods, indicating unusually strong short-term upward thrust under the project’s ROC(9) calibration.

### Boundary behavior

```text
Exactly +5.00% → Buy
Above +5.00%   → Strong Buy
```

## Buy

```json
"buy": "ROC_9 > 0.02 and ROC_9 <= 0.05"
```

### Literal meaning

ROC(9) is above `+2%` but no greater than `+5%`.

### Plain-English version

> Price is meaningfully higher than it was nine periods ago, but the advance has not exceeded the Strong threshold.

## Neutral

```json
"neutral": "-0.02 <= ROC_9 <= 0.02"
```

### Literal meaning

ROC(9) is between `-2%` and `+2%`, inclusive.

### Plain-English version

> Price is close enough to its nine-period-ago level that the project does not assign a directional momentum signal.

## Sell

```json
"sell": "ROC_9 >= -0.05 and ROC_9 < -0.02"
```

### Literal meaning

ROC(9) is at least `-5%` but below `-2%`.

### Plain-English version

> Price is meaningfully lower than it was nine periods ago, but the decline has not exceeded the Strong threshold.

## Strong Sell

```json
"strong_sell": "ROC_9 < -0.05"
```

### Literal meaning

The current adjusted closing price is more than `5%` below its adjusted closing price nine periods earlier.

### Plain-English version

> Price has declined by more than 5% over nine periods, indicating unusually strong short-term downward thrust under the project’s ROC(9) calibration.

### Boundary behavior

```text
Exactly -5.00% → Sell
Below -5.00%   → Strong Sell
```

---

# ROC(12), ROC(14), and ROC(20) rule translation

These three periods currently share the same signal thresholds.

## Signal table

| Signal | Raw rule | Display equivalent |
|---|---|---:|
| Strong Buy | `ROC_n > 0.07` | Above `+7.00%` |
| Buy | `ROC_n > 0.03 and ROC_n <= 0.07` | Above `+3.00%` through `+7.00%` |
| Neutral | `-0.03 <= ROC_n <= 0.03` | `-3.00%` through `+3.00%` |
| Sell | `ROC_n >= -0.07 and ROC_n < -0.03` | `-7.00%` through below `-3.00%` |
| Strong Sell | `ROC_n < -0.07` | Below `-7.00%` |

where `n` is `12`, `14`, or `20`.

## Strong Buy

```json
"strong_buy": "ROC_n > 0.07"
```

### Literal meaning

Price is more than `7%` above its level `n` periods ago.

### Plain-English version

> The security has produced a large positive return over the selected short- or medium-term lookback.

### Boundary behavior

```text
Exactly +7.00% → Buy
Above +7.00%   → Strong Buy
```

## Buy

```json
"buy": "ROC_n > 0.03 and ROC_n <= 0.07"
```

### Literal meaning

ROC is above `+3%` but no greater than `+7%`.

### Plain-English version

> Positive momentum is meaningful, but it remains inside the ordinary bullish range.

## Neutral

```json
"neutral": "-0.03 <= ROC_n <= 0.03"
```

### Literal meaning

ROC is between `-3%` and `+3%`, inclusive.

### Plain-English version

> The price change over the selected lookback is not large enough to receive a directional signal.

## Sell

```json
"sell": "ROC_n >= -0.07 and ROC_n < -0.03"
```

### Literal meaning

ROC is at least `-7%` but below `-3%`.

### Plain-English version

> Negative momentum is meaningful, but it remains inside the ordinary bearish range.

## Strong Sell

```json
"strong_sell": "ROC_n < -0.07"
```

### Literal meaning

Price is more than `7%` below its level `n` periods ago.

### Plain-English version

> The security has produced a large negative return over the selected short- or medium-term lookback.

### Boundary behavior

```text
Exactly -7.00% → Sell
Below -7.00%   → Strong Sell
```

---

# ROC(50) rule translation

## Signal table

| Signal | Raw rule | Display equivalent |
|---|---|---:|
| Strong Buy | `ROC_50 > 0.10` | Above `+10.00%` |
| Buy | `ROC_50 > 0.05 and ROC_50 <= 0.10` | Above `+5.00%` through `+10.00%` |
| Neutral | `-0.05 <= ROC_50 <= 0.05` | `-5.00%` through `+5.00%` |
| Sell | `ROC_50 >= -0.10 and ROC_50 < -0.05` | `-10.00%` through below `-5.00%` |
| Strong Sell | `ROC_50 < -0.10` | Below `-10.00%` |

## Strong Buy

```json
"strong_buy": "ROC_50 > 0.10"
```

### Literal meaning

Price is more than `10%` above its level fifty periods ago.

### Plain-English version

> Price has produced a large positive long-term return under the current ROC(50) calibration.

### Boundary behavior

```text
Exactly +10.00% → Buy
Above +10.00%   → Strong Buy
```

## Buy

```json
"buy": "ROC_50 > 0.05 and ROC_50 <= 0.10"
```

### Literal meaning

ROC(50) is above `+5%` but no greater than `+10%`.

### Plain-English version

> Long-term momentum is meaningfully positive, but the gain has not exceeded the current Strong threshold.

## Neutral

```json
"neutral": "-0.05 <= ROC_50 <= 0.05"
```

### Literal meaning

ROC(50) is between `-5%` and `+5%`, inclusive.

### Plain-English version

> Price remains close enough to its fifty-period-ago level that the project assigns no directional long-term momentum state.

## Sell

```json
"sell": "ROC_50 >= -0.10 and ROC_50 < -0.05"
```

### Literal meaning

ROC(50) is at least `-10%` but below `-5%`.

### Plain-English version

> Long-term momentum is meaningfully negative, but the decline has not exceeded the current Strong threshold.

## Strong Sell

```json
"strong_sell": "ROC_50 < -0.10"
```

### Literal meaning

Price is more than `10%` below its level fifty periods ago.

### Plain-English version

> Price has produced a large negative long-term return under the current ROC(50) calibration.

### Boundary behavior

```text
Exactly -10.00% → Sell
Below -10.00%   → Strong Sell
```

---

## Why the rule ranges are explicitly exclusive

The rule engine evaluates labels in a defined sequence. Broad rules such as:

```text
Buy: ROC > +3%
Strong Buy: ROC > +7%
```

overlap because every Strong Buy observation also satisfies Buy.

The repaired rulebook therefore defines ordinary states as bounded ranges:

```text
Strong Buy: ROC > +7%
Buy:        +3% < ROC <= +7%
```

and:

```text
Sell:        -7% <= ROC < -3%
Strong Sell: ROC < -7%
```

This makes each initialized ROC value eligible for exactly one state.

The current rules preserve the previously intended exact-boundary assignments:

| Boundary | Assigned state |
|---:|---|
| Exact positive ordinary threshold | Neutral |
| Exact positive Strong threshold | Buy |
| Exact negative ordinary threshold | Neutral |
| Exact negative Strong threshold | Sell |

---


## How to read the hover

### Value

The hover displays ROC on the percentage-point scale.

```text
ROC(14): -8.45
```

means:

> Price is 8.45% below its adjusted closing price fourteen periods earlier.

### Delta versus prior day

The absolute delta is the change in the ROC reading, not the stock’s one-day price return.

Example:

```text
Prior ROC(14):   -7.65
Current ROC(14): -8.45
```

The hover displays:

```text
Δ vs prior day: -0.80 pps (-10.46%)
```

Interpretation:

- `-0.80 pps` means the ROC reading moved down by `0.80` percentage points;
- `-10.46%` is the relative change in the ROC reading versus its prior value.

`pps` means percentage points.

The relative percentage can become very large when the prior ROC reading is near zero. It should not be confused with the security’s one-day return.

When the prior ROC value is unavailable:

```text
Δ vs prior day: —
```

No `pps` suffix is shown because no absolute delta exists.

### Trend

The `Trend` field describes whether the ROC value rose, fell, or remained flat versus the prior observation.

Examples:

```text
Trend: Rising
Trend: Falling
Trend: Flat
```

In Single Indicator paths, price direction can appear beside indicator direction:

```text
Trend: Falling | Price: Rising
```

### Alignment

ROC hover adds a one-bar price/ROC interpretation:

```text
Alignment: P(+), ROC(-) = upside momentum weakening
```

Symbol meanings:

```text
P(+)   = price rose versus the prior observation
P(-)   = price fell versus the prior observation
P(0)   = price was flat

ROC(+) = ROC rose versus the prior observation
ROC(-) = ROC fell versus the prior observation
ROC(0) = ROC was flat
```

Approved Alignment translations:

| Price direction | ROC direction | Hover text |
|---|---|---|
| `P(+)` | `ROC(+)` | confirming upside momentum |
| `P(-)` | `ROC(-)` | confirming downside momentum |
| `P(+)` | `ROC(-)` | upside momentum weakening |
| `P(-)` | `ROC(+)` | downside momentum easing |
| `P(0)` | `ROC(+)` | momentum improving while price is flat |
| `P(0)` | `ROC(-)` | momentum weakening while price is flat |
| `P(+)` | `ROC(0)` | price rising with stable momentum |
| `P(-)` | `ROC(0)` | price falling with stable momentum |
| `P(0)` | `ROC(0)` | price and momentum unchanged |

The Alignment line is omitted when the prior price or prior ROC value is unavailable.

### Alignment is not formal divergence

The Alignment field compares only the current observation with the immediately preceding observation.

It does **not** establish classical bullish or bearish divergence.

Formal divergence requires comparison of confirmed swing points, such as:

```text
Bullish divergence:
price makes a lower swing low
while ROC makes a higher swing low

Bearish divergence:
price makes a higher swing high
while ROC makes a lower swing high
```

The current project has not implemented pivot detection or formal ROC divergence classification.

Therefore:

```text
P(+), ROC(-)
```

means:

> Today’s price/ROC directions oppose one another, and upside momentum is weakening on a one-bar basis.

It does not mean:

> A confirmed bearish divergence exists.

---

## Practical interpretation by period

### ROC(9)

ROC(9) is the most responsive active ROC row.

Use it for:
- short-term thrust;
- rapid momentum changes;
- near-term confirmation;
- identifying sharp short-term advances or declines.

Tradeoff:
- reacts quickly;
- produces more frequent directional states;
- is more sensitive to noise and short-lived moves.

### ROC(12)

ROC(12) is a short-term momentum measure with a somewhat wider Neutral band than ROC(9).

Use it for:
- short-term momentum confirmation;
- a less reactive alternative to ROC(9);
- Custom-view momentum context.

### ROC(14)

ROC(14) is the primary medium-term ROC row in the MT Overview preset.

Use it for:
- intermediate momentum confirmation;
- swing-trading context;
- comparing price direction with medium-term thrust.

### ROC(20)

ROC(20) provides a longer medium-term comparison.

Use it for:
- smoother intermediate momentum;
- identifying more persistent advances or declines;
- supplementary medium-term analysis.

### ROC(50)

ROC(50) is the long-term ROC row.

Use it for:
- broad trend-thrust context;
- identifying sustained multi-week or multi-month price displacement;
- comparing long-term momentum across securities.

Caution:

The current `±10%` Strong threshold is retained provisionally. Production-path diagnostics showed that ROC(50) Strong Buy can occur frequently in higher-volatility growth equities. Threshold calibration is a required deferred follow-up.


---

## Threshold interpretation and limitations

### Project-specific thresholds

ROC does not have universal fixed overbought and oversold levels comparable to the commonly cited `70/30` RSI references.

ROC is:
- unbounded on the upside;
- bounded at `-100%` only if price falls to zero;
- highly sensitive to security volatility;
- sensitive to the selected lookback.

The project’s thresholds are therefore **calibrated classification bands**, not universal industry standards.

### Threshold table

| Period | Neutral band | Strong threshold |
|---|---:|---:|
| ROC(9) | `±2%` | Beyond `±5%` |
| ROC(12) | `±3%` | Beyond `±7%` |
| ROC(14) | `±3%` | Beyond `±7%` |
| ROC(20) | `±3%` | Beyond `±7%` |
| ROC(50) | `±5%` | Beyond `±10%` |

### Volatility dependence

The same threshold can behave differently across securities.

A `+7%` ROC reading may be unusual for a defensive ETF but common for a volatile growth stock.

Therefore:

- compare ROC with the security’s normal volatility;
- compare multiple ROC periods;
- avoid treating a Strong state as proof of imminent continuation or reversal;
- use price structure and other indicators for confirmation.

### Momentum persistence

A Strong Buy reading does not mean price is overbought and must fall.

A Strong Sell reading does not mean price is oversold and must rebound.

Strong trends can keep ROC elevated or depressed for extended periods.

### Lookback effect

Longer ROC periods accumulate more price movement.

That means longer-period thresholds may naturally trigger more often in sustained trends unless calibrated more widely.

This is one reason ROC(50) remains flagged for future calibration.

### Base effect

ROC compares against the price exactly `n` periods earlier.

A sharp move can enter or leave the lookback window and materially change ROC even when the current day’s price move is modest.

### Near-zero relative delta

The hover’s relative ROC delta can become extremely large when the previous ROC value is near zero.

Example:

```text
Prior ROC:   +0.20
Current ROC: +1.20

Absolute change: +1.00 pps
Relative change: +500%
```

The absolute percentage-point change is often the more intuitive comparison near zero.

---

## Project signal model

The project uses a **thresholded momentum-continuation model**.

```text
Large positive ROC
→ Strong Buy

Moderate positive ROC
→ Buy

Small positive or negative ROC
→ Neutral

Moderate negative ROC
→ Sell

Large negative ROC
→ Strong Sell
```

The labels are project classifications, not automatic trade instructions.

In ROC terms:

```text
Buy
= meaningful positive n-period momentum

Sell
= meaningful negative n-period momentum
```

Strong states indicate larger momentum magnitude.

They do not require:
- an ROC zero-line crossover;
- an ROC reversal;
- acceleration across multiple bars;
- a price breakout;
- volume confirmation;
- formal divergence.

---
## What ROC does not tell you

ROC does not directly identify:

- fair value;
- support or resistance;
- volume participation;
- trend strength independent of direction;
- future return probability;
- a confirmed top or bottom;
- formal divergence;
- a current-bar crossover event;
- the reason price moved.

ROC is one momentum input in a broader technical-analysis system.

---

## Verified implementation behavior

The repaired production-path diagnostic used:

```text
SPY
QQQ
AAPL
NVDA
XLP
EWJ
```

across ROC(9), ROC(12), ROC(14), ROC(20), and ROC(50).

Verified outcomes:

```text
Rule overlaps:                       0
Uncovered initialized observations: 0
Warmup labels incorrectly assigned: 0
Warmup scores incorrectly assigned: 0
Classifier label mismatches:        0
Classifier score mismatches:        0
```

Both extreme states were reachable:

```text
Strong Buy observations:  4,208
Strong Sell observations: 1,227
```

The diagnostic performed no file or database writes.

---

## Deferred ROC work

### Required ROC(50) threshold calibration

The current ROC(50) rules remain:

```text
Neutral: ±5%
Strong:  beyond ±10%
```

This calibration is intentionally retained for the completed mechanical repair, but it is not considered permanently settled.

Required future work:

1. test higher ROC(50) Strong thresholds, beginning with `±15%`;
2. evaluate whether the Neutral band should remain `±5%` or widen;
3. use a broader mixed-volatility universe;
4. compare equities, sector ETFs, broad-market ETFs, and international ETFs;
5. measure state frequencies across multiple market regimes;
6. approve any revised threshold only after production-path diagnostics.

### Formal divergence detection

Formal ROC divergence remains a separate future workstream.

It would require:

- pivot-high and pivot-low definitions;
- confirmed swing-point selection;
- minimum pivot separation;
- materiality tolerances;
- comparison of price pivots with ROC values on the same dates;
- treatment of unconfirmed recent pivots;
- historical validation.

The current `Alignment` field must not be relabeled as formal divergence.

---

## Technical ownership map

| Responsibility | Current owner |
|---|---|
| ROC parameter inventory | `master_rules_normalized.json` and rulebook-derived compute config |
| Fallback parameter inventory | `indicator_preprocessor.py → DEFAULT_CONFIG` |
| Adjusted Close / Close selection | `indicator_preprocessor.py → _get_price_series()` |
| ROC calculation | `indicator_preprocessor.py → compute_all_indicators()` |
| Fractional-unit normalization | `indicator_preprocessor.py` |
| Five-state rule expressions | `master_rules_normalized.json` |
| Expression evaluation | `expression_engine.py` |
| Missing-value restoration and scoring | `signal_classifier.py → SignalEngine._evaluate_rule_block()` |
| Row category / scope / window | `rolling_heatmap_classification.py` |
| Preset exposure | `rolling_heatmap_presets.py` |
| Percentage-point display | `rolling_heatmap_adapter.py` |
| ROC absolute-delta `pps` display | `rolling_heatmap_adapter.py` |
| One-bar Alignment interpretation | `rolling_heatmap_adapter.py` |
| SCD hover propagation and rendering | `streamlit_app.py` |

---

## External reference context

The following external references support the general, non-project-specific ROC description:

- Fidelity describes ROC as a pure momentum oscillator that compares current price with the price `n` periods earlier and fluctuates above and below zero:
  <https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/roc>

- Investopedia describes price ROC as a percentage-change oscillator, notes that it is not range-bound, emphasizes that thresholds depend on volatility and lookback, and treats divergence as a warning rather than a definitive trigger:
  <https://www.investopedia.com/terms/p/pricerateofchange.asp>

- pandas-ta-classic indicator reference confirms ROC is part of the supported momentum indicator set:
  <https://xgboosted.github.io/pandas-ta-classic/indicators.html>

These references do not define the project’s five-state thresholds. The thresholds, boundary assignments, score mapping, warmup policy, `pps` display, and Alignment language are project-specific implementation decisions.





## Old Notes
Status: Incomplete

**Purpose:** Measure the pure percentage change in price over a specified period to identify momentum acceleration or deceleration.
- Shows whether an asset is gaining or losing momentum by comparing current prices to historical ones. 


- Measures the momentum of price changes. It compares the current price to a price '`n`' periods ago.

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

**Calculation:** `ROC = [(Current Price - Price N periods ago) ÷ Price N periods ago] × 100`, typically using 12 or 14 periods.

**Signals & Interpretation:**
- Positive ROC = upward momentum
- Negative ROC = downward momentum
- ROC above zero line = bullish bias
- ROC below zero line = bearish bias
- Extreme readings suggest momentum exhaustion
- Divergences with price indicate potential trend changes

**Application/Strategies**:

- **Overbought/sold)**: Consider selling when ROC is high (overbought) and vice versa
- **Breakouts**: Look for price breakout accompanied by a riding ROC for confirmation.
- **Trend Reversals**: Look for price movement contradicting ROC for possible trend reversal.
- **Zero-line Crossovers**: A possible trend change might be signaled by ROC crossing above/below 0.




**Optimal Conditions:** Most effective in trending markets for confirming momentum direction. Works well on daily and weekly timeframes for trend analysis.

**Limitations:** Can be volatile and noisy without smoothing. Doesn't provide specific overbought/oversold levels like bounded oscillators.

**Complexity Level:** Beginner-friendly

---
**Strengths**: 
- Highly responsive to price changes, giving traders quick insights into market dynamics. 
- ROC is nearly identical to [[#Momentum (MOM)|MOM]], with MOM expressing the change as a value.

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
- **Considerations:** A long look-back period is slower to react to changes, which means opportunities take longer to manifest,


