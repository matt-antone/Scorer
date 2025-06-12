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
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'p1_roll_button')
        self.assert_widget_exists(self.screen, 'p2_roll_button')
        self.assert_widget_exists(self.screen, 'p1_roll_label')
        self.assert_widget_exists(self.screen, 'p2_roll_label')
        self.assert_widget_exists(self.screen, 'continue_button')
        
        # Check initial button states
        self.assert_widget_disabled(self.screen, 'p1_roll_button', False)
        self.assert_widget_disabled(self.screen, 'p2_roll_button', False)
        self.assert_widget_disabled(self.screen, 'continue_button', True)
        
        # Check initial label states
        self.assert_widget_text(self.screen, 'p1_roll_label', '')
        self.assert_widget_text(self.screen, 'p2_roll_label', '')
    
    def test_roll_die_player1(self):
        """Test rolling the die for player 1."""
        # Roll die for player 1
        self.screen.roll_die(1)
        self.advance_frames(1)
        
        # Check button states
        self.assert_widget_disabled(self.screen, 'p1_roll_button', True)
        self.assert_widget_disabled(self.screen, 'p2_roll_button', False)
        self.assert_widget_disabled(self.screen, 'continue_button', True)
        
        # Check that roll label has a value
        assert self.screen.p1_roll_label.text != ''
    
    def test_roll_die_player2(self):
        """Test rolling the die for player 2."""
        # Roll die for player 1 first
        self.screen.roll_die(1)
        self.advance_frames(1)
        
        # Roll die for player 2
        self.screen.roll_die(2)
        self.advance_frames(1)
        
        # Check button states
        self.assert_widget_disabled(self.screen, 'p1_roll_button', True)
        self.assert_widget_disabled(self.screen, 'p2_roll_button', True)
        self.assert_widget_disabled(self.screen, 'continue_button', False)
        
        # Check that both roll labels have values
        assert self.screen.p1_roll_label.text != ''
        assert self.screen.p2_roll_label.text != ''
    
    def test_continue_button(self):
        """Test the continue button functionality."""
        # Roll dice for both players
        self.screen.roll_die(1)
        self.advance_frames(1)
        self.screen.roll_die(2)
        self.advance_frames(1)
        
        # Click continue button
        self.screen.continue_button.trigger_action()
        self.advance_frames(1)
        
        # Check that we moved to the scoreboard screen
        assert self.app.root.current == 'scoreboard' 