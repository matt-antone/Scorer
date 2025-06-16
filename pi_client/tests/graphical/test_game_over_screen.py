"""
Tests for the Game Over Screen.
"""
from .test_base import BaseScreenTest

class TestGameOverScreen(BaseScreenTest):
    """Tests for the Game Over Screen."""
    
    def setUp(self):
        """Set up the test environment."""
        super().setUp()
        self.screen = self.get_screen('game_over')
        # Set up game state
        self.app.game_state.update({
            'p1_name': 'Player 1',
            'p2_name': 'Player 2',
            'p1_primary_score': 10,
            'p2_primary_score': 8,
            'p1_secondary_score': 5,
            'p2_secondary_score': 3,
            'p1_cp': 3,
            'p2_cp': 1,
            'winner': 'Player 1',
            'winner_name': 'Player 1',
            'winner_score': 15,
            'loser_name': 'Player 2',
            'loser_score': 11,
            'victory_type': 'Victory',
            'game_duration': '00:30'
        })
        self.screen.on_enter()
        self.advance_frames(1)
    
    def test_initial_state(self):
        """Test the initial state of the screen."""
        # Check that all required widgets exist
        self.assert_widget_exists(self.screen, 'winner_label')
        self.assert_widget_exists(self.screen, 'p1_name_label')
        self.assert_widget_exists(self.screen, 'p2_name_label')
        self.assert_widget_exists(self.screen, 'p1_final_score_label')
        self.assert_widget_exists(self.screen, 'p2_final_score_label')
        self.assert_widget_exists(self.screen, 'total_time_label')
        self.assert_widget_exists(self.screen, 'error_label')
        self.assert_widget_exists(self.screen, 'new_game_button')
        self.assert_widget_exists(self.screen, 'exit_button')
        
        # Check initial label states
        self.assert_widget_text(self.screen, 'winner_label', 'Player 1 Wins!')
        self.assert_widget_text(self.screen, 'p1_name_label', 'Player 1')
        self.assert_widget_text(self.screen, 'p2_name_label', 'Player 2')
        self.assert_widget_text(self.screen, 'p1_final_score_label', '15')
        self.assert_widget_text(self.screen, 'p2_final_score_label', '11')
        self.assert_widget_text(self.screen, 'total_time_label', '00:30')
        
        # Check button states
        self.assert_widget_disabled(self.screen, 'new_game_button', False)
        self.assert_widget_disabled(self.screen, 'exit_button', False)
        
        # Check error label
        self.assert_widget_opacity(self.screen, 'error_label', 0)
    
    def test_tie_game(self):
        """Test the screen state when game is tied."""
        # Update game state for tie
        self.app.game_state.update({
            'p1_primary_score': 10,
            'p2_primary_score': 10,
            'p1_secondary_score': 5,
            'p2_secondary_score': 5,
            'winner': 'Tie',
            'winner_name': 'Tie',
            'winner_score': 15,
            'loser_name': 'Tie',
            'loser_score': 15,
            'victory_type': 'Draw'
        })
        self.screen.on_enter()
        self.advance_frames(1)
        
        # Check winner label
        self.assert_widget_text(self.screen, 'winner_label', 'Game Ended in a Tie!')
        
        # Check scores
        self.assert_widget_text(self.screen, 'p1_final_score_label', '15')
        self.assert_widget_text(self.screen, 'p2_final_score_label', '15')
    
    def test_new_game_button(self):
        """Test the new game button functionality."""
        # Click new game button
        self.screen.new_game_button.trigger_action()
        self.advance_frames(1)
        
        # Check that we moved to the name entry screen
        assert self.app.root.current == 'name_entry'
        
        # Check that game state was reset
        assert self.app.game_state['p1_name'] == ''
        assert self.app.game_state['p2_name'] == ''
        assert self.app.game_state['p1_primary_score'] == 0
        assert self.app.game_state['p2_primary_score'] == 0
        assert self.app.game_state['p1_secondary_score'] == 0
        assert self.app.game_state['p2_secondary_score'] == 0
        assert self.app.game_state['p1_cp'] == 0
        assert self.app.game_state['p2_cp'] == 0
        assert self.app.game_state['winner'] == ''
        assert self.app.game_state['winner_name'] == ''
        assert self.app.game_state['winner_score'] == 0
        assert self.app.game_state['loser_name'] == ''
        assert self.app.game_state['loser_score'] == 0
        assert self.app.game_state['victory_type'] == ''
    
    def test_error_handling(self):
        """Test error handling in the screen."""
        # Simulate an error
        self.screen.handle_winner_determination_error("Test error")
        self.advance_frames(1)
        
        # Check error label
        self.assert_widget_text(self.screen, 'error_label', 'Test error')
        self.assert_widget_opacity(self.screen, 'error_label', 1)
        
        # Check that buttons are still enabled
        self.assert_widget_disabled(self.screen, 'new_game_button', False)
        self.assert_widget_disabled(self.screen, 'exit_button', False)
    
    def test_state_update(self):
        """Test handling of state updates."""
        # Update game state
        self.app.game_state.update({
            'p1_primary_score': 12,
            'p2_primary_score': 10,
            'p1_secondary_score': 6,
            'p2_secondary_score': 4,
            'winner': 'Player 1',
            'winner_name': 'Player 1',
            'winner_score': 18,
            'loser_name': 'Player 2',
            'loser_score': 14,
            'victory_type': 'Victory',
            'game_duration': '01:00'
        })
        
        # Trigger state update
        self.screen.on_state_update(self.app.game_state)
        self.advance_frames(1)
        
        # Check updated values
        self.assert_widget_text(self.screen, 'p1_final_score_label', '18')
        self.assert_widget_text(self.screen, 'p2_final_score_label', '14')
        self.assert_widget_text(self.screen, 'total_time_label', '01:00')
        self.assert_widget_text(self.screen, 'winner_label', 'Player 1 Wins!') 