# New Project Structure

```
scorer/
├── memory-bank/           # Preserved memory bank
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── systemPatterns.md
│   ├── techContext.md
│   ├── activeContext.md
│   └── progress.md
│
├── src/                   # Source code
│   ├── kivy_app/         # Kivy application
│   │   ├── main.py              # Main application
│   │   ├── scorer.kv            # Main KV file
│   │   │
│   │   ├── screens/            # Kivy screens
│   │   │   ├── splash_screen.py
│   │   │   ├── resume_or_new_screen.py
│   │   │   ├── name_entry_screen.py
│   │   │   ├── deployment_setup_screen.py
│   │   │   ├── first_turn_setup_screen.py
│   │   │   ├── game_over_screen.py
│   │   │   └── screensaver_screen.py
│   │   │
│   │   ├── widgets/           # Custom widgets
│   │   │   ├── score_display.py
│   │   │   ├── timer_display.py
│   │   │   └── network_status.py
│   │   │
│   │   ├── ui_state/         # UI state management
│   │   │   ├── ui_state.py       # UI state tracking
│   │   │   ├── ui_events.py      # UI event handling
│   │   │   └── state_bindings.py # UI state bindings
│   │   │
│   │   ├── navigation/       # Navigation management
│   │   │   ├── screen_manager.py  # Screen transitions
│   │   │   ├── navigation_rules.py # Navigation rules
│   │   │   └── history.py         # Navigation history
│   │   │
│   │   ├── lifecycle/        # Screen lifecycle
│   │   │   ├── base_screen.py     # Base screen class
│   │   │   ├── lifecycle_events.py # Lifecycle events
│   │   │   └── state_persistence.py # State persistence
│   │   │
│   │   ├── error/           # Error handling
│   │   │   ├── error_handler.py   # Error management
│   │   │   ├── error_screen.py    # Error display
│   │   │   └── error_types.py     # Error definitions
│   │   │
│   │   └── utils/            # Kivy utilities
│   │       ├── state_manager.py
│   │       └── screen_manager.py
│   │
│   ├── server/           # Backend services
│   │   ├── state_server.py      # WebSocket & state management
│   │   ├── network_manager.py   # WiFi & network handling
│   │   └── update_service.py    # Version & update management
│   │
│   ├── client/           # Web client application
│   │   ├── components/          # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Timer.tsx
│   │   │   └── ScoreDisplay.tsx
│   │   │
│   │   ├── screens/            # Main application screens
│   │   │   ├── observer/       # Observer client screens
│   │   │   │   ├── SplashScreen.tsx
│   │   │   │   ├── ResumeOrNewScreen.tsx
│   │   │   │   ├── NameEntryScreen.tsx
│   │   │   │   ├── DeploymentSetupScreen.tsx
│   │   │   │   ├── FirstTurnSetupScreen.tsx
│   │   │   │   ├── GameOverScreen.tsx
│   │   │   │   ├── ScreensaverScreen.tsx
│   │   │   │   └── NoConnectionScreen.tsx
│   │   │   │
│   │   │   └── player/        # Player client screens
│   │   │       ├── SplashScreen.tsx
│   │   │       ├── ResumeOrNewScreen.tsx
│   │   │       ├── NameEntryScreen.tsx
│   │   │       ├── DeploymentSetupScreen.tsx
│   │   │       ├── FirstTurnSetupScreen.tsx
│   │   │       ├── GameOverScreen.tsx
│   │   │       ├── ScreensaverScreen.tsx
│   │   │       ├── MainInterfaceScreen.tsx
│   │   │       └── NoConnectionScreen.tsx
│   │   │
│   │   ├── services/           # Client-side services
│   │   │   ├── websocket.ts
│   │   │   ├── gameState.ts
│   │   │   └── settings.ts
│   │   │
│   │   └── utils/             # Helper functions
│   │       ├── validation.ts
│   │       └── formatting.ts
│   │
│   └── shared/           # Shared code
│       ├── models/            # Data models
│       │   ├── GameState.ts
│       │   └── Settings.ts
│       │
│       ├── constants/         # Shared constants
│       │   ├── types.ts
│       │   └── config.ts
│       │
│       └── utils/            # Shared utilities
│           ├── validation.ts
│           └── formatting.ts
│
├── tests/                # Test suite
│   ├── kivy_app/        # Kivy tests
│   │   ├── unit/        # Unit tests
│   │   │   ├── screens/     # Screen tests
│   │   │   │   ├── test_splash_screen.py
│   │   │   │   ├── test_resume_or_new_screen.py
│   │   │   │   ├── test_name_entry_screen.py
│   │   │   │   ├── test_deployment_setup_screen.py
│   │   │   │   ├── test_first_turn_setup_screen.py
│   │   │   │   ├── test_game_over_screen.py
│   │   │   │   └── test_screensaver_screen.py
│   │   │   │
│   │   │   ├── widgets/     # Widget tests
│   │   │   │   ├── test_score_display.py
│   │   │   │   ├── test_timer_display.py
│   │   │   │   └── test_network_status.py
│   │   │   │
│   │   │   └── utils/       # Utility tests
│   │   │       ├── test_state_manager.py
│   │   │       └── test_screen_manager.py
│   │   │
│   │   ├── integration/ # Integration tests
│   │   │   ├── test_screen_transitions.py
│   │   │   ├── test_state_management.py
│   │   │   └── test_error_handling.py
│   │   │
│   │   └── e2e/        # End-to-end tests
│   │       ├── test_game_flow.py
│   │       ├── test_network_flow.py
│   │       └── test_error_recovery.py
│   │
│   ├── server/         # Server tests
│   │   ├── unit/       # Unit tests
│   │   │   ├── test_state_server.py
│   │   │   ├── test_network_manager.py
│   │   │   ├── test_update_service.py
│   │   │   └── test_asset_manager.py
│   │   │
│   │   ├── integration/ # Integration tests
│   │   │   ├── test_websocket.py
│   │   │   ├── test_state_sync.py
│   │   │   └── test_error_handling.py
│   │   │
│   │   └── e2e/        # End-to-end tests
│   │       ├── test_client_server.py
│   │       └── test_multi_device.py
│   │
│   ├── client/         # Client tests
│   │   ├── unit/       # Unit tests
│   │   │   ├── components/    # Component tests
│   │   │   │   ├── Button.test.tsx
│   │   │   │   ├── Input.test.tsx
│   │   │   │   ├── Timer.test.tsx
│   │   │   │   └── ScoreDisplay.test.tsx
│   │   │   │
│   │   │   ├── screens/       # Screen tests
│   │   │   │   ├── observer/  # Observer screen tests
│   │   │   │   │   ├── SplashScreen.test.tsx
│   │   │   │   │   ├── ResumeOrNewScreen.test.tsx
│   │   │   │   │   └── [other observer screens].test.tsx
│   │   │   │   │
│   │   │   │   └── player/    # Player screen tests
│   │   │   │       ├── SplashScreen.test.tsx
│   │   │   │       ├── MainInterfaceScreen.test.tsx
│   │   │   │       └── [other player screens].test.tsx
│   │   │   │
│   │   │   └── services/      # Service tests
│   │   │       ├── websocket.test.ts
│   │   │       ├── gameState.test.ts
│   │   │       └── settings.test.ts
│   │   │
│   │   ├── integration/ # Integration tests
│   │   │   ├── test_navigation.ts
│   │   │   ├── test_state_management.ts
│   │   │   └── test_error_handling.ts
│   │   │
│   │   └── e2e/        # End-to-end tests
│   │       ├── test_game_flow.cy.ts
│   │       ├── test_network.cy.ts
│   │       └── test_error_recovery.cy.ts
│   │
│   ├── shared/         # Shared tests
│   │   ├── test_models.py
│   │   ├── test_constants.py
│   │   └── test_utils.py
│   │
│   ├── fixtures/       # Test fixtures
│   │   ├── game_states/    # Game state fixtures
│   │   ├── network/        # Network fixtures
│   │   └── ui/            # UI fixtures
│   │
│   ├── mocks/          # Mock objects
│   │   ├── server/         # Server mocks
│   │   ├── client/         # Client mocks
│   │   └── network/        # Network mocks
│   │
│   └── config/         # Test configuration
│       ├── pytest.ini       # Python test config
│       ├── jest.config.js   # JavaScript test config
│       └── cypress.config.ts # E2E test config
│
├── scripts/             # Utility scripts
│   ├── install.sh       # Development setup
│   ├── setup_pi.sh      # Raspberry Pi setup
│   ├── deploy.sh        # Deployment script
│   ├── launch_scorer.sh # Kivy app launcher
│   └── kivy_backend_test.py # Kivy test script
│
├── system/             # System integration
│   ├── Scorer.desktop  # Desktop launcher
│   ├── scorer.service  # Systemd service
│   ├── autostart/      # Autostart configuration
│   └── kiosk/          # Kiosk mode configuration
│       ├── xinitrc     # X11 startup script
│       ├── xserverrc   # X server configuration
│       └── config/     # Kiosk-specific configs
│           ├── disable_screensaver.sh
│           ├── disable_power_management.sh
│           └── disable_pointer.sh
│
├── env/                # Environment setup
│   ├── requirements.txt        # Python dependencies
│   ├── package.json           # Node.js dependencies
│   ├── .env.example          # Environment variables
│   └── platform/             # Platform-specific configs
│       ├── pi/
│       │   ├── config.txt    # Raspberry Pi config
│       │   └── cmdline.txt   # Boot parameters
│       └── mac/
│           └── launchd.plist # macOS launch config
│
├── docs/               # Documentation
│   ├── api/           # API documentation
│   │   ├── websocket/     # WebSocket API
│   │   │   ├── endpoints.md
│   │   │   ├── events.md
│   │   │   └── examples.md
│   │   │
│   │   ├── state_server/  # State server API
│   │   │   ├── endpoints.md
│   │   │   ├── state_management.md
│   │   │   └── examples.md
│   │   │
│   │   ├── network/      # Network API
│   │   │   ├── endpoints.md
│   │   │   ├── protocols.md
│   │   │   └── examples.md
│   │   │
│   │   └── assets/       # Asset management API
│   │       ├── endpoints.md
│   │       ├── formats.md
│   │       └── examples.md
│   │
│   ├── components/    # Component documentation
│   │   ├── kivy/         # Kivy components
│   │   │   ├── screens/      # Screen documentation
│   │   │   │   ├── splash_screen.md
│   │   │   │   ├── resume_or_new_screen.md
│   │   │   │   ├── name_entry_screen.md
│   │   │   │   ├── deployment_setup_screen.md
│   │   │   │   ├── first_turn_setup_screen.md
│   │   │   │   ├── game_over_screen.md
│   │   │   │   └── screensaver_screen.md
│   │   │   │
│   │   │   ├── widgets/      # Widget documentation
│   │   │   │   ├── score_display.md
│   │   │   │   ├── timer_display.md
│   │   │   │   └── network_status.md
│   │   │   │
│   │   │   └── utils/        # Utility documentation
│   │   │       ├── state_manager.md
│   │   │       └── screen_manager.md
│   │   │
│   │   ├── client/       # Client components
│   │   │   ├── components/    # UI components
│   │   │   │   ├── Button.md
│   │   │   │   ├── Input.md
│   │   │   │   ├── Timer.md
│   │   │   │   └── ScoreDisplay.md
│   │   │   │
│   │   │   ├── screens/       # Screen documentation
│   │   │   │   ├── observer/  # Observer screens
│   │   │   │   │   ├── SplashScreen.md
│   │   │   │   │   ├── ResumeOrNewScreen.md
│   │   │   │   │   └── [other observer screens].md
│   │   │   │   │
│   │   │   │   └── player/    # Player screens
│   │   │   │       ├── SplashScreen.md
│   │   │   │       ├── MainInterfaceScreen.md
│   │   │   │       └── [other player screens].md
│   │   │   │
│   │   │   └── services/      # Service documentation
│   │   │       ├── websocket.md
│   │   │       ├── gameState.md
│   │   │       └── settings.md
│   │   │
│   │   └── server/       # Server components
│   │       ├── state_server.md
│   │       ├── network_manager.md
│   │       ├── update_service.md
│   │       └── asset_manager.md
│   │
│   ├── deployment/    # Deployment guides
│   │   ├── pi/           # Raspberry Pi deployment
│   │   │   ├── setup.md
│   │   │   ├── configuration.md
│   │   │   └── troubleshooting.md
│   │   │
│   │   ├── mac/          # macOS deployment
│   │   │   ├── setup.md
│   │   │   ├── configuration.md
│   │   │   └── troubleshooting.md
│   │   │
│   │   ├── production/   # Production deployment
│   │   │   ├── setup.md
│   │   │   ├── configuration.md
│   │   │   └── monitoring.md
│   │   │
│   │   └── updates/      # Update procedures
│   │       ├── process.md
│   │       ├── rollback.md
│   │       └── verification.md
│   │
│   ├── troubleshooting/ # Troubleshooting guides
│   │   ├── common_issues.md
│   │   ├── error_codes.md
│   │   ├── recovery.md
│   │   ├── network.md
│   │   └── state.md
│   │
│   ├── maintenance/   # Maintenance procedures
│   │   ├── updates.md
│   │   ├── database.md
│   │   ├── logs.md
│   │   ├── backup.md
│   │   └── performance.md
│   │
│   ├── development/  # Development guides
│   │   ├── setup.md
│   │   ├── standards.md
│   │   ├── git_workflow.md
│   │   ├── testing.md
│   │   └── release.md
│   │
│   ├── security/     # Security documentation
│   │   ├── authentication.md
│   │   ├── authorization.md
│   │   ├── data_protection.md
│   │   ├── network.md
│   │   └── updates.md
│   │
│   └── performance/  # Performance documentation
│       ├── optimization.md
│       ├── resources.md
│       ├── caching.md
│       ├── load_testing.md
│       └── monitoring.md
│
├── assets/            # Static assets
│   ├── images/        # Images
│   │   ├── screensaver/
│   │   └── icons/
│   │
│   └── fonts/         # Custom fonts
│       └── Inter/
│
├── config/            # Configuration
│   ├── development.yaml
│   └── production.yaml
│
├── .gitignore
└── README.md
```

