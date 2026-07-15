# Options - Stock Price Prediction & Options Analysis

**LSTM-based stock price prediction with sentiment enhancement**

## Overview

This project contains tools for:
1. **Stock price prediction** using LSTM neural networks
2. **Sentiment-enhanced prediction** integrating news sentiment analysis
3. **Options chain analysis** for call/put options evaluation

## Components

### 1. LSTM Stock Price Predictor (Basic)

**File**: `stockPrediction.py`

**Purpose**: Predict future stock prices using historical price data only

**Model Architecture**:
- Sequential LSTM with 4 layers
- Input: 60-day price windows
- Output: Next day's closing price
- Optimizer: Adam
- Loss: Mean Squared Error

**Training**:
- 80/20 train-test split
- MinMaxScaler normalization (0-1 range)
- Batch size: 1
- Epochs: 10

**Usage**:
```bash
cd ~/projects/options
source .venv/bin/activate
python stockPrediction.py
```

**Edit parameters** in the script:
```python
symbol = ['PATH']           # Stock ticker
start_date = '2020-01-01'   # Historical data start
end_date = '2024-01-01'     # Historical data end
future_days = 365           # Days to predict
```

**Output**:
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)
- Prediction chart: `{ticker}_prediction.png`

---

### 2. LSTM Stock Price Predictor with Sentiment

**File**: `stockPrediction_with_sentiment.py`

**Purpose**: Predict stock prices using both historical prices AND news sentiment

**Enhanced Features**:
- ✅ Integrates sentiment data from `Morgans/stock_sentiment.py`
- ✅ 2-feature input: [Close price, Sentiment score]
- ✅ Dropout layers (0.2) to prevent overfitting
- ✅ Graceful fallback to price-only if sentiment unavailable
- ✅ Comparison charts with/without sentiment

**Model Architecture**:
```python
LSTM(50, return_sequences=True, input_shape=(60, 2))  # 2 features
Dropout(0.2)
LSTM(50, return_sequences=False)
Dropout(0.2)
Dense(25)
Dense(1)  # Predicts Close price
```

**Data Flow**:
```
Morgans Sentiment Bot
    ↓
~/projects/shared_data/stocks/{ticker}_sentiment.csv
    ↓
sentiment_reader.py (merge with price data)
    ↓
LSTM Model (60-day windows, 2 features)
    ↓
Price predictions + comparison charts
```

**Usage**:
```bash
# Step 1: Collect sentiment data (run for 1+ hour)
cd ~/projects/Morgans
source .venv/bin/activate
python stock_sentiment.py --batch

# Step 2: Run sentiment-enhanced prediction
cd ~/projects/options
source .venv/bin/activate
python stockPrediction_with_sentiment.py
```

**Output**:
- RMSE/MAPE metrics for both models
- `{ticker}_prediction_sentiment.png` - Sentiment-enhanced prediction
- `{ticker}_prediction.png` - Price-only prediction
- Comparison showing improvement from sentiment

**Performance Improvement**:
- **TSLA**: 71% better RMSE with FinBERT sentiment
- **NKE**: 81% better RMSE with FinBERT sentiment
- **AAPL**: 74% better RMSE with FinBERT sentiment
- **PATH**: VADER sentiment performs 60% better than FinBERT

---

### 3. Options Chain Analyzer

**File**: `options_analyzer.py`

**Purpose**: Analyze call/put options chains and calculate ROI scenarios

**Features**:
- Fetch live options data via yfinance
- Calculate breakeven prices
- Compute ROI for target prices
- Filter by strike price range (90-130% of current price)
- Investment scenario modeling ($300 default)

**Usage**:
```bash
cd ~/projects/options
source .venv/bin/activate
python options_analyzer.py
```

**Edit parameters**:
```python
ticker = "PATH"
target = 20  # Target price for ROI calculation
```

**Output**:
```
Current Price: $15.50
Target Price: $20.00 (↑29.03%)

Available Expirations:
1. 2025-10-17 (8 days)
2. 2025-11-21 (43 days)
...

Call Options Analysis:
Strike  Last    Breakeven  Cost/Contract  Profit@Target  ROI
$15.00  $2.50   $17.50     $250          $250           100%
$16.00  $1.80   $17.80     $180          $220           122%
...

Investment Scenario ($300):
Best ROI: $16.00 strike (122% return = $366 profit)
```

---

