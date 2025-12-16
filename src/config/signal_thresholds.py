"""
Signal Thresholds Configuration
Centralized threshold definitions for all technical indicators.
All thresholds are uniform across timeframes - only indicator parameters vary.
Last Updated: November 11, 2025
"""

SIGNAL_THRESHOLDS = {
    'oscillators': {
        'rsi': {
            'description': 'Relative Strength Index - Momentum oscillator measuring overbought/oversold',
            'scale': '0-100',
            'thresholds': {
                'strong_sell': 80,      # >= 80: Extremely overbought
                'sell': 70,             # >= 70: Overbought
                'neutral_upper': 35,    # 35-70: Neutral zone (neither overbought nor oversold)
                'neutral_lower': 20,    # 20-35: Neutral zone
                'buy': 20,              # <= 20: Oversold
                'strong_buy': None,     # < 20: Extremely oversold (implicit)
            },
            'parameters': {
                'short_term': 10,
                'intermediate_term': 14,
                'long_term': [21, 30],  # Both used in rolling heatmap
            },
            'signal_logic': {
                'strong_sell': 'rsi_value >= 80',
                'sell': 'rsi_value >= 70',
                'neutral': '35 <= rsi_value < 70',
                'buy': '20 <= rsi_value < 35',
                'strong_buy': 'rsi_value < 20',
            }
        },
        
        'stochastic': {
            'description': 'Stochastic Oscillator - Momentum indicator comparing closing price to price range',
            'scale': '0-100',
            'thresholds': {
                'overbought': 80,       # K and D both >= 80: Overbought
                'oversold': 20,         # K and D both <= 20: Oversold
                'crossover_buy': None,  # K > D with both < 80: Bullish crossover
                'crossover_sell': None, # K < D with both > 20: Bearish crossover
            },
            'parameters': {
                'short_term': (5, 3, 3),      # (k_period, k_slowing, d_slowing)
                'intermediate_term': (14, 3, 3),
                'long_term': (21, 5, 5),
            },
            'signal_logic': {
                'sell': 'stoch_k >= 80 AND stoch_d >= 80',
                'buy': 'stoch_k <= 20 AND stoch_d <= 20',
                'buy_moderate': 'stoch_k > stoch_d',
                'sell_moderate': 'stoch_k < stoch_d',
                'neutral': 'stoch_k == stoch_d',
            }
        },
        
        'cci': {
            'description': 'Commodity Channel Index - Momentum indicator measuring deviation from mean',
            'scale': '-∞ to +∞ (typically -200 to +200)',
            'thresholds': {
                'strong_buy': 100,      # CCI > 100: Strong upward deviation
                'strong_sell': -100,    # CCI < -100: Strong downward deviation
                'buy': 0,               # CCI > 0: Above zero (bullish bias)
                'sell': 0,              # CCI < 0: Below zero (bearish bias)
            },
            'parameters': {
                'short_term': 10,
                'intermediate_term': 14,
                'long_term': 20,
            },
            'signal_logic': {
                'strong_buy': 'cci_value > 100',
                'buy': '0 < cci_value <= 100',
                'sell': '-100 <= cci_value < 0',
                'strong_sell': 'cci_value < -100',
            }
        },
        
        'roc': {
            'description': 'Rate of Change - Momentum indicator measuring price change over period',
            'scale': '-∞ to +∞ (percentage)',
            'thresholds': {
                'strong_buy': 5,        # ROC > 5: Strong positive momentum
                'buy': 0,               # ROC > 0: Positive momentum
                'strong_sell': -5,      # ROC < -5: Strong negative momentum
                'sell': 0,              # ROC < 0: Negative momentum
            },
            'parameters': {
                'short_term': 9,
                'intermediate_term': [12, 20],  # Both used in rolling heatmap
                'long_term': 50,
            },
            'signal_logic': {
                'strong_buy': 'roc_value > 5',
                'buy': '0 < roc_value <= 5',
                'sell': '-5 <= roc_value < 0',
                'strong_sell': 'roc_value < -5',
                'neutral': 'roc_value == 0',
            }
        },
        
        'ultimate_oscillator': {
            'description': 'Ultimate Oscillator - Multi-timeframe momentum indicator',
            'scale': '0-100',
            'thresholds': {
                'sell': 70,             # UO > 70: Overbought (sell signal)
                'buy': 30,              # UO < 30: Oversold (buy signal)
                'buy_moderate': 50,     # UO > 50: Above midpoint (bullish bias)
                'sell_moderate': 50,    # UO < 50: Below midpoint (bearish bias)
            },
            'parameters': {
                'short_term': (5, 10, 20),      # (short, medium, long) periods
                'intermediate_term': (7, 14, 28),
                'long_term': (10, 20, 40),
            },
            'signal_logic': {
                'sell': 'uo_value > 70',
                'buy_moderate': '50 < uo_value <= 70',
                'neutral': 'uo_value == 50',
                'sell_moderate': '30 <= uo_value < 50',
                'buy': 'uo_value < 30',
            }
        },
        
        'williams_r': {
            'description': 'Williams %R - Momentum indicator comparing closing price to high-low range',
            'scale': '0 to -100 (inverted)',
            'thresholds': {
                'sell_strong': -20,     # Williams%R > -20: Overbought territory
                'sell_moderate': -50,   # Williams%R > -50: Bearish bias
                'buy_moderate': -50,    # Williams%R < -50: Bullish bias
                'buy_strong': -80,      # Williams%R < -80: Oversold territory
            },
            'parameters': {
                'short_term': 5,
                'intermediate_term': 14,
                'long_term': 20,
            },
            'signal_logic': {
                'sell_strong': 'williams_r_value > -20',
                'sell_moderate': '-50 < williams_r_value <= -20',
                'buy_moderate': '-80 < williams_r_value <= -50',
                'buy_strong': 'williams_r_value < -80',
            }
        },
        
        'mfi': {
            'description': 'Money Flow Index - Volume-weighted momentum oscillator (NEW)',
            'scale': '0-100',
            'thresholds': {
                'sell': 70,             # MFI > 70: Overbought (volume-weighted)
                'buy': 30,              # MFI < 30: Oversold (volume-weighted)
                'neutral': 50,          # MFI == 50: Neutral point
            },
            'parameters': {
                'short_term': 10,
                'intermediate_term': 14,
                'long_term': 30,
            },
            'signal_logic': {
                'sell': 'mfi_value > 70',
                'neutral_sell': '50 < mfi_value <= 70',
                'neutral': 'mfi_value == 50',
                'neutral_buy': '30 <= mfi_value < 50',
                'buy': 'mfi_value < 30',
            }
        },
        
        'cmf': {
            'description': 'Chaikin Money Flow - Accumulation/Distribution oscillator (NEW)',
            'scale': '-1 to +1',
            'thresholds': {
                'buy': 0,               # CMF > 0: Money flowing in (accumulation)
                'sell': 0,              # CMF < 0: Money flowing out (distribution)
                'strong_buy': 0.25,     # CMF > 0.25: Strong accumulation
                'strong_sell': -0.25,   # CMF < -0.25: Strong distribution
            },
            'parameters': {
                'short_term': 10,
                'intermediate_term': 21,
                'long_term': 50,
            },
            'signal_logic': {
                'strong_buy': 'cmf_value > 0.25',
                'buy': '0 < cmf_value <= 0.25',
                'sell': '-0.25 <= cmf_value < 0',
                'strong_sell': 'cmf_value < -0.25',
            }
        },
    },
    
    'trend': {
        'adx': {
            'description': 'Average Directional Index - Trend strength and direction indicator',
            'scale': '0-100 (trend strength)',
            'thresholds': {
                'very_strong': 50,      # ADX >= 50: Very strong trend
                'strong': 25,           # ADX >= 25: Strong trend
                'weak': 25,             # ADX < 25: Weak trend (no clear direction)
                'di_threshold': 0,      # +DI vs -DI for directional bias
            },
            'parameters': {
                'short_term': 9,
                'intermediate_term': 14,
                'long_term': 20,
            },
            'signal_logic': {
                'trend_strength': {
                    'very_strong': 'adx >= 50',
                    'strong': '25 <= adx < 50',
                    'weak': 'adx < 25',
                },
                'direction': {
                    'buy': '+DI > -DI',
                    'sell': '-DI > +DI',
                    'neutral': '+DI == -DI',
                },
                'override': 'If adx < 25, signal is Neutral regardless of DI',
            }
        },
        
        'macd': {
            'description': 'Moving Average Convergence Divergence - Trend following momentum indicator with volatility-normalized magnitude filtering',
            'scale': '-∞ to +∞',
            'rationale': 'Magnitude filtering reduces false signals by requiring histogram movement to exceed noise level (std-normalized)',
            'parameters_and_thresholds': {
                (8, 17, 5): {
                    'description': 'Fast MACD for short-term momentum',
                    'used_in_timeframes': ['short_term'],
                    'magnitude_multiplier': 0.5,
                    'histogram_std_lookback': 20,
                    'rationale': 'Faster EMAs produce noisier histogram; tighter threshold (0.5×) filters whipsaw',
                },
                (12, 26, 9): {
                    'description': 'Standard MACD for intermediate-term momentum',
                    'used_in_timeframes': ['intermediate_term'],
                    'magnitude_multiplier': 0.5,
                    'histogram_std_lookback': 20,
                    'rationale': 'Balanced sensitivity; same multiplier as fast variant',
                },
                (20, 50, 10): {
                    'description': 'Slow MACD for long-term trend confirmation',
                    'used_in_timeframes': ['long_term'],
                    'magnitude_multiplier': 1.0,
                    'histogram_std_lookback': 20,
                    'rationale': 'Slower EMAs produce smoother histogram; wider threshold (1.0×) maintains signal sensitivity',
                },
            },
            'signal_logic': {
                'buy': 'macd > signal AND abs(macd - signal) >= magnitude_multiplier * std(histogram, histogram_std_lookback)',
                'sell': 'macd < signal AND abs(macd - signal) >= magnitude_multiplier * std(histogram, histogram_std_lookback)',
                'neutral': 'abs(macd - signal) < magnitude_multiplier * std(histogram, histogram_std_lookback)',
                'histogram_interpretation': 'positive histogram = bullish momentum, negative = bearish momentum',
                'zero_cross': 'MACD crossing zero = momentum direction reversal (secondary signal)',
            }
        },
        
        'moving_average': {
            'description': 'Simple Moving Average / Exponential Moving Average - Trend following',
            'scale': 'Price units',
            'thresholds': {
                'buy': 0.025,           # Price > MA + 0.025% (buy zone)
                'sell': -0.025,         # Price < MA - 0.025% (sell zone)
                'neutral': 0,           # Price within ±0.025% of MA (neutral zone)
            },
            'parameters': {
                'short_term_ema': [5, 10],
                'intermediate_term_ema': [20, 50],
                'intermediate_term_sma': [50],
                'long_term_sma': [100, 200],
            },
            'signal_logic': {
                'buy': 'price > ma_value * 1.00025',      # Price 0.025% above MA
                'sell': 'price < ma_value * 0.99975',     # Price 0.025% below MA
                'neutral': 'abs((price - ma) / ma * 100) <= 0.025',
            }
        },
        
        'hma': {
            'description': 'Hull Moving Average - Responsive trend following (NEW)',
            'scale': 'Price units',
            'thresholds': {
                'buy': 0.025,           # Price > HMA + 0.025% (same as MA)
                'sell': -0.025,         # Price < HMA - 0.025% (same as MA)
                'neutral': 0,           # Price within ±0.025% of HMA
            },
            'parameters': {
                'short_term': 9,
                'intermediate_term': 21,
                'long_term': 50,
            },
            'signal_logic': {
                'buy': 'price > hma_value * 1.00025',
                'sell': 'price < hma_value * 0.99975',
                'neutral': 'abs((price - hma) / hma * 100) <= 0.025',
            }
        },
        
        'vwma': {
            'description': 'Volume Weighted Moving Average - Trend following with volume weighting (NEW)',
            'scale': 'Price units',
            'thresholds': {
                'buy': 0.025,           # Price > VWMA + 0.025% (same as MA)
                'sell': -0.025,         # Price < VWMA - 0.025% (same as MA)
                'neutral': 0,           # Price within ±0.025% of VWMA
            },
            'parameters': {
                'short_term': 10,
                'intermediate_term': 20,
                'long_term': 50,
            },
            'signal_logic': {
                'buy': 'price > vwma_value * 1.00025',
                'sell': 'price < vwma_value * 0.99975',
                'neutral': 'abs((price - vwma) / vwma * 100) <= 0.025',
            }
        },
        
        'bull_bear_power': {
            'description': 'Elder Ray Index (Bull/Bear Power) - Trend strength via EMA comparison',
            'scale': 'Price difference units',
            'thresholds': {
                'both_positive': None,  # Bull > 0 AND Bear > 0: Strong buy
                'bull_positive': None,  # Bull > 0 AND Bear <= 0: Buy
                'bear_negative': None,  # Bear < 0 AND Bull <= 0: Sell
                'both_negative': None,  # Bull < 0 AND Bear < 0: Strong sell
                'mixed': None,          # One positive, one negative: Neutral
            },
            'parameters': {
                'short_term': 10,
                'intermediate_term': 13,
                'long_term': 21,
            },
            'signal_logic': {
                'strong_buy': 'bull_power > 0 AND bear_power > 0',
                'buy': 'bull_power > 0 AND bear_power <= 0',
                'sell': 'bull_power <= 0 AND bear_power < 0',
                'strong_sell': 'bull_power < 0 AND bear_power < 0',
                'neutral': '(bull_power > 0 AND bear_power < 0) OR (bull_power < 0 AND bear_power > 0)',
            }
        },
    },
    
    'volatility': {
        'bollinger_bands': {
            'description': 'Bollinger Bands - Volatility bands around moving average (NEW)',
            'scale': 'Price units',
            'thresholds': {
                'sell': None,           # Price above upper band: Overbought
                'buy': None,            # Price below lower band: Oversold
                'squeeze': None,        # Bands close together: Low volatility
                'expansion': None,      # Bands wide apart: High volatility
            },
            'parameters': {
                'short_term': (10, 1.5),        # (period, std_dev)
                'intermediate_term': (20, 2),
                'long_term': (50, 2.5),
            },
            'signal_logic': {
                'sell': 'price > upper_band',
                'buy': 'price < lower_band',
                'neutral': 'lower_band <= price <= upper_band',
                'squeeze': 'band_width < threshold',
                'expansion': 'band_width > threshold',
            }
        },
        
        'atr': {
            'description': 'Average True Range - Volatility measure (DISPLAY ONLY - no signal)',
            'scale': 'Price units (absolute)',
            'thresholds': {
                'note': 'ATR is a volatility measure only. No directional signal is generated.',
                'usage': 'Use for position sizing, stop-loss placement, and volatility context.',
            },
            'parameters': {
                'short_term': 10,
                'intermediate_term': 14,
                'long_term': 20,
            },
            'signal_logic': {
                'none': 'ATR does not generate buy/sell signals',
                'display': 'Show raw ATR value for volatility reference',
            }
        },
    },
    
    'volume': {
        'note': 'CMF moved to oscillators section for consistency',
    }
}

