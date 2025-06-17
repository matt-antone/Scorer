from typing import List, Dict, Optional, Tuple

class InitiativeState:
    """
    Pure logic class for initiative state and validation.
    This class is independent of Kivy and UI code.
    """
    def __init__(self, players: Optional[List[str]] = None, rolls: Optional[Dict[str, Optional[int]]] = None,
                 roll_validation: Optional[Dict[str, int]] = None, current_round: int = 1):
        self.players = players or ['Player1', 'Player2']
        self.rolls = rolls or {p: None for p in self.players}
        self.roll_validation = roll_validation or {'min_value': 1, 'max_value': 6}
        self.current_round = current_round
        self.initiative_winner = None
        self.initiative_loser = None

    def validate_roll(self, roll: int) -> bool:
        """Validate a roll value."""
        min_val = self.roll_validation.get('min_value', 1)
        max_val = self.roll_validation.get('max_value', 6)
        return isinstance(roll, int) and min_val <= roll <= max_val

    def add_roll(self, player: str, roll: int) -> bool:
        """Add a roll for a player."""
        if player not in self.players:
            return False
        if not self.validate_roll(roll):
            return False
        self.rolls[player] = roll
        return True

    def determine_initiative(self) -> Tuple[Optional[str], Optional[str]]:
        """Determine initiative based on roll results."""
        if None in self.rolls.values():
            return None, None
        
        p1_roll = self.rolls.get(self.players[0], 0)
        p2_roll = self.rolls.get(self.players[1], 0)
        
        if p1_roll > p2_roll:
            winner, loser = self.players[0], self.players[1]
        elif p2_roll > p1_roll:
            winner, loser = self.players[1], self.players[0]
        else:
            return None, None  # Tie
        
        self.initiative_winner = winner
        self.initiative_loser = loser
        return winner, loser

    def get_tied_players(self) -> List[str]:
        """Get players with the highest roll (for tie handling)."""
        if None in self.rolls.values():
            return []
        
        max_roll = max(self.rolls.values())
        return [p for p, r in self.rolls.items() if r == max_roll]

    def reset_tied_players(self, tied_players: List[str]) -> None:
        """Reset rolls for tied players."""
        for player in tied_players:
            if player in self.rolls:
                self.rolls[player] = None

    def validate_players(self) -> bool:
        """Validate players list."""
        return isinstance(self.players, list) and len(self.players) == 2 and all(isinstance(p, str) for p in self.players)

    def validate_rolls(self) -> bool:
        """Validate rolls dictionary."""
        if not isinstance(self.rolls, dict):
            return False
        for player in self.players:
            if player not in self.rolls:
                return False
            roll = self.rolls[player]
            if roll is not None and not self.validate_roll(roll):
                return False
        return True

    def validate_roll_validation(self) -> bool:
        """Validate roll validation rules."""
        if not isinstance(self.roll_validation, dict):
            return False
        required_keys = ['min_value', 'max_value']
        for key in required_keys:
            if key not in self.roll_validation:
                return False
        return True

    def validate_state(self) -> bool:
        """Validate the entire state."""
        return all([
            self.validate_players(),
            self.validate_rolls(),
            self.validate_roll_validation(),
        ])

    def get_state_dict(self) -> Dict:
        """Get state as dictionary for serialization."""
        return {
            'players': list(self.players),
            'rolls': dict(self.rolls),
            'roll_validation': dict(self.roll_validation),
            'current_round': self.current_round,
            'initiative_winner': self.initiative_winner,
            'initiative_loser': self.initiative_loser
        }

    def update_from_dict(self, state_dict: Dict) -> None:
        """Update state from dictionary."""
        if 'players' in state_dict:
            self.players = list(state_dict['players'])
        if 'rolls' in state_dict:
            self.rolls = dict(state_dict['rolls'])
        if 'roll_validation' in state_dict:
            self.roll_validation = dict(state_dict['roll_validation'])
        if 'current_round' in state_dict:
            self.current_round = state_dict['current_round']
        if 'initiative_winner' in state_dict:
            self.initiative_winner = state_dict['initiative_winner']
        if 'initiative_loser' in state_dict:
            self.initiative_loser = state_dict['initiative_loser'] 