## Key Changes

1. **UI State Management**

   - Local UI state tracking
   - UI event handling
   - State bindings
   - UI state persistence

2. **Navigation Flow**

   - Screen transition rules
   - Navigation history
   - State-based routing
   - Back navigation

3. **Screen Lifecycle**

   - Base screen class
   - Lifecycle events
   - State persistence
   - Resource management

4. **Error Handling**
   - Centralized error management
   - Error display screens
   - Error type definitions
   - Recovery strategies

## Implementation Details

1. **UI State Management Pattern**

   ```python
   # ui_state/ui_state.py
   class UIState:
       def __init__(self):
           self._ui_state = {}
           self._listeners = []

       def update_ui(self, key, value):
           self._ui_state[key] = value
           self._notify_listeners(key, value)

       def subscribe(self, listener):
           self._listeners.append(listener)
   ```

2. **Navigation Flow**

   ```python
   # navigation/screen_manager.py
   class NavigationManager:
       def __init__(self):
           self._history = []
           self._rules = NavigationRules()

       def navigate(self, screen_name, state=None):
           if self._rules.can_navigate(screen_name, state):
               self._history.append(screen_name)
               return True
           return False
   ```

3. **Screen Lifecycle**

   ```python
   # lifecycle/base_screen.py
   class BaseScreen(Screen):
       def on_enter(self):
           self._load_state()
           self._setup_ui()

       def on_leave(self):
           self._save_state()
           self._cleanup_resources()
   ```

