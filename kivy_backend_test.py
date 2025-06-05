import platform
import os
import sys

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

if platform.system() == "Linux":
    print("Minimal Test: Linux detected. Setting Kivy environment variables for SDL2/KMSDRM.")
    os.environ['KIVY_WINDOW'] = 'sdl2'
    os.environ['KIVY_TEXT'] = 'sdl2'
    os.environ['KIVY_LOG_LEVEL'] = 'debug'
    
    if 'DISPLAY' in os.environ:
        print(f"Minimal Test: DISPLAY environment variable was set to: {os.environ['DISPLAY']}. Unsetting it.")
        del os.environ['DISPLAY']
    else:
        print("Minimal Test: DISPLAY environment variable was not set.")

    print(f"Minimal Test: Env Vars Set -> KIVY_WINDOW={os.environ.get('KIVY_WINDOW')}, KIVY_TEXT={os.environ.get('KIVY_TEXT')}, DISPLAY={os.environ.get('DISPLAY')}")

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

            return Label(text=f"Kivy GL Test\\nWindow: {Window.__class__.__name__}\\nGL Backend (attempt): {actual_gl_backend}")

    if __name__ == '__main__':
        print("Minimal Test: Starting Kivy app...")
        MinimalTestApp().run()
        print("Minimal Test: Kivy app finished.")

except ImportError as e:
    print(f"Minimal Test: Failed to import Kivy modules: {e}")
    print("Minimal Test: Ensure Kivy is installed correctly in your virtual environment.")
except Exception as e:
    print(f"Minimal Test: An unexpected error occurred: {e}") 