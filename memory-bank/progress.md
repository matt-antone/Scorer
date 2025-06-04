# Progress: Scorer

This document tracks what works, what's left to build, current status, and known issues for Scorer.

## 1. Current Status

- **Phase**: Kivy GUI Development & Refinement (Post-Revert Stabilization)
- **Overall Progress**: ~60% (Core Kivy app logic and UI for setup and main game are largely implemented and were functional. Currently verifying stability after a revert and targeted fix. Web server and Dicer integration are pending.)
- **Last Update**: [Current Date] - Project reverted to an earlier commit to resolve persistent `ObjectProperty` binding issues. OS-specific cursor/fullscreen behavior re-implemented successfully. Application is launching and navigable.

## 2. What Works (Based on the state reverted to, plus re-applied fixes)

- **Core Application Structure**:
  - Splash screen display.
  - Multi-screen management (`ScreenManager`).
  - OS-specific graphics configuration (fullscreen/cursor).
- **Setup Screens**:
  - `NameEntryScreen`: Allows input and saving of player names.
  - `DeploymentSetupScreen`: Handles dice rolls for deployment initiative, allows winner to choose Attacker/Defender.
  - `FirstTurnSetupScreen`: Handles dice rolls for first turn, allows winner/Attacker to decide who takes the first turn.
- **Main Game Screen (`ScorerRootWidget`)**:
  - Displays player names, total scores, command points.
  - Displays current game round and main game timer.
  - Allows incrementing/decrementing scores and command points for both players.
  - "End Turn" functionality, which advances to the next player and increments the round appropriately.
  - Individual player turn timers.
  - Buttons for "New Game" (with confirmation) and "End Game" (leading to GameOverScreen).
- **Game State Management**:
  - `game_state.json` for saving and loading current game progress (scores, CPs, round, active player, timer states).
  - Game state is loaded on startup, allowing resumption.
- **Game Over**:
  - `GameOverScreen` displays the winner and final game statistics.
  - Option to start a new game.
- **Basic UI Theming**:
  - Application of "Inter" font.
  - Dark theme with specified background and element colors.
  - Consistent button styling.
- **Development Environment & Install Scripts**:
  - `requirements.txt` for Python dependencies (macOS focused initially, with considerations for Pi).
  - `install_on_pi.sh` script for automating Raspberry Pi setup (dependencies, venv, desktop launcher).
  - `Scorer.desktop` and `launch_scorer.sh` for Pi execution.

## 3. What's Left to Build (High-Level)

- **Flask Web Application**:
  - API endpoints for game state and player updates.
  - HTML/JS frontend for player viewing and interaction.
  - Kivy-Flask communication bridge.
- **QR Code Integration**:
  - Generation and display in Kivy UI for web access.
- **Dicer AI Detector Integration** (Future Phase).
- **Refinements & Advanced Features**:
  - Address `objc` SDL2 warnings on macOS development environment.
  - Further UI polish based on extended use.
  - Any additional game logic or features identified.
- **Comprehensive Testing on Raspberry Pi**.

## 4. Known Issues

- **macOS SDL2 Warnings**: `objc[...]: Class SDLApplication is implemented in both ...kivy/.dylibs/SDL2 and ...ffpyplayer/.dylibs/libSDL2-2.0.0.dylib` warnings appear in the console on macOS. This indicates a potential conflict between Kivy's and ffpyplayer's bundled SDL2 libraries. While not currently causing crashes, it could lead to instability on the macOS development environment.
- **Post-Revert Verification**: The application state after the revert needs thorough testing to ensure all previously working features are intact and stable with the re-applied cursor fix.
