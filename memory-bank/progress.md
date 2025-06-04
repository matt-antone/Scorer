# Progress: Scorer

This document tracks what works, what's left to build, current status, and known issues for Scorer.

## 1. Current Status

- **Phase**: Project Initiation & Planning.
- **Overall Progress**: 5% (Memory Bank foundation established).
- **Last Update**: 2024-07-25 - Initial Memory Bank files created and populated.

## 2. What Works

- N/A - Development has not yet started.

## 3. What's Left to Build (High-Level)

- **Development Environment Setup (macOS first, then adapted for Raspberry Pi)**:
  - **macOS**: Install Python (ensure a suitable version like 3.9+), Kivy, Flask, `qrcode`, `Pillow`, Black, Flake8.
  - Initialize Git repository locally.
  - Create project directory and `venv`.
  - Create initial `requirements.txt` based on macOS setup.
  - **Raspberry Pi (`madlab5.local`)**: Later, replicate a similar environment using `requirements.txt`, installing necessary system dependencies for Kivy.
- **Kivy Application (Core) - Initial development on macOS**:
  - Basic application window and main screen layout.
  - Game state data structures.
  - UI elements for:
    - Player 1 & 2 scores (Primary, Secondary, Total).
    - Player 1 & 2 Command Points.
    - Current Round display & control.
    - Game Timer display & control.
    - Start New Game / Load Game functionality.
    - QR Code display area.
  - Logic for updating scores, CPs, rounds, timer.
  - Fullscreen mode implementation.
- **Data Persistence**:
  - Functions to save game state to JSON.
  - Functions to load game state from JSON.
  - Logic for handling file operations (e.g., naming, finding previous games if desired).
- **Flask Web Application**:
  - Basic Flask app setup.
  - API Endpoints:
    - `GET /api/gamestate`
    - `POST /api/player/<player_id>/score` (and for secondary objectives if separate)
    - `POST /api/player/<player_id>/cp`
  - Communication bridge between Flask and Kivy app (e.g., Queue or events).
  - Basic HTML/JS web frontend for player interaction (view scores, update own scores/CPs).
- **QR Code Integration**:
  - Logic to get Raspberry Pi's local IP address.
  - Generate QR code image using the `qrcode` library.
  - Display QR code in the Kivy UI.
- **Dicer AI Detector Integration (Phased based on Dicer project readiness)**:
  - Define interface and data exchange mechanism between Scorer and Dicer.
  - Implement logic in Scorer to trigger Dicer (if applicable) and receive/process D6 dice results.
  - Modify Kivy UI to display/utilize Dicer results as needed (e.g., auto-fill roll results, suggest actions).
  - Manage Dicer as a background process.
  - Testing of integrated Dicer functionality.
- **Testing & Refinement**:
  - Unit tests for critical logic (game state, persistence).
  - User acceptance testing (gameplay testing).
  - UI/UX refinement based on feedback.
- **Documentation**:
  - README for setup and usage.
  - Code comments for complex sections.
  - Ongoing updates to the Memory Bank.

## 4. Known Issues

- N/A - Development has not yet started.
