"""
Tests for the Splash Screen.
"""
from .test_base import BaseScreenTest

class TestSplashScreen(BaseScreenTest):
    """Tests for the Splash Screen."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('splash')
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'title_label')
        self.assert_widget_exists(self.screen, 'version_label')
        
        # Check initial label states
        self.assert_widget_text(self.screen, 'title_label', 'Scorer')
        self.assert_widget_text(self.screen, 'version_label', 'v1.0.0')
    
    def test_screen_transition(self):
        """Test automatic transition to resume or new game screen."""
        # Wait for transition
        self.advance_frames(60)  # 1 second at 60 FPS
        
        # Check that we moved to the resume or new game screen
        assert self.app.root.current == 'resume_or_new' 