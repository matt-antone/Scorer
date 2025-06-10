from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
import logging

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
        self.input_box.text = ""  # Start with empty text
        logging.info(f"NumberPadPopup initialized with callback: {callback}, score_type: {score_type}, initial_value: {initial_value}")

    def on_button_press(self, button):
        """Handle button presses in the number pad."""
        logging.info(f"Button pressed: {button.text}")
        if button.text == 'C':
            self.input_box.text = ""
            logging.info("Cleared input box")
        elif button.text == 'OK':
            if self.input_box.text:
                try:
                    value = int(self.input_box.text)
                    logging.info(f"OK pressed with value: {value}, calling callback")
                    if self.callback:
                        self.callback(value)
                    else:
                        logging.error("No callback set for NumberPadPopup")
                except ValueError:
                    logging.error(f"Invalid number in input box: {self.input_box.text}")
            else:
                logging.info("OK pressed with empty input box")
            self.dismiss()
        elif button.text.isdigit():  # Only append if it's a digit
            current_text = self.input_box.text
            new_text = current_text + button.text
            self.input_box.text = new_text
            logging.info(f"Appended digit {button.text}, new text: {new_text}") 