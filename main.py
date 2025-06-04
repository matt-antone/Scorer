import random # Added for initiative roll
import time # Added for timer
import json # For saving/loading game state
import os   # For path manipulation
from kivy.config import Config # Ensure Config is imported first for this change
# Set default font *before* other Kivy components are imported if possible
# Note: Paths here assume the script is run from the project root where assets/fonts exists.
# If running from a different CWD, these paths might need to be absolute or adjusted.
# _font_path = "assets/fonts/Inter/static/" # Removed
# Config.set('kivy', 'default_font', [ # Removed
#     'Inter', # Removed
#     os.path.join(_font_path, 'Inter_18pt-Regular.ttf'), # Removed
#     os.path.join(_font_path, 'Inter_18pt-Italic.ttf'), # Removed
#     os.path.join(_font_path, 'Inter_18pt-Bold.ttf'), # Removed
#     os.path.join(_font_path, 'Inter_18pt-BoldItalic.ttf') # Removed
# ]) # Removed

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button # Import Button
from kivy.properties import DictProperty, StringProperty, NumericProperty, ObjectProperty # Added StringProperty, NumericProperty, ObjectProperty
from kivy.uix.popup import Popup # Import Popup
from kivy.uix.gridlayout import GridLayout # For NumberPad layout
from kivy.metrics import dp # Import dp from kivy.metrics
from kivy.uix.screenmanager import ScreenManager, Screen # Added ScreenManager, Screen
from kivy.clock import Clock # Added for timer updates
from kivy.uix.textinput import TextInput # Added for player names
from kivy.core.text import LabelBase # For registering fonts by name

# Register the Inter font family so it can be referred to by name 'Inter' in KV if needed.
# This also acts as a fallback or explicit way to use it.
# LabelBase.register( # Removed
#     name='Inter', # Removed
#     fn_regular=os.path.join(_font_path, 'Inter_18pt-Regular.ttf'), # Removed
#     fn_italic=os.path.join(_font_path, 'Inter_18pt-Italic.ttf'), # Removed
#     fn_bold=os.path.join(_font_path, 'Inter_18pt-Bold.ttf'), # Removed
#     fn_bolditalic=os.path.join(_font_path, 'Inter_18pt-BoldItalic.ttf') # Removed
# ) # Removed

# Register NotoColorEmoji font
# _noto_emoji_font_path = "assets/fonts/Noto_Color_Emoji/" # Removed
# LabelBase.register( # Removed
#     name='NotoColorEmoji', # Removed
#     fn_regular=os.path.join(_noto_emoji_font_path, 'NotoColorEmoji-Regular.ttf') # Removed
# ) # Removed

# Configure the window to be a fixed size, simulating the Pi screen for now
# We can make this more dynamic or fullscreen later.
Config.set('graphics', 'width', '800') # Typical 5-inch screen resolution might be 800x480
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', False) # Change to True if you want to resize on desktop

# --- New Setup Screens ---

class SplashScreen(Screen):
    pass

