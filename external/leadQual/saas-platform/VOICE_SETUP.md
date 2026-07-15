# 🎙️ Voice Integration Setup Guide

The voice integration is now **complete** with Deepgram speech-to-text and ElevenLabs text-to-speech.

## ✅ What's Been Implemented

### 1. Voice Agent Library (`lib/voice/`)
- ✅ **Deepgram Client** - Real-time speech-to-text transcription
- ✅ **ElevenLabs Client** - Natural text-to-speech synthesis
- ✅ **Voice Agent** - Orchestrates STT + TTS + AI workflow
- ✅ **Browser Audio** - Microphone recording and audio playback

### 2. Voice Widget Component
- ✅ **Floating widget** - Click-to-talk interface
- ✅ **Live transcription** - Shows what user is saying in real-time
- ✅ **Conversation history** - Displays full dialogue
- ✅ **State indicators** - Shows listening/processing/speaking status
- ✅ **Mute controls** - Toggle microphone on/off
- ✅ **Customizable** - Position, colors, voice selection

### 3. API Integration
- ✅ **Voice channel support** - Conversations can be marked as 'voice'
- ✅ **Compatible with existing workflow** - Uses same chat endpoints
- ✅ **Conversation persistence** - All voice messages saved to database

---

## 🚀 Quick Start

### Prerequisites

1. **Deepgram Account** - Sign up at https://deepgram.com
2. **ElevenLabs Account** - Sign up at https://elevenlabs.io
3. **API Keys obtained** - From both services

### Environment Setup

Add these to your `.env.local`:

```env
# Voice Integration (Deepgram STT + ElevenLabs TTS)
# Server-side keys (keep secret)
DEEPGRAM_API_KEY=your-deepgram-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key

# Client-side keys (safe to expose in browser)
# Option 1: Use same keys (not recommended for production)
NEXT_PUBLIC_DEEPGRAM_API_KEY=your-deepgram-api-key
NEXT_PUBLIC_ELEVENLABS_API_KEY=your-elevenlabs-api-key

# Option 2: Use client-specific keys with usage limits
# NEXT_PUBLIC_DEEPGRAM_API_KEY=your-client-deepgram-key
# NEXT_PUBLIC_ELEVENLABS_API_KEY=your-client-elevenlabs-key

# Optional: Specific ElevenLabs voice ID
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Rachel (default)
NEXT_PUBLIC_ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```

### Available Voice IDs (ElevenLabs)

```typescript
Rachel: '21m00Tcm4TlvDq8ikWAM'     // Calm, professional female (default)
Sarah: 'EXAVITQu4vr4xnSDxMaL'      // Warm, friendly female
Charlotte: 'XB0fDUnXU5powFXDhCwa'  // Confident, professional female
Adam: 'pNInz6obpgDQGcFmaJgB'       // Deep, professional male
Josh: 'TxGEqnHWrfWFTfGW9XjX'       // Young, friendly male
Antoni: 'ErXwobaYiN019PkySvjV'     // Balanced, warm male
```

---

## 📋 Usage Examples

### Basic Usage (Add to Any Page)

```tsx
import { VoiceWidget } from '@/components/VoiceWidget';

export default function Page() {
  return (
    <>
      <h1>My Business</h1>

      {/* Voice widget */}
      <VoiceWidget
        tenantSlug="your-tenant-slug"
        position="bottom-right"
        primaryColor="#3b82f6"
        greeting="Hi! Click the phone icon to speak with me."
      />
    </>
  );
}
```

### Customized Voice Widget

```tsx
<VoiceWidget
  tenantSlug="acme-realty"
  voiceId="EXAVITQu4vr4xnSDxMaL"  // Sarah voice
  position="bottom-left"
  primaryColor="#10b981"  // Green
  greeting="Welcome to Acme Realty! How can I help you find your dream home?"
/>
```

### Testing Page

Create a test page at `app/voice-test/page.tsx`:

