import platform
import os
import sys
import subprocess

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

    print("\n=== DRM/KMS System Diagnostics ===")
    check_drm_devices()
    check_user_groups()
    check_kms_status()

    print("\n=== Testing DRM card: card1 ===")  # Updated message
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

                return Label(text=f"Kivy GL Test\nWindow: {Window.__class__.__name__}\nGL Backend: {actual_gl_backend}\nDRM Card: card1")  # Updated card name

        print("Starting Kivy app...")
        MinimalTestApp().run()
        print("Kivy app finished.")

    except ImportError as e:
        print(f"Failed to import Kivy modules: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main() 