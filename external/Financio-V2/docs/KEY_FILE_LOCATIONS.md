# Financio-V2 - Key File Locations & Component Reference

## Quick Navigation Guide

This document provides absolute file paths for quick reference when reviewing the architecture analysis.

### Model Training & Prediction Pipeline

**XGBoost Models:**
- `/Users/mosley/projects/Financio-V2/financio_src/model/xgb_model.py` - XGBoost classifier
- `/Users/mosley/projects/Financio-V2/financio_src/model/optunaTune.py` - Hyperparameter optimization
- `/Users/mosley/projects/Financio-V2/financio_src/model/hyperTune.py` - Tuning utilities

**LSTM Predictor:**
- `/Users/mosley/projects/Financio-V2/financio_src/model/lstm_model.py` - LSTM architecture
- `/Users/mosley/projects/Financio-V2/financio_src/model/lstm_predictor_service.py` - Service wrapper

**Ensemble Model:**
- `/Users/mosley/projects/Financio-V2/financio_src/ensemble/ensemble_trading_model.py` - 4-signal ensemble

### Risk Management

- `/Users/mosley/projects/Financio-V2/financio_src/risk_management/enhanced_risk_manager.py` - Dynamic risk parameters
- `/Users/mosley/projects/Financio-V2/financio_src/trading/sizing.py` - Bayesian position sizing
- `/Users/mosley/projects/Financio-V2/financio_src/trading/risk_manager.py` - Risk checks

### Trading Execution

- `/Users/mosley/projects/Financio-V2/financio_src/trading/live_trading.py` - Main trading engine (791 lines)
- `/Users/mosley/projects/Financio-V2/financio_src/trading/trade_executor.py` - Execution wrapper (minimal)
- `/Users/mosley/projects/Financio-V2/financio_src/strategy/decision_rules.py` - Strategy selection logic

### Data Collection & Features

**Data Fetching:**
- `/Users/mosley/projects/Financio-V2/financio_src/data/fetch_prices.py` - Alpaca API integration
- `/Users/mosley/projects/Financio-V2/financio_src/data/preprocess.py` - Data preprocessing
- `/Users/mosley/projects/Financio-V2/financio_src/data/synthetic_data_generator.py` - Fallback data

**Feature Engineering:**
- `/Users/mosley/projects/Financio-V2/financio_src/features/price_features.py` - Technical indicators (17 features)
- `/Users/mosley/projects/Financio-V2/financio_src/features/indicators.py` - Stochastic oscillator
- `/Users/mosley/projects/Financio-V2/financio_src/features/atr.py` - Average True Range
- `/Users/mosley/projects/Financio-V2/financio_src/features/patterns.py` - Candlestick patterns
- `/Users/mosley/projects/Financio-V2/financio_src/features/macro_features.py` - EMPTY (opportunity)
- `/Users/mosley/projects/Financio-V2/financio_src/features/sentiment_features.py` - EMPTY (opportunity)
- `/Users/mosley/projects/Financio-V2/financio_src/features/volume_features.py` - STUB (opportunity)

### Ensemble & Multi-Bot

- `/Users/mosley/projects/Financio-V2/financio_src/multi_bot/bot_manager.py` - Bot lifecycle management
- `/Users/mosley/projects/Financio-V2/financio_src/multi_bot/communication.py` - Redis pub/sub
- `/Users/mosley/projects/Financio-V2/financio_src/multi_bot/integration.py` - Multi-bot integration layer
- `/Users/mosley/projects/Financio-V2/financio_src/multi_bot/strategy_manager.py` - Strategy selection

### Sentiment Analysis

- `/Users/mosley/projects/Financio-V2/financio_src/sentiment/sentiment_collector.py` - Multi-source sentiment data
- `/Users/mosley/projects/Financio-V2/financio_src/sentiment/enhanced_sentiment_service.py` - Unified sentiment service
- `/Users/mosley/projects/Financio-V2/financio_src/sentiment/morgans_sentiment_bridge.py` - Morgans bot bridge

### Backend API

- `/Users/mosley/projects/Financio-V2/backend/main.py` - FastAPI backend (29KB, main endpoints)
- `/Users/mosley/projects/Financio-V2/backend/db.py` - Database wrapper
- `/Users/mosley/projects/Financio-V2/backend/supabase_config.py` - Supabase configuration
- `/Users/mosley/projects/Financio-V2/backend/equity_data_extractor.py` - Analytics functions

### Database

- `/Users/mosley/projects/Financio-V2/financio_src/db/manager.py` - SQLite manager
- `/Users/mosley/projects/Financio-V2/financio_src/db/dbInit.py` - Database initialization

### Configuration

- `/Users/mosley/projects/Financio-V2/financio_src/config.py` - Main configuration file (API keys, parameters)
- `/Users/mosley/projects/Financio-V2/financio_src/config/integration_config.py` - Integration settings
- `/Users/mosley/projects/Financio-V2/.env` - Environment variables

### Utilities

