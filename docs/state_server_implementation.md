# State Server Implementation Plan

## 1. Overview

The state server is responsible for managing game state, player data, and synchronization between the Kivy host and client applications. It uses a SQLite database for persistent storage and provides a WebSocket interface for real-time state management.

## 2. Database Schema

### Game State Table

```sql
CREATE TABLE game_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id TEXT UNIQUE NOT NULL,
    player1_name TEXT NOT NULL,
    player2_name TEXT NOT NULL,
    current_turn INTEGER NOT NULL,
    game_status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Score Table

```sql
CREATE TABLE scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id TEXT NOT NULL,
    player_number INTEGER NOT NULL,
    score INTEGER NOT NULL,
    cp INTEGER NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES game_state(game_id)
);
```

### Timer Table

```sql
CREATE TABLE timers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id TEXT NOT NULL,
    player_number INTEGER NOT NULL,
    time_remaining INTEGER NOT NULL,
    is_running BOOLEAN NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES game_state(game_id)
);
```

### Settings Table

```sql
CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 3. WebSocket Interface

### Connection Management

```python
# Connection states
CONNECTED = 'connected'
DISCONNECTED = 'disconnected'
RECONNECTING = 'reconnecting'

# Client types
HOST = 'host'
PLAYER = 'player'
OBSERVER = 'observer'
```

### Message Types

```python
# System messages
CONNECT = 'connect'
DISCONNECT = 'disconnect'
HEARTBEAT = 'heartbeat'
ERROR = 'error'

# Game messages
GAME_STATE = 'game_state'
SCORE_UPDATE = 'score_update'
TIMER_UPDATE = 'timer_update'
TURN_CHANGE = 'turn_change'
GAME_END = 'game_end'

# Settings messages
SETTINGS_UPDATE = 'settings_update'
```

### Message Format

```json
{
  "type": "message_type",
  "data": {
    // Message specific data
  },
  "timestamp": "ISO8601 timestamp",
  "game_id": "optional_game_id"
}
```

## 4. Implementation Details

### State Server (Python)

```python
import asyncio
import websockets
import json
from datetime import datetime
import uuid

class GameStateServer:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.clients = {}  # game_id -> {client_id -> websocket}
        self.game_states = {}  # game_id -> game_state

    async def handle_connection(self, websocket, path):
        client_id = str(uuid.uuid4())
        try:
            # Handle initial connection
            await self.handle_connect(websocket, client_id)

            # Main message loop
            async for message in websocket:
                await self.handle_message(websocket, client_id, message)

        except websockets.exceptions.ConnectionClosed:
            await self.handle_disconnect(client_id)
        finally:
            await self.cleanup_client(client_id)

    async def handle_connect(self, websocket, client_id):
        # Send initial state
        await websocket.send(json.dumps({
            "type": "connect",
            "data": {"client_id": client_id},
            "timestamp": datetime.utcnow().isoformat()
        }))

    async def handle_message(self, websocket, client_id, message):
        data = json.loads(message)
        message_type = data.get("type")

        if message_type == "game_state":
            await self.handle_game_state(websocket, client_id, data)
        elif message_type == "score_update":
            await self.handle_score_update(websocket, client_id, data)
        # ... handle other message types

    async def broadcast_game_state(self, game_id, state):
        if game_id in self.clients:
            message = {
                "type": "game_state",
                "data": state,
                "timestamp": datetime.utcnow().isoformat(),
                "game_id": game_id
            }
            await self.broadcast_to_game(game_id, message)

    async def broadcast_to_game(self, game_id, message):
        if game_id in self.clients:
            websockets = self.clients[game_id].values()
            await asyncio.gather(
                *[ws.send(json.dumps(message)) for ws in websockets]
            )

async def main():
    db_manager = DatabaseManager('game_state.db')
    server = GameStateServer(db_manager)

    async with websockets.serve(
        server.handle_connection,
        "0.0.0.0",
        8765,
        ping_interval=30,
        ping_timeout=10
    ):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
```

### Client Connection (Python)

```python
class GameClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.ws = None
        self.client_id = None
        self.game_id = None
        self.connected = False

    async def connect(self):
        self.ws = await websockets.connect(self.server_url)
        self.connected = True

        # Start message handler
        asyncio.create_task(self.handle_messages())

        # Start heartbeat
        asyncio.create_task(self.heartbeat())

    async def handle_messages(self):
        while self.connected:
            try:
                message = await self.ws.recv()
                await self.process_message(json.loads(message))
            except websockets.exceptions.ConnectionClosed:
                await self.handle_disconnect()
                break

    async def heartbeat(self):
        while self.connected:
            try:
                await self.ws.send(json.dumps({
                    "type": "heartbeat",
                    "timestamp": datetime.utcnow().isoformat()
                }))
                await asyncio.sleep(30)
            except websockets.exceptions.ConnectionClosed:
                break

    async def send_game_state(self, state):
        if self.connected:
            await self.ws.send(json.dumps({
                "type": "game_state",
                "data": state,
                "timestamp": datetime.utcnow().isoformat(),
                "game_id": self.game_id
            }))
```

## 5. Error Handling

### Connection Errors

- Connection timeouts
- Network interruptions
- Reconnection handling
- Heartbeat failures

### Message Errors

- Invalid message format
- Missing required fields
- Invalid state transitions
- Concurrent updates

### State Conflicts

- Version conflicts
- Race conditions
- Data inconsistencies
- Resolution strategies

## 6. Testing Plan

### Unit Tests

- Message handling
- State management
- Error handling
- Connection management

### Integration Tests

- Client-server communication
- State synchronization
- Reconnection handling
- Error recovery

### Performance Tests

- Concurrent connections
- Message throughput
- Latency measurements
- Memory usage

## 7. Deployment

### Requirements

- Python 3.8+
- SQLite 3
- websockets
- asyncio

### Configuration

```python
# config.py
class Config:
    DATABASE_URI = 'sqlite:///game_state.db'
    WS_HOST = '0.0.0.0'
    WS_PORT = 8765
    PING_INTERVAL = 30
    PING_TIMEOUT = 10
```

### Startup Script

```bash
#!/bin/bash
# start_server.sh
python server.py
```

## 8. Monitoring

### Logging

- Connection events
- Message traffic
- Error rates
- Performance metrics

### Health Checks

- Connection status
- Message queue
- State consistency
- Resource usage

## 9. Security

### Connection Security

- WSS (WebSocket Secure)
- Authentication
- Rate limiting
- Message validation

### Data Security

- Message encryption
- State validation
- Access control
- Data sanitization

## 10. Next Steps

1. Set up development environment
2. Create database schema
3. Implement WebSocket server
4. Add client connection handling
5. Implement state synchronization
6. Add error handling
7. Add testing
8. Deploy and monitor
