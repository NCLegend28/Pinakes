# Financio Nightly Backtesting/Test-Agent Integration Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Integrate the provided `financio-agent` package into Financio-V2 so the VPS can run a nightly loop: collect telemetry/account data, summarize it, let a restricted strategist propose config-only backtest mutations, have a deterministic gatekeeper re-run validation/holdout backtests, and promote at most one paper-only branch for human review.

**Architecture:** Keep live trading untouched. The new agent runs as a separate host-level `systemd` oneshot/timer against the deployed repo, not inside the always-on trading containers. It can read telemetry and run backtests, but it never places orders and never auto-promotes live trading. Promotion means “create a git branch with a config diff”; Tali reviews/merges/deploys manually.

**Tech Stack:** Python 3.11, uv, SQLite, Alpaca SDK, httpx, Delphi OpenAI-compatible digest endpoint, Claude Code CLI strategist, deterministic Python gatekeeper, systemd timer on the Financio VPS.

---

## 2026-07-23 implementation/server-readiness notes

- Local integration has been implemented through Phase 5-prep: agent package landed, key defects fixed, tests added, Doppler-oriented systemd/docs added, and local targeted tests pass.
- Read-only VPS check found live stack at `/opt/financio-v2`, not `/opt/financio/Financio-V2`.
- Read-only VPS check found `/opt/financio-v2` is not currently a git repository, so the gatekeeper cannot create review branches there until deployment is changed to preserve/ship a git checkout.
- Read-only VPS check found `doppler`, `uv`, and `claude` are not installed on the VPS yet.
- Docker Compose labels confirm the active compose project working directory is `/opt/financio-v2` and `docker-compose.vps.yml`; services are up/healthy.

## What I found after unzipping

- User path was typoed. Archive found at: `/Volumes/samsungT7/projects/Financio-V2/files.zip`.
- Extracted to: `/Volumes/samsungT7/projects/Financio-V2/files_extracted/`.
- Top-level archive contains:
  - `AGENT_TODO.md`
  - nested `financio-agent.zip`
- Nested package contains:
  - `agent/config.py`
  - `agent/collect.py`
  - `agent/digest.py`
  - `agent/evolve.py`
  - `agent/gatekeeper.py`
  - `agent/report.py`
  - `agent/run_nightly.py`
  - `prompts/strategist.md`
  - `systemd/financio-agent.service`
  - `systemd/financio-agent.timer`
  - `pyproject.toml`
- Extracted agent Python files compile successfully with `python3 -m py_compile`.

## Important integration blockers to handle first

1. **Backtest CLI mismatch:** the agent expects `scripts/run_backtest.py --start ... --end ...` writing `experiments/backtest_*.json`; current repo has `run_backtests.py` at the repo root and `financio_src/screener/backtest.py`, but no `scripts/run_backtest.py` contract.
2. **Collector SQL bug:** `agent/collect.py` defines `fills` with 7 columns but inserts with 6 placeholders. This must be fixed before the first smoke test.
3. **Environment migration:** migrate the nightly agent to Doppler for VPS secrets/config. The systemd service should run `doppler run --project financio --config prd -- ...`; `.env.vps.template` remains a fallback/template for Compose and bootstrap documentation.
4. **Server path mismatch:** provided service uses `WorkingDirectory=/opt/financio`, while Financio deployment docs use `/opt/financio/Financio-V2` and memory also mentions `/opt/financio-v2`. Verify the live VPS path before installing the service.
5. **Git cleanliness:** gatekeeper aborts if the working tree is dirty. The local repo is currently very dirty; the server copy must be clean or the gatekeeper will refuse to run.
6. **Metric unit mismatch risk:** current backtest summaries use win rate as percent (`55.0`) while gatekeeper floors expect fraction (`0.55`). The new CLI contract must normalize units and have tests.

---

## Phase 0 — Safety and server posture

### Task 0.1: Confirm live server path and deployment mode

**Objective:** Verify where the Financio repo lives and whether it is clean without changing the VPS.

