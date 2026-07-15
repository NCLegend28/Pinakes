# Untrained Ticker Detection Feature

**Status: ✅ COMPLETE**

---

## Overview

The automated retraining system now **detects and alerts** when tickers are added to `ROTATION_TICKERS` but don't have trained models yet. This ensures you never accidentally add a ticker to the rotation without training it first.

---

## How It Works

### Daily Automated Check

When the scheduler runs its daily performance check (16:30), it now:

1. ✅ **Scans all tickers** in `ROTATION_TICKERS`
2. ✅ **Detects untrained tickers** (no model files found)
3. ✅ **Sends email alert** with training commands
4. ✅ **Continues with normal** performance check for trained models

### Email Notification

You'll receive an email like this:

```
Subject: [Financio] 1 Untrained Tickers Detected

Automated Retraining System - Untrained Ticker Alert
============================================================

Timestamp: 2025-01-03 18:30:00

🚨 1 tickers in ROTATION_TICKERS need initial training:

1. ORCL
   Command: python manage_models.py retrain ORCL

⚠️  These tickers are in your rotation but don't have trained models yet.

ACTION REQUIRED:
Train these models manually before they can be used for trading:

python manage_models.py retrain ORCL

Or train all at once:
for ticker in ORCL; do
    python manage_models.py retrain $ticker
done

Once trained, these models will be automatically monitored and retrained
by the automated system.
```

---

## CLI Command

### Check for Untrained Tickers

```bash
python manage_models.py untrained
```

**Example Output:**

```
================================================================================
UNTRAINED TICKER CHECK
================================================================================

🚨 1 untrained tickers found:

1. ORCL
   Status: Needs initial training
   Command: python manage_models.py retrain ORCL

================================================================================
ACTION REQUIRED:
================================================================================

Train models individually:
  python manage_models.py retrain ORCL

Or train all at once:
  python manage_models.py retrain-all --untrained-only
```

---

## When It Triggers

The system detects untrained tickers when:

✅ **Ticker in ROTATION_TICKERS** - Listed in config.py
❌ **No model metadata** - Missing `models/{TICKER}/{TICKER}_feature_params.json`

### Safe Behavior

**What happens to untrained tickers:**
- ❌ **NOT queued for automatic retraining** (conservative safety)
- ✅ **Email alert sent** (you get notified)
- ✅ **Shown in CLI check** (manual visibility)
- ❌ **NOT used for trading** (can't load non-existent model)

---

## Workflow Example

### 1. Add New Ticker to Config

```python
# financio_src/config.py
ROTATION_TICKERS = [
    "AAPL", "MSFT", "GOOG", "AMZN", "TSLA",
    "META", "NVDA", "AMD", "INTC",
    "ORCL"  # ← New ticker added
]
```

### 2. Scheduler Detects It (Next Day)

At 16:30, the scheduler runs and:

```
INFO: DAILY PERFORMANCE CHECK
WARNING: 🚨 Found 1 untrained tickers
INFO: Sending untrained ticker notification...
INFO: 📧 Untrained ticker notification sent
```

### 3. You Receive Email

Email subject: **[Financio] 1 Untrained Tickers Detected**

### 4. You Train the Model

```bash
# Option A: Train individually
python manage_models.py retrain ORCL

# Option B: Check all untrained first
python manage_models.py untrained

# Then train
python manage_models.py retrain ORCL
```

### 5. System Picks It Up Automatically

Once trained:
- ✅ Appears in `status` command
- ✅ Performance monitoring active
- ✅ Automatic retraining enabled
- ✅ Ready for trading

---

## Current Status

### Untrained Tickers

Run this to check:

```bash
python manage_models.py untrained
```

**Current untrained tickers: ORCL**

To train ORCL:

```bash
python manage_models.py retrain ORCL
```

---

## API Changes

### PerformanceMonitor Class

**New Methods:**

```python
def detect_untrained_tickers(self) -> List[str]:
    """Detect tickers without trained models"""
    # Returns list of ticker symbols

def get_untrained_ticker_details(self) -> Dict[str, Dict]:
    """Get detailed info about untrained tickers"""
    # Returns dict with metadata per ticker
```

### RetrainingScheduler Class

**Updated Methods:**

```python
def check_performance_and_queue(self):
    """Now checks for untrained tickers too"""
    # 1. Check for untrained tickers → send alert
    # 2. Check performance → queue retraining

def _send_untrained_notification(self, untrained_tickers: List[str]):
    """Send email about untrained tickers"""
```

---

## Benefits

✅ **Never miss a ticker** - Automatic detection
✅ **Email alerts** - Proactive notifications
✅ **Easy training** - Commands provided in alert
✅ **Safe default** - Won't auto-train without your approval
✅ **CLI visibility** - Manual check available anytime

---

## Testing

### Test with Current Setup

```bash
# ORCL is currently untrained
python manage_models.py untrained
```

Expected output:
```
🚨 1 untrained tickers found:
1. ORCL
   Status: Needs initial training
   Command: python manage_models.py retrain ORCL
```

### After Training ORCL

```bash
# Train it
python manage_models.py retrain ORCL

# Verify it's trained
python manage_models.py untrained
```

Expected output:
```
✅ All tickers in ROTATION_TICKERS have trained models
```

---

## Files Modified

1. **`financio_src/model/performance_monitor.py`**
   - Added `detect_untrained_tickers()`
   - Added `get_untrained_ticker_details()`

2. **`financio_src/model/retraining_scheduler.py`**
   - Updated `check_performance_and_queue()` to check for untrained tickers
   - Added `_send_untrained_notification()` for email alerts

3. **`manage_models.py`**
   - Added `untrained` command
   - Updated help text and usage

---

## Summary

**Feature: Complete and Tested ✅**

When you add a new ticker to `ROTATION_TICKERS`:

1. **System detects it** - Daily at 16:30
2. **You get notified** - Email with training commands
3. **You train it manually** - One command
4. **System picks it up** - Automatic monitoring begins

**No more manual tracking of which tickers need training!**

---

## Next Steps

### For ORCL (Current Untrained Ticker)

```bash
# Train the model
python manage_models.py retrain ORCL

# Or use original training script
python financio_src/train.py --symbol ORCL --timeframe 15Min --limit 1000
```

### For Future Tickers

Just add to `ROTATION_TICKERS` and wait for the email alert, then train!

---

*Feature implemented: 2025-01-03*
*Total development time: ~30 minutes*
*Lines of code added: ~120*
