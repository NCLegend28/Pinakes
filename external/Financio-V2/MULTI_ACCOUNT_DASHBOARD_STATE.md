# Financio V2 — Multi-Account Strategy Dashboard (Phase 1 + 2 + 3 + 4 + 5)

Canonical state record. Updated only for real, verified, non-broken change (Pinakes covenant).

- Repo: `NCLegend28/Financio-V2` (`main`)
- Verified at commit: `788849b9` (pushed to `origin/main`)
- Capital model: **one strategy per broker account** (Trend / ML / ML+Trend), each with its own Alpaca paper account and dedicated credentials. No shared/global fallback for scoped or aggregated views.
- Verification: targeted suite `164 passed, 5 warnings` across
  `tests/test_strategy_deployments.py`, `tests/test_portfolio_aggregator.py`,
  `tests/test_aggregate_equity_curve.py`, `tests/test_reconciliation.py`,
  `tests/test_verify_dashboard_vs_alpaca.py`, `tests/test_dashboard_truth_metrics.py`,
  `tests/test_frontend_production_dashboard.py`, `tests/test_config_dotenv_loading.py`,
  `tests/test_strategy_routing.py`; Python compile passed; same-origin Vite production build passed.
  Each subtask cleared spec + code-quality + integration review before landing.

## Phase 1 — Strict credential scoping (DONE, verified)

Guarantee: a strategy account's numbers come from that account's own credentials, or the request fails loudly. A loud error beats a plausible wrong number.

- Active deployments loaded from `FINANCIO_STRATEGY_DEPLOYMENTS` must name **dedicated** credential env vars. Loader validation (`validate_deployment_credentials`) is unconditional — no bypass/escape-hatch flag.
- Credential env names must be strings, trimmed, non-blank, match `^[A-Za-z_][A-Za-z0-9_]*$`, be unique across active deployments (API-key and secret-key namespaces checked independently), and distinct from the reserved/generic denylist:
  `PAPER_ALPACA_API_KEY`, `PAPER_ALPACA_SECRET_KEY`, `LIVE_ALPACA_API_KEY`, `LIVE_ALPACA_SECRET_KEY`, `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`.
- Global/legacy broker is lazy + optional (never constructed at import; never raises at import when generic creds absent). Non-Alpaca providers (`ACTIVE_BROKER=webull`) preserved via `get_active_broker()`.
- HTTP contract on the five broker-backed endpoints:
  - Scoped view with missing/unusable dedicated credentials -> **424** with detail `{"error":"deployment_credentials_unavailable","deployment_id":"...","missing_env":[...]}`.
  - Unscoped view with no real global broker -> **410** `{"error":"legacy_global_view_removed","hint":"use scope=all or deployment_id"}` (no local fallback).
  - Unknown deployment/account -> **404** before broker resolution.
- Env templates (`.env.template`, `.env.vps.template`) document `_TREND`/`_ML`/`_HYBRID` naming: `PAPER_ALPACA_API_KEY_<STRATEGY_SUFFIX>` / `PAPER_ALPACA_SECRET_KEY_<STRATEGY_SUFFIX>`; generic pair reserved/legacy, forbidden in the deployment registry.

## Phase 2 — Aggregation layer ("All" scope) (DONE, verified)

Server-side fan-out across every active deployment's own broker. `scope=all` is a real sum of strategy accounts, never a single legacy account.

