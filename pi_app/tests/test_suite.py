"""
Test suite for the Scorer application.
This module discovers and runs all test cases in the tests directory.
"""

import unittest
import os
import sys

def run_tests():
    """Discover and run all tests in the tests directory."""
    # Add the parent directory to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # Discover all tests in the pi_app/tests directory
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(os.path.abspath(os.path.dirname(__file__)), pattern='test_*.py')
    
    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return the result
    return result

if __name__ == '__main__':
    result = run_tests()
    sys.exit(not result.wasSuccessful()) 