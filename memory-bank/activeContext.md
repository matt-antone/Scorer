# Active Context

## Current Focus

- Verifying the new project structure and installation process.
- Ensuring the Pi App launches successfully after dependency and installer fixes.
- Fixing critical game round limit bug
- Ensuring proper game end after Round 5
- Implementing and fixing the game over screen functionality
- Ensuring proper game state management across all screens
- Addressing layout and functional issues in all screens

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

6. **Identified bug where game continues beyond standard 5 rounds**

- Game currently allows progression to Round 9, which violates Warhammer 40k rules
- Need to implement proper round limit enforcement

7. **Added game over screen with proper winner calculation and score display**

8. **Fixed game state handling to support both dictionary and object states**

9. **Implemented proper screen transitions after game completion**

10. **Added UI strings for game over screen**

11. **Fixed round limit enforcement to properly end game after round 5**

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

8. **Must enforce 5-round limit as per Warhammer 40k rules**

- Game should end after both players complete their turns in Round 5
- Round counter must not increment beyond 5

9. **Game State Management**

   - Decision: Game state must handle both dictionary and object formats for compatibility
   - Decision: All screens must check state type before accessing properties
   - Decision: Game state must be properly serialized when saving/loading

10. **Screen Transitions**

    - Decision: Game over screen must be registered in screen manager
    - Decision: Each screen must have its own KV file for layout
    - Decision: Screen transitions must be handled through the screen manager

11. **UI Implementation**

    - Decision: All UI strings must be defined in strings.py
    - Decision: KV files must be properly referenced in screen classes
    - Decision: Layout issues must be addressed consistently across all screens

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

7. **Fix round limit enforcement in game state management**

8. **Add validation to prevent round progression beyond 5**

9. **Ensure proper game end transition after Round 5**

10. **Review and fix layout issues in all screens**

    - [ ] Scoreboard screen
    - [ ] Name entry screen
    - [ ] Deployment setup screen
    - [ ] Initiative screen
    - [ ] Resume/New game screen

11. **Address functional issues**

    - [ ] Ensure proper state management in each screen
    - [ ] Fix any remaining navigation issues
    - [ ] Implement proper error handling

12. **Improve user experience**

    - [ ] Add proper feedback for user actions
    - [ ] Ensure consistent styling across screens
    - [ ] Implement proper validation in all input fields

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

## Known Issues

1. **Layout Issues**

   - [ ] Some screens may have inconsistent padding/spacing
   - [ ] Button sizes may need adjustment
   - [ ] Text alignment may need improvement

2. **Functional Issues**

   - [ ] Some screens may need better error handling
   - [ ] State management may need improvement in some screens
   - [ ] Navigation between screens may need refinement

3. **Game State**

   - [ ] Need to ensure consistent state handling across all screens
   - [ ] May need to improve state serialization
   - [ ] Need to handle edge cases better

## Implementation Notes

1. **Screen Implementation**

   - [ ] Each screen must have its own Python class and KV file
   - [ ] Screens must be registered in the screen manager
   - [ ] Screens must handle their own state management

2. **State Management**

   - [ ] Game state must be accessible to all screens
   - [ ] State changes must be properly saved
   - [ ] State must be properly loaded when resuming games

3. **UI Guidelines**

   - [ ] Use consistent styling across all screens
   - [ ] Follow the established color scheme
   - [ ] Use proper spacing and padding
   - [ ] Ensure text is readable and properly aligned
