# Stock Performance Heatmap Dashboard - Product Requirements Document (PRD)

## Overview

This document outlines the design and requirements for an interactive heatmap dashboard application focused on financial performance metrics. The app enables users to visualize percentage change data for selected securities, either by price or relative volume, across configurable timeframes and comparison groups.

The tool may later be incorporated as a custom internal tool (e.g., for MCP Server), but the initial prototype will be developed as a standalone dashboard using a frontend framework (Streamlit).

---

## 1. Objective

To build a heatmap-based visualization tool for comparing relative performance of ETFs and equities, based on user-selected metrics (price or volume) and timeframes, with professional-grade user experience matching industry standards like Finviz.

---

## 2. Key Features & Functionality

### 2.1 Core Metrics

- **Metric Type** (selectable):
    - Price (current price vs historical price)
    - Volume (current volume vs 10-day or 3-month average volume)

### 2.2 Comparison Periods

- **Price** comparisons:
    - 1-day (previous close), 1-week, 1-month, 3-month, 6-month, YTD, 12-month
        
- **Volume** comparisons:
    - 10-day average volume (default)
    - 3-month average volume
    - Intraday adjustment factor for real-time volume comparisons

### 2.3 Asset Groups (Buckets)

User can select one of three comparison groups:
- **Country ETFs** (max: 52 tickers)
- **Sector ETFs** (max: 30 tickers)        
- **User-defined input** (default: AMZN, META, NVDA, AAPL, GOOGL, MSFT, BABA, SPY, QQQ) (max: 10 tickers)

### 2.4 Advanced Search and Filtering

- **Real-time Search**: 300ms debounce, ticker/company name/sector search
- **Fuzzy Matching**: Typo tolerance and search suggestions
- **Advanced Filters**:
  - Performance range sliders
  - Market cap categories
  - Sector/industry checkboxes
  - Volume threshold filters
  - Custom date range selection
- **Filter Persistence**: Save and share filter presets
- **Keyboard Shortcuts**: Ctrl+F, / for quick search access

---

## 3. User Experience & Interface Design

### 3.1 Default Application State

- **Metric**: Price
- **Comparison**: 1-day change
- **Bucket**: User-defined tickers

### 3.2 User Controls

- Dropdown to select metric (price or volume)
- Dropdown or buttons to choose comparison period
- Dropdown to select bucket (Country, Sector, or User-defined)
- Text input to define tickers (if User-defined selected)

### 3.3 Heatmap Visualization

#### Core Visual Elements
- **Color Encoding**: % change (gradient scale)
- **Size Options**: Market cap proportional or fixed size for clarity
- **Layout**: Inspired by Finviz with grouping headers
- **Tooltips**: Rich information overlay with ticker, full name, % change, raw values, and reference benchmark

#### Technology Implementation
- Based on Plotly Treemap (initial prototype)
- Future: enhanced layout/UX using `go.Heatmap`, `imshow`, or D3.js if needed

### 3.4 Visual Design Specifications

#### Color Scheme (Finviz Professional Standard)
```css
/* Performance Colors */
--strong-positive: #00AA00;    /* >3% gain */
--moderate-positive: #33CC33;  /* 1-3% gain */
--slight-positive: #66FF66;    /* 0-1% gain */
--neutral: #CCCCCC;            /* ±0% */
--slight-negative: #FF6666;    /* 0 to -1% loss */
--moderate-negative: #CC3333;  /* -1 to -3% loss */
--strong-negative: #AA0000;    /* <-3% loss */

/* Interface Colors */
--background-primary: #FFFFFF;
--background-secondary: #F8F9FA;
--border-color: #E0E0E0;
--text-primary: #333333;
--text-secondary: #666666;
```

#### Typography Hierarchy
```css
/* Tile Labels */
.ticker-symbol { font: bold 14px sans-serif; }
.percentage-change { font: bold 12px sans-serif; }
.additional-info { font: normal 10px sans-serif; }

/* UI Elements */
.page-title { font: bold 24px sans-serif; }
.section-header { font: 500 18px sans-serif; }
.control-label { font: normal 14px sans-serif; }
.tooltip-text { font: normal 12px sans-serif; }
```

#### Layout Specifications
```css
/* Tile Design */
.heatmap-tile {
  min-width: 80px; min-height: 60px;
  max-width: 200px; max-height: 150px;
  border-radius: 4px;
  border: 1px solid var(--border-color);
  padding: 8px; margin: 2px;
}

/* Responsive Grid */
.heatmap-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 4px; padding: 16px;
}
```

