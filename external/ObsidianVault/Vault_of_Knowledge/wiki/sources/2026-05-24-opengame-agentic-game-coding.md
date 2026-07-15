---
type: source
tags: [agentic-coding, llm, code-agents, games, domain-specific, rl, evaluation]
created: 2026-05-24
updated: 2026-05-24
status: active
source_file: openGame.pdf
source_fingerprint: |
  OpenGame: Open Agentic Coding for Games. Yilei Jiang, Jinyuan Hu, Qianyin Xiao, Yaozhi Zheng, Ruize Ma, Kaituo Feng, Jiaming Han, Tianshuo Peng, Kaixuan Fan, Manyuan Zhang, Xiangyu Yue (CUHK MMLab). Game development sits at the intersection
---

# OpenGame: Open Agentic Coding for Games (Jiang et al., 2026)

**Summary**: CUHK's MMLab tackles a failure mode current code agents share — they ace isolated programming tasks but collapse when asked to build a *whole playable game*, hitting a "complexity wall" of cross-file inconsistency, broken scene wiring, and logical incoherence. OpenGame is an open-source agentic framework for end-to-end web game creation (targeting the Phaser JS engine because it's purely programmatic, unlike GUI-bound Unreal/Unity). Two pieces carry it: **GameCoder-27B**, a code model built on Qwen3.5-27B via continual pre-training → supervised fine-tuning → execution-grounded RL; and a self-evolving **Game Skill** = a *Template Skill* that grows a library of project skeletons from experience + a *Debug Skill* that maintains a living protocol of verified fixes. They also ship **OpenGame-Bench**, which scores *playability* (build health, visual usability, intent alignment via headless browser + VLM judging) rather than static unit tests. For Tali the most resonant idea is structural: the skill-as-living-protocol pattern is a formalization of exactly how her own Claude skills and CLAUDE.md conventions accumulate — see [[wiki/areas/ml-research/_overview|agent-engineering thread]].

**Key takeaways**:
- **The "complexity wall" names a real limit of today's code agents.** Three recurring frontier-model failures: (1) *logical incoherence* — losing track of global state across the game loop; (2) *engine-specific knowledge gaps* — re-implementing mechanics instead of using framework-native systems; (3) *cross-file inconsistencies* — mismatched asset keys, broken init order. This taxonomy generalizes to any large multi-file agentic build, not just games.
- **Skills-as-code, made to evolve.** Template Skill (growing library of stable project skeletons) + Debug Skill (accumulated verified fixes, generalized into rules) is the paper's articulation of [[wiki/concepts/agentic-coding|agentic coding]] as *capability accumulation* rather than per-task prompting. This is the academic mirror of the Greg-Isenberg / Karpathy "skills + harness is the moat" framing already in this vault — and of how this very wiki's ingest/skill setup is meant to compound.
- **Domain-specialized models beat general ones at the vertical — again.** GameCoder-27B (CPT + SFT + RL on game repos) is the [[wiki/concepts/domain-specific-llms|domain-specific model]] thesis applied to *code* rather than text — same conclusion as [[wiki/sources/2026-05-24-bloomberggpt-finance-llm|BloombergGPT]]: a smaller, domain-adapted model can beat a larger general one inside its lane. The recurring pattern across this ingest batch.
- **Execution-grounded RL is the interesting training stage.** Rather than rewarding text similarity, RL rewards *test pass rate from actually running the code* on single-file gameplay modules. Grounding the reward in execution is the same instinct as the EML-NODE project's "snap and backtest" gate — the model is disciplined by reality, not by a proxy.
- **Verifying playability is harder than verifying code — and they built for it.** OpenGame-Bench moves evaluation from "does it compile" to "can an agent build something actually playable," judged by headless browser execution + VLM. The broader lesson for [[wiki/areas/ml-research/_overview|ml-research]]: as agents produce interactive artifacts, evals must move from static checks to dynamic, multimodal behavior — static unit tests undersample what matters.
- **A concrete entrepreneurship adjacency.** "Natural-language spec → fully playable game" is a shippable-product shape (the paper's own personas: film lover, teacher, YouTuber). Lower-stakes than trading; squarely in the [[wiki/areas/entrepreneurship/_overview|agent-engineered SaaS lane]] of one-thing-well tools with built-in distribution.

**Notable quotes**:
- "they consistently stumble when asked to produce a fully playable game"
- "moves verification from static code analysis to dynamic playability assessment"

**Wiki pages touched**:
- [[wiki/concepts/agentic-coding]] (created)
- [[wiki/areas/ml-research/_overview]] (updated — agent-engineering thread)
- [[wiki/concepts/domain-specific-llms]] (updated — code variant)
- [[wiki/areas/entrepreneurship/_overview]] (updated — agent-engineered SaaS lane)
- [[wiki/people/andrej-karpathy]] (updated — skills-as-harness)
