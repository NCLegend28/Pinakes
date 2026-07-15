---
type: source
tags: [paper, mathematics, symbolic-regression, interpretability, ml-research, sheffer-stroke, universal-primitive]
created: 2026-05-09
updated: 2026-05-09
status: active
source_file: eml_function.pdf
source_fingerprint: |
  All elementary functions from a single operator

  Andrzej Odrzywołek
  Institute of Theoretical Physics, Jagiellonian University, 30-348 Krakow, Poland
  E-mail: andrzej.odrzywolek@uj.edu.pl

  April 7, 2026

  Abstract
---

# Odrzywołek (2026) — All elementary functions from a single operator

## Summary

A single-author paper from a theoretical physicist at Jagiellonian University proving — by systematic exhaustive search and constructive verification — that the binary operator `eml(x, y) = exp(x) − ln(y)`, paired with the constant `1`, is sufficient to express *every* standard elementary function (sin, cos, sqrt, all transcendentals, all arithmetic operations, and constants including `e`, `π`, `i`). This is the **continuous-mathematics analogue of NAND** — a Sheffer stroke for elementary functions, where one was previously assumed not to exist. Beyond the structural fact, the paper shows that because every elementary expression becomes a binary tree of identical EML nodes (grammar: `S → 1 | eml(S, S)`), the architecture supports gradient-based symbolic regression: parameterized EML trees trained with Adam, weights "snapping" to exact symbolic values, recovering closed-form formulas from numerical data. Worth treating as a *real* discovery — not because it changes computation in 2026, but because it forces a re-examination of what "elementary function" even means and gives a new architecture for legible, interpretable ML.

## Key takeaways

- **EML is a Sheffer stroke for continuous math.** NAND alone reconstructs all of Boolean logic; until this paper, it was unclear whether continuous math admitted a comparable single-operator basis. EML + 1 does. The two-button calculator `(1, eml)` is functionally equivalent to a full scientific calculator. That a single binary operation suffices was, in Odrzywołek's words, "not anticipated."
- **Neural networks are a special case of EML trees.** Section 5: "since standard activation functions are themselves elementary, any conventional neural network is a special case of an EML tree architecture." Reframes the entire deep-learning architecture space as a subset of a more uniform tree structure. Implication for [[wiki/areas/ml-research/_overview|ML research]]: the discovered-circuit family worth searching may be far smaller than current neural-architecture-search assumes.
- **Symbolic regression by gradient descent — actually demonstrated, with limits.** Trained-weight snapping recovers exact closed-form expressions from numerical data: 100% recovery at depth 2, ~25% at depths 3–4, <1% at depth 5, 0% from 448 attempts at depth 6. So the technique is real but currently shallow. This is exactly the lane bookmarked under [[wiki/concepts/prediction-markets|prediction-market modeling]] — recovering laws from data — and it sits in the same family as AI Feynman (Tegmark) and PySR (Cranmer). See [[wiki/concepts/symbolic-regression]].
- **Complex intermediates are intrinsic, like in QM.** "Just as quantum computing uses complex amplitudes to compute real probabilities, EML uses complex intermediates to compute real elementary functions." Trigonometric functions emerge from EML only via complex-domain computation through Euler's formula. The author tried and failed to find a real-domain-only Sheffer for elementary functions. This is a real structural rhyme with [[wiki/concepts/quantum-computing|quantum computing]], not just a metaphor.
- **EML is not unique — it has cousins.** EDL (`exp(x)/ln(y)` with constant `e`), `−EML` swapped (`ln(x) − exp(y)` with constant `−∞`), and a hypothesized ternary variant `T(x,y,z) = e^x/ln(z) × ln(z)/e^y` requiring no distinguished constant. The author explicitly frames this paper as the tip of an iceberg.
- **The "primitive sufficiency" axis is orthogonal to scale.** This paper's discovery doesn't fit the [[wiki/concepts/scaling-laws|scale-is-all-you-need]] framing at all — it's a different axis entirely. A 14-parameter level-2 master EML formula expresses any depth-2 elementary function exactly. For comparison: a transformer with trillions of parameters has an equivalent EML tree depth of ~40. The paper isn't claiming EML beats transformers; it's claiming there's a representation regime where exactness matters more than capacity.
- **AI-assisted but author-original.** Explicit AI-use disclosure: Claude, Grok, Gemini, ChatGPT used for editing and coding only. The discovery itself was systematic exhaustive search by the author, with one verification subroutine translated to Rust by GPT Codex 5.3 for a 1000× speedup. Useful real-world data point on the [[wiki/areas/ml-research/_overview|agent-engineering thread]]: AI accelerated the workflow but did not produce the insight.

## Notable quotes

- "The EML operator may be the tip of an iceberg."
- "any conventional neural network is a special case of an EML tree architecture."

## Wiki pages touched

- [[wiki/concepts/eml-operator]] — new, primary concept page
- [[wiki/concepts/symbolic-regression]] — new, broader context page
- [[wiki/concepts/kolmogorov-arnold-networks]] — new stub (referenced from paper)
- [[wiki/people/andrzej-odrzywolek]] — new person stub
- [[wiki/areas/ml-research/_overview]] — added universal-primitives / interpretability thread
- [[wiki/areas/entrepreneurship/_overview]] — added symbolic-regression-on-trading-data lane
- [[wiki/concepts/scaling-laws]] — added "primitive sufficiency" as orthogonal axis
- [[wiki/concepts/quantum-computing]] — added complex-intermediates rhyme
- [[wiki/self/open-questions]] — added universal-primitive meta-question
