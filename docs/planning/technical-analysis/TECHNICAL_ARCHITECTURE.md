# Technical Analysis Suite - Technical Architecture
**Project**: Stock Performance Dashboard - Technical Analysis Extension  
**Date**: September 25, 2025  
**Version**: 1.0  
**Status**: Architecture Design Complete

---

## 🏗️ ARCHITECTURE OVERVIEW

### **Integration Strategy**
The Technical Analysis Suite extends the existing Stock Performance Heatmap Dashboard using a **Single Application Extension** approach, preserving all existing functionality while adding comprehensive technical analysis capabilities through new pages and components.

### **Core Design Principles**
1. **Preserve Existing Functionality**: All current heatmap features remain unchanged
2. **Follow Established Patterns**: Use existing `DatabaseIntegrated*` patterns and conventions
3. **Leverage Proven Infrastructure**: Extend existing database, UI components, and data flow
4. **Maintain Performance Standards**: Meet or exceed current system performance requirements
5. **Ensure Professional Quality**: Match existing code quality and user experience standards

---

## 📊 SYSTEM ARCHITECTURE

### **High-Level Component Architecture**
```
Stock Performance Dashboard (Extended)
├── 📈 Performance Heatmaps (Existing - Preserved)
│   ├── Price Analysis (DatabaseIntegratedPerformanceCalculator)
│   ├── Volume Analysis (DatabaseIntegratedVolumeCalculator) 
│   └── Technical Heatmaps (NEW - DatabaseIntegratedTechnicalCalculator)
├── 🎯 Technical Analysis (NEW - Dashboard 1)
│   ├── Moving Averages Analysis
│   ├── Technical Indicators Analysis
│   ├── 52-Week High Analysis
│   ├── Rolling Heatmap (10-day signal history)
│   └── Pivot Points Analysis
└── 📋 Stock Comparison (NEW - Dashboard 2)
    ├── Technical Indicator Selection
    ├── Multi-Stock Heatmap Visualization
    └── Comparative Analysis Tools
```

### **Data Flow Architecture**
```
User Input (Ticker/Selection)
    ↓
Streamlit UI Layer
    ↓
DatabaseIntegratedTechnicalCalculator
    ↓
┌─────────────────┬─────────────────┐
│   Database      │    yfinance     │
│   (Historical)  │   (Current/     │
│                 │   Missing)      │
└─────────────────┴─────────────────┘
    ↓
pandas-ta-classic Calculations
    ↓
Signal Logic Processors
    ↓
┌─────────────────┬─────────────────┐
│  Technical      │   Heatmap       │
│  Tables         │  Visualization  │
│  (Dashboard 1)  │  (Dashboard 2)  │
└─────────────────┴─────────────────┘
    ↓
User Interface Display
```

---

## 🗄️ DATABASE ARCHITECTURE

### **Extended Database Schema**
The technical analysis system extends the existing `stock_data.db` with three new tables:

#### **technical_indicators_daily Table**
```sql
CREATE TABLE technical_indicators_daily (
    ticker TEXT NOT NULL,
    date DATE NOT NULL,
    
    -- Moving Averages
    sma_5 REAL, sma_9 REAL, sma_10 REAL, sma_20 REAL, sma_21 REAL,
    sma_50 REAL, sma_100 REAL, sma_200 REAL,
    ema_5 REAL, ema_9 REAL, ema_10 REAL, ema_20 REAL, ema_21 REAL, 
    ema_50 REAL, ema_100 REAL, ema_200 REAL,
    
    -- Technical Indicators  
    rsi_14 REAL,
    macd_value REAL, macd_signal REAL, macd_histogram REAL,
    stoch_k REAL, stoch_d REAL,
    stochrsi_value REAL,
    adx_value REAL, plus_di REAL, minus_di REAL,
    williams_r REAL,
    cci_14 REAL,
    ultimate_osc REAL,
    roc_12 REAL,
    atr_14 REAL,
    bull_power REAL, bear_power REAL,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (ticker, date)
);

-- Performance indexes
CREATE INDEX idx_technical_ticker_date ON technical_indicators_daily(ticker, date DESC);
CREATE INDEX idx_technical_date ON technical_indicators_daily(date DESC);
```

#### **price_extremes_periods Table**
```sql
CREATE TABLE price_extremes_periods (
    ticker TEXT NOT NULL,
    period TEXT NOT NULL,  -- '52w', '3m', '1m', '2w'
    
    high_price REAL NOT NULL,
    low_price REAL NOT NULL,
    high_date DATE NOT NULL,
    low_date DATE NOT NULL,
    
    -- Calculated levels for 52-week analysis
    level_minus_5pct REAL,   -- High - 5%
    level_minus_10pct REAL,  -- High - 10% 
    level_minus_15pct REAL,  -- High - 15%
    level_minus_20pct REAL,  -- High - 20%
    
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (ticker, period)
);

CREATE INDEX idx_extremes_ticker ON price_extremes_periods(ticker);
```

