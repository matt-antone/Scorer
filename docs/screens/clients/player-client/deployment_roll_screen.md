# Screen: Deployment Roll Screen

## 1. Purpose

The `DeploymentRollScreen` is the player client's interface for the pre-game roll-off. It allows players to roll their die and, if they win, choose their role as either Attacker or Defender.

## 2. Behavior & Flow

### Appearance Condition

- This screen appears when the `game_phase` is `'deployment_setup'`.
- Player names are displayed from the previous name entry phase.

### UI Components & Interaction

- **Player Name**: Displayed from the previous name entry phase (not updated in real-time).
- **"Roll Die" Button**: A button to initiate the roll.
- **Spinner**: A loading indicator that appears while waiting for the roll result.
- **Your Roll Display**: An area to show the D6 result.
- **Opponent's Roll Display**: An area to show the opponent's D6 result.
- **Winner Choice Section** (Hidden by default):
  - **Instructional Text**: "Choose Your Role".
  - **"Attacker" Button**.
  - **"Defender" Button**.
- **Status Messages**: Dynamic text to show the current state (e.g., "Waiting for opponent to roll...").

### Interaction Logic (Dual Control)

This screen is interactive but also listens for state changes initiated by the Kivy host.

1.  A player presses the **"Roll Die" Button**.
2.  The client immediately disables its own button, shows the **Spinner**, and sends a `{'action': 'deployment_roll', ...}` event. The roll button for this player on the Kivy host will also become disabled.
3.  The client waits for a `game_state_update`. When it arrives:
    a. The **Spinner** is hidden.
    b. The **Your Roll Display** is updated with the result.
    c. If the opponent has also rolled (from either their client or the Kivy host), their result is shown.
4.  **If both rolls are complete**, the server determines the winner. If this player is the winner, their client will:
    a. Show the **Winner Choice Section** (Attacker/Defender buttons).
    b. The losing player's client will show a "Waiting for winner to choose..." message.
5.  **Choosing the Role (First Press Wins)**:
    - The winning player can press either the **"Attacker"** or **"Defender"** button. This disables the choice buttons, shows the **Spinner**, and sends the choice to the server.
    - If the choice is made first on the Kivy host, this client will receive a `game_state_update`, and the **Winner Choice Section** will be hidden, replaced by a status update.

## 3. Screen Transition

- When the host presses "Continue" on the Kivy app, this client will transition to the **First Turn Setup Screen**.

## 4. Key Implementation Details

- **File Location**: `client/src/screens/DeploymentRollScreen.js`
- **Real-time Updates**: The screen must update in real-time to show roll results and role choices, regardless of whether they were initiated on this client or on the Kivy host.
- **Conditional UI**: The Attacker/Defender choice buttons must only appear for the player who won the roll, and they must be hidden if the choice is made elsewhere.
- **Name Display**: Player names are displayed from the previous name entry phase and are not updated in real-time during the deployment phase.
