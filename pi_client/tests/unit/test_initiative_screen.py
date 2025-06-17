import unittest
from unittest.mock import Mock, patch
from pi_client.state.initiative_state import InitiativeState

class TestInitiativeState(unittest.TestCase):
    """State-only tests for initiative logic and validation."""
    
    def setUp(self):
        self.state = InitiativeState()
        self.state.players = ['Player1', 'Player2']
        self.state.rolls = {'Player1': None, 'Player2': None}
        self.state.roll_validation = {'min_value': 1, 'max_value': 6}
        self.state.current_round = 1

    def test_initial_state(self):
        """Test initial state properties."""
        self.assertEqual(self.state.players, ['Player1', 'Player2'])
        self.assertEqual(self.state.rolls, {'Player1': None, 'Player2': None})
        self.assertEqual(self.state.current_round, 1)
        self.assertIsNone(self.state.initiative_winner)
        self.assertIsNone(self.state.initiative_loser)

    def test_validate_roll(self):
        """Test roll validation logic."""
        # Valid rolls
        self.assertTrue(self.state.validate_roll(3))
        self.assertTrue(self.state.validate_roll(1))
        self.assertTrue(self.state.validate_roll(6))
        
        # Invalid rolls
        self.assertFalse(self.state.validate_roll(0))
        self.assertFalse(self.state.validate_roll(7))
        self.assertFalse(self.state.validate_roll('a'))
        self.assertFalse(self.state.validate_roll(None))

    def test_add_roll(self):
        """Test adding rolls to state."""
        # Add valid roll
        self.assertTrue(self.state.add_roll('Player1', 5))
        self.assertEqual(self.state.rolls['Player1'], 5)
        
        # Add invalid roll
        self.assertFalse(self.state.add_roll('Player2', 10))
        self.assertIsNone(self.state.rolls['Player2'])

    def test_determine_initiative(self):
        """Test initiative determination logic."""
        # Player1 wins
        self.state.rolls = {'Player1': 5, 'Player2': 3}
        winner, loser = self.state.determine_initiative()
        self.assertEqual(winner, 'Player1')
        self.assertEqual(loser, 'Player2')
        
        # Player2 wins
        self.state.rolls = {'Player1': 2, 'Player2': 6}
        winner, loser = self.state.determine_initiative()
        self.assertEqual(winner, 'Player2')
        self.assertEqual(loser, 'Player1')
        
        # Tie
        self.state.rolls = {'Player1': 4, 'Player2': 4}
        winner, loser = self.state.determine_initiative()
        self.assertIsNone(winner)
        self.assertIsNone(loser)

    def test_handle_tie(self):
        """Test tie handling logic."""
        self.state.rolls = {'Player1': 4, 'Player2': 4}
        tied_players = self.state.get_tied_players()
        self.assertEqual(set(tied_players), {'Player1', 'Player2'})
        
        # Reset tied players
        self.state.reset_tied_players(tied_players)
        self.assertIsNone(self.state.rolls['Player1'])
        self.assertIsNone(self.state.rolls['Player2'])

    def test_state_validation(self):
        """Test state validation."""
        # Valid state
        self.assertTrue(self.state.validate_state())
        
        # Invalid state - missing players
        self.state.players = []
        self.assertFalse(self.state.validate_state())
        
        # Invalid state - invalid rolls
        self.state.players = ['Player1', 'Player2']
        self.state.rolls = {'Player1': 'invalid', 'Player2': None}
        self.assertFalse(self.state.validate_state())

    def test_get_state_dict(self):
        """Test state serialization."""
        state_dict = self.state.get_state_dict()
        expected_keys = ['players', 'rolls', 'roll_validation', 'current_round', 
                        'initiative_winner', 'initiative_loser']
        for key in expected_keys:
            self.assertIn(key, state_dict)

    def test_update_from_dict(self):
        """Test state deserialization."""
        new_state = {
            'players': ['Alice', 'Bob'],
            'rolls': {'Alice': 5, 'Bob': 3},
            'current_round': 2
        }
        self.state.update_from_dict(new_state)
        self.assertEqual(self.state.players, ['Alice', 'Bob'])
        self.assertEqual(self.state.rolls, {'Alice': 5, 'Bob': 3})
        self.assertEqual(self.state.current_round, 2)

if __name__ == '__main__':
    unittest.main() 