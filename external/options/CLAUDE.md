# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📚 Quick Start for New Claude Instances

**For comprehensive technical documentation** on the sentiment pipeline, see:
- `/Users/mosley/projects/Morgans/TECH_DOC_SENTIMENT_PIPELINE.md`

This document contains detailed architecture, file locations, troubleshooting, and next steps for the **3-way sentiment integration system** (NewsAPI + Reddit + SEC filings).

## Project Overview

This is a Python-based stock options and price prediction toolkit containing three main components:

1. **Options Analyzer** (`options_analyzer.py`) - Analyzes options chains, calculates breakeven points, and models investment scenarios
2. **Stock Price Predictor** (`stockPrediction.py`) - Uses LSTM neural networks to predict future stock prices based on historical data
3. **Sentiment-Enhanced Predictor** (`stockPrediction_with_sentiment.py`) - LSTM model that trains on both price data AND **3-way sentiment analysis** (NewsAPI + Reddit + SEC filings)

## Sentiment Integration (Updated 2025-10-18)

This project integrates with the **Morgans sentiment bot** (`~/projects/Morgans`) to enhance predictions with **multi-source sentiment analysis**.

**Architecture (3-Way Sentiment)**:
```
Morgans (Sentiment Collection)              Options (Prediction)
├── stock_sentiment.py (NewsAPI)       ←→   ├── sentiment_reader.py
├── reddit_sentiment_collector.py            ├── stockPrediction_with_sentiment.py
├── sec_sentiment_collector.py               └── Reads combined sentiment
└── combine_sentiment_history.py
         │
         ▼
~/projects/shared_data/stocks/
├── path_sentiment.csv              # NewsAPI raw
├── reddit/path_reddit_sentiment.csv # Reddit raw
├── sec/path_sec_sentiment.csv      # SEC raw
└── path_combined_sentiment.csv     # ★ 3-way combined (used by LSTM)
```

**Data Flow (3-Source Pipeline)**:
1. **NewsAPI Collection**: Fetches news articles, analyzes with VADER sentiment
   - Output: `path_sentiment.csv` (daily social media news sentiment)

2. **Reddit Collection**: Scrapes r/stocks, r/investing, analyzes posts with VADER
   - Output: `reddit/path_reddit_sentiment.csv` (community discussion sentiment)
   - Engagement-weighted: Higher score/comments = more weight

3. **SEC Collection** (NEW): Fetches 10-K, 10-Q, 8-K filings via SEC Edgar API
   - Output: `sec/path_sec_sentiment.csv` (fundamental business tone)
   - Keyword-based: Positive/negative word counting in filing text

4. **Sentiment Combination**: Merges all 3 sources with optimal weighting
   - PATH: 50% NewsAPI / 30% Reddit / 20% SEC
   - Output: `path_combined_sentiment.csv` (unified sentiment for LSTM)

5. **LSTM Prediction**: Trains on [Close price + Combined sentiment]
   - 60-day sliding windows, 2 features
   - 365-day future prediction

## Environment Setup

**Python Version**: 3.10.17

**Virtual Environment**: `.venv/` (located in project root)

Activate virtual environment:
```bash
source .venv/bin/activate
```

**Required Dependencies** (install manually if needed):
- `yfinance` - Yahoo Finance API for stock data
- `pandas` - Data manipulation
- `scikit-learn` - Data preprocessing (MinMaxScaler)
- `keras` / `tensorflow` - LSTM model building
- `matplotlib` - Visualization
- `numpy` - Numerical operations

## Running the Scripts

### Options Analyzer
Analyzes call options for a given ticker with optional target price:

```bash
python options_analyzer.py
```

Edit the `__main__` block to customize:
- `ticker` variable (default: "PATH")
- `target` variable for target price (default: 20)

The script will display:
- Current vs target price with % move
- Available expiration dates
- Call options chain with breakeven/ROI calculations
- Investment scenario for $300

### Stock Price Predictor (Basic)
Trains an LSTM model and predicts future stock prices:

```bash
python stockPrediction.py
```

Edit script parameters:
- `symbol` - Stock ticker (default: ['PATH'])
- `start_date` / `end_date` - Historical data range
- `future_days` - Days to predict (default: 365)

The script will:
- Download historical stock data from Yahoo Finance
- Train LSTM model on 80% of data
- Predict prices and display RMSE
- Generate matplotlib visualizations

### Stock Price Predictor with Sentiment
Enhanced version that integrates sentiment analysis:

```bash
# First, start the sentiment bot (in Morgans project)
cd ~/projects/Morgans
source .venv/bin/activate
python stock_sentiment.py  # Let it run for a few hours to collect data

# Then run the sentiment-enhanced predictor (in options project)
cd ~/projects/options
source .venv/bin/activate
python stockPrediction_with_sentiment.py
```

Edit script parameters:
- `symbol` - Stock ticker (must match sentiment bot config)
- `start_date` / `end_date` - Historical data range
- `future_days` - Days to predict (default: 365)

The script will:
- Attempt to load sentiment data from shared directory
- Merge sentiment scores with price data on matching dates
- Train LSTM with 2 features: [Close price, Sentiment score]
- Fall back to price-only if sentiment unavailable
- Generate comparison charts with/without sentiment

