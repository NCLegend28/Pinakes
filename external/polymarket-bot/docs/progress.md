# Project Progress

## VPS Deployment — Two-Service Architecture

### Overview

Redesigned the bot to run as two independent Docker services that communicate via WebSocket:

- **`polymarket-weather`** — headless scanner, runs the LangGraph pipeline, publishes live state over WebSocket on port 8765 (internal only)
- **`polymarket-dashboard`** — standalone FastAPI service, subscribes to the scanner's WebSocket and proxies state to browser clients on port 8766

```
┌─────────────────────────────────────────┐
│  VPS                                    │
│                                         │
│  ┌──────────────────────┐               │
│  │  polymarket-weather  │               │
│  │  - scan_loop()       │               │
│  │  - headless (no TTY) │               │
│  │  - WebSocket :8765   │  (internal)   │
│  └──────────┬───────────┘               │
│             │ ws://weather-bot:8765/ws  │
│  ┌──────────▼───────────┐               │
│  │  polymarket-dashboard│               │
│  │  - WS client→scanner │               │
│  │  - Proxies state     │               │
│  │  - Serves web UI     │──────────────►│ browser :8766
│  └──────────────────────┘               │
└─────────────────────────────────────────┘
```

---

### Code Changes

| File | Change |
|---|---|
| `src/polybot/config.py` | Added `HEADLESS`, `SCANNER_WS_URL`, `DASHBOARD_HOST`, `DASHBOARD_PORT` settings |
| `src/polybot/ui/dashboard.py` | Added `NullDashboard` — same interface as `Dashboard` but no Rich Live renderer, safe for headless VPS |
| `src/polybot/cli.py` | Uses `NullDashboard` when `HEADLESS=true`; added `run_dashboard()` entry point |
| `src/polybot/web/dashboard_service.py` | **New** — FastAPI app that consumes scanner WebSocket with auto-reconnect, re-broadcasts to browsers |
| `src/polybot/web/server.py` | Fixed `SyntaxWarning` on invalid escape sequences (`\s`, `\?`) in embedded JavaScript regexes |
| `pyproject.toml` | Added `websockets>=13.0` dependency, added `dashboard` script entry point |

### Deployment Files

| File | Purpose |
|---|---|
| `Dockerfile` | Single image used by both services |
| `docker-compose.yml` | Two services — `weather-bot` internal + `dashboard` public, shared volume for trade logs |
| `.env.weather.example` | Weather bot env template (`HEADLESS=true`, keys, scan config) |
| `.env.dashboard.example` | Dashboard env template (`SCANNER_WS_URL=ws://weather-bot:8765/ws`) |
| `docs/firewall-hetzner.md` | Full VPS setup guide (see below) |

### Firewall & VPS Setup Guide (`docs/firewall-hetzner.md`)

Covers the full path from a fresh Hetzner server to a running deployment:

1. Finding your public IP for the SSH allowlist
2. Hetzner server creation (Ubuntu 24.04, CX22)
3. Hetzner Cloud Firewall rules — network-level, outer gate (Layer 1)
4. UFW configuration — OS-level backstop (Layer 2) + Docker/UFW conflict explained
5. Full server setup walkthrough — Docker, uv, clone repo, env files, `docker compose up`
6. Optional nginx + Let's Encrypt for HTTPS

---

### Status

| Item | Status |
|---|---|
| Architecture design | Done |
| Code changes | Done |
| Dockerfile + docker-compose | Done |
| Hetzner server provisioned | Done |
| SSH access working | Done |
| `docker compose build` | Done |
| `docker compose up -d` | `weather-bot` crashing on startup — root cause TBD |
| Dashboard accessible in browser | Pending |
