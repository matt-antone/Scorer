# Warhammer 40k Scorer

A comprehensive scoring system for Warhammer 40k games, consisting of three main components:

## Project Structure

### 1. Pi App (`pi_app/`)

The core Kivy application running on Raspberry Pi 5 with a 5-inch touchscreen.

- Manages game state and scoring
- Provides the main user interface
- Generates QR codes for client connections
- Handles game flow through various screens

### 2. State Server (`state_server/`)

A Flask-based web server that manages game state synchronization.

- Provides RESTful API for game state
- Handles WebSocket connections for real-time updates
- Manages client authentication and sessions
- Persists game state in SQLite database

### 3. Phone Clients (`phone_clients/`)

Web-based applications for player interaction via mobile devices.

- Responsive web interface
- Real-time game state updates
- Score submission interface
- QR code scanning for connection

## Development Setup

Each component has its own:

- Memory bank for documentation
- Dependencies and requirements
- Development guidelines
- Testing framework

## Getting Started

1. Clone the repository
2. Follow the setup instructions in each component's directory
3. Start with the Pi App for local development
4. Set up the State Server for multiplayer functionality
5. Build the Phone Clients for player interaction

## Documentation

Each component maintains its own documentation in its `memory-bank/` directory:

- `projectbrief.md`: Core requirements and goals
- `productContext.md`: Why and how the component works
- `systemPatterns.md`: Architecture and design patterns
- `techContext.md`: Technical stack and setup
- `activeContext.md`: Current focus and changes
- `progress.md`: Current status and next steps
- `im-a-dummy.md`: Known issues and discrepancies

## Contributing

1. Read the memory bank files for the component you're working on
2. Follow the development guidelines
3. Update the memory bank as you make changes
4. Test thoroughly before submitting changes

## License

[Add your license information here]
