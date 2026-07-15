# Deployment to Server - Complete Checklist

## Files You Need (Minimal Package)

### ✅ What TO Copy

```
Financio-V2/
├── docker/
│   ├── Dockerfile.financio-bot       # Trading bot image
│   ├── Dockerfile.morgans-bot        # Sentiment bot image
│   └── Dockerfile.frontend           # Dashboard image
├── financio_src/                     # Core trading logic
├── backend/                          # API server
├── dashboard/src/                    # Dashboard source (NOT dist/)
├── supabase/migrations/              # Database schema
├── scripts/
│   ├── deploy-full-stack.sh         # Deployment automation
│   └── monitor-system.sh            # Monitoring
├── docker-compose.full-stack.yml    # Main orchestration
├── requirements.txt                 # Python dependencies
├── .env.production.template         # Config template
└── docs/DOCKER_DEPLOYMENT_GUIDE.md  # Setup guide
```

**Total Size**: ~50-100MB (without models/data)

### ❌ What NOT to Copy

```
❌ .git/                  # Git history (large, not needed)
❌ .venv/                 # Virtual environment (rebuild on server)
❌ node_modules/          # NPM packages (rebuild on server)
❌ models/                # ML models (large, use volumes or download)
❌ shared_data/           # Runtime data (created on server)
❌ logs/                  # Log files
❌ backups/               # Backup files
❌ test_*.py              # Test scripts
❌ *.ipynb                # Jupyter notebooks
❌ dashboard/dist/        # Build artifacts (rebuild on server)
❌ reports/               # Generated reports
❌ .env                   # Local environment (has secrets!)
❌ __pycache__/           # Python cache
❌ *.pyc, *.pyo          # Compiled Python
```

## Two Ways to Deploy

### Option 1: Use Deployment Package Script (Recommended)

```bash
# On your local machine
cd /Users/mosley/projects/Financio-V2

# Create clean package
./scripts/create-deployment-package.sh

# This creates: financio-deployment-YYYYMMDD-HHMMSS.tar.gz (~50MB)

# Copy to server
scp financio-deployment-*.tar.gz user@your-server:/opt/

# On server
ssh user@your-server
cd /opt
tar xzf financio-deployment-*.tar.gz
cd financio-deployment-*
cp .env.production.template .env.production
nano .env.production  # Add your API keys
./scripts/deploy-full-stack.sh
```

**Pros**:
- ✅ Only includes necessary files
- ✅ Single ~50MB archive
- ✅ Fast transfer
- ✅ Clean structure

### Option 2: Direct rsync (Advanced)

```bash
# On your local machine
rsync -avz \
  --exclude='.git' \
  --exclude='.venv' \
  --exclude='node_modules' \
  --exclude='models' \
  --exclude='shared_data' \
  --exclude='logs' \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  --exclude='dashboard/dist' \
  --exclude='.env' \
  /Users/mosley/projects/Financio-V2/ \
  user@your-server:/opt/financio/

# On server
ssh user@your-server
cd /opt/financio
cp .env.production.template .env.production
nano .env.production  # Add API keys
./scripts/deploy-full-stack.sh
```

**Pros**:
- ✅ Can sync updates easily
- ✅ Preserves file permissions
- ✅ Can resume interrupted transfers

## Pre-Deployment Checklist

### On Your Local Machine

- [ ] Test locally with Docker
  ```bash
  ./scripts/deploy-full-stack.sh
  ```

- [ ] Verify all required files exist
  ```bash
  ls docker/Dockerfile.*
  ls docker-compose.full-stack.yml
  ls scripts/deploy-full-stack.sh
  ```

- [ ] Create deployment package
  ```bash
  ./scripts/create-deployment-package.sh
  ```

- [ ] Note package size (should be <100MB)

### On Your Server

- [ ] Install Docker
  ```bash
  docker --version  # Should be 20.10+
  docker-compose --version  # Should be 2.0+
  ```

- [ ] Check resources
  ```bash
  free -h  # At least 8GB RAM
  df -h    # At least 50GB free space
  nproc    # At least 4 CPU cores
  ```

- [ ] Create deployment directory
  ```bash
  sudo mkdir -p /opt/financio
  sudo chown $USER:$USER /opt/financio
  ```

### API Keys & Credentials

- [ ] Alpaca API Key (required)
  - Get from: https://alpaca.markets
  - Paper trading is free
  - Save: `ALPACA_API_KEY` and `ALPACA_SECRET_KEY`

- [ ] NewsAPI Key (required for sentiment)
  - Get from: https://newsapi.org
  - Free tier: 100 requests/day
  - Save: `NEWS_API_KEY`

