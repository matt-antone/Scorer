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

# Run the tests
python3 -m pi_app.tests.graphical.run_tests 