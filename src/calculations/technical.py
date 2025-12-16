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
from typing import Dict, List, Optional, Tuple, Union, Any
from pathlib import Path
import logging

# Import trading day logic from performance module
from .performance import (
    get_last_completed_trading_day,
    get_last_n_trading_days,
    is_us_trading_day,
    get_trading_day_target
)

# Rule-engine harness: Option-C signals via rulebook + DSL
try:
    from .signal_classifier import run_optionc_heatmap, DEFAULT_SIGNAL_SCORES
except Exception:  # keep broad during migration; narrow later
    run_optionc_heatmap = None
    DEFAULT_SIGNAL_SCORES = {"strong_sell": -2, "sell": -1, "neutral": 0, "buy": 1, "strong_buy": 2}


try:
    # package-relative import (when running as part of src.calculations)
    from .indicator_preprocessor import compute_all_indicators
except ImportError:  # pragma: no cover
    # Fallback: absolute import (e.g., when running this file standalone)
    from src.calculations.indicator_preprocessor import compute_all_indicators


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Feature flag: controls whether calculate_technical_indicators uses the new
# Option-C TA engine (indicator_preprocessor) or the legacy pandas-ta-classic path. (12/7/25, GPT+) 
USE_NEW_TA_ENGINE: bool = False

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
            
            # Align timezone-awareness between yfinance index and start/end datetimes.
            # yfinance often returns a tz-aware DatetimeIndex (e.g., America/New_York),
            # while our start_date/end_date are naive -> comparison raises.
            idx = hist_data.index
            start_ts = pd.Timestamp(start_date)
            end_ts = pd.Timestamp(end_date)
            if getattr(idx, "tz", None) is not None:
                # Make bounds tz-aware in the same timezone as the index
                if start_ts.tzinfo is None:
                    start_ts = start_ts.tz_localize(idx.tz)
                else:
                    start_ts = start_ts.tz_convert(idx.tz)
                if end_ts.tzinfo is None:
                    end_ts = end_ts.tz_localize(idx.tz)
                else:
                    end_ts = end_ts.tz_convert(idx.tz)

            # Filter to requested date range
            #filtered_data = hist_data[(hist_data.index >= start_date) & (hist_data.index <= end_date)]
            filtered_data = hist_data[(idx >= start_ts) & (idx <= end_ts)]

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

    # A private helper that calls the new indicator engine (12/7/25; GPT+)    
    def _compute_indicators_with_engine(
        self,
        df: pd.DataFrame,
        config: Dict[str, Any] | None = None,
    ) -> pd.DataFrame:
        """
        Enrich an OHLCV DataFrame with Option-C indicator columns using the
        new TA Rule Engine preprocessor (indicator_preprocessor.compute_all_indicators).

        This is a parallel path that does NOT alter or depend on the legacy
        pandas-ta-classic logic. It simply returns a new DataFrame with the
        same index plus additional indicator columns.
        """

        return compute_all_indicators(df, config=config)        

    # New public method that fetches OHLCV via the existing DB/yfinance logic, runs the new `compute_all_indicators`, 
    # returns a DataFrame enriched with Option C indicator columns. (12/7/25; GPT+)   
    def calculate_optionc_indicators(
        self,
        ticker: str,
        save_to_db: bool = False,
        config: Dict[str, Any] | None = None,
    ) -> Optional[pd.DataFrame]:
        """
        Fetch sufficient OHLCV data for `ticker` and compute Option-C indicators
        using the new TA Rule Engine preprocessor.

        This method:
          - Uses the existing DB-first + yfinance-fallback OHLCV pipeline
          - Enriches the DataFrame with Option-C indicator columns
          - Does NOT compute legacy text signals
          - Does NOT change the behavior of calculate_technical_indicators()

        Returns:
            DataFrame with OHLCV + Option-C indicator columns, or None on failure.
        """
        # Re-use the existing helper that knows how much history we need
        df = self._get_sufficient_ohlcv_data(
            ticker=ticker,
            periods_needed=200,      # enough for SMA_200, BB_20_2, etc.
            save_to_db=save_to_db,
        )

        if df is None or df.empty:
            logger.error(f"Unable to retrieve sufficient OHLCV data for {ticker}")
            return None

        df_ind = self._compute_indicators_with_engine(df, config=config)
        return df_ind

    # New-engine variant of calculate_technical_indicators(); (12/8/25, GPT+)
    def _calculate_technical_indicators_optionc(
        self,
        ticker: str,
        save_to_db: bool = False,
        config: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """
        New-engine variant of calculate_technical_indicators().

        Uses:
          - calculate_optionc_indicators() to compute Option-C indicator columns
          - Existing *_signal helper methods to generate legacy-style signals

        Returns a dict shaped like the legacy implementation: a flat mapping
        of indicator values and their signals. For now this covers the subset
        of indicators we currently compute via indicator_preprocessor:
          - RSI(14)
          - MACD(12,26,9)
          - Stochastic (14,3,3)
          - SMA/EMA (20, 50, 200)
          - Bollinger (20, 2σ) is computed but not yet used in signals.
        """
        logger.info(f"🎯 [NEW ENGINE] Calculating Option-C technical indicators for {ticker}")

        # Use the existing DB-first OHLCV pipeline + preprocessor
        df_ind = self.calculate_optionc_indicators(
            ticker=ticker,
            save_to_db=save_to_db,
            config=config,
        )

        if df_ind is None or df_ind.empty or len(df_ind) < 50:
            logger.error(
                f"❌ [NEW ENGINE] Insufficient data for {ticker}: "
                f"{0 if df_ind is None else len(df_ind)} records"
            )
            return {
                "ticker": ticker,
                "error": True,
                "error_message": "Insufficient OHLCV data for technical analysis (Option-C engine)",
                "data_source": "error",
            }

        indicators: Dict[str, Any] = {}

        latest = df_ind.iloc[-1]
        # Index is usually DatetimeIndex; be defensive
        if hasattr(df_ind.index[-1], "date"):
            latest_date = df_ind.index[-1].date()
        else:
            latest_date = None

        # ------------------ RSI (14) ------------------
        if "RSI_14" in df_ind.columns and not pd.isna(latest["RSI_14"]):
            rsi_val = float(latest["RSI_14"])
            indicators["rsi_14"] = rsi_val
            indicators["rsi_signal"] = self._generate_rsi_signal(rsi_val)

        # ------------------ MACD (12,26,9) ------------------
        macd_cols = {"MACD_12_26_9_line", "MACD_12_26_9_signal", "MACD_12_26_9_hist"}
        if macd_cols.issubset(df_ind.columns):
            macd_line = float(latest["MACD_12_26_9_line"])
            macd_signal = float(latest["MACD_12_26_9_signal"])
            macd_hist = float(latest["MACD_12_26_9_hist"])

            indicators["macd_value"] = macd_line
            indicators["macd_signal"] = macd_signal
            indicators["macd_histogram"] = macd_hist

            histogram_list = (
                df_ind["MACD_12_26_9_hist"].dropna().tolist()
                if "MACD_12_26_9_hist" in df_ind.columns
                else []
            )

            indicators["macd_signal_interpretation"] = self._generate_macd_signal(
                macd_value=macd_line,
                signal_value=macd_signal,
                fast=12,
                slow=26,
                signal_period=9,
                histogram_data=histogram_list,
            )

        # ------------------ Stochastic (14,3,3) ------------------
        if {"STOCHK_14_3_3", "STOCHD_14_3_3"}.issubset(df_ind.columns):
            k_val = float(latest["STOCHK_14_3_3"])
            d_val = float(latest["STOCHD_14_3_3"])
            indicators["stoch_k"] = k_val
            indicators["stoch_d"] = d_val
            indicators["stoch_signal"] = self._generate_stochastic_signal(k_val, d_val)

        # ------------------ Moving Averages (20, 50, 200) ------------------
        close_latest = float(latest["Close"]) if "Close" in df_ind.columns else None
        ma_periods = [20, 50, 200]

        for period in ma_periods:
            sma_col = f"SMA_{period}"
            ema_col = f"EMA_{period}"

            # SMA
            if sma_col in df_ind.columns and not pd.isna(latest[sma_col]):
                sma_val = float(latest[sma_col])
                indicators[f"sma_{period}"] = sma_val
                if close_latest is not None:
                    indicators[f"sma_{period}_signal"] = self._generate_ma_signal(
                        close_latest, sma_val
                    )

            # EMA (only for those we actually compute → 20, 50 right now)
            if ema_col in df_ind.columns and not pd.isna(latest[ema_col]):
                ema_val = float(latest[ema_col])
                indicators[f"ema_{period}"] = ema_val
                if close_latest is not None:
                    indicators[f"ema_{period}_signal"] = self._generate_ma_signal(
                        close_latest, ema_val
                    )

        # ------------------ ADX (14) + DI+/DI- ------------------ (12/8, GPT+)
        if {"ADX_14", "DIp_14", "DIn_14"}.issubset(df_ind.columns):
            adx_val = float(latest["ADX_14"])
            plus_di = float(latest["DIp_14"])
            minus_di = float(latest["DIn_14"])

            indicators["adx_value"] = adx_val
            indicators["plus_di"] = plus_di
            indicators["minus_di"] = minus_di
            indicators["adx_signal"] = self._generate_adx_signal(
                adx_value=adx_val,
                plus_di=plus_di,
                minus_di=minus_di,
            )

        # NOTE:
        #  - This block is building the *legacy-style* `technical_indicators` dict
        #    (values + *_signal helpers) for the existing Streamlit tables.
        #  - The Option-C preprocessor now computes additional columns (e.g., ROC_*,
        #    WILLR_*), and the rule-engine/rolling-heatmap path can consume them.
        #  - However, we have not yet added legacy-style mappings/signals for those
        #    indicators in this dict. When/if we want them to appear in the legacy
        #    tables, we should add explicit mappings here.

        # Save to database if enabled and we have a latest_date
        if save_to_db and latest_date is not None:
            self._save_technical_indicators_to_db(ticker, latest_date, indicators)

        return indicators

    def calculate_rule_engine_signals_optionc(
        self,
        ticker: str,
        feature_scope: str = "heatmap",
        rules_path: Union[str, Path] = "master_rules_normalized.json",
        save_to_db: bool = False,
        config: Dict[str, Any] | None = None,
        indicators: list[str] | None = None,
        return_type: str = "scores",
    ) -> Any:     #Dict[str, Dict[str, pd.Series]]:
        """
        Run the rulebook/DSL engine on the Option-C indicator DataFrame for `ticker`.

        Returns numeric scores in [-2, 2] for the Option C slice:
        {
            "RSI": {"14": Series[int]},
            "MACD": {"12_26_9": Series[int]},
            "Stochastic": {"14_3_3": Series[int]},
            "ADX": {"14": Series[int]},
        }

        This is a parallel path for the rolling heatmap backend and does not affect
        legacy calculate_technical_indicators() behavior.
        """
        df_ind = self.calculate_optionc_indicators(
            ticker=ticker,
            save_to_db=save_to_db,
            config=config,
        )

        if df_ind is None or df_ind.empty:
            logger.warning(
                "⚠️ [NEW ENGINE] No Option-C indicator data available for rule-engine "
                f"evaluation on {ticker} (df is None/empty)."
            )
            return {}

        # Default indicator set: Option C baseline (non-breaking).
        # Tests / Option A onboarding can pass an explicit list.
        if indicators is None:
            indicators = ["RSI", "MACD", "Stochastic", "ADX"]
            
        scores = run_optionc_heatmap(
            df_ind, 
            rules_path=rules_path,
            indicators=indicators)

        if return_type not in ("scores", "rolling"):
            raise ValueError(f"return_type must be 'scores' or 'rolling', got: {return_type}")

        if return_type == "rolling":
            return self._build_optionc_rolling_signals(
                ticker=ticker,
                df_ind=df_ind,
                scores=scores,
                days=10,
            )        
        
        return scores


    def _build_optionc_rolling_signals(
        self,
        ticker: str,
        df_ind: pd.DataFrame,
        scores: Dict[str, Dict[str, pd.Series]],
        days: int = 10,
    ) -> Dict[str, Any]:
        """
        Build rolling heatmap payload for the *rule-engine* indicator set.

        Historical note:
          - This started as "Option C only" during the initial vertical slice.
          - As we onboard additional momentum params (Option A), the same payload
            contract remains, but the indicator/param coverage expands via metadata.
        """
        if df_ind is None or df_ind.empty or not scores:
            return {
                "engine": "optionc_rulebook_v1",
                "status": "empty",
                "ticker": ticker,
                "dates": [],
                "short_term": None,
                "intermediate_term": None,
                "long_term": None,
                "composite_scores": {"short_term": None, "overall": None},
                "extras": {},
            }

        df_ind = df_ind.sort_index()
        last_dates = df_ind.index[-days:]

        date_keys = [
            d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            for d in last_dates
        ]

        score_to_label = {v: k for k, v in DEFAULT_SIGNAL_SCORES.items()}

        # Rolling metadata:
        #   This list controls which indicator/param variants are emitted into the rolling
        #   heatmap payload. The preprocessor may compute more columns than are included
        #   here; inclusion is controlled deliberately to stage onboarding.
        optionc_meta = [
            {
                "engine_indicator": "RSI",
                "param_key": "14",
                "display_key": "RSI_14",
                "value_col": "RSI_14",
            },
            {
                "engine_indicator": "RSI",
                "param_key": "10",
                "display_key": "RSI_10",
                "value_col": "RSI_10",
            },
            {
                "engine_indicator": "RSI",
                "param_key": "21",
                "display_key": "RSI_21",
                "value_col": "RSI_21",
            },
            {
                "engine_indicator": "RSI",
                "param_key": "30",
                "display_key": "RSI_30",
                "value_col": "RSI_30",
            },
            {
                "engine_indicator": "MACD",
                "param_key": "12_26_9",
                "display_key": "MACD_12_26_9",
                "value_col": "MACD_12_26_9_hist",
            },
            {
                "engine_indicator": "MACD",
                "param_key": "5_34_1",
                "display_key": "MACD_5_34_1",
                "value_col": "MACD_5_34_1_hist",
            },
            {
                "engine_indicator": "MACD",
                "param_key": "8_17_5",
                "display_key": "MACD_8_17_5",
                "value_col": "MACD_8_17_5_hist",
            },
            {
                "engine_indicator": "MACD",
                "param_key": "20_50_10",
                "display_key": "MACD_20_50_10",
                "value_col": "MACD_20_50_10_hist",
            },            
            {
                "engine_indicator": "Stochastic",
                "param_key": "14_3_3",
                "display_key": "STOCH_14_3_3",
                "value_col": "STOCHK_14_3_3",
            },
            {
                "engine_indicator": "Stochastic",
                "param_key": "5_3_3",
                "display_key": "STOCH_5_3_3",
                "value_col": "STOCHK_5_3_3",
            },
            {
                "engine_indicator": "Stochastic",
                "param_key": "21_5_5",
                "display_key": "STOCH_21_5_5",
                "value_col": "STOCHK_21_5_5",
            },
            {
                "engine_indicator": "ROC",
                "param_key": "9",
                "display_key": "ROC_9",
                "value_col": "ROC_9",
            },
            {
                "engine_indicator": "ROC",
                "param_key": "12",
                "display_key": "ROC_12",
                "value_col": "ROC_12",
            },
            {
                "engine_indicator": "ROC",
                "param_key": "20",
                "display_key": "ROC_20",
                "value_col": "ROC_20",
            },
            {
                "engine_indicator": "ROC",
                "param_key": "50",
                "display_key": "ROC_50",
                "value_col": "ROC_50",
            },
            {
                "engine_indicator": "Williams_R",
                "param_key": "5",
                "display_key": "WILLR_5",
                "value_col": "WILLR_5",
            },
            {
                "engine_indicator": "Williams_R",
                "param_key": "14",
                "display_key": "WILLR_14",
                "value_col": "WILLR_14",
            },
            {
                "engine_indicator": "Williams_R",
                "param_key": "20",
                "display_key": "WILLR_20",
                "value_col": "WILLR_20",
            },            
            {
                "engine_indicator": "ADX",
                "param_key": "14",
                "display_key": "ADX_14",
                "value_col": "ADX_14",
            },
        ]

        indicators = [m["display_key"] for m in optionc_meta]
        data: Dict[str, Dict[str, Any]] = {}

        for idx, dt in enumerate(last_dates):
            date_key = date_keys[idx]
            row_cells: Dict[str, Any] = {}

            for meta in optionc_meta:
                eng_name = meta["engine_indicator"]
                param_key = meta["param_key"]
                display_key = meta["display_key"]
                value_col = meta["value_col"]

                series_dict = scores.get(eng_name, {})
                score_series = series_dict.get(param_key)
                if score_series is None or dt not in score_series.index:
                    continue

                raw_score = score_series.loc[dt]
                if pd.isna(raw_score):
                    continue

                try:
                    score_int = int(raw_score)
                except (TypeError, ValueError):
                    continue

                label = score_to_label.get(score_int, "neutral")

                value = None
                if value_col in df_ind.columns and dt in df_ind.index:
                    v = df_ind.loc[dt, value_col]
                    if not pd.isna(v):
                        value = float(v)

                if value is not None:
                    hover = f"{display_key} = {value:.2f}, score={score_int} ({label})"
                else:
                    hover = f"{display_key}, score={score_int} ({label})"

                row_cells[display_key] = {
                    "score": score_int,
                    "signal": label,
                    "value": value,
                    "hover": hover,
                }

            if row_cells:
                data[date_key] = row_cells

        # Build + cache the MultiIndex score DataFrame for future Plotly heatmap use.
        # This does not change the returned payload.
        try:
            df_scores = self._build_optionc_scores_multiindex_df(
                scores=scores,
                optionc_meta=optionc_meta,
                last_dates=last_dates,
            )
            if not hasattr(self, "_rolling_df_cache"):
                self._rolling_df_cache = {}
            self._rolling_df_cache[(ticker, "short_term", "optionc_scores")] = df_scores
        except Exception as e:
            logger.warning(f"Rolling DF cache build failed for {ticker}: {e}")

        status = "ok" if data else "empty"

        return {
            "engine": "optionc_rulebook_v1",
            "status": status,
            "ticker": ticker,
            "dates": list(data.keys()),
            "short_term": {
                "indicators": indicators,
                "data": data,
            } if data else None,
            "intermediate_term": None,
            "long_term": None,
            "composite_scores": {
                "short_term": {
                    "momentum": None,
                    "trend": None,
                    "volatility": None,
                    "volume": None,
                    "overall": None,
                },
                "overall": None,
            },
            "extras": {},
        }

    # Patch: MultiIndexDataFrame for Plotly 
    def _build_optionc_scores_multiindex_df(
        self,
        scores: Dict[str, Dict[str, pd.Series]],
        optionc_meta: List[Dict[str, str]],
        last_dates: pd.Index,
    ) -> pd.DataFrame:
        """
        Build a MultiIndex DataFrame of numeric scores for Option C.

        Output:
        index: last_dates
        columns: MultiIndex (engine_indicator, param_key)
        values: numeric score in [-2 .. 2]  
        """
        cols = []
        series_list = []

        for meta in optionc_meta:
            eng = meta["engine_indicator"]
            param = meta["param_key"]

            s = scores.get(eng, {}).get(param)
            if s is None:
                continue

            # align to our rolling window
            s2 = s.reindex(last_dates)

            cols.append((eng, param))
            series_list.append(s2)

        if not series_list:
            return pd.DataFrame(index=last_dates)

        df = pd.concat(series_list, axis=1)
        df.columns = pd.MultiIndex.from_tuples(cols, names=["indicator", "params"])
        return df


    def calculate_technical_indicators(self, ticker: str, save_to_db: bool = False) -> Optional[Dict]:
        """
        Calculate all technical indicators for a given ticker
        
        Args:
            ticker: Stock ticker symbol
            save_to_db: Whether to save calculated indicators to database
            
        Returns:
            Dictionary with technical indicators and signals or None if calculation failed
        """
        logger.info(f"🎯 Calculating technical indicators for {ticker}")


        # Optional parallel path: use new Option-C TA engine when enabled. (12/8/25; GPT+)
        if USE_NEW_TA_ENGINE:
            return self._calculate_technical_indicators_optionc(
                ticker=ticker,
                save_to_db=save_to_db,
            )
                
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
                
                # Extract histogram as list for magnitude-filtered signal generation
                histogram_list = macd_data['MACDh_12_26_9'].tolist()
                
                indicators['macd_signal_interpretation'] = self._generate_macd_signal(
                    macd_value=indicators['macd_value'],
                    signal_value=indicators['macd_signal'],
                    fast=12,
                    slow=26,
                    signal_period=9,
                    histogram_data=histogram_list
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
    
    def _generate_macd_signal(self, macd_value: float, signal_value: float, histogram: float = None, 
                              fast: int = 12, slow: int = 26, signal_period: int = 9,
                              histogram_data: list = None) -> Dict:
        """
        Generate MACD signal interpretation with magnitude filtering.
        
        Uses volatility-normalized magnitude filtering to reduce false signals.
        Only generates buy/sell signals if the histogram magnitude exceeds the threshold.
        
        Args:
            macd_value: Current MACD value
            signal_value: Current signal line value
            histogram: Current MACD histogram (optional for legacy compatibility)
            fast: Fast EMA period (for threshold lookup)
            slow: Slow EMA period (for threshold lookup)
            signal_period: Signal line period (for threshold lookup)
            histogram_data: List of recent histogram values for std calculation (optional)
        
        Returns:
            Dict with 'signal', 'strength', and 'description' keys
        """
        from src.config.signal_thresholds import get_macd_thresholds_by_parameters
        
        # Get thresholds for this MACD parameter set
        thresholds = get_macd_thresholds_by_parameters(fast, slow, signal_period)
        
        if thresholds is None:
            # Fallback for unknown parameter combinations
            logger.warning(f"⚠️ No thresholds found for MACD({fast},{slow},{signal_period}), using simple crossover")
            if macd_value > signal_value:
                return {'signal': 'Buy', 'strength': 'Moderate', 'description': 'MACD above signal line (no magnitude filter available)'}
            elif macd_value < signal_value:
                return {'signal': 'Sell', 'strength': 'Moderate', 'description': 'MACD below signal line (no magnitude filter available)'}
            else:
                return {'signal': 'Neutral', 'strength': 'Weak', 'description': 'MACD at signal line'}
        
        magnitude_multiplier = thresholds.get('magnitude_multiplier', 0.5)
        std_lookback = thresholds.get('histogram_std_lookback', 20)
        
        # Calculate histogram magnitude threshold
        histogram_magnitude = abs(macd_value - signal_value)
        
        if histogram_data is not None and len(histogram_data) >= std_lookback:
            # Use provided histogram data to calculate std
            import numpy as np
            histogram_std = np.std(histogram_data[-std_lookback:])
            magnitude_threshold = magnitude_multiplier * histogram_std
        else:
            # Fallback: use simple magnitude if no histogram data provided
            # This preserves legacy behavior for backward compatibility
            magnitude_threshold = magnitude_multiplier * 0.01  # Small default threshold
            logger.debug(f"Using fallback magnitude threshold for MACD({fast},{slow},{signal_period})")
        
        # Generate signal based on crossover AND magnitude
        if macd_value > signal_value and histogram_magnitude >= magnitude_threshold:
            return {
                'signal': 'Buy',
                'strength': 'Strong' if histogram_magnitude >= magnitude_threshold * 1.5 else 'Moderate',
                'description': f'MACD above signal (magnitude: {histogram_magnitude:.6f})'
            }
        elif macd_value < signal_value and histogram_magnitude >= magnitude_threshold:
            return {
                'signal': 'Sell',
                'strength': 'Strong' if histogram_magnitude >= magnitude_threshold * 1.5 else 'Moderate',
                'description': f'MACD below signal (magnitude: {histogram_magnitude:.6f})'
            }
        else:
            return {
                'signal': 'Neutral',
                'strength': 'Weak',
                'description': f'MACD signal not strong enough (magnitude: {histogram_magnitude:.6f}, threshold: {magnitude_threshold:.6f})'
            }
    
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
            
            rolling_signals: Dict[str, Any] = {
                "status": "not_implemented",
                "message": "Rolling signal heatmap - Phase 5 (future)",
            }

            try:
                df_ind = self.calculate_optionc_indicators(ticker=ticker, save_to_db=save_to_db)
                if df_ind is not None and not df_ind.empty:
                    scores = self.calculate_rule_engine_signals_optionc(
                        ticker=ticker,
                        feature_scope="heatmap",
                        save_to_db=save_to_db,
                    )
                    if scores:
                        rolling_signals = self._build_optionc_rolling_signals(
                            ticker=ticker,
                            df_ind=df_ind,
                            scores=scores,
                            days=10,
                        )
            except Exception as e:
                logger.error(f"Error building rolling signals for {ticker}: {e}")
                rolling_signals = {"status": "error", "message": str(e)}
                            
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
                
                # Phase 3: 52-Week High Analysis    
                'price_extremes': self.calculate_52_week_analysis(ticker),           
                                                
                # Phase 4: Pivot Points (placeholder for now)
                'pivot_points': self.calculate_pivot_points(
                    ticker=ticker,
                    target_date=None,
                    save_to_db=save_to_db,
                    ),

                # Phase 5: Rolling Signals 
                'rolling_signals': rolling_signals
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
    
    # ===== PIVOT POINTS ANALYSIS METHODS =====
    
    def _get_pivot_ohlc(self, ticker: str, target_date: date) -> Optional[Dict]:
        """
        Get High, Low, Close, Open for pivot calculations (database-first approach)
        
        Args:
            ticker: Stock ticker symbol
            target_date: Date to fetch OHLC data for
            
        Returns:
            Dict with OHLC values or None if data unavailable
        """
        try:
            # Try database first
            conn = self._get_database_connection()
            if conn:
                query = f"""
                SELECT Open, High, Low, Close
                FROM {self.daily_prices_table}
                WHERE Ticker = ? AND Date = ?
                """
                
                date_str = target_date.strftime('%Y-%m-%d')
                cursor = conn.cursor()
                cursor.execute(query, (ticker, date_str))
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    logger.info(f"✅ Found OHLC data in database for {ticker} on {date_str}")
                    return {
                        'open': result[0],
                        'high': result[1],
                        'low': result[2],
                        'close': result[3],
                        'date': target_date
                    }
            
            # Fallback to yfinance if not in database
            logger.info(f"📡 Fetching OHLC from yfinance for {ticker} on {target_date}")
            
            # Get data with buffer to ensure we have the target date
            start_date = target_date - timedelta(days=5)
            end_date = target_date + timedelta(days=1)
            
            hist_data = self._fetch_ohlcv_data_from_yfinance(ticker, start_date, end_date, save_to_db=True)
            
            if hist_data is not None and not hist_data.empty:
                # Find the exact date
                target_datetime = pd.Timestamp(target_date)
                if target_datetime in hist_data.index:
                    row = hist_data.loc[target_datetime]
                    return {
                        'open': row['Open'],
                        'high': row['High'],
                        'low': row['Low'],
                        'close': row['Close'],
                        'date': target_date
                    }
            
            logger.warning(f"⚠️ No OHLC data found for {ticker} on {target_date}")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching OHLC for {ticker} on {target_date}: {e}")
            return None
    
    def _calculate_classic_pivot(self, high: float, low: float, close: float) -> Dict:
        """
        Calculate Classic Pivot Points
        
        Formula:
            PP = (H + L + C) / 3
            R1 = 2*PP - L
            R2 = PP + (H - L)
            R3 = H + 2*(PP - L)
            S1 = 2*PP - H
            S2 = PP - (H - L)
            S3 = L - 2*(H - PP)
        
        Args:
            high: High price
            low: Low price
            close: Close price
            
        Returns:
            Dict with pivot point and resistance/support levels
        """
        try:
            # Calculate pivot point
            pp = (high + low + close) / 3
            
            # Calculate resistance levels
            r1 = 2 * pp - low
            r2 = pp + (high - low)
            r3 = high + 2 * (pp - low)
            
            # Calculate support levels
            s1 = 2 * pp - high
            s2 = pp - (high - low)
            s3 = low - 2 * (high - pp)
            
            return {
                'pivot': pp,
                'r1': r1,
                'r2': r2,
                'r3': r3,
                's1': s1,
                's2': s2,
                's3': s3
            }
            
        except Exception as e:
            logger.error(f"Error calculating classic pivot: {e}")
            return None
    
    def _calculate_fibonacci_pivot(self, high: float, low: float, close: float) -> Dict:
        """
        Calculate Fibonacci Pivot Points
        
        Formula:
            PP = (H + L + C) / 3
            R1 = PP + 0.382 * (H - L)
            R2 = PP + 0.618 * (H - L)
            R3 = PP + 1.000 * (H - L)
            S1 = PP - 0.382 * (H - L)
            S2 = PP - 0.618 * (H - L)
            S3 = PP - 1.000 * (H - L)
        
        Args:
            high: High price
            low: Low price
            close: Close price
            
        Returns:
            Dict with pivot point and resistance/support levels
        """
        try:
            # Calculate pivot point
            pp = (high + low + close) / 3
            
            # Calculate range
            range_hl = high - low
            
            # Calculate resistance levels using Fibonacci ratios
            r1 = pp + 0.382 * range_hl
            r2 = pp + 0.618 * range_hl
            r3 = pp + 1.000 * range_hl
            
            # Calculate support levels using Fibonacci ratios
            s1 = pp - 0.382 * range_hl
            s2 = pp - 0.618 * range_hl
            s3 = pp - 1.000 * range_hl
            
            return {
                'pivot': pp,
                'r1': r1,
                'r2': r2,
                'r3': r3,
                's1': s1,
                's2': s2,
                's3': s3
            }
            
        except Exception as e:
            logger.error(f"Error calculating fibonacci pivot: {e}")
            return None
    
    def _calculate_camarilla_pivot(self, high: float, low: float, close: float) -> Dict:
        """
        Calculate Camarilla Pivot Points
        
        Formula:
            PP = (H + L + C) / 3
            R1 = C + (H - L) * 1.1/12
            R2 = C + (H - L) * 1.1/6
            R3 = C + (H - L) * 1.1/4
            S1 = C - (H - L) * 1.1/12
            S2 = C - (H - L) * 1.1/6
            S3 = C - (H - L) * 1.1/4
        
        Args:
            high: High price
            low: Low price
            close: Close price
            
        Returns:
            Dict with pivot point and resistance/support levels
        """
        try:
            # Calculate pivot point (same as Classic)
            pp = (high + low + close) / 3
            
            # Calculate range
            range_hl = high - low
            
            # Calculate resistance levels using Camarilla multipliers
            r1 = close + range_hl * 1.1/12
            r2 = close + range_hl * 1.1/6
            r3 = close + range_hl * 1.1/4
            
            # Calculate support levels using Camarilla multipliers
            s1 = close - range_hl * 1.1/12
            s2 = close - range_hl * 1.1/6
            s3 = close - range_hl * 1.1/4
            
            return {
                'pivot': pp,
                'r1': r1,
                'r2': r2,
                'r3': r3,
                's1': s1,
                's2': s2,
                's3': s3
            }
            
        except Exception as e:
            logger.error(f"Error calculating camarilla pivot: {e}")
            return None
    
    def _calculate_woodys_pivot(self, high: float, low: float, close: float, open_price: float) -> Dict:
        """
        Calculate Woody's Pivot Points
        
        Formula:
            PP = (H + L + 2*C) / 4
            R1 = 2*PP - L
            R2 = PP + (H - L)
            R3 = H + 2*(PP - L)
            S1 = 2*PP - H
            S2 = PP - (H - L)
            S3 = L - 2*(H - PP)
        
        Args:
            high: High price
            low: Low price
            close: Close price
            open_price: Open price (used in Woody's calculation)
            
        Returns:
            Dict with pivot point and resistance/support levels
        """
        try:
            # Calculate pivot point (Woody's formula weights close more heavily)
            pp = (high + low + 2 * close) / 4
            
            # Calculate resistance levels (same as Classic but using Woody's PP)
            r1 = 2 * pp - low
            r2 = pp + (high - low)
            r3 = high + 2 * (pp - low)
            
            # Calculate support levels (same as Classic but using Woody's PP)
            s1 = 2 * pp - high
            s2 = pp - (high - low)
            s3 = low - 2 * (high - pp)
            
            return {
                'pivot': pp,
                'r1': r1,
                'r2': r2,
                'r3': r3,
                's1': s1,
                's2': s2,
                's3': s3
            }
            
        except Exception as e:
            logger.error(f"Error calculating woody's pivot: {e}")
            return None
    
    def _get_pivot_points_from_db(self, ticker: str, target_date: date) -> Optional[Dict]:
        """
        Fetch cached pivot points from database
        
        Args:
            ticker: Stock ticker symbol
            target_date: Date for pivot points
            
        Returns:
            Dict with all 4 pivot types or None if not cached
        """
        try:
            conn = self._get_database_connection()
            if not conn:
                return None
            
            query = f"""
            SELECT pivot_type, pivot, r1, r2, r3, s1, s2, s3
            FROM {self.pivot_table}
            WHERE ticker = ? AND date = ?
            """
            
            date_str = target_date.strftime('%Y-%m-%d')
            cursor = conn.cursor()
            cursor.execute(query, (ticker, date_str))
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                return None
            
            # Organize by pivot type
            pivots = {}
            for row in results:
                pivot_type = row[0]
                pivots[pivot_type] = {
                    'pivot': row[1],
                    'r1': row[2],
                    'r2': row[3],
                    'r3': row[4],
                    's1': row[5],
                    's2': row[6],
                    's3': row[7]
                }
            
            logger.info(f"✅ Found cached pivot points for {ticker} on {date_str}")
            return pivots
            
        except Exception as e:
            logger.error(f"Error fetching pivot points from database: {e}")
            return None
    
    def _save_pivot_points_to_db(self, ticker: str, calc_date: date, pivots_data: Dict) -> bool:
        """
        Save all pivot types to pivot_points_daily table
        
        Args:
            ticker: Stock ticker symbol
            calc_date: Date the pivots were calculated for
            pivots_data: Dict with all pivot types and their levels
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            conn = self._get_database_connection()
            if not conn:
                logger.warning("Database not available for saving pivot points")
                return False
            
            date_str = calc_date.strftime('%Y-%m-%d')
            cursor = conn.cursor()
            
            # Save each pivot type
            for pivot_type, levels in pivots_data.items():
                query = f"""
                INSERT OR REPLACE INTO {self.pivot_table}
                (ticker, date, pivot_type, pivot, r1, r2, r3, s1, s2, s3)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                
                cursor.execute(query, (
                    ticker,
                    date_str,
                    pivot_type,
                    levels['pivot'],
                    levels['r1'],
                    levels['r2'],
                    levels['r3'],
                    levels['s1'],
                    levels['s2'],
                    levels['s3']
                ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Saved {len(pivots_data)} pivot types to database for {ticker} on {date_str}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving pivot points to database: {e}")
            return False
    
    def calculate_pivot_points(self, ticker: str, target_date: Optional[date] = None, 
                               save_to_db: bool = True) -> Dict:
        """
        Calculate all 4 pivot point types for a ticker
        
        Uses previous trading day's OHLC by default. Implements database-first pattern:
        1. Check database for cached pivots
        2. If missing, fetch OHLC data (database -> yfinance fallback)
        3. Calculate all pivot types
        4. Save to database if enabled
        
        Args:
            ticker: Stock ticker symbol
            target_date: Date for pivot calculation (default: yesterday's trading day)
            save_to_db: Whether to save calculated pivots to database
            
        Returns:
            Dict with all 4 pivot types and calculation metadata:
            {
                'ticker': str,
                'calculation_date': str,
                'ohlc_date': str,
                'classic': {...},
                'fibonacci': {...},
                'camarilla': {...},
                'woodys': {...},
                'error': bool
            }
        """
        logger.info(f"📍 Calculating pivot points for {ticker}")
        
        try:
            # Determine target date (previous trading day if not specified)
            if target_date is None:
                from .performance import get_last_completed_trading_day
                last_trading_day = get_last_completed_trading_day()
                
                # Use previous trading day (pivots calculated from yesterday's OHLC)
                target_date = last_trading_day - timedelta(days=1)
                
                # Ensure it's a trading day
                from .performance import is_us_trading_day
                while not is_us_trading_day(target_date):
                    target_date -= timedelta(days=1)
                
                logger.info(f"Using previous trading day: {target_date}")
            
            # Check database cache first
            cached_pivots = self._get_pivot_points_from_db(ticker, target_date)
            if cached_pivots:
                logger.info(f"✅ Using cached pivot points for {ticker}")
                return {
                    'ticker': ticker,
                    'calculation_date': datetime.now().strftime('%Y-%m-%d'),
                    'ohlc_date': target_date.strftime('%Y-%m-%d'),
                    'classic': cached_pivots.get('classic'),
                    'fibonacci': cached_pivots.get('fibonacci'),
                    'camarilla': cached_pivots.get('camarilla'),
                    'woodys': cached_pivots.get('woodys'),
                    'error': False,
                    'source': 'database_cache'
                }
            
            # Fetch OHLC data for target date
            ohlc_data = self._get_pivot_ohlc(ticker, target_date)
            
            if not ohlc_data:
                return {
                    'ticker': ticker,
                    'error': True,
                    'message': f'Unable to fetch OHLC data for {ticker} on {target_date}'
                }
            
            # Calculate all pivot types
            pivots_data = {}
            
            # Classic Pivot
            classic = self._calculate_classic_pivot(
                ohlc_data['high'], 
                ohlc_data['low'], 
                ohlc_data['close']
            )
            if classic:
                pivots_data['classic'] = classic
            
            # Fibonacci Pivot
            fibonacci = self._calculate_fibonacci_pivot(
                ohlc_data['high'],
                ohlc_data['low'],
                ohlc_data['close']
            )
            if fibonacci:
                pivots_data['fibonacci'] = fibonacci
            
            # Camarilla Pivot
            camarilla = self._calculate_camarilla_pivot(
                ohlc_data['high'],
                ohlc_data['low'],
                ohlc_data['close']
            )
            if camarilla:
                pivots_data['camarilla'] = camarilla
            
            # Woody's Pivot
            woodys = self._calculate_woodys_pivot(
                ohlc_data['high'],
                ohlc_data['low'],
                ohlc_data['close'],
                ohlc_data['open']
            )
            if woodys:
                pivots_data['woodys'] = woodys
            
            # Save to database if enabled
            if save_to_db and pivots_data:
                self._save_pivot_points_to_db(ticker, target_date, pivots_data)
            
            logger.info(f"✅ Calculated {len(pivots_data)} pivot types for {ticker}")
            
            return {
                'ticker': ticker,
                'calculation_date': datetime.now().strftime('%Y-%m-%d'),
                'ohlc_date': target_date.strftime('%Y-%m-%d'),
                'classic': pivots_data.get('classic'),
                'fibonacci': pivots_data.get('fibonacci'),
                'camarilla': pivots_data.get('camarilla'),
                'woodys': pivots_data.get('woodys'),
                'error': False,
                'source': 'calculated'
            }
            
        except Exception as e:
            logger.error(f"Error calculating pivot points for {ticker}: {e}")
            return {
                'ticker': ticker,
                'error': True,
                'message': str(e)
            }


# Factory function for backward compatibility
def get_technical_calculator() -> DatabaseIntegratedTechnicalCalculator:
    """Factory function to get a database-integrated technical analysis calculator instance"""
    return DatabaseIntegratedTechnicalCalculator()


# Convenience function for single ticker analysis
def calculate_technical_analysis(ticker: str, save_to_db: bool = False) -> Dict:
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
