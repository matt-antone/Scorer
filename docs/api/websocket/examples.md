# WebSocket API Examples

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [endpoints.md](./endpoints.md): WebSocket API endpoints
- [events.md](./events.md): WebSocket events

## Overview

This document provides practical examples of using the WebSocket API in different scenarios.

## Connection Examples

### 1. Basic Connection

```javascript
// Client-side JavaScript
const ws = new WebSocket("ws://localhost:8080/ws");

ws.onopen = () => {
  console.log("Connected to server");
};

ws.onclose = () => {
  console.log("Disconnected from server");
};

ws.onerror = (error) => {
  console.error("WebSocket error:", error);
};
```

### 2. Connection with Authentication

```javascript
// Client-side JavaScript
const token = "your-auth-token";
const deviceId = "unique-device-id";

const ws = new WebSocket("ws://localhost:8080/ws", {
  headers: {
    Authorization: `Bearer ${token}`,
    "Client-Type": "player",
    "Device-ID": deviceId,
  },
});
```

## Game State Examples

### 1. Requesting Game State

```javascript
// Client-side JavaScript
function requestGameState(gameId) {
  const message = {
    type: "game_state_request",
    data: {
      game_id: gameId,
    },
  };
  ws.send(JSON.stringify(message));
}
```

### 2. Handling Game State Updates

```javascript
// Client-side JavaScript
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);

  if (message.type === "game_state_update") {
    const { game_id, state } = message.data;
    updateGameUI(state);
  }
};

function updateGameUI(state) {
  // Update scores
  document.getElementById("player1-score").textContent = state.scores.player1;
  document.getElementById("player2-score").textContent = state.scores.player2;

  // Update timer
  document.getElementById("timer").textContent = state.timer;

  // Update current player
  document.getElementById("current-player").textContent = state.current_player;
}
```

## Player Action Examples

### 1. Sending Player Action

```javascript
// Client-side JavaScript
function sendPlayerAction(gameId, playerId, action, value) {
  const message = {
    type: "player_action",
    data: {
      game_id: gameId,
      player_id: playerId,
      action: action,
      value: value,
      timestamp: new Date().toISOString(),
    },
  };
  ws.send(JSON.stringify(message));
}

// Example usage
sendPlayerAction("game123", "player1", "score_update", 10);
```

### 2. Handling Action Confirmation

```javascript
// Client-side JavaScript
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);

  if (message.type === "action_confirmed") {
    const { game_id, player_id, action, value } = message.data;
    showActionConfirmation(action, value);
  }
};

function showActionConfirmation(action, value) {
  const confirmation = document.getElementById("confirmation");
  confirmation.textContent = `Action ${action} confirmed with value ${value}`;
  confirmation.style.display = "block";
  setTimeout(() => {
    confirmation.style.display = "none";
  }, 3000);
}
```

## Error Handling Examples

### 1. Connection Error Handling

```javascript
// Client-side JavaScript
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

function connect() {
  const ws = new WebSocket("ws://localhost:8080/ws");

  ws.onclose = () => {
    if (reconnectAttempts < maxReconnectAttempts) {
      reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000);
      setTimeout(connect, delay);
    }
  };

  ws.onopen = () => {
    reconnectAttempts = 0;
  };
}
```

### 2. Error Message Handling

```javascript
// Client-side JavaScript
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);

  if (message.type === "error") {
    const { code, message: errorMessage } = message.data;
    handleError(code, errorMessage);
  }
};

function handleError(code, message) {
  switch (code) {
    case "AUTH_FAILED":
      // Handle authentication failure
      redirectToLogin();
      break;
    case "INVALID_STATE":
      // Handle invalid state
      requestGameState(currentGameId);
      break;
    case "ACTION_DENIED":
      // Handle denied action
      showError(message);
      break;
    default:
      // Handle unknown error
      showError("An unexpected error occurred");
  }
}
```

## Timer Examples

### 1. Starting Timer

```javascript
// Client-side JavaScript
function startTimer(duration) {
  const message = {
    type: "timer_start",
    data: {
      game_id: currentGameId,
      duration: duration,
      timestamp: new Date().toISOString(),
    },
  };
  ws.send(JSON.stringify(message));
}
```

### 2. Handling Timer Events

```javascript
// Client-side JavaScript
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);

  if (message.type === "timer_start") {
    const { duration } = message.data;
    startLocalTimer(duration);
  } else if (message.type === "timer_stop") {
    stopLocalTimer();
  }
};

function startLocalTimer(duration) {
  let timeLeft = duration;
  const timerElement = document.getElementById("timer");

  const timer = setInterval(() => {
    timeLeft--;
    timerElement.textContent = timeLeft;

    if (timeLeft <= 0) {
      clearInterval(timer);
      handleTimerComplete();
    }
  }, 1000);
}

function stopLocalTimer() {
  clearInterval(timer);
  document.getElementById("timer").textContent = "0";
}
```

## Best Practices

1. **Error Handling**

   - Always implement error handling
   - Use try-catch blocks
   - Log errors appropriately

2. **State Management**

   - Keep local state in sync
   - Handle race conditions
   - Implement rollback

3. **Performance**

   - Batch updates when possible
   - Use efficient data structures
   - Implement caching

4. **Security**
   - Validate all messages
   - Sanitize user input
   - Use secure connections

# Change Log

## 2024-03-21

- Initial documentation
- Added connection examples
- Added game state examples
- Added player action examples
- Added error handling examples
- Added timer examples
