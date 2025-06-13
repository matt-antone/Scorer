import os
import sys
import pytest
from kivy.config import Config

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Add the src directory to the Python path
src_dir = os.path.join(project_root, 'src')
sys.path.insert(0, src_dir)

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up the test environment with correct font paths."""
    # Get the absolute path to the pi_client directory
    pi_client_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pi_client'))
    
    # Add the pi_client directory to the Python path
    if pi_client_dir not in sys.path:
        sys.path.insert(0, pi_client_dir)
    
    # Set up Kivy font paths
    Config.set('kivy', 'font_dir', os.path.join(pi_client_dir, 'assets', 'fonts'))
    
    # Set up the test environment
    os.environ['KIVY_FONT_DIR'] = os.path.join(pi_client_dir, 'assets', 'fonts')
    
    yield
    
    # Clean up after tests
    if pi_client_dir in sys.path:
        sys.path.remove(pi_client_dir) 