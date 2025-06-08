# Player Client

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [observer_client.md](./observer_client.md): Observer client implementation
- [client_state.md](./client_state.md): Client state management
- [client_network.md](./client_network.md): Client network handling
- [client_security.md](./client_security.md): Client security implementation
- [../../api/websocket/events.md](../../api/websocket/events.md): WebSocket events API
- [../../api/state_server/state_management.md](../../api/state_server/state_management.md): State management API

# Overview

The Player Client is responsible for managing the player's interaction with the game. It handles player input, displays game state, and communicates with the server to update game progress.

# Purpose

- Handle player input
- Display game state
- Manage player actions
- Communicate with server
- Update game progress

# Properties

- `client_id`: Unique client identifier
- `game_state`: Current game state
  ```json
  {
    "game_id": "string",
    "player_id": "string",
    "player_name": "string",
    "role": "player",
    "status": "string",
    "score": number,
    "timer": number,
    "is_current_player": boolean,
    "last_action": "string",
    "last_action_time": "ISO8601"
  }
  ```
- `settings`: Client configuration
  ```json
  {
    "server_url": "string",
    "reconnect_attempts": number,
    "reconnect_delay": number,
    "heartbeat_interval": number,
    "auto_reconnect": boolean,
    "debug_mode": boolean
  }
  ```
- `ui_state`: UI state management
  ```json
  {
    "current_screen": "string",
    "screen_history": ["string"],
    "ui_theme": "string",
    "animations_enabled": boolean,
    "sound_enabled": boolean,
    "vibration_enabled": boolean
  }
  ```

# Methods

- `initializeClient(settings)`: Initialize client
- `connectToServer()`: Connect to game server
- `disconnectFromServer()`: Disconnect from server
- `handlePlayerAction(action)`: Handle player action
- `updateGameState(state)`: Update game state
- `updateUIState(state)`: Update UI state
- `handleServerMessage(message)`: Handle server message
- `handleError(error)`: Handle client error
- `saveClientState()`: Save client state
- `loadClientState()`: Load client state

# Events

- `client_initialized`: Fired when client is initialized
- `server_connected`: Fired when connected to server
- `server_disconnected`: Fired when disconnected from server
- `game_state_updated`: Fired when game state is updated
- `player_action_performed`: Fired when player performs action
- `ui_state_updated`: Fired when UI state is updated
- `server_message_received`: Fired when message is received
- `error_occurred`: Fired when error occurs

# Flow

1. Client initializes with settings
2. Connects to game server
3. Receives initial game state
4. Handles player input
5. Updates game state
6. Communicates with server

# Example Usage

```javascript
// player-client.js
class PlayerClient {
  constructor() {
    this.client_id = generateClientId();
    this.game_state = null;
    this.settings = {
      server_url: "ws://localhost:8080",
      reconnect_attempts: 5,
      reconnect_delay: 1000,
      heartbeat_interval: 5000,
      auto_reconnect: true,
      debug_mode: false,
    };
    this.ui_state = {
      current_screen: "splash",
      screen_history: [],
      ui_theme: "default",
      animations_enabled: true,
      sound_enabled: true,
      vibration_enabled: true,
    };
  }

  async initializeClient(settings) {
    try {
      this.settings = { ...this.settings, ...settings };
      await this.loadClientState();
      this.emit("client_initialized", { clientId: this.client_id });
      await this.connectToServer();
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async connectToServer() {
    try {
      this.websocket = new WebSocket(this.settings.server_url);

      this.websocket.onopen = () => {
        this.emit("server_connected", { timestamp: new Date().toISOString() });
        this.startHeartbeat();
      };

      this.websocket.onclose = () => {
        this.emit("server_disconnected", {
          timestamp: new Date().toISOString(),
        });
        if (this.settings.auto_reconnect) {
          this.reconnect();
        }
      };

      this.websocket.onmessage = (event) => {
        this.handleServerMessage(JSON.parse(event.data));
      };

      this.websocket.onerror = (error) => {
        this.handleError(error);
      };
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async handlePlayerAction(action) {
    try {
      if (!this.game_state || !this.game_state.is_current_player) {
        throw new Error("Not your turn");
      }

      const actionData = {
        type: action.type,
        data: action.data,
        player_id: this.game_state.player_id,
        game_id: this.game_state.game_id,
        timestamp: new Date().toISOString(),
      };

      await this.sendToServer(actionData);
      this.emit("player_action_performed", actionData);
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  updateGameState(state) {
    try {
      this.game_state = {
        ...this.game_state,
        ...state,
        last_updated: new Date().toISOString(),
      };

      this.emit("game_state_updated", this.game_state);
      this.updateUIState({ current_screen: this.determineScreen() });
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  updateUIState(state) {
    try {
      this.ui_state = {
        ...this.ui_state,
        ...state,
        screen_history: [...this.ui_state.screen_history, state.current_screen],
      };

      this.emit("ui_state_updated", this.ui_state);
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async handleServerMessage(message) {
    try {
      this.emit("server_message_received", message);

      switch (message.type) {
        case "game_state_update":
          this.updateGameState(message.data);
          break;
        case "player_action":
          this.handlePlayerAction(message.data);
          break;
        case "error":
          this.handleError(message.data);
          break;
        default:
          if (this.settings.debug_mode) {
            console.log("Unknown message type:", message.type);
          }
      }
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  handleError(error) {
    this.emit("error_occurred", {
      error: error.message,
      timestamp: new Date().toISOString(),
    });

    if (this.settings.debug_mode) {
      console.error("Player Client Error:", error);
    }
  }

  async saveClientState() {
    try {
      const state = {
        client_id: this.client_id,
        settings: this.settings,
        ui_state: this.ui_state,
        last_updated: new Date().toISOString(),
      };

      await localStorage.setItem("player_client_state", JSON.stringify(state));
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async loadClientState() {
    try {
      const state = JSON.parse(
        await localStorage.getItem("player_client_state")
      );
      if (state) {
        this.client_id = state.client_id;
        this.settings = { ...this.settings, ...state.settings };
        this.ui_state = { ...this.ui_state, ...state.ui_state };
      }
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  determineScreen() {
    if (!this.game_state) return "splash";

    switch (this.game_state.status) {
      case "waiting":
        return "waiting_screen";
      case "playing":
        return this.game_state.is_current_player
          ? "player_turn"
          : "opponent_turn";
      case "game_over":
        return "game_over";
      default:
        return "splash";
    }
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, methods, and flow
- Added client state management
- Added UI state management
- Added server communication
- Linked related API documentation
