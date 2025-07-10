# Stock Performance Heatmap Dashboard

Interactive financial visualization tool displaying stock and ETF performance through color-coded heatmaps.

## Features

- Interactive heatmaps with professional color coding
- Real-time data integration with yfinance  
- Responsive design for desktop and mobile
- Multiple asset groups: Country ETFs, Sector ETFs, custom tickers
- Performance analysis across multiple timeframes
- Volume analysis with intraday adjustments

## Quick Start

```bash
# Install dependencies
uv sync

# Run the dashboard
streamlit run streamlit_app.py
```

## Project Structure

- `src/data/` - Data fetching and database operations
- `src/config/` - Asset definitions and settings
- `data/` - SQLite database with historical data
- `streamlit_app.py` - Main dashboard application

## Development

Migrated from stock-screener project, preserving database and data fetching infrastructure.
