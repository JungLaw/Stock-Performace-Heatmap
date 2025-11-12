# SIGNAL LOGIC ARCHITECTURE: COMPLETE ANALYSIS

**Date:** November 8, 2025  
**Analyzed By:** Claude  
**Status:** Complete system inventory + recommendations

---

## EXECUTIVE SUMMARY

Your application currently has **10 implemented signal methods** and **6 missing indicators** with no signal logic. Signal logic is **completely decentralized** - thresholds are hardcoded directly in method bodies with no central config. This creates:

- ❌ **Maintenance debt** - changing thresholds requires code edits
- ❌ **Consistency risk** - rolling heatmap needs custom parameters (RSI(10), RSI(14), RSI(30)) but no way to parametrize
- ❌ **Missing implementations** - MFI, CMF, VWMA, HMA, Bollinger Bands have no signal methods

**Recommendation:** Centralize ALL signal logic into a single `SIGNAL_CONFIG` dict that:
- Stores thresholds per indicator per parameter set
- Supports multiple timeframes (short/intermediate/long)
- Auto-generates signal methods dynamically
- Makes adding new indicators a 5-minute configuration task

---

## PART 1: CURRENT SIGNAL METHODS INVENTORY

### 10 IMPLEMENTED SIGNAL METHODS

| # | Indicator | Method Location | Parameters | Thresholds | Type | Used By |
|---|-----------|-----------------|-----------|-----------|------|---------|
| 1 | **RSI** | Line 436+ | RSI(14) | Buy≤35, Sell≥70, SBuy≤20, SSell≥80 | Momentum | Tech Dashboard |
| 2 | **Moving Average** | Line 449+ | SMA/EMA(5-200) | ±0.025% neutral | Trend | Tech Dashboard |
| 3 | **ADX** | Line 460+ | ADX(14) | <25=Weak, 25-50=Strong, ≥50=VStrong | Trend | Tech Dashboard |
| 4 | **MACD** | Line 491+ | MACD(12,26,9) | MACD>Signal=Buy, <Signal=Sell | Trend | Tech Dashboard |
| 5 | **Elder Ray** | Line 500+ | Bull/Bear(13) | Both>0=SBuy, Both<0=SSell | Trend | Tech Dashboard |
| 6 | **Stochastic** | Line 513+ | Stoch(14,3,3) | K,D≥80=Sell, ≤20=Buy | Momentum | Tech Dashboard |
| 7 | **Williams %R** | Line 526+ | %R(14) | >-20=Sell, <-80=Buy | Momentum | Tech Dashboard |
| 8 | **CCI** | Line 537+ | CCI(14) | >100=Buy, <-100=Sell | Momentum | Tech Dashboard |
| 9 | **Ultimate Osc** | Line 548+ | UO(7,14,28) | >70=Sell, <30=Buy | Momentum | Tech Dashboard |
| 10 | **ROC** | Line 559+ | ROC(12) | >5=SBuy, >0=Buy, <-5=SSell | Momentum | Tech Dashboard |

### 6 MISSING SIGNAL METHODS

| Indicator | Status | Impact | Priority |
|-----------|--------|--------|----------|
| **MFI** (Money Flow Index) | NOT CALCULATED | Can't display in rolling heatmap | HIGH |
| **CMF** (Chaikin Money Flow) | NOT CALCULATED | Can't display in rolling heatmap | HIGH |
| **VWMA** (Volume Weighted MA) | NOT CALCULATED | Can't display in rolling heatmap | HIGH |
| **HMA** (Hull Moving Average) | NOT CALCULATED | Can't display in rolling heatmap | HIGH |
| **Bollinger Bands** | NOT CALCULATED | Can't display in rolling heatmap | HIGH |
| **ATR** (Average True Range) | CALCULATED only | Volatility measure, marked as signal=N/A | MEDIUM |

---

## PART 2: CURRENT ARCHITECTURE PROBLEMS

### Problem 1: Hardcoded Thresholds (No Central Config)

