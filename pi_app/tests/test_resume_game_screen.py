import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.app import App
from kivy.clock import Clock
from pi_app.screens.resume_or_new_screen import ResumeOrNewScreen
from pi_app.screens.base_screen import ValidationError, StateError

class TestApp(App):
    """Test application with game state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = {
            'has_saved_game': False,
            'saved_game_info': None,
            'save_file_path': None,
            'save_file_valid': False,
            'save_file_error': None
        }

class ResumeOrNewScreenTest(GraphicUnitTest):
    """Test cases for ResumeOrNewScreen."""

    def setUp(self):
        """Set up test environment."""
        self.app = TestApp()
        self.screen = ResumeOrNewScreen()
        self.app.game_state = {
            'has_saved_game': False,
            'saved_game_info': None,
            'save_file_path': None,
            'save_file_valid': False,
            'save_file_error': None
        }

    def tearDown(self):
        """Clean up test environment."""
        self.screen.stop_sync()
        if self.screen._error_timeout:
            self.screen._error_timeout.cancel()

    def test_initial_state(self):
        """Test initial state of ResumeOrNewScreen."""
        self.assertFalse(self.screen.is_loading)
        self.assertFalse(self.screen.is_syncing)
        self.assertFalse(self.screen.has_error)
        self.assertFalse(self.screen.has_saved_game)
        self.assertIsNone(self.screen.saved_game_info)
        self.assertIsNone(self.screen.save_file_path)
        self.assertFalse(self.screen.save_file_valid)
        self.assertIsNone(self.screen.save_file_error)

    def test_game_state_validation(self):
        """Test game state validation functionality."""
        # Test valid game state
        valid_state = {
            'players': ['Player1', 'Player2'],
            'current_round': 3,
            'scores': {'Player1': 10, 'Player2': 5},
            'command_points': {'Player1': 5, 'Player2': 3}
        }
        self.assertTrue(self.screen.validate_game_state(valid_state))
        
        # Test invalid game state
        with self.assertRaises(ValidationError):
            self.screen.validate_game_state({'invalid': 'state'})
        
        # Test missing required fields
        with self.assertRaises(ValidationError):
            self.screen.validate_game_state({
                'players': ['Player1', 'Player2']
            })

    def test_save_file_management(self):
        """Test save file management functionality."""
        # Test initial state
        self.assertIsNone(self.screen.save_file_path)
        self.assertFalse(self.screen.save_file_valid)
        
        # Test save file detection
        self.screen.detect_save_file()
        self.assertIsNotNone(self.screen.save_file_path)
        
        # Test save file validation
        self.screen.validate_save_file()
        self.assertTrue(self.screen.save_file_valid)
        
        # Test save file loading
        self.screen.load_save_file()
        self.assertIsNotNone(self.screen.saved_game_info)
        
        # Test save file error handling
        self.screen.handle_save_file_error()
        self.assertTrue(self.screen.has_error)
        self.assertIsNotNone(self.screen.save_file_error)

    def test_user_choice_handling(self):
        """Test user choice handling functionality."""
        # Test resume game choice
        self.screen.has_saved_game = True
        self.screen.saved_game_info = {
            'players': ['Player1', 'Player2'],
            'current_round': 3,
            'scores': {'Player1': 10, 'Player2': 5}
        }
        self.screen.resume_game()
        self.assertTrue(self.screen.game_resumed)
        
        # Test new game choice
        self.screen.start_new_game()
        self.assertTrue(self.screen.new_game_started)
        
        # Test invalid choice
        with self.assertRaises(ValidationError):
            self.screen.resume_game()  # No saved game

    def test_screen_transitions(self):
        """Test screen transitions."""
        # Test to name entry screen
        self.screen.start_new_game()
        # Verify screen transition (would need to mock screen manager)
        
        # Test to scoreboard screen
        self.screen.has_saved_game = True
        self.screen.saved_game_info = {
            'players': ['Player1', 'Player2'],
            'current_round': 3,
            'scores': {'Player1': 10, 'Player2': 5}
        }
        self.screen.resume_game()
        # Verify screen transition (would need to mock screen manager)

    def test_error_handling(self):
        """Test error handling functionality."""
        # Test save file error
        self.screen.handle_save_file_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('save file', self.screen._current_error.lower())
        
        # Test state error
        self.screen.handle_state_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('state', self.screen._current_error.lower())
        
        # Test validation error
        self.screen.handle_validation_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('validation', self.screen._current_error.lower())

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
            'type': 'game_state',
            'has_saved_game': True
        }
        self.screen.handle_client_update(update)
        self.assertTrue(self.screen.has_saved_game)
        
        # Test invalid update
        with self.assertRaises(ValidationError):
            self.screen.handle_client_update({
                'type': 'invalid_type'
            })

    def test_input_validation(self):
        """Test input validation."""
        # Test valid input
        self.assertTrue(self.screen.validate_input({
            'choice': 'resume'
        }, {
            'choice': lambda x: x in ['resume', 'new']
        }))
        
        # Test invalid input
        with self.assertRaises(ValidationError):
            self.screen.validate_input({
                'choice': 'invalid'
            }, {
                'choice': lambda x: x in ['resume', 'new']
            })

    def test_state_validation(self):
        """Test state validation."""
        # Test valid state
        self.assertTrue(self.screen.validate_state([
            'has_saved_game', 'saved_game_info', 'save_file_path',
            'save_file_valid', 'save_file_error'
        ]))
        
        # Test invalid state
        with self.assertRaises(StateError):
            self.screen.validate_state(['missing_key'])

# ... existing code ... 