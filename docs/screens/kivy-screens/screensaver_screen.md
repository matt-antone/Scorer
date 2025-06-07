# Screen: Screensaver Screen

## 1. Purpose

The `ScreensaverScreen` is designed to prevent screen burn-in on the DSI display and add visual interest during periods of inactivity. It automatically takes over the screen and displays a slideshow of images.

## 2. Behavior & Flow

### Activation

- An inactivity timer runs continuously in the background while the application is on the `ScorerRootWidget`.
- If no touch input is detected for a set period (e.g., 5 minutes), the `ScorerApp` controller automatically switches the screen to the `ScreensaverScreen`.
- The name of the previously active screen (`ScorerRootWidget`) is stored so the application knows where to return.

### Slideshow

- Upon activation, the screen begins a slideshow of all images found in the `assets/billboards/` directory.
- **Randomization**: The order of the images is randomized at the start of each slideshow to ensure variety.
- **Transitions**: The screen uses a slow, two-second fade animation (`Animation(opacity=0, d=2)`) to create a smooth and visually appealing transition between images.
- The slideshow loops indefinitely until it is interrupted.

### Deactivation

- The screensaver is deactivated by any touch input on the screen (`on_touch_down` event).
- When a touch is detected, the `ScorerApp` controller switches the view back to the previously active screen (which is almost always the `ScorerRootWidget`).

## 3. Screen Transition

- **To this screen**: Transitions automatically from `ScorerRootWidget` after a period of user inactivity.
- **From this screen**: Transitions back to `ScorerRootWidget` (or whichever screen was active before) immediately upon user touch input.

## 4. Key Implementation Details

- **File Location**: `screens/screensaver_screen.py`
- **Inactivity Logic**: The inactivity timer and the logic for switching to and from the screensaver are managed globally by the `ScorerApp` class.
- **Image Loading**: The screen dynamically loads all `.png` and `.jpg` files from the target directory.
- **Animation**: Uses Kivy's `Animation` class to handle the fading effect between slides, providing a more polished user experience than an abrupt image switch.
- **Synchronization**: The activation of this screen on the Kivy host triggers a corresponding screen change on all connected observer and player clients, ensuring a synchronized experience across all views.
