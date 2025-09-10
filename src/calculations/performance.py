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
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import logging
import calendar

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_us_market_holidays(year: int) -> List[datetime]:
    """
    Get all US stock market holidays for a given year
    
    Args:
        year: Year to get holidays for
        
    Returns:
        List of datetime objects representing market holidays
    """
    holidays = []
    
    # New Year's Day - January 1st (or observed Monday if weekend)
    new_years = date(year, 1, 1)
    if new_years.weekday() == 5:  # Saturday
        holidays.append(datetime.combine(date(year, 1, 3), datetime.min.time()))  # Monday
    elif new_years.weekday() == 6:  # Sunday  
        holidays.append(datetime.combine(date(year, 1, 2), datetime.min.time()))  # Monday
    else:
        holidays.append(datetime.combine(new_years, datetime.min.time()))
    
    # Martin Luther King Jr. Day - Third Monday in January (FIXED)
    jan_1 = date(year, 1, 1)
    # Find first Monday of January
    days_to_monday = (7 - jan_1.weekday()) % 7
    if days_to_monday == 0 and jan_1.weekday() == 0:  # Jan 1 is Monday
        first_monday = jan_1
    else:
        first_monday = jan_1 + timedelta(days=days_to_monday)
    mlk_day = first_monday + timedelta(days=14)  # Third Monday
    holidays.append(datetime.combine(mlk_day, datetime.min.time()))
    
    # Presidents Day - Third Monday in February (FIXED)
    feb_1 = date(year, 2, 1)
    # Find first Monday of February
    days_to_monday = (7 - feb_1.weekday()) % 7
    if days_to_monday == 0 and feb_1.weekday() == 0:  # Feb 1 is Monday
        first_monday_feb = feb_1
    else:
        first_monday_feb = feb_1 + timedelta(days=days_to_monday)
    presidents_day = first_monday_feb + timedelta(days=14)  # Third Monday
    holidays.append(datetime.combine(presidents_day, datetime.min.time()))
    
    # Good Friday - Friday before Easter (complex calculation)
    # Using a simplified approximation for most years
    # This could be enhanced with proper Easter calculation
    easter_approximations = {
        2023: date(2023, 4, 7),
        2024: date(2024, 3, 29), 
        2025: date(2025, 4, 18),
        2026: date(2026, 4, 3),
        2027: date(2027, 3, 26),
        2028: date(2028, 4, 14),
        2029: date(2029, 3, 30),
        2030: date(2030, 4, 19)
    }
    if year in easter_approximations:
        holidays.append(datetime.combine(easter_approximations[year], datetime.min.time()))
    
    # Memorial Day - Last Monday in May
    may_31 = date(year, 5, 31)
    memorial_day = may_31
    while memorial_day.weekday() != 0:  # Find last Monday
        memorial_day -= timedelta(days=1)
    holidays.append(datetime.combine(memorial_day, datetime.min.time()))
    
    # Juneteenth - June 19th (or observed if weekend) - federal holiday since 2021
    if year >= 2021:
        juneteenth = date(year, 6, 19)
        if juneteenth.weekday() == 5:  # Saturday
            holidays.append(datetime.combine(date(year, 6, 18), datetime.min.time()))  # Friday
        elif juneteenth.weekday() == 6:  # Sunday
            holidays.append(datetime.combine(date(year, 6, 20), datetime.min.time()))  # Monday
        else:
            holidays.append(datetime.combine(juneteenth, datetime.min.time()))
    
    # Independence Day - July 4th (or observed if weekend)
    july_4 = date(year, 7, 4)
    if july_4.weekday() == 5:  # Saturday
        holidays.append(datetime.combine(date(year, 7, 3), datetime.min.time()))  # Friday
    elif july_4.weekday() == 6:  # Sunday
        holidays.append(datetime.combine(date(year, 7, 5), datetime.min.time()))  # Monday
    else:
        holidays.append(datetime.combine(july_4, datetime.min.time()))
    
    # Labor Day - First Monday in September (FIXED)
    sep_1 = date(year, 9, 1)
    # Find first Monday of September
    days_to_monday = (7 - sep_1.weekday()) % 7
    if days_to_monday == 0 and sep_1.weekday() == 0:  # Sept 1 is Monday
        first_monday_sep = sep_1  # Sept 1 IS the first Monday
    else:
        first_monday_sep = sep_1 + timedelta(days=days_to_monday)
    holidays.append(datetime.combine(first_monday_sep, datetime.min.time()))
    
    # Thanksgiving Day - Fourth Thursday in November
    nov_1 = date(year, 11, 1)
    first_thursday = nov_1 + timedelta(days=(3 - nov_1.weekday()) % 7)
    if first_thursday.day <= 1:
        first_thursday += timedelta(days=7)
    thanksgiving = first_thursday + timedelta(days=21)  # Fourth Thursday
    holidays.append(datetime.combine(thanksgiving, datetime.min.time()))
    
    # Christmas Day - December 25th (or observed if weekend)
    christmas = date(year, 12, 25)
    if christmas.weekday() == 5:  # Saturday
        holidays.append(datetime.combine(date(year, 12, 24), datetime.min.time()))  # Friday
    elif christmas.weekday() == 6:  # Sunday
        holidays.append(datetime.combine(date(year, 12, 26), datetime.min.time()))  # Monday
    else:
        holidays.append(datetime.combine(christmas, datetime.min.time()))
    
    return sorted(holidays)


