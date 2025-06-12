# Warhammer 40k Scorer

A comprehensive scoring system for Warhammer 40k games, consisting of three main components:

## Project Structure

### 1. Pi App (`pi_app/`)

The core Kivy application running on Raspberry Pi 5 with a 5-inch touchscreen.

- Manages game state and scoring
- Provides the main user interface
- Generates QR codes for client connections
- Handles game flow through various screens
- Contains its own virtual environment and launcher script

### 2. State Server (`state_server/`)

A Flask-based web server that manages game state synchronization.

- Provides RESTful API for game state
- Handles WebSocket connections for real-time updates
- Manages client authentication and sessions
- Persists game state in SQLite database
- Includes database migrations and schema management

### 3. Phone Clients (`phone_clients/`)

Web-based applications for player interaction via mobile devices.

- Responsive web interface
- Real-time game state updates
- Score submission interface
- QR code scanning for connection

## Installation

> **For full details, see [`docs/installation_guide.md`](docs/installation_guide.md)**

### Prerequisites

- Python 3.8 or higher
- Git
- Homebrew (on macOS)

### Steps

1. **Clone the repository:**
   ```bash
   git clone [repository-url]
   cd Scorer
   ```
2. **Run the installer:**

   ```bash
   ./install.sh
   ```

   - Do NOT use sudo. The script will handle all dependencies as your user.
   - The installer will:
     - Install and link Homebrew dependencies (ffmpeg@6, SDL2, etc.)
     - Create a virtual environment for the Pi App
     - Install all Python dependencies (including ffpyplayer) in the Pi App's virtual environment
     - Build ffpyplayer from source with system libraries
     - Run Alembic migrations using the Pi App's virtual environment

3. **Launch the Pi App:**

   ```bash
   cd pi_app
   ./launch_scorer.sh
   ```

   If you see the app launch without errors, installation was successful.

4. **(Optional) Launch the State Server:**
   ```bash
   cd state_server
   source ../pi_app/.venv/bin/activate
   python main.py
   ```

## Development Setup

Each component has its own:

- Memory bank for documentation
- Dependencies and requirements
- Development guidelines
- Testing framework

## Testing

The project includes two types of tests: non-graphical (logic and state management) and graphical (Kivy UI) tests.

### Non-Graphical Tests

These tests verify core functionality and can be run on any platform (macOS, Raspberry Pi, CI, etc.).

#### Prerequisites

- Python 3.8 or higher
- pytest installed (`pip install pytest`)

#### Running Non-Graphical Tests

1. **Ensure you are in the project root directory:**

   ```bash
   cd /path/to/Scorer
   ```

2. **Activate the virtual environment:**

   ```bash
   source pi_app/.venv/bin/activate
   ```

3. **Run the tests using pytest:**
   ```bash
   python -m pytest tests/non_graphical/ -v
   ```

#### What's Tested

- Game state management
- Score calculations
- Player management
- Initiative tracking
- Game flow logic

#### Troubleshooting

- If you see import errors, ensure all imports use absolute paths (e.g., `from pi_app.screens...`)
- If you add new non-graphical tests, place them in `tests/non_graphical/`

### Graphical Tests (Kivy)

These tests verify the UI components and must be run on the Raspberry Pi with a display.

#### Prerequisites

- Raspberry Pi 5 with 5-inch touchscreen
- All dependencies installed via `install.sh`
- Virtual environment activated

#### Running Graphical Tests

1. **Ensure you are in the project root directory:**

   ```bash
   cd /path/to/Scorer
   ```

2. **Activate the virtual environment:**

   ```bash
   source pi_app/.venv/bin/activate
   ```

3. **Run the tests using pytest:**
   ```bash
   python -m pytest tests/graphical/ -v
   ```

#### What's Tested

- Screen transitions
- UI component behavior
- Touch interactions
- Visual feedback
- Layout rendering

#### Troubleshooting

- Ensure the display is connected and working
- Check that Kivy is properly installed
- Verify all dependencies are installed
- Run tests in a graphical environment (not headless)

## Documentation

- `docs/`: Technical documentation and implementation details
- `memory-bank/`: Project-wide documentation and context
- Component-specific documentation in each component's directory

## Contributing

1. Read the memory bank files for the component you're working on
2. Follow the development guidelines
3. Update the memory bank as you make changes
4. Test thoroughly before submitting changes

## Version Control

### Git Branch Management

#### Switching Branches

1. **List all branches:**

   ```bash
   git branch -a
   ```

   - Local branches are shown without prefix
   - Remote branches are prefixed with `remotes/origin/`

2. **Switch to an existing branch:**

   ```bash
   git checkout <branch-name>
   ```

   or using the newer syntax:

   ```bash
   git switch <branch-name>
   ```

3. **Create and switch to a new branch:**

   ```bash
   git checkout -b <new-branch-name>
   ```

   or using the newer syntax:

   ```bash
   git switch -c <new-branch-name>
   ```

4. **Update your local repository:**
   ```bash
   git fetch origin
   git pull origin <branch-name>
   ```

#### Best Practices

- Always create feature branches from the latest `main` branch
- Use descriptive branch names (e.g., `feature/scoreboard-updates`, `fix/initiative-bug`)
- Keep branches up to date with `main` to avoid merge conflicts
- Delete branches after they're merged

## License

[Add your license information here]
