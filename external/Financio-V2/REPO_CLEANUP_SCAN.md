# Financio-V2 Repo Cleanup Scan — 2026-06-21
*Read-only diagnostic. No files were modified. Review before deleting anything.*

## Summary
- **19 empty/stub files** (12 zero-byte, 7 near-empty stubs; plus 4 macOS resource-fork noise files)
- **7 files with broken internal imports** (0 syntax errors; all errors are missing symbols or non-existent packages)
- **23 unused/unreferenced files** categorized by confidence

---

## Category 1 — Empty / Stub Files

### 1a. Truly Zero-Byte (0 bytes on disk)

| File | Notes |
|------|-------|
| `financio_src/model/trend_model.py` | Flagged by user — completely empty |
| `financio_src/model/risk_model.py` | Completely empty — placeholder |
| `financio_src/model/sentiment_model.py` | Completely empty — placeholder |
| `financio_src/model/meta_decider.py` | Completely empty — placeholder |
| `financio_src/trading/risk_manager.py` | Completely empty — placeholder |
| `financio_src/trading/trade_executor.py` | Completely empty — placeholder |
| `financio_src/backtesting/backtest_sentiment.py` | Completely empty |
| `financio_src/backtesting/simulate_trades.py` | Completely empty |
| `financio_src/features/macro_features.py` | Completely empty |
| `financio_src/features/sentiment_features.py` | Completely empty (separate from `financio_src/sentiment/sentiment_features.py` which has real code) |
| `dashboard/__init__.py` | Completely empty |
| `tests/__init__.py` | Completely empty — acceptable for pytest but zero-byte |

### 1b. Near-Empty / Comment/Stub Only

| File | Size | Content |
|------|------|---------|
| `dashboard/src/services/api.py` | 21 b | Single line: `# deleted - not used` — should be deleted |
| `financio_src/data/fetch_news.py` | 44 b | Single comment: `# (later) Pull news headlines, Twitter, etc.` — stub |
| `financio_src/meta/__init__.py` | 40 b | `# Auto-generated for module recognition` — no real exports |
| `financio_src/db/__init__.py` | 30 b | Only `from .manager import DBManager` — functional but minimal |
| `financio_src/backtesting/__init__.py` | 37 b | Only `from .backtest_price import backtest` — functional but minimal |
| `financio_src/analytics/__init__.py` | 45 b | `from rl_train import update_confidence_bucket` — functional but depends on sys.path (see Category 2) |
| `__init__.py` (root) | 120 b | Comment-only — no exports, no code |

### 1c. macOS AppleDouble Resource-Fork Files (not real Python)

These are binary macOS metadata files named `._<something>.py`. They are not Python source and will confuse any tool that globs for `*.py`:

| File | Size | Notes |
|------|------|-------|
| `financio_src/ensemble/._ensemble_trading_model.py` | 4096 b | AppleDouble metadata — not Python source |
| `financio_src/features/._enhanced_features.py` | 4096 b | AppleDouble metadata — not Python source |
| `financio_src/features/._volatility_features.py` | 4096 b | AppleDouble metadata — not Python source |
| `financio_src/meta/._modelEval.py` | 4096 b | AppleDouble metadata — not Python source |

---

## Category 2 — Files With Errors

**Syntax errors:** None. All 228 Python files (excluding `._` resource forks) pass `python3 -m py_compile` cleanly.

**Type-checker:** `mypy` and `pyright` were not available in the sandbox. Checks are manual import inspection only.

### Broken Internal Imports

