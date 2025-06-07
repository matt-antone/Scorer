# Screen: Splash Screen

## 1. Purpose

The Splash Screen is the initial entry point of the Scorer application. Its primary purpose is to provide a clean, welcoming start page while performing necessary pre-flight checks and setup tasks in the background before the user can proceed.

## 2. Behavior & Flow

### Initialization

- On application start, the Splash Screen is the first UI component displayed.
- It features a prominent "START" button, which is initially **disabled**.
- A loading indicator is displayed to provide feedback to the user.

### Background Tasks

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

### User Interaction

- Once all background tasks are complete (network confirmed, QR codes generated), the loading indicator is hidden.
- The **"START" button becomes enabled**.
- The user must manually press the "START" button to move to the next screen.

## 3. Screen Transition

- Upon pressing the "START" button, the application transitions to the appropriate next screen, determined by the logic in the main `ScorerApp` class.
- Typically, it will transition to the `ResumeOrNewScreen` if a saved game is detected, or the `NameEntryScreen` if no saved game exists.

## 4. Key Implementation Details

- **File Location**: `screens/splash_screen.py`
- **Manual Start**: The transition is intentionally manual (requiring a button press) rather than timed. This ensures all background tasks have ample time to complete without creating race conditions.
- **Feedback**: The loading indicator is a key piece of UX, informing the user that the application is preparing for use.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.
