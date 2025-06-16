from typing import Optional

class SplashState:
    """
    Pure logic class for splash screen state and validation.
    This class is independent of Kivy and UI code.
    """
    def __init__(self, is_loading: Optional[bool] = None):
        self.is_loading = is_loading if is_loading is not None else True

    def validate_is_loading(self) -> bool:
        return isinstance(self.is_loading, bool)

    def validate_state(self) -> bool:
        return all([
            self.validate_is_loading(),
        ]) 