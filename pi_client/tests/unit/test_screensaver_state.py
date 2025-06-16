import unittest
import time
from pi_client.state.screensaver_state import ScreensaverState

class TestScreensaverState(unittest.TestCase):
    def setUp(self):
        self.state = ScreensaverState()

    def test_initial_state(self):
        self.assertTrue(self.state.enabled)
        self.assertFalse(self.state.active)
        self.assertEqual(self.state.image, 'default.jpg')
        self.assertEqual(self.state.timeout, 300)

    def test_activate(self):
        self.state.activate()
        self.assertTrue(self.state.active)

    def test_deactivate(self):
        self.state.activate()
        self.state.deactivate()
        self.assertFalse(self.state.active)

    def test_update_last_activity(self):
        old_time = self.state.last_activity
        time.sleep(0.01)
        self.state.update_last_activity()
        self.assertGreater(self.state.last_activity, old_time)

    def test_should_activate(self):
        self.state.last_activity = time.time() - 301
        self.assertTrue(self.state.should_activate())
        self.state.last_activity = time.time()
        self.assertFalse(self.state.should_activate()) 