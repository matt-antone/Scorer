# Observer Client Game Play Screen

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [resume_or_new_screen.md](./resume_or_new_screen.md): Previous screen in flow
- [game_over_screen.md](./game_over_screen.md): Next screen in flow
- [../../../api/websocket/events.md](../../../api/websocket/events.md): WebSocket events

# Overview

The Observer Client Game Play Screen displays the live game state, including scores, timer, and current player. It updates in real-time based on WebSocket events from the state server.

# Purpose

- Display live game state (scores, timer, current player)
- Update UI in real-time based on WebSocket events
- Provide visual feedback on game progress

# Properties

- `score_display`: Component to show player scores
- `timer_display`: Component to show countdown timer
- `current_player_label`: Label to display current player
- `error_message`: Text to display errors (if any)

# Events

- `on_score_update`: Fired when scores change
- `on_timer_update`: Fired when timer updates
- `on_player_change`: Fired when current player changes

# Flow

1. Screen loads and subscribes to WebSocket events
2. UI updates in real-time based on events
3. If game ends, transition to GameOverScreen

# Example Usage

```javascript
// observer-client.js
class GamePlayScreen {
  onLoad() {
    this.subscribeToEvents();
  }

  subscribeToEvents() {
    this.socket.on("score_update", (data) => {
      this.score_display.update(data.scores);
      this.dispatch("on_score_update", data);
    });

    this.socket.on("timer_update", (data) => {
      this.timer_display.update(data.time);
      this.dispatch("on_timer_update", data);
    });

    this.socket.on("player_change", (data) => {
      this.current_player_label.text = data.current_player;
      this.dispatch("on_player_change", data);
    });
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, events, and flow
- Linked related files
