---
type: source
tags: [quantum-computing, textbook, chinese-tech, qpanda, origin-quantum]
created: 2026-05-06
updated: 2026-05-07
status: active
source_file: 量子计算与编程入门 (Quantum Computing).pdf
source_fingerprint: |
  量子计算与编程入门 / Introduction to Quantum Computing and Programming. 郭国平 陈昭昀 郭光灿 著. 科学出版社. 2019. 本源量子系列教材.
---

# Introduction to Quantum Computing and Programming (Guo, Chen, Guo, 2019)

**Summary**: A 2019 Chinese-language textbook from Origin Quantum (本源量子) — a company spun out of the CAS Quantum Information Key Laboratory at USTC — co-authored by founder Guo Guoping (郭国平), Chen Zhaoyun (陈昭昀), and CAS academician Guo Guangcan (郭光灿). Five chapters move from background (what/why quantum) → quantum mechanics fundamentals → hardware (their own superconducting and semiconductor chip designs) → quantum algorithms and programming (Deutsch-Jozsa, Grover, QAOA, VQE, Shor) → frontier topics (noise testing, quantum machine learning, single/partial-amplitude virtual machines, cross-chip compilation). Every example is implemented in Origin Quantum's own stack — QPanda (C++/Python SDK), pyQPanda, QRunes (their language), VQNet (QML), Qurator (IDE), ChemiQ (quantum chemistry), and the Origin Quantum cloud platform. **For the user's stated goal of learning the Origin Quantum stack specifically, this is the canonical primary text** — the rest of the wiki should treat it that way. See [[wiki/projects/origin-quantum-stack]] for the structured learning project this seeded.

**Key takeaways**:
- **The motivation is "Moore's Law is ending."** Chapter 1 frames quantum as the next paradigm because classical compute is hitting heat-dissipation limits and size-effect (nanometer-scale physics) walls. This is the same architecture-over-scale argument that surfaces in [[wiki/sources/2026-05-06-msa-memory-sparse-attention|MSA]] for LLMs — when raw scale plateaus, architecture takes over. Worth holding both at once.
- **Application taxonomy from Ch 1.** The book lists seven near-term application areas: big data search, quantum simulation (esp. biopharma), quantum chemistry (drug discovery, personalized medicine, genomics), financial services (portfolio optimization, fraud detection), AI / quantum ML, agriculture (catalyst design for ammonia synthesis), and quantum cloud. Three of these directly intersect existing user areas: [[wiki/areas/biomedical/_overview|biomedical]] (chemistry, drug discovery), [[wiki/areas/entrepreneurship/_overview|entrepreneurship]] (financial services — connects to [[wiki/self/goals|the trading bot goal]]), and [[wiki/areas/ml-research/_overview|ML research]] (quantum machine learning).
- **First-party tooling is the whole point.** Every code example, virtual machine, and algorithm walkthrough uses Origin Quantum's tools — QPanda, pyQPanda, QRunes, VQNet, Qurator, ChemiQ, and the Origin Quantum cloud platform. Working through the book *is* working through the stack. The structured roadmap lives in [[wiki/projects/origin-quantum-stack]].
- **Hybrid classical-quantum is the practical paradigm.** Chapter 4 spends significant time on quantum-classical hybrid algorithms (QAOA, VQE) — these are NISQ-era algorithms designed for noisy intermediate-scale quantum hardware. They're not the asymptotic-speedup algorithms (Shor, Grover) — they're the algorithms that might actually do useful work on 50–100 qubit machines. If the user wants to *use* quantum computing in the next 3 years, this is the relevant family.
- **Quantum chemistry / VQE is the most concrete near-term win.** Chapter 4.6 covers VQE and quantum chemistry simulation in detail. Drug discovery is the clearest commercial application — D-Wave CTO Geordie Rose's $310B figure (cited in the preface) for pharma+chemistry+biotech is from this lineage. If the user's [[wiki/areas/biomedical/_overview|biomedical interest]] is real, VQE is the most practically interesting algorithm in the book — and ChemiQ is the Origin tool that wraps it.
- **Chinese quantum industry context.** The preface lists Alibaba, Baidu, and Origin Quantum as the major Chinese players competing with Google/IBM/Intel/Microsoft. The book is itself an artifact of that industrial push — it's a recruitment and ecosystem-building document as much as a textbook. Knowing this is part of speaking the dialect.
- **2019 means dated on AI/quantum interfaces.** Quantum machine learning has moved fast since 2019; the book's coverage of QML and quantum neural networks (and the VQNet examples) is preliminary. The fundamentals still apply, but supplement with newer sources before betting on a specific QML technique.
- **Mathematical appendix is the on-ramp.** Appendix 1 covers the linear algebra foundation (sets, vector spaces, matrices, eigenvalues, Hermitian matrices, linear operators) needed to read the rest. Appendix 2 walks through QPanda / pyQPanda / VQNet / Qurator installation and first runs. Read these *first*, in that order, before Chapter 1.

**Notable quotes**:
- "量子计算可以改变世界" — "Quantum computing can change the world"
- "下一代计算模式的重大变革也即将到来" — "The next-generation computing paradigm shift is coming"

**Wiki pages touched**:
- [[wiki/concepts/quantum-computing]] (created)
- [[wiki/concepts/quantum-machine-learning]] (created — stub)
- [[wiki/projects/origin-quantum-stack]] (created — learning project)
- [[wiki/areas/biomedical/_overview]] (updated — adds quantum chemistry / drug discovery thread)
- [[wiki/areas/entrepreneurship/_overview]] (updated — adds Chinese quantum industry, financial-services applications)
- [[wiki/self/open-questions]] (updated — adds quantum-vs-scale question)
