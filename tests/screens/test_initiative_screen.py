import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.app import App
from kivy.clock import Clock
from pi_client.screens.initiative_screen import InitiativeScreen
from pi_client.screens.base_screen import ValidationError, StateError
from pi_client.tests.graphical.test_base import BaseScreenTest
from kivy.uix.screenmanager import ScreenManager

class TestApp(App):
    """Test application with game state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = {
            'players': [],
            'rolls': {},
            'roll_validation': {
                'min_value': 1,
                'max_value': 6
            }
        }
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InitiativeScreen(name='initiative'))
        return sm

class TestInitiativeScreen(BaseScreenTest):
    """Test cases for InitiativeScreen."""

    app_class = TestApp

    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.screen = self.get_screen('initiative')
        # Initialize game state with players
        self.app.game_state['players'] = ['Player1', 'Player2']
        self.app.game_state['rolls'] = {}
        self.screen.on_enter()
        self.advance_frames(1)

    def test_initial_state(self):
        """Test initial state of InitiativeScreen."""
        self.assertFalse(self.screen.is_loading)
        self.assertFalse(self.screen.is_syncing)
        self.assertFalse(self.screen.has_error)
        self.assertEqual(len(self.screen.player_rolls), 0)
        self.assertIsNone(self.screen.initiative_winner)
        self.assertIsNone(self.screen.initiative_loser)
        self.assertEqual(self.screen.current_round, 1)

    def test_roll_validation(self):
        """Test roll validation functionality."""
        # Test valid roll
        self.assertTrue(self.screen.validate_roll(3))
        
        # Test roll too low
        with self.assertRaises(ValidationError):
            self.screen.validate_roll(0)
        
        # Test roll too high
        with self.assertRaises(ValidationError):
            self.screen.validate_roll(7)

    def test_initiative_determination(self):
        """Test initiative determination functionality."""
        # Test initiative determination
        self.screen.add_roll("Player1", 4)
        self.screen.add_roll("Player2", 3)
        self.screen.determine_initiative()
        self.assertEqual(self.screen.initiative_winner, "Player1")
        self.assertEqual(self.screen.initiative_loser, "Player2")
        
        # Test tie handling
        self.screen.reset_rolls()
        self.screen.add_roll("Player1", 4)
        self.screen.add_roll("Player2", 4)
        self.screen.determine_initiative()
        self.assertIsNone(self.screen.initiative_winner)
        self.assertIsNone(self.screen.initiative_loser)

    def test_screen_transitions(self):
        """Test screen transitions."""
        # Test to scoreboard screen
        self.screen.add_roll("Player1", 4)
        self.screen.add_roll("Player2", 3)
        self.screen.determine_initiative()
        self.screen.proceed_to_scoreboard()
        # Verify screen transition (would need to mock screen manager)
        
        # Test back to deployment setup screen
        self.screen.back_to_deployment()
        # Verify screen transition (would need to mock screen manager)

    def test_error_handling(self):
        """Test error handling functionality."""
        # Test roll validation error
        self.screen.handle_roll_validation_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('roll', self.screen._current_error.lower())
        
        # Test initiative determination error
        self.screen.handle_initiative_determination_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('initiative', self.screen._current_error.lower())
        
        # Test state error
        self.screen.handle_state_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('state', self.screen._current_error.lower())

    def test_input_validation(self):
        """Test input validation."""
        # Test valid input
        self.assertTrue(self.screen.validate_input({
            'roll': 3
        }, {
            'roll': self.screen.validate_roll
        }))
        
        # Test invalid input
        with self.assertRaises(ValidationError):
            self.screen.validate_input({
                'roll': 7
            }, {
                'roll': self.screen.validate_roll
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