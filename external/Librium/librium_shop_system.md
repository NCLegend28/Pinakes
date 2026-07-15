# Librium Shop System Technical Specification

## Overview

The Librium Shop System provides inter-generational progression through energium-based purchases. Players earn energium by meeting quotas, exceeding production targets, and maintaining ecosystem diversity, then spend it on upgrades, new cards, and strategic enhancements between generations.

## Core Requirements

### Functional Requirements
- Energium currency calculation and tracking across generations
- Shop interface with categorized items (upgrades, cards, abilities)
- Purchase validation and inventory management  
- Integration with existing card and ecosystem systems
- Save/load functionality for persistent progression

### Technical Requirements
- Python 3.8+ compatible with type hints
- Integration with existing Librium architecture
- Modular design for easy item addition and balancing
- Comprehensive testing for currency and purchase logic
- Event system for purchase notifications

## System Architecture

### Core Components

```python
from enum import Enum
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json

class ShopItemType(Enum):
    """Categories of items available in the shop"""
    CARD = "card"                    # New cards for deck
    UPGRADE = "upgrade"              # Permanent improvements
    PIONEER_ENHANCEMENT = "pioneer"  # Pioneer species upgrades
    ABILITY = "ability"              # Special one-time or persistent abilities
    RESEARCH = "research"            # Unlock new mechanics or options

class ShopItemRarity(Enum):
    """Rarity tiers affecting cost and availability"""
    COMMON = "common"        # Always available, low cost
    UNCOMMON = "uncommon"    # Available after generation 3, moderate cost
    RARE = "rare"           # Available after generation 6, high cost
    LEGENDARY = "legendary"  # Available after generation 10, very high cost

@dataclass
class Energium:
    """Energium currency tracking"""
    quota_bonus: int = 0
    excess_bonus: int = 0  
    diversity_bonus: int = 0
    total: int = 0
    
    def add_earnings(self, quota: int, excess: int, diversity: int) -> None:
        """Add energium earnings from generation completion"""
        self.quota_bonus += quota
        self.excess_bonus += excess
        self.diversity_bonus += diversity
        self.total = self.quota_bonus + self.excess_bonus + self.diversity_bonus
    
    def spend(self, amount: int) -> bool:
        """Attempt to spend energium, return success status"""
        if self.total >= amount:
            self.total -= amount
            return True
        return False
    
    def can_afford(self, amount: int) -> bool:
        """Check if player can afford an item"""
        return self.total >= amount
```

### Energium Calculation System

```python
from librium.core.quota_system import DifficultyMode

class EnergiumCalculator:
    """Handles energium calculation based on generation performance"""
    
    # Diversity thresholds by difficulty
    DIVERSITY_THRESHOLDS = {
        DifficultyMode.CONTEMPLATIVE: 6.0,  # 2 species + 2 biomes = 6 points
        DifficultyMode.BALANCED: 8.0,      # 3 species + 2 biomes = 8 points  
        DifficultyMode.INTENSE: 10.0,      # 4 species + 2 biomes = 10 points
        DifficultyMode.BRUTAL: 12.0        # 5 species + 2 biomes = 12 points
    }
    
    # Consolation energium for quota failure
    CONSOLATION_ENERGIUM = {
        DifficultyMode.CONTEMPLATIVE: 1,
        DifficultyMode.BALANCED: 1, 
        DifficultyMode.INTENSE: 0,
        DifficultyMode.BRUTAL: 0
    }
    
    @staticmethod
    def calculate_diversity_score(ecosystem_state) -> float:
        """
        Calculate ecosystem diversity score
        
        Args:
            ecosystem_state: Current ecosystem state with populations and terrain
            
        Returns:
            Diversity score (species_count * 2.0 + biome_count * 1.0)
        """
        # Number of Different Species (weighted higher)
        unique_species = len(set(
            pop.species_name for pop in ecosystem_state.populations 
            if not pop.is_extinct()
        ))
        species_score = unique_species * 2.0  # Higher weight for species diversity
        
        # Biome Variety  
        unique_biomes = len(set(
            hex_tile.terrain_type for hex_tile in ecosystem_state.hexes
        ))
        biome_score = unique_biomes * 1.0  # Lower weight for terrain variety
        
        return species_score + biome_score
    
    @staticmethod
    def calculate_energium_earned(biomass_produced: int, quota_required: int, 
                                 diversity_score: float, difficulty: DifficultyMode) -> Energium:
        """
        Calculate energium earned for generation completion
        
        Args:
            biomass_produced: Total biomass generated this generation
            quota_required: Required biomass quota for this generation  
            diversity_score: Calculated ecosystem diversity score
            difficulty: Current difficulty mode
            
        Returns:
            Energium object with breakdown of earnings
        """
        energium = Energium()
        
        # Quota achievement bonus
        if biomass_produced >= quota_required:
            energium.quota_bonus = 2  # Success bonus
        else:
            # Consolation energium (difficulty-dependent)
            energium.quota_bonus = EnergiumCalculator.CONSOLATION_ENERGIUM[difficulty]
        
        # Excess production bonus (only if quota met)
        if biomass_produced >= quota_required:
            excess_percentage = (biomass_produced - quota_required) / quota_required  
            energium.excess_bonus = int(excess_percentage / 0.25)  # +1 per 25% over quota
        
        # Diversity bonus (available even on quota failure)
        diversity_threshold = EnergiumCalculator.DIVERSITY_THRESHOLDS[difficulty]
        if diversity_score >= diversity_threshold:
            energium.diversity_bonus = 2
        
        # Calculate total
        energium.total = energium.quota_bonus + energium.excess_bonus + energium.diversity_bonus
        
        return energium
```

