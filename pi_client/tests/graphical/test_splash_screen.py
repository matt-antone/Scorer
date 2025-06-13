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
        self.screen.on_enter()
        self.advance_frames(1)
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'title_label')
        self.assert_widget_exists(self.screen, 'version_label')
        self.assert_widget_exists(self.screen, 'loading_label')
        
        # Check initial label states
        self.validate_string_field('title_label', 'AICamera Scorer')
        self.validate_string_field('version_label', 'v1.0.0')
        self.validate_string_field('loading_label', 'Loading...')
    
    def test_auto_transition(self):
        """Test automatic transition to resume screen."""
        # Wait for transition
        self.advance_frames(120)  # 2 seconds at 60 FPS
        
        # Check that we moved to the resume screen
        assert self.app.root.current == 'resume'

    def test_screen_transition(self):
        """Alias for test_auto_transition to match test suite expectations."""
        self.test_auto_transition() 