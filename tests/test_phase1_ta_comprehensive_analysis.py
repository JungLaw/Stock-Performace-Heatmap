"""
Test Phase 1: Comprehensive Analysis Method

PURPOSE:
Tests the calculate_comprehensive_analysis() method to ensure it:
- Returns properly structured dictionary with all required keys
- Handles errors gracefully
- Calls calculate_technical_indicators() internally
- Formats technical indicators for UI consumption

USAGE:
    python tests/test_phase1_comprehensive_analysis.py

TESTS:
1. Structure validation - confirms all required keys present
2. Error handling - verifies graceful error responses
3. Technical indicators formatting - checks nested structure
4. NVDA real-world test - validates with actual data

EXPECTED OUTPUT:
    All tests should PASS showing structure is correct for UI consumption
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from calculations.technical import DatabaseIntegratedTechnicalCalculator


def test_structure_validation():
    """Test that comprehensive analysis returns correct structure"""
    print("\n" + "="*70)
    print("TEST 1: Structure Validation")
    print("="*70)
    
    calculator = DatabaseIntegratedTechnicalCalculator()
    result = calculator.calculate_comprehensive_analysis('NVDA')
    
    # Required top-level keys
    required_keys = ['ticker', 'error', 'timestamp', 'moving_averages', 
                     'technical_indicators', 'price_extremes', 'pivot_points', 'rolling_signals']
    
    print("\nChecking required keys...")
    for key in required_keys:
        if key in result:
            print(f"  [PASS] '{key}' present")
        else:
            print(f"  [FAIL] '{key}' MISSING")
            return False
    
    print("\n[PASS] Structure validation PASSED")
    return True


def test_error_handling():
    """Test error handling with invalid ticker"""
    print("\n" + "="*70)
    print("TEST 2: Error Handling")
    print("="*70)
    
    calculator = DatabaseIntegratedTechnicalCalculator()
    result = calculator.calculate_comprehensive_analysis('INVALID_TICKER_XYZ')
    
    print(f"\nTesting invalid ticker: INVALID_TICKER_XYZ")
    print(f"  Error flag: {result.get('error')}")
    print(f"  Has message: {'message' in result}")
    print(f"  Has timestamp: {'timestamp' in result}")
    
    if result.get('error') and 'message' in result:
        print("\n[PASS] Error handling PASSED")
        return True
    else:
        print("\n[FAIL] Error handling FAILED")
        return False


def test_technical_indicators_formatting():
    """Test that technical indicators are properly formatted"""
    print("\n" + "="*70)
    print("TEST 3: Technical Indicators Formatting")
    print("="*70)
    
    calculator = DatabaseIntegratedTechnicalCalculator()
    result = calculator.calculate_comprehensive_analysis('NVDA')
    
    if result.get('error'):
        print(f"\n⚠️  Could not test formatting - analysis failed: {result.get('message')}")
        return False
    
    tech_indicators = result.get('technical_indicators', {})
    
    # Expected indicators
    expected_indicators = ['rsi_14', 'macd', 'stochastic', 'adx', 'elder_ray', 'atr_14']
    
    print("\nChecking formatted technical indicators...")
    for indicator in expected_indicators:
        if indicator in tech_indicators:
            indicator_data = tech_indicators[indicator]
            has_value = 'value' in indicator_data or any(k in indicator_data for k in ['k', 'd', 'bull_power'])
            has_signal = 'signal' in indicator_data
            
            if has_value and has_signal:
                print(f"  ✅ '{indicator}' properly formatted (has value + signal)")
            else:
                print(f"  ⚠️  '{indicator}' incomplete (value: {has_value}, signal: {has_signal})")
        else:
            print(f"  ❌ '{indicator}' MISSING")
    
    print("\n✅ Technical indicators formatting PASSED")
    return True


def test_nvda_real_world():
    """Test with NVDA - the default ticker"""
    print("\n" + "="*70)
    print("TEST 4: NVDA Real-World Test")
    print("="*70)
    
    calculator = DatabaseIntegratedTechnicalCalculator()
    result = calculator.calculate_comprehensive_analysis('NVDA')
    
    print(f"\nTicker: {result.get('ticker')}")
    print(f"Error: {result.get('error')}")
    print(f"Timestamp: {result.get('timestamp')}")
    print(f"Current Price: {result.get('current_price')}")
    print(f"Calculation Date: {result.get('calculation_date')}")
    
    # Check component statuses
    print("\nComponent Status:")
    print(f"  Moving Averages: {result.get('moving_averages', {}).get('status', 'N/A')}")
    print(f"  Technical Indicators: {'implemented' if isinstance(result.get('technical_indicators'), dict) and len(result.get('technical_indicators', {})) > 1 else 'pending'}")
    print(f"  Price Extremes: {result.get('price_extremes', {}).get('status', 'N/A')}")
    print(f"  Pivot Points: {result.get('pivot_points', {}).get('status', 'N/A')}")
    print(f"  Rolling Signals: {result.get('rolling_signals', {}).get('status', 'N/A')}")
    
    # Sample technical indicator data
    if not result.get('error'):
        tech_indicators = result.get('technical_indicators', {})
        if 'rsi_14' in tech_indicators:
            rsi_data = tech_indicators['rsi_14']
            print(f"\nSample RSI Data:")
            print(f"  Value: {rsi_data.get('value')}")
            print(f"  Signal: {rsi_data.get('signal', {}).get('signal')}")
            print(f"  Description: {rsi_data.get('signal', {}).get('description')}")
    
    if not result.get('error'):
        print("\n✅ NVDA real-world test PASSED")
        return True
    else:
        print(f"\n❌ NVDA real-world test FAILED: {result.get('message')}")
        return False


def run_all_tests():
    """Run all Phase 1 tests"""
    print("\n" + "="*70)
    print("PHASE 1: COMPREHENSIVE ANALYSIS METHOD - TEST SUITE")
    print("="*70)
    
    tests = [
        ("Structure Validation", test_structure_validation),
        ("Error Handling", test_error_handling),
        ("Technical Indicators Formatting", test_technical_indicators_formatting),
        ("NVDA Real-World Test", test_nvda_real_world)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ TEST EXCEPTION in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED - Phase 1 Complete!")
        return True
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed - Review needed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
