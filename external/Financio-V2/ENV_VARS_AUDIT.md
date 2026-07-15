# Environment Variables Audit for Docker Deployment

## Analysis Date
2026-01-03

## Summary
Comparison of environment variables across the system to ensure Docker deployment has all required variables.

## Environment Variable Sources

### 1. Trading Engine (financio_src/config.py)
```
✓ ALPACA_API_KEY (with fallbacks: LIVE_ALPACA_API_KEY, PAPER_ALPACA_API_KEY)
✓ ALPACA_SECRET_KEY (with fallbacks: LIVE_ALPACA_SECRET_KEY, PAPER_ALPACA_SECRET_KEY)
✓ ALPHA_VANTAGE_API_KEY
✓ NEWSAPI_KEY
✓ POLYGON_API_KEY (optional)
✓ TWITTER_BEARER_TOKEN (optional)
✓ REDDIT_CLIENT_ID (optional)
✓ REDDIT_CLIENT_SECRET (optional)
✓ REDDIT_USER_AGENT (optional)
✓ FINANCIO_MODE
✓ ENABLE_SENTIMENT_ANALYSIS
✓ EMAIL_ADDRESS (optional)
✓ EMAIL_PASSWORD (optional)
```

### 2. Config Manager (financio_src/config_manager.py)
```
✓ BOT_INSTANCE_ID
✓ INITIAL_BALANCE
✓ RISK_TOLERANCE
✓ MAX_POSITION_SIZE
✓ ENABLE_ENHANCED_RISK_MGMT
✓ MIN_PROFIT_THRESHOLD
✓ SL_ATR_MULTIPLIER
✓ TP_ATR_MULTIPLIER
✓ BOT_STRATEGY
✓ CONFIDENCE_THRESHOLD
✓ ROTATION_TICKERS
✓ LOG_LEVEL
✓ ENABLE_EMAIL_NOTIFICATIONS
✓ DB_ISOLATION
✓ MAX_DAILY_LOSSES
✓ PAUSE_DURATION_MINUTES
✓ MARKET_HOURS_ONLY
```

### 3. Backend (backend/supabase_config.py)
```
✓ SUPABASE_URL
✓ SUPABASE_ANON_KEY
✓ SUPABASE_SERVICE_KEY (or SUPABASE_SERVICE_ROLE_KEY)
✓ DB_HOST
✓ DB_PORT
✓ DB_NAME
✓ DB_USER
✓ DB_PASSWORD
```

### 4. Frontend (dashboard/src/)
```
✓ VITE_SUPABASE_URL
✓ VITE_SUPABASE_ANON_KEY
✓ VITE_API_URL (or VITE_API_BASE_URL)
✓ VITE_APP_URL (optional)
✓ VITE_STRIPE_PUBLISHABLE_KEY (optional)
✓ VITE_APP_NAME (optional)
✓ VITE_ENVIRONMENT (optional)
✓ VITE_ALPHA_VANTAGE_API_KEY (optional)
✓ VITE_FMP_API_KEY (optional)
✓ NODE_ENV
```

## Missing Variables in Current .env

