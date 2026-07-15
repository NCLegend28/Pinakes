# 🚀 Cryptocurrency Trading Bot

A sophisticated cryptocurrency trading bot built with Python, XGBoost ML, and React dashboard. Features real-time market analysis, automated trading decisions, and comprehensive risk management for 24/7 crypto markets.

## ✨ Features

- **Multi-Exchange Support**: Trade on Binance, Coinbase, Kraken, and more via CCXT
- **Machine Learning**: XGBoost-powered signal generation with 50+ technical indicators
- **Risk Management**: Dynamic volatility-based stops and position sizing
- **Real-time Dashboard**: React-based monitoring interface
- **24/7 Operation**: Designed for continuous crypto market trading
- **Paper Trading**: Safe testing mode before live trading
- **Comprehensive Logging**: Full audit trail of all trades and decisions

## 🏗️ Architecture

### Core Components

1. **Data Layer** (`CryptoDataFetcher`)
   - Real-time OHLCV data from multiple exchanges
   - Redis caching for performance
   - Funding rate and order book analysis

2. **Feature Engineering** (`CryptoFeatureEngineering`)
   - 50+ technical indicators (RSI, MACD, Bollinger Bands, etc.)
   - Crypto-specific features (funding rates, volatility regimes)
   - Time-based features for 24/7 markets

3. **Machine Learning** (`CryptoMLModel`)
   - XGBoost binary classification (BUY/SELL)
   - Confidence-based trade filtering
   - Automatic model retraining

4. **Risk Management** (`CryptoRiskManager`)
   - Volatility regime detection
   - ATR-based stop losses and take profits
   - Position sizing based on confidence

5. **Trading Engine** (`CryptoTradingBot`)
   - Automated trade execution
   - Position monitoring and management
   - Performance tracking and logging

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Redis (optional, but recommended)
- TA-Lib library
- Exchange API keys

### Installation

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd crypto-trading-bot
   pip install -r requirements.txt
   ```

2. **Install TA-Lib**
   ```bash
   # macOS
   brew install ta-lib
   pip install TA-Lib
   
   # Ubuntu/Debian
   sudo apt-get install libta-lib-dev
   pip install TA-Lib
   
   # Windows
   # Download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
   pip install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
   ```

3. **Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your exchange API credentials
   ```

4. **Initialize**
   ```bash
   python manage.py check     # Verify requirements
   python manage.py setup     # Create configuration
   python manage.py test      # Test exchange connection
   python manage.py init      # Initialize database
   ```

5. **Start Trading**
   ```bash
   python manage.py start --mode paper  # Paper trading
   python manage.py start --mode live   # Live trading
   ```

## 📊 Dashboard

The React dashboard provides real-time monitoring:

```bash
cd frontend
npm install
npm start
```

Access at: http://localhost:3000

### Dashboard Features

- Portfolio overview and P&L tracking
- Live trading signals with confidence levels
- Active position monitoring
- Performance analytics
- System status and health checks

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with your settings

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f crypto-bot

# Stop services
docker-compose down
```

### Services Included

- **crypto-bot**: Main trading application
- **redis**: Caching layer for performance
- **dashboard**: React frontend (optional)
- **nginx**: Reverse proxy (production profile)

### Production Deployment

```bash
# Start with production profile
docker-compose --profile production up -d

# Enable automatic backups
docker-compose --profile backup run backup
```

## ⚙️ Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Exchange Settings
CRYPTO_EXCHANGE=binance
CRYPTO_API_KEY=your_api_key
CRYPTO_API_SECRET=your_secret_key
CRYPTO_SANDBOX=true

# Trading Parameters
CRYPTO_SYMBOLS=BTC/USDT,ETH/USDT,BNB/USDT
CONFIDENCE_THRESHOLD=0.75
MAX_POSITION_SIZE=0.1

# Risk Management
BASE_SL_ATR_MULTIPLIER=3.0
BASE_TP_ATR_MULTIPLIER=4.0
```

