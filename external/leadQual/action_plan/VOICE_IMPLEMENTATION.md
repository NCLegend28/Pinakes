# 🎙️ Voice Integration Implementation Guide

## Option 1: OpenAI Realtime API (Recommended for Quality)

### Pros:
- Best quality (GPT-4o voice)
- Low latency (~300ms)
- Natural interruptions
- Built-in function calling

### Cons:
- Most expensive (~$0.06/min)
- Beta status

### Implementation:

```typescript
// /lib/voice/openai-realtime.ts
import { RealtimeClient } from '@openai/realtime-api-beta';

export class OpenAIVoiceAgent {
  private client: RealtimeClient;
  private audioContext: AudioContext;
  
  constructor(tenantId: string, config: VoiceConfig) {
    this.client = new RealtimeClient({
      apiKey: process.env.OPENAI_API_KEY,
      model: 'gpt-4o-realtime-preview-2024-12-17'
    });
    
    // Configure for tenant
    this.setupInstructions(tenantId, config);
    this.setupFunctions();
  }
  
  private setupInstructions(tenantId: string, config: VoiceConfig) {
    const instructions = `
You are a virtual receptionist for ${config.businessName}.

Business Type: ${config.industryType}
Services: ${config.services.join(', ')}
Hours: ${config.businessHours}

Your personality: ${config.personality || 'Friendly, professional, helpful'}

Key tasks:
1. Greet callers warmly
2. Understand what service they need
3. Check calendar availability
4. Book appointments
5. Suggest relevant upsells
6. Capture contact information
7. Confirm appointment details

Always:
- Be warm and conversational
- Ask clarifying questions
- Confirm understanding
- Use the customer's name when provided
- End with clear next steps
`;
    
    this.client.updateSession({
      instructions,
      voice: config.voiceType || 'alloy',
      turn_detection: { type: 'server_vad' } // Voice activity detection
    });
  }
  
  private setupFunctions() {
    // Check calendar availability
    this.client.addTool({
      name: 'check_availability',
      description: 'Check if a specific date and time is available',
      parameters: {
        type: 'object',
        properties: {
          date: { type: 'string', description: 'ISO date (YYYY-MM-DD)' },
          time: { type: 'string', description: '24-hour time (HH:MM)' },
          duration_minutes: { type: 'number' }
        },
        required: ['date', 'time']
      }
    }, async (params) => {
      // Call your calendar API
      const isAvailable = await this.checkCalendar(params);
      return { available: isAvailable };
    });
    
    // Book appointment
    this.client.addTool({
      name: 'book_appointment',
      description: 'Book an appointment after confirming availability',
      parameters: {
        type: 'object',
        properties: {
          customer_name: { type: 'string' },
          phone: { type: 'string' },
          email: { type: 'string' },
          date: { type: 'string' },
          time: { type: 'string' },
          service: { type: 'string' },
          notes: { type: 'string' }
        },
        required: ['customer_name', 'phone', 'date', 'time', 'service']
      }
    }, async (params) => {
      const booking = await this.createBooking(params);
      return { booking_id: booking.id, confirmation_sent: true };
    });
    
    // Get service pricing
    this.client.addTool({
      name: 'get_pricing',
      description: 'Get pricing for a service',
      parameters: {
        type: 'object',
        properties: {
          service: { type: 'string' }
        },
        required: ['service']
      }
    }, async (params) => {
      const pricing = await this.getPricing(params.service);
      return pricing;
    });
  }
  
  async startCall() {
    // Connect to audio stream
    await this.client.connect();
    
    // Start microphone
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    this.client.sendAudio(stream);
    
    // Handle AI audio output
    this.client.on('audio', (audioData) => {
      this.playAudio(audioData);
    });
    
    // Handle function calls
    this.client.on('function_call', async (call) => {
      console.log('Function called:', call.name, call.arguments);
    });
    
    // Handle conversation events
    this.client.on('conversation.updated', ({ item, delta }) => {
      if (item.role === 'assistant') {
        console.log('AI speaking:', delta.content);
      }
    });
  }
  
  private async checkCalendar(params: any): Promise<boolean> {
    // Implement calendar check
    return true;
  }
  
  private async createBooking(params: any) {
    // Implement booking creation
    return { id: 'booking_123' };
  }
  
  private async getPricing(service: string) {
    // Implement pricing lookup
    return { service, price: 50 };
  }
  
  private playAudio(audioData: ArrayBuffer) {
    // Play audio through browser
    if (!this.audioContext) {
      this.audioContext = new AudioContext();
    }
    
    this.audioContext.decodeAudioData(audioData, (buffer) => {
      const source = this.audioContext.createBufferSource();
      source.buffer = buffer;
      source.connect(this.audioContext.destination);
      source.start();
    });
  }
}
```

