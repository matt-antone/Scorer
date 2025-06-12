"""
Tests for the Name Entry Screen.
"""
from .test_base import BaseScreenTest

class TestNameEntryScreen(BaseScreenTest):
    """Tests for the Name Entry Screen."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('name_entry')
        self.screen.on_enter()
        self.advance_frames(1)
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'p1_name_input')
        self.assert_widget_exists(self.screen, 'p2_name_input')
        self.assert_widget_exists(self.screen, 'continue_button')
        
        # Check initial input states
        self.assert_widget_text(self.screen, 'p1_name_input', '')
        self.assert_widget_text(self.screen, 'p2_name_input', '')
        
        # Check button state
        self.assert_widget_disabled(self.screen, 'continue_button', True)
    
    def test_input_validation(self):
        """Test input validation."""
        # Test empty inputs
        self.screen.p1_name_input.text = ''
        self.screen.p2_name_input.text = ''
        self.screen.validate_inputs()
        self.advance_frames(1)
        self.assert_widget_disabled(self.screen, 'continue_button', True)
        
        # Test partial inputs
        self.screen.p1_name_input.text = 'Player 1'
        self.screen.p2_name_input.text = ''
        self.screen.validate_inputs()
        self.advance_frames(1)
        self.assert_widget_disabled(self.screen, 'continue_button', True)
        
        # Test valid inputs
        self.screen.p1_name_input.text = 'Player 1'
        self.screen.p2_name_input.text = 'Player 2'
        self.screen.validate_inputs()
        self.advance_frames(1)
        self.assert_widget_disabled(self.screen, 'continue_button', False)
    
    def test_continue_button(self):
        """Test the continue button functionality."""
        # Set valid inputs
        self.screen.p1_name_input.text = 'Player 1'
        self.screen.p2_name_input.text = 'Player 2'
        self.screen.validate_inputs()
        self.advance_frames(1)
        
        # Click continue button
        self.screen.continue_button.trigger_action()
        self.advance_frames(1)
        
        # Check that we moved to the deployment setup screen
        assert self.app.root.current == 'deployment_setup'
        
        # Check that names were saved
        assert self.app.game_state['p1_name'] == 'Player 1'
        assert self.app.game_state['p2_name'] == 'Player 2' 