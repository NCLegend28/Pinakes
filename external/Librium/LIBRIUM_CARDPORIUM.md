# 🌿 Librium Cardporium 🌿
## Complete Card Collection & Shop Catalog

*The definitive guide to all cards, items, and purchasables in the Librium ecosystem management game*

---

## 📋 Table of Contents
- [🌍 Terrain Cards](#-terrain-cards)
- [🌱 Flora Cards](#-flora-cards)
- [🐾 Fauna Cards](#-fauna-cards)
- [🌦️ Weather Cards](#️-weather-cards)
- [🛒 Shop System](#-shop-system)
  - [💳 Purchasable Cards](#-purchasable-cards)
  - [⚡ Permanent Upgrades](#-permanent-upgrades)
  - [🔬 Pioneer Enhancements](#-pioneer-enhancements)
  - [🎯 Special Abilities](#-special-abilities)
  - [📚 Research Unlocks](#-research-unlocks)

---

## 🌍 Terrain Cards

*Foundation cards that create ecosystem infrastructure and carrying capacity*

### 🌲 Forest Terrain
**Card ID:** `forest_terrain`
**Name:** Forest Terrain
**Rarity:** Common
**Biome Theme:** Forest
**Cost:** Base terrain card

**Description:** Dense canopy forest with high carrying capacity for diverse species

**Terrain Properties:**
- **Carrying Capacity:**
  - Producers: 3 per hex
  - Primary Consumers: 2 per hex
  - Secondary Consumers: 1 per hex
  - Omnivores: 1 per hex
  - Decomposers: 1 per hex
- **Baseline Biomass:** 12 per hex
- **Resource Modifier:** 1.0x
- **Stability Bonus:** +0.1
- **Weather Resistance:**
  - Drought: 0.8x (vulnerable)
  - Flood: 1.0x (neutral)
  - Cold Snap: 1.1x (resistant)
  - Heat Wave: 0.9x (slightly vulnerable)

**Synergy Bonuses:**
- Adjacent to Grassland: +20% herbivore migration
- Adjacent to Wetland: +15% overall production
- Adjacent to Mountain: +10% carnivore territory bonus

---

### 🌾 Grassland Terrain
**Card ID:** `grassland_terrain`
**Name:** Grassland Terrain
**Rarity:** Common
**Biome Theme:** Grassland
**Cost:** Base terrain card

**Description:** Open grassland perfect for grazing herbivores with excellent visibility

**Terrain Properties:**
- **Carrying Capacity:**
  - Producers: 2 per hex
  - Primary Consumers: 4 per hex (highest)
  - Secondary Consumers: 1 per hex
  - Omnivores: 2 per hex
  - Decomposers: 1 per hex
- **Baseline Biomass:** 10 per hex
- **Resource Modifier:** 1.1x (grazing efficiency)
- **Stability Bonus:** +0.05
- **Weather Resistance:**
  - Drought: 0.7x (very vulnerable)
  - Flood: 0.9x (vulnerable)
  - Cold Snap: 0.8x (vulnerable)
  - Heat Wave: 1.2x (very resistant)

**Synergy Bonuses:**
- Adjacent to Forest: +25% herbivore migration bonus
- Adjacent to Wetland: +20% seasonal grazing bonus
- 3+ Adjacent Grasslands: +15% herd formation bonus

---

### 💧 Wetland Terrain
**Card ID:** `wetland_terrain`
**Name:** Wetland Terrain
**Rarity:** Common
**Biome Theme:** Wetland
**Cost:** Base terrain card

**Description:** Rich wetland ecosystem with highest baseline biomass production

**Terrain Properties:**
- **Carrying Capacity:**
  - Producers: 4 per hex (highest)
  - Primary Consumers: 2 per hex
  - Secondary Consumers: 2 per hex
  - Omnivores: 2 per hex
  - Decomposers: 2 per hex (excellent)
- **Baseline Biomass:** 15 per hex (highest)
- **Resource Modifier:** 1.2x (nutrient rich)
- **Stability Bonus:** +0.15 (most stable)
- **Weather Resistance:**
  - Drought: 1.3x (very resistant)
  - Flood: 1.1x (resistant)
  - Cold Snap: 0.9x (slightly vulnerable)
  - Heat Wave: 1.0x (neutral)

**Synergy Bonuses:**
- Adjacent to any terrain: +15% decomposer efficiency
- Adjacent to Forest: +20% amphibian bonus
- Adjacent to Grassland: +20% seasonal migration bonus

---

### 🏜️ Desert Terrain
**Card ID:** `desert_terrain`
**Name:** Desert Terrain
**Rarity:** Common
**Biome Theme:** Desert
**Cost:** Base terrain card

**Description:** Harsh desert environment requiring specialized drought-resistant species

**Terrain Properties:**
- **Carrying Capacity:**
  - Producers: 1 per hex (lowest)
  - Primary Consumers: 1 per hex
  - Secondary Consumers: 1 per hex
  - Omnivores: 1 per hex
  - Decomposers: 1 per hex
- **Baseline Biomass:** 6 per hex (lowest)
- **Resource Modifier:** 0.7x (harsh conditions)
- **Stability Bonus:** -0.05 (challenging)
- **Weather Resistance:**
  - Drought: 1.5x (extremely resistant)
  - Flood: 0.6x (very vulnerable)
  - Cold Snap: 0.7x (vulnerable)
  - Heat Wave: 1.3x (very resistant)

**Synergy Bonuses:**
- Adjacent to Wetland: +25% oasis effect
- 3+ Adjacent Desert: +10% adaptation bonus
- Adjacent to Mountain: +15% specialized predator bonus

---

### ⛰️ Mountain Terrain
**Card ID:** `mountain_terrain`
**Name:** Mountain Terrain
**Rarity:** Common
**Biome Theme:** Mountain
**Cost:** Base terrain card

**Description:** High-altitude terrain ideal for predator territories and specialized species

**Terrain Properties:**
- **Carrying Capacity:**
  - Producers: 1 per hex
  - Primary Consumers: 1 per hex
  - Secondary Consumers: 2 per hex (predator territory)
  - Omnivores: 1 per hex
  - Decomposers: 1 per hex
- **Baseline Biomass:** 8 per hex
- **Resource Modifier:** 0.8x
- **Stability Bonus:** +0.05
- **Weather Resistance:**
  - Drought: 0.9x (slightly vulnerable)
  - Flood: 1.1x (resistant - good drainage)
  - Cold Snap: 1.2x (adapted to cold)
  - Heat Wave: 0.4x (very vulnerable)

**Synergy Bonuses:**
- Adjacent to Forest: +20% predator territory advantage
- Adjacent to Grassland: +10% hunting grounds bonus
- Adjacent to Desert: +20% specialized adaptation bonus

---

## 🌱 Flora Cards

*Producer cards that form the base of ecosystem food webs*

### 🌳 Ancient Oak
**Card ID:** `ancient_oak`
**Name:** Ancient Oak
**Rarity:** Common
**Biome Theme:** Forest
**Cost:** 2 Energy

**Description:** Majestic oak tree providing excellent habitat and food sources

**Species Properties:**
- **Trophic Level:** Producer
- **Population Size:** 2 per hex
- **Growth Rate:** 1.0x (standard)
- **Preferred Terrains:** Forest, Grassland
- **Feeding Range:** 0 (producer)
- **Special Abilities:**
  - Provides +1 stability bonus per hex
  - Creates microhabitat for small fauna

**Biomass Production:** 3.0 per population
**Optimal Conditions:** Forest terrain + moderate moisture
**Synergies:** +20% efficiency when adjacent to wetlands

---

### 🌾 Prairie Grass
**Card ID:** `prairie_grass`
**Name:** Prairie Grass
**Rarity:** Common
**Biome Theme:** Grassland
**Cost:** 1 Energy

**Description:** Hardy grass species forming the foundation of grassland ecosystems

**Species Properties:**
- **Trophic Level:** Producer
- **Population Size:** 4 per hex
- **Growth Rate:** 1.2x (fast growing)
- **Preferred Terrains:** Grassland, Desert
- **Feeding Range:** 0 (producer)
- **Special Abilities:**
  - High reproduction rate
  - Drought resistance
  - Excellent grazer support

**Biomass Production:** 2.0 per population
**Optimal Conditions:** Open grassland + full sunlight
**Synergies:** +25% when in clusters of 3+ hexes

---

### 🌿 Marsh Sedge
**Card ID:** `marsh_sedge`
**Name:** Marsh Sedge
**Rarity:** Common
**Biome Theme:** Wetland
**Cost:** 2 Energy

**Description:** Aquatic grass providing critical wetland habitat and water filtration

**Species Properties:**
- **Trophic Level:** Producer
- **Population Size:** 3 per hex
- **Growth Rate:** 1.1x
- **Preferred Terrains:** Wetland
- **Feeding Range:** 0 (producer)
- **Special Abilities:**
  - Water purification
  - Flood control
  - Spawning habitat for aquatic fauna

**Biomass Production:** 3.5 per population
**Optimal Conditions:** Wetland terrain + clean water
**Synergies:** +30% efficiency when adjacent to multiple water sources

---

### 🌵 Desert Succulent
**Card ID:** `desert_succulent`
**Name:** Desert Succulent
**Rarity:** Uncommon
**Biome Theme:** Desert
**Cost:** 3 Energy

**Description:** Specialized water-storing plant thriving in extreme desert conditions

**Species Properties:**
- **Trophic Level:** Producer
- **Population Size:** 2 per hex
- **Growth Rate:** 0.8x (slow but steady)
- **Preferred Terrains:** Desert, Mountain
- **Feeding Range:** 0 (producer)
- **Special Abilities:**
  - Extreme drought resistance
  - Water storage for other species
  - Blooms provide seasonal nectar

**Biomass Production:** 2.5 per population
**Optimal Conditions:** Desert terrain + temperature extremes
**Synergies:** +40% efficiency during drought events

---

### 🍄 Forest Mushrooms
**Card ID:** `forest_mushrooms`
**Name:** Forest Mushrooms
**Rarity:** Uncommon
**Biome Theme:** Forest
**Cost:** 2 Energy

**Description:** Decomposer fungi that recycle nutrients and support forest health

**Species Properties:**
- **Trophic Level:** Decomposer
- **Population Size:** 3 per hex
- **Growth Rate:** 1.3x (rapid decomposition)
- **Preferred Terrains:** Forest, Wetland
- **Feeding Range:** 1 hex (processes organic matter)
- **Special Abilities:**
  - Nutrient cycling
  - Soil health improvement
  - Mycelial network communication

**Biomass Production:** 2.0 per population
**Optimal Conditions:** Forest terrain + organic matter
**Synergies:** +50% efficiency in areas with high mortality

---

## 🐾 Fauna Cards

*Consumer cards that create dynamic food webs and population interactions*

### 🐰 Meadow Rabbit
**Card ID:** `meadow_rabbit`
**Name:** Meadow Rabbit
**Rarity:** Common
**Biome Theme:** Grassland
**Cost:** 3 Energy

**Description:** Fast-breeding herbivore forming the cornerstone of grassland food webs

**Species Properties:**
- **Trophic Level:** Primary Consumer (Herbivore)
- **Population Size:** 3 per hex
- **Growth Rate:** 1.4x (very fast breeding)
- **Preferred Terrains:** Grassland, Forest
- **Feeding Range:** 2 hexes
- **Food Requirements:** 4.5 producer biomass per population

**Special Abilities:**
- High reproductive rate
- Escape behavior from predators
- Seasonal population booms

**Biomass Production:** 2.5 per population
**Optimal Conditions:** Abundant grass + predator presence for balance
**Synergies:** +20% reproduction rate when adjacent to multiple grasslands

---

### 🦌 Forest Deer
**Card ID:** `forest_deer`
**Name:** Forest Deer
**Rarity:** Common
**Biome Theme:** Forest
**Cost:** 4 Energy

**Description:** Graceful herbivore that migrates between forest clearings and edges

**Species Properties:**
- **Trophic Level:** Primary Consumer (Herbivore)
- **Population Size:** 2 per hex
- **Growth Rate:** 1.1x
- **Preferred Terrains:** Forest, Grassland
- **Feeding Range:** 3 hexes (migratory)
- **Food Requirements:** 3.0 producer biomass per population

**Special Abilities:**
- Seasonal migration
- Selective browsing
- Alert system for herd protection

**Biomass Production:** 4.0 per population
**Optimal Conditions:** Mixed forest-grassland edges
**Synergies:** +25% efficiency when paths exist between biomes

---

### 🐺 Gray Wolf
**Card ID:** `gray_wolf`
**Name:** Gray Wolf
**Rarity:** Rare
**Biome Theme:** Forest
**Cost:** 6 Energy

**Description:** Apex predator maintaining ecosystem balance through pack hunting

**Species Properties:**
- **Trophic Level:** Secondary Consumer (Carnivore)
- **Population Size:** 1 per hex
- **Growth Rate:** 0.9x (slow, steady)
- **Preferred Terrains:** Forest, Mountain
- **Feeding Range:** 4 hexes (pack territory)
- **Food Requirements:** 6.0 herbivore biomass per population

**Special Abilities:**
- Pack hunting coordination
- Territory establishment
- Population control of herbivores

**Biomass Production:** 5.0 per population
**Optimal Conditions:** Large territory with abundant prey
**Synergies:** +30% hunting success in mountainous terrain

---

### 🦅 Golden Eagle
**Card ID:** `golden_eagle`
**Name:** Golden Eagle
**Rarity:** Rare
**Biome Theme:** Mountain
**Cost:** 5 Energy

**Description:** Soaring raptor with excellent visibility and hunting range

**Species Properties:**
- **Trophic Level:** Secondary Consumer (Carnivore)
- **Population Size:** 1 per hex
- **Growth Rate:** 0.8x (slow reproduction)
- **Preferred Terrains:** Mountain, Forest
- **Feeding Range:** 5 hexes (aerial hunting)
- **Food Requirements:** 5.0 small animal biomass per population

**Special Abilities:**
- Aerial reconnaissance
- Thermal soaring
- Scavenging capability

**Biomass Production:** 4.5 per population
**Optimal Conditions:** High elevation + open hunting grounds
**Synergies:** +40% hunting efficiency from mountain perches

---

### 🐸 Pond Frog
**Card ID:** `pond_frog`
**Name:** Pond Frog
**Rarity:** Common
**Biome Theme:** Wetland
**Cost:** 2 Energy

**Description:** Amphibian indicator species crucial for wetland ecosystem health

**Species Properties:**
- **Trophic Level:** Primary Consumer (Insectivore)
- **Population Size:** 4 per hex
- **Growth Rate:** 1.3x (boom-bust cycles)
- **Preferred Terrains:** Wetland, Forest
- **Feeding Range:** 1 hex (local)
- **Food Requirements:** 2.0 small producer/insect biomass per population

**Special Abilities:**
- Metamorphic life cycle
- Pollution sensitivity (ecosystem indicator)
- Pest control services

**Biomass Production:** 1.5 per population
**Optimal Conditions:** Clean water + stable temperatures
**Synergies:** +50% reproduction in pristine wetlands

---

### 🐻 Brown Bear
**Card ID:** `brown_bear`
**Name:** Brown Bear
**Rarity:** Legendary
**Biome Theme:** Forest
**Cost:** 8 Energy

**Description:** Massive omnivore requiring large territories and diverse food sources

**Species Properties:**
- **Trophic Level:** Omnivore
- **Population Size:** 1 per hex (territorial)
- **Growth Rate:** 0.7x (very slow reproduction)
- **Preferred Terrains:** Forest, Mountain, Wetland
- **Feeding Range:** 6 hexes (massive territory)
- **Food Requirements:**
  - 3.0 plant biomass per population
  - 3.0 animal biomass per population

**Special Abilities:**
- Seasonal diet switching
- Salmon run timing
- Hibernation capability
- Seed dispersal services

**Biomass Production:** 8.0 per population
**Optimal Conditions:** Large territory spanning multiple biomes
**Synergies:** +25% efficiency when wetland-forest-mountain borders exist

---

## 🌦️ Weather Cards

*Environmental event cards that create dynamic challenges and opportunities*

### ☀️ Heat Wave
**Card ID:** `heat_wave`
**Name:** Heat Wave
**Rarity:** Common
**Event Type:** Weather
**Duration:** 2 turns

**Description:** Prolonged period of extreme heat stressing water-dependent species

**Effects:**
- **Temperature:** +3°C above normal
- **Moisture Reduction:** -40%
- **Terrain Modifiers:**
  - Desert: +30% efficiency (adapted)
  - Grassland: +20% efficiency
  - Forest: -10% efficiency
  - Wetland: -20% efficiency
  - Mountain: -60% efficiency (elevation contrast)

**Population Effects:**
- Drought-adapted species: +15% growth
- Water-dependent species: -25% growth
- Increased water competition

**Strategic Uses:** Clear excess water-dependent populations, boost desert species

---

### 🌨️ Cold Snap
**Card ID:** `cold_snap`
**Name:** Cold Snap
**Rarity:** Common
**Event Type:** Weather
**Duration:** 2 turns

**Description:** Sudden temperature drop testing species' cold adaptation

**Effects:**
- **Temperature:** -5°C below normal
- **Activity Reduction:** -30%
- **Terrain Modifiers:**
  - Mountain: +20% efficiency (adapted)
  - Forest: +10% efficiency
  - Desert: -30% efficiency
  - Grassland: -20% efficiency
  - Wetland: -10% efficiency

**Population Effects:**
- Cold-adapted species: +10% growth
- Warm-climate species: -20% growth
- Reduced reproductive activity

**Strategic Uses:** Control warm-climate overpopulation, favor alpine species

---

### 🌧️ Heavy Rainfall
**Card ID:** `heavy_rainfall`
**Name:** Heavy Rainfall
**Rarity:** Uncommon
**Event Type:** Weather
**Duration:** 3 turns

**Description:** Extended period of abundant precipitation boosting plant growth

**Effects:**
- **Precipitation:** +200% above normal
- **Growth Boost:** +25% for producers
- **Terrain Modifiers:**
  - Wetland: +30% efficiency
  - Forest: +15% efficiency
  - Grassland: +10% efficiency
  - Desert: -10% efficiency (flooding)
  - Mountain: 0% (runoff)

**Population Effects:**
- Plant species: +25% growth rate
- Water-loving fauna: +15% growth
- Desert species: -15% growth

**Strategic Uses:** Boost plant production, support water ecosystems

---

### 🌪️ Storm Front
**Card ID:** `storm_front`
**Name:** Storm Front
**Rarity:** Rare
**Event Type:** Weather
**Duration:** 1 turn (intense)

**Description:** Violent storm causing ecosystem disruption and reshuffling

**Effects:**
- **Disturbance Level:** Extreme
- **Population Mixing:** Forces migration
- **Terrain Effects:**
  - Random population redistribution
  - 10% chance of population loss per hex
  - +20% pioneer species colonization next turn

**Strategic Uses:**
- Break up stagnant ecosystems
- Create opportunities for new colonization
- Reset overpopulated areas

---

### 🌤️ Perfect Weather
**Card ID:** `perfect_weather`
**Name:** Perfect Weather
**Rarity:** Rare
**Event Type:** Weather
**Duration:** 2 turns

**Description:** Ideal conditions promoting ecosystem flourishing and growth

**Effects:**
- **Growth Bonus:** +20% all species
- **Stability Bonus:** +15% ecosystem stability
- **No negative modifiers**
- **Breeding Season:** +30% reproduction rates

**Population Effects:**
- All species benefit equally
- Increased carrying capacity utilization
- Enhanced synergy bonuses

**Strategic Uses:** Maximize growth during ecosystem development phases

---

## 🛒 Shop System

*Inter-generational progression through energium-based purchases*

### Energium Currency
**Base Earning Rates:**
- **Quota Success:** 2 energium
- **Excess Production:** +1 per 25% over quota
- **Diversity Bonus:** 2 energium (if threshold met)
- **Consolation:** 1 energium (Contemplative/Balanced modes only)

**Difficulty Thresholds:**
- **Contemplative:** 6.0 diversity points
- **Balanced:** 8.0 diversity points
- **Intense:** 10.0 diversity points
- **Brutal:** 12.0 diversity points

---

## 💳 Purchasable Cards

*Additional cards available through shop purchases*

### 🌲 Extra Forest Card
**Item ID:** `extra_forest`
**Shop Category:** Cards
**Cost:** 3 energium
**Rarity:** Common
**Availability:** Generation 1+
**Max Purchases:** 3

**Description:** Add an additional Forest terrain card to your collection

**Contents:** Standard Forest Terrain Card
**Strategic Value:** Expand forest biome options for forest-focused strategies

---

### 💧 Extra Wetland Card
**Item ID:** `extra_wetland`
**Shop Category:** Cards
**Cost:** 4 energium
**Rarity:** Common
**Availability:** Generation 1+
**Max Purchases:** 3

**Description:** Add an additional Wetland terrain card to your collection

**Contents:** Standard Wetland Terrain Card
**Strategic Value:** Essential for high-biomass strategies due to wetland's superior baseline production

---

### 🌾 Extra Grassland Card
**Item ID:** `extra_grassland`
**Shop Category:** Cards
**Cost:** 3 energium
**Rarity:** Common
**Availability:** Generation 1+
**Max Purchases:** 3

**Description:** Add an additional Grassland terrain card for grazing animals

**Contents:** Standard Grassland Terrain Card
**Strategic Value:** Critical for herbivore-focused ecosystem builds

---

### 🌿 Specialized Moss Species
**Item ID:** `specialized_moss`
**Shop Category:** Cards
**Cost:** 6 energium
**Rarity:** Uncommon
**Availability:** Generation 3+
**Max Purchases:** 2

**Description:** Hardy moss that thrives in multiple biomes with +20% growth rate

**Card Properties:**
- **Trophic Level:** Producer
- **Population Size:** 3 per hex
- **Growth Rate:** 1.3x (+20% bonus)
- **Preferred Terrains:** Forest, Wetland, Mountain
- **Biomass Production:** 3.0 per population
- **Special:** Multi-biome adaptation

**Strategic Value:** Versatile producer for mixed-biome strategies

---

### 🌊 Nutrient-Rich Algae
**Item ID:** `nutrient_rich_algae`
**Shop Category:** Cards
**Cost:** 7 energium
**Rarity:** Uncommon
**Availability:** Generation 4+
**Max Purchases:** 2

**Description:** Aquatic producer providing excellent food base for wetland ecosystems

**Card Properties:**
- **Trophic Level:** Producer
- **Population Size:** 4 per hex
- **Growth Rate:** 1.25x
- **Preferred Terrains:** Wetland
- **Biomass Production:** 4.0 per population
- **Special:** Enhanced aquatic productivity

**Strategic Value:** Supercharge wetland food webs

---

### 🐺 Apex Predator
**Item ID:** `apex_predator`
**Shop Category:** Cards
**Cost:** 12 energium
**Rarity:** Rare
**Availability:** Generation 6+
**Max Purchases:** 1

**Description:** Powerful carnivore providing excellent population control

**Card Properties:**
- **Trophic Level:** Secondary Consumer
- **Population Size:** 1 per hex
- **Growth Rate:** 1.1x
- **Preferred Terrains:** Forest, Mountain
- **Feeding Range:** 3 hexes
- **Food Requirements:** 8.0 herbivore biomass per population
- **Biomass Production:** 6.0 per population
- **Special:** Elite population control

**Strategic Value:** Ultimate predator for controlling herbivore overpopulation

---

### 🦌 Migratory Herbivore
**Item ID:** `migratory_herbivore`
**Shop Category:** Cards
**Cost:** 10 energium
**Rarity:** Rare
**Availability:** Generation 5+
**Max Purchases:** 2

**Description:** Mobile herbivore that can feed across multiple terrain types

**Card Properties:**
- **Trophic Level:** Primary Consumer
- **Population Size:** 3 per hex
- **Growth Rate:** 1.15x
- **Preferred Terrains:** Grassland, Forest, Wetland
- **Feeding Range:** 4 hexes (extended mobility)
- **Food Requirements:** 4.5 producer biomass per population
- **Biomass Production:** 3.5 per population
- **Special:** Cross-terrain feeding

**Strategic Value:** Links disconnected ecosystems through mobile feeding

---

## ⚡ Permanent Upgrades

*One-time purchases that permanently enhance gameplay capabilities*

### 🏭 Efficient Ecosystems
**Item ID:** `efficient_ecosystems`
**Shop Category:** Upgrades
**Cost:** 8 energium
**Rarity:** Uncommon
**Availability:** Generation 4+
**Max Purchases:** 1

**Description:** All terrain cards provide +2 baseline biomass permanently

**Upgrade Effects:**
- **Terrain Bonus:** +2 baseline biomass per hex
- **Applies to:** All existing and future terrain
- **Stacks with:** Cluster bonuses and synergies

**Strategic Impact:**
- Forest: 12 → 14 baseline biomass (+17%)
- Wetland: 15 → 17 baseline biomass (+13%)
- Grassland: 10 → 12 baseline biomass (+20%)

**Value Analysis:** Permanent 13-20% increase in baseline production

---

### 🔗 Enhanced Synergies
**Item ID:** `enhanced_synergies`
**Shop Category:** Upgrades
**Cost:** 12 energium
**Rarity:** Rare
**Availability:** Generation 7+
**Max Purchases:** 1

**Description:** All synergy bonuses increased by 25%

**Upgrade Effects:**
- **Synergy Multiplier:** +25% to all bonuses
- **Cluster Bonuses:** Enhanced
- **Cross-biome Synergies:** Enhanced

**Example Improvements:**
- Forest-Grassland synergy: 20% → 25%
- 5-hex cluster bonus: 35% → 43.75%
- Desert oasis effect: 25% → 31.25%

**Strategic Impact:** Dramatically increases value of strategic terrain placement

---

### 🎓 Master Ecologist
**Item ID:** `master_ecologist`
**Shop Category:** Upgrades
**Cost:** 15 energium
**Rarity:** Rare
**Availability:** Generation 8+
**Max Purchases:** 1

**Description:** Unlock advanced ecosystem information and prediction tools

**UI Enhancements:**
- **Advanced Ecosystem Info:** Detailed population predictions
- **Food Web Analysis:** Visual food web connections
- **Carrying Capacity Meters:** Real-time capacity utilization
- **Stability Predictions:** Multi-turn stability forecasts

**Strategic Value:** Information advantage for complex ecosystem management

---

## 🔬 Pioneer Enhancements

*Upgrades that modify pioneer species behavior and effectiveness*

### 🧬 Pioneer Breeding Program
**Item ID:** `pioneer_breeding`
**Shop Category:** Pioneer Enhancement
**Cost:** 5 energium
**Rarity:** Common
**Availability:** Generation 1+
**Max Purchases:** 1

**Description:** Pioneer species use only 45% of carrying capacity (down from 60%)

**Enhancement Effects:**
- **Capacity Usage:** 60% → 45% (25% reduction)
- **Effect:** More room for player species
- **Applies to:** All current and future pioneer species

**Strategic Impact:** Significant increase in player species placement options

---

### 🛡️ Pioneer Species Resilience
**Item ID:** `pioneer_resilience`
**Shop Category:** Pioneer Enhancement
**Cost:** 7 energium
**Rarity:** Uncommon
**Availability:** Generation 5+
**Max Purchases:** 1

**Description:** Pioneer species gain +25% resistance to environmental disasters

**Enhancement Effects:**
- **Disaster Resistance:** +25% survival rate
- **Stability Contribution:** Enhanced ecosystem stability
- **Weather Resistance:** Improved weather event survival

**Strategic Value:** More stable pioneer foundations during crisis events

---

### 🧭 Enhanced Pioneer Adaptation
**Item ID:** `pioneer_adaptation`
**Shop Category:** Pioneer Enhancement
**Cost:** 6 energium
**Rarity:** Uncommon
**Availability:** Generation 3+
**Max Purchases:** 1

**Description:** Pioneer species adapt to non-preferred terrain 75% of the time (up from 50%)

**Enhancement Effects:**
- **Adaptation Rate:** 50% → 75% (50% increase)
- **Terrain Flexibility:** More diverse pioneer colonization
- **Ecosystem Coverage:** Better baseline coverage across biomes

**Strategic Value:** More consistent pioneer establishment across all terrain types

---

## 🎯 Special Abilities

*Consumable powers with limited uses for tactical advantages*

### ⛑️ Emergency Ecosystem Intervention
**Item ID:** `emergency_intervention`
**Shop Category:** Abilities
**Cost:** 10 energium
**Rarity:** Uncommon
**Availability:** Generation 1+
**Max Purchases:** 3
**Uses per Purchase:** 1

**Description:** One-time ability to prevent any species extinction

**Ability Effects:**
- **Target:** Any species in critical/extinct state
- **Effect:** Instantly restore to stable population
- **Usage:** Activate during any turn
- **Cooldown:** None (consumable)

**Strategic Applications:**
- Save valuable keystone species
- Prevent cascade extinctions
- Recover from disaster events
- Protect unique builds

---

### 🌤️ Weather Prediction System
**Item ID:** `weather_prediction`
**Shop Category:** Abilities
**Cost:** 6 energium
**Rarity:** Common
**Availability:** Generation 1+
**Max Purchases:** 2
**Uses per Purchase:** 3

**Description:** See next turn's weather in advance (3 uses)

**Ability Effects:**
- **Information:** Reveals next weather event
- **Planning Advantage:** Prepare ecosystem for upcoming conditions
- **Usage:** Activate before ending turn
- **Duration:** Instant information

**Strategic Applications:**
- Optimize species placement for weather
- Prepare for disasters
- Time weather-dependent strategies
- Avoid weather-vulnerable builds

---

### 💊 Ecosystem Vitality Boost
**Item ID:** `ecosystem_boost`
**Shop Category:** Abilities
**Cost:** 8 energium
**Rarity:** Uncommon
**Availability:** Generation 3+
**Max Purchases:** 2
**Uses per Purchase:** 2

**Description:** Instantly improve all population states by one level (2 uses)

**Ability Effects:**
- **Target:** All populations in ecosystem
- **Effect:**
  - Critical → Stressed
  - Stressed → Stable
  - Stable → Thriving
- **Usage:** Activate during any turn

**Strategic Applications:**
- Recovery from poor performance
- Boost ecosystem before evaluation
- Enhance carrying capacity efficiency
- Prepare for difficult quotas

---

## 📚 Research Unlocks

*High-cost unlocks that add new game mechanics and systems*

### 🧬 Genetic Diversity Research
**Item ID:** `genetic_diversity`
**Shop Category:** Research
**Cost:** 20 energium
**Rarity:** Legendary
**Availability:** Generation 12+
**Max Purchases:** 1

**Description:** Unlock genetic diversity tracking and breeding mechanics

**Research Unlocks:**
- **Genetic Tracking:** Monitor species adaptation over time
- **Breeding Programs:** Enhance species traits through selection
- **Hybrid Species:** Create new species through crossbreeding
- **Evolution Mechanics:** Long-term species adaptation systems

**New Systems:**
- Genetic diversity bonus calculations
- Species trait modification
- Evolutionary pressure responses
- Population genetics management

**Strategic Impact:** Adds entire new layer of species optimization

---

### 🌡️ Climate Adaptation Research
**Item ID:** `climate_adaptation`
**Shop Category:** Research
**Cost:** 18 energium
**Rarity:** Legendary
**Availability:** Generation 10+
**Max Purchases:** 1

**Description:** Unlock advanced weather resistance and adaptation mechanics

**Research Unlocks:**
- **Climate Zones:** Biome-specific weather patterns
- **Adaptation Tracking:** Species weather resistance evolution
- **Microclimate Management:** Terrain-level weather modification
- **Climate Events:** New extreme weather types

**New Systems:**
- Advanced weather prediction
- Species climate adaptation
- Terrain weather modification
- Long-term climate trends

**Strategic Impact:** Transforms weather from random events to strategic elements

---

## 📊 Card Statistics Summary

### Card Distribution by Rarity
- **Common:** 12 cards (60%)
- **Uncommon:** 5 cards (25%)
- **Rare:** 2 cards (10%)
- **Legendary:** 1 card (5%)

### Card Distribution by Type
- **Terrain Cards:** 5 cards
- **Flora Cards:** 5 cards
- **Fauna Cards:** 6 cards
- **Weather Cards:** 5 cards
- **Shop Items:** 16 items

### Cost Analysis (Shop Items)
- **Low Cost (3-6 energium):** 8 items
- **Medium Cost (7-10 energium):** 5 items
- **High Cost (12-18 energium):** 3 items
- **Premium Cost (20+ energium):** 1 item

### Strategic Archetypes Supported
- **Forest Ecosystem:** 6 specialized cards
- **Grassland Grazing:** 5 specialized cards
- **Wetland Production:** 4 specialized cards
- **Desert Survival:** 3 specialized cards
- **Mountain Predation:** 4 specialized cards
- **Multi-Biome Synergy:** 8 cards

---

## 🎯 Deck Building Strategies

### Early Game Foundation (Generations 1-3)
**Recommended Purchases:**
1. Extra terrain cards (3-4 energium each)
2. Pioneer Breeding Program (5 energium)
3. Weather Prediction System (6 energium)

**Strategy:** Establish reliable terrain base and pioneer management

### Mid Game Development (Generations 4-7)
**Recommended Purchases:**
1. Specialized flora cards (6-7 energium)
2. Efficient Ecosystems upgrade (8 energium)
3. Emergency Intervention abilities (10 energium)

**Strategy:** Enhance production and add safety mechanisms

### Late Game Optimization (Generations 8+)
**Recommended Purchases:**
1. Rare fauna cards (10-12 energium)
2. Enhanced Synergies upgrade (12 energium)
3. Master Ecologist upgrade (15 energium)

**Strategy:** Maximize efficiency and unlock advanced features

### End Game Mastery (Generation 10+)
**Recommended Purchases:**
1. Research unlocks (18-20 energium)
2. Premium abilities and enhancements
3. Complete card collection

**Strategy:** Access exclusive mechanics and perfect ecosystem control

---

*This Cardporium represents the complete catalog as of the current implementation. New cards and items may be added in future updates to expand strategic possibilities and gameplay depth.*

**Total Cards & Items:** 37 unique entries
**Last Updated:** Implementation Version 1.0
**Maintained by:** Librium Development Team