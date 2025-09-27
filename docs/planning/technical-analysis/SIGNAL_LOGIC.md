# Technical Analysis Signal Logic Specifications - CORRECTED
**Project**: Stock Performance Dashboard - Technical Analysis Extension  
**Date**: September 26, 2025  
**Version**: 1.1 - CORRECTED  
**Status**: Implementation Ready

---

## 📋 OVERVIEW

This document contains the precise signal logic specifications for all technical indicators in the Technical Analysis Suite. Each indicator includes calculation parameters, signal classification rules, and implementation guidelines.

**Signal Classifications Used:**
- **Buy**: Bullish signal, positive momentum
- **Sell**: Bearish signal, negative momentum  
- **Strong Buy**: Extremely bullish condition
- **Strong Sell**: Extremely bearish condition
- **Neutral**: No clear directional bias
- **Special States**: Overbought, Oversold, with contextual descriptions

---

## 📊 MOVING AVERAGES SIGNAL LOGIC - CORRECTED

### **Simple Moving Average (SMA) & Exponential Moving Average (EMA)**

**Calculation Periods**: 5, 9, 10, 20, 21, 50, 100, 200 days

**Signal Logic Rules (CORRECTED - ±0.025% neutral zone):**
```python
def moving_average_signal(current_price: float, ma_value: float) -> str:
    percentage_diff = ((current_price - ma_value) / ma_value) * 100
    
    if percentage_diff >= 0.025:
        return "Buy"
    elif percentage_diff <= -0.025:  
        return "Sell"
    else:
        return "Neutral"  # Between +0.025% and -0.025%
```

**Implementation Notes:**
- **Neutral Zone**: ±0.025% around moving average value (CORRECTED)
- **Buy Signal**: Current price ≥ 0.025% above moving average
- **Sell Signal**: Current price ≤ 0.025% below moving average
- **Bidirectional Analysis**: Calculate both MA vs Price and Price vs MA percentages

**Comment Generation Examples:**
- "NVDA is +4.1% above its 50D EMA. It has to fall -4.0% to reach it."
- "NVDA is +26.6% above its 200D SMA. It has to fall -21.0% to reach it."
- "Short-term MA(20) is above long-term MA(50), indicating bullish trend."

---

## 🎯 TECHNICAL INDICATORS SIGNAL LOGIC - UPDATED

### **RSI (Relative Strength Index) - Period 14 - CORRECTED**

**Calculation**: Standard RSI formula over 14-day period

**Hierarchical Signal Logic (CORRECTED - New neutral zone 35-70):**
```python
def rsi_signal(rsi_value: float) -> Tuple[str, str]:
    if rsi_value >= 80:
        return "Strong Sell", "Extremely overbought"
    elif rsi_value >= 70:
        return "Sell", "Overbought, potential selling opportunity"
    elif rsi_value >= 35:
        return "Neutral", "Within neutral range"
    elif rsi_value >= 20:
        return "Buy", "Oversold, potential buying opportunity"
    elif rsi_value > 0:
        return "Strong Buy", "Extremely oversold"
    else:
        return "Error", "Invalid RSI value"
```

**Signal Thresholds (UPDATED):**
- **≥80**: Extremely overbought (Strong Sell)
- **70-79**: Overbought (Sell)
- **35-69**: Neutral range (Neutral) - MUCH MORE REALISTIC
- **20-34**: Oversold (Buy)
- **>0-19**: Extremely oversold (Strong Buy)

---

### **STOCH (Stochastic Oscillator) - Periods 9,6**

**Calculation**: %K and %D lines using 9-period %K and 6-period %D smoothing

**Signal Logic Rules:**
```python
def stochastic_signal(k_value: float, d_value: float) -> Tuple[str, str]:
    if k_value > 80:
        return "Sell", "Overbought territory"
    elif k_value < 20:
        return "Buy", "Oversold territory"
    elif k_value > 50:
        return "Buy", "%K above 50, bullish bias"
    elif k_value < 50:
        return "Sell", "%K below 50, bearish bias"
    else:
        return "Neutral", "Around midpoint"
    
    # Additional crossover logic (requires historical data):
    # if k_crosses_above_d: return "Buy", "%K crosses above %D"  
    # if k_crosses_below_d: return "Sell", "%K crosses below %D"
```

