# Financio Multi-Bot Docker Deployment

This directory contains optimized Docker configurations for the Financio multi-bot trading system.

## 🚀 Quick Start

```bash
# 1. Build the optimized Docker image
./deploy.sh build

# 2. Start all services (Redis + Multi-Bot)
./deploy.sh start

# 3. Check service status and health
./deploy.sh status
```

## 📦 What's Included

- **Optimized Docker Image**: 2.67GB multi-bot container with all dependencies
- **Redis Cache**: Fast signal processing and inter-bot communication
- **Health Monitoring**: Automatic health checks and service recovery
- **Production Ready**: Complete orchestration with Docker Compose

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Multi-Bot     │    │     Redis       │
│   Container     │◄──►│   Container     │
│                 │    │                 │
│ • 48 Trading    │    │ • Signal Cache  │
│   Bots          │    │ • Message Queue │
│ • 16 Tickers    │    │ • Session Store │
│ • 3 Strategies  │    │                 │
└─────────────────┘    └─────────────────┘
         │
         ▼
    Host Network
    :8000 - API
    :8083 - Dashboard
    :6379 - Redis
```

## 🔧 Files Overview

| File | Purpose |
|------|---------|
| `Dockerfile.multibot` | Optimized multi-bot container |
| `docker-compose.yml` | Production orchestration |
| `../deploy.sh` | Automated deployment script |

## 📊 Service Endpoints

- **API Health**: http://localhost:8000/health
- **Dashboard**: http://localhost:8083
- **Multi-Bot Status**: http://localhost:8000/api/multi-bot/status
- **Live Signals**: http://localhost:8000/api/multi-bot/signals/{ticker}

## 🛠️ Available Commands

```bash
./deploy.sh build     # Build optimized image
./deploy.sh start     # Start all services
./deploy.sh stop      # Stop all services
./deploy.sh restart   # Restart services
./deploy.sh status    # Health & resource usage
./deploy.sh logs      # Follow container logs
./deploy.sh cleanup   # Clean up resources
```

## 🔍 Troubleshooting

### Check Service Status
```bash
./deploy.sh status
```

### View Logs
```bash
./deploy.sh logs
```

### Test Container Functionality
```bash
# Test imports and basic functionality
docker run --rm financio-multibot:optimized python -c "
import financio_src
print('✅ Container is working correctly')
"
```

### Manual Container Management
```bash
# Build manually
docker build -f docker/Dockerfile.multibot -t financio-multibot:optimized .

# Run manually
docker run -d --name financio-multibot -p 8000:8000 -p 8083:8083 financio-multibot:optimized
```

## 📈 Optimization Results

- **Original Image Size**: 2.73GB
- **Optimized Image Size**: 2.67GB
- **Space Saved**: 60MB (2.2% reduction)
- **All Dependencies**: ✅ Included and verified
- **Multi-Bot System**: ✅ 48 bots across 16 tickers operational

## 🔒 Production Notes

- Health checks ensure automatic recovery
- Redis persistence enabled for data safety
- Logs automatically managed and rotated
- Resource usage monitored and reported

For detailed configuration and advanced usage, see the complete deployment guide in the main documentation.
