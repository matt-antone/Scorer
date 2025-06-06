import random

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.metrics import dp


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._p1_ft_roll = 0
        self._p2_ft_roll = 0
        self._p1_ft_rolled_once = False
        self._p2_ft_rolled_once = False

    def on_pre_enter(self, *args):
        gs = App.get_running_app().game_state
        self.p1_name_label.text = gs['player1']['name']
        self.p2_name_label.text = gs['player2']['name']

        self._p1_ft_roll = 0
        self._p2_ft_roll = 0
        self._p1_ft_rolled_once = False
        self._p2_ft_rolled_once = False
        gs["first_turn_choice_winner_id"] = None
        gs["player1"]["first_turn_roll"] = 0
        gs["player2"]["first_turn_roll"] = 0
        
        self.p1_ft_roll_button.disabled = False
        self.p1_ft_roll_display_label.text = ""
        self.p1_ft_choice_box.clear_widgets()
        self.p1_ft_choice_box.opacity = 0

        self.p2_ft_roll_button.disabled = False
        self.p2_ft_roll_display_label.text = ""
        self.p2_ft_choice_box.clear_widgets()
        self.p2_ft_choice_box.opacity = 0
        
        attacker_name = "Attacker (Unknown)"
        if gs.get('deployment_attacker_id'):
             attacker_name = gs[f"player{gs['deployment_attacker_id']}"]['name']
        self.first_turn_status_label.text = f"Roll for First Turn! Attacker ({attacker_name}) decides ties."
        self.start_game_button.disabled = True

    def roll_first_turn_initiative(self, player_id):
        roll = random.randint(1,6)
        gs = App.get_running_app().game_state

        if player_id == 1:
            self._p1_ft_roll = roll
            gs['player1']['first_turn_roll'] = roll
            self.p1_ft_roll_button.disabled = True
            self._p1_ft_rolled_once = True
            self.p1_ft_roll_display_label.text = f"{roll}"
            if not self._p2_ft_rolled_once:
                self.first_turn_status_label.text = "Waiting for Player 2 to roll..."
                self.p2_ft_roll_display_label.text = "Roll"
            else:
                self.first_turn_status_label.text = "Comparing rolls..."
        elif player_id == 2:
            self._p2_ft_roll = roll
            gs['player2']['first_turn_roll'] = roll
            self.p2_ft_roll_button.disabled = True
            self._p2_ft_rolled_once = True
            self.p2_ft_roll_display_label.text = f"{roll}"
            if not self._p1_ft_rolled_once:
                self.first_turn_status_label.text = "Waiting for Player 1 to roll..."
                self.p1_ft_roll_display_label.text = "Roll"
            else:
                self.first_turn_status_label.text = "Comparing rolls..."
        
        if self._p1_ft_rolled_once and self._p2_ft_rolled_once:
            self.determine_first_turn_winner()

    def determine_first_turn_winner(self):
        gs = App.get_running_app().game_state
        p1_name = gs['player1']['name']
        p2_name = gs['player2']['name']
        
        winner_id = 0 # This is the ID of the player who gets to CHOOSE who goes first
        display_winner_name = "" # This is the name to display as having won the roll/tie-break

        if self._p1_ft_roll > self._p2_ft_roll:
            winner_id = 1; display_winner_name = p1_name
            self.p1_ft_roll_display_label.text = f"Win {self._p1_ft_roll}"
            self.p2_ft_roll_display_label.text = f"Lose {self._p2_ft_roll}"
        elif self._p2_ft_roll > self._p1_ft_roll:
            winner_id = 2; display_winner_name = p2_name
            self.p1_ft_roll_display_label.text = f"Lose {self._p1_ft_roll}"
            self.p2_ft_roll_display_label.text = f"Win {self._p2_ft_roll}"
        else: # Tie
            winner_id = gs.get("deployment_attacker_id", 1) # Attacker (winner_id) decides tie
            display_winner_name = gs[f'player{winner_id}']['name']
            self.first_turn_status_label.text = f"Tie! {display_winner_name} (Attacker) chooses who goes first."
            self.p1_ft_roll_display_label.text = f"Tie {self._p1_ft_roll}"
            self.p2_ft_roll_display_label.text = f"Tie {self._p2_ft_roll}"
        
        self.p1_ft_roll_button.disabled = True # Ensure roll buttons are disabled
        self.p2_ft_roll_button.disabled = True

        gs["first_turn_choice_winner_id"] = winner_id 
        self.first_turn_status_label.text = f"{display_winner_name} won roll/tie! {display_winner_name}, choose who takes first turn."

        chooser_choice_box = self.p1_ft_choice_box if winner_id == 1 else self.p2_ft_choice_box
        chooser_choice_box.clear_widgets()
        btn_self_first = Button(text="I'll Go First", on_press=lambda x: self.player_decides_first_turn(True), size_hint_y=None, height=dp(35), font_size='14sp')
        btn_opponent_first = Button(text="Opponent Goes First", on_press=lambda x: self.player_decides_first_turn(False), size_hint_y=None, height=dp(35), font_size='14sp')
        chooser_choice_box.add_widget(btn_self_first)
        chooser_choice_box.add_widget(btn_opponent_first)
        chooser_choice_box.opacity = 1

    def player_decides_first_turn(self, decision_is_self_goes_first: bool):
        gs = App.get_running_app().game_state
        chooser_id = gs.get("first_turn_choice_winner_id")
        if chooser_id is None: return

        starting_player_id = chooser_id if decision_is_self_goes_first else (1 if chooser_id == 2 else 2)
        gs["first_turn_player_id"] = starting_player_id
        gs["first_player_of_game_id"] = starting_player_id
        
        starting_player_name = gs[f'player{starting_player_id}']["name"]
        self.first_turn_status_label.text = f"{starting_player_name} will take the first turn!"

        chooser_choice_box = self.p1_ft_choice_box if chooser_id == 1 else self.p2_ft_choice_box
        chooser_ft_roll_display = self.p1_ft_roll_display_label if chooser_id == 1 else self.p2_ft_roll_display_label
        other_player_id = 1 if chooser_id == 2 else 2 # Get the ID of the other player
        other_ft_roll_display = self.p1_ft_roll_display_label if other_player_id == 1 else self.p2_ft_roll_display_label
        
        chooser_choice_box.clear_widgets()
        chooser_choice_box.opacity = 0
        
        chooser_final_text = "First" if starting_player_id == chooser_id else "Second"
        other_final_text = "Second" if starting_player_id == chooser_id else "First"
        
        chooser_ft_roll_display.text = chooser_final_text
        other_ft_roll_display.text = other_final_text

        self.start_game_button.disabled = False
        gs['status_message'] = "First turn decided. Ready to start game."

    def start_game_action(self):
        app = App.get_running_app()
        gs = app.game_state
        
        gs['active_player_id'] = gs.get('first_turn_player_id')
        if not gs['active_player_id']:
            app.show_error_popup("Error", "First turn player not set.")
            return

        gs['game_phase'] = 'game_play'
        gs['current_round'] = 1
        app.save_game_state()

        scorer_screen = app.root.get_screen('game')
        scorer_screen.start_timers_and_ui()

        app.switch_screen('game') 