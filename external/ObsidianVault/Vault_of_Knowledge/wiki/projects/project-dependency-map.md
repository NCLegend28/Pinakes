---
type: project
tags: [architecture, dependencies, path-audit, delphi]
created: 2026-06-13
updated: 2026-06-13
status: active
---

# Project Dependency Map & Path Audit

## Delphi's Workspace

`/Volumes/samsungT7/projects/` is Delphi's home. She has RAG access to all subdirectories and can read, write, and reason across every project. The six auto-indexed subdirs are: `wiki/`, `knowledge/`, `raw/`, `daily/`, `conversations/`, and `entities/`. This means Delphi can cross-reference Financio signals against vault insights, pull options analysis into conversation context, or query the sentiment pipeline state — all from a single workspace root.

The single canonical projects root (`Path(__file__).resolve().parent.parent` from any project) resolves correctly no matter which machine or drive the repo lives on.

This page documents the inter-project dependencies across the `/Volumes/samsungT7/projects/` workspace and flags every Python file that uses `Path.home() / 'projects'` or `os.path.expanduser("~/projects/...")` to reference a sibling project or shared directory. Those paths will silently resolve to `~/projects/` on the Mac home volume — not the external drive — breaking imports and data reads/writes.

---

## 1. Inter-Project Dependency Map

### Dependency Table