#### **pivot_points_daily Table**
```sql
CREATE TABLE pivot_points_daily (
    ticker TEXT NOT NULL,
    date DATE NOT NULL,
    pivot_type TEXT NOT NULL,  -- 'classic', 'fibonacci', 'woodys', 'camarilla'
    
    pivot REAL NOT NULL,
    r1 REAL, r2 REAL, r3 REAL,  -- Resistance levels
    s1 REAL, s2 REAL, s3 REAL,  -- Support levels
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (ticker, date, pivot_type)
);

CREATE INDEX idx_pivot_ticker_date ON pivot_points_daily(ticker, date DESC);
```

### **Database Integration Patterns**
Following the proven patterns from existing system:

```python
class DatabaseIntegratedTechnicalCalculator:
    """Follows same patterns as DatabaseIntegratedPerformanceCalculator"""
    
    def __init__(self, db_file: str = \"data/stock_data.db\"):
        self.db_file = db_file
        self.session_cache = {}  # For save_to_db=False scenarios
    
    def _get_historical_indicators_from_db(self, ticker: str, start_date: str) -> pd.DataFrame:
        """Database-first lookup, same pattern as existing system"""
        
    def _fetch_and_calculate_indicators(self, ticker: str, save_to_db: bool = True) -> Dict:
        """yfinance fallback with database save option"""
        
    def _save_indicators_to_database(self, ticker: str, indicators_df: pd.DataFrame):
        """Bulk insert/update technical indicators"""
```

---

## 🧮 CALCULATION ENGINE ARCHITECTURE

### **Core Calculator Structure**
```python
class DatabaseIntegratedTechnicalCalculator:
    """Main technical analysis calculation engine"""
    
    def __init__(self):
        self.db_file = "data/stock_data.db"
        self.session_cache = {}
        
        # Initialize signal processors
        self.signal_processors = {
            'moving_averages': MovingAverageSignalProcessor(),
            'rsi': RSISignalProcessor(),
            'macd': MACDSignalProcessor(),  
            'stochastic': StochasticSignalProcessor(),
            'adx': ADXSignalProcessor(),
            'williams_r': WilliamsRSignalProcessor(),
            'cci': CCISignalProcessor(),
            'ultimate_osc': UltimateOscillatorSignalProcessor(),
            'roc': ROCSignalProcessor(),
            'atr': ATRSignalProcessor(),
            'bull_bear_power': BullBearPowerSignalProcessor()
        }
        
        # Initialize specialized calculators
        self.extremes_calculator = PriceExtremesCalculator(self.db_file)
        self.pivot_calculator = PivotPointsCalculator(self.db_file)
    
    # Main calculation methods
    def calculate_single_stock_analysis(self, ticker: str) -> Dict:
        """Dashboard 1: Complete technical analysis for single stock"""
        
    def calculate_multi_stock_indicator(self, tickers: List[str], indicator: str) -> List[Dict]:
        """Dashboard 2: Single indicator across multiple stocks"""
        
    def get_rolling_heatmap_data(self, ticker: str, days: int = 10) -> pd.DataFrame:
        """Rolling heatmap: 10-day signal history"""
```

### **Signal Processor Architecture**
```python
from abc import ABC, abstractmethod

class SignalProcessor(ABC):
    """Base class for all technical indicator signal processors"""
    
    @abstractmethod
    def calculate_value(self, data: pd.DataFrame, **params) -> float:
        """Calculate the raw indicator value"""
        
    @abstractmethod  
    def generate_signal(self, value: float, **context) -> Dict[str, Any]:
        """Apply signal logic and return structured signal data"""
        
    def process_indicator(self, data: pd.DataFrame, **params) -> Dict[str, Any]:
        """Main processing method - calculate value and generate signal"""
        try:
            value = self.calculate_value(data, **params)
            signal_data = self.generate_signal(value, **params)
            
            return {
                'value': value,
                'signal': signal_data['signal'],
                'strength': signal_data.get('strength', ''),
                'comment': signal_data.get('comment', ''),
                'error': False
            }
        except Exception as e:
            return {
                'error': True,
                'message': str(e),
                'value': None,
                'signal': 'Error'
            }

class RSISignalProcessor(SignalProcessor):
    """RSI-specific signal processor implementation"""
    
    def calculate_value(self, data: pd.DataFrame, period: int = 14) -> float:
        """Calculate RSI using pandas-ta-classic"""
        import pandas_ta as ta
        rsi_series = ta.rsi(data['Close'], length=period)
        return rsi_series.iloc[-1]
    
    def generate_signal(self, rsi_value: float, **context) -> Dict[str, Any]:
        """Apply hierarchical RSI signal logic"""
        if rsi_value >= 80:
            return {
                'signal': 'Strong Sell',
                'strength': 'Extremely Overbought', 
                'comment': f'RSI at {rsi_value:.1f} indicates extremely overbought conditions'
            }
        elif rsi_value >= 70:
            return {
                'signal': 'Sell',
                'strength': 'Overbought',
                'comment': f'RSI at {rsi_value:.1f} shows overbought, potential selling opportunity'
            }
        # ... etc for all RSI thresholds
```

