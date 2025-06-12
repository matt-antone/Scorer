#!/usr/bin/env python3
"""
Script to run graphical tests on Raspberry Pi.
"""
import os
import sys
import time
from test_suite import test_suite

def main():
    """Run the graphical test suite."""
    print("Starting graphical tests...")
    print("This script must be run on a Raspberry Pi with a display.")
    print("Press Ctrl+C to stop the tests.")
    
    try:
        # Run the test suite
        success = test_suite()
        
        if success:
            print("\nAll tests passed!")
            sys.exit(0)
        else:
            print("\nSome tests failed.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nTests interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 