**Local command:**
```bash
ssh <financio-vps> 'pwd; hostname; ls -ld /opt/financio /opt/financio/Financio-V2 /opt/financio-v2 2>/dev/null || true'
```

**Server command:**
```bash
cd /opt/financio/Financio-V2   # adjust if discovery shows another path
git status --short -- ':!node_modules' ':!dashboard/node_modules' ':!files_extracted'
docker compose -f docker-compose.vps.yml ps
```

**Expected:** Financio stack exists, Docker Compose is the runtime, and the deployed repo is clean or has only known runtime artifacts.

### Task 0.2: Decide alert channel

**Objective:** Choose report channel before scheduling.

**Decision:** Prefer Telegram if that is already Financio’s alert path; otherwise use Discord from the package. Do not rely on Hermes TUI cron delivery.

**Files later touched:**
- `.env.vps.template`
- `agent/report.py` if replacing Discord with Telegram

---

## Phase 1 — Land the agent code locally, safely

### Task 1.1: Copy package into repo root

**Objective:** Move extracted package files into canonical repo locations.

**Files:**
- Create: `agent/`
- Create: `prompts/strategist.md`
- Create: `systemd/financio-agent.service`
- Create: `systemd/financio-agent.timer`
- Create: `proposals/.gitkeep`

**Command:**
```bash
cd /Volumes/samsungT7/projects/Financio-V2
cp -R files_extracted/financio-agent-unpacked/financio-agent/agent ./agent
cp -R files_extracted/financio-agent-unpacked/financio-agent/prompts ./prompts
cp -R files_extracted/financio-agent-unpacked/financio-agent/systemd ./systemd
mkdir -p proposals agent_data
```

**Verification:**
```bash
python3 -m py_compile agent/*.py
```

### Task 1.2: Add generated-output ignores

**Objective:** Prevent agent DBs/proposals/backtest artifacts from dirtying the repo every night.

**Modify:** `.gitignore`

**Add:**
```gitignore
# Financio nightly agent runtime artifacts
agent_data/
proposals/*.json
experiments/backtest_*.json
files_extracted/
._*
```

**Verification:**
```bash
git status --short -- agent prompts systemd .gitignore
```

### Task 1.3: Add dependencies to the main project

**Objective:** Make the agent runnable under Financio’s project environment.

**Modify:** `pyproject.toml`

**Ensure dependencies include:**
- `alpaca-py` — already present in Docker runtime requirements, not root `pyproject.toml` currently.
- `httpx` — already in Docker runtime requirements, not root `pyproject.toml` currently.

**Command:**
```bash
uv add alpaca-py httpx
```

**Verification:**
```bash
uv run python - <<'PY'
import alpaca, httpx
print('agent deps OK')
PY
```

---

## Phase 2 — Fix package issues before running

### Task 2.1: Fix fill insert placeholder count

**Objective:** Make `collect_alpaca()` able to write fills.

**Modify:** `agent/collect.py`

**Change:**
```python
"INSERT OR REPLACE INTO fills VALUES (?,?,?,?,?,?)"
```

to:
```python
"INSERT OR REPLACE INTO fills VALUES (?,?,?,?,?,?,?)"
```

**Test:** Create `tests/agent/test_collect.py` with a mocked Alpaca order and assert the `fills` row is persisted.

**Run:**
```bash
uv run pytest tests/agent/test_collect.py -v
```

### Task 2.2: Align agent Alpaca env with Financio mode-specific keys

**Objective:** Avoid accidentally reading live keys when running data-only/paper validation.

**Modify:** `agent/config.py`

**Behavior:**
- Prefer `PAPER_ALPACA_API_KEY` / `PAPER_ALPACA_SECRET_KEY` when `ALPACA_PAPER=true`.
- Prefer `LIVE_ALPACA_API_KEY` / `LIVE_ALPACA_SECRET_KEY` only if explicitly configured for non-paper collection.
- Still allow legacy `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` as fallback.

**Test:** `tests/agent/test_config.py`
- paper=true picks `PAPER_*`
- paper=false picks `LIVE_*`
- missing keys gives clear error before collector runs