## Code Architecture

### options_analyzer.py
**Main Function**: `get_options_data(ticker, target_price=None)`

Key flow:
1. Fetches current stock price via `yfinance`
2. Retrieves options expiration dates and chains
3. Filters call options within 90-130% of current price
4. Calculates per-contract cost, breakeven, and ROI metrics
5. If target price provided: calculates profit/loss scenarios
6. Returns filtered DataFrame with analysis

**Key Calculations**:
- `breakeven = strike + lastPrice`
- `profit_at_target = (target_price - strike - lastPrice) * 100`
- `roi_pct = profit_at_target / cost_per_contract * 100`

### stockPrediction.py
**Architecture**: Sequential LSTM model with 4 layers

Data preprocessing:
- Extracts 'Close' prices from historical data
- Normalizes using MinMaxScaler (0-1 range)
- Creates 60-day sliding windows for training

Model structure:
- LSTM(50, return_sequences=True) - first layer
- LSTM(50, return_sequences=False) - second layer
- Dense(25) - hidden layer
- Dense(1) - output layer
- Optimizer: adam, Loss: mean_squared_error

Training: 80/20 train-test split, batch_size=1, epochs=10

Prediction: Iteratively predicts next day using last 60 days of data

### stockPrediction_with_sentiment.py
**Enhanced LSTM model with sentiment integration**

Data preprocessing:
- Downloads price data via yfinance
- Loads sentiment data via `SentimentReader`
- Merges on matching dates (forward-fills missing sentiment)
- Normalizes both features together using MinMaxScaler
- Creates 60-day sliding windows with shape: (samples, 60, 2) where 2 = [price, sentiment]

Model structure:
- LSTM(50, return_sequences=True, input_shape=(60, 2)) - adapts to 2 features
- Dropout(0.2) - prevents overfitting
- LSTM(50, return_sequences=False)
- Dropout(0.2)
- Dense(25)
- Dense(1) - predicts Close price only

Key differences from basic version:
- Accepts 2 input features instead of 1
- Uses dropout layers for regularization
- Gracefully falls back to price-only if sentiment unavailable
- Generates separate charts for sentiment vs non-sentiment models

### sentiment_reader.py
**Utility module for reading sentiment data**

Key classes:
- `SentimentReader(data_type='stocks')` - Main reader class

Key methods:
- `get_latest_sentiment(symbol)` - Returns latest sentiment summary as dict
- `get_sentiment_history(symbol, days_back)` - Returns historical sentiment DataFrame
- `get_sentiment_for_dates(symbol, start_date, end_date)` - Gets sentiment aligned with date range
- `merge_with_price_data(price_df, symbol)` - Merges sentiment into price DataFrame

Sentiment data format:
- `sentiment_score`: Float from -1.0 (bearish) to +1.0 (bullish)
- `sentiment_label`: 'Bullish', 'Bearish', or 'Neutral'
- Automatically handles missing data with forward-fill and 0.0 fallback

## Important Notes

- All scripts default to ticker "PATH" - update before running
- Stock prediction is for educational purposes only, not financial advice
- Options data requires active market hours for real-time accuracy
- LSTM model performance depends on historical data quality and quantity

### Sentiment Integration Notes (3-Way System)

**Data Sources**:
- **NewsAPI**: Requires API key (free tier: https://newsapi.org) - Social media news sentiment
- **Reddit**: Requires PRAW credentials (free) - Community discussion sentiment
- **SEC Filings**: Free SEC Edgar API (requires user-agent) - Fundamental business tone

**Setup Requirements**:
1. Sentiment data must be collected BEFORE running sentiment-enhanced predictor
2. Run all 3 collectors to populate data:
   ```bash
   cd ~/projects/Morgans
   python stock_sentiment.py              # NewsAPI
   python reddit_sentiment_collector.py    # Reddit
   python sec_sentiment_collector.py --days 365  # SEC (historical)
   python combine_sentiment_history.py     # Combine all 3 sources
   ```

**Key Points**:
- Shared data directory: `~/projects/shared_data/stocks/`
- Stock symbols must match between sentiment bot config and prediction scripts
- Sentiment collectors should run daily (NewsAPI, Reddit) or weekly (SEC)
- Combined sentiment CSV is regenerated daily with 3-way optimal weighting
- Model gracefully handles missing sentiment by falling back to price-only mode
- For best results, collect at least 7 days of sentiment data before training

**Recent Updates (2025-10-18)**:
- ✓ SEC filings integration complete (22 filings for PATH)
- ✓ 3-way sentiment combination with optimal weights per ticker
- ✓ PATH now has 45 days of sentiment coverage (was 23 days before SEC)
- ⏳ Backtest pending to measure MAPE improvement from SEC integration

**Performance (PATH - 2-way results)**:
- With NewsAPI + Reddit: MAPE 5.12%, RMSE $0.80
- Optimal weights: 67% NewsAPI / 33% Reddit (before SEC)
- New 3-way weights: 50% NewsAPI / 30% Reddit / 20% SEC
- Full 3-way backtest results pending
