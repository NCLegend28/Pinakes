# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install / sync environment
uv sync

# Run all unit tests
uv run pytest

# Run a single test file
uv run pytest tests/test_router.py -v

# Run a single test by name
uv run pytest tests/test_router.py::test_fails_over_to_secondary_on_rate_limit -v

# Run integration tests (requires live backends)
uv run pytest tests/integration/ -v -m integration

# Lint
uv run ruff check .

# Type-check
uv run mypy agentrig/

# Run an agent
uv run python scripts/run_agent.py coding_harness "fix the failing test in X"

# Check backend health
uv run python scripts/health_check.py

# Start MLX local inference server (first run downloads ~18GB model)
bash scripts/start_mlx_server.sh
```

## Architecture

AgentRig is a three-layer system:

```
Agents layer  →  Harness layer  →  Model backends
```

**Backends** (`agentrig/backends/`) — both implement the `Backend` ABC (`base.py`). `AnthropicBackend` wraps the Anthropic SDK and raises `RateLimitError` on 429s or budget exhaustion. `MLXBackend` is a thin httpx wrapper over the OpenAI-compatible endpoint that `mlx_lm.server` exposes on `localhost:8080`.

**Router** (`agentrig/router.py`) — holds a `primary` and `secondary` backend. `chat()` tries primary, catches `RateLimitError`, flips to secondary, and starts a background asyncio task that polls `primary.healthy()` every N seconds and flips back when it recovers.

**Loop** (`agentrig/loop.py`) — ReAct-style think/act/observe loop. Sends messages to the router, parses tool calls from the response, dispatches them through the `ToolRegistry`, appends observations, and repeats until `stop_reason == "end_turn"` or a limit (iterations / cost / wall-time) is hit.

**Context** (`agentrig/context.py`) — `compress(messages, backend)` asks the active model to summarize the session into a `HandoffDigest` (pydantic model). `resume(digest)` converts it back into a message list for the incoming model. This is the handoff protocol between Claude and MLX at swap time. Not yet wired into `Router` — that's Phase 2.

**Validator** (`agentrig/validator.py`) — `Validator.review(prior_work, backend)` gives the swap-in model a structured "second eye" pass over the prior model's output and returns a `ValidationReport` with `Finding` objects. High-severity findings are intended to trigger a correction turn before the loop continues.

**Tools** (`agentrig/tools/`) — each tool implements `Tool` ABC with `name`, `description`, `schema`, and `async run(args)`. `ToolRegistry` holds the active set and exports Anthropic-format schemas via `to_schemas()`. Starter tools: `read_file`, `write_file`, `run_shell`, `web_search`, `web_fetch`, `arxiv`, `git`, `rss`.

**Agents** (`agents/<name>/`) — thin configs, not Python. Each agent is a `config.yaml` (loaded into `AgentConfig` via `agentrig/config.py`) plus a `system_prompt.md` and a `memory/` dir. `scripts/run_agent.py` is the entry point — it reads the config, wires up backends/tools/loop, and runs.

**Persistence** — `agentrig/telemetry.py` writes all runs, messages, costs, swaps, and validation findings to `agentrig.db` (SQLite). `agentrig/memory.py` is per-agent KV + flat-file storage under `agents/<name>/memory/`. `agentrig/bus.py` is a SQLite-backed inter-agent message queue.

## Key Design Constraints

- The router's failover is transparent — callers just call `router.chat()` and never see which backend responded.
- `estimate_cost()` on `MLXBackend` always returns `0.0` — local inference has no API cost.
- `asyncio_mode = "auto"` is set in pytest config — all test coroutines run without explicit `@pytest.mark.asyncio`.
- Integration tests are gated with `@pytest.mark.integration` and require `ANTHROPIC_API_KEY` in env plus the MLX server running. Unit tests mock both backends and run offline.
- Agent configs control `require_human_approval` — tools listed there are intended to gate on user confirmation before execution (not yet enforced in the loop; Phase 3 work).
