# Market Data Collection Guide

## Overview

Automated market data collection from Alpaca API for all rotation tickers, stored in local PostgreSQL database.

## Collected Data Summary

**Last Collection:** 2026-01-13

### Statistics
- **Total Tickers:** 18
- **Total Records:** 1,422
- **Data Period:** 7 days (2026-01-07 to 2026-01-14)
- **Timeframe:** Hourly (1H)
- **Records per Ticker:** ~80 (MDAI has 62)

### Rotation Tickers
AAPL, MSFT, GOOG, AMZN, TSLA, NVDA, META, NFLX, QUBT, RGTI, IONQ, QBTS, PLTR, AVGO, MDAI, ORCL, AMD, INTC

### Price Performance (7-day change)

**Top Gainers:**
1. INTC: +19.10% ($40.15 → $47.82)
2. GOOG: +7.37% ($313.82 → $336.96)
3. ORCL: +3.97% ($193.76 → $201.45)
4. AMD: +3.26% ($213.67 → $220.63)
5. TSLA: +3.22% ($431.02 → $444.90)

**Top Losers:**
1. QBTS: -6.74% ($30.88 → $28.80)
2. META: -4.96% ($660.57 → $627.79)
3. MSFT: -1.99% ($476.83 → $467.35)
4. MDAI: -1.86% ($1.61 → $1.58)
5. NVDA: -1.64% ($187.69 → $184.62)

### Average Closing Prices (7-day period)
| Ticker | Avg Close | Latest Close |
|--------|-----------|--------------|
| META   | $647.48   | $627.79     |
| MSFT   | $478.20   | $467.35     |
| TSLA   | $439.88   | $444.90     |
| AVGO   | $343.77   | $355.95     |
| GOOG   | $326.65   | $336.96     |
| AAPL   | $259.77   | $259.96     |
| AMZN   | $244.66   | $241.59     |
| AMD    | $208.69   | $220.63     |
| ORCL   | $195.83   | $201.45     |
| NVDA   | $186.31   | $184.62     |
| PLTR   | $179.37   | $177.05     |
| NFLX   | $90.08    | $89.61      |
| IONQ   | $50.19    | $49.04      |
| INTC   | $43.28    | $47.82      |
| QBTS   | $29.55    | $28.80      |
| RGTI   | $25.24    | $24.96      |
| QUBT   | $11.91    | $11.80      |
| MDAI   | $1.60     | $1.58       |

## Collection Scripts

### Main Collection Script
`scripts/collect_market_data.py`

Fetches real market data from Alpaca and stores in local database.

### Usage

```bash
# Activate virtual environment
source .venv/bin/activate

# Collect last 7 days (hourly data)
python scripts/collect_market_data.py --days 7 --timeframe 1Hour

# Collect last 24 hours
python scripts/collect_market_data.py --hours 24

# Collect specific tickers
python scripts/collect_market_data.py --tickers AAPL,MSFT,NVDA --days 30

# Different timeframes
python scripts/collect_market_data.py --days 1 --timeframe 15Min
python scripts/collect_market_data.py --days 30 --timeframe 1Day
```

### Available Options

- `--days N` - Number of days of historical data (default: 7)
- `--hours N` - Collect only last N hours (overrides --days)
- `--timeframe` - Data granularity:
  - `1Min` - 1-minute bars
  - `5Min` - 5-minute bars
  - `15Min` - 15-minute bars
  - `1Hour` - Hourly bars (default)
  - `1Day` - Daily bars
- `--tickers` - Comma-separated list (overrides current_tickers.txt)
- `--file` - File containing tickers (default: current_tickers.txt)

## Database Schema

### market_data Table

```sql
CREATE TABLE market_data (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    open DECIMAL(10, 2),
    high DECIMAL(10, 2),
    low DECIMAL(10, 2),
    close DECIMAL(10, 2),
    volume BIGINT,
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ticker, timestamp)
);

CREATE INDEX idx_market_data_ticker_timestamp
    ON market_data(ticker, timestamp DESC);
```

## Querying Collected Data

### Using MCP (Claude Code)

```sql
-- Latest prices for all tickers
SELECT ticker, timestamp, close, volume
FROM market_data
WHERE timestamp = (SELECT MAX(timestamp) FROM market_data)
ORDER BY ticker;

-- Price range for specific ticker
SELECT
    ticker,
    MIN(low) as week_low,
    MAX(high) as week_high,
    AVG(close) as avg_close
FROM market_data
WHERE ticker = 'AAPL'
GROUP BY ticker;

-- Hourly volatility
SELECT
    ticker,
    timestamp,
    ((high - low) / low * 100) as hour_volatility_pct
FROM market_data
ORDER BY hour_volatility_pct DESC
LIMIT 10;
```

