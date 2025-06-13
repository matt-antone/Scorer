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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.logger.info("GameOverScreen: Initializing")
        self.app = App.get_running_app()
        self.scores = {'p1': 0, 'p2': 0}
        self._error_timeout = None
        self._current_error = ''
        self.error_label = Label(text="")
        self.total_time_label = Label(text="00:00:00")
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
        super().on_enter()
        self.update_view_from_state()

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
        """Update the scores with new values."""
        try:
            self.validate_input(new_scores, {
                'score': lambda x: isinstance(x, (int, float)) and x >= 0
            })
            self.scores.update(new_scores)
            self.determine_winner()
        except Exception as e:
            self.handle_score_validation_error()

    def determine_winner(self):
        """Determine the winner based on scores."""
        try:
            if not self.scores or len(self.scores) < 2:
                self.scores = {'Player1': 0, 'Player2': 0}
            max_score = max(self.scores.values())
            winners = [p for p, s in self.scores.items() if s == max_score]
            self.winner = winners[0] if winners else ''
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

    def validate_state(self, required_keys=None):
        """Validate the current state."""
        if required_keys is None:
            required_keys = [
                'players', 'scores', 'winner', 'game_history',
                'cleanup_required', 'save_game'
            ]
            
        for key in required_keys:
            if not hasattr(self, key):
                raise StateError(f"Missing required state key: {key}")
                
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
        """Updates the UI based on current state."""
        try:
            # Update final scores
            self.ids.p1_final_score_label.text = str(self.scores['p1'])
            self.ids.p2_final_score_label.text = str(self.scores['p2'])
            
            # Update winner label
            if self.winner == "Player1":
                self.ids.winner_label.text = f"{self.p1_name} Wins!"
            elif self.winner == "Player2":
                self.ids.winner_label.text = f"{self.p2_name} Wins!"
            else:
                self.ids.winner_label.text = "Draw!"
            
            # Update error state
            if self.has_error:
                self.ids.error_label.opacity = 1
            else:
                self.ids.error_label.opacity = 0
            self.error_label.text = self._current_error or ""
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
            if update['type'] == 'scores':
                scores = update['scores']
                if self.validate_scores(scores):
                    self.scores.update(scores)
                    self.update_ui()
            elif update['type'] == 'winner':
                winner = update['winner']
                if self.validate_winner(winner):
                    self.winner = winner
                    self.update_ui()
            else:
                raise ValidationError("Invalid update type")
        except Exception as e:
            logger.error(f"Error in handle_client_update: {str(e)}")
            self.handle_winner_determination_error()

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