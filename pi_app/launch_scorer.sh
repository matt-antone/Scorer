#!/bin/bash
set -e

echo ">>> Launching Scorer..."

# Activate the virtual environment
source .venv/bin/activate

# Run the application using the venv's python
.venv/bin/python3 main.py 