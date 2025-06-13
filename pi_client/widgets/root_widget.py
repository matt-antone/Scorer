from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class ScorerRootWidget(BoxLayout):
    """Root widget for the Scorer application."""
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(transition=FadeTransition(), **kwargs)
    pass 