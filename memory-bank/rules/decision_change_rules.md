# Decision and Change Record Rules

## MANDATORY REQUIREMENTS

### When to Create Records

1. **Decision Records MUST be created when:**

   - Making architectural changes
   - Changing project structure
   - Selecting between multiple implementation options
   - Making choices that affect multiple components
   - Implementing new features that require design decisions
   - Changing core functionality
   - Modifying data structures
   - Updating dependencies

2. **Change Records MUST be created when:**
   - Implementing a decision
   - Making file structure changes
   - Updating multiple files
   - Modifying core functionality
   - Changing dependencies
   - Updating documentation
   - Fixing critical bugs
   - Making changes that affect multiple components

### Record Structure

1. **Decision Records MUST include:**

   ```markdown
   # Decision: [Title]

   ## Context

   - Current situation
   - Problems to solve
   - Requirements to meet

   ## Alternatives Considered

   1. **Option 1**
      - Pros
      - Cons
   2. **Option 2**
      - Pros
      - Cons
        [etc.]

   ## Decision

   - Clear statement of chosen solution
   - Implementation details
   - Required changes

   ## Related Changes

   - Links to change records
   - Links to affected components

   ## Verification

   - [ ] Checklist of verification steps
   - [ ] Testing requirements
   - [ ] Documentation updates

   ## Impact

   - Effects on system
   - Effects on components
   - Effects on users

   ## Future Considerations

   - Potential future changes
   - Areas to monitor
   - Possible improvements
   ```

2. **Change Records MUST include:**

   ```markdown
   # Change: [Title]

   ## Date: YYYY-MM-DD

   ## Description

   - What changed
   - Why it changed
   - How it changed

   ## Changes Made

   1. Component 1
      - Specific changes
      - Files modified
   2. Component 2
      - Specific changes
      - Files modified
        [etc.]

   ## Related Decisions

   - Links to decision records
   - Links to related changes

   ## Verification Steps

   1. Step 1
   2. Step 2
      [etc.]

   ## Impact

   - Effects on system
   - Effects on components
   - Effects on users

   ## Notes

   - Additional context
   - Known issues
   - Future considerations
   ```

### File Organization

1. **Decision Records:**

   - Location: `memory-bank/decisions/`
   - Naming: `[topic]_[aspect].md`
   - Example: `asset_directory_structure.md`

2. **Change Records:**
   - Location: `memory-bank/changes/`
   - Naming: `YYYY-MM-DD-[brief-description].md`
   - Example: `2024-05-20-asset-directory-move.md`

### Cross-Referencing

1. **MUST link between:**

   - Decision records and related change records
   - Change records and affected components
   - Active context and recent decisions/changes
   - Progress file and completed changes

2. **MUST update:**
   - Active context when creating new records
   - Progress file when changes are completed
   - System patterns when architecture changes
   - Tech context when dependencies change

### Verification Process

1. **Before Creating Records:**

   - [ ] Read all memory bank files
   - [ ] Check for related decisions/changes
   - [ ] Verify no conflicts
   - [ ] Plan all required updates

2. **After Creating Records:**
   - [ ] Update all cross-references
   - [ ] Verify links work
   - [ ] Check formatting
   - [ ] Update active context
   - [ ] Update progress file

### Maintenance Rules

1. **Regular Updates:**

   - Review decision records quarterly
   - Archive outdated decisions
   - Update related changes
   - Verify all links

2. **Change Management:**
   - Create new records for significant changes
   - Update existing records for minor changes
   - Document all modifications
   - Maintain change history

## NO EXCEPTIONS

These rules MUST be followed for ALL decisions and changes. There are NO EXCEPTIONS to these requirements. This ensures:

- Consistent documentation
- Clear decision history
- Traceable changes
- Maintainable system
- Reliable memory bank
