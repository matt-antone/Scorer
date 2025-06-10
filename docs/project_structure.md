# Project Structure

```
Scorer/
├── assets/            # Shared assets for all components
│   ├── fonts/        # Font files
│   ├── billboards/   # Screensaver images
│   ├── qr_codes/     # Generated QR codes
│   └── icons/        # Application icons
├── pi_app/           # Raspberry Pi application
│   ├── screens/      # Kivy screen implementations
│   ├── widgets/      # Kivy widget implementations
│   ├── main.py       # Main application entry point
│   └── scorer.kv     # Main Kivy layout file
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
