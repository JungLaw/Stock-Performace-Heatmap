# Moving-Average Crossover Event Rows

Moving-average crossover rows identify the exact date when a faster moving average crosses a slower moving average.

In this dashboard, crossover rows are **event-only rows**. They mark the crossover event date itself. They do not classify every day as bullish or bearish simply because one moving average is above or below another.

---

## Rows currently supported

The first-wave crossover rows are:

| Row | Fast average | Slow average | Typical use |
|---|---:|---:|---|
| EMA 9/21 Cross | EMA(9) | EMA(21) | Short-term trend and momentum shifts |
| SMA 20/50 Cross | SMA(20) | SMA(50) | Medium-term trend shifts |
| SMA 50/200 Cross | SMA(50) | SMA(200) | Long-term trend shifts, often associated with golden/death cross analysis |

---

## What the score means

Crossover rows use event-only scoring:

| Score | Meaning |
|---:|---|
| +2 | Bullish crossover event: the fast moving average crossed above the slow moving average on this date |
| -2 | Bearish crossover event: the fast moving average crossed below the slow moving average on this date |
| 0 | Valid no-event date: no crossover occurred on this date |
| Blank | Insufficient data, warmup period, or missing base data |

A score of `0` does **not** mean the setup is unimportant. It only means no new crossover event occurred on that date.

> NOTE: Difference between "Raw Crossover Event Value" & displayed "Scored Signal Value"
> The crossover rule expressions classify the 'raw event' column using thresholds: `> 0.5` becomes `strong_buy`, `< -0.5` becomes `strong_sell`, and `abs(...) <= 0.5` becomes neutral. 
> - The rulebook notes currently describe the raw event values as `1`, `-1`, and `0`.  
> 
> The rule engine maps bullish events to +2, bearish events to -2, and no-event to 0.
> - This is the 'scored' signal value that's displayed.

---

## Event row vs trend state

A crossover row answers:

> Did the crossover happen on this date?

It does not answer:

> Is the fast moving average currently above or below the slow moving average?

For example, after a bullish crossover, the fast average may remain above the slow average for many days. Only the crossover date receives the bullish event score. Later days normally show `0` unless a new crossover occurs.

This avoids double-counting a past event as if it were a fresh signal every day.

---

## Fast/Slow MA vs. Price
- "Where is price relative to the averages that will be pulled by future closes?"

## How to read spread

The hover displays a spread value:

```text
Spread = Fast MA - Slow MA
```

Examples:

```text
SMA(20) = 372.67
SMA(50) = 366.36
Spread  = +6.31
```

A positive spread means the fast moving average is above the slow moving average.

A negative spread means the fast moving average is below the slow moving average.

A spread near zero means the moving averages are close to crossing.

### `Spread % of Price`
Spread % of Price:
- How far apart are the MAs, normalized by price?

Spread % bps change:
- Is the MA gap compressing or widening vs. yesterday?

---

## Prior spread and spread compression

The hover may also show prior spread.

Example:

```text
Prior spread:   +8.67
Current spread: +6.31
```

The spread compressed by:

```text
8.67 - 6.31 = 2.36
```

That means the fast and slow moving averages moved closer together from the prior bar to the current bar.

Spread compression can be useful context because a crossover may be approaching even when no event has occurred yet.

---

## Estimated Days to Cross

`Estimated Days to Cross` is a simple spread-velocity estimate.

It answers:

> If the moving-average spread keeps shrinking at the most recent one-bar pace, when would the spread reach zero?

Example:

```text
Prior spread:   +8.67
Current spread: +6.31
Compression:     2.36

6.31 / 2.36 = 2.67
```

Rounded up:

```text
Estimated Days to Cross: 3 trading days
```

This is a **naive estimate**. It does not simulate future prices or future moving-average windows. It only extrapolates the most recent change in spread.

If the spread is widening, flat, missing, or the estimate is too far out, the dashboard shows an `N/A` explanation instead.

---

## Price Needed to Force Cross

`Price Needed to Force Cross` answers a very strict question:

> What next close would force the fast moving average and slow moving average to be equal on the next bar?

This is not a price target. It is not a forecast. It is a one-bar mathematical trigger.

For SMA crossovers, the next close must account for the rolling-window drop-off effect:

```text
SMA_fast_next = (current fast-window sum - oldest fast-window close + next close) / fast length

SMA_slow_next = (current slow-window sum - oldest slow-window close + next close) / slow length
```

The dashboard solves for the next close that would make:

```text
SMA_fast_next = SMA_slow_next
```

Because moving averages move slowly, the one-day force-cross price can be far away from the current price, especially when the spread is still large.