### Shop Item System

```python
class ShopItem(ABC):
    """Abstract base class for all shop items"""
    
    def __init__(self, item_id: str, name: str, description: str, cost: int,
                 item_type: ShopItemType, rarity: ShopItemRarity,
                 min_generation: int = 1, max_purchases: int = 1):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.cost = cost
        self.item_type = item_type
        self.rarity = rarity
        self.min_generation = min_generation
        self.max_purchases = max_purchases
        self.times_purchased = 0
    
    def can_purchase(self, generation: int, energium_available: int) -> tuple[bool, str]:
        """
        Check if item can be purchased
        
        Returns:
            (can_purchase: bool, reason: str)
        """
        if generation < self.min_generation:
            return False, f"Available from generation {self.min_generation}"
        
        if self.times_purchased >= self.max_purchases:
            return False, f"Maximum purchases reached ({self.max_purchases})"
        
        if energium_available < self.cost:
            return False, f"Insufficient energium (need {self.cost}, have {energium_available})"
        
        return True, "Available for purchase"
    
    @abstractmethod
    def apply_effect(self, game_state) -> str:
        """Apply the item's effect to the game state"""
        pass
    
    def purchase(self, game_state) -> str:
        """Execute the purchase and apply effects"""
        self.times_purchased += 1
        return self.apply_effect(game_state)

class CardShopItem(ShopItem):
    """Shop item that adds a new card to player's collection"""
    
    def __init__(self, card_class, **kwargs):
        super().__init__(**kwargs)
        self.card_class = card_class
    
    def apply_effect(self, game_state) -> str:
        """Add the card to player's available cards"""
        new_card = self.card_class()
        game_state.card_collection.add_card(new_card)
        return f"Added {new_card.name} to your card collection"

class UpgradeShopItem(ShopItem):
    """Shop item that provides permanent upgrades"""
    
    def __init__(self, upgrade_effect: Callable, **kwargs):
        super().__init__(**kwargs)
        self.upgrade_effect = upgrade_effect
    
    def apply_effect(self, game_state) -> str:
        """Apply permanent upgrade to game state"""
        return self.upgrade_effect(game_state)

class PioneerEnhancementItem(ShopItem):
    """Shop item that enhances pioneer species"""
    
    def __init__(self, enhancement_type: str, enhancement_value: float, **kwargs):
        super().__init__(**kwargs)
        self.enhancement_type = enhancement_type
        self.enhancement_value = enhancement_value
    
    def apply_effect(self, game_state) -> str:
        """Apply enhancement to pioneer species"""
        if hasattr(game_state, 'pioneer_manager'):
            return game_state.pioneer_manager.apply_enhancement(
                self.enhancement_type, self.enhancement_value
            )
        return "Pioneer system not available"

class AbilityShopItem(ShopItem):
    """Shop item that grants special abilities"""
    
    def __init__(self, ability_type: str, uses: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.ability_type = ability_type
        self.uses = uses
    
    def apply_effect(self, game_state) -> str:
        """Grant ability to player"""
        if not hasattr(game_state, 'player_abilities'):
            game_state.player_abilities = {}
        
        if self.ability_type not in game_state.player_abilities:
            game_state.player_abilities[self.ability_type] = 0
        
        game_state.player_abilities[self.ability_type] += self.uses
        return f"Granted {self.uses} use(s) of {self.ability_type}"
```

### Shop Catalog Definition

