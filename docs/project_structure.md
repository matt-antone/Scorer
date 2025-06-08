# Project Structure

```
scorer/
├── src/
│   ├── server/
│   │   ├── state_server.py
│   │   ├── network_manager.py
│   │   ├── update_service.py
│   │   └── asset_manager.py
│   ├── client/
│   │   ├── components/
│   │   ├── screens/
│   │   ├── services/
│   │   └── utils/
│   └── shared/
│       ├── models/
│       ├── constants/
│       └── utils/
├── tests/
│   ├── server/
│   ├── client/
│   └── integration/
├── scripts/
│   ├── install.sh
│   ├── setup_pi.sh
│   └── deploy.sh
├── docs/
│   ├── architecture/
│   ├── api/
│   └── guides/
├── assets/
│   ├── images/
│   └── fonts/
└── config/
    ├── development.yaml
    └── production.yaml
```

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

### assets/

- **images/**: Application images
- **fonts/**: Custom fonts

### config/

- `development.yaml`: Development settings
- `production.yaml`: Production settings

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
