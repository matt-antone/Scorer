import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.app import App
from kivy.clock import Clock
from pi_client.screens.deployment_setup_screen import DeploymentSetupScreen
from pi_client.screens.base_screen import ValidationError, StateError
from pi_client.tests.graphical.test_base import BaseScreenTest

class TestApp(App):
    """Test application with game state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = {
            'players': [],
            'roles': {},
            'deployment_sequence': [],
            'rolls': {},
            'roll_validation': {
                'min_value': 1,
                'max_value': 6,
                'required_rolls': 2
            }
        }

class TestDeploymentSetupScreen(BaseScreenTest):
    """Test cases for DeploymentSetupScreen."""

    app_class = TestApp

    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.screen = DeploymentSetupScreen()
        self.screen.deployment_sequence = []
        self.screen.players = ['Player1', 'Player2']  # Add test players
        self.screen.roles = ['Attacker', 'Defender']  # Roles as a list
        self.screen.rolls = {}
        self.screen.roll_validation = {}
        self.screen._current_error = None
        self.screen.has_error = False
        # Update app.game_state to match screen properties
        self.screen.app.game_state['players'] = self.screen.players
        self.screen.app.game_state['roles'] = self.screen.roles
        self.screen.app.game_state['deployment_sequence'] = self.screen.deployment_sequence
        self.screen.app.game_state['rolls'] = self.screen.rolls
        self.screen.app.game_state['roll_validation'] = self.screen.roll_validation
        self.screen.on_enter()
        self.advance_frames(1)

    def test_initial_state(self):
        """Test initial state of DeploymentSetupScreen."""
        screen = DeploymentSetupScreen()  # Create a new instance for initial state test
        self.assertFalse(screen.is_loading)
        self.assertFalse(screen.is_syncing)
        self.assertFalse(screen.has_error)
        self.assertEqual(len(screen.players), 0)
        self.assertEqual(len(screen.roles), 0)
        self.assertEqual(len(screen.deployment_sequence), 0)
        self.assertEqual(len(self.screen.rolls), 0)

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
        
        # Test roll sequence
        self.screen.add_roll("Player1", 3)
        self.screen.add_roll("Player1", 4)
        self.assertTrue(self.screen.validate_roll_sequence("Player1"))

    def test_deployment_sequence(self):
        """Test deployment sequence functionality."""
        # Test sequence generation
        self.screen.generate_deployment_sequence()
        self.assertGreater(len(self.screen.deployment_sequence), 0)
        self.assertEqual(len(self.screen.deployment_sequence), len(self.screen.players))
    
        # Test sequence validation
        self.assertTrue(self.screen.validate_deployment_sequence())
        
        # Test sequence update
        old_sequence = self.screen.deployment_sequence.copy()
        self.screen.update_deployment_sequence()
        self.assertNotEqual(self.screen.deployment_sequence, old_sequence)
        
        # Test sequence reset
        self.screen.reset_deployment_sequence()
        self.assertEqual(len(self.screen.deployment_sequence), 0)

    def test_screen_transitions(self):
        """Test screen transitions."""
        # Test to initiative screen
        self.screen.assign_role("Player1", "Attacker")
        self.screen.assign_role("Player2", "Defender")
        self.screen.proceed_to_initiative()
        # Verify screen transition (would need to mock screen manager)
        
        # Test back to name entry screen
        self.screen.back_to_name_entry()
        # Verify screen transition (would need to mock screen manager)

    def test_error_handling(self):
        """Test error handling functionality."""
        # Test role validation error
        self.screen.handle_role_validation_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('role', self.screen._current_error.lower())
        
        # Reset error state
        self.screen.has_error = False
        self.screen._current_error = None
        
        # Test roll validation error
        self.screen.handle_roll_validation_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('roll', self.screen._current_error.lower())
        
        # Test sequence validation error
        self.screen.handle_sequence_validation_error()
        self.assertTrue(self.screen.has_error)
        self.assertIn('sequence', self.screen._current_error.lower())

    def test_input_validation(self):
        """Test input validation."""
        # Test valid input
        self.assertTrue(self.screen.validate_input({
            'role': 'Attacker'
        }, {
            'role': self.screen.validate_role
        }))
        
        # Test invalid input
        with self.assertRaises(ValidationError):
            self.screen.validate_input({
                'role': 'InvalidRole'
            }, {
                'role': self.screen.validate_role
            })

    def test_state_validation(self):
        """Test state validation."""
        # Test valid state
        self.assertTrue(self.screen.validate_state([
            'players', 'roles', 'deployment_sequence', 'rolls',
            'roll_validation'
        ]))
        
        # Test invalid state
        self.assertFalse(self.screen.validate_state(['missing_key']))

# ... existing code ... 