### Trading Symbols

Supported format: `BASE/QUOTE` (e.g., `BTC/USDT`, `ETH/BTC`)

Popular configurations:
- **Major pairs**: `BTC/USDT,ETH/USDT,BNB/USDT`
- **DeFi tokens**: `UNI/USDT,AAVE/USDT,COMP/USDT`
- **Layer 1s**: `SOL/USDT,ADA/USDT,DOT/USDT`

## 🛠️ Management Commands

Use `manage.py` for bot operations:

```bash
# System checks
python manage.py check           # Verify requirements
python manage.py validate       # Check configuration
python manage.py test           # Test exchange connection

# Operations
python manage.py start          # Start bot (paper mode)
python manage.py start --mode live  # Start live trading
python manage.py status         # Show current status

# Data management
python manage.py backup         # Create backup
python manage.py report         # Generate performance report
python manage.py clean          # Clean old files
```

## 📈 Trading Logic

### Signal Generation

1. **Data Collection**: Fetch OHLCV, funding rates, order book
2. **Feature Engineering**: Calculate 50+ technical indicators
3. **ML Prediction**: XGBoost binary classification
4. **Confidence Filtering**: Only trade high-confidence signals
5. **Risk Assessment**: Check volatility regime and position sizing

### Risk Management

- **Stop Loss**: Dynamic ATR-based stops (2-4x ATR)
- **Take Profit**: Risk-reward optimized targets (3-5x ATR)
- **Position Sizing**: Confidence-weighted allocation
- **Time Limits**: Maximum 24-hour hold periods
- **Volatility Adjustment**: Regime-specific parameters

### Exit Conditions

Positions are closed when:
- Stop loss or take profit hit
- 24-hour time limit reached
- Model confidence drops significantly
- Manual override signal

## 📊 Performance Monitoring

### Key Metrics

- **Total P&L**: Cumulative profit/loss
- **Win Rate**: Percentage of profitable trades
- **Sharpe Ratio**: Risk-adjusted returns
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Average Trade Duration**: Typical holding period

### Reporting

```bash
# Generate reports
python manage.py report --days 30    # 30-day performance
python manage.py report --days 7     # Weekly summary
```

### Alerts and Notifications

Configure alerts in `.env`:
- Email notifications via SMTP
- Slack webhooks
- Discord webhooks
- Telegram bot integration

## 🔒 Security Best Practices

### API Security

- Use API keys with trading-only permissions
- Enable IP whitelisting on exchanges
- Store credentials in environment variables
- Use sandbox mode for testing

### File Permissions

```bash
chmod 600 .env                    # Protect environment file
chmod 700 backups/               # Secure backup directory
```

### Exchange Recommendations

- Start with sandbox/testnet
- Use dedicated trading keys
- Set up withdrawal restrictions
- Monitor API usage limits

## 📊 Backtesting

The bot includes a comprehensive backtesting engine with Kraken-specific trading costs and realistic market conditions.

### Quick Backtest

```bash
# Basic backtest with default settings
python3 manage.py backtest

# Custom parameters
python3 manage.py backtest \
  --symbol ETH/USDT \
  --days 30 \
  --timeframe 4h \
  --capital 25000
```

### Backtest Features

✅ **Kraken Fee Structure**
- Volume-based maker/taker fees (0.00% - 0.26%)
- Dynamic fee calculation based on 30-day volume

✅ **Realistic Slippage Modeling**
- Base slippage + volatility adjustments
- Market impact based on trade size
- Spread-based slippage component

✅ **Comprehensive Analytics**
- Sharpe ratio & maximum drawdown
- Win rate & profit factor
- Trade analysis with MFE/MAE
- Rolling performance metrics

✅ **Professional Visualizations**
- Equity curve with drawdown shading
- P&L distribution histograms
- Trade timeline scatter plots
- Performance metrics tables

### Backtest Commands

