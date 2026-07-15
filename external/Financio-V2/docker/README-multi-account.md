# 🏦 Multi-Account Trading Bot System

This system provides a professional-grade Docker architecture for managing multiple trading bot instances with different credentials, trading modes, and risk parameters.

## 🎯 Overview

The multi-account system allows you to run:
- **Paper Trading Bots**: For testing strategies with fake money
- **Live Trading Bots**: For production trading with real money  
- **Strategy Test Bots**: For validating new strategies
- **Multi-Bot Systems**: For advanced coordination

Each bot instance runs with completely isolated:
- ✅ **Credentials**: Separate API keys for different accounts
- ✅ **Databases**: Isolated trade data and logs
- ✅ **Risk Parameters**: Environment-specific risk management
- ✅ **Configurations**: Tailored settings per use case

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Make deployment script executable
chmod +x deploy-bots.sh

# Setup environment files and directories
./deploy-bots.sh setup
```

### 2. Configure Credentials
```bash
# Edit paper trading config
nano .env.paper

# Edit live trading config (when ready)
nano .env.live

# Edit strategy testing config
nano .env.test
```

### 3. Start Trading Bots
```bash
# Start paper trading (safe)
./deploy-bots.sh start-paper

# Start strategy testing
./deploy-bots.sh start-strategy hybrid

# Start live trading (requires confirmation)
./deploy-bots.sh start-live
```

## 📁 Architecture Overview

```
multi-account-system/
├── docker/
│   ├── Dockerfile.trading-bot          # Configurable bot container
│   └── docker-compose.multi-account.yml # Multi-bot orchestration
├── .env.paper.template                 # Paper trading config template
├── .env.live.template                  # Live trading config template
├── .env.test.template                  # Strategy testing config template
├── deploy-bots.sh                      # Deployment automation
├── launch_multi_account_bot.py         # Bot launcher
└── financio_src/
    └── config_manager.py               # Configuration management
```

## ⚙️ Configuration Management

### Environment Files

| File | Purpose | Safety Level |
|------|---------|--------------|
| `.env.paper` | Paper trading with test money | ✅ Safe |
| `.env.live` | Live trading with real money | ⚠️ Requires caution |
| `.env.test` | Strategy testing and validation | ✅ Safe |

### Key Configuration Parameters

**Trading Parameters:**
```env
INITIAL_BALANCE=100000          # Starting balance
RISK_TOLERANCE=0.02             # 2% risk per trade
MAX_POSITION_SIZE=10000         # Maximum position size
```

**Risk Management:**
```env
ENABLE_ENHANCED_RISK_MGMT=true  # Enhanced risk features
MIN_PROFIT_THRESHOLD=0.015      # 1.5% minimum profit
SL_ATR_MULTIPLIER=3.5           # Stop loss distance
TP_ATR_MULTIPLIER=4.5           # Take profit distance
```

**Strategy Selection:**
```env
BOT_STRATEGY=hybrid             # ml, trend, or hybrid
CONFIDENCE_THRESHOLD=0.75       # Minimum confidence
ROTATION_TICKERS=AAPL,MSFT,TSLA # Active tickers
```

## 🤖 Bot Deployment Options

### Paper Trading Bot
**Purpose**: Safe strategy testing with simulated money
```bash
./deploy-bots.sh start-paper
```
- Uses paper trading API
- Lower risk thresholds for testing
- All strategies enabled
- Email notifications disabled

### Live Trading Bot
**Purpose**: Production trading with real money
```bash
./deploy-bots.sh start-live
```
- Uses live trading API
- Conservative risk parameters
- Requires manual confirmation
- Email notifications enabled
- Enhanced safety features

### Strategy Test Bot
**Purpose**: Validate specific strategies
```bash
./deploy-bots.sh start-strategy ml
./deploy-bots.sh start-strategy trend
./deploy-bots.sh start-strategy hybrid
```
- Isolated testing environment
- Aggressive parameters for faster results
- Debug logging enabled
- Limited ticker set

### Multi-Bot System
**Purpose**: Advanced coordination between multiple bots
```bash
./deploy-bots.sh start-multi paper
./deploy-bots.sh start-multi live
```
- Ensemble decision making
- Inter-bot communication via Redis
- Coordinated signal processing
- Advanced portfolio management

## 📊 Monitoring and Management

### Check Status
```bash
# View all bot status
./deploy-bots.sh status

# View specific bot logs
./deploy-bots.sh logs paper
./deploy-bots.sh logs live
./deploy-bots.sh logs strategy-test

# Follow logs in real-time
./deploy-bots.sh follow multi-bot
```

### Strategy Updates
```bash
# Switch strategy for testing bot
./deploy-bots.sh update-strategy strategy-test ml

# Deploy code updates to all running bots
./deploy-bots.sh deploy-updates
```

### Stop Bots
```bash
# Stop specific bot type
./deploy-bots.sh stop paper
./deploy-bots.sh stop live

