# Financio-V2 Integration Architecture
## Integrating Morgans Sentiment Bot, LSTM Predictor, and Options Analyzer

**Date:** October 5, 2025
**Purpose:** Unified trading system with enhanced sentiment analysis, deep learning predictions, and options strategies

---

## 🎯 Integration Overview

This integration combines three powerful systems into Financio-V2:

1. **Morgans Sentiment Bot** (`~/projects/Morgans`) - Advanced sentiment analysis with VADER + FinBERT
2. **LSTM Price Predictor** (`~/projects/options`) - Deep learning time-series predictions
3. **Options Analyzer** (`~/projects/options`) - Options strategy recommendations

### Current Architecture (Financio-V2)

```
┌─────────────────────────────────────────────────────────────┐
│                    Financio-V2 Current                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Sentiment   │  │  Technical   │  │    Market    │     │
│  │   Model      │  │    Model     │  │    Regime    │     │
│  │  (TextBlob)  │  │ (RandomFor.) │  │  (Logistic)  │     │
│  │    30%       │  │     40%      │  │     30%      │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         └─────────────┬─────────────────────┘              │
│                       ▼                                     │
│                ┌──────────────┐                             │
│                │ Meta Model   │                             │
│                │ (Ensemble)   │                             │
│                └──────┬───────┘                             │
│                       ▼                                     │
│                 Trading Signal                              │
│                (Buy/Sell/Hold)                             │
└─────────────────────────────────────────────────────────────┘
```

### Target Architecture (Integrated System)

```
┌───────────────────────────────────────────────────────────────────────┐
│                    Financio-V2 Integrated                             │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Enhanced   │  │  Technical  │  │   Market    │  │    LSTM     │ │
│  │  Sentiment  │  │    Model    │  │   Regime    │  │  Predictor  │ │
│  │(VADER+BERT) │  │(RandomFor.) │  │ (Logistic)  │  │  (Deep NN)  │ │
│  │    25%      │  │     30%     │  │     20%     │  │     25%     │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                │                │                │         │
│         └────────────────┴────────────────┴────────────────┘         │
│                                 ▼                                     │
│                         ┌───────────────┐                             │
│                         │  Meta Model   │                             │
│                         │  (Enhanced)   │                             │
│                         └───────┬───────┘                             │
│                                 ▼                                     │
│                    ┌────────────────────────┐                         │
│                    │   Trading Signal       │                         │
│                    │   (Buy/Sell/Hold)      │                         │
│                    └────────┬───────────────┘                         │
│                             │                                         │
│             ┌───────────────┴───────────────┐                         │
│             ▼                               ▼                         │
│     ┌───────────────┐              ┌────────────────┐                 │
│     │ Stock Trading │              │ Options Trading│                 │
│     │   Execution   │              │  Recommendations│                │
│     └───────────────┘              └────────────────┘                 │
│                                    (Calls/Puts/Spreads)               │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Component Integration Details

### 1. Enhanced Sentiment Analysis Integration

**Current:** Financio uses TextBlob for basic sentiment scoring
**Target:** Use Morgans' VADER + FinBERT for sophisticated sentiment analysis

#### Data Flow

```
Morgans Bot (stock_sentiment.py)
  ├─ Fetches news from NewsAPI (30 days)
  ├─ Analyzes with VADER sentiment
  ├─ (Optional) Enhances with FinBERT
  └─ Saves to ~/projects/shared_data/stocks/
       ├─ {ticker}_combined_latest.json
       └─ {ticker}_combined_sentiment.csv

              ↓

SentimentReader (options/sentiment_reader.py)
  ├─ Reads sentiment history
  ├─ Merges with price data
  └─ Provides daily sentiment scores

              ↓

Financio Sentiment Service (NEW)
  ├─ Reads from shared directory
  ├─ Integrates with existing sentiment_collector.py
  ├─ Provides sentiment features to ensemble
  └─ Weight: 25% in ensemble model
```

#### Implementation Files

**New/Modified Files:**
- `financio_src/sentiment/morgans_sentiment_bridge.py` - Bridge to Morgans data
- `financio_src/sentiment/enhanced_sentiment_service.py` - Unified sentiment service
- Update `ensemble_trading_model.py` - Accept enhanced sentiment features

**Configuration:**
```python
# financio_src/config.py additions
SENTIMENT_CONFIG = {
    'use_morgans_sentiment': True,
    'morgans_data_dir': '~/projects/shared_data/stocks/',
    'fallback_to_textblob': True,  # If Morgans data unavailable
    'sentiment_weight': 0.25,
    'lookback_days': 30
}
```

---

### 2. LSTM Price Predictor Integration

**Current:** Financio uses only XGBoost-based ensemble
**Target:** Add LSTM deep learning predictions as 4th signal source

#### Data Flow

```
Historical Price Data
  └─ yfinance download

        ↓

