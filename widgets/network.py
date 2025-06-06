from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
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
from network_utils import is_raspberry_pi, scan_wifi_networks, connect_to_wifi

# --- Popup Classes moved from screens/splash_screen.py ---

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