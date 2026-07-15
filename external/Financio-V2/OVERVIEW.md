# Financio-V2 — System Overview

## What It Is

Financio-V2 is a full-stack algorithmic trading platform. It runs multiple concurrent trading bots across a universe of US equities, each driven by machine learning models that combine technical analysis, sentiment data, and market-regime detection to generate buy/sell signals. It includes a real-time React dashboard, a FastAPI backend, a Supabase (PostgreSQL) database, and interactive Plotly backtesting charts.

---

## Architecture at a Glance

```
┌─────────────────────────────────────────────────────┐
│  React Dashboard  (Vite + TypeScript + ShadCN UI)   │  port 5173 / 8080
│  Live P&L · Bot Status · Sentiment · Risk Controls  │
└───────────────────────┬─────────────────────────────┘
                        │ REST + WebSocket
┌───────────────────────▼─────────────────────────────┐
│  FastAPI Backend  (backend/main.py)                  │  port 8001
│  Account data · Portfolio · Risk parameter API      │
└──────────┬───────────────────────┬───────────────────┘
           │                       │
┌──────────▼──────────┐  ┌─────────▼──────────────────┐
│  Supabase (Postgres) │  │  Trading Engine             │
│  trades              │  │  financio_src/              │
│  portfolio_snapshots │  │  ├─ broker/   (Alpaca/WB)  │
│  bot_instances       │  │  ├─ strategy/ (Trend/etc.) │
│  notifications       │  │  ├─ ensemble/ (ML signals) │
└──────────────────────┘  │  ├─ sentiment/(news/social)│
                          │  ├─ risk_management/        │
                          │  ├─ model/   (XGB/LSTM/RL)  │
                          │  └─ multi_bot/              │
                          └────────────────────────────┘
```

---

## Trading Strategies

Three distinct strategies run simultaneously — each with its own timeframe, signal logic, and risk parameters. A fourth "Smart Hold" strategy is used for long-term compounding.

| Strategy | Timeframe | Hold Period | Stop-Loss | Take-Profit | Edge |
|---|---|---|---|---|---|
| **Trend** | 1Day | ~50 bars | 7% | 14% | Golden-cross + ADX + 52-week momentum |
| **Swing** | 1Day | ~20 bars | 2.5% | 5% | RSI oversold + volume confirmation + MA200 regime |
| **HF** | 1Day | ~3 bars | 0.3% | 0.5% | Z-score mean-reversion + volume surge + spread contraction |
| **Smart Hold** | 1Day | Unlimited | 12% | None | Rides bull runs; exits on RSI divergence / MACD top / parabolic blow-off |

All strategies use:
- **ATR-based dynamic SL/TP** (not fixed %) scaled to current volatility
- **Inverse-volatility position sizing** (target 1% daily vol exposure per trade)
- **Trailing stop** that ratchets up as price makes new highs
- **MA200 regime filter** — long entries suppressed in downtrends

---

## ML Model Stack

### Primary Model: XGBoost Classifier
- Trained per-ticker using `financio_src/train.py`
- **60 input features**: 17 core (EMA, VWAP, candlestick patterns, momentum) + 43 enhanced (OBV, volatility regime, microstructure, MACD, Stochastic, Hurst exponent, fractal dimension)
- 3-class output: BUY / HOLD / SELL
- Models stored at `models/{TICKER}/{STRATEGY}/`
- Hyperparameter tuning via Optuna

### Secondary: LSTM Predictor
- Sequence model for time-series price prediction
- Implemented in `financio_src/model/lstm_model.py` and `lstm_predictor_service.py`
- Contributes 25% weight in the ensemble decision

### Reinforcement Learning: PPO Position Sizer
- Uses `stable-baselines3` PPO agent trained in `rl_train/`
- Custom Gym environment (`trade_sizing_env.py`) rewards risk-adjusted returns
- Determines position size (fraction of equity) dynamically based on confidence

### Ensemble Signal Combiner (`financio_src/ensemble/`)
Combines four signal sources with learned weights:

