# Repository Guidelines

## Project Structure & Module Organization
The `files/` directory is the working root; Python entry points sit alongside documentation. `squeeze_hunter.py` hosts `SqueezeHunterSystem` and wires the Reddit (`reddit_squeeze_monitor.py`), Alpaca (`premarket_monitor.py`), and Discord (`discord_alert_bot.py`) modules, while `start.py` performs deployment checks before spawning the async loop. Backtesting lives in `backtest_engine.py`, dependencies in `requirements.txt`, and high-level docs in `README.md`, `QUICK_START.md`, and `TECH_SPEC.md`. Runtime artifacts such as `config.json` and `signal_history.json` are generated beside these files and must stay out of version control.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate`: keep dependencies isolated before installing requirements.
- `pip install -r requirements.txt`: installs praw, alpaca-py, discord.py, and other pinned dependencies.
- `python squeeze_hunter.py`: creates `config.json` on first launch and can run the orchestrator directly for debugging.
- `python start.py`: preferred production entry point; performs file, dependency, and credential checks before calling `asyncio.run`.
- `python backtest_engine.py`: replays historical squeezes and produces summary stats for regression checks.

## Coding Style & Naming Conventions
Code uses Python 3.9+, four-space indentation, and docstrings that describe method intent, arguments, and side effects. Keep module-level functions and methods in `snake_case`, classes in `PascalCase`, and constants uppercased; mirror existing type annotations and explicit Dict/List typing seen in `squeeze_hunter.py`. Favor small, composable async coroutines, and guard network calls with clear logging so Discord and Alpaca events remain traceable.

## Testing Guidelines
Treat `python backtest_engine.py` as the fast regression harness; capture before/after metrics (detection rate, average gain) whenever scoring logic or thresholds change. When touching individual modules, run them with representative CLI arguments or inject fake data via dependency seams to avoid hitting live APIs. Validate that `start.py` passes all four pre-flight checks and that new alert formats still render in Discord’s embed schema. Automated unit tests are not present yet, so document manual test cases in the PR body until a pytest suite is added.

## Commit & Pull Request Guidelines
This export omits `.git`, but upstream history follows short, imperative summaries grouped by subsystem (e.g., `feat: tighten combined signal threshold`). Keep commits scoped to one concern, reference related scripts in the body, and never include secrets or generated files. PRs should describe the motivation, outline configuration impacts, attach logs or screenshots of alerts/backtest output, and link to any tracking issues. Highlight testing performed, note any follow-on work, and request reviews from teammates responsible for the touched module.
