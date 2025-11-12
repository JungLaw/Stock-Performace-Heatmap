"""
Signal Logic Thresholds Configuration

Complete threshold definitions for all technical indicators across 3 timeframes.
- Existing indicators: extracted from current code (technical.py lines 436-569)
- Missing indicators: industry-standard thresholds

Source: Technical analysis best practices, TradingView standards, and industry conventions
"""

SIGNAL_THRESHOLDS = {
    # ============================================================================
    # MOMENTUM INDICATORS (Oscillators)
    # ============================================================================
    "momentum": {
        # ========================================================================
        # RSI (Relative Strength Index)
        # Industry standard: 70/30 overbought/oversold, 50 midpoint
        # Customized per timeframe sensitivity
        # ========================================================================
        "rsi": {
            "10": {  # SHORT-TERM: More sensitive (tighter bands)
                "strong_buy_max": 15,
                "buy_max": 30,
                "neutral_low": 30,
                "neutral_high": 70,
                "sell_min": 70,
                "strong_sell_min": 85,
                "description": "Short-term RSI - faster oscillation, tighter bands"
            },
            "14": {  # INTERMEDIATE-TERM: Standard (classic thresholds)
                "strong_buy_max": 20,
                "buy_max": 30,        # 35
                "neutral_low": 30,     # 35
                "neutral_high": 80,    # 70
                "sell_min": 80,        # 70
                "strong_sell_min": 90,  #80
                "description": "Standard RSI(14) - industry default"
            },
            "21": {  # LONG-TERM: Less sensitive (wider bands)
                "strong_buy_max": 25,
                "buy_max": 40,
                "neutral_low": 40,
                "neutral_high": 65,
                "sell_min": 65,
                "strong_sell_min": 75,
                "description": "Long-term RSI - smoother, filters noise"
            }   # "30" originally    
        },

        # ========================================================================
        # STOCHASTIC OSCILLATOR (%K and %D)
        # Industry standard: 80/20 overbought/oversold
        # Interpretation: K above/below D, K above/below 50 midline
        # ========================================================================
        "stochastic": {
            "5": {  # SHORT-TERM: Stoch(5,3,3)
                "overbought_level": 80,
                "oversold_level": 20,
                "midpoint": 50,
                "strong_overbought": 85,
                "strong_oversold": 15,
                "description": "Short-term Stochastic - rapid crosses, high sensitivity"
            },
            "14": {  # INTERMEDIATE-TERM: Stoch(14,3,3)
                "overbought_level": 80,
                "oversold_level": 20,
                "midpoint": 50,
                "strong_overbought": 85,
                "strong_oversold": 15,
                "description": "Standard Stochastic(14,3,3) - industry default"
            },
            "21": {  # LONG-TERM: Stoch(21,5,5)
                "overbought_level": 80,
                "oversold_level": 20,
                "midpoint": 50,
                "strong_overbought": 85,
                "strong_oversold": 15,
                "description": "Long-term Stochastic - smoothed, less whipsaw"
            }
        },

        # ========================================================================
        # CCI (Commodity Channel Index)
        # Industry standard: ±100 strong signal levels, ±200 extreme levels
        # 0 is neutral midpoint
        # ========================================================================
        "cci": {
            "10": {  # SHORT-TERM: CCI(10)
                "strong_buy_min": 100,
                "buy_min": 0,
                "neutral_low": 0,
                "neutral_high": 0,
                "sell_max": 0,
                "strong_sell_max": -100,
                "extreme_buy_min": 200,
                "extreme_sell_max": -200,
                "description": "Short-term CCI - rapid mean reversion signals"
            },
            "14": {  # INTERMEDIATE-TERM: CCI(14)
                "strong_buy_min": 100,
                "buy_min": 0,
                "neutral_low": -100,
                "neutral_high": 100,
                "sell_max": 0,
                "strong_sell_max": -100,
                "extreme_buy_min": 200,
                "extreme_sell_max": -200,
                "description": "Standard CCI(14) - classic thresholds"
            },
            "20": {  # LONG-TERM: CCI(30)
                "strong_buy_min": 100,
                "buy_min": 50,
                "neutral_low": -50,
                "neutral_high": 50,
                "sell_max": -50,
                "strong_sell_max": -100,
                "extreme_buy_min": 200,
                "extreme_sell_max": -200,
                "description": "Long-term CCI - wider bands, structural trends"
            }
        },

        # ========================================================================
        # ROC (Rate of Change)
        # Industry standard: Positive = bullish, negative = bearish
        # ±5% marks strong signals
        # ========================================================================
        "roc": {
            "9": {  # SHORT-TERM: ROC(9)
                "strong_buy_min": 5,
                "buy_min": 0,
                "neutral_low": 0,
                "neutral_high": 0,
                "sell_max": 0,
                "strong_sell_max": -5,
                "description": "Short-term ROC - quick momentum changes"
            },
            "12": {  # INTERMEDIATE-TERM: ROC(12)
                "strong_buy_min": 5,
                "buy_min": 0,
                "neutral_low": 0,
                "neutral_high": 0,
                "sell_max": 0,
                "strong_sell_max": -5,
                "description": "Standard ROC(12) - classic momentum measure"
            },
            "20": {  # INTERMEDIATE-TERM: ROC(20)
                "strong_buy_min": 5,
                "buy_min": 1,
                "neutral_low": 0,
                "neutral_high": 0,
                "sell_max": -1,
                "strong_sell_max": -5,
                "description": "Intermediate ROC(20) - smoother momentum"
            },
            "50": {  # LONG-TERM: ROC(50)
                "strong_buy_min": 5,
                "buy_min": 2,
                "neutral_low": -2,
                "neutral_high": 2,
                "sell_max": -2,
                "strong_sell_max": -5,
                "description": "Long-term ROC(50) - structural momentum"
            }
        },

        # ========================================================================
        # WILLIAMS %R (Williams Percent Range)
        # Industry standard: -20 to 0 overbought, -80 to -100 oversold
        # Range: -100 to 0
        # ========================================================================
        "williams_r": {
            "5": {  # SHORT-TERM: Williams %R(5)
                "overbought_max": -20,
                "strong_overbought_max": -10,
                "neutral_low": -50,
                "neutral_high": -50,
                "oversold_min": -80,
                "strong_oversold_min": -90,
                "description": "Short-term Williams %R - rapid reversals"
            },
            "14": {  # INTERMEDIATE-TERM: Williams %R(14)
                "overbought_max": -20,
                "strong_overbought_max": -10,
                "neutral_low": -50,
                "neutral_high": -50,
                "oversold_min": -80,
                "strong_oversold_min": -90,
                "description": "Standard Williams %R(14) - classic thresholds"
            },
            "20": {  # LONG-TERM: Williams %R(20)
                "overbought_max": -15,
                "strong_overbought_max": -5,
                "neutral_low": -50,
                "neutral_high": -50,
                "oversold_min": -85,
                "strong_oversold_min": -95,
                "description": "Long-term Williams %R - structural reversals"
            }
        },

        # ========================================================================
        # ULTIMATE OSCILLATOR
        # Industry standard: 70 overbought, 30 oversold, 50 midpoint
        # Combines 3 timeframes for trend confirmation
        # ========================================================================
        "ultimate_oscillator": {
            "5_10_20": {  # SHORT-TERM: UO(5,10,20)
                "overbought": 70,
                "oversold": 30,
                "midpoint": 50,
                "strong_overbought": 75,
                "strong_oversold": 25,
                "description": "Short-term Ultimate Osc - multi-timeframe momentum"
            },
            "7_14_28": {  # INTERMEDIATE-TERM: UO(7,14,28)
                "overbought": 70,
                "oversold": 30,
                "midpoint": 50,
                "strong_overbought": 75,
                "strong_oversold": 25,
                "description": "Standard Ultimate Osc(7,14,28) - industry default"
            },
            "10_20_40": {  # LONG-TERM: UO(10,20,40)
                "overbought": 70,
                "oversold": 30,
                "midpoint": 50,
                "strong_overbought": 75,
                "strong_oversold": 25,
                "description": "Long-term Ultimate Osc - longer period smoothing"
            }
        },

        # ========================================================================
        # MFI (Money Flow Index) - MISSING INDICATOR
        # Industry standard: 80/20 overbought/oversold (similar to RSI but with volume)
        # Interpretation: Price momentum weighted by volume
        # ========================================================================
        "mfi": {
            "10": {  # SHORT-TERM: MFI(10)
                "strong_buy_max": 15,
                "buy_max": 30,
                "neutral_low": 30,
                "neutral_high": 70,
                "sell_min": 70,
                "strong_sell_min": 85,
                "description": "Short-term MFI - volume-weighted momentum, high sensitivity"
            },
            "14": {  # INTERMEDIATE-TERM: MFI(14)
                "strong_buy_max": 20,
                "buy_max": 30,      #35
                "neutral_low": 30,   # 35
                "neutral_high": 70,
                "sell_min": 70,
                "strong_sell_min": 80,
                "description": "Standard MFI(14) - industry default, volume-weighted RSI"
            },
            "30": {  # LONG-TERM: MFI(30)
                "strong_buy_max": 25,
                "buy_max": 40,
                "neutral_low": 40,
                "neutral_high": 65,
                "sell_min": 65,
                "strong_sell_min": 75,
                "description": "Long-term MFI(30) - volume trends over longer period"
            }
        },
    },

    # ============================================================================
    # TREND INDICATORS
    # ============================================================================
    "trend": {
        # ========================================================================
        # ADX (Average Directional Index)
        # Industry standard: <25 weak trend, 25-50 strong trend, >50 very strong
        # Directional interpretation via +DI and -DI
        # ========================================================================
        "adx": {
            "9": {  # SHORT-TERM: ADX(9)
                "weak_max": 20,
                "strong_min": 35,
                "very_strong_min": 50,
                "description": "Short-term ADX - rapid trend confirmation"
            },
            "14": {  # INTERMEDIATE-TERM: ADX(14)
                "weak_max": 25,
                "strong_min": 50,
                "very_strong_min": 60,
                "description": "Standard ADX(14) - industry default"
            },
            "20": {  # LONG-TERM: ADX(20)
                "weak_max": 30,
                "strong_min": 50,
                "very_strong_min": 65,
                "description": "Long-term ADX - sustained trend identification"
            }
        },

        # ========================================================================
        # MACD (Moving Average Convergence Divergence)
        # Industry standard: Signal line crossover (MACD > Signal = buy)
        # Also: Histogram shows distance between MACD and signal line
        # ========================================================================
        "macd": {
            "8_17_5": {  # SHORT-TERM: MACD(8,17,5)
                "signal_crossover_threshold": 0,
                "histogram_positive": "bullish_bias",
                "histogram_negative": "bearish_bias",
                "description": "Short-term MACD - fast momentum tracking"
            },
            "12_26_9": {  # INTERMEDIATE-TERM: MACD(12,26,9)
                "signal_crossover_threshold": 0,
                "histogram_positive": "bullish_bias",
                "histogram_negative": "bearish_bias",
                "description": "Standard MACD(12,26,9) - industry default"
            },
            "20_50_10": {  # LONG-TERM: MACD(20,50,10)
                "signal_crossover_threshold": 0,
                "histogram_positive": "bullish_bias",
                "histogram_negative": "bearish_bias",
                "description": "Long-term MACD - macro trend confirmation"
            }
        },

        # ========================================================================
        # MOVING AVERAGES (SMA/EMA)
        # Industry standard: ±0.025% for tight trades, ±1% for wider
        # Interpretation: Price above MA = uptrend, below = downtrend
        # ========================================================================
        "moving_average": {
            "all": {
                "neutral_zone_pct": 0.025,
                "tight_trade_pct": 0.025,
                "swing_trade_pct": 0.5,
                "position_trade_pct": 1.0,
                "description": "Price deviation from MA - universal threshold"
            }
        },

        # ========================================================================
        # ELDER RAY INDEX (Bull Power & Bear Power)
        # Industry standard: Both positive = strong buy, both negative = strong sell
        # Derived from: EMA(13) - High/Low
        # ========================================================================
        "elder_ray": {
            "10": {
                "interpretation": "bullish_when_both_positive",
                "description": "Short-term Elder Ray - rapid power shifts"
            },
            "13": {
                "interpretation": "bullish_when_both_positive",
                "description": "Standard Elder Ray(13) - industry default"
            },
            "21": {
                "interpretation": "bullish_when_both_positive",
                "description": "Long-term Elder Ray - sustained power balance"
            }
        },

        # ========================================================================
        # HMA (Hull Moving Average) - MISSING INDICATOR
        # Industry standard: Same as regular MA - trend indicator
        # Combines WMA(n/2) and WMA(n) for faster response
        # ========================================================================
        "hull_moving_average": {
            "9": {
                "neutral_zone_pct": 0.025,
                "interpretation": "price_above_hma_bullish",
                "description": "Short-term HMA - more responsive than SMA/EMA"
            },
            "21": {
                "neutral_zone_pct": 0.025,
                "interpretation": "price_above_hma_bullish",
                "description": "Intermediate HMA - swing trend following"
            },
            "50": {
                "neutral_zone_pct": 0.025,
                "interpretation": "price_above_hma_bullish",
                "description": "Long-term HMA - structural trend identification"
            }
        },
    },

    # ============================================================================
    # VOLATILITY INDICATORS
    # ============================================================================
    "volatility": {
        # ========================================================================
        # ATR (Average True Range)
        # Industry standard: Volatility measure only - NO directional signal
        # Used for: Position sizing, support/resistance bands, breakout thresholds
        # ========================================================================
        "atr": {
            "10": {
                "signal": "N/A",
                "interpretation": "volatility_measure_only",
                "description": "Short-term ATR - rapid volatility changes"
            },
            "14": {
                "signal": "N/A",
                "interpretation": "volatility_measure_only",
                "description": "Standard ATR(14) - industry default volatility"
            },
            "20": {
                "signal": "N/A",
                "interpretation": "volatility_measure_only",
                "description": "Long-term ATR - structural volatility regime"
            }   # 50 previously
        },

        # ========================================================================
        # BOLLINGER BANDS - MISSING INDICATOR
        # Industry standard: Price > Upper = overbought, Price < Lower = oversold
        # Also: Band squeeze = low volatility (breakout coming), Band expansion = breakout
        # ========================================================================
        "bollinger_bands": {
            "10_1_5": {  # SHORT-TERM: BB(10,1.5)
                "upper_band": "overbought_signal",
                "middle_band": "sma_10",
                "lower_band": "oversold_signal",
                "squeeze_threshold": 0.5,
                "description": "Short-term BB - tight bands, quick reversals"
            },
            "20_2": {  # INTERMEDIATE-TERM: BB(20,2)
                "upper_band": "overbought_signal",
                "middle_band": "sma_20",
                "lower_band": "oversold_signal",
                "squeeze_threshold": 1.0,
                "description": "Standard BB(20,2) - industry default"
            },
            "50_2_5": {  # LONG-TERM: BB(50,2.5)
                "upper_band": "overbought_signal",
                "middle_band": "sma_50",
                "lower_band": "oversold_signal",
                "squeeze_threshold": 1.5,
                "description": "Long-term BB - wide bands, structural levels"
            }
        },
    },

    # ============================================================================
    # VOLUME INDICATORS
    # ============================================================================
    "volume": {
        # ========================================================================
        # CMF (Chaikin Money Flow) - MISSING INDICATOR
        # Industry standard: >0 buying pressure, <0 selling pressure
        # Range: -1 to +1 or sometimes -0.5 to +0.5
        # ========================================================================
        "cmf": {
            "10": {  # SHORT-TERM: CMF(10)
                "strong_buying_min": 0.1,
                "mild_buying_min": 0,
                "mild_selling_max": 0,
                "strong_selling_max": -0.1,
                "description": "Short-term CMF - rapid money flow shifts"
            },
            "21": {  # INTERMEDIATE-TERM: CMF(21)
                "strong_buying_min": 0.05,
                "mild_buying_min": 0,
                "mild_selling_max": 0,
                "strong_selling_max": -0.05,
                "description": "Standard CMF(21) - money flow confirmation"
            },
            "50": {  # LONG-TERM: CMF(50)
                "strong_buying_min": 0.05,
                "mild_buying_min": 0,
                "mild_selling_max": 0,
                "strong_selling_max": -0.05,
                "description": "Long-term CMF(50) - sustained accumulation/distribution"
            }
        },

        # ========================================================================
        # VWMA (Volume Weighted Moving Average) - MISSING INDICATOR
        # Industry standard: Same as regular MA - trend indicator
        # Volume weighting emphasizes higher-volume bars
        # ========================================================================
        "vwma": {
            "10": {
                "neutral_zone_pct": 0.025,
                "interpretation": "price_above_vwma_bullish",
                "description": "Short-term VWMA - volume-weighted trend"
            },
            "20": {
                "neutral_zone_pct": 0.025,
                "interpretation": "price_above_vwma_bullish",
                "description": "Intermediate VWMA - volume-confirmed trends"
            },
            "50": {
                "neutral_zone_pct": 0.025,
                "interpretation": "price_above_vwma_bullish",
                "description": "Long-term VWMA - structural volume trends"
            }
        },
    }
}

