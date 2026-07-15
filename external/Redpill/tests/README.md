# Kraken API Trading Bot Test Suite

This comprehensive test suite validates the Kraken API integration for the crypto trading bot, ensuring reliable and secure trading operations.

## Test Structure

### 1. Core API Tests (`test_kraken_api.py`)
- **CryptoDataFetcher Tests**: Data fetching, caching, error handling
- **Trading Bot Tests**: Order execution, position management, PnL calculation
- **Risk Management Tests**: Position sizing, stop-loss, take-profit calculations
- **API Integration Tests**: Order creation, cancellation, balance fetching
- **WebSocket Tests**: Real-time data subscriptions
- **Live Integration Tests**: Sandbox environment testing

### 2. Trading Scenarios (`test_kraken_trading_scenarios.py`)
- **Market Condition Tests**: Bull, bear, and sideways markets
- **Volatility Handling**: High volatility and flash crash scenarios
- **Error Recovery**: Rate limits, network errors, API failures
- **Order Management**: Partial fills, cancellations, stop-loss triggers
- **Multi-Symbol Trading**: Portfolio management, correlation handling

### 3. Performance Tests (`test_kraken_performance.py`)
- **Data Fetching Performance**: Concurrent requests, response times
- **Memory Usage**: Large dataset handling, memory efficiency
- **Load Testing**: High-frequency requests, concurrent sessions
- **Database Performance**: Trade storage and retrieval under load
- **Stress Testing**: Network instability, extreme market conditions

## Running Tests

### Quick Start
```bash
# Run basic unit tests
python run_tests.py --test-type quick

# Run with coverage
python run_tests.py --test-type unit --coverage

# Run all tests (including slow ones)
python run_tests.py --test-type all --slow
```

### Test Types
- `unit`: Core functionality tests (fast)
- `integration`: API integration tests (requires credentials)
- `performance`: Performance and load tests (slow)
- `scenarios`: Trading scenario tests
- `quick`: Fast tests only
- `all`: All tests

### Options
- `--coverage`: Generate coverage reports
- `--verbose`: Detailed output
- `--parallel N`: Run tests in parallel
- `--slow`: Include slow-running tests
- `--kraken-api`: Include tests requiring API access

## Environment Setup

### Required Dependencies
```bash
pip install pytest pytest-asyncio pytest-html pytest-cov pytest-xdist
pip install ccxt pandas numpy scikit-learn xgboost talib
```

### Kraken Sandbox Credentials (Optional)
For integration tests, set environment variables:
```bash
export KRAKEN_SANDBOX_API_KEY="your_sandbox_api_key"
export KRAKEN_SANDBOX_API_SECRET="your_sandbox_api_secret"
```

## Test Categories

### Unit Tests
- Fast execution (< 5 seconds total)
- No external dependencies
- Mock all API calls
- Test core logic and calculations

### Integration Tests  
- Require Kraken sandbox credentials
- Test real API interactions
- Validate data formats and responses
- Network-dependent

### Performance Tests
- Measure execution speed and memory usage
- Test concurrent operations
- Validate under load conditions
- May take several minutes

## Coverage Goals

- **Core Trading Logic**: > 95%
- **Data Fetching**: > 90%
- **Risk Management**: > 95%
- **Error Handling**: > 85%
- **Overall**: > 90%

## Test Data

### Mock Data
- Realistic OHLCV data with proper price relationships
- Kraken-specific order book format
- Typical API response structures
- Error scenarios and edge cases

### Synthetic Data
- Generated market conditions (bull, bear, sideways)
- High volatility periods
- Large datasets for performance testing
- Correlation patterns between assets

## Continuous Integration

The test suite is designed for CI/CD integration:

1. **Pre-commit**: Quick unit tests and linting
2. **Pull Request**: Full test suite (excluding slow tests)
3. **Nightly**: All tests including performance tests
4. **Release**: Complete test suite with integration tests

## Debugging Failed Tests

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **API Errors**: Check Kraken sandbox credentials
3. **Timeout Errors**: Network connectivity or server issues
4. **Data Errors**: Mock data format mismatches

### Debugging Tools
```bash
# Run specific test with verbose output
pytest tests/test_kraken_api.py::TestKrakenDataFetcher::test_fetch_ohlcv_data_success -v

# Run with pdb debugger
pytest tests/test_kraken_api.py --pdb

# Show test coverage
pytest tests/ --cov=crypto_bot --cov-report=html
```

## Adding New Tests

### Test Naming Convention
- Test files: `test_kraken_*.py`
- Test classes: `TestKraken*`
- Test methods: `test_*`

### Fixtures
Use provided fixtures for common setup:
- `kraken_config`: Standard configuration
- `mock_kraken_data`: Standard mock responses
- `kraken_fee_schedule`: Fee calculations

### Markers
Apply appropriate markers:
```python
@pytest.mark.asyncio          # Async test
@pytest.mark.slow             # Slow-running test
@pytest.mark.integration      # Integration test
@pytest.mark.kraken_api       # Requires API access
```

## Security Considerations

### Credential Safety
- Never commit real API credentials
- Use sandbox environment for testing
- Validate credential handling in tests
- Test unauthorized access scenarios

### Data Validation
- Verify all input sanitization
- Test with malformed data
- Validate output format consistency
- Check for injection vulnerabilities

## Performance Benchmarks

### Target Performance
- Data fetch: < 500ms per symbol
- Order execution: < 1 second
- Position management: < 100ms
- Database operations: < 50ms per trade

### Memory Usage
- Baseline: < 100MB
- Large datasets: < 500MB additional
- Memory leaks: None detected

## Reporting

Test reports are generated in `test_reports/`:
- `test_report.html`: Detailed test results
- `coverage_html/`: Coverage analysis
- `test_results.xml`: JUnit format for CI
- `coverage.xml`: Coverage for CI tools