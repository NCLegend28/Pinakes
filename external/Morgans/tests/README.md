# Morgans Test Harness

Fast, deterministic tests for the sentiment pipeline. Designed so Claude (or
any contributor) can verify changes in **under 30 seconds** without:

- Hitting your NewsAPI / Reddit / SEC quotas
- Waiting on real network I/O
- Running the full 485-ticker batch

## What's here

```
tests/
├── conftest.py                # pytest fixtures — mock HTTP, fake analyzers
├── tickers_test.json          # 5-ticker subset (GOOGL, NVDA, AAPL, JPM, BAC)
├── fixtures/
│   ├── sec_submissions_GOOGL.json   # canned SEC submissions API response
│   ├── sec_filing_10q.html          # canned 10-Q HTML for analyze_filing_text
│   └── newsapi_aapl.json            # canned NewsAPI response
├── test_sec_filings.py        # SEC analyzer correctness (CIK, parsing, scoring)
├── test_automate_threading.py # scheduler thread isolation + re-entry locks
└── test_stock_parallel.py     # parallelized stock_news produces same results
                                 as sequential
```

## Run

```bash
# All tests
.venv/bin/pytest tests/ -v

# Single file
.venv/bin/pytest tests/test_sec_filings.py -v

# Just one test
.venv/bin/pytest tests/test_sec_filings.py::test_cik_lookup -v

# Watch mode (re-runs on file save) — install pytest-watch first
pip install pytest-watch && ptw tests/
```

## What gets validated

| Test                               | Catches                                       |
|------------------------------------|-----------------------------------------------|
| `test_cik_lookup`                  | Regression of the GOOGL→CapitalG bug          |
| `test_lm_scoring`                  | Polarity collapsing to +1.0 (cover-page bug)  |
| `test_filing_type_filter`          | Accidentally re-including Form 4 noise        |
| `test_threading_isolation`         | A long job blocking short ones again          |
| `test_reentry_skip`                | Concurrent runs of the same job piling up     |
| `test_parallel_matches_sequential` | Parallelization losing or duplicating tickers |
| `test_thread_local_reddit`         | PRAW session contention across workers        |

## Adding a new test

When you fix a bug, write a test that **fails on the old code and passes on
the new code**. Save it next to the others. The harness exists so you (or
Claude) can re-run all checks in seconds before pushing — no need to wait
21 hours to discover stock_news still serializes.
