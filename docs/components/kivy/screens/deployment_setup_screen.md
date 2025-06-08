# Deployment Setup Screen

# Version History

- v1.0.0 (2024-03-21): Initial version
- v2.0.0 (2024-07-29): Reconciled with detailed behavior documentation, correcting the screen's purpose from unit placement to the pre-game roll-off.

Last Updated: 2024-07-29 10:00 UTC

# Related Files

- [../app.md](../app.md): Main Kivy application
- [name_entry_screen.md](./name_entry_screen.md): Previous screen
- [first_turn_setup_screen.md](./first_turn_setup_screen.md): Next screen
- [../../api/state_server/state_management.md](../../api/state_server/state_management.md): State management API

# Overview

The `DeploymentSetupScreen` is a flexible, interactive screen that manages the pre-game roll-off to determine the Attacker and Defender roles. It allows players to roll directly on the host application while also reflecting actions taken on the player web clients in real-time.

# Purpose

- Manage the dice roll-off to determine which player chooses their role.
- Allow players to roll either on the Kivy host or their web client.
- Synchronize roll results and button states across all clients.
- Handle ties by requiring players to re-roll.
- Present the winning player with the choice to be "Attacker" or "Defender".
- Enable transition to the next screen only after roles have been assigned.

# Properties

- `p1_name_label` / `p2_name_label`: Displays player names from the previous screen.
- `p1_roll_button` / `p2_roll_button`: Buttons for each player to roll the dice.
- `p1_roll_display_label` / `p2_roll_display_label`: Labels to show the D6 roll result.
- `p1_choice_box` / `p2_choice_box`: A container (hidden by default) that shows the "Attacker" and "Defender" choice buttons to the winner.
- `deployment_status_label`: A label to provide instructions or status updates (e.g., "Roll for initiative", "Tie! Roll again.").
- `continue_to_first_turn_button`: Button to advance to the next screen, enabled after roles are set.

# Methods

- `on_pre_enter()`: Handles screen entry, updates UI from the current game state.
- `update_view_from_state()`: The core method for synchronizing the UI with the `game_state` (button visibility, labels, etc.).
- `roll_deployment_initiative(player_id)`: Handles the roll button press for a player.
- `choose_deployment_role(chooser_id, chose_attacker)`: Handles the role choice button press.
- `proceed_to_first_turn()`: Handles the "Continue" button press and transitions to the next screen.

# Events

- `on_roll`: Fired when a player rolls the dice.
- `on_role_chosen`: Fired when the winning player chooses their role.
- `on_continue`: Fired when the continue button is pressed.

# Behavior & Flow

## Appearance Condition

- This screen appears on the Kivy host after the setup flow advances from the `NameEntryScreen`.
- Player names are displayed from the previous name entry phase.

## Interaction Logic (Dual Control)

This screen functions as both a controller and a real-time display.

1.  **Rolling the Dice**:
    - A player can press their "Roll" button on this screen. This disables their button on **both** the Kivy app and their web client and shows the result.
    - If a player rolls on their web client first, the "Roll" button for them on this screen will become disabled, and the result will appear here automatically.
2.  **Determining the Winner**:
    - Once both players have rolled (regardless of where they rolled from), the application determines the winner.
    - If there is a tie, the "Roll" buttons are re-enabled on all clients, and players must roll again.
3.  **Choosing the Role (First Press Wins)**:
    - If there is a clear winner, choice buttons appear on this screen **AND** on the winning player's web client.
    - If the choice is made on the winning player's web client, the choice section on this screen will disappear, and the final role ("Attacker"/"Defender") will be displayed for each player.
    - If the choice is made using the buttons on this screen, the same outcome occurs.
4.  **Continue**: Once the roles are set, the "Continue" button is enabled, allowing the host user to advance the game.

# Screen Transition

- Upon pressing the "Continue" button, the application transitions to the `FirstTurnSetupScreen`.

# Key Implementation Details

- **File Location**: `screens/deployment_setup_screen.py`
- **Dual Functionality**: This screen must be able to both send actions (rolling, choosing roles) and passively receive state updates initiated from player clients, updating its UI in real-time.
- **State-Driven UI**: The entire state of the screen—button status, roll results, visibility of choice/continue buttons—is derived directly from the central `game_state`.
- **Name Display**: Player names are displayed from the previous name entry phase and are not updated in real-time during the deployment phase.

# Changelog

## 2024-07-29

- Reconciled documentation, correcting the screen's purpose from unit deployment to the pre-game roll-off for choosing Attacker/Defender roles.
- Updated all sections to reflect the roll-off functionality.

## 2024-03-21

- Initial documentation (describing an outdated unit placement flow).
- Linked related API documentation.
