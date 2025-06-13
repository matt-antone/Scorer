"""
Test suite for the Scorer application.
This module discovers and runs all test cases in the tests directory.
"""

import unittest
import os
import sys
import traceback

# Ensure the project root is on sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class DetailedTestRunner(unittest.TextTestRunner):
    """Custom test runner that provides detailed error information."""
    
    def _makeResult(self):
        return DetailedTestResult(self.stream, self.descriptions, self.verbosity)

class DetailedTestResult(unittest.TextTestResult):
    """Custom test result that provides detailed error information."""
    
    def addError(self, test, err):
        """Called when an error occurs during test execution."""
        super().addError(test, err)
        self.stream.writeln("\nDetailed Error Information:")
        self.stream.writeln("=" * 80)
        self.stream.writeln(f"Test: {test}")
        self.stream.writeln(f"Error Type: {err[0].__name__}")
        self.stream.writeln(f"Error Message: {err[1]}")
        self.stream.writeln("\nTraceback:")
        self.stream.writeln("".join(traceback.format_tb(err[2])))
        self.stream.writeln("=" * 80)
    
    def addFailure(self, test, err):
        """Called when a test fails."""
        super().addFailure(test, err)
        self.stream.writeln("\nDetailed Failure Information:")
        self.stream.writeln("=" * 80)
        self.stream.writeln(f"Test: {test}")
        self.stream.writeln(f"Failure Type: {err[0].__name__}")
        self.stream.writeln(f"Failure Message: {err[1]}")
        self.stream.writeln("\nTraceback:")
        self.stream.writeln("".join(traceback.format_tb(err[2])))
        self.stream.writeln("=" * 80)

def run_tests():
    """Discover and run all tests in the tests directory."""
    # Add the parent directory to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    # Add pi_client to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pi_client')))
    
    # Discover all tests in the pi_app/tests directory
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(os.path.abspath(os.path.dirname(__file__)), pattern='test_*.py')
    
    # Run the tests with our custom runner
    test_runner = DetailedTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return the result
    return result

if __name__ == '__main__':
    result = run_tests()
    sys.exit(not result.wasSuccessful()) 