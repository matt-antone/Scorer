"""
Tests for the Resume or New Game Screen.
"""
from .test_base import BaseScreenTest

class TestResumeGameScreen(BaseScreenTest):
    """Tests for the Resume or New Game Screen."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('resume_or_new')
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'resume_button')
        self.assert_widget_exists(self.screen, 'new_game_button')
        
        # Check initial button states
        self.assert_widget_disabled(self.screen, 'resume_button', False)
        self.assert_widget_disabled(self.screen, 'new_game_button', False)
    
    def test_resume_button(self):
        """Test the resume button functionality."""
        # Set up a saved game state
        self.app.game_state.update({
            'p1_name': 'Player 1',
            'p2_name': 'Player 2',
            'p1_primary_score': 10,
            'p2_primary_score': 8
        })
        
        # Click resume button
        self.screen.resume_button.trigger_action()
        self.advance_frames(1)
        
        # Check that we moved to the scoreboard screen
        assert self.app.root.current == 'scoreboard'
        
        # Check that game state was preserved
        assert self.app.game_state['p1_name'] == 'Player 1'
        assert self.app.game_state['p2_name'] == 'Player 2'
        assert self.app.game_state['p1_primary_score'] == 10
        assert self.app.game_state['p2_primary_score'] == 8
    
    def test_new_game_button(self):
        """Test the new game button functionality."""
        # Set up a saved game state
        self.app.game_state.update({
            'p1_name': 'Player 1',
            'p2_name': 'Player 2',
            'p1_primary_score': 10,
            'p2_primary_score': 8
        })
        
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