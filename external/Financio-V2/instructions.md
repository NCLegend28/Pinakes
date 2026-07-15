-- Template --
### 🎯 Current Focus: [Task Name]
**Priority**: High/Medium/Low
**Context**: Why this matters, what's broken/missing
**Approach**: High-level strategy, not step-by-step
**Dependencies**: What needs to be working first
**Success Criteria**: How to know it's done
-- Template --

### 🎯 Current Focus: Multi-Bot Architecture and Integration
**Priority**: High
**Context**: You want multiple bots, each with specialized strategies (ML, trend-based, hybrid), distinct models (XGBoost, PPO, etc.), and tailored hyperparameters. These bots need to communicate and function cohesively to improve overall trading performance.
**Approach**: Develop a standardized architecture with clearly defined input-output interfaces, enabling bots to share signals, confidence scores, and state management effectively.
**Dependencies**:

Fully functional single-bot pipelines (training, backtesting, live trading)

Robust API and data processing structure
**Success Criteria**:

Multiple bots with distinct configurations operate simultaneously.

Bots share insights, improving collective decision-making (ensemble behavior).

Clear improvement in overall trading accuracy, risk management, or return metrics compared to isolated bots.

## 📝 Technical Notes:
Establish centralized logging and state management for transparency and debugging.

Clearly define data and signal formats to prevent miscommunication between bots.

Avoid tightly coupling bots; ensure each bot remains modular and independently testable.

### 🎯 Current Focus: Hyperparameter Optimization Pipeline
**Priority**: Medium
**Context**: Each bot type (trend, ML, hybrid) needs tailored hyperparameters for optimal performance.
**Approach**: Integrate automated hyperparameter tuning using Optuna and custom scripts for systematic optimization.
Dependencies:

Stable data fetching (fetch_price_data) and feature engineering pipeline (generate_features).

Operational backtesting (backtest) function.
**Success Criteria**:

Automated tuning produces reliably optimized hyperparameters.

Documented improvements in bot performance (F1 scores, Sharpe ratios).

## 📝 Technical Notes:
Ensure reproducibility by saving hyperparameter configurations and performance results.

Consider computational overhead; prioritize key hyperparameters affecting performance significantly.

### 🎯 Current Focus: Strategy Management and Dynamic Selection
**Priority**: High
**Context**: Bots require the ability to dynamically select appropriate strategies based on market conditions or model confidence.
**Approach**: Implement decision logic (choose_strategy) that evaluates signals from multiple bots, selecting strategies based on current market trends, volatility, and bot-specific confidence.
**Dependencies**:

Well-defined strategy evaluation criteria (ML confidence, EMA crossover signals, volatility measures).

Reliable feature generation (add_technical_indicators, candlestick_pattern).
**Success Criteria**:

Bots dynamically adapt strategies, evidenced by reduced losses or improved returns under varied market conditions.

## 📝 Technical Notes:
Include fallback mechanisms for when signals conflict or are uncertain.

Maintain clear logging of decisions for transparency and debugging.

### 🎯 Current Focus: Inter-Bot Communication Framework
**Priority**: High
**Context**: Bots must efficiently exchange data such as predictions, trade signals, and confidence scores.
**Approach**: Design a lightweight messaging or API-based system enabling rapid data exchange with minimal latency.
**Dependencies**:

Consistent data standards and formats (JSON, CSV, SQLite).

Robust API infrastructure or message broker system (e.g., Redis, Kafka).
**Success Criteria**:

Seamless data exchange demonstrated via synchronized bot actions.

Minimal latency (under 1 second) for data exchanges.

## 📝 Technical Notes:
Implement error handling and recovery mechanisms to address communication failures.

Clearly document API endpoints and expected data formats.

### 🚫 Don't Touch:
Core components (fetch_prices.py, price_features.py, featureManager.py) already tested and working.

Stable single-bot live trading loop (live_trading.py) until multi-bot framework is robust.

Functional frontend integration (PortfolioOverview.tsx) and established API structure.