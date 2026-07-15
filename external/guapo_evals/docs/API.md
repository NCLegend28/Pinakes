# guapo_evals API Reference

Base URL: `http://localhost:8000` (dev) — all endpoints are under `/v1/` except `/health` and `/metrics`.

**Authentication:** every endpoint except `POST /v1/auth/tenants` requires a bearer token:
```
Authorization: Bearer gev_<your_api_key>
```

---

## Auth

### POST /v1/auth/tenants
Create a new tenant and receive its API key. **Dev only** — disabled in staging/prod.  
The key is returned exactly once; save it immediately.

**Request**
```json
{
  "name": "string",          // required
  "owner_email": "string"    // optional
}
```

**Response `201`**
```json
{
  "tenant_id": "uuid",
  "name": "local-dev",
  "api_key": "gev_..."
}
```

**curl**
```bash
curl -s -X POST http://localhost:8000/v1/auth/tenants \
  -H "Content-Type: application/json" \
  -d '{"name": "local-dev", "owner_email": "you@example.com"}' | jq .
```

---

### GET /v1/auth/whoami
Confirm the token is valid and see which tenant it belongs to.

**Response `200`**
```json
{
  "tenant_id": "uuid",
  "tenant_name": "local-dev"
}
```

**curl**
```bash
curl -s http://localhost:8000/v1/auth/whoami \
  -H "Authorization: Bearer gev_..." | jq .
```

---

## Ingest

### POST /v1/ingest
Receive a batch of trace events from the SDK. This is the hot path — do not trigger evals here.

- Max 100 events per batch (configurable via `MAX_EVENTS_PER_BATCH`)
- Inputs/outputs are truncated at 32KB per span if oversized
- One bad event will not reject the whole batch; it's counted in `rejected`

**Request**
```json
{
  "events": [
    {
      "schema_version": 1,
      "trace_id": "uuid",
      "session_id": "string | null",
      "root_name": "string",
      "started_at": "2026-04-20T23:00:00Z",
      "ended_at": "2026-04-20T23:00:01Z",
      "duration_ms": 1042.5,
      "status": "ok | error",
      "error_message": "string | null",
      "tags": { "env": "prod", "model": "claude-sonnet-4-6" },
      "spans": [
        {
          "span_id": "uuid",
          "parent_span_id": "uuid | null",
          "kind": "llm | tool | chain | retriever | custom",
          "name": "string",
          "started_at": "2026-04-20T23:00:00Z",
          "ended_at": "2026-04-20T23:00:01Z",
          "duration_ms": 1042.5,
          "status": "ok | error",
          "error_message": "string | null",
          "model": "claude-sonnet-4-6",
          "usage": {
            "input_tokens": 512,
            "output_tokens": 128,
            "cached_input_tokens": 0,
            "cost_usd": null
          },
          "inputs": { "prompt": "Summarise this article..." },
          "outputs": { "response": "The article discusses..." },
          "tags": { "stage": "summarise" }
        }
      ]
    }
  ]
}
```

**Response `200`**
```json
{
  "accepted": 1,
  "rejected": 0
}
```

**curl**
```bash
curl -s -X POST http://localhost:8000/v1/ingest \
  -H "Authorization: Bearer gev_..." \
  -H "Content-Type: application/json" \
  -d '{
    "events": [{
      "schema_version": 1,
      "trace_id": "00000000-0000-0000-0000-000000000001",
      "root_name": "summarise_pipeline",
      "started_at": "2026-04-20T23:00:00Z",
      "ended_at": "2026-04-20T23:00:01Z",
      "duration_ms": 1042,
      "status": "ok",
      "tags": {"env": "dev"},
      "spans": []
    }]
  }' | jq .
```

---

## Traces

### GET /v1/traces
Paginated list of traces, newest first.

**Query parameters**

