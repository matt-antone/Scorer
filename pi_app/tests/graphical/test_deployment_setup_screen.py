"""
Tests for the Deployment Setup Screen.
"""
from .test_base import BaseScreenTest

class TestDeploymentSetupScreen(BaseScreenTest):
    """Tests for the Deployment Setup Screen."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('deployment_setup')
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'p1_deployment_button')
        self.assert_widget_exists(self.screen, 'p2_deployment_button')
        self.assert_widget_exists(self.screen, 'continue_button')
        
        # Check initial button states
        self.assert_widget_disabled(self.screen, 'p1_deployment_button', False)
        self.assert_widget_disabled(self.screen, 'p2_deployment_button', False)
        self.assert_widget_disabled(self.screen, 'continue_button', True)
    
    def test_deployment_selection(self):
        """Test deployment selection for both players."""
        # Select deployment for player 1
        self.screen.select_deployment(1)
        self.advance_frames(1)
        
        # Check button states
        self.assert_widget_disabled(self.screen, 'p1_deployment_button', True)
        self.assert_widget_disabled(self.screen, 'p2_deployment_button', False)
        self.assert_widget_disabled(self.screen, 'continue_button', True)
        
        # Select deployment for player 2
        self.screen.select_deployment(2)
        self.advance_frames(1)
        
        # Check button states
        self.assert_widget_disabled(self.screen, 'p1_deployment_button', True)
        self.assert_widget_disabled(self.screen, 'p2_deployment_button', True)
        self.assert_widget_disabled(self.screen, 'continue_button', False)
    
    def test_continue_button(self):
        """Test the continue button functionality."""
        # Select deployments for both players
        self.screen.select_deployment(1)
        self.advance_frames(1)
        self.screen.select_deployment(2)
        self.advance_frames(1)
        
        # Click continue button
        self.screen.continue_button.trigger_action()
        self.advance_frames(1)
        
        # Check that we moved to the initiative screen
        assert self.app.root.current == 'initiative' 