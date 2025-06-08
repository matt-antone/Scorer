# Client State Management

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [player_client.md](./player_client.md): Player client implementation
- [observer_client.md](./observer_client.md): Observer client implementation
- [client_network.md](./client_network.md): Client network handling
- [client_security.md](./client_security.md): Client security implementation
- [../../api/state_server/state_management.md](../../api/state_server/state_management.md): State management API

# Overview

The Client State Management component is responsible for managing the state of client applications. It provides a centralized way to handle state updates, persistence, and synchronization between different client components.

# Purpose

- Manage client state
- Handle state updates
- Persist state changes
- Synchronize state
- Provide state access

# Properties

- `state`: Current client state
  ```json
  {
    "client": {
      "id": "string",
      "type": "player|observer",
      "name": "string",
      "status": "string",
      "last_active": "ISO8601"
    },
    "game": {
      "id": "string",
      "status": "string",
      "current_player": "string",
      "last_action": "string",
      "last_action_time": "ISO8601"
    },
    "ui": {
      "current_screen": "string",
      "screen_history": ["string"],
      "theme": "string",
      "settings": {
        "animations": boolean,
        "sound": boolean,
        "vibration": boolean
      }
    },
    "network": {
      "connected": boolean,
      "last_heartbeat": "ISO8601",
      "reconnect_attempts": number,
      "latency": number
    }
  }
  ```
- `settings`: State management settings
  ```json
  {
    "persistence": {
      "enabled": boolean,
      "storage_key": "string",
      "auto_save": boolean,
      "save_interval": number
    },
    "synchronization": {
      "enabled": boolean,
      "sync_interval": number,
      "conflict_resolution": "server|client|manual"
    },
    "validation": {
      "enabled": boolean,
      "schema_path": "string",
      "strict_mode": boolean
    }
  }
  ```

# Methods

- `initializeState(initialState)`: Initialize state
- `updateState(updates)`: Update state
- `getState(path)`: Get state value
- `setState(path, value)`: Set state value
- `subscribeToState(path, callback)`: Subscribe to state changes
- `unsubscribeFromState(path, callback)`: Unsubscribe from state changes
- `saveState()`: Save state to storage
- `loadState()`: Load state from storage
- `validateState(state)`: Validate state against schema
- `resolveStateConflict(localState, serverState)`: Resolve state conflicts

# Events

- `state_initialized`: Fired when state is initialized
- `state_updated`: Fired when state is updated
- `state_saved`: Fired when state is saved
- `state_loaded`: Fired when state is loaded
- `state_validation_failed`: Fired when state validation fails
- `state_conflict_detected`: Fired when state conflict is detected

# Flow

1. Initialize state with settings
2. Load persisted state
3. Subscribe to state changes
4. Handle state updates
5. Validate state changes
6. Persist state changes
7. Resolve state conflicts

# Example Usage

