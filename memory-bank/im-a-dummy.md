# Screen Implementation Discrepancies

This document tracks the discrepancies between documented behavior and actual implementation of screens in the Scorer application. This must be read and considered before making any changes to screen implementations.

## 1. Splash Screen

- **Documented Behavior**:
  - Has a loading indicator that is only visible during background tasks
  - Performs network checks
  - Generates QR codes
  - Start button is disabled until background tasks complete
  - Shows status text for current operation
- **Actual Implementation**:
  - Loading indicator is always visible when start button is disabled
  - No network checks
  - No QR code generation
  - Start button is always enabled (`start_enabled = BooleanProperty(True)`)
  - No status text display

## 2. Game Over Screen

- **Documented Behavior**:
  - Has an "Exit" button
  - Displays detailed game statistics:
    - Command Points
    - Time played
    - Player roles
    - Total rounds
- **Actual Implementation**:
  - Only shows winner and final scores
  - Missing exit button
  - Missing detailed statistics display

## 3. Scoreboard Screen

- **Documented Behavior**:
  - Referred to as `GamePlayScreen` in documentation
  - Has more detailed functionality
- **Actual Implementation**:
  - Implemented as `ScoreboardScreen`
  - Missing some documented functionality
  - Naming inconsistency with documentation

## 4. Resume or New Screen

- **Documented Behavior**:
  - Shows detailed information about saved game
  - Displays saved game state
- **Actual Implementation**:
  - Only shows "A previous game was found"
  - Missing saved game state details

## 5. Initiative Screen

- **Documented Behavior**:
  - Handles ties by having Attacker choose who goes first
- **Actual Implementation**:
  - Doesn't properly handle ties
  - `_prepare_for_game_start` method doesn't check if winner is Attacker

## 6. Deployment Setup Screen

- **Documented Behavior**:
  - Has detailed UI for deployment choices
  - Shows Attacker/Defender roles
- **Actual Implementation**:
  - Missing some documented UI elements
  - Doesn't properly display roles after choice

## 7. Name Entry Screen

- **Documented Behavior**:
  - Has validation and error handling
  - Shows error messages
  - Has input constraints
- **Actual Implementation**:
  - No validation
  - No error messages
  - No input constraints

## 8. Screensaver Screen

- **Documented Behavior**:
  - Appears after inactivity
  - Shows game state
  - Allows easy return to game
- **Actual Implementation**:
  - Not implemented at all

## 9. Settings Screen

- **Documented Behavior**:
  - Allows configuration of game settings
  - Persists settings between sessions
- **Actual Implementation**:
  - Not implemented at all

## Critical Issues (Priority Order)

1. Screensaver Screen (Missing)
2. Settings Screen (Missing)
3. Splash Screen (Missing critical functionality)
4. Game Over Screen (Missing exit functionality)
5. Scoreboard Screen (Naming inconsistency)
6. Resume or New Screen (Missing game state display)
7. Initiative Screen (Missing tie handling)
8. Deployment Setup Screen (Missing role display)
9. Name Entry Screen (Missing validation)

## Required Reading

This document must be read in conjunction with:

1. projectbrief.md
2. productContext.md
3. systemPatterns.md
4. techContext.md
5. activeContext.md
6. progress.md

Before making any changes to screen implementations, all these documents must be reviewed to ensure consistency and proper functionality.
