# Observer Client Screen: Name Entry

## 1. Purpose

To show the observer the player names as they are being entered in real-time on the main Kivy application.

## 2. Proposal

- **Behavior**: This screen will be shown when the `game_phase` is `'name_entry'`. It will listen for game state updates.
- **UI**:
  - Display two columns for "Player 1" and "Player 2".
  - Under each column, display the current name for that player from the `game_state`.
  - As the host types names into the Kivy app, the names on the observer's screen should update in real-time. This provides excellent feedback that the connection is live.
- **Transition**: When the host presses "Continue" on the Kivy app, the client will transition to the **Deployment Setup Screen**.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `NameEntryScreen`, this client screen will be active.
