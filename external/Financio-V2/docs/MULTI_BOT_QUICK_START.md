# 🚀 Financio-V2 Multi-Bot Quick Start Guide

## 📋 Prerequisites

1. **Redis Server** (installed and running)
```bash
brew install redis
brew services start redis
```

2. **Python Dependencies**
```bash
pip install redis optuna
```

3. **Existing Financio-V2 System** (all models trained and operational)

---

## 🏃‍♂️ Quick Start Commands

### 1. **Test Multi-Bot System**
```bash
# Test signal generation and communication
python -m tests.test_multi_bot_signals

# Expected output: 48 bots created, signals published, consensus reached
```

### 2. **Monitor System Status**
```bash
# Interactive monitoring
python multi_bot_monitor.py --mode interactive

# One-time status check
python multi_bot_monitor.py --mode once

# Continuous monitoring (auto-refresh every 30s)
python multi_bot_monitor.py --mode continuous --interval 30
```

### 3. **Run Hyperparameter Optimization**
```bash
# Optimize first 3 tickers with 50 trials each
python multi_bot_hyperopt.py --tickers AAPL TSLA NVDA --trials 50

# Optimize all tickers (warning: takes several hours)
python multi_bot_hyperopt.py --trials 100 --jobs 4
```

### 4. **Start Production Trading**
```bash
# Multi-bot mode (recommended)
python multi_bot_live_integration.py --mode multi_bot

# Hybrid mode (multi-bot + single-bot fallback)
python multi_bot_live_integration.py --mode hybrid

# Production system with full lifecycle management
python run_multi_bot_production.py
```

### 5. **Access Web Dashboard**
```bash
# Start backend (if not running)
cd backend && uvicorn main:app --reload --port 8000

# Start frontend (if not running)
cd dashboard && npm run dev

# Open dashboard: http://localhost:5173
# Click "Multi-Bot System" tab to see new interface
```

---

## 🔧 System Configuration

### **Bot Types Available**
- **ML Bots**: XGBoost-based machine learning predictions
- **Trend Bots**: Technical analysis and trend following
- **Hybrid Bots**: Combination of ML and trend strategies

### **Communication Backends**
- **Redis**: Production-grade messaging (recommended)
- **In-Memory**: Development fallback (automatic)

### **Strategy Types**
- `ML_AGGRESSIVE`: High-confidence ML signals
- `TREND_MOMENTUM`: Strong trend following
- `REVERSAL_HUNTING`: Counter-trend opportunities
- `VOLATILITY_BREAKOUT`: Volatility-based entries
- `CONSERVATIVE`: Lower-risk, balanced approach
- `HYBRID_ADAPTIVE`: Dynamic strategy mixing

---

## 📊 API Endpoints

### **Multi-Bot Status**
```bash
curl http://localhost:8000/api/multi-bot/status
```

### **Get Signals for Ticker**
```bash
curl http://localhost:8000/api/multi-bot/signals/AAPL?minutes=10
```

### **Initialize System**
```bash
curl -X POST http://localhost:8000/api/multi-bot/initialize
```

### **Performance Metrics**
```bash
curl http://localhost:8000/api/multi-bot/performance
```

---

## 🛠️ Advanced Usage

### **Custom Bot Configuration**
```python
from financio_src.multi_bot.integration import get_integration_manager

integration = get_integration_manager()
integration.initialize_multi_bot_system()

# Generate ensemble decision for specific ticker
decision = integration.generate_ensemble_decision("AAPL")
print(f"Decision: {decision}")
```

### **Real-Time Signal Monitoring**
```python
from financio_src.multi_bot.communication import get_communication_manager

comm = get_communication_manager()
aggregation = comm.get_signal_aggregation("TSLA", minutes=30)
print(f"Consensus: {aggregation.consensus} (strength: {aggregation.consensus_strength})")
```

### **Custom Strategy Implementation**
```python
from financio_src.multi_bot.bot_manager import BaseTradingBot, BotSignal
from datetime import datetime

class CustomBot(BaseTradingBot):
    def generate_signal(self, market_data):
        # Your custom logic here
        return BotSignal(
            bot_id=self.bot_id,
            ticker=self.ticker,
            signal_type="BUY",
            confidence=0.85,
            strategy="CUSTOM",
            timestamp=datetime.utcnow()
        )
```

---

## 🔍 Troubleshooting

### **Redis Connection Issues**
```bash
# Check Redis status
redis-cli ping  # Should return "PONG"

# Restart Redis if needed
brew services restart redis
```

### **Import Errors**
```bash
# Ensure project root is in Python path
export PYTHONPATH="/Users/mosley/projects/Financio-V2:$PYTHONPATH"
```

### **Signal Generation Issues**
```bash
# Test individual components
python -c "from financio_src.multi_bot.integration import get_integration_manager; print('✅ Integration OK')"
python -c "from financio_src.multi_bot.communication import get_communication_manager; print('✅ Communication OK')"
```

### **Model Loading Errors**
- Ensure models are trained: `python financio_src/train.py --symbol AAPL`
- Check model paths: `ls models/*/` should show booster.json files
- Verify three-class models: `python -m tests.test_three_class_training`

---

## 📈 Performance Tuning

### **System Optimization**
- **Redis Memory**: Increase Redis memory limit for high-frequency trading
- **Bot Count**: Start with 3 bots per ticker, scale up based on performance
- **Signal Frequency**: Adjust time windows based on market conditions

### **Strategy Tuning**
- Use hyperparameter optimization for best performance
- Monitor strategy effectiveness via dashboard
- Adjust confidence thresholds based on market volatility

---

## 🆘 Support & Resources

### **Documentation**
- `MULTI_BOT_COMPLETION_REPORT.md` - Complete system overview
- `financio_src/multi_bot/` - Core implementation code
- `instructions.md` - Original project requirements

### **Monitoring**
- Dashboard: http://localhost:5173 (Multi-Bot System tab)
- Logs: `logs/multi_bot_*.log`
- Redis Monitor: `redis-cli monitor`

### **Testing**
- `test_multi_bot_signals.py` - Signal generation tests
- `demo_multi_bot.py` - Full system demo
- API tests via Postman or curl

---

*Happy Trading! 🚀*