### Using Python

```python
from scripts.local_data_collector import LocalDataCollector

collector = LocalDataCollector()

# Get recent data
recent_data = collector.get_recent_market_data('AAPL', hours=24)

# Custom SQL queries
query = """
    SELECT ticker, AVG(volume) as avg_volume
    FROM market_data
    WHERE timestamp > NOW() - INTERVAL '7 days'
    GROUP BY ticker
    ORDER BY avg_volume DESC
"""
results = collector.execute_query(query)

collector.close()
```

## Automation

### Scheduled Collection

Add to crontab for automatic daily collection:

```bash
# Collect market data daily at 4:30 PM EST (after market close)
30 16 * * 1-5 cd ~/projects/Financio-V2 && source .venv/bin/activate && python scripts/collect_market_data.py --hours 8 >> logs/market_data_collection.log 2>&1
```

### Integration with Trading Bots

```python
# In your trading bot
from scripts.local_data_collector import LocalDataCollector

collector = LocalDataCollector()

# Get latest prices
latest_prices = collector.execute_query("""
    SELECT DISTINCT ON (ticker)
        ticker, close, volume, timestamp
    FROM market_data
    ORDER BY ticker, timestamp DESC
""")

# Use for trading decisions
for price_data in latest_prices:
    ticker = price_data['ticker']
    current_price = price_data['close']
    # ... trading logic
```

## Data Quality

### Verification Queries

```sql
-- Check for gaps in data
SELECT ticker, COUNT(*) as record_count
FROM market_data
GROUP BY ticker
ORDER BY record_count;

-- Find missing hours
SELECT ticker, timestamp
FROM market_data
WHERE ticker = 'AAPL'
ORDER BY timestamp;

-- Check data freshness
SELECT
    ticker,
    MAX(timestamp) as latest_data,
    NOW() - MAX(timestamp) as data_age
FROM market_data
GROUP BY ticker;
```

## Troubleshooting

### No Data Received

**Problem:** All tickers return "No data"

**Solutions:**
1. Check Alpaca API credentials in `.env`
2. Verify date range (no future dates)
3. Check if market was open during requested period
4. Verify ticker symbols are valid

```bash
# Test Alpaca connection
python -c "
from alpaca.data.historical import StockHistoricalDataClient
import os
from dotenv import load_dotenv
load_dotenv()
client = StockHistoricalDataClient(
    os.getenv('PAPER_ALPACA_API_KEY'),
    os.getenv('PAPER_ALPACA_SECRET_KEY')
)
print('✓ Connected to Alpaca')
"
```

### Tables Don't Exist

**Problem:** `relation "market_data" does not exist`

**Solution:**
```bash
source .venv/bin/activate
python scripts/local_data_collector.py setup
```

### Duplicate Key Errors

**Problem:** Data insertion fails with unique constraint violation

**Solution:** The script uses `ON CONFLICT` to handle duplicates automatically. If you still see errors, the timestamp+ticker combination already exists (which is fine).

## Data Retention

### Cleanup Old Data

```sql
-- Keep only last 30 days
DELETE FROM market_data
WHERE timestamp < NOW() - INTERVAL '30 days';

-- Vacuum to reclaim space
VACUUM ANALYZE market_data;
```

### Backup Data

```bash
# Backup market data table
PGPASSWORD=postgres pg_dump \
    -h 127.0.0.1 -p 54322 -U postgres \
    -d postgres -t market_data \
    > market_data_backup_$(date +%Y%m%d).sql

# Restore from backup
PGPASSWORD=postgres psql \
    -h 127.0.0.1 -p 54322 -U postgres \
    -d postgres \
    < market_data_backup_20260113.sql
```

## Next Steps

1. **Add Sentiment Data Collection** - Integrate with Morgans bot
2. **Real-time Data Streaming** - Use Alpaca WebSocket for live updates
3. **Data Enrichment** - Add technical indicators to collected data
4. **Automated Retraining** - Trigger model retraining when new data arrives
5. **Data Visualization** - Create dashboards showing price movements

## Related Documentation

- `docs/LOCAL_DATABASE_SETUP.md` - Database setup guide
- `QUICK_START_LOCAL_DB.md` - Quick reference
- `scripts/local_data_collector.py` - Data collection utilities
- `scripts/collect_market_data.py` - Market data collector
