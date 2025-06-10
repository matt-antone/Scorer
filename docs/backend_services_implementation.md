# Backend Services Implementation Plan

## 1. Network Manager Service

### Purpose

Manages WiFi connections, network scanning, and QR code generation for client connections.

### Components

#### Network Scanner

```python
class NetworkScanner:
    def __init__(self):
        self.available_networks = []
        self.current_network = None

    async def scan_networks(self):
        # Use nmcli or iwlist to scan
        # Return list of networks with:
        # - SSID
        # - Signal strength
        # - Security type
        # - Channel

    async def get_current_network(self):
        # Get current connection details
        # Return:
        # - SSID
        # - Signal strength
        # - IP address
        # - Connection status
```

#### Connection Manager

```python
class ConnectionManager:
    def __init__(self, network_scanner):
        self.scanner = network_scanner
        self.saved_networks = []

    async def connect_to_network(self, ssid, password=None):
        # Connect to specified network
        # Handle different security types
        # Return connection status

    async def save_network(self, ssid, password):
        # Save network credentials
        # Encrypt password
        # Update saved networks list

    async def forget_network(self, ssid):
        # Remove network from saved list
        # Update configuration
```

#### QR Code Generator

```python
class QRCodeGenerator:
    def __init__(self, host_ip, port):
        self.host_ip = host_ip
        self.port = port

    def generate_player1_url(self):
        return f"http://{self.host_ip}:{self.port}/player1"

    def generate_player2_url(self):
        return f"http://{self.host_ip}:{self.port}/player2"

    def generate_observer_url(self):
        return f"http://{self.host_ip}:{self.port}/observer"

    async def generate_qr_codes(self):
        # Generate QR codes for all URLs
        # Return as base64 encoded images
```

## 2. Update Service

### Purpose

Manages application updates, version checking, and installation.

### Components

#### Version Checker

```python
class VersionChecker:
    def __init__(self, current_version):
        self.current_version = current_version
        self.github_api_url = "https://api.github.com/repos/your-repo/releases"

    async def check_for_updates(self):
        # Check GitHub releases
        # Compare versions
        # Return update info if available

    def is_update_available(self, latest_version):
        # Compare version strings
        # Return True if update needed
```

#### Update Manager

```python
class UpdateManager:
    def __init__(self, version_checker):
        self.checker = version_checker
        self.download_path = "updates/"

    async def download_update(self, version):
        # Download release assets
        # Verify checksums
        # Return download status

    async def install_update(self, version):
        # Stop services
        # Backup current version
        # Install new version
        # Restart services
```

#### Version Tracker

```python
class VersionTracker:
    def __init__(self):
        self.version_file = "version.json"

    def get_current_version(self):
        # Read version from file
        # Return version info

    def update_version(self, new_version):
        # Update version file
        # Log version change
```

## 3. Asset Management Service

### Purpose

Manages application assets, particularly screensaver images and other media.

### Components

#### Asset Manager

```python
class AssetManager:
    def __init__(self, asset_dir):
        self.asset_dir = asset_dir
        self.screensaver_dir = f"{asset_dir}/screensaver"

    async def save_screensaver_image(self, image_data, filename):
        # Validate image
        # Process image (resize, optimize)
        # Save to screensaver directory
        # Update settings

    async def get_screensaver_image(self, filename):
        # Load image from storage
        # Return image data

    async def list_screensaver_images(self):
        # List available images
        # Return image info
```

#### Image Processor

```python
class ImageProcessor:
    def __init__(self):
        self.max_size = (800, 480)  # Target resolution
        self.max_file_size = 5 * 1024 * 1024  # 5MB

    async def process_image(self, image_data):
        # Validate image format
        # Check file size
        # Resize if needed
        # Optimize for display
        # Return processed image

    def validate_image(self, image_data):
        # Check format
        # Check dimensions
        # Check file size
        # Return validation result
```

#### Default Asset Manager

```python
class DefaultAssetManager:
    def __init__(self, asset_dir):
        self.asset_dir = asset_dir

    async def ensure_default_assets(self):
        # Check for default assets
        # Create if missing
        # Return status

    async def reset_to_defaults(self):
        # Remove custom assets
        # Restore defaults
        # Update settings
```

## 4. Service Integration

### Service Manager

```python
class ServiceManager:
    def __init__(self):
        self.network_manager = NetworkManager()
        self.update_service = UpdateService()
        self.asset_manager = AssetManager()

    async def start_services(self):
        # Initialize all services
        # Start background tasks
        # Return startup status

    async def stop_services(self):
        # Stop all services
        # Clean up resources
        # Return shutdown status
```

### Configuration

```python
# config.py
class ServiceConfig:
    # Network
    NETWORK_SCAN_INTERVAL = 30  # seconds
    MAX_SAVED_NETWORKS = 10

    # Updates
    UPDATE_CHECK_INTERVAL = 3600  # 1 hour
    GITHUB_REPO = "your-repo"

    # Assets
    ASSET_DIR = "assets"
    SCREENSAVER_DIR = "assets/billboards"
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
```

## 5. Implementation Plan

### Phase 1: Network Manager

1. Implement network scanning
2. Add connection management
3. Create QR code generation
4. Add network persistence

### Phase 2: Update Service

1. Implement version checking
2. Add update downloading
3. Create installation process
4. Add version tracking

### Phase 3: Asset Management

1. Implement asset storage
2. Add image processing
3. Create default assets
4. Add asset validation

### Phase 4: Integration

1. Create service manager
2. Add configuration
3. Implement startup/shutdown
4. Add error handling

## 6. Testing Plan

### Unit Tests

- Network scanning
- Connection management
- Version checking
- Image processing
- Asset management

### Integration Tests

- Service interaction
- Update process
- Network changes
- Asset updates

### System Tests

- Full update cycle
- Network reconnection
- Asset replacement
- Service recovery

## 7. Next Steps

1. Set up development environment
2. Create service structure
3. Implement core functionality
4. Add testing
5. Integrate with state server
6. Deploy and monitor
