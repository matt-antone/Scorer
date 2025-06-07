# Player Client Screen: Splash

## 1. Purpose

To provide initial feedback to a player who has connected to the game while the host is still on the main `SplashScreen`.

## 2. Proposal

- **Behavior**: This screen will be shown if the `game_phase` is `'splash'`.
- **UI**: A very simple, non-interactive screen. It should display a message confirming the connection and indicating the player's identity, for example: "Connected as Player 1. Waiting for host to start the game."
- **Transition**: When the host starts the game and the `game_phase` from the server updates (e.g., to `name_entry`), the client will automatically transition to the **Player Client Name Entry Screen**.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `SplashScreen`, this client screen will be active.
