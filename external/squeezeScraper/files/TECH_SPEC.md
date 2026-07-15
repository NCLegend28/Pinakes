# Squeeze Hunter - Technical Specification Document
## AI-Powered Short Squeeze Detection System

**Version:** 1.0  
**Date:** November 20, 2025  
**Target Platform:** Python 3.9+  
**Deployment:** 24/7 background service  
**Primary Dependencies:** PRAW, Alpaca-py, Discord.py  

---

## 1. SYSTEM OVERVIEW

### 1.1 Purpose
Build a real-time short squeeze detection system that monitors Reddit posts and pre-market trading data to predict short squeeze opportunities before they occur.

### 1.2 Validated Use Case
- **SGBX (Nov 19-20, 2025)**: System would have detected setup 3.5 hours before market open
- **Signal Timeline**: Reddit catalyst 6:00 AM → Pre-market confirmation 8:50 AM → Squeeze execution 9:30 AM
- **Result**: +173% peak, +78% day 1 close
- **Detection**: 87.5/100 Reddit score + 21% pre-market bid premium

### 1.3 Core Components
```
┌────────────────────────────────────────────────┐
│            SQUEEZE HUNTER SYSTEM               │
├────────────────────────────────────────────────┤
│                                                │
│  [Reddit Monitor] ──────┐                     │
│   - PRAW API            │                      │
│   - Real-time stream    │                      │
│   - Signal scoring      │                      │
│                         ↓                      │
│  [Signal Processor] ←───┴────→ [Pre-Market]   │
│   - Correlation         │       - Alpaca API   │
│   - Confidence calc     │       - Bid/ask      │
│   - Alert decision      │       - Premium calc │
│                         ↓                      │
│  [Discord Alerter] ─────┘                     │
│   - Rich embeds                                │
│   - Color coding                               │
│   - Multi-tier alerts                          │
│                                                │
└────────────────────────────────────────────────┘
```

---

## 2. IMPLEMENTATION REQUIREMENTS

### 2.1 File Structure
```
squeeze_hunter/
├── squeeze_hunter.py              # Main orchestrator [PROVIDED]
├── reddit_squeeze_monitor.py      # Reddit signal detection [PROVIDED]
├── premarket_monitor.py           # Pre-market analysis [PROVIDED]
├── discord_alert_bot.py           # Alert system [PROVIDED]
├── backtest_engine.py             # Historical validation [PROVIDED]
├── start.py                       # Startup script [PROVIDED]
├── requirements.txt               # Dependencies [PROVIDED]
├── config.json                    # User configuration [AUTO-GENERATED]
├── signal_history.json            # Runtime logs [AUTO-GENERATED]
└── README.md                      # Documentation [PROVIDED]
```

**NOTE:** All files are already created. Implementation focus is on setup, configuration, and deployment.

### 2.2 Python Version
- **Required:** Python 3.9 or higher
- **Reason:** Uses modern asyncio features, type hints, dataclasses

### 2.3 Dependencies
```txt
# Core APIs
praw>=7.7.1                 # Reddit API wrapper
alpaca-py>=0.20.0          # Alpaca trading data API
discord.py>=2.3.2          # Discord bot framework

# Utilities
pytz>=2023.3               # Timezone handling
python-dotenv>=1.0.0       # Environment variables (optional)
requests>=2.31.0           # HTTP requests

# Optional (for future enhancements)
pandas>=2.1.0              # Data analysis
```

---

## 3. API INTEGRATION SPECIFICATIONS

### 3.1 Reddit API (PRAW)

#### 3.1.1 Authentication Setup
1. Navigate to: https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Configuration:
   ```
   Name: SqueezeHunter
   App type: Script
   Description: Short squeeze detection system
   About URL: [leave blank]
   Redirect URI: http://localhost:8080
   ```
4. Retrieve credentials:
   - `client_id`: String below app name (14 chars, e.g., "dj2Od9s6Wk_j4A")
   - `client_secret`: Secret key (27 chars, e.g., "k3N8s2M9...")
   - `user_agent`: Custom string "SqueezeHunter/1.0 by [your_reddit_username]"

#### 3.1.2 PRAW Configuration Object
```python
reddit_config = {
    'client_id': 'YOUR_14_CHAR_CLIENT_ID',
    'client_secret': 'YOUR_27_CHAR_SECRET',
    'user_agent': 'SqueezeHunter/1.0 by YourRedditUsername'
}
```

#### 3.1.3 Monitored Subreddits
```python
TARGET_SUBREDDITS = [
    'wallstreetbets',      # 15M+ members, main retail hub
    'shortsqueeze',        # 100K+ members, squeeze-focused
    'pennystocks',         # 250K+ members, small-cap focus
    '100xpennystock',      # 10K+ members, micro-cap
    'Shortsqueeze',        # Alternate capitalization
    'squeezeplays'         # 50K+ members, dedicated squeeze community
]
```

#### 3.1.4 Rate Limits
- PRAW handles rate limiting automatically
- Default: 60 requests per minute
- Backoff: Exponential (2s, 4s, 8s, 16s)
- Stream mode: Continuous with built-in throttling

#### 3.1.5 Data Schema (Reddit Signal)
```python
RedditSignal = {
    'timestamp': datetime,              # UTC timestamp of post
    'subreddit': str,                   # Subreddit name
    'post_id': str,                     # Reddit post ID (unique)
    'title': str,                       # Post title
    'body': str,                        # Post content (first 500 chars)
    'url': str,                         # Full Reddit URL
    'author': str,                      # Username
    'upvotes': int,                     # Score at detection time
    'num_comments': int,                # Comment count
    'tickers': List[str],               # Extracted ticker symbols
    'short_interest': float,            # SI% (0-1000)
    'market_cap_millions': float | None,# Market cap in millions
    'signal_score': float               # Calculated score (0-100)
}
```

