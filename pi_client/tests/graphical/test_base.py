"""
Base test class for graphical tests.
Provides common setup and teardown functionality.
"""
import unittest
import os
from kivy.tests.common import GraphicUnitTest
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from pi_client.main import ScorerApp
from pi_client.screens.splash_screen import SplashScreen
from pi_client.screens.resume_or_new_screen import ResumeOrNewScreen
from pi_client.screens.name_entry_screen import NameEntryScreen
from pi_client.screens.deployment_setup_screen import DeploymentSetupScreen
from pi_client.screens.initiative_screen import InitiativeScreen
from pi_client.screens.scoreboard_screen import ScoreboardScreen
from pi_client.screens.game_over_screen import GameOverScreen

class BaseScreenTest(GraphicUnitTest):
    """Base class for all screen tests."""
    
    app_class = ScorerApp
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        
        # Load all required KV files
        kv_files = [
            'scorer.kv',
            'screens/splash_screen.kv',
            'screens/name_entry_screen.kv',
            'screens/deployment_setup_screen.kv',
            'screens/initiative_screen.kv',
            'screens/scoreboard_screen.kv',
            'screens/game_over_screen.kv',
            'screens/resume_or_new_screen.kv',
            'widgets/button_styles.kv',
            'widgets/header_widget.kv',
            'widgets/number_pad_popup.kv',
            'widgets/concede_confirm_popup.kv'
        ]
        
        # Get the absolute path to the pi_client directory
        pi_client_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        
        for kv_file in kv_files:
            kv_path = os.path.join(pi_client_dir, kv_file)
            if os.path.exists(kv_path):
                Builder.load_file(kv_path)
            else:
                print(f"Warning: KV file not found: {kv_path}")
        
        self.app = self.app_class()
        self.app.game_state = {
            'players': [],
            'roles': [],
            'roll_validation': {'min_value': 1, 'max_value': 6},
            'scores': {},
            'winner': None,
            'game_stats': {'duration': 0, 'rounds_played': 0, 'total_points': 0},
        }
        self.app.root = ScreenManager()
        self.app.root.add_widget(SplashScreen(name='splash'))
        self.app.root.add_widget(ResumeOrNewScreen(name='resume'))
        self.app.root.add_widget(NameEntryScreen(name='name_entry'))
        self.app.root.add_widget(DeploymentSetupScreen(name='deployment_setup'))
        self.app.root.add_widget(InitiativeScreen(name='initiative'))
        self.app.root.add_widget(ScoreboardScreen(name='scoreboard'))
        self.app.root.add_widget(GameOverScreen(name='game_over'))
        self.app.root.current = 'splash'
        self.advance_frames(1)
    
    def tearDown(self):
        """Clean up test environment."""
        if hasattr(self, 'screen') and self.screen:
            self.screen.stop_sync()
            if hasattr(self.screen, '_error_timeout') and self.screen._error_timeout:
                self.screen._error_timeout.cancel()
        super().tearDown()
    
    def get_screen(self, name):
        """Get a screen by name."""
        return self.app.root.get_screen(name)
    
    def advance_frames(self, count):
        """Advance the clock by the given number of frames."""
        for _ in range(count):
            Clock.tick()
    
    def assert_widget_exists(self, screen, widget_id):
        """Assert that a widget exists in the screen."""
        widget = screen.ids.get(widget_id)
        assert widget is not None, f"Widget {widget_id} not found in screen"
    
    def assert_widget_text(self, screen, widget_id, expected_text):
        """Assert that a widget's text matches the expected text."""
        widget = screen.ids.get(widget_id)
        assert widget is not None, f"Widget {widget_id} not found in screen"
        assert widget.text == expected_text, f"Widget {widget_id} text mismatch: expected {expected_text}, got {widget.text}"
    
    def assert_widget_disabled(self, screen, widget_id, expected_disabled):
        """Assert that a widget's disabled state matches the expected state."""
        widget = screen.ids.get(widget_id)
        assert widget is not None, f"Widget {widget_id} not found in screen"
        assert widget.disabled == expected_disabled, f"Widget {widget_id} disabled state mismatch: expected {expected_disabled}, got {widget.disabled}"
    
    def validate_string_field(self, widget_id: str, expected_text: str) -> None:
        """Validate a string field's text matches the expected value, logging a warning if not."""
        screen = self.app.root.current_screen
        widget = screen.ids.get(widget_id)
        if not widget:
            self.fail(f"Widget {widget_id} not found")
            return
        if not hasattr(widget, 'text'):
            self.fail(f"Widget {widget_id} has no text property")
            return
        if widget.text != expected_text:
            import warnings
            warnings.warn(f"Widget {widget_id} text mismatch: expected {expected_text}, got {widget.text}")
            return 