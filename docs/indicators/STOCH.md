
## Summary: STOCH(14,3,3) 'Signals'

| Signal | Literal trigger | Layman’s Translation | Rule Logic | Bottom-line|
| --- | --- | --- | --- |--- |
| `strong_buy` | `%K < 20`, `%K > %D`, and `%K rose from the prior bar` | STOCH is oversold, and `%K` has turned upward strongly enough to move above `%D`. | The oscillator is in the oversold zone, `%K` is above its smoothed signal line, and `%K` is rising versus the immediately preceding period. |Price looks beaten down, but may be starting to rise.|
| `buy` | `%K < 20` and the full Strong Buy confirmation is absent | STOCH is oversold, but the upward reversal is not fully confirmed. | The oscillator is in the oversold zone, but `%K` is either not above `%D` or is not rising from the prior bar. |Trading at the low end of its 14-day range.|
| `neutral` | `20 <= %K <= 80` | STOCH is between its usual oversold and overbought zones. | `%K` is inside the middle range, including the exact boundary values of `20` and `80`. | Price is somewhere in the middle of its 14-day range|
| `sell` | `%K > 80` and the full Strong Sell confirmation is absent | STOCH is overbought, but the downward reversal is not fully confirmed. | The oscillator is in the overbought zone, but `%K` is either not below `%D` or is not falling from the prior bar. |Trading at the high-end of its 14-day range.|
| `strong_sell` | `%K > 80`, `%K < %D`, and `%K fell from the prior bar` | STOCH is overbought, and `%K` has turned downward strongly enough to move below `%D`. | The oscillator is in the overbought zone, `%K` is below its smoothed signal line, and `%K` is falling versus the immediately preceding period. |Looks stretched. Trading at the high-end of its 14-day range; showing signs of fatigue.|

---

## STOCH(14,3,3) — brief overview

For `STOCH(14,3,3)`:

```text
14 = high-low lookback period
3  = %K smoothing period
3  = %D smoothing period
```

The Stochastic Oscillator measures where the current closing price sits within the recent high-low range.

Its main components are:

```text
%K = the primary oscillator line
%D = a smoothed signal line derived from %K
```

Both are normally bounded between `0` and `100`.

A simplified conceptual formula is:

```text
%K = 100 × (current close − lowest low)
           ÷ (highest high − lowest low)
```

The exact implementation also applies the configured smoothing periods.

Simple interpretation:

* A high `%K` means price is closing near the upper end of its recent range.
* A low `%K` means price is closing near the lower end of its recent range.
* `%K < 20` is treated as oversold.
* `%K > 80` is treated as overbought.
* `%K > %D` means the faster oscillator line is above its smoothed signal line.
* `%K < %D` means the faster oscillator line is below its smoothed signal line.
* A rising `%K` suggests short-term momentum within the range is improving.
* A falling `%K` suggests short-term momentum within the range is weakening.

An oversold or overbought reading is not, by itself, proof that price will reverse. A security can remain near an extreme while a strong trend continues. The project therefore distinguishes between:

```text
Buy / Sell
= an extreme-zone condition without full reversal confirmation

Strong Buy / Strong Sell
= an extreme-zone condition plus %K/%D positioning
  and one-bar %K direction confirmation
```

### Value-added use

> Use STOCH(14,3,3) when you want a balanced momentum oscillator that identifies when price is near the upper or lower end of its recent range and distinguishes an unconfirmed extreme from a developing reversal.

This middle setting is intended to balance responsiveness and noise. It is generally less reactive than `STOCH(5,3,3)` and faster than the more heavily smoothed `STOCH(21,5,5)`.

### Use with

STOCH is most useful when interpreted with trend, momentum, and participation context.

