# Observer Client Resume Or New Screen

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [splash_screen.md](./splash_screen.md): Previous screen in flow
- [game_play_screen.md](./game_play_screen.md): Next screen in flow
- [../../../api/websocket/events.md](../../../api/websocket/events.md): WebSocket events

# Overview

The Observer Client Resume Or New Screen allows the user to resume a previous game or start a new one. It checks for existing game state and presents options accordingly.

# Purpose

- Display options to resume a saved game or start a new game
- Show summary of last game state if available
- Handle user selection and transition to the appropriate screen

# Properties

- `resume_button`: Button to resume previous game
- `new_game_button`: Button to start a new game
- `game_summary_text`: Text to display summary of last game (if any)
- `error_message`: Text to display errors (if any)

# Events

- `on_resume_selected`: Fired when resume is chosen
- `on_new_game_selected`: Fired when new game is chosen

# Flow

1. Screen loads and checks for saved game state
2. If found, enables resume option and shows summary
3. User selects resume or new game
4. Transitions to GamePlayScreen or loads previous state

# Example Usage

```javascript
// observer-client.js
class ResumeOrNewScreen {
  async onLoad() {
    const savedGame = await this.checkSavedGame();
    if (savedGame) {
      this.resume_button.disabled = false;
      this.game_summary_text.text = this.getGameSummary(savedGame);
    } else {
      this.resume_button.disabled = true;
    }
  }

  onResumeSelected() {
    // Load previous game state
  }

  onNewGameSelected() {
    // Start new game flow
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, events, and flow
- Linked related files
