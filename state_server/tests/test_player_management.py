"""
Tests for player management functionality in the state server.
"""

import pytest
import asyncio
import json
import websockets
from pathlib import Path
from datetime import datetime
from src.database.manager import DatabaseManager
from src.websocket.server import WebSocketServer


@pytest.fixture
def db_path(tmp_path):
    """Create a temporary database path."""
    return tmp_path / "test_state.db"


@pytest.fixture
def db_manager(db_path):
    """Create a database manager instance."""
    return DatabaseManager(db_path)


@pytest.fixture
def server(db_manager):
    """Create a WebSocket server instance."""
    return WebSocketServer(db_manager)


@pytest.mark.asyncio
async def test_create_player(db_manager):
    """Test creating a new player."""
    # Create a player
    player_id = "test_player_1"
    game_id = "test_game_1"
    name = "Test Player"
    role = "attacker"

    db_manager.create_player(player_id, game_id, name, role)

    # Verify player was created
    player = db_manager.get_player(player_id)
    assert player is not None
    assert player["player_id"] == player_id
    assert player["game_id"] == game_id
    assert player["name"] == name
    assert player["role"] == role
    assert player["status"] == "active"
    assert player["score"] == 0


@pytest.mark.asyncio
async def test_create_player_invalid_role(db_manager):
    """Test creating a player with an invalid role."""
    with pytest.raises(Exception) as exc_info:
        db_manager.create_player(
            "test_player_1",
            "test_game_1",
            "Test Player",
            "invalid_role"
        )
    assert "CHECK constraint failed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_update_player(db_manager):
    """Test updating player information."""
    # Create a player
    player_id = "test_player_1"
    game_id = "test_game_1"
    name = "Test Player"
    role = "attacker"

    db_manager.create_player(player_id, game_id, name, role)

    # Update player
    updates = {
        "name": "Updated Name",
        "score": 100,
        "status": "inactive"
    }
    db_manager.update_player(player_id, updates)

    # Verify updates
    player = db_manager.get_player(player_id)
    assert player["name"] == updates["name"]
    assert player["score"] == updates["score"]
    assert player["status"] == updates["status"]
    assert player["role"] == role  # Role should not change


@pytest.mark.asyncio
async def test_get_game_players(db_manager):
    """Test retrieving all players in a game."""
    game_id = "test_game_1"

    # Create multiple players
    players = [
        ("player_1", "Player 1", "attacker"),
        ("player_2", "Player 2", "defender"),
        ("player_3", "Player 3", "attacker")
    ]

    for player_id, name, role in players:
        db_manager.create_player(player_id, game_id, name, role)

    # Get all players
    game_players = db_manager.get_game_players(game_id)
    assert len(game_players) == len(players)

    # Verify each player
    for player in game_players:
        assert player["game_id"] == game_id
        assert player["role"] in ["attacker", "defender"]


@pytest.mark.asyncio
async def test_get_player_by_role(db_manager):
    """Test retrieving a player by their role."""
    game_id = "test_game_1"

    # Create players
    db_manager.create_player("attacker_1", game_id, "Attacker 1", "attacker")
    db_manager.create_player("defender_1", game_id, "Defender 1", "defender")

    # Get attacker
    attacker = db_manager.get_player_by_role(game_id, "attacker")
    assert attacker is not None
    assert attacker["role"] == "attacker"
    assert attacker["name"] == "Attacker 1"

    # Get defender
    defender = db_manager.get_player_by_role(game_id, "defender")
    assert defender is not None
    assert defender["role"] == "defender"
    assert defender["name"] == "Defender 1"


@pytest.mark.asyncio
async def test_websocket_create_player(server):
    """Test creating a player via WebSocket."""
    async with websockets.serve(server.handle_connection, "localhost", 8765):
        async with websockets.connect("ws://localhost:8765") as websocket:
            # Create player message
            message = {
                "action": "create_player",
                "player_id": "test_player_1",
                "game_id": "test_game_1",
                "name": "Test Player",
                "role": "attacker"
            }

            # Send message
            await websocket.send(json.dumps(message))

            # Get response
            response = await websocket.recv()
            response_data = json.loads(response)

            assert response_data["type"] == "player_created"
            assert response_data["player_id"] == message["player_id"]
            assert response_data["game_id"] == message["game_id"]
            assert response_data["name"] == message["name"]
            assert response_data["role"] == message["role"]


