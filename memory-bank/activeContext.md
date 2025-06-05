# Active Context

## Current Focus

- Application is now running stably on both development (macOS) and production (Raspberry Pi) environments
- Fixed recursion issue in game state loading
- Systemd service is properly configured for auto-start
- Investigating multiple platform-specific issues:
  - Splash screen timing discrepancy
  - Screen transition timing
  - Timer synchronization
  - Game state management consistency

## Recent Changes

- Fixed game state loading recursion issue
- Improved systemd service configuration
- Ensured proper display and touchscreen configuration on Raspberry Pi
- Identified several platform-specific timing and synchronization issues

## Next Steps

- Test application on both platforms:
  - macOS development environment
  - Raspberry Pi production environment
- Verify all game features:
  - Player name entry
  - Deployment setup
  - First turn setup
  - Game scoring
  - Timer functionality
  - Game state persistence
- Investigate platform-specific issues:
  - Compare timing implementations between platforms
  - Test screen transitions with adjusted delays
  - Verify timer accuracy and synchronization
  - Consolidate game state management code
  - Document platform-specific timing requirements

## Active Decisions

- Using systemd service for application management
- Kivy configuration optimized for both platforms
- Game state persistence using JSON file storage
- Need to determine best approach for:
  - Consistent splash screen timing across platforms
  - Platform-specific screen transition timing
  - Timer synchronization strategy
  - Game state management standardization

## Database Implementation Plan

### Core Principles

- Keep existing JSON-based system fully functional until new system is proven
- Run database locally on both development and production environments
- Implement new system in parallel without touching existing code
- Use database timestamps as single source of truth for game timing
- Real-time updates via WebSocket for all clients

### Implementation Phases

1. **Database Setup**

   - Create local PostgreSQL database on both environments
   - Implement schema for games, players, and turns
   - Set up database connection management
   - Configure PostgreSQL LISTEN/NOTIFY for real-time updates

2. **WebSocket Server**

   - Implement WebSocket server using FastAPI/Starlette
   - Set up connection management and client tracking
   - Create event broadcasting system
   - Implement authentication and session management
   - Handle reconnection and state recovery

3. **New API Layer**

   - Create new API endpoints for game management
   - Implement time calculation logic using database timestamps
   - Build web interface for remote score management
   - Add WebSocket event handlers for:
     - Score updates
     - Turn changes
     - Timer updates
     - Game state changes

4. **Testing Environment**

   - Create separate testing branch for database implementation
   - Set up test database with sample data
   - Implement automated tests for new functionality
   - Test WebSocket connections and event propagation
   - Load testing for multiple concurrent clients

5. **Migration Strategy**
   - Keep JSON system as fallback
   - Implement data migration tools
   - Create validation system for data consistency
   - Ensure WebSocket reconnection handling

### Technical Requirements

- Local PostgreSQL installation on Raspberry Pi
- Database backup and recovery procedures
- Connection pooling for efficient database access
- Error handling and retry mechanisms
- WebSocket server with:
  - Connection pooling
  - Event queuing
  - State management
  - Error recovery
  - Client authentication

### Success Criteria

- New system fully tested and stable
- Zero impact on existing functionality
- Successful parallel operation of both systems
- Complete test coverage for new features
- Performance metrics meeting requirements
- Real-time updates working reliably across all clients
- Successful handling of network interruptions
- Proper state recovery after disconnections
