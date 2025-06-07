# Screen: Deployment Setup Screen

## 1. Purpose

The `DeploymentSetupScreen` is a flexible, interactive screen that manages the pre-game roll-off. It allows players to roll directly on the host application while also reflecting actions taken on the player web clients in real-time.

## 2. Behavior & Flow

### Appearance Condition

- This screen appears on the Kivy host after the setup flow advances from the `NameEntryScreen`.
- Player names are displayed from the previous name entry phase.

### UI Components & Interaction

- The screen is divided into two columns for Player 1 (Red) and Player 2 (Blue).
- **Player Names**: Displayed from the previous name entry phase (not updated in real-time).
- **Roll Buttons**: Each player has a "Roll" button.
- **Roll Displays**: An area next to each button displays the D6 result.
- **Winner Choice Section** (Hidden by default):
  - **Instructional Text**: "Choose Role for [Winner's Name]".
  - **"Attacker" Button**.
  - **"Defender" Button**.
- **Status Labels**: Each player's column has a label to display their final role ("Attacker" or "Defender").
- **"Continue" Button**: A button to advance to the next screen, which is enabled only after the Attacker/Defender roles have been set.

### Interaction Logic (Dual Control)

This screen functions as both a controller and a real-time display.

1.  **Rolling the Dice**:
    - A player can press their "Roll" button on this screen. This disables their button on **both** the Kivy app and their web client and shows the result.
    - If a player rolls on their web client first, the "Roll" button for them on this screen will become disabled, and the result will appear here automatically.
2.  **Determining the Winner**:
    - Once both players have rolled (regardless of where they rolled from), the application determines the winner.
    - If there is a tie, the "Roll" buttons are re-enabled on all clients, and players must roll again.
3.  **Choosing the Role (First Press Wins)**:
    - If there is a clear winner, the **Winner Choice Section** appears on this screen **AND** on the winning player's web client.
    - If the choice is made on the winning player's web client, the choice section on this screen will disappear, and the final role ("Attacker"/"Defender") will be displayed for each player.
    - If the choice is made using the buttons on this screen, the same outcome occurs.
4.  **Continue**: Once the roles are set, the "Continue" button is enabled, allowing the host user to advance the game.

## 3. Screen Transition

- Upon pressing the "Continue" button, the application transitions to the `FirstTurnSetupScreen`.

## 4. Key Implementation Details

- **File Location**: `screens/deployment_setup_screen.py`
- **Dual Functionality**: This screen must be able to both send actions (rolling, choosing roles) and passively receive state updates initiated from player clients, updating its UI in real-time.
- **State-Driven UI**: The entire state of the screen—button status, roll results, visibility of choice/continue buttons—is derived directly from the central `game_state`.
- **Name Display**: Player names are displayed from the previous name entry phase and are not updated in real-time during the deployment phase.