- `/Users/mosley/projects/Financio-V2/financio_src/utils/featureManager.py` - Feature standardization
- `/Users/mosley/projects/Financio-V2/financio_src/utils/model_loader.py` - Model loading utilities
- `/Users/mosley/projects/Financio-V2/financio_src/utils/helpers.py` - Helper functions

### Backtesting

- `/Users/mosley/projects/Financio-V2/financio_src/backtesting/backtest_price.py` - Price-based backtesting
- `/Users/mosley/projects/Financio-V2/financio_src/backtesting/backtest_sentiment.py` - EMPTY
- `/Users/mosley/projects/Financio-V2/financio_src/backtesting/simulate_trades.py` - EMPTY

### Meta Learning

- `/Users/mosley/projects/Financio-V2/financio_src/meta/metaLearn.py` - Meta-learning logic
- `/Users/mosley/projects/Financio-V2/financio_src/meta/modelSelect.py` - Model selection
- `/Users/mosley/projects/Financio-V2/financio_src/meta/modelEval.py` - Model evaluation

### Root Level (Important Files)

- `/Users/mosley/projects/Financio-V2/README.md` - Project overview
- `/Users/mosley/projects/Financio-V2/SYSTEM_ARCHITECTURE.md` - Architecture diagrams
- `/Users/mosley/projects/Financio-V2/INTEGRATION_ARCHITECTURE.md` - Integration details
- `/Users/mosley/projects/Financio-V2/CLAUDE.md` - Development instructions
- `/Users/mosley/projects/Financio-V2/requirements.txt` - Python dependencies
- `/Users/mosley/projects/Financio-V2/pyproject.toml` - Poetry configuration

### Docker & Deployment

- `/Users/mosley/projects/Financio-V2/docker-compose.yml` - Main composition
- `/Users/mosley/projects/Financio-V2/docker-compose.development.yml` - Dev setup
- `/Users/mosley/projects/Financio-V2/docker-compose.production.yml` - Prod setup
- `/Users/mosley/projects/Financio-V2/Dockerfile` - Container build
- `/Users/mosley/projects/Financio-V2/deploy-alpha.sh` - Deployment script

### Models Directory

- `/Users/mosley/projects/Financio-V2/models/{TICKER}/` - Per-ticker models
  - `{TICKER}_booster.json` - XGBoost model
  - `{TICKER}_feature_params.json` - Feature metadata

### Logs Directory

- `/Users/mosley/projects/Financio-V2/logs/` - Trading logs
  - `{TICKER}_YYYY-MM-DD_stdout.log` - Standard output
  - `{TICKER}_YYYY-MM-DD_stderr.log` - Standard error
  - `financio_trades.db` - SQLite trade database

---

## Quick Reference: File Sizes

| Component | Files | Total Size | Status |
|-----------|-------|-----------|--------|
| Model Pipeline | 6 | ~50KB | Good |
| Risk Management | 3 | ~15KB | Excellent |
| Trading Execution | 4 | ~100KB | Adequate |
| Data Pipeline | 8 | ~40KB | Good |
| Sentiment | 3 | ~30KB | Good |
| Multi-Bot | 4 | ~40KB | Good |
| Backend | 4 | ~60KB | Adequate |
| Features | 8 | ~20KB | Limited |
| **Total** | **40+** | **~355KB** | **Production-Ready** |

## Finding Code Mentioned in Analysis

Each section of ARCHITECTURE_ANALYSIS.md includes **Location:** prefixes. Use these to find relevant files:

### Example:
```
Location: financio_src/model/xgb_model.py
Full path: /Users/mosley/projects/Financio-V2/financio_src/model/xgb_model.py
```

## Key Architecture Files

These files are most critical to understand the system:

1. **HIGHEST PRIORITY**
   - `/Users/mosley/projects/Financio-V2/financio_src/trading/live_trading.py` - Core engine (791 lines)
   - `/Users/mosley/projects/Financio-V2/financio_src/ensemble/ensemble_trading_model.py` - Decision logic
   - `/Users/mosley/projects/Financio-V2/financio_src/risk_management/enhanced_risk_manager.py` - Risk controls

2. **IMPORTANT**
   - `/Users/mosley/projects/Financio-V2/financio_src/multi_bot/bot_manager.py` - Bot coordination
   - `/Users/mosley/projects/Financio-V2/financio_src/sentiment/enhanced_sentiment_service.py` - Sentiment integration
   - `/Users/mosley/projects/Financio-V2/backend/main.py` - API endpoints

3. **SUPPORTING**
   - `/Users/mosley/projects/Financio-V2/financio_src/features/price_features.py` - Feature engineering
   - `/Users/mosley/projects/Financio-V2/financio_src/db/manager.py` - Data persistence
   - `/Users/mosley/projects/Financio-V2/financio_src/config.py` - Configuration

---

## Related Analysis Documents

- `/Users/mosley/projects/Financio-V2/ARCHITECTURE_ANALYSIS.md` - Full technical analysis
- `/Users/mosley/projects/Financio-V2/ARCHITECTURE_ANALYSIS_SUMMARY.txt` - Executive summary
- `/Users/mosley/projects/Financio-V2/ANALYSIS_INDEX.md` - Documentation index

---

Generated: November 3, 2025