# ============================================================================
# METADATA & NOTES
# ============================================================================

THRESHOLD_SOURCES = {
    "existing_indicators": [
        "RSI - Extracted from technical.py lines 436-447",
        "Stochastic - Extracted from technical.py lines 513-525",
        "CCI - Extracted from technical.py lines 537-547",
        "ROC - Extracted from technical.py lines 559-569",
        "Williams %R - Extracted from technical.py lines 526-536",
        "Ultimate Osc - Extracted from technical.py lines 548-558",
        "MACD - Extracted from technical.py lines 491-499",
        "ADX - Extracted from technical.py lines 460-490",
        "Moving Average - Extracted from technical.py lines 449-459",
        "Elder Ray - Extracted from technical.py lines 500-512",
        "ATR - Extracted from technical.py lines 379-383"
    ],
    "missing_indicators_source": [
        "MFI - Industry standard from TradingView, Investopedia, TA-Lib defaults",
        "CMF - Industry standard from Thinkorswim, TradingView conventions",
        "VWMA - Trend interpretation follows MA convention",
        "HMA - Trend interpretation follows MA convention",
        "Bollinger Bands - Industry standard from John Bollinger, TradingView standards"
    ]
}

# ============================================================================
# INTERPRETATION GUIDE
# ============================================================================

SIGNAL_INTERPRETATION = {
    "oscillator_signals": {
        "Strong Buy": {"value_range": "extreme_low", "action": "aggressive_buy", "risk": "high"},
        "Buy": {"value_range": "oversold", "action": "moderate_buy", "risk": "medium"},
        "Neutral": {"value_range": "neutral_zone", "action": "hold_or_watch", "risk": "low"},
        "Sell": {"value_range": "overbought", "action": "moderate_sell", "risk": "medium"},
        "Strong Sell": {"value_range": "extreme_high", "action": "aggressive_sell", "risk": "high"},
    },
    "trend_signals": {
        "Buy": {"interpretation": "above_MA_or_strong_uptrend", "action": "follow_trend", "risk": "medium"},
        "Neutral": {"interpretation": "consolidating_or_weak_trend", "action": "hold_wait", "risk": "medium"},
        "Sell": {"interpretation": "below_MA_or_strong_downtrend", "action": "follow_trend", "risk": "medium"},
    },
    "volatility_signals": {
        "N/A": {"interpretation": "measure_only", "action": "use_for_risk_management", "risk": "N/A"},
    }
}