| File | Error Type | Detail |
|------|-----------|--------|
| `retrain_synthetic_three_class.py` | Missing symbol | `from financio_src.config import SELECTED_TICKERS` — `SELECTED_TICKERS` does not exist in `financio_src/config.py`. Used on line 247 to iterate tickers. Will `NameError` at runtime. |
| `financio_src/utils/delete_test_trade.py` | Non-existent package | `from live_trading.config import DB_FILE` — `live_trading/` is only a logs directory with no Python package. Will `ModuleNotFoundError` at runtime. |
| `financio_src/meta/modelSelect.py` | Non-existent package | `from Shared.config import FEATURE_COLUMNS, XGB_PARAMS` — no `Shared/` directory exists anywhere in the repo. Old-style import from a prior project layout. |
| `financio_src/meta/metaUtils.py` | Bare/relative import | `from metaManager import run_and_log_trials, update_meta_model` — bare import; only works if script is run directly from the `meta/` directory. Breaks under package import. |
| `financio_src/meta/modelEval.py` | Bare import | `from config import FEATURE_COLUMNS, XGB_PARAMS` — bare import; does not resolve to `financio_src.config`. Old-style from a prior layout. |
| `financio_src/analytics/__init__.py` | Path-dependent import | `from rl_train import update_confidence_bucket` — works only when project root is on `sys.path`. If `financio_src` is imported as an installed package, `rl_train` won't resolve. The symbol exists; this is an import path concern, not a missing-symbol error. |
| `financio_src/multi_bot/` | Missing `__init__.py` | `financio_src/multi_bot/` is imported as a package (`from financio_src.multi_bot.integration import ...`) but has no `__init__.py`. Works in Python 3.3+ as a namespace package, but is fragile — any tool that checks for `__init__.py` will flag it, and some import machinery won't find it correctly across all environments. |

### Additional Structural Note

`financio_src/config.py` (a module file) **coexists** with `financio_src/config/` (a subdirectory containing `integration_config.py`). Python resolves `from financio_src.config import X` to the `.py` file, making `financio_src/config/integration_config.py` **unreachable** via any standard import path. The `integration_config.py` file can never be imported as `from financio_src.config.integration_config import ...` while `config.py` exists.

---

## Category 3 — Unused / Unreferenced Files

Confidence levels: **High** = zero references + no `__main__` + not in docker/shell; **Medium** = one or two mentions but not actual imports; **Low** = referenced only in comments/docs or adjacent scripts.

### Root-Level Scripts (never imported anywhere; are they needed as CLI entrypoints?)

| File | Confidence | Why Flagged |
|------|-----------|-------------|
| `pong_game.py` | High | Zero references. A stray pygame game file in a trading repo root. |
| `connect_supabase_local.py` | High | Zero references. One-off connection test, no imports by other files. |
| `supabase_pg_connect.py` | High | Zero references. Superseded by `backend/supabase_config.py`. |
| `supabase_db_manager.py` | High | Zero references. Standalone old DB manager, replaced by `financio_src/db/manager.py`. |
| `demo_multi_bot.py` | High | Zero references. Demo/prototype; production uses `run_multi_bot_production.py`. |
| `multi_bot_monitor.py` | High | Zero references. No docker CMD or shell script calls it. |
| `multi_bot_live_integration.py` | High | Zero references. Superseded by `financio_src/multi_bot/integration.py`. |
| `batch_retrain.py` | High | Zero references. Superseded by `batch_retrain_with_pipeline.py` and the `financio_src` retraining schedulers. |
| `batch_retrain_with_pipeline.py` | High | Zero references. No import or docker entrypoint references. |
| `financio_ticker_integration.py` | High | Zero references. No import, no docker entrypoint. |
| `add_sample_data.py` | High | Zero references. One-off data seeding script. |
| `migrate_sqlite_to_supabase.py` | High | Zero references. One-time migration; migration presumably complete. |
| `alter.py` | Medium | Zero Python imports. The word "alter" appears in 2 other files but only as English text (not a module import). One-off schema alteration; probably already run. |
| `synthetic_three_class_training.py` | High | Zero references. Superseded by `retrain_synthetic_three_class.py`. |
| `manual_three_class_training.py` | High | Zero references. One-off training script. |
| `update_model_attributes.py` | High | Zero references. No imports by other files. |
| `dashboard/src/services/api.py` | High | Self-documents deletion: file contains only `# deleted - not used`. |
| `dashboard/pong_game.py` | High | Zero references. Duplicate of root `pong_game.py` in wrong directory. |
| `enhanced_risk_trading.py` | Medium | Zero Python imports. Used as docker `CMD` in `docker/Dockerfile.bot` and `Dockerfile.trading-bot`. Keep if those Dockerfiles are still active. |

