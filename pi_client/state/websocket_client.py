import json
import asyncio
import websockets
from typing import Dict, Callable, Any, Optional

class WebSocketClient:
    def __init__(self):
        self.connection: Optional[websockets.WebSocketClientProtocol] = None
        self.handlers: Dict[str, Callable] = {}
        self._running = False

    async def connect(self, url: str) -> None:
        """Connect to the WebSocket server."""
        try:
            self.connection = await websockets.connect(url)
        except Exception as e:
            raise Exception(f'Connection failed: {str(e)}')

    def is_connected(self) -> bool:
        """Check if the client is connected to the server."""
        return self.connection is not None and not self.connection.closed

    async def send_message(self, message: Dict[str, Any]) -> None:
        """Send a message to the server."""
        if not self.is_connected():
            raise RuntimeError('Not connected to server')
        
        await self.connection.send(json.dumps(message))

    async def receive_message(self) -> Dict[str, Any]:
        """Receive a message from the server."""
        if not self.is_connected():
            raise RuntimeError('Not connected to server')
        
        message = await self.connection.recv()
        return json.loads(message)

    def register_handler(self, message_type: str, handler: Callable) -> None:
        """Register a handler for a specific message type."""
        self.handlers[message_type] = handler

    async def handle_messages(self) -> None:
        """Handle incoming messages using registered handlers."""
        if not self.is_connected():
            raise RuntimeError('Not connected to server')

        self._running = True
        while self._running and self.is_connected():
            try:
                message = await self.receive_message()
                message_type = message.get('type')
                if message_type in self.handlers:
                    await self.handlers[message_type](message.get('data'))
            except Exception as e:
                print(f"Error handling message: {str(e)}")
                self._running = False
                raise  # Re-raise the exception after handling it

    async def ensure_connection(self) -> None:
        """Ensure the connection is active, attempt reconnection if needed."""
        if not self.is_connected():
            raise Exception('Connection lost')

    async def close(self) -> None:
        """Close the WebSocket connection."""
        self._running = False
        if self.is_connected():
            await self.connection.close()
            self.connection = None 