# Player Client Screen: Name Entry

This document describes the player client screen that allows a player to enter their name.

## 1. Purpose

This screen serves as the first interactive step for a player after they have successfully connected to the server by scanning their QR code. Its purpose is to allow them to set their player name from their own device, which will then be synchronized with the main Kivy application and all other clients.

## 2. Behavior & Flow

### Appearance Condition

- This screen appears immediately after the player's `SplashScreen` confirms a successful connection to the server.

### UI Components & Interaction

- **Header/Title**: A clear title, such as "Enter Your Name".
- **Player Identifier**: A label that confirms which player this client is controlling (e.g., "You are Player 1").
- **Text Input Field**: A single text input field, pre-filled with the default name for that player (e.g., "Player 1").
- **Confirm Button**: A button labeled "Confirm" or "Set Name".
- **Spinner/Loading Indicator**: A visual spinner that is hidden by default.

### Interaction Logic

1.  The player modifies the name in the **Text Input Field**.
2.  The player presses the **Confirm Button**.
3.  Upon pressing the button, the client MUST:
    a. Immediately disable the **Text Input Field** and the **Confirm Button** to prevent duplicate submissions.
    b. Display the **Spinner**.
    c. Send a `{'action': 'set_player_name', 'player_id': 'p1', 'name': '...'}` event to the server.
4.  The client then waits for a `game_state_update` from the server.

## 3. Screen Transition

- **To this screen**: From the player client's `SplashScreen`.
- **From this screen**: Upon receiving a `game_state_update` from the server that confirms the name has been set, the client automatically transitions to the **Player Client Deployment Roll Screen**.

## 4. Key Implementation Details

- **Synchronization**: The name entered here is sent to the server, which updates the central `game_state`. The Kivy host's `NameEntryScreen` will listen for this change and update its own text input field in real-time.
- **State-Driven**: The transition away from this screen is not controlled by the client itself, but is triggered by a state change from the server.
