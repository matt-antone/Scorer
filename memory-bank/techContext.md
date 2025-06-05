# Tech Context: Scorer

This document lists the technologies, development setup, technical constraints, and dependencies for the Scorer project.

## 1. Core Technologies & Stack

- **Programming Language**: Python 3.11+
- **GUI Framework**: Kivy 2.2.1+
- **Web Framework**: Flask 3.0.0+
- **Data Persistence**: Local JSON file (`game_state.json`)
- **WebSocket Server**: `python-socketio` and `flask-socketio` for real-time communication.
- **QR Code Generation**: `qrcode` library with `Pillow`.
- **Custom Fonts**: Kivy's `LabelBase` for registering and using custom fonts like "InterBlack".

## 2. Platform & Hardware

### 2.1. Target Deployment Platform

- **Hardware**: Raspberry Pi 5 (8GB RAM, 32GB microSD)
- **Operating System**: Raspberry Pi OS (64-bit)
- **Display**: 5-inch DSI touchscreen (800x480@60Hz, using `tc358762` DSI device on socket 1)
- **Network**: Accessible on the local network (e.g., `madlab5.local`).

### 2.2. Development Platform

- **Operating System**: macOS
- **Key Difference**: Uses the default SDL2 window provider instead of the custom-built KMSDRM version for the Raspberry Pi.

## 3. Environment & Dependencies

### 3.1. Python Environment

- A `venv` virtual environment is used for both development and deployment.
- Dependencies are managed in `requirements.txt`.
- **Python Dependencies**:
  - `Kivy==2.2.1`
  - `Flask==3.0.0`
  - `python-socketio`
  - `flask-socketio`
  - `qrcode`
  - `Pillow`
  - `python-dotenv==1.0.0`
  - `requests==2.31.0`

### 3.2. System Dependencies (Raspberry Pi Only)

- **SDL2**: Must be built from source to include KMSDRM support, which is critical for hardware acceleration on the Pi's DSI display. The default `apt` version is insufficient.
- **Build Tools**: `build-essential`, `git`, `autoconf`, `automake`, `libtool`, `pkg-config`.
- **SDL2 Dependencies**: A full list of `lib-dev` packages required to build SDL2, including those for audio, video (X11, Wayland, DRM), and input.

## 4. Raspberry Pi Configuration

### 4.1. Boot Configuration (`/boot/firmware/config.txt`)

- `dtoverlay=vc4-kms-v3d`: Enables the KMS graphics driver.
- `max_framebuffers=2`: Required for KMS.
- `disable_fw_kms_setup=1`: Prevents firmware from interfering with KMS.
- `dtoverlay=tc358762,...`: Specific overlay for the DSI display.

### 4.2. Runtime Environment Variables

These variables are critical for launching the Kivy app correctly on the Pi.

- `SDL_VIDEODRIVER=kmsdrm`: Forces SDL2 to use the KMSDRM backend.
- `SDL_VIDEODRIVER_DEVICE=/dev/dri/card1`: Points to the DSI display's DRM device.
- `KIVY_BCM_DISPMANX_ID=5`: Selects the correct display socket for the 5-inch screen.
- `SDL_LOG_PRIORITY=VERBOSE`: (For debugging) Enables verbose logging from SDL2.

### 4.3. User Permissions

- The user running the application must be a member of the `video` and `render` groups to access the DRM hardware.

## 5. Development Tools & Workflow

- **Version Control**: Git & GitHub.
- **Code Formatting**: Black.
- **Linting**: Flake8.
- **Installation Scripts**:
  - `install.sh`: Full installation script for the Pi, including the complete SDL2 build process.
  - `install_on_pi.sh`: A quicker script for development, does not build SDL2.
- **Launcher Script**: `launch_scorer.sh` is a platform-aware script that sets the correct environment variables before running the application on either macOS or the Pi.

## Development Environment

- Target Platform: Raspberry Pi 5 with 5-inch touchscreen
- Development OS: macOS
- Python Version: 3.11.2
- Kivy Version: 2.3.1

## Critical Dependencies

### SDL2 Requirements

- SDL2 must be built from source with KMSDRM support for Raspberry Pi 5
- The default SDL2 package from apt does not include KMSDRM support
- Required build dependencies:
  ```bash
  sudo apt-get update
  sudo apt-get install -y build-essential git autoconf automake libtool pkg-config \
    libasound2-dev libpulse-dev libaudio-dev libx11-dev libxext-dev \
    libxrandr-dev libxcursor-dev libxi-dev libxinerama-dev libxxf86vm-dev \
    libxss-dev libgl1-mesa-dev libdbus-1-dev libudev-dev \
    libgles2-mesa-dev libegl1-mesa-dev libibus-1.0-dev \
    libdrm-dev libgbm-dev libinput-dev libudev-dev libxkbcommon-dev
  ```
