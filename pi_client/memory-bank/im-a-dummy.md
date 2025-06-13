# Pi App Memory Dump

## Critical Information

### Screen Implementation

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

### State Management

1. **Game State**

   ```python
   class GameState:
       def __init__(self):
           self.p1_name = ""
           self.p2_name = ""
           self.current_round = 1
           self.current_player_id = 1
           self.status = GameStatus.NOT_STARTED
   ```

2. **State Transitions**
   - NOT_STARTED → IN_PROGRESS: Game initialization
   - IN_PROGRESS → GAME_OVER: Round 5 completion
   - GAME_OVER → NOT_STARTED: New game start

## Key Patterns

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

## Common Issues

### State Management

1. **GameStatus Serialization**

   - Convert to string before saving
   - Convert back to enum when loading
   - Handle missing status gracefully

2. **State Validation**
   - Check required fields
   - Validate field types
   - Handle missing data

### Screen Transitions

1. **Screen Registration**

   - Register in build method
   - Check before transition
   - Handle missing screens

2. **State Requirements**
   - Validate before transition
   - Handle invalid state
   - Provide user feedback

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
