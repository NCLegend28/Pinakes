# Computer Control Server - Security Design

## Security Principles

### 1. Whitelist-Only
- **No arbitrary command execution**
- Each tool is explicitly coded
- No dynamic shell command construction
- No eval() or exec() of user input

### 2. Read-Mostly Operations
- Prefer read-only operations
- Write operations must be reversible
- No destructive operations without confirmation

### 3. Least Privilege
- Runs as user (no sudo/root)
- Can't access system files
- Limited to user's permissions

### 4. Input Validation
- All inputs validated and sanitized
- Application names validated against system
- Numeric bounds checking (e.g., volume 0-100)

### 5. Audit Trail
- All operations logged
- Timestamps recorded
- Success/failure tracked

---

## Approved Tools (Safe)

### System Information (Read-Only)

#### `get_system_info`
**What it does:** Returns CPU usage, memory usage, disk space
**Risk Level:** 🟢 None (read-only)
**Implementation:** Uses `psutil` library
**Can it harm system?** No - only reads metrics

#### `list_processes`
**What it does:** Lists running processes (name, PID, CPU%, memory%)
**Risk Level:** 🟢 None (read-only)
**Implementation:** Uses `psutil.process_iter()`
**Can it harm system?** No - only lists processes

#### `get_process_info`
**What it does:** Details about specific process by name or PID
**Risk Level:** 🟢 None (read-only)
**Implementation:** Uses `psutil.Process(pid)`
**Can it harm system?** No - only reads info

---

### Application Management

#### `open_application`
**What it does:** Launches macOS application
**Risk Level:** 🟡 Low (launches apps)
**Implementation:** Uses `subprocess.run(['open', '-a', app_name])`
**Validation:**
- Application name validated against `/Applications`
- No path traversal allowed
- No arguments passed to application
**Can it harm system?** Minimal - can only open legitimate apps
**Example:** `open_application("Safari")` ✓, `open_application("../../bad")` ✗

#### `list_applications`
**What it does:** Lists installed applications
**Risk Level:** 🟢 None (read-only)
**Implementation:** Reads `/Applications` directory
**Can it harm system?** No - only lists apps

---

### Window Management

#### `get_active_window`
**What it does:** Gets title and app of currently focused window
**Risk Level:** 🟢 None (read-only)
**Implementation:** Uses macOS AppleScript or similar
**Can it harm system?** No - only reads window info

---

### Media Operations

#### `take_screenshot`
**What it does:** Captures screenshot, saves to file
**Risk Level:** 🟢 None (creates file)
**Implementation:** Uses `screencapture` command
**Validation:**
- Output path must be in user's home directory
- No overwriting system files
**Can it harm system?** No - only saves image file

---

### Audio Control

#### `set_volume`
**What it does:** Sets system volume (0-100)
**Risk Level:** 🟢 None (reversible)
**Implementation:** Uses `osascript` to set volume
**Validation:**
- Input must be 0-100
- Bounds checked
**Can it harm system?** No - easily reversible

#### `get_volume`
**What it does:** Gets current system volume
**Risk Level:** 🟢 None (read-only)
**Implementation:** Uses `osascript` to get volume
**Can it harm system?** No - read-only

---

## Forbidden Tools (Not Implemented)

### ❌ `execute_shell_command`
**Why forbidden:** Arbitrary command execution too dangerous
**Alternative:** Use specific tools instead

### ❌ `kill_process` / `terminate_process`
**Why forbidden:** Could kill critical system processes
**Alternative:** User can do this manually if needed
**Future:** Maybe add with confirmation for user processes only

### ❌ `delete_file` / `remove_directory`
**Why forbidden:** Destructive, irreversible
**Alternative:** Use filesystem MCP server which has safeguards

### ❌ `sudo_command` / `run_as_admin`
**Why forbidden:** Elevated privileges too dangerous
**Alternative:** Never - user does this manually

### ❌ `shutdown` / `restart`
**Why forbidden:** Too disruptive
**Alternative:** User does this manually

### ❌ `network_configure`
**Why forbidden:** Could break connectivity
**Alternative:** Not needed for Phase 1

---

## Implementation Safeguards

### 1. Input Sanitization
```python
def sanitize_app_name(app_name: str) -> str:
    # Remove any path separators
    app_name = app_name.replace('/', '').replace('\\', '')
    # Remove any parent directory references
    app_name = app_name.replace('..', '')
    # Strip whitespace
    app_name = app_name.strip()
    return app_name
```

### 2. Path Validation
```python
def validate_user_path(path: str) -> bool:
    # Must be in user's home directory
    home = os.path.expanduser("~")
    abs_path = os.path.abspath(path)
    return abs_path.startswith(home)
```

### 3. Bounds Checking
```python
def validate_volume(volume: int) -> int:
    return max(0, min(100, volume))
```

### 4. Audit Logging
```python
def log_action(tool_name: str, args: dict, result: str):
    timestamp = datetime.now().isoformat()
    log_entry = f"{timestamp} | {tool_name} | {args} | {result}"
    # Write to logs/computer_control.log
```

---

## Audit Log Format

```
2024-12-08T14:30:15 | open_application | {"app": "Safari"} | SUCCESS
2024-12-08T14:30:45 | get_system_info | {} | SUCCESS
2024-12-08T14:31:00 | set_volume | {"level": 50} | SUCCESS
2024-12-08T14:31:15 | open_application | {"app": "../../etc/passwd"} | REJECTED: Invalid app name
```

---

## Risk Assessment

| Tool | Risk | Reversible | Damage Potential |
|------|------|------------|------------------|
| get_system_info | None | N/A | None |
| list_processes | None | N/A | None |
| get_process_info | None | N/A | None |
| list_applications | None | N/A | None |
| get_active_window | None | N/A | None |
| get_volume | None | N/A | None |
| take_screenshot | Minimal | Yes | None |
| open_application | Low | Yes | Minimal |
| set_volume | Minimal | Yes | None |

**Overall Risk:** 🟢 **LOW** - All operations are safe

---

## Future Enhancements (Phase 2+)

### Potential Additions (with safeguards)
- `close_application` - Close app by name (safe if validated)
- `get_clipboard` - Read clipboard (privacy concern, opt-in)
- `set_clipboard` - Write to clipboard (safe)
- `minimize_window` - Minimize active window (safe)

### Will Never Add
- Arbitrary shell commands
- File deletion
- System modification
- Network configuration
- Privilege escalation

---

## Testing Checklist

Before enabling this server:
- [ ] Test each tool individually
- [ ] Verify input validation works
- [ ] Confirm audit logging works
- [ ] Try malicious inputs (path traversal, injection)
- [ ] Verify nothing runs with elevated privileges
- [ ] Check log file is created and readable

---

## Emergency Procedures

### If Something Goes Wrong

1. **Stop SKYRA:** Press Ctrl+C in terminal
2. **Check logs:** `cat logs/computer_control.log`
3. **Disable server:** Comment out in `skyra.py`
4. **Report issue:** Document in KNOWN_ISSUES.md

### Server Never Has Access To
- Root/sudo privileges
- System files outside user directory
- Network configuration
- Other user accounts
- System kernel/drivers

---

**Reviewed by:** [Your name]
**Date:** [Review date]
**Approved:** [ ] Yes [ ] No [ ] Needs changes
**Notes:** [Any concerns or modifications]