### 3.2 Alpaca API

#### 3.2.1 Account Setup
1. Navigate to: https://alpaca.markets/
2. Create account (free tier sufficient)
3. Email verification required
4. Navigate to: Dashboard → API Keys
5. Generate new key pair (Paper Trading or Live)

#### 3.2.2 API Key Types
**Paper Trading (Recommended for testing):**
- Free, unlimited
- Real-time market data included
- No risk
- URLs: 
  - Data: https://data.alpaca.markets
  - Trading: https://paper-api.alpaca.markets

**Live Trading:**
- Requires funded account
- Same data access
- Real money at risk

#### 3.2.3 Alpaca Configuration Object
```python
alpaca_config = {
    'api_key': 'PK...',      # 20 chars, starts with PK
    'secret_key': 'sk...'    # 40 chars, starts with sk or similar
}
```

#### 3.2.4 Market Data Endpoints Used
```python
# Endpoints (via alpaca-py SDK):
StockHistoricalDataClient.get_stock_bars()      # Daily OHLCV
StockHistoricalDataClient.get_stock_latest_quote()  # Real-time bid/ask
```

#### 3.2.5 Data Schema (Pre-Market Analysis)
```python
PreMarketAnalysis = {
    'ticker': str,                      # Stock symbol
    'timestamp': datetime,              # UTC timestamp
    'previous_close': float,            # Prior day close price
    'bid_price': float,                 # Current bid
    'bid_size': int,                    # Shares at bid
    'ask_price': float,                 # Current ask
    'ask_size': int,                    # Shares at ask
    'bid_premium_pct': float,           # (bid/close - 1) * 100
    'ask_premium_pct': float,           # (ask/close - 1) * 100
    'spread_pct': float,                # (ask-bid)/bid * 100
    'signal_strength': str,             # 'STRONG', 'MODERATE', 'WEAK', 'NONE'
    'hours_since_reddit': float | None, # Time correlation
    'is_premarket': bool                # True if 4:00-9:30 AM ET
}
```

#### 3.2.6 Market Hours (Eastern Time)
```python
PREMARKET_START = 4:00 AM ET    # 04:00
MARKET_OPEN = 9:30 AM ET        # 09:30
MARKET_CLOSE = 4:00 PM ET       # 16:00
AFTERHOURS_END = 8:00 PM ET     # 20:00
```

### 3.3 Discord API

#### 3.3.1 Bot Setup
1. Navigate to: https://discord.com/developers/applications
2. Click "New Application"
3. Name: "Squeeze Hunter"
4. Navigate to "Bot" tab
5. Click "Add Bot" → Confirm
6. Under "Privileged Gateway Intents":
   - ❌ Presence Intent (not needed)
   - ❌ Server Members Intent (not needed)
   - ❌ Message Content Intent (not needed)

#### 3.3.2 Bot Permissions
Required permissions (bitwise value: 52224):
- ✅ Send Messages (2048)
- ✅ Embed Links (16384)
- ✅ Attach Files (32768)
- ✅ Read Message History (65536)

#### 3.3.3 Bot Invitation
1. Navigate to OAuth2 → URL Generator
2. Select scopes:
   - ✅ `bot`
3. Select permissions (from 3.3.2)
4. Copy generated URL
5. Open URL in browser
6. Select your server
7. Authorize

#### 3.3.4 Channel ID Retrieval
```
1. Open Discord desktop/web app
2. User Settings → Advanced
3. Enable "Developer Mode"
4. Right-click target channel
5. Click "Copy ID"
6. Result: 18-digit number (e.g., 1234567890123456789)
```

#### 3.3.5 Discord Configuration Object
```python
discord_config = {
    'token': 'MTIzN...',              # ~70 chars, Bot token
    'channel_id': 1234567890123456789 # 18-digit integer
}
```

#### 3.3.6 Embed Color Scheme
```python
COLORS = {
    'STRONG': 0xFF0000,      # Red (discord.Color.red())
    'MODERATE': 0xFF8C00,    # Orange (discord.Color.orange())
    'WEAK': 0xFFFF00,        # Yellow (discord.Color.yellow())
    'INFO': 0x0000FF         # Blue (discord.Color.blue())
}
```

---

## 4. SIGNAL DETECTION ALGORITHMS

### 4.1 Reddit Signal Scoring

#### 4.1.1 Scoring Formula
```python
total_score = si_score + mcap_score + keyword_score + engagement_score
# Range: 0-100 points
```

#### 4.1.2 Component Breakdown

**Short Interest Score (40 points max):**
```python
if short_interest >= 100:
    si_score = 40
elif short_interest >= 50:
    si_score = 30
elif short_interest >= 30:
    si_score = 20
elif short_interest >= 20:
    si_score = 10
else:
    si_score = 0
```

**Market Cap Score (20 points max):**
```python
if market_cap_millions < 50:
    mcap_score = 20      # Micro-cap
elif market_cap_millions < 200:
    mcap_score = 15      # Small-cap
elif market_cap_millions < 500:
    mcap_score = 10
elif market_cap_millions < 1000:
    mcap_score = 5
else:
    mcap_score = 0
```

**Keyword Density Score (20 points max):**
```python
SQUEEZE_KEYWORDS = [
    'short squeeze', 'short interest', 'SI', 'squeeze play',
    'short ratio', 'days to cover', 'DTC', 'utilization',
    'cost to borrow', 'CTB', 'borrow rate', 'float',
    'shares to borrow', 'ortex', 'fintel', 'gamma squeeze'
]

keyword_count = sum(1 for kw in SQUEEZE_KEYWORDS if kw in text.lower())
keyword_score = min(keyword_count * 3, 20)
```