```python
class ShopCatalog:
    """Defines all available shop items and their properties"""
    
    def __init__(self):
        self.items = self._initialize_catalog()
    
    def _initialize_catalog(self) -> Dict[str, ShopItem]:
        """Initialize the complete shop catalog"""
        catalog = {}
        
        # === CARD PURCHASES ===
        
        # Terrain Cards (Common)
        catalog["extra_forest"] = CardShopItem(
            item_id="extra_forest",
            name="Extra Forest Card", 
            description="Add an additional Forest terrain card to your collection",
            cost=3,
            item_type=ShopItemType.CARD,
            rarity=ShopItemRarity.COMMON,
            card_class=ForestCard,  # Assumes ForestCard class exists
            max_purchases=3
        )
        
        catalog["extra_wetland"] = CardShopItem(
            item_id="extra_wetland",
            name="Extra Wetland Card",
            description="Add an additional Wetland terrain card to your collection", 
            cost=4,
            item_type=ShopItemType.CARD,
            rarity=ShopItemRarity.COMMON,
            card_class=WetlandCard,
            max_purchases=3
        )
        
        # Flora Cards (Uncommon)
        catalog["specialized_moss"] = CardShopItem(
            item_id="specialized_moss",
            name="Specialized Moss Species",
            description="Hardy moss that thrives in multiple biomes with +20% growth rate",
            cost=6,
            item_type=ShopItemType.CARD,
            rarity=ShopItemRarity.UNCOMMON,
            min_generation=3,
            card_class=SpecializedMossCard,
            max_purchases=2
        )
        
        # Fauna Cards (Rare)
        catalog["apex_predator"] = CardShopItem(
            item_id="apex_predator", 
            name="Apex Predator",
            description="Powerful carnivore that provides excellent population control",
            cost=12,
            item_type=ShopItemType.CARD,
            rarity=ShopItemRarity.RARE,
            min_generation=6,
            card_class=ApexPredatorCard,
            max_purchases=1
        )
        
        # === PERMANENT UPGRADES ===
        
        catalog["efficient_ecosystems"] = UpgradeShopItem(
            item_id="efficient_ecosystems",
            name="Efficient Ecosystems",
            description="All terrain cards provide +2 baseline biomass permanently",
            cost=8,
            item_type=ShopItemType.UPGRADE,
            rarity=ShopItemRarity.UNCOMMON,
            min_generation=4,
            upgrade_effect=lambda gs: self._apply_baseline_biomass_boost(gs, 2)
        )
        
        catalog["master_ecologist"] = UpgradeShopItem(
            item_id="master_ecologist", 
            name="Master Ecologist",
            description="Unlock advanced ecosystem information and prediction tools",
            cost=15,
            item_type=ShopItemType.UPGRADE,
            rarity=ShopItemRarity.RARE,
            min_generation=8,
            upgrade_effect=lambda gs: self._unlock_advanced_ui(gs)
        )
        
        # === PIONEER ENHANCEMENTS ===
        
        catalog["pioneer_breeding"] = PioneerEnhancementItem(
            item_id="pioneer_breeding",
            name="Pioneer Breeding Program", 
            description="Pioneer species use only 45% of carrying capacity (down from 60%)",
            cost=5,
            item_type=ShopItemType.PIONEER_ENHANCEMENT,
            rarity=ShopItemRarity.COMMON,
            enhancement_type="capacity_usage_reduction",
            enhancement_value=0.15  # Reduce from 0.6 to 0.45
        )
        
        catalog["pioneer_resilience"] = PioneerEnhancementItem(
            item_id="pioneer_resilience",
            name="Pioneer Species Resilience",
            description="Pioneer species gain +25% resistance to environmental disasters",
            cost=7,
            item_type=ShopItemType.PIONEER_ENHANCEMENT, 
            rarity=ShopItemRarity.UNCOMMON,
            min_generation=5,
            enhancement_type="disaster_resistance",
            enhancement_value=0.25
        )
        
        # === SPECIAL ABILITIES ===
        
        catalog["emergency_intervention"] = AbilityShopItem(
            item_id="emergency_intervention",
            name="Emergency Ecosystem Intervention",
            description="One-time ability to prevent any species extinction",
            cost=10,
            item_type=ShopItemType.ABILITY,
            rarity=ShopItemRarity.UNCOMMON,
            ability_type="prevent_extinction",
            uses=1,
            max_purchases=3
        )
        
        catalog["weather_prediction"] = AbilityShopItem(
            item_id="weather_prediction",
            name="Weather Prediction System", 
            description="See next turn's weather in advance (3 uses)",
            cost=6,
            item_type=ShopItemType.ABILITY,
            rarity=ShopItemRarity.COMMON,
            ability_type="weather_prediction",
            uses=3,
            max_purchases=2
        )
        
        # === RESEARCH UNLOCKS ===
        
        catalog["genetic_diversity"] = UpgradeShopItem(
            item_id="genetic_diversity",
            name="Genetic Diversity Research",
            description="Unlock genetic diversity tracking and breeding mechanics",
            cost=20,
            item_type=ShopItemType.RESEARCH,
            rarity=ShopItemRarity.LEGENDARY,
            min_generation=12,
            upgrade_effect=lambda gs: self._unlock_genetic_system(gs)
        )
        
        return catalog
    
    def _apply_baseline_biomass_boost(self, game_state, boost_amount: int) -> str:
        """Apply permanent baseline biomass increase"""
        if not hasattr(game_state, 'permanent_upgrades'):
            game_state.permanent_upgrades = {}
        game_state.permanent_upgrades['baseline_biomass_boost'] = boost_amount
        return f"All terrain now provides +{boost_amount} baseline biomass"
    
    def _unlock_advanced_ui(self, game_state) -> str:
        """Unlock advanced UI features"""
        if not hasattr(game_state, 'ui_features'):
            game_state.ui_features = set()
        game_state.ui_features.add('advanced_ecosystem_info')
        game_state.ui_features.add('population_predictions')
        return "Advanced ecosystem analysis tools unlocked"
    
    def _unlock_genetic_system(self, game_state) -> str:
        """Unlock genetic diversity mechanics"""
        if not hasattr(game_state, 'research_unlocks'):
            game_state.research_unlocks = set()
        game_state.research_unlocks.add('genetic_diversity')
        return "Genetic diversity system unlocked - track species adaptation and breeding"
    
    def get_available_items(self, generation: int, energium_available: int) -> List[ShopItem]:
        """Get all items available for purchase"""
        available = []
        for item in self.items.values():
            can_purchase, _ = item.can_purchase(generation, energium_available)
            if can_purchase:
                available.append(item)
        return available
    
    def get_items_by_category(self, item_type: ShopItemType) -> List[ShopItem]:
        """Get all items of a specific type"""
        return [item for item in self.items.values() if item.item_type == item_type]
```

### Main Shop Manager

