# Active Context: Scorer

This document outlines the current work focus, recent changes, next steps, and active decisions for the Scorer project.

## 1. Current Work Focus

- Finalizing the initial development plan (complete).
- Setting up the development environment on the primary development machine (macOS).
- Preparing for the first phase of development: basic Kivy application structure locally on macOS.

## 2. Recent Changes & Decisions

- **Memory Bank Created**: All core memory bank files (`projectbrief.md`, `productContext.md`, `techContext.md`, `systemPatterns.md`, `activeContext.md`, `progress.md`) have been created and populated with initial content.
- **Game Edition**: Confirmed as Warhammer 40k 10th Edition.
- **Core Features Defined**: Point tracking (Primary/Secondary), CP tracking (manual), Round tracking (5 rounds), Game Timer.
- **Platform**: Raspberry Pi 5, 5-inch touchscreen (fullscreen), Python.
- **Key Technologies Chosen**:
  - GUI: Kivy
  - Web Server: Flask
  - QR Codes: `qrcode` library
  - Data Persistence: JSON files for game sessions.
- **Player Interaction**: Pi is primary controller; Web is for viewing and optional self-updates.
- **Data Storage**: Game sessions to be saved locally in a file for later reference.
- **Future Enhancement Identified**: Integration with "Dicer" (AI D6 dice detector, background process on Pi 5). This is a significant planned feature, with details to be refined as Dicer development progresses.
- **Development Environment Strategy**: Initial development will be done on macOS, with subsequent deployment and testing on the Raspberry Pi (`madlab5.local`).
- **TensorFlow Dependency Clarification**: Realized that `tensorflow-macos` and `tensorflow-metal` are for macOS development only and should not be in `requirements.txt` for Raspberry Pi deployment. A Pi-compatible TensorFlow package will be needed if Dicer is implemented on Pi.

## 3. Next Steps

- Set up the development environment on macOS:
  - Install Python (if not already satisfactorily configured), Kivy, Flask, `qrcode`, `Pillow`, Black, Flake8.
  - Initialize the Git repository locally.
  - Create a project directory and Python virtual environment (`venv`).
- Once the local environment is ready, proceed with:
  - Creating the basic Kivy application structure on macOS.
  - Implementing core game state management locally.
  - Developing the JSON-based game state saving/loading mechanism locally.

## 4. Active Questions & Considerations

- Specific layout details for the Kivy touchscreen interface.
- Detailed structure of the game state JSON file.
- Mechanism for inter-thread communication between Kivy and Flask.
- Interface and data exchange details for Dicer integration (to be defined as Dicer project evolves).
