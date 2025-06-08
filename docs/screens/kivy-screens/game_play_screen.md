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
  - The UI displays the current total score for each player. This total is the sum of their primary and secondary objective scores, which are tracked internally.
  - The UI provides separate "Primary" and "Secondary" buttons for each player.
  - Pressing either button launches the `NumberPadPopup` to update that specific score type.
- **NumberPadPopup**:
  - **Dynamic Title**: The popup's title clearly indicates which score is being modified (e.g., "Enter the updated Primary score").
  - **Placeholder Value**: The input field shows the _current_ score for that objective as placeholder text (`hint_text`), not as an editable value. This guides the user to enter the new total, not an increment.
  - **Input Behavior**: The user types the new score. The "OK" button confirms the change.
  - **No Change on Close**: If the user dismisses the popup ("OK") without entering a new number, the score is **not** changed. The old value (from the placeholder) is retained. A new value must be explicitly entered.
  - **Layout**: The popup is compact and sized to fit the number pad, positioned on the side of the screen corresponding to the player whose score is being edited.
- **Command Points (CP)**:
  - Displays the current CP for each player.
  - A simple `+` and `-` button layout allows for easy incrementing and decrementing.
- **Round Tracker**: A central header at the top of the screen shows the current game round (1-5) and indicates whose turn it is (e.g., "Player 1's Turn - Round 1").
- **End Turn Button**:
  - This button only appears on the side of the currently active player.
  - It is used to end the current player's turn.
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
