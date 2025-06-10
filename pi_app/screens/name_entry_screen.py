from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
import os

class NameEntryScreen(Screen):
    def __init__(self, **kwargs):
        kv_path = os.path.join(os.path.dirname(__file__), 'name_entry_screen.kv')
        Builder.load_file(kv_path)
        super().__init__(**kwargs)
        if not self.children:
            self.add_widget(Label(text='NameEntryScreen loaded (no KV)'))

    def submit_names(self):
        p1_name = self.ids.player1_name.text
        p2_name = self.ids.player2_name.text
        
        app = App.get_running_app()
        app.set_player_names(p1_name, p2_name)

        self.manager.current = 'deployment_setup'

    pass 