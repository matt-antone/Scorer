# Score Display (Kivy)

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [../screens/game_play_screen.md](../screens/game_play_screen.md): Screen using this widget
- [../../../api/websocket/events.md](../../../api/websocket/events.md): WebSocket events

# Overview

The Score Display widget shows the current scores for both players. It updates dynamically as scores change and provides visual feedback.

# Purpose

- Display player scores
- Update scores in real-time
- Provide visual feedback on score changes

# Properties

- `player1_score`: NumericProperty for Player 1 score
- `player2_score`: NumericProperty for Player 2 score
- `score_label1`: Label to display Player 1 score
- `score_label2`: Label to display Player 2 score

# Events

- `on_score_change`: Fired when a player's score changes

# Flow

1. Scores are initialized
2. Scores update dynamically
3. Visual feedback is provided on score changes

# Example Usage

```python
# main.py
class ScoreDisplay(Widget):
    player1_score = NumericProperty(0)
    player2_score = NumericProperty(0)

    def update_score(self, player, score):
        if player == 'player1':
            self.player1_score = score
        else:
            self.player2_score = score
        self.dispatch('on_score_change', player, score)
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, events, and flow
- Linked related files
