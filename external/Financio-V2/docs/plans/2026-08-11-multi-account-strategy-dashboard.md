# Multi-Account Strategy Dashboard ("All + Piece of the Pie") Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task. TDD throughout: write the failing test, watch it fail, implement, watch it pass, commit.

**Goal:** Each strategy (Trend, ML, ML + Trend) runs on its own Alpaca paper account. Selecting a strategy on the dashboard shows ONLY that account's data, straight from that account's broker credentials. An "All" selection shows cumulative data across all active strategy accounts plus each strategy's share of the pie. Every number must be traceable to Alpaca — Alpaca is the validation source. The system must accept new strategies by configuration only (registry entry + env keys + deployment JSON), with zero dashboard code changes.

**Architecture:** Keep the existing account-scoped deployment registry (`FINANCIO_STRATEGY_DEPLOYMENTS` env JSON → `financio_src/strategy_deployments.py`) as the single source of truth. Add a backend **aggregation layer** that fans out to every active deployment's own broker client, sums account-level numbers server-side, and returns totals + per-account breakdown with an explicit sum invariant. Make per-deployment credentials **strict** (no silent fallback to the shared global client — that is how mixed-money numbers leak in). Add a **reconciliation endpoint** that compares dashboard aggregates against fresh Alpaca reads so "factual" is checkable, not asserted. Frontend renders the selector and the All view entirely from API data.

**Tech Stack:** FastAPI backend (`backend/main.py`), `alpaca-py` (`financio_src/broker/alpaca_broker.py`), React+TS+Vite dashboard (`dashboard/`), pytest, Docker Compose on VPS 116.203.16.160 (`docker compose -p financio-clean -f docker-compose.production.yml`).

---

## Verified current state (2026-08-11, read-only audit)

Local repo `/Volumes/samsungT7/projects/Financio-V2-clean` on `main` @ `b4e4694c`, matches GitHub `main` and VPS `/opt/financio-v2`. All containers healthy.

What already exists (do not rebuild):
- `financio_src/strategy_deployments.py` — registry, canonical IDs (`trend`/`ml`/`hybrid` → "Trend"/"ML"/"ML + Trend"), alias mapping, one-active-strategy-per-account validation, `to_api_dict()` with `credentials.configured`.
- Scoped endpoints in `backend/main.py` already accept `deployment_id`/`account_id`: `/api/dashboard-data`, `/api/portfolio-positions`, `/api/order-history`, `/api/equity-curve`, `/api/portfolio-metrics`. Plus `/api/strategies`, `/api/deployments`, `/api/deployments/active`, `/api/accounts`, `/api/accounts/{id}/strategy`, `/api/active-bots`.
- Frontend `AITradingDashboard.tsx` has `normalizeApiScope()` (maps `"all"` → unscoped request) and a selector labeled "All bots" fed by `/api/active-bots`.
- Tests: `tests/test_strategy_deployments.py`, `tests/test_dashboard_truth_metrics.py`, `tests/test_equity_data_extractor_scope.py`, `tests/test_db_manager_strategy_scope.py`, `tests/test_order_derived_equity_curve.py`, `tests/test_frontend_production_dashboard.py`.

Live VPS deployment config (verified via `/api/deployments` + container env):

| deployment_id | account_id | strategy | key env | configured |
|---|---|---|---|---|
| trend-paper | alpaca-paper-trend | trend | `PAPER_ALPACA_API_KEY_TREND` | true |
| ml-paper | alpaca-paper-ml | ml | `PAPER_ALPACA_API_KEY` ⚠️ generic | true |
| hybrid-paper | alpaca-paper-hybrid | hybrid | `PAPER_ALPACA_API_KEY_HYBRID` | true |

### The three truth gaps this plan closes

1. **"All" is not cumulative.** Unscoped endpoints return `capital_model: legacy_global` served by the single process-wide broker client (`PAPER_ALPACA_API_KEY` account). "All" today = one account, not Trend+ML+Hybrid summed.
2. **ML shares credentials with the legacy global client.** `ml-paper` points at the generic env pair, so "ML Account" and "legacy global" are the same Alpaca account, and that account's history contains old mixed-strategy trading. ML's "performance" is not attributable.
3. **Silent fallback fakes separation.** `_broker_for_deployment()` (backend/main.py:289) returns the shared `_broker_client` whenever a deployment's env vars are missing — a scoped view can silently display another account's numbers as if they were that strategy's.

