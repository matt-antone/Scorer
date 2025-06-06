from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import threading
import qrcode
from kivy.clock import Clock
import os
from network_utils import is_raspberry_pi, get_local_ip, check_network_connection
from kivy.core.image import Image as CoreImage
from widgets.network import ConnectPopup

class SplashScreen(Screen):
    loading_indicator = ObjectProperty(None)
    start_button = ObjectProperty(None)

    def on_enter(self, *args):
        # Ensure widgets are mapped from .kv file
        if not self.ids:
            return

        self.loading_indicator = self.ids.loading_indicator
        self.start_button = self.ids.start_button

        self.start_button.opacity = 0
        self.start_button.disabled = True
        self.loading_indicator.opacity = 1
        
        # Start network check in a background thread
        if is_raspberry_pi():
            self.loading_indicator.text = 'Checking network connection...'
            threading.Thread(target=self._check_network_task, daemon=True).start()
        else:
            self.loading_indicator.text = 'Generating QR Codes...'
            threading.Thread(target=self._generate_qr_codes_task, daemon=True).start()

    def _check_network_task(self):
        is_connected, ip = check_network_connection()
        if is_connected:
            Clock.schedule_once(lambda dt: setattr(self.loading_indicator, 'text', 'Network connected. Generating QR Codes...'))
            self._generate_qr_codes_task(ip_address=ip)
        else:
            Clock.schedule_once(self._open_connect_popup)

    def _open_connect_popup(self, dt):
        popup = ConnectPopup()
        popup.bind(on_dismiss=self._on_connect_popup_dismiss)
        popup.open()

    def _on_connect_popup_dismiss(self, instance):
        self.loading_indicator.text = 'Re-checking network connection...'
        threading.Thread(target=self._check_network_task, daemon=True).start()

    def _generate_qr_codes_task(self, ip_address=None):
        """
        This runs in a background thread to avoid blocking the UI.
        """
        app = App.get_running_app()
        
        # Ensure the .cache directory exists
        cache_dir = os.path.dirname(app.p1_qr_path)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        ip = ip_address or get_local_ip()
        port = 6969
        
        # Observer
        observer_url = f"http://{ip}:{port}/"
        observer_qr_img = qrcode.make(observer_url)
        observer_qr_img.save(app.observer_qr_path)

        # Player 1
        p1_url = f"http://{ip}:{port}/p1"
        p1_qr_img = qrcode.make(p1_url)
        p1_qr_img.save(app.p1_qr_path)

        # Player 2
        p2_url = f"http://{ip}:{port}/p2"
        p2_qr_img = qrcode.make(p2_url)
        p2_qr_img.save(app.p2_qr_path)
        
        # Once done, schedule the UI update on the main thread
        Clock.schedule_once(self._on_qr_codes_generated)

    def _on_qr_codes_generated(self, dt):
        """
        This runs on the main Kivy thread to safely update the UI.
        It pre-loads the QR code images and updates the widgets on the next screen.
        """
        app = App.get_running_app()

        # Step 1: Pre-load the images into Kivy's cache to ensure they are ready.
        CoreImage(app.p1_qr_path).texture
        CoreImage(app.p2_qr_path).texture
        CoreImage(app.observer_qr_path).texture

        # Step 2: Get the NameEntryScreen and update its Image widgets directly.
        name_entry_screen = app.root.get_screen('name_entry')
        if name_entry_screen.p1_qr_code:
            name_entry_screen.p1_qr_code.source = app.p1_qr_path
            name_entry_screen.p1_qr_code.reload()
        if name_entry_screen.p2_qr_code:
            name_entry_screen.p2_qr_code.source = app.p2_qr_path
            name_entry_screen.p2_qr_code.reload()
        
        # Step 3: Now that everything is loaded, show the start button.
        self.loading_indicator.opacity = 0
        self.start_button.opacity = 1
        self.start_button.disabled = False


    def transition_to_next_screen(self, *args):
        app = App.get_running_app()
        if app:
            target_screen = app.target_screen_after_splash
            print(f"SplashScreen: Button pressed, transitioning to '{target_screen}'")
            app.transition_from_splash(target_screen, 0) # Use the existing transition handler in the app

    def on_leave(self, *args):
        print("SplashScreen: on_leave called") 