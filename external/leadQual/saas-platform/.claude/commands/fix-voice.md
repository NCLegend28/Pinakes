---
description: Apply the working voice integration fixes
---

# Voice Integration Fixes

This command documents the fixes that made voice integration work correctly.

## Key Fixes Applied

### 1. MediaRecorder - NO TIMESLICES
```typescript
// ❌ WRONG - causes corrupt audio
this.mediaRecorder.start(100); // timeslices

// ✅ CORRECT - collect all data on stop
this.mediaRecorder.start(); // no parameters
```

### 2. Manual Send Button (No Auto-Silence)
```typescript
// Disable auto-silence detection in browser-voice-client.ts
private resetSilenceTimer(): void {
  // Auto-silence disabled - use manual Send button instead
  return;
}
```

### 3. React State Closure Fix
```typescript
// ❌ WRONG - stale closure
const conversationIdRef = useRef<string | null>(null);
voiceClientRef.current = new BrowserVoiceClient({
  onTranscript: (text) => {
    handleTranscript(text); // captures old conversationId value
  },
});

// ✅ CORRECT - pass ref as parameter
voiceClientRef.current = new BrowserVoiceClient({
  onTranscript: (text) => {
    handleTranscript(text, conversationIdRef); // pass ref itself
  },
});

const handleTranscript = async (text: string, convIdRef: React.MutableRefObject<string | null>) => {
  const currentConversationId = convIdRef.current; // always fresh value
};
```

### 4. Update Both State AND Ref
```typescript
// When setting conversation ID, update BOTH
setConversationId(data.conversation_id); // for React re-renders
conversationIdRef.current = data.conversation_id; // for callbacks
```

### 5. Server-Side Proxy Architecture
- `/api/voice/stt` - Deepgram STT proxy (Node.js only)
- `/api/voice/tts` - ElevenLabs TTS proxy (Node.js only)
- `BrowserVoiceClient` - Zero SDK dependencies, pure browser APIs
- All API keys stay server-side, never exposed to browser

### 6. Minimum Audio Size Check
```typescript
if (audioBlob.size < 5000) {
  console.log('Audio too short, skipping transcription');
  return;
}
```

## Environment Variables Required
```env
DEEPGRAM_API_KEY=your-key
ELEVENLABS_API_KEY=your-key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```

## Files Involved
- `components/VoiceWidget.tsx` - Main UI component
- `lib/voice/browser-voice-client.ts` - Browser recording/playback
- `app/api/voice/stt/route.ts` - Server-side STT proxy
- `app/api/voice/tts/route.ts` - Server-side TTS proxy

## Common Errors & Solutions

**Error: "corrupt or unsupported data" from Deepgram**
- Solution: Remove timeslices from `mediaRecorder.start()`

**Error: "No conversation ID available"**
- Solution: Pass conversationIdRef as parameter to handleTranscript

**Error: "Module not found: Can't resolve 'node:child_process'"**
- Solution: Use server-side proxy architecture, don't import SDKs in browser code

**Audio files too small/empty**
- Solution: Add minimum size check (5KB+), user must speak for ~1 second
