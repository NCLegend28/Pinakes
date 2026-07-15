# autoFix Review Bot

Security-focused automation agent that ingests marketplace reviews, distills actionable issues, plans remediations, and drafts code patches for developer review.

## Layout
- `PRD.md` – product spec.
- `scripts/run_bot.py` – CLI orchestrator.
- `src/review_sources` – connectors for each marketplace.
- `src/analyzers` – sentiment/issue classifiers.
- `src/planners` – remediation planning logic.
- `src/editors` – repo editing guardrails.
- `tests/` – unit coverage.

## Quickstart
```bash
python -m autoFix.scripts.run_bot --config configs/sample_config.json --dry-run
```

## Connectors
- **App Store:** Pulls live reviews via Apple's RSS endpoint when `app_id` is provided; falls back to mocks for offline work.
- **Play Store:** Uses `google-play-scraper` (install with `pip install google-play-scraper`) to stream Android reviews; accepts mock data if the dependency is missing.
- **GitHub Issues:** Treats GitHub issues as internal "reviews" for private trackers; supply `repo`, optional `labels`, and a personal access token for authenticated requests.
- **CSV:** Continue using CSV dumps for bespoke marketplaces.

See `configs/real_connectors.example.json` for end-to-end wiring of the live connectors (replace placeholder tokens before running).

### Editor Guardrails
`RepoEditor` enforces allow-lists by default. For sandbox tests where no app files exist yet, set `"enforce_allow_list": false` in your config to let dry runs read/write outside the allow-list (not recommended for production).

## Security Notes
- Editors enforce allow-lists + dry runs by default.
- All network calls must respect marketplace API quotas and redact PII before logging.
