"""
Message handler for the WebSocket server.
Handles message validation, processing, and routing.
"""

import json
from typing import Dict, Any, Optional, Callable, Awaitable
from datetime import datetime
import websockets
from websockets.server import WebSocketServerProtocol


class MessageHandler:
    """Handles WebSocket message processing and routing."""

    def __init__(self, settings: Dict[str, Any]):
        """Initialize the message handler.

        Args:
            settings (Dict[str, Any]): Server settings including message size limits.
        """
        self.settings = settings
        self.handlers: Dict[str, Callable[[WebSocketServerProtocol, Dict[str, Any]], Awaitable[None]]] = {}
        self._register_default_handlers()

    def _register_default_handlers(self) -> None:
        """Register default message handlers."""
        self.register_handler("ping", self._handle_ping)
        self.register_handler("error", self._handle_error)

    def register_handler(self, message_type: str, handler: Callable[[WebSocketServerProtocol, Dict[str, Any]], Awaitable[None]]) -> None:
        """Register a handler for a specific message type.

        Args:
            message_type (str): The type of message to handle.
            handler (Callable): The handler function for this message type.
        """
        self.handlers[message_type] = handler

    async def handle_message(self, client: WebSocketServerProtocol, message: str) -> None:
        """Handle an incoming message.

        Args:
            client (WebSocketServerProtocol): The client that sent the message.
            message (str): The raw message string.
        """
        try:
            # Check message size
            if len(message.encode('utf-8')) > self.settings["max_message_size"]:
                await self._send_error(client, "message_too_large", "Message exceeds size limit")
                return

            # Parse message
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                await self._send_error(client, "invalid_json", "Invalid JSON format")
                return

            # Validate message structure
            if not isinstance(data, dict) or "type" not in data or "data" not in data:
                await self._send_error(client, "invalid_format", "Invalid message format")
                return

            # Get handler for message type
            handler = self.handlers.get(data["type"])
            if handler:
                await handler(client, data["data"])
            else:
                await self._send_error(client, "unknown_type", f"Unknown message type: {data['type']}")

        except Exception as e:
            await self._send_error(client, "internal_error", f"Internal server error: {str(e)}")

    async def _handle_ping(self, client: WebSocketServerProtocol, data: Dict[str, Any]) -> None:
        """Handle ping messages.

        Args:
            client (WebSocketServerProtocol): The client that sent the ping.
            data (Dict[str, Any]): The ping message data.
        """
        response = {
            "type": "pong",
            "data": {
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        await client.send(json.dumps(response))

    async def _handle_error(self, client: WebSocketServerProtocol, data: Dict[str, Any]) -> None:
        """Handle error messages.

        Args:
            client (WebSocketServerProtocol): The client that sent the error.
            data (Dict[str, Any]): The error message data.
        """
        # Log error but don't send response to avoid error loops
        print(f"Client error: {data.get('message', 'Unknown error')}")

    async def _send_error(self, client: WebSocketServerProtocol, code: str, message: str) -> None:
        """Send an error message to a client.

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
            try:
                await client.send(json.dumps(error_message))
            except websockets.exceptions.ConnectionClosed:
                pass  # Client disconnected, no need to handle 