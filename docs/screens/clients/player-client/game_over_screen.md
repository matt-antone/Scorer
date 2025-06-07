# Player Client Screen: Game Over

## 1. Purpose

To inform the player that the game has ended, show them the final results, and provide the option to start a new game.

## 2. Behavior & Flow

### Appearance Condition

- This screen is shown when the `game_phase` is `'game_over'`.
- It displays the final scores for both players.
- It shows a clear message declaring the winner (e.g., "You Win!", "You Lose!", or "Draw!").

### UI Components & Interaction

- **Final Scores**: Displays the final scores for both players.
- **Winner Declaration**: Personalized message showing the outcome for this player.
- **"New Game" Button**:
  - Allows the player to start a new game.
  - When pressed, sends a request to the server to start a new game.
  - The server will broadcast the new game state to all clients.
- **Status Message**: Shows "Waiting for other players..." when waiting for the new game to start.

### Game Logic Flow

1. **New Game Initiation**:

   - When a player presses "New Game":
     - The request is sent to the server
     - The server processes the request
     - All clients are notified of the new game state
     - The game cycle restarts for all players

2. **Real-time Updates**:
   - The interface listens for `game_state_update` events
   - Updates are processed immediately to reflect:
     - New game state changes
     - Other players' actions

## 3. Screen Transition

- This screen remains visible until a new game is started.
- When a new game begins (either from this client or another), the client will transition to the **Splash Screen** to restart the cycle.

## 4. Key Implementation Details

- **File Location**: `client/src/screens/GameOverScreen.js`
- **Interactive**: Unlike the observer client, this screen has the "New Game" button for player interaction.
- **State-Driven**: The screen's visibility is controlled by the `game_phase` property in the game state.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `GameOverScreen`, this client screen will be active.
