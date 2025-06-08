from kivy.app import App
from kivy.uix.screenmanager import Screen

class NameEntryScreen(Screen):
    def submit_names(self):
        p1_name = self.ids.player1_name.text
        p2_name = self.ids.player2_name.text
        
        app = App.get_running_app()
        app.set_player_names(p1_name, p2_name)

        self.manager.current = 'deployment_setup'

    pass 