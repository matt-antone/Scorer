# Player Client Screen: Screensaver

## 1. Purpose

To inform the player that the main application is currently idle.

## 2. Proposal

- **Behavior**: Shown when the `game_phase` is `'screensaver'`.
- **UI**:
  - A simple, non-interactive status screen.
  - Display a message like "The game is currently idle. Touch the main screen to continue."
  - This prevents the player from thinking their client has disconnected while the game is paused.
- **Transition**: When the host deactivates the screensaver, the client will transition back to the main interactive scoreboard.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `ScreensaverScreen`, this client screen will be active.
