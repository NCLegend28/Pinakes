# Local Database Setup Guide

This guide covers setting up and using local Supabase PostgreSQL for development and data collection.

## Prerequisites

- Docker Desktop installed and running
- Supabase CLI installed (`brew install supabase/tap/supabase`)
- PostgreSQL client tools (for testing)

## Quick Start

### 1. Start Local Supabase

```bash
# Using the management script (recommended)
./scripts/manage-supabase.sh start

# Or directly with Supabase CLI
supabase start
```

### 2. Check Status

```bash
./scripts/manage-supabase.sh status
```

This will show:
- All running services
- Database connection details
- Supabase Studio URL

### 3. Set Up Data Collection Tables

```bash
# Create tables for local data collection
./scripts/local_data_collector.py setup
```

## Database Connection Details

### Local Supabase PostgreSQL

```
Host:     127.0.0.1
Port:     54322
Database: postgres
User:     postgres
Password: postgres

Connection URL:
postgresql://postgres:postgres@127.0.0.1:54322/postgres
```

### Supabase Studio (Web UI)

Access the web interface at: http://127.0.0.1:54323

## MCP (Model Context Protocol) Connection

Claude Code can now access your local database via MCP. The configuration is in:
```
~/.config/claude-code/mcp_settings.json
```

Two MCP servers are configured:
1. **supabase**: Cloud Supabase instance (production)
2. **postgres**: Local Supabase instance (development/data collection)

You can query the local database using SQL through Claude Code.

## Management Scripts

### Supabase Manager (`./scripts/manage-supabase.sh`)

```bash
# Start Supabase
./scripts/manage-supabase.sh start

# Stop Supabase
./scripts/manage-supabase.sh stop

# Restart Supabase
./scripts/manage-supabase.sh restart

# Check status
./scripts/manage-supabase.sh status

# Reset database (WARNING: deletes all data)
./scripts/manage-supabase.sh reset

# Test connection
./scripts/manage-supabase.sh test

# Open Supabase Studio in browser
./scripts/manage-supabase.sh studio
```

### Data Collector (`./scripts/local_data_collector.py`)

```bash
# Set up tables
./scripts/local_data_collector.py setup

# Show database statistics
./scripts/local_data_collector.py stats

# Test data insertion
./scripts/local_data_collector.py test
```

## Data Collection Tables

The local database includes tables for:

### 1. `market_data`
Stores historical price and volume data:
- ticker, timestamp, OHLCV
- Source tracking
- Automatic deduplication

### 2. `sentiment_data`
Stores sentiment analysis results:
- Sentiment scores and labels
- Confidence levels
- Article counts
- Raw data in JSONB format

### 3. `model_predictions`
Stores ML model predictions:
- Model name and prediction
- Confidence scores
- Feature data

### 4. `backtest_results`
Stores backtesting results:
- Strategy performance metrics
- Sharpe ratio, drawdown, win rate
- Configuration snapshots

## Python Integration

### Using in Your Code

```python
from scripts.local_data_collector import LocalDataCollector

# Initialize collector
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
collector.insert_market_data('AAPL', market_data)

# Insert sentiment data
sentiment_data = {
    'timestamp': datetime.now(),
    'sentiment_score': 0.75,
    'sentiment_label': 'positive',
    'confidence': 0.85,
    'article_count': 10
}
collector.insert_sentiment_data('AAPL', sentiment_data, source='morgans')

# Get recent data
recent_prices = collector.get_recent_market_data('AAPL', hours=24)
recent_sentiment = collector.get_recent_sentiment('AAPL', hours=24)

# Get statistics
stats = collector.get_statistics()

# Clean up
collector.close()
```

### Using Direct SQL

```python
import psycopg2

conn = psycopg2.connect(
    host="127.0.0.1",
    port=54322,
    database="postgres",
    user="postgres",
    password="postgres"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM market_data WHERE ticker = 'AAPL' ORDER BY timestamp DESC LIMIT 10")
results = cursor.fetchall()

conn.close()
```

## Using with Existing Supabase Config

The `backend/supabase_config.py` file can be updated to use local database:

```python
# For local development, set environment variables:
export DB_HOST=127.0.0.1
export DB_PORT=54322
export DB_NAME=postgres
export DB_USER=postgres
export DB_PASSWORD=postgres
```

Or use the `.env.supabase.local` file:
```bash
source .env.supabase.local
```

## Common Tasks

### Querying with psql

```bash
# Connect to local database
PGPASSWORD=postgres psql -h 127.0.0.1 -p 54322 -U postgres -d postgres

# List tables
\dt

# Describe a table
\d market_data

# Query data
SELECT * FROM market_data ORDER BY timestamp DESC LIMIT 10;

# Exit
\q
```

### Backing Up Data

```bash
# Backup database
PGPASSWORD=postgres pg_dump -h 127.0.0.1 -p 54322 -U postgres -d postgres > backup.sql

# Restore database
PGPASSWORD=postgres psql -h 127.0.0.1 -p 54322 -U postgres -d postgres < backup.sql
```

### Migrations

Migrations are stored in `supabase/migrations/`:

```bash
# Create a new migration
supabase migration new your_migration_name

# Apply migrations
supabase db reset
```

## Troubleshooting

### Supabase Won't Start

1. Check if Docker is running:
   ```bash
   docker ps
   ```

2. Check for port conflicts:
   ```bash
   lsof -i :54321  # API
   lsof -i :54322  # PostgreSQL
   lsof -i :54323  # Studio
   ```

3. Check Supabase logs:
   ```bash
   supabase logs
   ```

### Connection Refused

If you get "connection refused" errors:

1. Verify Supabase is running:
   ```bash
   ./scripts/manage-supabase.sh status
   ```

2. Test the connection:
   ```bash
   ./scripts/manage-supabase.sh test
   ```

### MCP Not Working

If Claude Code can't access the database:

1. Verify MCP configuration:
   ```bash
   cat ~/.config/claude-code/mcp_settings.json
   ```

2. Restart Claude Code CLI

3. Test connection manually:
   ```bash
   PGPASSWORD=postgres psql -h 127.0.0.1 -p 54322 -U postgres -d postgres -c "SELECT 1"
   ```

## Production vs Development

### Development (Local Supabase)
- Port: 54322
- URL: postgresql://postgres:postgres@127.0.0.1:54322/postgres
- Use for: Development, testing, local data collection
- Data is ephemeral (can be reset anytime)

### Production (Cloud Supabase)
- Port: 5432 (via Supabase cloud URL)
- URL: From .env file (SUPABASE_URL)
- Use for: Live trading, production data
- Data is persistent and backed up

## Best Practices

1. **Always use local for development**: Never test on production database
2. **Reset database regularly**: Keep local db clean with `./scripts/manage-supabase.sh reset`
3. **Use migrations**: All schema changes should be in migration files
4. **Backup important data**: Before resetting, backup any data you need
5. **Monitor disk space**: Docker volumes can grow large over time

## Additional Resources

- [Supabase Local Development Docs](https://supabase.com/docs/guides/local-development)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MCP Protocol Docs](https://modelcontextprotocol.io)