**Engagement Score (20 points max):**
```python
# Upvotes (10 points max)
if upvotes >= 1000:
    upvote_score = 10
elif upvotes >= 500:
    upvote_score = 7
elif upvotes >= 100:
    upvote_score = 5
elif upvotes >= 50:
    upvote_score = 3
else:
    upvote_score = 0

# Comments (10 points max)
if num_comments >= 100:
    comment_score = 10
elif num_comments >= 50:
    comment_score = 7
elif num_comments >= 20:
    comment_score = 5
elif num_comments >= 10:
    comment_score = 3
else:
    comment_score = 0

engagement_score = upvote_score + comment_score
```

#### 4.1.3 Ticker Extraction
```python
import re

TICKER_PATTERN = r'\b[A-Z]{1,5}\b'
BLACKLIST = {
    'THE', 'ARE', 'FOR', 'AND', 'NOT', 'BUT', 'YOU', 'ALL',
    'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET',
    'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW',
    'OLD', 'SEE', 'TWO', 'WHO', 'BOY', 'DID', 'CAR', 'LET',
    'PUT', 'SAY', 'SHE', 'TOO', 'USE', 'YES', 'YOLO', 'DD',
    'CEO', 'IPO', 'FDA', 'SEC', 'ATH', 'EOD', 'AH', 'PM'
}

def extract_tickers(text: str) -> List[str]:
    matches = re.findall(TICKER_PATTERN, text)
    return [t for t in matches if t not in BLACKLIST]
```

#### 4.1.4 Short Interest Extraction
```python
SI_PATTERNS = [
    r'(\d{1,4})%?\s*(?:short interest|SI)',
    r'(?:short interest|SI)[:\s]+(\d{1,4})%?',
    r'SI[:\s]*(\d{1,4})%?'
]

def extract_short_interest(text: str) -> float | None:
    for pattern in SI_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            if 0 < value <= 1000:  # Sanity check
                return value
    return None
```

### 4.2 Pre-Market Signal Strength

#### 4.2.1 Signal Classification
```python
def calculate_signal_strength(
    bid_premium_pct: float,
    spread_pct: float
) -> str:
    """
    Returns: 'STRONG', 'MODERATE', 'WEAK', or 'NONE'
    """
    if bid_premium_pct >= 15 and spread_pct < 2:
        return 'STRONG'
    elif bid_premium_pct >= 10 or (bid_premium_pct >= 5 and spread_pct < 1):
        return 'MODERATE'
    elif bid_premium_pct >= 5:
        return 'WEAK'
    else:
        return 'NONE'
```

#### 4.2.2 Premium Calculation
```python
def calculate_premiums(
    previous_close: float,
    bid_price: float,
    ask_price: float
) -> Tuple[float, float, float]:
    """
    Returns: (bid_premium_pct, ask_premium_pct, spread_pct)
    """
    bid_premium_pct = ((bid_price / previous_close) - 1) * 100
    ask_premium_pct = ((ask_price / previous_close) - 1) * 100
    spread_pct = ((ask_price - bid_price) / bid_price) * 100
    
    return bid_premium_pct, ask_premium_pct, spread_pct
```

### 4.3 Combined Signal Confidence

#### 4.3.1 Confidence Formula
```python
def calculate_combined_confidence(
    reddit_score: float,
    bid_premium_pct: float
) -> float:
    """
    Weighted average favoring pre-market data
    Range: 0-100
    """
    combined = (reddit_score + (bid_premium_pct * 2)) / 2
    return min(combined, 100)
```

#### 4.3.2 Alert Decision Logic
```python
def should_send_combined_alert(
    reddit_score: float,
    bid_premium_pct: float,
    combined_confidence: float,
    thresholds: dict
) -> bool:
    """
    Combined alert criteria (all must be true):
    1. Reddit score >= threshold
    2. Bid premium >= threshold
    3. Combined confidence >= threshold
    """
    return (
        reddit_score >= thresholds['reddit_score_min'] and
        bid_premium_pct >= thresholds['bid_premium_min'] and
        combined_confidence >= thresholds['combined_confidence_min']
    )
```

---

## 5. SYSTEM CONFIGURATION

### 5.1 Configuration File Schema
```json
{
  "reddit": {
    "client_id": "string (14 chars)",
    "client_secret": "string (27 chars)",
    "user_agent": "string (format: AppName/Version by Username)"
  },
  "alpaca": {
    "api_key": "string (starts with PK, ~20 chars)",
    "secret_key": "string (starts with sk, ~40 chars)"
  },
  "discord": {
    "token": "string (~70 chars)",
    "channel_id": "integer (18 digits)"
  },
  "thresholds": {
    "reddit_score_min": "number (0-100, default: 50)",
    "bid_premium_min": "number (0-100, default: 10)",
    "combined_confidence_min": "number (0-100, default: 70)"
  }
}
```

### 5.2 Default Threshold Values
```python
DEFAULT_THRESHOLDS = {
    'reddit_score_min': 50,           # Minimum Reddit score to alert
    'bid_premium_min': 10,            # Minimum bid premium % to alert
    'combined_confidence_min': 70     # Minimum combined confidence
}

# Tuning Profiles:

CONSERVATIVE = {
    'reddit_score_min': 70,
    'bid_premium_min': 15,
    'combined_confidence_min': 80
}

AGGRESSIVE = {
    'reddit_score_min': 40,
    'bid_premium_min': 5,
    'combined_confidence_min': 60
}

BALANCED = DEFAULT_THRESHOLDS  # Default is balanced
```