* **EMA or SMA** — to determine whether an oversold or overbought condition is occurring with or against the prevailing trend.
* **ADX** — to distinguish a strong trend, where an extreme may persist, from a weaker environment where reversal signals may be more actionable.
* **MACD or ROC** — to check whether broader momentum supports the `%K/%D` turn.
* **RSI or MFI** — to see whether another bounded oscillator confirms that price is stretched.
* **Volume, OBV, or CMF** — to check whether participation supports the reversal.
* **Support and resistance** — an oversold or overbought turn near a meaningful price level is generally more informative than the same signal in isolation.

### Important distinction

The rule set uses a **contrarian-plus-reversal-confirmation** model.

The extreme zone supplies the contrarian setup:

```text
%K < 20 → oversold setup
%K > 80 → overbought setup
```

The Strong state requires added reversal evidence:

```text
Strong Buy:
%K is oversold
+ %K is above %D
+ %K rose from the prior bar

Strong Sell:
%K is overbought
+ %K is below %D
+ %K fell from the prior bar
```

The rules do not require a literal crossover to occur on the current bar. The hover field `Cross` reports whether an actual bullish or bearish `%K/%D` crossover occurred that day, but crossover status is display context rather than a scoring requirement.

---

## STOCH(14,3,3) Rule Translation

### Strong buy

```json
"strong_buy": "STOCHK_14_3_3 < 20 and STOCHK_14_3_3 > STOCHD_14_3_3 and rising_2bar(STOCHK_14_3_3, 1)"
```

#### Literal component breakdown

`STOCHK_14_3_3 < 20`

* The current `%K` value is below `20`.
* The oscillator is in the project’s oversold zone.
* Layman’s translation: **price is closing near the lower end of its recent 14-period range.**

`STOCHK_14_3_3 > STOCHD_14_3_3`

* The faster `%K` line is above the smoothed `%D` signal line.
* This indicates that short-term oscillator momentum has improved relative to its smoother baseline.
* Layman’s translation: **the faster Stochastic line has moved above its slower signal line.**

`rising_2bar(STOCHK_14_3_3, 1)`

* Despite the helper’s legacy name, the explicit argument `1` makes this a current-versus-prior-period comparison.
* The current `%K` value is greater than the immediately preceding `%K` value.
* Layman’s translation: **%K has risen since the prior period.**

#### Literal summary

`%K` is below `20`, `%K` is above `%D`, and `%K` is higher than it was one period earlier.

#### Plain-English version

That means STOCH is oversold, but `%K` is now rising and sits above its smoothed `%D` line.

#### Interpretation

This is a **strong bullish reversal-confirmation state from the oversold zone**.

It requires three layers:

1. `%K` is in the oversold zone;
2. `%K` is above `%D`;
3. `%K` is rising from the prior period.

The rule is stronger than a simple oversold reading because it requires evidence that oscillator momentum is turning upward.

#### Notes / confidence

* The `20` threshold is a conventional Stochastic oversold reference.
* The `%K > %D` relationship is commonly interpreted as bullish oscillator positioning.
* The one-bar rise is a project-selected confirmation rule intended to identify the turn promptly without the additional lag of a two-consecutive-move requirement.
* This is a reversal-confirmation state, not a guarantee that price has formed a durable bottom.
* An actual bullish crossover may have occurred on the same bar or earlier. The rule requires current positioning, not a current-bar crossover event.

---

### Buy

```json
"buy": "STOCHK_14_3_3 < 20 and (STOCHK_14_3_3 <= STOCHD_14_3_3 or not_rising_2bar(STOCHK_14_3_3, 1))"
```

#### Literal component breakdown

`STOCHK_14_3_3 < 20`

* The current `%K` value is below `20`.
* The oscillator is in the oversold zone.
* Layman’s translation: **price is closing near the lower end of its recent range.**

`STOCHK_14_3_3 <= STOCHD_14_3_3`

* `%K` is below or equal to `%D`.
* The faster oscillator line has not established bullish positioning above its smoothed signal line.
* Layman’s translation: **%K has not moved above %D.**

`not_rising_2bar(STOCHK_14_3_3, 1)`

