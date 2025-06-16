from typing import Optional

class ResumeOrNewState:
    """
    Pure logic class for resume or new game state and validation.
    This class is independent of Kivy and UI code.
    """
    def __init__(self, has_saved_game: Optional[bool] = None):
        self.has_saved_game = has_saved_game if has_saved_game is not None else False

    def validate_has_saved_game(self) -> bool:
        return isinstance(self.has_saved_game, bool)

    def validate_state(self) -> bool:
        return all([
            self.validate_has_saved_game(),
        ]) 