# Client Network Handling

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [player_client.md](./player_client.md): Player client implementation
- [observer_client.md](./observer_client.md): Observer client implementation
- [client_state.md](./client_state.md): Client state management
- [client_security.md](./client_security.md): Client security implementation
- [../../api/websocket/events.md](../../api/websocket/events.md): WebSocket events API
- [../../api/network_server/network_management.md](../../api/network_server/network_management.md): Network management API

# Overview

The Client Network Handling component is responsible for managing network connections, handling WebSocket communication, and ensuring reliable data transfer between the client and server.

# Purpose

- Manage network connections
- Handle WebSocket communication
- Ensure reliable data transfer
- Monitor connection health
- Handle reconnection logic

# Properties

- `connection`: Current connection state
  ```json
  {
    "status": "string",
    "websocket": "WebSocket",
    "url": "string",
    "protocol": "string",
    "last_heartbeat": "ISO8601",
    "latency": number,
    "reconnect_attempts": number
  }
  ```
- `settings`: Network settings
  ```json
  {
    "server": {
      "url": "string",
      "protocol": "string",
      "timeout": number
    },
    "reconnection": {
      "enabled": boolean,
      "max_attempts": number,
      "delay": number,
      "backoff_factor": number
    },
    "heartbeat": {
      "enabled": boolean,
      "interval": number,
      "timeout": number
    },
    "security": {
      "enabled": boolean,
      "token": "string",
      "encryption": boolean
    }
  }
  ```

# Methods

- `initializeConnection(settings)`: Initialize connection
- `connect()`: Connect to server
- `disconnect()`: Disconnect from server
- `sendMessage(message)`: Send message to server
- `handleMessage(message)`: Handle incoming message
- `startHeartbeat()`: Start heartbeat
- `stopHeartbeat()`: Stop heartbeat
- `handleReconnection()`: Handle reconnection
- `handleError(error)`: Handle network error
- `updateConnectionState(state)`: Update connection state

# Events

- `connection_initialized`: Fired when connection is initialized
- `connection_established`: Fired when connection is established
- `connection_lost`: Fired when connection is lost
- `connection_restored`: Fired when connection is restored
- `message_sent`: Fired when message is sent
- `message_received`: Fired when message is received
- `heartbeat_sent`: Fired when heartbeat is sent
- `heartbeat_received`: Fired when heartbeat is received
- `error_occurred`: Fired when error occurs

# Flow

1. Initialize connection with settings
2. Connect to server
3. Start heartbeat
4. Handle messages
5. Monitor connection
6. Handle reconnection
7. Handle errors

# Example Usage

```javascript
// client-network.js
class ClientNetworkManager {
  constructor() {
    this.connection = null;
    this.settings = {
      server: {
        url: "ws://localhost:8080",
        protocol: "game-protocol",
        timeout: 5000,
      },
      reconnection: {
        enabled: true,
        max_attempts: 5,
        delay: 1000,
        backoff_factor: 1.5,
      },
      heartbeat: {
        enabled: true,
        interval: 30000,
        timeout: 5000,
      },
      security: {
        enabled: true,
        token: "",
        encryption: true,
      },
    };
  }

  async initializeConnection(settings) {
    try {
      this.settings = { ...this.settings, ...settings };
      this.connection = {
        status: "initializing",
        websocket: null,
        url: this.settings.server.url,
        protocol: this.settings.server.protocol,
        last_heartbeat: null,
        latency: 0,
        reconnect_attempts: 0,
      };

      this.emit("connection_initialized", this.connection);
      await this.connect();
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async connect() {
    try {
      this.connection.websocket = new WebSocket(
        this.settings.server.url,
        this.settings.server.protocol
      );

      this.connection.websocket.onopen = () => {
        this.updateConnectionState({
          status: "connected",
          last_heartbeat: new Date().toISOString(),
        });

        this.emit("connection_established", this.connection);
        this.startHeartbeat();
      };

      this.connection.websocket.onclose = () => {
        this.updateConnectionState({
          status: "disconnected",
          websocket: null,
        });

        this.emit("connection_lost", this.connection);
        this.handleReconnection();
      };

      this.connection.websocket.onmessage = (event) => {
        this.handleMessage(JSON.parse(event.data));
      };

      this.connection.websocket.onerror = (error) => {
        this.handleError(error);
      };
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  disconnect() {
    try {
      if (this.connection.websocket) {
        this.connection.websocket.close();
      }

      this.stopHeartbeat();
      this.updateConnectionState({
        status: "disconnected",
        websocket: null,
      });
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async sendMessage(message) {
    try {
      if (
        !this.connection.websocket ||
        this.connection.status !== "connected"
      ) {
        throw new Error("Not connected to server");
      }

      const messageToSend = {
        ...message,
        timestamp: new Date().toISOString(),
      };

      if (this.settings.security.enabled) {
        messageToSend.token = this.settings.security.token;
      }

      this.connection.websocket.send(JSON.stringify(messageToSend));
      this.emit("message_sent", messageToSend);
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  handleMessage(message) {
    try {
      if (message.type === "heartbeat") {
        this.handleHeartbeat(message);
        return;
      }

      this.emit("message_received", message);
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  startHeartbeat() {
    try {
      if (!this.settings.heartbeat.enabled) return;

      if (this.heartbeatInterval) {
        clearInterval(this.heartbeatInterval);
      }

      this.heartbeatInterval = setInterval(() => {
        this.sendMessage({
          type: "heartbeat",
          timestamp: new Date().toISOString(),
        });

        this.emit("heartbeat_sent", {
          timestamp: new Date().toISOString(),
        });
      }, this.settings.heartbeat.interval);
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  stopHeartbeat() {
    try {
      if (this.heartbeatInterval) {
        clearInterval(this.heartbeatInterval);
        this.heartbeatInterval = null;
      }
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  handleHeartbeat(message) {
    try {
      const now = new Date().getTime();
      const sent = new Date(message.timestamp).getTime();
      const latency = now - sent;

      this.updateConnectionState({
        last_heartbeat: new Date().toISOString(),
        latency,
      });

      this.emit("heartbeat_received", {
        timestamp: new Date().toISOString(),
        latency,
      });
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async handleReconnection() {
    try {
      if (!this.settings.reconnection.enabled) return;

      if (
        this.connection.reconnect_attempts >=
        this.settings.reconnection.max_attempts
      ) {
        this.emit("error_occurred", {
          type: "max_reconnect_attempts",
          message: "Maximum reconnection attempts reached",
        });
        return;
      }

      const delay =
        this.settings.reconnection.delay *
        Math.pow(
          this.settings.reconnection.backoff_factor,
          this.connection.reconnect_attempts
        );

      await new Promise((resolve) => setTimeout(resolve, delay));

      this.connection.reconnect_attempts++;
      await this.connect();
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  handleError(error) {
    this.emit("error_occurred", {
      type: "network_error",
      message: error.message,
      timestamp: new Date().toISOString(),
    });
  }

  updateConnectionState(state) {
    try {
      this.connection = {
        ...this.connection,
        ...state,
      };
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, methods, and flow
- Added network connection management
- Added WebSocket handling
- Added heartbeat mechanism
- Added reconnection logic
- Linked related API documentation