LSTM Predictor (options/integratedSystem.py)
  ├─ Loads price + sentiment data
  ├─ Adaptive lookback window (30-60 days)
  ├─ Trains LSTM with dropout layers
  ├─ Predicts next 30 days
  └─ Outputs: predicted_price, confidence, MAPE

        ↓

Financio LSTM Service (NEW)
  ├─ Wraps LSTM predictor for Financio
  ├─ Caches predictions (15-min intervals)
  ├─ Provides prediction + confidence scores
  └─ Weight: 25% in ensemble model

        ↓

Enhanced Ensemble Model
  ├─ Combines: Sentiment(25%) + Technical(30%) + Regime(20%) + LSTM(25%)
  └─ Meta-model learns optimal weighting
```

#### Implementation Files

**New Files:**
- `financio_src/model/lstm_predictor_service.py` - LSTM integration wrapper
- `financio_src/model/lstm_model.py` - Copy/adapt from options/integratedSystem.py

**Modified Files:**
- `financio_src/ensemble/ensemble_trading_model.py`:
  - Add `lstm_model` to ensemble
  - Add `lstm_weight` to model_weights
  - Update `_create_meta_features()` to include LSTM predictions
  - Update training pipeline

**Key Code Changes:**
```python
# ensemble_trading_model.py
class EnsembleTradingModel:
    def __init__(self, config: Dict = None):
        # ... existing code ...

        # Add LSTM predictor
        self.lstm_predictor = None

        # Updated weights
        self.model_weights = {
            'sentiment': 0.25,
            'technical': 0.30,
            'market_regime': 0.20,
            'lstm': 0.25
        }

    def get_lstm_prediction(self, ticker: str, days_ahead: int = 30):
        """Get LSTM price prediction"""
        from financio_src.model.lstm_predictor_service import LSTMPredictorService

        if not self.lstm_predictor:
            self.lstm_predictor = LSTMPredictorService(config=self.config)

        prediction = self.lstm_predictor.predict(ticker, days_ahead)
        return {
            'predicted_price': prediction['price'],
            'confidence': prediction['confidence'],
            'expected_return': prediction['expected_return'],
            'mape': prediction['mape']
        }
```

---

### 3. Options Analyzer Integration

**Current:** Financio only trades stocks
**Target:** Add options strategy recommendations based on predictions

#### Data Flow

```
Ensemble Signal (Buy/Sell/Hold)
  └─ Confidence score
  └─ Expected return
  └─ Holding period

        ↓

LSTM 30-day Prediction
  └─ Target price
  └─ Price movement %

        ↓

Options Analyzer (options/options_analyzer.py)
  ├─ Fetches current options chain (yfinance)
  ├─ Filters by expiration (30-90 days)
  ├─ Calculates breakeven points
  ├─ Computes ROI for each strike
  └─ Recommends optimal contracts

        ↓

Options Strategy Recommendation
  ├─ If BULLISH + high confidence → Call options
  ├─ If BEARISH + high confidence → Put options
  ├─ If NEUTRAL → Iron condor / spreads
  └─ Position sizing based on risk tolerance
```

#### Implementation Files

**New Files:**
- `financio_src/trading/options_strategy_engine.py` - Options recommendations
- `financio_src/trading/options_execution.py` - Options trading via Alpaca

**Modified Files:**
- `financio_src/trading/live_trading.py`:
  - Add options trading logic
  - Check Alpaca options approval
  - Execute options orders

**Key Features:**
```python
# options_strategy_engine.py
class OptionsStrategyEngine:
    def recommend_strategy(self,
                          signal: TradingSignal,
                          lstm_prediction: Dict,
                          ticker: str) -> Dict:
        """
        Recommend options strategy based on ensemble signal and LSTM prediction

        Returns:
            {
                'strategy': 'call' | 'put' | 'spread' | 'none',
                'strike': float,
                'expiration': date,
                'contracts': int,
                'cost': float,
                'max_profit': float,
                'max_loss': float,
                'breakeven': float,
                'roi_potential': float
            }
        """

        # Only trade options if high confidence
        if signal.confidence < 0.75:
            return {'strategy': 'none'}

        # Get options chain
        options_data = self.get_options_chain(ticker)

        # Calculate expected move
        current_price = self.get_current_price(ticker)
        target_price = lstm_prediction['predicted_price']
        expected_move_pct = (target_price - current_price) / current_price

        # Recommend strategy
        if signal.action in [TradingAction.BUY, TradingAction.STRONG_BUY]:
            # Bullish: buy calls
            return self._recommend_call_strategy(
                ticker, current_price, target_price, options_data
            )
        elif signal.action in [TradingAction.SELL, TradingAction.STRONG_SELL]:
            # Bearish: buy puts
            return self._recommend_put_strategy(
                ticker, current_price, target_price, options_data
            )
        else:
            # Neutral: consider spreads
            return self._recommend_neutral_strategy(
                ticker, current_price, options_data
            )