- Build SDL2 with KMSDRM support:
  ```bash
  git clone https://github.com/libsdl-org/SDL.git
  cd SDL
  ./configure --enable-video-kmsdrm \
    --enable-video-opengl \
    --enable-video-opengles \
    --enable-video-opengles2 \
    --enable-video-egl \
    --enable-video-gbm \
    --enable-video-dummy \
    --enable-video-x11 \
    --enable-video-wayland \
    --enable-video-rpi \
    --enable-video-vivante \
    --enable-video-cocoa \
    --enable-video-metal \
    --enable-video-vulkan \
    --enable-video-offscreen
  make -j4
  sudo make install
  sudo ldconfig
  ```

## Display Configuration

- DSI Display: 800x480@60Hz
- DSI Device: tc358762
- DSI Configuration:
  - Channel: 0
  - Lanes: 1
  - Format: 0
  - DPI Clock: 30000000
  - Byte Clock: 90000000

## DRM/KMS Setup

- Required overlays in `/boot/firmware/config.txt`:
  ```
  dtoverlay=vc4-kms-v3d
  max_framebuffers=2
  disable_fw_kms_setup=1
  ```
- User must be in `video` and `render` groups
- DRM devices:
  - card0: V3D driver
  - card1: DSI display (drm-rp1-dsi)
  - card2: VC4 driver

## Known Issues

1. SDL2 KMSDRM Support:

   - Default SDL2 package lacks KMSDRM support
   - Must be built from source with KMSDRM enabled
   - Affects Kivy window provider initialization
   - Error: "kmsdrm not available"

2. Display Configuration:
   - VC4 driver reports "Cannot find any crtc or sizes"
   - DSI display properly initialized but requires specific configuration
   - Need to use correct CRTC (34) and connector (36) IDs

## Environment Variables

Critical SDL2/KMSDRM environment variables:

```bash
SDL_VIDEODRIVER=kmsdrm
SDL_VIDEODRIVER_DEVICE=/dev/dri/card1
SDL_VIDEO_KMSDRM_DEVICE=/dev/dri/card1
SDL_VIDEO_KMSDRM_CRTC=34
SDL_VIDEO_KMSDRM_CONNECTOR=36
SDL_VIDEO_KMSDRM_MODE=0
SDL_VIDEO_KMSDRM_FORCE_MODE=1
SDL_VIDEO_KMSDRM_FORCE_WIDTH=800
SDL_VIDEO_KMSDRM_FORCE_HEIGHT=480
SDL_VIDEO_KMSDRM_FORCE_REFRESH=60
SDL_VIDEO_KMSDRM_FORCE_DPI=30000
SDL_VIDEO_KMSDRM_FORCE_BYTE_CLOCK=90000000
SDL_VIDEO_KMSDRM_FORCE_DSI_CHANNEL=0
SDL_VIDEO_KMSDRM_FORCE_DSI_LANES=1
SDL_VIDEO_KMSDRM_FORCE_DSI_FORMAT=0
```

## Debugging Tools

- `modetest`: For checking display modes and DRM configuration
- `dmesg`: For kernel messages related to DRM/KMS
- SDL2 verbose logging:
  ```bash
  SDL_LOG_PRIORITY=VERBOSE
  SDL_LOG_CATEGORY_APPLICATION=VERBOSE
  SDL_LOG_CATEGORY_ERROR=VERBOSE
  SDL_LOG_CATEGORY_SYSTEM=VERBOSE
  SDL_LOG_CATEGORY_AUDIO=VERBOSE
  SDL_LOG_CATEGORY_VIDEO=VERBOSE
  SDL_LOG_CATEGORY_RENDER=VERBOSE
  SDL_LOG_CATEGORY_INPUT=VERBOSE
  ```

## Hardware Configuration

### Raspberry Pi 5

- Model: Raspberry Pi 5
- OS: Raspberry Pi OS (64-bit)
- RAM: 8GB
- Storage: 32GB microSD

### Display Configuration

- Display: 5-inch DSI touchscreen
- Resolution: 800x480@60Hz
- Interface: Camera/Display Socket 1 (not HDMI)
- DSI Device: tc358762
- DSI Configuration:
  - Channel: 0
  - Lanes: 1
  - Format: 0
  - DPI Clock: 30000000
  - Byte Clock: 90000000

### Required Overlays

- `dtoverlay=vc4-kms-v3d` - Enables KMS support
- `dtoverlay=tc358762,dsi0=1,dsi1=0,channel=0,lanes=1,format=0,dpi_clock=30000000,byte_clock=90000000` - Configures DSI display
- `max_framebuffers=2` - Required for KMS
- `disable_fw_kms_setup=1` - Prevents firmware from interfering with KMS