**Current State:**
```python
# technical.py line 436-447
def _generate_rsi_signal(self, rsi_value: float) -> Dict:
    if rsi_value >= 80:
        return {'signal': 'Strong Sell', ...}
    elif rsi_value >= 70:
        return {'signal': 'Sell', ...}
    elif rsi_value >= 35:
        return {'signal': 'Neutral', ...}
    # ... more thresholds hardcoded
```

**Issues:**
- Thresholds only work for RSI(14)
- Can't use RSI(10) for short-term without creating new method
- If someone finds better threshold, must edit code
- Comments reference numbers but don't auto-update

**Impact on Rolling Heatmap:**
- You need: RSI(10), RSI(14), RSI(30) with DIFFERENT thresholds
- Currently: Only RSI(14) is supported

---

### Problem 2: Features Using Signal Logic

**Only ONE feature uses signal logic currently:**
1. **Technical Analysis Dashboard** (`streamlit_app.py`)
   - Calls `calculate_technical_indicators()` method
   - Gets back dict with signal, strength, description

**NOT using signal logic:**
- Moving Averages Analysis - displays values only
- Pivot Points Analysis - displays levels only  
- Rolling Heatmap - NOT IMPLEMENTED YET

---

### Problem 3: Signal Logic Distribution

```
SCATTER PATTERN:
technical.py (lines 436-569)
├─ 10 signal methods (hardcoded thresholds)
├─ No central config
└─ Each method independent

streamlit_app.py
├─ References technical_calculator
├─ Calls calculate_technical_indicators()
└─ Gets signal dict, displays as-is

MISSING: Central SIGNAL_CONFIG
```

---

## PART 3: ROLLING HEATMAP REQUIREMENTS

Your indicator settings file specifies **17 indicators × 3 timeframes = 51 parameter sets**.

### Short-Term (1-15 days) Requirements

| Indicator | Parameter | Status | Signal Method Needed | Thresholds |
|-----------|-----------|--------|----------------------|-----------|
| RSI | 10 | ✅ Calculated | ⚠️ NEW | Need RSI(10)-specific thresholds |
| Stochastic | (5,3,3) | ✅ Calculated | ⚠️ NEW | Need Stoch(5)-specific thresholds |
| CCI | 10 | ✅ Calculated | ⚠️ NEW | Need CCI(10)-specific thresholds |
| ROC | 9 | ✅ Calculated | ⚠️ NEW | Need ROC(9)-specific thresholds |
| EMA | 5, 10 | ✅ Calculated | ✅ Exists | Uses _generate_ma_signal |
| ADX | 9 | ✅ Calculated | ⚠️ NEW | Need ADX(9)-specific thresholds |
| MACD | (8,17,5) | ✅ Calculated | ⚠️ NEW | Need MACD(8,17,5)-specific logic |
| HMA | 9 | ❌ NOT CALCULATED | ❌ MISSING | No calculation, no signal |
| ATR | 10 | ✅ Calculated | ✅ N/A | Volatility only (no signal) |
| Bollinger | (10, 1.5) | ❌ NOT CALCULATED | ❌ MISSING | No calculation, no signal |
| MFI | 10 | ❌ NOT CALCULATED | ❌ MISSING | No calculation, no signal |
| CMF | 10 | ❌ NOT CALCULATED | ❌ MISSING | No calculation, no signal |
| VWMA | 10 | ❌ NOT CALCULATED | ❌ MISSING | No calculation, no signal |
| Williams %R | 5 | ✅ Calculated | ⚠️ NEW | Need WR(5)-specific thresholds |
| Ultimate Osc | (5,10,20) | ✅ Calculated | ⚠️ NEW | Need UO(5,10,20)-specific thresholds |
| Bull/Bear Power | 10 | ✅ Calculated | ⚠️ NEW | Need BP(10)-specific logic |

**Summary:**
- ✅ 7 indicators calculated but need parameter-specific signal methods
- ❌ 6 indicators NOT implemented at all
- ✅ 1 indicator (ATR) correctly marked as volatility-only

---

## PART 4: RECOMMENDED CENTRALIZED ARCHITECTURE

### Option: Centralized SIGNAL_CONFIG Dictionary

Create a single source of truth for ALL signal logic:

