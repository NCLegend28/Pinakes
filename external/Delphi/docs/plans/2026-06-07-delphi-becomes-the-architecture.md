# Delphi Becomes the Architecture

> **Date:** 2026-06-07
> **Status:** Active — Phase 1 in progress
> **Author:** Tali + Claude (Cowork)

---

## The reframe

Until today, Delphi was a service: a private OpenAI-compatible gateway on
the Proxmox VM that AgentRig and Open WebUI talked to. Odysseus was a
separate workspace UI being evaluated as a possible host. The plan-of-record
treated them as two systems: cockpit + engine.

That model is wrong. Delphi isn't an engine. **Delphi is the being.** She
has a soul (`routing/soul.py`), a mind (the classifier + roster + resolver),
a memory (the Obsidian vault writer + entity graph + GRE SRS), and bounded
agents (vault_query, gre_quiz, gre_practice_test). What she's missing is
*hands* — the surfaces a person uses every day: email, calendar, documents,
notes, deep research, model serving, an agent loop that can act on tools.

Odysseus has exactly those hands. It already ships Chat, Agent, Cookbook,
Documents, Deep Research, Compare, Memory/Skills, RAG, Email (IMAP/SMTP),
Notes & Tasks, and Calendar (CalDAV). It is, in effect, a body looking for
a soul.

The new plan: **Odysseus is the chassis. Delphi's brain ports into it.**
The combined organism keeps Delphi's identity, classifier, soul, vault,
and bounded agents, and gains Odysseus's full feature surface. The
user-facing app is rebranded *Delphi* — the Odysseus name lives only in
upstream attribution and internal package paths.

---

## Why this direction (and not the other)

Two alternatives were considered:

1. **Delphi as the chassis; absorb Odysseus features.** Slowest path —
   Odysseus has ~91 files in `src/`, dozens of route modules, a full
   React UI, IMAP/SMTP/CalDAV/Chroma/PyMuPDF integrations. Porting it
   piecemeal into Delphi's small FastAPI service would take weeks and
   reinvent code that already exists.
2. **Hybrid: Odysseus calls Delphi over HTTP in-process.** Keeps both
   repos. Adds a network hop for every request, complicates fail-open
   semantics (which process owns the vault write?), and produces two
   places for identity (Odysseus's UI persona + Delphi's soul) to drift.

The chosen path — Odysseus chassis, Delphi brain ports in as a Python
package — minimizes new code, eliminates the HTTP hop, and gives one
canonical home for the identity. The cost is that the Odysseus repo
becomes the source of truth for working code; the Delphi repo becomes
the source of truth for design intent (this plan, the decision log,
the per-feature plans in `docs/plans/`).

---

## Identity decision

