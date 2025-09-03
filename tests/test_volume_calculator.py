"""
Volume Calculator Tests

Test suite for DatabaseIntegratedVolumeCalculator to verify:
1. Current volume retrieval (last completed trading day)
2. Benchmark calculations (10D/1W/1M/60D averages)
3. Missing data handling (strict validation)
4. Performance calculations (percentage change formula)
5. Multiple ticker processing
"""

import sys
from pathlib import Path
import sqlite3
from datetime import datetime, timedelta

# Add src to path for imports
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from calculations.volume import DatabaseIntegratedVolumeCalculator
from calculations.performance import get_last_completed_trading_day, get_last_n_trading_days


def test_database_connection():
    """Test 1: Verify database connection and volume data availability"""
    print("=" * 60)
    print("TEST 1: Database Connection and Volume Data")
    print("=" * 60)
    
    calculator = DatabaseIntegratedVolumeCalculator()
    
    # Check if database is available
    print(f"Database available: {calculator.db_available}")
    
    if calculator.db_available:
        # Test database connection
        conn = calculator._get_database_connection()
        if conn:
            cursor = conn.cursor()
            
            # Check total volume records
            cursor.execute("SELECT COUNT(*) FROM daily_prices WHERE Volume > 0")
            volume_count = cursor.fetchone()[0]
            print(f"Total volume records: {volume_count:,}")
            
            # Check unique tickers with volume data
            cursor.execute("SELECT COUNT(DISTINCT Ticker) FROM daily_prices WHERE Volume > 0")
            ticker_count = cursor.fetchone()[0]
            print(f"Tickers with volume data: {ticker_count}")
            
            # Check recent volume data
            cursor.execute("""
                SELECT Ticker, Date, Volume 
                FROM daily_prices 
                WHERE Volume > 0 
                ORDER BY Date DESC 
                LIMIT 5
            """)
            recent_data = cursor.fetchall()
            
            print("\nRecent volume data:")
            for ticker, date, volume in recent_data:
                print(f"  {ticker:6} | {date} | {volume:,}")
            
            conn.close()
            print("✅ Database connection test PASSED")
        else:
            print("❌ Database connection test FAILED")
    else:
        print("❌ Database not available")


def test_current_volume_retrieval():
    """Test 2: Current volume retrieval for known tickers"""
    print("\n" + "=" * 60)
    print("TEST 2: Current Volume Retrieval")
    print("=" * 60)
    
    calculator = DatabaseIntegratedVolumeCalculator()
    
    # Test with known tickers that should have volume data
    test_tickers = ['AAPL', 'MSFT', 'NVDA', 'META', 'AMZN']
    
    print(f"Last completed trading day: {get_last_completed_trading_day().strftime('%Y-%m-%d %A')}")
    print()
    
    for ticker in test_tickers:
        print(f"Testing current volume for {ticker}:")
        current_volume = calculator.get_current_volume(ticker)
        
        if current_volume is not None:
            print(f"  ✅ {ticker}: {current_volume:,}")
        else:
            print(f"  ❌ {ticker}: No current volume data")
        print()


def test_volume_benchmarks():
    """Test 3: Volume benchmark calculations for different periods"""
    print("=" * 60)
    print("TEST 3: Volume Benchmark Calculations")
    print("=" * 60)
    
    calculator = DatabaseIntegratedVolumeCalculator()
    
    # Test all benchmark periods
    benchmark_periods = ['10d', '1w', '1m', '60d']
    test_ticker = 'AAPL'  # Use AAPL as it should have comprehensive data
    
    print(f"Testing volume benchmarks for {test_ticker}:")
    print()
    
    for period in benchmark_periods:
        period_info = calculator.VOLUME_BENCHMARK_PERIODS[period]
        trading_days_needed = period_info['trading_days']
        label = period_info['label']
        
        print(f"{label} ({period}) - {trading_days_needed} trading days:")
        
        benchmark_avg = calculator.get_volume_benchmark(test_ticker, period)
        
        if benchmark_avg is not None:
            print(f"  ✅ Benchmark average: {benchmark_avg:,.0f}")
        else:
            print(f"  ❌ Unable to calculate benchmark")
        print()


def test_trading_day_logic():
    """Test 4: Verify trading day calculations are correct"""
    print("=" * 60)
    print("TEST 4: Trading Day Logic Verification")
    print("=" * 60)
    
    # Test different benchmark periods
    periods = ['10d', '1w', '1m', '60d']
    
    current_trading_day = get_last_completed_trading_day()
    print(f"Current (last completed) trading day: {current_trading_day.strftime('%Y-%m-%d %A')}")
    print()
    
    for period in periods:
        trading_days_needed = DatabaseIntegratedVolumeCalculator.VOLUME_BENCHMARK_PERIODS[period]['trading_days']
        
        trading_days = get_last_n_trading_days(current_trading_day, trading_days_needed)
        
        print(f"{period.upper()} ({trading_days_needed} trading days):")
        print(f"  Period: {trading_days[0].strftime('%Y-%m-%d %A')} to {trading_days[-1].strftime('%Y-%m-%d %A')}")
        print(f"  Found: {len(trading_days)}/{trading_days_needed} trading days")
        
        if len(trading_days) == trading_days_needed:
            print(f"  ✅ Trading day calculation correct")
        else:
            print(f"  ❌ Trading day calculation insufficient")
        print()


