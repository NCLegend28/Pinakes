# Agent Harness Plan — "AgentRig"

*Working name. Rename later.*

**Goal:** Build a reusable harness that runs Claude as primary and MLX-served local models as failover, with cross-model validation, so agents can keep working through rate limits and validate each other against hallucination. Three agents will live on top: research tracker, coding harness, research implementer.

---

## The Big Picture (Analogy)

Think of this like running a **24/7 recording studio with two engineers on rotation.**

- **Claude** is your A-list engineer — expensive per hour, world-class, has a day rate cap.
- **MLX local** (Qwen2.5-Coder-32B or similar) is your salaried in-house engineer — always available, not as sharp on some things, rock solid on others.
- **The harness** is the studio itself: power, mixing board, session notes, the logbook of what's been recorded, and the intercom between engineers when they swap.
- **The agents** are the bands that come in to record. Same studio, different albums.

When one engineer needs a break, the other picks up the session where it was left — reads the logbook, listens to what's been tracked, continues the album. When the first one comes back, same handoff in reverse. They also listen to each other's takes and flag anything that sounds off. That's the validation loop.

---

## Architecture at a Glance

```
┌─────────────────────────────────────────────────────────┐
│                      AGENTS LAYER                        │
│   research_tracker  │  coding_harness  │  implementer   │
│   (thin configs: prompts, tools, memory scope)          │
└────────────┬────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────┐
│                     HARNESS LAYER                        │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌────────┐ │
│  │  Router  │  │  Context  │  │Validator │  │  Loop  │ │
│  │(failover)│  │ (compress │  │ (2nd eye)│  │(ReAct) │ │
│  │          │  │ + handoff)│  │          │  │        │ │
│  └──────────┘  └───────────┘  └──────────┘  └────────┘ │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌────────┐ │
│  │  Tools   │  │Telemetry  │  │  Memory  │  │ Config │ │
│  │(registry)│  │ (SQLite)  │  │ (shared) │  │ (yaml) │ │
│  └──────────┘  └───────────┘  └──────────┘  └────────┘ │
└────────────┬────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────┐
│                     MODEL BACKENDS                       │
│   Anthropic API (Claude)    │    MLX Server (local)     │
│   claude-opus-4-7, etc.     │    Qwen2.5-Coder-32B-4bit │
└──────────────────────────────────────────────────────────┘
```

