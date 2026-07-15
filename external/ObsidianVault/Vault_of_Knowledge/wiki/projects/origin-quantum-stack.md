---
type: project
tags: [quantum-computing, learning, qpanda, origin-quantum, project]
created: 2026-05-07
updated: 2026-05-07
status: active
---

# Project: Learn the Origin Quantum Stack

**Goal**: Build working fluency in Origin Quantum's (本源量子) tooling — enough to read the book examples, run them, modify them, and eventually compose original quantum programs against the Origin Quantum cloud platform.

**Why this stack**: The user's stated commitment as of 2026-05-07. The choice trades portability (QPanda code doesn't move to Qiskit cleanly) for depth in a specific, vertically integrated ecosystem with first-party hardware. Worth treating that as the design parameter, not the constraint.

**Primary text**: [[wiki/sources/2026-05-06-quantum-computing-introduction|Guo, Chen, Guo (2019) — Introduction to Quantum Computing and Programming]]. Every example in the book is implemented in this stack.

---

## Stack components

| Component | What it is | When you need it |
|---|---|---|
| **QPanda** | C++ quantum SDK — the programming substrate | All circuit construction, simulation, hardware execution |
| **pyQPanda** | Python bindings to QPanda | Practical day-to-day work; almost everything in this project |
| **QRunes** | Origin's quantum programming language (text format) | Reading/writing portable circuit descriptions |
| **VQNet** | Quantum machine learning framework | Ch 5 / variational circuit ML |
| **Qurator** | IDE / visualization tool | Debugging circuits visually |
| **ChemiQ** | Quantum chemistry application | VQE / molecular simulation work |
| **Origin Quantum cloud (本源量子云平台)** | Cloud access to real and simulated quantum chips | Anything that needs real hardware execution; available since 2017 |

---

## Learning roadmap (mapped to the textbook)

Read in this order, not in book-cover order. The book's table of contents is pedagogically sequenced for a Chinese university course; for a builder learning the stack, the appendices come first.

### Phase 0 — Math foundations (Appendix 1)
Linear algebra you need *before* anything else makes sense:
- Sets, mappings, vector spaces, basis, inner products
- Matrices: addition, multiplication, invertibility, similarity
- Eigenvalues / eigenvectors, Hermitian matrices, unitary matrices
- Linear operators, matrix representations, outer products, projection operators

If this is review, skim. If it's new, work problems — the rest of the book assumes fluency.

### Phase 1 — Tooling install (Appendix 2)
Get the stack running on your machine before reading any quantum content:
- App 2.1 — QPanda compile environment, download QPanda 2, compile, install
- App 2.2 — pyQPanda system requirements, configuration, install
- App 2.3 — VQNet Python package install, run a simple VQNet example
- App 2.4 — Qurator: design philosophy, prep, quick start, feature tour

By end of phase: can run Hello-World pyQPanda script and a VQNet toy example.

### Phase 2 — Quantum mechanics fundamentals (Ch 2)
What you're actually programming:
- 2.1.1 Quantum systems
- 2.1.2 Observables and measurement in computational basis
- 2.1.3 Composite systems and joint measurement
- 2.2.1 Quantum program principles
- 2.2.2 Quantum control flow — the `if` and `while` of quantum programs

Anchor everything to running pyQPanda code. Don't read this purely on paper.

### Phase 3 — Background and orientation (Ch 1)
Now the framing chapter actually makes sense:
- 1.1 Three questions: what / why / who
- 1.2 History of QM and quantum computing
- 1.3 Quantum software landscape — languages, SDKs, cloud platforms

### Phase 4 — Hardware reality (Ch 3)
Skim, don't drill — but know what your code is targeting:
- 3.1 Quantum chips — superconducting, semiconductor, other paradigms
- 3.2 Hardware support — chip support systems, control systems
- 3.3 The full quantum computer architecture and program-to-device flow

### Phase 5 — Algorithms in QPanda (Ch 4)
This is where most of the actual learning happens:
- 4.1 Dev environment recap (QPanda, QRunes, Origin cloud)
- 4.2 Quantum algorithms intro + classical-quantum hybrid framing
- 4.3 **Deutsch–Jozsa** — first non-trivial quantum algorithm. Implement on cloud and in QPanda.
- 4.4 **Grover** — unstructured search, quadratic speedup
- 4.5 **QAOA** — combinatorial optimization (max-cut, SAT, optimization)
- 4.6 **VQE** — quantum chemistry, ground states. Pair with ChemiQ (App 3).
- 4.7 **Shor** — factoring, RSA. Mostly a "see how the masterpiece is built" milestone; you won't run this at meaningful scale.

### Phase 6 — Quantum chemistry workflow (Appendix 3)
After VQE in Ch 4.6, immediately work through ChemiQ:
- 3.1 ChemiQ install
- 3.2 Application examples
- 3.3 Interface intro
- 3.4 Non-gradient-descent VQE code example

This is the most concrete shippable workflow in the whole stack — molecular ground states.

### Phase 7 — Frontier topics (Ch 5)
Once everything else is solid:
- 5.1 Testing quantum system noise with QPanda
- 5.2 Quantum machine learning (read with skepticism — 2019 was early)
- 5.3 Single-amplitude and partial-amplitude virtual machines
- 5.4 Compiling quantum programs to different physical chips

---

## Milestones (rough)

- [ ] **Milestone 1**: pyQPanda installed, "hello qubit" Bell state circuit runs locally
- [ ] **Milestone 2**: Run Deutsch–Jozsa locally and on the Origin Quantum cloud
- [ ] **Milestone 3**: Working Grover's search for a small toy problem
- [ ] **Milestone 4**: VQE for H₂ ground state via ChemiQ
- [ ] **Milestone 5**: A simple variational circuit trained with VQNet
- [ ] **Milestone 6**: Compile the same program to two different chip simulators and compare results

---

## Open practical questions

- Is the Origin Quantum cloud platform usable from outside China without friction? Account creation, payment, latency. Worth verifying before depending on it for milestones 2+.
- Is the book-version of QPanda still current, or has the API drifted? Check actual release vs. 2019 textbook examples — expect breakage and be ready to adapt.
- Is there an English-language Origin Quantum docs / community to lean on, or is the path mostly through Chinese sources? Will affect how fast Phase 1 goes.

---

## Cross-links

- [[wiki/concepts/quantum-computing]] — broader concept page
- [[wiki/concepts/quantum-machine-learning]] — relevant for Phase 7
- [[wiki/areas/ml-research/_overview]] — VQNet sits at the QC × ML intersection
- [[wiki/areas/biomedical/_overview]] — ChemiQ / VQE workflow is the bridge to drug-discovery applications
- [[wiki/areas/entrepreneurship/_overview]] — financial QAOA applications, eventual product opportunities
- [[wiki/sources/2026-05-06-quantum-computing-introduction]] — primary text
