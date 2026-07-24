## RSI: Rule-by-Rule Summary

| Source      | Signal      | Rule logic                                                                    | In one sentence                                                                                     | Answers the question / tells you                                              |
| ----------- | ----------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **RSI(14)** | Strong Buy  | `RSI_14 < 30 and falling_2bar(RSI_14)`                                        | **RSI is oversold and becoming even more oversold** across two consecutive moves.                   | **Is RSI continuing to deteriorate while already oversold?**                  |
| **RSI(14)** | Buy         | `RSI_14 < 30 and not_falling_2bar(RSI_14)`                                    | **RSI is oversold**, but it is not continuing lower for two consecutive moves.                      | **Is RSI oversold without sustained further deterioration?**                  |
| **RSI(14)** | Sell        | `(RSI_14 > 70 and RSI_14 <= 75) or (RSI_14 > 75 and not_rising_2bar(RSI_14))` | **RSI is overbought**, but it is not both above 75 and continuing higher for two consecutive moves. | **Is RSI overbought without sustained acceleration into the higher extreme?** |
| **RSI(14)** | Strong Sell | `RSI_14 > 75 and rising_2bar(RSI_14)`                                         | **RSI is highly overbought and becoming even more overbought** across two consecutive moves.        | **Is RSI continuing to strengthen while already highly overbought?**          |
| **RSI(21)** | Strong Buy  | `RSI_21 < 30 and rising_2bar(RSI_21)`                                         | **RSI remains very weak, but is starting to pick-up** (it has risen for 2 consecutive days).        | **Has RSI begun a sustained reversal while still oversold?**                  |
| **RSI(21)** | Buy         | `RSI_21 < 30 and not_rising_2bar(RSI_21)`                                     | **RSI is oversold** but lacks two consecutive recovery moves.                                       | **Is RSI oversold without sustained reversal confirmation?**                  |
| **RSI(21)** | Sell        | `RSI_21 > 70 and not_falling_2bar(RSI_21)`                                    | **RSI is overbought** but lacks two consecutive retreating moves.                                   | **Is RSI overbought without sustained reversal confirmation?**                |
| **RSI(21)** | Strong Sell | `RSI_21 > 70 and falling_2bar(RSI_21)`                                        | **RSI remains very high but is weakening** (it's fallen for 2 consecutive days).                    | **Has RSI begun a sustained reversal while still overbought?**                |
| **RSI(30)** | Strong Buy  | `RSI_30 < 30 and rising_2bar(RSI_30, 1)`                                      | **RSI remains weak. but is getting stringer** (it's risen from the immediately preceding bar).      | **Has RSI begun reversing upward while still oversold?**                      |
| **RSI(30)** | Buy         | `RSI_30 < 30 and not_rising_2bar(RSI_30, 1)`                                  | **RSI is oversold** but did not rise from the immediately preceding bar.                            | **Is RSI oversold without even a one-bar recovery?**                          |
| **RSI(30)** | Sell        | `RSI_30 > 70 and not_falling_2bar(RSI_30, 1)`                                 | **RSI is overbought** but did not decline from the immediately preceding bar.                       | **Is RSI overbought without even a one-bar retreat?**                         |
| **RSI(30)** | Strong Sell | `RSI_30 > 70 and falling_2bar(RSI_30, 1)`                                     | **RSI remains very high, but is weakening  (it's declined from the immediately preceding bar).      | **Has RSI begun reversing downward while still overbought?**                  |


## Relative Strength Index (RSI)

### What RSI measures

The Relative Strength Index compares the magnitude of recent upward and downward price movements and expresses the result on a scale from 0 to 100.

In general:

- lower RSI readings indicate that recent downward movement has been stronger;
- higher RSI readings indicate that recent upward movement has been stronger;
- readings near the middle indicate a more balanced condition.

This application calculates four RSI periods:

- RSI(10)
- RSI(14)
- RSI(21)
- RSI(30)

The calculation period affects how quickly RSI reacts, but the four rows also use different scoring philosophies. They are therefore not interchangeable versions of the same rule.

RSI(14) is the primary model in this document. RSI(10), RSI(21), and RSI(30) provide supplementary interpretations.

---

### How this application uses RSI

Each RSI row converts the current oscillator reading—and, for some rows, its recent direction—into one of five heatmap states:

| Signal | Score |
|---|---:|
| Strong Buy | +2 |
| Buy | +1 |
| Neutral | 0 |
| Sell | -1 |
| Strong Sell | -2 |

The RSI family uses a contrarian scoring perspective:

- unusually low RSI readings receive bullish scores;
- unusually high RSI readings receive bearish scores.

What differs among the four rows is what qualifies a condition as **Strong**.

---

### How the four RSI models differ

| RSI | Model | Thresholds | Directional filter | What makes the signal Strong? | Core question |
|---|---|---|---|---|---|
| **RSI(10)** | Extreme-band contrarian | `20 / 30 / 70 / 80` | None—current level only | RSI enters the outer `<20` or `>80` band | **How extreme is RSI right now?** |
| **RSI(14)** | Aggressive contrarian persistence | Buy below `30`; Sell above `70`; Strong Sell above `75` | Two consecutive moves farther into the extreme | Oversold RSI keeps falling, or highly overbought RSI keeps rising | **Is RSI continuing farther into the extreme?** |
| **RSI(21)** | Two-bar in-zone reversal confirmation | `30 / 70` | Two consecutive moves back toward neutral | RSI begins a sustained reversal while still inside the extreme zone | **Has RSI begun a sustained reversal?** |
| **RSI(30)** | One-bar in-zone reversal confirmation | `30 / 70` | One move back toward neutral | The slower RSI makes its first reversal move while still inside the extreme zone | **Has the slower RSI begun turning?** |

### Model vocabulary

Use the following names when referring to the four rule sets:

```text
RSI(10): Extreme-band contrarian model
RSI(14): Aggressive contrarian persistence model
RSI(21): Two-bar in-zone reversal-confirmation model
RSI(30): One-bar in-zone reversal-confirmation model
```

The one-bar and two-bar requirements are collectively referred to as **directional filters**.

```text
RSI(10): No directional filter—level only
RSI(14): Two-bar persistence farther into the extreme
RSI(21): Two-bar reversal back toward neutral
RSI(30): One-bar reversal back toward neutral
```

---

## RSI(14) — Aggressive Contrarian Persistence Model

**Quick Reference**:
- Question: Is RSI continuing farther into the extreme?
- Strong Buy: Below 30 and falling for two consecutive moves.
- Strong Sell: Above 75 and rising for two consecutive moves.
```text
Current RSI < 30
    Falling for two consecutive moves -> Strong Buy (+2)
    Otherwise                         -> Buy (+1)

Current RSI from 30 through 70
                                      -> Neutral (0)

Current RSI > 70
    Above 75 and rising for two
    consecutive moves                 -> Strong Sell (-2)
    Otherwise                         -> Sell (-1)
```


RSI(14) is the primary RSI reference used by this application.

The model combines:

1. the current RSI zone; and
2. whether RSI has continued moving farther into that extreme for two consecutive bar-to-bar moves.

Its central interpretation is:

> Low RSI is bullish from a contrarian perspective, high RSI is bearish, and continued movement farther into the extreme increases the strength of that contrarian score.

Under this model, **Strong does not mean that a reversal has begun**.

It means the condition is becoming more stretched.

---

### RSI(14) signal summary

| Signal               | Layman’s translation                                                                            | Literal trigger                                                                                                            | Rule logic                                                                    |
| -------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Strong Buy (+2)**  | RSI is oversold and becoming even more oversold across two consecutive moves.                   | Current RSI is below 30, and RSI declined from two bars ago to one bar ago and again from one bar ago to the current bar.  | `RSI_14 < 30 and falling_2bar(RSI_14)`                                        |
| **Buy (+1)**         | RSI is oversold, but it is not continuing lower for two consecutive moves.                      | Current RSI is below 30, and the strict two-move falling pattern is absent.                                                | `RSI_14 < 30 and not_falling_2bar(RSI_14)`                                    |
| **Neutral (0)**      | RSI is in its middle range and is neither overbought nor oversold under this model.             | Current RSI is from 30 through 70, inclusive.                                                                              | `30 <= RSI_14 <= 70`                                                          |
| **Sell (-1)**        | RSI is overbought, but it is not both above 75 and continuing higher for two consecutive moves. | Current RSI is above 70, except when it is also above 75 and has risen for two consecutive moves.                          | `(RSI_14 > 70 and RSI_14 <= 75) or (RSI_14 > 75 and not_rising_2bar(RSI_14))` |
| **Strong Sell (-2)** | RSI is highly overbought and becoming even more overbought across two consecutive moves.        | Current RSI is above 75, and RSI increased from two bars ago to one bar ago and again from one bar ago to the current bar. | `RSI_14 > 75 and rising_2bar(RSI_14)`                                         |

---

### How the RSI(14) model works

The model asks two questions.

#### 1. Where is RSI now?

```text
RSI below 30       -> bullish contrarian zone
RSI from 30 to 70  -> Neutral
RSI above 70       -> bearish contrarian zone
```

#### 2. Is RSI continuing farther into the extreme?

```text
Below 30 and falling twice -> Strong Buy
Above 75 and rising twice  -> Strong Sell
```

The directional filter is evaluated using the current RSI value and the preceding two values.

---

### Strong Buy (+2)

#### Rule

```text
RSI_14 < 30 and falling_2bar(RSI_14)
```

#### In one sentence

> RSI is oversold and becoming even more oversold across two consecutive moves.

#### Answers the question

> **Is RSI continuing to deteriorate while already oversold?**

#### Example

```text
7/1: 34
7/2: 29
7/3: 24
```

The current RSI is below 30:

```text
24 < 30 -> True
```

RSI also fell during both consecutive moves:

```text
34 to 29 -> decline
29 to 24 -> decline
```

Result:

```text
Strong Buy (+2)
```

The score reflects increasing contrarian stretch. It does not indicate that RSI has stabilized or that price has begun recovering.

---

### Buy (+1)

#### Rule

```text
RSI_14 < 30 and not_falling_2bar(RSI_14)
```

#### In one sentence

> RSI is oversold, but it is not continuing lower for two consecutive moves.

#### Answers the question

> **Is RSI oversold without sustained further deterioration?**

#### Example: RSI is recovering

```text
7/1: 24
7/2: 26
7/3: 28
```

The current RSI is below 30, but the sequence is rising rather than falling.

Result:

```text
Buy (+1)
```

#### Example: only the latest move declined

```text
7/1: 25
7/2: 28
7/3: 27
```

The latest move declined:

```text
28 to 27 -> decline
```

But the preceding move increased:

```text
25 to 28 -> increase
```

Therefore, RSI did not decline for two consecutive moves.

Result:

```text
Buy (+1)
```

---

### Neutral (0)

#### Rule

```text
30 <= RSI_14 <= 70
```

#### In one sentence

> RSI is within the model’s middle range.

#### Answers the question

> **Is RSI currently outside either contrarian extreme zone?**

#### Example

```text
7/1: 46
7/2: 52
7/3: 57
```

The current value satisfies:

```text
30 <= 57 <= 70
```

Result:

```text
Neutral (0)
```

Exact boundary values remain Neutral:

```text
RSI = 30 -> Neutral
RSI = 70 -> Neutral
```

The prior direction does not matter while the current RSI remains inside this range.

---

### Sell (-1)

#### Rule

```text
(RSI_14 > 70 and RSI_14 <= 75)
or
(RSI_14 > 75 and not_rising_2bar(RSI_14))
```

#### In one sentence

> RSI is overbought, but it lacks the full combination of a reading above 75 and two consecutive increases.

#### Answers the question

> **Is RSI overbought without sustained acceleration into the higher extreme?**

The Sell rule covers two situations.

#### Situation 1: RSI is above 70 but no higher than 75

```text
7/1: 71
7/2: 73
7/3: 74
```

The current RSI is overbought:

```text
74 > 70
```

But it has not crossed the Strong Sell threshold:

```text
74 <= 75
```

Result:

```text
Sell (-1)
```

#### Situation 2: RSI is above 75 but lacks two consecutive rises

```text
7/1: 78
7/2: 76
7/3: 77
```

The current RSI is above 75:

```text
77 > 75
```

But the sequence did not rise twice:

```text
78 to 76 -> decline
76 to 77 -> increase
```

Result:

```text
Sell (-1)
```

Exact threshold behavior:

```text
RSI = 75 -> Sell
```

Strong Sell requires RSI to be strictly greater than 75.

---

### Strong Sell (-2)

#### Rule

```text
RSI_14 > 75 and rising_2bar(RSI_14)
```

#### In one sentence

> RSI is highly overbought and becoming even more overbought across two consecutive moves.

#### Answers the question

> **Is RSI continuing to strengthen while already highly overbought?**

#### Example

```text
7/1: 71
7/2: 74
7/3: 78
```

The current RSI is above 75:

```text
78 > 75 -> True
```

RSI also rose during both consecutive moves:

```text
71 to 74 -> increase
74 to 78 -> increase
```

Result:

```text
Strong Sell (-2)
```

The stronger bearish score reflects increasing upside stretch. It does not require RSI to turn downward first.

---

### What “Strong” means for RSI(14)

For RSI(14), Strong means:

```text
The oscillator remains extreme
+
the oscillator has continued moving farther into that extreme
```

It does not mean:

```text
a reversal has started
a threshold has been exited
price has confirmed a reversal
```

This is why RSI(14) is described as an **aggressive contrarian persistence model**.

The model assigns greater contrarian conviction while momentum is still worsening:

```text
Oversold and still falling -> Strong Buy
Highly overbought and still rising -> Strong Sell
```

---

### Persistence versus reversal

RSI(14) looks for persistence **into** the extreme.

#### Persistence into oversold territory

```text
7/1: 34
7/2: 29
7/3: 24
```

RSI is becoming progressively lower.

Under RSI(14):

```text
Strong Buy
```

A reversal-confirmation model would look for movement in the opposite direction.

#### Recovery while still oversold

```text
7/1: 24
7/2: 26
7/3: 28
```

RSI remains below 30 but is moving back toward neutral.

Under RSI(14):

```text
Buy
```

Under RSI(21), the same type of sequence can qualify as Strong Buy because RSI(21) rewards reversal evidence rather than continued deterioration.

---

## Supplementary RSI Settings

### RSI(10) — Extreme-Band Contrarian Model

RSI(10) is the fastest and most responsive RSI row.

It uses a level-only model. Recent RSI direction does not affect the classification.

Its purpose is to answer:

> **How extreme is the current short-term RSI reading?**

#### RSI(10) signal summary

| Signal               | Layman’s translation                                                     | Literal trigger                                         | Rule logic           |
| -------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------- | -------------------- |
| **Strong Buy (+2)**  | RSI is extremely low, producing the strongest contrarian bullish score.  | Current RSI is below 20.                                | `RSI_10 < 20`        |
| **Buy (+1)**         | RSI is within the ordinary oversold band.                                | Current RSI is from 20 through 30, inclusive.           | `20 <= RSI_10 <= 30` |
| **Neutral (0)**      | RSI is within its middle range.                                          | Current RSI is strictly above 30 and strictly below 70. | `30 < RSI_10 < 70`   |
| **Sell (-1)**        | RSI is within the ordinary overbought band.                              | Current RSI is from 70 through 80, inclusive.           | `70 <= RSI_10 <= 80` |
| **Strong Sell (-2)** | RSI is extremely high, producing the strongest contrarian bearish score. | Current RSI is above 80.                                | `RSI_10 > 80`        |

#### Example: Strong Buy

```text
7/1: 24
7/2: 18
```

Only the current value matters:

```text
18 < 20
```

Result:

```text
Strong Buy (+2)
```

#### Example: Strong Sell

```text
7/1: 76
7/2: 83
```

Only the current value matters:

```text
83 > 80
```

Result:

```text
Strong Sell (-2)
```

---

### RSI(21) — Two-Bar In-Zone Reversal-Confirmation Model

RSI(21) is slower than RSI(14) and uses a more selective interpretation.

A Strong signal requires RSI to remain inside the oversold or overbought zone while moving back toward neutral for two consecutive moves.

Its purpose is to answer:

> **Has RSI begun a sustained reversal while still extreme?**

#### RSI(21) signal summary

| Signal               | Layman’s translation                                             | Literal trigger                                                                 | Rule logic                                 |
| -------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------ |
| **Strong Buy (+2)**  | RSI remains oversold but has risen for two consecutive moves.    | Current RSI is below 30, and RSI increased during both recent bar-to-bar moves. | `RSI_21 < 30 and rising_2bar(RSI_21)`      |
| **Buy (+1)**         | RSI is oversold but lacks two consecutive recovery moves.        | Current RSI is below 30, and the strict two-move rising pattern is absent.      | `RSI_21 < 30 and not_rising_2bar(RSI_21)`  |
| **Neutral (0)**      | RSI is within its middle range.                                  | Current RSI is from 30 through 70, inclusive.                                   | `30 <= RSI_21 <= 70`                       |
| **Sell (-1)**        | RSI is overbought but lacks two consecutive retreating moves.    | Current RSI is above 70, and the strict two-move falling pattern is absent.     | `RSI_21 > 70 and not_falling_2bar(RSI_21)` |
| **Strong Sell (-2)** | RSI remains overbought but has fallen for two consecutive moves. | Current RSI is above 70, and RSI declined during both recent bar-to-bar moves.  | `RSI_21 > 70 and falling_2bar(RSI_21)`     |

#### Strong Buy example

```text
7/1: 24
7/2: 26
7/3: 28
```

RSI remains below 30 and rose twice:

```text
24 to 26 -> increase
26 to 28 -> increase
```

Result:

```text
Strong Buy (+2)
```

#### Strong Sell example

```text
7/1: 76
7/2: 74
7/3: 72
```

RSI remains above 70 and fell twice:

```text
76 to 74 -> decline
74 to 72 -> decline
```

Result:

```text
Strong Sell (-2)
```

The RSI must remain inside the applicable extreme zone. Once it returns to the 30–70 range, it becomes Neutral.

---

### RSI(30) — One-Bar In-Zone Reversal-Confirmation Model

RSI(30) is the slowest RSI row.

Because the oscillator itself is smoother, its Strong states require only one move back toward neutral rather than two consecutive moves.

Its purpose is to answer:

> **Has the slower RSI made its first move back toward neutral while still extreme?**

#### RSI(30) signal summary

| Signal               | Layman’s translation                                                        | Literal trigger                                                       | Rule logic                                    |
| -------------------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------- |
| **Strong Buy (+2)**  | RSI remains oversold but has risen from the immediately preceding bar.      | Current RSI is below 30 and higher than the prior RSI value.          | `RSI_30 < 30 and rising_2bar(RSI_30, 1)`      |
| **Buy (+1)**         | RSI is oversold but did not rise from the preceding bar.                    | Current RSI is below 30, and the one-bar rising condition is absent.  | `RSI_30 < 30 and not_rising_2bar(RSI_30, 1)`  |
| **Neutral (0)**      | RSI is within its middle range.                                             | Current RSI is from 30 through 70, inclusive.                         | `30 <= RSI_30 <= 70`                          |
| **Sell (-1)**        | RSI is overbought but did not decline from the preceding bar.               | Current RSI is above 70, and the one-bar falling condition is absent. | `RSI_30 > 70 and not_falling_2bar(RSI_30, 1)` |
| **Strong Sell (-2)** | RSI remains overbought but has declined from the immediately preceding bar. | Current RSI is above 70 and lower than the prior RSI value.           | `RSI_30 > 70 and falling_2bar(RSI_30, 1)`     |

#### Strong Buy example

```text
7/1: 27
7/2: 29
```

RSI remains below 30 and rose from the prior bar.

Result:

```text
Strong Buy (+2)
```

#### Strong Sell example

```text
7/1: 74
7/2: 72
```

RSI remains above 70 and declined from the prior bar.

Result:

```text
Strong Sell (-2)
```

The key distinction from RSI(21) is the confirmation horizon:

```text
RSI(21): two consecutive reversal moves
RSI(30): one reversal move
```

---

## The Question Each Model Answers

| RSI         | Strong-signal question                                                         |
| ----------- | ------------------------------------------------------------------------------ |
| **RSI(10)** | **How extreme is RSI right now?**                                              |
| **RSI(14)** | **Is RSI continuing farther into the extreme?**                                |
| **RSI(21)** | **Has RSI begun a sustained two-move reversal while still extreme?**           |
| **RSI(30)** | **Has the slower RSI begun reversing from the prior bar while still extreme?** |

### RSI(14): persistence into the extreme

```text
7/1: 34
7/2: 29
7/3: 24
```

Interpretation:

```text
RSI is moving farther into oversold territory.
```

### RSI(21): sustained in-zone reversal

```text
7/1: 24
7/2: 26
7/3: 28
```

Interpretation:

```text
RSI remains oversold but has reversed upward for two consecutive moves.
```

### RSI(30): first in-zone reversal move

```text
7/1: 27
7/2: 29
```

Interpretation:

```text
The slower RSI remains oversold but has made its first upward move.
```

---


## Understanding the Directional Filters

### Filter reference

| Filter                 | RSI observations used | Requirement                                 |
| ---------------------- | :-------------------: | ------------------------------------------- |
| `rising_2bar(RSI)`     |           3           | Two consecutive strict increases            |
| `falling_2bar(RSI)`    |           3           | Two consecutive strict decreases            |
| `rising_2bar(RSI, 1)`  |           2           | Current RSI is strictly above the prior RSI |
| `falling_2bar(RSI, 1)` |           2           | Current RSI is strictly below the prior RSI |

### Two-bar rising filter

```text
7/1: 22
7/2: 24
7/3: 27
```

Both moves increased:

```text
22 to 24
24 to 27
```

Therefore:

```text
rising_2bar(RSI) = True
```

### Two-bar falling filter

```text
7/1: 34
7/2: 29
7/3: 24
```

Both moves declined:

```text
34 to 29
29 to 24
```

Therefore:

```text
falling_2bar(RSI) = True
```

### One-bar rising filter

```text
7/1: 27
7/2: 29
```

The current RSI is above the prior RSI:

```text
29 > 27
```

Therefore:

```text
rising_2bar(RSI, 1) = True
```

### One-bar falling filter

```text
7/1: 74
7/2: 72
```

The current RSI is below the prior RSI:

```text
72 < 74
```

Therefore:

```text
falling_2bar(RSI, 1) = True
```

### Equality does not count

The comparisons are strict.

```text
7/1: 23
7/2: 23
7/3: 24
```

This is not a two-bar rise because the first move was unchanged.

Likewise:

```text
7/1: 24
7/2: 24
7/3: 23
```

This is not a two-bar decline because the first move was unchanged.

---

## In-Zone Reversal versus Threshold Exit

RSI(21) and RSI(30) use **in-zone reversal confirmation**.

The current RSI must remain inside the oversold or overbought zone.

### In-zone bullish reversal

```text
7/1: 24
7/2: 26
7/3: 28
```

The current RSI remains below 30.

### Threshold exit

```text
7/1: 27
7/2: 29
7/3: 32
```

The current RSI has crossed above 30 and returned to the Neutral range.

Under the current persistent-state rules:

```text
Current RSI from 30 through 70 -> Neutral
```

The model does not create a separate signal for the threshold-crossing event itself.

---

## Important Limitations

### RSI is not a standalone prediction

An extreme RSI condition does not guarantee an immediate reversal. RSI can remain unusually low or high while a strong price trend continues.

### Strong has different meanings across the family

```text
RSI(10): Strong means a more extreme current level.
RSI(14): Strong means continued movement farther into the extreme.
RSI(21): Strong means two-move reversal evidence while still extreme.
RSI(30): Strong means one-move reversal evidence while still extreme.
```

A Strong Buy from one RSI row therefore does not necessarily represent the same market behavior as a Strong Buy from another.

### Directional filters describe RSI—not price directly

A rising RSI means the oscillator increased. A falling RSI means the oscillator decreased. Neither condition alone guarantees that price will move in the corresponding direction afterward.

### RSI(14) is intentionally aggressive

RSI(14) assigns its strongest contrarian score while the extreme is still worsening. It may therefore identify a stretched condition before any stabilization is visible.

### RSI(21) is intentionally selective

RSI(21) requires two consecutive reversal moves while RSI remains inside the extreme zone. Strong signals may therefore be relatively rare.

---

## Quick Reference

```text
RSI(10)
Question: How extreme is RSI now?
Strong: Current RSI enters the outer <20 or >80 band.

RSI(14)
Question: Is RSI continuing farther into the extreme?
Strong Buy: Below 30 and falling for two consecutive moves.
Strong Sell: Above 75 and rising for two consecutive moves.

RSI(21)
Question: Has RSI begun a sustained reversal while still extreme?
Strong Buy: Below 30 and rising for two consecutive moves.
Strong Sell: Above 70 and falling for two consecutive moves.

RSI(30)
Question: Has the slower RSI begun turning while still extreme?
Strong Buy: Below 30 and higher than the prior bar.
Strong Sell: Above 70 and lower than the prior bar.
```





## Other 'Signal Summaries'


### RSI(21) — Signal Summary


| Signal               | Layman’s translation                                                                                   | Literal trigger                                                                                                            | Rule logic                                 |
| -------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| **Strong Buy (+2)**  | RSI is oversold but has started recovering for two consecutive moves while still remaining below 30.   | Current RSI is below 30, and RSI increased from two bars ago to one bar ago and again from one bar ago to the current bar. | `RSI_21 < 30 and rising_2bar(RSI_21)`      |
| **Buy (+1)**         | RSI is oversold, but it has not risen for both of the last two consecutive moves.                      | Current RSI is below 30, and the strict two-move rising pattern is absent.                                                 | `RSI_21 < 30 and not_rising_2bar(RSI_21)`  |
| **Neutral (0)**      | RSI is within its middle range and is neither oversold nor overbought under this model.                | Current RSI is from 30 through 70, inclusive.                                                                              | `30 <= RSI_21 <= 70`                       |
| **Sell (-1)**        | RSI is overbought, but it has not declined for both of the last two consecutive moves.                 | Current RSI is above 70, and the strict two-move falling pattern is absent.                                                | `RSI_21 > 70 and not_falling_2bar(RSI_21)` |
| **Strong Sell (-2)** | RSI is overbought but has started retreating for two consecutive moves while still remaining above 70. | Current RSI is above 70, and RSI declined from two bars ago to one bar ago and again from one bar ago to the current bar.  | `RSI_21 > 70 and falling_2bar(RSI_21)`     |

---

### RSI(30) — Signal Summary
Model: 1-Bar Contrarian Reversal-confirmation
Thresholds: 30/70

| Signal               | Layman’s translation                                                                                  | Literal trigger                                                       | Rule logic                                    |
| -------------------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------- |
| **Strong Buy (+2)**  | RSI is oversold and has risen from the immediately preceding bar while still remaining below 30.      | Current RSI is below 30 and is higher than the previous bar’s RSI.    | `RSI_30 < 30 and rising_2bar(RSI_30, 1)`      |
| **Buy (+1)**         | RSI is oversold, but it did not rise from the immediately preceding bar.                              | Current RSI is below 30, and the one-bar rising condition is absent.  | `RSI_30 < 30 and not_rising_2bar(RSI_30, 1)`  |
| **Neutral (0)**      | RSI is within its middle range and is neither oversold nor overbought under this model.               | Current RSI is from 30 through 70, inclusive.                         | `30 <= RSI_30 <= 70`                          |
| **Sell (-1)**        | RSI is overbought, but it did not decline from the immediately preceding bar.                         | Current RSI is above 70, and the one-bar falling condition is absent. | `RSI_30 > 70 and not_falling_2bar(RSI_30, 1)` |
| **Strong Sell (-2)** | RSI is overbought and has declined from the immediately preceding bar while still remaining above 70. | Current RSI is above 70 and is lower than the previous bar’s RSI.     | `RSI_30 > 70 and falling_2bar(RSI_30, 1)`     |

---

### RSI(10) — Signal Summary

Model: Contrarian Extreme-band
Thresholds: 20/80

| Signal               | Layman’s translation                                                            | Literal trigger                                                 | Rule logic           |
| -------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------- | -------------------- |
| **Strong Buy (+2)**  | RSI is extremely low, producing the strongest contrarian bullish score.         | Current RSI is below 20. Recent RSI direction doe s not matter. | `RSI_10 < 20`        |
| **Buy (+1)**         | RSI is low and within the ordinary oversold band.                               | Current RSI is from 20 through 30, inclusive.                   | `20 <= RSI_10 <= 30` |
| **Neutral (0)**      | RSI is within its middle range and is not classified as overbought or oversold. | Current RSI is strictly above 30 and strictly below 70.         | `30 < RSI_10 < 70`   |
| **Sell (-1)**        | RSI is high and within the ordinary overbought band.                            | Current RSI is from 70 through 80, inclusive.                   | `70 <= RSI_10 <= 80` |
| **Strong Sell (-2)** | RSI is extremely high, producing the strongest contrarian bearish score.        | Current RSI is above 80. Recent RSI direction does not matter.  | `RSI_10 > 80`        |




### RSI rule interpretation table

| Source      | Signal      | Rule logic                                                                    | In one sentence                                                                                 | Answers the question / tells you                                                |
| ----------- | ----------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **RSI(14)** | Strong Buy  | `RSI_14 < 30 and falling_2bar(RSI_14)`                                        | RSI is oversold and becoming even more oversold across 2 consecutive moves.                   | **“Is RSI continuing to deteriorate while already oversold?”**                  |
| **RSI(14)** | Buy         | `RSI_14 < 30 and not_falling_2bar(RSI_14)`                                    | RSI is oversold, but it is not continuing lower for 2 consecutive moves.                      | **“Is RSI oversold without sustained further deterioration?”**                  |
| **RSI(14)** | Sell        | `(RSI_14 > 70 and RSI_14 <= 75) or (RSI_14 > 75 and not_rising_2bar(RSI_14))` | RSI is overbought, but it is not both above 75 and continuing higher for 2 consecutive moves. | **“Is RSI overbought without sustained acceleration into the higher extreme?”** |
| **RSI(14)** | Strong Sell | `RSI_14 > 75 and rising_2bar(RSI_14)`                                         | RSI is highly overbought and becoming even more overbought across 2 consecutive moves.        | **“Is RSI continuing to strengthen while already highly overbought?”**          |
| **RSI(21)** | Strong Buy  | `RSI_21 < 30 and rising_2bar(RSI_21)`                                         | RSI remains oversold but has risen for 2 consecutive moves.                                   | **“Has RSI begun a sustained reversal while still oversold?”**                  |
| **RSI(21)** | Buy         | `RSI_21 < 30 and not_rising_2bar(RSI_21)`                                     | RSI is oversold but has not yet produced 2 consecutive recovery moves.                        | **“Is RSI oversold without sustained reversal confirmation?”**                  |
| **RSI(21)** | Sell        | `RSI_21 > 70 and not_falling_2bar(RSI_21)`                                    | RSI is overbought but has not yet declined for 2 consecutive moves.                           | **“Is RSI overbought without sustained reversal confirmation?”**                |
| **RSI(21)** | Strong Sell | `RSI_21 > 70 and falling_2bar(RSI_21)`                                        | RSI remains overbought but has fallen for 2 consecutive moves.                                | **“Has RSI begun a sustained reversal while still overbought?”**                |
| **RSI(30)** | Strong Buy  | `RSI_30 < 30 and rising_2bar(RSI_30, 1)`                                      | RSI remains oversold but has risen from the immediately preceding (1) bar.                          | **“Has RSI begun reversing upward while still oversold?”**                      |
| **RSI(30)** | Buy         | `RSI_30 < 30 and not_rising_2bar(RSI_30, 1)`                                  | RSI is oversold but has not risen from the immediately preceding (1) bar.                           | **“Is RSI oversold without even a one-bar recovery?”**                          |
| **RSI(30)** | Sell        | `RSI_30 > 70 and not_falling_2bar(RSI_30, 1)`                                 | RSI is overbought but has not declined from the immediately preceding (1) bar.                      | **“Is RSI overbought without even a one-bar retreat?”**                         |
| **RSI(30)** | Strong Sell | `RSI_30 > 70 and falling_2bar(RSI_30, 1)`                                     | RSI remains overbought but has declined from the immediately preceding (1) bar.                     | **“Has RSI begun reversing downward while still overbought?”**                  |

### The parallel questions by model

> For `"Strong Buy/Sell"` states:

| RSI setting | Core question                                                        |
| ----------- | -------------------------------------------------------------------- |
| **RSI(14)** | **Is RSI continuing farther into the extreme?**                      |
| **RSI(21)** | **Has RSI begun a sustained two-move reversal while still extreme?** |
| **RSI(30)** | **Has RSI begun a one-move reversal while still extreme?**           |

And for the ordinary `"Buy/Sell"` states:

| RSI setting | Ordinary-state question                                              |
| ----------- | -------------------------------------------------------------------- |
| **RSI(14)** | Is RSI extreme without sustained movement farther into that extreme? |
| **RSI(21)** | Is RSI extreme without two-move reversal confirmation?               |
| **RSI(30)** | Is RSI extreme without one-bar reversal confirmation?                |




---
## My Custom overview
**Purpose:** Measure the speed and magnitude of price changes to identify overbought and oversold conditions on a 0-100 scale.

**Use when:** You want to identify potential reversal points or confirm trend strength by analyzing momentum exhaustion. 
- **Ranging or sideways markets**, where it ${\fcolorbox{none}{lightgreen}{\textsf{excels at identifying potential reversals}}}$.

**Key Concept:** Compares average gains to average losses over a set period (typically 14). 
- High readings suggest buying pressure may be exhausted; 
- Low readings suggest selling pressure may be exhausted.

**Calculation:** $\large{\mathsf{RSI = 100 - [100 \div{(1 + RS)}]}}$, where **RS = Average Gain ÷ Average Loss** over 14 periods.

**Signals & Interpretation:**
- Above 70 = overbought (potential selling opportunity)
- Below 30 = oversold (potential buying opportunity)
- Above 80 = extremely overbought
- Below 20 = extremely oversold
- Divergences between RSI and price signal potential reversals
- 50 level acts as bullish/bearish bias divider

- **Buy**: RSI > 50 (indicates bullish momentum).
- **Sell**: RSI < 50 (indicates bearish momentum).

---

| Signal  | RSI                  | Action                            |
| ------- | -------------------- | --------------------------------- |
| Bullish | Above 50, Rising     | Suggests potential for an uptrend |
| Bearish | Below 50, Falling    | Confirms a downtrend signal       |
| Either  | Above 70 or Below 30 | Signals possible reversals        |


---

**Optimal Conditions:** Most effective in ranging or mildly trending markets. Works well on all timeframes, particularly daily and weekly for swing trading.

**Limitations:** 
Can remain overbought/oversold for extended periods in strong trends. May produce false signals during trending markets when momentum stays elevated.
- Can be unreliable in strongly trending markets, as it may stay in overbought or oversold territory for extended period


#### What it is
RSI is a momentum oscillator that compares recent gains and losses on a bounded 0–100 scale.

#### Why traders use it
It helps identify momentum extremes, shifts in buying/selling pressure, and possible exhaustion zones.

#### Common interpretations
Higher RSI values indicate stronger recent gains.
Lower RSI values indicate stronger recent losses.

#### Limitations
RSI can remain elevated or depressed for extended periods during strong trends, so it should not be used mechanically in isolation.

#### Use with
RSI is commonly paired with a trend filter such as EMA or ADX to distinguish mean-reversion setups from strong-trend continuation.

#### Common mistakes
Assuming that elevated RSI automatically means price must reverse immediately.