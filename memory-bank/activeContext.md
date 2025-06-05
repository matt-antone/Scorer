# Active Context

## Current Focus

- **Memory Bank Audit:** The primary focus is a comprehensive audit of all `memory-bank/` files. The goal is to identify and correct errors, remove duplicated information, and ensure each document serves a clear and distinct purpose. This is a critical maintenance task to ensure the project's documentation is reliable.

## Recent Changes

- **Refactored `techContext.md`:** Completely restructured the file to eliminate duplicate sections, remove incorrect information (e.g., PostgreSQL dependencies), and create a single, clear source of truth for the project's technical stack and platform configuration.
- **Completed Client-Server Bug Fixes:** Successfully resolved the series of bugs related to client-server state synchronization, including the "stuck on Game Over screen" issue, the "Round 6" logic error, and the missing `name_entry` game phase.
- **Documentation Overhaul:** Created extensive documentation in `systemPatterns.md`, including data schemas and sequence diagrams, to solidify the application's architecture.

## Active Decisions

- **Single Source of Truth:** Enforcing a strict policy that each piece of project knowledge resides in only one document. For example, `techContext.md` defines the _what_ (technologies), while `systemPatterns.md` defines the _how_ (architecture).
- **Systematic Audit Process:** Auditing files sequentially (`projectbrief.md`, `productContext.md`, `techContext.md`, `systemPatterns.md`, etc.) to build a consistent understanding and spot inconsistencies.

## Next Steps

1. **Complete the Audit:**
   - Audit `progress.md` to ensure it reflects the latest project status.
   - Audit the non-core file `sdl2_kmsdrm_setup.md` to determine if its contents are redundant and should be merged or deleted.
2. **Report Findings:** Present a summary of all findings from the audit.
3. **Finalize Corrections:** Apply any remaining necessary changes to the memory bank based on the audit's conclusions.

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
