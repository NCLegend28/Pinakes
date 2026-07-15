# 📚 Book Translator

Translate entire books (PDF, EPUB, TXT) between languages using Claude AI.
Designed for speed (async concurrent chunks), reliability (resume on crash), and
extensibility (add new language pairs in one place).

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Translate a book
python main.py my_book.pdf --pair zh-en
```

---

## Supported Formats

| Format | Extension |
|--------|-----------|
| PDF    | `.pdf`    |
| EPUB   | `.epub`   |
| Plain text | `.txt`, `.md` |

---

## Language Pairs

```
python main.py --list-pairs
```

| Key   | From     | To      |
|-------|----------|---------|
| zh-en | Chinese  | English |
| en-zh | English  | Chinese |
| zh-es | Chinese  | Spanish |
| en-es | English  | Spanish |
| es-en | Spanish  | English |
| ja-en | Japanese | English |
| fr-en | French   | English |

---

## Options

```
python main.py [FILE] [OPTIONS]

Options:
  --pair, -p       Language pair key (default: zh-en)
  --output, -o     Output file path (auto-generated if not set)
  --format, -f     Output format: txt or html (default: txt)
  --concurrent, -c Max parallel API calls (default: 5)
  --model, -m      Claude model (default: claude-opus-4-5)
  --chunk-tokens   Chunk size in tokens (default: 1500)
  --api-key        Anthropic API key
  --list-pairs     Show all language pairs
```

### Examples

```bash
# Chinese PDF → English TXT
python main.py book.pdf --pair zh-en

# EPUB → HTML output (renders as a nice readable page)
python main.py novel.epub --pair zh-en --format html

# Slower but careful (fewer concurrent calls, smaller chunks)
python main.py long_book.pdf --pair zh-en --concurrent 2 --chunk-tokens 800

# Custom output path
python main.py story.txt --pair ja-en --output ./output/japanese_story_en.txt
```

---

## Resume Support

Translation progress is automatically saved to `.translation_cache/`.
If the process is interrupted (network error, rate limit, Ctrl+C),
just re-run the exact same command — it will skip already-translated chunks.

---

## Adding a New Language Pair

Open `core/translator.py` and add an entry to `LANGUAGE_PAIRS`:

```python
"de-en": {
    "source_name": "German",
    "target_name": "English",
    "system_prompt": (
        "You are an expert literary translator specializing in German to English translation. "
        "Preserve paragraph structure, tone, and stylistic nuances. "
        "Return ONLY the translated text — no commentary, no explanations, no markdown."
    ),
},
```

That's it. No other files need to change.

---

## Architecture

```
book_translator/
├── main.py              ← CLI (argparse + rich)
├── core/
│   ├── translator.py    ← Async Claude engine + language pair registry
│   ├── chunker.py       ← Paragraph-aware text splitting
│   └── progress.py      ← Resume/cache logic
├── parsers/
│   ├── __init__.py      ← Format dispatcher
│   ├── pdf_parser.py    ← PyMuPDF
│   ├── txt_parser.py    ← Multi-encoding plain text
│   └── epub_parser.py   ← ebooklib + BeautifulSoup
├── writers/
│   └── __init__.py      ← TXT and HTML output
└── requirements.txt
```

### How chunking works

Large books can't be sent to the API in one shot. The chunker splits text into
~1500-token pieces along paragraph boundaries — like tearing a book at chapter
breaks rather than mid-sentence. This ensures the translator always receives
complete, grammatically whole units, which dramatically improves output quality.

### How concurrency works

Five chunks are translated simultaneously by default (controlled by a semaphore).
Think of it as five translators working different sections of the book in parallel.
Increase `--concurrent` if you have a high rate limit; decrease it if you're
hitting 429 errors.
