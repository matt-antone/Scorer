import platform
import os
import sys

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

if platform.system() == "Linux":
    print("Minimal Test: Linux detected. Setting Kivy environment variables.")
    os.environ['KIVY_WINDOW'] = 'sdl2'
    os.environ['KIVY_GRAPHICS_BACKEND'] = 'egl_rpi'
    os.environ['KIVY_TEXT'] = 'sdl2'
    os.environ['KIVY_EGL_LIB'] = '/opt/vc/lib/libEGL.so'
    os.environ['KIVY_GLES_LIB'] = '/opt/vc/lib/libGLESv2.so'
    os.environ['KIVY_LOG_LEVEL'] = 'debug' # Force debug logging early
    
    # Try to ensure DISPLAY is not set for headless operation
    if 'DISPLAY' in os.environ:
        print(f"Minimal Test: DISPLAY environment variable was set to: {os.environ['DISPLAY']}. Unsetting it.")
        del os.environ['DISPLAY']
    else:
        print("Minimal Test: DISPLAY environment variable was not set.")

    print(f"Minimal Test: Env Vars Set -> KIVY_WINDOW={os.environ.get('KIVY_WINDOW')}, KIVY_GRAPHICS_BACKEND={os.environ.get('KIVY_GRAPHICS_BACKEND')}, DISPLAY={os.environ.get('DISPLAY')}")

# It's crucial to import Kivy *after* setting environment variables
try:
    from kivy.config import Config
    if platform.system() == "Linux":
        print("Minimal Test: Applying Kivy Config settings.")
        Config.set('graphics', 'backend', 'egl_rpi')
        Config.set('kivy', 'log_level', 'debug') # Redundant with env var, but safe
        print(f"Minimal Test: Config Set -> graphics:backend={Config.get('graphics', 'backend')}, kivy:log_level={Config.get('kivy', 'log_level')}")

    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.core.window import Window

    print(f"Minimal Test: Kivy Window provider detected by Kivy: {Window.backend_name if hasattr(Window, 'backend_name') else 'N/A before App run'}")
    # Note: Window.graphics_system might not be populated until the window is created.

    class MinimalTestApp(App):
        def build(self):
            print(f"MinimalTestApp.build(): Kivy Window provider: {Window.backend_name}")
            # Attempt to get more detailed graphics system info if available
            gl_backend_used = "N/A"
            try:
                from kivy.graphics import gl_init_symbols
                gl_backend_used = Window.graphics_system
            except Exception as e:
                print(f"MinimalTestApp.build(): Error getting graphics_system: {e}")
                
            print(f"MinimalTestApp.build(): Kivy GL Backend reported: {gl_backend_used}")
            print(f"MinimalTestApp.build(): Window size: {Window.size}")
            return Label(text=f"Kivy Backend Test\nWindow: {Window.backend_name}\nGL: {gl_backend_used}")

    if __name__ == '__main__':
        print("Minimal Test: Starting Kivy app...")
        MinimalTestApp().run()
        print("Minimal Test: Kivy app finished.")

except ImportError as e:
    print(f"Minimal Test: Failed to import Kivy modules: {e}")
    print("Minimal Test: Ensure Kivy is installed correctly in your virtual environment.")
except Exception as e:
    print(f"Minimal Test: An unexpected error occurred: {e}") 