# Player Client Screen: Game Over

## 1. Purpose

To inform the player that the game has ended and show them the final results.

## 2. Proposal

- **Behavior**: Shown when the `game_phase` is `'game_over'`.
- **UI**:
  - A non-interactive screen.
  - It should display the final scores for both players.
  - It should have a clear message declaring the winner (e.g., "You Win!", "You Lose!", or "Draw!").
  - A message like "Waiting for host to start a new game." should be present.
- **Transition**: When the host starts a new game, the client will transition back to the **Splash Screen** view to restart the cycle.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `GameOverScreen`, this client screen will be active.
