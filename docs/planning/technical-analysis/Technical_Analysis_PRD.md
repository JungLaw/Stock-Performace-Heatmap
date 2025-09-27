# Technical Analysis Suite - Product Requirements Document (PRD)
**Project**: Stock Performance Dashboard - Technical Analysis Extension  
**Date**: September 25, 2025  
**Version**: 1.0  
**Status**: Planning Phase

---

## 🎯 EXECUTIVE SUMMARY

### **Vision**
Extend the existing Stock Performance Heatmap Dashboard with comprehensive technical analysis capabilities, providing traders and investors with professional-grade technical indicators, moving averages analysis, and multi-timeframe insights within the proven Streamlit application framework.

### **Goals**
1. **Dashboard 1**: Single-stock comprehensive technical analysis (Priority 1)
2. **Dashboard 2**: Multi-stock technical indicator comparison using existing bucket system (Priority 2)  
3. **Dashboard 3**: Interactive candlestick charts with technical overlays (Future)

### **Success Metrics**
- ✅ Complete technical indicator coverage (10+ indicators with custom signal logic)
- ✅ Professional UI matching TipRanks/Investing.com quality standards
- ✅ Sub-3 second load times for single stock analysis
- ✅ Integration with existing database and three-bucket architecture
- ✅ Rolling heatmap functionality (10 days x key indicators)

---

## 📊 PRODUCT OVERVIEW

### **Current State Integration**
**Extends Existing System:**
- ✅ Stock Performance Heatmap Dashboard (Production Ready)
- ✅ Three-bucket architecture (Country ETFs, Sector ETFs, Custom stocks)
- ✅ Database-first approach with 21K+ historical records
- ✅ Price and Volume performance analysis modes

**New Technical Analysis Integration:**
- 🆕 Technical Analysis dashboard section within existing Streamlit app
- 🆕 DatabaseIntegratedTechnicalCalculator following proven patterns
- 🆕 Technical indicators database tables extending current schema
- 🆕 Professional technical analysis UI components

---

## 🏗️ FEATURE REQUIREMENTS

### **DASHBOARD 1: Single Stock Technical Analysis** (Priority 1)

#### **Core Features**
- **Ticker Input**: User-selectable stock symbol (default: NVDA)
- **Moving Averages Analysis**: Comprehensive SMA/EMA table with signals
- **Technical Indicators**: 10+ indicators with custom signal logic  
- **52-Week High Analysis**: Custom percentage breakdown table
- **Rolling Heatmap**: 10-day historical indicator signal visualization
- **Pivot Points**: Classic, Fibonacci, Woody's, Camarilla levels

#### **Moving Averages Table Specifications**
```
Current Price: $177.19 (9/25/25, 12:31PM)

| Metric | SMA     | EMA     | SMA/P0 | EMA/P0 | P0/SMA | Signal | P0/EMA | Signal |
|--------|---------|---------|--------|--------|--------|--------|--------|--------|
| MA5    | $174.27 | $175.40 | -1.6%  | -1.0%  | +1.7%  | Buy    | +1.0%  | Buy    |
| MA9    | $xxx.xx | $xxx.xx | x.x%   | x.x%   | +x.x%  | Signal | +x.x%  | Signal |
| MA10   | $172.56 | $174.48 | -2.6%  | -1.5%  | +2.7%  | Buy    | +1.6%  | Buy    |
| MA20   | $175.76 | $175.04 | -0.8%  | -1.2%  | +0.8%  | Buy    | +1.2%  | Buy    |
| MA21   | $xxx.xx | $xxx.xx | x.x%   | x.x%   | +x.x%  | Signal | +x.x%  | Signal |
| MA50   | $174.11 | $170.17 | -1.7%  | -4.0%  | +1.8%  | Buy    | +4.1%  | Buy    |
| MA100  | $153.49 | $158.94 | -13.4% | -10.3% | +15.4% | Buy    | +11.5% | Buy    |
| MA200  | $139.95 | $147.35 | -21.0% | -16.8% | +26.6% | Buy    | +20.3% | Buy    |
```

**Moving Averages Features:**
- ✅ SMA & EMA calculations for periods: 5, 9, 10, 20, 21, 50, 100, 200
- ✅ Bidirectional percentage analysis (MA vs Price, Price vs MA)
- ✅ Signal generation: Buy/Sell/Neutral based on ±0.25% thresholds
- ✅ Color coding: Green (Buy), Red (Sell), Gray (Neutral)  
- ✅ Percentage color coding: Blue (+), Red (-)
- ✅ Column heatmap visualization for SMA and EMA values

