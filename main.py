from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.config import Config

# Configure the window to be a fixed size, simulating the Pi screen for now
# We can make this more dynamic or fullscreen later.
Config.set('graphics', 'width', '800') # Typical 5-inch screen resolution might be 800x480
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', False) # Change to True if you want to resize on desktop

class ScorerRootWidget(BoxLayout):
    """
    The root widget for the Scorer application.
    This will eventually hold all other UI elements.
    """
    def __init__(self, **kwargs):
        super(ScorerRootWidget, self).__init__(**kwargs)
        # The actual layout will be defined in scorer.kv
        pass

class ScorerApp(App):
    """
    The main Kivy application class for Scorer.
    """
    def build(self):
        # Kivy will automatically look for a .kv file named after the app class
        # in lowercase, without "App" -> scorer.kv
        return ScorerRootWidget()

if __name__ == '__main__':
    ScorerApp().run() 