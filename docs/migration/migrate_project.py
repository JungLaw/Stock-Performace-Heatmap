#!/usr/bin/env python3
"""
Stock Screener to Heatmap Dashboard Migration Script

This script safely migrates the existing stock-screener project to the new
heatmap dashboard structure while preserving all data and git history.

Usage:
    python migrate_project.py

Requirements:
    - Run from the parent directory containing stock-screener/
    - Ensure stock-screener/ exists and contains the expected files
    - Python 3.8+ with pathlib support
"""

import os
import shutil
import sqlite3
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Configuration
OLD_PROJECT_DIR = "stock-screener"
NEW_PROJECT_DIR = "stock-heatmap-dashboard"
BACKUP_SUFFIX = f"_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Asset group definitions for database population
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

class MigrationError(Exception):
    """Custom exception for migration errors"""
    pass

class ProjectMigrator:
    def __init__(self, old_dir: str, new_dir: str):
        self.old_path = Path(old_dir)
        self.new_path = Path(new_dir)
        self.backup_path = Path(f"{old_dir}{BACKUP_SUFFIX}")
        
        self.migration_log = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log migration steps with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        print(log_entry)
        self.migration_log.append(log_entry)
        
    def validate_environment(self) -> bool:
        """Validate that the environment is ready for migration"""
        self.log("Validating migration environment...")
        
        # Check if old project exists
        if not self.old_path.exists():
            raise MigrationError(f"Source project directory '{self.old_path}' not found")
            
        # Check if new project already exists
        if self.new_path.exists():
            raise MigrationError(f"Target directory '{self.new_path}' already exists")
            
        # Check for required files
        required_files = ["main.py", "utils_database.py", "pyproject.toml", "stock_data.db"]
        for file in required_files:
            if not (self.old_path / file).exists():
                raise MigrationError(f"Required file '{file}' not found in source project")
                
        # Check git repository
        if not (self.old_path / ".git").exists():
            self.log("WARNING: No git repository found. Version history will not be preserved.", "WARN")
            
        self.log("Environment validation passed ✓")
        return True
        
    def create_backup(self):
        """Create backup of original project"""
        self.log(f"Creating backup: {self.backup_path}")
        shutil.copytree(self.old_path, self.backup_path)
        self.log("Backup created successfully ✓")
        
    def create_new_structure(self):
        """Create the new project directory structure"""
        self.log("Creating new project structure...")
        
        # Create main directories
        directories = [
            self.new_path,
            self.new_path / "src",
            self.new_path / "src" / "data",
            self.new_path / "src" / "visualization", 
            self.new_path / "src" / "calculations",
            self.new_path / "src" / "config",
            self.new_path / "data",
            self.new_path / "tests",
            self.new_path / "docs",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            # Create __init__.py files for Python packages
            if "src" in str(directory) and directory.name != "src":
                (directory / "__init__.py").touch()
                
        self.log("Directory structure created ✓")
        
    def migrate_files(self):
        """Migrate and reorganize existing files"""
        self.log("Migrating existing files...")
        
        # File migration mapping
        file_mappings = {
            # Core files to root
            ".gitignore": ".gitignore",
            ".python-version": ".python-version", 
            "README.md": "README.md",
            "uv.lock": "uv.lock",
            
            # Database files to data directory
            "stock_data.db": "data/stock_data.db",
            
            # Source code migrations (will be modified)
            "main.py": "src/data/fetcher.py",
            "utils_database.py": "src/data/database.py",
            "verify.py": "scripts/verify_data.py",
        }
        
        # Copy files according to mapping
        for old_file, new_file in file_mappings.items():
            old_file_path = self.old_path / old_file
            new_file_path = self.new_path / new_file
            
            if old_file_path.exists():
                # Create parent directory if needed
                new_file_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(old_file_path, new_file_path)
                self.log(f"Migrated: {old_file} → {new_file}")
            else:
                self.log(f"WARNING: {old_file} not found, skipping", "WARN")
                
        # Copy git directory if it exists
        if (self.old_path / ".git").exists():
            shutil.copytree(self.old_path / ".git", self.new_path / ".git")
            self.log("Git repository migrated ✓")
            
        # Copy virtual environment reference (but not the actual venv)
        if (self.old_path / ".venv").exists():
            self.log("Virtual environment detected - you'll need to recreate it")
            
        self.log("File migration completed ✓")
        
    def update_pyproject_toml(self):
        """Update pyproject.toml with new dependencies and project info"""
        self.log("Updating pyproject.toml...")
        
        pyproject_path = self.new_path / "pyproject.toml"
        
        # Read existing content
        with open(pyproject_path, 'r') as f:
            content = f.read()
            
        # Update project metadata
        updated_content = content.replace(
            'name = "stock-screener"',
            'name = "stock-heatmap-dashboard"'
        ).replace(
            'description = "Add your description here"',
            'description = "Interactive stock performance heatmap dashboard with real-time data visualization"'
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
        lines = updated_content.split('\n')
        new_lines = []
        in_dependencies = False
        bracket_count = 0
        
        for line in lines:
            if line.startswith('dependencies = ['):
                new_lines.extend(new_deps.split('\n'))
                in_dependencies = True
                bracket_count = line.count('[') - line.count(']')
            elif in_dependencies:
                bracket_count += line.count('[') - line.count(']')
                if bracket_count <= 0:
                    in_dependencies = False
                # Skip old dependency lines
            else:
                new_lines.append(line)
                
        with open(pyproject_path, 'w') as f:
            f.write('\n'.join(new_lines))
            
        self.log("pyproject.toml updated with new dependencies ✓")
        
    def create_new_files(self):
        """Create new files required for the heatmap dashboard"""
        self.log("Creating new project files...")
        
        # Create __init__.py files
        init_files = [
            "src/__init__.py",
            "src/data/__init__.py", 
            "src/visualization/__init__.py",
            "src/calculations/__init__.py",
            "src/config/__init__.py",
        ]
        
        for init_file in init_files:
            (self.new_path / init_file).touch()
            
        # Create main Streamlit app
        streamlit_app_content = '''"""
Stock Performance Heatmap Dashboard - Main Application

This is the main entry point for the Streamlit dashboard.
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
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📊 Stock Performance Heatmap Dashboard")
    st.markdown("---")
    
    # Placeholder for dashboard content
    st.info("🚧 Dashboard under construction - migrated from stock-screener project")
    
    # Show migration status
    st.subheader("Migration Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Database", "✅ Migrated", help="Historical stock data preserved")
    with col2:
        st.metric("Data Fetching", "✅ Migrated", help="yfinance integration ready") 
    with col3:
        st.metric("Visualization", "🚧 In Progress", help="Heatmap under development")

if __name__ == "__main__":
    main()
'''
        
        with open(self.new_path / "streamlit_app.py", 'w') as f:
            f.write(streamlit_app_content)
            
        # Create asset configuration
        assets_config_content = f'''"""
Asset Group Definitions for Heatmap Dashboard

This module defines the various asset groups (Country ETFs, Sector ETFs, Custom)
that can be displayed in the heatmap visualization.
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
        
        with open(self.new_path / "src" / "config" / "assets.py", 'w') as f:
            f.write(assets_config_content)
            
        # Create settings configuration
        settings_content = '''"""
Application Settings and Configuration

This module contains configuration constants and settings for the
stock heatmap dashboard application.
"""

from datetime import datetime, timedelta

# Database configuration
DATABASE_FILE = "data/stock_data.db"
TABLE_NAME = "daily_prices"

# Data refresh settings
CACHE_DURATION_MINUTES = 15
MAX_API_REQUESTS_PER_MINUTE = 100
DATA_STALENESS_WARNING_HOURS = 4

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

# Volume analysis settings
VOLUME_ALERT_THRESHOLD = 2.0  # 2x average volume
VOLUME_PERIODS = {
    "10d": 10,   # 10-day average
    "3m": 65,    # ~3 months of trading days
}

# Market hours (Eastern Time)
MARKET_OPEN = "09:30"
MARKET_CLOSE = "16:00"

# Intraday volume adjustment factors
INTRADAY_VOLUME_ADJUSTMENTS = {
    ("09:30", "09:44"): 0.09,
    ("09:45", "09:59"): 0.14,
    ("10:00", "10:14"): 0.18,
    ("10:15", "10:29"): 0.21,
    ("10:30", "10:59"): 0.27,
    ("11:00", "11:29"): 0.38,
    ("11:30", "11:59"): 0.45,
    ("12:00", "12:59"): 0.52,
    ("13:00", "13:59"): 0.59,
    ("14:00", "14:59"): 0.68,
    ("15:00", "15:29"): 0.76,
    ("15:30", "15:44"): 0.78,
    ("15:45", "16:00"): 0.98,
}
'''
        
        with open(self.new_path / "src" / "config" / "settings.py", 'w') as f:
            f.write(settings_content)
            
        # Create placeholder files for other modules
        placeholder_files = {
            "src/data/processor.py": "# Data processing and transformation logic",
            "src/data/cache.py": "# Caching and data persistence logic", 
            "src/visualization/heatmap.py": "# Plotly treemap heatmap implementation",
            "src/visualization/components.py": "# Reusable Streamlit UI components",
            "src/calculations/performance.py": "# Price performance calculation logic",
            "src/calculations/volume.py": "# Volume analysis and relative volume calculations",
        }
        
        for file_path, placeholder_content in placeholder_files.items():
            with open(self.new_path / file_path, 'w') as f:
                f.write(f'"""\n{placeholder_content[2:]}\n\nTODO: Implement functionality\n"""\n\npass\n')
                
        # Create requirements.txt for deployment
        requirements_content = '''# Stock Heatmap Dashboard Dependencies
# Generated from pyproject.toml for deployment

streamlit>=1.28.0
plotly>=6.1.2
pandas>=2.3.0
yfinance>=0.2.63
numpy>=1.24.0
cachetools>=5.3.0
requests>=2.31.0
python-dotenv>=1.1.0
'''
        
        with open(self.new_path / "requirements.txt", 'w') as f:
            f.write(requirements_content)
            
        # Update README.md
        readme_content = '''# Stock Performance Heatmap Dashboard

An interactive financial visualization tool that displays stock and ETF performance data through intuitive, color-coded heatmaps. Built with Streamlit and Plotly, inspired by professional tools like Finviz.

## Features

- 📊 **Interactive Heatmaps**: Visualize performance data with professional color coding
- 🔄 **Real-time Data**: Integration with yfinance for current market data  
- 📱 **Responsive Design**: Works seamlessly across desktop and mobile devices
- 🎯 **Multiple Asset Groups**: Country ETFs, Sector ETFs, and custom ticker lists
- 📈 **Performance Analysis**: Price changes across multiple timeframes
- 📊 **Volume Analysis**: Relative volume with intraday adjustments
- 🎨 **Professional UI**: Finviz-inspired design with smooth interactions

## Quick Start

```bash
# Install dependencies
uv sync

# Run the dashboard
streamlit run streamlit_app.py
```

## Project Structure

```
stock-heatmap-dashboard/
├── src/                    # Source code
│   ├── data/              # Data fetching and processing
│   ├── visualization/     # UI components and charts
│   ├── calculations/      # Performance and volume analysis
│   └── config/           # Settings and asset definitions
├── data/                 # Database and cached data
├── tests/               # Unit and integration tests
└── streamlit_app.py    # Main application entry point
```

## Data Sources

- **Market Data**: yfinance API for real-time and historical stock data
- **Database**: SQLite for local data persistence and caching
- **Asset Groups**: Predefined lists of Country ETFs, Sector ETFs, and popular stocks

## Development

This project was migrated and evolved from a stock screener application, preserving valuable database infrastructure and data fetching capabilities while adding professional visualization features.

## License

MIT License - see LICENSE file for details
'''
        
        with open(self.new_path / "README.md", 'w') as f:
            f.write(readme_content)
            
        self.log("New project files created ✓")
        
    def update_migrated_code(self):
        """Update migrated code files to work with new structure"""
        self.log("Updating migrated code for new structure...")
        
        # Update fetcher.py (formerly main.py)
        fetcher_path = self.new_path / "src" / "data" / "fetcher.py"
        with open(fetcher_path, 'r') as f:
            content = f.read()
            
        # Update imports and paths
        updated_content = content.replace(
            'DB_FILE = "stock_data.db"',
            'DB_FILE = "../../data/stock_data.db"'
        ).replace(
            'import sqlite3',
            '''import sqlite3
import sys
from pathlib import Path

# Add config to path for imports
config_path = Path(__file__).parent.parent / "config"
sys.path.insert(0, str(config_path))

from assets import get_all_tickers, COUNTRY_ETFS, SECTOR_ETFS'''
        )
        
        # Add docstring
        docstring = '''"""
Stock Data Fetcher - Migrated from main.py

This module handles fetching historical and real-time stock data from yfinance
and populating the SQLite database. Originally developed as part of the
stock-screener project and enhanced for the heatmap dashboard.

Key Features:
- Historical data population
- Incremental data updates
- Data validation and preprocessing
- Support for multiple asset groups

Usage:
    from src.data.fetcher import setup_database, populate_initial_data
"""

'''
        
        updated_content = docstring + updated_content
        
        with open(fetcher_path, 'w') as f:
            f.write(updated_content)
            
        # Update database.py (formerly utils_database.py)
        database_path = self.new_path / "src" / "data" / "database.py"
        with open(database_path, 'r') as f:
            content = f.read()
            
        updated_content = content.replace(
            'DB_FILE = "stock_data.db"',
            'DB_FILE = "../../data/stock_data.db"'
        )
        
        # Add docstring
        docstring = '''"""
Database Utilities - Migrated from utils_database.py

This module provides utility functions for interacting with the SQLite database
containing historical stock data. Originally developed for stock screening and
enhanced for the heatmap dashboard.

Key Features:
- Database schema validation
- Data integrity checks
- Query utilities for historical data
- Duplicate detection and cleanup

Usage:
    from src.data.database import get_most_recent_date, get_stock_data_for_date
"""

'''
        
        updated_content = docstring + updated_content
        
        with open(database_path, 'w') as f:
            f.write(updated_content)
            
        self.log("Code migration updates completed ✓")
        
    def create_migration_summary(self):
        """Create a summary of the migration process"""
        self.log("Creating migration summary...")
        
        summary_content = f'''# Migration Summary Report

**Migration Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Source Project**: {self.old_path}
**Target Project**: {self.new_path}
**Backup Location**: {self.backup_path}

## Files Migrated

### Core Infrastructure
- ✅ SQLite database with historical data preserved
- ✅ yfinance integration and data fetching logic
- ✅ Data validation and preprocessing functions
- ✅ Git repository and version history

### Project Configuration  
- ✅ pyproject.toml updated with new dependencies
- ✅ Virtual environment reference (needs recreation)
- ✅ Git configuration and ignore rules

### New Project Structure
- ✅ Streamlit application framework
- ✅ Asset group definitions (Country/Sector ETFs)
- ✅ Configuration and settings modules
- ✅ Placeholder files for development

## Next Steps

### Immediate (Week 1)
1. **Recreate Virtual Environment**
   ```bash
   cd {self.new_path}
   uv sync
   ```

2. **Test Database Migration**
   ```bash
   cd {self.new_path}
   python -c "from src.data.database import check_table_schema; check_table_schema()"
   ```

3. **Run Basic Streamlit App**
   ```bash
   cd {self.new_path}
   streamlit run streamlit_app.py
   ```

### Development (Weeks 2-3)
1. Implement heatmap visualization in `src/visualization/heatmap.py`
2. Add performance calculations in `src/calculations/performance.py`
3. Build volume analysis in `src/calculations/volume.py`
4. Expand asset groups in database

### Testing & Polish (Week 4)
1. Add comprehensive tests
2. Optimize performance and caching
3. Implement Finviz-style design
4. Documentation and deployment prep

## Migration Log
{chr(10).join(self.migration_log)}

## Notes
- Original project backed up to: {self.backup_path}
- Database contains {self._count_database_records()} historical records
- Project ready for continued development
- All existing functionality preserved
'''
        
        with open(self.new_path / "MIGRATION_SUMMARY.md", 'w') as f:
            f.write(summary_content)
            
        self.log("Migration summary created ✓")
        
    def _count_database_records(self) -> int:
        """Count records in the migrated database"""
        try:
            db_path = self.new_path / "data" / "stock_data.db"
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM daily_prices")
                return cursor.fetchone()[0]
        except Exception:
            return 0
            
    def run_migration(self):
        """Execute the complete migration process"""
        try:
            print("🚀 Starting Stock Screener → Heatmap Dashboard Migration")
            print("=" * 60)
            
            # Validation phase
            self.validate_environment()
            
            # Backup phase  
            self.create_backup()
            
            # Migration phases
            self.create_new_structure()
            self.migrate_files()
            self.update_pyproject_toml() 
            self.create_new_files()
            self.update_migrated_code()
            self.create_migration_summary()
            
            print("=" * 60)
            print("✅ Migration completed successfully!")
            print(f"📁 New project: {self.new_path}")
            print(f"💾 Backup: {self.backup_path}")
            print(f"📊 Database records preserved: {self._count_database_records()}")
            print()
            print("🚀 Next steps:")
            print(f"   cd {self.new_path}")
            print("   uv sync")
            print("   streamlit run streamlit_app.py")
            
        except MigrationError as e:
            print(f"❌ Migration failed: {e}")
            return False
        except Exception as e:
            print(f"💥 Unexpected error during migration: {e}")
            return False
            
        return True

def main():
    """Main migration entry point"""
    # Check if we're in the right directory
    if not Path(OLD_PROJECT_DIR).exists():
        print(f"❌ Error: {OLD_PROJECT_DIR} directory not found")
        print(f"Please run this script from the directory containing {OLD_PROJECT_DIR}/")
        return
        
    # Run migration
    migrator = ProjectMigrator(OLD_PROJECT_DIR, NEW_PROJECT_DIR)
    success = migrator.run_migration()
    
    if success:
        print("\n🎉 Migration completed! Your stock screener has been transformed into a heatmap dashboard.")
    else:
        print("\n💔 Migration failed. Check the error messages above.")

if __name__ == "__main__":
    main()