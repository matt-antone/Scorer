# Screensaver Screen

# Version History

- v1.0.0 (2024-03-21): Initial version
- v2.0.0 (2024-07-29): Reconciled documentation to reflect behavior with static/custom images and correct transition flow.

Last Updated: 2024-07-29 10:00 UTC

# Related Files

- [../app.md](../app.md): Main Kivy application
- [settings_screen.md](./settings_screen.md): Where the screensaver is configured.

# Overview

The Screensaver Screen provides a simple display mode that shows either the default or a custom uploaded picture. It is displayed when the app is idle (if enabled in settings) and helps prevent screen burn-in.

# Purpose

- Activate after a period of inactivity if enabled in settings.
- Display a full-screen static image (either default or user-uploaded).
- Exit upon any touch input, returning to the previous screen.

# Properties

- `screensaver_image`: An `Image` widget that displays the picture.

# Methods

- `on_pre_enter()`: Loads the correct image source (default or custom) from the application's settings.
- `on_touch_down(touch)`: Detects any touch on the screen and transitions back to the previous screen.

# Events

- `on_exit_screensaver`: Fired when a touch is detected, triggering the screen transition.

# Behavior & Flow

## Activation

- The screensaver is enabled or disabled via the `SettingsScreen`.
- If enabled, the main application controller (`ScorerApp`) monitors for inactivity.
- After a set period of no user input on any screen, the controller transitions to the `ScreensaverScreen`.

## Display

- The screen displays a single, static image.
- The image source is determined by the settings: it's either the default picture (`assets/billboards/default.jpg`) or a custom picture uploaded by the user.
- The picture is scaled to fit the screen while maintaining its aspect ratio and is centered.
- A small "Touch anywhere to exit" label is displayed at the bottom.

## Deactivation

- Any touch event on the screen will immediately transition the view back to the screen that was active before the screensaver started.

# Key Implementation Details

- **File Location**: `screens/screensaver_screen.py`
- **Settings Integration**: The screen's behavior is entirely dependent on settings managed in the `SettingsScreen` and stored persistently.
- **Picture Handling**: Loads images from the `assets/billboards/` directory. Custom pictures are stored in a `custom/` subdirectory.
- **Activity Timeout**: The timeout logic resides in the main `App` class, not in the individual screens.

# Changelog

## 2024-07-29

- Reconciled documentation to describe the correct behavior using a static image instead of an animation.
- Updated the flow to clarify that it returns to the previous screen, not always the splash screen.
- Added details about settings integration and image handling.

## 2024-03-21

- Initial documentation (describing a generic animation and incorrect transition).
- Linked related files.
