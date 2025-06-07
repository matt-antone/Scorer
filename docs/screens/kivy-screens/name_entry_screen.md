# Screen: Name Entry Screen

## 1. Purpose

The `NameEntryScreen` is the first step in the "New Game" workflow. It allows players to input their names and, crucially, serves as the point where the QR codes for the player web clients are displayed for easy connection.

## 2. Behavior & Flow

### Initialization

- The screen displays two columns, one for Player 1 (Red) and one for Player 2 (Blue).
- Each column contains:
  - A `TextInput` field, pre-populated with default names ("Player 1" and "Player 2").
  - An `Image` widget where the player-specific QR code will be displayed.

### User Interaction & Synchronization

- **Name Entry**: Names can be entered in two ways:
  1.  **Locally**: Players can tap the `TextInput` fields on the Kivy host to change their names.
  2.  **Remotely**: If a player submits their name from their web client, the corresponding `TextInput` on this screen will update in real-time to reflect that change.
- **Continue Button**: A "Continue" button is present. Pressing this button manually advances the application to the next screen.

### QR Code Display

- The QR codes for Player 1 and Player 2, which were generated in the background during the `SplashScreen`, are displayed here.
- This screen uses the **Reliable Runtime Image Loading** pattern to ensure the QR codes appear without flickering or race conditions. The image textures are pre-loaded into Kivy's cache before this screen is shown, and the `Image` widgets have their `.reload()` method called to guarantee they display the newly available images.

## 3. Screen Transition: Hybrid Model

The transition from this screen is handled by a hybrid model, allowing for both manual and automatic advancement.

- **Manual Transition**: The user on the Kivy host can press the **"Continue" button** at any time. This action immediately saves the current state and transitions all clients to the `DeploymentSetupScreen`.
- **Automatic Transition**: The application controller continuously checks if both players have submitted their names via their respective web clients. The moment this condition is met, the application will **automatically transition all clients** to the `DeploymentSetupScreen`, even if the "Continue" button has not been pressed.

## 4. Key Implementation Details

- **File Location**: `screens/name_entry_screen.py`
- **Simplified Flow**: The logic requiring users to enter text before enabling the "Continue" button was intentionally removed to speed up the game setup process.
- **Reliable Image Loading**: This screen is a key example of the robust image loading pattern documented in `.cursorrules`. It ensures that images generated at runtime (the QR codes) are displayed reliably.
- **Controller Logic**: The main `ScorerApp` class handles all logic, including listening for remote name submissions and triggering the automatic screen transition.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.
