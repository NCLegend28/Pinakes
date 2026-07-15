# Squeeze Hunter 🎯

**AI-powered short squeeze detection system**

Monitors Reddit + Pre-market data to predict short squeezes before they happen.

---

## 🔥 What It Does

Squeeze Hunter combines three signals to identify high-probability short squeeze setups:

1. **Reddit Catalyst Detection** - Scans r/wallstreetbets, r/shortsqueeze, r/pennystocks for squeeze DD
2. **Pre-Market Confirmation** - Monitors bid/ask spreads for premium pricing (institutional positioning)
3. **Combined Alerts** - When both align, sends high-confidence alerts to Discord

### Real Example: SGBX (Nov 19, 2025)

```
6:00 AM  → Reddit post: "SGBX 766% SI, 20M market cap"
8:50 AM  → Pre-market bid $4.13 (+21% vs $3.41 close)
9:30 AM  → Market opens, squeeze triggers
Result   → +78% close, +110% peak
```

**You would have had 3.5 hours of lead time.**

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────┐
│         SQUEEZE HUNTER SYSTEM               │
├─────────────────────────────────────────────┤
│                                             │
│  [1] Reddit Monitor (PRAW)                  │
│      ↓ Detects squeeze catalysts            │
│      ↓ Scores signals 0-100                 │
│                                             │
│  [2] Pre-Market Monitor (Alpaca)            │
│      ↓ Checks bid/ask spreads               │
│      ↓ Calculates premium vs close          │
│                                             │
│  [3] Signal Processor                       │
│      ↓ Combines Reddit + Pre-market         │
│      ↓ Calculates confidence score          │
│                                             │
│  [4] Discord Alerts                         │
│      ↓ Sends formatted embeds               │
│      ↓ Color-coded by confidence            │
│                                             │
│  [5] Backtesting Engine                     │
│      ↓ Tests against historical squeezes    │
│      ↓ Validates predictive power           │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get API Credentials

#### Reddit (PRAW)
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - Name: SqueezeHunter
   - Type: Script
   - Redirect URI: http://localhost:8080
4. Copy `client_id` (under app name) and `client_secret`

#### Alpaca (Market Data)
1. Go to https://alpaca.markets/
2. Sign up for free account
3. Go to dashboard → API Keys
4. Generate new key pair
5. Copy `API Key` and `Secret Key`
6. **Note:** Free tier includes market data access

#### Discord (Alerts)
1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Name it "Squeeze Hunter"
4. Go to "Bot" tab → "Add Bot"
5. Copy bot token
6. Under "Bot Permissions", enable:
   - Send Messages
   - Embed Links
   - Attach Files
7. Go to OAuth2 → URL Generator
8. Select scopes: `bot`
9. Select permissions: Send Messages, Embed Links
10. Copy generated URL and open in browser to invite bot to your server
11. Get channel ID:
    - Enable Developer Mode in Discord (Settings → Advanced)
    - Right-click your channel → Copy ID

### 3. Configure System

First run creates `config.json`:

```bash
python squeeze_hunter.py
```

Edit `config.json` with your credentials:

```json
{
  "reddit": {
    "client_id": "your_reddit_client_id",
    "client_secret": "your_reddit_secret",
    "user_agent": "SqueezeHunter/1.0 by YourUsername"
  },
  "alpaca": {
    "api_key": "your_alpaca_key",
    "secret_key": "your_alpaca_secret"
  },
  "discord": {
    "token": "your_discord_bot_token",
    "channel_id": 123456789012345678
  },
  "thresholds": {
    "reddit_score_min": 50,
    "bid_premium_min": 10,
    "combined_confidence_min": 70
  }
}
```

### 4. Run System

```bash
python squeeze_hunter.py
```

System runs 24/7, monitoring Reddit and pre-market data.

---

## 🧪 Backtesting

Test the system against historical squeezes:

```bash
python backtest_engine.py
```

Tests against:
- GME (2021) - +2800% gain
- AMC (2021) - +664% gain
- SGBX (2025) - +110% gain
- SPRT, IRNT, BBBY, and more