Both backends speak an OpenAI-compatible shape (MLX's server mode gives us this for free). The router doesn't care which is which — it just knows "primary" and "secondary."

---

## Tech Choices (Locked)

| Component | Choice | Why |
|---|---|---|
| Language | Python 3.12 | Ecosystem, your strongest, fits MLX |
| Package mgmt | `uv` | Your convention |
| Local inference | `mlx-lm` server mode | Native M4, OpenAI-compatible, zero Docker |
| Primary model | Claude (via Anthropic SDK) | |
| Fallback model | Qwen2.5-Coder-14B-4bit (MLX) | ~9GB RAM; use 7B on 8GB Macs, 32B on 32GB+ |
| Config | YAML per agent | Easy to diff, easy to read |
| Telemetry | SQLite + structured logs | No infra, queryable |
| Memory | SQLite + JSON files | Simple, inspectable |
| Inter-agent msg | SQLite queue | Good enough for three agents |
| Secrets | `.env` local, Doppler hook ready | Your convention |
| Tests | `pytest` | |

---

## Repo Layout

```
agentrig/
├── CLAUDE.md                  # your standards doc (light integration)
├── pyproject.toml             # uv-managed
├── .env.example
├── README.md
│
├── agentrig/                  # the harness library
│   ├── __init__.py
│   ├── router.py              # Claude ↔ MLX failover
│   ├── context.py             # compression + cross-model handoff
│   ├── validator.py           # second-eye checks
│   ├── loop.py                # agentic loop (ReAct-style)
│   ├── telemetry.py           # logging, cost tracking, rate-limit tracking
│   ├── memory.py              # shared memory primitives
│   ├── config.py              # YAML loader, agent config schema
│   ├── bus.py                 # inter-agent message queue
│   ├── backends/
│   │   ├── base.py            # abstract Backend interface
│   │   ├── anthropic.py       # Claude wrapper
│   │   └── mlx_local.py       # MLX server wrapper
│   └── tools/
│       ├── base.py            # Tool interface
│       ├── registry.py        # enable/disable per agent
│       ├── fs.py              # file ops
│       ├── shell.py           # subprocess
│       ├── web.py             # search + fetch
│       ├── arxiv.py           # paper queries
│       ├── git.py
│       └── rss.py
│
├── agents/                    # thin agent configs
│   ├── research_tracker/
│   │   ├── config.yaml
│   │   ├── system_prompt.md
│   │   └── memory/
│   ├── coding_harness/
│   │   ├── config.yaml
│   │   ├── system_prompt.md
│   │   └── memory/
│   └── research_implementer/
│       ├── config.yaml
│       ├── system_prompt.md
│       └── memory/
│
├── scripts/
│   ├── start_mlx_server.sh    # boots MLX server on :8080
│   ├── run_agent.py           # CLI: python scripts/run_agent.py coding_harness
│   └── health_check.py
│
└── tests/
    ├── test_router.py
    ├── test_context.py
    ├── test_validator.py
    ├── test_loop.py
    └── integration/
        └── test_failover.py   # kills Claude mid-turn, verifies MLX picks up
```

---

## The Failover Loop (Your Core Idea, Detailed)

This is the flow you described. Walking it step by step:

1. **Task begins.** Agent is given an objective. Router picks **primary (Claude)**.
2. **Loop iteration:** agent plans → calls tool → observes result → repeats.
3. **Rate-limit signal.** Router catches one of:
   - HTTP 429 from Anthropic
   - Daily token budget hit (we track locally in telemetry)
   - Explicit `rate_limit_error` in response
4. **Freeze state.** The current conversation + scratchpad + tool history is snapshotted.
5. **Context compression for handoff.** (This is where your "converted context" lives.)
   - Claude (or a cached prior summary) writes a **handoff digest**: what we're doing, what's been tried, what the current hypothesis is, what to do next, open questions.
   - We strip verbose tool outputs, keep decisions and artifacts.
   - The digest is formatted for the smaller model's strengths (shorter context, more explicit structure).
6. **Swap to MLX.** Router flips primary to MLX. Same objective, compressed context loaded, loop continues.
7. **Validation pass on prior work.** Before MLX adds new work, it reviews the frozen Claude output:
   - Re-runs any code that was written (via shell tool)
   - Fact-checks any specific claims using web/arxiv tools
   - Flags anything it can't verify as `needs_recheck`
8. **MLX continues the work.**
9. **Claude recovers.** Router detects rate-limit window has reset (poll Anthropic or just retry after cooldown).
10. **Swap back.** Same handoff protocol in reverse. Claude validates MLX's work the same way.
11. **Repeat until task complete.**

### Validation — the "second eye"

This is important: **the validator isn't a separate model, it's a role the off-duty model plays at swap time.** Concretely:

- Before the swap-in model writes anything new, it gets a "validation turn" with a specific system prompt: *"Review the following work from the other model. Run any code. Verify factual claims. Flag hallucinations. Return structured findings."*
- Findings are appended to the shared scratchpad as `validation_notes`.
- If findings include `severity: high`, the loop pauses for a correction turn before continuing.
- Telemetry logs every flagged issue — over time you'll see which model hallucinates about what.

This is stronger than one model checking itself because the models have different failure modes. Claude has its blind spots; Qwen has different ones. Overlap of both = real error.

### Why you were hitting limits even on "local" models

You mentioned being surprised to hit limits on local models. Three likely reasons:

- **OpenRouter is not local.** It's a cloud gateway that routes to hosted models. You'll hit per-minute and daily caps there just like any cloud API.
- **Ollama cloud mode** (if you were using it) also has quotas for hosted endpoints.
- **True local** means inference running on your hardware — no network, no quotas, only your RAM and GPU as limits.

With `mlx_lm.server` on your M4, the only "limits" are your own machine's throughput. No 429s. This is the setup this plan uses.

---

## Phase-by-Phase Build Plan

Foundation-first, as you asked. Each phase is scoped to a weekend or a few evenings.

### ✅ Phase 0 — Setup (COMPLETE)

**Goal:** Empty-but-real project, environment works, MLX server serves tokens.

- [x] `uv init agentrig` — `pyproject.toml`, `.venv`, `uv.lock` in place
- [x] Add deps: `anthropic`, `mlx-lm`, `pyyaml`, `pydantic`, `httpx`, `rich`, `python-dotenv`, `pytest`, `ruff`, `mypy`
- [x] Full repo layout scaffolded: `agentrig/`, `agents/`, `scripts/`, `tests/`
- [x] `scripts/start_mlx_server.sh` — run with `bash scripts/start_mlx_server.sh`
- [x] `scripts/health_check.py` — Claude: OK confirmed; MLX: OK when server is running
- [x] Package installed as editable (`hatchling` build-system, `uv sync`)
- [x] 11/11 unit tests passing

### ✅ Phase 1 — Backend abstraction + router (COMPLETE)

**Goal:** A single `chat()` call that transparently routes to Claude or MLX and falls over correctly.

- [x] `Backend` ABC in `backends/base.py` — `chat()`, `healthy()`, `estimate_cost()`
- [x] `AnthropicBackend` — wraps SDK, catches 429s and budget overages, raises `RateLimitError`
- [x] `MLXBackend` — thin wrapper over the local `/v1/chat/completions` endpoint
- [x] `Router` — holds primary/secondary, flips on `RateLimitError`, polls for recovery
- [x] `test_router.py` — 3 tests: default routing, failover, recovery flip-back
- [x] `tests/integration/test_failover.py` — live test with synthetic $0.00001 budget

**Deliverable:** `router.chat(messages)` transparently falls over to MLX on rate limit. Integration test verifies end-to-end.

### ✅ Phase 2 — Context compression + handoff (COMPLETE)

**Goal:** When the router swaps, the other model picks up the session coherently.

- [x] Design the `HandoffDigest` schema (pydantic model):
  - `objective`, `decisions_made`, `current_state`, `next_steps`, `open_questions`, `artifacts` (paths to files), `validation_flags`
- [x] Implement `context.compress(messages, active_backend, target_backend) -> HandoffDigest`:
  - Calls the active model with a meta-prompt: "Summarize this session into a handoff digest."
  - Tailors length/style for target: terse prompt for MLX (≤16K context budget), rich prompt for Claude
  - `Backend.max_context_tokens` drives the selection (MLX=8 192, Anthropic=200 000)
- [x] Implement `context.resume(digest, target_backend) -> messages`:
  - Compact single-line format for small-context targets; full markdown for large-context targets
- [x] Unit tests: 9 tests covering roundtrip, prompt selection, and format variants (18 total, all passing)

**Analogy:** This is the engineer writing session notes before their shift ends, and the next engineer reading them before they touch the board.

### ✅ Phase 3 — Agentic loop + tools (COMPLETE)

**Goal:** The ReAct-style think/act/observe loop, with a minimal tool registry.

- [x] Implement `Tool` interface: `name`, `description`, `schema`, `run(args) -> result` + `to_anthropic_schema()`
- [x] Build registry with starter tools: `read_file`, `write_file`, `run_shell` (cwd-scoped), `web_search`, `web_fetch`, `arxiv`, `git`, `rss`
- [x] Implement `Loop`:
  - Parses tool calls from model response, dispatches via ToolRegistry
  - Appends observations, repeats until `stop_reason == "end_turn"` or limit hit
  - Enforces `max_iterations`, `max_cost_usd`, `max_wall_seconds`
  - Persists trace to SQLite via Telemetry (start_run, log_message, end_run)
  - Handles context handoff via `router.consume_handoff()` at swap time
- [x] Add `run_agent.py` CLI — `uv run python scripts/run_agent.py coding_harness "task"`
- [x] Unit tests: 21 tests covering Tool interface, ToolRegistry, ReadFileTool, WriteFileTool, ShellTool (44 total passing)

**Deliverable:** A real agentic session end to end with failover working and tools running.

### ✅ Phase 4 — Validator (COMPLETE)

**Goal:** Cross-model second-eye checks at every swap.

- [x] Implement `Validator.review(prior_work, current_backend) -> ValidationReport`
- [x] Define `ValidationReport` with `Finding(severity, category, description, suggested_fix)` and `has_high_severity` property
- [x] Wire into `Router`: on every swap, after context handoff, validator reviews the prior model's full message history using the incoming backend
- [x] Categories supported: `code_correctness`, `factual_claim`, `internal_consistency`, `tool_result_misread`
- [x] HIGH severity → correction message injected into working_messages before final call; MEDIUM → annotation message injected; LOW → silent log
- [x] `consume_validation_report()` on Router mirrors `consume_handoff()` — Loop drains it each turn
- [x] Loop calls `telemetry.log_swap()` when handoff consumed, `telemetry.log_finding()` for each finding
- [x] Tests: 5 new router tests (report set after swap, clears after consume, HIGH injection, MEDIUM annotation, validation disabled); 4 new loop tests (swap log, finding log, no-log on clean run)

### ✅ Phase 5 — Telemetry + memory (COMPLETE)

**Goal:** You can see what happened and agents remember across sessions.

- [x] SQLite schema: `runs`, `messages`, `tool_calls`, `swaps`, `validation_findings` — fully wired in `telemetry.py`
- [x] `Telemetry.log_tool_call()` added; `run_details()` enriches runs with swap/tool/finding counts; `recent_findings()` filters by min severity and joins run metadata
- [x] Simple CLI dashboard: `uv run python scripts/dashboard.py` → last 10 runs, costs, swap counts, flagged findings; `--findings` flag for validation findings table
- [x] Memory primitives: `AgentMemory` in `agentrig/memory.py` — SQLite KV store with upsert, and FTS5 text memory with BM25 search, per-agent namespacing
- [x] Config option for agents to scope memory reads via `memory.scope` in `config.yaml` (research tracker reads everyone's, coding harness reads its own, etc.)
- [x] Memory tools: `MemoryKVSetTool`, `MemoryKVGetTool`, `MemoryWriteTool`, `MemorySearchTool` in `agentrig/tools/memory.py`; wired into `scripts/run_agent.py`
- [x] Tests: `tests/test_memory.py` (24 tests — KV CRUD, FTS search, cross-namespace read/write isolation) + `tests/test_telemetry.py` (17 tests — run lifecycle, tool/swap/finding counts, ordering)
- [x] 86/86 unit tests passing

### ✅ Phase 6 — The three agents (COMPLETE)

**Research tracker** (`agents/research_tracker/`)
- Tools: `arxiv`, `rss`, `web_search`, `web_fetch`, `write_file`, + full memory tool suite
- Job: daily/on-demand scan of feeds and arxiv, deduplicate against FTS memory, rank by project relevance, write digest to `agents/research_tracker/memory/digest-YYYY-MM-DD.md`
- System prompt: full workflow with RSS sources, dedup via `memory_search`, KV tracking of `last_run_date`

**Coding harness** (`agents/coding_harness/`)
- Tools: `read_file`, `write_file`, `run_shell` (gated), `git` (gated), `web_search`, full memory suite, `bus_pop`
- Job: ReAct coding assistant — checks bus queue on startup, plans, executes, tests, iterates per Tali's `uv`/ruff/mypy/pytest conventions
- System prompt: startup checklist (bus_pop → memory_kv_get → continue), full workflow with ruff + mypy verify step

**Research implementer** (`agents/research_implementer/`)
- Tools: `read_file`, `write_file` (gated), `web_fetch`, full memory suite, `bus_push`
- Job: reads tracker digests, evaluates papers, writes structured plan files, queues tasks to coding harness via bus
- System prompt: full plan format, bus payload schema, "no code — plans only" rule

**New harness additions for Phase 6:**
- [x] `agentrig/tools/bus.py` — `BusPushTool`, `BusPopTool`, `BusPeekTool` wrapping `MessageBus`; wired into `run_agent.py`
- [x] `require_human_approval` gating live in `Loop._execute_tool` — prints args, prompts stdin y/N, logs denied calls to telemetry
- [x] All three `agents/*/memory/` directories created
- [x] `coding_harness/config.yaml` model fixed (`claude-opus-4-7` → `claude-opus-4-6`)
- [x] 86/86 unit tests passing

### Phase 7 — Productionize (ongoing)

- [ ] Dockerfile (optional — for when you want to run on a server)
- [ ] Doppler integration for secrets (light hook)
- [ ] Scheduled runs via `launchd` on the Mac (daily research digest)
- [ ] Slack/Discord webhook for agent notifications
- [ ] Evals: curated task set per agent, run weekly, track win rate over time

---

## What You Should Build First (Tonight, If You Want)

Smallest thing that makes the idea real:

1. Get MLX server running (`Phase 0`, 20 minutes)
2. Write the 40-line `Router` that calls Claude, catches `RateLimitError`, falls back to MLX (`Phase 1`, ~2 hours)
3. Drive it from a REPL: `router.chat("write a haiku about rate limits")` — then manually trigger a rate limit by setting a fake $0.01 budget.

Once that works, the rest of this plan becomes addition, not invention. Every subsequent phase is *"add another capability on top of a thing that already works."* That's the feeling you want — it's the opposite of overwhelming.

---

## Open Questions to Decide Later

- **Concurrent agents** — do research tracker and coding harness run in parallel or sequentially? (Start sequential, add concurrency only if needed.)
- **Human-in-the-loop checkpoints** — do you want confirmation before high-impact tool calls (git push, file deletions)? Default: yes, toggleable per agent.
- **Fine-tuning the local model** — down the line, you could fine-tune Qwen on your own codebases. Not for v1.
- **Cost ceilings** — daily Claude spend cap that forces MLX even before 429. Recommend yes, configurable in each agent's YAML.

---

## Success Criteria for v1

- Coding harness can complete a non-trivial task (e.g., "add a function with tests to Financio") with at least one forced model swap mid-task, and the final code passes tests.
- Validator catches at least one real hallucination in a contrived test (we'll seed one on purpose).
- Research tracker produces a usable daily digest with zero manual intervention for a full week.
- Total weekend-evenings to get here: ~5-6.

---

*Carpe diem, Don Guapo. As you climb.*