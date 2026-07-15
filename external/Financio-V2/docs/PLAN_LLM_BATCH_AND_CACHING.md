# Plan: Anthropic Batch API + Prompt Caching for the Tech Agent Backtest

**Status:** Phases 0–2 + 4 implemented and unit-tested (38/38 green). Empirical API verification (Phase 0 smoke tests + Phase 4 sync-vs-batch comparison) blocked pending Anthropic credit top-up. Phase 3 (live-agent caching) deferred — see §10.
**Owner:** Don Guapo
**Date:** 2026-05-02
**Related:** `docs/INTEGRATION_ARCHITECTURE.md`, NVDA Phase 1 backtest report (2026-04-29)

---

## 1. Strategic context

Phase 1 NVDA backtest cost ~$15–20 retail on Opus 4.6 for 125 day-records. To validate the LLM-as-signal hypothesis we need to extend that experiment to a 5-ticker basket, then likely a regime-split rerun, then a Phase-2 sentiment-on-vs-off comparison. At straight retail, that's a $200–500 burn before we know whether the agent is exploitable.

Two Anthropic-side levers reduce that bill ~75% with no change to signal quality:

- **Batch API** — 50% off list price for any request that can wait up to 24 hours. Backtests are the textbook fit: we're processing historical dates, not serving a live trader.
- **Prompt caching** — 90% off cached input tokens. The tech-agent system prompt is ~4.2K stable tokens (persona, frameworks, output schema, constraints). Across hundreds of day-records, that's the bulk of input spend.

The two stack: Batch is applied at the request-submission level, caching is applied at the prompt-construction level. They are independent.

**Out of scope for this plan:** the Haiku screening tier (separate plan once plumbing is in), Phase 2 P&L simulation, anything in the dashboard.

**Analogy.** We're laying a second pipe alongside the existing one. The old pipe (live LangChain `ChatAnthropic` path, sequential async backtest) keeps flowing exactly as it does today. The new pipe (native Anthropic SDK, batch submit + poll) is bigger and ~75% cheaper. A valve at the harness entry (`execution_mode` config) decides which pipe a given run uses. Live trading never sees the new pipe.

---

## 2. Constraint check: working code untouched unless required

This is the operating principle for the entire plan. Concretely:

1. **Live trading hot path** (`financio_src/agents/tech/agent.py`, the LangGraph `_node_analyze`) — **zero changes** in Phases 0–2. Phase 3 adds prompt caching as an *opt-in* config flag; default behavior is unchanged.
2. **Existing backtest behavior** (`harness.py` default execution) — **zero changes** to default code path. The new batch executor is a parallel module gated by `BacktestConfig.execution_mode`. Setting nothing → exact current behavior.
3. **LangChain `ChatAnthropic`** — **untouched**. We do not upgrade or remove it. The new code uses the native `anthropic` SDK directly. Two SDKs coexist (LangChain wraps anthropic anyway, so this is not a new transitive dep — only a new direct one).
4. **SQLite cache layer** (`llm_cache.py`) — **extended, not replaced**. We add a new table for batch metadata; the existing `llm_cache` table keeps its schema. Existing rows are still hits.
5. **Output formats** (JSONL + Parquet, live-compatible schema) — **identical**. The batch path produces the same `BacktestRecord` shape so all downstream metrics/report code is untouched.

If any step in the plan turns out to require touching live code, that's a flag to stop and reassess.

---

## 3. Architecture decision: native `anthropic` SDK for the new path

**Why not extend LangChain.** `langchain_anthropic.ChatAnthropic` does not expose the Message Batches API at all. Prompt caching via cache_control headers requires a recent version (>= 0.3.0) and a non-trivial message-content-block restructure that's awkward through the LangChain abstraction. To get Batch we have to drop down to the native SDK regardless — given that, it's cleaner to use the native SDK for the entire new path rather than mix abstractions.

**Why not rip out LangChain.** It's load-bearing for the live agent's LangGraph integration. Replacing it touches the live trading path. Constraint #1 says no.

**Result.** Two SDKs coexist:

- `langchain_anthropic.ChatAnthropic` — used by live agent, used by the existing default backtest path. Untouched.
- `anthropic.Anthropic` (native) — used by the new batch executor and the new prompt-caching wrapper. New code only.

Both SDKs read `ANTHROPIC_API_KEY` from the same env var. No config divergence.