Also verified: `/api/active-bots` returns `profit: "+0.00", trades: 0` placeholders from empty local scoped trades instead of per-account broker values.

---

## Design decisions

- **D1 — Strict scoping (always on, per Decision 4).** A scoped request (`deployment_id`/`account_id`) must be served by that deployment's own configured credentials or fail loudly (HTTP 424 `failed_dependency` with a clear reason). Never silently substitute the shared client. No fallback escape hatch exists — no `allow_shared_fallback` param, no disable flag.
- **D2 — Dedicated per-strategy accounts (all fresh, per Decision 1).** `PAPER_ALPACA_API_KEY_TREND/_ML/_HYBRID` + secrets are the only Alpaca paper credentials. **The generic `PAPER_ALPACA_API_KEY` pair is already deleted from the local `.env` (Don Guapo, 2026-08-11)** — there is no legacy client to fall back to. Consequence: `financio_src/config.py` must stop hard-requiring the generic pair at import (it currently raises), and `backend/main.py`'s module-level `_broker_client = get_active_broker(...)` must become lazy/optional (`None` when no generic creds), with every unscoped code path handling `None` by directing callers to scoped/`scope=all` requests. The loader rejects deployments that name the generic pair (strict, always on).
- **D3 — "All" is server-side aggregation.** New aggregator fans out to each active deployment's broker client. Invariant: `totals.X == sum(accounts[].X)` exactly (computed from the same snapshot, in code — never two separate fetches). Accounts that fail to respond are EXCLUDED from totals and listed in `excluded_accounts[{account_id, reason}]` — a partial sum presented as a full sum is a lie.
- **D4 — Pie = broker account values.** "Piece of the pie" = each account's share of combined equity (donut), plus P&L contribution (day + total, signed bars), plus a return-% comparison panel (fair even when starting capital differs).
- **D5 — Combined equity curve.** Sum of per-account Alpaca portfolio histories aligned on a union of timestamps with per-account carry-forward of the last known value; each account joins the sum only after its first data point. Per-strategy curves ship alongside for overlay rendering.
- **D6 — Extensibility by configuration.** Frontend renders selector options, colors, pie slices, and overlays from `/api/deployments/active`. Adding strategy #4 = 1 registry entry + 2 env vars + 1 deployment JSON entry. A test proves it.
- **D7 — Reconciliation is a feature.** `/api/reconciliation` re-reads every account fresh from Alpaca and diffs against the aggregate snapshot, returning per-account `matches: bool` at $0.01 tolerance. A CLI script wraps it for manual/CI verification.

---

## Architecture note (confirmed with Don Guapo, 2026-08-11 — local-first)

Data tiers as they actually exist in this repo:

- **Redis (in-memory) = realtime tier.** Live signal bus: multibot publishes via `financio_src/multi_bot/communication.py` (`RedisBackend`/`CommunicationManager`), backend `/api/live-signals` consumes. Correct tool for streaming; unchanged by this plan. **Sizing (measured on VPS 2026-08-11):** 1.49 MB used / 2.81 MB peak after weeks of 54-bot production — payloads are pub/sub (no storage) + 1h-TTL signal history, so steady state is single-digit MB and a 256 MB allocation is ~90× headroom. Deploy-phase hardening: set `maxmemory 200mb` + `maxmemory-policy volatile-ttl` (currently unlimited/noeviction) so a TTL-less write bug can't grow unbounded. **Not shared with Delphi:** Delphi has its own Redis (arq persist queue) on its own VPS; sharing would put a network hop + cross-service blast radius on Financio's hot path to save megabytes. One Redis per service, loopback/compose-network only.
  - **Redis Cloud instance (2026-08-11):** Don Guapo spun up a managed Redis Cloud (redislabs, AWS us-east-1) server and put its endpoint in `.env` `REDIS_URL` + password in `REDIS_PASSWORD`. **Currently connected to nothing:** no code reads `REDIS_URL`/`REDIS_PASSWORD` (`RedisBackend` reads only `REDIS_HOST`/`REDIS_PORT`, supports no password/TLS), and `docker-compose.production.yml` hardcodes `REDIS_HOST=redis`/`REDIS_PORT=6379` in container environments, which override `.env`. Wiring it up would require: password+TLS support in `RedisBackend`, compose env pass-through instead of hardcodes, and accepting ~60–80 ms per-op latency Mac↔us-east-1 on the hot path. Recommendation: keep the Docker Redis for local dev; treat the cloud instance as the production-time candidate (managed Redis reachable from the VPS — us-east-1 is also nearer Hetzner-to-market paths than a laptop). Pending Don Guapo's call.
