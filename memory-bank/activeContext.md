# Active Context: Scorer

This document outlines the current work focus, recent changes, next steps, and active decisions for the Scorer project.

## 1. Current Work Focus

- **Primary**: Thorough testing of all implemented Kivy application features on macOS, focusing on stability, data persistence (especially immediate saves for score/CP), and the complete game lifecycle from splash screen to game over, including resume/new game scenarios.
- **Secondary**: Consolidating learnings and ensuring documentation (Memory Bank, `.cursorrules`) is up-to-date.
- **Upcoming**: Preparing for initial deployment and testing on the Raspberry Pi if macOS stability is confirmed.

## 2. Recent Changes & Decisions

- **Enhanced Data Persistence Implemented**:
  - Game state (`game_state.json`) is now saved **immediately** after any score modification via the numpad (`process_numpad_value`) or any Command Point adjustment (`add_cp`, `remove_cp`) in `ScorerRootWidget`.
  - This significantly mitigates the risk of data loss for these critical, infrequent changes between turns or other major save points (like app exit, end of turn, concession).
- **macOS Window Sizing Resolved**:
  - The Kivy application window on macOS now consistently launches at the target 800x480 resolution.
  - This was achieved by setting `Config.set('graphics', 'resizable', False)` and explicitly calling `Window.size = (800, 480)` in `main.py` before `App.run()`.
  - Previous attempts (clearing Kivy config, using halved values in `Config.set`) were not consistently effective; the direct `Window.size` call proved most reliable for development.
- **Splash Screen Image Corrected**:
  - The `SplashScreen` now correctly displays the `assets/splash.png` image, stretched to fill the screen as intended.
  - Path issue in `scorer.kv` was resolved.
- **"Resume or New Game" Feature Completed & Tested**:
  - This flow is stable, handling various save file states and navigating correctly.
- **Core Game Logic Stabilized**:
  - Timer functionality, "End Turn" button logic, and `ObjectProperty` bindings for UI elements in `ScorerRootWidget` are stable and tested.
  - Concession logic is in place and functional.

## 3. Next Steps

- **Comprehensive macOS Testing**: Rigorously test all aspects of the application:
  - All screen transitions and button functionalities.
  - Game state saving and loading: Test resume from various game phases (name entry, deployment, first turn, playing, game over).
  - Verify immediate saves for score/CP by simulating interruptions (e.g., force quit if safe, or simply checking `game_state.json` after a change but before ending a turn).
  - Edge cases in input or game flow.
- **Gather User (Your) Feedback**: Once testing provides confidence, get your feedback on the current features, UI, and overall usability.
- **Raspberry Pi Deployment Plan**: If macOS version is stable and meets requirements:
  - Outline steps for deploying to the Raspberry Pi.
  - Identify any necessary Pi-specific configurations (e.g., for GPIO, different display settings if not covered by current OS detection).
- **Review `.cursorrules` and Memory Bank**: Ensure all recent learnings and patterns are documented.

## 4. Active Questions & Considerations

- Is the current macOS window sizing solution (explicit `Window.size` call) acceptable for all intended development and testing environments, or should further investigation into Kivy's metrics/density handling on macOS be pursued if discrepancies arise on other Mac systems?
- Are there any other user interactions or state changes that are infrequent but critical enough to warrant an immediate save to `game_state.json`?
- What is the intended functionality for the "Settings" button on `ScorerRootWidget` (currently exits app)? This needs to be defined for future implementation.
- For Raspberry Pi: Will any hardware-specific interactions (e.g., physical buttons via GPIO) be needed that might affect the Kivy app structure or event handling?

## Current Focus

- Resolving SDL2 KMSDRM support issue for Raspberry Pi 5 display
- Ensuring proper display configuration for DSI display

## Recent Changes

- Identified that SDL2 needs to be built from source with KMSDRM support
- Documented required build dependencies and configuration steps
- Added detailed display configuration parameters to techContext.md

## Active Decisions

1. SDL2 Build:

   - Must build SDL2 from source with KMSDRM support
   - Default apt package lacks required KMSDRM support
   - Need to install specific build dependencies

2. Display Configuration:
   - Using DSI display (card1) with specific parameters
   - CRTC ID: 34
   - Connector ID: 36
   - Display mode: 800x480@60Hz

## Next Steps

1. Build SDL2 from source with KMSDRM support:

   ```bash
   sudo apt-get update
   sudo apt-get install -y build-essential git autoconf automake libtool pkg-config \
     libasound2-dev libpulse-dev libaudio-dev libx11-dev libxext-dev \
     libxrandr-dev libxcursor-dev libxi-dev libxinerama-dev libxxf86vm-dev \
     libxss-dev libgl1-mesa-dev libesd0-dev libdbus-1-dev libudev-dev \
     libgles2-mesa-dev libegl1-mesa-dev libibus-1.0-dev \
     libdrm-dev libgbm-dev libinput-dev libudev-dev libxkbcommon-dev

   git clone https://github.com/libsdl-org/SDL.git
   cd SDL
   ./configure --enable-video-kmsdrm --enable-video-opengl --enable-video-opengles \
     --enable-video-opengles2 --enable-video-egl --enable-video-gbm \
     --enable-video-dummy --enable-video-x11 --enable-video-wayland \
     --enable-video-rpi --enable-video-vivante --enable-video-cocoa \
     --enable-video-metal --enable-video-vulkan --enable-video-offscreen
   make -j4
   sudo make install
   sudo ldconfig
   ```

2. After SDL2 rebuild:
   - Run kivy_backend_test.py again
   - Verify KMSDRM support is available
   - Check display output

## Current Issues

1. SDL2 KMSDRM Support:

   - Error: "kmsdrm not available"
   - Need to rebuild SDL2 from source
   - Default package lacks KMSDRM support

2. Display Configuration:
   - DSI display properly initialized
   - VC4 driver reports issues
   - Need to ensure correct display mode settings

## Environment Setup

- Using specific environment variables for SDL2/KMSDRM
- Debug logging enabled
- DSI display configuration parameters set