#### **Technical Indicators Table Specifications**
```
| Indicator Name    | Value | Signal      | Comments                           |
|------------------|-------|-------------|------------------------------------|
| RSI (14)         | 52.37 | Buy         | Bullish momentum above 50          |
| STOCH (9,6)      | 58.61 | Buy         | %K above 50, bullish bias          |
| MACD (12,26)     | -0.04 | Sell        | Below zero, bearish momentum       |
| ADX (14)         | 24.08 | Weak (Neutral) | Below 25, no clear trend        |
| Williams %R      | -24.92| Buy         | Above -80, bullish territory       |
| CCI (14)         | 11.09 | Neutral     | Between -100 and +100             |
| Ultimate Osc     | 55.40 | Neutral     | Between 30-70 range               |
| ROC (12)         | -2.16 | Sell        | Negative rate of change           |
| ATR (14)         | 4.97  | -           | Volatility measure                |
| Bull/Bear Power  | +0.85 | Buy         | Positive value, bulls stronger    |
```

**Technical Indicators Features:**
- ✅ 10+ professional technical indicators with pandas-ta-classic
- ✅ Custom signal logic following user specifications  
- ✅ Signal classifications: Buy, Sell, Strong Buy, Strong Sell, Neutral
- ✅ Contextual comments explaining current indicator state
- ✅ Color-coded signals for immediate visual recognition

#### **52-Week High Analysis Table**
```
| Window | High    | -5%     | -10%    | -15%    | -20%    | Low     | vs High | vs -5%  | vs -10% | vs -15% | vs -20% | vs Low  |
|--------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| 52W    | $184.48 | $175.26 | $166.03 | $156.81 | $147.58 | $94.31  | -4.0%   | +1.1%   | +6.7%   | +13.0%  | +20.1%  | +87.9%  |
| 3M     | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | +x.x%   | +x.x%   | +x.x%   | +x.x%   | +x.x%   | +x.x%   |
| 1M     | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | +x.x%   | +x.x%   | +x.x%   | +x.x%   | +x.x%   | +x.x%   |
| 2W     | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | +x.x%   | +x.x%   | +x.x%   | +x.x%   | +x.x%   | +x.x%   |
```

**52-Week High Features:**
- ✅ Multiple time periods: 52W, 3M, 1M, 2W
- ✅ Percentage breakdown levels: -5%, -10%, -15%, -20%
- ✅ Current price comparison to all levels
- ✅ Color coding for proximity to highs/lows

#### **Rolling Heatmap Specifications**
**10-Day Technical Indicator Signal History**
```
Indicator    | Day-10 | Day-9 | Day-8 | Day-7 | Day-6 | Day-5 | Day-4 | Day-3 | Day-2 | Day-1 |
-------------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
SMA(20)      | Buy    | Buy   | Buy   | Sell  | Sell  | Buy   | Buy   | Buy   | Buy   | Buy   |
EMA(50)      | Buy    | Buy   | Buy   | Buy   | Buy   | Buy   | Buy   | Sell  | Sell  | Buy   |
RSI(14)      | Sell   | Sell  | Buy   | Buy   | Buy   | Buy   | Sell  | Sell  | Buy   | Buy   |
MACD(12,26)  | Buy    | Buy   | Buy   | Sell  | Sell  | Sell  | Buy   | Buy   | Buy   | Sell  |
Stoch(9,6)   | Neutral| Buy   | Buy   | Buy   | Sell  | Sell  | Buy   | Buy   | Buy   | Buy   |
```

**Rolling Heatmap Features:**  
- ✅ 10 trading days of signal history
- ✅ 11 key technical indicators
- ✅ Color-coded cells: Green (Buy), Red (Sell), Gray (Neutral)
- ✅ Signal persistence analysis and trend identification
- ✅ Database storage of historical technical indicator values

#### **Pivot Points Table**
```
| Type       | S3      | S2      | S1      | Pivot   | R1      | R2      | R3      |
|------------|---------|---------|---------|---------|---------|---------|---------|
| Classic    | $163.28 | $165.84 | $168.07 | $170.63 | $172.86 | $175.42 | $177.65 |
| Fibonacci  | $165.84 | $167.67 | $168.80 | $170.63 | $172.46 | $173.59 | $175.42 |
| Woody's    | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx |
| Camarilla  | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx | $xxx.xx |
```

### **DASHBOARD 2: Multi-Stock Technical Comparison** (Priority 2)

#### **Core Features**
- **Bucket Integration**: Use existing Country ETFs, Sector ETFs, Custom stocks system
- **Single Indicator Focus**: Dropdown selection of technical indicator
- **Heatmap Visualization**: Leverage existing FinvizHeatmapGenerator
- **Comparative Analysis**: Find stocks with highest RSI, closest to 200D MA, etc.

