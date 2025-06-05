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
        kms_status = subprocess.check_output(['dmesg', '|', 'grep', 'drm']).decode()
        print(kms_status)
    except Exception as e:
        print(f"Error checking KMS status: {e}")

    print("\n=== Setting up Kivy Environment ===")
    os.environ['SDL_LOG_PRIORITY'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_APPLICATION'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_ERROR'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_SYSTEM'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_AUDIO'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_VIDEO'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_RENDER'] = 'VERBOSE'
    os.environ['SDL_LOG_CATEGORY_INPUT'] = 'VERBOSE'
    
    os.environ['SDL_VIDEODRIVER'] = 'kmsdrm'
    os.environ['KIVY_WINDOW'] = 'sdl2'
    os.environ['KIVY_TEXT'] = 'sdl2'
    os.environ['KIVY_LOG_LEVEL'] = 'debug'
    
    if 'DISPLAY' in os.environ:
        print(f"Minimal Test: DISPLAY environment variable was set to: {os.environ['DISPLAY']}. Unsetting it.")
        del os.environ['DISPLAY']
    else:
        print("Minimal Test: DISPLAY environment variable was not set.")

    print(f"Minimal Test: Env Vars Set -> SDL_VIDEODRIVER={os.environ.get('SDL_VIDEODRIVER')}, KIVY_WINDOW={os.environ.get('KIVY_WINDOW')}, KIVY_TEXT={os.environ.get('KIVY_TEXT')}, DISPLAY={os.environ.get('DISPLAY')}")

try:
    from kivy.config import Config
    if platform.system() == "Linux":
        print("Minimal Test: Applying Kivy Config settings.")
        Config.set('kivy', 'log_level', 'debug')
        print(f"Minimal Test: Config Set -> kivy:log_level={Config.get('kivy', 'log_level')}")

    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.core.window import Window

    print("Minimal Test: Kivy imported successfully.")

    class MinimalTestApp(App):
        def build(self):
            print(f"MinimalTestApp.build(): Kivy Window provider: {Window.__class__.__name__}")
            print(f"MinimalTestApp.build(): Window size: {Window.size}")
            actual_gl_backend = "Unknown"
            try:
                if hasattr(Window, 'backend_name'):
                     actual_gl_backend = Window.backend_name
                elif hasattr(Window, '_gl_backend_name'):
                     actual_gl_backend = Window._gl_backend_name
            except Exception as e:
                print(f"MinimalTestApp.build(): Error getting GL backend name: {e}")

            return Label(text=f"Kivy GL Test\nWindow: {Window.__class__.__name__}\nGL Backend (attempt): {actual_gl_backend}")

    if __name__ == '__main__':
        print("Minimal Test: Starting Kivy app...")
        MinimalTestApp().run()
        print("Minimal Test: Kivy app finished.")

except ImportError as e:
    print(f"Minimal Test: Failed to import Kivy modules: {e}")
    print("Minimal Test: Ensure Kivy is installed correctly in your virtual environment.")
except Exception as e:
    print(f"Minimal Test: An unexpected error occurred: {e}") 