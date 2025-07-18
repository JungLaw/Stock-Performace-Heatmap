"""
Test for fixing exact date calculation logic across all time periods
Location: tests/test_performance_fix.py
"""

import pytest
import sqlite3
import tempfile
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pandas as pd

# Import the class we're testing
import sys
sys.path.append('../src')
from src.calculations.performance import DatabaseIntegratedPerformanceCalculator

class TestExactDateCalculationFix:
    """Test that all time periods use exact dates, not closest dates"""
    
    def setup_method(self):
        """Set up test database and calculator for each test"""
        # Create temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Create calculator with test database
        self.calculator = DatabaseIntegratedPerformanceCalculator(db_file=self.temp_db.name)
        
        # Create empty table
        conn = sqlite3.connect(self.temp_db.name)
        conn.execute('''
            CREATE TABLE daily_prices (
                Ticker TEXT,
                Date TEXT,
                Open REAL,
                High REAL,
                Low REAL,
                Close REAL,
                "Adj Close" REAL,
                Volume INTEGER
            )
        ''')
        conn.close()
    
    def teardown_method(self):
        """Clean up after each test"""
        os.unlink(self.temp_db.name)
    
    def _calculate_target_date(self, period: str, mock_today: datetime = None) -> datetime:
        """Calculate target date for a given period (mimics calculator logic)"""
        if mock_today is None:
            mock_today = datetime.now()
            
        if period == 'ytd':
            return datetime(mock_today.year, 1, 1)
        else:
            period_days = {
                '1d': 1, '1w': 7, '1m': 30, 
                '3m': 90, '6m': 180, '1y': 365
            }
            days_back = period_days[period]
            return mock_today - timedelta(days=days_back)
    
    def _create_old_data(self, ticker: str, old_date: str, price: float):
        """Helper to insert old data into test database"""
        conn = sqlite3.connect(self.temp_db.name)
        old_data = {
            'Ticker': ticker,
            'Date': old_date,
            'Open': price - 5.0,
            'High': price + 5.0,
            'Low': price - 10.0,
            'Close': price,
            'Adj Close': price,
            'Volume': 1000000
        }
        
        conn.execute('''
            INSERT INTO daily_prices VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(old_data.values()))
        conn.commit()
        conn.close()
    
    def _create_mock_api_data(self, target_date: datetime, target_price: float) -> pd.DataFrame:
        """Helper to create mock yfinance data around target date"""
        # Create 3-day window around target date
        dates = [
            target_date - timedelta(days=1),
            target_date, 
            target_date + timedelta(days=1)
        ]
        
        return pd.DataFrame({
            'Open': [target_price - 5, target_price - 3, target_price - 1],
            'High': [target_price + 5, target_price + 3, target_price + 1], 
            'Low': [target_price - 10, target_price - 8, target_price - 6],
            'Close': [target_price - 2, target_price, target_price + 2],
            'Volume': [2000000, 2100000, 2200000]
        }, index=pd.to_datetime(dates))

    @pytest.mark.parametrize("period", ['1d', '1w', '1m', '3m', '6m', '1y'])
    @pytest.mark.parametrize("ticker", ['NVDA', 'AAPL', 'MSFT'])
    def test_exact_date_logic_all_periods_and_tickers(self, period, ticker):
        """
        MAIN TEST: All periods should use exact dates, not closest dates
        
        Scenario for each period/ticker:
        - Database has old data (before target date)
        - Target date not in database
        - Should fetch exact target date from API
        - Should NOT use closest date from database
        """
        
        # Mock today's date for consistent testing
        mock_today = datetime(2025, 7, 18, 15, 30)  # Fixed point in time
        
        with patch('src.calculations.performance.datetime') as mock_datetime:
            # Mock datetime.now() to return our fixed date
            mock_datetime.now.return_value = mock_today
            mock_datetime.strptime = datetime.strptime  # Keep strptime working
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            # Calculate what the target date should be
            target_date = self._calculate_target_date(period, mock_today)
            target_date_str = target_date.strftime('%Y-%m-%d')
            
            # Step 1: Put old data in database (several days before target)
            old_date = (target_date - timedelta(days=7)).strftime('%Y-%m-%d')
            old_price = 100.0
            self._create_old_data(ticker, old_date, old_price)
            
            # Step 2: Create mock API data with fresh target date price
            target_price = 150.0  # Should get this price, not old_price
            mock_hist_data = self._create_mock_api_data(target_date, target_price)
            
            # Step 3: Mock yfinance API
            with patch('yfinance.Ticker') as mock_ticker:
                mock_stock = MagicMock()
                mock_stock.history.return_value = mock_hist_data
                mock_ticker.return_value = mock_stock
                
                # Step 4: Call the method under test
                result = self.calculator.get_historical_price(ticker, period)
                
                # Step 5: CRITICAL ASSERTIONS
                
                # Should return exact target date price from API
                assert result == target_price, f"Period {period}, Ticker {ticker}: Expected exact API price {target_price}, got {result}"
                
                # Should have called yfinance (exact date not in DB)
                assert mock_ticker.called, f"Period {period}, Ticker {ticker}: Should have called yfinance for missing target date"
                
                # Should NOT return old database price
                assert result != old_price, f"Period {period}, Ticker {ticker}: Should NOT use old database price {old_price}"
                
                # Should NOT return closest date approximation
                # (This is the key test - no "close enough" logic)
                
    def test_exact_date_found_in_database_no_api_call(self):
        """When exact target date EXISTS in DB, should use it (no API call)"""
        
        mock_today = datetime(2025, 7, 18, 15, 30)
        
        with patch('src.calculations.performance.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_today
            mock_datetime.strptime = datetime.strptime
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            # Calculate 1-day target date
            target_date = self._calculate_target_date('1d', mock_today)
            target_date_str = target_date.strftime('%Y-%m-%d')
            
            # Put EXACT target date in database
            exact_price = 175.0
            self._create_old_data('GOOGL', target_date_str, exact_price)
            
            # Should use database price without API call
            with patch('yfinance.Ticker') as mock_ticker:
                result = self.calculator.get_historical_price('GOOGL', '1d')
                
                # Should return exact database price
                assert result == exact_price, f"Expected exact DB price {exact_price}, got {result}"
                
                # Should NOT call yfinance (exact date found)
                assert not mock_ticker.called, "Should NOT call yfinance when exact date exists in DB"

    def test_ytd_special_case(self):
        """YTD should use January 1st as baseline (different logic)"""
        
        mock_today = datetime(2025, 7, 18, 15, 30)
        
        with patch('src.calculations.performance.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_today
            mock_datetime.strptime = datetime.strptime  
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            # YTD target should be January 1, 2025
            expected_ytd_date = datetime(2025, 1, 1)
            ytd_date_str = expected_ytd_date.strftime('%Y-%m-%d')
            
            # Put exact YTD date in database
            ytd_price = 200.0
            self._create_old_data('SPY', ytd_date_str, ytd_price)
            
            # Should find and use January 1st price
            result = self.calculator.get_historical_price('SPY', 'ytd')
            
            assert result == ytd_price, f"YTD should use Jan 1st price {ytd_price}, got {result}"

    @pytest.mark.parametrize("gap_days", [1, 3, 7, 14, 30])
    def test_no_closest_date_fallback_regardless_of_gap(self, gap_days):
        """
        CRITICAL: Should never use closest date fallback, regardless of gap size
        
        This tests the specific bug: current code uses closest date if within 7 days
        """
        
        mock_today = datetime(2025, 7, 18, 15, 30)
        
        with patch('src.calculations.performance.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_today
            mock_datetime.strptime = datetime.strptime
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            # 1-day target date
            target_date = self._calculate_target_date('1d', mock_today)
            
            # Old data with specified gap
            old_date = (target_date - timedelta(days=gap_days)).strftime('%Y-%m-%d')
            old_price = 100.0
            self._create_old_data('TEST', old_date, old_price)
            
            # Mock API with different price
            api_price = 200.0
            mock_hist_data = self._create_mock_api_data(target_date, api_price)
            
            with patch('yfinance.Ticker') as mock_ticker:
                mock_stock = MagicMock()
                mock_stock.history.return_value = mock_hist_data
                mock_ticker.return_value = mock_stock
                
                result = self.calculator.get_historical_price('TEST', '1d')
                
                # Should ALWAYS use API price, never closest date
                # (This will fail with current buggy "within 7 days" logic)
                assert result == api_price, f"Gap {gap_days} days: Should use API price {api_price}, not closest DB price {old_price}"
                assert result != old_price, f"Gap {gap_days} days: Should NEVER use closest date fallback"


if __name__ == "__main__":
    # Quick test runner
    test = TestExactDateCalculationFix()
    
    # Test the main bug with 1-day period  
    test.setup_method()
    try:
        test.test_exact_date_logic_all_periods_and_tickers('1d', 'NVDA')
        print("✅ MAIN TEST PASSED: 1-day calculation uses exact date")
    except AssertionError as e:
        print(f"❌ MAIN TEST FAILED (EXPECTED): {e}")
    except Exception as e:
        print(f"💥 MAIN TEST ERROR: {e}")
    finally:
        test.teardown_method()
    
    # Test the closest date fallback bug specifically
    test2 = TestExactDateCalculationFix()
    test2.setup_method()
    try:
        test2.test_no_closest_date_fallback_regardless_of_gap(6)  # 6 days gap
        print("✅ CLOSEST DATE TEST PASSED: No fallback logic used")
    except AssertionError as e:
        print(f"❌ CLOSEST DATE TEST FAILED (EXPECTED): {e}")
    except Exception as e:
        print(f"💥 CLOSEST DATE TEST ERROR: {e}")
    finally:
        test2.teardown_method()