# Stock Screener Migration Walkthrough (Complete Guide)

## Pre-Migration Checklist

### 1. Environment Preparation

**Bash:**
```bash
# Navigate to your Projects directory (where stock-screener exists)
cd C:\Users\lawre\Projects

# Verify current structure
ls -la stock-screener/
# Expected files: main.py, utils_database.py, pyproject.toml, stock_data.db

# Check database status
cd stock-screener
python verify.py
cd ..
```

**PowerShell:**
```powershell
# Navigate to your Projects directory (where stock-screener exists)
Set-Location "C:\Users\lawre\Projects"

# Verify current structure
Get-ChildItem stock-screener
# Expected files: main.py, utils_database.py, pyproject.toml, stock_data.db

# Check database status
Set-Location stock-screener
python verify.py
Set-Location ..
```

### 2. Save the Migration Script
- Copy the migration script from the artifact above
- Save it as `migrate_project.py` in your Projects directory
- **Location**: `C:\Users\lawre\Projects\migrate_project.py`


> **Pre-Migration Commit ID**:
```powershell
PS C:\Users\lawre\Projects\stock-screener> git log --oneline -3
f93efe7 (HEAD -> main) Pre-migration checkpoint: Stock screener with working database and yfinance integration
```

### 3. Backup Verification

**Bash:**
```bash
# Ensure we can create backups (check disk space)
du -sh stock-screener/
# Should show ~2-5MB total

# Verify git status (optional but recommended)
cd stock-screener
git status
git log --oneline -5  # See recent commits
cd ..
```

**PowerShell:**
```powershell
# Check directory size
Get-ChildItem stock-screener -Recurse | Measure-Object -Property Length -Sum
# Should show ~2-5MB total

# Verify git status (optional but recommended)
Set-Location stock-screener
git status
git log --oneline -5  # See recent commits
Set-Location ..
```

## Migration Execution

### Step 1: Run the Migration Script

**Bash:**
```bash
# From C:\Users\lawre\Projects directory
python migrate_project.py
```

**PowerShell:**
```powershell
# From C:\Users\lawre\Projects directory
python migrate_project.py
```

**Expected Output:**
```
🚀 Starting Stock Screener → Heatmap Dashboard Migration
============================================================
[HH:MM:SS] INFO: Validating migration environment...
[HH:MM:SS] INFO: Environment validation passed ✓
[HH:MM:SS] INFO: Creating backup: stock-screener_backup_20250108_HHMMSS
[HH:MM:SS] INFO: Backup created successfully ✓
[HH:MM:SS] INFO: Creating new project structure...
[HH:MM:SS] INFO: Directory structure created ✓
[HH:MM:SS] INFO: Migrating existing files...
[HH:MM:SS] INFO: Migrated: .gitignore → .gitignore
[HH:MM:SS] INFO: Migrated: stock_data.db → data/stock_data.db
[HH:MM:SS] INFO: Migrated: main.py → src/data/fetcher.py
[HH:MM:SS] INFO: Migrated: utils_database.py → src/data/database.py
[HH:MM:SS] INFO: Git repository migrated ✓
[HH:MM:SS] INFO: File migration completed ✓
[HH:MM:SS] INFO: Updating pyproject.toml...
[HH:MM:SS] INFO: pyproject.toml updated with new dependencies ✓
[HH:MM:SS] INFO: Creating new project files...
[HH:MM:SS] INFO: New project files created ✓
[HH:MM:SS] INFO: Updating migrated code for new structure...
[HH:MM:SS] INFO: Code migration updates completed ✓
[HH:MM:SS] INFO: Creating migration summary...
[HH:MM:SS] INFO: Migration summary created ✓
============================================================
✅ Migration completed successfully!
📁 New project: stock-heatmap-dashboard
💾 Backup: stock-screener_backup_20250108_HHMMSS  
📊 Database records preserved: XXXX
```

### Step 2: Verify Migration Success

