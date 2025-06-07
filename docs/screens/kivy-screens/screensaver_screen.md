# Screen: Screensaver Screen

## 1. Purpose

The Screensaver Screen provides a simple display mode that shows either the default or a custom uploaded picture. It helps prevent screen burn-in during periods of inactivity.

## 2. Behavior & Flow

### Activation

- Enabled/Disabled via settings
- Shows when enabled and no activity detected
- Touch anywhere to exit

### Display

- Shows either:
  - Default picture
  - Custom uploaded picture
- Picture is scaled to fit screen while maintaining aspect ratio
- Centered on screen

### Layout

```
[Picture Display]
[Touch anywhere to exit]
```

## 3. Screen Transition

- **Touch Anywhere**: Returns to the previous screen
- **Settings Change**: Updates when enabled/disabled or picture changes

## 4. Key Implementation Details

- **File Location**: `screens/screensaver_screen.py`
- **State Management**:
  - Monitors enabled/disabled state
  - Updates when picture changes
- **Picture Handling**:
  - Loads from assets directory
  - Maintains aspect ratio
  - Optimizes for display
- **Settings Integration**:
  - Reads enabled/disabled state
  - Loads current picture
  - Updates when settings change

## 5. Implementation Notes

### Settings Integration

```python
# In settings_screen.py
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screensaver_enabled = BooleanProperty(False)
        self.screensaver_image = StringProperty('default.jpg')

    def toggle_screensaver(self):
        self.screensaver_enabled = not self.screensaver_enabled

    def upload_screensaver_image(self):
        # Handle image upload
        pass
```

### Screensaver Screen

```python
# In screensaver_screen.py
class ScreensaverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image = Image()
        self.add_widget(self.image)

    def on_enter(self):
        # Load current image from settings
        app = App.get_running_app()
        if app.screensaver_enabled:
            self.image.source = app.screensaver_image
```

### Settings Storage

```json
{
  "screensaver": {
    "enabled": false,
    "image": "default.jpg"
  }
}
```

## 6. File Structure

```
assets/
  screensaver/
    default.jpg
    custom/
      user_uploaded.jpg
```

## 7. Usage Notes

- Default picture is provided in assets/screensaver/default.jpg
- Custom pictures are stored in assets/screensaver/custom/
- Pictures should be:
  - JPG or PNG format
  - Landscape orientation
  - Minimum resolution: 800x480
  - Maximum file size: 5MB