**Signal Thresholds:**
- **>80**: Overbought (Sell signal expected)
- **<20**: Oversold (Buy signal expected)  
- **>50**: Bullish bias (Buy)
- **<50**: Bearish bias (Sell)
- **Crossovers**: %K crossing %D provides additional confirmation

---

### **STOCHRSI (Stochastic RSI) - Period 14**

**Calculation**: Stochastic oscillator applied to RSI values

**Signal Logic Rules:**
```python
def stochrsi_signal(stochrsi_value: float) -> Tuple[str, str]:
    if stochrsi_value > 80:
        return "Sell", "Overbought, momentum too high, potential reversal down"
    elif stochrsi_value < 20:
        return "Buy", "Oversold, momentum too low, potential reversal up"
    else:
        return "Neutral", "Between 20-80 without strong signals"
    
    # Crossover logic (requires signal line):
    # if crosses_above_oversold: return "Buy", "Cross above oversold level"
    # if crosses_below_overbought: return "Sell", "Cross below overbought level"
```

**Signal Thresholds:**
- **>80**: Overbought, potential reversal down (Sell)
- **<20**: Oversold, potential reversal up (Buy)
- **20-80**: Neutral range without strong signals

---

### **MACD (Moving Average Convergence Divergence) - Periods 12,26,9**

**Calculation**: MACD line (12EMA - 26EMA), Signal line (9EMA of MACD), Histogram (MACD - Signal)

**Signal Logic Rules:**
```python
def macd_signal(macd_value: float, signal_line: float) -> Tuple[str, str]:
    if macd_value > 0:
        if macd_value > signal_line:
            return "Buy", "Above zero with bullish crossover"
        else:
            return "Buy", "Above zero, bullish momentum"
    else:  # macd_value < 0
        if macd_value < signal_line:
            return "Sell", "Below zero with bearish crossover"
        else:
            return "Sell", "Below zero, bearish momentum"
    
    # Special case for macd ≈ 0:
    # if abs(macd_value) < 0.01: return "Neutral", "MACD near zero, flat"
```

**Signal Rules:**
- **MACD > 0**: Bullish momentum (Buy)
- **MACD < 0**: Bearish momentum (Sell)
- **MACD > Signal Line**: Additional bullish confirmation
- **MACD < Signal Line**: Additional bearish confirmation  
- **MACD ≈ 0**: Neutral/flat momentum

**Crossover Detection Requirements:**
- **Historical Data Needed**: 5-7 days for reliable MACD signal line crossover detection
- **Implementation**: Store previous MACD and signal line values for crossover analysis

---

### **ADX (Average Directional Index) - Period 14 - CORRECTED**

**Calculation**: ADX, +DI (Positive Directional Indicator), -DI (Negative Directional Indicator)

**Complex Signal Logic Implementation (CORRECTED):**
```python
def adx_signal(adx_value: float, plus_di: float, minus_di: float) -> Tuple[str, str]:
    # Step 1: Determine trend strength
    if adx_value >= 75:
        trend_strength = "Unsustainably Strong"
    elif adx_value >= 50:
        trend_strength = "Strong"
    elif adx_value >= 25:
        trend_strength = "Moderate"
    elif adx_value >= 20:
        trend_strength = "Weak"
    else:
        trend_strength = "No Trend"
    
    # Step 2: If no trend, return Neutral
    if adx_value < 25:
        return "Neutral", f"{trend_strength} (Neutral)"
    
    # Step 3: Determine trend direction and signal (CORRECTED)
    if adx_value >= 60 and minus_di > plus_di:
        signal = "Strong Sell"
    elif adx_value >= 50 and minus_di > plus_di:  # CORRECTED: was -DI > -DI
        signal = "Sell"
    elif adx_value >= 25 and adx_value < 75 and plus_di > minus_di:
        signal = "Buy"
    else:
        signal = "Neutral"
    
    return signal, f"{trend_strength} ({signal})"
```

**ADX Signal Rules (CORRECTED):**
- **<20**: No clear trend (Neutral)
- **20-25**: Weak trend (Neutral)  
- **25-50**: Moderate trend strength
  - **+DI > -DI**: Buy signal
  - **-DI > +DI**: Neutral (insufficient strength for sell)
- **50-75**: Strong trend
  - **+DI > -DI**: Buy signal
  - **-DI > +DI**: Sell signal (CORRECTED)
