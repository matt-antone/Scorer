# Project Structure

## Package Layout

```
pi_client/
├── widgets/           # UI widgets and components
├── screens/           # Screen implementations
├── assets/           # Static assets and resources
├── state/            # State management
├── tests/            # Test suite
│   ├── graphical/    # UI tests
│   └── unit/        # Unit tests
└── main.py          # Application entry point
```

## Key Changes

- Moved all app modules from `src/` to top level
- Updated import paths to match new structure
- Removed `src` prefix from imports

## Module Organization

1. Widgets

   - UI components
   - Reusable elements
   - Custom widgets

2. Screens

   - Screen implementations
   - Screen-specific logic
   - State management

3. Assets

   - Static resources
   - Images
   - Styles

4. State
   - Game state
   - State management
   - State synchronization

## Import Patterns

- Use direct module imports (e.g., `from screens import ...`)
- No `src` prefix in imports
- Maintain consistent import paths

## Testing

- Tests located in `tests/` directory
- Graphical tests in `tests/graphical/`
- Unit tests in `tests/unit/`
- Test imports match new structure

```
Scorer/
├── assets/            # Shared assets for all components
│   ├── fonts/        # Font files
│   ├── billboards/   # Screensaver images
│   ├── qr_codes/     # Generated QR codes
│   └── icons/        # Application icons
├── pi_client/           # Raspberry Pi application
│   ├── src/          # Source code directory
│   │   ├── screens/      # Kivy screen implementations
│   │   ├── widgets/      # Kivy widget implementations
│   │   ├── main.py       # Main application entry point
│   │   └── scorer.kv     # Main Kivy layout file
│   ├── setup.py      # Package setup
│   └── launch_scorer.sh
├── state_server/     # Flask server for state management
│   ├── db/          # Database models and migrations
│   ├── static/      # Static files for web server
│   └── templates/   # HTML templates
├── phone_clients/    # Web client for mobile devices
│   ├── src/         # TypeScript source files
│   └── public/      # Static web assets
└── memory-bank/     # Project documentation
    ├── projectbrief.md
    ├── productContext.md
    ├── systemPatterns.md
    ├── techContext.md
    ├── activeContext.md
    ├── progress.md
    └── im-a-dummy.md
```

## Directory Descriptions

### assets/

The `assets/` directory contains all shared assets used across components:

- **fonts/**: Contains the Inter font family used throughout the application
- **billboards/**: Contains images used in the screensaver
- **qr_codes/**: Directory where generated QR codes are stored
- **icons/**: Application icons in various sizes
- **background.png**: Main background image for the Kivy application
- **splash.png**: Splash screen image
- **transparent.png**: Transparent image used for button backgrounds

### pi_client/

The `pi_client/` directory contains the Raspberry Pi application:

- **src/**: Source code directory
  - **screens/**: Kivy screen implementations
  - **widgets/**: Kivy widget implementations
  - **main.py**: Main application entry point
  - **scorer.kv**: Main Kivy layout file
- **setup.py**: Package setup and dependencies
- **launch_scorer.sh**: Application launcher script

### state_server/

The `state_server/` directory contains the Flask server:

- **db/**: Database models and migrations
- **static/**: Static files for web server
- **templates/**: HTML templates

### phone_clients/

The `phone_clients/` directory contains the web client:

- **src/**: TypeScript source files
- **public/**: Static web assets

### memory-bank/

The `memory-bank/` directory contains project documentation:

- **projectbrief.md**: Project overview and requirements
- **productContext.md**: Product context and features
- **systemPatterns.md**: System architecture and patterns
- **techContext.md**: Technical stack and setup
- **activeContext.md**: Current work and changes
- **progress.md**: Implementation status
- **im-a-dummy.md**: Project patterns and rules

## Directory Purposes

### src/

- **server/**: Backend services

  - `state_server.py`: WebSocket server and state management
  - `network_manager.py`: WiFi and network handling
  - `update_service.py`: Version and update management
  - `asset_manager.py`: Asset handling and processing

- **client/**: Web client application

  - `components/`: Reusable UI components
  - `screens/`: Main application screens
  - `services/`: Client-side services
  - `utils/`: Helper functions

- **shared/**: Code shared between server and client
  - `models/`: Data models and types
  - `constants/`: Shared constants
  - `utils/`: Shared utility functions

### tests/

- **server/**: Backend service tests
- **client/**: Frontend tests
- **integration/**: End-to-end tests

### scripts/

- `install.sh`: Development environment setup
- `setup_pi.sh`: Raspberry Pi configuration
- `deploy.sh`: Deployment automation

### docs/

- **architecture/**: System design docs
- **api/**: API documentation
- **guides/**: User and developer guides

## Key Files

### Server

- `state_server.py`: Main WebSocket server
- `network_manager.py`: Network handling
- `update_service.py`: Update management
- `asset_manager.py`: Asset handling

### Client

- `App.tsx`: Main application
- `websocket.ts`: WebSocket service
- `gameState.ts`: Game state management
- `settings.ts`: Settings management

### Shared

- `types.ts`: Shared TypeScript types
- `constants.ts`: Shared constants
- `utils.ts`: Shared utilities

### Configuration

- `development.yaml`: Development settings
- `production.yaml`: Production settings

## Next Steps

1. Create new directory structure
2. Move existing files to new locations
3. Update import paths
4. Update documentation
5. Verify functionality