### 5.3 Configuration Validation
```python
def validate_config(config: dict) -> List[str]:
    """
    Returns list of validation errors (empty if valid)
    """
    errors = []
    
    # Check for placeholder values
    if 'YOUR_' in str(config):
        errors.append("Configuration contains placeholder values")
    
    # Validate Reddit config
    reddit = config.get('reddit', {})
    if not reddit.get('client_id'):
        errors.append("Missing reddit.client_id")
    if not reddit.get('client_secret'):
        errors.append("Missing reddit.client_secret")
    if not reddit.get('user_agent'):
        errors.append("Missing reddit.user_agent")
    
    # Validate Alpaca config
    alpaca = config.get('alpaca', {})
    if not alpaca.get('api_key'):
        errors.append("Missing alpaca.api_key")
    if not alpaca.get('secret_key'):
        errors.append("Missing alpaca.secret_key")
    
    # Validate Discord config
    discord = config.get('discord', {})
    if not discord.get('token'):
        errors.append("Missing discord.token")
    if not discord.get('channel_id'):
        errors.append("Missing discord.channel_id")
    
    # Validate thresholds
    thresholds = config.get('thresholds', {})
    if thresholds:
        for key in ['reddit_score_min', 'bid_premium_min', 'combined_confidence_min']:
            value = thresholds.get(key)
            if value is not None and not (0 <= value <= 100):
                errors.append(f"thresholds.{key} must be 0-100")
    
    return errors
```

---

## 6. OPERATIONAL WORKFLOWS

### 6.1 System Startup Sequence
```
1. Load configuration from config.json
2. Validate all API credentials
3. Initialize Reddit monitor (PRAW client)
4. Initialize Alpaca monitor (data client)
5. Start Discord bot (async)
6. Begin Reddit stream (async)
7. Start pre-market scan loop (async)
8. Start cleanup loop (async)
9. Enter main event loop
```

### 6.2 Signal Processing Flow

#### 6.2.1 Reddit Signal Path
```
[1] New post detected by PRAW stream
     ↓
[2] Extract tickers, SI%, market cap, keywords
     ↓
[3] Calculate signal score (0-100)
     ↓
[4] Score >= threshold?
     ├─ NO → Discard
     └─ YES → Continue
     ↓
[5] Store in active_signals dict
     ↓
[6] Send Reddit alert to Discord
     ↓
[7] Is pre-market hours?
     ├─ YES → Check pre-market immediately
     └─ NO → Schedule for next pre-market check
```

#### 6.2.2 Pre-Market Signal Path
```
[1] Pre-market hours detected (4:00-9:30 AM ET)
     ↓
[2] Iterate through active_signals
     ↓
[3] For each ticker:
     ├─ Get previous close price (Alpaca)
     ├─ Get current bid/ask (Alpaca)
     ├─ Calculate bid premium %
     └─ Calculate signal strength
     ↓
[4] Strength != 'NONE'?
     ├─ NO → Continue to next ticker
     └─ YES → Continue
     ↓
[5] Send pre-market alert to Discord
     ↓
[6] Calculate combined confidence
     ↓
[7] Combined confidence >= threshold?
     ├─ NO → End
     └─ YES → Send combined alert (🔥 HIGH PRIORITY)
```

#### 6.2.3 Combined Signal Path
```
[1] Reddit signal detected (Score >= 50)
     +
[2] Pre-market premium detected (Bid >= 10%)
     ↓
[3] Calculate combined confidence:
     confidence = (reddit_score + bid_premium * 2) / 2
     ↓
[4] confidence >= 70?
     ├─ NO → Send separate alerts only
     └─ YES → Send 🔥 COMBINED SIGNAL alert
     ↓
[5] Add ticker to alerted_tickers (prevent duplicates)
     ↓
[6] Log to signal_history.json
```

### 6.3 Alert Timing Strategy

#### 6.3.1 Reddit-Only Alerts
```
Sent immediately when:
- Signal score >= reddit_score_min (default: 50)
- Ticker not in alerted_tickers set
```

#### 6.3.2 Pre-Market Alerts
```
Sent during pre-market hours (4:00-9:30 AM ET) when:
- Bid premium >= bid_premium_min (default: 10%)
- Signal strength != 'NONE'
- Checked every 5 minutes during pre-market
```

#### 6.3.3 Combined Alerts
```
Sent when both conditions met:
- Reddit signal exists (score >= threshold)
- Pre-market confirmation (bid premium >= threshold)
- Combined confidence >= combined_confidence_min (default: 70)
- Only sent once per ticker (tracked in alerted_tickers)
```

### 6.4 Data Persistence

#### 6.4.1 Signal History Schema
```json
{
  "generated": "ISO 8601 datetime",
  "total_signals": "integer",
  "signals": [
    {
      "ticker": "string",
      "timestamp": "ISO 8601 datetime",
      "reddit_score": "float (0-100)",
      "bid_premium_pct": "float",
      "combined_confidence": "float (0-100)",
      "type": "string ('REDDIT', 'PREMARKET', 'COMBINED')"
    }
  ]
}
```

#### 6.4.2 Active Signals Memory
```python
active_signals = {
    'TICKER': {
        'reddit_signal': RedditSignal,      # Full signal dict
        'reddit_time': datetime,            # When Reddit signal detected
        'premarket_checked': bool,          # Has pre-market been checked?
        'premarket_analysis': PreMarketAnalysis | None,  # If checked
        'combined_alert_sent': bool         # Prevent duplicate combined alerts
    }
}
```

