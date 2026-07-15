# 🚀 Crypto Trading Bot - Production Deployment Guide

This guide covers deploying the crypto trading bot for live trading with full monitoring, security, and backup capabilities.

## 📋 Prerequisites

- Docker 20.10+ and Docker Compose 1.29+
- At least 4GB RAM and 20GB disk space
- Valid Kraken API credentials
- (Optional) SSL certificates for production

## 🎯 Quick Start

1. **Clone and configure:**
   ```bash
   git clone <repository>
   cd Redpill
   cp .env.production.example .env.production
   ```

2. **Edit configuration:**
   - Update `.env.production` with your Kraken API credentials
   - Set secure passwords for Redis, Grafana, and other services
   - Configure trading symbols (we recommend: ETH/USD, LTC/USD, ADA/USD based on our analysis)

3. **Deploy:**
   ```bash
   ./deploy.sh
   ```

## 📁 Project Structure

```
├── docker-compose.production.yml  # Production services
├── Dockerfile.production          # Production container
├── .env.production.example        # Environment template
├── deploy.sh                      # Deployment script
├── config/
│   ├── redis.conf                # Redis configuration
│   ├── prometheus.yml             # Metrics collection
│   ├── loki.yml                  # Log aggregation
│   ├── promtail.yml              # Log shipping
│   ├── grafana/
│   │   ├── datasources/          # Data source configs
│   │   └── dashboards/           # Pre-built dashboards
│   └── nginx/
│       ├── nginx.conf            # Reverse proxy config
│       └── ssl/                  # SSL certificates
└── secrets/
    └── kraken_api.key            # API credentials (create this)
```

## 🔧 Configuration

### Environment Variables (.env.production)

**Required:**
- `CRYPTO_API_KEY` - Your Kraken API key
- `CRYPTO_API_SECRET` - Your Kraken API secret
- `REDIS_PASSWORD` - Secure Redis password
- `GRAFANA_PASSWORD` - Grafana admin password

**Trading Settings:**
- `TRADING_MODE=live` - Set to 'live' for real trading, 'paper' for simulation
- `CRYPTO_SYMBOLS=ETH/USD,LTC/USD,ADA/USD` - Top performing pairs from our analysis
- `CONFIDENCE_THRESHOLD=0.75` - Minimum confidence for trades
- `MAX_POSITION_SIZE=0.20` - Maximum 20% of portfolio per position

### API Credentials

Create `secrets/kraken_api.key`:
```
your_api_key:your_api_secret
```

Get credentials from: https://www.kraken.com/u/security/api

**Required API permissions:**
- Query Funds
- Query Open Orders
- Query Closed Orders
- Query Trades History
- Create & Cancel Orders

## 🚀 Deployment Options

The deployment script offers three configurations:

### 1. Core Only
Basic setup with just the trading bot and Redis:
```bash
./deploy.sh
# Choose option 1
```

**Services:** `crypto-bot`, `redis`
**Ports:** 8000 (API), 6379 (Redis)

### 2. Core + Monitoring
Includes full observability stack:
```bash
./deploy.sh
# Choose option 2
```

**Additional services:** `prometheus`, `grafana`, `loki`, `promtail`, `node-exporter`
**Ports:** 3001 (Grafana), 9090 (Prometheus), 3100 (Loki)

### 3. Full Production
Complete production setup with SSL and reverse proxy:
```bash
./deploy.sh
# Choose option 3
```

**Additional services:** `nginx`, `deadmans-switch`, `backup`, `security-scan`
**Ports:** 80/443 (HTTPS), all internal services behind proxy

## 📊 Monitoring & Alerts

### Grafana Dashboard
- **URL:** http://localhost:3001
- **Login:** admin / (check GRAFANA_PASSWORD in .env)
- **Features:**
  - Real-time trading performance
  - Portfolio balance tracking
  - API response times
  - System resource usage
  - Error rates and alerts

### Prometheus Metrics
- **URL:** http://localhost:9090
- **Metrics include:**
  - `crypto_bot_total_profit` - Total profit/loss
  - `crypto_bot_trades_total` - Number of trades
  - `crypto_bot_win_rate` - Success rate
  - `crypto_bot_active_positions` - Current positions
  - `crypto_bot_api_request_duration_seconds` - API performance

### Log Aggregation
- **Loki URL:** http://localhost:3100
- **View logs in Grafana:** Explore > Loki data source
- **Log levels:** ERROR, WARN, INFO, DEBUG

### Dead Man's Switch
Automatically alerts you if the bot stops responding:
- **Telegram notifications** (configure TELEGRAM_BOT_TOKEN)
- **Webhook alerts** (configure DEADMANS_WEBHOOK_URL)
- **Check interval:** 5 minutes (configurable)

