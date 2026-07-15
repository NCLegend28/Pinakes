# 🚀 Quick Start Guide

## 5-Minute Setup

### 1. Install
```bash
npm install
```

### 2. Configure
```bash
cp .env.example .env
```

Edit `.env` and add at least one API key:

```env
# Choose ONE or more:
OPENAI_API_KEY=sk-...              # For OpenAI models
ANTHROPIC_API_KEY=sk-ant-...       # For Claude models
GROQ_API_KEY=gsk_...               # For ultra-fast Groq
# OR run Ollama locally (free)
```

### 3. Set Your Models
```env
# Guard Agent (classification)
GUARD_MODEL_PROVIDER=openai
GUARD_MODEL=gpt-4o-mini

# Qualifier Agent (lead scoring)
QUALIFIER_MODEL_PROVIDER=anthropic
QUALIFIER_MODEL=claude-3-5-sonnet-20241022
```

### 4. Test
```bash
npm run test:hot
```

## 📋 Quick Config Recipes

### 🟢 Beginner (All OpenAI)
```env
OPENAI_API_KEY=sk-...

GUARD_MODEL_PROVIDER=openai
GUARD_MODEL=gpt-4o-mini

QUALIFIER_MODEL_PROVIDER=openai
QUALIFIER_MODEL=gpt-4o
```

### 💎 Recommended (Mixed)
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

GUARD_MODEL_PROVIDER=openai        # Fast classification
GUARD_MODEL=gpt-4o-mini

QUALIFIER_MODEL_PROVIDER=anthropic # Deep reasoning
QUALIFIER_MODEL=claude-3-5-sonnet-20241022
```

### 💰 Budget (Groq + Local)
```env
GROQ_API_KEY=gsk_...

GUARD_MODEL_PROVIDER=groq          # Ultra-fast & cheap
GUARD_MODEL=llama-3.1-8b-instant

QUALIFIER_MODEL_PROVIDER=ollama    # Free local
QUALIFIER_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434/v1
```

### 🔒 Privacy (All Local)
```env
GUARD_MODEL_PROVIDER=ollama
GUARD_MODEL=llama3.2:3b

QUALIFIER_MODEL_PROVIDER=ollama
QUALIFIER_MODEL=llama3.1:8b

OLLAMA_BASE_URL=http://localhost:11434/v1
```
*Requires [Ollama](https://ollama.com) installed and running*

## 🧪 Test Commands

```bash
# Run all test cases
npm run dev

# Individual tests
npm run test:hot     # HOT lead (ready to buy)
npm run test:warm    # WARM lead (exploring)
npm run test:cold    # COLD lead (browsing)
npm run test:faq     # FAQ question
npm run test:spam    # Spam detection
```

## 🔧 Common Issues

**"Module not found"**
```bash
npm install
```

**"Invalid API key"**
- Check `.env` has the correct key
- No quotes around the key value

**"Model not found"** (Ollama)
```bash
ollama pull llama3.2:3b
ollama pull llama3.1:8b
ollama serve
```

**Want to see config on startup?**
```env
LOG_LEVEL=info
```

## 📊 What Each Model Does

| Agent | What it does | Recommended Model |
|-------|-------------|-------------------|
| **Guard** | Classifies intent, detects spam | Fast & cheap: `gpt-4o-mini`, `groq/llama-3.1-8b` |
| **Qualifier** | Scores leads, extracts info | Smart: `claude-3-5-sonnet`, `gpt-4o` |

## 💡 Pro Tips

1. **Start simple**: Use one provider (OpenAI or Anthropic)
2. **Mix later**: Guard with fast model, Qualifier with smart model
3. **Test locally**: Use Ollama for development (free!)
4. **Monitor costs**: Check `model_info` in output

## 🆘 Need Help?

1. Check [README.md](./README.md) for full docs
2. Run `npm run type-check` for errors
3. Set `LOG_LEVEL=debug` for verbose output

---

Ready to go! 🎉
