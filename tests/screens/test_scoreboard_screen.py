import unittest
from pi_client.screens.scoreboard_screen import ScoreboardScreen
from pi_client.state.scoreboard_state import ScoreboardState
from pi_client.screens.base_screen import ValidationError, StateError

class TestScoreboardScreen(unittest.TestCase):
    def setUp(self):
        self.state = ScoreboardState(
            players=['Player 1', 'Player 2'],
            scores={'Player 1': 0, 'Player 2': 0},
            current_round=1
        )
        self.screen = ScoreboardScreen()
        self.screen.state = self.state
        self.screen.players = self.state.players
        self.screen.scores = self.state.scores
        self.screen.current_round = self.state.current_round

    def test_initial_state(self):
        """Test initial state validation"""
        self.assertTrue(self.state.validate_state())
        self.assertEqual(self.screen.players, ['Player 1', 'Player 2'])
        self.assertEqual(self.screen.scores, {'Player 1': 0, 'Player 2': 0})
        self.assertEqual(self.screen.current_round, 1)

    def test_state_validation(self):
        """Test state validation"""
        # Valid state
        self.assertTrue(self.state.validate_state())
        self.assertTrue(self.screen.validate_state())

        # Invalid state - missing players
        self.state.players = []
        self.assertFalse(self.state.validate_state())
        self.assertFalse(self.screen.validate_state())

        # Invalid state - invalid scores
        self.state.players = ['Player 1', 'Player 2']
        self.state.scores = {'Player 1': -1}
        self.assertFalse(self.state.validate_state())
        self.assertFalse(self.screen.validate_state())

        # Invalid state - invalid round
        self.state.scores = {'Player 1': 0, 'Player 2': 0}
        self.state.current_round = 6
        self.assertFalse(self.state.validate_state())
        self.assertFalse(self.screen.validate_state())

    def test_score_validation(self):
        """Test score validation"""
        # Valid scores
        self.assertTrue(self.state.validate_scores())
        self.assertTrue(self.screen.validate_scores())

        # Invalid scores - missing player
        self.state.scores = {'Player 1': 0}
        self.assertFalse(self.state.validate_scores())
        self.assertFalse(self.screen.validate_scores())

        # Invalid scores - negative score
        self.state.scores = {'Player 1': -1, 'Player 2': 0}
        self.assertFalse(self.state.validate_scores())
        self.assertFalse(self.screen.validate_scores())

        # Invalid scores - non-integer score
        self.state.scores = {'Player 1': '0', 'Player 2': 0}
        self.assertFalse(self.state.validate_scores())
        self.assertFalse(self.screen.validate_scores())

    def test_round_validation(self):
        """Test round validation"""
        # Valid rounds
        for round_num in range(1, 6):
            self.state.current_round = round_num
            self.assertTrue(self.state.validate_current_round())
            self.assertTrue(self.screen.validate_current_round())

        # Invalid rounds
        invalid_rounds = [0, 6, -1, '1']
        for round_num in invalid_rounds:
            self.state.current_round = round_num
            self.assertFalse(self.state.validate_current_round())
            self.assertFalse(self.screen.validate_current_round())

    def test_error_handling(self):
        """Test error handling"""
        # Test with invalid state
        self.state.players = []
        self.assertFalse(self.state.validate_state())
        self.assertFalse(self.screen.validate_state())

        # Test with invalid scores
        self.state.players = ['Player 1', 'Player 2']
        self.state.scores = {'Player 1': -1}
        self.assertFalse(self.state.validate_scores())
        self.assertFalse(self.screen.validate_scores())

        # Test with invalid round
        self.state.scores = {'Player 1': 0, 'Player 2': 0}
        self.state.current_round = 6
        self.assertFalse(self.state.validate_current_round())
        self.assertFalse(self.screen.validate_current_round())

if __name__ == '__main__':
    unittest.main() 