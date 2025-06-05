# SDL2/KMSDRM Setup for Raspberry Pi 5

> **⚠️ WORK IN PROGRESS - NOT YET VERIFIED ⚠️**
>
> This document is currently recording our attempt to solve the SDL2/KMSDRM integration issue. The solution described below is being tested and has not yet been confirmed to work. We will update this document once we verify the solution works.

## The Problem

When running Kivy applications on a Raspberry Pi 5 with a touchscreen, you might encounter issues with the display not working properly. This is often because:

1. Kivy's SDL2 window provider is linking against the system SDL2 libraries
2. The system SDL2 libraries don't have KMSDRM support enabled
3. This causes Kivy to try to use X11 or Wayland, which aren't available or desired

## The Solution

The solution involves:

1. Compiling SDL2 from source with KMSDRM support
2. Ensuring Kivy links against this custom SDL2
3. Configuring the system to prioritize our custom SDL2

## Step-by-Step Process

### 1. Prepare the System

```bash
# Update package lists
sudo apt update

# Install build dependencies
sudo apt install -y build-essential git cmake ninja-build pkg-config \
    libasound2-dev libpulse-dev libaudio-dev libjack-dev libsndio-dev \
    libsamplerate0-dev libx11-dev libxext-dev libxrandr-dev libxcursor-dev \
    libxfixes-dev libxi-dev libxss-dev libwayland-dev libxkbcommon-dev \
    libdrm-dev libgbm-dev libgl1-mesa-dev libgles2-mesa-dev libegl1-mesa-dev \
    libdbus-1-dev libibus-1.0-dev libudev-dev fcitx-libs-dev \
    libfreetype6-dev liblzma-dev libjpeg-dev libtiff-dev libwebp-dev \
    libraspberrypi-dev raspberrypi-kernel-headers xorg-dev

# Remove system SDL2 dev packages
sudo apt remove libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
sudo apt autoremove
```

### 2. Build SDL2 from Source

```bash
# Create build directory
mkdir ~/sdl2_build && cd ~/sdl2_build

# Download and extract SDL2
wget https://github.com/libsdl-org/SDL/releases/download/release-2.30.3/SDL2-2.30.3.tar.gz
tar -zxvf SDL2-2.30.3.tar.gz
cd SDL2-2.30.3

# Configure with KMSDRM support
./configure --enable-video-kmsdrm --disable-video-x11 --disable-video-wayland --disable-video-rpi --disable-video-opengl
make -j$(nproc)
sudo make install
cd ..
```

### 3. Build SDL2 Satellite Libraries

```bash
# SDL2_image
wget https://github.com/libsdl-org/SDL_image/releases/download/release-2.8.2/SDL2_image-2.8.2.tar.gz
tar -zxvf SDL2_image-2.8.2.tar.gz
cd SDL2_image-2.8.2
./configure
make -j$(nproc)
sudo make install
cd ..

# SDL2_mixer
wget https://github.com/libsdl-org/SDL_mixer/releases/download/release-2.8.0/SDL2_mixer-2.8.0.tar.gz
tar -zxvf SDL2_mixer-2.8.0.tar.gz
cd SDL2_mixer-2.8.0
./configure
make -j$(nproc)
sudo make install
cd ..

# SDL2_ttf
wget https://github.com/libsdl-org/SDL_ttf/releases/download/release-2.22.0/SDL2_ttf-2.22.0.tar.gz
tar -zxvf SDL2_ttf-2.22.0.tar.gz
cd SDL2_ttf-2.22.0
./configure
make -j$(nproc)
sudo make install
cd ..
```

### 4. Configure System Library Paths

```bash
# Update library cache
sudo ldconfig

# Create custom library configuration
echo "/usr/local/lib" | sudo tee /etc/ld.so.conf.d/local.conf
sudo ldconfig
```

### 5. Reinstall Kivy

```bash
# Activate virtual environment
cd ~/Scorer
source .venv/bin/activate

# Uninstall existing Kivy and Pillow
pip uninstall -y kivy Pillow

# Reinstall with custom library paths
LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH LD_RUN_PATH=/usr/local/lib .venv/bin/python -m pip install --no-cache-dir --no-binary :all: kivy Pillow
```

## Common Issues and Solutions

### 1. Kivy Still Links Against System SDL2

If `ldd` shows Kivy is still using system SDL2:

```bash
ldd .venv/lib/python3.11/site-packages/kivy/core/window/_window_sdl2.cpython-311-aarch64-linux-gnu.so | grep SDL2
```

Solutions:

- Ensure `/usr/local/lib` is in `/etc/ld.so.conf.d/local.conf`
- Run `sudo ldconfig`
- Reinstall Kivy with explicit library paths

### 2. KMSDRM Not Available

If you get "kmsdrm not available" error:

- Check if `vc4-kms-v3d` is loaded: `lsmod | grep vc4`
- Ensure user is in `video` and `render` groups
- Verify SDL2 was built with KMSDRM support: check `config.log`

### 3. Compilation Takes Too Long

The compilation process is time-consuming on Raspberry Pi. There's no quick way around this as:

- Kivy's SDL2 window module must be recompiled to link against custom SDL2
- Cross-compilation is complex and might introduce other issues
- Pre-built wheels won't link against our custom SDL2

## Verification

To verify the setup:

1. Check library linkage:

```bash
ldd .venv/lib/python3.11/site-packages/kivy/core/window/_window_sdl2.cpython-311-aarch64-linux-gnu.so | grep SDL2
```

2. Run a test application with SDL_VIDEODRIVER set:

```bash
SDL_VIDEODRIVER=kmsdrm python3 your_app.py
```

## Important Notes

1. This process must be repeated if:

   - System SDL2 packages are updated
   - Kivy is reinstalled
   - System libraries are updated

2. Keep track of:

   - Which SDL2 version you compiled
   - Which Kivy version you're using
   - Any custom configuration changes

3. Document any additional steps needed for your specific setup

## References

- [SDL2 Documentation](https://wiki.libsdl.org/)
- [Kivy Documentation](https://kivy.org/doc/stable/)
- [Raspberry Pi KMS/DRM Documentation](https://www.raspberrypi.com/documentation/computers/config_txt.html#dtoverlay)
