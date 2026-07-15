# CLAUDE.md

Guidance for Claude Code when contributing to the **leadQual** repository.

## Current Project Snapshot
- **Core workflow**: TypeScript multi-agent lead qualification engine (multi-provider, DeepSeek/Ollama by default) in the repo root.
- **SaaS platform**: Fresh Next.js 15 app under `saas-platform/` that will host tenant dashboards, onboarding, and the embed widget described in `MVP_ROADMAP.md`.
- **Database assets**: SQL schema & seeds in `database/` ready for Supabase/Neon. Follow `database/SUPABASE_SETUP.md` when wiring persistence.
- **Business docs**: Start with `START_HERE.md`, then `EXECUTIVE_SUMMARY.md`, `PRODUCT_STRATEGY.md`, `ARCHITECTURE.md`, and `MVP_ROADMAP.md` for context and milestone planning.

## Local Development
### Lead Qualification Workflow
1. `npm install`
2. Copy `.env.example` → `.env` and set at least one provider key (OpenAI, Anthropic, Groq, or configure Ollama via `OLLAMA_BASE_URL`).
3. Run scenarios: `npm run test:hot` / `test:warm` / `test:cold` / `test:faq` / `test:spam`. Use `npm run dev <index>` to target a specific case.
4. Type checking: `npm run type-check`.

**Important**: `workflow-ollama.ts` is the operational path today. Preserve its capability matrix and JSON parsing helpers in `lib/` when extending or refactoring.

### SaaS Next.js App (`saas-platform/`)
1. `cd saas-platform && npm install`.
2. Use `npm run dev` for local work, `npm run lint` before pushing UI changes, `npm run build` to validate deployments.
3. Environment bootstrapping will use `.env.local` (see `database/SUPABASE_SETUP.md` for required Supabase keys once back-end APIs come online).
4. React 19 + Tailwind 4 are in play; keep components server-first unless client hooks are required.

## Coding Conventions
- TypeScript strict mode throughout; add interfaces/zod schemas in `config/` or `lib/` as needed.
- Use four-space indentation in workflow TS files (matches existing style) and the default Next.js formatting (Prettier) inside `saas-platform/`.
- Prefer functional additions over rewrites—add new workflow entry points or feature flags instead of editing proven guard/qualifier logic.

## Testing & Quality
- Ensure all npm scripts above succeed before handing work back.
- For new workflow features, add representative fixtures under `templates/` or inject additional test cases in `index.ts`.
- For dashboard changes, capture screenshots or note key pages touched so the team can verify parity.

## Coordination Notes
- Codex is partnering on this repo; announce major changes in `CLAUDE.md` after completing a task and check for updates from Codex before starting new work.
- Align commits with `MVP_ROADMAP.md` milestones (database setup → workflow integration → widget → dashboard → billing).
- Touch `shared` assets (e.g., `config/models.ts`, Supabase schema) only when requirements are finalized—coordinate before altering defaults.

Stay tight on scope, keep the multi-provider workflow stable, and focus current effort on bringing the Next.js platform online per the documented roadmap.
