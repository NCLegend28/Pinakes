---
type: source
tags: [llm, research-agents, scientific-discovery, evaluation, ideation, human-ai]
created: 2026-06-11
updated: 2026-06-11
status: active
source_file: "Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers.md"
source_fingerprint: |
  Si, Yang, Hashimoto (2024) Stanford. Can LLMs Generate Novel Research Ideas? arXiv 2409.04109.
---

# Can LLMs Generate Novel Research Ideas? (Si et al., 2024 — Stanford)

**Summary**: Si, Yang, and Hashimoto (Stanford) run the most methodologically rigorous evaluation to date of LLM research ideation — 104 NLP researchers recruited for blind review of 49 human ideas and 49 LLM-generated ideas across controlled topics. The LLM agent uses RAG over Semantic Scholar papers, over-generates 4,000 seed ideas per topic, deduplicates, then ranks via a Claude-3.5-Sonnet pairwise tournament. The main result is statistically significant (p<0.05 across three independent statistical tests): AI-generated ideas are rated as more novel than human expert ideas, while being slightly lower on feasibility and comparable on overall score. Two critical limitations surface: (1) LLMs plateau at ~200 unique ideas out of 4,000 generated (95% are near-duplicates at cosine sim >0.8), meaning naive inference scaling doesn't produce diversity; (2) LLM self-evaluation is near-random (Claude-3.5 pairwise ranker achieves only 53.3% consistency vs 56.1% for humans, both low). The paper explicitly leaves unresolved whether "judged as novel" translates to "produces better research outcomes" — the full execution study was still recruiting.

**Key takeaways**:
- **LLMs are genuinely creative at the ideation stage, with a real diversity ceiling.** The novelty result is credible (three independent stats tests, 100+ expert reviewers, carefully controlled design). LLMs can surface combinations a domain expert wouldn't naturally reach — the breadth of pretraining is the mechanism. The ceiling: 200 unique ideas per topic regardless of how many you generate. The practical implication for Tali's autonomous research work: use LLM ideation for breadth, not for endless generation — stop after ~200 candidates and move to execution.
- **LLMs cannot reliably self-evaluate.** The best LLM ranker (Claude-3.5 pairwise) only reaches 53.3% consistency, barely above random, on the task of identifying which idea is better. This is the clearest finding relevant to any agentic research system, including the [[wiki/projects/eml-neural-ode-polymarket|EML-NODE project]]: LLM-as-judge for selecting among candidate strategies or hypotheses is not reliable. Human selection (or proxy metrics like IC from backtesting) must anchor the ranking step.
- **For Financio: the ideation agent pattern is usable now, the self-evaluation pattern is not.** An Alpha-GPT-style loop (generate ideas → backtest → human reviews IC) works because the ranking step uses real market data, not LLM self-scoring. A loop that generates trading hypotheses and lets the LLM pick the best one without external validation is unreliable by this paper's evidence. This directly informs how to wire up any signal-mining agent for the 18-ticker rotation: generate many, filter by IC, human selects direction.
- **Novelty ≠ feasibility ≠ outcome.** Human ideas score higher on feasibility (6.61 vs 6.34 for AI). The overall score gap is not significant without human reranking. The paper's design can't answer whether more novel ideas produce better papers — the execution study was still pending. Translated to trading: a more "novel" signal hypothesis might be less executable. Novel ideas from an LLM still need Tali's domain filter for whether they're deployable in Financio's actual data pipeline.
- **Strong methodological template for Tali's own evals.** The blind-review design — style-normalize all outputs, match topic distributions, use multiple independent statistical tests, measure inter-reviewer consistency — is the right framework for any serious evaluation comparing human and LLM outputs. If Tali ever wants to formally compare Financio's LLM-generated signals against human-designed ones, this paper is the design blueprint.

**Notable quotes**:
- "LLM-generated ideas are judged as more novel (p<0.05) than human expert ideas while being judged slightly weaker on feasibility"
- "out of 4000 generated seed ideas, there are only 200 non-duplicate unique ideas"

**Wiki pages touched**:
- [[wiki/areas/ml-research/_overview]] (updated — autonomous research agents; LLM self-evaluation failures)
- [[wiki/concepts/multi-agent-systems]] (updated — self-evaluation reliability caveat)
- [[wiki/self/open-questions]] (updated — where does edge live in agentic AI; LLM-as-judge reliability)
- [[wiki/projects/eml-neural-ode-polymarket]] (updated — do not use LLM self-eval as ranking step)
- [[wiki/areas/entrepreneurship/_overview]] (updated — ideation agent usable; self-evaluation not)
