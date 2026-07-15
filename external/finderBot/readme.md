# Chip Supply Bot

## 🧠 Purpose
This is a full-stack search bot designed to identify **publicly traded companies** involved in a specific hardware or electronics component supply chain—starting with inputs like:

```
magnetic battery connector
```

The goal is to output:
- A structured list of relevant companies
- Their **tickers**, **stock prices**, **percent changes**, **volume**, and **role** in the supply chain

---

## 🔧 Current Capabilities
This bot currently operates as a **damn good search bot**, not a generative agent. It relies on deterministic classification and a curated company database.

### ✔️ Supported Flow:
1. **User Input:** A component or industry keyword (e.g. "magnetic pogo pins")
2. **Tag Classification:** Hardcoded mappings via `TAG_RULES` in `classify.py`
3. **Company Matching:** Filtered from a curated list in `company_lookup.py`
4. **Stock Data Collection:** Pulled using Yahoo Finance via `yfinance`
5. **Frontend Display:** Company cards with:
   - Name
   - Ticker
   - Industry
   - Role
   - Price, % change, and volume

---

## 🤖 LLM-Enhanced Agent Mode (Optional Upgrade)
To begin integrating a generative agent, we include `llm_classify.py`, which uses an OpenAI API call to dynamically tag user-provided components.

### 🧠 How it Works:
- `classify_component()` becomes a wrapper around a prompt like:
  ```
  "Given the component: 'magnetic battery connector', return 3 relevant tags that represent industries, materials, or technologies used in its supply chain."
  ```
- Returns tags such as `['rare earth', 'connectors', 'semiconductors']`

### 📁 Files Added:
- `llm_classify.py` — handles prompt engineering and OpenAI interaction
- `config.py` — stores your API key securely via environment variable or .env

---

## 🧰 Prompt Engineering Summary (for Agents)
To extend or refactor this bot for LLM agents or intelligent systems, the following prompt structure is optimal:

### 📌 Ideal Prompt Template:
```
I need a list of publicly traded companies involved in the [COMPONENT], including:
- Raw material suppliers
- Component manufacturers
- Chip/system integrators
- Company tickers and stock data
- Each company's role in the supply chain
Return this in a structured JSON or table format.
```

### 🧪 Sample Prompt:
```
List all public companies involved in making magnetic battery connectors used in mobile devices. Include rare earth miners (e.g. neodymium), pogo pin manufacturers, and charge IC makers. Give me ticker, stock price, percent change, and supply chain role.
```

---

## 🚀 Project Structure
```
project/
├── backend/
│   ├── main.py              # FastAPI endpoint `/analyze`
│   ├── classify.py          # Component-to-tag mapping (default)
│   ├── llm_classify.py      # OpenAI-powered classification (optional)
│   ├── company_lookup.py    # Static company DB + filter logic
│   ├── stock_data.py        # Pulls price/volume data from yfinance
│   ├── config.py            # Manages API key loading from .env
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/CompanyCard.tsx
│   │   └── api.ts
│   ├── index.html
│   ├── package.json
│   └── tailwind.config.js
├── docker-compose.yml
└── README.md
```

---

## 🧭 Future Agent Upgrades
- [ ] LLM-based component → tag mapping (OpenAI or Claude)
- [ ] Crunchbase API or scraping for live company role detection
- [ ] Auto-expanding company DB from industry tags
- [ ] Optional financial analytics (PE ratio, volume anomaly, etc.)
- [ ] Multi-agent task delegation

---

## 🧪 Example Output (API Response)
```json
[
  {
    "name": "MP Materials",
    "ticker": "MP",
    "industry": "Rare Earths",
    "role": "Neodymium supplier",
    "price": 30.55,
    "change": 1.35,
    "volume": 25329263
  },
  {
    "name": "TE Connectivity",
    "ticker": "TEL",
    "industry": "Connectors",
    "role": "Pogo pin manufacturer",
    "price": 136.78,
    "change": -0.84,
    "volume": 1583281
  }
]
```

---

## 🛠 Dev Notes
- Be explicit with `component` query.
- Tags are currently matched via simple rules or an OpenAI LLM if enabled.
- Output always structured for React frontend display.

To evolve this bot into an agent-ready system, focus next on:
- Expanding `llm_classify.py` with more robust prompting and fallback logic
- Auto-caching OpenAI results for speed
- Training a domain-specific tagging model or fine-tuned classifier
