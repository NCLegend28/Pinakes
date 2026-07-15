---
type: project
tags: [financio, algo-trading, deployment, vps, docker, project]
created: 2026-06-23
updated: 2026-07-07
status: active
---

# Project: Financio-V2

**Goal**: A production algorithmic trading platform — multi-bot trader (per-ticker XGBoost + ensemble), Morgans sentiment, FastAPI backend, React dashboard, Supabase auth — deployable to a VPS and scalable toward ~1000 customers.

**Repo**: `/Volumes/samsungT7/projects/Financio-V2` · **Siblings it depends on**: [[project-dependency-map|Morgans, shared_data]]

**Current phase (2026-07-07)**: VPS paper stack hardened — sentiment pipeline rebuilt around a Financio-exported watchlist (484→18 tickers), backend DB path bug fixed. Next: redeploy + observe a full Morgans cycle before TLS + domain + live.

---

## Milestone Log

*Reverse-chronological. One entry per milestone — what shipped, what it unblocked, what's next.*

### 2026-07-07 — Sentiment pipeline rebuilt: watchlist handoff, 484→18 tickers, dedup stages

**What shipped.** Four coordinated fixes across Financio-V2, Morgans, and shared_data, driven by production warnings (`Sentiment unavailable for QUBT/RGTI/IONQ/QBTS/MDAI… articles=0` and `Database file not found`):

- **Backend DB bug killed** — `backend/main.py` hardcoded a cwd-relative `../financio_src/logs/financio_trades.db`; in the container (cwd `/app`) that resolved outside the app, so the API never found the DB the bot was writing. Now respects `FINANCIO_DB_PATH` like the rest of the backend. Also fixed a latent schema bug: `log_trade()` INSERTs a `strategy` column `CREATE TABLE trades` never defined — first trade on a fresh DB would have failed. Added column + PRAGMA migration + `mkdir` for fresh volumes.
- **Watchlist handoff** — new `financio_src/watchlist_export.py` publishes `ROTATION_TICKERS` to `shared_data/stocks/active_watchlist.json` (atomic write) at bot startup; works for static and screener modes. Bot's shared_data mount flipped ro→rw in `docker-compose.vps.yml`.
- **Morgans ticker diet (484→18)** — `get_stocks_to_track()` now reads the watchlist (fail-loud if missing/stale >7d), reusing hand-tuned NewsAPI queries from the archived list. Root cause confirmed: 5 of the 18 traded tickers (QUBT, RGTI, IONQ, QBTS, MDAI) were never in Morgans' universe at all. Auto-discovery gated off by default (`TICKER_DISCOVERY_ENABLED`).
- **Bridge counting bug** — Financio's `combined` payload normalizer used `total_articles = reddit_mentions`, discarding news counts entirely (real ORCL payload: 127 Finnhub articles counted as 7). Now news + reddit with per-source counts preserved.
- **Staged pipeline in Morgans** — fetch (now parallel across sources) → sanitize (HTML/entity strip) → dedup (canonical URL + normalized headline, catches cross-source wire-story duplicates the old exact-match let through to be double-scored) → analyze. All 9 existing Morgans tests pass; E2E sim: 18/18 tickers accepted by `EnhancedSentimentService`, where the old code rejected payloads with <3 reddit mentions regardless of news volume.

**What it unblocked.** Every API budget now covers 18 tickers instead of 484 (~27× headroom per cycle); the traded tickers — including the five that starved — get sentiment every 6h cycle; the dashboard can finally read trade history; duplicate wire stories no longer skew sentiment scores.

**What's next.** Redeploy the VPS stack (`docker compose -f docker-compose.vps.yml up -d --build`), watch one full stock_news cycle to confirm all 18 `*_combined_latest.json` files land fresh, then resume the TLS + domain + live-mode path.

### 2026-06-23 — Full stack live on VPS (paper trading)

The entire Financio stack builds and runs on the VPS under `docker-compose.vps.yml` (redis · morgans · bot · backend · frontend/nginx). Path from "packaged" to "running" required clearing a chain of real deployment bugs:

- **Cross-arch frontend build** — `package.json` hardcoded `@rollup/rollup-linux-arm64-gnu` (Apple-Silicon artifact); removed it so rollup auto-selects the x64/musl binary. Added an `npm ci → fresh install` fallback in `Dockerfile.frontend` and a `chmod -R a+rX` so nginx can read assets off the exFAT-origin files.
- **Slim runtime image** — backend crashed on `import matplotlib` pulled transitively through `utils/__init__.py`; made `visualization` a lazy import so the trading path never needs plotting libs.
- **No-fallbacks guards firing correctly** — backend refused to start without `current_tickers.txt` (now baked into the image) and Morgans data; these are the intended fail-fast behaviors, not bugs.
- **Stale-key bug** — the Alpaca *data* websocket read raw `ALPACA_API_KEY` first, picking up a leaked live key from `financio_src/.env`; routed it through `config.py`'s mode-aware resolution so it uses the paper key like the trader does. Deleted the stale `.env` from the box.
- **Morgans on VPS** — `shared_data` needed `__init__.py` package markers and the volume needed `chown 1001` for the non-root container to write sentiment CSVs.
- **Fresh Supabase project** — migration applied via SQL editor; moved to the new `sb_publishable_` / `sb_secret_` API keys; fixed the doubled `/rest/v1/auth/v1` path (base URL only) and the auth Site URL (localhost → server IP).
- **Security** — `deploy-vps.sh` now ships via one multiplexed SSH connection, excludes all secrets from the package, verifies checksums, and has a `harden` command (ufw + fail2ban). Backend got env-driven CORS + `TrustedHostMiddleware`.

**Unblocked**: a real paper-trading validation run. **Next**: (1) paper day — confirm trades place, risk limits hold, Morgans data fresh; (2) firewall + TLS + domain; (3) flip `TRADING_MODE=live`.

### 2026-06-12 — Repo-wide path audit + no-fallback sweep

Audited every project for `Path.home()/'projects'` references that silently misroute on the external drive; converted to `Path(__file__).resolve()` anchoring across Financio, Morgans, shared_data, options, toolsHub, Redpill. Haiku sweep found + fixed 7 critical no-fallback/synthetic-data leaks (random simulated prices served by default, invented 0.5 confidence, fabricated bot state). See [[project-dependency-map]].

### 2026-06-11 — VPS packaging + enhancements

Built the Docker Compose VPS package, Telegram alerts, API rate-limit guards (`api_budget.py`), the weekly sector-conditioned tradeability screener + backtest harness, and the GCP fine-tune guide. Fine-tune analysis → [[wiki/sources/2026-06-11-llms-as-financial-annotators|annotation-first recommendation]]; design rationale → [[wiki/insights/sector-conditioned-screening-beats-static-universes]].

---

## Open threads

- Paper-run validation not yet completed (the gate before live).
- TLS + domain still pending — dashboard is plaintext HTTP on a publicly-scanned IP.
- Alpha Vantage free tier can't cover 18 tickers 4×/day — upgrade or drop (see RATE_LIMIT_AUDIT).
- ModernBERT sentiment model trained (macro-F1 ~0.66, label-quality-capped) — parallel A/B in Morgans pending.

## Related

- [[project-dependency-map]] — how Financio, Morgans, shared_data, options interconnect
- [[wiki/insights/sector-conditioned-screening-beats-static-universes]]
