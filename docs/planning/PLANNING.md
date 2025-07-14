# Stock Performance Heatmap Dashboard - Project Planning

## Executive Summary

This project aims to build an interactive financial heatmap dashboard that visualizes stock and ETF performance metrics using color-coded treemaps. The tool will enable users to compare securities across different timeframes and metrics (price changes and relative volume), providing institutional-quality analysis capabilities in an intuitive visual format.

### 🏆 MAJOR MILESTONE: CORE MVP COMPLETED (July 2025)
**Achievement**: Functional Finviz-style heatmap dashboard with professional visualization

#### ✅ Core Features Delivered:
- **Infrastructure**: Complete modular project structure with src/ organization
- **Performance Calculations**: Full implementation of price change calculations across all time periods (1D to 1Y, YTD)
- **Heatmap Visualization**: Professional Finviz-style treemap with exact color matching and rich tooltips
- **Interactive UI**: Complete Streamlit dashboard with sidebar controls, progress tracking, and data tables
- **Asset Groups**: Pre-configured Country ETFs (52), Sector ETFs (30), and Custom ticker support
- **Data Integration**: Real-time yfinance integration with error handling
- **Documentation**: Comprehensive README, updated planning docs, test suite

#### 🚨 Critical Issues Identified:
1. **Database Integration Gap**: PerformanceCalculator bypasses 19K+ cached records, calls yfinance directly
2. **Limited Ticker Management**: Basic text input instead of flexible multi-level ticker selection

#### 🎯 Next Phase Priority:
1. **Database-First Performance Calculator**: Fix caching to use SQLite before yfinance
2. **Enhanced Ticker Management UI**: Three-level selection system (checkboxes + permanent additions + session custom)

## High-Level Direction & Vision

### Core Value Proposition
- **Visual Performance Analysis**: Transform complex numerical data into instantly interpretable visual patterns
- **Comparative Intelligence**: Enable side-by-side comparison of multiple securities with configurable groupings
- **Real-time Insights**: Provide current market data with historical context for informed decision-making
- **Flexibility**: Support multiple metrics, timeframes, and asset groupings for diverse analytical needs

### Target Use Cases
1. **Portfolio Performance Review**: Quick assessment of holdings vs market segments
2. **Sector Rotation Analysis**: Identify hot/cold sectors and country allocations
3. **Volume Anomaly Detection**: Spot unusual trading activity that may signal opportunities
4. **Risk Assessment**: Visual identification of concentration risks and correlations

## Project Scope & Boundaries

### In Scope (MVP)
- Interactive heatmap visualization with Plotly treemaps
- Price performance analysis (1D to 12M periods)
- Relative volume analysis (vs 10D/3M averages)
- Three predefined asset groups: Country ETFs, Sector ETFs, Custom tickers
- Real-time data integration via yfinance
- Responsive web interface with Streamlit
- Intraday volume adjustment calculations
- Basic data persistence for API call optimization

### Out of Scope (Future Phases)
- Real-time streaming updates
- Advanced technical indicators beyond price/volume
- Portfolio integration and position tracking
- Alert systems and notifications
- Custom themes and white-labeling
- Mobile native applications
- Advanced authentication/user management

### Success Metrics
- **Functionality**: All predefined asset groups render correctly
- **Performance**: Dashboard loads in <3 seconds for 50+ securities
- **Accuracy**: Price/volume calculations match reference sources
- **Usability**: Users can navigate between views without documentation

## Technology Stack & Architecture

### Frontend Framework
**Streamlit** - Selected for rapid prototyping and built-in interactivity
- **Pros**: Fast development, native Python integration, good component ecosystem
- **Cons**: Limited customization, potential performance constraints at scale
- **Alternative considered**: Dash (more flexible but steeper learning curve)

### Visualization Library
**Plotly** - Primary choice for interactive charts
- **Treemap**: Main visualization for performance heatmaps
- **Heatmap**: Alternative layout for different data structures
- **Built-in interactivity**: Hover tooltips, zoom, click events

### Data Layer
**Primary Source**: yfinance API
- Real-time and historical price data
- Volume metrics and averages
- Company/ETF metadata

**Data Storage**: SQLite + CSV hybrid approach
- SQLite for structured queries and relationships
- CSV for bulk data exports and backups
- Local storage initially, cloud migration path planned

### Backend Architecture
```
├── Data Layer
│   ├── yfinance API integration
│   ├── SQLite database (metadata, cache)
│   └── CSV storage (bulk data)
├── Business Logic
│   ├── Performance calculations
│   ├── Volume adjustments
│   └── Data transformation
├── Presentation Layer
│   ├── Streamlit UI components
│   ├── Plotly visualizations
│   └── User controls
└── Configuration
    ├── Asset group definitions
    ├── Time period mappings
    └── Display settings
```

## Risk Assessment & Mitigation

