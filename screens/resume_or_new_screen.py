from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class ResumeOrNewScreen(Screen):
    resume_info_label = ObjectProperty(None)
    resume_button = ObjectProperty(None)
    new_game_button = ObjectProperty(None)

    def on_enter(self, *args):
        # Optional: Update the label text with more specific info if needed
        app = App.get_running_app()
        phase = app.game_state.get('game_phase')
        p1_name = app.game_state.get('player1', {}).get('name', 'P1')
        p2_name = app.game_state.get('player2', {}).get('name', 'P2')
        self.resume_info_label.text = f"Found saved game for {p1_name} vs {p2_name} in phase '{phase}'. Resume?"

    def resume_game_action(self):
        app = App.get_running_app()
        target_screen = app._get_screen_for_phase(app.game_state.get('game_phase'))
        app.switch_screen(target_screen)

    def start_new_game_from_resume_screen_action(self):
        app = App.get_running_app()
        app.start_new_game_flow() 