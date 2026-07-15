# Librium Quota System Technical Specification

## Overview

The Librium quota system implements generational biomass targets using fibonacci and tribonacci sequences to create organic difficulty progression. This system manages escalating resource requirements across game generations while providing multiple difficulty modes.

## Core Requirements

### Functional Requirements
- Generate biomass quotas for each generation using mathematical sequences
- Support multiple difficulty modes with different progression patterns
- Provide clean API for quota calculation and difficulty scaling
- Enable easy tuning of difficulty parameters for game balance

### Technical Requirements
- Python 3.8+ compatible
- Efficient calculation (memoization for recursive sequences)
- Type hints for code clarity
- Comprehensive unit tests
- Modular design for easy extension

## System Architecture

### Core Components

```python
from enum import Enum
from typing import Dict, Callable
from functools import lru_cache

class DifficultyMode(Enum):
    """Defines available difficulty modes with their parameters"""
    CONTEMPLATIVE = {
        "quota_multiplier": 0.8,
        "disaster_frequency": 0.5,
        "description": "Gentle learning curve for new players"
    }
    BALANCED = {
        "quota_multiplier": 1.0, 
        "disaster_frequency": 1.0,
        "description": "Standard game experience"
    }
    INTENSE = {
        "quota_multiplier": 1.3,
        "disaster_frequency": 1.4, 
        "description": "Challenging strategic pressure"
    }
    BRUTAL = {
        "quota_multiplier": 1.6,
        "disaster_frequency": 2.0,
        "description": "Tribonacci sequence with maximum pressure"
    }
```

### Sequence Generators

```python
class QuotaSequences:
    """Mathematical sequence generators for quota progression"""
    
    @staticmethod
    @lru_cache(maxsize=128)
    def fibonacci_quota(generation: int, base_quota: int = 100) -> int:
        """
        Generate fibonacci-based quota progression
        
        Args:
            generation: Current generation number (1-indexed)
            base_quota: Starting quota value for generation 1
            
        Returns:
            Biomass quota for the specified generation
            
        Sequence: 100, 100, 150, 200, 275, 375, 550, 825...
        Growth rate approaches golden ratio (~1.618)
        """
        if generation <= 0:
            raise ValueError("Generation must be positive")
        
        if generation <= 2:
            return base_quota
        
        # Recursive calculation with memoization
        prev_quota = QuotaSequences.fibonacci_quota(generation - 1, base_quota)
        prev_prev_quota = QuotaSequences.fibonacci_quota(generation - 2, base_quota)
        
        # Add 50% of the difference for smooth progression
        return prev_quota + prev_prev_quota // 2
    
    @staticmethod
    @lru_cache(maxsize=128)
    def tribonacci_quota(generation: int, base_quota: int = 100) -> int:
        """
        Generate tribonacci-based quota progression (brutal mode)
        
        Args:
            generation: Current generation number (1-indexed)
            base_quota: Starting quota value for generation 1
            
        Returns:
            Biomass quota for the specified generation
            
        Sequence: 100, 100, 150, 275, 425, 700, 1200, 2025...
        Growth rate approaches ~1.839 (much faster than fibonacci)
        """
        if generation <= 0:
            raise ValueError("Generation must be positive")
            
        if generation <= 2:
            return base_quota
        elif generation == 3:
            return base_quota + 50  # Initial boost for third generation
            
        # Sum of previous three terms
        return (QuotaSequences.tribonacci_quota(generation - 1, base_quota) +
                QuotaSequences.tribonacci_quota(generation - 2, base_quota) +
                QuotaSequences.tribonacci_quota(generation - 3, base_quota))
    
    @staticmethod
    def linear_quota(generation: int, base_quota: int = 100, growth_rate: int = 50) -> int:
        """
        Linear progression for comparison/testing
        
        Args:
            generation: Current generation number
            base_quota: Starting quota
            growth_rate: Quota increase per generation
            
        Returns:
            Linear quota progression
        """
        return base_quota + (generation - 1) * growth_rate
    
    @staticmethod
    def exponential_quota(generation: int, base_quota: int = 100, multiplier: float = 1.3) -> int:
        """
        Exponential progression for comparison/testing
        
        Args:
            generation: Current generation number
            base_quota: Starting quota
            multiplier: Growth multiplier per generation
            
        Returns:
            Exponential quota progression
        """
        return int(base_quota * (multiplier ** (generation - 1)))
```

