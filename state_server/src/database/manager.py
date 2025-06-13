"""
Database manager implementation for the state server.
Handles all database operations and provides a high-level interface for data access.
"""

import sqlite3
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
from .schema import DatabaseSchema


class DatabaseError(Exception):
    """Base exception for database-related errors."""
    pass


class DatabaseManager:
    """Manages database operations for the state server."""

    def __init__(self, db_path: Path):
        """Initialize the database manager.

        Args:
            db_path (Path): Path to the SQLite database file.
        """
        self.db_path = db_path
        self.schema = DatabaseSchema()
        self._initialize_database()

    def _initialize_database(self) -> None:
        """Initialize the database with the schema."""
        try:
            self.schema.initialize_database(self.db_path)
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to initialize database: {str(e)}")

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with proper configuration.

        Returns:
            sqlite3.Connection: Configured database connection.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def begin_transaction(self) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
        """Begin a database transaction.

        Returns:
            Tuple[sqlite3.Connection, sqlite3.Cursor]: Connection and cursor for the transaction.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("BEGIN TRANSACTION")
        return conn, cursor

    def commit_transaction(self, conn: sqlite3.Connection) -> None:
        """Commit a database transaction.

        Args:
            conn (sqlite3.Connection): Database connection to commit.

        Raises:
            DatabaseError: If the commit fails.
        """
        try:
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise DatabaseError(f"Failed to commit transaction: {str(e)}")
        finally:
            conn.close()

    def rollback_transaction(self, conn: sqlite3.Connection) -> None:
        """Rollback a database transaction.

        Args:
            conn (sqlite3.Connection): Database connection to rollback.
        """
        try:
            conn.rollback()
        finally:
            conn.close()

    def create_game_state(self, game_id: str, initial_state: Dict[str, Any]) -> None:
        """Create a new game state.

        Args:
            game_id (str): Unique identifier for the game.
            initial_state (Dict[str, Any]): Initial game state data.

        Raises:
            DatabaseError: If the operation fails.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO game_state (
                        game_id, status, current_player, scores, timer, settings
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    game_id,
                    initial_state.get('status', 'not_started'),
                    initial_state.get('current_player'),
                    json.dumps(initial_state.get('scores', {})),
                    json.dumps(initial_state.get('timer', {})),
                    json.dumps(initial_state.get('settings', {}))
                ))
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to create game state: {str(e)}")

    def get_game_state(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Get the current state of a game.

        Args:
            game_id (str): Unique identifier for the game.

        Returns:
            Optional[Dict[str, Any]]: Game state data if found, None otherwise.

        Raises:
            DatabaseError: If the operation fails.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM game_state WHERE game_id = ?
                """, (game_id,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        'game_id': row['game_id'],
                        'status': row['status'],
                        'current_player': row['current_player'],
                        'scores': json.loads(row['scores']),
                        'timer': json.loads(row['timer']),
                        'settings': json.loads(row['settings']),
                        'created_at': row['created_at'],
                        'updated_at': row['updated_at']
                    }
                return None
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to get game state: {str(e)}")

    def update_game_state(self, game_id: str, updates: Dict[str, Any]) -> None:
        """Update the state of a game.

        Args:
            game_id (str): Unique identifier for the game.
            updates (Dict[str, Any]): Updates to apply to the game state.

        Raises:
            DatabaseError: If the operation fails.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Get current state
                current_state = self.get_game_state(game_id)
                if not current_state:
                    raise DatabaseError(f"Game state not found: {game_id}")
                
                # Prepare update data
                update_data = {
                    'status': updates.get('status', current_state['status']),
                    'current_player': updates.get('current_player', current_state['current_player']),
                    'scores': json.dumps(updates.get('scores', current_state['scores'])),
                    'timer': json.dumps(updates.get('timer', current_state['timer'])),
                    'settings': json.dumps(updates.get('settings', current_state['settings'])),
                    'updated_at': datetime.now().isoformat()
                }
                
                # Build update query
                set_clause = ', '.join(f"{k} = ?" for k in update_data.keys())
                cursor.execute(f"""
                    UPDATE game_state 
                    SET {set_clause}
                    WHERE game_id = ?
                """, (*update_data.values(), game_id))
                
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to update game state: {str(e)}")

    def delete_game_state(self, game_id: str) -> None:
        """Delete a game state and all related data.

        Args:
            game_id (str): Unique identifier for the game.

        Raises:
            DatabaseError: If the operation fails.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Delete related data first
                cursor.execute("DELETE FROM scores WHERE game_id = ?", (game_id,))
                cursor.execute("DELETE FROM timers WHERE game_id = ?", (game_id,))
                cursor.execute("DELETE FROM settings WHERE game_id = ?", (game_id,))
                
                # Delete game state
                cursor.execute("DELETE FROM game_state WHERE game_id = ?", (game_id,))
                
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to delete game state: {str(e)}")

    def get_active_games(self) -> List[Dict[str, Any]]:
        """Get a list of all active games.

        Returns:
            List[Dict[str, Any]]: List of active game states.

        Raises:
            DatabaseError: If the operation fails.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM game_state 
                    WHERE status != 'completed'
                    ORDER BY created_at DESC
                """)
                
                return [{
                    'game_id': row['game_id'],
                    'status': row['status'],
                    'current_player': row['current_player'],
                    'scores': json.loads(row['scores']),
                    'timer': json.loads(row['timer']),
                    'settings': json.loads(row['settings']),
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                } for row in cursor.fetchall()]
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to get active games: {str(e)}")