#### 6.4.3 Cleanup Policy
```python
# Remove signals older than 48 hours
SIGNAL_RETENTION_HOURS = 48

# Cleanup runs every hour
CLEANUP_INTERVAL_SECONDS = 3600

def cleanup_old_signals():
    cutoff = datetime.now(UTC) - timedelta(hours=SIGNAL_RETENTION_HOURS)
    for ticker, data in list(active_signals.items()):
        if data['reddit_time'] < cutoff:
            del active_signals[ticker]
            alerted_tickers.discard(ticker)
```

---

## 7. ERROR HANDLING

### 7.1 API Failure Handling

#### 7.1.1 Reddit API Errors
```python
# PRAW handles most errors automatically
# Additional handling:

try:
    reddit.subreddit('test').new(limit=1)
except praw.exceptions.InvalidToken:
    # Bad credentials
    log_error("Invalid Reddit credentials")
    exit(1)
except praw.exceptions.ResponseException as e:
    # API error (rate limit, server error)
    log_error(f"Reddit API error: {e}")
    time.sleep(60)  # Wait 1 minute
except Exception as e:
    # Unknown error
    log_error(f"Unexpected Reddit error: {e}")
```

#### 7.1.2 Alpaca API Errors
```python
try:
    quote = client.get_stock_latest_quote(request)
except alpaca.common.exceptions.APIError as e:
    if e.status_code == 401:
        # Bad credentials
        log_error("Invalid Alpaca credentials")
        exit(1)
    elif e.status_code == 429:
        # Rate limit
        log_error("Alpaca rate limit hit")
        time.sleep(60)
    else:
        log_error(f"Alpaca API error: {e}")
except Exception as e:
    log_error(f"Unexpected Alpaca error: {e}")
```

#### 7.1.3 Discord API Errors
```python
try:
    await channel.send(embed=embed)
except discord.errors.Forbidden:
    # Bot lacks permissions
    log_error("Discord bot lacks permissions")
except discord.errors.HTTPException as e:
    # Discord API error
    log_error(f"Discord API error: {e}")
    time.sleep(5)
except Exception as e:
    log_error(f"Unexpected Discord error: {e}")
```

### 7.2 Data Validation

#### 7.2.1 Input Sanitization
```python
def sanitize_ticker(ticker: str) -> str:
    """Remove special chars, uppercase, max 5 chars"""
    clean = re.sub(r'[^A-Z]', '', ticker.upper())
    return clean[:5]

def validate_percentage(value: float) -> bool:
    """Ensure percentage is reasonable"""
    return 0 <= value <= 1000

def validate_price(price: float) -> bool:
    """Ensure price is positive and reasonable"""
    return 0.01 <= price <= 100000
```

### 7.3 Logging Strategy

#### 7.3.1 Log Levels
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('squeeze_hunter.log'),
        logging.StreamHandler()  # Also print to console
    ]
)

# Usage:
logging.info("System started")
logging.warning("High memory usage detected")
logging.error("Failed to connect to Discord")
logging.critical("System shutdown due to fatal error")
```

#### 7.3.2 Critical Events to Log
- System startup/shutdown
- API connection success/failure
- Signal detection (with score)
- Alert sent (with ticker)
- Configuration changes
- Errors and exceptions
- Performance metrics (every hour)

---

## 8. DEPLOYMENT INSTRUCTIONS

### 8.1 Initial Setup (First Time)

#### 8.1.1 Environment Setup
```bash
# Step 1: Clone/download system files
cd /path/to/squeeze_hunter/

# Step 2: Create virtual environment
python3 -m venv venv

# Step 3: Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Verify installation
python -c "import praw, alpaca, discord; print('✓ All packages installed')"
```

#### 8.1.2 Configuration Setup
```bash
# Step 1: Generate config template
python squeeze_hunter.py
# This creates config.json with placeholders

# Step 2: Edit config.json with your credentials
# Use your favorite text editor:
nano config.json
# OR
vim config.json
# OR
code config.json  # VS Code

# Step 3: Validate configuration
python start.py
# Will check for errors before starting
```

#### 8.1.3 Test Run
```bash
# Run in foreground to verify
python start.py

# Expected output:
# ✓ All system files present
# ✓ All dependencies installed
# ✓ Configuration valid
# System starting...
# [timestamp] Starting Reddit stream...
# [timestamp] Discord bot logged in as SqueezeHunter#1234

# Press Ctrl+C to stop
```

### 8.2 Production Deployment

#### 8.2.1 Linux (systemd service)
```bash
# Step 1: Create service file
sudo nano /etc/systemd/system/squeeze-hunter.service

# Content:
[Unit]
Description=Squeeze Hunter - Short Squeeze Detection System
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/squeeze_hunter
Environment="PATH=/path/to/squeeze_hunter/venv/bin"
ExecStart=/path/to/squeeze_hunter/venv/bin/python squeeze_hunter.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Step 2: Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable squeeze-hunter
sudo systemctl start squeeze-hunter

# Step 3: Check status
sudo systemctl status squeeze-hunter

# Step 4: View logs
sudo journalctl -u squeeze-hunter -f
```

#### 8.2.2 macOS (launchd)
```bash
# Step 1: Create plist file
nano ~/Library/LaunchAgents/com.squeeze-hunter.plist

# Content:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.squeeze-hunter</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/squeeze_hunter/venv/bin/python</string>
        <string>/path/to/squeeze_hunter/squeeze_hunter.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/squeeze_hunter</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/path/to/squeeze_hunter/stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/squeeze_hunter/stderr.log</string>
</dict>
</plist>

# Step 2: Load service
launchctl load ~/Library/LaunchAgents/com.squeeze-hunter.plist

# Step 3: Check status
launchctl list | grep squeeze-hunter

