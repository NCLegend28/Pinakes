---
type: concept
tags: [llm, domain-specific, pretraining, fine-tuning, data, annotation]
created: 2026-05-24
updated: 2026-06-11
status: active
---

# Domain-Specific LLMs

*Language models adapted to a vertical (finance, code, biomedical) that beat larger general models inside their domain — via mixed-corpus pretraining, continual pre-training, fine-tuning, or tool augmentation.*

Created from [[wiki/sources/2026-05-24-bloomberggpt-finance-llm|BloombergGPT (Wu et al., 2023)]], which showed that *mixing* domain and general data (363B finance + 345B general tokens) yields a model strong in-domain without sacrificing general ability — beating both pure-general and pure-domain alternatives. [[wiki/sources/2026-05-24-opengame-agentic-game-coding|OpenGame's GameCoder-27B (2026)]] applies the same thesis to *code*: continual pre-training + SFT + RL on game repos makes a 27B model beat larger general code models at building playable games.

The June 2026 batch adds two dimensions to this picture:

**Annotation as the new bottleneck**: [[wiki/sources/2026-06-11-llms-as-financial-annotators|Aguda et al. (2024), JPMorgan]] show that the labeled-data bottleneck for training domain models is now solvable with LLM-as-annotator: GPT-4 beats crowdworkers by ~29% F1 at ~10× lower cost, making it viable to generate large financial training sets without a full annotation team. See [[wiki/concepts/llm-as-annotator]]. The moat shifts from annotation labor to (a) seed corpus selection and (b) the expert validation tier for the uncertain ~35% of instances.

**Tool-augmented agents as an alternative to full fine-tuning**: [[wiki/sources/2026-06-11-finagent-multimodal-trading-agent|FinAgent (Zhang et al., 2024)]] and [[wiki/sources/2026-06-11-alpha-gpt-alpha-mining|Alpha-GPT (Wang et al., 2023)]] both show that injecting domain knowledge via tools, structured prompts, and RAG over financial knowledge bases achieves strong in-domain performance from a frontier general model — without retraining. This is a viable lower-investment path for Financio before committing to fine-tuning.

The recurring conclusions:
- **A smaller, domain-adapted model can outperform a larger general one inside its lane.** Echoes the architecture-beats-scale finding in [[wiki/concepts/long-context-memory|MSA]], on a different axis.
- **Curated proprietary data is the moat** (Bloomberg's 40-year archive) — and the reason these models are usually unreproducible. But annotation labor is no longer part of that moat.
- **You usually have to build the eval yourself**, because public benchmarks underdescribe real deployment.
- **The two paths to domain adaptation**: (1) pretraining/fine-tuning on proprietary data (BloombergGPT, FinGPT); (2) frontier model + domain tools + RAG + structured prompting (FinAgent, Alpha-GPT). Path 2 is faster and doesn't require GPU budget upfront. Path 1 is defensible at scale once the data and compute are in hand.

Relevant to any [[wiki/areas/entrepreneurship/_overview|vertical product]] (Financio, biomedical) considering a tuned model over a general API.

See also: [[wiki/concepts/scaling-laws]], [[wiki/concepts/compute-optimal-training]], [[wiki/concepts/agentic-coding]], [[wiki/concepts/llm-as-annotator]], [[wiki/concepts/multimodal-trading-agents]].