### **pandas-ta-classic Integration**
```python
class TechnicalCalculations:
    """Wrapper for pandas-ta-classic calculations"""
    
    @staticmethod
    def calculate_moving_averages(data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calculate all required moving averages"""
        import pandas_ta as ta
        
        periods = [5, 9, 10, 20, 21, 50, 100, 200]
        results = {}
        
        for period in periods:
            results[f'sma_{period}'] = ta.sma(data['Close'], length=period)
            results[f'ema_{period}'] = ta.ema(data['Close'], length=period)
            
        return results
    
    @staticmethod
    def calculate_all_indicators(data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate all technical indicators"""
        import pandas_ta as ta
        
        indicators = {}
        
        # RSI
        indicators['rsi_14'] = ta.rsi(data['Close'], length=14)
        
        # MACD
        macd_data = ta.macd(data['Close'], fast=12, slow=26, signal=9)
        indicators['macd_value'] = macd_data['MACD_12_26_9']
        indicators['macd_signal'] = macd_data['MACDs_12_26_9'] 
        indicators['macd_histogram'] = macd_data['MACDh_12_26_9']
        
        # Stochastic
        stoch_data = ta.stoch(data['High'], data['Low'], data['Close'], k=9, d=6)
        indicators['stoch_k'] = stoch_data['STOCHk_9_6_3']
        indicators['stoch_d'] = stoch_data['STOCHd_9_6_3']
        
        # StochRSI
        stochrsi_data = ta.stochrsi(data['Close'], length=14)
        indicators['stochrsi_value'] = stochrsi_data['STOCHRSIk_14_14_3_3']
        
        # ADX with Directional Indicators
        adx_data = ta.adx(data['High'], data['Low'], data['Close'], length=14)
        indicators['adx_value'] = adx_data['ADX_14']
        indicators['plus_di'] = adx_data['DMP_14']
        indicators['minus_di'] = adx_data['DMN_14']
        
        # Williams %R
        indicators['williams_r'] = ta.willr(data['High'], data['Low'], data['Close'], length=14)
        
        # CCI
        indicators['cci_14'] = ta.cci(data['High'], data['Low'], data['Close'], length=14)
        
        # Ultimate Oscillator
        indicators['ultimate_osc'] = ta.uo(data['High'], data['Low'], data['Close'])
        
        # Rate of Change
        indicators['roc_12'] = ta.roc(data['Close'], length=12)
        
        # ATR
        indicators['atr_14'] = ta.atr(data['High'], data['Low'], data['Close'], length=14)
        
        # Bull/Bear Power (Elder-ray)
        ema_13 = ta.ema(data['Close'], length=13)
        indicators['bull_power'] = data['High'] - ema_13
        indicators['bear_power'] = data['Low'] - ema_13
        
        return indicators
```

---

## 🎨 UI COMPONENT ARCHITECTURE

