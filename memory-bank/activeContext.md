# Active Context

## Current Focus

- **Post-Deployment Documentation:** The current focus is on updating all Memory Bank files to accurately reflect the successful deployment of the Scorer application onto the Raspberry Pi. This involves documenting the new installation process and updated technology stack.

## Recent Changes

- **Automated Installation Script (`install.sh`):** Overhauled the installation process into a single, robust script. It now handles system dependencies, Python packages, and programmatically creates the entire database structure, including source files and initializing the SQLite database with Alembic.
- **Technology Stack Simplification:**
  - Replaced the PostgreSQL database dependency with **SQLite**. This removes the need for an external database server and simplifies deployment significantly.
  - Pinned critical Python packages (`Flask`, `Flask-SocketIO`) in `requirements.txt` to resolve dependency conflicts and ensure a stable build.
- **"No Connection" Screen:** Implemented a UI screen on the web client that appears when the connection to the server is lost, improving user experience.

## Active Decisions

- **Automated First-Time Setup:** The project philosophy is that a user should be able to clone the repository and run a single `install.sh` script to get a fully working application, including the database.
- **Self-Contained Dependencies:** The application aims to be as self-contained as possible, with SQLite being a key part of that strategy.

## Next Steps

1. **Finalize Documentation:** Complete the updates to `progress.md` and any other necessary files to conclude this documentation cycle.
2. **Verify Pi Functionality:** Perform a final check of all features on the Raspberry Pi to ensure the recent changes have not introduced regressions.
3. **Plan Next Feature Sprint:** Begin planning the implementation of the next set of features, such as the dedicated "Player Client" for score updates.

## Open Questions

- Is a simple `show()`/`hide()` mechanism sufficient, or should the controller re-initialize screens each time they are shown?

## Current Challenges

- Refactoring the client-side JavaScript without introducing new bugs.
- Ensuring the new architecture is clean and maintainable.

## Environment Notes

- Development on macOS
- Target deployment on Raspberry Pi
- Virtual environment management
- Dependencies:
  - Flask-SocketIO
  - python-socketio
  - python-dotenv
  - asyncpg
  - SQLAlchemy
  - aiosqlite

## Tomorrow's Tasks

1. Review and refine game over screen styling
2. Ensure consistent font usage across all screens
3. Test game over state transitions
4. Verify all game data is displayed correctly
5. Document any additional styling requirements
