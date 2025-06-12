import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.app import App
from kivy.clock import Clock
from pi_app.screens.game_over_screen import GameOverScreen
from pi_app.screens.base_screen import ValidationError, StateError

class TestApp(App):
    """Test application with game state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = {
            'players': [],
            'scores': {},
            'winner': None,
            'game_history': [],
            'cleanup_required': False,
            'save_game': False
        }

class GameOverScreenTest(GraphicUnitTest):
    """Test cases for GameOverScreen."""

    def setUp(self):
        """Set up test environment."""
        self.app = TestApp()
        self.screen = GameOverScreen()
        self.app.game_state = {
            'players': [],
            'scores': {},
            'winner': None,
            'game_history': [],
            'cleanup_required': False,
            'save_game': False
        }

    def tearDown(self):
        """Clean up test environment."""
        self.screen.stop_sync()
        if self.screen._error_timeout:
            self.screen._error_timeout.cancel()

    def test_initial_state(self):
        """Test initial state of GameOverScreen."""
        self.assertFalse(self.screen.is_loading)
        self.assertFalse(self.screen.is_syncing)
        self.assertFalse(self.screen.has_error)
        self.assertEqual(len(self.screen.players), 0)
        self.assertEqual(len(self.screen.scores), 0)
        self.assertIsNone(self.screen.winner)
        self.assertEqual(len(self.screen.game_history), 0)
        self.assertFalse(self.screen.cleanup_required)
        self.assertFalse(self.screen.save_game)

    def test_final_score_display(self):
        """Test final score display functionality."""
        # Test score initialization
        self.screen.initialize_scores()
        self.assertEqual(len(self.screen.scores), 0)
        
        # Test score update
        self.screen.update_scores({'Player1': 10, 'Player2': 5})
        self.assertEqual(len(self.screen.scores), 2)
        self.assertEqual(self.screen.scores['Player1'], 10)
        self.assertEqual(self.screen.scores['Player2'], 5)
        
        # Test score validation
        self.assertTrue(self.screen.validate_scores())
        
        # Test score display
        score_display = self.screen.get_score_display()
        self.assertIn('Player1', score_display)
        self.assertIn('Player2', score_display)
        self.assertIn('10', score_display)
        self.assertIn('5', score_display)

    def test_winner_determination(self):
        """Test winner determination functionality."""
        # Test winner calculation
        self.screen.update_scores({'Player1': 10, 'Player2': 5})
        self.screen.determine_winner()
        self.assertEqual(self.screen.winner, 'Player1')
        
        # Test tie handling
        self.screen.update_scores({'Player1': 10, 'Player2': 10})
        self.screen.determine_winner()
        self.assertIsNone(self.screen.winner)
        
        # Test winner display
        self.screen.update_scores({'Player1': 10, 'Player2': 5})
        self.screen.determine_winner()
        winner_display = self.screen.get_winner_display()
        self.assertIn('Player1', winner_display)
        self.assertIn('winner', winner_display.lower())

    def test_game_state_cleanup(self):
        """Test game state cleanup functionality."""
        # Test cleanup initialization
        self.screen.initialize_cleanup()
        self.assertTrue(self.screen.cleanup_required)
        
        # Test cleanup execution
        self.screen.cleanup_game_state()
        self.assertFalse(self.screen.cleanup_required)
        self.assertEqual(len(self.screen.game_history), 1)
        
        # Test cleanup validation
        self.assertTrue(self.screen.validate_cleanup())
        
        # Test cleanup error handling
        self.screen.handle_cleanup_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('cleanup', self.screen._current_error.lower())

    def test_screen_transitions(self):
        """Test screen transitions."""
        # Test to splash screen
        self.screen.return_to_splash()
        # Verify screen transition (would need to mock screen manager)
        
        # Test to new game screen
        self.screen.start_new_game()
        # Verify screen transition (would need to mock screen manager)

    def test_error_handling(self):
        """Test error handling functionality."""
        # Test score validation error
        self.screen.handle_score_validation_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('score', self.screen._current_error.lower())
        
        # Test winner determination error
        self.screen.handle_winner_determination_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('winner', self.screen._current_error.lower())
        
        # Test cleanup error
        self.screen.handle_cleanup_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('cleanup', self.screen._current_error.lower())

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
            'type': 'scores',
            'scores': {'Player1': 10, 'Player2': 5}
        }
        self.screen.handle_client_update(update)
        self.assertEqual(len(self.screen.scores), 2)
        
        # Test invalid update
        with self.assertRaises(ValidationError):
            self.screen.handle_client_update({
                'type': 'invalid_type'
            })

    def test_input_validation(self):
        """Test input validation."""
        # Test valid input
        self.assertTrue(self.screen.validate_input({
            'action': 'new_game'
        }, {
            'action': lambda x: x in ['new_game', 'return_to_splash']
        }))
        
        # Test invalid input
        with self.assertRaises(ValidationError):
            self.screen.validate_input({
                'action': 'invalid_action'
            }, {
                'action': lambda x: x in ['new_game', 'return_to_splash']
            })

    def test_state_validation(self):
        """Test state validation."""
        # Test valid state
        self.assertTrue(self.screen.validate_state([
            'players', 'scores', 'winner', 'game_history',
            'cleanup_required', 'save_game'
        ]))
        
        # Test invalid state
        with self.assertRaises(StateError):
            self.screen.validate_state(['missing_key'])

# ... existing code ... 