```javascript
// client-state.js
class ClientStateManager {
  constructor() {
    this.state = null;
    this.settings = {
      persistence: {
        enabled: true,
        storage_key: "client_state",
        auto_save: true,
        save_interval: 5000,
      },
      synchronization: {
        enabled: true,
        sync_interval: 1000,
        conflict_resolution: "server",
      },
      validation: {
        enabled: true,
        schema_path: "./schemas/client-state.json",
        strict_mode: true,
      },
    };
    this.subscribers = new Map();
  }

  async initializeState(initialState) {
    try {
      this.state = {
        client: {
          id: generateClientId(),
          type: "player",
          name: "",
          status: "initializing",
          last_active: new Date().toISOString(),
        },
        game: {
          id: "",
          status: "waiting",
          current_player: "",
          last_action: "",
          last_action_time: null,
        },
        ui: {
          current_screen: "splash",
          screen_history: [],
          theme: "default",
          settings: {
            animations: true,
            sound: true,
            vibration: true,
          },
        },
        network: {
          connected: false,
          last_heartbeat: null,
          reconnect_attempts: 0,
          latency: 0,
        },
      };

      if (initialState) {
        this.state = { ...this.state, ...initialState };
      }

      await this.loadState();
      this.emit("state_initialized", this.state);

      if (this.settings.persistence.auto_save) {
        this.startAutoSave();
      }
    } catch (error) {
      console.error("Failed to initialize state:", error);
      throw error;
    }
  }

  updateState(updates) {
    try {
      const oldState = { ...this.state };
      this.state = { ...this.state, ...updates };

      if (this.settings.validation.enabled) {
        this.validateState(this.state);
      }

      this.notifySubscribers(oldState, this.state);
      this.emit("state_updated", { oldState, newState: this.state });

      if (this.settings.persistence.auto_save) {
        this.saveState();
      }
    } catch (error) {
      console.error("Failed to update state:", error);
      throw error;
    }
  }

  getState(path) {
    try {
      return path.split(".").reduce((obj, key) => obj[key], this.state);
    } catch (error) {
      console.error("Failed to get state:", error);
      throw error;
    }
  }

  setState(path, value) {
    try {
      const keys = path.split(".");
      const lastKey = keys.pop();
      const target = keys.reduce((obj, key) => obj[key], this.state);
      target[lastKey] = value;

      this.updateState(this.state);
    } catch (error) {
      console.error("Failed to set state:", error);
      throw error;
    }
  }

  subscribeToState(path, callback) {
    try {
      if (!this.subscribers.has(path)) {
        this.subscribers.set(path, new Set());
      }
      this.subscribers.get(path).add(callback);
    } catch (error) {
      console.error("Failed to subscribe to state:", error);
      throw error;
    }
  }

  unsubscribeFromState(path, callback) {
    try {
      if (this.subscribers.has(path)) {
        this.subscribers.get(path).delete(callback);
      }
    } catch (error) {
      console.error("Failed to unsubscribe from state:", error);
      throw error;
    }
  }

  async saveState() {
    try {
      if (!this.settings.persistence.enabled) return;

      const stateToSave = {
        state: this.state,
        timestamp: new Date().toISOString(),
      };

      await localStorage.setItem(
        this.settings.persistence.storage_key,
        JSON.stringify(stateToSave)
      );

      this.emit("state_saved", stateToSave);
    } catch (error) {
      console.error("Failed to save state:", error);
      throw error;
    }
  }

  async loadState() {
    try {
      if (!this.settings.persistence.enabled) return;

      const savedState = await localStorage.getItem(
        this.settings.persistence.storage_key
      );

      if (savedState) {
        const { state, timestamp } = JSON.parse(savedState);

        if (this.settings.validation.enabled) {
          this.validateState(state);
        }

        this.state = { ...this.state, ...state };
        this.emit("state_loaded", { state, timestamp });
      }
    } catch (error) {
      console.error("Failed to load state:", error);
      throw error;
    }
  }

  validateState(state) {
    try {
      if (!this.settings.validation.enabled) return;

      const schema = require(this.settings.validation.schema_path);
      const validation = validate(state, schema);

      if (!validation.valid) {
        this.emit("state_validation_failed", validation.errors);
        if (this.settings.validation.strict_mode) {
          throw new Error("State validation failed");
        }
      }
    } catch (error) {
      console.error("Failed to validate state:", error);
      throw error;
    }
  }

  async resolveStateConflict(localState, serverState) {
    try {
      if (!this.settings.synchronization.enabled) return localState;

      switch (this.settings.synchronization.conflict_resolution) {
        case "server":
          return serverState;
        case "client":
          return localState;
        case "manual":
          this.emit("state_conflict_detected", { localState, serverState });
          return null;
        default:
          return serverState;
      }
    } catch (error) {
      console.error("Failed to resolve state conflict:", error);
      throw error;
    }
  }

  startAutoSave() {
    if (this.autoSaveInterval) {
      clearInterval(this.autoSaveInterval);
    }

    this.autoSaveInterval = setInterval(() => {
      this.saveState();
    }, this.settings.persistence.save_interval);
  }

  notifySubscribers(oldState, newState) {
    this.subscribers.forEach((callbacks, path) => {
      const oldValue = this.getState(path);
      const newValue = this.getState(path);

      if (JSON.stringify(oldValue) !== JSON.stringify(newValue)) {
        callbacks.forEach((callback) => callback(newValue, oldValue));
      }
    });
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, methods, and flow
- Added state management functionality
- Added state persistence
- Added state validation
- Added state synchronization
- Linked related API documentation
