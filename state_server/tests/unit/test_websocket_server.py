"""
Unit tests for WebSocket server functionality.
"""

import asyncio
import json
import pytest
import pytest_asyncio
import websockets
from datetime import datetime
import logging

from src.websocket.server import WebSocketServer
from src.database.manager import DatabaseManager


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest_asyncio.fixture
async def db_path(tmp_path):
    """Create a temporary database path."""
    return str(tmp_path / "test.db")


@pytest_asyncio.fixture
async def db_manager(db_path):
    """Create a database manager instance."""
    manager = DatabaseManager(db_path)
    return manager


@pytest_asyncio.fixture
async def server(db_manager):
    """Create a WebSocket server instance."""
    return WebSocketServer(db_manager)


# Utility function to receive a specific message type
async def recv_until(websocket, expected_type):
    while True:
        resp = json.loads(await websocket.recv())
        if resp["type"] == expected_type:
            return resp


@pytest.mark.asyncio
async def test_websocket_player_management(server, db_manager):
    """Test player management functionality."""
    async with websockets.serve(server.handle_connection, "localhost", 8772):
        async with websockets.connect("ws://localhost:8772") as websocket:
            # Create player
            create_msg = {
                "action": "create_player",
                "player_id": "p4",
                "game_id": "g4",
                "name": "Dana",
                "role": "defender"
            }
            await websocket.send(json.dumps(create_msg))
            resp = await recv_until(websocket, "player_created")
            assert resp["player_id"] == "p4"

            # Get player data
            get_msg = {"action": "get_player", "player_id": "p4"}
            await websocket.send(json.dumps(get_msg))
            resp = await recv_until(websocket, "player_data")
            assert resp["player"]["player_id"] == "p4"
            assert resp["player"]["name"] == "Dana"
            assert resp["player"]["role"] == "defender"

            # Update player
            update_msg = {
                "action": "update_player",
                "player_id": "p4",
                "updates": {"name": "Dana Updated"}
            }
            await websocket.send(json.dumps(update_msg))
            resp = await recv_until(websocket, "player_updated")
            assert resp["player"]["name"] == "Dana Updated"

            # Get all players in game
            get_all_msg = {"action": "get_game_players", "game_id": "g4"}
            await websocket.send(json.dumps(get_all_msg))
            resp = await recv_until(websocket, "game_players")
            assert len(resp["players"]) == 1
            assert resp["players"][0]["player_id"] == "p4"

            # Get player by role
            get_role_msg = {
                "action": "get_player_by_role",
                "game_id": "g4",
                "role": "defender"
            }
            await websocket.send(json.dumps(get_role_msg))
            resp = await recv_until(websocket, "player_data")
            assert resp["player"]["role"] == "defender"


@pytest.mark.asyncio
async def test_websocket_unsupported_action(server):
    """Test handling of unsupported actions."""
    async with websockets.serve(server.handle_connection, "localhost", 8773):
        async with websockets.connect("ws://localhost:8773") as websocket:
            msg = {"action": "unsupported_action"}
            await websocket.send(json.dumps(msg))
            resp = await recv_until(websocket, "error")
            assert "Unknown action" in resp["message"]


@pytest.mark.asyncio
async def test_player_role_validation(server):
    """Test player role validation."""
    async with websockets.serve(server.handle_connection, "localhost", 8774):
        async with websockets.connect("ws://localhost:8774") as websocket:
            # Test invalid role
            create_msg = {
                "action": "create_player",
                "player_id": "p8",
                "game_id": "g8",
                "name": "Ivy",
                "role": "invalid_role"
            }
            await websocket.send(json.dumps(create_msg))
            resp = await recv_until(websocket, "error")
            assert "Invalid role" in resp["message"]

        # Test valid roles with separate connections
        for role in ["attacker", "defender"]:
            create_msg = {
                "action": "create_player",
                "player_id": f"p8_{role}",
                "game_id": "g8",
                "name": "Ivy",
                "role": role
            }
            async with websockets.connect("ws://localhost:8774") as websocket:
                await websocket.send(json.dumps(create_msg))
                resp = await recv_until(websocket, "player_created")
                assert resp["player_id"] == f"p8_{role}"
                assert resp["role"] == role


@pytest.mark.asyncio
async def test_player_timestamp_validation(server):
    """Test player timestamp validation."""
    async with websockets.serve(server.handle_connection, "localhost", 8775):
        async with websockets.connect("ws://localhost:8775") as websocket:
            # Create player with timestamp
            create_msg = {
                "action": "create_player",
                "player_id": "p9",
                "game_id": "g9",
                "name": "Jack",
                "role": "attacker",
                "created_at": datetime.utcnow().isoformat()
            }
            await websocket.send(json.dumps(create_msg))
            resp = await recv_until(websocket, "player_created")
            assert resp["player_id"] == "p9"

            # Get player and verify timestamp
            get_msg = {"action": "get_player", "player_id": "p9"}
            await websocket.send(json.dumps(get_msg))
            resp = await recv_until(websocket, "player_data")
            assert "created_at" in resp["player"]
            assert "updated_at" in resp["player"]
            assert resp["player"]["created_at"] <= resp["player"]["updated_at"]


@pytest.mark.asyncio
async def test_concurrent_player_operations(server):
    """Test concurrent player operations."""
    async with websockets.serve(server.handle_connection, "localhost", 8776):
        # Create multiple concurrent connections
        async with websockets.connect("ws://localhost:8776") as ws1, \
                  websockets.connect("ws://localhost:8776") as ws2:

            # Create players concurrently
            create_msg1 = {
                "action": "create_player",
                "player_id": "p10_1",
                "game_id": "g10",
                "name": "Kelly",
                "role": "attacker"
            }
            create_msg2 = {
                "action": "create_player",
                "player_id": "p10_2",
                "game_id": "g10",
                "name": "Liam",
                "role": "defender"
            }

            # Send create requests concurrently
            await asyncio.gather(
                ws1.send(json.dumps(create_msg1)),
                ws2.send(json.dumps(create_msg2))
            )

            # Get responses (order may vary)
            responses = [await recv_until(ws1, "player_created"), await recv_until(ws2, "player_created")]
            player_ids = {resp["player_id"] for resp in responses}
            assert {"p10_1", "p10_2"} == player_ids

            # Verify both players exist in game
            get_all_msg = {"action": "get_game_players", "game_id": "g10"}
            await ws1.send(json.dumps(get_all_msg))
            resp = await recv_until(ws1, "game_players")
            returned_ids = {p["player_id"] for p in resp["players"]}
            assert {"p10_1", "p10_2"} <= returned_ids 