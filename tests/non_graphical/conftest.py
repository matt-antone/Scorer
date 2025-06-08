"""
This conftest.py contains hooks specifically for non-graphical tests.
It patches Kivy's core components to prevent any window creation,
allowing tests of business logic to run headlessly.
"""
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def mock_kivy_core():
    """
    This fixture automatically patches Kivy's core modules for every test.
    It stops the event loop and window creation, which is essential for
    running tests without a graphical interface.
    """
    # Mock the entire Window object to prevent any real windowing system interaction
    mock_window = MagicMock()
    mock_window.size = (800, 600)
    
    # We patch the getter of the property, not the property itself
    with patch('kivy.core.window.Window', mock_window), \
         patch('kivy.base.EventLoopBase.ensure_window', lambda *args: mock_window), \
         patch('kivy.base.EventLoopBase.run', lambda *args: None):
        yield 