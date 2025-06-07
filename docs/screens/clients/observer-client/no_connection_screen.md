# Observer Client Screen: No Connection

## 1. Purpose

The No Connection Screen is a critical piece of user experience for the web client. It serves as a clear, visible indicator that the connection to the WebSocket server has been lost and that the data on screen is no longer live.

## 2. Behavior & Flow

### Appearance Condition

- This screen is not controlled by the `game_phase` like the others. Instead, it is managed directly by the WebSocket client logic.
- It is hidden by default when a connection is active.
- It appears automatically and overlays the entire interface if the WebSocket `disconnect` event is triggered.

### UI Components

- **Clear Message**: The screen displays a prominent, unambiguous message, such as "Connection Lost... Attempting to Reconnect."
- **Overlay**: It typically appears as a semi-transparent overlay (e.g., black with 50% opacity) that covers the entire browser window. This visually signals that the underlying UI is stale and not to be trusted.

## 3. Screen Transition

- **Hiding**: The screen automatically hides itself if the WebSocket `connect` event is triggered, indicating that the client has successfully re-established a connection with the server. Upon reconnecting, the client will request the latest game state, and the appropriate screen (`Setup`, `Game Play`, or `Game Over`) will be displayed with fresh data.
- **Showing**: It appears instantly upon disconnection.

## 4. Key Implementation Details

- **Event-Driven**: The visibility of this screen is tied directly to the core `connect` and `disconnect` events of the Socket.IO client library.
- **Robustness**: This screen is essential for preventing user confusion. Without it, a user might not realize their connection has dropped and could be looking at outdated game information. It provides immediate and clear feedback about the state of the client-server link.
