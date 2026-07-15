# 🚀 Financio-V2 Deployment Guide

## 📁 Simplified Architecture

We've consolidated from **8 different Docker Compose files** down to just **2 essential files**:

### ✅ **Active Files:**
- **[`docker-compose.yml`](docker-compose.yml)** - Development & Microservices
- **[`docker-compose.production.yml`](docker-compose.production.yml)** - Production & Live Trading

### 📦 **Backup Files:**
- Old compose files moved to `backup/docker-compose-old/`

## 🛠️ **Deploy Script Usage:**

### **Quick Start:**
```bash
# Setup environment (first time only)
./deploy-bots.sh setup

# Build images
./deploy-bots.sh build

# Start development mode (monolithic)
./deploy-bots.sh dev

# Start microservices mode (separate containers)
./deploy-bots.sh microservices

# Start production mode (LIVE TRADING!)
./deploy-bots.sh production
```

### **Monitoring:**
```bash
# Check status of all containers
./deploy-bots.sh status

# View logs
./deploy-bots.sh logs all
./deploy-bots.sh logs backend
./deploy-bots.sh logs trading-bots

# Follow logs in real-time
./deploy-bots.sh follow trading-bots

# Stop everything
./deploy-bots.sh stop
```

## 🎯 **Deployment Modes:**

### **1. Development Mode** 
```bash
./deploy-bots.sh dev
```
- **Purpose**: Local development and testing
- **Architecture**: Monolithic (single container)
- **Access**: http://localhost:10000
- **Use Case**: Code development, debugging

### **2. Microservices Mode**
```bash
./deploy-bots.sh microservices
```
- **Purpose**: Production-like architecture testing
- **Architecture**: Separate containers for frontend, backend, bots
- **Access**: 
  - Frontend: http://localhost:3000
  - Backend API: http://localhost:8000
- **Use Case**: Integration testing, performance testing

### **3. Production Mode**
```bash
./deploy-bots.sh production
```
- **Purpose**: Live trading with real money
- **Architecture**: Optimized production containers
- **Access**: 
  - Frontend: http://localhost:3000
  - Backend API: http://localhost:8000
- **Use Case**: Live trading, real money deployment

## 📊 **Focused Dockerfiles:**

### **Backend** ([`docker/Dockerfile.backend`](docker/Dockerfile.backend))
- **Purpose**: FastAPI server only
- **Size**: ~200MB (lightweight)
- **Dependencies**: FastAPI, pandas, SQLite utilities
- **No**: PyTorch, ML libraries, trading logic

### **Frontend** ([`docker/Dockerfile.frontend`](docker/Dockerfile.frontend))
- **Purpose**: React dashboard with Nginx
- **Size**: ~50MB (multi-stage build)
- **Dependencies**: Node.js build tools, Nginx
- **No**: Backend dependencies, trading logic

### **Trading Bots** ([`docker/Dockerfile.multibot`](docker/Dockerfile.multibot))
- **Purpose**: ML-powered trading system
- **Size**: ~2GB (includes PyTorch, Stable-Baselines3)
- **Dependencies**: PyTorch 2.7.1, Stable-Baselines3 2.6.0, all ML libraries
- **No**: Frontend build tools

## 🔧 **Benefits Achieved:**

### **✅ Simplified Management:**
- Single deployment script (`deploy-bots.sh`)
- Clear separation of concerns
- Easy mode switching

### **✅ Faster Builds:**
- Backend changes: No PyTorch rebuild
- Frontend changes: No Python dependencies
- Bot changes: Only when ML code changes

### **✅ Resource Efficiency:**
- Backend: Minimal CPU/memory usage
- Frontend: Nginx serves static files efficiently  
- Bots: Full ML resources when needed

### **✅ Clean Dependencies:**
- No version conflicts between services
- Each service has exactly what it needs
- Updated PyTorch to 2.7.1, Stable-Baselines3 to 2.6.0

## 🎉 **Ready for Action:**

Your Financio-V2 system is now:
- ✅ **Consolidated**: 2 compose files instead of 8
- ✅ **Focused**: Each Dockerfile serves one purpose
- ✅ **Updated**: Latest PyTorch and ML dependencies
- ✅ **Production-Ready**: Live trading deployment available
- ✅ **Developer-Friendly**: Easy local development

Start with `./deploy-bots.sh help` for full command reference!
