---
type: concept
tags: [ml, llm-architecture, memory, long-context, retrieval]
created: 2026-05-06
updated: 2026-05-06
status: active
---

# Long-Context Memory in LLMs

The problem of giving language models access to context windows that approach human-scale lifetime memory — estimated by cognitive scientists at roughly 10⁹ bits, or ~200–300M tokens at 3–5 bits per token. As of 2026, frontier LLMs typically support effective contexts of 128K–1M tokens, leaving a 100–1000× gap between current architectures and human-scale memory. Closing this gap matters for long-running agents, persona-stable role-playing, large-corpus summarization, and biomedical applications like Digital Twins where the relevant unit is a patient's full medical history.

## Three paradigms

Following the taxonomy laid out in [[wiki/sources/2026-05-06-msa-memory-sparse-attention|Chen et al. (2026)]]:

**Parameter-based memory.** Bake new knowledge directly into model weights via continual pre-training, LoRA fine-tuning, or test-time training architectures like Titans. *Strengths*: deep semantic integration, full architectural compatibility. *Weaknesses*: catastrophic forgetting when knowledge conflicts, hard to scale capacity (you can't fit 100M tokens into 4B params), expensive to update.

**External storage-based memory.** Retrieval-Augmented Generation (RAG) and its descendants (MemAgent, HippoRAG2). Store text in an external database, retrieve relevant chunks via embedding similarity, inject into the context window. *Strengths*: lifetime-scale capacity, avoids catastrophic forgetting, easy to update. *Weaknesses*: retrieval is decoupled from the model's internal representation space — the metric for "relevant" is a separate embedding model, not the LLM's own attention. This caps precision and prevents end-to-end optimization.

**Latent state-based memory.** Operate directly on the model's KV cache or hidden states. Includes sparse-attention variants (DSA, MSA), linear-attention compressions (RWKV, DeltaNet, Mamba), and learned memory compressors (MemGen, ParallelComp). *Strengths*: stays in the model's native representation space, end-to-end differentiable. *Weaknesses*: linear-attention variants catastrophically forget at extreme lengths; sparse-attention variants historically couldn't scale to 100M tokens until [[wiki/concepts/sparse-attention|MSA]] cracked it via document-wise RoPE and tiered storage.

## Why this is hard

Three forces fight each other:

1. **Capacity** — fitting more tokens. Bounded by VRAM × compression ratio.
2. **Precision** — retrieving the *right* tokens. Bounded by retrieval architecture.
3. **End-to-end trainability** — optimizing capacity and precision jointly against the downstream task. Bounded by whether the retrieval step is differentiable.

Most architectures are good at one or two. RAG nails capacity and trainability of the *generator*, but the retriever is a separate model. Linear attention nails capacity and end-to-end-ness, but loses precision. Dense attention nails precision and trainability, but caps capacity at O(L²). MSA's contribution is that all three can be satisfied simultaneously, at least at the 100M scale.

## The train-short / infer-long problem

A specific architectural detail worth knowing: standard Rotary Position Embeddings (RoPE) use monotonically increasing position IDs across the full sequence. If you train on 64K tokens and infer on 100M, position IDs at inference are 1500× outside the training distribution — and accuracy collapses. Fixes include:

- **Document-wise RoPE** (MSA): reset position IDs to 0 at the start of each retrieved document. Train and inference see the same per-document position range; only the *count* of documents differs.
- **Position interpolation / NTK-aware scaling**: rescale position frequencies at inference. Works for moderate extension but breaks at extreme scales.
- **YaRN, ALiBi, etc.**: alternative position encoding schemes designed for length extrapolation from the start.

## Open questions

- Can sparse-attention memory architectures handle highly interlinked evidence (many cross-document references), or is some form of external structured memory still needed for that case? [[wiki/sources/2026-05-06-msa-memory-sparse-attention|MSA's authors flag this as a limitation.]]
- How does the [[wiki/concepts/scaling-laws|scaling laws framework]] interact with memory architecture? Kaplan et al. assumed a fixed-context regime; the right scaling laws for memory-augmented models are an open question.
- Does any of this generalize to multimodal memory (images, audio across years), or are the techniques specific to text?

See also: [[wiki/concepts/sparse-attention]], [[wiki/concepts/scaling-laws]], [[wiki/areas/ml-research/_overview]].
