# Active Context

## Current Focus

- WebSocket server implementation for real-time game state updates
- Testing and validation of WebSocket functionality
- Database integration preparation
- Planning for individual player clients accessible via QR code (no login required)
- Web client development for the Scorer application
- Implementing game over screen functionality

## Recent Changes

- Implemented WebSocket server using Flask-SocketIO
- Created web client interface for real-time updates
- Added game state broadcasting functionality
- Integrated WebSocket server with main application
- Installed required dependencies (python-dotenv, asyncpg)
- Added game over data display to the web client
- Implemented splash screen with game over state
- Added styling for game over screen (in progress)

## Active Decisions

- Using Flask-SocketIO for WebSocket implementation
- Port 6969 for WebSocket server to avoid conflicts
- Maintaining JSON-based system until database integration is complete
- Web client interface for testing and monitoring
- Planning individual player clients for mobile access via QR code (no login, secure link)
- Using the same font styles (Inter) and sizing as the main scoreboard
- Maintaining consistent color scheme (red/blue panels)
- Displaying final scores, times, and round information

## Current Status

- Basic game over screen structure is in place
- Font styles need to be aligned with main scoreboard
- Game over state detection is working
- Data population for game over screen is implemented

## Known Issues

- Game over screen styling needs refinement
- Font consistency needs to be improved
- Background colors may need adjustment

## Current Considerations

- Testing WebSocket server stability and performance
- Validating real-time updates across all game state changes
- Preparing for database integration
- Monitoring for any platform-specific issues
- Designing player-specific web clients and QR code access (no login, secure session link)

## Next Steps

1. Thorough testing of WebSocket functionality
2. Implement error handling and reconnection logic
3. Consider authentication for web interface (except player clients)
4. Begin database integration planning
5. Document WebSocket API for future client implementations
6. Design and implement individual player clients with QR code access (no login, secure session link)
7. Complete game over screen implementation:
   - Review and refine game over screen styling
   - Ensure consistent font usage with main scoreboard
   - Test game over state transitions
   - Verify all game data is displayed correctly

## Open Questions

- Should we implement authentication for the web interface (admin/referee only)?
- What additional error handling is needed for production?
- How to handle WebSocket reconnection scenarios?
- What metrics should we track for WebSocket performance?
- What permissions should individual player clients have?
- How to securely generate and display QR codes for player access?
- What is the best way to generate secure, single-use or session-specific links?

## Current Challenges

- Ensuring stable WebSocket connections
- Managing concurrent client connections
- Handling game state synchronization
- Platform-specific testing requirements
- Designing secure and user-friendly player client flows (no login, secure link)

## Environment Notes

- Development on macOS
- Target deployment on Raspberry Pi
- Virtual environment management
- Dependencies:
  - Flask-SocketIO
  - python-socketio
  - python-dotenv
  - asyncpg
  - SQLAlchemy
  - aiosqlite

## Tomorrow's Tasks

1. Review and refine game over screen styling
2. Ensure consistent font usage across all screens
3. Test game over state transitions
4. Verify all game data is displayed correctly
5. Document any additional styling requirements
