import time

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from widgets.number_pad_popup import NumberPadPopup


class ScorerRootWidget(Screen):
    # Header elements from KV
    header_round_label = ObjectProperty(None)
    header_total_time_label = ObjectProperty(None)

    # Player 1 elements from KV
    p1_name_label = ObjectProperty(None)
    p1_score_label = ObjectProperty(None)
    p1_cp_label = ObjectProperty(None)
    p1_player_timer_label = ObjectProperty(None)
    p1_end_turn_button = ObjectProperty(None)
    p1_concede_button = ObjectProperty(None)

    # Player 2 elements from KV
    p2_name_label = ObjectProperty(None)
    p2_score_label = ObjectProperty(None)
    p2_cp_label = ObjectProperty(None)
    p2_player_timer_label = ObjectProperty(None)
    p2_end_turn_button = ObjectProperty(None)
    p2_concede_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numpad_popup = None

    def on_pre_enter(self, *args):
        """Ensure UI and timers are correctly initialized when entering the screen."""
        self.update_ui_from_state() # Initial UI setup from state
        
        gs = App.get_running_app().game_state
        if gs.get('game_phase') == 'game_play':
            if gs.get('game_timer', {}).get('status') == 'running':
                # If state says running, make sure the clock is scheduled.
                is_scheduled = False
                for event in Clock.get_events():
                    if event.callback == self.update_timer_display:
                        is_scheduled = True
                        break
                if not is_scheduled:
                    Clock.schedule_interval(self.update_timer_display, 1)
            else:
                # If game is playing but state says timer is stopped, start it.
                self.start_timer()

        # Final check to ensure UI is updated after a short delay
        Clock.schedule_once(lambda dt: self.update_ui_from_state(), 0.05)

    def update_ui_from_state(self):
        print("ScorerRootWidget: Attempting update_ui_from_state")
        gs = App.get_running_app().game_state

        # Enhanced widget readiness check
        required_widgets = {
            "header_round_label": self.header_round_label,
            "p1_name_label": self.p1_name_label,
            "p1_score_label": self.p1_score_label,
            "p1_cp_label": self.p1_cp_label,
            "p2_name_label": self.p2_name_label,
            "p2_score_label": self.p2_score_label,
            "p2_cp_label": self.p2_cp_label,
            "p1_end_turn_button": self.p1_end_turn_button,
            "p2_end_turn_button": self.p2_end_turn_button,
            "header_total_time_label": self.header_total_time_label,
            "p1_player_timer_label": self.p1_player_timer_label,
            "p2_player_timer_label": self.p2_player_timer_label,
            "p1_concede_button": self.p1_concede_button,
            "p2_concede_button": self.p2_concede_button
        }
        all_ready = True
        for name, widget_ref in required_widgets.items():
            if not widget_ref:
                print(f"ScorerRootWidget: Widget '{name}' not ready yet.")
                all_ready = False
        
        if not all_ready:
            Clock.schedule_once(lambda dt: self.update_ui_from_state(), 0.05) # Increased delay slightly
            print("ScorerRootWidget: Rescheduling update_ui_from_state due to missing widgets.")
            return
        
        print(f"ScorerRootWidget: game_phase = {gs.get('game_phase')}, active_player_id = {gs.get('active_player_id')}")

        # Updated player name logic
        p1_base_name = gs['player1']['name']
        p2_base_name = gs['player2']['name']

        if gs['game_phase'] == "game_play":
            if gs["active_player_id"] == 1:
                self.p1_name_label.text = f"{p1_base_name} - Active"
                self.p2_name_label.text = p2_base_name
            elif gs["active_player_id"] == 2:
                self.p1_name_label.text = p1_base_name
                self.p2_name_label.text = f"{p2_base_name} - Active"
            else: # Should not happen often if game is playing, but for robustness
                self.p1_name_label.text = p1_base_name
                self.p2_name_label.text = p2_base_name
        else: # Not playing (e.g. game over, setup)
            self.p1_name_label.text = p1_base_name
            self.p2_name_label.text = p2_base_name
        
        self.p1_score_label.text = str(gs['player1']['total_score'])
        self.p1_cp_label.text = f"Command Points: {gs['player1']['cp']}"
        self.p2_score_label.text = str(gs['player2']['total_score'])
        self.p2_cp_label.text = f"Command Points: {gs['player2']['cp']}"

        # Manage End Turn button visibility and state
        current_gs_active_id = gs.get("active_player_id") # Capture it for this specific decision block
        print(f"ScorerRootWidget.update_ui_from_state: ButtonLogic using active_player_id = {current_gs_active_id} for button visibility.")

        is_playing = gs['game_phase'] == "game_play"
        
        # Player 1 Button
        if is_playing and current_gs_active_id == 1:
            self.p1_end_turn_button.opacity = 1
            self.p1_end_turn_button.disabled = False
        else:
            self.p1_end_turn_button.opacity = 0
            self.p1_end_turn_button.disabled = True
        
        # Player 2 Button
        if is_playing and current_gs_active_id == 2:
            self.p2_end_turn_button.opacity = 1
            self.p2_end_turn_button.disabled = False
        else:
            self.p2_end_turn_button.opacity = 0
            self.p2_end_turn_button.disabled = True
        
        print(f"ScorerRootWidget: p1_end_turn_button.opacity={self.p1_end_turn_button.opacity}, .disabled={self.p1_end_turn_button.disabled}")
        print(f"ScorerRootWidget: p2_end_turn_button.opacity={self.p2_end_turn_button.opacity}, .disabled={self.p2_end_turn_button.disabled}")

        # Manage Concede button visibility and state
        if is_playing:
            self.p1_concede_button.opacity = 1
            self.p1_concede_button.disabled = False
            self.p2_concede_button.opacity = 1
            self.p2_concede_button.disabled = False
        else:
            self.p1_concede_button.opacity = 0
            self.p1_concede_button.disabled = True
            self.p2_concede_button.opacity = 0
            self.p2_concede_button.disabled = True

        if gs['game_phase'] == "game_play":
            self.header_round_label.text = f"Round {gs['current_round']}"
        elif gs['game_phase'] == "game_over":
            final_round = gs.get('last_round_played', 5)
            self.header_round_label.text = f"Round {final_round} (Game Over)"
        else: 
            self.header_round_label.text = "Round: -"
        print("ScorerRootWidget: update_ui_from_state completed.")

    def start_timers_and_ui(self):
        """A single method to call when transitioning to this screen to ensure UI and timers are correctly initialized."""
        self.update_ui_from_state() # Initial UI setup from state
        
        gs = App.get_running_app().game_state
        if gs.get('game_phase') == 'game_play':
            if gs.get('game_timer', {}).get('status') == 'running':
                # If state says running, make sure the clock is scheduled.
                is_scheduled = False
                for event in Clock.get_events():
                    if event.callback == self.update_timer_display:
                        is_scheduled = True
                        break
                if not is_scheduled:
                    Clock.schedule_interval(self.update_timer_display, 1)
            else:
                # If game is playing but state says timer is stopped, start it.
                self.start_timer()

        # Final check to ensure UI is updated after a short delay, as widgets might not be ready instantly.
        Clock.schedule_once(lambda dt: self.update_ui_from_state(), 0.05)

    def start_timer(self):
        gs = App.get_running_app().game_state
        if gs['game_timer']['status'] == 'stopped':
            time_now = time.time()
            gs['game_timer']['start_time'] = time_now
            gs['game_timer']['turn_segment_start_time'] = time_now
            gs['game_timer']['status'] = 'running'
            Clock.schedule_interval(self.update_timer_display, 1)
            print("Timer started.")
            self.update_timer_display(0)

    def stop_timer(self):
        gs = App.get_running_app().game_state
        if gs['game_timer']['status'] == 'running':
            gs['game_timer']['status'] = 'stopped'
            Clock.unschedule(self.update_timer_display)
            self.update_timer_display(0) 
            print("Timer stopped.")

    def _format_seconds_to_hms(self, total_seconds):
        total_seconds = int(total_seconds)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def update_timer_display(self, dt): 
        gs = App.get_running_app().game_state
        time_now = time.time()
        active_player_id = gs.get("active_player_id")
        game_status = gs['game_timer']['status']
        game_phase = gs['game_phase']

        # print(f"update_timer_display: active_id={active_player_id}, timer_status={game_status}, game_phase={game_phase}") # Basic log

        if game_status == 'running':
            elapsed_seconds = time_now - gs['game_timer']['start_time']
            gs['game_timer']['elapsed_display'] = self._format_seconds_to_hms(elapsed_seconds)
        
        if self.header_total_time_label: # Check if property is bound
            self.header_total_time_label.text = f"Total Time: {gs['game_timer']['elapsed_display']}"

        current_segment_duration = 0
        if game_status == 'running' and game_phase == 'game_play':
             current_segment_duration = time_now - gs['game_timer']['turn_segment_start_time']

        # Player 1 Timer Update
        p1_key = "player1"
        p1_total_seconds = gs[p1_key]['player_elapsed_time_seconds']
        if active_player_id == 1 and game_status == 'running' and game_phase == 'game_play':
            live_total_seconds_p1 = p1_total_seconds + current_segment_duration
            gs[p1_key]['player_time_display'] = self._format_seconds_to_hms(live_total_seconds_p1)
            # print(f"  P1 (Active) timer: base={p1_total_seconds:.2f}, seg_dur={current_segment_duration:.2f}, live_total={live_total_seconds_p1:.2f}")
        else:
            gs[p1_key]['player_time_display'] = self._format_seconds_to_hms(p1_total_seconds)
            # if game_phase == 'playing': print(f"  P1 (Inactive) timer: base={p1_total_seconds:.2f}")

        if self.p1_player_timer_label: 
            self.p1_player_timer_label.text = f"{gs[p1_key]['player_time_display']}"

        # Player 2 Timer Update
        p2_key = "player2"
        p2_total_seconds = gs[p2_key]['player_elapsed_time_seconds']
        if active_player_id == 2 and game_status == 'running' and game_phase == 'game_play':
            live_total_seconds_p2 = p2_total_seconds + current_segment_duration
            gs[p2_key]['player_time_display'] = self._format_seconds_to_hms(live_total_seconds_p2)
            # print(f"  P2 (Active) timer: base={p2_total_seconds:.2f}, seg_dur={current_segment_duration:.2f}, live_total={live_total_seconds_p2:.2f}")
        else:
            gs[p2_key]['player_time_display'] = self._format_seconds_to_hms(p2_total_seconds)
            # if game_phase == 'playing': print(f"  P2 (Inactive) timer: base={p2_total_seconds:.2f}")
            
        if self.p2_player_timer_label: 
            self.p2_player_timer_label.text = f"{gs[p2_key]['player_time_display']}"

    def end_turn(self):
        gs = App.get_running_app().game_state
        print(f"--- End Turn Button Pressed ---")
        print(f"Initial state: active_player_id={gs.get('active_player_id')}, game_phase={gs.get('game_phase')}, round={gs.get('current_round')}")

        if gs["game_phase"] != "game_play":
            print("End Turn: Game not in 'playing' phase. No action.")
            return

        time_now = time.time()
        outgoing_player_id = gs["active_player_id"]
        print(f"End Turn: Outgoing player_id = {outgoing_player_id}")
        
        if gs['game_timer']['status'] == 'running':
            turn_duration = time_now - gs['game_timer']['turn_segment_start_time']
            gs[f'player{outgoing_player_id}']['player_elapsed_time_seconds'] += turn_duration
            gs[f'player{outgoing_player_id}']['player_time_display'] = self._format_seconds_to_hms(
                gs[f'player{outgoing_player_id}']['player_elapsed_time_seconds']
            )
            print(f"End Turn: Player {outgoing_player_id} turn_duration={turn_duration:.2f}s, total_elapsed={gs[f'player{outgoing_player_id}']['player_elapsed_time_seconds']:.2f}s")

        next_player_id = 2 if outgoing_player_id == 1 else 1
        gs["active_player_id"] = next_player_id
        print(f"End Turn: Active player_id changed to {gs['active_player_id']}")
        newly_active_player_name = gs[f'player{gs["active_player_id"]}']["name"]

        first_player_of_game_id = gs.get("first_player_of_game_id")
        is_second_player_turn_end = (first_player_of_game_id is not None and outgoing_player_id != first_player_of_game_id)

        # Game Over Check: This is the absolute end condition.
        if gs["current_round"] == 5 and is_second_player_turn_end:
            gs["game_phase"] = "game_over"
            gs["last_round_played"] = 5
            gs["status_message"] = "Game Over - Round 5 complete"
            print("End Turn: Game Over. Final turn of Round 5 has ended.")
            self.stop_timer()
            App.get_running_app().switch_screen('game_over')
            App.get_running_app().save_game_state() # Save final state
            return

        # Round Advancement: Only happens if the game is not over.
        if is_second_player_turn_end:
            gs["current_round"] += 1
            print(f"End Turn: Round advanced to {gs['current_round']}")

        gs["status_message"] = f"Round {gs['current_round']} - {newly_active_player_name}'s Turn"
        gs['game_timer']['turn_segment_start_time'] = time_now 
        print(f"End Turn: New turn segment start_time = {time_now:.2f}")
        print(f"End Turn: Status message = {gs['status_message']}")
            
        print("End Turn: Calling self.update_ui_from_state()")
        self.update_ui_from_state()
        self.update_timer_display(0)
        App.get_running_app().save_game_state() # Save state after turn ends
        print(f"--- End Turn Processing Complete. Active player: {gs['active_player_id']} ---")

    def player_concedes(self, conceding_player_id):
        gs = App.get_running_app().game_state
        print(f"--- Player {conceding_player_id} Pressed Concede Button ---")

        if gs["game_phase"] != "game_play":
            print(f"Concede: Game not in 'playing' phase. No action.")
            return

        winning_player_id = 1 if conceding_player_id == 2 else 2
        conceding_player_name = gs[f'player{conceding_player_id}']['name']
        winning_player_name = gs[f'player{winning_player_id}']['name']

        gs["game_phase"] = "game_over"
        gs["status_message"] = f"{conceding_player_name} concedes. {winning_player_name} wins!"
        # Scores remain as they were when concede was pressed unless specified otherwise
        gs["last_round_played"] = gs["current_round"] # Record the round of concession

        print(f"Concede: Player {conceding_player_id} ({conceding_player_name}) conceded.")
        print(f"Concede: Player {winning_player_id} ({winning_player_name}) wins.")
        print(f"Concede: Game phase set to 'game_over'. Last round played: {gs['last_round_played']}")

        self.stop_timer()
        self.update_ui_from_state() # Update UI to hide buttons, show game over state on labels
        App.get_running_app().switch_screen('game_over')
        App.get_running_app().save_game_state()
        print(f"--- Concession Processing Complete ---")

    def open_score_numpad(self, player_id_to_score):
        gs = App.get_running_app().game_state
        if gs["game_phase"] != "game_play":
            gs["status_message"] = "Cannot change score, game not active."
            self.update_ui_from_state()
            return
        
        if self.numpad_popup:
             try:
                 self.numpad_popup.dismiss()
             except Exception as e:
                 print(f"Error dismissing numpad: {e}")
                 self.numpad_popup = None
        
        self.numpad_popup = NumberPadPopup(caller_widget=self)
        player_name = gs[f"player{player_id_to_score}"]["name"]
        self.numpad_popup.title = f"Enter {player_name} Score (Primary)" 
        self.numpad_popup.caller_info = {'player_id': player_id_to_score, 'score_type': 'primary'}
        self.numpad_popup.open()

    def process_numpad_value(self, score_value, player_id, score_type='primary'):
        player_key = f"player{player_id}"
        gs = App.get_running_app().game_state
        
        if player_key in gs:
            gs[player_key]["primary_score"] = score_value 
            gs[player_key]["total_score"] = gs[player_key]["primary_score"] + gs[player_key].get("secondary_score", 0) 
            gs["status_message"] = f"{gs[player_key]['name']} Score Updated"
            self.update_ui_from_state()
            App.get_running_app().save_game_state() # Save after processing numpad value
        else:
            gs["status_message"] = f"Error: Invalid player ID"
            self.update_ui_from_state()

    def add_cp(self, player_id, amount=1):
        gs = App.get_running_app().game_state
        if gs["game_phase"] != "game_play": return
        player_key = f"player{player_id}"
        if player_key in gs:
            gs[player_key]["cp"] = max(0, gs[player_key]["cp"] + amount)
            gs["status_message"] = f"{gs[player_key]['name']} CP Updated"
            self.update_ui_from_state()
            App.get_running_app().save_game_state() # Save after adding CP

    def remove_cp(self, player_id, amount=1): 
        gs = App.get_running_app().game_state
        if gs["game_phase"] != "game_play": return
        player_key = f"player{player_id}"
        if player_key in gs:
            if gs[player_key]["cp"] > 0:
                gs[player_key]["cp"] = max(0, gs[player_key]["cp"] - amount)
                gs["status_message"] = f"{gs[player_key]['name']} CP Updated"
            else:
                gs["status_message"] = f"{gs[player_key]['name']} CP is 0"
            self.update_ui_from_state()
            App.get_running_app().save_game_state() # Save after removing CP
    
    def request_new_game(self):
        print("New Game button pressed.")
        self.stop_timer() # Ensure current screen's timer is stopped
        App.get_running_app().start_new_game_flow()

    def exit_app(self):
        print("Exiting application...")
        gs = App.get_running_app().game_state
        if gs['game_timer']['status'] == 'running':
            if gs['game_phase'] == 'game_play' and gs.get('active_player_id'):
                active_player_id = gs['active_player_id']
                time_now = time.time()
                if gs['game_timer'].get('turn_segment_start_time') and gs['game_timer']['turn_segment_start_time'] > 0:
                    turn_duration = time_now - gs['game_timer']['turn_segment_start_time']
                    gs[f'player{active_player_id}']['player_elapsed_time_seconds'] += turn_duration
                    gs[f'player{active_player_id}']['player_time_display'] = self._format_seconds_to_hms(
                        gs[f'player{active_player_id}']['player_elapsed_time_seconds']
                    )
        self.stop_timer() 
        App.get_running_app().stop() 