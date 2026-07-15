# Ticker Management Guide

This guide explains how to manage stock tickers across the **Morgans sentiment bot** and **options prediction system** using the centralized ticker configuration.

## Overview

Both projects now use a **shared ticker configuration** located at:
```
~/projects/shared_data/stocks/tickers_config.py
```

This means you can:
- ✅ Add tickers in **one place** and use them everywhere
- ✅ Manage default settings (investment amount, prediction days) per ticker
- ✅ Easily run batch analysis across multiple tickers
- ✅ Keep sentiment bot and prediction system in sync

## Architecture

```
~/projects/
├── shared_data/stocks/
│   ├── tickers_config.py      ← Central ticker list (ADD TICKERS HERE)
│   ├── __init__.py
│   ├── path_sentiment.csv      ← Sentiment data
│   └── path_latest.json
│
├── Morgans/                    ← Sentiment bot (reads from shared config)
│   └── stock_sentiment.py
│
└── options/                    ← Prediction system (reads from shared config)
    ├── ticker_loader.py        ← Helper to load tickers
    ├── main.py                 ← Simple single-ticker analysis
    └── run_analysis_batch.py   ← Batch analysis for multiple tickers
```

## Adding New Tickers

### Method 1: Edit the Configuration File (Recommended)

1. Open `~/projects/shared_data/stocks/tickers_config.py`

2. Add your ticker to the `TICKERS` list:

```python
TICKERS = [
    {
        'symbol': 'PATH',
        'query': 'UiPath OR "PATH stock" OR "ticker PATH"',
        'investment': 300,
        'prediction_days': 30,
        'description': 'UiPath - RPA software company'
    },
    # Add new ticker here:
    {
        'symbol': 'AAPL',
        'query': 'Apple OR AAPL OR iPhone',
        'investment': 500,
        'prediction_days': 60,
        'description': 'Apple Inc - Technology company'
    },
]
```

3. Save the file. Both projects will now use the new ticker!

### Method 2: Add Programmatically

```python
from shared_data.stocks.tickers_config import add_ticker, save_tickers_to_file

# Add new ticker
add_ticker(
    symbol='AAPL',
    query='Apple OR AAPL OR iPhone',
    investment=500,
    prediction_days=60,
    description='Apple Inc - Technology company'
)

# Save to JSON file for persistence
save_tickers_to_file()
```

### Ticker Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `symbol` | Yes | Stock ticker (e.g., 'PATH', 'TSLA', 'AAPL') |
| `query` | Yes | NewsAPI search query for sentiment analysis |
| `investment` | No | Default investment amount (default: 300) |
| `prediction_days` | No | Prediction horizon in days (default: 30) |
| `description` | No | Human-readable description |

### Tips for Good Search Queries

The `query` field is used by the sentiment bot to find relevant news articles:

- ✅ **Good**: `'Apple OR AAPL OR iPhone OR "Tim Cook"'`
- ✅ **Good**: `'Tesla OR TSLA OR "Elon Musk Tesla" OR "Model 3"'`
- ❌ **Too broad**: `'technology'` (will get irrelevant news)
- ❌ **Too narrow**: `'AAPL'` (might miss articles that say "Apple" instead)

**Best practice**: Include company name, ticker, AND key products/people

## Using Tickers in Your Scripts

### Options Project

#### Option A: Simple Single-Ticker Analysis (main.py)

```python
from integratedSystem import run_full_analysis
from ticker_loader import get_ticker_config

# Just change the symbol here:
config = get_ticker_config('PATH')

run_full_analysis(
    ticker=config['symbol'],
    investment=config['investment'],
    prediction_days=config['prediction_days'],
    epochs=10,
    start_date='2025-08-01'
)
```

#### Option B: Batch Analysis (run_analysis_batch.py)

```bash
# Analyze specific tickers
python run_analysis_batch.py PATH TSLA NKE

# Or edit the script to analyze all tickers automatically
```

#### Option C: Custom Script

```python
from ticker_loader import get_all_tickers, get_ticker_config

# Get all tickers
all_tickers = get_all_tickers()
for ticker in all_tickers:
    print(f"Analyzing {ticker['symbol']}...")
    # Your analysis code here

# Get specific ticker
path_config = get_ticker_config('PATH')
print(path_config)
# {'symbol': 'PATH', 'investment': 300, 'prediction_days': 30, ...}
```

### Morgans Sentiment Bot

The sentiment bot automatically loads tickers from shared config:

```bash
cd ~/projects/Morgans
source .venv/bin/activate
python stock_sentiment.py
```

It will show:
```
✓ Loaded 3 tickers from shared config
Tracking: PATH, TSLA, NKE
```

## Viewing Available Tickers

### From Command Line

```bash
# Option 1: Via ticker_loader
cd ~/projects/options
python ticker_loader.py

# Option 2: Via shared config directly
cd ~/projects/shared_data
python -c "from stocks.tickers_config import display_tickers; display_tickers()"
```

### From Python Script

