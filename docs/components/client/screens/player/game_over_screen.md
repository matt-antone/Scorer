# Player Client Game Over Screen

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [game_play_screen.md](./game_play_screen.md): Previous screen in flow
- [screensaver_screen.md](./screensaver_screen.md): Next screen in flow
- [../../../api/websocket/events.md](../../../api/websocket/events.md): WebSocket events

# Overview

The Player Client Game Over Screen displays the final game results, including scores, winner, and options to restart or exit. It finalizes the game state and transitions to the screensaver.

# Purpose

- Display final scores and winner
- Provide options to restart or exit
- Finalize game state
- Transition to ScreensaverScreen

# Properties

- `winner_text`: Text to display the winner
- `score_text`: Text to display final scores
- `restart_button`: Button to start a new game
- `exit_button`: Button to exit the app

# Events

- `on_restart`: Fired when restart is selected
- `on_exit`: Fired when exit is selected

# Flow

1. Game ends and GameOverScreen is shown
2. Final scores and winner are displayed
3. User selects restart or exit
4. If restart, transition to ResumeOrNewScreen; if exit, close app

# Example Usage

```javascript
// player-client.js
class GameOverScreen {
  onLoad() {
    this.displayResults();
  }

  displayResults() {
    const winner = this.getWinner();
    this.winner_text.text = `Winner: ${winner}`;
    this.score_text.text = `Scores: ${this.getScores()}`;
  }

  onRestart() {
    this.navigateTo("resume_or_new_screen");
  }

  onExit() {
    this.closeApp();
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, events, and flow
- Linked related files
