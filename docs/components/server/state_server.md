# State Server

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [websocket_server.md](./websocket_server.md): WebSocket server for client communication
- [game_state.md](./game_state.md): Game state management
- [../../api/state_server/state_management.md](../../api/state_server/state_management.md): State management API
- [../../api/websocket/events.md](../../api/websocket/events.md): WebSocket events API

# Overview

The State Server is responsible for managing the game state, including scores, timer, and current player. It communicates with clients via WebSocket events and provides a REST API for state management.

# Purpose

- Manage game state (scores, timer, current player)
- Broadcast state updates to clients
- Handle game logic (e.g., determining winner)
- Provide REST API for state management
- Ensure state consistency and validation

# Properties

- `game_state`: Object to store current game state
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
- `clients`: List of connected clients
- `settings`: System configuration
  ```json
  {
    "max_players": number,
    "max_games": number,
    "timeout": number
  }
  ```

# Events

- `score_update`: Broadcasted when scores change
- `timer_update`: Broadcasted when timer updates
- `player_change`: Broadcasted when current player changes
- `game_over`: Broadcasted when game ends
- `connection_status`: Broadcasted when client connection status changes
- `error`: Broadcasted when an error occurs

# Security

- All connections require authentication
- Tokens expire after 24 hours
- Rate limiting per client
- Message validation required
- HTTPS/WSS required in production

# Flow

1. Server initializes and listens for client connections
2. Clients connect and subscribe to state updates
3. Server validates all incoming requests and messages
4. Server updates game state based on client actions
5. Server broadcasts state updates to all clients
6. If game ends, server broadcasts game over event

# Example Usage

```javascript
// state-server.js
class StateServer {
  constructor() {
    this.game_state = {
      scores: { player1: 0, player2: 0 },
      timer: 60,
      current_player: "player1",
    };
    this.clients = [];
  }

  onClientConnect(client) {
    this.clients.push(client);
    client.send("game_state", this.game_state);
  }

  updateScores(scores) {
    this.game_state.scores = scores;
    this.broadcast("score_update", scores);
  }

  updateTimer(time) {
    this.game_state.timer = time;
    this.broadcast("timer_update", time);
  }

  changePlayer(player) {
    this.game_state.current_player = player;
    this.broadcast("player_change", player);
  }

  endGame() {
    this.broadcast("game_over", this.game_state);
  }

  broadcast(event, data) {
    this.clients.forEach((client) => client.send(event, data));
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, events, and flow
- Linked related files
