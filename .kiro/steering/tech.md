# Technology Stack

## Core Technologies
- **Python 3.12+**: Primary programming language
- **Streamlit 1.28+**: Web framework for the dashboard interface
- **Plotly 6.1+**: Interactive visualization library for treemap heatmaps
- **Pandas 2.3+**: Data manipulation and analysis
- **yfinance 0.2.63+**: Yahoo Finance API for real-time market data
- **SQLite**: Local database for caching historical price data

## Key Dependencies
- **NumPy**: Numerical computations
- **cachetools**: In-memory caching for API responses
- **requests**: HTTP client for API calls
- **python-dotenv**: Environment variable management

## Development Tools
- **pytest**: Testing framework
- **uv**: Python package manager (pyproject.toml)
- **Git**: Version control

## Common Commands

### Environment Setup
```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# OR using uv
uv sync
```

### Running the Application
```bash
# Start the dashboard
streamlit run streamlit_app.py

# Run tests
python test_dashboard.py
# OR
pytest tests/
```

### Development
```bash
# Check database contents
python scripts/inspect_database.py

# Verify data integrity
python scripts/verify_data.py

# Debug specific issues
python scripts/debug_xlc.py
```

## Architecture Patterns
- **Modular Design**: Separated concerns into src/ subdirectories
- **Database-First Caching**: Prioritize cached data over API calls
- **Session State Management**: Streamlit session state for UI persistence
- **Error Handling**: Graceful degradation when data unavailable
- **Progress Tracking**: User feedback during data fetching operations