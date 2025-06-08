from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from widgets.number_pad_popup import NumberPadPopup

class ScoreboardScreen(Screen):
    # Player 1 UI elements
    p1_name_label = ObjectProperty(None)
    p1_total_score_label = ObjectProperty(None)
    p1_cp_label = ObjectProperty(None)
    p1_end_turn_button = ObjectProperty(None)
    
    # Player 2 UI elements
    p2_name_label = ObjectProperty(None)
    p2_total_score_label = ObjectProperty(None)
    p2_cp_label = ObjectProperty(None)
    p2_end_turn_button = ObjectProperty(None)

    # Shared UI elements
    header = ObjectProperty(None)

    def on_enter(self):
        """Called when the screen is shown. Sets up the initial scoreboard view."""
        self.update_view_from_state()

    def update_view_from_state(self):
        """Refreshes the entire UI from the central game_state."""
        app = App.get_running_app()
        state = app.game_state

        # Calculate total scores
        p1_total_score = state.get('p1_primary_score', 0) + state.get('p1_secondary_score', 0)
        p2_total_score = state.get('p2_primary_score', 0) + state.get('p2_secondary_score', 0)

        # Populate Player 1 info
        self.p1_name_label.text = state.get('p1_name', 'Player 1')
        self.p1_total_score_label.text = str(p1_total_score)
        self.p1_cp_label.text = str(state.get('p1_cp', 0))

        # Populate Player 2 info
        self.p2_name_label.text = state.get('p2_name', 'Player 2')
        self.p2_total_score_label.text = str(p2_total_score)
        self.p2_cp_label.text = str(state.get('p2_cp', 0))
        
        # Update header and End Turn button visibility
        current_player_name = state.get('current_player_name', '')
        current_round = state.get('current_round', 1)
        self.header.title = f"{current_player_name}'s Turn - Round {current_round}"

        if current_player_name == state.get('p1_name'):
            self.p1_end_turn_button.opacity = 1
            self.p1_end_turn_button.disabled = False
            self.p2_end_turn_button.opacity = 0
            self.p2_end_turn_button.disabled = True
        else:
            self.p1_end_turn_button.opacity = 0
            self.p1_end_turn_button.disabled = True
            self.p2_end_turn_button.opacity = 1
            self.p2_end_turn_button.disabled = False

    def open_score_popup(self, player, objective_type):
        """Opens a number pad popup to set a score."""
        app = App.get_running_app()
        
        def on_confirm(value):
            app.set_objective_score(player, objective_type, value)
            self.update_view_from_state()

        current_score_key = f"p{player}_{objective_type}_score"
        current_score = app.game_state.get(current_score_key, 0)

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

    def end_turn(self):
        """Handles the end of a player's turn."""
        app = App.get_running_app()
        app.end_turn()
        self.update_view_from_state() 