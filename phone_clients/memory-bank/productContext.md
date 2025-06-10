# Product Context: Phone Clients

## Overview

The Phone Clients are web-based applications that allow players to interact with the game through their mobile devices. They provide a responsive interface for viewing game state, submitting scores, and participating in game setup.

## Core Requirements

1. **User Interface**

   - Responsive web design for mobile devices
   - Clear visual hierarchy matching Pi App theme
   - Support for both portrait and landscape orientations
   - Accessible interface for all users

2. **Client Types**

   - Player 1 Client: For first player interaction
   - Player 2 Client: For second player interaction
   - Observer Client: For spectators to view game state

3. **Game Setup**

   - Name entry for players
   - Deployment roll-off participation
   - Attacker/Defender role selection
   - Initiative roll participation

4. **Game Play**
   - Real-time score display
   - Command Point tracking
   - Round and timer information
   - Score submission interface

## Dependencies

1. **State Server**

   - WebSocket connection for real-time updates
   - RESTful API for state queries
   - Authentication endpoints
   - State persistence

2. **Pi App**
   - QR code for initial connection
   - Game state synchronization
   - Client authentication
   - Game flow management

## Development Guidelines

1. **UI/UX**

   - Mobile-first responsive design
   - Clear visual feedback
   - Intuitive navigation
   - Consistent styling with Pi App

2. **State Management**

   - Real-time state updates
   - Local state caching
   - Offline support
   - State synchronization

3. **Performance**

   - Optimize for mobile devices
   - Efficient WebSocket usage
   - Minimize network requests
   - Handle poor network conditions

4. **Error Handling**
   - Graceful disconnection handling
   - Clear error messages
   - Automatic reconnection
   - State recovery

## Implementation Status

1. **Core Features**

   - WebSocket connection: Implemented
   - Real-time updates: Implemented
   - State synchronization: Implemented
   - Client authentication: Implemented

2. **Game Setup**

   - Name entry: Implemented
   - Deployment rolls: Implemented
   - Role selection: Implemented
   - Initiative rolls: Implemented

3. **Game Play**

   - Score display: Implemented
   - CP tracking: Implemented
   - Round display: Implemented
   - Score submission: Implemented

4. **UI Components**
   - Responsive layout: Implemented
   - Theme consistency: Implemented
   - Orientation support: Implemented
   - Accessibility: Partially implemented

## Future Enhancements

1. **Offline Support**

   - Local state caching
   - Offline score tracking
   - State synchronization on reconnect
   - Conflict resolution

2. **Enhanced UI**

   - Animations for state changes
   - Improved error messages
   - Better loading states
   - Enhanced accessibility

3. **Additional Features**
   - Game history viewing
   - Statistics tracking
   - Custom themes
   - Push notifications

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

- [Pi App Memory Bank](../../pi_app/memory-bank/)
- [State Server Memory Bank](../../state_server/memory-bank/)

### Implementation Files

- [src/](../src/)
- [public/](../public/)
- [package.json](../package.json)
- [tsconfig.json](../tsconfig.json)