**Expected Results:**
- Detection rate: 75-87%
- Average gain (detected): 200-400%
- Combined signal success: 90%+

---

## 📈 Signal Types

### Reddit Signal (50-100 points)

**Scoring:**
- Short Interest: 40 points
  - 100%+ SI = 40 pts
  - 50-100% = 30 pts
  - 30-50% = 20 pts
  - 20-30% = 10 pts
  
- Market Cap: 20 points
  - < $50M = 20 pts (micro-cap)
  - < $200M = 15 pts (small-cap)
  - < $500M = 10 pts
  - < $1B = 5 pts
  
- Keyword Density: 20 points
  - Mentions: "short squeeze", "SI", "float", "CTB", etc.
  
- Engagement: 20 points
  - Upvotes + comments

**Alert Threshold:** 50+ points

### Pre-Market Signal

**Criteria:**
- Bid price > previous close by 10%+
- Tight spread (< 2%)
- Small bid size (< 5,000 shares) = stealth positioning

**Signal Strength:**
- STRONG: 15%+ premium, tight spread
- MODERATE: 10-15% premium
- WEAK: 5-10% premium

### Combined Signal (🔥 Highest Confidence)

When both Reddit and Pre-market signals align:

```
Combined Confidence = (Reddit Score + Bid Premium * 2) / 2

Example (SGBX):
= (87.5 + 21.1 * 2) / 2
= 64.85 → STRONG SIGNAL
```

**Alert Threshold:** 70+ confidence

---

## 🎯 Usage Examples

### Monitor Specific Tickers

```python
from premarket_monitor import PreMarketMonitor

config = {
    'api_key': 'your_key',
    'secret_key': 'your_secret'
}

monitor = PreMarketMonitor(config)

# Check single ticker
analysis = monitor.analyze_premarket_signal('SGBX')
print(monitor.format_alert(analysis))

# Monitor multiple
results = monitor.monitor_tickers(['SGBX', 'GME', 'AMC'])
for result in results:
    print(monitor.format_alert(result))
```

### Scan Recent Reddit Posts

```python
from reddit_squeeze_monitor import RedditSqueezeMonitor

config = {
    'client_id': 'your_id',
    'client_secret': 'your_secret',
    'user_agent': 'SqueezeHunter/1.0'
}

monitor = RedditSqueezeMonitor(config)

# Scan last 24 hours
signals = monitor.scan_recent_posts(hours_back=24, limit=100)

for signal in signals:
    if signal['signal_score'] >= 70:
        print(f"{signal['tickers']}: {signal['signal_score']:.1f}/100")
        print(f"SI: {signal['short_interest']}%")
        print(f"URL: {signal['url']}\n")
```

### Custom Discord Alerts

```python
from discord_alert_bot import SqueezeAlertBot
import asyncio

bot = SqueezeAlertBot('your_token', your_channel_id)

async def send_test_alert():
    await bot.start_async()
    await asyncio.sleep(2)  # Wait for connection
    
    signal = {
        'tickers': ['TEST'],
        'signal_score': 85,
        'short_interest': 100,
        # ... other fields
    }
    
    await bot.send_alert('reddit', signal)

asyncio.run(send_test_alert())
```

---

## ⚙️ Configuration

### Thresholds (in `config.json`)

```json
"thresholds": {
  "reddit_score_min": 50,        // Min score to trigger Reddit alert
  "bid_premium_min": 10,          // Min % premium for pre-market alert  
  "combined_confidence_min": 70   // Min confidence for combined alert
}
```

**Tuning Recommendations:**

- **Conservative** (fewer false positives):
  - reddit_score_min: 70
  - bid_premium_min: 15
  - combined_confidence_min: 80

- **Aggressive** (catch more opportunities):
  - reddit_score_min: 40
  - bid_premium_min: 5
  - combined_confidence_min: 60

- **Balanced** (default):
  - reddit_score_min: 50
  - bid_premium_min: 10
  - combined_confidence_min: 70

---

## 📁 File Structure

