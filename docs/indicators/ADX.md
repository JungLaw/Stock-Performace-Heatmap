# ADX(14) 'Signal' Summary
Status: B

| Signal        | Literal trigger                                             | Plain-English meaning                                   |
| ------------- | ----------------------------------------------------------- | ------------------------------------------------------- |
| `strong_buy`  | `ADX > 25` and `+DI − -DI >= 10`                            | Strong trend with clearly bullish directional pressure. |
| `buy`         | `ADX > 20` and `+DI − -DI >= 5`                             | Meaningful bullish trend.                               |
| `neutral`     | `ADX <= 20` or `+DI` and `-DI` are less than 5 points apart | Trend is weak or direction is too close to call.        |
| `sell`        | `ADX > 20` and `-DI − +DI >= 5`                             | Meaningful bearish trend.                               |
| `strong_sell` | `ADX > 25` and `-DI − +DI >= 10`                            | Strong trend with clearly bearish directional pressure. |

## Industry-standard Baseline
The standard ADX interpretation is:

- ADX measures trend strength, not direction.
- +DI / -DI help determine direction.
- A reading above 25 is commonly treated as a strong trend.
	- The higher the number, the stronger the momentum.
	- ADX > 50: Signals an extremely strong trend, but caution is advised as the asset may be overbought or oversold and due for a price correction.
- A reading below 20 is commonly treated as weak / non-trending market.
	- Traders often avoid 'trend'-following strategies during this phase and use 'range-bound' or 'mean-reversion' tactics.
- Between 20 and 25 is often treated as a gray zone.
	- Fidelity says most chart analysts treat ADX above 25 as a strong trend and below 20 as no trend, with no clear signal interpretation between 20 and 25.
	- TradingView similarly notes that ADX above 25 suggests trend strength and ADX below 20 suggests a '***weak***' or '***trendless***' market; it also notes that +DI / -DI crosses can signal bullish or bearish conditions, but can generate false signals, especially when ADX is below 25.
- Fidelity notes that a '*rising ADX*' generally means the existing trend is strengthening, while a '*falling ADX*' suggests the trend is weakening or absent.

---
# ADX(14) — brief overview

**ADX** stands for **Average Directional Index**. It is used to measure **trend strength**, not trend direction by itself.

ADX usually works together with two "**directional indicators**":

```text
DIp_14 = +DI / positive directional indicator
DIn_14 = -DI / negative directional indicator
```

Simple interpretation:

* `ADX_14` tells you **how strong the trend is**.
* `DIp_14` tells you how much positive/upward directional movement is dominating.
* `DIn_14` tells you how much negative/downward directional movement is dominating.
* `DIp_14 > DIn_14` means upward directional pressure is stronger.
* `DIn_14 > DIp_14` means downward directional pressure is stronger.
* Higher ADX means the trend is stronger, regardless of whether it is bullish or bearish.
* If the ADX is falling, it means the **trend is weakening**, so trend-following signals should be taken with caution.

Value-added use:
> Use ADX when you want to distinguish “*there is a real trend here*” from “*price is just chopping around*” and when you want to confirm whether the directional pressure is more bullish or bearish.

## Understanding the Spread Numbers

When comparing a spread of, say, -5 to a spread of -20 (where -DI is higher than +DI):
- **Spread of -5 (Narrow):** This indicates a tight, compressed market. Sellers have a slight edge, but buyers are fighting back. The market is likely in a consolidation phase, a weak trend, or preparing for a potential reversal.
**Spread of -20 (Wide):** This indicates massive downward momentum. Sellers are completely dominating buyers. The wide gap shows that price ranges are expanding aggressively downward, signaling a highly stable and strong bearish trend


### Key Trading Insights from Spread Magnitude
Tracking +DI and -DI as a time series over time is highly beneficial. While the standalone ADX line tells you how hard the market is driving, it is completely "blind" to the steering wheel.
- Monitoring the historical behavior of the underlying +DI and -DI time series provides granular insights into shifts in market equilibrium.