# Stop all bots
./deploy-bots.sh stop all
```

## 🔄 Development Workflow

### 1. Strategy Development
```bash
# Develop locally
python launch_multi_account_bot.py --config-type test --validate-only

# Test with paper trading
./deploy-bots.sh start-paper
```

### 2. Strategy Validation
```bash
# Test specific strategy
./deploy-bots.sh start-strategy ml

# Monitor results
./deploy-bots.sh logs strategy-test
```

### 3. Production Deployment
```bash
# Deploy to live trading
./deploy-bots.sh start-live

# Monitor closely
./deploy-bots.sh follow live
```

### 4. Update Deployment
```bash
# Build new version
./deploy-bots.sh build

# Deploy updates
./deploy-bots.sh deploy-updates
```

## 🛡️ Safety Features

### Live Trading Protections
- **Manual Confirmation**: Requires typing "CONFIRM" for live trading
- **Conservative Parameters**: Stricter risk management for live trading
- **Position Limits**: Maximum position size restrictions
- **Market Hours**: Only trades during market hours (unless forced)
- **Daily Loss Limits**: Automatic pause after maximum losses

### Database Isolation
- **Paper Trading**: `financio_trades_paper.db`
- **Live Trading**: `financio_trades_live.db` 
- **Strategy Testing**: `financio_trades_strategy_test.db`

### Credential Separation
- Different Alpaca API keys for paper vs live
- Environment-specific configurations
- Isolated Docker containers

## 📈 Performance Optimization

### Resource Allocation
```yaml
# Recommended resource limits per bot
resources:
  limits:
    memory: 1G
    cpus: '0.5'
  reservations:
    memory: 512M
    cpus: '0.25'
```

### Scaling Strategies
```bash
# Scale specific bot types
docker-compose -f docker/docker-compose.multi-account.yml up -d --scale paper-trading-bot=2

# Scale by strategy
./deploy-bots.sh start-strategy ml
./deploy-bots.sh start-strategy trend  # Run in parallel
```

## 🔧 Troubleshooting

### Common Issues

**1. Configuration Errors**
```bash
# Validate configuration
python financio_src/config_manager.py --config-type paper --validate

# Check environment files
cat .env.paper | grep -E "API_KEY|SECRET_KEY"
```

**2. Bot Won't Start**
```bash
# Check logs
./deploy-bots.sh logs paper

# Check container status
docker ps | grep financio
```

**3. Live Trading Issues**
```bash
# Force start outside market hours
python launch_multi_account_bot.py --config-type live --force

# Check API connectivity
docker exec financio-live-bot python -c "from alpaca.trading.client import TradingClient; print('API OK')"
```

**4. Database Issues**
```bash
# Check database files
ls -la logs/*/financio_trades_*.db

# Reset database for testing
rm logs/strategy-test/financio_trades_strategy_test.db
```

## 📚 Configuration Examples

### Conservative Live Trading
```env
# .env.live
INITIAL_BALANCE=25000
RISK_TOLERANCE=0.01              # 1% risk
MAX_POSITION_SIZE=2500           # $2,500 max
MIN_PROFIT_THRESHOLD=0.020       # 2% minimum profit
SL_ATR_MULTIPLIER=4.0            # Wide stops
TP_ATR_MULTIPLIER=5.0            # High targets
CONFIDENCE_THRESHOLD=0.80        # High confidence only
```

### Aggressive Testing
```env
# .env.test
INITIAL_BALANCE=10000
RISK_TOLERANCE=0.05              # 5% risk
MAX_POSITION_SIZE=1000           # $1,000 max
MIN_PROFIT_THRESHOLD=0.005       # 0.5% minimum profit
SL_ATR_MULTIPLIER=2.0            # Tight stops
TP_ATR_MULTIPLIER=3.0            # Lower targets
CONFIDENCE_THRESHOLD=0.65        # Lower confidence
```

## 🔗 Integration Points

### Email Notifications
- Startup/shutdown notifications
- Trade execution alerts
- Error notifications
- Daily performance summaries

### Database Integration
- Isolated databases per account type
- Trade logging and analytics
- Performance tracking
- Risk monitoring

### Redis Communication
- Inter-bot signal sharing
- Real-time coordination
- Performance metrics
- System health monitoring

## 📋 Deployment Checklist

**Before Live Trading:**
- [ ] Paper trading tested successfully
- [ ] Strategy validation completed
- [ ] Live trading credentials configured
- [ ] Risk parameters reviewed
- [ ] Email notifications tested
- [ ] Market hours verified
- [ ] Position limits confirmed

**Production Monitoring:**
- [ ] Bot health checks active
- [ ] Log monitoring setup
- [ ] Performance tracking enabled
- [ ] Alert systems configured
- [ ] Backup procedures tested

This multi-account system provides the flexibility and safety needed for professional algorithmic trading across multiple accounts and strategies.
