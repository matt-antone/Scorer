from kivy.config import Config # Ensure Config is imported first for this change
import platform # For OS detection
from kivy.core.window import Window # Ensure Window is imported

# OS-specific graphics configuration
os_type = platform.system()
if os_type == "Linux":  # Assuming Raspberry Pi OS reports as Linux
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'show_cursor', '0') # Hide cursor for kiosk on Pi
    Config.set('graphics', 'borderless', '1') # Attempt to set borderless early for Pi
    Config.set('graphics', 'window_state', 'maximized') # Add attempt to maximize window state
else:  # Default to development mode (e.g., macOS, Windows)
    Config.set('graphics', 'fullscreen', '0') # Ensure not fullscreen
    Config.set('graphics', 'show_cursor', '1') # Show cursor for dev
    # Set fixed size for development environments only
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '480')
    Config.set('graphics', 'resizable', False)

import random # Added for initiative roll
import time # Added for timer
import json # For saving/loading game state
import os   # For path manipulation
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

# Register Inter Black specifically for the new design
_inter_black_font_path = "assets/fonts/Inter/static/Inter_18pt-Black.ttf"
if os.path.exists(_inter_black_font_path):
    LabelBase.register(name='InterBlack', fn_regular=_inter_black_font_path)
    print(f"Registered font: InterBlack from {_inter_black_font_path}")
else:
    print(f"Warning: Font file not found at {_inter_black_font_path}. InterBlack will not be available.")

# Configure the window to be a fixed size, simulating the Pi screen for now
# We can make this more dynamic or fullscreen later.
# Config.set('graphics', 'width', '800') # MOVED
# Config.set('graphics', 'height', '480') # MOVED
# Config.set('graphics', 'resizable', False) # MOVED

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
        
        scorer_screen = App.get_running_app().root.get_screen('scorer_root')
        if scorer_screen:
            scorer_screen.start_timer()

        App.get_running_app().save_game_state() # Save state when game starts

        self.manager.current = 'scorer_root'
        if scorer_screen:
             Clock.schedule_once(lambda dt: scorer_screen.update_ui_from_state(), 0)
             # Also ensure timers are visually updated if loading into an active game state
             Clock.schedule_once(lambda dt: scorer_screen.update_timer_display(0), 0.1)