- **SQLite (on disk) = durable/slow tier.** Trades DB (`financio_trades.db`), backtest artifacts (`experiments/*.json`), agent data. This is the "slow data" store for local dev.
- **Alpaca API = truth tier.** Account equity/positions/orders; the validation source (Phase 3).
- **Supabase is DORMANT.** No backend Python references; frontend client exists but nothing imports it (`supabaseClient.ts` is an explicit "not used" stub). `SUPABASE_*`/`VITE_SUPABASE_*` env vars and the compose build args feed nothing. Decision: leave SQLite as the durable store for local dev; hosted DB (Supabase/Postgres or other) is a production-time re-evaluation. Phase 5 may delete the dormant frontend Supabase files + compose args + env template lines so the repo stops implying an unused tier.

Env state (local `.env`, names verified 2026-08-11): six per-strategy Alpaca vars present (`_TREND/_ML/_HYBRID` × key/secret), generic paper pair removed, `LIVE_ALPACA_*` present but unused in paper mode, `REDIS_*`/`DATABASE_URL`/`DB_FILE` present. `EXECUTE_TRADES` and `ACTIVE_BROKER` are not set locally — defaults apply (`ACTIVE_BROKER=alpaca`; execution gates stay off until explicitly enabled), which is the safe posture for local work.

## Phase 0 — Prerequisites (Don Guapo actions, before code ships)

### Task 0.1: ML account + capital (DECIDED 2026-08-11 — see Decisions section)

**Option A chosen: fresh, dedicated ML paper account.** Create a new Alpaca paper account (or reset an unused one), copy its keys into `PAPER_ALPACA_API_KEY_ML` / `PAPER_ALPACA_SECRET_KEY_ML`. ML starts with clean, attributable history. The old generic account becomes "legacy" — its mixed history stays out of strategy comparison entirely (Decision 3: hidden, not even read-only).

**Also decided: equalize starting capital** across the three strategy paper accounts (Alpaca paper account reset sets a chosen starting balance — same amount for all three; record it as `base_value` in deployment metadata). With equal bases, the equity-share pie and the return-% panel tell the same story.

### Task 0.2: Env changes on VPS (one-liners for Don Guapo; Virgil does not edit secrets)

- Local reference: `.env.vps.template` gains commented `PAPER_ALPACA_API_KEY_ML=` / `PAPER_ALPACA_SECRET_KEY_ML=` lines (code task, Phase 1).
- **VPS:** `printf 'PAPER_ALPACA_API_KEY_ML=<key>\nPAPER_ALPACA_SECRET_KEY_ML=<secret>\n' >> /opt/financio-v2/.env` (Don Guapo pastes real values; or Doppler equivalent if/when Financio migrates).
- **VPS:** update `FINANCIO_STRATEGY_DEPLOYMENTS` in `/opt/financio-v2/.env` so `ml-paper` uses `"api_key_env": "PAPER_ALPACA_API_KEY_ML", "secret_key_env": "PAPER_ALPACA_SECRET_KEY_ML"`.
- **VPS:** recreate backend+multibot after env change: `cd /opt/financio-v2 && docker compose -p financio-clean -f docker-compose.production.yml up -d backend multi-bot`

Verification (VPS): `curl -s http://localhost:8000/api/deployments | python3 -c "import json,sys; [print(d['deployment_id'], d['credentials']['api_key_env'], d['credentials']['configured']) for d in json.load(sys.stdin)['deployments']]"` → three rows, three distinct env names, all `True`.

---

## Phase 1 — Strict credential scoping (kill the silent fallback)

