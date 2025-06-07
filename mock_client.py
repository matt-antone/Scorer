import socketio
import threading
import time

# Standard Python client for Socket.IO
sio = socketio.Client()

# Player ID for this client instance (can be changed)
PLAYER_ID = 1

@sio.event
def connect():
    print(f"Mock client connected with SID: {sio.sid}")
    print("--- Listening for game state updates ---")

@sio.event
def connect_error(data):
    print("Connection failed!")
    print(data)

@sio.event
def disconnect():
    print("Disconnected from server.")

@sio.on('game_state_update')
def on_game_state_update(data):
    """Handles game state updates from the server."""
    print("\n--- GAME STATE UPDATE RECEIVED ---")
    # Pretty print the relevant parts of the state
    p1 = data.get('player1', {})
    p2 = data.get('player2', {})
    print(f"Round: {data.get('current_round', 'N/A')}, Phase: {data.get('game_phase', 'N/A')}")
    print(f"Active Player: {data.get('active_player_id', 'N/A')}")
    print(f"P1: {p1.get('name', 'N/A')} | Score: {p1.get('total_score', 'N/A')} | CP: {p1.get('cp', 'N/A')}")
    print(f"P2: {p2.get('name', 'N/A')} | Score: {p2.get('total_score', 'N/A')} | CP: {p2.get('cp', 'N/A')}")
    print("------------------------------------")
    print("Enter command (e.g., 'end', 'score <val>', 'cp <val>', 'concede', 'quit'):")

def send_events():
    """A loop to read user input and send events to the server."""
    global PLAYER_ID
    time.sleep(1) # Give a moment for connection to establish
    print(f"Mock client running for Player ID: {PLAYER_ID}")
    print("Enter command (e.g., 'end', 'score <val>', 'cp <val>', 'concede', 'quit'):")

    while True:
        command = input("> ").strip().lower()
        parts = command.split()
        cmd = parts[0] if parts else ''

        if cmd == 'quit':
            break
        elif cmd == 'end':
            print("Sending 'end_turn' event...")
            sio.emit('end_turn', {'player_id': PLAYER_ID})
        elif cmd == 'score' and len(parts) == 2:
            try:
                score = int(parts[1])
                print(f"Sending 'update_score' event with value: {score}...")
                # Note: The real player client sends 'primary' or 'secondary'.
                # For this test, we'll mimic the primary score update path.
                sio.emit('update_score', {'player_id': PLAYER_ID, 'score_type': 'primary', 'value': score})
            except ValueError:
                print("Invalid score. Please enter a number.")
        elif cmd == 'cp' and len(parts) == 2:
            try:
                cp_val = int(parts[1])
                print(f"Sending 'increment_cp' event with value: {cp_val}...")
                sio.emit('increment_cp', {'player_id': PLAYER_ID, 'value': cp_val})
            except ValueError:
                print("Invalid CP value. Please enter a number.")
        elif cmd == 'concede':
            print("Sending 'concede_game' event...")
            sio.emit('concede_game', {'player_id': PLAYER_ID})
        elif cmd.startswith('player'):
             try:
                new_id = int(parts[1])
                if new_id in [1, 2]:
                    PLAYER_ID = new_id
                    print(f"Client now acting as Player {PLAYER_ID}")
                else:
                    print("Player ID must be 1 or 2.")
             except (ValueError, IndexError):
                print("Invalid command. Use 'player 1' or 'player 2'.")
        else:
            print("Unknown command. Available: end, score <val>, cp <val>, concede, player <id>, quit")

    sio.disconnect()

if __name__ == '__main__':
    try:
        sio.connect('http://localhost:6969')
        # Run the input loop in a separate thread so it doesn't block receiving messages
        input_thread = threading.Thread(target=send_events)
        input_thread.daemon = True
        input_thread.start()
        # The main thread will wait for the connection to close
        sio.wait()
    except socketio.exceptions.ConnectionError as e:
        print(f"Could not connect to the server: {e}")
    except KeyboardInterrupt:
        print("Interrupted by user. Disconnecting...")
    finally:
        if sio.connected:
            sio.disconnect()
        print("Client shut down.") 