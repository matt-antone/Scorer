# Kivy Application

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [screens/splash_screen.md](./screens/splash_screen.md): Splash screen implementation
- [screens/resume_or_new_screen.md](./screens/resume_or_new_screen.md): Resume or new game screen
- [screens/name_entry_screen.md](./screens/name_entry_screen.md): Name entry screen
- [screens/deployment_setup_screen.md](./screens/deployment_setup_screen.md): Deployment setup screen
- [screens/first_turn_setup_screen.md](./screens/first_turn_setup_screen.md): First turn setup screen
- [screens/game_over_screen.md](./screens/game_over_screen.md): Game over screen
- [screens/screensaver_screen.md](./screens/screensaver_screen.md): Screensaver screen
- [../../api/state_server/state_management.md](../../api/state_server/state_management.md): State management API

# Overview

The Kivy Application is the main entry point for the game interface. It manages the application lifecycle, screen transitions, and game state.

# Purpose

- Initialize application
- Manage screen transitions
- Handle game state
- Process user input
- Manage application lifecycle

# Properties

- `game_state`: Current game state
  ```json
  {
    "game_id": "string",
    "status": "string",
    "players": {
      "player1": {
        "id": "string",
        "name": "string",
        "score": number,
        "timer": number,
        "is_current_player": boolean
      },
      "player2": {
        "id": "string",
        "name": "string",
        "score": number,
        "timer": number,
        "is_current_player": boolean
      }
    },
    "current_screen": "string",
    "last_action": "string",
    "last_action_time": "ISO8601"
  }
  ```
- `settings`: Application settings
  ```json
  {
    "theme": {
      "primary_color": "string",
      "secondary_color": "string",
      "background_color": "string",
      "text_color": "string"
    },
    "screensaver": {
      "enabled": boolean,
      "timeout": number,
      "dim_level": number
    },
    "sound": {
      "enabled": boolean,
      "volume": number,
      "effects": boolean,
      "music": boolean
    },
    "display": {
      "fullscreen": boolean,
      "orientation": "string",
      "resolution": {
        "width": number,
        "height": number
      }
    }
  }
  ```

# Methods

- `build()`: Build application
- `on_start()`: Handle application start
- `on_stop()`: Handle application stop
- `on_pause()`: Handle application pause
- `on_resume()`: Handle application resume
- `load_game_state()`: Load game state
- `save_game_state()`: Save game state
- `update_game_state(state)`: Update game state
- `switch_screen(screen_name)`: Switch to screen
- `handle_input(event)`: Handle user input
- `start_screensaver()`: Start screensaver
- `stop_screensaver()`: Stop screensaver

# Events

- `app_started`: Fired when application starts
- `app_stopped`: Fired when application stops
- `app_paused`: Fired when application pauses
- `app_resumed`: Fired when application resumes
- `game_state_loaded`: Fired when game state is loaded
- `game_state_saved`: Fired when game state is saved
- `game_state_updated`: Fired when game state is updated
- `screen_changed`: Fired when screen changes
- `screensaver_started`: Fired when screensaver starts
- `screensaver_stopped`: Fired when screensaver stops

# Flow

1. Initialize application
2. Load settings
3. Load game state
4. Build interface
5. Handle user input
6. Update game state
7. Save game state

# Example Usage

