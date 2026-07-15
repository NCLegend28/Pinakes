# Librium Calamity & Difficulty Progression System
## Technical Specification v1.0

---

## 🎯 Executive Summary

The Calamity System introduces escalating environmental disasters that threaten ecosystem survival, coupled with a progressive difficulty curve that demands increasing mastery. Players face mounting pressure through accelerating disaster frequency, stricter balance requirements, and exponentially growing quotas, while offering rare mitigation opportunities through perfect ecosystem management.

---

## 📊 Core Difficulty Progression

### Quota Scaling System
**Base Formula:** Fibonacci sequence with difficulty multipliers
```python
def fibonacci_quota(generation: int, base: int = 100) -> int:
    """Natural growth pattern matching ecological principles"""
    if generation <= 2:
        return base
    return fibonacci_quota(generation - 1) + fibonacci_quota(generation - 2) // 2

def get_quota_with_difficulty(generation: int, difficulty: DifficultyMode) -> int:
    base_quota = fibonacci_quota(generation)
    multiplier = difficulty.quota_multiplier  # 0.8 to 1.6 range
    return int(base_quota * multiplier)
```

**Quota Progression Examples:**
- Generation 1: 100 biomass (all difficulties baseline)
- Generation 5: ~400 biomass (Contemplative) to ~640 biomass (Brutal)
- Generation 10: ~1,200 biomass (Contemplative) to ~1,920 biomass (Brutal)
- Generation 15: ~3,600 biomass (Contemplative) to ~5,760 biomass (Brutal)

### Difficulty Mode Configuration
```python
@dataclass
class DifficultyMode:
    quota_multiplier: float
    disaster_frequency_multiplier: float
    consolation_energium: int
    diversity_threshold: float

DIFFICULTY_SETTINGS = {
    "CONTEMPLATIVE": DifficultyMode(0.8, 0.7, 1, 6.0),
    "BALANCED": DifficultyMode(1.0, 1.0, 1, 8.0),
    "INTENSE": DifficultyMode(1.3, 1.4, 0, 10.0),
    "BRUTAL": DifficultyMode(1.6, 2.0, 0, 12.0)
}
```

---

## ⚡ Disaster & Calamity Framework

### Disaster Countdown Acceleration
**Core Principle:** Logarithmic reduction in disaster intervals with randomization
```python
def calculate_disaster_countdown(generation: int, difficulty: DifficultyMode) -> int:
    """Accelerating disaster pattern with difficulty scaling"""
    import random, math
    
    base_countdown = 10
    # Logarithmic reduction gets more aggressive over time
    reduction = int(2 * math.log(generation + 1))
    countdown = max(base_countdown - reduction, 3)  # Minimum 3 disasters
    
    # Apply difficulty multiplier
    countdown = int(countdown / difficulty.disaster_frequency_multiplier)
    countdown = max(countdown, 2)  # Absolute minimum
    
    # Randomization to prevent predictability
    variance = max(1, countdown // 3)
    return random.randint(countdown - variance, countdown + variance)
```

**Disaster Countdown Examples:**
| Generation | Base Pattern | Contemplative | Balanced | Intense | Brutal |
|------------|--------------|---------------|----------|---------|--------|
| 1-3        | 8-12        | 11-17        | 8-12     | 6-9     | 4-6    |
| 4-6        | 6-8         | 9-11         | 6-8      | 4-6     | 3-4    |
| 7-10       | 4-6         | 6-9          | 4-6      | 3-4     | 2-3    |
| 11+        | 3-5         | 4-7          | 3-5      | 2-3     | 2      |

### Calamity Trigger System
```python
class CalamityTracker:
    def __init__(self, difficulty: DifficultyMode):
        self.disaster_count = 0
        self.disasters_until_calamity = calculate_disaster_countdown(1, difficulty)
        self.calamity_count = 0
        
    def process_disaster(self, generation: int, difficulty: DifficultyMode):
        self.disaster_count += 1
        
        if self.disaster_count >= self.disasters_until_calamity:
            self.trigger_calamity(generation)
            self.reset_countdown(generation, difficulty)
    
    def trigger_calamity(self, generation: int):
        self.calamity_count += 1
        severity = 1.0 + (self.calamity_count * 0.2)  # Each calamity 20% worse
        return CalamityEvent(generation, severity)
```

---

## 🔄 Ecosystem Balance & Mitigation System

