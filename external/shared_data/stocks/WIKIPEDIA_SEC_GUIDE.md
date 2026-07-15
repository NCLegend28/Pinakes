## Wikipedia & SEC EDGAR Discovery Sources

**NEW: Expanded ticker discovery with Wikipedia curated lists and official SEC database** 📚

### Quick Overview

| Source | Coverage | Quality | Speed | Best For |
|--------|----------|---------|-------|----------|
| **Wikipedia** | ~600 stocks | High (curated) | Fast | S&P 500, major indices, blue chips |
| **SEC EDGAR** | ~13,000 companies | Mixed | Slow | Complete coverage, niche industries |
| **Hardcoded** | ~50 stocks | High | Instant | Tech giants, popular stocks |

---

## Wikipedia Scraper

### What It Does
Scrapes curated stock lists from Wikipedia pages:
- **S&P 500** (~500 stocks) - Large cap US stocks
- **Dow Jones Industrial Average** (30 stocks) - Blue chip leaders
- **NASDAQ-100** (~100 stocks) - Tech-heavy index
- **Big Tech** (8 stocks) - FAANG+ companies

### Why Use It?
✅ **Curated lists** - Already vetted for quality
✅ **Comprehensive** - Covers major indices
✅ **Fast** - No rate limits
✅ **Free** - No API key needed
✅ **Sector diversity** - Broad market coverage

### Usage

```python
from wikipedia_scraper import WikipediaScraper

scraper = WikipediaScraper()

# Scrape all sources
results = scraper.scrape_all()

# Get unique tickers
tickers = scraper.get_unique_tickers(results)
print(f"Found {len(tickers)} stocks")  # ~600 unique

# Export to CSV
scraper.export_to_csv('wikipedia_stocks.csv')
```

### Example Output

```
================================================================================
WIKIPEDIA STOCK SCRAPER
================================================================================

🔍 Scraping S&P 500 from Wikipedia...
   ✓ Found 503 S&P 500 stocks

🔍 Scraping Dow Jones from Wikipedia...
   ✓ Found 30 DJIA stocks

🔍 Scraping NASDAQ-100 from Wikipedia...
   ✓ Found 102 NASDAQ-100 stocks

🔍 Scraping Big Tech from Wikipedia...
   ✓ Found 8 Big Tech stocks

✓ Discovered 512 unique tickers from Wikipedia
```

### Advantages

1. **High quality** - Only includes actively traded, established companies
2. **Sector balance** - Covers all major sectors
3. **Market cap weighted** - Focuses on larger, more liquid stocks
4. **News coverage** - Well-known companies = more sentiment data

### Limitations

- **No small caps** - Misses emerging companies
- **US-focused** - Primarily US exchanges
- **Static** - Lists update slowly (quarterly rebalancing)
- **Parsing issues** - Wikipedia format changes can break scraper

---

## SEC EDGAR Scraper

### What It Does
Fetches the **complete database** of all US public companies from the SEC:
- **13,000+ companies** - Every US public company
- **SIC codes** - Industry classification (from 1987)
- **CIK numbers** - Official SEC identifiers
- **Official data** - Straight from the SEC

### Why Use It?
✅ **Complete coverage** - Literally every public company
✅ **Industry filtering** - SIC codes allow industry-specific discovery
✅ **Official source** - Most authoritative data
✅ **Free** - No API key needed
✅ **Hidden gems** - Find overlooked opportunities

### Usage

```python
from sec_edgar_scraper import SECEdgarScraper

scraper = SECEdgarScraper()

# Fetch all companies
all_companies = scraper.fetch_company_tickers()
print(f"Found {len(all_companies)} companies")  # ~13,000

# Filter by industry (Software)
software = scraper.get_industry_stocks('Technology', 'software')
print(f"Found {len(software)} software companies")

# Filter by industry (Pharma)
pharma = scraper.get_industry_stocks('Healthcare', 'pharma')
print(f"Found {len(pharma)} pharma companies")

# Export to CSV
scraper.export_to_csv(software, 'sec_software_stocks.csv')
```

### SIC Code Industry Examples

