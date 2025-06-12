"""
Tests for the Scoreboard Screen.
"""
from .test_base import BaseScreenTest

class TestScoreboardScreen(BaseScreenTest):
    """Tests for the Scoreboard Screen."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('scoreboard')
        # Set up initial game state
        self.app.game_state.update({
            'p1_name': 'Player 1',
            'p2_name': 'Player 2',
            'p1_primary_score': 0,
            'p2_primary_score': 0,
            'p1_secondary_score': 0,
            'p2_secondary_score': 0,
            'p1_cp': 0,
            'p2_cp': 0
        })
        self.screen.on_enter()
        self.advance_frames(1)
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'p1_name_label')
        self.assert_widget_exists(self.screen, 'p2_name_label')
        self.assert_widget_exists(self.screen, 'p1_total_score_label')
        self.assert_widget_exists(self.screen, 'p2_total_score_label')
        self.assert_widget_exists(self.screen, 'p1_cp_label')
        self.assert_widget_exists(self.screen, 'p2_cp_label')
        
        # Check initial label states
        self.assert_widget_text(self.screen, 'p1_name_label', 'Player 1')
        self.assert_widget_text(self.screen, 'p2_name_label', 'Player 2')
        self.assert_widget_text(self.screen, 'p1_total_score_label', '0')
        self.assert_widget_text(self.screen, 'p2_total_score_label', '0')
        self.assert_widget_text(self.screen, 'p1_cp_label', '0')
        self.assert_widget_text(self.screen, 'p2_cp_label', '0')
    
    def test_update_scores(self):
        """Test updating scores for both players."""
        # Update game state
        self.app.game_state.update({
            'p1_primary_score': 10,
            'p1_secondary_score': 5,
            'p2_primary_score': 8,
            'p2_secondary_score': 2,
            'p1_cp': 3,
            'p2_cp': 1
        })
        
        # Trigger view update
        self.screen.update_view_from_state()
        self.advance_frames(1)
        
        # Check updated scores
        self.assert_widget_text(self.screen, 'p1_total_score_label', '15')
        self.assert_widget_text(self.screen, 'p2_total_score_label', '10')
        self.assert_widget_text(self.screen, 'p1_cp_label', '3')
        self.assert_widget_text(self.screen, 'p2_cp_label', '1')
    
    def test_open_score_popup(self):
        """Test opening the score popup."""
        # Open popup for player 1 primary score
        self.screen.open_score_popup(1, 'primary')
        self.advance_frames(1)
        
        # Check that popup is open
        assert len(self.app.root.children) > 1
        popup = self.app.root.children[0]
        assert popup.title == 'Player 1 Primary Score'
        
        # Check popup widgets
        self.assert_widget_exists(popup, 'number_pad')
        self.assert_widget_exists(popup, 'confirm_button')
        self.assert_widget_exists(popup, 'cancel_button')
    
    def test_concede_game(self):
        """Test conceding the game."""
        # Open concede popup
        self.screen.concede_game()
        self.advance_frames(1)
        
        # Check that concede popup is open
        assert len(self.app.root.children) > 1
        popup = self.app.root.children[0]
        assert popup.title == 'Concede Game'
        
        # Check popup widgets
        self.assert_widget_exists(popup, 'confirm_button')
        self.assert_widget_exists(popup, 'cancel_button') 