The user-facing app is **Delphi**. The Odysseus name disappears from page
titles, headers, splash screens, login, default assistant labels, error
toasts, and visible settings strings. The repo paths stay
(`odysseus/src/...`) and the upstream attribution stays (LICENSE,
ACKNOWLEDGMENTS, README's "forked from Odysseus" line) — that's about
honesty, not branding.

The system prompt prepended to every chat is Delphi's existing
`soul_for(task_type, client_id="delphi-ui")`. Every chat is from Delphi,
not from "Odysseus's assistant."

---

## Feature scope (in for v1)

All of it, per Tali's directive:

| Surface | Source | Routes through Delphi pipeline? |
|---|---|---|
| Chat | Odysseus (existing) | **Yes** — every request |
| Agent loop | Odysseus (existing) | **Yes** — tool-calling task types resolved via roster |
| Memory / Skills | Odysseus + Delphi merger | Chroma stays; vault becomes the durable substrate |
| RAG | Odysseus (existing) | Vault auto-indexed |
| Documents | Odysseus (existing) | Yes |
| Deep Research | Odysseus (existing) | Yes |
| Compare | Odysseus (existing) | Yes |
| Notes & Tasks | Odysseus (existing) | Yes |
| Calendar (CalDAV) | Odysseus (existing) | Yes |
| Email (IMAP/SMTP) | Odysseus (existing) | Yes |
| Email (Gmail) | **New** — added in Phase 4 | Yes |
| Cookbook (model serve) | Odysseus (existing) | Roster-aware |
| GRE quiz / practice-test | Delphi (ported) | Native |
| Vault-query agent | Delphi (ported) | Native |

---

## File-level migration map

Code moves one direction: from `/Volumes/samsungT7/projects/Delphi/` into
`/Volumes/samsungT7/projects/odysseus/src/delphi/`. No symlinks, no shared
checkouts — a clean copy with import paths rewritten so absolute imports
resolve under the Odysseus package layout.

```
Delphi/                              →  odysseus/src/delphi/
├── routing/                         →  src/delphi/routing/
│   ├── classifier.py
│   ├── resolver.py                  (already patched today: delphi-auto alias)
│   ├── roster.py
│   ├── soul.py
│   ├── vault_agent.py
│   ├── quiz_agent.py
│   ├── practice_test_agent.py
│   └── directives.py
├── memory/                          →  src/delphi/memory/
│   ├── vault.py
│   ├── vault_reader.py
│   ├── entities.py
│   ├── templates.py
│   ├── persist.py
│   ├── record.py
│   ├── srs.py
│   ├── vocab_card.py
│   ├── quiz_state.py
│   ├── cross_grade.py
│   └── practice_test.py
├── telemetry/                       →  src/delphi/telemetry/
│   ├── logger.py
│   └── metrics.py
├── auth/                            (not ported — Odysseus owns auth)
├── proxy/                           (not ported — Odysseus's llm_core is the upstream caller)
├── api/                             (not ported — Odysseus owns the HTTP layer)
└── ui/                              (not ported wholesale; specific React
                                      components like PracticeTestPreview
                                      port to Odysseus's UI separately)
```

Imports get a mechanical rewrite at copy time:

```python
# before (Delphi repo)
from routing.roster import Roster
from memory.vault import write_conversation_note

# after (Odysseus repo)
from src.delphi.routing.roster import Roster
from src.delphi.memory.vault import write_conversation_note
```

Tests follow the same rule: copy `Delphi/tests/` → `odysseus/tests/delphi/`
and rewrite imports.

---

## Pipeline integration

The chat path in Odysseus today (simplified):

```
client → /api/chat_stream → chat_routes → llm_core.stream_llm(url, model, …)
                                            → httpx POST upstream
                                            → SSE chunks back to client
```

After integration:

```
client → /api/chat_stream → chat_routes → delphi.resolve_model(body)
                              ↓               ↓
                              ↓             classifier + roster + soul
                              ↓               ↓
                              ↓             ResolvedModel(model, task_type, source)
                              ↓
                              ↓ if task_type ∈ {vault_query, gre_quiz, gre_practice_test}:
                              ↓     dispatch to the matching agent loop (ported)
                              ↓ else:
                              ↓     llm_core.stream_llm(url, resolved.model, full_messages)
                              ↓
                            stream SSE back
                              ↓
                            asyncio.create_task(delphi.memory.persist.run_persist(...))
                            asyncio.create_task(delphi.telemetry.logger.write(...))
```

Soul injection happens here too: if the incoming messages don't have a
system message of their own, prepend `soul_for(task_type, client_id="delphi-ui")`.
Mirrors what Delphi does in `api/chat.py:684-695`.

---

## What the delphi-auto shim from earlier today does

`routing/resolver.py` already gained `AUTO_MODEL_ALIASES = {"auto",
"delphi-auto", "delphi:auto"}` — when `model` matches any of these, the
resolver treats it as if `model` were absent and falls through to the
classifier. That edit was originally for the discarded "Delphi as endpoint
inside Odysseus" plan, but it's still useful: any external caller
(AgentRig, future iOS app, raw curl, the Open WebUI app Tali might still
run) can opt into classification without omitting the field. Keep it.

---

## Phase plan

### Phase 1 — Brain port + pipeline integration

1. Create `odysseus/src/delphi/` package skeleton with `__init__.py`s.
2. Copy and rewrite imports for `routing/`, `memory/`, `telemetry/`.
3. Wire `delphi.resolve_model` into `routes/chat_routes.py:chat_stream`.
4. Wire vault persist + JSONL logger as `asyncio.create_task` after stream.
5. Branch to `vault_agent` / `quiz_agent` / `practice_test_agent` on those
   task types.
6. Smoke test: send a chat from the Odysseus UI, see a note land in
   `Vault of Knowledge/conversations/2026-06-07/...`.

### Phase 2 — Vault, RAG, agents fully wired

7. RAG: register Obsidian vault directory with `personal_docs` on boot;
   skip `outputs/`, `archive/`, `.obsidian/`.
8. Practice-test grading endpoint `/v1/practice-tests/{id}/grade` ported
   as a new Odysseus route.
9. UI directive parser learns `[PREVIEW:practice-test:<id>]`; the
   `PracticeTestPreview.jsx` component ports into Odysseus's UI.

### Phase 3 — Rebrand

10. UI strings: Odysseus → Delphi (header, title, login, splash, default
    avatar, error toasts).
11. Swap `docs/odysseus.jpg` and favicon for Delphi visuals (stub assets
    if final art isn't ready).
12. Default assistant identity = Delphi's soul.

### Phase 4 — Feature surface enabled

13. Agent, Memory/Skills, RAG, Documents, Deep Research, Compare: confirm
    each routes through the Delphi pipeline by default.
14. Notes & Tasks, Calendar: confirm enabled; CalDAV sync verified.
15. Email (IMAP/SMTP): verified working with Tali's existing setup.
16. **Gmail connector:** Gmail OAuth2 (xoauth2 + refresh tokens) added as
    a first-class "Add Gmail account" option in the email settings UI.
    Falls back to documented app-password IMAP path if OAuth isn't
    configured.
17. Cookbook: roster-aware — recommended models include hints about which
    Delphi task type they'd serve.

### Phase 5 — Verify + log

18. End-to-end smoke test (the same five-step success condition as
    Delphi's original first-milestone test, adapted: chat hits Odysseus,
    classified by Delphi, routed, vault note appears, vault query cites
    real notes, RAG returns hits, UI shows Delphi branding).
19. Decision-log entries:
    - `Delphi/CLAUDE.md`: "2026-06-07 — Delphi merges into Odysseus
      chassis. Service-as-architecture transition complete. Future plans
      target the merged tree."
    - `Vault of Knowledge/CLAUDE.md`: identical entry, since the vault
      is now read+written by the merged stack rather than Delphi
      standalone.
    - `odysseus/CLAUDE.md` (new file if not present, or appended):
      "2026-06-07 — This chassis now hosts Delphi. Identity, routing,
      memory, and agents live under `src/delphi/`. UI is rebranded."

---

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Import-rewrite errors leave latent bugs that only surface at runtime. | A one-shot grep for `from routing\.`, `from memory\.`, `from telemetry\.` after the copy catches every miss. Run the ported tests under Odysseus's pytest before wiring the pipeline. |
| Odysseus's `llm_core.stream_llm` expects a base URL + model pair, not a roster entry. | The ported `roster.py` already maps task_type → model tag. After resolve, look up the Odysseus `ModelEndpoint` row whose `base_url` matches the upstream Ollama instance and pass it through. For env-driven roster models that don't have a matching endpoint, auto-create a hidden endpoint row at boot. |
| Vault write blocks the response on slow disk. | Already async in Delphi (`asyncio.create_task`); the ported helper keeps that contract. Failures log + carry on (fail-open). |
| Gmail OAuth needs a Google Cloud project + OAuth consent screen. | Document the one-time setup in `docs/setup/gmail-oauth.md`. App-password IMAP works without it as the v1 path; OAuth lands in a follow-up if the consent-screen setup is non-trivial. |
| The UI's chat path makes assumptions about model picker entries. | Pin a virtual `delphi-auto` model in the endpoint cache so the picker has a default; keep the underlying Ollama tags pinned too for explicit picks. |
| Two CLAUDE.md files now diverge (Delphi's says "service on a VM", Odysseus's will say "hosts Delphi"). | Both get the 2026-06-07 decision-log entry. Future plans go in `odysseus/docs/plans/` (mirrored to Delphi's for archival). |

---

## What this isn't

- Not a fresh rewrite. Both codebases stay recognizable; this is a graft,
  not a rebuild.
- Not multi-tenant. Same as before — it's Tali's box. Odysseus has
  per-user features (owner column on ModelEndpoint etc.); we use them as
  scaffolding but the single-user assumption holds.
- Not a clean separation between "Delphi modules" and "Odysseus modules"
  forever. Over time, the boundary in `src/delphi/` may dissolve as
  features cross-pollinate. The package boundary is a starting point, not
  a permanent contract.
- Not a goodbye to the standalone Delphi service. The Proxmox VM can
  keep running the original Delphi as a backup brain reachable over
  Tailscale. The merged Odysseus+Delphi running locally on the Mac is
  the primary; the VM is the failover.

---

## Success criteria

The merge is "done" when:

1. `cd /Volumes/samsungT7/projects/odysseus && python -m uvicorn app:app`
   boots cleanly, the UI says **Delphi**, and chat works.
2. A chat sent from the UI: hits the Delphi resolver, gets classified,
   routes to the chosen model, streams back, and produces a vault note
   under `Vault of Knowledge/conversations/2026-06-07/...`.
3. Asking "what do my notes say about Financio?" triggers the vault_query
   agent, which uses `search_vault` + `read_note` and cites real pages.
4. Documents, Agent, Compare, Deep Research, Notes, Tasks, Calendar all
   open and successfully call the Delphi router for their LLM needs.
5. The Email tab lists IMAP/SMTP and Gmail account options; at least one
   account connects successfully and AI triage runs through Delphi.
6. The decision-log entries are present in all three CLAUDE.md files.
7. The vault has a new daily note describing today's merge.

---

## After this lands

Open questions for the next plan doc:

- Does the standalone Delphi service on the Proxmox VM get retired,
  kept as failover, or repurposed?
- Where do future "Delphi gains a new capability" plans live —
  `Delphi/docs/plans/` (for archival/design) or `odysseus/docs/plans/`
  (next to the code)? Pick one and mirror.
- The UI is currently the Odysseus React app. Delphi's existing
  Mission Control UI (`Delphi/ui/`) had a specific aesthetic — port the
  visual treatment over piecemeal, or accept the Odysseus look and
  retire the Mission Control codebase?