### **Streamlit Application Extension**
```python
# streamlit_app.py (Extended)
def main():
    """Extended main function with technical analysis integration"""
    
    # Preserve existing page config and initialization
    st.set_page_config(
        page_title="Stock Performance Dashboard",
        page_icon="📈", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()  # Existing + technical analysis state
    
    # Enhanced navigation with technical analysis
    page = st.sidebar.selectbox("Choose Dashboard:", [
        "📈 Performance Heatmaps",      # Existing system preserved
        "🎯 Technical Analysis",        # NEW: Dashboard 1  
        "📋 Stock Comparison"           # NEW: Dashboard 2
    ])
    
    # Route to appropriate dashboard
    if page == "📈 Performance Heatmaps":
        show_performance_heatmaps()     # Existing function unchanged
    elif page == "🎯 Technical Analysis":
        show_technical_analysis_dashboard()  # NEW
    elif page == "📋 Stock Comparison":
        show_stock_comparison_dashboard()    # NEW

def show_technical_analysis_dashboard():
    """Dashboard 1: Single stock technical analysis"""
    
    # Page header
    create_technical_analysis_header()
    
    # Ticker input
    ticker = st.text_input("Enter Stock Symbol:", value="NVDA", key="tech_ticker")
    ticker = ticker.upper().strip()
    
    if ticker:
        # Fetch technical analysis data
        with st.spinner(f"Analyzing {ticker}..."):
            technical_data = get_technical_analysis_data(ticker)
        
        if not technical_data.get('error'):
            # Display all components
            display_moving_averages_table(technical_data['moving_averages'])
            display_technical_indicators_table(technical_data['indicators'])  
            display_52_week_analysis_table(technical_data['extremes'])
            display_rolling_heatmap(technical_data['rolling_signals'])
            display_pivot_points_table(technical_data['pivot_points'])
        else:
            st.error(f"Error analyzing {ticker}: {technical_data['message']}")

def show_stock_comparison_dashboard():
    """Dashboard 2: Multi-stock technical comparison"""
    
    # Reuse existing bucket system with technical indicators
    controls = create_sidebar_controls_extended()  # Extended version
    
    if controls['technical_indicator'] and controls['tickers']:
        # Calculate technical indicator for all tickers
        comparison_data = calculate_multi_stock_technical(
            controls['tickers'], 
            controls['technical_indicator']
        )
        
        # Display using existing heatmap infrastructure
        display_technical_heatmap(comparison_data, controls)
```

### **UI Component Structure**
```python
# src/visualization/technical_dashboard.py (NEW)
class TechnicalAnalysisDashboard:
    """UI components for technical analysis dashboards"""
    
    def __init__(self):
        self.calculator = DatabaseIntegratedTechnicalCalculator()
    
    def display_moving_averages_table(self, ma_data: Dict) -> None:
        """Render moving averages table with exact user specifications"""
        
        # Create structured table data
        table_data = self._prepare_ma_table_data(ma_data)
        
        # Display with enhanced formatting
        st.subheader("📈 Moving Averages Analysis")
        st.caption(f"Current Price: ${ma_data['current_price']:.2f} ({ma_data['timestamp']})")
        
        # Create styled dataframe with color coding
        styled_df = self._style_ma_table(table_data)
        st.dataframe(styled_df, use_container_width=True)
        
        # Add heatmap columns using plotly
        self._display_ma_heatmap_columns(table_data)
    
    def display_technical_indicators_table(self, indicators_data: Dict) -> None:
        """Render technical indicators table with signals and comments"""
        
        st.subheader("📊 Technical Indicators")
        
        # Create table with proper formatting
        table_data = []
        for indicator_name, indicator_info in indicators_data.items():
            table_data.append({
                'Indicator': self._format_indicator_name(indicator_name),
                'Value': self._format_indicator_value(indicator_info['value'], indicator_name),
                'Signal': indicator_info['signal'],
                'Comments': indicator_info['comment']
            })
        
        # Display with signal color coding
        df = pd.DataFrame(table_data)
        styled_df = self._style_indicators_table(df)
        st.dataframe(styled_df, use_container_width=True)
    
    def display_rolling_heatmap(self, rolling_data: pd.DataFrame) -> None:
        """Render 10-day x 11-indicator rolling heatmap"""
        
        st.subheader("🔥 Rolling Signal Heatmap (10-Day History)")
        
        # Create interactive heatmap using plotly
        fig = self._create_rolling_heatmap_figure(rolling_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Add signal persistence analysis
        self._display_signal_persistence_analysis(rolling_data)
```

