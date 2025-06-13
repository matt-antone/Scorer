"""
Tests for the Game Over Screen.
"""
from .test_base import BaseScreenTest

class TestGameOverScreen(BaseScreenTest):
    """Tests for the Game Over Screen."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('game_over')
        # Set up game state
        self.app.game_state.update({
            'p1_name': 'Player 1',
            'p2_name': 'Player 2',
            'p1_primary_score': 10,
            'p2_primary_score': 8,
            'p1_secondary_score': 5,
            'p2_secondary_score': 3,
            'p1_cp': 3,
            'p2_cp': 1,
            'winner': 1
        })
        self.screen.on_enter()
        self.advance_frames(1)
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'winner_label')
        self.assert_widget_exists(self.screen, 'p1_final_score_label')
        self.assert_widget_exists(self.screen, 'p2_final_score_label')
        self.assert_widget_exists(self.screen, 'new_game_button')
        
        # Check initial label states
        self.assert_widget_text(self.screen, 'winner_label', 'Player 1 Wins!')
        self.assert_widget_text(self.screen, 'p1_final_score_label', '15')
        self.assert_widget_text(self.screen, 'p2_final_score_label', '11')
        
        # Check button state
        self.assert_widget_disabled(self.screen, 'new_game_button', False)
    
    def test_new_game_button(self):
        """Test the new game button functionality."""
        # Click new game button
        self.screen.new_game_button.trigger_action()
        self.advance_frames(1)
        
        # Check that we moved to the name entry screen
        assert self.app.root.current == 'name_entry'
        
        # Check that game state was reset
        assert self.app.game_state['p1_name'] == ''
        assert self.app.game_state['p2_name'] == ''
        assert self.app.game_state['p1_primary_score'] == 0
        assert self.app.game_state['p2_primary_score'] == 0
        assert self.app.game_state['p1_secondary_score'] == 0
        assert self.app.game_state['p2_secondary_score'] == 0
        assert self.app.game_state['p1_cp'] == 0
        assert self.app.game_state['p2_cp'] == 0
        assert self.app.game_state['winner'] == 0 