class ScorerRootWidget(Screen):
    # Header elements from KV
    header_round_label = ObjectProperty(None)
    header_total_time_label = ObjectProperty(None)

    # Player 1 elements from KV
    p1_name_label = ObjectProperty(None)
    p1_score_label = ObjectProperty(None)
    p1_cp_label = ObjectProperty(None)
    p1_player_timer_label = ObjectProperty(None)
    p1_end_turn_button = ObjectProperty(None)
    p1_concede_button = ObjectProperty(None)

    # Player 2 elements from KV
    p2_name_label = ObjectProperty(None)
    p2_score_label = ObjectProperty(None)
    p2_cp_label = ObjectProperty(None)
    p2_player_timer_label = ObjectProperty(None)
    p2_end_turn_button = ObjectProperty(None)
    p2_concede_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numpad_popup = None

    def on_pre_enter(self, *args):
        self.update_ui_from_state() # Call first to try and set up UI elements
        self.update_timer_display(0) # Initial call to set timer text based on current state
        
        gs = App.get_running_app().game_state
        if gs['game_phase'] == 'playing':
            if gs['game_timer']['status'] == 'running':
                # Timer should be running. Ensure Clock.schedule_interval is active.
                is_scheduled = False
                for event in Clock.get_events(): # Check events scheduled for this widget (self)
                    if event.callback == self.update_timer_display:
                        is_scheduled = True
                        break
                if not is_scheduled:
                    print("ScorerRootWidget.on_pre_enter: Timer status is 'running' but not scheduled. Re-scheduling.")
                    Clock.schedule_interval(self.update_timer_display, 1)
                # self.update_timer_display(0) # Already called above
            elif gs['game_timer']['status'] == 'stopped' and gs['game_timer']['start_time'] == 0:
                 print("ScorerRootWidget.on_pre_enter: Game playing, timer stopped & never started. Calling start_timer().")
                 self.start_timer() # This will set status to 'running' and schedule
        # Ensure UI is updated once more in case properties weren't ready on first call
        Clock.schedule_once(lambda dt: self.update_ui_from_state(), 0.05) 

    def update_ui_from_state(self):
        print("ScorerRootWidget: Attempting update_ui_from_state")
        gs = App.get_running_app().game_state

        # Enhanced widget readiness check
        required_widgets = {
            "header_round_label": self.header_round_label,
            "p1_name_label": self.p1_name_label,
            "p1_score_label": self.p1_score_label,
            "p1_cp_label": self.p1_cp_label,
            "p2_name_label": self.p2_name_label,
            "p2_score_label": self.p2_score_label,
            "p2_cp_label": self.p2_cp_label,
            "p1_end_turn_button": self.p1_end_turn_button,
            "p2_end_turn_button": self.p2_end_turn_button,
            "header_total_time_label": self.header_total_time_label,
            "p1_player_timer_label": self.p1_player_timer_label,
            "p2_player_timer_label": self.p2_player_timer_label,
            "p1_concede_button": self.p1_concede_button,
            "p2_concede_button": self.p2_concede_button
        }
        all_ready = True
        for name, widget_ref in required_widgets.items():
            if not widget_ref:
                print(f"ScorerRootWidget: Widget '{name}' not ready yet.")
                all_ready = False
        
        if not all_ready:
            Clock.schedule_once(lambda dt: self.update_ui_from_state(), 0.05) # Increased delay slightly
            print("ScorerRootWidget: Rescheduling update_ui_from_state due to missing widgets.")
            return
        
        print(f"ScorerRootWidget: game_phase = {gs.get('game_phase')}, active_player_id = {gs.get('active_player_id')}")

        # Updated player name logic
        p1_base_name = gs['player1']['name']
        p2_base_name = gs['player2']['name']

        if gs['game_phase'] == "playing":
            if gs["active_player_id"] == 1:
                self.p1_name_label.text = f"{p1_base_name} - Active"
                self.p2_name_label.text = p2_base_name
            elif gs["active_player_id"] == 2:
                self.p1_name_label.text = p1_base_name
                self.p2_name_label.text = f"{p2_base_name} - Active"
            else: # Should not happen often if game is playing, but for robustness
                self.p1_name_label.text = p1_base_name
                self.p2_name_label.text = p2_base_name
        else: # Not playing (e.g. game over, setup)
            self.p1_name_label.text = p1_base_name
            self.p2_name_label.text = p2_base_name
        
        self.p1_score_label.text = str(gs['player1']['total_score'])
        self.p1_cp_label.text = f"Command Points: {gs['player1']['cp']}"
        self.p2_score_label.text = str(gs['player2']['total_score'])
        self.p2_cp_label.text = f"Command Points: {gs['player2']['cp']}"

        # Manage End Turn button visibility and state
        current_gs_active_id = gs.get("active_player_id") # Capture it for this specific decision block
        print(f"ScorerRootWidget.update_ui_from_state: ButtonLogic using active_player_id = {current_gs_active_id} for button visibility.")

        is_playing = gs['game_phase'] == "playing"
        
        # Player 1 Button
        if is_playing and current_gs_active_id == 1:
            self.p1_end_turn_button.opacity = 1
            self.p1_end_turn_button.disabled = False
        else:
            self.p1_end_turn_button.opacity = 0
            self.p1_end_turn_button.disabled = True
        
        # Player 2 Button
        if is_playing and current_gs_active_id == 2:
            self.p2_end_turn_button.opacity = 1
            self.p2_end_turn_button.disabled = False
        else:
            self.p2_end_turn_button.opacity = 0
            self.p2_end_turn_button.disabled = True
        
        print(f"ScorerRootWidget: p1_end_turn_button.opacity={self.p1_end_turn_button.opacity}, .disabled={self.p1_end_turn_button.disabled}")
        print(f"ScorerRootWidget: p2_end_turn_button.opacity={self.p2_end_turn_button.opacity}, .disabled={self.p2_end_turn_button.disabled}")

        # Manage Concede button visibility and state
        if is_playing:
            self.p1_concede_button.opacity = 1
            self.p1_concede_button.disabled = False
            self.p2_concede_button.opacity = 1
            self.p2_concede_button.disabled = False
        else:
            self.p1_concede_button.opacity = 0
            self.p1_concede_button.disabled = True
            self.p2_concede_button.opacity = 0
            self.p2_concede_button.disabled = True

        if gs['game_phase'] == "playing":
            self.header_round_label.text = f"Round {gs['current_round']}"
        elif gs['game_phase'] == "game_over":
            final_round = gs.get('last_round_played', 5)
            self.header_round_label.text = f"Round {final_round} (Game Over)"
        else: 
            self.header_round_label.text = "Round: -"
        print("ScorerRootWidget: update_ui_from_state completed.")

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
        active_player_id = gs.get("active_player_id")
        game_status = gs['game_timer']['status']
        game_phase = gs['game_phase']

        # print(f"update_timer_display: active_id={active_player_id}, timer_status={game_status}, game_phase={game_phase}") # Basic log

        if game_status == 'running':
            elapsed_seconds = time_now - gs['game_timer']['start_time']
            gs['game_timer']['elapsed_display'] = self._format_seconds_to_hms(elapsed_seconds)
        
        if self.header_total_time_label: # Check if property is bound
            self.header_total_time_label.text = f"Total Time: {gs['game_timer']['elapsed_display']}"

        current_segment_duration = 0
        if game_status == 'running' and game_phase == 'playing':
             current_segment_duration = time_now - gs['game_timer']['turn_segment_start_time']

        # Player 1 Timer Update
        p1_key = "player1"
        p1_total_seconds = gs[p1_key]['player_elapsed_time_seconds']
        if active_player_id == 1 and game_status == 'running' and game_phase == 'playing':
            live_total_seconds_p1 = p1_total_seconds + current_segment_duration
            gs[p1_key]['player_time_display'] = self._format_seconds_to_hms(live_total_seconds_p1)
            # print(f"  P1 (Active) timer: base={p1_total_seconds:.2f}, seg_dur={current_segment_duration:.2f}, live_total={live_total_seconds_p1:.2f}")
        else:
            gs[p1_key]['player_time_display'] = self._format_seconds_to_hms(p1_total_seconds)
            # if game_phase == 'playing': print(f"  P1 (Inactive) timer: base={p1_total_seconds:.2f}")

        if self.p1_player_timer_label: 
            self.p1_player_timer_label.text = f"{gs[p1_key]['player_time_display']}"

        # Player 2 Timer Update
        p2_key = "player2"
        p2_total_seconds = gs[p2_key]['player_elapsed_time_seconds']
        if active_player_id == 2 and game_status == 'running' and game_phase == 'playing':
            live_total_seconds_p2 = p2_total_seconds + current_segment_duration
            gs[p2_key]['player_time_display'] = self._format_seconds_to_hms(live_total_seconds_p2)
            # print(f"  P2 (Active) timer: base={p2_total_seconds:.2f}, seg_dur={current_segment_duration:.2f}, live_total={live_total_seconds_p2:.2f}")
        else:
            gs[p2_key]['player_time_display'] = self._format_seconds_to_hms(p2_total_seconds)
            # if game_phase == 'playing': print(f"  P2 (Inactive) timer: base={p2_total_seconds:.2f}")
            
        if self.p2_player_timer_label: 
            self.p2_player_timer_label.text = f"{gs[p2_key]['player_time_display']}"

    def end_turn(self): # Removed player_id argument
        gs = App.get_running_app().game_state
        print(f"--- End Turn Button Pressed ---")
        print(f"Initial state: active_player_id={gs.get('active_player_id')}, game_phase={gs.get('game_phase')}, round={gs.get('current_round')}")

        if gs["game_phase"] != "playing":
            print("End Turn: Game not in 'playing' phase. No action.")
            return

        time_now = time.time()
        outgoing_player_id = gs["active_player_id"]
        print(f"End Turn: Outgoing player_id = {outgoing_player_id}")
        
        if gs['game_timer']['status'] == 'running':
            turn_duration = time_now - gs['game_timer']['turn_segment_start_time']
            gs[f'player{outgoing_player_id}']['player_elapsed_time_seconds'] += turn_duration
            gs[f'player{outgoing_player_id}']['player_time_display'] = self._format_seconds_to_hms(
                gs[f'player{outgoing_player_id}']['player_elapsed_time_seconds']
            )
            print(f"End Turn: Player {outgoing_player_id} turn_duration={turn_duration:.2f}s, total_elapsed={gs[f'player{outgoing_player_id}']['player_elapsed_time_seconds']:.2f}s")

        next_player_id = 2 if outgoing_player_id == 1 else 1
        gs["active_player_id"] = next_player_id
        print(f"End Turn: Active player_id changed to {gs['active_player_id']}")
        newly_active_player_name = gs[f'player{gs["active_player_id"]}']["name"]

        round_advanced_or_game_ended = False
        first_player_of_game_id = gs.get("first_player_of_game_id")
        # Round advances if the outgoing player was NOT the first player of the game (meaning both players have had a turn in this round number)
        if first_player_of_game_id is not None and outgoing_player_id != first_player_of_game_id:
            gs["current_round"] += 1
            round_advanced_or_game_ended = True
            print(f"End Turn: Round advanced to {gs['current_round']}")
        
        if gs["current_round"] > 5: 
            gs["game_phase"] = "game_over"
            gs["last_round_played"] = 5 
            gs["status_message"] = f"Game Over - Round 5 complete" 
            print(f"End Turn: Game Over. Last round was {gs['last_round_played']}. Transitioning to game_over screen.")
            self.stop_timer()
            self.manager.current = 'game_over' 
            return
        else:
            gs["status_message"] = f"Round {gs['current_round']} - {newly_active_player_name}'s Turn"
            gs['game_timer']['turn_segment_start_time'] = time_now 
            print(f"End Turn: New turn segment start_time = {time_now:.2f}")
            print(f"End Turn: Status message = {gs['status_message']}")
            
        print("End Turn: Calling self.update_ui_from_state()")
        self.update_ui_from_state()
        if not round_advanced_or_game_ended or gs["game_phase"] == "playing": # Ensure timer display updates if game still playing
             print("End Turn: Calling self.update_timer_display(0)")
             self.update_timer_display(0)
        App.get_running_app().save_game_state() # Save state after turn ends
        print(f"--- End Turn Processing Complete. Active player: {gs['active_player_id']} ---")

    def player_concedes(self, conceding_player_id):
        gs = App.get_running_app().game_state
        print(f"--- Player {conceding_player_id} Pressed Concede Button ---")

        if gs["game_phase"] != "playing":
            print(f"Concede: Game not in 'playing' phase. No action.")
            return

        winning_player_id = 1 if conceding_player_id == 2 else 2
        conceding_player_name = gs[f'player{conceding_player_id}']['name']
        winning_player_name = gs[f'player{winning_player_id}']['name']

        gs["game_phase"] = "game_over"
        gs["status_message"] = f"{conceding_player_name} concedes. {winning_player_name} wins!"
        # Scores remain as they were when concede was pressed unless specified otherwise
        gs["last_round_played"] = gs["current_round"] # Record the round of concession

        print(f"Concede: Player {conceding_player_id} ({conceding_player_name}) conceded.")
        print(f"Concede: Player {winning_player_id} ({winning_player_name}) wins.")
        print(f"Concede: Game phase set to 'game_over'. Last round played: {gs['last_round_played']}")

        self.stop_timer()
        self.update_ui_from_state() # Update UI to hide buttons, show game over state on labels
        self.manager.current = 'game_over'
        App.get_running_app().save_game_state()
        print(f"--- Concession Processing Complete ---")

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
            App.get_running_app().save_game_state() # Save after processing numpad value
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
            App.get_running_app().save_game_state() # Save after adding CP

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
            App.get_running_app().save_game_state() # Save after removing CP
    
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
        super().__init__(**kwargs)
        self.auto_dismiss = False # Prevent auto-dismissal on outside click
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
        
        winner_text = ""
        raw_status_message = gs.get("status_message", "")
        status_message_lower = raw_status_message.lower()
        print(f"GameOverScreen.on_pre_enter: Raw status_message from game_state: '{raw_status_message}'")

        # Always get player scores from game_state for display
        p1_score = gs['player1']['total_score']
        p2_score = gs['player2']['total_score']

        # Check for concession: looking for "concedes." and "wins!" (note the period)
        if "concedes." in status_message_lower and "wins!" in status_message_lower:
            # Game ended by concession, winner is in the status message
            winner_text = raw_status_message # Use the original casing from game_state as it's already formatted
            print(f"GameOverScreen: Detected concession. Winner text set to: '{winner_text}'")
        else:
            # Game ended normally or status_message format for concession not matched, determine by score
            if p1_score > p2_score:
                winner_text = f"{gs['player1']['name']} Wins by Score!"
            elif p2_score > p1_score:
                winner_text = f"{gs['player2']['name']} Wins by Score!"
            else:
                winner_text = "It's a Tie by Score!"
            print(f"GameOverScreen: No concession detected or message format mismatch. Determined winner by score. P1: {p1_score}, P2: {p2_score}. Winner text: '{winner_text}'")
        
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