### **Integration with Existing Components**
```python
# Extend existing create_sidebar_controls for Dashboard 2
def create_sidebar_controls_extended():
    """Extended sidebar controls with technical analysis options"""
    
    # Get existing controls (preserves all existing functionality)
    base_controls = create_sidebar_controls()  # From existing system
    
    # Add technical analysis specific controls
    if st.session_state.get('dashboard_mode') == 'technical_comparison':
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔍 Technical Indicator Selection")
        
        indicator_options = {
            "Distance from 200D SMA (%)": "sma_200_distance",
            "Distance from 50D EMA (%)": "ema_50_distance", 
            "RSI (14) Level": "rsi_14",
            "MACD Signal": "macd_signal",
            "ADX Trend Strength": "adx_strength",
            "Williams %R Level": "williams_r",
            "Volume vs 10D Average (%)": "volume_ma_10"
        }
        
        selected_indicator_name = st.sidebar.selectbox(
            "Choose Technical Indicator:",
            options=list(indicator_options.keys()),
            key="technical_indicator_selection"
        )
        
        base_controls['technical_indicator'] = indicator_options[selected_indicator_name]
        base_controls['technical_indicator_name'] = selected_indicator_name
    
    return base_controls

# Extend existing FinvizHeatmapGenerator for technical data
class TechnicalHeatmapGenerator(FinvizHeatmapGenerator):
    """Extended heatmap generator for technical indicators"""
    
    def create_technical_treemap(self, technical_data: List[Dict], indicator: str, **kwargs):
        """Create heatmap for technical indicator data"""
        
        # Adapt technical data to heatmap format
        heatmap_data = self._adapt_technical_data(technical_data, indicator)
        
        # Use existing treemap infrastructure with technical-specific styling
        fig = self.create_treemap(
            performance_data=heatmap_data,
            title=f"Technical Analysis: {kwargs.get('indicator_name', indicator)}",
            **kwargs
        )
        
        return fig
    
    def _adapt_technical_data(self, technical_data: List[Dict], indicator: str) -> List[Dict]:
        """Convert technical indicator data to heatmap-compatible format"""
        
        adapted_data = []
        for item in technical_data:
            adapted_data.append({
                'ticker': item['ticker'],
                'percentage_change': item['indicator_value'],  # Use indicator value as "performance"
                'current_price': item.get('current_price', 0),
                'display_name': item.get('display_name', item['ticker']),
                'signal': item.get('signal', 'Neutral'),
                'technical_indicator': indicator,
                'indicator_value': item['indicator_value']
            })
            
        return adapted_data
```

---

## 🚀 PERFORMANCE ARCHITECTURE

### **Caching Strategy**
```python
# Multi-level caching for optimal performance
class TechnicalAnalysisCache:
    """Comprehensive caching system for technical analysis"""
    
    def __init__(self):
        self.session_cache = {}      # In-memory session cache
        self.calculation_cache = {}   # Expensive calculation cache
        
    # Streamlit session caching
    @st.cache_data(ttl=900)  # 15 minutes
    def get_technical_indicators(ticker: str, save_to_db: bool = True) -> Dict:
        """Cache expensive technical indicator calculations"""
        
    @st.cache_data(ttl=3600)  # 1 hour  
    def get_rolling_heatmap_data(ticker: str, days: int = 10) -> pd.DataFrame:
        """Cache rolling heatmap matrix calculations"""
        
    @st.cache_data(ttl=1800)  # 30 minutes
    def get_pivot_points(ticker: str) -> Dict:
        """Cache pivot point calculations"""

# Database query optimization
class OptimizedQueries:
    """Optimized database queries for technical analysis"""
    
    @staticmethod
    def get_rolling_indicators_batch(ticker: str, days: int = 10) -> pd.DataFrame:
        """Optimized query for rolling heatmap data"""
        query = """
        SELECT date, rsi_14, macd_value, stoch_k, adx_value, williams_r,
               cci_14, ultimate_osc, roc_12, sma_20, ema_50
        FROM technical_indicators_daily 
        WHERE ticker = ? AND date >= date('now', '-{} days')
        ORDER BY date DESC
        """.format(days + 5)  # Buffer for weekends
        
        return pd.read_sql(query, conn, params=[ticker])
    
    @staticmethod  
    def get_latest_indicators_batch(tickers: List[str]) -> pd.DataFrame:
        """Optimized query for multi-ticker latest indicators"""
        placeholders = ','.join(['?' for _ in tickers])
        query = f"""
        SELECT ticker, date, rsi_14, macd_value, stoch_k, adx_value,
               sma_200, ema_50, williams_r, cci_14
        FROM technical_indicators_daily t1
        WHERE ticker IN ({placeholders})
        AND date = (
            SELECT MAX(date) FROM technical_indicators_daily t2 
            WHERE t2.ticker = t1.ticker
        )
        """
        
        return pd.read_sql(query, conn, params=tickers)
```

### **Parallel Processing for Multi-Stock Analysis**
```python
import concurrent.futures
from typing import List, Dict

class ParallelTechnicalProcessor:
    """Parallel processing for Dashboard 2 multi-stock analysis"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.calculator = DatabaseIntegratedTechnicalCalculator()
    
    def calculate_indicators_parallel(self, tickers: List[str], indicator: str) -> List[Dict]:
        """Process multiple tickers in parallel"""
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all ticker calculations
            future_to_ticker = {
                executor.submit(self._calculate_single_indicator, ticker, indicator): ticker 
                for ticker in tickers
            }
            
            results = []
            for future in concurrent.futures.as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    result = future.result(timeout=10)  # 10 second timeout per ticker
                    result['ticker'] = ticker
                    results.append(result)
                except Exception as e:
                    # Handle individual ticker failures gracefully
                    results.append({
                        'ticker': ticker,
                        'error': True, 
                        'message': str(e)
                    })
        
        return results
    
    def _calculate_single_indicator(self, ticker: str, indicator: str) -> Dict:
        """Calculate single indicator for single ticker"""
        return self.calculator.calculate_single_indicator(ticker, indicator)
```