class NameEntryScreen(Screen):
    player1_name_input = ObjectProperty(None)
    player2_name_input = ObjectProperty(None)
    continue_button = ObjectProperty(None)

    def on_pre_enter(self, *args):
        # Initialize or clear names in game_state if necessary
        gs = App.get_running_app().game_state
        # self.player1_name_input.text = gs['player1'].get('name', 'Player 1') # Optionally load previous
        # self.player2_name_input.text = gs['player2'].get('name', 'Player 2') # Optionally load previous
        self.player1_name_input.text = "Player 1"
        self.player2_name_input.text = "Player 2"
        self.update_continue_button_state()

    def on_text_validate_p1(self, instance):
        self.update_continue_button_state()

    def on_text_validate_p2(self, instance):
        self.update_continue_button_state()
    
    def on_name_input(self, instance, value): # Called on each text change
        self.update_continue_button_state()

    def update_continue_button_state(self):
        if self.player1_name_input and self.player2_name_input and self.continue_button:
            p1_name = self.player1_name_input.text.strip()
            p2_name = self.player2_name_input.text.strip()
            self.continue_button.disabled = not (p1_name and p2_name)

    def save_names_and_proceed(self):
        gs = App.get_running_app().game_state
        p1_name = self.player1_name_input.text.strip()
        p2_name = self.player2_name_input.text.strip()

        if not p1_name or not p2_name:
            # This should ideally be a label on the screen
            print("Please enter names for both players.")
            return

        gs['player1']['name'] = p1_name
        gs['player2']['name'] = p2_name
        gs['status_message'] = "Names entered. Proceeding to Deployment Setup."
        print(f"Names Saved: P1: {p1_name}, P2: {p2_name}")
        self.manager.current = 'deployment_setup'

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
            self.p1_roll_display_label.text = f"P1 Rolled: {roll}"
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
            self.p2_roll_display_label.text = f"P2 Rolled: {roll}"
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
            self.p1_roll_display_label.text = f"Deploy: Won! ({self._p1_roll})"
            self.p2_roll_display_label.text = f"Deploy: Lost. ({self._p2_roll})"
            self.p1_roll_button.disabled = True
            self.p2_roll_button.disabled = True
        elif self._p2_roll > self._p1_roll:
            winner_id = 2
            winner_name = p2_name
            self.p1_roll_display_label.text = f"Deploy: Lost. ({self._p1_roll})"
            self.p2_roll_display_label.text = f"Deploy: Won! ({self._p2_roll})"
            self.p1_roll_button.disabled = True
            self.p2_roll_button.disabled = True
        else: # Tie
            self.deployment_status_label.text = "Tie! Both players re-roll for deployment."
            self._p1_roll = 0; gs['player1']['deployment_roll'] = 0; self._p1_rolled_once = False
            self._p2_roll = 0; gs['player2']['deployment_roll'] = 0; self._p2_rolled_once = False
            self.p1_roll_button.disabled = False; self.p1_roll_display_label.text = "P1 Re-Roll!"
            self.p2_roll_button.disabled = False; self.p2_roll_display_label.text = "P2 Re-Roll!"
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
        self.manager.current = 'first_turn_setup'

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
        self.p1_ft_roll_display_label.text = "P1 First Turn: -"
        self.p1_ft_choice_box.clear_widgets()
        self.p1_ft_choice_box.opacity = 0

        self.p2_ft_roll_button.disabled = False
        self.p2_ft_roll_display_label.text = "P2 First Turn: -"
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
            self.p1_ft_roll_display_label.text = f"P1 Rolled: {roll}"
            if not self._p2_ft_rolled_once:
                self.first_turn_status_label.text = "Waiting for Player 2 to roll..."
                self.p2_ft_roll_display_label.text = "P2 To Roll"
            else:
                self.first_turn_status_label.text = "Comparing rolls..."
        elif player_id == 2:
            self._p2_ft_roll = roll
            gs['player2']['first_turn_roll'] = roll
            self.p2_ft_roll_button.disabled = True
            self._p2_ft_rolled_once = True
            self.p2_ft_roll_display_label.text = f"P2 Rolled: {roll}"
            if not self._p1_ft_rolled_once:
                self.first_turn_status_label.text = "Waiting for Player 1 to roll..."
                self.p1_ft_roll_display_label.text = "P1 To Roll"
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
            self.p1_ft_roll_display_label.text = f"First Turn: Won! ({self._p1_ft_roll})"
            self.p2_ft_roll_display_label.text = f"First Turn: Lost. ({self._p2_ft_roll})"
        elif self._p2_ft_roll > self._p1_ft_roll:
            winner_id = 2; display_winner_name = p2_name
            self.p1_ft_roll_display_label.text = f"First Turn: Lost. ({self._p1_ft_roll})"
            self.p2_ft_roll_display_label.text = f"First Turn: Won! ({self._p2_ft_roll})"
        else: # Tie
            winner_id = gs.get("deployment_attacker_id", 1) # Attacker (winner_id) decides tie
            display_winner_name = gs[f'player{winner_id}']['name']
            self.first_turn_status_label.text = f"Tie! {display_winner_name} (Attacker) chooses who goes first."
            self.p1_ft_roll_display_label.text = f"First Turn: Tie ({self._p1_ft_roll})"
            self.p2_ft_roll_display_label.text = f"First Turn: Tie ({self._p2_ft_roll})"
        
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
        gs["active_player_id"] = starting_player_id
        gs["first_player_of_game_id"] = starting_player_id
        
        starting_player_name = gs[f'player{starting_player_id}']["name"]
        self.first_turn_status_label.text = f"{starting_player_name} will take the first turn!"

        chooser_choice_box = self.p1_ft_choice_box if chooser_id == 1 else self.p2_ft_choice_box
        chooser_ft_roll_display = self.p1_ft_roll_display_label if chooser_id == 1 else self.p2_ft_roll_display_label
        other_player_id = 1 if chooser_id == 2 else 2 # Get the ID of the other player
        other_ft_roll_display = self.p1_ft_roll_display_label if other_player_id == 1 else self.p2_ft_roll_display_label
        
        chooser_choice_box.clear_widgets()
        chooser_choice_box.opacity = 0
        
        chooser_final_text = "Turn: First" if starting_player_id == chooser_id else "Turn: Second"
        other_final_text = "Turn: Second" if starting_player_id == chooser_id else "Turn: First"
        
        chooser_ft_roll_display.text = chooser_final_text
        other_ft_roll_display.text = other_final_text

        self.start_game_button.disabled = False
        gs['status_message'] = "First turn decided. Ready to start game."

    def start_game_action(self):
        gs = App.get_running_app().game_state
        
        if gs.get("active_player_id") is None:
            self.first_turn_status_label.text = "Error: First turn decision not completed."
            return

        gs["current_round"] = 1
        gs["game_phase"] = "playing"
        active_player_name = gs[f'player{gs["active_player_id"]}']["name"]
        gs["status_message"] = f"Round 1 - {active_player_name}'s Turn"
        
        scorer_screen = App.get_running_app().root.get_screen('scorer')
        if scorer_screen:
            scorer_screen.start_timer()

        App.get_running_app().save_game_state() # Save state when game starts

        self.manager.current = 'scorer'
        if scorer_screen:
             Clock.schedule_once(lambda dt: scorer_screen.update_ui_from_state(), 0)
             # Also ensure timers are visually updated if loading into an active game state
             Clock.schedule_once(lambda dt: scorer_screen.update_timer_display(0), 0.1)


