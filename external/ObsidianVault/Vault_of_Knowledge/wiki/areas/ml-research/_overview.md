---
type: area
tags: [ml, research, deep-learning, agent-engineering, symbolic-regression]
created: 2026-05-04
updated: 2026-06-11
status: active
---

# ML Research — Overview

*Ongoing engagement with machine learning research: papers, architectures, ideas.*

## Current Focus

Understanding the empirical foundations of modern large language models — the scaling laws framework that drove the post-2020 frontier, and now the architectural ideas (memory, sparse attention, position encoding) that may define the next phase as raw scale runs into context-window and memory-capacity ceilings.

## Active Threads

- **Scaling laws**: How compute, parameters, and data interact to determine model performance. See [[wiki/concepts/scaling-laws]] and [[wiki/concepts/compute-optimal-training]].
- **Long-context memory**: Architectures that push effective context from 1M toward 100M+ tokens — the regime where lifetime/agentic memory becomes possible. See [[wiki/concepts/long-context-memory]] and [[wiki/concepts/sparse-attention]]. Open question: when does architecture beat scale?
- **Quantum × ML**: Active learning project for the [[wiki/projects/origin-quantum-stack|Origin Quantum stack]] — VQNet sits squarely at this intersection. See also [[wiki/concepts/quantum-machine-learning]].
- **Foundational papers**: Working through the key papers that shaped the field — Kaplan et al. (2020), Chinchilla (2022), and the transformer lineage.
- **Agent engineering — the layer above the model**: Surfaced from the [[wiki/sources/2026-05-09-x-bookmarks-150-dump|May 2026 bookmarks dump]] as the actually-substantive thread under the noise. The premise: frontier models are converging, so the moat is the harness — context management, structured memory, skills as code, retry/error handling, sub-agent orchestration, evaluation loops. Reading targets: [[wiki/people/andrej-karpathy|Karpathy]]'s Sequoia agentic-engineering masterclass, the leaked / dissected Anthropic Claude Code internals (823-line retry system; structured memory architecture), Claude Skills design, and `ml-intern` (autonomous research-loop agent that produced 500+ projects). Direct relevance to the [[wiki/projects/origin-quantum-stack]] tooling layer and to the SaaS path in [[wiki/self/goals]].
- **Autonomous research agents**: Two concrete pointers: `ml-intern` running real post-training experiments at HuggingFace, and a paper showing AI agents executing a complete high-energy physics analysis pipeline end-to-end. Worth tracking as a separate trajectory from chatbot-style agents.
- **Multi-agent orchestration & agentic coding** *(added 2026-05-24)*: The sub-thread under agent-engineering concerned with *how agents are wired together*. [[wiki/sources/2026-05-24-tradingagents-multi-agent-trading|TradingAgents (2025)]] makes the case for role-specialized agents with *structured-output control + NL-only-for-debate* communication to beat the "telephone effect." [[wiki/sources/2026-05-24-opengame-agentic-game-coding|OpenGame (2026)]] formalizes [[wiki/concepts/agentic-coding|skills-as-code that compound]] (Template + Debug skills) plus execution-grounded RL and *playability* evals that move past static unit tests. Both are the academic mirror of this vault's own harness-is-the-moat premise. See [[wiki/concepts/multi-agent-systems]] and [[wiki/concepts/agentic-coding]].
- **LLM self-evaluation is unreliable — external validators required** *(added 2026-06-11)*: [[wiki/sources/2026-06-11-llms-novel-research-ideas|Si et al. (2024), Stanford]] ran the most rigorous head-to-head of LLM vs. human research ideation (100+ expert reviewers, blind study). Main finding: AI ideas are rated more novel (p<0.05), but LLM self-rankers achieve only ~53% consistency — barely above random. This is a concrete constraint on any agentic system that uses an LLM to score or select among its own outputs. For multi-agent trading systems or signal-mining agents, ranking by LLM judgment without external ground truth (IC, backtest) is not reliable. See [[wiki/concepts/multi-agent-systems]] for implications.
- **Multimodal trading agents** *(added 2026-06-11)*: [[wiki/sources/2026-06-11-finagent-multimodal-trading-agent|FinAgent (Zhang et al., 2024)]] extends the LLM trading-agent design to include visual Kline chart input (GPT-4V), a dual-level reflection system (price-pattern recognition + trade-decision retrospective), and a retrieval-task/decision-task separation that prevents noise between the two. The most portable engineering lesson: when building any retrieval-over-memory layer, generate separate query fields for retrieval vs. decision — they have different optimization objectives. See [[wiki/concepts/multimodal-trading-agents]].
- **Human-AI collaborative alpha mining** *(added 2026-06-11)*: [[wiki/sources/2026-06-11-alpha-gpt-alpha-mining|Alpha-GPT (Wang et al., 2023)]] demonstrates a live-competition-validated system (top-10 globally in WorldQuant IQC 2024, 41,000+ teams) for mining formulaic trading alphas by having an LLM mediate between researcher intuition and genetic-programming search. IC improves from 0.58% (LLM seed) → 2.23% (one interaction + search enhancement). The human-AI dialogue loop is measurably productive. See [[wiki/concepts/alpha-mining]] — the formulaic alpha paradigm sits adjacent to [[wiki/concepts/symbolic-regression]] and the EML thread.
- **LLM-as-annotator** *(added 2026-06-11)*: [[wiki/sources/2026-06-11-llms-as-financial-annotators|Aguda et al. (2024), JPMorgan]] establish that GPT-4 and PaLM 2 replace non-expert crowdworkers for financial NLP annotation (relation extraction on SEC filings) at ~29% higher F1 and ~10× lower cost. Expert review remains necessary for ~35% of instances; the LLM-RelIndex confidence metric identifies which ones. This resolves the labeled-data bottleneck for any domain fine-tuning project without a full annotation team. See [[wiki/concepts/llm-as-annotator]].
- **Domain-specialization vs general scale** *(added 2026-05-24)*: A recurring counter-current to pure scaling. [[wiki/sources/2026-05-24-bloomberggpt-finance-llm|BloombergGPT (2023)]] (mixed domain+general pretraining) and OpenGame's GameCoder-27B (CPT+SFT+RL on game repos) both show a smaller domain-adapted model beating a larger general one in-lane. See [[wiki/concepts/domain-specific-llms]].
- **Inference efficiency as the product unlock** *(added 2026-05-24)*: [[wiki/sources/2026-05-24-personalive-portrait-animation|PersonaLive (2025)]] makes [[wiki/concepts/diffusion-models|diffusion]] portrait animation real-time (7–22×) via appearance distillation (motion converges early; later denoising steps are redundant) + micro-chunk autoregressive streaming. The concrete cash-out of the "inference is the moat" framing, and a structural echo of MSA's train-short/infer-long fix. See [[wiki/concepts/real-time-avatars]].
- **World models and inference as the moat**: LeCun's `LeWorldModel` (a non-LLM world-model architecture, see [[wiki/people/yann-lecun]]) and the recurring "model race ended, inference is the real moat" framing in the bookmarks dump. Question worth holding: if every branch of physics gets a learned approximator, what does that do to scaling-law projections?
- **Universal primitives & legible architectures (symbolic regression by gradient descent)**: [[wiki/sources/2026-05-09-eml-elementary-functions|Odrzywołek (2026)]] showed that a single binary operator [[wiki/concepts/eml-operator|`eml(x,y) = exp(x) − ln(y)`]] plus the constant `1` is sufficient to express every elementary function — the continuous-math analogue of NAND. The structural payoff: every elementary expression becomes a uniform binary tree, parameterizable, trainable with Adam, and *legible as a closed-form expression* when training succeeds. This is real interpretability-by-construction, sitting alongside [[wiki/concepts/kolmogorov-arnold-networks|KAN]] in a small but growing family of "explanation-isn't-a-separate-step" architectures. The line worth dwelling on: "any conventional neural network is a special case of an EML tree architecture." See [[wiki/concepts/symbolic-regression]] for the broader landscape (PySR, AI Feynman, Cranmer GNN, deep symbolic regression, EML).

