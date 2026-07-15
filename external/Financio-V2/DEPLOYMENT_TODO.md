# Financio-V2 VPS Deployment — TODO

> Living checklist for the VPS packaging + production dashboard effort.
> Check items off (`[x]`) as soon as they are completed. Add discovered work as new unchecked items under the right section.

**Decisions (locked):**
- Broker: **Alpaca, live trading** (`TRADING_MODE=live`)
- Packaging: **Docker Compose** (bot + Morgans + Redis + backend + dashboard)
- Sentiment: **Morgans is REQUIRED** and runs as a sibling service — no TextBlob/native fallback
- Dashboard data: scalable for ~1000 users (Supabase Cloud for realtime/user data + FastAPI for trading data)
- **NO FALLBACKS** anywhere in the pipeline — fail fast and loud

---

## 1. Setup
- [x] Lock deployment decisions with Tali
- [x] Create this TODO document
- [x] Package todo-tracker skill

## 2. Pipeline audit
- [x] Sweep financio_src/ for fallback paths, silent excepts, mock data
- [x] Sweep backend/ and run_multi_bot_production.py
- [x] Identify hardcoded paths that break on a Linux VPS (~/projects/..., /Volumes/...)
- [x] Catalog env vars actually required at runtime

## 3. Dashboard audit
- [x] Find all placeholder/hardcoded values in dashboard/src
- [x] Identify duplicate live indicators and dead components
- [x] Map every displayed value to its real data source

## 4. Pipeline fixes (NO FALLBACKS)
- [x] Morgans bridge: required, hard-fail when data missing/stale (MorgansDataUnavailableError; 48h staleness via SENTIMENT_MAX_AGE_HOURS)
- [x] Remove TextBlob/native sentiment fallback path (enhanced_sentiment_service rewritten Morgans-only)
- [x] Broker locked to Alpaca; TRADING_MODE explicit; fail fast on missing keys (config.py, live_trading.py, backend)
- [x] Replace VPS-breaking paths with env-configured paths (backend/main.py, equity extractors, run_multi_bot, MORGANS_DATA_DIR everywhere)
- [x] Remove/convert silent except blocks in the trade path (Redis hard-fail, model class metadata required, PPO sizing explicit via POSITION_SIZER, ensemble FALLBACK path removed, sizing cold-start explicit)
- [x] Backend /api/live-signals returns real Redis-published signals (was hardcoded HOLD/0.75)
- [x] Startup validation in run_multi_bot_production.py (config, Morgans freshness, Redis) with non-zero exit

## 5. VPS package (Docker Compose)
- [x] docker-compose.vps.yml: bot, morgans, redis, backend, frontend (nginx reverse proxy, same-origin /api + /ws)
- [x] docker/Dockerfile.morgans (replaces broken Dockerfile.morgans-bot: wrong CMD file, unused OUTPUT_DIR; HOME symlink trick so Morgans needs zero code changes)
- [x] docker/Dockerfile.financio — single unified image for bot + backend (no torch/TF needed by the multi-bot path → small image)
- [x] Shared sentiment volume: ../shared_data → /shared_data (Morgans rw, bot/backend ro), MORGANS_DATA_DIR=/shared_data/stocks
- [x] .env.vps.template with every required var, no defaults for secrets
- [x] deploy-vps.sh (package + ship), healthchecks on all 5 services, restart policies, models bind-mounted (no rebuild to update models)

## 6. Dashboard production rework
- [x] Remove mock Flask api.py data path + 16 dead/mock components + mock services
- [x] Single live/connection indicator (driven by real /health poll + WS state)
- [x] Tabbed layout: Overview / Bots / Trades / Risk (AITradingDashboard rewrite)
- [x] Mobile-friendly: single-column mobile grids, wrapping TabsList
- [x] Every value real and verifiable; auth re-enabled (no hardcoded user); Supabase creds + API/WS URLs env-driven, throw if missing
- [x] equityCurveService / supabaseClient leftovers stubbed (mock data + localhost fallback removed)

## 7. Verification
- [x] `vite build` passes clean (4.6s, tsc --noEmit clean); no hardcoded creds in bundle
- [x] Python syntax checks on all 17 changed modules
- [x] Config fail-fast smoke tests: 5/5 pass (missing TRADING_MODE / live keys / sentiment keys rejected; live+paper key selection correct)
- [x] docker-compose.vps.yml YAML-validated (services, restart policies); deploy-vps.sh bash -n clean
- [x] Final placeholder sweep: zero real hits (remaining = shadcn CSS classes + Marketing-page animation)

---

## Discovered work
- [x] Dockerfile.bot was broken (Alpine + torch, wrong requirements path) — superseded by Dockerfile.financio
- [x] Dockerfile.backend baked dummy Alpaca keys + mock multi_bot stubs into the image — superseded by Dockerfile.financio (real modules, real keys)
- [x] .dockerignore strips model files from images — resolved by bind-mounting ./models instead of COPY
- [x] multibot-requirements.txt pinned pandas_ta==0.3.14b0 (breaks on numpy 2.x) — not needed by the multi-bot path; excluded from runtime image
- [x] backend /api/live-signals fabricated HOLD/0.75 signals — now reads real bot signals from Redis, 503 when feed is down
- [x] nginx conf missing /health, /active-bots, /summary, /trade-log, /bot-status proxy routes — added
- [ ] FUTURE: code-split the dashboard bundle (941 kB minified) via React.lazy if load time matters
- [ ] FUTURE: first live run — verify Morgans data freshness window (48h) suits the 6h stock-news cadence
- [ ] FUTURE: TLS for the frontend (certbot on host or Caddy/Traefik in front)