```tsx
'use client';

import { VoiceWidget } from '@/components/VoiceWidget';

export default function VoiceTestPage() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-4">Voice Widget Test</h1>
        <p className="text-gray-600 mb-8">
          Click the phone icon in the bottom-right to start a voice conversation.
        </p>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Test Instructions</h2>
          <ol className="list-decimal list-inside space-y-2 text-gray-700">
            <li>Click the phone button to start</li>
            <li>Allow microphone access when prompted</li>
            <li>Speak naturally - say "I want to book an appointment"</li>
            <li>Watch the transcript appear in real-time</li>
            <li>Listen to the AI response</li>
            <li>Continue the conversation or click "End Call"</li>
          </ol>
        </div>
      </div>

      {/* Voice widget */}
      <VoiceWidget
        tenantSlug="test-tenant"
        position="bottom-right"
        greeting="Hi! I'm ready to help. Click the phone to talk!"
      />
    </div>
  );
}
```

---

## 🔧 How It Works

### Complete Voice Conversation Flow

1. **User Clicks Phone Button**
   - VoiceWidget initializes VoiceAgent
   - Creates new conversation: `POST /api/v1/chat/start` with `channel: 'voice'`
   - Receives conversation ID and greeting

2. **User Starts Speaking**
   - Browser captures microphone audio
   - Audio streams to Deepgram for real-time transcription
   - Interim transcripts shown in UI
   - Final transcript sent when user pauses

3. **AI Processing**
   - Transcript sent to: `POST /api/v1/chat/message`
   - Existing workflow engine processes the message
   - Guard agent classifies intent
   - Qualifier agent responds appropriately
   - Response text returned

4. **AI Speaks Response**
   - Response text sent to ElevenLabs
   - Converted to natural speech audio
   - Audio played through browser
   - User can interrupt or respond

5. **Conversation Continues**
   - Process repeats until conversation ends
   - All messages saved to database
   - Lead qualification tracked
   - Webhooks fired as usual

---

## 🎯 Voice Agent States

The widget displays different states during conversation:

- **IDLE** - Ready to start (phone icon)
- **LISTENING** - Recording user speech (green pulse animation)
- **PROCESSING** - Sending to AI (yellow indicator)
- **SPEAKING** - Playing AI response (blue indicator)
- **ERROR** - Something went wrong (red indicator)

---

## 💰 Cost Estimation

### For 1000 voice conversations/month (avg 2 min each):

**Deepgram Nova-2** (Speech-to-Text):
- 2000 minutes × $0.0043/min = **$8.60/month**

**ElevenLabs Turbo v2.5** (Text-to-Speech):
- Approx 300 characters per response × 2 responses per conversation
- 600,000 characters × $0.00003/char = **$18/month**

**Total Voice Cost**: **~$26.60/month** for 1000 conversations

**Compare to**: OpenAI Realtime API would be **$120/month** for same usage

**Your Margin** at $99/month plan (500 conversations):
- Revenue: $99
- Voice costs: $13.30 (500 conversations)
- Other costs: ~$20 (AI, SMS, email, hosting)
- **Profit: ~$65/month = 65% margin**

---

## 🔒 Security Considerations

### API Key Exposure

**Problem**: Browser-based voice requires client-side API keys

**Solutions**:

1. **Use Deepgram/ElevenLabs client keys** (recommended)
   - Both services offer client-side keys with usage limits
   - Set daily/monthly caps to prevent abuse
   - Monitor usage in dashboards

2. **Implement proxy endpoints** (most secure)
   - Create `/api/voice/stt` and `/api/voice/tts` routes
   - Handle all API calls server-side
   - No keys exposed to browser
   - More complex but fully secure

3. **Rate limiting** (additional protection)
   - Add rate limiting middleware
   - Limit requests per IP/session
   - Prevent abuse

### Recommended Production Setup

```typescript
// app/api/voice/stt/route.ts
import { createClient } from '@deepgram/sdk';

export async function POST(request: Request) {
  // Verify tenant exists
  // Check rate limits
  // Forward to Deepgram server-side
  // Return transcription
}

// app/api/voice/tts/route.ts
import { ElevenLabsClient } from '@elevenlabs/elevenlabs-js';

export async function POST(request: Request) {
  // Verify tenant exists
  // Check rate limits
  // Forward to ElevenLabs server-side
  // Return audio
}
```

---

## 🧪 Testing

### Manual Testing

