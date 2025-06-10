# Phone Clients Project Brief

## Overview

The Phone Clients are web-based applications that allow players to interact with the game through their mobile devices. They provide a responsive interface for viewing game state and submitting scores.

## Core Requirements

1. Responsive web interface for mobile devices
2. Real-time game state updates
3. Score submission interface
4. QR code scanning for connection
5. Offline support with state synchronization

## Technical Stack

- TypeScript
- React
- WebSocket client
- QR code scanning
- Service Workers for offline support

## Key Components

1. Client Types

   - Player 1 Client
   - Player 2 Client
   - Observer Client

2. Features

   - Real-time score display
   - Score submission
   - Game state viewing
   - Connection management
   - QR code scanning

3. State Management
   - WebSocket connection
   - Local state caching
   - Offline state management
   - State synchronization

## Dependencies

- state_server: For game state and updates
- pi_app: For initial connection via QR code

## Development Guidelines

1. Must work on all modern mobile browsers
2. Must handle poor network conditions gracefully
3. Must provide clear feedback for all actions
4. Must support both portrait and landscape orientations
5. Must be accessible and follow WCAG guidelines
6. Must handle reconnection scenarios
7. Must provide clear error messages
