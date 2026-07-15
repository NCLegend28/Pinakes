# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Environment Setup
```bash
# Activate virtual environment
source .venv/bin/activate

# Install Python dependencies using uv
uv pip install -r requirements.txt

# Install specific package with uv
uv pip install package-name

# Update all dependencies
uv pip install --upgrade -r requirements.txt

# Sync dependencies (install/update/remove to match requirements.txt exactly)
uv pip sync requirements.txt
```

### Frontend Development (React Dashboard)
```bash
# Navigate to dashboard and start development server
cd dashboard && npm run dev

# Build for production
cd dashboard && npm run build

# Lint frontend code
cd dashboard && npm run lint
```

### Backend Development (Trading Engine)
```bash
# Start FastAPI backend server
cd backend && python -m uvicorn main:app --reload --port 8001

# Run Flask API service for dashboard mock data
cd dashboard/src/services && python api.py

# Run multi-bot production system
python run_multi_bot_production.py

# Test multi-bot signals
python -m tests.test_multi_bot_signals
```

### Database Development (Supabase)
```bash
# Start local Supabase development server
cd supabase && supabase start

# Reset and migrate database
cd supabase && supabase db reset

# Stop local Supabase server
cd supabase && supabase stop
```

### Docker Deployment
```bash
# Full production deployment
./deploy-alpha.sh

# Start with Docker Compose
docker-compose up -d

# Development environment
./scripts/deploy-development.sh

# Microservices architecture
./scripts/deploy-microservices.sh
```

### Testing
```bash
# Test model loading
python -m tests.test_model_loading_fix

# Test enhanced risk management
python -m tests.test_enhanced_risk_mgmt

# Test Supabase connection
python -m tests.test_supabase_connection

# Test long-only trading
python -m tests.test_long_only_trading
```

## System Architecture Overview

Financio-V2 is a comprehensive algorithmic trading platform with the following key architectural components:

### Core Components
1. **React Dashboard** (`dashboard/`) - Frontend interface with real-time monitoring
2. **FastAPI Backend** (`backend/`) - Trading API and data processing
3. **Trading Engine** (`financio_src/`) - Core ML-powered trading logic
4. **Supabase Database** (`supabase/`) - PostgreSQL with real-time capabilities
5. **Multi-Bot System** - 15+ concurrent trading bots across different tickers

### Multi-Layered Architecture
- **Frontend Layer**: React + TypeScript + Vite + ShadCN UI components
- **API Layer**: FastAPI backend with RESTful endpoints
- **Trading Engine**: ML models, sentiment analysis, and risk management
- **Data Layer**: Supabase PostgreSQL with real-time subscriptions
- **Communication**: Redis pub/sub for real-time bot coordination
- **External APIs**: Alpaca for trading, various news/social media APIs for sentiment

### Database Schema (Supabase)
Key tables:
- `users` - User management and preferences
- `trades` - All trading activity with metadata
- `bot_instances` - Multi-bot configuration and status
- `portfolio_snapshots` - Portfolio value tracking over time
- `notifications` - User alerts and system messages

### Trading Bot Architecture
Each bot operates independently with:
- **Ticker-specific ML models** stored in `models/{TICKER}/`
- **Strategy implementations** in `financio_src/strategy/`
- **Risk management** via enhanced portfolio-wide controls
- **Real-time communication** through Redis pub/sub
- **Sentiment analysis integration** for news and social media data

## Key Configuration Files

### Environment Configuration
- `financio_src/.env` - Trading engine configuration (API keys, trading mode)
- `dashboard/.env` - Frontend environment variables
- `.env.template` - Template for required environment variables

### Project Configuration
- `dashboard/package.json` - Frontend dependencies and scripts
- `requirements.txt` - Python dependencies for trading engine
- `supabase/config.toml` - Supabase local development configuration
- `docker-compose.yml` - Container orchestration

### Database Migrations
- `supabase/migrations/` - Database schema migrations
- `supabase/seed.sql` - Initial database seeding

## Important Implementation Details

### Real-Time Data Flow
1. Market data ingestion from Alpaca API
2. Feature engineering with 200+ technical indicators
3. ML model predictions combined with sentiment analysis
4. Risk management validation and position sizing
5. Trade execution through Alpaca
6. Real-time dashboard updates via WebSocket/Supabase subscriptions

### Enhanced Sentiment Analysis Integration
- **ENHANCED WITH MORGANS BOT** - VADER + FinBERT sentiment analysis
- **Primary Source**: Morgans bot (`~/projects/Morgans`) via shared directory
- **Fallback Source**: Financio's native TextBlob sentiment
- Multi-source data collection (news APIs, social media)
- 25% weight in ensemble model decisions (part of 4-signal ensemble)
- Real-time processing with 15-minute update intervals
- Data flow: Morgans → `~/projects/shared_data/stocks/` → EnhancedSentimentService → Ensemble

**Integration Files:**
- `financio_src/sentiment/morgans_sentiment_bridge.py` - Bridge to Morgans data
- `financio_src/sentiment/enhanced_sentiment_service.py` - Unified sentiment service

**See:** `INTEGRATION_ARCHITECTURE.md` and `INTEGRATION_PROGRESS.md` for full details

### Multi-Bot Coordination
- Independent bot operation per ticker with shared risk management
- Redis-based pub/sub communication between bots
- Portfolio-wide position limits and risk controls
- Ensemble decision making across multiple strategies

### Development vs Production Modes
- **Development**: Paper trading with local Supabase (ports 5173/8000)
- **Alpha Testing**: Paper trading with containerized setup (ports 8080/8001)
- **Production**: Live trading with Supabase Cloud (port 443/8000)

## File Structure Context

### Frontend (`dashboard/`)
- `src/components/` - React components including new AITradingDashboard
- `src/services/` - API clients and Supabase integration
- `src/pages/` - Route components and main application pages

### Trading Engine (`financio_src/`)
- `trading/` - Live trading execution logic
- `model/` - ML model training and prediction
- `sentiment/` - News and social media sentiment analysis
- `ensemble/` - Multi-signal ensemble trading model
- `risk_management/` - Portfolio and position risk controls
- `multi_bot/` - Bot coordination and management

### Database (`supabase/`)
- `migrations/` - Database schema evolution
- `config.toml` - Local development configuration

The system uses a service-oriented architecture where each component can operate independently while maintaining real-time coordination through well-defined APIs and messaging protocols.
