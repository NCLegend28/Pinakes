# Automatic Ticker Discovery & Management System

**Widens coverage scope so opportunities don't escape** 🎯

## Overview

The ticker automation system automatically discovers, filters, scores, and tracks stocks with high sentiment-prediction potential. No manual ticker list maintenance required.

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    TICKER AUTOMATION                        │
└─────────────────────────────────────────────────────────────┘

1. Discovery (ticker_discovery.py)
   ├─ Scans most active stocks
   ├─ Finds trending movers
   └─ Identifies sector leaders

2. Filtering (ticker_filters.py)
   ├─ Quality filters (market cap, volume, price)
   ├─ Opportunity scoring (momentum, volatility, liquidity)
   └─ Risk filtering (penny stocks, low liquidity)

3. Auto-Update (ticker_auto_updater.py)
   ├─ Runs discovery + filtering
   ├─ Updates tickers_config.py
   └─ Logs changes

4. Scheduling (setup_ticker_automation.sh)
   ├─ Sets up cron jobs
   └─ Automates the pipeline

5. Sentiment Collection (stock_sentiment.py)
   ├─ Automatically tracks new tickers
   └─ Runs hourly/daily
```

## Quick Start

### 1. Run Manual Discovery (Test First)

```bash
cd ~/projects/shared_data/stocks
python ticker_discovery.py
```

This will:
- Discover ~50+ stocks from multiple sources
- Display by sector
- Ask if you want to update config

### 2. Test Filtering & Scoring

```bash
python ticker_filters.py
```

This will:
- Score ~35 sample stocks
- Rank by opportunity score
- Show breakdown of top 3

### 3. Set Up Automation

```bash
./setup_ticker_automation.sh
```

Choose option 4 for full pipeline:
- **Ticker discovery**: Every Sunday at 6 AM
- **Sentiment collection**: Every hour

### 4. Monitor Logs

```bash
# View discovery log
tail -f ticker_updates.log

# View sentiment collection log
tail -f ~/projects/Morgans/sentiment_auto.log
```

## Discovery Sources

### 1. Most Active Stocks
- High trading volume = liquidity
- Major indices: S&P 500, Dow, NASDAQ
- Limit: Top 50 by volume

### 2. Trending Stocks
- Recent gainers (>10% in 7 days)
- Momentum plays
- Growth opportunities

### 3. Sector Leaders
- Top 3 stocks per sector
- Technology, Healthcare, Financials, Consumer, Energy, Industrials
- Market cap weighted

## Filtering Criteria

### Quality Filters (Must Pass)

| Criterion | Threshold | Reason |
|-----------|-----------|--------|
| Market Cap | ≥ $1B | Avoid penny stocks |
| Price | $5 - $1000 | Practical trading range |
| Avg Volume | ≥ 500k/day | Ensure liquidity |
| Price History | ≥ 30 days | Need historical data |
| Volatility | ≤ 15% daily σ | Avoid extreme risk |

### Opportunity Scoring (0-100)

Scores based on weighted metrics:

| Metric | Weight | What It Measures |
|--------|--------|------------------|
| **Momentum** | 25% | Recent price movement (7d + 30d) |
| **Volatility** | 20% | Daily price swings (opportunity) |
| **Volume Spike** | 20% | Recent interest increase |
| **Liquidity** | 15% | Volume vs market cap |
| **Sentiment Potential** | 20% | News coverage likelihood |

**High scores = ideal for sentiment-enhanced prediction**

Example scores:
- TSLA: 85 (high momentum, volatility, sentiment)
- AAPL: 75 (strong liquidity, moderate momentum)
- PATH: 65 (good volatility, niche sentiment)

## Auto-Update Behavior

### When Does It Update?

```python
# In ticker_auto_updater.py
min_new_tickers = 5  # Threshold

