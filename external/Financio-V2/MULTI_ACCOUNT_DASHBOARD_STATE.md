# Financio V2 — Multi-Account Strategy Dashboard (Phase 1 + 2 + 3 + 4 + 5 + 6)

Canonical state record. Updated only for real, verified, non-broken change (Pinakes covenant).

- Repo: `NCLegend28/Financio-V2` (`main`)
- Latest verified pushed commit: `04dbb7c2` (modernist frontend redesign, pushed to `origin/main`; not yet VPS-deployed)
- Current VPS deployed commit: `788849b9` (Phase 6 live deployment in `/opt/financio-v2`)
- Capital model: **one strategy per broker account** (Trend / ML / ML+Trend), each with its own Alpaca paper account and dedicated credentials. No shared/global fallback for scoped or aggregated views.
- Code verification: targeted suite `164 passed, 5 warnings` across
  `tests/test_strategy_deployments.py`, `tests/test_portfolio_aggregator.py`,
  `tests/test_aggregate_equity_curve.py`, `tests/test_reconciliation.py`,
  `tests/test_verify_dashboard_vs_alpaca.py`, `tests/test_dashboard_truth_metrics.py`,
  `tests/test_frontend_production_dashboard.py`, `tests/test_config_dotenv_loading.py`,
  `tests/test_strategy_routing.py`; Python compile passed; same-origin Vite production build passed.
  Each subtask cleared spec + code-quality + integration review before landing.
- Deployment verification: VPS backend/frontend rebuilt and recreated from `788849b9`; live `/api/reconciliation` verifier returned `overall: PASS`; public IP/domain `/health` and `scope=all` aggregate checks returned healthy three-account data.

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

## Phase 6 — VPS deploy + live verification (DONE, verified)

Guarantee: the pushed Phase 5 dashboard build is running on the VPS against real Alpaca paper account reads, and the aggregate dashboard total matches fresh broker truth.

- VPS checkout `/opt/financio-v2` fast-forwarded to `788849b9`; `backend` and `frontend` rebuilt/recreated with `docker compose -p financio-clean -f docker-compose.production.yml up -d --build backend frontend`.
- Runtime config was completed without exposing secrets:
  - dedicated credential names present for `PAPER_ALPACA_API_KEY_TREND` / `PAPER_ALPACA_SECRET_KEY_TREND`, `PAPER_ALPACA_API_KEY_ML` / `PAPER_ALPACA_SECRET_KEY_ML`, and `PAPER_ALPACA_API_KEY_HYBRID` / `PAPER_ALPACA_SECRET_KEY_HYBRID`;
  - `FINANCIO_STRATEGY_DEPLOYMENTS` added on the VPS to map `trend-paper`, `ml-paper`, and `hybrid-paper` to the dedicated env-var names;
  - `ALLOWED_HOSTS` updated for `116.203.16.160`, `financio.blaqdata.us`, and `www.financio.blaqdata.us` so public nginx/API routing passes host validation.
- Container health after deploy:
  - `financio-backend` healthy on `0.0.0.0:8000`;
  - `financio-frontend` healthy on `0.0.0.0:3000`;
  - nginx/redis/multi-bot remained running.
- Live API verification after config fix:
  - `/api/active-bots` returned 3 bots (`Trend`, `ML`, `ML + Trend`) with `dataSource: "deployment_broker"` and broker equity `10000.0` each.
  - `/api/dashboard-data?scope=all` returned `scope=all`, `capital_model=one_strategy_per_account`, `accounts=3`, `excluded=0`, `totals.equity="30000.00"`, `totals.cash="30000.00"`, positions `0`.
  - `/api/equity-curve?scope=all&range=30d` returned combined aggregate history plus 3 per-strategy overlays.
  - `/api/portfolio-positions?scope=all` returned `positions=0`, `excluded=0`.
  - `/api/order-history?scope=all&page=1&page_size=5&flatten=true` returned `orders=0`, `excluded=0`, `truncated=false`.
  - Scoped `dashboard-data`, `equity-curve`, and `order-history` checks passed for `trend-paper`, `ml-paper`, and `hybrid-paper`, all through `deployment_broker`.
- Live reconciliation CLI: `python3 scripts/verify_dashboard_vs_alpaca.py --base-url http://localhost:8000` returned `overall: PASS`; all three accounts matched broker equity (`10000.00` each), positions `0/0`, orders `0/0`, and sum-check dashboard total `30000.00` equaled Alpaca sum `30000.00` with delta `0.00`.
- Public route verification: `116.203.16.160`, `financio.blaqdata.us`, and `www.financio.blaqdata.us` all returned healthy `/health` and `scope=all` aggregate data (`3` accounts, `0` excluded, equity `30000.00`).
- Browser smoke: public dashboard loaded title `🐴 Financio Trading Dashboard`; selector shows `Strategy` / `All strategies`; visible Overview renders `$30,000` cumulative equity, `$30,000` cash, strategy allocation with three 33.33% slices, and aggregate equity chart. Served frontend bundle contains no stale `financio.blaqdata.us` hardcoded API base and no Supabase references.

## Modernist dashboard visual redesign (DONE in code, pushed; not yet deployed)

Guarantee: the frontend shell now uses the visual direction from `Dashboard redesign V2/` while preserving the Phase 5/6 broker-backed data flow and backend API contracts.

- Financio commit `04dbb7c2` (`feat: apply modernist dashboard redesign`) is pushed to `origin/main`; VPS production is still intentionally on `788849b9` until a separate deployment go-ahead.
- Frontend-only implementation touched `AITradingDashboard.tsx`, `StrategyAllocationPanel.tsx`, `index.css`, and frontend source-inspection tests. No backend files, credential loaders, API adapters, or deployment config were changed.
- Visual shell now matches the provided modernist trading-journal direction: light paper background, black editorial grid lines, oversized `Financio` masthead, red LIVE/accent state, uppercase label typography, square selectors/buttons, tab underline navigation, and bordered KPI/allocation panels.
- Existing backend/API behavior remains wired:
  - `All strategies` still maps to `scope=all`.
  - Strategy options still come from `/active-bots` deployment rows.
  - Dashboard, equity curve, positions, orders, active-bots, and trades requests are unchanged and still use scoped/aggregate backend endpoints.
  - No mock reference values from the design artifact are copied into production code.
- Verification before push:
  - RED source-inspection test failed before the redesign because `financio-modernist-shell` was absent.
  - `tests/test_frontend_production_dashboard.py tests/test_dashboard_truth_metrics.py -q` passed: `82 passed, 5 warnings`.
  - `VITE_API_BASE_URL= VITE_WS_URL= npm run build` passed.
  - `python3 -m py_compile tests/test_frontend_production_dashboard.py` passed.
  - `git diff --check` passed.
  - Local browser smoke through the Vite same-origin proxy to the live backend rendered the redesigned UI with real backend data: `$30,000` aggregate equity, 3 strategy accounts, `scope=all` dashboard/equity/positions calls, and the modernist masthead/allocation layout.

## Follow-ups / known non-blocking runtime notes

- Backend logs still show `AlpacaStreamer: Alpaca API credentials not configured`; dashboard broker reads and reconciliation pass through dedicated per-deployment credentials, but the market-data websocket path still appears to expect generic credentials or needs equivalent dedicated-config support.
- Backend logs show `Error reading trading data: no such table: trades`; this affects local trade-record display noise only. Broker-backed account totals, positions, orders, and reconciliation all passed with empty trade/order state.
