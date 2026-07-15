---
type: concept
tags: [llm, trading, multimodal, vision, finance, agent-engineering]
created: 2026-06-11
updated: 2026-06-11
status: stub
---

# Multimodal Trading Agents

*LLM-based trading systems that ingest visual market data (Kline candlestick charts, trading charts) alongside textual news and numerical prices — rather than flattening everything to text first.*

Created from [[wiki/sources/2026-06-11-finagent-multimodal-trading-agent|FinAgent (Zhang et al., 2024)]], which is the first trading agent to process Kline and trading charts via GPT-4V alongside news and price data. The architectural argument: certain patterns in candlestick structure (triangles, breakouts, head-and-shoulders) are visually legible but awkward to express numerically, and a multimodal LLM may extract signal from them more naturally.

**What's established**: FinAgent reports strong aggregate improvement over text-only LLM agents in backtest. What's not cleanly isolated: whether the visual modality specifically contributes over and above better text processing and the dual-level reflection system.

**Relation to Financio**: Financio currently processes sentiment text and OHLCV prices. Adding Kline chart images as input would require a multimodal LLM in the signal pipeline. The engineering cost is real; the incremental signal benefit is plausible but unproven. File under "worth tracking, not worth building yet."

The key portable idea from FinAgent is not the multimodal input per se but the **retrieval-task/decision-task separation** — generating distinct query fields for memory retrieval vs downstream decision-making. That principle applies regardless of modality.

See also: [[wiki/concepts/multi-agent-systems]], [[wiki/concepts/domain-specific-llms]], [[wiki/areas/entrepreneurship/_overview]].
