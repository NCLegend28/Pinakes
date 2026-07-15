# 🐳 Financio-V2 Docker Architecture Documentation

## Overview

The Financio-V2 trading platform uses a sophisticated Docker architecture with multiple specialized containers designed for different deployment scenarios. This document provides a comprehensive overview of each Docker image, their contents, and how they work together to create a scalable, maintainable trading system.

## 📦 Docker Images Catalog

### 1. **Production Image** (`Dockerfile.production`)
**Purpose**: Complete full-stack deployment in a single optimized container  
**Base**: `python:3.10-alpine` with multi-stage build  
**Size**: ~4.2GB (optimized)  

**Contents:**
- ✅ **Frontend**: React dashboard (built and served via Python)
- ✅ **Backend**: FastAPI REST API server
- ✅ **Multi-Bot System**: 48 trading bots across 16 tickers
- ✅ **ML Models**: Pre-trained models for signal generation
- ✅ **Dependencies**: All Python ML libraries + Node.js build tools

**Key Features:**
- Multi-stage build for size optimization
- Alpine Linux for security and performance
- Built-in health checks
- Production-optimized configurations

**Use Cases:**
- Single-server deployments
- Quick production setup
- Development/staging environments
- Resource-constrained deployments

---

### 2. **Backend-Only Image** (`Dockerfile.backend`)
**Purpose**: Lightweight API server for microservices architecture  
**Base**: `python:3.11-slim`  
**Size**: ~2.96GB  

**Contents:**
- ✅ **FastAPI Backend**: REST API server
- ✅ **Trading Logic**: Core trading algorithms
- ✅ **ML Dependencies**: scikit-learn, pandas, numpy
- ✅ **Database**: SQLite with trading data
- ❌ **Frontend**: Not included (served separately)

**Key Features:**
- Optimized for API performance
- Health checks on `/api/dashboard-data`
- Uvicorn ASGI server
- Environment-based configuration

**Use Cases:**
- Microservices deployments
- API-only services
- Horizontal scaling scenarios
- Load-balanced environments

---

### 3. **Frontend-Only Image** (`Dockerfile.frontend`)
**Purpose**: Static file server with React dashboard  
**Base**: `nginx:alpine` with multi-stage build  
**Size**: ~82.5MB  

**Contents:**
- ✅ **React Dashboard**: Built production assets
- ✅ **Nginx Server**: High-performance web server
- ✅ **Static Assets**: CSS, JS, images
- ❌ **Backend Logic**: Not included (API calls to backend)

**Key Features:**
- Extremely lightweight
- Nginx for optimal static file serving
- Health checks on root path
- Production build optimizations

**Use Cases:**
- CDN deployments
- Separate frontend scaling
- Static asset optimization
- Multi-region deployments

---

### 4. **Multi-Bot System Image** (`Dockerfile.multibot`)
**Purpose**: Specialized container for the multi-bot trading system  
**Base**: `python:3.11-slim`  
**Size**: 2.67GB (optimized from 2.73GB)  

**Contents:**
- ✅ **48 Trading Bots**: ML, Trend, Hybrid strategies
- ✅ **16 Tickers**: Major stocks and crypto
- ✅ **Signal Processing**: Real-time signal generation
- ✅ **Ensemble Logic**: Multi-bot decision aggregation
- ✅ **ML Models**: Stable-baselines3, scikit-learn
- ✅ **Redis Integration**: Fast inter-bot communication

**Key Features:**
- Optimized for trading performance
- Real-time signal processing
- Ensemble decision making
- Multi-strategy support
- Redis-based communication

**Use Cases:**
- Automated trading systems
- Signal generation services
- Multi-strategy deployments
- Real-time trading environments

---

### 5. **Individual Trading Bot Image** (`Dockerfile.trading`)
**Purpose**: Single bot container for distributed trading  
**Base**: `python:3.10-alpine`  
**Size**: ~2.5GB  

