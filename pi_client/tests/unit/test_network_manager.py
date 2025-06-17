import unittest
from unittest.mock import patch, MagicMock
import socket
import pytest
from kivy.clock import Clock
from pi_client.network.network_manager import NetworkManager
from pi_client.screens.splash_screen import SplashScreen

class TestNetworkManager(unittest.TestCase):
    """Test suite for network manager functionality."""

    def setUp(self):
        """Set up test environment."""
        self.network_manager = NetworkManager()
        # Ensure we're not affecting real network
        self.network_manager._check_interval = 0.1  # Short interval for testing

    def tearDown(self):
        """Clean up test environment."""
        self.network_manager.stop()
        Clock.unschedule(self.network_manager._check_network)

    @patch('socket.socket')
    def test_initial_network_check(self, mock_socket):
        """Test initial network check."""
        # Mock successful connection
        mock_socket.return_value.__enter__.return_value.connect.return_value = None
        
        # Create splash screen
        screen = SplashScreen()
        
        # Trigger network check
        screen.check_network()
        
        # Verify network state
        assert screen.system_checks['network'] is True
        assert screen.loading_status == 'Checking network...'
        assert screen.loading_progress == 20

    @patch('socket.socket')
    def test_network_failure(self, mock_socket):
        """Test network check failure."""
        # Mock connection failure
        mock_socket.return_value.__enter__.return_value.connect.side_effect = OSError
        
        # Create splash screen
        screen = SplashScreen()
        
        # Trigger network check
        screen.check_network()
        
        # Verify error state
        assert screen.system_checks['network'] is False
        assert screen.has_error is True
        assert "Network connection failed" in screen.error_message

    @patch('socket.socket')
    def test_network_recovery(self, mock_socket):
        """Test network recovery after failure."""
        # Mock initial failure then success
        mock_socket.return_value.__enter__.return_value.connect.side_effect = [
            OSError,  # First call fails
            None      # Second call succeeds
        ]
        
        # Create splash screen
        screen = SplashScreen()
        
        # Trigger initial check (fails)
        screen.check_network()
        assert screen.system_checks['network'] is False
        
        # Trigger recovery
        screen.recover_from_network_error()
        
        # Verify recovery
        assert screen.system_checks['network'] is True
        assert screen.has_error is False

    def test_connection_manager_popup(self):
        """Test connection manager popup behavior."""
        # Create splash screen
        screen = SplashScreen()
        
        # Simulate network failure
        screen.handle_network_error()
        
        # Verify popup is shown
        assert hasattr(screen, 'connection_popup')
        assert screen.connection_popup.is_open is True
        
        # Verify popup content
        assert "Network connection failed" in screen.connection_popup.title
        assert screen.connection_popup.ids.retry_button is not None
        assert screen.connection_popup.ids.close_button is not None

    @patch('socket.socket')
    def test_periodic_network_check(self, mock_socket):
        """Test periodic network checking."""
        # Mock successful connection
        mock_socket.return_value.__enter__.return_value.connect.return_value = None
        
        # Create splash screen
        screen = SplashScreen()
        
        # Start periodic checks
        screen.start_loading()
        
        # Advance time to trigger checks
        Clock.tick()
        
        # Verify checks were performed
        assert screen.system_checks['network'] is True
        assert screen._loading_timeout is not None

    def test_network_state_persistence(self):
        """Test network state persistence in game state."""
        # Create splash screen
        screen = SplashScreen()
        
        # Set network state
        screen.system_checks['network'] = True
        
        # Verify state is persisted
        app = MagicMock()
        app.game_state = {}
        screen.update_loading_progress(20, "Network connected")
        
        assert app.game_state['system_checks']['network'] is True
        assert app.game_state['loading_status'] == "Network connected"

    @patch('socket.socket')
    def test_multiple_interface_check(self, mock_socket):
        """Test checking multiple network interfaces."""
        # Mock different interfaces
        mock_socket.return_value.__enter__.return_value.connect.side_effect = [
            OSError,  # First interface fails
            None      # Second interface succeeds
        ]
        
        # Create splash screen
        screen = SplashScreen()
        
        # Trigger network check
        screen.check_network()
        
        # Verify successful connection
        assert screen.system_checks['network'] is True
        assert screen.has_error is False

    def test_network_error_messages(self):
        """Test different network error messages."""
        # Create splash screen
        screen = SplashScreen()
        
        # Test no interfaces
        screen.handle_network_error("No network interfaces available")
        assert "No network interfaces available" in screen.error_message
        
        # Test no internet
        screen.handle_network_error("No internet connection")
        assert "No internet connection" in screen.error_message
        
        # Test no local network
        screen.handle_network_error("No local network")
        assert "No local network" in screen.error_message
        
        # Test timeout
        screen.handle_network_error("Connection timeout")
        assert "Connection timeout" in screen.error_message

if __name__ == '__main__':
    unittest.main() 