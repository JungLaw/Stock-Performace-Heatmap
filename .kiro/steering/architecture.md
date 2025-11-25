# ARCHITECTURAL PRINCIPLES
Stock Performance Heatmap Dashboard

## Core Design Philosophy

**Principle**: Build once, use everywhere. All dashboards share common data management, calculation patterns, and storage architecture.

**Anti-Pattern**: Creating dashboard-specific implementations of data fetching, gap detection, backfill, or storage logic.

---

## 1. CENTRALIZED SIGNAL CONFIGURATION

### **Requirement**
All signal thresholds and indicator parameters must be defined in a single, centralized location.

### **Implementation**
- **Location**: `src/config/settings.py`
- **Structure**: `SIGNAL_THRESHOLDS` dictionary

### **Pattern**
```python
# src/config/settings.py
SIGNAL_THRESHOLDS = {
    'RSI': {
        'strong_buy': 20,
        'buy': 35,
        'neutral_low': 35,
        'neutral_high': 70,
        'sell': 70,
        'strong_sell': 80
    },
    'STOCH': {
        'oversold': 20,
        'overbought': 80
    },
    # ... all other indicators
}

# Usage in signal methods
def _generate_rsi_signal(self, rsi_value: float) -> Dict:
    thresholds = SIGNAL_THRESHOLDS['RSI']
    if rsi_value <= thresholds['strong_buy']:
        return {'signal': 'Strong Buy', ...}
    elif rsi_value <= thresholds['buy']:
        return {'signal': 'Buy', ...}
    # etc.
```

### **Applies To**
- Performance Heatmap signals
- Technical Analysis dashboard
- Rolling Heatmap (all 3 timeframes)
- Any future dashboard with signal logic

### **Rationale**
- Single source of truth prevents duplication
- Changes propagate automatically to all dashboards
- Comments and code stay synchronized
- Easier testing and validation

### **Violation Examples**
❌ Hardcoding thresholds in methods: `if rsi_value >= 70:`
❌ Duplicating thresholds in comments: `# RSI: >70 = Sell`
❌ Dashboard-specific threshold configs

---

## 2. UNIFIED DATA MANAGEMENT FLOW

### **Requirement**
All dashboards must use the same data pipeline for fetching, validating, and processing OHLCV data.

### **Standard Data Flow**
```
1. Request data for ticker + date range
2. Check database for existing data
3. Detect gaps (missing dates, holidays, non-trading days)
4. Auto-fill gaps from yfinance if needed
5. Validate data completeness
6. Return clean, contiguous OHLCV DataFrame
```

### **Core Methods (Already Implemented)**

#### **Gap Detection**
```python
# src/calculations/technical.py
def _detect_data_gaps(self, ticker: str, start_date: date, end_date: date) -> List[date]:
    """
    Identifies missing trading days in database
    - Accounts for weekends and holidays
    - Returns list of dates that need fetching
    """
```

#### **Auto-Fill**
```python
def _get_sufficient_ohlcv_data(self, ticker: str, periods_needed: int) -> pd.DataFrame:
    """
    Ensures sufficient OHLCV data exists for calculations
    - Checks database first
    - Auto-fetches missing data from yfinance
    - Handles lookback periods (e.g., 200-day EMA needs 200+ days)
    - Returns complete DataFrame ready for calculations
    """
```

#### **Trading Day Windows**
```python
def _get_trading_days(self, start_date: date, end_date: date) -> List[date]:
    """
    Returns list of valid trading days in date range
    - Excludes weekends
    - Excludes market holidays
    - Handles partial trading days
    """
```

### **Pattern Usage**
```python
# CORRECT: Use existing data management flow
def calculate_rolling_heatmap(self, ticker: str, days: int):
    # Step 1: Get sufficient OHLCV data (handles gaps automatically)
    ohlcv_df = self._get_sufficient_ohlcv_data(ticker, periods_needed=200)
    
    # Step 2: Calculate indicators from clean data
    indicators = self._calculate_technical_indicators(ohlcv_df)
    
    # Step 3: Generate signals
    signals = self._generate_signals(indicators)
    
    return signals

# WRONG: Creating parallel data fetching
def calculate_rolling_heatmap(self, ticker: str, days: int):
    # ❌ Don't do this - bypasses gap detection and validation
    raw_data = yf.download(ticker, period=f"{days}d")
    indicators = self._calculate_indicators(raw_data)
```

### **Applies To**
- Performance calculations
- Technical indicator calculations
- Rolling heatmap data generation
- Any feature requiring historical price data

### **Rationale**
- Consistent handling of missing data across all features
- Automatic gap detection prevents calculation errors
- Centralized holiday/weekend logic
- Database caching improves performance

### **Violation Examples**
❌ Direct yfinance calls without gap detection
❌ Custom date range logic per dashboard
❌ Skipping data validation steps
❌ Creating dashboard-specific data fetchers

---

