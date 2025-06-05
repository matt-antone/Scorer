import platform
import os
import sys
import subprocess
import json

def check_sdl2_config():
    print("\nChecking SDL2 configuration:")
    try:
        # Check SDL2 version and configuration
        sdl_version = subprocess.check_output(['pkg-config', '--modversion', 'sdl2']).decode().strip()
        print(f"SDL2 version: {sdl_version}")
        
        # Check SDL2 configuration
        sdl_config = subprocess.check_output(['sdl2-config', '--cflags', '--libs']).decode().strip()
        print(f"SDL2 configuration: {sdl_config}")
        
        # Check if KMSDRM is enabled in SDL2
        try:
            sdl_features = subprocess.check_output(['sdl2-config', '--features']).decode().strip()
            print(f"SDL2 features: {sdl_features}")
        except:
            print("Could not get SDL2 features")
            
    except Exception as e:
        print(f"Error checking SDL2 configuration: {e}")

def check_display_modes():
    print("\nChecking display modes:")
    try:
        # Check modes for DSI display
        print("\nDSI Display (drm-rp1-dsi) modes:")
        dsi_modes = subprocess.check_output(['modetest', '-M', 'drm-rp1-dsi']).decode()
        print(dsi_modes)
        
        # Check modes for VC4 driver
        print("\nVC4 Display modes:")
        vc4_modes = subprocess.check_output(['modetest', '-M', 'vc4-drm']).decode()
        print(vc4_modes)
        
    except Exception as e:
        print(f"Error checking display modes: {e}")

def check_boot_config():
    print("\nChecking /boot/config.txt:")
    try:
        with open('/boot/config.txt', 'r') as f:
            config = f.read()
            print("Current /boot/config.txt contents:")
            print(config)
            
            # Check for relevant overlays
            if 'dtoverlay=vc4-kms-v3d' in config:
                print("Found vc4-kms-v3d overlay")
            if 'dtoverlay=rp1-dsi' in config:
                print("Found rp1-dsi overlay")
                
    except Exception as e:
        print(f"Error checking /boot/config.txt: {e}")

def check_drm_devices():
    print("\nChecking DRM devices:")
    try:
        drm_devices = subprocess.check_output(['ls', '-l', '/dev/dri/']).decode()
        print(drm_devices)
    except Exception as e:
        print(f"Error checking DRM devices: {e}")

def check_user_groups():
    print("\nChecking user groups:")
    try:
        groups = subprocess.check_output(['groups']).decode().strip()
        print(f"User groups: {groups}")
    except Exception as e:
        print(f"Error checking groups: {e}")

def check_kms_status():
    print("\nChecking KMS status:")
    try:
        kms_status = subprocess.check_output(['dmesg']).decode()
        print("Kernel messages related to DRM/KMS:")
        for line in kms_status.split('\n'):
            if 'drm' in line.lower() or 'kms' in line.lower():
                print(line)
    except Exception as e:
        print(f"Error checking KMS status: {e}")