| Param | Type | Default | Description |
|---|---|---|---|
| `limit` | int | 50 | 1–200 |
| `before` | ISO datetime | — | Return traces with `started_at` before this timestamp (cursor pagination) |
| `root_name` | string | — | Exact match filter |
| `status` | `ok` \| `error` | — | Filter by outcome |
| `session_id` | string | — | Filter by session |

**Response `200`**
```json
{
  "items": [
    {
      "id": "uuid",
      "session_id": "string | null",
      "root_name": "summarise_pipeline",
      "started_at": "2026-04-20T23:00:00Z",
      "duration_ms": 1042.5,
      "status": "ok",
      "error_message": null,
      "span_count": 3,
      "total_input_tokens": 512,
      "total_output_tokens": 128,
      "total_cost_usd": 0.000432,
      "tags": { "env": "prod" }
    }
  ],
  "next_cursor": "2026-04-20T22:59:00Z"
}
```

Paginate by passing `next_cursor` as `before` on the next request. `next_cursor` is `null` when you've reached the end.

**curl**
```bash
# First page
curl -s "http://localhost:8000/v1/traces?limit=25" \
  -H "Authorization: Bearer gev_..." | jq .

# Filter by function name and status
curl -s "http://localhost:8000/v1/traces?root_name=summarise_pipeline&status=error" \
  -H "Authorization: Bearer gev_..." | jq .

# Next page (use next_cursor value from previous response)
curl -s "http://localhost:8000/v1/traces?limit=25&before=2026-04-20T22:59:00Z" \
  -H "Authorization: Bearer gev_..." | jq .
```

---

### GET /v1/traces/{trace_id}
Full trace with all spans, sorted chronologically.

**Response `200`**
```json
{
  "id": "uuid",
  "session_id": null,
  "root_name": "summarise_pipeline",
  "started_at": "2026-04-20T23:00:00Z",
  "ended_at": "2026-04-20T23:00:01Z",
  "duration_ms": 1042.5,
  "status": "ok",
  "error_message": null,
  "span_count": 2,
  "total_input_tokens": 512,
  "total_output_tokens": 128,
  "total_cost_usd": 0.000432,
  "tags": {},
  "spans": [
    {
      "id": "uuid",
      "parent_span_id": null,
      "kind": "llm",
      "name": "call_claude",
      "started_at": "2026-04-20T23:00:00Z",
      "ended_at": "2026-04-20T23:00:01Z",
      "duration_ms": 1040.0,
      "status": "ok",
      "error_message": null,
      "model": "claude-sonnet-4-6",
      "input_tokens": 512,
      "output_tokens": 128,
      "cost_usd": 0.000432,
      "inputs": { "prompt": "..." },
      "outputs": { "response": "..." },
      "tags": {}
    }
  ]
}
```

**curl**
```bash
curl -s "http://localhost:8000/v1/traces/00000000-0000-0000-0000-000000000001" \
  -H "Authorization: Bearer gev_..." | jq .
```

---

## Evals

### POST /v1/golden-sets
Create a named golden set. Returns `409` if a set with the same name already exists for this tenant.

**Request**
```json
{
  "name": "tweet-pipeline-v1",
  "description": "Optional description"
}
```

**Response `201`**
```json
{
  "id": "uuid",
  "name": "tweet-pipeline-v1",
  "description": "Optional description",
  "created_at": "2026-04-20T23:00:00Z"
}
```

**curl**
```bash
curl -s -X POST http://localhost:8000/v1/golden-sets \
  -H "Authorization: Bearer gev_..." \
  -H "Content-Type: application/json" \
  -d '{"name": "tweet-pipeline-v1", "description": "20 hand-labelled tweet cases"}' | jq .
```

---

### GET /v1/golden-sets
List all golden sets for the tenant, newest first.

**Response `200`**
```json
[
  {
    "id": "uuid",
    "name": "tweet-pipeline-v1",
    "description": "20 hand-labelled tweet cases",
    "created_at": "2026-04-20T23:00:00Z"
  }
]
```

