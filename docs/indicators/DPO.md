The Detrended Price Oscillator (DPO) strips away long-term price trends to expose short-term cyclical patterns and overbought or oversold extremes. Its primary value is cycle timing—helping traders estimate the duration between historical peaks and troughs to anticipate future turning points, independent of the broader bull or bear market.

The result: DPO tells you **where you are in the current price cycle** — independent of whether the trend is up, down, or sideways.

---
DPO: a way to remove the longer trend from price so shorter cycles are easier to see. 
- DPO is not designed for momentum signals; 
- it is used to identify cycle highs/lows and estimate cycle length. 

---
#### What It's Used For
For **timing entries within existing trends** — adding to positions on pullbacks, scaling in and out during a run. In that use case it is genuinely differentiated from everything else in your roster.

Useful for if you want to ***time the cycle within a trend***.



#### Rules

- **Strong Buy = DPO < −2%** (deeply negative)
- **Strong Sell = DPO > +2%** (deeply positive)


|Signal|Rule|Dashboard Label (suggested)|
|---|---|---|
|🟢 Strong Buy|DPO < −2%|**Cycle Trough — Add**|
|🔵 Buy|DPO −1% to −2%|**Cycle Low — Favorable Entry**|
|⚪ Neutral|DPO −1% to +1%|**Mid-Cycle — No Edge**|
|🟠 Sell|DPO +1% to +2%|**Cycle Peak — Hold/Trim**|
|🔴 Strong Sell|DPO > +2%|**Cycle Extended — Wait**|


The language shift from "Sell/Strong Sell" to "Hold/Trim/Wait" more accurately reflects what DPO is actually telling you — especially in a trending environment where a raw "Strong Sell" label could trigger the wrong response.

#### Example 1 — AAPL in a Strong Uptrend

Let's say AAPL is trading at **$185** and has been in a clear uptrend for several months. RSI has been pinned between 65–75 for weeks — giving you almost no actionable information about timing.

Here's what a 30-bar DPO sequence might actually look like on your dashboard:

|Day|Price|Trend Direction|DPO Value|DPO % of Price|Dashboard Signal|Action Implied|
|---|---|---|---|---|---|---|
|1|$172|Uptrend|−$2.10|−1.22%|🔵 Buy|Moderate cycle trough — decent add|
|5|$175|Uptrend|−$3.80|−2.17%|🟢 Strong Buy|Deep cycle trough — strong add signal|
|10|$178|Uptrend|−$0.40|−0.22%|⚪ Neutral|Mid-cycle — no edge either way|
|15|$181|Uptrend|+$1.90|+1.05%|🟠 Sell|Cycle peak building — consider trimming|
|20|$183|Uptrend|+$3.80|+2.07%|🔴 Strong Sell|Deep cycle peak — reduce/wait|
|25|$181|Uptrend|+$1.20|+0.66%|⚪ Neutral|Cycle rolling over — watch for trough|
|30|$185|Uptrend|−$2.40|−1.30%|🔵 Buy|New cycle trough forming — re-enter|

**What you're seeing:** Price went from $172 → $185 (up 7.6%) the whole time. The trend never broke. RSI stayed elevated throughout. But DPO gave you **four distinct actionable signals** within that same trending move.

##### Critical Interpretive Point
> **Strong Sell on DPO does NOT mean the stock is going down.** It means the stock is **at the top of its current cycle within the trend.**

In the example above, Day 20 shows 🔴 Strong Sell at $183 — but the stock went on to reach $185 by Day 30. The trend continued. What DPO told you was:

- _"Price is stretched above its cycle mean right now"_
- _"The next 5–10 bars are more likely to be flat or pull back slightly"_
- _"This is not the ideal moment to add new exposure"_
- _"Wait for the next trough before adding"_

Not: _"Sell everything, trend is over."_


#### Example 2: Tracking the Cycle Peak with Real Numbers

To make the previous ASCII text diagram clear, let’s look at a concrete, day-by-day numerical example of a hypothetical asset peaking and rolling over.

This table tracks Price, DPO % (our normalized value), and the Sequential Difference (how much the DPO % changed from the previous day).

