# Product Context: Pi App

## Overview

The Pi App is the primary interface for the Warhammer 40k Scorer application, running on a Raspberry Pi 5 with a 5-inch touchscreen. It serves as the central control point for game management and state synchronization.

## Core Requirements

1. **User Interface**

   - Fullscreen Kivy application optimized for touch interaction
   - Clear visual hierarchy with red vs. blue theme
   - Responsive layout for 800x480 display
   - Support for all game screens (Splash, Name Entry, Deployment, Initiative, Scoreboard, Game Over)

2. **Game State Management**

   - Maintains authoritative game state
   - Handles state transitions between screens
   - Persists game state to SQLite database
   - Broadcasts state updates to connected clients

3. **Network Integration**

   - Generates QR codes for client connections
   - Performs network checks on startup
   - Manages WebSocket server for real-time updates
   - Handles client authentication and state synchronization

4. **Screen Implementation Status**
   - Splash Screen: Implemented with background tasks
   - Resume or New Game Screen: Implemented with game state check
   - Name Entry Screen: Implemented with client integration
   - Deployment Setup Screen: Implemented with role selection
   - Initiative Screen: Implemented with tie handling
   - Scoreboard Screen: Implemented as main game interface
   - Game Over Screen: Partially implemented (missing exit functionality)
   - Screensaver Screen: Not implemented
   - Settings Screen: Not implemented

## Dependencies

1. **State Server**

   - Provides WebSocket server for client connections
   - Handles client authentication
   - Manages game state persistence
   - Broadcasts state updates to clients

2. **Phone Clients**
   - Connect via QR codes
   - Submit player names and deployment rolls
   - View game state updates
   - Submit scores and CP updates

## Development Guidelines

1. **UI/UX**

   - Follow Kivy best practices for touch interfaces
   - Maintain consistent visual theme
   - Ensure clear feedback for all actions
   - Support both touch and keyboard input

2. **State Management**

   - Use centralized state management in ScorerApp
   - Implement proper state transitions
   - Handle edge cases (e.g., mid-game interruptions)
   - Maintain data consistency

3. **Performance**

   - Optimize for Raspberry Pi 5 hardware
   - Minimize memory usage
   - Handle background tasks efficiently
   - Ensure smooth screen transitions

4. **Testing**
   - Test on both development (macOS) and target (Raspberry Pi) platforms
   - Verify all screen transitions
   - Test network functionality
   - Validate state persistence

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
