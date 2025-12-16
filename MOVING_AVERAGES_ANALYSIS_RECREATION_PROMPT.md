# MOVING AVERAGES ANALYSIS - SUBSECTION RECREATION PROMPT

## OVERVIEW

The "Moving Averages Analysis" subsection displays a comprehensive 8-period moving average analysis (SMA and EMA) with bidirectional percentage calculations and Buy/Sell/Neutral signals.

**Current Location in Dashboard**: Technical Analysis Dashboard (streamlit_app.py line 1521)  
**Primary Files**: 
- `src/calculations/technical.py` - Calculation logic
- `streamlit_app.py` - UI display and orchestration

---

## SYSTEM ARCHITECTURE

### Data Flow

```
User enters ticker + clicks "Analyze"
    ↓
streamlit_app.py calls: technical_calculator.calculate_comprehensive_analysis(ticker, save_to_db=...)
    ↓
technical.py: calculate_comprehensive_analysis() orchestrates all components
    ↓
technical.py: _calculate_moving_averages(ticker, save_to_db) [CORE SUBSECTION]
    ↓
Returns: { ticker, current_price, calculation_date, periods: {MA5, MA9, MA10, ..., MA200} }
    ↓
streamlit_app.py: display_moving_averages_table(ma_data) [DISPLAY SUBSECTION]
    ↓
Renders: Professional table with styling in Streamlit
```

---

## PART 1: DATA CALCULATION

### Method Location
**File**: `src/calculations/technical.py`  
**Method**: `_calculate_moving_averages(self, ticker: str, save_to_db: bool = True) -> Dict`  
**Lines**: 1176-1275 (current implementation)

### Method Signature
```python
def _calculate_moving_averages(self, ticker: str, save_to_db: bool = True) -> Dict:
    """
    Calculate comprehensive moving averages analysis for all 8 periods
    
    Implements PRD specifications:
    - Periods: 5, 9, 10, 20, 21, 50, 100, 200
    - Both SMA and EMA for each period
    - Bidirectional percentages: MA/P0 and P0/MA
    - Signals: Buy/Sell/Neutral (±0.025% threshold)
    
    Args:
        ticker: Stock ticker symbol
        save_to_db: Whether to save data to database
        
    Returns:
        Dictionary with comprehensive moving averages data for 8x8 table
    """
```

### Input Requirements
- **ticker**: String (e.g., "NVDA", "AAPL")
- **save_to_db**: Boolean flag (usually determined by bucket membership or user selection)

### Data Retrieval Steps (IN ORDER)

1. **Import pandas-ta-classic**
   - Try to import: `import pandas_ta_classic as ta`
   - Return error dict if import fails (error key = True, message = "pandas-ta-classic library required...")

2. **Fetch OHLCV Data**
   - Call: `self._get_sufficient_ohlcv_data(ticker, periods_needed=200, save_to_db=save_to_db)`
   - This method handles:
     * Database query first (primary source)
     * yfinance fallback if database unavailable
     * Returns pandas DataFrame with columns: Open, High, Low, Close, Volume, AdjClose
   - **Validation**: Check `if df is None or len(df) < 200`
     * If fails: Return error dict with message about insufficient data

3. **Get Current Price**
   - Call: `self.performance_calculator.get_current_price(ticker)`
   - This uses yfinance with session caching for real-time price
   - **Fallback**: If returns None, use `df['Close'].iloc[-1]` (last database close)
   - **Logging**: If using fallback, log warning about using database close

4. **Extract Current Date**
   - Get from DataFrame: `current_date = df.index[-1]`
   - This is the last date in the OHLCV data

### Calculation Steps (IN ORDER)

5. **Initialize Output Dictionary**
   ```python
   ma_data = {
       'ticker': ticker,
       'current_price': current_price,
       'calculation_date': current_date.strftime('%Y-%m-%d'),  # Format: YYYY-MM-DD
       'timestamp': current_date.isoformat(),                   # ISO format for DB storage
       'error': False,
       'periods': {}  # Will be populated below
   }
   ```

