# Observer Web Client Documentation

This document serves as an index for the documentation of the observer web client's user interface screens. The observer client is a browser-based view that allows spectators to follow the game state in real-time.

The client is designed to be simple and state-driven. A central controller will listen for `game_state_update` events from the server and show the appropriate screen based on the Kivy application's current screen (`game_phase`).

## Screen Index

This list documents the proposed client screens, creating a one-to-one mapping with the main Kivy application's screens.

- [**Splash Screen**](./splash_screen.md): Shown while the host is on the Kivy splash screen.
- [**Resume or New Screen**](./resume_or_new_screen.md): Shown while the host is deciding to resume a game or start a new one.
- [**Name Entry Screen**](./name_entry_screen.md): Shows player names being entered in real-time.
- [**Deployment Setup Screen**](./deployment_setup_screen.md): Mirrors the deployment roll-off.
- [**First Turn Setup Screen**](./first_turn_setup_screen.md): Mirrors the first-turn roll-off.
- [**Game Play Screen (Scoreboard)**](./game_play_screen.md): The main real-time view of the game, mirroring the `ScorerRootWidget`.
- [**Game Over Screen**](./game_over_screen.md): Shows the final results of the game.
- [**Screensaver Screen**](./screensaver_screen.md): Informs the observer that the host application is idle.
- [**No Connection Screen**](./no_connection_screen.md): A fallback screen shown if the connection to the server is lost.

_Note: The legacy `setup_screen.md` is preserved but is superseded by the more specific `name_entry`, `deployment_setup`, and `first_turn_setup` screen documents._
