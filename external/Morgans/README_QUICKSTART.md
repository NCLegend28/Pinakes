# Morgans Sentiment Bot - Quick Start Guide

**Last Updated**: 2025-10-18
**Version**: 3.0 (3-way sentiment integration)

---

## 🚀 For New Claude Instances

**Read this first**: `/Users/mosley/projects/Morgans/TECH_DOC_SENTIMENT_PIPELINE.md`

This comprehensive technical documentation contains:
- Complete architecture overview
- File locations and data flow
- Detailed component descriptions
- Troubleshooting guide
- Performance metrics
- Next steps and TODOs

---

## 📋 Quick Reference

### What This Project Does

Collects and combines sentiment data from **3 sources** to enhance stock price predictions:

1. **NewsAPI** - Social media news articles (VADER sentiment)
2. **Reddit** - Community discussions (VADER sentiment, engagement-weighted)
3. **SEC Filings** - Official company filings (keyword-based sentiment)

### Key Files

| File | Purpose |
|------|---------|
| `stock_sentiment.py` | NewsAPI collector (daily) |
| `reddit_sentiment_collector.py` | Reddit collector (daily) |
| `sec_sentiment_collector.py` | SEC filings collector (weekly) |
| `combine_sentiment_history.py` | 3-way combiner with optimal weights |
| `reddit_backfill.py` | Historical Reddit backfill |
| `backfill_all_tickers.py` | Batch backfill for all tickers |

### Output Files (in `~/projects/shared_data/stocks/`)

```
stocks/
├── path_sentiment.csv                # NewsAPI raw
├── path_combined_sentiment.csv       # ★ 3-way combined (LSTM input)
├── reddit/path_reddit_sentiment.csv  # Reddit raw
└── sec/path_sec_sentiment.csv        # SEC raw
```

---

## 🏃 Running the System

### Daily Collection (Recommended Cron Jobs)

```bash
# 6 AM - NewsAPI
0 6 * * * cd ~/projects/Morgans && source .venv/bin/activate && python stock_sentiment.py

# 7 AM - Reddit
0 7 * * * cd ~/projects/Morgans && source .venv/bin/activate && python reddit_sentiment_collector.py

# 8 AM Monday - SEC (weekly)
0 8 * * 1 cd ~/projects/Morgans && source .venv/bin/activate && python sec_sentiment_collector.py --days 7

# 9 AM - Combine all sources
0 9 * * * cd ~/projects/Morgans && source .venv/bin/activate && python combine_sentiment_history.py
```

### Manual Operation

```bash
# Activate virtual environment
cd ~/projects/Morgans
source .venv/bin/activate

# Collect current sentiment from all sources
python stock_sentiment.py              # NewsAPI (takes ~1 min)
python reddit_sentiment_collector.py    # Reddit (takes ~2 min)
python sec_sentiment_collector.py --days 7  # SEC new filings only

# Combine all sources (3-way weighted combination)
python combine_sentiment_history.py     # Outputs: *_combined_sentiment.csv

# Now run predictions in options project
cd ~/projects/options
source .venv/bin/activate
python stockPrediction_with_sentiment.py
```

### Historical Backfill (One-Time)

```bash
# Reddit historical backfill (goes back 365 days via Pushshift)
python reddit_backfill.py --symbol PATH --days 365

# Batch backfill all tickers
python backfill_all_tickers.py

# SEC historical backfill (fetches last year of filings)
python sec_sentiment_collector.py --days 365

# Re-combine after backfill
python combine_sentiment_history.py
```

---

## 📊 Current Status

### Tracked Tickers

| Ticker | NewsAPI | Reddit | SEC | Combined |
|--------|---------|--------|-----|----------|
| PATH   | ✓ 21 days | ✓ 8 days | ✓ 22 filings | ✓ 45 days |
| TSLA   | ✓ 11 days | ✓ 6 days | ✓ 40 filings | ✓ 44 days |
| AAPL   | ✓ 11 days | ✓ 6 days | ✓ 26 filings | ✓ 38 days |
| NKE    | ✓ 11 days | ✓ 4 days | ✗ No filings | ✓ 12 days |

### Optimal Weights (NewsAPI / Reddit / SEC)

