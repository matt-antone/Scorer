# Observer Client Screen: Game Over

## 1. Purpose

The Game Over Screen displays the final results of the match to the observer.

## 2. Behavior & Flow

### Appearance Condition

- This screen is displayed automatically by the central client controller when a `game_state_update` event is received with the `game_phase` property set to `'game_over'`.
- This happens immediately after the game ends on the main Kivy application.

### UI Components

- **Final Scores**: Displays the final total scores for both Player 1 and Player 2.
- **Winner Declaration**: A clear message announces the winner or declares a draw, mirroring the result shown on the Kivy `GameOverScreen`.
- **"Waiting for New Game" Message**: A status message informs the observer that the game has concluded and the client is awaiting the start of a new game.

## 3. Screen Transition

- This screen remains visible as long as the `game_phase` is `'game_over'`.
- If the users on the Kivy application choose to start a new game, the server will eventually send a new state with `game_phase: 'setup'`.
- The central client controller will then automatically hide this screen and show the **Setup Screen**, restarting the viewing cycle.

## 4. Key Implementation Details

- **Passive View**: This screen is entirely passive. It simply displays the final state and waits for the server to initiate a new game sequence.
- **State-Driven Visibility**: Its appearance and disappearance are managed entirely by the central controller based on the `game_phase`.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `GameOverScreen`, this client screen will be active.
