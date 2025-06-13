# Pi App System Patterns

## Screen Implementation

### Class Structure

1. **Base Pattern**

   ```python
   class ScreenName(Screen):
       def __init__(self, **kwargs):
           kv_path = os.path.join(os.path.dirname(__file__), 'screen_name.kv')
           Builder.load_file(kv_path)
           super().__init__(**kwargs)
           self.setup_ui()
   ```

2. **State Access**
   ```python
   app = App.get_running_app()
   state = app.game_state
   ```

### Screen Transitions

1. **Validation**

   ```python
   def transition_to_screen(self, screen_name):
       if not self.manager.has_screen(screen_name):
           raise ValueError(f"Screen {screen_name} not registered")
       self.manager.current = screen_name
   ```

2. **Error Recovery**
   ```python
   try:
       self.manager.current = 'screen_name'
   except Exception as e:
       logger.error(f"Screen transition failed: {e}")
       # Handle error
   ```

## State Management

### Game State

1. **Structure**

   ```python
   class GameState:
       def __init__(self):
           self.p1_name = ""
           self.p2_name = ""
           self.current_round = 1
           self.current_player_id = 1
           self.status = GameStatus.NOT_STARTED
   ```

2. **Validation**
   ```python
   def validate_state(self, state):
       required_fields = ['p1_name', 'p2_name', 'current_round']
       for field in required_fields:
           if field not in state:
               raise ValueError(f"Missing required field: {field}")
       return state
   ```

### State Persistence

1. **Saving**

   ```python
   def save_game_state(self):
       state_dict = {
           'p1_name': self.player1_name,
           'p2_name': self.player2_name,
           'status': self.status.name,
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

## Error Handling

### State Validation

1. **Type Checking**

   ```python
   if not isinstance(state, (dict, GameState)):
       raise TypeError("Invalid state type")
   ```

2. **Required Fields**
   ```python
   required_fields = ['p1_name', 'p2_name', 'current_round']
   for field in required_fields:
       if field not in state:
           raise ValueError(f"Missing required field: {field}")
   ```

### Screen Validation

1. **Screen Registration**

   ```python
   if not self.manager.has_screen('screen_name'):
       raise ValueError("Screen not registered")
   ```

2. **State Requirements**
   ```python
   if not self.validate_state_requirements():
       raise ValueError("Invalid state for screen")
   ```

## Best Practices

### Code Organization

1. **Screen Files**

   - One screen per file
   - Clear naming convention
   - Proper imports

2. **State Management**

   - Centralized state handling
   - Proper serialization
   - Error handling

3. **UI Implementation**
   - Consistent styling
   - Proper layout
   - Responsive design

### Error Handling

1. **Validation**

   - Input validation
   - State validation
   - Screen validation

2. **Recovery**
   - Graceful error handling
   - User feedback
   - State recovery

### Performance

1. **State Management**

   - Efficient updates
   - Proper serialization
   - Minimal memory usage

2. **UI Updates**
   - Efficient rendering
   - Proper layout
   - Smooth transitions

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
