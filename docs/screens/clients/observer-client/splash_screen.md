# Observer Client Screen: Splash Screen

## 1. Purpose

This screen provides initial visual feedback to the observer while the main Kivy application is on its `SplashScreen`.

## 2. Proposal

- **Behavior**: This screen should be very simple. It will be shown when the `game_phase` received from the server is `'splash'`.
- **UI**: Display a logo or a simple "Connecting to Scorer..." message. It indicates that the client is connected and waiting for the host to start the game setup.
- **Transition**: When the host presses the "START" button on the Kivy app, the server will send a new game state, and the client will transition to the next appropriate screen (e.g., `Resume or New Screen` or `Name Entry Screen`).
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `SplashScreen`, this client screen will be active.