### Balance Requirement Escalation
**Core Principle:** Exponentially stricter balance requirements over time
```python
def get_balance_threshold(generation: int) -> float:
    """Balance requirements become exponentially stricter"""
    base_threshold = 75.0    # Starting point (achievable with basic synergies)
    max_threshold = 98.0     # Near-perfect endgame requirement
    
    # Logarithmic scaling - accelerates early, levels off late
    progress = min(generation / 20.0, 1.0)  # Scale over 20 generations
    threshold = base_threshold + (max_threshold - base_threshold) * (progress ** 0.7)
    
    return min(threshold, max_threshold)
```

**Balance Threshold Progression:**
- Generation 1: 75% (manageable with basic understanding)
- Generation 5: 87% (requires shop upgrades and planning)
- Generation 10: 93% (demands ecosystem mastery)
- Generation 15: 96% (near-perfect optimization required)
- Generation 20+: 98% (only true masters achieve consistently)

### Perfect Balance Streak Tracking
```python
class EcosystemStabilityTracker:
    def __init__(self):
        self.perfect_balance_streak = 0
        self.generation_stability_history = []
        
    def track_generation(self, generation: int, ecosystem_stability: float):
        required_threshold = get_balance_threshold(generation)
        self.generation_stability_history.append({
            'generation': generation,
            'stability': ecosystem_stability,
            'threshold': required_threshold,
            'perfect': ecosystem_stability >= required_threshold
        })
        
        if ecosystem_stability >= required_threshold:
            self.perfect_balance_streak += 1
        else:
            self.perfect_balance_streak = 0
            
    def get_required_streak(self, generation: int) -> int:
        """Required consecutive perfect generations for mitigation"""
        base_streak = 2
        max_streak = 6  # Subject to change based on playtesting
        scaling_rate = 0.3
        
        progress = min(generation / 15.0, 1.0)
        required = base_streak + (max_streak - base_streak) * (progress ** scaling_rate)
        return int(required)
```

---

## 🛡️ Calamity Mitigation Mechanics

### Mitigation Calculation System
```python
def calculate_calamity_mitigation(stability_tracker: EcosystemStabilityTracker, 
                                generation: int) -> dict:
    """Calculate calamity mitigation effects based on perfect balance streak"""
    current_streak = stability_tracker.perfect_balance_streak
    required_streak = stability_tracker.get_required_streak(generation)
    
    if current_streak >= required_streak:
        # Full mitigation - rare but powerful
        return {
            "delay_calamity": 3,        # Push back disaster countdown by 3
            "reduce_severity": 0.5,     # Halve calamity damage
            "bonus_energium": 5,        # Substantial reward
            "mitigation_type": "FULL"
        }
    elif current_streak >= (required_streak - 1):
        # Partial mitigation - close but not perfect
        return {
            "delay_calamity": 1,
            "reduce_severity": 0.8,     # 20% damage reduction
            "bonus_energium": 2,
            "mitigation_type": "PARTIAL"
        }
    
    return {"mitigation_type": "NONE"}
```

### Mitigation Effects Implementation
```python
class CalamityEvent:
    def __init__(self, generation: int, base_severity: float = 1.0):
        self.generation = generation
        self.base_severity = base_severity
        self.actual_severity = base_severity  # Modified by mitigation
        
    def apply_mitigation(self, mitigation_effects: dict):
        if mitigation_effects.get("reduce_severity"):
            self.actual_severity *= mitigation_effects["reduce_severity"]
            
    def mass_extinction_event(self) -> dict:
        """Remove percentage of all populations"""
        extinction_rate = 0.4 * self.actual_severity  # 40% base rate
        return {
            "event_type": "MASS_EXTINCTION",
            "extinction_rate": extinction_rate,
            "description": f"Catastrophic event eliminates {extinction_rate:.1%} of all populations"
        }
        
    def ecosystem_collapse_event(self) -> dict:
        """Reduce carrying capacity across all terrain"""
        capacity_reduction = 0.3 * self.actual_severity  # 30% base reduction
        return {
            "event_type": "ECOSYSTEM_COLLAPSE", 
            "capacity_reduction": capacity_reduction,
            "description": f"Environmental degradation reduces carrying capacity by {capacity_reduction:.1%}"
        }
        
    def climate_shift_event(self) -> dict:
        """Permanently alter terrain effectiveness"""
        terrain_penalty = 0.25 * self.actual_severity  # 25% base penalty
        return {
            "event_type": "CLIMATE_SHIFT",
            "terrain_penalty": terrain_penalty,
            "description": f"Climate change reduces terrain productivity by {terrain_penalty:.1%}"
        }
```