class ScorerRootWidget(Screen):
    p1_action_area = ObjectProperty(None)
    p2_action_area = ObjectProperty(None)
    p1_player_timer_label = ObjectProperty(None)
    p2_player_timer_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ScorerRootWidget, self).__init__(**kwargs)
        self.numpad_popup = None

    def on_pre_enter(self, *args):
        self.update_ui_from_state()
        self.update_timer_display(0) 

    def update_ui_from_state(self):
        if not self.ids: 
            return
        gs = App.get_running_app().game_state

        self.ids.p1_name_label.text = gs['player1']['name']
        self.ids.p2_name_label.text = gs['player2']['name']
        self.ids.p1_score_label.text = f"Score: {gs['player1']['total_score']}"
        self.ids.p1_cp_label.text = f"CP: {gs['player1']['cp']}"
        self.ids.p2_score_label.text = f"Score: {gs['player2']['total_score']}"
        self.ids.p2_cp_label.text = f"CP: {gs['player2']['cp']}"

        if self.p1_action_area: self.p1_action_area.clear_widgets()
        if self.p2_action_area: self.p2_action_area.clear_widgets()
        
        if gs['game_phase'] == "playing":
            self.ids.round_label.text = f"Round: {gs['current_round']}"
            if gs.get("active_player_id"):
                active_player_name = gs[f'player{gs["active_player_id"]}']['name']
                self.ids.status_label.text = f"Status: {active_player_name}'s Turn"
                
                end_turn_button = Button(text="End Turn", on_press=self.end_turn, size_hint_y=None, height=dp(40))
                if gs["active_player_id"] == 1 and self.p1_action_area:
                    self.p1_action_area.add_widget(end_turn_button)
                elif gs["active_player_id"] == 2 and self.p2_action_area:
                    self.p2_action_area.add_widget(end_turn_button)
            else:
                 self.ids.status_label.text = "Status: Initializing..."
        elif gs['game_phase'] == "game_over":
            final_round = gs.get('last_round_played', 5)
            self.ids.round_label.text = f"Round: {final_round} (Game Over)"
            self.ids.status_label.text = f"Status: Game Over - Round {final_round} complete"
        else: 
            self.ids.round_label.text = "Round: -"
            self.ids.status_label.text = f"Status: {gs['status_message']}"

    def start_timer(self):
        gs = App.get_running_app().game_state
        if gs['game_timer']['status'] == 'stopped':
            time_now = time.time()
            gs['game_timer']['start_time'] = time_now
            gs['game_timer']['turn_segment_start_time'] = time_now
            gs['game_timer']['status'] = 'running'
            Clock.schedule_interval(self.update_timer_display, 1)
            print("Timer started.")
            self.update_timer_display(0)

    def stop_timer(self):
        gs = App.get_running_app().game_state
        if gs['game_timer']['status'] == 'running':
            gs['game_timer']['status'] = 'stopped'
            Clock.unschedule(self.update_timer_display)
            self.update_timer_display(0) 
            print("Timer stopped.")

    def _format_seconds_to_hms(self, total_seconds):
        total_seconds = int(total_seconds)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def update_timer_display(self, dt): 
        gs = App.get_running_app().game_state
        time_now = time.time()

        if gs['game_timer']['status'] == 'running':
            elapsed_seconds = time_now - gs['game_timer']['start_time']
            gs['game_timer']['elapsed_display'] = self._format_seconds_to_hms(elapsed_seconds)
        
        if self.ids.get('timer_label'):
            self.ids.timer_label.text = f"Timer: {gs['game_timer']['elapsed_display']}"

        active_player_id = gs.get("active_player_id")

        # Player 1 Timer Update
        p1_key = "player1"
        p1_total_seconds = gs[p1_key]['player_elapsed_time_seconds']
        if active_player_id == 1 and gs['game_timer']['status'] == 'running' and gs['game_phase'] == 'playing':
            current_segment_duration = time_now - gs['game_timer']['turn_segment_start_time']
            live_total_seconds_p1 = p1_total_seconds + current_segment_duration
            gs[p1_key]['player_time_display'] = self._format_seconds_to_hms(live_total_seconds_p1)
        else:
            gs[p1_key]['player_time_display'] = self._format_seconds_to_hms(p1_total_seconds)

        if self.p1_player_timer_label: # Use direct ObjectProperty
            p1_name_short = gs[p1_key]['name'].split(' ')[0]
            self.p1_player_timer_label.text = f"{p1_name_short} Time: {gs[p1_key]['player_time_display']}"

        # Player 2 Timer Update
        p2_key = "player2"
        p2_total_seconds = gs[p2_key]['player_elapsed_time_seconds']
        if active_player_id == 2 and gs['game_timer']['status'] == 'running' and gs['game_phase'] == 'playing':
            current_segment_duration = time_now - gs['game_timer']['turn_segment_start_time']
            live_total_seconds_p2 = p2_total_seconds + current_segment_duration
            gs[p2_key]['player_time_display'] = self._format_seconds_to_hms(live_total_seconds_p2)
        else:
            gs[p2_key]['player_time_display'] = self._format_seconds_to_hms(p2_total_seconds)
            
        if self.p2_player_timer_label: # Use direct ObjectProperty
            p2_name_short = gs[p2_key]['name'].split(' ')[0]
            self.p2_player_timer_label.text = f"{p2_name_short} Time: {gs[p2_key]['player_time_display']}"

    def end_turn(self, instance=None):
        gs = App.get_running_app().game_state
        if gs["game_phase"] != "playing":
            return

        time_now = time.time()
        outgoing_player_id = gs["active_player_id"]
        
        if gs['game_timer']['status'] == 'running':
            turn_duration = time_now - gs['game_timer']['turn_segment_start_time']
            gs[f'player{outgoing_player_id}']['player_elapsed_time_seconds'] += turn_duration
            gs[f'player{outgoing_player_id}']['player_time_display'] = self._format_seconds_to_hms(
                gs[f'player{outgoing_player_id}']['player_elapsed_time_seconds']
            )

        next_player_id = 2 if outgoing_player_id == 1 else 1
        gs["active_player_id"] = next_player_id
        newly_active_player_name = gs[f'player{gs["active_player_id"]}']['name']

        round_advanced_or_game_ended = False
        first_player_of_game_id = gs.get("first_player_of_game_id")
        if first_player_of_game_id is not None and outgoing_player_id != first_player_of_game_id:
            gs["current_round"] += 1
            round_advanced_or_game_ended = True
        
        if gs["current_round"] > 5: 
            gs["game_phase"] = "game_over"
            gs["last_round_played"] = 5 
            gs["status_message"] = f"Game Over - Round 5 complete" 
            self.stop_timer()
            # Transition to GameOverScreen
            self.manager.current = 'game_over_screen' 
            # No need to call update_ui_from_state() here for ScorerRootWidget as we are leaving it.
            # GameOverScreen's on_pre_enter will handle its own UI.
            return # Important to return here to skip further UI updates for ScorerRootWidget
        else:
            gs["status_message"] = f"Round {gs['current_round']} - {newly_active_player_name}'s Turn"
            gs['game_timer']['turn_segment_start_time'] = time_now 
            
        self.update_ui_from_state()
        if not round_advanced_or_game_ended or gs["game_phase"] == "playing":
             self.update_timer_display(0)

    def open_score_numpad(self, player_id_to_score):
        gs = App.get_running_app().game_state
        if gs["game_phase"] != "playing":
            gs["status_message"] = "Cannot change score, game not active."
            self.update_ui_from_state()
            return
        
        if self.numpad_popup:
             try:
                 self.numpad_popup.dismiss()
             except Exception as e:
                 print(f"Error dismissing numpad: {e}")
                 self.numpad_popup = None
        
        self.numpad_popup = NumberPadPopup(caller_widget=self)
        player_name = gs[f"player{player_id_to_score}"]["name"]
        self.numpad_popup.title = f"Enter {player_name} Score (Primary)" 
        self.numpad_popup.caller_info = {'player_id': player_id_to_score, 'score_type': 'primary'}
        self.numpad_popup.open()

    def process_numpad_value(self, score_value, player_id, score_type='primary'):
        player_key = f"player{player_id}"
        gs = App.get_running_app().game_state
        
        if player_key in gs:
            gs[player_key]["primary_score"] = score_value 
            gs[player_key]["total_score"] = gs[player_key]["primary_score"] + gs[player_key].get("secondary_score", 0) 
            gs["status_message"] = f"{gs[player_key]['name']} Score Updated"
            self.update_ui_from_state()
        else:
            gs["status_message"] = f"Error: Invalid player ID"
            self.update_ui_from_state()

    def add_cp(self, player_id, amount=1):
        gs = App.get_running_app().game_state
        if gs["game_phase"] != "playing": return
        player_key = f"player{player_id}"
        if player_key in gs:
            gs[player_key]["cp"] = max(0, gs[player_key]["cp"] + amount)
            gs["status_message"] = f"{gs[player_key]['name']} CP Updated"
            self.update_ui_from_state()

    def remove_cp(self, player_id, amount=1): 
        gs = App.get_running_app().game_state
        if gs["game_phase"] != "playing": return
        player_key = f"player{player_id}"
        if player_key in gs:
            if gs[player_key]["cp"] > 0:
                gs[player_key]["cp"] = max(0, gs[player_key]["cp"] - amount)
                gs["status_message"] = f"{gs[player_key]['name']} CP Updated"
            else:
                gs["status_message"] = f"{gs[player_key]['name']} CP is 0"
            self.update_ui_from_state()
    
    def request_new_game(self):
        print("New Game button pressed.")
        self.stop_timer() # Ensure current screen's timer is stopped
        App.get_running_app().start_new_game_flow()

    def exit_app(self):
        print("Exiting application...")
        gs = App.get_running_app().game_state
        if gs['game_timer']['status'] == 'running':
            if gs['game_phase'] == 'playing' and gs.get('active_player_id'):
                active_player_id = gs['active_player_id']
                time_now = time.time()
                if gs['game_timer'].get('turn_segment_start_time') and gs['game_timer']['turn_segment_start_time'] > 0:
                    turn_duration = time_now - gs['game_timer']['turn_segment_start_time']
                    gs[f'player{active_player_id}']['player_elapsed_time_seconds'] += turn_duration
                    gs[f'player{active_player_id}']['player_time_display'] = self._format_seconds_to_hms(
                        gs[f'player{active_player_id}']['player_elapsed_time_seconds']
                    )
        self.stop_timer() 
        App.get_running_app().stop()