### **Memory Management**
```python
class MemoryOptimizedCalculations:
    """Memory-efficient calculations for large datasets"""
    
    @staticmethod
    def calculate_indicators_streaming(data: pd.DataFrame) -> Dict:
        """Stream-based calculation to minimize memory usage"""
        
        # Process indicators one at a time to minimize peak memory
        results = {}
        
        # Calculate moving averages (memory intensive)
        ma_results = TechnicalCalculations.calculate_moving_averages(data)
        results.update({k: v.iloc[-1] for k, v in ma_results.items()})
        del ma_results  # Free memory immediately
        
        # Calculate momentum indicators
        momentum_results = TechnicalCalculations.calculate_momentum_indicators(data)
        results.update({k: v.iloc[-1] for k, v in momentum_results.items()})
        del momentum_results
        
        return results
    
    @staticmethod
    def optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
        """Optimize DataFrame memory usage"""
        
        # Convert float64 to float32 where precision allows
        for col in df.select_dtypes(include=['float64']):
            df[col] = pd.to_numeric(df[col], downcast='float')
            
        # Convert int64 to smaller int types where possible
        for col in df.select_dtypes(include=['int64']):
            df[col] = pd.to_numeric(df[col], downcast='integer')
            
        return df
```

---

## 🔒 ERROR HANDLING ARCHITECTURE

### **Comprehensive Error Handling Strategy**
```python
class TechnicalAnalysisErrorHandler:
    """Centralized error handling for technical analysis"""
    
    @staticmethod
    def handle_calculation_error(func):
        """Decorator for calculation error handling"""
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Calculation error in {func.__name__}: {str(e)}")
                return {
                    'error': True,
                    'message': f'Calculation failed: {str(e)}',
                    'function': func.__name__
                }
        return wrapper
    
    @staticmethod
    def handle_data_quality_issues(data: pd.DataFrame, min_required_days: int = 200) -> Dict:
        """Validate data quality for technical calculations"""
        
        issues = []
        
        # Check minimum data requirements
        if len(data) < min_required_days:
            issues.append(f"Insufficient data: {len(data)} days, need {min_required_days}")
        
        # Check for missing OHLCV columns
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_cols = [col for col in required_cols if col not in data.columns]
        if missing_cols:
            issues.append(f"Missing required columns: {missing_cols}")
        
        # Check for excessive missing values
        for col in required_cols:
            if col in data.columns:
                missing_pct = data[col].isnull().sum() / len(data)
                if missing_pct > 0.05:  # More than 5% missing
                    issues.append(f"Excessive missing data in {col}: {missing_pct:.1%}")
        
        # Check for data quality issues
        if data['High'].min() <= 0 or data['Low'].min() <= 0:
            issues.append("Invalid price data: zero or negative prices")
            
        if (data['High'] < data['Low']).any():
            issues.append("Invalid OHLC data: High < Low detected")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'data_days': len(data)
        }
    
    @staticmethod
    def create_error_response(error_type: str, message: str, ticker: str = None) -> Dict:
        """Create standardized error response"""
        return {
            'error': True,
            'error_type': error_type,
            'message': message,
            'ticker': ticker,
            'timestamp': datetime.now().isoformat()
        }

# Graceful degradation strategies
class GracefulDegradation:
    """Strategies for handling partial failures"""
    
    @staticmethod
    def handle_partial_indicator_failure(indicators: Dict) -> Dict:
        """Handle cases where some indicators fail to calculate"""
        
        successful_indicators = {}
        failed_indicators = []
        
        for name, result in indicators.items():
            if isinstance(result, dict) and result.get('error'):
                failed_indicators.append(name)
            else:
                successful_indicators[name] = result
        
        return {
            'successful': successful_indicators,
            'failed': failed_indicators,
            'partial_success': len(successful_indicators) > 0
        }
    
    @staticmethod
    def create_fallback_display(ticker: str, error_message: str) -> Dict:
        """Create fallback display when technical analysis fails"""
        
        return {
            'ticker': ticker,
            'message': f"Technical analysis unavailable for {ticker}",
            'error_details': error_message,
            'suggestions': [
                "Try a different ticker symbol",
                "Check if ticker has sufficient trading history (>200 days)",
                "Verify ticker symbol is correct and actively traded"
            ]
        }
```

---

## 📊 TESTING ARCHITECTURE