# Helper function to retrieve thresholds by indicator and parameter
def get_threshold(indicator_type: str, indicator_name: str, parameter_key: str = None):
    """
    Retrieve threshold configuration for a specific indicator.
    
    Args:
        indicator_type: One of 'oscillators', 'trend', 'volatility', 'volume'
        indicator_name: Name of the indicator (e.g., 'rsi', 'macd', 'adx')
        parameter_key: Optional - which parameter set to return (e.g., 'short_term', 'intermediate_term')
    
    Returns:
        Dict containing thresholds and parameters for the indicator
    """
    if indicator_type in SIGNAL_THRESHOLDS:
        if indicator_name in SIGNAL_THRESHOLDS[indicator_type]:
            threshold_config = SIGNAL_THRESHOLDS[indicator_type][indicator_name]
            if parameter_key:
                if 'parameters' in threshold_config and parameter_key in threshold_config['parameters']:
                    return threshold_config['parameters'][parameter_key]
            return threshold_config
    return None


def get_macd_thresholds_by_parameters(fast: int, slow: int, signal: int) -> dict:
    """
    Retrieve MACD threshold configuration by parameter tuple.
    
    This is the primary lookup for MACD thresholds, as features will reference
    MACD by its parameter tuple (e.g., (8,17,5)) rather than by timeframe.
    
    Args:
        fast: Fast EMA period
        slow: Slow EMA period
        signal: Signal line EMA period
    
    Returns:
        Dict with 'magnitude_multiplier', 'histogram_std_lookback', and metadata
        Returns None if parameter tuple not found in config
    
    Example:
        >>> thresholds = get_macd_thresholds_by_parameters(8, 17, 5)
        >>> thresholds['magnitude_multiplier']
        0.5
    """
    param_tuple = (fast, slow, signal)
    macd_config = SIGNAL_THRESHOLDS.get('trend', {}).get('macd', {})
    params_and_thresholds = macd_config.get('parameters_and_thresholds', {})
    
    if param_tuple in params_and_thresholds:
        return params_and_thresholds[param_tuple]
    
    return None