class NumberPadPopup(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(NumberPadPopup, self).__init__(**kwargs)
        self.caller_widget = caller_widget 
        self.title = "Enter Score"
        self.caller_info = kwargs.pop('caller_info', {'player_id': 1, 'score_type': 'primary'}) 
        self.entered_value = "" 
        self.content_layout = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(5))
        
        self.display = Label(text="0", font_size='24sp', size_hint_y=None, height=dp(40))
        self.content_layout.add_widget(self.display)
        
        grid = GridLayout(cols=3, spacing=dp(5))
        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            'C', '0', 'Ent'
        ]
        for btn_text in buttons:
            button = Button(text=btn_text, font_size='20sp', on_press=self.on_button_press)
            grid.add_widget(button)
            
        self.content_layout.add_widget(grid)
        self.content = self.content_layout
        self.size_hint = (None, None)
        self.size = (dp(250), dp(350))

    def on_button_press(self, instance):
        if instance.text == 'C':
            self.entered_value = ""
        elif instance.text == 'Ent':
            score = 0 
            if self.entered_value:
                try:
                    score = int(self.entered_value)
                except ValueError:
                    self.entered_value = "Error" 
                    self.display.text = self.entered_value
                    return 
            player_id = self.caller_info.get('player_id', 1) 
            score_type = self.caller_info.get('score_type', 'primary')
            self.caller_widget.process_numpad_value(score, player_id, score_type)
            self.dismiss()
        else: 
            if len(self.entered_value) < 3: 
                self.entered_value += instance.text
        self.display.text = self.entered_value if self.entered_value else "0"