```python
from ticker_loader import list_available_tickers, show_tickers

# Get list of symbols
symbols = list_available_tickers()
print(symbols)  # ['PATH', 'TSLA', 'NKE']

# Show formatted display
show_tickers()
```

## Quick Start Workflows

### Workflow 1: Add Ticker and Start Sentiment Collection

```bash
# 1. Add ticker to config
nano ~/projects/shared_data/stocks/tickers_config.py
# (Add your ticker to TICKERS list)

# 2. Start sentiment bot (let it run for hours/days)
cd ~/projects/Morgans
source .venv/bin/activate
python stock_sentiment.py

# 3. Verify ticker is being tracked
# Look for: "Analyzing [YOUR_TICKER]" in output
```

### Workflow 2: Run Prediction for New Ticker

```bash
cd ~/projects/options
source .venv/bin/activate

# Option A: Update main.py
# Change TICKER_SYMBOL = "PATH" to your ticker
python main.py

# Option B: Use batch script
python run_analysis_batch.py YOUR_TICKER
```

### Workflow 3: Batch Analyze All Tickers

```bash
cd ~/projects/options
source .venv/bin/activate

# Edit run_analysis_batch.py and uncomment:
# run_batch_analysis(epochs=10)

python run_analysis_batch.py
```

## Examples

### Example 1: Add NVDA (NVIDIA)

1. Edit `~/projects/shared_data/stocks/tickers_config.py`:

```python
TICKERS = [
    # ... existing tickers ...
    {
        'symbol': 'NVDA',
        'query': 'NVIDIA OR NVDA OR "Jensen Huang" OR "AI chips"',
        'investment': 500,
        'prediction_days': 60,
        'description': 'NVIDIA - GPU and AI chip manufacturer'
    },
]
```

2. Restart sentiment bot (it will automatically pick up NVDA)
3. Run prediction: `python run_analysis_batch.py NVDA`

### Example 2: Track Multiple Tech Stocks

Add these to `tickers_config.py`:

```python
TICKERS = [
    {'symbol': 'AAPL', 'query': 'Apple OR AAPL OR iPhone', 'investment': 500, 'prediction_days': 30, 'description': 'Apple Inc'},
    {'symbol': 'MSFT', 'query': 'Microsoft OR MSFT OR Azure', 'investment': 500, 'prediction_days': 30, 'description': 'Microsoft'},
    {'symbol': 'GOOGL', 'query': 'Google OR Alphabet OR GOOGL', 'investment': 500, 'prediction_days': 30, 'description': 'Alphabet/Google'},
    {'symbol': 'AMZN', 'query': 'Amazon OR AMZN OR AWS', 'investment': 500, 'prediction_days': 30, 'description': 'Amazon'},
]
```

Then batch analyze: `python run_analysis_batch.py AAPL MSFT GOOGL AMZN`

## Troubleshooting

### "Could not load shared ticker config"

**Cause**: The shared_data directory is not in Python path

**Fix**: The scripts automatically add it to `sys.path`. If you see this error, check:
```bash
ls ~/projects/shared_data/stocks/tickers_config.py
```

If file doesn't exist, create it from the template in this guide.

### "No sentiment data available for [TICKER]"

**Cause**: Sentiment bot hasn't collected data yet

**Fix**:
1. Make sure ticker is in `tickers_config.py`
2. Run sentiment bot: `cd ~/projects/Morgans && python stock_sentiment.py`
3. Wait at least 1 hour for data collection
4. Re-run prediction script

### Sentiment bot not tracking new ticker

**Cause**: Bot needs to be restarted to pick up new config

**Fix**:
1. Stop sentiment bot (Ctrl+C)
2. Add ticker to `tickers_config.py`
3. Restart: `python stock_sentiment.py`
4. Verify: Look for "✓ Loaded X tickers from shared config"

## Best Practices

1. **Add tickers with good search queries**: Include company name, ticker symbol, and key products
2. **Start sentiment collection early**: Sentiment bot needs time to build historical data
3. **Use batch scripts for multiple tickers**: More efficient than running individually
4. **Keep shared config as single source of truth**: Don't hardcode tickers in other scripts
5. **Document tickers**: Use the `description` field to remember what each ticker is

## File Locations

| File | Purpose |
|------|---------|
| `~/projects/shared_data/stocks/tickers_config.py` | Central ticker configuration |
| `~/projects/shared_data/stocks/tickers_config.json` | Optional: JSON export of config |
| `~/projects/Morgans/stock_sentiment.py` | Sentiment bot (consumer) |
| `~/projects/options/ticker_loader.py` | Ticker loader utility (consumer) |
| `~/projects/options/main.py` | Single ticker analysis |
| `~/projects/options/run_analysis_batch.py` | Batch analysis |

## Summary

- **Add tickers**: Edit `~/projects/shared_data/stocks/tickers_config.py`
- **View tickers**: Run `python ticker_loader.py`
- **Start sentiment collection**: Run `~/projects/Morgans/stock_sentiment.py`
- **Run predictions**: Run `~/projects/options/main.py` or `run_analysis_batch.py`
- **Both projects auto-sync**: Changes in config instantly available everywhere
