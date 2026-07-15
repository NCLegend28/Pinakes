# Librium Calamity System - Claude Code Implementation Brief

## 🎯 Project Overview

Implement the complete Calamity & Difficulty Progression System for Librium, an ecosystem management roguelike game. This system creates escalating environmental disasters that threaten ecosystem survival, with progressive difficulty curves and mitigation mechanics.

---

## 📋 Implementation Scope

### Core Deliverables
- **Calamity System Manager** - Main controller for disaster timing and progression
- **5 Calamity Types** - Complete implementations with unique mechanics
- **Mitigation System** - Perfect balance tracking and ecosystem protection
- **Difficulty Scaling** - Logarithmic progression across 4 difficulty modes
- **Save/Load System** - Complete state persistence
- **Integration Layer** - Clean API for game engine integration
- **Testing Framework** - Validation and balance testing tools

### Technical Requirements
- **Language:** Python 3.8+
- **Architecture:** Modular, extensible design
- **Performance:** <1ms calamity calculations per generation
- **Integration:** Compatible with existing EcoBalance engine
- **Testing:** Unit tests, integration tests, balance validation

---

## 🏗️ System Architecture

### Module Structure
```
librium_calamity_system/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── calamity_manager.py      # Main system controller
│   ├── difficulty_modes.py      # Difficulty configuration
│   ├── mitigation_system.py     # Balance tracking and mitigation
│   └── data_structures.py       # Core data classes
├── calamities/
│   ├── __init__.py
│   ├── base_calamity.py         # Abstract base class
│   ├── mass_extinction.py       # Population elimination
│   ├── ecosystem_collapse.py    # Carrying capacity reduction
│   ├── climate_shift.py         # Terrain productivity changes
│   ├── ecological_disease.py    # Targeted trophic level attacks
│   └── habitat_fragmentation.py # Connectivity disruption
├── integration/
│   ├── __init__.py
│   ├── game_interface.py        # Main integration API
│   ├── save_manager.py          # State persistence
│   └── event_logger.py          # Event tracking and metrics
├── utils/
│   ├── __init__.py
│   ├── performance.py           # Optimization utilities
│   ├── validation.py            # Balance testing tools
│   └── config.py                # System configuration
└── tests/
    ├── __init__.py
    ├── test_calamity_manager.py
    ├── test_calamities.py
    ├── test_mitigation.py
    ├── test_integration.py
    └── test_balance_validation.py
```

---

## 🎮 Core System Specifications

### Difficulty Progression Formula
```python
# Quota scaling (Fibonacci-based)
def calculate_quota(generation: int, difficulty_multiplier: float) -> int:
    base = fibonacci_quota(generation, base=100)
    return int(base * difficulty_multiplier)

# Balance threshold escalation
def get_balance_threshold(generation: int, difficulty_modifier: float) -> float:
    base_threshold = 75.0 * difficulty_modifier
    max_threshold = 98.0 * difficulty_modifier
    progress = min(generation / 20.0, 1.0)
    return base_threshold + (max_threshold - base_threshold) * (progress ** 0.7)

# Disaster countdown acceleration
def calculate_disaster_countdown(generation: int, frequency_multiplier: float) -> int:
    base_countdown = 10
    reduction = int(2 * math.log(generation + 1))
    countdown = max(base_countdown - reduction, 3)
    countdown = int(countdown / frequency_multiplier)
    return max(countdown, 2) + random.randint(-1, 1)
```

