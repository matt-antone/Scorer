import random

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.metrics import dp


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._p1_roll = 0
        self._p2_roll = 0
        self._p1_rolled_once = False # Track if P1 has rolled at least once in this phase
        self._p2_rolled_once = False # Track if P2 has rolled at least once in this phase

    def on_pre_enter(self, *args):
        gs = App.get_running_app().game_state
        self.p1_name_label.text = gs['player1']['name']
        self.p2_name_label.text = gs['player2']['name']
        
        self._p1_roll = 0
        self._p2_roll = 0
        self._p1_rolled_once = False
        self._p2_rolled_once = False
        gs["deployment_initiative_winner_id"] = None
        gs["deployment_attacker_id"] = None
        gs["deployment_defender_id"] = None
        gs["player1"]["deployment_roll"] = 0
        gs["player2"]["deployment_roll"] = 0

        self.p1_roll_button.disabled = False
        self.p1_roll_display_label.text = "P1 Deploy: -"
        self.p1_choice_box.clear_widgets()
        self.p1_choice_box.opacity = 0 

        self.p2_roll_button.disabled = False
        self.p2_roll_display_label.text = "P2 Deploy: -"
        self.p2_choice_box.clear_widgets()
        self.p2_choice_box.opacity = 0

        self.deployment_status_label.text = "Roll for Deployment Attacker/Defender"
        self.continue_to_first_turn_button.disabled = True
        
    def roll_deployment_initiative(self, player_id):
        roll = random.randint(1,6)
        gs = App.get_running_app().game_state

        if player_id == 1:
            self._p1_roll = roll
            gs['player1']['deployment_roll'] = roll
            self.p1_roll_button.disabled = True
            self._p1_rolled_once = True
            self.p1_roll_display_label.text = roll
            if not self._p2_rolled_once:
                self.deployment_status_label.text = "Waiting for Player 2 to roll..."
                self.p2_roll_display_label.text = "P2 To Roll"
            else: # P2 has already rolled
                self.deployment_status_label.text = "Comparing rolls..."
        elif player_id == 2:
            self._p2_roll = roll
            gs['player2']['deployment_roll'] = roll
            self.p2_roll_button.disabled = True
            self._p2_rolled_once = True
            self.p2_roll_display_label.text = roll
            if not self._p1_rolled_once:
                self.deployment_status_label.text = "Waiting for Player 1 to roll..."
                self.p1_roll_display_label.text = "P1 To Roll"
            else: # P1 has already rolled
                self.deployment_status_label.text = "Comparing rolls..."

        if self._p1_rolled_once and self._p2_rolled_once: # Both have rolled at least once
            self.determine_deployment_winner()

    def determine_deployment_winner(self):
        gs = App.get_running_app().game_state
        p1_name = gs['player1']['name']
        p2_name = gs['player2']['name']

        if self._p1_roll > self._p2_roll:
            winner_id = 1
            winner_name = p1_name
            self.p1_roll_display_label.text = f"Win {self._p1_roll}"
            self.p2_roll_display_label.text = f"Lose {self._p2_roll}"
            self.p1_roll_button.disabled = True
            self.p2_roll_button.disabled = True
        elif self._p2_roll > self._p1_roll:
            winner_id = 2
            winner_name = p2_name
            self.p1_roll_display_label.text = f"Lose {self._p1_roll}"
            self.p2_roll_display_label.text = f"Win {self._p2_roll}"
            self.p1_roll_button.disabled = True
            self.p2_roll_button.disabled = True
        else: # Tie
            self.deployment_status_label.text = "Tie! Both players re-roll for deployment."
            self._p1_roll = 0; gs['player1']['deployment_roll'] = 0; self._p1_rolled_once = False
            self._p2_roll = 0; gs['player2']['deployment_roll'] = 0; self._p2_rolled_once = False
            self.p1_roll_button.disabled = False; self.p1_roll_display_label.text = "Re-Roll!"
            self.p2_roll_button.disabled = False; self.p2_roll_display_label.text = "Re-Roll!"
            return

        gs['deployment_initiative_winner_id'] = winner_id
        self.deployment_status_label.text = f"{winner_name} wins roll! {winner_name}, choose Attacker or Defender."
        
        winner_choice_box = self.p1_choice_box if winner_id == 1 else self.p2_choice_box
        winner_choice_box.clear_widgets()
        btn_attacker = Button(text="I am Attacker", on_press=lambda x: self.player_chooses_deployment_role(True), size_hint_y=None, height=dp(35), font_size='14sp')
        btn_defender = Button(text="I am Defender", on_press=lambda x: self.player_chooses_deployment_role(False), size_hint_y=None, height=dp(35), font_size='14sp')
        winner_choice_box.add_widget(btn_attacker)
        winner_choice_box.add_widget(btn_defender)
        winner_choice_box.opacity = 1

    def player_chooses_deployment_role(self, is_attacker: bool):
        gs = App.get_running_app().game_state
        chooser_id = gs.get("deployment_initiative_winner_id")
        if chooser_id is None: return 

        attacker_id = chooser_id if is_attacker else (1 if chooser_id == 2 else 2)
        defender_id = (1 if chooser_id == 2 else 2) if is_attacker else chooser_id
        
        gs["deployment_attacker_id"] = attacker_id
        gs["deployment_defender_id"] = defender_id

        attacker_name = gs[f'player{attacker_id}']["name"]
        defender_name = gs[f'player{defender_id}']["name"]
        self.deployment_status_label.text = f"Attacker: {attacker_name}, Defender: {defender_name}. Players deploy units."
        
        chooser_choice_box = self.p1_choice_box if chooser_id == 1 else self.p2_choice_box
        chooser_roll_display = self.p1_roll_display_label if chooser_id == 1 else self.p2_roll_display_label
        other_roll_display = self.p2_roll_display_label if chooser_id == 1 else self.p1_roll_display_label
        
        chooser_choice_box.clear_widgets()
        chooser_choice_box.opacity = 0
        
        chosen_role_text = "Role: Attacker" if chooser_id == attacker_id else "Role: Defender"
        assigned_role_text = "Role: Defender" if chooser_id == attacker_id else "Role: Attacker"

        chooser_roll_display.text = chosen_role_text
        other_roll_display.text = assigned_role_text # Update the other player's label too

        self.continue_to_first_turn_button.disabled = False
        gs['status_message'] = "Deployment roles chosen. Ready for First Turn Setup."
        
    def proceed_to_first_turn_setup(self):
        app = App.get_running_app()
        app.game_state['game_phase'] = 'first_turn'
        app.save_game_state()
        app.switch_screen('first_turn_setup') 