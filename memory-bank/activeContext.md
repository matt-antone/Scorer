# Active Context: Scorer

This document outlines the current work focus, recent changes, next steps, and active decisions for the Scorer project.

## 1. Current Work Focus

- Thoroughly testing the newly implemented "Resume or New Game" feature flow.
- Confirming overall application stability and UI consistency after recent major feature additions and bug fixes.
- Preparing for user feedback and potentially moving towards Raspberry Pi deployment and testing if macOS stability is satisfactory.

## 2. Recent Changes & Decisions

- **"Resume or New Game" Feature Implemented**:
  - A new screen (`ResumeOrNewScreen`) has been added after the `SplashScreen`.
  - If a valid `game_state.json` is detected, this screen prompts the user to either "Resume Game" or "Start New Game".
  - "Resume Game" loads the existing game state and navigates to the appropriate screen based on `game_phase`.
  - "Start New Game" clears the old state and proceeds to `NameEntryScreen`.
  - If no save file (or an invalid/initial state save file) is found, the app proceeds directly to `NameEntryScreen` (or the appropriate screen for a new game flow) after the splash.
  - `ScorerApp.load_game_state()` was updated to return a boolean indicating if a _meaningful_ (in-progress) save was loaded.
  - `ScorerApp._determine_screen_from_gamestate()` helper method was added to centralize screen determination logic.
  - `ScorerApp.build()` logic was significantly updated to manage this new initial flow.
  - File deletion for `game_state.json` was tested (manual deletion required for out-of-workspace files).
- **Timer and End Turn Button Logic Resolved**:
  - Issues where the timer was running for the inactive player have been fixed; the timer display now correctly reflects only the active player's time.
  - The "End Turn" button visibility is now correctly managed, appearing only for the active player.
  - The "End Turn" button correctly switches turns, updates player states, and advances rounds.
  - Corrected Kivy `ObjectProperty` mapping for `p2_end_turn_button` in `scorer.kv` resolved "widget not ready" issues.
- **Application Structure Corrected**:
  - An `AttributeError` related to `_determine_screen_from_gamestate` was resolved by moving this method, along with `load_game_state` and the main `build` method, into the `ScorerApp` class from `ScorerRootWidget`. This ensures correct `self` context and proper application lifecycle management.
- **Global UI Theme & `ScorerRootWidget` Redesign**:
  - The "Red vs. Blue" two-column theme is active on `ScorerRootWidget` and other new screens (like `ResumeOrNewScreen`).
  - "InterBlack" font is registered and used as specified.
  - The `ScorerRootWidget` uses the new layout based on the HTML/CSS design, with updated KV and Python `ObjectProperty` bindings.
- **General Stability**: The application is significantly more stable and feature-complete regarding the core Kivy GUI operations. The main game loop, setup screens, and state transitions are functioning as intended on macOS.
- **Acknowledged macOS Warnings**: The `objc` class duplication warnings (SDL2) remain but are not currently blocking development.

## 3. Next Steps

- Conduct comprehensive testing of the "Resume or New Game" flow under various conditions:
  - No save file present.
  - Save file from an early game phase (e.g., `deployment_setup`).
  - Save file from mid-game (`playing` phase).
  - Save file from `game_over` phase.
- Verify game state persistence and timer states when resuming games.
- Gather user feedback on the current feature set and UI.
- Depending on feedback and stability, prepare for initial testing on the Raspberry Pi.

## 4. Active Questions & Considerations

- Are there any edge cases in the "Resume or New Game" logic that need further refinement?
- Is the current state sufficiently stable to begin Raspberry Pi deployment and testing?
- Revisit Flask web server integration planning once Kivy app stability is fully confirmed on target hardware.
