#!/bin/bash

echo "Starting Scorer App installation on Raspberry Pi..."

# Exit immediately if a command exits with a non-zero status.
set -e

# 1. Update package lists
echo "Updating package lists..."
# sudo apt-get update
# Temporarily commenting out sudo commands as the agent cannot run them directly.
# The user will need to uncomment and run these manually or run the script with sudo if needed.
echo "[USER ACTION REQUIRED] Please uncomment and run 'sudo apt-get update' if needed."

# 2. Install Kivy system dependencies
# Note: Some of these might already be installed on your Raspberry Pi OS image.
# This list is comprehensive for a bare-bones system.
echo "Installing Kivy system dependencies (if not already present)..."
echo "[USER ACTION REQUIRED] Please uncomment the following apt-get install command and run it, or install these packages manually:"
echo "# sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \"
#      pkg-config libgl1-mesa-dev libgles2-mesa-dev python3-setuptools libgstreamer1.0-dev \"
#      git-core gstreamer1.0-plugins-{bad,base,good,ugly} gstreamer1.0-omx \"
#      libmtdev-dev xclip xsel libjpeg-dev python3-pip python3-venv"
echo "Skipping direct execution of apt-get install due to permission constraints."

# 3. Install/Upgrade pip, setuptools, and virtualenv for the current user
# This uses python3, assuming it's the default Python 3 interpreter on the Pi.
echo "Upgrading pip, setuptools, and virtualenv for Python 3..."
python3 -m pip install --upgrade pip setuptools virtualenv --user

# Ensure the user's local bin directory is in PATH if it's not already for virtualenv
# This is often handled by default in ~/.bashrc or ~/.profile on new logins
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "Adding $HOME/.local/bin to PATH for this session."
    export PATH="$HOME/.local/bin:$PATH"
    echo "You might want to add 'export PATH=\"$HOME/.local/bin:\$PATH\"' to your ~/.bashrc or ~/.profile and re-login for this to be permanent."
fi

# 4. Create a Python virtual environment
PROJECT_DIR=$(pwd) # Assumes the script is run from the project root
VENV_DIR="$PROJECT_DIR/venv"

echo "Creating Python virtual environment at $VENV_DIR..."
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment '$VENV_DIR' already exists. Skipping creation."
else
    python3 -m virtualenv "$VENV_DIR"
fi

# 5. Activate the virtual environment (for the context of this script)
# The user will need to activate it manually in their terminal later.
source "$VENV_DIR/bin/activate"
echo "Activated virtual environment for this script execution."

# 6. Install Python packages from requirements.txt
echo "Installing Python packages from requirements.txt..."
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements.txt"
else
    echo "Error: requirements.txt not found in $PROJECT_DIR. Cannot install Python packages."
    exit 1
fi

echo "-----------------------------------------------------"
echo "Installation and setup script finished."
echo ""
echo "NEXT STEPS:"
echo "1. If you haven't already, ensure system dependencies were installed (you might need to run some 'sudo apt-get install ...' commands from above manually)."
echo "2. In your terminal, navigate to the project directory: cd $PROJECT_DIR"
echo "3. Activate the virtual environment: source venv/bin/activate"
echo "4. Run the application: python main.py"
echo ""
echo "Troubleshooting Kivy on Pi:"
echo " - If the app doesn't display correctly, you might need to set Kivy environment variables."
    echo "   Example for official 7\" DSI touchscreen: export KIVY_BCM_DISPMANX_ID=5"
    echo "   Example for HDMI: export KIVY_BCM_DISPMANX_ID=4 (usually default)"
echo " - Check Kivy logs in ~/.kivy/logs/ for errors."
echo "-----------------------------------------------------"

# Deactivate virtual environment (good practice within a script if activated here)
# However, for this script, we'll leave it to the user to manage activation for running the app.
# deactivate 