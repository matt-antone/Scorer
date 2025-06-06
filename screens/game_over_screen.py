from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class GameOverScreen(Screen):
    result_status_label = ObjectProperty(None)
    p1_final_name_label = ObjectProperty(None)
    p1_final_score_label = ObjectProperty(None)
    p1_final_cp_label = ObjectProperty(None)
    p1_final_time_label = ObjectProperty(None)
    p1_role_label = ObjectProperty(None)
    p2_final_name_label = ObjectProperty(None)
    p2_final_score_label = ObjectProperty(None)
    p2_final_cp_label = ObjectProperty(None)
    p2_final_time_label = ObjectProperty(None)
    p2_role_label = ObjectProperty(None)
    total_game_time_label = ObjectProperty(None)
    rounds_played_label = ObjectProperty(None)
    exit_button = ObjectProperty(None)

    def on_pre_enter(self, *args):
        gs = App.get_running_app().game_state
        
        # Use .get() for safe access to potentially missing keys
        p1_stats = gs.get('player1', {})
        p2_stats = gs.get('player2', {})
        timer_stats = gs.get('game_timer', {})

        winner_text = ""
        raw_status_message = gs.get("status_message", "Game Over")
        status_message_lower = raw_status_message.lower()
        print(f"GameOverScreen.on_pre_enter: Raw status_message from game_state: '{raw_status_message}'")

        p1_score = p1_stats.get('total_score', 0)
        p2_score = p2_stats.get('total_score', 0)

        if "concedes." in status_message_lower and "wins!" in status_message_lower:
            winner_text = raw_status_message
            print(f"GameOverScreen: Detected concession. Winner text set to: '{winner_text}'")
        else:
            p1_name = p1_stats.get('name', 'Player 1')
            p2_name = p2_stats.get('name', 'Player 2')
            if p1_score > p2_score:
                winner_text = f"{p1_name} Wins by Score!"
            elif p2_score > p1_score:
                winner_text = f"{p2_name} Wins by Score!"
            else:
                winner_text = "It's a Tie by Score!"
            print(f"GameOverScreen: Determined winner by score. P1: {p1_score}, P2: {p2_score}. Winner text: '{winner_text}'")
        
        if self.result_status_label: self.result_status_label.text = winner_text
        
        # Populate Player 1 Stats safely
        if self.p1_final_name_label: self.p1_final_name_label.text = f"{p1_stats.get('name', 'P1')}"
        if self.p1_final_score_label: self.p1_final_score_label.text = f"{p1_score}"
        if self.p1_final_cp_label: self.p1_final_cp_label.text = f"CP: {p1_stats.get('cp', 0)}"
        if self.p1_final_time_label: self.p1_final_time_label.text = f"{p1_stats.get('player_time_display', '00:00:00')}"

        # Populate Player 2 Stats safely
        if self.p2_final_name_label: self.p2_final_name_label.text = f"{p2_stats.get('name', 'P2')}"
        if self.p2_final_score_label: self.p2_final_score_label.text = f"{p2_score}"
        if self.p2_final_cp_label: self.p2_final_cp_label.text = f"CP: {p2_stats.get('cp', 0)}"
        if self.p2_final_time_label: self.p2_final_time_label.text = f"{p2_stats.get('player_time_display', '00:00:00')}"

        # Populate Game Stats safely
        if self.total_game_time_label: self.total_game_time_label.text = f"Total Game Time: {timer_stats.get('elapsed_display', '00:00:00')}"
        if self.rounds_played_label: self.rounds_played_label.text = f"Rounds Played: {gs.get('last_round_played', 5)}"

        attacker_id = gs.get('deployment_attacker_id')
        p1_role = "Attacker" if attacker_id == 1 else "Defender"
        p2_role = "Attacker" if attacker_id == 2 else "Defender"

        self.p1_role_label.text = p1_role
        self.p2_role_label.text = p2_role

    def start_new_game(self):
        app = App.get_running_app()
        app.start_new_game_flow()

    def exit_app_from_game_over(self):
        App.get_running_app().stop() 