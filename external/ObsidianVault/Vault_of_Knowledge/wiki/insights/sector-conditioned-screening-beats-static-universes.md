---
type: insight
tags: [trading, quant, financio, screening]
created: 2026-06-11
updated: 2026-06-11
status: active
---

# Sector-Conditioned Screening Beats Static Universes

The choice of which stocks to trade each week is itself a signal—and sector-specific indicator efficacy means that universe selection should be dynamic and feature-rich, not a static list.

## The Core Pattern: Sector Momentum Dominates Stock Momentum

Moskowitz & Grinblatt (1999, *Journal of Finance*) documented that most stock momentum is actually industry momentum. This means that sector context is not a refinement to a stock signal; it is the signal. A momentum-ruled stock in a down sector often reverts faster than a momentum-ruled stock in a rallying sector, even controlling for the stock's own micro-trend.

## Indicator Efficacy Varies Sharply by Sector

Different sectors respond to different technical signals:

- **Tech & Industrials**: Momentum and 52-week-high breakouts persist (continuation patterns work).
- **Utilities & Staples**: Mean reversion dominates (overbought snapbacks are reliable).
- **Energy**: Commodity-cycle linkage (crude, copper, rates) is the primary lever; chart patterns are noise.
- **Financials & Utilities**: Yield-curve and rate-sensitivity (duration risk) drive moves; chart technicals matter little.
- **Biotech & Healthcare**: Event-driven moves (post-earnings drift, Phase trial announcements) overwhelm chart indicators.

Fitting indicators sector-blind ignores this and produces poor out-of-sample performance.

## The Universe Selection Problem: Signal in the Filter

A practical weekly screening pipeline answers: "Is this a move I should play?" Three signals have been validated to predict near-term follow-through:

1. **Relative Volume** (>2× average) — indicates institutional participation; drives short-run continuation, then reversion.
2. **52-Week-High Proximity** (George & Hwang 2004) — most replicated continuation effect in the literature; strongest in tech and growth sectors.
3. **News Volume Direction** (Tetlock) — spike in news volume + positive/neutral tone → continuation; spike + negative tone → reversal. Effect is strongest in event-sensitive sectors (biotech, healthcare).

These three signals, combined sector-conditionally, produce a much tighter universe than "all stocks with volume > 1M shares."

## Turnover Control: The Hysteresis Buffer

Screening turnover eats alpha. A proven solution is a hysteresis buffer: **enter into the top-15 screened names, exit when rank falls below 30**. This asymmetry preserves momentum persistence while eliminating churn from marginal crosses. The optimal width is unpublished—Financio's own backtest is needed to fit it empirically.

## Feature Engineering: One Model, Sector as a Variable

Don't train separate models per sector (fragments training data; a 2021 S&P 500 study found fragmented models degrade performance). Instead, feed sector as a categorical feature alongside price momentum, volume, and news tone. Let a single model learn the nonlinear conditioning automatically. Recent (2025) sector-embedding results support this approach.

## The API Quota Problem Solved as a Side Effect

Financio's immediate constraint: NewsAPI (100 requests/day), Alpha Vantage (25/day), and similar providers limit sentiment-data collection. **A weekly sector-conditioned screener selects ~20 names from 500+.** Morgans bot then collects sentiment only for those 20, not the whole universe. This turns a hard quota limit into a solved problem, while simultaneously improving signal quality (collecting sentiment for a curated set beats shallow sentiment for all 500).

## The Open Gap: No Validated Per-Sector Indicator Protocol

The literature has not published a unified indicator-selection protocol validated across all 11 GICS sectors. Financio's backtest of this design (combining Moskowitz sector-momentum, George & Hwang 52-week-high, Tetlock news volume, and hysteresis turnover control) is original work. The results, once available, will be valuable.

---

## Related Work

- [[2026-06-11-alpha-gpt-alpha-mining]] — LLM-genetic programming for formulaic signal discovery, applicable to refining screening criteria.
- [[2026-06-11-finagent-multimodal-trading-agent]] — Tool-augmented agent decision separation (retrieval vs. decision); applies to screening task delegation.
- [[alpha-mining]] — Signal discovery and formula search.

## Implementation

The sector-conditioned screening logic is built into Financio-V2 at `financio_src/screener/` (completed 2026-06-11).
