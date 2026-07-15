---
type: concept
tags: [ml, scaling, compute, training, chinchilla]
created: 2026-05-04
updated: 2026-05-24
status: stub
---

# Compute-Optimal Training

The principle that for any fixed compute budget C, there is an optimal allocation between model size (N parameters) and training data (D tokens), approximated as C ∝ N × D. Kaplan et al. (2020) first formalized this, finding it optimal to train larger models on fewer tokens rather than smaller models to convergence. Chinchilla (Hoffmann et al., 2022) revised the balance, arguing Kaplan underweighted data — leading to the finding that most large models of that era were "undertrained" on data relative to their parameter count.

Practically: a Chinchilla-optimal model is smaller (cheaper to infer) for the same loss than a Kaplan-optimal one trained on the same budget.

> **Real-world ceiling — you hit data limits first.** [[wiki/sources/2026-05-24-bloomberggpt-finance-llm|BloombergGPT (2023)]] trained 50B params on ~700B tokens — well under Chinchilla's ~20-tokens-per-param ideal (which would want ~1T+) — because they were bounded by available finance text, not compute. A concrete reminder that the compute-optimal frontier is an idealization you often can't reach in any specialized [[wiki/concepts/domain-specific-llms|domain]], where curated data is the scarce input.

See also: [[wiki/concepts/scaling-laws]], [[wiki/sources/2026-05-04-scaling-laws-for-neural-language-models]], [[wiki/concepts/domain-specific-llms]], [[wiki/areas/ml-research/_overview]].