- `backend/portfolio_aggregator.py`: pure aggregation with **exact-sum invariant** (totals summed from the same snapshot as the account rows). Concurrent off-thread fan-out (`asyncio.gather` + `to_thread`) with per-account timeout (default 8s, `FINANCIO_AGGREGATE_PER_ACCOUNT_TIMEOUT_S`), TTL snapshot cache (default 15s, `FINANCIO_AGGREGATE_CACHE_TTL_S`, deployment-state-keyed, mutation-isolated).
- Failed / timed-out / unusable accounts are **excluded from totals AND disclosed** in `excluded_accounts` with sanitized reason codes plus a partial-data warning. A partial sum is never presented as a full sum.
- Money emitted as exact fixed-scale strings (e.g. `"123.45"`); responses strict-JSON safe (`allow_nan=False`); non-finite / malformed numeric inputs rejected. Day-P&L availability disclosed (no fake zeros when `last_equity` missing).
- `scope=all` wired into: `/api/dashboard-data`, `/api/portfolio-positions`, `/api/order-history`, `/api/equity-curve`.
  - `scope=all` combined with `deployment_id`/`account_id` -> **400**; unsupported scope value -> **400**.
  - Order history: per-account multi-page collection to a safe cap with honest truncation metadata (`order_history_truncated`, `truncated_accounts`, `total_orders_is_partial`, conservative `has_next`); UTC-normalized timestamp sorting; no duplicate ambiguous legacy strategy-only trades.
  - Equity curve: combined + per-strategy overlays; union timeline with carry-forward only after each account's first point (no synthetic pre-history); timestamps normalized to epoch-ms UTC; latest-point-anchored range filtering; `source: "aggregated_alpaca_portfolio_history"`.
- Rows tagged with `strategy_id`, `strategy_name`, `deployment_id`, `account_id`, `account_display_name`. A fourth strategy is picked up automatically from config — no hardcoded strategy list.

## Phase 3 — Reconciliation (Alpaca is the validation) (DONE, verified)

Guarantee: the dashboard's numbers are checkable against fresh broker truth on demand. An account that can't be verified is a FAILED validation, never a silent skip.

- `GET /api/reconciliation`: for each active deployment, a FRESH cache-bypassed strict-path broker read (equity, cash, positions_count, open_orders_count) is compared to a simultaneously-built aggregate snapshot (`PortfolioAggregator(cache_ttl_s=0, include_open_orders=True)`) at **$0.01 tolerance**. One shared `as_of` across both sides.
- Response: `as_of`, `tolerance_usd`, `accounts[{deployment_id, account_id, alpaca, dashboard, delta_equity, matches, error?}]`, `sum_check{dashboard_total_equity, alpaca_sum_equity, matches}`, `all_match`.
- Fresh reads run concurrently, each bounded by a per-account timeout (`FINANCIO_AGGREGATE_PER_ACCOUNT_TIMEOUT_S`, default 8s); a stalled broker becomes a `broker_snapshot_timeout` failure rather than hanging the request.
- Errored / timed-out / aggregate-excluded accounts carry a safe error code (`credentials_unavailable`, `broker_snapshot_unavailable`, `broker_snapshot_timeout`), `matches: false`, forcing `all_match: false`. No raw exception/secret text. Strict-JSON safe. Never touches the global/legacy broker.
- The aggregator change is a backward-compatible opt-in (`include_open_orders` off by default); exact-sum invariant, JSON safety, and TTL cache untouched.
- `scripts/verify_dashboard_vs_alpaca.py`: dependency-light stdlib-urllib CLI hitting `{--base-url}/api/reconciliation` (default `http://localhost:8000`, `--timeout`, `--json`). Prints a per-account table + sum-check + overall PASS/FAIL. **Exit 0 only when `all_match` is true**; any fetch failure (non-200, malformed/non-dict JSON, connection error, missing `all_match`) is a FAILED verification -> exit 1 with a clean one-line error (no traceback). Runnable on the VPS next to the backend container.

## Phase 4 — Active bots real per-account values (DONE, verified)

Guarantee: `/api/active-bots` no longer fabricates bot money metrics from local trade notionals when active deployments exist. The dashboard bot cards now reflect each deployment account's broker-backed aggregate row, or show honest nulls when the account is unavailable.