|Date (Daily Tracker)|Price|DPO % (`DPO/Price * 100`)|Sequential Diff (`.diff()`)|Market Rhythm Meaning|
|---|---|---|---|---|
|May 11|$100.00|`+1.00%`|_Baseline_|The short-term cycle is rising above its historical mean.|
|May 12|$102.00|`+1.40%`|`+0.40%`|Accelerating Upward: The upward wave is actively gaining speed.|
|May 13|$105.00|`+1.70%`|`+0.30%`|Decelerating Upward: Still climbing, but the upward push is losing steam.|
|May 14 (The Peak)|$106.00|`+1.80%`|`+0.10%`|The Crest: The wave has almost completely flattened out.|
|May 15 (The Signal)|$105.50|`+1.75%`|`-0.05%`|The Rollover Warning: DPO % is still high and positive, but the _Sequential Diff turned negative_. The cycle has peaked.|
|May 18|$103.00|`+1.20%`|`-0.55%`|Gaining Downward Velocity: The downward wave is actively accelerating.|
|May 19|$100.00|`0.00%`|`-1.20%`|Zero Cross: The cycle crosses the mean. (Standard indicators finally register this, but your dashboard saw it on May 15).|


This (from 5/11-5/14) is an example of: 
> *When a stock is climbing, the DPO percentage will be positive and growing* (e.g., `+1.2%`, `+1.5%`, `+1.7%`). *The sequential differences are positive* (`+0.3%`, `+0.2%`)."
> - **The Insight:** The moment the sequential difference turns **negative** while the DPO value itself is still high and positive (e.g., the DPO shifts from `+1.8%` to `+1.75%`), it means the cycle has officially peaked and flattened out. This provides a rolling indicator of a top long before the DPO crosses back under the zero line.


##### How to Interpret
- The "Aha!" Moment happens on May 15. On this day, the raw price barely budged, and the DPO % is still sitting at a very high `+1.75%`.
- If you only look at DPO %, it looks safely bullish.
- But because your `DPO_VELOCITY` column flipped from `+0.10%` to `-0.05%`, your dashboard can flag that this ticker's short-term cycle wave has officially rolled over.


---
#### What DPO Actually Does — The Core Mechanic

Most oscillators in your roster (RSI, Stoch, CCI, Williams %R, UO) measure **price momentum or relative position within a recent range.** They all still have the dominant trend embedded in their calculations — a stock in a strong uptrend will have persistently high RSI readings, and a stock in a downtrend will have persistently low ones.

**DPO does something fundamentally different:**
It **surgically removes the dominant trend** from the price series entirely, leaving only the **cyclical oscillation** around that trend. The formula deliberately displaces the moving average backward in time to eliminate trend direction, exposing the underlying rhythm of the market's natural ebb and flow.

The result: DPO tells you **where you are in the current price cycle** — independent of whether the trend is up, down, or sideways.

---
#### Indicator-by-indicator comparison:

|Indicator|What It Measures|Does It Remove Trend?|Cycle Timing?|
|---|---|---|---|
|RSI|Momentum — speed of recent price change|No — trend biases readings|Partial — but trend-contaminated|
|Stochastic|Price position within recent high/low range|No — range expands with trend|Partial — same limitation|
|CCI|Deviation from statistical mean|No — mean moves with trend|Closer — but still trend-influenced|
|Williams %R|Same family as Stochastic|No|Partial|
|Ultimate Osc|Weighted multi-timeframe momentum|No|Partial|
|MACD|EMA convergence/divergence|No — both EMAs follow trend|Divergence only — not cycle position|
|ROC|Raw % price change over N periods|No — trend inflates readings|No|
|**DPO**|**Cyclical position after trend removal**|**Yes — by design**|**Yes — primary purpose**|

**The gap DPO fills:** None of the above indicators explicitly isolate the cyclical component of price movement. They all measure momentum _within_ the trend. DPO measures the cycle _beneath_ the trend.

---

#### Three Practical Situations Where DPO Adds Unique Insight

##### 1. Identifying Cycle Peaks and Troughs in Strong Trends

In a powerful uptrend, RSI stays overbought for weeks — it gives you little actionable information about _when_ within the trend to add, reduce, or time entries. DPO will still oscillate clearly above and below its zero line even while the trend is running, marking the natural exhale/inhale rhythm of the move.

