---
type: area
tags: [entrepreneurship, startups, business, finance]
created: 2026-05-04
updated: 2026-06-11
status: active
---

# Entrepreneurship — Overview

*Building things: ideas, ventures, and the practice of entrepreneurship.*

## Current Focus

Concrete near-term goal: $10K for car repairs via shipped products — see [[wiki/self/goals]]. Candidate vehicles: Polymarket bot, trading bot, SaaS, app ideas. The constraint is real: revenue-positive within months, not VC-fundable.

## Active Threads

- **Trading & quantitative finance**: The trading-bot path overlaps with several emerging tools. [[wiki/sources/2026-05-06-quantum-computing-introduction|Origin Quantum's textbook]] flags portfolio optimization and fraud detection as near-term [[wiki/concepts/quantum-computing|quantum]] applications via QAOA — overkill for a personal trading bot today, but the [[wiki/projects/origin-quantum-stack|Origin Quantum learning project]] explicitly puts QAOA on the curriculum (Phase 5), so the relevant skill is being built in parallel. *Updated 2026-06-11*: Three June papers are directly applicable to Financio's signal pipeline. (1) **[[wiki/sources/2026-06-11-alpha-gpt-alpha-mining|Alpha-GPT]]** provides a blueprint for mining new formulaic signals without fine-tuning any model — LLM ideation → genetic programming search → IC backtest → human refinement; it ranked top-10 globally in a live competition. (2) **[[wiki/sources/2026-06-11-finagent-multimodal-trading-agent|FinAgent]]** contributes a key retrieval-engineering insight: generate separate query fields for the retrieval step and the decision step in any memory-backed agent — prevents noise contamination between them. Applicable if Financio ever builds a historical sentiment retrieval layer. (3) **[[wiki/sources/2026-06-11-llms-as-financial-annotators|JPMorgan annotation paper]]** means the labeled-data bottleneck for fine-tuning a Financio sentiment model is effectively resolved — GPT-4 API annotation + expert spot-check on the uncertain 35% (identified by RelIndex) is now the standard approach. See [[wiki/concepts/alpha-mining]], [[wiki/concepts/multimodal-trading-agents]], [[wiki/concepts/llm-as-annotator]].
- **Prediction markets — signal under the noise**: The [[wiki/sources/2026-05-09-x-bookmarks-150-dump|May 2026 bookmarks dump]] surfaced ~15 Polymarket trading-bot threads. Most are engagement-bait with implausible P&L claims — and that's named explicitly as an [[wiki/self/patterns|attention-loop pattern]]. But the underlying primitives are real and worth knowing: LMSR pricing (no order book), behavioral copy-trading (mirror the small minority of consistently-winning wallets), Bayesian belief updating, Kelly sizing. Collected on [[wiki/concepts/prediction-markets]]. If a real attempt happens, ground it there, not in the threads.
- **Agent-engineered SaaS**: A more grounded entrepreneurship lane than the trading bots — same bookmarks dump surfaced things like `career-ops` (job-search pipeline as a slash command), gamified push-up trackers with viral growth, agentic workflows for small B2B niches, and Greg Isenberg's "$120/yr Obsidian + Claude as personal OS" framing (see [[wiki/people/greg-isenberg]]). The pattern: small, owned tool that does one thing very well + Claude as runtime + social-proof distribution. Lower variance than prediction-market trading. [[wiki/sources/2026-05-24-opengame-agentic-game-coding|OpenGame (2026)]] is a concrete product shape in this lane — "natural-language spec → playable game" — and a reminder that [[wiki/concepts/agentic-coding|compounding skills + execution-grounded evals]] are what make such agents reliable enough to ship.
- **Real-time avatar front-end for voice agents** *(added 2026-05-24)*: [[wiki/sources/2026-05-24-personalive-portrait-animation|PersonaLive (2025)]] makes [[wiki/concepts/real-time-avatars|real-time talking-head animation]] practical from a single photo. Paired with an LLM + TTS (ElevenLabs) stack, this gives the AI-receptionist / voice-agent products an actual face — lower research risk than trading, components exist, repo open. The clearest near-term [[wiki/self/goals|app/SaaS]] lever in this batch. Carries a consent/deepfake guardrail.
- **Domain-specific models & data-as-moat** *(added 2026-05-24)*: [[wiki/sources/2026-05-24-bloomberggpt-finance-llm|BloombergGPT (2023)]] is the reference for when a vertical (Financio, biomedical) warrants a tuned [[wiki/concepts/domain-specific-llms|domain model]] over a general API — and its real lesson is that *curated proprietary data*, not the model, is the defensible asset. A different flavor of the same "the moat isn't the base model" thesis as the agent-engineering lane.
- **Symbolic regression on market data — the technical bridge**: The most direct overlap between the [[wiki/areas/ml-research/_overview|ml-research]] thread and this area. [[wiki/concepts/symbolic-regression]] (PySR, AI Feynman, KAN, [[wiki/concepts/eml-operator|EML]]) is the legitimate version of "give Claude a formula and get $14K back" — recovering closed-form regularities from price/order-flow/on-chain data and treating them as falsifiable hypotheses. Connects [[wiki/concepts/prediction-markets]] (where the data lives) to [[wiki/concepts/eml-operator]] (a complete-by-construction grammar). Currently shallow (depth ≤4 reliably recoverable from random init) — but a small, well-scoped attempt against, say, Polymarket LMSR-implied-probability time series is a real research-flavored entrepreneurship project, not a hype thread.
- **App / SaaS ideas**: Open. The user's [[wiki/self/creative-voice|writing voice]] and [[wiki/self/strengths|analytical-creative range]] suggest products at the intersection of expression and tools — but no specific bet yet.
- **Industry watch — Chinese tech**: A recurring pattern in ingested sources is high-quality work coming out of Chinese industry-academia collaborations (Origin Quantum, [[wiki/sources/2026-05-06-msa-memory-sparse-attention|Evermind/Shanda Group on MSA]], and now [[wiki/sources/2026-05-24-opengame-agentic-game-coding|CUHK on OpenGame]] and [[wiki/sources/2026-05-24-personalive-portrait-animation|U Macau/Dzine on PersonaLive]]). Worth tracking as a competitive landscape and as a potential source of tools / partners.

## Key Pages in This Area

- [[wiki/concepts/prediction-markets]] — LMSR, behavioral copy-trading, Bayesian updating, Kelly sizing
- [[wiki/concepts/symbolic-regression]] — recovering closed-form regularities from market data
- [[wiki/concepts/eml-operator]] — complete-by-construction grammar for the same
- [[wiki/people/jim-simons]] — quant icon; Renaissance Technologies founder
- [[wiki/people/greg-isenberg]] — Obsidian + Claude as personal OS framing
- [[wiki/sources/2026-05-09-x-bookmarks-150-dump]] — surfaced both the noise and the real primitives
- [[wiki/sources/2026-05-09-eml-elementary-functions]] — Odrzywołek (2026): EML paper
- [[wiki/concepts/real-time-avatars]] — talking-head front-end for voice agents (stub)
- [[wiki/concepts/agentic-coding]] — what makes shippable code agents reliable (stub)
- [[wiki/concepts/domain-specific-llms]] — when a vertical warrants a tuned model (stub)
- [[wiki/concepts/multi-agent-systems]] — trading-firm-as-agents design pattern (stub)
- [[wiki/sources/2026-05-24-tradingagents-multi-agent-trading]] — Xiao et al. 2025: agent-firm trading
- [[wiki/sources/2026-05-24-bloomberggpt-finance-llm]] — Wu et al. 2023: finance LLM, data-as-moat
- [[wiki/sources/2026-05-24-opengame-agentic-game-coding]] — Jiang et al. 2026: spec → playable game
- [[wiki/sources/2026-05-24-personalive-portrait-animation]] — Li et al. 2025: real-time avatar front-end
- [[wiki/sources/2026-06-11-finagent-multimodal-trading-agent]] — Zhang et al. 2024: retrieval separation + dual reflection for Financio
- [[wiki/sources/2026-06-11-alpha-gpt-alpha-mining]] — Wang et al. 2023: formulaic alpha mining; live competition benchmark
- [[wiki/sources/2026-06-11-llms-as-financial-annotators]] — Aguda et al. 2024: LLM annotation pipeline for training data
- [[wiki/concepts/alpha-mining]] — signal mining workflow for Financio (stub)
- [[wiki/concepts/llm-as-annotator]] — resolving the labeled-data bottleneck (stub)
- [[wiki/concepts/multimodal-trading-agents]] — visual chart input for trading agents (stub)

## Tension to watch

There's a values-level tension between *building products* (which often means quantification, optimization, attention capture) and the [[wiki/self/values|anti-commodification stance]] expressed in *NaN*. This is named in [[wiki/self/open-questions]] and worth revisiting as specific product bets get made.