6. **For Each Period [5, 9, 10, 20, 21, 50, 100, 200]** (IN THIS EXACT ORDER)

   a. **Validate Sufficient Data**
      ```python
      if len(df) < period:
          logger.warning(f"Skipping MA{period} - insufficient data")
          continue
      ```

   b. **Calculate SMA and EMA**
      ```python
      sma_series = ta.sma(df['Close'], length=period)
      ema_series = ta.ema(df['Close'], length=period)
      ```
      - Extract latest values:
        ```python
        sma_value = sma_series.iloc[-1]
        ema_value = ema_series.iloc[-1]
        ```

   c. **Calculate Bidirectional Percentages**
      
      **For SMA:**
      ```python
      sma_vs_price = ((sma_value - current_price) / current_price) * 100   # MA/P0 - how much MA differs from price
      price_vs_sma = ((current_price - sma_value) / sma_value) * 100       # P0/MA - how much price differs from MA
      ```
      
      **For EMA:**
      ```python
      ema_vs_price = ((ema_value - current_price) / current_price) * 100   # MA/P0
      price_vs_ema = ((current_price - ema_value) / ema_value) * 100       # P0/MA
      ```

   d. **Generate Signals**
      ```python
      sma_signal = self._generate_ma_signal(current_price, sma_value)
      ema_signal = self._generate_ma_signal(current_price, ema_value)
      ```

   e. **Store Period Data**
      ```python
      ma_data['periods'][f'MA{period}'] = {
          'sma': {
              'value': sma_value,
              'ma_vs_price': sma_vs_price,    # SMA/P0 (negative if price above)
              'price_vs_ma': price_vs_sma,    # P0/SMA (positive if price above)
              'signal': sma_signal
          },
          'ema': {
              'value': ema_value,
              'ma_vs_price': ema_vs_price,    # EMA/P0 (negative if price above)
              'price_vs_ma': price_vs_ema,    # P0/EMA (positive if price above)
              'signal': ema_signal
          }
      }
      ```

### Error Handling
- Wrap entire calculation in `try-except`
- Log any exceptions
- Return error dict: `{'error': True, 'message': f'Moving averages calculation failed: {str(e)}'}`

### Return Structure
```python
{
    'ticker': 'NVDA',
    'current_price': 182.45,
    'calculation_date': '2025-10-28',
    'timestamp': '2025-10-28T16:00:00.123456',
    'error': False,
    'periods': {
        'MA5': {
            'sma': {
                'value': 182.34,
                'ma_vs_price': -0.06,
                'price_vs_ma': 0.06,
                'signal': {'signal': 'Neutral', 'strength': 'Weak', 'description': '...'}
            },
            'ema': { similar structure }
        },
        'MA9': { ... },
        'MA10': { ... },
        'MA20': { ... },
        'MA21': { ... },
        'MA50': { ... },
        'MA100': { ... },
        'MA200': { ... }
    }
}
```

---

## PART 2: SIGNAL LOGIC

### Method Location
**File**: `src/calculations/technical.py`  
**Method**: `_generate_ma_signal(self, current_price: float, ma_value: float) -> Dict`  
**Lines**: 449-457 (current implementation)

### Threshold Rules
**From SIGNAL_THRESHOLDS dictionary** (line 70):
```python
'moving_average': {
    'neutral_threshold': 0.025  # ±0.025% neutral zone
}
```

### Signal Logic
```python
def _generate_ma_signal(self, current_price: float, ma_value: float) -> Dict:
    """Generate moving average signal using corrected logic (±0.025% neutral zone)"""
    percentage_diff = ((current_price - ma_value) / ma_value) * 100
    
    if percentage_diff >= 0.025:
        return {
            'signal': 'Buy',
            'strength': 'Moderate',
            'description': f'Price {percentage_diff:+.3f}% above MA'
        }
    elif percentage_diff <= -0.025:
        return {
            'signal': 'Sell',
            'strength': 'Moderate',
            'description': f'Price {percentage_diff:+.3f}% below MA'
        }
    else:
        return {
            'signal': 'Neutral',
            'strength': 'Weak',
            'description': f'Price {percentage_diff:+.3f}% near MA'
        }
```