> **Practical use:** In a trending stock where RSI is stuck at 70+, DPO tells you whether you're at a cyclical peak (DPO high = reduce/wait) or a cyclical trough within the trend (DPO low = add to position).

##### 2. Measuring Cycle Length for Better Parameter Setting

Because DPO detrends price, you can count the peaks and troughs clearly and measure the **average cycle length** for a specific instrument. This is analytically valuable because it lets you calibrate _all_ your other indicators' lookback periods to that instrument's actual cycle rather than using generic defaults.

> **Practical use:** If DPO on a particular stock shows a consistent 18-bar cycle, you might adjust your RSI from 14 to 18 for that specific name. Most traders never do this — and it's a genuine edge.

---

##### 3. Divergence in Low-Momentum Environments

When a stock is grinding higher with weak momentum — the kind of slow drift where MACD and ROC give flat, ambiguous signals — DPO's clean cycle oscillation makes divergence **much easier to see**. A series of rising prices with declining DPO cycle peaks is a clear distribution signal that MACD might completely miss in a low-volatility drift.


---



## The Best DPO Pairings

### 1. RSI — The Original Pairing (already mentioned)

**What RSI adds:** Momentum confirmation at the cycle extreme

|DPO Signal|RSI Confirms|Combined Reading|
|---|---|---|
|Strong Buy (< −2%, cycle trough)|RSI < 40 (weak/oversold)|**Highest conviction mean reversion long.** Both cycle position AND momentum confirm exhaustion|
|Strong Buy (< −2%)|RSI > 60 (still strong)|**Trend pullback entry.** Cycle low but momentum healthy — classic add-to-winner setup in uptrend|
|Strong Sell (> +2%, cycle peak)|RSI > 65 (overbought)|**High conviction fade/trim.** Both cycle peak AND momentum stretched — reduce or exit|
|Strong Sell (> +2%)|RSI < 45 (weakening)|**Distribution warning.** Cycle extended but momentum already rolling — price likely to drop sharply|
|Conflicting (DPO neutral)|RSI extreme either direction|**Ignore RSI signal.** No cycle context to support the momentum read — lower quality signal|

---

### 2. ADX — Trend Strength Filter

**What ADX adds:** Tells you _how to interpret_ the DPO signal — cycle timing vs outright reversal
- This is the most important DPO context filter.


|DPO Signal|ADX Context|Combined Reading|
|---|---|---|
|Strong Buy (cycle trough)|ADX > 25|**Add to existing trend position.** Cycle low inside confirmed trend = ideal re-entry|
|Strong Buy (cycle trough)|ADX < 20|**Short-term bounce only.** No trend to ride — quick trade, tight target|
|Strong Sell (cycle peak)|ADX > 25|**Trim/trail stops only.** Cycle peak but trend intact — don't short, just reduce|
|Strong Sell (cycle peak)|ADX < 20|**Legitimate fade.** No trend = cycle peak is a genuine mean reversion short setup|

$$------------------------------------------$$

DPO's signal interpretation does shift slightly depending on the broader trend context, which is exactly why it needs to be read **alongside the "Conviction Filter" bucket** (ADX, BullBear):

|ADX Reading|DPO Signal|Combined Interpretation|
|---|---|---|
|ADX > 25 (strong trend)|Strong Buy (DPO < −2%)|**High conviction add** — cycle trough in a confirmed trend|
|ADX > 25 (strong trend)|Strong Sell (DPO > +2%)|**Trim/wait** — cycle peak but trend intact, don't short|
|ADX < 20 (weak/choppy)|Strong Buy (DPO < −2%)|**Tentative** — cycle low but no trend to ride|
|ADX < 20 (weak/choppy)|Strong Sell (DPO > +2%)|**Legitimate fade** — extended in a trendless market, mean reversion likely|

This is the real professional use case — DPO in isolation is interesting, but DPO filtered through ADX conviction is where it becomes genuinely actionable on a dashboard.

---

### 3. MACD — Momentum Divergence Confirmation

**What MACD adds:** Whether momentum is confirming or diverging at the cycle extreme — the most powerful DPO pairing for catching reversals

