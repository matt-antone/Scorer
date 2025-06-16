import unittest
from pi_client.state.initiative_state import InitiativeState

class TestInitiativeState(unittest.TestCase):
    """Test cases for InitiativeState (pure logic, no Kivy)."""

    def setUp(self):
        self.state = InitiativeState(
            players=['Player1', 'Player2'],
            initiative_rolls={'Player1': 5, 'Player2': 3},
            initiative_validation={'Player1': True, 'Player2': True}
        )

    def test_validate_players(self):
        self.assertTrue(self.state.validate_players())
        self.state.players = ['Player1']
        self.assertFalse(self.state.validate_players())
        self.state.players = ['Player1', 2]
        self.assertFalse(self.state.validate_players())

    def test_validate_initiative_rolls(self):
        self.assertTrue(self.state.validate_initiative_rolls())
        self.state.initiative_rolls = {'Player1': 5}
        self.assertFalse(self.state.validate_initiative_rolls())
        self.state.initiative_rolls = {'Player1': 7, 'Player2': 3}
        self.assertFalse(self.state.validate_initiative_rolls())
        self.state.initiative_rolls = {'Player1': 5, 'Player2': 0}
        self.assertFalse(self.state.validate_initiative_rolls())

    def test_validate_initiative_validation(self):
        self.assertTrue(self.state.validate_initiative_validation())
        self.state.initiative_validation = {'Player1': True}
        self.assertFalse(self.state.validate_initiative_validation())
        self.state.initiative_validation = {'Player1': 1, 'Player2': True}
        self.assertFalse(self.state.validate_initiative_validation())

    def test_validate_state(self):
        self.assertTrue(self.state.validate_state())
        self.state.players = ['Player1']
        self.assertFalse(self.state.validate_state())
        self.state.players = ['Player1', 'Player2']
        self.state.initiative_rolls = {'Player1': 5}
        self.assertFalse(self.state.validate_state())

if __name__ == '__main__':
    unittest.main() 