#### 1. Trend Acceleration vs. Deceleration (Gauging the Intensity Shift (The "Spread"))
Tracking the distance between the two time series over multiple intervals quantifies who is completely dominating the trend:

When the gap between the +DI and -DI expands, it indicates that one group (buyers or sellers) is accelerating while the opposing group's momentum is collapsing. This confirms a high-probability continuation of the current trend.

- **Expanding Spread:** When the gap between +DI and -DI is actively widening, the trend is accelerating. Said differently, it indicates that one group (buyers or sellers) is accelerating while the opposing group's momentum is collapsing.
	- This confirms a high-probability continuation of the current trend.
	  You should stay with the trend and avoid fighting the move.


- **Contracting Spread:** When the gap begins to narrow (converge toward each other), the trend is losing steam.
	- This typicaly happens _before_ a full crossover occurs and serves as an early warning to tighten stop-losses or take profits
	- This provides an early warning signal of a potential "range-bound" period or an upcoming "trend reversal" long before the ADX line falls.



#### 2a. Predicting ADX Turning Points
- The ADX line is mathematically derived from the smoothed differences between +DI and -DI.
- A **widening spread** will force the ADX line to rise, confirming a strong trend.
- A **narrowing spread** causes the ADX line to flatten out and fall, signaling the end of the trend.

#### 2b. Identifying Early Entry and Exit Signals
Using the crossover of these two time series serves as a mechanical trend-following engine:
* Bullish Shift (+DI > -DI): Indicates buying pressure has overtaken selling pressure.
* Bearish Shift (-DI > +DI): Indicates selling pressure has conquered buying pressure.


#### 3. Volatility and Breakout Confirmation
- **The Squeeze:** When the spread shrinks close to zero, volatility is dangerously low.
- **The Pop:** A sudden, explosive widening of the spread confirms a legitimate breakout or breakdown, helping you filter out sideways market noise.


---

# ADX(14) Rule Translation

## Strong buy

```json
"strong_buy": "ADX_14 > 25 and (DIp_14 - DIn_14) >= 10"
```

Literal component breakdown:

* `ADX_14 > 25`

  * The ADX value is above 25.
  * In this rulebook, that means the trend is strong enough to matter.

* `(DIp_14 - DIn_14) >= 10`

  * The positive directional indicator is at least 10 points higher than the negative directional indicator.
  * In other words, bullish directional pressure is clearly stronger than bearish directional pressure.

Literal summary:

> ADX is above 25, and +DI is at least 10 points higher than -DI.

Plain-English version:

> The trend is strong, and the directional pressure is clearly bullish.

Notes / confidence:

* High confidence on literal meaning.
* This rule combines **trend strength** (`ADX > 25`) with **bullish direction** (`+DI meaningfully above -DI`).
* The `10-point DI gap` is a custom clarity threshold. It is easy to explain, but still a rulebook calibration choice.

---

## Buy

```json
"buy": "ADX_14 > 20 and (DIp_14 - DIn_14) >= 5"
```

Literal component breakdown:

* `ADX_14 > 20`

  * The ADX value is above 20.
  * In this rulebook, that means there is at least a meaningful trend, though not as strong as the `strong_buy` threshold.

* `(DIp_14 - DIn_14) >= 5`

  * The positive directional indicator is at least 5 points higher than the negative directional indicator.
  * Bullish directional pressure is moderately stronger than bearish directional pressure.

Literal summary:

> ADX is above 20, and +DI is at least 5 points higher than -DI.

Plain-English version:

> There is a meaningful bullish trend, but it is not strong enough to qualify as strong buy.

Notes / confidence:

* High confidence on literal meaning.
* This is the lighter version of the strong-buy rule: lower ADX threshold and smaller DI gap.
* The rule is not saying “price is up today.” It is saying the directional-movement system sees bullish directional pressure in a trend-strength context.

