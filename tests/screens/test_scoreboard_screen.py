import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.app import App
from kivy.clock import Clock
from pi_client.screens.scoreboard_screen import ScoreboardScreen
from pi_client.tests.graphical.test_base import BaseScreenTest
from pi_client.screens.base_screen import ValidationError, StateError

class TestApp(App):
    """Test application with game state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = {
            'players': ['Player1', 'Player2'],
            'initiative_winner': 'Player1',
            'initiative_loser': 'Player2',
            'current_round': 1,
            'max_rounds': 5,
            'scores': {
                'Player1': 0,
                'Player2': 0
            },
            'round_history': []
        }

class ScoreboardScreenTest(GraphicUnitTest):
    """Test cases for ScoreboardScreen."""

    def setUp(self):
        """Set up test environment."""
        self.app = TestApp()
        self.screen = ScoreboardScreen()
        self.app.game_state = {
            'players': ['Player1', 'Player2'],
            'initiative_winner': 'Player1',
            'initiative_loser': 'Player2',
            'current_round': 1,
            'max_rounds': 5,
            'scores': {
                'Player1': 0,
                'Player2': 0
            },
            'round_history': []
        }

    def tearDown(self):
        """Clean up test environment."""
        self.screen.stop_sync()
        if self.screen._error_timeout:
            self.screen._error_timeout.cancel()

    def test_initial_state(self):
        """Test initial state of ScoreboardScreen."""
        self.assertFalse(self.screen.is_loading)
        self.assertFalse(self.screen.is_syncing)
        self.assertFalse(self.screen.has_error)
        self.assertEqual(self.screen.current_round, 1)
        self.assertEqual(len(self.screen.round_history), 0)
        self.assertEqual(self.screen.scores['Player1'], 0)
        self.assertEqual(self.screen.scores['Player2'], 0)

    def test_score_tracking(self):
        """Test score tracking functionality."""
        # Test initial scores
        self.assertEqual(self.screen.scores['Player1'], 0)
        self.assertEqual(self.screen.scores['Player2'], 0)
        
        # Test score update
        self.screen.update_score('Player1', 5)
        self.assertEqual(self.screen.scores['Player1'], 5)
        self.assertEqual(self.app.game_state['scores']['Player1'], 5)
        
        # Test invalid score update
        with self.assertRaises(ValidationError):
            self.screen.update_score('InvalidPlayer', 5)
        
        # Test negative score
        with self.assertRaises(ValidationError):
            self.screen.update_score('Player1', -1)

    def test_round_management(self):
        """Test round management functionality."""
        # Test initial round
        self.assertEqual(self.screen.current_round, 1)
        
        # Test round increment
        self.screen.increment_round()
        self.assertEqual(self.screen.current_round, 2)
        self.assertEqual(self.app.game_state['current_round'], 2)
        
        # Test max rounds
        self.screen.current_round = 5
        with self.assertRaises(StateError):
            self.screen.increment_round()
        
        # Test round history
        self.screen.add_to_history({
            'round': 1,
            'scores': {
                'Player1': 5,
                'Player2': 3
            }
        })
        self.assertEqual(len(self.screen.round_history), 1)
        self.assertEqual(self.app.game_state['round_history'][0]['round'], 1)

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
            'type': 'score',
            'player': 'Player1',
            'value': 5
        }
        self.screen.handle_client_update(update)
        self.assertEqual(self.screen.scores['Player1'], 5)
        
        # Test invalid update
        with self.assertRaises(ValidationError):
            self.screen.handle_client_update({
                'type': 'invalid_type'
            })

    def test_screen_transitions(self):
        """Test screen transitions."""
        # Test back to initiative
        self.screen.back_to_initiative()
        # Verify screen transition (would need to mock screen manager)
        
        # Test continue to game over
        self.screen.current_round = 5
        self.screen.continue_to_game_over()
        # Verify screen transition (would need to mock screen manager)
        
        # Test continue before max rounds
        with self.assertRaises(ValidationError):
            self.screen.continue_to_game_over()

    def test_score_display(self):
        """Test score display functionality."""
        # Test initial display
        self.assertEqual(self.screen.get_score_display('Player1'), '0')
        self.assertEqual(self.screen.get_score_display('Player2'), '0')
        
        # Test score display after update
        self.screen.update_score('Player1', 5)
        self.assertEqual(self.screen.get_score_display('Player1'), '5')
        
        # Test round display
        self.assertEqual(self.screen.get_round_display(), 'Round 1')
        self.screen.increment_round()
        self.assertEqual(self.screen.get_round_display(), 'Round 2')

    def test_error_handling(self):
        """Test error handling functionality."""
        # Test score error
        self.screen.handle_score_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('score', self.screen._current_error.lower())
        
        # Test round error
        self.screen.handle_round_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('round', self.screen._current_error.lower())
        
        # Test sync error
        self.screen.handle_sync_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('sync', self.screen._current_error.lower())

    def test_input_validation(self):
        """Test input validation."""
        # Test valid input
        self.assertTrue(self.screen.validate_input({
            'player': 'Player1',
            'score': 5
        }, {
            'player': lambda x: x in self.app.game_state['players'],
            'score': lambda x: isinstance(x, int) and x >= 0
        }))
        
        # Test invalid input
        with self.assertRaises(ValidationError):
            self.screen.validate_input({
                'player': 'InvalidPlayer',
                'score': 5
            }, {
                'player': lambda x: x in self.app.game_state['players'],
                'score': lambda x: isinstance(x, int) and x >= 0
            })

    def test_state_validation(self):
        """Test state validation."""
        # Test valid state
        self.assertTrue(self.screen.validate_state([
            'players', 'scores', 'current_round', 'max_rounds', 'round_history'
        ]))
        
        # Test invalid state
        with self.assertRaises(StateError):
            self.screen.validate_state(['missing_key'])

# ... existing code ... 