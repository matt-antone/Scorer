import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.app import App
from kivy.clock import Clock
from pi_app.screens.splash_screen import SplashScreen
from pi_app.screens.base_screen import ValidationError, StateError

class TestApp(App):
    """Test application with game state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = {
            'app_version': '1.0.0',
            'loading_progress': 0,
            'loading_status': 'Initializing...',
            'has_saved_game': False,
            'saved_game_info': None,
            'system_checks': {
                'network': False,
                'resources': False,
                'storage': False
            },
            'resources': {
                'images': [],
                'fonts': [],
                'sounds': []
            }
        }

class SplashScreenTest(GraphicUnitTest):
    """Test cases for SplashScreen."""

    def setUp(self):
        """Set up test environment."""
        self.app = TestApp()
        self.screen = SplashScreen()
        self.app.game_state = {
            'app_version': '1.0.0',
            'loading_progress': 0,
            'loading_status': 'Initializing...',
            'has_saved_game': False,
            'saved_game_info': None,
            'system_checks': {
                'network': False,
                'resources': False,
                'storage': False
            },
            'resources': {
                'images': [],
                'fonts': [],
                'sounds': []
            }
        }

    def tearDown(self):
        """Clean up test environment."""
        self.screen.stop_sync()
        if self.screen._error_timeout:
            self.screen._error_timeout.cancel()
        if self.screen._loading_timeout:
            self.screen._loading_timeout.cancel()

    def test_initial_state(self):
        """Test initial state of SplashScreen."""
        self.assertFalse(self.screen.is_loading)
        self.assertFalse(self.screen.is_syncing)
        self.assertFalse(self.screen.has_error)
        self.assertEqual(self.screen.app_version, '1.0.0')
        self.assertEqual(self.screen.loading_progress, 0)
        self.assertEqual(self.screen.loading_status, 'Initializing...')
        self.assertFalse(self.screen.has_saved_game)
        self.assertIsNone(self.screen.saved_game_info)

    def test_system_checks(self):
        """Test system check functionality."""
        # Test initial state
        self.assertFalse(self.screen.system_checks['network'])
        self.assertFalse(self.screen.system_checks['resources'])
        self.assertFalse(self.screen.system_checks['storage'])
        
        # Test network check
        self.screen.check_network()
        self.assertTrue(self.screen.system_checks['network'])
        
        # Test resource check
        self.screen.check_resources()
        self.assertTrue(self.screen.system_checks['resources'])
        
        # Test storage check
        self.screen.check_storage()
        self.assertTrue(self.screen.system_checks['storage'])
        
        # Test all checks complete
        self.assertTrue(self.screen.all_checks_complete())

    def test_resource_initialization(self):
        """Test resource initialization functionality."""
        # Test initial state
        self.assertEqual(len(self.screen.resources['images']), 0)
        self.assertEqual(len(self.screen.resources['fonts']), 0)
        self.assertEqual(len(self.screen.resources['sounds']), 0)
        
        # Test image loading
        self.screen.load_images()
        self.assertGreater(len(self.screen.resources['images']), 0)
        
        # Test font loading
        self.screen.load_fonts()
        self.assertGreater(len(self.screen.resources['fonts']), 0)
        
        # Test sound loading
        self.screen.load_sounds()
        self.assertGreater(len(self.screen.resources['sounds']), 0)
        
        # Test resource validation
        self.assertTrue(self.screen.validate_resources())

    def test_error_recovery(self):
        """Test error recovery functionality."""
        # Test network error recovery
        self.screen.handle_network_error()
        self.assertTrue(self.screen.has_error)
        self.screen.recover_from_network_error()
        self.assertFalse(self.screen.has_error)
        
        # Test resource error recovery
        self.screen.handle_resource_error()
        self.assertTrue(self.screen.has_error)
        self.screen.recover_from_resource_error()
        self.assertFalse(self.screen.has_error)
        
        # Test storage error recovery
        self.screen.handle_storage_error()
        self.assertTrue(self.screen.has_error)
        self.screen.recover_from_storage_error()
        self.assertFalse(self.screen.has_error)

    def test_update_view_from_state(self):
        """Test view update from state."""
        # Test with initial state
        self.screen.update_view_from_state()
        self.assertEqual(self.screen.app_version, '1.0.0')
        self.assertEqual(self.screen.loading_progress, 0)
        
        # Test with updated loading progress
        self.app.game_state['loading_progress'] = 50
        self.app.game_state['loading_status'] = 'Loading resources...'
        self.screen.update_view_from_state()
        self.assertEqual(self.screen.loading_progress, 50)
        self.assertEqual(self.screen.loading_status, 'Loading resources...')
        
        # Test with saved game
        self.app.game_state['has_saved_game'] = True
        self.app.game_state['saved_game_info'] = {
            'players': ['Player1', 'Player2'],
            'current_round': 3,
            'scores': {'Player1': 10, 'Player2': 5}
        }
        self.screen.update_view_from_state()
        self.assertTrue(self.screen.has_saved_game)
        self.assertEqual(self.screen.saved_game_info['current_round'], 3)

    def test_update_loading_progress(self):
        """Test loading progress update."""
        # Test valid progress update
        self.screen.update_loading_progress(50, 'Loading resources...')
        self.assertEqual(self.screen.loading_progress, 50)
        self.assertEqual(self.screen.loading_status, 'Loading resources...')
        self.assertEqual(self.app.game_state['loading_progress'], 50)
        self.assertEqual(self.app.game_state['loading_status'], 'Loading resources...')
        
        # Test invalid progress
        with self.assertRaises(ValidationError):
            self.screen.update_loading_progress(-1, 'Invalid progress')
        
        # Test progress over 100
        with self.assertRaises(ValidationError):
            self.screen.update_loading_progress(101, 'Invalid progress')

    def test_check_saved_game(self):
        """Test saved game checking."""
        # Test no saved game
        self.screen.check_saved_game()
        self.assertFalse(self.screen.has_saved_game)
        self.assertIsNone(self.screen.saved_game_info)
        
        # Test with saved game
        self.app.game_state['has_saved_game'] = True
        self.app.game_state['saved_game_info'] = {
            'players': ['Player1', 'Player2'],
            'current_round': 3,
            'scores': {'Player1': 10, 'Player2': 5}
        }
        self.screen.check_saved_game()
        self.assertTrue(self.screen.has_saved_game)
        self.assertEqual(self.screen.saved_game_info['current_round'], 3)

    def test_recover_from_error(self):
        """Test error recovery."""
        # Test with validation error
        self.screen.handle_error(ValidationError("Test error"))
        self.screen.recover_from_error()
        self.assertFalse(self.screen.has_error)
        
        # Test with state error
        self.screen.handle_error(StateError("Test error"))
        self.screen.recover_from_error()
        self.assertFalse(self.screen.has_error)

    def test_broadcast_state(self):
        """Test state broadcasting."""
        self.screen.update_loading_progress(50, 'Loading resources...')
        self.screen.broadcast_state()
        # Verify state was broadcast (would need to mock WebSocket)

    def test_handle_client_update(self):
        """Test client update handling."""
        # Test valid loading update
        update = {
            'type': 'loading',
            'progress': 50,
            'status': 'Loading resources...'
        }
        self.screen.handle_client_update(update)
        self.assertEqual(self.screen.loading_progress, 50)
        self.assertEqual(self.screen.loading_status, 'Loading resources...')
        
        # Test valid saved game update
        update = {
            'type': 'saved_game',
            'has_saved_game': True,
            'game_info': {
                'players': ['Player1', 'Player2'],
                'current_round': 3
            }
        }
        self.screen.handle_client_update(update)
        self.assertTrue(self.screen.has_saved_game)
        self.assertEqual(self.screen.saved_game_info['current_round'], 3)
        
        # Test invalid update
        with self.assertRaises(ValidationError):
            self.screen.handle_client_update({
                'type': 'invalid_type'
            })

    def test_screen_transitions(self):
        """Test screen transitions."""
        # Test to resume game
        self.app.game_state['has_saved_game'] = True
        self.screen.start_game()
        # Verify screen transition (would need to mock screen manager)
        
        # Test to new game
        self.app.game_state['has_saved_game'] = False
        self.screen.start_game()
        # Verify screen transition (would need to mock screen manager)

    def test_loading_validation(self):
        """Test loading validation."""
        # Test valid progress
        self.assertTrue(self.screen.validate_loading_progress(50))
        
        # Test invalid progress
        with self.assertRaises(ValidationError):
            self.screen.validate_loading_progress(-1)
        
        # Test progress over 100
        with self.assertRaises(ValidationError):
            self.screen.validate_loading_progress(101)

    def test_saved_game_validation(self):
        """Test saved game validation."""
        # Test valid saved game
        self.assertTrue(self.screen.validate_saved_game({
            'players': ['Player1', 'Player2'],
            'current_round': 3,
            'scores': {'Player1': 10, 'Player2': 5}
        }))
        
        # Test invalid saved game
        with self.assertRaises(ValidationError):
            self.screen.validate_saved_game({
                'invalid_key': 'value'
            })

    def test_state_validation(self):
        """Test state validation."""
        # Test valid state
        self.assertTrue(self.screen.validate_state([
            'app_version', 'loading_progress', 'loading_status',
            'has_saved_game', 'saved_game_info', 'system_checks',
            'resources'
        ]))
        
        # Test invalid state
        with self.assertRaises(StateError):
            self.screen.validate_state(['missing_key'])

    def test_network_check(self):
        """Test network check functionality."""
        # Test network check initialization
        self.assertFalse(self.screen.has_network)
        self.assertFalse(self.screen.network_check_complete)
        
        # Test successful network check
        self.screen.check_network()
        self.assertTrue(self.screen.has_network)
        self.assertTrue(self.screen.network_check_complete)
        
        # Test network check failure
        self.screen.has_network = False
        self.screen.network_check_complete = False
        self.screen.check_network()
        self.assertFalse(self.screen.has_network)
        self.assertTrue(self.screen.network_check_complete)
        self.assertTrue(self.screen.has_error)
        self.assertIn('network', self.screen._current_error.lower())

    def test_qr_code_generation(self):
        """Test QR code generation functionality."""
        # Test QR code initialization
        self.assertIsNone(self.screen.player1_qr)
        self.assertIsNone(self.screen.player2_qr)
        self.assertIsNone(self.screen.observer_qr)
        
        # Test QR code generation
        self.screen.generate_qr_codes()
        self.assertIsNotNone(self.screen.player1_qr)
        self.assertIsNotNone(self.screen.player2_qr)
        self.assertIsNotNone(self.screen.observer_qr)
        
        # Test QR code content
        self.assertIn('player1', self.screen.player1_qr.lower())
        self.assertIn('player2', self.screen.player2_qr.lower())
        self.assertIn('observer', self.screen.observer_qr.lower())

    def test_loading_progress(self):
        """Test loading progress functionality."""
        # Test initial progress
        self.assertEqual(self.screen.loading_progress, 0)
        
        # Test progress update
        self.screen.update_loading_progress(50)
        self.assertEqual(self.screen.loading_progress, 50)
        
        # Test progress completion
        self.screen.update_loading_progress(100)
        self.assertEqual(self.screen.loading_progress, 100)
        self.assertFalse(self.screen.is_loading)
        
        # Test invalid progress
        with self.assertRaises(ValidationError):
            self.screen.update_loading_progress(-1)
        with self.assertRaises(ValidationError):
            self.screen.update_loading_progress(101)

    def test_loading_status(self):
        """Test loading status functionality."""
        # Test initial status
        self.assertEqual(self.screen.loading_status, 'Initializing...')
        
        # Test status update
        self.screen.update_loading_status('Checking network...')
        self.assertEqual(self.screen.loading_status, 'Checking network...')
        
        # Test status completion
        self.screen.update_loading_status('Ready!')
        self.assertEqual(self.screen.loading_status, 'Ready!')
        self.assertFalse(self.screen.is_loading)

    def test_saved_game_detection(self):
        """Test saved game detection functionality."""
        # Test no saved game
        self.screen.check_saved_game()
        self.assertFalse(self.screen.has_saved_game)
        self.assertIsNone(self.screen.saved_game_info)
        
        # Test with saved game
        self.app.game_state['has_saved_game'] = True
        self.app.game_state['saved_game_info'] = {
            'players': ['Player1', 'Player2'],
            'current_round': 3,
            'scores': {'Player1': 10, 'Player2': 5}
        }
        self.screen.check_saved_game()
        self.assertTrue(self.screen.has_saved_game)
        self.assertIsNotNone(self.screen.saved_game_info)

    def test_start_button_state(self):
        """Test start button state management."""
        # Test initial state
        self.assertFalse(self.screen.start_button_enabled)
        
        # Test enabling conditions
        self.screen.has_network = True
        self.screen.network_check_complete = True
        self.screen.update_start_button_state()
        self.assertTrue(self.screen.start_button_enabled)
        
        # Test disabling conditions
        self.screen.has_network = False
        self.screen.update_start_button_state()
        self.assertFalse(self.screen.start_button_enabled)

    def test_error_handling(self):
        """Test error handling functionality."""
        # Test network error
        self.screen.handle_network_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('network', self.screen._current_error.lower())
        
        # Test QR code error
        self.screen.handle_qr_code_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('qr code', self.screen._current_error.lower())
        
        # Test loading error
        self.screen.handle_loading_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('loading', self.screen._current_error.lower())

if __name__ == '__main__':
    unittest.main() 