---

## 4. File-by-file change inventory

| File | Change | Lines touched | Why required |
|---|---|---|---|
| `financio_src/requirements.txt` | Add `anthropic>=0.40.0` (pin); pin `langchain_anthropic>=0.3.0` only if Phase 0 verification shows installed version lacks cache_control | +1 to +2 | New dep; pin existing to known-good if needed |
| `financio_src/agents/tech/backtest/llm_client_native.py` | **NEW** — thin wrapper around `anthropic.Anthropic` that builds messages with `cache_control` markers on the stable system prompt | New file, ~80 lines | Native SDK entry point; encapsulates caching logic |
| `financio_src/agents/tech/backtest/batch_executor.py` | **NEW** — submit batch, poll status, fetch results, map back to `BacktestRecord`s | New file, ~250 lines | Core batch implementation |
| `financio_src/agents/tech/backtest/batch_state.py` | **NEW** — SQLite table `batch_jobs(batch_id, run_id, ticker, created_at, status, request_count, output_path)` for resumability across process restarts | New file, ~60 lines | Batch jobs are async and may outlive the harness process |
| `financio_src/agents/tech/backtest/harness.py` | Add `execution_mode: Literal["sync", "batch"] = "sync"` to `BacktestConfig`. Add a single dispatch branch in the `run()` method: if `batch`, hand off to `BatchExecutor`. **Default unchanged.** | ~15 lines added, 0 removed | Single dispatch point; existing path is the default |
| `financio_src/agents/tech/backtest/llm_cache.py` | Add one method `get_many(keys: list) -> dict` for bulk pre-flight cache lookup before batch submission. Existing methods untouched. | +20 lines, 0 removed | Avoid submitting batch requests for prompts already in cache |
| `financio_src/agents/tech/backtest/runner.py` | Add `--execution-mode {sync,batch}` CLI flag, default `sync`. | ~5 lines | Surface the toggle |
| `financio_src/agents/tech/backtest/cost.py` | Add `discount_factor` and `cached_input_tokens` parameters to cost calculation. Default discount = 0 (no change to existing call sites). | ~15 lines added | Accurate cost reporting for the new path |
| `financio_src/agents/tech/config.py` | Add `prompt_cache_enabled: bool = False` to `TechAgentConfig` (Phase 3 only). Default off → live agent unchanged. | +1 line (Phase 3) | Opt-in toggle for live caching |
| `financio_src/agents/tech/agent.py` | Phase 3 only: if `cfg.prompt_cache_enabled`, route through native SDK wrapper instead of `ChatAnthropic`. Conditional, additive. | ~10 lines (Phase 3) | Opt-in caching for live |
| `tests/test_batch_executor.py` | **NEW** — unit + integration tests | New file, ~150 lines | Required for confidence |
| `docs/INTEGRATION_ARCHITECTURE.md` | Append a section on the dual-SDK choice and execution modes | ~30 lines | Architecture doc upkeep |

**Total surface area:** 5 new files, ~6 edited files. No deletions. No live trading code touched until Phase 3, and Phase 3 is opt-in and additive only.

---

## 5. Phased implementation

Each phase is independently shippable and independently reversible. Don Guapo can stop after any phase and still have a working system better than the starting state.

### Phase 0 — Verification & dependency setup (1–2 hours)

The cheapest steps that de-risk everything downstream.

**Tasks:**

1. Inspect installed `langchain_anthropic` version in `.venv`: `python -c "import langchain_anthropic; print(langchain_anthropic.__version__)"`. Confirm whether it's >= 0.3.0 (needed only for Phase 3 live caching, not for backtest).
2. Add `anthropic>=0.40.0` to `financio_src/requirements.txt`. Run `uv pip install anthropic>=0.40.0` (or `uv pip sync` per CLAUDE.md). Confirm `from anthropic import Anthropic` imports cleanly.
3. Confirm Batch API supports `claude-opus-4-6` and `claude-haiku-4-5` by submitting a single trivial 1-request batch with each model and reading status. (Total cost: <$0.01.) This is the empirical check — Anthropic's docs are usually right but a model rolling off Batch support has happened before.
4. Confirm prompt caching works on Opus 4.6 with the actual tech-agent system prompt: send one cached request, send a second identical one, verify `cache_read_input_tokens > 0` in the response usage block. (Total cost: <$0.05.)
5. Document the verification results inline in this plan (append a "Phase 0 verification log" section).

