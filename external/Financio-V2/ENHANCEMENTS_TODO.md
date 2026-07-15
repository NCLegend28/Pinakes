# Financio-V2 Enhancements TODO — 2026-06-11

This is a living checklist. Items are checked off the moment work completes.

## Decisions (locked)

- Telegram channels: daily summary + error/health alerts (NO per-trade messages)
- Fine-tune analysis covers BOTH paths (sentiment/annotation AND trading-signal LLM), with sequencing recommendation
- Fine-tune on Google Cloud GPU (free credits) → ship model to VPS; inference on cloud until credits exhausted, then local GPU
- Rate-limit rule: the bot must NEVER exhaust a daily quota mid-day (no spam-then-dead)
- Papers ingest follows the vault's CLAUDE.md ingest workflow exactly
- Tali wants to LEARN from this — explanations with analogies, tied to making money

## Phase 1: Telegram notifications

- [x] Telegram notifier module (bot token + chat id, env-driven, fail-fast if enabled but unconfigured)
- [x] Daily summary goes to Telegram when enabled (alongside email)
- [x] Critical alerts (startup validation failure, shutdown) go to Telegram
- [x] .env.vps.template updated with TELEGRAM_* vars (compose passes whole .env already)
- [x] Syntax/smoke check (3 config tests pass; fixed blank-value parsing bug)

## Phase 2: API rate-limit audit & fixes

- [x] Inventory every external API call site + frequency math (Financio + Morgans: 497 tickers × 4 runs/day × 5 APIs)
- [x] Research current rate limits for each provider (web, June 2026, cited)
- [x] Identify overruns (Alpha Vantage 80× over, NewsAPI 20× over, FMP ~8× over)
- [x] Write RATE_LIMIT_AUDIT.md with findings + fixes
- [x] Implement Morgans/api_budget.py + wire into NewsAPI/AV/FMP call sites (4 unit tests pass incl. thread safety)

## Phase 3: Fine-tune model analysis

- [x] Web research: current (mid-2026) financial model landscape for both paths
- [x] Comparison doc: sentiment/annotation vs trading-signal, GCP plan, VPS/local-GPU fit
- [x] Saved to vault outputs/2026-06-11-finetune-model-analysis.md (recommendation: Qwen2.5-7B LoRA + ModernBERT insurance; Alpha-GPT workflow instead of trading-LLM fine-tune)

## Phase 4: Vault paper ingest (4 papers)

- [x] Ingest: A Multimodal Foundation Agent for Financial Trading (FinAgent)
- [x] Ingest: Alpha-GPT — Human-AI Interactive Alpha Mining
- [x] Ingest: LLMs as Financial Data Annotators
- [x] Ingest: Can LLMs Generate Novel Research Ideas?
- [x] Update index.md + log.md per vault conventions (4 source pages, 3 concept stubs, 8 pages updated)

## Phase 5: Learning synthesis

- [x] Plain-language walkthrough: delivered in chat + embedded in the analysis doc

## Phase 6: Training kickoff + tradeability brainstorm (added 2026-06-11)

- [x] Literature search: sector-specific indicators, universe selection, "is a move a play" (delegated; 25+ sources)
- [x] docs/GCP_FINETUNE_GUIDE.md — step-by-step: dataset → L4 spot VM → QLoRA + ModernBERT → eval → GGUF/ONNX ship
- [x] Tradeability-score design sketched (chat); decision pending on building the weekly screener module
- [x] DECISION (Tali): green-light the weekly screener module — APPROVED ("the word")

## Phase 7: Weekly tradeability screener (added 2026-06-11, built same day)

- [x] financio_src/screener/ package: sectors (104-name universe, 5 sector profiles), scoring (liquidity gate + cross-sectional sector-weighted composite), hysteresis buffer, news confirmation (Tetlock rule), weekly job, backtest harness with --grid parameter fitting
- [x] ROTATION_SOURCE wiring in config.py (static default = advisory; screener = consume file, hard-fail if missing/stale >8d)
- [x] .env.vps.template screener section
- [x] tests/test_screener_logic.py — 6 tests pass (gates, scoring bounds, hysteresis rules, determinism, backtest math)
- [x] Vault insight filed: sector-conditioned-screening-beats-static-universes
- [x] KILLED CRITICAL FALLBACK discovered en route: fetch_price_data silently substituted SYNTHETIC price data when the broker API failed — bots could trade on fabricated bars. Removed; empty-DF + retry + raise now.
- [ ] NEXT (needs Alpaca keys, run on Mac/VPS): `python -m financio_src.screener.backtest --start 2024-06-01 --end 2026-06-01 --grid` to fit enter/exit ranks, then `python -m financio_src.screener.screener` (dry run) for the first advisory list

## Phase 8: Dataset prep + thorough sweep (added 2026-06-12)

- [x] scripts/prep_finetune_dataset.py — dedup (72h window, keep most-complete row), staging, annotation JSONL, zip
- [x] DEDUP RESULT: 1,421,684 rows → 157,164 unique (88.9% duplicates — collector re-fetched 7-day windows every 6h, re-appending each headline up to 28×). Tali's ABT example now appears once.
- [x] Migration archives on the drive (all integrity-verified): financio_finetune_data_20260612_part1_headlines.zip (27.3MB: 487 deduped CSVs + texts_for_annotation.jsonl + dedup report), part2_reddit.zip, part3_sec.zip. Staging dir kept: financio_ft_staging_20260612/
- [x] ANSWER: shared_data is MODEL-annotated (VADER/FinBERT/keyword ensemble) — not gold labels. Second review = the frontier-annotation pass (GCP guide Step 0). Old labels preserved as weak_label for agreement filtering.
- [x] Haiku THOROUGH sweep: 11 findings (7 critical) — all critical fixed:
  - [x] backend served RANDOM SIMULATED PRICES by default (use_simulated_data=True) → real streaming default, SIMULATED_STREAM=true opt-in with screaming warning
  - [x] corrupt confidence → invented 0.5 in 3 backend files → None (unknown), logged
  - [x] /active-bots fabricated id/status/isRunning/profitPercent → measured from trades DB (recency-based status, real cost-basis %)
  - [x] missing current_tickers.txt → silent default watchlist → hard failure
  - [x] quantum feature selector silent classical swap → explicit require_quantum param (not in live path)
  - [x] earlier session: fetch_price_data synthetic-bars fallback killed

## Discovered work

- [x] Fixed TELEGRAM_ENABLED parsing bug: blank value in .env was treated as enabled
- [x] Fixed ROTATION_SOURCE same blank-value parsing footgun
- [ ] DECISION (Tali): align Morgans collection to Financio's 18 rotation tickers (or reorder loop so rotation tickers consume quota first) — see RATE_LIMIT_AUDIT.md
- [ ] DECISION (Tali): Alpha Vantage free tier (25/day) can't cover even 18 tickers 4×/day — upgrade ($50/mo) or drop AV as a source
- [ ] LOW (from sweep): financio_src/analytics/equity_curve.py contains placeholder simulation logic but is imported nowhere — delete or rewrite when touched