### Technical Risks
1. **API Rate Limits (yfinance)** - PARTIALLY MITIGATED
   - *Current Status*: PerformanceCalculator bypasses database cache, making unnecessary API calls
   - *Mitigation*: Implement database-first approach to leverage 19K+ cached records
   - *Impact*: 89% API call reduction for cached tickers
   
2. **Data Quality Issues** - MITIGATED
   - *Mitigation*: Data validation, error handling, manual override capabilities
   - *Status*: Implemented in current calculator
   
3. **Performance with Large Datasets** - MITIGATED
   - *Mitigation*: Lazy loading, data sampling, progressive rendering
   - *Status*: Current implementation handles 52 tickers efficiently

### Business Risks
1. **User Adoption** - ADDRESSED
   - *Status*: Professional Finviz-quality UI implemented
   - *Mitigation*: Comprehensive documentation, intuitive design
   
2. **Changing Requirements** - MANAGED  
   - *Status*: Modular architecture enables flexible enhancements
   - *Next*: Enhanced ticker management for user customization

### Data Risks
1. **Market Data Accuracy** - MANAGED
   - *Mitigation*: yfinance validation, clear disclaimers, error handling
   - *Status*: Implemented with graceful degradation
   
2. **Historical Data Preservation** - CRITICAL
   - *Status*: 19K+ records in SQLite database must be preserved
   - *Risk*: Current implementation doesn't leverage this valuable cache

## Critical Technical Decisions Made (July 2025)

### Database Integration Strategy
**Decision**: Database-first approach for historical data
**Rationale**: Leverage existing 19K+ cached records, reduce API calls
**Implementation Pattern**:
```python
def get_historical_price(ticker, date):
    1. Check database for ticker + date
    2. If found: return cached price (no API call)
    3. If missing: fetch from yfinance
    4. Auto-save fetched data to database
    5. Return price
```

### Data Persistence Strategy
**Historical Data**: Cache permanently in SQLite (never changes once market closes)
**Current Prices**: Fetch fresh from yfinance (real-time needed)
**New Daily Closes**: Save to database next day (complete volume data)
**Rationale**: Current volume incomplete during trading hours

### UI Architecture Decision
**Three-Level Ticker Management**:
1. **Level 1**: Checkbox selection from predefined ETF lists
2. **Level 2**: Add new tickers to permanent predefined lists (persistent)
3. **Level 3**: Session-only custom tickers (temporary analysis)
**Rationale**: Maximum flexibility while maintaining clean predefined collections

## Development Approach

### Phase 1: Core Infrastructure (Weeks 1-2)
- Set up development environment
- Implement basic data fetching
- Create foundational UI structure
- Basic price performance calculations

### Phase 2: Visualization Engine (Weeks 3-4)
- Plotly treemap integration
- Interactive controls implementation
- Tooltip and hover functionality
- Color scheme and sizing logic

### Phase 3: Advanced Features (Weeks 5-6)
- Volume analysis and adjustments
- Data persistence layer
- Error handling and validation
- Performance optimization

### Phase 4: Polish & Testing (Week 7)
- User interface refinements
- Comprehensive testing
- Documentation
- Deployment preparation

## Resource Requirements

### Development Team
- **Primary Developer**: Full-stack development, data analysis
- **Optional**: UI/UX consultant for design refinements
- **Testing**: End-user validation (financial analysts)

### Infrastructure
- **Development**: Local environment with Python 3.9+
- **Deployment**: Streamlit Cloud or similar hosting platform
- **Data**: Internet connection for API access
- **Storage**: Minimal local storage requirements (<1GB)

### Dependencies
```python
# Core libraries
streamlit>=1.28.0
plotly>=5.15.0
pandas>=2.0.0
yfinance>=0.2.0

# Data processing
numpy>=1.24.0
sqlite3 (built-in)

# Optional enhancements
requests>=2.31.0
cachetools>=5.3.0
```

## Quality Assurance Strategy

### Testing Approach
1. **Unit Tests**: Core calculation functions
2. **Integration Tests**: API connectivity and data flow
3. **User Acceptance Tests**: Real-world scenarios with sample users
4. **Performance Tests**: Load testing with maximum data sets

### Code Quality
- Type hints for all functions
- Comprehensive docstrings
- Code formatting with Black
- Linting with pylint/flake8
- Git hooks for pre-commit checks

### Monitoring
- Error logging and tracking
- Performance metrics collection
- User interaction analytics
- Data quality monitoring

## Future Evolution Path

### Phase 2 Enhancements
- Additional asset classes (commodities, currencies, bonds)
- Custom calculation periods
- Portfolio integration
- Export capabilities (PDF, Excel)

### Phase 3 Scaling
- Multi-user support
- Custom dashboards
- Advanced analytics
- API development for external integration

### Technical Evolution
- Migration to React frontend for enhanced UX
- Microservices architecture for scalability
- Real-time data streaming
- Machine learning insights integration

This planning document provides the strategic foundation for building a robust, scalable financial heatmap dashboard that can evolve with user needs and technical requirements.
