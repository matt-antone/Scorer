# Scorer - Tabletop Wargame Scorekeeping Assistant

## The Problem Scorer Solves

Tabletop wargames, especially Games Workshop's Warhammer 40,000, often involve complex scoring, round tracking, command point management, and timed turns. Keeping track of these elements manually can be cumbersome, prone to errors, and detract from the immersive experience of the game. Traditional pen-and-paper methods can become messy, and remembering all game state details, especially over longer games or multiple sessions, is challenging.

**Scorer** aims to provide a dedicated digital assistant to streamline this process for Warhammer 40,000 players, ensuring accurate scorekeeping, fair turn time management, and a persistent record of the game state. While designed with Warhammer 40,000 in mind, its core functionalities might be adaptable for other similar two-player, turn-based wargames. It is intended for tournament play and casual games, with an initial focus on a Raspberry Pi-powered touchscreen kiosk.

## Current Capabilities & Features

The Scorer application, built with Kivy, currently offers the following features:

- **User-Friendly Interface:**

  - Clear, touch-friendly interface designed with a "Red vs. Blue" two-player theme.
  - Custom "InterBlack" font for enhanced readability.
  - Visual splash screen on application start.

- **Comprehensive Game Setup:**

  - **Player Name Entry:** Allows customization of player names.
  - **Deployment Setup:** Facilitates dice rolls for determining deployment initiative and allows the winner to choose Attacker or Defender roles.
  - **First Turn Setup:** Manages dice rolls for first turn advantage, with the winner (or Attacker in case of a tie) choosing who takes the first turn.

- **In-Game Management (`ScorerRootWidget`):**

  - **Score Tracking:** Displays primary scores for both players.
  - **Command Point (CP) Management:** Allows players to add or subtract CPs.
  - **Round Tracking:** Clearly indicates the current game round (up to 5 rounds).
  - **Timers:**
    - Overall game timer.
    - Individual player turn timers that track time only for the active player.
  - **Turn Progression:** "End Turn" button specific to the active player, ensuring smooth turn transitions.
  - **Concession:** Allows either player to concede the game, immediately ending it and declaring the opponent the winner.
  - **New Game Option:** Allows players to abandon the current game and start a new one from the main scoring screen.

- **Persistent Game State:**

  - **Save/Load Functionality:**
    - Prompts users to "Resume Game" or "Start New Game" if a saved game state is detected.
    - Automatically saves game progress to a `game_state.json` file.
  - **Robust Saving:**
    - Game state is saved when the application is closed.
    - Progress is saved at key moments like the start of a game, end of each turn, and after a concession.
    - **Immediate Saves:** Critical changes like score updates or CP adjustments are saved instantly to prevent data loss from unexpected interruptions.

- **Game Conclusion:**

  - **Game Over Screen:** Displays final scores, CPs, time played per player, total game time, rounds played, and clearly states the winner (including wins by concession).
  - Options to start a new game or exit the application.

- **Development & Platform:**
  - Developed in Python using the Kivy framework.
  - Primarily designed for Warhammer 40,000, though adaptable for other similar systems.
  - Currently developed and tested on macOS, with a fixed window size (800x480) emulating the target Raspberry Pi display.
  - Includes OS-specific configurations for fullscreen (Linux/Raspberry Pi) and windowed mode (macOS/Windows).

## Future Goals (High-Level)

- Deployment and testing on a Raspberry Pi with a touchscreen.
- Potential integration with a Flask web server for remote viewing/interaction.
- QR code generation for easy access to web features.
- Integration with Dicer AI (a separate project component).
- Secondary score tracking and other advanced game-specific features.

---

This README provides an overview of the Scorer project. For more detailed insights into development patterns, technical decisions, and current work focus, please refer to the files within the `memory-bank/` directory and the `.cursorrules` file.
