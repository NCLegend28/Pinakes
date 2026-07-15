---
type: concept
tags: [multi-agent, llm, agent-engineering, orchestration, trading, research-agents]
created: 2026-05-24
updated: 2026-06-11
status: active
---

# Multi-Agent Systems

*Architectures where multiple LLM agents with distinct roles collaborate — analyzing, debating, and adjudicating — to solve a task no single agent handles well.*

Created from [[wiki/sources/2026-05-24-tradingagents-multi-agent-trading|TradingAgents (Xiao et al., 2025)]], which models a trading firm's org chart: role-specialized analysts → Bull/Bear debate → trader → risk team → fund manager. The two ideas worth carrying forward:

- **Role specialization** decomposes a multifaceted task across agents, mirroring how human organizations manage complexity.
- **Communication structure matters more than agent count.** Unstructured natural-language message-passing decays into a "telephone effect"; the fix is *structured outputs for control, natural language only for debate*. Adversarial role pairs (Bull vs Bear) are a cheap built-in check against single-agent rationalization.

**Additions from the June 2026 batch:**

- **Classical algorithm as one "agent" in a hybrid loop** ([[wiki/sources/2026-06-11-alpha-gpt-alpha-mining|Alpha-GPT]]): the system pairs an LLM agent (ideation, explanation, natural language interface) with a classical genetic-programming engine (combinatorial search). The LLM doesn't do the search; it generates seeds and interprets results. This LLM+algorithm hybrid is a multi-agent pattern that doesn't require all agents to be LLMs.
- **Self-evaluation is the weak link.** [[wiki/sources/2026-06-11-llms-novel-research-ideas|Si et al. (2024), Stanford]] show that LLM agents evaluating their own outputs (or each other's ideas) reach only ~53% consistency — barely above random. External validators (backtesting IC, human review, market data) must anchor any ranking or selection step. The "LLM adjudicates" pattern from TradingAgents is sound; the "LLM ranks its own ideas" pattern is not.
- **Single-agent + tools as a viable alternative** ([[wiki/sources/2026-06-11-finagent-multimodal-trading-agent|FinAgent]]): a single LLM with a structured five-module architecture (market intelligence, memory, dual reflection, tool-augmented decision) can beat multi-agent systems if the modules are cleanly separated. The distinction between role-specialized agents and module-specialized components inside a single agent is partly architectural, partly a question of scale and parallelism.

Directly relevant to the [[wiki/areas/ml-research/_overview|agent-engineering thread]] (the harness is the moat) and to AgentRig-style orchestration. Contrast with the single-model [[wiki/projects/eml-neural-ode-polymarket|EML-NODE]] approach to alpha.

See also: [[wiki/concepts/agentic-coding]], [[wiki/concepts/alpha-mining]], [[wiki/areas/entrepreneurship/_overview]].
