# SKYRA Quick Start Guide

## Launch SKYRA

### TUI Mode (Recommended)
```bash
cd ~/projects/skyra
python skyra.py --tui
```

### CLI Mode (Original)
```bash
cd ~/projects/skyra
python skyra.py
```

## What You'll See

```
============================================================
SKYRA - Personal AI Voice Assistant
Phase 1: MCP-Integrated Agent
============================================================

→ Connecting to MCP servers...
✓ Connected to MCP server: filesystem
✓ Connected to MCP server: weather
⚠ BRAVE_API_KEY not set - web search unavailable

✓ Ready with 16 tools from 2 servers
  Connected servers: filesystem, weather

✓ SKYRA initialized: claude-sonnet-4-5

Type 'quit' to exit, 'reset' to clear conversation history.
============================================================
```

## Example Commands

### Basic Conversation
```
You: Hello! What can you help me with?
SKYRA: [Introduces capabilities]
```

### File Operations
```
You: List the files in my Documents folder
SKYRA: 🔧 Using tool: list_directory
       [Shows files]

You: Search for all Python files in my projects directory
SKYRA: 🔧 Using tool: search_files
       [Shows matching files]

You: What's in the README.md file in this directory?
SKYRA: 🔧 Using tool: read_file
       [Shows content]
```

### Weather
```
You: What's the weather forecast for Los Angeles? (34.0522, -118.2437)
SKYRA: 🔧 Using tool: get_forecast
       [Shows detailed forecast]

You: Are there any weather alerts in California?
SKYRA: 🔧 Using tool: get_alerts
       [Shows active alerts]
```

### Multi-Step Tasks
```
You: Find all text files in my Desktop and tell me which one is largest
SKYRA: 🔧 Using tool: search_files
       🔧 Using tool: get_file_info (multiple times)
       [Analyzes and reports]
```

### Special Commands (TUI Mode)
- `/help` - Show help message
- `/tools` - List all available tools
- `/reset` - Clear conversation history
- `Ctrl+T` - Show tools
- `Ctrl+R` - Reset conversation
- `q` or `Ctrl+C` - Quit SKYRA

### Special Commands (CLI Mode)
- `tools` - List all available tools
- `reset` - Clear conversation history
- `quit` - Exit SKYRA

## Adding Brave Search

1. Get API key from https://api.search.brave.com/
2. Add to `.env`:
   ```bash
   echo "BRAVE_API_KEY=your_key_here" >> .env
   ```
3. Restart SKYRA

Now you can ask:
```
You: What's the latest news about AI assistants?
SKYRA: 🔧 Using tool: brave_web_search
       [Shows search results and summary]
```

## Troubleshooting

### "Command not found: node"
Install Node.js from https://nodejs.org/

### "Failed to connect to filesystem"
Make sure you have internet connection for npx to download the server.

### Tools not working
Check that MCP servers connected successfully on startup.

## What SKYRA Can Do Right Now

✅ **File Management**
- Read, write, edit files
- List directories
- Search for files
- Get file information
- Create directories
- Move/rename files

✅ **Weather Information**
- Get forecasts by coordinates
- Check weather alerts by state

✅ **Conversation**
- Natural language interaction
- Multi-turn context
- Tool selection and execution
- Result synthesis

## Next: Phase 2 - Voice

In Phase 2, you'll be able to:
- Say "Hey SKYRA" to activate
- Speak your requests naturally
- Hear SKYRA's responses
- Have hands-free conversations

---

**Need Help?**
- Check `PHASE1_COMPLETE.md` for detailed documentation
- Run `python test_skyra.py` to verify everything works
- See `config/mcp_agent.config.yaml` for settings
