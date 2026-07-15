# Odysseus — CLAUDE.md (chassis-hosting-Delphi edition)

> **Identity reframe (2026-06-07).** This repo is no longer just Odysseus.
> It's the **chassis hosting Delphi.** Odysseus's UI, routes, agent loop,
> Cookbook, Documents, Deep Research, Compare, Memory/Skills, RAG, Email,
> Notes, Tasks, and Calendar remain in place. Delphi's brain — classifier,
> roster, soul, vault writer, vault_query / gre_quiz / gre_practice_test
> agents — was ported in under `src/delphi/` and is hooked into the chat
> pipeline through a single shim at `src/delphi_pipeline.py`.
>
> The user-visible app is **Delphi.** Odysseus stays as the upstream
> attribution and the package paths.

---

## What lives where

| Layer | Path | Purpose |
|---|---|---|
| Web framework / routes / UI | `app.py`, `routes/`, `static/` | Unchanged Odysseus chassis |
| Sessions / DB / auth | `core/`, `data/app.db` | Unchanged Odysseus |
| Generic LLM transport | `src/llm_core.py`, `src/agent_loop.py` | Unchanged Odysseus |
| **Delphi brain (ported 2026-06-07)** | `src/delphi/` | Classifier + roster + soul + memory + telemetry + bounded agents |
| **Pipeline shim** | `src/delphi_pipeline.py` | The only seam between Odysseus call sites and Delphi |
| Vault RAG bootstrap | `src/app_initializer.py:register_delphi_vault_with_rag` | Auto-indexes 6 vault subdirs on boot |
| Delphi introspection routes | `routes/delphi_routes.py` | `/api/delphi/health`, `/api/delphi/roster` |

---

## Decision log

- **2026-06-07** — **Delphi merges into Odysseus chassis.** This repo gains
  the entire Delphi brain (24 modules) under `src/delphi/` plus the
  `src/delphi_pipeline.py` shim. The standalone Delphi service on the
  Proxmox VM is preserved as a Tailscale-reachable failover; the merged
  in-process Delphi here is the primary. UI is rebranded Delphi.
  Vault auto-indexing wired into RAG. Chat path (`routes/chat_routes.py`)
  patched: every chat now runs through Delphi's resolver, injects the
  soul, and persists the exchange to `Vault of Knowledge/conversations/`
  via fire-and-forget `asyncio.create_task`. Plan:
  `/Volumes/samsungT7/projects/Delphi/docs/plans/2026-06-07-delphi-becomes-the-architecture.md`.

## Kill switch

Set `DELPHI_PIPELINE_DISABLED=1` in the env to take the Delphi pipeline
out of the chat path entirely. The chat flow falls back to plain Odysseus
behavior — no soul injection, no vault persist, no resolver. Useful when
debugging a Delphi-side regression.

## Environment

Delphi's brain reads its own config from the same `.env` Odysseus uses.
The required vars (read by `src/delphi/config.py`):

| Var | Default | Notes |
|---|---|---|
| `DELPHI_BEARER_TOKEN` | — | Required even though chat enters via Odysseus auth; future external Delphi callers (AgentRig over Tailscale) still need it |
| `OBSIDIAN_VAULT_PATH` | — | Path to the Obsidian vault. RAG auto-index reads this. |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Or `https://ollama.com` for Cloud |
| `LOG_DIR` | — | Where Delphi's JSONL request log lands |
| `DELPHI_MODEL_*` | per-task defaults | Roster — see `src/delphi/config.py` for the full list |

---

## Mentorship note

Two CLAUDE.mds matter for this project: this one (chassis perspective)
and `/Volumes/samsungT7/projects/Delphi/CLAUDE.md` (brain / soul
perspective). They share the 2026-06-07 decision-log entry but otherwise
each focuses on its own concerns. When you change pipeline behavior,
update both.