@pytest.mark.asyncio
async def test_websocket_get_player(server, db_manager):
    """Test getting a player via WebSocket."""
    # Create a player first
    player_id = "test_player_1"
    game_id = "test_game_1"
    name = "Test Player"
    role = "attacker"
    db_manager.create_player(player_id, game_id, name, role)

    async with websockets.serve(server.handle_connection, "localhost", 8765):
        async with websockets.connect("ws://localhost:8765") as websocket:
            # Get player message
            message = {
                "action": "get_player",
                "player_id": player_id
            }

            # Send message
            await websocket.send(json.dumps(message))

            # Get response
            response = await websocket.recv()
            response_data = json.loads(response)

            assert response_data["type"] == "player_data"
            assert response_data["player"]["player_id"] == player_id
            assert response_data["player"]["game_id"] == game_id
            assert response_data["player"]["name"] == name
            assert response_data["player"]["role"] == role


@pytest.mark.asyncio
async def test_websocket_update_player(server, db_manager):
    """Test updating a player via WebSocket."""
    # Create a player first
    player_id = "test_player_1"
    game_id = "test_game_1"
    name = "Test Player"
    role = "attacker"
    db_manager.create_player(player_id, game_id, name, role)

    async with websockets.serve(server.handle_connection, "localhost", 8765):
        async with websockets.connect("ws://localhost:8765") as websocket:
            # Update player message
            updates = {
                "name": "Updated Name",
                "score": 100
            }
            message = {
                "action": "update_player",
                "player_id": player_id,
                "updates": updates
            }

            # Send message
            await websocket.send(json.dumps(message))

            # Get response
            response = await websocket.recv()
            response_data = json.loads(response)

            assert response_data["type"] == "player_updated"
            assert response_data["player"]["player_id"] == player_id
            assert response_data["player"]["name"] == updates["name"]
            assert response_data["player"]["score"] == updates["score"]


@pytest.mark.asyncio
async def test_websocket_get_game_players(server, db_manager):
    """Test getting all players in a game via WebSocket."""
    game_id = "test_game_1"

    # Create multiple players
    players = [
        ("player_1", "Player 1", "attacker"),
        ("player_2", "Player 2", "defender")
    ]

    for player_id, name, role in players:
        db_manager.create_player(player_id, game_id, name, role)

    async with websockets.serve(server.handle_connection, "localhost", 8765):
        async with websockets.connect("ws://localhost:8765") as websocket:
            # Get game players message
            message = {
                "action": "get_game_players",
                "game_id": game_id
            }

            # Send message
            await websocket.send(json.dumps(message))

            # Get response
            response = await websocket.recv()
            response_data = json.loads(response)

            assert response_data["type"] == "game_players"
            assert response_data["game_id"] == game_id
            assert len(response_data["players"]) == len(players)


@pytest.mark.asyncio
async def test_websocket_get_player_by_role(server, db_manager):
    """Test getting a player by role via WebSocket."""
    game_id = "test_game_1"

    # Create players
    db_manager.create_player("attacker_1", game_id, "Attacker 1", "attacker")
    db_manager.create_player("defender_1", game_id, "Defender 1", "defender")

    async with websockets.serve(server.handle_connection, "localhost", 8765):
        async with websockets.connect("ws://localhost:8765") as websocket:
            # Get player by role message
            message = {
                "action": "get_player_by_role",
                "game_id": game_id,
                "role": "attacker"
            }

            # Send message
            await websocket.send(json.dumps(message))

            # Get response
            response = await websocket.recv()
            response_data = json.loads(response)

            assert response_data["type"] == "player_data"
            assert response_data["player"]["role"] == "attacker"
            assert response_data["player"]["name"] == "Attacker 1" 