```bash
# Run backtest
python3 manage.py backtest --symbol BTC/USDT --days 14

# List all results
python3 manage.py results

# Open latest chart
python3 manage.py chart

# Open specific chart
python3 manage.py chart --result-name BTC_USDT_20250802_143914
```

### Output Files

Each backtest generates:
- 📊 **Performance Chart (PNG/PDF)** - Visual analysis
- 📈 **Equity Curve (CSV)** - Time series data  
- 📝 **Summary (JSON)** - Key metrics
- 📋 **Trades (CSV)** - Individual trade details

### Sample Results

```
============================================================
BACKTEST RESULTS - BTC/USDT
============================================================
Period: 2025-07-19 to 2025-08-02
Initial Capital: $10,000.00
Final Capital: $9,897.85
Total Return: $-102.15 (-1.02%)
Total Trades: 8
Win Rate: 50.0%
Profit Factor: 0.59
Sharpe Ratio: 0.25
Max Drawdown: -10.12%
Total Fees: $37.21
Total Slippage: $11.76
```

## 🔧 Troubleshooting

### Common Issues

1. **TA-Lib Installation**
   ```bash
   # If pip install fails, try conda
   conda install -c conda-forge ta-lib
   ```

2. **Redis Connection**
   ```bash
   # Start Redis locally
   redis-server
   
   # Or disable Redis in code (falls back to memory cache)
   ```

3. **Exchange API Errors**
   - Verify API key permissions
   - Check IP whitelist
   - Ensure sufficient balance
   - Validate symbol formats

4. **Model Training Failures**
   - Ensure sufficient historical data
   - Check data quality and completeness
   - Verify feature engineering pipeline

### Debug Mode

Enable detailed logging:
```bash
export LOG_LEVEL=DEBUG
python crypto_bot.py
```

### Health Checks

Monitor system health:
```bash
# Check bot status
curl http://localhost:8000/api/bot-status

# View recent logs
tail -f crypto_bot.log

# Database integrity
python -c \"import sqlite3; print('DB OK' if sqlite3.connect('crypto_trades.db').execute('SELECT 1').fetchone() else 'DB Error')\"
```

## 📚 API Reference

### REST Endpoints

- `GET /api/dashboard-data` - Portfolio overview
- `GET /api/positions` - Active positions
- `GET /api/live-signals/{symbol}` - Real-time signals
- `GET /api/bot-status` - System status
- `POST /api/train-model` - Trigger model training

### WebSocket (Future)

Real-time updates for:
- Live price feeds
- Trade executions
- Signal changes
- System alerts

## 🚧 Roadmap

### Upcoming Features

- [ ] Advanced portfolio optimization
- [ ] Multi-timeframe analysis
- [ ] Social sentiment integration
- [ ] On-chain data analysis
- [ ] Cross-exchange arbitrage
- [ ] Options and futures support

### Performance Improvements

- [ ] GPU-accelerated ML training
- [ ] Distributed computing support
- [ ] Advanced caching strategies
- [ ] Real-time feature computation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**IMPORTANT**: This software is for educational and research purposes. Cryptocurrency trading involves substantial risk of loss. Past performance does not guarantee future results. Always:

- Start with paper trading
- Use only funds you can afford to lose
- Understand the risks involved
- Comply with local regulations
- Monitor positions actively

The developers are not responsible for any financial losses incurred through the use of this software.

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd crypto-trading-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\\Scripts\\activate     # Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Code formatting
black .
flake8 .
```

## 📞 Support

- **Documentation**: See `/docs` directory
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Discord**: [Community Server](https://discord.gg/crypto-trading-bot)

---

## 🎯 Quick Commands Reference

```bash
# Setup
cp .env.example .env && python manage.py check

# Start paper trading
python manage.py start

# Monitor performance
python manage.py status && python manage.py report

# Backup data
python manage.py backup

# Docker deployment
docker-compose up -d
```

**Happy Trading! 🚀**