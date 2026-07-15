---
type: concept
tags: [ml-research, interpretability, neural-architecture, symbolic-regression]
created: 2026-05-09
updated: 2026-05-09
status: stub
---

# Kolmogorov–Arnold Networks (KAN)

A neural architecture (Liu et al., ICLR 2025) that replaces the fixed activation functions on neurons with *learnable univariate functions on edges*, motivated by the Kolmogorov–Arnold representation theorem (any multivariate continuous function can be written as a composition of univariate functions and addition). Each "weight" is a learned 1D spline rather than a scalar.

The result: networks whose internal mechanism is directly readable. Once trained, you can extract the learned univariate functions and inspect them as plots — and in many cases snap them to closed-form expressions (`sin`, `exp`, polynomials), recovering symbolic structure from the trained weights.

Surfaced as a stub because the [[wiki/concepts/eml-operator|EML operator]] paper cites KAN ([11] in the references) for the same family of "interpretability via architecture" claim — both architectures attempt to make trained networks legible *by construction* rather than by post-hoc explanation. KAN currently has the larger empirical footprint; EML is the more radical structural claim.

## Cross-links

- [[wiki/concepts/eml-operator]] — uniform-tree alternative in the same family
- [[wiki/concepts/symbolic-regression]] — KAN sits in the inductive-bias-deep-learning branch
- [[wiki/areas/ml-research/_overview]]