4. **Error Handling**

   ```python
   # error/error_handler.py
   class ErrorHandler:
       def __init__(self):
           self._error_screen = ErrorScreen()

       def handle_error(self, error):
           if isinstance(error, RecoverableError):
               return self._handle_recoverable(error)
           return self._handle_fatal(error)
   ```

## Benefits

1. **Robust UI State Management**

   - Predictable UI updates
   - Event-driven UI changes
   - UI state persistence
   - Clear UI state flow

2. **Reliable Navigation**

   - Rule-based transitions
   - History tracking
   - State-aware routing
   - Back navigation support

3. **Controlled Lifecycle**

   - Resource management
   - State persistence
   - Clean initialization
   - Proper cleanup

4. **Comprehensive Error Handling**
   - Centralized management
   - User-friendly errors
   - Recovery strategies
   - Error logging

## Next Steps

1. Implement UI state management
2. Set up navigation rules
3. Create base screen class
4. Implement error handling

## Screen Flow

### Kivy App Screens

1. **Splash Screen**

   - Initial loading screen
   - System checks
   - Resource initialization

2. **Resume or New Screen**

   - Game state check
   - Resume option
   - New game option

3. **Name Entry Screen**

   - Player name input
   - Game setup
   - Initial configuration

4. **Deployment Setup Screen**

   - Deployment configuration
   - Network setup
   - Device pairing

