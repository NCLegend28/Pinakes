# Complete Financial Trading System - Docker Deployment Plan

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Docker Compose Stack                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Morgans    │  │  Financio    │  │  Predictive  │          │
│  │  Sentiment   │─▶│   Trading    │◀─│     Bot      │          │
│  │     Bot      │  │     Bot      │  │   (LSTM)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                 │                  │                   │
│         └─────────────────┼──────────────────┘                   │
│                           │                                      │
│                  ┌────────▼────────┐                             │
│                  │  Shared Volume  │                             │
│                  │ /shared_data    │                             │
│                  └─────────────────┘                             │
│                           │                                      │
│         ┌─────────────────┼─────────────────┐                    │
│         │                 │                 │                    │
│  ┌──────▼─────┐  ┌────────▼────────┐  ┌────▼────┐               │
│  │ PostgreSQL │  │   Dashboard     │  │  Redis  │               │
│  │ (Supabase) │  │  (React/Vite)   │  │  Cache  │               │
│  └────────────┘  └─────────────────┘  └─────────┘               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Services Breakdown

### 1. Morgans Sentiment Bot
**Purpose**: VADER + FinBERT sentiment analysis for stocks
**Tech**: Python, transformers, VADER
**Outputs**: Sentiment scores to `/shared_data/stocks/`
**Schedule**: Runs every 15 minutes

### 2. Financio Trading Bot
**Purpose**: Multi-bot trading system with ML ensemble
**Tech**: Python, XGBoost, scikit-learn, Alpaca API
**Inputs**: Sentiment from shared_data, market data
**Outputs**: Trades to PostgreSQL

### 3. Predictive Bot (LSTM)
**Purpose**: Deep learning price predictions
**Tech**: Python, PyTorch/TensorFlow, LSTM models
**Inputs**: Historical prices, sentiment data
**Outputs**: Price predictions to ensemble model

### 4. Dashboard
**Purpose**: Real-time monitoring and control UI
**Tech**: React, TypeScript, Vite, TailwindCSS
**Ports**: 8080 (production)

### 5. PostgreSQL (Supabase)
**Purpose**: Central database for trades, users, portfolios
**Tech**: PostgreSQL 15+
**Volumes**: Persistent storage for data

### 6. Redis
**Purpose**: Real-time pub/sub, caching, bot coordination
**Tech**: Redis 7+
**Use cases**: Trade signals, sentiment cache, bot status

## Docker Compose Structure

```yaml
version: '3.8'

services:
  # Database
  postgres:
    - Persistent volume for data
    - Health checks
    - Port: 5432

  # Cache/Pub-Sub
  redis:
    - Persistent volume for data
    - Port: 6379
    - Pub/sub for real-time events

  # Sentiment Analysis
  morgans-bot:
    - Scheduled execution (cron)
    - Outputs to shared_data volume
    - Environment: API keys for news sources

  # Trading Engine
  financio-bot:
    - Multi-bot orchestration
    - Reads from shared_data
    - Writes to PostgreSQL
    - Environment: Alpaca keys, trading config

  # Price Prediction
  predictive-bot:
    - LSTM model inference
    - GPU support (optional)
    - Outputs predictions

  # Frontend
  dashboard:
    - Nginx server for static files
    - Port: 8080
    - Connects to PostgreSQL and Redis

volumes:
  shared_data:
    - /shared_data/stocks (sentiment CSVs, JSON)
    - /shared_data/models (trained models)
    - /shared_data/predictions (LSTM outputs)

  postgres_data:
    - Database persistence

  redis_data:
    - Cache persistence
```

## Environment Variables

### Shared (All Services)
```bash
ENVIRONMENT=production
TZ=America/New_York
LOG_LEVEL=INFO
```

### Financio Bot
```bash
ALPACA_API_KEY=your_key
ALPACA_SECRET_KEY=your_secret
TRADING_MODE=paper  # or live
SUPABASE_URL=http://postgres:5432
SUPABASE_KEY=your_key
REDIS_URL=redis://redis:6379
```

### Morgans Bot
```bash
NEWS_API_KEY=your_key
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
TWITTER_BEARER_TOKEN=your_token
OUTPUT_DIR=/shared_data/stocks
```

### Dashboard
```bash
VITE_API_URL=http://financio-bot:8001
VITE_SUPABASE_URL=http://postgres:5432
VITE_WS_URL=ws://redis:6379
```

## Deployment Steps

### 1. Prepare Environment
```bash
# Clone repositories
cd ~/projects
git clone <financio-repo>
git clone <morgans-repo>

# Create shared .env file
cp .env.template .env.production
# Edit with production credentials
```

### 2. Build Images
```bash
# Build all services
docker-compose -f docker-compose.production.yml build

# Or build individually
docker build -t financio-bot:latest -f docker/Dockerfile.financio .
docker build -t morgans-bot:latest -f docker/Dockerfile.morgans ../Morgans
docker build -t dashboard:latest -f docker/Dockerfile.frontend ./dashboard
```

### 3. Deploy Stack
```bash
# Start all services
docker-compose -f docker-compose.production.yml up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f financio-bot
docker-compose logs -f morgans-bot
```

