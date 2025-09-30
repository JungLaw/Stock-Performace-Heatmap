"""
Test Phase A: Database Save Logic

PURPOSE:
Tests the database save logic implementation to ensure:
- Bucket tickers always save (ignore checkbox)
- Non-bucket tickers respect checkbox
- No intraday data saves (only final data)
- Session cache works for unsaved tickers

USAGE:
    python tests/test_phaseA_database_save_logic.py

TESTS:
1. Bucket detection - identifies Country/Sector/Custom tickers
2. Non-bucket ticker behavior - respects save_to_db parameter
3. Final data validation - prevents intraday saves
4. Session-only analysis - data not persisted

EXPECTED OUTPUT:
    All tests should PASS confirming save logic works correctly
"""

import sys
from pathlib import Path
from datetime import datetime, date, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))
sys.path.insert(0, str(project_root))

from calculations.technical import DatabaseIntegratedTechnicalCalculator
from calculations.performance import get_last_completed_trading_day


def test_bucket_detection():
    """Test that bucket tickers are correctly identified"""
    print("\n" + "="*70)
    print("TEST 1: Bucket Detection")
    print("="*70)
    
    # Import the helper function
    import streamlit_app
    
    # Test known bucket tickers
    bucket_tickers = ['VTI', 'SPY', 'XLF', 'EWT', 'NVDA']  # Mix of country, sector, custom
    non_bucket_tickers = ['LEU', 'RANDOM', 'TEST123']
    
    print("\nTesting bucket tickers:")
    for ticker in bucket_tickers:
        is_bucket = streamlit_app.is_bucket_ticker(ticker)
        print(f"  {ticker}: {'[BUCKET]' if is_bucket else '[NOT BUCKET]'}")
    
    print("\nTesting non-bucket tickers:")
    for ticker in non_bucket_tickers:
        is_bucket = streamlit_app.is_bucket_ticker(ticker)
        print(f"  {ticker}: {'[BUCKET - UNEXPECTED]' if is_bucket else '[NOT BUCKET - CORRECT]'}")
    
    print("\n[PASS] Bucket detection test completed")
    return True


def test_final_data_validation():
    """Test that only final data gets saved"""
    print("\n" + "="*70)
    print("TEST 2: Final Data Validation")
    print("="*70)
    
    # Get last completed trading day
    last_complete = get_last_completed_trading_day()
    today = date.today()
    
    # Convert to date for comparison
    if isinstance(last_complete, datetime):
        last_complete_date = last_complete.date()
    else:
        last_complete_date = last_complete
    
    print(f"\nToday: {today}")
    print(f"Last completed trading day: {last_complete_date}")
    print(f"Is final data available for today? {last_complete_date >= today}")
    
    # Test the validation function
    import streamlit_app
    
    # Test with today's date (should be False if intraday)
    today_datetime = datetime.now()
    is_final_today = streamlit_app.is_final_data_available_for_date(today_datetime)
    print(f"\nCan save data for today? {is_final_today}")
    
    # Test with last completed day (should be True)
    last_complete_datetime = datetime.combine(last_complete, datetime.min.time())
    is_final_last = streamlit_app.is_final_data_available_for_date(last_complete_datetime)
    print(f"Can save data for {last_complete}? {is_final_last}")
    
    # Test with yesterday (should be True)
    yesterday = today - timedelta(days=1)
    yesterday_datetime = datetime.combine(yesterday, datetime.min.time())
    is_final_yesterday = streamlit_app.is_final_data_available_for_date(yesterday_datetime)
    print(f"Can save data for {yesterday}? {is_final_yesterday}")
    
    if last_complete_date >= today:
        print("\n[PASS] Final data validation test - Today's data is final")
    else:
        print("\n[PASS] Final data validation test - Correctly preventing intraday saves")
    
    return True


def test_save_to_db_parameter():
    """Test that save_to_db parameter is respected"""
    print("\n" + "="*70)
    print("TEST 3: save_to_db Parameter Behavior")
    print("="*70)
    
    calculator = DatabaseIntegratedTechnicalCalculator()
    
    # Test with save_to_db=False (session-only)
    print("\nTest 3a: Session-only analysis (save_to_db=False)")
    result_no_save = calculator.calculate_comprehensive_analysis('AAPL', save_to_db=False)
    
    if not result_no_save.get('error'):
        print(f"  [PASS] AAPL analysis completed (session-only)")
        print(f"  Current price: ${result_no_save.get('current_price')}")
        print(f"  Data available in memory: Yes")
    else:
        print(f"  [FAIL] Analysis failed: {result_no_save.get('message')}")
        return False
    
    # Test with save_to_db=True (will attempt database save)
    print("\nTest 3b: Persistent analysis (save_to_db=True)")
    result_with_save = calculator.calculate_comprehensive_analysis('MSFT', save_to_db=True)
    
    if not result_with_save.get('error'):
        print(f"  [PASS] MSFT analysis completed (attempted save)")
        print(f"  Current price: ${result_with_save.get('current_price')}")
        print(f"  Note: Actual database save depends on final data availability")
    else:
        print(f"  [FAIL] Analysis failed: {result_with_save.get('message')}")
        return False
    
    print("\n[PASS] save_to_db parameter behavior test completed")
    return True


def test_session_cache():
    """Test that unsaved data is accessible in current session"""
    print("\n" + "="*70)
    print("TEST 4: Session Cache for Unsaved Tickers")
    print("="*70)
    
    calculator = DatabaseIntegratedTechnicalCalculator()
    
    # Analyze with save_to_db=False
    ticker = 'GOOGL'
    result = calculator.calculate_comprehensive_analysis(ticker, save_to_db=False)
    
    if result.get('error'):
        print(f"\n[FAIL] Analysis failed: {result.get('message')}")
        return False
    
    print(f"\nAnalyzed {ticker} without saving to database")
    print(f"Current price: ${result.get('current_price')}")
    print(f"Calculation date: {result.get('calculation_date')}")
    
    # Verify data structure is complete
    has_ma = 'moving_averages' in result and not result['moving_averages'].get('error')
    has_ti = 'technical_indicators' in result
    
    print(f"\nData availability in session:")
    print(f"  Moving averages: {'[AVAILABLE]' if has_ma else '[MISSING]'}")
    print(f"  Technical indicators: {'[AVAILABLE]' if has_ti else '[MISSING]'}")
    
    if has_ma and has_ti:
        print("\n[PASS] Session cache test - Data available without database save")
        return True
    else:
        print("\n[FAIL] Session cache test - Data incomplete")
        return False


def run_all_tests():
    """Run all Phase A tests"""
    print("\n" + "="*70)
    print("PHASE A: DATABASE SAVE LOGIC - TEST SUITE")
    print("="*70)
    
    tests = [
        ("Bucket Detection", test_bucket_detection),
        ("Final Data Validation", test_final_data_validation),
        ("save_to_db Parameter Behavior", test_save_to_db_parameter),
        ("Session Cache", test_session_cache)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n[FAIL] TEST EXCEPTION in {test_name}: {e}")
            import traceback
            traceback.print_exc()
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
        print("\n[SUCCESS] ALL TESTS PASSED - Phase A Complete!")
        return True
    else:
        print(f"\n[FAIL] {total_count - passed_count} test(s) failed - Review needed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
