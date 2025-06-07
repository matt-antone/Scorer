# Observer Client Screen: Resume or New

## 1. Purpose

This screen informs the observer that the host user is currently deciding whether to resume a previous game or start a new one.

## 2. Proposal

- **Behavior**: This screen will be shown when the `game_phase` received from the server is `'resume_or_new'`.
- **UI**: Display a simple, clear status message, such as: "A game is already in progress. Waiting for host to resume or start a new game." This prevents confusion and lets the observer know why the game isn't starting immediately.
- **Transition**: The screen will transition automatically when the host makes a choice.
  - If "Resume" is chosen, the client will switch to the **Game Play Screen**.
  - If "Start New" is chosen, the client will switch to the **Name Entry Screen**.
- **Synchronization**: The appearance of this screen is directly controlled by the Kivy host application's state. When the host is on the `ResumeOrNewScreen`, this client screen will be active.
