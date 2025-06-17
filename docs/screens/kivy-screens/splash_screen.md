# Screen: Splash Screen

## 1. Purpose

The Splash Screen is the initial entry point of the Scorer application. Its primary purpose is to provide a clean, welcoming start page while performing necessary pre-flight checks and setup tasks in the background before the user can proceed.

## 2. Behavior & Flow

### Initialization

- On application start, the Splash Screen is the first UI component displayed.
- It features a prominent "START" button, which is initially **disabled**.
- A loading indicator is displayed to provide feedback to the user.
- An error label is present but hidden by default, used to display any network-related errors.

### Background Tasks

While the loading indicator is shown, the application performs several critical background tasks:

1.  **Network Check (Raspberry Pi Only)**:
    - It verifies if the device has an active network connection using the `NetworkManager` class.
    - The network check is performed in a background thread to avoid blocking the UI.
    - If no connection is found:
      - The error label becomes visible with a user-friendly message
      - The START button remains disabled
      - The loading indicator is hidden
      - A retry button appears, allowing users to attempt reconnection
    - If connection is successful:
      - The error label remains hidden
      - The START button becomes enabled
      - The loading indicator is hidden
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
- If network connection fails, users can use the retry button to attempt reconnection.

## 3. Screen Transition

- Upon pressing the "START" button, the application transitions to the appropriate next screen, determined by the logic in the main `ScorerApp` class.
- Typically, it will transition to the `ResumeOrNewScreen` if a saved game is detected, or the `NameEntryScreen` if no saved game exists.

## 4. Key Implementation Details

- **File Location**: `screens/splash_screen.py`
- **Manual Start**: The transition is intentionally manual (requiring a button press) rather than timed. This ensures all background tasks have ample time to complete without creating race conditions.
- **Feedback**: The loading indicator and error label provide clear feedback to users about the application's state.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.
- **Error Handling**: The screen includes robust error handling for network issues, with clear user feedback and retry options.

## Universal UI Requirements (MANDATORY)

- This screen (and all others) must use `pi_client/assets/background.png` as the background image for the entire screen.
- The `HeaderWidget` must be present at the top, with its `title` property set to `UI_STRINGS['splash']['title']`.
- The header must include a cog (settings) icon on the far right; tapping it launches the Settings screen.

These requirements are now mandatory for all screens to ensure UI consistency.
