"""
Debug XLC 1-month calculation to compare with Yahoo Finance
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from calculations.performance import DatabaseIntegratedPerformanceCalculator

def debug_xlc_calculation():
    """Debug XLC 1-month calculation"""
    print("🔍 Debugging XLC 1-Month Calculation")
    print("=" * 50)
    
    calc = DatabaseIntegratedPerformanceCalculator()
    
    # Show what today's date is being used
    now = datetime.now()
    target_date = now - timedelta(days=30)
    
    print(f"📅 Calculation dates:")
    print(f"   Today: {now.strftime('%Y-%m-%d %A')}")
    print(f"   Target (30 days ago): {target_date.strftime('%Y-%m-%d %A')}")
    
    # Get detailed calculation for XLC
    print(f"\n📊 XLC Calculation Details:")
    result = calc.calculate_performance_for_ticker('XLC', '1m')
    
    print(f"   Current Price: ${result['current_price']:.2f}")
    print(f"   Historical Price: ${result['historical_price']:.2f}")
    print(f"   Change: {result['percentage_change']:+.2f}%")
    print(f"   Period Label: {result['period_label']}")
    print(f"   Data Source: {result.get('data_source', 'unknown')}")
    
    # Let's also check what yfinance shows for comparison
    print(f"\n📈 Direct yfinance comparison:")
    import yfinance as yf
    
    stock = yf.Ticker('XLC')
    
    # Get current info
    try:
        info = stock.info
        current_from_info = info.get('currentPrice') or info.get('regularMarketPrice')
        print(f"   Current from yfinance info: ${current_from_info:.2f}")
    except:
        print("   Could not get current price from info")
    
    # Get recent history
    try:
        recent_hist = stock.history(period='2d')
        if not recent_hist.empty:
            latest_close = recent_hist['Close'].iloc[-1]
            print(f"   Latest close from history: ${latest_close:.2f}")
    except Exception as e:
        print(f"   Error getting recent history: {e}")
    
    # Get 1-month history to see what date we're comparing against
    try:
        start_date = target_date - timedelta(days=10)
        end_date = target_date + timedelta(days=3)
        
        print(f"\n📊 Historical data lookup:")
        print(f"   Fetching from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        hist_data = stock.history(start=start_date, end=end_date)
        
        if not hist_data.empty:
            print(f"   Available dates in range:")
            for date_idx in hist_data.index:
                date_str = date_idx.strftime('%Y-%m-%d')
                close_price = hist_data.loc[date_idx, 'Close']
                print(f"     {date_str}: ${close_price:.2f}")
                
            # Find closest to target
            hist_data.index = pd.to_datetime(hist_data.index).date
            target_date_only = target_date.date()
            
            available_dates = [d for d in hist_data.index if d <= target_date_only]
            if available_dates:
                closest_date = max(available_dates)
                closest_price = hist_data.loc[closest_date, 'Close']
                print(f"\n   ✅ Closest date used: {closest_date} = ${closest_price:.2f}")
                
                # Calculate percentage change
                if current_from_info:
                    pct_change = ((current_from_info - closest_price) / closest_price) * 100
                    print(f"   📊 Manual calculation: {pct_change:+.2f}%")
        
        else:
            print("   No historical data found in range")
            
    except Exception as e:
        print(f"   Error getting historical data: {e}")
    
    # Compare with Yahoo Finance reference
    print(f"\n🌐 Yahoo Finance Comparison:")
    print(f"   You mentioned Yahoo shows 1M price as $102.33")
    print(f"   Our historical price: ${result['historical_price']:.2f}")
    print(f"   Difference: ${abs(102.33 - result['historical_price']):.2f}")
    
    if abs(102.33 - result['historical_price']) > 0.50:
        print("   ⚠️  Significant difference detected!")
        print("   This could be due to:")
        print("     - Different date interpretation (calendar month vs 30 days)")
        print("     - Weekend/holiday date handling")
        print("     - Different data sources")
        print("     - Dividend adjustments")

if __name__ == "__main__":
    debug_xlc_calculation()
