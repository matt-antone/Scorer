# Observer Client Screen: First Turn Setup

## 1. Purpose

To allow the observer to follow the complex roll-off and decision process for determining which player takes the first turn.

## 2. Proposal

- **Behavior**: This screen will be shown when the `game_phase` is `'first_turn_setup'`. It needs to reflect the multiple steps of this phase.
- **UI**:
  - Display a title, e.g., "First Turn Roll-Off".
  - A status area must clearly show the current state of the process, such as:
    - "Waiting for Attacker to choose who rolls first."
    - "Player 2 is rolling..."
    - "Player 1 won the roll. Waiting for them to decide..."
    - "Player 1 has chosen to take the first turn."
  - It should also display the dice roll results for each player as they happen.
- **Transition**: When the host presses "Start Game" on the Kivy app, the client will transition to the **Game Play Screen**.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `FirstTurnSetupScreen`, this client screen will be active.