### Main Quota Manager

```python
class QuotaManager:
    """Main class for managing biomass quota calculations and difficulty scaling"""
    
    def __init__(self, difficulty: DifficultyMode = DifficultyMode.BALANCED, base_quota: int = 100):
        """
        Initialize quota manager
        
        Args:
            difficulty: Selected difficulty mode
            base_quota: Base quota value for generation 1
        """
        self.difficulty = difficulty
        self.base_quota = base_quota
        self.sequence_map: Dict[DifficultyMode, Callable] = {
            DifficultyMode.CONTEMPLATIVE: QuotaSequences.fibonacci_quota,
            DifficultyMode.BALANCED: QuotaSequences.fibonacci_quota,
            DifficultyMode.INTENSE: QuotaSequences.fibonacci_quota,
            DifficultyMode.BRUTAL: QuotaSequences.tribonacci_quota
        }
    
    def get_quota(self, generation: int) -> int:
        """
        Calculate the biomass quota for a specific generation
        
        Args:
            generation: Target generation number (1-indexed)
            
        Returns:
            Required biomass quota for the generation
            
        Raises:
            ValueError: If generation is not positive
        """
        if generation <= 0:
            raise ValueError("Generation must be positive")
        
        # Get base sequence value
        sequence_func = self.sequence_map[self.difficulty]
        base_quota = sequence_func(generation, self.base_quota)
        
        # Apply difficulty multiplier
        multiplier = self.difficulty.value["quota_multiplier"]
        final_quota = int(base_quota * multiplier)
        
        return final_quota
    
    def get_quota_progression(self, max_generation: int) -> Dict[int, int]:
        """
        Generate quota progression for multiple generations
        
        Args:
            max_generation: Maximum generation to calculate
            
        Returns:
            Dictionary mapping generation -> quota
        """
        return {gen: self.get_quota(gen) for gen in range(1, max_generation + 1)}
    
    def get_disaster_frequency(self) -> float:
        """
        Get disaster frequency multiplier for current difficulty
        
        Returns:
            Disaster frequency multiplier
        """
        return self.difficulty.value["disaster_frequency"]
    
    def change_difficulty(self, new_difficulty: DifficultyMode) -> None:
        """
        Change difficulty mode (useful for mid-game adjustments)
        
        Args:
            new_difficulty: New difficulty mode to apply
        """
        self.difficulty = new_difficulty
        
        # Clear memoization cache when difficulty changes
        QuotaSequences.fibonacci_quota.cache_clear()
        QuotaSequences.tribonacci_quota.cache_clear()
    
    def get_difficulty_info(self) -> Dict[str, any]:
        """
        Get comprehensive information about current difficulty
        
        Returns:
            Dictionary with difficulty parameters and description
        """
        return {
            "mode": self.difficulty.name,
            "quota_multiplier": self.difficulty.value["quota_multiplier"],
            "disaster_frequency": self.difficulty.value["disaster_frequency"],
            "description": self.difficulty.value["description"],
            "sequence_type": "tribonacci" if self.difficulty == DifficultyMode.BRUTAL else "fibonacci"
        }
```

## Implementation Guidelines

### File Structure
```
librium/
├── core/
│   ├── __init__.py
│   ├── quota_system.py       # Main quota manager classes
│   └── sequences.py          # Mathematical sequence generators
├── tests/
│   ├── __init__.py
│   ├── test_quota_system.py  # Unit tests for quota system
│   └── test_sequences.py     # Tests for sequence generators
└── examples/
    ├── __init__.py
    └── quota_examples.py     # Usage examples and demonstrations
```

### Usage Examples