---

## 🎮 Game Phase Architecture

### Phase-Based Progression System
```python
@dataclass
class GamePhase:
    name: str
    generation_range: tuple
    balance_threshold_range: tuple
    disaster_frequency_range: tuple
    strategic_focus: str
    
GAME_PHASES = {
    "LEARNING": GamePhase(
        name="Learning Phase",
        generation_range=(1, 5),
        balance_threshold_range=(75, 85),
        disaster_frequency_range=(8, 12),
        strategic_focus="Experimentation and basic synergy discovery"
    ),
    "MASTERY": GamePhase(
        name="Mastery Phase", 
        generation_range=(6, 12),
        balance_threshold_range=(85, 93),
        disaster_frequency_range=(4, 8),
        strategic_focus="Shop optimization and advanced ecosystem design"
    ),
    "PERFECTION": GamePhase(
        name="Perfection Phase",
        generation_range=(13, float('inf')),
        balance_threshold_range=(93, 98),
        disaster_frequency_range=(2, 5),
        strategic_focus="Near-perfect play and calamity survival"
    )
}
```

### Victory Condition Framework
```python
class VictoryConditions:
    def __init__(self, mode: str = "SURVIVAL"):
        self.mode = mode  # "SURVIVAL", "ENDLESS", "CALAMITY_COUNT"
        
    def check_survival_victory(self, calamities_survived: int) -> bool:
        """Win by surviving X calamities"""
        target_calamities = 5  # Configurable based on difficulty
        return calamities_survived >= target_calamities
        
    def check_endless_score(self, total_energium: int, generations: int) -> dict:
        """Endless mode high score calculation"""
        return {
            "total_energium": total_energium,
            "generations_survived": generations,
            "efficiency_score": total_energium / generations,
            "final_score": total_energium * math.log(generations)
        }
```

---

## ⚙️ Technical Implementation Details

### Performance Considerations
```python
class CalamitySystemManager:
    def __init__(self, difficulty: DifficultyMode):
        self.difficulty = difficulty
        self.stability_tracker = EcosystemStabilityTracker()
        self.calamity_tracker = CalamityTracker(difficulty)
        
        # Performance optimization
        self._cached_thresholds = {}  # Cache balance thresholds
        self._cached_countdowns = {}  # Cache disaster countdowns
        
    def process_generation_end(self, generation: int, ecosystem_state: EcosystemState):
        """Main entry point for end-of-generation processing"""
        # Calculate ecosystem stability
        stability = self._calculate_ecosystem_stability(ecosystem_state)
        
        # Update tracking systems
        self.stability_tracker.track_generation(generation, stability)
        
        # Check for mitigation opportunities
        mitigation = calculate_calamity_mitigation(self.stability_tracker, generation)
        
        # Process disaster countdown
        if mitigation.get("delay_calamity", 0) > 0:
            self.calamity_tracker.delay_countdown(mitigation["delay_calamity"])
            
        return {
            "stability": stability,
            "mitigation": mitigation,
            "next_disaster_countdown": self.calamity_tracker.disasters_until_calamity
        }
```

### Data Persistence Schema
```python
@dataclass
class CalamitySystemSaveData:
    """Serializable save data for calamity system state"""
    difficulty_mode: str
    current_generation: int
    disaster_count: int
    disasters_until_calamity: int
    calamity_count: int
    perfect_balance_streak: int
    stability_history: List[dict]
    mitigation_history: List[dict]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
        
    @classmethod
    def from_dict(cls, data: dict) -> 'CalamitySystemSaveData':
        """Reconstruct from saved dictionary"""
        return cls(**data)
```

### Integration Points
```python
class EcosystemIntegration:
    """Integration hooks with main ecosystem simulation"""
    
    @staticmethod
    def apply_calamity_effects(ecosystem_state: EcosystemState, 
                             calamity_event: CalamityEvent) -> EcosystemState:
        """Apply calamity effects to ecosystem state"""
        if calamity_event.event_type == "MASS_EXTINCTION":
            # Remove populations based on extinction rate
            return EcosystemIntegration._apply_mass_extinction(
                ecosystem_state, calamity_event.extinction_rate
            )
        elif calamity_event.event_type == "ECOSYSTEM_COLLAPSE":
            # Reduce carrying capacity
            return EcosystemIntegration._apply_capacity_reduction(
                ecosystem_state, calamity_event.capacity_reduction
            )
        elif calamity_event.event_type == "CLIMATE_SHIFT":
            # Modify terrain effectiveness
            return EcosystemIntegration._apply_climate_shift(
                ecosystem_state, calamity_event.terrain_penalty
            )
```