### **Unit Testing Strategy**
```python
# tests/test_technical_calculator.py
import unittest
import pandas as pd
from datetime import datetime, timedelta

class TestTechnicalCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calculator = DatabaseIntegratedTechnicalCalculator()
        
        # Create test data
        dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
        self.test_data = pd.DataFrame({
            'Date': dates,
            'Open': 100 + np.random.randn(len(dates)).cumsum(),
            'High': 102 + np.random.randn(len(dates)).cumsum(),
            'Low': 98 + np.random.randn(len(dates)).cumsum(), 
            'Close': 101 + np.random.randn(len(dates)).cumsum(),
            'Volume': 1000000 + np.random.randint(-100000, 100000, len(dates))
        })
    
    def test_rsi_calculation(self):
        """Test RSI calculation accuracy"""
        rsi_processor = RSISignalProcessor()
        result = rsi_processor.process_indicator(self.test_data, period=14)
        
        self.assertFalse(result['error'])
        self.assertIsInstance(result['value'], float)
        self.assertTrue(0 <= result['value'] <= 100)
        self.assertIn(result['signal'], ['Buy', 'Sell', 'Strong Buy', 'Strong Sell'])
    
    def test_moving_average_signals(self):
        """Test moving average signal generation"""
        ma_processor = MovingAverageSignalProcessor()
        
        # Test various price positions relative to MA
        test_cases = [
            (100.0, 99.0, "Buy"),    # Price 1% above MA
            (100.0, 101.0, "Sell"),  # Price 1% below MA  
            (100.0, 100.1, "Neutral")  # Price 0.1% below MA (within neutral zone)
        ]
        
        for current_price, ma_value, expected_signal in test_cases:
            signal = ma_processor._generate_ma_signal(current_price, ma_value)
            self.assertEqual(signal['signal'], expected_signal)

# Integration testing
class TestTechnicalAnalysisIntegration(unittest.TestCase):
    
    def test_dashboard_1_complete_analysis(self):
        """Test complete Dashboard 1 analysis flow"""
        result = self.calculator.calculate_single_stock_analysis('NVDA')
        
        # Verify all required components present
        required_components = [
            'moving_averages', 'technical_indicators', 
            'extremes_analysis', 'pivot_points'
        ]
        for component in required_components:
            self.assertIn(component, result)
            self.assertFalse(result[component].get('error', False))
    
    def test_dashboard_2_multi_stock(self):
        """Test Dashboard 2 multi-stock comparison"""
        tickers = ['NVDA', 'AAPL', 'MSFT']
        result = self.calculator.calculate_multi_stock_indicator(tickers, 'rsi_14')
        
        self.assertEqual(len(result), len(tickers))
        for ticker_result in result:
            self.assertIn('ticker', ticker_result)
            self.assertIn('indicator_value', ticker_result)

# Performance testing
class TestPerformanceRequirements(unittest.TestCase):
    
    def test_single_stock_performance(self):
        """Test Dashboard 1 meets <3 second requirement"""
        start_time = time.time()
        result = self.calculator.calculate_single_stock_analysis('NVDA')
        execution_time = time.time() - start_time
        
        self.assertLess(execution_time, 3.0)  # <3 second requirement
        self.assertFalse(result.get('error', False))
    
    def test_multi_stock_performance(self):
        """Test Dashboard 2 meets <5 second requirement for 50+ tickers"""
        tickers = [f'TICKER_{i}' for i in range(50)]  # 50 test tickers
        
        start_time = time.time()
        result = self.calculator.calculate_multi_stock_indicator(tickers, 'rsi_14')
        execution_time = time.time() - start_time
        
        self.assertLess(execution_time, 5.0)  # <5 second requirement
```

### **Data Validation Testing**
```python
class TestSignalLogicValidation(unittest.TestCase):
    
    def test_rsi_signal_thresholds(self):
        """Validate RSI signal logic against specifications"""
        test_cases = [
            (85.0, "Strong Sell", "Extremely overbought"),
            (75.0, "Sell", "Overbought"),
            (55.0, "Buy", "Bullish momentum"),
            (45.0, "Sell", "Bearish momentum"), 
            (25.0, "Buy", "Oversold"),
            (15.0, "Strong Buy", "Extremely oversold")
        ]
        
        processor = RSISignalProcessor()
        for rsi_value, expected_signal, expected_context in test_cases:
            result = processor.generate_signal(rsi_value)
            self.assertEqual(result['signal'], expected_signal)
            self.assertIn(expected_context.lower(), result['comment'].lower())
    
    def test_moving_average_neutral_zone(self):
        """Test ±0.25% neutral zone for moving averages"""
        processor = MovingAverageSignalProcessor()
        
        # Test cases within and outside neutral zone
        test_cases = [
            (100.0, 99.8, "Neutral"),   # 0.2% above MA (within neutral zone)
            (100.0, 100.2, "Neutral"),  # 0.2% below MA (within neutral zone)
            (100.0, 99.7, "Buy"),       # 0.3% above MA (outside neutral zone)
            (100.0, 100.3, "Sell")      # 0.3% below MA (outside neutral zone)
        ]
        
        for price, ma_value, expected_signal in test_cases:
            result = processor._generate_ma_signal(price, ma_value)
            self.assertEqual(result['signal'], expected_signal)
```

