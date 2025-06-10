# State Server Project Brief

## Overview

The State Server is a Flask-based web server that manages game state synchronization between the Pi App and phone clients. It ensures all clients have consistent game state and handles real-time updates.

## Core Requirements

1. Provide RESTful API for game state management
2. Handle WebSocket connections for real-time updates
3. Manage client authentication and session state
4. Persist game state in SQLite database
5. Handle concurrent game sessions

## Technical Stack

- Python 3.11+
- Flask
- Flask-SocketIO
- SQLite
- WebSocket support

## Key Components

1. API Endpoints

   - Game state CRUD operations
   - Client registration
   - Session management
   - QR code generation

2. WebSocket Events

   - State updates
   - Score changes
   - Game phase transitions
   - Client disconnection handling

3. Database
   - Game state tables
   - Session management
   - Client information

## Dependencies

- pi_app: Primary game state source
- phone_clients: Consumer of game state updates

## Development Guidelines

1. All state changes must be atomic
2. Real-time updates must be reliable
3. Error handling must be comprehensive
4. API must be versioned
5. Security must be implemented for all endpoints
6. Logging must be comprehensive for debugging
