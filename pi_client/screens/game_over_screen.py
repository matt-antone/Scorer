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
    
    # State manager
    state = ObjectProperty(None)

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
        self.state = GameOverState()
        if not self.children:
            self.add_widget(Label(text='GameOverScreen loaded (no KV)'))
        if not self.game_duration:
            self.game_duration = '00:00'

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
        # Register as observer
        if self.state_manager:
            self.state_manager.register_observer(self)
        self.load_game_state()
        self.update_ui()

    def on_leave(self):
        """Called when leaving the screen."""
        # Unregister as observer
        if self.state_manager:
            self.state_manager.unregister_observer(self)
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
        """Clean up the game state after game over."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            
            # Save game history if needed
            if self.save_game:
                self.game_history.append({
                    'winner': self.winner,
                    'scores': self.scores,
                    'duration': self.game_duration,
                    'victory_type': self.victory_type
                })
                self.app.game_state['game_history'] = self.game_history
            
            # Reset game state
            self.app.game_state.update({
                'p1_name': '',
                'p2_name': '',
                'p1_primary_score': 0,
                'p2_primary_score': 0,
                'p1_secondary_score': 0,
                'p2_secondary_score': 0,
                'p1_cp': 0,
                'p2_cp': 0,
                'winner': 0,
                'current_round': 1,
                'game_phase': 'setup'
            })
            
            # Reset screen state
            self.reset_screen()
            
        except Exception as e:
            logger.error(f"Error in cleanup_game_state: {str(e)}")
            self.handle_cleanup_error()

    def handle_cleanup_error(self):
        """Handle errors during game state cleanup."""
        try:
            self.has_error = True
            self.show_error("Error cleaning up game state")
            self.cleanup_required = False
            self.update_ui()
        except Exception as e:
            logger.error(f"Error in handle_cleanup_error: {str(e)}")
            self.show_error("Critical error in cleanup")

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
        """Determine the winner based on scores."""
        try:
            if not self.scores or len(self.scores) < 2:
                self.scores = {'Player1': 0, 'Player2': 0}
            
            # Calculate total scores
            p1_total = self.p1_primary_score + self.p1_secondary_score
            p2_total = self.p2_primary_score + self.p2_secondary_score
            
            # Update scores dict
            self.scores[self.p1_name] = p1_total
            self.scores[self.p2_name] = p2_total
            
            # Determine winner
            if p1_total > p2_total:
                self.winner = self.p1_name
                self.winner_name = self.p1_name
                self.winner_score = p1_total
                self.loser_name = self.p2_name
                self.loser_score = p2_total
                self.victory_type = 'Victory'
            elif p2_total > p1_total:
                self.winner = self.p2_name
                self.winner_name = self.p2_name
                self.winner_score = p2_total
                self.loser_name = self.p1_name
                self.loser_score = p1_total
                self.victory_type = 'Victory'
            else:
                self.winner = 'Tie'
                self.winner_name = 'Tie'
                self.winner_score = p1_total
                self.loser_name = 'Tie'
                self.loser_score = p2_total
                self.victory_type = 'Draw'
            
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
            
            # Update UI
            self.update_ui()
            return True
        except Exception as e:
            logger.error(f"Error in determine_winner: {str(e)}")
            self.handle_winner_determination_error()
            return False

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
                # Update winner label
                if 'winner_label' in self.ids:
                    if self.winner == 'Tie':
                        self.ids.winner_label.text = "Game Ended in a Tie!"
                    else:
                        self.ids.winner_label.text = f"{self.winner} Wins!"
                
                # Update player names
                if 'p1_name_label' in self.ids:
                    self.ids.p1_name_label.text = self.p1_name
                if 'p2_name_label' in self.ids:
                    self.ids.p2_name_label.text = self.p2_name
                
                # Update scores
                if 'p1_final_score_label' in self.ids:
                    p1_total = self.p1_primary_score + self.p1_secondary_score
                    self.ids.p1_final_score_label.text = str(p1_total)
                if 'p2_final_score_label' in self.ids:
                    p2_total = self.p2_primary_score + self.p2_secondary_score
                    self.ids.p2_final_score_label.text = str(p2_total)
                
                # Update game duration
                if 'total_time_label' in self.ids:
                    self.ids.total_time_label.text = self.game_duration
                
                # Update error label
                if 'error_label' in self.ids:
                    if self.has_error:
                        self.ids.error_label.opacity = 1
                        self.ids.error_label.text = self._current_error or "An error occurred"
                    else:
                        self.ids.error_label.opacity = 0
                        self.ids.error_label.text = ""
            
            # Update final scores text
            self.final_scores_text = f"{self.p1_name}: {self.p1_primary_score + self.p1_secondary_score} - {self.p2_name}: {self.p2_primary_score + self.p2_secondary_score}"
            
            return True
        except Exception as e:
            logger.error(f"Error in update_ui: {str(e)}")
            self.handle_winner_determination_error()
            return False

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

    def reset_screen(self):
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

    def on_state_update(self, state):
        """Handle state updates from the state manager."""
        self.logger.debug(f"[GameOverScreen] Received state update: {state}")
        self.p1_name = state.get('p1_name', '')
        self.p2_name = state.get('p2_name', '')
        self.p1_primary_score = state.get('p1_primary_score', 0)
        self.p2_primary_score = state.get('p2_primary_score', 0)
        self.p1_secondary_score = state.get('p1_secondary_score', 0)
        self.p2_secondary_score = state.get('p2_secondary_score', 0)
        self.p1_cp = state.get('p1_cp', 0)
        self.p2_cp = state.get('p2_cp', 0)
        self.winner = state.get('winner', '')
        self.scores = state.get('scores', {})
        self.final_scores = state.get('final_scores', [])
        self.update_ui()

    def handle_winner_determination_error(self, error_msg=None):
        """Handle errors during winner determination."""
        try:
            if error_msg is None:
                error_msg = "Unable to determine winner"
            
            self.has_error = True
            self._current_error = error_msg
            
            if hasattr(self, 'ids') and 'error_label' in self.ids:
                self.ids.error_label.text = error_msg
                self.ids.error_label.opacity = 1
            
            # Update game state
            if self.app:
                self.app.game_state['error'] = error_msg
            
            return False
        except Exception as e:
            logger.error(f"Error in handle_winner_determination_error: {str(e)}")
            return False

    def update_ui(self):
        # ... existing code ...
        # Only call handle_winner_determination_error if not already in error state
        if not self.has_error:
            # ... existing code ...
            # If error condition detected:
            # self.handle_winner_determination_error("Some error")
            pass
        # ... existing code ... 