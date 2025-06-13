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

logger = logging.getLogger(__name__)

Builder.load_file(os.path.join(os.path.dirname(__file__), "../widgets/rounded_button.kv"))
Builder.load_file(os.path.join(os.path.dirname(__file__), "game_over_screen.kv"))

class GameOverScreen(BaseScreen):
    """Screen for displaying game over state and final scores."""
    
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

    def __init__(self, **kwargs):
        """Initialize the screen."""
        super().__init__(**kwargs)
        Logger.info('GameOverScreen: Initializing')
        self.app = App.get_running_app()
        self.scores = {}  # Start with empty dict
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
        if not self.children:
            self.add_widget(Label(text='GameOverScreen loaded (no KV)'))

    def on_pre_enter(self):
        """Called before the screen is entered."""
        super().on_pre_enter()
        self.determine_winner()
        if not self.scores or len(self.scores) < 2:
            self.scores = {'Player1': 0, 'Player2': 0}
        self.has_error = False
        self.initialize_scores()
        self.initialize_cleanup()

    def on_enter(self):
        """Called when the screen is entered."""
        Logger.debug('Entering screen')
        self.load_game_state()
        self.update_ui()

    def on_leave(self):
        """Called when leaving the screen."""
        super().on_leave()
        self.stop_sync()
        if self._error_timeout:
            self._error_timeout.cancel()

    def initialize_scores(self):
        """Initialize the scores from game state."""
        try:
            self.scores = self.app.game_state.get('scores', {})
            self.players = list(self.scores.keys())
            self.validate_scores()
        except Exception as e:
            self.handle_score_validation_error()

    def initialize_cleanup(self):
        """Initialize cleanup process."""
        self.cleanup_required = True
        self.game_history = self.app.game_state.get('game_history', [])

    def cleanup_game_state(self):
        """Clean up the game state."""
        try:
            if not self.cleanup_required:
                return
                
            # Add current game to history
            game_summary = {
                'players': self.players,
                'scores': self.scores,
                'winner': self.winner,
                'timestamp': Clock.get_time()
            }
            self.game_history.append(game_summary)
            
            # Clear game state
            self.app.game_state.clear()
            self.cleanup_required = False
            
        except Exception as e:
            self.handle_cleanup_error()

    def update_scores(self, new_scores):
        """Update the scores with new values and update final_scores."""
        try:
            # Accept any dict of player: score, as long as all scores are non-negative numbers
            for score in new_scores.values():
                if not isinstance(score, (int, float)) or score < 0:
                    self.handle_score_validation_error()
                    return
            self.scores = dict(new_scores)  # Replace instead of update
            self.final_scores = [
                {'name': str(player), 'score': int(score)}
                for player, score in self.scores.items()
            ]
            self.determine_winner()
        except Exception as e:
            self.handle_score_validation_error()

    def determine_winner(self):
        """Determine the winner based on scores, handle ties as 'Tie'."""
        try:
            if not self.scores or len(self.scores) < 2:
                self.scores = {'Player1': 0, 'Player2': 0}
            max_score = max(self.scores.values())
            winners = [p for p, s in self.scores.items() if s == max_score]
            if len(winners) == 1:
                self.winner = winners[0]
            elif len(winners) > 1:
                self.winner = 'Tie'
            else:
                self.winner = ''
        except Exception as e:
            self.show_error("Critical error in winner validation")

    def validate_scores(self):
        """Validate the current scores."""
        if not isinstance(self.scores, dict):
            raise ValidationError("Scores must be a dictionary")
            
        for player, score in self.scores.items():
            if not isinstance(score, (int, float)) or score < 0:
                raise ValidationError(f"Invalid score for {player}")
                
        return True

    def validate_cleanup(self):
        """Validate the cleanup state."""
        if not self.cleanup_required:
            return True
            
        if not isinstance(self.game_history, list):
            raise StateError("Game history must be a list")
            
        return True

    def return_to_splash(self):
        """Return to the splash screen."""
        try:
            self.cleanup_game_state()
            self.app.root.current = 'splash'
        except Exception as e:
            self.handle_cleanup_error()

    def start_new_game(self):
        """Start a new game."""
        try:
            self.cleanup_game_state()
            self.app.root.current = 'name_entry'
        except Exception as e:
            self.handle_cleanup_error()

    def handle_score_validation_error(self):
        """Handle score validation errors."""
        self.show_error("Invalid score value")

    def handle_cleanup_error(self):
        """Handle cleanup errors."""
        self.show_error("Failed to clean up game state: cleanup error")

    def validate_state(self, state):
        """Validate a state dict for test compatibility."""
        if not isinstance(state, dict):
            return False
        if 'winner' not in state or 'scores' not in state:
            return False
        if state['winner'] is None:
            return False
        if not isinstance(state['scores'], dict):
            return False
        if not state['scores']:
            return False
        for v in state['scores'].values():
            if not isinstance(v, (int, float)) or v < 0:
                return False
        return True

    def validate_input(self, data, validators):
        """Validate input data against validators."""
        if not isinstance(data, dict):
            raise ValidationError("Input must be a dictionary")
            
        for key, validator in validators.items():
            if key not in data:
                raise ValidationError(f"Missing required input: {key}")
            if not validator(data[key]):
                raise ValidationError(f"Invalid input for {key}")
                
        return True

    def update_view_from_state(self):
        """Update view from state."""
        try:
            super().update_view_from_state()
            if not self.app:
                self.app = App.get_running_app()
            
            # Get game state
            game_state = self.app.game_state
            self.winner_name = game_state.get('winner_name', '')
            self.winner_score = game_state.get('winner_score', 0)
            self.loser_name = game_state.get('loser_name', '')
            self.loser_score = game_state.get('loser_score', 0)
            self.game_duration = game_state.get('game_duration', '00:00:00')
            self.victory_type = game_state.get('victory_type', '')
            
            # Update scores
            self.scores['p1'] = self.p1_primary_score + self.p1_secondary_score
            self.scores['p2'] = self.p2_primary_score + self.p2_secondary_score
            
            # Update final scores text
            self.final_scores_text = f"{self.p1_name}: {self.scores['p1']} - {self.p2_name}: {self.scores['p2']}"
            
            # Update UI
            self.update_ui()
            self.error_label.text = self._current_error or ""
            self.total_time_label.text = "00:00:00"
        except Exception as e:
            self.handle_winner_determination_error()

    def update_ui(self):
        """Update UI elements."""
        try:
            if hasattr(self, 'ids'):
                if 'winner_label' in self.ids:
                    self.ids.winner_label.text = f"Winner: {self.winner}" if self.winner else "No winner"
                if 'scores_list' in self.ids:
                    self.ids.scores_list.clear_widgets()
                    for score in self.final_scores:
                        self.ids.scores_list.add_widget(score)
                if 'p1_final_score_label' in self.ids:
                    self.ids.p1_final_score_label.text = str(self.scores['p1'])
                if 'p2_final_score_label' in self.ids:
                    self.ids.p2_final_score_label.text = str(self.scores['p2'])
                if 'error_label' in self.ids:
                    if self.has_error:
                        self.ids.error_label.opacity = 1
                    else:
                        self.ids.error_label.opacity = 0
                    self.error_label.text = self._current_error or ""
                if 'total_time_label' in self.ids:
                    self.total_time_label.text = "00:00:00"
        except Exception as e:
            self.handle_winner_determination_error()

    def start_sync(self):
        """Start synchronization."""
        try:
            self.is_syncing = True
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in start_sync: {str(e)}")
            self.handle_winner_determination_error()

    def stop_sync(self):
        """Stop synchronization."""
        try:
            self.is_syncing = False
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in stop_sync: {str(e)}")
            self.handle_winner_determination_error()

    def handle_client_update(self, update):
        """Handle client update."""
        try:
            if not isinstance(update, dict):
                raise ValidationError("Update must be a dictionary")
                
            if 'type' not in update:
                raise ValidationError("Update must have a type")
                
            if update['type'] == 'scores':
                if 'scores' not in update:
                    raise ValidationError("Scores update must include scores")
                self.update_scores(update['scores'])
            else:
                raise ValidationError("Invalid update type")
                
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            self.show_error(f"Error in handle_client_update: {str(e)}")

    def validate_winner(self, winner):
        """Validate winner."""
        try:
            if not isinstance(winner, str):
                return False
            if winner not in ["Player1", "Player2", ""]:
                return False
            return True
        except Exception as e:
            logger.error(f"Error in validate_winner: {str(e)}")
            return False

    def handle_winner_determination_error(self):
        self.show_error("Critical error in winner validation")

    def load_game_state(self):
        """Load game state from app."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            self.winner = self.app.game_state.get('winner', '')
            scores = self.app.game_state.get('scores', {})
            # Always generate final_scores from scores if not present
            if 'final_scores' in self.app.game_state:
                self.final_scores = self.app.game_state.get('final_scores', [])
            else:
                self.final_scores = [
                    {'name': str(player), 'score': int(score)}
                    for player, score in scores.items()
                ]
            self.show_winner = bool(self.winner)
            self.show_scores = bool(self.final_scores)
        except Exception as e:
            self.logger.error(f"Error in load_game_state: {str(e)}")
            self.handle_state_error()

    def handle_state_error(self):
        """Handle state loading error."""
        try:
            self.has_error = True
            self._current_error = "Error loading game state"
            self.logger.error("State loading error")
        except Exception as e:
            self.logger.error(f"Error in handle_state_error: {str(e)}")

    def reset(self):
        """Reset screen state."""
        self.has_error = False
        self._current_error = None
        self.winner = ''
        self.final_scores = []
        self.show_winner = False
        self.show_scores = False
        self.is_syncing = False
        self.is_loading = False
        self.scores = {}  # Reset to empty dict
        # Do not call update_ui or any method that could trigger error logic on empty state

    def return_to_menu(self):
        """Return to main menu."""
        self.manager.current = 'resume_or_new' 