from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty, BooleanProperty
from kivy.lang import Builder
from ..strings import UI_STRINGS

class ConnectionManagerPopup(Popup):
    """Popup for managing network connections."""

    title = StringProperty('Network Connection')
    is_open = BooleanProperty(False)
    connection_type = StringProperty('')
    ip_address = StringProperty('')
    error_message = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.6)
        self.auto_dismiss = False
        self.content = self._build_content()

    def _build_content(self):
        """Build popup content."""
        layout = BoxLayout(orientation='vertical', padding='20dp', spacing='10dp')

        # Status section
        status_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='100dp')
        self.status_label = Label(
            text='Checking network...',
            font_size='20sp',
            color=(1, 1, 1, 1)
        )
        status_layout.add_widget(self.status_label)

        # Connection info section
        info_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='100dp')
        self.connection_label = Label(
            text='',
            font_size='16sp',
            color=(1, 1, 1, 1)
        )
        self.ip_label = Label(
            text='',
            font_size='16sp',
            color=(1, 1, 1, 1)
        )
        info_layout.add_widget(self.connection_label)
        info_layout.add_widget(self.ip_label)

        # Error section
        error_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='50dp')
        self.error_label = Label(
            text='',
            font_size='16sp',
            color=(1, 0, 0, 1)
        )
        error_layout.add_widget(self.error_label)

        # Buttons section
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            spacing='10dp'
        )
        self.retry_button = Button(
            text='Retry',
            size_hint_x=0.5,
            on_release=self.on_retry
        )
        self.close_button = Button(
            text='Close',
            size_hint_x=0.5,
            on_release=self.on_close
        )
        button_layout.add_widget(self.retry_button)
        button_layout.add_widget(self.close_button)

        # Add all sections to main layout
        layout.add_widget(status_layout)
        layout.add_widget(info_layout)
        layout.add_widget(error_layout)
        layout.add_widget(button_layout)

        return layout

    def update_status(self, is_connected, connection_type='', ip_address='', error_message=''):
        """Update popup status."""
        self.is_open = True
        if is_connected:
            self.status_label.text = 'Connected'
            self.status_label.color = (0, 1, 0, 1)  # Green
            self.connection_label.text = f'Connection: {connection_type}'
            self.ip_label.text = f'IP Address: {ip_address}'
            self.error_label.text = ''
        else:
            self.status_label.text = 'Disconnected'
            self.status_label.color = (1, 0, 0, 1)  # Red
            self.connection_label.text = ''
            self.ip_label.text = ''
            self.error_label.text = error_message

    def on_retry(self, *args):
        """Handle retry button press."""
        if hasattr(self, 'on_retry_callback'):
            self.on_retry_callback()

    def on_close(self, *args):
        """Handle close button press."""
        self.is_open = False
        self.dismiss()

    def on_open(self):
        """Called when popup is opened."""
        self.is_open = True

    def on_dismiss(self):
        """Called when popup is dismissed."""
        self.is_open = False 