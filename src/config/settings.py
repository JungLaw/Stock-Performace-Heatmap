"""
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

# Logging & Verfification
# Feature flag: controls whether calculate_technical_indicators uses the new
USE_NEW_TA_ENGINE: bool = True
TA_RULES_ENGINE: bool = USE_NEW_TA_ENGINE
# "Don't use 'rule book' for tiles in the 'Technical Indicators' feature"
TI_TILES_USE_RULE_ENGINE: bool = False
# print 'debug ' statements
DEBUG_DF_COLUMNS: bool = True


