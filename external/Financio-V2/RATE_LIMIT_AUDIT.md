# API Rate-Limit Audit — Financio-V2 + Morgans

**Date:** 2026-06-11 · **Rule:** the bot must never exhaust a daily quota mid-day ("no spam-then-dead").
Limits verified by web research June 2026 (sources at bottom). Usage computed from code + scheduler cadences.

## The math (before fixes)

Morgans `automate.py` runs **stock_news every 6h (4×/day) over ~497 tickers** (`shared_data/stocks/tickers_config.py`), and for each ticker `analyze_stock_news()` hits up to 5 news APIs (`stock_sentiment_enhanced.py:83-104`). Financio itself trades only **18 rotation tickers**.

| Provider | Free-tier limit (verified) | Computed usage | Verdict |
|---|---|---|---|
| **Alpha Vantage** | **25 req/day** | 497×4 = 1,988/day | 🔴 **80× OVER** — dead after first 25 tickers of run #1 |
| **NewsAPI** | **100 req/day** (24h article delay on free) | 1,988/day | 🔴 **20× OVER** — dead after ~100 tickers |
| **FMP** | ~250 req/day (free; couldn't fully verify — confirm on your dashboard) | 1,988/day | 🔴 **~8× OVER** |
| **Finnhub** | 60 req/min | 497/run, paced by loop latency | 🟡 Bursts can 429; per-day OK |
| **GDELT** | No key; fair-use (~1 req/5s recommended) | 497×4/day | 🟡 OK if paced |
| **Reddit (PRAW)** | ~60 req/min adaptive | ~6 searches × 497 × 4 ≈ 12k/day spread out | 🟡 PRAW auto-throttles; OK |
| **SEC EDGAR** | 10 req/s + User-Agent w/ email | Daily incremental | 🟢 Already compliant (validates UA, `sec_filings.py:341`) |
| **Alpaca (Financio bot)** | 200 req/min (Basic) | 18 tickers × ~1 fetch/min cycle ≈ 20-40/min incl. backend | 🟢 ~5× headroom |
| **yfinance** | Unofficial; ~20-30 req/min practical, IP bans | LSTM/options paths only (not multi-bot prod) | 🟡 Avoid in prod loops |

**Why this matters beyond data loss:** Financio's pipeline now *requires* fresh Morgans sentiment (no fallbacks). If Morgans burns its quotas at 6:00 AM, sentiment goes stale, and the trading bot correctly refuses to trade. Quota exhaustion = trading outage.

## Fixes implemented (2026-06-11)

1. **`Morgans/api_budget.py`** — persistent, thread-safe daily budget per provider (UTC reset, survives restarts, warns at 80%, hard-stops at 100%). Budgets set ~10% below documented limits; override via env:
   - `NEWSAPI_DAILY_BUDGET` (default 90)
   - `ALPHAVANTAGE_DAILY_BUDGET` (default 22)
   - `FMP_DAILY_BUDGET` (default 225)
2. **`Morgans/stock_sentiment_enhanced.py`** — NewsAPI, Alpha Vantage, and FMP calls now go through the budget. On exhaustion that provider is skipped loudly for the rest of the day (visible in source_breakdown); other providers continue. This is quota management, not a silent fallback — nothing fabricates data.
3. Verified: 4 unit tests pass (exhaustion raises, persistence across restarts, UTC rollover, exactly-N-allowed under 60-thread contention).

## Decisions for Tali (not implemented — they change data scope)

1. **🎯 Biggest win: collect only what you trade.** Morgans scans 497 tickers; Financio trades 18. Restricting stock_news to the 18 rotation tickers (+ a small watchlist) makes the math trivially healthy: 18×4 = 72 NewsAPI calls/day (under 100 ✓), and even Alpha Vantage nearly fits (72/day vs 25 — prioritize top tickers or run AV 1×/day = 18 ✓). One-line-ish change: have `stock_sentiment_enhanced.run_analysis` read a `MORGANS_TICKERS` env or import Financio's rotation list.
2. **Alpha Vantage premium ($50/mo, 75 req/min)** or simply dropping AV as a source — at 25/day free it can never cover even 18 tickers 4×/day.
3. **Within-budget prioritization:** with budgets on, the first N tickers in the loop win the quota. If you keep 497 tickers, reorder the loop so Financio's 18 rotation tickers are always first (recommended regardless).

## Sources
- NewsAPI pricing — newsapi.org/pricing (June 2026): 100 req/day free, 24h delay
- Alpha Vantage — alphavantage.co/support (June 2026): 25 req/day free
- Reddit/PRAW — praw.readthedocs.io (June 2026): ~60 req/min adaptive
- SEC EDGAR — sec.gov/about/developer-resources (Mar 2025): 10 req/s, UA required
- Alpaca — docs.alpaca.markets (June 2026): 200 req/min Basic, 10k/min Algo Trader Plus
- yfinance — github.com/ranaroussi/yfinance issues (Apr 2026): ~20-30 req/min practical
- Finnhub/FMP/CryptoPanic: docs pages loaded but exact quotas not machine-verifiable — confirm in your account dashboards before raising budgets.
