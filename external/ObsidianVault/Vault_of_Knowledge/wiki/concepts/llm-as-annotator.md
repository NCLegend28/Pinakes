---
type: concept
tags: [llm, data-annotation, labeling, fine-tuning, dataset-creation, domain-specific]
created: 2026-06-11
updated: 2026-06-11
status: stub
---

# LLM-as-Annotator

*Using a large language model (typically via API) to generate training labels for supervised learning, replacing or augmenting human crowdworkers.*

Established by [[wiki/sources/2026-06-11-llms-as-financial-annotators|Aguda et al. (2024), JPMorgan AI Research]] for the finance domain: GPT-4 and PaLM 2 outperform MTurk crowdworkers by ~29% F1 on financial relation extraction, at 8–16× lower cost. Key caveat: neither model reaches expert-annotator quality (~10–15% below on hard instances). The operational recommendation is a **hybrid strategy**:

1. Run LLM annotation across the full dataset.
2. Compute a reliability index (LLM-RelIndex: confidence-weighted agreement across multiple LLM runs) for each instance.
3. High-confidence instances (~65%) → accept LLM labels.
4. Low-confidence instances (~35%) → route to domain expert review.

**Why this matters for fine-tuning decisions**: The bottleneck for training a domain-specific model is often labeled data, not compute. LLM-as-annotator resolves this without hiring a full annotation team. For Financio — if training a sentiment classifier or event-extraction model on earnings calls, news headlines, or SEC filings — the pipeline is: GPT-4 API labels → RelIndex filter → expert spot-check on uncertain ones → clean training set.

**Key failure mode**: Hallucination on the "no relation / no signal" label. When the true label is "no relevant signal," frontier LLMs tend to invent a relation anyway. Explicit negative sampling with a strict filter is needed. See [[wiki/sources/2026-06-11-llms-as-financial-annotators|the JPMorgan paper]] for quantified hallucination rates by model.

**Tension with BloombergGPT's thesis**: [[wiki/sources/2026-05-24-bloomberggpt-finance-llm|BloombergGPT]] positioned curated proprietary data as the moat. LLM-as-annotator changes the calculus: the seed data (your raw text corpus) is still proprietary and still matters, but the labeling cost is no longer a meaningful barrier. The moat is the *selection and validation* of what to annotate, not the annotation labor itself.

See also: [[wiki/concepts/domain-specific-llms]], [[wiki/areas/entrepreneurship/_overview]], [[wiki/self/open-questions]].
