import pytest
from kivy.app import App
from kivy.tests.common import GraphicUnitTest
import os
import json
from pi_client.main import ScorerApp

@pytest.fixture
def app(tmpdir):
    """A fixture that creates a ScorerApp instance with a temporary data dir."""
    # Mock the user_data_dir to use a temporary directory
    ScorerApp.user_data_dir = str(tmpdir)
    # Since these are non-graphical tests, we can instantiate the app
    # but we don't need to build it in a graphical way.
    app_instance = ScorerApp()
    return app_instance

def test_initialize_game_state(app):
    """Test that the game state is initialized with default values."""
    app.initialize_game_state()
    state = app.game_state
    assert state['p1_name'] == 'Player 1'
    assert state['p2_name'] == 'Player 2'
    assert state['p1_primary_score'] == 0
    assert state['p2_secondary_score'] == 0
    assert state['current_round'] == 0

def test_save_and_load_game_state(app, tmpdir):
    """Test that game state can be saved to and loaded from a file."""
    # Initialize and modify the state
    app.initialize_game_state()
    app.game_state['p1_name'] = "Tester1"
    app.game_state['p1_primary_score'] = 50

    # Save the state
    app.save_game_state()

    # Create a new app instance to load the state
    new_app = ScorerApp()
    ScorerApp.user_data_dir = str(tmpdir)
    new_app.load_game_state()

    assert new_app.game_state['p1_name'] == "Tester1"
    assert new_app.game_state['p1_primary_score'] == 50

def test_set_player_names(app):
    """Test setting player names."""
    app.initialize_game_state()
    app.set_player_names("Alice", "Bob")
    assert app.game_state['p1_name'] == "Alice"
    assert app.game_state['p2_name'] == "Bob"

    # Test with empty names, should default
    app.set_player_names("", "")
    assert app.game_state['p1_name'] == "Player 1"
    assert app.game_state['p2_name'] == "Player 2"

def test_set_objective_score(app):
    """Test setting objective scores."""
    app.initialize_game_state()
    app.set_objective_score(1, 'primary', 10)
    assert app.game_state['p1_primary_score'] == 10

    app.set_objective_score(2, 'secondary', 5)
    assert app.game_state['p2_secondary_score'] == 5

def test_update_cp(app):
    """Test updating command points."""
    app.initialize_game_state()
    app.game_state['p1_cp'] = 5
    app.update_cp(1, 1)
    assert app.game_state['p1_cp'] == 6

    app.update_cp(1, -2)
    assert app.game_state['p1_cp'] == 4

    # Test that CP cannot go below 0
    app.update_cp(1, -10)
    assert app.game_state['p1_cp'] == 0

class TestEndTurn:
    """Tests for the end_turn logic."""

    @pytest.fixture
    def app_for_turns(self, app):
        """Fixture to set up a game state for turn testing."""
        app.initialize_game_state()
        app.set_player_names("P1", "P2")
        app.game_state['first_turn_player_name'] = "P1"
        app.game_state['current_player_name'] = "P1"
        app.game_state['current_round'] = 1
        return app

    def test_end_turn_p1_starts_p1_ends(self, app_for_turns):
        """Test turn change from P1 to P2 within the same round."""
        app_for_turns.end_turn()
        assert app_for_turns.game_state['current_player_name'] == "P2"
        assert app_for_turns.game_state['current_round'] == 1

    def test_end_turn_p1_starts_p2_ends(self, app_for_turns):
        """Test turn change from P2 to P1, advancing the round."""
        # P1's turn ends
        app_for_turns.end_turn() 
        # P2's turn ends
        app_for_turns.end_turn()
        assert app_for_turns.game_state['current_player_name'] == "P1"
        assert app_for_turns.game_state['current_round'] == 2

    def test_end_turn_p2_starts_p2_ends(self, app_for_turns):
        """Test turn change from P2 to P1 within the same round."""
        app_for_turns.game_state['first_turn_player_name'] = "P2"
        app_for_turns.game_state['current_player_name'] = "P2"
        app_for_turns.end_turn()
        assert app_for_turns.game_state['current_player_name'] == "P1"
        assert app_for_turns.game_state['current_round'] == 1
    
    def test_end_turn_p2_starts_p1_ends(self, app_for_turns):
        """Test turn change from P1 to P2, advancing the round."""
        app_for_turns.game_state['first_turn_player_name'] = "P2"
        app_for_turns.game_state['current_player_name'] = "P2"
        # P2's turn ends
        app_for_turns.end_turn()
        # P1's turn ends
        app_for_turns.end_turn()
        assert app_for_turns.game_state['current_player_name'] == "P2"
        assert app_for_turns.game_state['current_round'] == 2 