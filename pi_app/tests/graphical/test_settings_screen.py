"""
Tests for the Settings Screen.
"""
from pi_app.tests.graphical.test_base import BaseScreenTest

class TestSettingsScreen(BaseScreenTest):
    """Tests for the Settings Screen."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('settings')
        self.screen.on_enter()
        self.advance_frames(1)
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'primary_score_label')
        self.assert_widget_exists(self.screen, 'primary_score_input')
        self.assert_widget_exists(self.screen, 'secondary_score_label')
        self.assert_widget_exists(self.screen, 'secondary_score_input')
        self.assert_widget_exists(self.screen, 'cp_label')
        self.assert_widget_exists(self.screen, 'cp_input')
        self.assert_widget_exists(self.screen, 'save_button')
        self.assert_widget_exists(self.screen, 'cancel_button')
        
        # Check initial input states
        self.assert_widget_text(self.screen, 'primary_score_input', '10')
        self.assert_widget_text(self.screen, 'secondary_score_input', '5')
        self.assert_widget_text(self.screen, 'cp_input', '3')
        
        # Check button states
        self.assert_widget_disabled(self.screen, 'save_button', False)
        self.assert_widget_disabled(self.screen, 'cancel_button', False)
    
    def test_input_validation(self):
        """Test input validation."""
        # Test invalid primary score
        self.screen.primary_score_input.text = '0'
        self.screen.validate_inputs()
        self.advance_frames(1)
        self.assert_widget_disabled(self.screen, 'save_button', True)
        
        # Test invalid secondary score
        self.screen.primary_score_input.text = '10'
        self.screen.secondary_score_input.text = '0'
        self.screen.validate_inputs()
        self.advance_frames(1)
        self.assert_widget_disabled(self.screen, 'save_button', True)
        
        # Test invalid CP
        self.screen.secondary_score_input.text = '5'
        self.screen.cp_input.text = '0'
        self.screen.validate_inputs()
        self.advance_frames(1)
        self.assert_widget_disabled(self.screen, 'save_button', True)
        
        # Test valid inputs
        self.screen.cp_input.text = '3'
        self.screen.validate_inputs()
        self.advance_frames(1)
        self.assert_widget_disabled(self.screen, 'save_button', False)
    
    def test_save_button(self):
        """Test the save button functionality."""
        # Set valid inputs
        self.screen.primary_score_input.text = '15'
        self.screen.secondary_score_input.text = '7'
        self.screen.cp_input.text = '4'
        self.screen.validate_inputs()
        self.advance_frames(1)
        
        # Click save button
        self.screen.save_button.trigger_action()
        self.advance_frames(1)
        
        # Check that we moved back to the previous screen
        assert self.app.root.current == 'scoreboard'
        
        # Check that settings were saved
        assert self.app.game_state['primary_score'] == 15
        assert self.app.game_state['secondary_score'] == 7
        assert self.app.game_state['cp'] == 4
    
    def test_cancel_button(self):
        """Test the cancel button functionality."""
        # Set inputs
        self.screen.primary_score_input.text = '15'
        self.screen.secondary_score_input.text = '7'
        self.screen.cp_input.text = '4'
        self.advance_frames(1)
        
        # Click cancel button
        self.screen.cancel_button.trigger_action()
        self.advance_frames(1)
        
        # Check that we moved back to the previous screen
        assert self.app.root.current == 'scoreboard'
        
        # Check that settings were not changed
        assert self.app.game_state['primary_score'] == 10
        assert self.app.game_state['secondary_score'] == 5
        assert self.app.game_state['cp'] == 3 