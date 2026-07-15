# Repository Guidelines

## Project Structure & Module Organization
- `book_pack_builder/` holds the Python pipeline: `run.py` orchestrates CLI flows, while `ingest.py`, `chunking.py`, `summarize.py`, `extract.py`, `indexer.py`, and `pack.py` split the book, call LLMs, and assemble artifacts.
- `prompts/` contains prompt templates tiered by abstraction; keep new prompt files lowercase and describe their focus in the filename.
- `examples/` offers quick-start assets (`short.pdf`, `pack.schema.yaml`) for smoke testing and schema reference.
- Outputs are written to `out/<slug>/` (created at runtime). Do not commit generated results.

## Build, Test, and Development Commands
```bash
python -m venv .venv && source .venv/bin/activate  # setup
pip install -r requirements.txt                    # deps
python -m book_pack_builder.run --help             # inspect CLI options
python -m book_pack_builder.run --input examples/short.pdf --out ./out
```
Use the last command after local changes to confirm the end-to-end pack still builds. Capture meaningful logs with `--verbose` when debugging ingestion or LLM calls.

## Coding Style & Naming Conventions
Follow PEP 8 with 4-space indentation and descriptive snake_case for functions, modules, and filenames. Prefer dataclasses or TypedDicts when shaping structured payloads passed between stages. Keep CLI arguments lowercase with hyphen-separated flags. Add short docstrings for public functions explaining side effects or expected artifacts.

## Testing Guidelines
There is no formal test harness yet; rely on the example run to validate changes. Compare regenerated outputs in `out/<slug>/tiers` and `tables` to ensure deltas are intentional. When adding new logic, isolate deterministic helpers and cover them with `pytest`-style unit tests under `tests/` (create the folder if needed) so they can run via `pytest`.

## Commit & Pull Request Guidelines
Write commit subjects in the imperative mood (`Add chunk overlap option`) and keep them under 65 characters. In pull requests, include: 1) a concise problem statement, 2) a summary of the solution, 3) before/after notes or screenshots if CLI output changed, and 4) the verification command(s) you executed. Link issues or TODO references where applicable and mention any required API keys or environment variables.

## Security & Configuration Tips
Never hard-code API keys; load them from the environment (`OPENAI_API_KEY`, etc.) and document new variables in the README. Be mindful of PDF/EPUB handling—log but do not persist raw text unless the contributor owns the content. Scrub sensitive material before sharing example outputs.