def get_baseline_date_for_display(period: str) -> str:
    """
    Get the baseline date for UI display purposes
    
    Args:
        period: Time period key ('1d', '1w', '1m', etc.)
        
    Returns:
        Formatted date string for display (e.g., "2025-08-22")
    """
    target_date = get_trading_day_target(period, datetime.now())
    return target_date.strftime('%Y-%m-%d')


def is_us_trading_day(check_date: datetime) -> bool:
    """
    Check if a given date is a US stock market trading day
    
    Args:
        check_date: Date to check
        
    Returns:
        True if it's a trading day, False if weekend or holiday
    """
    # Check if weekend
    if check_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False
    
    # Check if holiday
    year_holidays = get_us_market_holidays(check_date.year)
    check_date_only = datetime.combine(check_date.date(), datetime.min.time())
    
    return check_date_only not in year_holidays


def get_last_completed_trading_day(from_date: datetime = None) -> datetime:
    """
    Get the last COMPLETED trading day (for snapshot when today is holiday/weekend)
    
    This is different from "most recent trading day" - it ensures we get a completed
    trading session, not the current day even if it's a trading day.
    
    Args:
        from_date: Date to calculate from (defaults to now)
        
    Returns:
        Last completed trading day
    """
    if from_date is None:
        from_date = datetime.now()
    
    current_date = from_date
    
    # If today is a trading day, we want YESTERDAY's completed trading day
    # If today is holiday/weekend, we want the last trading day before today
    if is_us_trading_day(current_date):
        current_date -= timedelta(days=1)  # Go back one day first
    
    # Now find the most recent trading day
    while not is_us_trading_day(current_date):
        current_date -= timedelta(days=1)
    
    logger.info(f"🗓️ Last completed trading day: {current_date.strftime('%Y-%m-%d %A')}")
    return current_date


def get_last_n_trading_days(from_date: datetime, n: int) -> List[datetime]:
    """
    Get the last N trading days before (and including) a given date
    
    Args:
        from_date: Starting date to count backwards from
        n: Number of trading days to return
        
    Returns:
        List of datetime objects representing the last N trading days
    """
    trading_days = []
    current_date = from_date
    
    # Count backwards until we have N trading days
    while len(trading_days) < n:
        if is_us_trading_day(current_date):
            trading_days.insert(0, current_date)  # Insert at beginning to maintain order
        current_date -= timedelta(days=1)
    
    return trading_days


