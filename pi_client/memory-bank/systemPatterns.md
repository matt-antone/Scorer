# Pi Client System Patterns

## System Architecture

The Pi client is built using Kivy and follows a modular architecture with clear separation of concerns. The system is designed to work with the new state server implementation, using WebSocket for real-time state synchronization.

## Key Components

### 1. UI Layer

- **Screen Management**

  - BaseScreen class for common functionality
  - Individual screen implementations
  - Screen transitions
  - State observers

- **Widgets**
  - Custom widgets for game elements
  - Reusable components
  - Layout management
  - Event handling

### 2. State Management

- **State Manager**

  - WebSocket client integration
  - State synchronization
  - Error handling
  - State validation

- **State Models**
  - Game state
  - Player state
  - Round state
  - Score state

### 3. Communication

- **WebSocket Client**
  - Connection management
  - Message handling
  - State broadcasting
  - Error recovery

## Design Patterns

### 1. UI Patterns

```python
class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_manager = StateManager()
        self.observers = []

    def on_state_update(self, state):
        # Handle state updates
        # Update UI
        # Notify observers
```

### 2. State Management

```python
class StateManager:
    def __init__(self):
        self.connection = None
        self.state = None
        self.observers = []

    def connect(self):
        # Connect to state server
        # Handle authentication
        # Initialize state

    def update_state(self, updates):
        # Validate updates
        # Apply changes
        # Notify observers
```

### 3. Communication

```python
class WebSocketClient:
    def __init__(self):
        self.connection = None
        self.handlers = {}

    def connect(self):
        # Establish connection
        # Set up handlers
        # Start listening

    def send_message(self, message):
        # Validate message
        # Send to server
        # Handle response
```

## Implementation Details

### 1. Screen Management

- **Base Screen**

  - Common functionality
  - State management
  - Error handling
  - Loading states

- **Individual Screens**
  - Specific functionality
  - State observers
  - UI updates
  - Error handling

### 2. State Management

- **State Manager**

  - WebSocket integration
  - State synchronization
  - Error handling
  - State validation

- **State Models**
  - Data structures
  - Validation rules
  - Serialization
  - Deserialization

### 3. Communication

- **WebSocket Client**
  - Connection management
  - Message handling
  - State broadcasting
  - Error recovery

## Testing Strategy

### 1. Unit Tests

- **State Manager**

  - Connection handling
  - State updates
  - Error handling
  - Validation

- **WebSocket Client**
  - Connection management
  - Message handling
  - Error recovery
  - State synchronization

### 2. Integration Tests

- **Screen Tests**

  - State updates
  - UI changes
  - Error handling
  - Loading states

- **State Tests**
  - Server connection
  - State synchronization
  - Error recovery
  - Performance

### 3. End-to-End Tests

- **Workflow Tests**
  - Complete game flow
  - Error scenarios
  - Recovery procedures
  - Performance testing

## Related Documentation

- [Project Brief](projectbrief.md)
- [Product Context](productContext.md)
- [Technical Context](techContext.md)
- [Active Context](activeContext.md)
- [Progress](progress.md)