### Task 1.1: Loader-level distinct-credentials validation

**Files:** Modify `financio_src/strategy_deployments.py`; Test `tests/test_strategy_deployments.py`

**Step 1 — failing tests:**
```python
def test_active_deployments_require_dedicated_credential_env_names():
    # deployment with api_key_env=None → StrategyDeploymentError when strict
def test_active_deployments_reject_generic_env_pair_when_strict():
    # api_key_env="PAPER_ALPACA_API_KEY" → error mentions 'generic'
def test_two_deployments_sharing_env_names_rejected():
    # trend + ml both naming PAPER_ALPACA_API_KEY_TREND → error
def test_strict_validation_always_on():
    # no env flag can disable validation; generic pair rejected regardless
```
**Step 2:** Run `uv run pytest tests/test_strategy_deployments.py -q` → new tests FAIL.

**Step 3 — implement** `validate_deployment_credentials(deployments)` called unconditionally from `load_strategy_deployments_from_env()` (no flag, no grace window — Decision 4). Generic denylist: `{PAPER_ALPACA_API_KEY, PAPER_ALPACA_SECRET_KEY, LIVE_ALPACA_API_KEY, LIVE_ALPACA_SECRET_KEY, ALPACA_API_KEY, ALPACA_SECRET_KEY}`.

**Step 4:** tests pass. **Step 5:** commit `feat: enforce dedicated credential env names per strategy deployment`.

### Task 1.2: `_broker_for_deployment` strict mode + optional global broker

**Files:** Modify `backend/main.py` (~line 70 and ~line 289), `financio_src/config.py`; Test `tests/test_dashboard_truth_metrics.py` (extend), `tests/test_config_dotenv_loading.py` (extend)

**Context:** the generic paper key pair no longer exists in `.env` (Decision 1 update). Today `financio_src/config.py` raises at import without it and `backend/main.py:70` builds `_broker_client` at module level — the app won't even boot. This task makes the global client optional and the strict scoped path the only broker path.

**Step 1 — failing tests:**
- `config.py` imports cleanly with NO generic Alpaca keys when `FINANCIO_STRATEGY_DEPLOYMENTS` is set (per-deployment creds are the credential source).
- `config.py` still fails loudly when NEITHER generic keys NOR deployment credentials exist (no silent keyless boot).
- scoped call with unconfigured creds → raises `DeploymentCredentialsUnavailable`.
- unscoped (deployment=None) call with no generic creds → `_broker_client is None` and unscoped broker endpoints return HTTP 410 `{"error": "legacy_global_view_removed", "hint": "use scope=all or deployment_id"}` instead of crashing.

**Step 2 — implement:** `_broker_for_deployment(deployment)` → returns `(client, data_source)` tuple; raises when a deployment is given and its creds are absent/unusable — no fallback parameter exists. `_broker_client` becomes a lazy accessor that returns `None` without generic creds (never raises at import). Every scoped endpoint (`/api/dashboard-data`, `/api/portfolio-positions`, `/api/order-history`, `/api/equity-curve`, `/api/portfolio-metrics`) catches `DeploymentCredentialsUnavailable` → `HTTPException(424, detail={"error": "deployment_credentials_unavailable", "deployment_id": ..., "missing_env": [...]})`, and threads the returned `data_source` into responses (values: `deployment_broker`; `live_alpaca` only where a generic client actually exists during any transitional deploy).

**Step 3:** `uv run pytest tests/test_dashboard_truth_metrics.py -q` passes. Commit `feat: fail loudly when a scoped view lacks its own broker credentials`.

### Task 1.3: Env template + docs

Add `_ML` lines to `.env.vps.template` and `.env.template` with a comment block explaining the per-deployment naming convention (`PAPER_ALPACA_API_KEY_<STRATEGY_SUFFIX>`) and the reserved-for-legacy status of the generic pair. Commit.

---

## Phase 2 — Aggregation layer ("All" scope)

### Task 2.1: `backend/portfolio_aggregator.py` (pure logic + fan-out)

**Files:** Create `backend/portfolio_aggregator.py`; Create `tests/test_portfolio_aggregator.py`