- `/api/active-bots` and `/active-bots` remain aliases; the endpoint is async and uses `PortfolioAggregator` with normal TTL cache behavior (not reconciliation's `cache_ttl_s=0`).
- Active deployments use the strict `_broker_for_deployment(deployment)` path only; no global/legacy broker fallback.
- Successful account rows emit numeric-or-null dashboard fields sourced from the aggregate account row:
  - `profit` = `day_pnl`
  - `profitPercent` = `day_pnl_pct`
  - `totalReturn` / `totalReturnPct`
  - `equity`
  - `dataSource: "deployment_broker"`
- Failed/excluded deployments still appear in the bot list with `profit`, `profitPercent`, `totalReturn`, `totalReturnPct`, and `equity` all `null`, plus `dataSource: "unavailable"`. No dropped strategies, no fake zeroes, no fake strings.
- `trades` remains the local scoped trade count and is explicitly labeled `trades_source: "local_records"`; identity fields (`id`, `name`, `accountId`, `deploymentId`, `strategy`, `strategyId`, status/isRunning/lastTradeTime) are preserved.
- Strict JSON safety is guarded: malformed, non-finite, and oversized finite numeric values (for example `"1e309"`) become `null`, never `NaN`/`Infinity`.
- Zero active deployments keep the legacy SQL grouped-by-strategy branch and do not touch the aggregator.

## Phase 5 — Frontend aggregate strategy dashboard (DONE, verified)

Guarantee: the React dashboard's `All strategies` view now requests the real multi-account aggregate backend (`scope=all`) and presents partial-data states honestly. The frontend no longer carries the dormant Supabase tier.

- `dashboard/src/services/financioApiService.ts` supports `scope?: "all"` and serializes `scope=all` for `/api/dashboard-data`, `/api/equity-curve`, `/api/portfolio-positions`, and `/api/order-history`, while preserving `deployment_id` / `account_id` scoped params. It also exposes `getReconciliation()` and aggregate response interfaces for the dashboard.
- `AITradingDashboard.tsx` maps selector `botId === "all"` to `{scope: "all"}` — never legacy unscoped. Strategy-specific selections remain deployment/account scoped; HTTP 424 surfaces as `Credentials for this strategy's account are not configured` instead of showing another account's cached numbers.
- Selector copy is `Strategy` / `All strategies`; options come from `/active-bots` deployment-shaped rows, displaying strategy and account names. There is no hardcoded Trend/ML/Hybrid selector array; a fourth deployment gets the next palette color automatically.
- All view KPIs use aggregate `totals` fields: equity/current value, cash, day P&L, total return, unrealized P&L, positions, and account count. Partial sums are labeled when accounts are excluded.
- New `StrategyAllocationPanel` renders equity share, signed day-P&L contribution, and return-% by strategy account from aggregate account rows (`equity_share_pct`, `pnl_contribution_pct`, `total_return_pct`, `equity`, `day_pnl`).
- Aggregate equity chart renders the combined line by default, with a per-strategy overlay toggle. It uses `timestampMs` with Recharts numeric time axis (`type="number"`, `scale="time"`) so range changes are visually meaningful.
- Trades and orders show strategy badges in All view using backend row tags. `OrderHistoryTab` receives the active API scope (`scope=all`, `deployment_id`, or `account_id`) and no longer silently calls unscoped order history.
- Aggregate optional panels use `.catch()` fallbacks so a failable side panel cannot blank the core dashboard.
- Dormant Supabase frontend/env tier removed:
  - `dashboard/src/integrations/supabase/` and `dashboard/src/services/supabaseClient.ts` deleted.
  - `@supabase/supabase-js` removed from `dashboard/package.json` and lockfile.
  - `VITE_SUPABASE_*` compose build args and `SUPABASE_*` / `VITE_SUPABASE_*` template blocks removed.
  - Source tests assert no Supabase references remain in `dashboard/src`, compose files, env template, and dashboard package files. Durable local store remains SQLite until production-time re-evaluation.
- Same-origin Vite production build verified with explicit blank overrides: `VITE_API_BASE_URL= VITE_WS_URL= npm run build`.

## Not yet done

- Phase 6 — Deploy + live verification.
