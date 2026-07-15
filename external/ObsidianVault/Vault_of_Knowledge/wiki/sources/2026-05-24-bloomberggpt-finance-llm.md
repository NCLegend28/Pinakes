---
type: source
tags: [llm, finance, domain-specific, pretraining, scaling, nlp]
created: 2026-05-24
updated: 2026-05-24
status: active
source_file: bloombergGPT.pdf
source_fingerprint: |
  BloombergGPT: A Large Language Model for Finance. Shijie Wu, Ozan Irsoy, Steven Lu, Vadim Dabravolski, Mark Dredze, Sebastian Gehrmann, Prabhanjan Kambadur, David Rosenberg, Gideon Mann (Bloomberg). Abstract: The use of NLP in financial technology
---

# BloombergGPT: A Large Language Model for Finance (Wu et al., 2023)

**Summary**: Bloomberg trained a 50B-parameter BLOOM-style LLM on a *mixed* corpus — 363B tokens of finance text (curated from forty years of Bloomberg's proprietary data: web, news, filings, press, Bloomberg-internal) plus 345B tokens of general data (The Pile, C4, Wikipedia), ~700B total. The bet, novel at the time, was that mixing domain and general data beats both pure-general (good everywhere, great nowhere) and pure-domain (great in-domain, brittle outside). It paid off: BloombergGPT vastly outperforms comparably-sized open models (BLOOM-176B, GPT-NeoX, OPT) on in-domain financial NLP — sentiment, classification, NER, financial QA — while staying competitive on general benchmarks. They also published "Training Chronicles," a candid log of the training run. For Tali this is the foundational *domain-specific LLM* reference and a concrete, slightly-against-the-grain data point for the [[wiki/concepts/scaling-laws|scaling-laws]] discussion: data *composition*, not just data *quantity*, moves the needle.

**Key takeaways**:
- **Mixed-domain training is the load-bearing idea.** The contribution isn't "a finance model" — it's evidence that *combining* domain-specific and general corpora yields a model strong in-domain without sacrificing general ability. This is the cleanest statement of the [[wiki/concepts/domain-specific-llms|domain-specific LLM]] thesis and the most transferable lesson for anyone fine-tuning or pretraining for a vertical (Financio, biomedical, etc.).
- **Proprietary data is the actual moat.** "Largest domain-specific dataset yet" came from forty years of curated Bloomberg archives with tracked sourcing and usage rights — not scraped. The lesson for [[wiki/areas/entrepreneurship/_overview|product strategy]]: in a world where base models converge, owned/curated data is the defensible asset, echoing the agent-engineering "harness is the moat" framing differently — here it's *data* as moat.
- **A data-constrained, not compute-optimal, regime.** 50B params on ~700B tokens is well under the [[wiki/concepts/compute-optimal-training|Chinchilla]] ~20-tokens-per-param ratio (which would want ~1T+ tokens) — they were bounded by available finance text, not compute. A real-world example that the Chinchilla frontier is an *idealization* you hit data ceilings before reaching, especially in any specialized domain.
- **Domain-specific evaluation is half the work.** Much of the paper is building Bloomberg-internal benchmarks that "most accurately reflect intended usage," because public financial benchmarks underdescribe real tasks. The governance lesson (per Tali's CLAUDE.md AI/ML standards): the eval gate has to mirror deployment, and for a vertical you usually have to build it yourself.
- **Now historically bounded — read it for method, not SOTA.** This is a 2023 paper; [[wiki/sources/2026-05-24-tradingagents-multi-agent-trading|TradingAgents (2025)]] notes that later fine-tuned models (Instruct-FinGPT, Fin-T5) surpass BloombergGPT on several financial classification tasks, and general GPT-4-class models match or beat it on generative tasks. The durable contribution is the mixed-corpus methodology and the honest training write-up, not the leaderboard position.
- **Openness asymmetry worth noting.** Bloomberg released the *method and chronicles* but not the weights or the proprietary data — the same pattern that makes domain models defensible also makes them unreproducible. A tension to hold when evaluating "open" claims in the [[wiki/areas/ml-research/_overview|ml-research]] landscape.

**Notable quotes**:
- "the largest domain-specific dataset yet"
- "best-in-class results on financial benchmarks, while also maintaining competitive performance"

**Wiki pages touched**:
- [[wiki/concepts/domain-specific-llms]] (created)
- [[wiki/concepts/scaling-laws]] (updated — data composition axis)
- [[wiki/concepts/compute-optimal-training]] (updated — data-constrained regime)
- [[wiki/areas/entrepreneurship/_overview]] (updated — data-as-moat)
- [[wiki/areas/ml-research/_overview]] (updated)
- [[wiki/self/open-questions]] (updated — domain vs general)
