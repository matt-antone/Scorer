# Screen: Main Interface Screen

## 1. Purpose

The Main Interface Screen is the primary game interface for player clients, displaying the current game state, scores, and controls. It integrates with the settings system to handle game state changes, screen saver activation, and player interactions.

## 2. Behavior & Flow

### Game State Management

- Monitors game state (Active/Paused)
- Updates display based on current state
- Handles pause/resume during player's turn
- Manages screen saver activation

### Player Controls

- Score display
- CP display
- Turn indicator
- Pause/Resume during turn
- Concede game option

### Settings Integration

- Respects pause/resume state
- Handles screen saver activation
- Updates display based on settings
- Shows player names

### Layout

```
[Settings]                    [Pause]
----------------------------------------
Player 1: John               Player 2: Jane
Score: 45                    Score: 38
CP: 12                       CP: 10
[Your Turn]                  [Opponent's Turn]

[Game Time: 1:23:45]
[Last Action: 2 minutes ago]
```

## 3. Screen Transition

- **Settings Button**: Opens settings screen
- **Pause Button**: Toggles game state (during turn)
- **Screen Saver**: Activates based on settings
- **Game State Change**: Updates display

## 4. Key Implementation Details

- **File Location**: `client/src/screens/MainInterfaceScreen.js`
- **State Management**:
  - Monitors game state
  - Updates display in real-time
  - Handles settings changes
- **Settings Integration**:
  - Reads game state from settings
  - Updates display based on settings
  - Manages screen saver activation
- **Player Interaction**:
  - Displays score changes
  - Shows CP adjustments
  - Indicates turn changes
  - Shows player names
