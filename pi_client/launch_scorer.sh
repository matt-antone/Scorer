#!/bin/bash
set -e

# Always run from the project root
cd "$(dirname "$0")/.."

cd pi_client

echo ">>> Launching Scorer..."

# Check if virtual environment exists, if not create it
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install Kivy if not already installed
if ! pip show kivy &> /dev/null; then
    echo "Installing Kivy..."
    pip install kivy
fi

# Set PYTHONPATH to include the project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."

# Set Kivy environment variables
export KIVY_GL_BACKEND=sdl2
export KIVY_WINDOW=sdl2

if [ "$1" = "test" ]; then
    echo ">>> Running unit tests..."
    cd ../
    pi_client/.venv/bin/python3 tests/screens/test_suite.py
else
    # Change to project root and run the application as a module
    cd ..
    PYTHONPATH=$PYTHONPATH:. python3 -m pi_client.main
fi 