# Screen: InitiativeScreen

## 1. Purpose

The `InitiativeScreen` manages the roll-off to determine which player takes the first turn of the game. It's a simple, direct screen that resolves the final step before gameplay begins.

## 2. Behavior & Flow

### Appearance Condition

- This screen appears after the `NameEntryScreen`.
- Player names are displayed based on the input from the previous screen.

### UI Components & Interaction

- The screen is divided into the standard two-column layout for Player 1 and Player 2.
- **Player Names**: Displays the names of each player.
- **"Roll Die" Buttons**: Each player has an active "Roll Die" button.
- **Roll Displays**: An area next to each player's name to display their D6 result.
- **Status Label**: A central label that provides instructions to the players (e.g., "Roll for Initiative!", "Player 1 Wins!", "[Player Name] to choose who goes first.").
- **Choice Buttons** (Hidden by default):
  - After a winner is determined, a box appears on their side of the screen containing two buttons: one with their name, and one with their opponent's name. This allows them to choose who takes the first turn.
- **"Continue to Game" Button** (Hidden by default): This button appears only after the first turn player has been decided, allowing the game to proceed.

### Interaction Logic

1.  **Initial State**: Both players' "Roll Die" buttons are enabled.

2.  **Rolling**:

    - A player presses their "Roll Die" button.
    - Their dice roll result appears, and their button becomes disabled.
    - The other player can then roll.

3.  **Determining a Winner**:

    - Once both players have rolled, the application compares the results.
    - **Clear Winner**: The player with the higher roll wins. The `status_label` announces the winner. The choice buttons appear on the winner's side.
    - **Tie**: In the event of a tie, the game state's `attacker_player_id` (determined during the off-screen deployment phase) is used to break the tie. The Attacker is declared the winner. The choice buttons appear on the Attacker's side.

4.  **Choosing First Turn**:
    - The winner of the roll-off (or the Attacker in a tie) is presented with the choice.
    - They press the button corresponding to the player they want to go first.
    - Once the choice is made, the choice buttons disappear, the `status_label` confirms who is going first, and the "Continue to Game" button appears.

## 3. Screen Transition

- Upon pressing the "Continue to Game" button, the application transitions to the `ScoreboardScreen` to begin gameplay.

## 4. Key Implementation Details

- **File Location**: `screens/initiative_screen.py`
- **Controller-Responder Pattern**: This screen follows the standard pattern. All button presses delegate to handler methods in the `ScorerApp` controller, which updates the central `game_state`. The `InitiativeScreen` then updates its view based on that new state.
- **Tie-Breaking**: This is a critical rule. The screen's logic must correctly identify the `attacker_player_id` from the `game_state` to resolve tie-breaks.
