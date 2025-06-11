from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
import random

class DeploymentSetupScreen(Screen):
    # Game state
    p1_roll = NumericProperty(0)
    p2_roll = NumericProperty(0)
    winner_id = NumericProperty(0)

    def on_enter(self):
        """Called when the screen is shown."""
        app = App.get_running_app()
        self.ids.p1_name_label.text = app.game_state.get('p1_name', 'Player 1')
        self.ids.p2_name_label.text = app.game_state.get('p2_name', 'Player 2')
        self.reset_screen()

    def reset_screen(self, is_reroll=False):
        """Resets the screen to its initial state."""
        self.p1_roll = 0
        self.p2_roll = 0
        self.winner_id = 0
        self.ids.p1_roll_button.disabled = False
        self.ids.p2_roll_button.disabled = False
        self.ids.p1_choice_box.opacity = 0
        self.ids.p1_choice_box.disabled = True
        self.ids.p2_choice_box.opacity = 0
        self.ids.p2_choice_box.disabled = True

        if not is_reroll:
            self.ids.p1_roll_label.text = ""
            self.ids.p2_roll_label.text = ""
            self.ids.status_label.text = "Players roll to determine Attacker/Defender."
        else:
            self.ids.status_label.text = "It's a tie! Re-roll."

    def roll_die(self, player):
        """Handles the dice roll for a given player."""
        if player == 1 and self.p1_roll == 0:
            self.p1_roll = random.randint(1, 6)
            self.ids.p1_roll_label.text = str(self.p1_roll)
            self.ids.p1_roll_button.disabled = True
        elif player == 2 and self.p2_roll == 0:
            self.p2_roll = random.randint(1, 6)
            self.ids.p2_roll_label.text = str(self.p2_roll)
            self.ids.p2_roll_button.disabled = True

        if self.p1_roll > 0 and self.p2_roll > 0:
            self.determine_winner()

    def determine_winner(self):
        """Checks rolls and determines the winner or if a re-roll is needed."""
        if self.p1_roll > self.p2_roll:
            self.winner_id = 1
            winner_name = self.ids.p1_name_label.text
            self.ids.status_label.text = f"{winner_name} wins! Choose role:"
            self.show_choice_buttons()
        elif self.p2_roll > self.p1_roll:
            self.winner_id = 2
            winner_name = self.ids.p2_name_label.text
            self.ids.status_label.text = f"{winner_name} wins! Choose role:"
            self.show_choice_buttons()
        else:
            # Tie
            self.reset_screen(is_reroll=True)

    def show_choice_buttons(self):
        """Hides roll buttons and shows the attacker/defender choice on the winner's side."""
        self.ids.p1_roll_button.disabled = True
        self.ids.p2_roll_button.disabled = True
        if self.winner_id == 1:
            self.ids.p1_choice_box.opacity = 1
            self.ids.p1_choice_box.disabled = False
        elif self.winner_id == 2:
            self.ids.p2_choice_box.opacity = 1
            self.ids.p2_choice_box.disabled = False

    def select_role(self, role):
        """Handles the winner's role selection."""
        app = App.get_running_app()
        if self.winner_id == 1:
            attacker_name = self.ids.p1_name_label.text if role == 'attacker' else self.ids.p2_name_label.text
            defender_name = self.ids.p2_name_label.text if role == 'attacker' else self.ids.p1_name_label.text
        else: # winner_id == 2
            attacker_name = self.ids.p2_name_label.text if role == 'attacker' else self.ids.p1_name_label.text
            defender_name = self.ids.p1_name_label.text if role == 'attacker' else self.ids.p2_name_label.text
        app.game_state['attacker_name'] = attacker_name
        app.game_state['defender_name'] = defender_name
        print(f"Role selected. Attacker: {attacker_name}, Defender: {defender_name}")
        self.manager.current = 'initiative'

    def roll_player1(self):
        self.roll_die(1)

    def roll_player2(self):
        self.roll_die(2) 