## Key Pages in This Area

- [[wiki/concepts/scaling-laws]] — Power law relationships between scale and model loss
- [[wiki/concepts/compute-optimal-training]] — How to allocate a fixed compute budget optimally
- [[wiki/concepts/long-context-memory]] — Taxonomy of approaches for lifetime-scale LLM memory
- [[wiki/concepts/sparse-attention]] — Selective attention mechanisms enabling sub-quadratic long-context
- [[wiki/people/jared-kaplan]] — Lead author of the original scaling laws paper
- [[wiki/sources/2026-05-04-scaling-laws-for-neural-language-models]] — Kaplan et al. 2020 source summary
- [[wiki/sources/2026-05-06-msa-memory-sparse-attention]] — Chen et al. 2026: 100M-token end-to-end memory via sparse attention
- [[wiki/people/andrej-karpathy]] — Sequoia agentic-engineering talk; Obsidian-as-personal-OS framing
- [[wiki/people/yann-lecun]] — `LeWorldModel`; non-LLM world-model architecture
- [[wiki/sources/2026-05-09-x-bookmarks-150-dump]] — Bookmarks dump that surfaced the agent-engineering thread
- [[wiki/concepts/eml-operator]] — Sheffer-stroke for elementary functions; symbolic regression by gradient descent
- [[wiki/concepts/symbolic-regression]] — landscape: PySR, AI Feynman, KAN, EML
- [[wiki/concepts/kolmogorov-arnold-networks]] — interpretability-via-architecture (stub)
- [[wiki/people/andrzej-odrzywolek]] — EML author; theoretical physicist at Jagiellonian University (stub)
- [[wiki/sources/2026-05-09-eml-elementary-functions]] — Odrzywołek (2026): EML paper
- [[wiki/concepts/multi-agent-systems]] — role-specialized agents + structured communication (stub)
- [[wiki/concepts/agentic-coding]] — compounding skills + execution-grounded code agents (stub)
- [[wiki/concepts/domain-specific-llms]] — domain-adapted models beating larger general ones (stub)
- [[wiki/concepts/diffusion-models]] — generative denoising + inference acceleration (stub)
- [[wiki/sources/2026-05-24-tradingagents-multi-agent-trading]] — Xiao et al. 2025: trading-firm-as-agents
- [[wiki/sources/2026-05-24-bloomberggpt-finance-llm]] — Wu et al. 2023: mixed-corpus finance LLM
- [[wiki/sources/2026-05-24-opengame-agentic-game-coding]] — Jiang et al. 2026: agentic game creation
- [[wiki/sources/2026-05-24-personalive-portrait-animation]] — Li et al. 2025: real-time diffusion avatars
- [[wiki/sources/2026-06-11-finagent-multimodal-trading-agent]] — Zhang et al. 2024: multimodal LLM trading agent (Kline charts, dual reflection, retrieval separation)
- [[wiki/sources/2026-06-11-alpha-gpt-alpha-mining]] — Wang et al. 2023: human-AI interactive alpha mining; top-10 WorldQuant IQC 2024
- [[wiki/sources/2026-06-11-llms-as-financial-annotators]] — Aguda et al. 2024: LLMs beat crowdworkers for financial annotation
- [[wiki/sources/2026-06-11-llms-novel-research-ideas]] — Si et al. 2024: AI ideas more novel, LLM self-eval unreliable
- [[wiki/concepts/multimodal-trading-agents]] — visual market data + LLM trading agents (stub)
- [[wiki/concepts/alpha-mining]] — formulaic alpha search; genetic programming + LLM ideation (stub)
- [[wiki/concepts/llm-as-annotator]] — LLMs replacing crowdworkers for training data generation (stub)