### Internal `financio_src` Modules (never imported outside their own file)

| File | Confidence | Why Flagged |
|------|-----------|-------------|
| `financio_src/config/integration_config.py` | High | Zero imports anywhere. Additionally unreachable via standard Python import because `financio_src/config.py` shadows the `config/` subdirectory. |
| `financio_src/db/dbInit.py` | High | Zero references by any other file. Standalone DB init script with `__main__` block; superseded by `DBManager.__init__()` auto-init. |
| `financio_src/utils/dbinit.py` | High | Zero references. Lower-case duplicate of `dbInit.py`, also never imported. |
| `financio_src/utils/delete_test_trade.py` | High | Zero references (plus broken import; see Category 2). One-off utility. |
| `financio_src/utils/send_test_trade.py` | High | Zero references. One-off utility script. |
| `financio_src/meta/` (entire directory) | High | The `__init__.py` has no real exports. None of the five files (`metaLearn.py`, `metaManager.py`, `metaUtils.py`, `modelEval.py`, `modelSelect.py`) are imported anywhere. Three have broken imports (see Category 2). These appear to be experimental/archived meta-learning code. |
| `financio_src/backtesting/backtest_sentiment.py` | High | Zero references. Also 0 bytes. |
| `financio_src/backtesting/simulate_trades.py` | High | Zero references. Also 0 bytes. |
| `rl_train/train_sizing_ppo.py` | High | Zero references. Alternative PPO trainer; not imported by any other module. |
| `scripts/prep_finetune_dataset.py` | High | Zero references. No docker entrypoint or shell script uses it. |
| `scripts/tp_sl_tuner.py` | High | Zero references. No docker entrypoint or shell script uses it. |
| `backend/check_db.py` | High | Zero references. One-off SQLite inspection script. Hardcodes `../live_trading/logs/financio_trades.db`. |
| `backend/live_equity_calculator.py` | High | Zero references from Python files, docker CMDs, or shell scripts. |
| `backend/modules/` | High | Directory exists with only `__pycache__` — empty placeholder package. |

---

## Caveats

1. **No type-checker available.** `mypy` and `pyright` were not installed in the sandbox. Import-error detection is manual grep-based inspection. Dynamic imports (e.g., `importlib.import_module(...)`, string-based plugin loading) are not caught.

2. **Dynamic/string imports not checked.** If any module is loaded via `importlib` or eval, it won't appear in grep results. The `quantum/backend.py` uses `importlib.util.find_spec` for optional dependencies — those are intentional.

3. **Docker entrypoints.** `enhanced_live_trading.py` is referenced as a docker `CMD` in `docker/Dockerfile.bot` and `docker/Dockerfile.trading-bot`. It is NOT called from Python imports. Do not delete without checking which docker services are still active. `enhanced_risk_trading.py` is categorized as Medium-confidence unused for the same reason.

4. **Root-level retrain scripts.** Multiple `retrain_*.py` scripts at root level (`retrain_individual.py`, `retrain_remaining_models.py`, `retrain_three_class_models.py`, `retrain_single_model.py`) have 1–2 name matches each — but those matches are in `OVERVIEW.md` or comments, not actual `import` statements. They are CLI runner scripts, not imported modules. They are excluded from Category 3 since they appear intentional as standalone entrypoints.

5. **`financio_src/meta/` warnings.** All five meta files have broken imports referencing old project layouts (`Shared.config`, bare `metaManager`, bare `config`). The whole directory appears to be archived experimental code that was never integrated into the current `financio_src` package structure.

6. **macOS `._` files.** The four `._*.py` AppleDouble files are macOS filesystem artifacts (resource forks). They are harmless on macOS but will confuse any Linux-based tool, CI system, or linter that globs for `*.py`. Remove them with `find . -name "._*.py" -delete` (or add a `.gitattributes` rule).

7. **`SELECTED_TICKERS` in `retrain_synthetic_three_class.py`.** This is a runtime error that will only surface when that script is executed. The variable simply doesn't exist in `financio_src/config.py`. The script iterates over it, so it will crash on the `for ticker in SELECTED_TICKERS:` line.
