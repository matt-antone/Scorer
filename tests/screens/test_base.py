import unittest
from unittest.mock import MagicMock, patch
from pi_client.screens.base_screen import BaseScreen

class TestBaseScreen(unittest.TestCase):
    """Base class for screen tests that mocks Kivy dependencies."""

    def setUp(self):
        """Set up test environment with mocked Kivy dependencies."""
        # Mock Kivy's Builder
        self.builder_patcher = patch('kivy.lang.builder.Builder')
        self.mock_builder = self.builder_patcher.start()
        
        # Mock Kivy's Factory
        self.factory_patcher = patch('kivy.factory.Factory')
        self.mock_factory = self.factory_patcher.start()
        
        # Mock Kivy's Widget
        self.widget_patcher = patch('kivy.uix.widget.Widget')
        self.mock_widget = self.widget_patcher.start()
        
        # Create mock app
        self.app = MagicMock()
        self.app.game_state = {}
        
        # Create screen instance
        self.screen = type('TestScreen', (BaseScreen,), {})()
        self.screen.app = self.app
        self.screen._current_error = None
        self.screen.has_error = False
        self.screen.is_loading = False
        self.screen.is_syncing = False

    def tearDown(self):
        """Clean up test environment."""
        self.builder_patcher.stop()
        self.factory_patcher.stop()
        self.widget_patcher.stop()

if __name__ == '__main__':
    unittest.main() 