5. **First Turn Setup Screen**

   - Initial game setup
   - Player order
   - Starting conditions

6. **Game Over Screen**

   - Game completion
   - Score display
   - Restart options

7. **Screensaver Screen**
   - Idle state
   - Power management
   - Quick resume

### Client Screens

#### Observer Client Flow

1. **Splash Screen**

   - Initial loading
   - Connection check
   - Resource initialization

2. **Resume or New Screen**

   - Game state check
   - Resume option
   - New game option

3. **Name Entry Screen**

   - Observer name input
   - Game setup
   - Initial configuration

4. **Deployment Setup Screen**

   - Network configuration
   - Device pairing
   - Connection setup

5. **First Turn Setup Screen**

   - Game initialization
   - Player order
   - Starting conditions

6. **Game Over Screen**

   - Final score display
   - Game state cleanup
   - Restart options

7. **Screensaver Screen**

   - Idle state
   - Power management
   - Quick resume

8. **No Connection Screen**
   - Connection error display
   - Retry options
   - Error details

#### Player Client Flow

1. **Splash Screen**

   - Initial loading
   - Connection check
   - Resource initialization

2. **Resume or New Screen**

   - Game state check
   - Resume option
   - New game option

3. **Name Entry Screen**

   - Player name input
   - Game setup
   - Initial configuration

