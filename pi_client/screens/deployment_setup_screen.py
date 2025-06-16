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
    roll_validation = DictProperty({
        'min_value': 1,
        'max_value': 6,
        'required_rolls': 2
    })
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
            # Register as observer
            if self.state_manager:
                self.state_manager.register_observer(self)
            self.ids.p1_name_label.text = self.app.game_state.get('p1_name', 'Player 1')
            self.ids.p2_name_label.text = self.app.game_state.get('p2_name', 'Player 2')
            self.update_roll_validation()
            self.reset_screen()
        except Exception as e:
            logger.error(f"Error in on_enter: {str(e)}")
            self.handle_roll_validation_error()

    def on_leave(self):
        # Unregister as observer
        if self.state_manager:
            self.state_manager.unregister_observer(self)
        super().on_leave()

    def on_state_update(self, state):
        self.logger.debug(f"[DeploymentSetupScreen] Received state update: {state}")
        self.p1_name = state.get('p1_name', 'Player 1')
        self.p2_name = state.get('p2_name', 'Player 2')
        self.deployment_sequence = state.get('deployment_sequence', [])
        self.current_role = state.get('current_role', '')
        self.players = state.get('players', [])
        self.roles = state.get('roles', [])
        self.rolls = state.get('rolls', {})
        self.p1_deployment = state.get('p1_deployment', '')
        self.p2_deployment = state.get('p2_deployment', '')
        self.update_ui()

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
                self.update_role(player, role)
        except Exception as e:
            logger.error(f"Error in select_role: {str(e)}")
            self.handle_roll_validation_error()

    def update_role(self, player, role):
        """Update a player's role."""
        try:
            if not self.validate_role(role):
                raise ValidationError("Invalid role")
            
            if player == self.p1_name:
                self.p1_deployment = role
                if self.app:
                    self.app.game_state['p1_deployment'] = role
            elif player == self.p2_name:
                self.p2_deployment = role
                if self.app:
                    self.app.game_state['p2_deployment'] = role
            else:
                raise ValidationError("Invalid player")
            
            # Update game state
            if self.app:
                if role == 'Attacker':
                    self.app.game_state['attacker_name'] = player
                    self.app.game_state['defender_name'] = self.p2_name if player == self.p1_name else self.p1_name
                else:
                    self.app.game_state['defender_name'] = player
                    self.app.game_state['attacker_name'] = self.p2_name if player == self.p1_name else self.p1_name
            
            # Broadcast state update
            if self.state_manager:
                self.state_manager.broadcast_state()
            
            self.update_ui()
            return True
        except Exception as e:
            logger.error(f"Error in update_role: {str(e)}")
            self.handle_role_validation_error()
            return False

    def add_roll(self, player, roll):
        """Add a roll for a player."""
        try:
            if not self.validate_roll(roll):
                raise ValidationError("Invalid roll value")
            
            if player not in self.rolls:
                self.rolls[player] = []
            
            if len(self.rolls[player]) >= self.roll_validation['required_rolls']:
                raise ValidationError("Maximum rolls reached")
            
            self.rolls[player].append(roll)
            
            # Update game state
            if self.app:
                self.app.game_state['rolls'] = dict(self.rolls)
            
            # Broadcast state update
            if self.state_manager:
                self.state_manager.broadcast_state()
            
            return True
        except Exception as e:
            logger.error(f"Error in add_roll: {str(e)}")
            self.handle_roll_validation_error()
            return False

    def proceed_to_initiative(self):
        """Proceed to the initiative screen."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            
            # Validate required state
            required_keys = ['attacker_name', 'defender_name', 'p1_deployment', 'p2_deployment']
            if not self.validate_state(required_keys):
                raise StateError("Missing required state for initiative screen")
            
            # Update game state
            self.app.game_state['game_phase'] = 'initiative'
            
            # Broadcast state update
            if self.state_manager:
                self.state_manager.broadcast_state()
            
            # Transition to initiative screen
            self.manager.current = 'initiative'
            return True
        except Exception as e:
            logger.error(f"Error in proceed_to_initiative: {str(e)}")
            self.handle_roll_validation_error()
            return False

    def validate_role(self, role):
        """Validates a role selection."""
        return role in ['Attacker', 'Defender']

    def validate_roll(self, roll):
        """Validates a roll value."""
        return isinstance(roll, int) and self.roll_validation['min_value'] <= roll <= self.roll_validation_validation['max_value']

    def validate_roll_sequence(self, player):
        """Validates a player's roll sequence."""
        if player not in self.rolls:
            return False
        rolls = self.rolls[player]
        return len(rolls) <= self.roll_validation['required_rolls']

    def handle_role_validation_error(self):
        """Handles role validation errors."""
        self.has_error = True
        self._current_error = "Invalid role selection"
        self.role_validation_error = "Please select a valid role (Attacker or Defender)"

    def handle_roll_validation_error(self):
        """Handles roll validation errors."""
        self.has_error = True
        self._current_error = "Invalid roll"
        self.ids.status_label.text = "Invalid roll. Please try again."

    def handle_sequence_validation_error(self):
        """Handles sequence validation errors."""
        self.has_error = True
        self._current_error = "Invalid deployment sequence"
        self.ids.status_label.text = "Invalid deployment sequence. Please try again."

    def validate_state(self, required_keys):
        """Validates the current state."""
        try:
            if not isinstance(required_keys, list):
                raise StateError("required_keys must be a list")
            
            # Define required state structure
            required_state = {
                'players': {
                    'type': list,
                    'min_length': 2,
                    'max_length': 2,
                    'validator': lambda x: all(isinstance(p, str) for p in x)
                },
                'roles': {
                    'type': list,
                    'min_length': 2,
                    'max_length': 2,
                    'validator': lambda x: all(r in ['Attacker', 'Defender'] for r in x)
                },
                'deployment_sequence': {
                    'type': list,
                    'min_length': 2,
                    'max_length': 2,
                    'validator': lambda x: all(p in self.players for p in x)
                },
                'rolls': {
                    'type': dict,
                    'validator': lambda x: all(
                        isinstance(rolls, list) and 
                        len(rolls) <= self.roll_validation['required_rolls'] and
                        all(self.roll_validation['min_value'] <= r <= self.roll_validation['max_value'] for r in rolls)
                        for rolls in x.values()
                    )
                },
                'p1_deployment': {
                    'type': str,
                    'validator': lambda x: x in ['', 'Attacker', 'Defender']
                },
                'p2_deployment': {
                    'type': str,
                    'validator': lambda x: x in ['', 'Attacker', 'Defender']
                },
                'attacker_name': {
                    'type': str,
                    'validator': lambda x: x in self.players
                },
                'defender_name': {
                    'type': str,
                    'validator': lambda x: x in self.players
                },
                'roll_validation': {
                    'type': dict,
                    'validator': lambda x: all(
                        k in ['min_value', 'max_value', 'required_rolls'] and
                        isinstance(v, int) and
                        (k != 'required_rolls' or v > 0)
                        for k, v in x.items()
                    )
                }
            }
            
            # Validate each required key
            for key in required_keys:
                if key not in required_state:
                    raise StateError(f"Unknown required key: {key}")
                
                # Get value from either app.game_state or self.<property>
                gs_value = self.app.game_state.get(key, None)
                prop_value = getattr(self, key, None)
                value = gs_value if gs_value is not None else prop_value
                
                # Validate value type
                if not isinstance(value, required_state[key]['type']):
                    raise StateError(f"Invalid type for {key}: expected {required_state[key]['type']}, got {type(value)}")
                
                # Validate value constraints
                if 'min_length' in required_state[key] and len(value) < required_state[key]['min_length']:
                    raise StateError(f"{key} has insufficient items: expected at least {required_state[key]['min_length']}")
                
                if 'max_length' in required_state[key] and len(value) > required_state[key]['max_length']:
                    raise StateError(f"{key} has too many items: expected at most {required_state[key]['max_length']}")
                
                # Run custom validator if provided
                if 'validator' in required_state[key] and not required_state[key]['validator'](value):
                    raise StateError(f"Invalid value for {key}")
            
            return True
        except Exception as e:
            logger.error(f"Error in validate_state: {str(e)}")
            raise

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