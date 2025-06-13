"""
Database schema implementation for the state server.
Defines the structure of the SQLite database and provides initialization methods.
"""

import sqlite3
from typing import Dict, Any
from pathlib import Path


class DatabaseSchema:
    """Defines and manages the database schema for the state server."""

    def __init__(self):
        """Initialize the database schema with table definitions."""
        self.tables = {
            'game_state': {
                'game_id': 'TEXT PRIMARY KEY',
                'status': 'TEXT NOT NULL',
                'current_player': 'TEXT',
                'scores': 'JSON NOT NULL',
                'timer': 'JSON',
                'settings': 'JSON NOT NULL',
                'created_at': 'DATETIME DEFAULT CURRENT_TIMESTAMP',
                'updated_at': 'DATETIME DEFAULT CURRENT_TIMESTAMP'
            },
            'scores': {
                'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'game_id': 'TEXT NOT NULL',
                'player_id': 'TEXT NOT NULL',
                'score': 'INTEGER NOT NULL',
                'timestamp': 'DATETIME DEFAULT CURRENT_TIMESTAMP',
                'FOREIGN KEY(game_id)': 'REFERENCES game_state(game_id)'
            },
            'timers': {
                'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'game_id': 'TEXT NOT NULL',
                'player_id': 'TEXT NOT NULL',
                'time_remaining': 'INTEGER NOT NULL',
                'timestamp': 'DATETIME DEFAULT CURRENT_TIMESTAMP',
                'FOREIGN KEY(game_id)': 'REFERENCES game_state(game_id)'
            },
            'settings': {
                'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'game_id': 'TEXT NOT NULL',
                'setting_key': 'TEXT NOT NULL',
                'setting_value': 'TEXT NOT NULL',
                'timestamp': 'DATETIME DEFAULT CURRENT_TIMESTAMP',
                'FOREIGN KEY(game_id)': 'REFERENCES game_state(game_id)'
            }
        }

    def get_create_table_statements(self) -> Dict[str, str]:
        """Generate CREATE TABLE statements for all tables.

        Returns:
            Dict[str, str]: Dictionary mapping table names to their CREATE TABLE statements.
        """
        statements = {}
        for table_name, columns in self.tables.items():
            column_defs = []
            for col_name, col_def in columns.items():
                if col_name.startswith('FOREIGN KEY'):
                    column_defs.append(col_def)
                else:
                    column_defs.append(f"{col_name} {col_def}")
            
            statements[table_name] = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {', '.join(column_defs)}
                )
            """
        return statements

    def initialize_database(self, db_path: Path) -> None:
        """Initialize the database with the defined schema.

        Args:
            db_path (Path): Path to the SQLite database file.

        Raises:
            sqlite3.Error: If there's an error creating the database or tables.
        """
        try:
            # Create database directory if it doesn't exist
            db_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Connect to database
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                
                # Create tables
                for table_name, create_stmt in self.get_create_table_statements().items():
                    cursor.execute(create_stmt)
                
                # Create indexes
                self._create_indexes(cursor)
                
                # Enable foreign keys
                cursor.execute("PRAGMA foreign_keys = ON")
                
                conn.commit()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to initialize database: {str(e)}")

    def _create_indexes(self, cursor: sqlite3.Cursor) -> None:
        """Create necessary indexes for the database.

        Args:
            cursor (sqlite3.Cursor): SQLite cursor for executing statements.
        """
        # Index for scores table
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_scores_game_id 
            ON scores(game_id)
        """)
        
        # Index for timers table
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timers_game_id 
            ON timers(game_id)
        """)
        
        # Index for settings table
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_settings_game_id 
            ON settings(game_id)
        """)
        
        # Composite index for settings
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_settings_game_key 
            ON settings(game_id, setting_key)
        """)
