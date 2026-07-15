---
type: source
tags: [llm, finance, data-annotation, nlp, fine-tuning, labeling, domain-specific]
created: 2026-06-11
updated: 2026-06-11
status: active
source_file: "Large Language Models as Financial Data Annotators A Study on Effectiveness and Efficiency.md"
source_fingerprint: |
  Aguda, Siddagangappa et al. (2024) JPMorgan AI Research. LLMs as Financial Data Annotators. arXiv 2403.18152.
---

# LLMs as Financial Data Annotators (Aguda et al., 2024 — JPMorgan AI Research)

**Summary**: JPMorgan AI Research tests whether GPT-4, PaLM 2, and MPT-7B Instruct can replace non-expert crowdworkers for financial relation extraction — specifically, identifying labeled relationships between entity pairs (organization–date, person–title, etc.) in SEC filings, using the REFinD dataset (3,598 test instances, 22 relation types). Key finding: GPT-4 and PaLM 2 both significantly outperform MTurk crowdworkers by a 29% F1 margin; neither matches domain experts; MPT-7B underperforms but still beats crowdworkers with 5-shot CoT prompts. The paper introduces LLM-RelIndex, a confidence-weighted majority vote that identifies which ~65% of instances an LLM can label reliably without expert review. Cost comparison: GPT-4 at $24–51 vs crowdworkers at ~$389 for 3,598 instances, while delivering faster throughput and higher F1. The recommendation is a hybrid strategy: LLM for the easy 65%, domain expert for the hard 35%.

**Key takeaways**:
- **LLMs can replace crowdworkers for financial annotation at a fraction of the cost — but not domain experts.** For the specific use case of generating labeled training data for a financial NLP model (sentiment, NER, relation extraction), using GPT-4 API calls instead of MTurk reduces cost ~8–16× and improves quality by ~29% F1. This directly addresses Tali's fine-tuning decision: if the bottleneck is labeled training data for Financio's sentiment or event-extraction tasks, LLM-assisted annotation is now the obvious first step, not the experimental one. Domain expert review is only needed for the 35% of instances the RelIndex flags as uncertain.
- **Prompt engineering dominates small-model performance.** GPT-4 and PaLM 2 are robust to prompt variation (~5–7% range across prompt types). MPT-7B swings wildly (19% range), meaning a small locally-hostable model needs careful prompt crafting plus 5-shot examples to reach crowdworker parity. This is relevant to Tali's GPU/GCP trade-off: a frontier API (GPT-4) is more robust for annotation; a small fine-tuned model (for inference) needs its training data to be already clean.
- **The reliability index principle is the portable takeaway.** Rather than treating every LLM annotation as equally trustworthy, LLM-RelIndex scores each instance by how confidently all LLM runs agree. High-RelIndex → accept; low-RelIndex → flag for expert review. This principle generalizes beyond relation extraction: any LLM-annotated dataset for Financio (news sentiment polarity, event-type tagging, earnings call summarization) should have an analogous confidence filter before the labels go into training data. Build the filter, not just the prompt.
- **Hallucinations cluster on the "no relation" label.** When experts labeled a pair as no/other relation, LLMs hallucinated a specific relation instead at rates of 46–81% (PaLM 2 worst). Finance text is dense with co-occurring entities that don't have a meaningful relationship in context — the model wants to find a pattern. Implication for Financio: if using LLM annotation for negative samples (e.g., news items with no relevant signal), filter hallucinations explicitly.
- **Contradiction with the BloombergGPT data-moat thesis:** [[wiki/sources/2026-05-24-bloomberggpt-finance-llm|BloombergGPT]] argued that curated proprietary data is the moat. This paper shows that for annotation labor — a different but related bottleneck — a general frontier LLM already closes the gap. The moat is the *seed* data and the expert validation tier, not the crowdworker-scale annotation. These two findings are compatible but they carve the data pipeline differently.

**Notable quotes**:
- "LLMs can serve as more reliable annotators for ~65% of this dataset"
- "customizing the prompts for each relation group by providing specific examples belonging to those groups is paramount"

**Wiki pages touched**:
- [[wiki/concepts/llm-as-annotator]] (created stub)
- [[wiki/concepts/domain-specific-llms]] (updated — annotation-as-labeling vs pretraining; hybrid strategy)
- [[wiki/areas/entrepreneurship/_overview]] (updated — LLM annotation pipeline for Financio training data)
- [[wiki/areas/ml-research/_overview]] (updated — LLM-as-annotator thread)
- [[wiki/self/open-questions]] (updated — fine-tuning decision: data acquisition strategy)
