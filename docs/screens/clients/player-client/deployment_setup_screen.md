# Player Client Screen: Deployment Setup

## 1. Purpose

To show the player the status of the deployment roll-off.

## 2. Proposal

- **Behavior**: Shown when the `game_phase` is `'deployment_setup'`.
- **UI**:
  - A non-interactive status screen.
  - It should display a title: "Deployment Roll-Off".
  - It should show the roll results for both players as they happen.
  - Most importantly, it should display the same instructional text as the Kivy app, e.g., "Waiting for Player 2 to roll..." or "You won the roll-off!". This keeps the player informed even if they can't see the main screen clearly.
- **Transition**: When the host continues, the client transitions to the **First Turn Setup Screen**.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `DeploymentSetupScreen`, this client screen will be active.
