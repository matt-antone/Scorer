# Network Server

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [state_server.md](./state_server.md): State server implementation
- [websocket_server.md](./websocket_server.md): WebSocket server implementation
- [game_state.md](./game_state.md): Game state management
- [../../api/network/endpoints.md](../../api/network/endpoints.md): Network API endpoints
- [../../api/network/security.md](../../api/network/security.md): Network security API

# Overview

The Network Server is responsible for managing network connections, handling client discovery, and providing network-related services to other server components. It ensures reliable communication between the server and clients.

# Purpose

- Manage network connections
- Handle client discovery
- Provide network services
- Ensure reliable communication
- Monitor network health

# Properties

- `server`: Network server instance
- `clients`: Map of connected clients
  ```json
  {
    "client_id": {
      "client_id": "string",
      "ip": "string",
      "port": number,
      "status": "string",
      "last_seen": "ISO8601",
      "connection_type": "string"
    }
  }
  ```
- `settings`: Network configuration
  ```json
  {
    "port": number,
    "max_connections": number,
    "timeout": number,
    "heartbeat_interval": number,
    "reconnect_attempts": number,
    "reconnect_delay": number
  }
  ```

# Methods

- `startServer(port)`: Start network server
- `stopServer()`: Stop network server
- `handleConnection(client)`: Handle new client connection
- `handleDisconnection(client)`: Handle client disconnection
- `broadcastMessage(message)`: Broadcast message to all clients
- `sendMessage(clientId, message)`: Send message to specific client
- `discoverClients()`: Discover available clients
- `monitorHealth()`: Monitor network health
- `handleError(error)`: Handle network errors

# Events

- `server_started`: Fired when server starts
- `server_stopped`: Fired when server stops
- `client_connected`: Fired when client connects
- `client_disconnected`: Fired when client disconnects
- `message_received`: Fired when message is received
- `message_sent`: Fired when message is sent
- `client_discovered`: Fired when new client is discovered
- `health_updated`: Fired when health status changes
- `error_occurred`: Fired when error occurs

# Flow

1. Server initializes and starts listening
2. Clients connect and are registered
3. Server monitors client health
4. Messages are routed between components
5. Server handles disconnections and errors

# Example Usage

```javascript
// network-server.js
class NetworkServer {
  constructor() {
    this.server = null;
    this.clients = new Map();
    this.settings = {
      port: 8080,
      max_connections: 100,
      timeout: 30000,
      heartbeat_interval: 5000,
      reconnect_attempts: 5,
      reconnect_delay: 1000,
    };
  }

  async startServer(port) {
    try {
      this.server = new Server(port);
      this.setupEventHandlers();
      await this.server.start();
      this.emit("server_started", { port });
      this.startHealthMonitoring();
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  setupEventHandlers() {
    this.server.on("connection", (client) => {
      this.handleConnection(client);
    });

    this.server.on("error", (error) => {
      this.handleError(error);
    });
  }

  handleConnection(client) {
    if (this.clients.size >= this.settings.max_connections) {
      client.disconnect("Maximum connections reached");
      return;
    }

    const clientInfo = {
      client_id: generateClientId(),
      ip: client.ip,
      port: client.port,
      status: "connected",
      last_seen: new Date().toISOString(),
      connection_type: client.type,
    };

    this.clients.set(clientInfo.client_id, clientInfo);
    this.emit("client_connected", clientInfo);

    client.on("message", (message) => {
      this.handleMessage(clientInfo.client_id, message);
    });

    client.on("disconnect", () => {
      this.handleDisconnection(clientInfo.client_id);
    });
  }

  handleDisconnection(clientId) {
    const client = this.clients.get(clientId);
    if (client) {
      client.status = "disconnected";
      client.last_seen = new Date().toISOString();
      this.emit("client_disconnected", client);
    }
  }

  async broadcastMessage(message) {
    const messageData = {
      type: message.type,
      data: message.data,
      timestamp: new Date().toISOString(),
    };

    for (const [clientId, client] of this.clients.entries()) {
      if (client.status === "connected") {
        try {
          await this.sendMessage(clientId, messageData);
        } catch (error) {
          this.handleError(error);
        }
      }
    }
  }

  async sendMessage(clientId, message) {
    const client = this.clients.get(clientId);
    if (!client || client.status !== "connected") {
      throw new Error("Client not connected");
    }

    try {
      await this.server.send(clientId, message);
      this.emit("message_sent", { clientId, message });
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  startHealthMonitoring() {
    setInterval(() => {
      this.monitorHealth();
    }, this.settings.heartbeat_interval);
  }

  monitorHealth() {
    const now = new Date();
    for (const [clientId, client] of this.clients.entries()) {
      const lastSeen = new Date(client.last_seen);
      const timeSinceLastSeen = now - lastSeen;

      if (timeSinceLastSeen > this.settings.timeout) {
        client.status = "disconnected";
        this.emit("health_updated", { clientId, status: "disconnected" });
      }
    }
  }

  handleError(error) {
    this.emit("error_occurred", {
      error: error.message,
      timestamp: new Date().toISOString(),
    });
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, methods, and flow
- Added network monitoring
- Added error handling
- Added health checks
- Linked related API documentation
