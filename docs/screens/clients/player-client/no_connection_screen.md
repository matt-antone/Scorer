# Player Client Screen: No Connection

## 1. Purpose

The No Connection Screen provides an essential, unambiguous visual indicator that the player client's connection to the WebSocket server has been lost. This prevents the player from attempting to modify their score when the client is offline.

## 2. Behavior & Flow

### Appearance Condition

- The screen's visibility is tied directly to the state of the WebSocket connection.
- It is hidden by default.
- It appears automatically as a full-screen overlay the moment the WebSocket client's `disconnect` event is fired.

### UI Components

- **Clear Message**: It displays a simple, direct message like "Connection Lost... Reconnecting."
- **Overlay Style**: It functions as a semi-transparent overlay, visually disabling the underlying control interface to make it clear that the buttons are not currently functional.

## 3. Screen Transition

- **Hiding**: The screen automatically hides itself if a connection is re-established (when the WebSocket `connect` event fires). This restores the visibility and functionality of the main interface.
- **Showing**: Appears instantly upon disconnection.

## 4. Key Implementation Details

- **Event-Driven**: The logic is not based on game state, but on the fundamental `connect` and `disconnect` events of the client's WebSocket library.
- **Prevents Errors**: This screen is crucial for preventing user frustration and data-sync errors. Without it, a player might tap a button multiple times, assuming their score is being updated, when in reality the commands are not being sent to the server. It provides immediate feedback on the health of the connection.