---

## Option 2: Deepgram + ElevenLabs (Cost-Effective)

### Pros:
- High quality
- More affordable (~$0.02/min)
- Good latency
- Proven at scale

### Cons:
- More complex (2 services)
- Need to handle interruptions manually

### Implementation:

```typescript
// /lib/voice/deepgram-elevenlabs.ts
import { createClient } from '@deepgram/sdk';
import { ElevenLabsClient } from 'elevenlabs';

export class DeepgramElevenLabsAgent {
  private deepgram: any;
  private elevenlabs: ElevenLabsClient;
  private audioQueue: ArrayBuffer[] = [];
  
  constructor(private tenantId: string) {
    this.deepgram = createClient(process.env.DEEPGRAM_API_KEY);
    this.elevenlabs = new ElevenLabsClient({
      apiKey: process.env.ELEVENLABS_API_KEY
    });
  }
  
  async startListening() {
    // Get microphone stream
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    
    // Create Deepgram connection
    const connection = this.deepgram.listen.live({
      model: 'nova-2',
      language: 'en-US',
      smart_format: true,
      interim_results: true
    });
    
    // Send audio to Deepgram
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.addEventListener('dataavailable', (event) => {
      connection.send(event.data);
    });
    mediaRecorder.start(250); // Send every 250ms
    
    // Handle transcription results
    connection.on('Results', async (data) => {
      const transcript = data.channel.alternatives[0].transcript;
      
      if (transcript && data.is_final) {
        // Send to AI for response
        await this.processUserInput(transcript);
      }
    });
  }
  
  private async processUserInput(userMessage: string) {
    // Call your AI backend
    const response = await fetch('/api/chat', {
      method: 'POST',
      body: JSON.stringify({
        tenant_id: this.tenantId,
        message: userMessage,
        channel: 'voice'
      })
    });
    
    const { text, actions } = await response.json();
    
    // Convert text to speech
    await this.speak(text);
    
    // Handle any actions (booking, etc.)
    if (actions) {
      await this.handleActions(actions);
    }
  }
  
  private async speak(text: string) {
    const audioStream = await this.elevenlabs.textToSpeech.convert({
      voice_id: 'EXAVITQu4vr4xnSDxMaL', // Sarah voice
      text,
      model_id: 'eleven_turbo_v2_5',
      output_format: 'mp3_44100_128'
    });
    
    // Convert stream to audio and play
    const chunks: Buffer[] = [];
    for await (const chunk of audioStream) {
      chunks.push(chunk);
    }
    
    const audioBuffer = Buffer.concat(chunks);
    this.playAudio(audioBuffer);
  }
  
  private playAudio(buffer: Buffer) {
    const audioContext = new AudioContext();
    const audioData = new Uint8Array(buffer).buffer;
    
    audioContext.decodeAudioData(audioData, (decodedBuffer) => {
      const source = audioContext.createBufferSource();
      source.buffer = decodedBuffer;
      source.connect(audioContext.destination);
      source.start();
    });
  }
  
  private async handleActions(actions: any[]) {
    for (const action of actions) {
      switch (action.type) {
        case 'check_calendar':
          // Handle calendar check
          break;
        case 'book_appointment':
          // Handle booking
          break;
        case 'send_confirmation':
          // Send SMS/email
          break;
      }
    }
  }
}
```

---

## Option 3: Twilio Voice for Phone Calls

### For handling actual phone calls (not just web):

```typescript
// /pages/api/twilio/voice.ts
import { twiml } from 'twilio';

export default async function handler(req, res) {
  const VoiceResponse = twiml.VoiceResponse;
  const response = new VoiceResponse();
  
  // Greeting
  const gather = response.gather({
    input: 'speech',
    action: '/api/twilio/process-speech',
    language: 'en-US',
    speechTimeout: 'auto'
  });
  
  gather.say(
    'Thank you for calling. How can I help you today?',
    { voice: 'Polly.Joanna' }
  );
  
  res.setHeader('Content-Type', 'text/xml');
  res.status(200).send(response.toString());
}

// /pages/api/twilio/process-speech.ts
export default async function handler(req, res) {
  const { SpeechResult, CallSid } = req.body;
  
  // Process with your AI
  const aiResponse = await processWithAI(SpeechResult, CallSid);
  
  const response = new twiml.VoiceResponse();
  
  // Speak AI response
  response.say(aiResponse.text, { voice: 'Polly.Joanna' });
  
  // Continue conversation
  if (aiResponse.needsMoreInfo) {
    const gather = response.gather({
      input: 'speech',
      action: '/api/twilio/process-speech'
    });
    gather.say(aiResponse.followUpQuestion);
  } else {
    // End call
    response.say('Thank you for calling. Have a great day!');
    response.hangup();
  }
  
  res.setHeader('Content-Type', 'text/xml');
  res.status(200).send(response.toString());
}
```

