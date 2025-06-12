#!/bin/bash

# Set required environment variables for Kivy on Raspberry Pi
export KIVY_BCM_DISPMANX_ID=5
export SDL_VIDEODRIVER=kmsdrm
export SDL_VIDEODRIVER_DEVICE=/dev/dri/card1
export SDL_VIDEO_KMSDRM_DEVICE=/dev/dri/card1
export SDL_VIDEO_KMSDRM_CRTC=34
export SDL_VIDEO_KMSDRM_CONNECTOR=36
export SDL_LOG_PRIORITY=VERBOSE
export SDL_LOG_CATEGORY_VIDEO=VERBOSE

# Set Kivy to use framebuffer
export KIVY_WINDOW=sdl2
export KIVY_GL_BACKEND=sdl2
export KIVY_GRAPHICS=gl

# Activate virtual environment
source /home/matthewantone/Scorer/pi_app/.venv/bin/activate

# Run the tests
python -m pi_app.tests.graphical.run_tests 