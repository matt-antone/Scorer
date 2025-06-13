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
    """Screen for choosing to resume or start a new game."""
    
    # Properties
    has_saved_game = BooleanProperty(False)
    saved_game_info = ObjectProperty(None)  # Changed from StringProperty to ObjectProperty
    save_file_path = StringProperty('')
    save_file_valid = BooleanProperty(False)
    save_file_error = StringProperty('')
    game_resumed = BooleanProperty(False)  # Added missing property
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.logger.info("ResumeOrNewScreen: Initializing")
        self.save_file_path = os.path.join(os.path.expanduser('~'), '.scorer', 'saved_game.json')
        self.detect_save_file()
        kv_path = os.path.join(os.path.dirname(__file__), 'resume_or_new_screen.kv')
        Builder.load_file(kv_path)
        if not self.children:
            self.add_widget(Label(text='ResumeOrNewScreen loaded (no KV)'))

    def detect_save_file(self):
        """Detect if a save file exists and is valid."""
        try:
            if os.path.exists(self.save_file_path):
                with open(self.save_file_path, 'r') as f:
                    saved_game = json.load(f)
                if self.validate_saved_game(saved_game):
                    self.has_saved_game = True
                    self.saved_game_info = saved_game
                    self.save_file_valid = True
                    self.save_file_error = ''
                else:
                    self.save_file_valid = False
                    self.save_file_error = 'Invalid save file format'
            else:
                self.has_saved_game = False
                self.saved_game_info = None
                self.save_file_valid = False
                self.save_file_error = ''
        except Exception as e:
            self.logger.error(f"Error detecting save file: {str(e)}")
            self.save_file_valid = False
            self.save_file_error = str(e)

    def handle_save_file_error(self):
        """Handle save file error."""
        self.show_error(f"Save file error: {self.save_file_error}")

    def handle_validation_error(self):
        """Handle validation error."""
        self.show_error("Invalid game state format")
        self.save_file_valid = False
        self.save_file_error = "Invalid game state format"

    def handle_client_update(self, update):
        """Handle client update."""
        if update.get('type') == 'game_state':
            try:
                if self.validate_saved_game(update.get('state', {})):
                    self.has_saved_game = True
                    self.saved_game_info = update['state']
                    self.save_file_valid = True
                    self.save_file_error = ''
                else:
                    self.handle_validation_error()
            except (ValidationError, StateError) as e:
                self.logger.error(f"Validation error: {str(e)}")
                self.handle_validation_error()

    def broadcast_state(self):
        """Broadcast current state to all clients."""
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            app.game_state['has_saved_game'] = self.has_saved_game
            app.game_state['saved_game_info'] = self.saved_game_info
            if hasattr(app, 'broadcast_state'):
                app.broadcast_state()

    def resume_game(self):
        """Resume the saved game."""
        if self.has_saved_game and self.save_file_valid:
            app = App.get_running_app()
            if app:
                try:
                    app.load_game_state(self.saved_game_info)
                    self.game_resumed = True
                    app.root.current = 'scoreboard'
                except Exception as e:
                    self.logger.error(f"Failed to resume game: {str(e)}")
                    self.handle_state_error()

    def start_new_game(self):
        """Start a new game."""
        logging.info("Starting new game")
        app = App.get_running_app()
        if app:
            try:
                if hasattr(app, 'initialize_game_state'):
                    app.initialize_game_state()
                app.root.current = 'name_entry'
            except Exception as e:
                self.logger.error(f"Failed to start new game: {str(e)}")
                self.handle_state_error()

    def validate_saved_game(self, saved_game):
        """Validate saved game data."""
        if not isinstance(saved_game, dict):
            raise ValidationError("Saved game must be a dictionary")
        
        required_keys = ['players', 'current_round', 'scores']
        for key in required_keys:
            if key not in saved_game:
                raise ValidationError(f"Missing required saved game key: {key}")
        
        if not isinstance(saved_game['players'], list) or len(saved_game['players']) != 2:
            raise ValidationError("Players must be a list of exactly 2 players")
        
        if not isinstance(saved_game['current_round'], int) or saved_game['current_round'] < 1:
            raise ValidationError("Current round must be a positive integer")
        
        if not isinstance(saved_game['scores'], dict):
            raise ValidationError("Scores must be a dictionary")
        
        return True

    def update_view_from_state(self):
        """Update view from state."""
        super().update_view_from_state()
        self.has_saved_game = self.app.game_state.get('has_saved_game', False)
        if self.has_saved_game:
            self.saved_game_info = self.app.game_state.get('saved_game_info')
            self.save_file_valid = True
            self.save_file_error = ''

    def handle_state_error(self):
        """Handle state error."""
        self.show_error("Invalid game state")
        self.save_file_valid = False
        self.save_file_error = "Invalid game state" 