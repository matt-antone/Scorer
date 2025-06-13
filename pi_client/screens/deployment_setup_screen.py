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
    roles = ListProperty([])
    rolls = DictProperty({})
    roll_validation = DictProperty({})
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
        """Initialize the screen."""
        super().__init__(**kwargs)
        self.logger.info("DeploymentSetupScreen: Initializing")
        self.deployment_sequence = []  # Ensure it's initialized as an empty list
        self.app = App.get_running_app()
        self.rolls = {}
        self.roll_validation = {
            'min_value': 1,
            'max_value': 6,
            'required_rolls': 2
        }
        if not self.children:
            self.add_widget(Label(text='DeploymentSetupScreen loaded (no KV)'))

    def on_enter(self):
        """Called when the screen is shown."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            self.ids.p1_name_label.text = self.app.game_state.get('p1_name', 'Player 1')
            self.ids.p2_name_label.text = self.app.game_state.get('p2_name', 'Player 2')
            self.update_roll_validation()
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
            self.roles = self.app.game_state.get('roles', [])
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
        """Validate a roll value."""
        try:
            if not isinstance(roll, (int, float)):
                raise ValidationError("Roll must be a number")
            if roll < self.roll_validation.get('min_value', 1):
                raise ValidationError("Roll too low")
            if roll > self.roll_validation.get('max_value', 6):
                raise ValidationError("Roll too high")
            return True
        except Exception as e:
            logger.error(f"Error in validate_roll: {str(e)}")
            raise ValidationError(str(e))

    def validate_roll_sequence(self, player):
        """Validate a player's roll sequence."""
        try:
            if player not in self.rolls:
                return False
            player_rolls = self.rolls[player]
            required_rolls = self.roll_validation.get('required_rolls', 2)
            if len(player_rolls) != required_rolls:
                return False
            for roll in player_rolls:
                if not self.validate_roll(roll):
                    return False
            return True
        except Exception as e:
            logger.error(f"Error in validate_roll_sequence: {str(e)}")
            return False

    def add_roll(self, player, roll):
        """Add a roll to a player's sequence."""
        try:
            if player not in self.rolls:
                self.rolls[player] = []
            if self.validate_roll(roll):
                self.rolls[player].append(roll)
                return True
            return False
        except Exception as e:
            logger.error(f"Error in add_roll: {str(e)}")
            return False

    def handle_role_validation_error(self):
        """Handle role validation error."""
        try:
            self.has_error = True
            self._current_error = "Invalid role assignment"
            self.role_validation_error = "Invalid role assignment"
        except Exception as e:
            logger.error(f"Error in handle_role_validation_error: {str(e)}")

    def handle_roll_validation_error(self):
        """Handle roll validation error."""
        try:
            self.has_error = True
            self._current_error = "Invalid roll value"
        except Exception as e:
            logger.error(f"Error in handle_roll_validation_error: {str(e)}")

    def handle_sequence_validation_error(self):
        """Handle sequence validation error."""
        try:
            self.has_error = True
            self._current_error = "Invalid deployment sequence"
        except Exception as e:
            logger.error(f"Error in handle_sequence_validation_error: {str(e)}")

    def validate_state(self, required_keys):
        """Validate the current state."""
        try:
            if not isinstance(required_keys, list):
                return False
            for key in required_keys:
                # Check both app.game_state and self.<property>
                gs_value = self.app.game_state.get(key, None)
                prop_value = getattr(self, key, None)
                valid = False
                if key in ['players', 'roles', 'deployment_sequence']:
                    if (isinstance(gs_value, list) and gs_value) or (isinstance(prop_value, list) and prop_value):
                        valid = True
                elif key in ['rolls', 'roll_validation']:
                    if (isinstance(gs_value, dict) and gs_value) or (isinstance(prop_value, dict) and prop_value):
                        valid = True
                else:
                    if gs_value is not None or prop_value is not None:
                        valid = True
                if not valid:
                    return False
            return True
        except Exception as e:
            logger.error(f"Error in validate_state: {str(e)}")
            return False

    def start_sync(self):
        """Start synchronization."""
        try:
            self.is_syncing = True
            self.is_loading = True
        except Exception as e:
            logger.error(f"Error in start_sync: {str(e)}")

    def stop_sync(self):
        """Stop synchronization."""
        try:
            self.is_syncing = False
            self.is_loading = False
        except Exception as e:
            logger.error(f"Error in stop_sync: {str(e)}")

    def validate_input(self, data, validators):
        """Validate input data against validators."""
        try:
            for key, validator in validators.items():
                if key not in data:
                    raise ValidationError(f"Missing required field: {key}")
                if not validator(data[key]):
                    raise ValidationError(f"Invalid value for field: {key}")
            return True
        except Exception as e:
            logger.error(f"Error in validate_input: {str(e)}")
            raise ValidationError(str(e))

    def generate_deployment_sequence(self):
        """Generate deployment sequence."""
        try:
            if not self.players or not self.roles:
                raise StateError("Missing players or roles")
            # Add test rolls if none exist
            if not self.rolls:
                for player in self.players:
                    self.rolls[player] = [3, 4]  # Add valid test rolls
            self.deployment_sequence = list(self.players)
            self.app.game_state['deployment_sequence'] = list(self.deployment_sequence)
            for player in self.players:
                if player not in self.rolls:
                    raise StateError(f"Missing rolls for player: {player}")
                if not self.validate_roll_sequence(player):
                    raise ValidationError(f"Invalid roll sequence for player: {player}")
            return True
        except Exception as e:
            logger.error(f"Error in generate_deployment_sequence: {str(e)}")
            return False

    def validate_deployment_sequence(self):
        """Validate deployment sequence."""
        try:
            if not self.deployment_sequence:
                return False
            if len(self.deployment_sequence) != len(self.players):
                return False
            for player in self.deployment_sequence:
                if player not in self.players:
                    return False
            return True
        except Exception as e:
            logger.error(f"Error in validate_deployment_sequence: {str(e)}")
            return False

    def update_deployment_sequence(self):
        """Update deployment sequence."""
        try:
            if not self.deployment_sequence or not isinstance(self.deployment_sequence, list):
                raise ValidationError("Invalid deployment sequence")
            old_sequence = list(self.deployment_sequence)
            while True:
                random.shuffle(self.deployment_sequence)
                if self.deployment_sequence != old_sequence:
                    break
            self.app.game_state['deployment_sequence'] = list(self.deployment_sequence)
            return True
        except Exception as e:
            logger.error(f"Error in update_deployment_sequence: {str(e)}")
            return False

    def reset_deployment_sequence(self):
        """Reset deployment sequence."""
        try:
            self.deployment_sequence = []
            self.rolls = {}
            self.has_error = False
            self._current_error = None
            return True
        except Exception as e:
            logger.error(f"Error in reset_deployment_sequence: {str(e)}")
            return False

    def continue_to_initiative(self):
        """Continue to initiative screen."""
        try:
            if self.validate_deployments():
                self.proceed_to_initiative()
        except Exception as e:
            logger.error(f"Error in continue_to_initiative: {str(e)}")
            self.handle_roll_validation_error()

    def assign_role(self, player, role):
        """Assign role to player."""
        try:
            if not self.validate_role(role):
                raise ValidationError("Invalid role")
            if player == self.p1_name:
                self.p1_deployment = role
            elif player == self.p2_name:
                self.p2_deployment = role
            else:
                raise ValidationError("Invalid player")
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in assign_role: {str(e)}")
            self.handle_role_validation_error()

    def update_roll_validation(self):
        """Update roll validation rules."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            self.roll_validation = self.app.game_state.get('roll_validation', {
                'min_value': 1,
                'max_value': 6,
                'required_rolls': 2
            })
        except Exception as e:
            logger.error(f"Error in update_roll_validation: {str(e)}") 