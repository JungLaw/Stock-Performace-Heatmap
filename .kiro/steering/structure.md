# Project Structure

## Root Level
- `streamlit_app.py` - Main application entry point
- `pyproject.toml` - Modern Python project configuration (uv/pip)
- `requirements.txt` - Legacy pip dependencies
- `README.md` - Project documentation and setup instructions
- `test_dashboard.py` - Main test suite for validation

## Source Code (`src/`)
Modular architecture with clear separation of concerns:

### `src/calculations/`
- `performance.py` - Core performance calculation logic with database integration
- `volume.py` - Volume analysis (future enhancement)

### `src/visualization/`
- `heatmap.py` - Plotly treemap implementation with Finviz styling
- `components.py` - Reusable UI components

### `src/config/`
- `assets.py` - Asset group definitions (Country ETFs, Sector ETFs, Custom tickers)
- `settings.py` - Application configuration and constants

### `src/data/`
- `fetcher.py` - Data fetching from Yahoo Finance API
- `processor.py` - Data transformation and cleaning
- `cache.py` - Caching logic and database operations

## Data Storage (`data/`)
- `stock_data.db` - SQLite database for cached historical prices

## Documentation (`docs/`)
- `README.md` - Documentation index
- `planning/` - Project requirements and planning documents
- `migration/` - Migration history and guides

## Scripts (`scripts/`)
Utility scripts for maintenance and debugging:
- `inspect_database.py` - Database inspection tool
- `verify_data.py` - Data integrity validation
- `debug_xlc.py` - Specific debugging utilities
- `compare_sources.py` - Data source comparison
- `sql_delete_by_date.py` - Database cleanup

## Tests (`tests/`)
- `test_performance_fix.py` - Performance-specific tests
- `__pycache__/` - Python bytecode cache

## Reference Materials (`_references/`)
- Historical versions and development notes
- `constraints.md` - Development constraints and guidelines
- `notebooks/` - Jupyter notebooks for analysis
- `previous_versions/` - Legacy code and migration artifacts

## Conventions
- **Import Pattern**: Add `src/` to Python path in main files
- **Database Location**: Always use `data/stock_data.db` for SQLite
- **Asset Groups**: Defined in `src/config/assets.py` with display names
- **Error Handling**: Graceful degradation with user-friendly messages
- **Session State**: Prefix Streamlit session variables with descriptive names
- **Color Scheme**: Use Finviz-inspired colors defined in `src/config/settings.py`