* The current `%K` value is not greater than the immediately preceding `%K` value.
* `%K` is flat or falling versus the prior period.
* Layman’s translation: **%K has not risen since the prior period.**

`... <= STOCHD ... or not_rising_2bar(...)`

* Only one of these conditions needs to be true.
* The rule captures every oversold observation that does not satisfy the complete Strong Buy combination.
* Layman’s translation: **STOCH is oversold, but at least one required reversal confirmation is still missing.**

#### Literal summary

`%K` is below `20`, but `%K` is either not above `%D` or not rising from the prior period.

#### Plain-English version

That means STOCH is oversold, but the upward reversal is not fully confirmed.

#### Interpretation

This is a **bullish contrarian extreme-zone condition without complete reversal confirmation**.

The signal acknowledges that price is near the lower end of its recent range, but it does not claim that momentum has decisively turned upward.

#### Notes / confidence

* `Buy` is intentionally weaker than `Strong Buy`.
* It can occur while `%K` is still below `%D`, while `%K` is still falling, or both.
* The signal should be read as “oversold setup” rather than “confirmed bottom.”
* In a strong downtrend, STOCH may remain oversold and continue producing a Buy state without an immediate price reversal.

---

### Neutral

```json
"neutral": "20 <= STOCHK_14_3_3 <= 80"
```

#### Literal component breakdown

`20 <= STOCHK_14_3_3`

* `%K` is at least `20`.
* It is not below the oversold threshold.
* Layman’s translation: **%K is no longer in the oversold zone.**

`STOCHK_14_3_3 <= 80`

* `%K` is no greater than `80`.
* It is not above the overbought threshold.
* Layman’s translation: **%K has not entered the overbought zone.**

`20 <= STOCHK_14_3_3 <= 80`

* `%K` lies within the middle range.
* The exact values `20` and `80` are included in Neutral.
* Layman’s translation: **STOCH is between its two extreme zones.**

#### Literal summary

`%K` is between `20` and `80`, inclusive.

#### Plain-English version

That means price is not currently closing near enough to the top or bottom of its recent range to activate an extreme-zone signal.

#### Interpretation

This is a **middle-range / no-active-extreme state**.

Neutral does not mean that price has no momentum or no trend. It means only that the Stochastic `%K` value is not inside the rule set’s oversold or overbought zones.

#### Notes / confidence

* `%K = 20` is Neutral.
* `%K = 80` is Neutral.
* `%K/%D` positioning and one-bar direction do not change the classification while `%K` remains in this middle range.
* The rule deliberately reserves Buy/Sell classifications for readings strictly outside the middle band.

---

### Sell

```json
"sell": "STOCHK_14_3_3 > 80 and (STOCHK_14_3_3 >= STOCHD_14_3_3 or not_falling_2bar(STOCHK_14_3_3, 1))"
```

#### Literal component breakdown

`STOCHK_14_3_3 > 80`

* The current `%K` value is above `80`.
* The oscillator is in the overbought zone.
* Layman’s translation: **price is closing near the upper end of its recent range.**

`STOCHK_14_3_3 >= STOCHD_14_3_3`

* `%K` is above or equal to `%D`.
* The faster oscillator line has not established bearish positioning below its smoothed signal line.
* Layman’s translation: **%K has not moved below %D.**

`not_falling_2bar(STOCHK_14_3_3, 1)`

* The current `%K` value is not below the immediately preceding `%K` value.
* `%K` is flat or rising versus the prior period.
* Layman’s translation: **%K has not fallen since the prior period.**

`... >= STOCHD ... or not_falling_2bar(...)`

* Only one of these conditions needs to be true.
* The rule captures every overbought observation that does not satisfy the complete Strong Sell combination.
* Layman’s translation: **STOCH is overbought, but at least one required bearish reversal confirmation is still missing.**

#### Literal summary

`%K` is above `80`, but `%K` is either not below `%D` or not falling from the prior period.

