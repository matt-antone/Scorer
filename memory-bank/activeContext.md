# Active Context

## Current Focus

- High Priority: Network Check and QR Code Generation in SplashScreen
  - Implement ConnectionManager popup for network issues
  - Properly structure QR code generation for Player 1, Player 2, and Observer
- Fixing missing properties and methods in four screens: DeploymentSetupScreen, GameOverScreen, InitiativeScreen, and NameEntryScreen
- Ensuring all screens have proper state management and validation
- Maintaining documentation-driven development approach

## Recent Changes

- InitiativeScreen and NameEntryScreen have been fixed and tests are passing
- Added state classes for missing screens: ScreensaverState and SettingsState
- Implemented unit tests for both new state classes
- Identified remaining issues in DeploymentSetupScreen and GameOverScreen
- Verified all changes align with documentation and test requirements

## Current Status

- SplashScreen High Priority Issues:
  - Network Check: ❌ Missing ConnectionManager popup
  - QR Code Generation: ❌ Not properly structured for three clients
- InitiativeScreen: ✅ Fixed and passing tests
- NameEntryScreen: ✅ Fixed and passing tests
- DeploymentSetupScreen: ⚠️ Needs fixes for:
  - Missing properties: rolls
  - Missing methods: update_role, add_roll, proceed_to_initiative
  - State management improvements needed
- GameOverScreen: ⚠️ Needs fixes for:
  - Missing properties: scores, final_scores_text
  - KV file duplicate rules
  - State management improvements needed
- Screensaver and Settings screens now have state classes and unit tests
- Graphical (UI) tests are not expected to run reliably on macOS; they should be executed on the Raspberry Pi

## Next Steps

1. Implement ConnectionManager popup for network issues in SplashScreen
2. Restructure QR code generation to properly handle all three client types
3. Manually test the visuals and behavior of each screen on the Raspberry Pi before proceeding with automation
4. Address any visual errors or inconsistencies observed during manual testing
5. Once manual testing is complete, proceed with UI implementation and automation

## Active Decisions

- Prioritize network check and QR code generation in SplashScreen
- Prioritize manual testing to ensure visual and behavioral correctness
- Focus on state logic and unit tests before implementing graphics
- Ensure all screens are fully functional and properly tested

## Current Considerations

- Network connectivity is critical for QR code generation and client connections
- QR codes must be generated for all three client types (Player 1, Player 2, Observer)
- Manual testing is necessary due to visual errors observed in previous runs
- State classes for missing screens are now in place and tested
- Documentation and memory bank files are up to date with current progress
- Screen-specific fixes must align with documentation
- Test requirements drive implementation
- Maintain focus on core functionality
- Ensure proper state management
- Keep error handling consistent

## References

- @/changes/2024-05-20-state-management-design.md
- @/changes/2024-05-20-systemic-fixes-analysis.md
- @/decisions/state_management_design.md
- @/decisions/common_implementation_patterns.md
- @/decisions/2024-06-11-pi-app-structure.md

## 2024-06-12 Progress Update

- All InitiativeScreen tests now pass after fixing:
  - Initiative winner/loser logic
  - Tie handling
  - Added reset_rolls for test compatibility
- All NameEntryScreen tests now pass after fixing:
  - Validation and state properties
  - Ensuring player_names, qr_code, qr_code_valid, qr_code_error, and name_validation are always set in game state
- Next: Proceed to DeploymentSetupScreen and GameOverScreen to fix remaining test failures.

## 2024-06-13: UI Modularization and KV Warning Cleanup

- Consolidated all button styles into `button_styles.kv`.
- Removed all direct `Builder.load_file` calls for button styles from individual screen files.
- `button_styles.kv` is now included only once in `scorer.kv`.
- This resolved duplicate KV/class warnings and ensures maintainability.
- Change aligns with canonical directory structure (see systemPatterns.md).
- Rationale and pattern documented in .cursorrules.

## Pi-only Testing Note

- The network manager and splash screen network check tests are **Pi-only**. These tests require real network interfaces and Kivy UI threading, and are not expected to pass on macOS or CI. This is a permanent project rule.
