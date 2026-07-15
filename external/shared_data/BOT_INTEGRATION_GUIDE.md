# Bot Integration Guide

**All bots now connected to shared configuration pipeline** 🤖

## Overview

Three trading/sentiment bots are now integrated with the shared data pipeline:

```
┌─────────────────────────────────────────────────────────────┐
│              SHARED DATA PIPELINE                           │
└─────────────────────────────────────────────────────────────┘

STOCKS:
  ~/projects/shared_data/stocks/tickers_config.py
    ├─→ Morgans Stock Sentiment Bot
    ├─→ Options Prediction Bot
    └─→ Financio Trading Bot

CRYPTO:
  ~/projects/shared_data/crypto/crypto_config.py
    ├─→ Morgans Crypto Sentiment Bot
    └─→ Future Crypto Trading Bots
```

---

## 1. Stock Bots Integration

### Shared Stock Config
Location: `~/projects/shared_data/stocks/tickers_config.py`

Contains:
- Ticker symbols (AAPL, TSLA, PATH, etc.)
- News queries for each ticker
- Investment amounts
- Prediction parameters
- Descriptions

### Integrated Stock Bots

#### A. **Morgans Stock Sentiment Bot**
Location: `~/projects/Morgans/stock_sentiment.py`

**Integration**: ✅ Complete

```python
from shared_data.stocks.tickers_config import get_stocks_to_track

STOCKS_TO_TRACK = get_stocks_to_track()
```

**Usage**:
```bash
cd ~/projects/Morgans
source .venv/bin/activate
python stock_sentiment.py
```

**Output**:
- Sentiment CSV files: `~/projects/shared_data/stocks/{ticker}_sentiment.csv`
- Latest sentiment JSON: `~/projects/shared_data/stocks/{ticker}_latest.json`

---

#### B. **Options Prediction Bot**
Location: `~/projects/options/stockPrediction_with_sentiment.py`

**Integration**: ✅ Complete

```python
from sentiment_reader import SentimentReader

reader = SentimentReader(data_type='stocks')
sentiment = reader.get_latest_sentiment('AAPL')
```

**Usage**:
```bash
cd ~/projects/options
source .venv/bin/activate
python stockPrediction_with_sentiment.py
```

**Output**:
- LSTM predictions with sentiment-enhanced features
- Prediction charts: `{ticker}_prediction_sentiment.png`
- RMSE/MAPE metrics

---

#### C. **Financio Trading Bot**
Location: `~/projects/Financio-V2/`

**Integration**: ✅ Complete (via `financio_ticker_integration.py`)

```python
from financio_ticker_integration import FinancioTickerManager

manager = FinancioTickerManager()
tickers = manager.get_trading_tickers()
config = manager.get_sentiment_config_for_tickers(tickers)
```

**Setup**:
```bash
cd ~/projects/Financio-V2
python financio_ticker_integration.py
```

**Output**:
- Syncs `current_tickers.txt` with shared config
- Provides sentiment collector config
- Real-time trading signals

---

## 2. Crypto Bots Integration

### Shared Crypto Config
Location: `~/projects/shared_data/crypto/crypto_config.py`

Contains:
- Crypto symbols (BTC, ETH, ADA, SOL, etc.)
- News queries for each coin
- Market cap ranks
- Categories (Major, Smart Contract, Payment, Meme)
- Social activity flags

### Integrated Crypto Bots

#### A. **Morgans Crypto Sentiment Bot**
Location: `~/projects/Morgans/automate.py`

**Integration**: ✅ Complete

```python
from shared_data.crypto.crypto_config import get_all_crypto, SENTIMENT_SETTINGS

COINS_TO_TRACK = [
    {'query': crypto['query'], 'symbol': crypto['symbol']}
    for crypto in get_all_crypto()
]
```

**Usage**:
```bash
cd ~/projects/Morgans
source .venv/bin/activate
python automate.py
```

**Output**:
- Sentiment CSV files: `~/projects/shared_data/sentiment/crypto/{coin}_sentiment.csv`
- Latest sentiment JSON: `~/projects/shared_data/sentiment/crypto/{coin}_latest.json`
- Runs every hour automatically

---

## 3. Automatic Ticker Discovery

### Wikipedia + SEC EDGAR Integration

