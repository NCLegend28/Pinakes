# guapo_evals

**Datadog for AI agents.** Drop-in SDK that traces every LLM call, tool call,
and decision, then runs a golden-set eval suite on every deploy.

Three components:

```
┌─────────────────────┐       ┌─────────────────────┐       ┌───────────────┐
│ guapo_evals SDK     │──────▶│ Control Plane       │──────▶│ Dashboard     │
│ (pip install)       │ HTTP  │ (FastAPI + Postgres)│  SSE  │ (Next.js)     │
│ @traced decorator   │       │ ingest + eval runs  │       │ traces + evals│
└─────────────────────┘       └─────────────────────┘       └───────────────┘
   customer's app                   your service                  browser
```

## Why this exists

Agents are non-deterministic. A prompt change that fixes one case regresses
three others silently. Teams ship to prod blind. This gives them:

1. **Traces** — every LLM call, tool call, and decision logged with cost, latency, tokens.
2. **Evals** — golden-set regression suite that runs on every deploy. Fail the build if quality drops.
3. **Alerts** — hook into Slack/webhooks when pass-rate or p95 latency drifts.

## Repo layout

- `sdk/` — the `guapo_evals` Python package customers `pip install`. Zero-config tracing via decorator.
- `control_plane/` — FastAPI service that ingests traces, stores them, runs eval jobs. Postgres + async SQLAlchemy.
- `dashboard/` — Next.js UI for viewing traces, configuring evals, watching pass-rates.
- `examples/` — integration examples (OpenAI, Anthropic, LangChain, LangGraph, bare loop).
- `deploy/` — Docker Compose for self-hosted, systemd for VPS, k8s manifests for later.

## Quick start (local dev)

```bash
# 1. Set up Postgres locally (or use Docker — see deploy/docker-compose.yml)
createdb guapo_evals

# 2. Control plane
cd control_plane
uv sync
cp .env.example .env  # fill ANTHROPIC_API_KEY, DATABASE_URL
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000

# 3. SDK — install in editable mode for dev
cd ../sdk
uv sync
uv run pytest

# 4. Dashboard
cd ../dashboard
npm install
npm run dev  # port 3000
```

Then in any agent:

```python
from guapo_evals import init, traced

init(api_key="tenant-key-from-dashboard", endpoint="http://localhost:8000")

@traced(name="classify_ticket")
async def classify_ticket(text: str) -> str:
    # your existing code — no other changes
    response = await client.messages.create(...)
    return response.content[0].text
```

That's it. Traces flow to the control plane. Open the dashboard to see them.

## What to build first

See `docs/ROADMAP.md` for the 90-day plan. TL;DR:

1. Week 1–2: SDK MVP + control plane ingest endpoint. Dogfood on tweet pipeline.
2. Week 3–5: Dashboard + first eval runner (Claude-as-judge).
3. Week 6–8: First paying pilot. Alerts + CI integration.
4. Week 9–12: Launch on HN. Financio + AI Receptionist as case studies.

## License

Proprietary — BliqByte, 2026.
