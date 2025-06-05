#!/bin/bash

# Script to install Scorer Kivy application dependencies and set it up as a systemd service for kiosk mode.

echo "--- Scorer Full Kiosk Installation Script ---"
echo "IMPORTANT: This script should be run with sudo."
echo "It assumes you are running it from within the 'Scorer' project directory on the Raspberry Pi."
echo "It also assumes the Pi is configured to boot to Command Line Interface (CLI)."
echo "Please ensure network connectivity for downloading packages."
echo ""

# --- Safety Check: Ensure running with sudo ---
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root using sudo."
  exit 1
fi

# --- Configuration ---
APP_USER="${SUDO_USER:-pi}" # User who will run the app (owner of the files)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # Should be /path/to/Scorer
APP_WORKING_DIR="$SCRIPT_DIR"
MAIN_SCRIPT_PATH="$APP_WORKING_DIR/main.py"
PYTHON_EXECUTABLE=$(which python3)
VENV_DIR="$APP_WORKING_DIR/.venv" # Virtual environment directory

SERVICE_FILE_NAME="scorer.service"
SERVICE_FILE_PATH="/etc/systemd/system/$SERVICE_FILE_NAME"

echo "--- Detected Settings ---"
echo "Application User: $APP_USER"
echo "Project Directory (App Working Dir): $APP_WORKING_DIR"
echo "Main Script Path: $MAIN_SCRIPT_PATH"
echo "Python3 System Interpreter: $PYTHON_EXECUTABLE"
echo "Virtual Environment will be at: $VENV_DIR"
echo "Systemd Service File: $SERVICE_FILE_PATH"
echo ""

# --- Function to ask for user confirmation ---
confirm() {
    # call with a prompt string or use a default
    read -r -p "${1:-Are you sure? [y/N]} " response
    case "$response" in
        [yY][eE][sS]|[yY])
            true
            ;;
        *)
            false
            ;;
    esac
}

echo "This script will perform the following actions:"
echo "1. Update package lists (apt update)."
echo "2. Install system-level dependencies for Kivy (SDL2, graphics libs, etc.)."
echo "3. Create a Python virtual environment at '$VENV_DIR'."
echo "4. Install Kivy and other Python dependencies (e.g., Pillow) into the virtual environment."
echo "5. Create and enable a systemd service ('$SERVICE_FILE_NAME') to auto-start the Scorer app."
echo ""

if ! confirm "Proceed with installation? [y/N]"; then
    echo "Installation aborted by user."
    exit 0
fi

# --- 1. Update package lists ---
echo ""
echo "--- Updating package lists (sudo apt update) ---"
sudo apt update
if [ $? -ne 0 ]; then echo "Error during apt update. Exiting."; exit 1; fi

# --- 2. Install system-level dependencies for Kivy ---
# These are typical dependencies for Kivy on Debian-based systems like Raspberry Pi OS.
# This list is comprehensive and might include some already installed.
echo ""
echo "--- Installing system-level dependencies for Kivy ---"
sudo apt install -y build-essential git libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev pkg-config libgl1-mesa-dev libgles2-mesa-dev python3-setuptools libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-alsa gstreamer1.0-libav python3-dev libmtdev-dev libjpeg-dev libpng-dev libtiff5-dev libwebp-dev libffi-dev librsvg2-bin
    # xclip xsel # Only if you need clipboard on X11, not typical for kiosk

if [ $? -ne 0 ]; then echo "Error installing system dependencies. Exiting."; exit 1; fi
echo "System dependencies installed."

# --- 2.1 Install SDL2 build dependencies ---
echo ""
echo "--- Installing SDL2 build dependencies ---"
sudo apt install -y build-essential git autoconf automake libtool pkg-config \
    libasound2-dev libpulse-dev libaudio-dev libx11-dev libxext-dev \
    libxrandr-dev libxcursor-dev libxi-dev libxinerama-dev libxxf86vm-dev \
    libxss-dev libgl1-mesa-dev libdbus-1-dev libudev-dev \
    libgles2-mesa-dev libegl1-mesa-dev libibus-1.0-dev \
    libdrm-dev libgbm-dev libinput-dev libudev-dev libxkbcommon-dev

