# Local Qwen Setup (No Rate Limits!)

## 1. Install Ollama

```bash
# macOS
brew install ollama

# Or download from: https://ollama.ai
```

## 2. Start Ollama

```bash
# Start Ollama service
ollama serve
```

## 3. Pull Qwen Model

In a new terminal:
```bash
# Recommended: 14B model (better quality)
ollama pull qwen2.5:14b

# Or faster: 7B model (lower quality but faster)
ollama pull qwen2.5:7b
```

## 4. Test It

```bash
ollama run qwen2.5:14b "Say hello in JSON format"
```

Should output something like:
```json
{
  "message": "Hello!",
  "language": "en"
}
```

## 5. Configure book-pack-builder

```bash
cd ~/projects/bookPack/book-pack-builder

# Set to use local (default)
export USE_PROVIDER="local"

# Optional: Use 7b for speed
export OLLAMA_MODEL="qwen2.5:7b"
```

## 6. Run Your Book Processing

```bash
python cli.py books/Quantitative_risk_management.pdf --author "Alexander McNeil" --fast
```

**No more rate limits! No API costs!**

## Model Comparison

| Model | Size | Speed | Quality | RAM Needed |
|-------|------|-------|---------|------------|
| qwen2.5:7b | 4.7GB | Fast | Good | 8GB |
| qwen2.5:14b | 9GB | Medium | Better | 16GB |
| qwen2.5:32b | 20GB | Slow | Best | 32GB |

## Troubleshooting

**"Connection refused"**
- Make sure `ollama serve` is running in another terminal

**"Model not found"**
- Run `ollama pull qwen2.5:14b` first

**Too slow?**
- Use `qwen2.5:7b` instead
- Or switch to `USE_PROVIDER="anthropic"` for cloud
