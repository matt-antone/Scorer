# Screen Implementation Discrepancies

This document tracks the discrepancies between documented behavior and actual implementation of screens in the Scorer application. This must be read and considered before making any changes to screen implementations.

## 1. Splash Screen

- **Documented Behavior**:
  - Has a loading indicator that is only visible during background tasks
  - Performs network checks
  - Generates QR codes
  - Start button is disabled until background tasks complete
  - Shows status text for current operation
- **Actual Implementation**:
  - Loading indicator is always visible when start button is disabled
  - No network checks
  - No QR code generation
  - Start button is always enabled (`start_enabled = BooleanProperty(True)`)
  - No status text display

## 2. Game Over Screen

- **Documented Behavior**:
  - Has an "Exit" button
  - Displays detailed game statistics:
    - Command Points
    - Time played
    - Player roles
    - Total rounds
- **Actual Implementation**:
  - Only shows winner and final scores
  - Missing exit button
  - Missing detailed statistics display

## 3. Scoreboard Screen

- **Documented Behavior**:
  - Referred to as `GamePlayScreen` in documentation
  - Has more detailed functionality
- **Actual Implementation**:
  - Implemented as `ScoreboardScreen`
  - Missing some documented functionality
  - Naming inconsistency with documentation

## 4. Resume or New Screen

- **Documented Behavior**:
  - Shows detailed information about saved game
  - Displays saved game state
- **Actual Implementation**:
  - Only shows "A previous game was found"
  - Missing saved game state details

## 5. Initiative Screen

- **Documented Behavior**:
  - Handles ties by having Attacker choose who goes first
- **Actual Implementation**:
  - Doesn't properly handle ties
  - `_prepare_for_game_start` method doesn't check if winner is Attacker

## 6. Deployment Setup Screen

- **Documented Behavior**:
  - Has detailed UI for deployment choices
  - Shows Attacker/Defender roles
- **Actual Implementation**:
  - Missing some documented UI elements
  - Doesn't properly display roles after choice

## 7. Name Entry Screen

- **Documented Behavior**:
  - Has validation and error handling
  - Shows error messages
  - Has input constraints
- **Actual Implementation**:
  - No validation
  - No error messages
  - No input constraints

## 8. Screensaver Screen

- **Documented Behavior**:
  - Appears after inactivity
  - Shows game state
  - Allows easy return to game
- **Actual Implementation**:
  - Not implemented at all

## 9. Settings Screen

- **Documented Behavior**:
  - Allows configuration of game settings
  - Persists settings between sessions
- **Actual Implementation**:
  - Not implemented at all

## Critical Issues (Priority Order)

1. Screensaver Screen (Missing)
2. Settings Screen (Missing)
3. Splash Screen (Missing critical functionality)
4. Game Over Screen (Missing exit functionality)
5. Scoreboard Screen (Naming inconsistency)
6. Resume or New Screen (Missing game state display)
7. Initiative Screen (Missing tie handling)
8. Deployment Setup Screen (Missing role display)
9. Name Entry Screen (Missing validation)

## Required Reading

This document must be read in conjunction with:

1. projectbrief.md
2. productContext.md
3. systemPatterns.md
4. techContext.md
5. activeContext.md
6. progress.md

Before making any changes to screen implementations, all these documents must be reviewed to ensure consistency and proper functionality.

# Patterns and Rules

## Screen Implementation

### Base Screen Pattern

1. All screens MUST inherit from BaseScreen
2. UI elements MUST be defined in screen-specific KV files
3. Required methods MUST be implemented:
   - `update_view_from_state()`
   - `recover_from_error()`
   - `broadcast_state()`
   - `handle_client_update()`

### State Management

1. State MUST be validated before updates
2. State updates MUST be broadcast to clients
3. State errors MUST be handled gracefully
4. State recovery MUST be implemented
5. State consistency MUST be maintained

### Error Handling

1. Errors MUST use appropriate error types
2. Errors MUST be displayed clearly
3. Error recovery MUST be implemented
4. Errors MUST be logged
5. Error states MUST be cleared

### Synchronization

1. Sync MUST be started in `on_pre_enter()`
2. Sync MUST be stopped in `on_leave()`
3. Client updates MUST be handled
4. State MUST be broadcast
5. Sync errors MUST be handled

## Implementation Rules

### Screen Development

1. MUST inherit from BaseScreen
2. MUST define UI in KV file
3. MUST implement required methods
4. MUST handle state
5. MUST manage errors
6. MUST sync clients

### State Management

1. MUST validate state
2. MUST update state
3. MUST broadcast changes
4. MUST handle updates
5. MUST recover errors

### Error Handling

1. MUST use error types
2. MUST display errors
3. MUST handle recovery
4. MUST clear errors
5. MUST log issues

### Synchronization

1. MUST start sync
2. MUST handle updates
3. MUST broadcast state
4. MUST stop sync
5. MUST handle errors

## Best Practices

### Screen Implementation

1. Use BaseScreen
2. Define UI in KV
3. Implement methods
4. Handle state
5. Manage errors
6. Sync clients

### State Management

1. Validate state
2. Update state
3. Broadcast changes
4. Handle updates
5. Recover errors

### Error Handling

1. Use error types
2. Display errors
3. Handle recovery
4. Clear errors
5. Log issues

### Synchronization

1. Start sync
2. Handle updates
3. Broadcast state
4. Stop sync
5. Handle errors

## Common Patterns

### Screen Setup

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

### KV Layout

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

## Error Handling

### Error Types

```python
class ScreenError(Exception):
    """Base exception for screen-related errors."""
    pass

class ValidationError(ScreenError):
    """Raised when input validation fails."""
    pass

class StateError(ScreenError):
    """Raised when state is invalid."""
    pass

class SyncError(ScreenError):
    """Raised when synchronization fails."""
    pass
```

### Error Display

```python
def show_error(self, message, timeout=5):
    """Display an error message."""
    self._current_error = message
    self.has_error = True

    if self._error_timeout:
        self._error_timeout.cancel()
    self._error_timeout = Clock.schedule_once(
        lambda dt: self.clear_error(), timeout
    )
```

## State Management

### State Validation

```python
def validate_state(self, required_keys=None):
    """Validate current game state."""
    app = App.get_running_app()
    if not app or not hasattr(app, 'game_state'):
        raise StateError("Game state not available")

    if required_keys:
        state = app.game_state
        missing_keys = [key for key in required_keys if key not in state]
        if missing_keys:
            raise StateError(f"Missing required state keys: {missing_keys}")

    return True
```

### State Update

```python
def update_state(self, updates):
    """Update game state."""
    app = App.get_running_app()
    if not app or not hasattr(app, 'game_state'):
        raise StateError("Game state not available")

    try:
        app.game_state.update(updates)
        self.broadcast_state()
    except Exception as e:
        raise StateError(f"Failed to update state: {str(e)}")
```

## Synchronization

### Start Sync

```python
def start_sync(self):
    """Start client synchronization."""
    self.is_syncing = True
    # Child classes should implement specific sync logic
```

### Stop Sync

```python
def stop_sync(self):
    """Stop client synchronization."""
    self.is_syncing = False
    if self._sync_event:
        self._sync_event.cancel()
        self._sync_event = None
```

### Handle Updates

```python
def handle_client_update(self, update):
    """Handle client updates."""
    # Child classes should implement specific update handling
```
