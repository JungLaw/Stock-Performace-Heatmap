"""
Asset Group Definitions for Heatmap Dashboard
Enhanced with display names for better user experience
"""

# Country ETFs with display names (51 entries a/o 9/12)
# 9/14/25: Have 3 emerging |3 developed | 2 'World's: All + Total |2 xcl. Japan
COUNTRY_ETFS = [
    # Format: (ticker, display_name)
    ('VTI', 'US Total Market'),
    ('VEA', 'Developed Markets ex-US'),
    ('VWO', 'Emerging Markets'),
    ('EEM', 'Emerging Markets'),
    ('VGK', 'Europe'),
    ('VPL', 'Asia-Pacific ex-Japan'),
    ('EPP', 'Asia-Pacific ex-Japan'),
    ('EWJ', 'Japan'),
    ('EWZ', 'Brazil'),
    ('INDA', 'India'),
    ('MCHI', 'China'),  # added 9/15    
    ('FXI', 'China (lc)'),  # added 9/15
    ('KWEB', 'China (tech)'),  # added 9/15    
    ('EWU', 'United Kingdom'),
    ('EWG', 'Germany'),
    ('EWQ', 'France'),
    ('EWC', 'Canada'),
    ('EWA', 'Australia'),
    ('EWL', 'Switzerland'),
    ('EWI', 'Italy'),
    ('EWP', 'Spain'),
    ('EWD', 'Sweden'),
    ('EWN', 'Netherlands'),
    ('EWS', 'Singapore'),
    ('EWT', 'Taiwan'),  # TWN
    ('EWY', 'South Korea'),
    ('EWH', 'Hong Kong'),
    ('EWM', 'Malaysia'),
    ('EPOL', 'Poland'),
    ('EZA', 'South Africa'),
    ('ECH', 'Chile'),
    ('EIDO', 'Indonesia'),
    ('EPHE', 'Philippines'),
    ('VNM', 'Vietnam'),
    ('THD', 'Thailand'),
    ('TUR', 'Turkey'),
    ('RSX', 'Russia'),
    ('EFA', 'Developed Markets'),
    ('IEFA', 'Developed Markets'),
    ('IEMG', 'Emerging Markets'),
    ('ACWI', 'All World'),
    ('VT', 'Total World'),
    ('QQQ', 'Nasdaq 100'),
    ('ONEQ', 'Nasdaq'),
    ('SPY', 'S&P 500'),
    ('IWM', 'Russell 2000'),
    ('DIA', 'Dow Jones'),
    ('BND', 'US Bonds'),
    ('AGG', 'US Aggregate Bonds'),
    ('TLT', 'Long-Term Treasury'),
    ('VCIT', 'Corporate Bond (Inter.)'), # New 9/14/25
    ('USHY', 'Corporate Bonds (HY)'),       # New 9/14/25
#    ('GLD', 'Gold'),     # 9/14: moved to 'SECTOR_ETFS
#    ('SLV', 'Silver'),
#    ('VNQ', 'US REITs'),
#    ('VNQI', 'Intl. REITs'),
]

# Sector ETFs with display names (30 entries a/o 9/12)
SECTOR_ETFS = [
    # Format: (ticker, display_name)
    ('XLF', 'Financial'),
    ('KBE', 'Banking'),
    ('KRE', 'Regional Banks'),    
    ('XLK', 'Technology'),
    ('XLE', 'Energy'),
    ('XLV', 'Healthcare'),   # VHT, IYH
    ('XLI', 'Industrial'),
    ('XLP', 'Consumer Staples'),
    ('XLY', 'Consumer Discretionary'),
    ('XLU', 'Utilities'),
    ('XLC', 'Communications'),
    ('XLB', 'Materials'),
    ('XME', 'Metals & Mining'),
    ('XRT', 'Retail'),
    ('XHB', 'Homebuilders'),
    ('ITB', 'Home Construction'),
    ('XLRE', 'REITs (xcl. Home, Office)'),
    ('VNQ', 'REITs'),    # 9/14    
    ('VNQI', 'Intl. REITs'),   # 9/14 
 #  ('SMH', 'Semiconductors'),
    ('SOXX', 'Semiconductor Index'),
    ('IBB', 'Biotech (MW,LC)'),
    ('XBI', 'Biotech (EW, <LC)'),
    ('ARKK', 'Innovation ETF'),
    ('ARKQ', 'Autonomous & Robotics'),
    ('ARKW', 'Next Generation Internet'),
    ('ROBO', 'Robotics & AI'),
    ('ARKG', 'Genomic Revolution'),
    ('HACK', 'Cybersecurity'),
    ('SKYY', 'Cloud Computing'),
    ('ICLN', 'Clean Energy (Global, LC)'),
    ('PBW', 'Clean Energy (US, <LC)'),
    ('GLD', 'Gold'),      # Moved: 9/14
    ('SLV', 'Silver'),     # Moved: 9/14
    ('NLR', 'Nuclear/Uran.'), # New: 9/14       
    ('QQQ', 'Nasdaq 100'),     # Copied: 9/14
    ('ONEQ', 'Nasdaq'),         # Copied: 9/14
    ('SPY', 'S&P 500'),         # Copied: 9/14
    ('IWM', 'Russell 2000'),         # Copied: 9/14
    ('DIA', 'Dow Jones'),       # Copied: 9/14
    ('BND', 'US Bonds'),    # Copied: 9/14
    ('AGG', 'US Aggregate Bonds'),    # Copied: 9/14
    ('TLT', 'Long-Term Treasury'),    # Copied: 9/14
    ('VCIT', 'Corporate Bond (Inter.)'), # New/Copied 9/14/25
    ('USHY', 'Corporate Bonds (HY)'),       # New/Copied 9/14/25    
]
    # Potential additions: small cap, mid cap