**Contents:**
- ✅ **Single Bot Instance**: Configurable strategy
- ✅ **Trading Logic**: Core trading algorithms
- ✅ **ML Dependencies**: Required ML libraries
- ✅ **Models**: Strategy-specific models
- ❌ **Multi-Bot Logic**: Single bot focus

**Key Features:**
- Lightweight single-purpose container
- Environment-based bot configuration
- Alpine Linux for efficiency
- Strategy-specific deployments

**Use Cases:**
- Distributed bot deployments
- Strategy-specific scaling
- A/B testing different strategies
- Resource isolation per bot

---

### 6. **Development Image** (`Dockerfile.development`)
**Purpose**: Development environment with debugging tools  
**Base**: `python:3.10-alpine`  
**Size**: ~3GB (includes dev tools)  

**Contents:**
- ✅ **Complete Development Stack**: Backend + frontend tools
- ✅ **Debugging Tools**: IDE integration, debugger
- ✅ **Hot Reloading**: Live code updates
- ✅ **Development Utilities**: git, vim, htop, redis-cli
- ✅ **Node.js**: For frontend development

**Key Features:**
- Source code mounting for live updates
- Debug port exposure
- Development utilities included
- Redis included for local testing

**Use Cases:**
- Local development
- Debugging and testing
- Feature development
- Code testing environments

---

### 7. **Alpha Release Image** (`Dockerfile.alpha`)
**Purpose**: Alpha version deployment for testing  
**Base**: `python:3.10-alpine` with multi-stage build  
**Size**: ~4.2GB  

**Contents:**
- ✅ **Alpha Features**: Latest experimental features
- ✅ **Full Stack**: Frontend + backend + trading
- ✅ **Testing Tools**: Additional testing capabilities
- ✅ **Debug Information**: Enhanced logging

**Key Features:**
- Latest feature integration
- Enhanced monitoring
- Alpha-specific configurations
- Testing-friendly setup

**Use Cases:**
- Alpha testing deployments
- Feature testing
- Beta user environments
- Pre-production testing

---

### 8. **Multi-Account Trading Bot Image** (`Dockerfile.trading-bot`)
**Purpose**: Configurable bot instance for different trading accounts and modes  
**Base**: `python:3.11-slim`  
**Size**: ~2.5GB  

**Contents:**
- ✅ **Configurable Trading Bot**: Environment-based configuration
- ✅ **Multi-Strategy Support**: ML, Trend, Hybrid strategies
- ✅ **Account Isolation**: Separate credentials and databases
- ✅ **Enhanced Risk Management**: Environment-specific risk parameters
- ✅ **Configuration Manager**: Dynamic configuration loading

**Key Features:**
- Environment-based bot configuration
- Support for paper/live trading modes
- Isolated databases per account type
- Credential management via environment variables
- Strategy-specific parameter tuning

**Use Cases:**
- Paper trading for strategy testing
- Live trading with separate accounts
- Strategy validation and A/B testing
- Multi-account portfolio management

---

## 🏗️ Architecture Patterns

### Pattern 1: **Monolithic Production** (Recommended for small-medium deployments)
```
┌─────────────────────────────────────┐
│        Production Container         │
│                                     │
│  ┌─────────┐  ┌─────────┐  ┌──────┐│
│  │Frontend │  │Backend  │  │Multi-│││
│  │(React)  │  │(FastAPI)│  │Bot   │││
│  │         │  │         │  │System│││
│  └─────────┘  └─────────┘  └──────┘│
└─────────────────────────────────────┘
              │
              ▼
        ┌───────────┐
        │   Redis   │
        │   Cache   │
        └───────────┘
```

**Docker Compose**: `docker-compose.production.yml`

**Services:**
- `financio-app`: Single production container
- `redis`: Cache and message queue

**Scaling**: Vertical scaling (add more CPU/RAM)

---

