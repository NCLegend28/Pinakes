---
type: concept
tags: [symbolic-regression, ml-research, interpretability, scientific-discovery, mathematics]
created: 2026-05-09
updated: 2026-06-11
status: active
---

# Symbolic Regression

The problem of *recovering closed-form mathematical expressions from numerical data*. Inverse to the usual ML setup: rather than fitting a black-box function approximator, you search the space of human-readable symbolic expressions for one that explains the data — ideally exactly, not approximately.

If conventional ML answers "what value does `f(x)` take?", symbolic regression answers "what *is* `f`?" — and returns something a physicist or trader can read. That makes it the natural ML toolkit when the question isn't prediction but *discovery* — finding the law, not approximating it.

## Why this matters

Two reasons it shows up across this vault:

1. **Interpretability without a sacrifice tax.** Most interpretability methods (LIME, SHAP, attention visualization) explain a black box; they don't replace it. Symbolic regression returns an actual formula. When it succeeds, you don't need a separate explanation step. Connects to the [[wiki/concepts/eml-operator|EML]] result that "any conventional neural network is a special case of an EML tree architecture" — i.e., a sufficiently-trained EML tree *is* the explanation.
2. **Recovering laws from market data.** The [[wiki/areas/entrepreneurship/_overview|entrepreneurship lane]] has a real use case here: prediction-market prices, on-chain flows, and price-action data are all candidates for "is there a closed-form regularity I can extract?" The [[wiki/sources/2026-05-09-x-bookmarks-150-dump|May 2026 bookmarks dump]] surfaced multiple Polymarket trading threads referencing exactly this — most of them aspirational, but the underlying lane is legitimate.

## The current landscape (as of 2026)

Three architectural families:

### Genetic / evolutionary search (oldest)
- **PySR** (Cranmer, [44] in the EML paper) — production-quality genetic-programming-based symbolic regression in Python/Julia. Battle-tested in physics and astro. Heterogeneous grammar (you choose the operators).
- **AI Feynman** (Udrescu & Tegmark, 2020, [9] in EML paper) — physics-inspired heuristics (dimensional analysis, separability, symmetry detection) before search. Discovered ~100 known Feynman-lectures equations from data alone.
- **Deep Symbolic Regression** (Petersen et al., 2021, [46] in EML paper) — RNN-policy generates expressions; risk-seeking gradient training.

### Inductive-bias deep learning
- **Cranmer et al. (2020), [10]** — discovering symbolic models from deep learning with inductive biases. Train a GNN with sparsity priors, then read out the learned function.
- **KAN (Kolmogorov–Arnold Networks)** — see [[wiki/concepts/kolmogorov-arnold-networks]]. Replaces fixed neuron activations with *learnable* univariate functions on edges, making the learned network directly readable as a sum of univariate functions per the Kolmogorov–Arnold representation theorem.
- **Lample & Charton (2020), [49]** — transformers trained on symbolic-math pairs to learn symbolic algebra (integration, ODE solving) end-to-end.

### Uniform-grammar / single-primitive
- **EML trees** (Odrzywołek 2026) — see [[wiki/concepts/eml-operator]]. Distinct from the above: the search space is a *complete and uniform* tree of identical operators rather than a heterogeneous grammar. Every elementary function has a representation; the search has no "missing operator" failure mode. Currently shallow (depth ≤4 reliable from blind init), but the architectural property is unique.

## What EML brings that the others don't

Standard symbolic regression searches a heterogeneous grammar (`+`, `−`, `×`, `/`, `sin`, `exp`, …) — you choose the alphabet, and if your target needs an operator you didn't include, you're stuck. EML doesn't have this failure mode because *every elementary function is reachable from `eml` and `1`*. The search space is complete by construction.

The trade is depth: EML trees that express `x²` or `√x` are dozens of nodes deep, whereas in a `+,×` grammar they're nodes 2 and 3. So EML wins on completeness and uniformity, loses on shallow-target efficiency. For now.

## Connection to scaling

Symbolic regression sits orthogonal to [[wiki/concepts/scaling-laws|the scale-is-all-you-need framing]]. Where the scaling-laws axis asks "more parameters → less loss?", symbolic regression asks "is there a *small exact* expression that explains this data?". Different game entirely. The two regimes don't compete — they answer different questions about the same dataset.

## For Tali's purposes

The trading-bot lane (see [[wiki/self/goals]]) overlaps with this thread in a real way. Polymarket prices, behavioral copy-trading patterns, and market microstructure are candidates for "find the closed-form regularity, then exploit it." The [[wiki/sources/2026-05-09-x-bookmarks-150-dump|bookmarks dump]] referenced this lane several times under marketing language ("I gave Claude two formulas and got $14K back"); the legitimate version is using PySR or KAN-style symbolic regression on actual market data and treating recovered expressions as falsifiable hypotheses.

**Connection to alpha mining**: [[wiki/sources/2026-06-11-alpha-gpt-alpha-mining|Alpha-GPT (Wang et al., 2023)]] shows that formulaic alpha search (genetic programming over operator grammars on financial data) is a live, competitive practice — their system ranked top-10 globally in the WorldQuant IQC 2024. The operators they use (time-series correlation, z-score, grouped demeaning, etc.) are a different, financially-motivated grammar from EML trees, but the underlying paradigm — searching closed-form expressions with evolutionary methods — is identical. The two approaches are complementary: EML trees give completeness and uniformity guarantees; the WorldQuant-style grammar gives financial interpretability and practitioner legibility. For Financio's 18-ticker rotation, the Alpha-GPT workflow (LLM ideation → genetic search → IC backtest) may be more immediately deployable than EML. See [[wiki/concepts/alpha-mining]].

This is also the most concrete bridge between [[wiki/areas/ml-research/_overview|ML research]] and [[wiki/areas/entrepreneurship/_overview|entrepreneurship]] in this vault — the only thread where what's interesting in research and what's potentially shippable in a small product converge directly.

## Cross-links

- [[wiki/concepts/eml-operator]] — uniform-grammar approach
- [[wiki/concepts/kolmogorov-arnold-networks]] — interpretability-via-architecture
- [[wiki/concepts/scaling-laws]] — orthogonal frame
- [[wiki/concepts/prediction-markets]] — application target for trading-bot lane
- [[wiki/concepts/alpha-mining]] — formulaic alpha search in finance (WorldQuant grammar; Alpha-GPT)
- [[wiki/areas/ml-research/_overview]]
- [[wiki/areas/entrepreneurship/_overview]]
- [[wiki/sources/2026-05-09-eml-elementary-functions]]
- [[wiki/sources/2026-06-11-alpha-gpt-alpha-mining]]