**Acceptance:** All four verification artifacts captured. If any fail, stop and reassess — the plan assumes these primitives work.

**Rollback:** None needed — we only added a dep. `uv pip uninstall anthropic` reverses it.

---

### Phase 1 — Native SDK wrapper with prompt caching (2–3 hours)

Build the foundation: a clean native-SDK call site that handles cache_control correctly. No batch yet.

**Tasks:**

1. Create `llm_client_native.py` exposing one function:
   ```
   async def call_with_cache(
       client: AsyncAnthropic,
       model: str,
       system_prompt: str,        # cached
       user_prompt: str,          # not cached
       temperature: float,
       max_tokens: int,
   ) -> ResponseEnvelope
   ```
   Constructs the `messages.create` call with `system=[{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}]`. Returns a structured envelope with `text`, `input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`, `output_tokens`, `stop_reason`.
2. Add unit tests with a mocked `anthropic` client: assert cache_control marker is on the system block, not the user block; assert envelope shape.
3. Add an integration test (gated by env var `RUN_LIVE_LLM_TESTS=1`) that hits the real API with a 100-token system prompt three times in a row and asserts the third call shows `cache_read_input_tokens > 0`.

**Acceptance:** Unit tests pass. Integration test (when run manually) shows cache hits on repeat calls.

**Rollback:** Delete the new file. Nothing else touched.

---

### Phase 2 — Batch executor (4–6 hours, the meat of the work)

The new pipe.

**Tasks:**

1. Create `batch_state.py` with a `BatchJobStore` class wrapping a SQLite table for batch_id persistence. Schema in the file inventory above. Methods: `create()`, `update_status()`, `get_pending()`, `get_by_run_id()`.
2. Create `batch_executor.py` with a `BatchExecutor` class. Public surface:
   ```
   class BatchExecutor:
       def __init__(self, cfg: BacktestConfig, cache: LLMCache, client: AsyncAnthropic)
       async def run(self, inputs: list[HistoricalInputs], rag_context: str, run_id: str) -> list[BacktestRecord]
   ```
   Internal flow:
   - Build all (system_prompt, user_prompt) pairs from inputs
   - Bulk pre-flight cache check via `cache.get_many()` — pull hits out of the work list, prepare `BacktestRecord`s for them immediately
   - For misses: build batch requests with `custom_id = f"{ticker}|{date_iso}"` so we can map results back. Each request uses cache_control on the system prompt (so even within a single batch, the cache is shared across requests).
   - Submit batch via `client.messages.batches.create(requests=...)`. Persist `batch_id` to `batch_state` so we can resume.
   - Poll `client.messages.batches.retrieve(batch_id)` with exponential backoff (start 30s, cap 5min). Log progress. Most backtest batches complete in <1hr in practice; the 24h ceiling is the hard SLA.
   - On completion, stream results via `client.messages.batches.results(batch_id)`. For each result: parse, build `BacktestRecord`, write to cache, append to records list.
   - Merge cache hits + batch results, sort by date, return.
3. Wire dispatch into `harness.py`: in `Backtest.run()`, before the existing `asyncio.gather`, check `self.cfg.execution_mode`. If `"batch"`, instantiate `BatchExecutor` and delegate; otherwise fall through to the existing path. The existing path's code is unchanged — it just becomes one branch of an `if`.
4. Wire CLI flag in `runner.py`: `--execution-mode {sync,batch}`, default `sync`.
5. Tests:
   - Unit: `BatchExecutor` with a mocked `AsyncAnthropic` covering happy path, partial cache hits, batch-failed status, individual-request-errored within a successful batch, network timeout during polling, resumption after process crash (instantiate executor with an existing pending `batch_id` in `batch_state`, verify it picks up polling instead of resubmitting).
   - Integration (gated by env var, costs ~$0.50): real 5-day NVDA batch end-to-end. Compare output records against a sync run on the same dates — the parsed `direction` and `score` fields should be identical (modulo LLM nondeterminism — temperature 0.1 means small variance is possible; assert structural equality, not value equality).

