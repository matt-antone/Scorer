# WebSocket Server

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [state_server.md](./state_server.md): State server for game state management
- [game_state.md](./game_state.md): Game state management
- [../../api/websocket/events.md](../../api/websocket/events.md): WebSocket events API
- [../../api/websocket/endpoints.md](../../api/websocket/endpoints.md): WebSocket endpoints API

# Overview

The WebSocket Server is responsible for handling client connections and facilitating real-time communication between the server and clients. It uses WebSocket events to broadcast game state updates and handles authentication, rate limiting, and message validation.

# Purpose

- Handle client connections
- Facilitate real-time communication
- Broadcast game state updates
- Manage authentication and security
- Handle message validation and rate limiting

# Properties

- `server`: WebSocket server instance
- `clients`: List of connected clients
- `settings`: Server configuration
  ```json
  {
    "max_message_size": 1048576, // 1MB
    "max_messages_per_second": 50,
    "max_concurrent_connections": 100,
    "reconnection_attempts": 5,
    "reconnection_delay": 1000
  }
  ```

# Events

- `connection`: Fired when a client connects
- `disconnection`: Fired when a client disconnects
- `message`: Fired when a message is received from a client
- `error`: Fired when an error occurs
- `game_state_update`: Broadcasted when game state changes
- `player_action`: Received when a player performs an action
- `timer_start`: Broadcasted when timer starts
- `timer_stop`: Broadcasted when timer stops

# Security

- WSS required in production
- Token authentication required
- Rate limiting per client
- Message size limits
- Connection limits
- Message validation

# Flow

1. Server initializes and listens for client connections
2. Clients connect with authentication token
3. Server validates connection and adds client to list
4. Server handles incoming messages and validates them
5. Server broadcasts game state updates to all clients
6. If a client disconnects, it is removed from the clients list

# Example Usage

```javascript
// websocket-server.js
const WebSocket = require("ws");

class WebSocketServer {
  constructor(port) {
    this.server = new WebSocket.Server({ port });
    this.clients = [];
    this.settings = {
      max_message_size: 1048576, // 1MB
      max_messages_per_second: 50,
      max_concurrent_connections: 100,
      reconnection_attempts: 5,
      reconnection_delay: 1000,
    };
    this.setupEventHandlers();
  }

  setupEventHandlers() {
    this.server.on("connection", (client, request) => {
      if (this.clients.length >= this.settings.max_concurrent_connections) {
        client.close(1008, "Maximum connections reached");
        return;
      }

      const token = this.validateToken(request);
      if (!token) {
        client.close(1008, "Invalid token");
        return;
      }

      this.clients.push(client);

      client.on("message", (message) => {
        if (message.length > this.settings.max_message_size) {
          client.send(
            JSON.stringify({
              type: "error",
              data: {
                code: "MESSAGE_TOO_LARGE",
                message: "Message exceeds maximum size",
              },
            })
          );
          return;
        }
        this.handleMessage(client, message);
      });

      client.on("close", () => {
        this.clients = this.clients.filter((c) => c !== client);
      });

      client.on("error", (error) => {
        console.error("WebSocket error:", error);
        this.handleError(client, error);
      });
    });
  }

  validateToken(request) {
    const authHeader = request.headers["authorization"];
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return null;
    }
    const token = authHeader.split(" ")[1];
    // Validate token logic here
    return token;
  }

  handleMessage(client, message) {
    try {
      const data = JSON.parse(message);
      this.validateMessage(data);
      // Handle message based on type
      switch (data.type) {
        case "game_state_request":
          this.handleGameStateRequest(client, data);
          break;
        case "player_action":
          this.handlePlayerAction(client, data);
          break;
        default:
          this.sendError(
            client,
            "INVALID_MESSAGE_TYPE",
            "Unknown message type"
          );
      }
    } catch (error) {
      this.sendError(client, "INVALID_MESSAGE", error.message);
    }
  }

  validateMessage(message) {
    if (!message.type || !message.data) {
      throw new Error("Invalid message format");
    }
    // Additional validation based on message type
  }

  handleError(client, error) {
    this.sendError(client, "SERVER_ERROR", error.message);
  }

  sendError(client, code, message) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(
        JSON.stringify({
          type: "error",
          data: {
            code: code,
            message: message,
            timestamp: new Date().toISOString(),
          },
        })
      );
    }
  }

  broadcast(event, data) {
    const message = {
      type: event,
      data: data,
      timestamp: new Date().toISOString(),
    };
    this.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify(message));
      }
    });
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, events, and flow
- Added security measures
- Added message validation
- Added detailed configuration
- Linked related API documentation
