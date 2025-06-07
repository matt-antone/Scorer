# Observer Client Screen: Game Play

## 1. Purpose

The Game Play Screen is the primary interface for the observer client. It provides a real-time, read-only view of the main scoreboard, allowing spectators to follow the game's progress from their own devices.

## 2. Behavior & Flow

### Appearance Condition

- This screen is displayed automatically by the central client controller when a `game_state_update` event is received with the `game_phase` property set to `'game_play'`.

### UI Components & Data Synchronization

- This screen is a direct, visual mirror of the `ScorerRootWidget` from the main Kivy application. It displays:
  - **Player Names**
  - **Primary Scores**
  - **Secondary Scores**
  - **Total Scores**
  - **Command Points (CP)**
  - **Current Round**
  - **Active Player Indicator**: The side of the currently active player is visually highlighted.
  - **Game Timer**: The synchronized value of the main game timer. See the [Game Timer System documentation](../../../game_timer.md) for more details.
  - **Player Timers**: The synchronized value of each player's individual timer. See the [Player Timer System documentation](../../../player_timer.md) for more details.
- **Data Flow**: The screen listens for `game_state_update` events broadcast by the WebSocket server. Upon receiving an update, it immediately re-renders all its UI components with the new data from the event payload. This ensures the web view is always synchronized with the main application state.

## 3. Screen Transition

- This screen remains visible for the entire duration of active gameplay.
- When the game ends (after the second player's turn in Round 5), the server will send a new state with `game_phase: 'game_over'`.
- The central client controller will then automatically hide this screen and display the **Game Over Screen**.

## 4. Key Implementation Details

- **Read-Only**: There are no interactive elements on this screen. It is purely for displaying information.
- **Efficiency**: The screen should be designed to update efficiently, re-rendering only the data that has changed, if possible, to ensure a smooth experience.
- **State-Driven**: Like all other client screens, its visibility is controlled exclusively by the central controller based on the `game_phase`.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `ScorerRootWidget`, this client screen will be active.
