# 90-day Roadmap — guapo_evals

**Core thesis:** the fastest-growing AI engineering hiring category in 2026
is "evals + observability for agents." The market is paying $150–$200/hour
for contractors with this skillset. No dominant SMB-friendly tool exists.
Ship fast, charge cheap, convert via open source.

**North Star metric:** paying customers at day 90.
**Leading indicator:** active traces/day from external users.

---

## Weeks 1–2 — Dogfood
**Goal:** the SDK + control plane ingest works end-to-end on your own workload.

- [ ] `docker compose up` works cleanly from a fresh clone
- [ ] `POST /v1/auth/tenants` returns an api key; whoami confirms it
- [ ] Instrument the **tweet-analysis pipeline** with `@traced` — every stage shows up in the dashboard
- [ ] Instrument the **AI Receptionist** call loop — calls land as traces
- [ ] Instrument **Financio signal generation** — every signal is a trace with strategy tags
- [ ] Measure: SDK overhead ≤ 2ms p95 per decorated function (bench with / without init)
- [ ] Kill switch: setting `GUAPO_EVALS_API_KEY=""` disables everything silently

**Exit criteria:** you personally use the dashboard at least once a day to
debug your own agents. If you don't, nobody else will.

---

## Weeks 3–5 — Evals that actually catch regressions
**Goal:** prove that the eval runner catches a real regression on a real agent.

- [ ] Create a golden set of 20 tweet-pipeline cases (input + llm_judge rubric)
- [ ] Deliberately break the summarizer prompt — eval run goes red
- [ ] Add Slack webhook alerts on eval run failure
- [ ] Add pass-rate trendline to the dashboard
- [ ] Ship CI integration example: GitHub Actions workflow that POSTs to `/v1/eval-runs`

**Exit criteria:** a 3-minute screencast showing: (a) agent works, (b) bad
prompt change, (c) CI fails with a red eval, (d) dashboard shows the
failing cases with reasoning. This is the sales demo.

---

## Weeks 6–8 — First external user
**Goal:** one person who is not you runs traces through the system for 2 weeks.

- [ ] Write the landing page (bliqbyte.com/guapo or dedicated domain)
  - Headline: "Catch AI agent regressions before prod"
  - 90-second Loom demo embedded
  - "Install → decorate → done" code snippet as the hero
- [ ] Find 20 candidate pilots using the job-posting signal method (see `docs/FINDING_CUSTOMERS.md`)
- [ ] Cold-email 5/day referencing their specific job post
- [ ] Offer: free through end of year, 30-minute onboarding call, feedback in exchange
- [ ] Close 1 pilot

**Exit criteria:** someone you've never met has `guapo_evals.init()` in
their production code and opens the dashboard at least twice a week.

---

## Weeks 9–12 — Public launch + second user
**Goal:** first paid conversion, Hacker News launch post.

- [ ] Pricing page: Free (10k traces/mo) · Pro ($49 — 1M traces) · Team ($299 — SSO + unlimited)
- [ ] Stripe integration (just Pro tier — Team is invoice-based for now)
- [ ] Self-hostable Docker image on Docker Hub with one-line install
- [ ] Launch posts:
  - Hacker News: "Show HN: guapo_evals — open-source evals + tracing for AI agents"
  - r/LocalLLaMA: focus on local-model compatibility
  - r/MachineLearning: focus on the eval methodology
  - LinkedIn: sell the Forward-Deployed narrative (ties into BliqByte consulting)
- [ ] Publish the Financio + AI Receptionist case studies — real numbers, real regressions caught

**Exit criteria:** $49 × ≥1 from someone you don't know. The first paying
stranger is the proof the business is real.

---

## Things explicitly NOT in the first 90 days

Keeping scope vicious. These are deferred:

- TypeScript SDK (offered by hand to anyone who asks; don't build until 3+ ask)
- OpenTelemetry export
- LangChain / LlamaIndex first-class support (they have their own tracers — interop via OTel later)
- Prompt management / prompt versioning (separate product)
- A/B testing / experiment tracking
- Multimodal traces (audio, image) — text only for v1
- Team/org roles, SSO — single api key per tenant is fine until someone pays for Team
- On-call / PagerDuty integrations

---

## Services leverage

Every pilot conversation is an FDE (Forward-Deployed Engineer) opportunity.
If a prospect says "we'd use this but we don't even have golden sets yet,"
that's a $200/hr consulting engagement — 2 weeks of work to build their
eval harness on top of guapo_evals. This is the BliqByte flywheel:
product generates leads, services pay the bills, services validate the
product roadmap. Don't discount this path.

---

## Risks + kill criteria

- **Risk:** LangSmith/Braintrust/Langfuse ship a free tier that obsoletes you.
  - Hedge: self-hostable + open-source core. Compete on "no vendor lock-in" and price.
- **Risk:** Nobody cares about evals yet — it's a future problem.
  - The hiring data says otherwise, but if week 8 produces zero pilot interest, pivot the positioning (not the product) — reframe as "LLM cost observability" and lead with the $/trace dashboard.
- **Kill criteria:** if day 90 has zero external traces and zero paid interest,
  archive the repo and move compute to option #2 (inference cost optimizer).
  Don't sink another 90 days.
