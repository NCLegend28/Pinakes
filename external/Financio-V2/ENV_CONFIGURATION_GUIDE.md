# Financio-V2 Environment Configuration Guide

## Overview
This guide explains the unified environment variable configuration for Docker deployment of Financio-V2.

## Environment Files

### 1. `.env` (Production)
- **Purpose**: Active production environment variables
- **Location**: `/Users/mosley/projects/Financio-V2/.env`
- **Lines**: 295
- **Status**: ✅ Complete with all required variables

### 2. `.env.production.template` (Template)
- **Purpose**: Template for new deployments
- **Location**: `/Users/mosley/projects/Financio-V2/.env.production.template`
- **Lines**: 316
- **Status**: ✅ Updated with deployment checklist

### 3. `.env.unified` (Reference)
- **Purpose**: Backup/reference with actual values
- **Location**: `/Users/mosley/projects/Financio-V2/.env.unified`
- **Lines**: 295
- **Status**: ✅ Complete mirror of .env

## Variable Categories

### ✅ ACTIVE Variables (Used in Production)

#### System Configuration
```bash
ENVIRONMENT=production
NODE_ENV=production
LOG_LEVEL=INFO
TZ=America/Chicago  # Your timezone
```

#### Database (PostgreSQL + Supabase)
```bash
# PostgreSQL Direct
POSTGRES_DB=financio
POSTGRES_USER=admin
POSTGRES_PASSWORD=<your-password>
DATABASE_URL=postgresql://admin:<password>@postgres:5432/financio

# Supabase (Cloud)
SUPABASE_URL=https://wveuwbjevfcgkhcvvtgm.supabase.co
SUPABASE_ANON_KEY=<your-key>
SUPABASE_SERVICE_KEY=<your-key>
```

#### Redis
```bash
REDIS_URL=redis://redis:6379
REDIS_HOST=redis
REDIS_PORT=6379
```

#### Frontend (VITE_* variables)
```bash
VITE_SUPABASE_URL=https://wveuwbjevfcgkhcvvtgm.supabase.co
VITE_SUPABASE_ANON_KEY=<your-key>
VITE_API_URL=http://localhost:8001
VITE_API_BASE_URL=http://financio.blaqdata.us/api
```

#### Trading (Alpaca)
```bash
# The bot pulls actual balance from Alpaca API
ALPACA_API_KEY=<your-key>
ALPACA_SECRET_KEY=<your-secret>
TRADING_MODE=live  # or 'paper' for testing
```

#### Market Data APIs
```bash
ALPHA_VANTAGE_API_KEY=<your-key>
NEWSAPI_KEY=<your-key>
```

#### Risk Management (ACTIVE)
```bash
ENABLE_ENHANCED_RISK_MGMT=true
MIN_PROFIT_THRESHOLD=0.015  # 1.5% minimum profit
SL_ATR_MULTIPLIER=3.5       # Stop loss: 3.5x ATR
TP_ATR_MULTIPLIER=4.5       # Take profit: 4.5x ATR
CONFIDENCE_THRESHOLD=0.75   # Minimum confidence to trade
```

#### Bot Configuration (ACTIVE)
```bash
BOT_INSTANCE_ID=production-bot-001
FINANCIO_MODE=multi-bot
BOT_STRATEGY=hybrid
ROTATION_TICKERS=AAPL,MSFT,GOOG,AMZN,TSLA,NVDA,META,NFLX,QUBT,RGTI,IONQ,QBTS,PLTR,AVGO,MDAI,ORCL
```

### ⚠️ LEGACY Variables (Not Used in Trading)

**IMPORTANT**: These variables are stored for analytics/visualization but NOT used in live trading logic:

```bash
INITIAL_BALANCE=100000      # LEGACY - Analytics only
RISK_TOLERANCE=0.02         # LEGACY - Not implemented
MAX_POSITION_SIZE=1000      # LEGACY - Bot uses 1-6 share sizing
MAX_PORTFOLIO_RISK=0.02     # LEGACY - Not implemented
MAX_DAILY_LOSS=0.05         # LEGACY - Not implemented
```

**Why they're legacy:**
- The bot uses `get_size_from_confidence()` which returns 1-6 shares based on confidence buckets
- Position sizing is **NOT** based on account balance percentage
- The bot should call `alpaca.get_account().equity` but currently doesn't
- These values are only used in:
  - `financio_src/analytics/equity_curve.py` (visualizations)
  - `backend/equity_data_extractor.py` (metrics display)
  - `financio_src/config_manager.py` (stored but not referenced)

### 🔧 Optional Variables (Disabled by Default)

#### Social Media APIs (for Morgans Bot)
```bash
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
TWITTER_BEARER_TOKEN=
POLYGON_API_KEY=
```

#### Email Notifications
```bash
EMAIL_ENABLED=false
EMAIL_ADDRESS=
EMAIL_PASSWORD=
SMTP_SERVER=smtp.gmail.com
```

#### Telegram Notifications
```bash
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

#### Payments
```bash
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
```

## How the Bot Actually Works

### Position Sizing Logic
```python
# Line 444 in live_trading.py
qty = blended_position_size(confidence, volatility, macro_trend)

