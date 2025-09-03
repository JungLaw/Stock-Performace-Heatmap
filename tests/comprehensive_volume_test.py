"""
Comprehensive Volume Calculator Test
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from calculations.volume import DatabaseIntegratedVolumeCalculator


def comprehensive_test():
    """Test multiple tickers and benchmark periods"""
    print("COMPREHENSIVE VOLUME CALCULATOR TEST")
    print("=" * 50)
    
    calculator = DatabaseIntegratedVolumeCalculator()
    
    # Test multiple tickers
    test_tickers = ['AAPL', 'MSFT', 'NVDA', 'META', 'GOOGL']
    
    # Test all benchmark periods
    benchmark_periods = ['10d', '1w', '1m', '60d']
    
    print("Testing multiple benchmark periods with AAPL:")
    print("-" * 40)
    
    for period in benchmark_periods:
        performance = calculator.calculate_volume_performance('AAPL', period)
        if not performance.get('error', False):
            volume_change = performance['volume_change']
            label = performance['benchmark_label']
            print(f"{label:12}: {volume_change:+6.2f}%")
        else:
            print(f"{period:12}: ERROR")
    
    print("\nTesting multiple tickers with 10D benchmark:")
    print("-" * 40)
    
    for ticker in test_tickers:
        performance = calculator.calculate_volume_performance(ticker, '10d')
        if not performance.get('error', False):
            volume_change = performance['volume_change']
            current_vol = performance['current_volume']
            print(f"{ticker:6}: {volume_change:+6.2f}% (Vol: {current_vol:,})")
        else:
            print(f"{ticker:6}: ERROR")
    
    print("\nTesting group calculation:")
    print("-" * 40)
    
    group_results = calculator.calculate_volume_performance_for_group(test_tickers, '10d')
    summary = calculator.get_volume_performance_summary(group_results)
    
    print(f"Valid calculations: {summary['valid_count']}/{summary['total_count']}")
    print(f"Average volume change: {summary['avg_volume_change']:+.2f}%")
    
    if summary['best_performer']:
        best = summary['best_performer']
        print(f"Best performer: {best['ticker']} ({best['volume_change']:+.2f}%)")
    
    if summary['worst_performer']:
        worst = summary['worst_performer']
        print(f"Worst performer: {worst['ticker']} ({worst['volume_change']:+.2f}%)")


if __name__ == "__main__":
    comprehensive_test()
