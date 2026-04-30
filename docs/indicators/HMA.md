Status: incomplete

> These here below are examples only:

> 💡 **Tip**
> Use CCI with trend filters like ADX.

> ⚠️ **Warning**
> Extreme readings can persist in strong trends.

> 📌 **Key Insight**
> CCI measures deviation, not direction.


---
The **Hull Moving Average** was Alan Hull's solution to a fundamental problem with all traditional MAs: *the longer the period, the smoother, but the more lag.* Hull attacked that tradeoff mathematically using **weighted moving averages (WMAs) and square root periods** to dramatically cut lag while preserving smoothness.

The formula essentially is:
> **HMA(n) = WMA(2 × WMA(n/2) − WMA(n)), smoothed over √n periods**


---
The HMA is a fast, smooth moving average designed to reduce lag while maintaining responsiveness. Experienced traders adjust the lookback period to align with their trading timeframe.


**Settings**:
- **Short-term (1-15 days):** HMA(9)  
  - This is the most common setting for short-term trading, as it reacts quickly to price changes. It’s widely used for day trading or short-term swing trading.
- **Intermediate-term (15-50 days):** HMA(21)  
  - A 21-period HMA balances responsiveness and stability, making it suitable for swing traders or those tracking trends over a few weeks. It smooths out noise while capturing mid-term price movements.
- **Long-term (50+ days):** HMA(50)  
  - A 50-period HMA is used for long-term trend analysis, often in position trading or to identify major market trends. It’s less sensitive to short-term fluctuations, focusing on broader price direction.

---

**Why HMA(55) specifically:**

| Reason | Detail |
|---|---|
| **Fibonacci** | 55 is a core Fibonacci number — markets respect these periods because enough participants use them to become self-reinforcing |
| **Lag reduction math** | Because HMA's lag is dramatically less than a standard EMA or SMA, a 55-period HMA behaves more like a 30-35 period EMA in terms of responsiveness — you get intermediate-term smoothing with near-term reaction speed |
| **Avoids crowding** | Everyone watches EMA(50). HMA(55) gives you a slightly differentiated read on the same timeframe — less susceptible to stop-hunting around the round number |
| **√55 ≈ 7.4** | The smoothing period is ~7, which maps neatly to one trading week — there's an elegant internal structure to it |

In practice, HMA(55) on a daily chart behaves like a *living* trend line — it turns faster than a 50 SMA but without the whipsaw of a short EMA. It's particularly effective as a dynamic support/resistance level in trending markets.