class ResumeOrNewScreen(Screen):
    resume_info_label = ObjectProperty(None)
    resume_button = ObjectProperty(None)
    new_game_button = ObjectProperty(None)

    def on_pre_enter(self, *args):
        # Optionally, update the label text if needed, though it can be static
        if self.resume_info_label:
            self.resume_info_label.text = "Saved game data found. Resume or Start New Game?"

    def resume_game_action(self):
        app = App.get_running_app()
        gs = app.game_state
        
        current_phase = gs.get('game_phase')
        target_screen_for_resume = 'name_entry' # Default fallback

        if current_phase == 'playing':
            target_screen_for_resume = 'scorer_root'
        elif current_phase == 'first_turn_setup':
            target_screen_for_resume = 'first_turn_setup'
        elif current_phase == 'deployment_setup':
            target_screen_for_resume = 'deployment_setup'
        # Add other phases here if they are legitimately resumable states
        # For example, if you could resume directly to 'name_entry' under some condition
        # elif current_phase == 'name_entry':
        #     target_screen_for_resume = 'name_entry'
        else:
            # If the phase is unknown or not considered directly resumable to a specific game screen,
            # it might indicate an issue or a need to go to a more general starting point.
            # However, given our load_game_state logic, a "resumable" status should imply a valid phase.
            print(f"ResumeOrNewScreen: Warning - Unexpected game_phase '{current_phase}' for resume. Defaulting to 'scorer_root'.")
            target_screen_for_resume = 'scorer_root' # Fallback to scorer if phase is unusual but game was 'resumable'

        print(f"ResumeOrNewScreen: Resuming game. Determined target screen: '{target_screen_for_resume}' from game_phase: '{current_phase}'")
        
        # Special handling if resuming directly to scorer_root for timer and UI updates
        if target_screen_for_resume == 'scorer_root':
            scorer_screen = app.screen_manager.get_screen('scorer_root')
            if scorer_screen:
                # Ensure UI is updated based on the loaded state
                Clock.schedule_once(lambda x: scorer_screen.update_ui_from_state(), 0.05)
                # Handle timer state
                if gs.get('game_phase') == 'playing': # Double check, should be true if going to scorer_root
                    if gs.get('game_timer', {}).get('status') == 'running':
                        is_scheduled = False
                        for event in Clock.get_events():
                            if event.callback == scorer_screen.update_timer_display:
                                is_scheduled = True
                                break
                        if not is_scheduled:
                            print("ResumeOrNewScreen (to scorer_root): Timer status 'running', re-scheduling.")
                            Clock.schedule_interval(scorer_screen.update_timer_display, 1)
                    elif gs.get('game_timer', {}).get('status') == 'stopped' and gs.get('game_timer', {}).get('start_time', 0) == 0:
                        # This condition implies game is playing, timer was never started (e.g. quit before first turn fully ended)
                        # or was explicitly stopped but should now resume.
                        print("ResumeOrNewScreen (to scorer_root): Game playing, timer seems stopped/reset. Calling start_timer.")
                        scorer_screen.start_timer()
                    else:
                         # Ensure timer display reflects current state even if not actively running (e.g., was paused)
                        Clock.schedule_once(lambda x: scorer_screen.update_timer_display(0), 0.1)

        app.screen_manager.current = target_screen_for_resume

    def start_new_game_from_resume_screen_action(self):
        print("ResumeOrNewScreen: Starting new game.")
        App.get_running_app().start_new_game_flow() # This resets state and goes to name_entry


