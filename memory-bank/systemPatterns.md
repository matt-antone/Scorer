# System Patterns: Scorer

This document details the system architecture, key technical decisions, design patterns, and component relationships for Scorer.

## 1. System Architecture Overview

Scorer will be a Python application with two main components running concurrently on the Raspberry Pi 5:

1.  **Kivy GUI Application**: The primary user interface, running fullscreen on the 5-inch touchscreen. This component is responsible for displaying game information (scores, CPs, round, timer), handling direct touch interactions for all game management, managing the core game logic, and displaying QR codes for web access.
2.  **Flask Web Application**: A lightweight web server running in a separate thread (or potentially a subprocess managed by the Kivy app). This server provides a web API primarily for players to connect via their mobile devices to _view_ the complete game state. It also offers endpoints for players to _update their own_ scores/CPs, which are then synchronized with the Kivy application.

**Data Flow & State Management:**

- **Central Game State**: The Kivy application will maintain the authoritative current game state (Player 1 Score, P1 CPs, Player 2 Score, P2 CPs, Current Round, Timer status, etc.). This state will likely be held in Python objects or a dedicated data structure within the Kivy app.
- **Data Persistence**: The Kivy application will be responsible for saving the current game state to a JSON file (e.g., `current_game.json`) periodically or on significant changes (like round advance, score update) and on exit. It will also load from this file on startup to resume a game if one was in progress.
- **Web API Interaction**:
  - The Flask web app will serve a simple HTML/JavaScript frontend to players' browsers.
  - When a player interacts with the web interface (e.g., to increase their score), the JavaScript frontend will make an API call (e.g., POST request) to a Flask endpoint.
  - The Flask endpoint will then need to communicate this update to the Kivy application. This could be achieved through inter-thread communication mechanisms (e.g., a Queue, or custom events if Kivy/Flask are in the same process and Kivy's event loop can be used).
  - The Kivy application, upon receiving an update from the Flask backend, will validate it, update its central game state, and refresh its UI. The updated state will then also be available for subsequent GET requests from any connected web clients.
- **QR Code**: The Kivy application will generate a QR code pointing to the local IP address and port of the Flask server, displayed on the touchscreen for easy connection.

```mermaid
graph TD
    subgraph Raspberry Pi 5
        subgraph KivyApp [Kivy GUI Application (Fullscreen)]
            direction LR
            KivyUI[Touchscreen UI] --> KivyLogic[Game Logic & State]
            KivyLogic --> DataStore[JSON File (current_game.json)]
            KivyLogic --> QRCodeGen[QR Code Display]
        end

        subgraph FlaskWebApp [Flask Web Application (Thread/Subprocess)]
            direction LR
            FlaskAPI[Web API Endpoints] --> WebFrontend[HTML/JS Player Interface]
        end

        KivyLogic -- Update Requests / State Sync --> FlaskAPI
        FlaskAPI -- Read Game State --> KivyLogic
    end

    MobileDevice1[Player 1 Mobile Device] -- HTTP Requests --> WebFrontend
    MobileDevice2[Player 2 Mobile Device] -- HTTP Requests --> WebFrontend

    KivyUI -- Displays --> QRCodeGen
    QRCodeGen -- URL for --> FlaskWebApp
```

## 2. Key Design Patterns & Considerations

- **Model-View-Controller (MVC) or similar for Kivy**:
  - **Model**: The core game state data and persistence logic.
  - **View**: The Kivy widgets and UI layout (`.kv` files or Python definitions).
  - **Controller**: Logic that handles user input from the touchscreen, updates the model, and tells the view to refresh.
- **RESTful API for Flask**: The Flask app will expose simple RESTful endpoints for getting game state and submitting updates.
  - Example Endpoints:
    - `GET /api/gamestate`: Returns current scores, CPs, round, timer.
    - `POST /api/player/<player_id>/score`: Updates score for a player.
    - `POST /api/player/<player_id>/cp`: Updates CPs for a player.
- **Threading/Async for Web Server**: The Flask server will need to run without blocking the Kivy GUI's main loop. Python's `threading` module is a likely approach. Care must be taken with thread safety if both Kivy and Flask threads directly access shared mutable state (though the preferred pattern is message passing).
- **Event-Driven Programming**: Kivy is event-driven. Interactions on the touchscreen will trigger events. Updates from the web server might also be handled as events within the Kivy app.
- **Clear Separation of Concerns**:
  - Kivy app handles primary display, direct interaction, and core game logic.
  - Flask app handles remote access and player-specific updates via web.
  - Data persistence logic is encapsulated.
- **Error Handling & Resilience**:
  - Graceful handling of network issues for the web interface.
  - Robust saving/loading of game state to prevent data loss.
- **Configuration**: Potentially a simple configuration file (e.g., `config.ini` or `config.json`) for settings like default game time, if needed, though many settings can be part of the game setup UI.

## 3. User Interface (UI) / User Experience (UX) Patterns

- **Touchscreen (Kivy)**:
  - Large, clear buttons and text for easy readability and interaction on a 5-inch screen.
  - Intuitive layout for scores, CPs, round, timer for both players.
  - Simple navigation (e.g., starting a new game, adjusting settings if any) for complete game control.
- **Web Interface (Flask/HTML/JS)**:
  - Mobile-first responsive design, optimized for viewing all shared game information.
  - Clear display of all game data (both players' scores, CPs, round, timer).
  - If implementing self-updates: Simple +/- buttons or input fields for a player to adjust _their own_ score/CPs.
  - Minimalistic, with a primary focus on clear data presentation.

This provides a high-level view. Specific implementation details of the Kivy UI layouts, Flask endpoints, and data structures will evolve during development.
