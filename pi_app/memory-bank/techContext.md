# Pi App Technical Context

## Technology Stack

### Core Technologies

1. **Kivy Framework**

   - Version: 2.3.1
   - Used for all UI components
   - Supports both macOS and Raspberry Pi

2. **Python**

   - Version: 3.11.5
   - Core application language
   - Handles game logic and state management

3. **SQLite**
   - Used for game state persistence
   - Automatic database creation
   - Efficient state storage

### Dependencies

1. **FFmpeg**

   - Version: 6
   - Required for video/image processing
   - Used by ffpyplayer

2. **SDL2**

   - Custom build for KMS/DRM support
   - Required for Kivy windowing
   - Platform-specific configurations

3. **ffpyplayer**
   - Version: 4.5.1
   - Used for media handling
   - Built against compatible ffmpeg

## Development Environment

### macOS Development

1. **Setup Requirements**

   - Homebrew for package management
   - Python virtual environment
   - SDL2 with specific configuration

2. **Known Issues**
   - SDL2 environment sensitivity
   - Dependency conflicts possible
   - Requires specific build order

### Raspberry Pi Production

1. **Hardware Requirements**

   - Raspberry Pi OS
   - Touch screen support
   - Network connectivity

2. **Installation**
   - Automated install.sh script
   - Idempotent installation
   - Handles all dependencies

## Application Structure

### Directory Organization

1. **screens/**

   - One screen per file
   - Matching KV file for layout
   - Proper registration in manager

2. **widgets/**

   - Reusable UI components
   - Custom widget implementations
   - Shared styling

3. **state/**
   - Game state management
   - State persistence
   - Error handling

### File Organization

1. **Screen Files**

   - One Python file per screen
   - Matching KV file for layout
   - Proper registration in manager

2. **State Management**

   - Centralized state handling
   - Proper serialization
   - Error handling

3. **Assets**
   - Centralized in root directory
   - Shared across components
   - Proper path references

## Technical Patterns

### Screen Implementation

1. **Class Structure**

   ```python
   class ScreenName(Screen):
       def __init__(self, **kwargs):
           kv_path = os.path.join(os.path.dirname(__file__), 'screen_name.kv')
           Builder.load_file(kv_path)
           super().__init__(**kwargs)
   ```

2. **State Access**
   ```python
   app = App.get_running_app()
   state = app.game_state
   ```

### State Management

1. **Serialization**

   ```python
   def save_game_state(self):
       state_dict = {
           'p1_name': self.player1_name,
           'p2_name': self.player2_name,
           # ... other state fields
       }
       with open('game_state.json', 'w') as f:
           json.dump(state_dict, f)
   ```

2. **Loading**
   ```python
   def load_game_state(self):
       try:
           with open('game_state.json', 'r') as f:
               state = json.load(f)
           return self.validate_state(state)
       except FileNotFoundError:
           return self.initialize_game_state()
   ```

## Performance Considerations

### State Management

1. **Efficient Updates**

   - Only save when necessary
   - Validate before saving
   - Handle errors gracefully

2. **Memory Usage**
   - Clear old states
   - Proper cleanup
   - Resource management

### UI Performance

1. **Rendering**

   - Efficient layouts
   - Proper widget recycling
   - Smooth transitions

2. **Responsiveness**
   - Async operations
   - Background tasks
   - UI feedback

## Security Considerations

### State Protection

1. **Validation**

   - Input validation
   - State validation
   - Error handling

2. **Access Control**
   - Proper permissions
   - Secure storage
   - Data protection

### Network Security

1. **Client Communication**

   - Secure protocols
   - Data encryption
   - Access control

2. **QR Code Security**
   - Secure generation
   - Proper validation
   - Access management

## Related Documentation

### Core Memory Bank

- [projectbrief.md](../../memory-bank/projectbrief.md)
- [productContext.md](../../memory-bank/productContext.md)
- [systemPatterns.md](../../memory-bank/systemPatterns.md)
- [techContext.md](../../memory-bank/techContext.md)
- [activeContext.md](../../memory-bank/activeContext.md)
- [progress.md](../../memory-bank/progress.md)
- [im-a-dummy.md](../../memory-bank/im-a-dummy.md)

### Component Memory Banks

- [State Server Memory Bank](../../state_server/memory-bank/)
- [Phone Clients Memory Bank](../../phone_clients/memory-bank/)

### Implementation Files

- [main.py](../main.py)
- [scorer.kv](../scorer.kv)
- [screens/](../screens/)
- [widgets/](../widgets/)