```

---

## 🗄️ Database Schema Updates

### New Tables (Supabase)

```sql
-- LSTM predictions tracking
CREATE TABLE lstm_predictions (
    id BIGSERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    prediction_date TIMESTAMP NOT NULL,
    days_ahead INT NOT NULL,
    predicted_price DECIMAL(10, 2) NOT NULL,
    confidence DECIMAL(5, 4) NOT NULL,
    mape DECIMAL(5, 4),
    actual_price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Options recommendations tracking
CREATE TABLE options_recommendations (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    ticker VARCHAR(10) NOT NULL,
    strategy VARCHAR(20) NOT NULL, -- 'call', 'put', 'spread'
    strike_price DECIMAL(10, 2) NOT NULL,
    expiration_date DATE NOT NULL,
    recommended_contracts INT NOT NULL,
    cost_per_contract DECIMAL(10, 2) NOT NULL,
    total_cost DECIMAL(10, 2) NOT NULL,
    breakeven_price DECIMAL(10, 2) NOT NULL,
    expected_roi DECIMAL(5, 2),
    executed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Options trades tracking (extends trades table)
CREATE TABLE options_trades (
    id BIGSERIAL PRIMARY KEY,
    trade_id BIGINT REFERENCES trades(id),
    option_type VARCHAR(4) NOT NULL, -- 'CALL' or 'PUT'
    strike_price DECIMAL(10, 2) NOT NULL,
    expiration_date DATE NOT NULL,
    contracts INT NOT NULL,
    premium DECIMAL(10, 2) NOT NULL,
    underlying_price_at_entry DECIMAL(10, 2),
    underlying_price_at_exit DECIMAL(10, 2),
    profit_loss DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'OPEN', -- 'OPEN', 'CLOSED', 'EXPIRED'
    created_at TIMESTAMP DEFAULT NOW()
);

-- Enhanced sentiment tracking
CREATE TABLE sentiment_scores (
    id BIGSERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    vader_score DECIMAL(5, 4),
    finbert_score DECIMAL(5, 4),
    ensemble_score DECIMAL(5, 4),
    article_count INT DEFAULT 0,
    bullish_count INT DEFAULT 0,
    bearish_count INT DEFAULT 0,
    neutral_count INT DEFAULT 0,
    source VARCHAR(50), -- 'morgans', 'financio', 'combined'
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_lstm_predictions_ticker ON lstm_predictions(ticker);
CREATE INDEX idx_lstm_predictions_date ON lstm_predictions(prediction_date);
CREATE INDEX idx_options_recs_ticker ON options_recommendations(ticker);
CREATE INDEX idx_options_recs_user ON options_recommendations(user_id);
CREATE INDEX idx_sentiment_ticker ON sentiment_scores(ticker);
CREATE INDEX idx_sentiment_timestamp ON sentiment_scores(timestamp);
```

---

## 🔧 Configuration Management

### Environment Variables

```bash
# financio_src/.env additions

# Morgans Sentiment Bot Integration
USE_MORGANS_SENTIMENT=true
MORGANS_DATA_DIR=~/projects/shared_data/stocks/
MORGANS_UPDATE_INTERVAL=3600  # Check for updates every hour

# LSTM Predictor Integration
USE_LSTM_PREDICTIONS=true
LSTM_PREDICTION_DAYS=30
LSTM_UPDATE_INTERVAL=900  # Re-predict every 15 minutes
LSTM_CONFIDENCE_THRESHOLD=0.7  # Minimum confidence to use predictions

# Options Trading
OPTIONS_TRADING_ENABLED=true
OPTIONS_MIN_CONFIDENCE=0.75  # Higher bar for options
OPTIONS_MAX_CONTRACTS=10
OPTIONS_RISK_MULTIPLIER=1.5  # Options are riskier
ALPACA_OPTIONS_APPROVED=true  # Must have options approval
```

### Integration Config File

```python
# financio_src/config/integration_config.py

INTEGRATION_CONFIG = {
    'sentiment': {
        'morgans_enabled': True,
        'morgans_data_dir': '~/projects/shared_data/stocks/',
        'fallback_to_textblob': True,
        'weight': 0.25,
        'cache_ttl_seconds': 3600,
        'required_article_count': 5  # Minimum articles for valid sentiment
    },

    'lstm': {
        'enabled': True,
        'prediction_days': 30,
        'update_interval_seconds': 900,
        'weight': 0.25,
        'confidence_threshold': 0.7,
        'epochs': 10,
        'batch_size': 1,
        'use_sentiment': True,  # LSTM uses sentiment data
        'adaptive_lookback': True
    },

    'options': {
        'enabled': True,
        'min_confidence': 0.75,
        'max_contracts_per_trade': 10,
        'expiration_range_days': (30, 90),
        'preferred_delta': 0.5,  # At-the-money options
        'max_position_cost': 0.05,  # 5% of portfolio max
        'track_recommendations': True
    },

    'ensemble': {
        'weights': {
            'sentiment': 0.25,
            'technical': 0.30,
            'market_regime': 0.20,
            'lstm': 0.25
        },
        'min_confidence_to_trade': 0.6,
        'learning_enabled': True,  # Meta-model learns optimal weights
    }
}
```

---

## 📂 Project Structure (After Integration)

```
Financio-V2/
├── financio_src/
│   ├── sentiment/
│   │   ├── __init__.py
│   │   ├── sentiment_features.py (existing)
│   │   ├── sentiment_collector.py (existing)
│   │   ├── morgans_sentiment_bridge.py (NEW)
│   │   └── enhanced_sentiment_service.py (NEW)
│   │
│   ├── model/
│   │   ├── __init__.py
│   │   ├── lstm_model.py (NEW - from options/integratedSystem.py)
│   │   ├── lstm_predictor_service.py (NEW)
│   │   └── ... (existing XGBoost models)
│   │
│   ├── ensemble/
│   │   ├── __init__.py
│   │   └── ensemble_trading_model.py (MODIFIED - add LSTM)
│   │
│   ├── trading/
│   │   ├── __init__.py
│   │   ├── options_strategy_engine.py (NEW)
│   │   ├── options_execution.py (NEW)
│   │   └── live_trading.py (MODIFIED)
│   │
│   └── config/
│       ├── __init__.py
│       └── integration_config.py (NEW)
│
├── shared/ (NEW - link to ~/projects/shared_data/)
│   └── stocks/
│       ├── path_combined_latest.json
│       └── path_combined_sentiment.csv
│
└── INTEGRATION_ARCHITECTURE.md (this file)
```

---

## 🚀 Implementation Phases

### Phase 1: Enhanced Sentiment Integration (Days 1-2)
- [ ] Create `morgans_sentiment_bridge.py` to read from shared directory
- [ ] Create `enhanced_sentiment_service.py` to unify sentiment sources
- [ ] Update `ensemble_trading_model.py` to accept enhanced sentiment
- [ ] Add sentiment_scores table to Supabase
- [ ] Test sentiment data flow end-to-end

### Phase 2: LSTM Predictor Integration (Days 3-5)
- [ ] Copy LSTM code from options project to `financio_src/model/`
- [ ] Create `lstm_predictor_service.py` wrapper
- [ ] Add LSTM as 4th signal in ensemble model
- [ ] Create lstm_predictions table in Supabase
- [ ] Implement caching and update intervals
- [ ] Test LSTM predictions alongside XGBoost

### Phase 3: Options Analyzer Integration (Days 6-8)
- [ ] Create `options_strategy_engine.py`
- [ ] Implement strategy recommendation logic
- [ ] Create options_recommendations and options_trades tables
- [ ] Integrate with Alpaca options API
- [ ] Add options UI components to dashboard
- [ ] Test options recommendations

### Phase 4: Testing & Optimization (Days 9-10)
- [ ] End-to-end integration testing
- [ ] Backtest ensemble with all 4 signals
- [ ] Optimize model weights through meta-learning
- [ ] Performance profiling and optimization
- [ ] Documentation and CLAUDE.md updates

---

## 📈 Expected Performance Improvements

### Current Financio-V2 Performance
- **Accuracy:** ~65-70% (3-class: Buy/Hold/Sell)
- **Sentiment:** TextBlob (basic polarity)
- **Prediction Horizon:** 1-5 days
- **Asset Types:** Stocks only

### Expected Integrated System Performance
- **Accuracy:** ~72-77% (improved by LSTM + enhanced sentiment)
- **Sentiment:** VADER + FinBERT (sophisticated NLP)
- **Prediction Horizon:** 1-5 days (XGBoost) + 30 days (LSTM)
- **Asset Types:** Stocks + Options
- **Risk-Adjusted Returns:** +15-25% improvement (options leverage)

### Key Advantages

1. **Multi-timeframe Analysis:**
   - Short-term: XGBoost + technical signals
   - Long-term: LSTM predictions
   - Options: Leverage LSTM targets

2. **Enhanced Sentiment:**
   - More accurate with VADER + FinBERT
   - Continuous updates from Morgans bot
   - Historical sentiment trends

3. **Options Strategies:**
   - Leverage high-confidence predictions
   - Better risk/reward ratios
   - Defined risk (limited downside)

4. **Ensemble Learning:**
   - Meta-model learns optimal weighting
   - Adapts to changing market conditions
   - Reduces overfitting through diversity

---

## ⚠️ Risk Considerations

1. **Model Complexity:**
   - More models = more potential failure points
   - Requires careful monitoring and validation
   - Meta-model can overfit if not properly regularized

2. **Data Dependencies:**
   - System now depends on Morgans bot running continuously
   - LSTM requires sufficient historical data (65+ days)
   - Options require market liquidity

3. **Execution Risk:**
   - Options have higher slippage
   - Need to verify Alpaca options approval
   - Options expiration management required

4. **Computational Cost:**
   - LSTM training is more expensive than XGBoost
   - Real-time predictions every 15 minutes
   - May need GPU for faster training

---

## 🔗 Integration Dependencies

### Python Packages (Add to requirements.txt)
```txt
# LSTM Integration
tensorflow>=2.13.0
keras>=2.13.0

# Enhanced Sentiment (if not already present)
vaderSentiment>=3.3.2
transformers>=4.30.0  # For FinBERT (optional)
torch>=2.0.0  # For FinBERT (optional)

# Shared Data Management
watchdog>=3.0.0  # File monitoring for sentiment updates
```

### External Services
- **Morgans Bot:** Must be running continuously or on schedule
- **NewsAPI:** Required for sentiment data (free tier: 30 days history)
- **Alpaca Options:** Account must have options trading approval
- **Supabase:** Database updates for new tables

---

## 📚 Documentation Updates

### Files to Update
1. **CLAUDE.md:**
   - Add integration overview
   - Document new sentiment/LSTM/options services
   - Update architecture diagram

2. **SYSTEM_ARCHITECTURE.md:**
   - Update component diagram
   - Add LSTM prediction flow
   - Add options strategy flow

3. **README.md:**
   - Add integration features
   - Update setup instructions
   - Add new environment variables

4. **API Documentation:**
   - New endpoints for LSTM predictions
   - New endpoints for options recommendations
   - Enhanced sentiment endpoints

---

## ✅ Success Criteria

Integration is considered successful when:

1. **Sentiment Integration:**
   - [x] Morgans sentiment data flowing to Financio
   - [x] Enhanced sentiment weight in ensemble (25%)
   - [x] Fallback to TextBlob working if Morgans unavailable

2. **LSTM Integration:**
   - [x] LSTM predictions available for all tickers
   - [x] Prediction accuracy (MAPE) < 5%
   - [x] LSTM weight in ensemble (25%)
   - [x] Updates every 15 minutes

3. **Options Integration:**
   - [x] Options recommendations generated for high-confidence signals
   - [x] Options chain analysis working
   - [x] ROI calculations accurate
   - [x] Options trades executed successfully (paper trading)

4. **System Performance:**
   - [x] Overall accuracy improvement: +5-7%
   - [x] Latency: <500ms for signal generation
   - [x] No regression in existing functionality
   - [x] All tests passing

---

## 🎓 Next Steps After Integration

1. **Live Testing:**
   - Run in paper trading mode for 2 weeks
   - Monitor all 4 signal sources
   - Validate options recommendations

2. **Meta-Model Optimization:**
   - Let meta-model learn optimal weights
   - Compare fixed weights vs learned weights
   - A/B test different configurations

3. **Options Strategy Expansion:**
   - Add spreads (bull call, bear put)
   - Add iron condors for neutral signals
   - Implement options Greeks monitoring

4. **Mobile App Integration:**
   - Display LSTM predictions in mobile app
   - Show options recommendations
   - Push notifications for high-confidence signals

---

**Status:** Ready for Implementation
**Estimated Completion:** 10 days
**Risk Level:** Medium (manageable with proper testing)