| Consumer Project | Direction | Dependency | What Is Used |
|---|---|---|---|
| **Financio-V2** | → imports from → | **shared_data** | `shared_data.stocks.tickers_config` (get_all_tickers, get_ticker, get_stocks_to_track) via `financio_ticker_integration.py` — PROJECTS_ROOT added to sys.path using `financio_src/paths.py` (fixed) |
| **Financio-V2** | → reads data from → | **shared_data/stocks/** | Morgans sentiment CSVs via `morgans_sentiment_bridge.py`, `backtest_events.py`, `event_feedback.py`; path resolved via `MORGANS_DATA_DIR` env var with fallback default `~/projects/shared_data/stocks` (broken default) |
| **Financio-V2** | → imports from → | **Morgans** | Imports `sentimentBot.CryptoSentimentAnalyzer` directly in `scripts/unified_data_collector.py` via dynamic `sys.path.insert(0, str(self.morgans_project))` where `morgans_project` comes from `financio_src/paths.py` (fixed) |
| **Financio-V2** | → imports from → | **options** | `lstm_model.py` inserts `OPTIONS_DIR` from `financio_src/paths.py` (fixed), then imports `sentiment_reader.SentimentReader`; `options_strategy_engine.py` imports `options_analyzer.OptionsAnalyzer` from local path |
| **Morgans** | → imports from → | **shared_data** | `stock_sentiment.py`, `stock_sentiment_enhanced.py`, `combine_sentiment_history.py`, `backfill_all_tickers.py`, `sec_sentiment_collector.py`, `ticker_discovery.py`, `automate.py` all import `shared_data.stocks.tickers_config` and `shared_data.features.*` — all use `Path(__file__).resolve().parent.parent` to anchor (fixed) |
| **Morgans** | → writes data to → | **shared_data/stocks/** | Sentiment CSVs and JSON files written to `shared_data/stocks/` — path anchored via `Path(__file__).resolve().parent.parent / 'shared_data' / 'stocks'` (fixed) |
| **Morgans** | → imports from → | **options** | `event_classifier.py` is a shim that adds `Path(__file__).resolve().parent.parent / 'options'` to sys.path and re-exports `event_classifier.NewsEventClassifier` (fixed) |
| **options** | → imports from → | **shared_data** | `ticker_loader.py`, `finbert_multi_ticker.py`, `sentiment_weighting_optimizer.py`, `finbert_comparison.py` all import `shared_data.stocks.tickers_config` — all use broken `Path.home() / 'projects'` sys.path insert |
| **options** | → reads data from → | **shared_data/stocks/** | `sentiment_reader.py`, `sentiment_weighting_optimizer.py`, `stock_personality.py`, `finbert_comparison.py` read CSVs from `shared_data/stocks/` — all use broken `Path.home() / 'projects' / 'shared_data'` paths |
| **options** | → imports from → | **Morgans** | `finbert_comparison.py` adds `Path.home() / 'projects' / 'Morgans'` to sys.path and imports `sentimentBot.CryptoSentimentAnalyzer` (broken) |
| **Redpill** | → reads data from → | **shared_data** | `sentiment_reader.py` reads crypto sentiment from `Path.home() / 'projects' / 'shared_data' / 'sentiment'` (broken) |
| **toolsHub** | → imports from → | **shared_data** | `backend/routers/options.py` inserts `os.path.expanduser("~/projects/shared_data/stocks")` into sys.path (broken); `backend/routers/sentiment.py` defines `SHARED_DATA_PATH = os.path.expanduser("~/projects/shared_data")` (broken) |
| **toolsHub** | → imports from → | **options** | `backend/lstm_runner.py` adds `../../options` (relative to file location) to sys.path — resolves correctly as long as toolsHub stays at its current path |
| **toolsHub** | → reads data from → | **shared_data/stocks/** | Reads `*_combined_sentiment.csv` and crypto CSVs via SHARED_DATA_PATH (broken) |
| **skyra** | → self-references → | **skyra** | `test_computer_control.py` hardcodes `~/projects/skyra/logs/computer_control.log` for log path (broken) |
| **Financio-V2** | — internal — | **financio_src/quantum/** | `QuantumFeatureSelector` is an internal module (not the external `Quantum` project); no cross-project dependency |
| **Delphi** | — standalone — | (none) | No cross-project imports found; self-contained AI/memory service |
| **odysseus** | — standalone — | (none) | No cross-project imports found; self-contained AI assistant service |
| **Morgans** | → reads PDF from → | **bookPack** | `split_pdf.py` hardcodes `~/projects/bookPack/book-pack-builder/books/...` (broken, but appears to be a one-off utility script) |

### Dependency Diagram

```
shared_data/stocks/   ←──────────────────────── Morgans (writes CSVs)
      │
      ├──── Financio-V2  (reads via MorgansDataDir env var; sys.path via paths.py)
      ├──── options       (reads directly — BROKEN Path.home() paths)
      ├──── Redpill       (reads directly — BROKEN Path.home() paths)
      └──── toolsHub      (reads directly — BROKEN expanduser paths)

shared_data.stocks.tickers_config  ←── Morgans (imports; fixed)
      │                             ←── options (imports; BROKEN sys.path)
      └─────────────────────────── Financio-V2 (imports; fixed via paths.py)

Morgans/sentimentBot  ←──── options/finbert_comparison.py  (BROKEN sys.path)
                      ←──── Financio-V2/unified_data_collector.py (fixed via paths.py)

options/event_classifier  ←──── Morgans/event_classifier.py (shim; fixed)
options/ (lstm, etc.)     ←──── toolsHub/lstm_runner.py (relative path; OK)
options/sentiment_reader  ←──── Financio-V2/lstm_model.py (via paths.py OPTIONS_DIR; fixed)
```

---

## 2. Path Audit: Broken `Path.home()` References

All entries below are first-party project files (vendor/venv paths excluded). Severity: **sys.path** = import will silently fail or load wrong module; **data path** = reads/writes silently go to wrong location (no error, wrong disk).

| # | File (relative to `/Volumes/samsungT7/projects/`) | Line | Bad Line | Severity | Already Fixed? |
|---|---|---|---|---|---|
| 1 | `options/ticker_loader.py` | 21 | `sys.path.insert(0, str(Path.home() / 'projects'))` | sys.path | No |
| 2 | `options/sentiment_weighting_optimizer.py` | 24 | `sys.path.insert(0, str(Path.home() / 'projects'))` | sys.path | No |
| 3 | `options/sentiment_weighting_optimizer.py` | 40 | `SHARED_DATA_DIR = Path.home() / 'projects' / 'shared_data' / 'stocks'` | data path | No |
| 4 | `options/finbert_multi_ticker.py` | 18 | `sys.path.insert(0, str(Path.home() / 'projects'))` | sys.path | No |
| 5 | `options/finbert_comparison.py` | 25 | `sys.path.insert(0, str(Path.home() / 'projects' / 'Morgans'))` | sys.path | No |
| 6 | `options/finbert_comparison.py` | 38 | `SHARED_DATA_DIR = Path.home() / 'projects' / 'shared_data' / 'stocks'` | data path | No |
| 7 | `options/finbert_comparison.py` | 60 | `load_dotenv(Path.home() / 'projects' / 'Morgans' / '.env')` | data path | No |
| 8 | `options/finbert_comparison.py` | 310 | `sys.path.insert(0, str(Path.home() / 'projects'))` | sys.path | No |
| 9 | `options/sentiment_reader.py` | 22 | `self.data_dir = Path.home() / 'projects' / 'shared_data' / 'stocks'` | data path | No |
| 10 | `options/sentiment_reader.py` | 24 | `self.data_dir = Path.home() / 'projects' / 'shared_data' / 'sentiment' / data_type` | data path | No |
| 11 | `options/stock_personality.py` | 301 | `sentiment_file = Path.home() / 'projects' / 'shared_data' / 'stocks' / f'{symbol.lower()}_sentiment.csv'` | data path | No |
| 12 | `Redpill/sentiment_reader.py` | 45 | `self.base_dir = Path.home() / 'projects' / 'shared_data' / 'sentiment' / data_type` | data path | No |
| 13 | `toolsHub/backend/routers/sentiment.py` | 14 | `SHARED_DATA_PATH = os.path.expanduser("~/projects/shared_data")` | data path | No |
| 14 | `toolsHub/backend/routers/options.py` | 136 | `sys.path.insert(0, os.path.expanduser("~/projects/shared_data/stocks"))` | sys.path | No |
| 15 | `skyra/test_computer_control.py` | 84 | `log_path = os.path.expanduser("~/projects/skyra/logs/computer_control.log")` | data path | No |
| 16 | `Morgans/split_pdf.py` | 4 | `INPUT_FILE = os.path.expanduser("~/projects/bookPack/...")` | data path | No (one-off script) |
| 17 | `Financio-V2/financio_src/sentiment/event_feedback.py` | 35 | `os.getenv("MORGANS_DATA_DIR", "~/projects/shared_data/stocks")` | data path | Partial — overridable via env var, but default is broken |
| 18 | `Financio-V2/financio_src/sentiment/backtest_events.py` | 26 | `os.getenv("MORGANS_DATA_DIR", "~/projects/shared_data/stocks")` | data path | Partial — overridable via env var, but default is broken |

### Files That Are Already Fixed (for reference)

These were previously broken but have been corrected with `Path(__file__).resolve()` anchoring:

| File | Fix Used |
|---|---|
| `Financio-V2/financio_src/paths.py` | Central `_find_repo_root(Path(__file__).resolve())` — all Financio paths derive from this |
| `Financio-V2/financio_ticker_integration.py` | Uses `PROJECTS_ROOT` from `financio_src.paths` |
| `Morgans/stock_sentiment.py` | `Path(__file__).resolve().parent.parent / 'shared_data' / 'stocks'` |
| `Morgans/stock_sentiment_enhanced.py` | Same pattern |
| `Morgans/combine_sentiment_history.py` | Same pattern |
| `Morgans/sec_sentiment_collector.py` | Same pattern |
| `Morgans/ticker_discovery.py` | Same pattern |
| `Morgans/backfill_all_tickers.py` | `HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE.parent))` |
| `Morgans/event_classifier.py` | `Path(__file__).resolve().parent.parent / 'options'` |
| `shared_data/features/technical_indicators.py` | `Path(__file__).resolve().parent.parent.parent` |

---

## 3. Fixes Needed

Actionable checklist — files that still need `Path(__file__).resolve()` fixes. Priority is ordered by impact (live trading code first).

### High Priority — options project (actively imported by Financio-V2 and toolsHub)

- [ ] **`options/sentiment_reader.py`** (lines 22, 24) — Replace `Path.home() / 'projects' / 'shared_data'` with `Path(__file__).resolve().parent.parent / 'shared_data'`
- [ ] **`options/ticker_loader.py`** (line 21) — Replace `sys.path.insert(0, str(Path.home() / 'projects'))` with `sys.path.insert(0, str(Path(__file__).resolve().parent.parent))`
- [ ] **`options/finbert_comparison.py`** (lines 25, 38, 60, 310) — Four separate broken references:
  - `sys.path.insert(0, str(Path.home() / 'projects' / 'Morgans'))` → `str(Path(__file__).resolve().parent.parent / 'Morgans')`
  - `SHARED_DATA_DIR = Path.home() / 'projects' / 'shared_data' / 'stocks'` → `Path(__file__).resolve().parent.parent / 'shared_data' / 'stocks'`
  - `load_dotenv(Path.home() / 'projects' / 'Morgans' / '.env')` → `Path(__file__).resolve().parent.parent / 'Morgans' / '.env'`
  - Second `sys.path.insert` (line 310) — same fix as first
- [ ] **`options/finbert_multi_ticker.py`** (line 18) — Same sys.path fix as ticker_loader.py
- [ ] **`options/sentiment_weighting_optimizer.py`** (lines 24, 40) — Fix sys.path insert and `SHARED_DATA_DIR`
- [ ] **`options/stock_personality.py`** (line 301) — Fix `sentiment_file` path

### Medium Priority — toolsHub (dashboard backend)

- [ ] **`toolsHub/backend/routers/sentiment.py`** (line 14) — Replace `os.path.expanduser("~/projects/shared_data")` with `str(Path(__file__).resolve().parents[3] / 'shared_data')` (3 levels up from `routers/` → `backend/` → `toolsHub/` → `projects/`)
- [ ] **`toolsHub/backend/routers/options.py`** (line 136) — Same pattern, target `shared_data/stocks`

### Medium Priority — Redpill

- [ ] **`Redpill/sentiment_reader.py`** (line 45) — Replace `Path.home() / 'projects' / 'shared_data'` with `Path(__file__).resolve().parent.parent / 'shared_data'`

### Low Priority — Financio-V2 default fallbacks (overridable via env var)

- [ ] **`Financio-V2/financio_src/sentiment/event_feedback.py`** (line 35) — Replace the hardcoded default string `"~/projects/shared_data/stocks"` with a computed default using `financio_src.paths.SHARED_STOCKS_DIR`. As-is, anyone running without `MORGANS_DATA_DIR` set will write feedback CSVs to the wrong disk.
- [ ] **`Financio-V2/financio_src/sentiment/backtest_events.py`** (line 26) — Same fix: replace the `"~/projects/shared_data/stocks"` default with `str(SHARED_STOCKS_DIR)` from `financio_src.paths`.

### Low Priority — Test / utility scripts

- [ ] **`skyra/test_computer_control.py`** (line 84) — Replace `os.path.expanduser("~/projects/skyra/logs/...")` with `Path(__file__).resolve().parent / 'logs' / 'computer_control.log'`
- [ ] **`Morgans/split_pdf.py`** (line 4) — One-off PDF utility; hardcoded path to `bookPack`. Replace with actual drive path or make it a CLI argument.
- [ ] **`Librium/test_visualization.py`** (line 8) — `sys.path.append('/Users/mosley/projects/Librium')` is an absolute hardcoded home path. Replace with `sys.path.append(str(Path(__file__).resolve().parent))`.

---

## Notes

- The **Financio-V2** codebase has the most complete fix in place: `financio_src/paths.py` uses `_find_repo_root(Path(__file__).resolve())` to anchor all paths, and `financio_ticker_integration.py` derives `PROJECTS_ROOT` from that. Any Financio code that still reaches out to other projects should use this pattern.
- The **options** project is the most broken cluster: 6 files with a total of 11 broken references, no equivalent of `paths.py`.
- The **MORGANS_DATA_DIR** env var approach in Financio is sound architecture, but the `"~/projects/shared_data/stocks"` fallback default defeats the purpose when the env var is not set. Both `event_feedback.py` and `backtest_events.py` should fall back to `str(SHARED_STOCKS_DIR)` from `financio_src.paths` instead.
- **Delphi**, **odysseus**, **Apollo**, **Clawbot**, **Clew**, **IRIS**, **FutureSight**, **HealthGlimpse**, **agentRig**, **trading-agent-system**, **finAgent**, **Spider** — no broken cross-project path references found in first-party code.

See also: [[INTEGRATION_ARCHITECTURE]] (Financio-V2), [[INTEGRATION_PROGRESS]] (Financio-V2)
