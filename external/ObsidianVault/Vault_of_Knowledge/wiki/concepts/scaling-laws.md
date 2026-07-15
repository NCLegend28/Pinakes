---
type: concept
tags: [ml, scaling, deep-learning, empirical]
created: 2026-05-04
updated: 2026-05-24
status: stub
---

# Scaling Laws

Empirical regularities showing that neural language model performance (loss) follows smooth power laws as a function of compute budget, parameter count, and dataset size — discovered by Kaplan et al. (2020) and later refined by the Chinchilla paper (Hoffmann et al., 2022). The core insight is that these three factors are largely independent predictors of loss, and that scale matters more than architectural choices.

> ⚠️ **Counter-evidence on the "scale > architecture" claim**: [[wiki/sources/2026-05-06-msa-memory-sparse-attention|Chen et al. (2026)]] show a 4B model with a custom memory architecture (MSA) outperforming 70B–235B models on long-context QA. The scaling laws were derived under fixed-context assumptions; for memory-bound tasks, architecture appears to matter more than parameter count. This doesn't refute the original framework — it bounds where it applies. See [[wiki/concepts/long-context-memory]].

> ⚠️ **Data composition, not just data quantity**: [[wiki/sources/2026-05-24-bloomberggpt-finance-llm|BloombergGPT (Wu et al., 2023)]] shows that *mixing* domain-specific and general corpora (363B finance + 345B general tokens) produces a model strong in-domain without sacrificing general ability — beating both pure-general and pure-domain peers of the same size. The scaling laws treat D as a scalar token count; this is evidence that the *composition* of D is a separate, controllable lever on where capability lands. Bounds the framework rather than refuting it. See [[wiki/concepts/domain-specific-llms]].

> ⚠️ **Orthogonal axis — primitive sufficiency**: [[wiki/sources/2026-05-09-eml-elementary-functions|Odrzywołek (2026)]] shows that all elementary functions are expressible in a single binary operator ([[wiki/concepts/eml-operator|EML]]) plus the constant `1`. This isn't counter-evidence to scaling — it's an entirely different axis. Where scaling-laws ask "more parameters → less loss?", the primitive-sufficiency view asks "what's the smallest *exact* representation of this function class?". The two regimes don't compete; they answer different questions. Worth holding both: scale gives capacity, primitive sufficiency gives [[wiki/concepts/symbolic-regression|legibility]]. A trillion-parameter transformer has equivalent EML tree depth ~40, well beyond current symbolic-regression reach — meaning EML doesn't displace scale, but it does suggest there's a *minimum-description* axis the scaling-laws literature has barely touched.

See also: [[wiki/concepts/compute-optimal-training]], [[wiki/sources/2026-05-04-scaling-laws-for-neural-language-models]], [[wiki/concepts/long-context-memory]], [[wiki/concepts/eml-operator]], [[wiki/concepts/symbolic-regression]], [[wiki/concepts/domain-specific-llms]], [[wiki/areas/ml-research/_overview]].