**Location**: `~/projects/shared_data/stocks/`

**Discoverers**:
- `ticker_discovery.py` - Main discovery engine
- `wikipedia_scraper.py` - S&P 500, DJIA, NASDAQ-100
- `sec_edgar_scraper.py` - All 13,000+ public companies

**Auto-Update**:
- `ticker_auto_updater.py` - Scheduled auto-updates
- `setup_ticker_automation.sh` - Cron job setup

**Run Discovery**:
```bash
cd ~/projects/shared_data/stocks
python ticker_discovery.py
```

**Benefits**:
- Automatically discovers new trading opportunities
- Validates tickers (market cap, volume, liquidity)
- Scores by opportunity (momentum, volatility, sentiment potential)
- Updates all bots automatically

---

## 4. Data Flow Architecture

### Stock Pipeline

```
Wikipedia/SEC EDGAR
  ↓
Ticker Discovery (ticker_discovery.py)
  ↓
Shared Config (tickers_config.py)
  ↓
┌─────────────┬────────────────┬──────────────┐
↓             ↓                ↓              ↓
Morgans     Options        Financio      Auto-Updater
Sentiment   Prediction     Trading       (weekly)
Bot         Bot            Bot
  ↓             ↓                ↓
Sentiment   LSTM           Trading
CSV Files   Predictions    Signals
  ↓             ↓                ↓
Shared      Charts         P&L
Directory   & Metrics      Reports
```

### Crypto Pipeline

```
Manual Config / CoinGecko API
  ↓
Shared Config (crypto_config.py)
  ↓
Morgans Crypto Bot (automate.py)
  ↓
Sentiment CSV Files
  ↓
Future: Crypto Trading Bots
```

---

## 5. Configuration Management

### Adding New Stocks

**Method 1: Manual**
Edit `~/projects/shared_data/stocks/tickers_config.py`:

```python
{
    'symbol': 'NVDA',
    'query': 'NVDA OR "NVIDIA" OR "NVDA stock"',
    'investment': 300,
    'prediction_days': 30,
    'description': 'NVIDIA Corporation - Technology'
}
```

**Method 2: Automatic Discovery**
```bash
cd ~/projects/shared_data/stocks
python ticker_discovery.py
# Adds discovered tickers automatically
```

**Method 3: Scheduled Auto-Update**
```bash
./setup_ticker_automation.sh
# Choose option 1 for weekly discovery
```

### Adding New Crypto

Edit `~/projects/shared_data/crypto/crypto_config.py`:

```python
{
    'symbol': 'NEW',
    'name': 'New Coin',
    'query': 'newcoin OR new OR cryptocurrency',
    'category': 'Smart Contract',
    'market_cap_rank': 50,
    'high_volatility': True,
    'social_active': True
}
```

---

## 6. Running All Bots

### Stock Sentiment Collection (Hourly)

```bash
# One-time setup
cd ~/projects/shared_data/stocks
./setup_ticker_automation.sh
# Choose option 3 for hourly sentiment

# Or run manually
cd ~/projects/Morgans
python stock_sentiment.py --batch
```

### Crypto Sentiment Collection (Hourly)

```bash
cd ~/projects/Morgans
python automate.py
# Runs continuously, updates every hour
```

### Stock Price Prediction (On-Demand)

```bash
cd ~/projects/options
python stockPrediction_with_sentiment.py
```

### Financio Trading (Real-Time)

```bash
cd ~/projects/Financio-V2
# First sync tickers
python financio_ticker_integration.py

# Then start trading bot
python enhanced_live_trading.py
```

---

## 7. Monitoring & Logs

### Stock Sentiment Logs
```bash
tail -f ~/projects/Morgans/sentiment_auto.log
```

### Ticker Discovery Logs
```bash
tail -f ~/projects/shared_data/stocks/ticker_updates.log
```

### Check Latest Sentiment

**Stocks**:
```bash
cat ~/projects/shared_data/stocks/aapl_latest.json
```

**Crypto**:
```bash
cat ~/projects/shared_data/sentiment/crypto/btc_latest.json
```

---

## 8. Integration Benefits

### Before Integration
❌ Each bot managed its own ticker list
❌ Manual updates required for each bot
❌ Inconsistent queries across bots
❌ No automatic discovery
❌ Data scattered across projects