4. **Deployment Setup Screen**

   - Network configuration
   - Device pairing
   - Connection setup

5. **First Turn Setup Screen**

   - Game initialization
   - Player order
   - Starting conditions

6. **Main Interface Screen**

   - Game controls
   - Score display
   - Timer display
   - Player actions

7. **Game Over Screen**

   - Final score display
   - Game state cleanup
   - Restart options

8. **Screensaver Screen**

   - Idle state
   - Power management
   - Quick resume

9. **No Connection Screen**
   - Connection error display
   - Retry options
   - Error details

## Screen Responsibilities

### Kivy App Screens

1. **Splash Screen**

   - System initialization
   - Resource loading
   - Error checking

2. **Resume or New Screen**

   - Game state validation
   - Save file management
   - User choice handling

3. **Name Entry Screen**

   - Player validation
   - Game initialization
   - State preparation

4. **Deployment Setup Screen**

   - Network configuration
   - Device discovery
   - Connection management

5. **First Turn Setup Screen**

   - Game rules setup
   - Player order
   - Initial state

6. **Game Over Screen**

   - Final score display
   - Game state cleanup
   - Restart flow

7. **Screensaver Screen**
   - Power management
   - State preservation
   - Quick resume

### Client Screens

#### Observer Client Responsibilities

1. **Splash Screen**

   - System initialization
   - Resource loading
   - Error checking

2. **Resume or New Screen**

   - Game state validation
   - Save file management
   - User choice handling

3. **Name Entry Screen**

   - Observer validation
   - Game initialization
   - State preparation

4. **Deployment Setup Screen**

   - Network configuration
   - Device discovery
   - Connection management

5. **First Turn Setup Screen**

   - Game rules setup
   - Player order
   - Initial state

6. **Game Over Screen**

   - Final score display
   - Game state cleanup
   - Restart flow

7. **Screensaver Screen**

   - Power management
   - State preservation
   - Quick resume

8. **No Connection Screen**
   - Error handling
   - Connection retry
   - User feedback

#### Player Client Responsibilities

1. **Splash Screen**

   - System initialization
   - Resource loading
   - Error checking

2. **Resume or New Screen**

   - Game state validation
   - Save file management
   - User choice handling

3. **Name Entry Screen**

   - Player validation
   - Game initialization
   - State preparation

4. **Deployment Setup Screen**

   - Network configuration
   - Device discovery
   - Connection management

5. **First Turn Setup Screen**

   - Game rules setup
   - Player order
   - Initial state

6. **Main Interface Screen**

   - Game controls
   - Score management
   - Timer control
   - Player actions

7. **Game Over Screen**

   - Final score display
   - Game state cleanup
   - Restart flow

