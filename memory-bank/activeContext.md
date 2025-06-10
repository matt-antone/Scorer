# Active Context

## Current Focus

- Verifying the new project structure and installation process.
- Ensuring the Pi App launches successfully after dependency and installer fixes.

## Recent Changes

1. **Systemic Implementation Analysis**

   - Identified 5 major systemic issues
   - Created implementation plan
   - Documented in [Common Implementation Patterns](../decisions/common_implementation_patterns.md)
   - Changes tracked in [2024-05-20-systemic-fixes-analysis.md](../changes/2024-05-20-systemic-fixes-analysis.md)

2. **Asset Directory Restructuring**

   - Moved assets to root level for shared access
   - Updated all file references
   - Documented in decision record: [Asset Directory Structure](../decisions/asset_directory_structure.md)
   - Changes tracked in:
     - [2024-05-20-asset-directory-move.md](../changes/2024-05-20-asset-directory-move.md)
     - [2024-05-20-file-reference-updates.md](../changes/2024-05-20-file-reference-updates.md)

3. **Pi App Restructuring**

   - Moved the Pi App into its own directory (`pi_app/`).
   - Moved the state server into its own directory (`state_server/`).
   - Updated the installer script to handle the new structure and refuse to run as root.
   - Updated the Pi App launcher to ensure it runs from the correct directory.

4. **Updated the installer script**

   - Install Homebrew dependencies first and link them correctly.
   - Set up environment variables for ffmpeg.
   - Install all Python dependencies in the Pi App's virtual environment.
   - Build ffpyplayer from source with system libraries.
   - Run Alembic migrations using the Pi App's virtual environment.

5. **Cleaned up and reinstalled all dependencies**
   - The Pi App now launches successfully with no immediate errors.

## Active Decisions

1. **Systemic Implementation Patterns**

   - Decision: [Common Implementation Patterns](../decisions/common_implementation_patterns.md)
   - Status: Planning Phase
   - Impact: Will affect all screen implementations

2. **Asset Management**

   - Decision: [Asset Directory Structure](../decisions/asset_directory_structure.md)
   - Status: Implemented
   - Impact: Improved asset sharing and maintenance

3. **Installer Script**

   - Decision: The installer script now refuses to run as root to avoid permission issues with Homebrew and Python dependencies.
   - Status: Implemented
   - Impact: Ensures correct dependencies are installed and avoids permission issues.

4. **Alembic Migrations**

   - Decision: Alembic migrations are run using the correct config path (`state_server/db/alembic.ini`).
   - Status: Implemented
   - Impact: Ensures correct database migrations are applied.

5. **Pi App Launcher**

   - Decision: The Pi App launcher is updated to ensure it runs from the correct directory.
   - Status: Implemented
   - Impact: Ensures correct execution paths and dependencies are met.

6. **All dependencies and migrations are now managed from the Pi App's environment for consistency**

7. **Homebrew and Python dependencies are never installed as root**

## Next Steps

1. **Foundation Implementation**

   - [ ] Create `GameState` class
   - [ ] Implement `BaseScreen`
   - [ ] Create validation framework
   - [ ] Add lifecycle hooks

2. **Component Development**

   - [ ] Create standard widgets
   - [ ] Implement error handling
   - [ ] Add state persistence
   - [ ] Create UI patterns

3. **Integration Planning**

   - [ ] Plan screen updates
   - [ ] Design documentation validation
   - [ ] Plan feature flags
   - [ ] Create sync checks

4. **Testing**

   - [ ] Test the Pi App to ensure everything works as expected.
   - [ ] Verify the database setup and migrations.

5. **Documentation**

   - Following new decision and change record rules
   - Maintaining cross-references
   - Tracking all changes
   - Ensuring consistency

6. **Project Documentation**
   - [ ] Update project documentation to reflect the new structure and installation process.

## Current Considerations

1. **Implementation Order**

   - Foundation first
   - Components second
   - Integration last
   - Documentation throughout

2. **Documentation**

   - Following new decision and change record rules
   - Maintaining cross-references
   - Tracking all changes
   - Ensuring consistency

3. **Code Organization**
   - Maintaining clean architecture
   - Following established patterns
   - Ensuring proper separation of concerns
   - Documenting all decisions

## Cross-References

- [Project Brief](projectbrief.md)
- [Product Context](productContext.md)
- [System Patterns](systemPatterns.md)
- [Tech Context](techContext.md)
- [Progress](progress.md)
- [Decision Records](../decisions/)
- [Change Records](../changes/)
- [Rules](../rules/)
