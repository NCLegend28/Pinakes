---
type: source
tags: [ml, scaling, language-models, deep-learning, compute]
created: 2026-05-04
updated: 2026-05-04
status: active
source_file: test-scaling-laws.md
source_fingerprint: "# Scaling Laws for Neural Language Models\n\nKaplan et al. (OpenAI, 2020) established that language model performance follows smooth power laws with respect to three factors: compute budget, dataset size, and model parameter count. The key finding is that these factors are largely indepen"
---

# Scaling Laws for Neural Language Models

**Summary**: Kaplan et al. (2020) established that language model loss follows smooth power laws across three independent axes — compute, parameters, and data — and that larger models are dramatically more sample-efficient than smaller ones trained to convergence. This paper is foundational for anyone making decisions about ML training runs: it reframes the question from "what architecture?" to "what scale?" The Chinchilla correction (2022) later refined the data weighting, but the core framework holds and underpins every major frontier model decision since GPT-3.

**Key takeaways**:
- Scale dominates architecture: depth, width, and attention head count matter far less than raw compute, parameters, and data volume. Years of architecture tuning is largely superseded by just scaling up.
- For any fixed compute budget, train a *larger* model on *fewer* tokens — don't train smaller models to convergence. This was counterintuitive and changed industry practice.
- The optimal compute allocation follows C ∝ N × D (parameters × tokens), giving a principled formula for distributing a training budget.
- Chinchilla (Hoffmann et al., 2022) later argued Kaplan et al. underweighted data, meaning most large models of that era were overtrained on parameters and undertrained on data. The refinement matters — but it wouldn't exist without the original framework.
- This is the theoretical backbone behind GPT-3, PaLM, and essentially all post-2020 frontier models — knowing it well is non-negotiable for serious ML research engagement.

**Notable quotes**:
- "larger models are significantly more sample-efficient"
- "architectural details matter far less than scale itself"

**Wiki pages touched**:
- [[wiki/areas/ml-research/_overview]]
- [[wiki/concepts/scaling-laws]]
- [[wiki/concepts/compute-optimal-training]]
- [[wiki/people/jared-kaplan]]
- [[wiki/self/open-questions]]
