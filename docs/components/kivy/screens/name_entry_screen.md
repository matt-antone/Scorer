# Name Entry Screen

# Version History

- v1.0.0 (2024-03-21): Initial version
- v2.0.0 (2024-07-29): Reconciled with detailed behavior documentation.

Last Updated: 2024-07-29 10:00 UTC

# Related Files

- [../app.md](../app.md): Main Kivy application
- [splash_screen.md](./splash_screen.md): Previous screen
- [deployment_setup_screen.md](./deployment_setup_screen.md): Next screen
- [../../api/state_server/state_management.md](../../api/state_server/state_management.md): State management API

# Overview

The `NameEntryScreen` is the first step in the "New Game" workflow. It allows players to input their names and, crucially, serves as the point where the QR codes for the player web clients are displayed for easy connection.

# Purpose

- Allow local and remote name entry for Player 1 and Player 2.
- Display player-specific QR codes for web client connection.
- Synchronize names entered on web clients with the Kivy host.
- Provide a hybrid (manual and automatic) transition to the next screen.

# Properties

- `player1_name_input`: TextInput for Player 1's name.
- `player2_name_input`: TextInput for Player 2's name.
- `p1_qr_code`: Image widget to display Player 1's QR code.
- `p2_qr_code`: Image widget to display Player 2's QR code.
- `continue_button`: Button to manually proceed to the next screen.
- `error_label`: Label for displaying any errors.

# Methods

- `on_enter()`: Handles screen entry, displays QR codes using the reliable loading pattern.
- `save_names_and_proceed()`: Handles the "Continue" button press, saves the names, and transitions the screen.
- `set_active_input(text_input)`: Manages which text input is currently focused for keyboard entry.
- `on_touch_down(touch)`: Handles touch events to unfocus text inputs when tapping outside.
- `update_player_name_from_remote(player_id, name)`: Updates the TextInput when a name is submitted from a web client.

# Events

- `on_names_saved`: Fired when the continue button is pressed and names are saved to the game state.
- `on_auto_transition`: Fired when the controller detects both players have submitted names remotely.

# Behavior & Flow

## Initialization

- The screen displays two columns, one for Player 1 (Red) and one for Player 2 (Blue).
- Each column contains:
  - A `TextInput` field, pre-populated with default names ("Player 1" and "Player 2").
  - An `Image` widget where the player-specific QR code will be displayed.

## User Interaction & Synchronization

- **Name Entry**: Names can be entered in two ways:
  1.  **Locally**: Players can tap the `TextInput` fields on the Kivy host to change their names.
  2.  **Remotely**: If a player submits their name from their web client, the corresponding `TextInput` on this screen will update in real-time to reflect that change.
- **Continue Button**: A "Continue" button is present. Pressing this button manually advances the application to the next screen.

## QR Code Display

- The QR codes for Player 1 and Player 2, which were generated in the background during the `SplashScreen`, are displayed here.
- This screen uses the **Reliable Runtime Image Loading** pattern to ensure the QR codes appear without flickering or race conditions. The image textures are pre-loaded into Kivy's cache before this screen is shown, and the `Image` widgets have their `.reload()` method called to guarantee they display the newly available images.

# Screen Transition: Hybrid Model

The transition from this screen is handled by a hybrid model, allowing for both manual and automatic advancement.

- **Manual Transition**: The user on the Kivy host can press the **"Continue" button** at any time. This action immediately saves the current state and transitions all clients to the `DeploymentSetupScreen`.
- **Automatic Transition**: The application controller continuously checks if both players have submitted their names via their respective web clients. The moment this condition is met, the application will **automatically transition all clients** to the `DeploymentSetupScreen`, even if the "Continue" button has not been pressed.

# Key Implementation Details

- **File Location**: `screens/name_entry_screen.py`
- **Simplified Flow**: The logic requiring users to enter text before enabling the "Continue" button was intentionally removed to speed up the game setup process.
- **Reliable Image Loading**: This screen is a key example of the robust image loading pattern documented in `.cursorrules`. It ensures that images generated at runtime (the QR codes) are displayed reliably.
- **Controller Logic**: The main `ScorerApp` class handles all logic, including listening for remote name submissions and triggering the automatic screen transition.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.

# Changelog

## 2024-07-29

- Reconciled developer-focused documentation with user-facing behavioral documentation.
- Integrated detailed `Behavior & Flow` and `Key Implementation Details`.
- Clarified `Properties`, `Methods`, and `Events` to match the implementation.

## 2024-03-21

- Initial documentation
- Added overview, properties, methods, and flow
- Added input validation
- Added game state initialization
- Added QR code generation
- Added error handling
- Linked related API documentation
- Synchronized with new documentation standard from `docs/screens/kivy-screens/name_entry_screen.md`