## 3. STANDARD BACKFILL ARCHITECTURE

### **Requirement**
All historical data calculations must use real-time calculation pattern, not database lookup pattern.

### **Two Calculation Patterns**

#### **Pattern A: Real-Time Calculation (Use This)**
```python
def calculate_indicators_for_range(self, ticker: str, start_date: date, end_date: date):
    """
    Calculate indicators in real-time from OHLCV data
    
    Flow:
    1. Fetch OHLCV data (with lookback buffer)
    2. Calculate ALL indicators using pandas-ta
    3. Return calculated values for requested date range
    4. Optionally save to database
    """
    # Get OHLCV with sufficient lookback
    ohlcv_df = self._get_sufficient_ohlcv_data(ticker, periods_needed=200)
    
    # Calculate indicators (pandas-ta handles rolling windows)
    indicators_df = self._calculate_all_indicators(ohlcv_df)
    
    # Filter to requested date range
    result = indicators_df.loc[start_date:end_date]
    
    return result
```

**When to use:**
- Rolling heatmap (custom indicator parameters)
- Technical analysis with non-standard periods
- Any calculation requiring flexibility

**Why it works:**
- pandas-ta handles rolling windows correctly
- Full OHLCV context available for calculations
- No database schema limitations

#### **Pattern B: Database Lookup (Limited Use)**
```python
def get_stored_indicators(self, ticker: str, date: date):
    """
    Retrieve pre-calculated indicators from database
    
    Use ONLY when:
    - Indicators use standard parameters (RSI(14), not RSI(10))
    - Indicators are already calculated and stored
    - No custom timeframes needed
    """
    query = "SELECT * FROM technical_indicators_daily WHERE ticker = ? AND date = ?"
    return pd.read_sql(query, self.conn, params=[ticker, date])
```

**When to use:**
- Performance heatmap (standard indicators only)
- Quick lookups of previously calculated data

**Limitations:**
- Only works for standard indicator parameters
- Requires indicators to be pre-calculated
- Can't handle custom timeframes

### **Backfill Implementation**

**CORRECT Approach:**
```python
def backfill_indicators(self, ticker: str, days: int):
    """
    Fill missing historical indicator data
    
    Uses Pattern A (real-time calculation)
    """
    # Calculate for entire range at once
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    # Use real-time calculation pattern
    indicators = self.calculate_indicators_for_range(ticker, start_date, end_date)
    
    # Save to database
    self._save_indicators_to_db(indicators)
```

**WRONG Approach:**
```python
def backfill_indicators(self, ticker: str, days: int):
    """
    ❌ DON'T DO THIS - Broken architecture
    """
    for single_date in date_range:
        # ❌ Trying to calculate from single-day slice
        ohlcv_slice = ohlcv_df[ohlcv_df['date'] == single_date]
        
        # ❌ Can't calculate rolling indicators from single day
        indicators = self._calculate_indicators(ohlcv_slice)
```

### **Applies To**
- Rolling heatmap backfill
- Technical indicator historical data
- Any feature requiring historical calculations

### **Rationale**
- Real-time calculation handles custom parameters
- Avoids database schema limitations
- Consistent with pandas-ta calculation requirements
- Prevents architectural mismatches

### **Violation Examples**
❌ Calculating indicators from single-day data slices
❌ Assuming database has all needed indicator combinations
❌ Creating separate backfill logic per dashboard
❌ Using database lookup for custom indicator parameters

---

## 4. SHARED DATA STORAGE

### **Requirement**
Common indicators and data must be stored once and accessible by all dashboards.

### **Database Schema**

#### **`stock_prices` Table**
```sql
CREATE TABLE stock_prices (
    ticker TEXT,
    date DATE,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    adj_close REAL,
    volume INTEGER,
    PRIMARY KEY (ticker, date)
);
```

**Purpose**: OHLCV data for all tickers
**Used By**: All dashboards
**Update Pattern**: Auto-fill via `_get_sufficient_ohlcv_data()`

#### **`technical_indicators_daily` Table**
```sql
CREATE TABLE technical_indicators_daily (
    ticker TEXT,
    date DATE,
    -- Standard indicators only (RSI(14), SMA(20), etc.)
    rsi_14 REAL,
    sma_20 REAL,
    ema_21 REAL,
    macd REAL,
    -- ... other standard indicators
    PRIMARY KEY (ticker, date)
);
```

**Purpose**: Pre-calculated standard indicators
**Used By**: Performance heatmap, quick lookups
**Update Pattern**: Calculated and saved via `calculate_technical_indicators()`

**Limitations**: 
- Only stores standard parameters
- Custom parameters (RSI(10), SMA(50)) calculated in real-time

#### **`performance_metrics` Table**
```sql
CREATE TABLE performance_metrics (
    ticker TEXT,
    date DATE,
    period TEXT,  -- '1D', '1W', '1M', etc.
    performance REAL,
    baseline_price REAL,
    current_price REAL,
    PRIMARY KEY (ticker, date, period)
);
```