---

## Neutral

```json
"neutral": "ADX_14 <= 20 or abs(DIp_14 - DIn_14) < 5"
```

Literal component breakdown:

* `ADX_14 <= 20`

  * ADX is 20 or lower.
  * In this rulebook, that means the trend is too weak to classify confidently.

* `or`

  * Either condition can make the signal neutral.

* `abs(DIp_14 - DIn_14) < 5`

  * The gap between +DI and -DI is less than 5 points, ignoring which one is higher.
  * Bullish and bearish directional pressure are too close to call.

Literal summary:

> Treat ADX(14) as neutral if the trend is weak, or if +DI and -DI are less than 5 points apart.

Plain-English version:

> Either there is not enough trend strength, or the bullish/bearish directional pressure is too close to call.

Notes / confidence:

* High confidence on literal meaning.
* This is a useful neutral rule because it can suppress weak directional readings.
* The `or` matters: even if +DI is higher than -DI, the result can still be neutral if ADX is weak. Likewise, even if ADX is above 20, the result can still be neutral if +DI and -DI are too close.
* This rule can overlap with buy/sell edge cases depending on evaluation order, but the threshold design appears intended to separate weak/unclear conditions from actionable ones.

---

## Sell

```json
"sell": "ADX_14 > 20 and (DIn_14 - DIp_14) >= 5"
```

Literal component breakdown:

* `ADX_14 > 20`

  * The ADX value is above 20.
  * In this rulebook, that means there is at least a meaningful trend.

* `(DIn_14 - DIp_14) >= 5`

  * The negative directional indicator is at least 5 points higher than the positive directional indicator.
  * Bearish directional pressure is moderately stronger than bullish directional pressure.

Literal summary:

> ADX is above 20, and -DI is at least 5 points higher than +DI.

Plain-English version:

> There is a meaningful bearish trend, but it is not strong enough to qualify as strong sell.

Notes / confidence:

* High confidence on literal meaning.
* This mirrors the `buy` rule in the bearish direction.

---

## Strong sell

```json
"strong_sell": "ADX_14 > 25 and (DIn_14 - DIp_14) >= 10"
```

Literal component breakdown:

* `ADX_14 > 25`

  * The ADX value is above 25.
  * In this rulebook, that means the trend is strong enough to matter.

* `(DIn_14 - DIp_14) >= 10`

  * The negative directional indicator is at least 10 points higher than the positive directional indicator.
  * Bearish directional pressure is clearly stronger than bullish directional pressure.

Literal summary:

> ADX is above 25, and -DI is at least 10 points higher than +DI.

Plain-English version:

> The trend is strong, and the directional pressure is clearly bearish.

Notes / confidence:

* High confidence on literal meaning.
* This mirrors the `strong_buy` rule in the bearish direction.
* Again, ADX itself does not say bearish; the bearish direction comes from `-DI` being above `+DI`.


# Initial audit note

This rule set is more internally coherent than the Stochastic and RSI examples. It has a clean structure:

```text
trend strength threshold + directional gap threshold
```

The main thing to understand is that **ADX alone is not bullish or bearish**. The rulebook turns it into buy/sell only by pairing ADX with the spread between `+DI` and `-DI`.




---
# ADX (Notes)
> "Identifying a trend’s strength"

|Bucket|What it answers|Indicators|
|---|---|---|
|**Trend strength**|Is the trend strong enough to trust?|ADX|
|**Momentum / oscillators**|Overbought/oversold, turning points|RSI, Stochastic, MACD, ROC, **Williams %R**, CCI, UO, DPO|
|**Trend direction**|Which way, and is there even a trend?|SMA, EMA, HMA|
|**Volatility**|How big are the swings, right now?|Bollinger Bands, ATR|
|**Volume / money flow**|Is real participation behind the move?|CMF, MFI, VWMA|
|**Sentiment / power balance**|Who's winning, bulls or bears?|Bull Bear Power|


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
	- **Uptrend:** When the '`+DI`' (positive Directional Indicator) is above the '`-DI`' (negative Directional Indicator), the trend is bullish. 
	- **Downtrend:** When the '`-DI`' is above the '`+DI`', the trend is bearish.



