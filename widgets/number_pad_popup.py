from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

class NumberPadPopup(Popup):
    def __init__(self, caller_widget, **kwargs):
        super().__init__(**kwargs)
        self.auto_dismiss = False # Prevent auto-dismissal on outside click
        self.caller_widget = caller_widget 
        self.title = "Enter Score"
        self.caller_info = kwargs.pop('caller_info', {'player_id': 1, 'score_type': 'primary'}) 
        self.entered_value = "" 
        self.content_layout = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(5))
        
        self.display = Label(text="0", font_size='24sp', size_hint_y=None, height=dp(40))
        self.content_layout.add_widget(self.display)
        
        grid = GridLayout(cols=3, spacing=dp(5))
        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            'C', '0', 'Ent'
        ]
        for btn_text in buttons:
            button = Button(text=btn_text, font_size='20sp', on_press=self.on_button_press)
            grid.add_widget(button)
            
        self.content_layout.add_widget(grid)
        self.content = self.content_layout
        self.size_hint = (None, None)
        self.size = (dp(250), dp(350))

    def on_button_press(self, instance):
        if instance.text == 'C':
            self.entered_value = ""
        elif instance.text == 'Ent':
            score = 0 
            if self.entered_value:
                try:
                    score = int(self.entered_value)
                except ValueError:
                    self.entered_value = "Error" 
                    self.display.text = self.entered_value
                    return 
            player_id = self.caller_info.get('player_id', 1) 
            score_type = self.caller_info.get('score_type', 'primary')
            self.caller_widget.process_numpad_value(score, player_id, score_type)
            self.dismiss()
        else: 
            if len(self.entered_value) < 3: 
                self.entered_value += instance.text
        self.display.text = self.entered_value if self.entered_value else "0" 