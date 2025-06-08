- **Dependency Stability (macOS)**: Resolved a major dependency conflict between Kivy and ffpyplayer. By building `ffpyplayer` from source against a compatible version of `ffmpeg` (`ffmpeg@6`), we have eliminated runtime warnings about duplicate SDL2 libraries, which has fixed application instability and visual artifacts.
- **Automated Testing (Logic)**: A full suite of non-graphical unit tests for the application's core logic (`main.py`) is complete and passing. This provides confidence that game state, scoring, and turn progression function correctly.
- **Documentation**:
  - **Game Timer**: Completed documentation for a timestamp-based main game timer (`docs/game_timer.md`).
- **Focus:** The next major phase will be to implement the documented web client interactivity (setup, timers) and perform final testing.

## Known Issues

- **macOS Environment Sensitivity**: The Kivy windowing system on macOS can be fragile. Because the `install.sh` script manages `SDL2` by installing and then uninstalling it, any other system update or change (e.g., via Homebrew) can break the environment. If the app fails to launch with an `SDL2` error, the solution is to re-run `./install.sh`.

## Blockers

- **Automated Graphical Testing**: As detailed in `techContext.md`, automated testing of Kivy UI components is currently blocked on macOS. The `GraphicUnitTest` framework fails to initialize correctly, preventing any graphical tests from passing. This is a framework-level issue with no current workaround.

## Next Steps

- Implement the new client-driven setup flow.