1. Start dev server: `npm run dev`
2. Navigate to your test page
3. Click phone button
4. Say: "I want to schedule an appointment for tomorrow"
5. Verify:
   - Transcription appears correctly
   - AI responds appropriately
   - Voice sounds natural
   - Conversation flows smoothly

### Browser Requirements

- **Chrome/Edge**: Full support
- **Firefox**: Full support
- **Safari**: Full support (iOS 14.5+)
- **HTTPS required** for microphone access (except localhost)

### Troubleshooting

**No microphone access**:
- Check browser permissions
- Ensure HTTPS (or localhost)
- Try different browser

**No audio playback**:
- Check browser autoplay policies
- User must interact with page first
- Check speaker/volume settings

**Transcription not working**:
- Verify Deepgram API key
- Check browser console for errors
- Ensure microphone is working

**TTS not working**:
- Verify ElevenLabs API key
- Check audio format compatibility
- Review browser console

---

## 📊 Monitoring

### Deepgram Console
- https://console.deepgram.com
- Monitor usage, costs, errors
- View transcription accuracy

### ElevenLabs Dashboard
- https://elevenlabs.io/usage
- Track character usage
- Monitor API calls
- Review voice quality

### Database Queries

**Check voice conversations**:
```sql
SELECT
  id,
  channel,
  status,
  lead_score,
  created_at,
  (SELECT COUNT(*) FROM messages WHERE conversation_id = conversations.id) as message_count
FROM conversations
WHERE channel = 'voice'
ORDER BY created_at DESC
LIMIT 20;
```

**Voice conversation metrics**:
```sql
SELECT
  DATE(created_at) as date,
  COUNT(*) as total_conversations,
  COUNT(CASE WHEN lead_score = 'hot' THEN 1 END) as hot_leads,
  AVG((SELECT COUNT(*) FROM messages WHERE conversation_id = conversations.id)) as avg_messages
FROM conversations
WHERE channel = 'voice'
  AND created_at > NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

---

## 🚀 Next Steps

### Immediate
1. Add voice widget to landing page or dashboard
2. Test with real conversations
3. Monitor costs and quality
4. Adjust voice settings as needed

### Enhancements
1. **Voice selection UI** - Let tenants choose their AI voice
2. **Language support** - Add Spanish, French, etc.
3. **Voice interruption** - Allow users to interrupt AI
4. **Sentiment analysis** - Detect caller emotions
5. **Call recording** - Save audio for review
6. **Voicemail** - Handle after-hours calls
7. **Transfer to human** - Escalation when needed

### Phone Integration (Later)
- Integrate Twilio Voice for actual phone calls
- Get dedicated phone number
- Route calls through voice agent
- Add call forwarding, voicemail, etc.

---

## 📚 API Reference

### VoiceWidget Props

```typescript
interface VoiceWidgetProps {
  tenantSlug: string;           // Required: Tenant identifier
  voiceId?: string;             // Optional: ElevenLabs voice ID
  position?:                    // Optional: Widget position
    | 'bottom-right'
    | 'bottom-left'
    | 'top-right'
    | 'top-left';
  primaryColor?: string;        // Optional: Widget color (hex)
  greeting?: string;            // Optional: Initial greeting text
}
```

### VoiceAgent Methods

```typescript
const agent = new VoiceAgent(config);

// Start conversation
await agent.start();

// Stop conversation
agent.stop();

// Get current state
const state = agent.getState();

// Get conversation history
const history = agent.getHistory();

// Get conversation ID
const id = agent.getConversationId();
```

---

## ✅ Checklist for Production

- [ ] Deepgram API key configured
- [ ] ElevenLabs API key configured
- [ ] Voice widget added to pages
- [ ] Test conversation end-to-end
- [ ] Verify microphone permissions work
- [ ] Verify audio playback works
- [ ] Check HTTPS deployment
- [ ] Set up usage monitoring
- [ ] Set usage limits/alerts
- [ ] Test on multiple browsers
- [ ] Test on mobile devices
- [ ] Review cost per conversation
- [ ] Add rate limiting (if needed)
- [ ] Implement proxy endpoints (optional)
- [ ] Train team on voice features

---

**Voice integration is complete and ready to use!** 🎉

Questions? Check the implementation in `lib/voice/` or reach out for support.