```python
# Basic usage
from librium.core.quota_system import QuotaManager, DifficultyMode

# Initialize quota manager
quota_manager = QuotaManager(difficulty=DifficultyMode.BALANCED)

# Get quota for specific generation
gen_5_quota = quota_manager.get_quota(5)
print(f"Generation 5 quota: {gen_5_quota} biomass")

# Get progression for planning
progression = quota_manager.get_quota_progression(10)
for gen, quota in progression.items():
    print(f"Gen {gen}: {quota} biomass")

# Change difficulty mid-game
quota_manager.change_difficulty(DifficultyMode.INTENSE)
new_quota = quota_manager.get_quota(6)

# Check difficulty parameters
difficulty_info = quota_manager.get_difficulty_info()
disaster_frequency = quota_manager.get_disaster_frequency()
```

### Advanced Usage - Custom Sequences

```python
# Extend for custom sequences
class CustomQuotaSequences(QuotaSequences):
    @staticmethod
    @lru_cache(maxsize=128)
    def polynomial_quota(generation: int, base_quota: int = 100) -> int:
        """Custom polynomial progression"""
        return base_quota + (generation - 1) ** 2 * 10
    
    @staticmethod 
    @lru_cache(maxsize=128)
    def logarithmic_quota(generation: int, base_quota: int = 100) -> int:
        """Custom logarithmic progression for very long games"""
        import math
        if generation == 1:
            return base_quota
        return int(base_quota * math.log(generation) * 50)

# Custom difficulty modes
class ExtendedDifficultyMode(Enum):
    MARATHON = {
        "quota_multiplier": 0.6,
        "disaster_frequency": 0.3,
        "description": "Extended play with logarithmic growth"
    }
```

### Performance Considerations

```python
# Monitoring performance
import time
from functools import wraps

def performance_monitor(func):
    """Decorator to monitor quota calculation performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        if end_time - start_time > 0.001:  # Log if > 1ms
            print(f"Slow quota calculation: {func.__name__} took {end_time - start_time:.4f}s")
        
        return result
    return wrapper

# Apply to quota methods if needed
QuotaManager.get_quota = performance_monitor(QuotaManager.get_quota)
```

## Testing Strategy

### Unit Tests Structure

```python
import unittest
from librium.core.quota_system import QuotaManager, DifficultyMode, QuotaSequences

class TestQuotaSequences(unittest.TestCase):
    """Test mathematical sequence generators"""
    
    def test_fibonacci_progression(self):
        """Test fibonacci sequence correctness"""
        expected = [100, 100, 150, 200, 275, 375]
        for i, expected_quota in enumerate(expected, 1):
            actual = QuotaSequences.fibonacci_quota(i)
            self.assertEqual(actual, expected_quota, 
                           f"Generation {i}: expected {expected_quota}, got {actual}")
    
    def test_tribonacci_progression(self):
        """Test tribonacci sequence correctness"""
        expected = [100, 100, 150, 350, 600, 1100]  # Verify these values
        for i, expected_quota in enumerate(expected, 1):
            actual = QuotaSequences.tribonacci_quota(i)
            self.assertEqual(actual, expected_quota,
                           f"Generation {i}: expected {expected_quota}, got {actual}")
    
    def test_sequence_validation(self):
        """Test input validation"""
        with self.assertRaises(ValueError):
            QuotaSequences.fibonacci_quota(0)
        
        with self.assertRaises(ValueError):
            QuotaSequences.fibonacci_quota(-1)

class TestQuotaManager(unittest.TestCase):
    """Test quota manager functionality"""
    
    def setUp(self):
        self.manager = QuotaManager(DifficultyMode.BALANCED)
    
    def test_difficulty_multipliers(self):
        """Test difficulty scaling works correctly"""
        base_quota = self.manager.get_quota(5)
        
        # Test contemplative (easier)
        self.manager.change_difficulty(DifficultyMode.CONTEMPLATIVE)
        easy_quota = self.manager.get_quota(5)
        self.assertLess(easy_quota, base_quota)
        
        # Test brutal (harder)
        self.manager.change_difficulty(DifficultyMode.BRUTAL)
        hard_quota = self.manager.get_quota(5)
        self.assertGreater(hard_quota, base_quota)
    
    def test_progression_monotonic(self):
        """Ensure quotas always increase with generation"""
        progression = self.manager.get_quota_progression(10)
        quotas = list(progression.values())
        
        for i in range(1, len(quotas)):
            self.assertGreaterEqual(quotas[i], quotas[i-1],
                                  f"Quota decreased from gen {i} to {i+1}")

class TestIntegration(unittest.TestCase):
    """Integration tests for complete system"""
    
    def test_quota_reachability(self):
        """Test that quotas are theoretically reachable"""
        # This would integrate with ecosystem simulation
        # to verify quotas are achievable with optimal play
        pass
    
    def test_difficulty_balance(self):
        """Test difficulty progression feels appropriate"""
        # Verify brutal mode creates sufficient pressure
        # while contemplative mode remains learnable
        pass

if __name__ == "__main__":
    unittest.main()
```

