# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based interactive vocabulary bot called "Obscure Word Bot" that helps users discover beautiful, obscure English words. The bot serves up rare words with their definitions, etymologies, pronunciations, and example sentences through an interactive command-line interface.

## Core Architecture

### Main Components

- **ObscureWordBot class** (`obscure_word_bot.py:22-249`): Core bot functionality with word management, search, and interactive features
- **Word dataclass** (`obscure_word_bot.py:12-20`): Data structure representing individual words with all their metadata
- **JSON data store** (`obscure_words.json`): Persistent storage for the word collection

### Key Design Patterns

- **Data persistence**: Words are stored in JSON format and automatically saved when modified
- **Interactive CLI**: Full-featured command interface with user-friendly prompts and error handling
- **Tag-based organization**: Words are categorized with descriptive tags for easy filtering
- **Graceful degradation**: Falls back to default word collection if JSON file is corrupted

## Common Commands

### Running the Bot
```bash
python3 obscure_word_bot.py          # Start interactive session
python -c "from obscure_word_bot import ObscureWordBot; bot = ObscureWordBot(); print(bot.format_word(bot.get_random_word()))"  # Get single random word
```

### Interactive Commands (within the bot)
- `random` or `r` - Get a random word
- `tag <tagname>` - Get a word with specific tag
- `search <query>` - Search for words by content
- `tags` - List all available tags
- `quit` or `q` - Exit the bot

### Development Commands
```bash
python3 -c "import json; print(len(json.load(open('obscure_words.json'))))"  # Count words in collection
python3 -c "from obscure_word_bot import ObscureWordBot; print(', '.join(ObscureWordBot().list_tags()))"  # List all tags
```

## Data Structure

### Word Object Schema
Each word contains:
- `word`: The actual word (string)
- `definition`: Clear, poetic definition (string)
- `pronunciation`: Phonetic pronunciation guide (string)
- `etymology`: Word origin and linguistic history (string)
- `example_sentence`: Contextual usage example (string)
- `tags`: Categorization labels (list of strings)

### Tag Categories
Common tag patterns include:
- **Sensory**: relating to physical sensations
- **Emotional**: describing feelings or psychological states
- **Nature**: connected to natural phenomena
- **Literary/Poetic**: words with artistic or literary associations
- **Historical**: words with significant historical context
- **Linguistic**: technical language terms

## Code Organization

### Main Functions
- `_load_words()`: JSON file loading with error handling
- `_save_words()`: Persistent data storage
- `get_random_word()`: Random word selection
- `get_word_by_tag()`: Tag-filtered word retrieval
- `search_words()`: Full-text search functionality
- `format_word()`: Pretty-printed word display with ASCII art borders
- `interactive_session()`: Main CLI loop with command parsing

### Error Handling
- JSON parsing errors fall back to default word collection
- Invalid commands show helpful usage messages
- Keyboard interrupts are handled gracefully
- File I/O errors are caught and reported

## Development Notes

- The bot initializes with 10 carefully curated default words if no JSON file exists
- Word data is automatically saved after any modifications
- The interactive interface uses Unicode characters for visual appeal
- All string matching is case-insensitive for better usability
- The codebase follows Python dataclass patterns for clean data modeling

## Voice Cloning Project

This directory also contains a voice cloning application that can record audio and clone voices.

### Dependencies Installation

**PyAudio Installation Issues:**
If you encounter `portaudio.h not found` errors when installing PyAudio:

```bash
# macOS (required for audio recording)
brew install portaudio
pip install pyaudio

# Ubuntu/Debian
sudo apt-get install portaudio19-dev
pip install pyaudio
```

See `PYAUDIO_INSTALLATION_GUIDE.md` for comprehensive troubleshooting.

### Voice Cloner Commands

```bash
# Test voice cloning (requires microphone access)
python voice_cloner.py

# CLI interface
python voice_cli.py quick --audio sample.wav --text "Hello world" --output result.wav
python voice_cli.py interactive  # Interactive mode with recording
```

### PyTorch Compatibility

The voice cloner includes a fix for PyTorch 2.6 `weights_only` security changes. The TTS models from Coqui are trusted and safe to load.