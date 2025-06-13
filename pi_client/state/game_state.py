"""
GameState class for managing the application's state.

This module provides a centralized state management system for the Scorer application.
It handles game state, screen transitions, and data persistence.
"""

from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import wraps
import logging


class GameStatus(Enum):
    """Enum for tracking the current game status."""
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    PAUSED = auto()
    GAME_OVER = auto()


# --- Validation Decorators ---

def validate_player_id(setter):
    """
    Decorator for player ID validation.
    Ensures the value is None, 1, or 2.
    Raises ValueError if invalid.
    """
    @wraps(setter)
    def wrapper(self, value):
        if value is not None and value not in (1, 2):
            raise ValueError(f"{setter.__name__} must be 1 or 2")
        return setter(self, value)
    return wrapper


def non_negative(msg=None):
    """
    Decorator for non-negative integer validation.
    Ensures the value is >= 0.
    Accepts a custom error message for test compatibility.
    Raises ValueError if invalid.
    """
    def decorator(setter):
        @wraps(setter)
        def wrapper(self, value):
            if value < 0:
                raise ValueError(msg or f"{setter.__name__} cannot be negative")
            return setter(self, value)
        return wrapper
    return decorator


def validate_round(setter):
    """
    Decorator for round number validation.
    Ensures the value is between 1 and 5.
    Raises ValueError if invalid.
    """
    @wraps(setter)
    def wrapper(self, value):
        if value < 1 or value > 5:
            raise ValueError("Current round must be between 1 and 5")
        return setter(self, value)
    return wrapper


