# Active Context

## Current Focus

The primary focus is ensuring the application is robust and user-friendly on the target Raspberry Pi platform. The immediate past work involved resolving a series of complex bugs related to the Kivy application lifecycle, specifically on the `NameEntryScreen`. A significant amount of effort went into creating a reliable, event-driven initialization pattern to prevent race conditions.

The most recent change was to simplify the user flow on the `NameEntryScreen` by removing the validation logic that required users to enter text before proceeding. The "Continue" button is now always enabled, allowing for faster setup when default player names are acceptable.

## Recent Changes

- **Automated Installation Script (`install.sh`):** Overhauled the installation process into a single, robust script. It now handles system dependencies, Python packages, and programmatically creates the entire database structure, including source files and initializing the SQLite database with Alembic.
- **Technology Stack Simplification:**
  - Replaced the PostgreSQL database dependency with **SQLite**. This removes the need for an external database server and simplifies deployment significantly.
  - Pinned critical Python packages (`Flask`, `Flask-SocketIO`) in `requirements.txt` to resolve dependency conflicts and ensure a stable build.
- **"No Connection" Screen:** Implemented a UI screen on the web client that appears when the connection to the server is lost, improving user experience.
- **Screensaver Integration:** Fully integrated the `ScreensaverScreen` into the main application. This includes an inactivity timer that, after a set duration, displays a slideshow of images. User interaction on the screensaver returns the user to their previous screen.
- **Screensaver Enhancement:** The screensaver slideshow has been improved. It now randomizes the order of the billboard images and uses a slow, two-second fade animation for a smoother transition between slides.
- **Bug Fix:** Resolved a startup crash (`TypeError`) caused by a refactoring mismatch between `main.py` and `websocket_server.py`. The `WebSocketServer`'s constructor was updated to accept the necessary callbacks directly, improving the code's robustness.
- **Splash Screen Rework:** The splash screen has been changed from a timed, automatic transition to a manual one. It now features a large, styled "START" button that the user must press to enter the application. The logic for the splash screen has also been refactored into its own dedicated file (`screens/splash_screen.py`) for better code organization.
- **Race Condition Fix**: Resolved a crash on the `ResumeOrNewScreen` by implementing the robust widget initialization pattern. This prevents an `AttributeError` that occurred when the screen's `on_enter` event fired before the UI widgets were fully loaded and ready.
- **Client Connection UX**: Implemented a robust and user-friendly method for connecting clients.
  - The app now generates QR codes for Player 1, Player 2, and a general observer client.
  - On the `NameEntryScreen`, QR codes are displayed directly under the name inputs for easy setup.
  - A popup was previously available from the main game screen, but this was removed in favor of a more robust pre-game network check.
  - On a Raspberry Pi, the splash screen will now check for a network connection and present a connection manager popup if disconnected, ensuring QR codes can be generated with a valid IP.
  - The splash screen now provides feedback, showing a loading indicator while QR codes are generated in the background, then revealing the "START" button.
- **QR Code Race Condition Fix**: Resolved a critical bug where QR codes would fail to display. The fix involves a new robust pattern for loading runtime-generated images: preventing premature loads, pre-caching the image texture on a loading screen, and then explicitly calling `.reload()` on the target `Image` widget before it's displayed. This pattern has been documented in `.cursorrules`.
- **Refactoring and Bug Fix**: Resolved a `KeyError` crash on the `FirstTurnSetupScreen` by removing a duplicate class definition from `main.py` and consolidating the correct logic into `screens/first_turn_setup_screen.py`. This fix also involved correcting the game state handling to ensure the `first_turn_player_id` was set and read properly before starting the game.
- **macOS Stability Fix**: Resolved a significant dependency conflict on macOS where bundled versions of SDL2 and FFmpeg from `kivy` and `ffpyplayer` caused runtime instability and warnings. The fix involves using Homebrew to install shared versions of `sdl2` and `ffmpeg@6`, then building the Python packages from source against them. This procedure has been documented in `techContext.md`.

## Active Decisions

- **Automated First-Time Setup:** The project philosophy is that a user should be able to clone the repository and run a single `install.sh` script to get a fully working application, including the database.
- **Self-Contained Dependencies:** The application aims to be as self-contained as possible, with SQLite being a key part of that strategy.
- **Reliable Image Loading**: All runtime-generated images must be loaded using the pattern documented in `.cursorrules` to prevent race conditions.

## Next Steps

1.  **Final Pi Testing**: Conduct thorough testing on the Raspberry Pi to confirm that all UI elements, especially touch interactions, are working as expected after the recent fixes.
2.  **Feature Implementation**: Begin work on the "New Game" and "Exit" functionality from the `GameOverScreen`.
3.  **Code Cleanup**: Review code for any commented-out blocks or debugging statements that can be removed.

## Next Immediate Steps

1.  **Final Pi Testing**: Conduct thorough testing on the Raspberry Pi to confirm that all UI elements, especially touch interactions, are working as expected after the recent fixes.
2.  **Documentation**: Update the `.cursorrules` file to permanently capture the robust Kivy widget initialization pattern that was discovered. This is a critical piece of project intelligence to prevent future bugs.
3.  **Feature Implementation**: Begin work on the "New Game" and "Exit" functionality from the `GameOverScreen`.

## Open Questions

- Is a simple `show()`/`hide()` mechanism sufficient, or should the controller re-initialize screens each time they are shown?

## Current Challenges

- Refactoring the client-side JavaScript without introducing new bugs.
- Ensuring the new architecture is clean and maintainable.

## Environment Notes

- Development on macOS
- Target deployment on Raspberry Pi
- Virtual environment management
- Dependencies:
  - Flask-SocketIO
  - python-socketio
  - python-dotenv
  - asyncpg
  - SQLAlchemy
  - aiosqlite

## Tomorrow's Tasks

1. Review and refine game over screen styling
2. Ensure consistent font usage across all screens
3. Test game over state transitions
4. Verify all game data is displayed correctly
5. Document any additional styling requirements
