#!/bin/bash
# Platform: macOS and Raspberry Pi
# This script handles both environments with platform detection
# - On macOS: Uses default SDL2 settings
# - On Raspberry Pi: Configures KMSDRM and DSI display settings

# Navigate to the application directory
cd "$(dirname "$0")"

# Activate the Python virtual environment
source venv/bin/activate

# Check if we're running on Raspberry Pi
if [ "$(uname -m)" = "aarch64" ]; then
    # Raspberry Pi specific settings
    echo "Running on Raspberry Pi - setting Pi-specific environment variables"
    
    # Set KIVY_BCM_DISPMANX_ID for camera/display socket 1
    export KIVY_BCM_DISPMANX_ID=5

    # Enable SDL2 debug logging
    export SDL_LOG_PRIORITY=VERBOSE
    export SDL_LOG_CATEGORY_VIDEO=VERBOSE

    # Set SDL2/KMSDRM environment variables
    export SDL_VIDEODRIVER=kmsdrm
    export SDL_VIDEODRIVER_DEVICE=/dev/dri/card1
    export SDL_VIDEO_KMSDRM_DEVICE=/dev/dri/card1
    export SDL_VIDEO_KMSDRM_CRTC=34
    export SDL_VIDEO_KMSDRM_CONNECTOR=36
else
    # macOS specific settings
    echo "Running on macOS - using default SDL2 settings"
    export KIVY_WINDOW=sdl2
fi

# Run the Kivy application
python main.py 