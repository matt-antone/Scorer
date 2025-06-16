from typing import List, Dict, Optional

class ScoreboardState:
    """
    Pure logic class for scoreboard state and validation.
    This class is independent of Kivy and UI code.
    """
    def __init__(self, players: Optional[List[str]] = None, scores: Optional[Dict[str, int]] = None,
                 current_round: Optional[int] = None):
        self.players = players or []
        self.scores = scores or {}
        self.current_round = current_round if current_round is not None else 1

    def validate_players(self) -> bool:
        return isinstance(self.players, list) and len(self.players) == 2 and all(isinstance(p, str) for p in self.players)

    def validate_scores(self) -> bool:
        if not isinstance(self.scores, dict):
            return False
        for player in self.players:
            if player not in self.scores or not isinstance(self.scores[player], int) or self.scores[player] < 0:
                return False
        return True

    def validate_current_round(self) -> bool:
        return isinstance(self.current_round, int) and 1 <= self.current_round <= 5

    def validate_state(self) -> bool:
        return all([
            self.validate_players(),
            self.validate_scores(),
            self.validate_current_round(),
        ]) 