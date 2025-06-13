import unittest
from kivy.tests.common import GraphicUnitTest
from kivy.app import App
from kivy.clock import Clock
from pi_client.screens.game_over_screen import GameOverScreen
from pi_client.screens.base_screen import ValidationError, StateError
from pi_client.tests.graphical.test_base import BaseScreenTest
import pytest
from kivy.uix.screenmanager import ScreenManager, Screen

class TestApp(App):
    """Test application with game state."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_state = {
            'players': [],
            'scores': {},
            'winner': None,
            'game_history': [],
            'cleanup_required': False,
            'save_game': False
        }

    def build(self):
        return ScreenManager()

class TestGameOverScreen:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.app = TestApp()
        self.app.root = self.app.build()  # Ensure root is set
        # Add required screens for transitions
        self.app.root.add_widget(Screen(name='name_entry'))
        self.app.root.add_widget(Screen(name='resume_or_new'))
        self.screen = GameOverScreen(name='game_over')
        self.app.root.add_widget(self.screen)
        yield
        self.app.stop()

    def test_initial_state(self):
        """Test initial state of GameOverScreen."""
        assert not self.screen.is_loading
        assert not self.screen.is_syncing
        assert not self.screen.has_error
        assert self.screen.winner == ''
        assert len(self.screen.final_scores) == 0
        assert not self.screen.show_winner
        assert not self.screen.show_scores

    def test_load_game_state(self):
        """Test loading game state."""
        # Set up test data
        test_data = {
            'winner': 'Player1',
            'scores': {'Player1': 10, 'Player2': 5}
        }
        self.app.game_state = test_data

        # Load state
        self.screen.load_game_state()
        
        # Verify state
        assert self.screen.winner == 'Player1'
        assert len(self.screen.final_scores) == 2
        assert self.screen.show_winner
        assert self.screen.show_scores

    def test_error_handling(self):
        """Test error handling."""
        # Test invalid state
        self.app.game_state = None
        self.screen.load_game_state()
        assert self.screen.has_error

        # Test invalid scores
        self.screen.update_scores({'Player1': -1})
        assert self.screen.has_error

    def test_state_validation(self):
        """Test state validation."""
        # Test valid state
        valid_state = {
            'winner': 'Player1',
            'scores': {'Player1': 10, 'Player2': 5}
        }
        assert self.screen.validate_state(valid_state)

        # Test invalid state
        invalid_state = {
            'winner': None,
            'scores': {}
        }
        assert not self.screen.validate_state(invalid_state)

    def test_reset(self):
        """Test reset functionality."""
        # Set up initial state
        self.screen.winner = 'Player1'
        self.screen.final_scores = [{'name': 'Player1', 'score': 10}]
        self.screen.show_winner = True
        self.screen.show_scores = True
        self.screen.has_error = True

        # Reset
        self.screen.reset()

        # Verify reset
        assert self.screen.winner == ''
        assert len(self.screen.final_scores) == 0
        assert not self.screen.show_winner
        assert not self.screen.show_scores
        assert not self.screen.has_error

    def test_final_score_display(self):
        """Test final score display functionality."""
        # Test score initialization
        self.screen.initialize_scores()
        assert len(self.screen.final_scores) == 0

        # Test score update
        self.screen.update_scores({'Player1': 10, 'Player2': 5})
        assert len(self.screen.final_scores) == 2
        assert self.screen.final_scores[0]['name'] == 'Player1'
        assert self.screen.final_scores[0]['score'] == 10
        assert self.screen.final_scores[1]['name'] == 'Player2'
        assert self.screen.final_scores[1]['score'] == 5

    def test_winner_determination(self):
        """Test winner determination functionality."""
        # Test winner calculation
        self.screen.update_scores({'Player1': 10, 'Player2': 5})
        self.screen.determine_winner()
        assert self.screen.winner == 'Player1'

        # Test tie handling
        self.screen.update_scores({'Player1': 10, 'Player2': 10})
        self.screen.determine_winner()
        assert self.screen.winner == 'Tie'

    def test_client_synchronization(self):
        """Test client synchronization functionality."""
        # Test start sync
        self.screen.start_sync()
        assert self.screen.is_syncing

        # Test stop sync
        self.screen.stop_sync()
        assert not self.screen.is_syncing

        # Test client update
        update = {
            'type': 'scores',
            'scores': {'Player1': 10, 'Player2': 5}
        }
        self.screen.handle_client_update(update)
        assert len(self.screen.final_scores) == 2

        # Test invalid update
        with pytest.raises(ValidationError):
            self.screen.handle_client_update({'type': 'invalid'})

    def test_screen_transitions(self):
        """Test screen transitions."""
        # Test transition to new game
        self.screen.start_new_game()
        assert self.app.root.current == 'name_entry'

        # Test transition to main menu
        self.screen.return_to_menu()
        assert self.app.root.current == 'resume_or_new'

# ... existing code ... 