import os
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.app import App


class ScreensaverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.billboard_path = 'assets/billboards'
        self.image_files = []
        self.current_image_index = 0
        self.slideshow_event = None
        self.images_shown = 0
        self.max_images_to_show = 0

        layout = FloatLayout()
        self.image_widget_front = Image(fit_mode='fill', opacity=1)
        self.image_widget_back = Image(fit_mode='fill', opacity=0)
        layout.add_widget(self.image_widget_back)
        layout.add_widget(self.image_widget_front)
        self.add_widget(layout)

        if os.path.isdir(self.billboard_path):
            self.image_files = [os.path.join(self.billboard_path, f) for f in os.listdir(self.billboard_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if self.image_files:
                random.shuffle(self.image_files) # Randomize the list
        
        if not self.image_files:
            self.remove_widget(layout)
            self.add_widget(Label(text="No billboard images found in assets/billboards", font_size='20sp'))
        else:
            self.image_widget_front.source = self.image_files[0]

    def start_slideshow(self):
        self.stop_slideshow() # Ensure no old events are running
        if len(self.image_files) > 1:
            # Set the initial image for the back widget to avoid a black screen on first transition
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.image_widget_back.source = self.image_files[self.current_image_index]
            self.slideshow_event = Clock.schedule_interval(self.next_slide, 5)

    def stop_slideshow(self):
        if self.slideshow_event:
            self.slideshow_event.cancel()
            self.slideshow_event = None
        # Also cancel any running animations to prevent them from finishing on leave
        Animation.cancel_all(self.image_widget_front)
        Animation.cancel_all(self.image_widget_back)


    def next_slide(self, dt):
        # The back image is already loaded from the previous call or start_slideshow
        # Animate the front image to transparent and the back image to opaque
        anim_front = Animation(opacity=0, duration=2)
        anim_back = Animation(opacity=1, duration=2)

        anim_back.bind(on_complete=self._on_animation_complete)
        anim_front.start(self.image_widget_front)
        anim_back.start(self.image_widget_back)

    def _on_animation_complete(self, animation, widget):
        self.images_shown += 1
        if self.max_images_to_show > 0 and self.images_shown >= self.max_images_to_show:
            self._finish_slideshow()
            return

        # Swap the widgets
        self.image_widget_front, self.image_widget_back = self.image_widget_back, self.image_widget_front
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        self.image_widget_back.source = self.image_files[self.current_image_index]

    def _finish_slideshow(self, *args):
        """Safely tells the main app to exit the screensaver."""
        app = App.get_running_app()
        if app and app.root.current == 'screensaver':
            # This app method handles returning to the correct screen and resetting the timer
            app.reset_inactivity_timer()

    def on_enter(self, *args):
        # Reset state for a fresh slideshow every time
        self.images_shown = 0
        self.image_widget_front.opacity = 1
        self.image_widget_back.opacity = 0

        if self.image_files:
            # Re-shuffle, reset index, and set the first image
            random.shuffle(self.image_files)
            self.current_image_index = 0
            self.image_widget_front.source = self.image_files[self.current_image_index]
            
            # Set the counter and limit for this run
            self.images_shown = 1
            self.max_images_to_show = len(self.image_files) * 2

            # Check if we should exit immediately (e.g., only 1 image)
            if self.images_shown >= self.max_images_to_show:
                 Clock.schedule_once(self._finish_slideshow, 5) # Show the 1 image for 5s then exit
            else:
                self.start_slideshow()
        else:
            # If there are no images, exit immediately.
            Clock.schedule_once(self._finish_slideshow)

    def on_leave(self, *args):
        self.stop_slideshow() 