# Stochastic Oscillator

**Purpose:** Compare a security's closing price to its price range over a given period to identify momentum turning points (ie,  potential market reversals) and overbought/oversold levels.

**Use when:** You want to time entries and exits based on where current price sits relative to recent highs and lows.

**Key Concept:** Measures where the current close is relative to the high-low range. A close near the high suggests buying pressure; a close near the low suggests selling pressure.

**Calculation:**

- **`%K = [(Current Close - Lowest Low) ÷ (Highest High - Lowest Low)] × 100`**
- **`%D = 3-period moving average of %K`**
- Typically uses 14-period lookback

**Signals & Interpretation:**
Compares closing price to its range over a period, scaled 0-100.
- Above 80 = overbought conditions
- Below 20 = oversold conditions
- **Buy**: %K line > 50 = bullish signal
	- %K crossing above %D = bullish signal
- **Sell**: %K line < 50 = bearish signal
	- %K crossing below %D = bearish signal
- **Neutral**: Around 50 or no clear crossover.

- Divergences with price indicate potential reversals
- Look for signals when leaving extreme zones

**Optimal Conditions:** Most effective in ranging markets and during pullbacks in trends. Works well on shorter timeframes for day trading and swing trading.

**Limitations:** Prone to false signals in strong trending markets. Can stay in extreme zones longer than expected during powerful moves.