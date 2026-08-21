# Dashboard API Contract & Data Provenance

> Financio-V2-clean · verified 2026-08-21 · companion:
> `scripts/verify_dashboard_endpoints.py` (run it any time to re-prove every
> check below against the live backend: `python scripts/verify_dashboard_endpoints.py`,
> add `--with-toggle` / `--with-recon` for the mutating and broker-read checks).

Every number the dashboard renders traces to one of three provenance classes:

- **BROKER** — read from Alpaca (account balances, portfolio history, orders,
  market data). Highest trust; independently checkable in the Alpaca console.
- **RECORDED** — rows Financio's engine wrote (trades SQLite DB, deployments
  registry, config.py risk values). Trust equals the engine's bookkeeping.
- **DERIVED** — arithmetic the adapter (`dashboard/src/api/http.ts`) performs
  over BROKER/RECORDED values: sums, cumulative series, ratios. No invented
  figures — every derivation is listed here.

## Method-by-method contract

### `getSummary(botId?)` → KPI strip, risk tab, profile totals
| Datapoint | Endpoint | Provenance |
| --- | --- | --- |
| equity | `/api/dashboard-data?scope=all` → `totals.equity` (or `metrics.currentValue` scoped) | BROKER — Σ fresh per-account balance reads (money quantized server-side) |
| equityChangePctSinceInception | same → `totals.total_return_pct` / `metrics.totalReturnPercent` | BROKER vs base_value (all) · **CAVEAT: scoped view computes vs hardcoded initial_balance=10000 in backend** |
| realizedPnl, winRate | `/api/trades` pnl column | DERIVED — Σ / ratio over RECORDED per-trade pnl (rows with pnl null/0 excluded as unclosed) |
| totalTrades | `/api/dashboard-data` → `total_trades` | RECORDED — deployment-scoped trade count |
| volumeTraded | `/api/trades` | DERIVED — Σ price×qty over RECORDED rows |
| daysLive | `/api/trades` | DERIVED — now minus first RECORDED trade time |
| maxDrawdownPct | `/api/risk-metrics` → `drawdown_pct` (all) / `metrics.maxDrawdown` (scoped) | DERIVED server-side — **CAVEAT: crude bases (stop-loss Σ vs 100k; realized-pnl walk vs 10k)** |
| activeBots / totalBots | `/api/deployments` | RECORDED — deployment registry (env + status overrides) |

### `getPerformanceSeries(botId?)` → performance chart
| Metric | Source | Provenance |
| --- | --- | --- |
| equity | `/api/equity-curve?range=all&scope=all` → `combined[].{timestampMs,value}` (scoped: `equity_curve[]`) | BROKER — Alpaca `get_portfolio_history` account equity (source tag `alpaca_portfolio_history`); scoped fallback chain: order-derived → local trades → live snapshot, each labeled in `equity_data_source` |
| pnl / gross | `/api/trades` | DERIVED — per-day cumulative Σ of RECORDED pnl / price×qty |
| fees | constant 0 | Commission-free execution; no fee column exists — displayed as $0, never estimated |

### `getSectors()` → sector rail
`/api/market/sectors` — BROKER market data: SPDR sector ETF snapshots via
Alpaca data API; `changePct` = daily close vs previous daily close; 60 s
server cache; sorted desc. Empty array (with `error`) when no market-data
credentials — UI renders the rail empty rather than failing.

### `getTicker()` → masthead marquee
`/api/streaming/prices` — BROKER stream cache (IEX feed). `changePct` =
(price − bar open)/open; 0 when only quote data (no open) is cached. Empty
outside market hours until the first bar arrives. If `SIMULATED_STREAM=true`
the prices are RANDOM — dev only.

### `getTrades(limit)` → recent activity + trades tab
`/api/trades` — RECORDED rows verbatim (time, ticker, action, price, qty,
pnl, strategy). DERIVED: gross = price×qty; fee = 0. Sorted desc client-side.

### `getOrders(limit)` → orders tab
`/api/order-history?scope=all&status=all&flatten=true` — BROKER order rows
verbatim. Status mapping: filled→FILLED, partially_filled→PARTIAL,
canceled/expired→CANCELLED, rejected→REJECTED, anything else→PENDING.

### `getBots()` / `toggleBot(id)` → bots tab
`/api/deployments` — RECORDED registry. Per-bot trades/winRate/realizedPnl:
DERIVED from `/api/trades` rows matched by deployment_id → account_id →
strategy (mirror of backend `_trade_matches_deployment`). Toggle: `POST
/api/deployments/{id}/toggle` persists `deployment_status_overrides.json`
(validated: one active strategy per account) — API view immediate, **trading
engine applies on next restart/reload**.

### `getRiskParams()` / `updateRiskParams()` → risk tab + dialog
`/api/risk-parameters` — RECORDED live values from `financio_src/config.py`
(SL 1.0–6.0×ATR, TP 1.5–8.0×ATR, minProfit 0.5–5%, confidence 50–95%; POST
rewrites config.py). dailyRiskUsed = `/api/risk-metrics.daily_exposure`
(Σ prices of open-position rows); dailyRiskLimit = `portfolio_base` —
**CAVEAT: display bound only, not an enforced limit**.

### `getUserProfile()` → profile tab
`/api/profile` — name/title/location/about from `FINANCIO_PROFILE_*` env;
memberSince DERIVED from first RECORDED trade date.

## Known caveats (accepted, not bugs)
1. Scoped `totalReturnPercent` and `maxDrawdown` use hardcoded bases
   (10000 / 100000) in the backend — fine for paper; fix before live claims.
2. Trades DB empty until the engine records fills → trades/winRate/realized
   P&L honestly show zero/empty while equity/orders/curve stay live.
3. Bot toggle affects the running engine only after its restart.
4. Order statuses new/accepted/pending_new/replaced/done_for_day render as
   PENDING (deliberate coarse bucket).

## Independent verification paths
- `python scripts/verify_dashboard_endpoints.py` — shape + cross-checks
  (Σ accounts == totals, curve tail ≈ live equity, counts agree, ranges valid).
- `--with-recon` → `/api/reconciliation`: cache-bypassed broker reads compared
  to the aggregate snapshot (`all_match: true` expected).
- Alpaca console: account equity and order history must match the dashboard's
  masthead equity and orders tab directly.
