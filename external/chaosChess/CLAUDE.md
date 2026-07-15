# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
## Overall Vision

What if this could be a rogue like of some sorts. You build your deck of QUP's (quantumly unstable pieces), TUPs, and SUPs. You pick upgrades along that way, as you beat chess bosses. Like the bosses are legendary chess players and they also have the ability to destabilize their pieces. Upgrades can be like: pawns get a 15% increase to a chance of disappearing, or decrease, same with other pieces. temporal glitch: knights jump weirdly now or something. It's random but it brings strategy into it. It can be based off of Balatro, different bosses, different starter deck.

## Project Overview

ChaosChess is a Quantum Temporal Chess implementation with three variants:

1. **HTML/JavaScript** - Complete web-based implementation (`index.html`)
2. **Python CLI** - Interactive terminal version (`quantumChess.py`) 
3. **JavaScript modules** - Component files (`main.js`, `chess.js`, `quantum.js`)

The game implements three types of "instabilities" that randomly affect pieces:
- **Quantum**: Pieces vanish into "limbo" and may reappear later
- **Spatial**: Pieces teleport to random empty squares
- **Temporal**: Moves are scheduled to execute in future turns

## Architecture

### Web Implementation (index.html)
- Self-contained HTML file with embedded CSS and JavaScript
- `TinyChess` class: Basic chess engine with move validation
- `ChaosEngine` class: Handles quantum instabilities and effects
- Canvas-based rendering with piece sprites and visual effects
- Error handling for browser extension conflicts (MetaMask)

### Python Implementation (quantumChess.py)
- Uses `python-chess` library for chess logic
- `InstabilityEngine` class: Manages quantum effects and game state
- Interactive CLI with SAN/UCI move parsing
- Limbo and temporal queue data structures

    ## Changes
    - Use pygame to create the visual. make solid colors for the pieces.
    - Added sequential event processing system with 800ms delays between events
    - Player input blocked during event processing to prevent interference
### Shared Core Logic
All implementations use similar probability tables per piece type:
- Pawns: Higher quantum instability (20%)
- Kings: No instability across all types
- Queens: Lowest non-zero instability
- Configurable minimum limbo turns and temporal delays

## Running the Game

### Web Version
Open `index.html` in a browser - no build step required.

### Python Version
```bash
# Activate virtual environment
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies (if not already installed)
pip install python-chess

# Run the CLI version
python quantumChess.py

# Run the pygame visual version
python pygame_quantum_chess.py
```

### Development Commands
- No package.json or build tools detected
- No formal test suite present
- Python virtual environment already set up in `venv/`

## Key Implementation Details

### Probability System
Each piece type has three instability probabilities defined in `PROB_BY_PIECE` constants. These affect piece behavior before each move.

### State Management
- **Limbo**: Vanished pieces with reappearance chances per turn
- **Temporal Queue**: Scheduled moves with future execution turns, this means there can be multiple pieces of the same special type, there might be 3 bishops on the board or 4 knights.
- **Turn Counter**: Tracks game progression for timing effects

### Canvas Rendering (Web)
- Dual canvas system: board grid + pieces overlay  
- Animation system with flash effects for instabilities
- 80px tile size with Unicode chess symbols

### Pygame Interface Controls
- Click to select pieces and make moves
- ESC to quit, R to reset game
- SPACE to skip event processing (when events are playing)
- Events process sequentially with 800ms delays
- Input blocked during event processing to maintain sequence