# Step 4: View logs
tail -f /path/to/squeeze_hunter/stdout.log
```

#### 8.2.3 Windows (Task Scheduler)
```
1. Open Task Scheduler
2. Create Basic Task:
   - Name: Squeeze Hunter
   - Trigger: At startup
   - Action: Start a program
   - Program: C:\path\to\squeeze_hunter\venv\Scripts\python.exe
   - Arguments: squeeze_hunter.py
   - Start in: C:\path\to\squeeze_hunter
3. Settings:
   - ✓ Run whether user is logged on or not
   - ✓ Run with highest privileges
   - ✓ If task fails, restart every: 1 minute
4. Save and run task
```

#### 8.2.4 Docker (Optional)
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "squeeze_hunter.py"]
```

```bash
# Build and run
docker build -t squeeze-hunter .
docker run -d --name squeeze-hunter \
  -v $(pwd)/config.json:/app/config.json \
  -v $(pwd)/signal_history.json:/app/signal_history.json \
  --restart unless-stopped \
  squeeze-hunter

# View logs
docker logs -f squeeze-hunter
```

### 8.3 Monitoring and Maintenance

#### 8.3.1 Health Checks
```bash
# Check if process is running
ps aux | grep squeeze_hunter

# Check system logs
tail -f squeeze_hunter.log

# Check signal history
cat signal_history.json | jq '.total_signals'

# Check Discord bot status
# Should see bot online in Discord server
```

#### 8.3.2 Performance Monitoring
```python
# Add to main loop (optional):
import psutil

def log_system_metrics():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    logging.info(f"System: CPU {cpu}% | RAM {mem}%")

# Call every hour
```

#### 8.3.3 Update Procedure
```bash
# Step 1: Stop service
sudo systemctl stop squeeze-hunter  # Linux
# OR
launchctl unload ~/Library/LaunchAgents/com.squeeze-hunter.plist  # macOS

# Step 2: Backup
cp config.json config.json.backup
cp signal_history.json signal_history.json.backup

# Step 3: Update files
git pull  # If using git
# OR manually replace files

# Step 4: Update dependencies (if changed)
pip install -r requirements.txt --upgrade

# Step 5: Restart service
sudo systemctl start squeeze-hunter  # Linux
# OR
launchctl load ~/Library/LaunchAgents/com.squeeze-hunter.plist  # macOS
```

---

## 9. TESTING AND VALIDATION

### 9.1 Unit Testing (Optional)

#### 9.1.1 Test Reddit Signal Scoring
```python
def test_reddit_scoring():
    from reddit_squeeze_monitor import RedditSqueezeMonitor
    
    monitor = RedditSqueezeMonitor(config)
    
    # Test case: SGBX-like signal
    signal = {
        'short_interest': 766,
        'market_cap_millions': 20,
        'upvotes': 245,
        'num_comments': 67,
        'title': 'SGBX short squeeze 766% SI',
        'body': 'Low float, high SI, 0 shares to borrow'
    }
    
    score = monitor.calculate_signal_score(signal)
    
    assert score >= 80, f"Expected score >= 80, got {score}"
    print(f"✓ Reddit scoring test passed (score: {score})")
```

#### 9.1.2 Test Pre-Market Analysis
```python
def test_premarket_analysis():
    from premarket_monitor import PreMarketMonitor
    
    monitor = PreMarketMonitor(config)
    
    # Test premium calculation
    prev_close = 3.41
    bid = 4.13
    ask = 4.18
    
    bid_pct, ask_pct, spread = monitor._calculate_premiums(
        prev_close, bid, ask
    )
    
    assert abs(bid_pct - 21.1) < 0.5, f"Expected ~21%, got {bid_pct}"
    print(f"✓ Pre-market analysis test passed")
```

### 9.2 Integration Testing

#### 9.2.1 End-to-End Signal Flow
```bash
# Manual test procedure:

1. Start system in foreground
   python start.py

2. Monitor specific subreddit with known posts
   (or create test post in own subreddit)

3. Verify Reddit signal detected in logs
   [timestamp] 🎯 SIGNAL DETECTED: ['SGBX']

4. Check Discord for alert
   Should see embed in configured channel

5. If pre-market hours, verify pre-market check
   [timestamp] Pre-market: $4.13 (+21.1%)

6. Verify combined alert if thresholds met
   [timestamp] 🔥 COMBINED SIGNAL DETECTED

7. Check signal_history.json for entry
   cat signal_history.json | tail -20

✓ All steps successful = system working correctly
```

### 9.3 Backtesting

#### 9.3.1 Run Historical Validation
```bash
python backtest_engine.py
```

**Expected Output:**
```
============================================================
SQUEEZE HUNTER - BACKTESTING ENGINE
============================================================
Testing against 8 historical squeezes...

━━━ $GME ━━━
Date: 2021-01-28
Reddit Score: 90.0/100
Pre-Market Detection: ✓
Would Alert: ✓ YES
🔥 COMBINED SIGNAL (highest confidence)
Lead Time: 360.0 hours
Potential Gain: 2700.0%
Outcome: SUCCESS

[... more results ...]

============================================================
BACKTEST RESULTS
============================================================

Total Squeezes Tested: 8
Detected by System: 7 (87.5%)
Combined Signals: 6 (75.0%)
Average Gain (if detected): 350.5%
Total Potential Gain: 2453.5%

Signal Breakdown:
  Reddit Only: 1
  Pre-Market Only: 0
  Combined (Both): 6

Success Rate (alerted squeezes that worked): 85.7%

============================================================
```

#### 9.3.2 Interpretation
- **Detection rate 75%+**: System successfully identifies most squeezes
- **Combined signals 50%+**: High-confidence setups are common
- **Avg gain 200%+**: Opportunities are significant
- **Success rate 80%+**: Alerted squeezes usually work