**Acceptance:**
- Unit tests pass with >85% line coverage on new modules.
- Integration test produces a valid Parquet/JSONL output with the same schema as a sync run.
- A backtest run with `--execution-mode batch` on a 1-month window completes successfully and the cost report (Phase 4) shows ~50% reduction vs. baseline.
- Run with no flag = exact current behavior. (Verify with a diff of the JSONL output across sync runs before/after this PR — should be byte-identical given cache hits.)

**Rollback:** Set `execution_mode="sync"` (the default). All new files can be deleted without touching anything else. The harness `if/else` dispatch reverts to the original single code path with one line change.

---

### Phase 3 — Prompt caching for live agent (opt-in, 2 hours)

Smaller win, but free safety net once the wrapper exists.

**Tasks:**

1. Add `prompt_cache_enabled: bool = False` to `TechAgentConfig`. Default off.
2. In `agent.py`'s `_node_analyze`, branch: if `self.cfg.prompt_cache_enabled`, use `llm_client_native.call_with_cache` instead of `ChatAnthropic.ainvoke`. Wrap the response in the same shape `_node_analyze` already expects so no downstream code changes.
3. Test: enable the flag in a dev run, point at paper-trading Alpaca, run for one full market session. Compare cost report before/after.

**Acceptance:** With flag enabled, live cost report shows ≥60% reduction on input tokens after first scan. Trade decisions are unchanged (paper-mode comparison).

**Rollback:** Set the flag back to `False`. One config line.

**Note:** This phase is genuinely optional. If Phase 2 saves enough money to fund the validation experiments, Phase 3 can be deferred indefinitely.

---

### Phase 4 — Cost telemetry & validation (1–2 hours)

How we know it actually worked.

**Tasks:**

1. Extend `cost.py` to compute and report:
   - Standard cost (input + output tokens × list price)
   - Cached input savings (cached tokens × 0.9 × input price)
   - Batch discount (final cost × 0.5 if `execution_mode="batch"`)
   - Net effective cost
2. Append a "Cost summary" block to the existing backtest report (in `report.py`).
3. Run a controlled comparison:
   - Baseline: NVDA, 1-month window, sync mode, no caching
   - Treatment: NVDA, same 1-month window, batch mode, caching on
   - Both should produce structurally equivalent records (same direction calls, scores within reasonable LLM variance at temperature=0.1).
   - Cost reduction: target 70–80% net.
4. Update this plan with actual measured savings.

**Acceptance:** Cost report shows expected discount stack. A side-by-side run on the same window shows equivalent signal output at 70%+ cost reduction.

---

## 6. Sequencing & total effort

Realistic estimate: **1–2 working days of focused effort**, spread however suits Don Guapo. Phases 0, 1, 2, 4 are the critical path (Phase 3 is optional). Each phase ends in a shippable state — partial completion is not a problem.

Ordering rationale:
- Phase 0 first because it's cheap and could surface a blocker (e.g., Opus 4.6 unsupported in Batch).
- Phase 1 before 2 because Phase 2 reuses the wrapper.
- Phase 2 before 3 because the bigger savings live there and we want them faster.
- Phase 4 anywhere after 2; before is meaningless (nothing to measure).

---

## 7. Risks & open questions

**Risks:**

- **Batch latency is opaque.** Anthropic's "up to 24h" is a ceiling, not a typical. In practice batches usually complete in 1–60 minutes, but there's no SLA shorter than 24h. Mitigation: persist `batch_id` to disk so a stale batch survives a process restart; the polling loop is resumable, not a single long-running coroutine.
- **Cache invalidation on prompt drift.** If we tweak the system prompt, the cache misses for the first call after the change. This is fine — it just means the *first* request after each prompt change pays full price. Worth noting in commit messages: small system-prompt edits during experimentation will reset the cache.
- **Two SDKs in the dependency tree.** Slight bloat, low risk of conflict (LangChain already depends on `anthropic` transitively). Watch for version pin clashes during `uv pip sync`.
- **Batch result ordering is not guaranteed.** We must use the `custom_id` we set per request to map results back, not request order. Spelled out in the executor design.
- **Per-request errors inside a successful batch.** Anthropic returns the batch as "completed" even if individual requests within it errored. The executor must check each result's `result.type` field and propagate failures to `BacktestRecord.parse_error`, matching the existing error-handling contract.

**Open questions for Don Guapo before execution:**

