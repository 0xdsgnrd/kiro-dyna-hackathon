---
description: Automatically log current work session to DEVLOG
---

# Log Session to DEVLOG

## Process

### 1. Analyze Current Conversation
Review the conversation history and extract:
- Tasks completed (code written, features implemented, bugs fixed)
- Technical decisions made
- Challenges encountered and solutions
- Kiro CLI prompts/features used
- Files created or modified
- Time indicators (estimate based on conversation length/complexity)

### 2. Read Current DEVLOG
Read `DEVLOG.md` from project root to understand:
- Existing format and structure
- Current date/week organization
- Last entry date
- Total time logged so far

### 3. Generate Entry
Create a new entry following the existing format with:
- **Date and time** (use current date)
- **Duration estimate** (based on conversation complexity)
- **Tasks completed** (specific and actionable)
- **Technical decisions** (with rationale)
- **Challenges & solutions** (if any encountered)
- **Kiro usage** (which prompts/features were used)
- **Files affected** (created/modified)

### 4. Update DEVLOG
Append the new entry to DEVLOG.md in chronological order, maintaining:
- Consistent formatting
- Proper week/day organization
- Running time totals
- All existing content

### 5. Confirm
Provide brief summary:
- What was logged
- Estimated time added
- New total time (if tracking)