- **≥60**: Strong sell threshold when -DI > +DI (CORRECTED)
- **≥75**: Unsustainably strong (may reverse)

**Output Format Examples:**
- "Strong (Buy)" - Strong trend with bullish direction
- "Moderate (Sell)" - Moderate trend with bearish direction  
- "Weak (Neutral)" - Weak trend, no clear signal
- "No Trend (Neutral)" - Range-bound market

---

### **Williams %R - Period 14**

**Calculation**: Momentum oscillator scaled 0 to -100

**Signal Logic Rules:**
```python
def williams_r_signal(wr_value: float, prev_wr_value: float = None) -> Tuple[str, str]:
    if wr_value > -20:
        return "Sell", f"Overbought/Potential Sale ({wr_value:.2f})"
    elif wr_value < -80:
        return "Buy", f"Oversold/Potential Buy ({wr_value:.2f})"
    else:
        return "Neutral", f"Between -20 and -80 ({wr_value:.2f})"
    
    # Crossover logic (requires historical data):
    # if prev_wr_value and prev_wr_value <= -80 and wr_value > -80:
    #     return "Buy", "Cross above -80 from below"
    # if prev_wr_value and prev_wr_value >= -20 and wr_value < -20:
    #     return "Sell", "Cross below -20 from above"
```

**Signal Thresholds:**
- **> -20**: Overbought/Potential Sale
- **< -80**: Oversold/Potential Buy  
- **-20 to -80**: Neutral range
- **Cross above -80**: Buy signal (requires historical data)
- **Cross below -20**: Sell signal (requires historical data)

**Crossover Detection Requirements:**
- **Historical Data Needed**: 2-3 days for reliable crossover detection at -20/-80 levels
- **Implementation**: Store previous Williams %R values for crossover analysis

---

### **CCI (Commodity Channel Index) - Period 14**

**Calculation**: Measures deviation from average price, oscillates around 0

**Signal Logic Rules:**
```python
def cci_signal(cci_value: float) -> Tuple[str, str]:
    if cci_value > 100:
        return "Buy", "Strong upward deviation, bullish bias"
    elif cci_value < -100:
        return "Sell", "Strong downward deviation, bearish bias"  
    elif cci_value > 0:
        return "Buy", "Above zero, bullish bias"
    elif cci_value < 0:
        return "Sell", "Below zero, bearish bias"
    else:
        return "Neutral", "Near zero"
    
    # Additional context:
    # if cci_value > 100: add "Overbought condition" 
    # if cci_value < -100: add "Oversold condition"
```

**Signal Thresholds:**
- **>100**: Strong Buy signal, but often overbought
- **0 to 100**: Bullish bias (Buy)
- **-100 to 0**: Bearish bias (Sell)  
- **<-100**: Strong Sell signal, but often oversold
- **±100**: Traditional overbought/oversold levels

---

### **ATR (Average True Range) - Period 14**

**Calculation**: Moving average of True Range over 14 periods

**Signal Logic (Volatility Measure Only):**
```python
def atr_signal(atr_value: float, historical_avg: float = None) -> Tuple[str, str]:
    # ATR doesn't provide Buy/Sell signals, only volatility measurement
    if historical_avg:
        if atr_value > historical_avg * 1.5:
            return "-", "High volatility, increasing risk"
        elif atr_value < historical_avg * 0.5:  
            return "-", "Low volatility, decreasing risk"
        else:
            return "-", "Normal volatility range"
    else:
        return "-", f"Volatility measure: {atr_value:.2f}"
```

**ATR Usage Notes:**
- **No Buy/Sell Signals**: ATR measures volatility, not direction
- **High ATR**: Increased volatility, higher risk/reward potential
- **Low ATR**: Decreased volatility, consolidation periods
- **Context**: Used for stop-loss levels and position sizing

---

### **Ultimate Oscillator - Periods 7,14,28**

**Calculation**: Weighted average of three oscillators, scaled 0-100

