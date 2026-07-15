# Financio-V2 Component Guide

## 🏗️ System Components Deep Dive

### 📡 External Data Sources

#### **Alpaca Trading API**
- **Purpose**: Primary trading execution and market data source
- **Functionality**:
  - Real-time and historical price data
  - Order execution (Buy/Sell)
  - Portfolio and position management
  - Account information and balance tracking
- **Configuration**: Paper trading enabled by default, live trading for production
- **Rate Limits**: Built-in rate limiting to prevent API quota exhaustion
- **Files**: `financio_src/trading/live_trading.py`, `financio_src/config.py`

#### **Market Data APIs**
- **Purpose**: Supplementary market data for enhanced decision-making
- **Data Types**:
  - Extended hours trading data
  - News sentiment analysis
  - Sector performance metrics
  - Volume and volatility indicators
- **Files**: `financio_src/data/fetch_prices.py`, `financio_src/features/`

#### **Macro Economic Data**
- **Purpose**: Economic indicators for market context
- **Sources**: Federal Reserve data, economic calendars, sentiment indices
- **Files**: `financio_src/features/macro_features.py`

---

### 🖥️ User Interface Layer

#### **React Dashboard (`dashboard/`)**
- **Technology Stack**: React 18, TypeScript, Vite, shadcn-ui
- **Port**: 5173 (development), 8080 (production)
- **Key Components**:
  - `ActiveBots.tsx`: Real-time bot status and control panel
  - `TradingChart.tsx`: Interactive price charts with technical indicators
  - `MultiBotDashboard.tsx`: Overview of all trading bots
  - `RiskManagement.tsx`: Portfolio risk metrics and controls
  - `CodexDebugger.tsx`: Advanced debugging and system monitoring

**Data Flow**: Dashboard → FastAPI Backend → Supabase → Trading Bots

#### **Mobile App (`mobile-app/`)**
- **Technology**: React Native with TypeScript
- **Platform Support**: iOS and Android
- **Features**:
  - Portfolio monitoring
  - Trade notifications
  - Bot management
  - Biometric authentication
  - Real-time alerts

#### **REST API (`backend/main.py`)**
- **Framework**: FastAPI with automatic OpenAPI documentation
- **Port**: 8000 (development), 8001 (production)
- **Key Endpoints**:
  - `/api/dashboard-data`: Complete dashboard data
  - `/api/trades`: Trading history
  - `/api/active-bots`: Bot status and management
  - `/api/portfolio-summary`: Portfolio metrics
  - `/api/risk-metrics`: Risk management data

---

### 🧠 Application Layer

#### **FastAPI Backend (`backend/`)**
- **Primary Functions**:
  - Aggregate trading data from multiple sources
  - Provide unified API for frontend applications
  - Calculate real-time portfolio metrics
  - Manage user authentication and authorization
  - Handle multi-bot coordination

**Key Modules**:
- `main.py`: Core API endpoints and CORS configuration
- `equity_data_extractor.py`: Real-time equity calculations
- `live_equity_calculator.py`: Alpaca API integration for live data
- `supabase_config.py`: Database abstraction layer

#### **Multi-Bot Manager (`financio_src/multi_bot/`)**
- **Purpose**: Coordinate multiple trading bots to prevent conflicts
- **Components**:
  - `bot_manager.py`: Individual bot lifecycle management
  - `integration.py`: Cross-bot coordination and conflict resolution
  - `communication.py`: Redis-based inter-bot messaging
  - `strategy_manager.py`: Strategy allocation and optimization

**Coordination Logic**:
- Prevents multiple bots from trading the same ticker
- Manages shared capital allocation
- Handles bot failures and recovery
- Optimizes strategy distribution across market conditions

#### **Enhanced Risk Manager (`financio_src/risk_management/`)**
- **Core Features**:
  - Dynamic position sizing based on market volatility
  - Portfolio-wide risk limits and controls
  - ATR-based stop-loss and take-profit optimization
  - Confidence-weighted position sizing
  - Maximum drawdown protection

