---
name: ingest
description: >
  Ingest source files from the raw/ directory into The Brain wiki. Use this skill
  whenever the user says "ingest", "/ingest", "process this file", "add this to
  the wiki", "I dropped a file in raw/", or anything that implies a source file
  should be read and integrated into the knowledge base. Also trigger this skill
  proactively if the user mentions reading an article, paper, or note and seems
  to want it filed. Handles discovery, deduplication (including renamed files),
  selective ingestion, wiki updates, and log/index maintenance.
---

# Ingest Skill

You are acting as the wiki maintainer for a personal second-brain vault. Your job is to read source files, discuss them briefly with the user, and then integrate the knowledge into the persistent wiki — updating existing pages, creating stubs for new entities, and keeping the index and log current.

The vault lives at the root of the current project. Refer to CLAUDE.md for the full schema if you need it.

---

## Step 1 — Discover

Scan `raw/` recursively. The expected subdirectories are `articles/`, `notes/`, `papers/`, `bookmarks/`, and `voice/`, but not all of them need to exist — just scan whatever is there. Collect every file's full relative path (e.g. `raw/articles/foo.md`), size, and the first 200 characters of its content (the fingerprint). Skip hidden files and system files (`.DS_Store`, `*.tmp`, etc.). Create `wiki/sources/` if it doesn't exist yet.

---

## Step 2 — Deduplicate

Before presenting anything to the user, filter out files that have already been ingested. Two checks:

**Check A — Filename match:**
Parse `log.md` for lines matching the pattern `## [YYYY-MM-DD] ingest | <filename>`. Extract the `<filename>` portion. Match against each raw file's **basename** (e.g. `foo.md`, not the full path). Note: if two files in different subdirectories share the same basename, both will be skipped — that's the conservative, safe behavior. The fingerprint check below will catch genuine new files that happen to share a name.

**Check B — Fingerprint match (rename detection):**
Read all source pages in `wiki/sources/`. Each source page's frontmatter includes a `source_file` field (the original filename) and a `source_fingerprint` field (first 200 chars of the original content). For each raw file not already excluded by Check A, compare its fingerprint against every `source_fingerprint` in wiki/sources/. If the fingerprints match but the filenames differ, this file was renamed — warn the user and skip it:

> ⚠️ `new-name.md` looks like a rename of `original-name.md` (already ingested). Skipping.

After both checks, you have a clean list of genuinely new files.

---

## Step 3 — Report

Show the user the new files found. Example format:

```
Found 3 new files in raw/:
  1. articles/transformer-scaling-laws.md
  2. notes/startup-reflection-apr-2026.md
  3. papers/attention-is-all-you-need.pdf

Which would you like to ingest? (reply with numbers, "all", or "skip" to cancel)
```

If no new files are found, say so clearly and stop.

---

## Step 4 — Select

Wait for the user's reply. Accept:
- `"all"` → process every new file
- Numbers or names → process only those
- `"skip"` or `"cancel"` → stop

Process files one at a time in the order the user specified (or the order found, for "all").

---

## Step 5 — Ingest each file

For each selected file, run this sequence:

### 5a. Read
Read the full content of the source file. If it's a PDF or audio transcript, extract as much usable text as possible.

### 5b. Surface and discuss
Before writing anything, present 2–3 bullet points summarizing what you found most notable or surprising in the source. Then pause — ask the user if they want to emphasize anything, redirect the framing, or add context before you write the wiki page. Wait for a response (even "looks good, proceed" counts).

This step matters because the wiki should reflect the user's interpretation, not just yours. A brief exchange here prevents a lot of revision later.

If the user has pre-authorized batch ingestion (e.g. said "ingest all, no discussion needed"), skip the pause and proceed with your best-judgment framing — but note this in the summary so the user knows which pages to review.

### 5c. Write the source summary page
Create `wiki/sources/YYYY-MM-DD-slugified-title.md` (use today's date, slug the source title or filename).

Frontmatter:
```yaml
---
type: source
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
source_file: original-filename.ext
source_fingerprint: |
  <first 200 characters of source content, exactly as-is>
---
```

Store `source_fingerprint` as a YAML literal block scalar (the `|` form) so multi-line content and special characters don't need escaping. Truncate cleanly at a word boundary near 200 chars.

Body structure:
- **Summary**: one focused paragraph — what this source is about and why it matters to this user
- **Key takeaways**: 3–7 bullet points, opinionated (not just "this paper argues X" — note what it implies for the user's work or thinking)
- **Notable quotes**: max 2, each under 15 words, in quotation marks
- **Wiki pages touched**: a list of `[[wikilinks]]` to every page this source informed

### 5d. Update existing wiki pages
Identify which pages in `wiki/self/`, `wiki/areas/`, `wiki/projects/`, `wiki/concepts/`, `wiki/people/`, and `wiki/insights/` this source is relevant to. Read each one. Then update them:
- Add new information or perspectives
- Revise claims the source contradicts (note the contradiction explicitly — don't silently overwrite)
- Add a backlink to the new source page where relevant
- Update the `updated:` frontmatter date

A single source should typically touch 3–10 wiki pages. If you're only touching 1–2, look harder for connections.

### 5e. Create stubs for new entities
If the source introduces a concept, person, tool, or idea that deserves its own page but doesn't have one yet, create a stub:
- Concepts → `wiki/concepts/kebab-case-name.md`
- People → `wiki/people/firstname-lastname.md`
- Projects → `wiki/projects/project-name.md`

Stub frontmatter: include `status: stub`. Body: 1–2 sentences + at least one `[[wikilink]]` to a related page (isolated pages are a smell).

### 5f. Update index.md
- Add the new source page to the **Sources** section
- Add any new wiki pages (stubs included) to their respective sections
- Each entry: `- [[path/to/page]] — one-line description`

### 5g. Append to log.md
Add a new entry at the bottom:

```
## [YYYY-MM-DD] ingest | original-filename.ext

One sentence describing what was ingested and what it touched.
```

---

## Step 6 — Summary

After all selected files are processed, show a brief summary:

```
✅ Ingested 2 files
   • Wiki pages updated: 7
   • Stubs created: 2 (concepts/scaling-laws.md, people/ilya-sutskever.md)
   • Skipped (already ingested): 1
```

---

## Notes on judgment

- **Prefer updating over creating.** If an existing page already covers the topic, add to it rather than making a new page.
- **Be opinionated.** The wiki reflects what matters to this user, not a neutral encyclopedia. Take a stance in summaries.
- **Voice consistency.** Self pages use first person. All other pages use third person.
- **Contradictions are valuable.** If new info conflicts with an existing claim, flag it on the page with a note like `> ⚠️ This conflicts with [source] — needs resolution.` Don't silently resolve it.
