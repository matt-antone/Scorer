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
    
    # State management properties
    scores = DictProperty({})
    final_scores_text = StringProperty('')

    def __init__(self, **kwargs):
        """Initialize the screen with comprehensive state management."""
        super().__init__(**kwargs)
        self.logger.info("DeploymentSetupScreen: Initializing with enhanced state management")
        self.deployment_sequence = []
        self.app = App.get_running_app()
        self.rolls = {}
        self.roll_validation = {
            'min_value': 1,
            'max_value': 6,
            'required_rolls': 2
        }
        self.scores = {}
        self.final_scores_text = ''
        
        # Initialize state validation
        self._validate_initial_state()
        
        if not self.children:
            self.add_widget(Label(text='DeploymentSetupScreen loaded (no KV)'))

    def _validate_initial_state(self):
        """Validate initial state and set up required properties."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            
            # Ensure required state properties exist
            if not hasattr(self.app, 'game_state'):
                self.app.game_state = {}
            
            # Initialize required state keys
            required_keys = ['p1_name', 'p2_name', 'rolls', 'deployment_sequence']
            for key in required_keys:
                if key not in self.app.game_state:
                    if key == 'rolls':
                        self.app.game_state[key] = {}
                    elif key == 'deployment_sequence':
                        self.app.game_state[key] = []
                    else:
                        self.app.game_state[key] = ''
            
            self.logger.debug("Initial state validation completed")
        except Exception as e:
            self.logger.error(f"Error in initial state validation: {str(e)}")
            self.handle_error(e)

    def on_enter(self):
        """Enhanced screen entry with comprehensive state management."""
        try:
            self.logger.info("DeploymentSetupScreen: Entering with state management")
            
            # Register as observer for state updates
            if self.state_manager:
                self.state_manager.register_observer(self)
                self.logger.debug("Registered as state observer")
            
            # Update UI from current state
            self.update_view_from_state()
            
            # Update player names from game state
            self.ids.p1_name_label.text = self.app.game_state.get('p1_name', 'Player 1')
            self.ids.p2_name_label.text = self.app.game_state.get('p2_name', 'Player 2')
            
            # Update roll validation
            self.update_roll_validation()
            
            # Reset screen to initial state
            self.reset_screen()
            
            # Broadcast current state
            self.broadcast_state()
            
            self.logger.info("DeploymentSetupScreen: Successfully entered")
        except Exception as e:
            self.logger.error(f"Error in on_enter: {str(e)}")
            self.handle_error(e)

    def on_leave(self):
        """Enhanced screen exit with proper cleanup."""
        try:
            self.logger.info("DeploymentSetupScreen: Leaving with cleanup")
            
            # Unregister as observer
            if self.state_manager:
                self.state_manager.unregister_observer(self)
                self.logger.debug("Unregistered as state observer")
            
            # Stop any ongoing operations
            self.stop_sync()
            
            # Clear any pending operations
            self.clear_error()
            
            super().on_leave()
            self.logger.info("DeploymentSetupScreen: Successfully left")
        except Exception as e:
            self.logger.error(f"Error in on_leave: {str(e)}")

    def on_state_update(self, state):
        """Enhanced state update handler with comprehensive validation."""
        try:
            self.logger.debug(f"[DeploymentSetupScreen] Received state update: {state}")
            
            # Validate incoming state
            if not self.validate_incoming_state(state):
                raise StateError("Invalid incoming state")
            
            # Update local properties from state
            self.p1_name = state.get('p1_name', 'Player 1')
            self.p2_name = state.get('p2_name', 'Player 2')
            self.deployment_sequence = state.get('deployment_sequence', [])
            self.current_role = state.get('current_role', '')
            self.players = state.get('players', [])
            self.roles = state.get('roles', [])
            self.rolls = state.get('rolls', {})
            self.p1_deployment = state.get('p1_deployment', '')
            self.p2_deployment = state.get('p2_deployment', '')
            self.scores = state.get('scores', {})
            self.final_scores_text = state.get('final_scores_text', '')
            
            # Update UI to reflect new state
            self.update_ui()
            
            self.logger.debug("State update processed successfully")
        except Exception as e:
            self.logger.error(f"Error in on_state_update: {str(e)}")
            self.handle_error(e)

    def validate_incoming_state(self, state):
        """Validate incoming state updates."""
        try:
            if not isinstance(state, dict):
                return False
            
            # Check required keys
            required_keys = ['p1_name', 'p2_name', 'rolls', 'deployment_sequence']
            for key in required_keys:
                if key not in state:
                    self.logger.warning(f"Missing required key in state: {key}")
                    return False
            
            # Validate rolls structure
            if not isinstance(state.get('rolls', {}), dict):
                return False
            
            # Validate deployment sequence
            if not isinstance(state.get('deployment_sequence', []), list):
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error validating incoming state: {str(e)}")
            return False

    def reset_screen(self, is_reroll=False):
        """Enhanced screen reset with state management."""
        try:
            self.logger.debug("Resetting screen with state management")
            
            # Reset local properties
            self.p1_roll = 0
            self.p2_roll = 0
            self.winner_id = 0
            self.p1_deployment = ''
            self.p2_deployment = ''
            
            # Reset UI elements
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
            
            # Update game state
            if self.app:
                self.app.game_state['p1_roll'] = 0
                self.app.game_state['p2_roll'] = 0
                self.app.game_state['winner_id'] = 0
                self.app.game_state['p1_deployment'] = ''
                self.app.game_state['p2_deployment'] = ''
            
            # Broadcast state update
            self.broadcast_state()
            
            self.logger.debug("Screen reset completed")
        except Exception as e:
            self.logger.error(f"Error in reset_screen: {str(e)}")
            self.handle_error(e)

    def roll_die(self, player):
        """Enhanced dice roll with comprehensive validation and state management."""
        try:
            self.logger.debug(f"Rolling die for player {player}")
            
            # Validate player
            if player not in [1, 2]:
            
                raise ValidationError(f"Invalid player: {player}")
            
            # Check if player has already rolled
            if player == 1 and self.p1_roll != 0:
                raise ValidationError("Player 1 has already rolled")
            elif player == 2 and self.p2_roll != 0:
                raise ValidationError("Player 2 has already rolled")
            
            # Generate roll
            roll_value = random.randint(1, 6)
            
            # Validate roll
            if not self.validate_roll(roll_value):
                raise ValidationError(f"Invalid roll value: {roll_value}")
            
            # Update local state
            if player == 1:
                self.p1_roll = roll_value
                self.ids.p1_roll_label.text = str(self.p1_roll)
                self.ids.p1_roll_button.disabled = True
                self.add_roll("Player1", self.p1_roll)
            elif player == 2:
                self.p2_roll = roll_value
                self.ids.p2_roll_label.text = str(self.p2_roll)
                self.ids.p2_roll_button.disabled = True
                self.add_roll("Player2", self.p2_roll)

            # Check if both players have rolled
            if self.p1_roll > 0 and self.p2_roll > 0:
                self.determine_winner()
            
            # Broadcast state update
            self.broadcast_state()
            
            self.logger.debug(f"Roll completed for player {player}: {roll_value}")
        except Exception as e:
            self.logger.error(f"Error in roll_die: {str(e)}")
            self.handle_error(e)

    def determine_winner(self):
        """Enhanced winner determination with state management."""
        try:
            self.logger.debug("Determining winner")
            
            # Validate rolls exist
            if self.p1_roll == 0 or self.p2_roll == 0:
                raise StateError("Both players must roll before determining winner")
            
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
                # Tie - reset for re-roll
                self.reset_screen(is_reroll=True)
                return
            
            # Update game state
            if self.app:
                self.app.game_state['winner_id'] = self.winner_id
            
            # Broadcast state update
            self.broadcast_state()
            
            self.logger.debug(f"Winner determined: Player {self.winner_id}")
        except Exception as e:
            self.logger.error(f"Error in determine_winner: {str(e)}")
            self.handle_error(e)

    def select_role(self, player, role):
        """Enhanced role selection with comprehensive validation."""
        try:
            self.logger.debug(f"Selecting role for player {player}: {role}")
            
            # Validate player is winner
            if player != self.winner_id:
                raise ValidationError("Only the winner can select a role")
            
            # Validate role
            if not self.validate_role(role):
                raise ValidationError(f"Invalid role: {role}")
            
            # Update deployments
            if player == 1:
                self.p1_deployment = role
                self.p2_deployment = 'Defender' if role == 'Attacker' else 'Attacker'
            else:
                self.p2_deployment = role
                self.p1_deployment = 'Defender' if role == 'Attacker' else 'Attacker'
            
            # Update UI
            self.ids.p1_deployment_label.text = self.p1_deployment
            self.ids.p2_deployment_label.text = self.p2_deployment
            self.ids.continue_button.disabled = False
            
            # Update status
            attacker_name = self.p1_name if self.p1_deployment == 'Attacker' else self.p2_name
            defender_name = self.p1_name if self.p1_deployment == 'Defender' else self.p2_name
            self.ids.status_label.text = f"Role selected. Attacker: {attacker_name}, Defender: {defender_name}"
            
            # Update role in state
            self.update_role(player, role)
            
            # Broadcast state update
            self.broadcast_state()
            
            self.logger.debug(f"Role selection completed: Player {player} -> {role}")
        except Exception as e:
            self.logger.error(f"Error in select_role: {str(e)}")
            self.handle_error(e)

    def update_role(self, player, role):
        """Enhanced role update with comprehensive validation and state management."""
        try:
            self.logger.debug(f"Updating role for player {player}: {role}")
            
            # Validate role
            if not self.validate_role(role):
                raise ValidationError("Invalid role")
            
            # Update local state
            if player == 1:
                self.p1_deployment = role
                if self.app:
                    self.app.game_state['p1_deployment'] = role
            elif player == 2:
                self.p2_deployment = role
                if self.app:
                    self.app.game_state['p2_deployment'] = role
            else:
                raise ValidationError("Invalid player")
            
            # Update game state with attacker/defender names
            if self.app:
                if role == 'Attacker':
                    self.app.game_state['attacker_name'] = self.p1_name if player == 1 else self.p2_name
                    self.app.game_state['defender_name'] = self.p2_name if player == 1 else self.p1_name
                else:
                    self.app.game_state['defender_name'] = self.p1_name if player == 1 else self.p2_name
                    self.app.game_state['attacker_name'] = self.p2_name if player == 1 else self.p1_name
            
            # Broadcast state update
            self.broadcast_state()
            
            # Update UI
            self.update_ui()
            
            self.logger.debug(f"Role update completed: Player {player} -> {role}")
            return True
        except Exception as e:
            self.logger.error(f"Error in update_role: {str(e)}")
            self.handle_error(e)
            return False

    def add_roll(self, player, roll):
        """Enhanced roll addition with comprehensive validation."""
        try:
            self.logger.debug(f"Adding roll for {player}: {roll}")
            
            # Validate roll
            if not self.validate_roll(roll):
                raise ValidationError("Invalid roll value")
            
            # Initialize player rolls if needed
            if player not in self.rolls:
                self.rolls[player] = []
            
            # Check roll limit
            if len(self.rolls[player]) >= self.roll_validation['required_rolls']:
                raise ValidationError("Maximum rolls reached")
            
            # Add roll
            self.rolls[player].append(roll)
            
            # Update game state
            if self.app:
                self.app.game_state['rolls'] = dict(self.rolls)
            
            # Broadcast state update
            self.broadcast_state()
            
            self.logger.debug(f"Roll added successfully: {player} -> {roll}")
            return True
        except Exception as e:
            self.logger.error(f"Error in add_roll: {str(e)}")
            self.handle_error(e)
            return False

    def proceed_to_initiative(self):
        """Enhanced initiative transition with comprehensive validation."""
        try:
            self.logger.info("Proceeding to initiative screen")
            
            if not self.app:
                self.app = App.get_running_app()
            
            # Validate required state
            required_keys = ['attacker_name', 'defender_name', 'p1_deployment', 'p2_deployment']
            if not self.validate_state(required_keys):
                raise StateError("Missing required state for initiative screen")
            
            # Validate deployments are set
            if not self.p1_deployment or not self.p2_deployment:
                raise StateError("Both players must have deployments set")
            
            # Update game state
            self.app.game_state['game_phase'] = 'initiative'
            self.app.game_state['current_screen'] = 'initiative'
            
            # Broadcast state update
            self.broadcast_state()
            
            # Transition to initiative screen
            self.manager.current = 'initiative'
            
            self.logger.info("Successfully transitioned to initiative screen")
            return True
        except Exception as e:
            self.logger.error(f"Error in proceed_to_initiative: {str(e)}")
            self.handle_error(e)
            return False

    def validate_role(self, role):
        """Enhanced role validation."""
        try:
            valid_roles = ['Attacker', 'Defender']
            if role not in valid_roles:
                self.logger.warning(f"Invalid role: {role}")
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error in validate_role: {str(e)}")
            return False

    def validate_roll(self, roll):
        """Enhanced roll validation."""
        try:
            if not isinstance(roll, int):
                return False
            
            min_val = self.roll_validation.get('min_value', 1)
            max_val = self.roll_validation.get('max_value', 6)
            
            if not (min_val <= roll <= max_val):
                self.logger.warning(f"Roll {roll} outside valid range [{min_val}, {max_val}]")
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error in validate_roll: {str(e)}")
            return False

    def validate_roll_sequence(self, player):
        """Enhanced roll sequence validation."""
        try:
            if player not in self.rolls:
                return False
            
            rolls = self.rolls[player]
            max_rolls = self.roll_validation.get('required_rolls', 2)
            
            if len(rolls) > max_rolls:
                self.logger.warning(f"Player {player} has too many rolls: {len(rolls)}")
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error in validate_roll_sequence: {str(e)}")
            return False

    def handle_role_validation_error(self):
        """Enhanced role validation error handling."""
        try:
            self.has_error = True
            self._current_error = "Invalid role selection"
            self.role_validation_error = "Please select a valid role (Attacker or Defender)"
            
            # Update UI to show error
            if hasattr(self.ids, 'error_label'):
                self.ids.error_label.text = self.role_validation_error
                self.ids.error_label.opacity = 1
            
            self.logger.warning("Role validation error handled")
        except Exception as e:
            self.logger.error(f"Error in handle_role_validation_error: {str(e)}")

    def handle_roll_validation_error(self):
        """Enhanced roll validation error handling."""
        try:
            self.has_error = True
            self._current_error = "Invalid roll"
            
            # Update UI to show error
            if hasattr(self.ids, 'status_label'):
                self.ids.status_label.text = "Invalid roll. Please try again."
            
            self.logger.warning("Roll validation error handled")
        except Exception as e:
            self.logger.error(f"Error in handle_roll_validation_error: {str(e)}")

    def handle_sequence_validation_error(self):
        """Enhanced sequence validation error handling."""
        try:
            self.has_error = True
            self._current_error = "Invalid deployment sequence"
            
            # Update UI to show error
            if hasattr(self.ids, 'status_label'):
                self.ids.status_label.text = "Invalid deployment sequence. Please try again."
            
            self.logger.warning("Sequence validation error handled")
        except Exception as e:
            self.logger.error(f"Error in handle_sequence_validation_error: {str(e)}")

    def validate_state(self, required_keys):
        """Enhanced state validation with comprehensive checks."""
        try:
            self.logger.debug(f"Validating state with required keys: {required_keys}")
            
            if not isinstance(required_keys, list):
                raise StateError("required_keys must be a list")
            
            # Define required state structure with validators
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
                    'validator': lambda x: x in [self.p1_name, self.p2_name]
                },
                'defender_name': {
                    'type': str,
                    'validator': lambda x: x in [self.p1_name, self.p2_name]
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
            
            self.logger.debug("State validation completed successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error in validate_state: {str(e)}")
            raise

    def update_view_from_state(self):
        """Enhanced view update from state with comprehensive UI synchronization."""
        try:
            self.logger.debug("Updating view from state")
            
            if not self.app or not hasattr(self.app, 'game_state'):
                raise StateError("Game state not available")
            
            state = self.app.game_state
            
            # Update player names
            self.p1_name = state.get('p1_name', 'Player 1')
            self.p2_name = state.get('p2_name', 'Player 2')
            
            # Update rolls
            self.rolls = state.get('rolls', {})
            
            # Update deployments
            self.p1_deployment = state.get('p1_deployment', '')
            self.p2_deployment = state.get('p2_deployment', '')
            
            # Update deployment sequence
            self.deployment_sequence = state.get('deployment_sequence', [])
            
            # Update scores
            self.scores = state.get('scores', {})
            self.final_scores_text = state.get('final_scores_text', '')
            
            # Update UI elements
            self.update_ui()
            
            self.logger.debug("View update from state completed")
        except Exception as e:
            self.logger.error(f"Error in update_view_from_state: {str(e)}")
            self.handle_error(e)

    def update_ui(self):
        """Enhanced UI update with comprehensive element synchronization."""
        try:
            self.logger.debug("Updating UI elements")
            
            # Update player name labels
            if hasattr(self.ids, 'p1_name_label'):
                self.ids.p1_name_label.text = self.p1_name
            if hasattr(self.ids, 'p2_name_label'):
                self.ids.p2_name_label.text = self.p2_name
            
            # Update roll labels
            if hasattr(self.ids, 'p1_roll_label'):
                self.ids.p1_roll_label.text = str(self.p1_roll) if self.p1_roll > 0 else ""
            if hasattr(self.ids, 'p2_roll_label'):
                self.ids.p2_roll_label.text = str(self.p2_roll) if self.p2_roll > 0 else ""
            
            # Update deployment labels
            if hasattr(self.ids, 'p1_deployment_label'):
                self.ids.p1_deployment_label.text = self.p1_deployment
            if hasattr(self.ids, 'p2_deployment_label'):
                self.ids.p2_deployment_label.text = self.p2_deployment
            
            # Update button states
            if hasattr(self.ids, 'p1_roll_button'):
                self.ids.p1_roll_button.disabled = self.p1_roll > 0
            if hasattr(self.ids, 'p2_roll_button'):
                self.ids.p2_roll_button.disabled = self.p2_roll > 0
            
            # Update choice boxes
            if hasattr(self.ids, 'p1_choice_box'):
                self.ids.p1_choice_box.opacity = 1 if self.winner_id == 1 else 0
                self.ids.p1_choice_box.disabled = self.winner_id != 1
            if hasattr(self.ids, 'p2_choice_box'):
                self.ids.p2_choice_box.opacity = 1 if self.winner_id == 2 else 0
                self.ids.p2_choice_box.disabled = self.winner_id != 2
            
            # Update continue button
            if hasattr(self.ids, 'continue_button'):
                self.ids.continue_button.disabled = not (self.p1_deployment and self.p2_deployment)
            
            # Update error display
            if hasattr(self.ids, 'error_label') and self.has_error:
                self.ids.error_label.text = self._current_error or ""
                self.ids.error_label.opacity = 1
            elif hasattr(self.ids, 'error_label'):
                self.ids.error_label.opacity = 0
            
            self.logger.debug("UI update completed")
        except Exception as e:
            self.logger.error(f"Error in update_ui: {str(e)}")
            self.handle_error(e)

    def broadcast_state(self):
        """Enhanced state broadcasting with error handling."""
        try:
            if self.state_manager and self.state_manager.is_connected():
                # Prepare state update
                state_update = {
                    'p1_name': self.p1_name,
                    'p2_name': self.p2_name,
                    'rolls': dict(self.rolls),
                    'deployment_sequence': list(self.deployment_sequence),
                    'p1_deployment': self.p1_deployment,
                    'p2_deployment': self.p2_deployment,
                    'winner_id': self.winner_id,
                    'scores': dict(self.scores),
                    'final_scores_text': self.final_scores_text,
                    'current_screen': 'deployment_setup'
                }
                
                # Broadcast via state manager
                self.state_manager.broadcast_state(state_update)
                self.logger.debug("State broadcast completed")
            else:
                self.logger.warning("State manager not available for broadcasting")
        except Exception as e:
            self.logger.error(f"Error in broadcast_state: {str(e)}")
            self.handle_error(e)

    def handle_error(self, error):
        """Enhanced error handling with specific error types."""
        try:
            if isinstance(error, ValidationError):
                self.logger.warning(f"Validation error: {str(error)}")
                self.show_error(f"Validation Error: {str(error)}")
            elif isinstance(error, StateError):
                self.logger.error(f"State error: {str(error)}")
                self.show_error(f"State Error: {str(error)}")
            elif isinstance(error, SyncError):
                self.logger.error(f"Sync error: {str(error)}")
                self.show_error(f"Sync Error: {str(error)}")
            else:
                self.logger.error(f"Unexpected error: {str(error)}")
                self.show_error(f"Unexpected Error: {str(error)}")
            
            # Update UI to show error
            self.update_ui()
        except Exception as e:
            self.logger.error(f"Error in handle_error: {str(e)}")

    def update_roll_validation(self):
        """Enhanced roll validation update."""
        try:
            self.logger.debug("Updating roll validation")
            
            # Update validation rules based on current state
            self.roll_validation = {
                'min_value': 1,
                'max_value': 6,
                'required_rolls': 2
            }
            
            # Update game state
            if self.app:
                self.app.game_state['roll_validation'] = dict(self.roll_validation)
            
            self.logger.debug("Roll validation updated")
        except Exception as e:
            self.logger.error(f"Error in update_roll_validation: {str(e)}")
            self.handle_error(e)

    def continue_to_initiative(self):
        """Enhanced initiative transition with validation."""
        try:
            self.logger.info("Continuing to initiative")
            return self.proceed_to_initiative()
        except Exception as e:
            self.logger.error(f"Error in continue_to_initiative: {str(e)}")
            self.handle_error(e)
            return False

    def back_to_name_entry(self):
        """Enhanced back navigation with state cleanup."""
        try:
            self.logger.info("Navigating back to name entry")
            
            # Clear current state
            self.reset_screen()
            
            # Update game state
            if self.app:
                self.app.game_state['current_screen'] = 'name_entry'
            
            # Broadcast state update
            self.broadcast_state()
            
            # Navigate back
            self.manager.current = 'name_entry'
            
            self.logger.info("Successfully navigated back to name entry")
        except Exception as e:
            self.logger.error(f"Error in back_to_name_entry: {str(e)}")
            self.handle_error(e) 