class GameOverScreen(Screen):
    result_status_label = ObjectProperty(None)
    p1_final_name_label = ObjectProperty(None)
    p1_final_score_label = ObjectProperty(None)
    p1_final_cp_label = ObjectProperty(None)
    p1_final_time_label = ObjectProperty(None)
    p2_final_name_label = ObjectProperty(None)
    p2_final_score_label = ObjectProperty(None)
    p2_final_cp_label = ObjectProperty(None)
    p2_final_time_label = ObjectProperty(None)
    total_game_time_label = ObjectProperty(None)
    rounds_played_label = ObjectProperty(None)

    def on_pre_enter(self, *args):
        gs = App.get_running_app().game_state
        
        # Determine winner
        p1_score = gs['player1']['total_score']
        p2_score = gs['player2']['total_score']
        winner_text = ""
        if p1_score > p2_score:
            winner_text = f"{gs['player1']['name']} Wins!"
        elif p2_score > p1_score:
            winner_text = f"{gs['player2']['name']} Wins!"
        else:
            winner_text = "It's a Tie!"
        
        if self.result_status_label: self.result_status_label.text = winner_text
        
        # Populate Player 1 Stats
        if self.p1_final_name_label: self.p1_final_name_label.text = f"Player: {gs['player1']['name']}"
        if self.p1_final_score_label: self.p1_final_score_label.text = f"Final Score: {p1_score}"
        if self.p1_final_cp_label: self.p1_final_cp_label.text = f"CP Remaining: {gs['player1']['cp']}"
        if self.p1_final_time_label: self.p1_final_time_label.text = f"Time Played: {gs['player1']['player_time_display']}"

        # Populate Player 2 Stats
        if self.p2_final_name_label: self.p2_final_name_label.text = f"Player: {gs['player2']['name']}"
        if self.p2_final_score_label: self.p2_final_score_label.text = f"Final Score: {p2_score}"
        if self.p2_final_cp_label: self.p2_final_cp_label.text = f"CP Remaining: {gs['player2']['cp']}"
        if self.p2_final_time_label: self.p2_final_time_label.text = f"Time Played: {gs['player2']['player_time_display']}"

        # Populate Game Stats
        if self.total_game_time_label: self.total_game_time_label.text = f"Total Game Time: {gs['game_timer']['elapsed_display']}"
        # last_round_played should be 5 as per logic in end_turn
        if self.rounds_played_label: self.rounds_played_label.text = f"Rounds Played: {gs.get('last_round_played', 5)}"

    def start_new_game(self):
        App.get_running_app().start_new_game_flow()

    def exit_app_from_game_over(self): # Renamed to avoid conflict if we had an exit_app here
        App.get_running_app().stop()


