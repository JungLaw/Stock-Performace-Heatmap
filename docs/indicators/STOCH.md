
## Summary: STOCH(14,3,3) 'Signals'

| Signal | Literal trigger | Layman’s Translation | Rule Logic | Bottom-line|
| --- | --- | --- | --- |--- |
| [strong buy](#strong-buy) | :blue-background[%K < 20], :blue-background[%K > %D], and :blue-background[%K rose from the prior bar] | STOCH is oversold, and [%K](#understanding-k-and-d) has turned upward strongly enough to move above [%D](#understanding-k-and-d). | The oscillator is in the oversold zone, :blue-background[%K] is above its smoothed signal line, and :blue-background[%K] is rising versus the immediately preceding period. |Price looks beaten down, but may be starting to rise.|
| [buy](#buy) | :blue-background[%K < 20] and the full Strong Buy confirmation is absent | STOCH is oversold, but the upward reversal is not fully confirmed. | The oscillator is in the oversold zone, but :blue-background[%K] is either not above :blue-background[%D] or is not rising from the prior bar. |Trading at the low end of its 14-day range.|
| [neutral](#neutral) | :blue-background[20 <= %K <= 80] | STOCH is between its usual oversold and overbought zones. | :blue-background[%K] is inside the middle range, including the exact boundary values of '20' and '80'. | Price is somewhere in the middle of its 14-day range|
| [sell](#sell) | :blue-background[%K > 80] and the full Strong Sell confirmation is absent | STOCH is overbought, but the downward reversal is not fully confirmed. | The oscillator is in the overbought zone, but :blue-background[%K] is either not below [%D](#understanding-k-and-d) or is not falling from the prior bar. |Trading at the high-end of its 14-day range.|
| [strong sell](#strong-sell) | :blue-background[%K > 80], :blue-background[%K < %D], and :blue-background[%K fell from the prior bar] | STOCH is overbought, and :blue-background[%K] has turned downward strongly enough to move below :blue-background[%D]. | The oscillator is in the overbought zone, [%K](#understanding-k-and-d) is below its smoothed signal line, and :blue-background[%K] is falling versus the immediately preceding period. |Looks stretched. Trading at the high-end of its 14-day range; showing signs of fatigue.|

> :small[For more details see: ['Rule Interpretation Tables'](#stoch-14-3-3-rules-interpretation)]

---

### Key Combinations: Signal + Customizations
Priority here means potential information value and relevance to the contrarian decision—not measured profitability or statistical predictive strength.
- The first four are the clearest "**reinforcement**" combinations.
- The remaining four are important conflicts or cautions, which may be just as useful to monitor but for a different reason.

> See [Reading 'Signal' + 'Divergence' + 'Crossover' Together](#reading-signal-divergence-crossover-together) for all 'Buy', 'Sell', 'Neutral' combinations

| Priority/Scope                    | Combination                                                                                                                                                                                                                                                    |                                                                                           Example                                                                                            | Why it deserves attention                                                                                              | What to examine next                                              |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| 1 :small[( Reinforcement)]        | ${\fcolorbox{none}{darkgreen}{\textcolor{white}{\textsf{Strong Buy}}}}$ + $\large{\textcolor{blue}{\textsf{bullish}}}$ + ▲                                                                                                                                  |                                                                ${\fcolorbox{none}{Green}{\textcolor{blue}{\textsf{12.1}}~▲}}$                                                                | Oversold reversal qualifications, structural bullish disagreement and fresh upward crossover reinforce one another     | Whether price begins stabilizing or reclaiming nearby levels      |
| 1:small[( Reinforcement)]         | ${\fcolorbox{none}{Maroon}{\textcolor{white}{\textsf{Strong Sell}}}}$ + $\large{\textcolor{Red}{\textsf{bearish}}}$ + ▼                                                                                                                                      |                                                                ${\fcolorbox{none}{Brown}{\textcolor{red}{\textsf{81.0}}~▼}}$                                                                 | Overbought reversal qualifications, structural bearish disagreement and fresh downward crossover reinforce one another | Whether price begins rejecting recent highs                       |
| 1:small[( Reinforcement)]         | ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{Neutral}}}}$ + $\large{\textcolor{blue}{\textsf{bullish}}}$ + ▲                                                                                                                                     |                                                              ${\fcolorbox{none}{gainsboro}{\textcolor{blue}{\textsf{50.0}}~▲}}$                                                              | A potentially important bullish development exists despite the absence of an oversold Signal                           | Whether bullish K/D momentum persists and price responds          |
| 1:small[( Reinforcement)]         | ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{Neutral}}}}$ + $\large{\textcolor{Red}{\textsf{bearish}}}$ + ▼                                                                                                                                       |                                                              ${\fcolorbox{none}{gainsboro}{\textcolor{red}{\textsf{50.0}}~▼}}$                                                               | A potentially important bearish development exists despite the absence of an overbought Signal                         | Whether bearish K/D momentum persists and price responds          |
| 2:small[( Caution: Disagreement)] | ${\fcolorbox{none}{lightgreen}{\textcolor{black}{\textsf{Buy}}}}$ + $\large{\textcolor{blue}{\textsf{bullish}}}$ + $\large{\textcolor{orange}{\textsf{▼}}}$                                                                                                  |                                              ${\fcolorbox{none}{greenyellow}{\textcolor{blue}{\textsf{12.1}}~\textcolor{orange}{\textsf{▼}}}}$                                               | Bullish structural disagreement conflicts with a fresh bearish oscillator transition                                   | Whether immediate deterioration continues or reverses             |
| 2:small[( Caution: Disagreement)] | ${\fcolorbox{none}{Salmon}{\textsf{Sell}}}$ + $\large{\textcolor{Red}{\textsf{bearish}}}$ + $\large{\textcolor{orange}{\textsf{▲}}}$                                                                                                                          |                                                 ${\fcolorbox{none}{Salmon}{\textcolor{red}{\textsf{81.0}}~\textcolor{orange}{\textsf{▲}}}}$                                                  | Bearish structural disagreement conflicts with a fresh bullish oscillator transition                                   | Whether upward momentum continues despite price/%K disagreement   |
| 2:small[( Caution: Disagreement)] | ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{Neutral}}}}$ + $\large{\textcolor{blue}{\textsf{bullish}}}$ + ▼ <br> ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{Neutral}}}}$ + $\large{\textcolor{Red}{\textsf{bearish}}}$ + ▲ </br> |                      ${\fcolorbox{none}{gainsboro}{\textcolor{blue}{\textsf{50.0}}~▼}}$ <br>${\fcolorbox{none}{gainsboro}{\textcolor{red}{\textsf{50.0}}~▲}}$</br>                      | Divergence and fresh crossover indicate opposite developments                                                          | Which observation is gaining support from subsequent price action |
| 2:small[( Caution: Disagreement)] | ${\fcolorbox{none}{lightgreen}{\textcolor{black}{\textsf{Buy}}}}$ + $\large{\textcolor{orange}{\textsf{▼}}}$ or ${\fcolorbox{none}{Salmon}{\textsf{Sell}}}$ + $\large{\textcolor{orange}{\textsf{▲}}}$                                                           | ${\fcolorbox{none}{lightgreen}{\textcolor{black}{\textsf{12.1}}~\textcolor{orange}{\textsf{▼}}}}$<br>${\fcolorbox{none}{Salmon}{\textcolor{black}{\textsf{81.0}}~\textcolor{orange}{\textsf{▲}}}}$ | Fresh momentum opposes the usual contrarian expectation at an extreme                                                  | Whether the extreme persists rather than resolves                 |


