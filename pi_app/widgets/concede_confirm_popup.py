from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

class ConcedeConfirmPopup(Popup):
    """Popup for confirming a player's concession."""
    
    def __init__(self, player_number, **kwargs):
        super().__init__(**kwargs)
        self.player_number = player_number
        
    def confirm_concede(self):
        """Called when the player confirms their concession."""
        app = App.get_running_app()
        app.handle_concession(self.player_number)
        self.dismiss() 