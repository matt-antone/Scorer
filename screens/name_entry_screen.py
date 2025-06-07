import platform

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.vkeyboard import VKeyboard

# Behavor of this screen:
# 1. When the screen is entered, the names of the players are displayed in the input fields.
# 2. When the user taps on an input field, the virtual keyboard is displayed. if on Linux, and the virtual keyboard is not already displayed, then display it.
# 3. When the user taps on the continue button, the names of the players are saved and the game starts.
# 4. continue button is always enabled.

class NameEntryScreen(Screen):
    player1_name_input = ObjectProperty(None)
    player2_name_input = ObjectProperty(None)
    continue_button = ObjectProperty(None)
    active_input = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vkeyboard = None
        self._is_initialized = False
        # Bind to the properties to know when they are available from KV
        self.bind(
            player1_name_input=self._check_and_initialize,
            player2_name_input=self._check_and_initialize,
            continue_button=self._check_and_initialize
        )

    def _check_and_initialize(self, instance, value):
        """
        This method is called when any of the bound properties are set.
        It checks if all necessary widgets are available before running
        the main initialization logic for the screen.
        """
        if self.player1_name_input and self.player2_name_input and self.continue_button:
            if not self._is_initialized:
                self._is_initialized = True
                self._initialize_screen()

    def _initialize_screen(self):
        """
        Runs once all widgets are confirmed to be available.
        Populates fields and sets up bindings.
        """
        app = App.get_running_app()
        p1_name = app.game_state.get('player_1', {}).get('name', 'Player 1')
        p2_name = app.game_state.get('player_2', {}).get('name', 'Player 2')

        self.player1_name_input.text = p1_name
        self.player2_name_input.text = p2_name

    def set_active_input(self, text_input):
        if text_input.focus:
            # text_input.text = '' # This was causing an infinite loop
            self.active_input = text_input
            if platform.system() == "Linux" and not self.vkeyboard:
                self.vkeyboard = VKeyboard()
                self.add_widget(self.vkeyboard)
            if self.vkeyboard:
                self.vkeyboard.target = text_input
        else:
            if self.active_input == text_input:
                self.active_input = None
                if self.vkeyboard:
                    self.remove_widget(self.vkeyboard)
                    self.vkeyboard = None

    def on_touch_down(self, touch):
        # If a touch occurs outside the active text input and the keyboard, unfocus it.
        if self.active_input and not self.active_input.collide_point(*touch.pos):
            if not self.vkeyboard or not self.vkeyboard.collide_point(*touch.pos):
                self.active_input.focus = False
        return super().on_touch_down(touch)

    def save_names_and_proceed(self):
        app = App.get_running_app()
        app.set_player_name(1, self.player1_name_input.text.strip())
        app.set_player_name(2, self.player2_name_input.text.strip())
        app.start_deployment_phase() 