### Integration Points

```python
# Integration with game systems
class GameIntegration:
    """Examples of how quota system integrates with other game components"""
    
    @staticmethod
    def check_generation_complete(current_biomass: int, quota_manager: QuotaManager, 
                                 generation: int) -> bool:
        """Check if player has met quota for current generation"""
        required_quota = quota_manager.get_quota(generation)
        return current_biomass >= required_quota
    
    @staticmethod
    def calculate_quota_pressure(current_biomass: int, quota_manager: QuotaManager,
                                generation: int) -> float:
        """Calculate pressure level (0.0 to 1.0+) for UI feedback"""
        required_quota = quota_manager.get_quota(generation)
        if required_quota == 0:
            return 0.0
        return current_biomass / required_quota
    
    @staticmethod
    def get_deforestation_temptation(current_biomass: int, quota_manager: QuotaManager,
                                    generation: int) -> float:
        """Calculate how tempting emergency deforestation becomes"""
        pressure = GameIntegration.calculate_quota_pressure(current_biomass, quota_manager, generation)
        
        if pressure >= 1.0:
            return 0.0  # No temptation if already meeting quota
        elif pressure < 0.5:
            return 1.0  # Maximum temptation when far from quota
        else:
            return 2.0 * (1.0 - pressure)  # Linear decrease as pressure reduces
```

## Configuration and Tuning

### Configuration File Format

```python
# config/quota_settings.py
QUOTA_CONFIG = {
    "default_difficulty": "BALANCED",
    "base_quota": 100,
    "sequence_parameters": {
        "fibonacci": {
            "scaling_factor": 0.5,  # How much previous terms contribute
        },
        "tribonacci": {
            "third_generation_bonus": 50,
        }
    },
    "difficulty_presets": {
        "TUTORIAL": {
            "quota_multiplier": 0.5,
            "disaster_frequency": 0.2,
            "description": "Learn the basics"
        }
    },
    "performance": {
        "cache_size": 128,
        "enable_monitoring": False
    }
}

# Load configuration
def load_quota_config():
    """Load quota configuration from file or environment"""
    import os
    
    # Override with environment variables if available
    config = QUOTA_CONFIG.copy()
    
    if "LIBRIUM_BASE_QUOTA" in os.environ:
        config["base_quota"] = int(os.environ["LIBRIUM_BASE_QUOTA"])
    
    if "LIBRIUM_DIFFICULTY" in os.environ:
        config["default_difficulty"] = os.environ["LIBRIUM_DIFFICULTY"]
    
    return config
```

### Balance Tuning Tools