### Pattern 2: **Microservices** (Recommended for large deployments)
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Frontend   │  │   Backend   │  │ Multi-Bot   │
│ Container   │  │ Container   │  │ Container   │
│             │  │             │  │             │
│ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │
│ │ React   │ │  │ │FastAPI  │ │  │ │48 Bots  │ │
│ │Dashboard│ │◄─┤ │REST API │ │◄─┤ │ │Signal   │ │
│ │         │ │  │ │         │ │  │ │Gen      │ │
│ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │
└─────────────┘  └─────────────┘  └─────────────┘
      │                 │                 │
      └─────────────────┼─────────────────┘
                        ▼
                  ┌───────────┐
                  │   Redis   │
                  │   Cache   │
                  └───────────┘
```

**Docker Compose**: `docker-compose.microservices.yml`

**Services:**
- `frontend`: Nginx + React assets
- `backend`: FastAPI server only
- `multi-bot`: Trading bot system
- `redis`: Shared cache

**Scaling**: Horizontal scaling (add more containers)

---

### Pattern 3: **Development Environment**
```
┌─────────────────────────────────────┐
│      Development Container         │
│                                     │
│  ┌─────────┐  ┌─────────┐  ┌──────┐│
│  │Frontend │  │Backend  │  │Debug │││
│  │(Dev)    │◄─┤(Dev)    │  │Tools │││
│  │         │  │         │  │      │││
│  └─────────┘  └─────────┘  └──────┘│
│       ▲              ▲              │
│       │              │              │
│   Hot Reload    Live Reload         │
└───────┼──────────────┼──────────────┘
        │              │
    ┌───▼───┐      ┌───▼───┐
    │Source │      │Source │
    │Code   │      │Code   │
    │Mount  │      │Mount  │
    └───────┘      └───────┘
```

**Docker Compose**: `docker-compose.development.yml`

**Features:**
- Source code mounting
- Hot reloading
- Debug ports exposed
- Development tools included

---

### Pattern 4: **Multi-Account Trading** (Recommended for professional trading)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Paper Bot     │    │   Live Bot      │    │ Strategy Test   │
│   Container     │    │   Container     │    │   Container     │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Test Acct   │ │    │ │ Live Acct   │ │    │ │ Test Acct   │ │
│ │ Paper API   │ │    │ │ Live API    │ │    │ │ Paper API   │ │
│ │ Safe Params │ │    │ │ Prod Params │ │    │ │ Exp Params  │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                        ┌─────────────────┐
                        │      Redis      │
                        │  Shared Cache   │
                        └─────────────────┘
```

**Docker Compose**: `docker-compose.multi-account.yml`

**Services:**
- `paper-trading-bot`: Paper trading with test credentials
- `live-trading-bot`: Live trading with production credentials
- `strategy-test-bot`: Strategy validation with experimental parameters
- `multi-bot-system`: Advanced multi-bot coordination (optional)
- `redis`: Shared communication layer

**Configuration Management:**
- `.env.paper`: Paper trading configuration
- `.env.live`: Live trading configuration  
- `.env.test`: Strategy testing configuration
- `.env.multibot`: Multi-bot system configuration

**Scaling**: Independent scaling per account type

**Deployment Commands:**
```bash
# Start paper trading
./deploy-bots.sh start-paper

# Start live trading (requires confirmation)
./deploy-bots.sh start-live

# Test new strategy
./deploy-bots.sh start-strategy ml

# Deploy updates to running bots
./deploy-bots.sh deploy-updates
```

---

## 🔄 Multi-Account Deployment Workflow

### Development → Testing → Production Pipeline

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Development   │───▶│  Paper Trading  │───▶│  Live Trading   │
│                 │    │                 │    │                 │
│ • Code changes  │    │ • Strategy test │    │ • Production    │
│ • Local testing │    │ • Paper money   │    │ • Real money    │
│ • Unit tests    │    │ • Risk validation│    │ • Conservative  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Step 1: Development**
```bash
# Build and test locally
./deploy-bots.sh build
./deploy-bots.sh setup
```

**Step 2: Paper Trading Validation**
```bash
# Deploy to paper trading
./deploy-bots.sh start-paper

# Monitor performance
./deploy-bots.sh logs paper
```