### Signal Conditions
| Condition | Signal | Strength | Description |
|-----------|--------|----------|-------------|
| price_diff >= +0.025% | Buy | Moderate | Price above MA by threshold |
| price_diff <= -0.025% | Sell | Moderate | Price below MA by threshold |
| -0.025% < price_diff < +0.025% | Neutral | Weak | Price near MA |

### Return Structure
```python
{
    'signal': 'Buy' | 'Sell' | 'Neutral',
    'strength': 'Moderate' | 'Weak',
    'description': 'Human-readable description with percentage'
}
```

---

## PART 3: UI DISPLAY

### Method Location
**File**: `streamlit_app.py`  
**Method**: `display_moving_averages_table(ma_data: Dict) -> None`  
**Lines**: 1169-1264 (current implementation)

### Input Parameter
```python
ma_data  # Dict returned from _calculate_moving_averages()
```

### Validation
- Check: `if not ma_data or ma_data.get('error')`
- If error: Display `st.error()` with message and return

### Table Structure
**Columns (in order):**
1. Period (MA5, MA9, MA10, ..., MA200)
2. SMA Value ($X.XX)
3. P0/SMA (% - how much price differs from SMA)
4. SMA/P0 (% - how much SMA differs from price)
5. SMA Signal (Buy/Sell/Neutral - COLOR CODED)
6. SMA Comments (generated text explanation)
7. EMA Value ($X.XX)
8. P0/EMA (% - how much price differs from EMA)
9. EMA/P0 (% - how much EMA differs from price)
10. EMA Signal (Buy/Sell/Neutral - COLOR CODED)
11. EMA Comments (generated text explanation)

### Comment Generation
**Function**: `generate_ma_comment(ticker: str, period: int, ma_type: str, current_price: float, ma_value: float, price_vs_ma: float) -> str`

**Logic**:
```python
def generate_ma_comment(ticker, period, ma_type, current_price, ma_value, price_vs_ma):
    # Use price_vs_ma percentage to generate descriptive comment
    if abs(price_vs_ma) <= 0.025:
        return f"Price near {ma_type}{period}"
    elif price_vs_ma > 0:
        return f"Price {price_vs_ma:.2f}% above {ma_type}{period}"
    else:
        return f"Price {abs(price_vs_ma):.2f}% below {ma_type}{period}"
```

### Styling
**Signal Color Mapping** (using Bootstrap color scheme):
- **Buy Signal**: `background-color: #d4edda; color: #155724; font-weight: bold` (Green)
- **Sell Signal**: `background-color: #f8d7da; color: #721c24; font-weight: bold` (Red)
- **Neutral Signal**: `background-color: #f8f9fa; color: #6c757d; font-weight: bold` (Gray)

### Current Price Display
```python
st.caption(f"Current Price: ${current_price:.2f} ({calc_date})")
```

### DataFrame Configuration
```python
st.dataframe(
    styled_df,
    hide_index=True,
    use_container_width=True
)
```

### Percentage Format
- All percentages displayed as: `±X.X%` (one decimal place)
- Examples: `+0.1%`, `-0.5%`, `+2.3%`

---

## DEPENDENCIES & INTEGRATIONS

### Within technical.py
- `_get_sufficient_ohlcv_data()` - Fetches OHLCV data from DB/yfinance
- `self.performance_calculator.get_current_price()` - Gets live price
- `_generate_ma_signal()` - Generates Buy/Sell/Neutral signals
- `SIGNAL_THRESHOLDS` dictionary - Contains ±0.025% threshold
- Logging via `logger` object

### External Libraries
- `pandas_ta_classic` - For SMA and EMA calculations
- `pandas` - DataFrame operations
- `numpy` - Numerical operations

### Database
- Reads from: `daily_prices` table (OHLCV data)
- Reads from: `technical_indicators_daily` table (if needed for context)
- Writes: None (this subsection is read-only, calculation-based)

