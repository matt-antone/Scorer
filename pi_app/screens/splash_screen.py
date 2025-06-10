from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import BooleanProperty, StringProperty
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

logger = logging.getLogger(__name__)

class SplashScreen(Screen):
    start_enabled = BooleanProperty(False)
    status_text = StringProperty('Initializing...')
    qr_code_path = StringProperty('')
    show_loading = BooleanProperty(False)

    def __init__(self, **kwargs):
        logger.info("SplashScreen: Initializing")
        # Explicitly load the KV file
        kv_path = os.path.join(os.path.dirname(__file__), 'splash_screen.kv')
        Builder.load_file(kv_path)
        super().__init__(**kwargs)
        # Fallback label if KV fails
        if not self.children:
            self.add_widget(Label(text='SplashScreen loaded (no KV)'))
        
        # Schedule background tasks
        logger.info("SplashScreen: Scheduling background tasks")
        Clock.schedule_once(self._start_background_tasks)
    
    def _start_background_tasks(self, dt):
        """Start background tasks in a separate thread"""
        logger.info("SplashScreen: Starting background tasks")
        self.show_loading = True
        threading.Thread(target=self._perform_background_tasks, daemon=True).start()
    
    def _perform_background_tasks(self):
        """Perform all background tasks"""
        try:
            # Check network
            logger.info("SplashScreen: Checking network")
            if not self._check_network():
                Clock.schedule_once(lambda dt: self._update_status("No network connection"))
                Clock.schedule_once(lambda dt: setattr(self, 'show_loading', False))
                return
            
            # Get IP address
            logger.info("SplashScreen: Getting IP address")
            ip_address = self._get_ip_address()
            if not ip_address:
                Clock.schedule_once(lambda dt: self._update_status("Could not get IP address"))
                Clock.schedule_once(lambda dt: setattr(self, 'show_loading', False))
                return
            
            # Generate QR codes
            logger.info("SplashScreen: Generating QR codes")
            if not self._generate_qr_codes(ip_address):
                Clock.schedule_once(lambda dt: self._update_status("Failed to generate QR codes"))
                Clock.schedule_once(lambda dt: setattr(self, 'show_loading', False))
                return
            
            # All tasks complete
            logger.info("SplashScreen: All tasks complete")
            Clock.schedule_once(lambda dt: self._update_status("Ready"))
            Clock.schedule_once(lambda dt: setattr(self, 'show_loading', False))
            Clock.schedule_once(lambda dt: setattr(self, 'start_enabled', True))
            
        except Exception as e:
            logger.error(f"SplashScreen: Error in background tasks: {str(e)}")
            Clock.schedule_once(lambda dt: self._update_status("Error during initialization"))
            Clock.schedule_once(lambda dt: setattr(self, 'show_loading', False))
    
    def _update_status(self, text):
        self.status_text = text
    
    def _check_network(self):
        """Check if network is available"""
        try:
            # Try to connect to a reliable host
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            logger.info("SplashScreen: Network check successful")
            return True
        except OSError:
            logger.warning("SplashScreen: Network check failed")
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
            
            return True
            
        except Exception as e:
            logger.error(f"SplashScreen: Error generating QR codes: {str(e)}")
            return False
    
    def on_start_button(self):
        logger.info("SplashScreen: Start button pressed")
        app = App.get_running_app()
        if app:
            logger.info("SplashScreen: Calling after_splash()")
            app.after_splash()
        else:
            logger.error("SplashScreen: No running app found") 