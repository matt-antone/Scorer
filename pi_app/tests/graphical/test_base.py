"""
Base test class for graphical tests.
Provides common setup and teardown functionality.
"""
import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.clock import Clock

from ...main import ScorerApp

class BaseScreenTest(GraphicUnitTest):
    """Base class for all screen tests."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.app = ScorerApp()
        self.app.run()
        self.advance_frames(1)
    
    def tearDown(self):
        """Clean up after the test."""
        self.app.stop()
        super().tearDown()
    
    def get_screen(self, name):
        """Get a screen by name."""
        return self.app.root.get_screen(name)
    
    def advance_frames(self, count):
        """Advance the clock by the given number of frames."""
        for _ in range(count):
            Clock.tick()
    
    def assert_widget_exists(self, screen, widget_id):
        """Assert that a widget exists in the screen."""
        widget = screen.ids.get(widget_id)
        assert widget is not None, f"Widget {widget_id} not found in screen"
    
    def assert_widget_text(self, screen, widget_id, expected_text):
        """Assert that a widget's text matches the expected text."""
        widget = screen.ids.get(widget_id)
        assert widget is not None, f"Widget {widget_id} not found in screen"
        assert widget.text == expected_text, f"Widget {widget_id} text mismatch: expected {expected_text}, got {widget.text}"
    
    def assert_widget_disabled(self, screen, widget_id, expected_disabled):
        """Assert that a widget's disabled state matches the expected state."""
        widget = screen.ids.get(widget_id)
        assert widget is not None, f"Widget {widget_id} not found in screen"
        assert widget.disabled == expected_disabled, f"Widget {widget_id} disabled state mismatch: expected {expected_disabled}, got {widget.disabled}" 