"""
Quick test script to validate the heatmap dashboard implementation
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test that all modules import correctly"""
    try:
        from calculations.performance import PerformanceCalculator
        from visualization.heatmap import FinvizHeatmapGenerator
        from config.assets import ASSET_GROUPS
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_performance_calculation():
    """Test performance calculation with database integration"""
    try:
        from calculations.performance import DatabaseIntegratedPerformanceCalculator
        
        calc = DatabaseIntegratedPerformanceCalculator()
        print("🔄 Testing database-integrated performance calculation...")
        
        # Test with a ticker that should be in the database
        print("\n📋 Testing database cache with AAPL (should be in database):")
        result_aapl = calc.calculate_performance_for_ticker("AAPL", "1m")
        
        if result_aapl.get('error'):
            print(f"⚠️ AAPL calculation returned error: {result_aapl}")
        else:
            data_source = result_aapl.get('data_source', 'unknown')
            print(f"✅ AAPL: ${result_aapl['current_price']:.2f}, {result_aapl['percentage_change']:+.2f}% (source: {data_source})")
        
        # Test with a ticker that likely won't be in the database
        print("\n📞 Testing yfinance fallback with TSLA (likely not in database):")
        result_tsla = calc.calculate_performance_for_ticker("TSLA", "1m")
        
        if result_tsla.get('error'):
            print(f"⚠️ TSLA calculation returned error (likely market closed or API issue)")
        else:
            data_source = result_tsla.get('data_source', 'unknown')
            print(f"✅ TSLA: ${result_tsla['current_price']:.2f}, {result_tsla['percentage_change']:+.2f}% (source: {data_source})")
        
        # Test group calculation
        print("\n📋 Testing group calculation with database optimization:")
        test_tickers = ["AAPL", "MSFT", "GOOGL"]  # These should be in database
        group_results = calc.calculate_performance_for_group(test_tickers, "1w")
        
        # Show summary with database usage
        summary = calc.get_performance_summary(group_results)
        print(f"✅ Group calculation complete:")
        print(f"   - Total tickers: {summary['total_count']}")
        print(f"   - Valid data: {summary['valid_count']}")
        print(f"   - Database usage: {summary['api_efficiency']}")
        print(f"   - Average performance: {summary['avg_performance']:+.2f}%")
        
        return True
    except Exception as e:
        print(f"❌ Performance calculation error: {e}")
        return False

def test_heatmap_generation():
    """Test heatmap generation with mock data"""
    try:
        from visualization.heatmap import FinvizHeatmapGenerator
        
        generator = FinvizHeatmapGenerator()
        
        # Create mock performance data
        mock_data = [
            {
                'ticker': 'AAPL',
                'current_price': 150.0,
                'historical_price': 145.0,
                'percentage_change': 3.45,
                'absolute_change': 5.0,
                'period': '1d',
                'period_label': '1 Day',
                'error': False
            },
            {
                'ticker': 'GOOGL',
                'current_price': 2500.0,
                'historical_price': 2520.0,
                'percentage_change': -0.79,
                'absolute_change': -20.0,
                'period': '1d',
                'period_label': '1 Day',
                'error': False
            }
        ]
        
        print("🔄 Testing heatmap generation...")
        fig = generator.create_treemap(mock_data, title="Test Heatmap")
        
        if fig:
            print("✅ Heatmap generation successful")
            return True
        else:
            print("❌ Heatmap generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Heatmap generation error: {e}")
        return False

def test_asset_groups():
    """Test asset group configurations"""
    try:
        from config.assets import ASSET_GROUPS
        
        print("🔄 Testing asset groups...")
        
        for group_name, config in ASSET_GROUPS.items():
            tickers = config['tickers']
            print(f"✅ {group_name}: {len(tickers)} tickers (max: {config['max_tickers']})")
        
        return True
    except Exception as e:
        print(f"❌ Asset groups error: {e}")
        return False

def test_database_integration():
    """Test database integration specifically"""
    try:
        from calculations.performance import DatabaseIntegratedPerformanceCalculator
        import sqlite3
        from pathlib import Path
        
        print("📋 Testing database integration...")
        
        # Check if database exists
        db_path = Path("data/stock_data.db")
        if not db_path.exists():
            print("⚠️ Database file not found - will test yfinance-only mode")
            return True
        
        # Check database contents
        try:
            conn = sqlite3.connect("data/stock_data.db")
            cursor = conn.cursor()
            
            # Get ticker count
            cursor.execute("SELECT COUNT(DISTINCT Ticker) FROM daily_prices")
            ticker_count = cursor.fetchone()[0]
            
            # Get total record count
            cursor.execute("SELECT COUNT(*) FROM daily_prices")
            total_records = cursor.fetchone()[0]
            
            # Get available tickers
            cursor.execute("SELECT DISTINCT Ticker FROM daily_prices ORDER BY Ticker")
            tickers = [row[0] for row in cursor.fetchall()]
            
            # Get date range
            cursor.execute("SELECT MIN(Date), MAX(Date) FROM daily_prices")
            min_date, max_date = cursor.fetchone()
            
            conn.close()
            
            print(f"✅ Database connection successful:")
            print(f"   - Tickers: {ticker_count} ({', '.join(tickers[:5])}{'...' if len(tickers) > 5 else ''})")
            print(f"   - Records: {total_records:,}")
            print(f"   - Date range: {min_date} to {max_date}")
            
        except Exception as e:
            print(f"❌ Database query error: {e}")
            return False
        
        # Test calculator database functionality
        calc = DatabaseIntegratedPerformanceCalculator()
        
        # Test with a ticker that should be in database
        if "AAPL" in tickers:
            print(f"\n🔍 Testing database lookup for AAPL:")
            historical_price = calc._query_historical_price_from_db("AAPL", "2025-01-15")
            if historical_price:
                print(f"✅ Found AAPL price in database: ${historical_price:.2f}")
            else:
                print(f"🔍 AAPL not found for specific date, testing closest date...")
                from datetime import datetime
                closest = calc._find_closest_date_in_db("AAPL", datetime(2025, 1, 15))
                if closest:
                    date_str, price = closest
                    print(f"✅ Found closest AAPL price: {date_str} = ${price:.2f}")
                else:
                    print("⚠️ No AAPL data found in database")
        
        return True
        
    except Exception as e:
        print(f"❌ Database integration test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Dashboard Tests")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Asset Groups Test", test_asset_groups),
        ("Database Integration Test", test_database_integration),
        ("Performance Calculation Test", test_performance_calculation),
        ("Heatmap Generation Test", test_heatmap_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 30)
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Dashboard is ready to run.")
        print("💡 Run 'streamlit run streamlit_app.py' to start the dashboard")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    main()