#### **Technical Indicator Selection**
```
Dropdown Options:
- Distance from 200D SMA (%)
- Distance from 50D EMA (%) 
- RSI (14) Level
- MACD Signal (Bullish/Bearish)
- ADX Trend Strength
- Williams %R Level
- Golden Cross Proximity (Days)
- Death Cross Proximity (Days)
- Volume vs MA(10) (%)
```

#### **Heatmap Integration**
- ✅ Reuse existing three-bucket radio button system
- ✅ Replace performance_data with technical_indicator_data
- ✅ Color coding based on selected indicator (custom scales per indicator)
- ✅ Hover tooltips showing exact indicator values and signals
- ✅ Real-time filtering and bucket management

### **DASHBOARD 3: Interactive Candlestick Charts** (Future Priority)

#### **Deferred Features**
- Interactive price charts with technical indicator overlays
- Multiple timeframe support (1M, 5M, 15M, 1H, 1D, 1W, 1M)
- Indicator selection and parameter customization  
- Chart pattern recognition and alerts

---

## 🔧 TECHNICAL REQUIREMENTS

### **Database Schema Extensions**
```sql
-- Technical indicators storage for rolling heatmap
CREATE TABLE technical_indicators_daily (
    ticker TEXT,
    date DATE,
    rsi_14 REAL,
    sma_5 REAL, sma_10 REAL, sma_20 REAL, sma_50 REAL, sma_100 REAL, sma_200 REAL,
    ema_5 REAL, ema_10 REAL, ema_20 REAL, ema_50 REAL, ema_100 REAL, ema_200 REAL,
    macd_value REAL, macd_signal REAL, macd_histogram REAL,
    stoch_k REAL, stoch_d REAL,
    adx_value REAL, plus_di REAL, minus_di REAL,
    williams_r REAL,
    cci_14 REAL,
    ultimate_osc REAL,
    roc_12 REAL,
    atr_14 REAL,
    bull_power REAL, bear_power REAL,
    created_at TIMESTAMP,
    PRIMARY KEY (ticker, date)
);

-- Price extremes for 52-week analysis
CREATE TABLE price_extremes_periods (
    ticker TEXT,
    period TEXT,  -- '52w', '3m', '1m', '2w'
    high_price REAL,
    low_price REAL,
    high_date DATE,
    low_date DATE,
    updated_at TIMESTAMP,
    PRIMARY KEY (ticker, period)
);

-- Pivot points calculations
CREATE TABLE pivot_points_daily (
    ticker TEXT,
    date DATE,
    pivot_type TEXT,  -- 'classic', 'fibonacci', 'woodys', 'camarilla'
    pivot REAL,
    r1 REAL, r2 REAL, r3 REAL,
    s1 REAL, s2 REAL, s3 REAL,
    PRIMARY KEY (ticker, date, pivot_type)
);
```

### **Calculation Engine Architecture**
```python
class DatabaseIntegratedTechnicalCalculator:
    """Technical analysis calculator following existing database-first patterns"""
    
    def __init__(self, db_file="data/stock_data.db"):
        self.db_file = db_file
        self.signal_processors = {
            'moving_averages': MovingAverageSignalProcessor(),
            'rsi': RSISignalProcessor(),
            'macd': MACDSignalProcessor(),
            'stoch': StochasticSignalProcessor(),
            # ... etc for each indicator
        }
    
    def calculate_single_stock_analysis(self, ticker: str) -> Dict:
        """Dashboard 1: Complete technical analysis for single stock"""
        
    def calculate_multi_stock_indicator(self, tickers: List[str], indicator: str) -> List[Dict]:
        """Dashboard 2: Single indicator across multiple stocks"""
        
    def get_rolling_heatmap_data(self, ticker: str, days: int = 10) -> DataFrame:
        """10-day historical signal matrix"""
```

### **Signal Logic Implementation**
- ✅ Hierarchical signal precedence (extreme conditions override basic signals)
- ✅ Custom thresholds for each indicator based on user specifications
- ✅ Crossover detection for Williams %R, MACD signal line  
- ✅ Complex ADX logic with trend strength and direction analysis
- ✅ Moving average signal logic with ±0.25% neutral zones

### **UI Integration Architecture**  
```python
# streamlit_app.py (extended)
def main():
    # Existing functionality preserved
    page = st.sidebar.selectbox("Choose Dashboard:", [
        "📈 Performance Heatmaps",      # Existing system
        "🎯 Technical Analysis",        # NEW: Dashboard 1
        "📋 Stock Comparison"           # NEW: Dashboard 2  
    ])
    
    if page == "📈 Performance Heatmaps":
        show_performance_heatmaps()     # Existing code
    elif page == "🎯 Technical Analysis":
        show_technical_analysis_dashboard()  # NEW
    elif page == "📋 Stock Comparison":
        show_stock_comparison_dashboard()    # NEW
```