**Risk Parameters** (configurable in `config.py`):
- `SL_ATR_MULTIPLIER`: 3.5 (Stop-loss distance)
- `TP_ATR_MULTIPLIER`: 4.5 (Take-profit distance)
- `MIN_PROFIT_THRESHOLD`: 1.5% (Minimum profit to close)
- `MAX_LOSSES`: 3 (Maximum consecutive losses before pause)

---

### ⚡ Core Trading Engine

#### **Individual Trading Bots (`financio_src/trading/live_trading.py`)**
- **Architecture**: Each bot is an independent trading entity
- **Default Configuration**: 15 concurrent bots across rotation tickers
- **Bot Lifecycle**:
  1. Market data ingestion
  2. Feature calculation
  3. Model prediction
  4. Strategy application
  5. Risk management checks
  6. Order execution
  7. Position monitoring

**Long-Only Safety Features**:
- Prevents short selling on paper trading accounts
- Validates positions before sell orders
- Position quantity verification
- Enhanced error handling for trading restrictions

#### **ML Models (`financio_src/model/`)**
- **Primary Algorithm**: XGBoost gradient boosting classifiers
- **Model Performance**: 93.6% F1 accuracy on validation data
- **Prediction Classes**:
  - 0: Sell signal
  - 1: Hold (no action)
  - 2: Buy signal
- **Features**: 200+ technical indicators including:
  - Price-based: SMA, EMA, Bollinger Bands, RSI
  - Volume-based: OBV, Volume Profile, VWAP
  - Volatility: ATR, Volatility Ratio
  - Pattern Recognition: Support/Resistance levels

**Model Files Structure**:
```
models/
├── AAPL/
│   ├── AAPL_booster.json
│   ├── AAPL_feature_params.json
│   └── AAPL_model_params.json
├── TSLA/
└── ...
```

#### **Trading Strategies (`financio_src/strategy/`)**
- **Trend Strategy**: Swing point analysis with trendline fitting
- **ML Strategy**: XGBoost model predictions with confidence weighting
- **Hybrid Strategy**: Combined trend and ML signals with conflict resolution

**Strategy Selection Logic**:
```python
if trend_signal_strength > threshold and ml_confidence > 0.75:
    use_hybrid_strategy()
elif ml_confidence > 0.85:
    use_ml_strategy()
else:
    use_trend_strategy()
```

#### **Signal Processing (`financio_src/features/`)**
- **Technical Indicators**: RSI, MACD, Bollinger Bands, Stochastic
- **Custom Features**: Price momentum, volume patterns, volatility regimes
- **Feature Engineering Pipeline**:
  1. Raw data normalization
  2. Missing data handling
  3. Feature scaling and transformation
  4. Real-time feature calculation
  5. Model input preparation

---

### 📊 Data Processing Layer

#### **Data Fetcher (`financio_src/data/fetch_prices.py`)**
- **Primary Function**: Real-time and historical market data acquisition
- **Rate Limiting**: Intelligent API call management
- **Data Validation**: Price anomaly detection and correction
- **Caching**: Efficient data storage to minimize API calls

#### **Feature Engineering (`financio_src/features/`)**
- **Core Features**:
  - `price_features.py`: OHLCV-based indicators
  - `volume_features.py`: Volume profile and flow analysis
  - `volatility_features.py`: ATR, VIX-style calculations
  - `indicators.py`: Standard technical analysis tools

#### **Backtesting Engine (`financio_src/backtesting/`)**
- **Purpose**: Strategy validation on historical data
- **Metrics Calculated**:
  - Total return and annualized performance
  - Sharpe ratio and risk-adjusted returns
  - Maximum drawdown and recovery time
  - Win rate and profit factor
  - Trade distribution analysis

#### **Model Training (`financio_src/model/`)**
- **Automated Retraining**: Scheduled model updates based on performance
- **Hyperparameter Optimization**: Optuna-based parameter tuning
- **Cross-Validation**: Time-series aware validation splits
- **Performance Monitoring**: Continuous model performance tracking

