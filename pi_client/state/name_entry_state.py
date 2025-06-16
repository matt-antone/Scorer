from typing import List, Dict, Optional

class NameEntryState:
    """
    Pure logic class for name entry state and validation.
    This class is independent of Kivy and UI code.
    """
    def __init__(self, players: Optional[List[str]] = None, player_validation: Optional[Dict[str, bool]] = None):
        self.players = players or []
        self.player_validation = player_validation or {}

    def validate_players(self) -> bool:
        return (
            isinstance(self.players, list) and
            len(self.players) == 2 and
            all(isinstance(p, str) and len(p.strip()) > 0 for p in self.players) and
            self.players[0] != self.players[1]
        )

    def validate_player_validation(self) -> bool:
        if not isinstance(self.player_validation, dict):
            return False
        for player in self.players:
            if player not in self.player_validation or not isinstance(self.player_validation[player], bool):
                return False
        return True

    def validate_state(self) -> bool:
        return self.validate_players() and self.validate_player_validation() 