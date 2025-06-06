from kivy.app import App
from kivy.uix.screenmanager import Screen


class SplashScreen(Screen):
    def transition_to_next_screen(self):
        """
        Called when the 'START' button is pressed.
        It retrieves the target screen from the app and tells the app to transition.
        """
        app = App.get_running_app()
        if app:
            target_screen = app.target_screen_after_splash
            print(f"SplashScreen: Button pressed, transitioning to '{target_screen}'")
            app.transition_from_splash(target_screen, 0) # Use the existing transition handler in the app

    def on_leave(self, *args):
        print("SplashScreen: on_leave called") 