---

### 💾 Data & Infrastructure

#### **Supabase PostgreSQL Database**
- **Primary Database**: Unified data storage for all user and trading data
- **Tables**:
  - `users`: User profiles and authentication
  - `trades`: Complete trading history with metadata
  - `bot_instances`: Multi-bot configuration and status
  - `portfolio_snapshots`: Time-series portfolio data
  - `notifications`: User alerts and system messages
  - `subscriptions`: Billing and subscription management

**Security Features**:
- Row Level Security (RLS) ensures data isolation
- User-specific data access patterns
- Service role for backend operations
- Encrypted connections and data at rest

#### **SQLite Local Storage**
- **Purpose**: High-frequency trading data and logs
- **Files**:
  - `financio_trades.db`: Local trade history
  - `trading_bot.db`: Bot-specific operational data
- **Usage**: Local development and backup storage

#### **Redis Communication**
- **Purpose**: Real-time inter-bot communication
- **Features**:
  - Pub/Sub messaging for signal distribution
  - Bot status broadcasting
  - Performance metrics sharing
  - Fault tolerance and recovery coordination

#### **File System Storage**
- **Model Storage**: Trained ML models in JSON format
- **Log Files**: Comprehensive system and trading logs
- **Configuration**: Environment-specific settings and parameters

---

### 📱 Mobile Backend

#### **Mobile API (`mobile_api/`)**
- **Framework**: FastAPI with GraphQL and WebSocket support
- **Authentication**: Supabase Auth integration
- **Features**:
  - Real-time trading updates via WebSocket
  - GraphQL for efficient data fetching
  - Push notifications for trade alerts
  - Biometric authentication support

#### **Authentication System**
- **Provider**: Supabase Auth
- **Methods**: Email/password, OAuth providers, magic links
- **Security**: JWT tokens with automatic refresh
- **Mobile Integration**: React Native Auth components

#### **Notification System**
- **Push Notifications**: Trade alerts, portfolio updates, system status
- **In-App Notifications**: Real-time dashboard updates
- **Email Notifications**: Daily summaries and critical alerts

---

## 🔄 Data Flow Examples

### Example 1: New Trade Execution Flow

```
1. Market Data Ingestion:
   Alpaca API → Data Fetcher → Feature Engineering (1-2 seconds)

2. Signal Generation:
   Features → ML Model → Trading Strategy → Signal (< 1 second)

3. Risk Management:
   Signal → Risk Manager → Position Sizing → Approval (< 1 second)

4. Order Execution:
   Approved Signal → Trading Bot → Alpaca API → Order Confirmation (2-5 seconds)

5. Data Persistence:
   Order Confirmation → Database Update → Dashboard Update (1-2 seconds)

6. Communication:
   Trade Event → Redis → Other Bots → Dashboard (< 1 second)

Total: 5-11 seconds from market data to executed trade
```

### Example 2: Dashboard Data Flow

```
1. User Request:
   Dashboard Component → API Request (REST/GraphQL)

2. Backend Processing:
   FastAPI → Supabase Query → Data Aggregation

3. Real-time Updates:
   WebSocket Connection → Live Trade Updates → Dashboard

4. Caching:
   Frequently accessed data cached in Redis for < 100ms response
```

### Example 3: Multi-Bot Coordination

```
1. Bot Signal Generation:
   Bot A generates BUY signal for AAPL

2. Communication:
   Bot A → Redis → Multi-Bot Manager

3. Conflict Resolution:
   Manager checks if other bots have AAPL positions/signals

4. Decision:
   If no conflicts: Approve trade
   If conflicts: Apply priority/risk rules

5. Execution:
   Approved signal → Risk Manager → Order Execution
```

This architecture enables Financio-V2 to process thousands of signals per minute while maintaining data consistency, risk management, and real-time user experience across web and mobile platforms.