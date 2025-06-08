# Game State

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [state_server.md](./state_server.md): State server implementation
- [websocket_server.md](./websocket_server.md): WebSocket server implementation
- [../../api/state_server/state_management.md](../../api/state_server/state_management.md): State management API
- [../../api/websocket/events.md](../../api/websocket/events.md): WebSocket events API

# Overview

The Game State component is responsible for managing the core game state data structure and its lifecycle. It provides methods for state creation, updates, validation, and persistence, ensuring data consistency across the application.

# Purpose

- Define and maintain game state structure
- Validate state changes
- Handle state persistence
- Ensure state consistency
- Provide state recovery mechanisms

# Properties

- `game_state`: Core game state object
  ```json
  {
    "game_id": "string",
    "status": "string",
    "current_player": "string",
    "scores": {
      "player1": number,
      "player2": number
    },
    "timer": number,
    "settings": {
      "timer_duration": number,
      "max_score": number,
      "game_type": "string"
    },
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  }
  ```
- `player_states`: Map of player states
  ```json
  {
    "player_id": {
      "player_id": "string",
      "game_id": "string",
      "name": "string",
      "role": "string",
      "status": "string",
      "score": number,
      "created_at": "ISO8601",
      "updated_at": "ISO8601"
    }
  }
  ```
- `system_state`: System configuration
  ```json
  {
    "system_id": "string",
    "status": "string",
    "version": "string",
    "settings": {
      "max_players": number,
      "max_games": number,
      "timeout": number
    },
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  }
  ```

# Methods

- `createGameState(settings)`: Create new game state
- `updateGameState(gameId, state)`: Update existing game state
- `getGameState(gameId)`: Retrieve game state
- `validateGameState(state)`: Validate game state
- `storeGameState(gameId, state)`: Persist game state
- `recoverGameState(gameId)`: Recover game state
- `createPlayerState(gameId, name, role)`: Create player state
- `updatePlayerState(playerId, state)`: Update player state
- `getPlayerState(playerId)`: Retrieve player state
- `validatePlayerState(state)`: Validate player state
- `storePlayerState(playerId, state)`: Persist player state
- `recoverPlayerState(playerId)`: Recover player state

# Events

- `state_created`: Fired when new state is created
- `state_updated`: Fired when state is updated
- `state_validated`: Fired when state is validated
- `state_stored`: Fired when state is persisted
- `state_recovered`: Fired when state is recovered
- `state_error`: Fired when state operation fails

# Flow

1. Game state is created with initial settings
2. State changes are validated before updates
3. Updates are persisted to storage
4. State is broadcast to connected clients
5. Recovery mechanisms handle state restoration

# Example Usage

```javascript
// game-state.js
class GameState {
  constructor() {
    this.game_states = new Map();
    this.player_states = new Map();
    this.system_state = this.initializeSystemState();
  }

  createGameState(settings) {
    const gameState = {
      game_id: generateGameId(),
      status: "waiting",
      current_player: "player1",
      scores: { player1: 0, player2: 0 },
      timer: settings.timer_duration,
      settings: settings,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    this.validateGameState(gameState);
    this.game_states.set(gameState.game_id, gameState);
    this.emit("state_created", gameState);
    return gameState;
  }

  updateGameState(gameId, state) {
    const currentState = this.game_states.get(gameId);
    if (!currentState) {
      throw new Error("Game state not found");
    }

    const updatedState = {
      ...currentState,
      ...state,
      updated_at: new Date().toISOString(),
    };

    this.validateGameState(updatedState);
    this.game_states.set(gameId, updatedState);
    this.emit("state_updated", updatedState);
    return updatedState;
  }

  validateGameState(state) {
    const required = ["game_id", "status", "current_player", "scores", "timer"];
    for (const field of required) {
      if (!(field in state)) {
        throw new Error(`Missing required field: ${field}`);
      }
    }

    if (state.timer < 0) {
      throw new Error("Timer cannot be negative");
    }

    if (state.scores.player1 < 0 || state.scores.player2 < 0) {
      throw new Error("Scores cannot be negative");
    }

    this.emit("state_validated", state);
    return true;
  }

  async storeGameState(gameId) {
    const state = this.game_states.get(gameId);
    if (!state) {
      throw new Error("Game state not found");
    }

    try {
      await this.persistence.store(gameId, state);
      this.emit("state_stored", state);
    } catch (error) {
      this.emit("state_error", { gameId, error });
      throw error;
    }
  }

  async recoverGameState(gameId) {
    try {
      const state = await this.persistence.recover(gameId);
      this.validateGameState(state);
      this.game_states.set(gameId, state);
      this.emit("state_recovered", state);
      return state;
    } catch (error) {
      this.emit("state_error", { gameId, error });
      throw error;
    }
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, methods, and flow
- Added state validation
- Added persistence mechanisms
- Added recovery mechanisms
- Linked related API documentation
