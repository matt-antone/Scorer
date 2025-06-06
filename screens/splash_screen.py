from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import threading
import socket
import qrcode
from kivy.clock import Clock
import os


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


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
        
        # Start QR code generation in a background thread
        threading.Thread(target=self._generate_qr_codes_task, daemon=True).start()

    def _generate_qr_codes_task(self):
        """
        This runs in a background thread to avoid blocking the UI.
        """
        app = App.get_running_app()
        
        # Ensure the .cache directory exists
        cache_dir = os.path.dirname(app.p1_qr_path)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        ip = get_local_ip()
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
        """
        self.loading_indicator.opacity = 0
        self.start_button.opacity = 1
        self.start_button.disabled = False


    def transition_to_next_screen(self):
        """
        Called when the 'START' button is pressed.
        It retrieves the target screen from the app and tells the app to transition.
        """
        app = App.get_running_app()
        if app:
            target_screen = app.target_screen_after_splash
            print(f"SplashScreen: Button pressed, transitioning to '{target_screen}'")
            app.transition_from_splash(target_screen, 0) # Use the existing transition handler in the app

    def on_leave(self, *args):
        print("SplashScreen: on_leave called") 