class ScorerApp(App):
    SAVE_FILE_NAME = "game_state.json"
    SPLASH_DURATION = 2.5 # Duration in seconds for the splash screen

    def _get_default_game_state(self):
        """Helper method to return a pristine default game state dictionary."""
        return {
            "player1": { 
                "name": "Player 1", "primary_score": 0, "secondary_score": 0, "total_score": 0, "cp": 0, 
                "deployment_roll": 0, "first_turn_roll": 0,
                "player_elapsed_time_seconds": 0, "player_time_display": "00:00:00"
            },
            "player2": {
                "name": "Player 2", "primary_score": 0, "secondary_score": 0, "total_score": 0, "cp": 0,
                "deployment_roll": 0, "first_turn_roll": 0,
                "player_elapsed_time_seconds": 0, "player_time_display": "00:00:00"
            },
            "current_round": 0, "active_player_id": None, 
            "deployment_initiative_winner_id": None, "deployment_attacker_id": None, "deployment_defender_id": None,
            "first_turn_choice_winner_id": None, "first_player_of_game_id": None,
            "last_round_played": 0, 
            "game_phase": "setup", # Always start in setup for a new game
            "game_timer": { 
                "status": "stopped", "start_time": 0, "elapsed_display": "00:00:00",
                "turn_segment_start_time": 0 
            },
            "status_message": "Awaiting Name Entry..."
        }

    def reset_game_state_to_default(self):
        self.game_state = self._get_default_game_state()
        print("Game state has been reset to default.")

    def start_new_game_flow(self):
        print("Starting new game flow...")
        # Stop timer on current game screen if it exists and is active
        if self.root and self.root.current == 'scorer':
            scorer_screen = self.root.get_screen('scorer')
            if scorer_screen:
                scorer_screen.stop_timer()
        
        self.reset_game_state_to_default()
        self.save_game_state() # Save the fresh state immediately
        if self.root:
            self.root.current = 'name_entry'

    def get_save_file_path(self):
        return os.path.join(self.user_data_dir, self.SAVE_FILE_NAME)

    def save_game_state(self):
        save_path = self.get_save_file_path()
        try:
            if not os.path.exists(self.user_data_dir):
                os.makedirs(self.user_data_dir)
                print(f"Created user_data_dir: {self.user_data_dir}")
            with open(save_path, 'w') as f:
                json.dump(self.game_state, f, indent=4)
            print(f"Game state saved to {save_path}")
        except Exception as e:
            print(f"Error saving game state to {save_path}: {e}")

    def load_game_state(self):
        load_path = self.get_save_file_path()
        if os.path.exists(load_path):
            try:
                with open(load_path, 'r') as f:
                    loaded_state = json.load(f)
                    if isinstance(loaded_state, dict) and 'player1' in loaded_state and 'game_phase' in loaded_state:
                        self.game_state.update(loaded_state)
                        print(f"Game state loaded from {load_path}")
                    else:
                        print(f"Invalid game state format in {load_path}")
            except Exception as e:
                print(f"Error loading game state from {load_path}: {e}")
        else:
            print(f"No save file found at {load_path}. Starting with default state.")

    def build(self):
        self.game_state = self._get_default_game_state() # Initialize with defaults first
        self.screen_manager = ScreenManager()

        # Add all screens
        self.screen_manager.add_widget(SplashScreen(name='splash_screen')) # Add Splash Screen
        self.screen_manager.add_widget(NameEntryScreen(name='name_entry'))
        self.screen_manager.add_widget(DeploymentSetupScreen(name='deployment_setup'))
        self.screen_manager.add_widget(FirstTurnSetupScreen(name='first_turn_setup'))
        self.screen_manager.add_widget(ScorerRootWidget(name='scorer_root'))
        self.screen_manager.add_widget(GameOverScreen(name='game_over'))

        # Determine the actual screen to go to after splash
        loaded_state = self.load_game_state()
        actual_initial_screen = 'name_entry' # Default if no save or new game

        if loaded_state:
            self.game_state.update(loaded_state)
            # Logic to determine screen based on loaded state
            if self.game_state.get('game_phase') == 'name_entry' or not self.game_state.get('player1', {}).get('name'):
                actual_initial_screen = 'name_entry'
            elif self.game_state.get('game_phase') == 'deployment_setup':
                actual_initial_screen = 'deployment_setup'
            elif self.game_state.get('game_phase') == 'first_turn_setup':
                actual_initial_screen = 'first_turn_setup'
            elif self.game_state.get('game_phase') == 'game_active':
                 # Check if game might have ended prematurely (e.g. round > 5)
                if self.game_state.get('current_round', 0) > self.game_state.get('max_rounds', 5):
                    actual_initial_screen = 'game_over' # Or handle game conclusion logic
                else:
                    actual_initial_screen = 'scorer_root'
            elif self.game_state.get('game_phase') == 'game_over':
                actual_initial_screen = 'game_over'
            else: # Default to name entry if phase is unknown or first time
                actual_initial_screen = 'name_entry'
        else: # No save file, or error loading it, treat as new game
            self.initialize_game_state() # Sets up default state and phase 'name_entry'
            actual_initial_screen = 'name_entry'
            
        print(f"After load, determined actual initial screen: {actual_initial_screen}")

        self.screen_manager.current = 'splash_screen'
        Clock.schedule_once(lambda dt: self.transition_from_splash(actual_initial_screen, dt), self.SPLASH_DURATION)
        
        return self.screen_manager

    def transition_from_splash(self, target_screen_name, dt):
        """Transitions from splash screen to the target screen."""
        print(f"Transitioning from splash to {target_screen_name}")
        if target_screen_name == 'scorer_root' and self.game_state.get('current_round', 0) == 0:
            # This ensures if we are going to scorer_root but it's effectively a new game setup state
            # (e.g. loaded a game that was saved right at the start of round 1 before first turn action)
            # we properly initialize the ScorerRootWidget's UI elements from game_state
            # It might be better handled inside ScorerRootWidget.on_pre_enter
            print("Transitioning to scorer_root, ensuring game_state is applied.")
            # The on_pre_enter of ScorerRootWidget should handle UI updates.
            pass

        self.screen_manager.current = target_screen_name

    def initialize_game_state(self): 
        self.game_state = self._get_default_game_state() # Start with defaults
        self.load_game_state() # Then attempt to load and override

    def on_stop(self):
        print("Application stopping. Saving game state...")
        self.save_game_state()

if __name__ == '__main__':
    ScorerApp().run() 