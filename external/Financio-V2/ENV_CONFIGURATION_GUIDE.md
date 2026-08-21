# Financio-V2 Environment Configuration Guide

> **Revision: 2026-08-21 — Account-Scoped Credential Scheme.**
> This document SUPERSEDES the 2026-01-05 "unified .env" guide. The credential
> model changed in Financio-V2-clean: generic Alpaca keys with fallback chains
> are gone. If any doc, script, or troubleshooting note tells you to "set
> `ALPACA_API_KEY`" for paper trading, it is describing the old repo — do not
> follow it. Source of truth for the current scheme: `financio_src/config.py`,
> `financio_src/strategy_deployments.py`, and `.env.template` in
> `Financio-V2-clean`.

## The Credential Model (current)

### Principles

1. **Mode-specific keys only.** `TRADING_MODE` must be explicitly `paper` or
   `live` (no default — config.py refuses to guess for a trading system).
   - `paper` → resolves `PAPER_ALPACA_*` (falls back to generic `ALPACA_*` only
     if set — see below for why it shouldn't be).
   - `live` → resolves `LIVE_ALPACA_API_KEY` / `LIVE_ALPACA_SECRET_KEY`
     (generic `ALPACA_*` fallback permitted for live).
   - There is **no cross-mode fallback**: a live deployment can never silently
     pick up paper credentials, or vice versa.

2. **One broker account per strategy, dedicated credentials per account.**
   Each strategy runs against its own Alpaca paper account with its own key
   pair, named by convention:
   ```bash
   PAPER_ALPACA_API_KEY_ML        PAPER_ALPACA_SECRET_KEY_ML
   PAPER_ALPACA_API_KEY_TREND     PAPER_ALPACA_SECRET_KEY_TREND
   PAPER_ALPACA_API_KEY_HYBRID    PAPER_ALPACA_SECRET_KEY_HYBRID
   ```
   Generic `PAPER_ALPACA_API_KEY` / `PAPER_ALPACA_SECRET_KEY` are
   **deliberately left unset** in this scheme.

3. **`FINANCIO_STRATEGY_DEPLOYMENTS` is REQUIRED.** A JSON array in `.env`
   that maps each deployment to its account and credential env *names*:
   ```bash
   FINANCIO_STRATEGY_DEPLOYMENTS=[
     {"deployment_id":"trend-paper","account_id":"alpaca-paper-trend","strategy":"trend","status":"active","paper":true,"api_key_env":"PAPER_ALPACA_API_KEY_TREND","secret_key_env":"PAPER_ALPACA_SECRET_KEY_TREND"},
     {"deployment_id":"ml-paper","account_id":"alpaca-paper-ml","strategy":"ml","status":"active","paper":true,"api_key_env":"PAPER_ALPACA_API_KEY_ML","secret_key_env":"PAPER_ALPACA_SECRET_KEY_ML"},
     {"deployment_id":"hybrid-paper","account_id":"alpaca-paper-hybrid","strategy":"hybrid","status":"active","paper":true,"api_key_env":"PAPER_ALPACA_API_KEY_HYBRID","secret_key_env":"PAPER_ALPACA_SECRET_KEY_HYBRID"}
   ]
   ```
   (One line in the actual `.env`; shown wrapped here for readability.)
   `config.py` accepts dedicated keys **only through this map** — it checks
   that at least one *active* deployment's `api_key_env`/`secret_key_env`
   resolve to non-empty values.

4. **Validation invariants** (enforced at load, `strategy_deployments.py`):
   - One active strategy per broker account.
   - Active deployments must declare `api_key_env` and `secret_key_env`.
   - Credential env names must be **dedicated and distinct** — reserved/generic
     names (`ALPACA_API_KEY`, `PAPER_ALPACA_API_KEY`, …) are rejected inside
     the deployments map, and two active deployments may not share a name.
   - Strategy ids canonicalize through the registry: `trend`, `ml`, `hybrid`
     (aliases like "ML + Trend", "ensemble" resolve to these).

5. **Runtime pause/activate** (added 2026-08-21): the dashboard's bot toggle
   persists `deployment_status_overrides.json` (repo root; override path via
   `FINANCIO_DEPLOYMENT_STATUS_OVERRIDES_FILE`). The shared loader applies it
   on every load, so the API reflects toggles immediately; the trading engine
   (`run_multi_bot_production.py`) loads deployments at startup and picks up
   changes on its next restart/reload.

### The failure signature to recognize

```
ValueError: ❌ Missing Alpaca credential environment variables: ALPACA_API_KEY,
ALPACA_SECRET_KEY, PAPER_ALPACA_API_KEY, PAPER_ALPACA_SECRET_KEY
```

This happens **even when the dedicated per-strategy keys ARE set** if
`FINANCIO_STRATEGY_DEPLOYMENTS` is missing or empty — no map means no
deployments, so config.py falls back to demanding generic keys.

**Fix:** add/repair `FINANCIO_STRATEGY_DEPLOYMENTS` so every active entry's
`api_key_env`/`secret_key_env` name an env var that exists and is non-empty.
**Never** "fix" this by adding generic `ALPACA_API_KEY` / `PAPER_ALPACA_*`
keys — that reintroduces exactly the ambiguity this scheme removed.
(This exact incident occurred 2026-08-21.)

## Env Files & Loading Order

`financio_src/config.py` loads, in order (readable files only; never fails on
root-owned files — the Doppler/`virgil` VPS case):

1. `<repo root>/.env` — main config.
2. `financio_src/.env` — optional extras, does **not** override the root file.

Path overrides: `FINANCIO_DB_PATH` (trades SQLite), `FINANCIO_CONFIG_PATH`
(location of `config.py` for the risk-parameter writer; auto-resolves for both
`/app` container and local layouts).

## Other Active Variable Groups (unchanged in spirit from the unified era)

- **Backend/API**: backend on **:8001** (dev, `uvicorn main:app --port 8001`);
  `CORS_ALLOWED_ORIGINS` (unset → dev localhost list incl. :5173),
  `ALLOWED_HOSTS` (SET IN PRODUCTION), prod domain `financio.blaqdata.us`,
  frontend served on :8080 / same-origin behind nginx.
- **Dashboard (redesign, `dashboard/`)**: `VITE_API_BASE`
  (default `http://localhost:8001`; empty string = same-origin in prod),
  `VITE_API_TIMEOUT_MS` (default 20000). The old `VITE_SUPABASE_*` /
  `VITE_API_BASE_URL` build args belong to the legacy dashboard
  (`dashboard-legacy/`).
- **Profile (dashboard Profile tab)**: `FINANCIO_PROFILE_NAME`, `_TITLE`,
  `_LOCATION`, `_ABOUT`, `_AVATAR_URL` (optional; memberSince derives from the
  first recorded trade).
- **Risk management (active)**: `ENABLE_ENHANCED_RISK_MGMT`,
  `SL_ATR_MULTIPLIER` (3.5), `TP_ATR_MULTIPLIER` (4.5),
  `MIN_PROFIT_THRESHOLD` (0.015), `CONFIDENCE_THRESHOLD` (0.75). Editable at
  runtime via `POST /api/risk-parameters` (rewrites `config.py`).
- **Streaming/watchlist**: `current_tickers.txt` at repo root is REQUIRED
  (startup refuses to guess a watchlist); `SIMULATED_STREAM=true` serves
  random prices — dev only, never where customers can see it.
- **Trading engine**: `ROTATION_TICKERS`, `ACTIVE_BROKER`
  (`alpaca` default | `webull` + `WEBULL_*` vars), market-data keys
  (`ALPHA_VANTAGE_API_KEY`, `NEWSAPI_KEY`, optional `POLYGON_API_KEY`,
  Reddit/Twitter for sentiment).
- **Infra (Docker/VPS)**: `POSTGRES_*`/`DATABASE_URL`, `SUPABASE_*`,
  `REDIS_URL`/`REDIS_HOST`/`REDIS_PORT`, `TZ=America/Chicago`.

## Legacy / Historical (kept for context, not trading logic)

Still true from the 2026-01 audit: `INITIAL_BALANCE`, `RISK_TOLERANCE`,
`MAX_POSITION_SIZE`, `MAX_PORTFOLIO_RISK`, `MAX_DAILY_LOSS` are
analytics/visualization only — position sizing uses confidence buckets
(1–6 shares), not balance percentage. Implement balance-based sizing or drop
them from future templates.

## Security Practices (unchanged)

- `.env`, `.env.*` gitignored (templates excepted). Never commit real values.
- Rotate: Alpaca keys ~90 days; JWT ~6 months; DB passwords ~12 months.
- Distinct keys per environment (dev/staging/prod) and per strategy account.

## Verification Checklist

```bash
# 1) Map exists and parses
python3 -c "import json,re; t=open('.env').read(); \
print(json.loads(re.search(r'^FINANCIO_STRATEGY_DEPLOYMENTS=(.*)$',t,re.M).group(1)))"

# 2) Config imports (loads .env, validates deployments + credentials)
.venv/bin/python -c "from financio_src.config import ALPACA_API_KEY; print('✅ config OK')"

# 3) Backend up
cd backend && python -m uvicorn main:app --reload --port 8001
curl -s localhost:8001/api/deployments | python3 -m json.tool | head
```