---

## React Component for Voice Widget

```tsx
// /components/VoiceWidget.tsx
'use client';

import { useState, useEffect } from 'react';
import { Mic, MicOff, Phone, PhoneOff } from 'lucide-react';

export function VoiceWidget({ tenantId }: { tenantId: string }) {
  const [isActive, setIsActive] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  
  useEffect(() => {
    if (isActive) {
      startVoiceSession();
    }
    
    return () => {
      stopVoiceSession();
    };
  }, [isActive]);
  
  const startVoiceSession = async () => {
    // Initialize voice agent (choose your implementation)
    const agent = new OpenAIVoiceAgent(tenantId, {
      businessName: 'Your Business',
      industryType: 'nail_salon',
      services: ['manicure', 'pedicure', 'gel'],
      voiceType: 'alloy'
    });
    
    await agent.startCall();
  };
  
  const stopVoiceSession = () => {
    // Cleanup
  };
  
  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Voice widget UI */}
      <div className="bg-white rounded-full shadow-lg p-4">
        <button
          onClick={() => setIsActive(!isActive)}
          className={`
            p-4 rounded-full transition-colors
            ${isActive 
              ? 'bg-red-500 hover:bg-red-600' 
              : 'bg-blue-500 hover:bg-blue-600'
            }
          `}
        >
          {isActive ? (
            <PhoneOff className="w-6 h-6 text-white" />
          ) : (
            <Phone className="w-6 h-6 text-white" />
          )}
        </button>
        
        {isActive && (
          <div className="absolute bottom-20 right-0 bg-white rounded-lg shadow-xl p-4 w-80">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Active Call</span>
                <button onClick={() => setIsMuted(!isMuted)}>
                  {isMuted ? (
                    <MicOff className="w-5 h-5 text-red-500" />
                  ) : (
                    <Mic className="w-5 h-5 text-green-500" />
                  )}
                </button>
              </div>
              
              {/* Transcript */}
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {transcript && (
                  <div className="bg-blue-50 rounded p-2 text-sm">
                    <strong>You:</strong> {transcript}
                  </div>
                )}
                {aiResponse && (
                  <div className="bg-gray-50 rounded p-2 text-sm">
                    <strong>AI:</strong> {aiResponse}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
```

---

## Cost Comparison

### Monthly costs for 1000 conversations (avg 2 min each):

```python
# OpenAI Realtime API
conversations = 1000
avg_duration_minutes = 2
cost = conversations * avg_duration_minutes * 0.06  # $0.06/min
print(f"OpenAI Realtime: ${cost}/month")  # $120/month

# Deepgram + ElevenLabs
deepgram_cost = conversations * avg_duration_minutes * 0.0043  # Deepgram Nova-2
elevenlabs_cost = conversations * avg_duration_minutes * 150 * 0.00003  # $0.30 per 1M chars
total = deepgram_cost + elevenlabs_cost
print(f"Deepgram + ElevenLabs: ${total:.2f}/month")  # ~$18/month

# Your margin at $99/month plan (500 conversations)
revenue = 99
ai_voice_cost = 500 * 2 * 0.02  # Using cheaper option
other_costs = 10  # Infrastructure, etc.
profit = revenue - ai_voice_cost - other_costs
print(f"Profit per customer: ${profit}/month")  # ~$69/month = 69% margin
```

---

## Recommendation

**Start with Deepgram + ElevenLabs**:
- Good quality
- Affordable
- Proven at scale
- Easy to upgrade to OpenAI Realtime later if needed

**Add OpenAI Realtime as premium option**:
- Charge $199+ for plans using it
- Market as "Ultra-HD voice quality"
- Use for enterprise customers

**Add Twilio for phone calls**:
- Essential for full receptionist functionality
- Complements web voice widget
- Opens SMS channel too

---

*Next: Implement calendar integration and appointment booking logic*
