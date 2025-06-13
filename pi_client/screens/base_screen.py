from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivy.app import App
import logging

class ScreenError(Exception):
    """Base exception for screen-related errors."""
    pass

class ValidationError(ScreenError):
    """Raised when input validation fails."""
    pass

class StateError(ScreenError):
    """Raised when state is invalid or missing required data."""
    pass

class SyncError(ScreenError):
    """Raised when synchronization fails."""
    pass

class BaseScreen(Screen):
    """
    Base screen class that provides common functionality for all screens.
    All screens should inherit from this class.
    """
    # State flags
    is_loading = BooleanProperty(False)
    is_syncing = BooleanProperty(False)
    has_error = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sync_event = None
        self._error_timeout = None
        self._current_error = None
        self._current_status = None
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def on_pre_enter(self):
        """
        Called before the screen is shown.
        Updates the view from state and starts synchronization.
        """
        self.logger.debug("Pre-entering screen")
        try:
            self.update_view_from_state()
            self.start_sync()
        except Exception as e:
            self.logger.error(f"Error in on_pre_enter: {str(e)}")
            self.handle_error(e)

    def on_enter(self):
        """
        Called when the screen is shown.
        Hides the loading spinner.
        """
        self.logger.debug("Entering screen")
        self.show_loading(False)

    def on_leave(self):
        """
        Called when leaving the screen.
        Stops synchronization and clears any pending operations.
        """
        self.logger.debug("Leaving screen")
        self.stop_sync()
        self.clear_error()
        if self._error_timeout:
            self._error_timeout.cancel()
            self._error_timeout = None

    def update_view_from_state(self):
        """
        Update the UI from the current game state.
        Must be implemented by child classes.
        """
        self.logger.debug("Updating view from state")
        app = App.get_running_app()
        if not app or not hasattr(app, 'game_state'):
            raise StateError("Game state not available")
        
        # Child classes should implement their specific state updates
        pass

    def validate_state(self, required_keys=None):
        """
        Validate the current game state.
        
        Args:
            required_keys (list): List of required state keys to validate
            
        Returns:
            bool: True if state is valid, False otherwise
            
        Raises:
            StateError: If state is invalid
        """
        self.logger.debug("Validating state")
        app = App.get_running_app()
        if not app or not hasattr(app, 'game_state'):
            raise StateError("Game state not available")
            
        if required_keys:
            state = app.game_state
            missing_keys = [key for key in required_keys if key not in state]
            if missing_keys:
                raise StateError(f"Missing required state keys: {missing_keys}")
        
        return True

    def show_error(self, message, timeout=5):
        """
        Display an error message.
        Child classes should implement UI-specific error display.
        
        Args:
            message (str): Error message to display
            timeout (int): Time in seconds before error clears
        """
        self.logger.error(f"Showing error: {message}")
        self._current_error = message
        self.has_error = True
        
        # Clear error after timeout
        if self._error_timeout:
            self._error_timeout.cancel()
        self._error_timeout = Clock.schedule_once(
            lambda dt: self.clear_error(), timeout
        )

    def clear_error(self):
        """Clear any displayed error message."""
        self.logger.debug("Clearing error")
        self._current_error = None
        self.has_error = False

    def show_status(self, message):
        """
        Display a status message.
        Child classes should implement UI-specific status display.
        
        Args:
            message (str): Status message to display
        """
        self.logger.debug(f"Showing status: {message}")
        self._current_status = message

    def clear_status(self):
        """Clear any displayed status message."""
        self.logger.debug("Clearing status")
        self._current_status = None

    def show_loading(self, show=True):
        """
        Show or hide the loading state.
        Child classes should implement UI-specific loading display.
        
        Args:
            show (bool): Whether to show or hide the loading state
        """
        self.logger.debug(f"Setting loading state: {show}")
        self.is_loading = show

    def start_sync(self):
        """Start client synchronization."""
        self.logger.debug("Starting sync")
        self.is_syncing = True
        # Child classes should implement specific sync logic
        pass

    def stop_sync(self):
        """Stop client synchronization."""
        self.logger.debug("Stopping sync")
        self.is_syncing = False
        if self._sync_event:
            self._sync_event.cancel()
            self._sync_event = None

    def handle_error(self, error):
        """
        Handle different types of errors.
        
        Args:
            error (Exception): The error to handle
        """
        self.logger.error(f"Handling error: {str(error)}")
        if isinstance(error, ValidationError):
            self.show_error(f"Validation error: {str(error)}")
        elif isinstance(error, StateError):
            self.show_error(f"State error: {str(error)}")
        elif isinstance(error, SyncError):
            self.show_error(f"Sync error: {str(error)}")
        else:
            self.show_error(f"Unexpected error: {str(error)}")

    def recover_from_error(self):
        """
        Attempt to recover from an error state.
        Must be implemented by child classes.
        """
        self.logger.debug("Attempting error recovery")
        # Child classes should implement specific recovery logic
        pass

    def validate_input(self, input_data, rules=None):
        """
        Validate input data against provided rules.
        
        Args:
            input_data (dict): Input data to validate
            rules (dict): Validation rules for each input field
            
        Returns:
            bool: True if input is valid, False otherwise
            
        Raises:
            ValidationError: If input validation fails
        """
        self.logger.debug("Validating input")
        if not rules:
            return True
            
        for field, rule in rules.items():
            if field not in input_data:
                raise ValidationError(f"Missing required field: {field}")
            if not rule(input_data[field]):
                raise ValidationError(f"Invalid value for field: {field}")
        
        return True

    def sanitize_input(self, input_data):
        """
        Sanitize user input.
        
        Args:
            input_data (dict): Input data to sanitize
            
        Returns:
            dict: Sanitized input data
        """
        self.logger.debug("Sanitizing input")
        # Basic sanitization - strip whitespace from strings
        sanitized = {}
        for key, value in input_data.items():
            if isinstance(value, str):
                sanitized[key] = value.strip()
            else:
                sanitized[key] = value
        return sanitized

    def update_state(self, updates):
        """
        Update the game state.
        
        Args:
            updates (dict): State updates to apply
            
        Raises:
            StateError: If state update fails
        """
        self.logger.debug(f"Updating state: {updates}")
        app = App.get_running_app()
        if not app or not hasattr(app, 'game_state'):
            raise StateError("Game state not available")
            
        try:
            app.game_state.update(updates)
            self.broadcast_state()
        except Exception as e:
            raise StateError(f"Failed to update state: {str(e)}")

    def broadcast_state(self):
        """
        Broadcast state changes to clients.
        Must be implemented by child classes.
        """
        self.logger.debug("Broadcasting state")
        # Child classes should implement specific broadcast logic
        pass

    def handle_client_update(self, update):
        """
        Handle updates from clients.
        Must be implemented by child classes.
        
        Args:
            update (dict): Update from client
        """
        self.logger.debug(f"Handling client update: {update}")
        # Child classes should implement specific update handling
        pass

    def validate_game_state(self, state):
        """
        Validate game state.
        
        Args:
            state (dict): Game state to validate
            
        Returns:
            bool: True if state is valid, False otherwise
            
        Raises:
            StateError: If state validation fails
        """
        self.logger.debug("Validating game state")
        required_keys = ['players', 'current_round', 'scores']
        for key in required_keys:
            if key not in state:
                raise StateError(f"Missing required state key: {key}")
        return True

    def validate_loading_progress(self, progress):
        """
        Validate loading progress.
        
        Args:
            progress (int): Loading progress to validate
            
        Returns:
            bool: True if progress is valid, False otherwise
            
        Raises:
            ValidationError: If progress validation fails
        """
        self.logger.debug("Validating loading progress")
        if not isinstance(progress, int) or progress < 0 or progress > 100:
            raise ValidationError("Invalid loading progress")
        return True

    def validate_saved_game(self, saved_game):
        """
        Validate saved game data.
        
        Args:
            saved_game (dict): Saved game data to validate
            
        Returns:
            bool: True if saved game is valid, False otherwise
            
        Raises:
            StateError: If saved game validation fails
        """
        self.logger.debug("Validating saved game")
        required_keys = ['players', 'current_round', 'scores']
        for key in required_keys:
            if key not in saved_game:
                raise StateError(f"Missing required saved game key: {key}")
        return True

    def update_loading_progress(self, progress, status=None):
        """
        Update loading progress and status.
        
        Args:
            progress (int): New loading progress
            status (str): New loading status
        """
        self.logger.debug(f"Updating loading progress: {progress}, status: {status}")
        self.validate_loading_progress(progress)
        self.loading_progress = progress
        if status:
            self.loading_status = status 