---
## STOCH(14,3,3) — brief overview
:small[[Back to top](#summary-stoch-14-3-3-signals)]

For **STOCH(14,3,3)**:

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

Both are normally bounded between :gray-background[0] and :gray-background[100].

A simplified conceptual formula is:

```text
%K = 100 × (current close − lowest low)
           ÷ (highest high − lowest low)
```

The exact implementation also applies the configured smoothing periods.

Simple interpretation:

* A high [%K](#understanding-k-and-d) means price is closing near the upper end of its recent range.
* A low :blue-background[%K] means price is closing near the lower end of its recent range.
* :blue-background[%K < 20] is treated as oversold.
* :blue-background[%K > 80] is treated as overbought.
* :blue-background[%K > %D] means the faster oscillator line is above its smoothed signal line.
* [%K < %D](#understanding-k-and-d) means the faster oscillator line is below its smoothed signal line.
* A rising :blue-background[%K] suggests short-term momentum within the range is improving.
* A falling :blue-background[%K] suggests short-term momentum within the range is weakening.

> :small[[For more details, see: 'Understanding %K and %D'](#understanding-k-and-d)]

An oversold or overbought reading is not, by itself, proof that price will reverse. A security can remain near an extreme while a strong trend continues.

The project therefore distinguishes between:
```text
Buy / Sell
= an extreme-zone condition without full reversal confirmation

Strong Buy / Strong Sell
= an extreme-zone condition plus %K/%D positioning
  and one-bar %K direction confirmation
```

### Value-added use

> Use STOCH(14,3,3) when you want a balanced momentum oscillator that identifies when price is near the upper or lower end of its recent range and distinguishes an unconfirmed extreme from a developing reversal.

This middle setting is intended to balance responsiveness and noise. It is generally less reactive than **STOCH(5,3,3)** and faster than the more heavily smoothed **STOCH(21,5,5)**.

### Use with

STOCH is most useful when interpreted with trend, momentum, and participation context.

* **EMA or SMA** — to determine whether an oversold or overbought condition is occurring with or against the prevailing trend.
* **ADX** — to distinguish a strong trend, where an extreme may persist, from a weaker environment where reversal signals may be more actionable.
* **MACD or ROC** — to check whether broader momentum supports the :blue-background[%K/%D] turn.
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

The rules do not require a literal crossover to occur on the current bar. The hover field :blue-background[Cross] reports whether an actual bullish or bearish [%K/%D crossover](#crossovers) occurred that day, but crossover status is display context rather than a scoring requirement.

---
## Understanding the Stochastic Metrics
:small[[Back to top](#summary-stoch-14-3-3-signals)]



| Dimension               | What it tells us                                                                     |
| ----------------------- | ------------------------------------------------------------------------------------ |
| Signal                  | Which approved zone-and-momentum conditions have qualified                           |
| Divergence color        | Whether the latest price extreme disagrees with its historical %K reference          |
| Crossover arrow         | Whether the immediate K/D relationship just changed                                  |
| Combined interpretation | Whether the observations reinforce one another, conflict or provide an early warning |


| Field                   | What it tells us                                                                     |
| ----------------------- | ------------------------------------------------------------------------------------ |
|Zone|:gray-background[Oversold] / :gray-background[Neutral] / :gray-background[Overbought]|
|Position| if $\large{\textsf{'K'}}$ is :gray-background[above] / :gray-background[below] / :gray-background[equal] to $\large{\textsf{'D'}}$|
|Cross|:gray-background[Bullish] / :gray-background[Bearish] / :gray-background[None], subject to evidence safeguards|


### Crossovers
:small[[Parent](#understanding-the-stochastic-metrics)]

> **Crossover $\large{\rightarrow}$ Spot when momentum changes direction.**

A Stochastic crossover occurs when the faster **[%K](#understanding-k-and-d)** line crosses above or below the slower **[%D](#understanding-k-and-d)** line.
- Think of it as an early warning that buyers may be gaining strength or sellers may be taking control.
- It tells you when momentum is shifting—potentially before the price trend visibly changes.

The real advantage is using this with [divergence](#divergence).
- Divergence identifies where a trend may be vulnerable; crossovers help identify when momentum begins to shift.
- Together, they help you recognize potential turning points earlier, investigate conflicting signals, and avoid relying on price alone—without pretending a reversal is guaranteed.

$$\Large{\bf{-----------}}$$

$\Large{\textcolor{black}{\textsf{▲}}}$**: Fresh bullish K/D crossover**
- When '%K' crosses **above '%D'** (after being at or below it), the faster Stochastic line has moved above its smoothed signal line.
- **Interpretation:** Bullish relative oscillator momentum is emerging; this may be an early indication of an upward turn. IOW, bullish momentum has **strengthened**.

$\Large{\textcolor{black}{\textsf{▼}}}$**: Fresh bearish K/D crossover**
- When '%K' crosses **below '%D'** (after being at or above it), the faster Stochastic line has moved below its smoothed signal line.
- **Interpretation:** Bearish relative oscillator momentum is emerging; this may be an early indication of a downward turn. IOW, bearish momentum has **weakened**.


#### Understanding the Yellow Crossover Arrows
:small[[Parent](#crossovers)]

Yellow arrows $\large{\rightarrow}$ means "*Caution: the extreme 'Zone' condition may persist rather than reverse*".
- $\large{\textcolor{orange}{\textsf{▼}}}$ while 'oversold': warns of **renewed** $\large{\textcolor{crimson}{\textsf{bearish momentum}}}$;
- $\large{\textcolor{orange}{\textsf{▲}}}$ while 'overbought': warns of **renewed** $\large{\textcolor{DodgerBlue}{\textsf{bullish momentum}}}$.

$\large{\textsf{Crossover Arrow colors by Zone}}:$

| Zone                |            Bullish Crossover             |            Bearish Crossover             |
| ------------------- | :--------------------------------------: | :--------------------------------------: |
| Oversold (K < 20)   |                    ▲                     | $\large{\textcolor{orange}{\textsf{▼}}}$ |
| Neutral (20–80)     |                    ▲                     |                    ▼                     |
| Overbought (K > 80) | $\large{\textcolor{orange}{\textsf{▲}}}$ |                    ▼                     |

> ***'Oversold'*** + $\large{\textcolor{orange}{\textsf{▼}}}$ $\large{\rightarrow}$ Downward momentum may persist despite the oversold condition
>
> ***'Overbought'*** + $\large{\textcolor{orange}{\textsf{▲}}}$ $\large{\rightarrow}$ Upward momentum may persist despite the overbought condition
>
> **Note**: You'll never see $\large{\textcolor{orange}{\textsf{▲}}}$ when 'Oversold' nor a $\large{\textcolor{orange}{\textsf{▼}}}$ when 'Overbought'


### Divergence
:small[[Parent](#understanding-the-stochastic-metrics)]

> **Divergence — Spot when price and momentum tell different stories.**
> - Can help identify where a trend may be vulnerable.

Divergence occurs when '*price*' reaches a new high or low, but Stochastic ('[%K](#understanding-k-and-d)') fails to confirm that move.
- It's an **early warning** that the apparent strength or weakness behind the price movement may be fading.
- It tells you when a trend may be losing conviction — even while price continues pushing in the same direction.

Divergence identifies where a trend may be vulnerable.
[Crossovers](#crossovers) help identify when momentum begins to shift.
Together, they help you recognize potential turning points earlier, investigate conflicting signals, and avoid relying on price alone—without pretending a reversal is guaranteed.

$$\Large{\bf{-----------}}$$

There are 2 display options:
$\large{\textcolor{blue}{\textsf{bullish divergence}}}$ and $\large{\textcolor{Red}{\textsf{bearish divergence}}}$

#### Bullish Divergence
> Emerging bullish 'Price/%K' divergence

Price makes a lower low while Stochastic [%K](#understanding-k-and-d) makes a higher reading at the corresponding swing low.
- Price has deteriorated to a lower 'low' but the oscillator reading at the low has **improved**.

#### Bearish Divergence
> Emerging bearish 'Price/%K' divergence

Price makes a higher high while Stochastic %K makes a lower reading at the corresponding swing high.
- Price makes a higher 'high' but the corresponding oscillator reading at that point has **weakened**.

---
## Reading 'Signal' + 'Divergence' + 'Crossover' Together
:small[[Back to top](#summary-stoch-14-3-3-signals)]

There are 3 general categories — **Reinforcing**, **Conflicting**, and **Early Watch** — with one additional designation, **Routine**, for observations without a new event.
  - For example, Buy + Blue value + no crossover falls under Early Watch. Although the divergence supports the bullish possibility, Buy itself lacks complete bullish momentum support, and no fresh crossover reinforces the development.
  - By contrast, Strong Buy + Blue value + no crossover is Reinforcing: the Strong Buy qualification already establishes improving oscillator momentum, and the bullish divergence adds separate structural evidence.

A few distinctions worth preserving:
- '**Early Watch**' means there is a developing observation worth monitoring, without additional corroborating event evidence.
  - A 'high-attention' conflict can demand more immediate investigation than a 'medium-attention' reinforcing setup.
- '**Conflicting**' does not automatically mean an unfavorable trade. It means the evidence is pulling in different directions.
  - That is ==particularly useful when an apparent reversal opportunity might be premature==.

'***Scope***': an 'evidence-alignment' category
- Answers the question: "*How do the observations relate?*"
'***Relative attention***' a 'review-priority' column
- Answers the question: "*How urgently should I examine the chart?*"


| Scope       | Meaning                                                                                                        |
| ----------- | -------------------------------------------------------------------------------------------------------------- |
| Reinforcing | Multiple pieces of evidence support the same potential bullish or bearish development.                         |
| Conflicting | The annotations disagree with one another or with the direction anticipated by the Signal.                     |
| Early Watch | A potentially meaningful event has appeared, but additional, independent evidence has not yet aligned with it. |
| Routine     | No new divergence or crossover event is highlighted. Existing oscillator information remains useful.           |

### BUY: Signal + Customizations

| Signal                                                                  | Divergence                             |                Crossover                |                                              Example                                              | Interpretation                                                                                                                                                     | Relative attention | Scope        |
| ----------------------------------------------------------------------- | ----------------------------------------- | :-------------------------------------: | :-----------------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------ | ------------ |
| ${\fcolorbox{none}{darkgreen}{\textcolor{white}{\textsf{Strong Buy}}}}$ | $\large{\textcolor{blue}{\textsf{bullish}}}$ |                    ▲                    |                  ${\fcolorbox{none}{Green}{\textcolor{blue}{\textsf{12.1}}~▲}}$                   | Strong reinforcement. The oscillator qualifies Strong Buy, price has made a lower low without equivalent K deterioration, and a bullish K/D crossover has occurred | High               | Reinforcing  |
| ${\fcolorbox{none}{darkgreen}{\textcolor{white}{\textsf{Strong Buy}}}}$ | $\large{\textcolor{blue}{\textsf{bullish}}}$ |                  None                   |                   ${\fcolorbox{none}{Green}{\textcolor{blue}{\textsf{12.1}}}}$                    | Bullish structural disagreement reinforces an already improving oversold oscillator                                                                                | High               | Reinforcing  |
| ${\fcolorbox{none}{lightgreen}{\textcolor{black}{\textsf{Buy}}}}$       | $\large{\textcolor{blue}{\textsf{bullish}}}$ |                    ▲                    |               ${\fcolorbox{none}{greenyellow}{\textcolor{Blue}{\textsf{12.1}}~▲}}$                | A developing bullish divergence and fresh bullish crossover support a possible reversal, but the Strong Buy criteria are not all satisfied                         | High               | Reinforcing  |
| ${\fcolorbox{none}{lightgreen}{\textcolor{black}{\textsf{Buy}}}}$       | $\large{\textcolor{blue}{\textsf{bullish}}}$ | $\large{\textcolor{orange}{\textsf{▼}}}$ | ${\fcolorbox{none}{greenyellow}{\textcolor{blue}{\textsf{12.1}}~\textcolor{orange}{\textsf{▼}}}}$ | Conflicting evidence. Price/%K disagreement is bullish, but the immediate K/D crossover is bearish                                                                 | High — caution     | Conflicting  |
| ${\fcolorbox{none}{lightgreen}{\textcolor{black}{\textsf{Buy}}}}$       | $\large{\textcolor{blue}{\textsf{bullish}}}$ |                  None                   |                ${\fcolorbox{none}{greenyellow}{\textcolor{blue}{\textsf{12.1}}}}$                 | Price/%K disagreement may be an early warning of easing selling pressure; no fresh crossover confirms improving relative momentum                                  | Medium             | Early Watch  |
| ${\fcolorbox{none}{lightgreen}{\textcolor{black}{\textsf{Buy}}}}$       | Normal                                    |                    ▲                    |               ${\fcolorbox{none}{greenyellow}{\textcolor{Black}{\textsf{12.1}}~▲}}$               | A fresh bullish crossover occurred while oversold; the observation does not satisfy all Strong Buy qualifications                                                  | Medium             | Early Watch  |
| ${\fcolorbox{none}{lightgreen}{\textcolor{black}{\textsf{Buy}}}}$       | Normal                                    | $\large{\textcolor{orange}{\textsf{▼}}}$ |   ${\fcolorbox{none}{lightgreen}{\textcolor{black}{\textsf{12.1}}~\textcolor{orange}{\textsf{▼}}}}$    | Bearish momentum is developing despite the oversold condition; the apparent opportunity may be premature                                                           | High — caution     | Conflicting  |


### SELL: Signal + Customizations

| Signal                                                                | Divergence                          |                Crossover                |                                           Example                                           | Interpretation                                                                                                                                          | Relative attention | Scope        |
| --------------------------------------------------------------------- | --------------------------------------- | :-------------------------------------: | :-----------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------ |
| ${\fcolorbox{none}{Maroon}{\textcolor{white}{\textsf{Strong Sell}}}}$ | $\large{\textcolor{Red}{\textsf{bearish}}}$ |                    ▼                    |                ${\fcolorbox{none}{Brown}{\textcolor{red}{\textsf{81.0}}~▼}}$                | Strong reinforcement. Price has reached a higher high despite weaker %K, while a fresh bearish K/D crossover accompanies the qualified Strong Sell      | High               | Reinforcing  |
| ${\fcolorbox{none}{Maroon}{\textcolor{white}{\textsf{Strong Sell}}}}$ | $\large{\textcolor{Red}{\textsf{bearish}}}$ |                  None                   |                 ${\fcolorbox{none}{Brown}{\textcolor{red}{\textsf{81.0}}}}$                 | Bearish structural disagreement supports the already deteriorating overbought oscillator                                                                | High               | Reinforcing  |
| ${\fcolorbox{none}{Salmon}{\textsf{Sell}}}$                           | $\large{\textcolor{Red}{\textsf{bearish}}}$ |                    ▼                    |               ${\fcolorbox{none}{Salmon}{\textcolor{Red}{\textsf{81.0}}~▼}}$                | Emerging bearish divergence and a fresh bearish crossover point toward possible downside development, although full Strong Sell qualification is absent | High               | Reinforcing  |
| ${\fcolorbox{none}{Salmon}{\textsf{Sell}}}$                           | $\large{\textcolor{Red}{\textsf{bearish}}}$ | $\large{\textcolor{orange}{\textsf{▲}}}$ | ${\fcolorbox{none}{Salmon}{\textcolor{red}{\textsf{81.0}}~\textcolor{orange}{\textsf{▲}}}}$ | Conflicting evidence. Price/%K divergence warns of weakening buying momentum, but today's crossover is bullish                                          | High — caution     | Conflicting  |
| ${\fcolorbox{none}{Salmon}{\textsf{Sell}}}$                           | $\large{\textcolor{Red}{\textsf{bearish}}}$ |                  None                   |                ${\fcolorbox{none}{Salmon}{\textcolor{red}{\textsf{81.0}}}}$                 | Price/%K disagreement suggests possible weakening at a price high; a fresh bearish crossover has not occurred                                           | Medium             | Early Watch  |
| ${\fcolorbox{none}{Salmon}{\textsf{Sell}}}$                           | Normal                                  |                    ▼                    |              ${\fcolorbox{none}{Salmon}{\textcolor{black}{\textsf{81.0}}~▼}}$               | A fresh bearish crossover while overbought provides early reversal-related evidence                                                                     | Medium             | Early Watch  |
| ${\fcolorbox{none}{Salmon}{\textsf{Sell}}}$                           | Normal                                  | $\large{\textcolor{orange}{\textsf{▲}}}$ |  ${\fcolorbox{none}{Salmon}{\textcolor{black}{\textsf{81.0}}~\textcolor{orange}{\textsf{▲}}}}$   | Bullish momentum is developing despite the overbought condition; upside persistence may undermine the contrarian Sell setup                             | High — caution     | Conflicting  |


### NEUTRAL: Signal + Customizations

| Signal                                                               | Divergence                             | Crossover |                               Example                                | Interpretation                                                                                                                             | Relative attention | Scope        |
| -------------------------------------------------------------------- | ----------------------------------------- | :-------: | :------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------ | ------------ |
| ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{Neutral}}}}$ | $\large{\textcolor{blue}{\textsf{bullish}}}$ |     ▲     |  ${\fcolorbox{none}{gainsboro}{\textcolor{blue}{\textsf{50.0}}~▲}}$  | Bullish reinforcement. Price made a new lower low without matching oscillator weakness, and immediate K/D momentum has turned upward       | High               | Reinforcing  |
| ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{Neutral}}}}$ | $\large{\textcolor{Red}{\textsf{bearish}}}$   |     ▼     |  ${\fcolorbox{none}{gainsboro}{\textcolor{red}{\textsf{50.0}}~▼}}$   | Bearish reinforcement. Price made a higher high without matching oscillator strength, and immediate K/D momentum has turned downward       | High               | Reinforcing  |
| ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{Neutral}}}}$ | $\large{\textcolor{blue}{\textsf{bullish}}}$ |     ▼     |  ${\fcolorbox{none}{gainsboro}{\textcolor{blue}{\textsf{50.0}}~▼}}$  | Bullish structural warning, bearish immediate momentum. The measures disagree; watch whether the emerging bullish anomaly survives         | High — mixed       | Conflicting  |
| ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{Neutral}}}}$ | $\large{\textcolor{Red}{\textsf{bearish}}}$   |     ▲     |  ${\fcolorbox{none}{gainsboro}{\textcolor{red}{\textsf{50.0}}~▲}}$   | Bearish structural warning, bullish immediate momentum. The measures disagree; continued upside momentum could persist despite the anomaly | High — mixed       | Conflicting  |
| ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{Neutral}}}}$ | $\large{\textcolor{blue}{\textsf{bullish}}}$ |   None    |   ${\fcolorbox{none}{gainsboro}{\textcolor{blue}{\textsf{50.0}}}}$   | Price is making lower lows without matching oscillator deterioration; potential early bullish development                                  | Medium             | Early Watch  |
| ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{Neutral}}}}$ | $\large{\textcolor{Red}{\textsf{bearish}}}$   |   None    |   ${\fcolorbox{none}{gainsboro}{\textcolor{red}{\textsf{50.0}}}}$    | Price is making higher highs without matching oscillator improvement; potential early bearish development                                  | Medium             | Early Watch  |
| ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{Neutral}}}}$ | Normal                                    |   ▲ / ▼   | ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{50.0}}~▲/▼}}$ | Fresh oscillator momentum transition, without emerging divergence or an extreme-zone classification                                        | Routine context    | Early Watch  |
| ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{Neutral}}}}$ | Normal                                    |   None    |   ${\fcolorbox{none}{gainsboro}{\textcolor{black}{\textsf{50.0}}}}$   | No new event highlighted; existing Trend, Position, Spread and K/D development remain informative                                          | Routine            | Routine      |

