---
type: project
tags: [eml, neural-ode, symbolic-regression, polymarket, prediction-markets, trading-bot, project]
created: 2026-05-10
updated: 2026-05-10
status: active
schema_verified:
  subgraph: 2026-05-10
  gamma_openapi: 2026-05-10  # partial spec — /markets and /events not documented but Market schema is
implementation:
  repo: ~/projects/polymarket-bot
  package: src/polybot_research/eml_node/
  entry_points: [eml-schema-check, eml-phase0, eml-status]
  scaffolded: 2026-05-10
---

# Project: EML-Parameterized Neural ODE on Polymarket LMSR Time Series

**Goal**: Train an [[wiki/concepts/eml-operator|EML]]-parameterized Neural ODE on LMSR-implied-probability time series from resolved Polymarket markets. Attempt symbolic recovery of the right-hand-side dynamics. Treat any successfully snapped formula as a falsifiable trading hypothesis and backtest it on held-out resolved markets. End state: either a published-quality negative result ("market dynamics are not depth-≤4 elementary") or a real, interpretable, edge-bearing model.

**Why this stack**:
This project sits at the intersection of four active threads in this vault:

1. [[wiki/concepts/symbolic-regression]] — research-side payoff (does EML-NODE work in the wild?)
2. [[wiki/concepts/prediction-markets]] — domain-side payoff (LMSR is a known mechanism, so the data has structure)
3. [[wiki/self/goals|The trading-bot goal]] — revenue path if the model has any predictive power
4. [[wiki/areas/ml-research/_overview|Agent-engineering]] — the harness around the experiment is itself a Claude Code project

The [[wiki/insights/eml-as-ml-substrate|EML-as-substrate insight]] identifies Neural ODE RHS parameterization as the cleanest first experiment because (a) ODE machinery already exists, (b) the search space is small (depth 2–4 covers most plausible price dynamics), and (c) the failure mode degrades gracefully to a normal Neural ODE.

> ⚠️ This project deliberately operates inside the [[wiki/self/patterns|named attention-loop pattern]]. The bookmarks-dump audit showed that "Polymarket bot" is a saturated engagement-bait topic. This project is *not* "I built a bot, watch the money roll in" — it's a research-shaped experiment with a defined falsification criterion. Hold the line on that distinction.

---

## Stack

| Component | What it is | Why this choice |
|---|---|---|
| **Python 3.12** | Runtime | Per [[CLAUDE.md global standards]]; latest stable |
| **uv** | Package & env manager | Per global standards; reproducible installs |
| **PyTorch 2.x** | ML framework | `complex128` support required for EML; mature autograd |
| **torchdiffeq** | Neural ODE library | Battle-tested adjoint-based ODE solvers |
| **PySR** | Baseline symbolic regression | Comparison baseline against EML; same family of question |
| **mpmath** / **NumPy** | Numerical verification | Cross-check EML evaluation across implementations (per the paper) |
| **Polymarket Subgraph** | Data source | GraphQL API for historical resolved-market trade and price series |
| **Doppler** | Secrets management | Per [[CLAUDE.md]] tier 2; Polymarket / wallet keys never on disk |
| **DuckDB** or **Parquet** | Local data store | Fast columnar storage for OHLC-style price series |
| **MLflow** | Experiment tracking | Per the AI/ML governance section of the global standards |

---

## Phased plan

Phase numbering matches dependency order — don't skip ahead.

### Phase 0 — Data acquisition and cleaning
*Goal: a clean, versioned dataset of resolved Polymarket markets with implied-probability time series.*

#### Verified data sources (as of 2026-05-10)

- **Polymarket Gamma Markets API** (REST, source-of-truth for *what to pull*):
  Base URL likely `https://gamma-api.polymarket.com`; `/markets` and `/events` endpoints exist in production but are not in the partial OpenAPI doc reviewed 2026-05-10. Spike Phase 0.1 to confirm endpoint, filter params, pagination, and auth requirement (likely no auth for the public discovery endpoint). Schema verified via OpenAPI: `Market` has `conditionId`, `clobTokenIds`, `question`, `outcomes`, `outcomePrices`, `closed`/`closedTime`, `endDate`, `volume*`, `liquidity*`, `negRisk`, `marketType`, `umaResolutionStatus` — every metadata field needed.
