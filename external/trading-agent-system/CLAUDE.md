# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Technology Stack

- **Language:** Python 3.11+
- **AI SDK:** Anthropic Python SDK
- **Model:** Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
- **Config:** YAML
- **Logging:** JSON Lines (JSONL)
- **Architecture:** Modular, class-based

## Key Design Principles

- **Separation of Concerns:** Each agent has distinct responsibilities
- **Composability:** Agents work independently and collaboratively
- **Auditability:** All decisions logged with timestamps and rationale
- **Extensibility:** Easy to add new agents or workflows
- **Testability:** Each component independently testable
- **Reusability:** All modules designed as standalone, reusable components

## Architecture Overview

Multi-tiered AI agent system for algorithmic trading. Each agent is specialized through 5 curated books and collaborates via predefined workflows.

### Agent Hierarchy (12 Total Agents)

**Tier 1 Operations (agents/tier1_operations/)** - Core operational agents:
- **Strategy Architect**: Strategy design & validation, backtest analysis, signal generation
- **Risk Manager**: Position sizing, portfolio risk limits, VAR/CVaR monitoring, drawdown management
- **Infrastructure Engineer**: System architecture, deployment, API infrastructure
- **Execution Specialist**: Order execution, slippage analysis, market microstructure
- **Data Manager**: Data pipelines, storage, validation, availability

**Tier 2 Specialists (agents/tier2_specialists/)** - Domain-specific consultants:
- **Compliance Counsel**: Regulatory compliance, legal requirements
- **Tax Strategist**: International tax implications, tax optimization
- **FX Specialist**: Currency management, FX hedging
- **Regional Specialist**: Market-specific rules, regional requirements
- **Psychology Coach**: Trading psychology, behavioral aspects

**Tier 3 Council (agents/tier3_council/)** - Strategic oversight:
- **Strategy Council**: High-level strategic decision making, macro analysis
- **Quant Research Council**: Advanced quantitative research, hypothesis evaluation

### Core Components

**Base Agent Class** (`agents/base_agent.py`):
```python
class TradingAgent:
    def __init__(self, name, role, tier, book_summaries, tools=None, system_context=None)
    def _load_knowledge(self) -> str
    def _build_system_prompt(self) -> str
    def query(self, user_message, context=None, temperature=0.7, max_tokens=4096) -> Dict
    def _parse_response(self, response: str) -> Dict
    def _log_decision(self, query: str, result: Dict)
    def clear_history(self)
    def get_history(self) -> List[Dict]
```

**Agent Coordinator** (`orchestration/coordinator.py`):
```python
class AgentCoordinator:
    def register_agent(self, agent: TradingAgent)
    def route_query(self, query: str, context: Dict = None) -> Dict
    def execute_workflow(self, workflow_name: str, initial_context: Dict) -> Dict
    def collaborative_query(self, query: str, agent_names: List[str], context: Dict = None) -> Dict
```

**Agent Factory Pattern** - Each agent has a factory function:
```python
def create_[agent_name]() -> TradingAgent:
    loader = AgentConfigLoader()
    config = loader.get_agent_config('[config_key]')
    return TradingAgent(name=config['name'], role=config['role'],
                       tier=config['tier'], book_summaries=config['books'],
                       system_context=system_context)
```

### Directory Structure

- `agents/`: Agent implementations
  - `base_agent.py`: Base class for all agents
  - `tier1_operations/`: 5 operational agents
  - `tier2_specialists/`: 5 specialist agents
  - `tier3_council/`: 2 council agents
- `orchestration/`: Coordination layer
  - `coordinator.py`: Main orchestration logic
  - `workflows.py`: Multi-agent workflow definitions
  - `router.py`: Query routing logic
- `tools/`: Shared utilities
  - `data_access.py`: Data retrieval and storage
  - `calculators.py`: Risk/position sizing calculators
  - `compliance.py`: Compliance checking utilities
- `memory/`: Persistent state
  - `conversations/`: Conversation history
  - `decisions/`: Decision logs (JSONL)
  - `metrics/`: Performance metrics
- `knowledge/`: Knowledge base
  - `summaries/`: 60 book summaries (5 per agent)
  - `shared/`: Cross-cutting documentation
  - `context/`: Agent-specific context
- `config/`: Configuration files
  - `agents_config.yaml`: Agent configurations
  - `workflows_config.yaml`: Workflow definitions
- `tests/`: Test suite
  - `test_agents.py`: Agent unit tests
  - `test_coordinator.py`: Coordinator tests
  - `test_workflows.py`: Workflow integration tests

## Configuration

