# Screen: GamePlayScreen

## 1. Purpose

The `GamePlayScreen` is the player client's primary interface during gameplay. It provides a player-specific view and control point, allowing players to modify their own scores and Command Points (CPs) from their personal device, while maintaining synchronization with the main Kivy application.

## 2. Behavior & Flow

### Initialization

- When a player scans their specific QR code, this interface loads.
- It identifies itself to the server as either Player 1 or Player 2 based on the URL.
- Upon connection, it receives the current game state and populates its display with the correct values for that specific player.

### UI Components & Interaction

- **Player Identification**: A clear label indicates which player this client controls (e.g., "Player 1 Controls").
- **Score**:
  - Displays the player's current total score (sum of primary and secondary objectives).
  - Score is displayed as a button that, when pressed, launches a number pad popup.
  - The number pad popup includes:
    - Numeric keypad (0-9)
    - Red "C" button for clearing input
    - Green "OK" button for confirming the new score
  - Always enabled.
  - Internally tracks:
    - Primary objective score
    - Secondary objective score
    - Total score (sum of both)
- **Command Point (CP) Controls**:
  - Displays the player's current CP.
  - Layout: `<button>-<button> CP <button>+<button>`
  - The CP value is displayed between the increment/decrement buttons.
  - Always enabled.
- **End Turn Button**: Available only when it's your turn.
- **Concede Button**:
  - Located at the bottom of the screen.
  - When pressed, launches a custom confirmation popup.
  - The confirmation popup includes:
    - Warning message: "Are you sure you want to concede?"
    - Red "Cancel" button
    - Green "Confirm" button
  - Styled to match the number pad popup design.
  - Always enabled.
- **Game Timer Display**: Displays the synchronized value of the main game timer. This is a read-only view. See the [Game Timer System documentation](../../../game_timer.md) for more details.
- **Player Timer Display**: Displays the synchronized value of the player's individual timer. This is a read-only view. See the [Player Timer System documentation](../../../player_timer.md) for more details.

### Game Logic Flow (Dual Control)

1. **Score and CP Updates**:

   - Changes can be initiated from either this client or the Kivy host
   - The "first press wins" model applies - whichever client initiates the change first, that change is processed
   - All changes are immediately reflected on all clients
   - Controls are only enabled when it's your turn

2. **Turn Management**:

   - The "End Turn" button is only available when it's your turn
   - When pressed, it sends an `end_turn` event to the server
   - The server processes this and broadcasts the new state to all clients
   - Your controls become disabled, and the opponent's controls become enabled

3. **Real-time Updates**:
   - The interface listens for `game_state_update` events from the server
   - Updates are processed immediately to reflect:
     - Score changes from either client
     - Turn changes
     - Round changes
     - Timer updates

## 3. Screen Transition

- This is a single-screen interface. It does not transition to other game-related screens.
- It will remain active from the moment the player connects until:
  - The browser tab is closed
  - The connection is permanently lost
  - The game ends (server sends `game_phase: 'game_over'`)

## 4. Key Implementation Details

- **File Location**: `client/src/screens/MainInterfaceScreen.js`
- **Player-Specific**: The client is locked to a single player's data and controls
- **Dual Control**: While this client can initiate changes, it must respect the "first press wins" model
- **State-Driven**: All UI elements are enabled/disabled based on the current game state
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `ScorerRootWidget`, this client screen will be active.