### 4. Sentiment Reader

**File**: `sentiment_reader.py`

**Purpose**: Read sentiment data from Morgans bot for use in predictions

**Classes**:
- `SentimentReader(data_type='stocks')` - Main reader

**Methods**:
```python
reader = SentimentReader(data_type='stocks')

# Get latest sentiment
latest = reader.get_latest_sentiment('AAPL')
# Returns: {'sentiment_score': 0.45, 'sentiment_label': 'Bullish', ...}

# Get historical sentiment
history = reader.get_sentiment_history('AAPL', days_back=30)
# Returns: DataFrame with timestamp, sentiment_score, label

# Merge with price data
price_df = yf.download('AAPL', start='2024-01-01', end='2024-12-31')
merged = reader.merge_with_price_data(price_df, 'AAPL')
# Returns: DataFrame with Close + sentiment_score columns
```

**Data Sources**:
- Stock sentiment: `~/projects/shared_data/stocks/`
- Crypto sentiment: `~/projects/shared_data/sentiment/crypto/`

**Sentiment Score Range**: -1.0 (bearish) to +1.0 (bullish)

**Handles missing data**:
- Forward-fill gaps (uses last known sentiment)
- Defaults to 0.0 if no data available
- Logs warnings for data quality issues

---

## Environment Setup

### Python Version
Python 3.10.17

### Virtual Environment
```bash
cd ~/projects/options
source .venv/bin/activate
```

### Dependencies
```bash
pip install yfinance pandas scikit-learn keras tensorflow matplotlib numpy
```

**Key packages**:
- `yfinance` - Yahoo Finance API for stock/options data
- `pandas` - Data manipulation
- `scikit-learn` - MinMaxScaler normalization
- `keras`/`tensorflow` - LSTM model building
- `matplotlib` - Visualization
- `numpy` - Numerical operations

---

## Configuration

### Stock Tickers

**Configured in**: `~/projects/shared_data/stocks/tickers_config.py`

**Current stocks**:
- PATH - UiPath (RPA software) - $300 investment
- TSLA - Tesla (EVs) - $500 investment
- NKE - Nike (Athletic) - $300 investment
- AAPL - Apple (Tech) - $300 investment

**To add stocks**:
```bash
# Method 1: Edit config manually
vim ~/projects/shared_data/stocks/tickers_config.py

# Method 2: Auto-discovery
cd ~/projects/shared_data/stocks
python ticker_discovery.py
```

### Prediction Parameters

**Edit in each script**:

```python
# stockPrediction.py
symbol = ['PATH']           # Which stock to predict
start_date = '2020-01-01'   # How much history to use
end_date = '2024-01-01'     # Training data cutoff
future_days = 365           # How far ahead to predict

# LSTM parameters
lookback = 60               # Days in sliding window
train_split = 0.8           # 80% train, 20% test
epochs = 10                 # Training iterations
batch_size = 1              # Batch size
```

---

## Workflow

### Complete Prediction Workflow

**Step 1**: Collect sentiment data
```bash
cd ~/projects/Morgans
source .venv/bin/activate
python stock_sentiment.py --batch
# Let run for 1+ hour to collect sufficient data
```

**Step 2**: Verify sentiment data exists
```bash
ls ~/projects/shared_data/stocks/*_sentiment.csv
cat ~/projects/shared_data/stocks/path_latest.json
```

**Step 3**: Run sentiment-enhanced prediction
```bash
cd ~/projects/options
source .venv/bin/activate
python stockPrediction_with_sentiment.py
```

**Step 4**: Analyze results
```bash
# View prediction charts
open path_prediction_sentiment.png

# Compare with price-only prediction
open path_prediction.png
```

**Step 5** (optional): Analyze options for entry
```bash
python options_analyzer.py
# Find optimal strike price and expiration
```

---

## Understanding the Output

### LSTM Prediction Metrics

**RMSE (Root Mean Squared Error)**:
- Lower is better
- Measures average prediction error in dollars
- Example: RMSE = 2.5 means avg error of $2.50

**MAPE (Mean Absolute Percentage Error)**:
- Lower is better
- Measures average % error
- Example: MAPE = 5% means predictions off by 5% on average

**Typical Results**:
```
Without Sentiment:
  RMSE: $3.20
  MAPE: 8.5%

With Sentiment:
  RMSE: $1.80  (44% improvement)
  MAPE: 4.2%   (51% improvement)
```