### **Performance Requirements**
- ✅ **Single Stock Analysis**: <3 seconds load time
- ✅ **Multi-Stock Comparison**: <5 seconds for 50+ tickers
- ✅ **Database Queries**: <500ms for technical indicator lookups
- ✅ **Rolling Heatmap**: <2 seconds for 10-day matrix generation
- ✅ **Memory Usage**: <200MB for single stock analysis session

---

## 📅 IMPLEMENTATION TIMELINE

### **Phase 1: Core Technical Calculator** (Weeks 1-2)
- DatabaseIntegratedTechnicalCalculator implementation
- Signal logic processors for all indicators
- Database schema creation and migration
- Basic data fetching and caching integration

### **Phase 2: Dashboard 1 - Single Stock Analysis** (Weeks 3-4)  
- Moving averages table with full specifications
- Technical indicators table with signal logic
- 52-week high analysis implementation
- Basic UI layout and navigation integration

### **Phase 3: Advanced Dashboard 1 Features** (Weeks 5-6)
- Rolling heatmap (10-day historical signals)  
- Pivot points calculations (all 4 types)
- Professional UI polish and color coding
- Comments generation and contextual explanations

### **Phase 4: Dashboard 2 - Multi-Stock Comparison** (Weeks 7-8)
- Technical indicator dropdown selection
- Integration with existing bucket system
- Heatmap visualization for technical metrics
- Comparative analysis features ("find highest RSI", etc.)

### **Phase 5: Polish and Optimization** (Week 9)
- Performance optimization and caching
- Error handling and edge cases
- Documentation and user testing
- Integration testing with existing functionality

---

## ⚠️ RISKS AND MITIGATION STRATEGIES

### **Technical Risks**
1. **pandas-ta-classic Integration**
   - **Risk**: Library compatibility or missing indicators
   - **Mitigation**: Test all required indicators early, implement manual calculations as backup

2. **Database Performance**  
   - **Risk**: Slow queries for rolling heatmap with historical data
   - **Mitigation**: Proper indexing, data archival strategy, query optimization

3. **Signal Logic Complexity**
   - **Risk**: Bugs in custom signal logic, especially ADX and crossover detection
   - **Mitigation**: Comprehensive unit testing, validation against known indicator values

### **Integration Risks**
1. **UI Performance with Complex Tables**
   - **Risk**: Streamlit performance degradation with large technical tables
   - **Mitigation**: Pagination, lazy loading, caching of rendered components

2. **Existing System Impact**
   - **Risk**: Technical analysis features affect existing heatmap performance  
   - **Mitigation**: Separate calculation paths, isolated database queries

### **Data Quality Risks**
1. **Missing Historical Data**
   - **Risk**: Insufficient data for rolling heatmap or 52-week analysis
   - **Mitigation**: Data backfill strategy, graceful degradation for new tickers

---

## 🎯 SUCCESS CRITERIA

### **Functional Requirements Met**
- ✅ All 10+ technical indicators implemented with custom signal logic
- ✅ Moving averages table matches exact specifications 
- ✅ Rolling heatmap displays 10-day signal history accurately
- ✅ Integration with existing bucket system for Dashboard 2
- ✅ Professional UI quality matching reference sites

### **Performance Requirements Met**
- ✅ Single stock technical analysis loads in <3 seconds
- ✅ Multi-stock comparison handles 50+ tickers efficiently  
- ✅ Database queries respond in <500ms
- ✅ No impact on existing heatmap system performance

### **User Experience Requirements Met**
- ✅ Intuitive navigation between existing and new features
- ✅ Professional visual design consistent with existing system
- ✅ Clear signal explanations and contextual comments
- ✅ Color coding and visual hierarchy aid quick analysis

### **Technical Quality Requirements Met**  
- ✅ Clean integration with existing DatabaseIntegrated* patterns
- ✅ Comprehensive error handling and graceful degradation
- ✅ Database schema properly indexed and optimized
- ✅ Code follows established project patterns and standards

---

## 📚 REFERENCE MATERIALS

### **UI/UX References**
- **TipRanks Technical Analysis**: Consensus gauges, moving averages table, technical indicators layout
- **Investing.com Technical**: Technical indicators table format, pivot points display
- **Financhill Rolling Heatmap**: 10-day x 11-indicator matrix visualization
- **ChartMill Signal Analysis**: Detailed signal comments and explanations

### **Signal Logic References**
- **User-Defined Signal Logic**: Custom thresholds and rules for all indicators
- **Moving Averages**: ±0.25% thresholds for Buy/Sell/Neutral signals
- **ADX Complex Logic**: Trend strength classification with directional analysis
- **Crossover Detection**: Williams %R and MACD signal line crossover rules

---

*This PRD serves as the definitive specification for technical analysis implementation, ensuring professional delivery within existing application architecture.*