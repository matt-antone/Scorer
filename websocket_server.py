from flask import Flask, send_from_directory, request, render_template
from flask_socketio import SocketIO, emit
import json
import threading
from typing import Dict, Any, Optional
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketServer:
    def __init__(
        self,
        get_game_state_callback=None,
        update_score_callback=None,
        increment_cp_callback=None,
        end_turn_callback=None,
        concede_game_callback=None,
        host: str = "0.0.0.0",
        port: int = 6969,
    ):
        self.app = Flask(__name__, static_folder="static")
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.host = host
        self.port = port
        self.server_thread: Optional[threading.Thread] = None
        self.get_game_state_callback = get_game_state_callback
        self.update_score_callback = update_score_callback
        self.increment_cp_callback = increment_cp_callback
        self.end_turn_callback = end_turn_callback
        self.concede_game_callback = concede_game_callback
        self._setup_routes()
        self._setup_socket_handlers()

    def _setup_routes(self):
        @self.app.route('/')
        def index():
            return send_from_directory(self.app.static_folder, 'index.html')

        @self.app.route('/player/<int:player_id>')
        def player_client(player_id):
            if player_id not in [1, 2]:
                return "Invalid Player ID", 404
            return render_template('player.html', player_id=player_id)

        @self.app.route('/<path:path>')
        def serve_static(path):
            return send_from_directory(self.app.static_folder, path)

    def _setup_socket_handlers(self):
        @self.socketio.on('connect')
        def handle_connect():
            logger.info(f"Client connected: {request.sid}")
            # Immediately send the current game state to the newly connected client
            if self.get_game_state_callback:
                game_state = self.get_game_state_callback()
                emit('game_state_update', game_state)
            else:
                logger.warning("No game state callback registered, cannot send initial state.")

        @self.socketio.on('disconnect')
        def handle_disconnect():
            logger.info(f"Client disconnected: {request.sid}")

        @self.socketio.on('request_game_state')
        def handle_game_state_request():
            if self.get_game_state_callback:
                game_state = self.get_game_state_callback()
                emit("game_state_update", game_state)
            else:
                logger.warning("No game state callback registered")

        @self.socketio.on("update_score")
        def handle_score_update(data):
            if self.update_score_callback:
                logger.info(f"Received score update event: {data}")
                self.update_score_callback(data)
            else:
                logger.warning("No score update callback registered.")

        @self.socketio.on("increment_cp")
        def handle_cp_update(data):
            if self.increment_cp_callback:
                logger.info(f"Received CP increment event: {data}")
                self.increment_cp_callback(data)
            else:
                logger.warning("No CP increment callback registered.")

        @self.socketio.on("end_turn")
        def handle_end_turn(data):
            if self.end_turn_callback:
                logger.info(f"Received end turn event: {data}")
                self.end_turn_callback(data)
            else:
                logger.warning("No end turn callback registered.")

        @self.socketio.on("concede_game")
        def handle_concede_game(data):
            if self.concede_game_callback:
                logger.info(f"Received concede game event: {data}")
                self.concede_game_callback(data)
            else:
                logger.warning("No concede game callback registered.")

        @self.socketio.on('update_game_phase')
        def handle_game_phase_update(data):
            if self.get_game_state_callback:
                game_state = self.get_game_state_callback()
                new_phase = data.get('phase')
                if new_phase is not None:
                    game_state['phase'] = new_phase
                    self.broadcast_game_phase_update(new_phase)
                    logger.info(f"Game phase updated to: {new_phase}")

        @self.socketio.on('update_round')
        def handle_round_update(data):
            if self.get_game_state_callback:
                game_state = self.get_game_state_callback()
                new_round = data.get('round')
                if new_round is not None:
                    game_state['round'] = new_round
                    self.broadcast_round_update(new_round)
                    logger.info(f"Round updated to: {new_round}")

        @self.socketio.on('update_timer')
        def handle_timer_update(data):
            if self.get_game_state_callback:
                game_state = self.get_game_state_callback()
                if isinstance(data, dict) and 'status' in data:
                    game_state['game_timer'] = data
                    self.broadcast_timer_update(data)
                    logger.info(f"Timer updated: {data}")

    def start(self):
        """Start the WebSocket server in a separate thread"""
        if self.server_thread and self.server_thread.is_alive():
            logger.warning("WebSocket server is already running")
            return

        def run_server():
            logger.info(f"Starting WebSocket server on {self.host}:{self.port}")
            self.socketio.run(self.app, host=self.host, port=self.port, allow_unsafe_werkzeug=True)

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

    def stop(self):
        """Stop the WebSocket server"""
        if self.server_thread and self.server_thread.is_alive():
            logger.info("Stopping WebSocket server")
            self.server_thread.join(timeout=5)
            if self.server_thread.is_alive():
                logger.warning("WebSocket server thread did not stop gracefully")

    def broadcast_game_state(self):
        """
        Broadcasts the sanitized game state to all connected clients
        by calling the registered callback function.
        """
        if self.get_game_state_callback:
            game_state = self.get_game_state_callback()
            self.socketio.emit('game_state_update', game_state)
            logger.info("Broadcasted full game state update to all clients.")
        else:
            logger.warning("Cannot broadcast game state: no callback registered.")

    def broadcast_score_update(self, player_id: int, new_score: int):
        """Broadcast score update to all connected clients"""
        self.socketio.emit("score_update", {"player_id": player_id, "score": new_score})

    def broadcast_cp_update(self, player_id: int, new_cp: int):
        """Broadcast CP update to all connected clients"""
        self.socketio.emit('cp_update', {
            'player_id': player_id,
            'cp': new_cp
        })

    def broadcast_timer_update(self, timer_data: Dict[str, Any]):
        """Broadcast timer update to all connected clients"""
        self.socketio.emit('timer_update', timer_data)

    def broadcast_round_update(self, round_number: int):
        """Broadcast round update to all connected clients"""
        self.socketio.emit('round_update', {'round': round_number})

    def broadcast_game_phase_update(self, phase: str):
        """Broadcast game phase update to all connected clients"""
        self.socketio.emit("game_phase_update", {"phase": phase}) 