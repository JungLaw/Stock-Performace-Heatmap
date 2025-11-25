"""
PROOF: Test that existing calculate_technical_indicators(ticker) works correctly
Following new constraints: Prove existing system works before making changes
"""

import sys
sys.path.insert(0, 'src')

from calculations.technical import DatabaseIntegratedTechnicalCalculator

# Initialize calculator
tech_calc = DatabaseIntegratedTechnicalCalculator('data/stock_data.db')

print("\n" + "="*60)
print("PROOF: Testing existing calculate_technical_indicators('NVDA')")
print("="*60)

# Test the existing working method
print("\nCalling calculate_technical_indicators('NVDA')...")
result = tech_calc.calculate_technical_indicators('NVDA', save_to_db=False)

print(f"\nResult structure:")
print(f"  - Error: {result.get('error', 'N/A')}")
print(f"  - Ticker: {result.get('ticker', 'N/A')}")
print(f"  - Data source: {result.get('data_source', 'N/A')}")
print(f"  - Periods analyzed: {result.get('periods_analyzed', 'N/A')}")

if not result.get('error'):
    print(f"\n✅ SUCCESS: Method works correctly")
    
    # Show key indicators that should be populated
    key_indicators = ['rsi_14', 'macd_value', 'stoch_k', 'ema_20', 'sma_50', 'sma_200', 'williams_r', 'cci_14']
    
    print(f"\nKey indicator values:")
    for indicator in key_indicators:
        value = result.get(indicator)
        if value is not None:
            print(f"  ✅ {indicator}: {value:.4f}")
        else:
            print(f"  ❌ {indicator}: NULL/Missing")
    
    # Count total indicators
    indicator_count = 0
    for key, value in result.items():
        if key not in ['ticker', 'calculation_date', 'current_price', 'data_source', 'periods_analyzed', 'error']:
            if value is not None:
                indicator_count += 1
    
    print(f"\nTotal indicators calculated: {indicator_count}")
    
else:
    print(f"\n❌ FAILURE: {result.get('error_message', 'Unknown error')}")

print("\n" + "="*60)
print("PROOF COMPLETE")
print("="*60)