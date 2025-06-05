import platform # For OS detection
import os # Import os

from kivy.config import Config # Ensure Config is imported AFTER env vars are set

# OS-specific graphics configuration
os_type = platform.system()
if os_type == "Linux":  # Assuming Raspberry Pi OS reports as Linux
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'show_cursor', '0') # Hide cursor for kiosk on Pi
    Config.set('graphics', 'borderless', '1') # Attempt to set borderless early for Pi
    Config.set('graphics', 'window_state', 'maximized') # Add attempt to maximize window state
    Config.set('kivy', 'keyboard_mode', 'dock') # Enable docked keyboard for Pi
else:  # Default to development mode (e.g., macOS, Windows)
    Config.set('graphics', 'fullscreen', '0') # Ensure not fullscreen
    Config.set('graphics', 'show_cursor', '1') # Show cursor for dev
    # Set fixed size for development environments only
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '480')
    Config.set('graphics', 'resizable', False)

from kivy.core.window import Window # Ensure Window is imported AFTER Config changes

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
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition # Added ScreenManager, Screen, FadeTransition
from kivy.clock import Clock # Added for timer updates
from kivy.uix.textinput import TextInput # Added for player names
from kivy.uix.vkeyboard import VKeyboard # Import VKeyboard
from kivy.core.text import LabelBase # For registering fonts by name
from db.integration import reset_db_for_new_game_sync
from websocket_server import WebSocketServer

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
    def on_enter(self, *args):
        print("SplashScreen: on_enter called")
        app = App.get_running_app()
        if not app or not app.root:
            print("SplashScreen: on_enter called, but app or app.root is not yet available. Ignoring this call.")
            return

        print(f"SplashScreen: Scheduling transition to {app.target_screen_after_splash} in {app.VISIBLE_SPLASH_TIME}s")
        Clock.schedule_once(lambda dt: app.transition_from_splash(app.target_screen_after_splash, dt), app.VISIBLE_SPLASH_TIME)

    def on_leave(self, *args):
        print("SplashScreen: on_leave called")

