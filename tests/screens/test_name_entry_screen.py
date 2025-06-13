import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.app import App
from kivy.clock import Clock
from pi_client.screens.name_entry_screen import NameEntryScreen
from pi_client.screens.base_screen import ValidationError, StateError
from pi_client.tests.graphical.test_base import BaseScreenTest
from kivy.uix.screenmanager import Screen

class TestApp(App):
    """Test application with game state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = {
            'players': [],
            'player_names': [],
            'qr_code': None,
            'qr_code_valid': False,
            'qr_code_error': None,
            'name_validation': {
                'min_length': 2,
                'max_length': 20,
                'allowed_chars': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_ '
            }
        }

class TestNameEntryScreen(BaseScreenTest):
    """Test cases for NameEntryScreen."""

    app_class = TestApp

    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('name_entry')
        self.screen.on_enter()
        self.advance_frames(1)

    def test_initial_state(self):
        """Test initial state of NameEntryScreen."""
        self.assertFalse(self.screen.is_loading)
        self.assertFalse(self.screen.is_syncing)
        self.assertFalse(self.screen.has_error)
        self.assertEqual(self.screen.p1_name, '')
        self.assertEqual(self.screen.p2_name, '')
        self.assertFalse(self.screen.qr_code_valid)
        self.assertEqual(self.screen.qr_code_error, '')

    def test_qr_code_display(self):
        """Test QR code display functionality."""
        # Test QR code generation
        self.assertTrue(self.screen.generate_qr_code("Player1"))
        self.assertTrue(self.screen.qr_code_valid)
        
        # Test QR code error handling
        self.screen.handle_qr_code_error()
        self.assertTrue(self.screen.has_error)
        self.assertIsNotNone(self.screen.qr_code_error)

    def test_name_synchronization(self):
        """Test name synchronization functionality."""
        # Test name addition
        self.screen.p1_name = "Player1"
        self.screen.p2_name = "Player2"
        self.screen.update_ui()
        
        # Test name removal
        self.screen.remove_player_name('p1')
        self.assertEqual(self.screen.p1_name, '')
        
        # Test name validation
        self.assertTrue(self.screen.validate_name("Player1"))
        self.assertFalse(self.screen.validate_name("P"))

    def test_duplicate_name_handling(self):
        """Test duplicate name handling functionality."""
        # Test duplicate detection
        self.screen.p1_name = "Player1"
        self.screen.p2_name = "Player1"
        self.assertFalse(self.screen.validate_inputs())
        self.assertIn("different", self.screen.qr_code_error.lower())

    def test_name_validation(self):
        """Test name validation functionality."""
        # Test valid name
        self.assertTrue(self.screen.validate_name("Player1"))
        
        # Test too short name
        self.assertFalse(self.screen.validate_name("P"))
        
        # Test too long name
        self.assertFalse(self.screen.validate_name("P" * 21))
        
        # Test invalid characters
        self.assertFalse(self.screen.validate_name("Player@1"))

    def test_screen_transitions(self):
        """Test screen transitions."""
        # Test to deployment setup screen
        self.screen.p1_name = "Player1"
        self.screen.p2_name = "Player2"
        self.screen.proceed_to_deployment()
        self.assertEqual(self.app.game_state['p1_name'], "Player1")
        self.assertEqual(self.app.game_state['p2_name'], "Player2")

    def test_error_handling(self):
        """Test error handling functionality."""
        # Test name validation error
        self.screen.handle_name_validation_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('name', self.screen._current_error.lower())
        
        # Test QR code error
        self.screen.handle_qr_code_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('failed to generate', self.screen.qr_code_error.lower())
        
        # Test state error
        self.screen.handle_state_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('state', self.screen._current_error.lower())

    def test_client_synchronization(self):
        """Test client synchronization functionality."""
        # Test start sync
        self.screen.start_sync()
        self.assertTrue(self.screen.is_syncing)
        
        # Test stop sync
        self.screen.stop_sync()
        self.assertFalse(self.screen.is_syncing)
        
        # Test client update
        update = {
            'type': 'player_name',
            'player': 'p1',
            'name': 'Player1'
        }
        self.screen.handle_client_update(update)
        self.assertEqual(self.screen.p1_name, 'Player1')
        
        # Test invalid update
        with self.assertRaises(ValidationError):
            self.screen.handle_client_update({
                'type': 'invalid',
                'player': 'p1',
                'name': 'Player1'
            })

    def test_input_validation(self):
        """Test input validation."""
        # Test valid input
        self.assertTrue(self.screen.validate_input({
            'name': 'Player1'
        }, {
            'name': self.screen.validate_name
        }))
        
        # Test invalid input
        with self.assertRaises(ValidationError):
            self.screen.validate_input({
                'name': 'P'
            }, {
                'name': self.screen.validate_name
            })

    def test_state_validation(self):
        """Test state validation."""
        # Test valid state
        self.assertTrue(self.screen.validate_state([
            'players', 'player_names', 'qr_code', 'qr_code_valid',
            'qr_code_error', 'name_validation'
        ]))
        
        # Test invalid state
        with self.assertRaises(StateError):
            self.screen.validate_state(['missing_key'])

# ... existing code ... 