```python
# config/signal_logic.py

SIGNAL_CONFIG = {
    "momentum": {
        "rsi": {
            "10": {  # Short-term parameter set
                "strong_buy": 15,
                "buy": 30,
                "neutral_high": 70,
                "sell": 70,
                "strong_sell": 85
            },
            "14": {  # Intermediate-term (standard)
                "strong_buy": 20,
                "buy": 35,
                "neutral_high": 70,
                "sell": 70,
                "strong_sell": 80
            },
            "30": {  # Long-term parameter set
                "strong_buy": 25,
                "buy": 40,
                "neutral_high": 65,
                "sell": 65,
                "strong_sell": 75
            }
        },
        "stochastic": {
            "5": {
                "overbought": 80,
                "oversold": 20,
                "neutral_high": 50,
                "neutral_low": 50
            },
            "14": {
                "overbought": 80,
                "oversold": 20,
                "neutral_high": 50,
                "neutral_low": 50
            },
            "21": {
                "overbought": 80,
                "oversold": 20,
                "neutral_high": 50,
                "neutral_low": 50
            }
        },
        # ... similar for CCI, ROC, Williams %R, Ultimate Osc
    },
    "trend": {
        "adx": {
            "9": {"weak": 20, "strong": 40, "very_strong": 50},
            "14": {"weak": 25, "strong": 50, "very_strong": 60},
            "20": {"weak": 30, "strong": 50, "very_strong": 65}
        },
        "macd": {
            "8_17_5": {  # MACD(8,17,5)
                "buy_threshold": 0,
                "sell_threshold": 0
            },
            "12_26_9": {  # MACD(12,26,9)
                "buy_threshold": 0,
                "sell_threshold": 0
            },
            "20_50_10": {  # MACD(20,50,10)
                "buy_threshold": 0,
                "sell_threshold": 0
            }
        },
        # ... similar for Elder Ray, Moving Averages
    },
    "volatility": {
        "atr": {
            # ATR has no signal logic - volatility measure only
            "10": {"signal": "N/A"},
            "14": {"signal": "N/A"},
            "50": {"signal": "N/A"}
        },
        "bollinger": {
            # TODO: Need to implement Bollinger Band calculations first
        }
    },
    "volume": {
        "mfi": {
            # TODO: Need to implement MFI calculations first
        },
        "cmf": {
            # TODO: Need to implement CMF calculations first
        },
        "vwma": {
            # TODO: Need to implement VWMA calculations first
        }
    }
}

# Mapping of indicators to their categories (for rolling heatmap display)
TIMEFRAME_INDICATORS = {
    "short_term": {
        "momentum": ["RSI(10)", "Stoch(5,3,3)", "CCI(10)", "ROC(9)"],
        "trend": ["EMA(5)", "EMA(10)", "ADX(9)", "MACD(8,17,5)"],
        "volatility": ["ATR(10)", "Bollinger(10,1.5)"],
        "volume": ["MFI(10)", "CMF(10)", "VWMA(10)"]
    },
    "intermediate_term": {
        "momentum": ["RSI(14)", "Stoch(14,3,3)", "CCI(14)", "ROC(20)"],
        "trend": ["EMA(20)", "SMA(50)", "ADX(14)", "MACD(12,26,9)"],
        "volatility": ["ATR(14)", "Bollinger(20,2)"],
        "volume": ["MFI(14)", "CMF(21)", "VWMA(20)"]
    },
    "long_term": {
        "momentum": ["RSI(30)", "Stoch(21,5,5)", "CCI(30)", "ROC(50)"],
        "trend": ["SMA(100)", "SMA(200)", "ADX(20)", "MACD(20,50,10)"],
        "volatility": ["ATR(50)", "Bollinger(50,2.5)"],
        "volume": ["MFI(30)", "CMF(50)", "VWMA(50)"]
    }
}
```

### Benefits of This Approach

| Benefit | Impact |
|---------|--------|
| **Single Source of Truth** | Change RSI(14) threshold once, applies everywhere |
| **Parameter Flexibility** | RSI(10), RSI(14), RSI(30) all supported with appropriate thresholds |
| **Timeframe Consistency** | All 3 timeframes configured consistently |
| **Easy to Extend** | Add new indicator = add one section to config |
| **Testable** | Can validate thresholds against historical data |
| **Maintainable** | Non-code users can understand the structure |

