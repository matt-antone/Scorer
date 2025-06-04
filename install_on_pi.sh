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
     libmtdev-dev xclip xsel libjpeg-dev python3-pip python3-venv \
     libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev libavutil-dev libpostproc-dev libswresample-dev libswscale-dev
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

# 7. Create Launcher Script
echo "Creating launcher script (launch_scorer.sh)..."
cat << EOF > "$PROJECT_DIR/launch_scorer.sh"
#!/bin/bash
# Script to launch the Scorer Kivy application
cd "$PROJECT_DIR"
source "$VENV_DIR/bin/activate"
# Uncomment the following line if needed, or experiment with other Kivy environment variables
# export KIVY_WINDOW=egl_rpi
python main.py
EOF

chmod +x "$PROJECT_DIR/launch_scorer.sh"

# 8. Create assets directory for icon
echo "Creating assets directory for icon (if it doesn't exist)..."
mkdir -p "$PROJECT_DIR/assets"

# 9. Create Desktop Entry
echo "Creating desktop entry (Scorer.desktop)..."
cat << EOF > "$PROJECT_DIR/Scorer.desktop"
[Desktop Entry]
Version=1.0
Name=Scorer
Comment=Warhammer 40k Score Tracking App
Exec="$PROJECT_DIR/launch_scorer.sh"
Icon="$PROJECT_DIR/assets/icon_128.png"
Terminal=false
Type=Application
Categories=Game;Utility;
StartupNotify=true
Path="$PROJECT_DIR/"
EOF

chmod +x "$PROJECT_DIR/Scorer.desktop"

# Determine the actual user's home directory
if [ -n "$SUDO_USER" ]; then
    USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
else
    USER_HOME=$(getent passwd "$(whoami)" | cut -d: -f6)
fi

# Create directories for desktop entries if they don't exist and copy the .desktop file
if [ -d "$USER_HOME/Desktop" ]; then
    echo "Copying Scorer.desktop to $USER_HOME/Desktop/..."
    if [ -n "$SUDO_USER" ]; then
        sudo -u "$SUDO_USER" cp "$PROJECT_DIR/Scorer.desktop" "$USER_HOME/Desktop/"
        sudo -u "$SUDO_USER" chmod +x "$USER_HOME/Desktop/Scorer.desktop"
    else
        cp "$PROJECT_DIR/Scorer.desktop" "$USER_HOME/Desktop/"
        chmod +x "$USER_HOME/Desktop/Scorer.desktop"
    fi
elif [ -d "$USER_HOME/desktop" ]; then # Some systems use lowercase 'desktop'
    echo "Copying Scorer.desktop to $USER_HOME/desktop/..."
    if [ -n "$SUDO_USER" ]; then
        sudo -u "$SUDO_USER" cp "$PROJECT_DIR/Scorer.desktop" "$USER_HOME/desktop/"
        sudo -u "$SUDO_USER" chmod +x "$USER_HOME/desktop/Scorer.desktop"
    else
        cp "$PROJECT_DIR/Scorer.desktop" "$USER_HOME/desktop/"
        chmod +x "$USER_HOME/desktop/Scorer.desktop"
    fi
fi

APPLICATIONS_DIR="$USER_HOME/.local/share/applications"
echo "Creating $APPLICATIONS_DIR if it doesn't exist..."
if [ -n "$SUDO_USER" ]; then
    sudo -u "$SUDO_USER" mkdir -p "$APPLICATIONS_DIR"
    echo "Copying Scorer.desktop to $APPLICATIONS_DIR/..."
    sudo -u "$SUDO_USER" cp "$PROJECT_DIR/Scorer.desktop" "$APPLICATIONS_DIR/"
else
    mkdir -p "$APPLICATIONS_DIR"
    echo "Copying Scorer.desktop to $APPLICATIONS_DIR/..."
    cp "$PROJECT_DIR/Scorer.desktop" "$APPLICATIONS_DIR/"
fi

echo "-----------------------------------------------------"
echo "Installation and setup script finished."
echo ""
echo "IMPORTANT: This script must be run with sudo privileges (e.g., 'sudo bash install_on_pi.sh') to install system dependencies."
echo ""
echo "NEXT STEPS:"
echo "1. Ensure your desired icons (e.g., icon_128.png for the desktop, icon_64.png for in-app headers) are in the '$PROJECT_DIR/assets/' directory."
echo "   The desktop icon is set to use '$PROJECT_DIR/assets/icon_128.png'."
echo "2. You may need to reboot or log out/log in for the Scorer application icon to appear in your Desktop or application menu."
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