## Development Environment

### macOS Development Setup

- Python 3.11.7
- Kivy 2.2.1
- SDL2 (default macOS configuration)
- Environment Variables:
  - `KIVY_WINDOW=sdl2` - Uses default SDL2 window provider

### Raspberry Pi Production Setup

- Python 3.11.7
- Kivy 2.2.1
- SDL2 (built from source with KMSDRM support)
- Environment Variables:
  - `KIVY_BCM_DISPMANX_ID=5` - Required for camera/display socket 1
  - `SDL_VIDEODRIVER=kmsdrm` - Uses KMSDRM video driver
  - `SDL_VIDEODRIVER_DEVICE=/dev/dri/card1` - DRM device path
  - `SDL_VIDEO_KMSDRM_DEVICE=/dev/dri/card1` - KMSDRM device path
  - `SDL_VIDEO_KMSDRM_CRTC=34` - CRTC ID for display
  - `SDL_VIDEO_KMSDRM_CONNECTOR=36` - Connector ID for display
  - `SDL_LOG_PRIORITY=VERBOSE` - Enables verbose logging
  - `SDL_LOG_CATEGORY_VIDEO=VERBOSE` - Enables video subsystem logging

## Dependencies

### Python Dependencies

- Kivy==2.2.1
- Flask==3.0.0
- requests==2.31.0
- python-dotenv==1.0.0

### System Dependencies (Raspberry Pi)

- SDL2 (built from source with KMSDRM support)
- Required SDL2 build dependencies:
  ```bash
  sudo apt install -y build-essential git autoconf automake libtool pkg-config \
    libasound2-dev libpulse-dev libaudio-dev libx11-dev libxext-dev \
    libxrandr-dev libxcursor-dev libxi-dev libxinerama-dev libxxf86vm-dev \
    libxss-dev libgl1-mesa-dev libdbus-1-dev libudev-dev \
    libgles2-mesa-dev libegl1-mesa-dev libibus-1.0-dev \
    libdrm-dev libgbm-dev libinput-dev libudev-dev libxkbcommon-dev
  ```

## Development Tools

### Version Control

- Git for version control
- GitHub for remote repository

### Testing

- Kivy's built-in testing framework
- Manual testing on both macOS and Raspberry Pi

### Deployment

- `install.sh` - Full installation script including SDL2 build
- `install_on_pi.sh` - Quick installation script (no SDL2 build)
- `launch_scorer.sh` - Platform-aware launcher script

## Technical Constraints

### Display Configuration

- Must use KMSDRM for hardware acceleration
- Must configure DSI display through camera/display socket 1
- Must set correct KIVY_BCM_DISPMANX_ID for display socket

### Performance Requirements

- Target 60 FPS for smooth UI
- Hardware acceleration required for video processing
- Low latency for touch input

### Security

- No sensitive data storage
- Local network only
- No external API dependencies

## Known Issues

### SDL2/KMSDRM

- KMSDRM support requires SDL2 built from source
- Must use correct DRM device paths and IDs
- Must have proper user permissions (video and render groups)

### Display Configuration

- DSI display must be properly configured in /boot/firmware/config.txt
- Must use correct DSI parameters for tc358762 device
- Must have proper KMS support enabled

## Development Workflow

### Local Development (macOS)

1. Use default SDL2 settings
2. Test UI layout and functionality
3. Verify touch input behavior

### Raspberry Pi Testing

1. Build SDL2 from source with KMSDRM support
2. Configure DSI display in /boot/firmware/config.txt
3. Set correct environment variables
4. Test hardware acceleration and performance

## Deployment Process

### Raspberry Pi Setup

1. Run `install.sh` for full installation
2. Verify SDL2 build with KMSDRM support
3. Configure display in /boot/firmware/config.txt
4. Set up autostart with correct environment variables

### Verification Steps

1. Check SDL2 KMSDRM support
2. Verify display configuration
3. Test touch input
4. Monitor performance metrics

## Development Setup

### Prerequisites

1. Python 3.11 or higher
2. PostgreSQL 14 or higher
   - Installation (macOS):
     ```bash
     brew install postgresql@14
     brew services start postgresql@14
     createdb scorer
     ```
   - Installation (Raspberry Pi):
     ```bash
     sudo apt update
     sudo apt install postgresql postgresql-contrib
     sudo systemctl start postgresql
     sudo -u postgres createdb scorer
     ```
   - Verify installation:
     ```bash
     psql -U postgres -d scorer
     ```

### Environment Setup
