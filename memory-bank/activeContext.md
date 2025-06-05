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

- Resolving SDL2 KMSDRM support issues
- Ensuring proper display configuration for camera/display socket 1
- Investigating DSI display initialization through tc358762 device
- Platform-aware script execution environment

## Recent Changes

- Added platform detection to launch_scorer.sh
- Documented DSI display configuration requirements
- Added tc358762 overlay to /boot/firmware/config.txt
- Updated .cursorrules with bash script execution environment requirements

## Active Decisions

- Using KIVY_BCM_DISPMANX_ID=5 for camera/display socket 1
- Building SDL2 from source with KMSDRM support
- Configuring DSI display through tc358762 device
- Platform-specific environment variables in launch scripts

## Current Challenges

- KMSDRM support not available despite correct SDL2 build
- DSI display not showing up in DRM devices
- Need to verify tc358762 overlay configuration
- Need to ensure proper user permissions for DRM access

## Next Steps

1. Verify tc358762 overlay parameters
2. Check DRM device permissions
3. Test DSI display initialization
4. Monitor SDL2/KMSDRM debug output

## Open Questions

- Are all required DSI parameters correctly set?
- Is the tc358762 device properly initialized?
- Are there any missing overlays or configurations?
- Do we need additional kernel modules loaded?

## Recent Discoveries

- Display is connected through camera/display socket 1
- tc358762 device requires specific DSI configuration
- KIVY_BCM_DISPMANX_ID=5 is required for camera/display socket
- Platform detection is needed for environment variables

## Current Environment

- Development: macOS
- Target: Raspberry Pi 5 with 5-inch DSI touchscreen
- Display Interface: Camera/Display Socket 1
- DSI Device: tc358762

## Active Considerations

- Need to maintain separate configurations for macOS and Raspberry Pi
- Must ensure proper display initialization on Raspberry Pi
- Need to verify hardware acceleration support
- Must document all platform-specific requirements
