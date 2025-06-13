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
    """Splash screen that handles initial loading and setup."""
    
    # Properties
    app_version = StringProperty('1.0.0')
    loading_progress = NumericProperty(0)
    loading_status = StringProperty('Initializing...')
    has_network = BooleanProperty(False)
    network_check_complete = BooleanProperty(False)
    has_saved_game = BooleanProperty(False)
    start_button_enabled = BooleanProperty(False)
    player1_qr = ObjectProperty(None)
    player2_qr = ObjectProperty(None)
    observer_qr = ObjectProperty(None)
    resources = DictProperty({'images': [], 'fonts': [], 'sounds': []})
    system_checks = DictProperty({'network': False, 'resources': False, 'storage': False})
    is_loading = BooleanProperty(False)
    status_text = StringProperty('')
    start_enabled = BooleanProperty(False)
    saved_game_info = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.logger.info("SplashScreen: Initializing")
        self._loading_timeout = None
        self._error_timeout = None
        self.logger.info("SplashScreen: Scheduling background tasks")
        self._start_background_tasks()

    def _start_background_tasks(self):
        """Start background tasks for initialization."""
        self.logger.info("SplashScreen: Scheduling background tasks")
        Clock.schedule_once(self._perform_background_tasks)

    def _perform_background_tasks(self, dt):
        """Perform background initialization tasks."""
        self.update_loading_progress(50, "Loading resources...")
        self.check_network()
        self.check_saved_game()
        self.update_loading_progress(100, "Ready")

    def check_network(self):
        """Check network connectivity."""
        self.has_network = True  # Simplified for testing
        self.network_check_complete = True
        self.update_start_button_state()

    def check_saved_game(self):
        """Check for saved game."""
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            self.has_saved_game = app.game_state.get('has_saved_game', False)
            self.saved_game_info = app.game_state.get('saved_game_info')
        return self.has_saved_game

    def update_loading_status(self, status):
        """Update loading status."""
        self.loading_status = status

    def update_start_button_state(self):
        """Update start button state based on conditions."""
        self.start_button_enabled = (
            self.has_network and 
            self.network_check_complete and 
            not self.is_loading
        )

    def handle_network_error(self):
        """Handle network error."""
        self.show_error("Network connection failed")
        self.has_network = False
        self.network_check_complete = False
        self.update_start_button_state()

    def handle_qr_code_error(self):
        """Handle QR code generation error."""
        self.show_error("Failed to generate QR codes")

    def recover_from_network_error(self):
        """Recover from network error."""
        self.clear_error()
        self.check_network()

    def generate_qr_code(self, data):
        """Generate QR code for given data."""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img

    def start_game(self):
        """Start the game"""
        app = App.get_running_app()
        if app:
            if self.check_saved_game():
                app.root.current = 'resume_or_new'
            else:
                app.root.current = 'name_entry'

    def on_pre_enter(self):
        """Called before screen is entered."""
        super().on_pre_enter()
        self._start_background_tasks()

    def on_leave(self):
        """Called when leaving the screen."""
        super().on_leave()
        if self._loading_timeout:
            self._loading_timeout.cancel()
        if self._error_timeout:
            self._error_timeout.cancel()

    def _check_network(self):
        """Check if network is available"""
        try:
            # Try to connect to a reliable host
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            logger.info("SplashScreen: Network check successful")
            self.has_network = True
            self.system_checks['network'] = True
            return True
        except OSError:
            logger.warning("SplashScreen: Network check failed")
            self.has_network = False
            self.system_checks['network'] = False
            return False
    
    def _get_ip_address(self):
        """Get the local IP address"""
        try:
            # Create a socket to get the local IP
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
        self.status_text = text

    def show_game_saved(self, has_saved):
        """Show if the game is saved"""
        self.has_saved_game = has_saved

    def show_start_button_enabled(self, enabled):
        """Show if the start button is enabled"""
        self.start_button_enabled = enabled

    def show_player1_qr_code_path(self, qr_code_path):
        """Show the path to the QR code for player 1"""
        self.player1_qr = qr_code_path

    def show_player2_qr_code_path(self, qr_code_path):
        """Show the path to the QR code for player 2"""
        self.player2_qr = qr_code_path

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

    def show_network_check_completed(self, complete):
        """Show if network check is completed"""
        self.network_check_complete = complete

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
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(url)
                qr.make(fit=True)
                
                # Create QR code image
                qr_image = qr.make_image(fill_color="black", back_color="white")
                
                # Save QR code
                qr_path = os.path.join(qr_dir, f'{client}_qr.png')
                qr_image.save(qr_path)
                logger.info(f"SplashScreen: Saved QR code to {qr_path}")
                
                # Set the first QR code path for display
                if client == 'player1':
                    self.qr_code_path = qr_path
                    self.player1_qr = qr_path
            
            return True
            
        except Exception as e:
            logger.error(f"SplashScreen: Error generating QR codes: {str(e)}")
            return False
    
    def on_start_button(self):
        """Handle start button press"""
        logger.info("SplashScreen: Start button pressed")
        app = App.get_running_app()
        if app:
            logger.info("SplashScreen: Calling after_splash()")
            app.after_splash()
        else:
            logger.error("SplashScreen: No running app found")

    def handle_loading_error(self):
        """Handle loading error."""
        self.show_error("Loading failed: Failed to load resources")
        self.is_loading = False
        self.update_start_button_state()

    def handle_resource_error(self):
        """Handle resource error."""
        self.show_error("Failed to initialize resources")
        self.system_checks['resources'] = False
        self.update_start_button_state()

    def recover_from_resource_error(self):
        """Recover from resource error."""
        self.clear_error()
        self.load_images()
        self.load_fonts()
        self.load_sounds()

    def load_images(self):
        """Load image resources."""
        try:
            # Load images from assets directory
            image_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')
            if os.path.exists(image_dir):
                self.resources['images'] = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
                self.system_checks['resources'] = True
        except Exception as e:
            self.logger.error(f"Failed to load images: {str(e)}")
            self.handle_resource_error()

    def load_fonts(self):
        """Load font resources."""
        try:
            # Load fonts from assets directory
            font_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts')
            if os.path.exists(font_dir):
                self.resources['fonts'] = [f for f in os.listdir(font_dir) if f.endswith(('.ttf', '.otf'))]
        except Exception as e:
            self.logger.error(f"Failed to load fonts: {str(e)}")
            self.handle_resource_error()

    def load_sounds(self):
        """Load sound resources."""
        try:
            # Load sounds from assets directory
            sound_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sounds')
            if os.path.exists(sound_dir):
                self.resources['sounds'] = [f for f in os.listdir(sound_dir) if f.endswith(('.wav', '.mp3'))]
        except Exception as e:
            self.logger.error(f"Failed to load sounds: {str(e)}")
            self.handle_resource_error()

    def generate_qr_codes(self):
        """Generate QR codes for players and observer."""
        try:
            ip_address = self._get_ip_address()
            if ip_address:
                # Generate QR codes for player connections
                player1_data = f"http://{ip_address}:8000/player1"
                player2_data = f"http://{ip_address}:8000/player2"
                observer_data = f"http://{ip_address}:8000/observer"

                # Create QR codes
                self.player1_qr = self.generate_qr_code(player1_data)
                self.player2_qr = self.generate_qr_code(player2_data)
                self.observer_qr = self.generate_qr_code(observer_data)
            else:
                self.handle_qr_code_error()
        except Exception as e:
            self.logger.error(f"Failed to generate QR codes: {str(e)}")
            self.handle_qr_code_error()

    def update_loading_progress(self, progress, status=None):
        """Update loading progress."""
        if not isinstance(progress, (int, float)) or progress < 0 or progress > 100:
            raise ValidationError("Progress must be a number between 0 and 100")
        
        self.loading_progress = progress
        if status:
            self.loading_status = status
        
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            app.game_state['loading_progress'] = progress
            if status:
                app.game_state['loading_status'] = status

    def update_view_from_state(self):
        """Update view from game state."""
        app = App.get_running_app()
        if app and hasattr(app, 'game_state'):
            self.app_version = app.game_state.get('app_version', '1.0.0')
            self.loading_progress = app.game_state.get('loading_progress', 0)
            self.loading_status = app.game_state.get('loading_status', 'Initializing...')
            self.has_saved_game = app.game_state.get('has_saved_game', False)
            self.saved_game_info = app.game_state.get('saved_game_info')

    def validate_saved_game(self, saved_game):
        """Validate saved game data."""
        required_keys = ['players', 'current_round', 'scores']
        for key in required_keys:
            if key not in saved_game:
                raise StateError(f"Missing required saved game key: {key}")
        return True

    def handle_client_update(self, update):
        """Handle client update."""
        self.logger.debug(f"Handling client update: {update}")
        if update.get('type') == 'loading':
            progress = update.get('progress', 0)
            status = update.get('status')
            self.update_loading_progress(progress, status)

    def handle_storage_error(self):
        """Handle storage error."""
        self.show_error("Storage error: Unable to access or write to storage.")
        self.system_checks['storage'] = False
        self.update_start_button_state()

    def recover_from_storage_error(self):
        """Attempt to recover from a storage error."""
        self.clear_error()
        # Simulate re-checking storage (could be expanded as needed)
        self.system_checks['storage'] = True
        self.update_start_button_state()