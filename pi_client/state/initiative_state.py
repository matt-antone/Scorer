from typing import List, Dict, Optional

class InitiativeState:
    """
    Pure logic class for initiative state and validation.
    This class is independent of Kivy and UI code.
    """
    def __init__(self, players: Optional[List[str]] = None, initiative_rolls: Optional[Dict[str, int]] = None,
                 initiative_validation: Optional[Dict[str, bool]] = None):
        self.players = players or []
        self.initiative_rolls = initiative_rolls or {}
        self.initiative_validation = initiative_validation or {}

    def validate_players(self) -> bool:
        return isinstance(self.players, list) and len(self.players) == 2 and all(isinstance(p, str) for p in self.players)

    def validate_initiative_rolls(self) -> bool:
        if not isinstance(self.initiative_rolls, dict):
            return False
        for player in self.players:
            if player not in self.initiative_rolls:
                return False
            roll = self.initiative_rolls[player]
            if not isinstance(roll, int) or not (1 <= roll <= 6):
                return False
        return True

    def validate_initiative_validation(self) -> bool:
        if not isinstance(self.initiative_validation, dict):
            return False
        for player in self.players:
            if player not in self.initiative_validation or not isinstance(self.initiative_validation[player], bool):
                return False
        return True

    def validate_state(self) -> bool:
        return all([
            self.validate_players(),
            self.validate_initiative_rolls(),
            self.validate_initiative_validation(),
        ]) 