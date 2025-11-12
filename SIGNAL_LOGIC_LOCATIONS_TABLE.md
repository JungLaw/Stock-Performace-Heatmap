# SIGNAL LOGIC LOCATIONS TABLE

| Source File | Parent/Source Function or Class | Indicator | Used in Feature | Exists | DNE (Need to Add) |
|---|---|---|---|---|---|
| **technical.py** | `calculate_technical_indicators()` line 275 | RSI(14) | Technical Indicators Dashboard | ✅ Value calculated (line 315-319) + Signal method `_generate_rsi_signal()` (line 436) | - |
| **technical.py** | `calculate_technical_indicators()` line 275 | MACD(12,26,9) | Technical Indicators Dashboard | ✅ Value calculated (line 322-327) + Signal method `_generate_macd_signal()` (line 491) | - |
| **technical.py** | `calculate_technical_indicators()` line 275 | Stochastic(14,3,3) | Technical Indicators Dashboard | ✅ Value calculated (line 352-358) + Signal method `_generate_stochastic_signal()` (line 513) | - |
| **technical.py** | `calculate_technical_indicators()` line 275 | ADX(14) | Technical Indicators Dashboard | ✅ Value calculated (line 342-349) + Signal method `_generate_adx_signal()` (line 460) | - |
| **technical.py** | `calculate_technical_indicators()` line 275 | Elder Ray / Bull-Bear Power(13) | Technical Indicators Dashboard | ✅ Value calculated (line 331-339) + Signal method `_generate_elder_ray_signal()` (line 500) | - |
| **technical.py** | `calculate_technical_indicators()` line 275 | SMA(20, 50, 200) | Technical Indicators Dashboard | ✅ Value calculated (line 360-370) + Signal method `_generate_ma_signal()` (line 449) | - |
| **technical.py** | `calculate_technical_indicators()` line 275 | EMA(20, 50, 200) | Technical Indicators Dashboard | ✅ Value calculated (line 360-378) + Signal method `_generate_ma_signal()` (line 449) | - |
| **technical.py** | `calculate_technical_indicators()` line 275 | Williams %R(14) | Technical Indicators Dashboard | ✅ Value calculated (line 385-390) + Signal method `_generate_williams_r_signal()` (line 526) | - |
| **technical.py** | `calculate_technical_indicators()` line 275 | CCI(14) | Technical Indicators Dashboard | ✅ Value calculated (line 391-396) + Signal method `_generate_cci_signal()` (line 537) | - |
| **technical.py** | `calculate_technical_indicators()` line 275 | Ultimate Oscillator(7,14,28) | Technical Indicators Dashboard | ✅ Value calculated (line 397-402) + Signal method `_generate_ultimate_osc_signal()` (line 548) | - |
| **technical.py** | `calculate_technical_indicators()` line 275 | ROC(12) | Technical Indicators Dashboard | ✅ Value calculated (line 403-408) + Signal method `_generate_roc_signal()` (line 559) | - |
| **technical.py** | `calculate_technical_indicators()` line 275 | ATR(14) | Technical Indicators Dashboard | ✅ Value calculated (line 379-383) + Signal N/A (volatility measure only) | - |
| | | | | | |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | RSI(10) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated with period 10 | ✅ NEED: Value calc + Signal method for RSI(10) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Stochastic(5,3,3) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated with period 5 | ✅ NEED: Value calc + Signal method for Stoch(5) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | CCI(10) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated with period 10 | ✅ NEED: Value calc + Signal method for CCI(10) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | ROC(9) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated with period 9 | ✅ NEED: Value calc + Signal method for ROC(9) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | EMA(5), EMA(10) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated with periods 5,10 | ✅ NEED: Value calc (can reuse signal method) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | ADX(9) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated with period 9 | ✅ NEED: Value calc + Signal method for ADX(9) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | MACD(8,17,5) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated with params (8,17,5) | ✅ NEED: Value calc + Signal method for MACD(8,17,5) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | HMA(9) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | ATR(10) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated with period 10 | ✅ NEED: Value calc (N/A signal - volatility only) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Bollinger Bands(10,1.5) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | MFI(10) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | CMF(10) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | VWMA(10) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Williams %R(5) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated with period 5 | ✅ NEED: Value calc + Signal method for WR(5) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Ultimate Osc(5,10,20) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated with params (5,10,20) | ✅ NEED: Value calc + Signal method for UO(5,10,20) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Bull/Bear Power(10) | Rolling Heatmap (Short-Term) | ❌ Value NOT calculated with period 10 | ✅ NEED: Value calc + Signal method for BB(10) |
| | | | | | |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | RSI(14) | Rolling Heatmap (Intermediate-Term) | ✅ Value calculated (exists in `calculate_technical_indicators()`) | ✅ NEED: But must be sourced/called from rolling heatmap method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Stochastic(14,3,3) | Rolling Heatmap (Intermediate-Term) | ✅ Value calculated (exists in `calculate_technical_indicators()`) | ✅ NEED: But must be sourced/called from rolling heatmap method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | CCI(14) | Rolling Heatmap (Intermediate-Term) | ✅ Value calculated (exists in `calculate_technical_indicators()`) | ✅ NEED: But must be sourced/called from rolling heatmap method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | ROC(20) | Rolling Heatmap (Intermediate-Term) | ❌ Value NOT calculated (only ROC(12) exists) | ✅ NEED: Value calc + Signal method for ROC(20) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | EMA(20), SMA(50) | Rolling Heatmap (Intermediate-Term) | ✅ Value calculated (exists in `calculate_technical_indicators()`) | ✅ NEED: But must be sourced/called from rolling heatmap method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | ADX(14) | Rolling Heatmap (Intermediate-Term) | ✅ Value calculated (exists in `calculate_technical_indicators()`) | ✅ NEED: But must be sourced/called from rolling heatmap method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | MACD(12,26,9) | Rolling Heatmap (Intermediate-Term) | ✅ Value calculated (exists in `calculate_technical_indicators()`) | ✅ NEED: But must be sourced/called from rolling heatmap method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | HMA(21) | Rolling Heatmap (Intermediate-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | ATR(14) | Rolling Heatmap (Intermediate-Term) | ✅ Value calculated (exists in `calculate_technical_indicators()`) | ✅ NEED: But must be sourced/called from rolling heatmap method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Bollinger Bands(20,2) | Rolling Heatmap (Intermediate-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | MFI(14) | Rolling Heatmap (Intermediate-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | CMF(21) | Rolling Heatmap (Intermediate-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | VWMA(20) | Rolling Heatmap (Intermediate-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Williams %R(14) | Rolling Heatmap (Intermediate-Term) | ✅ Value calculated (exists in `calculate_technical_indicators()`) | ✅ NEED: But must be sourced/called from rolling heatmap method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Ultimate Osc(7,14,28) | Rolling Heatmap (Intermediate-Term) | ✅ Value calculated (exists in `calculate_technical_indicators()`) | ✅ NEED: But must be sourced/called from rolling heatmap method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Bull/Bear Power(13) | Rolling Heatmap (Intermediate-Term) | ✅ Value calculated (exists in `calculate_technical_indicators()`) | ✅ NEED: But must be sourced/called from rolling heatmap method |
| | | | | | |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | RSI(30) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated with period 30 | ✅ NEED: Value calc + Signal method for RSI(30) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Stochastic(21,5,5) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated with period 21 | ✅ NEED: Value calc + Signal method for Stoch(21) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | CCI(30) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated with period 30 | ✅ NEED: Value calc + Signal method for CCI(30) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | ROC(50) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated with period 50 | ✅ NEED: Value calc + Signal method for ROC(50) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | SMA(100), SMA(200) | Rolling Heatmap (Long-Term) | ✅ Value calculated (exists in `calculate_technical_indicators()`) | ✅ NEED: But must be sourced/called from rolling heatmap method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | ADX(20) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated with period 20 | ✅ NEED: Value calc + Signal method for ADX(20) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | MACD(20,50,10) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated with params (20,50,10) | ✅ NEED: Value calc + Signal method for MACD(20,50,10) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | HMA(50) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | ATR(50) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated with period 50 | ✅ NEED: Value calc + Signal method for ATR(50) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Bollinger Bands(50,2.5) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | MFI(30) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | CMF(50) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | VWMA(50) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated anywhere | ✅ NEED: Value calc + Signal method |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Williams %R(20) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated with period 20 | ✅ NEED: Value calc + Signal method for WR(20) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Ultimate Osc(10,20,40) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated with params (10,20,40) | ✅ NEED: Value calc + Signal method for UO(10,20,40) |
| **MISSING - Rolling Heatmap Not Implemented** | `generate_rolling_heatmap_data()` (NOT IMPLEMENTED - line 1096) | Bull/Bear Power(21) | Rolling Heatmap (Long-Term) | ❌ Value NOT calculated with period 21 | ✅ NEED: Value calc + Signal method for BB(21) |

---

## SUMMARY COUNTS

### Currently Implemented (Technical Analysis Dashboard)
- **Total indicators:** 12 (with signals)
- **Location:** `calculate_technical_indicators()` method in `technical.py` (lines 275-420)
- **Signal methods:** 10 separate `_generate_*_signal()` methods (lines 436-569)
- **Status:** Fully functional

### Missing (For Rolling Heatmap)
- **Short-term indicators:** 17 needed (7 need new period variants, 6 completely missing)
- **Intermediate-term indicators:** 17 needed (2 need new period variants, 6 completely missing)
- **Long-term indicators:** 17 needed (8 need new period variants, 6 completely missing)
- **Total missing/to-refactor:** 51 indicator × timeframe combinations
- **Location:** `generate_rolling_heatmap_data()` method (NOT YET IMPLEMENTED - placeholder at line 1096)

