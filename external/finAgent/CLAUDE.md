# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive Python-based Financial Analysis Agent that combines both document processing and quantitative stock/portfolio analysis. The main application is in `finagent2.py` which integrates:

1. **Document Processing**: Extract and analyze financial documents (PDF, DOCX, TXT)
2. **Stock Analysis**: Fundamental analysis using real-time market data
3. **Portfolio Optimization**: Modern Portfolio Theory-based allocation
4. **Risk Assessment**: ML-based investment recommendations
5. **AI-Powered Analysis**: OpenAI integration for enhanced insights

## Development Setup

### Environment
- **Python Version**: 3.11.7 (managed via pyenv)
- **Virtual Environment**: `venv/` directory contains all dependencies
- **API Keys**: Multiple APIs supported for enhanced functionality

### Setup Commands
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install pandas numpy yfinance scikit-learn requests PyPDF2 python-docx openai python-dotenv flask

# Run the command-line application
python3 finagent2.py

# OR run the web interface
python3 app.py
```

### Dependencies
Core packages installed:
- **Data & Analysis**: `pandas`, `numpy`, `scikit-learn`
- **Financial Data**: `yfinance` (Yahoo Finance API) - **No API key required**
- **Document Processing**: `PyPDF2`, `python-docx`
- **AI Integration**: `openai` 
- **Environment Variables**: `python-dotenv` (loads `.env` file)
- **Web Interface**: `flask` (web UI for document uploads and analysis)
- **Web Requests**: `requests`

## Architecture

### Core Components

**FinancialDataCollector** (`finagent2.py:109-158`)
- Fetches real-time stock data via yfinance
- Retrieves financial statements, price history, and company metrics
- Provides sector comparison data

**DocumentProcessor** (`finagent2.py:160-202`)
- Handles document parsing and text extraction
- Supports PDF, DOCX, and TXT formats
- Unified interface for all document types

**DocumentAnalyzer** (`finagent2.py:204-344`)
- AI-powered document classification and analysis
- Template-based analysis for different document types
- Keyword-based document type detection
- OpenAI integration with fallback capability

**FundamentalAnalyzer** (`finagent2.py:346-561`)
- DCF (Discounted Cash Flow) valuation models
- ML-based investment decision engine
- Risk assessment using financial ratios
- Target price calculations

**PortfolioOptimizer** (`finagent2.py:563-754`)
- Modern Portfolio Theory implementation
- Risk-adjusted portfolio weights
- Rebalancing recommendations
- Sharpe ratio optimization

**InvestmentResearchAgent** (`finagent2.py:756-975`)
- Main orchestrator class
- Combines all analysis capabilities
- Manages both stock and document analysis history
- Export functionality for all results

### Data Models

**Key Enums**:
- `InvestmentDecision`: STRONG_BUY, BUY, HOLD, SELL, STRONG_SELL
- `RiskLevel`: LOW, MODERATE, HIGH, VERY_HIGH  
- `DocumentType`: FINANCIAL_STATEMENT, TAX_DOCUMENT, INVESTMENT_REPORT, etc.

**Data Classes**:
- `CompanyAnalysis`: Comprehensive stock analysis results
- `DocumentAnalysis`: Document processing results
- `PortfolioRecommendation`: Portfolio optimization output

## Usage Patterns

### Web Interface (Recommended)
```bash
# Start the web application
python3 app.py

# Access at: http://localhost:5001
```

**Web Interface Features:**
- **Document Upload**: Drag-and-drop interface for PDF, DOCX, TXT files
- **Stock Analysis**: Enter stock symbols for comprehensive analysis
- **Portfolio Optimization**: Input multiple stocks for optimal allocation
- **Interactive Results**: Visual charts and detailed analysis display
- **Reports Archive**: All reports automatically organized by date in folders
- **Export Functions**: Download analysis results as JSON with date organization

### Programmatic Usage

#### Stock Analysis
```python
agent = InvestmentResearchAgent(openai_api_key="your-key")
analysis = agent.analyze_stock("AAPL")
print(f"Recommendation: {analysis.investment_decision.value}")
```

#### Portfolio Optimization
```python
portfolio_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]
analyses, portfolio_rec = agent.analyze_portfolio(portfolio_symbols)
```

#### Document Processing
```python
doc_analysis = agent.process_document("financial_statement.pdf")
print(f"Document Type: {doc_analysis.document_type.value}")
```

#### Batch Processing
```python
# Multiple stocks
analyses = agent.batch_process_documents(file_paths)

# Multiple documents  
doc_analyses = agent.batch_process_documents(document_paths)
```

## Environment Variables

**Basic functionality works without any API keys** (uses yfinance for stock data).

**Optional API keys for enhanced functionality:**
- `OPENAI_API_KEY` - Enhanced AI document analysis (without this, uses basic template analysis)
- `ALPHA_VANTAGE_KEY` - Alternative financial data source (optional, yfinance is primary)
- `FMP_KEY` - Financial Modeling Prep API (optional, yfinance is primary)

**Environment variable loading:**
- Create a `.env` file in the project root
- The agent automatically loads environment variables from `.env` file
- Format: `OPENAI_API_KEY=your-key-here` (no quotes needed)

## Development Notes

- **Comprehensive Integration**: Single agent handles both document and market analysis
- **ML Integration**: Random Forest classifier for investment decisions
- **Error Handling**: Graceful fallbacks when APIs are unavailable
- **Real-time Data**: Live market data integration via yfinance
- **Date-Organized Reports**: Automatic report organization by date in `reports/YYYY-MM-DD/` folders
- **Export Capabilities**: JSON export for all analysis results with timestamp and type classification
- **Modular Design**: Components can be used independently

## Report Organization

All financial analysis reports are automatically saved and organized by date:

```
reports/
├── 2025-09-12/
│   ├── document_analysis_143052_financial_statement_pdf.json
│   ├── stock_analysis_AAPL_143105.json
│   └── portfolio_analysis_143208.json
├── 2025-09-13/
│   ├── document_analysis_091234_tax_return_pdf.json
│   └── stock_analysis_GOOGL_094521.json
```

**Report Types:**
- `document_analysis_HHMMSS_filename.json` - Document processing results
- `stock_analysis_SYMBOL_HHMMSS.json` - Individual stock analysis
- `portfolio_analysis_HHMMSS.json` - Portfolio optimization results

**Access Reports:**
- Web interface: Navigate to "Reports Archive" to browse by date
- Direct download: Each analysis result page includes download link
- Programmatic: Reports saved in `reports/` directory with date folders

## Legacy Files

- `finagent.py`: Original document-only processor (deprecated)
- Use `finagent2.py` for all new development as it includes all capabilities