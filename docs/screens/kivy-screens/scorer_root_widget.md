# Screen: Scorer Root Widget

## 1. Purpose

The `ScorerRootWidget` is the main game interface of the application. It is where the players will spend almost all of their time during a game. It serves as the central dashboard for tracking all critical game information: scores, Command Points (CPs), the current round, and the active player.

## 2. Behavior & Flow

### Initialization

- The screen is divided into the standard "Red vs. Blue" two-column layout for Player 1 and Player 2.
- When the screen appears (either from starting a new game or resuming an old one), its `update_view_from_state()` method is called to populate all UI elements with the correct data from the central `game_state`.

### UI Components & Interaction

- **Player Name Labels**: Displays the names of Player 1 and Player 2.
- **Primary Score**:
  - Displays the current primary score for each player.
  - Has `+` and `-` buttons to increment or decrement the score. The score is capped between 0 and 50.
- **Secondary Score**:
  - Displays the current secondary score for each player.
  - Has `+` and `-` buttons to increment or decrement the score. The score is capped between 0 and 40.
- **Total Score**: A large, prominent label that automatically displays the sum of the primary and secondary scores.
- **Command Points (CP)**:
  - Displays the current CP for each player.
  - Has `+` and `-` buttons to adjust the CP value.
- **Round Tracker**: A central display at the top of the screen shows the current game round (1-5).
- **Active Player Indicator**: The side of the currently active player is visually highlighted to indicate whose turn it is.
- **End Turn Button**: A button at the bottom of the screen allows the current player to end their turn.
- **Settings/Menu Button**: Provides access to application settings or other options (e.g., concede game - future feature).
- **Game Timer**: This screen displays and controls the main game timer. For full details on its behavior and state management, see the [Game Timer System documentation](../../game_timer.md).
- **Player Timers**: This screen displays the individual time elapsed for each player. For details, see the [Player Timer System documentation](../../player_timer.md).

### Game Logic Flow

1.  **Player's Turn**: The active player's side is highlighted. They can adjust their scores and CPs as needed.
2.  **Ending a Turn**: The active player presses the "End Turn" button.
3.  **State Update**: The application updates the `game_state`:
    - The active player switches to the other player.
    - If the second player just finished their turn, the `current_round` is incremented.
4.  **UI Refresh**: The `update_view_from_state()` method is called to reflect the changes (e.g., highlighting the new active player, updating the round counter).
5.  **Game End Condition**: After the second player finishes their turn in Round 5, the application automatically transitions to the `GameOverScreen`. This logic is handled in the `end_turn` method within the `ScorerApp` controller.

## 3. Screen Transition

- **To this screen**: From `FirstTurnSetupScreen` (new game) or `ResumeOrNewScreen` (resumed game).
- **From this screen**: Transitions to `GameOverScreen` when the game ends, or to `ScreensaverScreen` after a period of inactivity.

## 4. Key Implementation Details

- **File Location**: `screens/scorer_root_widget.py`
- **Central Hub**: This is the most complex and interactive screen in the application.
- **Controller-Responder Pattern**: It strictly follows the pattern. All button presses (`+`/`-`/`End Turn`) call handler methods on the `ScorerApp` controller. The `ScorerRootWidget` is then responsible for visually representing the resulting state from the `game_state` dictionary via its `update_view_from_state` method. This keeps the screen's code clean and focused on UI presentation.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.