| Signal | Default Weight | Notes |
|---|---|---|
| Sentiment | 0.25 (calibrated) | Adjusted automatically from Morgans feedback loop |
| Technical (XGBoost) | 0.30 | Primary model prediction |
| Market Regime | 0.20 | Macro trend / volatility regime detector |
| LSTM | 0.25 | Sequence-based price prediction |

Output: `TradingSignal` with action (STRONG_BUY → STRONG_SELL), confidence, expected return, risk score, position size, SL/TP levels.

---

## Broker Layer

Multi-broker abstraction added on the `webull-dev` branch:

```
financio_src/broker/
├── base_broker.py      # Abstract BaseBroker interface
├── alpaca_broker.py    # Alpaca adapter (alpaca-py SDK)
└── webull_broker.py    # Webull adapter (webull-openapi SDK)
```

Switch brokers via `ACTIVE_BROKER=alpaca` (default) or `ACTIVE_BROKER=webull`. The trading engine, data fetcher, and backend API all call `get_active_broker()` — no broker-specific code outside the adapter layer.

---

## Sentiment Analysis

### Native (Financio-internal)
- Sources: Alpha Vantage news, NewsAPI, Polygon, Reddit (PRAW), Twitter
- Models: VADER sentiment, TextBlob
- Feeds into ensemble at 15-minute intervals

### Morgans Integration
Financio reads processed sentiment from a sibling project (`~/projects/Morgans`) via a shared filesystem directory (`~/projects/shared_data/stocks/`).

```
Morgans bot runs → writes {ticker}_combined_sentiment.csv
                         + {ticker}_combined_latest.json
                              ↓
financio_src/sentiment/morgans_sentiment_bridge.py
    → reads, normalizes, caches
    → feeds EnsembleTradingModel (25% weight, auto-calibrated)
```

**Sentiment calibration feedback loop** (runs during every backtest):
1. Load Morgans spike events (|score| ≥ 0.5) for the sector
2. Measure actual 1/3/7/21-day forward price returns at each event date
3. Compute directional accuracy — "was the bullish/bearish call correct?"
4. Map accuracy → sentiment weight via piecewise interpolation (0.10–0.40 range)
5. Save to `models/sentiment_calibration.json` → loaded by `EnsembleTradingModel` at startup

---

## Backtesting (`backtest_strategies.py`)

Interactive Plotly charts rendered per sector. Run with:

```bash
python backtest_strategies.py [--tickers AAPL MSFT ...] [--start 2015-01-01] [--out-dir .]
```

Outputs one HTML file per sector (e.g. `backtest_chart_technology.html`) containing:

| Panel | Content |
|---|---|
| **Equity** (top) | Normalized portfolio value for each strategy + Buy & Hold. Green/red regime bands. Gold diamond markers for key market events. Triangle markers for Morgans sentiment spikes. |
| **Drawdown** | Max drawdown % per strategy, dotted lines |
| **Morgans Sentiment** | Daily sector-average sentiment score line, filled green/red above/below zero. Only shown when Morgans data is available. |
| **Per-Stock Returns** | Grouped bar chart — total return × strategy for every ticker in the sector |

Chart covers 80+ tickers across 8 sectors (Technology, Industrial, Energy, Retail, Healthcare, Finance, Speculative, ETF Benchmarks) with a Plotly range-slider linking the date panels.

---

## Risk Management

### Trade-level (ATR-based)
- SL = `entry_price − 3.5 × ATR(14)` (configurable via API)
- TP = `entry_price + 4.5 × ATR(14)`
- Trailing stop ratchets 2 ATR below the running high-water mark
- Minimum profit threshold: 1.5% (avoids break-even churn)
- Confidence threshold: 75% minimum for entry

### Portfolio-level (`financio_src/risk_management/enhanced_risk_manager.py`)
- Max 3 consecutive losses → 2-minute cooling-off pause
- Position sizing capped by inverse-volatility formula
- Long-only mode enforced by default (`LONG_ONLY_MODE = True`)

### Runtime control
Risk parameters (SL/TP multipliers, confidence threshold, enable/disable enhanced risk) are editable through the dashboard's Risk Management panel, which calls `POST /api/risk-parameters` on the backend. **Note: this endpoint currently has no authentication — tracked as a known issue.**

