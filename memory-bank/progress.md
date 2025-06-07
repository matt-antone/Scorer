# Progress

This document tracks the current working state of the Scorer application, what's left to build, and any known issues.

## What Works

- **Installation**: A fully automated `install.sh` script successfully sets up the entire environment on a fresh Raspberry Pi OS, including correct Python dependencies, FFmpeg, and a custom-built SDL2 with KMS/DRM support. The script is idempotent and handles both initial setup and updates.
- **Game State**: The application uses a robust SQLite database for game state persistence (`db/scorer.db`). The database is automatically created if it doesn't exist.
- **Kivy Backend**: The Kivy application runs correctly on both macOS (for development) and Raspberry Pi (for production) using the appropriate display drivers.
- **Splash Screen**: The application starts with a manual splash screen requiring a user to press a "START" button to proceed, rather than an automatic timer.
- **Name Entry Screen**: The "Continue" button is now always enabled, removing the validation that required users to input names. This simplifies the flow for users who accept the default names.
- **Screensaver**: The application now includes a screensaver that activates after a period of inactivity. It displays a slideshow of images from the `assets/billboards` directory and deactivates upon user interaction, returning to the previous screen. The slideshow order is randomized, and images transition with a slow fade effect.
- **Game Resume Flow**: The `ResumeOrNewScreen` now uses a robust initialization pattern, fixing a race condition and ensuring that saved games can be resumed reliably without crashing.
- **QR Code Display**: QR codes for player and observer clients are now generated and displayed reliably on the `NameEntryScreen`. The system uses a robust loading pattern that prevents race conditions by pre-caching images and reloading widgets before they are displayed.
- **First Turn Setup**: The `FirstTurnSetupScreen` is now stable. A `KeyError` crash was resolved by eliminating a duplicate class definition and in-sourcing the correct logic for determining the first player is used.
- **Game Over Screen**: The game over screen now correctly displays final stats and includes "New Game" and "Exit" buttons with fully implemented functionality.
- **UI Stability**: Fixed a bug where button text would disappear when a button was disabled. This was resolved by explicitly setting the `disabled_color` in the widget style.
- **Dependency Stability (macOS)**: Resolved a major dependency conflict between Kivy and ffpyplayer. By building `ffpyplayer` from source against a compatible version of `ffmpeg` (`ffmpeg@6`), we have eliminated runtime warnings about duplicate SDL2 libraries, which has fixed application instability and visual artifacts.
- **Documentation**:
  - **Game Timer**: Completed documentation for a timestamp-based main game timer (`docs/game_timer.md`).
  - **Player Timers**: Completed documentation for a timestamp-based "chess-clock" style player timer system (`docs/player_timer.md`).
  - **Client-Driven Setup**: Completed a major documentation overhaul for a new interactive setup flow where players can enter names and roll for deployment from their own devices.

## What's Left to Build

- **Client-Driven Setup Implementation**: Implement the new interactive setup flow as per the updated documentation.
- **Timer Implementation**: Implement the main game timer and player timer systems according to the new documentation.
- add a button both player's scoreboard that pops up their qr code. use an approriate icon
- we need to add events to the player client that match the games status. we will be adding interface for rolling screens and names screen
- Finalize UI elements for touch interaction on the Raspberry Pi.
- Conduct a full regression test of all game logic paths.

## Current Status

- **Overall:** The project is successfully deployed and stable on the target Raspberry Pi hardware. The core features are complete and the installation process is automated and reliable. The macOS development environment is now also stable after significant dependency troubleshooting.
- **Focus:** The documentation phase for the timer systems and the new interactive setup flow is complete. The next focus is implementing these features.

## Known Issues

- **None**: All major bugs related to installation, game state, UI initialization, QR code display, game setup flow, and dependency conflicts have been resolved.

## Blockers

- There are no active blockers.

## Next Steps

- Implement the new client-driven setup flow.
- Implement the game and player timer systems as per the new documentation.
- Perform final testing on the Raspberry Pi to ensure touch interactions are smooth.
- Add "New Game" and "Exit" functionality to the Game Over screen.
- Document the "New Game" and "Exit" features in `productContext.md`.
