"""
Tests for the GameState class.
"""

import pytest
from datetime import datetime
from .game_state import GameState, GameStatus


def test_initial_state():
    """Test the initial state of a new GameState instance."""
    state = GameState()
    
    assert state.player1_name == ""
    assert state.player2_name == ""
    assert state.attacker_id is None
    assert state.first_turn_player_id is None
    assert state.current_round == 1
    assert state.current_player_id is None
    assert state.game_start_time is None
    assert state.last_action_time is None
    assert state.player1_primary == 0
    assert state.player1_secondary == 0
    assert state.player2_primary == 0
    assert state.player2_secondary == 0
    assert state.status == GameStatus.NOT_STARTED


def test_invalid_player_id():
    """Test that invalid player IDs raise ValueError."""
    state = GameState()
    
    with pytest.raises(ValueError, match="attacker_id must be 1 or 2"):
        state.attacker_id = 3
    
    with pytest.raises(ValueError, match="first_turn_player_id must be 1 or 2"):
        state.first_turn_player_id = 3
    
    with pytest.raises(ValueError, match="current_player_id must be 1 or 2"):
        state.current_player_id = 3


def test_invalid_scores():
    """Test that negative scores raise ValueError."""
    state = GameState()
    
    with pytest.raises(ValueError, match="Primary scores cannot be negative"):
        state.player1_primary = -1
    
    with pytest.raises(ValueError, match="Primary scores cannot be negative"):
        state.player2_primary = -1
    
    with pytest.raises(ValueError, match="Secondary scores cannot be negative"):
        state.player1_secondary = -1
    
    with pytest.raises(ValueError, match="Secondary scores cannot be negative"):
        state.player2_secondary = -1


def test_invalid_round():
    """Test that invalid round numbers raise ValueError."""
    state = GameState()
    
    with pytest.raises(ValueError, match="Current round must be at least 1"):
        state.current_round = 0


def test_start_game():
    """Test starting a new game."""
    state = GameState(
        player1_name="Player 1",
        player2_name="Player 2",
        attacker_id=1,
        first_turn_player_id=1
    )
    
    state.start_game()
    
    assert state.status == GameStatus.IN_PROGRESS
    assert state.current_player_id == 1
    assert state.game_start_time is not None
    assert state.last_action_time is not None


def test_start_game_validation():
    """Test that starting a game requires all necessary information."""
    state = GameState()
    
    with pytest.raises(ValueError, match="Both player names must be set"):
        state.start_game()
    
    state.player1_name = "Player 1"
    with pytest.raises(ValueError, match="Both player names must be set"):
        state.start_game()
    
    state.player2_name = "Player 2"
    with pytest.raises(ValueError, match="Attacker must be set"):
        state.start_game()
    
    state.attacker_id = 1
    with pytest.raises(ValueError, match="First turn player must be set"):
        state.start_game()


def test_end_game():
    """Test ending a game."""
    state = GameState(
        player1_name="Player 1",
        player2_name="Player 2",
        attacker_id=1,
        first_turn_player_id=1
    )
    
    state.start_game()
    state.end_game()
    
    assert state.status == GameStatus.GAME_OVER


def test_pause_resume_game():
    """Test pausing and resuming a game."""
    state = GameState(
        player1_name="Player 1",
        player2_name="Player 2",
        attacker_id=1,
        first_turn_player_id=1
    )
    
    state.start_game()
    state.pause_game()
    assert state.status == GameStatus.PAUSED
    
    state.resume_game()
    assert state.status == GameStatus.IN_PROGRESS


def test_update_score():
    """Test updating player scores."""
    state = GameState(
        player1_name="Player 1",
        player2_name="Player 2",
        attacker_id=1,
        first_turn_player_id=1
    )
    
    state.start_game()
    
    state.update_score(1, primary=10)
    assert state.player1_primary == 10
    
    state.update_score(1, secondary=5)
    assert state.player1_secondary == 5
    
    state.update_score(2, primary=8)
    assert state.player2_primary == 8
    
    state.update_score(2, secondary=3)
    assert state.player2_secondary == 3


def test_next_round():
    """Test advancing to the next round."""
    state = GameState(
        player1_name="Player 1",
        player2_name="Player 2",
        attacker_id=1,
        first_turn_player_id=1
    )
    
    state.start_game()
    assert state.current_round == 1
    
    state.next_round()
    assert state.current_round == 2


def test_switch_player():
    """Test switching the current player."""
    state = GameState(
        player1_name="Player 1",
        player2_name="Player 2",
        attacker_id=1,
        first_turn_player_id=1
    )
    
    state.start_game()
    assert state.current_player_id == 1
    
    state.switch_player()
    assert state.current_player_id == 2
    
    state.switch_player()
    assert state.current_player_id == 1


def test_get_current_player_name():
    """Test getting the current player's name."""
    state = GameState(
        player1_name="Player 1",
        player2_name="Player 2",
        attacker_id=1,
        first_turn_player_id=1
    )
    
    state.start_game()
    assert state.get_current_player_name() == "Player 1"
    
    state.switch_player()
    assert state.get_current_player_name() == "Player 2"


def test_get_current_player_score():
    """Test getting the current player's scores."""
    state = GameState(
        player1_name="Player 1",
        player2_name="Player 2",
        attacker_id=1,
        first_turn_player_id=1
    )
    
    state.start_game()
    state.update_score(1, primary=10, secondary=5)
    state.update_score(2, primary=8, secondary=3)
    
    assert state.get_current_player_score() == (10, 5)
    
    state.switch_player()
    assert state.get_current_player_score() == (8, 3)


def test_get_game_duration():
    """Test getting the game duration."""
    state = GameState(
        player1_name="Player 1",
        player2_name="Player 2",
        attacker_id=1,
        first_turn_player_id=1
    )
    
    assert state.get_game_duration() == 0.0
    
    state.start_game()
    duration = state.get_game_duration()
    assert duration >= 0.0
    
    state.end_game()
    assert state.get_game_duration() >= duration 