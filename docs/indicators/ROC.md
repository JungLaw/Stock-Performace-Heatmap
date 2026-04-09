Status: Incomplete

<div class="markdown-alert markdown-alert-note">
  <p>This is a custom HTML callout.</p>
</div>


**Purpose:** Measure the pure percentage change in price over a specified period to identify momentum acceleration or deceleration.
- Shows whether an asset is gaining or losing momentum by comparing current prices to historical ones. 

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

```ad-keypoints
The ROC oscillates above and below a zero line, which serves as a critical threshold for interpreting momentum:

- **Positive ROC (Above Zero Line):** Indicates upward price momentum. The higher the ROC, the stronger the bullish trend.
- **Negative ROC (Below Zero Line):** Reflects downward price momentum, with increasingly negative values pointing to a stronger bearish trend.
- **ROC at Zero:** Suggests no price change over the given period, often seen in consolidating or sideways markets.
```

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