**curl**
```bash
curl -s http://localhost:8000/v1/golden-sets \
  -H "Authorization: Bearer gev_..." | jq .
```

---

### POST /v1/golden-sets/{id}/cases
Add a test case to a golden set.

`criteria` defines how the case is judged:
- **LLM judge:** `{"type": "llm_judge", "rubric": "The summary must be under 50 words and factually accurate."}`
- **Contains:** `{"type": "contains", "value": "expected substring"}`
- **Exact match:** `{"type": "exact_match", "value": "exact expected output"}`

**Request**
```json
{
  "input_payload": { "text": "The article to summarise..." },
  "criteria": {
    "type": "llm_judge",
    "rubric": "The summary must be under 50 words and capture the main claim."
  },
  "notes": "Edge case: very short source article"
}
```

**Response `201`**
```json
{
  "id": "uuid",
  "input_payload": { "text": "The article to summarise..." },
  "criteria": { "type": "llm_judge", "rubric": "..." },
  "notes": "Edge case: very short source article"
}
```

**curl**
```bash
curl -s -X POST "http://localhost:8000/v1/golden-sets/<golden_set_id>/cases" \
  -H "Authorization: Bearer gev_..." \
  -H "Content-Type: application/json" \
  -d '{
    "input_payload": {"text": "SpaceX launched 60 Starlink satellites on Tuesday..."},
    "criteria": {
      "type": "llm_judge",
      "rubric": "Summary must be factually accurate, under 50 words, no hallucinations."
    },
    "notes": "Standard news article case"
  }' | jq .
```

---

### GET /v1/golden-sets/{id}/cases
List all cases in a golden set.

**Response `200`**
```json
[
  {
    "id": "uuid",
    "input_payload": { "text": "..." },
    "criteria": { "type": "llm_judge", "rubric": "..." },
    "notes": "Standard news article case"
  }
]
```

**curl**
```bash
curl -s "http://localhost:8000/v1/golden-sets/<golden_set_id>/cases" \
  -H "Authorization: Bearer gev_..." | jq .
```

---

### POST /v1/eval-runs
Trigger an eval run against a golden set. **Async** — returns immediately with `status: pending`; the run executes in the background.

**Request**
```json
{
  "golden_set_id": "uuid",
  "target": "string",       // endpoint URL, git sha, or symbolic name
  "git_sha": "string"       // optional, for CI correlation
}
```

**Response `202`**
```json
{
  "id": "uuid",
  "golden_set_id": "uuid",
  "target": "http://localhost:8000",
  "git_sha": "abc1234",
  "status": "pending",
  "started_at": null,
  "ended_at": null,
  "total_cases": 20,
  "passed_cases": 0,
  "failed_cases": 0,
  "created_at": "2026-04-20T23:00:00Z"
}
```

**curl**
```bash
curl -s -X POST http://localhost:8000/v1/eval-runs \
  -H "Authorization: Bearer gev_..." \
  -H "Content-Type: application/json" \
  -d '{
    "golden_set_id": "<golden_set_id>",
    "target": "http://localhost:8000",
    "git_sha": "abc1234"
  }' | jq .
```

---

### GET /v1/eval-runs
List eval runs for the tenant, newest first.

**Query parameters**

| Param | Type | Default |
|---|---|---|
| `limit` | int | 50 |

**Response `200`**
```json
[
  {
    "id": "uuid",
    "golden_set_id": "uuid",
    "target": "http://localhost:8000",
    "git_sha": "abc1234",
    "status": "completed",
    "started_at": "2026-04-20T23:00:00Z",
    "ended_at": "2026-04-20T23:01:12Z",
    "total_cases": 20,
    "passed_cases": 18,
    "failed_cases": 2,
    "created_at": "2026-04-20T23:00:00Z"
  }
]
```

