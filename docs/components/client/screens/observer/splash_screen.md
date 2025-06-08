# Observer Client Splash Screen

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [resume_or_new_screen.md](./resume_or_new_screen.md): Next screen in flow
- [../../../api/websocket/events.md](../../../api/websocket/events.md): WebSocket events

# Overview

The Observer Client Splash Screen is the initial screen shown when the observer client (web app) launches. It performs network checks, connects to the state server, and transitions to the next screen when ready.

# Purpose

- Display loading animation
- Check network connectivity
- Connect to state server
- Transition to ResumeOrNewScreen or error screen

# Properties

- `loading_spinner`: Spinner to indicate loading
- `status_text`: Text to display current status
- `error_message`: Text to display errors (if any)

# Events

- `on_loading_complete`: Fired when connection is established
- `on_error`: Fired if connection fails

# Flow

1. Observer client launches and shows SplashScreen
2. Network and server connection checks run
3. If successful, transition to ResumeOrNewScreen
4. If error, show error message and retry/exit options

# Example Usage

```javascript
// observer-client.js
class SplashScreen {
  async onLoad() {
    try {
      await this.checkConnection();
      this.dispatch("on_loading_complete");
    } catch (error) {
      this.dispatch("on_error", error.message);
    }
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, events, and flow
- Linked related files