#### Plain-English version

That means STOCH is overbought, but the downward reversal is not fully confirmed.

#### Interpretation

This is a **bearish contrarian extreme-zone condition without complete reversal confirmation**.

The signal recognizes that price is near the upper end of its recent range, but it does not claim that momentum has decisively turned downward.

#### Notes / confidence

* `Sell` is intentionally weaker than `Strong Sell`.
* It can occur while `%K` remains above `%D`, while `%K` is still rising, or both.
* The signal should be read as “overbought setup” rather than “confirmed top.”
* In a strong uptrend, STOCH may remain overbought and continue producing a Sell state without an immediate price reversal.

---

### Strong sell

```json
"strong_sell": "STOCHK_14_3_3 > 80 and STOCHK_14_3_3 < STOCHD_14_3_3 and falling_2bar(STOCHK_14_3_3, 1)"
```

#### Literal component breakdown

`STOCHK_14_3_3 > 80`

* The current `%K` value is above `80`.
* The oscillator is in the project’s overbought zone.
* Layman’s translation: **price is closing near the upper end of its recent 14-period range.**

`STOCHK_14_3_3 < STOCHD_14_3_3`

* The faster `%K` line is below the smoothed `%D` signal line.
* This indicates that short-term oscillator momentum has weakened relative to its smoother baseline.
* Layman’s translation: **the faster Stochastic line has moved below its slower signal line.**

`falling_2bar(STOCHK_14_3_3, 1)`

* Despite the helper’s legacy name, the explicit argument `1` makes this a current-versus-prior-period comparison.
* The current `%K` value is lower than the immediately preceding `%K` value.
* Layman’s translation: **%K has fallen since the prior period.**

#### Literal summary

`%K` is above `80`, `%K` is below `%D`, and `%K` is lower than it was one period earlier.

#### Plain-English version

That means STOCH is overbought, but `%K` is now falling and sits below its smoothed `%D` line.

#### Interpretation

This is a **strong bearish reversal-confirmation state from the overbought zone**.

It requires three layers:

1. `%K` is in the overbought zone;
2. `%K` is below `%D`;
3. `%K` is falling from the prior period.

The rule is stronger than a simple overbought reading because it requires evidence that oscillator momentum is turning downward.

#### Notes / confidence

* The `80` threshold is a conventional Stochastic overbought reference.
* The `%K < %D` relationship is commonly interpreted as bearish oscillator positioning.
* The one-bar decline is a project-selected confirmation rule intended to identify the turn promptly without the additional lag of a two-consecutive-move requirement.
* This is a reversal-confirmation state, not a guarantee that price has formed a durable top.
* An actual bearish crossover may have occurred on the same bar or earlier. The rule requires current positioning, not a current-bar crossover event.

---

## Industry-standard baseline

Standard Stochastic interpretation usually emphasizes:
* Stochastic ranges from **0 to 100** and shows where the close sits relative to the recent high-low range.
* The common overbought / oversold zones are **above 80** and **below 20**.
  * A classic '*buy*' signal ("Oversold") often involves Stochastic (**'`%K`'**) moving up from oversold, especially below/around 20.
  * A classic '*sell*' signal  ("Overbought") often involves Stochastic (**'`%K`'**) moving down from overbought, especially above/around 80.
* **`%K/%D`** crosses or relative positioning can suggest improving or weakening oscillator momentum.
  * %K / %D crossovers are often most meaningful when they occur in overbought or oversold zones, not necessarily in the middle of the range. 
* Extreme readings should be interpreted in trend context because an oscillator can remain overbought or oversold during a persistent trend.

Industry practice does not usually define the project’s exact five-level scoring system. A basic industry-style interpretation is:

