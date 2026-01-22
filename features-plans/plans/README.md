# Agent Plans Directory

This directory stores implementation plans created by the Planning Agent and used by execution agents.

## Purpose

Plans bridge the gap between requirements and implementation:

```
User Request → Planning Agent → Plan Document → Execution Agents → Implementation
```

## Workflow

### 1. Create a Plan
```
User: "Plan the implementation of [feature]"
Planning Agent: Creates .agents/.plans/PLAN-XXX-feature-name.md
```

### 2. Review & Approve
```
User: Reviews the plan, requests changes or approves
Planning Agent: Updates plan to "Ready" status
```

### 3. Execute the Plan
```
User: "Execute PLAN-XXX"
Execution Agents: Read the plan, execute tasks phase by phase
Planning Agent: Updates execution log
```

### 4. Validate & Complete
```
QA Agent: Validates implementation against success criteria
Review Agent: Code review
Planning Agent: Marks plan as "Completed"
```

## File Naming

```
PLAN-XXX-descriptive-name.md
```

Examples:
- `PLAN-001-user-authentication.md`
- `PLAN-002-api-rate-limiting.md`
- `PLAN-003-dark-mode-implementation.md`

## Plan Statuses

| Status | Meaning |
|--------|---------|
| **Draft** | Plan is being created, not ready for execution |
| **Ready** | Plan is approved, ready to execute |
| **In Progress** | Agents are currently executing the plan |
| **Completed** | All tasks done, success criteria met |
| **Blocked** | Waiting on dependency or decision |
| **Cancelled** | Plan abandoned (document why in Notes) |

## Directory Structure

```
.agents/.plans/
├── README.md                           # This file
├── PLAN-TEMPLATE.md                    # Template for new plans
├── active/                             # Plans currently in progress
│   └── PLAN-XXX-current-work.md
├── completed/                          # Finished plans (archive)
│   └── PLAN-XXX-done-feature.md
└── drafts/                             # Plans being developed
    └── PLAN-XXX-planning.md
```

## Using Plans with Agents

### For Planning Agent
```
When asked to plan a feature:
1. Copy PLAN-TEMPLATE.md
2. Fill in all sections
3. Set status to "Draft"
4. Present to user for review
5. Update to "Ready" when approved
```

### For Execution Agents
```
When asked to execute a plan:
1. Read the full plan document
2. Execute your assigned phase
3. Check off completed tasks
4. Add to execution log
5. Report blockers immediately
```

### For QA/Review Agents
```
When validating a plan:
1. Read success criteria
2. Verify each criterion is met
3. Review code changes
4. Report issues or approve
```

## Integration with Features

Plans complement the `features/` directory:

| Location | Purpose |
|----------|---------|
| `features/in-progress/FEATURE-XXX.md` | What to build (requirements) |
| `.agents/.plans/PLAN-XXX.md` | How to build it (implementation) |

A feature may have multiple plans:
- `FEATURE-024-Agent-Team-Builder.md` (the what)
- `PLAN-024a-page-structure.md` (how: HTML structure)
- `PLAN-024b-agent-catalog.md` (how: content creation)

## Quick Start

Create a new plan:
```bash
cp .agents/.plans/PLAN-TEMPLATE.md .agents/.plans/PLAN-XXX-your-feature.md
```

Or ask me:
```
"Create a plan for implementing [feature]"
```