# Default custom tickers (remain as tickers only)
CUSTOM_DEFAULT = ['AMZN', 'META', 'NVDA', 'AAPL', 'GOOGL', 'MSFT', 'BABA', 'SPY', 'ONEQ', 'TSM']

# Helper functions to work with ticker/name pairs
def get_tickers_only(ticker_list):
    """Extract just the tickers from a list of (ticker, name) tuples"""
    if not ticker_list:
        return []
    # Handle both tuple format and string format
    if isinstance(ticker_list[0], tuple):
        return [item[0] for item in ticker_list]
    else:
        return ticker_list

def get_display_name(ticker, ticker_list):
    """Get display name for a ticker from a list of (ticker, name) tuples"""
    if not ticker_list:
        return ticker
    # Handle both tuple format and string format
    if isinstance(ticker_list[0], tuple):
        for item_ticker, display_name in ticker_list:
            if item_ticker == ticker:
                return display_name
    return ticker

def get_ticker_name_dict(ticker_list):
    """Convert list of (ticker, name) tuples to dictionary"""
    if not ticker_list:
        return {}
    # Handle both tuple format and string format
    if isinstance(ticker_list[0], tuple):
        return {ticker: name for ticker, name in ticker_list}
    else:
        return {ticker: ticker for ticker in ticker_list}

# Asset group metadata
ASSET_GROUPS = {
    "country": {
        "name": "Country ETFs",
        "description": "Exchange-traded funds representing different countries and regions",
        "tickers": get_tickers_only(COUNTRY_ETFS),
        "ticker_names": get_ticker_name_dict(COUNTRY_ETFS),
        "max_tickers": 60,    # 52
        "use_display_names": True  # Flag to indicate display names should be used
    },
    "sector": {
        "name": "Sector ETFs", 
        "description": "Exchange-traded funds representing different market sectors",
        "tickers": get_tickers_only(SECTOR_ETFS),
        "ticker_names": get_ticker_name_dict(SECTOR_ETFS),
        "max_tickers": 60,   # 30
        "use_display_names": True  # Flag to indicate display names should be used
    },
    "custom": {
        "name": "Custom Tickers",
        "description": "User-defined list of stock tickers",
        "tickers": CUSTOM_DEFAULT,
        "ticker_names": {ticker: ticker for ticker in CUSTOM_DEFAULT},
        "max_tickers": 10,
        "use_display_names": False  # Flag to indicate tickers should be displayed as-is
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

def get_display_name_for_ticker(ticker: str, group_name: str = None) -> str:
    """
    Get display name for a ticker, optionally specifying the group
    
    Args:
        ticker: The ticker symbol
        group_name: Optional group name ('country', 'sector', 'custom')
        
    Returns:
        Display name or ticker if no display name found
    """
    if group_name:
        group = ASSET_GROUPS.get(group_name, {})
        ticker_names = group.get("ticker_names", {})
        return ticker_names.get(ticker, ticker)
    else:
        # Search all groups
        for group in ASSET_GROUPS.values():
            ticker_names = group.get("ticker_names", {})
            if ticker in ticker_names and group.get("use_display_names", False):
                return ticker_names[ticker]
        return ticker

def should_use_display_names(group_name: str) -> bool:
    """Check if a group should use display names"""
    group = ASSET_GROUPS.get(group_name, {})
    return group.get("use_display_names", False)