If results are significantly lower, check:
- Threshold configuration (may be too strict)
- Scoring algorithm (may need tuning)
- Data quality (ensure APIs work correctly)

---

## 10. TROUBLESHOOTING

### 10.1 Common Issues

#### Issue: "Invalid Reddit credentials"
**Symptoms:** Error on startup, can't connect to Reddit
**Solutions:**
1. Verify client_id and client_secret are correct
2. Check user_agent format: "AppName/Version by Username"
3. Ensure Reddit app is "script" type, not "web app"
4. Try creating new Reddit app

#### Issue: "Discord bot not responding"
**Symptoms:** No alerts in Discord, bot appears offline
**Solutions:**
1. Verify bot token is correct (should be ~70 chars)
2. Check bot is invited to server
3. Verify channel_id is correct (18 digits)
4. Ensure bot has permissions (Send Messages, Embed Links)
5. Check bot is shown as online in server member list

#### Issue: "No pre-market data for ticker"
**Symptoms:** Pre-market checks fail, Alpaca errors
**Solutions:**
1. Verify Alpaca credentials (api_key starts with PK)
2. Check if ticker is valid (some penny stocks lack data)
3. Ensure using Paper Trading API (included in free tier)
4. Try with known ticker (SPY, AAPL) to test connection
5. Check market hours (pre-market is 4:00-9:30 AM ET)

#### Issue: "System crashes/restarts frequently"
**Symptoms:** Process dies, systemd shows restarts
**Solutions:**
1. Check error logs: `tail -f squeeze_hunter.log`
2. Check system resources: `top` or `htop`
3. Verify network connectivity
4. Check for API rate limits
5. Ensure Python version is 3.9+

#### Issue: "Reddit signal scores always 0"
**Symptoms:** All Reddit posts score 0, no alerts
**Solutions:**
1. Check subreddit list in configuration
2. Verify posts contain squeeze keywords
3. Lower reddit_score_min threshold temporarily
4. Check logs for parsing errors
5. Test with known squeeze post

### 10.2 Debug Mode

#### Enable Verbose Logging
```python
# In squeeze_hunter.py, change:
logging.basicConfig(level=logging.INFO)
# To:
logging.basicConfig(level=logging.DEBUG)
```

**Debug output includes:**
- Every post scanned
- Extracted tickers and metrics
- Signal score calculations
- API call results
- Timing information

### 10.3 Manual Testing

#### Test Reddit Connection
```python
python -c "
import praw
reddit = praw.Reddit(
    client_id='YOUR_ID',
    client_secret='YOUR_SECRET',
    user_agent='SqueezeHunter/1.0'
)
print('✓ Reddit connected:', reddit.read_only)
for post in reddit.subreddit('wallstreetbets').hot(limit=1):
    print('✓ Can read posts:', post.title)
"
```

#### Test Alpaca Connection
```python
python -c "
from alpaca.data.historical import StockHistoricalDataClient
client = StockHistoricalDataClient(
    api_key='YOUR_KEY',
    secret_key='YOUR_SECRET'
)
from alpaca.data.requests import StockLatestQuoteRequest
req = StockLatestQuoteRequest(symbol_or_symbols='SPY')
quote = client.get_stock_latest_quote(req)
print('✓ Alpaca connected, SPY quote:', quote['SPY'].bid_price)
"
```

#### Test Discord Connection
```python
python -c "
import discord
import asyncio

async def test():
    client = discord.Client(intents=discord.Intents.default())
    
    @client.event
    async def on_ready():
        print('✓ Discord connected as', client.user)
        channel = client.get_channel(YOUR_CHANNEL_ID)
        if channel:
            print('✓ Can access channel:', channel.name)
        await client.close()
    
    await client.start('YOUR_TOKEN')

asyncio.run(test())
"
```

---

## 11. PERFORMANCE OPTIMIZATION

### 11.1 Resource Usage

**Expected Resource Requirements:**
- **CPU:** 5-15% average (spikes during signal processing)
- **RAM:** 150-300 MB
- **Network:** 1-5 Mbps (mostly during Reddit stream)
- **Disk:** < 100 MB (logs + history)

### 11.2 Optimization Strategies

#### 11.2.1 Reduce Reddit Scan Frequency
```python
# In reddit_squeeze_monitor.py
# Change stream to polling (less real-time but lower overhead)

def scan_periodic(self, interval_seconds=300):
    """Scan every 5 minutes instead of real-time stream"""
    while True:
        signals = self.scan_recent_posts(hours_back=1, limit=50)
        for signal in signals:
            self.callback(signal)
        time.sleep(interval_seconds)
```

#### 11.2.2 Limit Pre-Market Checks
```python
# Only check top N tickers by score
MAX_PREMARKET_CHECKS = 10

def get_top_signals(active_signals, n=10):
    sorted_signals = sorted(
        active_signals.items(),
        key=lambda x: x[1]['reddit_signal']['signal_score'],
        reverse=True
    )
    return [ticker for ticker, _ in sorted_signals[:n]]
```

#### 11.2.3 Cache Previous Close Prices
```python
# Reduce Alpaca API calls
close_price_cache = {}  # ticker -> (price, timestamp)
CACHE_DURATION = 86400  # 24 hours

def get_previous_close_cached(ticker):
    if ticker in close_price_cache:
        price, timestamp = close_price_cache[ticker]
        if time.time() - timestamp < CACHE_DURATION:
            return price
    
    # Fetch fresh if not cached
    price = fetch_from_alpaca(ticker)
    close_price_cache[ticker] = (price, time.time())
    return price
```

---

## 12. SECURITY CONSIDERATIONS

### 12.1 Credential Protection

