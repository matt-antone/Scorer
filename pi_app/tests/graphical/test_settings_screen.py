"""
Tests for the Settings Screen.
"""
from .test_base import BaseScreenTest

class TestSettingsScreen(BaseScreenTest):
    """Tests for the Settings Screen."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('settings')
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'display_rotation_switch')
        self.assert_widget_exists(self.screen, 'screensaver_timeout_input')
        self.assert_widget_exists(self.screen, 'save_button')
        self.assert_widget_exists(self.screen, 'back_button')
        
        # Check initial widget states
        self.assert_widget_disabled(self.screen, 'save_button', False)
        self.assert_widget_disabled(self.screen, 'back_button', False)
    
    def test_display_rotation(self):
        """Test display rotation setting."""
        # Toggle display rotation
        self.screen.display_rotation_switch.active = True
        self.advance_frames(1)
        
        # Click save button
        self.screen.save_button.trigger_action()
        self.advance_frames(1)
        
        # Check that setting was saved
        assert self.app.settings['display_rotation'] is True
    
    def test_screensaver_timeout(self):
        """Test screensaver timeout setting."""
        # Set screensaver timeout
        self.screen.screensaver_timeout_input.text = '300'
        self.advance_frames(1)
        
        # Click save button
        self.screen.save_button.trigger_action()
        self.advance_frames(1)
        
        # Check that setting was saved
        assert self.app.settings['screensaver_timeout'] == 300
    
    def test_back_button(self):
        """Test back button functionality."""
        # Click back button
        self.screen.back_button.trigger_action()
        self.advance_frames(1)
        
        # Check that we moved to the previous screen
        assert self.app.root.current == 'resume_or_new' 