---

## 🧪 Testing & Validation Framework

### Balance Testing Scenarios
```python
class CalamityBalanceTests:
    """Test scenarios for validating calamity system balance"""
    
    def test_progression_curve(self):
        """Validate that difficulty scales appropriately"""
        for generation in range(1, 21):
            quota = fibonacci_quota(generation)
            threshold = get_balance_threshold(generation)
            
            # Ensure progression feels reasonable
            assert quota > 0, "Quota must be positive"
            assert 75 <= threshold <= 98, "Threshold must be in valid range"
            
    def test_mitigation_rarity(self):
        """Ensure perfect balance streaks are rare but achievable"""
        # Simulate 1000 games to check mitigation frequency
        mitigation_achieved = 0
        for simulation in range(1000):
            if self._simulate_perfect_balance_probability() > 0.05:
                mitigation_achieved += 1
        
        # Mitigation should occur in 5-15% of attempts
        assert 0.05 <= mitigation_achieved/1000 <= 0.15
```

### Performance Benchmarks
- **Calamity calculation:** < 1ms per generation
- **Stability tracking:** < 0.5ms per generation  
- **Mitigation evaluation:** < 0.1ms per generation
- **Save/load operations:** < 10ms for complete state

---

## 🔧 Configuration & Tuning Parameters

### Tunable Constants
```python
class CalamitySystemConfig:
    """Centralized configuration for easy balance tuning"""
    
    # Progression scaling
    QUOTA_BASE = 100
    BALANCE_THRESHOLD_BASE = 75.0
    BALANCE_THRESHOLD_MAX = 98.0
    BALANCE_THRESHOLD_SCALING = 0.7
    
    # Disaster timing
    DISASTER_COUNTDOWN_BASE = 10
    DISASTER_COUNTDOWN_MIN = 2
    DISASTER_RANDOMNESS_FACTOR = 0.3
    
    # Mitigation requirements
    PERFECT_STREAK_BASE = 2
    PERFECT_STREAK_MAX = 6  # SUBJECT TO CHANGE
    PERFECT_STREAK_SCALING = 0.3
    
    # Calamity severity
    CALAMITY_SEVERITY_ESCALATION = 0.2  # 20% worse each calamity
    MASS_EXTINCTION_BASE_RATE = 0.4     # 40% population loss
    CAPACITY_REDUCTION_BASE_RATE = 0.3  # 30% capacity loss
    CLIMATE_SHIFT_BASE_PENALTY = 0.25   # 25% terrain penalty
```

---

## 📈 Future Enhancement Opportunities

### Planned Features
- **Calamity Prediction System:** Advanced warning based on ecosystem stress indicators
- **Partial Mitigation Mechanics:** Graduated protection based on near-perfect balance
- **Calamity Type Selection:** Different calamity types based on ecosystem weaknesses
- **Recovery Mechanics:** Post-calamity ecosystem restoration opportunities

### Research Integration Points
- **Genetic Diversity Research:** Reduces calamity impact through species resilience
- **Climate Adaptation Research:** Provides climate shift calamity resistance
- **Advanced Monitoring:** Predictive calamity warning systems

---

## 🎯 Success Metrics

### Player Engagement Indicators
- **Progression Retention:** Players continue past generation 10
- **Mastery Achievement:** Players successfully achieve perfect balance streaks
- **Difficulty Scaling:** Appropriate challenge curve across all difficulty modes
- **Strategic Depth:** Multiple viable approaches to calamity survival

### Balance Validation Targets
- **Mitigation Frequency:** 10-20% of experienced players achieve regular mitigation
- **Calamity Survival:** 5-15% of players survive 3+ calamities
- **Difficulty Differentiation:** Clear progression path from Contemplative to Brutal
- **Phase Transition:** Natural progression through Learning → Mastery → Perfection phases

---

*This technical specification provides the foundation for implementing a challenging yet fair calamity system that rewards ecosystem mastery while maintaining engaging difficulty progression throughout the game's lifecycle.*

**Version:** 1.0  
**Last Updated:** September 2025  
**Status:** Ready for Implementation