# Installation Script Changes

## Overview

The installation script (`install.sh`) has been updated to improve platform detection, add logging, and handle both macOS and Raspberry Pi environments properly.

## Changes Made

### 1. Platform Detection Improvements

- Added robust platform detection using both `/proc/device-tree/model` and `uname`
- Added explicit checks for file existence before attempting to read
- Added clear error messages for unsupported platforms
- Improved Raspberry Pi detection to handle different model strings

### 2. Logging System

- Added comprehensive logging to `install.log`
- Captures both standard output and error output
- Includes timestamps for installation start and completion
- Logs all installation steps and any errors that occur

### 3. Environment-Specific Dependencies

#### Raspberry Pi

- Uses `apt-get` for system dependencies
- Installs required SDL2 and FFmpeg libraries
- Handles display rotation configuration
- Uses system Python packages

#### macOS

- Uses Homebrew for system dependencies
- Installs specific version of FFmpeg (6.x)
- Sets up proper environment variables for FFmpeg
- Uses Homebrew's SDL2 packages

### 4. Error Handling

- Added root user check
- Added platform support validation
- Added dependency existence checks
- Improved error messages and logging

## Usage

The installation script can now be run on either platform:

```bash
./install.sh
```

The script will:

1. Detect the platform automatically
2. Install appropriate dependencies
3. Set up the Python virtual environment
4. Install Python packages
5. Configure display settings (on Raspberry Pi)
6. Log all operations to `install.log`

## Troubleshooting

If you encounter issues:

1. Check `install.log` for detailed error messages
2. Verify platform detection is working correctly
3. Ensure all required system packages are available
4. Check Python virtual environment creation
5. Verify FFmpeg and SDL2 installation

## Future Improvements

Potential areas for future enhancement:

1. Add progress indicators for long-running operations
2. Add rollback capability for failed installations
3. Add dependency version checking
4. Add configuration file support
5. Add more detailed logging options