---

## Multi-Bot System

Multiple bot instances run concurrently, each assigned to a ticker or set of tickers:

```
financio_src/multi_bot/
├── bot_manager.py      # Lifecycle management — start/stop/restart bots
├── communication.py    # Redis pub/sub for inter-bot messaging
├── strategy_manager.py # Per-bot strategy assignment
└── integration.py      # Ties bot_manager to the trading engine
```

Bot state (status, config, last signal) persists in the `bot_instances` Supabase table, which the dashboard subscribes to for real-time updates.

---

## Dashboard (`dashboard/`)

React + TypeScript + Vite + ShadCN UI

| Component | Purpose |
|---|---|
| `MultiBotDashboard.tsx` | Top-level overview — all active bots, P&L summary |
| `ActiveBots.tsx` | Per-bot status, last signal, start/stop controls |
| `TradingChart.tsx` | Live OHLCV chart with technical overlays |
| `SentimentAnalysisDashboard.tsx` | Morgans + native sentiment scores by ticker |
| `RiskManagement.tsx` | Live risk parameter editor (SL/TP/confidence sliders) |
| `PortfolioOverview.tsx` | Account value, positions, unrealized P&L |
| `CodexDebugger.tsx` | System-level diagnostics and log viewer |

Backend communication: REST calls to `FastAPI` + WebSocket for real-time updates.

---

## Key Configuration

All secrets via environment variables (`.env` in project root, never committed):

| Variable | Purpose |
|---|---|
| `ACTIVE_BROKER` | `alpaca` (default) or `webull` |
| `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` | Alpaca credentials |
| `WEBULL_APP_KEY` / `WEBULL_APP_SECRET` / `WEBULL_ACCOUNT_ID` | Webull credentials |
| `SUPABASE_URL` / `SUPABASE_SERVICE_KEY` | Database connection |
| `NEWSAPI_KEY` / `ALPHA_VANTAGE_API_KEY` | Sentiment data APIs |
| `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET` | Reddit sentiment source |

---

## Trained Models

20+ tickers have trained XGBoost models stored in `models/`:

```
AAL  AAPL  AMD  AMZN  AVGO  F  GOOG  HOOD  INTC  IONQ
MARA  MDAI  META  MSFT  NFLX  NIO  NVDA  ORCL  PLTR  ...
```

Retraining scripts:
- `retrain_single_model.py` — retrain one ticker
- `retrain_three_class_models.py` — retrain all tickers (3-class BUY/HOLD/SELL)
- `batch_retrain.py` — parallel batch retraining
- `manage_models.py` — inspect, compare, and promote model versions

Auto-retrainer (`financio_src/model/auto_retrainer.py`) monitors model performance drift and triggers retraining when accuracy drops below the minimum F1 threshold.

---

## Running Locally

```bash
# Python environment
source .venv/bin/activate          # or: uv sync

# Backend API
cd backend && python -m uvicorn main:app --reload --port 8001

# Frontend dashboard
cd dashboard && npm run dev         # http://localhost:5173

# Run all trading bots
python run_multi_bot_production.py

# Generate backtest charts
python backtest_strategies.py --start 2020-01-01

# Retrain a single model
python retrain_single_model.py --ticker AAPL
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Trading engine | Python 3.12, XGBoost 3.0, stable-baselines3, TensorFlow/Keras |
| Feature engineering | pandas, pandas-ta, numpy, scipy |
| Backtesting charts | Plotly 5.x (self-contained HTML) |
| Broker APIs | alpaca-py, webull-openapi-python-sdk |
| Sentiment | VADER, TextBlob, FinBERT (via Morgans), PRAW, Tweepy |
| Backend API | FastAPI, Pydantic, Uvicorn |
| Database | Supabase (PostgreSQL + real-time subscriptions) |
| Frontend | React 18, TypeScript, Vite, ShadCN UI, Tailwind |
| Containerization | Docker, docker-compose |
| Hyperparameter tuning | Optuna |
| Model serving | joblib, XGBoost native JSON format |
