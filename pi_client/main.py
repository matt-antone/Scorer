import kivy
import json
import threading
import logging
from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from kivy.app import App
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen

# Absolute imports from pi_client package
from pi_client.widgets.root_widget import ScorerRootWidget
from pi_client.screens.splash_screen import SplashScreen
from pi_client.screens.name_entry_screen import NameEntryScreen
from pi_client.screens.deployment_setup_screen import DeploymentSetupScreen
from pi_client.screens.initiative_screen import InitiativeScreen
from pi_client.screens.scoreboard_screen import ScoreboardScreen
from pi_client.widgets.header_widget import HeaderWidget
from pi_client.widgets.number_pad_popup import NumberPadPopup
from pi_client.screens.resume_or_new_screen import ResumeOrNewScreen
from pi_client.state import GameState, GameStatus
from pi_client.screens.game_over_screen import GameOverScreen

kivy.require('2.3.0')

# Set up logging
logging.basicConfig(level=logging.INFO)

# ----------------- FLASK & SOCKETIO SETUP -----------------
# Correctly point to the client's build directory, relative to this script
build_dir = 'client/build'
flask_app = Flask(__name__, static_folder=f'{build_dir}/static', template_folder=build_dir)
socketio = SocketIO(flask_app, async_mode='eventlet')

@flask_app.route('/')
def serve_react_app():
    return send_from_directory(build_dir, 'index.html')

@flask_app.route('/<path:path>')
def serve_react_static_files(path):
    # This serves files from the 'static' folder as well as other assets like manifest.json
    return send_from_directory(build_dir, path)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

def run_flask_app():
    # Use a specific port to avoid conflicts
    socketio.run(flask_app, host='0.0.0.0', port=5001, debug=False)

# ----------------- KIVY APP SETUP -----------------