class ScorerApp(App):
    SAVE_FILE_NAME = "game_state.json"
    SPLASH_DURATION = 10 # Duration in seconds for the splash screen

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
        if self.root and self.root.current == 'scorer_root':
            scorer_screen = self.root.get_screen('scorer_root')
            if scorer_screen:
                scorer_screen.stop_timer()
        
        self.reset_game_state_to_default()
        self.save_game_state() 
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
        """
        Loads game state from SAVE_FILE_NAME.
        Initializes to default if no valid save file is found or if the game was over.
        Returns a status: "no_save", "game_over", or "resumable".
        """
        save_file_path = self.get_save_file_path()
        try:
            if os.path.exists(save_file_path):
                with open(save_file_path, 'r') as f:
                    loaded_state = json.load(f)
                    # Basic validation: check if it's a dictionary and has player keys
                    if isinstance(loaded_state, dict) and \
                       'player1' in loaded_state and 'player2' in loaded_state and \
                       'game_phase' in loaded_state: # Ensure game_phase exists
                        
                        self.game_state.update(loaded_state) # Load valid state
                        print(f"Game state loaded from {save_file_path}")
                        
                        if self.game_state.get('game_phase') == 'game_over':
                            print("Loaded game state is 'game_over'. Treating as new game for screen choice.")
                            # We've loaded it, but for screen determination, it's like starting fresh for 'name_entry'
                            return "game_over" 
                        else:
                            # Game is not over, or game_phase is something else (e.g. playing, setup)
                            print(f"Resumable game state loaded. Phase: {self.game_state.get('game_phase')}")
                            return "resumable"
                    else:
                        print(f"Save file {save_file_path} is incomplete or malformed. Starting new game state.")
                        self.initialize_game_state() # Reset to default
                        return "no_save"
            else:
                print("No save file found. Initializing new game state.")
                self.initialize_game_state() # Ensure clean state if no file
                return "no_save"
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {save_file_path}. Initializing new game state.")
            self.initialize_game_state() # Reset to default
            return "no_save"
        except Exception as e:
            print(f"An unexpected error occurred during load_game_state: {e}. Initializing new game state.")
            self.initialize_game_state() # Reset to default
            return "no_save"

    def _determine_screen_from_gamestate(self):
        """
        Determines the initial screen based on the loaded game state.
        """
        load_status = self.load_game_state() # This now populates self.game_state

        if load_status == "resumable":
            # Check if essential player names are present for a truly resumable game.
            # This prevents going to resume_or_new if the game state is somehow partial
            # before names are even entered (though load_game_state's initialize should prevent this).
            p1_name = self.game_state.get('player1', {}).get('name')
            p2_name = self.game_state.get('player2', {}).get('name')
            if p1_name and p2_name:
                print(f"Determined screen: resume_or_new (status: {load_status})")
                return 'resume_or_new'
            else:
                # If names are missing even if it thought it was resumable, something is off. Start new.
                print("Resumable state but missing player names. Defaulting to name_entry.")
                self.initialize_game_state() # Ensure a fresh start if names were bad
                return 'name_entry'
        elif load_status == "game_over":
            print(f"Determined screen: name_entry (status: {load_status}, game was over)")
            # Game was over, so we want to start a new game by going to name entry.
            # Ensure a clean slate for the new game by re-initializing
            self.initialize_game_state()
            return 'name_entry'
        else: # "no_save" or any other unhandled case from load_game_state
            print(f"Determined screen: name_entry (status: {load_status})")
            # No save or bad save, so start new. initialize_game_state was already called in load_game_state.
            return 'name_entry'

    def build(self):
        self.game_state = self._get_default_game_state() 
        self.screen_manager = ScreenManager()

        self.screen_manager.add_widget(SplashScreen(name='splash_screen'))
        self.screen_manager.add_widget(ResumeOrNewScreen(name='resume_or_new'))
        self.screen_manager.add_widget(NameEntryScreen(name='name_entry'))
        self.screen_manager.add_widget(DeploymentSetupScreen(name='deployment_setup'))
        self.screen_manager.add_widget(FirstTurnSetupScreen(name='first_turn_setup'))
        self.screen_manager.add_widget(ScorerRootWidget(name='scorer_root'))
        self.screen_manager.add_widget(GameOverScreen(name='game_over'))

        # Directly determine the target screen after splash.
        # _determine_screen_from_gamestate now handles loading and deciding.
        actual_initial_screen_after_splash = self._determine_screen_from_gamestate()
        print(f"Build: Initial screen after splash will be '{actual_initial_screen_after_splash}'.")
            
        self.screen_manager.current = 'splash_screen'
        Clock.schedule_once(lambda dt: self.transition_from_splash(actual_initial_screen_after_splash, dt), self.SPLASH_DURATION)
        
        # Explicitly set fullscreen and borderless for Linux just before returning screen_manager
        if platform.system() == "Linux":
            Window.fullscreen = True
            Window.borderless = True
            print("Linux detected in build(): Set Window.fullscreen=True and Window.borderless=True")

        return self.screen_manager

    def transition_from_splash(self, target_screen_name, dt):
        """Transitions from splash screen to the target screen."""
        print(f"Transitioning from splash to {target_screen_name}")
        self.screen_manager.current = target_screen_name

        if target_screen_name == 'scorer_root':
            scorer_screen = self.screen_manager.get_screen('scorer_root')
            if scorer_screen:
                gs = self.game_state
                if gs.get('game_phase') == 'playing':
                    if gs.get('game_timer', {}).get('status') == 'running':
                        is_scheduled = False
                        for event in Clock.get_events(): 
                            if event.callback == scorer_screen.update_timer_display:
                                is_scheduled = True
                                break
                        if not is_scheduled:
                            print("ScorerApp.transition_from_splash: Timer status 'running', re-scheduling for scorer_root.")
                            Clock.schedule_interval(scorer_screen.update_timer_display, 1)
                    elif gs.get('game_timer', {}).get('status') == 'stopped' and gs.get('game_timer', {}).get('start_time', 0) == 0:
                        print("ScorerApp.transition_from_splash: Game playing, timer stopped & never started. Calling start_timer for scorer_root.")
                        scorer_screen.start_timer()
                # Ensure UI is updated after transition
                Clock.schedule_once(lambda x: scorer_screen.update_ui_from_state(), 0.05)

    def initialize_game_state(self): 
        self.game_state = self._get_default_game_state() 
        self.load_game_state()

    def on_stop(self):
        print("Application stopping. Saving game state...")
        self.save_game_state()

if __name__ == '__main__':
    # Conditionally set Window.size for non-Linux environments
    if platform.system() != "Linux":
        Window.size = (800, 480) # Explicitly set window size before run for dev
    ScorerApp().run() 