#!/bin/bash

# Activate virtual environment
source /home/matthewantone/Scorer/pi_client/.venv/bin/activate

# Set environment variables for Kivy on Raspberry Pi
export KIVY_BCM_DISPMANX_ID=5
export SDL_VIDEODRIVER=x11
export DISPLAY=:0
export XAUTHORITY=/home/matthewantone/.Xauthority

# Add pi_client to Python path
export PYTHONPATH=/home/matthewantone/Scorer:$PYTHONPATH

# Run tests
python3 -m pi_client.tests.graphical.run_tests 