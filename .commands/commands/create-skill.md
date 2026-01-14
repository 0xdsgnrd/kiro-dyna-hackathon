---
description: "Create a new skill for AI agents using meta-skill-creator"
---

# Create Skill: $ARGUMENTS

Create a new skill that extends AI agent capabilities with specialized knowledge, workflows, or tool integrations.

## Arguments

`$ARGUMENTS` should be the skill name in hyphen-case (e.g., `pdf-editor`, `api-helper`, `brand-guidelines`).

If no arguments provided, ask the user for:
1. Skill name (hyphen-case, e.g., `my-new-skill`)
2. Brief description of what the skill should do

## Process

### Step 1: Understand the Skill

Before creating, gather context:
- What functionality should this skill support?
- What are concrete examples of how it will be used?
- What would a user say that should trigger this skill?

Ask clarifying questions if the purpose is unclear.

### Step 2: Plan Reusable Contents

Analyze what resources the skill needs:
- **scripts/**: Executable code for tasks that require deterministic reliability
- **references/**: Documentation loaded into context as needed (schemas, guides, patterns)
- **assets/**: Files used in output (templates, images, boilerplate)

### Step 3: Initialize the Skill

Run the initialization script:
```bash
python meta-skill-creator/scripts/init_skill.py "$ARGUMENTS" --path ./skills
```

This creates:
- `skills/$ARGUMENTS/SKILL.md` - Main skill file with template
- `skills/$ARGUMENTS/scripts/example.py` - Example script
- `skills/$ARGUMENTS/references/api_reference.md` - Example reference
- `skills/$ARGUMENTS/assets/example_asset.txt` - Example asset

### Step 4: Edit the Skill

Update the generated SKILL.md:

1. **Frontmatter** - Complete the description:
   ```yaml
   ---
   name: $ARGUMENTS
   description: [Complete description of what skill does AND when to use it]
   ---
   ```

2. **Body** - Choose appropriate structure:
   - **Workflow-Based**: For sequential processes
   - **Task-Based**: For tool collections
   - **Reference/Guidelines**: For standards or specifications
   - **Capabilities-Based**: For integrated systems

3. **Resources** - Add/customize scripts, references, assets as needed

4. **Clean up** - Delete unused example files

### Step 5: Validate the Skill

Run validation:
```bash
python meta-skill-creator/scripts/quick_validate.py ./skills/$ARGUMENTS
```

Fix any errors before proceeding.

### Step 6: Package (Optional)

If ready for distribution:
```bash
python meta-skill-creator/scripts/package_skill.py ./skills/$ARGUMENTS
```

Creates `$ARGUMENTS.skill` file (zip format).

## Guidelines

### Naming Conventions
- Hyphen-case only: `my-skill-name`
- Lowercase letters, digits, and hyphens
- Max 64 characters
- No leading/trailing hyphens or consecutive hyphens

### Description Best Practices
- Include what the skill does
- Include when to use it (triggers/contexts)
- Max 1024 characters
- No angle brackets

### Keep It Concise
- Context window is shared - only add what the model doesn't know
- SKILL.md body should be under 500 lines
- Use references/ for detailed documentation

## Output

When complete, report:
- Skill location: `./skills/$ARGUMENTS/`
- Files created
- Next steps (edit SKILL.md, add resources, validate)

## Example

`/create-skill pdf-editor`

Creates a skill at `./skills/pdf-editor/` with:
- SKILL.md template ready for PDF manipulation workflows
- Example resource directories
- Validation passing

## Reference

See `meta-skill-creator/SKILL.md` for complete skill creation documentation.
