---
type: concept
tags: [quantum-computing, ml, qml, emerging-tech]
created: 2026-05-06
updated: 2026-05-06
status: stub
---

# Quantum Machine Learning

The intersection of [[wiki/concepts/quantum-computing|quantum computing]] and machine learning — using quantum circuits as differentiable function approximators (variational quantum circuits, quantum neural networks) or using quantum subroutines (HHL for linear systems, quantum kernel methods) inside otherwise classical ML pipelines.

As of 2019 — the date of [[wiki/sources/2026-05-06-quantum-computing-introduction|the source that introduced this to the wiki]] — QML was preliminary, dominated by toy problems. As of 2026 the field has moved, but I haven't ingested current sources yet. This page is a stub to be expanded when newer material arrives.

The relevant architectural question: does QML offer real advantages for tasks where classical deep learning already works? Most expert opinion as of the early 2020s was *not for now* — classical deep learning's bitter-lesson advantage of "scale + data" is hard to compete with, and quantum hardware noise wipes out most theoretical edges. The bet is that a few specific problems (e.g. learning quantum-natural functions in chemistry / physics) will eventually show quantum-native advantage.

See also: [[wiki/concepts/quantum-computing]], [[wiki/areas/ml-research/_overview]].
