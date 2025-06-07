# Observer Client Screen: Screensaver

## 1. Purpose

To inform the observer that the main Kivy application is currently idle and displaying its screensaver.

## 2. Proposal

- **Behavior**: This screen will be shown when the `game_phase` received from the server is `'screensaver'`.
- **UI**:
  - Display a simple, passive message, such as "The Scorer is currently idle." or "Screensaver active."
  - This prevents the observer from thinking the game is still active or that their connection has frozen. It clearly communicates the host system's state.
- **Transition**: When the host touches the Kivy app's screen, deactivating the screensaver, the server will send a new game state (likely `game_phase: 'game_play'`). The client will then automatically transition back to the **Game Play Screen**.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `ScreensaverScreen`, this client screen will be active.