### Difficulty Mode Configuration
```python
DIFFICULTY_SETTINGS = {
    "CONTEMPLATIVE": {
        "quota_multiplier": 0.8,
        "disaster_frequency_multiplier": 0.7,
        "consolation_energium": 1,
        "diversity_threshold": 6.0,
        "balance_threshold_modifier": 0.9
    },
    "BALANCED": {
        "quota_multiplier": 1.0,
        "disaster_frequency_multiplier": 1.0,
        "consolation_energium": 1,
        "diversity_threshold": 8.0,
        "balance_threshold_modifier": 1.0
    },
    "INTENSE": {
        "quota_multiplier": 1.3,
        "disaster_frequency_multiplier": 1.4,
        "consolation_energium": 0,
        "diversity_threshold": 10.0,
        "balance_threshold_modifier": 1.1
    },
    "BRUTAL": {
        "quota_multiplier": 1.6,
        "disaster_frequency_multiplier": 2.0,
        "consolation_energium": 0,
        "diversity_threshold": 12.0,
        "balance_threshold_modifier": 1.2
    }
}
```

---

## ⚡ Calamity Types Implementation

### 1. Mass Extinction Event
**Target:** All populations across ecosystem
**Base Effect:** 40% population elimination (severity-scaled)
**Vulnerability Factors:**
- Small population sizes (≤2 individuals) = 50% more vulnerable
- Isolated populations = 20% more vulnerable
- Critical/stressed populations = 40% more vulnerable

**Implementation Requirements:**
- Population size-based vulnerability calculation
- Cascade effect analysis (food web disruption)
- Recovery recommendation generation

### 2. Ecosystem Collapse
**Target:** Terrain carrying capacity
**Base Effect:** 30% carrying capacity reduction (permanent)
**Vulnerability Factors:**
- Mountain terrain = 20% more vulnerable
- Grassland terrain = 10% more vulnerable
- High capacity utilization (>85%) = 30% more vulnerable

**Implementation Requirements:**
- Terrain-specific vulnerability mapping
- Overcrowding cascade calculations
- Permanent capacity modification

### 3. Climate Shift Event
**Target:** Terrain productivity and weather resistance
**Base Effect:** 25% productivity loss + 20% weather vulnerability increase (permanent)
**Vulnerability Factors:**
- Wetland terrain = 30% more sensitive
- Mountain terrain = 20% more sensitive
- Desert terrain = 30% more resistant

**Implementation Requirements:**
- Climate sensitivity by terrain type
- Weather resistance modification
- Seasonal pattern disruption

### 4. Ecological Disease Outbreak
**Target:** Specific trophic levels or population types
**Base Effect:** 60% infection rate, 50% mortality for infected
**Disease Types:**
- **Herbivore Plague:** Targets primary consumers when herbivore:carnivore ratio > 3:1
- **Overcrowding Disease:** Targets dense populations (>90% capacity)
- **Genetic Bottleneck Syndrome:** Targets isolated populations (<2 individuals)
- **Generalist Pathogen:** Affects all trophic levels equally

**Implementation Requirements:**
- Adaptive disease type selection
- Spread simulation with adjacency rules
- Resistance evolution mechanics

### 5. Habitat Fragmentation Crisis
**Target:** Ecosystem connectivity and migration patterns
**Base Effect:** 35% fragmentation intensity creating movement barriers (permanent)
**Effects:**
- Genetic diversity loss in isolated clusters
- Resource access limitation
- Migration pattern disruption

**Implementation Requirements:**
- Strategic barrier placement algorithm
- Connected component analysis for isolation
- Migration route disruption calculation

---

## 🛡️ Mitigation System

### Perfect Balance Streak Requirements
```python
def get_required_streak(generation: int) -> int:
    base_streak = 2
    max_streak = 6  # Tunable parameter
    scaling_rate = 0.3
    progress = min(generation / 15.0, 1.0)
    return int(base_streak + (max_streak - base_streak) * (progress ** scaling_rate))
```

### Mitigation Effects
- **Full Mitigation:** 50% severity reduction + 3 disaster delay + 5 bonus energium
- **Partial Mitigation:** 20% severity reduction + 1 disaster delay + 2 bonus energium