Status values: `pending` → `running` → `completed` | `failed`

**curl**
```bash
curl -s "http://localhost:8000/v1/eval-runs?limit=10" \
  -H "Authorization: Bearer gev_..." | jq .
```

---

### GET /v1/eval-runs/{id}
Full run detail including per-case results and LLM judge reasoning.

**Response `200`**
```json
{
  "id": "uuid",
  "golden_set_id": "uuid",
  "target": "http://localhost:8000",
  "git_sha": "abc1234",
  "status": "completed",
  "started_at": "2026-04-20T23:00:00Z",
  "ended_at": "2026-04-20T23:01:12Z",
  "total_cases": 20,
  "passed_cases": 18,
  "failed_cases": 2,
  "created_at": "2026-04-20T23:00:00Z",
  "results": [
    {
      "id": "uuid",
      "case_id": "uuid",
      "passed": true,
      "score": 0.95,
      "reasoning": "The summary is accurate and within the word limit.",
      "actual_output": { "response": "SpaceX deployed 60 satellites..." },
      "duration_ms": 1820.5
    },
    {
      "id": "uuid",
      "case_id": "uuid",
      "passed": false,
      "score": 0.3,
      "reasoning": "The summary introduced a factual error — the article says Tuesday, the summary says Wednesday.",
      "actual_output": { "response": "SpaceX launched satellites on Wednesday..." },
      "duration_ms": 2100.0
    }
  ]
}
```

**curl**
```bash
curl -s "http://localhost:8000/v1/eval-runs/<run_id>" \
  -H "Authorization: Bearer gev_..." | jq .

# Just the failures
curl -s "http://localhost:8000/v1/eval-runs/<run_id>" \
  -H "Authorization: Bearer gev_..." | jq '.results[] | select(.passed == false)'
```

---

## System

### GET /health
Liveness probe — no auth required.

```bash
curl -s http://localhost:8000/health
# {"status":"ok"}
```

### GET /metrics
Prometheus metrics — no auth required.

```bash
curl -s http://localhost:8000/metrics | grep guapo
```

Key metrics:
- `guapo_ingest_events_total{tenant, status}` — events ingested
- `guapo_ingest_latency_seconds` — ingest handler latency histogram
- `guapo_ingest_batch_size` — events per batch histogram

---

## Full workflow example

```bash
export BASE=http://localhost:8000

# 1. Create tenant
RESP=$(curl -s -X POST $BASE/v1/auth/tenants \
  -H "Content-Type: application/json" \
  -d '{"name": "local-dev"}')
export KEY=$(echo $RESP | jq -r .api_key)

# 2. Confirm it works
curl -s $BASE/v1/auth/whoami -H "Authorization: Bearer $KEY" | jq .

# 3. Create a golden set
GS_ID=$(curl -s -X POST $BASE/v1/golden-sets \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "tweet-pipeline-v1"}' | jq -r .id)

# 4. Add a case
curl -s -X POST "$BASE/v1/golden-sets/$GS_ID/cases" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input_payload": {"tweet": "Markets rally as Fed signals rate pause"},
    "criteria": {
      "type": "llm_judge",
      "rubric": "Sentiment label must be bullish or bearish with a confidence score 0-1."
    }
  }' | jq .

# 5. Trigger an eval run
RUN_ID=$(curl -s -X POST $BASE/v1/eval-runs \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d "{\"golden_set_id\": \"$GS_ID\", \"target\": \"$BASE\"}" | jq -r .id)

# 6. Poll until done
watch -n 3 "curl -s $BASE/v1/eval-runs/$RUN_ID \
  -H 'Authorization: Bearer $KEY' | jq '{status, passed_cases, failed_cases}'"

# 7. See the failures
curl -s "$BASE/v1/eval-runs/$RUN_ID" \
  -H "Authorization: Bearer $KEY" | jq '.results[] | select(.passed == false)'
```
