> **Bottom-line**
> - The actual average size of the stock's price swings over the last '`N`' days.
> - So, if the ATR(14) for an asset is $1.18, its price has an average range of movement of $1.18 per trading day over the last 14 days.

---
**Scope**: "volatility"

|Bucket|What it answers|Indicators|
|---|---|---|
|**Volatility**|How big are the swings, right now?|Bollinger Bands, ATR|
|Momentum / oscillators|Overbought/oversold, turning points|RSI, Stochastic, MACD, ROC, Williams %R, CCI, UO, DPO|
|Trend direction|Which way, and is there even a trend?|SMA, EMA, HMA|
|Trend strength|Is the trend strong enough to trust?|ADX|
|Volume / money flow|Is real participation behind the move?|CMF, MFI, VWMA|
|Sentiment / power balance|Who's winning, bulls or bears?|Bull Bear Power|

---
# ATR(14) — brief overview
**ATR** stands for **Average True Range**.
- It measures how much price typically moves over a given lookback period.
- IOW, it's the average price range of an investment over a period.

**ATR (Average True Range)** 
- Measures the actual average size of that stock's price swings over the last N days (typically 14), in real dollar/point terms.
- Answers the question "*how much does this thing normally move?*".


For `ATR(14)`:

```text
ATR_14 = average true range over 14 periods
```

---
# ATRP

While a standard SMA is not required to use ATRP, many traders use the two together to create more robust buy/sell rules that adapt to market volatility.

## What is ATRP?

Unlike the standard ATR, which gives you a dollar or point value, ATRP converts that value into a percentage of the asset's current price.

- Formula: $\text{ATRP} = (\text{ATR} / \text{Price}) \times 100$.
- Purpose: It allows you to compare the volatility of different stocks regardless of their price. For example, a $5 move on a $500 stock is less volatile than a $5 move on a $20 stock.

## How to use ATRP with SMA Buy/Sell Rules

Using ATRP alongside an SMA helps you "filter" signals. It isn't strictly necessary for a simple SMA strategy, but it is highly recommended for risk management. [7]

- Volatility Filter: You might set a rule to only buy on an SMA crossover if ATRP is above a certain level (ensuring there is enough "action" for a trend to form) or below a certain level (to avoid dangerously wild swings).
- Dynamic Stop-Losses: Instead of a fixed percentage, you can use a multiple of the ATRP to set your stop-loss. This ensures your stop is wider during volatile times and tighter during calm times.
- ATR-Based SMA Bands: Some platforms offer an 'ATR-based SMA indicator' where upper and lower bands are plotted a certain distance from the SMA based on volatility. A common buy rule is to enter when the price breaks above the upper volatility band.

## Summary of Differences

|Feature|Standard ATR|Average True Range P (ATRP)|
|---|---|---|
|Output|Absolute value (e.g., $2.50)|Percentage (e.g., 1.5%)|
|Main Use|Setting specific price stops|Comparing volatility across different assets|
|SMA Rule Role|Exit/Stop-loss placement|Strategy filtering and risk gauging|



---
# Notes

> *"Measures volatility (average range of price movement)."*
> "*ATR doesn't indicate 'direction', only **'magnitude'***"

"*Consider this as your market seismograph (or dance intensity meter to keep the metaphor going). It measures market volatility by assessing the range of price movement. This tells you whether the market is gliding smoothly or breaking into dramatic spins.*"

**ATR**: not a signal generator but arguably the single most professionally-respected one here; irreplaceable for position sizing/stop placement, and doesn't overlap with price-direction indicators.

---
**Purpose:** Measure market volatility by calculating the average range of price movement over a specified period, providing crucial information for risk management.

**Use when:** You need to set stop-losses, position sizes, or profit targets based on the security's typical volatility characteristics.

**Key Concept:** Captures the true daily range including gaps by taking the largest of: current high-low, current high-previous close, or current low-previous close. Essential for risk management.

**Calculation:**
- **True Range:** Max of (High-Low), (High-Previous Close), (Low-Previous Close)
- **ATR:** Moving average of True Range over N periods (typically 14)

---
**Signals & Interpretation:**
Measures volatility (average range of price movement).

- Higher ATR = higher volatility and risk
- Lower ATR = lower volatility and risk
- Rising ATR = increasing volatility
- Falling ATR = decreasing volatility
- Use multiples of ATR for stop-losses (e.g., 2×ATR)
- ATR doesn't indicate direction, only magnitude

---
- **High Volatility**: Value above a historical average or threshold (e.g., rising ATR indicates increasing volatility; specific cutoff varies by asset/dashboard).
- **Low/Less Volatility**: Value below average or declining.
- No direct Buy/Sell; used to gauge risk or stop-loss levels.

---
**Optimal Conditions:** Essential for all trading strategies and timeframes. Most valuable for position sizing, stop-loss placement, and profit target setting.

**Limitations:** Purely a volatility measure with no directional bias. Cannot be used alone for entry/exit signals. Lagging indicator based on historical volatility.


## Using ATR

**ATR Multiplier**:

|Style|Typical multiplier|
|---|---|
|Scalping|1x – 1.5x ATR|
|Day trading|1.5x – 2x ATR|
|Swing trading|2x – 3x ATR|
|Position/trend-following|3x – 4x ATR|


### Using ATR to 'Buy' (based on EMA)
AAPL: $327.50 (7/16)
- **14-day ATR**: $7.2 (about 2.45% of price)
- **20-day EMA**: $306.79

**Use**: 20-day EMA ≈ $306.79, ATR(14) = $7.25
**Calculation**: $306.79 − (2 × $7.25) = $306.79 − $14.50 = **$292.29**

### Simple ATR-offset 'Buy' limit order (more common in practice)
A lighter-weight version, without the EMA: **Buy limit = today's close − (0.5 to 1 × ATR)**

This is a common swing-trading technique for getting filled on an ordinary daily dip instead of paying up at the current price.

Using AAPL: $327.50 − (0.5 × $7.25) = $327.50 − $3.63 = **~$323.87** as a limit buy, expecting a normal one-day wiggle to fill it rather than requiring a deep retracement.

### Using ATR to get a 'Stop loss" price (Sell)

Say ATR(14) on a stock is **$4** (its average daily range over the last 14 days), and price breaks above resistance/EMA at **$150**, confirmed by ADX rising through 25.

Using a 2x multiplier (mid-range, appropriate for swing trading):

**Stop = Entry − (2 × ATR) = $150 − (2 × $4) = $150 − $8 = $142**

You buy at $150, place your stop at $142.
- If price closes below $142, that's no longer "normal daily wiggle" — it's twice the stock's typical daily range moving against you, which suggests the breakout failed, so you're out.