### CRITICAL - Missing from .env:
1. **PostgreSQL Individual Variables** (redundant with DATABASE_URL but some code uses them):
   - ❌ POSTGRES_DB (template has it, .env doesn't)
   - ❌ POSTGRES_USER (template has it, .env doesn't)
   - ❌ POSTGRES_PASSWORD (template has it, .env doesn't)
   - ❌ POSTGRES_HOST (template has it, .env doesn't)
   - ❌ POSTGRES_PORT (template has it, .env doesn't)

2. **Redis Authentication**:
   - ❌ REDIS_PASSWORD (template has it, .env doesn't)
   - ❌ REDIS_HOST (template has it, .env doesn't)
   - ❌ REDIS_PORT (template has it, .env doesn't)

3. **Morgans Bot Integration**:
   - ❌ MORGANS_PATH (for building Morgans bot)
   - ❌ SHARED_DATA_PATH (for sentiment data sharing)

4. **Social Media APIs** (Optional but in template):
   - ❌ REDDIT_CLIENT_ID
   - ❌ REDDIT_CLIENT_SECRET
   - ❌ REDDIT_USER_AGENT
   - ❌ TWITTER_BEARER_TOKEN
   - ❌ POLYGON_API_KEY

5. **Frontend Variables** (for Docker build):
   - ❌ VITE_API_URL
   - ❌ VITE_SUPABASE_URL (exists as SUPABASE_URL but frontend needs VITE_ prefix)
   - ❌ VITE_SUPABASE_ANON_KEY (exists as SUPABASE_ANON_KEY but frontend needs VITE_ prefix)
   - ❌ VITE_APP_NAME
   - ❌ VITE_ENVIRONMENT
   - ❌ DASHBOARD_PORT

6. **Bot Configuration**:
   - ❌ BOT_INSTANCE_ID
   - ❌ INITIAL_BALANCE
   - ❌ RISK_TOLERANCE
   - ❌ BOT_STRATEGY
   - ❌ BOT_UPDATE_INTERVAL
   - ❌ SENTIMENT_UPDATE_INTERVAL
   - ❌ MODEL_CONFIDENCE_THRESHOLD
   - ❌ ENSEMBLE_SENTIMENT_WEIGHT
   - ❌ MAX_DAILY_LOSSES
   - ❌ PAUSE_DURATION_MINUTES
   - ❌ MARKET_HOURS_ONLY
   - ❌ DB_ISOLATION

7. **Monitoring & Notifications**:
   - ❌ EMAIL_ENABLED
   - ❌ EMAIL_ADDRESS
   - ❌ EMAIL_PASSWORD
   - ❌ SMTP_SERVER
   - ❌ SMTP_PORT
   - ❌ TELEGRAM_BOT_TOKEN
   - ❌ TELEGRAM_CHAT_ID
   - ❌ ENABLE_EMAIL_NOTIFICATIONS

8. **System Configuration**:
   - ❌ TZ (timezone)
   - ❌ LOG_FORMAT
   - ❌ LOG_FILE_SIZE
   - ❌ LOG_FILE_COUNT
   - ❌ LOG_TO_FILE
   - ❌ LOG_TO_CONSOLE

9. **Resource Limits**:
   - ❌ FINANCIO_BOT_CPU_LIMIT
   - ❌ FINANCIO_BOT_MEMORY_LIMIT
   - ❌ MORGANS_BOT_CPU_LIMIT
   - ❌ MORGANS_BOT_MEMORY_LIMIT
   - ❌ POSTGRES_CPU_LIMIT
   - ❌ POSTGRES_MEMORY_LIMIT

10. **Backup Configuration**:
    - ❌ BACKUP_ENABLED
    - ❌ BACKUP_INTERVAL
    - ❌ BACKUP_RETENTION_DAYS
    - ❌ BACKUP_PATH

11. **API Configuration**:
    - ❌ API_RATE_LIMIT
    - ❌ API_BURST_LIMIT

12. **Feature Flags**:
    - ❌ ENABLE_LSTM_PREDICTIONS
    - ❌ ENABLE_SHORT_SELLING
    - ❌ ENABLE_OPTIONS_TRADING
    - ❌ ENABLE_MULTI_TIMEFRAME

### PRESENT but might need validation:
- ✓ SUPABASE_URL
- ✓ SUPABASE_ANON_KEY
- ✓ SUPABASE_SERVICE_KEY
- ✓ DATABASE_URL
- ✓ REDIS_URL
- ✓ JWT_SECRET
- ✓ API_SECRET_KEY
- ✓ DATA_ENCRYPTION_KEY
- ✓ ALPACA_API_KEY / LIVE_ALPACA_API_KEY
- ✓ ALPACA_SECRET_KEY / LIVE_ALPACA_SECRET_KEY
- ✓ ALPHA_VANTAGE_API_KEY
- ✓ NEWSAPI_KEY
- ✓ ENABLE_ENHANCED_RISK_MGMT
- ✓ MIN_PROFIT_THRESHOLD
- ✓ SL_ATR_MULTIPLIER
- ✓ TP_ATR_MULTIPLIER
- ✓ CONFIDENCE_THRESHOLD
- ✓ MAX_POSITION_SIZE
- ✓ TRADING_MODE
- ✓ ENVIRONMENT
- ✓ NODE_ENV
- ✓ DEBUG
- ✓ APP_NAME
- ✓ APP_URL
- ✓ ALLOWED_HOSTS
- ✓ CORS_ORIGINS
- ✓ STRIPE_PUBLISHABLE_KEY
- ✓ STRIPE_SECRET_KEY
- ✓ STRIPE_WEBHOOK_SECRET

## Recommendations

### Priority 1 (CRITICAL - System won't work without these):
1. Add VITE_* variables for frontend build
2. Add PostgreSQL individual variables (POSTGRES_DB, etc.)
3. Add Redis individual variables (REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
4. Add BOT_INSTANCE_ID and core bot config

### Priority 2 (HIGH - Features won't work correctly):
5. Add Morgans integration paths (MORGANS_PATH, SHARED_DATA_PATH)
6. Add bot configuration variables
7. Add LOG_LEVEL and logging configuration

### Priority 3 (MEDIUM - Optional features):
8. Add social media API keys (if using Morgans bot)
9. Add email/Telegram notification configs
10. Add monitoring configuration (Sentry, Prometheus, Grafana)

### Priority 4 (LOW - Nice to have):
11. Add resource limits
12. Add backup configuration
13. Add feature flags
14. Add API rate limiting

## Template Comparison

**Variables in .env.production.template but NOT in .env:**
- All frontend VITE_* variables
- All PostgreSQL individual variables
- All Redis individual variables
- All Morgans bot variables
- All notification variables
- All monitoring variables
- All resource limits
- All backup configuration
- All feature flags
- System timezone (TZ)
- Detailed logging configuration

**Variables in .env but NOT in .env.production.template:**
- DATA_ENCRYPTION_KEY
- ALLOWED_HOSTS
- CORS_ORIGINS
- Some legacy Stripe keys
- PROMETHEUS_ENABLED
- GRAFANA_ENABLED
