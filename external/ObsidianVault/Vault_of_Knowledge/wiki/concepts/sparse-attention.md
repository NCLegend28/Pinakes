---
type: concept
tags: [ml, attention, llm-architecture, efficiency]
created: 2026-05-06
updated: 2026-05-06
status: stub
---

# Sparse Attention

A family of attention mechanisms that selectively attend to a subset of the context rather than computing full O(L²) dense attention. The motivation is straightforward: at very long contexts, most tokens are irrelevant to any given query, so a well-designed sparse pattern can match dense-attention quality at a fraction of the cost.

Variants differ in how the sparse pattern is chosen:

- **Static patterns** (Longformer, BigBird): pre-defined local + global windows. Cheap, but blind to content.
- **Routed / top-k** (DSA, [[wiki/sources/2026-05-06-msa-memory-sparse-attention|MSA]]): learned routing query selects the top-k most relevant chunks per attention head. Content-aware, end-to-end trainable. The main cost is the routing computation itself, which has to stay sub-quadratic.
- **Hash-based** (Reformer): cluster keys by locality-sensitive hashing, attend within clusters. Asymptotically efficient but tricky to make stable.

The contribution of MSA is showing that top-k sparse attention plus document-wise position encoding plus tiered KV storage can scale to 100M-token contexts on commodity (2× A800) hardware — three orders of magnitude beyond where prior sparse-attention work plateaued.

See also: [[wiki/concepts/long-context-memory]], [[wiki/areas/ml-research/_overview]].
