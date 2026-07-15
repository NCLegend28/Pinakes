---
type: concept
tags: [prediction-markets, polymarket, finance, lmsr, bayesian, kelly]
created: 2026-05-09
updated: 2026-05-24
status: stub
---

# Prediction Markets

*Markets where participants trade contracts whose payoff is tied to the outcome of a future event — a mechanism for aggregating beliefs into prices.*

Created from the [[wiki/sources/2026-05-09-x-bookmarks-150-dump|May 2026 bookmarks dump]] to capture the *real* primitives that the engagement-bait Polymarket threads gesture at — separated from the noise. If a serious attempt at a Polymarket-edge product happens (see [[wiki/self/goals]] and the trading-bot path in [[wiki/areas/entrepreneurship/_overview]]), this is the page to build out.

## Real primitives worth knowing

- **LMSR (Logarithmic Market Scoring Rule)** — Polymarket isn't an order book; it's an automated market maker that prices contracts via a log-loss scoring rule. Liquidity is parameterized; price moves predictably with volume; no counterparty matching needed. Implication: the trader is competing against a known pricing curve, not against other traders directly.
- **Behavioral copy-trading** — Across millions of trades, a small minority of wallets (~0.51% in the figure cited in the bookmarks) consistently win. The hypothesis: identify their behavioral fingerprints (entry timing, sizing, market preference) and mirror them, rather than try to predict outcomes from scratch.
- **Bayesian belief updating** — Treat each market as a probability estimate; treat new information (news, satellite data, on-chain flows) as evidence; update accordingly. Edge comes from update speed and source quality, not from "calling it right."
- **Kelly criterion sizing** — Optimal bet size as a function of edge and odds. Most retail traders systematically over- or under-size; correct sizing is a structural advantage independent of pick quality.
- **Maker vs taker economics** — In the cited dataset, takers (market orders) lose ~1.12% per trade on average; makers (limit orders) earn ~1.12%. The implication is structural: passive provision of liquidity is the consistently profitable side, not active speculation.

## Two approaches to edge (added 2026-05-24)

The trading lane now has two contrasting *methods* on file, worth holding as distinct hypotheses about where edge lives:

- **Agent-orchestration alpha** — [[wiki/sources/2026-05-24-tradingagents-multi-agent-trading|TradingAgents (2025)]] reads everything (fundamentals, sentiment, news, technicals), debates Bull vs Bear, and adjudicates. A [[wiki/concepts/multi-agent-systems|multi-agent firm]] applied to (equities) trading. Transferable here: the structured-output + adversarial-debate pattern could wrap a Polymarket decision, though it's heavier than the primitives above.
- **Symbolic-mechanism alpha** — [[wiki/projects/eml-neural-ode-polymarket|EML-NODE]] recovers the closed-form dynamics of price motion. Legible, falsifiable, lighter.

Both still answer to the [[wiki/people/jim-simons|Renaissance lesson]]: real edges are small and sustainable, and any reported backtest needs out-of-sample, cost-aware validation.

## Cross-links

- [[wiki/areas/entrepreneurship/_overview]] — trading-bot lane in current goals
- [[wiki/self/goals]] — the $10K target
- [[wiki/self/patterns]] — the engagement-bait attention loop around this topic
- [[wiki/sources/2026-05-09-x-bookmarks-150-dump]] — source of all surfaced primitives above
- [[wiki/sources/2026-05-24-tradingagents-multi-agent-trading]] — agent-firm trading approach
- [[wiki/concepts/multi-agent-systems]] — the orchestration pattern behind it
