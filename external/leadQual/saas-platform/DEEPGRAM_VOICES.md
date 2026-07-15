# Deepgram Aura Voice Options

## Recommended Voices for Business Receptionist

### Professional Female Voices
- `aura-asteria-en` - Clear, professional, warm (recommended)
- `aura-luna-en` - Friendly, approachable
- `aura-stella-en` - Confident, authoritative
- `aura-athena-en` - Intelligent, precise
- `aura-hera-en` - Mature, professional

### Professional Male Voices
- `aura-orion-en` - Deep, confident
- `aura-arcas-en` - Warm, trustworthy
- `aura-perseus-en` - Clear, professional
- `aura-angus-en` - Friendly, approachable
- `aura-orpheus-en` - Smooth, engaging
- `aura-helios-en` - Energetic, positive
- `aura-zeus-en` - Authoritative, commanding

## How to Use

### Environment Variable
Set in `.env.local`:
```bash
DEEPGRAM_API_KEY=your_deepgram_api_key
DEEPGRAM_VOICE_ID=aura-asteria-en  # Optional, defaults to aura-asteria-en
```

### In VoiceWidget Component
```tsx
<VoiceWidget
  tenantSlug="your-tenant"
  voiceId="aura-luna-en"  // Optional, override default
  greeting="Hello, how can I help you today?"
/>
```

## Voice Characteristics

| Voice | Gender | Accent | Best For |
|-------|--------|--------|----------|
| Asteria | Female | American | Customer service, professional |
| Luna | Female | American | Friendly interactions, warm tone |
| Stella | Female | American | Leadership, confident messaging |
| Athena | Female | American | Technical support, precise info |
| Hera | Female | American | Mature audience, professional |
| Orion | Male | American | Authoritative messaging |
| Arcas | Male | American | Trustworthy, warm interactions |
| Perseus | Male | American | Customer service, clear |
| Angus | Male | American | Casual, friendly |
| Orpheus | Male | American | Engaging storytelling |
| Helios | Male | American | Energetic, positive |
| Zeus | Male | American | Strong, commanding |

## Cost

**Deepgram Aura TTS**: ~$0.015 per 1,000 characters

### Example Calculation
- Average AI response: 150 characters
- 1,000 conversations/month = 1,000 responses
- Total characters: 150,000
- Cost: 150,000 / 1,000 × $0.015 = **$2.25/month**

**50% cheaper than ElevenLabs!**

## Audio Specs

- **Encoding**: Linear16 PCM
- **Container**: WAV
- **Sample Rate**: 24kHz
- **Quality**: High-quality, natural-sounding

## Tips

1. **Asteria** is the best default for most business use cases
2. **Luna** works well for friendlier, more casual brands
3. **Orion** or **Arcas** for male voice preference
4. Test multiple voices to find what fits your brand
5. Voice selection can be changed per-tenant in the database
