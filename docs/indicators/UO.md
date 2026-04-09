Status: Working

- **Purpose:** To measure momentum across different timeframes, aiming to reduce false signals. 
- **Calculation:** Incorporates data from three time periods (7, 14, and 28) to create a single, more stable momentum measurement. 
	- Default settings are 7, 14, and 28 periods for the short, medium,
- **Features:**
    - **Multi-Timeframe:** Addresses limitations of single-timeframe oscillators by combining data from different trends. 
    - **Divergence-Based Signals:** Relies on divergences between the indicator and price as a primary signal for buy and sell orders. 
    - **Volatility Reduction:** The multi-timeframe approach helps smooth out the signal, leading to fewer false signals

$$----------$$

UO uses three different periods to capture a broader view of momentum. 
- Uses three different time periods (7, 14, and 28) to measure momentum across short, medium, and long-term trends, aiming to provide more reliable buy and sell signals by reducing volatility

**Signals:** UO relies on "*divergences*" for signals, a strategy that helps confirm potential trend reversals.

**Volatility vs. Signal Generation:** UO is designed to <u>reduce volatility</u> and generate <u>fewer but more reliable signals</u>, whereas [[#Awesome Oscillator (AO)|AO]] can produce more frequent signals but with less reliability in certain market conditions.

---

$\large{\rightarrow}$ Gemini 
> **Adjusting the settings**
 
- **For higher sensitivity:**
    If the default settings are too slow for a particular security, you can shorten the timeframes (e.g., to 4, 8, and 16 periods).
    
- **For lower sensitivity:**
    For highly volatile stocks, you can lengthen the timeframes to reduce noise and get fewer signal