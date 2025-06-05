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
    os.environ['KIVY_LOG_LEVEL'] = 'debug'
    
    if 'DISPLAY' in os.environ:
        print(f"Minimal Test: DISPLAY was {os.environ['DISPLAY']}. Unsetting.")
        del os.environ['DISPLAY']
    else:
        print("Minimal Test: DISPLAY was not set.")

    print(f"Minimal Test: Env Vars Set -> KIVY_WINDOW={os.environ.get('KIVY_WINDOW')}, KIVY_GRAPHICS_BACKEND={os.environ.get('KIVY_GRAPHICS_BACKEND')}, DISPLAY={os.environ.get('DISPLAY')}")

try:
    from kivy.config import Config
    if platform.system() == "Linux":
        print("Minimal Test: Applying Kivy Config settings.")
        Config.set('graphics', 'backend', 'egl_rpi')
        Config.set('kivy', 'log_level', 'debug')
        print(f"Minimal Test: Config Set -> graphics:backend={Config.get('graphics', 'backend')}, kivy:log_level={Config.get('kivy', 'log_level')}")

    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.core.window import Window
    import kivy.core.gl as KivyGL # Import Kivy GL module

    # Attempt to list available GL backends (this is somewhat internal)
    print("Minimal Test: Attempting to list Kivy GL backend providers...")
    try:
        # In Kivy, graphics backends are often registered and then chosen.
        # We can inspect kivy.graphics.cgl.cgl_get_backend_name() after initialization,
        # or look for registration functions if diving very deep.
        # For now, we rely on Kivy's own logging of "Backend used <...>"
        # and the success/failure of the app.
        # However, we can check the *requested* one if available
        # This might show what was requested by env var before it falls back
        print(f"Minimal Test: Kivy CGL requested backend (if available from env): {KivyGL.gl_get_backend_name()}")
    except Exception as e:
        print(f"Minimal Test: Could not get requested CGL backend name: {e}")

    class MinimalTestApp(App):
        def build(self):
            # The most reliable info comes from Kivy's own startup logs for "Backend used"
            # This print is more for confirming Window object properties after init.
            print(f"MinimalTestApp.build(): Kivy Window provider: {Window.__class__.__name__}") # Use class name to avoid missing attribute
            print(f"MinimalTestApp.build(): Window size: {Window.size}")
            return Label(text=f"Kivy GL Backend Test\nWindow System: {Window.__class__.__name__}")

    if __name__ == '__main__':
        print("Minimal Test: Starting Kivy app...")
        MinimalTestApp().run()
        print("Minimal Test: Kivy app finished.")

except ImportError as e:
    print(f"Minimal Test: Failed to import Kivy modules: {e}")
    print("Minimal Test: Ensure Kivy is installed correctly in your virtual environment.")
except Exception as e:
    print(f"Minimal Test: An unexpected error occurred: {e}") 