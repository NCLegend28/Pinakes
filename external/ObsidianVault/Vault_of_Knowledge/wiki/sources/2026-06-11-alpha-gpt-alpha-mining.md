---
type: source
tags: [llm, quantitative-finance, alpha-mining, alpha-factors, genetic-programming, human-ai, trading-signals]
created: 2026-06-11
updated: 2026-06-11
status: active
source_file: "Alpha-GPT Human-AI Interactive Alpha Mining for Quantitative Investment.md"
source_fingerprint: |
  Wang, Yuan et al. (2023/2024) HKUST/IDEA Research/Columbia. Alpha-GPT: Human-AI Interactive Alpha Mining. arXiv 2308.00016.
---

# Alpha-GPT: Human-AI Interactive Alpha Mining (Wang et al., 2023)

**Summary**: Wang, Yuan et al. (HKUST, IDEA Research, Columbia) propose a third paradigm for quantitative alpha mining — after hand-crafted factors and genetic-programming search — by inserting an LLM as the mediator between human trading intuition and algorithmic factor search. The system, Alpha-GPT, runs an iterative three-stage loop: ideation (the researcher describes a market hypothesis in natural language; a Trading Idea Polisher agent formalizes it using a RAG knowledge library of existing alphas), implementation (a Quant Developer agent generates seed alpha formulas, then genetic programming evolves them), and review (an Analyst agent backtests, generates an IC score and natural-language interpretation, and feeds results back to the researcher for the next round). In autonomous mode it uses hierarchical RAG to explore large databases top-down without overwhelming the LLM context. Evaluated in the WorldQuant IQC 2024 competition (41,000+ teams), Alpha-GPT ranked top-10 globally, generating 81 qualified alphas with strong out-of-sample scores — a live competition, not a historical backtest. The alpha IC goes from 0.58% (seed) → 1.23% (search enhancement) → 2.23% (one interaction round + enhancement), showing that the human-AI dialogue loop itself adds measurable signal beyond the LLM alone.

**Key takeaways**:
- **The human-AI dialogue loop is measurably productive.** IC doubling from 0.58% to 1.23% via genetic-programming enhancement, then doubling again to 2.23% after one round of human feedback, suggests that human domain expertise applied to the LLM's generated alphas is a genuine multiplier — not just interface sugar. The iterative loop (ideate → backtest → explain → refine) is exactly the workflow Tali runs manually when building signals for [[wiki/areas/entrepreneurship/_overview|Financio]]. Alpha-GPT automates the translate-and-scale steps while keeping the human in the loop for direction.
- **Formulaic alphas (symbolic signals) still have an edge worth chasing.** This paper is entirely about formulaic (expression-based) alphas, not ML black-boxes. An alpha like `-((close-open)/((high-low)+0.001))` is falsifiable, explainable, and decays differently than a gradient-boosted model. This is adjacent to [[wiki/concepts/symbolic-regression|symbolic regression]] — the same instinct toward legible, closed-form predictors — and directly relevant to the EML-NODE hypothesis in [[wiki/projects/eml-neural-ode-polymarket|the Polymarket project]].
- **Top-10 worldwide in a live, real-time competition is a credible benchmark.** Unlike most trading-agent papers evaluated on historical simulations, Alpha-GPT was deployed in the WorldQuant IQC 2024 during the competition period with no future data leakage. Top-10 from 41,000 teams is the clearest "this isn't just a research demo" signal in this batch of papers. The out-of-sample score being competitive (43,319 vs top-10's 48,715) shows the alphas generalize.
- **Candidate for Financio's signal-mining workflow.** The AlphaBot + genetic programming + IC feedback loop is a blueprint for how Tali could systematically mine novel signals for the 18-ticker rotation without hand-coding each one. The interactive mode (human in the loop) suits her current scale; autonomous mode would suit a wider database once the ticker universe grows. Direct alternative to fine-tuning a trading LLM from scratch — you leverage the frontier model's prior knowledge and let genetic search handle the combinatorial work.
- **Separation of concerns: LLM for ideation, algorithms for optimization.** The architecture deliberately does not ask the LLM to do combinatorial search — it generates seeds and explains outputs, while classical genetic programming does the iteration. This division of labor reflects sound ML system design and echoes the [[wiki/sources/2026-06-11-finagent-multimodal-trading-agent|FinAgent]] pattern of using LLMs to adjudicate structured signals rather than recompute them.

**Notable quotes**:
- "Alpha-GPT can generate performant alphas, ranking among the top 10 worldwide and top 3 regionally"
- "a repeated process of experimentation-and-analysis" (framing alpha mining as an iterative loop, not a stroke-of-genius)

**Wiki pages touched**:
- [[wiki/concepts/alpha-mining]] (created stub)
- [[wiki/concepts/symbolic-regression]] (updated — formulaic alphas as adjacent terrain)
- [[wiki/areas/entrepreneurship/_overview]] (updated — alpha-mining workflow for Financio)
- [[wiki/areas/ml-research/_overview]] (updated — human-AI collaborative research loop)
- [[wiki/concepts/multi-agent-systems]] (updated — orchestration with classical search hybrid)
- [[wiki/projects/eml-neural-ode-polymarket]] (updated — formulaic-alpha connection)
- [[wiki/people/jim-simons]] (live competition context for backtest comparison)
