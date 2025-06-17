from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import BooleanProperty, StringProperty, DictProperty
from kivy.clock import Clock
from kivy.event import EventDispatcher
import logging
import json
import threading
from io import BytesIO
import qrcode
from .base_screen import BaseScreen
from ..state.splash_state import SplashState
from ..strings import UI_STRINGS
from ..network.network_manager import NetworkManager
from ..widgets.connection_manager_popup import ConnectionManagerPopup
from kivy.logger import Logger

logger = logging.getLogger(__name__)

class SplashScreen(Screen, EventDispatcher):
    """Splash screen for initial loading and network setup."""

    start_enabled = BooleanProperty(False)
    loading_status = StringProperty('')
    error_message = StringProperty('')
    system_checks = DictProperty({
        'network': False,
        'resources': False,
        'storage': False,
        'saved_game': False
    })

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.network_manager = NetworkManager()
        self.connection_popup = None
        self._timeouts = []
        self._register_events()
        self._setup_network_manager()

    def _register_events(self):
        """Register screen events."""
        self.register_event_type('on_loading_complete')
        self.register_event_type('on_error')

    def _setup_network_manager(self):
        """Setup network manager callbacks."""
        self.network_manager.bind(
            on_network_state_change=self._on_network_state_change,
            on_network_error=self._on_network_error
        )

    def on_pre_enter(self):
        """Called before screen is entered."""
        self._reset_state()
        self._clear_timeouts()

    def on_enter(self):
        """Called when screen is entered."""
        self.start_loading()
        self._validate_state()

    def on_leave(self):
        """Called when leaving the screen."""
        self._clear_timeouts()
        self._clear_error()
        self._reset_loading_state()
        if self.connection_popup:
            self.connection_popup.dismiss()

    def _reset_state(self):
        """Reset screen state."""
        self.start_enabled = False
        self.loading_status = ''
        self.error_message = ''
        self.system_checks = {
            'network': False,
            'resources': False,
            'storage': False,
            'saved_game': False
        }

    def _clear_timeouts(self):
        """Clear all pending timeouts."""
        for timeout in self._timeouts:
            Clock.unschedule(timeout)
        self._timeouts = []

    def _validate_state(self):
        """Validate screen state."""
        if not self.network_manager.is_connected:
            self._show_network_error()
            return False

        if not self._check_resources():
            self._show_resource_error()
            return False

        if not self._check_storage():
            self._show_storage_error()
            return False

        if not self._check_saved_game():
            self._show_saved_game_error()
            return False

        return True

    def start_loading(self):
        """Start the loading process."""
        self.loading_status = 'Checking network...'
        self.network_manager.start_monitoring()

    def check_network(self):
        """Check network connectivity."""
        try:
            self.network_manager.check_network()
            self.system_checks['network'] = self.network_manager.is_connected
            self.update_loading_progress(20, "Network connected")
            return True
        except Exception as e:
            self.handle_network_error(str(e))
            return False

    def handle_network_error(self, error_message=None):
        """Handle network errors."""
        if error_message is None:
            error_message = "Network connection failed. Please check your connection and try again."
        self.error_message = error_message
        self.system_checks['network'] = False
        Clock.schedule_once(lambda dt: self._show_connection_popup(False, error_message=error_message))
        self.start_enabled = False
        if not getattr(self, '_error_dispatched', False):
            self._error_dispatched = True
            self.dispatch('on_error', error_message)
            self._error_dispatched = False

    def _on_network_state_change(self, instance, is_connected, connection_type, ip_address):
        """Handle network state changes."""
        if is_connected:
            self.loading_status = 'Network connected'
            self._show_connection_popup(True, connection_type, ip_address)
            self._generate_qr_codes()
        else:
            self.loading_status = 'Network disconnected'
            self._show_connection_popup(False)
            self.start_enabled = False

    def _on_network_error(self, instance, error_message):
        """Handle network errors."""
        self.handle_network_error(error_message)

    def _show_connection_popup(self, is_connected, connection_type='', ip_address='', error_message=''):
        """Show connection manager popup."""
        if not self.connection_popup:
            self.connection_popup = ConnectionManagerPopup()
            self.connection_popup.on_retry_callback = self._retry_network_check
        self.connection_popup.update_status(
            is_connected,
            connection_type,
            ip_address,
            error_message
        )
        if not self.connection_popup.is_open:
            self.connection_popup.open()

    def _retry_network_check(self):
        """Retry network check."""
        self.loading_status = 'Retrying network check...'
        self.network_manager.check_network()

    def update_loading_progress(self, progress, status):
        """Update loading progress and status."""
        self.loading_status = status
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            if not hasattr(app, 'game_state') or app.game_state is None:
                app.game_state = {}
            if 'system_checks' not in app.game_state or app.game_state['system_checks'] is None:
                app.game_state['system_checks'] = {}
            app.game_state['system_checks'].update(self.system_checks)

    def _generate_qr_codes(self):
        """Generate QR codes for client connections."""
        if not self.network_manager.is_connected:
            return

        client_types = ['player1', 'player2', 'observer']
        qr_data = []
        
        for client_type in client_types:
            data = {
                'type': client_type,
                'ip': self.network_manager.ip_address,
                'port': 8000,  # Default port
                'role': client_type
            }
            qr_data.append(data)

        # Start QR code generation in background thread
        threading.Thread(target=self._generate_qr_codes_thread, args=(qr_data,)).start()

    def _generate_qr_codes_thread(self, qr_data):
        """Generate QR codes in background thread."""
        try:
            qr_codes = []
            for data in qr_data:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(json.dumps(data))
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                
                qr_codes.append({
                    'type': data['type'],
                    'image': buffer.getvalue()
                })

            # Store QR codes in game state
            app = App.get_running_app()
            if app and hasattr(app, 'game_state'):
                if not hasattr(app, 'game_state') or app.game_state is None:
                    app.game_state = {}
                app.game_state['qr_codes'] = qr_codes
                self.start_enabled = True
        except Exception as e:
            Logger.error(f'QR Code generation failed: {str(e)}')
            Clock.schedule_once(lambda dt: self._handle_qr_code_error(str(e)))

    def _handle_qr_code_error(self, error_message):
        """Handle QR code generation errors."""
        self.error_message = f"QR code generation failed: {error_message}"
        self.start_enabled = False

    def on_loading_complete(self):
        """Called when loading is complete."""
        self.start_enabled = True
        self.dispatch('on_loading_complete')

    def on_error(self, error_message):
        """Called when an error occurs."""
        self.error_message = error_message
        self.start_enabled = False

    def _check_resources(self):
        """Check if required resources are available."""
        return True

    def _show_resource_error(self):
        """Show resource error."""
        self.error_message = "Required resources not found"
        self.start_enabled = False

    def _check_storage(self):
        """Check if storage is available."""
        return True

    def _show_storage_error(self):
        """Show storage error."""
        self.error_message = "Storage not available"
        self.start_enabled = False

    def _check_saved_game(self):
        """Check if there's a saved game."""
        return True

    def _show_saved_game_error(self):
        """Show saved game error."""
        self.error_message = "Error checking saved game"
        self.start_enabled = False

    def _show_network_error(self):
        """Show network error."""
        self.error_message = "Network connection required"
        self.start_enabled = False

    def _reset_loading_state(self):
        """Reset loading state."""
        self.loading_status = ''
        self.start_enabled = False