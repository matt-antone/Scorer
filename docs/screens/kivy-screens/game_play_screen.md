# Screen: GamePlayScreen

## 1. Purpose

The `GamePlayScreen` is the main game interface of the application. It serves as both the central control point and a real-time display of the game state. While players can make changes from their web clients, this screen maintains full control over all game elements and provides a complete view of both players' information.

## 2. Behavior & Flow

### Initialization

- The screen is divided into the standard "Red vs. Blue" two-column layout for Player 1 and Player 2.
- When the screen appears (either from starting a new game or resuming an old one), its `update_view_from_state()` method is called to populate all UI elements with the correct data from the central `game_state`.

### UI Components & Interaction

- **Player Name Labels**: Displays the names of Player 1 and Player 2.
- **Score**:
  - Displays the current total score for each player (sum of primary and secondary objectives).
  - Score is displayed as a button that, when pressed, launches a number pad popup.
  - The number pad popup includes:
    - Numeric keypad (0-9)
    - Red "C" button for clearing input
    - Green "OK" button for confirming the new score
  - Always enabled for both players.
  - Internally tracks:
    - Primary objective score
    - Secondary objective score
    - Total score (sum of both)
- **Command Points (CP)**:
  - Displays the current CP for each player.
  - Layout: `<button>-<button> CP <button>+<button>`
  - The CP value is displayed between the increment/decrement buttons.
  - Always enabled for both players.
- **Round Tracker**: A central display at the top of the screen shows the current game round (1-5).
- **Active Player Indicator**: The side of the currently active player is visually highlighted to indicate whose turn it is.
- **End Turn Button**: A button at the bottom of the screen allows the current player to end their turn.
- **Concede Button**:
  - Located at the bottom of the screen.
  - When pressed, launches a custom confirmation popup.
  - The confirmation popup includes:
    - Warning message: "Are you sure you want to concede?"
    - Red "Cancel" button
    - Green "Confirm" button
  - Styled to match the number pad popup design.
  - Always enabled for both players.
- **Game Timer**: This screen displays and controls the main game timer. For full details on its behavior and state management, see the [Game Timer System documentation](../../game_timer.md).
- **Player Timers**: This screen displays the individual time elapsed for each player. For details, see the [Player Timer System documentation](../../player_timer.md).

### Game Logic Flow (Dual Control)

1. **Score and CP Updates**:

   - Changes can be initiated from either this screen or the player's web client
   - The "first press wins" model applies - whichever client initiates the change first, that change is processed
   - All changes are immediately reflected on all clients

2. **Turn Management**:

   - The active player's side is highlighted
   - Only the active player can make changes to their scores and CPs
   - The "End Turn" button can be pressed from either this screen or the active player's web client
   - When a turn ends:
     - The active player switches to the other player
     - If the second player just finished their turn, the `current_round` is incremented
     - The UI refreshes to reflect the changes

3. **Game End Condition**:
   - After the second player finishes their turn in Round 5, the application automatically transitions to the `GameOverScreen`
   - This transition is controlled exclusively by this screen

## 3. Screen Transition

- **To this screen**: From `FirstTurnSetupScreen` (new game) or `ResumeOrNewScreen` (resumed game).
- **From this screen**: Transitions to `GameOverScreen` when the game ends, or to `ScreensaverScreen` after a period of inactivity.

## 4. Key Implementation Details

- **File Location**: `screens/scorer_root_widget.py`
- **Central Hub**: This is the most complex and interactive screen in the application.
- **Controller-Responder Pattern**: It strictly follows the pattern. All button presses (`+`/`-`/`End Turn`) call handler methods on the `ScorerApp` controller. The `ScorerRootWidget` is then responsible for visually representing the resulting state from the `game_state` dictionary via its `update_view_from_state` method.
- **Dual Control**: While this screen maintains full control, it also listens for and processes updates initiated from player web clients.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.
