# Stock Performance Heatmap Dashboard 📈

A professional Finviz-style interactive heatmap dashboard for visualizing stock and ETF performance across different time periods and asset groups.

![Dashboard Status](https://img.shields.io/badge/Status-MVP%20Complete-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

## 🎯 Features

### ✅ Core Functionality
- **📊 Interactive Heatmaps**: Finviz-style treemap visualizations with professional color coding
- **📅 Multiple Time Periods**: 1 Day, 1 Week, 1 Month, 3 Months, 6 Months, YTD, 1 Year
- **🎯 Asset Groups**: Pre-configured Country ETFs (52), Sector ETFs (30), Custom tickers
- **💹 Real-time Data**: Live market data via Yahoo Finance (yfinance)
- **📋 Rich Tooltips**: Detailed hover information with prices and percentage changes
- **📈 Summary Statistics**: Performance overview with best/worst performers
- **📊 Data Tables**: Sortable detailed data export

### 🎨 Professional Design
- **🎨 Finviz Color Scheme**: Exact color matching with professional gradients
- **📱 Responsive Layout**: Works on desktop, tablet, and mobile
- **⚡ Performance Optimized**: Fast loading with progress indicators
- **🔄 Real-time Updates**: Refresh data on demand

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Virtual environment (recommended)

### Installation

1. **Clone/Navigate to the project**:
   ```bash
   cd C:\\Users\\lawre\\Projects\\stock-heatmap-dashboard
   ```

2. **Activate virtual environment**:
   ```bash
   # Windows
   .venv\\Scripts\\activate
   
   # Linux/Mac  
   source .venv/bin/activate
   ```

3. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**:
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📱 How to Use

### 1. Select Asset Group
- **Country ETFs**: 52 major country and regional ETFs
- **Sector ETFs**: 30 major sector and thematic ETFs  
- **Custom Tickers**: Enter your own stock/ETF symbols

### 2. Choose Time Period
- **1 Day**: Compare vs previous close
- **1 Week**: 7-day performance
- **1 Month**: 30-day performance
- **3 Months**: Quarterly performance
- **6 Months**: Semi-annual performance
- **YTD**: Year-to-date from January 1st
- **1 Year**: 12-month performance

### 3. Refresh Data
Click the "🔄 Refresh Data" button to fetch the latest market data.

### 4. Analyze Results
- **Color Coding**: Green = gains, Red = losses, Gray = neutral
- **Hover Tooltips**: Detailed price and change information
- **Summary Stats**: Overview of performance distribution
- **Data Table**: Sortable detailed view

## 🎨 Color Legend

| Performance Range | Color | Description |
|------------------|-------|-------------|
| > +3% | ![#00AA00](https://via.placeholder.com/15/00AA00/000000?text=+) Strong Gain | Bright Green |
| +1% to +3% | ![#33CC33](https://via.placeholder.com/15/33CC33/000000?text=+) Moderate Gain | Medium Green |
| 0% to +1% | ![#66FF66](https://via.placeholder.com/15/66FF66/000000?text=+) Slight Gain | Light Green |
| 0% | ![#CCCCCC](https://via.placeholder.com/15/CCCCCC/000000?text=+) Neutral | Gray |
| 0% to -1% | ![#FF6666](https://via.placeholder.com/15/FF6666/000000?text=+) Slight Loss | Light Red |
| -1% to -3% | ![#CC3333](https://via.placeholder.com/15/CC3333/000000?text=+) Moderate Loss | Medium Red |
| < -3% | ![#AA0000](https://via.placeholder.com/15/AA0000/000000?text=+) Strong Loss | Dark Red |

## 🏗️ Project Structure

```
stock-heatmap-dashboard/
├── src/
│   ├── calculations/
│   │   ├── performance.py      # Price change calculations
│   │   └── volume.py          # Volume analysis (future)
│   ├── visualization/
│   │   ├── heatmap.py         # Plotly treemap implementation
│   │   └── components.py      # UI components
│   ├── config/
│   │   ├── assets.py          # Asset group definitions
│   │   └── settings.py        # App configuration
│   └── data/
│       ├── fetcher.py         # Data fetching from APIs
│       ├── processor.py       # Data transformation
│       └── cache.py           # Caching logic
├── docs/
│   └── planning/              # Project documentation
├── data/                      # Local data storage
├── streamlit_app.py          # Main application
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## 🔧 Technical Details

### Technology Stack
- **Frontend**: Streamlit (Python-based web framework)
- **Visualization**: Plotly (interactive charts)
- **Data Source**: Yahoo Finance via yfinance
- **Storage**: SQLite + CSV (local storage)
- **Dependencies**: Pandas, NumPy, requests

### Performance Features
- **Caching**: Intelligent API call optimization
- **Progress Tracking**: Real-time loading indicators
- **Error Handling**: Graceful failure management
- **Responsive Design**: Mobile-friendly interface

### Data Sources
- **Primary**: Yahoo Finance (yfinance library)
- **Update Frequency**: On-demand refresh
- **Historical Data**: Up to 1 year lookback
- **Coverage**: All major stocks, ETFs, and indices

## 📊 Asset Groups

### Country ETFs (52 tickers)
Major country and regional ETFs including:
- **Developed Markets**: VTI, VEA, VGK, EWJ, EWU, EWG, etc.
- **Emerging Markets**: VWO, EEM, INDA, EWZ, EWT, etc.
- **Regional**: VPL, EPP, etc.

### Sector ETFs (30 tickers)
Major sector and thematic ETFs including:
- **SPDR Sectors**: XLF, XLK, XLE, XLV, XLI, XLP, XLY, XLU, etc.
- **Technology**: SMH, SOXX, SKYY, HACK, etc.
- **Thematic**: ARKK, ICLN, ROBO, etc.

### Custom Tickers
Default includes: AMZN, META, NVDA, AAPL, GOOGL, MSFT, BABA, SPY, QQQ
- Add your own symbols (up to 10 for optimal performance)
- Supports all major exchanges

## 🧪 Testing

Run the test suite to validate installation:

```bash
python test_dashboard.py
```

Expected output:
```
🧪 Running Dashboard Tests
================================
✅ All tests passed! Dashboard is ready to run.
💡 Run 'streamlit run streamlit_app.py' to start the dashboard
```

## 🚀 Next Steps / Roadmap

### Phase 2 Enhancements (Future)
- [ ] **Volume Analysis**: Relative volume vs average with intraday adjustments  
- [ ] **Market Cap Sizing**: Tile sizes proportional to market capitalization
- [ ] **Export Features**: PDF reports, CSV data export
- [ ] **Advanced Filters**: Custom date ranges, performance filters
- [ ] **Real-time Updates**: Auto-refresh capabilities

### Phase 3 Advanced Features (Future)
- [ ] **Portfolio Integration**: Connect with brokerage APIs
- [ ] **Alerting System**: Email/SMS notifications for performance thresholds
- [ ] **Technical Indicators**: RSI, MACD, moving averages
- [ ] **Sector Drill-down**: Hierarchical sector analysis
- [ ] **API Access**: REST API for programmatic access

## 📚 Documentation

- **PRD**: `docs/planning/PRD.md` - Complete product requirements
- **Planning**: `docs/planning/PLANNING.md` - Project strategy and architecture  
- **Tasks**: `docs/planning/TASKS.md` - Development progress tracking

## 🤝 Contributing

1. **Development Environment**: Follow installation steps above
2. **Code Style**: Use Black for Python formatting
3. **Testing**: Run test suite before committing
4. **Documentation**: Update docs for new features

## 📝 License

This project is for internal use and development purposes.

## 🆘 Support

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated
2. **Data Fetch Errors**: Check internet connection and try again
3. **Performance Issues**: Limit custom tickers to 10 or fewer
4. **Display Issues**: Try refreshing the browser page

### Getting Help

1. **Test the installation**: Run `python test_dashboard.py`
2. **Check logs**: Look for error messages in the terminal
3. **Restart**: Try restarting the Streamlit server

---

**Built with ❤️ using Streamlit and Plotly | Data provided by Yahoo Finance**

*Last updated: July 2025*
