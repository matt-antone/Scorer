import unittest
from pi_client.state.settings_state import SettingsState

class TestSettingsState(unittest.TestCase):
    def setUp(self):
        self.state = SettingsState()

    def test_default_theme(self):
        self.assertEqual(self.state.theme['primary_color'], '#FF0000')
        self.assertEqual(self.state.theme['background_color'], '#FFFFFF')

    def test_default_screensaver(self):
        self.assertTrue(self.state.screensaver['enabled'])
        self.assertEqual(self.state.screensaver['timeout'], 300)
        self.assertEqual(self.state.screensaver['image'], 'default.jpg')

    def test_update_setting(self):
        self.state.update_setting('theme', 'primary_color', '#00FF00')
        self.assertEqual(self.state.theme['primary_color'], '#00FF00')
        self.state.update_setting('screensaver', 'timeout', 600)
        self.assertEqual(self.state.screensaver['timeout'], 600)
        with self.assertRaises(AttributeError):
            self.state.update_setting('nonexistent', 'foo', 'bar') 