def setup_environment():
    # Clear any existing SDL environment variables
    for key in list(os.environ.keys()):
        if key.startswith('SDL_'):
            del os.environ[key]

    # Set up environment
    os.environ['SDL_VIDEODRIVER'] = 'kmsdrm'
    os.environ['SDL_VIDEODRIVER_DEVICE'] = '/dev/dri/card1'  # DSI display
    os.environ['KIVY_WINDOW'] = 'sdl2'
    os.environ['KIVY_TEXT'] = 'sdl2'
    os.environ['KIVY_LOG_LEVEL'] = 'debug'
    
    # Additional SDL environment variables for KMSDRM
    os.environ['SDL_VIDEO_KMSDRM_DEVICE'] = '/dev/dri/card1'
    os.environ['SDL_VIDEO_KMSDRM_CRTC'] = '0'
    os.environ['SDL_VIDEO_KMSDRM_CONNECTOR'] = '0'
    os.environ['SDL_VIDEO_KMSDRM_MODE'] = '0'
    
    # Force specific display mode based on DSI configuration
    os.environ['SDL_VIDEO_KMSDRM_FORCE_MODE'] = '1'
    os.environ['SDL_VIDEO_KMSDRM_FORCE_WIDTH'] = '800'
    os.environ['SDL_VIDEO_KMSDRM_FORCE_HEIGHT'] = '480'
    os.environ['SDL_VIDEO_KMSDRM_FORCE_REFRESH'] = '60'
    
    # DSI specific configuration
    os.environ['SDL_VIDEO_KMSDRM_FORCE_DPI'] = '30000'  # DPI clock from kernel
    os.environ['SDL_VIDEO_KMSDRM_FORCE_BYTE_CLOCK'] = '90000000'  # Byte clock from kernel
    os.environ['SDL_VIDEO_KMSDRM_FORCE_DSI_CHANNEL'] = '0'  # DSI channel from kernel
    os.environ['SDL_VIDEO_KMSDRM_FORCE_DSI_LANES'] = '1'  # DSI lanes from kernel
    os.environ['SDL_VIDEO_KMSDRM_FORCE_DSI_FORMAT'] = '0'  # DSI format from kernel
    
    # Debug logging
    os.environ['SDL_LOG_PRIORITY'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_APPLICATION'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_ERROR'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_SYSTEM'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_AUDIO'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_VIDEO'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_RENDER'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_INPUT'] = 'VERBOSE'
    
    if 'DISPLAY' in os.environ:
        print(f"DISPLAY environment variable was set to: {os.environ['DISPLAY']}. Unsetting it.")
        del os.environ['DISPLAY']
    else:
        print("DISPLAY environment variable was not set.")

    print("Environment variables set:")
    print(f"SDL_VIDEODRIVER={os.environ.get('SDL_VIDEODRIVER')}")
    print(f"SDL_VIDEODRIVER_DEVICE={os.environ.get('SDL_VIDEODRIVER_DEVICE')}")
    print(f"SDL_VIDEO_KMSDRM_DEVICE={os.environ.get('SDL_VIDEO_KMSDRM_DEVICE')}")
    print(f"SDL_VIDEO_KMSDRM_CRTC={os.environ.get('SDL_VIDEO_KMSDRM_CRTC')}")
    print(f"SDL_VIDEO_KMSDRM_CONNECTOR={os.environ.get('SDL_VIDEO_KMSDRM_CONNECTOR')}")
    print(f"SDL_VIDEO_KMSDRM_MODE={os.environ.get('SDL_VIDEO_KMSDRM_MODE')}")
    print(f"SDL_VIDEO_KMSDRM_FORCE_MODE={os.environ.get('SDL_VIDEO_KMSDRM_FORCE_MODE')}")
    print(f"SDL_VIDEO_KMSDRM_FORCE_WIDTH={os.environ.get('SDL_VIDEO_KMSDRM_FORCE_WIDTH')}")
    print(f"SDL_VIDEO_KMSDRM_FORCE_HEIGHT={os.environ.get('SDL_VIDEO_KMSDRM_FORCE_HEIGHT')}")
    print(f"SDL_VIDEO_KMSDRM_FORCE_REFRESH={os.environ.get('SDL_VIDEO_KMSDRM_FORCE_REFRESH')}")
    print(f"SDL_VIDEO_KMSDRM_FORCE_DPI={os.environ.get('SDL_VIDEO_KMSDRM_FORCE_DPI')}")
    print(f"SDL_VIDEO_KMSDRM_FORCE_BYTE_CLOCK={os.environ.get('SDL_VIDEO_KMSDRM_FORCE_BYTE_CLOCK')}")
    print(f"SDL_VIDEO_KMSDRM_FORCE_DSI_CHANNEL={os.environ.get('SDL_VIDEO_KMSDRM_FORCE_DSI_CHANNEL')}")
    print(f"SDL_VIDEO_KMSDRM_FORCE_DSI_LANES={os.environ.get('SDL_VIDEO_KMSDRM_FORCE_DSI_LANES')}")
    print(f"SDL_VIDEO_KMSDRM_FORCE_DSI_FORMAT={os.environ.get('SDL_VIDEO_KMSDRM_FORCE_DSI_FORMAT')}")
    print(f"KIVY_WINDOW={os.environ.get('KIVY_WINDOW')}")
    print(f"KIVY_TEXT={os.environ.get('KIVY_TEXT')}")
    print(f"DISPLAY={os.environ.get('DISPLAY')}")

def main():
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")

    if platform.system() != "Linux":
        print("This script is designed for Linux systems.")
        return

    print("\n=== System Diagnostics ===")
    check_sdl2_config()
    check_display_modes()
    check_boot_config()
    check_drm_devices()
    check_user_groups()
    check_kms_status()

    print("\n=== Testing DRM card: card1 ===")
    setup_environment()

    try:
        from kivy.config import Config
        Config.set('kivy', 'log_level', 'debug')
        print(f"Kivy config set -> kivy:log_level={Config.get('kivy', 'log_level')}")

        from kivy.app import App
        from kivy.uix.label import Label
        from kivy.core.window import Window

        print("Kivy imported successfully.")

        class MinimalTestApp(App):
            def build(self):
                print(f"Window provider: {Window.__class__.__name__}")
                print(f"Window size: {Window.size}")
                actual_gl_backend = "Unknown"
                try:
                    if hasattr(Window, 'backend_name'):
                         actual_gl_backend = Window.backend_name
                    elif hasattr(Window, '_gl_backend_name'):
                         actual_gl_backend = Window._gl_backend_name
                except Exception as e:
                    print(f"Error getting GL backend name: {e}")

                return Label(text=f"Kivy GL Test\nWindow: {Window.__class__.__name__}\nGL Backend: {actual_gl_backend}\nDRM Card: card1")

        print("Starting Kivy app...")
        MinimalTestApp().run()
        print("Kivy app finished.")

    except ImportError as e:
        print(f"Failed to import Kivy modules: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main() 