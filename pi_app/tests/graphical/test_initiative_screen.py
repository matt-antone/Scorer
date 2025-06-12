"""
Tests for the Initiative Screen.
"""
from .test_base import BaseScreenTest

class TestInitiativeScreen(BaseScreenTest):
    """Tests for the Initiative Screen."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('initiative')
        self.screen.on_enter()
        self.advance_frames(1)
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'p1_initiative_label')
        self.assert_widget_exists(self.screen, 'p2_initiative_label')
        self.assert_widget_exists(self.screen, 'continue_button')
        
        # Check initial label states
        self.assert_widget_text(self.screen, 'p1_initiative_label', 'Player 1: Roll for Initiative')
        self.assert_widget_text(self.screen, 'p2_initiative_label', 'Player 2: Roll for Initiative')
        
        # Check button state
        self.assert_widget_disabled(self.screen, 'continue_button', True)
    
    def test_initiative_roll(self):
        """Test initiative roll functionality."""
        # Roll initiative for both players
        self.screen.p1_initiative = 5
        self.screen.p2_initiative = 3
        self.screen.validate_initiative()
        self.advance_frames(1)
        
        # Check button state
        self.assert_widget_disabled(self.screen, 'continue_button', False)
        
        # Click continue button
        self.screen.continue_button.trigger_action()
        self.advance_frames(1)
        
        # Check that we moved to the scoreboard screen
        assert self.app.root.current == 'scoreboard'
        
        # Check that initiative was saved
        assert self.app.game_state['p1_initiative'] == 5
        assert self.app.game_state['p2_initiative'] == 3
        assert self.app.game_state['first_player'] == 1 