### Task 2.3: Make reporting match Financio’s alert path

**Objective:** Use the channel Tali will actually read.

**Option A:** Keep package Discord report and add `DISCORD_WEBHOOK_URL` to `.env.vps.template`.

**Option B, preferred if Telegram is already enabled:** Replace/add a Telegram report sender using `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`, preserving concise Financio alert style.

**Test:** Mock `httpx.post` and assert a promoted branch report includes:
- verdict
- mutation names
- validation Sharpe/drawdown
- “paper only / human review required”

---

## Phase 3 — Implement the required backtest CLI contract

### Task 3.1: Add `scripts/run_backtest.py`

**Objective:** Provide the exact command the strategist and gatekeeper depend on.

**Create:** `scripts/run_backtest.py`

**Contract:**
```bash
uv run python scripts/run_backtest.py \
  --start 2024-01-01 \
  --end 2026-01-31 \
  --tickers AAPL,NVDA \
  --exit-window 5 \
  --tp 0.10 \
  --sl 0.005
```

**Output:** newest `experiments/backtest_YYYYMMDD-HHMMSS.json` with:
```json
{
  "start": "2024-01-01",
  "end": "2026-01-31",
  "tickers": ["AAPL", "NVDA"],
  "metrics": {
    "sharpe": 0.0,
    "max_drawdown": 0.0,
    "win_rate": 0.0
  },
  "total_return_pct": 0.0,
  "total_trades": 0,
  "per_ticker": []
}
```

**Unit rules:**
- `metrics.win_rate` is fraction `0.0..1.0`, not percent.
- `metrics.max_drawdown` is fraction `0.0..1.0`.
- `total_return_pct` may be percentage points, but must be consistent for baseline and mutation comparisons.

### Task 3.2: Add date filtering to the existing backtest path

**Objective:** Make `--start` / `--end` real, not cosmetic.

**Modify:** `run_backtests.py`

**Change:** extend `run_single_backtest()`:
```python
def run_single_backtest(ticker, data_limit=2000, exit_window=5, tp_pct=0.1, sl_pct=0.005, start=None, end=None):
    ...
    df = safe_fetch_price_data(ticker)
    if start:
        df = df[df.index >= pd.Timestamp(start)]
    if end:
        df = df[df.index <= pd.Timestamp(end)]
```

Handle timezone-aware vs naive indexes explicitly in the implementation.

**Test:** mock `safe_fetch_price_data()` with dates before/inside/after the window; assert only in-window rows are fed into feature generation.

### Task 3.3: Add aggregate metrics, especially max drawdown

**Objective:** Give gatekeeper all required metrics.

**Modify:** `scripts/run_backtest.py` or helper module.

**Implement:**
- aggregate total trades
- aggregate win rate fraction
- aggregate average Sharpe
- aggregate total return
- compute drawdown from cumulative trade returns if equity curve is unavailable

**Tests:**
- profitable trades produce positive return
- empty trades produce zeros and no crash
- win rate is `0.55`, not `55.0`

### Task 3.4: Verify CLI smoke run locally

**Objective:** Prove the contract works before wiring the agent.

**Command:**
```bash
TRADING_MODE=paper ENABLE_SENTIMENT_ANALYSIS=false \
uv run python scripts/run_backtest.py \
  --start 2026-03-01 --end 2026-05-01 \
  --tickers NVDA --exit-window 5 --tp 0.10 --sl 0.005
```

**Expected:** exits `0` and writes `experiments/backtest_*.json` with `metrics`, `total_return_pct`, and `total_trades`.

---

## Phase 4 — Harden the strategist/gatekeeper loop

### Task 4.1: Add gatekeeper tests

**Objective:** Make the deterministic safety layer trustworthy.

**Tests:** `tests/agent/test_gatekeeper.py`
- `_swap_dates()` forces validation/holdout dates even if the proposal command lies.
- dirty git tree returns `{"verdict": "aborted"}`.
- mutation below floors is rejected.
- eligible winner creates only `agent/proposal-YYYY-MM-DD` branch.

