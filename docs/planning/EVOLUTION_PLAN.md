# Stock Screener to Heatmap Dashboard Evolution Plan

## Project Restructuring Strategy

### Phase 1: Preserve and Reorganize (Week 1)

#### Current Assets to Preserve
- `stock_data.db` - Valuable historical data foundation
- `main.py` - Excellent data fetching and database setup logic
- `utils_database.py` - Production-quality database utilities
- `pyproject.toml` - Modern dependency management
- `.git/` - Version control history

#### New Project Structure
```
stock-heatmap-dashboard/
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── fetcher.py          # Evolved from main.py
│   │   ├── database.py         # Evolved from utils_database.py
│   │   ├── processor.py        # NEW: data transformation
│   │   └── cache.py           # NEW: caching logic
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── heatmap.py         # NEW: plotly treemap
│   │   └── components.py      # NEW: UI components
│   ├── calculations/
│   │   ├── __init__.py
│   │   ├── performance.py     # NEW: price calculations
│   │   └── volume.py          # NEW: volume analysis
│   └── config/
│       ├── __init__.py
│       ├── settings.py        # NEW: app configuration
│       └── assets.py          # NEW: ETF definitions
├── data/                      # Move stock_data.db here
├── tests/
├── docs/
├── streamlit_app.py          # NEW: main entry point
├── pyproject.toml            # UPDATED: add Streamlit deps
├── README.md                 # UPDATED: new project description
└── requirements.txt          # NEW: for deployment
```

### Phase 2: Code Migration and Enhancement

#### 2.1 Database Layer Migration
**Action**: Move and enhance existing database code
- `main.py` → `src/data/fetcher.py` (enhanced)
- `utils_database.py` → `src/data/database.py` (enhanced)
- Add new asset groups (Country ETFs, Sector ETFs)

#### 2.2 Add Missing Dependencies
**Update pyproject.toml**:
```toml
dependencies = [
    # Existing
    "pandas>=2.3.0",
    "plotly>=6.1.2", 
    "yfinance>=0.2.63",
    
    # NEW for heatmap dashboard
    "streamlit>=1.28.0",
    "numpy>=1.24.0",
    "cachetools>=5.3.0",
    "sqlite3",  # built-in
]
```

#### 2.3 Expand Database Schema (Optional Enhancement)
**Consider adding tables**:
```sql
-- Keep existing daily_prices table
-- Add metadata table
CREATE TABLE IF NOT EXISTS ticker_metadata (
    Ticker TEXT PRIMARY KEY,
    Name TEXT,
    Sector TEXT,
    Category TEXT,  -- 'country_etf', 'sector_etf', 'custom'
    MarketCap REAL,
    LastUpdated TEXT
);

-- Add volume averages cache
CREATE TABLE IF NOT EXISTS volume_averages (
    Ticker TEXT PRIMARY KEY,
    Avg10Day REAL,
    Avg3Month REAL,
    LastCalculated TEXT
);
```

### Phase 3: New Feature Development

#### 3.1 Asset Group Expansion
**Extend existing ticker list**:
```python
# Current: 14 tickers
EXISTING_TICKERS = ["NVDA", "META", "MSFT", "IYK", "IYC", "MCHI", "EWJ",
                   "AMZN", "AAPL", "GOOGL", "SPY", "QQQ", "IYE", "IYF"]

# Add PRD-required asset groups
COUNTRY_ETFS = [52 tickers from PRD]
SECTOR_ETFS = [30 tickers from PRD]
CUSTOM_DEFAULT = ["AMZN", "META", "NVDA", "AAPL", "GOOGL", "MSFT", "BABA", "SPY", "QQQ"]
```

#### 3.2 Performance Calculations
**Build on existing data**:
- Use existing OHLCV data for price change calculations
- Leverage existing date handling for period comparisons
- Add volume analysis using existing volume data

#### 3.3 Visualization Layer
**New Streamlit + Plotly integration**:
- Build treemap using existing clean data
- Implement Finviz-style design system
- Add interactive controls for existing asset groups

## Migration Timeline

### Week 1: Foundation Restructuring
- [ ] Create new folder structure
- [ ] Migrate existing code to new locations  
- [ ] Update dependencies and configuration
- [ ] Expand database with new asset groups
- [ ] Test existing functionality in new structure

### Week 2: Core Dashboard Development
- [ ] Build Streamlit UI framework
- [ ] Implement basic treemap visualization
- [ ] Add performance calculation logic
- [ ] Integrate existing database with new UI
- [ ] Test with existing ticker data

### Week 3: Feature Enhancement
- [ ] Add volume analysis capabilities
- [ ] Implement Finviz-style design
- [ ] Add interactive controls and filtering
- [ ] Optimize performance and caching
- [ ] Comprehensive testing

## Risk Mitigation

### Data Preservation
- [ ] Backup stock_data.db before any changes
- [ ] Test database migration with copy first
- [ ] Verify data integrity after restructuring

### Code Quality Maintenance  
- [ ] Preserve existing error handling patterns
- [ ] Maintain existing data validation logic
- [ ] Keep existing database transaction safety

### Gradual Enhancement
- [ ] Keep existing functionality working during migration
- [ ] Add new features incrementally
- [ ] Test each component before integration

## Expected Benefits

### Time Savings
- **Database Setup**: Save 3-5 days of database architecture work
- **Data Fetching**: Save 2-3 days of yfinance integration
- **Data Validation**: Save 1-2 days of error handling development
- **Historical Context**: Immediate access to months of historical data

### Quality Foundation
- **Proven Code**: Existing code is tested and working
- **Modern Architecture**: Current project uses best practices
- **Scalable Design**: Database schema supports PRD requirements

### Reduced Risk
- **Known Quantities**: Existing code behavior is understood
- **Incremental Development**: Lower risk than complete rewrite
- **Data Continuity**: Maintain historical data context

This evolution strategy leverages your existing investment while building toward the PRD vision efficiently.
