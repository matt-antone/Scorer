#!/bin/bash
set -e

# Always run from the directory where this script is located
cd "$(dirname "$0")"

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

# Set PYTHONPATH to include src directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

if [ "$1" = "test" ]; then
    echo ">>> Running unit tests..."
    cd ..  # Go to project root
    pi_client/.venv/bin/python3 tests/screens/test_suite.py
else
    # Run the application using the venv's python
    .venv/bin/python3 src/main.py 
fi 