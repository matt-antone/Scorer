#!/bin/bash

# Script to launch the Scorer Kivy application

# Navigate to the application directory
cd /home/matthewantone/Scorer/

# Activate the Python virtual environment
source venv/bin/activate

# Set Kivy environment variable (optional, remove if not needed when launching from desktop)
export KIVY_WINDOW=egl_rpi

# Run the Kivy application
python main.py 