**Run:**
```bash
uv run pytest tests/agent/test_gatekeeper.py -v
```

### Task 4.2: Restrict strategist writable files

**Objective:** Ensure the Claude strategist cannot edit trading/execution code.

**Modify:** `prompts/strategist.md` and `agent/evolve.py`

**Policy:** allowed mutations only in:
- `financio_src/config.py`
- `financio_src/config_manager.py`
- optional strategy config files if later identified

**Add validation:** proposal `config_diff.file` must be on an allowlist before gatekeeper applies it.

**Test:** malicious proposal targeting `financio_src/trading/live_trading.py` is rejected before any write.

### Task 4.3: Add consecutive-rejection kill switch

**Objective:** Prevent endless overfitting attempts if the strategist produces bad proposals.

**Modify:** `agent/run_nightly.py` or new `agent/state.py`

**Behavior:**
- Store a rejection streak in SQLite.
- If 5 consecutive nights yield `no_promotion` / rejected proposals, run `--skip-evolve` mode and alert Tali.
- Reset streak when a winner is promoted or after manual acknowledgement.

---

## Phase 5 — Local end-to-end run

### Task 5.1: Data-only smoke test

**Objective:** Verify collector/digest/report does not crash with current env.

**Command:**
```bash
TRADING_MODE=paper \
ALPACA_PAPER=true \
ENABLE_SENTIMENT_ANALYSIS=false \
AGENT_DATA_DIR=agent_data \
uv run python -m agent.run_nightly --skip-evolve
```

**Expected:**
- SQLite created at `agent_data/financio_agent.sqlite3`
- tables exist: `fills`, `positions_snapshot`, `portfolio_history`, `bars`, `signal_events`
- report sends or cleanly skips if no webhook/token configured

**Verification:**
```bash
sqlite3 agent_data/financio_agent.sqlite3 '.tables'
```

### Task 5.2: Manual supervised evolve run

**Objective:** Run one complete agent loop with human review, not scheduled.

**Command:**
```bash
TRADING_MODE=paper \
ALPACA_PAPER=true \
ENABLE_SENTIMENT_ANALYSIS=false \
FINANCIO_REPO=/Volumes/samsungT7/projects/Financio-V2 \
uv run python -m agent.run_nightly
```

**Expected:**
- proposal JSON may or may not be created
- if created, gatekeeper re-runs validation/holdout
- if promoted, branch is `agent/proposal-YYYY-MM-DD`
- no live/paper orders are placed

---

## Phase 6 — VPS install, still manual

### Task 6.1: Ship code to VPS without starting timer

**Objective:** Deploy agent files but do not schedule yet.

**Local command:**
```bash
./deploy-vps.sh package
./deploy-vps.sh ship <user>@<financio-vps>
```

**Server command:**
```bash
cd /opt/financio/Financio-V2
uv sync
uv run python -m py_compile agent/*.py scripts/run_backtest.py
```

If `uv` is missing on the host:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Task 6.2: Install Claude Code CLI on VPS for strategist only

**Objective:** Enable headless config-proposal runs.

**Server command:**
```bash
node --version || sudo apt-get install -y nodejs npm
npm --version
npm install -g @anthropic-ai/claude-code
claude --version
```

**Secret boundary:** Tali sets `ANTHROPIC_API_KEY` in the server env file; do not paste/read the value.

### Task 6.3: Add agent values to Doppler

**Objective:** Make the agent configurable through Doppler so server agents do not need to read or edit `.env` files.

**Modify:** Doppler project/config, plus `.env.vps.template` as documentation fallback.

**Set in Doppler (`project=financio`, `config=prd` initially):**
```env
AGENT_ENABLED=false
AGENT_DATA_DIR=agent_data
AGENT_ALERT_CHANNEL=telegram
ALPACA_PAPER=true
DELPHI_BASE_URL=http://<delphi-host-or-tailnet>:8080/v1
DELPHI_API_KEY=<set in Doppler>
DELPHI_DIGEST_MODEL=hermes
ANTHROPIC_API_KEY=<set in Doppler>
STRATEGIST_MODEL=claude-sonnet-4-6
CLAUDE_BIN=claude
MAX_MUTATIONS_PER_NIGHT=3
AGENT_REJECTION_PAUSE_THRESHOLD=5
```