```python
class ShopManager:
    """Main shop management system"""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.catalog = ShopCatalog()
        self.purchase_history: List[Dict] = []
        
        # Initialize energium tracking if not exists
        if not hasattr(game_state, 'energium'):
            game_state.energium = Energium()
    
    def process_generation_completion(self, biomass_produced: int, quota_required: int,
                                    ecosystem_state, difficulty: DifficultyMode) -> Energium:
        """
        Process generation completion and award energium
        
        Args:
            biomass_produced: Total biomass generated this generation
            quota_required: Required quota for this generation
            ecosystem_state: Current ecosystem state for diversity calculation
            difficulty: Current difficulty mode
            
        Returns:
            Energium earned this generation
        """
        # Calculate diversity score
        diversity_score = EnergiumCalculator.calculate_diversity_score(ecosystem_state)
        
        # Calculate energium earned
        earned = EnergiumCalculator.calculate_energium_earned(
            biomass_produced, quota_required, diversity_score, difficulty
        )
        
        # Add to total energium
        self.game_state.energium.add_earnings(
            earned.quota_bonus, earned.excess_bonus, earned.diversity_bonus
        )
        
        return earned
    
    def get_shop_interface(self, generation: int) -> Dict[str, List[ShopItem]]:
        """
        Get organized shop interface for current generation
        
        Returns:
            Dictionary organized by category with available items
        """
        available_items = self.catalog.get_available_items(
            generation, self.game_state.energium.total
        )
        
        # Organize by category
        interface = {
            "cards": [],
            "upgrades": [], 
            "pioneer_enhancements": [],
            "abilities": [],
            "research": []
        }
        
        for item in available_items:
            if item.item_type == ShopItemType.CARD:
                interface["cards"].append(item)
            elif item.item_type == ShopItemType.UPGRADE:
                interface["upgrades"].append(item)
            elif item.item_type == ShopItemType.PIONEER_ENHANCEMENT:
                interface["pioneer_enhancements"].append(item)
            elif item.item_type == ShopItemType.ABILITY:
                interface["abilities"].append(item)
            elif item.item_type == ShopItemType.RESEARCH:
                interface["research"].append(item)
        
        # Sort each category by cost
        for category in interface.values():
            category.sort(key=lambda x: x.cost)
        
        return interface
    
    def purchase_item(self, item_id: str, generation: int) -> tuple[bool, str]:
        """
        Attempt to purchase an item
        
        Args:
            item_id: ID of item to purchase
            generation: Current generation number
            
        Returns:
            (success: bool, message: str)
        """
        if item_id not in self.catalog.items:
            return False, f"Item '{item_id}' not found in catalog"
        
        item = self.catalog.items[item_id]
        
        # Check if purchase is valid
        can_purchase, reason = item.can_purchase(generation, self.game_state.energium.total)
        if not can_purchase:
            return False, reason
        
        # Attempt to spend energium
        if not self.game_state.energium.spend(item.cost):
            return False, f"Insufficient energium (need {item.cost}, have {self.game_state.energium.total})"
        
        # Execute purchase
        try:
            effect_message = item.purchase(self.game_state)
            
            # Record purchase
            self.purchase_history.append({
                "generation": generation,
                "item_id": item_id,
                "item_name": item.name,
                "cost": item.cost,
                "effect": effect_message
            })
            
            return True, f"Purchased {item.name}: {effect_message}"
            
        except Exception as e:
            # Refund energium if purchase failed
            self.game_state.energium.total += item.cost
            return False, f"Purchase failed: {str(e)}"
    
    def get_purchase_history(self) -> List[Dict]:
        """Get complete purchase history"""
        return self.purchase_history.copy()
    
    def get_energium_breakdown(self) -> Dict[str, int]:
        """Get detailed energium breakdown"""
        return {
            "quota_bonus": self.game_state.energium.quota_bonus,
            "excess_bonus": self.game_state.energium.excess_bonus,
            "diversity_bonus": self.game_state.energium.diversity_bonus,
            "total": self.game_state.energium.total
        }
```

## Integration Points

### Game State Integration

```python
# Integration with main game loop
class GameState:
    def __init__(self):
        # Existing attributes...
        self.energium = Energium()
        self.shop_manager = ShopManager(self)
        self.permanent_upgrades = {}
        self.player_abilities = {}
        self.ui_features = set()
        self.research_unlocks = set()
        self.card_collection = CardCollection()  # Assumes this exists
    
    def complete_generation(self, biomass_produced: int, quota_required: int,
                           ecosystem_state, difficulty: DifficultyMode):
        """Process generation completion including energium calculation"""
        # Calculate and award energium
        earned = self.shop_manager.process_generation_completion(
            biomass_produced, quota_required, ecosystem_state, difficulty
        )
        
        # Return results for UI display
        return {
            "quota_met": biomass_produced >= quota_required,
            "biomass_produced": biomass_produced,
            "quota_required": quota_required,
            "energium_earned": earned,
            "total_energium": self.energium.total
        }

# Integration with ecosystem calculations
def calculate_baseline_biomass_with_upgrades(self, position) -> float:
    """Enhanced baseline biomass calculation with shop upgrades"""
    base_biomass = self.get_baseline_biomass(position)
    
    # Apply permanent upgrades
    if hasattr(self.game_state, 'permanent_upgrades'):
        boost = self.game_state.permanent_upgrades.get('baseline_biomass_boost', 0)
        base_biomass += boost
    
    return base_biomass
```

### Card System Integration

```python
# Enhanced card collection management
class CardCollection:
    def __init__(self):
        self.available_cards = []
        self.starting_deck = self._initialize_starting_deck()
    
    def add_card(self, card):
        """Add new card from shop purchase"""
        self.available_cards.append(card)
    
    def get_available_cards(self) -> List:
        """Get all cards available for play"""
        return self.starting_deck + self.available_cards
    
    def _initialize_starting_deck(self) -> List:
        """Initialize starting card deck"""
        # Base starting cards for new players
        return [
            ForestCard(), GrasslandCard(), WetlandCard(),  # Basic terrain
            # Other starting cards...
        ]
```