**Signal Logic Rules:**
```python
def ultimate_oscillator_signal(uo_value: float) -> Tuple[str, str]:
    if uo_value > 70:
        return "Sell", "Overbought, potential sell signal"
    elif uo_value < 30:
        return "Buy", "Oversold, potential buy signal"  
    elif uo_value > 50:
        return "Buy", "Above midpoint, bullish bias"
    elif uo_value < 50:
        return "Sell", "Below midpoint, bearish bias"
    else:
        return "Neutral", "At midpoint"
    
    # Divergence logic (requires price data):
    # if bullish_divergence: return "Buy", "Bullish divergence detected"
    # if bearish_divergence: return "Sell", "Bearish divergence detected"
```

**Signal Thresholds:**
- **>70**: Overbought (Sell)
- **50-70**: Bullish bias (Buy)  
- **30-50**: Bearish bias (Sell)
- **<30**: Oversold (Buy)
- **Crossovers**: Cross above 30 (Buy), cross below 70 (Sell)

---

### **ROC (Rate of Change) - Period 12-14**

**Calculation**: Percentage change in price over specified period

**Signal Logic Rules:**
```python
def roc_signal(roc_value: float) -> Tuple[str, str]:
    if roc_value > 0:
        return "Buy", "Price increasing, bullish momentum"
    elif roc_value < 0:
        return "Sell", "Price decreasing, bearish momentum"
    else:
        return "Neutral", "No price change"
    
    # Enhanced logic with thresholds:
    # if roc_value > 5: return "Strong Buy", "Strong positive momentum"
    # if roc_value < -5: return "Strong Sell", "Strong negative momentum"
```

**Signal Rules:**
- **ROC > 0**: Price increasing (Buy)
- **ROC < 0**: Price decreasing (Sell)  
- **ROC ≈ 0**: No momentum (Neutral)
- **Enhanced**: Large positive/negative values indicate strong momentum

---

### **Bull/Bear Power (Elder-ray System) - Period 13**

**Calculation**: Bull Power = High - EMA(13), Bear Power = Low - EMA(13)

**Signal Logic Rules:**
```python
def bull_bear_power_signal(bull_power: float, bear_power: float) -> Tuple[str, str]:
    combined_power = bull_power + bear_power  # or use dominant power
    
    if combined_power > 0:
        if bull_power > 0 and bear_power > -abs(bull_power):
            return "Buy", "Bulls stronger, increasing bull power"
        else:
            return "Buy", "Positive value, bulls stronger overall"
    elif combined_power < 0:
        return "Sell", "Negative value, bears stronger"
    else:
        return "Neutral", "Bulls and bears balanced"
    
    # Alternative: Use individual components
    # if bull_power > 0 and bear_power > previous_bear_power:
    #     return "Buy", "Bull power positive and bear power weakening"
```

**Signal Rules:**
- **Positive Combined Value**: Bulls stronger (Buy)
- **Negative Combined Value**: Bears stronger (Sell)
- **≈ 0**: Balanced market (Neutral)
- **Advanced**: Analyze trend changes in individual components

---

## 🔧 IMPLEMENTATION GUIDELINES - UPDATED

### **Data Staleness Handling (CRITICAL FOR INTERMITTENT USAGE)**
```python
def ensure_sufficient_data(ticker: str, required_days: int = 250) -> pd.DataFrame:
    """Ensure sufficient, current data for technical analysis - HANDLES 2+ WEEK GAPS"""
    
    # 1. Check what exists in daily_prices
    existing_data = get_existing_ohlcv(ticker)
    last_date = existing_data['Date'].max() if not existing_data.empty else None
    
    # 2. Determine what we need
    today = datetime.now().date()
    required_start_date = today - timedelta(days=required_days)
    
    # 3. Check for gaps or staleness (CRITICAL for intermittent usage)
    needs_update = (
        existing_data.empty or                                    # No data
        last_date < (today - timedelta(days=5)) or               # Stale (>5 days old)
        len(existing_data) < required_days or                    # Insufficient history
        existing_data['Date'].min() > required_start_date        # Missing early history
    )
    
    # 4. Fetch missing data if needed
    if needs_update:
        logger.info(f"Updating data for {ticker}: last_date={last_date}, required_days={required_days}")
        fetch_and_backfill_data(ticker, required_start_date, today)
    
    # 5. Return validated dataset
    return get_validated_ohlcv(ticker, required_days)
```

