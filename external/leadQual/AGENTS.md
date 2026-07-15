# Repository Guidelines

## Project Structure & Module Organization
The repository splits into two active products. The multi-provider lead qualification workflow lives at the root (`index.ts`, `workflow-*.ts`, `config/`, `templates/`) with shared utilities in `lib/`. The SaaS dashboard resides in `saas-platform/` and follows standard Next.js app directory conventions (`app/` for routes, `components/` for UI, `lib/` for data helpers, `scripts/` for maintenance). Supabase SQL migrations, seeds, and helper docs sit under `database/`, while business and delivery references are in the Markdown files at the root (start with `START_HERE.md`, `MVP_ROADMAP.md`, and `HANDOFF_TO_CODEX.md`).

## Build, Test, and Development Commands
From the root run `npm install` once, then `npm run dev` to execute the agent workflow scenarios or `npm run test:hot|warm|cold|faq|spam` for targeted cases. `npm run type-check` must stay green before handing off. For the SaaS app: `cd saas-platform && npm install`, `npm run dev` for the dashboard, `npm run lint` prior to commits, and `npm run seed:demo` to load sample tenants (requires Supabase env vars). Use `npm run build` in both packages to confirm deploy readiness.

## Coding Style & Naming Conventions
Keep strict TypeScript types and prefer small composable functions. Workflow files use four-space indentation and snake_case file names; the Next.js app relies on Prettier defaults (two-space, PascalCase React components, kebab-case folders). Tailwind utility order is managed by the ESLint config; do not hand-format. Server actions stay in `lib/` or `app/**/actions.ts`, and Zod schemas live beside their consumers.

## Testing Guidelines
Before opening a PR, rerun the workflow scenario most impacted by your change plus `npm run type-check`. In the dashboard ensure `npm run lint` and `npm run build` succeed, and manually verify seeded flows (e.g., billing downloads, integrations links) until automated tests exist. Capture screenshots or console output for any UI-affecting work and note Supabase tables touched. Record new fixtures under `templates/` when adjusting agent prompts.

## Commit & Pull Request Guidelines
Aim for conventional commits (`feat:`, `fix:`, `chore:`) scoped to one concern. Reference relevant docs or tickets in the PR body, list validation commands executed, and flag follow-up tasks for partner agents. Keep configuration edits isolated, and never overwrite `.env` samples with secrets.

## Agent Collaboration
Sync with Claude Code via `CLAUDE.md` updates and leave a short summary in this `AGENTS.md` when workflows change. Announce planned schema or shared utility edits in the handoff channel, prefer additive changes over rewrites, and pause if you encounter unexpected local modifications.
