---
type: meta
tags: [hermes, operational-memory, agent-ops]
created: 2026-07-11
updated: 2026-07-11
status: active
---

# Hermes Operational Memory

This is Hermes/Virgil's external operational notebook for durable, human-readable context that is too project-specific or too verbose for Hermes' built-in memory. It lives inside the Obsidian knowledge vault so Tali can audit, edit, and link it, but it should stay operational rather than biographical.

## Location

- Vault: `/Volumes/samsungT7/projects/ObsidianVault/Vault of Knowledge`
- This note: `meta/hermes-operational-memory.md`
- Related vault instructions: `CLAUDE.md`
- Append-only vault log: `log.md`

## What belongs here

Use this note for stable operational context that will help future agent sessions act correctly:

- Repo locations, service names, deployment topology, and host boundaries.
- Standing conventions that apply across sessions.
- Non-secret runbooks and known pitfalls.
- Cross-project dependency notes.
- Links to project pages, plans, and outputs in the vault.

Do **not** store secrets, tokens, private keys, passwords, one-time task progress, temporary TODOs, or raw command output dumps here. Short-lived task state should remain in the active chat/session; completed milestones should go on the relevant project page.

## Update protocol

When Hermes learns a durable operational fact:

1. Prefer updating the specific project page first, e.g. `wiki/projects/<project>.md`.
2. Put cross-cutting agent-operation facts here.
3. Add a short entry to `log.md` for meaningful changes.
4. If the fact is tiny and globally useful for every Hermes session, also save it in Hermes built-in memory.
5. If it is a repeatable procedure, make or patch a Hermes skill instead of bloating this note.

## Current operational anchors

### Vault

- The Obsidian vault is at `/Volumes/samsungT7/projects/ObsidianVault/Vault of Knowledge`.
- `OBSIDIAN_VAULT_PATH` is exported in `/Users/mosley/.hermes/.env` and points to this vault for future Hermes sessions/tools.
- `CLAUDE.md` defines the vault schema and standing wiki workflows.
- `meta/` is the right place for notes about the knowledge system itself; it is intentionally separate from user self-pages and project pages.

### Delphi

- Local repo: `/Volumes/samsungT7/projects/Delphi`.
- Current project focus: voice and vision capabilities.
- Delphi STT uses local Whisper/faster-whisper with a provider abstraction so OpenAI `whisper-1` remains swappable by config.
- Delphi VPS is separate from Financio: Ubuntu 22.04 at `46.225.83.22`; Docker/Caddy app bound to `127.0.0.1:80`, exposed tailnet-only by Tailscale Serve at `https://delphi-1.tail6d29ca.ts.net`.
- Vault/OM on the Delphi VPS: host `/root/Vault` mounted as `/vault`, metadata in `/root/Vault/.delphi`.

### Financio / Polymarket

- Polymarket bot repo: `/Volumes/samsungT7/projects/polymarket-bot`.
- ExFAT pitfalls: use `UV_LINK_MODE=copy` and `UV_PROJECT_ENVIRONMENT=$HOME/.cache/polymarket-bot-venv` for `uv sync`; AppleDouble `._*` files can break wheel installs.
- Docker builds for this repo may need `DOCKER_BUILDKIT=0` because the legacy builder path avoids prior ARG expansion problems in `--from`.
- Bot entry point: `python -m polybot.cli`.
- Position sizing is recorded at open time; already-open positions do not resize after fixes, so restarts affect only new opens.
- Config uses `pydantic-settings`; process environment silently overrides `.env`.

### ExpenseTracker

- Tali's ExpenseTracker iOS app repo: `/Volumes/samsungT7/projects/expenseTracker`.
- SwiftUI + SwiftData, iOS 17+, bundle ID `aferro.ExpenseTracker`, development team `32MK8DGN3X`.
- Xcode 16+ PBX file-system-synchronized root group means new files under `ExpenseTracker/ExpenseTracker/` auto-include; do not hand-edit the pbxproj just to add files.

### Job Apply Agent

- Local repo: `/Users/mosley/job-apply-agent`.
- Purpose: local-first job application assistant for truthful resume tailoring, SQLite lifecycle tracking, CSV export, and hiring-team email drafts.
- Run locally with `cd /Users/mosley/job-apply-agent && python3 run.py`; default URL `http://127.0.0.1:8765`.
- MVP intentionally keeps application submission human-in-the-loop; it does not bypass job-board controls or invent qualifications.

### Server/admin identity

- In sysadmin/server contexts, Hermes should operate as Virgil, Tali's system administrator.
- Address the user as Don Guapo in that context.
- Be explicit about which commands run locally vs. on a VPS/server.
- Never edit secrets directly; tell Don Guapo exactly what to change.

## Open operational gaps

- Confirm backup posture for the Delphi VPS vault and Docker deployment.
- Consider splitting each project anchor above into a small `meta/ops/<project>.md` runbook if this page grows too large.