| Ticker | Weights | Notes |
|--------|---------|-------|
| PATH   | 50% / 30% / 20% | Balanced with SEC baseline |
| TSLA   | 25% / 50% / 25% | Reddit-heavy (community stock) |
| AAPL   | 70% / 0% / 30% | NewsAPI + SEC, skip Reddit |
| NKE    | 33% / 67% / 0% | No SEC filings available |

### Recent Changes (2025-10-18)

- ✅ SEC filings integration complete
- ✅ 3-way sentiment combination implemented
- ✅ PATH coverage improved: 23 days → 45 days (+96%)
- ✅ Combined sentiment CSVs regenerated with SEC data
- ⏳ MAPE backtest pending (measure 3-way vs 2-way performance)

---

## 🔧 Configuration

### Adding New Tickers

1. Edit `~/projects/shared_data/stocks/tickers_config.py`:
   ```python
   def get_stocks_to_track():
       return [
           {'symbol': 'PATH', 'name': 'UiPath'},
           {'symbol': 'NVDA', 'name': 'NVIDIA'},  # Add new ticker
           # ...
       ]
   ```

2. Run collectors:
   ```bash
   python stock_sentiment.py  # Auto-picks up new ticker
   python reddit_sentiment_collector.py
   python sec_sentiment_collector.py --ticker NVDA --days 365
   python combine_sentiment_history.py
   ```

3. Add optimal weights (after backtest):
   ```python
   # In combine_sentiment_history.py
   OPTIMAL_WEIGHTS = {
       'PATH': (0.50, 0.30, 0.20),
       'NVDA': (0.60, 0.20, 0.20),  # Add weights after testing
   }
   ```

### API Credentials

**NewsAPI**: Edit `stock_sentiment.py`
```python
api_key = 'YOUR_NEWSAPI_KEY'  # Get from https://newsapi.org
```

**Reddit**: Edit `reddit_sentiment_collector.py`
```python
reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_SECRET',
    user_agent='YOUR_USER_AGENT'
)
```

**SEC**: No credentials needed (free API, just needs user-agent)

---

## 🐛 Troubleshooting

### "No SEC filings found"

**Check**: Is this an operating company or investment fund?
- NKE is an investment company, not UiPath (no filings)
- Some tickers may need manual CIK mapping

**Fix**: Add to `~/projects/shared_data/features/sec_filings.py`:
```python
self.manual_cik_mappings = {
    'PATH': '0001734722',  # UiPath Inc
    'YOUR_TICKER': '000XXXXXXX',  # Find CIK on sec.gov
}
```

### "ImportError: cannot import name 'combine_all_tickers'"

**Fix**: Function renamed to `combine_all_stocks()` in v3.0
- Update `backfill_all_tickers.py` lines 16 and 105

### Reddit API Rate Limits

**Solution**: Backfill script has built-in rate limiting (2 sec between requests)
- If still hitting limits, increase sleep time in `reddit_backfill.py`

### Sentiment not merging with price data

**Debug**:
```python
import pandas as pd
df = pd.read_csv('~/projects/shared_data/stocks/path_combined_sentiment.csv')
print(df['date'].dtype)  # Should be datetime64
print(df.head())
```

---

## 📈 Performance Metrics

### PATH (UiPath) - Current Best Results

**Before SEC (2-way)**:
- MAPE: 5.12%
- RMSE: $0.80
- Weighting: 67% NewsAPI / 33% Reddit

**After SEC (3-way)** - *backtest pending*:
- Weighting: 50% NewsAPI / 30% Reddit / 20% SEC
- Coverage: 45 days (was 23 days)
- Expected improvement: TBD

### Next Steps

1. Run 3-way backtest to measure MAPE improvement
2. Optimize SEC weighting via grid search
3. Add more tickers (NVDA, META, GOOGL)
4. Implement real-time sentiment updates

---

## 📝 Related Documentation

- **Main Technical Doc**: `TECH_DOC_SENTIMENT_PIPELINE.md` (this directory)
- **Options Project**: `~/projects/options/CLAUDE.md`
- **Shared Tickers**: `~/projects/shared_data/stocks/tickers_config.py`

---

## 🆘 Need Help?

**For a new Claude instance**: Read `TECH_DOC_SENTIMENT_PIPELINE.md` first

**For troubleshooting**: Check "Troubleshooting" section in technical doc

**For architecture questions**: See "Architecture" and "Data Flow" sections in technical doc

**For adding features**: See "Next Steps" section in technical doc

---

**Last Updated**: 2025-10-18 | **Version**: 3.0 (SEC Integration)
