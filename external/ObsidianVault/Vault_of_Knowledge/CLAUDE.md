# The Brain — Schema & Operating Instructions

This vault is a persistent personal knowledge base (second brain) maintained collaboratively by the user and an LLM agent. The LLM writes and maintains the wiki; the user curates sources, directs analysis, and asks questions.

---

## Directory Layout

```
Vault of Knowledge/
├── CLAUDE.md          ← this file: conventions, workflows, page formats
├── index.md           ← master catalog of all wiki pages
├── log.md             ← append-only operation log
│
├── raw/               ← immutable source files (never modify)
│   ├── articles/
│   ├── notes/
│   ├── papers/
│   ├── bookmarks/
│   └── voice/
│
├── wiki/              ← LLM-maintained knowledge base
│   ├── self/          ← identity: values, goals, traits, patterns
│   ├── areas/         ← ongoing life domains (no end date)
│   │   ├── ml-research/
│   │   ├── biomedical/
│   │   ├── entrepreneurship/
│   │   └── personal-dev/
│   ├── projects/      ← active projects and ideas
│   ├── concepts/      ← frameworks and mental models
│   ├── people/        ← influential people
│   ├── insights/      ← synthesized observations and patterns
│   ├── sources/       ← one summary page per ingested source
│   └── archive/       ← retired wiki pages, kept for reference
│
├── outputs/           ← generated artifacts (charts, tables, decks)
├── archive/           ← cold storage: old raw sources, dead projects
└── meta/              ← notes about this system itself
```

---

## Page Format

Every wiki page starts with YAML frontmatter. No exceptions.

```yaml
---
type: self | area | project | concept | person | insight | source
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active | stub | archived
---
```

- `type` determines which folder the page lives in.
- `status: stub` = page exists but needs more content. Flag these during lint.
- Use lowercase-hyphenated filenames: `growth-mindset.md`, `transformer-architecture.md`.
- Every page should link to at least one other page. Isolated pages are a smell.
- Cross-links use Obsidian `[[wikilink]]` syntax.

### Self pages
Live in `wiki/self/`. Describe who the user is — not what they did. Updated whenever a source reveals something about identity, values, or behavioral patterns. Core pages: `values.md`, `goals.md`, `patterns.md`, `strengths.md`, `open-questions.md`.

### Area pages
Live in `wiki/areas/<domain>/`. Each area has an `_overview.md` that summarizes the domain, current focus, and key sub-topics. Sub-pages cover specific threads within the area.

### Source pages
Live in `wiki/sources/`. Filename matches the source: `2026-05-04-article-title.md`. Contains: one-paragraph summary, key takeaways (bullet list), notable quotes (max 2, under 15 words each), and links to every wiki page it touched.

### Insight pages
Live in `wiki/insights/`. An insight is a synthesized observation — something the user wouldn't get from reading a single source. Often generated during query or lint, not ingest. Title should be a declarative statement: `attention-mechanisms-mirror-executive-function.md`.

---

## Workflows

### Ingest
Triggered when the user drops a source into `raw/` and says "ingest [filename]".

