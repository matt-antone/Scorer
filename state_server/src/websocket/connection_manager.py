"""
Connection manager for the WebSocket server.
Manages client connections, authentication, and connection state.
"""

import asyncio
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime
import websockets
from websockets.server import WebSocketServerProtocol
import logging


class ConnectionManager:
    """Manages WebSocket client connections and their states."""

    def __init__(self, settings: Dict[str, Any]):
        """Initialize the connection manager.

        Args:
            settings (Dict[str, Any]): Server settings including connection limits and timeouts.
        """
        self.settings = settings
        self.clients: Dict[WebSocketServerProtocol, Dict[str, Any]] = {}
        self.client_types = ["host", "player", "observer"]
        self.connection_times: Dict[WebSocketServerProtocol, float] = {}
        self.message_counts: Dict[WebSocketServerProtocol, int] = {}
        self.last_message_times: Dict[WebSocketServerProtocol, float] = {}
        self.logger = logging.getLogger(__name__)

    def get_connection_count(self) -> int:
        """Get the current number of connected clients.

        Returns:
            int: Number of connected clients.
        """
        return len(self.clients)

    def get_client_info(self, client: WebSocketServerProtocol) -> Optional[Dict[str, Any]]:
        """Get information about a specific client.

        Args:
            client (WebSocketServerProtocol): The client to get information for.

        Returns:
            Optional[Dict[str, Any]]: Client information if found, None otherwise.
        """
        return self.clients.get(client)

    async def handle_connection(self, client: WebSocketServerProtocol, path: str) -> bool:
        """Handle a new client connection.

        Args:
            client (WebSocketServerProtocol): The new client connection.
            path (str): The connection path.

        Returns:
            bool: True if connection is accepted, False otherwise.
        """
        self.logger.debug(f"Handling connection for {client.remote_address}")
        # Check connection limit
        if len(self.clients) >= self.settings["max_concurrent_connections"]:
            self.logger.debug(f"Connection rejected: Maximum connections reached for {client.remote_address}")
            await client.close(1008, "Maximum connections reached")
            return False

        # Validate client type from headers
        client_type = self._get_client_type(client)
        if not client_type or client_type not in self.client_types:
            self.logger.debug(f"Connection rejected: Invalid client type for {client.remote_address}")
            await client.close(1008, "Invalid client type")
            return False

        # Initialize client state
        self.clients[client] = {
            "client_type": client_type,
            "connected_at": datetime.utcnow().isoformat(),
            "last_heartbeat": datetime.utcnow().isoformat(),
            "message_count": 0
        }
        self.connection_times[client] = time.time()
        self.message_counts[client] = 0
        self.last_message_times[client] = time.time()
        self.logger.debug(f"Connection accepted for {client.remote_address} with type {client_type}")
        return True

    async def handle_disconnection(self, client: WebSocketServerProtocol) -> None:
        """Handle client disconnection.

        Args:
            client (WebSocketServerProtocol): The disconnected client.
        """
        if client in self.clients:
            del self.clients[client]
        if client in self.connection_times:
            del self.connection_times[client]
        if client in self.message_counts:
            del self.message_counts[client]
        if client in self.last_message_times:
            del self.last_message_times[client]

    def check_message_rate(self, client: WebSocketServerProtocol) -> bool:
        """Check if a client has exceeded the message rate limit.

        Args:
            client (WebSocketServerProtocol): The client to check.

        Returns:
            bool: True if rate limit is exceeded, False otherwise.
        """
        current_time = time.time()
        if client not in self.last_message_times:
            return False

        # Reset count if more than 1 second has passed
        if current_time - self.last_message_times[client] >= 1:
            self.message_counts[client] = 0
            self.last_message_times[client] = current_time
            return False

        # Check if rate limit is exceeded
        if self.message_counts[client] >= self.settings["max_messages_per_second"]:
            return True

        self.message_counts[client] += 1
        return False

    def _get_client_type(self, client: WebSocketServerProtocol) -> Optional[str]:
        """Get the client type from the connection headers.

        Args:
            client (WebSocketServerProtocol): The client connection.

        Returns:
            Optional[str]: Client type if found in headers, None otherwise.
        """
        try:
            headers = client.request_headers
            client_type = headers.get("Client-Type", "").lower()
            return client_type if client_type in self.client_types else None
        except Exception:
            return None

    async def broadcast(self, message: Dict[str, Any], exclude: Optional[WebSocketServerProtocol] = None) -> None:
        """Broadcast a message to all connected clients.

        Args:
            message (Dict[str, Any]): The message to broadcast.
            exclude (Optional[WebSocketServerProtocol]): Client to exclude from broadcast.
        """
        if not isinstance(message, dict):
            message = {"type": "error", "data": {"message": "Invalid message format"}}

        message["timestamp"] = datetime.utcnow().isoformat()
        message_str = json.dumps(message)

        for client in self.clients:
            if client != exclude and client.open:
                try:
                    await client.send(message_str)
                except websockets.exceptions.ConnectionClosed:
                    await self.handle_disconnection(client)

    async def send_error(self, client: WebSocketServerProtocol, code: str, message: str) -> None:
        """Send an error message to a specific client.

        Args:
            client (WebSocketServerProtocol): The client to send the error to.
            code (str): Error code.
            message (str): Error message.
        """
        if client.open:
            error_message = {
                "type": "error",
                "data": {
                    "code": code,
                    "message": message,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            await client.send(json.dumps(error_message)) 