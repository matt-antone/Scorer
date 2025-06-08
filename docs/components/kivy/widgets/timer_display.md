# Timer Display (Kivy)

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [../screens/game_play_screen.md](../screens/game_play_screen.md): Screen using this widget
- [../../../api/websocket/events.md](../../../api/websocket/events.md): WebSocket events

# Overview

The Timer Display widget shows a countdown timer for the game. It updates in real-time and triggers events when the timer reaches zero.

# Purpose

- Display countdown timer
- Update timer in real-time
- Trigger events on timer completion

# Properties

- `time_remaining`: NumericProperty for remaining time
- `timer_label`: Label to display the time
- `timer_trigger`: Event triggered when timer reaches zero

# Events

- `on_timer_complete`: Fired when timer reaches zero

# Flow

1. Timer is initialized with a duration
2. Timer updates every second
3. When timer reaches zero, `on_timer_complete` is triggered

# Example Usage

```python
# main.py
class TimerDisplay(Widget):
    time_remaining = NumericProperty(0)

    def start_timer(self, duration):
        self.time_remaining = duration
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        if self.time_remaining > 0:
            self.time_remaining -= 1
        else:
            self.dispatch('on_timer_complete')
            return False
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, events, and flow
- Linked related files