### After Integration
✅ Single source of truth for all tickers
✅ Automatic updates across all bots
✅ Consistent queries and parameters
✅ Automatic ticker discovery (Wikipedia + SEC)
✅ Centralized data storage
✅ Easy to add new bots

---

## 9. Performance Tracking

### Source Performance

Track which discovery sources find better opportunities:

```bash
cd ~/projects/shared_data/stocks
python source_performance_tracker.py
```

Shows:
- Average opportunity score by source (Wikipedia vs SEC vs hardcoded)
- Average prediction RMSE/MAPE by source
- Recommendations for which sources to use

### FinBERT vs VADER

Compare sentiment analyzers across stocks:

```bash
cd ~/projects/options
python finbert_multi_ticker.py
```

Results (from your testing):
- **TSLA, NKE, AAPL**: FinBERT wins (71-81% improvement)
- **PATH**: VADER wins (60% improvement)

### Stock Personality Auto-Select

Automatically choose best analyzer per stock:

```python
from stock_personality import auto_select_sentiment_analyzer

analyzer = auto_select_sentiment_analyzer('TSLA')
# Returns 'finbert' for complex stocks, 'vader' for straightforward
```

---

## 10. Future Enhancements

### Planned Integrations

1. **Real-time Twitter sentiment** (twitter_integration.py framework exists)
2. **Reddit WSB scraping** for meme stock detection
3. **Crypto price prediction** using crypto sentiment data
4. **Multi-asset portfolio optimizer** using stock + crypto sentiment
5. **Alert system** for sentiment shifts and opportunities

### Crypto Expansion

1. Auto-discovery from CoinGecko/CoinMarketCap
2. DeFi protocol sentiment tracking
3. NFT collection sentiment analysis
4. Crypto futures sentiment (perpetuals, options)

---

## 11. Troubleshooting

### Bot can't find shared config

**Issue**: `ModuleNotFoundError: No module named 'shared_data'`

**Fix**:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / 'projects'))
```

### Tickers not syncing

**Issue**: Bot still using old tickers

**Fix**:
1. Verify shared config updated: `cat ~/projects/shared_data/stocks/tickers_config.py`
2. Restart bot
3. For Financio: Re-run `python financio_ticker_integration.py`

### Sentiment data not found

**Issue**: `FileNotFoundError: sentiment CSV not found`

**Fix**:
1. Run sentiment bot first: `python stock_sentiment.py`
2. Wait for data collection (1+ hour for initial run)
3. Check data exists: `ls ~/projects/shared_data/stocks/*_sentiment.csv`

---

## 12. Quick Reference

### File Locations

**Stock Config**: `~/projects/shared_data/stocks/tickers_config.py`
**Crypto Config**: `~/projects/shared_data/crypto/crypto_config.py`
**Stock Sentiment Data**: `~/projects/shared_data/stocks/`
**Crypto Sentiment Data**: `~/projects/shared_data/sentiment/crypto/`

### Key Scripts

**Stock Discovery**: `ticker_discovery.py`
**Stock Sentiment**: `stock_sentiment.py`
**Crypto Sentiment**: `automate.py`
**Financio Integration**: `financio_ticker_integration.py`
**Setup Automation**: `setup_ticker_automation.sh`

### Update Workflow

1. **Discover new tickers**: `python ticker_discovery.py`
2. **Sync Financio**: `python financio_ticker_integration.py`
3. **Collect sentiment**: `python stock_sentiment.py --batch`
4. **Run predictions**: `python stockPrediction_with_sentiment.py`
5. **Start trading**: `python enhanced_live_trading.py`

---

## Summary

All three bots are now integrated with the shared configuration pipeline:

✅ **Morgans Stock Bot** - Collects sentiment for all shared tickers
✅ **Options Prediction Bot** - Uses sentiment data for LSTM predictions
✅ **Financio Trading Bot** - Trades using shared ticker list and sentiment
✅ **Morgans Crypto Bot** - Collects sentiment for all shared crypto

**Benefits**:
- Centralized management
- Automatic discovery
- Consistent data
- Easy scaling
- Better performance tracking

**Result: All bots stay in sync, opportunities never escape!** 🚀
