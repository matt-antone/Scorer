from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import NumericProperty, BooleanProperty, StringProperty, DictProperty, ListProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.clock import Clock
import logging
import os
from .base_screen import BaseScreen, ValidationError, StateError, SyncError
from kivy.logger import Logger
from ..state.game_over_state import GameOverState

logger = logging.getLogger(__name__)

Builder.load_file(os.path.join(os.path.dirname(__file__), "game_over_screen.kv"))

class GameOverScreen(BaseScreen):
    """Screen for displaying game over state and final scores with comprehensive state management."""
    
    # Properties
    p1_name = StringProperty('')
    p2_name = StringProperty('')
    p1_primary_score = NumericProperty(0)
    p2_primary_score = NumericProperty(0)
    p1_secondary_score = NumericProperty(0)
    p2_secondary_score = NumericProperty(0)
    p1_cp = NumericProperty(0)
    p2_cp = NumericProperty(0)
    winner = StringProperty('')
    app = ObjectProperty(None)
    
    # Game state
    winner_name = StringProperty('')
    winner_score = NumericProperty(0)
    loser_name = StringProperty('')
    loser_score = NumericProperty(0)
    game_duration = StringProperty('')
    victory_type = StringProperty('')
    scores = DictProperty({})
    final_scores_text = StringProperty('')
    
    # UI state
    is_loading = BooleanProperty(False)
    is_syncing = BooleanProperty(False)
    has_error = BooleanProperty(False)
    players = ListProperty([])
    game_history = ListProperty([])
    cleanup_required = BooleanProperty(False)
    save_game = BooleanProperty(False)
    error_label = None
    total_time_label = None
    final_scores = ListProperty([])
    show_winner = BooleanProperty(False)
    show_scores = BooleanProperty(False)
    
    # State manager
    state = ObjectProperty(None)

    def __init__(self, **kwargs):
        """Initialize the screen with comprehensive state management."""
        super().__init__(**kwargs)
        self.logger.info('GameOverScreen: Initializing with enhanced state management')
        self.app = App.get_running_app()
        self.scores = {}
        self.final_scores_text = ''
        self._error_timeout = None
        self._current_error = ''
        self.error_label = Label(text="")
        self.total_time_label = Label(text="00:00:00")
        self.winner = ''
        self.final_scores = []
        self.show_winner = False
        self.show_scores = False
        self.is_loading = False
        self.is_syncing = False
        self.has_error = False
        self.state = GameOverState()
        
        # Initialize state validation
        self._validate_initial_state()
        
        if not self.children:
            self.add_widget(Label(text='GameOverScreen loaded (no KV)'))
        if not self.game_duration:
            self.game_duration = '00:00'

    def _validate_initial_state(self):
        """Validate initial state and set up required properties."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            
            # Ensure required state properties exist
            if not hasattr(self.app, 'game_state'):
                self.app.game_state = {}
            
            # Initialize required state keys
            required_keys = ['p1_name', 'p2_name', 'scores', 'game_history', 'game_duration']
            for key in required_keys:
                if key not in self.app.game_state:
                    if key == 'scores':
                        self.app.game_state[key] = {}
                    elif key == 'game_history':
                        self.app.game_state[key] = []
                    elif key == 'game_duration':
                        self.app.game_state[key] = '00:00'
                    else:
                        self.app.game_state[key] = ''
            
            self.logger.debug("Initial state validation completed")
        except Exception as e:
            self.logger.error(f"Error in initial state validation: {str(e)}")
            self.handle_error(e)

    def on_pre_enter(self):
        """Enhanced pre-enter with comprehensive state management."""
        try:
            self.logger.info("GameOverScreen: Pre-entering with state management")
            super().on_pre_enter()
            
            # Determine winner and initialize scores
            self.determine_winner()
            if not self.scores or len(self.scores) < 2:
                self.scores = {'Player1': 0, 'Player2': 0}
            
            # Initialize state
            self.has_error = False
            self.initialize_scores()
            self.initialize_cleanup()
            
            # Update view from state
            self.update_view_from_state()
            
            self.logger.info("GameOverScreen: Pre-enter completed")
        except Exception as e:
            self.logger.error(f"Error in on_pre_enter: {str(e)}")
            self.handle_error(e)

    def on_enter(self):
        """Enhanced screen entry with comprehensive state management."""
        try:
            self.logger.info("GameOverScreen: Entering with state management")
            
            # Register as observer for state updates
            if self.state_manager:
                self.state_manager.register_observer(self)
                self.logger.debug("Registered as state observer")
            
            # Load game state and update UI
            self.load_game_state()
            self.update_ui()
            
            # Broadcast current state
            self.broadcast_state()
            
            self.logger.info("GameOverScreen: Successfully entered")
        except Exception as e:
            self.logger.error(f"Error in on_enter: {str(e)}")
            self.handle_error(e)

    def on_leave(self):
        """Enhanced screen exit with proper cleanup."""
        try:
            self.logger.info("GameOverScreen: Leaving with cleanup")
            
            # Unregister as observer
            if self.state_manager:
                self.state_manager.unregister_observer(self)
                self.logger.debug("Unregistered as state observer")
            
            # Stop any ongoing operations
            self.stop_sync()
            
            # Clear any pending operations
            if self._error_timeout:
                self._error_timeout.cancel()
                self._error_timeout = None
            
            super().on_leave()
            self.logger.info("GameOverScreen: Successfully left")
        except Exception as e:
            self.logger.error(f"Error in on_leave: {str(e)}")

    def on_state_update(self, state):
        """Enhanced state update handler with comprehensive validation."""
        try:
            self.logger.debug(f"[GameOverScreen] Received state update: {state}")
            
            # Validate incoming state
            if not self.validate_incoming_state(state):
                raise StateError("Invalid incoming state")
            
            # Update local properties from state
            self.p1_name = state.get('p1_name', '')
            self.p2_name = state.get('p2_name', '')
            self.p1_primary_score = state.get('p1_primary_score', 0)
            self.p2_primary_score = state.get('p2_primary_score', 0)
            self.p1_secondary_score = state.get('p1_secondary_score', 0)
            self.p2_secondary_score = state.get('p2_secondary_score', 0)
            self.p1_cp = state.get('p1_cp', 0)
            self.p2_cp = state.get('p2_cp', 0)
            self.winner = state.get('winner', '')
            self.winner_name = state.get('winner_name', '')
            self.winner_score = state.get('winner_score', 0)
            self.loser_name = state.get('loser_name', '')
            self.loser_score = state.get('loser_score', 0)
            self.game_duration = state.get('game_duration', '00:00')
            self.victory_type = state.get('victory_type', '')
            self.scores = state.get('scores', {})
            self.final_scores_text = state.get('final_scores_text', '')
            self.players = state.get('players', [])
            self.game_history = state.get('game_history', [])
            self.final_scores = state.get('final_scores', [])
            self.show_winner = state.get('show_winner', False)
            self.show_scores = state.get('show_scores', False)
            
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
            required_keys = ['p1_name', 'p2_name', 'scores', 'game_duration']
            for key in required_keys:
                if key not in state:
                    self.logger.warning(f"Missing required key in state: {key}")
                    return False
            
            # Validate scores structure
            if not isinstance(state.get('scores', {}), dict):
                return False
            
            # Validate game history
            if not isinstance(state.get('game_history', []), list):
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error validating incoming state: {str(e)}")
            return False

    def initialize_scores(self):
        """Enhanced score initialization with validation."""
        try:
            self.logger.debug("Initializing scores")
            
            self.scores = self.app.game_state.get('scores', {})
            self.players = list(self.scores.keys())
            
            # Validate scores
            if not self.validate_scores():
                raise ValidationError("Invalid scores in game state")
            
            # Update final scores text
            self.update_final_scores_text()
            
            self.logger.debug("Scores initialized successfully")
        except Exception as e:
            self.logger.error(f"Error in initialize_scores: {str(e)}")
            self.handle_score_validation_error()

    def update_final_scores_text(self):
        """Update the final scores text based on current scores."""
        try:
            if not self.scores:
                self.final_scores_text = "No scores available"
                return
            
            score_lines = []
            for player, score in self.scores.items():
                score_lines.append(f"{player}: {score}")
            
            self.final_scores_text = "\n".join(score_lines)
            self.logger.debug(f"Final scores text updated: {self.final_scores_text}")
        except Exception as e:
            self.logger.error(f"Error in update_final_scores_text: {str(e)}")
            self.final_scores_text = "Error updating scores"

    def initialize_cleanup(self):
        """Enhanced cleanup initialization."""
        try:
            self.logger.debug("Initializing cleanup")
            
            self.cleanup_required = True
            self.game_history = self.app.game_state.get('game_history', [])
            
            self.logger.debug("Cleanup initialized successfully")
        except Exception as e:
            self.logger.error(f"Error in initialize_cleanup: {str(e)}")
            self.handle_error(e)

    def cleanup_game_state(self):
        """Enhanced game state cleanup with comprehensive validation."""
        try:
            self.logger.info("Cleaning up game state")
            
            if not self.app:
                self.app = App.get_running_app()
            
            # Validate cleanup requirements
            if not self.validate_cleanup():
                raise StateError("Invalid cleanup state")
            
            # Save game history if needed
            if self.save_game:
                game_record = {
                    'winner': self.winner,
                    'scores': dict(self.scores),
                    'duration': self.game_duration,
                    'victory_type': self.victory_type,
                    'timestamp': Clock.get_time()
                }
                self.game_history.append(game_record)
                self.app.game_state['game_history'] = list(self.game_history)
                self.logger.debug("Game history saved")
            
            # Reset game state
            reset_state = {
                'p1_name': '',
                'p2_name': '',
                'p1_primary_score': 0,
                'p2_primary_score': 0,
                'p1_secondary_score': 0,
                'p2_secondary_score': 0,
                'p1_cp': 0,
                'p2_cp': 0,
                'winner': '',
                'current_round': 1,
                'game_phase': 'setup',
                'scores': {},
                'game_duration': '00:00',
                'current_screen': 'splash'
            }
            
            self.app.game_state.update(reset_state)
            
            # Reset screen state
            self.reset_screen()
            
            # Broadcast state update
            self.broadcast_state()
            
            self.logger.info("Game state cleanup completed successfully")
        except Exception as e:
            self.logger.error(f"Error in cleanup_game_state: {str(e)}")
            self.handle_cleanup_error()

    def handle_cleanup_error(self):
        """Enhanced cleanup error handling."""
        try:
            self.logger.warning("Handling cleanup error")
            
            self.has_error = True
            self._current_error = "Error cleaning up game state"
            
            # Show error in UI
            self.show_error("Error cleaning up game state")
            
            # Update UI
            self.update_ui()
            
            self.cleanup_required = False
            
            self.logger.warning("Cleanup error handled")
        except Exception as e:
            self.logger.error(f"Error in handle_cleanup_error: {str(e)}")
            self.show_error("Critical error in cleanup")

    def update_scores(self, new_scores):
        """Enhanced score update with comprehensive validation."""
        try:
            self.logger.debug(f"Updating scores: {new_scores}")
            
            # Validate new scores
            if not isinstance(new_scores, dict):
                raise ValidationError("Scores must be a dictionary")
            
            # Validate each score
            for player, score in new_scores.items():
                if not isinstance(score, (int, float)) or score < 0:
                    raise ValidationError(f"Invalid score for {player}: {score}")
            
            # Update scores
            self.scores = dict(new_scores)
            
            # Update final scores list
            self.final_scores = [
                {'name': str(player), 'score': int(score)}
                for player, score in self.scores.items()
            ]
            
            # Update final scores text
            self.update_final_scores_text()
            
            # Determine winner
            self.determine_winner()
            
            # Broadcast state update
            self.broadcast_state()
            
            self.logger.debug("Scores updated successfully")
        except Exception as e:
            self.logger.error(f"Error in update_scores: {str(e)}")
            self.handle_score_validation_error()

    def determine_winner(self):
        """Enhanced winner determination with comprehensive validation."""
        try:
            self.logger.debug("Determining winner")
            
            # Validate scores exist
            if not self.scores or len(self.scores) < 2:
                self.scores = {'Player1': 0, 'Player2': 0}
                self.logger.warning("No scores available, using defaults")
            
            # Calculate total scores
            p1_total = self.p1_primary_score + self.p1_secondary_score
            p2_total = self.p2_primary_score + self.p2_secondary_score
            
            # Update scores in state
            self.scores = {
                self.p1_name or 'Player1': p1_total,
                self.p2_name or 'Player2': p2_total
            }
            
            # Determine winner
            if p1_total > p2_total:
                self.winner = self.p1_name or 'Player1'
                self.winner_name = self.p1_name or 'Player1'
                self.winner_score = p1_total
                self.loser_name = self.p2_name or 'Player2'
                self.loser_score = p2_total
                self.victory_type = 'score'
            elif p2_total > p1_total:
                self.winner = self.p2_name or 'Player2'
                self.winner_name = self.p2_name or 'Player2'
                self.winner_score = p2_total
                self.loser_name = self.p1_name or 'Player1'
                self.loser_score = p1_total
                self.victory_type = 'score'
            else:
                self.winner = 'Tie'
                self.winner_name = 'Tie'
                self.winner_score = p1_total
                self.loser_name = 'Tie'
                self.loser_score = p2_total
                self.victory_type = 'tie'
            
            # Update final scores text
            self.update_final_scores_text()
            
            # Update UI
            self.show_winner = True
            self.show_scores = True
            
            # Update game state
            if self.app:
                self.app.game_state.update({
                    'winner': self.winner,
                    'winner_name': self.winner_name,
                    'winner_score': self.winner_score,
                    'loser_name': self.loser_name,
                    'loser_score': self.loser_score,
                    'victory_type': self.victory_type,
                    'scores': dict(self.scores)
                })
            
            self.logger.debug(f"Winner determined: {self.winner}")
        except Exception as e:
            self.logger.error(f"Error in determine_winner: {str(e)}")
            self.handle_winner_determination_error(str(e))

    def validate_scores(self):
        """Enhanced score validation."""
        try:
            if not isinstance(self.scores, dict):
                return False
            
            for player, score in self.scores.items():
                if not isinstance(score, (int, float)) or score < 0:
                    self.logger.warning(f"Invalid score for {player}: {score}")
                    return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error in validate_scores: {str(e)}")
            return False

    def validate_cleanup(self):
        """Enhanced cleanup validation."""
        try:
            # Validate that cleanup is required
            if not self.cleanup_required:
                return False
            
            # Validate game history is a list
            if not isinstance(self.game_history, list):
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error in validate_cleanup: {str(e)}")
            return False

    def return_to_splash(self):
        """Enhanced return to splash with state management."""
        try:
            self.logger.info("Returning to splash screen")
            
            # Clean up game state
            self.cleanup_game_state()
            
            # Navigate to splash
            self.manager.current = 'splash'
            
            self.logger.info("Successfully returned to splash")
        except Exception as e:
            self.logger.error(f"Error in return_to_splash: {str(e)}")
            self.handle_error(e)

    def start_new_game(self):
        """Enhanced new game start with state management."""
        try:
            self.logger.info("Starting new game")
            
            # Clean up current game state
            self.cleanup_game_state()
            
            # Navigate to name entry
            self.manager.current = 'name_entry'
            
            self.logger.info("Successfully started new game")
        except Exception as e:
            self.logger.error(f"Error in start_new_game: {str(e)}")
            self.handle_error(e)

    def handle_score_validation_error(self):
        """Enhanced score validation error handling."""
        try:
            self.logger.warning("Handling score validation error")
            
            self.has_error = True
            self._current_error = "Invalid score data"
            
            # Show error in UI
            if hasattr(self.ids, 'error_label'):
                self.ids.error_label.text = "Invalid score data"
                self.ids.error_label.opacity = 1
            
            self.logger.warning("Score validation error handled")
        except Exception as e:
            self.logger.error(f"Error in handle_score_validation_error: {str(e)}")

    def validate_state(self, state):
        """Enhanced state validation."""
        try:
            if not isinstance(state, dict):
                return False
            
            required_keys = ['p1_name', 'p2_name', 'scores', 'game_duration']
            for key in required_keys:
                if key not in state:
                    return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error in validate_state: {str(e)}")
            return False

    def update_view_from_state(self):
        """Enhanced view update from state with comprehensive UI synchronization."""
        try:
            self.logger.debug("Updating view from state")
            
            if not self.app or not hasattr(self.app, 'game_state'):
                raise StateError("Game state not available")
            
            state = self.app.game_state
            
            # Update player names
            self.p1_name = state.get('p1_name', '')
            self.p2_name = state.get('p2_name', '')
            
            # Update scores
            self.p1_primary_score = state.get('p1_primary_score', 0)
            self.p2_primary_score = state.get('p2_primary_score', 0)
            self.p1_secondary_score = state.get('p1_secondary_score', 0)
            self.p2_secondary_score = state.get('p2_secondary_score', 0)
            self.p1_cp = state.get('p1_cp', 0)
            self.p2_cp = state.get('p2_cp', 0)
            
            # Update game state
            self.winner = state.get('winner', '')
            self.winner_name = state.get('winner_name', '')
            self.winner_score = state.get('winner_score', 0)
            self.loser_name = state.get('loser_name', '')
            self.loser_score = state.get('loser_score', 0)
            self.game_duration = state.get('game_duration', '00:00')
            self.victory_type = state.get('victory_type', '')
            self.scores = state.get('scores', {})
            self.final_scores_text = state.get('final_scores_text', '')
            self.players = state.get('players', [])
            self.game_history = state.get('game_history', [])
            self.final_scores = state.get('final_scores', [])
            self.show_winner = state.get('show_winner', False)
            self.show_scores = state.get('show_scores', False)
            
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
                self.ids.p1_name_label.text = self.p1_name or 'Player 1'
            if hasattr(self.ids, 'p2_name_label'):
                self.ids.p2_name_label.text = self.p2_name or 'Player 2'
            
            # Update final score labels
            if hasattr(self.ids, 'p1_final_score_label'):
                p1_total = self.p1_primary_score + self.p1_secondary_score
                self.ids.p1_final_score_label.text = str(p1_total)
            if hasattr(self.ids, 'p2_final_score_label'):
                p2_total = self.p2_primary_score + self.p2_secondary_score
                self.ids.p2_final_score_label.text = str(p2_total)
            
            # Update total time label
            if hasattr(self.ids, 'total_time_label'):
                self.ids.total_time_label.text = self.game_duration or '00:00'
            
            # Update error display
            if hasattr(self.ids, 'error_label'):
                if self.has_error and self._current_error:
                    self.ids.error_label.text = self._current_error
                    self.ids.error_label.opacity = 1
                else:
                    self.ids.error_label.opacity = 0
            
            # Update button states
            if hasattr(self.ids, 'new_game_button'):
                self.ids.new_game_button.disabled = self.is_loading
            if hasattr(self.ids, 'exit_button'):
                self.ids.exit_button.disabled = self.is_loading
            
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
                    'p1_primary_score': self.p1_primary_score,
                    'p2_primary_score': self.p2_primary_score,
                    'p1_secondary_score': self.p1_secondary_score,
                    'p2_secondary_score': self.p2_secondary_score,
                    'p1_cp': self.p1_cp,
                    'p2_cp': self.p2_cp,
                    'winner': self.winner,
                    'winner_name': self.winner_name,
                    'winner_score': self.winner_score,
                    'loser_name': self.loser_name,
                    'loser_score': self.loser_score,
                    'game_duration': self.game_duration,
                    'victory_type': self.victory_type,
                    'scores': dict(self.scores),
                    'final_scores_text': self.final_scores_text,
                    'players': list(self.players),
                    'game_history': list(self.game_history),
                    'final_scores': list(self.final_scores),
                    'show_winner': self.show_winner,
                    'show_scores': self.show_scores,
                    'current_screen': 'game_over'
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

    def load_game_state(self):
        """Enhanced game state loading with validation."""
        try:
            self.logger.debug("Loading game state")
            
            if not self.app:
                self.app = App.get_running_app()
            
            # Load state from app
            state = self.app.game_state
            
            # Validate state
            if not self.validate_state(state):
                raise StateError("Invalid game state")
            
            # Update local properties
            self.p1_name = state.get('p1_name', '')
            self.p2_name = state.get('p2_name', '')
            self.p1_primary_score = state.get('p1_primary_score', 0)
            self.p2_primary_score = state.get('p2_primary_score', 0)
            self.p1_secondary_score = state.get('p1_secondary_score', 0)
            self.p2_secondary_score = state.get('p2_secondary_score', 0)
            self.p1_cp = state.get('p1_cp', 0)
            self.p2_cp = state.get('p2_cp', 0)
            self.game_duration = state.get('game_duration', '00:00')
            
            # Update scores
            self.scores = state.get('scores', {})
            self.players = list(self.scores.keys())
            
            # Determine winner
            self.determine_winner()
            
            self.logger.debug("Game state loaded successfully")
        except Exception as e:
            self.logger.error(f"Error in load_game_state: {str(e)}")
            self.handle_state_error()

    def handle_state_error(self):
        """Enhanced state error handling."""
        try:
            self.logger.warning("Handling state error")
            
            self.has_error = True
            self._current_error = "Error loading game state"
            
            # Show error in UI
            self.show_error("Error loading game state")
            
            self.logger.warning("State error handled")
        except Exception as e:
            self.logger.error(f"Error in handle_state_error: {str(e)}")

    def reset_screen(self):
        """Enhanced screen reset with state management."""
        try:
            self.logger.debug("Resetting screen")
            
            # Reset local properties
            self.p1_name = ''
            self.p2_name = ''
            self.p1_primary_score = 0
            self.p2_primary_score = 0
            self.p1_secondary_score = 0
            self.p2_secondary_score = 0
            self.p1_cp = 0
            self.p2_cp = 0
            self.winner = ''
            self.winner_name = ''
            self.winner_score = 0
            self.loser_name = ''
            self.loser_score = 0
            self.game_duration = '00:00'
            self.victory_type = ''
            self.scores = {}
            self.final_scores_text = ''
            self.players = []
            self.final_scores = []
            self.show_winner = False
            self.show_scores = False
            self.has_error = False
            self._current_error = ''
            
            # Update UI
            self.update_ui()
            
            self.logger.debug("Screen reset completed")
        except Exception as e:
            self.logger.error(f"Error in reset_screen: {str(e)}")
            self.handle_error(e)

    def return_to_menu(self):
        """Enhanced return to menu with state management."""
        try:
            self.logger.info("Returning to menu")
            self.return_to_splash()
        except Exception as e:
            self.logger.error(f"Error in return_to_menu: {str(e)}")
            self.handle_error(e)

    def handle_winner_determination_error(self, error_msg=None):
        """Enhanced winner determination error handling."""
        try:
            self.logger.warning("Handling winner determination error")
            
            self.has_error = True
            self._current_error = error_msg or "Error determining winner"
            
            # Show error in UI
            if hasattr(self.ids, 'error_label'):
                self.ids.error_label.text = self._current_error
                self.ids.error_label.opacity = 1
            
            self.logger.warning("Winner determination error handled")
        except Exception as e:
            self.logger.error(f"Error in handle_winner_determination_error: {str(e)}") 