```python
# Available industries in scraper:

'Technology': {
    'software': range(7370, 7380),      # SIC 7370-7379
    'semiconductors': range(3570, 3578),
    'internet': [7375]
}

'Healthcare': {
    'pharma': [2834, 2835, 2836],
    'biotech': [2836],
    'medical_devices': range(3841, 3846)
}

'Financials': {
    'banks': range(6020, 6036),
    'insurance': range(6310, 6332),
    'investment': range(6200, 6212)
}

'Automotive': {
    'manufacturers': [3711],
    'parts': range(3714, 3715)
}
```

### Example Output

```
================================================================================
SEC EDGAR COMPANY DATABASE SCRAPER
================================================================================

🔍 Fetching SEC EDGAR company database...
   ✓ Fetched 13,247 companies from SEC EDGAR

Symbol   Name                                              CIK          SIC
--------------------------------------------------------------------------------
AAPL     Apple Inc.                                        0000320193   3571
MSFT     Microsoft Corporation                             0000789019   7372
GOOGL    Alphabet Inc.                                     0001652044   7370
PATH     UiPath Inc.                                       0001797526   7372
...

🔍 Filtering by SIC codes: [7370, 7371, 7372, ...]
   ✓ Found 847 companies matching SIC codes

SOFTWARE COMPANIES (SIC 7370-7379)
================================================================================
Symbol   Name                                              CIK          SIC
--------------------------------------------------------------------------------
MSFT     Microsoft Corporation                             0000789019   7372
ORCL     Oracle Corporation                                0001341439   7372
CRM      Salesforce Inc.                                   0001108524   7372
ADBE     Adobe Inc.                                        0000796343   7372
...
```

### Advantages

1. **Complete coverage** - Every public company, no exceptions
2. **Industry classification** - SIC codes allow precise filtering
3. **Official data** - Directly from SEC, highly reliable
4. **Hidden opportunities** - Find small/mid-cap gems
5. **Niche industries** - Discover sector-specific plays

### Limitations

