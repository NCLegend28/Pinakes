# Authentication Bypass Configuration

## ✅ Changes Made

### 1. Added DISABLE_AUTH Configuration

**File: `.env`**
```bash
# Testing Configuration
DISABLE_AUTH=true  # Set to "false" to enable authentication (default: false)
```

**File: `main.py`**
- Added `DISABLE_AUTH` configuration variable (line 38)
- Modified `get_current_user()` function to bypass JWT validation when enabled
- Logs warning when authentication is disabled

### 2. Fixed VSCode Workspace Path

**Before:**
```bash
VSCODE_WORKSPACE_PATH=/path/to/your/workspace  # ❌ Hardcoded
```

**After:**
```bash
# Note: Workspace path is determined dynamically by the VSCode extension
VSCODE_EXTENSION_PORT=3000  # ✅ No hardcoded path
```

The workspace path is now automatically detected by the VSCode extension from the active workspace.

---

## Testing Without Authentication

### Method 1: Direct API Calls (No Token Needed)

```bash
# Trigger Copilot suggestion - NO AUTH HEADER REQUIRED
curl -X POST http://localhost:8000/copilot/trigger-suggestion \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a function to reverse a string",
    "trigger_type": "inline",
    "mode": "ask",
    "language": "python"
  }'
```

### Method 2: Use Test Script

```bash
python test_no_auth.py
```

This script tests all major endpoints without authentication.

---

## How Authentication Bypass Works

When `DISABLE_AUTH=true`:

1. **All API endpoints** that normally require authentication will work without JWT tokens
2. A default test user is used: `{"username": "test_user"}`
3. Server logs a warning: ⚠️ AUTHENTICATION DISABLED
4. You can make requests without the `Authorization: Bearer <token>` header

**Example Response when auth is disabled:**
```
INFO:mobilePilot:⚠️  AUTHENTICATION DISABLED - Using default user for testing
```

---

## Re-enabling Authentication

To turn authentication back on:

**Option 1: Edit `.env` file**
```bash
DISABLE_AUTH=false
```

**Option 2: Remove the line entirely**
```bash
# DISABLE_AUTH=true  # Commented out = authentication enabled
```

The server will auto-reload and require JWT tokens again.

---

## Current Test Results

✅ All tests passing with authentication disabled:

```
🧪 Testing mobilePilot API (Auth Disabled)
============================================================

1. Health Check (no auth required)
   Status: 200 ✅

2. Trigger Copilot Suggestion (auth disabled)
   Status: 200 ✅
   Request ID: suggestion_20260202_033458_377170

3. Check Pending Requests (auth disabled)
   Status: 200 ✅
   Pending requests: 1

4. Get Workspace Status (auth disabled)
   Status: 200 ✅

============================================================
✅ All tests complete! Authentication successfully bypassed.
```

---

## Security Note

> [!WARNING]
> **DISABLE_AUTH should ONLY be used for local testing!**
> 
> - Never deploy with `DISABLE_AUTH=true` in production
> - Anyone who can reach your server can make requests
> - No user tracking or access control
> - Re-enable authentication before deploying

---

## Quick Commands

```bash
# Test without auth
python test_no_auth.py

# Test with full workflow (still needs auth to be disabled)
python test_workflow.py

# View server logs
# (Check the terminal where you ran 'python start.py start')

# Re-enable auth
# Edit .env: DISABLE_AUTH=false
# Server will auto-reload
```