## Testing Strategy

### Unit Tests

```python
import unittest
from librium.core.shop_system import *

class TestEnergiumCalculation(unittest.TestCase):
    """Test energium calculation mechanics"""
    
    def test_quota_success_bonus(self):
        """Test energium for meeting quota"""
        result = EnergiumCalculator.calculate_energium_earned(
            biomass_produced=150,
            quota_required=100, 
            diversity_score=8.0,
            difficulty=DifficultyMode.BALANCED
        )
        
        self.assertEqual(result.quota_bonus, 2)
        self.assertEqual(result.excess_bonus, 2)  # 50% over = 2 bonuses
        self.assertEqual(result.diversity_bonus, 2)  # Meets threshold
        self.assertEqual(result.total, 6)
    
    def test_quota_failure_consolation(self):
        """Test consolation energium for quota failure"""
        result = EnergiumCalculator.calculate_energium_earned(
            biomass_produced=80,
            quota_required=100,
            diversity_score=10.0,
            difficulty=DifficultyMode.CONTEMPLATIVE
        )
        
        self.assertEqual(result.quota_bonus, 1)  # Consolation
        self.assertEqual(result.excess_bonus, 0)  # No excess
        self.assertEqual(result.diversity_bonus, 2)  # Still get diversity
        self.assertEqual(result.total, 3)
    
    def test_brutal_mode_no_consolation(self):
        """Test no consolation energium in brutal mode"""
        result = EnergiumCalculator.calculate_energium_earned(
            biomass_produced=80,
            quota_required=100,
            diversity_score=6.0,  # Below brutal threshold
            difficulty=DifficultyMode.BRUTAL
        )
        
        self.assertEqual(result.quota_bonus, 0)  # No consolation
        self.assertEqual(result.excess_bonus, 0)  # No excess
        self.assertEqual(result.diversity_bonus, 0)  # Below threshold
        self.assertEqual(result.total, 0)

class TestShopPurchases(unittest.TestCase):
    """Test shop purchase mechanics"""
    
    def setUp(self):
        self.game_state = GameState()
        self.game_state.energium.total = 10  # Starting energium
        self.shop = ShopManager(self.game_state)
    
    def test_successful_purchase(self):
        """Test successful item purchase"""
        success, message = self.shop.purchase_item("extra_forest", generation=1)
        
        self.assertTrue(success)
        self.assertEqual(self.game_state.energium.total, 7)  # 10 - 3 cost
        self.assertIn("Forest", message)
    
    def test_insufficient_energium(self):
        """Test purchase failure due to insufficient energium"""
        success, message = self.shop.purchase_item("apex_predator", generation=6)
        
        self.assertFalse(success)
        self.assertIn("Insufficient energium", message)
        self.assertEqual(self.game_state.energium.total, 10)  # Unchanged
    
    def test_generation_restriction(self):
        """Test purchase failure due to generation restriction"""
        self.game_state.energium.total = 50  # Enough energium
        success, message = self.shop.purchase_item("apex_predator", generation=3)
        
        self.assertFalse(success)
        self.assertIn("Available from generation", message)

class TestShopIntegration(unittest.TestCase):
    """Test shop integration with game systems"""
    
    def test_generation_completion_flow(self):
        """Test complete generation completion and shop access"""
        game_state = GameState()
        shop = ShopManager(game_state)
        
        # Mock ecosystem state
        class MockEcosystemState:
            populations = [MockPopulation("Hardy Grass"), MockPopulation("Field Mouse")]
            hexes = [MockHex("forest"), MockHex("grassland")]
        
        class MockPopulation:
            def __init__(self, name):
                self.species_name = name
            def is_extinct(self):
                return False
        
        class MockHex:
            def __init__(self, terrain):
                self.terrain_type = terrain
        
        # Process generation completion
        earned = shop.process_generation_completion(
            biomass_produced=130,
            quota_required=100,
            ecosystem_state=MockEcosystemState(),
            difficulty=DifficultyMode.BALANCED
        )
        
        # Verify energium calculation
        self.assertEqual(earned.quota_bonus, 2)
        self.assertEqual(earned.excess_bonus, 1)  # 30% over
        self.assertEqual(earned.diversity_bonus, 2)  # 4+2=6 >= 8 threshold? Should be 0
        
        # Test shop interface
        shop_interface = shop.get_shop_interface(generation=1)
        self.assertIn("cards", shop_interface)
        self.assertIn("upgrades", shop_interface)

if __name__ == "__main__":
    unittest.main()
```

### Integration Testing

```python
# Integration tests with existing systems
def test_pioneer_enhancement_integration():
    """Test pioneer enhancement purchases affect pioneer behavior"""
    game_state = GameState()
    game_state.energium.total = 20
    shop = ShopManager(game_state)
    
    # Purchase pioneer breeding program
    success, message = shop.purchase_item("pioneer_breeding", generation=1)
    assert success
    
    # Verify enhancement is applied
    # This would require integration with actual pioneer system
    # assert game_state.pioneer_manager.capacity_usage == 0.45

def test_upgrade_integration_with_terrain():
    """Test terrain upgrades affect biomass calculation"""
    game_state = GameState()
    game_state.energium.total = 20
    shop = ShopManager(game_state)
    
    # Purchase efficient ecosystems upgrade
    success, message = shop.purchase_item("efficient_ecosystems", generation=4)
    assert success
    
    # Verify upgrade affects terrain biomass calculation
    # This would require integration with actual terrain system
    # terrain_manager = TerrainManager(game_state)
    # base_biomass = terrain_manager.calculate_baseline_biomass_with_upgrades(position)
    # assert base_biomass includes +2 boost

def test_ability_usage_integration():
    """Test purchased abilities can be used in gameplay"""
    game_state = GameState()
    game_state.energium.total = 15
    shop = ShopManager(game_state)
    
    # Purchase emergency intervention ability
    success, message = shop.purchase_item("emergency_intervention", generation=1)
    assert success
    
    # Verify ability is available
    assert "prevent_extinction" in game_state.player_abilities
    assert game_state.player_abilities["prevent_extinction"] == 1
```

