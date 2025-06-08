import kivy
import json
import threading
from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from kivy.app import App
from kivy.utils import get_color_from_hex
from widgets.root_widget import ScorerRootWidget
from screens.splash_screen import SplashScreen
from screens.name_entry_screen import NameEntryScreen
from screens.deployment_setup_screen import DeploymentSetupScreen
from screens.initiative_screen import InitiativeScreen
from screens.scoreboard_screen import ScoreboardScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from widgets.header_widget import HeaderWidget
from widgets.number_pad_popup import NumberPadPopup

kivy.require('2.3.0')

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
        return ScorerRootWidget()

    def on_stop(self):
        self.save_game_state()

    def get_persistent_storage_path(self):
        return self.user_data_dir + '/game_state.json'

    def save_game_state(self):
        path = self.get_persistent_storage_path()
        with open(path, 'w') as f:
            json.dump(self.game_state, f, indent=4)

    def load_game_state(self):
        path = self.get_persistent_storage_path()
        try:
            with open(path, 'r') as f:
                self.game_state = json.load(f)
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
        }
        self.save_game_state()

    def set_player_names(self, p1_name, p2_name):
        self.game_state['p1_name'] = p1_name if p1_name else "Player 1"
        self.game_state['p2_name'] = p2_name if p2_name else "Player 2"
        print(f"Game state updated: {self.game_state}")
        self.save_game_state()

    def set_objective_score(self, player, objective_type, value):
        """Sets the score for a given player's objective type."""
        score_key = f"p{player}_{objective_type}_score"
        self.game_state[score_key] = value
        self.save_game_state()

    def update_cp(self, player, amount):
        """Updates the command points for a given player."""
        cp_key = f"p{player}_cp"
        self.game_state[cp_key] = max(0, self.game_state[cp_key] + amount)
        self.save_game_state()

    def end_turn(self):
        """Ends the current turn, updates the player and round."""
        p1 = self.game_state['p1_name']
        p2 = self.game_state['p2_name']
        current_player = self.game_state['current_player_name']
        first_turn_player = self.game_state.get('first_turn_player_name')

        # If the player finishing their turn is not the one who started the round,
        # then a full round has passed.
        if current_player != first_turn_player:
            self.game_state['current_round'] += 1

        # Determine who is next
        if current_player == p1:
            self.game_state['current_player_name'] = p2
        else: # current_player is p2
            self.game_state['current_player_name'] = p1
        
        self.save_game_state()

if __name__ == '__main__':
    ScorerApp().run() 