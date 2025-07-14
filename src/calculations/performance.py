"""
Price Performance Calculations

This module handles all price-related performance calculations for the heatmap dashboard,
including percentage changes across various time periods.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import yfinance as yf


class PerformanceCalculator:
    """Calculates price performance metrics for stocks and ETFs"""
    
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
    
    def __init__(self):
        self.cache = {}
    
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
    
    def get_historical_price(self, ticker: str, period: str) -> Optional[float]:
        """
        Get historical price for a specific ticker and time period
        
        Args:
            ticker: Stock ticker symbol
            period: Time period key ('1d', '1w', '1m', etc.)
            
        Returns:
            Historical price as float, or None if not available
        """
        try:
            # Calculate the target date
            if period == 'ytd':
                # Year-to-date: get price from January 1st of current year
                target_date = datetime(datetime.now().year, 1, 1)
            else:
                days_back = self.TIME_PERIODS[period]['days']
                target_date = datetime.now() - timedelta(days=days_back)
            
            # Fetch historical data
            stock = yf.Ticker(ticker)
            
            # Get historical data with some buffer to account for weekends/holidays
            start_date = target_date - timedelta(days=10)
            end_date = target_date + timedelta(days=3)
            
            hist_data = stock.history(start=start_date, end=end_date)
            
            if hist_data.empty:
                return None
            
            # Find the closest available date to our target
            hist_data.index = pd.to_datetime(hist_data.index).date
            target_date = target_date.date()
            
            # Get the closest date that's not after our target
            available_dates = [d for d in hist_data.index if d <= target_date]
            if not available_dates:
                return None
                
            closest_date = max(available_dates)
            return float(hist_data.loc[closest_date, 'Close'])
            
        except Exception as e:
            print(f"Error fetching historical price for {ticker} ({period}): {e}")
            return None
    
    def get_current_price(self, ticker: str) -> Optional[float]:
        """
        Get current price for a ticker
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Current price as float, or None if not available
        """
        try:
            stock = yf.Ticker(ticker)
            
            # Try to get current price from info first (faster)
            info = stock.info
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            
            if current_price:
                return float(current_price)
            
            # Fallback to recent history
            hist = stock.history(period='2d')
            if not hist.empty:
                return float(hist['Close'].iloc[-1])
                
            return None
            
        except Exception as e:
            print(f"Error fetching current price for {ticker}: {e}")
            return None
    
    def calculate_performance_for_ticker(self, ticker: str, period: str) -> Dict:
        """
        Calculate complete performance data for a single ticker
        
        Args:
            ticker: Stock ticker symbol
            period: Time period for comparison
            
        Returns:
            Dictionary with performance data
        """
        current_price = self.get_current_price(ticker)
        historical_price = self.get_historical_price(ticker, period)
        
        if current_price is None or historical_price is None:
            return {
                'ticker': ticker,
                'current_price': None,
                'historical_price': None,
                'percentage_change': 0.0,
                'absolute_change': 0.0,
                'period': period,
                'period_label': self.TIME_PERIODS.get(period, {}).get('label', period),
                'error': True
            }
        
        percentage_change = self.calculate_percentage_change(current_price, historical_price)
        absolute_change = current_price - historical_price
        
        return {
            'ticker': ticker,
            'current_price': current_price,
            'historical_price': historical_price,
            'percentage_change': percentage_change,
            'absolute_change': absolute_change,
            'period': period,
            'period_label': self.TIME_PERIODS.get(period, {}).get('label', period),
            'error': False
        }
    
    def calculate_performance_for_group(self, tickers: List[str], period: str) -> List[Dict]:
        """
        Calculate performance data for a group of tickers
        
        Args:
            tickers: List of ticker symbols
            period: Time period for comparison
            
        Returns:
            List of dictionaries with performance data for each ticker
        """
        results = []
        
        for ticker in tickers:
            print(f"Calculating performance for {ticker}...")
            performance_data = self.calculate_performance_for_ticker(ticker, period)
            results.append(performance_data)
        
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
                'worst_performer': None
            }
        
        percentages = [p['percentage_change'] for p in valid_data]
        
        best_performer = max(valid_data, key=lambda x: x['percentage_change'])
        worst_performer = min(valid_data, key=lambda x: x['percentage_change'])
        
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
            'negative_count': len([p for p in percentages if p < 0])
        }


def get_performance_calculator() -> PerformanceCalculator:
    """Factory function to get a performance calculator instance"""
    return PerformanceCalculator()


# Convenience functions for direct use
def calculate_simple_performance(ticker: str, period: str = '1d') -> Dict:
    """
    Quick function to calculate performance for a single ticker
    
    Args:
        ticker: Stock ticker symbol
        period: Time period ('1d', '1w', '1m', etc.)
        
    Returns:
        Performance data dictionary
    """
    calculator = PerformanceCalculator()
    return calculator.calculate_performance_for_ticker(ticker, period)


def calculate_group_performance(tickers: List[str], period: str = '1d') -> List[Dict]:
    """
    Quick function to calculate performance for a group of tickers
    
    Args:
        tickers: List of ticker symbols
        period: Time period ('1d', '1w', '1m', etc.)
        
    Returns:
        List of performance data dictionaries
    """
    calculator = PerformanceCalculator()
    return calculator.calculate_performance_for_group(tickers, period)
