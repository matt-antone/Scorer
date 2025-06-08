# Splash Screen

# Version History

- v1.0.0 (2024-03-21): Initial version
- v1.0.1 (2024-03-21): Added game state checking and user interaction
- v2.0.0 (2024-07-29): Reconciled with detailed behavior documentation.

Last Updated: 2024-07-29 10:00 UTC

# Related Files

- [../app.md](../app.md): Main Kivy application
- [resume_or_new_screen.md](./resume_or_new_screen.md): Next screen if saved game exists
- [name_entry_screen.md](./name_entry_screen.md): Next screen for new game
- [../../api/state_server/state_management.md](../../api/state_server/state_management.md): State management API

# Overview

The Splash Screen is the initial entry point of the Scorer application. Its primary purpose is to provide a clean, welcoming start page while performing necessary pre-flight checks and setup tasks in the background before the user can proceed.

# Purpose

- Display a loading indicator while background tasks run.
- Perform network checks (on Raspberry Pi) to ensure connectivity for QR code generation.
- Generate QR codes for player and observer clients.
- Enable a "START" button only after all background tasks are successfully completed.
- Check for a saved game state to determine the next screen.

# Properties

- `loading_indicator`: A widget (e.g., a spinner) to indicate background tasks are running.
- `start_button`: Button to start/resume game. Initially disabled.
- `error_label`: Error message display (e.g., for network issues).

# Methods

- `on_enter()`: Handles screen entry and triggers background tasks.
- `on_leave()`: Handles screen exit.
- `_check_network_task()`: Performs network connectivity checks.
- `_generate_qr_codes_task()`: Initiates QR code generation in a background thread.
- `_on_qr_codes_generated()`: Callback executed when QR codes are ready, enables the start button.
- `transition_to_next_screen()`: Handles the transition to the next screen based on game state.
- `handle_error(error)`: Handles and displays errors.

# Events

- `on_loading_complete`: Fired when all background tasks are complete and the start button is enabled.
- `on_error`: Fired if a connection or other critical task fails.

# Behavior & Flow

## Initialization

- On application start, the Splash Screen is the first UI component displayed.
- It features a prominent "START" button, which is initially **disabled**.
- A loading indicator is displayed to provide feedback to the user.

## Background Tasks

While the loading indicator is shown, the application performs several critical background tasks:

1.  **Network Check (Raspberry Pi Only)**:
    - It verifies if the device has an active network connection.
    - If no connection is found, a `ConnectionManager` popup appears, prompting the user to connect to a network. This is crucial because a valid IP address is required to generate the QR codes for the web clients.
2.  **QR Code Generation**:
    - Once a network connection is confirmed, the application generates three QR codes in a background thread:
      - Player 1's client
      - Player 2's client
      - Observer client
    - This process can take a moment, which is why it's done here to avoid blocking the UI later.

## User Interaction

- Once all background tasks are complete (network confirmed, QR codes generated), the loading indicator is hidden.
- The **"START" button becomes enabled**.
- The user must manually press the "START" button to move to the next screen.

# Screen Transition

- Upon pressing the "START" button, the application transitions to the appropriate next screen, determined by the logic in the main `ScorerApp` class.
- Typically, it will transition to the `ResumeOrNewScreen` if a saved game is detected, or the `NameEntryScreen` if no saved game exists.

# Key Implementation Details

- **File Location**: `screens/splash_screen.py`
- **Manual Start**: The transition is intentionally manual (requiring a button press) rather than timed. This ensures all background tasks have ample time to complete without creating race conditions.
- **Feedback**: The loading indicator is a key piece of UX, informing the user that the application is preparing for use.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.

# Changelog

## 2024-07-29

- Reconciled developer-focused documentation with user-facing behavioral documentation.
- Integrated detailed `Behavior & Flow` and `Key Implementation Details`.
- Clarified `Properties`, `Methods`, and `Events` to match the implementation.

## 2024-03-21

- Initial documentation
- Added overview, properties, methods, and flow
- Added app initialization
- Added resource loading
- Added requirements checking
- Added error handling
- Linked related API documentation
- Added game state checking
- Added user interaction handling
- Added start button functionality
- Updated screen transitions
- Added conditional routing logic
- Synchronized with new documentation standard from `docs/screens/kivy-screens/splash_screen.md`
