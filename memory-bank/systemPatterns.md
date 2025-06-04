# System Patterns: Scorer

This document details the system architecture, key technical decisions, design patterns, and component relationships for Scorer.

## 1. System Architecture Overview

Scorer will be a Python application with two main components running concurrently on the Raspberry Pi 5:

1.  **Kivy GUI Application**: The primary user interface, running fullscreen on the 5-inch touchscreen. This component is responsible for displaying game information (scores, CPs, round, timer), handling direct touch interactions for all game management, managing the core game logic, and displaying QR codes for web access.
2.  **Flask Web Application**: A lightweight web server running in a separate thread (or potentially a subprocess managed by the Kivy app). This server provides a web API primarily for players to connect via their mobile devices to _view_ the complete game state. It also offers endpoints for players to _update their own_ scores/CPs, which are then synchronized with the Kivy application.

**Data Flow & State Management:**

- **Central Game State**: The `ScorerApp` (Kivy application main class) maintains the authoritative current game state (Player 1 Score, P1 CPs, Player 2 Score, P2 CPs, Current Round, Timer status, game phase, etc.). This state is held in a Python dictionary (`game_state`).
- **Data Persistence**: The `ScorerApp` is responsible for saving the current `game_state` to `game_state.json` (in the user's Kivy app data directory) on significant changes (like round advance, score update - to be fully verified for all cases) and on application exit. It also loads from this file on startup.
- **Startup Flow with `ResumeOrNewScreen`**:
  - On startup, `ScorerApp.load_game_state()` attempts to load `game_state.json`.
  - It determines if the loaded state represents a _meaningful_ in-progress game (i.e., not the initial 'setup' phase).
  - If a meaningful save exists, the `ResumeOrNewScreen` is displayed, offering to "Resume Game" or "Start New Game".
  - If no meaningful save exists, the application proceeds directly to the standard new game flow (e.g., `NameEntryScreen`).
- **Web API Interaction**: (Future Implementation)
  - The Flask web app will serve a simple HTML/JavaScript frontend to players' browsers.
  - When a player interacts with the web interface (e.g., to increase their score), the JavaScript frontend will make an API call (e.g., POST request) to a Flask endpoint.
  - The Flask endpoint will then need to communicate this update to the Kivy application. This could be achieved through inter-thread communication mechanisms (e.g., a Queue, or custom events if Kivy/Flask are in the same process and Kivy's event loop can be used).
  - The Kivy application, upon receiving an update from the Flask backend, will validate it, update its central game state, and refresh its UI. The updated state will then also be available for subsequent GET requests from any connected web clients.
- **QR Code**: The Kivy application will generate a QR code pointing to the local IP address and port of the Flask server, displayed on the touchscreen for easy connection.

```mermaid
graph TD
    subgraph Raspberry Pi 5
        subgraph KivyApp [Kivy GUI Application (ScorerApp)]
            direction LR
            ScreenManager[Screen Manager] --> ActiveScreen[Current Screen UI]
            ActiveScreen --> KivyLogic[Game Logic & State (in ScorerApp & Screens)]
            KivyLogic -- Read/Write --> DataStore[game_state.json]
            KivyLogic --> QRCodeGen[QR Code Display (Future)]
            KivyApp --> ResumeOrNewScreen {Resume or New?}
            DataStore -- Loaded by --> ResumeOrNewScreen
        end

        subgraph FlaskWebApp [Flask Web Application (Thread/Subprocess - Future)]
            direction LR
            FlaskAPI[Web API Endpoints] --> WebFrontend[HTML/JS Player Interface]
        end

        KivyLogic -- Update Requests / State Sync (Future) --> FlaskAPI
        FlaskAPI -- Read Game State (Future) --> KivyLogic
    end

    MobileDevice1[Player 1 Mobile Device] -- HTTP Requests (Future) --> WebFrontend
    MobileDevice2[Player 2 Mobile Device] -- HTTP Requests (Future) --> WebFrontend

    ActiveScreen -- Displays (Future) --> QRCodeGen
    QRCodeGen -- URL for (Future) --> FlaskWebApp
```

## 2. Key Design Patterns & Considerations

- **Model-View-Controller (MVC) like structure for Kivy**:
  - **Model**: The `game_state` dictionary in `ScorerApp` and the logic for saving/loading it.
  - **View**: The Kivy widgets and UI layout defined in `scorer.kv` (e.g., `<ScorerRootWidget>:`, `<ResumeOrNewScreen>:`).
  - **Controller**: Python classes for each `Screen` (e.g., `ScorerRootWidget`, `NameEntryScreen`) and the main `ScorerApp` class. These handle user input from the touchscreen, update the model (`game_state`), and call methods to refresh the view (e.g., `update_ui_from_state`).
- **Kivy `ObjectProperty` and KV Binding**: Python class properties (e.g., `p1_name_label = ObjectProperty(None)` in a screen's Python class) must be explicitly mapped in the corresponding KV rule (e.g., `p1_name_label: p1_name_label_id`) to link the Python reference to the widget defined with `id: p1_name_label_id` in KV. This is crucial for accessing and manipulating widgets from Python code.
- **App Structure (`ScorerApp` vs. `Screen` subclasses)**: Core application lifecycle methods (`build`, `on_start`, `on_stop`, `load_game_state`, `_determine_screen_from_gamestate`) and management of global application state (`game_state`) reside in the main `ScorerApp` class. Screen-specific UI updates, event handling, and display logic are primarily managed within their respective `Screen` subclasses (e.g., `ScorerRootWidget.update_ui_from_state()`).
- **Deferred UI Updates with `Clock.schedule_once`**: When UI updates depend on widget properties that might not be immediately available after a screen transition or KV rule application (e.g., due to widget instantiation timing), `Clock.schedule_once(update_method, small_delay)` is used to defer the update slightly, allowing Kivy to fully prepare the widgets.
- **RESTful API for Flask**: (Future Implementation) The Flask app will expose simple RESTful endpoints.
- **Threading/Async for Web Server**: (Future Implementation) The Flask server will need to run without blocking Kivy's main loop.
- **Event-Driven Programming**: Kivy is event-driven. Touch interactions trigger events that are handled by methods in the Screen classes.
- **Clear Separation of Concerns**: Maintained between `ScorerApp` (global state, lifecycle) and individual `Screen` classes (screen-specific views and controllers).
- **Error Handling & Resilience**: Basic error handling is in place (e.g., for file loading). Needs to be reviewed for robustness, especially concerning `game_state.json`.

## 3. User Interface (UI) / User Experience (UX) Patterns

- **Touchscreen (Kivy)**:
  - Large, clear buttons (`ScoreboardButton` style) and text for easy readability and interaction.
  - Intuitive layout for scores, CPs, round, timer for both players on `ScorerRootWidget`.
  - Clear flow through setup screens (`NameEntryScreen`, `DeploymentSetupScreen`, `FirstTurnSetupScreen`).
  - `ResumeOrNewScreen` provides clear options on startup if saved data exists.
- **Web Interface (Flask/HTML/JS)**: (Future Implementation)
  - Mobile-first responsive design.

## 4. Global Visual Theme

- **Core Aesthetic**: The application adopts a consistent "Red vs. Blue" two-column visual theme across all screens, with the exception of the `SplashScreen`.
- **Background**: Achieved using `assets/background.png` on `ScorerRootWidget` and `BoxLayout`s with appropriate background colors for other screens like `ResumeOrNewScreen` and setup screens.
- **Content Organization**: Player 1 information is generally on the left (red side), Player 2 on the right (blue side).
- **Font**: "InterBlack" is registered via `LabelBase.register` and used for key headers and labels, as specified in `scorer.kv` (e.g., via `<InterBlack@Label>`).

This provides a high-level view. Specific implementation details of the Kivy UI layouts, Flask endpoints, and data structures will evolve during development.