class ScorerApp(App):
    game_state = {}

    def build(self):
        self.load_game_state()
        # Start the Flask server in a background thread
        flask_thread = threading.Thread(target=run_flask_app)
        flask_thread.daemon = True
        flask_thread.start()
        # Set up the ScreenManager with all screens
        self.sm = ScreenManager()
        self.sm.add_widget(SplashScreen(name='splash'))
        self.sm.add_widget(ResumeOrNewScreen(name='resume_or_new'))
        self.sm.add_widget(NameEntryScreen(name='name_entry'))
        self.sm.add_widget(DeploymentSetupScreen(name='deployment_setup'))
        self.sm.add_widget(InitiativeScreen(name='initiative'))
        self.sm.add_widget(ScoreboardScreen(name='scoreboard'))
        self.sm.add_widget(GameOverScreen(name='game_over'))
        # Decide which screen to show after splash
        self.sm.current = 'splash'
        return self.sm

    def after_splash(self):
        # Called after splash screen tasks are done and user presses START
        if self.should_resume_game():
            print('after_splash: switching to resume_or_new')
            self.sm.current = 'resume_or_new'
        else:
            print('after_splash: switching to name_entry')
            self.sm.current = 'name_entry'

    def should_resume_game(self):
        # Returns True if a valid, in-progress game is found
        # Check if we have a current player and round number
        current_player = self.game_state.get('current_player_name')
        current_round = self.game_state.get('current_round', 0)
        first_turn_player = self.game_state.get('first_turn_player_name')
        game_ended = self.game_state.get('game_ended', False)
        
        # A game is in progress if we have a current player and round number
        # and we're not in the initial setup state, and the game hasn't ended
        return (current_player is not None and 
                current_round > 0 and 
                first_turn_player is not None and
                not game_ended)

    def on_stop(self):
        self.save_game_state()

    def get_persistent_storage_path(self):
        return self.user_data_dir + '/game_state.json'

    def save_game_state(self):
        path = self.get_persistent_storage_path()
        # Convert GameStatus enum to string before saving
        state_to_save = self.game_state.copy()
        if 'status' in state_to_save and state_to_save['status'] is not None:
            state_to_save['status'] = state_to_save['status'].name
        with open(path, 'w') as f:
            json.dump(state_to_save, f, indent=4)
        logging.info(f"Game state saved: {state_to_save}")

    def load_game_state(self):
        path = self.get_persistent_storage_path()
        try:
            with open(path, 'r') as f:
                loaded_state = json.load(f)
            
            # Ensure all required keys are present
            default_state = {
                'p1_name': 'Player 1',
                'p2_name': 'Player 2',
                'p1_primary_score': 0,
                'p1_secondary_score': 0,
                'p2_primary_score': 0,
                'p2_secondary_score': 0,
                'p1_cp': 0,
                'p2_cp': 0,
                'attacker_name': None,
                'defender_name': None,
                'first_turn_player_name': None,
                'current_player_name': None,
                'current_round': 0,
                'current_player_id': 1,  # Default to Player 1
                'status': None,
            }
            
            # Update loaded state with any missing default values
            self.game_state = {**default_state, **loaded_state}
            
            # Convert status string back to GameStatus enum
            if self.game_state['status'] is not None:
                self.game_state['status'] = GameStatus[self.game_state['status']]
            
            logging.info(f"Game state loaded: {self.game_state}")
        except (FileNotFoundError, json.JSONDecodeError):
            self.initialize_game_state()

    def initialize_game_state(self):
        self.game_state = {
            'p1_name': 'Player 1',
            'p2_name': 'Player 2',
            'p1_primary_score': 0,
            'p1_secondary_score': 0,
            'p2_primary_score': 0,
            'p2_secondary_score': 0,
            'p1_cp': 0,
            'p2_cp': 0,
            'attacker_name': None,
            'defender_name': None,
            'first_turn_player_name': None,
            'current_player_name': None,
            'current_round': 0,
            'current_player_id': 1,  # Start with Player 1 by default
            'status': None,
        }
        self.save_game_state()
        logging.info("Game state initialized")

    def set_player_names(self, p1_name, p2_name):
        self.game_state['p1_name'] = p1_name if p1_name else "Player 1"
        self.game_state['p2_name'] = p2_name if p2_name else "Player 2"
        logging.info(f"Player names set: {self.game_state}")
        self.save_game_state()

    def set_objective_score(self, player, objective_type, value):
        """Sets the score for a given player's objective type."""
        score_key = f"p{player}_{objective_type}_score"
        logging.info(f"Setting {score_key} to {value}")
        self.game_state[score_key] = value
        self.save_game_state()
        logging.info(f"Score updated, new game state: {self.game_state}")

    def update_cp(self, player_id, amount):
        """Update command points for a player"""
        cp_key = f'p{player_id}_cp'
        current_cp = self.game_state.get(cp_key, 0)
        self.game_state[cp_key] = max(0, current_cp + amount)
        self.save_game_state()

    def end_turn(self):
        """Ends the current turn, updates the player and round."""
        p1 = self.game_state['p1_name']
        p2 = self.game_state['p2_name']
        current_player = self.game_state.get('current_player_name')
        
        # If this is the first turn of the game
        if current_player is None:
            # Set the first turn player and current player to the first turn player
            first_turn_player = self.game_state.get('first_turn_player_name')
            self.game_state['current_player_name'] = first_turn_player
            self.game_state['current_round'] = 1
        else:
            # If the player finishing their turn is not the one who started the round,
            # then a full round has passed.
            first_turn_player = self.game_state.get('first_turn_player_name')
            if current_player != first_turn_player:
                self.game_state['current_round'] += 1

            # Determine who is next
            if current_player == p1:
                self.game_state['current_player_name'] = p2
            else:  # current_player is p2
                self.game_state['current_player_name'] = p1
        
        self.save_game_state()

    def handle_concession(self, player_number):
        """Handles a player's concession."""
        # Get the conceding player's name
        conceding_player = self.game_state[f'p{player_number}_name']
        other_player = self.game_state[f'p{3-player_number}_name']
        
        # Set the final scores
        self.game_state['game_ended'] = True
        self.game_state['winner'] = other_player
        self.game_state['conceding_player'] = conceding_player
        
        # Save the game state
        self.save_game_state()
        
        # Switch to the game over screen
        self.root.manager.current = 'game_over'

# Initialize the game state
game_state = GameState()

# Example: Set player names
game_state.player1_name = "Player 1"
game_state.player2_name = "Player 2"

# Example: Set attacker and first turn player
game_state.attacker_id = 1
game_state.first_turn_player_id = 2

# Example: Start the game
game_state.start_game()

# Example: Update scores
game_state.update_score(1, primary=10, secondary=5)
game_state.update_score(2, primary=8, secondary=3)

# Example: Print current state
print("Current game state:", game_state)

if __name__ == '__main__':
    ScorerApp().run() 