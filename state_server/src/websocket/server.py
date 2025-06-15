"""
WebSocket server implementation.
Handles client connections, message routing, and state management.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
import websockets
from websockets.server import WebSocketServerProtocol
from datetime import datetime

from .connection_manager import ConnectionManager
from .message_handler import MessageHandler


class WebSocketServer:
    """WebSocket server for handling client connections and state management."""

    def __init__(self, settings: Dict[str, Any]):
        """Initialize the WebSocket server.

        Args:
            settings (Dict[str, Any]): Server settings including host, port, and limits.
        """
        self.settings = settings
        self.connection_manager = ConnectionManager(settings)
        self.message_handler = MessageHandler(settings)
        self.server: Optional[websockets.WebSocketServer] = None
        self.logger = logging.getLogger(__name__)

    async def start(self) -> None:
        """Start the WebSocket server."""
        try:
            self.server = await websockets.serve(
                self._handle_connection,
                self.settings["host"],
                self.settings["port"],
                ping_interval=self.settings.get("ping_interval", 30),
                ping_timeout=self.settings.get("ping_timeout", 10),
                max_size=self.settings["max_message_size"],
                max_queue=self.settings.get("max_queue_size", 32)
            )
            self.logger.info(f"WebSocket server started on {self.settings['host']}:{self.settings['port']}")
        except Exception as e:
            self.logger.error(f"Failed to start WebSocket server: {str(e)}")
            raise

    async def stop(self) -> None:
        """Stop the WebSocket server."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.logger.info("WebSocket server stopped")

    async def _handle_connection(self, client: WebSocketServerProtocol, path: str) -> None:
        """Handle a new client connection.

        Args:
            client (WebSocketServerProtocol): The new client connection.
            path (str): The connection path.
        """
        self.logger.debug(f"Handling new connection from {client.remote_address}")
        try:
            # Handle connection
            if not await self.connection_manager.handle_connection(client, path):
                self.logger.debug(f"Connection rejected for {client.remote_address}")
                return

            self.logger.info(f"New client connected: {client.remote_address}")
            await self._broadcast_connection_status()

            # Handle messages
            async for message in client:
                if self.connection_manager.check_message_rate(client):
                    await self.connection_manager.send_error(
                        client,
                        "rate_limit_exceeded",
                        "Message rate limit exceeded"
                    )
                    continue

                await self.message_handler.handle_message(client, message)

        except websockets.exceptions.ConnectionClosed:
            self.logger.info(f"Client disconnected: {client.remote_address}")
        except Exception as e:
            self.logger.error(f"Error handling client connection: {str(e)}")
        finally:
            await self.connection_manager.handle_disconnection(client)
            await self._broadcast_connection_status()

    async def _broadcast_connection_status(self) -> None:
        """Broadcast current connection status to all clients."""
        status = {
            "type": "connection_status",
            "data": {
                "connected_clients": self.connection_manager.get_connection_count(),
                "timestamp": self._get_timestamp()
            }
        }
        await self.connection_manager.broadcast(status)

    def _get_timestamp(self) -> str:
        """Get current UTC timestamp in ISO format.

        Returns:
            str: Current timestamp in ISO format.
        """
        return datetime.utcnow().isoformat()

    def register_message_handler(self, message_type: str, handler: Any) -> None:
        """Register a handler for a specific message type.

        Args:
            message_type (str): The type of message to handle.
            handler (Any): The handler function for this message type.
        """
        self.message_handler.register_handler(message_type, handler)

    async def broadcast(self, message: Dict[str, Any], exclude: Optional[WebSocketServerProtocol] = None) -> None:
        """Broadcast a message to all connected clients.

        Args:
            message (Dict[str, Any]): The message to broadcast.
            exclude (Optional[WebSocketServerProtocol]): Client to exclude from broadcast.
        """
        await self.connection_manager.broadcast(message, exclude) 