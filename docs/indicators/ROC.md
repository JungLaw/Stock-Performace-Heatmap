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


