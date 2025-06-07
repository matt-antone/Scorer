from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock

# Behavior of this screen:
# 1. Default visual state:
#   - Player 1 and Player 2 names are displayed in the labels.
#   - Player 1 roll button is enabled.
#   - Player 2 roll button is enabled.
#   - Deployment status label is "Roll for who deploys first. Winner chooses Attacker/Defender."
#   - Continue button is disabled.
#   - Roll is blank by default and once the roll has been made, it is displayed until there is a new roll. Never replaced with text.
# 2. Button Visual States:
#   - When the user taps on the roll button, the roll is displayed in the label and the button is disabled.
#   - When the user taps on the choice box, the choice is displayed in the label.
#   - The continue button is disabled until there is a winner and that player has chosen their role.
#   - Role choice buttons are hidden by default and displayed for the winner.
#   - 
# 3. Status Messages:
#   - "Roll for who deploys first. Winner chooses Attacker/Defender." is displayed when the user has not rolled yet.
#   - "Win" or "Lose" is displayed in the roll button label when the user has rolled and the winner has been determined.
#   - "Tie! Both players re-roll for deployment." is displayed when the user has rolled and the roll is a tie.
#   - "Waiting for {player_name} to roll..." is displayed when the user has rolled and the winner has not been determined.
#   - "Deploy your units and click 'Continue' below." is displayed when the user has chosen their role and the game is ready to proceed to the first turn setup screen.

class DeploymentSetupScreen(Screen):
    # Player 1 UI
    p1_name_label = ObjectProperty(None)
    p1_roll_button = ObjectProperty(None)
    p1_roll_display_label = ObjectProperty(None)
    p1_choice_box = ObjectProperty(None)

    # Player 2 UI
    p2_name_label = ObjectProperty(None)
    p2_roll_button = ObjectProperty(None)
    p2_roll_display_label = ObjectProperty(None)
    p2_choice_box = ObjectProperty(None)

    # General UI
    deployment_status_label = ObjectProperty(None)
    continue_to_first_turn_button = ObjectProperty(None)

    def on_pre_enter(self, *args):
        """Called every time the screen is shown. Does an initial draw."""
        self.update_view_from_state()

    def update_view_from_state(self, *args):
        """Updates the entire screen based on the central game_state and documented rules."""
        app = App.get_running_app()
        if not app:
            return
        gs = app.game_state

        self.p1_name_label.text = gs['player1']['name']
        self.p2_name_label.text = gs['player2']['name']

        p1_roll = gs['player1'].get('deployment_roll', 0)
        p2_roll = gs['player2'].get('deployment_roll', 0)
        winner_id = gs.get('deployment_initiative_winner_id')
        attacker_id = gs.get('deployment_attacker_id')

        # Reset buttons and choice boxes to a clean state before applying logic
        self.p1_roll_button.text = "Roll"
        self.p2_roll_button.text = "Roll"
        self.p1_choice_box.clear_widgets()
        self.p1_choice_box.opacity = 0
        self.p2_choice_box.clear_widgets()
        self.p2_choice_box.opacity = 0

        # Rule 1: Roll display label only ever shows the number, or is blank
        self.p1_roll_display_label.text = str(p1_roll) if p1_roll > 0 else ""
        self.p2_roll_display_label.text = str(p2_roll) if p2_roll > 0 else ""

        # Disable roll buttons if a player has rolled or a winner is decided
        self.p1_roll_button.disabled = p1_roll > 0 or winner_id is not None
        self.p2_roll_button.disabled = p2_roll > 0 or winner_id is not None

        if winner_id is None:
            # --- State: Before a winner is decided ---
            if p1_roll > 0 and p2_roll > 0: # Tie condition
                self.deployment_status_label.text = "Tie! Both players re-roll for deployment."
                self.p1_roll_button.text = f"Tie ({p1_roll})"
                self.p2_roll_button.text = f"Tie ({p2_roll})"
            elif p1_roll > 0:
                self.deployment_status_label.text = f"Waiting for {gs['player2']['name']} to roll..."
            elif p2_roll > 0:
                self.deployment_status_label.text = f"Waiting for {gs['player1']['name']} to roll..."
            else: # Initial state
                self.deployment_status_label.text = "Roll for who deploys first. Winner chooses Attacker/Defender."
        else:
            # --- State: After a winner has been decided ---
            # Rule 3: Display "Win" or "Lose" on the roll button itself
            if p1_roll > p2_roll:
                self.p1_roll_button.text = "Win"
                self.p2_roll_button.text = "Lose"
            else:
                self.p1_roll_button.text = "Lose"
                self.p2_roll_button.text = "Win"
            
            winner_name = gs[f'player{winner_id}']['name']
            if not attacker_id:
                # State: Winner decided, but role not chosen yet. Show choice buttons.
                self.deployment_status_label.text = f"{winner_name} wins! Choose Attacker or Defender."
                winner_choice_box = self.p1_choice_box if winner_id == 1 else self.p2_choice_box
                winner_choice_box.opacity = 1
                self._setup_choice_buttons(winner_choice_box, winner_id)

        if attacker_id:
            # --- State: Role has been chosen ---
            p1_role = "Attacker" if attacker_id == 1 else "Defender"
            p2_role = "Attacker" if attacker_id == 2 else "Defender"

            # Rule 2: Display the chosen role in a label within the choice_box
            self.p1_choice_box.add_widget(Label(text=p1_role, font_size='18sp'))
            self.p1_choice_box.opacity = 1
            self.p2_choice_box.add_widget(Label(text=p2_role, font_size='18sp'))
            self.p2_choice_box.opacity = 1
            
            self.deployment_status_label.text = "Deploy your units and click 'Continue' below."

        # Rule 2: Enable continue button only after a role has been chosen
        self.continue_to_first_turn_button.disabled = not attacker_id

    def _setup_choice_buttons(self, choice_box, winner_id):
        """Helper to create and add choice buttons."""
        app = App.get_running_app()
        btn_attacker = Button(
            text="I am Attacker",
            on_press=lambda x: app.handle_deployment_role_choice(winner_id, True),
            size_hint_y=None, height=dp(35), font_size='14sp'
        )
        btn_defender = Button(
            text="I am Defender",
            on_press=lambda x: app.handle_deployment_role_choice(winner_id, False),
            size_hint_y=None, height=dp(35), font_size='14sp'
        )
        choice_box.add_widget(btn_attacker)
        choice_box.add_widget(btn_defender)

    def roll_deployment_initiative(self, player_id):
        """Called from KV. Delegates the action to the main app."""
        App.get_running_app().handle_deployment_roll(player_id)

    def choose_deployment_role(self, chooser_id, chose_attacker):
        """Called from KV. Delegates the action to the main app."""
        App.get_running_app().handle_deployment_role_choice(chooser_id, chose_attacker)

    def proceed_to_first_turn(self):
        """Called from KV. Delegates the action to the main app."""
        App.get_running_app().proceed_to_first_turn_from_deployment()

    def on_pre_leave(self, *args):
        """Unbind when the screen is no longer visible."""
        App.get_running_app().unbind(game_state=self.update_view_from_state)