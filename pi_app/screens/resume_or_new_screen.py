from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
import logging
import os

class ResumeOrNewScreen(Screen):
    def __init__(self, **kwargs):
        kv_path = os.path.join(os.path.dirname(__file__), 'resume_or_new_screen.kv')
        Builder.load_file(kv_path)
        super().__init__(**kwargs)
        if not self.children:
            self.add_widget(Label(text='ResumeOrNewScreen loaded (no KV)'))

    def resume_game(self):
        logging.info("Resuming game")
        app = App.get_running_app()
        if app:
            # Set phase to game_play and go to main game screen
            app.game_state['game_phase'] = 'game_play'
            app.save_game_state()
            logging.info("Transitioning to scoreboard screen")
            self.manager.current = 'scoreboard'
        else:
            logging.error("No running app found")

    def start_new_game(self):
        logging.info("Starting new game")
        app = App.get_running_app()
        if app:
            app.initialize_game_state()
            logging.info("Transitioning to name entry screen")
            self.manager.current = 'name_entry'
        else:
            logging.error("No running app found") 