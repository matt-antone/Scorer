#!/bin/bash
set -e

echo ">>> Starting Scorer installation..."

# Create a Python virtual environment
if [ ! -d ".venv" ]; then
    echo ">>> Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install Python dependencies from requirements.txt
echo ">>> Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# OS-specific installations for ffpyplayer
echo ">>> Installing ffpyplayer..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ">>> Running macOS specific setup for ffpyplayer..."
    
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install Homebrew to continue."
        exit 1
    fi

    echo ">>> Uninstalling potentially conflicting pip packages..."
    pip uninstall -y ffpyplayer || true
    
    echo ">>> Ensuring Homebrew dependencies are installed..."
    brew install ffmpeg@6
    brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf

    echo ">>> Building ffpyplayer from source..."
    # Set environment variables to link against Homebrew's ffmpeg@6
    export LDFLAGS="-L/opt/homebrew/opt/ffmpeg@6/lib"
    export CPPFLAGS="-I/opt/homebrew/opt/ffmpeg@6/include"
    USE_SYSTEM_LIBS=1 pip install --no-binary ffpyplayer ffpyplayer

    echo ">>> Cleaning up build-time Homebrew dependencies..."
    # The following lines are commented out to support the test environment,
    # which requires the SDL2 libraries to be present.
    # brew uninstall sdl2 sdl2_image sdl2_mixer sdl2_ttf
    # brew autoremove
else
    echo ">>> Installing ffpyplayer using pip..."
    pip install ffpyplayer==4.5.2
fi

# Initialize and migrate the database
echo ">>> Setting up the database..."
if [ ! -f "db/scorer.db" ]; then
    alembic -c db/alembic.ini upgrade head
fi

echo ">>> Installation complete." 