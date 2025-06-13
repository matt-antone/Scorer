from pi_client.state.game_state import GameState, GameStatus

print("--- GameState Integration Test ---")

# Create a new game state
state = GameState()
print("Initial state:", state)

# Set player names
state.player1_name = "Alice"
state.player2_name = "Bob"
print(f"Players: {state.player1_name} vs {state.player2_name}")

# Set attacker and first turn player
state.attacker_id = 1
state.first_turn_player_id = 2
print(f"Attacker: {state.attacker_id}, First turn: {state.first_turn_player_id}")

# Set scores
state.player1_primary = 10
state.player1_secondary = 5
state.player2_primary = 8
state.player2_secondary = 3
print(f"Scores: P1({state.player1_primary}, {state.player1_secondary}), P2({state.player2_primary}, {state.player2_secondary})")

# Set round and current player
state.current_round = 2
state.current_player_id = 2
print(f"Round: {state.current_round}, Current player: {state.current_player_id}")

# Try invalid values and catch errors
try:
    state.player1_primary = -1
except ValueError as e:
    print("Caught error:", e)

try:
    state.attacker_id = 3
except ValueError as e:
    print("Caught error:", e)

try:
    state.current_round = 0
except ValueError as e:
    print("Caught error:", e)

print("--- Integration Test Complete ---") 