# Shared Data Pipeline

**Central configuration and data storage for all trading bots**

## Overview

This directory serves as the **single source of truth** for:
- Stock ticker configuration
- Cryptocurrency configuration
- Sentiment analysis data
- Ticker discovery and validation

All bots (`Morgans`, `options`, `Financio-V2`) read from this shared pipeline.

## Directory Structure

```
shared_data/
├── README.md                          ← You are here
├── BOT_INTEGRATION_GUIDE.md          ← Complete integration documentation
├── stocks/
│   ├── tickers_config.py             ← Stock ticker configuration
│   ├── ticker_discovery.py           ← Auto-discovery engine
│   ├── ticker_filters.py             ← Quality filtering & scoring
│   ├── ticker_auto_updater.py        ← Scheduled auto-updates
│   ├── wikipedia_scraper.py          ← Wikipedia stock lists
│   ├── sec_edgar_scraper.py          ← SEC EDGAR database
│   ├── source_performance_tracker.py ← Track discovery sources
│   ├── setup_ticker_automation.sh    ← Cron job setup
│   ├── WIKIPEDIA_SEC_GUIDE.md        ← Discovery documentation
│   ├── *_sentiment.csv               ← Historical sentiment data
│   └── *_latest.json                 ← Latest sentiment summaries
└── crypto/
    ├── crypto_config.py              ← Cryptocurrency configuration
    └── sentiment/crypto/             ← Crypto sentiment data
        ├── *_sentiment.csv           ← Historical crypto sentiment
        └── *_latest.json             ← Latest crypto summaries
```

## Key Configuration Files

### 1. Stock Configuration
**File**: `stocks/tickers_config.py`

**Defines**:
- Ticker symbols (AAPL, TSLA, PATH, NKE)
- News search queries for each ticker
- Investment amounts ($300-$500)
- Prediction parameters (30 days)
- Stock descriptions

**Used by**:
- `Morgans/stock_sentiment.py` - Sentiment collection
- `options/stockPrediction_with_sentiment.py` - Price prediction
- `Financio-V2/financio_ticker_integration.py` - Trading

**Key functions**:
```python
from shared_data.stocks.tickers_config import (
    get_all_tickers,      # Get all ticker configs
    get_ticker,           # Get specific ticker
    get_stocks_to_track   # Get list for sentiment bot
)
```

### 2. Crypto Configuration
**File**: `crypto/crypto_config.py`

**Defines**:
- 14 cryptocurrencies (BTC, ETH, BNB, XRP, ADA, SOL, DOGE, DOT, MATIC, LTC, ATOM, XLM, AVAX, LINK)
- News search queries
- Categories (Major, Smart Contract, Payment, Meme, etc.)
- Market cap ranks
- Volatility flags

**Used by**:
- `Morgans/automate.py` - Crypto sentiment collection

**Key functions**:
```python
from shared_data.crypto.crypto_config import (
    get_all_crypto,           # Get all crypto configs
    get_crypto_symbols,       # Get symbol list
    get_crypto_by_category,   # Filter by category
    get_major_crypto          # Top 5 by market cap
)
```

## Ticker Discovery System

### Discovery Sources

1. **Hardcoded** (`stocks/tickers_config.py`)
   - Manually curated high-quality stocks
   - Currently: 4 stocks (PATH, TSLA, NKE, AAPL)

2. **Wikipedia** (`stocks/wikipedia_scraper.py`)
   - S&P 500 (500 stocks)
   - DJIA (30 stocks)
   - NASDAQ-100 (100 stocks)
   - Big Tech companies
   - **Total**: ~600 stocks

3. **SEC EDGAR** (`stocks/sec_edgar_scraper.py`)
   - Official SEC company database
   - All publicly traded companies
   - Filterable by SIC codes (industry)
   - **Total**: ~13,000 companies

4. **Trending** (`stocks/ticker_discovery.py`)
   - Stocks with >10% gain in last 7 days
   - Momentum-based opportunities

5. **Sector Leaders** (`stocks/ticker_discovery.py`)
   - Top 3 stocks per sector by volume

### Quality Filters

**Applied by**: `stocks/ticker_filters.py`

- ✅ Market cap ≥ $1B (avoid penny stocks)
- ✅ Price $5-$1000 (practical trading range)
- ✅ Volume ≥ 500k/day (ensure liquidity)
- ✅ Volatility ≤ 15% daily σ (manage risk)

### Opportunity Scoring

**Weighted metrics** (0-100 scale):
- Momentum: 25% - Recent price movement
- Volatility: 20% - Price variance (optimal range)
- Volume spike: 20% - Trading activity increase
- Liquidity: 15% - Bid-ask spread
- Sentiment potential: 20% - News activity

### Running Discovery

```bash
cd ~/projects/shared_data/stocks

# Discover from all sources
python ticker_discovery.py

# Setup automatic weekly discovery
./setup_ticker_automation.sh
# Choose option 1 for weekly discovery
```

## Data Files

