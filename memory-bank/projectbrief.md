# Project Brief

## Project Overview

### Purpose

The Scorer application is a Warhammer 40k scoreboard designed to run on a Raspberry Pi with a touch screen. It provides a comprehensive scoring system for tracking game progress, managing turns, and determining winners.

### Core Features

1. **Game Management**

   - Round tracking (5 rounds)
   - Turn management
   - Score tracking
   - Winner calculation

2. **User Interface**

   - Touch screen support
   - Clear score display
   - Easy navigation
   - Responsive design

3. **State Management**
   - Game state persistence
   - Save/Load functionality
   - Error recovery
   - State validation

## Current Status

### Implemented Features

1. **Core Components**

   - Pi App (Primary Interface)
   - State Server (Game State Management)
   - Phone Clients (Mobile Access)

2. **Game Logic**

   - Round limit enforcement
   - Turn switching
   - Score calculation
   - Winner determination

3. **State Management**
   - State persistence
   - Save/Load functionality
   - Error handling
   - State validation

### In Progress

1. **Component Improvements**

   - Layout consistency
   - Error handling
   - State management
   - Navigation flow

2. **Missing Features**
   - Settings screen
   - Screensaver screen
   - Game statistics
   - Advanced options

## Project Goals

### Short Term

1. **Component Improvements**

   - Fix layout issues
   - Improve error handling
   - Enhance state management
   - Refine navigation

2. **Missing Features**
   - Implement settings screen
   - Add screensaver functionality
   - Add game statistics
   - Implement advanced options

### Long Term

1. **Enhanced Features**

   - Advanced statistics
   - Custom game rules
   - Multiple game modes
   - Tournament support

2. **User Experience**
   - Improved UI/UX
   - Better feedback
   - Smoother transitions
   - Enhanced customization

## Technical Requirements

### Hardware

1. **Raspberry Pi**

   - Raspberry Pi OS
   - Touch screen support
   - Network connectivity
   - Adequate storage

2. **Display**
   - Touch screen
   - Adequate resolution
   - Good visibility
   - Proper orientation

### Software

1. **Core Dependencies**

   - Python 3.11.5
   - Kivy 2.3.1
   - SQLite
   - FFmpeg 6

2. **Development**
   - macOS support
   - Virtual environment
   - Version control
   - Testing framework

## Success Criteria

### Functional

1. **Core Features**

   - All components implemented
   - Game logic working
   - State management reliable
   - Error handling robust

2. **User Experience**
   - Intuitive interface
   - Clear feedback
   - Smooth transitions
   - Reliable operation

### Technical

1. **Performance**

   - Fast startup
   - Smooth operation
   - Efficient state management
   - Reliable persistence

2. **Reliability**
   - Error recovery
   - State preservation
   - Data integrity
   - System stability

## Project Timeline

### Current Phase

1. **Component Improvements**

   - Layout fixes
   - Error handling
   - State management
   - Navigation refinement

2. **Missing Features**
   - Settings screen
   - Screensaver
   - Statistics
   - Advanced options

### Next Phase

1. **Enhanced Features**

   - Advanced statistics
   - Custom rules
   - Game modes
   - Tournament support

2. **Polish**
   - UI/UX improvements
   - Performance optimization
   - Testing
   - Documentation

## Core Architecture

### Screen Management

The application uses a standardized screen management system based on the `BaseScreen` class, which provides:

1. **Core Functionality**

   - State management
   - Error handling
   - Input validation
   - Client synchronization
   - Lifecycle management

2. **Standardized Behavior**

   - Consistent error handling
   - Uniform loading states
   - Predictable transitions
   - Reliable state updates
   - Real-time synchronization

3. **Implementation Requirements**
   - All screens must inherit from BaseScreen
   - UI elements defined in screen-specific KV files
   - Required method implementations
   - State management
   - Error handling
   - Client synchronization

## Project Goals

### Technical Goals

1. Implement robust screen management
2. Ensure consistent user experience
3. Provide reliable state management
4. Enable real-time synchronization
5. Handle errors gracefully

### User Experience Goals

1. Consistent screen behavior
2. Clear error messages
3. Reliable state updates
4. Real-time synchronization
5. Predictable transitions

## Implementation Strategy

### Screen Development

1. Use BaseScreen foundation
2. Define UI in KV files
3. Implement required methods
4. Handle state updates
5. Manage errors
6. Sync with clients

### State Management

1. Validate state
2. Update state
3. Broadcast changes
4. Handle updates
5. Recover errors

### Error Handling

1. Use error types
2. Display errors
3. Handle recovery
4. Clear errors
5. Log issues

### Synchronization

1. Start sync
2. Handle updates
3. Broadcast state
4. Stop sync
5. Handle errors

## Project Requirements

### Screen Requirements

- Inherit from BaseScreen
- Define UI in KV
- Implement methods
- Handle state
- Manage errors
- Sync clients

### State Management

- Validate state
- Update state
- Broadcast changes
- Handle updates
- Recover errors

### Error Handling

- Use error types
- Display errors
- Handle recovery
- Clear errors
- Log issues

### Synchronization

- Start sync
- Handle updates
- Broadcast state
- Stop sync
- Handle errors

## Success Criteria

### Technical Success

1. All screens use BaseScreen
2. Consistent error handling
3. Reliable state management
4. Real-time synchronization
5. Graceful error recovery

### User Experience Success

1. Consistent screen behavior
2. Clear error messages
3. Reliable state updates
4. Real-time synchronization
5. Predictable transitions

## Implementation Plan

### Phase 1: Foundation

1. Implement BaseScreen
2. Define core functionality
3. Establish patterns
4. Create documentation
5. Set guidelines

### Phase 2: Migration

1. Update existing screens
2. Implement required methods
3. Handle state
4. Manage errors
5. Sync clients

### Phase 3: Enhancement

1. Improve error handling
2. Enhance state management
3. Optimize synchronization
4. Add features
5. Polish UI

### Phase 4: Testing

1. Unit tests
2. Integration tests
3. Error handling tests
4. Sync tests
5. UI tests