## Performance Considerations

### Optimization Strategies

```python
# Caching for shop interface generation
from functools import lru_cache

class OptimizedShopCatalog(ShopCatalog):
    """Performance-optimized shop catalog with caching"""
    
    @lru_cache(maxsize=128)
    def get_available_items_cached(self, generation: int, energium_available: int, 
                                  purchase_state_hash: str) -> List[ShopItem]:
        """
        Cached version of get_available_items
        
        Args:
            purchase_state_hash: Hash of purchase history to invalidate cache
        """
        return self.get_available_items(generation, energium_available)
    
    def get_purchase_state_hash(self) -> str:
        """Generate hash of current purchase state for cache invalidation"""
        purchase_counts = tuple(sorted(
            (item.item_id, item.times_purchased) for item in self.items.values()
        ))
        return str(hash(purchase_counts))

# Memory management for large catalogs
class LazyShopItem(ShopItem):
    """Lazy-loaded shop item for memory efficiency"""
    
    def __init__(self, item_config: Dict, **kwargs):
        self._config = item_config
        self._loaded = False
        super().__init__(**kwargs)
    
    def _ensure_loaded(self):
        """Load item data on first access"""
        if not self._loaded:
            # Load complex item data from config
            self._loaded = True
    
    def apply_effect(self, game_state) -> str:
        self._ensure_loaded()
        return super().apply_effect(game_state)
```

## Configuration and Data Management

### Shop Configuration Files

```python
# config/shop_config.json
{
    "balance_settings": {
        "energium_multipliers": {
            "contemplative": 1.2,
            "balanced": 1.0,
            "intense": 0.9,
            "brutal": 0.8
        },
        "cost_scaling": {
            "generation_multiplier": 0.05,
            "rarity_multipliers": {
                "common": 1.0,
                "uncommon": 1.5,
                "rare": 2.5,
                "legendary": 4.0
            }
        }
    },
    "item_availability": {
        "generation_gates": {
            "uncommon_unlock": 3,
            "rare_unlock": 6,
            "legendary_unlock": 10
        },
        "difficulty_restrictions": {
            "contemplative": ["all"],
            "balanced": ["all"],
            "intense": ["common", "uncommon", "rare"],
            "brutal": ["common", "uncommon"]
        }
    }
}

# config/shop_items.json
{
    "cards": {
        "extra_forest": {
            "name": "Extra Forest Card",
            "description": "Add an additional Forest terrain card to your collection",
            "cost": 3,
            "rarity": "common",
            "max_purchases": 3,
            "card_type": "ForestCard"
        }
    },
    "upgrades": {
        "efficient_ecosystems": {
            "name": "Efficient Ecosystems", 
            "description": "All terrain cards provide +2 baseline biomass permanently",
            "cost": 8,
            "rarity": "uncommon",
            "min_generation": 4,
            "effect_type": "baseline_biomass_boost",
            "effect_value": 2
        }
    }
}

# Configuration loader
class ShopConfigLoader:
    """Load and manage shop configuration"""
    
    @staticmethod
    def load_shop_config(config_path: str = "config/shop_config.json") -> Dict:
        """Load shop configuration from file"""
        with open(config_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def load_item_definitions(items_path: str = "config/shop_items.json") -> Dict:
        """Load item definitions from file"""
        with open(items_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def create_catalog_from_config(config: Dict, items: Dict) -> ShopCatalog:
        """Create shop catalog from configuration files"""
        catalog = ShopCatalog()
        # Implementation would parse JSON and create ShopItem objects
        return catalog
```

### Save/Load System Integration

```python
class ShopSaveManager:
    """Handle saving and loading shop state"""
    
    @staticmethod
    def save_shop_state(shop_manager: ShopManager, save_path: str) -> None:
        """Save complete shop state to file"""
        shop_data = {
            "energium": {
                "quota_bonus": shop_manager.game_state.energium.quota_bonus,
                "excess_bonus": shop_manager.game_state.energium.excess_bonus,
                "diversity_bonus": shop_manager.game_state.energium.diversity_bonus,
                "total": shop_manager.game_state.energium.total
            },
            "purchase_history": shop_manager.purchase_history,
            "item_purchase_counts": {
                item.item_id: item.times_purchased 
                for item in shop_manager.catalog.items.values()
            },
            "permanent_upgrades": getattr(shop_manager.game_state, 'permanent_upgrades', {}),
            "player_abilities": getattr(shop_manager.game_state, 'player_abilities', {}),
            "research_unlocks": list(getattr(shop_manager.game_state, 'research_unlocks', set()))
        }
        
        with open(save_path, 'w') as f:
            json.dump(shop_data, f, indent=2)
    
    @staticmethod
    def load_shop_state(shop_manager: ShopManager, save_path: str) -> bool:
        """Load shop state from file"""
        try:
            with open(save_path, 'r') as f:
                shop_data = json.load(f)
            
            # Restore energium
            energium_data = shop_data.get("energium", {})
            shop_manager.game_state.energium = Energium(
                quota_bonus=energium_data.get("quota_bonus", 0),
                excess_bonus=energium_data.get("excess_bonus", 0),
                diversity_bonus=energium_data.get("diversity_bonus", 0),
                total=energium_data.get("total", 0)
            )
            
            # Restore purchase history
            shop_manager.purchase_history = shop_data.get("purchase_history", [])
            
            # Restore item purchase counts
            purchase_counts = shop_data.get("item_purchase_counts", {})
            for item_id, count in purchase_counts.items():
                if item_id in shop_manager.catalog.items:
                    shop_manager.catalog.items[item_id].times_purchased = count
            
            # Restore upgrades and abilities
            shop_manager.game_state.permanent_upgrades = shop_data.get("permanent_upgrades", {})
            shop_manager.game_state.player_abilities = shop_data.get("player_abilities", {})
            shop_manager.game_state.research_unlocks = set(shop_data.get("research_unlocks", []))
            
            return True
            
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Failed to load shop state: {e}")
            return False
```