**Step 3: Strategy Testing**
```bash
# Test specific strategies
./deploy-bots.sh start-strategy ml
./deploy-bots.sh start-strategy trend

# Compare results
./deploy-bots.sh logs strategy-test
```

**Step 4: Live Trading Deployment**
```bash
# Deploy to live trading (with confirmation)
./deploy-bots.sh start-live

# Monitor closely
./deploy-bots.sh follow live
```

### Update Deployment Process

**Zero-Downtime Updates:**
1. Build new images with changes
2. Test in paper trading environment
3. Validate with strategy testing
4. Deploy to live trading with rolling update

```bash
# Deploy updates to all running bots
./deploy-bots.sh deploy-updates
```

**Rollback Process:**
```bash
# Stop problematic bot
./deploy-bots.sh stop live

# Revert to previous image
docker tag financio-trading-bot:previous financio-trading-bot:latest

# Restart with previous version
./deploy-bots.sh start-live
```

---

## 🔄 Container Communication

### Inter-Container Communication

**1. HTTP API Calls**
- Frontend → Backend: REST API calls
- Multi-Bot → Backend: Signal submission
- External → Backend: API consumption

**2. Redis Pub/Sub**
- Multi-Bot System: Inter-bot communication
- Signal Distribution: Real-time signal sharing
- Cache Layer: Performance optimization

**3. Shared Volumes**
- Log Files: Centralized logging
- Model Files: ML model sharing
- Database Files: SQLite database access

### Network Architecture

```
External Traffic
       │
       ▼
┌─────────────┐
│Load Balancer│ (Optional)
│   (Nginx)   │
└─────────────┘
       │
       ▼
┌─────────────┐    ┌─────────────┐
│  Frontend   │    │   Backend   │
│   :80/443   │◄──►│    :8000    │
└─────────────┘    └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ Multi-Bot   │
                   │   :8083     │
                   └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   Redis     │
                   │   :6379     │
                   └─────────────┘
```

---

## 📊 Resource Requirements

| Image | CPU | RAM | Disk | Network |
|-------|-----|-----|------|---------|
| **Production** | 2-4 cores | 4-8GB | 10GB | Medium |
| **Backend** | 1-2 cores | 2-4GB | 3GB | High |
| **Frontend** | 0.5 cores | 512MB | 1GB | Low |
| **Multi-Bot** | 2-4 cores | 3-6GB | 5GB | Medium |
| **Trading Bot** | 0.5-1 core | 1-2GB | 2GB | Low |
| **Development** | 2 cores | 4GB | 8GB | Medium |

### Scaling Recommendations

**Small Deployment (< 10 users)**
- Use Production image
- Single server deployment
- Basic Redis instance

**Medium Deployment (10-100 users)**
- Use Microservices pattern
- 2-3 backend replicas
- Dedicated Redis cluster

**Large Deployment (100+ users)**
- Full microservices with load balancing
- Horizontal bot scaling
- Redis cluster with persistence
- CDN for frontend assets

---

## 🚀 Deployment Strategies

### Quick Start (Development)
```bash
# Clone and start development environment
git clone <repo>
cd Financio-V2
./deploy.sh build
./deploy.sh start
```

### Production Deployment
```bash
# Production deployment
docker-compose -f docker-compose.production.yml up -d

# Verify deployment
curl http://localhost:10000/api/dashboard-data
curl http://localhost:8080/
```

### Microservices Deployment
```bash
# Scale microservices
docker-compose -f docker-compose.microservices.yml up -d --scale backend=3

# Monitor services
docker-compose ps
docker stats
```

### Multi-Bot Scaling
```bash
# Deploy multi-bot system
./deploy.sh build
./deploy.sh start

# Scale individual bots
docker-compose -f docker/docker-compose.yml up -d --scale financio-multibot=3
```

---

## 🔧 Configuration Management

### Environment Variables

**Common Variables (All Images)**
```env
PYTHONPATH=/app
REDIS_HOST=redis
REDIS_PORT=6379
LOG_LEVEL=INFO
```

