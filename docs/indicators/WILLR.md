

|Bucket|What it answers|Indicators|
|---|---|---|
|**Momentum / oscillators**|Overbought/oversold, turning points|RSI, Stochastic, MACD, ROC, **Williams %R**, CCI, UO, DPO|
|**Trend direction**|Which way, and is there even a trend?|SMA, EMA, HMA|
|**Trend strength**|Is the trend strong enough to trust?|ADX|
|**Volatility**|How big are the swings, right now?|Bollinger Bands, ATR|
|**Volume / money flow**|Is real participation behind the move?|CMF, MFI, VWMA|
|**Sentiment / power balance**|Who's winning, bulls or bears?|Bull Bear Power|


# Industry-standard baseline

Williams %R is normally interpreted as a bounded oscillator from `0` to `-100`. It reflects where the close sits relative to the highest high / lowest low over the lookback period. The common default interpretation is:

```text
0 to -20      = overbought / near top of range
-80 to -100   = oversold / near bottom of range
around -50    = midpoint of recent range
```


---
# Williams R% (original notes)

**Purpose:** Identify overbought and oversold levels by measuring where the current close falls within the recent price range, similar to Stochastic but with inverted scale.

**Use when:** You want overbought/oversold signals with faster, more sensitive readings than traditional Stochastic.
- **Market conditions:** The indicator works best in sideways or ranging markets. In strong trends, it can stay overbought or oversold for a long time, so use it with caution and confirmation

**Key Concept:** Uses the same logic as Stochastic but inverted, ranging from 0 to -100.
- More sensitive to recent price action and often provides earlier signals.

**Calculation:** `%R = [(Highest High - Current Close) ÷ (Highest High - Lowest Low)] × -100`, typically over 14 periods.

**Signals & Interpretation:**
Momentum indicator scaled 0 to -100.

- **Overbought**:  '`> -20`'
	- Above -20 = overbought (near 0)
		-  price near highs, potential sell
- **Oversold**: '`< -80`'
	- Below -80 = oversold (near -100)
		- price near lows, potential buy
- **Potential 'Buy' signal**: Crossing above -80 from below
	- Often triggered when Williams %R crosses above -80 from below (indicating a shift from oversold to bullish momentum).
- **Potential 'Sell' signal**: Crossing below -20 from above
	- Often triggered when Williams %R crosses below -20 from above (indicating a shift from overbought to bearish momentum).
- Divergences with price suggest momentum shifts
- More sensitive than Stochastic to recent price changes

**Optimal Conditions:** Effective in volatile markets where quick momentum shifts occur. Works well on shorter timeframes and for active trading strategies.

**Limitations:** High sensitivity can lead to many false signals and whipsaws. Requires careful confirmation from other indicators.