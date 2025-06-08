# Progress

This document tracks the current working state of the Scorer application, what's left to build, and any known issues.

## What Works

- **Installation**: A fully automated `install.sh` script successfully sets up the entire environment on a fresh Raspberry Pi OS, including correct Python dependencies, FFmpeg, and a custom-built SDL2 with KMS/DRM support. The script is idempotent and handles both initial setup and updates.
- **Game State**: The application uses a robust SQLite database for game state persistence (`db/scorer.db`). The database is automatically created if it doesn't exist.
- **Kivy Backend**: The Kivy application runs correctly on both macOS (for development) and Raspberry Pi (for production) using the appropriate display drivers.
- **Game Flow**: The application has a complete and logical flow from start to finish:
  - **Splash Screen**: A manual start screen.
  - **Name Entry Screen**: Simplified with default names.
  - **Initiative Screen**: A functional roll-off where the winner chooses who goes first, and the Attacker breaks ties.
  - **Scoreboard Screen**: The main game interface.
  - **Game Over Screen**: Displays final stats with options to start a new game or exit.
- **Score Entry**: The `NumberPadPopup` for entering scores has been refined:
  - It uses the current score as a placeholder (`hint_text`), requiring the user to input a new value.
  - The title is dynamic to clarify which score is being edited.
  - The layout is compact and streamlined.
  - The score is only updated if a new value is entered.
- **Game Resume Flow**: The `ResumeOrNewScreen` now uses a robust initialization pattern, fixing a race condition and ensuring that saved games can be resumed reliably without crashing.
- **QR Code Display**: QR codes for player and observer clients are now generated and displayed reliably on the `NameEntryScreen`.
- **UI Stability**: Fixed a bug where button text would disappear when a button was disabled. This was resolved by explicitly setting the `disabled_color` in the widget style.
- **Dependency Stability (macOS)**: Resolved a major dependency conflict between Kivy and ffpyplayer. By building `ffpyplayer` from source against a compatible version of `ffmpeg` (`ffmpeg@6`), we have eliminated runtime warnings about duplicate SDL2 libraries, which has fixed application instability and visual artifacts.
- **Documentation**:
  - **Game Timer**: Completed documentation for a timestamp-based main game timer (`docs/game_timer.md`).
  - **Player Timers**: Completed documentation for a timestamp-based "chess-clock" style player timer system (`docs/player_timer.md`).
  - **Client-Driven Setup**: Completed a major documentation overhaul for a new interactive setup flow where players can enter names and roll for deployment from their own devices.

## What's Left to Build

- **Client-Driven Setup and Timers**: While the core Kivy application is feature-complete, the advanced features for client-driven setup and the integrated game timers are documented but not yet implemented.
- Finalize UI elements for touch interaction on the Raspberry Pi.
- Conduct a full regression test of all game logic paths.

## Current Status

- **Overall:** The core Kivy application is functionally complete and stable on both macOS and the target Raspberry Pi hardware. All screens in the game flow are implemented.
- **Focus:** The next major phase will be to implement the documented web client interactivity (setup, timers) and perform final testing.

## Known Issues

- **macOS Environment Sensitivity**: The Kivy windowing system on macOS can be fragile. Because the `install.sh` script manages `SDL2` by installing and then uninstalling it, any other system update or change (e.g., via Homebrew) can break the environment. If the app fails to launch with an `SDL2` error, the solution is to re-run `./install.sh`.

## Blockers

- There are no active blockers.

## Next Steps

- Implement the new client-driven setup flow.
- Implement the game and player timer systems as per the new documentation.
- Perform final testing on the Raspberry Pi to ensure touch interactions are smooth.
- Add "New Game" and "Exit" functionality to the Game Over screen.
- Document the "New Game" and "Exit" features in `productContext.md`.