### **pandas-ta-classic vs Manual Calculation Strategy**
```python
# Use pandas-ta-classic for standard indicators
def calculate_with_pandas_ta(data: pd.DataFrame) -> Dict:
    """Calculate standard indicators using pandas-ta-classic"""
    import pandas_ta as ta
    
    indicators = {}
    
    # Standard indicators - use pandas-ta-classic
    indicators['rsi_14'] = ta.rsi(data['Close'], length=14)
    indicators['macd'] = ta.macd(data['Close'], fast=12, slow=26, signal=9)
    indicators['stoch'] = ta.stoch(data['High'], data['Low'], data['Close'], k=9, d=6)
    indicators['adx'] = ta.adx(data['High'], data['Low'], data['Close'], length=14)
    indicators['williams_r'] = ta.willr(data['High'], data['Low'], data['Close'], length=14)
    indicators['cci_14'] = ta.cci(data['High'], data['Low'], data['Close'], length=14)
    indicators['ultimate_osc'] = ta.uo(data['High'], data['Low'], data['Close'])
    indicators['roc_12'] = ta.roc(data['Close'], length=12)
    indicators['atr_14'] = ta.atr(data['High'], data['Low'], data['Close'], length=14)
    
    return indicators

# Manual calculations for custom logic
def calculate_manual_indicators(data: pd.DataFrame) -> Dict:
    """Calculate custom indicators manually"""
    
    indicators = {}
    
    # Bull/Bear Power (Elder-ray system)
    ema_13 = data['Close'].ewm(span=13).mean()
    indicators['bull_power'] = data['High'] - ema_13
    indicators['bear_power'] = data['Low'] - ema_13
    
    # Moving averages with custom signal logic
    periods = [5, 9, 10, 20, 21, 50, 100, 200]
    for period in periods:
        indicators[f'sma_{period}'] = data['Close'].rolling(window=period).mean()
        indicators[f'ema_{period}'] = data['Close'].ewm(span=period).mean()
    
    return indicators
```

### **Crossover Detection Implementation**
```python
class CrossoverDetector:
    """Handle crossover detection for Williams %R and MACD"""
    
    def __init__(self):
        self.required_history = {
            'williams_r': 3,  # 2-3 days for Williams %R crossovers
            'macd': 7        # 5-7 days for MACD signal line crossovers
        }
    
    def detect_williams_r_crossover(self, current_wr: float, historical_wr: List[float]) -> Optional[str]:
        """Detect Williams %R crossover signals"""
        if len(historical_wr) < 2:
            return None
            
        prev_wr = historical_wr[-1]
        
        # Cross above -80 from below (Buy signal)
        if prev_wr <= -80 and current_wr > -80:
            return "Buy - Cross above -80 from below"
            
        # Cross below -20 from above (Sell signal)  
        if prev_wr >= -20 and current_wr < -20:
            return "Sell - Cross below -20 from above"
            
        return None
    
    def detect_macd_crossover(self, current_macd: float, current_signal: float, 
                             historical_macd: List[float], historical_signal: List[float]) -> Optional[str]:
        """Detect MACD signal line crossover"""
        if len(historical_macd) < 2 or len(historical_signal) < 2:
            return None
            
        prev_macd = historical_macd[-1]
        prev_signal = historical_signal[-1]
        
        # Bullish crossover: MACD crosses above signal line
        if prev_macd <= prev_signal and current_macd > current_signal:
            return "Buy - MACD crosses above signal line"
            
        # Bearish crossover: MACD crosses below signal line
        if prev_macd >= prev_signal and current_macd < current_signal:
            return "Sell - MACD crosses below signal line"
            
        return None
```

---

## 📊 TESTING AND VALIDATION - CORRECTED

