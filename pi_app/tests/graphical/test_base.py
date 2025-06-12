"""
Base test class for graphical tests.
Provides common setup and teardown functionality.
"""
from kivy.tests.common import GraphicUnitTest
from kivy.base import EventLoop
from pi_app.main import ScorerApp

class BaseScreenTest(GraphicUnitTest):
    """Base class for all screen tests."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.app = ScorerApp()
        self.app.root = self.app.build()
        # Allow KV rules to be applied
        self.advance_frames(1)
        self.render(self.app.root)
    
    def tearDown(self):
        """Clean up after the test."""
        self.app.stop()
        super().tearDown()
    
    def get_screen(self, screen_name):
        """Get a screen by name and set it as current."""
        screen = self.app.root.get_screen(screen_name)
        self.app.root.current = screen_name
        self.advance_frames(1)
        return screen
    
    def render(self, widget):
        """Render a widget and advance frames."""
        self.render_widget(widget)
        self.advance_frames(1)
    
    def assert_widget_exists(self, widget, widget_id):
        """Assert that a widget with the given ID exists."""
        assert hasattr(widget, widget_id), f"Widget {widget_id} not found"
    
    def assert_widget_text(self, widget, widget_id, expected_text):
        """Assert that a widget's text matches the expected value."""
        self.assert_widget_exists(widget, widget_id)
        actual_text = getattr(widget, widget_id).text
        assert actual_text == expected_text, \
            f"Expected text '{expected_text}', got '{actual_text}'"
    
    def assert_widget_disabled(self, widget, widget_id, expected_disabled=True):
        """Assert that a widget's disabled state matches the expected value."""
        self.assert_widget_exists(widget, widget_id)
        actual_disabled = getattr(widget, widget_id).disabled
        assert actual_disabled == expected_disabled, \
            f"Expected disabled={expected_disabled}, got {actual_disabled}" 