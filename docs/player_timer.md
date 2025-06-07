# Player Timer System

This document describes the "chess clock" style timer used to track individual player turn times.

## 1. Purpose

The player timer system tracks the total time each player spends on their own turns. This encourages a balanced pace of play and is a common feature in competitive tournament settings.

## 2. Core Behavior

- **Chess-Clock Style**: The system functions like a chess clock. When the main game timer is running, exactly one player's timer is also running: the timer of the currently active player.
- **Control**: The timer is controlled implicitly by the game flow:
  - **End Turn**: When the active player presses the "End Turn" button, their timer stops, and their opponent's timer starts.
  - **Global Pause**: When the main game timer is paused, the active player's timer is also paused. Resuming the main game timer resumes the active player's timer.

## 3. State Management & Synchronization

The player timers are managed by the central **State Management Server** using a timestamp-based model, which works in conjunction with the main game state.

- **State Representation**: The timer status is stored within the main `game_state` object.

  - `p1_accumulated_seconds`: The total time in seconds that Player 1's timer has run across all their previous turns.
  - `p2_accumulated_seconds`: The total time in seconds that Player 2's timer has run across all their previous turns.
  - The system also relies on two existing state properties:
    - `active_player`: (`'p1'` or `'p2'`) Determines which player's clock should be running.
    - `turn_start_time_unix`: The UNIX timestamp recorded when the current turn began. This is set when a player ends their turn, making them the new active player.

- **Actions**:

  - The `end_turn` action is the primary trigger.
  - The `toggle_timer` action (for the main game timer) also implicitly pauses/resumes the active player's timer.

- **Logic**: The State Management Server handles the updates.

  - **On `end_turn`**:
    1.  Calculate the elapsed time for the turn: `elapsed_turn_seconds = current_unix_time() - turn_start_time_unix`.
    2.  Add this time to the accumulated total for the player who just finished their turn (e.g., `p1_accumulated_seconds += elapsed_turn_seconds`).
    3.  Switch the `active_player`.
    4.  Update `turn_start_time_unix` to the current time.
    5.  The server then broadcasts the new state.

- **Synchronization**: Each client is responsible for calculating the current player's display time locally.
  - **Display Calculation for Active Player**: `display_time = active_player_accumulated_seconds + (current_unix_time() - turn_start_time_unix)` (This calculation only happens if the main game timer is not paused).
  - The non-active player's time is simply their stored `accumulated_seconds`.

## 4. UI Implementation

- **Display**: Each player's total elapsed time will be displayed on their respective side of the screen on the following views:
  - Kivy: `ScorerRootWidget`
  - Observer Client: `game_play_screen`
  - Player Client: `main_interface_screen`
- **Controls**: There are no direct controls for the player timers. They are operated entirely through the "End Turn" button and the main game's "Start/Pause" control.
