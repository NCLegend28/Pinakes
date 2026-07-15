# guapo_evals — AI Governance & Architecture

This file is read by Claude (and Tali) before touching code. Architectural
decisions, conventions, and guardrails live here.

## What this product is

An observability + eval platform for AI agents. Customers install a Python SDK,
decorate their LLM-using functions, and get traces + evals in a dashboard.

Think: **LangSmith / Braintrust / Langfuse, but opinionated and cheap.**

## What it is NOT

- Not a model gateway (use LiteLLM, Portkey).
- Not a prompt management tool (that's a v2 feature).
- Not a feature store (different problem).
- Not trying to support every framework on day 1 — start with Anthropic + OpenAI raw SDKs.

## Architecture — three services, one repo (monorepo)

```
customer app ──▶ guapo_evals SDK ──HTTP──▶ control_plane ──▶ Postgres
                                              │
                                              ├──▶ eval_worker (async tasks)
                                              │
                                              └──▶ SSE ──▶ dashboard (Next.js)
```

**SDK** (`sdk/`): Python, async-first, zero dependencies beyond `httpx` +
`pydantic`. Non-blocking ingest — never slow down the customer's app. If the
control plane is down, drop the trace to local disk and retry later.

**Control plane** (`control_plane/`): FastAPI + async SQLAlchemy + Postgres.
Three logical subsystems:
- `api/` — HTTP endpoints: `/ingest`, `/evals`, `/traces`, `/auth`
- `evaluators/` — runs golden-set evals (Claude-as-judge, rule-based, exact-match)
- `models/` — SQLAlchemy ORM (Trace, Span, EvalRun, GoldenSet, Tenant)

**Dashboard** (`dashboard/`): Next.js 14 (App Router). Server components for
lists, client components for the live trace view. SSE for live updates.

## Non-negotiable conventions

**Async throughout.** SDK, server, workers. No `time.sleep()`, no sync
`requests`. Uses `asyncio`, `httpx.AsyncClient`, SQLAlchemy 2.0 async.

**Typed everywhere.** `mypy --strict` on SDK. Pydantic v2 for all API
boundaries. Dataclasses for internal config. `TypedDict` or `BaseModel` —
never bare `dict`.

**The SDK must never raise into the customer's app.** If ingest fails, log
a warning and drop the trace. A broken eval platform must not break the
customer's production traffic. There's a dedicated test suite for this.

**Tenant isolation from day one.** Every trace has a `tenant_id`. Every query
filters on it. Row-level enforcement in one place (middleware) — not sprinkled
through route handlers.

**Secrets:** `.env` local → Doppler staging/prod. Never commit keys. See
`.env.example` in each service.

**Python package manager: `uv`.** Not pip, not poetry.
`pyproject.toml` with `[tool.uv]` section. Lock file committed.

**Migrations: Alembic.** Never `create_all()` in prod. Every schema change
has a migration file, even in dev.

## Language choices — why Python for all three

- SDK in Python: customers are Python-first. A TypeScript SDK comes later.
- Control plane in Python: shares Pydantic models with SDK for ingest
  validation. One language = less cognitive overhead for a solo founder.
- Dashboard in TS/Next.js: no choice — it's a browser UI.

Later, if profiling shows the ingest hot path is CPU-bound, the ingest
endpoint alone can be rewritten in Rust (Axum) and the rest stays in Python.
Do not pre-optimize.

## Testing philosophy

- SDK: unit tests for every public function. Property-based tests (`hypothesis`)
  for the decorator — it should never drop data or block the parent coroutine.
- Control plane: integration tests against a real Postgres (testcontainers).
  No mocking the database.
- End-to-end: one happy-path test that runs the SDK against a live control
  plane and verifies a trace lands.

## Observability of the observability tool

Yes, this is meta. The control plane emits Prometheus metrics:
- `traces_ingested_total{tenant,status}`
- `ingest_latency_seconds` histogram
- `eval_run_duration_seconds` histogram
- `db_query_duration_seconds` histogram

No external APM on the control plane — just Prom + Grafana.

## What NOT to do

- **Don't build a pretty dashboard first.** The SDK and ingest must be rock-solid
  before a single pixel of UI polish. Customers tolerate an ugly dashboard; they
  don't tolerate dropped traces.
- **Don't support every LLM framework.** Ship Anthropic + OpenAI. LangChain and
  LlamaIndex come via their existing callback/tracer hooks, not first-class.
- **Don't build prompt management.** Separate product. Scope creep kills v1.
- **Don't run evals synchronously in the ingest path.** Evals are background jobs.
  Ingest latency p95 must stay under 50ms.

## File creation rules for Claude

When Claude edits this repo:
- Every new Python file starts with a module docstring explaining its role.
- Every public function has a type signature and a one-line docstring.
- No `print()` — use the `logging` module. SDK uses a namespaced logger
  (`logging.getLogger("guapo_evals")`).
- No silent `except:` clauses. Every exception handler logs what it caught
  and why it's safe to swallow.

## Questions that come up and their answers

**Q: Why not use OpenTelemetry?**
A: Eventually yes — we'll emit OTel-compatible spans from the SDK so customers
already on OTel can pipe traces to us and their existing backend. For v1,
a custom wire format is simpler and faster to iterate on. Track OTel export as
a v2 item.

**Q: Why Claude-as-judge and not a fine-tuned classifier?**
A: Cold-start problem. Nobody has labeled eval data yet. Claude with a good
rubric beats a from-scratch classifier at day 1. Add a fine-tuning path when
customers have >10k labeled examples.

**Q: Why not multi-tenant SaaS only — why self-hostable?**
A: Enterprise security buyers will not send their production LLM traces to a
third-party cloud. Self-hosted (Docker Compose → k8s) is the enterprise motion.
SaaS is the SMB motion. Both share the same codebase.
