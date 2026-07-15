---
type: concept
tags: [quantitative-finance, alpha-factors, trading-signals, genetic-programming, llm, symbolic-regression]
created: 2026-06-11
updated: 2026-06-11
status: stub
---

# Alpha Mining

*The practice of discovering trading signals (alphas) — formulaic or ML-based expressions with predictive power over excess return — via systematic search rather than pure intuition.*

An alpha is a function of market data with predictive power over excess return or risk. Classic references: WorldQuant's "101 Formulaic Alphas" (Kakushadze 2016) — e.g., `-((close-open)/((high-low)+0.001))` captures mean-reversion from intraday volatility. The space of possible formulas (combining operators like `ts_corr`, `ts_zscore`, `grouped_demean`, `relu`, etc. over OHLCV and sector features) is combinatorially large — too large for pure hand-crafting.

**Three paradigms** (per [[wiki/sources/2026-06-11-alpha-gpt-alpha-mining|Alpha-GPT, Wang et al. 2023]]):
1. **Manual**: researcher translates market intuition into a formula directly. High signal-to-noise, low throughput.
2. **Algorithmic (genetic programming)**: exhaustive evolutionary search over formula space. High throughput, low human-interpretability, compute-intensive.
3. **Human-AI interactive (Alpha-GPT's contribution)**: LLM mediates between researcher intuition and algorithmic search — researcher describes hypothesis in natural language, LLM formalizes it into seed formulas, genetic programming evolves them, LLM explains results, researcher redirects. IC goes 0.58% (seed) → 2.23% (one interaction + search enhancement).

**Relation to symbolic regression**: [[wiki/concepts/symbolic-regression|Symbolic regression]] (PySR, EML, AI Feynman) and formulaic alpha mining are converging — both seek closed-form expressions from data, both use evolutionary or gradient-based search. The [[wiki/concepts/eml-operator|EML operator]] could function as an alpha grammar in principle. The [[wiki/projects/eml-neural-ode-polymarket|EML-NODE project]] is exploring this via a different route (Neural ODE RHS on prediction market time series).

**For Financio**: the Alpha-GPT paradigm is directly applicable — translate a signal hypothesis (e.g., "sentiment divergence from price momentum over 15-minute windows") into seed formulas via an LLM, then evolve with backtested IC, then iterate with domain judgment. This doesn't require fine-tuning any model; it uses frontier APIs as the ideation layer and classical search for optimization.

See also: [[wiki/concepts/symbolic-regression]], [[wiki/concepts/eml-operator]], [[wiki/areas/entrepreneurship/_overview]], [[wiki/sources/2026-06-11-alpha-gpt-alpha-mining]].
