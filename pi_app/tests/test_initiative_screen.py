import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.app import App
from kivy.clock import Clock
from pi_app.screens.initiative_screen import InitiativeScreen
from pi_app.screens.base_screen import ValidationError, StateError

class TestApp(App):
    """Test application with game state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = {
            'players': ['Player1', 'Player2'],
            'deployment_winner': 'Player1',
            'deployment_loser': 'Player2',
            'player_rolls': {},
            'initiative_winner': None,
            'initiative_loser': None,
            'current_round': 1,
            'max_rounds': 5
        }

class InitiativeScreenTest(GraphicUnitTest):
    """Test cases for InitiativeScreen."""

    def setUp(self):
        """Set up test environment."""
        self.app = TestApp()
        self.screen = InitiativeScreen()
        self.app.game_state = {
            'players': ['Player1', 'Player2'],
            'deployment_winner': 'Player1',
            'deployment_loser': 'Player2',
            'player_rolls': {},
            'initiative_winner': None,
            'initiative_loser': None,
            'current_round': 1,
            'max_rounds': 5
        }

    def tearDown(self):
        """Clean up test environment."""
        self.screen.stop_sync()
        if self.screen._error_timeout:
            self.screen._error_timeout.cancel()

    def test_initial_state(self):
        """Test initial state of InitiativeScreen."""
        self.assertFalse(self.screen.is_loading)
        self.assertFalse(self.screen.is_syncing)
        self.assertFalse(self.screen.has_error)
        self.assertEqual(len(self.screen.player_rolls), 0)
        self.assertIsNone(self.screen.initiative_winner)
        self.assertIsNone(self.screen.initiative_loser)
        self.assertEqual(self.screen.current_round, 1)

    def test_roll_sequence(self):
        """Test roll sequence functionality."""
        # Test initial state
        self.assertEqual(len(self.screen.player_rolls), 0)
        
        # Test first player roll
        self.screen.roll_dice('Player1')
        self.assertEqual(len(self.screen.player_rolls), 1)
        self.assertIn('Player1', self.screen.player_rolls)
        
        # Test second player roll
        self.screen.roll_dice('Player2')
        self.assertEqual(len(self.screen.player_rolls), 2)
        self.assertIn('Player2', self.screen.player_rolls)
        
        # Test roll completion
        self.assertTrue(self.screen.rolls_complete())
        
        # Test invalid roll sequence
        with self.assertRaises(ValidationError):
            self.screen.roll_dice('Player1')  # Already rolled

    def test_winner_determination(self):
        """Test winner determination functionality."""
        # Test initial state
        self.assertIsNone(self.screen.initiative_winner)
        self.assertIsNone(self.screen.initiative_loser)
        
        # Test winner determination after rolls
        self.screen.roll_dice('Player1')
        self.screen.roll_dice('Player2')
        winner, loser = self.screen.determine_winner()
        self.screen.assign_roles(winner, loser)
        
        self.assertEqual(self.screen.initiative_winner, winner)
        self.assertEqual(self.screen.initiative_loser, loser)
        self.assertEqual(self.app.game_state['initiative_winner'], winner)
        self.assertEqual(self.app.game_state['initiative_loser'], loser)
        
        # Test invalid winner assignment
        with self.assertRaises(ValidationError):
            self.screen.assign_roles('InvalidPlayer', 'Player2')
        
        # Test same player assignment
        with self.assertRaises(ValidationError):
            self.screen.assign_roles('Player1', 'Player1')

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
            'type': 'roll',
            'player': 'Player1',
            'value': 6
        }
        self.screen.handle_client_update(update)
        self.assertIn('Player1', self.screen.player_rolls)
        self.assertEqual(self.screen.player_rolls['Player1'], 6)
        
        # Test invalid update
        with self.assertRaises(ValidationError):
            self.screen.handle_client_update({
                'type': 'invalid_type'
            })

    def test_screen_transitions(self):
        """Test screen transitions."""
        # Test back to deployment setup
        self.screen.back_to_deployment()
        # Verify screen transition (would need to mock screen manager)
        
        # Test continue to scoreboard
        self.screen.roll_dice('Player1')
        self.screen.roll_dice('Player2')
        winner, loser = self.screen.determine_winner()
        self.screen.assign_roles(winner, loser)
        self.screen.continue_to_scoreboard()
        # Verify screen transition (would need to mock screen manager)
        
        # Test continue without rolls
        with self.assertRaises(ValidationError):
            self.screen.continue_to_scoreboard()

    def test_roll_display(self):
        """Test roll display functionality."""
        # Test initial display
        self.assertEqual(self.screen.get_roll_display('Player1'), '')
        self.assertEqual(self.screen.get_roll_display('Player2'), '')
        
        # Test roll display after roll
        self.screen.roll_dice('Player1')
        self.assertNotEqual(self.screen.get_roll_display('Player1'), '')
        
        # Test roll display after both rolls
        self.screen.roll_dice('Player2')
        self.assertNotEqual(self.screen.get_roll_display('Player1'), '')
        self.assertNotEqual(self.screen.get_roll_display('Player2'), '')

    def test_error_handling(self):
        """Test error handling functionality."""
        # Test roll error
        self.screen.handle_roll_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('roll', self.screen._current_error.lower())
        
        # Test winner determination error
        self.screen.handle_winner_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('winner', self.screen._current_error.lower())
        
        # Test sync error
        self.screen.handle_sync_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('sync', self.screen._current_error.lower())

    def test_input_validation(self):
        """Test input validation."""
        # Test valid input
        self.assertTrue(self.screen.validate_input({
            'player': 'Player1'
        }, {
            'player': lambda x: x in self.app.game_state['players']
        }))
        
        # Test invalid input
        with self.assertRaises(ValidationError):
            self.screen.validate_input({
                'player': 'InvalidPlayer'
            }, {
                'player': lambda x: x in self.app.game_state['players']
            })

    def test_state_validation(self):
        """Test state validation."""
        # Test valid state
        self.assertTrue(self.screen.validate_state([
            'players', 'player_rolls', 'current_round', 'max_rounds'
        ]))
        
        # Test invalid state
        with self.assertRaises(StateError):
            self.screen.validate_state(['missing_key'])

# ... existing code ... 