8. **Screensaver Screen**

   - Power management
   - State preservation
   - Quick resume

9. **No Connection Screen**
   - Error handling
   - Connection retry
   - User feedback

## Testing Strategy

### 1. Unit Tests

- **Coverage Requirements**

  ```python
  {
      "kivy_app": {
          "screens": 90,    # 90% coverage required
          "widgets": 85,    # 85% coverage required
          "utils": 80       # 80% coverage required
      },
      "server": {
          "core": 95,       # 95% coverage required
          "utils": 90       # 90% coverage required
      },
      "client": {
          "components": 85, # 85% coverage required
          "screens": 80,    # 80% coverage required
          "services": 90    # 90% coverage required
      }
  }
  ```

- **Critical Areas (100% Coverage)**
  - Game state management
  - Score calculations
  - Timer functionality
  - Network communication
  - Error handling
  - State persistence
  - Security features

### 2. Integration Tests

- **Test Areas**

  - Screen transitions
  - State synchronization
  - Network communication
  - Error recovery
  - Data persistence

- **Coverage Requirements**
  - 80% of critical paths
  - 70% of edge cases
  - 100% of error paths

### 3. E2E Tests

- **Test Scenarios**

  - Complete game flow
  - Network failure recovery
  - Multi-device synchronization
  - Error handling
  - State persistence

- **Coverage Requirements**
  - 70% of user flows
  - 100% of critical paths
  - 80% of error scenarios

### 4. Test Data Management

- **Fixtures**

  - Game states
  - Network conditions
  - UI states
  - Error scenarios

- **Mock Objects**
  - Server responses
  - Network conditions
  - Device interactions
  - System events

### 5. Testing Tools

- **Python (Kivy & Server)**

  - pytest
  - pytest-cov
  - pytest-mock
  - pytest-asyncio

- **JavaScript (Client)**
  - Jest
  - React Testing Library
  - Cypress
  - MSW (Mock Service Worker)

### 6. CI/CD Integration

- **Automated Testing**

  - Run on every PR
  - Run on main branch
  - Run before deployment

- **Coverage Reports**
  - Generate on every run
  - Track coverage trends
  - Enforce minimums
  - Report to team

## Next Steps

1. Set up test infrastructure
2. Create initial test suites
3. Configure coverage tools
4. Set up CI/CD pipeline

## Documentation Standards

### 1. API Documentation

- **Format**: OpenAPI/Swagger
- **Required Sections**:
  - Endpoint description
  - Request/Response format
  - Error codes
  - Examples
  - Rate limits

### 2. Component Documentation

- **Format**: Markdown
- **Required Sections**:
  - Purpose
  - Props/Properties
  - Events
  - Examples
  - Dependencies

### 3. Deployment Guides

- **Format**: Markdown
- **Required Sections**:
  - Prerequisites
  - Step-by-step instructions
  - Configuration
  - Verification
  - Troubleshooting

### 4. Troubleshooting Guides

- **Format**: Markdown
- **Required Sections**:
  - Problem description
  - Symptoms
  - Causes
  - Solutions
  - Prevention

### 5. Maintenance Procedures

- **Format**: Markdown
- **Required Sections**:
  - Purpose
  - Frequency
  - Steps
  - Verification
  - Rollback

### 6. Development Guides

- **Format**: Markdown
- **Required Sections**:
  - Setup
  - Standards
  - Workflow
  - Testing
  - Release

### 7. Security Documentation

- **Format**: Markdown
- **Required Sections**:
  - Overview
  - Implementation
  - Configuration
  - Monitoring
  - Updates

### 8. Performance Documentation

- **Format**: Markdown
- **Required Sections**:
  - Metrics
  - Benchmarks
  - Optimization
  - Monitoring
  - Alerts

## Documentation Maintenance

### 1. Version Control

- All docs in version control
- Branch per feature
- PR reviews required
- Automated checks

### 2. Update Process

- Update with code changes
- Review with PRs
- Version tracking
- Change logging

### 3. Quality Checks

- Link validation
- Format checking
- Example testing
- Code snippet testing

### 4. Review Process

- Technical review
- Editorial review
- User testing
- Final approval

## Next Steps

1. Create documentation templates
2. Set up documentation tools
3. Implement automated checks
4. Create initial documentation
