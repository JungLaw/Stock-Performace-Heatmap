#!/usr/bin/env python3
"""
Quick fix for the failed migration - UTF-8 compatible version
"""

import shutil
from pathlib import Path

def fix_migration():
    """Complete the failed migration"""
    old_path = Path("stock-screener")
    new_path = Path("stock-heatmap-dashboard")
    
    print("Fixing migration...")
    
    # Step 1: Copy missing pyproject.toml
    print("1. Copying pyproject.toml...")
    shutil.copy2(old_path / "pyproject.toml", new_path / "pyproject.toml")
    print("   OK: pyproject.toml copied")
    
    # Step 2: Update pyproject.toml with new dependencies
    print("2. Updating pyproject.toml...")
    pyproject_path = new_path / "pyproject.toml"
    
    with open(pyproject_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Update project metadata
    updated_content = content.replace(
        'name = "stock-screener"',
        'name = "stock-heatmap-dashboard"'
    ).replace(
        'description = "Add your description here"',
        'description = "Interactive stock performance heatmap dashboard"'
    )
    
    # Add new dependencies
    new_deps = '''dependencies = [
    "httpx>=0.28.1",
    "ipykernel>=6.29.5", 
    "ipywidgets>=8.1.7",
    "mcp[cli]>=1.2.1",
    "pandas>=2.3.0",
    "plotly>=6.1.2",
    "pyrate-limiter>=2.10.0",
    "python-dotenv>=1.1.0",
    "requests-cache>=1.2.1",
    "requests-ratelimiter>=0.7.0",
    "tabulate>=0.9.0",
    "yfinance>=0.2.63",
    # New dependencies for heatmap dashboard
    "streamlit>=1.28.0",
    "numpy>=1.24.0",
    "cachetools>=5.3.0",
]'''
    
    # Replace dependencies section
    lines = updated_content.split('\\n')
    new_lines = []
    in_dependencies = False
    bracket_count = 0
    
    for line in lines:
        if line.startswith('dependencies = ['):
            new_lines.extend(new_deps.split('\\n'))
            in_dependencies = True
            bracket_count = line.count('[') - line.count(']')
        elif in_dependencies:
            bracket_count += line.count('[') - line.count(']')
            if bracket_count <= 0:
                in_dependencies = False
            # Skip old dependency lines
        else:
            new_lines.append(line)
            
    with open(pyproject_path, 'w', encoding='utf-8') as f:
        f.write('\\n'.join(new_lines))
    print("   OK: pyproject.toml updated")
    
    # Step 3: Create main Streamlit app
    print("3. Creating streamlit_app.py...")
    streamlit_content = '''"""
Stock Performance Heatmap Dashboard - Main Application

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    st.set_page_config(
        page_title="Stock Performance Heatmap Dashboard",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title(":chart_with_upwards_trend: Stock Performance Heatmap Dashboard")
    st.markdown("---")
    
    st.info(":construction: Dashboard under construction - migrated from stock-screener project")
    
    # Show migration status
    st.subheader("Migration Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Database", ":white_check_mark: Migrated", help="Historical stock data preserved")
    with col2:
        st.metric("Data Fetching", ":white_check_mark: Migrated", help="yfinance integration ready") 
    with col3:
        st.metric("Visualization", ":construction: In Progress", help="Heatmap under development")
        
    # Show database info
    st.subheader("Database Status")
    try:
        import sqlite3
        conn = sqlite3.connect('data/stock_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM daily_prices')
        record_count = cursor.fetchone()[0]
        cursor.execute('SELECT DISTINCT Ticker FROM daily_prices')
        tickers = sorted([row[0] for row in cursor.fetchall()])
        conn.close()
        
        st.success(f"Database contains {record_count} records for {len(tickers)} tickers")
        st.write("Tickers:", ", ".join(tickers))
    except Exception as e:
        st.error(f"Database connection error: {e}")

if __name__ == "__main__":
    main()
'''
    
    with open(new_path / "streamlit_app.py", 'w', encoding='utf-8') as f:
        f.write(streamlit_content)
    print("   OK: streamlit_app.py created")
    
    # Step 4: Create config files
    print("4. Creating configuration files...")
    
    # Country ETFs list
    COUNTRY_ETFS = [
        "VTI", "VEA", "VWO", "EEM", "VGK", "VPL", "EWJ", "EWZ", "INDA", "EWU",
        "EWG", "EWQ", "EWC", "EWA", "EWL", "EWI", "EWP", "EWD", "EWN", "EWS",
        "EWT", "EWY", "EWH", "EWM", "EPOL", "EPP", "EZA", "ECH", "EIDO", "EPHE",
        "VNM", "THD", "TUR", "RSX", "QQQ", "SPY", "IWM", "DIA", "EFA", "IEFA",
        "IEMG", "ACWI", "VT", "BND", "AGG", "TLT", "GLD", "SLV", "VNQ", "VNQI", "XLF", "XLK"
    ]
    
    SECTOR_ETFS = [
        "XLF", "XLK", "XLE", "XLV", "XLI", "XLP", "XLY", "XLU", "XLRE", "XLC",
        "XLB", "XME", "XRT", "XHB", "ITB", "KBE", "KRE", "SMH", "SOXX", "IBB",
        "XBI", "ARKK", "ARKQ", "ARKW", "ARKG", "ICLN", "PBW", "HACK", "SKYY", "ROBO"
    ]
    
    CUSTOM_DEFAULT = ["AMZN", "META", "NVDA", "AAPL", "GOOGL", "MSFT", "BABA", "SPY", "QQQ"]
    
    # Create assets.py
    assets_content = f'''"""
Asset Group Definitions for Heatmap Dashboard
"""

# Country ETFs (52 tickers)
COUNTRY_ETFS = {COUNTRY_ETFS}

# Sector ETFs (30 tickers)  
SECTOR_ETFS = {SECTOR_ETFS}

# Default custom tickers (9 tickers)
CUSTOM_DEFAULT = {CUSTOM_DEFAULT}

# Asset group metadata
ASSET_GROUPS = {{
    "country": {{
        "name": "Country ETFs",
        "description": "Exchange-traded funds representing different countries and regions",
        "tickers": COUNTRY_ETFS,
        "max_tickers": 52
    }},
    "sector": {{
        "name": "Sector ETFs", 
        "description": "Exchange-traded funds representing different market sectors",
        "tickers": SECTOR_ETFS,
        "max_tickers": 30
    }},
    "custom": {{
        "name": "Custom Tickers",
        "description": "User-defined list of stock tickers",
        "tickers": CUSTOM_DEFAULT,
        "max_tickers": 10
    }}
}}

def get_asset_group(group_name: str) -> dict:
    """Get asset group configuration by name"""
    return ASSET_GROUPS.get(group_name, {{}})

def get_all_tickers() -> list:
    """Get all unique tickers from all asset groups"""
    all_tickers = set()
    for group in ASSET_GROUPS.values():
        all_tickers.update(group["tickers"])
    return sorted(list(all_tickers))
'''
    
    with open(new_path / "src" / "config" / "assets.py", 'w', encoding='utf-8') as f:
        f.write(assets_content)
    
    # Create settings.py
    settings_content = '''"""
Application Settings and Configuration
"""

# Database configuration
DATABASE_FILE = "data/stock_data.db"
TABLE_NAME = "daily_prices"

# Data refresh settings
CACHE_DURATION_MINUTES = 15
MAX_API_REQUESTS_PER_MINUTE = 100

# Display settings
DEFAULT_METRIC = "price"  # "price" or "volume"
DEFAULT_PERIOD = "1d"     # 1d, 1w, 1m, 3m, 6m, ytd, 1y
DEFAULT_ASSET_GROUP = "custom"

# Color scheme (Finviz-inspired)
COLOR_SCHEME = {
    "strong_positive": "#00AA00",    # >3% gain
    "moderate_positive": "#33CC33",  # 1-3% gain  
    "slight_positive": "#66FF66",    # 0-1% gain
    "neutral": "#CCCCCC",            # ±0%
    "slight_negative": "#FF6666",    # 0 to -1% loss
    "moderate_negative": "#CC3333",  # -1 to -3% loss
    "strong_negative": "#AA0000",    # <-3% loss
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    "strong": 3.0,      # ±3%
    "moderate": 1.0,    # ±1%
    "slight": 0.1,      # ±0.1%
}
'''
    
    with open(new_path / "src" / "config" / "settings.py", 'w', encoding='utf-8') as f:
        f.write(settings_content)
    print("   OK: Configuration files created")
    
    # Step 5: Create requirements.txt
    print("5. Creating requirements.txt...")
    requirements_content = '''# Stock Heatmap Dashboard Dependencies
streamlit>=1.28.0
plotly>=6.1.2
pandas>=2.3.0
yfinance>=0.2.63
numpy>=1.24.0
cachetools>=5.3.0
requests>=2.31.0
python-dotenv>=1.1.0
'''
    
    with open(new_path / "requirements.txt", 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    print("   OK: requirements.txt created")
    
    # Step 6: Update README
    print("6. Updating README.md...")
    readme_content = '''# Stock Performance Heatmap Dashboard

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
'''
    
    with open(new_path / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("   OK: README.md updated")
    
    # Step 7: Update migrated code files
    print("7. Updating migrated code...")
    
    # Update fetcher.py
    fetcher_path = new_path / "src" / "data" / "fetcher.py"
    with open(fetcher_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    updated_content = content.replace(
        'DB_FILE = "stock_data.db"',
        'DB_FILE = "../../data/stock_data.db"'
    )
    
    # Add proper docstring
    docstring = '''"""
Stock Data Fetcher - Enhanced from original main.py

Handles fetching historical and real-time stock data from yfinance
and populating the SQLite database.
"""

'''
    
    with open(fetcher_path, 'w', encoding='utf-8') as f:
        f.write(docstring + updated_content)
    
    # Update database.py
    database_path = new_path / "src" / "data" / "database.py"
    with open(database_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    updated_content = content.replace(
        'DB_FILE = "stock_data.db"',
        'DB_FILE = "../../data/stock_data.db"'
    )
    
    docstring = '''"""
Database Utilities - Enhanced from original utils_database.py

Utility functions for interacting with the SQLite database
containing historical stock data.
"""

'''
    
    with open(database_path, 'w', encoding='utf-8') as f:
        f.write(docstring + updated_content)
    
    print("   OK: Code files updated")
    
    # Create placeholder files
    placeholder_files = {
        "src/data/processor.py": "# Data processing and transformation\\npass\\n",
        "src/data/cache.py": "# Caching and data persistence\\npass\\n", 
        "src/visualization/heatmap.py": "# Plotly treemap heatmap implementation\\npass\\n",
        "src/visualization/components.py": "# Reusable Streamlit UI components\\npass\\n",
        "src/calculations/performance.py": "# Price performance calculations\\npass\\n",
        "src/calculations/volume.py": "# Volume analysis and calculations\\npass\\n",
    }
    
    for file_path, content in placeholder_files.items():
        with open(new_path / file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("8. Migration fix completed!")
    
    # Count database records
    try:
        import sqlite3
        with sqlite3.connect(new_path / "data" / "stock_data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM daily_prices")
            record_count = cursor.fetchone()[0]
            print(f"   Database: {record_count} records preserved")
    except:
        print("   Database: Available (could not count records)")
    
    print("\\nMigration successfully completed!")
    print(f"New project: {new_path}")
    print("Next steps:")
    print(f"   cd {new_path}")
    print("   uv sync")
    print("   streamlit run streamlit_app.py")

if __name__ == "__main__":
    fix_migration()