### Streamlit Components
- `st.caption()` - For current price display
- `st.dataframe()` - For table rendering
- `st.error()` - For error messages
- DataFrame styling via `.style` API

---

## TESTING CHECKLIST

### Data Calculation (_calculate_moving_averages)
- [ ] With sufficient data (200+ periods): Returns valid dict with all 8 periods
- [ ] With insufficient data (<200 periods): Returns error dict with appropriate message
- [ ] Current price uses yfinance correctly
- [ ] Current price falls back to database close when yfinance unavailable
- [ ] All 8 periods calculated (5, 9, 10, 20, 21, 50, 100, 200)
- [ ] Both SMA and EMA calculated for each period
- [ ] Percentages calculated correctly (bidirectional)
- [ ] Signals generated with correct thresholds

### Signal Logic (_generate_ma_signal)
- [ ] Buy signal when price >= 0.025% above MA
- [ ] Sell signal when price <= -0.025% below MA
- [ ] Neutral signal when price within ±0.025% of MA
- [ ] Descriptions formatted correctly with percentages

### Display (display_moving_averages_table)
- [ ] Table renders with all 8 periods
- [ ] SMA and EMA columns display correctly
- [ ] Percentages formatted as ±X.X%
- [ ] Signals color-coded correctly
- [ ] Comments generated and displayed
- [ ] Current price shown in caption
- [ ] No layout overflow or rendering issues

---

## KNOWN ISSUES & EDGE CASES

1. **Insufficient Data**: If ticker has <200 periods of history
   - Action: Return error dict, do not attempt partial calculation

2. **yfinance Unavailable**: If API is down or rate-limited
   - Action: Use last database close price with warning log

3. **NULL Values**: If SMA/EMA calculation returns NaN
   - Action: Log warning, skip that period, continue with others

4. **Trading Day Gaps**: If no data available for certain dates
   - Action: `_get_sufficient_ohlcv_data()` handles this; uses trading day logic

5. **Performance**: For very old tickers with 50+ years of data
   - Action: Ensure 200-period limit is respected, not fetching entire history

---

## RECREATION INSTRUCTIONS

### Step 1: Create the Calculation Method
Create `_calculate_moving_averages()` in `technical.py`:
- Follow "PART 1: DATA CALCULATION" exactly
- Use the method signature provided
- Return the exact output structure specified

### Step 2: Verify Signal Method Exists
Ensure `_generate_ma_signal()` exists in `technical.py`:
- Follow "PART 2: SIGNAL LOGIC" exactly
- Verify ±0.025% threshold is hardcoded

### Step 3: Create/Update Display Function
Create or update `display_moving_averages_table()` in `streamlit_app.py`:
- Follow "PART 3: UI DISPLAY" exactly
- Implement color styling as specified
- Ensure all columns render correctly

### Step 4: Wire into Orchestrator
Update `calculate_comprehensive_analysis()` in `technical.py`:
- Add line: `'moving_averages': self._calculate_moving_averages(ticker, save_to_db=save_to_db)`
- Ensure it's called for every analysis request

### Step 5: Wire into Dashboard
Update Technical Analysis Dashboard in `streamlit_app.py`:
- Add section after line ~1521
- Call: `display_moving_averages_table(data['moving_averages'])`

### Step 6: Test
- Run with NVDA ticker
- Verify all 8 periods display
- Verify signals and colors render correctly
- Verify percentages format correctly

---

## IMPORTANT NOTES

1. **Do NOT make assumptions**: If uncertain about any detail, ask first
2. **Exact thresholds**: Use ±0.025% (NOT 0.025, NOT 2.5%, NOT 1%)
3. **Exact periods**: Use [5, 9, 10, 20, 21, 50, 100, 200] (NOT [5, 10, 20, 50, 200])
4. **Exact columns**: Follow the column order and naming exactly as specified
5. **Exact styling**: Use the exact Bootstrap color codes provided (no alternatives)
6. **Database-first**: Always fetch OHLCV from database first, yfinance second
7. **Error handling**: Always return error dicts with 'error': True and 'message' keys
8. **Logging**: Use logger.info/warning/error consistently throughout

