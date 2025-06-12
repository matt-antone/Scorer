import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.app import App
from kivy.clock import Clock
from pi_app.screens.name_entry_screen import NameEntryScreen
from pi_app.screens.base_screen import ValidationError, StateError

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

class NameEntryScreenTest(GraphicUnitTest):
    """Test cases for NameEntryScreen."""

    def setUp(self):
        """Set up test environment."""
        self.app = TestApp()
        self.screen = NameEntryScreen()
        self.app.game_state = {
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

    def tearDown(self):
        """Clean up test environment."""
        self.screen.stop_sync()
        if self.screen._error_timeout:
            self.screen._error_timeout.cancel()

    def test_initial_state(self):
        """Test initial state of NameEntryScreen."""
        self.assertFalse(self.screen.is_loading)
        self.assertFalse(self.screen.is_syncing)
        self.assertFalse(self.screen.has_error)
        self.assertEqual(len(self.screen.players), 0)
        self.assertEqual(len(self.screen.player_names), 0)
        self.assertIsNone(self.screen.qr_code)
        self.assertFalse(self.screen.qr_code_valid)
        self.assertIsNone(self.screen.qr_code_error)

    def test_qr_code_display(self):
        """Test QR code display functionality."""
        # Test QR code generation
        self.screen.generate_qr_code()
        self.assertIsNotNone(self.screen.qr_code)
        self.assertTrue(self.screen.qr_code_valid)
        
        # Test QR code validation
        self.screen.validate_qr_code()
        self.assertTrue(self.screen.qr_code_valid)
        
        # Test QR code error handling
        self.screen.handle_qr_code_error()
        self.assertTrue(self.screen.has_error)
        self.assertIsNotNone(self.screen.qr_code_error)
        
        # Test QR code refresh
        old_qr = self.screen.qr_code
        self.screen.refresh_qr_code()
        self.assertNotEqual(self.screen.qr_code, old_qr)

    def test_name_synchronization(self):
        """Test name synchronization functionality."""
        # Test name addition
        self.screen.add_player_name("Player1")
        self.assertEqual(len(self.screen.player_names), 1)
        self.assertEqual(self.screen.player_names[0], "Player1")
        
        # Test name removal
        self.screen.remove_player_name("Player1")
        self.assertEqual(len(self.screen.player_names), 0)
        
        # Test name update
        self.screen.add_player_name("Player1")
        self.screen.update_player_name("Player1", "Player1Updated")
        self.assertEqual(self.screen.player_names[0], "Player1Updated")
        
        # Test name list validation
        self.assertTrue(self.screen.validate_name_list(self.screen.player_names))

    def test_duplicate_name_handling(self):
        """Test duplicate name handling functionality."""
        # Test duplicate detection
        self.screen.add_player_name("Player1")
        with self.assertRaises(ValidationError):
            self.screen.add_player_name("Player1")
        
        # Test case-insensitive duplicate detection
        with self.assertRaises(ValidationError):
            self.screen.add_player_name("player1")
        
        # Test duplicate resolution
        self.screen.add_player_name("Player1")
        self.screen.resolve_duplicate_name("Player1")
        self.assertEqual(self.screen.player_names[0], "Player1_1")

    def test_name_validation(self):
        """Test name validation functionality."""
        # Test valid name
        self.assertTrue(self.screen.validate_name("Player1"))
        
        # Test too short name
        with self.assertRaises(ValidationError):
            self.screen.validate_name("P")
        
        # Test too long name
        with self.assertRaises(ValidationError):
            self.screen.validate_name("P" * 21)
        
        # Test invalid characters
        with self.assertRaises(ValidationError):
            self.screen.validate_name("Player@1")

    def test_screen_transitions(self):
        """Test screen transitions."""
        # Test to deployment setup screen
        self.screen.add_player_name("Player1")
        self.screen.add_player_name("Player2")
        self.screen.proceed_to_deployment()
        # Verify screen transition (would need to mock screen manager)
        
        # Test back to resume game screen
        self.screen.back_to_resume()
        # Verify screen transition (would need to mock screen manager)

    def test_error_handling(self):
        """Test error handling functionality."""
        # Test name validation error
        self.screen.handle_name_validation_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('name', self.screen._current_error.lower())
        
        # Test QR code error
        self.screen.handle_qr_code_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('qr code', self.screen._current_error.lower())
        
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
            'type': 'player_names',
            'names': ['Player1', 'Player2']
        }
        self.screen.handle_client_update(update)
        self.assertEqual(len(self.screen.player_names), 2)
        
        # Test invalid update
        with self.assertRaises(ValidationError):
            self.screen.handle_client_update({
                'type': 'invalid_type'
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

if __name__ == '__main__':
    unittest.main() 