# Base Screen

## Overview

The `BaseScreen` class provides core functionality and common patterns for all screens in the application. It implements essential features like state management, error handling, input validation, and client synchronization.

## Purpose

- Provide a consistent foundation for all screens
- Implement common functionality to reduce code duplication
- Standardize error handling and state management
- Enable consistent client synchronization

## Properties

### State Flags

- `is_loading` (BooleanProperty): Indicates if the screen is in a loading state
- `is_syncing` (BooleanProperty): Indicates if the screen is synchronizing with clients
- `has_error` (BooleanProperty): Indicates if the screen has an active error

### Internal State

- `_current_error` (str): Current error message
- `_current_status` (str): Current status message
- `_sync_event` (ClockEvent): Event for periodic synchronization
- `_error_timeout` (ClockEvent): Event for error message timeout

## Methods

### Lifecycle Methods

- `on_pre_enter()`: Called before screen is shown
  - Updates view from state
  - Starts synchronization
- `on_enter()`: Called when screen is shown
  - Hides loading state
- `on_leave()`: Called when leaving screen
  - Stops synchronization
  - Clears errors and timeouts

### State Management

- `update_view_from_state()`: Updates UI from game state
  - Must be implemented by child classes
- `validate_state(required_keys=None)`: Validates current game state
  - Returns True if valid
  - Raises StateError if invalid
- `update_state(updates)`: Updates game state
  - Broadcasts changes to clients
  - Raises StateError if update fails

### Error Handling

- `show_error(message, timeout=5)`: Displays error message
  - Sets error state
  - Auto-clears after timeout
- `clear_error()`: Clears error state
- `handle_error(error)`: Handles different error types
  - ValidationError
  - StateError
  - SyncError
- `recover_from_error()`: Attempts error recovery
  - Must be implemented by child classes

### Status Management

- `show_status(message)`: Displays status message
- `clear_status()`: Clears status message

### Loading State

- `show_loading(show=True)`: Controls loading state
  - Child classes implement UI display

### Input Handling

- `validate_input(input_data, rules=None)`: Validates user input
  - Returns True if valid
  - Raises ValidationError if invalid
- `sanitize_input(input_data)`: Sanitizes user input
  - Strips whitespace from strings
  - Returns sanitized data

### Synchronization

- `start_sync()`: Starts client synchronization
  - Child classes implement specific sync logic
- `stop_sync()`: Stops client synchronization
- `broadcast_state()`: Broadcasts state changes
  - Must be implemented by child classes
- `handle_client_update(update)`: Handles client updates
  - Must be implemented by child classes

## Exception Classes

- `ScreenError`: Base exception for screen-related errors
- `ValidationError`: Raised when input validation fails
- `StateError`: Raised when state is invalid
- `SyncError`: Raised when synchronization fails

## Implementation Guidelines

### Required Implementation

Child classes must implement:

1. `update_view_from_state()`: Update UI from game state
2. `recover_from_error()`: Error recovery logic
3. `broadcast_state()`: State broadcasting logic
4. `handle_client_update()`: Client update handling

### UI Implementation

Child classes should:

1. Define UI elements in KV file
2. Implement UI-specific error display
3. Implement UI-specific status display
4. Implement UI-specific loading display

### State Management

Child classes should:

1. Validate state before updates
2. Handle state update failures
3. Implement proper error recovery
4. Maintain state consistency

### Error Handling

Child classes should:

1. Use appropriate error types
2. Implement specific error recovery
3. Display user-friendly error messages
4. Handle all possible error cases

## Example Usage

```python
class MyScreen(BaseScreen):
    def update_view_from_state(self):
        # Update UI from game state
        pass

    def recover_from_error(self):
        # Implement error recovery
        pass

    def broadcast_state(self):
        # Broadcast state changes
        pass

    def handle_client_update(self, update):
        # Handle client updates
        pass
```

```kv
<MyScreen>:
    BoxLayout:
        orientation: 'vertical'

        Label:
            id: error_label
            text: root._current_error if root.has_error else ""
            opacity: 1 if root.has_error else 0

        Label:
            id: status_label
            text: root._current_status or ""

        Spinner:
            id: loading_spinner
            opacity: 1 if root.is_loading else 0
            disabled: not root.is_loading
```

## Best Practices

1. Always validate state before updates
2. Implement proper error recovery
3. Keep UI elements in KV files
4. Use appropriate error types
5. Handle all possible error cases
6. Maintain state consistency
7. Implement proper synchronization
8. Use logging for debugging
