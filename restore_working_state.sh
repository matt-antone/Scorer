#!/bin/bash

echo "Starting restoration of working state..."

# Detect environment
if [ "$(uname -m)" = "aarch64" ]; then
    echo "Running on Raspberry Pi..."
    
    # Remove the dtoverlay=tc358762 entry from config.txt
    echo "Removing tc358762 overlay from config.txt..."
    sudo sed -i '/dtoverlay=tc358762/d' /boot/firmware/config.txt

    # Delete the modified launch_scorer.sh
    echo "Removing modified launch_scorer.sh..."
    rm -f launch_scorer.sh

    # Run the original installation script
    echo "Running original installation script..."
    bash install_on_pi.sh

    echo "Restoration complete. Please reboot your Raspberry Pi."
else
    echo "Running on local development environment..."
    
    # Delete the modified launch_scorer.sh
    echo "Removing modified launch_scorer.sh..."
    rm -f launch_scorer.sh

    # Restore files from last working commit
    echo "Restoring files from last working commit..."
    git checkout b86e7d4 -- main.py scorer.kv launch_scorer.sh

    echo "Restoration complete. You can now run the application locally."
fi 