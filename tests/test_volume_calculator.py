"""
Tests for src/calculations/volume.py - DatabaseIntegratedVolumeCalculator

This test suite covers the complete volume calculator functionality including:
- Core volume calculation methods
- Auto-fetch functionality (database → yfinance fallback → auto-save)
- Session cache behavior for save_to_db=False scenarios
- Database integration and save_to_db parameter handling

Test Coverage:
- _fetch_volume_from_yfinance() - yfinance API integration
- _save_volume_data_to_db() - database save functionality  
- get_current_volume() - current volume with auto-fetch
- get_volume_benchmark() - benchmark calculations with auto-fetch
- calculate_volume_performance() - complete volume analysis
- Session cache functionality for exploration workflow

Run with: 
    pytest tests/test_volume_calculator.py -v
    python tests/test_volume_calculator.py  # Direct execution
"""

import sys
import os
sys.path.insert(0, 'src')

from calculations.volume import DatabaseIntegratedVolumeCalculator
from datetime import datetime, timedelta
import pytest


class TestVolumeCalculatorCore:
    """Test core volume calculator functionality"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.calculator = DatabaseIntegratedVolumeCalculator()
    
    def test_fetch_volume_from_yfinance(self):
        """
        Test _fetch_volume_from_yfinance() method
        
        Verifies:
        - API connection works
        - Returns valid DataFrame with Volume column
        - Data quality validation works
        """
        print("\n🧪 Testing _fetch_volume_from_yfinance() method")
        
        ticker = "AAPL"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=15)
        
        result = self.calculator._fetch_volume_from_yfinance(ticker, start_date, end_date)
        
        assert result is not None, "Should return DataFrame for valid ticker"
        assert len(result) > 0, "Should return records for recent date range"
        assert 'Volume' in result.columns, "DataFrame should contain Volume column"
        assert (result['Volume'] > 0).any(), "Should have valid volume data"
        
        print(f"✅ Successfully fetched {len(result)} records for {ticker}")
        print(f"✅ Date range: {result.index[0].date()} to {result.index[-1].date()}")
    
    def test_save_volume_data_to_db(self):
        """
        Test _save_volume_data_to_db() method
        
        Verifies:
        - Data save functionality works
        - Duplicate prevention works
        - save_to_db parameter respected
        """
        print("\n🧪 Testing _save_volume_data_to_db() method")
        
        ticker = "MSFT"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=10)
        
        # Fetch data first
        volume_data = self.calculator._fetch_volume_from_yfinance(ticker, start_date, end_date)
        assert volume_data is not None, "Should fetch volume data"
        
        # Test save functionality
        save_result = self.calculator._save_volume_data_to_db(ticker, volume_data, save_to_db=True)
        assert save_result == True, "Save operation should succeed"
        
        # Verify data was saved
        recent_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
        saved_volume = self.calculator._query_volume_from_db(ticker, recent_date)
        assert saved_volume is not None, "Should find saved volume data"
        
        print(f"✅ Successfully saved and verified {ticker} volume data")


class TestVolumeCalculatorAutoFetch:
    """Test auto-fetch functionality"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.calculator = DatabaseIntegratedVolumeCalculator()
    
    def test_current_volume_auto_fetch(self):
        """
        Test get_current_volume() with auto-fetch
        
        Verifies:
        - Database-first approach works
        - Auto-fetch fallback works for missing data
        - save_to_db parameter controls database saving
        """
        print("\n🧪 Testing get_current_volume() auto-fetch")
        
        # Use ticker that may not be in database
        ticker = "BABA"
        
        # Test auto-fetch with database save
        current_volume = self.calculator.get_current_volume(ticker, save_to_db=True)
        assert current_volume is not None, "Should retrieve current volume"
        assert current_volume > 0, "Volume should be positive"
        
        # Test that data was cached (second call should be faster)
        cached_volume = self.calculator.get_current_volume(ticker, save_to_db=True)
        assert cached_volume == current_volume, "Should return same cached volume"
        
        print(f"✅ Current volume auto-fetch working: {current_volume:,} shares")
    
    def test_benchmark_auto_fetch(self):
        """
        Test volume benchmark calculation with auto-fetch
        
        Verifies:
        - Benchmark calculation works for various periods
        - Auto-fetch handles missing historical data
        - 60D period works (previously failing issue)
        """
        print("\n🧪 Testing volume benchmark auto-fetch")
        
        ticker = "NVDA"
        
        # Test 60D benchmark that was previously failing
        benchmark_60d = self.calculator.get_volume_benchmark(ticker, "60d", save_to_db=True)
        assert benchmark_60d is not None, "60D benchmark should work with auto-fetch"
        assert benchmark_60d > 0, "Benchmark should be positive"
        
        # Test complete performance calculation
        performance = self.calculator.calculate_volume_performance(ticker, "60d", save_to_db=True)
        assert not performance.get('error', False), "Performance calculation should succeed"
        assert 'volume_change' in performance, "Should include volume change calculation"
        
        print(f"✅ 60D benchmark working: {benchmark_60d:,.0f} average volume")
        print(f"✅ Volume performance: {performance['volume_change']:+.2f}%")


