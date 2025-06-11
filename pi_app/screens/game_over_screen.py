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
        
        # Get scores based on state type
        if isinstance(state, dict):
            p1_total = state.get('p1_primary_score', 0) + state.get('p1_secondary_score', 0)
            p2_total = state.get('p2_primary_score', 0) + state.get('p2_secondary_score', 0)
            p1_name = state.get('p1_name', 'Player 1')
            p2_name = state.get('p2_name', 'Player 2')
        else:
            p1_total = state.player1_primary + state.player1_secondary
            p2_total = state.player2_primary + state.player2_secondary
            p1_name = state.player1_name
            p2_name = state.player2_name
        
        # Calculate winner
        if p1_total > p2_total:
            winner = p1_name
        elif p2_total > p1_total:
            winner = p2_name
        else:
            winner = "Draw"
            
        self.winner_text = f"Winner: {winner}"
        self.final_scores_text = f"{p1_name}: {p1_total}\n{p2_name}: {p2_total}"

    def start_new_game(self):
        """Starts a new game by reinitializing the game state."""
        app = App.get_running_app()
        app.initialize_game_state()
        self.manager.current = 'name_entry' 