---

## STOCH(14,3,3) Rule Translation
:small[[Back to top](#summary-stoch-14-3-3-signals)]

### Strong buy

```json
"strong_buy": "STOCHK_14_3_3 < 20 and STOCHK_14_3_3 > STOCHD_14_3_3 and rising_2bar(STOCHK_14_3_3, 1)"
```

#### Literal component breakdown

:blue-background[STOCHK_14_3_3 < 20]

* The current :blue-background[%K] value is below '20'.
* The oscillator is in the project’s oversold zone.
* Layman’s translation: **price is closing near the lower end of its recent 14-period range.**

:blue-background[STOCHK_14_3_3 > STOCHD_14_3_3]

* The faster :blue-background[%K] line is above the smoothed :blue-background[%D] signal line.
* This indicates that short-term oscillator momentum has improved relative to its smoother baseline.
* Layman’s translation: **the faster Stochastic line has moved above its slower signal line.**

:blue-background[rising_2bar(STOCHK_14_3_3, 1)]

* Despite the helper’s legacy name, the explicit argument '1' makes this a current-versus-prior-period comparison.
* The current :blue-background[%K] value is greater than the immediately preceding :blue-background[%K] value.
* Layman’s translation: **%K has risen since the prior period.**

#### Literal summary

:blue-background[%K] is below '20', :blue-background[%K] is above :blue-background[%D], and :blue-background[%K] is higher than it was one period earlier.

#### Plain-English version

That means STOCH is oversold, but :blue-background[%K] is now rising and sits above its smoothed :blue-background[%D] line.

#### Interpretation

This is a **strong bullish reversal-confirmation state from the oversold zone**.

It requires three layers:

1. :blue-background[%K] is in the oversold zone;
2. :blue-background[%K] is above :blue-background[%D];
3. :blue-background[%K] is rising from the prior period.

The rule is stronger than a simple oversold reading because it requires evidence that oscillator momentum is turning upward.

#### Notes / confidence

* The :gray-background[20] threshold is a conventional Stochastic oversold reference.
* The :blue-background[%K > %D] relationship is commonly interpreted as bullish oscillator positioning.
* The one-bar rise is a project-selected confirmation rule intended to identify the turn promptly without the additional lag of a two-consecutive-move requirement.
* This is a reversal-confirmation state, not a guarantee that price has formed a durable bottom.
* An actual bullish crossover may have occurred on the same bar or earlier. The rule requires current positioning, not a current-bar crossover event.

---

### Buy

```json
"buy": "STOCHK_14_3_3 < 20 and (STOCHK_14_3_3 <= STOCHD_14_3_3 or not_rising_2bar(STOCHK_14_3_3, 1))"
```

#### Literal component breakdown

:blue-background[STOCHK_14_3_3 < 20]

* The current :blue-background[%K] value is below '20'.
* The oscillator is in the oversold zone.
* Layman’s translation: **price is closing near the lower end of its recent range.**

:blue-background[STOCHK_14_3_3 <= STOCHD_14_3_3]

* :blue-background[%K] is below or equal to :blue-background[%D].
* The faster oscillator line has not established bullish positioning above its smoothed signal line.
* Layman’s translation: **%K has not moved above %D.**

:blue-background[not_rising_2bar(STOCHK_14_3_3, 1)]

* The current :blue-background[%K] value is not greater than the immediately preceding :blue-background[%K] value.
* :blue-background[%K] is flat or falling versus the prior period.
* Layman’s translation: **%K has not risen since the prior period.**

:blue-background[... <= STOCHD ... or not_rising_2bar(...)]

* Only one of these conditions needs to be true.
* The rule captures every oversold observation that does not satisfy the complete Strong Buy combination.
* Layman’s translation: **STOCH is oversold, but at least one required reversal confirmation is still missing.**

#### Literal summary

:blue-background[%K] is below '20', but :blue-background[%K] is either not above :blue-background[%D] or not rising from the prior period.

#### Plain-English version

That means STOCH is oversold, but the upward reversal is not fully confirmed.

#### Interpretation

This is a **bullish contrarian extreme-zone condition without complete reversal confirmation**.

The signal acknowledges that price is near the lower end of its recent range, but it does not claim that momentum has decisively turned upward.

#### Notes / confidence

* [Buy](#buy) is intentionally weaker than [Strong Buy](#strong-buy).
* It can occur while :blue-background[%K] is still below :blue-background[%D], while :blue-background[%K] is still falling, or both.
* The signal should be read as “oversold setup” rather than “confirmed bottom.”
* In a strong downtrend, STOCH may remain oversold and continue producing a Buy state without an immediate price reversal.

---

### Neutral

```json
"neutral": "20 <= STOCHK_14_3_3 <= 80"
```

#### Literal component breakdown

:blue-background[20 <= STOCHK_14_3_3]

* :blue-background[%K] is at least '20'.
* It is not below the oversold threshold.
* Layman’s translation: **%K is no longer in the oversold zone.**

:blue-background[STOCHK_14_3_3 <= 80]

* :blue-background[%K] is no greater than '80'.
* It is not above the overbought threshold.
* Layman’s translation: **%K has not entered the overbought zone.**

:blue-background[20 <= STOCHK_14_3_3 <= 80]

* :blue-background[%K] lies within the middle range.
* The exact values '20' and '80' are included in Neutral.
* Layman’s translation: **STOCH is between its two extreme zones.**

#### Literal summary

:blue-background[%K] is between '20' and '80', inclusive.

#### Plain-English version

That means price is not currently closing near enough to the top or bottom of its recent range to activate an extreme-zone signal.

#### Interpretation

This is a **middle-range / no-active-extreme state**.

Neutral does not mean that price has no momentum or no trend. It means only that the Stochastic :blue-background[%K] value is not inside the rule set’s oversold or overbought zones.

#### Notes / confidence

* :blue-background[%K = 20] is Neutral.
* :blue-background[%K = 80] is Neutral.
* :blue-background[%K/%D] positioning and one-bar direction do not change the classification while :blue-background[%K] remains in this middle range.
* The rule deliberately reserves Buy/Sell classifications for readings strictly outside the middle band.

---

### Sell

```json
"sell": "STOCHK_14_3_3 > 80 and (STOCHK_14_3_3 >= STOCHD_14_3_3 or not_falling_2bar(STOCHK_14_3_3, 1))"
```

#### Literal component breakdown

:blue-background[STOCHK_14_3_3 > 80]

* The current :blue-background[%K] value is above '80'.
* The oscillator is in the overbought zone.
* Layman’s translation: **price is closing near the upper end of its recent range.**

:blue-background[STOCHK_14_3_3 >= STOCHD_14_3_3]

* :blue-background[%K] is above or equal to :blue-background[%D].
* The faster oscillator line has not established bearish positioning below its smoothed signal line.
* Layman’s translation: **%K has not moved below %D.**

:blue-background[not_falling_2bar(STOCHK_14_3_3, 1)]

* The current :blue-background[%K] value is not below the immediately preceding :blue-background[%K] value.
* :blue-background[%K] is flat or rising versus the prior period.
* Layman’s translation: **%K has not fallen since the prior period.**

:blue-background[... >= STOCHD ... or not_falling_2bar(...)]

* Only one of these conditions needs to be true.
* The rule captures every overbought observation that does not satisfy the complete Strong Sell combination.
* Layman’s translation: **STOCH is overbought, but at least one required bearish reversal confirmation is still missing.**

#### Literal summary

:blue-background[%K] is above '80', but :blue-background[%K] is either not below :blue-background[%D] or not falling from the prior period.

#### Plain-English version

That means STOCH is overbought, but the downward reversal is not fully confirmed.

#### Interpretation

This is a **bearish contrarian extreme-zone condition without complete reversal confirmation**.

The signal recognizes that price is near the upper end of its recent range, but it does not claim that momentum has decisively turned downward.

#### Notes / confidence

* [Sell](#sell) is intentionally weaker than [Strong Sell](#strong-sell).
* It can occur while :blue-background[%K] remains above :blue-background[%D], while :blue-background[%K] is still rising, or both.
* The signal should be read as “overbought setup” rather than “confirmed top.”
* In a strong uptrend, STOCH may remain overbought and continue producing a Sell state without an immediate price reversal.

---

### Strong sell

```json
"strong_sell": "STOCHK_14_3_3 > 80 and STOCHK_14_3_3 < STOCHD_14_3_3 and falling_2bar(STOCHK_14_3_3, 1)"
```

#### Literal component breakdown

:blue-background[STOCHK_14_3_3 > 80]

* The current :blue-background[%K] value is above '80'.
* The oscillator is in the project’s overbought zone.
* Layman’s translation: **price is closing near the upper end of its recent 14-period range.**

:blue-background[STOCHK_14_3_3 < STOCHD_14_3_3]

* The faster :blue-background[%K] line is below the smoothed :blue-background[%D] signal line.
* This indicates that short-term oscillator momentum has weakened relative to its smoother baseline.
* Layman’s translation: **the faster Stochastic line has moved below its slower signal line.**

:blue-background[falling_2bar(STOCHK_14_3_3, 1)]

* Despite the helper’s legacy name, the explicit argument :gray-background[1] makes this a current-versus-prior-period comparison.
* The current :blue-background[%K] value is lower than the immediately preceding :blue-background[%K] value.
* Layman’s translation: **%K has fallen since the prior period.**

#### Literal summary

:blue-background[%K] is above '80', :blue-background[%K] is below :blue-background[%D], and :blue-background[%K] is lower than it was one period earlier.

#### Plain-English version

That means STOCH is overbought, but :blue-background[%K] is now falling and sits below its smoothed :blue-background[%D] line.

#### Interpretation

This is a **strong bearish reversal-confirmation state from the overbought zone**.

It requires three layers:

1. :blue-background[%K] is in the overbought zone;
2. :blue-background[%K] is below :blue-background[%D];
3. :blue-background[%K] is falling from the prior period.

The rule is stronger than a simple overbought reading because it requires evidence that oscillator momentum is turning downward.

#### Notes / confidence

* The :gray-background[80] threshold is a conventional Stochastic overbought reference.
* The :blue-background[%K < %D] relationship is commonly interpreted as bearish oscillator positioning.
* The one-bar decline is a project-selected confirmation rule intended to identify the turn promptly without the additional lag of a two-consecutive-move requirement.
* This is a reversal-confirmation state, not a guarantee that price has formed a durable top.
* An actual bearish crossover may have occurred on the same bar or earlier. The rule requires current positioning, not a current-bar crossover event.

---

## Industry-standard baseline

Standard Stochastic interpretation usually emphasizes:
* Stochastic ranges from **0 to 100** and shows where the close sits relative to the recent high-low range.
* The common overbought / oversold zones are **above 80** and **below 20**.
  * A classic '*buy*' signal ("Oversold") often involves Stochastic (':blue-background[%K]') moving up from oversold, especially below/around 20.
  * A classic '*sell*' signal  ("Overbought") often involves Stochastic (':blue-background[%K]') moving down from overbought, especially above/around 80.
* :blue-background[%K/%D] crosses or relative positioning can suggest improving or weakening oscillator momentum.
  * %K / %D crossovers are often most meaningful when they occur in overbought or oversold zones, not necessarily in the middle of the range. 
* Extreme readings should be interpreted in trend context because an oscillator can remain overbought or oversold during a persistent trend.

Industry practice does not usually define the project’s exact five-level scoring system. A basic industry-style interpretation is:

| Condition | Basic translation |
| --- | --- |
| :blue-background[%K < 20] | Oversold; price is closing near the bottom of its recent range. |
| :blue-background[%K < 20] and :blue-background[%K] turns above :blue-background[%D] | Potential bullish reversal from oversold territory. |
| :blue-background[20 <= %K <= 80] | Middle range; no active Stochastic extreme. |
| :blue-background[%K > 80] | Overbought; price is closing near the top of its recent range. |
| :blue-background[%K > 80] and :blue-background[%K] turns below :blue-background[%D] | Potential bearish reversal from overbought territory. |

The project adds a formal distinction between an unconfirmed extreme and a reversal-confirmed Strong state.




---

## Comparison of the three Stochastic settings
:small[[Back to top](#summary-stoch-14-3-3-signals)]

All three settings use the same :gray-background[20/80] zones and the same five-state Model E logic. Their main difference is responsiveness.

| Setting | Relative speed | What it emphasizes | When it is most applicable | Main trade-off |
| --- | --- | --- | --- | --- |
| STOCH(5,3,3) | Fastest | Very recent shifts in range position and momentum | Short-term monitoring, faster swing setups, and cases where early reversal evidence matters | More responsive, but more sensitive to short-lived noise and rapid state changes |
| STOCH(14,3,3) | Balanced | A conventional intermediate view of range position and momentum | General-purpose daily analysis and a balance between early response and stability | May react later than the 5-period version but remains more responsive than the 21-period version |
| STOCH(21,5,5) | Slowest and smoothest | More persistent changes in range position and momentum | Slower swing analysis, confirmation-oriented use, and cases where fewer state changes are preferred | Filters more noise but can confirm turns later |

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
:small[[Back to top](#summary-stoch-14-3-3-signals)]

### STOCH(14,3,3) Rules interpretation

| Source | Signal | Rule logic | What's happening | Answers the question| Bottom-line|
| --- | --- | --- | --- | --- | --- |
| **STOCH(14,3,3)** | Strong Buy | :gray-background[STOCHK_14_3_3 < 20 and STOCHK_14_3_3 > STOCHD_14_3_3 and rising_2bar(STOCHK_14_3_3, 1)] | STOCH is oversold, and :blue-background[%K] is rising above :blue-background[%D]. | *“Is STOCH oversold and showing a confirmed upward turn?”* | Near the bottom of its recent range, and the indicator is showing a confirmed upward turn|
| **STOCH(14,3,3)** | Buy | :gray-background[STOCHK_14_3_3 < 20 and (STOCHK_14_3_3 <= STOCHD_14_3_3 or not_rising_2bar(STOCHK_14_3_3, 1))] | STOCH is oversold, but the upward turn is not fully confirmed. | *“Is STOCH oversold w/o complete bullish reversal confirmation?”* |Near the bottom of its recent range, but the indicator has not yet confirmed a clear upward turn.|
| **STOCH(14,3,3)** | Neutral | :gray-background[20 <= STOCHK_14_3_3 <= 80] | STOCH is between its oversold and overbought zones. | *“Is STOCH currently outside both extreme zones?”* |Trading in the middle portion of its recent range rather than near either extreme.|
| **STOCH(14,3,3)** | Sell | :gray-background[STOCHK_14_3_3 > 80 and (STOCHK_14_3_3 >= STOCHD_14_3_3 or not_falling_2bar(STOCHK_14_3_3, 1))] | STOCH is overbought, but the downward turn is not fully confirmed. | *“Is STOCH overbought w/o complete bearish reversal confirmation?”* |Trading near the top of its recent range, but the indicator has not yet confirmed a clear downward turn.|
| **STOCH(14,3,3)** | Strong Sell | :gray-background[STOCHK_14_3_3 > 80 and STOCHK_14_3_3 < STOCHD_14_3_3 and falling_2bar(STOCHK_14_3_3, 1)] | STOCH is overbought, and :blue-background[%K] is falling below :blue-background[%D]. | *“Is STOCH overbought and showing a confirmed downward turn?”* |Trading near the top of its recent range, and the indicator is showing a confirmed downward turn.|

### STOCH(5,3,3) Rules interpretation

| Source | Signal | Rule logic | What's happening | Answers the question| Bottom-line|
| --- | --- | --- | --- | --- | --- |
| **STOCH(5,3,3)** | Strong Buy | :gray-background[STOCHK_5_3_3 < 20 and STOCHK_5_3_3 > STOCHD_5_3_3 and rising_2bar(STOCHK_5_3_3, 1)] | The fast STOCH is oversold, and :blue-background[%K] is rising above :blue-background[%D]. | *“Is the short-term STOCH oversold and already turning upward?”* | Trading near the low end of its recent range and now appears to be turning upward.|
| **STOCH(5,3,3)** | Buy | :gray-background[STOCHK_5_3_3 < 20 and (STOCHK_5_3_3 <= STOCHD_5_3_3 or not_rising_2bar(STOCHK_5_3_3, 1))] | The fast STOCH is oversold, but the upward turn is incomplete. | *“Is the short-term STOCH oversold w/o full bullish confirmation?”* |Price looks low compared with its recent range, but there is not yet enough evidence of a rebound.|
| **STOCH(5,3,3)** | Neutral | :gray-background[20 <= STOCHK_5_3_3 <= 80] | The fast STOCH is between its two extreme zones. | *“Is the short-term STOCH outside both extreme zones?”* |Price is neither especially high nor especially low compared with its recent range.|
| **STOCH(5,3,3)** | Sell | :gray-background[STOCHK_5_3_3 > 80 and (STOCHK_5_3_3 >= STOCHD_5_3_3 or not_falling_2bar(STOCHK_5_3_3, 1))] | The fast STOCH is overbought, but the downward turn is incomplete. | *“Is the short-term STOCH overbought w/o full bearish confirmation?”* |Price looks high compared with its recent range, but there is not yet enough evidence of a pullback.|
| **STOCH(5,3,3)** | Strong Sell | :gray-background[STOCHK_5_3_3 > 80 and STOCHK_5_3_3 < STOCHD_5_3_3 and falling_2bar(STOCHK_5_3_3, 1)] | The fast STOCH is overbought, and :blue-background[%K] is falling below :blue-background[%D]. | *“Is the short-term STOCH overbought and already turning downward?”* |Price has been trading near the high end of its recent range and now appears to be turning downward.|

### STOCH(21,5,5) Rules interpretation

| Source | Signal | Rule logic | What's happening | Answers the question| Bottom-line|
| --- | --- | --- | --- | --- | --- |
| **STOCH(21,5,5)** | Strong Buy | :gray-background[STOCHK_21_5_5 < 20 and STOCHK_21_5_5 > STOCHD_21_5_5 and rising_2bar(STOCHK_21_5_5, 1)] | The smoother STOCH is oversold, and :blue-background[%K] is rising above :blue-background[%D]. | *“Is the slower STOCH oversold and showing a sustained-looking upward turn?”* |Price looks beaten down, but it may be starting to recover.|
| **STOCH(21,5,5)** | Buy | :gray-background[STOCHK_21_5_5 < 20 and (STOCHK_21_5_5 <= STOCHD_21_5_5 or not_rising_2bar(STOCHK_21_5_5, 1))] | The smoother STOCH is oversold, but the upward turn is incomplete. | *“Is the slower STOCH oversold w/o full bullish confirmation?”* |Price looks beaten down, but it may still be falling.|
| **STOCH(21,5,5)** | Neutral | :gray-background[20 <= STOCHK_21_5_5 <= 80] | The smoother STOCH is between its two extreme zones. | *“Is the slower STOCH outside both extreme zones?”* |Price is somewhere in the middle.|
| **STOCH(21,5,5)** | Sell | :gray-background[STOCHK_21_5_5 > 80 and (STOCHK_21_5_5 >= STOCHD_21_5_5 or not_falling_2bar(STOCHK_21_5_5, 1))] | The smoother STOCH is overbought, but the downward turn is incomplete. | *“Is the slower STOCH overbought w/o full bearish confirmation?”* |Price looks stretched, but it may still keep rising.|
| **STOCH(21,5,5)** | Strong Sell | :gray-background[STOCHK_21_5_5 > 80 and STOCHK_21_5_5 < STOCHD_21_5_5 and falling_2bar(STOCHK_21_5_5, 1)] | The smoother STOCH is overbought, and :blue-background[%K] is falling below :blue-background[%D]. | *“Is the slower STOCH overbought and showing a sustained-looking downward turn?”* |Price looks stretched and may be starting to fall.|


---
## Understanding '%K' and '%D'
:small[[Back to top](#summary-stoch-14-3-3-signals)]

#### Difference between %K and %D
:small[[Parent](#understanding-k-and-d)]

| Term | What it is                           | What it tells you                                                                                     |
| ---- | ------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| :blue-background[%K] | The primary Stochastic line          | Where the close is within the recent high-low range, usually after smoothing depending on the version |
| :blue-background[%D] | A moving average / smoothing of :blue-background[%K] | The signal line used to judge whether %K is turning up or down                                        |

In your project’s naming:

```text
STOCHK_14_3_3 = %K
STOCHD_14_3_3 = %D
```

Consider this comparison:

```json
"buy": "STOCHK_14_3_3 > STOCHD_14_3_3"
```

Literal translation:

> The %K line is above the %D line.

Plain-English version:

> The current Stochastic reading is stronger than its smoothed signal line.

This relationship provides evidence of bullish relative oscillator momentum. However, it is only one component of the project's Strong Buy rule, which also requires %K below 20 and rising from the preceding session.

#### What '%K = 80' means
:small[[Parent](#understanding-k-and-d)]

A :blue-background[%K] value around :gray-background[80] means:
> The close is near the upper end of its recent high-low range.

A :blue-background[%K] value around :gray-background[20] means:
> The close is near the lower end of its recent high-low range.

A :blue-background[%K] value around :gray-background[50] means:
> The close is near the middle of its recent range.

#### What '%D' adds
:small[[Parent](#understanding-k-and-d)]

:blue-background[%D] does **not** directly tell you where the latest close sits in the range. It is a smoothed version of :blue-background[%K].

So :blue-background[%D] is more like:
> The recent average / signal-line version of the Stochastic reading.

That is why the rulebook compares :blue-background[%K] to :blue-background[%D]:

```text
%K > %D  → current Stochastic is above its smoothed signal line
%K < %D  → current Stochastic is below its smoothed signal line
```

> **%K** shows where the close sits within the recent high-low range. 
> **%D** is the smoothed signal line used to confirm whether %K is turning up or down.


---
## Notes: Stochastic Oscillator
:small[[Back to top](#summary-stoch-14-3-3-signals)]

The **Stochastic Oscillator** compares where the latest closing price sits relative to the recent high-low range.

For **Stoch(14,3,3)**:
* :gray-background[14] = lookback window for the recent high-low range.
* First :gray-background[3] = smoothing applied to :blue-background[%K].
* Second :gray-background[3] = smoothing used to create :blue-background[%D].

In this project:

```text
STOCHK_14_3_3 = %K line
STOCHD_14_3_3 = %D line
```

**Simple interpretation (:blue-background[%K] and :blue-background[%D]):**
* :blue-background[%K] above :blue-background[%D] = short-term momentum is leaning bullish.
* :blue-background[%K] below :blue-background[%D] = short-term momentum is leaning bearish.
* :blue-background[%K] near the middle zone, around 50, suggests balanced / unclear momentum.
* :blue-background[%K] rising or falling adds directional confirmation.


**Interpretation (Index values)**:
Compares closing price to its range over a period, scaled 0-100.
- Above 80 = overbought conditions
- Below 20 = oversold conditions
- **Buy**: %K line > 50 = bullish signal
	- %K crossing above %D = bullish signal
- **Sell**: %K line < 50 = bearish signal
	- %K crossing below %D = bearish signal
- **Neutral**: Around 50 or no clear crossover.

(See 'More about :blue-background[%K] & :blue-background[%D]' below for more information)

---
### 101
**Purpose:** Compare a security's closing price to its price range over a given period to identify momentum turning points (ie,  potential market reversals) and overbought/oversold levels.

**Use when:** You want to time entries and exits based on where current price sits relative to recent highs and lows.
- Use Stochastic when you want to see whether price is closing closer to the top or bottom of its recent range, and whether short-term momentum is turning up or down.

**Key Concept:** Measures where the current close is relative to the high-low range. A close near the high suggests buying pressure; a close near the low suggests selling pressure.

**Calculation:**
- :blue-background[%K = [(Current Close - Lowest Low) ÷ (Highest High - Lowest Low)] × 100]
- :blue-background[%D = 3-period moving average of %K]
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