- **The Graph subgraph** (CTF Exchange orderbook indexer, source-of-truth for *trade-by-trade prices*):
  `https://gateway.thegraph.com/api/subgraphs/id/7fu2DWYK93ePfzB24c2wrP94S3x4LGHUrQxphhoEypyY`
  Auth: `Authorization: Bearer $GRAPH_API_KEY` (key in `.env`, never inline). Schema verified 2026-05-10.
- **CTF Conditional Tokens contract** (on-chain Polygon): fallback for resolution data if Gamma's `outcomePrices` / `umaResolutionStatus` is insufficient. Likely unnecessary.

#### Verified subgraph schema

The subgraph indexes orderbook activity only — no market metadata, no resolution outcomes (those come from Gamma). Five entities matter:

| Entity | What it actually carries | How we use it |
|---|---|---|
| `OrderFilledEvent` | Per-fill records: `id`, `transactionHash`, `timestamp`, `orderHash`, `maker`, `taker`, `makerAssetId`, `takerAssetId`, `makerAmountFilled`, `takerAmountFilled`, `fee`, `blockNumber`, `side`, **`price` (BigDecimal, pre-computed)** | Source of price time series. The `price` field is already computed — no need to derive from amounts. |
| `MarketData` | Join table only: `id`, `condition`, `outcomeIndex`. Despite the name, no historical data. | Maps `assetId` → `(condition, outcomeIndex)`. Required to know which token represents YES vs NO. |
| `Orderbook` | Per-asset cumulative aggregates: `tradesQuantity`, `buysQuantity`, `sellsQuantity`, `collateralVolume`, `scaledCollateralVolume`, `averageTradeSize`, `totalFees`. Despite the name, no depth/bid/ask data. | **Strategic filter**: query first to identify high-activity assets *before* pulling expensive fill data. Cuts query budget 10–100×. |
| `OrdersMatchedEvent` | Per-tx batch wrapper | Confirms batch-fill pattern; rarely queried directly |
| `Account` | Per-wallet aggregates | Phase 5+ behavioral copy-trading lane |

> ⚠️ **Pre-computed `price` and `side` are the big wins** — eliminates the entire amount-arithmetic / unit-conversion class of bugs from Phase 0. Verified 2026-05-10 via schema introspection.

#### Substeps

- **0.0 — Schema introspection (codified, completed 2026-05-10)**. Run the introspection queries against any subgraph version change to detect schema drift. Save responses as `data/schema_snapshots/YYYY-MM-DD.json` and diff against last snapshot. Two queries:
  ```graphql
  { __type(name: "OrderFilledEvent") { fields { name type { name kind ofType { name kind } } } } }
  { __schema { types { name kind } } }
  ```
  Plus the Gamma OpenAPI spec snapshot (saved separately, refresh when `info.version` bumps).
