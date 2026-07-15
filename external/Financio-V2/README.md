# 🚀 Financio-V2: Advanced Algorithmic Trading Platform

**Version:** v1.0.0-alpha.1
**Status:** Production Ready & Fully Operational
**Lovable Project:** https://lovable.dev/projects/8b352f26-f7b5-446a-bad7-54cf436b69f6

---

## 🔗 Shared Ticker Integration

**✅ Now integrated with shared data pipeline!**

Financio-V2 is connected to the centralized ticker configuration system, allowing automatic synchronization with other trading bots.

### Quick Sync

```bash
cd ~/projects/Financio-V2
python financio_ticker_integration.py
```

**Current Tickers**: PATH, TSLA, NKE, AAPL

### Integration Benefits
- ✅ Centralized ticker management
- ✅ Automatic updates from ticker discovery
- ✅ Shared sentiment data from Morgans bot
- ✅ Consistent queries across all bots

**See**: `~/projects/README.md` for complete ecosystem overview

---

## 🎯 Project Overview

Financio-V2 is a comprehensive algorithmic trading platform featuring advanced machine learning models, multi-bot ensemble architecture, and real-time dashboard monitoring. The system combines institutional-grade trading capabilities with user-friendly interfaces.

### ✨ Key Features
- **48 Active Trading Bots** with ensemble decision-making
- **Advanced ML Models** with 93.6% F1 accuracy
- **Real-Time Dashboard** with live monitoring
- **Docker Deployment** with production-ready infrastructure
- **Multi-Strategy Trading** (ML, Trend, Hybrid approaches)
- **Risk Management** with sophisticated controls

## 📋 Documentation & Reports

**📁 Complete documentation now lives under [`docs/`](./docs/) (detailed reports are in [`docs/reports/`](./docs/reports/)):**

- **[📊 Complete Features List](./docs/COMPREHENSIVE_FEATURES_LIST.md)** - 150+ system features
- **[🚀 Alpha Release Notes](./docs/ALPHA_RELEASE_NOTES.md)** - v1.0.0-alpha.1 documentation  
- **[🐳 Docker Deployment Guide](./docs/DOCKER_DEPLOYMENT.md)** - Containerization setup
- **[🤖 Multi-Bot System Report](./docs/MULTI_BOT_COMPLETION_REPORT.md)** - Advanced architecture
- **[📈 Dashboard Integration](./docs/DASHBOARD_INTEGRATION_SUCCESS.md)** - UI implementation

**👉 [View All Reports](./docs/reports/README.md)**

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)
```bash
# Clone the repository
git clone <YOUR_GIT_URL>
cd Financio-V2

# Deploy with Docker
./deploy-alpha.sh

# Access dashboard
open http://localhost:8002
```

### Option 2: Development Setup
```bash
# Clone and setup
git clone <YOUR_GIT_URL>
cd Financio-V2

# Install dependencies
npm i

# Start development server
npm run dev

# Start backend (separate terminal)
cd backend && python -m uvicorn main:app --reload --port 8001
```

### Option 3: Lovable Platform

