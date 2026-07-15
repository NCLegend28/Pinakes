---
type: insight
tags: [engineering-practice, tooling, ci, code-quality, financio]
created: 2026-06-23
updated: 2026-06-23
status: active
---

# You out-tool bug classes; you don't out-know them

**The realization (2026-06-23)**: After a long string of deployment bugs on
[[wiki/projects/financio-v2|Financio-V2]] — a missing `autocomplete` attribute
that broke password-manager paste, an arch-pinned rollup dep, a transitive
`matplotlib` import, a stale Alpaca key, a missing tickers file — the instinct
was "I need to know more / be a better coder." That's the wrong lesson.

**The right lesson**: senior engineers don't memorize footguns. They install
cheap, automated checks that catch entire *classes* of mistakes before a human
ever sees them. The skill is building the safety net, not having perfect recall.
A chef doesn't *remember* not to undercook chicken — they own a thermometer.

## The layered net (each layer catches before the next)

| Layer | Tool | Bug classes it kills | Which Financio bug it would've caught |
|---|---|---|---|
| **Static analysis** | ESLint + `eslint-plugin-jsx-a11y`; Chrome **Lighthouse** | accessibility, form attrs, dead code, type errors | the missing `autocomplete`/`name` on the auth inputs (Lighthouse has a literal "use appropriate autocomplete" audit) |
| **Type check** | `tsc --noEmit`, `mypy`/`pyright` | wrong types, missing symbols | `SELECTED_TICKERS` import that doesn't exist |
| **CI build + boot** | GitHub Action: `docker compose build && up`, hit `/health` | "does it even start" bugs | rollup arch pin, `matplotlib` import, missing `current_tickers.txt`, the unhealthy backend |
| **Pre-commit hooks** | `pre-commit`: secret scan, custom greps | leaked secrets, bad path patterns | the live Alpaca key committed to git; `Path.home()/'projects'` on the external drive |
| **Checklists** | human, for security/money/auth paths | the stuff tools can't reason about | mode-aware key selection, RLS, "is this plaintext HTTP for live money" |

## Operating principle

When a bug bites, don't just fix it — ask **"what automated check would have
caught this whole category?"** and install that. One Lighthouse run catches every
future form-attribute bug. One CI boot-test catches every future "image doesn't
start" bug. The fix scales; memorizing the specific bug does not.

## Minimum viable net for Financio (highest leverage first)

1. `npm run lint` with `jsx-a11y` enabled + a Lighthouse pass on auth/critical pages.
2. CI job that builds `docker-compose.vps.yml` on x64 and boots it (would have caught ~half of the 2026-06-23 deploy bugs).
3. `pre-commit` with `detect-secrets` + a grep rule banning `Path.home() / 'projects'`.
4. A short written checklist for auth forms and anything touching real money.

## Related

- [[wiki/projects/financio-v2]] — the deploy that surfaced this
- [[wiki/projects/project-dependency-map]] — itself the output of a "audit the whole class" pass
