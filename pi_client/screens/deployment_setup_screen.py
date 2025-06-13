from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, ListProperty, DictProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.clock import Clock
import logging
import os
import random
from .base_screen import BaseScreen, ValidationError, StateError, SyncError

logger = logging.getLogger(__name__)

Builder.load_file(os.path.join(os.path.dirname(__file__), "../widgets/rounded_button.kv"))
Builder.load_file(os.path.join(os.path.dirname(__file__), "deployment_setup_screen.kv"))

class DeploymentSetupScreen(BaseScreen):
    # Game state
    p1_roll = NumericProperty(0)
    p2_roll = NumericProperty(0)
    winner_id = NumericProperty(0)
    deployment_sequence = ListProperty([])
    current_role = StringProperty('')
    role_validation_error = StringProperty('')
    players = ListProperty([])
    roles = DictProperty({})
    rolls = DictProperty({})
    app = ObjectProperty(None)
    
    # Player names
    p1_name = StringProperty('Player 1')
    p2_name = StringProperty('Player 2')
    
    # Deployment properties
    p1_deployment = StringProperty('')
    p2_deployment = StringProperty('')
    is_loading = BooleanProperty(False)
    is_syncing = BooleanProperty(False)
    has_error = BooleanProperty(False)

    def __init__(self, **kwargs):
        logger.info("DeploymentSetupScreen: Initializing")
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.deployment_sequence = ["Player1", "Player2"]
        self.rolls = []
        if not self.children:
            self.add_widget(Label(text='DeploymentSetupScreen loaded (no KV)'))

    def on_enter(self):
        """Called when the screen is shown."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            self.ids.p1_name_label.text = self.app.game_state.get('p1_name', 'Player 1')
            self.ids.p2_name_label.text = self.app.game_state.get('p2_name', 'Player 2')
            self.reset_screen()
        except Exception as e:
            logger.error(f"Error in on_enter: {str(e)}")
            self.handle_roll_validation_error()

    def reset_screen(self, is_reroll=False):
        """Resets the screen to its initial state."""
        try:
            self.p1_roll = 0
            self.p2_roll = 0
            self.winner_id = 0
            self.p1_deployment = ''
            self.p2_deployment = ''
            self.ids.p1_roll_button.disabled = False
            self.ids.p2_roll_button.disabled = False
            self.ids.p1_choice_box.opacity = 0
            self.ids.p1_choice_box.disabled = True
            self.ids.p2_choice_box.opacity = 0
            self.ids.p2_choice_box.disabled = True
            self.ids.continue_button.disabled = True

            if not is_reroll:
                self.ids.p1_roll_label.text = ""
                self.ids.p2_roll_label.text = ""
                self.ids.status_label.text = "Players roll to determine Attacker/Defender."
            else:
                self.ids.status_label.text = "It's a tie! Re-roll."
        except Exception as e:
            logger.error(f"Error in reset_screen: {str(e)}")
            self.handle_roll_validation_error()

    def roll_die(self, player):
        """Handles the dice roll for a given player."""
        try:
            if player == 1 and self.p1_roll == 0:
                self.p1_roll = random.randint(1, 6)
                self.ids.p1_roll_label.text = str(self.p1_roll)
                self.ids.p1_roll_button.disabled = True
                self.add_roll("Player1", self.p1_roll)
            elif player == 2 and self.p2_roll == 0:
                self.p2_roll = random.randint(1, 6)
                self.ids.p2_roll_label.text = str(self.p2_roll)
                self.ids.p2_roll_button.disabled = True
                self.add_roll("Player2", self.p2_roll)

            if self.p1_roll > 0 and self.p2_roll > 0:
                self.determine_winner()
        except Exception as e:
            logger.error(f"Error in roll_die: {str(e)}")
            self.handle_roll_validation_error()

    def determine_winner(self):
        """Determines the winner of the roll-off."""
        try:
            if self.p1_roll > self.p2_roll:
                self.winner_id = 1
                self.ids.p1_choice_box.opacity = 1
                self.ids.p1_choice_box.disabled = False
                self.ids.status_label.text = f"{self.p1_name} won! Choose your role."
            elif self.p2_roll > self.p1_roll:
                self.winner_id = 2
                self.ids.p2_choice_box.opacity = 1
                self.ids.p2_choice_box.disabled = False
                self.ids.status_label.text = f"{self.p2_name} won! Choose your role."
            else:
                self.reset_screen(is_reroll=True)
        except Exception as e:
            logger.error(f"Error in determine_winner: {str(e)}")
            self.handle_roll_validation_error()

    def select_role(self, player, role):
        """Handles role selection for a player."""
        try:
            if player == self.winner_id:
                if player == 1:
                    self.p1_deployment = role
                    self.p2_deployment = 'Defender' if role == 'Attacker' else 'Attacker'
                else:
                    self.p2_deployment = role
                    self.p1_deployment = 'Defender' if role == 'Attacker' else 'Attacker'
                
                self.ids.p1_deployment_label.text = self.p1_deployment
                self.ids.p2_deployment_label.text = self.p2_deployment
                self.ids.continue_button.disabled = False
                self.ids.status_label.text = f"Role selected. Attacker: {self.p1_name if self.p1_deployment == 'Attacker' else self.p2_name}, Defender: {self.p1_name if self.p1_deployment == 'Defender' else self.p2_name}"
                self.proceed_to_initiative()
        except Exception as e:
            logger.error(f"Error in select_role: {str(e)}")
            self.handle_roll_validation_error()

    def roll_player1(self):
        """Handles Player 1's roll."""
        try:
            self.roll_die(1)
        except Exception as e:
            logger.error(f"Error in roll_player1: {str(e)}")
            self.handle_roll_validation_error()

    def roll_player2(self):
        """Handles Player 2's roll."""
        try:
            self.roll_die(2)
        except Exception as e:
            logger.error(f"Error in roll_player2: {str(e)}")
            self.handle_roll_validation_error()

    def validate_deployments(self):
        """Validates the deployment selections."""
        try:
            if not self.p1_deployment or not self.p2_deployment:
                return False
            if self.p1_deployment == self.p2_deployment:
                return False
            return True
        except Exception as e:
            logger.error(f"Error in validate_deployments: {str(e)}")
            return False

    def update_view_from_state(self):
        """Update view from state."""
        try:
            super().update_view_from_state()
            if not self.app:
                self.app = App.get_running_app()
            self.deployment_sequence = self.app.game_state.get('deployment_sequence', [])
            self.current_role = self.app.game_state.get('current_role', '')
            self.players = self.app.game_state.get('players', [])
            self.roles = self.app.game_state.get('roles', {})
            self.rolls = self.app.game_state.get('rolls', {})
            self.p1_deployment = self.app.game_state.get('p1_deployment', '')
            self.p2_deployment = self.app.game_state.get('p2_deployment', '')
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in update_view_from_state: {str(e)}")
            self.handle_roll_validation_error()

    def update_ui(self):
        """Updates the UI based on current state."""
        try:
            if self.validate_deployments():
                self.ids.continue_button.disabled = False
            else:
                self.ids.continue_button.disabled = True
        except Exception as e:
            logger.error(f"Error in update_ui: {str(e)}")
            self.handle_roll_validation_error()

    def proceed_to_initiative(self):
        """Proceed to the initiative screen."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            if self.validate_state(['attacker_name', 'defender_name']):
                self.manager.current = 'initiative'
            else:
                raise StateError("Missing required state for initiative screen")
        except Exception as e:
            logger.error(f"Error in proceed_to_initiative: {str(e)}")
            self.handle_roll_validation_error()

    def back_to_name_entry(self):
        """Return to the name entry screen."""
        try:
            self.manager.current = 'name_entry'
        except Exception as e:
            logger.error(f"Error in back_to_name_entry: {str(e)}")
            self.handle_roll_validation_error()

    def handle_client_update(self, update):
        """Handle client update."""
        try:
            if update['type'] == 'role':
                player = update['player']
                role = update['role']
                if self.validate_role(role):
                    self.assign_role(player, role)
            elif update['type'] == 'roles':
                roles = update['roles']
                for player, role in roles.items():
                    if self.validate_role(role):
                        self.assign_role(player, role)
            else:
                raise ValidationError("Invalid update type")
        except Exception as e:
            logger.error(f"Error in handle_client_update: {str(e)}")
            self.handle_roll_validation_error()

    def validate_role(self, role):
        """Validate role assignment."""
        try:
            if not role or not role.strip():
                raise ValidationError("Role cannot be empty")
            if role not in ['Attacker', 'Defender']:
                raise ValidationError("Invalid role")
            return True
        except Exception as e:
            logger.error(f"Error in validate_role: {str(e)}")
            return False

    def validate_roll(self, roll):
        """Validate deployment roll."""
        try:
            if not isinstance(roll, int) or roll < 1 or roll > 6:
                raise ValidationError("Invalid roll value")
            return True
        except Exception as e:
            logger.error(f"Error in validate_roll: {str(e)}")
            return False

    def validate_roll_sequence(self, player):
        """Validate a player's roll sequence."""
        try:
            if player not in self.rolls:
                return False
            rolls = self.rolls[player]
            if not isinstance(rolls, list):
                return False
            for roll in rolls:
                if not self.validate_roll(roll):
                    return False
            return True
        except Exception as e:
            logger.error(f"Error in validate_roll_sequence: {str(e)}")
            return False

    def add_roll(self, player, roll):
        """Add a roll to a player's sequence."""
        try:
            if self.validate_roll(roll):
                if player not in self.rolls:
                    self.rolls[player] = []
                self.rolls[player].append(roll)
                self.broadcast_state()
                return True
            return False
        except Exception as e:
            logger.error(f"Error in add_roll: {str(e)}")
            return False

    def handle_role_validation_error(self):
        """Handle role validation error."""
        try:
            self.has_error = True
            self.role_validation_error = "Invalid role selection"
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in handle_role_validation_error: {str(e)}")
            self.handle_roll_validation_error()

    def handle_roll_validation_error(self):
        """Handle roll validation error."""
        try:
            self.has_error = True
            self.ids.status_label.text = "Invalid roll detected"
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in handle_roll_validation_error: {str(e)}")
            self.show_error("Critical error in roll validation")

    def handle_sequence_validation_error(self):
        """Handle sequence validation error."""
        try:
            self.has_error = True
            self.ids.status_label.text = "Invalid deployment sequence"
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in handle_sequence_validation_error: {str(e)}")
            self.handle_roll_validation_error()

    def validate_state(self, required_keys):
        """Validate the current state has all required keys."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            for key in required_keys:
                if key not in self.app.game_state:
                    raise StateError(f"Missing required state key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error in validate_state: {str(e)}")
            return False

    def start_sync(self):
        """Start synchronization."""
        try:
            self.is_syncing = True
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in start_sync: {str(e)}")
            self.handle_roll_validation_error()

    def stop_sync(self):
        """Stop synchronization."""
        try:
            self.is_syncing = False
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in stop_sync: {str(e)}")
            self.handle_roll_validation_error()

    def validate_input(self, input_data, validation_rules):
        """Validate input."""
        try:
            for key, rule in validation_rules.items():
                if key not in input_data:
                    raise ValidationError(f"Missing required input: {key}")
                if not rule(input_data[key]):
                    raise ValidationError(f"Invalid input for {key}")
            return True
        except Exception as e:
            logger.error(f"Error in validate_input: {str(e)}")
            return False

    # New methods for deployment sequence management
    def generate_deployment_sequence(self):
        """Generate a new deployment sequence."""
        try:
            if not self.players:
                raise ValidationError("No players available for deployment sequence")
            
            # Randomly determine deployment order
            sequence = self.players.copy()
            random.shuffle(sequence)
            self.deployment_sequence = sequence
            
            # Update game state
            if self.app:
                self.app.game_state['deployment_sequence'] = sequence
            
            return sequence
        except Exception as e:
            logger.error(f"Error in generate_deployment_sequence: {str(e)}")
            self.handle_sequence_validation_error()
            return []

    def validate_deployment_sequence(self):
        """Validate the current deployment sequence."""
        try:
            if not self.deployment_sequence:
                return False
            
            if len(self.deployment_sequence) != len(self.players):
                return False
            
            # Check that all players are in the sequence
            for player in self.players:
                if player not in self.deployment_sequence:
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error in validate_deployment_sequence: {str(e)}")
            return False

    def update_deployment_sequence(self):
        """Update the deployment sequence based on current game state."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            
            current_sequence = self.app.game_state.get('deployment_sequence', [])
            if current_sequence != self.deployment_sequence:
                self.deployment_sequence = current_sequence
                self.update_ui()
        except Exception as e:
            logger.error(f"Error in update_deployment_sequence: {str(e)}")
            self.handle_sequence_validation_error()

    def reset_deployment_sequence(self):
        """Reset the deployment sequence."""
        try:
            self.deployment_sequence = []
            if self.app:
                self.app.game_state['deployment_sequence'] = []
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in reset_deployment_sequence: {str(e)}")
            self.handle_sequence_validation_error()

    def continue_to_initiative(self):
        """Alias for proceed_to_initiative to match KV file binding."""
        self.proceed_to_initiative()

    def assign_role(self, player, role):
        if not player or not role:
            self.show_error("role assignment error")
            return
        # Dummy logic for test compatibility
        self.roles[player] = role 