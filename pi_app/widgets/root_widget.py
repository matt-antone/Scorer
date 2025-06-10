from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import FadeTransition

class ScorerRootWidget(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(transition=FadeTransition(), **kwargs)
    pass 