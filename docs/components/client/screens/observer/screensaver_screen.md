# Observer Client Screensaver Screen

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [game_over_screen.md](./game_over_screen.md): Previous screen in flow
- [splash_screen.md](./splash_screen.md): Next screen in flow
- [../../../api/websocket/events.md](../../../api/websocket/events.md): WebSocket events

# Overview

The Observer Client Screensaver Screen is displayed when the app is idle. It shows a screensaver animation and transitions back to the SplashScreen when user interaction is detected.

# Purpose

- Display screensaver animation
- Detect user interaction
- Transition back to SplashScreen

# Properties

- `screensaver_animation`: Animation component
- `touch_area`: Area to detect user interaction

# Events

- `on_touch`: Fired when user interaction is detected

# Flow

1. App becomes idle and ScreensaverScreen is shown
2. Screensaver animation plays
3. User interaction detected
4. Transition back to SplashScreen

# Example Usage

```javascript
// observer-client.js
class ScreensaverScreen {
  onLoad() {
    this.startAnimation();
  }

  startAnimation() {
    this.screensaver_animation.play();
  }

  onTouch() {
    this.navigateTo("splash_screen");
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, events, and flow
- Linked related files
