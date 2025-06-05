import platform
import os
import sys
import subprocess

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

if platform.system() == "Linux":
    print("\n=== DRM/KMS System Diagnostics ===")
    
    # Check DRM devices
    print("\nChecking DRM devices:")
    try:
        drm_devices = subprocess.check_output(['ls', '-l', '/dev/dri/']).decode()
        print(drm_devices)
    except Exception as e:
        print(f"Error checking DRM devices: {e}")

    # Check user groups
    print("\nChecking user groups:")
    try:
        groups = subprocess.check_output(['groups']).decode().strip()
        print(f"User groups: {groups}")
    except Exception as e:
        print(f"Error checking groups: {e}")

    # Check if KMS is enabled in kernel
    print("\nChecking KMS status:")
    try:
        kms_status = subprocess.check_output(['dmesg']).decode()
        print("Kernel messages related to DRM/KMS:")
        for line in kms_status.split('\n'):
            if 'drm' in line.lower() or 'kms' in line.lower():
                print(line)
    except Exception as e:
        print(f"Error checking KMS status: {e}")

    # Try each DRM card
    drm_cards = ['card0', 'card1', 'card2']
    for card in drm_cards:
        print(f"\n=== Testing DRM card: {card} ===")
        
        # Clear any existing SDL environment variables
        for key in list(os.environ.keys()):
            if key.startswith('SDL_'):
                del os.environ[key]

        # Set up environment for this card
        os.environ['SDL_VIDEODRIVER'] = 'kmsdrm'
        os.environ['SDL_VIDEODRIVER_DEVICE'] = f'/dev/dri/{card}'
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
            print(f"Minimal Test: DISPLAY environment variable was set to: {os.environ['DISPLAY']}. Unsetting it.")
            del os.environ['DISPLAY']
        else:
            print("Minimal Test: DISPLAY environment variable was not set.")

        print(f"Environment variables set for {card}:")
        print(f"SDL_VIDEODRIVER={os.environ.get('SDL_VIDEODRIVER')}")
        print(f"SDL_VIDEODRIVER_DEVICE={os.environ.get('SDL_VIDEODRIVER_DEVICE')}")
        print(f"KIVY_WINDOW={os.environ.get('KIVY_WINDOW')}")
        print(f"KIVY_TEXT={os.environ.get('KIVY_TEXT')}")
        print(f"DISPLAY={os.environ.get('DISPLAY')}")

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

                    return Label(text=f"Kivy GL Test\nWindow: {Window.__class__.__name__}\nGL Backend: {actual_gl_backend}\nDRM Card: {card}")

            print(f"Starting Kivy app with {card}...")
            MinimalTestApp().run()
            print(f"Kivy app finished with {card}.")

        except ImportError as e:
            print(f"Failed to import Kivy modules: {e}")
        except Exception as e:
            print(f"Error with {card}: {e}")
            continue

        print(f"\n=== Finished testing {card} ===\n")

except ImportError as e:
    print(f"Minimal Test: Failed to import Kivy modules: {e}")
    print("Minimal Test: Ensure Kivy is installed correctly in your virtual environment.")
except Exception as e:
    print(f"Minimal Test: An unexpected error occurred: {e}") 