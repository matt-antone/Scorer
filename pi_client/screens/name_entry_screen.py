from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, DictProperty, ListProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.clock import Clock
import logging
import os
from .base_screen import BaseScreen, ValidationError, StateError, SyncError

logger = logging.getLogger(__name__)

Builder.load_file(os.path.join(os.path.dirname(__file__), "../widgets/rounded_button.kv"))
Builder.load_file(os.path.join(os.path.dirname(__file__), "name_entry_screen.kv"))

class NameEntryScreen(BaseScreen):
    """Screen for entering player names."""
    
    # Properties
    p1_name = StringProperty('')
    p2_name = StringProperty('')
    qr_code_valid = BooleanProperty(False)
    qr_code_error = StringProperty('')
    is_loading = BooleanProperty(False)
    is_syncing = BooleanProperty(False)
    has_error = BooleanProperty(False)
    app = ObjectProperty(None)
    players = ListProperty([])
    player_names = ListProperty([])
    qr_code = StringProperty('')
    name_validation = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.logger.info("NameEntryScreen: Initializing")
        self.app = App.get_running_app()
        self.players = []
        if not self.children:
            self.add_widget(Label(text='NameEntryScreen loaded (no KV)'))

    def on_enter(self):
        """Called when the screen is shown."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            self.reset_screen()
            self.update_view_from_state()
            # Always set player_names, qr_code, qr_code_valid, qr_code_error, and name_validation in game state
            self.app.game_state['player_names'] = [self.p1_name, self.p2_name]
            self.app.game_state['qr_code'] = self.qr_code
            self.app.game_state['qr_code_valid'] = self.qr_code_valid
            self.app.game_state['qr_code_error'] = self.qr_code_error
            self.app.game_state['name_validation'] = self.name_validation
        except Exception as e:
            logger.error(f"Error in on_enter: {str(e)}")
            self.handle_name_validation_error()

    def reset_screen(self):
        """Reset screen state."""
        try:
            self.p1_name = ''
            self.p2_name = ''
            self.qr_code_valid = False
            self.qr_code_error = ''
            self.is_loading = False
            self.is_syncing = False
            self.has_error = False
            self.players = []
            
            # Update UI
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in reset_screen: {str(e)}")
            self.handle_name_validation_error()

    def update_ui(self):
        """Update UI elements."""
        try:
            # Update input fields
            self.ids.p1_name_input.text = self.p1_name
            self.ids.p2_name_input.text = self.p2_name
            
            # Update continue button state
            self.ids.continue_button.disabled = not self.validate_inputs()
            
            # Update error label
            if self.qr_code_error:
                self.ids.error_label.text = self.qr_code_error
                self.ids.error_label.opacity = 1
            else:
                self.ids.error_label.opacity = 0
        except Exception as e:
            logger.error(f"Error in update_ui: {str(e)}")
            self.handle_name_validation_error()

    def validate_inputs(self):
        """Validate input fields."""
        try:
            if not self.p1_name or not self.p2_name:
                return False
            
            if not self.validate_name(self.p1_name) or not self.validate_name(self.p2_name):
                return False
            
            if self.p1_name == self.p2_name:
                self.qr_code_error = "Player names must be different"
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error in validate_inputs: {str(e)}")
            return False

    def validate_name(self, name):
        """Validate a player name."""
        try:
            if not name:
                return False
            
            if len(name) < 2 or len(name) > 20:
                self.qr_code_error = "Name must be between 2 and 20 characters"
                return False
            
            if not all(c.isalnum() or c.isspace() for c in name):
                self.qr_code_error = "Name can only contain letters, numbers, and spaces"
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error in validate_name: {str(e)}")
            return False

    def remove_player_name(self, player):
        """Remove a player's name."""
        try:
            if player == 'p1':
                self.p1_name = ''
                self.ids.p1_name_input.text = ''
            elif player == 'p2':
                self.p2_name = ''
                self.ids.p2_name_input.text = ''
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in remove_player_name: {str(e)}")
            self.handle_name_validation_error()

    def handle_qr_code_error(self):
        """Handle QR code error."""
        try:
            self.has_error = True
            self.qr_code_error = "Failed to generate QR code"
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in handle_qr_code_error: {str(e)}")
            self.handle_name_validation_error()

    def generate_qr_code(self, player_name):
        """Generate QR code for player name."""
        try:
            if not self.validate_name(player_name):
                raise ValidationError("Invalid player name")
            
            # TODO: Implement actual QR code generation
            # For now, just mark as valid
            self.qr_code_valid = True
            self.qr_code_error = ''
            self.update_ui()
            return True
        except Exception as e:
            self.handle_qr_code_error()
            return False

    def proceed_to_deployment(self):
        """Proceed to deployment setup screen."""
        try:
            if self.validate_inputs():
                if self.app:
                    self.app.game_state.update({
                        'p1_name': self.p1_name,
                        'p2_name': self.p2_name,
                        'player_names': [self.p1_name, self.p2_name]
                    })
                if self.manager:
                    self.manager.current = 'deployment_setup'
        except Exception as e:
            logger.error(f"Error in proceed_to_deployment: {str(e)}")
            self.handle_name_validation_error()

    def back_to_resume(self):
        """Return to resume game screen."""
        try:
            if self.manager:
                self.manager.current = 'resume'
        except Exception as e:
            logger.error(f"Error in back_to_resume: {str(e)}")
            self.handle_name_validation_error()

    def update_view_from_state(self):
        """Update view from state."""
        try:
            super().update_view_from_state()
            if not self.app:
                self.app = App.get_running_app()
            # Update player names
            self.p1_name = self.app.game_state.get('p1_name', '')
            self.p2_name = self.app.game_state.get('p2_name', '')
            self.player_names = [self.p1_name, self.p2_name]
            # Always set player_names, qr_code, qr_code_valid, qr_code_error, and name_validation in game state
            self.app.game_state['player_names'] = self.player_names
            self.app.game_state['qr_code'] = self.qr_code
            self.app.game_state['qr_code_valid'] = self.qr_code_valid
            self.app.game_state['qr_code_error'] = self.qr_code_error
            self.app.game_state['name_validation'] = self.name_validation
            # Update UI
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in update_view_from_state: {str(e)}")
            self.handle_name_validation_error()

    def handle_client_update(self, update):
        """Handle client update."""
        if update['type'] == 'player_name':
            player = update['player']
            name = update['name']
            if not self.validate_name(name):
                raise ValidationError("Invalid player name")
            if player == 'p1':
                self.p1_name = name
            elif player == 'p2':
                self.p2_name = name
            self.update_ui()
        else:
            raise ValidationError("Invalid update type")

    def handle_error(self, error):
        """Handle error."""
        try:
            self.show_error(str(error))
        except Exception as e:
            logger.error(f"Error in handle_error: {str(e)}")
            self.handle_name_validation_error()

    def handle_name_validation_error(self):
        """Handle name validation error."""
        try:
            self.show_error("Invalid player name")
        except Exception as e:
            logger.error(f"Error in handle_name_validation_error: {str(e)}")
            self.show_error("Critical error in name validation")

    def handle_duplicate_name_error(self):
        """Handle duplicate name error."""
        try:
            self.show_error("Player names must be different")
        except Exception as e:
            logger.error(f"Error in handle_duplicate_name_error: {str(e)}")
            self.handle_name_validation_error()

    def handle_state_error(self):
        """Handle state error."""
        try:
            self.show_error("Game state error")
        except Exception as e:
            logger.error(f"Error in handle_state_error: {str(e)}")
            self.handle_name_validation_error()

    def validate_state(self, required_keys):
        """Validate the current state has all required keys."""
        if not self.app:
            self.app = App.get_running_app()
        for key in required_keys:
            if key not in self.app.game_state:
                raise StateError(f"Missing required state key: {key}")
        return True

    def start_sync(self):
        """Start synchronization."""
        try:
            self.is_syncing = True
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in start_sync: {str(e)}")
            self.handle_name_validation_error()

    def stop_sync(self):
        """Stop synchronization."""
        try:
            self.is_syncing = False
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in stop_sync: {str(e)}")
            self.handle_name_validation_error()

    def validate_input(self, input_data, validation_rules):
        """Validate input."""
        for key, rule in validation_rules.items():
            if key not in input_data:
                raise ValidationError(f"Missing required input: {key}")
            if not rule(input_data[key]):
                raise ValidationError(f"Invalid input for {key}")
        return True 