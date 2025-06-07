# Player Client Screen: First Turn Setup

## 1. Purpose

To show the player the status of the roll-off that determines who takes the first turn.

## 2. Proposal

- **Behavior**: Shown when the `game_phase` is `'first_turn_setup'`.
- **UI**:
  - A non-interactive status screen that mirrors the state of the main Kivy app.
  - It must display clear instructional text that follows the complex flow of this phase, such as:
    - "Waiting for the Attacker to choose who rolls first."
    - "It's your turn to roll."
    - "Waiting for opponent to roll."
    - "You won the roll! Choose whether to take the first turn or pass on the main screen."
- **Transition**: When the host starts the game, the client transitions to the main interactive scoreboard, which is documented in `main_interface_screen.md`.
