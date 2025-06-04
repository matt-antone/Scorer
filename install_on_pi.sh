#!/bin/bash

echo "Starting Scorer App installation on Raspberry Pi..."

# Exit immediately if a command exits with a non-zero status.
set -e

# 1. Update package lists
echo "Updating package lists..."
sudo apt-get update

# 2. Install Kivy system dependencies and python3-venv
echo "Installing Kivy system dependencies and python3-venv..."
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
     pkg-config libgl1-mesa-dev libgles2-mesa-dev python3-setuptools libgstreamer1.0-dev \
     git-core gstreamer1.0-plugins-{bad,base,good,ugly} gstreamer1.0-omx \
     libmtdev-dev xclip xsel libjpeg-dev python3-pip python3-venv
# The python3-venv package is crucial here.

# 3. Create a Python virtual environment
# No need to install virtualenv using pip if python3-venv is installed via apt.
PROJECT_DIR=$(pwd) # Assumes the script is run from the project root
VENV_DIR="$PROJECT_DIR/venv"

echo "Creating Python virtual environment at $VENV_DIR using python3 -m venv..."
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment '$VENV_DIR' already exists. Removing and recreating to ensure freshness."
    # sudo rm -rf "$VENV_DIR" # Requires sudo if script is not run as sudo and venv was created by sudo previously
    # The user will need to handle removal if needed and permissions allow, or run script with sudo.
    echo "[USER ACTION REQUIRED IF RECREATION FAILS] Manually remove $VENV_DIR if needed."
    # For now, let's assume user handles removal or it's a fresh setup.
    # If running the whole script with sudo, recreation is fine.
    # If not, this might fail if venv was created by sudo previously.
    # A safer bet for non-sudo script execution is to just skip if exists.
    # However, the error output suggests the script was run with sudo, so rm -rf should be fine if script is run with sudo.
    rm -rf "$VENV_DIR" # Simpler: just remove if script has permissions (e.g. run with sudo)
fi
python3 -m venv "$VENV_DIR" # Use python3 -m venv


# 4. Activate the virtual environment (for the context of this script)
# The user will need to activate it manually in their terminal later.
source "$VENV_DIR/bin/activate"
echo "Activated virtual environment for this script execution."

# 5. Upgrade pip within the virtual environment
echo "Upgrading pip within the virtual environment..."
pip install --upgrade pip setuptools

# 6. Install Python packages from requirements.txt into the virtual environment
echo "Installing Python packages from requirements.txt..."
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements.txt"
else
    echo "Error: requirements.txt not found in $PROJECT_DIR. Cannot install Python packages."
    deactivate # Deactivate venv if requirements are missing
    exit 1
fi

echo "-----------------------------------------------------"
echo "Installation and setup script finished."
echo ""
echo "IMPORTANT: This script must be run with sudo privileges (e.g., 'sudo bash install_on_pi.sh') to install system dependencies."
echo ""
echo "NEXT STEPS:"
echo "1. After the script completes, in your terminal, navigate to the project directory: cd $PROJECT_DIR"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the application: python main.py"
echo ""
echo "Troubleshooting Kivy on Pi:"
echo " - If the app doesn't display correctly, you might need to set Kivy environment variables."
    echo "   Example for official 7\" DSI touchscreen: export KIVY_BCM_DISPMANX_ID=5"
    echo "   Example for HDMI: export KIVY_BCM_DISPMANX_ID=4 (usually default)"
echo " - Check Kivy logs in ~/.kivy/logs/ for errors."
echo "-----------------------------------------------------"

# Deactivate virtual environment explicitly if script was run with sudo and sourced venv
# to avoid leaving a root-owned activated venv state in a non-root shell if not careful.
# However, the script is designed to be run by the user, who will then activate manually.
# If the script is run with `sudo bash install_on_pi.sh`, the `source` command affects the script's subshell,
# not the user's calling shell. So explicit deactivation here is mostly for script hygiene.
echo "Script finished. Remember to activate the venv in your terminal: source $VENV_DIR/bin/activate" 