**Rule:** start with `AGENT_ENABLED=false`; enable only after manual smoke tests pass.

### Task 6.4: Patch systemd unit for actual VPS path and Doppler

**Objective:** Run host-level nightly job against the deployed repo with Doppler-injected secrets.

**Modify:** `systemd/financio-agent.service`

**Target shape:**
```ini
[Unit]
Description=Financio nightly backtesting/test agent
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=oneshot
User=virgil
WorkingDirectory=/opt/financio-v2
Environment=DOPPLER_PROJECT=financio
Environment=DOPPLER_CONFIG=prd
Environment=FINANCIO_REPO=/opt/financio-v2
Environment=PATH=/home/virgil/.local/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/usr/bin/env doppler run --project financio --config prd -- uv run python -m agent.run_nightly
TimeoutStartSec=3h
Nice=10
```

Doppler must be configured for the service user with `doppler login && doppler setup --project financio --config prd`, or via a root-readable service-token drop-in outside git.

### Task 6.5: Run VPS data-only smoke test

**Server command:**
```bash
cd /opt/financio-v2
doppler run --project financio --config prd -- uv run python -m agent.run_nightly --skip-evolve
sqlite3 agent_data/financio_agent.sqlite3 '.tables'
```

**Expected:** collector tables populate or fail with clear config/API errors; no strategist mutation occurs.

### Task 6.6: Run VPS full loop manually once

**Server command:**
```bash
cd /opt/financio-v2
doppler run --project financio --config prd -- uv run python -m agent.run_nightly
```

**Human review required:** read `proposals/YYYY-MM-DD.json`, gatekeeper report, and any `agent/proposal-*` branch before merging.

---

## Phase 7 — Schedule after manual approval

### Task 7.1: Install systemd unit/timer

**Server command:**
```bash
sudo cp systemd/financio-agent.service /etc/systemd/system/
sudo cp systemd/financio-agent.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now financio-agent.timer
systemctl list-timers financio-agent.timer
```

### Task 7.2: Verify first scheduled run

**Server command:**
```bash
journalctl -u financio-agent.service -n 200 --no-pager
systemctl status financio-agent.timer --no-pager
```

**Expected:** nightly report arrives in chosen channel and service exits cleanly.

---

## Phase 8 — Operating rules after launch

1. **No live auto-promotion.** The agent may only create paper-review branches.
2. **Human merge only.** Tali reviews proposal JSON, validation/holdout metrics, and branch diff before merge.
3. **Paper soak:** keep any promoted config on paper for at least 2 weeks with positive expectancy before considering live.
4. **Monthly split roll-forward:** update `SplitConfig` monthly so holdout remains out-of-sample.
5. **Track trial count:** include number of nightly mutations tried per strategy in the report to avoid best-of-N overfitting blindness.
6. **Pause on rejection streak:** after 5 consecutive rejected nights, stop evolve and alert.
7. **Before risky server changes:** verify backups/snapshot and current Docker health.

---

## Recommended implementation order

1. Commit plan only.
2. Copy agent files and add `.gitignore` protections.
3. Fix collector SQL bug.
4. Build and test `scripts/run_backtest.py` contract.
5. Add gatekeeper allowlist + tests.
6. Run local `--skip-evolve`.
7. Run local supervised full loop.
8. Ship to VPS without timer.
9. Run VPS `--skip-evolve`.
10. Run VPS full loop manually.
11. Install timer only after Tali approves first manual result.

## Definition of done

- `uv run pytest tests/agent -v` passes.
- `uv run python scripts/run_backtest.py --start ... --end ...` writes valid `experiments/backtest_*.json`.
- `uv run python -m agent.run_nightly --skip-evolve` creates/populates SQLite and reports or cleanly skips reporting.
- Manual full run cannot place orders and either produces no proposal or creates a paper-only branch.
- VPS timer is enabled only after manual smoke/full-loop verification.