### 4. Initialize Database
```bash
# Run migrations
docker-compose exec financio-bot python -m alembic upgrade head

# Seed initial data
docker-compose exec postgres psql -U financio -d financio_db -f /seed.sql
```

### 5. Monitor System
```bash
# Access dashboard
open http://localhost:8080

# Monitor bot status
docker-compose exec financio-bot python check_bot_status.py

# View Redis pub/sub
docker-compose exec redis redis-cli monitor
```

## Resource Requirements

### Minimum (Paper Trading)
- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 50GB SSD

### Recommended (Live Trading)
- **CPU**: 8 cores (16 threads)
- **RAM**: 16GB
- **Storage**: 100GB NVMe SSD
- **GPU**: Optional (for LSTM training)

### Production (Multi-Bot, High Frequency)
- **CPU**: 16 cores (32 threads)
- **RAM**: 32GB
- **Storage**: 500GB NVMe SSD
- **GPU**: NVIDIA T4 or better (for real-time LSTM)
- **Network**: Low-latency connection (<10ms to Alpaca)

## Data Volumes

### /shared_data Structure
```
shared_data/
├── stocks/
│   ├── {TICKER}_sentiment.csv       # Historical sentiment
│   ├── {TICKER}_combined_latest.json # Latest sentiment
│   └── sentiment_summary.json       # Aggregated stats
├── models/
│   ├── {TICKER}/
│   │   ├── booster.json             # XGBoost model
│   │   ├── scaler.pkl               # Feature scaler
│   │   └── metadata.json            # Model info
│   └── lstm/
│       ├── {TICKER}_lstm.pt         # PyTorch model
│       └── config.json              # LSTM config
└── predictions/
    ├── {TICKER}_predictions.csv     # LSTM predictions
    └── ensemble_signals.json        # Combined signals
```

## Networking

### Internal Network
All services on `financio_network` (bridge)
- Services communicate by service name
- No external exposure except dashboard

### External Exposure
- Dashboard: Port 8080 → Public
- PostgreSQL: Port 5432 → Local only (SSH tunnel)
- Redis: Port 6379 → Internal only

## Security Considerations

### 1. Secrets Management
```bash
# Use Docker secrets
docker secret create alpaca_api_key ./secrets/alpaca_key.txt
docker secret create supabase_key ./secrets/supabase_key.txt
```

### 2. Network Isolation
- Trading bots in private subnet
- Dashboard in DMZ
- Database access restricted

### 3. API Key Rotation
```bash
# Rotate keys without downtime
docker-compose exec financio-bot python rotate_api_keys.py
docker-compose restart financio-bot
```

### 4. Backup Strategy
```bash
# Automated backups
docker-compose exec postgres pg_dump financio_db > backup_$(date +%Y%m%d).sql

# Volume backups
docker run --rm -v shared_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/shared_data_$(date +%Y%m%d).tar.gz /data
```

## Monitoring & Alerts

### 1. Health Checks
```yaml
healthcheck:
  test: ["CMD", "python", "health_check.py"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 2. Logging
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 3. Metrics Collection
- Prometheus for metrics
- Grafana for dashboards
- Alert rules for critical errors

## Scaling Options

### Horizontal Scaling (Multiple Bots)
```bash
# Scale trading bots
docker-compose up -d --scale financio-bot=5

# Each bot handles different tickers
# Coordinated via Redis pub/sub
```

### Vertical Scaling (More Resources)
```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 8G
    reservations:
      cpus: '2'
      memory: 4G
```

## CI/CD Pipeline

### 1. Build & Test
```bash
# GitHub Actions
- Build Docker images
- Run unit tests
- Run integration tests
- Security scan (Trivy)
```

### 2. Deploy
```bash
# On successful build
- Tag images with version
- Push to registry
- Deploy to production
- Run smoke tests
```

### 3. Rollback
```bash
# Quick rollback
docker-compose pull  # Get previous version
docker-compose up -d
```

## Cost Estimation

### AWS (us-east-1)
- **EC2**: t3.2xlarge ($0.33/hr) = ~$240/month
- **EBS**: 500GB SSD ($50/month)
- **Data Transfer**: ~$20/month
- **Total**: ~$310/month

### DigitalOcean
- **Droplet**: 8GB/4CPU ($48/month)
- **Volume**: 100GB ($10/month)
- **Total**: ~$58/month

### Self-Hosted
- **Initial**: $2000-5000 (hardware)
- **Monthly**: $20-50 (electricity)
- **Break-even**: 6-12 months

## Next Steps

1. ✅ Create Dockerfile for each service
2. ✅ Create docker-compose.production.yml
3. ✅ Setup shared volumes
4. ✅ Configure environment variables
5. ✅ Test on local machine
6. ✅ Deploy to production server
7. ✅ Setup monitoring and alerts
8. ✅ Document deployment procedures

## Maintenance

### Daily
- Check bot health status
- Monitor error logs
- Verify trade execution

### Weekly
- Review performance metrics
- Update sentiment data freshness
- Backup database

### Monthly
- Retrain ML models
- Review and optimize strategies
- Update dependencies

---

**Ready to implement?** Let's start with creating the Dockerfiles for each service!
