import unittest
from unittest.mock import Mock
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.tests.common import GraphicUnitTest
from pi_client.screens.game_over_screen import GameOverScreen
from pi_client.state.game_over_state import GameOverState

# Load required KV files with correct relative paths
Builder.load_file('pi_client/widgets/button_styles.kv')
Builder.load_file('pi_client/screens/game_over_screen.kv')

class TestGameOverScreen(GraphicUnitTest):
    def setUp(self):
        super().setUp()
        self.screen = GameOverScreen()
        self.screen.state = GameOverState()
        Clock.schedule_once(lambda dt: None, 0)  # Process any pending events

    def test_initial_state(self):
        """Test initial state of GameOverScreen"""
        self.assertIsNotNone(self.screen.state)
        self.assertEqual(self.screen.p1_name, '')
        self.assertEqual(self.screen.p2_name, '')
        self.assertEqual(self.screen.p1_primary_score, 0)
        self.assertEqual(self.screen.p1_secondary_score, 0)
        self.assertEqual(self.screen.p2_primary_score, 0)
        self.assertEqual(self.screen.p2_secondary_score, 0)
        self.assertEqual(self.screen.game_duration, '00:00')

    def test_initialize_scores(self):
        """Test score initialization"""
        self.screen.initialize_scores()
        self.assertEqual(self.screen.p1_primary_score, 0)
        self.assertEqual(self.screen.p1_secondary_score, 0)
        self.assertEqual(self.screen.p2_primary_score, 0)
        self.assertEqual(self.screen.p2_secondary_score, 0)

    def test_cleanup_game_state(self):
        """Test game state cleanup (mock state manager if needed)"""
        # If cleanup_game_state uses a state manager, inject a mock if possible
        # Otherwise, just call the method to ensure no exceptions
        try:
            self.screen.cleanup_game_state()
        except Exception as e:
            self.fail(f"cleanup_game_state raised an exception: {e}")

    def test_start_new_game(self):
        """Test starting a new game (mock state manager if needed)"""
        try:
            self.screen.start_new_game()
        except Exception as e:
            self.fail(f"start_new_game raised an exception: {e}")

    def test_handle_winner_determination_error(self):
        """Test error handling for winner determination"""
        error_msg = "Test error"
        self.screen.handle_winner_determination_error(error_msg)
        self.assertEqual(self.screen.ids['error_label'].text, error_msg)
        self.assertEqual(self.screen.ids['error_label'].opacity, 1)

    def test_update_ui(self):
        """Test UI update functionality"""
        self.screen.p1_name = "Player 1"
        self.screen.p2_name = "Player 2"
        self.screen.p1_primary_score = 10
        self.screen.p1_secondary_score = 5
        self.screen.p2_primary_score = 8
        self.screen.p2_secondary_score = 3
        self.screen.game_duration = "01:30"
        
        self.screen.update_ui()
        
        self.assertEqual(self.screen.ids['p1_name_label'].text, "Player 1")
        self.assertEqual(self.screen.ids['p2_name_label'].text, "Player 2")
        self.assertEqual(self.screen.ids['p1_final_score_label'].text, "15")
        self.assertEqual(self.screen.ids['p2_final_score_label'].text, "11")
        self.assertEqual(self.screen.ids['total_time_label'].text, "01:30")

if __name__ == '__main__':
    unittest.main() 