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
    
    def _query_volume_benchmarks_from_db(self, ticker: str, trading_days: List[datetime]) -> Optional[float]:
        """
        Calculate volume benchmark average from database for specific trading days
        
        Args:
            ticker: Stock ticker symbol
            trading_days: List of trading days to include in average
            
        Returns:
            Average volume as float, or None if insufficient data
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
            
            if results:
                volumes = [int(row[1]) for row in results]
                found_dates = [row[0] for row in results]
                
                logger.info(f"📊 Found {len(results)}/{len(trading_days)} volume records for {ticker}")
                logger.info(f"   📅 Available dates: {found_dates}")
                
                # Strict validation: require ALL trading days to have volume data
                if len(results) == len(trading_days):
                    avg_volume = sum(volumes) / len(volumes)
                    logger.info(f"✅ Calculated volume benchmark for {ticker}: {avg_volume:,.0f} (from {len(volumes)} days)")
                    return float(avg_volume)
                else:
                    missing_count = len(trading_days) - len(results)
                    logger.warning(f"❌ Insufficient volume data for {ticker}: missing {missing_count} days")
                    return None
            else:
                logger.warning(f"❌ No volume data found for {ticker} in benchmark period")
                return None
                
        except Exception as e:
            logger.error(f"Database volume benchmark query error for {ticker}: {e}")
            return None
        finally:
            conn.close()
    
    def get_current_volume(self, ticker: str) -> Optional[int]:
        """
        Get current (last completed trading day) volume using strict date validation
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Last completed trading day volume as integer, or None if not available
        """
        # Get last completed trading day (not today if incomplete)
        current_trading_day = get_last_completed_trading_day()
        current_date_str = current_trading_day.strftime('%Y-%m-%d')
        
        logger.info(f"🔍 Getting current volume for {ticker} (last completed trading day: {current_date_str})")
        
        # Query database for exact date
        volume = self._query_volume_from_db(ticker, current_date_str)
        
        if volume is not None:
            logger.info(f"📊 Current volume for {ticker}: {volume:,}")
            return volume
        else:
            logger.warning(f"⚠️ No current volume data available for {ticker}")
            return None
    
    def get_volume_benchmark(self, ticker: str, benchmark_period: str) -> Optional[float]:
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
        
        # Get the required trading days
        current_trading_day = get_last_completed_trading_day()
        trading_days = get_last_n_trading_days(current_trading_day, trading_days_needed)
        
        if len(trading_days) < trading_days_needed:
            logger.warning(f"❌ Insufficient trading days available: {len(trading_days)}/{trading_days_needed}")
            return None
        
        logger.info(f"📅 Benchmark period: {trading_days[0].strftime('%Y-%m-%d')} to {trading_days[-1].strftime('%Y-%m-%d')}")
        
        # Calculate benchmark from database
        benchmark_avg = self._query_volume_benchmarks_from_db(ticker, trading_days)
        
        if benchmark_avg is not None:
            logger.info(f"✅ {period_label} benchmark for {ticker}: {benchmark_avg:,.0f}")
            return benchmark_avg
        else:
            logger.warning(f"⚠️ Unable to calculate {period_label} benchmark for {ticker}")
            return None
    
    def calculate_volume_performance(self, ticker: str, benchmark_period: str = '10d') -> Dict:
        """
        Calculate complete volume performance data for a single ticker
        
        Args:
            ticker: Stock ticker symbol
            benchmark_period: Benchmark period for comparison ('10d', '1w', '1m', '60d')
            
        Returns:
            Dictionary with volume performance data
        """
        logger.info(f"🎯 Calculating volume performance for {ticker} ({benchmark_period} benchmark)")
        
        # Get current volume and benchmark average
        current_volume = self.get_current_volume(ticker)
        benchmark_avg = self.get_volume_benchmark(ticker, benchmark_period)
        
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
    
    def calculate_volume_performance_for_group(self, tickers: List[str], benchmark_period: str = '10d') -> List[Dict]:
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
            volume_data = self.calculate_volume_performance(ticker, benchmark_period)
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


def calculate_simple_volume_performance(ticker: str, benchmark_period: str = '10d') -> Dict:
    """
    Quick function to calculate volume performance for a single ticker
    
    Args:
        ticker: Stock ticker symbol
        benchmark_period: Benchmark period ('10d', '1w', '1m', '60d')
        
    Returns:
        Volume performance data dictionary
    """
    calculator = DatabaseIntegratedVolumeCalculator()
    return calculator.calculate_volume_performance(ticker, benchmark_period)


def calculate_group_volume_performance(tickers: List[str], benchmark_period: str = '10d') -> List[Dict]:
    """
    Quick function to calculate volume performance for a group of tickers
    
    Args:
        tickers: List of ticker symbols
        benchmark_period: Benchmark period ('10d', '1w', '1m', '60d')
        
    Returns:
        List of volume performance data dictionaries
    """
    calculator = DatabaseIntegratedVolumeCalculator()
    return calculator.calculate_volume_performance_for_group(tickers, benchmark_period)
