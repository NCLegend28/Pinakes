# Known Issues and Workarounds

## Phase 1 Issues

### 1. Node.js MCP Server EPIPE Errors

**Issue:**
```
Error: write EPIPE
    at afterWriteDispatched (node:internal/stream_base_commons:159:15)
```

**When it happens:**
- After filesystem tool calls complete successfully
- During server cleanup/shutdown
- Appears in terminal as Node.js error

**Impact:**
- ⚠️ **Low** - Tool calls complete successfully before the error
- Error happens during cleanup, not during actual work
- Response is already delivered to user

**Root Cause:**
- Bug in `@modelcontextprotocol/server-filesystem@0.6.x`
- Server tries to write to stdio after pipe is closed
- Race condition in cleanup code

**Workarounds:**
1. ✅ **Ignore it** - Your queries work fine, error is cosmetic
2. ✅ **Error handling added** - Updated mcp_manager.py to catch BrokenPipeError
3. ⏳ **Wait for update** - Package maintainers may fix this

**Status:** Non-blocking, error handling implemented

---

### 2. Brave Search Server Deprecation Warning

**Issue:**
```
npm warn deprecated @modelcontextprotocol/server-brave-search@0.6.2:
Package no longer supported.
```

**When it happens:**
- On server startup when connecting to Brave Search

**Impact:**
- ⚠️ **Low** - Server still works perfectly
- Just a deprecation notice, not a failure

**Root Cause:**
- Package is deprecated but functional
- May need migration to newer search server in future

**Workarounds:**
1. ✅ **Keep using it** - Works fine for Phase 1
2. ⏳ **Future**: Migrate to alternative search server (Phase 3)

**Status:** Working, will need update in future phases

---

### 3. Tilde (~) Path Expansion

**Issue:**
Using `~` in file paths may not work consistently across all tools.

**Example:**
```python
# May not work
list_directory(path="~/Documents")

# Better
list_directory(path="/Users/username/Documents")
```

**Workaround:**
- Use `os.path.expanduser()` in tool arguments
- Agent usually handles this automatically
- If issues arise, use full absolute paths

**Status:** Handled by agent, generally not an issue

---

## Reporting New Issues

Found a bug? Document it here with:
1. **Issue description**
2. **When it happens**
3. **Impact level** (Low/Medium/High)
4. **Workaround** (if any)
5. **Status**

---

## Future Improvements

### Phase 2 Considerations
- Voice pipeline latency optimization
- Audio device selection
- Wake word false positive rate

### Phase 3 Considerations
- OAuth token refresh for Google services
- Home Assistant connection persistence
- Spotify rate limiting

### Phase 4 Considerations
- Vector DB indexing performance
- Memory retrieval relevance tuning
- Conversation history pruning

---

**Last Updated:** December 8, 2024
**Phase:** 1 (The Brain)
