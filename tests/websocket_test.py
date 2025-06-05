import unittest
import socketio
import time
import threading
from websocket_server import WebSocketServer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestWebSocketServer(unittest.TestCase):
    def setUp(self):
        self.server = WebSocketServer()
        # Register a dummy game state callback
        self.server.set_game_state_callback(lambda: {
            'player1': {'id': 1, 'name': 'Player 1', 'total_score': 0, 'cp': 0, 'timer': 0},
            'player2': {'id': 2, 'name': 'Player 2', 'total_score': 0, 'cp': 0, 'timer': 0},
            'round': 1,
            'phase': 'init',
            'game_timer': {'status': 'stopped', 'start_time': 0, 'elapsed_display': '00:00:00'}
        })
        self.server.start()
        time.sleep(1)  # Wait for server to start
        self.client = socketio.Client()
        self.clients = []  # Track all clients for cleanup
        
    def tearDown(self):
        try:
            if hasattr(self, 'client') and self.client.connected:
                self.client.disconnect()
            # Clean up any additional clients
            for client in self.clients:
                if client.connected:
                    client.disconnect()
            if hasattr(self, 'server'):
                self.server.stop()
        except Exception as e:
            logger.error(f"Error during tearDown: {e}")
        
    def test_connection(self):
        """Test basic connection to WebSocket server"""
        connected = False
        connection_error = None
        
        @self.client.on('connect')
        def on_connect():
            nonlocal connected
            connected = True
            
        @self.client.on('connect_error')
        def on_connect_error(data):
            nonlocal connection_error
            connection_error = data
            
        try:
            self.client.connect('http://localhost:6969')
            time.sleep(1)
            self.assertTrue(connected, "Failed to connect to WebSocket server")
            self.assertIsNone(connection_error, f"Connection error occurred: {connection_error}")
        except Exception as e:
            self.fail(f"Connection test failed with error: {e}")
        
    def test_game_state_request(self):
        """Test requesting and receiving game state"""
        received_state = None
        error_occurred = False
        
        @self.client.on('game_state_update')
        def on_game_state(data):
            nonlocal received_state
            received_state = data
            
        @self.client.on('error')
        def on_error(data):
            nonlocal error_occurred
            error_occurred = True
            logger.error(f"Error received: {data}")
            
        try:
            self.client.connect('http://localhost:6969')
            self.client.emit('request_game_state')
            time.sleep(1)
            
            self.assertFalse(error_occurred, "Error occurred during game state request")
            self.assertIsNotNone(received_state, "No game state received")
            self.assertIn('player1', received_state, "Game state missing player1")
            self.assertIn('player2', received_state, "Game state missing player2")
            self.assertIn('round', received_state, "Game state missing round")
            self.assertIn('phase', received_state, "Game state missing phase")
        except Exception as e:
            self.fail(f"Game state test failed with error: {e}")
        
    def test_score_update(self):
        """Test score update broadcasting"""
        received_score = None
        error_occurred = False
        
        @self.client.on('score_update')
        def on_score(data):
            nonlocal received_score
            received_score = data
            
        @self.client.on('error')
        def on_error(data):
            nonlocal error_occurred
            error_occurred = True
            logger.error(f"Error received: {data}")
            
        try:
            self.client.connect('http://localhost:6969')
            self.client.emit('update_score', {'player_id': 1, 'score': 100})
            time.sleep(1)
            
            self.assertFalse(error_occurred, "Error occurred during score update")
            self.assertIsNotNone(received_score, "No score update received")
            self.assertEqual(received_score['player_id'], 1, "Incorrect player ID in score update")
            self.assertEqual(received_score['score'], 100, "Incorrect score value")
        except Exception as e:
            self.fail(f"Score update test failed with error: {e}")
        
    def test_cp_update(self):
        """Test CP update broadcasting"""
        received_cp = None
        error_occurred = False
        
        @self.client.on('cp_update')
        def on_cp(data):
            nonlocal received_cp
            received_cp = data
            
        @self.client.on('error')
        def on_error(data):
            nonlocal error_occurred
            error_occurred = True
            logger.error(f"Error received: {data}")
            
        try:
            self.client.connect('http://localhost:6969')
            self.client.emit('update_cp', {'player_id': 1, 'cp': 50})
            time.sleep(1)
            
            self.assertFalse(error_occurred, "Error occurred during CP update")
            self.assertIsNotNone(received_cp, "No CP update received")
            self.assertEqual(received_cp['player_id'], 1, "Incorrect player ID in CP update")
            self.assertEqual(received_cp['cp'], 50, "Incorrect CP value")
        except Exception as e:
            self.fail(f"CP update test failed with error: {e}")
            
    def test_game_phase_update(self):
        """Test game phase update broadcasting"""
        received_phase = None
        error_occurred = False
        
        @self.client.on('game_phase_update')
        def on_phase(data):
            nonlocal received_phase
            received_phase = data
            
        @self.client.on('error')
        def on_error(data):
            nonlocal error_occurred
            error_occurred = True
            logger.error(f"Error received: {data}")
            
        try:
            self.client.connect('http://localhost:6969')
            self.client.emit('update_game_phase', {'phase': 'playing'})
            time.sleep(1)
            
            self.assertFalse(error_occurred, "Error occurred during phase update")
            self.assertIsNotNone(received_phase, "No phase update received")
            self.assertEqual(received_phase['phase'], 'playing', "Incorrect phase value")
        except Exception as e:
            self.fail(f"Game phase update test failed with error: {e}")
            
    def test_round_update(self):
        """Test round update broadcasting"""
        received_round = None
        error_occurred = False
        
        @self.client.on('round_update')
        def on_round(data):
            nonlocal received_round
            received_round = data
            
        @self.client.on('error')
        def on_error(data):
            nonlocal error_occurred
            error_occurred = True
            logger.error(f"Error received: {data}")
            
        try:
            self.client.connect('http://localhost:6969')
            self.client.emit('update_round', {'round': 2})
            time.sleep(1)
            
            self.assertFalse(error_occurred, "Error occurred during round update")
            self.assertIsNotNone(received_round, "No round update received")
            self.assertEqual(received_round['round'], 2, "Incorrect round value")
        except Exception as e:
            self.fail(f"Round update test failed with error: {e}")
            
    def test_timer_update(self):
        """Test timer update broadcasting"""
        received_timer = None
        error_occurred = False
        
        @self.client.on('timer_update')
        def on_timer(data):
            nonlocal received_timer
            received_timer = data
            
        @self.client.on('error')
        def on_error(data):
            nonlocal error_occurred
            error_occurred = True
            logger.error(f"Error received: {data}")
            
        try:
            self.client.connect('http://localhost:6969')
            timer_data = {
                'status': 'running',
                'start_time': time.time(),
                'elapsed_display': '00:01:00'
            }
            self.client.emit('update_timer', timer_data)
            time.sleep(1)
            
            self.assertFalse(error_occurred, "Error occurred during timer update")
            self.assertIsNotNone(received_timer, "No timer update received")
            self.assertEqual(received_timer['status'], 'running', "Incorrect timer status")
            self.assertEqual(received_timer['elapsed_display'], '00:01:00', "Incorrect elapsed time")
        except Exception as e:
            self.fail(f"Timer update test failed with error: {e}")
        
    def test_multiple_clients(self):
        """Test multiple clients receiving updates"""
        client1_received = False
        client2_received = False
        error_occurred = False
        
        client1 = socketio.Client()
        client2 = socketio.Client()
        self.clients.extend([client1, client2])
        
        @client1.on('score_update')
        def on_score1(data):
            nonlocal client1_received
            client1_received = True
            
        @client2.on('score_update')
        def on_score2(data):
            nonlocal client2_received
            client2_received = True
            
        @client1.on('error')
        @client2.on('error')
        def on_error(data):
            nonlocal error_occurred
            error_occurred = True
            logger.error(f"Error received: {data}")
            
        try:
            client1.connect('http://localhost:6969')
            client2.connect('http://localhost:6969')
            self.client.connect('http://localhost:6969')
            
            self.client.emit('update_score', {'player_id': 1, 'score': 100})
            time.sleep(1)
            
            self.assertFalse(error_occurred, "Error occurred during multiple client test")
            self.assertTrue(client1_received, "Client 1 did not receive score update")
            self.assertTrue(client2_received, "Client 2 did not receive score update")
        except Exception as e:
            self.fail(f"Multiple clients test failed with error: {e}")

if __name__ == '__main__':
    unittest.main() 