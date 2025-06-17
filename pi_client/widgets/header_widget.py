from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
from .gear_button import GearButton

class HeaderWidget(BoxLayout):
    title = StringProperty('')

    def __init__(self, **kwargs):
        self.register_event_type('on_settings')
        super().__init__(**kwargs)
        self.bind(title=self._on_title)

    def _on_title(self, instance, value):
        """Called when the title property changes."""
        if not value:
            self.title = 'Warhammer 40k Scoreboard'

    def on_settings(self, *args):
        pass 