1. Read the source file.
2. Briefly surface 2-3 key takeaways for discussion (don't write the wiki page yet).
3. After discussion, write a source summary page in `wiki/sources/`.
4. Identify which existing wiki pages this source touches. Update them — revise claims, add connections, note contradictions.
5. If a new entity, concept, or person appears that lacks a page, create a stub.
6. Update `index.md` with the new source page and any new wiki pages.
7. Append an entry to `log.md`.

A single source typically touches 5–15 wiki pages. Err on the side of updating more.

### Query
Triggered when the user asks a question.

1. Read `index.md` to identify relevant pages.
2. Read those pages.
3. Synthesize an answer with inline `[[links]]` to the pages used.
4. If the answer is a valuable synthesis (comparison, pattern, analysis), offer to file it as an insight page.
5. Append a query entry to `log.md`.

### Lint
Triggered when the user says "lint the wiki" (or periodically suggested).

Check for:
- Orphan pages (no inbound links)
- Stubs that could now be fleshed out
- Contradictions between pages
- Claims that newer sources have superseded
- Concepts mentioned on multiple pages but lacking their own page
- Missing area `_overview.md` files
- Data gaps worth filling (suggest specific sources to look for)

Report findings as a checklist. Don't auto-fix — surface issues for user direction.

### Milestone (standing instruction — applies to EVERY repository)

Whenever work on any code repository hits a milestone — a deploy, a passing
end-to-end run, a major feature shipped, a hard bug class eliminated, a phase
boundary — record it in the vault. This is automatic; the user should not have
to ask.

1. Each repository gets one project page at `wiki/projects/<repo-name>.md`
   (type: project). If it doesn't exist yet, create it.
2. Every page carries a `## Milestone Log` section, reverse-chronological.
   Each entry: `### YYYY-MM-DD — <short title>`, then a few lines covering
   **what shipped**, **what it unblocked**, and **what's next**. Be specific
   about the bugs killed and decisions locked — this is the durable record.
3. Append a matching one-line entry to `log.md` (`milestone` operation).
4. Update `index.md` if the project page is new.
5. Keep `updated:` frontmatter and the page's "current phase" line in sync.

A milestone entry is opinionated and concrete, not a changelog dump — capture
why the milestone mattered, not every commit.

---

## Index & Log Conventions

**index.md**: Organized by section (Self, Areas, Projects, Concepts, People, Insights, Sources). Each entry: `- [[page-link]] — one-line description`. Updated on every ingest or new page creation.

**log.md**: Append-only. Each entry starts with `## [YYYY-MM-DD] operation | title` so it's grep-able. Operations: `ingest`, `query`, `lint`, `update`, `create`, `milestone`.

---

## Output Formats

When generating outputs, save to `outputs/` with a datestamped filename.

- **Comparison tables**: markdown tables, also save as `outputs/YYYY-MM-DD-title.md`
- **Charts**: Python/matplotlib script saved to `outputs/`, with a note on how to run it
- **Slide decks**: Marp-formatted markdown saved to `outputs/`
- **Graphs**: describe with mermaid diagrams embedded in wiki pages

---

## Principles

- The user reads; the LLM writes. Never ask the user to write wiki content.
- Maintain voice consistency across pages — third-person for factual pages, first-person for self pages.
- When two sources conflict, note the contradiction explicitly on the relevant page. Don't silently overwrite.
- Prefer updating existing pages over creating new ones. Page sprawl is harder to maintain.
- A good wiki page is opinionated, not encyclopedic. It reflects what matters to this user.

---

## Operational Memory

Hermes/Virgil has an external operational notebook at `meta/hermes-operational-memory.md`. Use it for durable agent-operation context that is too verbose or project-specific for built-in Hermes memory: repo locations, host boundaries, service topology, non-secret runbooks, standing conventions, and cross-project pitfalls.

Do not put secrets, tokens, private keys, passwords, one-time task progress, or raw command dumps there. Prefer project pages for project milestones, Hermes built-in memory for tiny global facts, and Hermes skills for repeatable procedures.

## Decision log

- **2026-07-11** — **Hermes operational memory created.** `meta/hermes-operational-memory.md` is now the audit-friendly, Obsidian-side operational notebook for Hermes/Virgil. It complements built-in Hermes memory and project pages; it does not replace the wiki's milestone workflow or the rule against storing secrets.

- **2026-06-07** — **Vault is now read+written by the merged Delphi/Odysseus
  stack.** Until today, the standalone Delphi service on the Proxmox VM
  was the sole writer to this vault. As of today, the Delphi brain lives
  inside the Odysseus codebase at `odysseus/src/delphi/` and is the
  primary writer; the VM stays as a Tailscale-reachable failover. Six
  subdirs (`wiki/`, `knowledge/`, `raw/`, `daily/`, `conversations/`,
  `entities/`) are auto-registered with the Odysseus RAG index on every
  boot so the rest of the workspace (chat, agent, deep research) can
  search them. `outputs/`, `archive/`, `.obsidian/`, and `meta/` stay
  outside the index. The conversation note format and `entities/`
  auto-creation rules are unchanged — same Delphi memory code, new host.
  Plan: `/Volumes/samsungT7/projects/Delphi/docs/plans/2026-06-07-delphi-becomes-the-architecture.md`.
