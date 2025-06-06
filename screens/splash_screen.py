from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
import threading
import socket
import qrcode
from kivy.clock import Clock
import os
from network_utils import is_raspberry_pi, get_local_ip, check_network_connection, scan_wifi_networks, connect_to_wifi
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout as KivyRecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.image import Image

# --- Popup Classes moved from main.py ---

class SelectableGridLayout(FocusBehavior, KivyRecycleBoxLayout):
    ''' Adds selection and focus behaviour to the RecycleBoxLayout. '''
    pass

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
            rv.parent.parent.parent.selected_ssid = rv.data[index]['text']


class WifiRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(WifiRecycleView, self).__init__(**kwargs)
        self.data = [{'text': str(i)} for i in range(100)]


class ConnectPopup(Popup):
    selected_ssid = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Client Connection Info"
        self.size_hint = (0.9, 0.9)

        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        if is_raspberry_pi():
            main_layout.add_widget(self._create_pi_network_manager())
        else:
            main_layout.add_widget(self._create_standard_qr_display())

        # Always add a close button
        close_button = Button(text="Close", size_hint_y=None, height=dp(50))
        close_button.bind(on_press=self.dismiss)
        main_layout.add_widget(close_button)

        self.content = main_layout

    def _create_standard_qr_display(self):
        app = App.get_running_app()
        grid = GridLayout(cols=3, spacing=dp(10))
        # Observer, P1, P2 QR code display (as implemented before)
        # Observer Client
        observer_box = BoxLayout(orientation='vertical')
        observer_box.add_widget(Label(text="Observer Client", font_size='18sp'))
        observer_qr = Image(source=app.observer_qr_path)
        observer_box.add_widget(observer_qr)
        grid.add_widget(observer_box)

        # Player 1 Client
        p1_box = BoxLayout(orientation='vertical')
        p1_box.add_widget(Label(text="Player 1 Client", font_size='18sp'))
        p1_qr = Image(source=app.p1_qr_path)
        p1_box.add_widget(p1_qr)
        grid.add_widget(p1_box)

        # Player 2 Client
        p2_box = BoxLayout(orientation='vertical')
        p2_box.add_widget(Label(text="Player 2 Client", font_size='18sp'))
        p2_qr = Image(source=app.p2_qr_path)
        p2_box.add_widget(p2_qr)
        grid.add_widget(p2_box)
        return grid

    def _create_pi_network_manager(self):
        pi_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        
        # Header
        pi_layout.add_widget(Label(text="Raspberry Pi Network Manager", font_size='20sp', size_hint_y=None, height=dp(30)))

        # Network List
        rv = WifiRecycleView()
        rv.viewclass = SelectableLabel
        # placeholder data
        networks = scan_wifi_networks()
        rv.data = [{'text': net} for net in networks]
        pi_layout.add_widget(rv)

        # Password Input
        password_input = TextInput(hint_text='Password', password=True, size_hint_y=None, height=dp(40))
        pi_layout.add_widget(password_input)

        # Connect Button
        connect_button = Button(text="Connect", size_hint_y=None, height=dp(50))
        connect_button.bind(on_press=lambda x: self.attempt_pi_connection(self.selected_ssid, password_input.text))
        pi_layout.add_widget(connect_button)
        
        return pi_layout
        
    def attempt_pi_connection(self, ssid, password):
        if not ssid:
            print("No network selected.")
            return
        print(f"Attempting to connect to {ssid}...")
        success, message = connect_to_wifi(ssid, password)
        print(message)
        if success:
            # Optionally, we can auto-close the popup and regenerate QR codes
            self.dismiss()

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