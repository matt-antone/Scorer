from dataclasses import dataclass, field
from typing import Dict

@dataclass
class SettingsState:
    theme: Dict = field(default_factory=lambda: {
        'primary_color': '#FF0000',
        'secondary_color': '#0000FF',
        'background_color': '#FFFFFF',
        'text_color': '#000000'
    })
    screensaver: Dict = field(default_factory=lambda: {
        'enabled': True,
        'timeout': 300,
        'image': 'default.jpg'
    })
    sound: Dict = field(default_factory=lambda: {
        'enabled': True,
        'volume': 0.7,
        'effects': True,
        'music': True
    })
    display: Dict = field(default_factory=lambda: {
        'fullscreen': True,
        'orientation': 'landscape',
        'resolution': {'width': 800, 'height': 480}
    })

    def update_setting(self, category: str, key: str, value):
        if hasattr(self, category):
            getattr(self, category)[key] = value
        else:
            raise AttributeError(f"Unknown settings category: {category}") 