**Bash:**
```bash
# Check new project structure
ls -la stock-heatmap-dashboard/
tree stock-heatmap-dashboard/  # if tree command available

# Verify key files exist
ls -la stock-heatmap-dashboard/data/stock_data.db
ls -la stock-heatmap-dashboard/src/data/
ls -la stock-heatmap-dashboard/streamlit_app.py
```

**PowerShell:**
```powershell
# Check new project structure
Get-ChildItem stock-heatmap-dashboard
# For tree view (if available):
# tree stock-heatmap-dashboard /F

# Verify key files exist
Test-Path stock-heatmap-dashboard/data/stock_data.db
Get-ChildItem stock-heatmap-dashboard/src/data/
Test-Path stock-heatmap-dashboard/streamlit_app.py
```

**Expected New Structure:**
```
stock-heatmap-dashboard/
├── .git/                    # Git history preserved
├── .gitignore              # Original ignore rules
├── data/
│   └── stock_data.db       # Your valuable database
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── fetcher.py      # Enhanced main.py
│   │   ├── database.py     # Enhanced utils_database.py
│   │   ├── processor.py    # New placeholder
│   │   └── cache.py        # New placeholder
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── heatmap.py      # New placeholder
│   │   └── components.py   # New placeholder
│   ├── calculations/
│   │   ├── __init__.py
│   │   ├── performance.py  # New placeholder
│   │   └── volume.py       # New placeholder
│   └── config/
│       ├── __init__.py
│       ├── assets.py       # New asset definitions
│       └── settings.py     # New configuration
├── tests/                  # Empty directory for future tests
├── docs/                   # Empty directory for documentation
├── scripts/
│   └── verify_data.py      # Migrated verify.py
├── streamlit_app.py        # New main entry point
├── pyproject.toml          # Updated with new dependencies
├── requirements.txt        # New deployment file
├── README.md               # Updated project description
└── MIGRATION_SUMMARY.md    # Migration report
```

## Post-Migration Setup

### Step 3: Navigate to New Project

**Bash:**
```bash
cd stock-heatmap-dashboard
```

**PowerShell:**
```powershell
Set-Location stock-heatmap-dashboard
```

### Step 4: Recreate Virtual Environment

**Bash:**
```bash
# If using uv (recommended)
uv sync

# OR if using pip/venv
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

**PowerShell:**
```powershell
# If using uv (recommended)
uv sync

# OR if using pip/venv
python -m venv .venv
.venv\Scripts\Activate.ps1  # Activate virtual environment
pip install -e .
```

#### Update: new dependencies didn't install automatically
- Update failed due to critical flaw in `fix_migration.py` (no closed brackets in `if line.startswith('dependencies = ['):`)
- had to manually install streamlit, cachetools, and numpy using `uv add`
```bash
# Add the missing dependencies
uv add streamlit>=1.28.0
uv add numpy>=1.24.0  
uv add cachetools>=5.3.0
```



### Step 5: Test Database Migration
```bash
# Test database connectivity
python -c "
import sqlite3
conn = sqlite3.connect('data/stock_data.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM daily_prices')
print(f'Database records: {cursor.fetchone()[0]}')
cursor.execute('SELECT DISTINCT Ticker FROM daily_prices')
tickers = [row[0] for row in cursor.fetchall()]
print(f'Tickers in database: {sorted(tickers)}')
conn.close()
"
```


**Expected Output:**
```
Database records: 1234  # Your actual record count
Tickers in database: ['AAPL', 'AMZN', 'GOOGL', 'IYC', 'IYE', 'IYF', 'IYK', 'META', 'MCHI', 'MSFT', 'NVDA', 'QQQ', 'SPY']
```

```
# Actual
Database records: 19026  (Database records: 19026eba19)
Tickers in database: ['AAPL', 'AMZN', 'EWJ', 'GOOGL', 'IYC', 'IYE', 'IYF', 'IYK', 'MCHI', 'META', 'MSFT', 'NVDA', 'QQQ', 'SPY']
```


### Step 6: Test Basic Streamlit App

**Bash:**
```bash
# Launch the basic Streamlit dashboard
streamlit run streamlit_app.py
```

**PowerShell:**
```powershell
# Launch the basic Streamlit dashboard
streamlit run streamlit_app.py
```

**Expected Result:**
- Browser opens to `http://localhost:8501`
- Dashboard displays "🚧 Dashboard under construction"
- Migration status shows green checkmarks for Database and Data Fetching
- No errors in terminal

