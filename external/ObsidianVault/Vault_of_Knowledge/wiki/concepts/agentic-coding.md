---
type: concept
tags: [agentic-coding, code-agents, llm, agent-engineering, skills]
created: 2026-05-24
updated: 2026-05-24
status: stub
---

# Agentic Coding

*Autonomous code agents that go beyond isolated functions to build whole multi-file artifacts — and the harness (skills, debug protocols, execution-grounded feedback) that lets them stay coherent at scale.*

Created from [[wiki/sources/2026-05-24-opengame-agentic-game-coding|OpenGame (Jiang et al., 2026)]], which names the "complexity wall" frontier code agents hit on large builds — logical incoherence (lost global state), engine-specific knowledge gaps, and cross-file inconsistencies — and answers it with a self-evolving **Game Skill**: a *Template Skill* (growing library of stable project skeletons) plus a *Debug Skill* (accumulated verified fixes generalized into rules). Verification moves from static unit tests to *execution-grounded* signals (does it actually run / play).

The transferable ideas:
- **Skills-as-code that compound** — capability accumulates across tasks instead of being re-prompted each time. This is the academic formalization of the [[wiki/people/andrej-karpathy|Karpathy]] / [[wiki/people/greg-isenberg|Isenberg]] "harness is the moat" framing, and of how this vault's own ingest/skill setup is meant to work.
- **Execution-grounded reward** disciplines the model by reality, not a text-similarity proxy.

Sits in the [[wiki/areas/ml-research/_overview|agent-engineering thread]] and connects to [[wiki/concepts/multi-agent-systems]] (orchestration) and [[wiki/concepts/domain-specific-llms]] (GameCoder-27B as a code-domain model).

See also: [[wiki/areas/entrepreneurship/_overview]].
