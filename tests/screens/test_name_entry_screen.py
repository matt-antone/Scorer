import unittest
from pi_client.state.name_entry_state import NameEntryState

class TestNameEntryState(unittest.TestCase):
    """Test cases for NameEntryState (pure logic, no Kivy)."""

    def setUp(self):
        self.state = NameEntryState(
            players=['Alice', 'Bob'],
            player_validation={'Alice': True, 'Bob': True}
        )

    def test_validate_players(self):
        self.assertTrue(self.state.validate_players())
        self.state.players = ['Alice']
        self.assertFalse(self.state.validate_players())
        self.state.players = ['Alice', '']
        self.assertFalse(self.state.validate_players())
        self.state.players = ['Alice', 'Alice']
        self.assertFalse(self.state.validate_players())

    def test_validate_player_validation(self):
        self.assertTrue(self.state.validate_player_validation())
        self.state.player_validation = {'Alice': True}
        self.assertFalse(self.state.validate_player_validation())
        self.state.player_validation = {'Alice': 1, 'Bob': True}
        self.assertFalse(self.state.validate_player_validation())

    def test_validate_state(self):
        self.assertTrue(self.state.validate_state())
        self.state.players = ['Alice']
        self.assertFalse(self.state.validate_state())
        self.state.players = ['Alice', 'Bob']
        self.state.player_validation = {'Alice': True}
        self.assertFalse(self.state.validate_state())

if __name__ == '__main__':
    unittest.main() 