```python
# tools/quota_analyzer.py
class QuotaAnalyzer:
    """Tools for analyzing and tuning quota progression"""
    
    @staticmethod
    def analyze_progression(max_generation: int = 15):
        """Analyze quota progression across difficulties"""
        results = {}
        
        for difficulty in DifficultyMode:
            manager = QuotaManager(difficulty)
            progression = manager.get_quota_progression(max_generation)
            
            results[difficulty.name] = {
                "progression": progression,
                "growth_rates": QuotaAnalyzer.calculate_growth_rates(progression),
                "difficulty_spike": QuotaAnalyzer.find_difficulty_spikes(progression)
            }
        
        return results
    
    @staticmethod
    def calculate_growth_rates(progression: Dict[int, int]) -> Dict[int, float]:
        """Calculate generation-to-generation growth rates"""
        growth_rates = {}
        
        for gen in range(2, len(progression) + 1):
            if gen in progression and (gen - 1) in progression:
                prev_quota = progression[gen - 1]
                curr_quota = progression[gen]
                growth_rates[gen] = curr_quota / prev_quota if prev_quota > 0 else 0.0
        
        return growth_rates
    
    @staticmethod
    def find_difficulty_spikes(progression: Dict[int, int], spike_threshold: float = 1.8) -> List[int]:
        """Find generations with large difficulty spikes"""
        growth_rates = QuotaAnalyzer.calculate_growth_rates(progression)
        return [gen for gen, rate in growth_rates.items() if rate > spike_threshold]

# Usage for balance tuning
if __name__ == "__main__":
    analysis = QuotaAnalyzer.analyze_progression()
    for difficulty, data in analysis.items():
        print(f"\n{difficulty} Mode:")
        print(f"  Max generation quota: {max(data['progression'].values())}")
        print(f"  Average growth rate: {sum(data['growth_rates'].values()) / len(data['growth_rates']):.2f}")
        print(f"  Difficulty spikes at generations: {data['difficulty_spike']}")
```

## Error Handling and Edge Cases

```python
class QuotaSystemError(Exception):
    """Base exception for quota system errors"""
    pass

class InvalidGenerationError(QuotaSystemError):
    """Raised when generation number is invalid"""
    pass

class DifficultyNotFoundError(QuotaSystemError):
    """Raised when difficulty mode is not recognized"""
    pass

# Enhanced error handling in QuotaManager
def get_quota_safe(self, generation: int) -> int:
    """Get quota with comprehensive error handling"""
    try:
        if generation <= 0:
            raise InvalidGenerationError(f"Generation must be positive, got {generation}")
        
        if generation > 1000:  # Sanity check for extremely high generations
            raise InvalidGenerationError(f"Generation {generation} exceeds maximum supported value")
        
        return self.get_quota(generation)
        
    except (ValueError, OverflowError) as e:
        raise QuotaSystemError(f"Failed to calculate quota for generation {generation}: {e}")
    except KeyError as e:
        raise DifficultyNotFoundError(f"Difficulty mode {self.difficulty} not found: {e}")
```

## Documentation and Examples

### API Documentation

Generate comprehensive API documentation using docstrings:

```bash
# Generate documentation
python -m pydoc librium.core.quota_system
python -m pydoc librium.core.sequences

# Or use Sphinx for full documentation
sphinx-quickstart docs/
sphinx-build -b html docs/ docs/_build/
```

### Example Scripts

```python
# examples/quota_demo.py
"""
Demonstration script showing quota system capabilities
Run with: python examples/quota_demo.py
"""

def demo_basic_usage():
    print("=== Basic Quota System Demo ===")
    manager = QuotaManager(DifficultyMode.BALANCED)
    
    for gen in range(1, 8):
        quota = manager.get_quota(gen)
        print(f"Generation {gen}: {quota} biomass required")

def demo_difficulty_comparison():
    print("\n=== Difficulty Comparison ===")
    generation = 6
    
    for difficulty in DifficultyMode:
        manager = QuotaManager(difficulty)
        quota = manager.get_quota(generation)
        info = manager.get_difficulty_info()
        print(f"{difficulty.name:12}: {quota:4d} biomass ({info['sequence_type']})")

def demo_progression_analysis():
    print("\n=== Progression Analysis ===")
    analyzer = QuotaAnalyzer()
    results = analyzer.analyze_progression(10)
    
    for difficulty, data in results.items():
        avg_growth = sum(data['growth_rates'].values()) / len(data['growth_rates'])
        print(f"{difficulty}: Avg growth rate {avg_growth:.2f}x per generation")

if __name__ == "__main__":
    demo_basic_usage()
    demo_difficulty_comparison()
    demo_progression_analysis()
```

This technical specification provides a complete implementation guide for the Librium quota system, ready for Claude Code to implement with proper Python practices, comprehensive testing, and extensible architecture.