### 3.5 Interactive Behavior

#### Hover Effects
- **Visual Enhancement**: 20% white overlay, increased border width
- **Elevation**: Drop shadow (0 4px 8px rgba(0,0,0,0.1))
- **Animation**: 200ms ease-in-out transition
- **Rich Tooltips**: Extended metadata overlay

#### Click Interactions  
- **Primary Click**: Navigate to detailed view/chart
- **Right Click**: Context menu (watch, compare, etc.)
- **Double Click**: Add to comparison list
- **Keyboard Support**: Full tab navigation, Enter selection

#### Responsive Design Strategy
```css
/* Mobile (320-768px) */
- Stack tiles vertically
- Larger touch targets (minimum 44px)
- Simplified tooltips, swipe gestures

/* Tablet (768-1024px) */
- 3-4 tile columns, medium-sized tiles
- Touch-optimized controls

/* Desktop (1024px+) */
- 6-12 tile columns, full feature set
- Keyboard shortcuts, dense information display
```

---

## 4. Performance & Technical Requirements

### 4.1 Performance Standards

#### Rendering Performance
- **Initial Load**: <3 seconds for 100+ tiles
- **Filter Application**: <500ms response time
- **Smooth Animations**: 60fps for all transitions
- **Memory Usage**: <200MB additional browser memory
- **Data Refresh**: <2 seconds for new data fetch

#### Scalability Targets
- **Maximum Tiles**: Support up to 500 tiles
- **Concurrent Users**: 100+ simultaneous users
- **Data Freshness**: <15 minute data lag
- **Uptime**: 99.5% availability

### 4.2 Accessibility & Compliance

#### WCAG 2.1 AA Compliance
- **Color Contrast**: Minimum 4.5:1 ratio for all text
- **Keyboard Navigation**: Full functionality without mouse
- **Screen Reader Support**: Proper ARIA labels and descriptions
- **Focus Indicators**: Clear visual focus states
- **Alternative Formats**: High contrast and colorblind-friendly modes

#### Internationalization Support
- **Currency Support**: Multiple currency formats
- **Number Formatting**: Locale-appropriate number display
- **RTL Support**: Right-to-left language compatibility
- **Timezone Handling**: Local timezone display options

---

## 5. Data Architecture & Backend

### 5.1 Data Sources
- **Primary**: `yfinance` for real-time and historical data
- **API Methods**:
  - `.history(period='1d')`, `.info.get('previousClose')`, etc.
  - `.info.get('averageDailyVolume10Day')` and `.info.get('averageDailyVolume3Month')`

### 5.2 Intraday Volume Adjustment Table
Applied for intraday volume normalization against historical averages:

| Begin of Period | End of Period | Intraday Adjustment Factor |
|----------------|---------------|---------------------------|
| 9:30 AM | 9:44:59 AM | 0.09 |
| 9:45 AM | 9:59:59 AM | 0.14 |
| 10:00 AM | 10:14:59 AM | 0.18 |
| 10:15 AM | 10:29:59 AM | 0.21 |
| 10:30 AM | 10:59:59 AM | 0.27 |
| 11:00 AM | 11:29:59 AM | 0.38 |
| 11:30 AM | 11:59:59 AM | 0.45 |
| 12:00 PM | 12:59:59 PM | 0.52 |
| 1:00 PM | 1:59:59 PM | 0.59 |
| 2:00 PM | 2:59:59 PM | 0.68 |
| 3:00 PM | 3:29:59 PM | 0.76 |
| 3:30 PM | 3:44:59 PM | 0.78 |
| 3:45 PM | 3:59:59 PM | 0.98 |

### 5.3 Data Management Strategy

#### Caching Strategy
- **Browser Cache**: 15 minutes for price data
- **Server Cache**: 5 minutes for aggregated data
- **Historical Data**: 24 hours cache duration
- **Graceful Degradation**: When cache expires

#### Data Validation & Quality
- **Price Validation**: ±50% sanity check
- **Volume Validation**: 10x average volume alert
- **Missing Data**: Clear indicators and handling
- **Corporate Actions**: Automatic adjustments (splits, dividends)
- **Market Events**: Holiday and closure handling

#### Data Refresh Logic
- **Price Metrics**: Real-time snapshot on request
- **Volume Metrics**: End-of-day or intraday adjusted snapshot on request

