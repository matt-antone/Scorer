# Active Context: Scorer

This document outlines the current work focus, recent changes, next steps, and active decisions for the Scorer project.

## 1. Current Work Focus

- Stabilizing the application after a recent revert to an earlier commit.
- Verifying all core Kivy application functionality on macOS, including setup screens, main game interface, scoring, timers, and game state persistence.
- Preparing for the next phase of development, which could involve addressing macOS-specific SDL2 warnings or proceeding with new features.

## 2. Recent Changes & Decisions

- **Project Reverted**: The project was reverted to a commit from before the recent series of `ObjectProperty` binding issues and subsequent complex troubleshooting steps.
- **OS-Specific Graphics Re-applied**: The Python code in `main.py` for OS-specific graphics configuration (fullscreen on Pi, windowed with cursor on macOS) was successfully re-implemented and is functional.
- **Application Stability**: The application is currently launching, the splash screen displays, and navigation through all implemented screens (`NameEntryScreen`, `DeploymentSetupScreen`, `FirstTurnSetupScreen`, `ScorerRootWidget`, `GameOverScreen`) is working on macOS. Core game logic (scoring, CP, timers, round progression, game state saving/loading) is believed to be in its previously functional state.
- **Acknowledged macOS Warnings**: The `objc` class duplication warnings related to SDL2 (from Kivy and `ffpyplayer`) are still present in the console output on macOS. These are noted as a potential source of instability on the development environment but are not currently preventing the application from running.
- **Previous UI Work**: Prior to the revert, significant work had been done on:
  - Implementing the full setup flow (name entry, deployment, first turn).
  - Developing the main scoring screen with player scores, CPs, timers, and round tracking.
  - Implementing game state persistence using `game_state.json`.
  - Redesigning the UI based on SVG/CSS mockups, including font and color scheme updates.
  - Extensive troubleshooting of Kivy `ObjectProperty` bindings and KV language intricacies.
- **Global UI Theme Adopted**: A "Red vs. Blue" two-column visual theme will be applied to all screens, except for the `SplashScreen`. This will typically involve using `assets/background.png` and organizing content into left (red) and right (blue) areas. The "InterBlack" font will be used for key text elements to match the design.

## 3. Next Steps

- Conduct thorough testing of all existing Kivy application features on macOS to confirm the stability and correctness of the reverted state plus the re-applied cursor fix. This includes:
  - Name entry and saving.
  - Deployment initiative rolls and attacker/defender choices.
  - First turn initiative rolls and first turn choices.
  - Main game screen: score updates, CP updates, timer functionality (game timer, player timers), end turn logic, round advancement.
  - Game over screen: correct display of winner and stats.
  - "New Game" functionality from all relevant points.
  - Game state saving on exit and loading on startup.
- Based on testing, decide on the next immediate development priority:
  - Option A: Attempt to resolve the `objc` SDL2 duplication warnings on macOS to improve development environment stability.
  - Option B: Proceed with new feature development (e.g., Flask web server integration) if the current stability is deemed sufficient for now.

## 4. Active Questions & Considerations

- What is the most effective and least disruptive way to address the SDL2 duplication warnings on macOS, if chosen as the next step?
- Confirm that all UI elements and logic from the more recent (pre-revert) UI redesign efforts are satisfactory in the current reverted state or identify any desired elements to reintegrate carefully.
- Plan for the Flask web server implementation, including API design and Kivy-Flask communication.
