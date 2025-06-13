#!/bin/bash
set -e

# Always run from the directory where this script is located
cd "$(dirname "$0")/.."

echo ">>> Running Scorer tests..."

# Activate the virtual environment
source .venv/bin/activate

# Install the package in development mode
echo "Installing pi_client package..."
pip install -e .

# Set PYTHONPATH to include the project root
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Run the tests
python -m pytest tests/ -v 