**Production Specific**
```env
NODE_ENV=production
FINANCIO_MODE=production
```

**Development Specific**
```env
NODE_ENV=development
DEBUG=true
HOT_RELOAD=true
```

**Multi-Bot Specific**
```env
BOT_COUNT=48
TICKER_COUNT=16
SIGNAL_INTERVAL=30
```

### Volume Management

**Persistent Volumes**
- `financio_logs`: Application logs
- `financio_models`: ML model files
- `financio_data`: Database files
- `redis_data`: Redis persistence

**Mount Points**
- `/app/logs`: Log files
- `/app/models`: ML models
- `/app/financio_src/logs`: Database files

---

## 🔍 Monitoring and Health Checks

### Health Check Endpoints

| Service | Endpoint | Check Type |
|---------|----------|------------|
| Production | `http://localhost:10000/api/dashboard-data` | API Health |
| Backend | `http://localhost:8000/health` | Service Health |
| Frontend | `http://localhost/` | Static Files |
| Multi-Bot | `http://localhost:8000/api/multi-bot/status` | Bot Status |
| Redis | `redis-cli ping` | Cache Health |

### Monitoring Strategy

**Application Metrics**
- Bot performance and signal accuracy
- API response times
- Trading success rates
- Resource utilization

**Infrastructure Metrics**
- Container CPU/RAM usage
- Network throughput
- Disk I/O and space
- Redis performance

**Business Metrics**
- Portfolio performance
- Trade execution success
- Risk management effectiveness
- User engagement

---

## 🔒 Security Considerations

### Container Security
- Alpine Linux base images for minimal attack surface
- Non-root user execution
- Read-only file systems where possible
- Resource limits to prevent DoS

### Network Security
- Internal Docker networks
- Port exposure minimization
- API authentication (when configured)
- Redis password protection (recommended)

### Data Security
- Environment variable secrets
- Volume encryption (recommended)
- Regular security updates
- Log sanitization

---

## 🚨 Troubleshooting Guide

### Common Issues

**1. Container Won't Start**
```bash
# Check logs
docker-compose logs [service-name]

# Check resource usage
docker stats

# Verify image build
docker images | grep financio
```

**2. API Connection Issues**
```bash
# Test backend connectivity
curl http://localhost:8000/health

# Check Redis connectivity
docker exec redis redis-cli ping

# Verify network
docker network ls
```

**3. Performance Issues**
```bash
# Monitor resources
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Check disk space
docker system df

# Analyze logs
docker logs --tail 100 [container-name]
```

### Debug Mode

**Interactive Container Access**
```bash
# Access running container
docker exec -it financio-backend bash

# Run debug container
docker run -it --rm financio-multibot:optimized /bin/bash
```

**Log Analysis**
```bash
# Follow logs in real-time
docker-compose logs -f

# Search specific service logs
docker-compose logs backend | grep ERROR
```

---

## 📚 Additional Resources

### Related Documentation
- [Multi-Bot System Guide](../docs/multi-bot-guide.md)
- [API Reference](../docs/api-reference.md)
- [Deployment Guide](../docs/deployment.md)
- [Trading Strategies](../docs/strategies.md)

### External Resources
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Deployment Guide](https://create-react-app.dev/docs/deployment/)

---

## 📝 Summary

The Financio-V2 Docker architecture provides flexible deployment options ranging from simple single-container setups to sophisticated microservices architectures. Each image is optimized for its specific purpose, enabling efficient resource utilization and scalable deployments.

**Key Benefits:**
- ✅ **Flexible Deployment**: Multiple patterns for different scales
- ✅ **Optimized Performance**: Purpose-built containers
- ✅ **Easy Scaling**: Horizontal and vertical scaling options
- ✅ **Development Friendly**: Hot reloading and debugging support
- ✅ **Production Ready**: Health checks and monitoring
- ✅ **Security Focused**: Alpine Linux and minimal attack surface

Choose the deployment pattern that best fits your use case, infrastructure, and scaling requirements.
