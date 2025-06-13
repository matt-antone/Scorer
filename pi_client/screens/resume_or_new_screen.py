from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.clock import Clock
import logging
import os
import json
from .base_screen import BaseScreen, ValidationError, StateError, SyncError

logger = logging.getLogger(__name__)

class ResumeOrNewScreen(BaseScreen):
    """Screen for choosing to resume a saved game or start a new one."""
    
    # Properties
    has_saved_game = BooleanProperty(False)
    saved_game_info = ObjectProperty(None)
    save_file_path = ObjectProperty(None)
    save_file_error = StringProperty('')
    game_resumed = BooleanProperty(False)
    is_loading = BooleanProperty(False)
    status_text = StringProperty('')
    has_error = BooleanProperty(False)
    save_file_valid = BooleanProperty(False)
    new_game_started = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.logger.info("ResumeOrNewScreen: Initializing")
        self._loading_timeout = None
        self._error_timeout = None
        self._start_background_tasks()

    def _start_background_tasks(self):
        """Start background tasks for initialization."""
        self.logger.info("ResumeOrNewScreen: Scheduling background tasks")
        Clock.schedule_once(self._perform_background_tasks)

    def _perform_background_tasks(self, dt):
        """Perform background initialization tasks."""
        self.detect_save_file()
        self.check_saved_game()

    def on_enter(self):
        """Called when the screen is entered."""
        super().on_enter()
        self.detect_save_file()
        self.check_saved_game()
        self.update_view_from_state()

    def update_view_from_state(self):
        """Update the view based on the current state."""
        if hasattr(self, 'resume_button'):
            self.resume_button.disabled = not self.has_saved_game
        if hasattr(self, 'new_game_button'):
            self.new_game_button.disabled = False

    def detect_save_file(self):
        """Detect if there is a save file."""
        try:
            save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'saves')
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            default_save_path = os.path.join(save_dir, 'game_save.json')
            if os.path.exists(default_save_path):
                self.save_file_path = default_save_path
                self.has_saved_game = True
            else:
                self.save_file_path = None
                self.has_saved_game = False
        except Exception as e:
            self.handle_save_file_error(str(e))

    def check_saved_game(self):
        """Check if there is a saved game."""
        if self.save_file_path and os.path.exists(self.save_file_path):
            try:
                with open(self.save_file_path, 'r') as f:
                    saved_game = json.load(f)
                self.validate_saved_game(saved_game)
                self.saved_game_info = saved_game
                self.has_saved_game = True
                self.save_file_valid = True
            except (json.JSONDecodeError, ValidationError, StateError) as e:
                self.handle_save_file_error(str(e))
        else:
            self.has_saved_game = False
            self.saved_game_info = None
            self.save_file_valid = False

    def resume_game(self):
        """Resume a saved game."""
        try:
            if not self.has_saved_game or not self.saved_game_info:
                raise StateError("No saved game to resume")
            
            app = App.get_running_app()
            if app and hasattr(app, 'game_state'):
                app.game_state.update(self.saved_game_info)
                self.game_resumed = True
                app.root.current = 'scoreboard'
        except Exception as e:
            self.handle_error(str(e))

    def start_new_game(self):
        """Start a new game."""
        try:
            app = App.get_running_app()
            if app and hasattr(app, 'game_state'):
                app.game_state.clear()
                app.game_state.update({
                    'p1_name': '',
                    'p2_name': '',
                    'p1_primary_score': 0,
                    'p2_primary_score': 0,
                    'p1_secondary_score': 0,
                    'p2_secondary_score': 0,
                    'p1_cp': 0,
                    'p2_cp': 0,
                    'winner': 0
                })
                self.game_resumed = False
                self.new_game_started = True
                app.root.current = 'name_entry'
        except Exception as e:
            self.handle_error(str(e))

    def validate_saved_game(self, saved_game):
        """Validate saved game data."""
        if not isinstance(saved_game, dict):
            raise ValidationError("Saved game must be a dictionary")
        
        required_keys = ['p1_name', 'p2_name', 'p1_primary_score', 'p2_primary_score']
        for key in required_keys:
            if key not in saved_game:
                raise StateError(f"Missing required saved game key: {key}")
        
        if not isinstance(saved_game['p1_name'], str) or not saved_game['p1_name']:
            raise ValidationError("Player 1 name must be a non-empty string")
        
        if not isinstance(saved_game['p2_name'], str) or not saved_game['p2_name']:
            raise ValidationError("Player 2 name must be a non-empty string")
        
        if not isinstance(saved_game['p1_primary_score'], (int, float)) or saved_game['p1_primary_score'] < 0:
            raise ValidationError("Player 1 primary score must be a non-negative number")
        
        if not isinstance(saved_game['p2_primary_score'], (int, float)) or saved_game['p2_primary_score'] < 0:
            raise ValidationError("Player 2 primary score must be a non-negative number")
        
        return True

    def handle_save_file_error(self, message):
        """Handle save file error."""
        self.save_file_error = message
        self.has_saved_game = False
        self.saved_game_info = None
        self.save_file_path = None
        self.save_file_valid = False
        self.handle_error(message)

    def handle_error(self, message):
        """Handle error."""
        self.show_error(message)
        self.has_error = True

    def clear_error(self):
        """Clear error state."""
        self.has_error = False
        if self._error_timeout:
            self._error_timeout.cancel()
            self._error_timeout = None

    def show_error(self, message):
        """Show error message."""
        self.status_text = message
        if self._error_timeout:
            self._error_timeout.cancel()
        self._error_timeout = Clock.schedule_once(lambda dt: self.clear_error(), 5)

    def on_pre_enter(self):
        """Called before screen is entered."""
        super().on_pre_enter()
        self._start_background_tasks()

    def on_leave(self):
        """Called when leaving the screen."""
        super().on_leave()
        if self._loading_timeout:
            self._loading_timeout.cancel()
        if self._error_timeout:
            self._error_timeout.cancel()

    def handle_client_update(self, update):
        """Handle client update."""
        if update.get('type') == 'saved_game':
            try:
                has_saved = update.get('has_saved_game', False)
                game_info = update.get('game_info')
                if has_saved and game_info:
                    self.validate_saved_game(game_info)
                    self.has_saved_game = True
                    self.saved_game_info = game_info
                else:
                    self.has_saved_game = False
                    self.saved_game_info = None
            except (ValidationError, StateError) as e:
                self.handle_error(str(e))

    def validate_game_state(self, state):
        """Validate game state."""
        if not isinstance(state, dict):
            raise ValidationError("Game state must be a dictionary")
        
        required_keys = ['players', 'current_round', 'scores']
        for key in required_keys:
            if key not in state:
                raise StateError(f"Missing required state key: {key}")
        
        return True 