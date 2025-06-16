import unittest
from pi_client.state.game_over_state import GameOverState

class TestGameOverState(unittest.TestCase):
    """Test cases for GameOverState (pure logic, no Kivy)."""

    def setUp(self):
        self.state = GameOverState(
            players=['Player1', 'Player2'],
            scores={'Player1': 10, 'Player2': 8},
            final_scores={'Player1': 10, 'Player2': 8},
            winner='Player1',
            game_duration=120,
            rounds_played=5
        )

    def test_validate_players(self):
        self.assertTrue(self.state.validate_players())
        self.state.players = ['Player1']
        self.assertFalse(self.state.validate_players())
        self.state.players = ['Player1', 2]
        self.assertFalse(self.state.validate_players())

    def test_validate_scores(self):
        self.assertTrue(self.state.validate_scores())
        self.state.scores = {'Player1': 10}
        self.assertFalse(self.state.validate_scores())
        self.state.scores = {'Player1': -1, 'Player2': 8}
        self.assertFalse(self.state.validate_scores())

    def test_validate_final_scores(self):
        self.assertTrue(self.state.validate_final_scores())
        self.state.final_scores = {'Player1': 10}
        self.assertFalse(self.state.validate_final_scores())
        self.state.final_scores = {'Player1': -1, 'Player2': 8}
        self.assertFalse(self.state.validate_final_scores())

    def test_validate_winner(self):
        self.assertTrue(self.state.validate_winner())
        self.state.winner = 'InvalidPlayer'
        self.assertFalse(self.state.validate_winner())
        self.state.winner = None
        self.assertFalse(self.state.validate_winner())

    def test_validate_game_duration(self):
        self.assertTrue(self.state.validate_game_duration())
        self.state.game_duration = -1
        self.assertFalse(self.state.validate_game_duration())

    def test_validate_rounds_played(self):
        self.assertTrue(self.state.validate_rounds_played())
        self.state.rounds_played = -1
        self.assertFalse(self.state.validate_rounds_played())

    def test_validate_state(self):
        self.assertTrue(self.state.validate_state())
        self.state.players = ['Player1']
        self.assertFalse(self.state.validate_state())
        self.state.players = ['Player1', 'Player2']
        self.state.scores = {'Player1': 10}
        self.assertFalse(self.state.validate_state())

if __name__ == '__main__':
    unittest.main() 