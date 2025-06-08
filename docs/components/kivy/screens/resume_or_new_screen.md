# Resume or New Game Screen

# Version History

- v1.0.0 (2024-03-21): Initial version
- v2.0.0 (2024-07-29): Reconciled with detailed behavior documentation.

Last Updated: 2024-07-29 10:00 UTC

# Related Files

- [../app.md](../app.md): Main Kivy application
- [splash_screen.md](./splash_screen.md): Previous screen
- [name_entry_screen.md](./name_entry_screen.md): Next screen for new game
- [scorer_root_widget.md](./scorer_root_widget.md): Next screen for resume
- [../../api/state_server/state_management.md](../../api/state_server/state_management.md): State management API

# Overview

The `ResumeOrNewScreen` acts as a conditional gateway in the application's startup flow. Its sole purpose is to appear if, and only if, a meaningful, in-progress game state is found in `game_state.json` upon application launch. It presents the user with a clear choice: continue the previous game or discard it and start a new one.

# Purpose

- Conditionally appear at startup if a valid saved game is found.
- Offer a clear choice to "Resume Game" or "Start New Game".
- Handle the loading of the previous game state or discard it.
- Transition to the appropriate screen based on user choice.

# Properties

- `resume_info_label`: A label to display a summary of the saved game state.
- `resume_button`: A button to resume the saved game.
- `new_game_button`: A button to start a new game.
- `error_label`: A label to display any errors during state loading.

# Methods

- `on_enter()`: Handles screen entry. Checks for saved game data and updates the `resume_info_label`.
- `resume_game_action()`: Handles the "Resume Game" button press, transitioning to `ScorerRootWidget`.
- `start_new_game_from_resume_screen_action()`: Handles the "Start New Game" button press, transitioning to `NameEntryScreen`.
- `handle_error(error)`: Handles and displays errors.

# Events

- `on_resume_selected`: Fired when the "Resume Game" button is pressed.
- `on_new_game_selected`: Fired when the "Start New Game" button is pressed.

# Behavior & Flow

## Appearance Condition

- This screen is **not** always shown.
- During the startup sequence, `ScorerApp.load_game_state()` is called.
- If the loaded state represents a valid, non-initial game (e.g., the `game_phase` is not `'setup'`), the `ScreenManager` is directed to this screen.
- If no saved game exists or the saved game is in a setup phase, this screen is skipped entirely, and the flow proceeds directly to the `NameEntryScreen`.

## User Interaction

- The screen presents two distinct, clearly labeled buttons:
  - **"Resume Game"**: Choosing this option instructs the application to use the loaded `game_state` and transition directly to the main game interface (`ScorerRootWidget`).
  - **"Start New Game"**: Choosing this option discards the loaded `game_state` and transitions to the standard new game flow, starting with the `NameEntryScreen`.

# Screen Transition

- **On "Resume Game"**:
  - The `game_phase` is set to `'game_play'`.
  - The screen transitions to `ScorerRootWidget`.
  - The UI on `ScorerRootWidget` is then populated with the data from the loaded `game_state`.
- **On "Start New Game"**:
  - The screen transitions to `NameEntryScreen`, initiating the same sequence as if no saved game had been found.

# Key Implementation Details

- **File Location**: `screens/resume_or_new_screen.py`
- **Robust Initialization**: This screen uses the robust widget initialization pattern (binding to `ObjectProperty` changes) to prevent race conditions. This ensures that the buttons are fully loaded and ready before any `on_enter` logic attempts to access them, preventing potential `AttributeError` crashes.
- **Controller Logic**: The decision to show this screen and the handling of the user's choice are managed by the main `ScorerApp` class, reinforcing the Controller-Responder pattern.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.

# Changelog

## 2024-07-29

- Reconciled developer-focused documentation with user-facing behavioral documentation.
- Integrated detailed `Behavior & Flow` and `Key Implementation Details`.
- Clarified `Properties`, `Methods`, and `Events` to match the implementation.

## 2024-03-21

- Initial documentation
- Added overview, properties, methods, and flow
- Added saved game loading
- Added resume functionality
- Added new game handling
- Added error handling
- Linked related API documentation
- Synchronized with new documentation standard from `docs/screens/kivy-screens/resume_or_new_screen.md`
