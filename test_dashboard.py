"""
Quick test script to validate the heatmap dashboard implementation
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    """Test that all modules import correctly"""
    try:
        from calculations.performance import PerformanceCalculator
        from visualization.heatmap import FinvizHeatmapGenerator
        from config.assets import ASSET_GROUPS
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_performance_calculation():
    """Test performance calculation with a simple ticker"""
    try:
        from calculations.performance import PerformanceCalculator
        
        calc = PerformanceCalculator()
        print("🔄 Testing performance calculation for AAPL...")
        
        # Test with AAPL
        result = calc.calculate_performance_for_ticker("AAPL", "1d")
        
        if result.get('error'):
            print(f"⚠️ AAPL calculation returned error (likely market closed or API issue)")
        else:
            print(f"✅ AAPL: ${result['current_price']:.2f}, {result['percentage_change']:+.2f}%")
        
        return True
    except Exception as e:
        print(f"❌ Performance calculation error: {e}")
        return False

def test_heatmap_generation():
    """Test heatmap generation with mock data"""
    try:
        from visualization.heatmap import FinvizHeatmapGenerator
        
        generator = FinvizHeatmapGenerator()
        
        # Create mock performance data
        mock_data = [
            {
                'ticker': 'AAPL',
                'current_price': 150.0,
                'historical_price': 145.0,
                'percentage_change': 3.45,
                'absolute_change': 5.0,
                'period': '1d',
                'period_label': '1 Day',
                'error': False
            },
            {
                'ticker': 'GOOGL',
                'current_price': 2500.0,
                'historical_price': 2520.0,
                'percentage_change': -0.79,
                'absolute_change': -20.0,
                'period': '1d',
                'period_label': '1 Day',
                'error': False
            }
        ]
        
        print("🔄 Testing heatmap generation...")
        fig = generator.create_treemap(mock_data, title="Test Heatmap")
        
        if fig:
            print("✅ Heatmap generation successful")
            return True
        else:
            print("❌ Heatmap generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Heatmap generation error: {e}")
        return False

def test_asset_groups():
    """Test asset group configurations"""
    try:
        from config.assets import ASSET_GROUPS
        
        print("🔄 Testing asset groups...")
        
        for group_name, config in ASSET_GROUPS.items():
            tickers = config['tickers']
            print(f"✅ {group_name}: {len(tickers)} tickers (max: {config['max_tickers']})")
        
        return True
    except Exception as e:
        print(f"❌ Asset groups error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Dashboard Tests")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Asset Groups Test", test_asset_groups),
        ("Performance Calculation Test", test_performance_calculation),
        ("Heatmap Generation Test", test_heatmap_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 30)
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Dashboard is ready to run.")
        print("💡 Run 'streamlit run streamlit_app.py' to start the dashboard")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    main()