### Stock Sentiment Data
**Location**: `stocks/`

**Format**:
- `{ticker}_sentiment.csv` - Historical sentiment scores
- `{ticker}_latest.json` - Latest sentiment summary

**Example**: `aapl_sentiment.csv`
```csv
timestamp,sentiment_score,sentiment_label,article_count
2025-10-09 14:30:00,0.75,Bullish,15
```

**Example**: `aapl_latest.json`
```json
{
  "symbol": "AAPL",
  "timestamp": "2025-10-09T14:30:00",
  "overall_sentiment": "Bullish",
  "average_score": 0.75,
  "total_articles": 15
}
```

### Crypto Sentiment Data
**Location**: `sentiment/crypto/`

**Same format as stocks**, e.g.:
- `btc_sentiment.csv`
- `btc_latest.json`

## Integration with Bots

### Morgans Stock Sentiment Bot
```python
# Morgans/stock_sentiment.py
from shared_data.stocks.tickers_config import get_stocks_to_track

STOCKS_TO_TRACK = get_stocks_to_track()
# Returns: [{'symbol': 'AAPL', 'query': '...'}, ...]
```

### Options Prediction Bot
```python
# options/sentiment_reader.py
reader = SentimentReader(data_type='stocks')
sentiment = reader.get_latest_sentiment('AAPL')
# Reads from: shared_data/stocks/aapl_latest.json
```

### Financio Trading Bot
```python
# Financio-V2/financio_ticker_integration.py
manager = FinancioTickerManager()
tickers = manager.get_trading_tickers()
config = manager.get_sentiment_config_for_tickers(tickers)
```

### Morgans Crypto Bot
```python
# Morgans/automate.py
from shared_data.crypto.crypto_config import get_all_crypto

COINS_TO_TRACK = [
    {'query': crypto['query'], 'symbol': crypto['symbol']}
    for crypto in get_all_crypto()
]
```

## Adding New Assets

### Add Stock Ticker

**Method 1**: Manual edit
```python
# Edit stocks/tickers_config.py
TICKERS = [
    # ... existing tickers ...
    {
        'symbol': 'NVDA',
        'query': 'NVDA OR "NVIDIA" OR "NVDA stock"',
        'investment': 300,
        'prediction_days': 30,
        'description': 'NVIDIA Corporation - Technology'
    }
]
```

**Method 2**: Auto-discovery
```bash
cd stocks/
python ticker_discovery.py
# Automatically discovers, validates, and scores new tickers
```

**Method 3**: Scheduled updates
```bash
cd stocks/
./setup_ticker_automation.sh
# Choose option 1 for weekly auto-discovery
```

### Add Cryptocurrency

```python
# Edit crypto/crypto_config.py
CRYPTO_TO_TRACK = [
    # ... existing cryptos ...
    {
        'symbol': 'MATIC',
        'name': 'Polygon',
        'query': 'polygon OR matic OR cryptocurrency',
        'category': 'Layer 2',
        'market_cap_rank': 15,
        'high_volatility': True,
        'social_active': True
    }
]
```

## Monitoring

### Check Data Files
```bash
# List all stock sentiment files
ls stocks/*_sentiment.csv

# List all crypto sentiment files
ls sentiment/crypto/*_sentiment.csv

# View latest sentiment
cat stocks/aapl_latest.json
cat sentiment/crypto/btc_latest.json
```

### View Discovery Logs
```bash
tail -f stocks/ticker_updates.log
```

### Performance Tracking
```bash
cd stocks/
python source_performance_tracker.py
# Shows which discovery sources find better opportunities
```

## Automation

### Setup Cron Jobs
```bash
cd stocks/
./setup_ticker_automation.sh
```

**Options**:
1. Weekly ticker discovery (Wikipedia + SEC)
2. Daily trending discovery
3. Hourly stock sentiment collection
4. Hourly crypto sentiment collection

## Documentation

- **Complete Integration Guide**: `BOT_INTEGRATION_GUIDE.md`
- **Discovery System Guide**: `stocks/WIKIPEDIA_SEC_GUIDE.md`
- **Project Overview**: `../README.md`

## Quick Reference

### Import Paths
```python
# Stock config
from shared_data.stocks.tickers_config import get_all_tickers

# Crypto config
from shared_data.crypto.crypto_config import get_all_crypto

# Discovery
from shared_data.stocks.ticker_discovery import TickerDiscovery

# Filters
from shared_data.stocks.ticker_filters import TickerFilter
```

### Data Paths
- Stock sentiment: `~/projects/shared_data/stocks/{ticker}_sentiment.csv`
- Crypto sentiment: `~/projects/shared_data/sentiment/crypto/{coin}_sentiment.csv`
- Latest stock: `~/projects/shared_data/stocks/{ticker}_latest.json`
- Latest crypto: `~/projects/shared_data/sentiment/crypto/{coin}_latest.json`

---

**See parent directory README**: `~/projects/README.md`

**All bots stay in sync through this shared pipeline!** 🚀