| Condition | Basic translation |
| --- | --- |
| `%K < 20` | Oversold; price is closing near the bottom of its recent range. |
| `%K < 20` and `%K` turns above `%D` | Potential bullish reversal from oversold territory. |
| `20 <= %K <= 80` | Middle range; no active Stochastic extreme. |
| `%K > 80` | Overbought; price is closing near the top of its recent range. |
| `%K > 80` and `%K` turns below `%D` | Potential bearish reversal from overbought territory. |

The project adds a formal distinction between an unconfirmed extreme and a reversal-confirmed Strong state.




---

## Comparison of the three Stochastic settings

All three settings use the same `20/80` zones and the same five-state Model E logic. Their main difference is responsiveness.

| Setting | Relative speed | What it emphasizes | When it is most applicable | Main trade-off |
| --- | --- | --- | --- | --- |
| `STOCH(5,3,3)` | Fastest | Very recent shifts in range position and momentum | Short-term monitoring, faster swing setups, and cases where early reversal evidence matters | More responsive, but more sensitive to short-lived noise and rapid state changes |
| `STOCH(14,3,3)` | Balanced | A conventional intermediate view of range position and momentum | General-purpose daily analysis and a balance between early response and stability | May react later than the 5-period version but remains more responsive than the 21-period version |
| `STOCH(21,5,5)` | Slowest and smoothest | More persistent changes in range position and momentum | Slower swing analysis, confirmation-oriented use, and cases where fewer state changes are preferred | Filters more noise but can confirm turns later |

### Practical selection guide

```text
Use STOCH(5,3,3)
when speed is more important than stability.

Use STOCH(14,3,3)
when you want the balanced default.

Use STOCH(21,5,5)
when stability and persistence are more important than early response.
```

The settings should not be treated as three independent votes of equal meaning. They are different time-horizon views of the same underlying oscillator concept.

---

## Rule interpretation tables

### STOCH(14,3,3) Rules interpretation

| Source | Signal | Rule logic | What's happening | Answers the question| Bottom-line|
| --- | --- | --- | --- | --- | --- |
| **STOCH(14,3,3)** | Strong Buy | `STOCHK_14_3_3 < 20 and STOCHK_14_3_3 > STOCHD_14_3_3 and rising_2bar(STOCHK_14_3_3, 1)` | STOCH is oversold, and `%K` is rising above `%D`. | *“Is STOCH oversold and showing a confirmed upward turn?”* | Near the bottom of its recent range, and the indicator is showing a confirmed upward turn|
| **STOCH(14,3,3)** | Buy | `STOCHK_14_3_3 < 20 and (STOCHK_14_3_3 <= STOCHD_14_3_3 or not_rising_2bar(STOCHK_14_3_3, 1))` | STOCH is oversold, but the upward turn is not fully confirmed. | *“Is STOCH oversold w/o complete bullish reversal confirmation?”* |Near the bottom of its recent range, but the indicator has not yet confirmed a clear upward turn.|
| **STOCH(14,3,3)** | Neutral | `20 <= STOCHK_14_3_3 <= 80` | STOCH is between its oversold and overbought zones. | *“Is STOCH currently outside both extreme zones?”* |Trading in the middle portion of its recent range rather than near either extreme.|
| **STOCH(14,3,3)** | Sell | `STOCHK_14_3_3 > 80 and (STOCHK_14_3_3 >= STOCHD_14_3_3 or not_falling_2bar(STOCHK_14_3_3, 1))` | STOCH is overbought, but the downward turn is not fully confirmed. | *“Is STOCH overbought w/o complete bearish reversal confirmation?”* |Trading near the top of its recent range, but the indicator has not yet confirmed a clear downward turn.|
| **STOCH(14,3,3)** | Strong Sell | `STOCHK_14_3_3 > 80 and STOCHK_14_3_3 < STOCHD_14_3_3 and falling_2bar(STOCHK_14_3_3, 1)` | STOCH is overbought, and `%K` is falling below `%D`. | *“Is STOCH overbought and showing a confirmed downward turn?”* |Trading near the top of its recent range, and the indicator is showing a confirmed downward turn.|

