# Product Context: Scorer

This document describes why Scorer exists, the problems it solves, and the desired user experience for Warhammer 40k (10th Edition) players.

## 1. Problem Statement

Playing Warhammer 40k (10th Edition) involves tracking multiple dynamic game elements:

- **Victory Points (VPs)**: From primary objectives (e.g., controlling objective markers) and a changing roster of secondary objectives (e.g., "Bring it Down," "Assassination," tactical secondaries drawn each round). Manual tracking with dice or pen and paper can be cumbersome and prone to errors, especially when managing both player's scores.
- **Command Points (CPs)**: CPs are a crucial resource spent on Stratagems. Players gain CPs primarily during their command phase. Forgetting to gain CPs or miscounting available CPs can significantly impact gameplay.
- **Game Round**: Tracking the current game round (out of a typical 5) is essential for knowing when primary objectives score, when some secondary objectives are revealed/scored, and when the game ends.
- **Game Duration**: While 10th Edition doesn't have strict per-turn time limits like chess, many games are played with an overall time limit (e.g., 2.5-3 hours for a 2000pt game). A visible timer helps players manage their pace.

Traditional methods (dice, pen/paper, generic phone apps) can be fiddly, easily disturbed, or lack the specific focus needed for Warhammer 40k. This can lead to:

- Distraction from the game itself.
- Disputes over scores or CPs.
- An uneven pace of play if time isn't managed.

## 2. Proposed Solution: Scorer

Scorer aims to provide a dedicated, streamlined, and accessible digital tool to manage these core game elements directly at the gaming table.

- **Primary Control & Display (Touchscreen)**: The Raspberry Pi's touchscreen serves as the comprehensive, primary interface for all game management actions (scores, CPs, rounds, timer for both players) and display. It is fully self-sufficient for running a game.
- **Focused Functionality**: It will specifically address Warhammer 40k 10th Edition tracking needs for VPs (primary/secondary), CPs, round, and overall game time.
- **Convenient Viewing & Self-Update (Web Interface)**: The web server allows players to conveniently view all shared game data on their smartphones. Additionally, it provides an option for players to update their _own_ scores and CPs directly from their device.
- **Fullscreen Immersion**: The fullscreen app on the Pi helps maintain focus on the game.

## 3. User Experience Goals

### Core Game Flow

1. **Splash Screen**

   - Quick startup
   - Network status check
   - QR code generation
   - Clear start button

2. **Resume/New Game**

   - Clear options
   - Easy state recovery
   - Smooth transition

3. **Name Entry**

   - Simple input
   - Default names
   - Clear validation
   - QR code display

4. **Deployment Setup**

   - Clear instructions
   - Easy roll-off
   - Attacker/Defender selection
   - First turn determination

5. **Initiative**

   - Simple roll-off
   - Clear winner display
   - Easy turn selection
   - Smooth transition

6. **Scoreboard**

   - Clear score display
   - Easy score entry
   - Round tracking
   - Turn switching
   - Game end detection

7. **Game Over**
   - Winner display
   - Final scores
   - New game option
   - Clean transition

## Feature Requirements

### Core Features

1. **Game State Management**

   - Save/Load functionality
   - State persistence
   - Error recovery
   - State validation

2. **Score Tracking**

   - Primary objectives
   - Secondary objectives
   - Command points
   - Round tracking

3. **Turn Management**

   - Player switching
   - Round progression
   - Game end detection
   - State updates

4. **UI/UX**
   - Consistent styling
   - Clear feedback
   - Easy navigation
   - Responsive design

### Advanced Features

1. **Settings**

   - Theme selection
   - Game preferences
   - Display options
   - Sound settings

2. **Screensaver**

   - Auto-activation
   - Touch to wake
   - Power management
   - State preservation

3. **Statistics**
   - Win/loss tracking
   - Score history
   - Player stats
   - Game analytics

## User Interface

### Design Principles

1. **Consistency**

   - Uniform styling
   - Consistent layout
   - Standard components
   - Clear hierarchy

2. **Clarity**

   - Readable text
   - Clear buttons
   - Obvious actions
   - Intuitive flow

3. **Feedback**
   - Action confirmation
   - Error messages
   - State changes
   - Progress indicators

### Layout Guidelines

1. **Screen Organization**

   - Clear sections
   - Logical grouping
   - Proper spacing
   - Balanced layout

2. **Component Design**

   - Touch-friendly
   - Clear labels
   - Proper sizing
   - Consistent spacing

3. **Navigation**
   - Clear paths
   - Easy transitions
   - Back options
   - State preservation

## Game Rules

### Core Rules

1. **Round Limit**

   - Maximum 5 rounds
   - Both players complete
   - Game end detection
   - Winner calculation

2. **Scoring**

   - Primary objectives
   - Secondary objectives
   - Command points
   - Total calculation

3. **Turn Order**
   - Initiative roll
   - First turn selection
   - Player switching
   - Round progression

### Advanced Rules

1. **Customization**

   - Round limits
   - Scoring rules
   - Timer options
   - Game preferences

2. **Statistics**
   - Win tracking
   - Score history
   - Player stats
   - Game analytics

## User Feedback

### Current Issues

1. **Layout**

   - Inconsistent spacing
   - Button sizing
   - Text alignment
   - Screen transitions

2. **Functionality**

   - Error handling
   - State management
   - Navigation flow
   - Input validation

3. **Experience**
   - User feedback
   - State recovery
   - Error messages
   - Progress indicators

### Improvement Areas

1. **UI/UX**

   - Consistent styling
   - Better feedback
   - Smoother transitions
   - Clearer navigation

2. **Functionality**

   - Robust error handling
   - Improved state management
   - Better validation
   - Enhanced recovery

3. **Features**
   - Missing screens
   - Advanced options
   - Statistics tracking
   - Customization

## 4. Target Users & Scenarios

- **Primary Users**: Warhammer 40k players engaged in 10th Edition games (casual home games, club games, potentially small local tournaments).
- **Key Scenarios**:

  - Two players at a table using the Raspberry Pi as the central scoring device. One player might primarily interact with the touchscreen.
  - Players using their own smartphones via the web interface to update their scores/CPs independently while still having the central Pi display for shared visibility.
  - Games where managing overall game time is important to ensure completion within an allotted period.

- The user experience now includes a clear choice to resume or start a new game if a previous game is detected, improving clarity and control for users.