def get_trading_day_target(period: str, from_date: datetime = None) -> datetime:
    """
    Get the target trading day for a given period using proper trading day math
    
    Args:
        period: Time period key ('1d', '1w', '1m', etc.)
        from_date: Date to calculate from (defaults to now)
        
    Returns:
        Target datetime for the historical comparison
    """
    if from_date is None:
        from_date = datetime.now()
    
    # Handle YTD specially - use last trading day of previous year
    if period == 'ytd':
        # Get December 31st of previous year
        dec_31_prev_year = datetime(from_date.year - 1, 12, 31)
        # Move to Friday if Dec 31st falls on weekend
        while dec_31_prev_year.weekday() >= 5:  # Saturday=5, Sunday=6
            dec_31_prev_year -= timedelta(days=1)
        logger.info(f"YTD baseline: {dec_31_prev_year.strftime('%Y-%m-%d %A')}")
        return dec_31_prev_year
    
    # Handle 1Y specially - use exact calendar year then find last trading day
    if period == '1y':
        try:
            # Go back exactly 1 year (same month/day)
            calendar_year_back = from_date.replace(year=from_date.year - 1)
            
            # Find the last trading day on or before the calendar date
            target_date = calendar_year_back
            while not is_us_trading_day(target_date):
                target_date -= timedelta(days=1)
            
            logger.info(f"Using last trading day for 1Y: {target_date.strftime('%Y-%m-%d %A')} (calendar: {calendar_year_back.strftime('%Y-%m-%d')})")
            return target_date
        except ValueError:
            # Handle leap year edge case (Feb 29)
            calendar_year_back = from_date.replace(year=from_date.year - 1, month=2, day=28)
            
            # Find the last trading day on or before the leap year adjusted date
            target_date = calendar_year_back
            while not is_us_trading_day(target_date):
                target_date -= timedelta(days=1)
                
            logger.info(f"Leap year adjustment + trading day for 1Y: {target_date.strftime('%Y-%m-%d %A')}")
            return target_date
    
    # Handle 1D specially - get last COMPLETED trading day (not current day)
    if period == '1d':
        # Get last 2 trading days, use the older one for 1D historical comparison
        last_two_days = get_last_n_trading_days(from_date, 2)
        if len(last_two_days) >= 2:
            historical_day = last_two_days[0]  # Older trading day (Thursday)
            current_day = last_two_days[1]     # Most recent trading day (Friday)
            logger.info(f"Using 1D historical: {historical_day.strftime('%Y-%m-%d %A')} (vs current: {current_day.strftime('%Y-%m-%d %A')})")
            return historical_day
        else:
            # Fallback to existing logic if insufficient data
            last_completed = get_last_completed_trading_day(from_date)
            logger.info(f"Fallback to last completed trading day for 1D: {last_completed.strftime('%Y-%m-%d %A')}")
            return last_completed
    
    # Map other periods to approximate trading days
    trading_days_map = {
        '1w': 5,      # ~1 week = 5 trading days  
        '1m': 22,     # ~1 month = 22 trading days
        '3m': 65,     # ~3 months = 65 trading days
        '6m': 125     # ~6 months = 130 trading days
    }
    
    trading_days_back = trading_days_map.get(period, 1)
    
    # Get the Nth trading day back, with holiday base period adjustment
    trading_days = get_last_n_trading_days(from_date, trading_days_back + 1)  # +1 because we want the day before the last N days
    
    if len(trading_days) >= 2:
        target_date = trading_days[0]  # The oldest trading day (target for comparison)
        
        # Verify the target date is actually a trading day (additional safety check)
        if not is_us_trading_day(target_date):
            logger.warning(f"Target date {target_date.strftime('%Y-%m-%d')} is not a trading day, adjusting...")
            # Find the last trading day before the target
            adjusted_target = target_date
            while not is_us_trading_day(adjusted_target):
                adjusted_target -= timedelta(days=1)
            logger.info(f"Adjusted base period from {target_date.strftime('%Y-%m-%d')} to {adjusted_target.strftime('%Y-%m-%d %A')}")
            return adjusted_target
        
        return target_date
    else:
        # Fallback to calendar math with trading day adjustment
        logger.warning(f"Trading day calculation failed for {period}, using calendar math with adjustment")
        days_back = {'1d': 1, '1w': 7, '1m': 30, '3m': 90, '6m': 180}.get(period, 1)
        calendar_target = from_date - timedelta(days=days_back)
        
        # Adjust if calendar target falls on holiday/weekend
        if not is_us_trading_day(calendar_target):
            adjusted_target = calendar_target
            while not is_us_trading_day(adjusted_target):
                adjusted_target -= timedelta(days=1)
            logger.info(f"Calendar fallback adjusted from {calendar_target.strftime('%Y-%m-%d')} to {adjusted_target.strftime('%Y-%m-%d %A')}")
            return adjusted_target
        
        return calendar_target


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
    
    def _validate_exact_target_date(self, hist_data: pd.DataFrame, target_date: datetime, ticker: str) -> Optional[float]:
        """
        Validate that yfinance response contains exact target date and return price
        
        Args:
            hist_data: Historical data from yfinance
            target_date: Required target date
            ticker: Stock ticker for logging
            
        Returns:
            Price for exact target date, or None if exact date not available
        """
        if hist_data.empty:
            return None
            
        # Convert to date objects for comparison
        hist_data.index = pd.to_datetime(hist_data.index).date
        target_date_only = target_date.date()
        
        # Require EXACT date match - no approximations
        if target_date_only in hist_data.index:
            exact_price = float(hist_data.loc[target_date_only, 'Close'])
            logger.info(f"✅ Found EXACT target date {target_date_only} for {ticker}: ${exact_price:.2f}")
            return exact_price
        else:
            available_dates = list(hist_data.index)
            logger.warning(f"❌ EXACT target date {target_date_only} NOT found for {ticker}")
            logger.info(f"   📅 Available dates in response: {available_dates}")
            return None

    def _find_closest_date_in_db(self, ticker: str, target_date: datetime) -> Optional[Tuple[str, float]]:
        """
        DEPRECATED: Find the closest available date in database before or on target date
        
        This function is preserved for backward compatibility but should not be used
        in the main data flow. Use exact date validation instead.
        
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
    
    def _save_historical_data_to_db(self, ticker: str, historical_data: pd.DataFrame, save_to_db: bool = True) -> bool:
        """
        Save fetched historical data to database
        
        Args:
            ticker: Stock ticker symbol
            historical_data: DataFrame with historical OHLCV data
            save_to_db: Whether to actually save to database (default: True for backward compatibility)
            
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
    
    def get_historical_price(self, ticker: str, period: str, save_to_db: bool = True) -> Optional[float]:
        """
        Get historical price using database-first approach with STRICT date validation
        
        Implementation with exact date requirement:
        1. Calculate proper trading day target date
        2. Check database for exact ticker + date
        3. If found: return cached price (no API call)
        4. If missing: fetch from yfinance with auto-save
        5. Require EXACT target date match - no approximations
        6. Return price only if exact date available
        
        Args:
            ticker: Stock ticker symbol
            period: Time period key ('1d', '1w', '1m', etc.)
            save_to_db: Whether to save fetched data to database
            
        Returns:
            Historical price as float, or None if exact date not available
        """
        # Calculate target date using proper trading day logic
        target_date = get_trading_day_target(period, datetime.now())
        target_date_str = target_date.strftime('%Y-%m-%d')
        
        # DIAGNOSTIC: Enhanced logging
        current_time = datetime.now()
        logger.info(f"🔍 STRICT VALIDATION: {ticker} {period} calculation:")
        logger.info(f"   📅 Current time: {current_time.strftime('%Y-%m-%d %A %H:%M')}")
        logger.info(f"   🎯 Target date: {target_date.strftime('%Y-%m-%d %A')}")
        logger.info(f"   🔄 Period: {period}")
        
        # Step 1: Check database for EXACT date
        logger.info(f"🔍 Looking for {ticker} EXACT date {target_date_str} in database")
        db_price = self._query_historical_price_from_db(ticker, target_date_str)
        
        if db_price is not None:
            logger.info(f"📊 Using cached EXACT price for {ticker}: ${db_price:.2f}")
            return db_price
        
        # Step 2: Not found in database - auto-fetch from yfinance
        logger.info(f"📡 Auto-fetching {ticker} from yfinance (exact date {target_date_str} not in database)")
        
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
                self._save_historical_data_to_db(ticker, hist_data, save_to_db=save_to_db)
            
            # Step 4: STRICT VALIDATION - require exact target date
            exact_price = self._validate_exact_target_date(hist_data, target_date, ticker)
            
            if exact_price is not None:
                logger.info(f"✅ Retrieved {ticker} EXACT historical price: ${exact_price:.2f}")
                return exact_price
            else:
                logger.error(f"❌ EXACT target date {target_date_str} unavailable for {ticker} - returning None")
                return None
            
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
    
    def calculate_performance_for_ticker(self, ticker: str, period: str, save_to_db: bool = True) -> Dict:
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
        historical_price = self.get_historical_price(ticker, period, save_to_db=save_to_db)
        
        if current_price is None or historical_price is None:
            return {
                'ticker': ticker,
                'current_price': current_price,
                'historical_price': historical_price,
                'percentage_change': 0.0,
                'absolute_change': 0.0,
                'period': period,
                'period_label': get_enhanced_period_label(period),
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
            'period_label': get_enhanced_period_label(period),
            'error': False,
            'data_source': data_source
        }
        
        logger.info(f"✅ {ticker}: ${current_price:.2f} vs ${historical_price:.2f} = {percentage_change:+.2f}%")
        return result
    
    def calculate_performance_for_group(self, tickers: List[str], period: str, save_to_db: bool = True) -> List[Dict]:
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
            performance_data = self.calculate_performance_for_ticker(ticker, period, save_to_db=save_to_db)
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


def get_enhanced_period_label(period: str) -> str:
    """
    Get enhanced period label with baseline date for specific periods
    
    Args:
        period: Time period key ('1d', '1w', '1m', etc.)
        
    Returns:
        Enhanced label with baseline date for specified periods, standard label for others
    """
    # Enhanced labels with baseline dates for ALL periods
    enhanced_periods = {
        '1d': '1D',
        '1w': '1W',
        '1m': '1M', 
        '3m': '3M',
        '6m': '6M',
        'ytd': 'YTD',
        '1y': '1Y'
    }
    
    if period in enhanced_periods:
        baseline_date = get_baseline_date_for_display(period)
        # Convert to MM/DD/YY format
        baseline_dt = datetime.strptime(baseline_date, '%Y-%m-%d')
        baseline_formatted = baseline_dt.strftime('%m/%d/%y')
        return f"{enhanced_periods[period]} ({baseline_formatted})"
    
    # Fallback for unknown periods
    return period.upper()



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
