import pytest
from kivy.app import App
from kivy.tests.common import GraphicUnitTest
from kivy.base import EventLoop
from main import ScorerApp
from pi_app.widgets.number_pad_popup import NumberPadPopup


class InitiativeScreenTests(GraphicUnitTest):
    def setUp(self):
        super().setUp()
        self.app = ScorerApp()
        self.app.root = self.app.build()
        self.advance_frames(1)  # Allow KV rules to be applied
        self.screen = self.app.root.get_screen('initiative')
        self.app.root.current = 'initiative'
        self.render(self.app.root)

    def test_roll_die_ui_feedback(self):
        """Test the roll_die method and its effect on the UI."""
        # Initial state
        assert self.screen.p1_roll_button.disabled is False
        self.screen.roll_die(1)
        self.advance_frames(1)
        # Assert player 1 button is disabled and has a roll value
        assert self.screen.p1_roll_button.disabled is True
        assert self.screen.p1_roll_label.text != ''


class ScoreboardScreenTests(GraphicUnitTest):
    def setUp(self):
        super().setUp()
        self.app = ScorerApp()
        self.app.root = self.app.build()
        self.advance_frames(1)  # Allow KV rules to be applied
        self.screen = self.app.root.get_screen('scoreboard')
        self.app.root.current = 'scoreboard'
        # Manually trigger on_enter to populate the view
        self.screen.on_enter()
        self.render(self.app.root)

    def test_update_view_from_state(self):
        """Test that the UI correctly reflects the game state."""
        self.app.game_state['p1_name'] = "Player One"
        self.app.game_state['p1_primary_score'] = 10
        self.app.game_state['p1_secondary_score'] = 5
        self.app.game_state['p1_cp'] = 3
        
        self.screen.on_enter()
        self.render(self.app.root)

        assert self.screen.p1_name_label.text == "Player One"
        assert self.screen.p1_total_score_label.text == "15"
        assert self.screen.p1_cp_label.text == "3"

    def test_open_score_popup(self):
        """Test that the score popup opens with the correct parameters."""
        self.screen.open_score_popup(1, 'primary')
        self.render(self.app.root)
        # Check that a popup is open.
        assert isinstance(EventLoop.window.children[0], NumberPadPopup)
        # Check that it's the right one
        popup = EventLoop.window.children[0]
        assert popup.title == 'Player 1 Primary Score' 