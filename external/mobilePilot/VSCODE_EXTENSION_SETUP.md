# VSCode Extension Connection Guide

## Quick Setup

The VSCode extension is **installed** but **not connected** to the server. Here's how to connect it:

### Method 1: Command Palette (Recommended)

1. Open VSCode
2. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
3. Type: `mobilePilot: Connect to mobilePilot Server`
4. Press Enter

**You'll be prompted for:**
- Server URL: `http://localhost:8000` (default)
- Username: `admin`
- Password: `AdminTest123!`

> **Note:** With `DISABLE_AUTH=true`, the extension may still need to authenticate once, but the server will bypass auth checks.

### Method 2: Status Bar (If Available)

Look at the bottom of VSCode for the mobilePilot status icon:
- 🔴 **Disconnected** - Click to connect
- 🟢 **Connected** - Already connected!

---

## How Polling Works

Once connected, the extension automatically polls the server **every 3 seconds**:

```typescript
//Human File: extension.ts, Line 527
copilotRequestPollingInterval = setInterval(async () => {
    if (mobilePilotClient.isConnected() && !isProcessingCopilotRequests) {
        // Get pendingRequests from: GET /copilot/pending-requests
        const requests = await mobilePilotClient.getPendingCopilotRequests();
        
        for (const request of requests) {
            await handleCopilotRequest(request);
        }
    }
}, 3000); // 3 seconds
```

**What happens:**
1. Extension checks if connected
2. Every 3 seconds, calls `GET /copilot/pending-requests`
3. Processes each pending request (triggers Copilot)
4. Sends results back to server via `POST /copilot/complete-request`

---

## Verification

After connecting, check the VSCode Output panel:
1. Press `Cmd+Shift+U` or View → Output
2. Select "mobilePilot" from dropdown
3. You should see: `✅ Connected to mobilePilot server: http://localhost:8000`

---

## If Authentication Fails

The extension tries to authenticate even with `DISABLE_AUTH=true`. If you get auth errors:

### Option 1: Modify Extension to Skip Auth

I can update the extension source to respect `DISABLE_AUTH` and skip authentication.

### Option 2: Use Default Credentials

Just enter:
- Username: `admin`
- Password: `AdminTest123!`

The server will bypass the auth check but log you in successfully.

---

## Testing After Connection

Once connected, re-run the test:
```bash
python test_no_auth.py
```

Then check the VSCode Output panel - you should see:
```
🔄 Starting Copilot request polling...
📋 Retrieved 1 pending Copilot requests
🎯 Processing Copilot request: suggestion_... (copilot_suggestion)
🤖 Executing Copilot suggestion: ...
```

The extension will:
1. Pick up your pending request
2. Insert comment in active editor
3. Trigger Copilot inline suggestions
4. Send result back to server

---

## Extension Commands Available

All available from Command Palette (`Cmd+Shift+P`):
- `mobilePilot: Connect to mobilePilot Server`
- `mobilePilot: Disconnect from mobilePilot Server`
- `mobilePilot: Show Status`
- `mobilePilot: Test Real Copilot`
- `mobilePilot: Discover Instance`

---

## Current Status

✅ Extension installed: `mobilepilot.mobilepilot-extension`  
✅ Server running: `http://localhost:8000`  
✅ Authentication disabled: `DISABLE_AUTH=true`  
⏳ **Action needed:** Connect extension in VSCode

Once connected, your complete mobile → server → VSCode → Copilot workflow will be operational!