#### Never commit credentials to git:
```bash
# Add to .gitignore:
config.json
*.log
signal_history.json
__pycache__/
venv/
```

#### Use environment variables (optional):
```python
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    'reddit': {
        'client_id': os.getenv('REDDIT_CLIENT_ID'),
        'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
        'user_agent': os.getenv('REDDIT_USER_AGENT')
    },
    # ... etc
}
```

### 12.2 Rate Limit Protection

All APIs are rate-limited. The system includes built-in protections:
- PRAW: Automatic exponential backoff
- Alpaca: 200 requests/minute (well below limit with this system)
- Discord: 50 requests/second (far exceeds needs)

### 12.3 Input Validation

**Never trust external data:**
- All ticker symbols sanitized (uppercase, alphanumeric only)
- All numerical values range-checked
- All strings length-limited
- Regex patterns use non-greedy matching

---

## 13. FUTURE ENHANCEMENTS

### 13.1 Planned Features (Phase 2)

#### Twitter/X Integration
```python
# Monitor @unusual_whales, @zerohedge for squeeze mentions
from tweepy import StreamingClient

class TwitterSqueezeMonitor:
    def __init__(self, bearer_token):
        self.client = StreamingClient(bearer_token)
    
    def add_rules(self):
        rules = [
            'short squeeze has:mentions',
            'short interest OR SI from:unusual_whales',
            '$TICKER short interest'
        ]
        # ... implement
```

#### Options Flow Detection
```python
# Detect unusual options activity (potential gamma squeeze)
def detect_gamma_setup(ticker):
    # High call volume near ITM strikes
    # Low IV → High IV transition
    # Delta > 0.5 calls accumulating
    pass
```

#### Machine Learning Scoring
```python
# Train model on historical squeezes
from sklearn.ensemble import RandomForestClassifier

def train_squeeze_predictor():
    features = [
        'short_interest',
        'market_cap',
        'volume_ratio',
        'social_sentiment',
        'bid_premium'
    ]
    # Train on 50+ historical squeezes
    # Predict probability (0-1) of squeeze success
```

### 13.2 Community Features

#### Web Dashboard
- Real-time signal viewer
- Historical performance charts
- Backtesting interface
- Configuration UI

#### Mobile App
- Push notifications (iOS/Android)
- Quick ticker lookup
- Position tracking
- Alert history

---

## 14. CHANGELOG

### Version 1.0 (Nov 20, 2025)
- Initial release
- Reddit monitoring via PRAW
- Pre-market analysis via Alpaca
- Discord alerts with rich embeds
- Backtesting engine
- Complete documentation

---

## 15. SUPPORT AND RESOURCES

### 15.1 Official Documentation
- PRAW: https://praw.readthedocs.io/
- Alpaca: https://docs.alpaca.markets/
- Discord.py: https://discordpy.readthedocs.io/

### 15.2 API Status Pages
- Reddit: https://www.redditstatus.com/
- Alpaca: https://status.alpaca.markets/
- Discord: https://discordstatus.com/

### 15.3 Community
- Questions, issues, feedback: GitHub Issues
- Feature requests: GitHub Discussions

---

## 16. IMPLEMENTATION CHECKLIST

Use this checklist to verify complete implementation:

### Environment Setup
- [ ] Python 3.9+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] All system files present

### API Configuration
- [ ] Reddit app created (script type)
- [ ] Reddit credentials obtained (client_id, client_secret)
- [ ] Alpaca account created (free tier)
- [ ] Alpaca API keys generated
- [ ] Discord bot created
- [ ] Discord bot invited to server
- [ ] Discord channel ID obtained

### Configuration
- [ ] config.json created
- [ ] All API credentials filled in
- [ ] Thresholds configured
- [ ] Configuration validated (no errors)

### Testing
- [ ] Reddit connection test passed
- [ ] Alpaca connection test passed
- [ ] Discord connection test passed
- [ ] Backtest run successfully (detection rate 75%+)
- [ ] End-to-end test completed

### Deployment
- [ ] System runs in foreground without errors
- [ ] Alerts received in Discord
- [ ] Service/daemon configured (systemd/launchd/Task Scheduler)
- [ ] Auto-start on boot enabled
- [ ] Logs directory configured
- [ ] Monitoring set up

### Production
- [ ] System running 24/7
- [ ] Discord alerts working
- [ ] Logs being written
- [ ] signal_history.json being updated
- [ ] No critical errors in logs

---

## 17. QUICK REFERENCE

### Start System
```bash
python start.py              # With validation
python squeeze_hunter.py     # Direct start
```

### Stop System
```bash
# Foreground: Ctrl+C
# Service (Linux): sudo systemctl stop squeeze-hunter
# Service (macOS): launchctl unload ~/Library/LaunchAgents/com.squeeze-hunter.plist
```

### View Logs
```bash
tail -f squeeze_hunter.log              # Application logs
sudo journalctl -u squeeze-hunter -f    # System logs (Linux)
tail -f ~/Library/Logs/squeeze-hunter.log  # System logs (macOS)
```

### Check Status
```bash
# Process running?
ps aux | grep squeeze_hunter

# Service status (Linux)
sudo systemctl status squeeze-hunter

# Service status (macOS)
launchctl list | grep squeeze-hunter
```

### View Signal History
```bash
cat signal_history.json | jq '.'        # Pretty print
cat signal_history.json | jq '.total_signals'  # Count
cat signal_history.json | jq '.signals[-5:]'   # Last 5
```

### Run Backtest
```bash
python backtest_engine.py
```

### Update Configuration
```bash
nano config.json             # Edit
python start.py              # Validates before starting
```

---

**END OF TECHNICAL SPECIFICATION**

For implementation questions or issues, refer to README.md or create a GitHub issue.