if [ $? -ne 0 ]; then echo "Error installing SDL2 build dependencies. Exiting."; exit 1; fi
echo "SDL2 build dependencies installed."

# --- 2.2 Build and install SDL2 with KMSDRM support ---
echo ""
echo "--- Building SDL2 with KMSDRM support ---"
echo "This may take several minutes..."

# Create a temporary directory for the build
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Clone SDL2 repository
echo "Cloning SDL2 repository..."
git clone https://github.com/libsdl-org/SDL.git
if [ $? -ne 0 ]; then echo "Error cloning SDL2 repository. Exiting."; exit 1; fi

cd SDL

# Configure SDL2 with KMSDRM support
echo "Configuring SDL2..."
./configure --enable-video-kmsdrm \
    --enable-video-opengl \
    --enable-video-opengles \
    --enable-video-opengles2 \
    --enable-video-egl \
    --enable-video-gbm \
    --enable-video-dummy \
    --enable-video-x11 \
    --enable-video-wayland \
    --enable-video-rpi \
    --enable-video-vivante \
    --enable-video-cocoa \
    --enable-video-metal \
    --enable-video-vulkan \
    --enable-video-offscreen

if [ $? -ne 0 ]; then echo "Error configuring SDL2. Exiting."; exit 1; fi

# Build SDL2
echo "Building SDL2..."
make -j4
if [ $? -ne 0 ]; then echo "Error building SDL2. Exiting."; exit 1; fi

# Install SDL2
echo "Installing SDL2..."
sudo make install
if [ $? -ne 0 ]; then echo "Error installing SDL2. Exiting."; exit 1; fi

# Update shared library cache
echo "Updating shared library cache..."
sudo ldconfig
if [ $? -ne 0 ]; then echo "Error updating shared library cache. Exiting."; exit 1; fi

# Clean up
cd "$SCRIPT_DIR"
rm -rf "$TEMP_DIR"

echo "SDL2 with KMSDRM support installed successfully."

# --- 3. Create Python virtual environment ---
echo ""
echo "--- Setting up Python virtual environment at $VENV_DIR ---"
if [ -z "$PYTHON_EXECUTABLE" ]; then
    echo "Error: python3 interpreter not found. Cannot create virtual environment."
    exit 1
fi

# Ensure python3-venv is installed
sudo apt install -y python3-venv
if [ $? -ne 0 ]; then echo "Error installing python3-venv. Exiting."; exit 1; fi


if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    sudo -u "$APP_USER" "$PYTHON_EXECUTABLE" -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then echo "Error creating virtual environment. Exiting."; exit 1; fi
else
    echo "Virtual environment already exists. Skipping creation."
fi
echo "Virtual environment setup."

# Define Python executable within the venv for subsequent steps
VENV_PYTHON_EXECUTABLE="$VENV_DIR/bin/python3"
VENV_PIP_EXECUTABLE="$VENV_DIR/bin/pip3"

# --- 4. Install Kivy and other Python dependencies into the virtual environment ---
echo ""
echo "--- Installing Kivy and Python dependencies into virtual environment ---"
# Activate venv for the current user for pip install (might need sudo -u $APP_USER for pip if permissions are an issue)
# Using direct path to pip executable is safer in scripts
echo "Installing Kivy (this may take a while)..."
sudo -H -u "$APP_USER" "$VENV_PIP_EXECUTABLE" install kivy # Use stable Kivy from PyPI
# Consider \`kivy[base,media,full]\` or \`kivy_examples\` if you need more
# For specific Pi wheels if standard install fails:
# sudo "$VENV_PIP_EXECUTABLE" install https://github.com/kivy-garden/kivy-garden/archive/master.zip
# sudo "$VENV_PIP_EXECUTABLE" install https://github.com/kivy/kivy/archive/master.zip # Bleeding edge Kivy

if [ $? -ne 0 ]; then echo "Error installing Kivy. Check logs and dependencies. Exiting."; exit 1; fi
echo "Kivy installed."

echo "Installing Pillow (for image handling)..."
sudo -H -u "$APP_USER" "$VENV_PIP_EXECUTABLE" install Pillow
if [ $? -ne 0 ]; then echo "Error installing Pillow. Exiting."; exit 1; fi
echo "Pillow installed."

