"""
Tests for the Resume Screen.
"""
from pi_app.tests.graphical.test_base import BaseScreenTest

class TestResumeScreen(BaseScreenTest):
    """Tests for the Resume Screen."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('resume')
        self.screen.on_enter()
        self.advance_frames(1)
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'resume_button')
        self.assert_widget_exists(self.screen, 'new_game_button')
        
        # Check button states
        self.assert_widget_disabled(self.screen, 'resume_button', True)  # Initially disabled
        self.assert_widget_disabled(self.screen, 'new_game_button', False)  # Always enabled
    
    def test_resume_button(self):
        """Test the resume button functionality."""
        # Set up game state to enable resume
        self.app.game_state.update({
            'p1_name': 'Player 1',
            'p2_name': 'Player 2',
            'p1_primary_score': 5,
            'p2_primary_score': 3
        })
        self.screen.on_enter()  # Refresh screen state
        self.advance_frames(1)
        
        # Check that resume button is enabled
        self.assert_widget_disabled(self.screen, 'resume_button', False)
        
        # Click resume button
        self.screen.resume_button.trigger_action()
        self.advance_frames(1)
        
        # Check that we moved to the scoreboard screen
        assert self.app.root.current == 'scoreboard'
    
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