# Project Brief: Scorer

This document outlines the core requirements and goals for the Scorer application.

## 1. Project Overview

Scorer is a Python application designed to assist in tracking game status for Warhammer 40k (10th Edition). It will run fullscreen on a Raspberry Pi 5 equipped with a 5-inch touchscreen, providing a primary interface for users. Additionally, Scorer will host a web server, enabling players to connect and interact with game information (including updating their own scores) via their mobile phone browsers, facilitated by QR code scanning for easy access. Future plans include integration with "Dicer," an AI dice detection system, to further automate game input.

## 2. Core Requirements

The application must fulfill the following core functionalities:

- **Game Point Tracking**: Accurately track game points for two players in Warhammer 40k 10th Edition, including primary and secondary objectives.
- **Command Point Tracking**: Monitor command points for each player (manual increment/decrement, as CPs are acquired in each player's command phase).
- **Round Tracking**: Display and manage the current game round (up to 5 rounds).
- **Game Timer**: Implement a general game timer (e.g., countdown for total game duration, or count-up).
- **Platform**:
  - Run fullscreen on a Raspberry Pi 5.
  - Utilize a 5-inch touchscreen as the primary display and comprehensive control interface for all game management tasks.
- **Technology**:
  - Developed in Python.
- **Web Server**:
  - Include a built-in web server.
  - Allow players to connect via a web browser to view all game data.
  - Optionally allow players to update their own game points and command points through the web interface as a convenience.
  - Use QR codes (displayed on the Pi's screen) to provide easy access to the web interface for players' mobile devices.

### 2.1. Planned Future Enhancements

- **AI Dice Detection (Dicer Integration)**: Integrate with the "Dicer" project, an AI system for detecting D6 dice results. Dicer is planned to run as a background process on the Raspberry Pi 5. Specific integration points and data exchange mechanisms are to be determined as Dicer's development progresses.

## 3. Project Goals

- To provide a dedicated, user-friendly, and efficient tool for Warhammer 40k (10th Edition) players to manage crucial game elements.
- To enhance the gaming experience by reducing manual tracking burdens.
- To leverage the Raspberry Pi's capabilities for a portable and integrated solution.
- To offer a convenient way for players to follow along and interact with the game state using their own devices, including managing their own scores.

## 4. Scope

- **In Scope**:
  - Development of the Python application for the Raspberry Pi (fullscreen).
  - Creation of the touchscreen user interface (primary comprehensive controller).
  - Implementation of the web server and web interface for player viewing and optional self-updates.
  - QR code generation and display.
  - Core tracking logic for 10th Edition primary/secondary objectives, command points, rounds, and a general game timer.
  - Integration with the "Dicer" AI dice detector (D6 detection, background process on Pi 5). This is dependent on the progress and interface definition of the Dicer project and may be phased in.
- **Out of Scope (Initially, unless specified later)**:
  - Tracking specific game phases (e.g., Command Phase, Movement Phase). The focus is on scores, CPs, round, and timer.
  - Detailed army list management.
  - User accounts or persistent player profiles beyond a single game session.
  - Online multiplayer (beyond local network web access).
  - Integration with external Warhammer 40k APIs or databases.

## Game Structure Constraints

- There will only ever be one game in the database at a time.
- There will only ever be two players per game.
- There will only ever be 5 turns per player per game (10 turns total per game).

## Database Constraints

- Only one game row exists (enforced by a check constraint)
- Only two players per game (enforced by application logic: a new game will delete all existing records)
- Only 5 turns per player (enforced by unique constraint on game_id, player_id, round_number)
