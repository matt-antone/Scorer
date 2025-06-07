# Screen: First Turn Setup Screen

## 1. Purpose

The `FirstTurnSetupScreen` manages the final roll-off to determine which player takes the first turn of the game. This screen follows the deployment roll-off and is the last step before gameplay begins.

## 2. Behavior & Flow

### Initialization

- The screen prompts the winner of the previous deployment roll-off (the "Attacker") to decide who will roll first for the first turn.
- It presents two buttons: "Player 1 Rolls First" and "Player 2 Rolls First".

### User Interaction & Logic

1.  **Role Choice**: The Attacker chooses which player will roll first by pressing the corresponding button. Let's say Player 1 is chosen to roll first.
2.  **First Roll**: The screen updates. The "Roll" button for Player 1 becomes active. Player 2's "Roll" button is disabled.
3.  **Player 1 Rolls**: Player 1 presses their "Roll" button. Their D6 result is displayed, and their button is disabled. Player 2's "Roll" button now becomes active.
4.  **Player 2 Rolls**: Player 2 presses their "Roll" button. Their D6 result is displayed, and their button is disabled.
5.  **Determine Winner**:
    - The application automatically compares the scores.
    - **If there is a tie**: The process resets. The instructional text reverts to prompting the Attacker to choose who rolls first, and the "Player 1 Rolls First" / "Player 2 Rolls First" buttons reappear.
    - **If there is a clear winner**: The instructional text announces which player won the roll (e.g., "Player 2 Wins!").
6.  **First Turn Decision**: The winner of the roll-off now has the choice to either take the first turn or pass it to their opponent. The screen displays two new buttons: "Take First Turn" and "Pass First Turn".
7.  **Final Selection**: The player makes their choice. A "Start Game" button appears.

## 3. Screen Transition

- Upon pressing the "Start Game" button, the application sets the `game_phase` to `'game_play'` and transitions to the main `ScorerRootWidget`, officially starting the game.

## 4. Key Implementation Details

- **File Location**: `screens/first_turn_setup_screen.py`
- **Consolidated Logic**: This screen's logic was consolidated from a previous implementation where a duplicate class definition in `main.py` caused a `KeyError`. The correct logic now resides entirely within its own file and the `ScorerApp` controller.
- **Controller-Responder Pattern**: Like the previous setup screen, this screen strictly adheres to the Controller-Responder pattern. It delegates all user actions (role choices, rolls, turn decisions) to handler methods in `ScorerApp` and updates its view based on the resulting changes to the central `game_state`.
- **State-Driven Complexity**: This screen manages a more complex sequence of states than the deployment screen (choosing who rolls, rolling, determining the winner, choosing who goes first). This entire flow is managed cleanly by reading from and writing to the `game_state` dictionary, demonstrating the power of a state-driven UI.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.
