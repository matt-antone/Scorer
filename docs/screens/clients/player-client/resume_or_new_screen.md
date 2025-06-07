# Player Client Screen: Resume or New

## 1. Purpose

To inform the connected player that the host is deciding whether to resume a previous game or start a new one.

## 2. Proposal

- **Behavior**: Shown when the `game_phase` is `'resume_or_new'`.
- **UI**: A simple, non-interactive status screen. It should display a message like: "Host is choosing to resume or start a new game. Please wait." This prevents the player from thinking their client is stuck.
- **Transition**: Transitions automatically based on the host's choice.
  - If "Resume" is chosen, the client will switch to the main interactive scoreboard.
  - If "Start New" is chosen, the client will switch to the Name Entry view.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `ResumeOrNewScreen`, this client screen will be active.