---

## Required Move

`Required Move` shows the distance between the current price and the `Price Needed to Force Cross`.

Example:

```text
Current close:                $363.79
Price Needed to Force Cross:  $226.22
Required Move:               -$137.57 (-37.8%)
```

This means:

> To force the crossover on the next bar, price would need to close 37.8% lower than the current close.

It does not mean the stock is expected to move there.

---

## Impractical one-day trigger guard

The dashboard flags extreme one-bar trigger moves as impractical.

Current guard:

```text
CROSSOVER_MAX_REQUIRED_MOVE_PCT = 20.0
```

If the required one-day move is larger than 20%, the hover marks it as:

```text
impractical one-day trigger
```

Example:

```text
Price Needed to Force Cross: $226.22 - impractical one-day trigger
Required Move: -137.57 (-37.8%) - impractical one-day trigger
```

The value is still shown because the math is valid. The guard simply warns that the value should not be interpreted as a practical short-term target.

---

## Estimated-days guard

The dashboard also limits spread-velocity estimates.

Current guard:

```text
CROSSOVER_MAX_ESTIMATED_DAYS = 60
```

If the naive estimate is more than 60 trading days away, the dashboard displays an `N/A` message rather than presenting a long-range estimate with false precision.

---

## Why price relative to both moving averages matters

This matters because current price is the new input pulling the averages around.

> Price below both MAs:
> - Current closes may pull the fast MA down faster than the slow MA.

> Price above both MAs:
> - Current closes may pull the fast MA up faster than the slow MA.

> Price between the MAs:
> - Mixed/transitional pressure.

---
The crossover event itself is based on the relationship between the fast and slow moving averages. However, the current price provides important context.

### Price below both moving averages

If price is below both the fast and slow moving averages, it may apply downward pressure to the fast average first. 
- This can increase 'bearish convergence risk', especially if the fast average is still above the slow average but falling toward it.

Example interpretation:

```text
Fast MA is above Slow MA, but price is below both.
```

This can mean:

> The chart has not printed a bearish crossover yet, but current prices may be pulling the fast average down toward the slow average.

### Price above both moving averages

If price is above both moving averages, it may apply upward pressure to the fast average first. 
- This can increase 'bullish convergence' or 'continuation risk', especially if the fast average is below the slow average but rising toward it.

Example interpretation:

```text
Fast MA is below Slow MA, but price is above both.
```

This can mean:

> The chart has not printed a bullish crossover yet, but current prices may be pulling the fast average upward toward the slow average.

### Price between the moving averages

If price is between the fast and slow moving averages, interpretation is more mixed. It may still contribute to convergence, but the direction and strength depend on which average is above, how wide the spread is, and how the spread is changing.

---

## Cross type

`Cross type` indicates the active or next possible crossover direction.

On an event day:

* A bullish event means the fast average crossed above the slow average.
* A bearish event means the fast average crossed below the slow average.

On a non-event day, the dashboard infers the next possible cross from the current spread:

|        Current spread | Current structure | Next possible cross |
| --------------------: | ----------------- | ------------------- |
| Fast MA above Slow MA | Positive spread   | Bearish cross       |
| Fast MA below Slow MA | Negative spread   | Bullish cross       |

This is not a forecast. It only identifies the direction of the next possible crossing event.

---

## Practical interpretation checklist

When reviewing a crossover row, read the hover in this order:

1. **Event value**
   Did a crossover happen on this date?

2. **Spread**
   How far apart are the moving averages?

3. **Prior spread**
   Is the spread narrowing or widening?

4. **Price location**
   Is price above both averages, below both averages, or between them?

5. **Estimated Days to Cross**
   If the spread keeps changing at the latest pace, how soon might it reach zero?

6. **Price Needed to Force Cross / Required Move**
   What next close would force an immediate crossover, and is that move practical?

---

## Limitations

Crossover rows are useful event markers, but they are lagging by design.

They should not be interpreted as standalone forecasts.

Important limitations:

* Moving averages lag price.
* Event-only rows do not describe ongoing bullish or bearish state.
* `Estimated Days to Cross` is a naive spread-velocity estimate.
* `Price Needed to Force Cross` is a next-bar mathematical trigger, not a target.
* Large required moves should be treated as impractical one-day triggers.
* Price context matters, especially whether price is above both averages, below both averages, or between them.

---

## What this row does not do

This row does not introduce:

* event + state scoring
* regime logic
* composite signals
* cross-confirmation logic
* ranking
* aggregate technical strength
* UI-local scoring

It remains an event-only signal row.