**Buy/Sell Signals (LJ)**:
First, identify '**Trend Strength**'.
Second, if a trend exists (`ADX >= 25`), then verify '**Trend Direction**'.
Lastly, use the following logic to determine the 'Action/Signal':
- **Buy**: if `25 <= ADX <75` and '`+DI > -DI`'
- **Sell**: if `ADX  >= 50` and '`-DI > -DI`'
- **Strong Sell**: if `ADX  >= 60` and '`-DI > -DI`'

---
* **`ADX < 20`**: Indicates a weak or non-trending market. Traders often avoid trend-following strategies during this phase and use range-bound or mean-reversion tactics.
* **`ADX > 25`**: Confirms that a strong trend is underway. The higher the number, the stronger the momentum.
* **`ADX > 50`**: Signals an extremely strong trend, but caution is advised as the asset may be overbought or oversold and due for a price correction.

---
- **Strong Trend (Buy or Sell depending on +DI/-DI)**: >25 (strong directional movement; +DI > -DI for buy, -DI > +DI for sell).
- **Neutral**: <20-25 (weak or no trend, range-bound market). (see ""Industry-standard Baseline")

---
**Optimal Conditions:** Essential for strategy selection across all timeframes. Most valuable when combined with directional indicators to determine both trend strength and direction.

**Limitations:**
- Highly ineffective in sideways, "range-bound" markets.
- Doesn't indicate trend direction. Can remain low during strong but smooth trends.
- Lagging indicator that confirms strength after it develops. IOW, it tracks past price movements and will only register a trend after it has already begun.

**Use with:**
To build a reliable strategy, traders frequently pair the ADX with momentum indicators like the Relative Strength Index (RSI) or Moving Averages.


**Complexity Level:** Intermediate


## How Traders Use It
* **Trend Confirmation**: An ADX value above 25 gives traders confidence to use trend-following systems (like moving averages). If the ADX is falling, it means the trend is weakening, so trend-following signals should be taken with caution.
* **Directional Signals**: The +DI and -DI lines help identify trend direction. When the +DI crosses above the -DI, it signals upward momentum. When the -DI crosses above the +DI, it signals downward momentum.



---
# Future Improvements

The current signal rules have two limitations.

## 1. They do not check whether ADX is rising

A common ADX interpretation is not just “*ADX is above 25*,” but also whether ADX is **rising** or **falling**.
- Fidelity notes that a rising ADX generally means the existing trend is strengthening, while a falling ADX suggests the trend is weakening or absent.

Your rules do not say:

```text
ADX_14 is rising
```

They only say:

```text
ADX_14 > 20
ADX_14 > 25
```

That means the rule could label a strong buy/sell even if ADX is high but starting to weaken.

For a heatmap, that may be acceptable. But if we were designing a more sophisticated rule, we might distinguish:

* strong trend and strengthening
* strong trend but weakening
* weak trend
* direction unclear

**Relevant 'Signals'**: `strong buy/sell`

## 2. The `buy` threshold at `ADX > 20` is slightly permissive

Using `ADX > 20` for basic buy/sell is defensible, but the 20–25 zone is often treated as transitional.
- Fidelity explicitly frames 20–25 as a gray zone with no clear signal interpretation.

So:

```json
"buy": "ADX_14 > 20 and (DIp_14 - DIn_14) >= 5"
```

is not wrong, but it is a bit more permissive than a stricter system that would require `ADX > 25` for any directional signal.

However, because your rule also requires a DI gap of at least 5, it is not recklessly permissive.

**Relevant 'Signals'**: `buy/sell`
