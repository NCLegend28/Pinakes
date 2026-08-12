# Financio V2 — Multi-Account Strategy Dashboard (Phase 1 + 2)

Canonical state record. Updated only for real, verified, non-broken change (Pinakes covenant).

- Repo: `NCLegend28/Financio-V2` (`main`)
- Verified at commit: `25e07d3f` (pushed to `origin/main`)
- Capital model: **one strategy per broker account** (Trend / ML / ML+Trend), each with its own Alpaca paper account and dedicated credentials. No shared/global fallback for scoped or aggregated views.
- Verification: targeted suite `126 passed, 5 warnings` across
  `tests/test_portfolio_aggregator.py`, `tests/test_aggregate_equity_curve.py`,
  `tests/test_dashboard_truth_metrics.py`, `tests/test_strategy_deployments.py`,
  `tests/test_strategy_routing.py`, `tests/test_config_dotenv_loading.py`.
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

## Not yet done

- Phase 3 — Reconciliation (`/api/reconciliation` + `scripts/verify_dashboard_vs_alpaca.py`, fresh cache-bypassed Alpaca reads diffed vs the aggregate snapshot at $0.01 tolerance).
- Phase 4 — `/api/active-bots` real per-account values.
- Phase 5 — Frontend (deployment-driven selector, allocation panel, combined curve overlays, 424/excluded states).
- Phase 6 — Deploy + live verification.