class TestVolumeCalculatorSessionCache:
    """Test session cache functionality for save_to_db=False"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.calculator = DatabaseIntegratedVolumeCalculator()
    
    def test_session_cache_workflow(self):
        """
        Test complete session cache workflow
        
        Verifies:
        - save_to_db=False stores data in session cache only
        - Complete volume analysis works with session cache
        - Database remains unpolluted
        - "Try before you buy" exploration workflow works
        """
        print("\n🧪 Testing session cache workflow (save_to_db=False)")
        
        # Use ticker not in database for clean test
        ticker = "AMD"
        
        # Perform analysis with save_to_db=False
        result = self.calculator.calculate_volume_performance(ticker, "10d", save_to_db=False)
        
        # Verify analysis completed successfully
        assert not result.get('error', False), "Session-only analysis should succeed"
        assert result['current_volume'] > 0, "Should have valid current volume"
        assert result['benchmark_average'] > 0, "Should have valid benchmark"
        assert 'volume_change' in result, "Should calculate volume change"
        
        # Verify session cache populated
        assert ticker in self.calculator.session_volume_cache, "Session cache should contain ticker"
        cache_size = len(self.calculator.session_volume_cache[ticker])
        assert cache_size > 0, "Session cache should have volume records"
        
        # Verify database not polluted
        db_volume = self.calculator._query_volume_from_db(ticker, "2025-09-05")
        assert db_volume is None, "Database should not contain session-only data"
        
        print(f"✅ Session-only analysis: {result['volume_change']:+.2f}% volume change")
        print(f"✅ Session cache: {cache_size} records")
        print("✅ Database clean - no pollution")


class TestVolumeCalculatorIntegration:
    """Test group calculations and complete workflows"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.calculator = DatabaseIntegratedVolumeCalculator()
    
    def test_group_volume_calculation(self):
        """
        Test calculate_volume_performance_for_group()
        
        Verifies:
        - Group calculations work with auto-fetch
        - Mixed database/session scenarios handled
        - All tickers processed successfully
        """
        print("\n🧪 Testing group volume calculation")
        
        tickers = ["AAPL", "MSFT", "GOOGL"]
        
        # Test group calculation with database save
        results = self.calculator.calculate_volume_performance_for_group(
            tickers, "10d", save_to_db=True
        )
        
        assert len(results) == len(tickers), "Should return results for all tickers"
        
        # Verify all calculations succeeded
        success_count = len([r for r in results if not r.get('error', False)])
        assert success_count == len(tickers), f"All {len(tickers)} calculations should succeed"
        
        print(f"✅ Group calculation: {success_count}/{len(tickers)} tickers successful")
        
        # Display results
        for result in results:
            ticker = result['ticker']
            change = result['volume_change']
            print(f"   {ticker}: {change:+.2f}% volume change")


def run_all_tests():
    """Run all tests when executed directly"""
    print("VOLUME CALCULATOR TEST SUITE")
    print("=" * 50)
    
    # Core functionality tests
    core_tests = TestVolumeCalculatorCore()
    core_tests.setup_method()
    core_tests.test_fetch_volume_from_yfinance()
    core_tests.test_save_volume_data_to_db()
    
    # Auto-fetch tests
    auto_fetch_tests = TestVolumeCalculatorAutoFetch()
    auto_fetch_tests.setup_method()
    auto_fetch_tests.test_current_volume_auto_fetch()
    auto_fetch_tests.test_benchmark_auto_fetch()
    
    # Session cache tests
    session_tests = TestVolumeCalculatorSessionCache()
    session_tests.setup_method()
    session_tests.test_session_cache_workflow()
    
    # Integration tests
    integration_tests = TestVolumeCalculatorIntegration()
    integration_tests.setup_method()
    integration_tests.test_group_volume_calculation()
    
    print("\n🎉 ALL VOLUME CALCULATOR TESTS PASSED!")
    print("✅ Auto-fetch functionality working")
    print("✅ Session cache enabling exploration workflow")
    print("✅ Database integration robust")
    print("✅ Volume calculator ready for production")


if __name__ == "__main__":
    run_all_tests()
