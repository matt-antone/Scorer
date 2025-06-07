# Screen: Deployment Setup Screen

## 1. Purpose

The `DeploymentSetupScreen` is a passive, read-only view that allows observers to watch the pre-game roll-off and role selection process.

## 2. Behavior & Flow

### Appearance Condition

- This screen appears when the `game_phase` is `'deployment_setup'`.
- Player names are displayed from the previous name entry phase.

### UI Components & Interaction

- The screen is divided into two columns for Player 1 and Player 2.
- **Player Names**: Displayed from the previous name entry phase (not updated in real-time).
- **Roll Results**: Areas to display each player's D6 result as they roll.
- **Status Area**: Shows the current state of the roll-off and the final Attacker/Defender roles once they are chosen.

### Interaction Logic

This is a passive, read-only screen that updates in real-time to reflect:

- Roll results as they happen (from either Kivy host or player clients)
- Final Attacker/Defender roles once chosen

## 3. Screen Transition

- When the host presses "Continue" on the Kivy app, this client will transition to the **First Turn Setup Screen**.

## 4. Key Implementation Details

- **File Location**: `client/src/screens/DeploymentSetupScreen.js`
- **Real-time Updates**: The screen must update in real-time to show roll results and role choices, regardless of where they were initiated.
- **Name Display**: Player names are displayed from the previous name entry phase and are not updated in real-time during the deployment phase.
