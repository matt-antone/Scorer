# Screen: Resume or New Screen

## 1. Purpose

The `ResumeOrNewScreen` acts as a conditional gateway in the application's startup flow. Its sole purpose is to appear if, and only if, a meaningful, in-progress game state is found in `game_state.json` upon application launch. It presents the user with a clear choice: continue the previous game or discard it and start a new one.

## 2. Behavior & Flow

### Appearance Condition

- This screen is **not** always shown.
- During the startup sequence, `ScorerApp.load_game_state()` is called.
- If the loaded state represents a valid, non-initial game (e.g., the `game_phase` is not `'setup'`), the `ScreenManager` is directed to this screen.
- If no saved game exists or the saved game is in a setup phase, this screen is skipped entirely, and the flow proceeds directly to the `NameEntryScreen`.

### User Interaction

- The screen presents two distinct, clearly labeled buttons:
  - **"Resume Game"**: Choosing this option instructs the application to use the loaded `game_state` and transition directly to the main game interface (`ScorerRootWidget`).
  - **"Start New Game"**: Choosing this option discards the loaded `game_state` and transitions to the standard new game flow, starting with the `NameEntryScreen`.

## 3. Screen Transition

- **On "Resume Game"**:
  - The `game_phase` is set to `'game_play'`.
  - The screen transitions to `ScorerRootWidget`.
  - The UI on `ScorerRootWidget` is then populated with the data from the loaded `game_state`.
- **On "Start New Game"**:
  - The screen transitions to `NameEntryScreen`, initiating the same sequence as if no saved game had been found.

## 4. Key Implementation Details

- **File Location**: `screens/resume_or_new_screen.py`
- **Robust Initialization**: This screen uses the robust widget initialization pattern (binding to `ObjectProperty` changes) to prevent race conditions. This ensures that the buttons are fully loaded and ready before any `on_enter` logic attempts to access them, preventing potential `AttributeError` crashes.
- **Controller Logic**: The decision to show this screen and the handling of the user's choice are managed by the main `ScorerApp` class, reinforcing the Controller-Responder pattern.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.
