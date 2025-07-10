# Performance Heatmap Dashboard - Product Requirements Document (PRD)

## Overview

This document outlines the design and requirements for an interactive heatmap dashboard application focused on financial performance metrics. The app enables users to visualize percentage change data for selected securities, either by price or relative volume, across configurable timeframes and comparison groups.

The tool may later be incorporated as a custom internal tool (e.g., for MCP Server), but the initial prototype will be developed as a standalone dashboard using a frontend framework (e.g., Streamlit or Dash).

---

## 1. Objective

To build a heatmap-based visualization tool for comparing relative performance of ETFs and equities, based on user-selected metrics (price or volume) and timeframes.

---

## 2. Key Features

### Metrics

- **Metric Type** (selectable):
    
    - Price (current price vs historical price)
    - Volume (current volume vs 10-day or 3-month average volume)
        

### Comparison Periods

- **Price** comparisons:
    
    - 1-day (previous close)
    - 1-week
    - 1-month
    - 3-month
    - 6-month
    - YTD
    - 12-month
        
- **Volume** comparisons:
    
    - 10-day average volume (default)
    - 3-month average volume
    - Intraday adjustment factor for real-time volume comparisons
        

### Buckets

- User can select one of three comparison groups:
    
    - **Country ETFs** (max: 52 tickers)
    - **Sector ETFs** (max: 30 tickers)
        
    - **User-defined input** (default: AMZN, META, NVDA, AAPL, GOOGL, MSFT, BABA, SPY, QQQ) (max: 10 tickers)
        

### Visualization

- Interactive heatmap:
    
    - **Color**: % change (gradient scale)
    - **Size**: or fixed size for clarity
    - **X-axis**: Ticker
    - **Y-axis**: Metric type or comparison period (contextual)
        
    - **Tooltips**: Show ticker, full name, % change, raw values, and reference benchmark
        
- Layout inspired by Finviz:
    
    - Grouping headers (e.g., US Sector, Global, etc.)
    - Hover tooltips
    - Button/dropdown filters on sidebar
        

---

## 3. UI/UX Design

- **Default View**:
    
    - Metric: Price
    - Comparison: 1-day change
    - Bucket: User-defined tickers
        
- **Controls**:
    
    - Dropdown to select metric (price or volume)
    - Dropdown or buttons to choose comparison period
    - Dropdown to select bucket (Country, Sector, or User-defined)
    - Text input to define tickers (if User-defined selected)
        
- **Heatmap Style**:
    
    - Based on Plotly Treemap (initial prototype)
    - Future: enhanced layout/UX using `go.Heatmap`, `imshow`, or D3.js if needed
        

---

## 4. Data & Backend

- **Data Source**:
    - Primarily `yfinance` for real-time and historical data
    - Uses:
        
        - `.history(period='1d')`, `.info.get('previousClose')`, etc.
            
        - `.info.get('averageDailyVolume10Day')` and `.info.get('averageDailyVolume3Month')`
            
- **Intraday Volume Adjustment Table**:  
    Applied for intraday volume normalization against historical averages
    
|BoP|EoP|Intraday Adjustment Factor|
|---|---|---|
|9:30 AM|9:44:59 AM|0.09|
|9:45 AM|9:59:59 AM|0.14|
|10:00 AM|10:14:59 AM|0.18|
|10:15 AM|10:29:59 AM|0.21|
|10:30 AM|10:59:59 AM|0.27|
|11:00 AM|11:29:59 AM|0.38|
|11:30 AM|11:59:59 AM|0.45|
|12:00 PM|12:59:59 PM|0.52|
|1:00 PM|1:59:59 PM|0.59|
|2:00 PM|2:59:59 PM|0.68|
|3:00 PM|3:29:59 PM|0.76|
|3:30 PM|3:44:59 PM|0.78|
|3:45 PM|3:59:59 PM|0.98|

	
- **Data Refresh Logic**:
    
    - Price metrics: real-time snapshot on request
        
    - Volume metrics: end-of-day or intraday adjusted snapshot on request
        
- **Persistence**:
    
    - Plan to store past query results to avoid redundant API calls
        
    - Options: local CSV storage, SQLite, or cloud storage
        
    - CSV format TBD, but must include: ticker, timestamp, price, volume, derived % changes, etc.
        

---

## 5. Future Enhancements (Out of Scope for MVP)
- Drill-down into sectors to sub-sectors (e.g., Financials -> Regional Banks)
- Real-time updating dashboard with auto-refresh
- Custom theming and branding for MCP Server integration
    

---

## 6. Deployment Considerations

- **Initial App**: Streamlit-based dashboard (frontend only)
- **Future Internal Tool (MCP Server)**:
    
    - Business logic (data fetching, transformation) can be reused
    - Streamlit UI may be replaced by custom React-based frontend
    - Backend services (e.g., FastAPI or Flask) may serve pre-processed JSON data
        

---

## 7. Open Items & Actionable Next Steps

### ❓ Design Decisions

-  Finalize visual encoding for volume heatmap (e.g., size based on rel. vol?)
    
-  Do we include % labels on each heatmap cell?
    

### ⚙️ Technical Decisions

-  Format for CSV storage (schema for storing past requests)
-  Choose charting tool: Plotly Treemap vs Heatmap
-  Whether to cache fetched data by ticker + timestamp
-  Strategy to handle rate limits from yfinance (if any)
    

### 📌 Implementation Tasks

-  Create schema to store historical data (price, volume)
-  Build data fetching and transformation layer
-  Develop basic Streamlit UI with control panel and heatmap output
-  Integrate Plotly heatmap visualization with color + tooltip logic
-  Set up data refresh mechanism on user request
    

### 📈 Test Cases

-  Render sectors with up to 30 ETFs
-  Render countries with up to 52 ETFs
-  User-input group with 8–10 tickers
-  Compare multiple timeframes for accuracy
-  Validate intraday volume adjustments
    

---

## Appendix

- **Finviz Screenshot Reference**: Provided by user (visual styling inspiration)
    
- **Default Ticker Set**: AMZN, META, NVDA, AAPL, GOOGL, MSFT, BABA, SPY, QQQ