**Purpose**: Performance calculations for heatmap
**Used By**: Performance heatmap dashboard
**Update Pattern**: Calculated via `PerformanceCalculator`

### **Storage Patterns**

#### **When to Store in Database**
✅ Standard indicators (RSI(14), SMA(20), EMA(21))
✅ OHLCV data (used by all features)
✅ Performance metrics (reused across periods)
✅ Data that's expensive to recalculate

#### **When NOT to Store**
❌ Custom indicator parameters (RSI(10), SMA(50))
❌ Temporary calculations
❌ Dashboard-specific transformations
❌ Data that changes frequently

### **Access Pattern**
```python
# CORRECT: Check database first, calculate if missing
def get_indicator_data(self, ticker: str, indicator: str, period: int):
    # Try database for standard parameters
    if self._is_standard_parameter(indicator, period):
        db_data = self._get_from_database(ticker, indicator)
        if db_data is not None:
            return db_data
    
    # Calculate in real-time for custom parameters
    return self._calculate_indicator(ticker, indicator, period)

# WRONG: Always calculate, ignore database
def get_indicator_data(self, ticker: str, indicator: str, period: int):
    # ❌ Wastes time recalculating stored data
    return self._calculate_indicator(ticker, indicator, period)
```

### **Applies To**
- All dashboards accessing OHLCV data
- Technical indicator storage and retrieval
- Performance metric caching

### **Rationale**
- Reduces redundant calculations
- Improves performance across dashboards
- Consistent data across features
- Efficient use of database storage

### **Violation Examples**
❌ Creating dashboard-specific data tables
❌ Storing duplicate OHLCV data
❌ Bypassing database checks
❌ Storing all indicator combinations (storage explosion)

---

## IMPLEMENTATION CHECKLIST

When implementing any new dashboard or feature:

### **Data Management**
- [ ] Uses `_get_sufficient_ohlcv_data()` for data fetching
- [ ] Uses `_detect_data_gaps()` for gap detection
- [ ] Uses `_get_trading_days()` for date range validation
- [ ] No direct yfinance calls without gap detection

### **Signal Logic**
- [ ] All thresholds defined in `SIGNAL_THRESHOLDS` config
- [ ] Signal methods reference config, not hardcoded values
- [ ] No threshold duplication in comments or code

### **Backfill Architecture**
- [ ] Uses real-time calculation pattern (Pattern A)
- [ ] Calculates from full OHLCV DataFrame, not single-day slices
- [ ] No database lookup for custom indicator parameters

### **Data Storage**
- [ ] Checks database before calculating
- [ ] Stores only standard indicators in database
- [ ] Uses shared tables (`stock_prices`, `technical_indicators_daily`)
- [ ] No dashboard-specific duplicate storage

### **Code Organization**
- [ ] No redundant implementations of existing functionality
- [ ] Follows existing patterns in codebase
- [ ] Integrates with existing calculators (PerformanceCalculator, TechnicalCalculator)

---

## VIOLATION CONSEQUENCES

**If architectural patterns are violated:**

1. **Immediate**: Code review flags the violation
2. **Short-term**: Technical debt accumulates
3. **Long-term**: 
   - Maintenance nightmare (multiple implementations to update)
   - Inconsistent behavior across dashboards
   - Performance degradation (redundant calculations)
   - Database bloat (duplicate storage)

**Enforcement**: Architectural violations are treated as constraint violations and trigger session termination.

---

## EXAMPLES FROM CODEBASE

### **Good Example: Performance Calculator**
```python
# src/calculations/performance.py
class PerformanceCalculator:
    def calculate_performance(self, ticker: str, period: str):
        # ✅ Uses shared data management
        ohlcv_data = self._get_sufficient_ohlcv_data(ticker, periods_needed=252)
        
        # ✅ Uses gap detection
        gaps = self._detect_data_gaps(ticker, start_date, end_date)
        
        # ✅ Stores in shared table
        self._save_to_database('performance_metrics', data)
```

### **Bad Example: Redundant Implementation**
```python
# ❌ DON'T DO THIS
class RollingHeatmapCalculator:
    def get_data(self, ticker: str):
        # ❌ Custom data fetching (bypasses gap detection)
        data = yf.download(ticker, period="1y")
        
        # ❌ Custom gap handling
        data = data.fillna(method='ffill')
        
        # ❌ Custom storage
        data.to_sql('rolling_heatmap_data', self.conn)
```

---

## QUESTIONS?

If unsure whether an implementation follows architectural patterns:

1. **Ask**: "Does this use existing data management methods?"
2. **Check**: "Am I duplicating functionality that already exists?"
3. **Verify**: "Does this integrate with shared storage?"
4. **Confirm**: "Am I following the real-time calculation pattern?"

**When in doubt, ask before implementing.**
