# Financio-V2 Docker Deployment Guide

## Quick Start

### Prerequisites
- Docker 20.10+ installed
- Docker Compose 2.0+ installed
- At least 8GB RAM available
- 50GB+ free disk space

### 1. Clone and Setup
```bash
cd /Users/mosley/projects/Financio-V2

# Create production environment file
cp .env.production.template .env.production

# Edit with your API keys
nano .env.production
```

### 2. Required API Keys

You'll need to obtain these keys before deployment:

**Trading (Required)**
- Alpaca Paper Trading: https://alpaca.markets (free)
- OR Alpaca Live Trading: https://alpaca.markets (requires funding)

**Sentiment Analysis (Required)**
- NewsAPI: https://newsapi.org (free tier available)

**Sentiment Analysis (Optional)**
- Reddit API: https://www.reddit.com/prefs/apps
- Twitter API: https://developer.twitter.com
- Alpha Vantage: https://www.alphavantage.co

**Database**
- Option 1: Use included PostgreSQL (default)
- Option 2: Supabase Cloud: https://supabase.com (free tier)

### 3. Deploy

```bash
# Make deployment script executable
chmod +x scripts/deploy-full-stack.sh

# Run deployment
./scripts/deploy-full-stack.sh
```

The script will:
1. ✅ Check prerequisites
2. ✅ Build Docker images
3. ✅ Initialize database
4. ✅ Start all services
5. ✅ Run health checks
6. ✅ Display status

### 4. Access the System

Once deployed, access:

- **Dashboard**: http://localhost:8080
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Architecture

```
┌─────────────────────────────────────────┐
│         Docker Host Machine             │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │   Docker Compose Network          │ │
│  │                                   │ │
│  │  ┌─────────┐  ┌──────────┐       │ │
│  │  │Sentiment│  │ Trading  │       │ │
│  │  │   Bot   │─▶│   Bot    │       │ │
│  │  └─────────┘  └──────────┘       │ │
│  │       │             │             │ │
│  │       ▼             ▼             │ │
│  │  ┌─────────────────────┐         │ │
│  │  │   Shared Volume     │         │ │
│  │  │   /shared_data      │         │ │
│  │  └─────────────────────┘         │ │
│  │       │             │             │ │
│  │  ┌────▼───┐    ┌───▼────┐        │ │
│  │  │ Redis  │    │Postgres│        │ │
│  │  └────────┘    └────────┘        │ │
│  │                     │             │ │
│  │                ┌────▼────┐        │ │
│  │                │Dashboard│        │ │
│  │                └─────────┘        │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Service Details

### Morgans Sentiment Bot
- **Image**: Custom built from `../Morgans`
- **Function**: Collects and analyzes sentiment from news & social media
- **Output**: Saves to `/shared_data/stocks/`
- **Schedule**: Runs every 15 minutes
- **Resources**: 2 CPU, 4GB RAM

### Financio Trading Bot
- **Image**: Built from current directory
- **Function**: Executes trades based on ML ensemble + sentiment
- **Input**: Reads from `/shared_data/stocks/`
- **Database**: Writes trades to PostgreSQL
- **Resources**: 4 CPU, 8GB RAM

### PostgreSQL Database
- **Version**: PostgreSQL 15
- **Purpose**: Stores trades, users, portfolios
- **Persistence**: Volume `postgres_data`
- **Resources**: 2 CPU, 4GB RAM

### Redis Cache
- **Version**: Redis 7
- **Purpose**: Caching, pub/sub messaging
- **Persistence**: Volume `redis_data`
- **Resources**: 1 CPU, 2GB RAM

### React Dashboard
- **Tech**: React + Vite + TailwindCSS
- **Port**: 8080
- **Purpose**: Real-time monitoring and control
- **Resources**: 0.5 CPU, 512MB RAM

## Management Commands

### View Logs
```bash
# All services
docker-compose -f docker-compose.full-stack.yml logs -f

# Specific service
docker-compose -f docker-compose.full-stack.yml logs -f financio-bot
docker-compose -f docker-compose.full-stack.yml logs -f morgans-bot
```

### Monitor System
```bash
# Run monitoring dashboard
./scripts/monitor-system.sh
```

### Restart Services
```bash
# Restart all
docker-compose -f docker-compose.full-stack.yml restart

# Restart specific service
docker-compose -f docker-compose.full-stack.yml restart financio-bot
```

### Scale Trading Bots
```bash
# Run 3 trading bot instances
docker-compose -f docker-compose.full-stack.yml up -d --scale financio-bot=3
```

### Stop System
```bash
# Stop all services (keeps data)
docker-compose -f docker-compose.full-stack.yml down