# Summary of all indicators and their parameters
INDICATOR_SUMMARY = {
    'short_term': {
        'oscillators': ['rsi(10)', 'stochastic(5,3,3)', 'cci(10)', 'roc(9)', 'ultimate_osc(5,10,20)', 'williams_r(5)', 'mfi(10)', 'cmf(10)'],
        'trend': ['adx(9)', 'macd(8,17,5)', 'ema(5,10)', 'hma(9)', 'vwma(10)', 'bull_bear(10)'],
        'volatility': ['bollinger(10,1.5)', 'atr(10)'],
    },
    'intermediate_term': {
        'oscillators': ['rsi(14)', 'stochastic(14,3,3)', 'cci(14)', 'roc(12,20)', 'ultimate_osc(7,14,28)', 'williams_r(14)', 'mfi(14)', 'cmf(21)'],
        'trend': ['adx(14)', 'macd(12,26,9)', 'ema(20,50)', 'sma(50)', 'hma(21)', 'vwma(20)', 'bull_bear(13)'],
        'volatility': ['bollinger(20,2)', 'atr(14)'],
    },
    'long_term': {
        'oscillators': ['rsi(21,30)', 'stochastic(21,5,5)', 'cci(20)', 'roc(50)', 'ultimate_osc(10,20,40)', 'williams_r(20)', 'mfi(30)', 'cmf(50)'],
        'trend': ['adx(20)', 'macd(20,50,10)', 'sma(100,200)', 'hma(50)', 'vwma(50)', 'bull_bear(21)'],
        'volatility': ['bollinger(50,2.5)', 'atr(20)'],
    }
}
