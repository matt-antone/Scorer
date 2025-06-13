"""
Unit tests for the database implementation.
"""

import unittest
import tempfile
from pathlib import Path
from src.database.manager import DatabaseManager, DatabaseError


class TestDatabaseManager(unittest.TestCase):
    """Test cases for the DatabaseManager class."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary database file
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"
        self.db_manager = DatabaseManager(self.db_path)

    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()

    def test_create_game_state(self):
        """Test creating a new game state."""
        game_id = "test_game_1"
        initial_state = {
            'status': 'not_started',
            'current_player': 'player1',
            'scores': {'player1': 0, 'player2': 0},
            'timer': {'player1': 300, 'player2': 300},
            'settings': {'time_limit': 300}
        }

        # Create game state
        self.db_manager.create_game_state(game_id, initial_state)

        # Verify game state
        state = self.db_manager.get_game_state(game_id)
        self.assertIsNotNone(state)
        self.assertEqual(state['game_id'], game_id)
        self.assertEqual(state['status'], initial_state['status'])
        self.assertEqual(state['current_player'], initial_state['current_player'])
        self.assertEqual(state['scores'], initial_state['scores'])
        self.assertEqual(state['timer'], initial_state['timer'])
        self.assertEqual(state['settings'], initial_state['settings'])

    def test_update_game_state(self):
        """Test updating a game state."""
        game_id = "test_game_2"
        initial_state = {
            'status': 'not_started',
            'current_player': 'player1',
            'scores': {'player1': 0, 'player2': 0},
            'timer': {'player1': 300, 'player2': 300},
            'settings': {'time_limit': 300}
        }

        # Create initial state
        self.db_manager.create_game_state(game_id, initial_state)

        # Update state
        updates = {
            'status': 'in_progress',
            'scores': {'player1': 10, 'player2': 5}
        }
        self.db_manager.update_game_state(game_id, updates)

        # Verify updates
        state = self.db_manager.get_game_state(game_id)
        self.assertEqual(state['status'], updates['status'])
        self.assertEqual(state['scores'], updates['scores'])
        self.assertEqual(state['current_player'], initial_state['current_player'])
        self.assertEqual(state['timer'], initial_state['timer'])
        self.assertEqual(state['settings'], initial_state['settings'])

    def test_delete_game_state(self):
        """Test deleting a game state."""
        game_id = "test_game_3"
        initial_state = {
            'status': 'not_started',
            'current_player': 'player1',
            'scores': {'player1': 0, 'player2': 0},
            'timer': {'player1': 300, 'player2': 300},
            'settings': {'time_limit': 300}
        }

        # Create game state
        self.db_manager.create_game_state(game_id, initial_state)

        # Verify state exists
        state = self.db_manager.get_game_state(game_id)
        self.assertIsNotNone(state)

        # Delete state
        self.db_manager.delete_game_state(game_id)

        # Verify state is deleted
        state = self.db_manager.get_game_state(game_id)
        self.assertIsNone(state)

    def test_get_active_games(self):
        """Test getting active games."""
        # Create multiple game states
        games = [
            ("game1", {'status': 'not_started'}),
            ("game2", {'status': 'in_progress'}),
            ("game3", {'status': 'completed'})
        ]

        for game_id, state in games:
            self.db_manager.create_game_state(game_id, state)

        # Get active games
        active_games = self.db_manager.get_active_games()

        # Verify results
        self.assertEqual(len(active_games), 2)
        game_ids = {game['game_id'] for game in active_games}
        self.assertEqual(game_ids, {'game1', 'game2'})

    def test_invalid_game_id(self):
        """Test operations with invalid game ID."""
        game_id = "nonexistent_game"

        # Test get_game_state
        state = self.db_manager.get_game_state(game_id)
        self.assertIsNone(state)

        # Test update_game_state
        with self.assertRaises(DatabaseError):
            self.db_manager.update_game_state(game_id, {'status': 'in_progress'})

        # Test delete_game_state
        self.db_manager.delete_game_state(game_id)  # Should not raise an error


if __name__ == '__main__':
    unittest.main() 