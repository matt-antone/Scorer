# Player Client Screen: Main Interface

## 1. Purpose

The Main Interface is the single, persistent screen for the player client. It provides a simple and direct way for a player to modify their own score and Command Points (CPs) from their personal device, which are then synchronized with the main Kivy application.

## 2. Behavior & Flow

### Initialization

- When a player scans their specific QR code, this interface loads.
- It identifies itself to the server as either Player 1 or Player 2 based on the URL.
- Upon connection, it receives the current game state and populates its display with the correct values for that specific player.

### UI Components & Interaction

- **Player Identification**: A clear label indicates which player this client controls (e.g., "Player 1 Controls").
- **Primary Score Controls**:
  - Displays the player's current primary score.
  - `+` and `-` buttons to modify the score.
- **Secondary Score Controls**:
  - Displays the player's current secondary score.
  - `+` and `-` buttons to modify the score.
- **Command Point (CP) Controls**:
  - Displays the player's current CP.
  - `+` and `-` buttons to modify the CP count.
- **Game Timer Display**: Displays the synchronized value of the main game timer. This is a read-only view. See the [Game Timer System documentation](../../../game_timer.md) for more details.
- **Player Timer Display**: Displays the synchronized value of the player's individual timer. This is a read-only view. See the [Player Timer System documentation](../../../player_timer.md) for more details.

### Data Synchronization

- **Sending Updates**: When a player presses a `+` or `-` button, the client sends a specific event to the WebSocket server (e.g., `update_score` or `update_cp`). The payload includes the player ID, the type of score to modify (primary, secondary, or cp), and the action (increment or decrement).
- **Receiving Updates**: The interface also listens for `game_state_update` events from the server. This is crucial for two reasons:
  1. It keeps the player client in sync if the score is changed on the main Kivy app.
  2. It confirms that the player's own update was received and processed successfully by the server, as the server will broadcast the new state back to all clients after an update.

## 3. Screen Transition

- This is a single-screen interface. It does not transition to other game-related screens. It will remain active from the moment the player connects until the browser tab is closed or the connection is permanently lost.

## 4. Key Implementation Details

- **Minimalism**: The interface is intentionally simple, focusing only on the essential controls to minimize distraction.
- **Player-Specific**: The client is locked to a single player's data. It cannot view or modify the opponent's score.
- **API Events**: The interaction relies on a set of specific WebSocket events designed for player actions, which are distinct from the general `game_state_update` used for broadcasting.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `ScorerRootWidget` (active gameplay), this client screen will be active.