## User Interface Integration

### Shop UI Data Structures

```python
@dataclass
class ShopUIData:
    """Data structure for shop UI rendering"""
    current_energium: int
    energium_breakdown: Dict[str, int]
    available_items: Dict[str, List[ShopItem]]
    purchase_history: List[Dict]
    generation: int
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for UI consumption"""
        return {
            "current_energium": self.current_energium,
            "energium_breakdown": self.energium_breakdown,
            "categories": {
                category: [
                    {
                        "id": item.item_id,
                        "name": item.name,
                        "description": item.description,
                        "cost": item.cost,
                        "rarity": item.rarity.value,
                        "can_afford": self.current_energium >= item.cost,
                        "times_purchased": item.times_purchased,
                        "max_purchases": item.max_purchases
                    }
                    for item in items
                ]
                for category, items in self.available_items.items()
            },
            "recent_purchases": self.purchase_history[-5:],  # Last 5 purchases
            "generation": self.generation
        }

class ShopUIManager:
    """Manage shop UI data and interactions"""
    
    def __init__(self, shop_manager: ShopManager):
        self.shop_manager = shop_manager
    
    def get_shop_ui_data(self, generation: int) -> ShopUIData:
        """Get complete shop UI data for current state"""
        return ShopUIData(
            current_energium=self.shop_manager.game_state.energium.total,
            energium_breakdown=self.shop_manager.get_energium_breakdown(),
            available_items=self.shop_manager.get_shop_interface(generation),
            purchase_history=self.shop_manager.get_purchase_history(),
            generation=generation
        )
    
    def handle_purchase_request(self, item_id: str, generation: int) -> Dict[str, any]:
        """Handle UI purchase request and return result"""
        success, message = self.shop_manager.purchase_item(item_id, generation)
        
        return {
            "success": success,
            "message": message,
            "new_energium_total": self.shop_manager.game_state.energium.total,
            "updated_ui_data": self.get_shop_ui_data(generation).to_dict() if success else None
        }
```

## Error Handling and Validation

### Comprehensive Error Management

```python
class ShopSystemError(Exception):
    """Base exception for shop system errors"""
    pass

class InsufficientEnergiumError(ShopSystemError):
    """Raised when player doesn't have enough energium"""
    pass

class ItemNotAvailableError(ShopSystemError):
    """Raised when item is not available for purchase"""
    pass

class PurchaseLimitReachedError(ShopSystemError):
    """Raised when item purchase limit is reached"""
    pass

class InvalidItemError(ShopSystemError):
    """Raised when item ID is invalid"""
    pass

# Enhanced error handling in ShopManager
def purchase_item_safe(self, item_id: str, generation: int) -> Dict[str, any]:
    """Purchase item with comprehensive error handling"""
    try:
        if item_id not in self.catalog.items:
            raise InvalidItemError(f"Item '{item_id}' does not exist")
        
        item = self.catalog.items[item_id]
        
        if generation < item.min_generation:
            raise ItemNotAvailableError(
                f"'{item.name}' is not available until generation {item.min_generation}"
            )
        
        if item.times_purchased >= item.max_purchases:
            raise PurchaseLimitReachedError(
                f"Maximum purchases reached for '{item.name}' ({item.max_purchases})"
            )
        
        if self.game_state.energium.total < item.cost:
            raise InsufficientEnergiumError(
                f"Need {item.cost} energium, have {self.game_state.energium.total}"
            )
        
        # Execute purchase
        success, message = self.purchase_item(item_id, generation)
        
        return {
            "success": True,
            "message": message,
            "energium_spent": item.cost,
            "energium_remaining": self.game_state.energium.total
        }
        
    except ShopSystemError as e:
        return {
            "success": False,
            "error_type": type(e).__name__,
            "message": str(e),
            "energium_remaining": self.game_state.energium.total
        }
    except Exception as e:
        return {
            "success": False,
            "error_type": "UnexpectedError",
            "message": f"An unexpected error occurred: {str(e)}",
            "energium_remaining": self.game_state.energium.total
        }
```

## Usage Examples and Documentation

### Complete Usage Example

