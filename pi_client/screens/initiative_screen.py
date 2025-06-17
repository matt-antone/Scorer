from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, DictProperty, ObjectProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
import logging
import os
import random
from .base_screen import BaseScreen, ValidationError, StateError, SyncError

logger = logging.getLogger(__name__)

Builder.load_file(os.path.join(os.path.dirname(__file__), "initiative_screen.kv"))

class InitiativeScreen(BaseScreen):
    """Screen for determining initiative order with comprehensive state management."""
    
    # Properties
    p1_name = StringProperty('')
    p2_name = StringProperty('')
    p1_roll = NumericProperty(0)
    p2_roll = NumericProperty(0)
    winner_id = NumericProperty(0)
    current_round = NumericProperty(1)
    max_rounds = NumericProperty(5)
    player_rolls = DictProperty({})
    initiative_winner = ObjectProperty(None, allownone=True)
    initiative_loser = ObjectProperty(None, allownone=True)
    is_loading = BooleanProperty(False)
    is_syncing = BooleanProperty(False)
    has_error = BooleanProperty(False)
    app = ObjectProperty(None)
    p1_roll_button = None
    p2_roll_button = None
    players = ListProperty([])
    rolls = DictProperty({})
    roll_validation = DictProperty({'min_value': 1, 'max_value': 6})
    _error_timeout = None
    _current_error = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.logger.info("InitiativeScreen: Initializing with enhanced state management")
        self.app = App.get_running_app()
        self.initiative_winner = None
        self.initiative_loser = None
        self._error_timeout = None
        self._current_error = ''
        if not self.children:
            self.add_widget(Label(text='InitiativeScreen loaded (no KV)'))
        self.p1_roll_button = Button(disabled=False)
        self.p2_roll_button = Button(disabled=False)
        self._validate_initial_state()

    def _validate_initial_state(self):
        try:
            if not self.app:
                self.app = App.get_running_app()
            if not hasattr(self.app, 'game_state'):
                self.app.game_state = {}
            required_keys = ['players', 'rolls', 'roll_validation', 'current_round']
            for key in required_keys:
                if key not in self.app.game_state:
                    if key == 'players':
                        self.app.game_state[key] = ['Player1', 'Player2']
                    elif key == 'rolls':
                        self.app.game_state[key] = {p: None for p in self.app.game_state['players']}
                    elif key == 'roll_validation':
                        self.app.game_state[key] = {'min_value': 1, 'max_value': 6}
                    elif key == 'current_round':
                        self.app.game_state[key] = 1
            self.logger.debug("Initial state validation completed")
        except Exception as e:
            self.logger.error(f"Error in initial state validation: {str(e)}")
            self.handle_error(e)

    def on_pre_enter(self):
        try:
            self.logger.info("InitiativeScreen: Pre-entering with state management")
            super().on_pre_enter()
            self.initialize_rolls()
            self.has_error = False
            self.update_view_from_state()
            self.logger.info("InitiativeScreen: Pre-enter completed")
        except Exception as e:
            self.logger.error(f"Error in on_pre_enter: {str(e)}")
            self.handle_error(e)

    def on_enter(self):
        try:
            self.logger.info("InitiativeScreen: Entering with state management")
            if self.state_manager:
                self.state_manager.register_observer(self)
                self.logger.debug("Registered as state observer")
            self.update_view_from_state()
            self.broadcast_state()
            self.logger.info("InitiativeScreen: Successfully entered")
        except Exception as e:
            self.logger.error(f"Error in on_enter: {str(e)}")
            self.handle_error(e)

    def on_leave(self):
        try:
            self.logger.info("InitiativeScreen: Leaving with cleanup")
            if self.state_manager:
                self.state_manager.unregister_observer(self)
                self.logger.debug("Unregistered as state observer")
            self.stop_sync()
            if self._error_timeout:
                self._error_timeout.cancel()
                self._error_timeout = None
            super().on_leave()
            self.logger.info("InitiativeScreen: Successfully left")
        except Exception as e:
            self.logger.error(f"Error in on_leave: {str(e)}")

    def on_state_update(self, state):
        try:
            self.logger.debug(f"[InitiativeScreen] Received state update: {state}")
            if not self.validate_incoming_state(state):
                raise StateError("Invalid incoming state")
            self.p1_name = state.get('p1_name', '')
            self.p2_name = state.get('p2_name', '')
            self.current_round = state.get('current_round', 1)
            self.players = state.get('players', ['Player1', 'Player2'])
            self.rolls = state.get('rolls', {p: None for p in self.players})
            self.roll_validation = state.get('roll_validation', {'min_value': 1, 'max_value': 6})
            self.initiative_winner = state.get('initiative_winner', None)
            self.initiative_loser = state.get('initiative_loser', None)
            self.update_ui()
            self.logger.debug("State update processed successfully")
        except Exception as e:
            self.logger.error(f"Error in on_state_update: {str(e)}")
            self.handle_error(e)

    def validate_incoming_state(self, state):
        try:
            if not isinstance(state, dict):
                return False
            required_keys = ['players', 'rolls', 'roll_validation', 'current_round']
            for key in required_keys:
                if key not in state:
                    self.logger.warning(f"Missing required key in state: {key}")
                    return False
            if not isinstance(state.get('rolls', {}), dict):
                return False
            if not isinstance(state.get('players', []), list):
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error validating incoming state: {str(e)}")
            return False

    def initialize_rolls(self):
        try:
            self.players = self.app.game_state.get('players', ['Player1', 'Player2'])
            self.rolls = {player: None for player in self.players}
            self.roll_validation = self.app.game_state.get('roll_validation', {'min_value': 1, 'max_value': 6})
            self.logger.debug("Rolls initialized successfully")
        except Exception as e:
            self.logger.error(f"Error in initialize_rolls: {str(e)}")
            self.handle_roll_validation_error()

    def validate_roll(self, roll):
        try:
            min_val = self.roll_validation.get('min_value', 1)
            max_val = self.roll_validation.get('max_value', 6)
            if not isinstance(roll, int) or roll < min_val or roll > max_val:
                raise ValidationError("Invalid roll value")
            return True
        except Exception as e:
            self.logger.error(f"Error in validate_roll: {str(e)}")
            self.handle_roll_validation_error()
            return False

    def determine_initiative(self):
        try:
            if None in self.rolls.values():
                return
            p1_roll = self.rolls.get(self.players[0], 0)
            p2_roll = self.rolls.get(self.players[1], 0)
            self.ids.p1_roll_label.text = str(p1_roll)
            self.ids.p2_roll_label.text = str(p2_roll)
            if p1_roll > p2_roll:
                self.winner_id = 1
                self.initiative_winner = self.players[0]
                self.initiative_loser = self.players[1]
                self.ids.status_label.text = f"{self.initiative_winner} won initiative!"
                self.ids.p1_choice_box.opacity = 1
                self.ids.p1_choice_box.disabled = False
            elif p2_roll > p1_roll:
                self.winner_id = 2
                self.initiative_winner = self.players[1]
                self.initiative_loser = self.players[0]
                self.ids.status_label.text = f"{self.initiative_winner} won initiative!"
                self.ids.p2_choice_box.opacity = 1
                self.ids.p2_choice_box.disabled = False
            else:
                self.reset_rolls()
                self.ids.status_label.text = "It's a tie! Roll again."
                return
            if self.app:
                self.app.game_state.update({
                    'initiative_winner': self.initiative_winner,
                    'initiative_loser': self.initiative_loser,
                    'current_round': self.current_round
                })
            self.broadcast_state()
            self.logger.debug("Initiative determined and state broadcasted")
        except Exception as e:
            self.logger.error(f"Error in determine_initiative: {str(e)}")
            self.handle_winner_validation_error()

    def handle_initiative_tie(self):
        try:
            max_roll = max(self.rolls.values())
            tied_players = [p for p, r in self.rolls.items() if r == max_roll]
            for player in tied_players:
                self.rolls[player] = None
            if hasattr(self, 'ids'):
                if 'status_label' in self.ids:
                    self.ids.status_label.text = "Tie detected - tied players must roll again"
                for player in tied_players:
                    button_id = f'{player}_roll_button'
                    if button_id in self.ids:
                        self.ids[button_id].disabled = False
            self.show_error("Tie detected - tied players must roll again")
            self.logger.debug("Initiative tie handled")
        except Exception as e:
            self.logger.error(f"Error in handle_initiative_tie: {str(e)}")
            self.handle_initiative_determination_error()

    def handle_roll_validation_error(self):
        try:
            self.has_error = True
            self._current_error = "Invalid roll value"
            if hasattr(self.ids, 'error_label'):
                self.ids.error_label.text = "Invalid roll value"
                self.ids.error_label.opacity = 1
            self.logger.warning("Roll validation error handled")
        except Exception as e:
            self.logger.error(f"Error in handle_roll_validation_error: {str(e)}")

    def handle_initiative_determination_error(self):
        try:
            self.has_error = True
            self._current_error = "Failed to determine initiative"
            if hasattr(self.ids, 'error_label'):
                self.ids.error_label.text = "Failed to determine initiative"
                self.ids.error_label.opacity = 1
            self.logger.warning("Initiative determination error handled")
        except Exception as e:
            self.logger.error(f"Error in handle_initiative_determination_error: {str(e)}")

    def validate_state(self, required_keys=None):
        try:
            if required_keys is None:
                required_keys = [
                    'players', 'rolls', 'initiative_winner',
                    'roll_validation'
                ]
            for key in required_keys:
                if not hasattr(self, key):
                    raise StateError(f"Missing required state key: {key}")
            return True
        except Exception as e:
            self.logger.error(f"Error in validate_state: {str(e)}")
            return False

    def validate_input(self, data, validators):
        try:
            if not isinstance(data, dict):
                raise ValidationError("Input must be a dictionary")
            for key, validator in validators.items():
                if key not in data:
                    raise ValidationError(f"Missing required input: {key}")
                if not validator(data[key]):
                    raise ValidationError(f"Invalid input for {key}")
            return True
        except Exception as e:
            self.logger.error(f"Error in validate_input: {str(e)}")
            return False

    def update_view_from_state(self):
        try:
            self.logger.debug("Updating view from state")
            if not self.app or not hasattr(self.app, 'game_state'):
                raise StateError("Game state not available")
            state = self.app.game_state
            self.p1_name = state.get('p1_name', '')
            self.p2_name = state.get('p2_name', '')
            self.current_round = state.get('current_round', 1)
            self.players = state.get('players', ['Player1', 'Player2'])
            self.rolls = state.get('rolls', {p: None for p in self.players})
            self.roll_validation = state.get('roll_validation', {'min_value': 1, 'max_value': 6})
            self.initiative_winner = state.get('initiative_winner', None)
            self.initiative_loser = state.get('initiative_loser', None)
            self.update_ui()
            self.logger.debug("View update from state completed")
        except Exception as e:
            self.logger.error(f"Error in update_view_from_state: {str(e)}")
            self.handle_error(e)

    def update_ui(self):
        try:
            self.logger.debug("Updating UI elements")
            if hasattr(self.ids, 'p1_name_label'):
                self.ids.p1_name_label.text = self.p1_name or 'Player 1'
            if hasattr(self.ids, 'p2_name_label'):
                self.ids.p2_name_label.text = self.p2_name or 'Player 2'
            if hasattr(self.ids, 'p1_roll_label'):
                self.ids.p1_roll_label.text = str(self.rolls.get(self.players[0], ''))
            if hasattr(self.ids, 'p2_roll_label'):
                self.ids.p2_roll_label.text = str(self.rolls.get(self.players[1], ''))
            if hasattr(self.ids, 'status_label'):
                if self.initiative_winner:
                    self.ids.status_label.text = f"{self.initiative_winner} won initiative!"
                else:
                    self.ids.status_label.text = "Roll to determine initiative."
            if hasattr(self.ids, 'error_label'):
                if self.has_error and self._current_error:
                    self.ids.error_label.text = self._current_error
                    self.ids.error_label.opacity = 1
                else:
                    self.ids.error_label.opacity = 0
            self.logger.debug("UI update completed")
        except Exception as e:
            self.logger.error(f"Error in update_ui: {str(e)}")
            self.handle_error(e)

    def broadcast_state(self):
        try:
            if self.state_manager and self.state_manager.is_connected():
                state_update = {
                    'p1_name': self.p1_name,
                    'p2_name': self.p2_name,
                    'current_round': self.current_round,
                    'players': list(self.players),
                    'rolls': dict(self.rolls),
                    'roll_validation': dict(self.roll_validation),
                    'initiative_winner': self.initiative_winner,
                    'initiative_loser': self.initiative_loser,
                    'current_screen': 'initiative'
                }
                self.state_manager.broadcast_state(state_update)
                self.logger.debug("State broadcast completed")
            else:
                self.logger.warning("State manager not available for broadcasting")
        except Exception as e:
            self.logger.error(f"Error in broadcast_state: {str(e)}")
            self.handle_error(e)

    def handle_error(self, error):
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
            self.update_ui()
        except Exception as e:
            self.logger.error(f"Error in handle_error: {str(e)}")

    def reset_screen(self, is_reroll=False):
        """Resets the screen to its initial state."""
        try:
            self.p1_roll = 0
            self.p2_roll = 0
            self.winner_id = 0
            self.ids.p1_roll_button.disabled = False
            self.ids.p2_roll_button.disabled = False
            self.ids.continue_button.disabled = True
            self.ids.p1_choice_box.opacity = 0
            self.ids.p1_choice_box.disabled = True
            self.ids.p2_choice_box.opacity = 0
            self.ids.p2_choice_box.disabled = True

            if not is_reroll:
                self.ids.p1_roll_label.text = ""
                self.ids.p2_roll_label.text = ""
                self.ids.status_label.text = "Players roll for initiative."
            else:
                self.ids.status_label.text = "It's a tie! Re-roll."
        except Exception as e:
            logger.error(f"Error in reset_screen: {str(e)}")
            self.handle_winner_validation_error()

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
        """Determines the winner of the initiative roll."""
        try:
            if self.p1_roll > self.p2_roll:
                self.winner_id = 1
                self.initiative_winner = self.ids.p1_name_label.text
                self.initiative_loser = self.ids.p2_name_label.text
                self.ids.status_label.text = f"{self.initiative_winner} won initiative!"
                self.ids.p1_choice_box.opacity = 1
                self.ids.p1_choice_box.disabled = False
            elif self.p2_roll > self.p1_roll:
                self.winner_id = 2
                self.initiative_winner = self.ids.p2_name_label.text
                self.initiative_loser = self.ids.p1_name_label.text
                self.ids.status_label.text = f"{self.initiative_winner} won initiative!"
                self.ids.p2_choice_box.opacity = 1
                self.ids.p2_choice_box.disabled = False
            else:
                self.reset_screen(is_reroll=True)
                return

            if self.app:
                self.app.game_state.update({
                    'initiative_winner': self.initiative_winner,
                    'initiative_loser': self.initiative_loser,
                    'current_round': self.current_round
                })
        except Exception as e:
            logger.error(f"Error in determine_winner: {str(e)}")
            self.handle_winner_validation_error()

    def select_first_turn(self, player_id):
        """Handle first turn selection."""
        try:
            if player_id not in [1, 2]:
                raise ValidationError("Invalid player ID")
                
            # Set first player in game state
            if self.app:
                self.app.game_state['first_player'] = player_id
                
            # Update UI
            self.ids.status_label.text = f"{self.players[player_id-1]} will go first!"
            self.ids.continue_button.opacity = 1
            self.ids.continue_button.disabled = False
            
            # Disable choice boxes
            self.ids.p1_choice_box.disabled = True
            self.ids.p2_choice_box.disabled = True
            
        except Exception as e:
            logger.error(f"Error in select_first_turn: {str(e)}")
            self.handle_winner_validation_error()

    def continue_to_game(self):
        """Alias for proceed_to_scoreboard to match KV file binding."""
        try:
            self.proceed_to_scoreboard()
        except Exception as e:
            logger.error(f"Error in continue_to_game: {str(e)}")
            self.handle_winner_validation_error()

    def handle_winner_error(self):
        """Handle winner determination error."""
        try:
            self.has_error = True
            self.ids.status_label.text = "Error determining winner"
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in handle_winner_error: {str(e)}")
            self.handle_winner_validation_error()

    def proceed_to_scoreboard(self):
        """Proceed to scoreboard screen."""
        try:
            app = App.get_running_app()
            if app:
                self.validate_state()
                app.root.current = 'scoreboard'
        except StateError as e:
            logger.error(f"State validation error: {str(e)}")
            self.handle_state_error()

    def back_to_deployment(self):
        """Go back to deployment screen."""
        try:
            app = App.get_running_app()
            if app:
                app.root.current = 'deployment'
        except Exception as e:
            logger.error(f"Error in back_to_deployment: {str(e)}")
            self.handle_winner_validation_error()

    def handle_round_validation_error(self):
        """Handle round validation error."""
        try:
            self.show_error("Invalid round value")
            self.reset_screen()
        except Exception as e:
            logger.error(f"Error in handle_round_validation_error: {str(e)}")
            self.handle_winner_validation_error()

    def add_roll(self, player, roll):
        """Add a roll for a player."""
        try:
            # Validate player
            if player not in self.players:
                raise ValidationError(f"Invalid player: {player}")
                
            # Validate roll
            self.validate_roll(roll)
            
            # Add roll
            self.rolls[player] = roll
            
            # Update game state
            if self.app:
                self.app.game_state['rolls'] = self.rolls
                
            # Update UI
            self.update_ui()
            
            # Check if all players have rolled
            if None not in self.rolls.values():
                self.determine_initiative()
                
        except Exception as e:
            self.handle_roll_validation_error()

    def handle_state_error(self):
        """Handle state error."""
        try:
            self.show_error("Invalid game state")
            self.reset_screen()
        except Exception as e:
            logger.error(f"Error in handle_state_error: {str(e)}")
            self.handle_winner_validation_error()

    def handle_winner_validation_error(self):
        """Handle winner validation error."""
        try:
            self.has_error = True
            self.ids.status_label.text = "Error validating winner"
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in handle_winner_validation_error: {str(e)}")
            self.show_error("Critical error in winner validation")

    def reset_rolls(self):
        """Reset all player rolls and clear winner/loser."""
        for player in self.rolls:
            self.rolls[player] = None
        self.initiative_winner = None
        self.initiative_loser = None
        self.update_ui() 