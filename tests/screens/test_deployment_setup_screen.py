import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.app import App
from kivy.clock import Clock
from pi_app.screens.deployment_setup_screen import DeploymentSetupScreen
from pi_app.screens.base_screen import ValidationError, StateError

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

class DeploymentSetupScreenTest(GraphicUnitTest):
    """Test cases for DeploymentSetupScreen."""

    def setUp(self):
        """Set up test environment."""
        self.app = TestApp()
        self.screen = DeploymentSetupScreen()
        self.app.game_state = {
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

    def tearDown(self):
        """Clean up test environment."""
        self.screen.stop_sync()
        if self.screen._error_timeout:
            self.screen._error_timeout.cancel()

    def test_initial_state(self):
        """Test initial state of DeploymentSetupScreen."""
        self.assertFalse(self.screen.is_loading)
        self.assertFalse(self.screen.is_syncing)
        self.assertFalse(self.screen.has_error)
        self.assertEqual(len(self.screen.players), 0)
        self.assertEqual(len(self.screen.roles), 0)
        self.assertEqual(len(self.screen.deployment_sequence), 0)
        self.assertEqual(len(self.screen.rolls), 0)

    def test_role_assignment(self):
        """Test role assignment functionality."""
        # Test role assignment
        self.screen.assign_role("Player1", "Attacker")
        self.assertEqual(self.screen.roles["Player1"], "Attacker")
        
        # Test role validation
        self.assertTrue(self.screen.validate_role("Attacker"))
        with self.assertRaises(ValidationError):
            self.screen.validate_role("InvalidRole")
        
        # Test role update
        self.screen.update_role("Player1", "Defender")
        self.assertEqual(self.screen.roles["Player1"], "Defender")
        
        # Test role removal
        self.screen.remove_role("Player1")
        self.assertNotIn("Player1", self.screen.roles)

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
            'type': 'roles',
            'roles': {'Player1': 'Attacker', 'Player2': 'Defender'}
        }
        self.screen.handle_client_update(update)
        self.assertEqual(len(self.screen.roles), 2)
        
        # Test invalid update
        with self.assertRaises(ValidationError):
            self.screen.handle_client_update({
                'type': 'invalid_type'
            })

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
        with self.assertRaises(StateError):
            self.screen.validate_state(['missing_key'])

# ... existing code ... 