- **0.1 — Spike Gamma `/markets` endpoint.** ✅ Verified 2026-05-10. Base URL `https://gamma-api.polymarket.com`, GET `/markets`, no auth required, returns array of `Market` objects matching the OpenAPI schema. Confirmed working filter: `closed=true&limit=N`. Default sort is oldest-first; pass ordering params (`order=endDate&ascending=false` or equivalent) for recent-first.

  ⚠️ **Two issues surfaced from the spike that the plan must absorb**:

  **(a) AMM vs CLOB era filter is mandatory.** Polymarket migrated from an FPMM AMM to a CLOB ~2022. The subgraph we use (`OrderFilledEvent`) indexes CLOB only — AMM-era markets have zero fills there. Filter signals on each Gamma `Market`: skip if `fpmmLive: true`; keep if `enableOrderBook: true` AND `volume1yrClob > 0` (or some equivalent CLOB-volume threshold). Most efficient final filter: **`volume1yrClob > $X`** as a single threshold catches both "had a CLOB" and "had real activity."

  **(b) `outcomePrices` semantics ✅ verified for UMA-era markets (2026-05-10).** On three recent UMA-resolved markets (closed Feb–Mar 2026), `outcomePrices` reliably encodes the binary payout: `["0", "1"]` when NO won, `["1", "0"]` when YES won. Index 0 = YES payout, index 1 = NO payout. `umaResolutionStatuses: ["proposed"]` accompanies these on resolved markets. The 2020-era `["0", "0"]` we saw earlier was a pre-UMA artifact. **Resolution ground truth is `outcomePrices` parsed as JSON, with payout values strictly in {0, 1} for resolved binary markets** — no CTF contract reads or alternate sources needed.

  **(c) Gamma silently ignores unknown filter params.** Probe with `fpmm_live=false` returned a market with `fpmmLive: true`. Implication: trust only filters known to be honored (`closed`, `limit`, `order`, `ascending` — all verified). Do all other filtering client-side in an auditable pass.

  **(d) `fpmmLive` is `null`, not `false`, on new CLOB-only markets.** The AMM/CLOB filter predicate must be "skip if `fpmmLive == true`" — not "keep if `fpmmLive == false`" (which would silently drop everything).

  **(e) `volume1yrClob` is `null` on very recent markets** (e.g. closed within ~60 days). Don't use it as a single liquidity filter — combine with `volume` or `enableOrderBook == true` to avoid dropping fresh markets.
