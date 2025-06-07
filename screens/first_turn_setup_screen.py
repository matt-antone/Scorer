from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp

# Behavior of this screen (mirrors DeploymentSetupScreen):
# 1. Default visual state:
#   - Player names displayed.
#   - Roll buttons enabled.
#   - Status label shows initial roll instruction.
#   - Start Game button disabled.
#   - Roll displays are blank.
# 2. Button Visual States:
#   - Tapping roll button shows the number in the display label and disables the button.
#   - Winner's choice buttons appear after a winner is decided.
#   - Tapping choice button shows "First" or "Second" in the display label.
#   - Start Game button enabled only when first turn is decided.
# 3. Status Messages:
#   - "Roll for First Turn. Winner chooses who goes first." -> Initial state.
#   - "Tie! {attacker_name} (Attacker) chooses who goes first." -> Tie state.
#   - "Waiting for {player_name} to roll..." -> One player has rolled.
#   - "{winner_name} wins! Choose who takes the first turn." -> Winner decided.
#   - "{player_name} will take the first turn! Click 'Start Game' below." -> Turn decided.


class FirstTurnSetupScreen(Screen):
    # Player 1 UI
    p1_name_label = ObjectProperty(None)
    p1_ft_roll_button = ObjectProperty(None)
    p1_ft_roll_display_label = ObjectProperty(None)
    p1_ft_choice_box = ObjectProperty(None)

    # Player 2 UI
    p2_name_label = ObjectProperty(None)
    p2_ft_roll_button = ObjectProperty(None)
    p2_ft_roll_display_label = ObjectProperty(None)
    p2_ft_choice_box = ObjectProperty(None)

    # General UI
    first_turn_status_label = ObjectProperty(None)
    start_game_button = ObjectProperty(None)

    def on_pre_enter(self, *args):
        """Called every time the screen is shown. Does an initial draw."""
        self.update_view_from_state()

    def update_view_from_state(self, *args):
        """Updates the entire screen based on the central game_state."""
        app = App.get_running_app()
        if not app:
            return
        gs = app.game_state

        self.p1_name_label.text = gs['player1']['name']
        self.p2_name_label.text = gs['player2']['name']

        p1_roll = gs['player1'].get('first_turn_roll', 0)
        p2_roll = gs['player2'].get('first_turn_roll', 0)
        winner_id = gs.get('first_turn_initiative_winner_id')
        first_turn_player_id = gs.get('first_turn_player_id')

        # Clean state
        self.p1_ft_roll_button.text = "Roll"
        self.p2_ft_roll_button.text = "Roll"
        self.p1_ft_choice_box.clear_widgets()
        self.p1_ft_choice_box.opacity = 0
        self.p2_ft_choice_box.clear_widgets()
        self.p2_ft_choice_box.opacity = 0
        
        self.p1_ft_roll_display_label.text = str(p1_roll) if p1_roll > 0 else ""
        self.p2_ft_roll_display_label.text = str(p2_roll) if p2_roll > 0 else ""

        self.p1_ft_roll_button.disabled = p1_roll > 0 or winner_id is not None
        self.p2_ft_roll_button.disabled = p2_roll > 0 or winner_id is not None

        if winner_id is None:
            # --- State: Before a winner is decided ---
            if p1_roll > 0:
                self.first_turn_status_label.text = f"Waiting for {gs['player2']['name']} to roll..."
            elif p2_roll > 0:
                self.first_turn_status_label.text = f"Waiting for {gs['player1']['name']} to roll..."
            else:
                self.first_turn_status_label.text = "Roll for First Turn. Winner chooses who goes first."
        elif first_turn_player_id is None:
            # --- State: Winner decided, but turn not chosen ---
            winner_name = gs[f'player{winner_id}']['name']
            if p1_roll == p2_roll:
                attacker_name = gs[f"player{gs['deployment_attacker_id']}"]['name']
                self.first_turn_status_label.text = f"Tie! {attacker_name} (Attacker) chooses who goes first."
            else:
                self.first_turn_status_label.text = f"{winner_name} wins! Choose who takes the first turn."

            # Show choice buttons for the winner
            winner_choice_box = self.p1_ft_choice_box if winner_id == 1 else self.p2_ft_choice_box
            winner_choice_box.opacity = 1
            self._setup_choice_buttons(winner_choice_box, winner_id)
        else:
            # --- State: First turn player decided ---
            p1_turn_text = "First" if first_turn_player_id == 1 else "Second"
            p2_turn_text = "First" if first_turn_player_id == 2 else "Second"
            self.p1_ft_roll_display_label.text = p1_turn_text
            self.p2_ft_roll_display_label.text = p2_turn_text

            starting_player_name = gs[f'player{first_turn_player_id}']["name"]
            self.first_turn_status_label.text = f"{starting_player_name} will take the first turn! Click 'Start Game' below."
        
        self.start_game_button.disabled = first_turn_player_id is None

    def _setup_choice_buttons(self, choice_box, winner_id):
        """Helper to create and add first turn choice buttons."""
        app = App.get_running_app()
        btn_self_first = Button(
            text="I'll Go First",
            on_press=lambda x: app.handle_first_turn_choice(winner_id, True),
            size_hint_y=None, height=dp(35), font_size='14sp'
        )
        btn_opponent_first = Button(
            text="They Go First",
            on_press=lambda x: app.handle_first_turn_choice(winner_id, False),
            size_hint_y=None, height=dp(35), font_size='14sp'
        )
        choice_box.add_widget(btn_self_first)
        choice_box.add_widget(btn_opponent_first)

    def roll_first_turn_initiative(self, player_id):
        """Called from KV. Delegates the action to the main app."""
        App.get_running_app().handle_first_turn_roll(player_id)

    def start_game_action(self):
        """Called from KV. Delegates the action to the main app."""
        App.get_running_app().start_game() 