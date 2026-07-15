---
type: concept
tags: [mathematics, sheffer-stroke, universal-primitive, symbolic-regression, interpretability, ml-architecture]
created: 2026-05-09
updated: 2026-05-09
status: active
---

# The EML Operator

The binary operator `eml(x, y) = exp(x) − ln(y)`. Discovered by Andrzej Odrzywołek (2026, [[wiki/sources/2026-05-09-eml-elementary-functions|paper]]) to be the first known **Sheffer-stroke for elementary functions** — a single binary operator that, paired with the constant `1`, generates every standard elementary function: arithmetic (`+`, `−`, `×`, `/`), all transcendentals (`sin`, `cos`, `tan`, `log`, `exp`, hyperbolics, inverses), radicals, and constants including `e`, `π`, `i`. Continuous-mathematics analogue of NAND.

## Why this matters

Boolean logic has had its single-sufficient operator since 1913 (Sheffer; NAND, equivalently NOR). For continuous math no such primitive was known — calculators have always exposed many distinct buttons because their underlying functions were thought to require many distinct primitives. Odrzywołek shows by systematic exhaustive search that this assumption was wrong: a calculator with two buttons (`1` and `eml`) can compute everything a full scientific calculator can. The pre-existing reductions (logarithm tables → slide rule; Euler's exp/ln representation; algebraic adjunctions) had cut the count down from many to a handful, but no further. EML closes the gap.

The deeper claim is structural, not engineering: elementary functions are members of a much simpler class than previously recognized.

## Construction

```
eml(x, y) = exp(x) − ln(y)
```

With this and the constant `1`, every elementary expression becomes a binary tree of identical EML nodes. The grammar is trivial and context-free:

```
S → 1 | eml(S, S)
```

Concrete examples (from the paper, where `E` denotes `eml`):

```
e   = E(1, 1)               # depth 1, RPN: 11E
e^x = E(x, 1)
ln(z) = E(1, E(E(1, z), 1)) # depth 3, RPN: 11xE1EE  (K = 7)
```

Every elementary tree has leaf count `2^n` for some depth `n`; the EML representation is *uniform*, isomorphic to full binary trees / Catalan structures. This is what makes the next part possible.

## Symbolic regression by gradient descent

Because EML trees are uniform — every node is the same operator with two inputs — they can be parameterized as differentiable circuits and trained with standard optimizers. Each input slot becomes a linear combination `α + β·x + γ·f` (with `f` the previous EML output), and the parameters are passed through a Gumbel-softmax to make the choice of `1` / variable / previous-output continuous. Train with Adam, then "snap" weights to the nearest vertex (0 or 1) of the simplex.

When the generating law is elementary, snapped weights yield a fitting error at machine epsilon squared (~10⁻³²) — *exact symbolic recovery* of the closed-form expression, not an approximation.

Empirical recovery rates from the paper (over 1000+ runs):

| Tree depth | Blind recovery rate |
|---|---|
| 2 | 100% |
| 3–4 | ~25% |
| 5 | <1% |
| 6 | 0/448 attempts |

So the technique is real but currently shallow. Above depth 4 the optimization landscape becomes too rugged for blind initialization. The paper notes that perturbed-initialization runs (start near a known correct EML tree, add Gaussian noise) recover to exact values 100% of the time even at depths 5–6 — meaning *the basins of attraction exist*, finding them from random init is what's hard.

This sits in the [[wiki/concepts/symbolic-regression|symbolic-regression]] family alongside AI Feynman (Tegmark), PySR (Cranmer), and deep symbolic regression (Petersen et al.) — but with the unique property of having a *complete and uniform* search grammar, not a heterogeneous one.

## Relationship to neural networks

> Since standard activation functions are themselves elementary, any conventional neural network is a special case of an EML tree architecture.

This is the line that should make ML researchers stop. Current neural networks can learn symbolic algebra and digit-level arithmetic, but their internal mechanisms are opaque. EML trees, by construction, are *legible as elementary function expressions* when training succeeds — a form of interpretability conventional networks structurally cannot offer.

The cost: depth scales unfavorably. A transformer with ~10¹² parameters has equivalent EML tree depth around 40, well beyond current symbolic-regression reach. EML is not currently competitive on capacity. It's interesting as an *architectural lower bound on legibility*.

## Cousins (open frontier)

Odrzywołek explicitly frames EML as the tip of an iceberg. Two confirmed variants:

- **EDL**: `edl(x, y) = exp(x) / ln(y)` with constant `e`
- **−EML (swapped)**: `−eml(y, x) = ln(x) − exp(y)` with constant `−∞`

One hypothesized:

- **Ternary T**: `T(x, y, z) = e^x / ln(z) × ln(z) / e^y`, where `T(x, x, x) = 1` may eliminate the need for any distinguished constant — a "true" universal primitive with no terminal symbol pairing.

A univariate continuous Sheffer (single unary operator generating all elementary functions while also serving as a neural activation) is open.

## The complex-numbers point

EML internally requires complex arithmetic to compute real elementary functions — trig functions emerge only via Euler's formula through `ln(−1) = iπ`. Odrzywołek tried to find a real-domain-only Sheffer (using pairs of trig/hyperbolic inverses instead of `exp`/`ln`) and found nothing. The use of complex intermediates appears intrinsic, not incidental.

His framing: "Just as quantum computing uses complex amplitudes to compute real probabilities, EML uses complex intermediates to compute real elementary functions." This is a real structural rhyme with [[wiki/concepts/quantum-computing|quantum computing]] — both regimes seem to require the complex domain to access certain real-valued targets.

## Hardware angle

Because every EML expression has the topology of a binary tree of identical nodes, the operator is a candidate analog-computing primitive — the math equivalent of building an entire digital chip from NAND gates. Could be implemented on FPGA or as an analog circuit with a single repeated element. Speculative, but the path is visible.

## Cross-links

- [[wiki/sources/2026-05-09-eml-elementary-functions]] — primary source
- [[wiki/concepts/symbolic-regression]] — broader context
- [[wiki/concepts/scaling-laws]] — orthogonal axis (primitive sufficiency vs. scale)
- [[wiki/concepts/quantum-computing]] — complex-intermediates rhyme
- [[wiki/concepts/kolmogorov-arnold-networks]] — related interpretability-via-architecture line
- [[wiki/people/andrzej-odrzywolek]] — author
- [[wiki/areas/ml-research/_overview]]
- [[wiki/areas/entrepreneurship/_overview]] — symbolic regression on market data lane