### **Corrected Signal Logic Testing**
```python
def test_rsi_signal_logic_corrected():
    """Test RSI signal logic against CORRECTED specifications"""
    test_cases = [
        (85.0, "Strong Sell", "Extremely overbought"),
        (75.0, "Sell", "Overbought, potential selling opportunity"),
        (50.0, "Neutral", "Within neutral range"),  # CORRECTED: now neutral
        (30.0, "Buy", "Oversold, potential buying opportunity"),
        (15.0, "Strong Buy", "Extremely oversold")
    ]
    
    for rsi_value, expected_signal, expected_context in test_cases:
        signal, comment = rsi_signal(rsi_value)
        assert signal == expected_signal, f"RSI {rsi_value}: expected {expected_signal}, got {signal}"
        assert expected_context.lower() in comment.lower(), f"RSI {rsi_value}: comment mismatch"

def test_moving_average_neutral_zone_corrected():
    """Test CORRECTED ±0.025% neutral zone for moving averages"""
    processor = MovingAverageSignalProcessor()
    
    # Test cases within and outside CORRECTED neutral zone
    test_cases = [
        (100.0, 99.98, "Neutral"),   # 0.02% above MA (within 0.025% neutral zone)
        (100.0, 100.02, "Neutral"),  # 0.02% below MA (within 0.025% neutral zone)
        (100.0, 99.97, "Buy"),       # 0.03% above MA (outside 0.025% neutral zone)
        (100.0, 100.03, "Sell")      # 0.03% below MA (outside 0.025% neutral zone)
    ]
    
    for price, ma_value, expected_signal in test_cases:
        result = processor._generate_ma_signal(price, ma_value)
        assert result['signal'] == expected_signal, f"MA signal test failed: price={price}, ma={ma_value}"

def test_adx_signal_logic_corrected():
    """Test CORRECTED ADX signal logic"""
    test_cases = [
        (15.0, 25.0, 30.0, "Neutral", "No Trend (Neutral)"),          # Below 20
        (23.0, 25.0, 30.0, "Neutral", "Weak (Neutral)"),              # 20-25 range
        (40.0, 35.0, 25.0, "Buy", "Moderate (Buy)"),                  # 25-50, +DI > -DI
        (55.0, 20.0, 30.0, "Sell", "Strong (Sell)"),                  # 50-75, -DI > +DI (CORRECTED)
        (65.0, 15.0, 35.0, "Strong Sell", "Strong (Strong Sell)")     # ≥60, -DI > +DI (CORRECTED)
    ]
    
    for adx, plus_di, minus_di, expected_signal, expected_comment in test_cases:
        signal, comment = adx_signal(adx, plus_di, minus_di)
        assert signal == expected_signal, f"ADX signal test failed: ADX={adx}, +DI={plus_di}, -DI={minus_di}"
        assert expected_comment in comment, f"ADX comment test failed: expected '{expected_comment}' in '{comment}'"
```

### **Reference Value Validation**
```python
# Test against known reference values (e.g., NVDA on specific date)
REFERENCE_VALUES = {
    'NVDA_2025_09_25': {
        'rsi_14': 52.37,
        'macd_12_26': -0.04,
        'stoch_k': 58.61,
        'adx_14': 24.08,
        # ... etc for all indicators
    }
}

def validate_against_reference(ticker: str, date: str, calculated_values: Dict):
    """Validate calculated values against known reference values"""
    reference = REFERENCE_VALUES.get(f"{ticker}_{date}")
    if not reference:
        return True  # No reference available
        
    for indicator, expected_value in reference.items():
        calculated_value = calculated_values.get(indicator)
        if calculated_value:
            # Allow small tolerance for floating point differences
            tolerance = abs(expected_value * 0.01)  # 1% tolerance
            assert abs(calculated_value - expected_value) <= tolerance, \
                f"{indicator}: expected {expected_value}, got {calculated_value}"
```

---

## 📚 REFERENCE SOURCES - UPDATED

### **Signal Logic References**
- **User-Defined Specifications**: Custom thresholds and rules (UPDATED with corrections)
- **RSI Neutral Zone**: 35-70 range (CORRECTED from 50+ bias)
- **Moving Average Threshold**: ±0.025% neutral zone (CORRECTED from ±0.25%)
- **ADX Logic**: Proper -DI > +DI comparison for sell signals (CORRECTED)
- **Crossover Requirements**: 2-3 days Williams %R, 5-7 days MACD (SPECIFIED)

### **Implementation Notes**
- **Signal Precedence**: Most extreme condition takes priority (Strong Buy/Sell over Buy/Sell)
- **Crossover Detection**: Requires historical data, implement with specified timeframes
- **Error Handling**: All calculations must handle missing data and edge cases gracefully
- **Performance**: Cache calculations and implement batch processing for multi-ticker analysis
- **Data Staleness**: Robust handling for intermittent usage patterns (2+ week gaps)

---

*This signal logic specification provides the definitive CORRECTED implementation guide for all technical indicators, ensuring consistent and accurate signal generation across the entire Technical Analysis Suite with proper neutral zones, thresholds, and logic.*