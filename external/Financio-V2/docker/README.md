# 🐳 Financio-V2 Docker Deployment Guide

This guide provides comprehensive instructions for deploying Financio-V2 using ### Microservices Architecture

**Use Case**: Scalable production deployment with separate containers for each component
**Features**: Individual containers, load balancing, monitoring, Redis caching

```bash
# Deploy microservices
./scripts/deploy-microservices.sh

# With monitoring stack
docker-compose -f docker-compose.microservices.yml --profile monitoring up -d
```

**Access Points**:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- Redis: localhost:6379
- Prometheus: http://localhost:9090 (optional)
- Grafana: http://localhost:3000 (optional, admin/admin)ferent scenarios and environments.

## 📁 Docker Infrastructure Overview

```
docker/
├── Dockerfile.production      # Full-stack production deployment
├── Dockerfile.development     # Development with hot reloading
├── Dockerfile.backend         # Backend-only microservice
├── Dockerfile.frontend        # Frontend-only with Nginx
├── Dockerfile.multibot        # Multi-bot trading system
├── Dockerfile.trading         # Individual trading bot
└── nginx/
    ├── default.conf           # Frontend-only Nginx config
    └── production.conf        # Production reverse proxy config

docker-compose files:
├── docker-compose.production.yml    # Production deployment
├── docker-compose.development.yml   # Development environment
├── docker-compose.microservices.yml # Microservices architecture
├── docker-compose.testing.yml       # Testing environment
└── docker-compose.yml               # Legacy/simple deployment

scripts/
├── deploy-production.sh      # Production deployment script
├── deploy-development.sh     # Development setup script
├── deploy-microservices.sh   # Microservices deployment
├── run-tests.sh             # Testing environment
└── docker-manager.sh        # Unified management utility
```

## 🚀 Quick Start

### Option 1: Using the Docker Manager (Recommended)
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Deploy production environment
./scripts/docker-manager.sh production

# Start development environment
./scripts/docker-manager.sh development

# Check status of all environments
./scripts/docker-manager.sh status

# View logs
./scripts/docker-manager.sh logs --env production

# Run tests
./scripts/docker-manager.sh testing --type unit
```

### Option 2: Direct Script Execution
```bash
# Production deployment
./scripts/deploy-production.sh

# Development environment
./scripts/deploy-development.sh

# Microservices architecture
./scripts/deploy-microservices.sh

# Run tests
./scripts/run-tests.sh --type all --coverage
```

## 🏗️ Deployment Scenarios

### 1. Production Deployment

**Use Case**: Complete production environment with optimized containers
**Features**: Multi-stage builds, health checks, volume persistence, Redis caching

```bash
# Quick deployment
./scripts/deploy-production.sh

# Manual deployment
export POSTGRES_PASSWORD=$(openssl rand -base64 32)
docker-compose -f docker-compose.production.yml build --no-cache
docker-compose -f docker-compose.production.yml up -d

# With trading bots
docker-compose -f docker-compose.production.yml --profile trading up -d

# With Nginx reverse proxy
docker-compose -f docker-compose.production.yml --profile nginx up -d
```

**Access Points**:
- Frontend: http://localhost:8080
- Backend API: http://localhost:10000
- Redis: localhost:6379

### 2. Development Environment

**Use Case**: Local development with hot reloading and debugging tools
**Features**: Source code mounting, hot reloading, debug ports, development databases

```bash
# Start development environment
./scripts/deploy-development.sh

# With optional services
docker-compose -f docker-compose.development.yml --profile database up -d  # PostgreSQL
docker-compose -f docker-compose.development.yml --profile analysis up -d  # Jupyter
docker-compose -f docker-compose.development.yml --profile multibot up -d  # Multi-bot dev
```

**Access Points**:
- Frontend (Vite): http://localhost:5173
- Backend API: http://localhost:8000
- Debug Port: localhost:5678
- Jupyter: http://localhost:8888 (optional)

### 3. Microservices Architecture

**Use Case**: Scalable production deployment with separate containers for each component
**Features**: Individual containers, load balancing, monitoring, database integration

```bash
# Deploy microservices
./scripts/deploy-microservices.sh

# With monitoring stack
docker-compose -f docker-compose.microservices.yml --profile monitoring up -d
```

**Access Points**:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- Redis: localhost:6379

**Scaling**:
```bash
# Scale trading bots
docker-compose -f docker-compose.microservices.yml up --scale trading-bot-1=3

# Scale specific services
docker-compose -f docker-compose.microservices.yml up --scale backend=2
```

### 4. Testing Environment

**Use Case**: Isolated testing with comprehensive test suites
**Features**: Unit tests, integration tests, performance tests, code quality checks

```bash
# Run all tests
./scripts/run-tests.sh --type all --coverage

# Run specific test types
./scripts/run-tests.sh --type unit          # Unit tests only
./scripts/run-tests.sh --type integration  # Integration tests
./scripts/run-tests.sh --type performance  # Performance tests
./scripts/run-tests.sh --type quality      # Code quality checks
```

## 🛠️ Individual Container Usage

### Backend Only
```bash
docker build -f docker/Dockerfile.backend -t financio-backend .
docker run -p 8000:8000 -e PYTHONPATH=/app financio-backend
```

### Frontend Only
```bash
docker build -f docker/Dockerfile.frontend -t financio-frontend .
docker run -p 80:80 financio-frontend
```

### Multi-Bot System
```bash
docker build -f docker/Dockerfile.multibot -t financio-multibot .
docker run -e REDIS_HOST=redis financio-multibot
```

### Individual Trading Bot
```bash
docker build -f docker/Dockerfile.trading -t financio-trading .
docker run -e BOT_ID=custom-bot-1 -e BOT_STRATEGY=ml_enhanced financio-trading
```

## 📊 Monitoring and Management

### Health Checks
All production containers include health checks:
```bash
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"