---

## 🔧 DEPLOYMENT ARCHITECTURE

### **Production Configuration**
```python
# config/production_config.py
class ProductionConfig:
    """Production-specific configuration"""
    
    # Database settings
    DATABASE_FILE = "data/stock_data.db"
    DATABASE_BACKUP_ENABLED = True
    DATABASE_BACKUP_INTERVAL_HOURS = 24
    
    # Performance settings  
    MAX_CONCURRENT_CALCULATIONS = 4
    CALCULATION_TIMEOUT_SECONDS = 30
    CACHE_TTL_MINUTES = 15
    
    # API limits
    YFINANCE_MAX_REQUESTS_PER_MINUTE = 100
    YFINANCE_RETRY_ATTEMPTS = 3
    YFINANCE_BACKOFF_SECONDS = 5
    
    # UI settings
    STREAMLIT_SERVER_PORT = 8501
    STREAMLIT_SERVER_ADDRESS = "0.0.0.0"
    STREAMLIT_MAX_UPLOAD_SIZE = 200  # MB
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/technical_analysis.log"
    LOG_ROTATION_SIZE = "10MB"
    LOG_BACKUP_COUNT = 5

# monitoring/health_checks.py
class SystemHealthChecker:
    """Production health monitoring"""
    
    def check_database_health(self) -> Dict:
        """Check database connectivity and performance"""
        try:
            conn = sqlite3.connect(ProductionConfig.DATABASE_FILE)
            
            # Test basic query performance
            start_time = time.time()
            cursor = conn.execute("SELECT COUNT(*) FROM daily_prices")
            count = cursor.fetchone()[0]
            query_time = time.time() - start_time
            
            conn.close()
            
            return {
                'status': 'healthy',
                'record_count': count,
                'query_time_ms': int(query_time * 1000)
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def check_api_connectivity(self) -> Dict:
        """Test yfinance API connectivity"""
        try:
            import yfinance as yf
            ticker = yf.Ticker("AAPL")
            
            start_time = time.time()
            info = ticker.info
            api_time = time.time() - start_time
            
            return {
                'status': 'healthy',
                'api_response_time_ms': int(api_time * 1000),
                'test_ticker': 'AAPL'
            }
        except Exception as e:
            return {
                'status': 'unhealthy', 
                'error': str(e)
            }
```

---

## 📈 SCALABILITY CONSIDERATIONS

### **Future Expansion Architecture**
```python
class ScalableArchitecture:
    """Architecture designed for future expansion"""
    
    # Modular indicator system - easy to add new indicators
    def register_new_indicator(self, name: str, processor_class: SignalProcessor):
        """Dynamically register new technical indicators"""
        self.signal_processors[name] = processor_class()
    
    # Plugin-based architecture for new dashboard types
    def register_dashboard_plugin(self, name: str, dashboard_class):
        """Register new dashboard types"""
        self.dashboard_plugins[name] = dashboard_class
    
    # Scalable database partitioning strategy
    def implement_database_partitioning(self):
        """Future: Partition tables by date ranges for performance"""
        # technical_indicators_daily_2024, technical_indicators_daily_2025, etc.
        pass
    
    # API-ready architecture for external integrations
    def create_rest_api_endpoints(self):
        """Future: Expose technical analysis via REST API"""
        # GET /api/technical/{ticker}
        # GET /api/technical/compare?tickers=NVDA,AAPL&indicator=rsi_14
        pass

# Horizontal scaling preparation
class DistributedCalculations:
    """Prepare for distributed calculation scenarios"""
    
    def setup_calculation_queue(self):
        """Future: Queue-based calculation distribution"""
        # Use Redis/Celery for distributed calculations
        pass
    
    def implement_result_caching(self):
        """Future: Distributed caching with Redis"""
        # Cache calculation results across multiple instances
        pass
```

---

*This technical architecture provides a comprehensive blueprint for implementing the Technical Analysis Suite while maintaining the proven patterns and quality standards of the existing Stock Performance Heatmap Dashboard. The architecture ensures seamless integration, optimal performance, and future scalability.*