#### Persistence Strategy
- **Storage Options**: SQLite (primary), local CSV backup
- **Data Schema**: ticker, timestamp, price, volume, derived % changes
- **API Optimization**: Store past query results to avoid redundant calls

---

## 6. Export & Integration Features

### 6.1 Export Capabilities
- **Image Export**: PNG/SVG formats
- **Data Export**: CSV with current view data
- **Report Generation**: PDF format
- **Sharing**: URL with filter state preservation
- **Embedding**: Code for external site integration

### 6.2 API Integration (Future)
- **Webhook Notifications**: For volume/price alerts
- **REST API**: Programmatic access
- **Portfolio Integration**: Connect with brokerage APIs
- **Social Sharing**: Platform integration capabilities

---

## 7. Implementation Roadmap

### 7.1 Priority Matrix

| Feature Category | Priority | Effort | Impact | Finviz Parity |
|-----------------|----------|---------|--------|---------------|
| Core Visualization | P0 | High | High | Essential |
| Color Scheme | P0 | Low | High | Essential |
| Hover Tooltips | P0 | Medium | High | Essential |
| Search Functionality | P1 | Medium | Medium | Important |
| Responsive Design | P1 | High | Medium | Important |
| Export Features | P2 | Medium | Low | Nice-to-have |
| Advanced Filters | P2 | High | Medium | Enhancement |
| API Integration | P3 | High | Low | Future |

### 7.2 Implementation Tasks

#### Phase 1: Core Foundation
- Create schema to store historical data (price, volume)
- Build data fetching and transformation layer
- Develop basic Streamlit UI with control panel and heatmap output
- Integrate Plotly heatmap visualization with color + tooltip logic

#### Phase 2: Enhanced Features
- Set up data refresh mechanism on user request
- Implement search and filtering capabilities
- Add responsive design and mobile optimization
- Performance optimization and caching

#### Phase 3: Advanced Features
- Export and sharing functionality
- Advanced filtering and sorting
- API integration capabilities
- Real-time updates and notifications

### 7.3 Test Cases & Validation

- Render sectors with up to 30 ETFs
- Render countries with up to 52 ETFs
- User-input group with 8–10 tickers
- Compare multiple timeframes for accuracy
- Validate intraday volume adjustments
- Performance testing with maximum data loads
- Cross-browser compatibility testing
- Accessibility compliance verification

---

## 8. Future Enhancements (Out of Scope for MVP)

- Drill-down into sectors to sub-sectors (e.g., Financials → Regional Banks)
- Real-time updating dashboard with auto-refresh
- Custom theming and branding for MCP Server integration
- Machine learning-based anomaly detection
- Advanced analytics and trend prediction
- Multi-asset class support (bonds, commodities, currencies)

---

## 9. Deployment Considerations

### 9.1 Initial Deployment
- **Platform**: Streamlit-based dashboard (frontend only)
- **Hosting**: Streamlit Cloud or similar platform
- **Database**: Local SQLite with data persistence

### 9.2 Future Scaling (MCP Server Integration)
- **Architecture**: Business logic reusable across platforms
- **Frontend**: Potential React-based replacement
- **Backend**: FastAPI or Flask serving pre-processed JSON data
- **Infrastructure**: Cloud deployment with auto-scaling

---

## 10. Technical Decisions & Open Items

### 10.1 Design Decisions
- ✓ Visual encoding for volume heatmap: Color intensity + optional size
- ✓ Percentage labels: Always visible on tiles (not just tooltips)
- ✓ Charting tool: Plotly Treemap for initial implementation

### 10.2 Implementation Decisions
- ✓ Storage format: SQLite primary, CSV backup
- ✓ Caching strategy: Browser + server-side hybrid approach
- ✓ Rate limiting: Request batching and intelligent caching for yfinance

---

## Appendix

### A.1 Reference Materials
- **Finviz Heatmap**: Visual styling and interaction inspiration
- **Default Ticker Set**: AMZN, META, NVDA, AAPL, GOOGL, MSFT, BABA, SPY, QQQ

### A.2 Technical Specifications
- **Minimum Browser Support**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Performance Benchmarks**: <3s load time, 60fps animations, <500ms interactions
- **Accessibility Standards**: WCAG 2.1 AA compliance required

---

*This PRD represents a comprehensive specification for building a world-class financial heatmap dashboard that meets or exceeds industry standards while providing unique value through enhanced volume analysis and superior user experience.*