### Ecosystem Stability Calculation
```python
def calculate_ecosystem_stability(ecosystem_state: dict) -> float:
    stability = 100.0
    
    # Penalties
    stability -= population_stress_penalty(ecosystem_state)  # Max -30
    stability -= overcrowding_penalty(ecosystem_state)      # Max -25
    stability -= food_web_gaps_penalty(ecosystem_state)     # Max -45 (15 per missing level)
    
    # Bonuses
    stability += biodiversity_bonus(ecosystem_state)        # Max +20
    
    return max(0, min(100, stability))
```

---

## 🔧 Integration API

### Main Interface
```python
class CalamitySystemInterface:
    def __init__(self, difficulty: DifficultyMode, ecosystem_manager):
        # Initialize system components
    
    def process_generation_end(self, ecosystem_state: dict) -> dict:
        # Main entry point for generation processing
        # Returns: disaster info, calamity results, mitigation status
    
    def get_calamity_preview(self, ecosystem_state: dict) -> dict:
        # Preview upcoming calamity and vulnerability analysis
    
    def get_mitigation_status(self) -> dict:
        # Current mitigation eligibility and requirements
    
    def save_state(self) -> dict:
        # Serialize complete system state
    
    def load_state(self, save_data: dict, ecosystem_manager):
        # Restore system from saved state
```

### Expected Integration Points
```python
# Game engine integration example
calamity_system = CalamitySystemInterface(DifficultyMode.BALANCED, ecosystem_manager)

# Each generation end
result = calamity_system.process_generation_end(ecosystem_state)

if result['calamity_triggered']:
    calamity_result = result['calamity_result']
    # Apply effects to ecosystem:
    # - Remove populations (mass extinction)
    # - Reduce carrying capacity (ecosystem collapse)
    # - Modify terrain productivity (climate shift)
    # - etc.

if result['mitigation_achieved']:
    # Award bonus energium and display achievement
```

---

## 📊 Data Structures

### Core Data Classes
```python
@dataclass
class CalamityResult:
    event_type: CalamityType
    severity: float
    affected_populations: List[Dict]
    affected_hexes: List[Dict]
    permanent_effects: List[Dict]
    cascade_effects: List[Dict]
    mitigation_applied: float
    description: str
    recovery_recommendations: List[str]

@dataclass
class EcosystemState:
    hexes: List[Dict]           # Terrain data with capacity, adjacency
    populations: List[Dict]     # Species data with size, state, location
    generation: int
    # Additional ecosystem metrics

@dataclass
class MitigationState:
    perfect_balance_streak: int
    balance_threshold_met: bool
    shop_upgrades: Dict[str, bool]
    research_unlocks: Dict[str, bool]
    ecosystem_factors: Dict[str, float]
```

---

## 🧪 Testing Requirements

### Unit Tests
- **Calamity Manager:** Generation processing, countdown calculation, state tracking
- **Each Calamity Type:** Effect calculation, vulnerability assessment, cascade analysis
- **Mitigation System:** Balance calculation, streak tracking, eligibility determination
- **Difficulty Scaling:** Threshold calculation, quota progression, timing adjustments

### Integration Tests
- **Full System Flow:** Complete generation processing with all components
- **Save/Load Functionality:** State persistence and restoration
- **API Interface:** External integration points and error handling

### Balance Validation Tests
- **Difficulty Progression:** Validate appropriate challenge scaling
- **Mitigation Frequency:** Ensure 10-20% achievable mitigation rate
- **Calamity Distribution:** Verify diverse calamity selection over time
- **Performance Benchmarks:** <1ms generation processing, <10ms save/load

### Test Data Requirements
- **Mock Ecosystem States:** Various sizes, compositions, and stress levels
- **Edge Cases:** Empty ecosystems, single-hex systems, extreme populations
- **Progression Scenarios:** 20-generation test runs for each difficulty

---

## 🎯 Implementation Priorities

### Phase 1: Core Foundation
1. **Data structures and enums** (`data_structures.py`)
2. **Difficulty configuration** (`difficulty_modes.py`)
3. **Base calamity class** (`base_calamity.py`)
4. **Calamity manager core** (`calamity_manager.py`)

