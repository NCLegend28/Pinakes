# HANDOVER — Financio Multi-Account Strategy Dashboard (planning → implementation)

**Date:** 2026-08-11 · **From:** Virgil (planning session, TUI) · **Status:** PLAN COMPLETE, NO CODE WRITTEN

## What this session did

Read-only audit of local repo + live VPS, then produced the implementation plan:

- **Plan (canonical):** `docs/plans/2026-08-11-multi-account-strategy-dashboard.md` (this repo)
- Copy at `~/.hermes/plans/2026-08-11_170000-financio-multi-account-strategy-dashboard.md`

No files outside `docs/plans/` were modified. No deploys, no restarts, no env changes, no orders.

## The ask (from Don Guapo)

Each strategy (Trend, ML, ML + Trend) gets its own Alpaca account. Dashboard strategy selection shows that account's data; an "All" selection shows cumulative data plus each strategy's piece of the pie. Data must be coherent and factual — **Alpaca is the validation**. Leave room for more strategies. Plan only, no implementation.

## Verified starting state (2026-08-11)

- Local `/Volumes/samsungT7/projects/Financio-V2-clean` on `main` @ `b4e4694c` == GitHub `main` == VPS `/opt/financio-v2`. All containers healthy.
- 3 active deployments live (`/api/deployments`): trend-paper, ml-paper, hybrid-paper; scoped endpoints + registry already exist.
- **Truth gaps found (drive the whole plan):**
  1. Unscoped/"All" today = `legacy_global` single shared Alpaca account, NOT a sum of the three strategy accounts.
  2. `ml-paper` uses the generic `PAPER_ALPACA_API_KEY` pair → "ML Account" IS the legacy mixed-history account; not attributable.
  3. `_broker_for_deployment()` silently falls back to the shared client when per-deployment creds are missing → scoped views can show another account's numbers.
  4. Minor: `/api/active-bots` returns placeholder `profit "+0.00" / trades 0` instead of per-account broker values.

## Plan shape (6 phases, TDD)

0. **Don Guapo prerequisites:** dedicated ML Alpaca account + `PAPER_ALPACA_API_KEY_ML`/`_SECRET_KEY_ML` env, update `FINANCIO_STRATEGY_DEPLOYMENTS`, recreate backend+multibot.
1. Strict credential scoping — loader rejects generic/shared env pairs; scoped views 424 instead of silent fallback.
2. Aggregation layer — `backend/portfolio_aggregator.py`, `scope=all` on dashboard-data/positions/order-history, combined+per-strategy equity curves. Exact-sum invariant; failed accounts excluded AND listed.
3. Reconciliation — `/api/reconciliation` + `scripts/verify_dashboard_vs_alpaca.py` diff dashboard vs fresh Alpaca reads ($0.01 tolerance).
4. `/api/active-bots` real per-account values (nulls on failure, never fake zeros).
5. Frontend — "All strategies" selector driven by deployments (no hardcoded strategy lists), StrategyAllocationPanel (equity-share donut + P&L contribution + return-% comparison), combined curve with overlays, 424/excluded-account states.
6. Deploy + live verification (exact curls in plan §Phase 6).

## Decisions from Don Guapo (2026-08-11, via TUI — Telegram replies weren't reaching the agent)

1. ML account: **DECIDED — Option A**, fresh dedicated paper account. **Update: fresh accounts created for ALL three strategies** (Trend/ML/Hybrid) — all six `_TREND`/`_ML`/`_HYBRID` key env vars get new values; old per-strategy account history is discarded. Don Guapo is placing keys in `Financio-V2-clean/.env` (root `.env` is the ONLY env file the clean repo uses — no `.env.docker`; compose `env_file: .env` + dotenv both read it). Old `Financio-V2` folder will be retired after verification.
2. Starting capital: **DECIDED — equalize** across all strategy paper accounts (amount picked at account creation; record as `base_value` in deployment metadata).
3. Legacy/global account: **DECIDED — hidden.** Mixed data is tarnished; it appears nowhere on the dashboard.
4. Strict mode: **DECIDED — strict from day one.** No disable flag, no `allow_shared_fallback`; loader validation always on, scoped views 424 on missing creds.

## For the next session (kickoff instruction)

Load skills `subagent-driven-development`, `test-driven-development`, `trading-dashboard-integrations` (+ its `references/account-scoped-strategy-deployments.md`). Execute `docs/plans/2026-08-11-multi-account-strategy-dashboard.md` task-by-task starting at Phase 1 (Phase 0 is Don Guapo's; confirm env state first with the Phase 0 verification curl). Work in `/Volumes/samsungT7/projects/Financio-V2-clean` on `main` (or a feature branch if preferred), commit per task, do NOT deploy to VPS until the Phase 6 gate passes and Don Guapo approves.

## Guardrails (unchanged)

- Paper mode only; never touch/print secrets — Don Guapo edits `.env` values himself (one-line commands, local vs VPS labeled).
- Deploy command: `cd /opt/financio-v2 && docker compose -p financio-clean -f docker-compose.production.yml up -d --build backend frontend`.
- Never fabricate numbers; broker truth or explicit nulls/warnings.
