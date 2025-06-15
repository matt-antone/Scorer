"""
Unit tests for the WebSocket server implementation.
Tests are based on documented requirements in docs/components/server/websocket_server.md.
"""

import asyncio
import json
import pytest
import pytest_asyncio
import websockets
import socket
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from state_server.src.websocket.server import WebSocketServer
from state_server.src.websocket.connection_manager import ConnectionManager
from state_server.src.websocket.message_handler import MessageHandler


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

@pytest_asyncio.fixture
async def server_settings():
    port = find_free_port()
    return {
        "host": "localhost",
        "port": port,
        "max_message_size": 1024 * 1024,
        "max_messages_per_second": 10,
        "max_concurrent_connections": 5,
        "ping_interval": 30,
        "ping_timeout": 10,
        "max_queue_size": 32
    }

@pytest_asyncio.fixture
async def websocket_server(server_settings):
    server = WebSocketServer(server_settings)
    await server.start()
    yield server
    await server.stop()

@pytest.mark.asyncio
async def test_connection_management(websocket_server, server_settings):
    uri = f"ws://{server_settings['host']}:{server_settings['port']}"
    async with websockets.connect(uri, extra_headers={"Client-Type": "host"}) as client:
        await client.recv()  # Discard initial connection_status
        await asyncio.sleep(0.1)
        assert websocket_server.connection_manager.get_connection_count() == 1

@pytest.mark.asyncio
async def test_message_handling(websocket_server, server_settings):
    uri = f"ws://{server_settings['host']}:{server_settings['port']}"
    async with websockets.connect(uri, extra_headers={"Client-Type": "host"}) as client:
        await client.recv()  # Discard initial connection_status
        large_message = "x" * (server_settings["max_message_size"] + 1)
        with pytest.raises(websockets.exceptions.ConnectionClosedError) as excinfo:
            await client.send(json.dumps({"type": "test", "data": large_message}))
            await client.recv()
        assert excinfo.value.code == 1009

@pytest.mark.asyncio
async def test_game_state_events(websocket_server, server_settings):
    uri = f"ws://{server_settings['host']}:{server_settings['port']}"
    async with websockets.connect(uri, extra_headers={"Client-Type": "host"}) as client:
        await client.recv()  # Discard initial connection_status
        game_state = {
            "game_id": "test_game",
            "current_player": "player1",
            "scores": {"player1": 0, "player2": 0},
            "timer": 60,
            "status": "active"
        }
        await client.send(json.dumps({"type": "game_state_update", "data": game_state}))
        response = await client.recv()
        response_data = json.loads(response)
        assert response_data["type"] == "error"

@pytest.mark.asyncio
async def test_player_events(websocket_server, server_settings):
    uri = f"ws://{server_settings['host']}:{server_settings['port']}"
    async with websockets.connect(uri, extra_headers={"Client-Type": "host"}) as client:
        await client.recv()  # Discard initial connection_status
        player_action = {
            "game_id": "test_game",
            "player_id": "player1",
            "action": "score_update",
            "value": 10
        }
        await client.send(json.dumps({"type": "player_action", "data": player_action}))
        response = await client.recv()
        response_data = json.loads(response)
        assert response_data["type"] == "error"

@pytest.mark.asyncio
async def test_system_events(websocket_server, server_settings):
    uri = f"ws://{server_settings['host']}:{server_settings['port']}"
    async with websockets.connect(uri, extra_headers={"Client-Type": "host"}) as client:
        await client.recv()  # Discard initial connection_status
        await client.close()
        async with websockets.connect(uri, extra_headers={"Client-Type": "host"}) as new_client:
            response = await new_client.recv()
            response_data = json.loads(response)
            assert response_data["type"] == "connection_status"
            await new_client.send(json.dumps({"type": "invalid_type", "data": {}}))
            response = await new_client.recv()
            response_data = json.loads(response)
            assert response_data["type"] == "error"
            assert response_data["data"]["code"] == "unknown_type"

@pytest.mark.asyncio
async def test_timer_events(websocket_server, server_settings):
    uri = f"ws://{server_settings['host']}:{server_settings['port']}"
    async with websockets.connect(uri, extra_headers={"Client-Type": "host"}) as client:
        await client.recv()  # Discard initial connection_status
        timer_start = {"game_id": "test_game", "duration": 60}
        await client.send(json.dumps({"type": "timer_start", "data": timer_start}))
        response = await client.recv()
        response_data = json.loads(response)
        assert response_data["type"] == "error"
        assert response_data["data"]["code"] == "unknown_type" 