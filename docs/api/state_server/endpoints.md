# State Server API Endpoints

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [state_management.md](./state_management.md): State management documentation
- [examples.md](./examples.md): Usage examples
- [../websocket/endpoints.md](../websocket/endpoints.md): WebSocket API endpoints

## Overview

The State Server API provides endpoints for managing game state, player state, and system state. It handles the communication between the Kivy app, client applications, and the state server.

## Base URL

```
http://{host}:{port}/api/v1
```

## Authentication

All endpoints require authentication using a Bearer token:

```
Authorization: Bearer {token}
```

## Endpoints

### Game Management

#### GET /games

Get all active games.

**Response:**

```json
{
  "games": [
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
  ],
  "timestamp": "ISO8601"
}
```

#### POST /games

Create a new game.

**Request Body:**

```json
{
  "settings": {
    "timer_duration": number,
    "max_score": number,
    "game_type": "string"
  }
}
```

**Response:**

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

#### GET /games/{game_id}

Get a specific game.

**Parameters:**

- `game_id` (path): Unique game identifier

**Response:**

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

#### DELETE /games/{game_id}

Delete a game.

**Parameters:**

- `game_id` (path): Unique game identifier

**Response:**

```json
{
  "success": boolean,
  "message": "string",
  "timestamp": "ISO8601"
}
```

### Game State Management

#### GET /game-state/{game_id}

Get game state.

**Parameters:**

- `game_id` (path): Unique game identifier

**Response:**

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

#### POST /game-state/{game_id}

Update game state.

**Parameters:**

- `game_id` (path): Unique game identifier

**Request Body:**

```json
{
  "state": {
    "status": "string",
    "current_player": "string",
    "scores": {
      "player1": number,
      "player2": number
    },
    "timer": number
  }
}
```

**Response:**

```json
{
  "success": boolean,
  "message": "string",
  "timestamp": "ISO8601"
}
```

### Player Management

#### GET /players/{game_id}

Get all players in a game.

**Parameters:**

- `game_id` (path): Unique game identifier

**Response:**

```json
{
  "players": [
    {
      "player_id": "string",
      "game_id": "string",
      "name": "string",
      "role": "string",
      "status": "string",
      "score": number,
      "created_at": "ISO8601",
      "updated_at": "ISO8601"
    }
  ],
  "timestamp": "ISO8601"
}
```

#### POST /players/{game_id}

Add a player to a game.

**Parameters:**

- `game_id` (path): Unique game identifier

**Request Body:**

```json
{
  "name": "string",
  "role": "string"
}
```

**Response:**

```json
{
  "player_id": "string",
  "game_id": "string",
  "name": "string",
  "role": "string",
  "status": "string",
  "score": number,
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

#### GET /player-state/{player_id}

Get player state.

**Parameters:**

- `player_id` (path): Unique player identifier

**Response:**

```json
{
  "player_id": "string",
  "game_id": "string",
  "name": "string",
  "role": "string",
  "status": "string",
  "score": number,
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

#### POST /player-state/{player_id}

Update player state.

**Parameters:**

- `player_id` (path): Unique player identifier

**Request Body:**

```json
{
  "state": {
    "status": "string",
    "score": number
  }
}
```

**Response:**

```json
{
  "success": boolean,
  "message": "string",
  "timestamp": "ISO8601"
}
```

### System Configuration

#### GET /config

Get system configuration.

**Response:**

```json
{
  "settings": {
    "max_players": number,
    "max_games": number,
    "timeout": number
  },
  "timestamp": "ISO8601"
}
```

#### PUT /config

Update system configuration.

**Request Body:**

```json
{
  "settings": {
    "max_players": number,
    "max_games": number,
    "timeout": number
  }
}
```

**Response:**

```json
{
  "success": boolean,
  "message": "string",
  "timestamp": "ISO8601"
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request

```json
{
  "error": "string",
  "message": "string",
  "timestamp": "ISO8601"
}
```

### 401 Unauthorized

```json
{
  "error": "string",
  "message": "string",
  "timestamp": "ISO8601"
}
```

### 404 Not Found

```json
{
  "error": "string",
  "message": "string",
  "timestamp": "ISO8601"
}
```

### 500 Internal Server Error

```json
{
  "error": "string",
  "message": "string",
  "timestamp": "ISO8601"
}
```

## Rate Limits

- 100 requests per minute per IP
- 1000 requests per hour per IP
- Burst limit: 10 requests per second

## Security

- All endpoints require HTTPS in production
- Tokens expire after 24 hours
- Rate limiting per IP
- Input validation required

## Examples

See [examples.md](./examples.md) for detailed usage examples.

# Change Log

## 2024-03-21

- Initial documentation
- Added game management endpoints
- Added game state management endpoints
- Added player management endpoints
- Added system configuration endpoints
- Added error responses
- Added rate limits