⚠️ **Includes junk** - Many tiny, illiquid companies
⚠️ **SIC codes outdated** - Classification from 1987 (doesn't understand "software as a service")
⚠️ **Slow** - ~13,000 companies takes time to process
⚠️ **No market data** - Must use yfinance to validate (market cap, volume)
⚠️ **Rate limits** - SEC API slower than Wikipedia

---

## Integration with Discovery System

### Automatic Integration

The main `ticker_discovery.py` now includes both sources:

```python
from ticker_discovery import TickerDiscovery

discovery = TickerDiscovery()

# Discover with Wikipedia (default)
tickers = discovery.discover_all(use_wikipedia=True)

# Discover with SEC EDGAR (optional, slower)
tickers = discovery.discover_all(use_wikipedia=True, use_sec=True)
```

### Recommended Strategy

**Phase 1: Wikipedia Only (Recommended)**
```python
discovery.discover_all(use_wikipedia=True, use_sec=False)
```
- Fast (~2 minutes)
- High quality stocks
- Good coverage (~600 stocks)
- **Best for: Initial setup, daily/weekly updates**

**Phase 2: Add SEC for Niche (Optional)**
```python
discovery.discover_all(use_wikipedia=True, use_sec=True)
```
- Slower (~10 minutes)
- Complete coverage
- Many low-quality stocks filtered out
- **Best for: Monthly deep dives, industry-specific searches**

---

## Performance Tracking

Track which sources find better opportunities:

```python
from source_performance_tracker import SourcePerformanceTracker

tracker = SourcePerformanceTracker()

# Log discovery
tracker.log_discovery('wikipedia', wiki_tickers, opportunity_scores)
tracker.log_discovery('sec_edgar', sec_tickers, opportunity_scores)

# Log prediction results
tracker.log_prediction_result('AAPL', 'wikipedia', rmse=2.15, mape=1.8)

# Compare sources
tracker.display_comparison()
```

Output:
```
================================================================================
DISCOVERY SOURCE PERFORMANCE COMPARISON
================================================================================

Source       Discoveries  Total Tickers  Avg Score  Median Score  Avg RMSE  Predictions
---------------------------------------------------------------------------------------
wikipedia    5            512            76.3       75.1          $3.24     15
hardcoded    5            50             68.7       67.2          $4.18     8
sec_edgar    2            847            52.1       48.9          None      0

🏆 Best Opportunity Scores: wikipedia (76.3)
🎯 Best Prediction Accuracy: wikipedia (RMSE: $3.24)
```

This shows **Wikipedia finds higher-quality opportunities** than other sources!

---

## Testing the New Sources

### Test 1: Wikipedia Scraper

```bash
cd ~/projects/shared_data/stocks
python wikipedia_scraper.py
```

Expected:
- Scrapes S&P 500, DJIA, NASDAQ-100, Big Tech
- ~500-600 unique tickers
- Exports to `wikipedia_stocks.csv`

### Test 2: SEC EDGAR Scraper

```bash
python sec_edgar_scraper.py
```

Expected:
- Fetches ~13,000 companies
- Shows software/pharma examples
- Exports to `sec_edgar_top500.csv`

### Test 3: Integrated Discovery

```bash
python ticker_discovery.py
```

Expected:
- Discovers from all sources (hardcoded, Wikipedia, optionally SEC)
- Validates each ticker
- Asks to update config

---

## Comparison: Which Source To Use?

| Use Case | Recommended Source | Why |
|----------|-------------------|-----|
| **Daily updates** | Wikipedia | Fast, high quality, covers major stocks |
| **Weekly deep dive** | Wikipedia + Hardcoded trending | Balance speed and opportunities |
| **Monthly research** | Wikipedia + SEC (limited) | Complete coverage, find hidden gems |
| **Industry-specific** | SEC EDGAR with SIC filter | Pharma, software, banks, etc. |
| **Blue chips only** | Wikipedia (DJIA + S&P 500) | Established companies only |
| **Growth stocks** | Hardcoded trending + Wikipedia NASDAQ-100 | High momentum plays |

---

## Real-World Example

### Scenario: Find all publicly traded software companies

**Option 1: Wikipedia (incomplete but fast)**
```python
scraper = WikipediaScraper()
results = scraper.scrape_all()
nasdaq_stocks = [s for s in results['nasdaq100']]  # ~40 tech stocks
```

**Option 2: SEC EDGAR (complete but slow)**
```python
scraper = SECEdgarScraper()
software = scraper.get_industry_stocks('Technology', 'software')  # ~850 companies
```

**Best Approach: Combine both**
```python
# Wikipedia for major players
wiki_software = scraper_wiki.scrape_nasdaq100()

# SEC EDGAR for hidden gems
sec_software = scraper_sec.get_industry_stocks('Technology', 'software')

# Filter SEC results by market cap/volume
from ticker_filters import TickerFilter
filter = TickerFilter()
quality_sec = filter.score_and_rank(sec_software, top_n=50)

# Combine: Major players + top hidden gems
all_software = wiki_software + [s['symbol'] for s in quality_sec]
```

Result: ~90 high-quality software stocks (40 from Wikipedia + 50 from SEC)

---

## Troubleshooting

### Wikipedia scraper fails

**Issue**: `Could not find S&P 500 table`

**Cause**: Wikipedia changed page structure

**Fix**: Update table selector in `wikipedia_scraper.py`:
```python
table = soup.find('table', {'class': 'wikitable sortable'})
```

### SEC EDGAR rate limit

**Issue**: `429 Too Many Requests`

**Cause**: Too many API calls too fast

**Fix**: Add delays in `sec_edgar_scraper.py`:
```python
import time
for company in companies:
    # ... process ...
    time.sleep(0.1)  # 10 requests/sec
```

### No tickers discovered

**Issue**: All tickers filtered out

**Cause**: Quality filters too strict

**Fix**: Lower thresholds in `ticker_discovery.py`:
```python
MIN_MARKET_CAP = 500_000_000  # $500M instead of $1B
MIN_PRICE = 3.0  # $3 instead of $5
```

---

## Summary

### Wikipedia Scraper
✅ Use for: Fast, high-quality, major stock discovery
✅ Coverage: ~600 stocks from S&P 500, DJIA, NASDAQ-100
✅ Best for: Daily/weekly automated updates

### SEC EDGAR Scraper
✅ Use for: Complete coverage, industry-specific searches
✅ Coverage: ~13,000 all US public companies
✅ Best for: Monthly deep dives, niche industries

### Integration
Both scrapers are now integrated into `ticker_discovery.py`:
```python
# Default: Wikipedia only (fast, high quality)
discovery.discover_all()

# Optional: Add SEC EDGAR (slow, comprehensive)
discovery.discover_all(use_sec=True)
```

### Performance Tracking
Use `source_performance_tracker.py` to measure which sources find better opportunities and optimize your discovery strategy over time.

**Result: Never miss an opportunity, backed by official data sources!** 🚀