class NameEntryScreen(Screen):
    player1_name_input = ObjectProperty(None)
    player2_name_input = ObjectProperty(None)
    continue_button = ObjectProperty(None)
    active_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_added = False
        self.vkeyboard = None

    def set_active_input(self, text_input):
        if text_input.focus:
            self.active_input = text_input
            if self.vkeyboard:
                self.vkeyboard.target = text_input
        else:
            # If the input that just lost focus is the active one, clear it
            if self.active_input == text_input:
                self.active_input = None
                if self.vkeyboard:
                    self.vkeyboard.target = None

    def on_enter(self, *args):
        # Defer the field initialization to the next frame to ensure widgets are ready
        Clock.schedule_once(self._initialize_fields)

        # Dynamically add the VKeyboard on Linux platforms
        if platform.system() == "Linux" and not self._keyboard_added:
            self.vkeyboard = VKeyboard(size_hint_y=None)
            self.ids.main_layout.add_widget(self.vkeyboard)
            self._keyboard_added = True

    def _initialize_fields(self, dt):
        """Initializes the text input fields with names from the game state."""
        app = App.get_running_app()
        if not self.player1_name_input or not self.player2_name_input:
            print("ERROR: NameEntryScreen fields not ready, rescheduling initialization.")
            Clock.schedule_once(self._initialize_fields, 0.05)
            return

        p1_name = app.game_state.get('player1', {}).get('name', 'Player 1')
        p2_name = app.game_state.get('player2', {}).get('name', 'Player 2')
        self.player1_name_input.text = p1_name
        self.player2_name_input.text = p2_name
        # Initial validation check
        self.on_name_input(self.player1_name_input, p1_name)

    def on_name_input(self, instance, value):
        # Guard clause: Do not proceed if widgets aren't linked yet.
        if not all([self.player1_name_input, self.player2_name_input, self.continue_button]):
            return

        # Enable continue button only if both fields have non-empty, non-whitespace text
        p1_name = self.player1_name_input.text.strip()
        p2_name = self.player2_name_input.text.strip()
        self.continue_button.disabled = not (p1_name and p2_name)

    def on_text_validate_p1(self, instance):
        # When Enter is pressed on P1 input, focus P2 input
        self.player2_name_input.focus = True

    def on_text_validate_p2(self, instance):
        # When Enter is pressed on P2 input, if valid, proceed
        if not self.continue_button.disabled:
            self.save_names_and_proceed()

    def save_names_and_proceed(self):
        app = App.get_running_app()
        p1_name = self.player1_name_input.text.strip()
        p2_name = self.player2_name_input.text.strip()

        # Update game state
        app.game_state['player1']['name'] = p1_name
        app.game_state['player2']['name'] = p2_name
        app.game_state['game_phase'] = 'deployment'
        app.save_game_state()

        # Switch screen
        app.switch_screen('deployment_setup')

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
        app = App.get_running_app()
        app.game_state['game_phase'] = 'first_turn'
        app.save_game_state()
        app.switch_screen('first_turn_setup')

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
        app = App.get_running_app()
        app.game_state['game_phase'] = 'game_play'
        app.game_state['current_round'] = 1
        app.save_game_state()

        # Get the scorer screen and start its timers/UI updates
        scorer_screen = app.root.get_screen('scorer_root')
        scorer_screen.start_timers_and_ui()

        app.switch_screen('scorer_root')

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
        """Ensure UI and timers are correctly initialized when entering the screen."""
        self.update_ui_from_state() # Initial UI setup from state
        
        gs = App.get_running_app().game_state
        if gs.get('game_phase') == 'game_play':
            if gs.get('game_timer', {}).get('status') == 'running':
                # If state says running, make sure the clock is scheduled.
                is_scheduled = False
                for event in Clock.get_events():
                    if event.callback == self.update_timer_display:
                        is_scheduled = True
                        break
                if not is_scheduled:
                    Clock.schedule_interval(self.update_timer_display, 1)
            else:
                # If game is playing but state says timer is stopped, start it.
                self.start_timer()

        # Final check to ensure UI is updated after a short delay
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

        if gs['game_phase'] == "game_play":
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

        is_playing = gs['game_phase'] == "game_play"
        
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

        if gs['game_phase'] == "game_play":
            self.header_round_label.text = f"Round {gs['current_round']}"
        elif gs['game_phase'] == "game_over":
            final_round = gs.get('last_round_played', 5)
            self.header_round_label.text = f"Round {final_round} (Game Over)"
        else: 
            self.header_round_label.text = "Round: -"
        print("ScorerRootWidget: update_ui_from_state completed.")

    def start_timers_and_ui(self):
        """A single method to call when transitioning to this screen to ensure UI and timers are correctly initialized."""
        self.update_ui_from_state() # Initial UI setup from state
        
        gs = App.get_running_app().game_state
        if gs.get('game_phase') == 'game_play':
            if gs.get('game_timer', {}).get('status') == 'running':
                # If state says running, make sure the clock is scheduled.
                is_scheduled = False
                for event in Clock.get_events():
                    if event.callback == self.update_timer_display:
                        is_scheduled = True
                        break
                if not is_scheduled:
                    Clock.schedule_interval(self.update_timer_display, 1)
            else:
                # If game is playing but state says timer is stopped, start it.
                self.start_timer()

        # Final check to ensure UI is updated after a short delay, as widgets might not be ready instantly.
        Clock.schedule_once(lambda dt: self.update_ui_from_state(), 0.05)

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
        if game_status == 'running' and game_phase == 'game_play':
             current_segment_duration = time_now - gs['game_timer']['turn_segment_start_time']

        # Player 1 Timer Update
        p1_key = "player1"
        p1_total_seconds = gs[p1_key]['player_elapsed_time_seconds']
        if active_player_id == 1 and game_status == 'running' and game_phase == 'game_play':
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
        if active_player_id == 2 and game_status == 'running' and game_phase == 'game_play':
            live_total_seconds_p2 = p2_total_seconds + current_segment_duration
            gs[p2_key]['player_time_display'] = self._format_seconds_to_hms(live_total_seconds_p2)
            # print(f"  P2 (Active) timer: base={p2_total_seconds:.2f}, seg_dur={current_segment_duration:.2f}, live_total={live_total_seconds_p2:.2f}")
        else:
            gs[p2_key]['player_time_display'] = self._format_seconds_to_hms(p2_total_seconds)
            # if game_phase == 'playing': print(f"  P2 (Inactive) timer: base={p2_total_seconds:.2f}")
            
        if self.p2_player_timer_label: 
            self.p2_player_timer_label.text = f"{gs[p2_key]['player_time_display']}"

    def end_turn(self):
        gs = App.get_running_app().game_state
        print(f"--- End Turn Button Pressed ---")
        print(f"Initial state: active_player_id={gs.get('active_player_id')}, game_phase={gs.get('game_phase')}, round={gs.get('current_round')}")

        if gs["game_phase"] != "game_play":
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

        first_player_of_game_id = gs.get("first_player_of_game_id")
        is_second_player_turn_end = (first_player_of_game_id is not None and outgoing_player_id != first_player_of_game_id)

        # Game Over Check: This is the absolute end condition.
        if gs["current_round"] == 5 and is_second_player_turn_end:
            gs["game_phase"] = "game_over"
            gs["last_round_played"] = 5
            gs["status_message"] = "Game Over - Round 5 complete"
            print("End Turn: Game Over. Final turn of Round 5 has ended.")
            self.stop_timer()
            App.get_running_app().switch_screen('game_over')
            App.get_running_app().save_game_state() # Save final state
            return

        # Round Advancement: Only happens if the game is not over.
        if is_second_player_turn_end:
            gs["current_round"] += 1
            print(f"End Turn: Round advanced to {gs['current_round']}")

        gs["status_message"] = f"Round {gs['current_round']} - {newly_active_player_name}'s Turn"
        gs['game_timer']['turn_segment_start_time'] = time_now 
        print(f"End Turn: New turn segment start_time = {time_now:.2f}")
        print(f"End Turn: Status message = {gs['status_message']}")
            
        print("End Turn: Calling self.update_ui_from_state()")
        self.update_ui_from_state()
        self.update_timer_display(0)
        App.get_running_app().save_game_state() # Save state after turn ends
        print(f"--- End Turn Processing Complete. Active player: {gs['active_player_id']} ---")

    def player_concedes(self, conceding_player_id):
        gs = App.get_running_app().game_state
        print(f"--- Player {conceding_player_id} Pressed Concede Button ---")

        if gs["game_phase"] != "game_play":
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
        App.get_running_app().switch_screen('game_over')
        App.get_running_app().save_game_state()
        print(f"--- Concession Processing Complete ---")

    def open_score_numpad(self, player_id_to_score):
        gs = App.get_running_app().game_state
        if gs["game_phase"] != "game_play":
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
        if gs["game_phase"] != "game_play": return
        player_key = f"player{player_id}"
        if player_key in gs:
            gs[player_key]["cp"] = max(0, gs[player_key]["cp"] + amount)
            gs["status_message"] = f"{gs[player_key]['name']} CP Updated"
            self.update_ui_from_state()
            App.get_running_app().save_game_state() # Save after adding CP

    def remove_cp(self, player_id, amount=1): 
        gs = App.get_running_app().game_state
        if gs["game_phase"] != "game_play": return
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
            if gs['game_phase'] == 'game_play' and gs.get('active_player_id'):
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
        
        # Use .get() for safe access to potentially missing keys
        p1_stats = gs.get('player1', {})
        p2_stats = gs.get('player2', {})
        timer_stats = gs.get('game_timer', {})

        winner_text = ""
        raw_status_message = gs.get("status_message", "Game Over")
        status_message_lower = raw_status_message.lower()
        print(f"GameOverScreen.on_pre_enter: Raw status_message from game_state: '{raw_status_message}'")

        p1_score = p1_stats.get('total_score', 0)
        p2_score = p2_stats.get('total_score', 0)

        if "concedes." in status_message_lower and "wins!" in status_message_lower:
            winner_text = raw_status_message
            print(f"GameOverScreen: Detected concession. Winner text set to: '{winner_text}'")
        else:
            p1_name = p1_stats.get('name', 'Player 1')
            p2_name = p2_stats.get('name', 'Player 2')
            if p1_score > p2_score:
                winner_text = f"{p1_name} Wins by Score!"
            elif p2_score > p1_score:
                winner_text = f"{p2_name} Wins by Score!"
            else:
                winner_text = "It's a Tie by Score!"
            print(f"GameOverScreen: Determined winner by score. P1: {p1_score}, P2: {p2_score}. Winner text: '{winner_text}'")
        
        if self.result_status_label: self.result_status_label.text = winner_text
        
        # Populate Player 1 Stats safely
        if self.p1_final_name_label: self.p1_final_name_label.text = f"Player: {p1_stats.get('name', 'P1')}"
        if self.p1_final_score_label: self.p1_final_score_label.text = f"Final Score: {p1_score}"
        if self.p1_final_cp_label: self.p1_final_cp_label.text = f"CP Remaining: {p1_stats.get('cp', 0)}"
        if self.p1_final_time_label: self.p1_final_time_label.text = f"Time Played: {p1_stats.get('player_time_display', '00:00:00')}"

        # Populate Player 2 Stats safely
        if self.p2_final_name_label: self.p2_final_name_label.text = f"Player: {p2_stats.get('name', 'P2')}"
        if self.p2_final_score_label: self.p2_final_score_label.text = f"Final Score: {p2_score}"
        if self.p2_final_cp_label: self.p2_final_cp_label.text = f"CP Remaining: {p2_stats.get('cp', 0)}"
        if self.p2_final_time_label: self.p2_final_time_label.text = f"Time Played: {p2_stats.get('player_time_display', '00:00:00')}"

        # Populate Game Stats safely
        if self.total_game_time_label: self.total_game_time_label.text = f"Total Game Time: {timer_stats.get('elapsed_display', '00:00:00')}"
        if self.rounds_played_label: self.rounds_played_label.text = f"Rounds Played: {gs.get('last_round_played', 5)}"

    def start_new_game(self):
        app = App.get_running_app()
        app.start_new_game_flow()

    def exit_app_from_game_over(self):
        App.get_running_app().stop()


