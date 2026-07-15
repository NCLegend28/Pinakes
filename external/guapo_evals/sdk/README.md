# guapo_evals Python SDK

Drop-in tracing + evals for LLM-powered apps.

## Install

```bash
pip install guapo-evals    # once published
# or for dev:
uv pip install -e .
```

## Quick start

```python
import guapo_evals
from guapo_evals import traced, log_llm_call

guapo_evals.init(api_key="sk_live_...", endpoint="https://api.guapo.dev")

@traced(name="answer_question", tags={"env": "prod"})
async def answer_question(q: str) -> str:
    response = await client.messages.create(
        model="claude-opus-4-7",
        messages=[{"role": "user", "content": q}],
    )
    # Optional: fine-grained LLM call logging
    log_llm_call(
        model="claude-opus-4-7",
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
    )
    return response.content[0].text
```

That's it. Traces flow to the control plane asynchronously.

## Guarantees

- **Non-blocking.** Ingest happens on a background task. Your request path is not slowed down.
- **Never raises.** If the control plane is down or your API key is wrong, the SDK
  logs a warning and drops the trace. Your app keeps running.
- **Bounded memory.** Queue holds max 10k events. When full, oldest traces drop.

## Configuration

Either pass `api_key` + `endpoint` to `init()` or set env vars:

- `GUAPO_EVALS_API_KEY`
- `GUAPO_EVALS_ENDPOINT` (defaults to https://api.guapo.dev)

## Shutdown

Call `await guapo_evals.shutdown()` before your process exits to flush
pending traces. If you're using FastAPI, add it to the lifespan handler.

## Dev

```bash
uv sync
uv run pytest
uv run mypy guapo_evals
uv run ruff check .
```
