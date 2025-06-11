from kivy.app import App
from kivy.uix.screenmanager import Screen
from widgets.number_pad_popup import NumberPadPopup
from widgets.concede_confirm_popup import ConcedeConfirmPopup
from kivy.clock import Clock
import time
import logging
from state.game_state import GameStatus

class ScoreboardScreen(Screen):
    timer_event = None

    def on_enter(self):
        """Called when the screen is shown. Sets up the initial scoreboard view and starts the timer update."""
        self.update_view_from_state()
        self.start_timer_update()

    def on_leave(self):
        """Called when the screen is left. Unschedule the timer update."""
        self.stop_timer_update()

    def start_timer_update(self):
        if self.timer_event is None:
            self.timer_event = Clock.schedule_interval(self.update_timer_label, 1)

    def stop_timer_update(self):
        if self.timer_event is not None:
            self.timer_event.cancel()
            self.timer_event = None

    def update_timer_label(self, dt=None):
        app = App.get_running_app()
        state = app.game_state
        total_seconds = state.get('timer_accumulated_seconds', 0)
        if state.get('timer_is_running', False):
            total_seconds += int(time.time() - state.get('timer_start_time_unix', 0))
        self.ids.total_time_label.text = self.format_time(total_seconds)

    def format_time(self, seconds):
        seconds = int(seconds)
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02}:{m:02}:{s:02}"  # 01:23:45

    def update_view_from_state(self):
        """Refreshes the entire UI from the central game_state."""
        app = App.get_running_app()
        state = app.game_state

        # Calculate total scores
        p1_total_score = state.get('p1_primary_score', 0) + state.get('p1_secondary_score', 0)
        p2_total_score = state.get('p2_primary_score', 0) + state.get('p2_secondary_score', 0)

        # Populate Player 1 info
        self.ids.p1_name_label.text = state.get('p1_name', 'Player 1')
        self.ids.p1_total_score_label.text = str(p1_total_score)
        self.ids.p1_cp_label.text = str(state.get('p1_cp', 0))

        # Populate Player 2 info
        self.ids.p2_name_label.text = state.get('p2_name', 'Player 2')
        self.ids.p2_total_score_label.text = str(p2_total_score)
        self.ids.p2_cp_label.text = str(state.get('p2_cp', 0))
        
        # Update header and End Turn button visibility
        current_player_name = state.get('current_player_name', '')
        current_round = state.get('current_round', 1)
        self.ids.header.text = f"{current_player_name}'s Turn - Round {current_round}"

        if current_player_name == state.get('p1_name'):
            self.ids.p1_end_turn_button.opacity = 1
            self.ids.p1_end_turn_button.disabled = False
            self.ids.p2_end_turn_button.opacity = 0
            self.ids.p2_end_turn_button.disabled = True
        else:
            self.ids.p1_end_turn_button.opacity = 0
            self.ids.p1_end_turn_button.disabled = True
            self.ids.p2_end_turn_button.opacity = 1
            self.ids.p2_end_turn_button.disabled = False

    def open_score_popup(self, player, objective_type):
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

    def show_number_pad(self, objective_type, player):
        """Opens a number pad popup to set a score."""
        self.open_score_popup(player, objective_type)

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