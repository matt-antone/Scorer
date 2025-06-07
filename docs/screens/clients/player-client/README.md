# Player Web Client Documentation

This document serves as an index for the documentation of the player web client. This client provides an interface for a specific player to follow the game state and, when appropriate, update their own score and Command Points directly from their mobile device.

It is accessed via a player-specific QR code generated on the Kivy application's `NameEntryScreen`. The client is state-driven, showing different views based on the main application's `game_phase` to ensure the player is always informed of the current game status.

## Screen Index

- [**Splash Screen**](./splash_screen.md): Initial status view shown while the host is on the Kivy splash screen.
- [**Resume or New Screen**](./resume_or_new_screen.md): Informs the player that the host is making a choice.
- [**Name Entry Screen**](./name_entry_screen.md): A non-interactive view to confirm the player's name.
- [**Deployment Setup Screen**](./deployment_setup_screen.md): A non-interactive view of the deployment roll-off.
- [**First Turn Setup Screen**](./first_turn_setup_screen.md): A non-interactive view of the first-turn roll-off.
- [**Main Interface Screen (Scoreboard)**](./main_interface_screen.md): The core interactive screen where a player can increment or decrement their own scores and CPs. This is shown during active gameplay.
- [**Game Over Screen**](./game_over_screen.md): A non-interactive view of the final results.
- [**Screensaver Screen**](./screensaver_screen.md): Informs the player that the host application is idle.
- [**No Connection Screen**](./no_connection_screen.md): A fallback screen shown if the connection to the server is lost.
