# Test Organization

This directory contains the complete test suite for the Stock Performance Heatmap Dashboard.

## Test Files Structure

### Core Module Tests
- **`test_volume_calculator.py`** - Tests `src/calculations/volume.py`
  - DatabaseIntegratedVolumeCalculator class
  - Auto-fetch functionality (database → yfinance → auto-save)
  - Core volume calculation methods
  - Database integration and save operations

- **`test_performance_calculator.py`** - Tests `src/calculations/performance.py` 
  - DatabaseIntegratedPerformanceCalculator class
  - Price performance calculations
  - Trading day logic and date validation

### Feature Integration Tests  
- **`test_volume_integration.py`** - Integration tests for volume analysis
  - Session cache functionality (save_to_db=False)
  - "Try before you buy" exploration workflow
  - Group calculations with mixed save scenarios
  - End-to-end auto-fetch workflows

- **`test_holiday_logic.py`** - Tests trading day calculations
  - US market holiday handling
  - Weekend logic and trading day validation
  - Edge cases for holiday adjustments

### Legacy/Development Tests
- **`comprehensive_volume_test.py`** - Multi-ticker production simulation
  - Tests 5 tickers across all benchmark periods
  - Simulates real dashboard usage patterns
  - Performance and load testing

- **`simple_volume_test.py`** - Quick validation and debugging
  - Fast smoke test for basic functionality
  - Windows Unicode compatibility focused
  - Minimal external dependencies

## Test Categories

### Unit Tests
Focus on individual functions and methods:
- `test_volume_calculator.py` (Classes: TestVolumeCalculatorCore, TestVolumeCalculatorAutoFetch)
- Individual method testing with assertions

### Integration Tests  
Focus on feature workflows and system behavior:
- `test_volume_integration.py` (Classes: TestSessionCacheWorkflow, TestGroupCalculationsIntegration)
- End-to-end scenario testing

### System Tests
Focus on complete user workflows:
- Exploration workflow (new stock evaluation)
- Production workflow (bucket ticker auto-fetch)
- Mixed scenario testing

## Running Tests

### All Tests
```bash
# Run all tests with pytest (recommended)
pytest tests/ -v

# Run all tests with detailed output
pytest tests/ -v -s
```

### Specific Test Files
```bash
# Core volume calculator tests
pytest tests/test_volume_calculator.py -v
python tests/test_volume_calculator.py

# Integration and workflow tests  
pytest tests/test_volume_integration.py -v
python tests/test_volume_integration.py

# Trading day logic tests
pytest tests/test_holiday_logic.py -v
```

### Specific Test Classes
```bash
# Session cache tests only
pytest tests/test_volume_integration.py::TestSessionCacheWorkflow -v

# Auto-fetch tests only  
pytest tests/test_volume_calculator.py::TestVolumeCalculatorAutoFetch -v
```

## Test Coverage Map

### Volume Calculator (`src/calculations/volume.py`)
| Method | Test File | Test Class | Status |
|--------|-----------|------------|--------|
| `_fetch_volume_from_yfinance()` | test_volume_calculator.py | TestVolumeCalculatorCore | ✅ |
| `_save_volume_data_to_db()` | test_volume_calculator.py | TestVolumeCalculatorCore | ✅ |
| `get_current_volume()` | test_volume_calculator.py | TestVolumeCalculatorAutoFetch | ✅ |
| `get_volume_benchmark()` | test_volume_calculator.py | TestVolumeCalculatorAutoFetch | ✅ |
| `calculate_volume_performance()` | test_volume_integration.py | TestSessionCacheWorkflow | ✅ |
| Session cache functionality | test_volume_integration.py | TestSessionCacheWorkflow | ✅ |

### Key Workflows Tested
| Workflow | Test File | Description | Status |
|----------|-----------|-------------|--------|
| Auto-fetch (save_to_db=True) | test_volume_calculator.py | Database-first → yfinance → save | ✅ |
| Exploration (save_to_db=False) | test_volume_integration.py | Session cache only, no DB pollution | ✅ |
| 60D period resolution | test_volume_calculator.py | Previously failing, now working | ✅ |
| Group calculations | test_volume_integration.py | Multiple tickers with mixed scenarios | ✅ |

## Test Data and Dependencies

### External Dependencies
- **yfinance API**: Tests require internet connection
- **SQLite database**: Tests use actual database file
- **Real market data**: Tests use current market data (not mocked)

### Test Tickers Used
- **AAPL, MSFT, NVDA** - Established tickers likely in database
- **AMD, BABA, ROKU** - Test tickers for exploration scenarios  
- **PLTR, SNOW, ZM** - Additional test cases for various scenarios

### Database Considerations
- Tests may modify actual database (add test data)
- Session cache tests designed to avoid database pollution
- Some tests verify database state changes

## Test Development Guidelines

### Adding New Tests
1. **Identify the module**: Which `src/` file are you testing?
2. **Choose appropriate test file**: Core functionality vs integration
3. **Follow naming convention**: `test_<module_name>.py`
4. **Add clear docstrings**: Explain what the test verifies
5. **Update this README**: Add new test to coverage map

### Test Structure Template
```python
class TestNewFeature:
    """Test description of the feature"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.calculator = DatabaseIntegratedVolumeCalculator()
    
    def test_specific_functionality(self):
        """
        Test specific aspect of functionality
        
        Verifies:
        - Specific behavior 1
        - Specific behavior 2
        - Expected outcome
        """
        # Arrange
        # Act  
        # Assert
        pass
```

### Best Practices
- **Clear test names**: Describe what is being tested
- **Comprehensive docstrings**: Explain verification goals
- **Isolated tests**: Each test should be independent
- **Realistic data**: Use actual tickers and market scenarios
- **Performance awareness**: Note tests that require API calls

## Troubleshooting

### Common Issues
- **Internet connection**: Many tests require yfinance API access
- **Rate limiting**: Avoid running tests too frequently 
- **Database locks**: Ensure no other processes using database
- **Encoding issues**: Windows console may have Unicode limitations

### Test Failures
- Check internet connection for API-dependent tests
- Verify database file permissions and access
- Review yfinance API changes that might affect data structure
- Check that test tickers still exist and are tradeable

## Future Test Enhancements

### Potential Additions
- **Mock yfinance responses** for offline testing
- **Performance benchmarking** tests
- **UI integration tests** with Streamlit
- **Database migration tests**
- **Error handling edge cases**

### Maintenance
- **Regular review** of test tickers (ensure still valid)
- **Update for API changes** in yfinance
- **Expand coverage** for new features
- **Optimize test execution time**

---

**Last Updated**: September 2025  
**Total Test Files**: 6 (2 core + 2 integration + 2 legacy)  
**Test Coverage**: Volume calculator auto-fetch enhancement complete
