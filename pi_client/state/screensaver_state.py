from dataclasses import dataclass, field
import time

@dataclass
class ScreensaverState:
    enabled: bool = True
    active: bool = False
    image: str = 'default.jpg'
    timeout: int = 300  # seconds
    last_activity: float = field(default_factory=lambda: time.time())

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
        self.update_last_activity()

    def update_last_activity(self):
        self.last_activity = time.time()

    def should_activate(self) -> bool:
        return self.enabled and (time.time() - self.last_activity) > self.timeout 