@dataclass
class GameState:
    """
    Centralized state management for the Scorer application.
    
    This class manages all game state, including:
    - Player information
    - Game progress
    - Scores
    - Game status
    """
    
    # Game Setup
    _player1_name: str = field(default="")
    _player2_name: str = field(default="")
    _attacker_id: Optional[int] = field(default=None)
    _first_turn_player_id: Optional[int] = field(default=None)
    
    # Game Progress
    _current_round: int = field(default=1)
    _current_player_id: Optional[int] = field(default=None)
    _game_start_time: Optional[datetime] = field(default=None)
    _last_action_time: Optional[datetime] = field(default=None)
    
    # Scores
    _player1_primary: int = field(default=0)
    _player1_secondary: int = field(default=0)
    _player2_primary: int = field(default=0)
    _player2_secondary: int = field(default=0)
    
    # Game Status
    _status: GameStatus = field(default=GameStatus.NOT_STARTED)
    
    @property
    def player1_name(self) -> str:
        return self._player1_name
    
    @player1_name.setter
    def player1_name(self, value: str) -> None:
        self._player1_name = value
    
    @property
    def player2_name(self) -> str:
        return self._player2_name
    
    @player2_name.setter
    def player2_name(self, value: str) -> None:
        self._player2_name = value
    
    @property
    def attacker_id(self) -> Optional[int]:
        return self._attacker_id
    
    @attacker_id.setter
    @validate_player_id
    def attacker_id(self, value: Optional[int]) -> None:
        self._attacker_id = value
    
    @property
    def first_turn_player_id(self) -> Optional[int]:
        return self._first_turn_player_id
    
    @first_turn_player_id.setter
    @validate_player_id
    def first_turn_player_id(self, value: Optional[int]) -> None:
        self._first_turn_player_id = value
    
    @property
    def current_player_id(self) -> Optional[int]:
        return self._current_player_id
    
    @current_player_id.setter
    @validate_player_id
    def current_player_id(self, value: Optional[int]) -> None:
        self._current_player_id = value
    
    @property
    def game_start_time(self) -> Optional[datetime]:
        return self._game_start_time
    
    @game_start_time.setter
    def game_start_time(self, value: Optional[datetime]) -> None:
        self._game_start_time = value
    
    @property
    def last_action_time(self) -> Optional[datetime]:
        return self._last_action_time
    
    @last_action_time.setter
    def last_action_time(self, value: Optional[datetime]) -> None:
        self._last_action_time = value
    
    @property
    def player1_primary(self) -> int:
        return self._player1_primary
    
    @player1_primary.setter
    @non_negative("Primary scores cannot be negative")
    def player1_primary(self, value: int) -> None:
        self._player1_primary = value
    
    @property
    def player1_secondary(self) -> int:
        return self._player1_secondary
    
    @player1_secondary.setter
    @non_negative("Secondary scores cannot be negative")
    def player1_secondary(self, value: int) -> None:
        self._player1_secondary = value
    
    @property
    def player2_primary(self) -> int:
        return self._player2_primary
    
    @player2_primary.setter
    @non_negative("Primary scores cannot be negative")
    def player2_primary(self, value: int) -> None:
        self._player2_primary = value
    
    @property
    def player2_secondary(self) -> int:
        return self._player2_secondary
    
    @player2_secondary.setter
    @non_negative("Secondary scores cannot be negative")
    def player2_secondary(self, value: int) -> None:
        self._player2_secondary = value
    
    @property
    def status(self) -> GameStatus:
        return self._status
    
    @status.setter
    def status(self, value: GameStatus) -> None:
        self._status = value
    
    @property
    def current_round(self) -> int:
        return self._current_round
    
    @current_round.setter
    @validate_round
    def current_round(self, value: int) -> None:
        self._current_round = value
    
    def __post_init__(self):
        """Validate initial state after initialization."""
        self._validate_state()
    
    def _validate_state(self) -> None:
        """Validate the current state."""
        # Validate player IDs
        if self._attacker_id is not None and self._attacker_id not in (1, 2):
            raise ValueError("attacker_id must be 1 or 2")
        
        if self._first_turn_player_id is not None and self._first_turn_player_id not in (1, 2):
            raise ValueError("first_turn_player_id must be 1 or 2")
        
        if self._current_player_id is not None and self._current_player_id not in (1, 2):
            raise ValueError("current_player_id must be 1 or 2")
        
        # Validate scores
        if self._player1_primary < 0 or self._player2_primary < 0:
            raise ValueError("Primary scores cannot be negative")
        
        if self._player1_secondary < 0 or self._player2_secondary < 0:
            raise ValueError("Secondary scores cannot be negative")
        
        # Validate round
        if self._current_round < 1 or self._current_round > 5:
            raise ValueError("Current round must be between 1 and 5")
    
    def start_game(self) -> None:
        """Start a new game."""
        if self._status != GameStatus.NOT_STARTED:
            raise ValueError("Game can only be started when not started")
        
        if not self._player1_name or not self._player2_name:
            raise ValueError("Both player names must be set")
        
        if self._attacker_id is None:
            raise ValueError("Attacker must be set")
        
        if self._first_turn_player_id is None:
            raise ValueError("First turn player must be set")
        
        self._status = GameStatus.IN_PROGRESS
        self._current_player_id = self._first_turn_player_id
        self._game_start_time = datetime.now()
        self._last_action_time = self._game_start_time
        self._validate_state()
    
    def end_game(self) -> None:
        """End the current game."""
        if self._status not in (GameStatus.IN_PROGRESS, GameStatus.PAUSED):
            raise ValueError("Game can only be ended when in progress or paused")
        
        self._status = GameStatus.GAME_OVER
        self._last_action_time = datetime.now()
        self._validate_state()
    
    def pause_game(self) -> None:
        """Pause the current game."""
        if self._status != GameStatus.IN_PROGRESS:
            raise ValueError("Game can only be paused when in progress")
        
        self._status = GameStatus.PAUSED
        self._last_action_time = datetime.now()
        self._validate_state()
    
    def resume_game(self) -> None:
        """Resume a paused game."""
        if self._status != GameStatus.PAUSED:
            raise ValueError("Game can only be resumed when paused")
        
        self._status = GameStatus.IN_PROGRESS
        self._last_action_time = datetime.now()
        self._validate_state()
    
    def update_score(self, player_id: int, primary: Optional[int] = None, secondary: Optional[int] = None) -> None:
        """Update a player's score."""
        if self._status not in (GameStatus.IN_PROGRESS, GameStatus.PAUSED):
            raise ValueError("Scores can only be updated when game is in progress or paused")
        
        if player_id not in (1, 2):
            raise ValueError("player_id must be 1 or 2")
        
        if primary is not None:
            if primary < 0:
                raise ValueError("Primary score cannot be negative")
            if player_id == 1:
                self._player1_primary = primary
            else:
                self._player2_primary = primary
        
        if secondary is not None:
            if secondary < 0:
                raise ValueError("Secondary score cannot be negative")
            if player_id == 1:
                self._player1_secondary = secondary
            else:
                self._player2_secondary = secondary
        
        self._last_action_time = datetime.now()
        self._validate_state()
    
    def next_round(self) -> None:
        """Advance to the next round."""
        if self._status != GameStatus.IN_PROGRESS:
            raise ValueError("Round can only be advanced when game is in progress")
        
        if self._current_round >= 5:
            self._status = GameStatus.GAME_OVER
            logging.info("Game over: Maximum round limit (5) reached")
            return
        
        self._current_round += 1
        self._last_action_time = datetime.now()
        self._validate_state()
    
    def switch_player(self) -> None:
        """Switch the current player."""
        if self._status != GameStatus.IN_PROGRESS:
            raise ValueError("Player can only be switched when game is in progress")
        
        if self._current_player_id is None:
            raise ValueError("No current player set")
        
        self._current_player_id = 3 - self._current_player_id  # Switch between 1 and 2
        self._last_action_time = datetime.now()
        self._validate_state()
    
    def get_current_player_name(self) -> str:
        """Get the name of the current player."""
        if self._current_player_id is None:
            raise ValueError("No current player set")
        
        return self._player1_name if self._current_player_id == 1 else self._player2_name
    
    def get_current_player_score(self) -> tuple[int, int]:
        """Get the current player's scores."""
        if self._current_player_id is None:
            raise ValueError("No current player set")
        
        if self._current_player_id == 1:
            return (self._player1_primary, self._player1_secondary)
        else:
            return (self._player2_primary, self._player2_secondary)
    
    def get_game_duration(self) -> float:
        """Get the current game duration in seconds."""
        if self._game_start_time is None:
            return 0.0
        
        end_time = self._last_action_time or datetime.now()
        return (end_time - self._game_start_time).total_seconds()

    def __init__(
        self,
        player1_name: str = "",
        player2_name: str = "",
        attacker_id: Optional[int] = None,
        first_turn_player_id: Optional[int] = None,
        current_round: int = 1,
        current_player_id: Optional[int] = None,
        game_start_time: Optional[datetime] = None,
        last_action_time: Optional[datetime] = None,
        player1_primary: int = 0,
        player1_secondary: int = 0,
        player2_primary: int = 0,
        player2_secondary: int = 0,
        status: GameStatus = GameStatus.NOT_STARTED
    ):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.attacker_id = attacker_id
        self.first_turn_player_id = first_turn_player_id
        self.current_round = current_round
        self.current_player_id = current_player_id
        self.game_start_time = game_start_time
        self.last_action_time = last_action_time
        self.player1_primary = player1_primary
        self.player1_secondary = player1_secondary
        self.player2_primary = player2_primary
        self.player2_secondary = player2_secondary
        self.status = status
        self._validate_state() 