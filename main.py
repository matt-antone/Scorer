import platform # For OS detection
import os # Import os
import json # For saving/loading game state
import time # Added for timer
import qrcode
import io

from kivy.config import Config # Ensure Config is imported AFTER env vars are set

# OS-specific graphics configuration
os_type = platform.system()
if os_type == "Linux":  # Assuming Raspberry Pi OS reports as Linux
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'show_cursor', '0') # Hide cursor for kiosk on Pi
    Config.set('graphics', 'borderless', '1') # Attempt to set borderless early for Pi
    Config.set('graphics', 'window_state', 'maximized') # Add attempt to maximize window state
    Config.set('kivy', 'keyboard_mode', 'dock') # Enable docked keyboard for Pi
else:  # Default to development mode (e.g., macOS, Windows)
    Config.set('graphics', 'fullscreen', '0') # Ensure not fullscreen
    Config.set('graphics', 'show_cursor', '1') # Show cursor for dev
    # Set fixed size for development environments only
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '480')
    Config.set('graphics', 'resizable', False)

from kivy.core.window import Window # Ensure Window is imported AFTER Config changes

import random # Added for initiative roll
# Set default font *before* other Kivy components are imported if possible
# Note: Paths here assume the script is run from the project root where assets/fonts exists.
# If running from a different CWD, these paths might need to be absolute or adjusted.

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button # Import Button
from kivy.properties import StringProperty # Removed BooleanProperty, DictProperty, NumericProperty, ObjectProperty
from kivy.uix.popup import Popup # Import Popup
from kivy.metrics import dp # Import dp from kivy.metrics
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition # Added ScreenManager, Screen, FadeTransition
from kivy.clock import Clock # Added for timer updates
from kivy.core.text import LabelBase # For registering fonts by name
from db.integration import reset_db_for_new_game_sync
from websocket_server import WebSocketServer
from screens.screensaver_screen import ScreensaverScreen
from screens.splash_screen import SplashScreen
from screens.deployment_setup_screen import DeploymentSetupScreen
from screens.name_entry_screen import NameEntryScreen
from screens.first_turn_setup_screen import FirstTurnSetupScreen
from screens.scorer_root_widget import ScorerRootWidget
from screens.game_over_screen import GameOverScreen
from screens.resume_or_new_screen import ResumeOrNewScreen

# Register the Inter font family so it can be referred to by name 'Inter' in KV if needed.
# This also acts as a fallback or explicit way to use it.

# Register NotoColorEmoji font

# Register Inter Black specifically for the new design
_inter_black_font_path = "assets/fonts/Inter/static/Inter_18pt-Black.ttf"
if os.path.exists(_inter_black_font_path):
    LabelBase.register(name='InterBlack', fn_regular=_inter_black_font_path)
    print(f"Registered font: InterBlack from {_inter_black_font_path}")
else:
    print(f"Warning: Font file not found at {_inter_black_font_path}. InterBlack will not be available.")

# Configure the window to be a fixed size, simulating the Pi screen for now
# We can make this more dynamic or fullscreen later.
# Config.set('graphics', 'width', '800') # MOVED
# Config.set('graphics', 'height', '480') # MOVED
# Config.set('graphics', 'resizable', False) # MOVED

# --- New Setup Screens ---