class ResumeOrNewScreen(Screen):
    resume_info_label = ObjectProperty(None)
    resume_button = ObjectProperty(None)
    new_game_button = ObjectProperty(None)

    def on_enter(self, *args):
        # Optional: Update the label text with more specific info if needed
        app = App.get_running_app()
        phase = app.game_state.get('game_phase')
        p1_name = app.game_state.get('player1', {}).get('name', 'P1')
        p2_name = app.game_state.get('player2', {}).get('name', 'P2')
        self.resume_info_label.text = f"Found saved game for {p1_name} vs {p2_name} in phase '{phase}'. Resume?"

    def resume_game_action(self):
        app = App.get_running_app()
        target_screen = app._get_screen_for_phase(app.game_state.get('game_phase'))
        app.switch_screen(target_screen)

    def start_new_game_from_resume_screen_action(self):
        app = App.get_running_app()
        app.start_new_game_flow()

class ScorerApp(App):
    SAVE_FILE_NAME = "game_state.json"
    VISIBLE_SPLASH_TIME = 4 # Desired visible time for the splash screen
    target_screen_after_splash = None  # Add this attribute

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = self._get_default_game_state()
        self.websocket_server = WebSocketServer()
        self.websocket_server.set_game_state_callback(self.get_game_state)
        self.load_game_state()
        self.websocket_server.start()

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

    def show_error_popup(self, title, message):
        """Show an error popup with the given title and message."""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        message_label = Label(text=message, text_size=(self.root.width * 0.8, None), size_hint_y=None, height=dp(100))
        ok_button = Button(text='OK', size_hint_y=None, height=dp(40))
        
        content.add_widget(message_label)
        content.add_widget(ok_button)
        
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        ok_button.bind(on_press=popup.dismiss)
        popup.open()

    def start_new_game_flow(self):
        print("Starting new game flow...")
        # Stop timer on current game screen if it exists and is active
        if self.root and self.root.current == 'scorer_root':
            scorer_screen = self.root.get_screen('scorer_root')
            if scorer_screen:
                scorer_screen.stop_timer()
        
        # Reset the database for a new game
        try:
            from db.integration import reset_db_for_new_game_sync
            reset_db_for_new_game_sync()
            print("Database reset successful")
        except Exception as e:
            error_msg = f"Error resetting database: {e}\nThe game will continue, but some features may be limited."
            print(error_msg)
            self.show_error_popup("Database Error", error_msg)
            # Continue with game state reset even if database reset fails
            # This ensures the application remains functional
        
        self.reset_game_state_to_default()
        self.game_state['game_phase'] = 'name_entry' # Explicitly set the phase
        self.save_game_state() # This contains the broadcast call
        self.websocket_server.broadcast_game_state() # Explicitly broadcast again for robustness
        if self.root:
            self.switch_screen('name_entry')

    def get_save_file_path(self):
        return os.path.join(self.user_data_dir, self.SAVE_FILE_NAME)

    def save_game_state(self):
        """Save the current game state to a file"""
        try:
            with open(self.get_save_file_path(), 'w') as f:
                json.dump(self.game_state, f)
            # Broadcast the updated game state to all connected clients
            self.websocket_server.broadcast_game_state()
        except Exception as e:
            print(f"Error saving game state: {e}")

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
                            print("Loaded game state is 'game_over', but treating as resumable to show final screen.")
                            return "resumable"
                        else:
                            # Game is not over, or game_phase is something else (e.g. playing, setup)
                            print(f"Resumable game state loaded. Phase: {self.game_state.get('game_phase')}")
                            return "resumable"
                    else:
                        print(f"Save file {save_file_path} is incomplete or malformed. Starting new game state.")
                        self.game_state = self._get_default_game_state() # Reset to default
                        return "no_save"
            else:
                print("No save file found. Initializing new game state.")
                self.game_state = self._get_default_game_state() # Ensure clean state if no file
                return "no_save"
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {save_file_path}. Initializing new game state.")
            self.game_state = self._get_default_game_state() # Reset to default
            return "no_save"
        except Exception as e:
            print(f"An unexpected error occurred during load_game_state: {e}. Initializing new game state.")
            self.game_state = self._get_default_game_state() # Reset to default
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
        print("ScorerApp.build(): Method started at", time.time())
        # Initialize game state
        self.initialize_game_state()
        print("ScorerApp.build(): Game state initialized.")

        # Create the screen manager
        self.screen_manager = ScreenManager()
        print("ScorerApp.build(): ScreenManager created.")

        # Determine which screen to show after splash
        self.target_screen_after_splash = self._determine_screen_from_gamestate()
        print(f"ScorerApp.build(): Target screen after splash: {self.target_screen_after_splash}")

        # Add the splash screen first
        self.screen_manager.add_widget(SplashScreen(name='splash_screen'))
        print("ScorerApp.build(): SplashScreen added to ScreenManager.")
        self.screen_manager.add_widget(ResumeOrNewScreen(name='resume_or_new'))
        self.screen_manager.add_widget(NameEntryScreen(name='name_entry'))
        self.screen_manager.add_widget(DeploymentSetupScreen(name='deployment_setup'))
        self.screen_manager.add_widget(FirstTurnSetupScreen(name='first_turn_setup'))
        self.screen_manager.add_widget(ScorerRootWidget(name='scorer_root'))
        self.screen_manager.add_widget(GameOverScreen(name='game_over'))
        print("ScorerApp.build(): All game screens added to ScreenManager.")

        # --- Point of setting splash screen current ---
        time_before_splash_current = time.time()
        print(f"ScorerApp.build(): About to set 'splash_screen' as current. Time elapsed since build start: {time_before_splash_current - time.time():.4f}s")
        self.switch_screen('splash_screen')
        # ---------------------------------------------
        
        if platform.system() == "Linux":
            Window.fullscreen = True
            Window.borderless = True
            print("ScorerApp.build(): Linux detected - Window.fullscreen and Window.borderless set.")

        build_end_time = time.time()
        print(f"ScorerApp.build(): Method finished. Total time in build(): {build_end_time - time.time():.4f}s")
        return self.screen_manager

    def transition_from_splash(self, target_screen_name, dt):
        print(f"ScorerApp.transition_from_splash(): Transitioning to {target_screen_name}")
        if not target_screen_name:
            print("ScorerApp.transition_from_splash(): No target screen specified, defaulting to 'resume_or_new'")
            target_screen_name = 'resume_or_new'
        
        try:
            self.switch_screen(target_screen_name)
            print(f"ScorerApp.transition_from_splash(): Successfully transitioned to {target_screen_name}")
        except Exception as e:
            print(f"ScorerApp.transition_from_splash(): Error during transition: {str(e)}")
            # Fallback to resume_or_new screen if transition fails
            self.switch_screen('resume_or_new')

    def initialize_game_state(self): 
        self.game_state = self._get_default_game_state() 

    def on_stop(self):
        """Called when the application is stopping"""
        self.websocket_server.stop()
        self.save_game_state()

    def update_score(self, player_id, new_score):
        """Update a player's score and broadcast the change"""
        player_key = f"player{player_id}"
        if player_key in self.game_state:
            self.game_state[player_key]["total_score"] = new_score
            self.save_game_state()
            self.websocket_server.broadcast_score_update(player_id, new_score)

    def update_cp(self, player_id, new_cp):
        """Update a player's CP and broadcast the change"""
        player_key = f"player{player_id}"
        if player_key in self.game_state:
            self.game_state[player_key]["cp"] = new_cp
            self.save_game_state()
            self.websocket_server.broadcast_cp_update(player_id, new_cp)

    def update_timer(self, timer_data):
        """Update timer data and broadcast the change"""
        self.game_state['game_timer'].update(timer_data)
        self.save_game_state()
        self.websocket_server.broadcast_timer_update(timer_data)

    def update_round(self, round_number):
        """Update the current round and broadcast the change"""
        self.game_state['current_round'] = round_number
        self.save_game_state()
        self.websocket_server.broadcast_round_update(round_number)

    def update_game_phase(self, phase):
        """Update the game phase and broadcast the change"""
        self.game_state['game_phase'] = phase
        self.save_game_state()
        self.websocket_server.broadcast_game_phase_update(phase)

    def get_game_state(self):
        """
        Returns a sanitized, deep copy of the game state suitable for clients.
        This acts as a sanitization layer between the server's internal state
        and what clients receive.
        """
        # Create a deep copy to avoid modifying the internal state accidentally
        sanitized_state = json.loads(json.dumps(self.game_state))

        # --- Sanitization and Rule Enforcement ---

        # 1. Clamp the round number to a valid client-facing range (1-5)
        # The internal state can go to 6 briefly, but clients should never see that.
        if sanitized_state.get('current_round', 0) > 5:
            sanitized_state['current_round'] = 5

        # 2. Translate internal-only screens/phases into client-friendly phases.
        current_screen = self.root.current
        # If the app is on the "Resume or New" screen, the client should think
        # it's in the 'setup' phase to prevent showing a stale 'Game Over' screen.
        if current_screen == 'resume_or_new':
            sanitized_state['game_phase'] = 'setup'
        
        # If the app is in deployment or first turn setup, the client should be
        # in a setup phase (like 'name_entry') to not show the game board.
        server_phase = sanitized_state.get('game_phase')
        if server_phase in ['name_entry', 'deployment', 'first_turn']:
            sanitized_state['game_phase'] = 'setup'

        # 3. Remove fields that are not relevant to the client.
        # This reduces payload size and prevents leaking internal-only data.
        for player in ['player1', 'player2']:
            # Remove internal roll data and raw second counts.
            # Keep 'player_time_display' as the client uses it directly.
            for field in ['deployment_roll', 'first_turn_roll', 'player_elapsed_time_seconds']:
                if field in sanitized_state.get(player, {}):
                    del sanitized_state[player][field]

        # Also remove internal-only timer fields
        if 'game_timer' in sanitized_state:
            for field in ['start_time', 'turn_segment_start_time']:
                if field in sanitized_state['game_timer']:
                    del sanitized_state['game_timer'][field]

        return sanitized_state

    def switch_screen(self, screen_name):
        self.root.transition = FadeTransition(duration=0.2)
        self.root.current = screen_name

    def on_start(self):
        self.load_game_state()
        self._determine_screen_from_gamestate()

    def _get_screen_for_phase(self, phase):
        if phase == 'deployment':
            return 'deployment_setup'
        elif phase == 'first_turn':
            return 'first_turn_setup'
        elif phase == 'game_play':
            return 'scorer_root'
        else:
            return 'name_entry'

if __name__ == '__main__':
    # Conditionally set Window.size for non-Linux environments
    if platform.system() != "Linux":
        Window.size = (800, 480) # Explicitly set window size before run for dev
    ScorerApp().run() 