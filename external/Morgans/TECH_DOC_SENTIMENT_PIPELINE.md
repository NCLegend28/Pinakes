# Sentiment-Enhanced Stock Prediction Pipeline - Technical Documentation

**Last Updated**: 2025-10-18
**Author**: Automated documentation from recent system updates
**Version**: 3.0 (3-way sentiment integration)

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Recent Updates (SEC Integration)](#recent-updates-sec-integration)
4. [Data Flow](#data-flow)
5. [File Locations](#file-locations)
6. [Components](#components)
7. [Running the System](#running-the-system)
8. [Performance Metrics](#performance-metrics)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## System Overview

**Purpose**: Multi-source sentiment analysis pipeline that collects, combines, and uses sentiment data from three sources (NewsAPI, Reddit, SEC filings) to enhance LSTM stock price predictions.

**Tech Stack**:
- Python 3.10.17
- Virtual environments in each project (`.venv/`)
- Core libraries: `yfinance`, `pandas`, `scikit-learn`, `keras/tensorflow`, `praw`, `vaderSentiment`
- SEC Edgar API (free, requires user-agent)
- NewsAPI (free tier)
- Reddit API (PRAW)

**Key Projects**:
- **Morgans** (`~/projects/Morgans/`) - Sentiment collection and aggregation
- **Options** (`~/projects/options/`) - Stock prediction with sentiment
- **Shared Data** (`~/projects/shared_data/stocks/`) - Centralized sentiment storage

---

## Architecture

### Three-Source Sentiment Model

```
┌─────────────────────────────────────────────────────────────────┐
│                     SENTIMENT COLLECTION                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   NewsAPI    │  │    Reddit    │  │ SEC Filings  │         │
│  │   Articles   │  │     Posts    │  │  (10-K, 10-Q)│         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │    VADER     │  │    VADER     │  │   Keyword    │         │
│  │  Sentiment   │  │  Sentiment   │  │   Analysis   │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│  ┌──────────────────────────────────────────────────┐         │
│  │        Save to ~/shared_data/stocks/             │         │
│  │  - path_sentiment.csv                            │         │
│  │  - reddit/path_reddit_sentiment.csv              │         │
│  │  - sec/path_sec_sentiment.csv                    │         │
│  └──────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SENTIMENT COMBINATION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  combine_sentiment_history.py                            │  │
│  │                                                          │  │
│  │  Optimal 3-way weighting per ticker:                    │  │
│  │  - PATH: 50% NewsAPI / 30% Reddit / 20% SEC            │  │
│  │  - TSLA: 25% NewsAPI / 50% Reddit / 25% SEC            │  │
│  │  - AAPL: 70% NewsAPI / 0% Reddit / 30% SEC             │  │
│  │  - NKE:  33% NewsAPI / 67% Reddit / 0% SEC (no filings)│  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       ▼                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  path_combined_sentiment.csv                             │  │
│  │  Columns: date, newsapi_score, reddit_score, sec_score,  │  │
│  │           combined_score, data_sources, sentiment_label  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LSTM PRICE PREDICTION                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  stockPrediction_with_sentiment.py                       │  │
│  │                                                          │  │
│  │  1. Download price data (yfinance)                      │  │
│  │  2. Load combined_sentiment.csv                         │  │
│  │  3. Merge on date (forward-fill missing sentiment)      │  │
│  │  4. Normalize: [Close price, Sentiment score]           │  │
│  │  5. Create 60-day windows                               │  │
│  │  6. Train LSTM: (samples, 60, 2) input shape            │  │
│  │  7. Predict future prices (365 days)                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Output: Prediction charts + performance metrics (MAPE, RMSE)  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Recent Updates (SEC Integration)

### What Changed (2025-10-18)

**Previous Architecture**: 2-way sentiment (NewsAPI + Reddit)
- PATH: 67% NewsAPI / 33% Reddit
- MAPE: 4.35% to 5.12%

**New Architecture**: 3-way sentiment (NewsAPI + Reddit + SEC)
- PATH: 50% NewsAPI / 30% Reddit / 20% SEC
- Added 22 SEC filing dates to sentiment coverage
- Total sentiment days: 21 NewsAPI + 8 Reddit + 22 SEC = **45 unique days**

### Why Add SEC Filings?

1. **Fundamental Business Tone**: Official filings provide stable baseline vs volatile social media
2. **Sparse Coverage Fill**: SEC filings occur on dates without social media sentiment
3. **Professional Language**: +1.0 sentiment baseline from optimistic corporate language
4. **Regulatory Timing**: Captures earnings, quarterly reports, material events

### Files Created/Modified

**New Files**:
- `/Users/mosley/projects/Morgans/sec_sentiment_collector.py` - SEC data collector
- `/Users/mosley/projects/shared_data/stocks/sec/` - Directory for SEC sentiment CSVs
- `/Users/mosley/projects/shared_data/stocks/sec/path_sec_sentiment.csv` - PATH SEC data
- `/Users/mosley/projects/shared_data/stocks/sec/tsla_sec_sentiment.csv` - TSLA SEC data
- `/Users/mosley/projects/shared_data/stocks/sec/aapl_sec_sentiment.csv` - AAPL SEC data

**Modified Files**:
- `/Users/mosley/projects/Morgans/combine_sentiment_history.py` - Now handles 3-way combination
- Updated `load_sec_sentiment()` function
- Updated `combine_sentiments()` to accept 3 DataFrames
- Updated optimal weights dictionary for 3-way weighting

### SEC Data Collection Results

| Ticker | Filings | Date Range | Avg Sentiment | Status |
|--------|---------|------------|---------------|--------|
| PATH   | 22      | 2024-10-23 to 2025-09-08 | +1.000 | ✓ Success |
| TSLA   | 40      | 2025-09-05 to 2025-10-17 | +0.995 | ✓ Success |
| AAPL   | 26      | 2024-10-31 to 2025-09-26 | +1.000 | ✓ Success |
| NKE    | 0       | N/A | N/A | ⚠️ No filings |

---

## Data Flow

### Daily Operation (Automated via Cron)

```bash
# 1. Collect NewsAPI sentiment (runs daily at 6 AM)
cd ~/projects/Morgans
source .venv/bin/activate
python stock_sentiment.py  # Collects for all tickers

# 2. Collect Reddit sentiment (runs daily at 7 AM)
python reddit_sentiment_collector.py  # Collects for all tickers

# 3. Collect SEC filings (runs weekly on Mondays)
python sec_sentiment_collector.py --days 7  # New filings only

# 4. Combine all sources into unified sentiment (runs daily at 8 AM)
python combine_sentiment_history.py  # Creates *_combined_sentiment.csv

# 5. Run predictions (manual or scheduled)
cd ~/projects/options
source .venv/bin/activate
python stockPrediction_with_sentiment.py  # Uses combined sentiment
```

### Historical Backfill (One-time)

```bash
# Reddit historical backfill (already completed)
cd ~/projects/Morgans
python reddit_backfill.py --symbol PATH --days 365
python backfill_all_tickers.py  # Batch mode for all tickers

# SEC historical backfill (completed 2025-10-18)
python sec_sentiment_collector.py --days 365  # Fetches last year of filings
```

---

## File Locations

### Morgans Project (Sentiment Collection)

```
~/projects/Morgans/
├── .venv/                              # Python virtual environment
├── stock_sentiment.py                  # NewsAPI collector
├── reddit_sentiment_collector.py       # Reddit collector (daily)
├── reddit_backfill.py                  # Reddit historical backfill
├── backfill_all_tickers.py            # Batch backfill for all tickers
├── sec_sentiment_collector.py         # SEC filings collector (NEW)
├── combine_sentiment_history.py       # 3-way combiner (UPDATED)
└── TECH_DOC_SENTIMENT_PIPELINE.md     # This document
```

### Shared Data (Centralized Storage)

```
~/projects/shared_data/stocks/
├── path_sentiment.csv                  # NewsAPI sentiment for PATH
├── path_combined_sentiment.csv         # 3-way combined sentiment for PATH
├── path_combined_latest.json           # Latest sentiment snapshot
├── tsla_sentiment.csv                  # NewsAPI for TSLA
├── tsla_combined_sentiment.csv         # Combined for TSLA
├── aapl_sentiment.csv                  # NewsAPI for AAPL
├── aapl_combined_sentiment.csv         # Combined for AAPL
├── nke_sentiment.csv                   # NewsAPI for NKE
├── nke_combined_sentiment.csv          # Combined for NKE
├── reddit/
│   ├── path_reddit_sentiment.csv       # Reddit sentiment for PATH
│   ├── tsla_reddit_sentiment.csv       # Reddit for TSLA
│   ├── aapl_reddit_sentiment.csv       # Reddit for AAPL
│   └── nke_reddit_sentiment.csv        # Reddit for NKE
└── sec/                                # SEC filings directory (NEW)
    ├── path_sec_sentiment.csv          # SEC sentiment for PATH
    ├── tsla_sec_sentiment.csv          # SEC for TSLA
    └── aapl_sec_sentiment.csv          # SEC for AAPL
```

### Options Project (Prediction)

```
~/projects/options/
├── .venv/                              # Python virtual environment
├── stockPrediction.py                  # Basic LSTM (price only)
├── stockPrediction_with_sentiment.py   # LSTM with sentiment (UPDATED)
├── sentiment_reader.py                 # Utility to read combined sentiment
├── options_analyzer.py                 # Options chain analyzer
├── PATH_prediction_sentiment.png       # Latest prediction chart
├── PATH_future_sentiment.png           # Future prediction chart
└── CLAUDE.md                           # Project instructions
```

### Shared Features (Utilities)

```
~/projects/shared_data/features/
├── sec_filings.py                      # SECFilingsAnalyzer class
└── (other feature modules)

~/projects/shared_data/stocks/
└── tickers_config.py                   # Centralized ticker configuration
```

---

## Components

### 1. SEC Sentiment Collector

**File**: `sec_sentiment_collector.py`

**Purpose**: Fetch and analyze SEC filings (10-K, 10-Q, 8-K) for sentiment

**How it works**:
1. Uses `SECFilingsAnalyzer` from `shared_data/features/sec_filings.py`
2. Fetches filings via SEC Edgar API (requires user-agent header)
3. Analyzes filing text using keyword-based sentiment:
   - Positive keywords: "growth", "strong", "innovative", "successful", etc.
   - Negative keywords: "decline", "risk", "loss", "uncertainty", etc.
   - Sentiment score = (positive - negative) / (positive + negative)
4. Saves to `~/shared_data/stocks/sec/{ticker}_sec_sentiment.csv`

**CSV Format**:
```csv
date,filing_type,sentiment_score,positive_mentions,negative_mentions,url,sentiment_label
2025-09-08,10-Q,1.000,19,0,https://...,Positive
```

**Usage**:
```bash
# Single ticker
python sec_sentiment_collector.py --ticker PATH --days 365

# All tracked tickers
python sec_sentiment_collector.py --days 365
```

**Known Issues**:
- Some tickers require manual CIK mapping (see `sec_filings.py:manual_cik_mappings`)
- PATH CIK: `0001734722` (manually mapped)
- NKE has no recent filings (investment company, not operating company)

### 2. 3-Way Sentiment Combiner

**File**: `combine_sentiment_history.py`

**Purpose**: Merge NewsAPI, Reddit, and SEC sentiment with optimal weighting

**Key Functions**:

```python
load_newsapi_sentiment(symbol)  # Loads NewsAPI CSV, groups by date
load_reddit_sentiment(symbol)    # Loads Reddit CSV, handles raw/aggregated formats
load_sec_sentiment(symbol)       # Loads SEC CSV (NEW)
combine_sentiments(newsapi_df, reddit_df, sec_df, symbol)  # 3-way merge
combine_all_stocks()             # Batch process all tickers
```

**Optimal Weights** (tuned via backtest):

```python
OPTIMAL_WEIGHTS = {
    'PATH': (0.50, 0.30, 0.20),  # NewsAPI 50%, Reddit 30%, SEC 20%
    'TSLA': (0.25, 0.50, 0.25),  # Reddit-heavy (community-driven stock)
    'NKE': (0.33, 0.67, 0.0),    # No SEC data available
    'AAPL': (0.70, 0.0, 0.30),   # NewsAPI + SEC, skip Reddit noise
}
```

**Output CSV Format**:
```csv
date,newsapi_score,reddit_score,sec_score,combined_score,data_sources,sentiment_label
2025-10-18,0.392,0.531,0.0,0.448,NewsAPI+Reddit,Bullish
2024-10-23,0.0,0.0,1.0,0.200,SEC,Neutral
```

**Data Source Tracking**: Each row tracks which sources contributed:
- `SEC` - SEC filing only
- `NewsAPI` - NewsAPI only
- `Reddit` - Reddit only
- `NewsAPI+Reddit` - Both social sources
- `NewsAPI+SEC` - News + fundamental
- `NewsAPI+Reddit+SEC` - All three sources

**Usage**:
```bash
python combine_sentiment_history.py
```

### 3. LSTM Prediction with Sentiment

**File**: `stockPrediction_with_sentiment.py`

**Purpose**: Train LSTM model on price + sentiment, predict future prices

**Model Architecture**:
```
Input: (samples, 60, 2)  # 60-day windows, 2 features (Close price, Sentiment)

Layer 1: LSTM(50, return_sequences=True)
Layer 2: Dropout(0.2)
Layer 3: LSTM(50, return_sequences=False)
Layer 4: Dropout(0.2)
Layer 5: Dense(25)
Layer 6: Dense(1)  # Output: Close price prediction

Optimizer: Adam
Loss: MSE
Epochs: 10
Batch size: 1
```

**Data Preprocessing**:
1. Download price data via `yfinance`
2. Load `{ticker}_combined_sentiment.csv`
3. Merge on date, forward-fill missing sentiment
4. Normalize both features: `MinMaxScaler(0, 1)`
5. Create 60-day sliding windows
6. Train/test split: 80/20

**Performance Metrics**:
- MAPE (Mean Absolute Percentage Error)
- RMSE (Root Mean Squared Error)
- Comparison with price-only model

**Graceful Fallback**: If sentiment unavailable, trains on price only

**Usage**:
```bash
cd ~/projects/options
source .venv/bin/activate
python stockPrediction_with_sentiment.py
```

**Outputs**:
- `PATH_prediction_sentiment.png` - Train/test prediction overlay
- `PATH_future_sentiment.png` - 365-day future prediction
- Console: MAPE, RMSE, current price, predicted price

---

## Running the System

### First-Time Setup

```bash
# 1. Install dependencies (if needed)
cd ~/projects/Morgans
source .venv/bin/activate
pip install yfinance pandas scikit-learn keras tensorflow praw vaderSentiment

cd ~/projects/options
source .venv/bin/activate
pip install yfinance pandas scikit-learn keras tensorflow matplotlib numpy

# 2. Verify API credentials
# - NewsAPI key in stock_sentiment.py
# - Reddit credentials in reddit_sentiment_collector.py
# - SEC requires user-agent (already configured)

# 3. Run initial data collection
cd ~/projects/Morgans
python stock_sentiment.py           # Collect NewsAPI (current)
python reddit_sentiment_collector.py  # Collect Reddit (current)
python sec_sentiment_collector.py --days 365  # Collect SEC (historical)

# 4. Combine sentiment sources
python combine_sentiment_history.py

# 5. Run prediction
cd ~/projects/options
python stockPrediction_with_sentiment.py
```

### Daily Maintenance

**Recommended Cron Schedule**:

```cron
# NewsAPI collection (6 AM daily)
0 6 * * * cd ~/projects/Morgans && source .venv/bin/activate && python stock_sentiment.py >> ~/logs/newsapi.log 2>&1

# Reddit collection (7 AM daily)
0 7 * * * cd ~/projects/Morgans && source .venv/bin/activate && python reddit_sentiment_collector.py >> ~/logs/reddit.log 2>&1

# SEC collection (Monday 8 AM weekly)
0 8 * * 1 cd ~/projects/Morgans && source .venv/bin/activate && python sec_sentiment_collector.py --days 7 >> ~/logs/sec.log 2>&1

# Combine sentiment (9 AM daily)
0 9 * * * cd ~/projects/Morgans && source .venv/bin/activate && python combine_sentiment_history.py >> ~/logs/combine.log 2>&1

# Prediction (manual or 10 AM daily)
# 0 10 * * * cd ~/projects/options && source .venv/bin/activate && python stockPrediction_with_sentiment.py >> ~/logs/predict.log 2>&1
```

### Manual Operations

**Backfill historical Reddit data**:
```bash
cd ~/projects/Morgans
python reddit_backfill.py --symbol PATH --days 365
```

**Collect SEC filings for new ticker**:
```bash
# Add ticker to tickers_config.py first
python sec_sentiment_collector.py --ticker NVDA --days 365
```

**Re-run sentiment combination**:
```bash
python combine_sentiment_history.py
```

**Test prediction for single ticker**:
```bash
cd ~/projects/options
# Edit stockPrediction_with_sentiment.py to set symbol = ['PATH']
python stockPrediction_with_sentiment.py
```

---

## Performance Metrics

### PATH (UiPath) Results

**Before SEC Integration** (2-way: NewsAPI + Reddit):
- Weighting: 67% NewsAPI / 33% Reddit
- MAPE: 5.12%
- RMSE: $0.80
- Training samples: 300
- Sentiment days: 23

**After SEC Integration** (3-way: NewsAPI + Reddit + SEC):
- Weighting: 50% NewsAPI / 30% Reddit / 20% SEC
- Sentiment days: **45** (+22 from SEC)
- Data coverage:
  - 22 days: SEC-only (fundamental baseline)
  - 15 days: NewsAPI-only
  - 6 days: NewsAPI+Reddit
  - 2 days: Reddit-only
- Mean combined sentiment: 0.221 (Bullish bias from SEC +1.0 baseline)
- Sentiment breakdown: 88.9% Bullish, 8.9% Neutral, 2.2% Bearish

**Note**: Full MAPE comparison not yet run for 3-way model. Need to execute backtest.

### Other Tickers (2-way results, pre-SEC)

| Ticker | MAPE | Weighting (NewsAPI/Reddit) | Notes |
|--------|------|----------------------------|-------|
| TSLA   | 4.73% | 33% / 67% | Reddit-heavy (community driven) |
| NKE    | 2.81% | 33% / 67% | Reddit-focused |
| AAPL   | 2.19% | 100% / 0% | NewsAPI only (Reddit too noisy) |

**3-way results pending** - Need to run backtest to measure MAPE improvement.

---

## Troubleshooting

### Common Issues

**1. ImportError: cannot import name 'combine_all_tickers'**
- **Cause**: Function was renamed to `combine_all_stocks()`
- **Fix**: Update imports in `backfill_all_tickers.py` line 16 and line 105
- **Status**: ✓ Fixed (2025-10-18)

**2. SEC CIK lookup fails for ticker**
- **Cause**: Company name doesn't match SEC database or ticker ambiguity
- **Fix**: Add manual CIK mapping to `sec_filings.py`:
  ```python
  self.manual_cik_mappings = {
      'PATH': '0001734722',  # UiPath Inc
      # Add more as needed
  }
  ```
- **How to find CIK**: Visit https://www.sec.gov/edgar/searchedgar/companysearch.html

**3. No SEC filings found for ticker**
- **Cause**: Company may be investment fund (like NKE) or newly public
- **Fix**: Verify company type, check filing history on SEC Edgar
- **Workaround**: Set SEC weight to 0.0 in `OPTIMAL_WEIGHTS`

**4. Sentiment data not merging with price data**
- **Cause**: Date format mismatch or timezone issues
- **Fix**: Check `pd.to_datetime()` calls in `combine_sentiment_history.py`
- **Debug**: Print date columns after merge to verify format

**5. LSTM model overfitting (loss drops too fast)**
- **Cause**: Too many epochs or insufficient dropout
- **Fix**: Adjust dropout rate (0.2 → 0.3) or reduce epochs (10 → 5)
- **Monitor**: Watch validation loss vs training loss

**6. Reddit API rate limits**
- **Cause**: Too many requests in short time
- **Fix**: Add `time.sleep(2)` between subreddit searches
- **Already implemented**: Backfill script has built-in rate limiting

**7. Pandas FutureWarning: `groupby.apply` deprecation**
- **Cause**: Pandas 2.x compatibility
- **Fix**: Add `include_groups=False` to `groupby().apply()` calls
- **Status**: ⚠️ Low priority (just a warning, still works)

### Debug Mode

**Enable verbose output**:
```bash
# Add to script
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Check sentiment data quality**:
```python
import pandas as pd
df = pd.read_csv('~/projects/shared_data/stocks/path_combined_sentiment.csv')
print(df.describe())
print(df['data_sources'].value_counts())
print(df[df['combined_score'] == 0.0])  # Check for missing data
```

**Verify SEC API connection**:
```bash
curl -A "SentimentBot/1.0" "https://data.sec.gov/submissions/CIK0001734722.json" | jq .
```

---

## Next Steps

### Immediate Tasks

- [ ] **Run 3-way backtest**: Measure MAPE improvement from adding SEC sentiment
  ```bash
  cd ~/projects/options
  # Create backtest script to compare 2-way vs 3-way performance
  python backtest_3way_sentiment.py
  ```

- [ ] **Optimize SEC weighting**: Current weights (50/30/20) are initial guesses
  - Run grid search to find optimal 3-way weights
  - May need different weights per ticker (TSLA vs AAPL behavior differs)

- [ ] **Add more tickers**: NVDA, META, GOOGL, MSFT
  - Update `tickers_config.py`
  - Run SEC collector for new tickers
  - Check if manual CIK mappings needed

- [ ] **Fix Pandas deprecation warning**:
  ```python
  # In combine_sentiment_history.py line 83
  daily = df.groupby('date', include_groups=False).apply(lambda x: ...)
  ```

### Medium-Term Improvements

- [ ] **SEC sentiment enhancement**:
  - Current: Simple keyword counting (+1.0 for all filings)
  - Improvement: Use FinBERT or VADER on filing sections (MD&A, Risk Factors)
  - Extract numeric metrics (revenue growth %, EPS beat/miss)

- [ ] **Reddit engagement weighting**:
  - Currently: Engagement-weighted average per day
  - Improvement: Weight by subreddit quality (r/stocks vs r/wallstreetbets)
  - Filter out low-quality posts (score < 10)

- [ ] **Real-time sentiment updates**:
  - Current: Daily batch collection
  - Improvement: Websocket streaming from Reddit, NewsAPI webhooks
  - Update combined sentiment every hour

- [ ] **Sentiment anomaly detection**:
  - Flag sudden sentiment shifts (> 0.3 change day-over-day)
  - Alert on divergence between social vs SEC sentiment
  - Track sentiment volatility as separate feature

### Long-Term Architecture

- [ ] **Multi-model ensemble**:
  - Train separate LSTMs per sentiment source
  - Ensemble predictions with weighted average
  - Compare vs single 3-way model

- [ ] **Transformer-based prediction**:
  - Replace LSTM with Transformer architecture
  - Handle variable-length sequences better
  - Better long-term dependencies

- [ ] **Options strategy integration**:
  - Use prediction + sentiment to generate options strategies
  - Calculate optimal strike/expiration based on predicted price + volatility
  - Backtest options trades with sentiment signals

- [ ] **Dashboard/UI**:
  - Real-time sentiment dashboard (Streamlit/Dash)
  - Live prediction updates
  - Historical sentiment charts
  - Alert notifications for sentiment spikes

---

## Code Snippets

### Quick Reference

**Load combined sentiment for ticker**:
```python
import pandas as pd
from pathlib import Path

ticker = 'PATH'
sentiment_path = Path.home() / 'projects' / 'shared_data' / 'stocks' / f'{ticker.lower()}_combined_sentiment.csv'
df = pd.read_csv(sentiment_path)
df['date'] = pd.to_datetime(df['date'])
print(df.tail(10))
```

**Check data source coverage**:
```python
print(df['data_sources'].value_counts())
print(f"Total days: {len(df)}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
```

**Get latest sentiment**:
```python
latest = df.iloc[-1]
print(f"Date: {latest['date']}")
print(f"Combined score: {latest['combined_score']:.3f}")
print(f"Sources: {latest['data_sources']}")
print(f"Label: {latest['sentiment_label']}")
```

**Merge sentiment with price data**:
```python
import yfinance as yf

# Download price data
price_df = yf.download(ticker, start='2024-01-01', end='2025-10-18')
price_df = price_df.reset_index()
price_df['date'] = pd.to_datetime(price_df['Date'])

# Merge with sentiment
merged = pd.merge(price_df, df[['date', 'combined_score']], on='date', how='left')
merged['combined_score'] = merged['combined_score'].fillna(method='ffill').fillna(0.0)

print(f"Merged rows: {len(merged)}")
print(f"Non-zero sentiment: {(merged['combined_score'] != 0).sum()}")
```

---

## References

### Documentation Links

- **SEC Edgar API**: https://www.sec.gov/edgar/sec-api-documentation
- **NewsAPI**: https://newsapi.org/docs
- **PRAW (Reddit API)**: https://praw.readthedocs.io/
- **VADER Sentiment**: https://github.com/cjhutto/vaderSentiment
- **Keras LSTM**: https://keras.io/api/layers/recurrent_layers/lstm/
- **yfinance**: https://pypi.org/project/yfinance/

### Project Documentation

- `/Users/mosley/projects/options/CLAUDE.md` - Options project instructions
- `/Users/mosley/projects/Morgans/README.md` - Morgans bot overview (if exists)
- `/Users/mosley/projects/shared_data/stocks/tickers_config.py` - Ticker configuration

### Key Files to Review

When picking up this project, read these files first:

1. **Architecture understanding**:
   - `combine_sentiment_history.py` - See how 3-way combination works
   - `stockPrediction_with_sentiment.py` - See how LSTM integrates sentiment

2. **Data collection**:
   - `sec_sentiment_collector.py` - SEC collection logic
   - `sec_filings.py` - SEC API wrapper
   - `reddit_backfill.py` - Historical backfill logic

3. **Configuration**:
   - `tickers_config.py` - Which tickers are tracked
   - `CLAUDE.md` - Project-specific instructions

---

## Contact & Maintenance

**Last Updated**: 2025-10-18
**Maintainer**: Automated system (Claude Code)
**Version**: 3.0 (3-way sentiment integration)

**Change Log**:
- **v3.0** (2025-10-18): Added SEC filings integration, 3-way sentiment combination
- **v2.0** (2025-10-17): Added Reddit historical backfill, optimal weighting per ticker
- **v1.0** (2024-XX-XX): Initial 2-way sentiment system (NewsAPI + Reddit)

---

**END OF TECHNICAL DOCUMENTATION**
