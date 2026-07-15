# Voice Integration Architecture

## Overview
The voice integration uses a **server-side proxy architecture** to avoid webpack bundling issues with Node.js modules in browser code.

## Architecture

```
Browser (VoiceWidget)
    ↓
BrowserVoiceClient (HTTP fetch)
    ↓
API Routes (/api/voice/stt, /api/voice/tts)
    ↓
External Services (Deepgram, ElevenLabs)
```

## Components

### 1. Browser-Side (`lib/voice/browser-voice-client.ts`)
- **No SDK imports** - Pure browser code
- Uses Web APIs: MediaRecorder, AudioContext
- Communicates with backend via HTTP fetch
- Handles:
  - Microphone recording (WebM format)
  - Audio playback
  - Base64 encoding/decoding

### 2. Server-Side Proxy APIs

#### STT Proxy (`app/api/voice/stt/route.ts`)
- Receives base64 audio from browser
- Calls Deepgram API with pre-recorded transcription
- Returns transcript + confidence score
- **Cost**: ~$0.0043/min (Deepgram Nova-2)

#### TTS Proxy (`app/api/voice/tts/route.ts`)
- Receives text from browser
- Calls ElevenLabs API with Turbo v2.5 model
- Returns base64 audio
- **Cost**: ~$0.00003/char (ElevenLabs Turbo v2.5)

### 3. UI Component (`components/VoiceWidget.tsx`)
- Floating phone button interface
- Real-time transcript display
- Conversation history
- State management (idle/listening/processing/speaking)
- Mute/unmute controls

## Configuration

### Environment Variables
```env
# Required server-side keys
DEEPGRAM_API_KEY=your-deepgram-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key

# Optional: Custom voice ID (default: Rachel)
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```

### Usage Example
```tsx
import { VoiceWidget } from '@/components/VoiceWidget';

<VoiceWidget
  tenantSlug="acme-real-estate"
  position="bottom-right"
  primaryColor="#3b82f6"
  greeting="Hi! How can I help you today?"
/>
```

## Flow

### Voice Conversation Flow
1. User clicks phone button → Creates conversation via `/api/v1/chat/start`
2. User speaks → Browser records audio (WebM)
3. User stops speaking → Audio sent to `/api/voice/stt`
4. Deepgram transcribes → Transcript returned to browser
5. Transcript sent to `/api/v1/chat` → AI processes message
6. AI response sent to `/api/voice/tts`
7. ElevenLabs generates speech → Audio returned to browser
8. Browser plays audio → Resumes listening

### Key Features
- **Continuous listening**: Auto-resumes after AI speaks
- **Mute control**: Pause/resume recording
- **Error recovery**: Auto-retry after failures
- **Conversation persistence**: All messages saved to database

## Cost Comparison

### Our Stack (Deepgram + ElevenLabs)
- STT: $0.0043/min (Deepgram Nova-2)
- TTS: ~$0.00003/char (~$0.015/min at 500 chars/min)
- **Total**: ~$0.02/min

### OpenAI Realtime API
- **Total**: ~$0.06/min (text input) or ~$0.24/min (audio input)

**Savings**: 67-92% cheaper than OpenAI Realtime API

## Security

### API Key Protection
- API keys never exposed to browser
- All external API calls happen server-side
- Rate limiting can be added to proxy routes

### Multi-Tenant Isolation
- Tenant identified by slug
- RLS policies enforce data isolation
- Each conversation tagged with tenant_id

## Testing

Visit `/voice-test` to test the integration:
1. Click phone button
2. Allow microphone access
3. Start speaking
4. Watch real-time transcription
5. Hear AI voice response

## Troubleshooting

### No audio playback
- Check browser permissions for microphone
- Ensure AudioContext is allowed (may need user interaction first)

### Transcription errors
- Verify `DEEPGRAM_API_KEY` is set
- Check network connectivity
- Review browser console for errors

### TTS errors
- Verify `ELEVENLABS_API_KEY` is set
- Check voice ID is valid
- Ensure text is not empty

## Future Enhancements

- [ ] Add voice activity detection (VAD) for better silence handling
- [ ] Implement streaming TTS for lower latency
- [ ] Add support for multiple languages
- [ ] Voice biometrics for authentication
- [ ] Call recording and playback
- [ ] Real-time sentiment analysis
- [ ] Custom wake words
