# System Patterns

## Architecture Overview

### Component Structure

1. **Pi App**

   - Primary interface
   - Game state source
   - Touch screen control

2. **State Server**

   - State synchronization
   - WebSocket server
   - Database management

3. **Phone Clients**
   - Mobile interface
   - Real-time updates
   - Score submission

### Communication Flow

1. **State Updates**

   - Pi App → State Server
   - State Server → Phone Clients
   - Phone Clients → State Server

2. **Data Flow**
   - Game state persistence
   - Real-time synchronization
   - Error recovery

## System Patterns

### State Management

1. **Centralized State**

   - Single source of truth
   - Atomic updates
   - State validation

2. **State Synchronization**
   - Real-time updates
   - Conflict resolution
   - Error recovery

### Error Handling

1. **System-wide**

   - Graceful degradation
   - Error recovery
   - State preservation

2. **Component-specific**
   - Local error handling
   - State recovery
   - User feedback

### Security

1. **Authentication**

   - Client verification
   - Session management
   - Access control

2. **Data Protection**
   - State validation
   - Input sanitization
   - Error handling

## Best Practices

### Code Organization

1. **Component Structure**

   - Clear separation
   - Proper interfaces
   - Consistent patterns

2. **Documentation**
   - Component-specific
   - System-wide
   - Cross-references

### Testing

1. **Unit Tests**

   - Component-specific
   - System-wide
   - Integration tests

2. **Validation**
   - State validation
   - Error handling
   - Performance testing

### Performance

1. **Optimization**

   - State management
   - Network usage
   - Resource utilization

2. **Monitoring**
   - Performance metrics
   - Error tracking
   - State validation

## Related Documentation

### Core Memory Bank

- [projectbrief.md](projectbrief.md)
- [productContext.md](productContext.md)
- [techContext.md](techContext.md)
- [activeContext.md](activeContext.md)
- [progress.md](progress.md)
- [im-a-dummy.md](im-a-dummy.md)

### Component Memory Banks

- [Pi App Memory Bank](../pi_app/memory-bank/)
- [State Server Memory Bank](../state_server/memory-bank/)
- [Phone Clients Memory Bank](../phone_clients/memory-bank/)