### Environment Variables (.env)
```bash
ANTHROPIC_API_KEY=your_api_key_here
DEFAULT_MODEL=claude-sonnet-4-5-20250929
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=4096
KNOWLEDGE_BASE_PATH=knowledge/
MEMORY_PATH=memory/
LOGS_PATH=memory/decisions/
MAX_CONVERSATION_HISTORY=20
ENABLE_DECISION_LOGGING=true
ENABLE_METRICS_TRACKING=true
```

### Agent Configuration Schema (agents_config.yaml)
Each agent defined with:
- `name`: Display name
- `tier`: 1, 2, or 3
- `role`: Primary responsibility description
- `books`: List of 5 book summary filenames
- `responsibilities`: List of specific duties
- `decision_areas`: Key questions the agent addresses
- `handoffs`: Protocol for consulting other agents
- `critical_rules`: (Optional) Must-follow rules for the agent

## Predefined Workflows

1. **Daily Operations Workflow**
   - Data Manager → Strategy Architect → Risk Manager → Execution Specialist → Psychology Coach

2. **New Strategy Workflow**
   - Quant Research Council → Strategy Architect → Data Manager → Risk Manager → Execution Specialist → Compliance Counsel → Strategy Council

3. **New Market Workflow**
   - Regional Specialist → Compliance Counsel → Tax Strategist → FX Specialist → Infrastructure Engineer → Strategy Council

4. **Risk Review Workflow**
   - Data Manager → Risk Manager → Strategy Architect → Psychology Coach → Strategy Council

## Development Commands

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with ANTHROPIC_API_KEY

# Initialize system
python main.py --init
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agents.py -v

# Run with coverage
pytest tests/ --cov=agents --cov=orchestration --cov=tools
```

### Running
```bash
# Test single agent
python -c "from agents.tier1_operations.strategy_architect import create_strategy_architect; agent = create_strategy_architect(); print(agent.query('What makes a good momentum strategy?'))"

# Test routing
python main.py --test-routing

# Execute workflow
python main.py --workflow new_market --country Singapore

# Interactive mode
python main.py --interactive
```

## Implementation Patterns

### Agent System Prompt Structure
```
You are {name}, a specialized AI agent in a multi-agent trading system.

ROLE: {role}
TIER: {tier}

KNOWLEDGE BASE:
{loaded book summaries + shared docs}

{agent-specific context}

COMMUNICATION GUIDELINES:
- Be precise and actionable
- Cite sources from knowledge base
- Flag consultation needs: "CONSULT: [Agent] - [Question]"
- Flag risks immediately
- Use structured output formats
```

### Workflow Execution Pattern
- Accept initial context dictionary
- Execute steps sequentially
- Pass results between agents
- Handle agent consultation requests (CONSULT: syntax)
- Return structured results with status, steps, decisions, warnings
- Log all steps with timestamps
- Implement retry logic for API failures (3 retries with exponential backoff)
- Graceful degradation if agents fail

### Error Handling Standards
- Use try/except blocks for API calls
- Log errors with full context
- Return structured error responses
- Never expose API keys in logs
- Include timestamps in all logs
- Provide helpful error messages

## Ticker Discovery System

The system includes an automated ticker discovery and management module:

**Components:**
- `tools/screener.py`: Quantitative screening engine (momentum, value, quality, growth, technical)
- `tools/ticker_universe.py`: Ticker universe management (watchlist → active → removal lifecycle)
- `tools/strategy_matcher.py`: Dynamic strategy assignment for tickers
- `tools/regime_detector.py`: Market regime detection and screening adjustments
- `monitoring/ticker_performance.py`: Performance tracking and auto-removal
- `orchestration/discovery_workflow.py`: Multi-agent discovery workflows
- `cli.py`: Command-line interface for ticker management

**Discovery Workflows:**
1. **Daily Discovery**: Automated screening with agent evaluation
2. **Weekly Review**: Performance-based ticker removal/promotion
3. **Regime-Aware Screening**: Adjusts criteria based on market conditions

**Universe Management:**
- Core Universe: High-conviction tickers (max 50)
- Satellite Universe: Broader opportunity set (max 100)
- Tactical Universe: Short-term trades (max 50)
- Watchlist: Candidates under evaluation (max 100)

## Key Files to Review

- **TECH_DOC.md**: Complete implementation guide with detailed specifications
- **TICKER_DISCOVER.md**: Ticker discovery and management system specification
- **knowledge/shared/multi-country-bot-trading.md**: Existing trading documentation
- **config/agents_config.yaml**: All agent configurations
- **.env**: Environment configuration (create from .env.example)