```python
# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
import json
import os

class ScorerApp(App):
    # Properties
    game_state = ObjectProperty(None)
    settings = ObjectProperty(None)
    current_screen = StringProperty('splash')
    screensaver_active = ObjectProperty(False)

    def build(self):
        try:
            # Initialize settings
            self.settings = self.load_settings()

            # Configure window
            self.configure_window()

            # Initialize game state
            self.game_state = self.load_game_state()

            # Create screen manager
            self.screen_manager = ScreenManager()

            # Add screens
            self.add_screens()

            # Bind events
            self.bind_events()

            # Start screensaver timer
            self.start_screensaver_timer()

            return self.screen_manager
        except Exception as e:
            self.handle_error(e)
            raise

    def load_settings(self):
        try:
            settings_path = os.path.join(self.user_data_dir, 'settings.json')
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    return json.load(f)
            return self.get_default_settings()
        except Exception as e:
            self.handle_error(e)
            return self.get_default_settings()

    def get_default_settings(self):
        return {
            'theme': {
                'primary_color': '#FF0000',
                'secondary_color': '#0000FF',
                'background_color': '#FFFFFF',
                'text_color': '#000000'
            },
            'screensaver': {
                'enabled': True,
                'timeout': 300,
                'dim_level': 0.5
            },
            'sound': {
                'enabled': True,
                'volume': 0.7,
                'effects': True,
                'music': True
            },
            'display': {
                'fullscreen': True,
                'orientation': 'landscape',
                'resolution': {
                    'width': 800,
                    'height': 480
                }
            }
        }

    def configure_window(self):
        try:
            if platform == 'android':
                from android.permissions import request_permissions, Permission
                request_permissions([
                    Permission.INTERNET,
                    Permission.ACCESS_NETWORK_STATE
                ])

            Window.fullscreen = self.settings['display']['fullscreen']
            Window.orientation = self.settings['display']['orientation']

            if not Window.fullscreen:
                Window.size = (
                    self.settings['display']['resolution']['width'],
                    self.settings['display']['resolution']['height']
                )
        except Exception as e:
            self.handle_error(e)

    def load_game_state(self):
        try:
            state_path = os.path.join(self.user_data_dir, 'game_state.json')
            if os.path.exists(state_path):
                with open(state_path, 'r') as f:
                    return json.load(f)
            return self.get_default_game_state()
        except Exception as e:
            self.handle_error(e)
            return self.get_default_game_state()

    def get_default_game_state(self):
        return {
            'game_id': '',
            'status': 'waiting',
            'players': {
                'player1': {
                    'id': '',
                    'name': '',
                    'score': 0,
                    'timer': 0,
                    'is_current_player': False
                },
                'player2': {
                    'id': '',
                    'name': '',
                    'score': 0,
                    'timer': 0,
                    'is_current_player': False
                }
            },
            'current_screen': 'splash',
            'last_action': '',
            'last_action_time': None
        }

    def add_screens(self):
        try:
            from screens.splash_screen import SplashScreen
            from screens.resume_or_new_screen import ResumeOrNewScreen
            from screens.name_entry_screen import NameEntryScreen
            from screens.deployment_setup_screen import DeploymentSetupScreen
            from screens.first_turn_setup_screen import FirstTurnSetupScreen
            from screens.game_over_screen import GameOverScreen
            from screens.screensaver_screen import ScreensaverScreen

            self.screen_manager.add_widget(SplashScreen(name='splash'))
            self.screen_manager.add_widget(ResumeOrNewScreen(name='resume_or_new'))
            self.screen_manager.add_widget(NameEntryScreen(name='name_entry'))
            self.screen_manager.add_widget(DeploymentSetupScreen(name='deployment_setup'))
            self.screen_manager.add_widget(FirstTurnSetupScreen(name='first_turn_setup'))
            self.screen_manager.add_widget(GameOverScreen(name='game_over'))
            self.screen_manager.add_widget(ScreensaverScreen(name='screensaver'))
        except Exception as e:
            self.handle_error(e)
            raise

    def bind_events(self):
        try:
            Window.bind(on_keyboard=self.handle_keyboard)
            self.bind(current_screen=self.on_screen_change)
            self.bind(game_state=self.on_game_state_change)
        except Exception as e:
            self.handle_error(e)

    def start_screensaver_timer(self):
        try:
            if self.settings['screensaver']['enabled']:
                self.screensaver_timer = Clock.schedule_interval(
                    self.check_screensaver,
                    self.settings['screensaver']['timeout']
                )
        except Exception as e:
            self.handle_error(e)

    def check_screensaver(self, dt):
        try:
            if not self.screensaver_active and self.settings['screensaver']['enabled']:
                self.start_screensaver()
        except Exception as e:
            self.handle_error(e)

    def start_screensaver(self):
        try:
            self.screensaver_active = True
            self.switch_screen('screensaver')
            self.emit('screensaver_started')
        except Exception as e:
            self.handle_error(e)

    def stop_screensaver(self):
        try:
            self.screensaver_active = False
            self.switch_screen(self.game_state['current_screen'])
            self.emit('screensaver_stopped')
        except Exception as e:
            self.handle_error(e)

    def handle_keyboard(self, window, key, *args):
        try:
            if key == 27:  # ESC key
                if self.screensaver_active:
                    self.stop_screensaver()
                return True
            return False
        except Exception as e:
            self.handle_error(e)
            return False

    def on_screen_change(self, instance, value):
        try:
            self.emit('screen_changed', value)
        except Exception as e:
            self.handle_error(e)

    def on_game_state_change(self, instance, value):
        try:
            self.emit('game_state_updated', value)
            self.save_game_state()
        except Exception as e:
            self.handle_error(e)

    def switch_screen(self, screen_name):
        try:
            self.current_screen = screen_name
            self.game_state['current_screen'] = screen_name
            self.screen_manager.current = screen_name
        except Exception as e:
            self.handle_error(e)

    def save_game_state(self):
        try:
            state_path = os.path.join(self.user_data_dir, 'game_state.json')
            with open(state_path, 'w') as f:
                json.dump(self.game_state, f)
            self.emit('game_state_saved')
        except Exception as e:
            self.handle_error(e)

    def update_game_state(self, state):
        try:
            self.game_state.update(state)
            self.emit('game_state_updated', self.game_state)
        except Exception as e:
            self.handle_error(e)

    def on_start(self):
        try:
            self.emit('app_started')
        except Exception as e:
            self.handle_error(e)

    def on_stop(self):
        try:
            self.save_game_state()
            self.emit('app_stopped')
        except Exception as e:
            self.handle_error(e)

    def on_pause(self):
        try:
            self.save_game_state()
            self.emit('app_paused')
        except Exception as e:
            self.handle_error(e)

    def on_resume(self):
        try:
            self.emit('app_resumed')
        except Exception as e:
            self.handle_error(e)

    def handle_error(self, error):
        print(f"Error in ScorerApp: {str(error)}")

if __name__ == '__main__':
    ScorerApp().run()
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, methods, and flow
- Added application lifecycle management
- Added screen management
- Added game state handling
- Added screensaver functionality
- Linked related API documentation
