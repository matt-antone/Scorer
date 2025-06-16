import unittest
from datetime import datetime, timedelta
from pi_client.state.game_over_state import GameOverState

class TestGameOverState(unittest.TestCase):
    def setUp(self):
        self.state = GameOverState()
        self.state.p1_name = 'Player 1'
        self.state.p2_name = 'Player 2'

    def test_initial_state(self):
        """Test initial state values"""
        self.assertEqual(self.state.p1_name, 'Player 1')
        self.assertEqual(self.state.p2_name, 'Player 2')
        self.assertEqual(self.state.p1_primary_score, 0)
        self.assertEqual(self.state.p1_secondary_score, 0)
        self.assertEqual(self.state.p2_primary_score, 0)
        self.assertEqual(self.state.p2_secondary_score, 0)
        self.assertEqual(self.state.game_duration, '00:00')
        self.assertIsNone(self.state.error_message)
        self.assertIsNone(self.state.start_time)
        self.assertEqual(self.state.winner, '')
        self.assertEqual(self.state.winner_name, '')
        self.assertEqual(self.state.winner_score, 0)
        self.assertEqual(self.state.loser_name, '')
        self.assertEqual(self.state.loser_score, 0)
        self.assertEqual(self.state.victory_type, '')
        self.assertEqual(self.state.scores, {})
        self.assertEqual(self.state.final_scores, [])
        self.assertEqual(self.state.game_history, [])
        self.assertFalse(self.state.cleanup_required)
        self.assertFalse(self.state.save_game)

    def test_initialize_scores(self):
        """Test score initialization"""
        self.state.p1_primary_score = 10
        self.state.p1_secondary_score = 5
        self.state.p2_primary_score = 8
        self.state.p2_secondary_score = 3
        self.state.winner_score = 15
        self.state.loser_score = 11
        self.state.scores = {'Player 1': 15, 'Player 2': 11}
        self.state.final_scores = [{'name': 'Player 1', 'score': 15}, {'name': 'Player 2', 'score': 11}]
        
        self.state.initialize_scores()
        
        self.assertEqual(self.state.p1_primary_score, 0)
        self.assertEqual(self.state.p1_secondary_score, 0)
        self.assertEqual(self.state.p2_primary_score, 0)
        self.assertEqual(self.state.p2_secondary_score, 0)
        self.assertEqual(self.state.winner_score, 0)
        self.assertEqual(self.state.loser_score, 0)
        self.assertEqual(self.state.scores, {})
        self.assertEqual(self.state.final_scores, [])

    def test_get_total_scores(self):
        """Test total score calculations"""
        self.state.p1_primary_score = 10
        self.state.p1_secondary_score = 5
        self.state.p2_primary_score = 8
        self.state.p2_secondary_score = 3
        
        self.assertEqual(self.state.get_p1_total_score(), 15)
        self.assertEqual(self.state.get_p2_total_score(), 11)

    def test_determine_winner_p1_wins(self):
        """Test winner determination when player 1 wins"""
        self.state.p1_primary_score = 10
        self.state.p1_secondary_score = 5
        self.state.p2_primary_score = 8
        self.state.p2_secondary_score = 3
        
        winner = self.state.determine_winner()
        
        self.assertEqual(winner, 'Player 1')
        self.assertEqual(self.state.winner, 'Player 1')
        self.assertEqual(self.state.winner_name, 'Player 1')
        self.assertEqual(self.state.winner_score, 15)
        self.assertEqual(self.state.loser_name, 'Player 2')
        self.assertEqual(self.state.loser_score, 11)
        self.assertEqual(self.state.victory_type, 'Victory')
        self.assertEqual(self.state.scores, {'Player 1': 15, 'Player 2': 11})

    def test_determine_winner_p2_wins(self):
        """Test winner determination when player 2 wins"""
        self.state.p1_primary_score = 8
        self.state.p1_secondary_score = 3
        self.state.p2_primary_score = 10
        self.state.p2_secondary_score = 5
        
        winner = self.state.determine_winner()
        
        self.assertEqual(winner, 'Player 2')
        self.assertEqual(self.state.winner, 'Player 2')
        self.assertEqual(self.state.winner_name, 'Player 2')
        self.assertEqual(self.state.winner_score, 15)
        self.assertEqual(self.state.loser_name, 'Player 1')
        self.assertEqual(self.state.loser_score, 11)
        self.assertEqual(self.state.victory_type, 'Victory')
        self.assertEqual(self.state.scores, {'Player 1': 11, 'Player 2': 15})

    def test_determine_winner_tie(self):
        """Test winner determination when game is tied"""
        self.state.p1_primary_score = 10
        self.state.p1_secondary_score = 5
        self.state.p2_primary_score = 10
        self.state.p2_secondary_score = 5
        
        winner = self.state.determine_winner()
        
        self.assertEqual(winner, 'Tie')
        self.assertEqual(self.state.winner, 'Tie')
        self.assertEqual(self.state.winner_name, 'Tie')
        self.assertEqual(self.state.winner_score, 15)
        self.assertEqual(self.state.loser_name, 'Tie')
        self.assertEqual(self.state.loser_score, 15)
        self.assertEqual(self.state.victory_type, 'Draw')
        self.assertEqual(self.state.scores, {'Player 1': 15, 'Player 2': 15})

    def test_add_to_game_history(self):
        """Test adding game state to history"""
        self.state.p1_primary_score = 10
        self.state.p1_secondary_score = 5
        self.state.p2_primary_score = 8
        self.state.p2_secondary_score = 3
        self.state.determine_winner()
        self.state.save_game = True
        
        self.state.add_to_game_history()
        
        self.assertEqual(len(self.state.game_history), 1)
        history_entry = self.state.game_history[0]
        self.assertEqual(history_entry['winner'], 'Player 1')
        self.assertEqual(history_entry['winner_name'], 'Player 1')
        self.assertEqual(history_entry['winner_score'], 15)
        self.assertEqual(history_entry['loser_name'], 'Player 2')
        self.assertEqual(history_entry['loser_score'], 11)
        self.assertEqual(history_entry['victory_type'], 'Victory')
        self.assertEqual(history_entry['scores'], {'Player 1': 15, 'Player 2': 11})
        self.assertEqual(history_entry['duration'], '00:00')
        self.assertIn('timestamp', history_entry)

    def test_reset(self):
        """Test resetting all state values"""
        self.state.p1_name = 'Player 1'
        self.state.p2_name = 'Player 2'
        self.state.p1_primary_score = 10
        self.state.p1_secondary_score = 5
        self.state.p2_primary_score = 8
        self.state.p2_secondary_score = 3
        self.state.determine_winner()
        self.state.save_game = True
        self.state.cleanup_required = True
        
        self.state.reset()
        
        self.assertEqual(self.state.p1_name, '')
        self.assertEqual(self.state.p2_name, '')
        self.assertEqual(self.state.p1_primary_score, 0)
        self.assertEqual(self.state.p1_secondary_score, 0)
        self.assertEqual(self.state.p2_primary_score, 0)
        self.assertEqual(self.state.p2_secondary_score, 0)
        self.assertEqual(self.state.game_duration, '00:00')
        self.assertIsNone(self.state.error_message)
        self.assertIsNone(self.state.start_time)
        self.assertEqual(self.state.winner, '')
        self.assertEqual(self.state.winner_name, '')
        self.assertEqual(self.state.winner_score, 0)
        self.assertEqual(self.state.loser_name, '')
        self.assertEqual(self.state.loser_score, 0)
        self.assertEqual(self.state.victory_type, '')
        self.assertEqual(self.state.scores, {})
        self.assertEqual(self.state.final_scores, [])
        self.assertFalse(self.state.cleanup_required)
        self.assertFalse(self.state.save_game)

    def test_error_handling(self):
        """Test error message handling"""
        error_msg = "Test error"
        self.state.set_error(error_msg)
        self.assertEqual(self.state.error_message, error_msg)
        
        self.state.clear_error()
        self.assertIsNone(self.state.error_message)

    def test_game_duration(self):
        """Test game duration calculation"""
        self.state.start_time = datetime.now() - timedelta(minutes=1, seconds=30)
        self.state.update_game_duration()
        self.assertEqual(self.state.game_duration, "01:30")

    def test_state_serialization(self):
        """Test state serialization to and from dictionary"""
        self.state.p1_name = "Player 1"
        self.state.p2_name = "Player 2"
        self.state.p1_primary_score = 10
        self.state.p1_secondary_score = 5
        self.state.p2_primary_score = 8
        self.state.p2_secondary_score = 3
        self.state.game_duration = "01:30"
        self.state.error_message = "Test error"
        
        state_dict = self.state.to_dict()
        new_state = GameOverState.from_dict(state_dict)
        
        self.assertEqual(new_state.p1_name, "Player 1")
        self.assertEqual(new_state.p2_name, "Player 2")
        self.assertEqual(new_state.p1_primary_score, 10)
        self.assertEqual(new_state.p1_secondary_score, 5)
        self.assertEqual(new_state.p2_primary_score, 8)
        self.assertEqual(new_state.p2_secondary_score, 3)
        self.assertEqual(new_state.game_duration, "01:30")
        self.assertEqual(new_state.error_message, "Test error")

if __name__ == '__main__':
    unittest.main() 