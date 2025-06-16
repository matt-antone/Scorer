import unittest
from pi_client.screens.splash_screen import SplashScreen
from pi_client.state.splash_state import SplashState
from pi_client.screens.base_screen import ValidationError, StateError

class TestSplashScreen(unittest.TestCase):
    def setUp(self):
        self.state = SplashState(is_loading=True)
        self.screen = SplashScreen()
        self.screen.state = self.state
        self.screen.is_loading = self.state.is_loading

    def test_initial_state(self):
        """Test initial state validation"""
        self.assertTrue(self.state.validate_state())
        self.assertTrue(self.screen.is_loading)

    def test_state_validation(self):
        """Test state validation"""
        # Valid state
        self.assertTrue(self.state.validate_state())
        self.assertTrue(self.screen.validate_state())

        # Invalid state - non-boolean is_loading
        self.state.is_loading = 'true'
        self.assertFalse(self.state.validate_state())
        self.assertFalse(self.screen.validate_state())

    def test_loading_validation(self):
        """Test loading validation"""
        # Valid is_loading
        self.state.is_loading = False
        self.assertTrue(self.state.validate_is_loading())
        self.assertTrue(self.screen.validate_is_loading())

        # Invalid is_loading
        self.state.is_loading = 'true'
        self.assertFalse(self.state.validate_is_loading())
        self.assertFalse(self.screen.validate_is_loading())

    def test_error_handling(self):
        """Test error handling"""
        # Test with invalid state
        self.state.is_loading = 'true'
        self.assertFalse(self.state.validate_state())
        self.assertFalse(self.screen.validate_state())

if __name__ == '__main__':
    unittest.main() 