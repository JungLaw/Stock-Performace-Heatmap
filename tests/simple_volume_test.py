"""
Simple Volume Calculator Test

Quick test to verify volume calculator functionality without Unicode issues.
"""

import sys
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from calculations.volume import DatabaseIntegratedVolumeCalculator


def simple_test():
    """Simple test to verify volume calculator works"""
    print("VOLUME CALCULATOR SIMPLE TEST")
    print("=" * 40)
    
    try:
        # Initialize calculator
        calculator = DatabaseIntegratedVolumeCalculator()
        print(f"Database available: {calculator.db_available}")
        
        # Test with AAPL
        ticker = 'AAPL'
        print(f"\nTesting with {ticker}:")
        
        # Test current volume
        current_volume = calculator.get_current_volume(ticker)
        print(f"Current volume: {current_volume}")
        
        # Test 10D benchmark
        benchmark_10d = calculator.get_volume_benchmark(ticker, '10d')
        print(f"10D benchmark: {benchmark_10d}")
        
        # Test volume performance
        performance = calculator.calculate_volume_performance(ticker, '10d')
        print(f"Volume performance: {performance}")
        
        print("\nSUCCESS: Basic functionality works!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    simple_test()
