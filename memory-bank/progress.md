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
- **First Turn Setup**: The `FirstTurnSetupScreen` is now stable. A `KeyError` crash was resolved by eliminating a duplicate class definition and ensuring the correct logic for determining the first player is used.

## What's Left to Build

- Finalize UI elements for touch interaction on the Raspberry Pi.
- Add "New Game" and "Exit" functionality to the Game Over screen.
- Conduct a full regression test of all game logic paths.

## Current Status

- **Overall:** The project is successfully deployed and stable on the target Raspberry Pi hardware. The core features are complete and the installation process is automated and reliable.
- **Focus:** The current focus is on completing this memory bank documentation update cycle before moving on to new feature development.

## Known Issues

- **None**: All major bugs related to installation, game state, UI initialization, QR code display, and game setup flow have been resolved.

## Blockers

- There are no active blockers.

## Next Steps

- Perform final testing on the Raspberry Pi to ensure touch interactions are smooth.
- Add "New Game" and "Exit" functionality to the Game Over screen.
- Document the "New Game" and "Exit" features in `productContext.md`.
