# Observer Client Screen: Setup

## 1. Purpose

The Setup Screen is the view shown to the observer client whenever the application is in a pre-game state. It provides visual feedback that the game is being configured.

## 2. Behavior & Flow

### Appearance Condition

- This screen is displayed automatically by the central client controller whenever a `game_state_update` event is received from the server and the `game_phase` property in the payload is set to `'setup'`.
- This includes the following application states on the Kivy host:
  - Name Entry Screen
  - Deployment Setup Screen
  - First Turn Setup Screen
  - Resume or New Screen (which the server sanitizes to the `'setup'` phase for clients)

### UI Components

- **Status Text**: Displays a simple message indicating that the game is being set up, for example, "Game Setup in Progress...".
- **Player Name Display**:
  - As players enter their names on the `NameEntryScreen` in the Kivy app, this screen will update in real-time to show the entered names under "Player 1" and "Player 2".
  - This provides immediate feedback that the connection to the server is live and that the game is proceeding.

### State Updates

- The screen subscribes to `game_state_update` events.
- With each new event, it will refresh the player names to reflect the latest state from the server.

## 3. Screen Transition

- The screen remains visible as long as the `game_phase` is `'setup'`.
- When the game officially begins, the server will send a new state with `game_phase: 'game_play'`, at which point the central client controller will automatically hide this screen and show the **Game Play Screen**.

## 4. Key Implementation Details

- **State-Driven**: This screen does not contain any logic for its own visibility. It is shown or hidden entirely based on the `game_phase` managed by the central controller.
- **Real-time Feedback**: Displaying the player names as they are typed is a key UX feature that confirms to the observer that the system is working correctly before the game even starts.