### STOCH(5,3,3) Rules interpretation

| Source | Signal | Rule logic | What's happening | Answers the question| Bottom-line|
| --- | --- | --- | --- | --- | --- |
| **STOCH(5,3,3)** | Strong Buy | `STOCHK_5_3_3 < 20 and STOCHK_5_3_3 > STOCHD_5_3_3 and rising_2bar(STOCHK_5_3_3, 1)` | The fast STOCH is oversold, and `%K` is rising above `%D`. | *“Is the short-term STOCH oversold and already turning upward?”* | Trading near the low end of its recent range and now appears to be turning upward.|
| **STOCH(5,3,3)** | Buy | `STOCHK_5_3_3 < 20 and (STOCHK_5_3_3 <= STOCHD_5_3_3 or not_rising_2bar(STOCHK_5_3_3, 1))` | The fast STOCH is oversold, but the upward turn is incomplete. | *“Is the short-term STOCH oversold w/o full bullish confirmation?”* |Price looks low compared with its recent range, but there is not yet enough evidence of a rebound.|
| **STOCH(5,3,3)** | Neutral | `20 <= STOCHK_5_3_3 <= 80` | The fast STOCH is between its two extreme zones. | *“Is the short-term STOCH outside both extreme zones?”* |Price is neither especially high nor especially low compared with its recent range.|
| **STOCH(5,3,3)** | Sell | `STOCHK_5_3_3 > 80 and (STOCHK_5_3_3 >= STOCHD_5_3_3 or not_falling_2bar(STOCHK_5_3_3, 1))` | The fast STOCH is overbought, but the downward turn is incomplete. | *“Is the short-term STOCH overbought w/o full bearish confirmation?”* |Price looks high compared with its recent range, but there is not yet enough evidence of a pullback.|
| **STOCH(5,3,3)** | Strong Sell | `STOCHK_5_3_3 > 80 and STOCHK_5_3_3 < STOCHD_5_3_3 and falling_2bar(STOCHK_5_3_3, 1)` | The fast STOCH is overbought, and `%K` is falling below `%D`. | *“Is the short-term STOCH overbought and already turning downward?”* |Price has been trading near the high end of its recent range and now appears to be turning downward.|

### STOCH(21,5,5) Rules interpretation

| Source | Signal | Rule logic | What's happening | Answers the question| Bottom-line|
| --- | --- | --- | --- | --- | --- |
| **STOCH(21,5,5)** | Strong Buy | `STOCHK_21_5_5 < 20 and STOCHK_21_5_5 > STOCHD_21_5_5 and rising_2bar(STOCHK_21_5_5, 1)` | The smoother STOCH is oversold, and `%K` is rising above `%D`. | *“Is the slower STOCH oversold and showing a sustained-looking upward turn?”* |Price looks beaten down, but it may be starting to recover.|
| **STOCH(21,5,5)** | Buy | `STOCHK_21_5_5 < 20 and (STOCHK_21_5_5 <= STOCHD_21_5_5 or not_rising_2bar(STOCHK_21_5_5, 1))` | The smoother STOCH is oversold, but the upward turn is incomplete. | *“Is the slower STOCH oversold w/o full bullish confirmation?”* |Price looks beaten down, but it may still be falling.|
| **STOCH(21,5,5)** | Neutral | `20 <= STOCHK_21_5_5 <= 80` | The smoother STOCH is between its two extreme zones. | *“Is the slower STOCH outside both extreme zones?”* |Price is somewhere in the middle.|
| **STOCH(21,5,5)** | Sell | `STOCHK_21_5_5 > 80 and (STOCHK_21_5_5 >= STOCHD_21_5_5 or not_falling_2bar(STOCHK_21_5_5, 1))` | The smoother STOCH is overbought, but the downward turn is incomplete. | *“Is the slower STOCH overbought w/o full bearish confirmation?”* |Price looks stretched, but it may still keep rising.|
| **STOCH(21,5,5)** | Strong Sell | `STOCHK_21_5_5 > 80 and STOCHK_21_5_5 < STOCHD_21_5_5 and falling_2bar(STOCHK_21_5_5, 1)` | The smoother STOCH is overbought, and `%K` is falling below `%D`. | *“Is the slower STOCH overbought and showing a sustained-looking downward turn?”* |Price looks stretched and may be starting to fall.|