- [ ] Database Password (required)
  - Generate strong password
  - Save: `POSTGRES_PASSWORD`

- [ ] Redis Password (required)
  - Generate strong password
  - Save: `REDIS_PASSWORD`

- [ ] Optional: Reddit API
  - Get from: https://www.reddit.com/prefs/apps
  - Save: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`

- [ ] Optional: Twitter API
  - Get from: https://developer.twitter.com
  - Save: `TWITTER_BEARER_TOKEN`

## Deployment Steps

### 1. Transfer Package

```bash
# Copy package to server
scp financio-deployment-*.tar.gz user@server:/opt/

# Or use rsync for resumable transfer
rsync -avz --progress financio-deployment-*.tar.gz user@server:/opt/
```

### 2. Extract on Server

```bash
ssh user@server
cd /opt
tar xzf financio-deployment-*.tar.gz
cd financio-deployment-*
```

### 3. Configure Environment

```bash
# Copy template
cp .env.production.template .env.production

# Edit with your API keys
nano .env.production

# Or use sed for quick edits
sed -i 's/your_alpaca_key/YOUR_ACTUAL_KEY/' .env.production
```

### 4. Deploy

```bash
# Make sure scripts are executable
chmod +x scripts/*.sh

# Run deployment
./scripts/deploy-full-stack.sh
```

The script will:
- ✅ Build Docker images (~10-15 minutes)
- ✅ Initialize database
- ✅ Start all services
- ✅ Run health checks
- ✅ Display status

### 5. Verify

```bash
# Check all services are running
docker-compose -f docker-compose.full-stack.yml ps

# Should show:
# financio-postgres       Up (healthy)
# financio-redis          Up (healthy)
# financio-morgans        Up
# financio-trading-bot    Up (healthy)
# financio-dashboard      Up

# Test dashboard
curl http://localhost:8080

# View logs
docker-compose -f docker-compose.full-stack.yml logs -f
```

## Post-Deployment

### Monitor System

```bash
# Run monitoring dashboard
./scripts/monitor-system.sh

# Or check individual services
docker-compose -f docker-compose.full-stack.yml logs -f financio-bot
```

### Verify Sentiment Data

```bash
# Check sentiment files are being created
ls -lh shared_data/stocks/

# Should see:
# *_sentiment.csv files (historical data)
# *_combined_latest.json files (current data)
```

### Test Trading (Paper Mode)

```bash
# Check trading bot logs
docker-compose -f docker-compose.full-stack.yml logs financio-bot | grep -i "trade"

# Should see trade executions or signals
```

### Access Dashboard

```bash
# From server
curl http://localhost:8080

# From your computer (if server has public IP)
open http://YOUR_SERVER_IP:8080
```

## Troubleshooting

### Package Too Large?

```bash
# Check what's in the package
tar tzf financio-deployment-*.tar.gz | head -50

# Recreate if needed
./scripts/create-deployment-package.sh
```

### Transfer Failed?

```bash
# Use rsync for resumable transfer
rsync -avz --partial --progress \
  financio-deployment-*.tar.gz \
  user@server:/opt/
```

### Out of Disk Space?

```bash
# Clean Docker cache
docker system prune -a --volumes

# Check space
df -h
```

### Services Won't Start?

```bash
# Check logs
docker-compose -f docker-compose.full-stack.yml logs

# Verify .env.production
cat .env.production | grep -v '^#' | grep -v '^$'

# Check resources
docker stats
```

## File Size Reference

```
Deployment Package:           ~50-100 MB
  ├── Source Code:           ~20 MB
  ├── Dashboard Source:      ~10 MB
  ├── Docker Configs:        ~1 MB
  └── Scripts/Docs:          ~5 MB

After Deployment:            ~5-10 GB
  ├── Docker Images:         ~3-4 GB
  ├── Database:              ~100 MB (grows)
  ├── Sentiment Data:        ~500 MB (grows)
  └── Logs:                  ~100 MB (rotates)

Optional (not in package):
  ├── ML Models:             ~2-5 GB
  └── Historical Data:       ~10-50 GB
```

## Updates

To update an existing deployment:

```bash
# Create new package with updates
./scripts/create-deployment-package.sh

# Copy to server
scp financio-deployment-*.tar.gz user@server:/opt/

# On server - backup first!
cd /opt/financio-deployment-*
docker-compose -f docker-compose.full-stack.yml down
cd ..
tar xzf financio-deployment-NEW.tar.gz
cd financio-deployment-NEW
# Copy old .env.production
cp ../financio-deployment-OLD/.env.production .
./scripts/deploy-full-stack.sh
```

---

**Ready to deploy?** Start with Option 1 (deployment package script) - it's the cleanest! 🚀
