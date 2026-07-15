# Kimi K2 Cloud Setup (via Ollama)

## Overview

Kimi K2 is accessed through Ollama's cloud service - no Chinese phone number required! This gives you enterprise-grade AI without the API key hassle.

---

## Model

### kimi-k2:1t-cloud (Default)
- **Provider**: Ollama Cloud
- **Context**: 8,192 tokens
- **Use**: Guard, Qualifier, Clarifier agents
- **Speed**: Fast
- **Cost**: Very low

---

## Setup (Super Simple)

### Option 1: Ollama Cloud (Recommended)

Already using it! Just configure the base URL:

```env
# Add to .env.local
OLLAMA_BASE_URL=https://your-ollama-cloud-endpoint.com/v1
# or
OLLAMA_BASE_URL=http://localhost:11434/v1  # for local Ollama
```

### Option 2: Local Ollama

```bash
# Pull the model
ollama pull kimi-k2:1t-cloud

# Verify it's available
ollama list
```

No API key needed!

---

## Apply Model Switch

Run the SQL migration to update all agents:

```bash
psql $DATABASE_URL -f database/seeds/003_switch_to_kimi.sql
```

This updates:
- ✅ All industry templates → `ollama/kimi-k2:1t-cloud`
- ✅ Existing tenant agent configs → `ollama/kimi-k2:1t-cloud`

---

## Pricing (via Ollama Cloud)

**Extremely cost-effective** - Ollama's cloud pricing is competitive:

**Cost per conversation** (estimate):
- Guard agent (~500 tokens): ~$0.001
- Qualifier agent (~1500 tokens): ~$0.003
- **Total**: ~$0.004 per conversation

### Monthly Costs (1000 conversations)
- **Kimi K2 (Ollama)**: ~$4.00 ✅ **Cheapest option**
- Compare to DeepSeek: ~$8
- Compare to GPT-4o-mini: ~$30

---

## API Configuration

The workflow engine uses Ollama's OpenAI-compatible endpoint:

```typescript
// In agent_configs table
{
  provider: 'ollama',
  model: 'kimi-k2:1t-cloud',
  temperature: 0.7,
  max_tokens: 2000
}
```

### API Call Example

```bash
curl $OLLAMA_BASE_URL/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kimi-k2:1t-cloud",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant"},
      {"role": "user", "content": "Hello"}
    ],
    "temperature": 0.7
  }'
```

---

## Features

### Supported
- ✅ JSON mode
- ✅ Streaming
- ✅ System messages
- ✅ Temperature control
- ✅ Max tokens

### Not Supported
- ❌ Structured outputs (use JSON instructions instead)
- ❌ Function calling / tools
- ❌ Vision (text-only)

---

## Model Capabilities

Configured in `lib/workflow/model-capabilities.ts`:

```typescript
'ollama/kimi-k2:1t-cloud': {
  supportsStructuredOutputs: false,
  supportsJsonMode: true,
  requiresJsonInstructions: true,
  maxTokens: 8192,
  supportsTools: false
}
```

This means:
- AI will receive JSON formatting instructions in system prompt
- Responses are parsed as JSON
- No native structured output support

---

## Testing

### 1. Verify Model is Available

```bash
# If using local Ollama
ollama list | grep kimi-k2

# If using Ollama Cloud - check your endpoint
curl $OLLAMA_BASE_URL/models
```

### 2. Test Conversation

```bash
npm run dev
# Go to /voice-test
# Click phone button
# Say "I'm looking for a house"
# Check console for model used
```

Look for:
```
[DirectCompletion] baseURL: http://localhost:11434/v1, model: kimi-k2:1t-cloud
```

---

## Troubleshooting

### "Connection refused"
- Check Ollama is running: `ollama serve`
- Verify OLLAMA_BASE_URL is correct
- For cloud: Check your endpoint URL

### "Model not found"
- Pull the model: `ollama pull kimi-k2:1t-cloud`
- Check spelling: `kimi-k2:1t-cloud` (exact match)
- List models: `ollama list`

### "Slow responses"
- Local Ollama needs GPU for speed
- Consider Ollama Cloud for faster processing
- Check system resources

### JSON Parsing Errors
- Kimi sometimes wraps JSON in markdown
- `parseJsonOutput()` handles this automatically
- Check system prompt has JSON instructions

---

## Why Kimi K2 (via Ollama)?

### Pros
- ✅ **No API key required** - works through Ollama
- ✅ **No signup hassles** - no Chinese phone number needed
- ✅ **Cheapest option** - ~$4/month for 1000 conversations
- ✅ Fast response times
- ✅ Good instruction following
- ✅ OpenAI-compatible API
- ✅ Multilingual (Chinese + English)

### Cons
- ❌ No structured outputs
- ❌ Smaller context than GPT-4
- ❌ Limited documentation

### Best For
- MVP and early stage
- Cost-conscious deployments
- Quick iterations
- Developers already using Ollama

---

## Migration Path

### Switch to Kimi K2

```bash
# Run the migration
psql $DATABASE_URL -f database/seeds/003_switch_to_kimi.sql
```

This updates:
- All industry templates → `ollama/kimi-k2:1t-cloud`
- All existing agents → `ollama/kimi-k2:1t-cloud`

### Rollback to DeepSeek (if needed)

```sql
UPDATE industry_templates
SET default_provider = 'ollama', default_model = 'deepseek-v3.1:671b-cloud'
WHERE industry = 'real_estate';

UPDATE agent_configs
SET provider = 'ollama', model = 'deepseek-v3.1:671b-cloud'
WHERE provider = 'ollama' AND model = 'kimi-k2:1t-cloud';
```

---

## Production Checklist

- [ ] Set `OLLAMA_BASE_URL` in environment
- [ ] Pull model: `ollama pull kimi-k2:1t-cloud` (if local)
- [ ] Run migration: `003_switch_to_kimi.sql`
- [ ] Test conversation flow
- [ ] Monitor response times
- [ ] Test error handling
- [ ] Verify JSON parsing works

---

## Support

- **Ollama**: https://ollama.com/
- **Community**: https://github.com/ollama/ollama
- **Models**: https://ollama.com/library

---

## Status

✅ **Configured**: Model capabilities added (`ollama/kimi-k2:1t-cloud`)
✅ **Migration**: SQL script ready (`003_switch_to_kimi.sql`)
✅ **No API Key Needed**: Works through Ollama
✅ **Ready to Use**: Just run migration and test

**Next Steps**:
1. Run: `psql $DATABASE_URL -f database/seeds/003_switch_to_kimi.sql`
2. Test: Visit `/onboarding` and try Step 3 (voice widget)
3. Deploy: Push to production
