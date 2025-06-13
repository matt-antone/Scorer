from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import BooleanProperty, StringProperty, NumericProperty, ObjectProperty, DictProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
import logging
import os
import socket
import qrcode
from io import BytesIO
from PIL import Image
import threading
from .base_screen import BaseScreen, ValidationError, StateError, SyncError

logger = logging.getLogger(__name__)

class SplashScreen(BaseScreen):
    """Splash screen for the application."""

    start_enabled = BooleanProperty(False)
    status_text = StringProperty('')
    loading_status = StringProperty('Initializing...')
    app_version = StringProperty('1.0.0')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading_progress = 0
        self.is_loading = False
        self.is_syncing = False
        self.has_error = False
        self.has_saved_game = False
        self.saved_game_info = None
        self.system_checks = {
            'network': False,
            'resources': False,
            'storage': False
        }
        self.resources = {
            'images': [],
            'fonts': [],
            'sounds': []
        }
        self._loading_timeout = None
        self._error_timeout = None

    def on_enter(self):
        """Called when the screen is entered."""
        super().on_enter()
        self.start_loading()

    def start_loading(self):
        """Start the loading process."""
        self.is_loading = True
        self.loading_progress = 0
        self.loading_status = 'Initializing...'
        self._loading_timeout = Clock.schedule_once(self.check_network, 1)

    def check_network(self, dt=None):
        """Check network connectivity."""
        try:
            # Real network check
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                self.system_checks['network'] = True
            except OSError:
                self.system_checks['network'] = False
                self.handle_network_error()
                return
            self.loading_progress = 20
            self.loading_status = 'Checking network...'
            self._loading_timeout = Clock.schedule_once(self.check_resources, 1)
        except Exception as e:
            self.handle_error(str(e))

    def check_resources(self, dt=None):
        """Check required resources."""
        try:
            self.load_resources()
            # Simulate resource check
            self.loading_progress = 40
            self.loading_status = 'Loading resources...'
            self.system_checks['resources'] = True
            self._loading_timeout = Clock.schedule_once(self.check_storage, 1)
        except Exception as e:
            self.handle_error(str(e))

    def check_storage(self, dt):
        """Check storage availability."""
        try:
            # Simulate storage check
            self.loading_progress = 60
            self.loading_status = 'Checking storage...'
            self.system_checks['storage'] = True
            self._loading_timeout = Clock.schedule_once(self.check_saved_game, 1)
        except Exception as e:
            self.handle_error(str(e))

    def check_saved_game(self, dt=None):
        """Check for saved game (scheduled by Clock)."""
        try:
            # Simulate saved game check
            self.loading_progress = 80
            self.loading_status = 'Checking for saved game...'
            self.has_saved_game = False
            self.saved_game_info = None
            self._loading_timeout = Clock.schedule_once(self.finish_loading, 1)
        except Exception as e:
            self.handle_error(str(e))

    def finish_loading(self, dt):
        """Finish the loading process."""
        try:
            self.loading_progress = 100
            self.loading_status = 'Ready!'
            self.is_loading = False
            self.start_enabled = True
            
            # Transition to next screen
            app = App.get_running_app()
            if app and hasattr(app, 'root'):
                if self.has_saved_game:
                    app.root.current = 'resume_or_new'
                else:
                    app.root.current = 'name_entry'
        except Exception as e:
            self.handle_error(str(e))

    def handle_error(self, message):
        """Handle error."""
        self.show_error(message)
        self.has_error = True
        self.is_loading = False
        if self._loading_timeout:
            self._loading_timeout.cancel()
            self._loading_timeout = None

    def on_leave(self):
        """Called when leaving the screen."""
        super().on_leave()
        if self._loading_timeout:
            self._loading_timeout.cancel()
            self._loading_timeout = None
        if self._error_timeout:
            self._error_timeout.cancel()
            self._error_timeout = None

    def _start_background_tasks(self):
        """Start background tasks for initialization."""
        self.logger.info("SplashScreen: Scheduling background tasks")
        Clock.schedule_once(self._perform_background_tasks)

    def _perform_background_tasks(self, dt):
        """Perform background initialization tasks."""
        self.update_loading_progress(50, "Loading resources...")
        self.check_network()
        self.check_saved_game()
        self.load_resources()
        self.update_loading_progress(100, "Ready")

    def _check_saved_game_logic(self):
        """Logic-only: Check for saved game."""
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            self.has_saved_game = app.game_state.get('has_saved_game', False)
            self.saved_game_info = app.game_state.get('saved_game_info')
            if self.has_saved_game and self.saved_game_info:
                try:
                    self.validate_saved_game(self.saved_game_info)
                except (ValidationError, StateError):
                    self.has_saved_game = False
                    self.saved_game_info = None
        return self.has_saved_game

    def load_resources(self):
        """Load application resources."""
        try:
            # Load images
            image_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images')
            if os.path.exists(image_dir):
                self.resources['images'] = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
            
            # Load fonts
            font_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'fonts')
            if os.path.exists(font_dir):
                self.resources['fonts'] = [f for f in os.listdir(font_dir) if f.endswith(('.ttf', '.otf'))]
            
            # Load sounds
            sound_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'sounds')
            if os.path.exists(sound_dir):
                self.resources['sounds'] = [f for f in os.listdir(sound_dir) if f.endswith(('.wav', '.mp3'))]
            
            self.system_checks['resources'] = len(self.resources['images']) > 0
        except Exception as e:
            self.handle_resource_error()

    def update_loading_status(self, status):
        """Update loading status."""
        self.loading_status = status

    def handle_network_error(self):
        """Handle network error."""
        self.show_error("Network connection failed")
        self.system_checks['network'] = False

    def handle_qr_code_error(self):
        """Handle QR code generation error."""
        self.show_error("Failed to generate QR codes")

    def handle_loading_error(self):
        """Handle loading error."""
        self.show_error("Loading failed: Failed to load resources")
        self.is_loading = False

    def handle_resource_error(self):
        """Handle resource error."""
        self.show_error("Failed to initialize resources")
        self.system_checks['resources'] = False

    def recover_from_network_error(self):
        """Recover from network error."""
        self.clear_error()
        self.check_network()

    def recover_from_resource_error(self):
        self.clear_error()
        self.load_resources()

    def generate_qr_codes(self):
        ip_address = self._get_ip_address() or '127.0.0.1'
        self._generate_qr_codes(ip_address)

    def load_images(self):
        self.load_resources()

    def generate_qr_code(self, data):
        """Generate QR code for given data."""
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            # Convert PIL Image to bytes
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            return buffer.getvalue()
        except Exception as e:
            self.handle_qr_code_error()
            return None

    def start_game(self):
        """Start the game"""
        app = App.get_running_app()
        if app:
            if self._check_saved_game_logic():
                app.root.current = 'resume_or_new'
            else:
                app.root.current = 'name_entry'

    def on_pre_enter(self):
        """Called before screen is entered."""
        super().on_pre_enter()
        self._start_background_tasks()

    def _check_network(self):
        """Check if network is available"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            logger.info("SplashScreen: Network check successful")
            self.system_checks['network'] = True
            return True
        except OSError:
            logger.warning("SplashScreen: Network check failed")
            self.system_checks['network'] = False
            return False
    
    def _get_ip_address(self):
        """Get the local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            logger.info(f"SplashScreen: Got IP address: {ip}")
            return ip
        except Exception as e:
            logger.error(f"SplashScreen: Failed to get IP address: {str(e)}")
            return None

    def _update_status(self, text):
        """Update status text"""
        self.loading_status = text

    def show_game_saved(self, has_saved):
        """Show if the game is saved"""
        self.has_saved_game = has_saved

    def show_resources_available(self, resources):
        """Show the available resources"""
        self.resources = resources

    def show_system_check_results(self, checks):
        """Show the results of system checks"""
        self.system_checks = checks

    def show_app_version_available(self, version):
        """Show the available app version"""
        self.app_version = version

    def show_qr_code_generation_error(self):
        """Show an error message for QR code generation"""
        self.handle_qr_code_error()

    def show_network_connection_error(self):
        """Show an error message for network connection"""
        self.handle_network_error()

    def _generate_qr_codes(self, ip_address):
        """Generate QR codes for player and observer clients"""
        try:
            # Create QR codes directory if it doesn't exist
            qr_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'qr_codes')
            os.makedirs(qr_dir, exist_ok=True)
            
            # Generate QR codes for different clients
            base_url = f"http://{ip_address}:5000"
            clients = {
                'player1': f"{base_url}/player/1",
                'player2': f"{base_url}/player/2",
                'observer': f"{base_url}/observer"
            }
            
            for client, url in clients.items():
                logger.info(f"SplashScreen: Generating QR code for {client}")
                qr_data = self.generate_qr_code(url)
                if qr_data:
                    # Save QR code
                    qr_path = os.path.join(qr_dir, f'{client}_qr.png')
                    with open(qr_path, 'wb') as f:
                        f.write(qr_data)
                    logger.info(f"SplashScreen: Saved QR code to {qr_path}")
                    
                    # Set the first QR code path for display
                    if client == 'player1':
                        self.player1_qr = qr_path
            
            return True
            
        except Exception as e:
            logger.error(f"SplashScreen: Error generating QR codes: {str(e)}")
            return False

    def handle_client_update(self, update):
        """Handle client update."""
        if update.get('type') == 'saved_game':
            try:
                has_saved = update.get('has_saved_game', False)
                game_info = update.get('game_info')
                if has_saved and game_info:
                    self.validate_saved_game(game_info)
                    self.has_saved_game = True
                    self.saved_game_info = game_info
                else:
                    self.has_saved_game = False
                    self.saved_game_info = None
            except (ValidationError, StateError) as e:
                self.has_saved_game = False
                self.saved_game_info = None
                self.has_error = True
                self.loading_status = str(e)
        elif update.get('type') == 'loading':
            progress = update.get('progress', 0)
            status = update.get('status')
            self.update_loading_progress(progress, status)

    def validate_saved_game(self, saved_game):
        """Validate saved game data."""
        if not isinstance(saved_game, dict):
            raise ValidationError("Saved game must be a dictionary")
        
        required_keys = ['players', 'current_round', 'scores']
        for key in required_keys:
            if key not in saved_game:
                raise StateError(f"Missing required saved game key: {key}")
        
        if not isinstance(saved_game['players'], list) or len(saved_game['players']) != 2:
            raise ValidationError("Players must be a list of exactly 2 players")
        
        if not isinstance(saved_game['current_round'], int) or saved_game['current_round'] < 1:
            raise ValidationError("Current round must be a positive integer")
        
        if not isinstance(saved_game['scores'], dict):
            raise ValidationError("Scores must be a dictionary")
        
        return True

    def update_loading_progress(self, progress, status=None):
        """Update loading progress and status."""
        self.loading_progress = progress
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            app.game_state['loading_progress'] = progress
        if status:
            self.loading_status = status

    def clear_error(self):
        """Clear any error state."""
        self.has_error = False
        self.loading_status = 'Initializing...'
        if self._loading_timeout:
            self._loading_timeout.cancel()
            self._loading_timeout = None

    def on_start_button(self):
        """Handle start button press."""
        if not self.start_enabled:
            return
            
        app = App.get_running_app()
        if app and hasattr(app, 'root'):
            if self.has_saved_game:
                app.root.current = 'resume_or_new'
            else:
                app.root.current = 'name_entry'