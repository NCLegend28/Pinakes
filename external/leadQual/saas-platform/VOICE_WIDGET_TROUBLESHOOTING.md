# Voice Widget Troubleshooting Checklist

## Problem: Failed to Start Conversation

Use this checklist to diagnose and fix voice widget issues systematically.

---

## 1. Check Browser Console

### What to Look For
```
✅ Good: "✓ Recording started with auto-silence detection"
❌ Bad: "Failed to start conversation"
❌ Bad: "No conversation ID available"
❌ Bad: "Failed to start recording: [error]"
```

### Action
Open browser console (F12) and look for errors.

---

## 2. API Routes Exist

### Check These Endpoints

#### Start Conversation
```bash
# Test: POST /api/v1/chat/start
curl -X POST http://localhost:3002/api/v1/chat/start \
  -H "Content-Type: application/json" \
  -d '{"tenant_slug":"demo","channel":"voice"}'
```

**Expected**: `{ "conversation_id": "uuid", "message": "..." }`
**If 404**: Route doesn't exist
**If 500**: Database or logic error

#### Send Message
```bash
# Test: POST /api/v1/chat/message
curl -X POST http://localhost:3002/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"tenant_slug":"demo","conversation_id":"test-id","message":"Hello"}'
```

**Expected**: `{ "message": "response text" }`

#### STT (Speech-to-Text)
```bash
# Test: POST /api/voice/stt
curl -X POST http://localhost:3002/api/voice/stt \
  -H "Content-Type: application/json" \
  -d '{"audio":"base64data","config":{"model":"nova-2"}}'
```

**Expected**: `{ "transcript": "text" }`

#### TTS (Text-to-Speech)
```bash
# Test: POST /api/voice/tts
curl -X POST http://localhost:3002/api/voice/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello","config":{}}'
```

**Expected**: `{ "audio": "base64data" }`

---

## 3. Environment Variables Set

### Required Variables

```env
# Check .env.local has these:

# Deepgram (for voice)
DEEPGRAM_API_KEY=xxxxx

# Ollama (for AI)
OLLAMA_BASE_URL=http://localhost:11434/v1
# or cloud URL

# Database
DATABASE_URL=postgresql://...
# or Supabase URL
NEXT_PUBLIC_SUPABASE_URL=https://...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
```

### Test
```bash
# In your project directory
cat .env.local | grep -E "(DEEPGRAM|OLLAMA|DATABASE|SUPABASE)"
```

---

## 4. Database Connected

### Test Connection
```bash
psql $DATABASE_URL -c "SELECT COUNT(*) FROM tenants;"
```

**Expected**: Returns a number (even if 0)
**If error**: Database not accessible

### Check Tables Exist
```bash
psql $DATABASE_URL -c "\dt"
```

**Should see**:
- tenants
- users
- agent_configs
- conversations
- messages
- industry_templates

---

## 5. Tenant Exists

### Check in Database
```bash
psql $DATABASE_URL -c "SELECT slug, name FROM tenants;"
```

**If empty**: No tenants exist
**If "demo" missing**: Widget using wrong slug

### Create Test Tenant (if needed)
```sql
INSERT INTO tenants (name, slug, industry, plan, status)
VALUES ('Demo Company', 'demo', 'real_estate', 'starter', 'active');
```

---

## 6. Agent Configs Exist

### Check Guard Agent
```bash
psql $DATABASE_URL -c "
SELECT tenant_id, agent_type, provider, model
FROM agent_configs
WHERE agent_type = 'guard';
"
```

**Expected**: At least one guard agent
**If empty**: No agent configs set up

### Create from Templates (if needed)
```sql
-- Copy from industry templates to agent_configs
INSERT INTO agent_configs (
  tenant_id, agent_type, name, provider, model,
  temperature, system_instructions
)
SELECT
  (SELECT id FROM tenants WHERE slug = 'demo'),
  agent_type, name, default_provider, default_model,
  default_temperature, system_instructions
FROM industry_templates
WHERE industry = 'real_estate';
```

---

## 7. Conversation API Working

### Test Manually in Browser
1. Open DevTools → Network tab
2. Try starting conversation
3. Look for `/api/v1/chat/start` request
4. Check response

**Good Response:**
```json
{
  "conversation_id": "uuid-here",
  "message": "greeting text"
}
```

**Bad Responses:**
```json
// 404: Route not found
// 500: Server error
{ "error": "message" }
```

---

## 8. Voice Widget Props Correct

### Check Component Usage
```tsx
<VoiceWidget
  tenantSlug="demo"  // ← Must match database tenant.slug
  position="bottom-right"
  primaryColor="#3b82f6"
  greeting="Optional greeting"
/>
```

