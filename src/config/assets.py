"""
Asset Group Definitions for Heatmap Dashboard
"""

# Country ETFs (52 tickers)
COUNTRY_ETFS = ['VTI', 'VEA', 'VWO', 'EEM', 'VGK', 'VPL', 'EWJ', 'EWZ', 'INDA', 'EWU', 'EWG', 'EWQ', 'EWC', 'EWA', 'EWL', 'EWI', 'EWP', 'EWD', 'EWN', 'EWS', 'EWT', 'EWY', 'EWH', 'EWM', 'EPOL', 'EPP', 'EZA', 'ECH', 'EIDO', 'EPHE', 'VNM', 'THD', 'TUR', 'RSX', 'QQQ', 'SPY', 'IWM', 'DIA', 'EFA', 'IEFA', 'IEMG', 'ACWI', 'VT', 'BND', 'AGG', 'TLT', 'GLD', 'SLV', 'VNQ', 'VNQI', 'XLF', 'XLK']

# Sector ETFs (30 tickers)  
SECTOR_ETFS = ['XLF', 'XLK', 'XLE', 'XLV', 'XLI', 'XLP', 'XLY', 'XLU', 'XLRE', 'XLC', 'XLB', 'XME', 'XRT', 'XHB', 'ITB', 'KBE', 'KRE', 'SMH', 'SOXX', 'IBB', 'XBI', 'ARKK', 'ARKQ', 'ARKW', 'ARKG', 'ICLN', 'PBW', 'HACK', 'SKYY', 'ROBO']

# Default custom tickers (9 tickers)
CUSTOM_DEFAULT = ['AMZN', 'META', 'NVDA', 'AAPL', 'GOOGL', 'MSFT', 'BABA', 'SPY', 'QQQ']

# Asset group metadata
ASSET_GROUPS = {
    "country": {
        "name": "Country ETFs",
        "description": "Exchange-traded funds representing different countries and regions",
        "tickers": COUNTRY_ETFS,
        "max_tickers": 52
    },
    "sector": {
        "name": "Sector ETFs", 
        "description": "Exchange-traded funds representing different market sectors",
        "tickers": SECTOR_ETFS,
        "max_tickers": 30
    },
    "custom": {
        "name": "Custom Tickers",
        "description": "User-defined list of stock tickers",
        "tickers": CUSTOM_DEFAULT,
        "max_tickers": 10
    }
}

def get_asset_group(group_name: str) -> dict:
    """Get asset group configuration by name"""
    return ASSET_GROUPS.get(group_name, {})

def get_all_tickers() -> list:
    """Get all unique tickers from all asset groups"""
    all_tickers = set()
    for group in ASSET_GROUPS.values():
        all_tickers.update(group["tickers"])
    return sorted(list(all_tickers))
