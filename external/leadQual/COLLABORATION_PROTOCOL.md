# 🤝 Collaboration Protocol

## Tandem Development: Claude Code + OpenAI Codex

This project is being developed collaboratively by multiple AI assistants. Follow these protocols to avoid conflicts.

## Rules

### 1. ⚠️ NO OVERWRITES WITHOUT REVIEW
- **Never overwrite** files without checking if they've been recently modified
- **Always read files first** before editing
- **Ask for confirmation** if unsure about changes

### 2. 🔍 Check Before You Edit
```bash
# Always check git status first
git status

# Check file modification time
ls -la path/to/file

# Read file before editing
# Use Read tool to verify current state
```

### 3. ✅ Safe Collaboration Patterns

**GOOD:**
- Create new files for new features
- Add comments with your changes: `// Added by Claude Code - 2025-10-21`
- Read entire file before making edits
- Ask user: "I see this file was recently modified. Should I proceed with changes?"

**BAD:**
- Blindly overwriting files without reading
- Assuming file state without checking
- Making changes without communication

### 4. 📢 Communication

When making changes, clearly state:
- **What file** you're modifying
- **Why** you're modifying it
- **What changes** you're making
- **Request review** if file seems recently modified

### 5. 🚨 Conflict Resolution

If you detect a potential conflict:
1. **STOP** - Don't make the change
2. **READ** the current file state
3. **NOTIFY** the user of the conflict
4. **ASK** for direction: "File X appears to have recent changes. How should I proceed?"

## File Ownership (Current)

### Claude Code Completed:
- ✅ `database/schema.sql`
- ✅ `database/seeds/001_industry_templates.sql`
- ✅ `database/SUPABASE_SETUP.md`
- ✅ `saas-platform/` (entire directory - Week 1)
- ✅ `WEEK1_COMPLETE.md`
- ✅ `DEEPSEEK_SUCCESS.md`
- ✅ All existing workflow files

### Available for Collaboration:
- Week 2+ features (authentication, dashboard, widget)
- New components
- New utilities
- Documentation updates

## Git Workflow

### Before Making Changes
```bash
git status                    # Check for uncommitted changes
git log -1 --stat            # See last commit
git diff                     # See current changes
```

### Making Changes
```bash
# 1. Create feature branch (optional but recommended)
git checkout -b feature/your-feature

# 2. Make your changes
# 3. Commit with clear message
git add .
git commit -m "feat: description of changes

- Detail 1
- Detail 2

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: OpenAI Codex <noreply@openai.com>"
```

### Markers in Code

When adding to existing files, use markers:
```typescript
// ============================================================================
// Added by Claude Code - 2025-10-21
// Feature: Multi-tenant authentication
// ============================================================================

// Your code here

// ============================================================================
// End Claude Code Addition
// ============================================================================
```

Or:
```typescript
// ============================================================================
// Added by OpenAI Codex - 2025-10-21
// Feature: Dashboard analytics
// ============================================================================

// Your code here

// ============================================================================
// End OpenAI Codex Addition
// ============================================================================
```

## Communication Protocol

### When Starting Work
1. Check `git status`
2. Check latest commit: `git log -1`
3. Announce: "I'm going to work on [feature X] in [file Y]"
4. Wait for user confirmation if needed

### When Completing Work
1. Summarize changes made
2. List files modified
3. Suggest next steps
4. Hand off cleanly

## Emergency Override

User can override any protocol with explicit instruction:
- "Overwrite file X with Y" - OK to overwrite
- "Force this change" - OK to proceed
- "Merge these changes" - OK to combine

## Status: ACTIVE ✅

This protocol is **ACTIVE** as of 2025-10-21.

All AI assistants working on this project must follow these rules.

---

**Remember**: When in doubt, ASK. Better to ask than to overwrite hours of work.
