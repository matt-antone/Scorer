# Game Over Screen

# Version History

- v1.0.0 (2024-03-21): Initial version
- v2.0.0 (2024-07-29): Reconciled with detailed behavior documentation.

Last Updated: 2024-07-29 10:00 UTC

# Related Files

- [../app.md](../app.md): Main Kivy application
- [scorer_root_widget.md](./scorer_root_widget.md): Previous screen
- [name_entry_screen.md](./name_entry_screen.md): Next screen for new game
- [../../api/state_server/state_management.md](../../api/state_server/state_management.md): State management API

# Overview

The `GameOverScreen` is the final screen in the gameplay loop. It appears automatically when the game's end condition is met, displaying the final results and providing the user with options for what to do next.

# Purpose

- Automatically appear when the game ends.
- Display the final scores for both players.
- Prominently declare the winner or a draw.
- Provide options to start a new game or exit the application.

# Properties

- `result_status_label`: A prominent label to declare the winner or a draw.
- `p1_final_name_label` / `p2_final_name_label`: Labels for player names.
- `p1_final_score_label` / `p2_final_score_label`: Labels for final total scores.
- `p1_final_cp_label` / `p2_final_cp_label`: Labels for final Command Points.
- `p1_final_time_label` / `p2_final_time_label`: Labels for each player's final elapsed time.
- `p1_role_label` / `p2_role_label`: Labels showing each player's role (Attacker/Defender).
- `total_game_time_label`: A label for the total game duration.
- `rounds_played_label`: A label showing the total number of rounds played.
- `new_game_button`: A button to start a new game.
- `exit_button`: A button to exit the application.

# Methods

- `on_pre_enter()`: Handles screen entry and calls a method to populate all labels from the final `game_state`.
- `start_new_game()`: Handles the "New Game" button press, calling the controller to reset the game state.
- `exit_app_from_game_over()`: Handles the "Exit" button press, calling `App.get_running_app().stop()`.

# Events

- `on_new_game`: Fired when the "New Game" button is pressed.
- `on_exit_app`: Fired when the "Exit" button is pressed.

# Behavior & Flow

## Appearance Condition

- This screen is shown automatically when the `end_turn` logic in the `ScorerApp` controller determines that the game is over.
- The specific trigger is when the second player completes their turn in Round 5, or a player concedes.
- The `game_phase` in the central `game_state` is set to `'game_over'`, which causes the `ScreenManager` to switch to this screen.

## User Interaction

- **Starting a New Game**:
  - Pressing the "New Game" button triggers the `start_new_game_flow` method in the `ScorerApp` controller.
  - This method resets the central `game_state` to its initial values.
  - The application then transitions to the `NameEntryScreen` to begin the setup for a fresh game.
- **Exiting the Application**:
  - Pressing the "Exit" button calls `App.get_running_app().stop()`, which safely terminates the Kivy application.

# Screen Transition

- **To this screen**: Transitions automatically from `ScorerRootWidget` when the game ends.
- **From this screen**:
  - Transitions to `NameEntryScreen` if the user chooses "New Game".
  - Exits the application if the user chooses "Exit".

# Key Implementation Details

- **File Location**: `screens/game_over_screen.py`
- **Fully Implemented**: The "New Game" and "Exit" buttons have fully implemented functionality, managed by the `ScorerApp` controller.
- **State-Driven**: The appearance of this screen and all the data it displays are entirely driven by the final `game_state`.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.

# Changelog

## 2024-07-29

- Reconciled developer-focused documentation with user-facing behavioral documentation.
- Clarified the properties to match the actual labels on the screen.
- Integrated the detailed `Behavior & Flow` and `Key Implementation Details`.

## 2024-03-21

- Initial documentation
- Added overview, properties, methods, and flow
- Added results display
- Added statistics calculation
- Added new game and exit handling
- Added error handling
- Linked related API documentation
