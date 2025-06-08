from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty
import random

class InitiativeScreen(Screen):
    p1_name_label = ObjectProperty(None)
    p2_name_label = ObjectProperty(None)
    status_label = ObjectProperty(None)
    p1_roll_label = ObjectProperty(None)
    p2_roll_label = ObjectProperty(None)
    p1_roll_button = ObjectProperty(None)
    p2_roll_button = ObjectProperty(None)
    p1_choice_box = ObjectProperty(None)
    p2_choice_box = ObjectProperty(None)
    continue_box = ObjectProperty(None)

    p1_roll = NumericProperty(0)
    p2_roll = NumericProperty(0)
    
    def on_enter(self):
        """Called when the screen is shown."""
        app = App.get_running_app()
        self.p1_name_label.text = app.game_state.get('p1_name', 'Player 1')
        self.p2_name_label.text = app.game_state.get('p2_name', 'Player 2')
        self.reset_screen()

    def reset_screen(self, is_reroll=False):
        """Resets the screen to its initial state."""
        self.p1_roll = 0
        self.p2_roll = 0
        self.p1_roll_button.disabled = False
        self.p2_roll_button.disabled = False
        self.p1_choice_box.opacity = 0
        self.p1_choice_box.disabled = True
        self.p2_choice_box.opacity = 0
        self.p2_choice_box.disabled = True
        self.continue_box.opacity = 0
        self.continue_box.disabled = True

        if not is_reroll:
            self.p1_roll_label.text = ""
            self.p2_roll_label.text = ""
        self.status_label.text = "Roll for Initiative!"

    def roll_die(self, player):
        """Handles the dice roll for a given player."""
        if player == 1 and self.p1_roll == 0:
            self.p1_roll = random.randint(1, 6)
            self.p1_roll_label.text = f"Rolled: {self.p1_roll}"
            self.p1_roll_button.disabled = True
        elif player == 2 and self.p2_roll == 0:
            self.p2_roll = random.randint(1, 6)
            self.p2_roll_label.text = f"Rolled: {self.p2_roll}"
            self.p2_roll_button.disabled = True

        if self.p1_roll > 0 and self.p2_roll > 0:
            self.determine_winner()

    def determine_winner(self):
        """Checks rolls and determines the winner or handles a tie."""
        app = App.get_running_app()
        p1_name = app.game_state.get('p1_name')
        p2_name = app.game_state.get('p2_name')

        if self.p1_roll > self.p2_roll:
            self.status_label.text = f"{p1_name} wins and takes the first turn!"
            self._prepare_for_game_start(p1_name)
        elif self.p2_roll > self.p1_roll:
            self.status_label.text = f"{p2_name} wins and takes the first turn!"
            self._prepare_for_game_start(p2_name)
        else:
            # Tie
            attacker_name = app.game_state.get('attacker_name')
            self.status_label.text = f"It's a tie! {attacker_name}, you choose who goes first."
            self.show_tiebreaker_buttons()

    def show_tiebreaker_buttons(self):
        self.p1_roll_button.disabled = True
        self.p2_roll_button.disabled = True
        
        app = App.get_running_app()
        attacker_name = app.game_state.get('attacker_name')
        p1_name = app.game_state.get('p1_name')

        if attacker_name == p1_name:
            self.p1_choice_box.opacity = 1
            self.p1_choice_box.disabled = False
        else:
            self.p2_choice_box.opacity = 1
            self.p2_choice_box.disabled = False

    def select_first_turn(self, choice_name):
        """Sets the first turn player based on the Attacker's tiebreaker choice."""
        self.status_label.text = f"{choice_name} will take the first turn."
        self._prepare_for_game_start(choice_name)

    def _prepare_for_game_start(self, first_player_name):
        """Sets the game state and shows the continue button."""
        self.p1_roll_button.disabled = True
        self.p2_roll_button.disabled = True
        self.p1_choice_box.opacity = 0
        self.p1_choice_box.disabled = True
        self.p2_choice_box.opacity = 0
        self.p2_choice_box.disabled = True
        
        app = App.get_running_app()
        app.game_state['first_turn_player_name'] = first_player_name
        app.game_state['current_player_name'] = first_player_name
        app.game_state['current_round'] = 1
        print(f"First turn will go to: {first_player_name}. Waiting for user to continue.")

        self.continue_box.opacity = 1
        self.continue_box.disabled = False

    def proceed_to_game(self):
        """Transitions to the scoreboard."""
        print("Proceeding to scoreboard.")
        self.manager.current = 'scoreboard' 