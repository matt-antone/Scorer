# Screen: First Turn Setup Screen

## 1. Purpose

The `FirstTurnSetupScreen` is the player client's interface for the final roll-off to determine who takes the first turn. It allows players to make choices and roll their die, with the Attacker having special privileges for choosing who rolls first.

## 2. Behavior & Flow

### Appearance Condition

- This screen appears when the `game_phase` is `'first_turn_setup'`.
- Player names and roles (Attacker/Defender) are displayed from the previous phase.

### UI Components & Interaction

- **Player Name & Role**: Displayed from the previous phase (not updated in real-time).
- **Attacker Choice Section** (Only shown to Attacker):
  - **Instructional Text**: "Choose who rolls first".
  - **"Player 1 Rolls First" Button**.
  - **"Player 2 Rolls First" Button**.
- **"Roll Die" Button**: A button to initiate the roll (enabled only when it's your turn).
- **Spinner**: A loading indicator that appears while waiting for the roll result.
- **Your Roll Display**: An area to show your D6 result.
- **Opponent's Roll Display**: An area to show the opponent's D6 result.
- **First Turn Choice Section** (Hidden by default, only shown to winner):
  - **Instructional Text**: "Choose whether to take first turn".
  - **"Take First Turn" Button**.
  - **"Pass First Turn" Button**.
- **Status Messages**: Dynamic text to show the current state (e.g., "Waiting for Attacker to choose...", "Waiting for opponent to roll...").

### Interaction Logic (Dual Control)

This screen is interactive but also listens for state changes initiated by the Kivy host.

1.  **If you are the Attacker**:

    - You can choose who rolls first using the **Attacker Choice Section**.
    - This disables the choice buttons on **both** your client and the Kivy host.
    - If the choice is made first on the Kivy host, your choice buttons will be disabled.

2.  **When it's your turn to roll**:

    - Press the **"Roll Die" Button**.
    - The client immediately disables your button, shows the **Spinner**, and sends a `{'action': 'first_turn_roll', ...}` event.
    - The roll button for you on the Kivy host will also become disabled.
    - When the result arrives, the **Spinner** is hidden and your roll is displayed.

3.  **If there is a tie**:

    - The **Attacker Choice Section** reappears for the Attacker.
    - The process repeats with the Attacker choosing who rolls first again.

4.  **If you win the roll**:
    - The **First Turn Choice Section** appears on your client **AND** on the Kivy host.
    - You can press either **"Take First Turn"** or **"Pass First Turn"**.
    - If the choice is made first on the Kivy host, your choice section will be hidden.

## 3. Screen Transition

- When the host presses "Start Game" on the Kivy app, this client will transition to the **Game Play Screen**.

## 4. Key Implementation Details

- **File Location**: `client/src/screens/FirstTurnSetupScreen.js`
- **Real-time Updates**: The screen must update in real-time to show roll results and choices, regardless of whether they were initiated on this client or on the Kivy host.
- **Conditional UI**: The Attacker Choice Section and First Turn Choice Section must only appear for the appropriate players.
- **Tie Resolution**: Unlike the deployment phase, ties in the first turn roll-off result in the Attacker choosing who rolls first again, rather than both players rolling again.