# Add any other Python dependencies your Scorer app needs here.
# For example, if you had a requirements.txt:
# if [ -f "$APP_WORKING_DIR/requirements.txt" ]; then
#     echo "Installing dependencies from requirements.txt..."
#     sudo -H -u "$APP_USER" "$VENV_PIP_EXECUTABLE" install -r "$APP_WORKING_DIR/requirements.txt"
#     if [ $? -ne 0 ]; then echo "Error installing from requirements.txt. Exiting."; exit 1; fi
# else
#     echo "No requirements.txt found. Skipping."
# fi

# --- 5. Create and enable systemd service ---
echo ""
echo "--- Creating and enabling systemd service: $SERVICE_FILE_NAME ---"
SERVICE_CONTENT=$(cat <<EOF
[Unit]
Description=Scorer Kivy Application
After=network.target multi-user.target
# If Kivy shows display errors related to X11 or Wayland not being found,
# and you're certain you need a graphical server context even for KMS/DRM:
# Wants=graphical.target
# After=graphical.target

[Service]
Type=simple
User=$APP_USER
WorkingDirectory=$APP_WORKING_DIR
ExecStart=$VENV_PYTHON_EXECUTABLE $MAIN_SCRIPT_PATH

# Environment variables for Kivy on Raspberry Pi (headless/CLI boot)
# Environment="DISPLAY=:0" # REMOVED - to avoid X11 attempts if not present/intended
# Environment="KIVY_BCM_DISPMANX_ID=4" # REMOVED - for older Pi display manager
Environment="KIVY_LOG_LEVEL=debug"   # For troubleshooting startup issues. Can be changed to 'info' or 'warning' in production.
# KIVY_WINDOW=sdl2 and KIVY_GRAPHICS=gles are often defaults but can be set if auto-detection fails.
# Forcing specific KMS/DRM settings might be needed if problems persist, e.g.:
# Environment="KIVY_GRAPHICS_BACKEND=drm" # Or similar depending on Kivy version & RPi setup
# Environment="KIVY_WINDOW_SYSTEM=egl"   # If EGL is the target

# Access to input devices is crucial for touchscreens
SupplementaryGroups=input video render tty

StandardOutput=journal
StandardError=journal
Restart=on-failure
RestartSec=10s
# RestartPreventExitStatus=255 # If Kivy has a clean exit code you want to respect

[Install]
WantedBy=multi-user.target
# WantedBy=graphical.target # If used above
EOF
)

echo "Creating systemd service file at $SERVICE_FILE_PATH..."
echo "$SERVICE_CONTENT" | sudo tee "$SERVICE_FILE_PATH" > /dev/null
if [ $? -ne 0 ]; then echo "Error writing service file. Exiting."; exit 1; fi
echo "Service file created."

# Set correct ownership for the project directory if the script created/modified files as root
# This ensures the $APP_USER can access its own files.
echo "Setting ownership of $APP_WORKING_DIR to $APP_USER..."
sudo chown -R "$APP_USER:$APP_USER" "$APP_WORKING_DIR"

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling $SERVICE_FILE_NAME..."
sudo systemctl enable "$SERVICE_FILE_NAME"
if [ $? -ne 0 ]; then echo "Error enabling service. Exiting."; exit 1; fi
echo "Service enabled."

# --- Final Instructions ---
echo ""
echo "--- Installation Successfully Completed ---"
echo "The Scorer application has been configured to run as a service ($SERVICE_FILE_NAME)."
echo "It should start automatically on the next boot (assuming the Pi boots to CLI)."
echo ""
echo "To manage the service:"
echo "  Start:   sudo systemctl start $SERVICE_FILE_NAME"
echo "  Stop:    sudo systemctl stop $SERVICE_FILE_NAME"
echo "  Status:  sudo systemctl status $SERVICE_FILE_NAME"
echo "  Logs:    journalctl -u $SERVICE_FILE_NAME -f"
echo ""
echo "Make sure your Raspberry Pi is configured to boot to the Command Line Interface (CLI)."
echo "You can do this via 'sudo raspi-config' -> System Options -> Boot / Auto Login -> Console or Console Autologin."
echo ""
echo "Reboot the Raspberry Pi now to test the auto-start: sudo reboot"
echo "--- End of Script ---" 