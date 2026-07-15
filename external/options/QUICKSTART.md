# Sentiment-Enhanced Stock Prediction Quickstart

This guide will help you get started with the sentiment-enhanced stock prediction system.

## Overview

Your stock prediction model now integrates with the Morgans sentiment bot to combine:
- **Historical price data** (from Yahoo Finance)
- **News sentiment analysis** (from NewsAPI, analyzed with VADER + keywords)

## Step 1: Set Up Sentiment Bot

First, configure and start the sentiment bot to collect data:

```bash
# Navigate to Morgans project
cd ~/projects/Morgans
source .venv/bin/activate

# Make sure you have a NewsAPI key in .env file
# If not, get one free at https://newsapi.org
# Add to .env: NEWSAPI_KEY=your_key_here

# Edit stock_sentiment.py to add your tickers
# Look for STOCKS_TO_TRACK and add:
# {'query': 'PATH OR "UiPath" stock', 'symbol': 'PATH'}

# Start the sentiment bot
python stock_sentiment.py
```

Let it run for at least a few hours to collect sentiment data. The bot will:
- Fetch news articles every hour (configurable)
- Analyze sentiment using VADER + keyword matching
- Save results to `~/projects/shared_data/stocks/`

## Step 2: Run the Sentiment-Enhanced Predictor

Once you have sentiment data:

```bash
# Navigate to options project
cd ~/projects/options
source .venv/bin/activate

# Run the sentiment-enhanced predictor
python stockPrediction_with_sentiment.py
```

The script will:
1. Download historical price data for PATH (or your configured ticker)
2. Look for sentiment data in the shared directory
3. Merge sentiment scores with price data
4. Train an LSTM model with 2 features: [Close price, Sentiment score]
5. Generate predictions and visualizations
6. Save charts as PNG files

## Step 3: Compare Results

The script automatically compares models:

- **With sentiment**: Trains on price + sentiment
- **Without sentiment**: Falls back to price-only if sentiment unavailable

Charts are saved as:
- `PATH_prediction_sentiment.png` - Test set predictions
- `PATH_future_sentiment.png` - Future predictions (365 days)

## What to Expect

### Sentiment Data Format

The sentiment bot creates:
- `path_sentiment.csv` - Historical sentiment scores for each news article
- `path_latest.json` - Latest aggregate sentiment summary

Example sentiment score ranges:
- `-1.0 to -0.15`: Bearish
- `-0.15 to +0.15`: Neutral
- `+0.15 to +1.0`: Bullish

### Model Input

The LSTM model receives sequences like:
```
[
  [price_day1, sentiment_day1],
  [price_day2, sentiment_day2],
  ...
  [price_day60, sentiment_day60]
]
```

And predicts: `price_day61`

### Performance Metrics

The script reports:
- **RMSE** (Root Mean Square Error): Lower is better
- **MAPE** (Mean Absolute Percentage Error): Lower is better

Compare these metrics between sentiment-enhanced and price-only models.

## Configuration

### Customize Stocks to Track

Edit `~/projects/Morgans/stock_sentiment.py`:

```python
STOCKS_TO_TRACK = [
    {'query': 'PATH OR "UiPath" stock', 'symbol': 'PATH'},
    {'query': 'TSLA OR Tesla stock', 'symbol': 'TSLA'},
    # Add more...
]
```

### Customize Prediction Script

Edit `~/projects/options/stockPrediction_with_sentiment.py`:

```python
symbol = 'PATH'  # Change ticker
start_date = '2019-01-01'  # Change date range
end_date = '2025-05-04'
future_days = 365  # Change prediction horizon
```

## Troubleshooting

### "No sentiment data found for PATH"

**Solution**: Sentiment bot hasn't run yet or ticker mismatch
- Check: `ls ~/projects/shared_data/stocks/`
- Verify sentiment bot is running
- Ensure ticker symbols match exactly

### "Sentiment data is X hours old"

**Solution**: Sentiment bot stopped or needs restart
- Restart: `cd ~/projects/Morgans && python stock_sentiment.py`

### "No articles found for PATH"

**Solution**: NewsAPI may not have recent articles for this ticker
- Try a broader search query
- Check NewsAPI quota (free tier has limits)
- Verify API key is valid

### Model trains without sentiment

**Solution**: This is expected behavior
- Script falls back to price-only mode automatically
- Check console output for sentiment availability messages

## Advanced Usage

### Run Sentiment Bot in Background

```bash
cd ~/projects/Morgans
source .venv/bin/activate
nohup python stock_sentiment.py > sentiment.log 2>&1 &
```

Check logs: `tail -f ~/projects/Morgans/sentiment.log`

### View Current Sentiment

```bash
cat ~/projects/shared_data/stocks/path_latest.json
```

### Extract Sentiment History

```python
from sentiment_reader import SentimentReader

reader = SentimentReader(data_type='stocks')
df = reader.get_sentiment_history('PATH', days_back=30)
print(df[['timestamp', 'ensemble_score', 'ensemble_label']])
```

## Files Created

### In ~/projects/options:
- `sentiment_reader.py` - Reads sentiment data
- `stockPrediction_with_sentiment.py` - Enhanced predictor
- `PATH_prediction_sentiment.png` - Visualization
- `PATH_future_sentiment.png` - Future predictions

### In ~/projects/Morgans:
- `stock_sentiment.py` - Stock sentiment analyzer

### In ~/projects/shared_data/stocks/:
- `path_sentiment.csv` - Historical sentiment
- `path_latest.json` - Latest summary

## Next Steps

1. ✅ Start sentiment bot and let it collect data
2. ✅ Run sentiment-enhanced predictor
3. 📊 Compare RMSE/MAPE with and without sentiment
4. 🔄 Iterate: adjust model parameters, try different stocks
5. 📈 Use predictions with options_analyzer.py for trading strategies

## Resources

- NewsAPI: https://newsapi.org (free tier: 100 requests/day)
- VADER Sentiment: https://github.com/cjhutto/vaderSentiment
- Morgans project: `~/projects/Morgans/CLAUDE.md`
