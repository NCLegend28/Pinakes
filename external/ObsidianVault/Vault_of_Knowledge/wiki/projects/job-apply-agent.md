---
type: project
tags: [job-search, automation, local-first, ai-agents]
created: 2026-07-11
updated: 2026-07-11
status: active
---

# Job Apply Agent

Local-first job-application assistant at `/Users/mosley/job-apply-agent`.

## Current phase

MVP scaffold: truthful resume tailoring, SQLite tracker, CSV export, and hiring-team email drafts.

## Purpose

Help Tali apply to jobs with less repetitive admin while keeping the process honest and auditable. The assistant ingests a resume/professional doc plus a job description, creates a tailored resume draft constrained to claims already present in the source docs, tracks the application lifecycle, and drafts an email to the hiring team.

Related: [[wiki/self/goals]], [[wiki/concepts/agentic-coding]], [[wiki/insights/out-tool-bugs-dont-out-know-them]].

## Architecture

- Python standard-library app; no external dependencies for the MVP.
- Web UI served by `wsgiref.simple_server` at `http://127.0.0.1:8765`.
- SQLite tracker at `data/jobs.db` by default.
- Core modules:
  - `jobapply/tailor.py` — skill extraction, match score, truthful resume draft.
  - `jobapply/tracker.py` — jobs table, status history, CSV export.
  - `jobapply/emailer.py` — hiring-team email draft/mailto link.
  - `jobapply/app.py` — local web UI.

## Product constraints

- Human-in-the-loop by design.
- Does not blindly submit applications.
- Does not bypass CAPTCHAs, evade job-board controls, or invent qualifications.
- Missing keywords are reported separately rather than inserted into the resume.

## Milestone Log

### 2026-07-11 — Local-first MVP built and smoke-tested

**What shipped:** Created `/Users/mosley/job-apply-agent` with a working local web app. It accepts resume/professional-doc text and job descriptions, creates a truthful tailored resume draft, stores applications in SQLite, tracks lifecycle statuses, exports CSV, and drafts a hiring-team email. Added six unit tests covering tailoring, status history, CSV export, and email drafting.

**What it unblocked:** Tali can start using a single local dashboard for job applications without waiting on Google OAuth, SMTP credentials, or browser automation. The CSV export gives an immediate bridge to Google Sheets.

**What's next:** Add Google Sheets sync after Workspace auth is configured, Gmail send-after-approval, duplicate detection, follow-up reminders, job-board capture helpers, and inbox parsing for response/interview/rejection status updates.
