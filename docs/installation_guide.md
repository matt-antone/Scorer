# Installation Guide

This guide provides detailed instructions for setting up the Warhammer 40k Scorer project on your system.

## Prerequisites

- Python 3.8 or higher
- Git
- Homebrew (on macOS)
- SDL2 and related libraries (installed automatically by the installer)

## Installation Steps

### 1. Clone the Repository

```bash
git clone [repository-url]
cd Scorer
```

### 2. Run the Installer

The project includes an automated installer script that handles all setup tasks:

```bash
./install.sh
```

**Important:** Do not run the installer with sudo. The script will handle dependencies as the current user.

The installer will:

1. Install and link Homebrew dependencies (ffmpeg@6, SDL2, etc.)
2. Create a virtual environment for the Pi Client
3. Install all Python dependencies (including ffpyplayer) in the Pi Client's virtual environment
4. Build ffpyplayer from source with system libraries
5. Run Alembic migrations using the Pi Client's virtual environment
6. Configure the environment

### 3. Verify Installation

After installation, verify that all components are set up correctly:

#### Pi Client

```bash
cd pi_client
./launch_scorer.sh
```

If you see the app launch without errors, the installation was successful and all dependencies are working.

#### State Server

```bash
cd state_server
source ../pi_client/.venv/bin/activate
python main.py
```

## Project Structure

```
Scorer/
├── pi_client/              # Kivy application for Raspberry Pi
│   ├── assets/         # Application assets
│   ├── screens/        # Kivy screen definitions
│   ├── widgets/        # Custom Kivy widgets
│   ├── main.py         # Main application entry point
│   └── launch_scorer.sh # Launcher script
├── state_server/       # Flask-based state server
│   ├── db/            # Database and migrations
│   ├── api/           # API endpoints
│   └── main.py        # Server entry point
├── phone_clients/     # Web-based client applications
├── docs/              # Project documentation
├── memory-bank/       # Project context and documentation
├── tests/             # Test suite
└── install.sh         # Installation script
```

## Troubleshooting

### Common Issues

1. **Permission Denied**

   - Ensure you're not running the installer as root
   - Check file permissions in the project directory

2. **Missing Dependencies**

   - Run `./install.sh` again to reinstall dependencies
   - Check the installation log for specific errors

3. **Database Migration Issues**
   - Ensure you're in the correct directory when running migrations
   - Check the database configuration in `state_server/db/alembic.ini`

### Getting Help

If you encounter issues not covered in this guide:

1. Check the project's issue tracker
2. Review the memory bank documentation
3. Contact the development team

## Next Steps

After installation:

1. Review the project documentation in `docs/`
2. Set up your development environment
3. Run the test suite to verify everything works
4. Start developing!

## Contributing

See the main README.md for contribution guidelines and project structure details.
