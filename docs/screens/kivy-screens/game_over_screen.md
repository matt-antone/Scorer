# Screen: Game Over Screen

## 1. Purpose

The `GameOverScreen` is the final screen in the gameplay loop. It appears automatically when the game's end condition is met, displaying the final results and providing the user with options for what to do next.

## 2. Behavior & Flow

### Appearance Condition

- This screen is shown automatically when the `end_turn` logic in the `ScorerApp` controller determines that the game is over.
- The specific trigger is when the second player completes their turn in Round 5.
- The `game_phase` in the central `game_state` is set to `'game_over'`, which causes the `ScreenManager` to switch to this screen.

### UI Components & Interaction

- **Final Scores**: The screen displays the final scores for both Player 1 and Player 2.
- **Winner Declaration**: A prominent label declares the winner of the game or announces a draw.
- **"New Game" Button**: This button allows users to start a new game.
- **"Exit" Button**: This button allows users to close the Scorer application.

### User Interaction

- **Starting a New Game**:
  - Pressing the "New Game" button triggers the `start_new_game_flow` method in the `ScorerApp` controller.
  - This method resets the central `game_state` to its initial values.
  - The application then transitions to the `NameEntryScreen` to begin the setup for a fresh game.
- **Exiting the Application**:
  - Pressing the "Exit" button calls `App.get_running_app().stop()`, which safely terminates the Kivy application.

## 3. Screen Transition

- **To this screen**: Transitions automatically from `ScorerRootWidget` when the game ends.
- **From this screen**:
  - Transitions to `NameEntryScreen` if the user chooses "New Game".
  - Exits the application if the user chooses "Exit".

## 4. Key Implementation Details

- **File Location**: `screens/game_over_screen.py`
- **Fully Implemented**: The "New Game" and "Exit" buttons have fully implemented functionality, managed by the `ScorerApp` controller.
- **State-Driven**: The appearance of this screen is entirely driven by the `game_phase` property in the central `game_state`.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.
