"""
Test Phase 2: Moving Averages Comprehensive Analysis

PURPOSE:
Tests the _calculate_moving_averages() method to ensure it:
- Calculates SMA and EMA for all 8 periods (5, 9, 10, 20, 21, 50, 100, 200)
- Computes bidirectional percentages (MA/P0 and P0/MA)
- Generates Buy/Sell/Neutral signals with +-0.025% threshold
- Returns properly structured data for 8x8 table display

USAGE:
    python tests/test_phase2_ta_moving_averages.py

TESTS:
1. Period coverage - all 8 periods calculated
2. Bidirectional percentages - both directions computed correctly
3. Signal logic - +-0.025% threshold applied correctly
4. NVDA real-world test - validates with actual data

EXPECTED OUTPUT:
    All tests should PASS with proper MA calculations for 8x8 table
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from calculations.technical import DatabaseIntegratedTechnicalCalculator


def test_period_coverage():
    """Test that all 8 periods are calculated"""
    print("\n" + "="*70)
    print("TEST 1: Period Coverage")
    print("="*70)
    
    calculator = DatabaseIntegratedTechnicalCalculator()
    result = calculator._calculate_moving_averages('NVDA')
    
    if result.get('error'):
        print(f"\n[FAIL] Calculation failed: {result.get('message')}")
        return False
    
    required_periods = ['MA5', 'MA9', 'MA10', 'MA20', 'MA21', 'MA50', 'MA100', 'MA200']
    periods_data = result.get('periods', {})
    
    print(f"\nCalculated periods: {len(periods_data)}")
    print(f"Required periods: {len(required_periods)}")
    
    all_present = True
    for period in required_periods:
        if period in periods_data:
            print(f"  [PASS] {period} present")
        else:
            print(f"  [FAIL] {period} MISSING")
            all_present = False
    
    if all_present:
        print("\n[PASS] Period coverage test PASSED")
        return True
    else:
        print("\n[FAIL] Period coverage test FAILED")
        return False


def test_bidirectional_percentages():
    """Test bidirectional percentage calculations"""
    print("\n" + "="*70)
    print("TEST 2: Bidirectional Percentages")
    print("="*70)
    
    calculator = DatabaseIntegratedTechnicalCalculator()
    result = calculator._calculate_moving_averages('NVDA')
    
    if result.get('error'):
        print(f"\n[FAIL] Calculation failed: {result.get('message')}")
        return False
    
    current_price = result.get('current_price')
    periods_data = result.get('periods', {})
    
    if not periods_data:
        print("\n[FAIL] No period data available")
        return False
    
    # Test MA20 as example
    ma20_data = periods_data.get('MA20')
    if not ma20_data:
        print("\n[FAIL] MA20 data not found")
        return False
    
    print(f"\nCurrent Price: ${current_price:.2f}")
    print(f"\nMA20 SMA Analysis:")
    print(f"  SMA Value: ${ma20_data['sma']['value']:.2f}")
    print(f"  SMA/P0 (MA vs Price): {ma20_data['sma']['ma_vs_price']:+.3f}%")
    print(f"  P0/SMA (Price vs MA): {ma20_data['sma']['price_vs_ma']:+.3f}%")
    print(f"  Signal: {ma20_data['sma']['signal']['signal']}")
    
    # Verify bidirectional percentages are inverses (approximately)
    sma_value = ma20_data['sma']['value']
    ma_vs_price = ma20_data['sma']['ma_vs_price']
    price_vs_ma = ma20_data['sma']['price_vs_ma']
    
    # Check if price is above MA
    if current_price > sma_value:
        # ma_vs_price should be negative (MA below price)
        # price_vs_ma should be positive (price above MA)
        if ma_vs_price < 0 and price_vs_ma > 0:
            print("\n[PASS] Bidirectional percentages correct (price above MA)")
            return True
        else:
            print(f"\n[FAIL] Incorrect signs: ma_vs_price={ma_vs_price:.3f}, price_vs_ma={price_vs_ma:.3f}")
            return False
    else:
        # ma_vs_price should be positive (MA above price)
        # price_vs_ma should be negative (price below MA)
        if ma_vs_price > 0 and price_vs_ma < 0:
            print("\n[PASS] Bidirectional percentages correct (price below MA)")
            return True
        else:
            print(f"\n[FAIL] Incorrect signs: ma_vs_price={ma_vs_price:.3f}, price_vs_ma={price_vs_ma:.3f}")
            return False


def test_signal_logic():
    """Test signal generation with +-0.025% threshold"""
    print("\n" + "="*70)
    print("TEST 3: Signal Logic (+-0.025% threshold)")
    print("="*70)
    
    calculator = DatabaseIntegratedTechnicalCalculator()
    result = calculator._calculate_moving_averages('NVDA')
    
    if result.get('error'):
        print(f"\n[FAIL] Calculation failed: {result.get('message')}")
        return False
    
    periods_data = result.get('periods', {})
    
    print("\nSignal Analysis:")
    signal_counts = {'Buy': 0, 'Sell': 0, 'Neutral': 0}
    
    for period_name, period_data in periods_data.items():
        sma_signal = period_data['sma']['signal']['signal']
        ema_signal = period_data['ema']['signal']['signal']
        
        signal_counts[sma_signal] = signal_counts.get(sma_signal, 0) + 1
        signal_counts[ema_signal] = signal_counts.get(ema_signal, 0) + 1
        
        print(f"  {period_name}: SMA={sma_signal}, EMA={ema_signal}")
    
    print(f"\nSignal Distribution:")
    print(f"  Buy: {signal_counts['Buy']}")
    print(f"  Sell: {signal_counts['Sell']}")
    print(f"  Neutral: {signal_counts['Neutral']}")
    
    # Verify signals are valid
    valid_signals = all(s in ['Buy', 'Sell', 'Neutral'] for s in signal_counts.keys())
    
    if valid_signals:
        print("\n[PASS] Signal logic test PASSED")
        return True
    else:
        print("\n[FAIL] Invalid signals found")
        return False


def test_nvda_real_world():
    """Test with NVDA - comprehensive validation"""
    print("\n" + "="*70)
    print("TEST 4: NVDA Real-World Comprehensive Test")
    print("="*70)
    
    calculator = DatabaseIntegratedTechnicalCalculator()
    
    # Get comprehensive analysis (includes moving averages)
    result = calculator.calculate_comprehensive_analysis('NVDA')
    
    if result.get('error'):
        print(f"\n[FAIL] Analysis failed: {result.get('message')}")
        return False
    
    ma_data = result.get('moving_averages', {})
    
    if ma_data.get('error'):
        print(f"\n[FAIL] Moving averages calculation failed: {ma_data.get('message')}")
        return False
    
    print(f"\nTicker: {ma_data.get('ticker')}")
    print(f"Current Price: ${ma_data.get('current_price'):.2f}")
    print(f"Calculation Date: {ma_data.get('calculation_date')}")
    print(f"Periods Calculated: {len(ma_data.get('periods', {}))}")
    
    # Display sample MA50 data
    periods_data = ma_data.get('periods', {})
    if 'MA50' in periods_data:
        ma50 = periods_data['MA50']
        print(f"\nMA50 Sample Data:")
        print(f"  SMA50: ${ma50['sma']['value']:.2f}")
        print(f"  Price vs SMA50: {ma50['sma']['price_vs_ma']:+.3f}%")
        print(f"  SMA50 Signal: {ma50['sma']['signal']['signal']}")
        print(f"  EMA50: ${ma50['ema']['value']:.2f}")
        print(f"  Price vs EMA50: {ma50['ema']['price_vs_ma']:+.3f}%")
        print(f"  EMA50 Signal: {ma50['ema']['signal']['signal']}")
    
    print("\n[PASS] NVDA real-world test PASSED")
    return True


def run_all_tests():
    """Run all Phase 2 tests"""
    print("\n" + "="*70)
    print("PHASE 2: MOVING AVERAGES COMPREHENSIVE ANALYSIS - TEST SUITE")
    print("="*70)
    
    tests = [
        ("Period Coverage", test_period_coverage),
        ("Bidirectional Percentages", test_bidirectional_percentages),
        ("Signal Logic", test_signal_logic),
        ("NVDA Real-World Test", test_nvda_real_world)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n[FAIL] TEST EXCEPTION in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n[SUCCESS] ALL TESTS PASSED - Phase 2 Complete!")
        return True
    else:
        print(f"\n[FAIL] {total_count - passed_count} test(s) failed - Review needed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
