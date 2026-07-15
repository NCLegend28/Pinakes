# Review-Guided Auto Fixer PRD

## Overview
Build a security-first automation agent that continuously ingests software marketplace reviews, extracts actionable bugs or feature gaps, plans remediations, and opens developer-ready patches. The bot must never push code live; instead it produces reproducible diffs and review notes for human approval.

## Goals
- Aggregate reviews from Apple App Store, Google Play, GitHub issues, and custom CSV exports.
- Prioritize security-related complaints and repeat regressions.
- Map each issue to affected code areas using heuristic ownership metadata and repository context graphs.
- Generate proposed fixes by editing local files via a policy-constrained editor, producing patches + test suggestions.
- Emit artifacts: issue summary, remediation plan, code diff, validation checklist.

## Non-Goals
- Automatic production deployments.
- Replacing human review or merging without approval.
- Mutating shared_data assets unless explicitly whitelisted.

## Personas & Needs
- **App Maintainers:** want triaged complaints with ready-to-review fixes, clear test plans.
- **Security Engineers:** require audit logs, sandboxed editing, and guardrails against unsafe code generation.
- **Product Analysts:** need aggregated sentiment trends and recurrence tracking.

## Functional Requirements
1. Connectors poll configured marketplaces and normalize reviews into a shared schema.
2. Analyzer classifies severity (bug/perf/security/ux) using rules + embeddings (pluggable).
3. Planner pairs issues with remediations by correlating stack traces, component tags, and historical git blame.
4. Editor subsystem applies fixes via structured operations (insert/replace) and stages diffs for review.
5. Reporter assembles Markdown bundle (issue synopsis, fix notes, security checklist, tests needed).
6. CLI entrypoint `python -m autoFix.scripts.run_bot --config <path>` orchestrates the pipeline.
7. Dry-run mode validates review ingestion + planning without editing code.

## Security & Compliance
- Run connectors and editors inside least-privilege sandboxes; only allow whitelisted paths.
- Enforce policy that secrets/configs are never echoed; redact sensitive inputs before logging.
- Every change requires reviewer sign-off; include signed metadata (timestamp, author, review IDs).
- Maintain allow-list of files directories permitted for automated edits.
- Provide tamper-evident logs persisted to `logs/autoFix_audit.log`.

## Metrics
- Mean time from review ingestion to patch (target < 30 min for high sev).
- % of patches that merge with zero requested changes.
- False positive rate for review classification (<10%).
- Number of prevented security incidents traced to proactive fixes.

## Milestones
1. **MVP (week 1):** connectors + analyzer + dry-run planner outputs Markdown report.
2. **Alpha (week 2):** deterministic editor applying fixes behind feature flag, git patch export.
3. **Beta (week 3):** add security heuristics, reviewer notification hooks, regression tests.

## Open Questions
- Preferred ML stack for embeddings (local vs API)?
- Should planners access proprietary telemetry beyond reviews?
- Integration surface for existing CI (Jenkins vs GitHub Actions)?