### Prediction Charts

**Components**:
- **Blue line**: Actual historical prices
- **Orange line**: Model predictions on test set
- **Green line**: Future price predictions
- **Shaded area**: Confidence interval (if enabled)

**Interpretation**:
- Tight fit on historical data = good model training
- Smooth future predictions = model has learned patterns
- Wild future predictions = model overfitting or uncertain

---

## Sentiment Analyzer Selection

### Auto-Select Best Analyzer per Stock

**File**: `stock_personality.py` (if exists)

**Logic**:
```python
from stock_personality import auto_select_sentiment_analyzer

analyzer = auto_select_sentiment_analyzer('TSLA')
# Returns: 'finbert' (complex, controversial stock)

analyzer = auto_select_sentiment_analyzer('PATH')
# Returns: 'vader' (straightforward, less news)
```

**Criteria**:
- **FinBERT**: Complex stocks, high news volume, controversial
- **VADER**: Straightforward stocks, lower news volume, crypto

### Manual Comparison

**File**: `finbert_multi_ticker.py`

**Usage**:
```bash
cd ~/projects/options
source .venv/bin/activate
python finbert_multi_ticker.py
```

**Output**:
```
FinBERT vs VADER Comparison:

TSLA:
  VADER RMSE: $8.50
  FinBERT RMSE: $2.45 (71% better)
  Winner: FinBERT ✓

PATH:
  VADER RMSE: $1.20
  FinBERT RMSE: $3.00 (60% worse)
  Winner: VADER ✓
```

---

## Integration with Other Bots

### Data from Morgans Sentiment Bot
```python
# sentiment_reader.py
reader = SentimentReader(data_type='stocks')
sentiment = reader.get_latest_sentiment('AAPL')

# Reads from:
# ~/projects/shared_data/stocks/aapl_latest.json
```

### Data to Financio Trading Bot
Prediction results can inform trading decisions in `Financio-V2/`.

---

## Troubleshooting

### "No sentiment data found"

**Issue**: Prediction script can't find sentiment files

**Fix**:
```bash
# Run sentiment collection first
cd ~/projects/Morgans
python stock_sentiment.py --batch

# Wait 1+ hour for data
ls ~/projects/shared_data/stocks/*_sentiment.csv

# If no files, check API keys
cat ~/projects/Morgans/.env
```

### "LSTM model not converging"

**Issue**: High RMSE, poor predictions

**Fixes**:
1. Increase training data (earlier start_date)
2. Increase epochs (10 → 25)
3. Adjust lookback window (60 → 90 days)
4. Add more features (volume, sentiment, RSI)

### "Stock data download failed"

**Issue**: yfinance can't fetch data

**Fix**:
```bash
# Check ticker symbol is valid
python -c "import yfinance as yf; print(yf.Ticker('PATH').info)"

# Try different date range
# Some tickers have limited history
```

### "Sentiment merge issues"

**Issue**: Price and sentiment dates don't align

**Handled automatically**:
- Forward-fill: Uses last known sentiment for missing dates
- Fallback: Uses 0.0 sentiment if no data
- Logs warnings for quality issues

---

## File Reference

### Main Scripts
- `stockPrediction.py` - LSTM price prediction (price only)
- `stockPrediction_with_sentiment.py` - LSTM with sentiment
- `sentiment_reader.py` - Read sentiment data
- `options_analyzer.py` - Options chain analysis
- `finbert_multi_ticker.py` - Compare VADER vs FinBERT

### Configuration (External)
- `~/projects/shared_data/stocks/tickers_config.py` - Stock config
- `~/projects/Morgans/.env` - API keys for sentiment

### Data Input
- `~/projects/shared_data/stocks/{ticker}_sentiment.csv` - Sentiment history
- `~/projects/shared_data/stocks/{ticker}_latest.json` - Latest sentiment

### Output
- `{ticker}_prediction.png` - Price-only prediction chart
- `{ticker}_prediction_sentiment.png` - Sentiment-enhanced chart
- Console: RMSE/MAPE metrics

---

## Documentation

- **Project overview**: `~/projects/README.md`
- **Integration guide**: `~/projects/shared_data/BOT_INTEGRATION_GUIDE.md`
- **Project instructions**: `CLAUDE.md`

---

**Predicting the future with LSTM and sentiment analysis!** 📈🤖
