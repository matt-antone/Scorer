# Screen: First Turn Setup Screen

## 1. Purpose

The `FirstTurnSetupScreen` is a passive, read-only view that allows observers to watch the final roll-off and decision process for determining which player takes the first turn.

## 2. Behavior & Flow

### Appearance Condition

- This screen appears when the `game_phase` is `'first_turn_setup'`.
- Player names and roles (Attacker/Defender) are displayed from the previous phase.

### UI Components & Interaction

- The screen is divided into two columns for Player 1 and Player 2.
- **Player Names & Roles**: Displayed from the previous phase (not updated in real-time).
- **Status Area**: Shows the current state of the process, such as:
  - "Waiting for Attacker to choose who rolls first"
  - "Player 1 is rolling..."
  - "Player 2 is rolling..."
  - "Tie! Attacker must choose again"
  - "Player 1 won the roll. Waiting for their decision..."
  - "Player 1 has chosen to take the first turn"
- **Roll Results**: Areas to display each player's D6 result as they roll.

### Interaction Logic

This is a passive, read-only screen that updates in real-time to reflect:

- The Attacker's choice of who rolls first
- Roll results as they happen (from either Kivy host or player clients)
- Tie situations where the Attacker must choose again
- The winner's choice to take or pass the first turn

## 3. Screen Transition

- When the host presses "Start Game" on the Kivy app, this client will transition to the **Game Play Screen**.

## 4. Key Implementation Details

- **File Location**: `client/src/screens/FirstTurnSetupScreen.js`
- **Real-time Updates**: The screen must update in real-time to show all choices and roll results, regardless of where they were initiated.
- **Tie Resolution**: Unlike the deployment phase, ties in the first turn roll-off result in the Attacker choosing who rolls first again, rather than both players rolling again.
