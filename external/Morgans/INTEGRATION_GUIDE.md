# Sentiment Bot Integration Guide

## Overview
The sentiment analysis bot is now integrated with the crypto trading bot via a shared file system approach.

## Architecture

```
Morgans (Sentiment Bot)          Redpill (Trading Bot)
├── sentimentBot.py         ←→   ├── crypto_bot.py
├── automate.py                  ├── sentiment_reader.py
└── Saves to shared dir          └── Reads from shared dir

            ↓                             ↑
    ~/projects/shared_data/sentiment/
    ├── crypto/
    │   ├── btc_latest.json
    │   ├── btc_sentiment.csv
    │   ├── eth_latest.json
    │   ├── eth_sentiment.csv
    │   └── ...
    └── stocks/  (for future use)
```

## How It Works

### 1. Sentiment Data Generation (Morgans)
- `automate.py` runs continuously (or on schedule)
- Fetches news from NewsAPI and CryptoPanic every hour
- Analyzes sentiment using VADER + Keywords + optional FinBERT
- Saves two files per crypto:
  - `{symbol}_latest.json` - Current sentiment summary
  - `{symbol}_sentiment.csv` - Historical data

### 2. Sentiment Reading (Redpill)
- `sentiment_reader.py` module provides easy access to sentiment data
- Trading bot imports and uses it during decision-making
- Sentiment adjusts ML confidence scores up or down

### 3. Trading Decision Integration
When the trading bot considers a trade:
1. ML model generates signal + confidence
2. Sentiment reader checks latest sentiment
3. If sentiment agrees → boost confidence
4. If sentiment contradicts → reduce confidence
5. Trade only executes if adjusted confidence > threshold

## Running the System

### Start Sentiment Bot
```bash
cd ~/projects/Morgans
source .venv/bin/activate
python automate.py
```

This will:
- Run immediately on startup
- Continue running every hour
- Track BTC, ETH, XLM, ADA, ATOM, LTC

### Start Trading Bot
```bash
cd ~/projects/Redpill
source venv/bin/activate
python crypto_bot.py
```

The trading bot will automatically read sentiment data if available.

## Configuration

### Sentiment Bot (.env in Morgans/)
```bash
NEWSAPI_KEY=your_key
CRYPTOPANIC_KEY=your_key
UPDATE_INTERVAL_HOURS=1
FINBERT_ENABLED=false
VADER_ENABLED=true
```

### Trading Bot (.env in Redpill/)
```bash
# How much sentiment influences trading (0.0 to 1.0)
SENTIMENT_WEIGHT=0.2

# If sentiment agrees: confidence += (sentiment_score * SENTIMENT_WEIGHT)
# If sentiment contradicts: confidence -= (sentiment_score * SENTIMENT_WEIGHT)
```

## Example Scenarios

### Scenario 1: Sentiment Boosts Trade
```
ML Signal: BUY ETH at 0.70 confidence
Sentiment: Bullish (+0.227)
Adjustment: +0.227 * 0.2 = +0.045
Final Confidence: 0.745
Result: ✅ Trade executes (above 0.60 threshold)
```

### Scenario 2: Sentiment Blocks Trade
```
ML Signal: BUY BTC at 0.62 confidence
Sentiment: Bearish (-0.35)
Adjustment: -0.35 * 0.2 = -0.07
Final Confidence: 0.55
Result: ❌ Trade blocked (below 0.60 threshold)
```

### Scenario 3: No Sentiment Data
```
ML Signal: BUY ADA at 0.65 confidence
Sentiment: None available
Adjustment: 0
Final Confidence: 0.65
Result: ✅ Trade executes (uses original confidence)
```

## Monitored Coins

Current sentiment tracking:
- **BTC** - Bitcoin
- **ETH** - Ethereum
- **XLM** - Stellar Lumens
- **ADA** - Cardano
- **ATOM** - Cosmos
- **LTC** - Litecoin

To add more, edit `COINS_TO_TRACK` in `automate.py`.

## Advantages of This Approach

✅ **No API server needed** - Simple file-based communication
✅ **Independent operation** - Bots can run separately or together
✅ **Persistent data** - Sentiment history saved in CSV
✅ **Easy debugging** - Can inspect JSON/CSV files directly
✅ **Scalable** - Add stocks later in `stocks/` folder
✅ **Fault tolerant** - Trading bot works without sentiment data

## Future Enhancements

- [ ] Stock sentiment analysis (use `stocks/` directory)
- [ ] Real-time sentiment alerts via webhook
- [ ] Sentiment trend analysis (improving/declining)
- [ ] Multi-timeframe sentiment (1h, 4h, 24h)
- [ ] Sentiment-based position sizing
- [ ] Email/SMS alerts on major sentiment shifts

## Logs and Monitoring

Check sentiment bot logs:
```bash
cat ~/projects/Morgans/crypto_bot.log
```

Check trading bot logs:
```bash
cat ~/projects/Redpill/crypto_bot.log
```

View latest sentiment:
```bash
cat ~/projects/shared_data/sentiment/crypto/eth_latest.json
```

## Troubleshooting

**Problem:** Trading bot can't find sentiment data
- **Solution:** Make sure automate.py has run at least once
- Check: `ls ~/projects/shared_data/sentiment/crypto/`

**Problem:** Sentiment data is stale
- **Solution:** Check if automate.py is running
- Sentiment older than 6 hours triggers a warning

**Problem:** Too many/few trades after integration
- **Solution:** Adjust `SENTIMENT_WEIGHT` in Redpill/.env
- Lower value (0.1) = less sentiment influence
- Higher value (0.3) = more sentiment influence