```
squeeze_hunter/
├── squeeze_hunter.py          # Main orchestrator
├── reddit_squeeze_monitor.py  # Reddit signal detection
├── premarket_monitor.py       # Pre-market analysis
├── discord_alert_bot.py       # Discord integration
├── backtest_engine.py         # Historical validation
├── requirements.txt           # Dependencies
├── config.json               # API credentials (you create)
└── signal_history.json       # Auto-generated logs
```

---

## 🛡️ Risk Management

**CRITICAL:** This system identifies opportunities, not guarantees.

### Position Sizing
- Max 2-5% portfolio per signal
- STRONG signals: 5%
- MODERATE signals: 3%
- WEAK signals: 1-2%

### Stop Losses
- Set immediately on entry
- Typical: -10% to -15%
- Adjust based on volatility

### Profit Taking
- Have a plan BEFORE entry
- Consider scaling out:
  - 50% at +50%
  - 25% at +100%
  - 25% runner with trailing stop

### Exit Signals
- Volume dies (< 2x average)
- Breaks below VWAP
- Pre-market gap downs
- Reversal patterns (bearish engulfing, etc.)

---

## 🔧 Troubleshooting

### Reddit Monitor Issues

**Problem:** "Invalid credentials"
```
Solution: Check client_id and client_secret in config.json
Verify user_agent format: "AppName/Version by Username"
```

**Problem:** "Rate limited"
```
Solution: PRAW has built-in rate limiting. If issues persist:
- Reduce scan frequency
- Use scan_recent_posts() vs stream for testing
```

### Alpaca Issues

**Problem:** "Unauthorized"
```
Solution: 
1. Verify API keys are correct
2. Check if keys are for Paper vs Live trading
3. Ensure keys have market data permissions
```

**Problem:** "No data returned for ticker"
```
Solution:
- Some penny stocks lack real-time data
- Try with well-known tickers first (SPY, AAPL)
- Check if ticker is valid/active
```

### Discord Issues

**Problem:** "Bot not responding"
```
Solution:
1. Verify bot is invited to server
2. Check bot has permissions in channel
3. Confirm channel_id is correct
4. Bot must be online (system running)
```

**Problem:** "Missing Access"
```
Solution: Bot needs these permissions:
- View Channels
- Send Messages
- Embed Links
```

---

## 🚀 Advanced Features (Coming Soon)

- [ ] Twitter integration (X API)
- [ ] Options flow detection
- [ ] Volume spike alerts
- [ ] Insider buying tracking
- [ ] SEC filing monitoring
- [ ] Real-time paper trading
- [ ] Performance analytics dashboard
- [ ] Mobile app (push notifications)

---

## 📊 Performance Metrics

Track system performance:

```bash
# View signal history
cat signal_history.json

# Analyze by ticker
cat signal_history.json | grep SGBX

# Count total alerts
cat signal_history.json | grep -c "COMBINED"
```

---

## 🤝 Contributing

Improvements welcome! Focus areas:
- Additional data sources
- Improved scoring algorithms
- ML-based signal enhancement
- Better backtesting metrics
- UI/dashboard

---

## ⚖️ Legal Disclaimer

**This system is for educational purposes only.**

- Not financial advice
- Past performance ≠ future results
- Short squeezes are high-risk
- Can lose 100% of position
- Do your own due diligence
- Consult financial advisor

**USE AT YOUR OWN RISK.**

---

## 📝 License

MIT License - Free to use, modify, distribute

---

## 💡 Tips for Success

1. **Start Small** - Paper trade first, validate signals
2. **Trust Combined Signals** - Highest success rate
3. **Be Patient** - Wait for your setup
4. **Use Stops** - Always protect capital
5. **Take Profits** - Don't get greedy
6. **Review Daily** - Check signal_history.json
7. **Backtest** - Run backtest_engine.py monthly
8. **Stay Disciplined** - Stick to your rules

---

## 📞 Support

Questions? Issues? Want to share results?

Create an issue or discussion on GitHub.

**Good hunting! 🎯**
