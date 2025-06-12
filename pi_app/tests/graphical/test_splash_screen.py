"""
Tests for the Splash Screen.
"""
from pi_app.tests.graphical.test_base import BaseScreenTest

class TestSplashScreen(BaseScreenTest):
    """Tests for the Splash Screen."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('splash')
        self.screen.on_enter()
        self.advance_frames(1)
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'title_label')
        self.assert_widget_exists(self.screen, 'version_label')
        self.assert_widget_exists(self.screen, 'loading_label')
        
        # Check initial label states
        self.assert_widget_text(self.screen, 'title_label', 'AICamera Scorer')
        self.assert_widget_text(self.screen, 'version_label', 'v1.0.0')
        self.assert_widget_text(self.screen, 'loading_label', 'Loading...')
    
    def test_auto_transition(self):
        """Test automatic transition to resume screen."""
        # Wait for transition
        self.advance_frames(120)  # 2 seconds at 60 FPS
        
        # Check that we moved to the resume screen
        assert self.app.root.current == 'resume' 