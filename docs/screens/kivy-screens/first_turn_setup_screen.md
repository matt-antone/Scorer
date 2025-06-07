# Screen: First Turn Setup Screen

## 1. Purpose

The `FirstTurnSetupScreen` is a flexible, interactive screen that manages the final roll-off to determine which player takes the first turn. It allows the Attacker to make choices directly on the host application while also reflecting actions taken on the player web clients in real-time.

## 2. Behavior & Flow

### Appearance Condition

- This screen appears on the Kivy host after the setup flow advances from the `DeploymentSetupScreen`.
- Player names and roles (Attacker/Defender) are displayed from the previous phase.

### UI Components & Interaction

- The screen is divided into two columns for Player 1 (Red) and Player 2 (Blue).
- **Player Names & Roles**: Displayed from the previous phase (not updated in real-time).
- **Attacker Choice Section**:
  - **Instructional Text**: "Choose who rolls first".
  - **"Player 1 Rolls First" Button**.
  - **"Player 2 Rolls First" Button**.
- **Roll Buttons**: Each player has a "Roll" button (initially disabled).
- **Roll Displays**: Areas to display each player's D6 result.
- **First Turn Choice Section** (Hidden by default):
  - **Instructional Text**: "Choose whether to take first turn".
  - **"Take First Turn" Button**.
  - **"Pass First Turn" Button**.
- **"Start Game" Button**: A button to begin gameplay, enabled only after the first turn decision is made.

### Interaction Logic (Dual Control)

This screen functions as both a controller and a real-time display.

1.  **Choosing Who Rolls First**:

    - The Attacker can make this choice on this screen. This disables the choice buttons on **both** the Kivy app and their web client.
    - If the Attacker makes the choice on their web client first, the choice buttons on this screen will become disabled.
    - The chosen player's "Roll" button becomes enabled on all clients.

2.  **Rolling the Dice**:

    - The chosen player can roll from their client. This disables their button on **both** the Kivy app and their web client and shows the result.
    - If they roll on their web client first, the "Roll" button for them on this screen will become disabled, and the result will appear here automatically.
    - After the first roll, the other player's "Roll" button becomes enabled.

3.  **Determining the Winner**:

    - Once both players have rolled, the application determines the winner.
    - **If there is a tie**: The Attacker must choose who rolls first again. The choice buttons reappear, and the process repeats.
    - **If there is a clear winner**: The winner's "First Turn Choice Section" appears on this screen **AND** on their web client.

4.  **Choosing First Turn**:

    - The winner can press either "Take First Turn" or "Pass First Turn" on this screen or their web client.
    - If the choice is made on the web client first, the choice section on this screen will disappear.
    - If the choice is made using the buttons on this screen, the same outcome occurs.

5.  **Start Game**: Once the first turn decision is made, the "Start Game" button is enabled, allowing the host user to begin gameplay.

## 3. Screen Transition

- Upon pressing the "Start Game" button, the application transitions to the `ScorerRootWidget` and sets `game_phase` to `'game_play'`.

## 4. Key Implementation Details

- **File Location**: `screens/first_turn_setup_screen.py`
- **Dual Functionality**: This screen must be able to both send actions (choices, rolling) and passively receive state updates initiated from player clients, updating its UI in real-time.
- **State-Driven UI**: The entire state of the screen—button status, roll results, visibility of choice sections—is derived directly from the central `game_state`.
- **Tie Resolution**: Unlike the deployment phase, ties in the first turn roll-off result in the Attacker choosing who rolls first again, rather than both players rolling again.