## 🔒 Security Features

### Container Security
- Non-root user execution (appuser:1001)
- Read-only root filesystem
- Dropped capabilities
- Security scanning with Trivy

### Network Security
- Internal Docker network isolation
- Localhost-only service binding
- Basic authentication on web interfaces
- SSL/TLS encryption

### Data Security
- Redis authentication
- Encrypted database storage (optional)
- Secure API key management
- Regular security scans

## 📁 Data Management

### Backups
Automated daily backups:
```bash
# Manual backup
./deploy.sh --backup

# Backup location
ls -la ./backups/
```

### Backup Contents
- SQLite database (`crypto_trades_YYYYMMDD_HHMMSS.db`)
- ML models (`models_YYYYMMDD_HHMMSS.tar.gz`)
- 30-day retention (configurable)

### Data Persistence
Docker volumes ensure data survives container restarts:
- `bot_data` - Database and application data
- `bot_logs` - Application logs
- `bot_models` - Trained ML models
- `redis_data` - Cache and session data

## 🛠 Operations

### Managing Services
```bash
# View status
docker-compose -f docker-compose.production.yml ps

# View logs
./deploy.sh --logs
./deploy.sh --logs redis

# Restart services
./deploy.sh --restart

# Stop all services  
./deploy.sh --stop

# Update and redeploy
./deploy.sh --update
```

### Health Monitoring
Each service has health checks:
```bash
# Check bot health
curl http://localhost:8000/api/health

# View all health statuses
docker-compose -f docker-compose.production.yml ps
```

### Performance Tuning
Monitor these metrics for optimal performance:
- **CPU usage** < 80%
- **Memory usage** < 2GB
- **API response time** < 5s
- **Error rate** < 1%

## 🚨 Troubleshooting

### Common Issues

**Bot won't start:**
```bash
# Check logs
./deploy.sh --logs

# Verify environment
docker-compose -f docker-compose.production.yml exec crypto-bot env | grep CRYPTO
```

**Database errors:**
```bash
# Check database file
docker-compose -f docker-compose.production.yml exec crypto-bot ls -la /app/data/

# Restore from backup
cp backups/crypto_trades_YYYYMMDD_HHMMSS.db crypto_trades.db
```

**API connection issues:**
```bash
# Test Kraken API
curl -X POST "https://api.kraken.com/0/public/Time"

# Check firewall rules
# Ensure ports 443, 80 are accessible
```

### Log Locations
- **Bot logs:** `docker logs crypto-trading-bot`
- **Nginx logs:** `docker logs crypto-bot-nginx`
- **System logs:** Available in Grafana
- **Persistent logs:** `./logs/` directory

## 📈 Trading Configuration

### Recommended Settings
Based on our backtesting analysis:

**Top Performing Pairs:**
1. **ETH/USD** - Efficiency Score: 69.6/100
2. **LTC/USD** - Efficiency Score: 67.8/100  
3. **ADA/USD** - Efficiency Score: 67.2/100

**Risk Management:**
- `MAX_POSITION_SIZE=0.20` (20% max per position)
- `CONFIDENCE_THRESHOLD=0.75` (75% minimum confidence)
- `MIN_PROFIT_THRESHOLD=0.015` (1.5% minimum profit target)

### Paper Trading
Start with paper trading to validate the system:
```bash
# Edit .env.production
TRADING_MODE=paper

# Deploy and monitor for 24-48 hours
./deploy.sh
```

### Live Trading Transition
When ready for live trading:
```bash
# Edit .env.production  
TRADING_MODE=live

# Restart services
./deploy.sh --restart
```

## 📞 Support & Maintenance

### Regular Tasks
- **Daily:** Check Grafana dashboard
- **Weekly:** Review trade performance
- **Monthly:** Update Docker images
- **Quarterly:** Rotate API keys

### Emergency Procedures
```bash
# Emergency stop
./deploy.sh --stop

# Quick restart
./deploy.sh --restart

# View recent errors
./deploy.sh --logs | grep ERROR
```

### Monitoring Alerts
Set up alerts for:
- Bot downtime > 5 minutes
- Error rate > 5%
- Portfolio loss > 10%
- API latency > 10 seconds

## 🎯 Production Checklist

Before going live:
- [ ] Valid Kraken API credentials configured
- [ ] SSL certificates installed
- [ ] Firewall rules configured
- [ ] Backup strategy tested
- [ ] Monitoring alerts configured
- [ ] Paper trading validated
- [ ] Emergency procedures documented
- [ ] API rate limits understood
- [ ] Risk management settings reviewed

---

**⚠️ Important:** This bot trades with real money. Always start with small amounts and paper trading. Never invest more than you can afford to lose. Cryptocurrency trading involves significant risk.