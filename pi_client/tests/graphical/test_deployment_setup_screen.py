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
        self.screen.on_enter()
        self.advance_frames(1)
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'p1_deployment_label')
        self.assert_widget_exists(self.screen, 'p2_deployment_label')
        self.assert_widget_exists(self.screen, 'continue_button')
        
        # Check initial label states
        self.assert_widget_text(self.screen, 'p1_deployment_label', 'Player 1: Choose Deployment')
        self.assert_widget_text(self.screen, 'p2_deployment_label', 'Player 2: Choose Deployment')
        
        # Check button state
        self.assert_widget_disabled(self.screen, 'continue_button', True)
    
    def test_deployment_selection(self):
        """Test deployment selection functionality."""
        # Select deployments
        self.screen.p1_deployment = 'Dawn of War'
        self.screen.p2_deployment = 'Hammer and Anvil'
        self.screen.validate_deployments()
        self.advance_frames(1)
        
        # Check button state
        self.assert_widget_disabled(self.screen, 'continue_button', False)
        
        # Click continue button
        self.screen.continue_button.trigger_action()
        self.advance_frames(1)
        
        # Check that we moved to the initiative screen
        assert self.app.root.current == 'initiative'
        
        # Check that deployments were saved
        assert self.app.game_state['p1_deployment'] == 'Dawn of War'
        assert self.app.game_state['p2_deployment'] == 'Hammer and Anvil' 