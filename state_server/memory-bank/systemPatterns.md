# State Server System Patterns

## Architecture Overview

### Component Structure

1. **Database Layer**

   - SQLite database
   - Schema matching documentation
   - Transaction management
   - Data persistence

2. **WebSocket Layer**

   - Server implementation
   - Message handling
   - Connection management
   - State broadcasting

3. **State Management**

   - State structure
   - State validation
   - State synchronization
   - Error recovery

4. **Security Layer**

   - Authentication
   - Rate limiting
   - Access control
   - Session management

### Communication Flow

1. **Client Communication**

   - WebSocket connections
   - Message processing
   - State updates
   - Error handling

2. **State Flow**
   - State creation
   - State updates
   - State validation
   - State broadcasting

## Implementation Patterns

### Database Pattern

1. **Schema Design**

   ```python
   class DatabaseSchema:
       def __init__(self):
           self.tables = {
               'game_state': {
                   'game_id': 'TEXT PRIMARY KEY',
                   'status': 'TEXT',
                   'current_player': 'TEXT',
                   'scores': 'JSON',
                   'timer': 'JSON',
                   'settings': 'JSON'
               },
               'scores': {
                   'game_id': 'TEXT',
                   'player_id': 'TEXT',
                   'score': 'INTEGER',
                   'timestamp': 'DATETIME'
               },
               'timers': {
                   'game_id': 'TEXT',
                   'player_id': 'TEXT',
                   'time_remaining': 'INTEGER',
                   'timestamp': 'DATETIME'
               },
               'settings': {
                   'game_id': 'TEXT',
                   'setting_key': 'TEXT',
                   'setting_value': 'TEXT',
                   'timestamp': 'DATETIME'
               }
           }
   ```

2. **Manager Implementation**

   ```python
   class DatabaseManager:
       def __init__(self, db_path):
           self.db_path = db_path
           self.connection = None
           self.schema = DatabaseSchema()

       def initialize(self):
           # Create tables
           # Set up indexes
           # Configure constraints

       def execute_query(self, query, params=None):
           # Execute query
           # Handle errors
           # Return results

       def begin_transaction(self):
           # Start transaction
           # Handle errors
           # Return transaction

       def commit_transaction(self, transaction):
           # Commit transaction
           # Handle errors
           # Verify success
   ```

### WebSocket Pattern

1. **Server Implementation**

   ```python
   class WebSocketServer:
       def __init__(self, host, port):
           self.host = host
           self.port = port
           self.clients = {}
           self.message_handlers = {}

       def start(self):
           # Start server
           # Handle connections
           # Process messages

       def handle_connection(self, client):
           # Validate client
           # Track connection
           # Handle errors

       def handle_message(self, client, message):
           # Validate message
           # Process message
           # Send response
   ```

2. **Message Handling**

   ```python
   class MessageHandler:
       def __init__(self):
           self.handlers = {
               'CONNECT': self.handle_connect,
               'DISCONNECT': self.handle_disconnect,
               'HEARTBEAT': self.handle_heartbeat,
               'STATE_UPDATE': self.handle_state_update,
               'ERROR': self.handle_error
           }

       def handle_message(self, message):
           # Validate message
           # Get handler
           # Process message
           # Return response
   ```

### State Management Pattern

1. **State Structure**

   ```python
   class GameState:
       def __init__(self):
           self.game_id = None
           self.status = None
           self.current_player = None
           self.scores = {}
           self.timer = {}
           self.settings = {}

       def update(self, updates):
           # Validate updates
           # Apply changes
           # Broadcast state

       def validate(self):
           # Check structure
           # Verify values
           # Return status
   ```

2. **State Operations**

   ```python
   class StateManager:
       def __init__(self, db_manager):
           self.db_manager = db_manager
           self.states = {}

       def create_state(self, game_id):
           # Create state
           # Initialize values
           # Store state

       def update_state(self, game_id, updates):
           # Validate updates
           # Apply changes
           # Broadcast state

       def get_state(self, game_id):
           # Get state
           # Validate state
           # Return state
   ```

### Security Pattern

1. **Authentication**

   ```python
   class AuthenticationManager:
       def __init__(self):
           self.tokens = {}
           self.sessions = {}

       def authenticate(self, client_id, credentials):
           # Validate credentials
           # Create token
           # Track session

       def validate_token(self, token):
           # Check token
           # Verify expiration
           # Return status
   ```

2. **Rate Limiting**

   ```python
   class RateLimiter:
       def __init__(self, limits):
           self.limits = limits
           self.requests = {}

       def check_limit(self, client_id):
           # Check limits
           # Update counts
           # Return status

       def reset_limits(self):
           # Reset counts
           # Update timestamps
           # Clear expired
   ```

## Error Handling Pattern

1. **Error Types**

   ```python
   class StateServerError(Exception):
       pass

   class DatabaseError(StateServerError):
       pass

   class WebSocketError(StateServerError):
       pass

   class StateError(StateServerError):
       pass

   class SecurityError(StateServerError):
       pass
   ```

2. **Error Handling**

   ```python
   class ErrorHandler:
       def __init__(self):
           self.handlers = {
               DatabaseError: self.handle_database_error,
               WebSocketError: self.handle_websocket_error,
               StateError: self.handle_state_error,
               SecurityError: self.handle_security_error
           }

       def handle_error(self, error):
           # Get handler
           # Process error
           # Return response
   ```

## Testing Pattern

1. **Unit Tests**

   ```python
   class TestDatabase(unittest.TestCase):
       def setUp(self):
           self.db = DatabaseManager(':memory:')
           self.db.initialize()

       def test_create_state(self):
           # Test state creation
           # Verify state
           # Check persistence

       def test_update_state(self):
           # Test state update
           # Verify changes
           # Check broadcasting
   ```

2. **Integration Tests**

   ```python
   class TestWebSocket(unittest.TestCase):
       def setUp(self):
           self.server = WebSocketServer('localhost', 8000)
           self.server.start()

       def test_client_connection(self):
           # Test connection
           # Verify state
           # Check communication

       def test_state_sync(self):
           # Test sync
           # Verify state
           # Check broadcasting
   ```

## Migration Pattern

1. **Parallel Operation**

   ```python
   class MigrationManager:
       def __init__(self, old_server, new_server):
           self.old_server = old_server
           self.new_server = new_server
           self.state_comparator = StateComparator()

       def start_parallel_operation(self):
           # Start both servers
           # Monitor states
           # Compare results

       def validate_states(self):
           # Compare states
           # Verify operations
           # Check consistency
   ```

2. **Switchover**

   ```python
   class SwitchoverManager:
       def __init__(self, old_server, new_server):
           self.old_server = old_server
           self.new_server = new_server
           self.monitor = StateMonitor()

       def prepare_switchover(self):
           # Verify states
           # Check readiness
           # Prepare clients

       def execute_switchover(self):
           # Enable new server
           # Monitor states
           # Handle issues
   ```

## Related Documentation

- [Active Context](activeContext.md)
- [Progress Report](progress.md)
- [Technical Context](../memory-bank/techContext.md)
- [Product Context](../memory-bank/productContext.md)
