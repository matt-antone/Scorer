# WebSocket API Endpoints

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [events.md](./events.md): WebSocket event documentation
- [examples.md](./examples.md): Usage examples
- [../state_server/endpoints.md](../state_server/endpoints.md): State server endpoints

## Overview

The WebSocket API provides real-time communication between the Kivy app, client applications, and the state server. It handles game state synchronization, player actions, and system events.

## Connection

### Endpoint

```
ws://{host}:{port}/ws
```

### Parameters

- `host`: Server hostname or IP
- `port`: Server port (default: 8080)

### Headers

```json
{
  "Authorization": "Bearer {token}",
  "Client-Type": "kivy|observer|player",
  "Device-ID": "{device_id}"
}
```

## Events

### Game State Events

#### `game_state_update`

Sent when game state changes.

**Payload:**

```json
{
  "type": "game_state_update",
  "data": {
    "game_id": "string",
    "state": {
      "current_player": "string",
      "scores": {
        "player1": number,
        "player2": number
      },
      "timer": number,
      "status": "string"
    },
    "timestamp": "ISO8601"
  }
}
```

#### `game_state_request`

Request current game state.

**Payload:**

```json
{
  "type": "game_state_request",
  "data": {
    "game_id": "string"
  }
}
```

### Player Events

#### `player_action`

Sent when a player performs an action.

**Payload:**

```json
{
  "type": "player_action",
  "data": {
    "game_id": "string",
    "player_id": "string",
    "action": "string",
    "value": any,
    "timestamp": "ISO8601"
  }
}
```

### System Events

#### `connection_status`

Sent when connection status changes.

**Payload:**

```json
{
  "type": "connection_status",
  "data": {
    "status": "connected|disconnected|reconnecting",
    "reason": "string",
    "timestamp": "ISO8601"
  }
}
```

#### `error`

Sent when an error occurs.

**Payload:**

```json
{
  "type": "error",
  "data": {
    "code": "string",
    "message": "string",
    "details": object,
    "timestamp": "ISO8601"
  }
}
```

## Error Codes

| Code              | Description           | Action                     |
| ----------------- | --------------------- | -------------------------- |
| `AUTH_FAILED`     | Authentication failed | Reconnect with valid token |
| `INVALID_STATE`   | Invalid game state    | Request fresh state        |
| `ACTION_DENIED`   | Action not allowed    | Check game rules           |
| `CONNECTION_LOST` | Connection lost       | Attempt reconnect          |
| `SERVER_ERROR`    | Server error          | Contact support            |

## Rate Limits

- Maximum message size: 1MB
- Maximum messages per second: 50
- Maximum concurrent connections: 100
- Reconnection attempts: 5 with exponential backoff

## Security

- All connections must use WSS in production
- Tokens expire after 24 hours
- Rate limiting per client
- Message validation required

## Examples

See [examples.md](./examples.md) for detailed usage examples.

# Change Log

## 2024-03-21

- Initial documentation
- Added all core endpoints
- Added error codes
- Added rate limits