def test_volume_performance_calculation():
    """Test 5: Volume performance calculation and percentage change formula"""
    print("=" * 60)
    print("TEST 5: Volume Performance Calculations")
    print("=" * 60)
    
    calculator = DatabaseIntegratedVolumeCalculator()
    
    # Test with different tickers and benchmark periods
    test_scenarios = [
        ('AAPL', '10d'),
        ('MSFT', '1w'), 
        ('NVDA', '1m'),
        ('META', '60d')
    ]
    
    for ticker, benchmark_period in test_scenarios:
        print(f"Testing {ticker} with {benchmark_period} benchmark:")
        
        performance_data = calculator.calculate_volume_performance(ticker, benchmark_period)
        
        if not performance_data.get('error', False):
            current_vol = performance_data['current_volume']
            benchmark_avg = performance_data['benchmark_average']
            volume_change = performance_data['volume_change']
            
            # Verify calculation manually
            expected_change = ((current_vol / benchmark_avg) - 1) * 100
            
            print(f"  Current volume: {current_vol:,}")
            print(f"  Benchmark average: {benchmark_avg:,.0f}")
            print(f"  Volume change: {volume_change:+.2f}%")
            print(f"  Manual verification: {expected_change:+.2f}%")
            
            if abs(volume_change - expected_change) < 0.01:  # Allow tiny floating point differences
                print(f"  ✅ Calculation verified correct")
            else:
                print(f"  ❌ Calculation mismatch")
        else:
            print(f"  ❌ Error calculating performance for {ticker}")
        print()


def test_multiple_ticker_processing():
    """Test 6: Multiple ticker processing and group calculations"""
    print("=" * 60)
    print("TEST 6: Multiple Ticker Processing")
    print("=" * 60)
    
    calculator = DatabaseIntegratedVolumeCalculator()
    
    # Test with multiple tickers
    test_tickers = ['AAPL', 'MSFT', 'NVDA', 'META', 'GOOGL']
    benchmark_period = '10d'
    
    print(f"Testing group calculation for {len(test_tickers)} tickers with {benchmark_period} benchmark:")
    print()
    
    # Time the group calculation
    start_time = datetime.now()
    
    group_results = calculator.calculate_volume_performance_for_group(test_tickers, benchmark_period)
    
    end_time = datetime.now()
    calculation_time = (end_time - start_time).total_seconds()
    
    print(f"Group calculation completed in {calculation_time:.2f} seconds")
    print()
    
    # Analyze results
    valid_results = []
    error_results = []
    
    for result in group_results:
        if result.get('error', False):
            error_results.append(result)
        else:
            valid_results.append(result)
    
    print("Results Summary:")
    print(f"  Valid calculations: {len(valid_results)}")
    print(f"  Errors: {len(error_results)}")
    print()
    
    if valid_results:
        print("Valid results:")
        for result in valid_results:
            ticker = result['ticker']
            volume_change = result['volume_change']
            print(f"  {ticker:6}: {volume_change:+6.2f}%")
    
    if error_results:
        print("\nError results:")
        for result in error_results:
            ticker = result['ticker']
            print(f"  {ticker:6}: Error")
    
    # Test summary statistics
    print("\nTesting summary statistics:")
    summary = calculator.get_volume_performance_summary(group_results)
    
    print(f"  Total tickers: {summary['total_count']}")
    print(f"  Valid calculations: {summary['valid_count']}")
    print(f"  Average volume change: {summary['avg_volume_change']:+.2f}%")
    
    if summary['best_performer']:
        best = summary['best_performer']
        print(f"  Best performer: {best['ticker']} ({best['volume_change']:+.2f}%)")
    
    if summary['worst_performer']:
        worst = summary['worst_performer']
        print(f"  Worst performer: {worst['ticker']} ({worst['volume_change']:+.2f}%)")


def test_missing_data_handling():
    """Test 7: Missing data handling and strict validation"""
    print("\n" + "=" * 60)
    print("TEST 7: Missing Data Handling")
    print("=" * 60)
    
    calculator = DatabaseIntegratedVolumeCalculator()
    
    # Test with a ticker that might not exist or have incomplete data
    test_cases = [
        'INVALID_TICKER',  # Should not exist
        'TEST123',         # Should not exist  
    ]
    
    print("Testing missing data scenarios:")
    print()
    
    for ticker in test_cases:
        print(f"Testing {ticker} (should have missing data):")
        
        current_volume = calculator.get_current_volume(ticker)
        benchmark = calculator.get_volume_benchmark(ticker, '10d')
        performance = calculator.calculate_volume_performance(ticker, '10d')
        
        print(f"  Current volume: {current_volume}")
        print(f"  Benchmark average: {benchmark}")
        print(f"  Performance error flag: {performance.get('error', False)}")
        
        if current_volume is None and benchmark is None and performance.get('error', False):
            print(f"  ✅ Missing data handled correctly")
        else:
            print(f"  ❌ Missing data not handled correctly")
        print()


def run_all_tests():
    """Run all volume calculator tests"""
    print("🧪 VOLUME CALCULATOR TEST SUITE")
    print("Testing DatabaseIntegratedVolumeCalculator")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        test_database_connection()
        test_current_volume_retrieval()
        test_volume_benchmarks()
        test_trading_day_logic()
        test_volume_performance_calculation()
        test_multiple_ticker_processing()
        test_missing_data_handling()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
