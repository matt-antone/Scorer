# Game Timer System

This document describes the functionality of the main game timer used in the Scorer application.

## 1. Purpose

The primary purpose of the game timer is to help players manage their overall game pace. Warhammer 40k games are often played with a time limit (e.g., 3 hours for a 2000-point game), and a visible clock is essential for ensuring the game can be completed within the allotted time.

## 2. Core Behavior

- **Modes**: The timer only counts up:
  - **Count-up**: Starts from 00:00:00 and counts up, showing the total elapsed time.
- **Controls**: The timer is controlled via buttons on the main Kivy `ScorerRootWidget`. The required controls are:
  - **Start/Pause**: A single button that toggles the timer between running and paused states.

## 3. State Management & Synchronization

The game timer is a critical part of the shared game state and must be managed by the central **State Management Server**.

- **State Representation**: The timer's status is stored within the main `game_state` object. This simplified model uses timestamps to ensure perfect synchronization without needing constant tick updates from the server.

  - `timer_is_running`: `true` or `false`.
  - `timer_start_time_unix`: The UNIX timestamp (seconds since epoch) from when the timer was last started or resumed. It is `null` or `0` if the timer is paused.
  - `timer_accumulated_seconds`: The total elapsed time in seconds that the timer has already run _before_ the current running period. This value is updated every time the timer is paused.

- **Actions**: All interactions with the timer are handled as events sent to the State Management Server.

  - Pressing the Start/Pause button on the Kivy UI fires a `{'action': 'toggle_timer'}` event.

- **Logic**: The State Management Server contains the logic to handle the `toggle_timer` action.
  - **On Start/Resume**: It sets `timer_is_running` to `true` and records the current `timer_start_time_unix`.
  - **On Pause**: It sets `timer_is_running` to `false`, calculates the elapsed time since `timer_start_time_unix`, adds it to `timer_accumulated_seconds`, and then clears `timer_start_time_unix`.
- **Synchronization**: The server broadcasts the timer state (`timer_is_running`, `timer_start_time_unix`, `timer_accumulated_seconds`) to all clients. Each client is responsible for calculating the current display time locally.
  - **Display Calculation**: `display_time = timer_accumulated_seconds + (current_unix_time() - timer_start_time_unix if timer_is_running else 0)`

## 4. UI Implementation

- **Kivy**: The main timer display and its control (`Start/Pause`) is located on the `ScorerRootWidget`.
- **Web Clients**: The observer and player clients will display the synchronized time from the `game_state` but will not have controls to modify the timer. The timer is controlled exclusively from the host Kivy application.