|DPO Signal|MACD Condition|Combined Reading|
|---|---|---|
|Strong Buy (cycle trough)|MACD histogram turning positive / crossing up|**Confirmed cycle low.** Cycle position AND momentum both turning — high conviction entry|
|Strong Buy (cycle trough)|MACD still declining|**Cycle low not confirmed yet.** DPO may be early — wait for MACD to stabilize before entering|
|Strong Sell (cycle peak)|MACD histogram turning negative / crossing down|**Confirmed cycle peak.** Both signals agree momentum is rolling — trim aggressively|
|Strong Sell (cycle peak)|MACD still rising|**DPO early.** Cycle extended but momentum still positive — hold a bit longer, tighten stops|
|DPO at cycle peak + price making new high|MACD making lower high|**Classic bearish divergence confirmed by cycle position.** One of the strongest reversal signals in the entire framework|
|DPO at cycle trough + price making new low|MACD making higher low|**Classic bullish divergence confirmed by cycle position.** Equally powerful to the above|

> The MACD divergence + DPO cycle position combination is particularly valuable — DPO tells you _you're at a cycle extreme_ while MACD divergence tells you _momentum isn't confirming the price extreme._ Together they're a much stronger signal than either alone.

---

### 4. OBV — Volume Confirmation at Cycle Extremes

**What OBV adds:** Whether volume is supporting or contradicting the cycle position

|DPO Signal|OBV Condition|Combined Reading|
|---|---|---|
|Strong Buy (cycle trough)|OBV rising or flat (accumulation)|**Confirmed cycle low.** Price at cycle trough but volume shows accumulation — smart money buying the dip|
|Strong Buy (cycle trough)|OBV declining (distribution)|**Trap.** Cycle low forming but volume shows selling — don't buy, possible larger decline ahead|
|Strong Sell (cycle peak)|OBV declining (distribution)|**Confirmed cycle peak.** Price extended AND volume shows smart money exiting — strong trim signal|
|Strong Sell (cycle peak)|OBV still rising|**Cycle extended but supported.** Volume not confirming the peak — hold a little longer before trimming|

---

### 5. Bollinger Bands — Cycle Position + Statistical Extremes

**What Bollinger adds:** Whether the cycle extreme coincides with a statistical price extreme — amplifies the DPO signal significantly

|DPO Signal|Bollinger Condition|Combined Reading|
|---|---|---|
|Strong Buy (cycle trough)|Price at or below lower BB|**Double extreme confirmation.** Cycle low + statistical oversold = highest conviction mean reversion setup|
|Strong Buy (cycle trough)|Price near BB midline|**Mild cycle trough only.** No statistical extreme to amplify it — standard add opportunity|
|Strong Sell (cycle peak)|Price at or above upper BB|**Double extreme — trim aggressively.** Cycle peak + statistical overbought = overextension on both measures|
|Strong Sell (cycle peak)|Price near BB midline|**Cycle peak without statistical stretch.** Less urgent — monitor but not a strong action signal|
|DPO cycle trough + price below lower BB|BB beginning to contract|**Mean reversion imminent.** Cycle, statistics, and volatility all pointing to snapback — strong entry|

---

### 6. ATR — Cycle Timing + Volatility Context

**What ATR adds:** Whether there's enough volatility energy at the cycle extreme to actually generate a tradeable move

|DPO Signal|ATR Condition|Combined Reading|
|---|---|---|
|Strong Buy (cycle trough)|ATR expanding|**Actionable cycle low.** Volatility increasing at the trough = the move out of it will be meaningful|
|Strong Buy (cycle trough)|ATR contracting|**Low energy cycle low.** Cycle trough but volatility dying — bounce may be weak and short-lived|
|Strong Sell (cycle peak)|ATR expanding|**Volatile peak.** Expansion at cycle high = sharp reversal possible — trim quickly|
|Strong Sell (cycle peak)|ATR contracting|**Slow rollover.** Cycle peak but low volatility — likely a gradual drift rather than sharp decline|

---

### Priority Ranking — Which Pairings Matter Most

If you can only watch a few alongside DPO:

|Priority|Pairing|Why|
|---|---|---|
|1|**DPO + ADX**|Determines how to _interpret_ the signal — trend timing vs outright reversal|
|2|**DPO + MACD**|Divergence confirmation at cycle extremes is the most powerful signal DPO generates|
|3|**DPO + RSI**|Momentum confirmation at cycle extremes — the classic pairing|
|4|**DPO + OBV**|Volume confirmation — is smart money agreeing with the cycle position?|
|5|**DPO + Bollinger**|Statistical extreme amplification — doubles the conviction when both fire together|
|6|**DPO + ATR**|Volatility energy check — is there enough power behind the cycle extreme to trade?|

