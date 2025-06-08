# First Turn Setup Screen

# Version History

- v1.0.0 (2024-03-21): Initial version
- v2.0.0 (2024-07-29): Reconciled with detailed behavior documentation for the first turn roll-off.

Last Updated: 2024-07-29 10:00 UTC

# Related Files

- [../app.md](../app.md): Main Kivy application
- [deployment_setup_screen.md](./deployment_setup_screen.md): Previous screen
- [scorer_root_widget.md](./scorer_root_widget.md): Next screen
- [../../api/state_server/state_management.md](../../api/state_server/state_management.md): State management API

# Overview

The `FirstTurnSetupScreen` is a flexible, interactive screen that manages the final roll-off to determine which player takes the first turn. It allows the Attacker to make choices directly on the host application while also reflecting actions taken on the player web clients in real-time.

# Purpose

- Manage the dice roll-off to determine who takes the first turn.
- Allow the Attacker to choose which player rolls first.
- Synchronize all choices, rolls, and UI states across all clients.
- Allow the roll-off winner to choose whether to take or pass the first turn.
- Enable transition to the main game screen only after the first turn player is decided.

# Properties

- `p1_name_label` / `p2_name_label`: Displays player names and roles (Attacker/Defender).
- `p1_ft_roll_button` / `p2_ft_roll_button`: Buttons for each player to roll (initially disabled).
- `p1_ft_roll_display_label` / `p2_ft_roll_display_label`: Labels to show the D6 roll result.
- `p1_ft_choice_box` / `p2_ft_choice_box`: Containers for choice buttons (e.g., who rolls first, take/pass turn).
- `first_turn_status_label`: Provides instructions and status updates.
- `start_game_button`: Button to start the game, enabled when setup is complete.

# Methods

- `on_pre_enter()`: Handles screen entry and updates the UI from the current game state.
- `update_view_from_state()`: The core method for synchronizing the UI with the `game_state`.
- `roll_first_turn_initiative(player_id)`: Handles the roll button press for a player.
- `attacker_chooses_roller(chosen_player_id)`: Handles the Attacker's choice of who rolls first.
- `winner_chooses_first_turn(winner_takes_turn)`: Handles the roll-off winner's choice to take or pass the first turn.
- `start_game_action()`: Handles the "Start Game" button press and transitions to the main game screen.

# Events

- `on_roll`: Fired when a player rolls the dice.
- `on_first_turn_decided`: Fired when the winner chooses to take or pass the first turn.
- `on_game_start`: Fired when the "Start Game" button is pressed.

# Behavior & Flow

## Appearance Condition

- This screen appears on the Kivy host after the setup flow advances from the `DeploymentSetupScreen`.
- Player names and roles (Attacker/Defender) are displayed from the previous phase.

## Interaction Logic (Dual Control)

1.  **Choosing Who Rolls First**:

    - The Attacker can make this choice on this screen or their web client. This disables the choice buttons on all clients.
    - The chosen player's "Roll" button becomes enabled on all clients.

2.  **Rolling the Dice**:

    - The chosen player rolls on either the host or their client, disabling their roll button everywhere and showing the result.
    - After the first roll, the other player's "Roll" button becomes enabled.

3.  **Determining the Winner**:

    - Once both players have rolled, the application determines the winner.
    - **If there is a tie**: The Attacker must choose who rolls first again. The choice buttons reappear, and the process repeats.
    - **If there is a clear winner**: The winner's "First Turn Choice Section" (`Take First Turn` / `Pass First Turn`) appears on this screen and on their web client.

4.  **Choosing First Turn**:

    - The winner can press either "Take First Turn" or "Pass First Turn" on this screen or their web client. The choice is reflected everywhere.

5.  **Start Game**: Once the first turn decision is made, the "Start Game" button is enabled, allowing the host user to begin gameplay.

# Screen Transition

- Upon pressing the "Start Game" button, the application transitions to the `ScorerRootWidget` and sets `game_phase` to `'game_play'`.

# Key Implementation Details

- **File Location**: `screens/first_turn_setup_screen.py`
- **Dual Functionality**: This screen must be able to both send actions (choices, rolling) and passively receive state updates initiated from player clients, updating its UI in real-time.
- **State-Driven UI**: The entire state of the screen is derived directly from the central `game_state`.
- **Tie Resolution**: Unlike the deployment phase, ties in the first turn roll-off result in the Attacker choosing who rolls first again, rather than both players rolling again.

# Changelog

## 2024-07-29

- Reconciled documentation to reflect the detailed, multi-step roll-off process for determining the first turn.
- Corrected the screen's purpose from a simple timer/order setup to the interactive roll-off flow.

## 2024-03-21

- Initial documentation (describing a generic and outdated setup flow).
- Linked related API documentation.