---
## Understanding '`%K`' and '`%D`'

#### Difference between %K and %D

| Term | What it is                           | What it tells you                                                                                     |
| ---- | ------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| `%K` | The primary Stochastic line          | Where the close is within the recent high-low range, usually after smoothing depending on the version |
| `%D` | A moving average / smoothing of `%K` | The signal line used to judge whether %K is turning up or down                                        |

In your project’s naming:

```text
STOCHK_14_3_3 = %K
STOCHD_14_3_3 = %D
```

So for this rule:

```json
"buy": "STOCHK_14_3_3 > STOCHD_14_3_3"
```

Literal translation:

> The %K line is above the %D line.

Plain-English version:

> The current Stochastic reading is stronger than its smoothed signal line.

#### What `%K = 80` means

A `%K` value around `80` means:
> The close is near the upper end of its recent high-low range.

A `%K` value around `20` means:
> The close is near the lower end of its recent high-low range.

A `%K` value around `50` means:
> The close is near the middle of its recent range.

#### What `%D` adds

`%D` does **not** directly tell you where the latest close sits in the range. It is a smoothed version of `%K`.

So `%D` is more like:
> The recent average / signal-line version of the Stochastic reading.

That is why the rulebook compares `%K` to `%D`:

```text
%K > %D  → current Stochastic is above its smoothed signal line
%K < %D  → current Stochastic is below its smoothed signal line
```

> **%K** shows where the close sits within the recent high-low range. 
> **%D** is the smoothed signal line used to confirm whether %K is turning up or down.


---
## Notes: Stochastic Oscillator

The **Stochastic Oscillator** compares where the latest closing price sits relative to the recent high-low range.

For `Stoch(14,3,3)`:
* `14` = lookback window for the recent high-low range.
* First `3` = smoothing applied to `%K`.
* Second `3` = smoothing used to create `%D`.

In this project:

```text
STOCHK_14_3_3 = %K line
STOCHD_14_3_3 = %D line
```

**Simple interpretation (`%K` and `%D`):**
* `%K` above `%D` = short-term momentum is leaning bullish. 
* `%K` below `%D` = short-term momentum is leaning bearish.
* `%K` near the middle zone, around 50, suggests balanced / unclear momentum.
* `%K` rising or falling adds directional confirmation.


**Interpretation (Index values)**:
Compares closing price to its range over a period, scaled 0-100.
- Above 80 = overbought conditions
- Below 20 = oversold conditions
- **Buy**: %K line > 50 = bullish signal
	- %K crossing above %D = bullish signal
- **Sell**: %K line < 50 = bearish signal
	- %K crossing below %D = bearish signal
- **Neutral**: Around 50 or no clear crossover.

(See 'More about `%K` & `%D`' below for more information)

---
### 101
**Purpose:** Compare a security's closing price to its price range over a given period to identify momentum turning points (ie,  potential market reversals) and overbought/oversold levels.

**Use when:** You want to time entries and exits based on where current price sits relative to recent highs and lows.
- Use Stochastic when you want to see whether price is closing closer to the top or bottom of its recent range, and whether short-term momentum is turning up or down.

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

**Tips:**
- Divergences with price indicate potential reversals
- Look for signals when leaving extreme zones

**Optimal Conditions:** Most effective in ranging markets and during pullbacks in trends. Works well on shorter timeframes for day trading and swing trading.

**Limitations:** Prone to false signals in strong trending markets. Can stay in extreme zones longer than expected during powerful moves.

