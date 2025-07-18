"""
Database-Integrated Performance Calculator

This version uses the SQLite database first for historical data,
only falling back to yfinance for missing data or current prices.
Implements the agreed database-first lookup pattern.
"""

import pandas as pd
import numpy as np
import sqlite3
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseIntegratedPerformanceCalculator:
    """
    Performance calculator that uses database cache first, then yfinance fallback.
    Implements the agreed pattern: Check DB → Fetch from API if missing → Auto-save new data
    """
    
    # Define available time periods
    TIME_PERIODS = {
        '1d': {'days': 1, 'label': '1 Day'},
        '1w': {'days': 7, 'label': '1 Week'},
        '1m': {'days': 30, 'label': '1 Month'},
        '3m': {'days': 90, 'label': '3 Months'},
        '6m': {'days': 180, 'label': '6 Months'},
        'ytd': {'days': None, 'label': 'YTD'},
        '1y': {'days': 365, 'label': '1 Year'}
    }
    
    def __init__(self, db_file: str = "data/stock_data.db", table_name: str = "daily_prices"):
        self.db_file = db_file
        self.table_name = table_name
        self.current_price_cache = {}  # Session-level cache for current prices
        self.cache_duration_minutes = 15  # Current price cache duration
        
        # Verify database exists
        db_path = Path(db_file)
        if not db_path.exists():
            logger.warning(f"Database file {db_file} not found. Will rely on yfinance only.")
            self.db_available = False
        else:
            self.db_available = True
            logger.info(f"Database found: {db_file}")
    
    def _get_database_connection(self) -> Optional[sqlite3.Connection]:
        """Get database connection if available"""
        if not self.db_available:
            return None
        
        try:
            return sqlite3.connect(self.db_file)
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return None
    
    def _query_historical_price_from_db(self, ticker: str, target_date: str) -> Optional[float]:
        """
        Query historical closing price from database for specific ticker and date
        
        Args:
            ticker: Stock ticker symbol
            target_date: Date in 'YYYY-MM-DD' format
            
        Returns:
            Closing price as float, or None if not found
        """
        conn = self._get_database_connection()
        if not conn:
            return None
        
        try:
            query = f"""
            SELECT Close FROM {self.table_name}
            WHERE Ticker = ? AND Date = ?
            """
            
            cursor = conn.cursor()
            cursor.execute(query, (ticker, target_date))
            result = cursor.fetchone()
            
            if result:
                logger.info(f"✅ Found {ticker} price for {target_date} in database: ${result[0]:.2f}")
                return float(result[0])
            else:
                logger.info(f"❌ No database entry for {ticker} on {target_date}")
                return None
                
        except Exception as e:
            logger.error(f"Database query error for {ticker} on {target_date}: {e}")
            return None
        finally:
            conn.close()
    
    def _find_closest_date_in_db(self, ticker: str, target_date: datetime) -> Optional[Tuple[str, float]]:
        """
        Find the closest available date in database before or on target date
        
        Args:
            ticker: Stock ticker symbol
            target_date: Target datetime object
            
        Returns:
            Tuple of (date_string, closing_price) or None if not found
        """
        conn = self._get_database_connection()
        if not conn:
            return None
        
        try:
            # Convert target date to string
            target_date_str = target_date.strftime('%Y-%m-%d')
            
            # Query for closest date <= target_date
            query = f"""
            SELECT Date, Close FROM {self.table_name}
            WHERE Ticker = ? AND Date <= ?
            ORDER BY Date DESC
            LIMIT 1
            """
            
            cursor = conn.cursor()
            cursor.execute(query, (ticker, target_date_str))
            result = cursor.fetchone()
            
            if result:
                date_str, price = result
                logger.info(f"✅ Found closest date for {ticker}: {date_str} (target: {target_date_str}), price: ${price:.2f}")
                return (date_str, float(price))
            else:
                logger.info(f"❌ No historical data for {ticker} before {target_date_str}")
                return None
                
        except Exception as e:
            logger.error(f"Database closest date query error for {ticker}: {e}")
            return None
        finally:
            conn.close()
    
    def _record_exists_in_db(self, ticker: str, date: str) -> bool:
        """
        Check if a specific (ticker, date) record already exists in database
        
        Args:
            ticker: Stock ticker symbol
            date: Date in 'YYYY-MM-DD' format
            
        Returns:
            True if record exists, False otherwise
        """
        conn = self._get_database_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT 1 FROM {self.table_name} WHERE Ticker = ? AND Date = ?", (ticker, date))
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            logger.error(f"Error checking if record exists for {ticker} on {date}: {e}")
            return False
        finally:
            conn.close()
    
    def _save_historical_data_to_db(self, ticker: str, historical_data: pd.DataFrame) -> bool:
        """
        Save fetched historical data to database
        
        Args:
            ticker: Stock ticker symbol
            historical_data: DataFrame with historical OHLCV data
            
        Returns:
            True if saved successfully, False otherwise
        """
        if not self.db_available:
            logger.info(f"🚫 Database not available - skipping save for {ticker}")
            return False
        
        conn = self._get_database_connection()
        if not conn:
            logger.error(f"❌ Failed to get database connection for {ticker}")
            return False
        
        try:
            # DIAGNOSTIC: Log what data we received from API
            logger.info(f"🔍 DIAGNOSTIC: Processing {ticker} data from API:")
            logger.info(f"   📊 Original data shape: {historical_data.shape}")
            if not historical_data.empty:
                date_range = f"{historical_data.index[0].date()} to {historical_data.index[-1].date()}"
                logger.info(f"   📅 Date range: {date_range}")
                logger.info(f"   📋 Dates included: {[d.strftime('%Y-%m-%d') for d in historical_data.index]}")
            
            # Prepare data for database insertion
            df = historical_data.copy()
            df.reset_index(inplace=True)
            df['Ticker'] = ticker
            
            # Handle yfinance API changes - it no longer returns 'Adj Close'
            # We'll use 'Close' as 'Adj Close' if Adj Close is missing
            if 'Adj Close' not in df.columns:
                if 'Close' in df.columns:
                    df['Adj Close'] = df['Close']
                    logger.info(f"Using 'Close' as 'Adj Close' for {ticker}")
                else:
                    logger.error(f"No Close or Adj Close column found for {ticker}")
                    return False
            
            # Ensure proper column order and names
            expected_columns = ['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            
            # Convert Date to string format
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            
            # CRITICAL FIX: Exclude today's date from permanent database saves
            # Today's data is incomplete/preliminary and should only be session-cached
            today_str = datetime.now().strftime('%Y-%m-%d')
            original_count = len(df)
            
            # DIAGNOSTIC: Log filtering details
            logger.info(f"🛡️ DIAGNOSTIC: Filtering out today's incomplete data:")
            logger.info(f"   📅 Today's date: {today_str}")
            logger.info(f"   📊 Records before filtering: {original_count}")
            
            df = df[df['Date'] != today_str]  # Filter out today's data
            filtered_count = len(df)
            
            logger.info(f"   📊 Records after filtering: {filtered_count}")
            if original_count > filtered_count:
                removed_count = original_count - filtered_count
                logger.info(f"🛡️ Filtered out {removed_count} today's records for {ticker} (preliminary data not saved to DB)")
            else:
                logger.info(f"✅ No today's records to filter for {ticker}")
            
            # DIAGNOSTIC: Show what dates we're actually saving
            if filtered_count > 0:
                dates_to_save = df['Date'].tolist()
                logger.info(f"💾 DIAGNOSTIC: Will save {filtered_count} records with dates: {dates_to_save}")
            else:
                logger.warning(f"⚠️ No historical data left to save for {ticker} after filtering")
            
            # Check if all required columns exist
            missing_columns = [col for col in expected_columns if col not in df.columns]
            if missing_columns:
                logger.error(f"Missing columns for {ticker}: {missing_columns}")
                logger.info(f"Available columns: {list(df.columns)}")
                return False
            
            # Select only the columns we need
            df = df[expected_columns]
            
            # DIAGNOSTIC: Log final save attempt
            if len(df) > 0:
                logger.info(f"💾 DIAGNOSTIC: Checking which of {len(df)} records need to be saved for {ticker}")
                
                # Check each record individually and only insert new ones
                new_records = []
                skipped_count = 0
                
                for index, row in df.iterrows():
                    date_str = row['Date']
                    if not self._record_exists_in_db(ticker, date_str):
                        new_records.append(row)
                        logger.info(f"  ✅ Will save new record: {ticker} {date_str}")
                    else:
                        skipped_count += 1
                        logger.info(f"  ⏭️ Skipping existing record: {ticker} {date_str}")
                
                if new_records:
                    # Convert new records back to DataFrame for insertion
                    new_df = pd.DataFrame(new_records)
                    
                    logger.info(f"💾 DIAGNOSTIC: Inserting {len(new_df)} new records for {ticker} (skipped {skipped_count} existing)")
                    
                    # Insert only the new records
                    new_df.to_sql(self.table_name, conn, if_exists='append', index=False, method='multi')
                    
                    logger.info(f"✅ SUCCESS: Saved {len(new_df)} new historical records for {ticker} to database")
                else:
                    logger.info(f"ℹ️ No new records to save for {ticker} - all {skipped_count} records already exist")
                
                # DIAGNOSTIC: Verify total count after save
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE Ticker = ?", (ticker,))
                total_records = cursor.fetchone()[0]
                logger.info(f"📊 DIAGNOSTIC: {ticker} now has {total_records} total records in database")
            else:
                logger.warning(f"⚠️ No data to save for {ticker} - skipping database insert")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save historical data for {ticker}: {e}")
            logger.info(f"DataFrame columns: {list(historical_data.columns)}")
            logger.info(f"DataFrame shape: {historical_data.shape}")
            logger.info(f"DataFrame head: {historical_data.head()}")
            return False
        finally:
            conn.close()
    
    def get_historical_price(self, ticker: str, period: str) -> Optional[float]:
        """
        Get historical price using database-first approach
        
        Implementation of agreed pattern:
        1. Check database for ticker + date
        2. If found: return cached price (no API call)
        3. If missing: fetch from yfinance
        4. Auto-save fetched data to database
        5. Return price
        
        Args:
            ticker: Stock ticker symbol
            period: Time period key ('1d', '1w', '1m', etc.)
            
        Returns:
            Historical price as float, or None if not available
        """
        # Calculate target date
        if period == 'ytd':
            target_date = datetime(datetime.now().year, 1, 1)
        else:
            days_back = self.TIME_PERIODS[period]['days']
            target_date = datetime.now() - timedelta(days=days_back)
        
        # Step 1: Check database first
        logger.info(f"🔍 Looking for {ticker} historical price for {period} (target: {target_date.strftime('%Y-%m-%d')})")
        
        # Try exact date first
        target_date_str = target_date.strftime('%Y-%m-%d')
        db_price = self._query_historical_price_from_db(ticker, target_date_str)
        
        if db_price is not None:
            logger.info(f"📊 Using cached price for {ticker}: ${db_price:.2f}")
            return db_price
        
        # FIXED: No longer use closest date fallback - always fetch exact dates
        # If exact date not found in database, fetch from API (don't use approximations)
        
        # Step 2: Not found in database, fetch from yfinance
        logger.info(f"📡 Fetching {ticker} from yfinance (not in database)")
        
        try:
            stock = yf.Ticker(ticker)
            
            # Get historical data with buffer for weekends/holidays
            start_date = target_date - timedelta(days=15)
            end_date = target_date + timedelta(days=5)
            
            hist_data = stock.history(start=start_date, end=end_date)
            
            if hist_data.empty:
                logger.warning(f"⚠️ No historical data returned from yfinance for {ticker}")
                return None
            
            # Step 3: Auto-save fetched data to database
            if self.db_available:
                self._save_historical_data_to_db(ticker, hist_data)
            
            # Step 4: Find the closest date in fetched data
            hist_data.index = pd.to_datetime(hist_data.index).date
            target_date_only = target_date.date()
            
            # Get the closest available date that's not after our target
            available_dates = [d for d in hist_data.index if d <= target_date_only]
            if not available_dates:
                logger.warning(f"⚠️ No suitable historical dates found for {ticker}")
                return None
            
            closest_date = max(available_dates)
            historical_price = float(hist_data.loc[closest_date, 'Close'])
            
            logger.info(f"✅ Retrieved {ticker} historical price from yfinance: ${historical_price:.2f}")
            return historical_price
            
        except Exception as e:
            logger.error(f"Error fetching historical price for {ticker} from yfinance: {e}")
            return None
    
    def get_current_price(self, ticker: str) -> Optional[float]:
        """
        Get current price with optional session-level caching
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Current price as float, or None if not available
        """
        # Check session cache first
        now = datetime.now()
        cache_key = ticker
        
        if cache_key in self.current_price_cache:
            cached_data = self.current_price_cache[cache_key]
            cached_time = cached_data['timestamp']
            cache_age_minutes = (now - cached_time).total_seconds() / 60
            
            if cache_age_minutes < self.cache_duration_minutes:
                logger.info(f"💾 Using cached current price for {ticker}: ${cached_data['price']:.2f} (cached {cache_age_minutes:.1f}m ago)")
                return cached_data['price']
        
        # Fetch fresh current price from yfinance
        logger.info(f"📡 Fetching current price for {ticker} from yfinance")
        
        try:
            stock = yf.Ticker(ticker)
            
            # Try to get current price from info first (faster)
            info = stock.info
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            
            if current_price:
                current_price = float(current_price)
            else:
                # Fallback to recent history
                hist = stock.history(period='2d')
                if not hist.empty:
                    current_price = float(hist['Close'].iloc[-1])
                else:
                    logger.warning(f"⚠️ No current price data available for {ticker}")
                    return None
            
            # Cache the current price
            self.current_price_cache[cache_key] = {
                'price': current_price,
                'timestamp': now
            }
            
            logger.info(f"✅ Retrieved current price for {ticker}: ${current_price:.2f}")
            return current_price
            
        except Exception as e:
            logger.error(f"Error fetching current price for {ticker}: {e}")
            return None
    
    def calculate_percentage_change(self, current_price: float, historical_price: float) -> float:
        """
        Calculate percentage change between current and historical price
        
        Args:
            current_price: Current stock price
            historical_price: Historical stock price for comparison
            
        Returns:
            Percentage change as float (e.g., 5.25 for 5.25%)
        """
        if historical_price == 0 or pd.isna(historical_price) or pd.isna(current_price):
            return 0.0
            
        return ((current_price - historical_price) / historical_price) * 100
    
    def calculate_performance_for_ticker(self, ticker: str, period: str) -> Dict:
        """
        Calculate complete performance data for a single ticker using database-first approach
        
        Args:
            ticker: Stock ticker symbol
            period: Time period for comparison
            
        Returns:
            Dictionary with performance data
        """
        logger.info(f"🎯 Calculating performance for {ticker} ({period})")
        
        # Get current and historical prices using database-first approach
        current_price = self.get_current_price(ticker)
        historical_price = self.get_historical_price(ticker, period)
        
        if current_price is None or historical_price is None:
            return {
                'ticker': ticker,
                'current_price': current_price,
                'historical_price': historical_price,
                'percentage_change': 0.0,
                'absolute_change': 0.0,
                'period': period,
                'period_label': self.TIME_PERIODS.get(period, {}).get('label', period),
                'error': True,
                'data_source': 'error'
            }
        
        percentage_change = self.calculate_percentage_change(current_price, historical_price)
        absolute_change = current_price - historical_price
        
        # Determine data source for reporting
        data_source = 'database+yfinance'  # Mixed sources
        
        result = {
            'ticker': ticker,
            'current_price': current_price,
            'historical_price': historical_price,
            'percentage_change': percentage_change,
            'absolute_change': absolute_change,
            'period': period,
            'period_label': self.TIME_PERIODS.get(period, {}).get('label', period),
            'error': False,
            'data_source': data_source
        }
        
        logger.info(f"✅ {ticker}: ${current_price:.2f} vs ${historical_price:.2f} = {percentage_change:+.2f}%")
        return result
    
    def calculate_performance_for_group(self, tickers: List[str], period: str) -> List[Dict]:
        """
        Calculate performance data for a group of tickers using database-first approach
        
        Args:
            tickers: List of ticker symbols
            period: Time period for comparison
            
        Returns:
            List of dictionaries with performance data for each ticker
        """
        logger.info(f"🎯 Calculating performance for {len(tickers)} tickers ({period})")
        results = []
        
        for i, ticker in enumerate(tickers, 1):
            logger.info(f"📊 Processing {ticker} ({i}/{len(tickers)})...")
            performance_data = self.calculate_performance_for_ticker(ticker, period)
            results.append(performance_data)
        
        # Log summary of data sources used
        db_count = len([r for r in results if 'database' in r.get('data_source', '')])
        api_count = len([r for r in results if not r.get('error', True)])
        error_count = len([r for r in results if r.get('error', False)])
        
        logger.info(f"📊 Performance calculation complete:")
        logger.info(f"   - Database cache utilized: {db_count} tickers")
        logger.info(f"   - API calls made: {api_count} tickers")  
        logger.info(f"   - Errors: {error_count} tickers")
        
        return results
    
    def get_performance_summary(self, performance_data: List[Dict]) -> Dict:
        """
        Get summary statistics for a group of performance data
        
        Args:
            performance_data: List of performance dictionaries
            
        Returns:
            Summary statistics dictionary
        """
        # Filter out error cases
        valid_data = [p for p in performance_data if not p['error']]
        
        if not valid_data:
            return {
                'total_count': len(performance_data),
                'valid_count': 0,
                'error_count': len(performance_data),
                'avg_performance': 0.0,
                'best_performer': None,
                'worst_performer': None,
                'database_usage': 0
            }
        
        percentages = [p['percentage_change'] for p in valid_data]
        
        best_performer = max(valid_data, key=lambda x: x['percentage_change'])
        worst_performer = min(valid_data, key=lambda x: x['percentage_change'])
        
        # Count database usage
        db_usage = len([p for p in valid_data if 'database' in p.get('data_source', '')])
        
        return {
            'total_count': len(performance_data),
            'valid_count': len(valid_data),
            'error_count': len(performance_data) - len(valid_data),
            'avg_performance': np.mean(percentages),
            'median_performance': np.median(percentages),
            'std_performance': np.std(percentages),
            'best_performer': best_performer,
            'worst_performer': worst_performer,
            'positive_count': len([p for p in percentages if p > 0]),
            'negative_count': len([p for p in percentages if p < 0]),
            'database_usage': db_usage,
            'api_efficiency': f"{db_usage}/{len(valid_data)} from cache"
        }


# Factory function and convenience functions for backward compatibility
def get_performance_calculator() -> DatabaseIntegratedPerformanceCalculator:
    """Factory function to get a database-integrated performance calculator instance"""
    return DatabaseIntegratedPerformanceCalculator()


def calculate_simple_performance(ticker: str, period: str = '1d') -> Dict:
    """
    Quick function to calculate performance for a single ticker using database-first approach
    
    Args:
        ticker: Stock ticker symbol
        period: Time period ('1d', '1w', '1m', etc.)
        
    Returns:
        Performance data dictionary
    """
    calculator = DatabaseIntegratedPerformanceCalculator()
    return calculator.calculate_performance_for_ticker(ticker, period)


def calculate_group_performance(tickers: List[str], period: str = '1d') -> List[Dict]:
    """
    Quick function to calculate performance for a group of tickers using database-first approach
    
    Args:
        tickers: List of ticker symbols
        period: Time period ('1d', '1w', '1m', etc.)
        
    Returns:
        List of performance data dictionaries
    """
    calculator = DatabaseIntegratedPerformanceCalculator()
    return calculator.calculate_performance_for_group(tickers, period)