Simply visit the [Lovable Project](https://lovable.dev/projects/8b352f26-f7b5-446a-bad7-54cf436b69f6) and start prompting. Changes are automatically committed to this repo.

## 🧪 Tests

All standalone regression scripts now live under the [`tests/`](./tests) directory. Run them with Python's module syntax so imports stay consistent:

```bash
python -m tests.test_multi_bot_signals
python -m tests.test_enhanced_features
python -m tests.test_model_loading_fix
```

Use `pytest tests` for a full sweep.

## 🛠️ Technology Stack

### Frontend
- **React + TypeScript** - Modern UI framework
- **Vite** - Fast development and build tool
- **Tailwind CSS** - Utility-first styling
- **shadcn-ui** - Professional component library

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLite** - Efficient data storage
- **Redis** - Real-time communication
- **Alpaca API** - Live trading integration

### Infrastructure
- **Docker** - Containerized deployment
- **Multi-Bot Architecture** - Scalable trading system
- **Real-Time Processing** - Sub-second latency

## 🎯 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Dashboard│    │   FastAPI       │    │   Trading       │
│   (Frontend)    │◄──►│   Backend       │◄──►│   Engine        │
│   - Live Charts │    │   - Live Data   │    │   - ML Models   │
│   - Portfolio   │    │   - API Routes  │    │   - Multi-Bots  │
│   - Bot Status  │    │   - Database    │    │   - Live Trading│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Current Status

- ✅ **Alpha Release**: v1.0.0-alpha.1 deployed and operational
- ✅ **Multi-Bot System**: 48 bots across 16 tickers active  
- ✅ **Dashboard**: Unified interface with real-time monitoring
- ✅ **Docker**: Containerized deployment ready for production
- ✅ **Performance**: 93.6% ML model accuracy, <1ms communication latency

## 🚀 Deployment Options

### 🎯 Quick Start (Recommended)
```bash
# 1. Set up environment variables
cp .env.template financio_src/.env
# Edit financio_src/.env with your API keys

# 2. Choose your deployment:
./scripts/docker-manager.sh production      # Full production setup
./scripts/docker-manager.sh development    # Development environment
./scripts/docker-manager.sh microservices  # Scalable architecture
```

### 🐳 Docker Deployments

#### Production Environment
```bash
# Optimized production deployment with Redis, health checks, and volume persistence
./scripts/deploy-production.sh

# Access: Frontend (http://localhost:8080) | API (http://localhost:10000)
```

#### Development Environment  
```bash
# Hot reloading, debug ports, and development tools
./scripts/deploy-development.sh

# Access: Frontend (http://localhost:5173) | API (http://localhost:8001)
```

#### Microservices Architecture
```bash
# Separate containers for backend, frontend, multi-bot, and trading bots
./scripts/deploy-microservices.sh

# With monitoring: --profile monitoring (Prometheus + Grafana)
# Access: Frontend (http://localhost) | API (http://localhost:8000) | Redis (localhost:6379)
```

#### Testing Environment
```bash
# Comprehensive test suites with isolated containers
./scripts/run-tests.sh --type all --coverage

# Test types: unit, integration, performance, quality
```

### 📋 Docker Management
```bash
# Unified management utility
./scripts/docker-manager.sh status              # Check all environments
./scripts/docker-manager.sh logs --env production --service backend
./scripts/docker-manager.sh stop --env development
./scripts/docker-manager.sh backup              # Backup data volumes
./scripts/docker-manager.sh clean               # Clean Docker resources
```

### 🌐 Platform Deployments

#### Lovable Platform
Simply open [Lovable](https://lovable.dev/projects/8b352f26-f7b5-446a-bad7-54cf436b69f6) and click Share → Publish.

#### Legacy Docker (Alpha)
```bash
# Original alpha deployment
./deploy-alpha.sh
docker-compose -f docker-compose.alpha.yml up -d
```

### 🔧 Custom Domain
Navigate to Project > Settings > Domains and click Connect Domain.  
Read more: [Setting up a custom domain](https://docs.lovable.dev/tips-tricks/custom-domain#step-by-step-guide)

## 🔧 Development

### Project Structure
```
Financio-V2/
├── dashboard/          # React frontend
├── backend/           # FastAPI backend  
├── financio_src/      # Trading engine
├── docs/              # Documentation & reports (see docs/reports/)
├── models/            # ML model storage
└── docker-compose.yml # Container orchestration
```

### Key Commands
```bash
# Start full system
docker-compose up -d

# Development mode
npm run dev                    # Frontend
python -m uvicorn main:app     # Backend

# Multi-bot system
python run_multi_bot_production.py

# Run tests
python -m tests.test_multi_bot_signals
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- **Documentation**: Check the [`docs/`](./docs/) tree (detailed reports are under [`docs/reports/`](./docs/reports/))
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Lovable Platform**: Direct integration support

## 📖 Quick Reference

### Essential Files
- `📁 docker/` - All Docker configurations and deployment scripts
- `📁 docs/` - Comprehensive project documentation and reports (see `docs/reports/` for deep dives)  
- `📁 scripts/` - Deployment and management utilities
- `📄 .env.template` - Environment configuration template
- `📄 docker/README.md` - Complete Docker deployment guide

### Key Commands
```bash
# Quick deployment
./scripts/docker-manager.sh production

# Development setup
./scripts/docker-manager.sh development  

# View documentation
cat docker/README.md                    # Docker guide
cat docs/reports/README.md              # All reports index
```

---

**Ready for professional algorithmic trading with institutional-grade capabilities!** 🚀
