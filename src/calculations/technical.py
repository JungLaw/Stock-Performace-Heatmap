"""
Database-Integrated Technical Analysis Calculator

Technical analysis calculator that uses database cache first, then yfinance fallback.
Follows the same proven pattern as DatabaseIntegratedPerformanceCalculator and
DatabaseIntegratedVolumeCalculator for consistency and reliability.
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

class DatabaseIntegratedTechnicalCalculator:
    """
    Technical analysis calculator that uses database cache first, then yfinance fallback.
    Implements corrected signal logic and follows proven DatabaseIntegrated* patterns.
    """
    
    # Define available technical indicators
    TECHNICAL_INDICATORS = {
        # Momentum Oscillators
        'rsi': {'periods': [14], 'label': 'RSI', 'type': 'oscillator'},
        'stoch': {'periods': [14], 'label': 'Stochastic', 'type': 'oscillator'},
        'stochrsi': {'periods': [14], 'label': 'Stochastic RSI', 'type': 'oscillator'},
        'williams_r': {'periods': [14], 'label': 'Williams %R', 'type': 'oscillator'},
        'cci': {'periods': [14], 'label': 'CCI', 'type': 'oscillator'},
        'ultimate_osc': {'periods': [7, 14, 28], 'label': 'Ultimate Oscillator', 'type': 'oscillator'},
        'roc': {'periods': [12], 'label': 'Rate of Change', 'type': 'momentum'},
        
        # Trend Indicators
        'macd': {'periods': [12, 26, 9], 'label': 'MACD', 'type': 'trend'},
        'adx': {'periods': [14], 'label': 'ADX', 'type': 'trend'},
        'elder_ray': {'periods': [13], 'label': 'Elder Ray Index', 'type': 'trend'},
        
        # Moving Averages
        'sma': {'periods': [5, 9, 10, 20, 21, 50, 100, 200], 'label': 'Simple MA', 'type': 'moving_average'},
        'ema': {'periods': [5, 9, 10, 20, 21, 50, 100, 200], 'label': 'Exponential MA', 'type': 'moving_average'},
        
        # Volatility
        'atr': {'periods': [14], 'label': 'Average True Range', 'type': 'volatility'}
    }
    
    # Signal strength thresholds (corrected logic)
    SIGNAL_THRESHOLDS = {
        'rsi': {
            'strong_buy': 20,      # RSI <= 20
            'buy': 35,             # RSI <= 35 
            'neutral_low': 35,     # RSI > 35
            'neutral_high': 70,    # RSI < 70
            'sell': 70,            # RSI >= 70
            'strong_sell': 80      # RSI >= 80
        },
        'moving_average': {
            'neutral_threshold': 0.025  # ±0.025% neutral zone
        },
        'adx': {
            'weak_trend': 25,      # ADX < 25
            'strong_trend': 50     # ADX >= 50
        }
    }
    
    def __init__(self, db_file: str = "data/stock_data.db"):
        self.db_file = db_file
        self.daily_prices_table = "daily_prices"
        self.technical_table = "technical_indicators_daily"
        self.extremes_table = "price_extremes_periods"
        self.pivot_table = "pivot_points_daily"
        
        # Import and initialize performance calculator for current price fetching
        from .performance import DatabaseIntegratedPerformanceCalculator
        self.performance_calculator = DatabaseIntegratedPerformanceCalculator(db_file)
        
        # Session-level cache for technical data when save_to_db=False
        self.session_technical_cache = {}  # {ticker: {date: indicators_dict}}
        
        # Verify database exists
        db_path = Path(db_file)
        if not db_path.exists():
            logger.warning(f"Database file {db_file} not found. Will rely on yfinance only.")
            self.db_available = False
        else:
            self.db_available = True
            logger.info(f"Technical analysis database found: {db_file}")
    
    def _get_database_connection(self) -> Optional[sqlite3.Connection]:
        """Get database connection if available"""
        if not self.db_available:
            return None
        
        try:
            return sqlite3.connect(self.db_file)
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return None
    
    def _fetch_ohlcv_data_from_db(self, ticker: str, start_date: datetime, end_date: datetime) -> Optional[pd.DataFrame]:
        """
        Fetch OHLCV data from database for technical analysis calculations
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date for data range
            end_date: End date for data range
            
        Returns:
            DataFrame with OHLCV data or None if insufficient data
        """
        conn = self._get_database_connection()
        if not conn:
            return None
        
        try:
            query = f"""
            SELECT Date, Open, High, Low, Close, Volume
            FROM {self.daily_prices_table}
            WHERE Ticker = ? AND Date >= ? AND Date <= ?
            ORDER BY Date ASC
            """
            
            start_str = start_date.strftime('%Y-%m-%d')
            end_str = end_date.strftime('%Y-%m-%d')
            
            df = pd.read_sql_query(query, conn, params=(ticker, start_str, end_str))
            
            if df.empty:
                logger.info(f"❌ No database OHLCV data for {ticker} between {start_str} and {end_str}")
                return None
            
            # Set Date as index and convert to datetime
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            
            logger.info(f"✅ Found {len(df)} OHLCV records for {ticker} in database ({start_str} to {end_str})")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching OHLCV data for {ticker}: {e}")
            return None
        finally:
            conn.close()
    
    def _fetch_ohlcv_data_from_yfinance(self, ticker: str, start_date: datetime, end_date: datetime, save_to_db: bool = True) -> Optional[pd.DataFrame]:
        """
        Fetch OHLCV data from yfinance with auto-save capability
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date for data range
            end_date: End date for data range
            save_to_db: Whether to save fetched data to database
            
        Returns:
            DataFrame with OHLCV data or None if fetch failed
        """
        try:
            stock = yf.Ticker(ticker)
            
            # Add buffer to ensure we get enough data
            buffer_start = start_date - timedelta(days=10)
            buffer_end = end_date + timedelta(days=5)
            
            hist_data = stock.history(start=buffer_start, end=buffer_end)
            
            if hist_data.empty:
                logger.warning(f"⚠️ No historical data returned from yfinance for {ticker}")
                return None
            
            logger.info(f"📡 Fetched {len(hist_data)} records from yfinance for {ticker}")
            
            # Auto-save to database if enabled
            if save_to_db and self.db_available:
                self._save_ohlcv_data_to_db(ticker, hist_data)
            
            # Filter to requested date range
            filtered_data = hist_data[(hist_data.index >= start_date) & (hist_data.index <= end_date)]
            
            logger.info(f"✅ Filtered to {len(filtered_data)} records for {ticker} in requested range")
            return filtered_data
            
        except Exception as e:
            logger.error(f"Error fetching OHLCV data from yfinance for {ticker}: {e}")
            return None
    
    def _save_ohlcv_data_to_db(self, ticker: str, historical_data: pd.DataFrame) -> bool:
        """
        Save fetched OHLCV data to database (reusing logic from performance calculator)
        
        Args:
            ticker: Stock ticker symbol
            historical_data: DataFrame with historical OHLCV data
            
        Returns:
            True if saved successfully, False otherwise
        """
        # Import the save method from performance calculator to avoid code duplication
        from .performance import DatabaseIntegratedPerformanceCalculator
        
        try:
            perf_calc = DatabaseIntegratedPerformanceCalculator(db_file=self.db_file)
            success = perf_calc._save_historical_data_to_db(ticker, historical_data, save_to_db=True)
            
            if success:
                logger.info(f"✅ OHLCV data saved to database for {ticker}")
            else:
                logger.warning(f"⚠️ Failed to save OHLCV data for {ticker}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error saving OHLCV data for {ticker}: {e}")
            return False
    
    def _get_sufficient_ohlcv_data(self, ticker: str, periods_needed: int = 200, save_to_db: bool = True) -> Optional[pd.DataFrame]:
        """
        Get sufficient OHLCV data for technical analysis calculations
        
        Args:
            ticker: Stock ticker symbol
            periods_needed: Number of periods needed for calculations (default 200 for 200-day MA)
            save_to_db: Whether to save fetched data to database
            
        Returns:
            DataFrame with sufficient OHLCV data or None if insufficient
        """
        # Calculate date range needed
        end_date = datetime.now()
        
        # Get approximately periods_needed trading days worth of calendar days
        # Assuming ~252 trading days per year, add buffer for weekends/holidays
        days_buffer = int(periods_needed * 4) + 30  # For 200 periods = ~824 days/~2.3 years ('5':~1030 days/~3 years)
        start_date = end_date - timedelta(days=days_buffer)
        
        logger.info(f"🔍 Getting OHLCV data for {ticker}: need {periods_needed} periods, fetching {days_buffer} calendar days")
        
        # Try database first
        db_data = self._fetch_ohlcv_data_from_db(ticker, start_date, end_date)
        
        if db_data is not None and len(db_data) >= periods_needed:
            logger.info(f"✅ Sufficient database data for {ticker}: {len(db_data)} records")
            return db_data
        
        # Fallback to yfinance if insufficient database data
        if db_data is not None:
            logger.info(f"⚠️ Insufficient database data for {ticker}: {len(db_data)} < {periods_needed} needed")
        
        yf_data = self._fetch_ohlcv_data_from_yfinance(ticker, start_date, end_date, save_to_db=save_to_db)
        
        if yf_data is not None and len(yf_data) >= periods_needed:
            logger.info(f"✅ Sufficient yfinance data for {ticker}: {len(yf_data)} records")
            return yf_data
        elif yf_data is not None:
            logger.warning(f"⚠️ Insufficient yfinance data for {ticker}: {len(yf_data)} < {periods_needed} needed")
            return yf_data  # Return what we have, indicators will handle insufficient data
        else:
            logger.error(f"❌ No OHLCV data available for {ticker}")
            return None
    
    def calculate_technical_indicators(self, ticker: str, save_to_db: bool = True) -> Optional[Dict]:
        """
        Calculate all technical indicators for a given ticker
        
        Args:
            ticker: Stock ticker symbol
            save_to_db: Whether to save calculated indicators to database
            
        Returns:
            Dictionary with technical indicators and signals or None if calculation failed
        """
        logger.info(f"🎯 Calculating technical indicators for {ticker}")
        
        try:
            # Import pandas-ta-classic
            import pandas_ta_classic as ta
        except ImportError:
            logger.error("pandas-ta-classic not available")
            return None
        
        # Get sufficient OHLCV data (200 periods for 200-day moving averages)
        df = self._get_sufficient_ohlcv_data(ticker, periods_needed=200, save_to_db=save_to_db)
        
        if df is None or len(df) < 50:  # Minimum 50 periods for basic calculations
            logger.error(f"❌ Insufficient data for {ticker}: {len(df) if df is not None else 0} records")
            return {
                'ticker': ticker,
                'error': True,
                'error_message': 'Insufficient OHLCV data for technical analysis',
                'data_source': 'error'
            }
        
        try:
            # Calculate technical indicators using pandas-ta-classic
            indicators = {}
            
            # Get the most recent values (latest trading day)
            latest = df.iloc[-1]
            latest_date = df.index[-1].date()
            
            # 1. RSI (14-period)
            rsi_values = ta.rsi(df['Close'], length=14)
            if not rsi_values.empty:
                latest_rsi = rsi_values.iloc[-1]
                indicators['rsi_14'] = latest_rsi
                indicators['rsi_signal'] = self._generate_rsi_signal(latest_rsi)
            
            # 2. MACD (12,26,9)
            macd_data = ta.macd(df['Close'], fast=12, slow=26, signal=9)
            if not macd_data.empty:
                indicators['macd_value'] = macd_data['MACD_12_26_9'].iloc[-1]
                indicators['macd_signal'] = macd_data['MACDs_12_26_9'].iloc[-1]
                indicators['macd_histogram'] = macd_data['MACDh_12_26_9'].iloc[-1]
                indicators['macd_signal_interpretation'] = self._generate_macd_signal(
                    indicators['macd_value'], indicators['macd_signal']
                )
            
            # 3. Elder Ray Index (Bull/Bear Power)
            eri_data = ta.eri(df['High'], df['Low'], df['Close'], length=13)
            if not eri_data.empty:
                indicators['bull_power'] = eri_data['BULLP_13'].iloc[-1]
                indicators['bear_power'] = eri_data['BEARP_13'].iloc[-1]
                indicators['elder_ray_signal'] = self._generate_elder_ray_signal(
                    indicators['bull_power'], indicators['bear_power']
                )
            
            # 4. ADX (14-period)
            adx_data = ta.adx(df['High'], df['Low'], df['Close'], length=14)
            if not adx_data.empty:
                indicators['adx_value'] = adx_data['ADX_14'].iloc[-1]
                indicators['plus_di'] = adx_data['DMP_14'].iloc[-1]
                indicators['minus_di'] = adx_data['DMN_14'].iloc[-1]
                indicators['adx_signal'] = self._generate_adx_signal(
                    indicators['adx_value'], indicators['plus_di'], indicators['minus_di']
                )
            
            # 5. Stochastic (14,3,3)
            stoch_data = ta.stoch(df['High'], df['Low'], df['Close'], k=14, d=3, smooth_k=3)
            if not stoch_data.empty:
                indicators['stoch_k'] = stoch_data['STOCHk_14_3_3'].iloc[-1]
                indicators['stoch_d'] = stoch_data['STOCHd_14_3_3'].iloc[-1]
                indicators['stoch_signal'] = self._generate_stochastic_signal(
                    indicators['stoch_k'], indicators['stoch_d']
                )
            
            # 6. Key Moving Averages
            ma_periods = [20, 50, 200]
            for period in ma_periods:
                if len(df) >= period:
                    # Simple Moving Average
                    sma_values = ta.sma(df['Close'], length=period)
                    if not sma_values.empty:
                        indicators[f'sma_{period}'] = sma_values.iloc[-1]
                        indicators[f'sma_{period}_signal'] = self._generate_ma_signal(
                            latest['Close'], sma_values.iloc[-1]
                        )
                    
                    # Exponential Moving Average
                    ema_values = ta.ema(df['Close'], length=period)
                    if not ema_values.empty:
                        indicators[f'ema_{period}'] = ema_values.iloc[-1]
                        indicators[f'ema_{period}_signal'] = self._generate_ma_signal(
                            latest['Close'], ema_values.iloc[-1]
                        )
            
            # 7. ATR (Average True Range) for volatility
            atr_values = ta.atr(df['High'], df['Low'], df['Close'], length=14)
            if not atr_values.empty:
                indicators['atr_14'] = atr_values.iloc[-1]
            
            # 8. Williams %R (14-period)
            williams_r_values = ta.willr(df['High'], df['Low'], df['Close'], length=14)
            if not williams_r_values.empty:
                indicators['williams_r'] = williams_r_values.iloc[-1]
                indicators['williams_r_signal'] = self._generate_williams_r_signal(indicators['williams_r'])
            
            # 9. CCI (Commodity Channel Index, 14-period)
            cci_values = ta.cci(df['High'], df['Low'], df['Close'], length=14)
            if not cci_values.empty:
                indicators['cci_14'] = cci_values.iloc[-1]
                indicators['cci_signal'] = self._generate_cci_signal(indicators['cci_14'])
            
            # 10. Ultimate Oscillator
            uo_values = ta.uo(df['High'], df['Low'], df['Close'])
            if not uo_values.empty:
                indicators['ultimate_osc'] = uo_values.iloc[-1]
                indicators['ultimate_osc_signal'] = self._generate_ultimate_osc_signal(indicators['ultimate_osc'])
            
            # 11. ROC (Rate of Change, 12-period)
            roc_values = ta.roc(df['Close'], length=12)
            if not roc_values.empty:
                indicators['roc_12'] = roc_values.iloc[-1]
                indicators['roc_signal'] = self._generate_roc_signal(indicators['roc_12'])
            
            # Add metadata
            indicators.update({
                'ticker': ticker,
                'calculation_date': latest_date.strftime('%Y-%m-%d'),
                'current_price': latest['Close'],
                'data_source': 'database+yfinance',
                'periods_analyzed': len(df),
                'error': False
            })
            
            logger.info(f"✅ Technical indicators calculated for {ticker}: {len([k for k in indicators.keys() if not k.startswith('_')])} indicators")
            
            # Save to database if enabled
            if save_to_db:
                self._save_technical_indicators_to_db(ticker, latest_date, indicators)
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators for {ticker}: {e}")
            return {
                'ticker': ticker,
                'error': True,
                'error_message': str(e),
                'data_source': 'error'
            }
    
    def _generate_rsi_signal(self, rsi_value: float) -> Dict:
        """Generate RSI signal using corrected logic (35-70 neutral zone)"""
        if rsi_value >= 80:
            return {'signal': 'Strong Sell', 'strength': 'Strong', 'description': 'Extremely overbought'}
        elif rsi_value >= 70:
            return {'signal': 'Sell', 'strength': 'Moderate', 'description': 'Overbought, potential selling opportunity'}
        elif rsi_value >= 35:
            return {'signal': 'Neutral', 'strength': 'Weak', 'description': 'Within neutral range'}
        elif rsi_value >= 20:
            return {'signal': 'Buy', 'strength': 'Moderate', 'description': 'Oversold, potential buying opportunity'}
        else:
            return {'signal': 'Strong Buy', 'strength': 'Strong', 'description': 'Extremely oversold'}
    
    def _generate_ma_signal(self, current_price: float, ma_value: float) -> Dict:
        """Generate moving average signal using corrected logic (±0.025% neutral zone)"""
        percentage_diff = ((current_price - ma_value) / ma_value) * 100
        
        if percentage_diff >= 0.025:
            return {'signal': 'Buy', 'strength': 'Moderate', 'description': f'Price {percentage_diff:+.3f}% above MA'}
        elif percentage_diff <= -0.025:
            return {'signal': 'Sell', 'strength': 'Moderate', 'description': f'Price {percentage_diff:+.3f}% below MA'}
        else:
            return {'signal': 'Neutral', 'strength': 'Weak', 'description': f'Price {percentage_diff:+.3f}% near MA'}
    
    def _generate_adx_signal(self, adx_value: float, plus_di: float, minus_di: float) -> Dict:
        """Generate ADX signal using corrected logic (-DI > +DI for sell)"""
        # Trend strength classification
        if adx_value < 25:
            trend_strength = "Weak"
        elif adx_value < 50:
            trend_strength = "Strong"
        else:
            trend_strength = "Very Strong"
        
        # Directional bias (CORRECTED: -DI > +DI for sell)
        if minus_di > plus_di:
            direction = "Sell"
            description = f"{trend_strength} downtrend (-DI > +DI)"
        elif plus_di > minus_di:
            direction = "Buy"
            description = f"{trend_strength} uptrend (+DI > -DI)"
        else:
            direction = "Neutral"
            description = f"{trend_strength} sideways (DI equal)"
        
        # Override for weak trends
        if adx_value < 25:
            direction = "Neutral"
            description = "Weak trend, no clear direction"
            strength = "Weak"
        else:
            strength = "Strong" if adx_value >= 50 else "Moderate"
        
        return {'signal': direction, 'strength': strength, 'description': description}
    
    def _generate_macd_signal(self, macd_value: float, signal_value: float) -> Dict:
        """Generate MACD signal interpretation"""
        if macd_value > signal_value:
            return {'signal': 'Buy', 'strength': 'Moderate', 'description': 'MACD above signal line'}
        elif macd_value < signal_value:
            return {'signal': 'Sell', 'strength': 'Moderate', 'description': 'MACD below signal line'}
        else:
            return {'signal': 'Neutral', 'strength': 'Weak', 'description': 'MACD at signal line'}
    
    def _generate_elder_ray_signal(self, bull_power: float, bear_power: float) -> Dict:
        """Generate Elder Ray Index signal interpretation"""
        if bull_power > 0 and bear_power > 0:
            return {'signal': 'Strong Buy', 'strength': 'Strong', 'description': 'Both Bull and Bear power positive'}
        elif bull_power > 0:
            return {'signal': 'Buy', 'strength': 'Moderate', 'description': 'Bull power positive'}
        elif bear_power < 0:
            return {'signal': 'Sell', 'strength': 'Moderate', 'description': 'Bear power negative'}
        elif bull_power < 0 and bear_power < 0:
            return {'signal': 'Strong Sell', 'strength': 'Strong', 'description': 'Both Bull and Bear power negative'}
        else:
            return {'signal': 'Neutral', 'strength': 'Weak', 'description': 'Mixed Elder Ray signals'}
    
    def _generate_stochastic_signal(self, stoch_k: float, stoch_d: float) -> Dict:
        """Generate Stochastic signal interpretation"""
        if stoch_k >= 80 and stoch_d >= 80:
            return {'signal': 'Sell', 'strength': 'Strong', 'description': 'Stochastic overbought'}
        elif stoch_k <= 20 and stoch_d <= 20:
            return {'signal': 'Buy', 'strength': 'Strong', 'description': 'Stochastic oversold'}
        elif stoch_k > stoch_d:
            return {'signal': 'Buy', 'strength': 'Moderate', 'description': '%K above %D'}
        elif stoch_k < stoch_d:
            return {'signal': 'Sell', 'strength': 'Moderate', 'description': '%K below %D'}
        else:
            return {'signal': 'Neutral', 'strength': 'Weak', 'description': 'Stochastic neutral'}
    
    def _generate_williams_r_signal(self, williams_r_value: float) -> Dict:
        """Generate Williams %R signal using corrected logic"""
        if williams_r_value > -20:
            return {'signal': 'Sell', 'strength': 'Strong', 'description': 'Overbought territory above -20'}
        elif williams_r_value < -80:
            return {'signal': 'Buy', 'strength': 'Strong', 'description': 'Oversold territory below -80'}
        elif williams_r_value > -50:
            return {'signal': 'Sell', 'strength': 'Moderate', 'description': 'Bearish bias above -50'}
        else:
            return {'signal': 'Buy', 'strength': 'Moderate', 'description': 'Bullish bias below -50'}
    
    def _generate_cci_signal(self, cci_value: float) -> Dict:
        """Generate CCI signal using corrected logic"""
        if cci_value > 100:
            return {'signal': 'Buy', 'strength': 'Strong', 'description': 'Strong upward deviation, bullish bias'}
        elif cci_value < -100:
            return {'signal': 'Sell', 'strength': 'Strong', 'description': 'Strong downward deviation, bearish bias'}
        elif cci_value > 0:
            return {'signal': 'Buy', 'strength': 'Moderate', 'description': 'Above zero, bullish bias'}
        else:
            return {'signal': 'Sell', 'strength': 'Moderate', 'description': 'Below zero, bearish bias'}
    
    def _generate_ultimate_osc_signal(self, uo_value: float) -> Dict:
        """Generate Ultimate Oscillator signal using corrected logic"""
        if uo_value > 70:
            return {'signal': 'Sell', 'strength': 'Strong', 'description': 'Overbought, potential sell signal'}
        elif uo_value < 30:
            return {'signal': 'Buy', 'strength': 'Strong', 'description': 'Oversold, potential buy signal'}
        elif uo_value > 50:
            return {'signal': 'Buy', 'strength': 'Moderate', 'description': 'Above midpoint, bullish bias'}
        else:
            return {'signal': 'Sell', 'strength': 'Moderate', 'description': 'Below midpoint, bearish bias'}
    
    def _generate_roc_signal(self, roc_value: float) -> Dict:
        """Generate ROC signal using corrected logic"""
        if roc_value > 5:
            return {'signal': 'Strong Buy', 'strength': 'Strong', 'description': 'Strong positive momentum'}
        elif roc_value > 0:
            return {'signal': 'Buy', 'strength': 'Moderate', 'description': 'Price increasing, bullish momentum'}
        elif roc_value < -5:
            return {'signal': 'Strong Sell', 'strength': 'Strong', 'description': 'Strong negative momentum'}
        elif roc_value < 0:
            return {'signal': 'Sell', 'strength': 'Moderate', 'description': 'Price decreasing, bearish momentum'}
        else:
            return {'signal': 'Neutral', 'strength': 'Weak', 'description': 'No significant momentum'}
    
    def _save_technical_indicators_to_db(self, ticker: str, date: date, indicators: Dict) -> bool:
        """
        Save technical indicators to database (only if final data available)
        
        Args:
            ticker: Stock ticker symbol
            date: Date for the indicators
            indicators: Dictionary with calculated indicators
            
        Returns:
            True if saved successfully, False otherwise
        """
        # Import trading day logic
        from .performance import get_last_completed_trading_day
        
        # Final data validation: Only save if date is last completed trading day or earlier
        last_complete_day = get_last_completed_trading_day()
        
        # Convert to date objects for comparison
        if isinstance(last_complete_day, datetime):
            last_complete_day = last_complete_day.date()
        
        if isinstance(date, datetime):
            date_only = date.date()
        else:
            date_only = date
        
        if date_only > last_complete_day:
            logger.warning(f"⚠️ Skipping database save for {ticker} on {date_only} - final data not available yet (last complete: {last_complete_day})")
            return False
        
        conn = self._get_database_connection()
        if not conn:
            return False
        
        try:
            # Prepare data for database insertion
            insert_data = {
                'ticker': ticker,
                'date': date.strftime('%Y-%m-%d'),
                'rsi_14': indicators.get('rsi_14'),
                'macd_value': indicators.get('macd_value'),
                'macd_signal': indicators.get('macd_signal'),
                'macd_histogram': indicators.get('macd_histogram'),
                'stoch_k': indicators.get('stoch_k'),
                'stoch_d': indicators.get('stoch_d'),
                'adx_value': indicators.get('adx_value'),
                'plus_di': indicators.get('plus_di'),
                'minus_di': indicators.get('minus_di'),
                'atr_14': indicators.get('atr_14'),
                'bull_power': indicators.get('bull_power'),
                'bear_power': indicators.get('bear_power'),
                'sma_5': indicators.get('sma_5'),
                'sma_9': indicators.get('sma_9'),
                'sma_10': indicators.get('sma_10'),
                'sma_20': indicators.get('sma_20'),
                'sma_21': indicators.get('sma_21'),
                'sma_50': indicators.get('sma_50'),
                'sma_100': indicators.get('sma_100'),
                'sma_200': indicators.get('sma_200'),
                'ema_5': indicators.get('ema_5'),
                'ema_9': indicators.get('ema_9'),
                'ema_10': indicators.get('ema_10'),
                'ema_20': indicators.get('ema_20'),
                'ema_21': indicators.get('ema_21'),
                'ema_50': indicators.get('ema_50'),
                'ema_100': indicators.get('ema_100'),
                'ema_200': indicators.get('ema_200')
            }
            
            # Build dynamic INSERT OR REPLACE query
            columns = list(insert_data.keys())
            placeholders = ', '.join(['?' for _ in columns])
            column_names = ', '.join(columns)
            
            query = f"""
            INSERT OR REPLACE INTO {self.technical_table}
            ({column_names})
            VALUES ({placeholders})
            """
            
            cursor = conn.cursor()
            cursor.execute(query, list(insert_data.values()))
            conn.commit()
            
            logger.info(f"✅ Technical indicators saved to database for {ticker} on {date}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving technical indicators for {ticker}: {e}")
            return False
        finally:
            conn.close()
    
    def _get_latest_indicator_date(self, ticker: str) -> Optional[datetime.date]:
        """Get the latest date with technical indicators for a ticker"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            query = f"""
            SELECT MAX(date) as latest_date
            FROM {self.technical_table}
            WHERE ticker = ?
            """
            
            cursor.execute(query, (ticker,))
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0]:
                return datetime.strptime(result[0], '%Y-%m-%d').date()
            return None
            
        except Exception as e:
            logger.error(f"Error getting latest indicator date for {ticker}: {e}")
            return None
    
    def _calculate_indicators_for_date(self, ohlcv_data: pd.DataFrame, target_date: datetime.date) -> Dict:
        """Calculate technical indicators using data up to target_date"""
        try:
            # Filter data up to target date
            ohlcv_data.index = pd.to_datetime(ohlcv_data.index)
            target_datetime = pd.Timestamp(target_date)
            filtered_data = ohlcv_data[ohlcv_data.index <= target_datetime].copy()
            
            if len(filtered_data) < 200:
                logger.warning(f"Insufficient data for {target_date}: only {len(filtered_data)} rows")
                return {}
            
            # Calculate all indicators using existing methods
            indicators = {}
            
            # Moving averages
            ma_results = self._calculate_moving_averages(filtered_data)
            if ma_results:
                indicators.update(ma_results)
            
            # Technical indicators
            tech_results = self._calculate_technical_indicators(filtered_data)
            if tech_results:
                indicators.update(tech_results)
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators for {target_date}: {e}")
            return {}
    
    def backfill_technical_indicators(self, ticker: str, days: int = 22) -> Dict:
        """
        Fill gaps in technical_indicators_daily table for time-series continuity
        
        Args:
            ticker: Stock ticker symbol
            days: Number of trading days to backfill (default: 22 = 1 month)
        
        Returns:
            Dict with success status and number of dates backfilled
        """
        try:
            from .performance import get_last_completed_trading_day, get_last_n_trading_days
            
            # 1. Check if data is current
            latest_date = self._get_latest_indicator_date(ticker)
            last_complete_day = get_last_completed_trading_day()
            
            if latest_date and latest_date >= last_complete_day:
                logger.info(f"✅ {ticker} technical indicators current (latest: {latest_date})")
                return {'success': True, 'backfilled': 0, 'reason': 'data_current'}
            
            # 2. Get required date range (last 22 trading days)
            required_dates = get_last_n_trading_days(days, end_date=last_complete_day)
            
            # 3. Query database for existing dates
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            placeholders = ','.join(['?' for _ in required_dates])
            query = f"""
            SELECT DISTINCT date
            FROM {self.technical_table}
            WHERE ticker = ? AND date IN ({placeholders})
            """
            
            date_strings = [d.strftime('%Y-%m-%d') for d in required_dates]
            cursor.execute(query, [ticker] + date_strings)
            existing_dates_raw = cursor.fetchall()
            conn.close()
            
            existing_dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in existing_dates_raw]
            
            # 4. Identify missing dates
            missing_dates = [d for d in required_dates if d not in existing_dates]
            
            if not missing_dates:
                logger.info(f"✅ {ticker} has complete {days}-day history")
                return {'success': True, 'backfilled': 0, 'reason': 'no_gaps'}
            
            logger.info(f"🔄 Backfilling {len(missing_dates)} missing dates for {ticker}")
            
            # 5. Fetch OHLCV data (includes gap detection)
            ohlcv_data = self._get_sufficient_ohlcv_data(
                ticker=ticker,
                periods_needed=200,  # Need sufficient data for 200-day MA
                save_to_db=True
            )
            
            if ohlcv_data is None or ohlcv_data.empty:
                logger.error(f"Failed to fetch OHLCV data for {ticker}")
                return {'success': False, 'error': 'ohlcv_fetch_failed'}
            
            # 6. Calculate and save indicators for each missing date
            backfilled_count = 0
            for date in sorted(missing_dates):
                indicators = self._calculate_indicators_for_date(ohlcv_data, date)
                
                if indicators:
                    success = self._save_technical_indicators_to_db(ticker, date, indicators)
                    if success:
                        backfilled_count += 1
            
            logger.info(f"✅ Backfilled {backfilled_count}/{len(missing_dates)} dates for {ticker}")
            return {
                'success': True,
                'backfilled': backfilled_count,
                'attempted': len(missing_dates)
            }
            
        except Exception as e:
            logger.error(f"Error backfilling technical indicators for {ticker}: {e}")
            return {'success': False, 'error': str(e)}
    
    def _get_price_extremes_from_db(self, ticker: str, period: str) -> Optional[Dict]:
        """Get cached price extremes from database with staleness check"""
        try:
            from .performance import get_last_completed_trading_day
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            query = f"""
            SELECT high_price, low_price, high_date, low_date,
                   level_minus_5pct, level_minus_10pct, level_minus_15pct,
                   level_minus_20pct, level_minus_33pct, updated_at
            FROM {self.extremes_table}
            WHERE ticker = ? AND period = ?
            """
            
            cursor.execute(query, (ticker, period))
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return None
            
            # Check staleness
            updated_at = datetime.strptime(result[9], '%Y-%m-%d %H:%M:%S').date()
            last_complete_day = get_last_completed_trading_day()
            
            if updated_at < last_complete_day:
                logger.info(f"Cached {period} extremes for {ticker} are stale (updated: {updated_at})")
                return None
            
            return {
                'high_price': result[0],
                'low_price': result[1],
                'high_date': result[2],
                'low_date': result[3],
                'level_minus_5pct': result[4],
                'level_minus_10pct': result[5],
                'level_minus_15pct': result[6],
                'level_minus_20pct': result[7],
                'level_minus_33pct': result[8],
                'updated_at': result[9]
            }
            
        except Exception as e:
            logger.error(f"Error getting price extremes from DB for {ticker} {period}: {e}")
            return None
    
    def _calculate_price_extremes(self, ticker: str, period: str, start_date: datetime.date, 
                                   close_based: bool = True) -> Optional[Dict]:
        """Calculate high/low extremes for a period"""
        try:
            # Fetch OHLCV data
            ohlcv_data = self._get_sufficient_ohlcv_data(ticker, periods_needed=200, save_to_db=True)
            if ohlcv_data is None or ohlcv_data.empty:
                return None
            
            # Filter data from start_date to present
            ohlcv_data.index = pd.to_datetime(ohlcv_data.index)
            start_datetime = pd.Timestamp(start_date)
            period_data = ohlcv_data[ohlcv_data.index >= start_datetime].copy()
            
            if period_data.empty:
                logger.warning(f"No data available for {ticker} from {start_date}")
                return None
            
            # Calculate high/low based on close_based flag
            if close_based:
                high_price = period_data['Close'].max()
                low_price = period_data['Close'].min()
                high_date = period_data['Close'].idxmax().date()
                low_date = period_data['Close'].idxmin().date()
            else:
                high_price = period_data['High'].max()
                low_price = period_data['Low'].min()
                high_date = period_data['High'].idxmax().date()
                low_date = period_data['Low'].idxmin().date()
            
            # Calculate breakdown levels
            breakdown_levels = {
                'level_minus_5pct': high_price * 0.95,
                'level_minus_10pct': high_price * 0.90,
                'level_minus_15pct': high_price * 0.85,
                'level_minus_20pct': high_price * 0.80,
                'level_minus_33pct': high_price * 0.67
            }
            
            return {
                'high_price': high_price,
                'low_price': low_price,
                'high_date': high_date.strftime('%Y-%m-%d'),
                'low_date': low_date.strftime('%Y-%m-%d'),
                **breakdown_levels
            }
            
        except Exception as e:
            logger.error(f"Error calculating price extremes for {ticker} {period}: {e}")
            return None
    
    def _save_price_extremes_to_db(self, ticker: str, period: str, extremes_data: Dict) -> bool:
        """Save price extremes to database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            query = f"""
            INSERT OR REPLACE INTO {self.extremes_table}
            (ticker, period, high_price, low_price, high_date, low_date,
             level_minus_5pct, level_minus_10pct, level_minus_15pct,
             level_minus_20pct, level_minus_33pct, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """
            
            cursor.execute(query, (
                ticker,
                period,
                extremes_data['high_price'],
                extremes_data['low_price'],
                extremes_data['high_date'],
                extremes_data['low_date'],
                extremes_data['level_minus_5pct'],
                extremes_data['level_minus_10pct'],
                extremes_data['level_minus_15pct'],
                extremes_data['level_minus_20pct'],
                extremes_data['level_minus_33pct']
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Price extremes saved for {ticker} {period}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving price extremes for {ticker} {period}: {e}")
            return False
    
    def calculate_52_week_analysis(self, ticker: str, user_52w_high: Optional[float] = None) -> Dict:
        """
        Calculate 52-week high/low analysis with 6 periods
        
        Args:
            ticker: Stock ticker symbol
            user_52w_high: Optional user-inputted intraday high for '52w' period
        
        Returns:
            Dict with all 6 periods and their breakdown levels
        """
        try:
            from .performance import get_trading_day_target, get_last_completed_trading_day
            
            last_complete_day = get_last_completed_trading_day()
            
            # Define all 6 periods with their start dates
            periods_config = {
                '52w_close': ('1y', True),   # Close-based calculation (use '1y' not '52w')
                '6m': ('6m', True),
                '3m': ('3m', True),
                '1m': ('1m', True),
                'ytd': ('ytd', True)
            }
            
            results = {}
            
            # Calculate all close-based periods first
            for period, (period_key, close_based) in periods_config.items():
                # Check cache first
                cached = self._get_price_extremes_from_db(ticker, period)
                if cached:
                    results[period] = cached
                    continue
                
                # Calculate if not cached or stale
                start_date = get_trading_day_target(period_key)
                extremes = self._calculate_price_extremes(ticker, period, start_date, close_based=True)
                
                if extremes:
                    self._save_price_extremes_to_db(ticker, period, extremes)
                    results[period] = extremes
            
            # Handle '52w' period with user override logic
            # First calculate intraday-based 52w high
            start_date_52w = get_trading_day_target('1y')  # Use '1y' for 52-week period
            intraday_extremes = self._calculate_price_extremes(ticker, '52w', start_date_52w, close_based=False)
            
            if intraday_extremes:
                intraday_high = intraday_extremes['high_price']
                
                # Get close-based high for validation (if available)
                close_based_high = results.get('52w_close', {}).get('high_price', 0)
                
                # Validation: user input must exceed close-based high
                if user_52w_high and close_based_high:
                    if user_52w_high <= close_based_high:
                        return {
                            'error': True,
                            'message': f'Custom high (${user_52w_high:.2f}) must exceed 52W closing high (${close_based_high:.2f})'
                        }
                    final_52w_high = max(intraday_high, user_52w_high)
                else:
                    # No validation if no user input or no 52w_close available
                    final_52w_high = max(intraday_high, user_52w_high) if user_52w_high else intraday_high
                
                # Use intraday low for consistency
                final_extremes = {
                    'high_price': final_52w_high,
                    'low_price': intraday_extremes['low_price'],
                    'high_date': intraday_extremes['high_date'],
                    'low_date': intraday_extremes['low_date'],
                    'level_minus_5pct': final_52w_high * 0.95,
                    'level_minus_10pct': final_52w_high * 0.90,
                    'level_minus_15pct': final_52w_high * 0.85,
                    'level_minus_20pct': final_52w_high * 0.80,
                    'level_minus_33pct': final_52w_high * 0.67
                }
                
                self._save_price_extremes_to_db(ticker, '52w', final_extremes)
                results['52w'] = final_extremes
            
            return {'success': True, 'periods': results}
            
        except Exception as e:
            logger.error(f"Error calculating 52-week analysis for {ticker}: {e}")
            return {'success': False, 'error': str(e)}
    
    def calculate_comprehensive_analysis(self, ticker: str, save_to_db: bool = True) -> Dict:
        """
        Calculate comprehensive technical analysis for Dashboard 1
        
        This is the main method called by the UI. It orchestrates all component
        calculations and returns a properly structured dictionary for display.
        
        Args:
            ticker: Stock ticker symbol
            save_to_db: Whether to save calculated data to database
            
        Returns:
            Dictionary with comprehensive analysis data structured for UI:
            {
                'ticker': str,
                'error': bool,
                'timestamp': str,
                'moving_averages': dict,      # Phase 2 implementation
                'technical_indicators': dict,  # Reformatted from calculate_technical_indicators()
                'price_extremes': dict,        # Phase 3 implementation
                'pivot_points': dict,          # Phase 4 implementation
                'rolling_signals': dict        # Phase 5 implementation (future)
            }
        """
        logger.info(f"🎯 Starting comprehensive technical analysis for {ticker}")
        
        try:
            # Get basic technical indicators (existing method)
            tech_indicators = self.calculate_technical_indicators(ticker, save_to_db=save_to_db)
            
            if tech_indicators.get('error'):
                # Return error structure matching UI expectations
                return {
                    'ticker': ticker,
                    'error': True,
                    'message': tech_indicators.get('error_message', 'Technical indicator calculation failed'),
                    'timestamp': datetime.now().isoformat()
                }
            
            # Prepare comprehensive analysis structure
            analysis_data = {
                'ticker': ticker,
                'error': False,
                'timestamp': datetime.now().isoformat(),
                'current_price': tech_indicators.get('current_price'),
                'calculation_date': tech_indicators.get('calculation_date'),
                
                # Phase 2: Moving Averages
                'moving_averages': self._calculate_moving_averages(ticker, save_to_db=save_to_db),
                
                # Reformat technical indicators for UI consumption
                'technical_indicators': self._format_technical_indicators(tech_indicators),
                
                # Phase 3: 52-Week High Analysis (placeholder for now)
                'price_extremes': {
                    'status': 'not_implemented',
                    'message': '52-week high analysis - Phase 3'
                },
                
                # Phase 4: Pivot Points (placeholder for now)
                'pivot_points': {
                    'status': 'not_implemented',
                    'message': 'Pivot points analysis - Phase 4'
                },
                
                # Phase 5: Rolling Signals (placeholder for future)
                'rolling_signals': {
                    'status': 'not_implemented',
                    'message': 'Rolling signal heatmap - Phase 5 (future)'
                }
            }
            
            logger.info(f"✅ Comprehensive analysis complete for {ticker}")
            return analysis_data
            
        except Exception as e:
            logger.error(f"❌ Error in comprehensive analysis for {ticker}: {e}")
            return {
                'ticker': ticker,
                'error': True,
                'message': f'Comprehensive analysis failed: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def _format_technical_indicators(self, raw_indicators: Dict) -> Dict:
        """
        Reformat technical indicators from calculate_technical_indicators() for UI display
        
        Args:
            raw_indicators: Raw dictionary from calculate_technical_indicators()
            
        Returns:
            Formatted dictionary suitable for technical indicators table display
        """
        # Extract relevant indicators with their signals
        formatted = {
            'rsi_14': {
                'value': raw_indicators.get('rsi_14'),
                'signal': raw_indicators.get('rsi_signal', {})
            },
            'macd': {
                'value': raw_indicators.get('macd_value'),
                'signal_line': raw_indicators.get('macd_signal'),
                'histogram': raw_indicators.get('macd_histogram'),
                'signal': raw_indicators.get('macd_signal_interpretation', {})
            },
            'stochastic': {
                'k': raw_indicators.get('stoch_k'),
                'd': raw_indicators.get('stoch_d'),
                'signal': raw_indicators.get('stoch_signal', {})
            },
            'adx': {
                'value': raw_indicators.get('adx_value'),
                'plus_di': raw_indicators.get('plus_di'),
                'minus_di': raw_indicators.get('minus_di'),
                'signal': raw_indicators.get('adx_signal', {})
            },
            'elder_ray': {
                'bull_power': raw_indicators.get('bull_power'),
                'bear_power': raw_indicators.get('bear_power'),
                'signal': raw_indicators.get('elder_ray_signal', {})
            },
            'atr_14': {
                'value': raw_indicators.get('atr_14'),
                'signal': {'signal': 'N/A', 'description': 'Volatility measure only'}
            },
            'williams_r': {
                'value': raw_indicators.get('williams_r'),
                'signal': raw_indicators.get('williams_r_signal', {})
            },
            'cci_14': {
                'value': raw_indicators.get('cci_14'),
                'signal': raw_indicators.get('cci_signal', {})
            },
            'ultimate_osc': {
                'value': raw_indicators.get('ultimate_osc'),
                'signal': raw_indicators.get('ultimate_osc_signal', {})
            },
            'roc_12': {
                'value': raw_indicators.get('roc_12'),
                'signal': raw_indicators.get('roc_signal', {})
            }
        }
        
        return formatted
    
    def _calculate_moving_averages(self, ticker: str, save_to_db: bool = True) -> Dict:
        """
        Calculate comprehensive moving averages analysis for all 8 periods
        
        Implements PRD specifications:
        - Periods: 5, 9, 10, 20, 21, 50, 100, 200
        - Both SMA and EMA for each period
        - Bidirectional percentages: MA/P0 and P0/MA
        - Signals: Buy/Sell/Neutral (±0.025% threshold)
        
        Args:
            ticker: Stock ticker symbol
            save_to_db: Whether to save data to database
            
        Returns:
            Dictionary with comprehensive moving averages data for 8x8 table
        """
        logger.info(f"📊 Calculating comprehensive moving averages for {ticker}")
        
        try:
            import pandas_ta_classic as ta
        except ImportError:
            logger.error("pandas-ta-classic not available")
            return {
                'error': True,
                'message': 'pandas-ta-classic library required for moving averages'
            }
        
        # Get sufficient OHLCV data (need 200+ periods for 200-day MA)
        df = self._get_sufficient_ohlcv_data(ticker, periods_needed=200, save_to_db=save_to_db)
        
        if df is None or len(df) < 200:
            logger.error(f"Insufficient data for {ticker}: {len(df) if df is not None else 0} records")
            return {
                'error': True,
                'message': f'Insufficient data for moving averages: need 200 periods, have {len(df) if df is not None else 0}'
            }
        
        try:
            # Current price - fetch live price from yfinance with session caching
            current_price = self.performance_calculator.get_current_price(ticker)
            
            # Fallback to last database close if yfinance fails
            if current_price is None:
                current_price = df['Close'].iloc[-1]
                logger.warning(f"⚠️ Using last database close for {ticker}: ${current_price:.2f}")
            
            current_date = df.index[-1]
            
            # All periods per PRD specification
            periods = [5, 9, 10, 20, 21, 50, 100, 200]
            
            ma_data = {
                'ticker': ticker,
                'current_price': current_price,
                'calculation_date': current_date.strftime('%Y-%m-%d'),
                'timestamp': current_date.isoformat(),
                'error': False,
                'periods': {}
            }
            
            # Calculate for each period
            for period in periods:
                if len(df) < period:
                    logger.warning(f"Skipping MA{period} - insufficient data")
                    continue
                
                # Calculate SMA and EMA
                sma_series = ta.sma(df['Close'], length=period)
                ema_series = ta.ema(df['Close'], length=period)
                
                if sma_series.empty or ema_series.empty:
                    logger.warning(f"Failed to calculate MA{period}")
                    continue
                
                sma_value = sma_series.iloc[-1]
                ema_value = ema_series.iloc[-1]
                
                # Calculate bidirectional percentages
                sma_vs_price = ((sma_value - current_price) / current_price) * 100  # MA/P0
                price_vs_sma = ((current_price - sma_value) / sma_value) * 100      # P0/MA
                
                ema_vs_price = ((ema_value - current_price) / current_price) * 100  # MA/P0
                price_vs_ema = ((current_price - ema_value) / ema_value) * 100      # P0/MA
                
                # Generate signals using ±0.025% threshold
                sma_signal = self._generate_ma_signal(current_price, sma_value)
                ema_signal = self._generate_ma_signal(current_price, ema_value)
                
                # Store comprehensive data for this period
                ma_data['periods'][f'MA{period}'] = {
                    'sma': {
                        'value': sma_value,
                        'ma_vs_price': sma_vs_price,      # SMA/P0 (negative if price above)
                        'price_vs_ma': price_vs_sma,      # P0/SMA (positive if price above)
                        'signal': sma_signal
                    },
                    'ema': {
                        'value': ema_value,
                        'ma_vs_price': ema_vs_price,      # EMA/P0 (negative if price above)
                        'price_vs_ma': price_vs_ema,      # P0/EMA (positive if price above)
                        'signal': ema_signal
                    }
                }
            
            logger.info(f"✅ Calculated moving averages for {len(ma_data['periods'])} periods")
            return ma_data
            
        except Exception as e:
            logger.error(f"Error calculating moving averages for {ticker}: {e}")
            return {
                'error': True,
                'message': f'Moving averages calculation failed: {str(e)}'
            }
    
    def calculate_technical_analysis_for_group(self, tickers: List[str], save_to_db: bool = True) -> List[Dict]:
        """
        Calculate technical analysis for a group of tickers
        
        Args:
            tickers: List of ticker symbols
            save_to_db: Whether to save calculated indicators to database
            
        Returns:
            List of dictionaries with technical analysis for each ticker
        """
        logger.info(f"🎯 Calculating technical analysis for {len(tickers)} tickers")
        results = []
        
        for i, ticker in enumerate(tickers, 1):
            logger.info(f"📊 Processing technical analysis for {ticker} ({i}/{len(tickers)})...")
            technical_data = self.calculate_technical_indicators(ticker, save_to_db=save_to_db)
            results.append(technical_data)
        
        # Log summary
        successful_count = len([r for r in results if not r.get('error', False)])
        error_count = len([r for r in results if r.get('error', False)])
        
        logger.info(f"📊 Technical analysis complete:")
        logger.info(f"   - Successful calculations: {successful_count} tickers")
        logger.info(f"   - Errors: {error_count} tickers")
        
        return results


# Factory function for backward compatibility
def get_technical_calculator() -> DatabaseIntegratedTechnicalCalculator:
    """Factory function to get a database-integrated technical analysis calculator instance"""
    return DatabaseIntegratedTechnicalCalculator()


# Convenience function for single ticker analysis
def calculate_technical_analysis(ticker: str, save_to_db: bool = True) -> Dict:
    """
    Quick function to calculate technical analysis for a single ticker
    
    Args:
        ticker: Stock ticker symbol
        save_to_db: Whether to save indicators to database
        
    Returns:
        Technical analysis data dictionary
    """
    calculator = DatabaseIntegratedTechnicalCalculator()
    return calculator.calculate_technical_indicators(ticker, save_to_db=save_to_db)
