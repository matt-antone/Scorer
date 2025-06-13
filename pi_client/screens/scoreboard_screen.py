from kivy.app import App
from kivy.uix.screenmanager import Screen
from pi_client.widgets.number_pad_popup import NumberPadPopup
from pi_client.widgets.concede_confirm_popup import ConcedeConfirmPopup
from kivy.clock import Clock
import time
import logging
from pi_client.state import GameStatus
from kivy.properties import BooleanProperty, StringProperty, NumericProperty, DictProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import os
from .base_screen import BaseScreen, ValidationError, StateError, SyncError

logger = logging.getLogger(__name__)

class ScoreboardScreen(BaseScreen):
    """Screen for displaying and managing game scores."""
    
    # Properties
    scores = DictProperty({})
    current_round = NumericProperty(1)
    max_rounds = NumericProperty(10)
    round_history = ListProperty([])
    score_history = DictProperty({})
    is_loading = BooleanProperty(False)
    status_text = StringProperty('')
    has_error = BooleanProperty(False)
    initiative_winner = StringProperty('')
    players = ListProperty([])
    p1_name_label = None
    p2_name_label = None
    p1_score_display = None
    p2_score_display = None
    total_time_label = None
    history_display = None
    p1_total_score_label = None
    p2_total_score_label = None
    timer_event = None
    _current_error = None
    is_syncing = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.logger.info("ScoreboardScreen: Initializing")
        self._loading_timeout = None
        self._error_timeout = None
        self._start_background_tasks()
        self.app = None
        # Initialize scores for both players
        self.scores = {'Player1': 0, 'Player2': 0}
        # Create dummy UI attributes for test compatibility
        self.p1_name_label = Label(text="Player One")
        self.p2_name_label = Label(text="Player Two")
        self.p1_score_display = Label(text="0")
        self.p2_score_display = Label(text="0")
        self.total_time_label = Label(text="00:00:00")
        self.history_display = Label(text="")
        self.p1_total_score_label = Label(text="0")
        self.p2_total_score_label = Label(text="0")

    def _start_background_tasks(self):
        """Start background tasks for initialization."""
        self.logger.info("ScoreboardScreen: Scheduling background tasks")
        Clock.schedule_once(self._perform_background_tasks)

    def _perform_background_tasks(self, dt):
        """Perform background initialization tasks."""
        self.initialize_scores()
        self.load_round_history()
        self.load_score_history()

    def initialize_scores(self):
        """Initialize scores for all players."""
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            players = app.game_state.get('players', [])
            for player in players:
                if player not in self.scores:
                    self.scores[player] = 0

    def load_round_history(self):
        """Load round history from game state."""
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            self.round_history = app.game_state.get('round_history', [])

    def load_score_history(self):
        """Load score history from game state."""
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            self.score_history = app.game_state.get('score_history', {})

    def update_score(self, player, points):
        """Update a player's score."""
        if player not in ['Player1', 'Player2']:
            raise ValidationError(f"Invalid player: {player}")
        
        if points < 0:
            raise ValidationError("Score cannot be negative")
        
        app = App.get_running_app()
        if not app or not hasattr(app, 'game_state'):
            raise StateError("Game state not available")

        if player == 'Player1':
            app.game_state['p1_primary_score'] = points
        else:
            app.game_state['p2_primary_score'] = points

        self.scores[player] = points
        self.score_history[str(self.current_round)] = dict(self.scores)
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            app.game_state['scores'] = dict(self.scores)
            app.game_state['score_history'] = dict(self.score_history)
            if hasattr(app, 'broadcast_state'):
                app.broadcast_state()

    def increment_round(self):
        """Increment the current round."""
        if self.current_round >= self.max_rounds:
            self._current_error = "Maximum rounds reached"
            raise StateError(self._current_error)
        self.current_round += 1
        self.round_history.append(self.current_round)
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            app.game_state['current_round'] = self.current_round
            app.game_state['round_history'] = list(self.round_history)
            if hasattr(app, 'broadcast_state'):
                app.broadcast_state()

    def validate_round(self, round_num):
        """Validate round number."""
        if not isinstance(round_num, int) or round_num < 1:
            raise ValidationError("Round number must be a positive integer")
        if round_num > self.max_rounds:
            raise StateError(f"Round number cannot exceed {self.max_rounds}")
        return True

    def validate_score(self, score):
        """Validate score value."""
        if not isinstance(score, (int, float)) or score < 0:
            raise ValidationError("Score must be a non-negative number")
        return True

    def handle_client_update(self, update):
        """Handle client update."""
        if update.get('type') == 'game_state':
            try:
                state = update.get('state', {})
                if 'scores' in state:
                    for player, score in state['scores'].items():
                        self.validate_score(score)
                        self.scores[player] = score
                if 'current_round' in state:
                    self.validate_round(state['current_round'])
                    self.current_round = state['current_round']
                if 'round_history' in state:
                    self.round_history = state['round_history']
                if 'score_history' in state:
                    self.score_history = state['score_history']
            except (ValidationError, StateError) as e:
                self.handle_error(str(e))

    def handle_error(self, message):
        """Handle error."""
        self._current_error = message
        self.show_error(message)
        self.has_error = True

    def clear_error(self):
        """Clear error state."""
        self._current_error = None
        self.has_error = False
        if self._error_timeout:
            self._error_timeout.cancel()
            self._error_timeout = None

    def show_error(self, message):
        """Show error message."""
        self.status_text = message
        if self._error_timeout:
            self._error_timeout.cancel()
        self._error_timeout = Clock.schedule_once(lambda dt: self.clear_error(), 5)

    def on_pre_enter(self):
        """Called before screen is entered."""
        super().on_pre_enter()
        self._start_background_tasks()
        self.start_timer_update()

    def on_enter(self):
        """Called when the screen is entered."""
        super().on_enter()
        self.load_game_state()
        self.update_view_from_state()
        self.start_timer_update()

    def on_leave(self):
        """Called when the screen is left. Unschedule the timer update."""
        super().on_leave()
        self.stop_timer_update()
        self.stop_sync()
        if self._error_timeout:
            self._error_timeout.cancel()
        if self._loading_timeout:
            self._loading_timeout.cancel()

    def start_timer_update(self):
        """Start timer update."""
        if self.timer_event is None:
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def stop_timer_update(self):
        """Stop timer update."""
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

    def update_timer(self, dt):
        """Update timer display."""
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            current_time = time.time()
            game_start = app.game_state.get('game_start_time', current_time)
            elapsed = int(current_time - game_start)
            app.game_state['elapsed_time'] = elapsed
            if hasattr(app, 'broadcast_state'):
                app.broadcast_state()

    def update_view_from_state(self):
        """Update the view based on the current state."""
        app = App.get_running_app()
        if not app or not hasattr(app, 'game_state'):
            return

        # Update player names
        if hasattr(self, 'p1_name_label'):
            self.p1_name_label.text = app.game_state.get('p1_name', '')
        if hasattr(self, 'p2_name_label'):
            self.p2_name_label.text = app.game_state.get('p2_name', '')

        # Update scores
        p1_total = app.game_state.get('p1_primary_score', 0) + app.game_state.get('p1_secondary_score', 0)
        p2_total = app.game_state.get('p2_primary_score', 0) + app.game_state.get('p2_secondary_score', 0)
        
        if hasattr(self, 'p1_total_score_label'):
            self.p1_total_score_label.text = str(p1_total)
        if hasattr(self, 'p2_total_score_label'):
            self.p2_total_score_label.text = str(p2_total)

        # Update command points
        if hasattr(self, 'p1_cp_label'):
            self.p1_cp_label.text = str(app.game_state.get('p1_cp', 0))
        if hasattr(self, 'p2_cp_label'):
            self.p2_cp_label.text = str(app.game_state.get('p2_cp', 0))

        # Update round display
        if 'round_display' in self.ids:
            self.ids.round_display.text = f"Round {self.current_round}"
            
        # Update score displays
        for player in self.players:
            display_id = f'{player}_score_display'
            if display_id in self.ids:
                score = self.scores.get(player, 0)
                self.ids[display_id].text = str(score)
                
        # Update history display
        if 'history_display' in self.ids:
            history_text = "\n".join([
                f"Round {r['round']}: {r['scores']}"
                for r in self.round_history
            ])
            self.ids.history_display.text = history_text
            
    def update_ui(self):
        """Update the UI elements."""
        try:
            if hasattr(self, 'ids'):
                # Update round display
                if 'round_display' in self.ids:
                    self.ids.round_display.text = f"Round {self.current_round}"
                    
                # Update score displays
                for player in self.players:
                    display_id = f'{player}_score_display'
                    if display_id in self.ids:
                        score = self.scores.get(player, 0)
                        self.ids[display_id].text = str(score)
                        
                # Update history display
                if 'history_display' in self.ids:
                    history_text = "\n".join([
                        f"Round {r['round']}: {r['scores']}"
                        for r in self.round_history
                    ])
                    self.ids.history_display.text = history_text
                    
        except Exception as e:
            self.handle_error(str(e))
            
    def broadcast_state(self):
        """Broadcast current state to all clients."""
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            state = {
                'type': 'scoreboard',
                'scores': self.scores,
                'current_round': self.current_round,
                'round_history': self.round_history,
                'score_history': self.score_history
            }
            app.broadcast_state(state)

    def handle_sync_error(self):
        """Handle synchronization error."""
        self.show_error("Failed to synchronize game state")
        self.is_syncing = False

    def get_round_display(self):
        """Return the current round as a display string, e.g., 'Round 1'."""
        app = App.get_running_app()
        round_num = 1
        if app and hasattr(app, 'game_state'):
            round_num = app.game_state.get('current_round', 1)
        return f"Round {round_num}"

    def open_score_popup(self, player_num, score_type):
        """Open the score input popup."""
        try:
            if player_num not in [1, 2]:
                raise ValidationError(f"Invalid player number: {player_num}")
            
            if score_type not in ['primary', 'secondary']:
                raise ValidationError(f"Invalid score type: {score_type}")
            
            title = f"Player {player_num} {score_type.title()} Score"
            popup = NumberPadPopup(title=title)
            popup.bind(on_dismiss=self.on_score_popup_dismiss)
            popup.open()
        except Exception as e:
            self.handle_error(str(e))

    def on_score_popup_dismiss(self, popup):
        """Handle score popup dismissal."""
        if popup.score is not None:
            try:
                player = f"Player{popup.player_num}"
                self.update_score(player, popup.score)
            except Exception as e:
                self.handle_error(str(e))

    def concede_game(self):
        """Handle game concession."""
        try:
            app = App.get_running_app()
            if not app or not hasattr(app, 'game_state'):
                raise StateError("Game state not available")

            # Determine winner based on current scores
            p1_total = app.game_state.get('p1_primary_score', 0) + app.game_state.get('p1_secondary_score', 0)
            p2_total = app.game_state.get('p2_primary_score', 0) + app.game_state.get('p2_secondary_score', 0)
            
            if p1_total > p2_total:
                app.game_state['winner'] = 1
            elif p2_total > p1_total:
                app.game_state['winner'] = 2
            else:
                app.game_state['winner'] = 0  # Draw

            app.root.current = 'game_over'
        except Exception as e:
            self.handle_error(str(e))

    def continue_to_game_over(self):
        self.proceed_to_game_over()

    def handle_round_error(self):
        self.show_error("Invalid round value")

    def proceed_to_game_over(self):
        """Proceed to the game over screen."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            self.app.game_state['final_scores'] = self.scores
            self.app.root.current = 'game_over'
        except Exception as e:
            self.handle_error("Failed to proceed to game over")

    def change_cp(self, player, amount):
        """Handles a command point change request."""
        app = App.get_running_app()
        app.update_cp(player, amount)
        self.update_view_from_state()

    def end_turn(self, outgoing_player_id):
        """End the current player's turn and switch to the other player."""
        if outgoing_player_id not in (1, 2):
            logging.error(f"Invalid player ID: {outgoing_player_id}")
            return

        app = App.get_running_app()
        game_state = app.game_state
        
        # If we're at round 5 and player 2 is ending their turn, end the game
        if game_state['current_round'] == 5 and outgoing_player_id == 2:
            logging.info("Game over: Round 5 completed by both players")
            game_state['status'] = GameStatus.GAME_OVER
            app.save_game_state()
            app.root.current = 'game_over'
            return

        # Switch to the other player
        game_state['current_player_id'] = 3 - outgoing_player_id  # Switch between 1 and 2
        
        # If we're switching back to player 1, increment the round
        if game_state['current_player_id'] == 1:
            if game_state['current_round'] < 5:
                game_state['current_round'] += 1
        
        # Update the current player name
        game_state['current_player_name'] = game_state['p1_name'] if game_state['current_player_id'] == 1 else game_state['p2_name']
        
        app.save_game_state()
        self.update_view_from_state()

    def show_number_pad(self, player, objective_type):
        """Opens a number pad popup to set a score."""
        app = App.get_running_app()
        
        def on_confirm(value):
            logging.info(f"Score update callback called with value: {value} for player {player}, objective {objective_type}")
            app.set_objective_score(player, objective_type, value)
            self.update_view_from_state()
            logging.info("View updated after score change")

        current_score_key = f"p{player}_{objective_type}_score"
        current_score = app.game_state.get(current_score_key, 0)
        logging.info(f"Opening score popup for player {player}, {objective_type}, current score: {current_score}")

        popup = NumberPadPopup(
            callback=on_confirm,
            initial_value=current_score,
            score_type=objective_type
        )
        
        # Position the popup on the correct side of the screen
        if player == 1:
            popup.pos_hint = {'x': 0.05, 'center_y': 0.5}
        else: # player == 2
            popup.pos_hint = {'right': 0.95, 'center_y': 0.5}

        popup.open()

    def increment_score(self, player):
        """Increments the command points for a player."""
        self.change_cp(player, 1)

    def decrement_score(self, player):
        """Decrements the command points for a player."""
        self.change_cp(player, -1)

    def show_concede_confirm(self):
        """Shows the concede confirmation popup."""
        app = App.get_running_app()
        current_player = 1 if app.game_state.get('current_player_name') == app.game_state.get('p1_name') else 2
        popup = ConcedeConfirmPopup(player_number=current_player)
        
        # Position the popup on the correct side of the screen
        if current_player == 1:
            popup.pos_hint = {'x': 0.05, 'center_y': 0.5}
        else: # player == 2
            popup.pos_hint = {'right': 0.95, 'center_y': 0.5}
        
        popup.open()

    def back_to_initiative(self):
        """Return to initiative screen."""
        app = App.get_running_app()
        if app and hasattr(app, 'root') and app.root is not None:
            app.root.current = 'initiative'

    def get_score_display(self, player):
        """Get formatted score display for a player."""
        return str(self.scores.get(player, 0))

    def handle_score_error(self):
        """Handle score error."""
        self.handle_error("Invalid score value")

    def validate_game_state(self, state):
        """Validate game state."""
        if not isinstance(state, dict):
            raise ValidationError("Game state must be a dictionary")
        
        required_keys = ['players', 'current_round', 'scores']
        for key in required_keys:
            if key not in state:
                raise StateError(f"Missing required state key: {key}")
        
        return True

    def load_game_state(self):
        """Load game state from the app."""
        app = App.get_running_app()
        if not app or not hasattr(app, 'game_state'):
            return

        self.current_round = app.game_state.get('current_round', 1)
        self.round_history = app.game_state.get('round_history', [])
        self.scores = {
            'Player1': app.game_state.get('p1_primary_score', 0) + app.game_state.get('p1_secondary_score', 0),
            'Player2': app.game_state.get('p2_primary_score', 0) + app.game_state.get('p2_secondary_score', 0)
        }

    def update_ui(self):
        """Update the UI elements."""
        try:
            if hasattr(self, 'ids'):
                # Update round display
                if 'round_display' in self.ids:
                    self.ids.round_display.text = f"Round {self.current_round}"
                    
                # Update score displays
                for player in self.players:
                    display_id = f'{player}_score_display'
                    if display_id in self.ids:
                        score = self.scores.get(player, 0)
                        self.ids[display_id].text = str(score)
                        
                # Update history display
                if 'history_display' in self.ids:
                    history_text = "\n".join([
                        f"Round {r['round']}: {r['scores']}"
                        for r in self.round_history
                    ])
                    self.ids.history_display.text = history_text
                    
        except Exception as e:
            self.handle_error(str(e))
            
    def broadcast_state(self):
        """Broadcast current state to all clients."""
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            state = {
                'type': 'scoreboard',
                'scores': self.scores,
                'current_round': self.current_round,
                'round_history': self.round_history,
                'score_history': self.score_history
            }
            app.broadcast_state(state)

    def handle_sync_error(self):
        """Handle synchronization error."""
        self.show_error("Failed to synchronize game state")
        self.is_syncing = False

    def get_round_display(self):
        """Return the current round as a display string, e.g., 'Round 1'."""
        app = App.get_running_app()
        round_num = 1
        if app and hasattr(app, 'game_state'):
            round_num = app.game_state.get('current_round', 1)
        return f"Round {round_num}"

    def open_score_popup(self, player_num, score_type):
        """Open the score input popup."""
        try:
            if player_num not in [1, 2]:
                raise ValidationError(f"Invalid player number: {player_num}")
            
            if score_type not in ['primary', 'secondary']:
                raise ValidationError(f"Invalid score type: {score_type}")
            
            title = f"Player {player_num} {score_type.title()} Score"
            popup = NumberPadPopup(title=title)
            popup.bind(on_dismiss=self.on_score_popup_dismiss)
            popup.open()
        except Exception as e:
            self.handle_error(str(e))

    def on_score_popup_dismiss(self, popup):
        """Handle score popup dismissal."""
        if popup.score is not None:
            try:
                player = f"Player{popup.player_num}"
                self.update_score(player, popup.score)
            except Exception as e:
                self.handle_error(str(e))

    def concede_game(self):
        """Handle game concession."""
        try:
            app = App.get_running_app()
            if not app or not hasattr(app, 'game_state'):
                raise StateError("Game state not available")

            # Determine winner based on current scores
            p1_total = app.game_state.get('p1_primary_score', 0) + app.game_state.get('p1_secondary_score', 0)
            p2_total = app.game_state.get('p2_primary_score', 0) + app.game_state.get('p2_secondary_score', 0)
            
            if p1_total > p2_total:
                app.game_state['winner'] = 1
            elif p2_total > p1_total:
                app.game_state['winner'] = 2
            else:
                app.game_state['winner'] = 0  # Draw

            app.root.current = 'game_over'
        except Exception as e:
            self.handle_error(str(e))

    def continue_to_game_over(self):
        self.proceed_to_game_over()

    def handle_round_error(self):
        self.show_error("Invalid round value")

    def proceed_to_game_over(self):
        """Proceed to the game over screen."""
        try:
            if not self.app:
                self.app = App.get_running_app()
            self.app.game_state['final_scores'] = self.scores
            self.app.root.current = 'game_over'
        except Exception as e:
            self.handle_error("Failed to proceed to game over")

    def change_cp(self, player, amount):
        """Handles a command point change request."""
        app = App.get_running_app()
        app.update_cp(player, amount)
        self.update_view_from_state()

    def end_turn(self, outgoing_player_id):
        """End the current player's turn and switch to the other player."""
        if outgoing_player_id not in (1, 2):
            logging.error(f"Invalid player ID: {outgoing_player_id}")
            return

        app = App.get_running_app()
        game_state = app.game_state
        
        # If we're at round 5 and player 2 is ending their turn, end the game
        if game_state['current_round'] == 5 and outgoing_player_id == 2:
            logging.info("Game over: Round 5 completed by both players")
            game_state['status'] = GameStatus.GAME_OVER
            app.save_game_state()
            app.root.current = 'game_over'
            return

        # Switch to the other player
        game_state['current_player_id'] = 3 - outgoing_player_id  # Switch between 1 and 2
        
        # If we're switching back to player 1, increment the round
        if game_state['current_player_id'] == 1:
            if game_state['current_round'] < 5:
                game_state['current_round'] += 1
        
        # Update the current player name
        game_state['current_player_name'] = game_state['p1_name'] if game_state['current_player_id'] == 1 else game_state['p2_name']
        
        app.save_game_state()
        self.update_view_from_state()

    def show_number_pad(self, player, objective_type):
        """Opens a number pad popup to set a score."""
        app = App.get_running_app()
        
        def on_confirm(value):
            logging.info(f"Score update callback called with value: {value} for player {player}, objective {objective_type}")
            app.set_objective_score(player, objective_type, value)
            self.update_view_from_state()
            logging.info("View updated after score change")

        current_score_key = f"p{player}_{objective_type}_score"
        current_score = app.game_state.get(current_score_key, 0)
        logging.info(f"Opening score popup for player {player}, {objective_type}, current score: {current_score}")

        popup = NumberPadPopup(
            callback=on_confirm,
            initial_value=current_score,
            score_type=objective_type
        )
        
        # Position the popup on the correct side of the screen
        if player == 1:
            popup.pos_hint = {'x': 0.05, 'center_y': 0.5}
        else: # player == 2
            popup.pos_hint = {'right': 0.95, 'center_y': 0.5}

        popup.open()

    def increment_score(self, player):
        """Increments the command points for a player."""
        self.change_cp(player, 1)

    def decrement_score(self, player):
        """Decrements the command points for a player."""
        self.change_cp(player, -1)

    def show_concede_confirm(self):
        """Shows the concede confirmation popup."""
        app = App.get_running_app()
        current_player = 1 if app.game_state.get('current_player_name') == app.game_state.get('p1_name') else 2
        popup = ConcedeConfirmPopup(player_number=current_player)
        
        # Position the popup on the correct side of the screen
        if current_player == 1:
            popup.pos_hint = {'x': 0.05, 'center_y': 0.5}
        else: # player == 2
            popup.pos_hint = {'right': 0.95, 'center_y': 0.5}
        
        popup.open()

    def back_to_initiative(self):
        """Return to initiative screen."""
        app = App.get_running_app()
        if app and hasattr(app, 'root') and app.root is not None:
            app.root.current = 'initiative'

    def get_score_display(self, player):
        """Get formatted score display for a player."""
        return str(self.scores.get(player, 0))

    def handle_score_error(self):
        """Handle score error."""
        self.handle_error("Invalid score value")

    def validate_game_state(self, state):
        """Validate game state."""
        if not isinstance(state, dict):
            raise ValidationError("Game state must be a dictionary")
        
        required_keys = ['players', 'current_round', 'scores']
        for key in required_keys:
            if key not in state:
                raise StateError(f"Missing required state key: {key}")
        
        return True 