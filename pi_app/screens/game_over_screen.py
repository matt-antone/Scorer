from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import StringProperty
from kivy.lang import Builder
import os

class GameOverScreen(Screen):
    winner_text = StringProperty('')
    final_scores_text = StringProperty('')

    def __init__(self, **kwargs):
        kv_path = os.path.join(os.path.dirname(__file__), 'game_over_screen.kv')
        Builder.load_file(kv_path)
        super().__init__(**kwargs)

    def on_enter(self):
        """Called when the screen is shown. Updates the winner and scores."""
        app = App.get_running_app()
        state = app.game_state
        
        # Set winner text
        winner = state.get('winner', 'No winner')
        self.winner_text = f"Winner: {winner}"
        
        # Set final scores
        p1_name = state.get('p1_name', 'Player 1')
        p2_name = state.get('p2_name', 'Player 2')
        p1_total = state.get('p1_primary_score', 0) + state.get('p1_secondary_score', 0)
        p2_total = state.get('p2_primary_score', 0) + state.get('p2_secondary_score', 0)
        
        self.final_scores_text = f"{p1_name}: {p1_total}\n{p2_name}: {p2_total}"

    def start_new_game(self):
        """Starts a new game by reinitializing the game state."""
        app = App.get_running_app()
        app.initialize_game_state()
        self.manager.current = 'name_entry' 