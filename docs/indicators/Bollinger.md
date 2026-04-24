

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