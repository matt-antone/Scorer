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

- **Clarity**: Key game information (scores, CPs, round, timer) should be clearly visible and unambiguous at a glance on both the Pi screen and the web interface.
- **Comprehensive Pi Control**: The Pi's touchscreen interface must allow for easy and complete management of all game aspects by either player, without requiring a phone.
- **Simplicity**: Interactions for updating scores, CPs, advancing rounds, and managing the timer (on both Pi and web where applicable) should be intuitive and require minimal taps/effort.
- **Reliability**: The application should accurately track and display information throughout the game, with updates correctly synchronized between the Pi and web clients.
- **Non-Intrusive Web Viewing**: The web interface should primarily serve as an excellent viewer, allowing players to follow along without distracting from the physical game board. Optional self-updates should be seamless.
- **Accessibility**: QR code for web access makes it easy for anyone with a smartphone to connect.

## 4. Target Users & Scenarios

- **Primary Users**: Warhammer 40k players engaged in 10th Edition games (casual home games, club games, potentially small local tournaments).
- **Key Scenarios**:
  - Two players at a table using the Raspberry Pi as the central scoring device. One player might primarily interact with the touchscreen.
  - Players using their own smartphones via the web interface to update their scores/CPs independently while still having the central Pi display for shared visibility.
  - Games where managing overall game time is important to ensure completion within an allotted period.