# Updates config if:
new_tickers_found >= min_new_tickers
```

### What Gets Added?

Each new ticker gets:

```python
{
    'symbol': 'NVDA',
    'query': 'NVDA OR "NVIDIA" OR "NVDA stock"',
    'investment': 300,
    'prediction_days': 30,
    'description': 'NVIDIA Corporation - Technology',
    'auto_discovered': True,
    'discovered_at': '2025-10-10'
}
```

### Update Log

Logs stored in `ticker_updates.log` (JSON format):

```json
{
  "timestamp": "2025-10-10T06:00:00",
  "new_tickers_added": 7,
  "total_tickers": 52,
  "tickers": ["AAPL", "MSFT", ...],
  "metadata": {...}
}
```

## Cron Schedule Options

### Option 1: Weekly Discovery (Recommended)

```bash
# Every Sunday at 6 AM
0 6 * * 0 cd ~/projects/shared_data/stocks && python ticker_auto_updater.py
```

**Why weekly?**
- Markets change slowly
- Avoid API rate limits
- Balance freshness vs stability

### Option 2: Daily Discovery (Aggressive)

```bash
# Every day at 2 AM
0 2 * * * cd ~/projects/shared_data/stocks && python ticker_auto_updater.py
```

**Why daily?**
- Catch fast movers
- React to market shifts
- Higher API usage

### Option 3: Sentiment Collection (Hourly)

```bash
# Every hour
0 * * * * cd ~/projects/Morgans && source .venv/bin/activate && python stock_sentiment.py --batch
```

**Why hourly?**
- Catch breaking news
- Real-time sentiment
- 24 updates/day per ticker

## Integration with Sentiment Bot

The sentiment bot (`stock_sentiment.py`) automatically:

1. **Reads shared config** on each run
   ```python
   from shared_data.stocks.tickers_config import get_stocks_to_track
   STOCKS_TO_TRACK = get_stocks_to_track()
   ```

2. **Collects sentiment for ALL tickers** in config
   - No manual list maintenance
   - New tickers added automatically

3. **Saves to shared directory**
   ```
   ~/projects/shared_data/stocks/
   ├── aapl_sentiment.csv
   ├── msft_sentiment.csv
   ├── tsla_sentiment.csv
   └── ...
   ```

4. **Prediction bot reads shared data**
   ```python
   from sentiment_reader import SentimentReader
   reader = SentimentReader(data_type='stocks')
   sentiment = reader.get_latest_sentiment('AAPL')
   ```

## File Structure

```
~/projects/shared_data/stocks/
├── tickers_config.py          # Centralized ticker list (auto-updated)
├── ticker_discovery.py        # Discovery engine
├── ticker_filters.py          # Filtering & scoring
├── ticker_auto_updater.py     # Scheduled updater
├── setup_ticker_automation.sh # Setup script
├── ticker_updates.log         # Update history (JSON)
├── TICKER_AUTOMATION.md       # This file
└── [sentiment CSV files]      # Per-ticker sentiment data
```

## Usage Examples

### Example 1: Manual Discovery

```bash
cd ~/projects/shared_data/stocks
python ticker_discovery.py
```

Output:
```
================================================================================
AUTOMATIC TICKER DISCOVERY
================================================================================

🔍 Discovering most active stocks...
   ✓ Found 48 active stocks

🔍 Discovering trending stocks (>10% gain in 7d)...
   ✓ PLTR: +15.3% in 7d
   ✓ NVDA: +12.1% in 7d
   ✓ Found 8 trending stocks

🔍 Discovering sector leaders (top 3 per sector)...
   ✓ Technology: AAPL, MSFT, NVDA
   ✓ Healthcare: UNH, JNJ, LLY
   ...

✓ Total unique tickers discovered: 52

Add discovered tickers to config? (y/n): y
✓ Ticker discovery complete!
```

### Example 2: Test Filtering

```bash
python ticker_filters.py
```

Output:
```
================================================================================
TOP 20 OPPORTUNITY STOCKS
================================================================================

Rank   Symbol   Score    Price       MCap       Sector               7d%      30d%
-------------------------------------------------------------------------------------------------------
1      TSLA     87.3     $245.50     $780.2B    Consumer Cyclical    +8.5%    +18.3%
2      NVDA     82.1     $495.20     $1.2T      Technology           +12.1%   +25.7%
3      AMD      76.5     $118.30     $192.5B    Technology           +5.2%    +14.8%
...
```

### Example 3: Automated Setup

```bash
./setup_ticker_automation.sh
```

Choose option 4:
```
Setting up full pipeline...
✓ Full pipeline configured:
  - Ticker discovery: Sundays at 6 AM
  - Sentiment collection: Every hour
```

### Example 4: Check Status

```bash
# View current cron jobs
crontab -l | grep -E "ticker|sentiment"

