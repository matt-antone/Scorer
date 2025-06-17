import socket
import logging
import threading
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, StringProperty, DictProperty
import time

logger = logging.getLogger(__name__)

class NetworkManager(EventDispatcher):
    """Manages network connectivity and monitoring."""

    is_connected = BooleanProperty(False)
    connection_type = StringProperty('')
    ip_address = StringProperty('')
    network_info = DictProperty({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._monitor_thread = None
        self._stop_monitoring = False
        self._interfaces = self._get_network_interfaces()
        self.register_event_type('on_network_state_change')
        self.register_event_type('on_network_error')

    def start_monitoring(self):
        """Start network monitoring in background thread."""
        if self._monitor_thread and self._monitor_thread.is_alive():
            return

        self._stop_monitoring = False
        self._monitor_thread = threading.Thread(target=self._monitor_network)
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def stop_monitoring(self):
        """Stop network monitoring."""
        self._stop_monitoring = True
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1.0)
            self._monitor_thread = None

    def _monitor_network(self):
        """Monitor network status in background thread."""
        while not self._stop_monitoring:
            try:
                self.check_network()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                self.dispatch('on_network_error', str(e))

    def check_network(self):
        """Check network connectivity."""
        try:
            # Check internet connectivity
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                internet_connected = True
            except OSError:
                internet_connected = False

            # Check local network
            interfaces = self._get_network_interfaces()
            if not interfaces:
                raise Exception("No network interfaces available")

            # Update state
            was_connected = self.is_connected
            self.is_connected = internet_connected
            # Always set connection_type as a string
            if 'wlan' in interfaces[0].lower():
                self.connection_type = 'WiFi'
            elif 'eth' in interfaces[0].lower():
                self.connection_type = 'Ethernet'
            else:
                self.connection_type = ''
            self.ip_address = interfaces[0]

            # Dispatch events if state changed
            if was_connected != self.is_connected:
                self.dispatch('on_network_state_change', 
                            self.is_connected,
                            self.connection_type,
                            self.ip_address)

        except Exception as e:
            self.is_connected = False
            self.connection_type = ''  # Always a string
            self.dispatch('on_network_error', str(e))
            raise

    def _check_network(self):
        """Alias for check_network for test compatibility."""
        return self.check_network()

    def _get_network_interfaces(self):
        """Get available network interfaces and their IP addresses."""
        interfaces = []
        try:
            # Get all network interfaces
            for interface in socket.getaddrinfo(socket.gethostname(), None):
                if interface[0] == socket.AF_INET:  # IPv4 only
                    ip = interface[4][0]
                    if not ip.startswith('127.'):  # Skip localhost
                        interfaces.append(ip)
        except Exception as e:
            logger.error(f"NetworkManager: Error getting interfaces: {str(e)}")
        return interfaces

    def on_network_state_change(self, is_connected, connection_type, ip_address):
        """Event handler for network state changes."""
        pass

    def on_network_error(self, error_message):
        """Event handler for network errors."""
        pass

    def stop(self):
        """Alias for stop_monitoring for test compatibility."""
        self.stop_monitoring() 