1. **Batch poll cadence.** Default is exponential backoff 30s → 5min cap. If you want shorter loops for snappier dev feedback (at the cost of more polling API calls, which are free but generate noise), say so.
2. **CI integration.** Should the batch integration test run in CI on every PR (~$0.50/run, 1–60 min latency), or be gated to manual `make test-llm-integration`? Recommend manual — Batch latency is incompatible with PR feedback loops.
3. **Fall-through behavior on batch failure.** If a batch submission fails (e.g., Anthropic outage), should the executor automatically fall back to the sync path, or hard-fail and let Don Guapo retry manually? Recommend hard-fail with a clear error message — silent fallback hides cost surprises.

---

## 8. Definition of done

- [x] Phase 0 verification log appended to this doc (§9)
- [x] All new files merged with passing unit tests (38/38 green: 11 client + 19 batch + 8 cost)
- [ ] Integration test demonstrates a real batch run on NVDA 1-month *(blocked on credits)*
- [x] Default `python -m financio_src.agents.tech.backtest.runner ...` command preserves existing behavior — verified by `BacktestConfig.execution_mode` defaulting to `"sync"` and the harness `if/else` keeping the original gather() path untouched. Tests `test_all_cache_hits_skips_batch_submission` and `test_mixed_hits_and_misses_submits_only_misses` confirm cache-row format compatibility between sync and batch
- [ ] `--execution-mode batch` produces structurally equivalent output at measured 70%+ cost reduction *(blocked on credits)*
- [x] Cost report block added to backtest summary (`report.py` accepts `cost_summary=` kwarg; `runner.py` populates it via `cost.report_cost`)
- [ ] One-paragraph note added to `docs/INTEGRATION_ARCHITECTURE.md` explaining the dual-SDK choice *(deferred — non-blocking)*
- [ ] This plan doc updated with actuals (measured cost reduction, any deviations from plan) *(blocked on credits — will fill §9 table after first batch run)*

## 10. Phase 3 status: deferred, not abandoned

Phase 3 (opt-in prompt caching for the LIVE agent) is intentionally not implemented in this pass. Reasoning:

- The immediate research goal is cheap backtest experimentation, not lower live-trading cost. Phases 1+2+4 cover that goal completely.
- Live agent runs at 15-min cadence — even a 70% cost reduction there is small in absolute dollars compared to running 5-ticker walk-forward backtests on Opus.
- Implementation is small (~10 lines + 1 config flag) and entirely additive. It can be done in a single sitting whenever the live cost shows up on a bill.
- All the prerequisites (the `llm_client_native` wrapper, prompt-cache-aware system blocks) are now in place — Phase 3 becomes a 30-minute add-on rather than a new project.

Trigger to revisit: when live trading is running 5+ tickers in production AND the monthly Anthropic bill exceeds ~$200/mo. Until then, deferred is the right call.

---

## 9. Phase 0 verification log

Executed 2026-05-02. **Partially blocked by Anthropic account credit balance** — the empirical API checks cannot complete until credits are added. All non-API checks passed. The verification script (`outputs/phase0_verify.py`) is idempotent and resumable; rerun it after topping up.

| Check | Result | Notes |
|---|---|---|
| `langchain_anthropic` installed version | ✅ **1.4.0** | Far above the >=0.3.0 floor; supports `cache_control` natively |
| `anthropic` SDK installed | ✅ **0.85.0** in venv, 0.97.0 in sandbox; pinned `>=0.40.0` in `requirements.txt` | Already present, just unpinned |
| Model string `claude-opus-4-6` accepted by API | ✅ **Implicit pass** | Got `400 invalid_request_error: credit balance too low`, not `model not found` — API validated the model before billing check |
| Model string `claude-haiku-4-5-20251001` accepted by API | ✅ **Implicit pass** | Same as above |
| Batch API end-to-end with Opus 4.6 | ⏸ **BLOCKED — credit balance** | Submission rejected at billing layer. Rerun after top-up. |
| Batch API end-to-end with Haiku 4.5 | ⏸ **BLOCKED — credit balance** | Same |
| Prompt caching returns `cache_read_input_tokens > 0` on repeat call | ⏸ **BLOCKED — credit balance** | Same. Code path validated against SDK 0.97.0 docs in dry-run. |

**To resume:** add credits at https://console.anthropic.com/settings/billing, then `cd outputs && python3 phase0_verify.py`. Cost on rerun: <$0.10.