# Stop and remove volumes (deletes data!)
docker-compose -f docker-compose.full-stack.yml down -v
```

## Troubleshooting

### Service Won't Start

1. Check logs:
```bash
docker-compose -f docker-compose.full-stack.yml logs [service-name]
```

2. Verify environment variables:
```bash
docker-compose -f docker-compose.full-stack.yml config
```

3. Check resource availability:
```bash
docker stats
```

### Sentiment Data Not Updating

1. Check Morgans bot is running:
```bash
docker-compose -f docker-compose.full-stack.yml ps morgans-bot
```

2. Verify API keys are set:
```bash
docker-compose -f docker-compose.full-stack.yml exec morgans-bot env | grep API
```

3. Check shared volume:
```bash
ls -lh shared_data/stocks/
```

### Database Connection Issues

1. Verify PostgreSQL is healthy:
```bash
docker-compose -f docker-compose.full-stack.yml exec postgres pg_isready
```

2. Check connection string:
```bash
docker-compose -f docker-compose.full-stack.yml exec financio-bot env | grep SUPABASE_URL
```

3. Test connection:
```bash
docker-compose -f docker-compose.full-stack.yml exec postgres psql -U financio -d financio_db -c "SELECT 1;"
```

### High Resource Usage

1. Check resource allocation:
```bash
docker stats --no-stream
```

2. Adjust limits in `docker-compose.full-stack.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '2'  # Reduce from 4
      memory: 4G  # Reduce from 8G
```

3. Restart services:
```bash
docker-compose -f docker-compose.full-stack.yml up -d
```

## Backup & Restore

### Backup Database
```bash
# Create backup
docker-compose -f docker-compose.full-stack.yml exec -T postgres \
  pg_dump -U financio financio_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Or use the backup script
./scripts/backup-database.sh
```

### Restore Database
```bash
# Restore from backup
docker-compose -f docker-compose.full-stack.yml exec -T postgres \
  psql -U financio -d financio_db < backup_20260103_120000.sql
```

### Backup Shared Data
```bash
# Tar up shared data directory
tar czf shared_data_backup_$(date +%Y%m%d).tar.gz shared_data/
```

## Production Deployment

### On AWS EC2

1. **Launch Instance**
   - Instance Type: t3.2xlarge (8 vCPU, 32GB RAM)
   - Storage: 100GB GP3 SSD
   - Security Group: Allow 8080, 22

2. **Install Docker**
```bash
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Deploy**
```bash
git clone <your-repo>
cd Financio-V2
cp .env.production.template .env.production
# Edit .env.production with production keys
./scripts/deploy-full-stack.sh
```

### On DigitalOcean Droplet

Similar to AWS, but use:
- Droplet: 8GB/4 CPU ($48/month)
- Volume: 100GB Block Storage ($10/month)

### Self-Hosted Server

Requirements:
- Ubuntu 22.04 LTS or similar
- Docker & Docker Compose installed
- Static IP or DDNS
- Port forwarding for dashboard (8080)

## Security Best Practices

### 1. API Keys
- Never commit `.env.production` to git
- Use strong, unique passwords
- Rotate keys regularly
- Use environment variables, not hardcoded values

### 2. Network Security
```yaml
# Expose only dashboard to public
ports:
  - "8080:80"  # Dashboard only

# PostgreSQL and Redis internal only
# No external ports exposed
```

### 3. Container Security
- Run as non-root user (already configured)
- Use official base images only
- Keep images updated
- Scan for vulnerabilities

### 4. Database Security
- Strong PostgreSQL password
- Enable SSL for production
- Regular backups
- Limit connection access

## Monitoring & Alerts

### Built-in Monitoring
```bash
# Real-time dashboard
./scripts/monitor-system.sh
```

### External Monitoring (Optional)

Add Prometheus + Grafana:
```bash
# Add to docker-compose.full-stack.yml
prometheus:
  image: prom/prometheus
  ...

grafana:
  image: grafana/grafana
  ...
```

## Performance Tuning

### For High-Frequency Trading
1. Use SSD/NVMe storage
2. Increase bot instances: `--scale financio-bot=5`
3. Use Redis for hot data
4. Optimize database indexes

### For Cost Optimization
1. Reduce resource limits
2. Use spot instances on cloud
3. Scale down during off-market hours
4. Use compression for logs

## Support

For issues:
1. Check logs first
2. Review this guide
3. Check GitHub issues
4. Create new issue with logs

## Next Steps

After successful deployment:
1. ✅ Monitor initial trades (paper trading)
2. ✅ Verify sentiment data updates
3. ✅ Review dashboard metrics
4. ✅ Test alerts and notifications
5. ✅ Backtest with historical data
6. ✅ Switch to live trading (when ready)

---

**Happy Trading! 🚀📈**
