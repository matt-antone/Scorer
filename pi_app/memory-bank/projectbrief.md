# Pi App Project Brief

## Overview

The Pi App is the core Kivy application that runs on the Raspberry Pi 5 with a 5-inch touchscreen. It serves as the main interface for game management and scoring.

## Core Requirements

1. Display and manage game state
2. Handle user input for scoring
3. Generate QR codes for client connections
4. Manage game flow through various screens
5. Persist game state locally

## Technical Stack

- Python 3.11+
- Kivy 2.3.0
- SQLite for local state storage
- QR code generation
- Network connectivity management

## Key Components

1. Screens

   - Splash Screen
   - Resume/New Game Screen
   - Name Entry Screen
   - Deployment Setup Screen
   - Initiative Screen
   - Scoreboard Screen
   - Game Over Screen
   - Screensaver Screen
   - Settings Screen

2. Widgets

   - RoundedButton
   - NumberPadPopup
   - ConcedeConfirmPopup

3. State Management
   - Local game state storage
   - State synchronization with server
   - QR code generation for client connections

## Dependencies

- state_server: For game state synchronization
- phone_clients: For player interaction

## Development Guidelines

1. All UI components must be touch-friendly
2. Screens must handle both portrait and landscape orientations
3. State changes must be persisted immediately
4. Network operations must be handled asynchronously
5. Error states must be handled gracefully with user feedback
