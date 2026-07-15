# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python-based cryptocurrency analysis toolkit with three main components:
1. **Sentiment Analysis Bot** (`sentimentBot.py` / `main.py`) - Multi-method crypto news sentiment analyzer
2. **Staking Tracker** (`crypto_staking_tracker.py`) - ROI calculator for staking investments
3. **Test Script** (`test_script.py`) - Testing/debugging utilities

## Environment Setup

### Python Environment
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### API Keys
- Configured in `.env` file (never commit this file)
- NewsAPI key: For fetching crypto news articles
- CryptoPanic key: For crypto-specific news aggregation
- Keys are loaded using `python-dotenv`

## Running the Scripts

### Sentiment Analysis
```bash
# Run main sentiment analyzer
python main.py

# Run enhanced sentiment bot (updated version)
python sentimentBot.py
```

### Staking Tracker
```bash
python crypto_staking_tracker.py
```

## Architecture & Key Components

### Sentiment Analysis System
- **Multi-method analysis**: VADER, FinBERT (optional), and keyword-based
- **Ensemble scoring**: Weighted average of all methods (FinBERT: 0.5, VADER: 0.35, Keywords: 0.15)
- **Data flow**:
  1. Fetch news from NewsAPI/CryptoPanic
  2. Analyze each article using all available methods
  3. Compute ensemble scores
  4. Aggregate sentiment metrics (bullish/bearish/neutral counts)
  5. Save to CSV for historical tracking
- **Sentiment labels**:
  - Bullish (score > 0.15)
  - Bearish (score < -0.15)
  - Neutral (between -0.15 and 0.15)

### Key Classes

**CryptoSentimentAnalyzer** (`main.py` / `sentimentBot.py`)
- `analyze_text_sentiment()`: Core sentiment analysis method
- `fetch_newsapi_articles()`: NewsAPI integration
- `fetch_cryptopanic_news()`: CryptoPanic integration
- `analyze_news_batch()`: Batch processing with progress tracking
- `calculate_aggregate_sentiment()`: Time-windowed metrics
- `detect_sentiment_shift()`: Alert on significant sentiment changes

**CryptoStakingTracker** (`crypto_staking_tracker.py`)
- `calculate_returns()`: Simulate staking returns with price changes
- `calculate_current_position()`: Live position tracking via CoinGecko API
- `breakeven_price_change()`: Calculate breakeven thresholds
- `generate_scenarios()`: Multi-scenario analysis

### Data Storage
- Sentiment results saved to CSV files (e.g., `xlm_sentiment.csv`)
- Timestamp-based tracking for historical analysis
- Files stored in project root directory

### External APIs
- **NewsAPI** (`newsapi.org`): General news search with crypto queries
- **CryptoPanic** (`cryptopanic.com/api`): Crypto-specific news aggregator
- **CoinGecko** (`api.coingecko.com`): Price data (current & historical)

## Configuration

### FinBERT Model
- Optional AI model for enhanced sentiment accuracy
- Model: `yiyanghkust/finbert-tone` (no auth required)
- Enable by setting `use_finbert=True` in analyzer initialization
- Requires ~500MB download on first use
- Outputs: [negative, neutral, positive] probabilities

### Sentiment Thresholds
- VADER compound score: ±0.05 for bullish/bearish
- Ensemble score: ±0.15 for bullish/bearish
- Keyword score: ±0.3 for bullish/bearish
- Sentiment shift detection: ±0.3 change threshold

## Important Notes

- The project is NOT a git repository (no version control)
- Main difference between `main.py` and `sentimentBot.py`: Enhanced error handling and timezone fixes in `sentimentBot.py`
- Staking APY assumptions: Cosmos (ATOM) ~16%, Stellar (XLM) ~8%
- CoinGecko API has rate limits on free tier
- CSV files accumulate data over time for trend analysis
