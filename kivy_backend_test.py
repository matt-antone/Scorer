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
    os.environ['SDL_VIDEODRIVER_DEVICE'] = '/dev/dri/card2'
    os.environ['KIVY_WINDOW'] = 'sdl2'
    os.environ['KIVY_TEXT'] = 'sdl2'
    os.environ['KIVY_LOG_LEVEL'] = 'debug'
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

    print("\n=== Testing DRM card: card2 ===")
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

                return Label(text=f"Kivy GL Test\nWindow: {Window.__class__.__name__}\nGL Backend: {actual_gl_backend}\nDRM Card: card2")

        print("Starting Kivy app...")
        MinimalTestApp().run()
        print("Kivy app finished.")

    except ImportError as e:
        print(f"Failed to import Kivy modules: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main() 