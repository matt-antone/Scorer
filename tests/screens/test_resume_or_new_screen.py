import unittest
from pi_client.screens.resume_or_new_screen import ResumeOrNewScreen
from pi_client.state.resume_or_new_state import ResumeOrNewState
from pi_client.screens.base_screen import ValidationError, StateError

class TestResumeOrNewScreen(unittest.TestCase):
    def setUp(self):
        self.state = ResumeOrNewState(has_saved_game=False)
        self.screen = ResumeOrNewScreen()
        self.screen.state = self.state
        self.screen.has_saved_game = self.state.has_saved_game

    def test_initial_state(self):
        """Test initial state validation"""
        self.assertTrue(self.state.validate_state())
        self.assertFalse(self.screen.has_saved_game)

    def test_state_validation(self):
        """Test state validation"""
        # Valid state
        self.assertTrue(self.state.validate_state())
        self.assertTrue(self.screen.validate_state())

        # Invalid state - non-boolean has_saved_game
        self.state.has_saved_game = 'true'
        self.assertFalse(self.state.validate_state())
        self.assertFalse(self.screen.validate_state())

    def test_saved_game_validation(self):
        """Test saved game validation"""
        # Valid has_saved_game
        self.state.has_saved_game = True
        self.assertTrue(self.state.validate_has_saved_game())
        self.assertTrue(self.screen.validate_has_saved_game())

        # Invalid has_saved_game
        self.state.has_saved_game = 'true'
        self.assertFalse(self.state.validate_has_saved_game())
        self.assertFalse(self.screen.validate_has_saved_game())

    def test_error_handling(self):
        """Test error handling"""
        # Test with invalid state
        self.state.has_saved_game = 'true'
        self.assertFalse(self.state.validate_state())
        self.assertFalse(self.screen.validate_state())

if __name__ == '__main__':
    unittest.main() 