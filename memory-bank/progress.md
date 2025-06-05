# Progress: Scorer

This document tracks what works, what's left to build, current status, and known issues for Scorer.

## 1. Current Status

- **Phase**: Kivy GUI Feature Completion, Stability & Robustness
- **Overall Progress**: ~75-80% (Core Kivy app logic, UI for all game phases, resume/new flow, and critical data persistence are implemented and largely stable on macOS. Web server and Dicer integration are pending.)
- **Last Update**: [Current Date] - Splash screen image implemented, macOS window sizing addressed, and critical data persistence for score/CP changes implemented for immediate saves.
- **Identified root cause of KMSDRM issue**: Default SDL2 package lacks KMSDRM support
- **Documented required build steps**: Added detailed configuration parameters

## 2. What Works

- **Core Application Structure**:
  - Splash screen display with custom image (`splash.png`), full-screen.
  - Multi-screen management (`ScreenManager`).
  - OS-specific graphics configuration (fullscreen/cursor for Linux, fixed window for macOS).
  - Correct placement of app lifecycle methods (`build`, `load_game_state`, etc.) in `ScorerApp`.
  - Addressed macOS window sizing to consistently use 800x480 by setting `Window.size` before `App.run()` and `Config.set('resizable', False)`.
- **Setup Screens**:
  - `NameEntryScreen`: Allows input and saving of player names.
  - `DeploymentSetupScreen`: Handles dice rolls for deployment initiative, allows winner to choose Attacker/Defender.
  - `FirstTurnSetupScreen`: Handles dice rolls for first turn, allows winner/Attacker to decide who takes the first turn.
- **Resume or New Game Flow**:
  - `ResumeOrNewScreen`: Appears after splash if a meaningful save file exists.
  - Correctly navigates to resume game (loading state) or start new game (clearing state).
  - Handles scenarios with no save file or initial/invalid save files by proceeding to new game flow.
- **Main Game Screen (`ScorerRootWidget`)**:
  - Redesigned UI based on HTML/CSS mockups, using "InterBlack" font and red/blue theme with background image.
  - Displays player names (with "- Active" suffix for current player), total scores, command points.
  - Displays current game round and main game timer.
  - Individual player turn timers: Timer display updates for the active player.
  - Allows incrementing/decrementing scores (primary) and command points for both players.
  - **"End Turn" functionality**:
    - Buttons appear only for the active player.
    - Correctly switches active player, updates player times, and advances rounds/ends game.
  - **"Concede" functionality**:
    - Allows either player to concede, ending the game and declaring the other player the winner.
    - Game state updated and transitions to `GameOverScreen`.
  - Buttons for "New Game" (starts new game flow) and "Settings" (placeholder, currently exits app).
- **Game State Management**:
  - `game_state.json` for saving and loading current game progress.
  - Game state is loaded on startup (powering the "Resume or New Game" logic).
  - **Robust data persistence**: Game state saved on app exit, at key phase transitions (e.g., start of game, end of turn, concession), and **immediately after any score or Command Point modification** to prevent data loss.
- **Game Over**:
  - `GameOverScreen` displays the winner (including concession scenarios) and final game statistics.
  - Option to start a new game or exit.
- **UI Theming & Fonts**:
  - Global "Red vs. Blue" theme implemented on relevant screens.
  - "InterBlack" font registered and used for key labels.
  - Consistent button styling (`ScoreboardButton`).
- **Development Environment & Install Scripts**:
  - `requirements.txt` for Python dependencies.
  - Basic Kivy app structure is sound and debuggable on macOS.
  - `.cursorrules` file documents Kivy development patterns.
- **Basic Kivy application structure**
- **SDL2 compilation with KMSDRM support**
- **DRM subsystem configuration**
- **User permissions and group setup**
- **Diagnostic test script for KMSDRM**
- **Display mode detection**
- **DSI display initialization**

## 3. What's Left to Build (High-Level)

- **Thorough Testing & Refinement on macOS**:
  - Comprehensive testing of all features, especially save/load scenarios, immediate save functionality, and edge cases.
- **Raspberry Pi Deployment & Testing**:
  - Deploy current version to Pi and test all features.
  - Address any Pi-specific issues (e.g., performance, touch input, fullscreen behavior).
- **Flask Web Application (Future Phase)**:
  - API endpoints for game state and player updates.
  - HTML/JS frontend for player viewing and interaction.
  - Kivy-Flask communication bridge.
- **QR Code Integration (Future Phase)**:
  - Generation and display in Kivy UI for web access.
- **Dicer AI Detector Integration (Future Phase)**.
- **Refinements & Advanced Features (Potential)**:
  - Secondary score input/tracking.
  - Full implementation of the "Settings" button/screen functionality on `ScorerRootWidget`.
  - Further UI polish based on extended use and Pi testing.
- **Complete KMSDRM support**
- **Finalize display configuration**
- **Optimize performance**
- **Complete documentation**

1. SDL2 with KMSDRM Support:

   - Need to build SDL2 from source
   - Enable KMSDRM support
   - Install required dependencies

2. Display Configuration:
   - Verify DSI display settings
   - Ensure correct CRTC and connector IDs
   - Test display output

## 4. Known Issues

- **macOS SDL2 Warnings**: `objc[...] Class SDLApplication ...` warnings persist on macOS. Not currently blocking, but noted.
- **Settings Button**: The "Settings" button on `ScorerRootWidget` currently exits the app; its intended functionality needs to be designed and implemented. (This is more a placeholder than an issue).
- **KMSDRM Support**
  - **Status**: Investigating
  - **Impact**: High
  - **Current Focus**: Debugging "kmsdrm not available" error
  - **Next Steps**: Run diagnostic tests, verify kernel support
- **DRM Card Selection**
  - **Status**: Pending
  - **Impact**: Medium
  - **Current Focus**: Identifying correct card for display
  - **Next Steps**: Test with different cards, document findings
- **Kernel KMS Support**
  - **Status**: Verifying
  - **Impact**: High
  - **Current Focus**: Confirming KMS is properly enabled
  - **Next Steps**: Check kernel configuration, review logs
- **SDL2 KMSDRM Support**:
  - **Status**: Default SDL2 package lacks KMSDRM support
  - **Impact**: High
  - **Current Focus**: Need to rebuild from source
  - **Next Steps**: Build SDL2 from source with KMSDRM support
- **Display Configuration**:
  - **Status**: VC4 driver reports issues
  - **Impact**: High
  - **Current Focus**: DSI display needs specific settings
  - **Next Steps**: Verify display mode

## 5. Recent Achievements

- **Created comprehensive diagnostic test script**
- **Verified DRM device presence and permissions**
- **Confirmed proper group memberships**
- **Added detailed system diagnostics**

## 6. Next Milestones

1. **Resolve KMSDRM support**
2. **Complete display configuration**
3. **Optimize performance**
4. **Finalize documentation**

## 7. Blockers

- **KMSDRM support not working**
- **Need to verify kernel-level KMS support**
- **May need to adjust SDL2 configuration**

## 8. Notes

- **DRM subsystem appears properly configured**
- **Permissions and groups look correct**
- **Need to verify kernel-level support**
- **May need to adjust SDL2 configuration**

## Next Steps

1. Build SDL2 from source with KMSDRM support
2. Test display output after rebuild
3. Verify KMSDRM functionality
4. Document successful configuration
