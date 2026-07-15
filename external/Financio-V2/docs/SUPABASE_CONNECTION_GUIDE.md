# Supabase PostgreSQL Connection Guide

This guide shows how to connect to your local Supabase PostgreSQL database from Python scripts.

## 🗂️ Files Created

### Connection Scripts

1. **`supabase_pg_connect.py`** - Simple connection script (based on your original)
2. **`supabase_db_manager.py`** - Advanced database manager with trading operations
3. **`connect_supabase_local.py`** - Comprehensive connection tester

### Configuration Files

1. **`.env.supabase.local`** - Environment variables for local Supabase connection
2. **`SUPABASE_CONNECTION_GUIDE.md`** - This guide

## 🔧 Local Supabase Connection Details

```
Host: 127.0.0.1
Port: 54322 (PostgreSQL port, not API port 54321)
Database: postgres
Username: postgres
Password: postgres
```

## 🚀 Quick Start

### 1. Basic Connection Test

```bash
python3 supabase_pg_connect.py
```

This will:
- Connect to local Supabase
- Show current time
- Display data counts for all Financio tables
- Show recent trades

### 2. Advanced Database Operations

```bash
python3 supabase_db_manager.py
```

This demonstrates:
- Bot instance management
- Trading statistics
- Portfolio analytics
- Recent trades analysis

### 3. Comprehensive Connection Test

```bash
python3 connect_supabase_local.py
```

This will:
- Test all connection parameters
- List all database tables
- Verify Financio schema
- Show row counts for each table

## 📋 Using in Your Trading Bot

### Simple Connection (your original approach)

```python
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('.env.supabase.local')

# Connection parameters
USER = os.getenv("SUPABASE_DB_USER", "postgres")
PASSWORD = os.getenv("SUPABASE_DB_PASSWORD", "postgres")
HOST = os.getenv("SUPABASE_DB_HOST", "127.0.0.1")
PORT = os.getenv("SUPABASE_DB_PORT", "54322")
DBNAME = os.getenv("SUPABASE_DB_NAME", "postgres")

# Connect
connection = psycopg2.connect(
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    dbname=DBNAME
)

cursor = connection.cursor()
cursor.execute("SELECT NOW();")
result = cursor.fetchone()
print("Current Time:", result)

cursor.close()
connection.close()
```

### Advanced Usage with Database Manager

```python
from supabase_db_manager import FinancioSupabaseDB

# Initialize database manager
db = FinancioSupabaseDB()
db.connect()

# Insert a trade
trade_id = db.insert_trade(
    user_id="your-user-id",
    ticker="AAPL",
    action="BUY",
    price=195.50,
    quantity=10,
    strategy="ML_HYBRID",
    reason="Strong momentum signal",
    confidence=0.85,
    bot_id="your-bot-id"
)

# Get recent trades
recent_trades = db.get_recent_trades(limit=10)

# Update bot status
db.update_bot_status("your-bot-id", "running", {"last_action": "trade_executed"})

# Get trading statistics
stats = db.get_trading_stats("your-user-id", days=30)

db.disconnect()
```

## 🏗️ Database Schema

Your local Supabase has these Financio tables:

- **`users`** - User accounts and preferences
- **`trades`** - All trading transactions
- **`bot_instances`** - Trading bot configurations and status
- **`portfolio_snapshots`** - Portfolio value over time
- **`notifications`** - System and trading notifications

## 🔧 Environment Variables

The `.env.supabase.local` file contains:

```env
# PostgreSQL Connection
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=postgres
SUPABASE_DB_HOST=127.0.0.1
SUPABASE_DB_PORT=54322
SUPABASE_DB_NAME=postgres

# Connection URL
SUPABASE_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres

# API Access (for reference)
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🚨 Important Notes

1. **Port Difference**:
   - API port: `54321` (for REST API, used by frontend)
   - PostgreSQL port: `54322` (for direct database connections)

2. **Local Development Only**: These credentials are for local Supabase only

3. **Production Setup**: For production, use your actual Supabase project credentials

## 🔍 Troubleshooting

### Connection Failed?

1. **Check Supabase is running**:
   ```bash
   cd supabase && supabase status
   ```

2. **Start Supabase if stopped**:
   ```bash
   cd supabase && supabase start
   ```

3. **Install required packages**:
   ```bash
   pip install psycopg2-binary python-dotenv
   ```

### No Data in Tables?

Run the sample data script:
```bash
python3 add_sample_data.py
```

## 🎯 Next Steps

1. **Integrate with your trading bot** using the database manager
2. **Add real-time data streaming** using Supabase real-time features
3. **Set up production Supabase** when ready for deployment
4. **Add logging and monitoring** for database operations

---

✅ **Your local Supabase PostgreSQL connection is ready!**