### Step 7: Verify Code Migration
```bash
# Test the migrated data fetching code
python -c "
import sys
sys.path.insert(0, 'src')
from data.database import check_table_schema
check_table_schema()
"
```

**Expected Output:**
```
Current table schema:
  (0, 'Ticker', 'TEXT', 1, None, 1)
  (1, 'Date', 'TEXT', 1, None, 2)  
  (2, 'Open', 'REAL', 1, None, 0)
  (3, 'High', 'REAL', 1, None, 0)
  (4, 'Low', 'REAL', 1, None, 0)
  (5, 'Close', 'REAL', 1, None, 0)
  (6, 'Adj Close', 'REAL', 1, None, 0)
  (7, 'Volume', 'INTEGER', 1, None, 0)
```

## Troubleshooting Common Issues

### Issue 1: Migration Script Fails
**Symptoms:** Script exits with error during validation
**Solutions:**

**Bash:**
```bash
# Check if in correct directory
pwd  # Should show C:\Users\lawre\Projects

# Verify stock-screener exists
ls -la stock-screener/

# Check for required files
ls -la stock-screener/main.py
ls -la stock-screener/stock_data.db
```

**PowerShell:**
```powershell
# Check if in correct directory
Get-Location  # Should show C:\Users\lawre\Projects

# Verify stock-screener exists
Get-ChildItem stock-screener

# Check for required files
Test-Path stock-screener/main.py
Test-Path stock-screener/stock_data.db
```

### Issue 2: Database Path Issues
**Symptoms:** "No such file or directory" when testing database
**Solutions:**

**Bash:**
```bash
# Check database was moved correctly
ls -la stock-heatmap-dashboard/data/stock_data.db

# If missing, manually copy
cp stock-screener/stock_data.db stock-heatmap-dashboard/data/
```

**PowerShell:**
```powershell
# Check database was moved correctly
Test-Path stock-heatmap-dashboard/data/stock_data.db

# If missing, manually copy
Copy-Item stock-screener/stock_data.db stock-heatmap-dashboard/data/
```

### Issue 3: Import Errors in New Structure
**Symptoms:** ModuleNotFoundError when testing code
**Solutions:**

**Bash:**
```bash
# Verify __init__.py files exist
find stock-heatmap-dashboard/src -name "__init__.py"

# If missing, create them
touch stock-heatmap-dashboard/src/__init__.py
touch stock-heatmap-dashboard/src/data/__init__.py
# etc.
```

**PowerShell:**
```powershell
# Verify __init__.py files exist
Get-ChildItem stock-heatmap-dashboard/src -Recurse -Name "__init__.py"

# If missing, create them
New-Item stock-heatmap-dashboard/src/__init__.py -ItemType File -Force
New-Item stock-heatmap-dashboard/src/data/__init__.py -ItemType File -Force
# etc.
```

### Issue 4: Streamlit Won't Start
**Symptoms:** streamlit command not found
**Solutions:**

**Bash:**
```bash
# Ensure virtual environment is activated
which python  # Should show .venv path

# Install streamlit explicitly
pip install streamlit>=1.28.0

# Or reinstall all dependencies
uv sync --force
```

**PowerShell:**
```powershell
# Ensure virtual environment is activated
Get-Command python | Select-Object Source  # Should show .venv path

# Install streamlit explicitly
pip install streamlit>=1.28.0

# Or reinstall all dependencies
uv sync --force
```

## Development Next Steps

### Week 1: Foundation Testing

