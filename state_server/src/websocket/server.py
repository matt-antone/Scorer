"""
WebSocket server implementation for the state server.
Handles real-time communication with clients.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, Set
import websockets
from websockets.server import WebSocketServerProtocol
from datetime import datetime

from ..database.manager import DatabaseManager


class WebSocketServer:
    """WebSocket server for real-time state updates."""

    def __init__(self, db_manager: DatabaseManager):
        """Initialize the WebSocket server.

        Args:
            db_manager (DatabaseManager): Database manager instance.
        """
        self.db_manager = db_manager
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.game_clients: Dict[str, Set[websockets.WebSocketServerProtocol]] = {}
        self.server: Optional[websockets.WebSocketServer] = None
        self.logger = logging.getLogger(__name__)

    async def start(self, host: str, port: int) -> None:
        """Start the WebSocket server.

        Args:
            host (str): Host to bind to.
            port (int): Port to bind to.
        """
        async with websockets.serve(self.handle_connection, host, port):
            await asyncio.Future()  # run forever

    async def stop(self) -> None:
        """Stop the WebSocket server."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.logger.info("WebSocket server stopped")

    async def handle_connection(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None:
        """Handle a new WebSocket connection.

        Args:
            websocket (websockets.WebSocketServerProtocol): WebSocket connection.
            path (str): Request path.
        """
        await self.register(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_message(websocket, data)
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': 'Invalid JSON message'
                    }))
        finally:
            await self.unregister(websocket)

    async def register(self, websocket: websockets.WebSocketServerProtocol) -> None:
        """Register a new client connection.

        Args:
            websocket (websockets.WebSocketServerProtocol): WebSocket connection.
        """
        self.clients.add(websocket)

    async def unregister(self, websocket: websockets.WebSocketServerProtocol) -> None:
        """Unregister a client connection.

        Args:
            websocket (websockets.WebSocketServerProtocol): WebSocket connection.
        """
        self.clients.remove(websocket)
        # Remove from game-specific clients
        for game_clients in self.game_clients.values():
            game_clients.discard(websocket)

    async def register_game_client(self, websocket: websockets.WebSocketServerProtocol, game_id: str) -> None:
        """Register a client for a specific game.

        Args:
            websocket (websockets.WebSocketServerProtocol): WebSocket connection.
            game_id (str): Game identifier.
        """
        if game_id not in self.game_clients:
            self.game_clients[game_id] = set()
        self.game_clients[game_id].add(websocket)

    async def broadcast(self, message: Dict[str, Any]) -> None:
        """Broadcast a message to all connected clients.

        Args:
            message (Dict[str, Any]): Message to broadcast.
        """
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients]
            )

    async def broadcast_game(self, game_id: str, message: Dict[str, Any]) -> None:
        """Broadcast a message to all clients in a specific game.

        Args:
            game_id (str): Game identifier.
            message (Dict[str, Any]): Message to broadcast.
        """
        if game_id in self.game_clients and self.game_clients[game_id]:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.game_clients[game_id]]
            )

    async def handle_message(self, websocket: websockets.WebSocketServerProtocol, message: Dict[str, Any]) -> None:
        """Handle incoming WebSocket messages.

        Args:
            websocket (websockets.WebSocketServerProtocol): WebSocket connection.
            message (Dict[str, Any]): Message to handle.
        """
        try:
            action = message.get('action')
            if not action:
                raise ValueError("No action specified in message")

            if action == 'create_player':
                await self.handle_create_player(websocket, message)
            elif action == 'get_player':
                await self.handle_get_player(websocket, message)
            elif action == 'update_player':
                await self.handle_update_player(websocket, message)
            elif action == 'get_game_players':
                await self.handle_get_game_players(websocket, message)
            elif action == 'get_player_by_role':
                await self.handle_get_player_by_role(websocket, message)
            else:
                raise ValueError(f"Unknown action: {action}")

        except Exception as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': str(e)
            }))

    async def handle_create_player(self, websocket: websockets.WebSocketServerProtocol, message: Dict[str, Any]) -> None:
        """Handle player creation request.

        Args:
            websocket (websockets.WebSocketServerProtocol): WebSocket connection.
            message (Dict[str, Any]): Message containing player data.
        """
        try:
            player_id = message.get('player_id')
            game_id = message.get('game_id')
            name = message.get('name')
            role = message.get('role')

            if not all([player_id, game_id, name, role]):
                raise ValueError("Missing required player data")

            if role not in ['attacker', 'defender']:
                raise ValueError("Invalid role. Must be 'attacker' or 'defender'")

            self.db_manager.create_player(player_id, game_id, name, role)
            await self.register_game_client(websocket, game_id)

            # Broadcast player creation to all game clients
            await self.broadcast_game(game_id, {
                'type': 'player_created',
                'player_id': player_id,
                'game_id': game_id,
                'name': name,
                'role': role
            })

            # Send confirmation to the creating client
            await websocket.send(json.dumps({
                'type': 'player_created',
                'player_id': player_id,
                'game_id': game_id,
                'name': name,
                'role': role
            }))

        except Exception as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f"Failed to create player: {str(e)}"
            }))

    async def handle_get_player(self, websocket: websockets.WebSocketServerProtocol, message: Dict[str, Any]) -> None:
        """Handle player retrieval request.

        Args:
            websocket (websockets.WebSocketServerProtocol): WebSocket connection.
            message (Dict[str, Any]): Message containing player ID.
        """
        try:
            player_id = message.get('player_id')
            if not player_id:
                raise ValueError("No player ID specified")

            player = self.db_manager.get_player(player_id)
            if player:
                await websocket.send(json.dumps({
                    'type': 'player_data',
                    'player': player
                }))
            else:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': f"Player not found: {player_id}"
                }))

        except Exception as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f"Failed to get player: {str(e)}"
            }))

    async def handle_update_player(self, websocket: websockets.WebSocketServerProtocol, message: Dict[str, Any]) -> None:
        """Handle player update request.

        Args:
            websocket (websockets.WebSocketServerProtocol): WebSocket connection.
            message (Dict[str, Any]): Message containing player updates.
        """
        try:
            player_id = message.get('player_id')
            updates = message.get('updates', {})

            if not player_id:
                raise ValueError("No player ID specified")

            if not updates:
                raise ValueError("No updates specified")

            self.db_manager.update_player(player_id, updates)

            # Get updated player data
            player = self.db_manager.get_player(player_id)
            if player:
                # Broadcast update to all game clients
                await self.broadcast_game(player['game_id'], {
                    'type': 'player_updated',
                    'player': player
                })

                # Send confirmation to the updating client
                await websocket.send(json.dumps({
                    'type': 'player_updated',
                    'player': player
                }))
            else:
                raise ValueError(f"Player not found: {player_id}")

        except Exception as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f"Failed to update player: {str(e)}"
            }))

    async def handle_get_game_players(self, websocket: websockets.WebSocketServerProtocol, message: Dict[str, Any]) -> None:
        """Handle game players retrieval request.

        Args:
            websocket (websockets.WebSocketServerProtocol): WebSocket connection.
            message (Dict[str, Any]): Message containing game ID.
        """
        try:
            game_id = message.get('game_id')
            if not game_id:
                raise ValueError("No game ID specified")

            players = self.db_manager.get_game_players(game_id)
            await websocket.send(json.dumps({
                'type': 'game_players',
                'game_id': game_id,
                'players': players
            }))

        except Exception as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f"Failed to get game players: {str(e)}"
            }))

    async def handle_get_player_by_role(self, websocket: websockets.WebSocketServerProtocol, message: Dict[str, Any]) -> None:
        """Handle player retrieval by role request.

        Args:
            websocket (websockets.WebSocketServerProtocol): WebSocket connection.
            message (Dict[str, Any]): Message containing game ID and role.
        """
        try:
            game_id = message.get('game_id')
            role = message.get('role')

            if not all([game_id, role]):
                raise ValueError("Missing game ID or role")

            if role not in ['attacker', 'defender']:
                raise ValueError("Invalid role. Must be 'attacker' or 'defender'")

            player = self.db_manager.get_player_by_role(game_id, role)
            if player:
                await websocket.send(json.dumps({
                    'type': 'player_data',
                    'player': player
                }))
            else:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': f"No {role} found for game: {game_id}"
                }))

        except Exception as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f"Failed to get player by role: {str(e)}"
            }))

    async def broadcast(self, message: Dict[str, Any], exclude: Optional[WebSocketServerProtocol] = None) -> None:
        """Broadcast a message to all connected clients.

        Args:
            message (Dict[str, Any]): The message to broadcast.
            exclude (Optional[WebSocketServerProtocol]): Client to exclude from broadcast.
        """
        await self.broadcast(message) 