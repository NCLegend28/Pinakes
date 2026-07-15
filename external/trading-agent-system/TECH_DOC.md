# Technical Documentation: Multi-Agent Trading System

**Project:** Trading Agent System with Anthropic Claude  
**Version:** 1.0.0  
**Date:** October 6, 2025  
**Purpose:** Complete implementation guide for Claude Code

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Implementation Checklist](#3-implementation-checklist)
4. [Agent Specifications](#4-agent-specifications)
5. [Core Components](#5-core-components)
6. [Configuration System](#6-configuration-system)
7. [Workflows](#7-workflows)
8. [Testing Strategy](#8-testing-strategy)
9. [Deployment](#9-deployment)

---

## 1. Project Overview

### 1.1 System Purpose
A multi-agent AI system for operating a cross-border algorithmic trading business. Each agent is specialized through 5 curated books and collaborates via predefined workflows.

### 1.2 Technology Stack
- **Language:** Python 3.11+
- **AI SDK:** Anthropic Python SDK
- **Model:** Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
- **Config:** YAML
- **Storage:** JSON Lines (JSONL) for logs
- **Structure:** Modular, class-based architecture

### 1.3 Key Design Principles
- **Separation of Concerns:** Each agent has distinct responsibilities
- **Composability:** Agents work independently and collaboratively
- **Auditability:** All decisions logged with timestamps and rationale
- **Extensibility:** Easy to add new agents or workflows
- **Testability:** Each component independently testable

---

## 2. Architecture

### 2.1 System Layers

```
┌─────────────────────────────────────────────────┐
│         User Interface / API Gateway            │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│         Agent Coordinator & Router              │
│   - Query routing                               │
│   - Workflow orchestration                      │
│   - Multi-agent collaboration                   │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│              Agent Layer (12 Agents)            │
│                                                 │
│  Tier 1: Operations (5 agents)                  │
│  Tier 2: Specialists (5 agents)                 │
│  Tier 3: Council (2 agents)                     │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│            Knowledge Base Layer                 │
│  - Book summaries (60 files)                    │
│  - Shared documentation                         │
│  - Company policies                             │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│         Memory & Persistence Layer              │
│  - Conversation history                         │
│  - Decision logs                                │
│  - Performance metrics                          │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│              Tools & Utilities                  │
│  - Risk calculators                             │
│  - Data access                                  │
│  - Compliance checks                            │
└─────────────────────────────────────────────────┘
```

### 2.2 Data Flow

```
User Query → Router → Agent(s) → Claude API → Response → Parser → Logger → User
                ↓                                          ↑
         Knowledge Base                            Tools & Calculators
```

---

## 3. Implementation Checklist

### Phase 1: Foundation (Priority: CRITICAL)
- [ ] `agents/base_agent.py` - Base agent class with full functionality
- [ ] `config/agents_config.yaml` - Agent configuration definitions
- [ ] `knowledge/shared/multi-country-bot-trading.md` - Copy existing doc
- [ ] `.env` - Environment variables (ANTHROPIC_API_KEY)
- [ ] `requirements.txt` - Dependencies

### Phase 2: Agent Implementations (Priority: HIGH)
- [ ] All Tier 1 agent factory functions (5 files)
- [ ] All Tier 2 agent factory functions (5 files)
- [ ] All Tier 3 agent factory functions (2 files)
- [ ] Agent configuration loader

### Phase 3: Orchestration (Priority: HIGH)
- [ ] `orchestration/coordinator.py` - Main coordinator class
- [ ] `orchestration/workflows.py` - Workflow definitions
- [ ] `orchestration/router.py` - Query routing logic

### Phase 4: Tools & Utilities (Priority: MEDIUM)
- [ ] `tools/data_access.py` - Market data interface
- [ ] `tools/calculators.py` - Risk/position sizing calculators
- [ ] `tools/compliance.py` - Compliance checking utilities

### Phase 5: Memory & Logging (Priority: MEDIUM)
- [ ] Memory system for conversation persistence
- [ ] Decision logging with structured format
- [ ] Metrics tracking system

### Phase 6: Testing (Priority: MEDIUM)
- [ ] Unit tests for base agent
- [ ] Integration tests for workflows
- [ ] End-to-end test scenarios

### Phase 7: Documentation & Examples (Priority: LOW)
- [ ] `README.md` - Project documentation
- [ ] `examples/` - Usage examples
- [ ] API documentation

---

## 4. Agent Specifications

### 4.1 Agent Registry

| Agent Name | Tier | Primary Role | Book Count | Status |
|------------|------|--------------|------------|--------|
| Strategy Architect | 1 | Strategy design & validation | 5 | TODO |
| Risk Manager | 1 | Risk & position management | 5 | TODO |
| Infrastructure Engineer | 1 | System architecture | 5 | TODO |
| Execution Specialist | 1 | Order execution | 5 | TODO |
| Data Manager | 1 | Data pipelines | 5 | TODO |
| Compliance Counsel | 2 | Regulatory compliance | 5 | TODO |
| Tax Strategist | 2 | International tax | 5 | TODO |
| FX Specialist | 2 | Currency management | 5 | TODO |
| Regional Specialist | 2 | Market-specific rules | 5 | TODO |
| Psychology Coach | 2 | Trading psychology | 5 | TODO |
| Strategy Council | 3 | Strategic oversight | 5 | TODO |
| Quant Research Council | 3 | Advanced research | 5 | TODO |

### 4.2 Agent Configuration Schema

```yaml
# config/agents_config.yaml

agents:
  strategy_architect:
    name: "Strategy Architect"
    tier: 1
    role: "Design and validate trading strategies, backtest frameworks"
    books:
      - "algorithmic_trading_chan.md"
      - "advances_financial_ml_lopez.md"
      - "systematic_trading_carver.md"
      - "evidence_based_technical_aronson.md"
      - "evaluation_optimization_pardo.md"
    responsibilities:
      - "Strategy design validation"
      - "Backtest analysis review"
      - "Signal generation logic"
      - "Statistical validation of edges"
      - "Performance attribution analysis"
    handoffs:
      risk_validation: "Risk Manager"
      execution_analysis: "Execution Specialist"
      data_requirements: "Data Manager"
      compliance_check: "Compliance Counsel"
    decision_areas:
      - "Is this strategy statistically sound?"
      - "What are the edge decay risks?"
      - "How should we test this hypothesis?"
      - "What data do we need?"
      - "What are the overfitting risks?"
    
  risk_manager:
    name: "Risk Manager"
    tier: 1
    role: "All risk management, position sizing, portfolio construction"
    books:
      - "math_money_management_vince.md"
      - "quantitative_risk_mcneil.md"
      - "active_portfolio_grinold.md"
      - "risk_management_hull.md"
      - "kelly_criterion_maclean.md"
    responsibilities:
      - "Position sizing calculations"
      - "Portfolio risk limits"
      - "Drawdown management"
      - "Correlation analysis"
      - "VAR/CVaR monitoring"
    critical_rules:
      - "ALWAYS calculate Kelly fraction"
      - "NEVER exceed max drawdown limits"
      - "CHECK correlation before adding positions"
      - "MONITOR real-time VAR"
      - "FLAG concentration risks immediately"
    decision_areas:
      - "What is the optimal position size?"
      - "Are we within risk limits?"
      - "What is our portfolio correlation risk?"
      - "Should we reduce exposure?"
      - "What is our tail risk?"

  # ... (continue for all 12 agents)
```

---

## 5. Core Components

### 5.1 Base Agent Class

**File:** `agents/base_agent.py`

**Requirements:**
- Initialize with name, role, tier, book summaries
- Load knowledge base from markdown files
- Build comprehensive system prompt
- Handle conversation history
- Query Claude API with proper error handling
- Parse structured responses (JSON decisions)
- Extract consultation requests (CONSULT: syntax)
- Log all decisions to JSONL files
- Support context injection
- Temperature and max_tokens configuration

**Key Methods:**
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

**System Prompt Structure:**
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

DECISION FORMAT:
{JSON schema for structured decisions}
```

### 5.2 Agent Configuration Loader

**File:** `agents/config_loader.py`

**Purpose:** Load and validate agent configurations from YAML

```python
import yaml
from pathlib import Path
from typing import Dict, Any

class AgentConfigLoader:
    """Load agent configurations from YAML"""
    
    def __init__(self, config_path: str = "config/agents_config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load YAML configuration"""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_agent_config(self, agent_key: str) -> Dict[str, Any]:
        """Get configuration for specific agent"""
        return self.config['agents'].get(agent_key, {})
    
    def list_agents(self) -> List[str]:
        """List all configured agents"""
        return list(self.config['agents'].keys())
    
    def validate_config(self) -> bool:
        """Validate configuration structure"""
        required_fields = ['name', 'tier', 'role', 'books']
        for agent_key, agent_config in self.config['agents'].items():
            for field in required_fields:
                if field not in agent_config:
                    raise ValueError(f"Agent {agent_key} missing required field: {field}")
        return True
```

### 5.3 Agent Factory Pattern

**File:** `agents/tier1_operations/strategy_architect.py`

**Pattern:** Each agent has a factory function that uses config

```python
from agents.base_agent import TradingAgent
from agents.config_loader import AgentConfigLoader

def create_strategy_architect() -> TradingAgent:
    """Create the Chief Strategy Architect agent"""
    
    loader = AgentConfigLoader()
    config = loader.get_agent_config('strategy_architect')
    
    # Build system context from config
    system_context = f"""
SPECIFIC RESPONSIBILITIES:
{chr(10).join([f"{i+1}. {r}" for i, r in enumerate(config['responsibilities'])])}

KEY DECISION AREAS:
{chr(10).join([f"- {d}" for d in config['decision_areas']])}

HANDOFF PROTOCOLS:
{chr(10).join([f"- {k}: {v}" for k, v in config.get('handoffs', {}).items()])}
    """
    
    return TradingAgent(
        name=config['name'],
        role=config['role'],
        tier=config['tier'],
        book_summaries=config['books'],
        system_context=system_context
    )
```

**Implementation Task:** Create factory function for all 12 agents following this pattern.

### 5.4 Agent Coordinator

**File:** `orchestration/coordinator.py`

**Requirements:**
- Register all agents
- Route single queries to appropriate agent
- Execute multi-agent workflows
- Handle collaborative queries (multiple agents on same question)
- Maintain workflow history
- Error handling and recovery

**Key Methods:**
```python
class AgentCoordinator:
    def __init__(self)
    def register_agent(self, agent: TradingAgent)
    def route_query(self, query: str, context: Dict = None) -> Dict
    def execute_workflow(self, workflow_name: str, initial_context: Dict) -> Dict
    def collaborative_query(self, query: str, agent_names: List[str], context: Dict = None) -> Dict
    def _daily_operations_workflow(self, context: Dict) -> Dict
    def _new_strategy_workflow(self, context: Dict) -> Dict
    def _new_market_workflow(self, context: Dict) -> Dict
    def _risk_review_workflow(self, context: Dict) -> Dict
```

**Routing Logic:**
```python
def route_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Route query to most appropriate agent using keyword matching"""
    
    keywords = {
        "strategy": "Strategy Architect",
        "backtest": "Strategy Architect",
        "risk": "Risk Manager",
        "position": "Risk Manager",
        "infrastructure": "Infrastructure Engineer",
        "api": "Infrastructure Engineer",
        "execution": "Execution Specialist",
        "slippage": "Execution Specialist",
        "data": "Data Manager",
        "compliance": "Compliance Counsel",
        "regulatory": "Compliance Counsel",
        "tax": "Tax Strategist",
        "currency": "FX Specialist",
        "fx": "FX Specialist",
        "market rules": "Regional Specialist",
        "psychology": "Psychology Coach",
        "macro": "Strategy Council",
        "research": "Quant Research Council"
    }
    
    query_lower = query.lower()
    for keyword, agent_name in keywords.items():
        if keyword in query_lower and agent_name in self.agents:
            return self.agents[agent_name].query(query, context)
    
    # Default to Strategy Architect
    return self.agents.get("Strategy Architect").query(query, context)
```

### 5.5 Workflow Definitions

**File:** `orchestration/workflows.py`

**Purpose:** Define reusable multi-agent workflows

**Workflow Schema:**
```python
@dataclass
class WorkflowStep:
    agent_name: str
    query_template: str
    context_keys: List[str]  # Which previous results to include
    required: bool = True
    
@dataclass
class Workflow:
    name: str
    description: str
    steps: List[WorkflowStep]
    initial_context_required: List[str]
```

**Example Workflows:**

1. **Daily Operations Workflow**
   - Data Manager → Validate data
   - Strategy Architect → Generate signals
   - Risk Manager → Validate positions
   - Execution Specialist → Create execution plan
   - Psychology Coach → Review decisions

2. **New Strategy Workflow**
   - Quant Research Council → Evaluate concept
   - Strategy Architect → Design implementation
   - Data Manager → Assess data availability
   - Risk Manager → Define risk parameters
   - Execution Specialist → Evaluate feasibility
   - Compliance Counsel → Regulatory review
   - Strategy Council → Final decision

3. **New Market Workflow**
   - Regional Specialist → Feasibility assessment
   - Compliance Counsel → Regulatory requirements
   - Tax Strategist → Tax implications
   - FX Specialist → Currency considerations
   - Infrastructure Engineer → Technical requirements
   - Strategy Council → Go/no-go decision

4. **Risk Review Workflow**
   - Data Manager → Current positions/exposures
   - Risk Manager → Risk metrics analysis
   - Strategy Architect → Performance attribution
   - Psychology Coach → Behavioral assessment
   - Strategy Council → Strategic adjustments

---

## 6. Configuration System

### 6.1 Environment Variables

**File:** `.env`

```bash
# API Keys
ANTHROPIC_API_KEY=your_api_key_here

# Model Configuration
DEFAULT_MODEL=claude-sonnet-4-5-20250929
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=4096

# Paths
KNOWLEDGE_BASE_PATH=knowledge/
MEMORY_PATH=memory/
LOGS_PATH=memory/decisions/

# Agent Settings
MAX_CONVERSATION_HISTORY=20
ENABLE_DECISION_LOGGING=true
ENABLE_METRICS_TRACKING=true
```

### 6.2 Knowledge Base Structure

```
knowledge/
├── summaries/
│   ├── algorithmic_trading_chan.md
│   ├── advances_financial_ml_lopez.md
│   ├── systematic_trading_carver.md
│   ├── evidence_based_technical_aronson.md
│   ├── evaluation_optimization_pardo.md
│   ├── math_money_management_vince.md
│   ├── quantitative_risk_mcneil.md
│   ├── active_portfolio_grinold.md
│   ├── risk_management_hull.md
│   ├── kelly_criterion_maclean.md
│   ├── python_algo_trading_hilpisch.md
│   ├── designing_data_intensive_kleppmann.md
│   ├── site_reliability_google.md
│   ├── building_microservices_newman.md
│   ├── clean_architecture_martin.md
│   ├── trading_exchanges_harris.md
│   ├── algo_hft_trading_cartea.md
│   ├── empirical_microstructure_hasbrouck.md
│   ├── science_algo_trading_kissell.md
│   ├── algo_trading_dma_johnson.md
│   ├── python_data_analysis_mckinney.md
│   ├── financial_data_science_hilpisch.md
│   ├── time_series_databases_dunning.md
│   ├── database_design_hernandez.md
│   ├── (continue for all 60 books...)
│   └── ...
│
├── shared/
│   ├── multi-country-bot-trading.md (already exists)
│   ├── company-policies.md (to be created)
│   ├── best-practices.md (to be created)
│   └── regulatory-summary.md (to be created)
│
└── context/
    ├── strategy_notes.md
    ├── risk_limits.md
    └── infrastructure_standards.md
```

### 6.3 Book Summary Format

Each book summary should follow this template:

```markdown
# [Book Title] by [Author]

## Core Thesis
[2-3 paragraph summary of main argument]

## Key Concepts

### Concept 1: [Name]
[Explanation with examples]

### Concept 2: [Name]
[Explanation with examples]

## Practical Applications
1. [Application 1]
2. [Application 2]
3. [Application 3]

## Critical Insights
- [Insight 1]
- [Insight 2]
- [Insight 3]

## Relevant Quotes
> "[Important quote 1]"

> "[Important quote 2]"

## Connections to Trading
[How this book's concepts apply to algorithmic trading]

## Implementation Checklist
- [ ] [Actionable item 1]
- [ ] [Actionable item 2]
- [ ] [Actionable item 3]

## Further Reading
- [Related resource 1]
- [Related resource 2]
```

---

## 7. Workflows

### 7.1 Workflow Implementation Guide

Each workflow should:
1. Accept initial context dictionary
2. Execute steps sequentially
3. Pass results between agents
4. Handle agent consultation requests
5. Return structured results
6. Log all steps

### 7.2 Workflow Result Format

```python
{
    "workflow": "workflow_name",
    "status": "success|partial|failed",
    "steps": [
        {
            "step_number": 1,
            "agent": "Agent Name",
            "query": "Query sent to agent",
            "response": {...},
            "duration_ms": 1234,
            "timestamp": "ISO8601"
        },
        ...
    ],
    "final_decision": {...},
    "consultation_requests": [...],
    "warnings": [...],
    "errors": [...]
}
```

### 7.3 Error Handling

Each workflow should implement:
- Retry logic for API failures (3 retries with exponential backoff)
- Graceful degradation (continue with available agents if one fails)
- Clear error reporting
- Rollback procedures where applicable

---

## 8. Testing Strategy

### 8.1 Unit Tests

**File:** `tests/test_agents.py`

Test cases:
- Base agent initialization
- Knowledge base loading
- System prompt construction
- Query execution
- Response parsing
- Decision logging
- Conversation history management

**File:** `tests/test_coordinator.py`

Test cases:
- Agent registration
- Query routing
- Workflow execution
- Collaborative queries
- Error handling

### 8.2 Integration Tests

**File:** `tests/test_workflows.py`

Test complete workflows with mock agents:
- Daily operations workflow
- New strategy workflow
- New market workflow
- Risk review workflow

### 8.3 Test Data

Create test fixtures:
- Mock book summaries (shortened versions)
- Sample queries
- Expected responses
- Mock market data

---

## 9. Deployment

### 9.1 Setup Instructions

```bash
# 1. Clone repository
git clone [repo-url]
cd trading-agent-system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# 5. Create knowledge base
# Place book summaries in knowledge/summaries/
# Ensure multi-country-bot-trading.md is in knowledge/shared/

# 6. Initialize system
python main.py --init

# 7. Run tests
pytest tests/

# 8. Start system
python main.py
```

### 9.2 Directory Creation Script

```python
# setup.py
from pathlib import Path

def create_directory_structure():
    """Create all necessary directories"""
    
    directories = [
        "agents/tier1_operations",
        "agents/tier2_specialists",
        "agents/tier3_council",
        "knowledge/summaries",
        "knowledge/shared",
        "knowledge/context",
        "orchestration",
        "memory/conversations",
        "memory/decisions",
        "memory/metrics",
        "tools",
        "tests",
        "config",
        "examples"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py for Python packages
        if directory.startswith('agents') or directory == 'orchestration' or directory == 'tools':
            init_file = Path(directory) / "__init__.py"
            if not init_file.exists():
                init_file.touch()
    
    print("✓ Directory structure created")

if __name__ == "__main__":
    create_directory_structure()
```

---

## 10. Implementation Priority

### Week 1: Foundation
1. Set up project structure (`setup.py`)
2. Implement `base_agent.py` with full functionality
3. Create `config_loader.py`
4. Create `agents_config.yaml` with all 12 agent definitions
5. Test base agent with simple queries

### Week 2: Agent Layer
1. Implement all 12 agent factory functions
2. Create system context for each agent
3. Test each agent individually
4. Validate knowledge base loading

### Week 3: Orchestration
1. Implement `coordinator.py`
2. Implement `workflows.py`
3. Implement `router.py`
4. Test single-agent queries
5. Test multi-agent workflows

### Week 4: Tools & Enhancement
1. Implement `tools/calculators.py`
2. Implement `tools/data_access.py`
3. Implement `tools/compliance.py`
4. Add memory persistence
5. Add metrics tracking

### Week 5: Testing & Documentation
1. Write comprehensive tests
2. Create usage examples
3. Write README.md
4. Create API documentation
5. Performance optimization

---

## 11. Key Implementation Notes

### 11.1 For Base Agent (`agents/base_agent.py`)

**Critical features:**
- Load multiple markdown files and concatenate
- Handle missing files gracefully
- Construct comprehensive system prompts
- Parse JSON from code blocks in responses
- Extract "CONSULT:" directives
- Log to JSONL with proper structure
- Maintain conversation history with size limits
- Handle API errors with retries

### 11.2 For Agent Factories

**Pattern to follow:**
```python
def create_[agent_name]() -> TradingAgent:
    loader = AgentConfigLoader()
    config = loader.get_agent_config('[config_key]')
    
    system_context = f"""
SPECIFIC RESPONSIBILITIES:
{format_list(config['responsibilities'])}

KEY DECISION AREAS:
{format_list(config['decision_areas'])}

{format_critical_rules(config.get('critical_rules', []))}

HANDOFF PROTOCOLS:
{format_handoffs(config.get('handoffs', {}))}
    """
    
    return TradingAgent(
        name=config['name'],
        role=config['role'],
        tier=config['tier'],
        book_summaries=config['books'],
        system_context=system_context
    )
```

### 11.3 For Coordinator (`orchestration/coordinator.py`)

**Workflow execution pattern:**
```python
def _execute_workflow_step(
    self,
    agent_name: str,
    query: str,
    context: Dict
) -> Dict:
    """Execute single workflow step"""
    
    if agent_name not in self.agents:
        return {"error": f"Agent not found: {agent_name}"}
    
    start_time = time.time()
    
    try:
        result = self.agents[agent_name].query(query, context)
        duration_ms = int((time.time() - start_time) * 1000)
        
        return {
            "agent": agent_name,
            "query": query,
            "result": result,
            "duration_ms": duration_ms,
            "status": "success"
        }
    except Exception as e:
        return {
            "agent": agent_name,
            "query": query,
            "error": str(e),
            "status": "failed"
        }
```

### 11.4 Error Handling Standards

All components should:
- Use try/except blocks for API calls
- Log errors with full context
- Return structured error responses
- Never expose API keys in logs
- Provide helpful error messages
- Include timestamps in all logs

---

## 12. Quick Start Commands

```bash
# Initialize project
python setup.py

# Run single agent test
python -c "from agents.tier1_operations.strategy_architect import create_strategy_architect; agent = create_strategy_architect(); print(agent.query('What makes a good momentum strategy?'))"

# Run coordinator test
python main.py --test-routing

# Execute specific workflow
python main.py --workflow new_market --country Singapore

# Interactive mode
python main.py --interactive

# Run all tests
pytest tests/ -v

# Generate documentation
python -m pydoc -w agents orchestration tools
```

---

## 13. Troubleshooting Guide

### Common Issues:

**1. "Module not found" errors**
- Ensure all `__init__.py` files exist
- Check Python path includes project root
- Verify virtual environment is activated

**2. "File not found" for book summaries**
- Check file paths in `agents_config.yaml`
- Ensure files exist in `knowledge/summaries/`
- Verify file extensions (.md)

**3. API rate limits**
- Implement exponential backoff
- Add delays between workflow steps
- Monitor API usage

**4. Empty responses from agents**
- Check system prompt is loading correctly
- Verify knowledge base is not too large (stay under context limits)
- Check temperature settings

**5. Workflow failures**
- Check all agents are registered
- Verify context is passed correctly between steps
- Review agent logs for errors

---

## 14. Next Steps After Implementation

1. **Book Summary Generation**
   - Run your summarization program on all 60 books
   - Place summaries in `knowledge/summaries/`
   - Follow the template format

2. **Testing**
   - Test each agent individually
   - Test all workflows
   - Create integration test scenarios

3. **Optimization**
   - Monitor token usage
   - Optimize system prompts for clarity
   - Reduce unnecessary context

4. **Enhancement**
   - Add real market data connections
   - Implement actual risk calculators
   - Build compliance rule engine
   - Create web interface

5. **Production Readiness**
   - Add authentication
   - Implement rate limiting
   - Set up monitoring/alerting
   - Create backup/recovery procedures

---

## 15. Success Criteria

The system is ready when:
- [ ] All 12 agents initialize successfully
- [ ] Each agent can answer domain-specific questions
- [ ] All 4 workflows execute end-to-end
- [ ] Decisions are logged with full audit trail
- [ ] Agents correctly identify when to consult others
- [ ] Error handling works for all failure modes
- [ ] Tests pass with >80% coverage
- [ ] Documentation is complete and accurate

---

**END OF TECHNICAL DOCUMENTATION**

This document should provide Claude Code with everything needed to implement the complete multi-agent trading system. Each section includes enough detail for autonomous implementation while maintaining flexibility for intelligent decision-making.
