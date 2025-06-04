# Progress: Scorer

This document tracks what works, what's left to build, current status, and known issues for Scorer.

## 1. Current Status

- **Phase**: Kivy GUI Feature Completion & Stability
- **Overall Progress**: ~70% (Core Kivy app logic, UI for setup, main game, and resume/new flow are implemented and largely stable on macOS. Web server and Dicer integration are pending.)
- **Last Update**: [Current Date] - "Resume or New Game" feature fully implemented. Timer logic and "End Turn" button functionality corrected. App structure refined by moving key lifecycle methods to `ScorerApp`.

## 2. What Works

- **Core Application Structure**:
  - Splash screen display.
  - Multi-screen management (`ScreenManager`).
  - OS-specific graphics configuration (fullscreen/cursor).
  - Correct placement of app lifecycle methods (`build`, `load_game_state`, etc.) in `ScorerApp`.
- **Setup Screens**:
  - `NameEntryScreen`: Allows input and saving of player names.
  - `DeploymentSetupScreen`: Handles dice rolls for deployment initiative, allows winner to choose Attacker/Defender.
  - `FirstTurnSetupScreen`: Handles dice rolls for first turn, allows winner/Attacker to decide who takes the first turn.
- **Resume or New Game Flow**:
  - `ResumeOrNewScreen`: Appears after splash if a meaningful save file exists.
  - Correctly navigates to resume game (loading state) or start new game (clearing state).
  - Handles scenarios with no save file or initial/invalid save files by proceeding to new game flow.
- **Main Game Screen (`ScorerRootWidget`)**:
  - Redesigned UI based on HTML/CSS mockups, using "InterBlack" font and red/blue theme.
  - Displays player names (with "- Active" suffix for current player), total scores, command points.
  - Displays current game round and main game timer.
  - Individual player turn timers: **Timer display updates only for the active player.**
  - Allows incrementing/decrementing scores and command points for both players via numpad popup for scores.
  - **"End Turn" functionality**:
    - Buttons appear only for the active player.
    - Correctly switches active player, updates player times, and advances rounds/ends game.
    - `p2_end_turn_button` correctly linked and functional.
  - Buttons for "New Game" (starts new game flow) and "Settings" (placeholder/future use, currently exits app).
- **Game State Management**:
  - `game_state.json` for saving and loading current game progress.
  - Game state is loaded on startup (powering the "Resume or New Game" logic).
  - Game state saved on exit and at key points (e.g., start of game, end of turn - to be fully verified).
- **Game Over**:
  - `GameOverScreen` displays the winner and final game statistics.
  - Option to start a new game or exit.
- **UI Theming & Fonts**:
  - Global "Red vs. Blue" theme implemented on relevant screens (e.g. `ScorerRootWidget`, `ResumeOrNewScreen`).
  - "InterBlack" font registered and used for key labels.
  - Consistent button styling (`ScoreboardButton`).
- **Development Environment & Install Scripts**:
  - `requirements.txt` for Python dependencies.
  - Basic Kivy app structure is sound and debuggable on macOS.

## 3. What's Left to Build (High-Level)

- **Thorough Testing & Refinement on macOS**:
  - Edge cases for "Resume or New Game" (e.g., corrupted save file, different game phases).
  - Confirm save-on-exit and save-at-critical-points robustness.
- **Raspberry Pi Deployment & Testing**:
  - Deploy current version to Pi and test all features.
  - Address any Pi-specific issues.
- **Flask Web Application**:
  - API endpoints for game state and player updates.
  - HTML/JS frontend for player viewing and interaction.
  - Kivy-Flask communication bridge.
- **QR Code Integration**:
  - Generation and display in Kivy UI for web access.
- **Dicer AI Detector Integration** (Future Phase).
- **Refinements & Advanced Features**:
  - Full implementation of the "Settings" button/screen functionality on `ScorerRootWidget`.
  - Further UI polish based on extended use and Pi testing.

## 4. Known Issues

- **macOS SDL2 Warnings**: `objc[...] Class SDLApplication ...` warnings persist on macOS. Not currently blocking, but noted.
- **Save Robustness**: While save/load is working for the resume flow, confirm it triggers robustly at all intended points (e.g. mid-game before an unexpected exit if possible, end of every turn, etc.).