---

The core principle across all six: **DPO tells you _where_ you are in the cycle. Every companion indicator answers a different question about _whether_ that cycle position is worth acting on.**


---


#### Metrics


$\large{\textsf{1) Cross-Ticker Comparison: Yes, with a Big Catch}}$

Expressing the DPO as a percentage **perfectly normalizes the vertical amplitude**. This means you can directly compare how far away two completely different tickers are from their underlying cycle means. 

- **The Benefit:** If Apple (AAPL) is trading at $180 and has a DPO % value of `+2.0%`, and a micro-cap stock is trading at $5 and has a DPO % value of `+2.0%`, you know both stocks are pushed exactly **2% above their short-term structural means**, regardless of their nominal stock price.
- **The Catch:** While it normalizes the **price scale**, it _does not_ normalize the **volatility profile**. High-beta or tech stocks will naturally swing between +/- 8% on a 20-period DPO %, while utility stocks or consumer staples might max out at +/- 1.5%.

> **Dashboard Tip:** To rank or sort multiple tickers seamlessly, do not just look at the raw percentage. Instead, divide your new DPO % by the asset’s [Average True Range (ATR) as a % of price](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/percentage-price-oscillator-ppo). This yields a volatility-adjusted cycle score


---
$\large{\textsf{Does the Raw DPO Value Tell You Anything??}}$
The raw DPO value is an **absolute dollar metric** (or point metric, if tracking an index like the S&P 500). It represents the literal currency distance between the past price and its centered moving average. 

- **Information Value-Added:** Raw DPO tells you the exact financial overhead or cushion currently built into the asset's cycle wave. 
	- For options traders, a raw DPO value of `+$4.50` indicates that the short-term cycle has stretched $4.50 past its equilibrium point. 
	- This provides a direct, dollar-denominated figure to weigh against options premiums or expected strike targets.
- **The Downside:** It suffers from severe **price-drift distortion**. 
	- If a stock runs from $20 to $100 over three years, a raw DPO fluctuation of `+$2.00` is massive at the start (a 10% move) but completely negligible noise at the end (a 2% move)


---

$\large{\textsf{Do Sequential Differences Offer Any Insight?}}$

Yes. Calculating the sequential difference—the rate of change of the DPO from row to row—yields **significant predictive value for cycle inflection points**.

Mathematically, calculating the day-over-day change of the DPO behaves like taking the **first derivative of the cyclical wave**.

```python
# In pandas, this is simply:
df['DPO_ROC'] = df['DPO_20'].diff()
```

When you track sequential differences on your dashboard, look for these two structural insights:

```
    DPO Value:     ▲ Upward Wave     │    ▼ Downward Wave
                   ▲                 │                 ▼
  ───────────────┼─▲─────────────────┼─────────────────▼─┼──────── (Zero Line)
                 │   ▲               │               ▼   │
                 │     ▲             │             ▼     │
  Sequential     │                   │                   │
  Difference:    (Positive & Rising) (Turns Negative Here)(Negative & Dropping)
                                     ▲
                             [Cycle Top Peak]
```

**Cycle Top Acceleration Signals:**

When a stock is climbing, the DPO percentage will be positive and growing (e.g., `+1.2%`, `+1.5%`, `+1.7%`). The sequential differences are positive (`+0.3%`, `+0.2%`).

- **The Insight:** The moment the sequential difference turns **negative** while the DPO value itself is still high and positive (e.g., the DPO shifts from `+1.8%` to `+1.75%`), it means the cycle has officially peaked and flattened out. This provides a rolling indicator of a top long before the DPO crosses back under the zero line. [[1](https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dpo)]

**Momentum Velocity Filtering**:

If the raw price spikes up violently on an earnings gap, standard momentum indicators will skyrocket.

- **The Insight:** Because DPO shifts the moving average baseline backward, a massive day-over-day spike in sequential difference highlights whether the sudden price burst is pushing the asset outside its historical wave rhythm, or if it is merely catch-up noise within a standard cycle envelope