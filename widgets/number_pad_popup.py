from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty

class NumberPadPopup(Popup):
    input_box = ObjectProperty(None)
    callback = ObjectProperty(None)
    score_type = StringProperty('')
    
    def __init__(self, callback, score_type, initial_value=0, **kwargs):
        super(NumberPadPopup, self).__init__(**kwargs)
        self.callback = callback
        self.score_type = score_type
        self.title = f"Enter the updated {self.score_type} score"
        self.input_box.hint_text = str(initial_value)

    def on_button_press(self, button):
        """Appends the pressed button's text to the input box."""
        current_text = self.input_box.text
        new_text = current_text + button.text
        self.input_box.text = new_text

    def on_clear_press(self):
        """Clears the input box."""
        self.input_box.text = ""

    def on_ok_press(self):
        """Calls the callback with the entered value and dismisses the popup."""
        if self.input_box.text:
            value = int(self.input_box.text)
            self.callback(value)
        self.dismiss() 