# Which calls get_size_from_confidence()
# Returns: 1-6 shares based on confidence bucket
# Does NOT use account balance!
```

### What SHOULD Happen (Future Improvement)
```python
# Get actual account balance
account = alpaca_client.get_account()
portfolio_value = float(account.equity)

# Calculate position size as % of portfolio
risk_per_trade = portfolio_value * RISK_TOLERANCE  # e.g., 2%
position_size = risk_per_trade / (entry_price * stop_loss_distance)
```

## Docker Deployment

### Using the .env file
```bash
# Docker Compose automatically reads .env
docker-compose -f docker-compose.production.yml up -d

# Verify variables are loaded
docker-compose config | grep SUPABASE_URL
```

### Frontend Build
The frontend Docker build uses `--build-arg` for VITE_* variables:

```dockerfile
# From docker/Dockerfile.frontend
ARG VITE_SUPABASE_URL
ARG VITE_SUPABASE_ANON_KEY
ARG VITE_API_BASE_URL
```

These are passed from the .env file during build.

### Backend Services
Backend services receive environment variables directly:

```yaml
# From docker-compose.production.yml
environment:
  - DATABASE_URL=${DATABASE_URL}
  - REDIS_URL=${REDIS_URL}
  - ALPACA_API_KEY=${ALPACA_API_KEY}
```

## Variable Usage by Component

### Frontend (dashboard/)
**Required:**
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`
- `VITE_API_URL` or `VITE_API_BASE_URL`
- `NODE_ENV`

**Optional:**
- `VITE_STRIPE_PUBLISHABLE_KEY`
- `VITE_ALPHA_VANTAGE_API_KEY`

### Backend (backend/)
**Required:**
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`

### Trading Engine (financio_src/)
**Required:**
- `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`
- `ALPHA_VANTAGE_API_KEY`
- `NEWSAPI_KEY`
- `ENABLE_ENHANCED_RISK_MGMT`
- `MIN_PROFIT_THRESHOLD`
- `SL_ATR_MULTIPLIER`, `TP_ATR_MULTIPLIER`
- `CONFIDENCE_THRESHOLD`

**Optional:**
- Social media APIs (for enhanced sentiment)
- Email/Telegram (for notifications)

## Security Best Practices

### 1. Never Commit Real Values
```bash
# Already in .gitignore
.env
.env.*
!.env.template
!.env.*.template
```

### 2. Use Strong Secrets
Generate secure random strings:
```bash
# For JWT_SECRET, API_SECRET_KEY, DATA_ENCRYPTION_KEY
openssl rand -base64 64 | tr -d '\n'
```

### 3. Rotate Keys Regularly
- Alpaca API keys: Every 90 days
- JWT secrets: Every 6 months
- Database passwords: Every 12 months

### 4. Use Different Keys Per Environment
- Development: Different keys
- Staging: Different keys
- Production: Unique keys

## Troubleshooting

### Frontend Build Fails
**Error:** `VITE_SUPABASE_URL is undefined`

**Fix:** Ensure VITE_* variables are in .env and passed as build args:
```yaml
build:
  args:
    - VITE_SUPABASE_URL=${VITE_SUPABASE_URL}
```

### Backend Can't Connect to Database
**Error:** `Connection refused to postgres:5432`

**Fix:** Check DATABASE_URL and individual POSTGRES_* variables match:
```bash
POSTGRES_HOST=postgres  # Must match service name in docker-compose
DATABASE_URL=postgresql://admin:password@postgres:5432/financio
```

### Bot Can't Access Alpaca
**Error:** `Missing Alpaca API keys`

**Fix:** The bot tries multiple variable names:
```python
# From config.py
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY") or \
                 os.getenv("LIVE_ALPACA_API_KEY") or \
                 os.getenv("PAPER_ALPACA_API_KEY")
```

Ensure at least one is set.

### Redis Connection Fails
**Error:** `Error connecting to Redis`

**Fix:** Redis doesn't require password by default:
```bash
REDIS_URL=redis://redis:6379  # No password
REDIS_PASSWORD=  # Empty
```

## Migration from Old .env

If you had an old .env file:
```bash
# 1. Backup was created automatically
ls -la .env.backup.*

# 2. Your old file had ~71 lines
# 3. New file has ~295 lines

# 4. All your existing values were preserved
# 5. 60+ new variables were added

# 6. To see what changed:
diff .env.backup.YYYYMMDD_HHMMSS .env
```

## Summary

### Total Variables: 100+
- **Active in Trading**: 40-50 variables
- **Frontend Build**: 10 variables
- **Legacy/Analytics**: 5 variables
- **Optional**: 30-40 variables
- **System Config**: 15-20 variables

### Files Updated
- ✅ `.env` - Production ready
- ✅ `.env.production.template` - Template ready
- ✅ `.env.unified` - Reference ready
- ✅ All legacy variables marked
- ✅ All comments added

### Next Steps
1. Review optional services (email, social media APIs)
2. Test Docker build with new .env
3. Verify frontend receives VITE_* variables
4. Consider implementing proper account-balance-based position sizing

## References

- Main Config: `financio_src/config.py`
- Config Manager: `financio_src/config_manager.py`
- Trading Logic: `financio_src/trading/live_trading.py`
- Position Sizing: `financio_src/trading/sizing.py`
- Backend Config: `backend/supabase_config.py`