class ScorerApp(App):
    SAVE_FILE_NAME = "game_state.json"
    VISIBLE_SPLASH_TIME = 4 # Desired visible time for the splash screen
    INACTIVITY_TIMEOUT_SECONDS = 60 # 5 minutes
    target_screen_after_splash = None
    last_active_screen = None # To store the screen before screensaver
    p1_qr_path = StringProperty(".cache/p1_qr.png")
    p2_qr_path = StringProperty(".cache/p2_qr.png")
    observer_qr_path = StringProperty(".cache/observer_qr.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = self._get_default_game_state()
        self.ws_server = WebSocketServer(
            get_game_state_callback=self.get_game_state,
            broadcast_callback=self.save_game_state # Use save_game_state to trigger broadcasts
        )

    def _get_default_game_state(self):
        """Returns a new, clean game state dictionary."""
        return {
            "player1": {"name": "Player 1", "primary_score": 0, "secondary_score": 0, "total_score": 0, "cp": 1, "deployment_roll": 0, "first_turn_roll": 0, "player_elapsed_time_seconds": 0.0, "player_time_display": "00:00:00"},
            "player2": {"name": "Player 2", "primary_score": 0, "secondary_score": 0, "total_score": 0, "cp": 1, "deployment_roll": 0, "first_turn_roll": 0, "player_elapsed_time_seconds": 0.0, "player_time_display": "00:00:00"},
            "current_round": 0,
            "active_player_id": None,
            "deployment_initiative_winner_id": None,
            "deployment_attacker_id": None,
            "deployment_defender_id": None,
            "first_turn_choice_winner_id": None,
            "first_player_of_game_id": None,
            "last_round_played": 0,
            "game_phase": "setup", # initial state
            "game_timer": {"status": "stopped", "start_time": None, "elapsed_display": "00:00:00", "turn_segment_start_time": None}
        }

    def reset_game_state_to_default(self):
        """Resets the current game state to the default."""
        self.game_state = self._get_default_game_state()

    def show_error_popup(self, title, message):
        """Displays an error popup dialog."""
        popup_content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        popup_content.add_widget(Label(text=message, size_hint_y=None, height=dp(40)))
        ok_button = Button(text='OK', size_hint_y=None, height=dp(50))
        popup_content.add_widget(ok_button)
        
        popup = Popup(title=title, content=popup_content, size_hint=(0.8, 0.4))
        ok_button.bind(on_press=popup.dismiss)
        popup.open()

    def start_new_game_flow(self):
        """Initiates the sequence for starting a new game."""
        # Reset the database synchronously
        reset_db_for_new_game_sync()
        # Reset the in-memory game state
        self.reset_game_state_to_default()
        # Update the game phase and save/broadcast
        self.game_state['game_phase'] = 'name_entry'
        self.save_game_state()
        # Switch to the name entry screen
        if self.root:
            self.switch_screen('name_entry')

    def get_save_file_path(self):
        """Returns the full path to the save file in the user's data directory."""
        return os.path.join(self.user_data_dir, self.SAVE_FILE_NAME)

    def save_game_state(self):
        """Saves the current game state to a JSON file and triggers a broadcast."""
        try:
            with open(self.get_save_file_path(), 'w') as f:
                json.dump(self.game_state, f)
            # After saving, broadcast the new state to all clients
            if self.ws_server:
                self.ws_server.broadcast_game_state()
        except Exception as e:
            print(f"Error saving game state: {e}")

    def load_game_state(self):
        """
        Loads the game state from the JSON file.
        If the file doesn't exist or is invalid, returns a default state.
        This also determines if a splash screen should be shown.
        """
        save_file = self.get_save_file_path()
        if os.path.exists(save_file):
            try:
                with open(save_file, 'r') as f:
                    loaded_state = json.load(f)
                # Basic validation to see if it's a meaningful game state
                if loaded_state and 'game_phase' in loaded_state:
                    self.game_state = loaded_state
                    print("Successfully loaded game state from file.")
                    return True # Indicate that a load happened
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading or parsing game state file: {e}. Starting fresh.")
                self.reset_game_state_to_default()
        else:
            print("No save file found. Starting with a fresh game state.")
            self.reset_game_state_to_default()
        return False # Indicate no load happened

    def _determine_screen_from_gamestate(self):
        """
        Determines the appropriate starting screen based on the game state.
        This allows resuming a game in progress.
        """
        if self.game_state and self.game_state.get('game_in_progress'):
            # If a game is in progress, go to the resume/new screen
            return 'resume_or_new'
        else:
            # Otherwise, start a new game flow
            return 'name_entry'

    def build(self):
        # Determine the initial screen based on saved state BEFORE building the UI
        # This tells the splash screen where to go next.
        self.target_screen_after_splash = self._determine_screen_from_gamestate()

        sm = ScreenManager(transition=FadeTransition(duration=0.5))

        # Pre-load all screens to make transitions instant after startup.
        # The `name` property is crucial for the ScreenManager to identify screens.
        sm.add_widget(Screen(name='startup')) # Blank startup screen
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(ResumeOrNewScreen(name='resume_or_new'))
        sm.add_widget(NameEntryScreen(name='name_entry'))
        sm.add_widget(DeploymentSetupScreen(name='deployment_setup'))
        sm.add_widget(FirstTurnSetupScreen(name='first_turn_setup'))
        sm.add_widget(ScorerRootWidget(name='game'))
        sm.add_widget(GameOverScreen(name='game_over'))
        sm.add_widget(ScreensaverScreen(name='screensaver'))

        return sm

    def transition_from_splash(self, target_screen_name, dt):
        """
        Callback from the splash screen to transition to the next screen.
        """
        if self.root.current == 'splash':
            print(f"ScorerApp: Transitioning from splash to {target_screen_name}")
            self.root.current = target_screen_name
            # Start the inactivity timer once the main app is visible
            self.reset_inactivity_timer()

    def initialize_game_state(self):
        self.game_state = self.load_game_state()

    def on_stop(self):
        """Called when the app is closing."""
        print("ScorerApp: on_stop called, attempting to save game state.")
        self.save_game_state()
        if self.ws_server:
            self.ws_server.stop()
        Clock.unschedule(self.start_screensaver)

    # --- Game State Update Methods ---
    def update_score(self, player_id, new_score):
        player_key = f"player{player_id}"
        if player_key in self.game_state:
            self.game_state[player_key]['total_score'] = new_score
            self.save_game_state()

    def update_cp(self, player_id, new_cp):
        player_key = f"player{player_id}"
        if player_key in self.game_state:
            self.game_state[player_key]['cp'] = new_cp
            self.save_game_state()

    def update_timer(self, timer_data):
        self.game_state['game_timer'].update(timer_data)
        self.save_game_state()

    def update_round(self, round_number):
        self.game_state['current_round'] = round_number
        self.save_game_state()

    def update_game_phase(self, phase):
        self.game_state['game_phase'] = phase
        self.save_game_state()

    def set_player_name(self, player_id, name):
        player_key = f"player{player_id}"
        if player_key in self.game_state:
            self.game_state[player_key]['name'] = name
            self.save_game_state()

    def get_game_state(self):
        """
        Designated callback for the WebSocket server.
        Returns a sanitized version of the application's game_state.
        """
        client_state = json.loads(json.dumps(self.game_state))
        current_screen = self.root.current if self.root else ''
        if current_screen == 'resume_or_new':
            client_state['game_phase'] = 'setup'
        if client_state.get('current_round', 0) > 5:
            client_state['current_round'] = 5
        if client_state.get('game_phase') == 'game_over':
            client_state['last_round_played'] = 5
            client_state['current_round'] = 5
        return client_state

    def switch_screen(self, screen_name):
        if self.root:
            self.root.current = screen_name

    def on_start(self):
        """Called after build() and the root widget is created."""
        # Step 1: Clean up old QR codes
        for path in [self.p1_qr_path, self.p2_qr_path, self.observer_qr_path]:
            if os.path.exists(path):
                os.remove(path)

        self.ws_server.start()
        Window.bind(on_touch_down=self.reset_inactivity_timer)
        Window.bind(on_flip=self._on_first_frame)

    def _on_first_frame(self, *args):
        """This event is called after the first frame is drawn."""
        print("DIAGNOSTIC: First frame drawn, transitioning to splash screen.")
        # Unbind this method so it doesn't get called on every frame
        Window.unbind(on_flip=self._on_first_frame)
        # Now it's safe to set the current screen
        self.root.current = 'splash'
        return True # Returning True consumes the event

    def reset_inactivity_timer(self, *args):
        if self.root and self.root.current == 'screensaver':
            # If on screensaver, deactivate it and go to the last known screen
            self.root.current = self.last_active_screen or self._get_screen_for_phase(self.game_state.get('game_phase', 'setup'))
            # Still restart the timer after this interaction
        
        # Always cancel the pending call and schedule a new one
        Clock.unschedule(self.start_screensaver)
        Clock.schedule_once(self.start_screensaver, self.INACTIVITY_TIMEOUT_SECONDS)

    def start_screensaver(self, dt):
        if self.root and self.root.current not in ['screensaver', 'splash']:
            self.last_active_screen = self.root.current
            self.root.current = 'screensaver'

    def _get_screen_for_phase(self, phase):
        phase_to_screen = {
            "splash": "splash",
            "resume_or_new": "resume_or_new",
            "name_entry": "name_entry",
            "deployment_setup": "deployment_setup",
            "first_turn_setup": "first_turn_setup",
            "game_play": "game",
            "game_over": "game_over"
        }
        return phase_to_screen.get(phase, "splash")  # Default to splash


if __name__ == '__main__':
    ScorerApp().run() 