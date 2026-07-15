# Which Financial Model Should Financio Fine-Tune? — Analysis & Recommendation

*2026-06-11 · For Tali · Sources: web research (June 2026, cited) + the four papers ingested today ([[2026-06-11-llms-as-financial-annotators]], [[2026-06-11-alpha-gpt-alpha-mining]], [[2026-06-11-finagent-multimodal-trading-agent]], [[2026-06-11-llms-novel-research-ideas]])*

## The recommendation up front

**Fine-tune a small sentiment/annotation model first (Path 1). Do not fine-tune a trading-signal LLM yet (Path 2).** Specifically:

1. **Primary build:** LoRA-fine-tune **Qwen2.5-7B-Instruct** (Apache 2.0) on ~10-30k labeled financial texts, trained on a GCP **L4 spot instance** (~$2-5 per run against your $300 credits), quantized to Q4 and served on your **local GPU** later. Plug it in behind Morgans' existing FinBERT slot.
2. **Cheap insurance bet alongside it:** fine-tune **ModernBERT** (~140M params) on the same dataset. It runs at hundreds of texts/second *on the VPS CPU* with no GPU at all. If the 7B's accuracy edge over ModernBERT is small on YOUR data, the encoder wins on cost and you keep the GPU free.
3. **For trading signals:** run the **Alpha-GPT workflow** (frontier API + your existing backtester) instead of fine-tuning — it needs no training and its credibility is the best of the bunch (top-10 of 41,000+ teams in a live WorldQuant competition).

Why this ordering: the sentiment model improves an input your ensemble already trusts (25% weight), it's measurable against your own Morgans archive, and it's deployable on hardware you'll actually have. The trading-signal LLM is where the literature is currently weakest — more below.

## Why Path 1 (sentiment/annotation) wins right now

**The analogy:** your ensemble is a kitchen with four cooks (technical 30%, sentiment 25%, regime 20%, LSTM 25%). Fine-tuning a sentiment model is upgrading one cook's knife — cheap, low-risk, and you can taste-test the difference. Fine-tuning a trading-signal LLM is firing the head chef and hiring a celebrity chef you've only seen on TV — expensive, and the TV footage (backtests) is edited.

1. **FinBERT is now beatable with modest effort.** A Dec 2025 study showed Qwen3-8B and Llama3-8B beat FinBERT on five financial sentiment datasets *using only 5% of the training data*; FinBERT sometimes got worse with fine-tuning [arXiv:2512.00946]. FinLoRA showed vanilla rank-8 LoRA on Llama 3.1 8B doubled base-model scores across 19 financial datasets [arXiv:2505.19819]. Your current sentiment cook is using a 2019 knife.
2. **Your labeling bottleneck is already solved** — that's the core finding of the annotators paper you ingested: GPT-4-class annotation + spot-checking the uncertain ~35% replaces human labelers at ~1/10th the cost with *higher* F1. You also own a unique asset: months of Morgans sentiment history aligned with actual price outcomes. That's training data nobody else has.
3. **It fits your hardware plan.** Training: a 7B QLoRA run on 50k examples costs ~$2-5 on an L4 spot ($0.376/hr) or ~$11-18 on an A100 spot — your $300/90-day GCP credits cover dozens of experiments. Inference: 7B Q4 needs ~5GB VRAM (any used RTX 3090 at ~$900 crushes it at ~87 tok/s); ModernBERT needs no GPU at all.
4. **Measurable in dollars.** Swap the new model into Morgans, A/B the ensemble's signal quality on the 18 rotation tickers, and the backtest tells you if it pays. No leap of faith.

## Why NOT Path 2 (trading-signal LLM) yet

The 2025-26 literature turned notably skeptical, and the papers you ingested agree:

