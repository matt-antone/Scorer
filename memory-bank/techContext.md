# Tech Context: Scorer

This document lists the technologies, development setup, technical constraints, and dependencies for Scorer.

## 1. Core Technologies

- **Programming Language**: Python (targeting version 3.9+ or as appropriate for Raspberry Pi OS stability)
- **GUI Framework (Raspberry Pi Touchscreen)**: Kivy
  - Reason: Popular open-source Python library for rapid development of applications with innovative user interfaces, such as multi-touch apps. Well-suited for Raspberry Pi and touchscreen interaction. It will be used to create the fullscreen application.
- **Web Framework (Player Interface)**: Flask
  - Reason: A lightweight and highly popular WSGI web application framework in Python. Its simplicity and flexibility make it ideal for the embedded web server providing player access.
- **QR Code Generation**: `qrcode` library (likely with `Pillow` for image manipulation).
  - Reason: A popular and easy-to-use Python library for creating QR codes.
- **Data Persistence**: JSON files.
  - Reason: Game sessions (current scores, CPs, round, timer state, etc.) will be saved to local JSON files (specifically `game_state.json` in the Kivy user data directory). This allows for game state to be preserved between application runs or in case of a restart.
- **Custom Fonts**: Uses `LabelBase.register` from `kivy.core.text` to register custom fonts like "InterBlack" for use throughout the application via KV language or Python styling.

## 2. Platform & Deployment

- **Primary Development Environment**: macOS (user's local machine).
- **Target Deployment Platform**: Raspberry Pi 5 with a 5-inch touchscreen, accessible at `madlab5.local` on the local network. (Username for SSH: `matthewantone`).
- **Operating System (Deployment)**: Raspberry Pi OS (default configuration, likely with desktop environment to support Kivy, unless a more minimal setup is feasible).
- **Python Environment**: Standard Python installation on macOS for development, `venv` will be used for managing project dependencies. Similar setup on Raspberry Pi OS for deployment.
- **Web Server Deployment**: The Flask development server will be used initially. For a more robust local deployment, Gunicorn might be considered later if needed, but is likely not necessary for the intended use case.

## 3. Development Setup & Tools (macOS and mirrored on Pi where applicable)

- **Python Execution Command**: `python3` (to be used for running scripts and invoking pip, e.g., `python3 -m pip ...`)
- **Version Control**: Git (repository to be hosted on a platform like GitHub).
- **Dependency Management**: `requirements.txt` file managed by `pip` and `venv`.
- **Code Formatting**: Black (to ensure consistent code style).
- **Linting**: Flake8 (to catch common Python errors and style issues).
- **IDE/Editor**: User's preference (Cursor).

## 4. Technical Constraints & Considerations

- **Raspberry Pi Performance**: The application should be optimized to run smoothly on the Raspberry Pi 5, considering its processing power and RAM limitations, especially with a GUI and web server running simultaneously.
- **Touchscreen Input**: The Kivy interface must be designed for touch input, with appropriately sized buttons and interactive elements for the 5-inch screen.
- **Local Network Reliance**: The web interface for players relies on the Raspberry Pi and the players' devices being on the same local network.
- **Python Version Compatibility**: Ensure all chosen libraries are compatible with the target Python version on the Raspberry Pi.
- **Fullscreen Mode**: Kivy will need to be configured to run in fullscreen mode, hiding any desktop elements.
- **Platform-Specific Dependencies**: Care must be taken with dependencies that have platform-specific builds. For example, TensorFlow, planned for the future "Dicer" AI feature, has different packages for macOS (e.g., `tensorflow-macos`, `tensorflow-metal`) and ARM-based Linux on Raspberry Pi (e.g., a general `tensorflow` package). The `requirements.txt` for Pi deployment must only include packages compatible with the Pi. macOS-specific packages should be managed in the local macOS development environment if needed for features developed there but not immediately deployed or used on the Pi.
