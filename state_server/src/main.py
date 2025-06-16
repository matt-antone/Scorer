"""
Main entry point for the state server.
Initializes and runs the WebSocket server.
"""

import asyncio
import logging
from pathlib import Path
from database.manager import DatabaseManager
from websocket.server import WebSocketServer


def setup_logging() -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


async def main() -> None:
    """Main entry point for the state server."""
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Initialize database
        db_path = Path("state.db")
        db_manager = DatabaseManager(db_path)
        logger.info("Database initialized")

        # Initialize WebSocket server
        server = WebSocketServer(db_manager)
        host = "0.0.0.0"  # Listen on all interfaces
        port = 8765  # Default WebSocket port

        logger.info(f"Starting WebSocket server on {host}:{port}")
        await server.start(host, port)

    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server failed: {str(e)}") 