- **0.2 — Pull resolved-market universe from Gamma.** Paginated call: `closed=true`, `order=endDate&ascending=false`, `limit=` whatever the max is. *Use only verified filter params (`closed`, `limit`, `order`, `ascending`) — Gamma silently ignores unknown ones.* Capture full `Market` objects to `data/gamma_markets_raw_v1.json`. Then post-filter client-side in a single auditable pass:
  - Drop `fpmmLive == true` (AMM-era; no subgraph data)
  - Drop `marketType != "normal"` (binary only)
  - Drop `negRisk == true` (multi-outcome bundles)
  - Drop markets where `enableOrderBook != true` AND `(volume1yrClob ?? volume1moClob ?? 0) < $X` (combined liquidity filter that doesn't punish fresh markets)
  - Drop markets where `outcomePrices` parsed as JSON ≠ exactly `["0", "1"]` or `["1", "0"]` (filters out unresolved/disputed/pre-UMA markets)
  
  This *replaces* the previous "Orderbook subgraph filter" step — Gamma is the discovery surface; subgraph is the price-history surface.
- **0.3 — Extract join keys and metadata from Gamma response.** For each market, parse `clobTokenIds` (JSON-encoded array of two token IDs for binary markets) and `conditionId`. Build a `markets_index.parquet` keyed by `conditionId` with columns: `question`, `outcomes`, `outcomePrices`, `endDate`, `closedTime`, `volume`, `liquidity`, `umaResolutionStatus`, `clobTokenIds`. Drop markets with malformed or missing token IDs.
- **0.4 — Pull and bucket fills from subgraph.** For each token ID in `clobTokenIds`, query `OrderFilledEvent` filtered by `makerAssetId` or `takerAssetId`, sorted by `(blockNumber, transactionHash)`. Bucket the `price` field into 1-hour intervals (start; revisit). Handle batch-matched fills inside the same `transactionHash` consistently. (The `MarketData` subgraph entity is now redundant — Gamma already gives us the asset → condition mapping — but keep it as a verification cross-check.)
- **0.5 — Sanity cross-check.** For each market, compare the final pre-resolution price from our bucketed series to Gamma's `outcomePrices[1]` (assuming index 1 = YES). Disagreement > epsilon flags a bucketing or join bug — investigate before proceeding.
- **0.6 — Snapshot to versioned Parquet** with descriptive stats (per-market: volatility, time-to-resolution, fill density, gap distribution).
- **0.7 — Hold out 20% of conditions** (stratified by category if possible) as a final test set; never look at them until Phase 5.

**End-of-phase deliverable**: `data/polymarket_resolved_v1.parquet` + `data/markets_index.parquet` + `data_card.md` documenting provenance, filtering, schema snapshot references, and known caveats. Also `data/schema_snapshots/2026-05-10.json` (subgraph) and `data/schema_snapshots/2026-05-10-gamma.json` (Gamma OpenAPI) as baselines.

### Phase 1 — Baselines
*Goal: establish reconstruction MSE numbers for non-EML approaches, so EML has something to be measured against.*

- 1.1 — Trivial baselines: zero-order hold, linear interpolation, EWMA. Just to anchor the loss scale.
- 1.2 — Standard Neural ODE with MLP RHS (3 layers, 64 hidden units, `tanh` activations). Train on 60% of markets; validate on 20% (the dev set, not the test set).
- 1.3 — PySR baseline: run on a sample of 10 markets, see what closed-form expressions it surfaces. This is for *scientific* comparison, not for the eventual EML benchmark.
- 1.4 — Record all baseline results in MLflow with full hyperparams.

**End-of-phase deliverable**: a `baselines_report.md` with reconstruction MSE distributions across markets and per-market scatter plots.

### Phase 2 — EML primitive (verified against the paper)
*Goal: reproduce the paper's depth-2 100% snap-recovery result on synthetic data before attempting market data.*

- 2.1 — Implement `eml(x, y) = exp(x) − ln(y)` in PyTorch with `complex128` dtype; handle `ln(0)` and overflow per the paper's recipe (clamp arguments and outputs of `exp`)
- 2.2 — Implement parameterized EML tree with Gumbel-softmax-gated input choice (logits → simplex via softmax)
- 2.3 — Implement training recipe: Adam → hardening phase (push softmax weights toward 0/1) → snap to nearest vertex
- 2.4 — Verify on synthetic data: train on `(x, ln(x))` pairs, check that snapped tree exactly recovers `ln(z) = eml(1, eml(eml(1, z), 1))` (the paper's depth-3 ln formula)
- 2.5 — Stress-test depths 2, 3, 4 on a battery of elementary-function targets; record recovery rates and compare to the paper's 100% / 25% / <1% numbers

**End-of-phase deliverable**: `eml_torch/` package + a `verification_report.md` showing recovery rates match the paper within statistical noise. **Gate: do not proceed to Phase 3 if recovery rates are materially worse than the paper's.** Most likely cause of failure here is a complex-arithmetic / branch-cut bug.

### Phase 3 — EML-RHS Neural ODE
*Goal: drop-in replace the Phase 1 MLP RHS with an EML tree; train end-to-end on Polymarket data.*

- 3.1 — Wrap the EML tree from Phase 2 as a `torch.nn.Module` with the right input/output signature for `torchdiffeq.odeint`
- 3.2 — Start with depth 2, single-input (just price → derivative). Train on the same 60% train split as the baseline.
- 3.3 — Sweep depths 3 and 4. Record convergence behavior, any NaN issues.
- 3.4 — Multi-input variant: include trade-volume and time-to-resolution as additional inputs to the EML RHS.
- 3.5 — Compare all EML-NODE variants to the MLP-NODE baseline on the dev set.

**End-of-phase deliverable**: `experiments/eml_node_results.md` with reconstruction MSE comparison. Honest assessment of whether EML-NODE is competitive or strictly worse than MLP-NODE on raw fit.

### Phase 4 — Symbolic snap and inspect
*Goal: for trees that snap successfully, write out the closed-form RHS and check it against known LMSR theory.*

- 4.1 — For each market with a snapped EML tree, extract the symbolic expression (Mathematica or `sympy`-side simplification)
- 4.2 — Cluster markets by snapped expression — do many markets converge on the same RHS, or is each one different?
- 4.3 — Compare snapped expressions to LMSR's known closed-form pricing dynamics. If recovery matches a known mechanism, that's a *validation* result. If it discovers something new, that's a *research* result. If nothing snaps cleanly, that's a *negative* result.
- 4.4 — Write up findings as a draft `findings.md` for circulation

**End-of-phase deliverable**: `findings.md` documenting which expressions were recovered, how often, and how they relate to LMSR theory.

### Phase 5 — Falsifiability (held-out test)
*Goal: backtest any recovered formulas on the 20% held-out market set. This is where research turns into a hypothesis check.*

- 5.1 — For each snapped expression from Phase 4, generate forward-simulation predictions on the held-out markets
- 5.2 — Score predictions against actual resolution outcomes; compare to MLP-NODE baseline
- 5.3 — Apply the [[wiki/concepts/prediction-markets|primitives we already know to apply]]: Kelly-sized bets on confident predictions, Bayesian belief updates, behavioral-fingerprint comparisons
- 5.4 — Report: does any snapped formula beat the baseline on out-of-sample data? With what variance?

**End-of-phase deliverable**: `backtest_report.md` with honest pass/fail call. **Gate: do not proceed to Phase 6 unless at least one snapped formula shows statistically significant out-of-sample edge.**

### Phase 6 — Productize (optional, gated on Phase 5)
*Goal: only if Phase 5 produces a real edge, wrap the surviving formula in a small live-trading harness.*

- 6.1 — Live data feed integration; latency check
- 6.2 — Position-sizing per Kelly with fractional safety factor (no full-Kelly in production)
- 6.3 — Risk caps: daily loss limit, max position size, kill switch
- 6.4 — Paper-trade for ≥30 days before any real capital
- 6.5 — Real-capital deployment with a $100 starting bankroll. Scale only on demonstrated stability, not on expected value.

**End-of-phase deliverable**: a tiny, monitored, live trading harness — or a clean shutdown with documented "did not survive paper trading" findings.

---

## Milestones

- [x] **M0**: Subgraph schema introspected and verified (Phase 0.0, completed 2026-05-10)
- [x] **M0.5**: Gamma `/markets` endpoint verified (Phase 0.1, completed 2026-05-10) — base URL, schema match, no auth confirmed
- [x] **M0.6**: `outcomePrices` resolution semantics verified on recent UMA markets (Phase 0.1.5, completed 2026-05-10) — `["0","1"]` / `["1","0"]` reliably encode payouts
- [x] **M0.7**: Project scaffolded into `polymarket-bot` repo as `polybot_research.eml_node`; Phase 0 stages 0.0–0.4 implemented; 22-test smoke suite passing (completed 2026-05-10)
- [x] **M0.8**: First end-to-end Phase 0 pull successful — 50 markets fetched, 8 kept (16% pass rate), 16 assets queried, ~10K fills landed (completed 2026-05-10)
- [x] **M0.9**: `OrderFilledEvent.price` semantics empirically resolved — `sell` rows price = probability, `buy` rows price = 1/probability. Codified in `data/probability.py` with 11 unit tests; verified against known resolution on `Espresso > $200M` market (final YES prob = 0.999, market resolved YES) (completed 2026-05-10)
- [x] **M1.0**: Phase 0.5 bucketing implemented (`data/bucketing.py`) — per-market hourly YES-probability time series with VWAP, mean, first, last, and n_fills aggregations; YES + NO assets joined into single series; forward-fill into empty buckets; output as one Parquet per market under `data/research/eml_node/processed/`. 13-test suite covers single-bucket aggregation, multi-bucket separation, YES/NO joining, forward-fill, edge cases. End-to-end verified on Espresso > $200M: 54 hourly buckets, range [0.38, 0.999], converges to 0.999 at resolution as YES wins (completed 2026-05-10)
- [x] **M1.1**: Phase 0.6 sanity cross-check implemented (`data/sanity.py`). Per-market check that the bucketed final pre-resolution YES probability (last real bucket's `yes_prob_last`) agrees with Gamma's resolution outcome within a configurable threshold (default 0.05). Persisted as `processed/_sanity_report.parquet` with per-market discrepancy, fill count in final bucket, and pass/fail. CLI `eml-sanity` exits non-zero on any failure. 12-test suite covers pass cases (final at 0.999), fail cases (wrong direction), edge cases (empty series, unparseable yes_won, only-synthetic buckets), and threshold configurability. Wired as stage 0.6 in `run_phase_0` (completed 2026-05-10)
- [x] **M1**: 313 resolved CLOB-era markets pulled, cleaned, bucketed; 99.4% pass the Phase 0.6 sanity check (median discrepancy 0.001 = 1 tick); 2 markets show real pre-resolution mispricing (final trade vs eventual resolution off by 0.10–0.22), flagged for Phase 5 backtest review (completed 2026-05-10)
- [ ] **M2**: Baseline Neural ODE trained; reconstruction MSE recorded (Phase 1)
- [ ] **M3**: EML primitive verified against paper's depth-3 `ln(z)` recovery (Phase 2)
- [ ] **M4**: First EML-NODE training run completes without NaN (Phase 3)
- [ ] **M5**: At least one market admits a snapped EML expression (Phase 4)
- [ ] **M6**: Held-out backtest comparison reported, pass-or-fail call made (Phase 5)
- [ ] **M7** (gated): Live paper-trading harness running, ≥30 day track record (Phase 6)

---

## Architecture note (added 2026-06-11)

**Do not use LLM self-evaluation to rank candidate EML expressions or hypothesis variants.** [[wiki/sources/2026-06-11-llms-novel-research-ideas|Si et al. (2024)]] show LLM rankers achieve only ~53% consistency on idea ranking — barely above random. For this project, the correct ranking signal is reconstruction MSE (Phase 3), symbolic snap success rate (Phase 4), and out-of-sample IC / profit (Phase 5). LLM judgment may be used for *interpretation* of snapped expressions in natural language, not for *selection* among competing formulas.

**Related**: [[wiki/sources/2026-06-11-alpha-gpt-alpha-mining|Alpha-GPT]]'s formulaic alpha mining (genetic programming on WorldQuant grammar) is a parallel track to EML-NODE and complements it — if EML-NODE stalls at Phase 3, the Alpha-GPT paradigm (LLM seeds + GP optimization + IC filter) is a proven alternative that doesn't require any model training. Both are bets on formulaic, legible signals.

---

## Open practical questions

- ~~**API access reality**~~: ✅ Resolved 2026-05-10. Subgraph endpoint verified, auth works, indexer is fresh (timestamps within seconds of wall-clock), pre-computed `price` field available on `OrderFilledEvent`. Gamma API still unverified.
- **Sparse / irregular fill data**: Polymarket markets vary wildly in liquidity. Bucketing fills into a uniform-time series will produce sparse or irregular samples for low-liquidity markets. Options: (a) interpolate, (b) use irregular-time ODE solvers (`torchdiffeq` supports this), (c) filter harder in Phase 0.2 to exclude thin markets. Decision deferred until we see the per-market gap distribution in Phase 0.6.
- **ODE framing assumption**: LMSR price dynamics depend on discrete trade flow — does a continuous-time ODE framing make sense, or do we need stochastic/jump processes (SDEs, Hawkes processes)? May need a Phase 0.8 to test this empirically.
- **Bucketing rule for batch-matched fills**: Multiple fills inside the same `transactionHash` are atomic. Use `blockNumber` as primary sort and the position within the tx (which the subgraph doesn't expose directly) as secondary. May need to either treat the entire batch as a single event at the resulting price, or use the volume-weighted price across the batch. Decide based on what looks right empirically in Phase 0.6.
- **Snap behavior on noisy data**: Does the paper's 100%-at-depth-2 snap recovery generalize from clean synthetic data to noisy market data? This is the single biggest unknown. Phase 2 stress-tests should add Gaussian noise to the synthetic targets to check.
- **Depth budget**: Are market dynamics really depth ≤4 elementary, or do they need depth 6+ (where the paper showed 0% blind recovery)? If the latter, this project is dead in the water and needs to wait for advances in EML training.
- **Complex-arithmetic correctness**: PyTorch `complex128` operations have edge cases around branch cuts. Phase 2 verification must catch these or downstream training will silently produce nonsense.
- **Cost of compute**: How much GPU time does a full sweep cost? If trivial, fine. If non-trivial, may need to start with CPU-only on a small market subset.

---

## Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| ~~Polymarket API access is restricted from outside U.S.~~ | ✅ Resolved 2026-05-10 | — | Subgraph access verified |
| ~~Gamma `/markets` endpoint not in partial OpenAPI~~ | ✅ Resolved 2026-05-10 | — | Endpoint verified at `https://gamma-api.polymarket.com/markets`, no auth, returns Market schema |
| ~~`outcomePrices` may not encode resolution~~ | ✅ Resolved 2026-05-10 | — | UMA markets reliably encode payouts as `["0","1"]` or `["1","0"]` in `outcomePrices` |
| AMM-era markets present in Gamma but absent from CLOB subgraph | High (silent data loss if not filtered) | Medium | Filter `fpmmLive == true` (AMM) — note `null` is valid for new CLOB markets, predicate must not be `== false` |
| Gamma silently ignores unknown filter params | Medium | Medium | Use only verified params (`closed`, `limit`, `order`, `ascending`); all other filtering done client-side in auditable pass |
| `volume1yrClob` is null on very recent markets — overly aggressive liquidity filter drops fresh data | Medium | Low | Combine with `volume`, `volume1moClob`, or `enableOrderBook` rather than relying on yearly stat alone |
| Gamma rate limits unknown | Medium | Low | Test in Phase 0.2; Polymarket docs may state limits |
| Schema drift on subgraph version change breaks data pipeline | Low | High | Phase 0.0 introspection + snapshot diff catches drift early; pin subgraph version in queries |
| Bucketing rule for batch-matched fills is wrong | Medium | Medium | Validate empirically in Phase 0.6; cross-check against on-chain trade-by-trade if results look off |
| EML snap recovery fails on noisy data | Medium | High | Phase 2 stress-tests with noise; Phase 3 gates on this |
| Market dynamics are stochastic, not deterministic | High | Medium | ODE framing may need to extend to Neural SDE; flagged early |
| Snapped formulas don't generalize out-of-sample | High | Medium | This is the *finding*; report honestly as negative result |
| Falling into the [[wiki/self/patterns\|engagement-bait attention loop]] mid-project | Medium | High | Hold the line — research falsifiability criterion is the test, not "did the bot make money" |
| Loss of focus to other vault projects | Medium | Medium | Time-box phases; check in against milestones, not vibe |

---

## Success criteria

This project is a **success** if any of the following are true at the end:

1. A snapped EML formula shows statistically significant out-of-sample edge on held-out markets.
2. We produce a clean negative result demonstrating that LMSR price dynamics are not recoverable in the EML depth-≤4 regime — useful contribution to [[wiki/concepts/symbolic-regression]] research.
3. We discover a previously-unidentified bug or pathology in EML training on noisy data, documented and reproducible.

This project is a **failure** if it stalls before Phase 4 with no honest write-up of why.

---

## Verified empirical findings (2026-05-10 first pull)

- **`OrderFilledEvent.price` is `taker_amount_filled / maker_amount_filled` exactly** — confirmed row-by-row on 4 sample assets across ~3000 fills. No discrepancies.
- **The semantic meaning of `price` depends on `side`**:
  - `side == "sell"`: price ∈ (0, 1] — equals the implied probability of the fill's own token directly.
  - `side == "buy"`: price ∈ [1, ∞) — equals 1/probability. Cheap tokens show very large prices on buys.
- **Verification**: derived YES probability from both YES-side and NO-side fills converges to 0.999 at the end of "Espresso FDV above $200M one day after launch?", which resolved YES. Both sides agree, confirming the rule.
- **Side casing**: subgraph returns lowercase (`buy`, `sell`), not uppercase as initially assumed.
- **AMM-era / negRisk filter pass rate**: ~16% on the most-recent 50-market slice. Most drops are negRisk multi-outcome bundles + pre-UMA stale `outcomePrices`.
- **Subgraph 1000-row page limit** is the natural pagination unit; markets with >1000 fills require a second page (10 of our 16 assets needed only 1 page; 4 needed 2). Well under the 5000-skip hard cap, but for very high-volume markets we'll need keyset pagination by `timestamp_gt` (TODO already in code).
- **Sanity-check finding (313 markets, 2026-05-10)**: 99.4% pass rate against Gamma resolution; median discrepancy 0.001 (= one CLOB tick — the closest-to-resolution price possible); max 0.22 on two markets where trading wound down at the wrong price (Infinex public-sale market: final trade 0.78 with 25 fills, but resolved YES; Stable FDV >$2B: final trade 0.10 with 31 fills, but resolved NO). These are *real-world signals* worth keeping in the dataset, not bugs — they're the kind of pre-resolution mispricing Phase 5's falsifiability test cares about. The Phase 0.7 split should not blindly drop them.

## Implementation paths (scaffolded 2026-05-10)

Code lives in the existing `~/projects/polymarket-bot` repo as a sibling package:

```
src/polybot_research/eml_node/
├── README.md             — implementation index, links here
├── cli.py                — entry points (eml-schema-check, eml-phase0, eml-status)
├── data/
│   ├── models.py         — ResolvedMarket, Fill, MarketFillSeries
│   ├── filter.py         — audit-ready client-side Gamma filter (verified semantics)
│   ├── gamma.py          — ResolvedMarketsClient (closed markets, recent-first)
│   ├── subgraph.py       — SubgraphClient (CTF Exchange OrderFilledEvent)
│   ├── schema_check.py   — Phase 0.0 introspection + drift detection
│   └── pipeline.py       — Phase 0.2–0.4 orchestrator (run_phase_0)
├── eml/
│   └── operator.py       — eml() with stability clamps; EMLNode/EMLTree stubs
└── node/                 — Phase 3 stub
```

Outputs land under `data/research/eml_node/` (separate from `data/trades/` so live-bot logs and research artifacts don't collide).

**Reused from `polybot`**: `polybot.utils.retry.async_retry` (in both Gamma and subgraph clients), `polybot.config.Settings` pattern (research adds `GRAPH_API_KEY` to the same `.env`).

**Heavy ML deps gated** behind `[research]` optional extra in `pyproject.toml` — production installs of the live bot stay lean. Install with `uv sync --extra research`.

**Tests**: `tests/polybot_research/eml_node/test_filter.py` — 22 tests, each grounded in a verified Gamma semantic from a Phase 0 spike.

## Cross-links

- [[wiki/insights/eml-as-ml-substrate]] — the synthesis that motivated this project
- [[wiki/concepts/eml-operator]] — primitive
- [[wiki/concepts/symbolic-regression]] — research context
- [[wiki/concepts/prediction-markets]] — domain
- [[wiki/areas/entrepreneurship/_overview]] — trading-bot lane
- [[wiki/areas/ml-research/_overview]] — agent-engineering harness
- [[wiki/self/goals]] — $10K target context
- [[wiki/self/patterns]] — engagement-bait attention-loop guard
- [[wiki/sources/2026-05-09-eml-elementary-functions]] — paper
- [[wiki/sources/2026-05-09-x-bookmarks-150-dump]] — what *not* to be
- [[wiki/sources/2026-05-24-tradingagents-multi-agent-trading]] — the *other* bet on where trading edge lives: LLM-orchestration ([[wiki/concepts/multi-agent-systems|multi-agent]] read-debate-decide) vs this project's symbolic-mechanism (recover the closed-form RHS). Worth holding both as distinct, separately-falsifiable hypotheses; this project deliberately picks the legible-mechanism side.
