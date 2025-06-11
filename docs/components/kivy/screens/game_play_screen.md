# Game Play Screen (ScorerRootWidget)

# Version History

- v1.0.0 (2024-03-21): Initial version (describing an incorrect unit-based game)
- v2.0.0 (2024-07-29): Reconciled documentation to reflect the screen's actual function as the main scoreboard and game controller.

Last Updated: 2024-07-29 10:00 UTC

# Related Files

- [../app.md](../app.md): Main Kivy application
- [first_turn_setup_screen.md](./first_turn_setup_screen.md): Previous screen
- [game_over_screen.md](./game_over_screen.md): Next screen
- [screensaver_screen.md](./screensaver_screen.md): Inactivity screen
- [../../game_timer.md](../../game_timer.md): Game Timer System documentation
- [../../player_timer.md](../../player_timer.md): Player Timer System documentation

# Overview

The `GamePlayScreen` (implemented as `ScorerRootWidget`) is the main game interface of the application. It serves as both the central control point and a real-time display of the game state. While players can make changes from their web clients, this screen maintains full control over all game elements and provides a complete view of both players' information.

# Purpose

- Display all primary game state information: scores, CPs, timers, and round.
- Provide Kivy host controls for all game actions (scoring, CP changes, ending turn).
- Act as the authoritative source for game progression (ending turns, ending the game).
- Synchronize its state with all connected web clients in real-time.

# Properties

- **Header**
  - `header_round_label`: Displays the current game round (1-5).
  - `header_total_time_label`: Displays the total elapsed game time.
- **Player 1 / Player 2 Columns**
  - `p1_name_label` / `p2_name_label`: Displays player's name.
  - `p1_score_label` / `p2_score_label`: A button displaying the player's total score.
  - `p1_cp_label` / `p2_cp_label`: A label displaying the player's current Command Points.
  - `p1_player_timer_label` / `p2_player_timer_label`: Displays the player's individual elapsed time.
  - `p1_end_turn_button` / `p2_end_turn_button`: A button to end the current turn.
  - `p1_concede_button` / `p2_concede_button`: A button to concede the game.
  - `p1_role_label` / `p2_role_label`: Displays the player's role (Attacker/Defender).

# Methods

- `update_ui_from_state()`: The core method to populate all UI elements from the central `game_state`.
- `open_score_numpad(player_id)`: Opens a popup numpad for score entry.
- `process_numpad_value(...)`: Processes the value from the numpad and updates the score.
- `add_cp(player_id, amount)` / `remove_cp(player_id, amount)`: Modify Command Points.
- `end_turn(outgoing_player_id)`: Manages the logic for ending a player's turn, switching active players, and incrementing the round.
- `player_concedes(conceding_player_id)`: Opens a confirmation popup and handles the concession logic.
- `start_timer()` / `stop_timer()`: Controls the main game timer.
- `update_timer_display(dt)`: The scheduled method that updates all timer labels on screen.

# Events

- `on_score_change`: Fired when a player's score is updated.
- `on_cp_change`: Fired when a player's CP is updated.
- `on_turn_end`: Fired when the "End Turn" button is processed.
- `on_concede`: Fired when a player confirms concession.
- `on_game_over`: Fired when the game ends after the final round.

# Behavior & Flow

## Initialization

- The screen is divided into the standard "Red vs. Blue" two-column layout.
- When the screen appears, its `update_view_from_state()` method is called to populate all UI elements.

## Interaction & Game Logic

1. **Score and CP Updates**:

   - Changes can be made from the Kivy host or a player's web client.
   - The host UI provides buttons for CP changes and a numpad popup for score changes.
   - All changes are reflected across all clients in real-time.

2. **Turn Management**:

   - The active player's side is visually highlighted.
   - The `end_turn` button is the primary mechanism for game progression.
   - When a turn ends, the active player switches. If the second player's turn ends, the round counter increments.

3. **Game End Condition**:
   - The game automatically ends and transitions to the `GameOverScreen` after the second player finishes their turn in Round 5.
   - A player can also end the game by pressing their `Concede` button and confirming in the popup.

# Key Implementation Details

- **File Location**: `screens/scorer_root_widget.py`
- **Central Hub**: This is the most complex and interactive screen in the application.
- **Controller-Responder Pattern**: It strictly follows this pattern. All button presses call handler methods on the `ScorerApp` controller. The `ScorerRootWidget` is then responsible for visually representing the resulting state from the `game_state` dictionary via its `update_view_from_state` method.
- **Dual Control**: While this screen maintains full control, it also listens for and processes updates initiated from player web clients.
- All widget access is performed via `self.ids.<id>` (matching the widget's id in the .kv file). `ObjectProperty` is not used for widget binding, as per project-wide pattern.

# Changelog

## 2024-07-29

- Reconciled documentation, correcting the screen's purpose from a unit-based strategy game to the actual scoreboard implementation.
- Updated all sections (`Overview`, `Purpose`, `Properties`, `Methods`, `Behavior`) to accurately describe the `ScorerRootWidget`.

## 2024-03-21

- Initial documentation (describing an incorrect unit-based game flow).
- Added client integration section for non-existent features.
- Maintained original client functionality.