**Common Issues:**
- `tenantSlug` doesn't match database
- Missing required props
- Component not imported correctly

---

## 9. Microphone Permission

### Browser Permission Required
- Chrome: Shows popup on first use
- Firefox: Shows icon in address bar
- Safari: Asks permission

**If denied:**
1. Click lock icon in address bar
2. Reset permissions
3. Reload page

---

## 10. HTTPS Required (Production)

### Local Development
- `http://localhost:3002` ✅ Works
- `http://127.0.0.1:3002` ✅ Works

### Production
- `https://yourdomain.com` ✅ Required
- `http://yourdomain.com` ❌ Won't work

**Why**: Browsers block microphone on HTTP (except localhost)

---

## Common Error Messages & Fixes

### "Failed to start conversation"
```
Causes:
1. API route returns error
2. Tenant doesn't exist
3. Database not connected

Fix:
- Check console for specific error
- Test API route with curl
- Verify tenant exists
```

### "No conversation ID available"
```
Causes:
1. Start conversation didn't return ID
2. ID not stored in state
3. Race condition

Fix:
- Check /api/v1/chat/start response
- Verify conversationIdRef.current is set
- Add logging to handleToggleVoice
```

### "Failed to start recording"
```
Causes:
1. Microphone permission denied
2. No microphone available
3. Already recording

Fix:
- Check browser permissions
- Test mic in another app
- Reload page
```

### "STT failed: 401"
```
Causes:
1. DEEPGRAM_API_KEY missing
2. Invalid API key
3. Quota exceeded

Fix:
- Check .env.local has key
- Verify key is valid
- Check Deepgram dashboard
```

### "TTS failed: 500"
```
Causes:
1. Deepgram API error
2. Invalid voice ID
3. Text too long

Fix:
- Check API response
- Use default voice
- Limit text length
```

---

## Debug Mode

### Add Verbose Logging

In `VoiceWidget.tsx`:
```tsx
const handleToggleVoice = async () => {
  console.log('[Widget] Toggle voice called');
  console.log('[Widget] isActive:', isActive);
  console.log('[Widget] voiceClientRef:', voiceClientRef.current);

  if (!voiceClientRef.current) {
    console.error('[Widget] Voice client not initialized!');
    return;
  }

  // ... rest of function
};
```

In `browser-voice-client.ts`:
```typescript
async startRecording(): Promise<void> {
  console.log('[Client] startRecording called');
  try {
    console.log('[Client] Requesting media...');
    const stream = await navigator.mediaDevices.getUserMedia(...);
    console.log('[Client] Media stream obtained');
    // ... rest
  } catch (error) {
    console.error('[Client] Recording failed:', error);
    throw error;
  }
}
```

---

## Quick Diagnosis Script

Run this in browser console:

```javascript
// Check if widget is loaded
console.log('Widget loaded:', !!window.VoiceWidget);

// Check environment
console.log('Origin:', window.location.origin);
console.log('HTTPS:', window.location.protocol === 'https:');

// Test API
fetch('/api/v1/chat/start', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({tenant_slug: 'demo', channel: 'voice'})
})
.then(r => r.json())
.then(d => console.log('API Test:', d))
.catch(e => console.error('API Error:', e));

// Check mic access
navigator.mediaDevices.getUserMedia({audio: true})
  .then(() => console.log('Mic: OK'))
  .catch(e => console.error('Mic:', e.message));
```

---

## Step-by-Step Fix Process

1. **Open browser console** (F12)
2. **Try to start conversation** (click phone button)
3. **Read error message** in console
4. **Find error in this checklist** above
5. **Apply fix** from that section
6. **Reload page and test again**

---

## Still Not Working?

### Check These Files Exist
```
app/api/v1/chat/start/route.ts
app/api/v1/chat/message/route.ts
app/api/voice/stt/route.ts
app/api/voice/tts/route.ts
components/VoiceWidget.tsx
lib/voice/browser-voice-client.ts
```

### Verify Imports
```bash
# Check for TypeScript errors
npm run type-check

# Check for build errors
npm run build
```

### Last Resort
```bash
# Kill dev server
# Clear .next cache
rm -rf .next

# Restart
npm run dev
```

---

## Success Indicators

When working correctly, console shows:
```
✓ Recording started with auto-silence detection
[Audio] Level: 15.3, Threshold: 15, HasAudio: true
[Audio] Speech detected, starting silence timer
Silence detected, auto-stopping recording
[Audio Processing] Blob size: 45032 bytes, type: audio/webm
[STT Response] { transcript: 'Hello', confidence: 0.98 }
[Debounce] Received transcript: Hello
[Debounce] Sending combined message: Hello
```

---

## Status
Use this checklist whenever voice widget fails. Work through each section systematically.
