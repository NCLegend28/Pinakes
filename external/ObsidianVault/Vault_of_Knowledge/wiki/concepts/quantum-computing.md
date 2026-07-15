---
type: concept
tags: [quantum-computing, physics, computing, emerging-tech]
created: 2026-05-06
updated: 2026-05-09
status: active
---

# Quantum Computing

Computation that exploits quantum-mechanical phenomena — superposition, entanglement, interference — to manipulate information in ways classical computers cannot. The unit is the qubit, which (unlike a classical bit) can occupy a superposition of |0⟩ and |1⟩ simultaneously. With *n* qubits, the state space is 2ⁿ-dimensional, and a well-designed algorithm can extract value from that exponential space without explicitly enumerating it.

## Why now

Two converging pressures:

1. **Classical compute is hitting walls.** Moore's law has slowed; the heat-dissipation effect ("热耗效应") and size effect ("尺寸效应") both bite at sub-5nm process nodes. Adding more transistors costs more thermal headroom than it returns in throughput.
2. **Specific high-value problems are exponentially hard classically.** Molecular simulation, integer factoring, certain optimization problems. For these, even a moderately sized quantum machine could beat the largest classical supercomputers — *if* the algorithms work and the hardware is good enough.

This mirrors a pattern visible elsewhere: when scale plateaus, architecture takes over. See [[wiki/concepts/long-context-memory|MSA's argument for memory-architecture over parameter scale]] for the same shape of argument inside ML.

## What quantum is good at (and not)

**Strong asymptotic speedups (proven, but require fault-tolerant hardware that doesn't yet exist):**
- Integer factoring → Shor's algorithm (breaks RSA at scale)
- Unstructured search → Grover's algorithm (quadratic speedup)

**NISQ-era hybrid algorithms (run on today's noisy hardware):**
- Quantum chemistry → VQE (variational quantum eigensolver). Find ground states of molecules. Most promising near-term commercial application — drug discovery, materials science, catalyst design.
- Combinatorial optimization → QAOA (quantum approximate optimization algorithm). Portfolio optimization, scheduling, maximum-cut problems. See [[wiki/areas/entrepreneurship/_overview|finance applications]].
- Quantum machine learning → see [[wiki/concepts/quantum-machine-learning]].

**What quantum is *not* good at:**
- General-purpose computing — most code doesn't have quantum-amenable structure.
- Tasks dominated by I/O or memory bandwidth.
- Anything where the input/output dwarfs the computation.

## Hardware paradigms

- **Superconducting** (Google, IBM, Origin Quantum) — qubits as Josephson junctions cooled to millikelvin. Currently dominant. Coherence times limit circuit depth.
- **Semiconductor / quantum dot** (Intel, Origin Quantum) — qubits as electrons in silicon. Promises better scaling and integration with existing fab infrastructure.
- **Trapped ion** (IonQ, Quantinuum) — qubits as individual ions held in electromagnetic traps. Higher fidelity, slower gates.
- **Photonic** (PsiQuantum, Xanadu) — qubits as photons. Room-temperature operation possible.
- **Topological** (Microsoft, long-game) — qubits as anyons. Theoretically far more error-resistant, practically still unproven.

No paradigm is clearly winning yet.

## Industry landscape (as of 2019, dated)

Western: Google, IBM, Intel, Microsoft running large quantum teams. D-Wave commercializing quantum annealing.

Chinese: Alibaba, Baidu, [[wiki/sources/2026-05-06-quantum-computing-introduction|Origin Quantum (本源量子)]] — the last spun out of the CAS Quantum Information Key Lab at USTC, with their own QPanda SDK, QRunes language, VQNet (QML), Qurator (IDE), ChemiQ (quantum chemistry), and quantum cloud platform.

The competitive structure looks similar to early classical computing: vertically integrated chip-makers also building the software stack. Picking a stack is a real commitment — code written in QPanda doesn't port to Qiskit/Cirq/PennyLane without rewrites, and vice versa. The user's current bet is on Origin Quantum specifically — see [[wiki/projects/origin-quantum-stack]].

## Open questions

- When does quantum advantage actually materialize in a useful, commercial sense — vs. carefully constructed benchmark problems? Still uncertain in 2026.
- Will fault-tolerant quantum computing arrive at a relevant scale, or will NISQ-era hybrid algorithms be the entire story for the next decade?
- Does the [[wiki/concepts/scaling-laws|scaling-laws]] framework have an analogue for quantum systems? Qubit count, coherence time, and gate fidelity are independent axes — what does the loss surface look like?

## A structural rhyme worth holding

[[wiki/sources/2026-05-09-eml-elementary-functions|Odrzywołek (2026)]] notes that the [[wiki/concepts/eml-operator|EML operator]] requires complex intermediates to compute real elementary functions (trig functions emerge only via Euler's formula through `ln(−1) = iπ`); attempts to find a real-domain-only Sheffer for elementary functions failed. His framing: *"Just as quantum computing uses complex amplitudes to compute real probabilities, EML uses complex intermediates to compute real elementary functions."* This isn't metaphor — both regimes appear to require the complex domain to access certain real-valued targets. Worth holding open: is this a deeper fact about computation, or a coincidence of two specific constructions?

See also: [[wiki/concepts/quantum-machine-learning]], [[wiki/concepts/eml-operator]], [[wiki/areas/ml-research/_overview]], [[wiki/areas/biomedical/_overview]], [[wiki/sources/2026-05-06-quantum-computing-introduction]].
