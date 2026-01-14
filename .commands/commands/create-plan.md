---
description: "Create an implementation plan for a feature or task"
---

# Create Plan: $ARGUMENTS

Use the planning-skill to create a structured implementation plan for the specified feature or task.

## Process

1. **Create the plan file** using the planning skill script:
   ```bash
   python skills/planning-skill/scripts/create_plan.py "$ARGUMENTS"
   ```

2. **Read the generated plan file** from `.agents/.plans/drafts/`

3. **Fill in all sections** based on:
   - Understanding of the task/feature requirements
   - Existing codebase context from CLAUDE.md
   - Agent roles defined in AGENTS.md
   - Any related feature tickets

4. **Key sections to complete**:
   - Summary: One paragraph explaining what and why
   - Goals: 3-5 measurable outcomes
   - Context: Current state, problem, constraints
   - Implementation Plan: Phased tasks with agent assignments
   - Files to Create/Modify: Specific file changes
   - Success Criteria: How to verify completion

5. **Present the completed plan** for user review

## Guidelines

- Break complex work into 3-5 phases
- Assign each phase to the appropriate agent
- Include a validation phase with QA Agent and Review Agent
- List specific files that will be created or modified
- Define measurable success criteria

## Output

When complete, report:
- Plan file location
- Plan ID and title
- Summary of phases
- Next steps for user (review and approve)

## Example

If invoked as `/create-plan user-authentication`, the output should include:
- Created plan at `.agents/.plans/drafts/PLAN-XXX-user-authentication.md`
- Phases covering: design, implementation, testing, review
- Specific files to be created/modified
- Clear success criteria
