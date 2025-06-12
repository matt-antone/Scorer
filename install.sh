#!/bin/bash
set -e

# Set up logging
LOG_FILE="install.log"
exec 1> >(tee -a "$LOG_FILE")
exec 2> >(tee -a "$LOG_FILE" >&2)

echo ">>> Starting Scorer installation at $(date)"

# Refuse to run as root
if [ "$EUID" -eq 0 ]; then
  echo "ERROR: Do not run this script as root or with sudo. Dependencies must be installed as your user."
  exit 1
fi

echo ">>> Starting Scorer installation..."

# Detect platform
if [ -f /proc/device-tree/model ] && grep -q "Raspberry Pi" /proc/device-tree/model; then
    echo ">>> Detected Raspberry Pi environment..."
    # Install system dependencies using apt
    echo ">>> Installing system dependencies..."
    sudo apt-get update
    sudo apt-get install -y \
        python3-venv \
        python3-pip \
        libffi-dev \
        libsdl2-dev \
        libsdl2-image-dev \
        libsdl2-mixer-dev \
        libsdl2-ttf-dev \
        ffmpeg \
        libavdevice-dev \
        libavfilter-dev \
        libavformat-dev \
        libavcodec-dev \
        libswresample-dev \
        libswscale-dev \
        libavutil-dev
elif [ "$(uname)" == "Darwin" ]; then
    echo ">>> Detected macOS environment..."
    # Check for Homebrew
    if ! command -v brew &> /dev/null; then
        echo "Homebrew is not installed. Please install Homebrew first: https://brew.sh/"
        exit 1
    fi

    # Install and link Homebrew dependencies
    echo ">>> Installing Homebrew dependencies..."
    brew install ffmpeg@6 sdl2 sdl2_image sdl2_mixer sdl2_ttf
    brew link ffmpeg@6 --force

    # Set up environment variables for ffmpeg
    export LDFLAGS="-L/opt/homebrew/opt/ffmpeg@6/lib"
    export CPPFLAGS="-I/opt/homebrew/opt/ffmpeg@6/include"
else
    echo "ERROR: Unsupported platform. This script only supports Raspberry Pi and macOS."
    exit 1
fi

# Install Pi App dependencies
echo ">>> Installing Pi App Python dependencies..."
cd pi_app
python3 -m venv .venv || true
source .venv/bin/activate
pip install --upgrade pip

# Install dependencies in the correct order
echo ">>> Installing core dependencies..."
pip install -r ../requirements.txt

# Install ffpyplayer from source
echo ">>> Installing ffpyplayer from source..."
USE_SYSTEM_LIBS=1 pip install --no-binary ffpyplayer ffpyplayer==4.5.2

# Run Alembic migrations if config exists
if [ -f ../state_server/db/alembic.ini ]; then
    echo ">>> Running Alembic migrations..."
    cd ../state_server
    source ../pi_app/.venv/bin/activate
    
    # Check if migrations directory is empty
    if [ ! "$(ls -A db/migrations/versions/*.py 2>/dev/null)" ]; then
        echo ">>> Generating initial migration..."
        alembic -c db/alembic.ini revision --autogenerate -m "Initial migration"
    fi
    
    # Run migrations
    echo ">>> Applying migrations..."
    alembic -c db/alembic.ini upgrade head
    cd ../pi_app
else
    echo "Alembic config not found at state_server/db/alembic.ini, skipping migrations."
fi

cd ..

# Offer display rotation for Raspberry Pi
if [ -f /proc/device-tree/model ] && grep -q "Raspberry Pi" /proc/device-tree/model; then
    echo ""
    read -p "Do you want to rotate the display 180 degrees for upside-down mounting? (y/n): " rotate
    if [ "$rotate" = "y" ] || [ "$rotate" = "Y" ]; then
        # Remove any previous rotation lines to avoid duplicates
        sudo sed -i '/^display_lcd_rotate=/d' /boot/config.txt
        sudo sed -i '/^display_hdmi_rotate=/d' /boot/config.txt
        # Add the new rotation line (for most Pi screens)
        echo "display_lcd_rotate=2" | sudo tee -a /boot/config.txt
        echo "Display rotation set to 180 degrees. Please reboot for changes to take effect."
    else
        echo "Display rotation unchanged."
    fi
fi

echo ">>> Installation complete at $(date)!" 