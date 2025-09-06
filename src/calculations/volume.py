"""
Database-Integrated Volume Calculator

Volume analysis and calculations using database-first approach.
Follows the same pattern as DatabaseIntegratedPerformanceCalculator
with strict date validation for accurate volume benchmark calculations.
"""

import pandas as pd
import numpy as np
import sqlite3
import yfinance as yf
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import logging

# Import trading day logic from performance module
from .performance import (
    get_last_completed_trading_day,
    get_last_n_trading_days,
    is_us_trading_day,
    get_trading_day_target
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseIntegratedVolumeCalculator:
    """
    Volume calculator that uses database cache first, then yfinance fallback.
    Implements strict date validation for accurate volume benchmark calculations.
    """
    
    # Define available volume benchmark periods
    VOLUME_BENCHMARK_PERIODS = {
        '10d': {'trading_days': 10, 'label': '10 Days'},
        '1w': {'trading_days': 5, 'label': '1 Week'},
        '1m': {'trading_days': 22, 'label': '1 Month'},
        '60d': {'trading_days': 60, 'label': '3 Months'}
    }
    
    def __init__(self, db_file: str = "data/stock_data.db", table_name: str = "daily_prices"):
        self.db_file = db_file
        self.table_name = table_name
        
        # Session-level cache for volume data when save_to_db=False
        self.session_volume_cache = {}  # {ticker: {date: volume, date2: volume2, ...}}
        
        # Verify database exists
        db_path = Path(db_file)
        if not db_path.exists():
            logger.warning(f"Database file {db_file} not found. Will rely on yfinance only.")
            self.db_available = False
        else:
            self.db_available = True
            logger.info(f"Volume calculator initialized with database: {db_file}")
    
    def _get_database_connection(self) -> Optional[sqlite3.Connection]:
        """Get database connection if available"""
        if not self.db_available:
            return None
        
        try:
            return sqlite3.connect(self.db_file)
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return None
    
    def _add_to_session_cache(self, ticker: str, historical_data: pd.DataFrame) -> None:
        """
        Add volume data to session cache for save_to_db=False scenarios
        
        Args:
            ticker: Stock ticker symbol
            historical_data: DataFrame with historical OHLCV data
        """
        if ticker not in self.session_volume_cache:
            self.session_volume_cache[ticker] = {}
        
        # Store volume data by date
        for date, row in historical_data.iterrows():
            date_str = date.strftime('%Y-%m-%d')
            volume = int(row['Volume']) if row['Volume'] > 0 else 0
            self.session_volume_cache[ticker][date_str] = volume
        
        date_count = len(self.session_volume_cache[ticker])
        logger.info(f"📦 Added {ticker} to session cache: {date_count} volume records")
    
    def _query_session_cache(self, ticker: str, target_date: str) -> Optional[int]:
        """
        Query volume from session cache
        
        Args:
            ticker: Stock ticker symbol
            target_date: Date in 'YYYY-MM-DD' format
            
        Returns:
            Volume as integer, or None if not found
        """
        if ticker in self.session_volume_cache:
            volume = self.session_volume_cache[ticker].get(target_date)
            if volume is not None and volume > 0:
                logger.info(f"📦 Found {ticker} volume for {target_date} in session cache: {volume:,}")
                return volume
        
        return None
    
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
    
    def _save_volume_data_to_db(self, ticker: str, historical_data: pd.DataFrame, save_to_db: bool = True) -> bool:
        """
        Save fetched volume data to database (follows same pattern as price calculator)
        
        Args:
            ticker: Stock ticker symbol
            historical_data: DataFrame with historical OHLCV data
            save_to_db: Whether to actually save to database (default: True)
            
        Returns:
            True if saved successfully, False otherwise
        """
        # Early return if save_to_db is False
        if not save_to_db:
            logger.info(f"🚫 Database save disabled for {ticker} - skipping save")
            return False
        if not self.db_available:
            logger.info(f"🚫 Database not available - skipping save for {ticker}")
            return False
        
        conn = self._get_database_connection()
        if not conn:
            logger.error(f"❌ Failed to get database connection for {ticker}")
            return False
        
        try:
            # DIAGNOSTIC: Log what data we received from API
            logger.info(f"🔍 DIAGNOSTIC: Processing {ticker} volume data from API:")
            logger.info(f"   📊 Original data shape: {historical_data.shape}")
            if not historical_data.empty:
                date_range = f"{historical_data.index[0].date()} to {historical_data.index[-1].date()}"
                logger.info(f"   📅 Date range: {date_range}")
                logger.info(f"   📋 Dates included: {[d.strftime('%Y-%m-%d') for d in historical_data.index]}")
            
            # Prepare data for database insertion
            df = historical_data.copy()
            df.reset_index(inplace=True)
            df['Ticker'] = ticker
            
            # Handle yfinance API changes - ensure Adj Close exists
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
                    
                    logger.info(f"✅ SUCCESS: Saved {len(new_df)} new volume records for {ticker} to database")
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
            logger.error(f"Failed to save volume data for {ticker}: {e}")
            logger.info(f"DataFrame columns: {list(historical_data.columns)}")
            logger.info(f"DataFrame shape: {historical_data.shape}")
            logger.info(f"DataFrame head: {historical_data.head()}")
            return False
        finally:
            conn.close()
    
    def _query_volume_from_db(self, ticker: str, target_date: str) -> Optional[int]:
        """
        Query volume from database for specific ticker and date
        
        Args:
            ticker: Stock ticker symbol
            target_date: Date in 'YYYY-MM-DD' format
            
        Returns:
            Volume as integer, or None if not found
        """
        conn = self._get_database_connection()
        if not conn:
            return None
        
        try:
            query = f"""
            SELECT Volume FROM {self.table_name}
            WHERE Ticker = ? AND Date = ?
            """
            
            cursor = conn.cursor()
            cursor.execute(query, (ticker, target_date))
            result = cursor.fetchone()
            
            if result:
                volume = int(result[0]) if result[0] is not None else None
                if volume and volume > 0:
                    logger.info(f"✅ Found {ticker} volume for {target_date} in database: {volume:,}")
                    return volume
                else:
                    logger.warning(f"❌ Zero/null volume for {ticker} on {target_date}")
                    return None
            else:
                logger.info(f"❌ No database entry for {ticker} on {target_date}")
                return None
                
        except Exception as e:
            logger.error(f"Database volume query error for {ticker} on {target_date}: {e}")
            return None
        finally:
            conn.close()
    
    def _fetch_volume_from_yfinance(self, ticker: str, start_date: datetime, end_date: datetime) -> Optional[pd.DataFrame]:
        """
        Fetch volume data from yfinance for specified date range
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date for data fetch
            end_date: End date for data fetch
            
        Returns:
            DataFrame with historical OHLCV data, or None if fetch fails
        """
        try:
            logger.info(f"📡 Fetching volume data for {ticker} from yfinance ({start_date.date()} to {end_date.date()})")
            
            stock = yf.Ticker(ticker)
            hist_data = stock.history(start=start_date, end=end_date)
            
            if hist_data.empty:
                logger.warning(f"⚠️ No historical data returned from yfinance for {ticker}")
                return None
            
            # Log what we received
            date_range = f"{hist_data.index[0].date()} to {hist_data.index[-1].date()}"
            logger.info(f"✅ Retrieved {len(hist_data)} records for {ticker}: {date_range}")
            
            # Verify Volume column exists and has valid data
            if 'Volume' not in hist_data.columns:
                logger.error(f"❌ No Volume column in yfinance data for {ticker}")
                return None
            
            # Check for valid volume data
            valid_volume_count = (hist_data['Volume'] > 0).sum()
            total_records = len(hist_data)
            logger.info(f"📊 Volume data quality: {valid_volume_count}/{total_records} records with valid volume")
            
            if valid_volume_count == 0:
                logger.warning(f"⚠️ No valid volume data (all zero/null) for {ticker}")
                return None
            
            return hist_data
            
        except Exception as e:
            logger.error(f"❌ Error fetching volume data for {ticker} from yfinance: {e}")
            return None
    
    def _query_volume_benchmarks_from_db(self, ticker: str, trading_days: List[datetime], save_to_db: bool = True) -> Optional[float]:
        """
        Calculate volume benchmark average with auto-fetch fallback and session cache support
        
        Args:
            ticker: Stock ticker symbol
            trading_days: List of trading days to include in average
            save_to_db: Whether to save fetched data to database
            
        Returns:
            Average volume as float, or None if insufficient data after auto-fetch
        """
        # First try database
        db_result = self._query_volume_benchmarks_from_database(ticker, trading_days)
        
        if db_result is not None:
            return db_result
        
        # If database fails, try session cache
        session_result = self._query_volume_benchmarks_from_session_cache(ticker, trading_days)
        
        if session_result is not None:
            logger.info(f"📦 Using session cache for {ticker} benchmark calculation")
            return session_result
        
        # If both fail, attempt auto-fetch
        return self._auto_fetch_for_benchmark(ticker, trading_days, save_to_db)
    
    def _query_volume_benchmarks_from_database(self, ticker: str, trading_days: List[datetime]) -> Optional[float]:
        """
        Calculate volume benchmark average from database only
        """
        conn = self._get_database_connection()
        if not conn:
            return None
        
        try:
            # Convert trading days to date strings
            date_strings = [day.strftime('%Y-%m-%d') for day in trading_days]
            
            # Create placeholders for IN clause
            placeholders = ','.join('?' for _ in date_strings)
            
            query = f"""
            SELECT Date, Volume FROM {self.table_name}
            WHERE Ticker = ? AND Date IN ({placeholders}) AND Volume > 0
            ORDER BY Date
            """
            
            cursor = conn.cursor()
            cursor.execute(query, [ticker] + date_strings)
            results = cursor.fetchall()
            
            if results and len(results) == len(trading_days):
                volumes = [int(row[1]) for row in results]
                found_dates = [row[0] for row in results]
                
                logger.info(f"📊 Found {len(results)}/{len(trading_days)} volume records for {ticker}")
                logger.info(f"   📅 Available dates: {found_dates}")
                
                avg_volume = sum(volumes) / len(volumes)
                logger.info(f"✅ Calculated volume benchmark for {ticker}: {avg_volume:,.0f} (from {len(volumes)} days)")
                return float(avg_volume)
            else:
                missing_count = len(trading_days) - len(results) if results else len(trading_days)
                logger.info(f"📊 Insufficient database data for {ticker}: missing {missing_count} days")
                return None
                
        except Exception as e:
            logger.error(f"Database volume benchmark query error for {ticker}: {e}")
            return None
        finally:
            conn.close()
    
    def _query_volume_benchmarks_from_session_cache(self, ticker: str, trading_days: List[datetime]) -> Optional[float]:
        """
        Calculate volume benchmark average from session cache
        """
        if ticker not in self.session_volume_cache:
            return None
        
        date_strings = [day.strftime('%Y-%m-%d') for day in trading_days]
        volumes = []
        found_dates = []
        
        for date_str in date_strings:
            volume = self.session_volume_cache[ticker].get(date_str)
            if volume is not None and volume > 0:
                volumes.append(volume)
                found_dates.append(date_str)
        
        if len(volumes) == len(trading_days):
            avg_volume = sum(volumes) / len(volumes)
            logger.info(f"📦 Calculated benchmark from session cache for {ticker}: {avg_volume:,.0f} (from {len(volumes)} days)")
            return float(avg_volume)
        else:
            missing_count = len(trading_days) - len(volumes)
            logger.info(f"📦 Insufficient session cache data for {ticker}: missing {missing_count} days")
            return None
    
    def _auto_fetch_for_benchmark(self, ticker: str, trading_days: List[datetime], save_to_db: bool) -> Optional[float]:
        """
        Auto-fetch missing data for benchmark calculation
        """
        logger.info(f"📡 Auto-fetching missing volume data for {ticker} benchmark calculation")
        
        # Determine date range for fetching (with buffer)
        earliest_needed = min(trading_days)
        latest_needed = max(trading_days)
        start_date = earliest_needed - timedelta(days=15)  # Buffer for weekends/holidays
        end_date = latest_needed + timedelta(days=5)       # Small buffer forward
        
        # Fetch historical data
        hist_data = self._fetch_volume_from_yfinance(ticker, start_date, end_date)
        
        if hist_data is not None and not hist_data.empty:
            # Save data based on save_to_db setting
            if save_to_db and self.db_available:
                self._save_volume_data_to_db(ticker, hist_data, save_to_db=save_to_db)
                logger.info(f"🔄 Retrying benchmark calculation after auto-fetch for {ticker}")
                return self._query_volume_benchmarks_from_database(ticker, trading_days)
            elif not save_to_db:
                # Store in session cache
                self._add_to_session_cache(ticker, hist_data)
                logger.info(f"🔄 Retrying benchmark calculation using session cache for {ticker}")
                return self._query_volume_benchmarks_from_session_cache(ticker, trading_days)
            else:
                logger.warning(f"⚠️ Database not available and save_to_db=True for {ticker}")
                return None
        else:
            logger.warning(f"⚠️ Auto-fetch failed for {ticker} - unable to get missing benchmark data")
            return None
    
    def get_current_volume(self, ticker: str, save_to_db: bool = True) -> Optional[int]:
        """
        Get current (last completed trading day) volume with auto-fetch fallback
        
        Implementation with auto-fetch:
        1. Get last completed trading day date
        2. Check database for exact ticker + date
        3. If found: return cached volume (no API call)
        4. If missing: fetch from yfinance with auto-save
        5. Return volume from fetched data
        
        Args:
            ticker: Stock ticker symbol
            save_to_db: Whether to save fetched data to database
            
        Returns:
            Last completed trading day volume as integer, or None if not available
        """
        # Get last completed trading day (not today if incomplete)
        current_trading_day = get_last_completed_trading_day()
        current_date_str = current_trading_day.strftime('%Y-%m-%d')
        
        logger.info(f"🔍 Getting current volume for {ticker} (last completed trading day: {current_date_str})")
        
        # Step 1: Check database for exact date
        volume = self._query_volume_from_db(ticker, current_date_str)
        
        if volume is not None:
            logger.info(f"📊 Using cached current volume for {ticker}: {volume:,}")
            return volume
        
        # Step 1.5: Check session cache if not in database
        session_volume = self._query_session_cache(ticker, current_date_str)
        if session_volume is not None:
            logger.info(f"📦 Using session cached current volume for {ticker}: {session_volume:,}")
            return session_volume
        
        # Step 2: Not found in database - auto-fetch from yfinance
        logger.info(f"📡 Auto-fetching current volume for {ticker} from yfinance (date {current_date_str} not in database)")
        
        try:
            # Get data with buffer for weekends/holidays
            start_date = current_trading_day - timedelta(days=10)
            end_date = current_trading_day + timedelta(days=3)
            
            hist_data = self._fetch_volume_from_yfinance(ticker, start_date, end_date)
            
            if hist_data is None or hist_data.empty:
                logger.warning(f"⚠️ No volume data returned from yfinance for {ticker}")
                return None
            
            # Step 3: Auto-save fetched data to database OR session cache
            if save_to_db and self.db_available:
                self._save_volume_data_to_db(ticker, hist_data, save_to_db=save_to_db)
            elif not save_to_db:
                # Store in session cache for temporary use
                self._add_to_session_cache(ticker, hist_data)
                logger.info(f"📦 Stored {ticker} volume data in session cache (save_to_db=False)")
            else:
                logger.warning(f"⚠️ Database not available and save_to_db=True for {ticker}")
            
            # Step 4: Extract current volume from fetched data
            # Convert to date objects for comparison
            hist_data.index = pd.to_datetime(hist_data.index).date
            current_date_only = current_trading_day.date()
            
            if current_date_only in hist_data.index:
                current_volume = int(hist_data.loc[current_date_only, 'Volume'])
                if current_volume > 0:
                    logger.info(f"✅ Retrieved current volume for {ticker}: {current_volume:,}")
                    return current_volume
                else:
                    logger.warning(f"⚠️ Zero volume found for {ticker} on {current_date_str}")
                    return None
            else:
                available_dates = list(hist_data.index)
                logger.warning(f"❌ Current date {current_date_str} not found in fetched data for {ticker}")
                logger.info(f"   📅 Available dates: {available_dates}")
                return None
            
        except Exception as e:
            logger.error(f"Error auto-fetching current volume for {ticker}: {e}")
            return None
    
    def get_volume_benchmark(self, ticker: str, benchmark_period: str, save_to_db: bool = True) -> Optional[float]:
        """
        Calculate volume benchmark average for specified period using strict date validation
        
        Args:
            ticker: Stock ticker symbol
            benchmark_period: Period key ('10d', '1w', '1m', '60d')
            
        Returns:
            Average volume for benchmark period as float, or None if insufficient data
        """
        if benchmark_period not in self.VOLUME_BENCHMARK_PERIODS:
            logger.error(f"❌ Invalid benchmark period: {benchmark_period}")
            return None
        
        trading_days_needed = self.VOLUME_BENCHMARK_PERIODS[benchmark_period]['trading_days']
        period_label = self.VOLUME_BENCHMARK_PERIODS[benchmark_period]['label']
        
        logger.info(f"🔍 Calculating {period_label} volume benchmark for {ticker} ({trading_days_needed} trading days)")
        
        # Get the required trading days (EXCLUDING current day from benchmark)
        current_trading_day = get_last_completed_trading_day()
        # Get N+1 trading days, then exclude the most recent (current) day
        trading_days_plus_current = get_last_n_trading_days(current_trading_day, trading_days_needed + 1)
        trading_days = trading_days_plus_current[:-1]  # Remove most recent day (exclude current from benchmark)
        
        if len(trading_days) < trading_days_needed:
            logger.warning(f"❌ Insufficient trading days available: {len(trading_days)}/{trading_days_needed}")
            return None
        
        logger.info(f"📅 Benchmark period: {trading_days[0].strftime('%Y-%m-%d')} to {trading_days[-1].strftime('%Y-%m-%d')}")
        
        # Calculate benchmark from database with auto-fetch fallback
        benchmark_avg = self._query_volume_benchmarks_from_db(ticker, trading_days, save_to_db=save_to_db)
        
        if benchmark_avg is not None:
            logger.info(f"✅ {period_label} benchmark for {ticker}: {benchmark_avg:,.0f}")
            return benchmark_avg
        else:
            logger.warning(f"⚠️ Unable to calculate {period_label} benchmark for {ticker}")
            return None
    
    def calculate_volume_performance(self, ticker: str, benchmark_period: str = '10d', save_to_db: bool = True) -> Dict:
        """
        Calculate complete volume performance data for a single ticker
        
        Args:
            ticker: Stock ticker symbol
            benchmark_period: Benchmark period for comparison ('10d', '1w', '1m', '60d')
            
        Returns:
            Dictionary with volume performance data
        """
        logger.info(f"🎯 Calculating volume performance for {ticker} ({benchmark_period} benchmark)")
        
        # Get current volume and benchmark average with auto-fetch support
        current_volume = self.get_current_volume(ticker, save_to_db=save_to_db)
        benchmark_avg = self.get_volume_benchmark(ticker, benchmark_period, save_to_db=save_to_db)
        
        if current_volume is None or benchmark_avg is None or benchmark_avg == 0:
            return {
                'ticker': ticker,
                'current_volume': current_volume,
                'benchmark_average': benchmark_avg,
                'volume_change': 0.0,
                'benchmark_period': benchmark_period,
                'benchmark_label': self.VOLUME_BENCHMARK_PERIODS.get(benchmark_period, {}).get('label', benchmark_period),
                'error': True,
                'data_source': 'error'
            }
        
        # Calculate percentage change: (Current Volume / Benchmark Average) - 1
        volume_change = ((current_volume / benchmark_avg) - 1) * 100
        
        result = {
            'ticker': ticker,
            'current_volume': current_volume,
            'benchmark_average': benchmark_avg,
            'volume_change': volume_change,
            'benchmark_period': benchmark_period,
            'benchmark_label': self.VOLUME_BENCHMARK_PERIODS[benchmark_period]['label'],
            'error': False,
            'data_source': 'database'
        }
        
        logger.info(f"✅ {ticker}: {current_volume:,} vs {benchmark_avg:,.0f} avg = {volume_change:+.2f}%")
        return result
    
    def calculate_volume_performance_for_group(self, tickers: List[str], benchmark_period: str = '10d', save_to_db: bool = True) -> List[Dict]:
        """
        Calculate volume performance data for a group of tickers
        
        Args:
            tickers: List of ticker symbols
            benchmark_period: Benchmark period for comparison
            
        Returns:
            List of dictionaries with volume performance data for each ticker
        """
        logger.info(f"🎯 Calculating volume performance for {len(tickers)} tickers ({benchmark_period} benchmark)")
        results = []
        
        for i, ticker in enumerate(tickers, 1):
            logger.info(f"📊 Processing {ticker} ({i}/{len(tickers)})...")
            volume_data = self.calculate_volume_performance(ticker, benchmark_period, save_to_db=save_to_db)
            results.append(volume_data)
        
        # Log summary
        valid_count = len([r for r in results if not r.get('error', True)])
        error_count = len([r for r in results if r.get('error', False)])
        
        logger.info(f"📊 Volume performance calculation complete:")
        logger.info(f"   - Valid calculations: {valid_count} tickers")
        logger.info(f"   - Errors: {error_count} tickers")
        
        return results
    
    def get_volume_performance_summary(self, volume_data: List[Dict]) -> Dict:
        """
        Get summary statistics for a group of volume performance data
        
        Args:
            volume_data: List of volume performance dictionaries
            
        Returns:
            Summary statistics dictionary
        """
        # Filter out error cases
        valid_data = [v for v in volume_data if not v.get('error', False)]
        
        if not valid_data:
            return {
                'total_count': len(volume_data),
                'valid_count': 0,
                'error_count': len(volume_data),
                'avg_volume_change': 0.0,
                'best_performer': None,
                'worst_performer': None
            }
        
        volume_changes = [v['volume_change'] for v in valid_data]
        
        best_performer = max(valid_data, key=lambda x: x['volume_change'])
        worst_performer = min(valid_data, key=lambda x: x['volume_change'])
        
        return {
            'total_count': len(volume_data),
            'valid_count': len(valid_data),
            'error_count': len(volume_data) - len(valid_data),
            'avg_volume_change': np.mean(volume_changes),
            'median_volume_change': np.median(volume_changes),
            'std_volume_change': np.std(volume_changes),
            'best_performer': best_performer,
            'worst_performer': worst_performer,
            'above_average_count': len([v for v in volume_changes if v > 0]),
            'below_average_count': len([v for v in volume_changes if v < 0])
        }


# Factory function for convenience
def get_volume_calculator() -> DatabaseIntegratedVolumeCalculator:
    """Factory function to get a database-integrated volume calculator instance"""
    return DatabaseIntegratedVolumeCalculator()


def calculate_simple_volume_performance(ticker: str, benchmark_period: str = '10d', save_to_db: bool = True) -> Dict:
    """
    Quick function to calculate volume performance for a single ticker
    
    Args:
        ticker: Stock ticker symbol
        benchmark_period: Benchmark period ('10d', '1w', '1m', '60d')
        save_to_db: Whether to save fetched data to database
        
    Returns:
        Volume performance data dictionary
    """
    calculator = DatabaseIntegratedVolumeCalculator()
    return calculator.calculate_volume_performance(ticker, benchmark_period, save_to_db=save_to_db)


def calculate_group_volume_performance(tickers: List[str], benchmark_period: str = '10d', save_to_db: bool = True) -> List[Dict]:
    """
    Quick function to calculate volume performance for a group of tickers
    
    Args:
        tickers: List of ticker symbols
        benchmark_period: Benchmark period ('10d', '1w', '1m', '60d')
        save_to_db: Whether to save fetched data to database
        
    Returns:
        List of volume performance data dictionaries
    """
    calculator = DatabaseIntegratedVolumeCalculator()
    return calculator.calculate_volume_performance_for_group(tickers, benchmark_period, save_to_db=save_to_db)
