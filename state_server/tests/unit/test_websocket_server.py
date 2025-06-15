"""
Unit tests for the WebSocket server implementation.
"""

import asyncio
import json
import pytest
import websockets
import socket
import logging
from datetime import datetime
from typing import Dict, Any
import pytest_asyncio
import random

from state_server.src.websocket.server import WebSocketServer
from state_server.src.websocket.connection_manager import ConnectionManager
from state_server.src.websocket.message_handler import MessageHandler

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def find_free_port() -> int:
    """Find a free port for the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

@pytest.fixture
def server_settings() -> Dict[str, Any]:
    """Fixture providing server settings for testing."""
    return {
        "host": "localhost",
        "port": find_free_port(),
        "max_message_size": 1024 * 1024,  # 1MB
        "max_messages_per_second": 10,
        "max_concurrent_connections": 5,
        "ping_interval": 30,
        "ping_timeout": 10,
        "max_queue_size": 32
    }

@pytest_asyncio.fixture
async def websocket_server(server_settings: Dict[str, Any]) -> WebSocketServer:
    """Async fixture providing a WebSocket server instance for testing, with proper teardown."""
    server = WebSocketServer(server_settings)
    await server.start()
    logger.debug(f"Starting WebSocket server on port {server_settings['port']}")
    yield server
    logger.info("Stopping WebSocket server")
    await server.stop()

@pytest.mark.asyncio
async def test_server_initialization(websocket_server: WebSocketServer, server_settings: Dict[str, Any]) -> None:
    """Test server initialization with settings."""
    assert websocket_server.settings == server_settings
    assert isinstance(websocket_server.connection_manager, ConnectionManager)
    assert isinstance(websocket_server.message_handler, MessageHandler)

@pytest_asyncio.fixture
async def server():
    port = random.randint(8000, 9000)
    settings = {
        "host": "localhost",
        "port": port,
        "max_message_size": 1024 * 1024,
        "max_messages_per_second": 10,
        "max_concurrent_connections": 5,
        "ping_interval": 30,
        "ping_timeout": 10,
        "max_queue_size": 32
    }
    server = WebSocketServer(settings)
    await server.start()
    logger.debug(f"Server started on port {port}")
    yield server
    await server.stop()
    logger.debug("Server stopped")

@pytest.mark.asyncio
async def test_connection_handling(server):
    logger.debug("Starting test_connection_handling")
    async with websockets.connect(f"ws://localhost:{server.settings['port']}", extra_headers={"Client-Type": "host"}) as websocket:
        logger.debug("Client connected")
        await asyncio.sleep(1)  # Wait for server to register client
        count = server.connection_manager.get_connection_count()
        logger.debug(f"Connection count: {count}")
        assert count == 1
    logger.debug("Test completed")

@pytest.mark.asyncio
async def test_message_handling(websocket_server):
    uri = f"ws://{websocket_server.settings['host']}:{websocket_server.settings['port']}"
    async with websockets.connect(uri, extra_headers={"Client-Type": "host"}) as client:
        await client.recv()  # Discard initial connection_status
        # Test valid message
        message = {
            "type": "ping",
            "data": {"timestamp": datetime.utcnow().isoformat()}
        }
        await client.send(json.dumps(message))
        response = await asyncio.wait_for(client.recv(), timeout=5)
        response_data = json.loads(response)
        assert response_data["type"] == "pong"

        # Test invalid JSON
        await client.send("invalid json")
        response = await asyncio.wait_for(client.recv(), timeout=5)
        response_data = json.loads(response)
        assert response_data["type"] == "error"
        assert response_data["data"]["code"] == "invalid_json"

@pytest.mark.asyncio
async def test_message_rate_limiting(websocket_server):
    uri = f"ws://{websocket_server.settings['host']}:{websocket_server.settings['port']}"
    async with websockets.connect(uri, extra_headers={"Client-Type": "host"}) as client:
        await client.recv()  # Discard initial connection_status
        # Send messages up to rate limit
        for _ in range(websocket_server.settings["max_messages_per_second"]):
            message = {
                "type": "ping",
                "data": {"timestamp": datetime.utcnow().isoformat()}
            }
            await client.send(json.dumps(message))
            response = await asyncio.wait_for(client.recv(), timeout=5)
            response_data = json.loads(response)
            assert response_data["type"] == "pong"

        # Send one more message to exceed rate limit
        message = {
            "type": "ping",
            "data": {"timestamp": datetime.utcnow().isoformat()}
        }
        await client.send(json.dumps(message))
        response = await asyncio.wait_for(client.recv(), timeout=5)
        response_data = json.loads(response)
        assert response_data["type"] == "error"
        assert response_data["data"]["code"] == "rate_limit_exceeded"

@pytest.mark.asyncio
async def test_connection_limit(websocket_server):
    uri = f"ws://{websocket_server.settings['host']}:{websocket_server.settings['port']}"
    clients = []
    for i in range(websocket_server.settings["max_concurrent_connections"]):
        client = await websockets.connect(uri, extra_headers={"Client-Type": "player"})
        await client.recv()  # Discard initial connection_status
        clients.append(client)
        assert websocket_server.connection_manager.get_connection_count() == i + 1
    # Try to connect one more
    with pytest.raises(websockets.exceptions.ConnectionClosedError) as excinfo:
        extra_client = await websockets.connect(uri, extra_headers={"Client-Type": "player"})
        await extra_client.recv()
    assert excinfo.value.code == 1008
    for client in clients:
        await client.close()

@pytest.mark.asyncio
async def test_broadcast(websocket_server):
    uri = f"ws://{websocket_server.settings['host']}:{websocket_server.settings['port']}"
    clients = []
    for client_type in ["host", "player", "observer"]:
        client = await websockets.connect(uri, extra_headers={"Client-Type": client_type})
        await client.recv()  # Discard initial connection_status
        clients.append(client)
    message = {"type": "test", "data": {"message": "test broadcast"}}
    await websocket_server.broadcast(message)
    for client in clients:
        # Discard any additional connection_status messages
        while True:
            response = await client.recv()
            response_data = json.loads(response)
            if response_data["type"] == "test":
                break
        assert response_data["type"] == "test"
        assert response_data["data"]["message"] == "test broadcast"
    for client in clients:
        await client.close()

@pytest.mark.asyncio
async def test_message_too_large(websocket_server):
    uri = f"ws://{websocket_server.settings['host']}:{websocket_server.settings['port']}"
    async with websockets.connect(uri, extra_headers={"Client-Type": "host"}) as client:
        await client.recv()  # Discard initial connection_status
        large_message = "x" * (websocket_server.settings["max_message_size"] + 1)
        with pytest.raises(websockets.exceptions.ConnectionClosedError) as excinfo:
            await client.send(large_message)
            await client.recv()
        assert excinfo.value.code == 1009

@pytest.mark.asyncio
async def test_unknown_message_type(websocket_server):
    uri = f"ws://{websocket_server.settings['host']}:{websocket_server.settings['port']}"
    async with websockets.connect(uri, extra_headers={"Client-Type": "host"}) as client:
        await client.recv()  # Discard initial connection_status
        message = {"type": "unknown", "data": {}}
        await client.send(json.dumps(message))
        response = await asyncio.wait_for(client.recv(), timeout=5)
        response_data = json.loads(response)
        assert response_data["type"] == "error"
        assert response_data["data"]["code"] == "unknown_type" 