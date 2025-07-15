"""
Compare yfinance vs Yahoo Finance website for multiple tickers
"""

import yfinance as yf
from datetime import datetime, timedelta

def compare_data_sources():
    """Compare yfinance data with Yahoo Finance website"""
    
    tickers_to_check = ['XLC', 'SPY', 'QQQ', 'AAPL']
    check_date = '2025-06-13'
    
    print("🔍 Comparing yfinance vs Yahoo Finance website")
    print("=" * 60)
    print(f"Checking date: {check_date}")
    print()
    
    for ticker in tickers_to_check:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start='2025-06-10', end='2025-06-17')
            
            if not hist.empty and check_date in hist.index.strftime('%Y-%m-%d'):
                yf_price = hist.loc[check_date, 'Close']
                print(f"{ticker:6} | yfinance: ${yf_price:.2f} | Website: $_____ (check manually)")
            else:
                print(f"{ticker:6} | No data available for {check_date}")
                
        except Exception as e:
            print(f"{ticker:6} | Error: {e}")
    
    print()
    print("📋 Manual verification steps:")
    print("1. Go to finance.yahoo.com")
    print("2. Search for each ticker")
    print("3. Click 'Historical Data'")
    print("4. Check the closing price for 2025-06-13")
    print("5. Compare with yfinance values above")
    print()
    print("💡 If systematic differences exist, this explains your discrepancy!")

if __name__ == "__main__":
    compare_data_sources()