# View health check logs
docker inspect --format='{{json .State.Health}}' container-name
```

### Logs
```bash
# View logs for specific environment
./scripts/docker-manager.sh logs --env production --service backend

# Follow logs in real-time
docker-compose -f docker-compose.production.yml logs -f

# View logs for specific service
docker-compose -f docker-compose.production.yml logs -f multi-bot
```

### Resource Usage
```bash
# Monitor resource usage
docker stats

# View volume usage
docker system df -v

# Check network information
docker network ls
docker network inspect financio-production
```

## 💾 Data Management

### Backup Volumes
```bash
# Backup all data volumes
./scripts/docker-manager.sh backup

# Manual backup
docker run --rm -v financio_logs:/data -v $(pwd)/backup:/backup alpine tar czf /backup/logs.tar.gz -C /data .
```

### Restore Volumes
```bash
# Restore from backup
./scripts/docker-manager.sh restore backups/20250625_143000

# Manual restore
docker run --rm -v financio_logs:/data -v $(pwd)/backup:/backup alpine tar xzf /backup/logs.tar.gz -C /data
```

### Database Operations
```bash
# SQLite database operations (default)
# View trading data
sqlite3 financio_src/logs/financio_trades.db "SELECT * FROM trades LIMIT 10;"

# Backup SQLite database
cp financio_src/logs/financio_trades.db backup/financio_trades_$(date +%Y%m%d).db

# Check database size
ls -lh financio_src/logs/financio_trades.db
```

## 🔧 Configuration

### Environment Variables
Create `financio_src/.env` with your configuration:
```env
# API Keys
ALPHA_VANTAGE_API_KEY=your_api_key
FINANCIALMODELINGPREP_API_KEY=your_api_key

# Trading Configuration
TRADING_MODE=paper  # or live
INITIAL_BALANCE=100000
RISK_TOLERANCE=0.02

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
```

### Custom Configuration
```bash
# Override Postgres password
export POSTGRES_PASSWORD=your_secure_password

# Set custom bot configuration
export BOT_ID=custom-bot
export BOT_STRATEGY=technical_analysis
```

## 🚨 Troubleshooting

### Common Issues

**1. Port Conflicts**
```bash
# Check port usage
lsof -i :8000
lsof -i :5173

# Change ports in docker-compose files if needed
```

**2. Permission Issues**
```bash
# Fix volume permissions
docker-compose exec backend chown -R app:app /app/logs
```

**3. Memory Issues**
```bash
# Increase Docker memory limit
# Docker Desktop > Settings > Resources > Memory

# Monitor memory usage
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

**4. Network Issues**
```bash
# Recreate networks
docker network prune
docker-compose down && docker-compose up -d
```

### Debug Mode
```bash
# Run containers with debug output
docker-compose -f docker-compose.development.yml up --verbose

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend sh

# Check container logs
docker logs --follow container-name
```

### Clean Reset
```bash
# Stop all environments
./scripts/docker-manager.sh stop --env production
./scripts/docker-manager.sh stop --env development
./scripts/docker-manager.sh stop --env microservices

# Clean all Docker resources
./scripts/docker-manager.sh clean --all

# Remove specific volumes
docker volume rm financio_logs financio_models
```

## 📈 Performance Optimization

### Production Optimizations
- Multi-stage builds reduce image size
- Health checks ensure service reliability
- Volume mounting for persistent data
- Redis caching for improved performance
- Nginx reverse proxy for load balancing

### Development Optimizations
- Hot reloading for rapid development
- Source code mounting for instant updates
- Debug ports for debugging
- Development databases for testing

### Scaling Recommendations
```bash
# Scale backend services
docker-compose -f docker-compose.microservices.yml up --scale backend=3

# Scale trading bots
docker-compose -f docker-compose.microservices.yml up --scale trading-bot-1=5

# Use Docker Swarm for multi-node scaling
docker swarm init
docker stack deploy -c docker-compose.production.yml financio
```

## 🔐 Security Considerations

### Production Security
- Environment variables for sensitive data
- Health checks prevent unhealthy containers
- Security headers in Nginx configuration
- Rate limiting on API endpoints
- SSL/TLS configuration ready

### Network Security
```bash
# Use custom networks
docker network create --driver bridge financio-secure

# Isolate services
docker-compose -f docker-compose.production.yml --project-name financio-prod up -d
```

### Secrets Management
```bash
# Use Docker secrets in production
echo "sensitive_api_key" | docker secret create api_key -

# Reference in compose file:
# secrets:
#   - api_key
```

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Multi-stage Builds](https://docs.docker.com/develop/multistage-build/)
- [Docker Networking](https://docs.docker.com/network/)
- [Docker Volumes](https://docs.docker.com/storage/volumes/)

---

For additional help or questions, refer to the project documentation in the `reports/` directory or check the logs using the provided management scripts.