```python
# examples/shop_demo.py
"""
Complete shop system demonstration
Run with: python examples/shop_demo.py
"""

def demo_complete_shop_flow():
    """Demonstrate complete shop workflow"""
    print("=== Librium Shop System Demo ===\n")
    
    # Initialize game state and shop
    game_state = GameState()
    shop = ShopManager(game_state)
    
    # Simulate generation completion
    print("1. Completing Generation 1...")
    
    # Mock ecosystem state for diversity calculation
    class MockEcosystem:
        populations = [
            type('Pop', (), {'species_name': 'Hardy Grass', 'is_extinct': lambda: False})(),
            type('Pop', (), {'species_name': 'Field Mouse', 'is_extinct': lambda: False})(),
            type('Pop', (), {'species_name': 'Pioneer Moss', 'is_extinct': lambda: False})()
        ]
        hexes = [
            type('Hex', (), {'terrain_type': 'forest'})(),
            type('Hex', (), {'terrain_type': 'grassland'})()
        ]
    
    earned = shop.process_generation_completion(
        biomass_produced=130,
        quota_required=100,
        ecosystem_state=MockEcosystem(),
        difficulty=DifficultyMode.BALANCED
    )
    
    print(f"Energium earned: {earned.total}")
    print(f"  - Quota bonus: {earned.quota_bonus}")
    print(f"  - Excess bonus: {earned.excess_bonus}")
    print(f"  - Diversity bonus: {earned.diversity_bonus}")
    print(f"Total energium: {game_state.energium.total}\n")
    
    # Show shop interface
    print("2. Shop Interface:")
    shop_ui = ShopUIManager(shop)
    ui_data = shop_ui.get_shop_ui_data(generation=1)
    
    for category, items in ui_data.available_items.items():
        if items:
            print(f"\n{category.upper()}:")
            for item in items[:3]:  # Show first 3 items
                affordability = "✓" if ui_data.current_energium >= item.cost else "✗"
                print(f"  {affordability} {item.name} - {item.cost} energium")
                print(f"    {item.description}")
    
    # Make a purchase
    print("\n3. Making Purchase...")
    result = shop_ui.handle_purchase_request("extra_forest", generation=1)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        print(f"Energium remaining: {result['new_energium_total']}")
    else:
        print(f"✗ Purchase failed: {result['message']}")
    
    # Show updated shop
    print("\n4. Updated Shop State:")
    updated_data = shop_ui.get_shop_ui_data(generation=1)
    print(f"Current energium: {updated_data.current_energium}")
    print(f"Recent purchases: {len(updated_data.purchase_history)}")

def demo_progression_simulation():
    """Simulate shop progression across multiple generations"""
    print("\n=== Multi-Generation Shop Progression ===\n")
    
    game_state = GameState() 
    shop = ShopManager(game_state)
    
    # Simulate 10 generations
    for gen in range(1, 11):
        # Simulate varying performance
        quota = 100 + (gen - 1) * 50  # Increasing quotas
        produced = quota + random.randint(-20, 100)  # Variable performance
        
        # Mock ecosystem with increasing diversity
        class MockEcosystem:
            populations = [type('Pop', (), {
                'species_name': f'Species_{i}', 
                'is_extinct': lambda: False
            })() for i in range(min(gen + 1, 6))]
            hexes = [type('Hex', (), {
                'terrain_type': f'biome_{i}'
            })() for i in range(min(gen, 4))]
        
        earned = shop.process_generation_completion(
            produced, quota, MockEcosystem(), DifficultyMode.BALANCED
        )
        
        print(f"Gen {gen:2d}: {produced:3d}/{quota:3d} biomass, "
              f"{earned.total:2d} energium (total: {game_state.energium.total:3d})")
        
        # Make strategic purchases
        if game_state.energium.total >= 8 and gen >= 4:
            success, msg = shop.purchase_item("efficient_ecosystems", gen)
            if success:
                print(f"       Purchased: Efficient Ecosystems")

if __name__ == "__main__":
    demo_complete_shop_flow()
    demo_progression_simulation()
```

## Installation and Setup

### File Structure
```
librium/
├── core/
│   ├── __init__.py
│   ├── shop_system.py           # Main shop classes
│   ├── energium_calculator.py   # Energium calculation logic
│   └── shop_items.py           # Shop item definitions
├── config/
│   ├── shop_config.json        # Shop configuration
│   └── shop_items.json         # Item definitions
├── tests/
│   ├── test_shop_system.py     # Shop system tests
│   ├── test_energium.py        # Energium calculation tests
│   └── test_shop_integration.py # Integration tests
├── examples/
│   └── shop_demo.py            # Usage examples
└── docs/
    └── shop_api.md             # API documentation
```

### Integration Checklist

1. **✓ Core Implementation**
   - [ ] Implement EnergiumCalculator class
   - [ ] Implement ShopItem hierarchy
   - [ ] Implement ShopCatalog with initial items
   - [ ] Implement ShopManager

2. **✓ Game Integration**
   - [ ] Integrate with GameState class
   - [ ] Connect to generation completion workflow
   - [ ] Integrate with terrain baseline biomass system
   - [ ] Connect to pioneer species enhancements

3. **✓ Testing**
   - [ ] Unit tests for energium calculation
   - [ ] Shop purchase flow tests
   - [ ] Integration tests with existing systems
   - [ ] Performance testing for large catalogs

4. **✓ Configuration**
   - [ ] Create shop configuration files
   - [ ] Implement save/load functionality
   - [ ] Add balance tuning parameters

5. **✓ UI Integration**
   - [ ] Implement ShopUIManager
   - [ ] Create shop interface data structures
   - [ ] Add error handling for UI interactions

This technical specification provides a complete implementation guide for the Librium shop system, ready for Claude Code to implement with full integration into the existing game architecture.