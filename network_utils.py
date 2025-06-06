# network_utils.py
# This file will contain Raspberry Pi-specific network management functions.
import platform
import subprocess
import socket

def get_local_ip():
    """Gets the local IP address of the device."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def check_network_connection():
    """Checks for a valid network connection by trying to get a non-localhost IP."""
    ip = get_local_ip()
    if ip and not ip.startswith('127.'):
        return True, ip
    return False, None

def is_raspberry_pi():
    """Check if the current platform is a Raspberry Pi."""
    return platform.system() == "Linux"

def scan_wifi_networks():
    """Scans for available Wi-Fi networks using nmcli."""
    if not is_raspberry_pi():
        return ["Not on Pi - WiFi 1", "Not on Pi - WiFi 2 (Secured)"]
    
    try:
        # Rescan first to get the most up-to-date list
        subprocess.run(['nmcli', 'dev', 'wifi', 'rescan'], check=True, capture_output=True)
        # Get the list of available Wi-Fi networks
        result = subprocess.run(
            ['nmcli', '-f', 'SSID', 'dev', 'wifi'],
            check=True,
            capture_output=True,
            text=True
        )
        # Process the output
        lines = result.stdout.strip().split('\n')
        networks = [line.strip() for line in lines[1:] if line.strip()] # Skip header and empty lines
        # Remove duplicates
        unique_networks = sorted(list(set(networks)))
        return unique_networks
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error scanning for Wi-Fi networks: {e}")
        return ["Error scanning networks"]

def connect_to_wifi(ssid, password):
    """Connects to a Wi-Fi network using nmcli."""
    if not is_raspberry_pi():
        print(f"Simulating connection to {ssid} on non-Pi device.")
        return True, "Connected successfully (simulation)."
        
    try:
        command = ['nmcli', 'dev', 'wifi', 'connect', ssid]
        if password:
            command.extend(['password', password])
        
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=30 # 30-second timeout for connection attempt
        )
        if "successfully activated" in result.stdout:
            return True, f"Successfully connected to {ssid}."
        else:
            return False, f"Failed to connect to {ssid}. Reason unknown."
            
    except subprocess.TimeoutExpired:
        return False, f"Connection to {ssid} timed out."
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        return False, f"Failed to connect to {ssid}: {error_message}"
    except FileNotFoundError:
        return False, "Error: 'nmcli' command not found. Is NetworkManager installed?" 