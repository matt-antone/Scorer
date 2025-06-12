import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.app import App
from kivy.clock import Clock
from pi_app.screens.base_screen import BaseScreen, ScreenError, ValidationError, StateError, SyncError

class TestScreen(BaseScreen):
    """Test implementation of BaseScreen for testing."""
    def update_view_from_state(self):
        pass

    def recover_from_error(self):
        pass

    def broadcast_state(self):
        pass

    def handle_client_update(self, update):
        pass

class TestApp(App):
    """Test application with game state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = {}

class BaseScreenTest(GraphicUnitTest):
    """Test cases for BaseScreen."""

    def setUp(self):
        """Set up test environment."""
        self.app = TestApp()
        self.screen = TestScreen()
        self.app.game_state = {'test_key': 'test_value'}

    def tearDown(self):
        """Clean up test environment."""
        self.screen.stop_sync()
        if self.screen._error_timeout:
            self.screen._error_timeout.cancel()

    def test_initial_state(self):
        """Test initial state of BaseScreen."""
        self.assertFalse(self.screen.is_loading)
        self.assertFalse(self.screen.is_syncing)
        self.assertFalse(self.screen.has_error)
        self.assertIsNone(self.screen._current_error)
        self.assertIsNone(self.screen._current_status)
        self.assertIsNone(self.screen._sync_event)
        self.assertIsNone(self.screen._error_timeout)

    def test_show_error(self):
        """Test error display functionality."""
        error_message = "Test error"
        self.screen.show_error(error_message)
        
        self.assertTrue(self.screen.has_error)
        self.assertEqual(self.screen._current_error, error_message)
        self.assertIsNotNone(self.screen._error_timeout)

    def test_clear_error(self):
        """Test error clearing functionality."""
        self.screen.show_error("Test error")
        self.screen.clear_error()
        
        self.assertFalse(self.screen.has_error)
        self.assertIsNone(self.screen._current_error)
        self.assertIsNone(self.screen._error_timeout)

    def test_show_status(self):
        """Test status display functionality."""
        status_message = "Test status"
        self.screen.show_status(status_message)
        
        self.assertEqual(self.screen._current_status, status_message)

    def test_clear_status(self):
        """Test status clearing functionality."""
        self.screen.show_status("Test status")
        self.screen.clear_status()
        
        self.assertIsNone(self.screen._current_status)

    def test_show_loading(self):
        """Test loading state functionality."""
        self.screen.show_loading(True)
        self.assertTrue(self.screen.is_loading)
        
        self.screen.show_loading(False)
        self.assertFalse(self.screen.is_loading)

    def test_validate_state(self):
        """Test state validation functionality."""
        # Test valid state
        self.assertTrue(self.screen.validate_state(['test_key']))
        
        # Test invalid state
        with self.assertRaises(StateError):
            self.screen.validate_state(['missing_key'])

    def test_update_state(self):
        """Test state update functionality."""
        updates = {'new_key': 'new_value'}
        self.screen.update_state(updates)
        
        self.assertIn('new_key', self.app.game_state)
        self.assertEqual(self.app.game_state['new_key'], 'new_value')

    def test_validate_input(self):
        """Test input validation functionality."""
        input_data = {'test_field': 'test_value'}
        rules = {
            'test_field': lambda x: isinstance(x, str)
        }
        
        # Test valid input
        self.assertTrue(self.screen.validate_input(input_data, rules))
        
        # Test invalid input
        with self.assertRaises(ValidationError):
            self.screen.validate_input({'test_field': 123}, rules)
        
        # Test missing field
        with self.assertRaises(ValidationError):
            self.screen.validate_input({}, rules)

    def test_sanitize_input(self):
        """Test input sanitization functionality."""
        input_data = {
            'string_field': '  test value  ',
            'number_field': 123,
            'list_field': ['  item  ']
        }
        
        sanitized = self.screen.sanitize_input(input_data)
        
        self.assertEqual(sanitized['string_field'], 'test value')
        self.assertEqual(sanitized['number_field'], 123)
        self.assertEqual(sanitized['list_field'], ['  item  '])

    def test_lifecycle_methods(self):
        """Test screen lifecycle methods."""
        # Test on_pre_enter
        self.screen.on_pre_enter()
        self.assertFalse(self.screen.is_loading)
        
        # Test on_enter
        self.screen.on_enter()
        self.assertFalse(self.screen.is_loading)
        
        # Test on_leave
        self.screen.on_leave()
        self.assertFalse(self.screen.is_syncing)
        self.assertFalse(self.screen.has_error)
        self.assertIsNone(self.screen._error_timeout)

    def test_error_handling(self):
        """Test error handling functionality."""
        # Test ValidationError
        with self.assertRaises(ValidationError):
            self.screen.handle_error(ValidationError("Test validation error"))
        
        # Test StateError
        with self.assertRaises(StateError):
            self.screen.handle_error(StateError("Test state error"))
        
        # Test SyncError
        with self.assertRaises(SyncError):
            self.screen.handle_error(SyncError("Test sync error"))
        
        # Test generic error
        with self.assertRaises(Exception):
            self.screen.handle_error(Exception("Test generic error"))

    def test_sync_methods(self):
        """Test synchronization methods."""
        # Test start_sync
        self.screen.start_sync()
        self.assertTrue(self.screen.is_syncing)
        
        # Test stop_sync
        self.screen.stop_sync()
        self.assertFalse(self.screen.is_syncing)
        self.assertIsNone(self.screen._sync_event)

# ... existing code ... 