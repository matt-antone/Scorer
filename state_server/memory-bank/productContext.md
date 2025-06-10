# Product Context: State Server

## Overview

The State Server is a Flask-based web server that manages game state synchronization between the Pi App and phone clients. It ensures consistent game state across all connected devices and handles real-time updates via WebSocket connections.

## Core Requirements

1. **State Management**

   - Maintains single source of truth for game state
   - Handles state sanitization for client consumption
   - Persists game state in SQLite database
   - Manages state transitions and validation

2. **WebSocket Server**

   - Provides real-time communication channel
   - Handles client connections and disconnections
   - Broadcasts state updates to all connected clients
   - Manages client authentication and session state

3. **API Endpoints**

   - RESTful endpoints for state queries
   - WebSocket events for real-time updates
   - Client authentication endpoints
   - Game state persistence endpoints

4. **Database Management**
   - SQLite database for game state persistence
   - Alembic migrations for schema management
   - Efficient querying and state updates
   - Data validation and sanitization

## Dependencies

1. **Pi App**

   - Primary source of game state updates
   - Initiates WebSocket server
   - Provides client authentication
   - Manages game flow and state transitions

2. **Phone Clients**
   - Connect via WebSocket
   - Request state updates
   - Submit player actions
   - Receive real-time updates

## Development Guidelines

1. **State Management**

   - Implement atomic state changes
   - Ensure reliable real-time updates
   - Handle concurrent connections
   - Maintain data consistency

2. **Security**

   - Implement proper authentication
   - Validate all client inputs
   - Sanitize state for client consumption
   - Handle unauthorized access attempts

3. **Performance**

   - Optimize database queries
   - Handle multiple concurrent connections
   - Minimize latency for real-time updates
   - Efficient state broadcasting

4. **Error Handling**
   - Graceful handling of disconnections
   - Proper error reporting
   - State recovery mechanisms
   - Logging for debugging

## Implementation Status

1. **Core Features**

   - WebSocket server: Implemented
   - State management: Implemented
   - Database persistence: Implemented
   - Client authentication: Implemented

2. **API Endpoints**

   - State queries: Implemented
   - Real-time updates: Implemented
   - Authentication: Implemented
   - Game state persistence: Implemented

3. **Database**

   - Schema: Implemented
   - Migrations: Implemented
   - Queries: Implemented
   - State persistence: Implemented

4. **Security**
   - Authentication: Implemented
   - Input validation: Implemented
   - State sanitization: Implemented
   - Error handling: Implemented

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
- [Phone Clients Memory Bank](../../phone_clients/memory-bank/)

### Implementation Files

- [db/](../db/)
- [static/](../static/)
- [templates/](../templates/)
- [scorer.db](../scorer.db)