**Bash:**
```bash
# Test asset configuration
python -c "
import sys
sys.path.insert(0, 'src')
from config.assets import get_all_tickers, COUNTRY_ETFS
print(f'Total unique tickers: {len(get_all_tickers())}')
print(f'Country ETFs: {len(COUNTRY_ETFS)}')
"

# Test settings configuration  
python -c "
import sys
sys.path.insert(0, 'src')
from config.settings import COLOR_SCHEME, PERFORMANCE_THRESHOLDS
print('Color scheme loaded:', list(COLOR_SCHEME.keys()))
print('Thresholds loaded:', PERFORMANCE_THRESHOLDS)
"
```

**PowerShell:**
```powershell
# Test asset configuration
python -c @"
import sys
sys.path.insert(0, 'src')
from config.assets import get_all_tickers, COUNTRY_ETFS
print(f'Total unique tickers: {len(get_all_tickers())}')
print(f'Country ETFs: {len(COUNTRY_ETFS)}')
"@

# Test settings configuration  
python -c @"
import sys
sys.path.insert(0, 'src')
from config.settings import COLOR_SCHEME, PERFORMANCE_THRESHOLDS
print('Color scheme loaded:', list(COLOR_SCHEME.keys()))
print('Thresholds loaded:', PERFORMANCE_THRESHOLDS)
"@
```

### Week 1: Expand Database with New Assets
```bash
# Run enhanced data fetcher with new asset groups
python -c "
import sys
sys.path.insert(0, 'src')
from data.fetcher import setup_database, populate_initial_data
from config.assets import COUNTRY_ETFS, SECTOR_ETFS

# This will add new tickers to your existing database
setup_database()
# Note: You'll need to modify fetcher.py to use new asset groups
"
```

### Week 2: Start Dashboard Development
1. **Implement Basic Heatmap**: Edit `src/visualization/heatmap.py`
2. **Add Performance Calculations**: Edit `src/calculations/performance.py`  
3. **Create UI Components**: Edit `src/visualization/components.py`
4. **Enhance Main App**: Edit `streamlit_app.py`

### Week 3: Polish and Testing
1. **Add Volume Analysis**: Edit `src/calculations/volume.py`
2. **Implement Caching**: Edit `src/data/cache.py`
3. **Add Tests**: Create files in `tests/`
4. **Documentation**: Enhance `docs/`

## Migration Verification Checklist

- [ ] Migration script completed without errors
- [ ] New directory structure created correctly
- [ ] Database file copied and accessible
- [ ] Git history preserved
- [ ] Virtual environment recreated successfully  
- [ ] Streamlit app launches without errors
- [ ] Database contains expected number of records
- [ ] All original tickers present in database
- [ ] Asset configuration files created
- [ ] Settings configuration accessible
- [ ] Code imports work in new structure
- [ ] Migration summary generated

## Rollback Procedure (If Needed)

If something goes wrong, you can easily rollback:

**Bash:**
```bash
# Remove new project (if needed)
rm -rf stock-heatmap-dashboard/

# Your original project is safely backed up
ls -la stock-screener_backup_*/

# Restore from backup if needed
cp -r stock-screener_backup_*/ stock-screener-restored/
```

**PowerShell:**
```powershell
# Remove new project (if needed)
Remove-Item stock-heatmap-dashboard -Recurse -Force

# Your original project is safely backed up
Get-ChildItem stock-screener_backup_*

# Restore from backup if needed
Copy-Item stock-screener_backup_* stock-screener-restored -Recurse
```

## Success Indicators

✅ **Migration Successful If:**
- New project directory exists with complete structure
- Database accessible with all original data
- Streamlit app launches and displays migration status
- No import errors when testing core modules
- Git history preserved with all commits
- Original project safely backed up

🎉 **Ready for Development When:**
- All verification tests pass
- Asset groups configuration loads correctly
- Database queries return expected data
- Streamlit dashboard shows "migrated" status
- Virtual environment contains all dependencies

You're now ready to start building the heatmap dashboard on your solid foundation!