# View recent discoveries
python ticker_auto_updater.py  # Will show history
```

## Customization

### Adjust Quality Filters

Edit `ticker_filters.py`:

```python
class TickerFilter:
    MIN_MARKET_CAP = 1_000_000_000  # $1B (increase for blue chips only)
    MIN_PRICE = 5.0                  # $5 (increase to avoid cheaper stocks)
    MIN_AVG_VOLUME = 500_000         # 500k (increase for more liquidity)
```

### Adjust Opportunity Weights

```python
WEIGHTS = {
    'momentum': 0.35,           # More weight on momentum
    'volatility': 0.15,         # Less weight on volatility
    'volume_spike': 0.20,
    'liquidity': 0.10,
    'sentiment_potential': 0.20
}
```

### Change Update Threshold

Edit `ticker_auto_updater.py`:

```python
# Update only if 10+ new tickers found
updater.run_discovery(min_new_tickers=10)
```

## Monitoring & Maintenance

### Check Discovery Log

```bash
tail -f ~/projects/shared_data/stocks/ticker_updates.log
```

### View Recent Updates

```bash
cd ~/projects/shared_data/stocks
python -c "
import json
with open('ticker_updates.log', 'r') as f:
    logs = json.load(f)
    for log in logs[-5:]:
        print(f\"{log['timestamp']}: Added {log['new_tickers_added']} tickers\")
"
```

### Manual Trigger

```bash
# Run discovery now
cd ~/projects/shared_data/stocks
python ticker_auto_updater.py

# Force update (bypass threshold)
python -c "
from ticker_auto_updater import AutoUpdater
updater = AutoUpdater()
updater.run_discovery(min_new_tickers=0)  # Accept any new tickers
"
```

## Troubleshooting

### Issue: No new tickers discovered

**Cause**: All high-quality stocks already tracked

**Solution**: Lower quality thresholds or expand discovery sources

### Issue: Too many low-quality tickers

**Cause**: Filters too permissive

**Solution**: Increase `MIN_MARKET_CAP`, `MIN_AVG_VOLUME` in `ticker_filters.py`

### Issue: Cron job not running

**Check cron log**:
```bash
# macOS
log show --predicate 'process == "cron"' --last 1h

# Linux
grep CRON /var/log/syslog | tail -20
```

**Verify cron entry**:
```bash
crontab -l | grep ticker
```

### Issue: API rate limits

**Cause**: Too many API calls (yfinance has limits)

**Solution**:
- Reduce discovery frequency (weekly instead of daily)
- Add delays in discovery loop
- Use caching

## Best Practices

### 1. Start Conservative

- Run discovery **manually** first
- Review discovered tickers
- Test with **weekly schedule**
- Scale up to daily if needed

### 2. Monitor API Usage

- yfinance has rate limits (~2000 requests/hour)
- Each ticker check = 2-3 requests
- 50 tickers = ~100-150 requests
- Safe to run hourly for sentiment, weekly for discovery

### 3. Review Periodically

- Check `ticker_updates.log` weekly
- Remove underperforming tickers manually
- Adjust scoring weights based on results

### 4. Balance Coverage vs Quality

- More tickers = wider coverage BUT more noise
- Fewer tickers = higher quality BUT missed opportunities
- Recommended: 30-60 high-quality tickers

## Integration with Stock Personality Detector

The ticker automation integrates seamlessly with `stock_personality.py`:

```python
from stock_personality import auto_select_sentiment_analyzer

# For each new ticker discovered
for symbol in new_tickers:
    # Auto-select VADER or FinBERT
    analyzer = auto_select_sentiment_analyzer(symbol)

    # Use selected analyzer
    if analyzer == 'finbert':
        # Run FinBERT sentiment collection
    else:
        # Run VADER sentiment collection
```

This ensures each stock uses the optimal sentiment analyzer based on its personality.

## Future Enhancements

Potential additions:

1. **Real-time trending** (Twitter API, Reddit WSB)
2. **News event triggers** (earnings, IPOs, M&A)
3. **Sector rotation detection** (automatically shift focus)
4. **Performance feedback loop** (remove low-performing tickers)
5. **Portfolio optimization** (diversify across sectors)
6. **Alert system** (notify on high-opportunity discoveries)

## Summary

The ticker automation system:

✅ **Discovers** stocks from multiple sources
✅ **Filters** by quality (market cap, volume, liquidity)
✅ **Scores** by opportunity (momentum, volatility, sentiment potential)
✅ **Auto-updates** shared config
✅ **Integrates** with sentiment bot
✅ **Scales** with your needs

**Result: Never miss an opportunity** 🚀
