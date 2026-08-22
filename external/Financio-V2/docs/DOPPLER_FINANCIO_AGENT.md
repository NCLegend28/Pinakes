# Financio Doppler setup for the nightly backtesting agent

The nightly agent is designed to run through Doppler on the VPS:

```bash
doppler run --project financio --config prd -- uv run python -m agent.run_nightly --skip-evolve
doppler run --project financio --config prd -- uv run python -m agent.run_nightly
```

## Required Doppler secrets/config values

Trading/account collection:

- `ALPACA_PAPER=true` for the agent until manually changed.
- `PAPER_ALPACA_API_KEY`
- `PAPER_ALPACA_SECRET_KEY`
- Optional legacy fallback: `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`
- Only use `LIVE_ALPACA_API_KEY` / `LIVE_ALPACA_SECRET_KEY` for agent collection if `ALPACA_PAPER=false` is intentional.

Digest:

- `DELPHI_BASE_URL`
- `DELPHI_API_KEY`
- `DELPHI_DIGEST_MODEL=hermes`

Strategist:

- `ANTHROPIC_API_KEY`
- `STRATEGIST_MODEL=claude-sonnet-4-6`
- `CLAUDE_BIN=claude`

Alerts:

- `AGENT_ALERT_CHANNEL=telegram`
- `TELEGRAM_ENABLED=true`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Splits/gates:

- `AGENT_TRAIN_START`
- `AGENT_TRAIN_END`
- `AGENT_VALIDATION_END`
- `AGENT_HOLDOUT_END`
- `GATE_MIN_SHARPE`
- `GATE_MAX_DRAWDOWN`
- `GATE_MIN_WIN_RATE`
- `GATE_MIN_TRADES`

Operational:

- `AGENT_ENABLED=false` until manual VPS smoke tests pass.
- `AGENT_DATA_DIR=agent_data`
- `FINANCIO_REPO=/opt/financio-v2`
- `MAX_MUTATIONS_PER_NIGHT=3`
- `AGENT_REJECTION_PAUSE_THRESHOLD=5`

## VPS service-user setup

Run as the service user that owns the repo:

```bash
doppler login
doppler setup --project financio --config prd
cd /opt/financio-v2
doppler run -- uv run python -m agent.run_nightly --skip-evolve
```

If using a Doppler service token instead of an interactive login, store it in a root-readable systemd EnvironmentFile or drop-in, not in git.

## Safety rule

Doppler makes secrets easier for agents, but it does not change the promotion rule: the agent may create paper-review branches only. Live deployment still requires human review and manual merge/deploy.