---

## PART 5: IMPLEMENTATION ROADMAP

### Phase 1: Centralize Existing Logic (Week 1)
1. Create `config/signal_logic.py` with SIGNAL_CONFIG
2. Extract all 10 existing signal methods' thresholds into config
3. Update signal methods to read from config instead of hardcoded values
4. Verify existing functionality still works

### Phase 2: Add Missing Indicators (Week 2)
1. Implement MFI, CMF, VWMA, HMA calculations
2. Implement Bollinger Bands calculations
3. Add signal logic for each (MFI, CMF, VWMA thresholds TBD; Bollinger uses band crossover)
4. Add signal methods for these indicators

### Phase 3: Support Multiple Parameters (Week 3)
1. Modify signal methods to accept parameter set as argument
2. Support RSI(10), RSI(14), RSI(30) with appropriate thresholds
3. Same for all other indicators that need multiple parameters
4. Update `calculate_technical_indicators()` to pass parameters

### Phase 4: Rolling Heatmap Integration (Week 4)
1. Update rolling heatmap to use centralized signal config
2. Display all 17 indicators × 3 timeframes
3. Verify correct signals show for each parameter set

---

## PART 6: WHERE SIGNAL LOGIC IS CURRENTLY USED

### Technical Analysis Dashboard

**Current Flow:**
```
User selects ticker
    ↓
streamlit_app.py calls:
    st.session_state.technical_calculator.calculate_technical_indicators(ticker)
    ↓
technical.py execute (lines ~275-410):
    1. Fetch OHLCV data
    2. Calculate 11 indicators (RSI, MACD, Stoch, etc.)
    3. Call _generate_*_signal() for each
    4. Store signal in indicators dict
    5. Return dict with all values + signals
    ↓
streamlit_app.py displays:
    - Indicator value (e.g., "RSI: 45.2")
    - Signal (e.g., "Neutral")
    - Strength (e.g., "Weak")
    - Description (e.g., "Within neutral range")
```

**Current Usage Details:**
- **Only used in:** Technical Analysis Dashboard tab
- **Not used in:** Moving Averages (displays values only), Pivot Points (displays levels only)
- **Missing from:** Rolling Heatmap (not yet implemented)

---

## PART 7: RECOMMENDATIONS FOR CONSISTENCY

### For Your 3 Timeframes

**Principle:** More sensitive parameters for shorter timeframes

```
SHORT-TERM (1-15 days):
- RSI(10) threshold bands slightly tighter (e.g., 15-85 vs 20-80)
- Reason: Faster momentum changes, need quicker signals

INTERMEDIATE-TERM (15-50 days):  
- RSI(14) threshold bands standard (e.g., 20-80)
- Reason: Classic technical analysis thresholds

LONG-TERM (50+ days):
- RSI(30) threshold bands wider (e.g., 25-75)
- Reason: Broader perspective, filter out noise
```

**Same logic applies to:**
- Stochastic: Stoch(5) vs Stoch(14) vs Stoch(21)
- CCI: CCI(10) vs CCI(14) vs CCI(30)
- All oscillators: Shorter periods = tighter thresholds

---

## SUMMARY

### What Works Today
✅ 10 signal methods implemented and working  
✅ Technical Analysis Dashboard displays signals correctly  
✅ Signal strength (Strong/Moderate/Weak) system in place  
✅ Basic RSI, MACD, Stoch, ADX signals functional  

### What's Broken
❌ No centralized config - thresholds hardcoded  
❌ Can't support multiple parameters (RSI(10) vs RSI(14))  
❌ 6 indicators completely missing (MFI, CMF, VWMA, HMA, Bollinger, etc.)  
❌ Rolling heatmap can't display signals without new architecture  

### What's Needed
→ Centralized `SIGNAL_CONFIG` dictionary  
→ 6 missing indicator implementations  
→ Parameter-aware signal method wrappers  
→ Rolling heatmap integration  

**Effort Estimate:** 2-3 weeks for full implementation (including missing indicators)

---

**Ready for next steps? Should I propose the implementation plan in detail?**