**Response shape (spell it out; this is the contract):**
```json
{
  "scope": "all",
  "as_of": "2026-08-11T17:04:22Z",
  "capital_model": "one_strategy_per_account",
  "data_source": "aggregated_deployment_brokers",
  "totals": {
    "equity": 30119.42, "cash": 12000.11, "long_market_value": 18119.31,
    "unrealized_pnl": 240.87, "day_pnl": -13.02, "day_pnl_pct": -0.043,
    "total_return": 119.42, "total_return_pct": 0.398,
    "positions_count": 9, "accounts_count": 3
  },
  "accounts": [
    {
      "deployment_id": "trend-paper", "account_id": "alpaca-paper-trend",
      "strategy_id": "trend", "strategy_name": "Trend",
      "account_display_name": "Trend Account", "paper": true,
      "equity": 10050.00, "cash": 4000.00, "unrealized_pnl": 80.00,
      "day_pnl": 5.00, "total_return": 50.00, "total_return_pct": 0.5,
      "base_value": 10000.00, "positions_count": 3,
      "equity_share_pct": 33.37, "pnl_contribution_pct": 41.9,
      "data_source": "deployment_broker", "as_of": "..."
    }
  ],
  "excluded_accounts": [
    {"deployment_id": "x", "account_id": "y", "reason": "credentials_unavailable"}
  ],
  "warnings": []
}
```
Semantics: `total_return` = `equity - base_value` where `base_value` = earliest available portfolio-history base (fallback: Alpaca `account.last_equity` for day P&L; document each field's Alpaca source in the module docstring). `equity_share_pct` over included accounts only, sums to 100 ± 0.1. `day_pnl` = `equity - last_equity` per Alpaca.

**Step 1 — failing tests (fake broker clients, no network):**
```python
def test_totals_equal_sum_of_included_accounts():        # exact-sum invariant
def test_failed_account_excluded_and_listed_with_reason()
def test_equity_share_pcts_sum_to_100_over_included()
def test_empty_deployments_returns_zero_totals_and_warning()
def test_single_account_all_equals_that_account()
def test_fourth_fake_deployment_included_automatically()  # extensibility proof
def test_snapshot_cache_ttl_serves_cached_within_window()
```
**Step 2 — implement** `class PortfolioAggregator` with `async gather_snapshot(deployments) -> dict` using `asyncio.gather` over per-deployment `run_in_executor` broker reads (alpaca-py is sync), per-account timeout ~8s, TTL cache (default 15s, `FINANCIO_AGGREGATE_CACHE_TTL_S`) so one dashboard render doesn't multiply Alpaca calls.

**Step 3:** `uv run pytest tests/test_portfolio_aggregator.py -q` all pass. Commit `feat: portfolio aggregator with exact-sum invariant across strategy accounts`.

### Task 2.2: Wire `scope=all` into the API

**Files:** Modify `backend/main.py`; Test `tests/test_dashboard_truth_metrics.py` (extend)

- `/api/dashboard-data?scope=all` → aggregator snapshot + last-N scoped local trades across deployments, each row tagged `strategy_id`/`strategy_name`/`deployment_id`.
- `/api/portfolio-positions?scope=all` → merged positions, each row tagged with `strategy_id`, `account_id`.
- `/api/order-history?scope=all` → merge per-account normalized order pages (reuse existing normalization; fetch per-account with cap, merge, sort desc by submitted_at, then paginate the merged list server-side; each row gains `strategy_id`, `account_display_name`). Response keeps `total_orders/total_pages/has_next/has_prev`.
- `scope=all` combined with `deployment_id` → HTTP 400.
- Unscoped requests (no scope, no deployment) stay `legacy_global` for now and gain `"deprecation": "unscoped view will be removed after migration; use scope=all"`.

TDD as in Phase 1; commit `feat: scope=all aggregated dashboard, positions, and order history`.

### Task 2.3: Combined + per-strategy equity curves

**Files:** Modify `backend/order_equity_curve.py` or create `backend/aggregate_equity_curve.py` (follow where `/api/equity-curve` helpers live); Test `tests/test_aggregate_equity_curve.py`

Algorithm (from D5): per account, pull Alpaca portfolio history (reuse existing per-deployment path); normalize timestamps to epoch ms UTC; build union timeline; carry each account's last value forward between its points; an account contributes only from its first point onward; combined point = sum of contributing accounts, with `contributing_accounts` count on each point.

**Failing tests:** two-account alignment with different timestamps; later-start account joins without back-filling zeros before its first point (no fake history); carry-forward across gaps; `range` filtering anchored to latest curve point (reuse existing anchoring convention from `test_order_derived_equity_curve.py`); tz-aware/naive mixing normalized (known pitfall).

API: `/api/equity-curve?scope=all&range=30d` →
```json
{"scope": "all", "combined": [{"timestampMs": 0, "value": 0.0, "contributing_accounts": 3}],
 "per_strategy": {"trend": [...], "ml": [...], "hybrid": [...]},
 "source": "aggregated_alpaca_portfolio_history", "warnings": []}
```
Commit `feat: combined equity curve summed across strategy accounts with per-strategy overlays`.

---

## Phase 3 — Reconciliation (Alpaca is the validation)

### Task 3.1: `/api/reconciliation` endpoint

**Files:** Modify `backend/main.py` (+ small helper in `backend/portfolio_aggregator.py`); Test `tests/test_reconciliation.py`

For each active deployment: fresh (cache-bypassed) Alpaca read of `equity`, `cash`, `positions_count`, `open_orders_count` → compare with a simultaneously-built aggregate snapshot →
```json
{"as_of": "...", "tolerance_usd": 0.01,
 "accounts": [{"deployment_id": "trend-paper", "alpaca": {...}, "dashboard": {...},
               "delta_equity": 0.0, "matches": true}],
 "sum_check": {"dashboard_total_equity": 30119.42, "alpaca_sum_equity": 30119.42, "matches": true},
 "all_match": true}
```
**Failing tests:** matching fakes → `all_match true`; a $0.02 discrepancy → that account `matches false` and `all_match false`; one account erroring → present with `error` field and `all_match false` (an unverifiable account is a failed validation, not a skipped one).

### Task 3.2: `scripts/verify_dashboard_vs_alpaca.py`

CLI wrapper: calls the endpoint (`--base-url`, default `http://localhost:8000`), prints a per-account table + PASS/FAIL, exit code 0/1. Runnable on the VPS inside/next to the backend container. Smoke-test command documented in the script docstring. Commit `feat: reconciliation endpoint and verifier script — Alpaca as source of truth`.

---

## Phase 4 — `/api/active-bots` tells the truth

**Files:** Modify `backend/main.py` (~line 358); Test extend `tests/test_dashboard_truth_metrics.py`

Replace placeholder `profit: "+0.00"` with per-account broker values via the aggregator snapshot (cache makes this cheap): `profit` = day P&L, `profitPercent` = day P&L %, `totalReturn`/`totalReturnPct`, `equity`, `trades` = broker-side count where cheaply available, else local scoped count labeled `trades_source: "local_records"`. Null (never 0) when the account read fails, plus `dataSource: "deployment_broker" | "unavailable"`. Failing test: fake broker equity/last_equity → expected fields; broker error → nulls not zeros. Commit.

---

## Phase 5 — Frontend

### Task 5.1: API service types + calls

**Files:** Modify `dashboard/src/services/financioApiService.ts`

Add `scope?: 'all'` to `getDashboardData/getEquityCurve/getPortfolioPositions/getOrderHistory` params (serialize as `scope=all`); add `getReconciliation()`; add TS interfaces `AggregateTotals`, `AccountSlice`, `AggregateEquityCurve` mirroring Phase 2 shapes exactly.

### Task 5.2: Selector = strategies, driven by deployments

**Files:** Modify `dashboard/src/components/AITradingDashboard.tsx`

- Label "Strategy"; options: `All strategies` + one per `/api/active-bots` row (which is deployment-shaped), display `strategy_name` (`Trend`, `ML`, `ML + Trend`) with account name as secondary text. NO hardcoded strategy list anywhere.
- `normalizeApiScope`: `botId === "all"` → `{scope: 'all'}` (was: undefined/unscoped). Scoped values unchanged.
- Stable color map keyed by `strategy_id` from a palette array indexed by deployment order — new strategies get the next color automatically.

### Task 5.3: All view — cumulative + piece of the pie

**Files:** Modify `AITradingDashboard.tsx`; Create `dashboard/src/components/StrategyAllocationPanel.tsx`

When scope=all:
- KPI row from `totals` (equity, cash, day P&L, total return, unrealized P&L, positions, accounts).
- `StrategyAllocationPanel`: donut of `equity_share_pct` per strategy (label: "Equity share") + signed horizontal bars for day-P&L contribution + compact per-strategy return-% list (the fair comparison per D4). Tooltip per slice: equity, share %, day P&L, return %.
- Equity chart renders `combined` line + per-strategy overlay toggle (default: combined only), colors from the strategy color map, numeric time X-axis (`timestampMs`, `type="number"`, `scale="time"` — known pitfall).
- Trades/orders tables show a strategy badge per row (from row tags added in Task 2.2).
- If `excluded_accounts` non-empty → prominent warning banner naming the excluded strategy and reason. Cumulative numbers labeled "partial — excludes N account(s)".

### Task 5.4: Scoped view + failure states

Scoped selection keeps existing per-deployment fetches (already wired) — verify every panel (metrics, positions, orders, curve, trades) carries `deployment_id`, none silently unscoped. A 424 renders an explicit "Credentials for this strategy's account are not configured" state, never cached/other-account numbers. All aggregate fetches isolated with `.catch()` fallbacks so one failing panel can't blank the dashboard (known `Promise.all` pitfall).

### Task 5.5: Frontend tests + build

Extend `tests/test_frontend_production_dashboard.py` + `dashboard/src` tests: assert bundle/source contains `scope=all` serialization, "All strategies" option, no hardcoded strategy name arrays in the selector, no sample-price constants (mock-data pitfall). Build with same-origin API (`VITE_API_BASE_URL= VITE_WS_URL= npm run build` — Vite env-baking pitfall). Commands: `cd dashboard && npm test -- --run && npm run build`. Commit `feat: strategy selector with aggregate All view and allocation pie`.

---

### Task 5.6: Remove dormant Supabase tier (frontend + env)

Delete `dashboard/src/integrations/supabase/`, `dashboard/src/services/supabaseClient.ts`, the `VITE_SUPABASE_*` build args in `docker-compose.production.yml`/`docker-compose.full-stack.yml`, and the `SUPABASE_*`/`VITE_SUPABASE_*` blocks in `.env.template`; drop `@supabase/supabase-js` from `dashboard/package.json` if present. Failing test first: assert no `supabase` references remain in `dashboard/src` or compose files (extend `tests/test_frontend_production_dashboard.py`). Rationale: architecture note — tier is dormant, nothing imports it; durable local store is SQLite until a production-time re-evaluation. Commit `chore: remove dormant supabase tier`.

## Phase 6 — Deploy + live verification

1. Full local gate: `uv run pytest tests/test_strategy_deployments.py tests/test_portfolio_aggregator.py tests/test_aggregate_equity_curve.py tests/test_reconciliation.py tests/test_dashboard_truth_metrics.py tests/test_frontend_production_dashboard.py -q` → all pass; `python3 -m py_compile backend/*.py financio_src/*.py`.
2. Push `main`; Don Guapo completes Phase 0 env changes (if not already).
3. **VPS:** `cd /opt/financio-v2 && git pull && docker compose -p financio-clean -f docker-compose.production.yml up -d --build backend frontend`
4. **VPS live checks (each one-line):**
   - `curl -s 'http://localhost:8000/api/dashboard-data?scope=all' | python3 -m json.tool | head -40` → `capital_model: one_strategy_per_account`, 3 accounts, empty `excluded_accounts`.
   - `curl -s 'http://localhost:8000/api/reconciliation' | python3 -c "import json,sys; d=json.load(sys.stdin); print('all_match', d['all_match']); [print(a['deployment_id'], a['matches'], a['delta_equity']) for a in d['accounts']]"` → `all_match True`.
   - `python3 scripts/verify_dashboard_vs_alpaca.py` → PASS.
   - `curl -s 'http://localhost:8000/api/dashboard-data?deployment_id=trend-paper' | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['data_source'], d['metrics']['currentValue'])"` → `deployment_broker` + Trend account equity; repeat for `ml-paper`, `hybrid-paper` — three DIFFERENT equity values matching each Alpaca account.
5. Browser: `http://116.203.16.160/` hard-refresh — flip All → Trend → ML → ML + Trend; numbers change per account; pie sums to 100%; combined curve = sum of overlays. Don Guapo cross-checks any one account against the Alpaca web dashboard (the human validation step).

---

## Adding strategy #4 later (the "leave room" contract)

1. `financio_src/strategy_deployments.py`: one `StrategyDefinition` entry (id, display name, aliases).
2. Env: `PAPER_ALPACA_API_KEY_<NEW>` / `PAPER_ALPACA_SECRET_KEY_<NEW>` (new Alpaca paper account).
3. `FINANCIO_STRATEGY_DEPLOYMENTS`: one JSON entry.
4. Restart backend + multibot. Selector option, pie slice, overlay color, aggregation, reconciliation all appear automatically — guaranteed by `test_fourth_fake_deployment_included_automatically` and the no-hardcoded-strategies frontend test.

## Risks & mitigations

- **Alpaca rate limits (~200 req/min/account):** distinct keys per account get separate budgets; TTL cache (Task 2.1) bounds fan-out; reconciliation is on-demand only.
- **Unequal starting capital skews the pie:** pie is labeled "equity share"; return-% panel is the performance comparison; Phase 0 recommends equalizing.
- **Legacy history contamination:** resolved by the Task 0.1 decision; legacy account stays out of "All" either way (it has no active deployment).
- **Timezone/naive-datetime mixing** in merged curves/orders: normalize to epoch ms UTC at ingestion; regression-tested.
- **WebSocket pushes are account-blind today:** out of scope; panels poll (existing pattern). Note as follow-up.
- **Multibot execution unaffected:** it already routes account-scoped tasks from the same registry; Phase 1 strictness applies to it identically — verify its startup log `Loaded 3 active account-scoped strategy deployments` after env change.

## Decisions (Don Guapo, 2026-08-11)

1. **ML account — DECIDED: Option A.** Fresh dedicated paper account; ML history starts clean and attributable. The generic-key account is legacy only. **Update 2026-08-11: Don Guapo created fresh accounts for ALL THREE strategies** — Trend and Hybrid keys must also be swapped to the new accounts (their old account history is discarded along with the legacy account's). This supersedes "reset" language in Task 0.1: all three `_TREND`/`_ML`/`_HYBRID` env pairs get brand-new account keys, locally and on the VPS.
2. **Starting capital — DECIDED: equalize.** All strategy paper accounts reset to the same starting balance. (Pick the amount when creating/resetting the accounts; note it in `FINANCIO_STRATEGY_DEPLOYMENTS` metadata as `base_value` so return-% math has an anchor.)
3. **Legacy account — DECIDED: hidden.** Mixed history is tarnished; the legacy/global account appears nowhere in the dashboard once `scope=all` ships. Unscoped `legacy_global` responses remain only as deprecated compatibility during migration (Phase 2), then are removed.
4. **Strict mode — DECIDED: strict from day one.** `FINANCIO_STRICT_DEPLOYMENT_CREDENTIALS` is not needed as a user-facing toggle: strict is the only behavior. Loader rejects shared/generic/missing credential env names at startup; scoped requests without their own working credentials return HTTP 424; "All" excludes and names unreachable accounts. Task 1.1/1.2 scope change: drop the grace-period flag path and `test_strict_validation_off_by_default_env_flag`; replace with `test_strict_validation_always_on` (no env flag disables validation). The `allow_shared_fallback` query param (D1) is also dropped — no shared-fallback path exists at all.

## Definition of done

- Selecting any strategy shows only that account's Alpaca-backed data; selecting All shows sums that pass the exact-sum invariant and `/api/reconciliation` returns `all_match: true` against live Alpaca.
- No silent shared-client fallback anywhere; every payload carries honest `capital_model` + `data_source`.
- A 4th strategy can be added with zero dashboard code changes (test-proven).
- Full targeted pytest suite + frontend tests/build green locally and deployed; live curls in Phase 6 match Alpaca per-account values.
