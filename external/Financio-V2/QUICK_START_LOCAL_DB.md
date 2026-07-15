# Quick Start: Local Database

## ✅ Setup Complete!

Your local Supabase PostgreSQL database is configured and working.

## Quick Commands

### Start/Stop Supabase
```bash
# Start
./scripts/manage-supabase.sh start

# Stop
./scripts/manage-supabase.sh stop

# Check status
./scripts/manage-supabase.sh status

# Open web UI
./scripts/manage-supabase.sh studio
```

### Data Collection
```bash
# Activate venv first
source .venv/bin/activate

# Show database statistics
python scripts/local_data_collector.py stats

# Test data insertion
python scripts/local_data_collector.py test

# Set up tables (if needed)
python scripts/local_data_collector.py setup
```

### Direct Database Access
```bash
# Using psql
PGPASSWORD=postgres psql -h 127.0.0.1 -p 54322 -U postgres -d postgres

# Using Python
python -c "from scripts.local_data_collector import LocalDataCollector; c = LocalDataCollector()"
```

## Connection Details

**PostgreSQL:**
- Host: `127.0.0.1`
- Port: `54322`
- Database: `postgres`
- User: `postgres`
- Password: `postgres`
- URL: `postgresql://postgres:postgres@127.0.0.1:54322/postgres`

**Supabase Studio (Web UI):**
- URL: `http://127.0.0.1:54323`

## MCP Access (Claude Code)

You can now query the local database directly through Claude Code using SQL:

```sql
-- Example queries
SELECT * FROM market_data ORDER BY timestamp DESC LIMIT 10;
SELECT * FROM sentiment_data WHERE ticker = 'AAPL';
SELECT COUNT(*) FROM trades;
```

## Available Tables

### Core Trading Tables (from Supabase migrations)
- `users` - User accounts
- `trades` - All trading activity
- `bot_instances` - Bot configuration
- `portfolio_snapshots` - Portfolio history
- `notifications` - User notifications
- `subscriptions` - User subscriptions

### Data Collection Tables
- `market_data` - Price/volume data (OHLCV)
- `sentiment_data` - Sentiment analysis results
- `model_predictions` - ML model predictions
- `backtest_results` - Backtesting results

## Using in Python Code

```python
from scripts.local_data_collector import LocalDataCollector
from datetime import datetime

# Initialize
collector = LocalDataCollector()

# Insert market data
market_data = {
    'timestamp': datetime.now(),
    'open': 150.00,
    'high': 152.00,
    'low': 149.00,
    'close': 151.50,
    'volume': 1000000
}
collector.insert_market_data('AAPL', market_data, source='alpaca')

# Insert sentiment
sentiment_data = {
    'timestamp': datetime.now(),
    'sentiment_score': 0.75,
    'sentiment_label': 'positive',
    'confidence': 0.85,
    'article_count': 15
}
collector.insert_sentiment_data('AAPL', sentiment_data, source='morgans')

# Query recent data
recent_prices = collector.get_recent_market_data('AAPL', hours=24)
recent_sentiment = collector.get_recent_sentiment('AAPL', hours=24)

# Get statistics
stats = collector.get_statistics()
print(stats)

# Clean up
collector.close()
```

## Integration with Existing Code

Update your environment variables to use local database:

```bash
# Use local Supabase
export DB_HOST=127.0.0.1
export DB_PORT=54322
export DB_NAME=postgres
export DB_USER=postgres
export DB_PASSWORD=postgres
```

Or use the existing `backend/supabase_config.py`:

```python
from backend.supabase_config import supabase_manager

# Direct SQL queries
conn = supabase_manager.get_direct_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM trades ORDER BY time DESC LIMIT 10")
results = cursor.fetchall()
conn.close()
```

## Troubleshooting

**Connection refused?**
```bash
# Check if Supabase is running
./scripts/manage-supabase.sh status

# Start if not running
./scripts/manage-supabase.sh start
```

**Module not found?**
```bash
# Make sure venv is activated
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

**Tables don't exist?**
```bash
# Reset database with migrations
./scripts/manage-supabase.sh reset

# Or create data collection tables
source .venv/bin/activate
python scripts/local_data_collector.py setup
```

## Full Documentation

See `docs/LOCAL_DATABASE_SETUP.md` for complete documentation.