### Phase 2: Calamity Implementations
1. **Mass Extinction** (simplest - direct population effects)
2. **Ecosystem Collapse** (moderate - terrain modifications)
3. **Climate Shift** (complex - permanent productivity changes)
4. **Ecological Disease** (complex - spread simulation)
5. **Habitat Fragmentation** (most complex - connectivity analysis)

### Phase 3: Integration & Polish
1. **Mitigation system** (`mitigation_system.py`)
2. **Save/load functionality** (`save_manager.py`)
3. **Main API interface** (`game_interface.py`)
4. **Event logging and metrics** (`event_logger.py`)

### Phase 4: Testing & Validation
1. **Unit test suite** (all components)
2. **Integration tests** (full system flows)
3. **Balance validation** (progression curves and mitigation rates)
4. **Performance optimization** (caching and efficiency)

---

## 🔧 Configuration Parameters

### Tunable Constants
```python
class CalamitySystemConfig:
    # Progression scaling
    QUOTA_BASE = 100
    BALANCE_THRESHOLD_BASE = 75.0
    BALANCE_THRESHOLD_MAX = 98.0
    
    # Disaster timing
    DISASTER_COUNTDOWN_BASE = 10
    DISASTER_COUNTDOWN_MIN = 2
    
    # Mitigation requirements
    PERFECT_STREAK_BASE = 2
    PERFECT_STREAK_MAX = 6        # TUNABLE - subject to playtesting
    
    # Calamity base effects
    MASS_EXTINCTION_BASE_RATE = 0.4
    ECOSYSTEM_COLLAPSE_BASE_RATE = 0.3
    CLIMATE_SHIFT_BASE_PENALTY = 0.25
    DISEASE_INFECTION_BASE_RATE = 0.6
    FRAGMENTATION_BASE_INTENSITY = 0.35
    
    # Performance settings
    CACHE_SIZE_LIMIT = 1000
    CALCULATION_TIMEOUT_MS = 100
```

---

## 🚀 Success Criteria

### Functional Requirements
✅ **Complete System Integration:** Seamless integration with existing EcoBalance engine  
✅ **Difficulty Scaling:** Clear progression from Contemplative to Brutal modes  
✅ **Calamity Variety:** All 5 calamity types implemented with unique mechanics  
✅ **Mitigation Mechanics:** Perfect balance streak system with meaningful rewards  
✅ **State Persistence:** Full save/load functionality with no data loss  

### Performance Requirements
✅ **Response Time:** <1ms calamity calculations per generation  
✅ **Memory Usage:** <50MB total system memory footprint  
✅ **Save/Load Speed:** <10ms for complete state operations  

### Balance Requirements
✅ **Mitigation Rate:** 10-20% achievable mitigation rate for skilled players  
✅ **Calamity Survival:** 5-15% of players survive 3+ calamities  
✅ **Progression Feel:** Smooth difficulty curve without frustrating spikes  

### Code Quality Requirements
✅ **Test Coverage:** >90% unit test coverage  
✅ **Documentation:** Complete docstrings and type hints  
✅ **Modularity:** Clean separation of concerns and extensible design  
✅ **Error Handling:** Graceful failure with meaningful error messages  

---

## 📖 Additional Resources

### Reference Documents
- **EcoBalance Engine Technical Report:** Core ecosystem simulation mechanics
- **Librium Cardporium:** Complete card catalog with synergy systems
- **Calamity Types Specification:** Detailed mechanics for each calamity type

### Design Principles
- **Emergent Complexity:** Simple rules creating complex strategic decisions
- **Risk vs Reward:** Tension between optimization and resilience
- **Player Agency:** Meaningful choices with clear consequences
- **Progressive Mastery:** Escalating challenges requiring deeper understanding

---

**Ready for Claude Code Implementation!** 🚀

This brief provides complete specifications for implementing the Librium Calamity System. All design decisions are finalized, parameters are specified, and integration points are clearly defined. The system is architecturally sound and ready for professional implementation.