- A 20-year, 100+ symbol systematic backtest found LLM strategies "generally do not consistently outperform buy-and-hold" — too conservative in bull markets, too aggressive in bears [arXiv:2505.07078].
- The "Alpha Illusion" paper (May 2026) argues reported LLM-agent alpha "should not be treated as deployment evidence" — lookahead bias is endemic because the model has literally read the history it's being backtested on [arXiv:2605.16895]. FinAgent's 92% ARR on TSLA is exactly the kind of number to apply this lens to.
- The research-ideas paper you ingested adds the killer constraint: **LLM self-evaluation is near-random (53% consistency)**. An LLM trading agent is an idea generator wearing a judge's robe. Use LLMs to *propose* (signals, alpha formulas), and let your backtester's IC be the only judge.
- Cost: per-decision frontier-LLM reasoning on a 60-second trading cycle is economically silly; fine-tuned small models for this are still research-grade (TRADING-R1, Fin-R1 — and Fin-R1's commercial license is unverified).

**The Alpha-GPT path captures most of Path 2's upside with none of the training cost:** LLM seeds candidate alpha formulas → your backtester scores them (IC) → you refine interactively. Their result: human feedback more than tripled the information coefficient of seed alphas (0.58% → 2.23%). Your edge is that you know your data — that loop is where "trying to make money, not just make projects" lives.

## The build plan (Path 1, concrete)

**Phase A — Dataset (1-2 weekends, ~$30-50 in API costs)**
- Pull 20-40k texts from your own pipeline: Morgans news headlines, Reddit posts, SEC filing snippets for your 18 tickers (+ sector peers for breadth).
- Annotate with a frontier model using the annotators-paper recipe: structured prompt, 3-class labels (bearish/neutral/bullish) + confidence; spot-check the low-confidence ~35% yourself. Add Financial PhraseBank (4.8k, note non-commercial license — use for eval, not the commercial training set) and TFNS (9.5k) as public seasoning.
- Hold out a gold eval set (~1k, hand-checked) — this eval set is worth more than the model.

**Phase B — Train on GCP ($300 credits, 90-day window)**
- `g2-standard-8` (1× L4 24GB) spot @ ~$0.376/hr. QLoRA rank-8, the FinLoRA-validated config: 4-8h per run on the 7B ≈ **$2-4/run**.
- Train both: Qwen2.5-7B-Instruct (LoRA) and ModernBERT (full fine-tune, minutes on the same box).
- Compare on the gold set: if ModernBERT is within ~2 F1 points of the 7B, ship ModernBERT to the VPS (ONNX, CPU, effectively free). Else ship the 7B.

**Phase C — Deploy & verify**
- Cloud-serve the winner until credits run dry, then: ModernBERT → VPS CPU directly; 7B Q4 → local GPU (used RTX 3090 ~$900 is the value pick; 4060 Ti 16GB ~$500 is the budget floor at ~34 tok/s).
- Wire into Morgans as the FinBERT replacement, A/B against VADER+FinBERT on live collection for 2-4 weeks, and let ensemble backtest IC decide. (No self-grading LLMs — the judge is the backtest.)

**Phase D (later, optional) — Alpha-GPT loop** using the same backtest harness, as the Path-2 substitute.

## Key risks
- **License hygiene:** Qwen2.5-7B is Apache 2.0 ✓; Financial PhraseBank is CC BY-NC-SA (keep it eval-only for a commercial product); Fin-R1 license unverified — skip.
- **GCP credits expire in 90 days** — the constraint is the calendar, not the $300. Do Phase A before opening the GCP account.
- **Data leakage:** when backtesting the upgraded sentiment signal, only use sentiment generated from texts published *before* each trading decision — same lookahead discipline the Alpha Illusion paper demands.

*Full citations live in the research notes; headline sources: arXiv:2512.00946 (Dec 2025), arXiv:2505.19819 FinLoRA (May 2025), arXiv:2602.06370 (Feb 2026, encoder-vs-LLM cost), arXiv:2505.07078 (May 2025), arXiv:2605.16895 Alpha Illusion (May 2026), Aguda et al. 2024 (annotators), Wang et al. 2023 (Alpha-GPT), cloud.google.com pricing (fetched June 2026).*
