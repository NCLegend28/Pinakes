# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Librium is a strategic roguelike ecosystem management game with deckbuilding elements. Players cultivate dynamic ecosystems through contemplative card placement while meeting escalating resource demands across multiple generations. The game combines realistic ecological simulation with jazz-influenced pacing - contemplative planning with moments of frantic adaptation during natural disasters.

**Genre**: Strategic roguelike with deckbuilding elements
**Theme**: Ecosystem management and balance
**Inspiration**: Balatro (synergy mechanics) + Mini Motorways (escalating complexity)
**Philosophy**: No artificial time pressure - tension from ecological balance, not arbitrary constraints

## Core Architecture

### Population Dynamics Engine
- **Population States**: Thriving (150-200% optimal), Stable (80-150%), Stressed (40-79%), Critical (10-39%), Extinct (0-9%)
- **Growth Formula**: `Next_Population = Current_Population + (Food_Available - Food_Required) * Growth_Rate - Environmental_Stress`
- **Trophic Levels**: Primary Producers (Flora), Primary Consumers (Herbivores), Secondary Consumers (Carnivores), Decomposers

### Food Web System
- **Feeding Requirements**:
  - Herbivores: 1.5 flora production (2-hex range)
  - Small Carnivores: 2 herbivore population (2-hex range)  
  - Large Carnivores: 3 herbivore population (3-hex range)
  - Omnivores: Flexible substitution ratios (0.5 flora = 1 herbivore)

### Terrain-Specific Carrying Capacity
- Forest: 3 flora + 2 herbivores + 1 carnivore per hex
- Grassland: 2 flora + 4 herbivores + 1 carnivore per hex
- Wetland: 4 flora + 2 herbivores + 2 carnivores per hex
- Desert: 1 flora + 1 herbivore + 1 carnivore per hex
- Mountain: 1 flora + 1 herbivore + 2 carnivores per hex

### Key Formulas
- **Biomass**: `Hex_Biomass = (Flora_Production * Herbivore_Efficiency * Weather_Modifier) + Carnivore_Bonus`
- **Diversity**: `Ecosystem_Diversity = (Unique_Species_Count * Biome_Variety * Interaction_Complexity) / Total_Hexes`
- **Stability**: `Stability = 100 - (Population_Stress + Overcrowding_Penalty + Food_Web_Gaps + Weather_Vulnerability)`

### Equilibrium Conditions
Perfect equilibrium achieved when:
- `Flora_Production >= (Herbivore_Consumption * 1.2)`
- `Herbivore_Population >= (Carnivore_Consumption * 1.5)`
- `Decomposer_Capacity >= (Total_Death_Rate * 1.1)`
- `Carrying_Capacity_Usage <= 90%`

## Technical Implementation Guidelines

### Performance Optimization
- Use hex-grid based calculation optimization
- Implement population state caching for performance
- Process cascade effects in batches
- Consider synergy calculation parallelization

### Data Structures
- Species population arrays with state tracking
- Terrain type matrices with capacity data
- Food web relationship graphs
- Resource flow calculation pipelines

### Scalability Features
- Modular biome addition support
- Dynamic grid size accommodation
- Extensible species interaction systems
- Configurable balance parameter adjustment

## Simulation Features

### Population Flow Dynamics
- **Migration Types**: Pressure-driven, Opportunity-driven, Disaster-driven, Seasonal
- **Reproductive Cycles**: Fast Breeders (per-turn), Moderate Breeders (2-3 turns), Slow Breeders (3-5 turns)
- **Mortality Factors**: Natural mortality (10-20%), Predation, Starvation, Disease

### Environmental Integration
- **Weather Effects**: Drought, Flood, Cold Snap, Heat Wave
- **Degradation Factors**: Overuse, Monoculture, Fragmentation
- **Synergy Systems**: Adjacent tile bonuses, ecosystem cluster effects, cross-biome synergies

### System States
- **Stable Equilibrium**: Self-correcting, +25% resource bonus, disaster resistance
- **Unstable Equilibrium**: Disturbance-sensitive, standard generation
- **Chaotic State**: Large oscillations, -50% penalty, high extinction risk

## Cascade Systems
- **Positive Feedback Loops**: Overgrazing, Predator loss, Habitat destruction cascades
- **Negative Feedback Loops**: Predation pressure, Resource competition, Migration relief

## Game Systems

### Core Gameplay Loop
1. **Planning Phase**: No time limits, contemplative card placement on hex grid
2. **Resolution Phase**: Ecosystem simulation runs, resources generated
3. **Quota Evaluation**: Meet biomass/diversity/stability requirements
4. **Growth Phase**: Choose expansion, specialization, or resilience paths
5. **Crisis Management**: Survive disasters through ecosystem design

### Card & Deckbuilding Systems
- **4 Card Types**: Terrain, Flora, Fauna, Weather
- **Dynamic Deck Evolution**: Based on successful strategies
- **Rarity Tiers**: Common to legendary keystone species
- **Specialization Paths**: Forest, Grassland, Wetland, Desert themes

### Resource & Progression
- **3 Primary Resources**: Biomass, Diversity, Stability
- **Escalating Quotas**: Across 8-12 generations
- **Multiple Victory Conditions**: Survival, Perfection, Adaptation, Diversity
- **Meta-Progression**: Card unlocks and ecosystem discoveries

## Development Workflow

### AI Tool Integration
- **Programming**: Claude (Python expertise) + GitHub Copilot
- **Game Design**: Claude for mechanics, GPT-4 for narrative
- **Visual Assets**: Midjourney (concept), DALL-E 3 (UI), Stable Diffusion (consistency)
- **Audio**: AIVA (adaptive jazz), Mubert (dynamic nature sounds)
- **Development Platform**: Unity with Unity Muse

### Development Priorities
1. **Card Design System** - Interface between player decisions and ecosystem engine
2. **Disaster Impact Mechanics** - How catastrophes interact with population dynamics
3. **Resource Balancing** - Quota scaling and progression curves
4. **Visual Feedback** - Communicating complex simulation data clearly

## Technical Architecture

### Language & Platform
- **Core Systems**: Python (aligning with user preferences)
- **Game Engine**: Unity for final implementation
- **Architecture**: Hex-grid based for strategic placement
- **Design**: Modular system supporting extensible biomes and species

### System Status
- **Ecosystem Simulation Engine**: ✅ Completed
- **Card & Deckbuilding Systems**: 🔄 Conceptualized
- **Resource & Progression**: 📋 Outlined
- **Visual & Audio Systems**: 📋 Planned